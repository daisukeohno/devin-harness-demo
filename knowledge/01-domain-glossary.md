---
name: "Sensor analytics: 用語と指標の定義"
scope: "sensor-analytics リポジトリで解析ロジック、指標、レポートを扱うとき"
---

社内で使っている用語の定義です。会話や PR の説明で表記を揃えてください。

- **reading**: 1 デバイス・1 タイムスタンプの 1 行。5 分周期が標準。
- **dropout**: センサー側の欠測。連続 3 サンプルまでは前方補完し、それより長い区間は欠損のまま残す。
- **anomaly**: 移動平均から移動標準偏差の 3 倍を超えて離れたサンプル。閾値は `config.py` の `anomaly_sigma`。
- **usable samples (`n_samples`)**: 実際に統計計算に使われたサンプル数。
- **dropped samples (`n_dropped`)**: 欠損またはウィンドウ不足で評価対象外になった数。

指標を報告するときは、必ず `n_samples` と `n_dropped` を併記します。
母数を書かない数値はレビューで差し戻します。

用語の対応（社内 / 顧客向け資料）:

| 社内 | 顧客向け |
|---|---|
| dropout | 欠測区間 |
| anomaly | 異常サンプル |
| usable samples | 有効サンプル数 |
