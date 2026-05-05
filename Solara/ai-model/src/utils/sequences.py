# src/utils/sequences.py

import numpy as np

# ---------------------------
# 🧠 TRAINING SEQUENCES
# ---------------------------

def create_sequences(
    X,
    y,
    seq_length,
    pred_steps,
    stride=1
):
    """
    Create sequences for training LSTM

    Args:
        X: feature array
        y: target array
        seq_length: input window
        pred_steps: future prediction length
        stride: step size (default=1)

    Returns:
        X_seq, y_seq
    """

    X = np.array(X, dtype=np.float32)
    y = np.array(y, dtype=np.float32)

    n_samples = len(X)

    if n_samples < seq_length + pred_steps:
        raise ValueError("❌ Not enough data to create sequences")

    X_seq = []
    y_seq = []

    for i in range(0, n_samples - seq_length - pred_steps + 1, stride):
        X_seq.append(X[i: i + seq_length])
        y_seq.append(y[i + seq_length: i + seq_length + pred_steps])

    return (
        np.array(X_seq, dtype=np.float32),
        np.array(y_seq, dtype=np.float32)
    )


# ---------------------------
# ⚡ INFERENCE SEQUENCE
# ---------------------------

def create_inference_sequence(
    X,
    seq_length
):
    """
    Create single sequence for prediction

    Args:
        X: latest feature dataframe/array
        seq_length: input window

    Returns:
        reshaped sequence (1, seq_length, features)
    """

    X = np.array(X, dtype=np.float32)

    if len(X) < seq_length:
        raise ValueError("❌ Not enough data for inference")

    seq = X[-seq_length:]

    return seq.reshape(1, seq_length, X.shape[1])


# ---------------------------
# 🕒 TIMESTAMP ALIGNMENT
# ---------------------------

def generate_time_labels(
    start_time,
    steps,
    interval_minutes=15
):
    """
    Generate future timestamps for prediction

    Args:
        start_time: last known datetime
        steps: number of prediction steps
        interval_minutes: interval between predictions

    Returns:
        list of timestamps
    """

    from datetime import timedelta

    return [
        start_time + timedelta(minutes=interval_minutes * (i + 1))
        for i in range(steps)
    ]


# ---------------------------
# 🧪 DEBUG TOOL
# ---------------------------

def inspect_sequences(X_seq, y_seq):
    """
    Debug helper to inspect shapes
    """

    print("📊 X_seq shape:", X_seq.shape)
    print("📊 y_seq shape:", y_seq.shape)

    print("🔍 Sample X:", X_seq[0][:3])
    print("🔍 Sample y:", y_seq[0][:3])

