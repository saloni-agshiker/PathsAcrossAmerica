from dotenv import load_dotenv
import os
import requests
from PIL import Image
from io import BytesIO

#loads.env file
load_dotenv()

#retrieve api key from variable in env file
key = os.getenv("MAPS_API_KEY")
location = "Atlanta, Georgia"

#Google Maps Static API URL
url = f"https://maps.googleapis.com/maps/api/staticmap?center={location}&zoom=12&size=600x400&key={key}"

#makes request
response = requests.get(url)

if response.status_code == 200:
    img = Image.open(BytesIO(response.content))
    img.show()  #opens the map image in your system's image viewer
else:
    print("Error:", response.status_code, response.text)