---
name: local-testing
description: Set up the environment, run the test suite and lint, and smoke-test the API before opening a PR. Use for any change under src/ or tests/.
---

# ローカル検証

PR を出す前に必ずこの手順を通す。途中で失敗したら、飛ばさずに原因を直す。

## 1. 依存関係

```bash
cd "$(git rev-parse --show-toplevel)"
uv sync --extra dev
```

## 2. 静的チェックとテスト

```bash
uv run ruff check .
uv run ruff format --check .
uv run pytest -q
```

`ruff format --check` が落ちた場合は `uv run ruff format .` を実行し、差分を確認してからコミットする。

## 3. API のスモークテスト

サーバーを別プロセスで起動して、3 つのエンドポイントを叩く。

```bash
uv run uvicorn sensor_analytics.api:app --port 8000 &
sleep 3
curl -sf "http://localhost:8000/health"
curl -sf "http://localhost:8000/summary?device_id=dev-001" | head -c 400
curl -sf "http://localhost:8000/anomalies?device_id=dev-001&window=12" | head -c 400
kill %1
```

`/summary` のレスポンスに `n_samples` と `n_dropped` が入っていることを目視で確認する。
入っていなければ実装が `AGENTS.md` の決めごとに違反している。

## 4. PR に書くこと

- 実行したコマンドと結果（テスト件数、lint の結果）
- 数値の振る舞いを変えた場合は、変更前後の値の比較
