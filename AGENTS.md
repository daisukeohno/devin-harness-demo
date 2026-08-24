# AGENTS.md

このリポジトリで作業するエージェント（Devin セッション、Devin Review）向けの共通前提です。

## プロジェクト概要

センサーの時系列データを取り込み、要約統計と異常区間を返す小さな解析サービス。

- `src/sensor_analytics/loading.py` — CSV の読み込みと正規化
- `src/sensor_analytics/analysis.py` — 要約統計、移動平均、異常検知
- `src/sensor_analytics/api.py` — FastAPI エンドポイント
- `tests/` — pytest

## コマンド

```bash
uv sync
uv run pytest
uv run ruff check .
uv run ruff format --check .
```

PR を出す前に上の 3 つ（test / check / format）を必ず通すこと。

## 決めごと

- タイムスタンプは UTC で保持する。ローカル時刻へ変換するのは表示層だけ。
- 単位は SI 系（温度は °C、電流は A、電圧は V）。列名に単位を含める場合は `_c` / `_a` / `_v` の接尾辞を使う。
- 欠損値を勝手に 0 で埋めない。前方補完の上限は `MAX_FFILL_STEPS`（`config.py`）まで。
- しきい値やウィンドウ幅などのパラメータはコードに直接書かず `config.py` に置く。
- 解析結果を返す関数は、必ず「使ったサンプル数」と「除外したサンプル数」を一緒に返す。

## やらないこと

- サンプルデータの差し替え（`data/sample_readings.csv` は合成データ。実データを入れない）。
- 依存関係の追加は必要最小限。追加する場合は理由を PR に書く。
