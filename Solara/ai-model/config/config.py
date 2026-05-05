# # config/config.py

# ---------------------------
#  MODEL CONFIG
# ---------------------------
SEQ_LENGTH = 24              # past 24 timesteps
PRED_STEPS = 96             # next 24 hours (15 min interval)
# ---------------------------
# SOLAR THRESHOLDS
# ---------------------------
PEAK_THRESHOLD = 600        # strong sunlight (EV charging)
OPTIMAL_THRESHOLD = 550     # good for storage devices
LOW_THRESHOLD = 200         # poor sunlight
TIME_INTERVAL_MIN = 15      # prediction resolution
# ---------------------------
#  DEVICE PROFILES
# ---------------------------
DEVICE_CONFIG = {
    "solar_car": {
        "efficiency": 0.22,
        "threshold": 600,
        "area": 3.0
    },
    "solar_light": {
        "efficiency": 0.18,
        "threshold": 400,
        "area": 0.2
    },
    "powerwall": {
        "efficiency": 0.20,
        "threshold": 500,
        "area": 1.5
    }
}
# ---------------------------
#  MODEL INPUT FEATURES
# ---------------------------
FEATURES = [
    'temp',
    'humidity',
    'cloud_cover',
    'hour_sin',
    'hour_cos',
    'doy_sin',
    'doy_cos',
    'lat',
    'lon',
    'clear_sky_ghi',
    'aod',
    'pressure',
    'wind_speed'
]
# ---------------------------
#  TARGET CONFIG
# ---------------------------
TARGET = "ghi"  # model predicts residual (ghi - clear_sky_ghi)
# ---------------------------
# ⚙️ DATA SAFETY LIMITS
# ---------------------------
DEFAULT_VALUES = {
    "cloud_cover": 50,
    "aod": 0.1,
    "pressure": 1013,
    "wind_speed": 1.5
}
MAX_GHI = 1200
MIN_GHI = 0
# ---------------------------
# CONFIDENCE ENGINE
# ---------------------------
CONF_WEIGHTS = {
    "agreement": 0.6,   # ensemble agreement
    "cloud": 0.25,      # cloud uncertainty
    "stability": 0.15   # time-series smoothness
}
# ---------------------------
# 🚀 SOLAR WINDOW CONFIG
# ---------------------------
WINDOW_MIN_DURATION = 30   # minimum usable window (minutes)
SMOOTHING_FACTOR = 3       # for prediction smoothing



