from dotenv import load_dotenv
import os
import requests


load_dotenv()
API_KEY = os.getenv("MAPS_API_KEY")
url = f"https://addressvalidation.googleapis.com/v1:validateAddress?key={API_KEY}"


# Minimal‐validation test addresses
test_addresses = [
   {
       "regionCode": "US",
       "locality": "Cupertino",
       "administrativeArea": "CA",
       "postalCode": "95014",
       "addressLines": ["1 Infinite Loop"]
   },
   {
       "regionCode": "US",
       "locality": "New York",
       "administrativeArea": "NY",
       "postalCode": "10005",
       "addressLines": ["11 Wall Street"]
   },
   {
       "regionCode": "US",
       "locality": "Atlanta",
       "administrativeArea": "GA",
       "postalCode": "30309",
       "addressLines": ["48 Morningside Drive"]
   }
]


for addr in test_addresses:
   resp = requests.post(url, json={"address": addr}, timeout=5)


   if resp.status_code != 200:
       print(f"❌ {addr['addressLines'][0]} → HTTP {resp.status_code}")
       continue


   result = resp.json().get("result", {})
   loc = result.get("geocode", {}).get("location", {})


   lat = loc.get("latitude")
   lng = loc.get("longitude")


   if lat is not None and lng is not None:
       print(f"✅ {addr['addressLines'][0]} → Lat: {lat}, Lng: {lng}")
   else:
       print(f"❌ {addr['addressLines'][0]} → no geocode returned")




