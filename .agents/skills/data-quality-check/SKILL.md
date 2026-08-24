---
name: data-quality-check
description: Profile a sensor CSV before analysing it - schema, sampling interval, gaps, duplicates, units and outliers. Use whenever new or unfamiliar data is added or an analysis result looks suspicious.
argument-hint: <path-to-csv>
---

# データ品質チェック

解析に入る前に、入力データの素性を必ず確認する。ここを飛ばすと後段の結論がすべて疑わしくなる。

## 手順

1. **スキーマ**: `timestamp, device_id, temperature_c, voltage_v, current_a` が揃っているか。列名の単位接尾辞（`_c` / `_v` / `_a`）が実際の単位と一致しているか。
2. **サンプリング周期**: デバイスごとに `timestamp.diff()` の分布を出す。想定周期（5 分）から外れる区間を列挙する。
3. **欠損**: デバイスごと・列ごとの欠損率と、連続欠損の最大長。連続長が `config.MAX_FFILL_STEPS` を超える区間は補完せず落とす対象として報告する。
4. **重複**: `(device_id, timestamp)` の重複を数える。重複があれば、どちらを残すかを人に確認する。
5. **タイムゾーン**: naive な timestamp が混ざっていないか。UTC 以外のオフセットが来ていないか。
6. **外れ値**: 各列の p1 / p50 / p99 と物理的にあり得ない値（負の絶対温度、電圧 0 など）の件数。

## 出力

以下の形式で結果をセッション内に提示する。数値を自分で丸めず、そのまま載せる。

```
device_id | n_rows | 周期(中央値) | 欠損率(温度/電圧/電流) | 最大連続欠損 | 重複 | 外れ値
```

## 判断の分かれ目

- 欠損率が 5% を超える、または最大連続欠損が 6 サンプルを超える場合は、解析に進む前に人へ報告する。
- 重複や周期の乱れを勝手に補正しない。補正案を提示して承認を待つ。
