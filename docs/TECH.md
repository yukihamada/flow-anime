# FLOW — Technical Guide

## Tech Stack

- **Site**: HTML/CSS/JS (no framework, lightweight)
- **Server**: Python 3.11 + SQLite (analytics, email subscriptions, feedback)
- **Deploy**: Fly.io (Tokyo region, `nrt`)
- **Image Generation**: Gemini 3 Pro Image
- **Music**: Suno AI
- **Story**: Claude + BJJ practitioner supervision
- **Domain**: [flow-anime.com](https://flow-anime.com)

## Repository Structure

```
flow-anime/
  index.html          # Top page (JP/EN/PT i18n)
  opening.html        # OP video + 60 episodes + ED
  review.html         # Review & voting
  rpg.html            # Community feedback (RPG members)
  pitch.html          # Pitch deck
  server.py           # Python server (analytics + X posting)
  story/
    series_bible.md        # Series bible (world, characters, settings)
    episode_guide_s1-5.md  # All 60 episode guides
  music/
    op_new.mp3 / op_en.mp3 / op_pt.mp3  # OP in 3 languages
    ed_new.mp3 / ed_en.mp3 / ed_pt.mp3  # ED in 3 languages
    songs.md                             # All lyrics
  images/
    characters/        # Character design sheets (clean, no text)
    keyvisual/         # Key visuals
    scenes/            # Scene concept art
    flow_art/          # Flow system art
    op_scenes/         # OP scene images (10 scenes x 3 patterns)
  scripts/             # Image generation & posting scripts
  docs/                # Technical documentation
```

## Local Development

```bash
git clone https://github.com/yukihamada/flow-anime.git
cd flow-anime
python3 server.py
# Open http://localhost:8080
```

## Deploy

```bash
fly deploy --remote-only
```

## API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/api/event` | POST | Track analytics event (pageview, duration, etc.) |
| `/api/subscribe` | POST | Email subscription |
| `/api/rpg-feedback` | POST | Community feedback submission |
| `/api/live` | GET | Real-time active visitor count |
| `/api/stats?key=` | GET | Analytics dashboard data (auth required) |
| `/api/subscribers?key=` | GET | Subscriber list (auth required) |
| `/api/rpg-feedback?key=` | GET | Feedback list (auth required) |
| `/api/health` | GET | Health check |

## Dashboard

Access at: `https://flow-anime.com/dashboard.html?key=<DASH_KEY>`

Features:
- Real-time pageviews, unique visitors
- Dwell time analysis (average, by page, distribution)
- Language & country breakdown (via timezone detection)
- Subscriber management
- Feedback & voting results
- Live event feed
