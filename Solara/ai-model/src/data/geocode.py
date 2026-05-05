# src/data/geocode.py

import requests

def get_lat_lon(city):
    url = "https://api.openweathermap.org/geo/1.0/direct"

    params = {
        "q": city,
        "limit": 1,
        "appid": "YOUR_API_KEY"   # replace later with env
    }

    try:
        res = requests.get(url, params=params, timeout=10)
        data = res.json()

        if not data:
            raise ValueError("City not found")

        lat = data[0]["lat"]
        lon = data[0]["lon"]

        return lat, lon

    except Exception as e:
        print(f"❌ Geocoding failed: {e}")
        return None, None