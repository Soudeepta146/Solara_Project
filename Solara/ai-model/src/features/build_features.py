# src/features/build_features.py

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import pandas as pd
import numpy as np

from config.config import DEFAULT_VALUES, MAX_GHI, MIN_GHI
from src.features.solar_physics import add_solar_features
from src.features.solar_logic import adjusted_yield


INPUT_PATH = "data/processed/dataset.csv"
OUTPUT_PATH = "data/processed/dataset_features.csv"


def build_features():
    print("🚀 Starting feature engineering...")

    df = pd.read_csv(INPUT_PATH)

    # --------------------------
    # BASIC CLEANING
    # --------------------------
    df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")

    # Fill missing essential columns
    for col, val in DEFAULT_VALUES.items():
        if col not in df.columns:
            df[col] = val

    # Clip unrealistic values
    df["ghi"] = df["ghi"].clip(MIN_GHI, MAX_GHI)

    # --------------------------
    #  TIME FEATURES
    # --------------------------
    df["hour"] = df["datetime"].dt.hour
    df["day_of_year"] = df["datetime"].dt.dayofyear

    df["hour_sin"] = np.sin(2 * np.pi * df["hour"] / 24)
    df["hour_cos"] = np.cos(2 * np.pi * df["hour"] / 24)

    df["doy_sin"] = np.sin(2 * np.pi * df["day_of_year"] / 365)
    df["doy_cos"] = np.cos(2 * np.pi * df["day_of_year"] / 365)

    # --------------------------
    #  SOLAR PHYSICS FEATURES
    # --------------------------
    df = add_solar_features(df)

    # --------------------------
    #  DERIVED FEATURES
    # --------------------------

    # ratio of actual vs theoretical sunlight
    df["ghi_ratio"] = df["ghi"] / (df["clear_sky_ghi"] + 1e-6)

    # normalized cloud impact
    df["cloud_impact"] = df["cloud_cover"] / 100.0

    # temperature efficiency drop (simple physics approx)
    df["temp_effect"] = 1 - ((df["temp"] - 25) * 0.004)

    # final solar output estimation
    df["solar_output"] = adjusted_yield(
        df["ghi"],
        df["cloud_cover"]
    ) * df["temp_effect"]

    # stability feature (important for confidence later)
    df["ghi_rolling_std"] = df["ghi"].rolling(window=4, min_periods=1).std()

    # --------------------------
    #  CLEANING
    # --------------------------
    df = df.replace([np.inf, -np.inf], np.nan)

    df = df.ffill().bfill()

    # Drop rows where datetime failed
    df = df.dropna(subset=["datetime"])

    # --------------------------
    #  SAVE
    # --------------------------
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    print("✅ Feature engineering complete")
    print("📊 Shape:", df.shape)
    print("🧠 Columns:", df.columns.tolist())


if __name__ == "__main__":
    build_features()









# # import sys, os
# # sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
# import pandas as pd
# import numpy as np

# from src.features.solar_physics import add_solar_features
# from src.features.solar_logic import adjusted_yield


# INPUT_PATH = "data/processed/dataset.csv"
# OUTPUT_PATH = "data/processed/dataset_features.csv"


# def build_features():
#     df = pd.read_csv(INPUT_PATH)

#     df["datetime"] = pd.to_datetime(df["datetime"])

#     # --------------------------
#     # TIME FEATURES
#     # --------------------------
#     df["hour"] = df["datetime"].dt.hour
#     df["day_of_year"] = df["datetime"].dt.dayofyear

#     df["hour_sin"] = np.sin(2 * np.pi * df["hour"] / 24)
#     df["hour_cos"] = np.cos(2 * np.pi * df["hour"] / 24)

#     df["doy_sin"] = np.sin(2 * np.pi * df["day_of_year"] / 365)
#     df["doy_cos"] = np.cos(2 * np.pi * df["day_of_year"] / 365)

#     # --------------------------
#     # SOLAR PHYSICS
#     # --------------------------
#     df = add_solar_features(df)

