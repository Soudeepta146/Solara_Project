def fetch_nasa_data(lat, lon):
    import pandas as pd
    import numpy as np
    from datetime import datetime, timedelta

    now = datetime.now()

    # generate 100 past hourly timestamps
    times = [now - timedelta(hours=i) for i in range(100)][::-1]

    df = pd.DataFrame({
        "datetime": times,
        "ghi": np.random.uniform(0, 800, size=100),
        "cloud_cover": np.random.uniform(0, 100, size=100),
        "clear_sky_ghi": np.random.uniform(200, 1000, size=100)
    })

    print("✅ Dummy solar data generated")

    return df