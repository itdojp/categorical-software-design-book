#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bulk create milestones, labels, and issues for:
  categorical-software-design-book

Prerequisites:
  - GitHub CLI: gh
  - Authenticated: gh auth login
  - Run in the target repo directory, or pass --repo owner/repo

Usage:
  python3 scripts/bulk_create_issues.py --dry-run
  python3 scripts/bulk_create_issues.py --repo <owner>/categorical-software-design-book
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import tempfile
import textwrap
from dataclasses import dataclass
from typing import List, Optional, Sequence, Set


# -----------------------------
# Seed data
# -----------------------------

MILESTONES = [
    {
        "title": "M0: Bootstrap（生成/公開/CI）",
        "description": "book-formatterによる雛形生成、Pages公開、CI品質ゲート、運用ポリシーまで。",
    },
    {
        "title": "M1: Skeleton（章立て確定・テンプレ・共通例題）",
        "description": "章ファイルの骨格、章テンプレ、記法/用語/図式スタイル、共通例題、Context Packを確定。",
    },
    {
        "title": "M2: Draft-1（第1〜5章ドラフト）",
        "description": "基礎（合成/図式/関手/自然変換）を“AI委任の設計成果物”に落とす。",
    },
    {
        "title": "M3: Draft-2（第6〜10章ドラフト）",
        "description": "普遍性/統合/並列配線/効果境界/ケーススタディで運用まで通す。",
    },
    {
        "title": "M4: Appendices & Tools（付録・テンプレ集・プロンプト集・簡易ツール）",
        "description": "再利用可能なテンプレ、プロンプト、参考文献、任意でlint/validatorと図版整備。",
    },
    {
        "title": "M5: QA & Release（校正・品質ゲート・v1.0）",
        "description": "通読レビュー、品質チェック最終実行、v1.0.0リリース、フィードバック導線。",
    },
]

LABELS = [
    {"name": "type/setup", "color": "1f77b4", "description": "Repo/bootstrap/setup tasks"},
    {"name": "type/writing", "color": "2ca02c", "description": "Writing/drafting chapters"},
    {"name": "type/diagram", "color": "ff7f0e", "description": "Diagrams/figures/visual assets"},
    {"name": "type/tooling", "color": "9467bd", "description": "Tools/scripts/schema/validator"},
    {"name": "type/qa", "color": "d62728", "description": "Review/QA/proofreading"},
    {"name": "type/automation", "color": "8c564b", "description": "CI/CD/automation"},
    {"name": "prio/P0", "color": "b60205", "description": "Blocker / must-do"},
    {"name": "prio/P1", "color": "fbca04", "description": "Important"},
    {"name": "prio/P2", "color": "cfd3d7", "description": "Nice to have"},
]


def md(s: str) -> str:
    return textwrap.dedent(s).strip() + "\n"


