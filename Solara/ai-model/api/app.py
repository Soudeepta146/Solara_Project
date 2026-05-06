# app.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "message": "Solara AI Backend Running Successfully 🚀"
    }

from pydantic import BaseModel

import numpy as np
import pandas as pd
import joblib
import json
import requests

from datetime import datetime
from tensorflow.keras.models import load_model
from config.config import SEQ_LENGTH, DEVICE_CONFIG
from src.data.fetch_real_data import fetch_nasa_data
from src.utils.scaler import transform_data
from src.utils.sequences import create_inference_sequence, generate_time_labels
from src.features.solar_physics import add_solar_features
from src.services.solar_window import generate_device_windows

# ---------------------------
# PATH
# ---------------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODEL_DIR = os.path.join(BASE_DIR, "models")

# ---------------------------
# LOAD MODELS
# ---------------------------
print("🚀 Loading models...")

model1 = load_model(os.path.join(MODEL_DIR, "lstm_v2.keras"))
model2 = load_model(os.path.join(MODEL_DIR, "lstm_v2.keras"))

scaler = joblib.load(os.path.join(MODEL_DIR, "scaler.pkl"))

with open(os.path.join(MODEL_DIR, "features.json"), "r") as f:
    FEATURES = json.load(f)

print("✅ Features loaded")

# ---------------------------
# INPUT MODEL
# ---------------------------
class LocationInput(BaseModel):
    lat: float
    lon: float
    device: str = "solar_car"

# ---------------------------
# FEATURE ENGINEERING
# ---------------------------
def build_features(df):
    df["datetime"] = pd.to_datetime(df["datetime"])

    df["hour"] = df["datetime"].dt.hour
    df["day_of_year"] = df["datetime"].dt.dayofyear

    df["hour_sin"] = np.sin(2 * np.pi * df["hour"] / 24)
    df["hour_cos"] = np.cos(2 * np.pi * df["hour"] / 24)

    df["doy_sin"] = np.sin(2 * np.pi * df["day_of_year"] / 365)
    df["doy_cos"] = np.cos(2 * np.pi * df["day_of_year"] / 365)

    df = add_solar_features(df)

    df = df.ffill().bfill()

    return df

