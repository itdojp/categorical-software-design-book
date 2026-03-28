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

- 圏論の記法や訳語に不安がある場合は、[第2章 合成の最小コア（対象・射・合成）]({{ '/chapters/chapter02/' | relative_url }})、[用語集（Glossary）]({{ '/glossary/' | relative_url }}), [付録D: クイックリファレンス]({{ '/appendices/desk-reference/' | relative_url }}) を先に参照する
- Context Pack の仕様だけ先に押さえたい場合は、[第1章 AIエージェント開発の分担モデルと設計成果物]({{ '/chapters/chapter01/' | relative_url }})、[Context Pack v1 仕様]({{ '/spec/context-pack-v1/' | relative_url }}), [最小例: minimal-example]({{ '/examples/minimal-example/' | relative_url }}) から入る
- 通しの運用像を先に確認したい場合は、[第10章 ケーススタディ（仕様→設計→検証→AI実装）]({{ '/chapters/chapter10/' | relative_url }}) を先に読み、必要になった章へ戻る

## 所要時間（目安）

- 通読: 2〜4時間（章末の演習は除く）
- 演習まで実施: 1〜2日（自プロジェクトに適用する場合は追加）

## 読み方ガイド

- 通読ルート（初読者向け）:
  - 第1章から第10章まで順に読み、最後に第10章のケーススタディで全体を回収する
