# src/services/device_optimizer.py

import numpy as np
from config.config import DEVICE_CONFIG
from src.features.solar_logic import adjusted_yield


# ---------------------------
# 🔋 DEVICE CONFIG FETCHER
# ---------------------------

def get_device_config(device_type):
    """
    Get device configuration safely
    """
    return DEVICE_CONFIG.get(device_type, DEVICE_CONFIG["powerwall"])


# ---------------------------
# 🧠 FIX: REQUIRED FOR PREDICT.PY
# ---------------------------

def get_device_recommendation(device_type):
    """
    Alias for compatibility with predict.py
    """
    return get_device_config(device_type)


# ---------------------------
# ⚡ DEVICE OUTPUT CALCULATION
# ---------------------------

def calculate_device_output(
    ghi,
    cloud_cover,
    temp,
    device_type="powerwall"
):
    """
    Calculate real-world energy output (kWh)
    """

    config = get_device_config(device_type)

    output = adjusted_yield(
        ghi=ghi,
        cloud_cover=cloud_cover,
        temp=temp,
        area=config["area"],
        efficiency=config["efficiency"]
    )

    return float(output)


# ---------------------------
# 📊 TIME SERIES OUTPUT
# ---------------------------

def generate_device_timeseries(
    ghi_values,
    cloud_values,
    temp_values,
    device_type="powerwall"
):
    """
    Generate device output for full forecast timeline
    """

    outputs = []

    for ghi, cloud, temp in zip(ghi_values, cloud_values, temp_values):
        outputs.append(
            calculate_device_output(
                ghi,
                cloud,
                temp,
                device_type
            )
        )

    return outputs


# ---------------------------
# 🎯 DEVICE PERFORMANCE STATUS
# ---------------------------

def get_device_status(peak_ghi):
    """
    High-level recommendation
    """

    if peak_ghi >= 800:
        return "⚡ Optimal Charging (Max Efficiency)"
    elif peak_ghi >= 600:
        return "☀️ Good Performance"
    elif peak_ghi >= 400:
        return "🌤️ Moderate Output"
    else:
        return "⚠️ Low Efficiency"


# ---------------------------
# 🧠 DEVICE RECOMMENDATION ENGINE
# ---------------------------

def recommend_device_action(
    ghi,
    cloud_cover,
    temp,
    device_type="powerwall"
):
    """
    Smart suggestion engine
    """

    config = get_device_config(device_type)
    threshold = config["threshold"]

    output = calculate_device_output(
        ghi,
        cloud_cover,
        temp,
        device_type
    )

    if ghi >= threshold:
        action = "⚡ Use device now (good solar window)"
    elif ghi >= threshold * 0.7:
        action = "🌤️ Acceptable, but not optimal"
    else:
        action = "⏳ Wait for better sunlight"

    heat_alert = "🔥 Cooling required" if temp > 35 else "✅ Temp normal"

    cloud_alert = (
        "☁️ Efficiency drop >30% — reposition device"
        if cloud_cover > 60 else "☀️ Clear conditions"
    )

    return {
        "device": device_type,
        "estimated_output_kwh": round(output, 3),
        "action": action,
        "heat_alert": heat_alert,
        "cloud_alert": cloud_alert
    }


# ---------------------------
# 🏆 BEST DEVICE COMPARISON
# ---------------------------

def compare_devices(
    ghi,
    cloud_cover,
    temp
):
    """
    Compare all devices and return best one
    """

    results = {}

    for device in DEVICE_CONFIG.keys():
        output = calculate_device_output(
            ghi,
            cloud_cover,
            temp,
            device
        )

        results[device] = output

    best_device = max(results, key=results.get)

    return {
        "best_device": best_device,
        "outputs": {k: round(v, 3) for k, v in results.items()}
    }


