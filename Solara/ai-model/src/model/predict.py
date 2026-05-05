# src/model/predict.py

import os
import numpy as np
import pandas as pd
import joblib

from dotenv import load_dotenv
from tensorflow.keras.models import load_model

from config.config import FEATURES, SEQ_LENGTH
from src.data.providers import openweather_hourly, tomorrow_hourly
from src.features.solar_physics import add_solar_features

# =========================
# LOAD ENV
# =========================
load_dotenv()

# =========================
# LOAD MODEL + SCALER
# =========================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "lstm_v2.keras")
SCALER_PATH = os.path.join(BASE_DIR, "models", "scaler.pkl")

model = load_model(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

# =========================
# CLASSIFY WINDOWS
# =========================
def classify_window(avg_ghi):
    if avg_ghi > 700:
        return "PEAK Performance⚡"
    elif avg_ghi > 400:
        return "GOOD Performance☀️"
    elif avg_ghi > 100:
        return "LOW Performance 🌤️"
    else:
        return "OFF 🌙 No Solar Activity"
    
# =========================
# DEVICE STATUS FUNCTION
# =========================
def get_device_status(y_pred):
    peak = max(y_pred)

    if peak > 700:
        return "⚡ Peak Performance"
    elif peak > 400:
        return "☀️ Good Performance"
    elif peak > 100:
        return "🌤️ Low Performance"
    else:
        return "🌙 No Solar Activity"


# =========================
# MAIN PREDICT FUNCTION
# =========================
def predict(lat, lon, device_type="solar_car"):

    # -----------------------------
    # 1. FETCH WEATHER DATA
    # -----------------------------
    try:
        df = tomorrow_hourly(lat, lon, os.getenv("TOMORROW_API_KEY"))
        if df.empty:
            raise Exception("Tomorrow empty")
        print("✅ Using Tomorrow.io data")
    except:
        df = openweather_hourly(lat, lon, os.getenv("OPENWEATHER_API_KEY"))
        print("⚠️ Using OpenWeather fallback")

    if df.empty:
        return {"status": "error", "message": "No weather data available"}

    # -----------------------------
    # 2. DATETIME CLEANING
    # -----------------------------
    # df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")

    df["datetime"] = pd.to_datetime(df["datetime"], utc=True)
    df["datetime"] = df["datetime"].dt.tz_convert("Asia/Kolkata")

    # filter only next 24 hours
    now = pd.Timestamp.now(tz="Asia/Kolkata")
    df = df[df["datetime"] >= now]
    df = df[df["datetime"] <= now + pd.Timedelta(hours=24)]
    
    df = df.reset_index(drop=True)
    df = df.dropna(subset=["datetime"]).sort_values("datetime").reset_index(drop=True)

    # -----------------------------
    # 3. TIME FEATURES (CRITICAL)
    # -----------------------------
    df["hour"] = df["datetime"].dt.hour
    df["dayofyear"] = df["datetime"].dt.dayofyear

    df["hour_sin"] = np.sin(2 * np.pi * df["hour"] / 24)
    df["hour_cos"] = np.cos(2 * np.pi * df["hour"] / 24)

    df["doy_sin"] = np.sin(2 * np.pi * df["dayofyear"] / 365)
    df["doy_cos"] = np.cos(2 * np.pi * df["dayofyear"] / 365)

    # -----------------------------
    # 4. LOCATION FEATURES
    # -----------------------------
    df["lat"] = lat
    df["lon"] = lon

    # -----------------------------
    # 5. SOLAR PHYSICS FEATURES
    # -----------------------------
    df = add_solar_features(df)

    # -----------------------------
    # 7. ENSURE ALL FEATURES EXIST
    # -----------------------------
    missing = [col for col in FEATURES if col not in df.columns]
    if missing:
        raise ValueError(f"❌ Missing features: {missing}")

    # -----------------------------
    # 8. PREPARE INPUT
    # -----------------------------
    X = df[FEATURES].astype(np.float32)

    print("✅ Input shape:", X.shape)

    # -----------------------------
    # 9. SCALE DATA
    # -----------------------------
    X_scaled = scaler.transform(X)

    # -----------------------------
    # 10. CREATE SEQUENCE
    # -----------------------------
    if len(X_scaled) < SEQ_LENGTH:
        raise ValueError("❌ Not enough data for LSTM sequence")

    X_seq = X_scaled[-SEQ_LENGTH:]
    X_seq = np.expand_dims(X_seq, axis=0)

    # -----------------------------
    # 11. PREDICT
    # -----------------------------
    y_pred = model.predict(X_seq)[0]

    # residual model fix
    y_pred = np.maximum(y_pred, 0)

    # -----------------------------
    # 12. DEVICE OUTPUT
    # -----------------------------
    if device_type.lower() == "ev":
        device_output = y_pred * 0.8
    elif device_type.lower() == "solar_car":
        device_output = y_pred * 0.6
    elif device_type.lower() == "powerwall":
        device_output = y_pred * 0.9
    else:
        device_output = y_pred

    # -----------------------------
    # 13. TIME LABELS
    # -----------------------------
    last_time = df["datetime"].iloc[-1]

    time_labels = [
        (last_time + pd.Timedelta(minutes=15 * i)).strftime("%Y-%m-%d %H:%M")
        for i in range(len(y_pred))
    ]

    # FORCE NIGHT ZERO (VERY IMPORTANT)
    for i, t in enumerate(time_labels):
        hour = int(t.split(" ")[1].split(":")[0])
        if hour < 6 or hour > 18:
            y_pred[i] = 0
    # df.loc[(df["hour"] < 6) | (df["hour"] > 18), "clear_sky_ghi"] = 0

    # -----------------------------
    # 14. WINDOWS
    # -----------------------------
    windows = []
    step = 6  # 1.5 hr

    for i in range(0, len(y_pred) - step, step):
        avg_ghi = np.mean(y_pred[i:i + step])

        windows.append({
            "start": time_labels[i],
            "end": time_labels[i + step - 1],
            "avg_ghi": float(avg_ghi),
            "type": classify_window(avg_ghi)
        })

    # -----------------------------
    # 15. FINAL RESPONSE
    # -----------------------------
    return {
        "status": "success",
        "location": {"lat": lat, "lon": lon},
        "device": device_type,
        "ghi_forecast": y_pred.tolist(),
        "time_labels": time_labels,
        "solar_windows": windows,
        "device_output_series": device_output.tolist(),
        "device_status": get_device_status(y_pred),
        "peak_value": float(max(y_pred))
    }


