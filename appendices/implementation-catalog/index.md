---
title: "付録E: Applied Category Theory 実装カタログ"
appendix: implementation-catalog
---

# 付録E: Applied Category Theory 実装カタログ

本付録は、Applied Category Theory（ACT）の実装・研究成果を、
本書の設計成果物、Context Pack、レビュー、CI へ接続するためのカタログです。
インストール手順や言語入門ではなく、「どの問題で参照するか」と
「どこで過信してはいけないか」を判断する入口として使います。

確認日: 2026-06-06。
外部ツールの成熟度や公開 URL は変わるため、採用前には公式ページ、論文、
リポジトリの最新状態を確認してください。

## 使い方

1. まず「使いどころ」で、自分の課題が統合、配線、効果、資源、差分のどれかを選ぶ。
2. 「本書での対応章」へ戻り、Context Pack や Diagram に落とす。
3. 「注意点」をレビュー条件へ変換する。
4. 採用する場合は、公式 URL と確認日を Issue / PR に残す。

このカタログは、ツールを推奨順位で並べたものではありません。
本書の章に対応する「再参照地図」です。

## カタログ一覧

<table>
  <thead>
    <tr>
      <th>ツール / 研究</th>
      <th>使いどころ</th>
      <th>本書での対応章</th>
      <th>注意点</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><a href="https://categoricaldata.net/">CQL</a></td>
      <td>DBスキーマ統合、データ移行、lineage、データ品質の保存。</td>
      <td>第4章、第7章、第10章</td>
      <td>汎用分散DBMSとして扱わない。CQL自身も、保存・更新を担うDBMSではないと説明している。</td>
    </tr>
    <tr>
      <td><a href="https://github.com/AlgebraicJulia/Catlab.jl">Catlab.jl</a></td>
      <td>wiring diagram、string diagram、monoidal modeling、圏論的構造の計算。</td>
      <td>第8章、付録E</td>
      <td>proof assistant ではない。Catlab README は、形式的に検証可能な proof を生成しないと明記している。</td>
    </tr>
    <tr>
      <td><a href="https://arxiv.org/abs/2404.04837">GATlab</a></td>
      <td>generalized algebraic theories による machine-readable な語彙・構造定義。</td>
      <td>第8章、付録A、付録E</td>
      <td>論文・研究実装として扱う。Julia / AlgebraicJulia エコシステムとの関係を確認する。</td>
    </tr>
    <tr>
      <td><a href="https://catcolab.org/">CatColab</a></td>
      <td>共同で conceptual model を作り、形式的・相互運用可能な modeling language へ接続する。</td>
      <td>第3章、第8章、付録E</td>
      <td>共同編集・モデル共有では、maturity、権限、データ感度、公開範囲を事前に確認する。</td>
    </tr>
    <tr>
      <td><a href="https://pijul.org/model/">Pijul / patch theory</a></td>
      <td>merge、conflict、patch semantics、pushout 的な共同編集モデルの理解。</td>
      <td>第7章、付録E</td>
      <td>GitHub標準運用とは異なる。GitHub PR にそのまま置き換えるのではなく、差分意味論の参照として使う。</td>
    </tr>
    <tr>
      <td><a href="https://ocaml.org/releases/5.0.0">OCaml effects</a></td>
      <td>実用言語での effect handlers、直接スタイルの制御抽象、効果境界の設計。</td>
      <td>第9章、付録E</td>
      <td>OCaml の effect handlers は静的な effect safety を提供しない。未処理 effect と継続の線形利用に注意する。</td>
    </tr>
    <tr>
      <td><a href="https://koka-lang.github.io/koka/doc/index.html">Koka</a></td>
      <td>effect types / handlers、効果の型付け、handler 設計の研究・学習。</td>
      <td>第9章、付録E</td>
      <td>Koka v3 は研究言語として扱う。production 利用を断定しない。</td>
    </tr>
    <tr>
      <td><a href="https://granule-project.github.io/granule.html">Granule</a></td>
      <td>graded modal types、linear / resource reasoning、PII や one-time token の概念整理。</td>
      <td>第9章、付録E</td>
      <td>概念参照向き。既存プロダクトへ直ちに導入できる production tool と断定しない。</td>
    </tr>
  </tbody>
