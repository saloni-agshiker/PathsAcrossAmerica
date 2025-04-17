from geopy.geocoders import Nominatim
import math

def geocode_address(address: str):
    geolocator = Nominatim(user_agent='pathsacrossamerica')
    location = geolocator.geocode(address)
    if location:
        return (location.latitude, location.longitude)
    return (None, None)

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

