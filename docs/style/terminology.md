---
title: "用語ガイド"
description: "訳語・表記ゆれを抑制するための用語方針"
permalink: /style/terminology/
---

# 用語ガイド

## 基本方針

- 初出では **日本語（英語）** を併記する。例: 関手（Functor）
- 以後は原則として日本語を用いる（必要に応じて英語を括弧書き）
- 章を跨ぐ概念は [用語集（Glossary）]({{ '/glossary/' | relative_url }}) を正とし、章側は参照する
- 略語は初出で展開する。例: SSOT（Single Source of Truth）、DoD（Definition of Done）

## 主要概念（推奨訳語）

<table>
  <thead>
    <tr>
      <th>English</th>
      <th>日本語</th>
      <th>備考</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Object</td>
      <td>対象</td>
      <td>本書ではドメインの「型/状態」を含む</td>
    </tr>
    <tr>
      <td>Morphism</td>
      <td>射</td>
      <td>操作/API/変換、Pre/Post を伴う</td>
    </tr>
    <tr>
      <td>Composition</td>
      <td>合成</td>
      <td>可能な限り可換性（検証）へ落とす</td>
    </tr>
    <tr>
      <td>Identity</td>
      <td>恒等射</td>
      <td><code>id_A</code> / <code>1_A</code> のいずれかに統一（<a href="{{ '/style/notation/' | relative_url }}">記法ガイド</a> 参照）</td>
    </tr>
    <tr>
      <td>Diagram</td>
      <td>図式</td>
      <td>不変条件（可換性）を表現する</td>
    </tr>
    <tr>
      <td>Commutative</td>
      <td>可換</td>
      <td>「同じ結果になる」ことをテスト可能にする</td>
    </tr>
    <tr>
      <td>Functor</td>
      <td>関手</td>
      <td>仕様→設計→実装の写像として扱う</td>
    </tr>
    <tr>
      <td>Natural transformation</td>
      <td>自然変換</td>
      <td>差分・リファクタの意味保存を表す</td>
    </tr>
    <tr>
      <td>Adjunction</td>
      <td>随伴</td>
      <td>仕様と実装の「最良の対応」を表現する</td>
    </tr>
    <tr>
      <td>Universal property</td>
      <td>普遍性</td>
      <td>標準化（契約）・比較の軸にする</td>
    </tr>
    <tr>
      <td>Monad</td>
      <td>モナド</td>
      <td>効果（副作用）境界の設計へ射影する</td>
    </tr>
    <tr>
      <td>Kleisli</td>
      <td>クライスリ</td>
      <td>Kleisli 圏/射の文脈で用いる</td>
    </tr>
  </tbody>
</table>

## 本書固有の用語

- **Design Artifacts（設計成果物）**: Objects/Morphisms/Diagrams を中心に、AIへ引き渡せる形に固定した成果物一式
- **Context Pack**: AIエージェントへの入力契約（[Context Pack v1 仕様]({{ '/spec/context-pack-v1/' | relative_url }})）
