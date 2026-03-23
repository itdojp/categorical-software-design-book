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

- まず `index.md` の目次から全体像を把握する
- 理論・設計の対応を先に掴みたい場合は、概念マップ → `GLOSSARY.md` → `appendices/desk-reference/index.md` → 第2章 → 第4章の順で引く
- 第1章で「人間とAIの責任分界」と「設計成果物＝入力契約」を固定する
- 第2〜6章で、Objects/Morphisms/Diagrams と契約の標準形を最小セットで揃える
- 第7〜9章で、統合/分業/効果境界の破綻点を図式と検証へ落とす
- 第10章で、Issue→PR→CI→レビューの運用形へ接続する

## 成果物テンプレ（導線）

- Context Pack v1 仕様: `docs/spec/context-pack-v1.md`
- 共通例題 Context Pack: `docs/examples/common-example/context-pack-v1.yaml`
- 付録A（テンプレ集）: `appendices/templates/index.md`
- 付録B（プロンプト集）: `appendices/prompts/index.md`
- 付録C（参考文献）: `appendices/references/index.md`
- 付録D（図版索引・症状別の戻り先）: `appendices/desk-reference/index.md`

## フィードバック

- 誤植/表記ゆれ/質問/技術的指摘は、Issueテンプレを利用してください（`.github/ISSUE_TEMPLATE/`）。

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
- `qa-reports/*.json`

詳細は `scripts/qa.sh` と `.github/workflows/ci.yml` を参照してください。
