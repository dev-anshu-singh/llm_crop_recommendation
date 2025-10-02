import json
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_community.vectorstores import FAISS
from data_sources.state_district_name_data import get_state_and_district
from llm import llm_model
import config
import utils
from data_sources import soil_api_services, weather_api_service, state_district_name_data, static_district_data_source, static_data
from llm.prompt import crop_recommendation_prompt
from datetime import datetime

vector_store = FAISS.load_local(
    config.FAISS_INDEX_PATH,
    llm_model.gemini_embedding_model,
    allow_dangerous_deserialization=True
)

agro_zone_retriever = vector_store.as_retriever(
    search_kwargs={
        'k': 2,
        'filter': {
            'type': 'agro_climatic_zone_docs'
        }
    }
)

# 1. Location Chain (No change here)
location_chain = RunnableLambda(
    lambda x: {
        'location': get_state_and_district(x['latitude'], x['longitude']),
        'query': f"{get_state_and_district(x['latitude'], x['longitude'])['state']} {get_state_and_district(x['latitude'], x['longitude'])['district']}"
    }
)

# 2. Parallel Data Retrieval (Modified)
# This part ONLY retrieves data that depends on the location information.
location_dependent_retrieval = RunnableParallel(
    other_env_data=RunnableLambda(
        lambda x: json.dumps(static_district_data_source.get_district_info(x['location']['district']), indent=2)),
    agro_climatic_context=RunnableLambda(lambda x: utils.get_retrieved_context(agro_zone_retriever, x['query'])),
)

# 3. Full Chain (Restructured)
full_chain = (
    # Step 1: Prepare initial inputs
        {
            "latitude": lambda x: x["latitude"],
            "longitude": lambda x: x["longitude"],
            "farm_plot_size": lambda x: x["farm_plot_size"],
            "irrigation_type": lambda x: ", ".join(x["irrigation_type"]) if x.get("irrigation_type") else "None",
            "previous_crop": lambda x: x["previous_crop"],
            "soil_test_values": lambda x: x["soil_test_values"],
            "excluded_crops": lambda x: x["excluded_crops"] or "None",
            "date": lambda x: x["date"],
            "fertilizer_recommendation": lambda x: x["fertilizer_recommendation"],
            "msp_prices": lambda x: x["msp_prices"]
        }
        # Step 2: Add location and query to the dictionary.
        # Now the main dictionary contains 'latitude', 'longitude', 'location', and 'query'.
        | RunnablePassthrough.assign(
    location_data=location_chain
)
        # The output of location_chain is {'location': {...}, 'query': '...'}
        # RunnablePassthrough.assign will merge this into the main dictionary.
        # We now have access to x['location_data']['location'] and x['location_data']['query']

        # Step 3: Now run all parallel tasks.
        # Pass through existing keys and run new retrievals.
        | RunnableParallel(
    # Pass through all existing data
    farm_plot_size=lambda x: x["farm_plot_size"],
    irrigation_type=lambda x: x["irrigation_type"],
    previous_crop=lambda x: x["previous_crop"],
    excluded_crops=lambda x: x["excluded_crops"],
    msp_prices=lambda x: x["msp_prices"],
    fertilizer_recommendation=lambda x: x["fertilizer_recommendation"],
    date=lambda x: x["date"],
    location=lambda x: x["location_data"]["location"],  # Extract from the nested dict

    # Now run retrievals that depend on location or other inputs
    soil_test_values=RunnableLambda(
        lambda x: x['soil_test_values'] or soil_api_services.get_soil_properties(x['latitude'], x['longitude'])),
    weather_data=RunnableLambda(lambda x: weather_api_service.get_daily_weather(x['latitude'], x['longitude'])),
    other_env_data=RunnableLambda(
        lambda x: json.dumps(static_district_data_source.get_district_info(x['location_data']['location']['district']),
                             indent=2)),
    agro_climatic_context=RunnableLambda(
        lambda x: utils.get_retrieved_context(agro_zone_retriever, x['location_data']['query'])),
)
        # Step 4: Final steps
        | crop_recommendation_prompt
        | llm_model.gemini_structured_llm
)