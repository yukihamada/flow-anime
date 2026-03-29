import os, time
from pathlib import Path
from google import genai
from google.genai import types

API_KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
client = genai.Client(api_key=API_KEY)
MODEL = "gemini-2.5-flash-image"
OUT = Path("/Users/yuki/workspace/flow-anime/images/sns")
OUT.mkdir(parents=True, exist_ok=True)

# Load Nagare reference
ref_path = Path("/Users/yuki/workspace/flow-anime/images/characters/nagare_sheet_v2.png")
ref = types.Part.from_bytes(data=ref_path.read_bytes(), mime_type="image/png") if ref_path.exists() else None

images = [
    {
        "path": OUT / "x_profile.png",
        "prompt": """Create a PROFILE PICTURE (avatar) for a Twitter/X account for the anime "FLOW".

Square format (1:1 ratio, 400x400px concept).

Design: The kanji character 流 (nagare/flow) rendered in dynamic sumi-e ink brush style. The brush stroke is fluid and energetic, with water droplets and ink splashes emanating from the strokes. The character is white/light cyan against a solid dark navy-black background (#0a0a15).

Around the kanji, subtle blue particle effects (like the anime's ink particle motif).

Simple, iconic, instantly recognizable even at small sizes. No text other than the kanji. No character faces.

Style: Clean, bold, Japanese calligraphy meets modern design. Think anime studio logo quality."""
    },
    {
        "path": OUT / "x_cover.png",
        "prompt": """Create a COVER/BANNER image for a Twitter/X account for the anime "FLOW".

Wide format (3:1 ratio, 1500x500px concept).

Composition (left to right):
- Left 20%: Dark gradient, nearly black. Small text "FLOW" in clean white typography, stacked vertically.
- Center: NAGARE (17yo boy, messy black hair, white gi, LEFT ARM wrapped in BLACK BANDAGE) in a low seated guard position. He's looking to the right with intense eyes. Behind him, flowing blue sumi-e ink effects trail to the right.
- Right side: The ink effects transform into digital glitch/code patterns (representing SAGE/AI). ERR text fragments scattered.
- Far right: Fading into a clean dark background.

The overall composition tells the story in one image: tradition (left) → human fighter (center) → AI world (right).

Bottom edge: Very subtle, tiny text "AIに読めない柔術で、世界の頂点へ"

Color palette: Deep black background, blue/cyan accents (#4a9eff, #00d4ff), white gi contrast.

Style: Cinematic anime banner, premium quality. Clean negative space. Not cluttered.

Reference for Nagare's design:"""
    }
]

refs = [ref] if ref else []
for i, img in enumerate(images):
    out = img["path"]
    if out.exists():
        print(f"[skip] {out.name}")
        continue
    print(f"[{i+1}/2] Generating {out.name}...")
    try:
        r = client.models.generate_content(model=MODEL, contents=refs + [img["prompt"]],
            config=types.GenerateContentConfig(response_modalities=["IMAGE","TEXT"]))
        for p in r.candidates[0].content.parts:
            if p.inline_data:
                out.write_bytes(p.inline_data.data)
                print(f"  [ok] {out}")
                break
    except Exception as e:
        print(f"  [err] {e}")
    if i < len(images)-1:
        time.sleep(5)
print("Done")
