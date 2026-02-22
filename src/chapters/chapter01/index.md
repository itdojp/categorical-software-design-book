---
title: "第1章: AIエージェント開発の分担モデルと設計成果物"
chapter: chapter01
---

# 第1章: AIエージェント開発の分担モデルと設計成果物

## 学習ゴール

- 人間とAIの責任分界（要件/設計/検証 vs 実装/テスト/リファクタ）を説明できる
- 「設計成果物＝AIへの入力契約」という前提で、成果物の最小セットを定義できる
- Context Pack v1 の構造を理解し、最小の入力として作成できる

## 圏論コア（定義・直観・ミニ例）

（本章で扱う最小の定義・直観・ミニ例を記載）

## ソフトウェア設計への射影（どこに効くか）

- 曖昧さが残るとAI委任が破綻するポイント（境界/不変条件/権限/失敗条件）
- 仕様→設計→検証の固定が、後段（実装/テスト生成）を安定化させる理由

## 設計成果物（テンプレ：表/図式/チェックリスト）

本書の共通例題（注文処理）は [Context Pack v1（共通例題）](../../../docs/examples/common-example/context-pack-v1.yaml) を参照。

- Objects: 型/状態/権限/エラー
- Morphisms: 操作/API、Pre/Post、失敗条件
- Diagrams: 可換図式（不変条件）
- Acceptance tests: 最小の受入テスト

## AIエージェントへの引き渡し（Context Pack/プロンプト/禁止事項）

- Context Pack v1 仕様: [docs/spec/context-pack-v1.md](../../../docs/spec/context-pack-v1.md)
- 共通例題 Context Pack: [docs/examples/common-example/context-pack-v1.yaml](../../../docs/examples/common-example/context-pack-v1.yaml)
- 禁止事項: 不変条件（Diagrams）と権限境界を無断変更しない

## 検証（テスト観点・可換性チェック）

- 不変条件（Diagrams）がテスト観点へ落ちていることを確認する
- 例: 監査ログ一貫性（D2）が必ず満たされる（[共通例題 Context Pack](../../../docs/examples/common-example/context-pack-v1.yaml)）

## 演習（手で設計→AIに実装/テスト生成させる）

1. 共通例題を読み、Objects/Morphisms/Diagrams を要約してContext Pack v1を作る
2. 作成した Context Pack をAIに渡し、受入テストと実装スケルトンを生成させる
3. 生成物が Forbidden changes を侵害していないかレビューする

## まとめ（再利用可能なルール）

- AIに委任する前に、入力契約（Context Pack）を固定する
- 不変条件（Diagrams）は「検証可能な形」で定義する
- 用語・記法・成果物テンプレをSSOTで管理し、章間の揺れを抑制する
