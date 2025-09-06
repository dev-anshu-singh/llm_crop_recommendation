import openmeteo_requests
import requests_cache
from retry_requests import retry
import json
import pandas as pd

cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)


def get_daily_weather(latitude: float, longitude: float) -> str:
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": [
            "temperature_2m",
            "rain",
            "precipitation",
            "soil_moisture_1_to_3cm",
            "soil_temperature_6cm"
        ],
        "past_days": 7,
        "forecast_days": 7,
        "timezone": "auto"
    }

    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]

    # --- Hourly data ---
    hourly = response.Hourly()
    hourly_data = {
        "date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left"
        ),
        "temperature_2m": hourly.Variables(0).ValuesAsNumpy(),
        "rain": hourly.Variables(1).ValuesAsNumpy(),
        "precipitation": hourly.Variables(2).ValuesAsNumpy(),
        "soil_moisture_1_to_3cm": hourly.Variables(3).ValuesAsNumpy(),
        "soil_temperature_6cm": hourly.Variables(4).ValuesAsNumpy()
    }

    hourly_df = pd.DataFrame(data=hourly_data)

    # Fix timezone
    tz = response.Timezone()
    if isinstance(tz, bytes):
        tz = tz.decode("utf-8")
    hourly_df["date"] = hourly_df["date"].dt.tz_convert(tz)

    # --- Aggregate to daily data ---
    daily_df = hourly_df.groupby(hourly_df["date"].dt.date).agg(
        temp_min=("temperature_2m", "min"),
        temp_max=("temperature_2m", "max"),
        rain_sum=("rain", "sum"),
        soil_temp_min=("soil_temperature_6cm", "min"),
        soil_temp_max=("soil_temperature_6cm", "max"),
        soil_moisture_min=("soil_moisture_1_to_3cm", "min"),
        soil_moisture_max=("soil_moisture_1_to_3cm", "max"),
    ).reset_index().rename(columns={"date": "day"})

    daily_df = daily_df.round(2)

    # Convert day to string for JSON serialization
    daily_df["day"] = daily_df["day"].astype(str)

    # Add ranges
    daily_df["temp_range_C"] = list(zip(daily_df["temp_min"], daily_df["temp_max"]))
    daily_df["soil_temp_6cm_range_C"] = list(zip(daily_df["soil_temp_min"], daily_df["soil_temp_max"]))
    daily_df["soil_moisture_1-3cm_range_m3"] = list(zip(daily_df["soil_moisture_min"], daily_df["soil_moisture_max"]))

    # Keep only desired columns
    daily_df = daily_df[["day", "temp_range_C", "rain_sum",
                         "soil_temp_6cm_range_C", "soil_moisture_1-3cm_range_m3"]]

    # --- Convert to JSON ---
    records = daily_df.to_dict(orient="records")
    json_output = json.dumps(records, indent=2, ensure_ascii=False)

    return json_output

# print(get_daily_weather(latitude=25.5045,longitude=86.4701))
