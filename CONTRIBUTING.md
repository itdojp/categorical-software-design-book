# Contributing

## 基本方針

- **Issue first**: 変更は原則Issue起点で行う（目的・スコープ・DoDを明確化）
- **小さいPR**: レビュー可能な粒度に分割する（目安: 1章/1テーマ）
- **SSOT**: 用語・テンプレ・共通例題は単一の真実に集約する
- **No placeholders**: 未確定表現（プレースホルダ）を公開コンテンツに残さない（CIで検出）

## 執筆/改稿のルール

- 章構造は `docs/style/chapter-template.md` に従う
- 用語/記法は `docs/style/terminology.md`, `docs/style/notation.md` と `GLOSSARY.md` に従う
- 図式・図版は `docs/style/diagram-style.md` に従う

## ローカルQA（CI相当）

前提:
- Node.js（CIは Node 20）
- Python 3（CIは Python 3.12）
- Git
- Bash

実行:

```bash
npm run qa
```

出力:
- `qa-reports/*.json`

## レビュー観点（最低限）

- 章間の参照が壊れていない（リンク/アンカー/用語）
- 不変条件（Diagrams）が検証可能な形になっている
- AI引き渡し（Context Pack）が再現可能である（`docs/spec/context-pack-v1.md`）

## 提案・議論

- 仕様変更や訳語変更は Issue で合意を取る
- 図式の表現方式（Mermaid/SVG/TeX等）の変更は、移行計画を添える
