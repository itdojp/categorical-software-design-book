# Changelog

このプロジェクトの注目すべき変更点を記録します。

形式は Keep a Changelog に準拠し、バージョニングは SemVer を採用します。

## [Unreleased]

### Added

- [#114](https://github.com/itdojp/categorical-software-design-book/issues/114) の 2026 Applied Category Theory / Agent Runtime 改訂を要約しました。
  - [#115](https://github.com/itdojp/categorical-software-design-book/issues/115): Context Pack v2 仕様、schema、minimal/common example、v1/v2 validator 自動判定を追加。
  - [#116](https://github.com/itdojp/categorical-software-design-book/issues/116): CQL / Functorial Data Migration と `data_contracts.migration_verification` を第4章・第7章・第10章・共通例題へ接続。
  - [#117](https://github.com/itdojp/categorical-software-design-book/issues/117): Agent Runtime Contract、MCP、guardrails、tracing を追加。
    trace evidence を第1章・第9章・第10章・テンプレート/プロンプトへ反映。
  - [#118](https://github.com/itdojp/categorical-software-design-book/issues/118): Applied Category Theory 実装カタログ付録を追加。
    Catlab / GATlab / CatColab / CQL / Pijul / OCaml effects / Koka / Granule の位置づけを章別に整理。
  - [#119](https://github.com/itdojp/categorical-software-design-book/issues/119): Algebraic Effects / Effect Handlers と Context Pack v2 `effects` を第9章・共通例題・参考文献へ追加。
  - [#120](https://github.com/itdojp/categorical-software-design-book/issues/120): Structured Cospans / Open Systems と `open_systems` を第8章・第7章補足・共通例題へ追加。
  - [#121](https://github.com/itdojp/categorical-software-design-book/issues/121): Optics / Lenses / Categorical Cybernetics と `views.lenses_or_optics` を第5章・第8章・第10章へ追加。
  - [#122](https://github.com/itdojp/categorical-software-design-book/issues/122): Patch Theory / Version Control Semantics と `change_semantics` を第7章・共通例題・クイックリファレンスへ追加。
  - [#123](https://github.com/itdojp/categorical-software-design-book/issues/123): Graded / Linear Resource Types と `resource_constraints` を第9章・共通例題・クイックリファレンスへ追加。
  - [#124](https://github.com/itdojp/categorical-software-design-book/issues/124): 章間整合、Context Pack v1/v2、navigation、参考文献、QA の final check を実施。

### Changed

- [#110](https://github.com/itdojp/categorical-software-design-book/issues/110) に従い、Phase 5 理論・実装接続レビューゲート、関連書分界、Copilot review completion gate を追加しました。

## [1.0.0] - 2026-02-22

### Added

- 書籍サイト（Jekyll）雛形とナビゲーションSSOT（`book-config.json` → `_data/navigation.yml` 自動生成）
- 第1章〜第10章のドラフト（Objects/Morphisms/Diagrams を軸にした章テンプレ構成）
- 付録A（設計成果物テンプレ集）/ 付録B（AIエージェント用プロンプト集）/ 付録C（学習マップ・参考文献）
- Context Pack v1 仕様（`docs/spec/context-pack-v1.md`）
- 共通例題（`docs/examples/common-example/context-pack-v1.yaml`）
- Context Pack v1 の JSON Schema（`docs/spec/context-pack-v1.schema.json`）
- Context Pack v1 の最小 lint（`scripts/validate-context-pack.py`）
- CI品質ゲート（リンク/Unicode/構造/textlint + Context Pack lint）
- GitHub Pages 公開設定（Deploy from branch: `main` / `/`）
- Mermaid 図式のクライアントサイドレンダリング（Pages対応）と主要図式の追加
- フィードバック用Issueテンプレ（誤植/技術的指摘/質問）
