---
title: "Context Pack v1 仕様"
description: "AIエージェントに設計成果物を引き渡すための入出力契約"
---

# Context Pack v1 仕様

本書における **Context Pack** は、人間が作る設計成果物を、AIエージェントが実装/テストへ落とすための入力契約です。章末演習・実務適用では、この形式を維持します。

## 目的

- AIに委任する範囲（実装/テスト/リファクタ）を明確化する
- AIが勝手に解釈・改変しやすい点（境界/不変条件/権限/失敗条件）を固定する
- 検証可能性（テスト/可換性チェック）を先に確保する

## フォーマット（推奨: YAML）

Context Pack は YAML/JSON のいずれでもよいが、レビュー容易性のため YAML を推奨します。

機械可読スキーマ:
- JSON Schema: [context-pack-v1.schema.json](context-pack-v1.schema.json)（[raw](https://raw.githubusercontent.com/itdojp/categorical-software-design-book/main/docs/spec/context-pack-v1.schema.json)）

簡易lint（必須項目/型チェック）:

```bash
python3 scripts/validate-context-pack.py docs/examples/common-example/context-pack-v1.yaml
```

最小構成（v1）は以下です。

### 1. Problem statement

- 目的（Goals）
- 非目的（Non-goals）
- スコープ（In/Out）

### 2. Domain glossary

- 用語定義（日本語/英語、別名）
- 主要な略語

### 3. Objects

ドメインの「型/状態/権限/エラー」を列挙します。

- Entity / Value Object
- State machine（必要な場合）
- Error taxonomy（分類）

### 4. Morphisms

操作/API（コマンド/クエリ）を列挙し、最低限以下を含めます。

- 入力/出力
- Pre/Post（前提/事後条件）
- 失敗条件（エラー）
- 監査（必要な場合）

### 5. Diagrams（可換図式＝不変条件）

システムが満たすべき不変条件を列挙します。

必須:
- 条件（自然言語）
- 検証方法（受入テスト/プロパティ/チェック観点）

### 6. Constraints

- 性能（SLO/タイムアウト/再試行）
- セキュリティ（権限/監査/PII）
- 運用（可観測性/障害対応）

### 7. Acceptance tests（最小セット）

DoD として必要な受入テストを列挙します（シナリオ/期待結果）。

### 8. Coding conventions

- 言語/フレームワーク
- ディレクトリ構成
- 依存（追加禁止も含む）

### 9. Forbidden changes

AIが勝手に変更してはいけない事項を明示します。

例:
- 公開APIの互換性
- 不変条件（Diagrams）
- 権限境界（ACL/RBAC）

## 最小の有効例（Minimal valid example）

以下は「必須キー＋最小要素」だけで成立する例です（章末演習の叩き台）。

```yaml
version: 1
name: minimal-example

problem_statement:
  goals: ["最小の例として成立させる"]
  non_goals: ["仕様追加をしない"]

domain_glossary:
  terms:
    - term: Order
      ja: 注文

objects:
  - id: Order
    kind: entity

morphisms:
  - id: PlaceOrder
    input: { orderId: "OrderId" }
    output: { orderId: "OrderId" }
    pre: ["Order.state == Draft"]
    post: ["Order.state == Placed"]
    failures: ["InvalidState"]

diagrams:
  - id: D1-order-state
    statement: "PlaceOrder は Draft のみに適用できる"
    verification: ["Draft 以外では InvalidState になる"]

constraints: {}

acceptance_tests:
  - id: AT1-happy-path
    scenario: Draft の Order に PlaceOrder を適用する
    expected: ["Order.state == Placed"]

coding_conventions:
  language: language-agnostic
  directory: []
  dependencies: {}

forbidden_changes:
  - "Diagrams を満たさない変更"
```

## 例（共通例題）

共通例題（注文処理）の Context Pack v1 は次を参照します。

- 共通例題ページ（HTML）: [docs/examples/common-example/](../examples/common-example/)
- YAML（raw）: [raw](https://raw.githubusercontent.com/itdojp/categorical-software-design-book/main/docs/examples/common-example/context-pack-v1.yaml)
- YAML（GitHub）: [GitHub](https://github.com/itdojp/categorical-software-design-book/blob/main/docs/examples/common-example/context-pack-v1.yaml)
