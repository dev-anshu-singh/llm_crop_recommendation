from datetime import datetime
from schemas.input_output_schema import UserInput
from . import chain
from data_sources.static_data import load_msp_data, load_fertilizer_data

def generate_recommendation(user_input: UserInput):
    """
    Prepares the input dictionary and generates crop recommendations by
    invoking the main LCEL chain.
    """
    # Convert the Pydantic model to a dictionary to feed it into the chain.
    input_dict = user_input.dict()

    # Add static data that doesn't depend on the user's direct input
    # These will be passed along but are only used by the prompt template at the end.
    input_dict["date"] = datetime.now().strftime("%Y-%m-%d")
    input_dict["fertilizer_recommendation"] = load_fertilizer_data()
    input_dict["msp_prices"] = load_msp_data()

    # Invoke the chain with the prepared input
    return chain.full_chain.invoke(input_dict)