#     # --------------------------
#     # DERIVED FEATURES
#     # --------------------------
#     df["ghi_ratio"] = df["ghi"] / (df["clear_sky_ghi"] + 1e-6)

#     df["solar_output"] = adjusted_yield(
#         df["ghi"],
#         df["cloud_cover"]
#     )

#     # --------------------------
#     # CLEANING
#     # --------------------------
#     df = df.replace([np.inf, -np.inf], np.nan)
#     df = df.ffill().bfill()

#     # --------------------------
#     # SAVE
#     # --------------------------
#     df.to_csv(OUTPUT_PATH, index=False)

#     print("✅ Feature engineering complete")
#     print("📊 Shape:", df.shape)
#     print("🧠 Columns:", df.columns.tolist())


# if __name__ == "__main__":
#     build_features()








# # src/features/build_features.py

# import pandas as pd
# import numpy as np
# from src.features.solar_physics import add_solar_features


# def build_features():

#     df = pd.read_csv("data/processed/dataset.csv")

#     df['datetime'] = pd.to_datetime(df['datetime'])

#     # -----------------------------
#     # TIME FEATURES
#     # -----------------------------
#     df['hour'] = df['datetime'].dt.hour
#     df['day_of_year'] = df['datetime'].dt.dayofyear

#     # 🔥 IMPORTANT (YOU WERE MISSING THIS)
#     df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)
#     df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)

#     df['doy_sin'] = np.sin(2 * np.pi * df['day_of_year'] / 365)
#     df['doy_cos'] = np.cos(2 * np.pi * df['day_of_year'] / 365)

#     # -----------------------------
#     # SOLAR PHYSICS
#     # -----------------------------
#     df = add_solar_features(df)

#     df = df.ffill().bfill()

#     df.to_csv("data/processed/dataset.csv", index=False)

#     print("✅ Features added:", df.columns.tolist())


# if __name__ == "__main__":
#     build_features()








# # src/features/build_features.py
# # src/features/build_features.py

# import pandas as pd
# import numpy as np
# from src.features.solar_physics import add_solar_features

# def build_features():
#     df = pd.read_csv("data/processed/dataset.csv")
#     df['datetime'] = pd.to_datetime(df['datetime'])

#     # ---- TIME FEATURES ----
#     df['hour'] = df['datetime'].dt.hour
#     df['day_of_year'] = df['datetime'].dt.dayofyear

#     # cyclic encodings
#     df['hour_sin'] = np.sin(2*np.pi*df['hour']/24)
#     df['hour_cos'] = np.cos(2*np.pi*df['hour']/24)
#     df['doy_sin']  = np.sin(2*np.pi*df['day_of_year']/365)
#     df['doy_cos']  = np.cos(2*np.pi*df['day_of_year']/365)

#     # ---- SOLAR PHYSICS ----
#     df = add_solar_features(df)

#     # clean
#     df = df.ffill().bfill()

#     df.to_csv("data/processed/dataset.csv", index=False)
#     print("✅ Features:", df.columns.tolist(), df.shape)

# if __name__ == "__main__":
#     build_features()








# import pandas as pd
# import numpy as np
# from src.features.solar_physics import add_solar_features


# def build_features():
#     print("🚀 Building features...")

#     df = pd.read_csv("data/processed/dataset.csv")

#     df['datetime'] = pd.to_datetime(df['datetime'])

#     # -----------------------------
#     # TIME FEATURES
#     # -----------------------------
#     df['hour'] = df['datetime'].dt.hour

#     df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)
#     df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)

#     # -----------------------------
#     # SOLAR PHYSICS FEATURES
#     # -----------------------------
#     df = add_solar_features(df)

#     # -----------------------------
#     # CLEANING
#     # -----------------------------
#     df = df.ffill().bfill()

#     # -----------------------------
#     # SAVE
#     # -----------------------------
#     df.to_csv("data/processed/dataset.csv", index=False)

#     print("✅ Features added:", df.shape)
#     print("Columns:", df.columns.tolist())


# if __name__ == "__main__":
#     build_features()