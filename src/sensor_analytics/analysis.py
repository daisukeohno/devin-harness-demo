"""Pure analysis helpers. No file or network I/O lives in this module."""

from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd

from sensor_analytics.config import DEFAULT_CONFIG, AnalysisConfig


class InsufficientDataError(ValueError):
    """Raised when a series is too short to analyse."""


@dataclass(frozen=True)
class Summary:
    """Summary statistics for one signal, with sample accounting."""

    column: str
    mean: float
    std: float
    minimum: float
    maximum: float
    n_samples: int
    n_dropped: int


@dataclass(frozen=True)
class AnomalyReport:
    """Anomalous samples found by the rolling z-score rule."""

    column: str
    window: int
    sigma: float
    n_samples: int
    n_dropped: int
    timestamps: list[pd.Timestamp] = field(default_factory=list)


def summarise(
    series: pd.Series,
    column: str,
    config: AnalysisConfig = DEFAULT_CONFIG,
) -> Summary:
    """Summary statistics for ``series``, reporting how many samples were used."""
    n_total = len(series)
    clean = series.dropna()
    if len(clean) < config.min_samples:
        raise InsufficientDataError(
            f"{column}: {len(clean)} usable samples, need at least {config.min_samples}"
        )
    return Summary(
        column=column,
        mean=float(clean.mean()),
        std=float(clean.std(ddof=1)),
        minimum=float(clean.min()),
        maximum=float(clean.max()),
        n_samples=len(clean),
        n_dropped=n_total - len(clean),
    )


def rolling_baseline(series: pd.Series, window: int) -> tuple[pd.Series, pd.Series]:
    """Rolling mean and standard deviation over ``window`` samples."""
    if window < 2:
        raise ValueError("window must be at least 2")
    rolling = series.rolling(window=window, min_periods=window)
    return rolling.mean(), rolling.std(ddof=1)


def find_anomalies(
    frame: pd.DataFrame,
    column: str,
    config: AnalysisConfig = DEFAULT_CONFIG,
    window: int | None = None,
) -> AnomalyReport:
    """Flag samples that deviate from their rolling baseline.

    The frame needs ``timestamp`` and ``column``. Samples without a full
    rolling window are not evaluated and are counted in ``n_dropped``.
    """
    window = window or config.anomaly_window
    series = frame[column]
    n_total = len(series)
    if n_total < max(window, config.min_samples):
        raise InsufficientDataError(
            f"{column}: {n_total} samples, need at least {max(window, config.min_samples)}"
        )

    mean, std = rolling_baseline(series, window)
    deviation = (series - mean).abs()
    flagged = (std > 0) & (deviation > config.anomaly_sigma * std)
    evaluated = mean.notna() & std.notna() & series.notna()

    return AnomalyReport(
        column=column,
        window=window,
        sigma=config.anomaly_sigma,
        n_samples=int(evaluated.sum()),
        n_dropped=int(n_total - evaluated.sum()),
        timestamps=list(frame.loc[flagged & evaluated, "timestamp"]),
    )
