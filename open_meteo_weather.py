import requests
import pandas as pd

def get_monthly_temp_humidity(lat, lon, year):
    url = (
        "https://archive-api.open-meteo.com/v1/archive"
        f"?latitude={lat}&longitude={lon}"
        f"&start_date={year}-01-01&end_date={year}-12-31"
        "&daily=temperature_2m_mean,relative_humidity_2m_mean"
        "&timezone=UTC"
    )

    r = requests.get(url, timeout=60)
    r.raise_for_status()
    data = r.json()

    df = pd.DataFrame({
        "date": data["daily"]["time"],
        "temperature": data["daily"]["temperature_2m_mean"],
        "humidity": data["daily"]["relative_humidity_2m_mean"],
    })

    df["date"] = pd.to_datetime(df["date"])
    df["Month"] = df["date"].dt.month_name()

    monthly = df.groupby("Month").mean(numeric_only=True).reset_index()

    month_order = [
        "January","February","March","April","May","June",
        "July","August","September","October","November","December"
    ]
    monthly["Month"] = pd.Categorical(monthly["Month"], categories=month_order, ordered=True)
    monthly = monthly.sort_values("Month")

    monthly.rename(columns={
        "temperature": "Avg Temperature (°C)",
        "humidity": "Avg Humidity (%)"
    }, inplace=True)

    return monthly