ISSUES = [
    # -------------------------
    # M0
    # -------------------------
    {
        "title": "001: book-formatterで書籍プロジェクト雛形を生成し初回コミット",
        "milestone": "M0: Bootstrap（生成/公開/CI）",
        "labels": ["type/setup", "prio/P0"],
        "body": md(
            """
            ## 目的
            book-formatter を使って書籍プロジェクト雛形を生成し、`categorical-software-design-book` の初回コミットまで完了させる。

            ## 作業
            - [ ] （ローカル）`book-formatter` を取得して `npm install`
            - [ ] `npm start init --output ./book-config.yaml` で設定雛形を生成（JSON/YAMLどちらで管理するか決める）
            - [ ] 本書メタデータを設定ファイルへ反映
              - title: 圏論によるAIエージェント時代の合成的ソフトウェア設計
              - description: 仕様・設計・検証を合成可能にする共通言語
              - repository.url / branch など
            - [ ] `npm start validate-config --config ./book-config.yaml` を通す（formatter側で）
            - [ ] `npm start create-book --config ./book-config.yaml --output <book-repo-dir> --force` で雛形生成
            - [ ] 生成物を `categorical-software-design-book` へ配置し初回コミット

            ## 完了条件（DoD）
            - [ ] book repo に `src/`, `index.md`, `_config.yml`, `package.json` 等が揃っている
            - [ ] GitHub上でリポジトリが閲覧可能（READMEが最低限ある）
            - [ ] 設定ファイルがリポジトリで管理されている（後から再生成/更新できる）
            """
        ),
    },
    {
        "title": "002: book-configの確定（章立て・付録・メタデータ）",
        "milestone": "M0: Bootstrap（生成/公開/CI）",
        "labels": ["type/setup", "prio/P0"],
        "body": md(
            """
            ## 目的
            本書の「章構成」「付録」「メタデータ」を book-config（JSON/YAML）で確定し、設定ファイルを単一の真実（SSOT）にする。

            ## 作業
            - [ ] `title / description / author / version / language / license` を確定
            - [ ] `structure.chapters[]` と `structure.appendices[]` を確定
              - chapter01..chapter10
              - appendices: templates / prompts / references
            - [ ] `repository.url` と `branch` を正しい値にする
            - [ ] `npm start validate-config --config ./book-config.* --verbose` を通す（formatter側で）

            ## 完了条件（DoD）
            - [ ] 設定ファイルから生成したナビゲーションで全章へ到達できる
            - [ ] 章ID/パスが今後の運用でブレない（命名規約が固まっている）
            """
        ),
    },
    {
        "title": "003: GitHub Pages公開設定（Deploy from a branch）",
        "milestone": "M0: Bootstrap（生成/公開/CI）",
        "labels": ["type/setup", "prio/P0"],
        "body": md(
            """
            ## 目的
            GitHub Pages を有効化し、公開URLで閲覧できる状態にする。

            ## 作業
            - [ ] Settings → Pages で有効化
              - Source: Deploy from a branch
              - Branch: `main`
              - Folder: 生成物に合わせて `/` か `/docs` を選択
            - [ ] 公開URLで以下を確認
              - [ ] トップ（index）
              - [ ] 章ページ
              - [ ] ナビ（前/次、目次、サイドバー等）
            - [ ] `docs/_config.yml` の `url/baseurl/repository` を監査（必要なら正規化）

            ## 完了条件（DoD）
            - [ ] 公開URLで404が出ない
            - [ ] 章間リンクが機能する
            """
        ),
    },
    {
        "title": "004: ローカル開発手順をREADMEに確立（プレビュー/ビルド）",
        "milestone": "M0: Bootstrap（生成/公開/CI）",
        "labels": ["type/setup", "prio/P1"],
        "body": md(
            """
            ## 目的
            執筆者がローカルで再現性高くプレビューできる状態を作る（環境差で詰まらないようにする）。

            ## 作業
            - [ ] README に以下を明記
              - 前提（Node, Ruby/Bundler, もしくはDocker）
              - セットアップ
              - ローカルプレビュー（Jekyll serve等）
              - ビルド（Jekyll build等）
            - [ ] （任意）`scripts/` で `dev/build` ラッパを用意
            - [ ] （任意）Docker化（執筆環境固定が必要なら）

            ## 完了条件（DoD）
            - [ ] README手順のみでローカルプレビューまで到達できる
            """
        ),
    },
    {
        "title": "005: CI品質ゲート整備（build/link/unicode/markdown/textlint）",
        "milestone": "M0: Bootstrap（生成/公開/CI）",
        "labels": ["type/automation", "prio/P0"],
        "body": md(
            """
            ## 目的
            AI編集を前提に、壊れやすいポイント（リンク切れ、不可視文字、構造崩れ、文章品質）をPR段階で機械検出する。

            ## 方針
            book-formatter の品質チェック（リンク/Unicode/レイアウトリスク/Markdown構造/textlint）をCIに組み込む。

            ## 作業
            - [ ] GitHub Actions（例: `.github/workflows/ci.yml`）を追加
            - [ ] PRごとに以下を実行（book repo を `<book-dir>` として指定）
              - [ ] （必要なら）`book-formatter` をCIで clone して `npm install`
              - [ ] `npm run check-links -- <book-dir>`
              - [ ] `npm run check-unicode -- <book-dir> --output unicode-report.json`
              - [ ] `npm run check-layout-risk -- <book-dir> --output layout-risk-report.json`
              - [ ] `npm run check-markdown-structure -- <book-dir> --output markdown-structure-report.json`
              - [ ] `npm run check-textlint -- <book-dir> --output textlint-report.json`
              - [ ] （任意）`npm run check-textlint -- <book-dir> --with-preset --output textlint-report-with-preset.json`
              - [ ] （任意）Jekyll build（最低限ビルドが通ること）
            - [ ] 失敗時にレポートJSONをArtifactsに保存

            ## 完了条件（DoD）
            - [ ] PRで品質チェックが自動実行される
            - [ ] チェック失敗時に原因調査に必要なレポートが残る
            """
        ),
    },
    {
        "title": "006: 執筆運用ポリシー整備（AI利用/更新/貢献）",
        "milestone": "M0: Bootstrap（生成/公開/CI）",
        "labels": ["type/setup", "prio/P1"],
        "body": md(
            """
            ## 目的
            AIを使って執筆/改稿する前提で、責任分界・出典・検証・更新方針を明文化する。

            ## 作業
            - [ ] `AI_USAGE_POLICY.md`
              - AI生成物は必ず人間が検証（仕様/図式/例が矛盾しないこと）
              - 参考文献・出典の扱い（引用/要約/リンク）
              - プロンプトやContext Packの機密/公開範囲
            - [ ] `UPDATE_POLICY.md`
              - バージョニング（SemVer相当）、破壊的変更の扱い、改訂履歴
            - [ ] `CONTRIBUTING.md`
              - Issue first、PR粒度、レビュー観点、図式/テンプレ変更のルール
            - [ ] （任意）`.github/PULL_REQUEST_TEMPLATE.md` を用意（チェックリスト）

            ## 完了条件（DoD）
            - [ ] 今後の執筆/改稿がポリシーに沿って運用できる
            """
        ),
    },

    # -------------------------
    # M1
    # -------------------------
    {
        "title": "007: 章ファイルのスケルトン生成（chapter01..10 + appendices）",
        "milestone": "M1: Skeleton（章立て確定・テンプレ・共通例題）",
        "labels": ["type/setup", "prio/P0"],
        "body": md(
            """
            ## 目的
            章構成を物理ファイルとして固定し、以後は「章を埋める」作業に集中できる状態にする。

            ## 作業
            - [ ] `chapters/chapter01..chapter10/index.md` を作成（front matter含む）
            - [ ] `appendices/templates/index.md` 等を作成
            - [ ] 章タイトル・番号・ナビゲーションの整合性を確認
            - [ ] 空の状態でもビルドできることを確認

            ## 完了条件（DoD）
            - [ ] 全章が空でもビルドでき、ナビが途切れない
            """
        ),
    },
    {
        "title": "008: 章テンプレ確定（学習ゴール/コア/設計成果物/AI引き渡し/演習）",
        "milestone": "M1: Skeleton（章立て確定・テンプレ・共通例題）",
        "labels": ["type/writing", "prio/P0"],
        "body": md(
            """
            ## 目的
            章ごとの品質と粒度を揃える（AI生成でも破綻しない構造にする）。

            ## テンプレ（必須セクション案）
            - 学習ゴール（読了後にできること）
            - 圏論コア（定義・直観・ミニ例）
            - ソフトウェア設計への射影（どこに効くか）
            - 設計成果物（テンプレ：表/図式/チェックリスト）
            - AIエージェントへの引き渡し（Context Pack/プロンプト/禁止事項）
            - 検証（テスト観点・可換性チェック）
            - 演習（手で設計→AIに実装/テスト生成させる）
            - まとめ（再利用可能なルール）

            ## 作業
            - [ ] `docs/style/chapter-template.md`（等）としてテンプレ文書化
            - [ ] chapter01 にテンプレを適用して雛形を作る
            - [ ] PRレビュー観点（章テンプレ遵守）を定義

            ## 完了条件（DoD）
            - [ ] chapter01 がテンプレ通りの骨格になっている
            """
        ),
    },
    {
        "title": "009: 用語・記法・図式スタイルガイド作成（統一ルール）",
        "milestone": "M1: Skeleton（章立て確定・テンプレ・共通例題）",
        "labels": ["type/writing", "type/diagram", "prio/P1"],
        "body": md(
            """
            ## 目的
            記法ブレと訳語ブレを排除し、読解コストとAI生成の揺れを減らす。

            ## 作業
            - [ ] 記法ルール（対象/射/合成/恒等、可換図式、積/余積、⊗、Kleisli等）
            - [ ] 用語の日本語訳方針（関手/自然変換/随伴/普遍性など）
            - [ ] 図式の表現方式（Mermaid/PlantUML/SVG/TeX等）を決める
            - [ ] 画像配置・命名規約（`docs/assets/images/...` 等）を決める
            - [ ] `GLOSSARY.md`（用語集）を作る（最初は最低限）

            ## 完了条件（DoD）
            - [ ] 同じ概念が章ごとに違う言葉で出ない
            """
        ),
    },
    {
        "title": "010: 共通例題システム確定（仕様→設計→検証の最小版）",
        "milestone": "M1: Skeleton（章立て確定・テンプレ・共通例題）",
        "labels": ["type/writing", "type/tooling", "prio/P0"],
        "body": md(
            """
            ## 目的
            全章で参照できる「一本の例題」を固定し、抽象概念を設計成果物へ落とす基盤にする。

            ## 推奨例題（案）
            注文処理（Order/Payment/Inventory/Shipment）＋監査ログ（Audit）
            ※分割/統合/移行/効果/非同期/整合性を一通り扱える。

            ## 作業
            - [ ] ドメイン境界（bounded context）を定義
            - [ ] 主要データ型（Objects）と操作（Morphisms）を列挙
            - [ ] 可換性で表現できる要件（Diagrams）を3〜5個作る
              - 例：冪等、整合性、監査ログ一貫性、権限境界
            - [ ] 「最小のContext Pack（v1）」として格納

            ## 完了条件（DoD）
            - [ ] chapter01〜chapter10 で同一例題を参照できる
            """
        ),
    },
    {
        "title": "011: Context Pack v1 仕様作成（AIエージェント引き渡しフォーマット）",
        "milestone": "M1: Skeleton（章立て確定・テンプレ・共通例題）",
        "labels": ["type/writing", "prio/P0"],
        "body": md(
            """
            ## 目的
            人間が作る設計成果物を、AIが実装/テストへ落とすための「入出力契約」を固定する。

            ## Context Pack v1（案）
            - Problem statement（目的・非目的）
            - Domain glossary（用語辞書）
            - Objects（型/状態/権限/エラー）
            - Morphisms（操作/API）＋ Pre/Post ＋ 失敗条件
            - Diagrams（可換図式）＝必須不変条件
            - Constraints（性能/セキュリティ/運用）
            - Acceptance tests（最小セット）
            - Coding conventions（言語/ディレクトリ/依存）
            - Forbidden changes（AIが勝手に変更してはいけない事項）

            ## 作業
            - [ ] `docs/spec/context-pack-v1.md` として仕様化
            - [ ] 例題システムのContext Packをこの形式に合わせる
            - [ ] 章末演習でこのフォーマットを使うことを明記

            ## 完了条件（DoD）
            - [ ] 「同じフォーマットでAIに渡せる」が全章で維持できる
            """
        ),
    },
    {
        "title": "012: （任意）Context Packの機械可読スキーマ（YAML/JSON）作成",
        "milestone": "M1: Skeleton（章立て確定・テンプレ・共通例題）",
        "labels": ["type/tooling", "prio/P2"],
        "body": md(
            """
            ## 目的
            設計成果物を機械可読にして、欠落/矛盾をlint可能にする（AI投入前の防波堤）。

            ## 作業
            - [ ] YAML/JSONで Objects/Morphisms/Diagrams を表現する最小スキーマ定義
            - [ ] 例題システムをその形式で格納
            - [ ] 必須項目チェック（簡易lint）の設計（実装はM4でも可）

            ## 完了条件（DoD）
            - [ ] 本文の表/図式が「データ」として再利用可能になる
            """
        ),
    },

    # -------------------------
    # M2 chapters 1-5
    # -------------------------
    {
        "title": "101: 第1章ドラフト — AIエージェント開発の分担モデルと設計成果物",
        "milestone": "M2: Draft-1（第1〜5章ドラフト）",
        "labels": ["type/writing", "prio/P0"],
        "body": md(
            """
            ## 狙い
            - 人間が担うべき作業（要件定義/設計/検証条件の固定）と、AIに委任できる作業（実装/テスト/リファクタ）を切り分ける。
            - 「設計成果物＝AIへの入力契約」という本書の立場を確立する。

            ## 必須内容
            - [ ] 失敗パターン（AI任せで壊れるポイント：曖昧さ、境界不明、検証不足）
            - [ ] 本書の用語（Objects/Morphisms/Diagrams、Context Pack）
            - [ ] 例題システムの最小Context Packを提示
            - [ ] 章末演習：Context Pack→AI実装/テストの最小ループ

            ## 完了条件（DoD）
            - [ ] 読者が「何を作ればAIに投げられるか」を理解できる
            """
        ),
    },
    {
        "title": "102: 第2章ドラフト — 合成の最小コア（対象・射・合成）",
        "milestone": "M2: Draft-1（第1〜5章ドラフト）",
        "labels": ["type/writing", "prio/P0"],
        "body": md(
            """
            ## 狙い
            設計の単位を揃え、合成可能な分解（部品化）を作る。

            ## 必須内容
            - [ ] 対象＝状態/型/境界、射＝変換/操作、合成＝パイプライン
            - [ ] 合成律（結合律・恒等射）が保守性に効く理由
            - [ ] 設計成果物：Objects/Morphismsテンプレ（例題で埋める）
            - [ ] AI引き渡し：射の契約（Pre/Post、失敗）をAIに守らせる

            ## 完了条件（DoD）
            - [ ] 例題システムを Objects/Morphisms に落とせる
            """
        ),
    },
    {
        "title": "103: 第3章ドラフト — 図式と可換性（仕様をテスト可能にする）",
        "milestone": "M2: Draft-1（第1〜5章ドラフト）",
        "labels": ["type/writing", "prio/P0"],
        "body": md(
            """
            ## 狙い
            「正しさ」を例示ではなく性質（可換条件）として固定し、テストに落とす。

            ## 必須内容
            - [ ] 可換図式＝同値条件/整合条件（冪等、正規化、互換性、権限境界など）
            - [ ] 図式→テスト観点への変換手順（単体/統合/プロパティ）
            - [ ] AIプロンプト例：図式からテストを生成させる（禁止：仕様追加）
            - [ ] 演習：図式追加→テスト追加→CIで破綻検知

            ## 完了条件（DoD）
            - [ ] 図式が“検証項目リスト”へ変換できる
            """
        ),
    },
    {
        "title": "104: 第4章ドラフト — 関手（仕様→設計→実装の写像）",
        "milestone": "M2: Draft-1（第1〜5章ドラフト）",
        "labels": ["type/writing", "prio/P1"],
        "body": md(
            """
            ## 狙い
            AI委任を「仕様→実装の構造保存写像」として捉え、逸脱を検知/抑制する。

            ## 必須内容
            - [ ] 関手＝構造保存（合成保存・恒等保存）
            - [ ] 仕様の分解と実装の分解の対応（モジュール境界の固定）
            - [ ] Context Pack に「保存すべき構造」を書く（禁止事項/制約）
            - [ ] AI生成物のレビュー観点：関手性の破綻パターン

            ## 完了条件（DoD）
            - [ ] 仕様変更時に「どこまでAIに任せてよいか」線引きできる
            """
        ),
    },
    {
        "title": "105: 第5章ドラフト — 自然変換（差分・リファクタを意味保存で扱う）",
        "milestone": "M2: Draft-1（第1〜5章ドラフト）",
        "labels": ["type/writing", "prio/P1"],
        "body": md(
            """
            ## 狙い
            AIによる改修・リファクタを「意味保存の差分」として扱い、破壊的変更を抑制する。

            ## 必須内容
            - [ ] 自然変換＝対象ごとの成分が整合する“全体の置換”
            - [ ] リファクタをAIに投げるときの安全柵（自然性＝可換条件）
            - [ ] テンプレ：Before/After + 可換チェック（影響範囲、互換性）
            - [ ] 演習：差分説明→可換図式テスト→CIで検証

            ## 完了条件（DoD）
            - [ ] AI改修を「意味保存」でレビューできる
            """
        ),
    },

    # -------------------------
    # M3 chapters 6-10
    # -------------------------
    {
        "title": "201: 第6章ドラフト — 普遍性（積・余積）で標準化する契約",
        "milestone": "M3: Draft-2（第6〜10章ドラフト）",
        "labels": ["type/writing", "prio/P1"],
        "body": md(
            """
            ## 狙い
            API/データ契約の迷いを減らし、AIが実装/テストを安定生成できる“標準形”に落とす。

            ## 必須内容
            - [ ] 積＝AND（情報の束）、余積＝OR（分岐/Union/エラー合成）
            - [ ] エラー設計（成功/失敗の余積）とテスト設計の接続
            - [ ] AIに「最小の契約」を設計させる指示の書き方
            - [ ] 例題での適用（DTO/API/ドメイン型）

            ## 完了条件（DoD）
            - [ ] インターフェース肥大化を抑える設計ルールが得られる
            """
        ),
    },
    {
        "title": "202: 第7章ドラフト — Pullback/Pushout（統合・移行の設計パターン）",
        "milestone": "M3: Draft-2（第6〜10章ドラフト）",
        "labels": ["type/writing", "prio/P1"],
        "body": md(
            """
            ## 狙い
            統合点（結合・移行・境界変更）を図式として設計し、壊れ方を事前に封じる。

            ## 必須内容
            - [ ] Pullback（整合のある結合）/ Pushout（共通インターフェースでの接着）の直観
            - [ ] 代表ケース：スキーマ統合、サービス統合、認証統合、移行（旧→新）
            - [ ] 図式としての統合条件 → テスト項目（差分/互換）へ変換
            - [ ] 例題での適用（Order/Payment等の接着）

            ## 完了条件（DoD）
            - [ ] “統合で壊れる”を事前に図式で表現できる
            """
        ),
    },
    {
        "title": "203: 第8章ドラフト — モノidal圏とストリング図式（分業と配線）",
        "milestone": "M3: Draft-2（第6〜10章ドラフト）",
        "labels": ["type/writing", "type/diagram", "prio/P1"],
        "body": md(
            """
            ## 狙い
            並列/配線/分業（マルチエージェント）を設計成果物として固定し、実装委任を破綻させない。

            ## 必須内容
            - [ ] 逐次合成（∘）と並列合成（⊗）の区別
            - [ ] ストリング図式で接続点・合流点を可視化
            - [ ] エージェント分割テンプレ（役割/入出力/合成規則）
            - [ ] 例題での適用（CIパイプライン、並列テスト、非同期処理）

            ## 完了条件（DoD）
            - [ ] 複数AIエージェントの協調を“設計”として管理できる
            """
        ),
    },
    {
        "title": "204: 第9章ドラフト — モナド/Kleisli（効果境界の設計）",
        "milestone": "M3: Draft-2（第6〜10章ドラフト）",
        "labels": ["type/writing", "prio/P1"],
        "body": md(
            """
            ## 狙い
            IO/DB/外部API/例外/リトライ等の“効果”を境界に隔離し、AI委任後も検証可能性を維持する。

            ## 必須内容
            - [ ] pure core / impure shell の設計原則
            - [ ] 失敗モデル・リトライ・冪等性・監査ログの扱い
            - [ ] AIへの指示：副作用を勝手に増やさない／境界を守る
            - [ ] 図式→テスト：効果境界のテスト戦略

            ## 完了条件（DoD）
            - [ ] 運用要件（監査・信頼性）を破壊しない実装委任ができる
            """
        ),
    },
    {
        "title": "205: 第10章ドラフト — ケーススタディ（仕様→設計→検証→AI実装）",
        "milestone": "M3: Draft-2（第6〜10章ドラフト）",
        "labels": ["type/writing", "prio/P0"],
        "body": md(
            """
            ## 狙い
            本書の方法を「通し」で実演し、読者が自プロジェクトへ移植できる運用形に落とす。

            ## 必須内容
            - [ ] 例題システムで Context Pack → AI実装 → テスト → レビュー まで通す
            - [ ] 図式が壊れたときの検知・修正フロー
            - [ ] GitHub運用（Issue→PR→CI→レビュー）具体例
            - [ ] 失敗例（AIが勝手に仕様追加/構造破壊）と防止策

            ## 完了条件（DoD）
            - [ ] 読者が自分のプロジェクトに移植できる手順が手に入る
            """
        ),
    },

    # -------------------------
    # M4 appendices & tools
    # -------------------------
    {
        "title": "301: 付録A — 設計成果物テンプレ集（Objects/Morphisms/Diagrams/チェックリスト）",
        "milestone": "M4: Appendices & Tools（付録・テンプレ集・プロンプト集・簡易ツール）",
        "labels": ["type/writing", "prio/P0"],
        "body": md(
            """
            ## 目的
            本文の内容を再利用可能な“型”として提供する（コピペで使える）。

            ## 収録内容
            - [ ] Objectsテンプレ（型/状態/不変条件/権限/エラー）
            - [ ] Morphismsテンプレ（シグネチャ、Pre/Post、失敗、冪等性）
            - [ ] Diagramsテンプレ（可換条件→テスト観点）
            - [ ] レビュー用チェックリスト（AI生成物レビュー含む）

            ## 完了条件（DoD）
            - [ ] 本文の例が、そのままテンプレとして再利用できる
            """
        ),
    },
    {
        "title": "302: 付録B — AIエージェント用プロンプト集（実装/テスト/リファクタ/検証）",
        "milestone": "M4: Appendices & Tools（付録・テンプレ集・プロンプト集・簡易ツール）",
        "labels": ["type/writing", "prio/P0"],
        "body": md(
            """
            ## 目的
            本書の方法を、現場でそのまま実行できるプロンプトとして提供する。

            ## 収録内容（最低限）
            - [ ] Context Pack投入プロンプト（入力固定化）
            - [ ] 図式→テスト生成プロンプト
            - [ ] 関手性/自然性チェックプロンプト（逸脱検知）
            - [ ] 禁止事項を守らせるプロンプト（勝手な仕様追加を抑止）
            - [ ] レビュー用プロンプト（差分説明、影響範囲、根拠提示）

            ## 完了条件（DoD）
            - [ ] 章末演習でそのまま使える
            """
        ),
    },
    {
        "title": "303: 付録C — 学習マップ・参考文献・発展ルート",
        "milestone": "M4: Appendices & Tools（付録・テンプレ集・プロンプト集・簡易ツール）",
        "labels": ["type/writing", "prio/P1"],
        "body": md(
            """
            ## 目的
            本書の範囲外も含め、次の学習・調査の導線を提供する。

            ## 作業
            - [ ] 圏論（最小）→ 応用（FP/型/意味論）→ 形式手法 の学習導線
            - [ ] 本書の線引き（扱わない高等トピック）
            - [ ] 参考文献（書籍/論文/講義ノート）整理（章ごとに対応づけ）

            ## 完了条件（DoD）
            - [ ] 読者が次に学ぶべき順番が分かる
            """
        ),
    },
    {
        "title": "304: （任意）設計テンプレの簡易バリデータ（lint）実装",
        "milestone": "M4: Appendices & Tools（付録・テンプレ集・プロンプト集・簡易ツール）",
        "labels": ["type/tooling", "prio/P2"],
        "body": md(
            """
            ## 目的
            Context Pack / テンプレの欠落・矛盾を機械的に検出し、AI投入前に止める。

            ## 作業
            - [ ] YAML/JSON（Context Pack）に対する必須項目チェック
            - [ ] 参照整合（型名・操作名・図式参照の整合）を最低限チェック
            - [ ] CIで実行できる形にする（失敗時にエラー一覧を出す）

            ## 完了条件（DoD）
            - [ ] “AIに渡す前に人間が気付ける”状態
            """
        ),
    },
    {
        "title": "305: 図版整備（主要図式セット＋命名規約＋配置）",
        "milestone": "M4: Appendices & Tools（付録・テンプレ集・プロンプト集・簡易ツール）",
        "labels": ["type/diagram", "prio/P1"],
        "body": md(
            """
            ## 目的
            抽象概念の理解と運用を支える図版を、再利用可能な資産として整備する。

            ## 作業
            - [ ] 各章で最低1つの図式を作る（可換図式/境界図/ストリング図式）
            - [ ] 画像形式を決めて統一（推奨: SVG）
            - [ ] 画像の配置・命名規約を確定
            - [ ] レイアウト崩れ（横長表/巨大画像）を抑制

            ## 完了条件（DoD）
            - [ ] 図がない章が発生しない
            """
        ),
    },

    # -------------------------
    # M5 QA & release
    # -------------------------
    {
        "title": "401: 全章通読レビュー（論理整合・用語統一・参照整合）",
        "milestone": "M5: QA & Release（校正・品質ゲート・v1.0）",
        "labels": ["type/qa", "prio/P0"],
        "body": md(
            """
            ## 目的
            通読で破綻しない状態にする（章間矛盾、用語ブレ、参照切れを潰す）。

            ## 作業
            - [ ] 用語統一（用語集と照合）
            - [ ] 章間の前提整合（矛盾がない）
            - [ ] 図表番号・章番号・相互参照の整合
            - [ ] AIプロンプトが本文と矛盾しない
            - [ ] 例題システムが章を跨いで一貫している

            ## 完了条件（DoD）
            - [ ] 読者が「途中で前提が変わった」と感じない
            """
        ),
    },
    {
        "title": "402: 品質チェック最終実行（リンク/Unicode/構造/textlint/ビルド）",
        "milestone": "M5: QA & Release（校正・品質ゲート・v1.0）",
        "labels": ["type/qa", "type/automation", "prio/P0"],
        "body": md(
            """
            ## 目的
            v1.0としての品質ゲートを通し、公開状態で崩れないことを担保する。

            ## 作業
            - [ ] リンクチェック（内部リンク/アンカー）
            - [ ] Unicode品質チェック（不可視文字/互換漢字/異体字セレクタ等）
            - [ ] Markdown構造チェック（Front Matter/見出しレベル/コードフェンス言語）
            - [ ] textlint（必要なら技術文書プリセット併用）
            - [ ] Jekyll build（公開用ビルド）

            ## 完了条件（DoD）
            - [ ] CIがグリーン
            - [ ] Pagesで表示崩れ/404なし
            """
        ),
    },
    {
        "title": "403: v1.0.0 リリース作業（version固定・CHANGELOG・README整備）",
        "milestone": "M5: QA & Release（校正・品質ゲート・v1.0）",
        "labels": ["type/qa", "prio/P1"],
        "body": md(
            """
            ## 目的
            完成版として参照可能な固定点（v1.0.0）を作る。

            ## 作業
            - [ ] `version` を v1.0.0 に固定（設定/サイト表示）
            - [ ] CHANGELOG を作成（主要変更、破壊的変更の扱い）
            - [ ] README に「この本の読み方」「対象読者」「成果物テンプレ導線」を整理
            - [ ] 公開URLの最終確認

            ## 完了条件（DoD）
            - [ ] v1.0.0 としてタグ/リリースが作成されている（運用方針に従う）
            """
        ),
    },
    {
        "title": "404: フィードバック導線（Errata/Discussion/Issueテンプレ）整備",
        "milestone": "M5: QA & Release（校正・品質ゲート・v1.0）",
        "labels": ["type/setup", "type/qa", "prio/P2"],
        "body": md(
            """
            ## 目的
            公開後の改善をIssuesで回せる導線を用意する。

            ## 作業
            - [ ] 誤植報告テンプレ（.github/ISSUE_TEMPLATE/）
            - [ ] 技術的指摘テンプレ（再現手順/根拠/提案）
            - [ ] 質問テンプレ（どこが分からないかを特定させる）
            - [ ] （任意）Discussions を有効化し、質問/議論の場所を分離

            ## 完了条件（DoD）
            - [ ] フィードバックが一定の形式で集まり、対応がトラックできる
            """
        ),
    },
]


