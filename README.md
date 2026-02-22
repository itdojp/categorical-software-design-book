# 圏論によるAIエージェント時代の合成的ソフトウェア設計

仕様・設計・検証を合成可能にする共通言語。

## 公開URL

- https://itdojp.github.io/categorical-software-design-book/

## 対象読者

- AIを用いた実装・テスト生成を運用している（または導入したい）ソフトウェア開発者/テックリード
- 仕様追加や境界破壊を抑止するために、設計成果物（入力契約）と検証条件を固定したい方
- 設計・検証をテンプレ化して、レビュー可能な差分（PR）へ落としたい方

## この本の読み方（推奨）

- まず `index.md` の目次から全体像を把握する
- 第1章で「人間とAIの責任分界」と「設計成果物＝入力契約」を固定する
- 第2〜6章で、Objects/Morphisms/Diagrams と契約の標準形を最小セットで揃える
- 第7〜9章で、統合/分業/効果境界の破綻点を図式と検証へ落とす
- 第10章で、Issue→PR→CI→レビューの運用形へ接続する

## 成果物テンプレ（導線）

- Context Pack v1 仕様: `docs/spec/context-pack-v1.md`
- 共通例題 Context Pack: `docs/examples/common-example/context-pack-v1.yaml`
- 付録A（テンプレ集）: `appendices/templates/index.md`
- 付録B（プロンプト集）: `appendices/prompts/index.md`
- 付録C（学習マップ・参考文献）: `appendices/references/index.md`

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

## 品質チェック（book-formatter）

CIでは `itdojp/book-formatter` のチェッカー（リンク/Unicode/構造/textlint等）を実行します。ローカルで同等のチェックを行う場合は、book-formatter を取得して実行してください（詳細は `.github/workflows/ci.yml` を参照）。
