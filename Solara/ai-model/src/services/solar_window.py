# src/services/solar_window.py

import numpy as np
from datetime import timedelta

from config.config import TIME_INTERVAL_MIN


# ---------------------------
# 🎯 CLASSIFY IRRADIANCE
# ---------------------------

def classify_window(avg_ghi):
    if avg_ghi >= 800:
        return "PEAK ⚡"
    elif avg_ghi >= 600:
        return "GOOD ☀️"
    elif avg_ghi >= 400:
        return "MODERATE 🌤️"
    else:
        return "LOW ❌"


# ---------------------------
# 🧠 CORE WINDOW ENGINE
# ---------------------------

def generate_solar_windows(
    timestamps,
    ghi_values,
    threshold=600,
    min_duration=30
):
    """
    Generate solar windows based on threshold

    Args:
        timestamps: list of datetime
        ghi_values: list of predicted GHI
        threshold: device-specific threshold
        min_duration: minimum valid window (minutes)

    Returns:
        list of windows
    """

    windows = []
    current_window = None
    ghi_bucket = []

    for t, ghi in zip(timestamps, ghi_values):

        if ghi >= threshold:
            if current_window is None:
                current_window = {
                    "start": t,
                    "end": t
                }
                ghi_bucket = [ghi]
            else:
                current_window["end"] = t
                ghi_bucket.append(ghi)

        else:
            if current_window:
                duration = (current_window["end"] - current_window["start"]).total_seconds() / 60

                if duration >= min_duration:
                    avg_ghi = float(np.mean(ghi_bucket))

                    windows.append({
                        "start": current_window["start"],
                        "end": current_window["end"],
                        "duration_min": int(duration),
                        "avg_ghi": round(avg_ghi, 2),
                        "type": classify_window(avg_ghi)
                    })

                current_window = None
                ghi_bucket = []

    # last window check
    if current_window:
        duration = (current_window["end"] - current_window["start"]).total_seconds() / 60

        if duration >= min_duration:
            avg_ghi = float(np.mean(ghi_bucket))

            windows.append({
                "start": current_window["start"],
                "end": current_window["end"],
                "duration_min": int(duration),
                "avg_ghi": round(avg_ghi, 2),
                "type": classify_window(avg_ghi)
            })

    return windows


# ---------------------------
# 🏆 BEST WINDOW SELECTOR
# ---------------------------

def get_best_window(windows):
    """
    Select best window based on avg_ghi + duration
    """

    if not windows:
        return None

    return max(
        windows,
        key=lambda w: (w["avg_ghi"] * 0.7 + w["duration_min"] * 0.3)
    )


# ---------------------------
# 🔋 DEVICE-SPECIFIC WINDOWS
# ---------------------------

def generate_device_windows(
    timestamps,
    ghi_values,
    device_config
):
    """
    Generate windows for specific device
    """

    threshold = device_config["threshold"]

    windows = generate_solar_windows(
        timestamps,
        ghi_values,
        threshold=threshold
    )

    best_window = get_best_window(windows)

    return {
        "windows": windows,
        "best_window": best_window
    }


# ---------------------------
# ⚡ ALERT GENERATION
# ---------------------------

def generate_alerts(windows, current_time):
    """
    Generate smart alerts
    """

    alerts = []

    for w in windows:
        start_diff = (w["start"] - current_time).total_seconds() / 60

        if 0 < start_diff <= 30:
            alerts.append(
                f"⚡ Solar window starts in {int(start_diff)} minutes"
            )

    return alerts




