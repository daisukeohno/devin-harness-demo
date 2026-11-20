import pytest
from fastapi.testclient import TestClient

from sensor_analytics.api import app

client = TestClient(app)


def test_health():
    assert client.get("/health").json() == {"status": "ok"}


def test_devices_lists_sample_devices():
    response = client.get("/devices")
    assert response.status_code == 200
    assert response.json() == {"devices": ["dev-001", "dev-002"]}


@pytest.mark.parametrize(
    ("prefix", "expected"),
    [
        ("dev-001", ["dev-001"]),
        ("dev-00", ["dev-001", "dev-002"]),
        ("dev-999", []),
        ("DEV-001", []),
    ],
)
def test_devices_filters_by_prefix(prefix, expected):
    response = client.get("/devices", params={"prefix": prefix})
    assert response.status_code == 200
    assert response.json() == {"devices": expected}


def test_summary_returns_three_signals():
    payload = client.get("/summary", params={"device_id": "dev-001"}).json()
    assert [signal["column"] for signal in payload["signals"]] == [
        "temperature_c",
        "voltage_v",
        "current_a",
    ]
    assert all("n_dropped" in signal for signal in payload["signals"])


def test_summary_unknown_device_is_404():
    assert client.get("/summary", params={"device_id": "nope"}).status_code == 404


def test_anomalies_rejects_unknown_column():
    response = client.get("/anomalies", params={"device_id": "dev-001", "column": "pressure_pa"})
    assert response.status_code == 400
