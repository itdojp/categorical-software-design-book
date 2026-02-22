---
title: "付録C: 参考文献"
appendix: references
---

# 付録C: 参考文献

本付録は、本書の範囲外も含めて「次に学ぶ順番」を提示します。網羅ではなく、移植可能な学習ルートを優先します。

## 学習マップ（推奨順）

1. 最小の圏論（本書 第2〜5章）
   - 対象/射/合成、図式と可換性、関手、自然変換
2. 契約設計の標準形（第6章）
   - 積/余積（AND/OR、成功/失敗、エラーvariant）
3. 統合・移行（第7章）
   - Pullback/Pushout を図式として扱い、差分/互換テストへ落とす
4. 並列と分業（第8章）
   - モノidal圏/ストリング図式で配線と合流点を設計する
5. 効果境界（第9章）
   - pure core / impure shell、失敗/リトライ/冪等/監査を境界で管理する
6. 実務適用（第10章）
   - Issue→PR→CI→レビューの運用形へ落とす

## 本書の線引き（扱わない/深追いしないトピック）

本書は「AI委任の設計成果物」に焦点を当てるため、以下は深追いしません（必要に応じて発展学習）。

- 高階圏（2圏、∞圏）や圏の高次構造
- トポス、層、スキーム等の幾何的側面
- 豊穣圏、圏論的論理の詳細（内部言語）
- 厳密な証明中心の展開（実務適用の説明を優先）

## 参考文献（圏論）

- Saunders Mac Lane, *Categories for the Working Mathematician*
- Steve Awodey, *Category Theory*
- Emily Riehl, *Category Theory in Context*
- Bartosz Milewski, *Category Theory for Programmers*（プログラマ向け解説）
- David I. Spivak, *Category Theory for the Sciences*
- Brendan Fong & David I. Spivak, *Seven Sketches in Compositionality*

## 参考文献（FP/型/意味論・周辺）

- Benjamin C. Pierce, *Types and Programming Languages*
- Andrew W. Appel, *Modern Compiler Implementation*（意味保存の観点に有用）
- Paul Hudak ほか, *Haskell* 系入門（モナド/効果の実装直観）

## 参考文献（テスト/検証/形式手法）

- Leslie Lamport, *Specifying Systems*（TLA+）
- Daniel Jackson, *Software Abstractions*（Alloy）
- プロパティベーステスト（QuickCheck/Hypothesis）関連資料

## 章ごとの対応づけ（目安）

| 章 | 次に読む候補 |
| --- | --- |
| 第2〜3章 | Mac Lane / Awodey / Riehl（基礎）、Milewski（直観） |
| 第4〜5章 | Milewski（関手/自然変換の実装直観）、Fong & Spivak（合成的設計） |
| 第6章 | Fong & Spivak（普遍性の応用）、型システム入門（合併型/直積型） |
| 第7章 | Spivak / Fong & Spivak（統合の図式化） |
| 第9章 | FP文献（モナド/効果）、形式手法（不変条件の固定） |
