---
title: "第10章: ケーススタディ（仕様→設計→検証→AI実装）"
chapter: chapter10
---

# 第10章: ケーススタディ（仕様→設計→検証→AI実装）

最終章では、前章までに分解した概念を
1つの変更要求へ戻します。
仕様差分、AI 委任、レビュー、CI が、
どの順序で連鎖するかを通しで追います。

本章の見せ場は、CancelOrder の Context Pack diff と差し戻し表です。
抽象概念が PR 運用でどの観点に変わるかを、最後にまとめて回収します。

## 学習ゴール

- 1つの変更要求が、どの artifact と検証へ波及するかを追跡できる
- Context Pack 差分 → AI 委任 → レビュー → CI の順序を説明できる
- 第1〜9章で導入した概念が、実務ループのどこで効くかを回収できる
- 自案件へ移植するときに固定すべき最小成果物を判断できる

## ケースの起点: 「出荷前の注文取消」を追加する

本章では、注文処理の共通例題に「支払い前の注文は取消できる」という変更要求を入れます。
ただし、取消と同時に監査証跡が残り、必要なら在庫引当が解放されることを必須にします。
返金、出荷後取消、配送事業者との連携はこの章の対象外です。

- Goal:
  - `Draft` または `Placed` の注文を `Cancelled` に遷移できる
  - `CancelOrder` 成功時に監査証跡が残る
  - `Placed` の注文を取り消した場合は在庫引当が解放される
- Non-goal:
  - `Paid` 済み注文の返金フロー
  - 出荷後取消と配送取消
  - BI/分析向けの取消理由集計
- 完了条件:
  - `CancelOrder` の契約、Diagram、Acceptance test が本文内で追える
  - AI 出力をどの根拠で差し戻すかが分かる
  - CI が何を検知し、どこへ戻るかが分かる

この章で示すのは「コードの書き方」ではなく、「どの順序で契約を固定すれば壊れにくいか」です。

## 変更前の契約を読む

最初に見るのはコードではなく契約です。今回の論点は `Order` の状態と、
`PlaceOrder` 以降に発生する副作用です。

```yaml
problem_statement:
  goals:
    - 注文の作成から出荷までの一連の処理を、境界と不変条件で記述できる
    - 監査ログを「後付け」ではなく契約として扱う
  non_goals:
    - 決済事業者・配送事業者の具体実装の詳細化

objects:
  - id: Order
    states: [Draft, Placed, Paid, Shipped, Cancelled]
```

`Cancelled` は既に状態モデルに含まれています。したがって今回は状態追加ではなく、
「その状態へ至る操作」と「守るべき検証」を明示する変更です。

次に、変更が波及する既存操作を確認します。

```yaml
- id: PlaceOrder
  pre:
    - Order.state == Draft
  post:
    - Order.state == Placed
    - InventoryReservation が作成される（または更新される）
    - AuditEvent("PlaceOrder") が記録される

- id: AuthorizePayment
  pre:
    - Order.state == Placed
    - InventoryReservation.status == Reserved
  post:
    - Payment.status == Authorized
    - Order.state == Paid
    - AuditEvent("AuthorizePayment") が記録される
```

`CancelOrder` は `PlaceOrder` 後の在庫引当と、
`AuthorizePayment` 前後の境界に割り込みます。
この位置づけを曖昧にすると、支払い済み取消や監査漏れが混入します。

守るべき不変条件も先に確認します。

```yaml
- id: D2-audit-consistency
  statement: 重要操作（CreateOrder/PlaceOrder/AuthorizePayment/ShipOrder）は必ず監査証跡を残す
- id: D3-state-transition-safety
  statement: 状態遷移は単調であり、禁止遷移（例: Shipped → Paid）は起きない

forbidden_changes:
  - D2-audit-consistency を満たさない実装変更
  - Order の状態モデル（states）を合意なく変更
```

全文は [共通例題: 注文処理]({{ '/examples/common-example/' | relative_url }}) を参照してください。
本文では、読解に必要な断片だけを引き上げます。

## Context Pack をどう変えるか

### 1) Morphism を追加する

最初に固定するのは `CancelOrder` の契約です。
ここが曖昧なまま AI に委任すると、
「汎用ステータス更新 API」や「監査を任意にする実装」が出やすくなります。

```diff
+ - id: CancelOrder
+   input: { orderId: "OrderId", reason: "string" }
+   output: { orderId: "OrderId" }
+   pre:
+     - Order.state in [Draft, Placed]
+   post:
+     - Order.state == Cancelled
+     - InventoryReservation.status == Released または対象が存在しない
+     - AuditEvent("CancelOrder") が記録される
+   failures:
+     - NotFound
+     - InvalidState
```

修正順が「Context Pack → 実装」である理由は明確です。
AI が触ってよい境界と、人間が差し戻す基準を先に固定するためです。

### 2) Diagram と Acceptance test を追加する

`CancelOrder` は操作追加だけでは足りません。
監査と在庫解放が守られるかを、Diagram と受入テストへ落とします。

```diff
- - id: D2-audit-consistency
-   statement: 重要操作（CreateOrder/PlaceOrder/AuthorizePayment/ShipOrder）は必ず監査証跡を残す
+ - id: D2-audit-consistency
+   statement: 重要操作（CreateOrder/PlaceOrder/AuthorizePayment/CancelOrder/ShipOrder）は必ず監査証跡を残す
+
+ - id: D4-cancel-releases-reservation
+   statement: Placed の注文を取消すと、在庫引当は解放され、監査証跡が残る
+   verification:
+     - CancelOrder 成功後、Order.state == Cancelled になる
+     - InventoryReservation.status == Released になる
+     - AuditEvent("CancelOrder") が存在する
```

```diff
+ - id: AT4-cancel-before-payment
+   scenario: Placed の Order を CancelOrder する
+   expected:
+     - Order.state == Cancelled
+     - InventoryReservation.status == Released
+     - AuditEvent("CancelOrder") が存在する
+
+ - id: AT5-cancel-after-payment
+   scenario: Paid の Order を CancelOrder する
+   expected:
+     - InvalidState
```

この章では、例として `D2` を更新し、`D4` と `AT4/AT5` を追加した差分を扱います。
既存契約を壊さず、変更要求の影響範囲だけを増やすのが要点です。実リポジトリの `context-pack-v1.yaml` の現在値そのものではなく、章内で読解に必要な差分を再掲しています。

## AI へ委任する

Context Pack を更新したら、その差分だけを根拠付きで AI に渡します。
詳細な定型は [付録B: AIエージェント用プロンプト集](../../appendices/prompts/) にあります。
この章では最小断片だけを再掲します。

```text
以下の Context Pack 差分を唯一の仕様として、CancelOrder の実装スケルトンを作成せよ。
Forbidden changes を必ず守れ。

出力:
1. 実装構成案
2. CancelOrder に必要なモジュール境界
3. 未確定事項（質問）と、その理由
```

```text
以下の Diagrams（D2, D4）を満たすことを検証するテスト観点を生成せよ。
仕様追加は禁止。Diagrams/Pre/Post/failures を変更してはいけない。

出力形式:
- Diagram id:
  - 観測点:
  - テスト粒度:
  - 代表テストケース:
  - 反例:
```

この時点で AI に期待するのは完成コードではありません。
まず必要なのは、境界の切り方と不足情報の洗い出しです。

- 実装構成案:
  - `CancelOrderService` を追加する
  - `OrderRepository`、`InventoryReservationRepository`、`AuditAppender` を使う
- テスト観点:
  - `D2` と `D4` に紐づく統合テストを提案する
  - `AT4` と `AT5` に対応する成功/失敗ケースを提示する
