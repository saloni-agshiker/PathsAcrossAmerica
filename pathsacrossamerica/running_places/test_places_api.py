from dotenv import load_dotenv
import os
import requests

#loads.env file
load_dotenv()

#retrieve api key from variable in env file
key = os.getenv("MAPS_API_KEY")

#Google Maps Static API URL & place_id
place_id = "ChIJj61dQgK6j4AR4GeTYWZsKWw"
url = f"https://places.googleapis.com/v1/places/{place_id}?fields=id,displayName&key={key}"

#return json file
headers = {
    "Content-Type": "application/json",
}

response = requests.get(url, headers=headers)

#prints response
if response.status_code == 200:
    print(response.json())  #json response
else:
    print("Error:", response.status_code)
    print(response.text)