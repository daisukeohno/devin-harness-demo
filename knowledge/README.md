# Knowledge 登録用ノート

このディレクトリの Markdown は、Devin の Knowledge に登録するための元ネタです。
リポジトリに置いただけでは Knowledge になりません（Knowledge は Web アプリ側の資産です）。

各ファイルの frontmatter は登録時に使う情報です。

```yaml
---
name: ノートのタイトル
scope: いつこのノートを参照してほしいか（トリガー条件）
---
```

## 登録方法（2 通り）

### 手動

1. Devin の Web アプリで Knowledge を開く
2. 新規ノートを作成し、`name` をタイトル、`scope` を「When to use」に入れる
3. frontmatter を除いた本文を貼り付ける

### 一括

セッション内の Devin に頼むのが速い。

```
knowledge/ 以下の Markdown を読んで、frontmatter の name と scope を使って
それぞれ Knowledge ノートとして登録してください。既に同名のノートがあれば更新してください。
```

Devin は Knowledge 管理用のツールを持っているので、この指示だけで登録できます（作成・更新には承認が入ります）。

## Skills との使い分け

- Knowledge: 前提、定義、制約、過去の経緯。「知っておいてほしいこと」
- Skills: 手順。「こうやってほしいこと」

同じ内容を両方に書くと更新漏れの原因になるので、片方に寄せます。