- 期待する質問:
  - `Paid` の取消を返金付きで扱うか
  - 在庫解放を同期で行うか、非同期に切るか

質問が返ってこない場合は、AI が non-goal を勝手に補完している可能性があります。

## レビューで差し戻す

AI 出力は「それらしく見える」だけでは通しません。
差し戻し理由は、必ず `problem_statement`、`Diagrams`、`forbidden_changes` にひも付けます。

<table>
  <thead>
    <tr>
      <th>AI提案</th>
      <th>差し戻す理由</th>
      <th>根拠</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>UpdateOrderStatus</code> という汎用 API にまとめる</td>
      <td><code>CancelOrder</code> の pre/post が消え、禁止状態遷移が紛れ込む</td>
      <td><code>D3-state-transition-safety</code>、<code>CancelOrder.pre/post</code></td>
    </tr>
    <tr>
      <td>監査失敗時は warning のみで続行する</td>
      <td>監査を任意化すると運用要件を壊す</td>
      <td><code>D2-audit-consistency</code>、<code>forbidden_changes</code></td>
    </tr>
    <tr>
      <td><code>Paid</code> でも取消可能にして返金は後続対応にする</td>
      <td>仕様追加であり、non-goal を越える</td>
      <td><code>problem_statement.non_goals</code></td>
    </tr>
  </tbody>
</table>

レビューの順序も固定します。

1. まず `Context Pack` と Diff を照合する
2. 次に `Diagram id` ごとのテスト観点が出ているかを見る
3. その後に実装詳細へ入る

この順序を守ると、レビューが感想戦になりません。

## CI で何を検知するか

このリポジトリでは、文書 QA と `Context Pack` 検証を CI に組み込んでいます。
通しケースでは、どの失敗をどのゲートが拾うかを分けて理解することが重要です。

- `python3 scripts/validate-context-pack.py docs/examples/common-example/context-pack-v1.yaml`
  - 必須項目不足、ID 重複、最小構造の崩れを検知する
- `python3 scripts/validate-context-pack-schema.py docs/examples/common-example/context-pack-v1.yaml`
  - `Context Pack v1` のスキーマ逸脱を検知する
- `npm run qa`
  - リンク、構造、Unicode、textlint、rendered HTML を含む主要チェックをまとめて実行する
- Diagram / Acceptance test 由来のテスト（別リポジトリで動かす想定の例）

注記: `docs/examples/common-example/context-pack-v1.yaml` のような repository 内パスは local 検証用の例です。reader-facing な内容確認は公開ページの [共通例題: 注文処理]({{ '/examples/common-example/' | relative_url }}) を正本として参照します。
  - 例題アプリ側の CI で、`D2`、`D4`、`AT4`、`AT5` がコード差分で壊れていないかを検知する（この book リポジトリの `.github/workflows/ci.yml` では実行していない）

CI が落ちたときの修正順も、ケーススタディの一部です。

1. 契約とテスト期待が食い違うなら、先に `Context Pack` を見直す
2. `Context Pack` が正しいなら、実装を修正する
3. 文書 QA だけが落ちたなら、本文とリンクを独立に直す

局所的にコードだけ直すと、次の PR で同じ破綻が再発します。

## このケースで前章の概念がどう効くか

