---
title: "Context Pack v2 仕様"
description: "Context Pack v1 を壊さず、Agent Runtime・データ契約・効果境界・検証証跡を追加する拡張仕様"
permalink: /spec/context-pack-v2/
---

# Context Pack v2 仕様

Context Pack v2 は、Context Pack v1 の `Problem statement / Domain glossary / Objects / Morphisms / Diagrams / Constraints / Acceptance tests / Coding conventions / Forbidden changes` を残したまま、AI エージェント実行、データ契約、効果境界、guardrail、trace evidence、resource constraints、変更意味論を追加する拡張です。

v2 は v1 の置換ではありません。v1 だけで十分な小さな実装委任では v1 を使い、AI エージェントの tool call、外部データ境界、監査証跡、予算・権限・PII 制約までレビューしたい場合に v2 を使います。

注記: このページは Context Pack v2 の形式と必須項目の正本です。v1 の正本は [Context Pack v1 仕様]({{ '/spec/context-pack-v1/' | relative_url }}) です。

## v1 互換性と移行方針

- v2 は v1 の必須項目を削除しない。
- v2 の YAML では `version: 2` と `context_pack_version: 2` を明示する。
- 既存 v1 YAML はそのまま有効であり、v2 対応のために破壊的に書き換えない。
- v1 から v2 へ移行する場合は、まず v1 の `Objects / Morphisms / Diagrams / Acceptance tests / Forbidden changes` を検証し、その後に v2 追加フィールドを差分として足す。
- v2 追加フィールドは、圏論語彙の比喩利用、設計成果物への対応づけ、検証条件を混同しないために `formalization_level` で明示する。

## 検証コマンド {#validation-commands}

依存導入（初回のみ）は次のとおりです。

```bash
python3 -m pip install -r scripts/requirements-qa.txt
```

minimal lint（必須項目/型/ID重複/参照整合の簡易検証）を実行します。`context_pack_version: 2` がある場合は v2 の追加項目も検証されます。

```bash
python3 scripts/validate-context-pack.py docs/examples/minimal-example/context-pack-v2.yaml
python3 scripts/validate-context-pack.py docs/examples/common-example/context-pack-v2.yaml
```

schema validation（JSON Schema）を実行します。schema は YAML の `context_pack_version` から自動選択されます。明示したい場合は `--schema docs/spec/context-pack-v2.schema.json` を指定します。

```bash
python3 scripts/validate-context-pack-schema.py docs/examples/minimal-example/context-pack-v2.yaml
python3 scripts/validate-context-pack-schema.py docs/examples/common-example/context-pack-v2.yaml
python3 scripts/validate-context-pack-schema.py --schema docs/spec/context-pack-v2.schema.json docs/examples/common-example/context-pack-v2.yaml
```

機械可読スキーマ（JSON Schema）は次を参照してください。

- [Context Pack v2 JSON Schema]({{ '/docs/spec/context-pack-v2.schema.json' | relative_url }})
- [Context Pack v1 JSON Schema]({{ '/docs/spec/context-pack-v1.schema.json' | relative_url }})

## 追加フィールド一覧

| フィールド | 目的 | 後続Issueとの関係 |
| --- | --- | --- |
| `data_contracts` | schema、mapping、migration verification を記録する | CQL / Functorial Data Migration の章追加で詳細化する |
| `open_systems` | component、boundary、composition を外部境界付きで記録する | Structured Cospans / Open Systems の章追加で詳細化する |
| `views.lenses_or_optics` | view、projection、更新規則を記録する | Optics / Lenses の章追加で詳細化する |
| `effects` | effect operation と handler、safety note を分離する | Algebraic Effects / Effect Handlers の章追加で詳細化する |
| `agent_runtime` | allowed / forbidden tools、guardrails、trace evidence を記録する | MCP / Agent Runtime Contract の章追加で詳細化する |
| `resource_constraints` | tool budget、data sensitivity、linear resource を記録する | Graded / Linear Resource Types の章追加で詳細化する |
| `change_semantics` | 許可する refactor、禁止する conflict 解決、merge invariant を記録する | Patch Theory / Version Control Semantics の章追加で詳細化する |
| `formalization_level` | 比喩、機械検証、CI、手動レビューを分ける | 全章横断の誤読防止 |

## 圏論語彙の扱い

v2 では、圏論語彙を次の3層へ分けて記録します。

| 層 | 書く場所 | 例 | 判断基準 |
| --- | --- | --- | --- |
| 比喩 | `formalization_level.metaphor_only` | サービス境界を Object と呼ぶ | 説明の助けであり、数学的証明ではない |
| 対応づけ | `data_contracts` / `open_systems` / `views` / `effects` | OrderSchema と Order object の対応 | 設計成果物としてレビューできる |
| 検証条件 | `acceptance_tests` / `merge_invariants` / `tested_by_ci` | D2-audit-consistency を CI で確認する | コマンド、テスト、レビュー証跡で確認できる |

「圏論だから正しい」とは書きません。正しさを主張する場合は、どの契約・テスト・CI・レビュー証跡で確認したかに落とします。

## 必須フィールド

最小限、次の v2 追加フィールドを扱います。

