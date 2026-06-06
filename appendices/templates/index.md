---
title: "付録A: 設計成果物テンプレ集"
appendix: templates
---

# 付録A: 設計成果物テンプレ集

本書で用いる設計成果物（Design Artifacts）のテンプレです。章内で必要に応じて参照します。
用語の定義を引き直すときは [用語集（Glossary）]({{ '/glossary/' | relative_url }}) を、
図版・チェックリスト・症状別の戻り先を引き直すときは
[付録D: クイックリファレンス](../../appendices/desk-reference/) を参照してください。

## Context Pack（最小スケルトン）

このスケルトンは「着手用」の最小形です。まずは `scripts/validate-context-pack.py` の minimal lint（必須フィールド/型/ID重複/参照整合の簡易検証）で破綻を早期検知し、内容が具体化した段階で schema validation（JSON Schema による仕様準拠チェック）も通します。

検証コマンドの詳細は [Context Pack v1 仕様（検証コマンド）]({{ '/spec/context-pack-v1/' | relative_url }}#validation-commands) と [Context Pack v2 仕様（検証コマンド）]({{ '/spec/context-pack-v2/' | relative_url }}#validation-commands) を参照してください。

注意: schema validation はプレースホルダ（例: `name: <project-or-example-name>`）を具体値へ置換した段階で通す想定です。

注記: 本付録は reader-facing な雛形集です。説明が食い違う場合は、まず [公開トップページの「確認したいこと別の正本」]({{ '/' | relative_url }}#確認したいこと別の正本) を参照してください。形式と必須項目は [Context Pack v1 仕様]({{ '/spec/context-pack-v1/' | relative_url }}) / [Context Pack v2 仕様]({{ '/spec/context-pack-v2/' | relative_url }})、実行手順は各仕様の検証コマンド、語義は [用語集（Glossary）]({{ '/glossary/' | relative_url }})、版差は [CHANGELOG](https://github.com/itdojp/categorical-software-design-book/blob/main/CHANGELOG.md) を確認します。

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

## Context Pack v2（Agent Runtime 拡張スケルトン）

AI エージェントの tool call、guardrail、trace evidence、データ契約、効果境界までレビュー対象にする場合は v2 を使います。v2 は v1 の必須項目を削除しない拡張です。詳細は [Context Pack v2 仕様]({{ '/spec/context-pack-v2/' | relative_url }}) を参照してください。

```yaml
version: 2
context_pack_version: 2
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
coding_conventions:
  language: language-agnostic
  directory: []
  dependencies: {}
forbidden_changes: []

data_contracts:
  schemas: []
  mappings: []
  migration_verification: []

open_systems:
  components: []
  boundaries: []
  composition: []

views:
  lenses_or_optics: []

effects:
  operations: []
  handlers: []
  effect_safety_notes: []

agent_runtime:
  allowed_tools: []
  forbidden_tools: []
  guardrails: {}
  trace_evidence: {}

resource_constraints:
  tool_budget: {}
  data_sensitivity: {}
  linear_resources: []

change_semantics:
  allowed_refactors: []
  forbidden_conflict_resolutions: []
  merge_invariants: []

formalization_level:
  metaphor_only: []
  machine_checked: []
  tested_by_ci: []
  reviewed_manually: []
```

## 理論・実装接続レビューゲート（Phase 5）

圏論の語彙をソフトウェア設計へ対応づける場合は、対応を「説明」だけで終わらせず、Context Pack と検証条件へ戻せる形で記録します。

- 用語・記号の一貫性:
  - Object / Morphism / Functor / Natural transformation / Product / Coproduct / Monad / Kleisli の表記が用語集と矛盾しないこと。
  - 戻り先: [用語集（Glossary）]({{ '/glossary/' | relative_url }})
- 対応づけの明示:
  - 元の理論概念、対応する設計成果物、保存したい構造、保存しないことを同じ箇所に書くこと。
  - 戻り先: [第4章]({{ '/chapters/chapter04/' | relative_url }}) / [第5章]({{ '/chapters/chapter05/' | relative_url }})
- 検証可能性:
  - 図式や不変条件が、Acceptance test、property、review checklist のいずれかへ落ちていること。
  - 戻り先: [Context Pack v1 仕様]({{ '/spec/context-pack-v1/' | relative_url }})
- 適用範囲と限界:
  - 「圏論だから正しい」と断定せず、実務上の前提、適用しない場面、未確定事項を残すこと。
  - 戻り先: [付録D]({{ '/appendices/desk-reference/' | relative_url }})
- 関連書との分界:
  - 日本語本は Context Pack / GitHub / CI 運用、英語本は compositional design / verifiable engineering の全体像という役割差を保つこと。
  - 戻り先: 公開トップページの「関連書について」

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

この節は詳細版のチェックリストです。まず論点を絞りたい場合は、[付録D: クイックリファレンス](../../appendices/desk-reference/) の「レビュー前の最小確認項目」から入ってください。

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
