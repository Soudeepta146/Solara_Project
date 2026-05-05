# # src/model/lstm_model.py

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, Input


def build_model(input_shape, output_steps):
    """
    Production-ready LSTM model (clean + no warnings)
    """

    model = Sequential([
        Input(shape=input_shape),

        LSTM(128, return_sequences=True),
        Dropout(0.2),

        LSTM(64, return_sequences=False),
        Dropout(0.2),

        Dense(32, activation="relu"),
        Dense(output_steps)
    ])

    model.compile(
        optimizer="adam",
        loss="mse"
    )

    return model






