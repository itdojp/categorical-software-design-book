---
title: "第9章: モナド/クライスリ（効果境界の設計）"
chapter: chapter09
---

# 第9章: モナド/クライスリ（効果境界の設計）

副作用を domain 判断と同じ場所に置くと、
仕様とテストが急速に読めなくなります。
第9章では、pure core / impure shell を
効果境界として整理します。

本章の見せ場は、pure core / impure shell 図と core / shell 対応表です。
どの判断を純粋に保ち、どの処理を境界へ追い出すかを、その場で確認できます。

## 学習ゴール

- pure core / impure shell の設計原則を説明できる
- 失敗モデル・リトライ・冪等性・監査ログを「効果」として境界へ隔離できる
- AIへの指示として「副作用を勝手に増やさない」「境界を守る」を明文化できる
- 図式（Diagrams）から、効果境界のテスト戦略へ落とせる
- 運用要件（監査・信頼性）を破壊しない実装委任ができる

## 圏論コア（定義・直観・ミニ例）

モナド（Monad）とクライスリ（Kleisli）は、効果（IO/DB/例外/リトライ等）を含む計算を合成可能にするための枠組みです。本章では、厳密な公理よりも設計上の直観を優先します。

- 効果付きの型: `M A`（例: `Result<A, E>`, `Task<A>`, `IO<A>`）
- 効果付きの射（クライスリ射）: `A → M B`
- 合成: `A → M B` と `B → M C` を合成して `A → M C` を作る（エラー伝播や副作用の順序を含む）

ミニ例（型シグネチャと変換の形）は次のとおりです。

- `f: A → Result<B, E>`
- `g: B → Result<C, E>`
- `h: A → Result<C, E>`（`h = kleisliCompose(f, g)`、圏論の記法では `h = g ∘ f` に相当）

`h` は次のように「失敗を伝播し、成功なら次の変換へ進む」形になる（`flatMap`/`andThen`/`bind` 等、API 名は実装により異なる）。ここで `kleisliCompose(f, g)` は「先に `f`、次に `g`」を意味し、圏論の記法では `g ∘ f` に対応する。

```ts
type Result<A, E> = { ok: true; value: A } | { ok: false; error: E };

const kleisliCompose =
  <A, B, C, E>(f: (a: A) => Result<B, E>, g: (b: B) => Result<C, E>) =>
  (a: A): Result<C, E> => {
    const rb = f(a);
    return rb.ok ? g(rb.value) : rb;
  };

// h = kleisliCompose(f, g) （= g ∘ f）
```

直観は次のとおりです。

「効果を型に押し上げ、合成規則を明示する」と、AIに委任しても境界が崩れにくい。逆に、効果が暗黙（グローバル状態、隠れDBアクセス、暗黙リトライ）だと、合成や検証が破綻します。

## ソフトウェア設計への射影（どこに効くか）

AI委任が難しいのは、効果が絡む領域です。

- IO/DB/外部API
- 例外、再試行、タイムアウト
- 冪等性、監査ログ

本章の基本方針は pure core / impure shell です。

- pure core:
  - ドメイン判断（状態遷移、検証、計算）を純粋関数として定義する
  - 入力→出力が明確でテストしやすい
- impure shell:
  - DB/外部API/監査/リトライなどの効果をここへ閉じ込める
  - 失敗モデル（failures）と再試行規則を Context Pack として固定する

<figure class="diagram-with-fallback">
  <div class="mermaid-live">
    <div class="mermaid-wrapper">
      <div class="mermaid">
graph LR
  IN["Command / Input"] --> CORE["pure core（判断/状態遷移）"]
  CORE --> SHELL["impure shell（DB/外部API/監査/リトライ）"]
  SHELL --> OUT["Result / Output"]
      </div>
    </div>
  </div>
  <div class="mermaid-fallback">
    <img src="{{ '/assets/images/chapter09/pure-core-impure-shell.svg' | relative_url }}" alt="pure core / impure shell 図の fallback SVG。入力が pure core に入り、その結果が impure shell を経て出力になる。">
  </div>
  <figcaption>図: pure core / impure shell。入力は純粋な判断ロジックに入り、その結果だけを効果境界へ渡して DB・外部 API・監査・再試行を処理します。</figcaption>
</figure>

共通例題（注文処理）の観点は次のとおりです。

- `PlaceOrder` は在庫引当、監査、状態遷移を含む。ここで効果を増やすと、冪等（D1）や監査整合（D2）が壊れやすい。

## 設計成果物（テンプレ：表/図式/チェックリスト）

参照先は次のとおりです。

- 共通例題（Context Pack v1）: [共通例題: 注文処理]({{ '/examples/common-example/' | relative_url }})

### 効果境界テンプレ（最小）

```yaml
constraints:
  effect_boundary:
    pure_core: [] # 純粋にできる判断（状態遷移、計算、検証）
    impure_shell: [] # 効果（DB/外部API/監査/リトライ）
    failures: [] # 失敗モデル（variant列挙）
    retry: {} # 再試行方針（条件、回数、バックオフ、タイムアウト）
    idempotency: {} # 冪等性の鍵（キー、スコープ、保持期間）
    audit: {} # 監査イベント（必須項目、改竄検知）
    diagrams: [] # 効果境界に関する不変条件（例: D1, D2）
```

例（方針イメージ）は次のとおりです。

```text
pure core:
  decidePlaceOrder(order, inventory) -> Decision
impure shell:
  loadOrder(orderId) -> IO<Result<Order, NotFound>>
  reserveInventory(order) -> IO<Result<Reservation, OutOfStock>>
  appendAudit(event) -> IO<Unit>
```

## 第9章補論: Kleisli arrow と Agent tool call

AI エージェントの tool call も、効果付き計算として扱えます。たとえば `get_order` は入力 schema を受け取り、DB 読み取り、権限確認、PII マスキング、失敗を含む出力を返します。これは単なる `A -> B` ではなく、外部世界との相互作用を含む `A -> M B` として扱う方が安全です。

Model Context Protocol（MCP）は、LLM アプリケーションと外部データソース / tool を接続する open protocol として定義されています（[MCP specification 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25)）。本書では MCP の詳細仕様を再掲せず、tool input/output schema、権限、guardrail、trace evidence を Context Pack v2 の契約へ落とします。

対応は次のとおりです。

| 圏論 | Agent runtime |
| --- | --- |
| `A` | tool input schema |
| `B` | tool output schema |
| `M` | 外部世界との相互作用、失敗、権限、監査、非決定性 |
| Kleisli composition | tool call chain / workflow |
| unit | 純粋値を effect context へ持ち上げる |
| bind | 前段 tool 結果を次段 tool へ渡す |
| law violation | retry、重複実行、副作用漏れ、監査欠落、非 idempotent 実行 |

この対応で重要なのは、tool call chain を「便利な手順」ではなく、合成される効果としてレビューすることです。`get_order` の出力を `cancel_order` に渡す場合、`tenant_id`、権限、`Order.state`、idempotency key、監査イベントが保存されなければ、Kleisli 合成の直観は破綻します。

```yaml
agent_runtime:
  allowed_tools:
    - name: get_order
      protocol: MCP
      effect: ReadDB
      input_schema_ref: schemas/GetOrderInput.json
      output_schema_ref: schemas/GetOrderOutput.json
      preconditions:
        - tenant_id_is_bound
        - caller_has_order_read_permission
      postconditions:
        - no_write_performed
        - pii_fields_redacted_unless_allowed

    - name: cancel_order
      protocol: MCP
      effect: WriteDB
      input_schema_ref: schemas/CancelOrderInput.json
      output_schema_ref: schemas/CancelOrderOutput.json
      idempotency_key: order_id
      audit_required: true
      retry_policy: bounded

  forbidden_tools:
    - direct_sql_write
    - shell_without_sandbox
    - network_call_to_unregistered_endpoint

  guardrails:
    input:
      - reject_cross_tenant_request
    output:
      - verify_no_secret_exfiltration
    tool:
      - validate_tool_input_schema
      - validate_tool_output_schema

  trace_evidence:
    required_spans:
      - llm_generation
      - tool_call
      - guardrail_result
      - handoff
    retention_policy: project_default
```

