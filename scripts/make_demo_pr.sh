#!/usr/bin/env bash
# Devin Review のデモ用に、REVIEW.md の観点に引っかかる変更をブランチで作る。
#
# 使い方:
#   ./scripts/make_demo_pr.sh          # ブランチを作ってコミットまで
#   ./scripts/make_demo_pr.sh --push   # push まで（PR は GitHub 上で作る）
#
# 仕込んでいる問題:
#   1. 欠損値の 0 埋め（データ制約違反）
#   2. しきい値のハードコード（config.py を経由していない）
#   3. n_samples / n_dropped を返さない新関数
#   4. naive datetime と UTC datetime の比較
set -euo pipefail

cd "$(git rev-parse --show-toplevel)"
BRANCH="demo/review-findings-$(date +%s)"
git checkout -b "$BRANCH"

cat >> src/sensor_analytics/analysis.py <<'PY'


def quick_health_score(frame: pd.DataFrame) -> float:
    """Rough health score for a device.

    NOTE: intentionally flawed. Used to demo Devin Review.
    """
    import datetime

    values = frame["temperature_c"].fillna(0)
    recent = frame[frame["timestamp"] > datetime.datetime(2026, 3, 1)]
    penalty = (values > 55.0).sum() * 0.05
    return max(0.0, 1.0 - penalty - 0.01 * len(recent))
PY

git add src/sensor_analytics/analysis.py
git commit -m "feat: add quick health score for devices"

if [[ "${1:-}" == "--push" ]]; then
  git push -u origin "$BRANCH"
  echo "pushed $BRANCH. GitHub 上で PR を作ると Devin Review が動きます。"
else
  echo "created $BRANCH (未 push)。--push を付けると push します。"
fi
