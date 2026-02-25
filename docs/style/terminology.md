---
title: "用語ガイド"
description: "訳語・表記ゆれを抑制するための用語方針"
---

# 用語ガイド

## 基本方針

- 初出では **日本語（英語）** を併記する（例: 関手（Functor））
- 以後は原則として日本語を用いる（必要に応じて英語を括弧書き）
- 章を跨ぐ概念は [用語集（Glossary）]({{ '/glossary/' | relative_url }}) を正とし、章側は参照する
- 略語は初出で展開する（例: Context Pack v1）

## 主要概念（推奨訳語）

| English | 日本語 | 備考 |
| --- | --- | --- |
| Object | 対象 | 本書ではドメインの「型/状態」を含む |
| Morphism | 射 | 操作/API/変換、Pre/Post を伴う |
| Composition | 合成 | 可能な限り可換性（検証）へ落とす |
| Identity | 恒等射 | `id_A` / `1_A` のいずれかに統一（`docs/style/notation.md`参照） |
| Diagram | 図式 | 不変条件（可換性）を表現する |
| Commutative | 可換 | 「同じ結果になる」ことをテスト可能にする |
| Functor | 関手 | 仕様→設計→実装の写像として扱う |
| Natural transformation | 自然変換 | 差分・リファクタの意味保存を表す |
| Adjunction | 随伴 | 仕様と実装の「最良の対応」を表現する |
| Universal property | 普遍性 | 標準化（契約）・比較の軸にする |
| Monad | モナド | 効果（副作用）境界の設計へ射影する |
| Kleisli | クライスリ | Kleisli 圏/射の文脈で用いる |

## 本書固有の用語

- **Design Artifacts（設計成果物）**: Objects/Morphisms/Diagrams を中心に、AIへ引き渡せる形に固定した成果物一式
- **Context Pack**: AIエージェントへの入力契約（[Context Pack v1 仕様]({{ '/docs/spec/context-pack-v1/' | relative_url }})）
