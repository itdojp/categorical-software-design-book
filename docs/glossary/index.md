---
title: "用語集（Glossary）"
description: "本書で用いる主要概念・訳語・固有用語の参照先（SSOT）"
---

# 用語集（Glossary）

章を跨いで参照される用語の正（SSOT）です。表記ゆれ抑制の方針は [用語ガイド]({{ '/style/terminology/' | relative_url }}) を参照してください。

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

| 用語 | 英語/表記 | 定義 |
| --- | --- | --- |
| 設計成果物 | Design Artifacts | Objects/Morphisms/Diagrams を中心に、AIへ引き渡せる形に固定した成果物一式 |
| Context Pack | Context Pack | AIエージェントへ設計成果物を引き渡すための入力契約。仕様は [Context Pack v1 仕様]({{ '/spec/context-pack-v1/' | relative_url }}) を参照 |

