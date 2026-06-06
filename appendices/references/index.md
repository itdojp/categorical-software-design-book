---
title: "付録C: 参考文献"
appendix: references
---

# 付録C: 参考文献

本付録は、本書の範囲外も含めて「次に学ぶ順番」を提示します。網羅ではなく、移植可能な学習ルートを優先します。

役割の切り分け:

- 語義と訳語は [用語集（Glossary）]({{ '/glossary/' | relative_url }}) を正とします。
- Context Pack の形式・必須項目・検証手順は [Context Pack v1 仕様]({{ '/spec/context-pack-v1/' | relative_url }}) を正とします。
- 版差や公開版とのずれを確認するときは `CHANGELOG` と GitHub 履歴を確認します。
- 本付録は、原典・推薦図書・次に読む順番を確認するための補助導線です。
- 説明が食い違う場合は、まず [公開トップページの「確認したいこと別の正本」]({{ '/' | relative_url }}#確認したいこと別の正本) を参照してください。

学習を進める前に、本書の図版・チェックリスト・症状別導線を引き直したい場合は
[付録D: クイックリファレンス](../../appendices/desk-reference/) を参照してください。

## 学習マップ（推奨順）

1. 最小の圏論（本書 第2〜5章）
   - 対象/射/合成、図式と可換性、関手、自然変換
2. 契約設計の標準形（[第6章](../../chapters/chapter06/)）
   - 積/余積（AND/OR、成功/失敗、エラーvariant）
3. 統合・移行（[第7章](../../chapters/chapter07/)）
   - Pullback/Pushout を図式として扱い、差分/互換テストへ落とす
4. 並列と分業（[第8章](../../chapters/chapter08/)）
   - モノイダル圏/ストリング図式で配線と合流点を設計する
5. 効果境界（[第9章](../../chapters/chapter09/)）
   - pure core / impure shell、失敗/リトライ/冪等/監査を境界で管理する
6. 実務適用（[第10章](../../chapters/chapter10/)）
   - Issue→PR→CI→レビューの運用形へ落とす

## 本書の線引き（扱わない/深追いしないトピック）

本書は「AI委任の設計成果物」に焦点を当てるため、以下は深追いしません（必要に応じて発展学習）。

- 高階圏（2圏、∞圏）や圏の高次構造
- トポス、層、スキーム等の幾何的側面
- 豊穣圏、圏論的論理の詳細（内部言語）
- 厳密な証明中心の展開（実務適用の説明を優先）

## 参考文献（圏論）

- Saunders Mac Lane, *Categories for the Working Mathematician*
- Steve Awodey, *Category Theory*
- Emily Riehl, *Category Theory in Context*
- Bartosz Milewski, *Category Theory for Programmers*（プログラマ向け解説）
- David I. Spivak, *Category Theory for the Sciences*
- Brendan Fong & David I. Spivak, *Seven Sketches in Compositionality*

## 参考文献（データ統合 / Functorial Data Migration）

- Categorical Data, “CQL Categorical Databases”, <https://categoricaldata.net/>
  - CQL の公式サイト。database の querying、combining、migrating、evolving を圏論で扱う open-source 言語/IDE としての位置づけを確認する。
- Categorical Data, “CQL Tutorial”, <https://categoricaldata.net/cql/tutorial.html>
  - `Typesides`、`Schemas`、`Instances`、`Mappings`、`Delta and Sigma` の導入を確認する。
- David I. Spivak, “Functorial Data Migration”, *Information and Computation*, 2013, <https://www.sciencedirect.com/science/article/pii/S0890540112001010>
  - Categorical Data の papers page から参照されている Functorial Data Migration の論文。データ移行をスキーマ写像から導く考え方の背景として読む。
- Categorical Data, “Papers”, <https://categoricaldata.net/papers.html>
  - CQL、Functorial Data Migration、Algebraic Data Integration などの一次導線を確認する。

## 参考文献（Applied Category Theory 実装・研究カタログ）

- AlgebraicJulia, “Catlab.jl”, <https://github.com/AlgebraicJulia/Catlab.jl>
  - Juliaで実装された applied / computational category theory のフレームワーク。wiring diagram や monoidal modeling の参照導線として使う。README では、Catlab は theorem prover / proof assistant ではないと明記されている。
- Owen Lynch, Kris Brown, James Fairbanks, Evan Patterson, “GATlab: Modeling and Programming with Generalized Algebraic Theories”, <https://arxiv.org/abs/2404.04837>
  - generalized algebraic theories による algebraic specification のDSL。語彙や構造定義を machine-readable にする研究導線として使う。
- CatColab, <https://catcolab.org/>
  - collaborative conceptual modeling の実装導線。公式サイトの補足として Topos Institute の CatColab 解説 <https://topos.institute/work/catcolab/> も確認する。
- Pijul, “Model”, <https://pijul.org/model/>
  - patch theory、pushout、conflict を、分散バージョン管理の mental model として確認する導線。
- OCaml, “OCaml 5.0.0 Release Notes”, <https://ocaml.org/releases/5.0.0>
  - OCaml 5 で導入された effect handlers の公式リリース導線。
- OCaml Manual, “Language extensions / Effect handlers”, <https://ocaml.org/manual/5.3/effects.html>
  - OCaml effect handlers の使用上の制約、未処理 effect、線形継続の注意点を確認する。
- Koka, “The Koka Programming Language”, <https://koka-lang.github.io/koka/doc/index.html>
  - effect types / handlers を備える研究言語としての公式導線。production 利用の断定を避ける。
- Granule Project, “The Granule Language”, <https://granule-project.github.io/granule.html>
  - graded modal types、linear λ-calculus、resource reasoning の概念参照として使う。

## 参考文献（Agent Runtime / MCP / Guardrails / Tracing）

- Model Context Protocol, “Specification 2025-11-25”, <https://modelcontextprotocol.io/specification/2025-11-25>
  - MCP を外部 tool / data source へ接続する protocol として確認する一次導線。本書では詳細仕様の再掲ではなく、tool contract とレビュー境界へ落とす。
- OpenAI, “OpenAI Agents SDK”, <https://openai.github.io/openai-agents-python/>
  - agents、handoffs、guardrails、tracing などを備えた実行基盤の例。特定実装に閉じず、Agent Runtime Contract の検証点を考えるための参照として使う。
- OpenAI, “Guardrails”, <https://openai.github.io/openai-agents-python/guardrails/>
  - input / output の検証点として guardrail を扱う参考導線。
- OpenAI, “Tracing”, <https://openai.github.io/openai-agents-python/tracing/>
  - tool call、handoff、guardrail result を後から確認する trace evidence の参考導線。
- GitHub Docs, “GitHub Copilot features”, <https://docs.github.com/en/copilot/get-started/features>
  - Copilot coding agent、code review、MCP servers など、GitHub上のAI支援機能を確認する導線。
- OpenAI, “Codex”, <https://openai.com/codex/>
  - GitHub / CLI / cloud 環境でタスクを委任するエージェント実行基盤の例として参照する。

## 参考文献（FP/型/意味論・周辺）

- Benjamin C. Pierce, *Types and Programming Languages*
- Andrew W. Appel, *Modern Compiler Implementation*（意味保存の観点に有用）
- Paul Hudak ほか, *Haskell* 系入門（モナド/効果の実装直観）

## 参考文献（テスト/検証/形式手法）

- Leslie Lamport, *Specifying Systems*（TLA+）
- Daniel Jackson, *Software Abstractions*（Alloy）
- プロパティベーステスト（QuickCheck/Hypothesis）関連資料

## 章ごとの対応づけ（目安）

| 章 | 次に読む候補 |
| --- | --- |
| 第2〜3章 | Mac Lane / Awodey / Riehl（基礎）、Milewski（直観） |
| 第4〜5章 | Milewski（関手/自然変換の実装直観）、Fong & Spivak（合成的設計） |
| 第6章 | Fong & Spivak（普遍性の応用）、型システム入門（合併型/直積型） |
| 第7章 | Spivak / Fong & Spivak（統合の図式化）、CQL / Functorial Data Migration（スキーマ統合・データ移行）、Pijul / patch theory（差分意味論） |
| 第8章 | Fong & Spivak（モノイダル圏/ストリング図式の直観）、Catlab / GATlab / CatColab、実務の並列/合流設計資料 |
| 第9章 | FP文献（モナド/効果）、OCaml effects / Koka / Granule、MCP / Agents SDK（tool call と guardrail / tracing の実行境界）、形式手法（不変条件の固定） |
| 第10章 | GitHub Actions / GitHub Copilot features / Agent Runtime Contract / テスト戦略 / レビュー運用の実務資料（再現可能性を優先） |
