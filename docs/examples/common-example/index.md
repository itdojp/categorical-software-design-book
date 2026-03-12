---
title: "共通例題: 注文処理（Context Pack v1）"
description: "全章で参照する共通例題（Order/Payment/Inventory/Shipment/Audit）"
permalink: /examples/common-example/
---

# 共通例題: 注文処理（Context Pack v1）

本ページは、本文理解を補助するための要約ページです。章本文の代替ではなく、
共通例題の骨格を 1 画面で把握し、必要なときに YAML 全文へ降りるための導線として使います。

## 1画面サマリ

### 概要

- 対象領域は `Order / Payment / InventoryReservation / Shipment / AuditEvent` の 5 つです
- 代表フローは `CreateOrder → PlaceOrder → AuthorizePayment → ShipOrder` です
- 重点は「監査を後付けにしないこと」と「状態遷移を不変条件として固定すること」です

### 主要 Object

<table>
  <thead>
    <tr>
      <th>Object</th>
      <th>役割</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>Order</code></td>
      <td>注文本体。<code>Draft → Placed → Paid → Shipped / Cancelled</code> の状態を持ちます。</td>
    </tr>
    <tr>
      <td><code>Payment</code></td>
      <td>決済承認の結果を保持します。</td>
    </tr>
    <tr>
      <td><code>InventoryReservation</code></td>
      <td>在庫引当の成否と状態を保持します。</td>
    </tr>
    <tr>
      <td><code>Shipment</code></td>
      <td>出荷指示と出荷完了を表します。</td>
    </tr>
    <tr>
      <td><code>AuditEvent</code></td>
      <td>重要操作の監査証跡を保持します。</td>
    </tr>
  </tbody>
</table>

### 主要 Morphism

- <code>CreateOrder</code>: 空でない明細から <code>Draft</code> の注文を作り、監査を残します
- <code>PlaceOrder</code>: <code>Draft</code> を <code>Placed</code> へ進め、在庫引当と監査を発生させます
- <code>AuthorizePayment</code>: 引当済み注文を決済承認し、<code>Paid</code> へ進めます
- <code>ShipOrder</code>: <code>Paid</code> の注文だけを出荷し、<code>Shipped</code> へ進めます

### 主要 Diagram

- <code>D1-idempotency-place-order</code>: <code>PlaceOrder</code> を重複実行しても在庫引当と監査が二重化しません
- <code>D2-audit-consistency</code>: 重要操作は必ず監査証跡を残します
- <code>D3-state-transition-safety</code>: 禁止状態遷移は <code>InvalidState</code> で止まります

### 主要 Acceptance test

- <code>AT1-happy-path</code>: 作成から出荷までの正常系を通します
- <code>AT2-invalid-transition</code>: 禁止状態遷移が失敗することを確認します
- <code>AT3-audit-search-export</code>: 監査検索とエクスポートの運用要件を確認します

## 導線

- Context Pack v1 仕様: [Context Pack v1 仕様](../../spec/context-pack-v1.md)
- 例題 Context Pack（YAML）:
  - raw（推奨）: [raw](https://raw.githubusercontent.com/itdojp/categorical-software-design-book/main/docs/examples/common-example/context-pack-v1.yaml)
  - GitHub: [GitHub](https://github.com/itdojp/categorical-software-design-book/blob/main/docs/examples/common-example/context-pack-v1.yaml)
  - サイト内で読む: [YAML（全文）](#yaml-full)

## 検証（ローカル）

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

（任意）CI相当の一括チェック: `npm run qa`（レポート: `qa-reports/*.json`）

## YAML（全文） {#yaml-full}

```yaml
{% include_relative context-pack-v1.yaml %}
```
