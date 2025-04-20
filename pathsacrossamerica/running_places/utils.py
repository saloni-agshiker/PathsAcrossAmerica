import requests
import googlemaps
import math
from django.conf import settings

MAPS_API_KEY = settings.MAPS_API_KEY

def validate_address(address: str):
    """
    Uses Google’s Address Validation API.
    Returns (latitude, longitude) if response includes coordinates,
    otherwise returns (None, None).
    """
    url = f"https://addressvalidation.googleapis.com/v1:validateAddress?key={MAPS_API_KEY}"
    payload = {
        "address": {
            "addressLines": [address]
        }
    }

    try:
        resp = requests.post(url, json=payload, timeout=5)
        resp.raise_for_status()
    except requests.RequestException:
        return None, None

    result = resp.json().get("result", {})
    loc = result.get("geocode", {}).get("location", {})
    lat = loc.get("latitude")
    lng = loc.get("longitude")

    if lat is not None and lng is not None:
        return lat, lng

    return None, None



def geocode_address(address: str):
    """
    Uses the Google Maps Geocoding API to retrieve lat/lng.
    Returns (latitude, longitude) of the first geocoded result,
    or (None, None) if nothing is found.
    """
    gmaps = googlemaps.Client(key=MAPS_API_KEY)
    results = gmaps.geocode(address)
    if not results:
        return None, None

    loc = results[0]["geometry"]["location"]
    return loc.get("lat"), loc.get("lng")


def haversine_distance(lat1, lng1, lat2, lng2):
    R = 3959
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lng2 - lng1)

    a = (math.sin(d_phi / 2) **2
         + math.cos(phi1)*math.cos(phi2)*math.sin(d_lambda / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance