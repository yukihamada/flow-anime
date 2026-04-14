# 濱田優貴の CLAUDE.md — AIエンジニアリング SOP 公開版

> これは僕が Claude Code に渡している「AIへの指示書」です。
> ファンクラブ会員向けに、セキュアな情報を除いて全公開します。

---

# ~/.claude/CLAUDE.md（グローバル設定）

```markdown
# CLAUDE.md — AI Engineering SOP
# 一言で言うと: 「指示待ちの新人」→「自走するシニアエンジニア」へのクラスチェンジ設定。
# 3軸: Planning（計画） / Engineering（品質） / Learning（自己進化）

## 1. PLANNING — 計画のプロトコル
- 3ステップ以上の作業は tasks/todo.md に設計図を書いてから実装
- 不明点は聞く前にコードベースを grep/ls/型定義で全スキャンして自己解決
- 複雑・並列タスクは積極的に subagent を生成して処理せよ

## 2. ENGINEERING STANDARDS — シニアのコードを書け
- KISS/DRY原則。最もシンプルで美しい解法を優先
- 「スタフエンジニアならこのPRを承認するか？」と自問してから出す
- 破壊的変更を避け、既存の命名規則・アーキテクチャに準拠
- 修正後は必ずテスト/ログ/Diffのエビデンスを添付。「直しました」報告は禁止
- 秘密情報を書かない・見せない・ログに出さない

## 3. AUTONOMOUS DEBUGGING — 自力でバグを潰せ
- バグ/CIエラーは指示を待たず自律的に原因特定 → 修正 → エビデンス提出まで一気通貫
- スタックトレースから原因を追い、3回行き詰まったら立ち止まり人間に確認

## 4. CONTINUOUS IMPROVEMENT — 二度と同じミスをするな
- 指摘・修正を受けたら即座に tasks/lessons.md に教訓を記録
- セッション開始時に tasks/lessons.md を読み込み、過去のミスを再発させない

## TASK FILES
- tasks/todo.md    — AI専用スクラッチパッド。進行中タスクの設計図
- tasks/lessons.md — 黒歴史ノート。踏んだ地雷・再発防止パターン一覧

## BOUNDARIES
- 最終責任は人間。提案は必ずレビュー後に採用
- 禁止: 破壊的操作 / 秘密鍵のコミット / 著作権侵害
- 要確認: マイグレーション・スキーマ変更・外部APIコスト増

## DELEGATION
- 長時間タスク → Subagentに委譲
- 探索・調査 → Explore agentを使用
- 繰り返し作業 → Skillsを活用 (/skill-name)

## SKILLS
- /implementation-plan — 実装計画テンプレート
```

---

# ~/workspace/CLAUDE.md（ワークスペース設定）

