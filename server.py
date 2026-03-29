#!/usr/bin/env python3
"""FLOW Server — static files + analytics + X auto-poster with cron."""
import json, os, sqlite3, time, hashlib, uuid, threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from datetime import datetime, timezone, timedelta

DB_PATH = "/data/analytics.db" if os.path.exists("/data") else "analytics.db"
PORT = int(os.environ.get("PORT", 8080))
DASH_KEY = os.environ.get("DASH_KEY", "flow2026")
STATIC_DIR = os.environ.get("STATIC_DIR", "/app")
SCHEDULE_PATH = os.path.join(STATIC_DIR, "promo", "post_schedule.json")
POST_LOG_PATH = os.path.join(DB_PATH.rsplit("/",1)[0] if "/" in DB_PATH else ".", "post_log.json")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ts TEXT DEFAULT (datetime('now')),
        path TEXT,
        event TEXT DEFAULT 'pageview',
        uid TEXT,
        ref TEXT,
        ua TEXT,
        ip_hash TEXT,
        data TEXT
    )""")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_ts ON events(ts)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_path ON events(path)")
    conn.execute("""CREATE TABLE IF NOT EXISTS subscribers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        lang TEXT DEFAULT 'ja',
        ts TEXT DEFAULT (datetime('now')),
        source TEXT DEFAULT 'website'
    )""")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_sub_email ON subscribers(email)")
    conn.commit()
    conn.close()

def log_event(path, event, uid, ref, ua, ip, data=None):
    ip_hash = hashlib.sha256((ip or "unknown").encode()).hexdigest()[:16]
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT INTO events (path, event, uid, ref, ua, ip_hash, data) VALUES (?,?,?,?,?,?,?)",
                 (path, event, uid, ref, ua[:200] if ua else "", ip_hash, json.dumps(data) if data else None))
    conn.commit()
    conn.close()

def get_stats(hours=24):
    conn = sqlite3.connect(DB_PATH)
    since = (datetime.now(timezone.utc) - timedelta(hours=hours)).strftime("%Y-%m-%d %H:%M:%S")
    all_time_since = "2020-01-01"

    # Total pageviews (all time)
    total_pv = conn.execute("SELECT COUNT(*) FROM events WHERE event='pageview'").fetchone()[0]
    # Unique visitors (all time)
    total_uv = conn.execute("SELECT COUNT(DISTINCT ip_hash) FROM events WHERE event='pageview'").fetchone()[0]
    # Pageviews last N hours
    recent_pv = conn.execute("SELECT COUNT(*) FROM events WHERE event='pageview' AND ts>=?", (since,)).fetchone()[0]
    recent_uv = conn.execute("SELECT COUNT(DISTINCT ip_hash) FROM events WHERE event='pageview' AND ts>=?", (since,)).fetchone()[0]

    # Top pages
    top_pages = conn.execute("""SELECT path, COUNT(*) as c, COUNT(DISTINCT ip_hash) as u
        FROM events WHERE event='pageview' GROUP BY path ORDER BY c DESC LIMIT 10""").fetchall()

    # Hourly trend (last 48 hours)
    trend_since = (datetime.now(timezone.utc) - timedelta(hours=48)).strftime("%Y-%m-%d %H:%M:%S")
    hourly = conn.execute("""SELECT strftime('%Y-%m-%d %H:00', ts) as hour, COUNT(*) as c, COUNT(DISTINCT ip_hash) as u
        FROM events WHERE event='pageview' AND ts>=? GROUP BY hour ORDER BY hour""", (trend_since,)).fetchall()

    # Custom events (votes, feedback, etc.)
    custom = conn.execute("""SELECT event, COUNT(*) as c FROM events WHERE event!='pageview' GROUP BY event ORDER BY c DESC""").fetchall()

    # Feedback data
    feedback = conn.execute("""SELECT data FROM events WHERE event='feedback' ORDER BY ts DESC LIMIT 50""").fetchall()
    votes = conn.execute("""SELECT data FROM events WHERE event='vote' ORDER BY ts DESC LIMIT 100""").fetchall()

    # Referrers
    refs = conn.execute("""SELECT ref, COUNT(*) as c FROM events WHERE ref!='' AND ref IS NOT NULL
        GROUP BY ref ORDER BY c DESC LIMIT 10""").fetchall()

    # Recent events
    recent = conn.execute("""SELECT ts, path, event, data FROM events ORDER BY ts DESC LIMIT 30""").fetchall()

    # Duration / dwell time stats
    duration_rows = conn.execute("""SELECT data FROM events WHERE event='duration' AND ts>=?""", (since,)).fetchall()
    durations = []
    for row in duration_rows:
        try:
            d = json.loads(row[0]) if row[0] else {}
            s = d.get("seconds", 0)
            if 0 < s < 3600:  # filter outliers
                durations.append(s)
        except Exception:
            pass
    avg_duration = round(sum(durations) / len(durations), 1) if durations else 0
    total_duration_events = len(durations)

    # Duration by page
    dur_by_page_rows = conn.execute("""SELECT path, data FROM events WHERE event='duration' AND ts>=?""", (since,)).fetchall()
    page_durations = {}
    for path, data_str in dur_by_page_rows:
        try:
            d = json.loads(data_str) if data_str else {}
            s = d.get("seconds", 0)
            if 0 < s < 3600:
                if path not in page_durations:
                    page_durations[path] = []
                page_durations[path].append(s)
        except Exception:
            pass
    duration_by_page = [
        {"path": p, "avg": round(sum(ds)/len(ds), 1), "count": len(ds)}
        for p, ds in sorted(page_durations.items(), key=lambda x: sum(x[1])/len(x[1]), reverse=True)
    ]

    # Duration distribution (buckets: 0-10s, 10-30s, 30-60s, 60-180s, 180s+)
    dur_buckets = {"0-10s": 0, "10-30s": 0, "30-60s": 0, "1-3min": 0, "3min+": 0}
    for s in durations:
        if s <= 10: dur_buckets["0-10s"] += 1
        elif s <= 30: dur_buckets["10-30s"] += 1
        elif s <= 60: dur_buckets["30-60s"] += 1
        elif s <= 180: dur_buckets["1-3min"] += 1
        else: dur_buckets["3min+"] += 1

    # Subscriber count
    sub_count = conn.execute("SELECT COUNT(*) FROM subscribers").fetchone()[0]

    # Language & timezone breakdown (from pageview data field)
    lang_rows = conn.execute("""SELECT data FROM events WHERE event='pageview' AND ts>=? AND data IS NOT NULL""", (since,)).fetchall()
    lang_counts = {}
    tz_counts = {}
    for row in lang_rows:
        try:
            d = json.loads(row[0]) if row[0] else {}
            l = d.get("lang", "unknown")
            # Normalize: "ja" from "ja-JP", "en" from "en-US", "pt" from "pt-BR"
            l_short = l.split("-")[0].lower() if l else "unknown"
            lang_counts[l_short] = lang_counts.get(l_short, 0) + 1
            t = d.get("tz", "")
            if t:
                # Extract region from timezone like "Asia/Tokyo" -> "Japan", "America/Sao_Paulo" -> "Brazil"
                tz_to_country = {
                    "Asia/Tokyo": "Japan", "Asia/Seoul": "Korea", "Asia/Shanghai": "China",
                    "Asia/Hong_Kong": "Hong Kong", "Asia/Taipei": "Taiwan", "Asia/Singapore": "Singapore",
                    "America/New_York": "US East", "America/Chicago": "US Central",
                    "America/Denver": "US Mountain", "America/Los_Angeles": "US West",
                    "America/Sao_Paulo": "Brazil", "America/Argentina/Buenos_Aires": "Argentina",
                    "America/Bogota": "Colombia", "America/Mexico_City": "Mexico",
                    "Europe/London": "UK", "Europe/Paris": "France", "Europe/Berlin": "Germany",
                    "Europe/Lisbon": "Portugal", "Europe/Madrid": "Spain", "Europe/Rome": "Italy",
                    "Australia/Sydney": "Australia", "Pacific/Auckland": "New Zealand",
                    "Asia/Bangkok": "Thailand", "Asia/Jakarta": "Indonesia",
                    "Asia/Manila": "Philippines", "Asia/Kolkata": "India",
                }
                country = tz_to_country.get(t, t.split("/")[-1].replace("_", " "))
                tz_counts[country] = tz_counts.get(country, 0) + 1
        except Exception:
            pass

    # Sort by count descending
    lang_breakdown = sorted([{"lang": k, "count": v} for k, v in lang_counts.items()], key=lambda x: -x["count"])
    country_breakdown = sorted([{"country": k, "count": v} for k, v in tz_counts.items()], key=lambda x: -x["count"])

    # Subscriber language breakdown
    sub_lang_rows = conn.execute("SELECT lang, COUNT(*) FROM subscribers GROUP BY lang ORDER BY COUNT(*) DESC").fetchall()
    sub_by_lang = [{"lang": l, "count": c} for l, c in sub_lang_rows]

    conn.close()
    return {
        "total_pageviews": total_pv,
        "total_unique": total_uv,
        "recent_pageviews": recent_pv,
        "recent_unique": recent_uv,
        "recent_hours": hours,
        "top_pages": [{"path": p, "views": c, "unique": u} for p, c, u in top_pages],
        "hourly": [{"hour": h, "views": c, "unique": u} for h, c, u in hourly],
        "custom_events": [{"event": e, "count": c} for e, c in custom],
        "feedback": [json.loads(f[0]) for f in feedback if f[0]],
        "votes": [json.loads(v[0]) for v in votes if v[0]],
        "referrers": [{"ref": r, "count": c} for r, c in refs],
        "recent_events": [{"ts": t, "path": p, "event": e, "data": d} for t, p, e, d in recent],
        "avg_duration": avg_duration,
        "duration_sessions": total_duration_events,
        "duration_by_page": duration_by_page,
        "duration_buckets": dur_buckets,
        "subscriber_count": sub_count,
        "lang_breakdown": lang_breakdown,
        "country_breakdown": country_breakdown,
        "sub_by_lang": sub_by_lang,
    }

def subscribe_email(email, lang='ja', source='website'):
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute("INSERT OR IGNORE INTO subscribers (email, lang, source) VALUES (?,?,?)", (email, lang, source))
        conn.commit()
        count = conn.execute("SELECT COUNT(*) FROM subscribers").fetchone()[0]
        return count, None
    except Exception as e:
        return 0, str(e)
    finally:
        conn.close()

def submit_rpg_feedback(data):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""CREATE TABLE IF NOT EXISTS rpg_feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ts TEXT DEFAULT (datetime('now')),
        email TEXT,
        name TEXT,
        data TEXT
    )""")
    conn.execute("INSERT INTO rpg_feedback (email, name, data) VALUES (?,?,?)",
                 (data.get("email",""), data.get("name",""), json.dumps(data, ensure_ascii=False)))
    # Also register as subscriber if email provided
    email = data.get("email","").strip().lower()
    if email and "@" in email:
        conn.execute("INSERT OR IGNORE INTO subscribers (email, lang, source) VALUES (?,?,?)",
                     (email, "ja", "rpg"))
    # Count contributions for this email
    points = 0
    if email:
        points = conn.execute("SELECT COUNT(*) FROM rpg_feedback WHERE email=?", (email,)).fetchone()[0]
    conn.commit()
    total = conn.execute("SELECT COUNT(*) FROM rpg_feedback").fetchone()[0]
    conn.close()
    return {"ok": True, "points": points, "total_feedback": total}

