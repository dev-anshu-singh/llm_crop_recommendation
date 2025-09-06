import requests
import config

BASE_URL = config.SOIL_API_BASE_URL

def get_soil_properties(lat: float, lon: float,
                        properties: list = ["N", "P", "K"],
                        endpoint: str = "gridded",
                        nearby: bool = True) -> dict:
    """
    Query SIS India API for soil properties and return only selected values.

    Args:
        lat (float): Latitude
        lon (float): Longitude
        properties (list): List of soil properties to request (default: ["N", "P", "K"])
        endpoint (str): One of ["gridded", "mandal", "district"]
        nearby (bool): For gridded data, whether to enable nearby pixel search

    Returns:
        dict: Dictionary with requested soil property values
    """
    url = f"{BASE_URL}/properties/query/{endpoint}"

    # Build query params
    params = {"lat": lat, "lon": lon}
    if nearby and endpoint == "gridded":
        params["nearby"] = "true"

    for prop in properties:
        params.setdefault("properties", [])
        params["properties"].append(prop)

    # Send request
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception(f"API call failed: {response.status_code} {response.text}")

    data = response.json()

    try:
        soil_props = data["features"][0]["properties"]["soil_properties"]
        # Keep only requested properties
        result = {}
        for prop in properties:
            value = soil_props.get(prop)
            result[prop] = round(value, 2) if value is not None else None
        return result
    except (KeyError, IndexError):
        return {prop: None for prop in properties}

# print(get_soil_properties(lat=25.5045,lon=86.4701))