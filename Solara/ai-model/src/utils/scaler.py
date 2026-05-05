# src/utils/scaler.py
# src/utils/scaler.py
# src/utils/scaler.py

from sklearn.preprocessing import MinMaxScaler
import numpy as np
import pandas as pd


# ---------------------------
# 🧠 TRAIN SCALER
# ---------------------------

def scale_data(df):
    """
    Fit scaler on training data and return scaled data + scaler
    """

    if not isinstance(df, pd.DataFrame):
        raise ValueError("Input must be a pandas DataFrame")

    # fill missing values
    df = df.ffill().bfill()

    scaler = MinMaxScaler()

    scaled = scaler.fit_transform(df.values.astype(np.float32))

    return scaled, scaler


# ---------------------------
# 🔄 TRANSFORM (PREDICTION)
# ---------------------------

def transform_data(df, scaler, expected_features=None):
    """
    Transform new data using trained scaler

    Args:
        df: new input dataframe
        scaler: fitted scaler
        expected_features: list of features used in training
    """

    if not isinstance(df, pd.DataFrame):
        raise ValueError("Input must be a pandas DataFrame")

    # --------------------------
    # FEATURE ALIGNMENT
    # --------------------------
    if expected_features is not None:
        for col in expected_features:
            if col not in df.columns:
                df[col] = 0  # safe fallback

        df = df[expected_features]

    # --------------------------
    # CLEANING
    # --------------------------
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.ffill().bfill()

    # --------------------------
    # TRANSFORM
    # --------------------------
    return scaler.transform(df.values.astype(np.float32))


# ---------------------------
# 🔙 INVERSE TRANSFORM
# ---------------------------

def inverse_transform(data, scaler):
    """
    Convert scaled data back to original scale
    """

    data = np.array(data, dtype=np.float32)

    return scaler.inverse_transform(data)


# ---------------------------
# 🧪 DEBUG HELPER
# ---------------------------

def validate_features(df, expected_features):
    """
    Debug utility to ensure feature consistency
    """

    missing = [col for col in expected_features if col not in df.columns]

    if missing:
        print(f"⚠️ Missing features: {missing}")
    else:
        print("✅ All features present")










# from sklearn.preprocessing import MinMaxScaler
# import numpy as np


# def scale_data(df):
#     """
#     Fit scaler on training data
#     """
#     scaler = MinMaxScaler()

#     scaled = scaler.fit_transform(df.values.astype(np.float32))

#     return scaled, scaler


# def transform_data(df, scaler):
#     """
#     Use same scaler during prediction
#     """
#     return scaler.transform(df.values.astype(np.float32))


# def inverse_transform(data, scaler):
#     """
#     Convert scaled data back to original (optional use)
#     """
#     return scaler.inverse_transform(data)







# from sklearn.preprocessing import MinMaxScaler

# def scale_data(df):
#     scaler = MinMaxScaler()
#     scaled = scaler.fit_transform(df)
#     return scaled, scaler