def get_rpg_feedback():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""CREATE TABLE IF NOT EXISTS rpg_feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ts TEXT DEFAULT (datetime('now')),
        email TEXT,
        name TEXT,
        data TEXT
    )""")
    rows = conn.execute("SELECT ts, name, data FROM rpg_feedback ORDER BY ts DESC").fetchall()
    total = len(rows)
    # Points leaderboard
    leaders = conn.execute("""SELECT email, name, COUNT(*) as pts FROM rpg_feedback
        WHERE email != '' GROUP BY email ORDER BY pts DESC LIMIT 20""").fetchall()
    conn.close()
    return {
        "total": total,
        "feedback": [{"ts": t, "name": n, "data": json.loads(d) if d else {}} for t, n, d in rows],
        "leaderboard": [{"email": e, "name": n, "points": p} for e, n, p in leaders]
    }

def get_subscribers():
    conn = sqlite3.connect(DB_PATH)
    subs = conn.execute("SELECT email, lang, ts, source FROM subscribers ORDER BY ts DESC").fetchall()
    count = len(subs)
    conn.close()
    return {"count": count, "subscribers": [{"email": e, "lang": l, "ts": t, "source": s} for e, l, t, s in subs]}


# ============ X POSTING ============
def load_schedule():
    if os.path.exists(SCHEDULE_PATH):
        return json.loads(open(SCHEDULE_PATH).read())
    return []

def save_schedule(posts):
    os.makedirs(os.path.dirname(SCHEDULE_PATH), exist_ok=True)
    open(SCHEDULE_PATH, "w").write(json.dumps(posts, ensure_ascii=False, indent=2))

def load_post_log():
    if os.path.exists(POST_LOG_PATH):
        return json.loads(open(POST_LOG_PATH).read())
    return {}

def save_post_log(log):
    open(POST_LOG_PATH, "w").write(json.dumps(log, ensure_ascii=False, indent=2))

def post_to_x(text, image_path=None):
    """Post a tweet via X API v2."""
    try:
        import tweepy
    except ImportError:
        return None, "tweepy not installed"
    keys = {k: os.environ.get(k) for k in ["X_API_KEY","X_API_SECRET","X_ACCESS_TOKEN","X_ACCESS_TOKEN_SECRET"]}
    if not all(keys.values()):
        return None, "X API keys not configured"
    try:
        client = tweepy.Client(
            consumer_key=keys["X_API_KEY"], consumer_secret=keys["X_API_SECRET"],
            access_token=keys["X_ACCESS_TOKEN"], access_token_secret=keys["X_ACCESS_TOKEN_SECRET"])
        media_ids = None
        if image_path and os.path.exists(image_path):
            auth = tweepy.OAuth1UserHandler(keys["X_API_KEY"], keys["X_API_SECRET"], keys["X_ACCESS_TOKEN"], keys["X_ACCESS_TOKEN_SECRET"])
            api = tweepy.API(auth)
            media = api.media_upload(image_path)
            media_ids = [media.media_id]
        r = client.create_tweet(text=text, media_ids=media_ids)
        return r.data["id"], None
    except Exception as e:
        return None, str(e)

def cron_poster():
    """Background thread: check every 5 min if an approved post is due."""
    while True:
        try:
            posts = load_schedule()
            log = load_post_log()
            now = datetime.now(timezone(timedelta(hours=9)))  # JST
            start_date = log.get("_start_date")
            if not start_date:
                time.sleep(300)
                continue
            start = datetime.fromisoformat(start_date)
            for post in posts:
                if post["id"] in log:
                    continue
                if post.get("status") != "approved":
                    continue
                # Calculate target time
                target = start + timedelta(days=post["day"]-1, hours=post["hour"]-start.hour)
                target = target.replace(hour=post["hour"], minute=0, second=0)
                if now >= target:
                    print(f"[CRON] Posting: {post['id']}")
                    img = post.get("image")
                    if img and not os.path.isabs(img):
                        img = os.path.join(os.environ.get("STATIC_DIR", "/app"), img)
                    tweet_id, err = post_to_x(post["text"], img)
                    if tweet_id:
                        log[post["id"]] = {"tweet_id": str(tweet_id), "ts": now.isoformat()}
                        print(f"[CRON] OK: {tweet_id}")
                    else:
                        log[post["id"]] = {"error": err, "ts": now.isoformat()}
                        print(f"[CRON] ERR: {err}")
                    save_post_log(log)
                    time.sleep(5)
        except Exception as e:
            print(f"[CRON] Error: {e}")
        time.sleep(300)  # Check every 5 min

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=STATIC_DIR, **kwargs)

    def do_POST(self):
        if self.path == "/api/posts/approve":
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length)) if length else {}
            if body.get("key") != DASH_KEY:
                self._json_response({"error": "unauthorized"}, 403); return
            post_id = body.get("id")
            action = body.get("action", "approve")  # approve, reject, post_now
            posts = load_schedule()
            for p in posts:
                if p["id"] == post_id:
                    if action == "approve":
                        p["status"] = "approved"
                    elif action == "reject":
                        p["status"] = "rejected"
                    elif action == "post_now":
                        tweet_id, err = post_to_x(p["text"])
                        log = load_post_log()
                        if tweet_id:
                            log[post_id] = {"tweet_id": str(tweet_id), "ts": datetime.now(timezone.utc).isoformat()}
                            p["status"] = "posted"
                        else:
                            log[post_id] = {"error": err, "ts": datetime.now(timezone.utc).isoformat()}
                            p["status"] = "error"
                        save_post_log(log)
                    break
            save_schedule(posts)
            self._json_response({"ok": True, "posts": posts})
        elif self.path == "/api/posts/start":
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length)) if length else {}
            if body.get("key") != DASH_KEY:
                self._json_response({"error": "unauthorized"}, 403); return
            log = load_post_log()
            log["_start_date"] = datetime.now(timezone(timedelta(hours=9))).isoformat()
            save_post_log(log)
            self._json_response({"ok": True, "start_date": log["_start_date"]})
        elif self.path == "/api/posts/edit":
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length)) if length else {}
            if body.get("key") != DASH_KEY:
                self._json_response({"error": "unauthorized"}, 403); return
            posts = load_schedule()
            for p in posts:
                if p["id"] == body.get("id"):
                    if "text" in body: p["text"] = body["text"]
                    if "day" in body: p["day"] = body["day"]
                    if "hour" in body: p["hour"] = body["hour"]
                    break
            save_schedule(posts)
            self._json_response({"ok": True})
        elif self.path == "/api/event":
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length)) if length else {}
            ip = self.headers.get("X-Forwarded-For", self.client_address[0]).split(",")[0].strip()
            ua = self.headers.get("User-Agent", "")
            log_event(
                path=body.get("path", "/"),
                event=body.get("event", "pageview"),
                uid=body.get("uid", ""),
                ref=body.get("ref", ""),
                ua=ua, ip=ip,
                data=body.get("data")
            )
            self._json_response({"ok": True})
        elif self.path == "/api/rpg-feedback":
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length)) if length else {}
            result = submit_rpg_feedback(body)
            ip = self.headers.get("X-Forwarded-For", self.client_address[0]).split(",")[0].strip()
            log_event("/rpg", "rpg_feedback", "", "", self.headers.get("User-Agent", ""), ip, {"name": body.get("name","")})
            self._json_response(result)
        elif self.path == "/api/subscribe":
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length)) if length else {}
            email = body.get("email", "").strip().lower()
            lang = body.get("lang", "ja")
            source = body.get("source", "website")
            if not email or "@" not in email:
                self._json_response({"error": "invalid email"}, 400)
                return
            count, err = subscribe_email(email, lang, source)
            if err:
                self._json_response({"error": err}, 500)
            else:
                # Also log as event
                ip = self.headers.get("X-Forwarded-For", self.client_address[0]).split(",")[0].strip()
                log_event("/", "email_signup", "", "", self.headers.get("User-Agent", ""), ip, {"email_domain": email.split("@")[1]})
                self._json_response({"ok": True, "count": count})
        else:
            self.send_error(404)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/stats":
            params = parse_qs(parsed.query)
            key = params.get("key", [""])[0]
            if key != DASH_KEY:
                self._json_response({"error": "unauthorized"}, 403)
                return
            hours = int(params.get("hours", [24])[0])
            self._json_response(get_stats(hours))
        elif parsed.path == "/api/posts":
            params = parse_qs(parsed.query)
            if params.get("key", [""])[0] != DASH_KEY:
                self._json_response({"error": "unauthorized"}, 403); return
            self._json_response({"posts": load_schedule(), "log": load_post_log()})
        elif parsed.path == "/api/subscribers":
            params = parse_qs(parsed.query)
            if params.get("key", [""])[0] != DASH_KEY:
                self._json_response({"error": "unauthorized"}, 403)
                return
            self._json_response(get_subscribers())
        elif parsed.path == "/api/rpg-feedback":
            params = parse_qs(parsed.query)
            if params.get("key", [""])[0] != DASH_KEY:
                self._json_response({"error": "unauthorized"}, 403)
                return
            self._json_response(get_rpg_feedback())
        elif parsed.path == "/api/live":
            # Real-time active visitors: unique IPs in last 5 minutes
            conn = sqlite3.connect(DB_PATH)
            since = (datetime.now(timezone.utc) - timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S")
            count = conn.execute("SELECT COUNT(DISTINCT ip_hash) FROM events WHERE event='pageview' AND ts>=?", (since,)).fetchone()[0]
            conn.close()
            self._json_response({"count": max(count, 0)})
        elif parsed.path == "/api/health":
            self._json_response({"status": "ok", "ts": datetime.now(timezone.utc).isoformat()})
        else:
            super().do_GET()

    def _json_response(self, data, code=200):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def log_message(self, format, *args):
        pass  # Silence access logs

if __name__ == "__main__":
    os.chdir(STATIC_DIR)
    init_db()
    # Start cron poster thread
    t = threading.Thread(target=cron_poster, daemon=True)
    t.start()
    print(f"FLOW Server on :{PORT} (static: {STATIC_DIR}, cron: active)")
    HTTPServer(("", PORT), Handler).serve_forever()
