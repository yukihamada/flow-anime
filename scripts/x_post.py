#!/usr/bin/env python3
"""FLOW — X (Twitter) auto-poster with image support.

Usage:
  python3 x_post.py post "ツイートの本文" [image_path]
  python3 x_post.py schedule              # Run all scheduled posts
  python3 x_post.py test                  # Test connection
  python3 x_post.py delete <tweet_id>     # Delete a tweet
"""

import os, sys, json, time
from pathlib import Path
from datetime import datetime, timedelta

# Load env
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    for line in env_path.read_text().splitlines():
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

import tweepy

def get_client():
    """Get authenticated X API v2 client."""
    return tweepy.Client(
        consumer_key=os.environ["X_API_KEY"],
        consumer_secret=os.environ["X_API_SECRET"],
        access_token=os.environ["X_ACCESS_TOKEN"],
        access_token_secret=os.environ["X_ACCESS_TOKEN_SECRET"],
    )

def get_api_v1():
    """Get v1.1 API for media uploads."""
    auth = tweepy.OAuth1UserHandler(
        os.environ["X_API_KEY"],
        os.environ["X_API_SECRET"],
        os.environ["X_ACCESS_TOKEN"],
        os.environ["X_ACCESS_TOKEN_SECRET"],
    )
    return tweepy.API(auth)

def upload_media(image_path):
    """Upload an image and return media_id."""
    api = get_api_v1()
    media = api.media_upload(str(image_path))
    print(f"  Media uploaded: {media.media_id}")
    return media.media_id

def post_tweet(text, image_path=None):
    """Post a tweet, optionally with an image."""
    client = get_client()
    media_ids = None
    if image_path and Path(image_path).exists():
        mid = upload_media(image_path)
        media_ids = [mid]

    response = client.create_tweet(text=text, media_ids=media_ids)
    tweet_id = response.data["id"]
    print(f"  Posted: https://x.com/i/web/status/{tweet_id}")
    return tweet_id

def delete_tweet(tweet_id):
    """Delete a tweet."""
    client = get_client()
    client.delete_tweet(tweet_id)
    print(f"  Deleted: {tweet_id}")

def test_connection():
    """Test API connection."""
    client = get_client()
    me = client.get_me()
    print(f"  Connected as: @{me.data.username} ({me.data.name})")
    print(f"  ID: {me.data.id}")

# ============ SCHEDULED POSTS ============
BASE = Path(__file__).parent.parent
SCHEDULE_FILE = BASE / "promo" / "post_schedule.json"
POSTED_FILE = BASE / "promo" / "posted.json"

