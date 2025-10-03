# from geopy.geocoders import Nominatim
#
#
# def get_state_and_district(lat, lon) -> dict:
#
#     # input -> latitude, longitude (float)
#     # output -> dictionary return {"state": state,"district": district}
#
#     geolocator = Nominatim(user_agent="geoapi", timeout=10)
#
#     # Reverse geocoding
#     location = geolocator.reverse((lat, lon), language="en")
#
#     if location is None:
#         return None
#
#     # Extract address components
#     address = location.raw.get("address", {})
#     state = address.get("state", None)
#     district = address.get("county") or address.get("district")
#
#     return {
#         "state": state,
#         "district": district
#     }
#
# # print(get_state_and_district(25.5045,86.4701))

from geopy.geocoders import Photon
from geopy.exc import GeocoderTimedOut, GeocoderServiceError


def get_state_and_district(lat, lon) -> dict:
    try:
        # Use Photon instead of Nominatim
        geolocator = Photon(user_agent="crop_recommendation_api")

        location = geolocator.reverse((lat, lon), timeout=15)

        if location is None:
            return {"state": "Unknown", "district": "Unknown"}

        address = location.raw.get("properties", {})
        state = address.get("state", "Unknown")
        district = address.get("county") or address.get("district") or "Unknown"

        return {"state": state, "district": district}

    except (GeocoderTimedOut, GeocoderServiceError) as e:
        print(f"Geocoding error: {e}")
        return {"state": "Unknown", "district": "Unknown"}
    except Exception as e:
        print(f"Unexpected error in geocoding: {e}")
        return {"state": "Unknown", "district": "Unknown"}


# print(get_state_and_district(25,86))