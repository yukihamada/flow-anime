#!/usr/bin/env python3
"""Regenerate character sheets WITHOUT any text — clean illustrations only."""

import os, sys, time
from pathlib import Path
from google import genai
from google.genai import types

API_KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
if not API_KEY:
    sys.exit("Error: API key not set")

client = genai.Client(api_key=API_KEY)
MODEL = "gemini-3-pro-image-preview"

CHAR_DIR = Path(__file__).parent.parent / "images" / "characters"
CHAR_DIR.mkdir(parents=True, exist_ok=True)

def load_ref(name):
    for suffix in ["_sheet_v2.png", "_sheet.png"]:
        path = CHAR_DIR / f"{name}{suffix}"
        if path.exists():
            return types.Part.from_bytes(data=path.read_bytes(), mime_type="image/png")
    return None

CHARS = [
    {
        "id": "nagare",
        "out": "nagare_sheet_v2.png",
        "prompt": """Recreate this character sheet for NAGARE, keeping the EXACT same character design, poses, and layout.

CRITICAL: DO NOT include ANY text, labels, annotations, or writing of any kind. No Japanese text, no English text, no labels, no arrows, no notes. ONLY the character illustrations on a clean white background.

Character: NAGARE — 17-year-old boy, messy black hair, intense dark eyes.
- Full body front view in white jiu-jitsu gi (道着), barefoot
- Left arm wrapped in BLACK bandage/tape from hand to shoulder
- White belt tied at waist
- Close-up face portrait showing determined expression
- Sitting meditation pose in gi
- Detail view of right hand with black belt bracelet wrapped around wrist
- Detail view of bandaged left arm

Style: Anime character design sheet, clean lines, white background, professional animation reference quality. Multiple views of the same character. 3:4 portrait ratio.""",
    },
    {
        "id": "rio",
        "out": "rio_sheet.png",
        "prompt": """Recreate this character sheet for RIO, keeping the EXACT same character design, poses, and layout.

CRITICAL: DO NOT include ANY text, labels, annotations, or writing of any kind. No Japanese text, no English text, no labels, no arrows, no notes. ONLY the character illustrations on a clean white background.

Character: RIO — 18-year-old young man, platinum silver/white hair slicked back, ice blue eyes, sharp features.
- Full body front view in sleek black SAGE corporate suit/uniform with holographic shoulder patches
- Arms crossed confident pose
- Close-up face with AI analysis glasses (thin blue-tinted visor)
- Side/back view showing the suit details
- Casual outfit: white turtleneck, gray pants, smartwatch
- Detail: AI analysis glasses accessory

Style: Anime character design sheet, clean lines, white background, professional animation reference quality. Multiple views. 3:4 portrait ratio.""",
    },
    {
        "id": "marcelo",
        "out": "marcelo_sheet.png",
        "prompt": """Recreate this character sheet for LUCIANO, keeping the EXACT same character design, poses, and layout.

CRITICAL: DO NOT include ANY text, labels, annotations, or writing of any kind. No Japanese text, no English text, no labels, no arrows, no notes. ONLY the character illustrations on a clean white background.

Character: LUCIANO — 55-year-old Brazilian man, dark brown skin, gray-streaked dreadlocks, warm smile, thick gray beard.
- Full body front view in blue jiu-jitsu gi with RED coral belt (珊瑚帯)
- Warm, wise expression
- Side view showing dreadlocks
- Sitting cross-legged meditation pose in gi
- Casual outfit: Hawaiian shirt, cargo shorts, sandals, prayer beads
- Small photo frame detail (old photo of young Kaido)

Style: Anime character design sheet, clean lines, white background, professional animation reference quality. Multiple views. 3:4 portrait ratio.""",
    },
    {
        "id": "rin",
        "out": "rin_sheet.png",
        "prompt": """Recreate this character sheet for RIN, keeping the EXACT same character design, poses, and layout.

CRITICAL: DO NOT include ANY text, labels, annotations, or writing of any kind. No Japanese text, no English text, no labels, no arrows, no notes. ONLY the character illustrations on a clean white background.

Character: RIN — 19-year-old woman, short dark red/auburn hair, sharp green-gold eyes, athletic build.
- Full body front view in dark purple/navy jiu-jitsu gi, purple belt, barefoot
- Fighting stance showing confidence
- Close-up face showing fierce, slightly smirking expression
- Sitting pose in casual clothes: black spider-web pattern top, ripped black jeans, red wrist tape
- Leather jacket with spider patch detail
- Small spider tattoo on ankle detail
- Red knee tape/support visible

Style: Anime character design sheet, clean lines, white background, professional animation reference quality. Multiple views. 3:4 portrait ratio.""",
    },
    {
        "id": "sage",
        "out": "sage_sheet.png",
        "prompt": """Recreate this character sheet for SAGE (the AI), keeping the EXACT same character design, poses, and layout.

CRITICAL: DO NOT include ANY text, labels, annotations, or writing of any kind. No Japanese text, no English text, no labels, no arrows, no notes. ONLY the character illustrations on a clean white background.

Character: SAGE — Humanoid AI avatar, androgynous, translucent blue-white crystalline body, circuit-like patterns visible under skin, calm expressionless face, glowing cyan eyes.
- Full body front view: translucent humanoid form with visible data circuits
- Side view
- Close-up face: serene, slightly unsettling, perfect symmetry
- Avatar mode: more solid blue form with data ripples at feet
- Combat analysis mode: dynamic pose with holographic displays around body, silhouette
- Signature pose with circular holographic rings

Style: Anime character design sheet, clean lines, white background, professional animation reference quality. Ethereal/digital aesthetic. 3:4 portrait ratio.""",
    },
]

for char in CHARS:
    out_path = CHAR_DIR / char["out"]
    print(f"Generating {char['id']}...")

    ref = load_ref(char["id"])
    parts = [ref, char["prompt"]] if ref else [char["prompt"]]

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=parts,
                config=types.GenerateContentConfig(
                    response_modalities=["image", "text"],
                    temperature=0.8,
                ),
            )
            for part in response.candidates[0].content.parts:
                if part.inline_data and part.inline_data.mime_type.startswith("image/"):
                    # Backup old file
                    if out_path.exists():
                        backup = CHAR_DIR / f"{char['id']}_sheet_old.png"
                        if not backup.exists():
                            out_path.rename(backup)
                    out_path.write_bytes(part.inline_data.data)
                    print(f"  [OK] {char['out']}")
                    break
            else:
                print(f"  [WARN] No image in response")
                continue
            break
        except Exception as e:
            err = str(e)
            if "429" in err or "RESOURCE_EXHAUSTED" in err:
                wait = 20 * (attempt + 1)
                print(f"  [RATE] Waiting {wait}s...")
                time.sleep(wait)
            else:
                print(f"  [ERR] {err[:100]}")
                break

print("\nDone!")