<table>
  <thead>
    <tr>
      <th>章</th>
      <th>概念</th>
      <th>このケースで効く箇所</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>第1章</td>
      <td>責任分界と Context Pack</td>
      <td>人間が <code>CancelOrder</code> の契約を固定してから AI に渡す</td>
    </tr>
    <tr>
      <td>第2章</td>
      <td>Objects / Morphisms</td>
      <td><code>Order</code> と <code>InventoryReservation</code> を保ったまま、<code>CancelOrder</code> を明示的な Morphism として追加する</td>
    </tr>
    <tr>
      <td>第3章</td>
      <td>Diagrams</td>
      <td><code>D2</code> と <code>D4</code> をテスト観点へ落とし、監査漏れと在庫解放漏れを検知する</td>
    </tr>
    <tr>
      <td>第4章</td>
      <td>関手</td>
      <td>仕様差分を、境界を壊さず設計と実装へ写像する</td>
    </tr>
    <tr>
      <td>第5章</td>
      <td>自然変換</td>
      <td>差分レビューで「意味保存の変更か」を確認し、汎用 API 化を差し戻す</td>
    </tr>
    <tr>
      <td>第6章</td>
      <td>普遍性</td>
      <td>取消要求を万能 DTO にせず、最小契約として独立した操作に保つ</td>
    </tr>
    <tr>
      <td>第7章</td>
      <td>統合図式</td>
      <td>注文と在庫引当の整合を、統合境界の問題として扱う</td>
    </tr>
    <tr>
      <td>第8章</td>
      <td>分業と配線</td>
      <td>取消、在庫解放、監査追記を別責務として配線し、順序を明示する</td>
    </tr>
    <tr>
      <td>第9章</td>
      <td>効果境界</td>
      <td>状態判定は pure core に置き、監査追記と在庫解放は impure shell に閉じ込める</td>
    </tr>
  </tbody>
</table>

ケーススタディの payoff は、この表をコードレビューの観点へそのまま持ち出せることです。

## 他案件へ移植するポイント

- 変更要求は 1 PR で 1 件に絞る
- 先に確認するのは `problem_statement`、`morphism`、`diagram`、`acceptance test`、`forbidden_changes`
- AI には全文コードではなく、契約差分と non-goal を先に渡す
- レビューコメントは Diagram id か Forbidden change を根拠に書く
- CI が落ちたら「契約 → 実装 → 文書」の順で戻る

この 5 点だけ守れば、対象ドメインが変わっても運用の骨格は再利用できます。

## 演習

### 演習1: 別の変更要求で同じ流れを再現する

1. `RefundOrder` や `PartialShipment` のように、別の変更要求を 1 つ選ぶ
2. `problem_statement` の Goal / Non-goal を書く
3. 追加または更新する `Morphism`、`Diagram`、`Acceptance test` を 1 つずつ決める
4. Context Pack の検証を通す

   ```bash
   python3 -m pip install -r scripts/requirements-qa.txt  # 初回のみ
   python3 scripts/validate-context-pack.py docs/examples/common-example/context-pack-v1.yaml
   python3 scripts/validate-context-pack-schema.py docs/examples/common-example/context-pack-v1.yaml
   npm run qa  # 任意
   ```
   注記: ここで使う `docs/examples/common-example/context-pack-v1.yaml` は local 検証例です。reader-facing な内容確認は公開ページの [共通例題: 注文処理]({{ '/examples/common-example/' | relative_url }}) を正本として参照します。
5. AI へ渡す prompt と、差し戻し条件を 3 行で書く

### 演習2: レビュー観点を PR コメントとして書く

次の 3 つを必ず含むレビューコメントを作成してください。

- どの `Diagram id` を根拠にしているか
- どの `Forbidden change` または `Non-goal` に触れるか
- 直す順序が `Context Pack` 先行である理由

## まとめ

- ケーススタディは、1つの変更要求を artifact の連鎖として追える形にすると価値が出る
- 先に固定するのはコードではなく、`Context Pack` の契約、Diagram、Acceptance test である
- レビューは感想ではなく、`Non-goal`、`Diagram id`、`Forbidden changes` を根拠に行う
- CI が落ちたときは `Context Pack` から戻ると、局所修正で終わりにくい

### 次に使う導線

- 付録Aのテンプレと付録Bのプロンプトを使うと、この章の流れを自案件の PR に移せる。
- 仕様の現在値を引き直したいときは、共通例題と Context Pack v1 仕様へ戻ると差分を再現しやすい。
