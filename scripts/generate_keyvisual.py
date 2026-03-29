#!/usr/bin/env python3
"""FLOW anime - Key Visual generator using Gemini"""

import os
import sys
import time
from pathlib import Path

from google import genai
from google.genai import types

API_KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
if not API_KEY:
    sys.exit("Error: API key not set")

client = genai.Client(api_key=API_KEY)
OUT_DIR = Path(__file__).parent.parent / "images" / "keyvisual"
OUT_DIR.mkdir(parents=True, exist_ok=True)

MODEL = "gemini-2.5-flash-image"

# Load character sheets as reference
CHAR_DIR = Path(__file__).parent.parent / "images" / "characters"

def load_ref(name):
    path = CHAR_DIR / f"{name}_sheet.png"
    if path.exists():
        return types.Part.from_bytes(data=path.read_bytes(), mime_type="image/png")
    return None

refs = {n: load_ref(n) for n in ["nagare", "rio", "marcelo", "rin", "sage"]}
ref_parts = [v for v in refs.values() if v is not None]

KEY_VISUALS = [
    {
        "name": "kv_main",
        "prompt": """Create the MAIN KEY VISUAL poster for an anime called "FLOW".

Composition (vertical poster, 2:3 ratio):
- Center: NAGARE (17yo boy, messy black hair, white gi, black belt wrapped on wrist) in a low guard stance, looking up with intense eyes. His right hand grips a gi collar. Around him, water-ink brushstroke effects swirl.
- Upper left: RIO (18yo, silver slicked hair, black AI suit with holographic patches, ice blue eyes) standing with arms crossed, looking down coldly. Data/code streams around him.
- Upper right: SAGE AI entity as a translucent geometric humanoid, looming over everything. White/cyan glow. Probability numbers floating.
- Lower left: LUCIANO (55yo, dark skin, grey dreadlocks, blue gi, coral belt) sitting cross-legged, warm smile, grounded.
- Lower right: RIN (19yo woman, dark red pixie cut, purple gi, amber eyes) in ashi garami position, fierce expression. Spider web pattern.
- Background: A BJJ mat splits into two worlds — left side is traditional (warm, wooden dojo), right side is futuristic (holographic AI screens, data streams)
- Top: Title "FLOW" in bold, stylized letters with water/ink effect
- Bottom: Tagline in Japanese "AIに読めない柔術で、世界の頂点へ"

Style: High-end anime movie poster quality. Dark atmosphere with dramatic lighting. Think Jujutsu Kaisen movie poster meets Ghost in the Shell aesthetics. Rich color palette: deep blues, blacks, with cyan/white accents from AI elements and warm orange from traditional side.

These reference images show the character designs to maintain consistency:""",
    },
    {
        "name": "kv_flow_awakening",
        "prompt": """Create a DRAMATIC KEY VISUAL for anime "FLOW" - the "Flow Awakening" scene.

Scene: NAGARE (17yo boy, messy black hair, white gi) is on a BJJ mat mid-grappling. The moment of "FLOW state" activation.

Composition:
- Nagare is in the center, transitioning between techniques. His body is half-realistic anime, half-dissolving into black ink/water brushstrokes.
- The mat beneath him ripples like water surface.
- The entire background transforms from a modern tournament arena (fluorescent lights, AI screens) into a sumi-e (Japanese ink painting) landscape — mountains, rivers, clouds made of brushstrokes.
- AI analysis UI elements on the edges of the frame are glitching, showing "ERR" and corrupted numbers.
- His opponent is frozen, unable to comprehend what's happening.
- Water droplets suspended in mid-air around Nagare, catching light.

Color: The realistic side is cool blue/grey. The ink-painting side is black/white/warm gold. The transition zone between them glows with ethereal light.

Style: Cinematic anime, 16:9 widescreen composition. Movie-quality illustration. Atmospheric, breathtaking, the kind of image that makes people stop scrolling.

Reference character designs:""",
    },
    {
        "name": "kv_rivals",
        "prompt": """Create a KEY VISUAL for anime "FLOW" - "Nagare vs Rio" rivalry poster.

Split composition (vertical):
- Left half: NAGARE (17yo, messy black hair, white gi, intense dark eyes) surrounded by water/ink effects. Traditional. Human. Imperfect. His left arm hangs slightly limp. Background is a weathered wooden dojo.
- Right half: RIO (18yo, platinum silver hair slicked back, black high-tech gi with AI patches, ice blue eyes) surrounded by data streams and geometric patterns. Technological. Perfect. Optimized. Background is a sleek modern training facility with holographic displays.
- Center dividing line: Where they meet, water/ink clashes with data streams, creating sparks and visual interference.
- They face each other in mirror fighting stances — but their styles are completely opposite.
- Faint image of SAGE AI looming above them both like a puppeteer.

Title "FLOW" at top. Below: "人間の直感 vs 機械の最適解"

Style: High contrast, dramatic anime poster. Split-screen aesthetic. Dark, intense mood. Think "Naruto vs Sasuke" level of iconic rivalry imagery but with BJJ/tech aesthetics.

Reference character designs:""",
    },
]


def generate_kv(kv):
    name = kv["name"]
    out_path = OUT_DIR / f"{name}.png"
    if out_path.exists():
        print(f"  [skip] {name} already exists")
        return True

    print(f"  [gen] {name}...")
    try:
        contents = ref_parts + [kv["prompt"]]
        response = client.models.generate_content(
            model=MODEL,
            contents=contents,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE", "TEXT"],
            ),
        )
        for part in response.candidates[0].content.parts:
            if part.inline_data:
                out_path.write_bytes(part.inline_data.data)
                print(f"  [ok] saved: {out_path}")
                return True
            if part.text:
                print(f"  text: {part.text[:200]}")
        print(f"  [warn] no image generated for {name}")
        return False
    except Exception as e:
        print(f"  [err] {name}: {e}")
        return False


def main():
    print("=== FLOW Key Visual Generator ===")
    print(f"Output: {OUT_DIR}")
    print(f"References loaded: {sum(1 for v in refs.values() if v)}/5")
    print()

    success = 0
    for i, kv in enumerate(KEY_VISUALS):
        print(f"[{i+1}/{len(KEY_VISUALS)}] {kv['name']}")
        if generate_kv(kv):
            success += 1
        if i < len(KEY_VISUALS) - 1:
            time.sleep(5)

    print(f"\nDone: {success}/{len(KEY_VISUALS)} key visuals generated")


if __name__ == "__main__":
    main()