def load_schedule():
    """Load or create the posting schedule."""
    if SCHEDULE_FILE.exists():
        return json.loads(SCHEDULE_FILE.read_text())

    # Generate from the promo plan
    img = lambda p: str(BASE / p)
    posts = [
        {
            "id": "teaser",
            "text": "もし柔術に専用のアニメがあったら——\n\nAIが全ての格闘技を解析した2030年。\n「予測不能」だけが武器の少年がいる。\n\nFLOW、始動。\n\n#柔術 #BJJ #FLOW",
            "image": img("images/keyvisual/kv_themat.png"),
            "day": 1, "hour": 12
        },
        {
            "id": "nagare",
            "text": "流（ながれ）— 17歳。\n\n5歳の事故で左腕の感覚を失った。\n師匠は2年前に消えた。\n残されたのは1本の黒帯と「流れに乗れ」という言葉だけ。\n\n左腕の黒い包帯は、壊れた自分を隠すためじゃない。\n受け入れた証だ。\n\n#FLOW #柔術アニメ",
            "image": img("images/characters/nagare_sheet_v2.png"),
            "day": 1, "hour": 19
        },
        {
            "id": "music",
            "text": "柔術アニメのオープニングを作りました。\n\n「水面の下で 流れが始まる\n AIが叫ぶ ERROR ERROR\n 壊れた身体で 完璧を超えろ\n これが俺の柔術だ」\n\n▶ 音楽+映像付きで体験:\nhttps://flow-anime.fly.dev/opening.html\n\n#FLOW #アニメOP",
            "image": img("images/keyvisual/kv_main.png"),
            "day": 2, "hour": 12
        },
        {
            "id": "rio",
            "text": "理央（りお）— 18歳。SAGE社のエース。\n\n「感覚？ そんな曖昧なものに命を預けるのか」\n\nAIの最適解に従う完璧な柔術。\nしかしある日、イヤピースを外す——\n\n#FLOW #柔術アニメ",
            "image": img("images/characters/rio_sheet.png"),
            "day": 3, "hour": 19
        },
        {
            "id": "rin",
            "text": "凛（りん）— 19歳。「蜘蛛」の異名。\n\n足関節の天才。\nAIを使わない理由？\n\n「つまらないから。」\n\n#FLOW #柔術アニメ #BJJ",
            "image": img("images/scenes/scene_ep6_rin_spider.png"),
            "day": 4, "hour": 12
        },
        {
            "id": "flow_system",
            "text": "FLOW SYSTEM — 4段階の覚醒レベル\n\n滴（しずく）→ 一瞬だけAI予測を外す\n流（ながれ）→ 技が水のように連続する\n渦（うず）→ 相手も巻き込む。全AI停止\n海（うみ）→ 師匠だけが到達した未知の領域\n\n代償は——左腕の感覚。\n\n#FLOW #柔術アニメ",
            "image": img("images/flow_art/flow_lv3_uzu.png"),
            "day": 5, "hour": 19
        },
        {
            "id": "sage_ui",
            "text": "2030年の柔術試合。\n\n観客はAI予測画面を見ている。\n「サブミッション確率 87.3%」\n「予測: FIGHTER A 勝利」\n\nしかしフロウが発動すると——\n全画面が「ERR」に染まる。\n\n#FLOW #柔術アニメ",
            "image": img("images/sage_ui/sage_ui_glitch.png"),
            "day": 6, "hour": 12
        },
        {
            "id": "ending",
            "text": "FLOW エンディング「帰り道」\n\n「帰り道はいつも同じ\n でも昨日の僕とは違う\n エビひとつ まだ下手だけど\n 先生の『もう一回』が聞こえる」\n\n柔術やってる人なら、わかると思う。\n\n#FLOW #柔術 #BJJ",
            "image": img("images/keyvisual/kv_themat.png"),
            "day": 7, "hour": 19
        },
        {
            "id": "feedback",
            "text": "FLOWを見てくれた方へ。\n\n率直な感想を聞かせてください。\n・どのキャラが好き？\n・どのシーズンが一番見たい？\n・技の描写は正確？\n\n柔術やってる人の声が、この作品を本物にします。\n\n▶ https://flow-anime.fly.dev/opening.html\n\n#FLOW #柔術",
            "image": None,
            "day": 7, "hour": 21
        },
        {
            "id": "en_launch",
            "text": "What if Brazilian Jiu-Jitsu had its own anime?\n\nFLOW — a world where AI controls fighting.\nOne boy with a broken arm fights with something AI can't predict.\n\n60 episodes. Original soundtrack. Real BJJ techniques in every fight.\n\n▶ https://flow-anime.fly.dev/opening.html\n\n#BJJ #anime #FLOW",
            "image": img("images/keyvisual/kv_main.png"),
            "day": 8, "hour": 9
        },
    ]

    SCHEDULE_FILE.parent.mkdir(parents=True, exist_ok=True)
    SCHEDULE_FILE.write_text(json.dumps(posts, ensure_ascii=False, indent=2))
    print(f"  Schedule created: {SCHEDULE_FILE}")
    return posts

def run_schedule():
    """Post all scheduled tweets that are due."""
    posts = load_schedule()
    posted = json.loads(POSTED_FILE.read_text()) if POSTED_FILE.exists() else {}

    for post in posts:
        pid = post["id"]
        if pid in posted:
            print(f"  [skip] {pid} — already posted")
            continue

        print(f"\n  [post] {pid}")
        print(f"  Text: {post['text'][:60]}...")
        try:
            tweet_id = post_tweet(post["text"], post.get("image"))
            posted[pid] = {"tweet_id": tweet_id, "posted_at": datetime.now().isoformat()}
            POSTED_FILE.write_text(json.dumps(posted, ensure_ascii=False, indent=2))
            time.sleep(3)  # Rate limit
        except Exception as e:
            print(f"  [err] {pid}: {e}")
            break  # Stop on error

    print(f"\n  Posted: {len(posted)}/{len(posts)}")

# ============ CLI ============
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "test":
        test_connection()
    elif cmd == "post":
        text = sys.argv[2] if len(sys.argv) > 2 else input("Tweet text: ")
        image = sys.argv[3] if len(sys.argv) > 3 else None
        post_tweet(text, image)
    elif cmd == "delete":
        delete_tweet(sys.argv[2])
    elif cmd == "schedule":
        run_schedule()
    elif cmd == "preview":
        posts = load_schedule()
        for p in posts:
            print(f"\n--- Day {p['day']} {p['hour']}:00 [{p['id']}] ---")
            print(p["text"][:100] + ("..." if len(p["text"]) > 100 else ""))
            if p.get("image"): print(f"  📎 {Path(p['image']).name}")
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
