#!/usr/bin/env python3
"""FLOW - Character expression sheets"""
import os, sys, time
from pathlib import Path
from google import genai
from google.genai import types

API_KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
client = genai.Client(api_key=API_KEY)
OUT_DIR = Path(__file__).parent.parent / "images" / "expressions"
OUT_DIR.mkdir(parents=True, exist_ok=True)
CHAR_DIR = Path(__file__).parent.parent / "images" / "characters"
MODEL = "gemini-2.5-flash-image"

CHARS = [
    {"name": "nagare", "desc": "NAGARE (17yo boy, messy black hair, dark brown eyes, white gi). Calm by default, intense when fighting."},
    {"name": "rio", "desc": "RIO (18yo boy, platinum silver slicked-back hair, ice blue eyes, black AI suit). Confident, calculating, cold."},
    {"name": "marcelo", "desc": "LUCIANO (55yo man, dark brown skin, grey dreadlocks, warm brown eyes, blue gi). Warm, wise grandfather energy."},
    {"name": "rin", "desc": "RIN (19yo woman, dark red pixie-cut hair, amber eyes, purple gi). Fierce, defiant, independent."},
    {"name": "sage", "desc": "SAGE (AI entity, translucent geometric humanoid, white eyes with scrolling code, cyan/white). Serene, unsettling."},
]

EXPRESSIONS = "Expression sheet with 6 face close-ups arranged in 2 rows of 3, clean white background, anime style consistent with character sheet reference. Expressions: 1) Neutral/Default 2) Angry/Battle mode (intense eyes, gritted teeth) 3) Smiling/Happy (rare, genuine) 4) Shocked/Surprised (wide eyes) 5) Sad/Pained (downcast eyes) 6) Determined/Resolute (burning eyes, slight smirk). Label each expression in Japanese. Keep the art style consistent with the reference character sheet."

def generate(char):
    name = char["name"]
    out = OUT_DIR / f"{name}_expressions.png"
    if out.exists():
        print(f"  [skip] {name}")
        return True
    ref_path = CHAR_DIR / f"{name}_sheet.png"
    parts = []
    if ref_path.exists():
        parts.append(types.Part.from_bytes(data=ref_path.read_bytes(), mime_type="image/png"))
    parts.append(f"Using this character reference, create: {EXPRESSIONS}\n\nCharacter: {char['desc']}")
    print(f"  [gen] {name}...")
    try:
        r = client.models.generate_content(model=MODEL, contents=parts,
            config=types.GenerateContentConfig(response_modalities=["IMAGE","TEXT"]))
        for p in r.candidates[0].content.parts:
            if p.inline_data:
                out.write_bytes(p.inline_data.data)
                print(f"  [ok] {out}")
                return True
        print(f"  [warn] no image for {name}")
        return False
    except Exception as e:
        print(f"  [err] {name}: {e}")
        return False

print("=== Expression Sheets ===")
ok = 0
for i, c in enumerate(CHARS):
    print(f"[{i+1}/{len(CHARS)}] {c['name'].upper()}")
    if generate(c): ok += 1
    if i < len(CHARS)-1: time.sleep(4)
print(f"\nDone: {ok}/{len(CHARS)}")
