# 圏論によるAIエージェント時代の合成的ソフトウェア設計

仕様・設計・検証を合成可能にする共通言語。

## 関連書と位置づけ

- 本 repo は `categorical-software-design-book` として公開する独立した日本語書籍である。
- `Compositional Software Design for Agentic Systems`（`composable-software-design-book`）は、関連する独立した英語書籍である。
- 両書は問題意識と語彙を一部共有しますが、旧版/新版や単純翻訳の関係ではありません。
- 日本語で AI エージェント時代の設計成果物、Context Pack、GitHub/CI 運用まで追いたい読者には、本書から読むことを推奨する。
- 英語で compositional design / verifiable engineering の全体像を通読したい読者は、関連英語書籍から始めてください。
- 関連英語書籍:
  - 公開サイト: https://itdojp.github.io/composable-software-design-book/
  - リポジトリ: https://github.com/itdojp/composable-software-design-book

## 公開URL

- https://itdojp.github.io/categorical-software-design-book/

## 対象読者

- AIを用いた実装・テスト生成を運用している（または導入したい）ソフトウェア開発者/テックリード
- 仕様追加や境界破壊を抑止するために、設計成果物（入力契約）と検証条件を固定したい方
- 設計・検証をテンプレ化して、レビュー可能な差分（PR）へ落としたい方

## この本の読み方（推奨）

- 読者向け本文の正本は [公開トップページ](https://itdojp.github.io/categorical-software-design-book/) です。README は repository の入口として、参照先の優先順位と開発者向け情報を要約しています。
- まず [公開トップページ](https://itdojp.github.io/categorical-software-design-book/) の目次から全体像を把握する
- 参照先が複数ある場合の優先順位は、公開トップページの `確認したいこと別の正本` 表を参照してください
- 理論・設計の対応を先に掴みたい場合は、概念マップ → 用語集 → [付録D: クイックリファレンス](https://itdojp.github.io/categorical-software-design-book/appendices/desk-reference/) → 第2章 → 第4章の順で引く
- 第1章で「人間とAIの責任分界」と「設計成果物＝入力契約」を固定する
- 第2〜6章で、Objects/Morphisms/Diagrams と契約の標準形を最小セットで揃える
- 第7〜9章で、統合/分業/効果境界の破綻点を図式と検証へ落とす
- 第10章で、Issue→PR→CI→レビューの運用形へ接続する

## 成果物テンプレ（導線）

- Context Pack v1 仕様: [Context Pack v1 仕様](https://itdojp.github.io/categorical-software-design-book/spec/context-pack-v1/)
- 最小例ハブ: [最小例: minimal-example](https://itdojp.github.io/categorical-software-design-book/examples/minimal-example/)
- 共通例題ハブ: [共通例題: 注文処理](https://itdojp.github.io/categorical-software-design-book/examples/common-example/)
- 付録A（テンプレ集）: [付録A](https://itdojp.github.io/categorical-software-design-book/appendices/templates/)
- 付録B（プロンプト集）: [付録B](https://itdojp.github.io/categorical-software-design-book/appendices/prompts/)
- 付録C（参考文献）: [付録C](https://itdojp.github.io/categorical-software-design-book/appendices/references/)
- 付録D（図版・最小確認項目・症状別の戻り先）: [付録D](https://itdojp.github.io/categorical-software-design-book/appendices/desk-reference/)
- まず論点を絞る場合は付録D、詳細なレビュー用チェックリストは付録Aを参照
- 仕様や雛形が食い違う場合は、まず公開トップの `確認したいこと別の正本` 表で確認対象を切り分けてください。形式と必須項目は Context Pack v1 仕様、共通例題は各 example ページ内 YAML と解説、用語は Glossary、版差は CHANGELOG / GitHub 履歴を正とします

## フィードバック

- 誤植/表記ゆれ/質問/技術的指摘は、GitHub Issues のテンプレートを利用してください。
- Issues: https://github.com/itdojp/categorical-software-design-book/issues/new/choose

## ローカル開発（プレビュー/ビルド）

### 前提

- Ruby（Bundlerが利用できること）
- Jekyll（`bundle exec jekyll` で実行）
- Node.js（任意: book-formatter による品質チェックをローカル実行する場合）

### セットアップ

```bash
bundle install
```

### ローカルプレビュー

`_config.yml` は GitHub Pages（Project Pages）向けに `baseurl` を設定しています。ローカルでは `--baseurl ""` で上書きしてプレビューします。

```bash
bundle exec jekyll serve --livereload --baseurl ""
```

### ビルド

```bash
bundle exec jekyll build
```

注記: 目次や章順の SSOT は `book-config.json` です。`_data/navigation.yml` は generator による生成物として扱い、手編集せず `npm run gen:navigation` / `npm run check:navigation` で整合を確認してください。

## 品質チェック（ローカルQA）

CI では `itdojp/book-formatter` のチェッカー、Context Pack 検証、Jekyll の rendered HTML 回帰チェックを実行します。
Mermaid 図は fallback SVG を含めて QA 対象です。ローカルでは `npm run qa` で主要チェックを一括実行できます（`book-formatter/` は自動取得/更新）。

前提は次のとおりです。
- Ruby / Bundler（`bundle exec jekyll build` による rendered HTML チェック用）
- Node.js（CIは Node 20）
- Python 3（CIは Python 3.12）
- Git / Bash
- （推奨）Python仮想環境（venv/conda）

実行は次のとおりです。

```bash
npm run qa
```

出力は次のとおりです。
- `qa-reports/*.json`（contributor 向けの検証出力。reader-facing な正本ではありません）

詳細は `scripts/qa.sh` と `.github/workflows/ci.yml` を参照してください。
