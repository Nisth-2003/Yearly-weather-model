from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pandas as pd

from state_coordinates import STATE_COORDS
from open_meteo_weather import get_monthly_temp_humidity
from nasa_uv import get_monthly_uv
from excel_generator import create_or_update_excel

app = FastAPI(title="India Monthly Climate (Hybrid API)")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/download")
def download(year: int):
    if year < 1950 or year > 2100:
        raise HTTPException(status_code=400, detail="Invalid year")

    all_rows = []

    for state, (lat, lon) in STATE_COORDS.items():
        temp_df = get_monthly_temp_humidity(lat, lon, year)
        uv_df = get_monthly_uv(lat, lon, year)

        merged = pd.merge(temp_df, uv_df, on="Month", how="left")
        merged.insert(0, "State", state.title())
        merged.insert(1, "Year", year)

        all_rows.append(merged)

    final_df = pd.concat(all_rows, ignore_index=True)
    file_path = create_or_update_excel(year, final_df)

    return FileResponse(
        path=file_path,
        filename=file_path,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
