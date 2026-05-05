import pandas as pd

def merge_data(nasa_df, weather_df):
    if nasa_df.empty or weather_df.empty:
        return pd.DataFrame()

    return pd.merge_asof(
        nasa_df.sort_values("datetime"),
        weather_df.sort_values("datetime"),
        on="datetime",
        direction="nearest"
    )