```yaml
context_pack_version: 2

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

## フィールドの書き方

### data_contracts

`schemas` には対象とするデータ構造、`mappings` には対応関係、`migration_verification` には移行時の確認条件を書きます。`schemas` / `mappings` / `migration_verification` は、簡単な文字列の配列でも、`id`、`source`、`target`、`preserves`、`type`、`expected` などを持つ構造化オブジェクトの配列でも構いません。ここでは CQL / Functorial Data Migration の詳細な理論説明は行わず、後続の第7章追加に接続できる設計成果物の受け皿として扱います。

構造化して書く場合の最小例は次のとおりです。

```yaml
data_contracts:
  schemas:
    - id: LegacyOrderDB
      role: source
    - id: OrderReadModel
      role: target
    - id: AuditEventSchema
      role: lineage_source
      fields: [eventId, lineage]
  mappings:
    - id: legacy_to_read_model
      source: LegacyOrderDB
      target: OrderReadModel
      preserves:
        - OrderId
        - PaymentAuthorization
        - AuditEvent.lineage
      does_not_preserve:
        - legacy_internal_status_text
  migration_verification:
    - type: row_count_invariant
    - type: foreign_key_preservation
    - type: lineage_trace_check
    - type: acceptance_query
```

### open_systems

`components` には責務境界、`boundaries` には外部との接点、`composition` には合成後も守る不変条件を書きます。境界を超える外部システムの詳細を Context Pack 内へ混ぜず、観測できる契約へ落とします。

### views.lenses_or_optics

読み取り view、射影、更新規則を明示します。view の追加が元データの制約や監査条件を破らないかをレビューできるようにします。

### effects

外部I/O、永続化、tool call、監査ログ追記などを `operations` として列挙し、どの `handlers` が扱うかを分けます。`effect_safety_notes` には、成功条件、失敗条件、再試行、冪等性、監査上の注意を書きます。

### agent_runtime

`allowed_tools` と `forbidden_tools` で実行環境の境界を固定します。`guardrails` は入力検証、出力検証、tool invocation の制約を書き、`trace_evidence` はPR、CI、レビュー、ログなど後から監査できる証跡を書きます。

### resource_constraints

`tool_budget` は tool call 回数や CI 時間などの予算、`data_sensitivity` は PII・本番データ・監査ログの扱い、`linear_resources` はワンタイムトークンや冪等性キーなど再利用してはいけない資源を記録します。

### change_semantics

`allowed_refactors` は許可する意味保存の変更、`forbidden_conflict_resolutions` は禁止する衝突解決、`merge_invariants` はマージ前に守る不変条件を書きます。

### formalization_level

- `metaphor_only`: 説明上の比喩であり、検証済みとは言わない項目。
- `machine_checked`: 証明器やモデル検査などで機械確認した項目。
- `tested_by_ci`: テストや schema validation で CI 確認する項目。
- `reviewed_manually`: 人間レビューで確認する項目。

この分離により、圏論語彙の比喩利用、CI 検証、機械検証、手動レビューを混同しません。

## 最小の有効例（Minimal valid example）

以下は「v1 の必須キー＋ v2 追加フィールド」だけで成立する例です。authoring / local 検証用の source は `docs/examples/minimal-example/context-pack-v2.yaml` です。

```yaml
version: 2
context_pack_version: 2
name: minimal-example-v2

problem_statement:
  goals: ["最小の v2 例として成立させる"]
  non_goals: ["v1 の必須項目を削除しない"]

domain_glossary:
  terms:
    - term: Order
      ja: 注文

objects:
  - id: Order
    kind: entity
    fields: [orderId, state]

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

data_contracts:
  schemas:
    - id: OrderSchema
      object: Order
      fields: [orderId, state]
  mappings: []
  migration_verification: []

open_systems:
  components:
    - id: OrderService
      boundary: "注文状態の更新だけを担当する"
  boundaries:
    - id: OrderApiBoundary
      rule: "入力検証を通過した PlaceOrder だけを受け付ける"
  composition: []

views:
  lenses_or_optics:
    - id: OrderStateView
      source: Order
      focus: state
      update_rule: "state 更新は Diagrams と acceptance_tests を破らない範囲に限る"

effects:
  operations:
    - id: PersistOrder
      kind: write
  handlers:
    - id: OrderRepository
      handles: [PersistOrder]
  effect_safety_notes:
    - "永続化は PlaceOrder の post 条件と監査可能な結果で確認する"

agent_runtime:
  allowed_tools:
    - "local test runner"
  forbidden_tools:
    - "production database"
  guardrails:
    input_validation:
      - "Context Pack の必須フィールドが欠落していないこと"
    output_validation:
      - "Forbidden changes を破る差分を出力しないこと"
    tool_invocation:
      - "許可された local tool だけを使うこと"
  trace_evidence:
    required:
      - "実行した検証コマンド"
      - "レビューで確認した Diagram id"

resource_constraints:
  tool_budget:
    max_tool_calls: 20
  data_sensitivity:
    pii: "none"
    production_data: "prohibited"
  linear_resources:
    - id: OneTimeToken
      rule: "再利用禁止。使用したら trace_evidence に記録する"

change_semantics:
  allowed_refactors:
    - "内部実装の名前変更。ただし public contract と Diagram は維持する"
  forbidden_conflict_resolutions:
    - "InvalidState を成功扱いに変更すること"
  merge_invariants:
    - "D1-order-state と AT1-happy-path が通ること"

formalization_level:
  metaphor_only:
    - "Order を Object と呼ぶ説明は設計上の比喩であり、数学的証明ではない"
  machine_checked: []
  tested_by_ci:
    - "AT1-happy-path"
  reviewed_manually:
    - "data_contracts と diagrams の対応づけ"
```

## 共通例題

注文処理の Context Pack v2 は次を参照します。

- [共通例題: 注文処理]({{ '/examples/common-example/' | relative_url }})
- local 検証用 YAML: `docs/examples/common-example/context-pack-v2.yaml`
