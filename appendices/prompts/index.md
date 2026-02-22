---
title: "付録B: AIエージェント用プロンプト集"
appendix: prompts
---

# 付録B: AIエージェント用プロンプト集

本書の章末演習で、そのまま利用できるプロンプト例です。前提として、AIに渡す入力契約は Context Pack v1（`docs/spec/context-pack-v1.md`）を想定します。

## 共通ルール（先頭に付ける）

```text
あなたは実装/テスト/レビュー支援のAIである。

禁止事項:
- 仕様追加（Goals/Non-goals の外）をしない
- Context Pack の契約（Objects/Morphisms/Diagrams/Pre/Post/failures/Forbidden changes）を変更しない
- 不足情報を勝手に補完しない（質問する）

出力要件:
- 参照した Context Pack の要素（Morphism id / Diagram id 等）を明記して追跡可能にする
- 重要な判断は根拠（どの契約に基づくか）を示す
```

## 実装

### 1) Context Pack投入（実装スケルトン生成）

```text
以下の Context Pack を唯一の仕様として、実装スケルトンを作成せよ。
Forbidden changes を必ず守れ。

出力:
1. 実装構成案（モジュール境界、責務、依存）
2. Morphismごとの実装単位（関数/API/ジョブ）の一覧
3. 未確定事項（質問）と、回答がないと実装できない理由

Context Pack:
<PASTE_CONTEXT_PACK_HERE>
```

## テスト

### 2) 図式→テスト生成（Diagrams起点）

```text
以下の Diagrams（不変条件）を満たすことを検証するテスト観点を生成せよ。
仕様追加は禁止。Diagrams/Pre/Post/failures を変更してはいけない。

出力形式:
- Diagram id:
  - 観測点:
  - テスト粒度（Unit/Integration/Property）:
  - 代表テストケース（入力/期待結果）:
  - 反例（壊れ方）:

Context Pack（必要部分）:
<PASTE_CONTEXT_PACK_HERE>
```

### 3) 成功/失敗（余積）からのテスト網羅

```text
各 Morphism の failures（エラーvariant）を列挙し、variantごとの最小テストケースを作成せよ。
仕様追加は禁止。failures を増減してはいけない。

出力:
- Morphism id:
  - Success ケース:
  - 各 failure variant のケース（入力/期待結果）:

Context Pack（必要部分）:
<PASTE_CONTEXT_PACK_HERE>
```

## リファクタ

### 4) 関手性チェック（仕様→実装の構造保存）

```text
以下の差分（Before/After）について、関手性の観点で逸脱がないかレビューせよ。
仕様追加は禁止。Forbidden changes を前提に、違反の可能性を指摘し、修正方針を提案せよ。

観点:
- 境界（Objects）とモジュール対応が保たれているか
- 操作の合成（順序/依存）が勝手に変わっていないか
- Pre/Post/failures/Diagrams が暗黙に変化していないか

入力:
- Context Pack: <PASTE_CONTEXT_PACK_HERE>
- Diff: <PASTE_DIFF_HERE>
```

### 5) 自然性チェック（意味保存の差分）

```text
以下のリファクタ（Before/After）を「意味保存の差分」として扱い、自然性（可換条件）を満たすかレビューせよ。
仕様追加は禁止。各 Morphism について可換チェック（テスト観点）を提示せよ。

出力:
- 影響範囲（Objects/Morphisms/Diagrams）
- 互換性リスク（API/データ/監査/権限）
- 可換チェック（Morphism id ごとのテスト観点）
- 差し戻し条件（Forbidden changes 観点）

入力:
- Context Pack: <PASTE_CONTEXT_PACK_HERE>
- Before/After 概要: <PASTE_BEFORE_AFTER_HERE>
```

### 6) 禁止事項を守らせる（強制ガード）

```text
次の Forbidden changes を破る提案は一切しないこと。
もし要求を満たすために Forbidden changes を破る必要があるなら、実行せず「必要な確認事項」を質問せよ。

Forbidden changes:
<PASTE_FORBIDDEN_CHANGES_HERE>
```
