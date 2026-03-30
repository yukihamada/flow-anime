#!/usr/bin/env python3
"""FLOW - 第1話「残像」シーン画像生成 (2パターンずつ)"""
import os, time
from pathlib import Path
from google import genai
from google.genai import types

API_KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
client = genai.Client(api_key=API_KEY)
OUT = Path(__file__).parent.parent / "images" / "ep1"
OUT.mkdir(exist_ok=True)
MODEL = "gemini-3.1-flash-image-preview"

CHAR_DIR = Path(__file__).parent.parent / "images" / "characters"

def load_char(name):
    p = CHAR_DIR / f"{name}_sheet.png"
    if p.exists():
        return types.Part.from_bytes(data=p.read_bytes(), mime_type="image/png")
    return None

nagare = load_char("nagare")

SCENES = [
    {
        "id": "scene01_sage_hud",
        "label": "シーン1: SAGEのHUD視点",
        "patterns": [
            {
                "id": "a",
                "prompt": """Anime key visual for "FLOW" — Scene 1A: SAGE AI HUD perspective during BJJ match opening.
First-person POV from Viktor (SAGE-equipped fighter). Dark arena, 40,000 spectators.
Full-screen teal HUD overlay: wireframe skeleton on opponent's body, joint mobility percentages (shoulder 94%, hip 87%), fatigue meter at bottom. Floating text: "RIGHT FOOT: INNER WEIGHT — PASS RIGHT 94.7%". Earpiece glyph pulsing. The opponent's every move is predicted before it happens.
Style: cinematic anime, dark/dramatic lighting, teal & white UI elements, photorealistic arena crowd in background. Cold, mechanical, efficient. Feels like watching a puppet show."""
            },
            {
                "id": "b",
                "prompt": """Anime key visual for "FLOW" — Scene 1B: SAGE AI broadcast overlay on giant arena screen.
Wide shot of massive sports arena. Giant screen shows the match with SAGE prediction UI overlaid. Two fighters on mat below — one is Viktor (SAGE), moving with robotic precision. Spectators watch their phones/tablets doing "answer checking" — SAGE predicted the move before it happened and they're confirming it.
Left side of screen: submission probability chart. Right side: "VICTOR WINS — 99.2% confidence". Timer counting down. Bottom ticker: "SAGE Corp — Prediction Accuracy This Season: 99.8%"
Style: anime wide establishing shot, dramatic arena lighting, cold blue/white color palette, technology dominating nature."""
            }
        ]
    },
    {
        "id": "scene02_kaido_sweep",
        "label": "シーン2: 海堂のスイープ・水柱",
        "patterns": [
            {
                "id": "a",
                "prompt": """CLIMACTIC anime key visual for "FLOW" — Scene 2A: Kaido Yoichi's sweep destroys SAGE.
Kaido (tall, long black hair loose, white gi, no earpiece) performs a cross-grip sweep against Viktor. The moment of contact: the entire tatami mat ERUPTS into a massive water geyser — Captain Tsubasa level exaggeration. Viktor flies through the air spinning. Water columns explode upward like a whale breaching. Time is frozen in slow motion.
In background corner: SAGE screen displays "ERR ERR ERR" in rapid succession, crashing.
The water has ink-wash (sumi-e) quality — not realistic water but painterly, calligraphic water.
Style: anime sakuga moment, maximum dynamic energy, ink-wash water effects, warm arena lights catching the spray, crowd silhouetted in awe. This is the most beautiful and shocking thing the audience has ever seen."""
            },
            {
                "id": "b",
                "prompt": """Atmospheric anime key visual for "FLOW" — Scene 2B: The aftermath — water ink ripple on the tatami.
After Kaido's sweep wins. Close-up: the tatami mat surface. Viktor has been submitted (out of frame). The mat has a sumi-e ink calligraphy RESIDUAL IMAGE of the sweep — like a ghost print left by the movement. Water ripples expand outward from where the technique happened.
Kaido stands calmly in the background, slightly out of focus, long hair settling. Crowd erupting.
In the very corner of the frame: a small child (young Nagare, 5 years old) watching with enormous eyes, mouth slightly open. He doesn't understand what he saw but he can't look away.
Style: quiet after the storm, sumi-e ink aesthetics on realistic surface, warm emotional lighting, the ink ripple is both literal and metaphorical."""
            }
        ]
    },
    {
        "id": "scene03_nagare_classroom",
        "label": "シーン3: 流の日常・教室",
        "patterns": [
            {
                "id": "a",
                "prompt": """Anime key visual for "FLOW" — Scene 3A: Nagare (17) alone in classroom during lunch break.
Nagare sits in the corner of a bright high school classroom, midday light streaming in. Everyone else is laughing in groups. He is completely alone, watching Kaido's match on his phone — the same sweep, replayed for the hundredth time. His left arm rests unnaturally bent on the desk. Three classmates nearby glance at it and quickly look away.
His face: not sad, not angry. Focused. Searching for something in those 7 seconds of footage.
Style: slice-of-life anime, warm nostalgic colors, contrast between the bright social classroom and his isolated focus. Character design: messy black hair, school uniform slightly rumpled, eyes sharp and alive despite the solitude."""
            },
            {
                "id": "b",
                "prompt": """Anime key visual for "FLOW" — Scene 3B: Nagare's phone screen close-up.
Extreme close-up: Nagare's phone screen showing Kaido's match paused at the exact moment of the sweep. His thumb and two fingers visible holding the phone. The screen is cracked slightly at the corner. He's zoomed in on the mat surface — trying to see the water ripple effect. Phone background has a worn-looking photo of the now-closed Kaido dojo sign.
Just above the phone, slightly blurred: his left hand, fingers bent wrong, trembling almost imperceptibly.
Style: intimate close-up anime shot, warm screen glow in contrast to darker surroundings, emotional weight in the detail."""
            }
        ]
    },
    {
        "id": "scene04_closed_dojo",
        "label": "シーン4: 閉鎖された道場",
        "patterns": [
            {
                "id": "a",
                "prompt": """Anime key visual for "FLOW" — Scene 4A: Nagare standing before the closed dojo.
Late afternoon light. A narrow alley in a Tokyo residential neighborhood. Metal roll-down shutter, rusted, padlocked. A weathered sign: "海堂柔術" (Kaido Jujutsu) — some characters faded, paint peeling. A yellowed paper notice of closure taped to the side.
Nagare (17, school uniform, left arm slightly off) stands before it with his back to the viewer. He's not moving. Just standing. The late light makes long shadows. Behind him, ordinary Tokyo life continues — a bicycle, an elderly neighbor.
Style: anime establishing shot, melancholic warm light, realistic urban Tokyo detail, quiet emotional weight. The closed shutter IS the story."""
            },
            {
                "id": "b",
                "prompt": """Anime key visual for "FLOW" — Scene 4B: Close-up on the dojo sign with Nagare's reflection.
The rusted metal shutter of Kaido's closed dojo. The sign "海堂柔術" slightly corroded. In the polished lower panel of the shutter: Nagare's reflection, distorted, warped by the metal's imperfections. He's looking up at the sign.
Superimposed ghost image (translucent, in warm memory colors): the same shutter in the past, OPEN, warm light spilling out, the sound of training implied.
His right hand, half-raised, almost touching the shutter. Not quite touching.
Style: dual-layer composition, present/past contrast, muted present colors vs warm memory colors, intimate urban melancholy."""
            }
        ]
    },
    {
        "id": "scene05_flashback_child",
        "label": "シーン5: 幼少期回想",
        "patterns": [
            {
                "id": "a",
                "prompt": """Anime key visual for "FLOW" — Scene 5A: Evening at the dojo — Kaido and young Nagare.
Warm evening light, small dojo interior (tatami, low ceilings, one fluorescent light with slight flicker). Young Nagare (8 years old, tiny, messy hair, white gi) is attempting a triangle choke on a practice dummy and failing for the tenth time, flopping over.
Kaido (30s, tall, long black hair tied back, coral belt, kind face) kneels beside him. He's tapping Nagare's head lightly — affectionate, not condescending. About to demonstrate.
Subtle detail: Kaido is humming to himself, completely unaware. Young Nagare notices and almost smiles.
Style: warm nostalgic anime, golden hour interior light, safe and small world feeling, the relationship is everything."""
            },
            {
                "id": "b",
                "prompt": """Anime key visual for "FLOW" — Scene 5B: Young Nagare and Kaido — the "one more time" moment.
Young Nagare (8) looks up at Kaido after failing the drill. "How many times do I have to do this?" Written on his face. Kaido is crouching at eye level, completely present, not distracted.
Kaido's face: genuine delight. Not the face of a teacher. The face of someone who just loves this. He's saying "one more time" but it sounds like an invitation, not an order.
Behind them through a small window: the sun is setting. They've been here all afternoon. Neither has noticed.
Style: intimate two-shot, warm color palette, the dojo feels like home, slight nostalgia filter as if this is a memory being remembered imperfectly."""
            }
        ]
    },
    {
        "id": "scene06_night_resolve",
        "label": "シーン6: 夜の決意",
        "patterns": [
            {
                "id": "a",
                "prompt": """Anime key visual for "FLOW" — Scene 6A: Nagare's night room — trembling hand and resolve.
Night. Small bedroom, blue light from laptop/phone screen. Nagare sits on the floor, back against the bed. The screen shows Kaido's sweep paused mid-water-column.
Nagare looks at his own LEFT HAND. He's trying to close it into a fist. The fingers close... slowly... trembling. Not fully. But they move.
His face: not pain, not frustration. Something like wonder. Something like: I didn't know it could still do that.
On his wrist: a worn black belt wrapped like a bracelet — Kaido's belt.
Style: intimate night scene, blue screen light as only illumination, quiet intensity, everything compressed into that hand and that face."""
            },
            {
                "id": "b",
                "prompt": """Anime key visual for "FLOW" — Scene 6B: Nagare's eyes — the moment of decision.
Extreme close-up: Nagare's face, night, lit only by screen glow. Half the frame is shadow. His eyes are the entire image.
His eyes are not sad. They are completely, terrifyingly calm. Focused on something far away, through the wall, through the city, through time.
In the reflection of his eyes: the ghost of Kaido's sweep, a tiny water ripple.
Behind him out of focus: the TV shows a SAGE Corp news segment (muted). The words "prediction" and "98.2%" visible.
His hand comes up into frame — the left one — and he closes it. The trembling stops for exactly one second.
Style: ultra-close portrait, dramatic lighting, the EYES are everything, ink-wash ghost reflection effect, the moment before a story begins."""
            }
        ]
    }
]

def gen(prompt, out_path, refs=None):
    if out_path.exists():
        print(f"  SKIP {out_path.name}")
        return True
    parts = []
    if refs:
        parts.extend(refs)
    parts.append(prompt)
    try:
        resp = client.models.generate_content(
            model=MODEL,
            contents=parts,
            config=types.GenerateContentConfig(response_modalities=["IMAGE","TEXT"])
        )
        for part in resp.candidates[0].content.parts:
            if part.inline_data:
                out_path.write_bytes(part.inline_data.data)
                print(f"  OK  {out_path.name}")
                return True
        print(f"  FAIL no image {out_path.name}")
        return False
    except Exception as e:
        print(f"  ERR {out_path.name}: {e}")
        return False

if __name__ == "__main__":
    char_refs = [r for r in [nagare] if r]
    for scene in SCENES:
        print(f"\n=== {scene['label']} ===")
        for pat in scene["patterns"]:
            fname = f"{scene['id']}_{pat['id']}.png"
            out = OUT / fname
            gen(pat["prompt"], out, char_refs)
            time.sleep(3)
    print("\nDone.")
