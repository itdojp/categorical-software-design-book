---
title: "図式・図版スタイル"
description: "図式の表現方式、画像配置、命名規約"
---

# 図式・図版スタイル

## 表現方式（暫定）

- アーキテクチャ/フロー: **Mermaid**（` ```mermaid `）を第一候補とする
- 圏論の可換図式: まずは **テキスト＋最小の図版**（SVG）で表現し、必要に応じて表現方式を拡張する

補足:
- GitHub Pages ではクライアント側で Mermaid をレンダリングする（`assets/js/mermaid-init.js`）。現状は Mermaid `10.9.1` をCDNから読み込み、` ```mermaid ` ブロックを図として表示する。
- dark/light 切替では図のテーマが焼き付くため、テーマ切替時に再レンダリングする（`assets/js/mermaid-init.js`）。
- Mermaid で表現力が不足する可換図式/ストリング図式は、SVG（`assets/images/`）を利用する。

## 画像配置

- 公開サイトで利用する画像: `assets/images/`
- 執筆運用・設計資料（開発者向け）の画像: `docs/assets/images/`

## 命名規約

- 章に紐づく図: `assets/images/chapterNN/<slug>.svg`
  - 例: `assets/images/chapter01/context-pack-overview.svg`
- 共通図（複数章で参照）: `assets/images/shared/<slug>.svg`

## 参照方法（Markdown）

```md
![図: Context Packの全体像](../../assets/images/chapter01/context-pack-overview.svg)
```

## 作図の最小要件

- 1図1メッセージ（図の目的が1文で説明できる）
- 図中ラベルは `docs/style/terminology.md` に従う
- 図の更新時は差分が追える形式（SVG/テキスト）を優先する