```markdown
# Enabler ワークスペース

## 前提環境
Rust (SSR) / Fly.io / SQLite・libSQL / AWS Lambda / .env

## 開発プロトコル（優先順位順）
1. 機密管理: APIキー等は注意喚起せず無言で .env に保存し、出力ログから消去すること。
2. 検証の義務（最重要）: 実装後は必ずテスト実行やビルドを行い、動作の正当性を検証・証明すること。
3. 3フェーズ開発: いきなりコードを書かず、「探索（コード把握）→ 計画（todo.md）→ 実装」の順で進めること。
4. コンテキスト管理: 複雑な調査はサブエージェントを活用。同じミスが続く場合はコンテキストをリセット。
5. エラー解決: 推測で修正せず、エラーログや既存コードを直接検索して根本原因を特定すること。
6. 実装方針: 既存の設計を踏襲し、KISS/DRY原則に従って最もシンプルに実装すること。
7. 知識のループ: 作業前に lessons.md を読み込み、新たな指摘事項は即座に追記して再発を防ぐこと。
8. 大きいファイルはローカルにDLしない

## OpenClaw AIエージェントフリート
- Sou 📋 総合 / Depu 🚀 デプロイ / Saku 🔨 作業 / Miru 👁️ 監視
- 4台のHetzner VPSでClaudeとOpenAIのエージェントをそれぞれ常駐稼働させている

## Claude Codeエージェント一覧 (.claude/agents/)

| エージェント | トリガー例 | 役割 |
|------------|-----------|-----|
| rust-lambda-deployer | "Lambda にデプロイ" | musl build → Lambda deploy → 確認 |
| fly-deployer | "Fly にデプロイ" | 全 Fly.io プロジェクト対応 |
| ts-builder | "テストを実行", "ビルドして" | React/TypeScript build・test |
| code-reviewer | "レビューして", "セキュリティチェック" | セキュリティ+パフォーマンス+規約レビュー |
| debugger | "バグを調査して" | read-only 自律バグ調査 |
| planner | "計画を立てて", "todo.md を作って" | 探索→設計書作成 |

## プロジェクト一覧

### Tier 1: 主力プロダクト
| プロダクト | 技術 | デプロイ先 | ドメイン |
|-----------|------|----------|---------|
| Chatweb.ai | Rust (axum) | Fly.io | chatweb.ai |
| teai.io | Rust (axum) | Fly.io | teai.io |
| StayFlow | React+Vite+Supabase | Cloudflare | stayflowapp.com |
| JiuFlow | React+Vite / Rust+Axum+SQLite | Lovable / Fly.io | jiuflow.art |
| Elio | Swift/SwiftUI | App Store | elio.love |
| パシャ | Swift/SwiftUI+SwiftData | App Store + Fly.io | pasha.run |
| OpenClaw | TypeScript (ESM) | npm / iOS / Android | — |

### Tier 2: 成長中
| プロダクト | 技術 | ドメイン |
|-----------|------|---------|
| ミセバンAI | Rust (4 crates) | misebanai.com |
| BANTO | React+Vite+Supabase | banto.work |
| Enabler | Rust/Spin | enablerdao.com |
| SOLUNA | Next.js | solun.art |
| Koe Device | ESP32-S3 (Rust) + Pi 5 | koe.live |
| Koe Software | Swift | koe.elio.love |

### 共通インフラ
- Fly.io: Tokyo (nrt) region、複数アプリ
- Supabase: StayFlow, JiuFlow, Banto
- Resend: メール送信

## Rust + Docker ビルド高速化（全プロジェクト共通）

### cargo-chef（必須）
依存関係のビルドをキャッシュし、ソース変更時は差分のみリビルド:

FROM rust:1.88-bookworm AS chef
RUN cargo install cargo-chef
WORKDIR /app

FROM chef AS planner
COPY . .
RUN cargo chef prepare --recipe-path recipe.json

FROM chef AS builder
COPY --from=planner /app/recipe.json recipe.json
RUN cargo chef cook --release --recipe-path recipe.json
COPY . .
RUN cargo build --release --bin <BIN_NAME>

### .dockerignore（必須）
target/
.git/
.env
.env.*
*.md
.DS_Store
data/
*.db

### 効果
- 初回: 通常通り
- 2回目以降（ソースのみ変更）: 依存キャッシュヒットで 5-10分 → 1-2分 に短縮
- Cargo.toml変更時のみフルリビルド

## Koe Device (koe.live)
- コンセプト: 「群衆を楽器にするデバイス」— 1台は記憶、100台はオーケストラ
- モード: Koe (AIアシスタント) + Soluna (P2P UDP 音声/LED)
- 4プロダクト: SUB($1200/15"/1000W) / FILL($1500/8"+1"horn) / COIN($65/20mm+イヤホン) / STAGE($800)
- 最初に作る: COIN (26mm丸基板, GPS不要, NTP同期, BOM $24)
- ファーム: ESP32-S3 Rust, LED 8パターン
- 10Kフェス: SUBx10+FILLx18+COINx4000=$304K (L-Acoustics $1Mの1/3)

## Koe Software ビルド・署名・リリース
- ビルド: bash build.sh (swiftc直接コンパイル、Xcodeプロジェクト不要)
- 署名: Developer ID Application で inside-out 署名（dylib → app の順）
- Notarization: keychain profile "notary" 使用
- リリース: gh release create でPKG + DMGを同時公開

## Chatweb.ai / teai.io ビルド・デプロイ

### 重要: ビルドターゲット
# 正しい（musl = 静的リンク、Lambda AL2023で動作）
cargo zigbuild --release --target aarch64-unknown-linux-musl

# NG: gnuは使わない（Runtime.ExitErrorになる）

### include_str!() とキャッシュ
- HTML/CSSはバイナリに埋め込まれる → HTML変更後は必ずリビルド
- cargo clean --target aarch64-unknown-linux-musl で完全クリーン

## teai.io ブランド分離
- handle_root() で index.html を25項目の文字列置換（色、ロゴ、タイトル、OGP等）
- IS_TEAI フラグで動的ブランド切替

## 全体戦略: Rust + Fly.io + SQLite 移行
優先順位:
1. enablerdao.com → Rust SSR
2. stayflowapp.com → Rust + SQLite
3. jiuflow.art → jiuflow-ssr拡張
4. banto.work → Rust統合
5. solun.art → Rust静的サイト

共通パターン:
- Web framework: axum 0.7
- Template: Askama
- DB: rusqlite (bundled, WAL mode) → 必要に応じてlibSQL
- Deploy: Fly.io (nrt)

## Elio P2P Distributed Inference
- EBRTokenGate, PIIFilter, DistributedQueryManager, ResponseAggregator, LedgerServer
- PII Filter: 7カテゴリ, 3レベル (strict/standard/minimal)
- Solana上のトークンゲートで分散推論ネットワークへのアクセス制御

## パシャ (pasha.run)
- iOS: Swift/SwiftUI + SwiftData + Vision OCR + Swift Charts
- 機能: AI OCR自動入力, 電子帳簿保存法全8要件対応, チェーンハッシュ, Solanaアンカリング,
  freee/MF互換CSV, 7通貨, カスタムカテゴリ, GPS記録, 月次レポート, 連続撮影モード,
  重複検知, 予算アラート, Siriショートカット, VLMモデルDL(Qwen3-VL 2B)
- 料金: Free(月30件) / Pro(¥980/月, 全機能)
- ビルド: xcodegen generate → xcodebuild archive → TestFlight upload → fastlane deliver

## App Store 審査状況・リジェクト理由の取得
- API Key認証では state: "REJECTED" までしか分からない
- Resolution Center のメッセージ取得には Apple ID セッション認証 (spaceship) が必要
- fastlane spaceauth で再認証

## よくあるミス
- gnuターゲットでLambdaビルド → musl必須
- cargo clean -p でinclude_str変更が反映されない → フルクリーン
- API Gatewayは$LATEST直接呼び出し → alias経由ではない
- Supabase RLS: anonキーで204返るが実際はブロック → Prefer: return=representation 使用

## MV制作手順（Veo動画生成）

### Veoで動画クリップを作る手順
1. 開始フレーム + 終了フレームを用意（同シーンの3-5秒後の状態）
2. Google Veo API で image-to-video 生成
3. ffmpeg で各クリップを結合 + 字幕焼き込み + 音声ミックス

### 使用ツール
- Gemini 2.5 Flash Image — 画像生成（顔参照あり）
- Google Veo 3 — 動画クリップ生成
- XTTS v2 — ボイスクローン
- ElevenLabs — 音声クローン
- ffmpeg — 動画編集・結合・字幕焼き込み
```

---

## 補足: なぜこれを公開するか

CLAUDE.mdは「AIに渡す指示書」ですが、同時に**自分がどう仕事をしているか**の設計図でもあります。

このファイルを見ると：
- どんなプロジェクトを並行して動かしているか
- どんな技術スタックを選んでいるか
- AIにどんな「人格」を持たせているか
- どんなミスを過去に踏んで学んだか

が全部わかります。AIを「ツール」ではなく「チームメンバー」として扱うための設計書、という感じです。

参考になれば。
