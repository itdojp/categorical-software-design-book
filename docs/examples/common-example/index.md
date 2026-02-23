---
title: "共通例題: 注文処理（Context Pack v1）"
description: "全章で参照する共通例題（Order/Payment/Inventory/Shipment/Audit）"
---

# 共通例題: 注文処理（Context Pack v1）

本ページは、本文・仕様ページから「共通例題のContext Pack」に確実に到達するためのハブです。

## 導線

- Context Pack v1 仕様: [docs/spec/context-pack-v1.md](../../spec/context-pack-v1.md)
- 例題 Context Pack（YAML）:
  - raw（推奨）: [raw](https://raw.githubusercontent.com/itdojp/categorical-software-design-book/main/docs/examples/common-example/context-pack-v1.yaml)
  - GitHub: [GitHub](https://github.com/itdojp/categorical-software-design-book/blob/main/docs/examples/common-example/context-pack-v1.yaml)
  - サイト内で読む: [YAML（全文）](#yaml-full)

## 最小lint（ローカル）

```bash
python3 scripts/validate-context-pack.py docs/examples/common-example/context-pack-v1.yaml
```

## YAML（全文） {#yaml-full}

```yaml
{% include_relative context-pack-v1.yaml %}
```
