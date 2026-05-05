# src/features/solar_physics.py

def add_solar_features(df):
    import numpy as np
    import pandas as pd

    df = df.copy()
    df["datetime"] = pd.to_datetime(df["datetime"])

    df["day_of_year"] = df["datetime"].dt.dayofyear
    df["hour"] = df["datetime"].dt.hour + df["datetime"].dt.minute / 60

    lat_rad = np.radians(df["lat"])

    decl = np.radians(23.45) * np.sin(
        2 * np.pi * (284 + df["day_of_year"]) / 365
    )

    hour_angle = np.radians((df["hour"] - 12) * 15)

    elevation = np.arcsin(
        np.sin(lat_rad) * np.sin(decl) +
        np.cos(lat_rad) * np.cos(decl) * np.cos(hour_angle)
    )

    elevation = np.clip(elevation, -np.pi/2, np.pi/2)

    df["solar_elevation"] = elevation

    #  DAY/NIGHT FIX (VERY IMPORTANT)
    df["is_day"] = (elevation > 0).astype(int)

    zenith = (np.pi / 2) - elevation
    cos_zenith = np.cos(zenith)
    cos_zenith = np.clip(cos_zenith, 0.01, 1)

    I_sc = 1367
    d_r = 1 + 0.033 * np.cos(2 * np.pi * df["day_of_year"] / 365)

    air_mass = 1 / cos_zenith
    tau = 0.75 ** (air_mass ** 0.4)

    clear_sky = I_sc * d_r * cos_zenith * tau

    # 🚫 NIGHT = ZERO
    clear_sky[df["is_day"] == 0] = 0

    df["clear_sky_ghi"] = np.clip(clear_sky, 0, 1200)

    return df



