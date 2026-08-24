import numpy as np
import pandas as pd
import pytest

from sensor_analytics.analysis import (
    InsufficientDataError,
    find_anomalies,
    rolling_baseline,
    summarise,
)
from sensor_analytics.loading import device_series, read_readings


def _frame(values):
    return pd.DataFrame(
        {
            "timestamp": pd.date_range("2026-03-01", periods=len(values), freq="5min", tz="UTC"),
            "temperature_c": values,
        }
    )


def test_summarise_reports_sample_accounting():
    values = [40.0] * 30 + [np.nan] * 2
    result = summarise(pd.Series(values), "temperature_c")
    assert result.n_samples == 30
    assert result.n_dropped == 2


def test_summarise_rejects_short_series():
    with pytest.raises(InsufficientDataError):
        summarise(pd.Series([40.0, 41.0]), "temperature_c")


def test_summarise_rejects_all_missing_series():
    with pytest.raises(InsufficientDataError):
        summarise(pd.Series([np.nan] * 40), "temperature_c")


def test_rolling_baseline_requires_window_of_two():
    with pytest.raises(ValueError):
        rolling_baseline(pd.Series([1.0, 2.0]), window=1)


def test_find_anomalies_flags_injected_spike():
    values = [40.0 + 0.05 * (index % 3) for index in range(60)]
    values[45] = 80.0
    report = find_anomalies(_frame(values), "temperature_c", window=12)
    assert len(report.timestamps) >= 1
    assert report.n_samples + report.n_dropped == 60


def test_find_anomalies_rejects_short_series():
    with pytest.raises(InsufficientDataError):
        find_anomalies(_frame([40.0] * 10), "temperature_c", window=12)


def test_sample_data_has_anomalies_on_dev_001():
    frame = device_series(read_readings(), "dev-001")
    report = find_anomalies(frame, "temperature_c")
    assert report.timestamps, "sample data is expected to contain injected spikes"
