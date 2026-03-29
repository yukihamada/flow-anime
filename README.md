# FLOW — 柔術 x AI アニメ

<div align="center">

<img src="images/og_image.png" width="700">

**「もし柔術に、専用のアニメがあったら？」**

[flow-anime.com](https://flow-anime.com) | [@flow_bjj](https://x.com/flow_bjj) | [Opening](https://flow-anime.com/opening.html) | [Feedback](https://flow-anime.com/rpg.html)

</div>

---

## なぜ作ったか

柔術はすごい。

年齢も体格も関係ない。50歳から始めても、片腕でも、強くなれる。殴り合いじゃないから安全で、一生続けられる。道場に行けば、国籍も職業もバラバラな人たちが畳の上で笑ってる。

**この面白さを、もっと多くの人に知ってほしい。**

でも「柔術って何？」って聞かれて、言葉で説明しても伝わらない。
「寝技の格闘技で...」「いや、総合格闘技とは違って...」「グレイシーっていう一族が...」

だったら、**アニメにすればいいじゃん。**

ワンピースが海賊を、スラムダンクがバスケを広めたように。
柔術の「あの感覚」—— エビが少しうまくなった日、初めてスイープが決まった日、先生の「もう一回」 —— をアニメにしたら、世界中の人が柔術を始めるかもしれない。

それが FLOW です。

## どんな話？

> **2030年。AIが格闘技を支配する時代。**
> 予測精度99.8%のAI「SAGE」が全ての試合を解析する。
> 選手はAIの指示通りに動く。人間の意志は形骸化した。
>
> 左腕が壊れた17歳の少年 **流（ながれ）** は、
> AIに読めない唯一の武器 —— **"フロウ"** で世界の頂点を目指す。

| | |
|---|---|
| エピソード | 全60話・5シーズン |
| テーマ | 人間の直感 vs 機械の最適解 |
| 音楽 | OP「0.2%の証明」/ ED「もう一回」(JP/EN/PT) |
| 技 | 全試合に実在するBJJ技名を使用 |

<div align="center">
<img src="images/characters/nagare_sheet_v2.png" width="150"><img src="images/characters/rio_sheet.png" width="150"><img src="images/characters/marcelo_sheet.png" width="150"><img src="images/characters/rin_sheet.png" width="150"><img src="images/characters/sage_sheet.png" width="150">

*流 / 理央 / ルシアーノ / 凛 / SAGE*
</div>

## みんなで作るアニメ

**FLOW はオープンプロジェクトです。**

脚本、キャラデザ、音楽、世界観設定 —— 全部このリポジトリにあります。
企画書じゃなくて、**生きたプロジェクト**。

柔術をやってる人、アニメが好きな人、音楽を作れる人、絵が描ける人。
「こうしたら面白くない？」があれば、どんどん取り込んでいきたい。

### 参加の仕方

| やりたいこと | 方法 |
|---|---|
| 感想・フィードバック | [flow-anime.com/rpg.html](https://flow-anime.com/rpg.html) から送信 |
| 技の監修 | 「この技の描写おかしいよ」→ Issue を立てる |
| ストーリー案 | 「こんな展開が見たい」→ Issue or PR |
| キャラ案 | 新キャラのアイデア → Issue |
| 音楽 | OPやED、挿入歌の案 → PR |
| イラスト | シーンやキャラのイラスト → PR |
| 翻訳 | 英語・ポルトガル語・その他 → PR |
| コード | サイト改善、新機能 → PR |

**貢献はポイントとして記録されます。** FLOW が形になったとき、貢献した人にクレジット掲載・限定コンテンツ・収益還元を予定しています。

## リポジトリ構成

```
flow-anime/
  index.html          # トップページ（3言語対応）
  opening.html        # OP映像 + 全60話 + ED
  review.html         # レビュー＆投票
  rpg.html            # RPGメンバー向けフィードバック
  pitch.html          # 企画書
  server.py           # Python サーバー（アナリティクス + X投稿）
  story/
    series_bible.md    # シリーズバイブル（世界観・キャラ・設定）
    episode_guide_s1-5.md  # 全60話のエピソードガイド
  music/
    op_new.mp3         # OP「0.2%の証明」(日本語)
    op_en.mp3          # OP (English)
    op_pt.mp3          # OP (Portugues)
    ed_new.mp3         # ED「もう一回」(日本語)
    ed_en.mp3          # ED (English)
    ed_pt.mp3          # ED (Portugues)
    songs.md           # 全曲歌詞
  images/
    characters/        # キャラクターデザインシート
    keyvisual/         # キービジュアル
    scenes/            # シーンコンセプトアート
    flow_art/          # フロウシステムアート
    op_scenes/         # OP用シーン画像（10場面 x 3パターン）
  scripts/             # 画像生成・投稿スクリプト
```

## 技術スタック

- **サイト**: HTML/CSS/JS（フレームワークなし、軽量）
- **サーバー**: Python + SQLite（アナリティクス・メール登録・フィードバック）
- **デプロイ**: Fly.io (Tokyo region)
- **画像生成**: Gemini 3 Pro Image
- **音楽**: Suno AI
- **ストーリー**: Claude + 柔術経験者の監修
- **ドメイン**: [flow-anime.com](https://flow-anime.com)

## ローカルで動かす

```bash
git clone https://github.com/yukihamada/flow-anime.git
cd flow-anime
python3 server.py
# http://localhost:8080 で開く
```

## 柔術やったことない人へ

この README を読んで少しでも気になったら、近くの道場の体験クラスに行ってみてください。

「エビ」っていう地味な動きを延々やらされます。
帰り道、全身が筋肉痛です。
でも次の日、なぜかまた行きたくなります。

先生が言います。「もう一回」。

---

<div align="center">

**流れる水は、終わらない。**

<sub>監修: 村田良蔵 | 制作: 濱田優貴 | Built with Claude Code + Gemini + Suno</sub>

</div>
