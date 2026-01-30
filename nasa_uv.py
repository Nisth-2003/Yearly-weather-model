import requests
import pandas as pd
import numpy as np

def get_monthly_uv(lat, lon, year):
    url = (
        "https://power.larc.nasa.gov/api/temporal/daily/point"
        f"?latitude={lat}&longitude={lon}"
        f"&start={year}0101&end={year}1231"
        "&parameters=ALLSKY_SFC_UVB"
        "&community=RE&format=JSON"
    )

    r = requests.get(url, timeout=60)
    r.raise_for_status()

    data = r.json()["properties"]["parameter"]["ALLSKY_SFC_UVB"]

    df = pd.DataFrame({
        "date": list(data.keys()),
        "uvb": list(data.values())
    })

    df["date"] = pd.to_datetime(df["date"])

    # 🚨 VERY IMPORTANT FIX
    # Replace NASA missing value (-999) with NaN
    df["uvb"] = df["uvb"].replace(-999, np.nan)

    # Convert UVB → UV Index
    df["uv_index"] = df["uvb"] * 40

    df["Month"] = df["date"].dt.month_name()

    monthly = (
        df.groupby("Month")
        .agg(
            **{
                "Avg UV Index": ("uv_index", "mean"),
                "UV Min": ("uv_index", "min"),
                "UV Max": ("uv_index", "max"),
            }
        )
        .reset_index()
    )

    # Month order
    month_order = [
        "January","February","March","April","May","June",
        "July","August","September","October","November","December"
    ]
    monthly["Month"] = pd.Categorical(
        monthly["Month"], categories=month_order, ordered=True
    )
    monthly = monthly.sort_values("Month")

    return monthly.round(2)
