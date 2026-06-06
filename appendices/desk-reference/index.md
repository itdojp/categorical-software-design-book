---
title: "付録D: クイックリファレンス"
appendix: desk-reference
---

# 付録D: クイックリファレンス

本付録は、一読後に「どこへ戻れば判断材料を引き直せるか」を素早く確認するための再参照ページです。図版の位置と、典型的な詰まり方ごとの戻り先をまとめます。

本書では、この付録を図版索引・レビュー前の最小確認項目・症状別の再参照導線をまとめた統合入口として扱います。図版から戻りたい場合、レビュー前の確認項目を引き直したい場合、症状から戻りたい場合は、まず本付録を起点にしてください。

本文や付録間で説明が食い違う場合は、本付録だけで判断せず、まず [公開トップページの「確認したいこと別の正本」]({{ '/' | relative_url }}#確認したいこと別の正本) を参照してください。形式と必須項目は [Context Pack v1 仕様]({{ '/spec/context-pack-v1/' | relative_url }})、実行手順は [検証コマンド]({{ '/spec/context-pack-v1/' | relative_url }}#validation-commands)、語義は [用語集（Glossary）]({{ '/glossary/' | relative_url }})、版差は [CHANGELOG](https://github.com/itdojp/categorical-software-design-book/blob/main/CHANGELOG.md) を確認します。

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

## 2. レビュー前の最小確認項目

設計成果物や PR を確認する前に、最低限次の項目を見直してください。

詳細なレビュー用チェックリストや成果物テンプレートが必要な場合は、[付録A: 設計成果物テンプレ集](../../appendices/templates/) に戻ってください。本節は「まずどこを見るか」を絞るための最小入口です。

- Context Pack に goals / non-goals、境界、Forbidden changes が明記されている
- merge / refactor を含む PR では、Context Pack v2 の `change_semantics` を確認する
- `change_semantics` では、許可する refactor、禁止する conflict 解決、merge invariant が分かれている
- 用語や訳語が [用語集（Glossary）]({{ '/glossary/' | relative_url }}) と衝突していない
- 図式や不変条件が、対応するテスト観点へ落ちている
- 効果境界や副作用が pure core / impure shell の切り分けと矛盾していない
- 理論概念から実務成果物への対応について、保存したい構造、保存しないこと、検証方法が同じレビュー単位で説明されている
- 関連英語書籍 `composable-software-design-book` と旧版/新版・単純翻訳の関係として扱わず、本書の Context Pack / GitHub / CI 運用上の責務が明確である
- Issue / PR / CI のどこで確認するかが、第10章のケーススタディと整合している

## 3. merge conflict を Pushout で見る最小メモ

差分レビューや conflict 解決で判断に迷ったら、次の対応を使います。
[第7章の補論]({{ '/chapters/chapter07/' | relative_url }}#第7章補論-merge-conflict-を-pushout-で見る) に戻ります。

| 観点 | 見るもの |
| --- | --- |
| 共通祖先 | `A`: merge base、合意済み Context Pack、既存テスト |
| 片側の変更 | `f: A -> B`: 人間または AI agent の branch 差分 |
| もう片側の変更 | `g: A -> C`: main 側、または並行 PR の差分 |
| merge 候補 | `D`: 両方の変更を含む候補。`Forbidden changes` と `merge_invariants` を満たす場合だけ採用する |

最小チェック。

- `allowed_refactors`: 意味保存として扱う変更だけを許可する。
  - 例: `rename_private_method_without_behavior_change`、`extract_pure_function`
- `forbidden_conflict_resolutions`: 危険な conflict 解決を禁止する。
  - 例: `delete_failing_test`
  - 例: `remove_audit_log_to_resolve_type_error`
  - 例: `weaken_authorization_check`
- `merge_invariants`: merge 後に守る不変条件を確認する。
  - 例: `all_acceptance_tests_preserved`
  - 例: `diagram_commutativity_preserved`
  - 例: `context_pack_fields_not_silently_removed`

ここでの Pushout は、GitHub 標準運用の置換ではありません。
実務上は PR、CI、review thread、Context Pack validation の証跡で採否を判断します。

## 4. resource constraints の最小メモ

AI agent の tool 実行で予算や機密情報を扱う場合は、[第9章]({{ '/chapters/chapter09/' | relative_url }}) と Context Pack v2 の `resource_constraints` に戻ります。

| 観点 | Context Pack v2 | まず確認すること |
| --- | --- | --- |
| tool budget | `tool_budget.max_external_api_calls` / `max_llm_retries` | API 呼び出し回数と retry 回数が上限を超えない |
| PII | `data_sensitivity.pii.allowed_tools` / `forbidden_tools` | PII は `pii_redactor` など許可 tool だけへ渡す |
| one-time token | `linear_resources` | `payment_authorization_token` や `password_reset_token` を複製・ログ出力・再利用しない |
| 実行時検査 | `agent_runtime.guardrails` | resource constraint を超える tool call を実行前に拒否する |

最小チェック。

- `max_external_api_calls` と `max_llm_retries` が明示されている。
- PII の `allowed_tools` と `forbidden_tools` が分かれている。
- one-time token に `must_not_duplicate`、`must_not_log`、`must_not_reuse` がある。
- `agent_runtime.guardrails` が予算超過、PII 未 redaction、token logging を止める。

Graded / linear の語彙は、ここでは資源制約を考える補助線です。
実務上は Context Pack validation、CI、監査ログ、review で確認します。

## 5. 目的別の引き直し方

迷ったら、まず「いま困っているのが仕様・統合・分業・副作用・運用のどれか」を切り分けると、戻る章を選びやすくなります。

- 仕様が曖昧で AI が勝手に補完する: [第1章]({{ '/chapters/chapter01/' | relative_url }}) → [第2章]({{ '/chapters/chapter02/' | relative_url }})
- 差分レビューで意味保存を確認したい: [第5章]({{ '/chapters/chapter05/' | relative_url }}) → [第10章]({{ '/chapters/chapter10/' | relative_url }})
- 統合・移行で境界が壊れる: [第7章]({{ '/chapters/chapter07/' | relative_url }})
- merge / refactor で意味保存が不安定になる: [第7章補論]({{ '/chapters/chapter07/' | relative_url }})
- 並列化や責務分担で配線が壊れる: [第8章]({{ '/chapters/chapter08/' | relative_url }})
- 失敗処理・監査・再試行の責務が混ざる: [第9章]({{ '/chapters/chapter09/' | relative_url }})
- tool budget / PII / one-time token の扱いが曖昧になる: [第9章]({{ '/chapters/chapter09/' | relative_url }})
- 設計成果物のテンプレートを先に見たい: [付録A: 設計成果物テンプレ集]({{ '/appendices/templates/' | relative_url }})
- AIレビュー・実装プロンプトを先に見たい: [付録B: AIエージェント用プロンプト集]({{ '/appendices/prompts/' | relative_url }})
- 次に学ぶ順番や原典を確認したい: [付録C: 参考文献]({{ '/appendices/references/' | relative_url }})
- ACTの実装・研究候補を章別に引きたい: [付録E: Applied Category Theory 実装カタログ]({{ '/appendices/implementation-catalog/' | relative_url }})

## 6. 症状から引く戻り先

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
      <td><a href="{{ '/glossary/' | relative_url }}">用語集（Glossary）</a></td>
      <td>主要概念の意味を確認し、表記ルールが必要なら用語ガイドへ進む</td>
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
      <td>tool budget、PII、ワンタイム token の扱いが曖昧になる</td>
      <td><a href="{{ '/chapters/chapter09/' | relative_url }}">第9章</a></td>
      <td>resource constraints、guardrails、linear resources</td>
    </tr>
    <tr>
      <td>ACTのツールや研究成果を、どの章の設計課題へ戻すべきか迷う</td>
      <td><a href="{{ '/appendices/implementation-catalog/' | relative_url }}">付録E</a></td>
      <td>CQL、Catlab、GATlab、CatColab、Pijul、OCaml effects、Koka、Granule の使いどころと注意点</td>
    </tr>
    <tr>
      <td>Issue / PR / CI にどう落とすか分からない</td>
      <td><a href="{{ '/chapters/chapter10/' | relative_url }}">第10章</a></td>
      <td>ケーススタディ全体、レビュー手順、CI の検証ポイント</td>
    </tr>
    <tr>
      <td>公開ページの説明と公開版 YAML / GitHub の変更履歴が一致しないように見える</td>
      <td><a href="{{ '/' | relative_url }}#update-info">トップページ / 利用と更新情報</a></td>
      <td><a href="https://github.com/itdojp/categorical-software-design-book/blob/main/CHANGELOG.md">CHANGELOG</a>、コミット履歴、公開ページ本文との版差確認手順</td>
    </tr>
  </tbody>
</table>
