import pytest

from sensor_analytics import oncall_demo


def test_drift_prints_alert_with_observed_statuses(monkeypatch, capsys):
    responses = {"/ready": 404, "/health": 200}
    monkeypatch.setattr(oncall_demo, "status_for", lambda port, path: responses[path])

    assert oncall_demo.main(["--profile", "drift"]) == 0
    output = capsys.readouterr().out
    assert output.startswith("[ONCALL-DEMO-SENSOR]")
    assert "GET /ready → HTTP 404" in output
    assert "GET /health → HTTP 200" in output


def test_recovery_does_not_emit_alert_marker(monkeypatch, capsys):
    responses = {"/health": 200}
    monkeypatch.setattr(oncall_demo, "status_for", lambda port, path: responses[path])

    assert oncall_demo.main(["--profile", "healthy"]) == 0
    output = capsys.readouterr().out
    assert "RECOVERED" in output
    assert "GET /health → HTTP 200" in output
    assert "[ONCALL-DEMO-SENSOR]" not in output


@pytest.mark.parametrize(("ready", "health"), [(200, 200), (404, 503)])
def test_unexpected_http_status_does_not_emit_alert(monkeypatch, capsys, ready, health):
    responses = {"/ready": ready, "/health": health}
    monkeypatch.setattr(oncall_demo, "status_for", lambda port, path: responses[path])

    assert oncall_demo.main([]) == 1
    output = capsys.readouterr()
    assert not output.out
    assert "想定外の応答" in output.err


def test_unreachable_api_does_not_emit_alert(monkeypatch, capsys):
    def unavailable(port, path):
        raise ConnectionRefusedError()

    monkeypatch.setattr(oncall_demo, "status_for", unavailable)

    assert oncall_demo.main([]) == 1
    output = capsys.readouterr()
    assert not output.out
    assert "ローカル API に接続できません" in output.err
