"""Print a Slack-ready synthetic alert using real loopback HTTP observations."""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from http.client import HTTPConnection, HTTPException

from sensor_analytics.config import DEMO_PROBE_TIMEOUT_SECONDS

ALERT_MARKER = "[ONCALL-DEMO-SENSOR]"
MONITOR_PATHS = {"drift": "/ready", "healthy": "/health"}


def status_for(port: int, path: str) -> int:
    connection = HTTPConnection("127.0.0.1", port, timeout=DEMO_PROBE_TIMEOUT_SECONDS)
    try:
        connection.request("GET", path)
        with connection.getresponse() as response:
            return response.status
    finally:
        connection.close()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", choices=MONITOR_PATHS, default="drift")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args(argv)
    if not 1 <= args.port <= 65535:
        parser.error("--port must be between 1 and 65535")

    path = MONITOR_PATHS[args.profile]
    try:
        status = status_for(args.port, path)
        control_status = status if args.profile == "healthy" else status_for(args.port, "/health")
    except (OSError, HTTPException) as error:
        print(f"ローカル API に接続できません: {error}", file=sys.stderr)
        return 1

    expected_status = 404 if args.profile == "drift" else 200
    if (status, control_status) != (expected_status, 200):
        print(f"想定外の応答: {path} → {status}, /health → {control_status}", file=sys.stderr)
        return 1

    if args.profile == "healthy":
        print(f"RECOVERED（デモ）: GET {path} → HTTP {status}（期待値: 200）")
    else:
        observed_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
        print(
            f"{ALERT_MARKER} 模擬アラート：センサー API 可用性チェック失敗\n"
            "対象: sensor-analytics（ローカルデモ。本番影響なし）\n"
            f"観測時刻: {observed_at}\n"
            f"監視プローブ: GET {path} → HTTP {status}（期待値: 200）\n"
            f"対照プローブ: GET /health → HTTP {control_status}\n"
            "対象リポジトリ: https://github.com/daisukeohno/devin-harness-demo"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