</table>

## 章別の引き方

### 第7章: 統合・移行・差分

- CQL:
  - schema、mapping、migration、lineage を具体的に考える入口。
  - Context Pack v2 の `data_contracts.schemas`、`mappings`、`migration_verification` に接続する。
- Pijul / patch theory:
  - patch を履歴ではなく意味を持つ変更単位として見る入口。
  - GitHub PR 運用を置き換えるのではなく、conflict resolution と merge invariant を考える補助線にする。

### 第8章: 配線・分業・共同モデリング

- Catlab.jl:
  - wiring diagram / monoidal modeling を、計算可能な構造として試す入口。
  - proof assistant ではないため、検証済み主張にしたい場合は別の証跡が必要。
- GATlab:
  - 語彙・構造・interface を GAT として機械可読化する研究導線。
  - 本書では `formalization_level` と「比喩 / 対応づけ / 検証条件」の分離に接続する。
- CatColab:
  - 複数人でモデルを作り、概念モデルを共有・批評する入口。
  - 共同編集対象に機密データや未公開設計を含める場合は、権限と公開範囲を先に決める。

### 第9章: 効果・handler・資源

- OCaml effects:
  - effect handler を実用言語の制御抽象として確認する入口。
  - 静的 effect safety がないため、未処理 effect はテスト・レビュー・設計規約で補う。
- Koka:
  - effect types と handlers を、型システム側から整理する入口。
  - 本書では `effects.operations` / `handlers` / `effect_safety_notes` の設計に接続する。
- Granule:
  - graded / linear resource reasoning の概念整理に使う。
  - Context Pack v2 の `resource_constraints.linear_resources` と相性がよい。

## カタログ項目を Issue / PR に落とすテンプレート

```yaml
act_catalog_entry:
  name: <tool-or-research-name>
  official_url: <official-or-paper-url>
  confirmed_at: "YYYY-MM-DD"
  source_type: official-site # official-site | repository | paper | release-note
  use_case:
    - <what-problem-it-helps>
  book_chapters:
    - chapter07
  maps_to_context_pack:
    - data_contracts
  not_for:
    - <what-not-to-claim>
  maturity_notes:
    - <research/prototype/production caveat>
  review_questions:
    - <question reviewers must ask>
```

レビューコメントへ落とすときは、次の形にします。

```text
このPRでは <tool-or-research-name> を <use_case> の参照として使っている。
公式URLは <official_url>、確認日は <confirmed_at>。
<not_for> という限界があるため、本文では <unsafe-claim> と断定しない。
Context Pack では <maps_to_context_pack> に対応させ、検証は <review_questions> で確認する。
```

## 採用前チェックリスト

- [ ] 公式 URL または論文 URL を Issue / PR に残した。
- [ ] 確認日を残した。
- [ ] 本書のどの章・どの Context Pack フィールドに接続するかを書いた。
- [ ] 「できること」と「しないこと」を同じ箇所に書いた。
- [ ] 形式証明、production 利用、GitHub 標準運用との互換性を過大評価していない。
- [ ] CI、レビュー、手動確認のどれで検証するかを分けた。

## 関連導線

- 統合・移行の設計: [第7章]({{ '/chapters/chapter07/' | relative_url }})
- 分業と配線: [第8章]({{ '/chapters/chapter08/' | relative_url }})
- 効果境界: [第9章]({{ '/chapters/chapter09/' | relative_url }})
- 実装・研究URL一覧: [付録C: 参考文献]({{ '/appendices/references/' | relative_url }})
- テンプレート化して自案件へ移す: [付録A: 設計成果物テンプレ集]({{ '/appendices/templates/' | relative_url }})