- 理論・設計の対応を先に掴みたい読者向け:
  - [概念マップ](#概念マップ) → [用語集（Glossary）]({{ '/glossary/' | relative_url }}) → [付録D: クイックリファレンス]({{ '/appendices/desk-reference/' | relative_url }}) → [第2章]({{ '/chapters/chapter02/' | relative_url }}) → [第4章]({{ '/chapters/chapter04/' | relative_url }}) の順に引く
- 実務適用ルート（導入担当・テックリード向け）:
  - 第1章 → 第3章 → 第4章 → 第7章 → 第9章 → 第10章の順に読み、自プロジェクトへ当てる
- 辞書的参照ルート（レビュー担当・運用担当向け）:
  - 用語は [用語集（Glossary）]({{ '/glossary/' | relative_url }}), 図版・レビュー前確認項目・症状別導線は [付録D: クイックリファレンス]({{ '/appendices/desk-reference/' | relative_url }})、設計成果物の雛形は [付録A: 設計成果物テンプレ集]({{ '/appendices/templates/' | relative_url }}) を起点に引き直す
  - プロンプトは [付録B: AIエージェント用プロンプト集]({{ '/appendices/prompts/' | relative_url }})、学習マップと参考文献は [付録C: 参考文献]({{ '/appendices/references/' | relative_url }}) を起点に引き直す

### 確認したいこと別の正本

| 確認したいこと | 最初に開くページ | 説明が食い違う場合の正本 |
| --- | --- | --- |
| 正式な読み順・章立て | このトップページの目次 | 公開トップページの目次（`book-config.json` から生成） |
| 形式と必須項目 | [Context Pack v1 仕様]({{ '/spec/context-pack-v1/' | relative_url }}) | 仕様ページ |
| 最小の入力例 | [最小例: minimal-example]({{ '/examples/minimal-example/' | relative_url }}) | 例題ページ内の YAML と解説 |
| 共通例題の通し像 | [共通例題: 注文処理]({{ '/examples/common-example/' | relative_url }}) | 例題ページ内の YAML と解説 |
| 用語・訳語 | [用語集（Glossary）]({{ '/glossary/' | relative_url }}) | 用語集 |
| 図版・戻り先・レビュー前確認 | [付録D: クイックリファレンス]({{ '/appendices/desk-reference/' | relative_url }}) | 付録D |
| 版差・更新履歴 | [CHANGELOG](https://github.com/itdojp/categorical-software-design-book/blob/main/CHANGELOG.md) | CHANGELOG と GitHub 履歴 |

### 付録起点ショートカット

- 設計成果物の雛形が先に欲しい: [付録A: 設計成果物テンプレ集]({{ '/appendices/templates/' | relative_url }}) → 第1章 → 第10章
- AI への入力例やレビュー/実装プロンプトを先に確認したい: [付録B: AIエージェント用プロンプト集]({{ '/appendices/prompts/' | relative_url }}) → 第1章 → 第10章
- 原典や背景文献から確認したい: [付録C: 参考文献]({{ '/appendices/references/' | relative_url }}) → 第2章 / 第4章 / 第9章
- 図版・症状別の戻り先を先に押さえたい: [付録D: クイックリファレンス]({{ '/appendices/desk-reference/' | relative_url }}) → 該当章
  - まずは付録Dの最小確認項目で論点を絞り、詳細なレビュー観点が必要になったら [付録A: 設計成果物テンプレ集]({{ '/appendices/templates/' | relative_url }}) のチェックリストへ進む

<span id="toc"></span>
## 目次（Part構成）

注記: 編集起点の SSOT は `book-config.json` ですが、reader-facing な正本は公開トップページの目次です。左ナビゲーションと前後導線は `book-config.json` から生成されるため、この要約と差分がある場合は公開トップページと sidebar / Prev/Next の生成導線を優先してください。

### Part I: 委任の前提を固定する

- [第1章 AIエージェント開発の分担モデルと設計成果物]({{ '/chapters/chapter01/' | relative_url }})
- [第2章 合成の最小コア（対象・射・合成）]({{ '/chapters/chapter02/' | relative_url }})
- [第3章 図式と可換性（仕様をテスト可能にする）]({{ '/chapters/chapter03/' | relative_url }})

AI に何を渡し、何を渡さないかを固定する入口です。第1章だけでも、責任分界と Context Pack の位置づけを把握できます。

### Part II: 仕様から実装への写像を安定化する

- [第4章 関手（仕様→設計→実装の写像）]({{ '/chapters/chapter04/' | relative_url }})
- [第5章 自然変換（差分・リファクタを意味保存で扱う）]({{ '/chapters/chapter05/' | relative_url }})
- [第6章 普遍性（積・余積）で標準化する契約]({{ '/chapters/chapter06/' | relative_url }})

仕様変更・差分・標準化を、意味保存の観点でどう扱うかを揃える中核部です。

### Part III: 壊れやすい境界を設計する

- [第7章 Pullback/Pushout（統合・移行の設計パターン）]({{ '/chapters/chapter07/' | relative_url }})
- [第8章 モノイダル圏とストリング図式（分業と配線）]({{ '/chapters/chapter08/' | relative_url }})
- [第9章 モナド/クライスリ（効果境界の設計）]({{ '/chapters/chapter09/' | relative_url }})

統合・分業・副作用のように破綻しやすい場所を、図式・配線・境界として設計する章群です。

### Part IV: 通しケースで回収する

- [第10章 ケーススタディ（仕様→設計→検証→AI実装）]({{ '/chapters/chapter10/' | relative_url }})

前章までの概念を、Issue → Context Pack → AI 実装 → レビュー → CI の実務ループへ接続します。

## 共通例題

本書の running example は注文処理です。`Order / Payment / Inventory / Shipment / Audit` を持つ最小の業務系システムを使い、章ごとに境界・契約・不変条件を増やしていきます。

- 主要フロー: `CreateOrder → PlaceOrder → AuthorizePayment → ShipOrder`
- 主要な観測点: `D1`（冪等性）、`D2`（監査整合）、`D3`（状態遷移安全）
- 第10章で回収する論点: 注文取消のような変更要求を入れたときに、Context Pack・図式・テスト・レビュー観点がどう連動するか

- 共通例題ハブ: [共通例題: 注文処理]({{ '/examples/common-example/' | relative_url }})
- 最小例ハブ: [最小例: minimal-example]({{ '/examples/minimal-example/' | relative_url }})

第10章では、この共通例題に変更要求を入れ、設計成果物と検証がどう連動するかを通しで扱います。

## 付録

- [付録A: 設計成果物テンプレ集]({{ '/appendices/templates/' | relative_url }})
- [付録B: AIエージェント用プロンプト集]({{ '/appendices/prompts/' | relative_url }})
- [付録C: 参考文献]({{ '/appendices/references/' | relative_url }})
- [付録D: クイックリファレンス]({{ '/appendices/desk-reference/' | relative_url }})

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

### 安全適用チェック

- 本書の最小例と共通例題は、検証用のリポジトリと検証用の権限境界で試してください。本番プロジェクトへ、そのまま直移植しないでください。
- Context Pack、Forbidden changes、レビュー観点は、利用中のリポジトリ規約と監査要件に合わせて再確認してください。
- 実務適用前に `validate-context-pack*` と `npm run qa` を通し、差分レビューと CI の両方で確認してください。

1. Context Pack v1 仕様を読む: [Context Pack v1 仕様]({{ '/spec/context-pack-v1/' | relative_url }})
2. 最小例（minimal-example）を読む: [最小例: minimal-example]({{ '/examples/minimal-example/' | relative_url }})（例題ページ内の YAML と解説を起点に確認する）
3. 次に共通例題（注文処理）を読む: [共通例題: 注文処理]({{ '/examples/common-example/' | relative_url }})（公開ページ内の入力例・差分・レビュー観点を順に確認する）
4. Context Pack を検証する（minimal lint + schema validation）:
   - 実行前に、公開ページで見ている版と同じ commit / tag を local checkout していることを確認する
   - （初回のみ）`python3 -m pip install -r scripts/requirements-qa.txt`
   - minimal lint（minimal-example）:
     `python3 scripts/validate-context-pack.py docs/examples/minimal-example/context-pack-v1.yaml`
   - minimal lint（common-example）:
     `python3 scripts/validate-context-pack.py docs/examples/common-example/context-pack-v1.yaml`
   - schema validation（minimal-example）:
     `python3 scripts/validate-context-pack-schema.py docs/examples/minimal-example/context-pack-v1.yaml`
   - schema validation（common-example）:
     `python3 scripts/validate-context-pack-schema.py docs/examples/common-example/context-pack-v1.yaml`
   - 検証スクリプト: リポジトリ同梱の `scripts/validate-context-pack.py` と `scripts/validate-context-pack-schema.py` を使う
5. （任意）CI相当の主要チェックを一括実行する: `npm run qa`
   - 実行後は、検証レポートと失敗箇所を確認してから差分レビューへ進む（詳細: [第10章]({{ '/chapters/chapter10/' | relative_url }})）

## 用語集

- 用語・訳語を確認するときは [用語集（Glossary）]({{ '/glossary/' | relative_url }}) を参照します。
- 図版、レビュー前確認項目、症状別の戻り先は [付録D: クイックリファレンス]({{ '/appendices/desk-reference/' | relative_url }}) を起点に確認します。
- 形式や検証コマンドを確認するときは [Context Pack v1 仕様]({{ '/spec/context-pack-v1/' | relative_url }}) と [検証コマンド]({{ '/spec/context-pack-v1/' | relative_url }}#validation-commands) を参照します。

### 付録の使い分け

- 付録A: 設計成果物テンプレートを先に確認したいときに使います。
- 付録B: AI エージェントに渡す入力例やプロンプト例を確認したいときに使います。
- 付録C: 原典や背景文献を確認したいときに使います。
- 付録D: 図版、レビュー前確認項目、症状別の戻り先を短時間で引き直したいときに使います。詳細なレビュー用チェックリストは付録Aを参照してください。

<span id="update-info"></span>
## 利用と更新情報

- 公開版: [GitHub Pages](https://itdojp.github.io/categorical-software-design-book/)
- リポジトリ: [GitHub Repository](https://github.com/itdojp/categorical-software-design-book)
- 変更履歴: [CHANGELOG.md](https://github.com/itdojp/categorical-software-design-book/blob/main/CHANGELOG.md)
- 版差確認: [コミット履歴](https://github.com/itdojp/categorical-software-design-book/commits/main/) / [Pull Requests](https://github.com/itdojp/categorical-software-design-book/pulls)
- フィードバック: [誤植・質問・技術的指摘](https://github.com/itdojp/categorical-software-design-book/issues/new/choose)

### 版差・更新確認の手順

1. まず公開ページ本文と例題ページ内の YAML を確認し、読者向けに現在公開されている内容を把握します。
2. Context Pack や最小例の入力仕様を確認したい場合は、まず [Context Pack v1 仕様]({{ '/spec/context-pack-v1/' | relative_url }}) と [検証コマンド]({{ '/spec/context-pack-v1/' | relative_url }}#validation-commands) を確認し、その後に [付録A]({{ '/appendices/templates/' | relative_url }}) と [付録B]({{ '/appendices/prompts/' | relative_url }}) の雛形・入力例を見直します。
3. 用語や図式の意味を確認したい場合は [用語集（Glossary）]({{ '/glossary/' | relative_url }}) と [付録D]({{ '/appendices/desk-reference/' | relative_url }}) を見直します。
4. 公開本文と開発中の版差を確認したい場合は、[CHANGELOG.md](https://github.com/itdojp/categorical-software-design-book/blob/main/CHANGELOG.md)、[コミット履歴](https://github.com/itdojp/categorical-software-design-book/commits/main/)、[Pull Requests](https://github.com/itdojp/categorical-software-design-book/pulls) を参照します。
5. 誤植、質問、技術的指摘を送りたい場合は [Issue template](https://github.com/itdojp/categorical-software-design-book/issues/new/choose) を使います。
6. 仕様や概念の根拠を厳密に確認したい場合は [付録C]({{ '/appendices/references/' | relative_url }}) と一次資料を参照します。

AI エージェント、CI、Context Pack の運用例は、読者のプロジェクトへそのまま移植することを前提にしていません。実務へ適用する場合は、本書の図式・契約・検証観点を土台にしつつ、利用中のモデル、リポジトリ規約、権限境界、監査要件に合わせて再確認してください。

## ライセンス

本書は CC BY-NC-SA 4.0 で公開されています。商用利用は別途契約が必要です。

---

- **著者:** {{ site.author | default: '株式会社アイティードゥ' }}
- **バージョン:** {{ site.version | default: '' }}
- **最終更新:** {{ site.time | date: "%Y-%m-%d" }}

注記: 上の「最終更新」は公開サイトのビルド日です。公開本文と開発中の版差を確認する場合は、`CHANGELOG.md`、コミット履歴、Pull Requests を参照してください。
