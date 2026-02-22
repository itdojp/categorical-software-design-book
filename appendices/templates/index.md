---
title: "付録A: 設計成果物テンプレ集"
appendix: templates
---

# 付録A: 設計成果物テンプレ集

本書で用いる設計成果物（Design Artifacts）のテンプレです。章内で必要に応じて参照します。

## Context Pack（最小スケルトン）

```yaml
version: 1
name: <project-or-example-name>

problem_statement:
  goals: []
  non_goals: []

domain_glossary:
  terms: []

objects: []
morphisms: []
diagrams: []

constraints: {}
acceptance_tests: []
coding_conventions: {}
forbidden_changes: []
```

## Objects テンプレ（型/状態/不変条件/権限/エラー）

| 項目 | 内容 |
| --- | --- |
| id | 対象名（例: `Order`） |
| kind | entity / value / event |
| description | 対象の説明 |
| states | 状態（任意） |
| fields | 主要フィールド（任意） |
| invariants | 不変条件（Diagramsへの参照でも可） |
| permissions | 権限（誰が扱えるか） |
| errors | 関連エラー（分類/代表例） |
| audit | 監査（必要なイベント/属性） |

例（抜粋）:

| 項目 | 内容 |
| --- | --- |
| id | Order |
| kind | entity |
| description | 注文。状態遷移を持つ。 |
| states | Draft, Placed, Paid, Shipped, Cancelled |
| invariants | 禁止遷移（例: Shipped → Paid） |

## Morphisms テンプレ（シグネチャ、Pre/Post、失敗、冪等性）

| 項目 | 内容 |
| --- | --- |
| id | 操作名（例: `PlaceOrder`） |
| input | 入力（型/必須/制約） |
| output | 出力（型/必須） |
| actor | 操作者（任意、権限と紐づけ） |
| pre | 前提条件（成立しない場合は failures） |
| post | 事後条件（成立しない場合は仕様違反） |
| failures | 失敗条件（variant列挙） |
| idempotency | 冪等性（キー、スコープ、期待挙動） |
| side_effects | 副作用（DB/外部API/監査/通知等） |
| observability | ログ/メトリクス/トレース（任意） |

例（抜粋）:

```yaml
id: PlaceOrder
input: { orderId: "OrderId", idempotencyKey: "IdempotencyKey" }
output: { orderId: "OrderId" }
pre:
  - "Order.state == Draft"
post:
  - "Order.state == Placed"
  - "AuditEvent(\"PlaceOrder\") が記録される"
failures:
  - NotFound
  - InvalidState
  - OutOfStock
idempotency:
  key: idempotencyKey
  scope: orderId
  expectation: "重複実行しても在庫引当や監査が二重計上されない"
```

## Diagrams テンプレ（可換条件→テスト観点）

| 項目 | 内容 |
| --- | --- |
| id | 不変条件ID（例: `D2-audit-consistency`） |
| statement | 自然言語の条件 |
| involved | 関係する Objects/Morphisms |
| observation_points | 観測点（状態、戻り値、イベント、監査等） |
| verification | 検証項目（テスト観点） |
| test_level | Unit / Integration / Property |
| counterexample | 反例（任意） |

例（抜粋）:

```yaml
id: D2-audit-consistency
statement: "重要操作は必ず監査証跡を残す"
involved:
  objects: [AuditEvent]
  morphisms: [CreateOrder, PlaceOrder, AuthorizePayment, ShipOrder]
observation_points:
  - "操作成功時に AuditEvent が存在する"
verification:
  - "各操作に対応する監査イベントが記録される"
test_level: Integration
```

## レビュー用チェックリスト（AI生成物レビュー含む）

### 契約（Context Pack）レビュー

- Goals/Non-goals が明確（仕様追加の余地が小さい）
- Objects/Morphisms/Diagrams が揃っている（欠落がない）
- Pre/Post/failures が検証可能な表現になっている
- Forbidden changes が具体的（境界/契約/不変条件/依存など）

### AI生成物レビュー（逸脱検知）

- 関手性（第4章）:
  - 境界（Objects）が勝手に統合/分割されていない
  - 操作の合成（順序/依存）が勝手に変わっていない
- 自然性（第5章）:
  - Before/After の差分説明があり、可換チェック（テスト観点）がある
  - 互換性（API/データ/監査/権限）を破壊していない
- 効果境界（第9章）:
  - 副作用が勝手に増えていない
  - pure core / impure shell の境界が維持されている
