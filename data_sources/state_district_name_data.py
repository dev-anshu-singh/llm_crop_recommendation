from geopy.geocoders import Nominatim


def get_state_and_district(lat, lon) -> dict:

    # input -> latitude, longitude (float)
    # output -> dictionary return {"state": state,"district": district}

    geolocator = Nominatim(user_agent="geoapi", timeout=10)

    # Reverse geocoding
    location = geolocator.reverse((lat, lon), language="en")

    if location is None:
        return None

    # Extract address components
    address = location.raw.get("address", {})
    state = address.get("state", None)
    district = address.get("county") or address.get("district")

    return {
        "state": state,
        "district": district
    }

# print(get_state_and_district(25.5045,86.4701))