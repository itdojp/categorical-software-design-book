# Pull Request

## 概要

- 目的:
- 対象Issue:

## 関連 Issue（任意）

- Refs #
- Parent roadmap（該当時のみ）:
- Management issue（該当時のみ）:

## 変更内容

- 変更内容:

## チェックリスト

- [ ] `docs/style/chapter-template.md` に沿った構成になっている（章変更の場合）
- [ ] `GLOSSARY.md` / `docs/style/*` に沿って用語・記法が統一されている
- [ ] 主要リンクが壊れていない（相互参照、画像、外部リンク）
- [ ] Context Pack v1 の参照/更新が必要な場合、`docs/spec/context-pack-v1.md` に従っている
- [ ] `npm run qa`（またはCI）を実行し、次を確認した
  - link / unicode / structure / textlint
  - Context Pack minimal lint / schema validation
  - rendered HTML check
- [ ] Context Pack v1 を更新した場合、spec/例題/テンプレの同期チェックが通っている
      （該当する場合）

## Review Completion Gate（必須）

- [ ] GitHub Copilot review を依頼した
- [ ] review 本文・inline comment・suggestion を全件確認した
- [ ] 必要な修正を行った、または不要な理由を該当 thread / PR に返信した
- [ ] 未解決 review thread 0 を確認した
- [ ] merge 前に CI green を確認した
