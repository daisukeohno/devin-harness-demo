import pandas as pd
import pytest

from sensor_analytics.config import AnalysisConfig
from sensor_analytics.loading import SchemaError, device_series, normalise, read_readings


def test_read_sample_data_is_utc_and_sorted():
    frame = read_readings()
    assert str(frame["timestamp"].dt.tz) == "UTC"
    for device_id in frame["device_id"].unique():
        series = device_series(frame, device_id)
        assert series["timestamp"].is_monotonic_increasing


def test_missing_columns_are_rejected():
    with pytest.raises(SchemaError):
        normalise(pd.DataFrame({"timestamp": ["2026-03-01T00:00:00Z"]}))


def test_long_gaps_stay_missing():
    frame = pd.DataFrame(
        {
            "timestamp": pd.date_range("2026-03-01", periods=6, freq="5min", tz="UTC"),
            "device_id": ["dev-001"] * 6,
            "temperature_c": [40.0, None, None, None, None, 41.0],
            "voltage_v": [48.0] * 6,
            "current_a": [12.0] * 6,
        }
    )
    out = normalise(frame, AnalysisConfig(max_ffill_steps=2))
    assert out["temperature_c"].isna().sum() == 2
