---
title: "図式・図版スタイル"
description: "図式の表現方式、画像配置、命名規約"
---

# 図式・図版スタイル

## 表現方式（現状の方針）

- アーキテクチャ/フロー: **Mermaid** を第一候補とする
- 圏論の可換図式: まずは **テキスト＋最小の図版**（SVG）で表現し、必要に応じて表現方式を拡張する

補足:
- Mermaid は progressive enhancement と位置づける。GitHub Pages ではクライアント側で Mermaid をレンダリングする（`assets/js/mermaid-init.js`）。現状は Mermaid `10.9.1` を CDN から読み込み、HTML 内の `.mermaid` 要素を図として表示する。
- dark/light 切替では図のテーマが焼き付くため、テーマ切替時に再レンダリングする（`assets/js/mermaid-init.js`）。
- Mermaid で表現力が不足する可換図式/ストリング図式は、SVG（`assets/images/`）を利用する。
- 重要図（章の中核図、トップページの概念図）は fallback 必須とする。非JS環境や CDN 障害でも最低限読めることを公開品質の要件に含める。

## Mermaid fallback の標準

- 重要図は `<figure class="diagram-with-fallback">` を標準とする
- 通常表示: `.mermaid-live` 内の Mermaid を描画する
- fallback 表示: `.mermaid-fallback` 内の静的 SVG を使う
- fallback は次の条件で読める状態にする
  - JavaScript 無効時
  - Mermaid CDN の読み込み失敗時
  - テキスト抽出や単純 HTML 検査時
- `figcaption` で図の要点を 1〜2 文で説明する
- `alt` には、図だけでも意味が取れる最小限の説明を入れる

## 画像配置

- 公開サイトで利用する画像: `assets/images/`
- 執筆運用・設計資料（開発者向け）の画像: `docs/assets/images/`

## 命名規約

- 章に紐づく図: `assets/images/chapterNN/<slug>.svg`
  - 例: `assets/images/chapter01/context-pack-overview.svg`
- 共通図（複数章で参照）: `assets/images/shared/<slug>.svg`
- fallback SVG も同じ命名規約に従う
  - 例: `assets/images/chapter01/context-pack-loop.svg`
  - 例: `assets/images/shared/context-pack-concept-map.svg`

## 参照方法（HTML / Mermaid fallback）

```html
<figure class="diagram-with-fallback">
  <div class="mermaid-live">
    <div class="mermaid-wrapper">
      <div class="mermaid">
graph TD
  A --> B
      </div>
    </div>
  </div>
  <div class="mermaid-fallback">
    <img src="{{ '/assets/images/chapter01/context-pack-loop.svg' | relative_url }}" alt="図の要約">
  </div>
  <figcaption>図: Mermaid と SVG fallback を併置する。</figcaption>
</figure>
```

## 作図の最小要件

- 1図1メッセージ（図の目的が1文で説明できる）
- 図中ラベルは `docs/style/terminology.md` に従う
- 図の更新時は差分が追える形式（SVG/テキスト）を優先する
- fallback SVG は Mermaid と同じ意味構造を保つ（ノード名/主要な矢印/方向）