# ---------------------------
# MAIN API
# ---------------------------
@app.post("/predict")
def predict(data: LocationInput):

    try:
        lat = data.lat
        lon = data.lon
        device_type = data.device

        print(f"📍 Request: {lat}, {lon} | Device: {device_type}")

        # ---------------------------
        # 1️⃣ FETCH DATA
        # ---------------------------
        print("STEP 1: Fetching data...")
        df = fetch_nasa_data(lat, lon)
        print("STEP 2: Data fetched:", df.head() if df is not None else "None")

        if df is None or df.empty:
            return {"status": "error", "message": "No data available"}

        # ---------------------------
        # 2️⃣ FEATURES
        # ---------------------------
        df = build_features(df)

        for col in FEATURES:
            if col not in df.columns:
                df[col] = 0

        X = df[FEATURES]

        # ---------------------------
        # 3️⃣ SCALE + SEQUENCE
        # ---------------------------
        scaled = transform_data(X, scaler, FEATURES)
        seq = create_inference_sequence(scaled, SEQ_LENGTH)

        # ---------------------------
        # 4️⃣ MODEL PREDICTION
        # ---------------------------
        pred1 = model1.predict(seq, verbose=0)[0]
        pred2 = model2.predict(seq, verbose=0)[0]

        residual = (pred1 + pred2) / 2

        # ---------------------------
        # 5️⃣ FINAL GHI
        # ---------------------------
        clear_sky = df["clear_sky_ghi"].values[-len(residual):]
        final_ghi = clear_sky + residual

        final_ghi = np.maximum(0, final_ghi)
        final_ghi = pd.Series(final_ghi).rolling(3, min_periods=1).mean().values
        final_ghi = np.clip(final_ghi, 0, 1200)

        # ---------------------------
        # 6️⃣ TIME LABELS
        # ---------------------------
        last_time = df["datetime"].iloc[-1]
        time_labels = generate_time_labels(last_time, len(final_ghi))

        # ---------------------------
        # 7️⃣ WINDOWS
        # ---------------------------
        device_config = DEVICE_CONFIG.get(device_type, DEVICE_CONFIG["powerwall"])

        window_data = generate_device_windows(
            time_labels,
            final_ghi,
            device_config
        )

        best = window_data.get("best_window")

        # ---------------------------
        #  PEAK TIME
        # ---------------------------
        peak_time = None
        if best:
            peak_time = {
                "start": best["start"].strftime("%H:%M"),
                "end": best["end"].strftime("%H:%M"),
                "avg_ghi": round(best["avg_ghi"], 2),
                "label": "Best Time for Solar Usage ☀️"
            }

        # ---------------------------
        # TODAY SUMMARY
        # ---------------------------
        total_solar_hours = 0
        best_hours_str = "No strong solar window"
        worst_hours_str = "18:00 - 06:00"

        if window_data.get("windows"):
            for w in window_data["windows"]:
                duration = (w["end"] - w["start"]).total_seconds() / 3600
                total_solar_hours += duration

            if best:
                best_hours_str = f"{best['start'].strftime('%H:%M')} - {best['end'].strftime('%H:%M')}"

        today_summary = {
            "best_hours": best_hours_str,
            "worst_hours": worst_hours_str,
            "total_solar_hours": round(total_solar_hours, 2)
        }

        # ---------------------------
        #  CONFIDENCE
        # ---------------------------
        agreement = np.exp(-np.mean(np.abs(pred1 - pred2)))

        cloud = df["cloud_cover"].iloc[-1]
        cloud_factor = 1 - (cloud / 100)

        variability = np.std(final_ghi) / (np.mean(final_ghi) + 1e-6)
        stability = np.exp(-variability)

        confidence = float(np.clip(
            (0.6 * agreement + 0.25 * cloud_factor + 0.15 * stability) * 100,
            0, 100
        ))

        # ---------------------------
        #  LOCATION NAME
        # ---------------------------
        location_name = "Unknown"
        try:
            geo = requests.get(
                "https://nominatim.openstreetmap.org/reverse",
                params={"lat": lat, "lon": lon, "format": "json"},
                headers={"User-Agent": "solara-app"},
                timeout=5
            ).json()

            addr = geo.get("address", {})

            location_name = (
                addr.get("city")
                or addr.get("town")
                or addr.get("village")
                or addr.get("state")
                or geo.get("display_name", "Unknown")
            )

        except Exception as e:
            print("Geo error:", e)

        # ---------------------------
        #  SMART ALERTS (UPGRADED)
        # ---------------------------

        alerts = []

        
        # Use the mean value for consistency with the dashboard display
        avg_ghi = np.mean(final_ghi)

        # 1. Category: Solar Status (Mutually Exclusive)
        if avg_ghi < 20:
            alerts.append("🌙 No solar activity currently")
        elif avg_ghi < 300:
            alerts.append("⚠️ Low solar generation expected")
        elif avg_ghi < 700:
            alerts.append("🌞 Good solar conditions now")
        else:alerts.append("⚡ Peak solar generation — best time to use devices")
    
       
        #  cloud impact
        cloud = df["cloud_cover"].iloc[-1]
        if cloud > 30:
            alerts.append("⛅ Efficiency Alert: Scattered clouds detected. Yield may drop by >30%.")
        elif cloud > 70:
            alerts.append("☁️ Heavy clouds may reduce efficiency")
        elif cloud > 40:
            alerts.append("🌥 Partial cloud cover detected")

        # ---------------------------
        #  FINAL RESPONSE
        # ---------------------------
        return {
            "location": location_name,
            "lat": lat,
            "lon": lon,
            "irradiance": round(float(np.mean(final_ghi)), 2),
            "ghi_forecast": final_ghi.tolist(),  # <--- ADD THIS LINE (must be a list)
            "cloud_cover": float(cloud), 
            "analysis": {
                "status": "High" if np.mean(final_ghi) > 600 else "Low",
                "confidence": round(confidence, 1),
                "alerts": alerts
            },

            "solar_windows": [
                {
                    "start": w["start"].strftime("%H:%M"),
                    "end": w["end"].strftime("%H:%M"),
                    "quality": w["type"]
                }
                for w in window_data.get("windows", [])
            ],

            "peak_time": peak_time,
            "today_summary": today_summary
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
    
if __name__ == "__main__":
    import uvicorn
    import os
    # This looks for a PORT assigned by Render, defaults to 8000 for local testing
    port = int(os.environ.get("PORT", 8000)) 
    uvicorn.run(app, host="0.0.0.0", port=port)



