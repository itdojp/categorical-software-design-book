---
title: "共通例題: 注文処理（Context Pack v1）"
description: "全章で参照する共通例題（Order/Payment/Inventory/Shipment/Audit）"
permalink: /examples/common-example/
---

# 共通例題: 注文処理（Context Pack v1）

本ページは、本文・仕様ページから「共通例題の Context Pack」に確実に到達するためのハブです。

注記: 公開ページ本文と同じ版を確認したい場合は、このページ内に埋め込まれた YAML を優先してください。GitHub の repository view では埋め込み表示が展開されないため、その場合は同階層の [`context-pack-v1.yaml`]({{ '/docs/examples/common-example/context-pack-v1.yaml' | relative_url }}) を参照します。版差が疑われる場合は、CHANGELOG とコミット履歴を確認します。

## 導線

- Context Pack v1 仕様: [Context Pack v1 仕様]({{ '/spec/context-pack-v1/' | relative_url }})
- 例題 Context Pack（YAML）:
  - サイト内で読む（公開版スナップショット）: [YAML（全文）](#yaml-full)

## 検証（ローカル）

注記: 以下のコマンドは local checkout 上の `docs/examples/common-example/context-pack-v1.yaml` を検証します。公開ページの YAML と同じ版を再現したい場合は、対象の commit / tag に合わせてから実行してください。

依存導入（初回のみ）:

```bash
python3 -m pip install -r scripts/requirements-qa.txt
```

minimal lint:

```bash
python3 scripts/validate-context-pack.py docs/examples/common-example/context-pack-v1.yaml
```

schema validation（JSON Schema）:

```bash
python3 scripts/validate-context-pack-schema.py docs/examples/common-example/context-pack-v1.yaml
```

位置づけ/差分は [Context Pack v1 仕様（検証コマンド）]({{ '/spec/context-pack-v1/' | relative_url }}#validation-commands) を参照してください。

（任意）CI相当の一括チェック: `npm run qa`（実行後に生成された検証レポートを確認する）

## YAML（全文） {#yaml-full}

```yaml
{% include_relative context-pack-v1.yaml %}
```
