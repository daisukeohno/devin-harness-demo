"""Reading and normalising raw sensor CSV files."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from sensor_analytics.config import DEFAULT_CONFIG, AnalysisConfig

REQUIRED_COLUMNS = ("timestamp", "device_id", "temperature_c", "voltage_v", "current_a")

DATA_DIR = Path(__file__).parent / "data"
SAMPLE_PATH = DATA_DIR / "sample_readings.csv"


class SchemaError(ValueError):
    """Raised when an input frame is missing required columns."""


def read_readings(path: Path | str = SAMPLE_PATH) -> pd.DataFrame:
    """Read a readings CSV and return a normalised frame."""
    frame = pd.read_csv(path)
    return normalise(frame)


def normalise(frame: pd.DataFrame, config: AnalysisConfig = DEFAULT_CONFIG) -> pd.DataFrame:
    """Validate columns, convert timestamps to UTC and bound gap filling.

    Missing values are forward-filled for at most
    ``config.max_ffill_steps`` samples per device. Longer gaps stay missing
    so downstream code can drop them explicitly.
    """
    missing = [column for column in REQUIRED_COLUMNS if column not in frame.columns]
    if missing:
        raise SchemaError(f"missing columns: {', '.join(missing)}")

    out = frame.copy()
    out["timestamp"] = pd.to_datetime(out["timestamp"], utc=True, errors="coerce")
    out = out.dropna(subset=["timestamp", "device_id"])
    out = out.sort_values(["device_id", "timestamp"]).reset_index(drop=True)

    value_columns = ["temperature_c", "voltage_v", "current_a"]
    for column in value_columns:
        out[column] = pd.to_numeric(out[column], errors="coerce")

    out[value_columns] = out.groupby("device_id")[value_columns].ffill(limit=config.max_ffill_steps)
    return out


def device_series(frame: pd.DataFrame, device_id: str) -> pd.DataFrame:
    """Return the rows for one device, timestamp ordered."""
    rows = frame.loc[frame["device_id"] == device_id]
    return rows.sort_values("timestamp").reset_index(drop=True)
