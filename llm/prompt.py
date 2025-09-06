from langchain.prompts import PromptTemplate

crop_recommendation_prompt = PromptTemplate(
    input_variables=[
        "location",
        "farm_plot_size",
        "irrigation_type",
        "soil_test_values",
        "previous_crop",
        "excluded_crops"
        "weather_data",
        "other_env_data",
        "fertilizer_recommendation",
        "msp_prices",
        "agro_climatic_context",
        "date"
    ],
    template="""
You are an Indian agricultural expert helping a farmer decide the most suitable crop for their farm.

## User & Farm Information:
- Date: {date}
- Location: {location}
- Farm plot size: {farm_plot_size} hectares
- Irrigation type(s): {irrigation_type}
- Previous crop: {previous_crop}
- Soil Test (NPK values): {soil_test_values}

## Weather & Environmental Data of previous 7 days and forecast of next 7 days:
{weather_data}

Other important information:
{other_env_data}

## Soil nutrient Recommendation according to crop:
{fertilizer_recommendation}

## Market Prices (MSP and current trends):
{msp_prices}

These crops should not be recommended: {excluded_crops}

---
### Task:
Carefully read and understand the significance of the above technical information about the farm and also general info provided.
Your answer should be based on date, location, farm plot size, irrigation type, previous crop, soil test values, weather data (previous 7 days and next 7 days),
labour cost, irrigation area of that district, month wise rainfall data, groundwater level data and on production data of different
crops in that particular area. Try to connect and relate all this data and information.
**If you are unable to decide just keep your recommendation based on production data of different crops in that particular area keep more produced crop higher.**
Based on the above information, recommend **at least 6 suitable crops** for the farmer.
Use the above information and also your own knowledge in appropriate manner.
Consider every provided information and also take crop rotation in your consideration for at least one crop.
Rank them in order of suitability (1 = best option).
Give reason that on which of the above factor you chose that crop as suitable.

Make sure your output follows the schema exactly.
"""
)
