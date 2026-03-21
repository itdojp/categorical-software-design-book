---
title: "付録D: クイックリファレンス"
appendix: desk-reference
---

# 付録D: クイックリファレンス

本付録は、一読後に「どこへ戻れば判断材料を引き直せるか」を素早く確認するための再参照ページです。図版の位置と、典型的な詰まり方ごとの戻り先をまとめます。

## 1. 図版索引

まず図を見直して全体像を掴みたい場合は、この表を起点に戻ってください。

<table>
  <thead>
    <tr>
      <th>図版</th>
      <th>場所</th>
      <th>何を確認するときに使うか</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>概念マップ</td>
      <td><a href="{{ '/' | relative_url }}#概念マップ">トップページ / 概念マップ</a></td>
      <td>本書全体の論点が、仕様・設計・検証・運用でどうつながるかを見直すとき</td>
    </tr>
    <tr>
      <td>Context Pack → AI → 検証ループ</td>
      <td><a href="{{ '/chapters/chapter01/' | relative_url }}">第1章 / 最小ループ</a></td>
      <td>人間が固定すべき入力契約と、AIへ委任する範囲の境界を確認するとき</td>
    </tr>
    <tr>
      <td>Pullback / Pushout の比較図</td>
      <td><a href="{{ '/chapters/chapter07/' | relative_url }}">第7章 / 統合・移行の設計パターン</a></td>
      <td>統合・移行で「どの境界を合わせるか」を見失ったとき</td>
    </tr>
    <tr>
      <td>ストリング図式の配線図</td>
      <td><a href="{{ '/chapters/chapter08/' | relative_url }}">第8章 / モノイダル圏とストリング図式</a></td>
      <td>並列処理・分業・合流点の責務分担を整理したいとき</td>
    </tr>
    <tr>
      <td>effect boundary の分割図</td>
      <td><a href="{{ '/chapters/chapter09/' | relative_url }}">第9章 / 効果境界の設計</a></td>
      <td>副作用・再試行・監査を pure core と分離して考え直したいとき</td>
    </tr>
    <tr>
      <td>Issue → PR → CI の通しフロー</td>
      <td><a href="{{ '/chapters/chapter10/' | relative_url }}">第10章 / ケーススタディ</a></td>
      <td>設計成果物を GitHub 運用へどう接続するかを再確認するとき</td>
    </tr>
  </tbody>
</table>

## 2. 目的別の引き直し方

迷ったら、まず「いま困っているのが仕様・統合・分業・副作用・運用のどれか」を切り分けると、戻る章を選びやすくなります。

- 仕様が曖昧で AI が勝手に補完する: [第1章]({{ '/chapters/chapter01/' | relative_url }}) → [第2章]({{ '/chapters/chapter02/' | relative_url }})
- 差分レビューで意味保存を確認したい: [第5章]({{ '/chapters/chapter05/' | relative_url }}) → [第10章]({{ '/chapters/chapter10/' | relative_url }})
- 統合・移行で境界が壊れる: [第7章]({{ '/chapters/chapter07/' | relative_url }})
- 並列化や責務分担で配線が壊れる: [第8章]({{ '/chapters/chapter08/' | relative_url }})
- 失敗処理・監査・再試行の責務が混ざる: [第9章]({{ '/chapters/chapter09/' | relative_url }})

## 3. 症状から引く戻り先

症状ベースで再参照したい場合は、この表を使って最初の戻り先を決めてください。

<table>
  <thead>
    <tr>
      <th>症状</th>
      <th>最初に戻る場所</th>
      <th>まず見るもの</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>AI が仕様を補完して、意図しない実装差分を出す</td>
      <td><a href="{{ '/chapters/chapter01/' | relative_url }}">第1章</a></td>
      <td>失敗パターン表、Context Pack の最小構成、Forbidden changes</td>
    </tr>
    <tr>
      <td>用語や境界の意味が章ごとにずれて見える</td>
      <td><a href="{{ '/style/terminology/' | relative_url }}">用語ガイド</a></td>
      <td>主要概念（推奨訳語）と Glossary へのリンク</td>
    </tr>
    <tr>
      <td>統合や移行で、どの条件を一致させるべきか判断できない</td>
      <td><a href="{{ '/chapters/chapter07/' | relative_url }}">第7章</a></td>
      <td>Pullback / Pushout の使い分け、統合時の受入条件</td>
    </tr>
    <tr>
      <td>並列処理や分業で、接続点の責務が曖昧になる</td>
      <td><a href="{{ '/chapters/chapter08/' | relative_url }}">第8章</a></td>
      <td>ストリング図式、結合点の責務、配線の検証観点</td>
    </tr>
    <tr>
      <td>副作用・再試行・監査が混ざり、レビュー観点がぶれる</td>
      <td><a href="{{ '/chapters/chapter09/' | relative_url }}">第9章</a></td>
      <td>pure core / impure shell、モナド、失敗境界</td>
    </tr>
    <tr>
      <td>Issue / PR / CI にどう落とすか分からない</td>
      <td><a href="{{ '/chapters/chapter10/' | relative_url }}">第10章</a></td>
      <td>ケーススタディ全体、レビュー手順、CI の検証ポイント</td>
    </tr>
  </tbody>
</table>
