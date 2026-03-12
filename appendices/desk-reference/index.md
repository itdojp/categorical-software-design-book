---
title: "付録D: クイックリファレンス"
appendix: desk-reference
---

# 付録D: クイックリファレンス

本付録は、一読後に「どこへ戻ればよいか」を机上で引き直すための再参照ページです。
用語の定義は [用語集（Glossary）](../../GLOSSARY.md) を正とし、
本付録では図版・チェックリスト・症状別導線をまとめます。

## 1. 図版索引

| 図版 | 場所 | 何を確認するときに使うか |
| --- | --- | --- |
| 概念マップ | [トップページ](../../index.md#概念マップ) | Context Pack から AI / PR / レビュー / CI までの全体像を引き直す |
| 図2-1 | [第2章](../../chapters/chapter02/) | Objects / Morphisms / 合成の最小読解を確認する |
| 図3-1 | [第3章](../../chapters/chapter03/) | 図式を verification とテスト観点へ変換するときの読み方を確認する |
| 図4-1 | [第4章](../../chapters/chapter04/) | Spec → Code の写像で何を保存すべきかを確認する |
| 図6-1 | [第6章](../../chapters/chapter06/) | 積と余積を契約のどこへ使い分けるかを確認する |
| Pullback / Pushout 図 | [第7章](../../chapters/chapter07/) | 統合条件と移行条件をどの共通基準で固定するかを確認する |
| 図8-1 | [第8章](../../chapters/chapter08/) | 並列作業の合流点と Merge gate を確認する |
| 図9-1 | [第9章](../../chapters/chapter09/) | pure core / impure shell の境界を確認する |

## 2. 作業局面ごとのチェックリスト

### Context Pack を更新する前

- Goal / Non-goal を 1 PR で 1 変更要求に絞る
- Objects / Morphisms / Diagrams / Acceptance tests / Forbidden changes の欠落がないか確認する
- 詳細な記法は [付録A: 設計成果物テンプレ集](../../appendices/templates/) を参照する

### AI へ委任する前

- AI に渡す差分が Context Pack の変更箇所だけに閉じているか確認する
- 仕様追加禁止と Forbidden changes を先頭で明記する
- 出力に根拠（Morphism id / Diagram id）を要求する
- 定型文は [付録B: AIエージェント用プロンプト集](../../appendices/prompts/) を参照する

### PR レビュー前

- 変更が Diagram / Pre / Post / failures を暗黙に変えていないか確認する
- 境界変更がある場合は、第4章・第7章の観点で意図的な変更かを確認する
- 互換性の説明が必要な差分は、第5章の Before / After テンプレで説明できるか確認する

### CI が落ちたとき

- 契約の齟齬なら、第1章・第3章・第10章へ戻り、Context Pack と期待結果を照合する
- 並列作業の衝突なら、第8章の Merge gate を見直す
- 効果や副作用の混線なら、第9章の pure core / impure shell へ戻る

## 3. 症状から引く戻り先

| 症状 | 最初に戻る場所 | まず見るもの |
| --- | --- | --- |
| AI が仕様を勝手に広げる | [第1章](../../chapters/chapter01/) / [第4章](../../chapters/chapter04/) | Context Pack、Forbidden changes、境界の対応 |
| テスト観点が曖昧でレビューが感想になる | [第3章](../../chapters/chapter03/) | Diagram、verification、観測点表 |
| 差分が安全な変更か説明できない | [第5章](../../chapters/chapter05/) | Before / After、可換チェック、Approval |
| DTO が肥大化し optional だらけになる | [第6章](../../chapters/chapter06/) | Product / Union、入力束、failure variant |
| 統合や移行で互換性が崩れる | [第7章](../../chapters/chapter07/) | Pullback / Pushout、Compatibility、Principal |
| 並列作業の合流で衝突が増える | [第8章](../../chapters/chapter08/) | ストリング図式、Merge gate、合流順序 |
| 副作用が増え、監査や再試行が読めなくなる | [第9章](../../chapters/chapter09/) | pure core / impure shell、失敗モデル、監査観測点 |
| 変更要求を end-to-end で再現できない | [第10章](../../chapters/chapter10/) | Context Pack diff、差し戻し表、CI の戻り順 |

## 4. 参照ハブ

- 用語を引き直す: [用語集（Glossary）](../../GLOSSARY.md)
- 設計成果物の書き方を引き直す: [付録A: 設計成果物テンプレ集](../../appendices/templates/)
- AI への渡し方を引き直す: [付録B: AIエージェント用プロンプト集](../../appendices/prompts/)
- 次に学ぶ文献へ進む: [付録C: 参考文献](../../appendices/references/)
