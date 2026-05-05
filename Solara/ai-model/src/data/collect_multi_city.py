from src.data.fetch_real_data import fetch_nasa_data
from src.data.providers import openweather_hourly
from src.data.geocode import get_lat_lon
import pandas as pd
import os

API_KEY = os.getenv("OPENWEATHER_API_KEY")


def collect_for_city(city_name):
    print(f"🌍 Fetching data for: {city_name}")

    lat, lon = get_lat_lon(city_name)

    if lat is None:
        return pd.DataFrame()

    nasa_df = fetch_nasa_data(lat, lon)
    weather_df = openweather_hourly(lat, lon, API_KEY)

    if nasa_df.empty or weather_df.empty:
        print("❌ Data fetch failed")
        return pd.DataFrame()

    merged = pd.merge_asof(
        nasa_df.sort_values("datetime"),
        weather_df.sort_values("datetime"),
        on="datetime",
        direction="nearest"
    )

    merged["city"] = city_name

    return merged


if __name__ == "__main__":
    df = collect_for_city("Kolkata")
    print(df.head())