# -----------------------------
# Implementation
# -----------------------------

@dataclass(frozen=True)
class Repo:
    owner: str
    name: str

    @property
    def full(self) -> str:
        return f"{self.owner}/{self.name}"


def _run(cmd: Sequence[str], *, input_text: Optional[str] = None, capture: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(
        list(cmd),
        input=input_text,
        text=True,
        capture_output=capture,
        check=False,
        encoding="utf-8",
    )


def _require_gh() -> None:
    res = _run(["gh", "--version"])
    if res.returncode != 0:
        print("ERROR: GitHub CLI (gh) が見つかりません。gh をインストールしてください。", file=sys.stderr)
        sys.exit(1)


def _get_repo_from_gh() -> str:
    res = _run(["gh", "repo", "view", "--json", "nameWithOwner", "--jq", ".nameWithOwner"])
    if res.returncode != 0:
        msg = (res.stderr or res.stdout or "").strip()
        raise RuntimeError(f"gh repo view failed. {msg}")
    return res.stdout.strip()


def _parse_repo(repo_full: str) -> Repo:
    if "/" not in repo_full:
        raise ValueError(f"--repo は owner/repo 形式で指定してください: {repo_full}")
    owner, name = repo_full.split("/", 1)
    owner = owner.strip()
    name = name.strip()
    if not owner or not name:
        raise ValueError(f"--repo が不正です: {repo_full}")
    return Repo(owner=owner, name=name)


def _list_existing_labels(repo: Repo) -> Set[str]:
    res = _run(["gh", "api", f"repos/{repo.owner}/{repo.name}/labels", "--paginate", "--jq", ".[].name"])
    if res.returncode != 0:
        return set()
    return {line.strip() for line in res.stdout.splitlines() if line.strip()}


def _list_existing_milestones(repo: Repo) -> Set[str]:
    res = _run(["gh", "api", f"repos/{repo.owner}/{repo.name}/milestones", "--paginate", "--jq", ".[].title"])
    if res.returncode != 0:
        return set()
    return {line.strip() for line in res.stdout.splitlines() if line.strip()}


def _list_existing_issue_titles(repo: Repo) -> Set[str]:
    res = _run(
        ["gh", "issue", "list", "--repo", repo.full, "--state", "all", "--limit", "500", "--json", "title", "--jq", ".[].title"]
    )
    if res.returncode != 0:
        return set()
    return {line.strip() for line in res.stdout.splitlines() if line.strip()}


def ensure_labels(repo: Repo, *, dry_run: bool) -> None:
    existing = _list_existing_labels(repo)
    for lbl in LABELS:
        name = lbl["name"]
        if name in existing:
            continue
        cmd = [
            "gh",
            "api",
            "-X",
            "POST",
            f"repos/{repo.owner}/{repo.name}/labels",
            "-f",
            f"name={name}",
            "-f",
            f"color={lbl['color']}",
            "-f",
            f"description={lbl['description']}",
        ]
        if dry_run:
            print(f"[dry-run] create label: {name}")
            continue
        res = _run(cmd)
        if res.returncode != 0:
            err = (res.stderr or res.stdout or "").lower()
            if "already exists" in err or "validation failed" in err:
                continue
            raise RuntimeError(f"Failed to create label '{name}': {(res.stderr or res.stdout).strip()}")


def ensure_milestones(repo: Repo, *, dry_run: bool) -> None:
    existing = _list_existing_milestones(repo)
    for ms in MILESTONES:
        title = ms["title"]
        if title in existing:
            continue
        cmd = [
            "gh",
            "api",
            "-X",
            "POST",
            f"repos/{repo.owner}/{repo.name}/milestones",
            "-f",
            f"title={title}",
            "-f",
            f"description={ms.get('description','')}",
        ]
        if dry_run:
            print(f"[dry-run] create milestone: {title}")
            continue
        res = _run(cmd)
        if res.returncode != 0:
            err = (res.stderr or res.stdout or "").lower()
            if "already exists" in err or "validation failed" in err:
                continue
            raise RuntimeError(f"Failed to create milestone '{title}': {(res.stderr or res.stdout).strip()}")


def create_issues(repo: Repo, *, dry_run: bool, skip_existing: bool) -> None:
    existing_titles = _list_existing_issue_titles(repo) if skip_existing else set()

    for issue in ISSUES:
        title = issue["title"]
        if skip_existing and title in existing_titles:
            print(f"[skip] {title}")
            continue

        if dry_run:
            print(f"[dry-run] create issue: {title}  (milestone={issue['milestone']}, labels={issue['labels']})")
            continue

        body = issue["body"].rstrip() + "\n"
        with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8", newline="\n") as f:
            f.write(body)
            body_path = f.name

        try:
            cmd: List[str] = [
                "gh",
                "issue",
                "create",
                "--repo",
                repo.full,
                "--title",
                title,
                "--body-file",
                body_path,
                "--milestone",
                issue["milestone"],
            ]
            for lbl in issue["labels"]:
                cmd.extend(["--label", lbl])

            res = _run(cmd)
            if res.returncode != 0:
                raise RuntimeError(f"Failed to create issue '{title}': {(res.stderr or res.stdout).strip()}")

            url = (res.stdout or "").strip()
            print(f"[created] {title}\n  {url}")
        finally:
            try:
                os.unlink(body_path)
            except OSError:
                pass


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", help="owner/repo. 省略時は `gh repo view` から取得")
    parser.add_argument("--dry-run", action="store_true", help="作成せずに計画を表示")
    parser.add_argument("--no-skip-existing", action="store_true", help="同名タイトルがあっても作成（重複作成）")
    args = parser.parse_args(argv)

    _require_gh()

    repo_full = args.repo
    if not repo_full:
        try:
            repo_full = _get_repo_from_gh()
        except Exception as e:
            print(f"ERROR: リポジトリが特定できません。--repo owner/repo を指定してください。\n{e}", file=sys.stderr)
            return 1

    repo = _parse_repo(repo_full)
    skip_existing = not args.no_skip_existing

    print(f"Target repo: {repo.full}")
    if args.dry_run:
        print("Mode: dry-run (no changes)\n")

    try:
        ensure_labels(repo, dry_run=args.dry_run)
        ensure_milestones(repo, dry_run=args.dry_run)
        create_issues(repo, dry_run=args.dry_run, skip_existing=skip_existing)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
