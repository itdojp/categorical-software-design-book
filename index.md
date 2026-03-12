---
title: "圏論によるAIエージェント時代の合成的ソフトウェア設計"
description: "AI実装委任を壊さないための設計成果物・検証・運用を圏論で整理する"
---

# 圏論によるAIエージェント時代の合成的ソフトウェア設計

AI時代の実装委任は、コード生成の巧拙よりも「何を固定して渡すか」で成否が決まります。仕様の暗黙補完、境界越境、監査漏れが起きる現場では、速度が上がるほど破綻も増えます。本書は、圏論を難解な数学としてではなく、仕様・境界・不変条件を設計成果物へ落とすための共通言語として扱います。AI導入の一般論や圏論入門ではありません。目的は、AI実装委任の運用品質を上げることです。Context Pack と検証条件を SSOT（Single Source of Truth）として固定し、GitHub と CI の運用まで接続する方法を示します。

## はじめに

> **関連書について**
> - 本書は `categorical-software-design-book` として公開する独立した日本語書籍である。
> - `Compositional Software Design for Agentic Systems`（`composable-software-design-book`）は、関連する独立した英語書籍であり、旧版/新版や単純翻訳ではありません。
> - 日本語で AI エージェント時代の設計成果物、Context Pack、GitHub/CI 運用まで追いたい読者には、本書から読むことを推奨する。
> - 英語で compositional design / verifiable engineering の全体像を通読したい読者は、関連英語書籍から始めてください。
> - 関連英語書籍: [公開サイト](https://itdojp.github.io/composable-software-design-book/) / [リポジトリ](https://github.com/itdojp/composable-software-design-book)

AIに実装やテストを委任すると、速度は上がる一方で、仕様の曖昧さ・境界の越境・検証漏れが増えます。本書が扱うのは、この「速くなるほど壊れやすい」状況を、設計成果物と検証の運用で安定化させる方法です。

本書の中心にあるのは、注文処理の共通例題です。第1章から第9章で Objects / Morphisms / Diagrams / 境界設計を揃えます。第10章では、それらを Issue → Context Pack → AI 実装 → レビュー → CI の通しケースとして回収します。

## 本書の約束

- AI へ渡す前に、人間が固定すべき項目を設計成果物として示す
- 仕様・設計・検証を、Objects / Morphisms / Diagrams で接続できるようにする
- 統合・分業・効果境界のような壊れやすい領域を、図式とテスト観点へ落とせるようにする
- GitHub の Issue / PR / CI 運用へ接続できる実務手順まで示す

## 本書が約束しないこと

- 厳密な証明を中心に圏論そのものを学ぶ教科書にはしない
- 特定言語や特定フレームワークの実装テクニック集にはしない
- プロンプト例だけで運用問題を解決する近道は提示しない

## 読了後にできること

- Context Pack（入力契約）を用いて、AIへの委任範囲と責任分界を固定できる
- Objects/Morphisms/Diagrams により、仕様・設計・検証の接続点を成果物として残せる
- 図式（不変条件）をテスト観点へ変換し、CIで破綻を機械検知できる
- 統合/分業/効果境界の“壊れやすい領域”を、図式と検証の単位として扱える

## 想定読者

- AIを用いた実装/テスト生成を運用している（または導入したい）開発者/テックリード
- 仕様追加・境界破壊・検証漏れを、成果物とプロセスで抑止したい方
- GitHub（Issue/PR）とCIで、レビュー可能な差分として運用したい方

## 向かない読者

- 圏論の厳密な定義や証明を主目的として学びたい方
- AI 実装支援を使わず、純粋に特定言語の API 設計だけを学びたい方
- 設計成果物やレビュー運用を導入せず、プロンプト最適化だけで解決したい方

## 前提知識

- 実装経験（言語は問わない）
- Git/GitHubの基本操作（Issue/PR）
- テスト/CIの基本（単体/統合、品質ゲート）

## 前提が足りない場合の補助導線

- 圏論の記法や訳語に不安がある場合は、[第2章 合成の最小コア（対象・射・合成）](chapters/chapter02/)、[用語集（Glossary）](GLOSSARY.md)、[記法ガイド](docs/style/notation.md) を先に参照する
- Context Pack の仕様だけ先に押さえたい場合は、[第1章 AIエージェント開発の分担モデルと設計成果物](chapters/chapter01/)、[Context Pack v1 仕様](docs/spec/context-pack-v1.md)、[最小例: minimal-example](docs/examples/minimal-example/) から入る
- 通しの運用像を先に確認したい場合は、[第10章 ケーススタディ（仕様→設計→検証→AI実装）](chapters/chapter10/) を先に読み、必要になった章へ戻る

## 所要時間（目安）

- 通読: 2〜4時間（章末の演習は除く）
- 演習まで実施: 1〜2日（自プロジェクトに適用する場合は追加）

## 読み方ガイド

- 通読ルート（初読者向け）:
  - 第1章から第10章まで順に読み、最後に第10章のケーススタディで全体を回収する
- 実務適用ルート（導入担当・テックリード向け）:
  - 第1章 → 第3章 → 第4章 → 第7章 → 第9章 → 第10章の順に読み、自プロジェクトへ当てる
- 辞書的参照ルート（レビュー担当・運用担当向け）:
  - 用語は [用語集（Glossary）](GLOSSARY.md)、設計成果物の雛形は [付録A: 設計成果物テンプレ集](appendices/templates/) を起点に引き直す
  - プロンプトは [付録B: AIエージェント用プロンプト集](appendices/prompts/)、学習マップと参考文献は [付録C: 参考文献](appendices/references/) を起点に引き直す

## 目次（Part構成）

### Part I: 委任の前提を固定する

- [第1章 AIエージェント開発の分担モデルと設計成果物](chapters/chapter01/)
- [第2章 合成の最小コア（対象・射・合成）](chapters/chapter02/)
- [第3章 図式と可換性（仕様をテスト可能にする）](chapters/chapter03/)

AI に何を渡し、何を渡さないかを固定する入口です。第1章だけでも、責任分界と Context Pack の位置づけを把握できます。

### Part II: 仕様から実装への写像を安定化する

- [第4章 関手（仕様→設計→実装の写像）](chapters/chapter04/)
- [第5章 自然変換（差分・リファクタを意味保存で扱う）](chapters/chapter05/)
- [第6章 普遍性（積・余積）で標準化する契約](chapters/chapter06/)

仕様変更・差分・標準化を、意味保存の観点でどう扱うかを揃える中核部です。

### Part III: 壊れやすい境界を設計する

- [第7章 Pullback/Pushout（統合・移行の設計パターン）](chapters/chapter07/)
- [第8章 モノイダル圏とストリング図式（分業と配線）](chapters/chapter08/)
- [第9章 モナド/クライスリ（効果境界の設計）](chapters/chapter09/)

統合・分業・副作用のように破綻しやすい場所を、図式・配線・境界として設計する章群です。

### Part IV: 通しケースで回収する

- [第10章 ケーススタディ（仕様→設計→検証→AI実装）](chapters/chapter10/)

前章までの概念を、Issue → Context Pack → AI 実装 → レビュー → CI の実務ループへ接続します。

## 共通例題

本書の running example は注文処理です。`Order / Payment / Inventory / Shipment / Audit` を持つ最小の業務系システムを使い、章ごとに境界・契約・不変条件を増やしていきます。

- 主要フロー: `CreateOrder → PlaceOrder → AuthorizePayment → ShipOrder`
- 主要な観測点: `D1`（冪等性）、`D2`（監査整合）、`D3`（状態遷移安全）
- 第10章で回収する論点: 注文取消のような変更要求を入れたときに、Context Pack・図式・テスト・レビュー観点がどう連動するか

- 共通例題ハブ: [共通例題: 注文処理](docs/examples/common-example/)
- 最小例ハブ: [最小例: minimal-example](docs/examples/minimal-example/)

第10章では、この共通例題に変更要求を入れ、設計成果物と検証がどう連動するかを通しで扱います。

## 付録

- [付録A: 設計成果物テンプレ集](appendices/templates/)
- [付録B: AIエージェント用プロンプト集](appendices/prompts/)
- [付録C: 参考文献](appendices/references/)

## 概念マップ

<figure class="diagram-with-fallback">
  <div class="mermaid-live">
    <div class="mermaid-wrapper">
      <!-- textlint-disable -->
      <div class="mermaid">
graph TD
  PS["Problem statement（Goals/Non-goals）"] --> CP["Context Pack（SSOT）"]
  GL["Glossary"] --> CP
  O["Objects"] --> CP
  M["Morphisms（Pre/Post/failures）"] --> CP
  D["Diagrams（不変条件）"] --> CP
  AT["Acceptance tests"] --> CP
  FC["Forbidden changes"] --> CP

  CP --> AI["AI: 実装/テスト案生成"]
  %% 区切り。
  AI --> PR["PR（差分）"]
  %% 区切り。
  PR --> RV["レビュー（Forbidden changes / Diagrams）"]
  %% 区切り。
  RV --> CI["CI（品質ゲート）"]
      </div>
      <!-- textlint-enable -->
    </div>
  </div>
  <div class="mermaid-fallback">
    <img src="{{ '/assets/images/shared/context-pack-concept-map.svg' | relative_url }}" alt="Context Pack に入力契約が集約され、AI、PR、レビュー、CI へ接続する概念図。">
  </div>
  <figcaption>図: 概念マップ。入力契約となる要素が Context Pack に集約される。そこから AI→PR→レビュー→CI へ接続する流れを示す。</figcaption>
</figure>

## クイックスタート

読み始める前にすぐ試したい場合だけ、この節を使ってください。通読を優先する場合は、第1章から入る方が理解しやすくなります。

1. Context Pack v1 仕様を読む: [Context Pack v1 仕様](docs/spec/context-pack-v1.md)
2. 最小例（minimal-example）を読む: [最小例: minimal-example](docs/examples/minimal-example/)（[raw](https://raw.githubusercontent.com/itdojp/categorical-software-design-book/main/docs/examples/minimal-example/context-pack-v1.yaml)）
3. 次に共通例題（注文処理）を読む: [共通例題: 注文処理](docs/examples/common-example/)（[raw](https://raw.githubusercontent.com/itdojp/categorical-software-design-book/main/docs/examples/common-example/context-pack-v1.yaml)）
4. Context Pack を検証する（minimal lint + schema validation）:
   - （初回のみ）`python3 -m pip install -r scripts/requirements-qa.txt`
   - minimal lint（minimal-example）:
     `python3 scripts/validate-context-pack.py docs/examples/minimal-example/context-pack-v1.yaml`
   - minimal lint（common-example）:
     `python3 scripts/validate-context-pack.py docs/examples/common-example/context-pack-v1.yaml`
   - schema validation（minimal-example）:
     `python3 scripts/validate-context-pack-schema.py docs/examples/minimal-example/context-pack-v1.yaml`
   - schema validation（common-example）:
     `python3 scripts/validate-context-pack-schema.py docs/examples/common-example/context-pack-v1.yaml`
   - 検証スクリプト: [scripts/validate-context-pack.py](https://github.com/itdojp/categorical-software-design-book/blob/main/scripts/validate-context-pack.py), [scripts/validate-context-pack-schema.py](https://github.com/itdojp/categorical-software-design-book/blob/main/scripts/validate-context-pack-schema.py)
5. （任意）CI相当の主要チェックを一括実行する: `npm run qa`
   - ローカル: `qa-reports/*.json` が生成される
   - CI: Artifacts（qa-reports）に同等レポートが保存される（詳細: [第10章](chapters/chapter10/)）

## 用語集

- 用語・訳語の SSOT: [用語集（Glossary）](GLOSSARY.md)（GitHub: [GLOSSARY.md](https://github.com/itdojp/categorical-software-design-book/blob/main/GLOSSARY.md)）
- 用語/記法/図式の統一ルール:
  - [章テンプレート](docs/style/chapter-template.md)
  - [用語ガイド](docs/style/terminology.md)
  - [記法ガイド](docs/style/notation.md)
  - [図式・図版スタイル](docs/style/diagram-style.md)

## ライセンス

本書は CC BY-NC-SA 4.0 で公開されています。商用利用は別途契約が必要です。

---

- **著者:** {{ site.author | default: '株式会社アイティードゥ' }}
- **バージョン:** {{ site.version | default: '' }}
- **最終更新:** {{ site.time | date: "%Y-%m-%d" }}
