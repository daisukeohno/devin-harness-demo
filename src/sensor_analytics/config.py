"""Tunable parameters for the analysis pipeline.

Keep every threshold, window width and limit here so reviewers can see
behaviour changes in one place.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class AnalysisConfig:
    """Parameters used by :mod:`sensor_analytics.analysis`."""

    max_ffill_steps: int = 3
    """Upper bound for forward-filling gaps. Longer gaps stay missing."""

    anomaly_window: int = 12
    """Number of samples in the rolling window used for anomaly detection."""

    anomaly_sigma: float = 3.0
    """Deviation from the rolling mean, in rolling standard deviations."""

    min_samples: int = 24
    """Series shorter than this are rejected instead of analysed."""


DEFAULT_CONFIG = AnalysisConfig()

MAX_FFILL_STEPS = DEFAULT_CONFIG.max_ffill_steps
