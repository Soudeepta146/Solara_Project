import pandas as pd

def preprocess(df):
    df["datetime"] = pd.to_datetime(df["datetime"])
    df = df.sort_values("datetime")

    df = df.ffill().bfill()
    df = df[df["ghi"] >= 0]

    return df


