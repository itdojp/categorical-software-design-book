# 圏論によるAIエージェント時代の合成的ソフトウェア設計

仕様・設計・検証を合成可能にする共通言語。

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
