---
title: "最小例: minimal-example（Context Pack v1/v2）"
description: "Context Pack v1 と v2 の最小の有効例（minimal lint + schema validation）"
permalink: /examples/minimal-example/
---

# 最小例: minimal-example（Context Pack v1/v2）

本ページは、本文・仕様ページから「最小例の Context Pack」に確実に到達するためのハブです。v1 は従来の入力契約、v2 は v1 を壊さず Agent Runtime・データ契約・効果境界・検証証跡を追加する拡張です。

注記: 公開ページ本文と同じ版を確認したい場合は、このページ内に埋め込まれた YAML を優先してください。GitHub の repository view では埋め込み表示が展開されないため、その場合は同階層の [`context-pack-v1.yaml`](./context-pack-v1.yaml) / [`context-pack-v2.yaml`](./context-pack-v2.yaml) を参照します。版差が疑われる場合は、CHANGELOG とコミット履歴を確認します。

## 導線

- Context Pack v1 仕様: [Context Pack v1 仕様]({{ '/spec/context-pack-v1/' | relative_url }})
- Context Pack v2 仕様: [Context Pack v2 仕様]({{ '/spec/context-pack-v2/' | relative_url }})
- 最小例 Context Pack（YAML）:
  - v1 をサイト内で読む（公開版スナップショット）: [v1 YAML（全文）](#yaml-v1-full)
  - v2 をサイト内で読む（公開版スナップショット）: [v2 YAML（全文）](#yaml-v2-full)

## v1 と v2 の使い分け

- v1: Objects / Morphisms / Diagrams / Acceptance tests / Forbidden changes を固定できれば十分な小さな実装委任に使う。
- v2: allowed / forbidden tools、guardrails、trace evidence、data contracts、resource constraints までレビュー対象にしたい場合に使う。
- v2 は v1 の置換ではない。既存 v1 YAML は壊さず、必要な案件だけ v2 フィールドを追加する。

## 検証（ローカル）

注記: 以下のコマンドは local checkout 上の `docs/examples/minimal-example/*.yaml` を検証します。公開ページの YAML と同じ版を再現したい場合は、対象の commit / tag に合わせてから実行してください。

依存導入（初回のみ）:

```bash
python3 -m pip install -r scripts/requirements-qa.txt
```

minimal lint:

```bash
python3 scripts/validate-context-pack.py docs/examples/minimal-example/context-pack-v1.yaml
python3 scripts/validate-context-pack.py docs/examples/minimal-example/context-pack-v2.yaml
```

schema validation（JSON Schema）:

```bash
python3 scripts/validate-context-pack-schema.py docs/examples/minimal-example/context-pack-v1.yaml
python3 scripts/validate-context-pack-schema.py docs/examples/minimal-example/context-pack-v2.yaml
```

位置づけ/差分は [Context Pack v1 仕様（検証コマンド）]({{ '/spec/context-pack-v1/' | relative_url }}#validation-commands) と [Context Pack v2 仕様（検証コマンド）]({{ '/spec/context-pack-v2/' | relative_url }}#validation-commands) を参照してください。

（任意）CI相当の一括チェック: `npm run qa`（実行後に生成された検証レポートを確認する）

## YAML v1（全文） {#yaml-v1-full}

```yaml
{% include_relative context-pack-v1.yaml %}
```

## YAML v2（全文） {#yaml-v2-full}

```yaml
{% include_relative context-pack-v2.yaml %}
```
