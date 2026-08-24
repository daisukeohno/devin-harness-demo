"""HTTP surface for the analysis helpers."""

from __future__ import annotations

from dataclasses import asdict

from fastapi import FastAPI, HTTPException

from sensor_analytics.analysis import InsufficientDataError, find_anomalies, summarise
from sensor_analytics.config import DEFAULT_CONFIG
from sensor_analytics.loading import device_series, read_readings

app = FastAPI(title="sensor-analytics", version="0.1.0")

SIGNALS = ("temperature_c", "voltage_v", "current_a")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/devices")
def devices() -> dict[str, list[str]]:
    frame = read_readings()
    return {"devices": sorted(frame["device_id"].unique().tolist())}


@app.get("/summary")
def summary(device_id: str) -> dict[str, object]:
    frame = device_series(read_readings(), device_id)
    if frame.empty:
        raise HTTPException(status_code=404, detail=f"unknown device: {device_id}")
    try:
        signals = [asdict(summarise(frame[column], column)) for column in SIGNALS]
    except InsufficientDataError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    return {"device_id": device_id, "signals": signals}


@app.get("/anomalies")
def anomalies(
    device_id: str,
    column: str = "temperature_c",
    window: int = DEFAULT_CONFIG.anomaly_window,
) -> dict[str, object]:
    if column not in SIGNALS:
        raise HTTPException(status_code=400, detail=f"unknown column: {column}")
    frame = device_series(read_readings(), device_id)
    if frame.empty:
        raise HTTPException(status_code=404, detail=f"unknown device: {device_id}")
    try:
        report = find_anomalies(frame, column, window=window)
    except InsufficientDataError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    payload = asdict(report)
    payload["timestamps"] = [timestamp.isoformat() for timestamp in report.timestamps]
    return {"device_id": device_id, **payload}
