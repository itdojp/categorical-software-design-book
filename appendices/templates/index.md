---
title: "付録A: 設計成果物テンプレ集"
appendix: templates
---

# 付録A: 設計成果物テンプレ集

本書で用いる設計成果物（Design Artifacts）のテンプレです。章内で必要に応じて参照します。

## Context Pack（最小スケルトン）

このスケルトンは `scripts/validate-context-pack.py` を通る（Schema-valid）形です。

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

acceptance_tests:
  - id: AT1-happy-path
    scenario: "<scenario>"
    expected: ["<expected>"]

coding_conventions:
  language: language-agnostic
  directory: []
  dependencies: {}

forbidden_changes:
  - "<forbidden change>"
```

## Objects テンプレ（型/状態/不変条件/権限/エラー）

```yaml
objects:
  - id: <ObjectId>
    kind: entity # entity | value | event
    description: ""
    states: []
    fields: []
    invariants: []
    permissions: []
    errors: []
    audit: {}
```

例（抜粋）:

```yaml
objects:
  - id: Order
    kind: entity
    description: "注文。状態遷移を持つ。"
    states: [Draft, Placed, Paid, Shipped, Cancelled]
    invariants:
      - "禁止遷移（例: Shipped → Paid）"
```

## Morphisms テンプレ（シグネチャ、Pre/Post、失敗、冪等性）

```yaml
morphisms:
  - id: <MorphismId>
    input: {}
    output: {}
    actor: "" # 任意（権限と紐づけ）
    pre: []
    post: []
    failures: []
    idempotency: {} # 任意
    side_effects: [] # 任意
    observability: {} # 任意
```

例（抜粋）:

```yaml
morphisms:
  - id: PlaceOrder
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

```yaml
diagrams:
  - id: <DiagramId>
    statement: "<invariant statement>"
    involved:
      objects: []
      morphisms: []
    observation_points: []
    verification: []
    test_level: Integration # Unit | Integration | Property
    counterexample: "" # 任意
```

例（抜粋）:

```yaml
diagrams:
  - id: D2-audit-consistency
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

- 関手性（[第4章](../../chapters/chapter04/)）:
  - 境界（Objects）が勝手に統合/分割されていない
  - 操作の合成（順序/依存）が勝手に変わっていない
- 自然性（[第5章](../../chapters/chapter05/)）:
  - Before/After の差分説明があり、可換チェック（テスト観点）がある
  - 互換性（API/データ/監査/権限）を破壊していない
- 効果境界（[第9章](../../chapters/chapter09/)）:
  - 副作用が勝手に増えていない
  - pure core / impure shell の境界が維持されている
