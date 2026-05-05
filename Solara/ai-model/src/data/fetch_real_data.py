import requests
import pandas as pd

def fetch_nasa_data(lat, lon):
    url = "https://power.larc.nasa.gov/api/temporal/hourly/point"

    params = {
        "parameters": "ALLSKY_SFC_SW_DWN,T2M,RH2M",
        "community": "RE",
        "longitude": lon,
        "latitude": lat,
        "start": "20230101",
        "end": "20231231",
        "format": "JSON"
    }

    try:
        res = requests.get(url, params=params, timeout=15)
        # res.raise_for_status()
        data = res.json()

        ghi = data["properties"]["parameter"]["ALLSKY_SFC_SW_DWN"]
        temp = data["properties"]["parameter"]["T2M"]
        humidity = data["properties"]["parameter"]["RH2M"]

        rows = []

        for t in ghi:
            rows.append({
                "datetime": pd.to_datetime(t, format="%Y%m%d%H"),
                "ghi": ghi[t],
                "temp": temp[t],
                "humidity": humidity[t],
                "cloud_cover": 20,  # fallback
                "lat": lat,
                "lon": lon
            })

        df = pd.DataFrame(rows)

        if df.empty:
            raise ValueError("NASA returned empty data")

        return df

    except Exception as e:
        print(f"❌ NASA API failed for {lat},{lon}: {e}")
        return pd.DataFrame()



