from django.contrib.sites import requests
from geopy.geocoders import Nominatim
import googlemaps
import math

from pathsacrossamerica.pathsacrossamerica.settings import MAPS_API_KEY


def geocode_address(address: str):
    geolocator = Nominatim(user_agent='pathsacrossamerica')
    location = geolocator.geocode(address)
    if location:
        return (location.latitude, location.longitude)
    return (None, None)

def geocode_address(address: str):
    gmaps = googlemaps.Client(key=MAPS_API_KEY)
    geocode_result = gmaps.geocode(address)
    return geocode_result

def address_validation(address: str):
    url = f"https://addressvalidation.googleapis.com/v1:validateAddress?key={MAPS_API_KEY}"
    headers = {
        "Content-Type": "application/json",
    }

    response = requests.get(url, headers=headers)

    # prints response
    if response.status_code == 200:
        formatted_address = response.json().get("result", {}).get("address", {}).get("formattedAddress")
        location = response.json().get("result", {}).get("geocode", {}).get("location", {})
        latitude = location.get("latitude")
        longitude = location.get("longitude")

    else:
        print("Error:", response.status_code)
        print(response.text)

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

