---
title: "最小例: minimal-example（Context Pack v1）"
description: "Context Pack v1 の最小の有効例（Schema-valid）"
---

# 最小例: minimal-example（Context Pack v1）

本ページは、本文・仕様ページから「最小例のContext Pack」に確実に到達するためのハブです。

## 導線

- Context Pack v1 仕様: [docs/spec/context-pack-v1.md](../../spec/context-pack-v1.md)
- 最小例 Context Pack（YAML）:
  - raw（推奨）: [raw](https://raw.githubusercontent.com/itdojp/categorical-software-design-book/main/docs/examples/minimal-example/context-pack-v1.yaml)
  - GitHub: [GitHub](https://github.com/itdojp/categorical-software-design-book/blob/main/docs/examples/minimal-example/context-pack-v1.yaml)
  - サイト内で読む: [YAML（全文）](#yaml-full)

## 最小lint（ローカル）

```bash
python3 scripts/validate-context-pack.py docs/examples/minimal-example/context-pack-v1.yaml
```

## YAML（全文） {#yaml-full}

```yaml
{% include_relative context-pack-v1.yaml %}
```
