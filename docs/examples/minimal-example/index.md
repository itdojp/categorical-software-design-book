---
title: "最小例: minimal-example（Context Pack v1）"
description: "Context Pack v1 の最小の有効例（minimal lint + schema validation）"
permalink: /examples/minimal-example/
---

# 最小例: minimal-example（Context Pack v1）

本ページは、本文理解を補助するための最小例サマリです。章本文の代替ではなく、
「最低限どこまで書けば Context Pack v1 として成立するか」を先に把握し、
必要なら YAML 全文へ降りるための導線として使います。

## 最小例の見どころ

次の断片だけで、`problem_statement`、`objects`、`morphisms`、`diagrams`、
`acceptance_tests`、`forbidden_changes` が揃っていることを確認できます。

```yaml
problem_statement:
  goals: ["最小の例として成立させる"]
objects:
  - id: Order
morphisms:
  - id: PlaceOrder
    pre: ["Order.state == Draft"]
diagrams:
  - id: D1-order-state
acceptance_tests:
  - id: AT1-happy-path
```

## 省けないもの / 省いてよいもの

<table>
  <thead>
    <tr>
      <th>省けないもの</th>
      <th>省いてよいもの</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>problem_statement</code>、<code>objects</code>、<code>morphisms</code>、<code>diagrams</code>、<code>acceptance_tests</code>、<code>forbidden_changes</code></td>
      <td>複数 Object、詳細な field 一覧、複数 Morphism、詳細な <code>constraints</code>、詳細なディレクトリ規約</td>
    </tr>
    <tr>
      <td>最低 1 つの操作契約と 1 つの不変条件</td>
      <td>運用要件の拡張、監査や権限制御の詳細、複数テストシナリオ</td>
    </tr>
  </tbody>
</table>

## 導線

- Context Pack v1 仕様: [Context Pack v1 仕様](../../spec/context-pack-v1.md)
- 最小例 Context Pack（YAML）:
  - raw（推奨）: [raw](https://raw.githubusercontent.com/itdojp/categorical-software-design-book/main/docs/examples/minimal-example/context-pack-v1.yaml)
  - GitHub: [GitHub](https://github.com/itdojp/categorical-software-design-book/blob/main/docs/examples/minimal-example/context-pack-v1.yaml)
  - サイト内で読む: [YAML（全文）](#yaml-full)

## 検証（ローカル）

依存導入（初回のみ）:

```bash
python3 -m pip install -r scripts/requirements-qa.txt
```

minimal lint:

```bash
python3 scripts/validate-context-pack.py docs/examples/minimal-example/context-pack-v1.yaml
```

schema validation（JSON Schema）:

```bash
python3 scripts/validate-context-pack-schema.py docs/examples/minimal-example/context-pack-v1.yaml
```

位置づけ/差分は [Context Pack v1 仕様（検証コマンド）]({{ '/spec/context-pack-v1/' | relative_url }}#validation-commands) を参照してください。

（任意）CI相当の一括チェック: `npm run qa`（レポート: `qa-reports/*.json`）

## YAML（全文） {#yaml-full}

```yaml
{% include_relative context-pack-v1.yaml %}
```
