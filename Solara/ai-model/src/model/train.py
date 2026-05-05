# # src/model/train.py

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import pandas as pd
import numpy as np
import joblib
import json

from config.config import SEQ_LENGTH, PRED_STEPS, FEATURES
from src.utils.scaler import scale_data
from src.utils.sequences import create_sequences
from src.model.lstm_model import build_model


def train():
    print("🚀 Loading dataset...")

    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "dataset_features.csv")
    MODEL_DIR = os.path.join(BASE_DIR, "models")

    os.makedirs(MODEL_DIR, exist_ok=True)

    # --------------------------
    # LOAD DATA
    # --------------------------
    df = pd.read_csv(DATA_PATH)

    # ensure datetime sorted (VERY IMPORTANT)
    if "datetime" in df.columns:
        df["datetime"] = pd.to_datetime(df["datetime"])
        df = df.sort_values("datetime").reset_index(drop=True)

    print(f"📊 Raw data shape: {df.shape}")

    # --------------------------
    # REQUIRED COLUMNS CHECK
    # --------------------------
    required_cols = FEATURES + ["ghi", "clear_sky_ghi"]

    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"❌ Missing columns: {missing_cols}")

    # --------------------------
    # CLEANING
    # --------------------------
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.ffill().bfill()

    # --------------------------
    # INPUT / TARGET
    # --------------------------
    X = df[FEATURES].astype(np.float32)

    # residual learning (VERY IMPORTANT for your physics-based system)
    y = (df["ghi"] - df["clear_sky_ghi"]).astype(np.float32)

    # --------------------------
    # SCALING
    # --------------------------
    scaled_X, scaler = scale_data(X)

    # --------------------------
    # SEQUENCE CREATION
    # --------------------------
    X_seq, y_seq = create_sequences(
        scaled_X,
        y.values,
        SEQ_LENGTH,
        PRED_STEPS
    )

    if len(X_seq) == 0:
        raise ValueError("❌ No sequences generated")

    print(f"📊 Final Training Shape → X: {X_seq.shape}, Y: {y_seq.shape}")

    # --------------------------
    # BUILD MODEL
    # --------------------------
    model = build_model(
        (X_seq.shape[1], X_seq.shape[2]),
        PRED_STEPS
    )

    model.summary()

    # --------------------------
    # TRAIN MODEL 1
    # --------------------------
    print("🚀 Training model v1...")

    history1 = model.fit(
        X_seq,
        y_seq,
        epochs=20,
        batch_size=32,
        validation_split=0.1,
        verbose=1
    )

    model.save(os.path.join(MODEL_DIR, "lstm_v1.keras"))

    # --------------------------
    # TRAIN MODEL 2 (ENSEMBLE)
    # --------------------------
    print("🚀 Training model v2...")

    history2 = model.fit(
        X_seq,
        y_seq,
        epochs=10,
        batch_size=32,
        verbose=1
    )

    model.save(os.path.join(MODEL_DIR, "lstm_v2.keras"))

    # --------------------------
    # SAVE SCALER
    # --------------------------
    joblib.dump(scaler, os.path.join(MODEL_DIR, "scaler.pkl"))

    # --------------------------
    # SAVE FEATURES (CRITICAL)
    # --------------------------
    with open(os.path.join(MODEL_DIR, "features.json"), "w") as f:
        json.dump(FEATURES, f)

    print("✅ Training complete")

    # --------------------------
    # QUICK SANITY CHECK
    # --------------------------
    print("\n🔍 Sanity Check:")
    print("Sample prediction range:", np.min(y_seq), "→", np.max(y_seq))


if __name__ == "__main__":
    train()