OpenAI Agents SDK は、Agents、tools、handoffs、guardrails、tracing などの primitives を提供する実装例です。公式ドキュメントでは、guardrails は input / output / tool invocation の検証点として説明され、tracing は generation、function tool call、guardrail、handoff などを span として記録します（[Agents SDK Guardrails](https://openai.github.io/openai-agents-python/guardrails/)、[Agents SDK Tracing](https://openai.github.io/openai-agents-python/tracing/)）。ただし、本書では特定 SDK に閉じません。OpenAI Agents SDK、GitHub Copilot agent、Codex などは、Agent Runtime Contract を実装・運用する具体例として扱います。

### law violation をレビュー観点へ落とす

Kleisli の law をここで証明する必要はありません。実務では、破綻を次のレビュー観点へ落とします。

- retry:
  - 同じ `idempotency_key` で二重取消が起きないか。
- 重複実行:
  - tool call が再実行されても監査イベントが二重集計されないか。
- 副作用漏れ:
  - `get_order` のような read tool が write を行っていないか。
- 監査欠落:
  - `cancel_order` 成功時に `tool_call` と `guardrail_result` の trace が残るか。
- 非 idempotent 実行:
  - retry policy が bounded で、失敗時の再実行条件が明示されているか。


## 第9章補論: Monad から Algebraic Effects へ

Monad / Kleisli は、副作用を `M` に包み、`A -> M B` を安全に合成する考え方です。
この説明は本章の基本線として残します。
一方で、AI agent の tool 実行契約では、「どの操作を要求するか」と
「その操作をどの環境でどう実行するか」を分けて固定したい場面があります。
ここで Algebraic Effects / Effect Handlers の見方が役に立ちます。

| 見方 | 設計で固定するもの | AI agent tool call での読み替え |
| --- | --- | --- |
| Monad | 副作用を `M` に包み、合成規則を明示する | tool call chain を `A -> M B` としてレビューする |
| Algebraic Effects | 必要な operation を宣言する | `ReserveInventory`、`AppendAuditEvent` のような要求を列挙する |
| Handlers | operation の解釈・実行方法を決める | 本番MCP、test double、local fake、監査付き実装を切り替える |

重要なのは、Monad を否定することではありません。
Monad は効果付き計算の合成を説明し、Algebraic Effects は operation と handler の分離を説明します。
本書では、前者を「合成の安全性」、後者を「実行契約の差し替え可能性」として使い分けます。

注文処理では、在庫引当を次のように分けます。

```yaml
effects:
  operations:
    - id: ReserveInventory
      input: ReserveInventoryInput
      output: ReserveInventoryResult
      possible_failures:
        - OutOfStock
        - InventoryServiceTimeout
      required_properties:
        - idempotent_by_order_id
        - audited
  handlers:
    - id: ProductionInventoryHandler
      operation: ReserveInventory
      implementation: InventoryService.MCP
      retry_policy: bounded
      timeout_ms: 3000
      audit_sink: OrderAuditLog
    - id: TestInventoryHandler
      operation: ReserveInventory
      implementation: InMemoryFake
      allowed_environments:
        - test
        - local
  effect_safety_notes:
    - "ReserveInventory の本番 handler は timeout と bounded retry を必須にする"
    - "bounded retry の詳細として指数バックオフを使う場合は運用設定で明示する"
    - "TestInventoryHandler を production で使わない"
```

この形にすると、AI に実装を委任するときのレビュー境界が明確になります。
AI は `ReserveInventory` という operation を増やしてよいわけではありません。
Context Pack にある operation と handler の範囲で実装し、retry、timeout、audit、test double の条件を守ります。
本番 handler は MCP や外部サービスに接続してよい一方、test handler は local / test に閉じ込めます。

### effect safety の限界

OCaml 5 は effect handlers を導入し、OCaml manual は computations が effectful operation を実行し、その意味を handler が与える仕組みとして説明しています。
ただし同 manual は、OCaml の effect handlers が static effect safety を提供せず、未処理 effect は `Effect.Unhandled` になることも明記しています。
また、captured continuation は線形に扱う必要があり、再利用や未再開は実行時の問題や resource leak につながります。

Koka は effect types / handlers を備える研究言語として、operation と handler の分離を学ぶ参考になります。
ただし、型や effect annotation があることを「本番運用が必ず安全」と読むのは誤りです。
本書では、型で表現できる境界、Context Pack で固定する契約、CI / review / trace で確認する証跡を分けます。

## 第9章補論: Graded / Linear Resource Types と resource constraints

AI agent の tool 実行では、効果の有無だけでなく、資源の使い方も固定します。
外部 API を何回まで呼べるか、PII をどの tool へ渡せるか、
ワンタイムトークンを複製・ログ出力・再利用しないかは、実装前に契約へ落とします。

この発展的背景として、graded modal types と linear types があります。
Granule は、linear λ-calculus に graded modal types を組み合わせる研究言語として公開されています（[Granule Project](https://granule-project.github.io/granule.html)）。
公式ページでは、資源使用量、セキュリティレベル、副作用などを型で追跡する例が示されています。
ただし本書では、Granule の production 導入を推奨しません。
ここでは、資源制約を Context Pack v2 の `resource_constraints` として表現するための参照に留めます。

実務での対応づけは次のとおりです。

| 観点 | 実務上の制約 | Context Pack v2 |
| --- | --- | --- |
| graded resource | tool call 回数、LLM retry 回数、CI 時間 | `resource_constraints.tool_budget` |
| data sensitivity | PII、本番データ、監査ログの取り扱い | `resource_constraints.data_sensitivity` |
| linear resource | ワンタイムトークン、決済承認 token、冪等性 key | `resource_constraints.linear_resources` |
| runtime enforcement | 実行直前の拒否、redaction、承認要求 | `agent_runtime.guardrails` |

```yaml
resource_constraints:
  tool_budget:
    max_external_api_calls: 3
    max_llm_retries: 2

  data_sensitivity:
    pii:
      allowed_tools:
        - pii_redactor
      forbidden_tools:
        - general_llm_without_redaction

  linear_resources:
    - id: payment_authorization_token
      kind: one_time_token
      rule:
        - must_not_duplicate
        - must_not_log
        - must_not_reuse
    - id: password_reset_token
      kind: one_time_token
      rule:
        - must_not_duplicate
        - must_not_log
        - must_not_reuse
```

### `agent_runtime.guardrails` との分担

`resource_constraints` は、予算・機密度・再利用禁止資源のポリシーです。
一方、`agent_runtime.guardrails` は、tool 実行の前後でそのポリシーを検査する実行時のゲートです。

たとえば `max_external_api_calls: 3` は resource constraint です。
実際に4回目の外部 API 呼び出しを止める処理は guardrail です。
`pii.allowed_tools` は、PII を扱える tool の境界です。
実際に `general_llm_without_redaction` へ渡さない検査は guardrail です。
`payment_authorization_token` を `must_not_log` とするのは linear resource の制約です。
ログ出力前に token を検出して拒否する処理は guardrail です。

AI agent に作業を委任する場合は、`resource_constraints` を「守るべき契約」、
`agent_runtime.guardrails` を「実行時に止める場所」として渡します。
型理論の語彙は、ここでは比喩と対応づけです。
本番の安全性は、Context Pack validation、CI、監査ログ、review で確認します。

## 実装カタログへの接続

効果境界を言語・型システム側から調べる場合は、[付録E: Applied Category Theory 実装カタログ]({{ '/appendices/implementation-catalog/' | relative_url }}) を参照します。

| 候補 | 第9章での使いどころ | 注意点 |
| --- | --- | --- |
| OCaml effects | effect handlers を実用言語の制御抽象として確認する | OCaml の effect handlers は静的 effect safety を提供しないため、未処理 effect は設計・テスト・レビューで補う |
| Koka | effect types / handlers を型システム側から理解する | 研究言語として扱い、production 利用を断定しない |
| Granule | graded / linear resource reasoning を概念整理する | production tool ではなく、resource constraints を設計する参照として使う |

この対応は、Context Pack v2 の `effects` と `resource_constraints` へ戻すためのものです。

## AIエージェントへの引き渡し

効果境界は、AIが勝手に“便利化”しやすい部分です。以下を禁止事項として明確化します。

- 副作用の無断追加（DBアクセス、外部呼び出し、非同期化、リトライ）
- pure core への効果混入（テスト不能化）
- 監査/冪等性の破壊

指示の書き方（抜粋）は次のとおりです。

> pure core / impure shell を維持せよ。pure core にIO/DB/外部APIを追加してはいけない。  
> failures/retry/idempotency/audit を Context Pack の通りに実装せよ。勝手に増減してはいけない。  
> 図式（Diagrams）を満たすテスト観点を出力し、破綻を検知できるようにせよ。

## 検証（テスト観点・可換性チェック）

効果境界のテスト戦略は、層ごとに分離します。

- pure core（単体）:
  - 状態遷移、計算、検証ロジック
  - 図式（Diagrams）由来の性質をプロパティとして検証しやすい
- impure shell（統合）:
  - DB/外部API/監査/再試行
  - 冪等性（D1）や監査整合（D2）を観測点（状態/イベント）で検証する

## 演習

1. 共通例題の `PlaceOrder` を取り上げ、pure core と impure shell を分解する
2. failures/retry/idempotency/audit をテンプレに落とす
3. D1（冪等）/D2（監査整合）を壊さないためのテスト観点を列挙する
4. AIに委任する場合の禁止事項（副作用の無断追加、境界破壊）を Context Pack に追記する
5. Context Pack を更新したら検証する（編集対象に合わせてパスを置き換える）。
   - （初回のみ）`python3 -m pip install -r scripts/requirements-qa.txt`
   - minimal lint を実行する。
     - `python3 scripts/validate-context-pack.py <your-context-pack.yaml>`
     - 例: `docs/examples/common-example/context-pack-v1.yaml`
   - schema validation を実行する。
     - `python3 scripts/validate-context-pack-schema.py <your-context-pack.yaml>`
     - 例: `docs/examples/common-example/context-pack-v1.yaml`
   - （任意）CI相当の一括チェックとして `npm run qa` を実行する。
   - 検証コマンドの SSOT を確認する。
     - [Context Pack v1 仕様（検証コマンド）]({{ '/spec/context-pack-v1/' | relative_url }}#validation-commands)
   - 注記: `docs/examples/common-example/context-pack-v1.yaml` のような repository 内パスは local 検証用の例です。reader-facing な内容確認は公開ページの [共通例題: 注文処理]({{ '/examples/common-example/' | relative_url }}) を正本として参照します。

## まとめ

- 効果（IO/DB/例外/リトライ等）を型と境界に押し上げ、合成と検証を破綻させない
- pure core / impure shell を維持すると、AI委任後も検証可能性が保たれる
- 冪等性・監査・再試行は境界の契約として固定し、図式（Diagrams）とテスト観点へ接続する

### 次章への接続

- 第10章では、ここで分離した判断と副作用を、1つの変更要求の通しケースへ戻す。
