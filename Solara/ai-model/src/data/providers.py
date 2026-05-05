# src/data/providers.py

import requests
import pandas as pd


# -------------------------------
#  OPENWEATHER (fallback)
# -------------------------------
def openweather_hourly(lat, lon, api_key):
    url = "https://api.openweathermap.org/data/2.5/forecast"

    params = {
        "lat": lat,
        "lon": lon,
        "appid": api_key,
        "units": "metric"
    }

    try:
        res = requests.get(url, params=params, timeout=10)
        data = res.json()

        if "list" not in data:
            raise ValueError(data)

        rows = []

        for item in data["list"]:
            rows.append({
                "datetime": pd.to_datetime(item["dt_txt"]),
                "temp": item["main"]["temp"],
                "humidity": item["main"]["humidity"],
                "cloud_cover": item["clouds"]["all"],
                "pressure": item["main"].get("pressure", 0),
                "wind_speed": item["wind"].get("speed", 0),
                "ghi": 0,   # fallback
                "aod": 0
            })

        df = pd.DataFrame(rows)
        return df

    except Exception as e:
        print(f"❌ OpenWeather failed: {e}")
        return pd.DataFrame()


# -------------------------------
#  TOMORROW.IO (PRIMARY)
# -------------------------------
def tomorrow_hourly(lat, lon, api_key):
    """
    Correct & stable Tomorrow.io API
    """

    url = "https://api.tomorrow.io/v4/weather/forecast"

    params = {
        "location": f"{lat},{lon}",
        "apikey": api_key,
        "timesteps": "1h",
        "fields": "temperature,humidity,cloudCover,solarGHI,pressureSurfaceLevel,windSpeed"
    }

    try:
        res = requests.get(url, params=params, timeout=10)
        data = res.json()

        # 🔴 DEBUG (VERY IMPORTANT)
        print("DEBUG TOMORROW RESPONSE:", data)

        if "timelines" not in data:
            raise ValueError(f"❌ Invalid Tomorrow response: {data}")

        rows = []

        for item in data["timelines"]["hourly"]:
            values = item.get("values", {})

            rows.append({
                "datetime": item.get("time"),
                "temp": values.get("temperature", 0),
                "humidity": values.get("humidity", 0),
                "cloud_cover": values.get("cloudCover", 0),
                "ghi": values.get("solarGHI", 0),
                "pressure": values.get("pressureSurfaceLevel", 0),
                "wind_speed": values.get("windSpeed", 0),
                "aod": 0
            })

        df = pd.DataFrame(rows)

        # 🔴 SAFETY CHECK (FIX YOUR ERROR)
        if df.empty or "datetime" not in df.columns:
            raise ValueError("❌ Tomorrow returned empty or invalid data")

        df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")

        return df

    except Exception as e:
        print(f"❌ Tomorrow.io failed: {e}")
        return pd.DataFrame()



