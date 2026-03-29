#!/usr/bin/env python3
"""FLOW - Scene concept art + Flow art + SAGE UI"""
import os, sys, time
from pathlib import Path
from google import genai
from google.genai import types

API_KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
client = genai.Client(api_key=API_KEY)
BASE = Path(__file__).parent.parent / "images"
CHAR_DIR = BASE / "characters"
MODEL = "gemini-2.5-flash-image"

def load_refs():
    parts = []
    for n in ["nagare","rio","marcelo","rin","sage"]:
        p = CHAR_DIR / f"{n}_sheet.png"
        if p.exists():
            parts.append(types.Part.from_bytes(data=p.read_bytes(), mime_type="image/png"))
    return parts

REFS = load_refs()

SCENES = [
    # Flow concept art
    {"dir": "flow_art", "name": "flow_lv1_shizuku", "prompt": """Anime concept art for "FLOW" anime - Level 1 "Shizuku (Droplet)" visualization.
Scene: Nagare (white gi, messy black hair) on a BJJ mat. A single water droplet falls from above in slow motion. Around his right hand gripping the opponent's collar, a subtle ripple effect appears — like a stone dropped in still water. The AI analysis overlay in the corner shows one number briefly glitch. Everything else is normal anime style, only the droplet moment has a slight ink-wash quality. Subtle, understated. The beginning of something."""},

    {"dir": "flow_art", "name": "flow_lv2_nagare", "prompt": """Anime concept art for "FLOW" anime - Level 2 "Nagare (Flow)" visualization.
Scene: Nagare mid-transition between techniques on the mat. His body leaves ink-brush afterimages — 3 to 5 overlapping poses showing a continuous sweep-to-back-take-to-choke sequence. The mat surface has become water, rippling. Half the frame is normal anime art, the other half transitions into sumi-e ink painting style. AI screens in background show cascading ERR messages. Water streams trail from his movements. Opponent looks confused, unable to track the flow."""},

    {"dir": "flow_art", "name": "flow_lv3_uzu", "prompt": """Anime concept art for "FLOW" anime - Level 3 "Uzu (Vortex)" visualization.
Scene: Both Nagare AND his opponent are now caught in the flow state. A massive ink vortex/whirlpool spirals from the center of the mat, engulfing both fighters. The entire arena has transformed — spectators see normal reality, but from the fighters' perspective everything is an abstract ink-wash landscape. Both fighters' eyes glow. ALL AI screens in the arena have crashed — static and noise. The vortex pulls everything into black ink. Dramatic, overwhelming, terrifying and beautiful."""},

    {"dir": "flow_art", "name": "flow_lv4_umi", "prompt": """Anime concept art for "FLOW" anime - Level 4 "Umi (Ocean)" — the unknown final level.
Scene: Abstract, mysterious. A lone figure (Kaido, Nagare's missing master) standing/floating in an infinite ocean of ink. The ocean is both literal water and sumi-e brushstrokes. Above: a vast sky filled with flowing calligraphy and technique names dissolving into nothing. The figure is peaceful, eyes closed, in a meditative seated position. Is this enlightenment or oblivion? Ethereal light filters through. Colors: black ink, deep indigo, occasional gold shimmer. This image should feel like a question, not an answer."""},

    # SAGE UI
    {"dir": "sage_ui", "name": "sage_ui_normal", "prompt": """UI/UX design mockup for anime "FLOW" — the SAGE AI analysis interface during a normal BJJ match.
Clean, futuristic heads-up display overlay on a dark background showing a BJJ match. Elements:
- Top bar: "SAGE v4.2 | MARS RATING SYSTEM" with connection status
- Left panel: Fighter A profile (photo, name, belt, win rate, MARS rating number)
- Right panel: Fighter B profile (same layout)
- Center: Real-time position detection — wireframe overlay on fighters showing "SIDE CONTROL" with arrows indicating pressure vectors
- Bottom left: Submission probability bar chart (armbar 34%, triangle 12%, RNC 8%, sweep 46%)
- Bottom right: Match timeline with predicted outcome "Fighter A wins — 87.3% confidence"
- Floating labels on the fighters: grip points highlighted in cyan, weight distribution shown as heat map
Style: Sleek, dark theme, cyan/white accents, slightly transparent. Think F1 race telemetry meets fighting game HUD. Professional broadcast quality."""},

    {"dir": "sage_ui", "name": "sage_ui_glitch", "prompt": """UI/UX design mockup for anime "FLOW" — the SAGE AI interface GLITCHING when Nagare enters Flow state.
Same layout as normal SAGE UI but everything is breaking:
- Top bar: "SAGE v4.2" text is corrupted, characters scrambled, red warning flashes
- Fighter profiles: Nagare's data shows "???" for all stats, photo is distorted
- Center position detection: wireframe can't track Nagare — his outline flickers between 3-4 positions, labeled "POSITION: UNDEFINED" in red
- Submission probability: all bars going haywire, numbers rapidly changing, some showing "ERR" or "NaN"
- Prediction: "CONFIDENCE: 12.4%... 8.1%... ERR... RECALCULATING..." in frantic red text
- Digital noise/static artifacts scattered across the interface
- One corner shows an emergency alert: "ANOMALY DETECTED — PATTERN MATCH: KAIDO YOICHI [ARCHIVED]"
Style: Same sleek dark UI but corrupted. Glitch art aesthetic. Red warning colors bleeding through cyan. CRT scanline effects."""},

    # Scene art
    {"dir": "scenes", "name": "scene_ep1_kaido", "prompt": """Cinematic anime scene from "FLOW" Episode 1 opening.
A massive arena, 2030 World Championship (Murajial). Thousands of spectators. Giant holographic SAGE screens everywhere showing stats.
In the center of the mat: KAIDO YOICHI (40yo Japanese man, tied-back long black hair, weathered face, white gi, black belt) in a low combat stance. His opponent VIKTOR (huge, muscular, eastern European, black gi with AI patches) towers over him.
The SAGE screen shows "VIKTOR — WIN PROBABILITY: 99.7%"
But Kaido is smiling. A subtle ink-wash aura begins to form around him.
The moment before everything changes.
Dramatic lighting from above. The crowd is a blur of lights. Cinematic 16:9 widescreen."""},

    {"dir": "scenes", "name": "scene_ep10_awakening", "prompt": """Cinematic anime scene from "FLOW" Episode 10 climax — Nagare's first full "Flow" activation in a tournament.
Nagare (white gi, messy black hair) is on the mat in a tournament. He was losing badly — his gi is disheveled, sweat dripping.
THE MOMENT: His eyes close. His right hand touches the mat. A ripple of water spreads from his palm across the entire mat surface.
When his eyes open, they reflect an ocean.
The background transforms: left half is the real tournament (bright lights, screaming crowd, AI screens), right half dissolves into a vast sumi-e ink painting of mountains and water.
His body begins to move — leaving brushstroke afterimages.
The opponent across from him looks terrified.
Every AI screen in the arena simultaneously shows "ERR".
The most important frame in the entire series. Make it breathtaking."""},

    {"dir": "scenes", "name": "scene_ep6_rin_spider", "prompt": """Anime scene from "FLOW" Episode 6 — Rin's introduction.
A dimly lit BJJ gym, no-gi class. RIN (19yo woman, dark red pixie-cut, amber eyes, black rash guard with crimson spider web pattern, red ankle tape) has just caught a much larger male opponent in an ashi garami (leg entanglement).
She's on her back, legs wrapped around his leg like a spider's web. Her expression is calm, almost bored — she's done this a thousand times. The opponent's face shows panic as he realizes he's caught.
Red thread-like lines emanate from her legs, forming a spider web pattern across the mat — visualizing her "system" of leg locks.
A small spider tattoo on her neck is visible.
Dramatic low-angle shot looking up at her."""},

    {"dir": "scenes", "name": "scene_ep12_reunion", "prompt": """Anime scene from "FLOW" Episode 12 climax — Rio confronts Nagare.
Luciano's small basement dojo in Shimokitazawa, Tokyo. Old mats, no AI screens, warm lighting from paper lanterns.
RIO (18yo, platinum silver hair, ice blue eyes, expensive black suit — out of place in this humble dojo) stands in the doorway, backlit.
NAGARE (white gi, black belt on wrist) faces him from the center of the mat. Tension between them is visible — the air between them distorts slightly.
LUCIANO sits in the background, watching silently, his face in shadow.
Two childhood friends who chose opposite paths. The composition should feel like a western standoff.
Cool blue light from Rio's side, warm amber from Nagare's side."""},

    {"dir": "scenes", "name": "scene_s4_sage_reveal", "prompt": """Anime scene from Season 4 — The SAGE revelation.
A massive server room deep underground. Rows of quantum computing towers emit cool blue light.
In the center: a glass chamber. Inside, suspended in translucent fluid, connected to thousands of data cables — the faint outline of a human body. It's KAIDO, Nagare's missing master.
SAGE's holographic avatar (translucent geometric humanoid, white eyes) stands before the chamber, one hand pressed against the glass.
NAGARE stands facing this scene, frozen in shock. His black belt bracelet is glowing.
The most horrifying moment of the series: the master wasn't hiding. He was absorbed.
Cold, clinical lighting. Horror meets sci-fi. Blue and white dominant with stark shadows."""},
]

def generate(item):
    d = BASE / item["dir"]
    d.mkdir(parents=True, exist_ok=True)
    out = d / f"{item['name']}.png"
    if out.exists():
        print(f"  [skip] {item['name']}")
        return True
    print(f"  [gen] {item['name']}...")
    try:
        contents = REFS + [item["prompt"] + "\n\nUse these character reference sheets for consistency:"]
        r = client.models.generate_content(model=MODEL, contents=contents,
            config=types.GenerateContentConfig(response_modalities=["IMAGE","TEXT"]))
        for p in r.candidates[0].content.parts:
            if p.inline_data:
                out.write_bytes(p.inline_data.data)
                print(f"  [ok] {out.name}")
                return True
        print(f"  [warn] no image")
        return False
    except Exception as e:
        print(f"  [err] {item['name']}: {e}")
        return False

print(f"=== Scene/Flow/UI Art Generator ({len(SCENES)} images) ===")
ok = 0
for i, s in enumerate(SCENES):
    print(f"[{i+1}/{len(SCENES)}] {s['name']}")
    if generate(s): ok += 1
    if i < len(SCENES)-1: time.sleep(4)
print(f"\nDone: {ok}/{len(SCENES)}")
