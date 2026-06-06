---
title: "第7章: Pullback/Pushout（統合・移行の設計パターン）"
chapter: chapter07
---

# 第7章: Pullback/Pushout（統合・移行の設計パターン）

統合と移行は、
局所最適の寄せ集めにすると一気に壊れます。
第7章では、共通基準で結合する条件を
Pullback / Pushout として固定します。

本章の見せ場は、Pullback / Pushout の2図と統合点テンプレです。
どこを揃えれば互換性と整合性が保てるかを、本文だけで追えます。

## 学習ゴール

- Pullback（整合のある結合）/ Pushout（共通インターフェースでの接着）の直観を説明できる
- スキーマ統合、サービス統合、認証統合、移行（旧→新）を図式として設計できる
- 図式としての統合条件を、テスト項目（差分/互換）へ変換できる
- 例題（Order/Payment等）で統合点の設計成果物を作れる
- “統合で壊れる”を事前に図式で表現できる

## 圏論コア（定義・直観・ミニ例）

統合（結合・移行）は「2つのものを同時に満たす」「共通部分で貼り合わせる」といった構造を持ちます。本章では、その標準形として Pullback と Pushout の直観を使います。

### Pullback（整合のある結合）

2つの対象 `A`, `B` を、共通の対象 `C` への対応（写像）を揃えたまま結合する構造です。

<figure class="diagram-with-fallback">
  <div class="mermaid-live">
    <div class="mermaid-wrapper">
      <div class="mermaid">
graph TD
  P["P = A ×_C B"] -->|p1| A
  P -->|p2| B
  A -->|f| C
  B -->|g| C
      </div>
    </div>
  </div>
  <div class="mermaid-fallback">
    <img src="{{ '/assets/images/chapter07/pullback.svg' | relative_url }}" alt="Pullback の fallback SVG。P から A と B へ射が出て、A と B はそれぞれ C へ写る。">
  </div>
  <figcaption>図: Pullback。結合対象 P は A と B を同時に満たし、A と B は共通対象 C への整合条件を保ちます。</figcaption>
</figure>

直観は次のとおりです。

`A` と `B` は独立だが、`C` に対応する部分は一致していなければならない。Pullback は「一致条件（整合性）」を保った結合を表現します。

### Pushout（共通インターフェースでの接着）

共通部分 `C` を介して、`A` と `B` を貼り合わせて新しい対象 `P` を作る構造です。

<figure class="diagram-with-fallback">
  <div class="mermaid-live">
    <div class="mermaid-wrapper">
      <div class="mermaid">
graph TD
  C -->|i1| A
  C -->|i2| B
  A -->|j1| P
  B -->|j2| P
      </div>
    </div>
  </div>
  <div class="mermaid-fallback">
    <img src="{{ '/assets/images/chapter07/pushout.svg' | relative_url }}" alt="Pushout の fallback SVG。共通対象 C から A と B へ射があり、A と B は貼り合わせ先 P へ写る。">
  </div>
  <figcaption>図: Pushout。共通対象 C を基準に A と B を貼り合わせ、統合先 P で共通インターフェースを成立させます。</figcaption>
</figure>

直観は次のとおりです。

