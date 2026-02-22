# Changelog

このプロジェクトの注目すべき変更点を記録します。

形式は Keep a Changelog に準拠し、バージョニングは SemVer を採用します。

## [Unreleased]

## [1.0.0] - 2026-02-22

### Added

- 書籍サイト（Jekyll）雛形とナビゲーションSSOT（`book-config.json` → `_data/navigation.yml` 自動生成）
- 第1章〜第10章のドラフト（Objects/Morphisms/Diagrams を軸にした章テンプレ構成）
- 付録A（設計成果物テンプレ集）/ 付録B（AIエージェント用プロンプト集）/ 付録C（学習マップ・参考文献）
- Context Pack v1 仕様（`docs/spec/context-pack-v1.md`）と共通例題（`docs/examples/common-example/context-pack-v1.yaml`）
- Context Pack v1 のJSON Schema（`docs/spec/context-pack-v1.schema.json`）と最小lint（`scripts/validate-context-pack.py`）
- CI品質ゲート（リンク/Unicode/構造/textlint + Context Pack lint）
- GitHub Pages 公開設定（Deploy from branch: `main` / `/`）
- Mermaid 図式のクライアントサイドレンダリング（Pages対応）と主要図式の追加
- フィードバック用Issueテンプレ（誤植/技術的指摘/質問）

