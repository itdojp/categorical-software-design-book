---
title: "共通例題（注文処理）"
description: "全章で参照する共通ドメイン例（Order/Payment/Inventory/Shipment/Audit）"
---

# 共通例題（注文処理）

本書は抽象概念を「設計成果物」へ落とすことを重視するため、全章で参照する共通例題を固定します。

- ドメイン: 注文処理（Order/Payment/Inventory/Shipment）＋監査ログ（Audit）
- 目的: 分割/統合/移行/効果/非同期/整合性を一通り扱える最小構成

## 成果物

- reader-facing な正本: https://itdojp.github.io/categorical-software-design-book/examples/common-example/
- 形式と必須項目の正本: [`docs/spec/context-pack-v1.md`](../../spec/context-pack-v1.md)
- local 検証 / authoring 用入口: [`docs/examples/common-example/context-pack-v1.yaml`](./context-pack-v1.yaml)

注記: 内容確認の起点は公開ページの共通例題ハブです。README は repository 内での補助説明であり、YAML への repo-relative link は local 検証や authoring 作業へ戻るための入口です。current checkout に未公開の変更が含まれる場合でも、reader-facing な確認は公開ページと `CHANGELOG.md` を優先します。
