import os, time
from pathlib import Path
from google import genai
from google.genai import types

API_KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
client = genai.Client(api_key=API_KEY)
MODEL = "gemini-2.5-flash-image"
CHAR_DIR = Path("/Users/yuki/workspace/flow-anime/images/characters")

# Load existing refs
refs = []
for n in ["nagare","rio","marcelo","rin","sage"]:
    p = CHAR_DIR / f"{n}_sheet.png"
    if p.exists():
        refs.append(types.Part.from_bytes(data=p.read_bytes(), mime_type="image/png"))

images = [
    {
        "path": "/Users/yuki/workspace/flow-anime/images/characters/nagare_sheet_v2.png",
        "prompt": """Anime character design sheet for NAGARE from "FLOW" anime. Updated design v2.

KEY VISUAL CHANGE: His LEFT ARM (from shoulder to fingertips) is wrapped in BLACK COMPRESSION BANDAGE/TAPE. Not a medical cast — a fighter's wrap. Tight, layered, like a boxer's hand wrap but covering the entire arm. This is his SIGNATURE look.

On top of the black wrap, around his left wrist, a worn black belt is tied as a bracelet.

Character: NAGARE (流) - Male, 17 years old
- Lean wiry build (168cm, 62kg)
- Messy black hair falling over left eye
- Sharp dark brown eyes, intense and observant
- RIGHT arm is bare/normal
- LEFT arm completely wrapped in black bandage from shoulder to fingers

Sheet layout:
- Full body front view (white gi, black-wrapped left arm clearly visible)
- Side view
- Face close-up (calm but intense)
- Seated guard position (signature fighting stance, right hand gripping collar, left arm as frame)
- Detail inset: the black-wrapped hand with black belt bracelet

Style: Modern seinen anime (Jujutsu Kaisen quality). Clean white background. Japanese annotations.

The black arm against the white gi creates a striking contrast — this is what makes him recognizable in silhouette.

Reference images for consistency:"""
    },
    {
        "path": "/Users/yuki/workspace/flow-anime/images/keyvisual/kv_themat.png",
        "prompt": """Anime key visual poster for "FLOW" anime — called "The Mat."

Composition: Bird's-eye view (camera directly above, looking straight down).
A single BJJ mat (light gray/white) fills the frame. One overhead light creates a circular spotlight.

In the center of the mat, NAGARE (17yo, messy black hair, white gi, LEFT ARM wrapped in distinctive black bandage) sits in an open guard position. Alone. Looking up at the camera with intense eyes.

His black-wrapped left arm contrasts starkly against the white gi and white mat.

No AI screens. No special effects. No other characters. Just one fighter and the mat.

The simplicity IS the statement.

Bottom of frame, small text: "全ては畳の上で。"
Top: "FLOW" in clean typography.

Style: Cinematic anime, high contrast, dramatic single-light source. The feeling of walking into a quiet dojo at night. Intimate. Powerful.

Reference for Nagare's design:"""
    }
]

for i, img in enumerate(images):
    out = Path(img["path"])
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