`C`（共通インターフェース/共通スキーマ/共通認証）を基準に、`A` と `B` を接着する。移行や統合APIの設計で頻出します。
第8章の [境界を持つコンポーネントの合成]({{ '/chapters/chapter08/' | relative_url }}#第8章補論-境界を持つコンポーネントの合成) では、この Pushout の直観を shared boundary / shared interface の設計へ引き継ぎます。

## ソフトウェア設計への射影（どこに効くか）

統合点で壊れる典型は「どこが同一で、どこが差分か」が曖昧なまま接着してしまうことです。Pullback/Pushout を図式として書くことで、統合条件（同値条件/互換条件）を先に固定できます。

代表ケースは次のとおりです。

- スキーマ統合:
  - 旧DBと新DBを共通キー（例: `orderId`）で整合させつつ統合する（Pullback）
- サービス統合:
  - 旧APIと新APIを共通インターフェースで接着し、クライアント互換を保つ（Pushout）
- 認証統合:
  - 複数[IdP]({{ '/glossary/' | relative_url }}#idp) の subject を整合させる
  - 共通の主体（[Principal]({{ '/glossary/' | relative_url }}#principal)）へ写す（Pullback）
- 移行（旧→新）:
  - 旧データと新データが共通の正規形（Canonical）へ写したとき一致する（Pullback）

統合条件は「図式としての可換条件」なので、第3章の手順でテスト項目へ変換できます（差分/互換テスト、リコンシリエーション、契約テスト）。

## 設計成果物（テンプレ：表/図式/チェックリスト）

共通例題（注文処理）では、境界（Order/Payment/Inventory/Shipment/Audit）の統合点が複数あります。統合する場合は、少なくとも次を成果物として固定します。

### 統合点テンプレ（最小）

| 要素 | 内容 |
| --- | --- |
| 対象 | 統合対象（旧/新、A/B） |
| 共通基準 | 共通キー/共通正規形/共通インターフェース（C） |
| 写像 | 旧→C、新→C（またはC→旧/C→新） |
| 図式（統合条件） | 可換条件（同じものとして扱う条件） |
| 検証 | 差分/互換テスト、リコンシリエーション、監査 |

### 図式→テスト項目（差分/互換）への変換

- Pullback（整合結合）:
  - 同じ `C` へ写るはずのものが一致することを検証する（差分ゼロ、許容差の定義）
- Pushout（接着）:
  - 共通インターフェースを通る経路で、旧/新の観測結果が一致することを検証する（互換テスト）

## 第7章補論: スキーマ統合と関手的データ移行

Pullback/Pushout は、API 統合だけでなく DB スキーマ統合にも現れます。旧注文 DB、監査ログ、read model を別々に扱うと、`OrderId`、決済承認、監査 lineage のどれを保存するのかが曖昧になります。ここで CQL（Categorical Query Language）や Functorial Data Migration の考え方を使うと、「どのスキーマを小さな圏として見て、どの写像でデータを移すか」を設計成果物として明示できます。

CQL は、圏論を使って database の querying、combining、migrating、evolving を扱う open-source の言語/IDE として公開されています（[CQL 公式サイト](https://categoricaldata.net/)）。公式 tutorial でも `Typesides`、`Schemas`、`Instances`、`Mappings`、`Delta and Sigma` が導入されており（[CQL Tutorial](https://categoricaldata.net/cql/tutorial.html)）、本書ではその全機能を解説するのではなく、スキーマ統合の設計語彙として必要な部分だけを使います。

対応づけは次のとおりです。

| ソフトウェア設計 | 圏論的対応 |
| --- | --- |
| DBスキーマ | 小さな圏 |
| テーブル / エンティティ | 対象 |
| 外部キー / 関係 | 射 |
| DBインスタンス | `Schema -> Set` の関手 |
| スキーマ変換 | 関手 |
| データ移行 | スキーマ関手から誘導される移行 |
| 統合・集約 | colimit / pushout 的構成 |
| 整合性制約 | 可換図式・等式制約 |
| lineage / provenance | 移行経路の保存情報 |

この対応づけで重要なのは、用語を飾りとして使うことではありません。たとえば、旧スキーマ `LegacyOrderDB` と新しい `OrderReadModel` を統合するとき、共通部分 `OrderId` と `PaymentAuthorization` をどの経路でも同じものとして扱うなら、その同一視は Pushout 的な接着として設計できます。一方、移行後の read model と元データを突き合わせ、同じ `OrderId` へ写る行だけを検証対象にするなら、Pullback 的な整合条件として読めます。

Context Pack v2 では、この対応を `data_contracts` に残します。

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

この例では、`legacy_to_read_model` が「何を保存し、何を保存しないか」を明示します。`AuditEvent.lineage` は、共通例題 v2 の `AuditEventSchema` で定義する追跡キーです。`legacy_internal_status_text` のような旧システム内部の表示用文字列は read model へ持ち込まない一方、`OrderId`、決済承認、監査 lineage は保存対象として扱います。AI に実装や移行スクリプトの案を出させる場合も、ここを勝手に変えさせないことがレビュー境界になります。

### CQL / FDM を使うときの限界

CQL は汎用分散 DBMS ではありません。本書で扱うのは、スキーマ、写像、等式制約、移行検証を設計成果物として明示する用途です。実案件では、CQL の実行環境、対象データ量、既存 DB との接続、運用監視、権限、PII、再実行手順を別途評価します。SQL 実装詳細、DB 製品比較、CQL tutorial の再掲は本章の範囲外です。

また、Pushout 的に統合したからといって、業務上の整合性が自動で証明されるわけではありません。正しさは、`row_count_invariant`、`foreign_key_preservation`、`lineage_trace_check`、`acceptance_query` のような検証条件に落とし、CI、fixture、監査レビューで確認します。圏論語彙は、比喩、対応づけ、検証条件を分けて使います。

### 実装カタログへの接続

統合・移行の実装候補を調べる場合は、[付録E: Applied Category Theory 実装カタログ]({{ '/appendices/implementation-catalog/' | relative_url }}) を参照します。第7章では特に次を確認します。

- CQL:
  - schema、mapping、migration、lineage を具体化する入口。
  - Context Pack v2 の `data_contracts` と `migration_verification` に戻す。
- Pijul / patch theory:
  - merge や conflict を patch semantics として考える入口。
  - GitHub標準運用の置換ではなく、`change_semantics.merge_invariants` を考える補助線として使う。

## AIエージェントへの引き渡し

統合・移行は、AIが局所的に“つなぐ”と破綻しやすい領域です。AIへ委任する場合は、統合条件（図式）と検証項目を先に入力します。

指示の書き方（抜粋）は次のとおりです。

> Pullback/Pushout の統合条件（Diagrams）を満たすように実装/テストを生成せよ。  
> 互換性（旧/新）を破壊する仕様追加は禁止。写像（旧→C、新→C）を勝手に変えてはいけない。  
> 差分/互換テスト項目を Diagram id に紐づけて出力せよ。

## 検証（テスト観点・可換性チェック）

統合の検証は「一致条件を観測可能にする」ことが中心です。

- 差分検証（Diff）:
  - Pullback の一致条件（旧→C と 新→C が一致）を検証する
- 互換検証（[Compatibility]({{ '/glossary/' | relative_url }}#compatibility)）:
  - Pushout の共通インターフェース経由で旧/新が同じ観測結果になることを検証する
- 監査:
  - 統合・移行操作が監査証跡を残す（D2のような図式）

## 演習

1. 統合ケースを1つ選ぶ（例: `Payment` を外部サービスに切り出す/統合する）
2. 共通基準 `C`（正規形または共通インターフェース）を定義する
3. 図式（Pullback/Pushout）の統合条件を Context Pack の Diagrams として記述する
4. Context Pack を更新したら検証する（編集対象に合わせてパスを置き換える）。
   - （初回のみ）`python3 -m pip install -r scripts/requirements-qa.txt`
   - minimal lint を実行する。
     - `python3 scripts/validate-context-pack.py <your-context-pack.yaml>`
     - 例: `docs/examples/common-example/context-pack-v1.yaml`
     - `data_contracts` を使う場合の例: `docs/examples/common-example/context-pack-v2.yaml`
   - schema validation を実行する。
     - `python3 scripts/validate-context-pack-schema.py <your-context-pack.yaml>`
     - 例: `docs/examples/common-example/context-pack-v1.yaml`
     - `data_contracts` を使う場合の例: `docs/examples/common-example/context-pack-v2.yaml`
   - （任意）CI相当の一括チェックとして `npm run qa` を実行する。
   - 検証コマンドの SSOT を確認する。
     - [Context Pack v1 仕様（検証コマンド）]({{ '/spec/context-pack-v1/' | relative_url }}#validation-commands)
     - [Context Pack v2 仕様（検証コマンド）]({{ '/spec/context-pack-v2/' | relative_url }}#validation-commands)
   - reader-facing な正本として共通例題を引き直す場合は、repo path ではなく [共通例題（注文処理）]({{ '/examples/common-example/' | relative_url }}) を参照する。
5. 図式→テスト項目（差分/互換）へ変換し、検証項目リストとして残す

## まとめ

- Pullback は「整合条件を保った結合」、Pushout は「共通基準での接着」として統合を表現できる
- 統合条件を図式（Diagrams）として固定し、差分/互換テストへ変換することで、統合で壊れる要因を先に封じられる

### 次章への接続

- 第8章では、ここで定義した統合点を前提に、分業と合流点の配線を設計する。
