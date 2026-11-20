# devin-harness-demo

Devin の「ハーネス」— Knowledge / Skills / REVIEW.md / Playbook / Blueprint — を
お客様のデモでそのまま見せるためのサンプルリポジトリです。

題材は汎用的な**センサー時系列データの解析サービス**（FastAPI + pandas）にしてあります。
特定の業種に依存しないので、製造・モビリティ・エネルギー・SaaS どの相手にも同じ流れで説明できます。

## 何が入っているか

| 見せるもの | 場所 | Devin 側での扱い |
|---|---|---|
| Skills（再利用可能な手順） | `.agents/skills/*/SKILL.md` | リポジトリを接続すると自動的に発見される。`@skills:<name>` で明示指定も可能 |
| Review 観点 | `REVIEW.md`, `src/sensor_analytics/REVIEW.md` | Devin Review が PR 解析時に読み込む（`**/REVIEW.md`）。ディレクトリ単位でスコープできる |
| エージェント共通の前提 | `AGENTS.md` | Devin セッションと Devin Review の両方が参照する |
| Knowledge 候補 | `knowledge/*.md` | Web アプリの Knowledge に登録して使う。`scripts/import_knowledge.py` で一括登録できる |
| Playbook 候補 | `playbooks/*.md` | Web アプリの Playbooks に登録し、セッション開始時に添付する |
| 環境 Blueprint | `blueprint.yaml` | Devin の Environment 設定に貼り付ける（このファイル自体は参考値） |
| デモ台本 | `docs/demo-script-ja.md` | 15分でひと通り見せる手順 |
| Devin Oncall デモ | [日本語台本](docs/oncall-demo-ja.md) | 模擬監視アラートから Slack で原因調査と復旧確認 |

## ローカルでの動かし方

```bash
uv sync                      # 依存関係
uv run pytest                # テスト
uv run ruff check .          # lint
uv run uvicorn sensor_analytics.api:app --reload   # API 起動
```

サンプルデータは `src/sensor_analytics/data/sample_readings.csv`（合成データ。実データ・顧客データは含みません）。

```bash
curl "http://localhost:8000/health"
curl "http://localhost:8000/summary?device_id=dev-001"
curl "http://localhost:8000/anomalies?device_id=dev-001&window=12"
```

## デモの流れ（要約）

1. リポジトリを Devin に接続 → Skills が自動で認識されるところを見せる
2. Knowledge を登録 → 「この組織固有の前提」をモデルに与える場所だと説明する
3. Playbook を添付してセッションを開始 → 手順の再現性を見せる
4. わざと問題のある PR を作る（`scripts/make_demo_pr.sh`）→ `REVIEW.md` の観点に沿って Devin Review が指摘するのを見せる

詳細は `docs/demo-script-ja.md`。

## 注意

- 秘密情報・顧客データは一切含めていません。Knowledge のサンプルも架空の値です。
- Devin Review が自動で読み込むのは `**/REVIEW.md` などの既定パターンです。独自パスのファイルを読ませたい場合は Settings > Review の Review Rules に glob を追加します。
- Playbook と Knowledge は Web アプリ側の資産なので、リポジトリの Markdown はあくまで「登録用の元ネタ」です。
