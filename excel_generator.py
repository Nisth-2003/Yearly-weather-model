'''import pandas as pd

def create_excel(state, year, averages):
    df = pd.DataFrame([{
        "State": state.title(),
        "Year": year,
        "Average Temperature (°C)": averages["avg_temperature"],
        "Average Humidity (%)": averages["avg_humidity"]
    }])

    filename = f"{state}_{year}_yearly_weather.xlsx"
    df.to_excel(filename, index=False)
    return filename

import pandas as pd
import os

def create_or_update_excel(state, year, averages):
    filename = f"{state}_{year}_yearly_weather.xlsx"

    df = pd.DataFrame([{
        "State": state.title(),
        "Year": year,
        "Average Temperature (°C)": averages["avg_temperature"],
        "Average Humidity (%)": averages["avg_humidity"]
    }])

    # This will CREATE if not exists
    # or OVERWRITE if already exists
    df.to_excel(filename, index=False)

    return filename
'''
import pandas as pd

def create_or_update_excel(year, df):
    filename = f"india_all_states_{year}_monthly_climate.xlsx"
    df.to_excel(filename, index=False)
    return filename

