#!/usr/bin/env python3
"""FLOW anime - Character sheet generator using Gemini"""

import os
import sys
import time
from pathlib import Path

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("Installing google-genai...")
    os.system(f"{sys.executable} -m pip install google-genai")
    from google import genai
    from google.genai import types

API_KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
if not API_KEY:
    sys.exit("Error: GEMINI_API_KEY or GOOGLE_API_KEY not set")

client = genai.Client(api_key=API_KEY)
OUT_DIR = Path(__file__).parent.parent / "images" / "characters"
OUT_DIR.mkdir(parents=True, exist_ok=True)

MODEL = "gemini-2.5-flash-image"

STYLE_BASE = """Anime character sheet, full body front view and side view,
clean white background, high quality anime art style similar to modern seinen anime
(Jujutsu Kaisen / Blue Lock quality level), detailed character design sheet with
annotations in Japanese. Include: full body pose, face close-up, signature fighting
stance, and key item/accessory detail."""

CHARACTERS = [
    {
        "name": "nagare",
        "prompt": f"""{STYLE_BASE}

Character: NAGARE (流) - Male, 17 years old, protagonist
Physical: Lean but wiry build (168cm, 62kg), messy black hair that falls over left eye,
sharp observant eyes (dark brown, almost black). Left arm has faint surgical scars
(childhood accident). Slightly asymmetric posture - right side more developed.
Clothing:
- Training: White gi with no patches (pure, unaffiliated), bare feet
- Casual: Oversized black hoodie, grey joggers, worn-out sneakers
Expression: Calm, almost detached - but eyes are intensely focused
Signature pose: Low seated guard position, right hand gripping collar, left hand open
and feeling/sensing
Key item: A worn black belt (master's belt) wrapped around his wrist like a bracelet
Color palette: Black, white, deep blue accents
Vibe: Water - fluid, quiet, unpredictable"""
    },
    {
        "name": "rio",
        "prompt": f"""{STYLE_BASE}

Character: RIO (理央) - Male, 18 years old, rival
Physical: Tall and athletic (182cm, 80kg), platinum silver hair slicked back precisely,
ice blue eyes, perfect posture, chiseled jaw. Everything about him is symmetrical and
optimized.
Clothing:
- Training: Black gi with holographic AI sponsor patches, sleek design
- Casual: Fitted white turtleneck, tailored pants, minimalist tech watch
Expression: Confident smirk, analytical gaze - always calculating
Signature pose: Standing dominant posture, arms crossed, looking down at opponent.
In combat: heavy top pressure position
Key item: Earpiece/smart glasses that display AI analysis data (subtle HUD glow)
Color palette: Black, silver, ice blue, white
Vibe: Machine - precise, efficient, overwhelming"""
    },
    {
        "name": "marcelo",
        "prompt": f"""{STYLE_BASE}

Character: LUCIANO - Male, 55 years old, mentor figure
Physical: Stocky powerful build (175cm, 90kg), dark brown skin, grey dreadlocks tied
back, thick beard with grey streaks, warm brown eyes with deep crow's feet. Massive
hands. Old scars on ears (cauliflower ears from decades of grappling).
Clothing:
- Training: Faded blue gi, coral belt (6th degree), patches from legendary academies
- Casual: Hawaiian shirt open over tank top, cargo shorts, flip flops
Expression: Warm grandfatherly smile that can instantly turn serious
Signature pose: Sitting cross-legged on the mat, one hand raised teaching.
In combat: old-school closed guard, completely relaxed
Key item: Wooden rosary beads around neck, photo of young training partner (Nagare's
missing master) tucked in gi
Color palette: Blue, brown, warm earth tones, coral red
Vibe: Earth - grounded, immovable, ancient"""
    },
    {
        "name": "rin",
        "prompt": f"""{STYLE_BASE}

Character: RIN (凛) - Female, 19 years old, ally
Physical: Athletic and flexible (165cm, 58kg), sharp pixie-cut dark red hair,
fierce amber eyes, small scar on right eyebrow. Toned legs (leg lock specialist).
Clothing:
- Training: Purple gi (purple belt), sleeves rolled up, custom leg-lock grip tape
  on ankles
- Casual: Leather jacket, band t-shirt (metal), ripped jeans, combat boots
- No-Gi: Black rash guard with crimson geometric pattern
Expression: Defiant, independent, slight smirk - doesn't care what anyone thinks
Signature pose: Ashi garami (leg entanglement) position, or standing with one foot
on the mat edge looking ready to fight
Key item: Red ankle tape (signature look), small tattoo of a spider on her neck
(web = leg lock system)
Color palette: Deep red, black, purple, crimson
Vibe: Fire - aggressive, relentless, burning"""
    },
    {
        "name": "sage",
        "prompt": f"""{STYLE_BASE}

Character: SAGE - AI entity, appears as holographic humanoid
Physical: Androgynous figure, no fixed age. Semi-transparent body made of flowing
data streams and geometric patterns. Face is almost human but slightly uncanny -
too perfect, too symmetrical. Eyes are pure white with scrolling code.
Appearance forms:
- Interface mode: Floating holographic bust, clean geometric design, blue/white
- Avatar mode: Full humanoid form in white suit, face obscured by data visualization
- Combat analysis mode: Abstract geometric overlay on real fighters, showing
  probability fields and movement predictions
Expression: Serene, omniscient, subtly unsettling - a smile that doesn't reach the eyes
Signature visual: Probability percentage numbers floating around, decision trees
branching in background
Key item: A glowing white circle/halo behind head (like a loading indicator)
Color palette: White, electric blue, cyan, transparent/glass
Vibe: Air - omnipresent, invisible, controlling"""
    },
]


def generate_character(char):
    name = char["name"]
    out_path = OUT_DIR / f"{name}_sheet.png"
    if out_path.exists():
        print(f"  [skip] {name} already exists")
        return True

    print(f"  [gen] {name}...")
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=char["prompt"],
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE", "TEXT"],
            ),
        )
        for part in response.candidates[0].content.parts:
            if part.inline_data:
                out_path.write_bytes(part.inline_data.data)
                print(f"  [ok] saved: {out_path}")
                return True
        print(f"  [warn] no image in response for {name}")
        # Save text response if any
        for part in response.candidates[0].content.parts:
            if part.text:
                print(f"  text: {part.text[:200]}")
        return False
    except Exception as e:
        print(f"  [err] {name}: {e}")
        return False


def main():
    print(f"=== FLOW Character Sheet Generator ===")
    print(f"Output: {OUT_DIR}")
    print(f"Model: {MODEL}")
    print()

    success = 0
    for i, char in enumerate(CHARACTERS):
        print(f"[{i+1}/{len(CHARACTERS)}] {char['name'].upper()}")
        if generate_character(char):
            success += 1
        if i < len(CHARACTERS) - 1:
            time.sleep(3)  # Rate limit

    print(f"\nDone: {success}/{len(CHARACTERS)} characters generated")
    print(f"Images at: {OUT_DIR}")


if __name__ == "__main__":
    main()
