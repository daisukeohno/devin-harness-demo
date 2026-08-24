---
name: release-checklist
description: Cut a release of the analytics service - version bump, changelog, tag and post-release verification. Invoke explicitly when asked to prepare a release.
argument-hint: <version, e.g. 0.2.0>
triggers: ["user"]
---

# リリース手順

`@skills:release-checklist 0.2.0` のように、バージョンを指定して呼ぶ。

1. `main` が最新か確認する（`git fetch && git status`）。未マージの PR がある場合は人に確認する。
2. `pyproject.toml` の `version` と `src/sensor_analytics/api.py` の `FastAPI(version=...)` を指定バージョンに揃える。
3. `docs/CHANGELOG.md` に前回タグからのコミットを分類して追記する（Added / Changed / Fixed）。解析結果の数値が変わる変更は Changed の先頭に書く。
4. `@skills:local-testing` を実行して全項目を通す。
5. `release/<version>` ブランチで PR を作る。PR 本文にテスト結果と、数値の変化があればその比較を貼る。
6. マージ後にタグを打つのは人の作業。エージェントはタグを作らない。

## 中止する条件

- テストが 1 件でも落ちている
- `n_samples` / `n_dropped` を返さなくなった関数がある
- サンプルデータが差し替えられている
