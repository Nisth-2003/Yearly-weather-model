import requests
import pandas as pd

def get_monthly_weather(lat, lon, year):
    url = (
        "https://archive-api.open-meteo.com/v1/archive"
        f"?latitude={lat}&longitude={lon}"
        f"&start_date={year}-01-01&end_date={year}-12-31"
        "&daily=temperature_2m_mean,relative_humidity_2m_mean,uv_index_max"
        "&timezone=UTC"
    )

    r = requests.get(url, timeout=60)
    r.raise_for_status()
    data = r.json()

    df = pd.DataFrame({
        "date": data["daily"]["time"],
        "temperature": data["daily"]["temperature_2m_mean"],
        "humidity": data["daily"]["relative_humidity_2m_mean"],
        "uv_index": data["daily"]["uv_index_max"],
    })

    # Convert date
    df["date"] = pd.to_datetime(df["date"])
    df["Month"] = df["date"].dt.month_name()

    # Ensure numeric (VERY IMPORTANT)
    df["temperature"] = pd.to_numeric(df["temperature"], errors="coerce")
    df["humidity"] = pd.to_numeric(df["humidity"], errors="coerce")
    df["uv_index"] = pd.to_numeric(df["uv_index"], errors="coerce")

    # Monthly aggregation (NaN-safe)
    monthly = (
        df.groupby("Month")
        .agg({
            "temperature": "mean",
            "humidity": "mean",
            "uv_index": "mean"
        })
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

    # Rename & round
    monthly.rename(columns={
        "temperature": "Average Temperature (°C)",
        "humidity": "Average Humidity (%)",
        "uv_index": "Average UV Index"
    }, inplace=True)

    monthly["Average UV Index"] = monthly["Average UV Index"].round(2)
    monthly["Average Temperature (°C)"] = monthly["Average Temperature (°C)"].round(2)
    monthly["Average Humidity (%)"] = monthly["Average Humidity (%)"].round(2)

    return monthly
