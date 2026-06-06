---
title: "共通例題: 注文処理（Context Pack v1/v2）"
description: "全章で参照する共通例題（Order/Payment/Inventory/Shipment/Audit）と v2 拡張"
permalink: /examples/common-example/
---

# 共通例題: 注文処理（Context Pack v1/v2）

本ページは、本文・仕様ページから「共通例題の Context Pack」に確実に到達するためのハブです。v1 は注文処理の基本契約、v2 は同じ注文処理へ Agent Runtime・データ契約・効果境界・検証証跡を追加した拡張例です。

注記: 公開ページ本文と同じ版を確認したい場合は、このページ内に埋め込まれた YAML を優先してください。GitHub の repository view では埋め込み表示が展開されないため、その場合は同階層の [`context-pack-v1.yaml`](./context-pack-v1.yaml) / [`context-pack-v2.yaml`](./context-pack-v2.yaml) を参照します。版差が疑われる場合は、CHANGELOG とコミット履歴を確認します。

## 導線

- Context Pack v1 仕様: [Context Pack v1 仕様]({{ '/spec/context-pack-v1/' | relative_url }})
- Context Pack v2 仕様: [Context Pack v2 仕様]({{ '/spec/context-pack-v2/' | relative_url }})
- 例題 Context Pack（YAML）:
  - v1 をサイト内で読む（公開版スナップショット）: [v1 YAML（全文）](#yaml-v1-full)
  - v2 をサイト内で読む（公開版スナップショット）: [v2 YAML（全文）](#yaml-v2-full)

## v2で追加されるレビュー対象

共通例題の v2 では、既存の `Order / Payment / Inventory / Shipment / Audit` と `D1 / D2 / D3` を保ったまま、次を追加します。

- `data_contracts`: OrderSchema、AuditEventSchema、LegacyOrderDB、OrderReadModel と、監査 lineage を保った read model 移行検証。
- `effects`: 永続化、在庫引当、監査ログ追記、監査エクスポートを operation / handler に分離。特に `ReserveInventory` は本番 handler と test handler を分ける。
- `agent_runtime`: tool contract 形式の allowed tools / forbidden tools、input / output / tool invocation guardrails、PR・CI・review の trace evidence。
- `resource_constraints`: CI 時間、PII、本番データ、冪等性キー、ワンタイム決済トークン。
- `formalization_level`: 比喩、CI検証、手動レビューを分け、圏論語彙を検証済み主張と混同しない。

## 検証（ローカル）

注記: 以下のコマンドは local checkout 上の `docs/examples/common-example/*.yaml` を検証します。公開ページの YAML と同じ版を再現したい場合は、対象の commit / tag に合わせてから実行してください。

依存導入（初回のみ）:

```bash
python3 -m pip install -r scripts/requirements-qa.txt
```

minimal lint:

```bash
python3 scripts/validate-context-pack.py docs/examples/common-example/context-pack-v1.yaml
python3 scripts/validate-context-pack.py docs/examples/common-example/context-pack-v2.yaml
```

schema validation（JSON Schema）:

```bash
python3 scripts/validate-context-pack-schema.py docs/examples/common-example/context-pack-v1.yaml
python3 scripts/validate-context-pack-schema.py docs/examples/common-example/context-pack-v2.yaml
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
