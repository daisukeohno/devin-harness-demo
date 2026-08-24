---
name: impact-analysis
description: Read-only impact analysis for a requirement or spec change - find every affected module, test, endpoint and document, then propose a change plan without editing code. Use before implementing anything non-trivial.
allowed-tools: Read, Grep, ListDir
triggers: ["user"]
---

# 影響範囲分析（読み取り専用）

要求や仕様が変わったときに、まず「どこに効くか」を洗い出すための手順。
この Skill が動いている間はコードを変更しない。

## 手順

1. **要求の言い換え**: 変更要求を、観測可能な振る舞いの差として 3 行以内で書き直す。曖昧な点は質問として残す。
2. **入口の特定**: `src/sensor_analytics/api.py` のうち影響するエンドポイントを列挙する。
3. **依存の追跡**: 対象の関数から呼ばれている関数、呼んでいる関数を `analysis.py` / `loading.py` / `config.py` の範囲で辿る。
4. **設定値**: `config.py` のどのパラメータが関係するか。既定値を変えると既存の結果がどう変わるか。
5. **テスト**: 影響する既存テストと、足りていないテストケースを挙げる。
6. **ドキュメント**: `AGENTS.md` の決めごと、`REVIEW.md` の観点、`docs/` の記述で更新が必要なものを挙げる。

## 出力フォーマット

```
## 変更要求の解釈
## 影響範囲（ファイル: 関数: 理由）
## 互換性への影響（API レスポンス、既定値）
## 変更方針（案 A / 案 B と、それぞれのリスク）
## 検証計画（追加するテスト、確認する数値）
## 人に確認したいこと
```

最後まで書き終えたら、実装に進む前に人の承認を待つ。
