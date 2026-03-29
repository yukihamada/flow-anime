import os, sys, time
from pathlib import Path
from google import genai
from google.genai import types

API_KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
client = genai.Client(api_key=API_KEY)
MODEL = "gemini-2.5-flash-image"
CHAR_DIR = Path("/Users/yuki/workspace/flow-anime/images/characters")

def load_refs():
    parts = []
    for n in ["nagare","rio","marcelo","rin","sage"]:
        p = CHAR_DIR / f"{n}_sheet.png"
        if p.exists():
            parts.append(types.Part.from_bytes(data=p.read_bytes(), mime_type="image/png"))
    return parts

REFS = load_refs()
print(f"Loaded {len(REFS)} reference images")

IMAGES = [
    {
        "path": "/Users/yuki/workspace/flow-anime/images/flow_art/flow_lv3_uzu.png",
        "prompt": """Anime concept art for "FLOW" anime - Level 3 "Uzu (Vortex)" visualization.
IMPORTANT: Use FULL COLOR matching the style of the other flow art in this series (not monochrome).

Scene: A large tournament arena. NAGARE (white gi, messy black hair, 17yo) and his OPPONENT (black gi with AI patches) are both caught in the flow state on the mat. A massive swirling VORTEX of water and ink spirals from the center of the mat upward, engulfing both fighters. The vortex is colored — deep blues, cyan, black ink swirls with golden light at the edges.

Both fighters are clearly visible at LARGE SCALE (waist-up at minimum). Nagare's eyes glow with blue light. The opponent looks terrified and confused.

The arena background is visible — spectators, overhead lights — but ALL the AI analysis screens in the arena have crashed, showing static and red "ERR" text. Digital noise artifacts scatter at the edges.

The vortex should feel overwhelming, beautiful, and slightly terrifying. This is the level where BOTH fighters lose control.

Style: Full-color anime art, dynamic composition, dramatic lighting. Consistent with modern seinen anime quality (Jujutsu Kaisen domain expansion level of visual impact).

Reference character sheets for consistency:"""
    },
    {
        "path": "/Users/yuki/workspace/flow-anime/images/scenes/scene_ep12_reunion.png",
        "prompt": """Anime scene from "FLOW" Episode 12 — Rio confronts Nagare at the dojo.

CRITICAL: The two characters must look COMPLETELY DIFFERENT from each other.

Setting: Luciano's small basement dojo in Shimokitazawa, Tokyo. Old mats, no AI screens, warm amber lighting from paper lanterns. Traditional Japanese aesthetic.

LEFT SIDE — NAGARE (17yo boy): messy black hair falling over left eye, dark brown eyes, white gi (slightly worn), lean build (168cm). Standing in the center of the mat. Tense but calm. Black belt wrapped around his LEFT WRIST as a bracelet.

RIGHT SIDE — RIO (18yo boy): platinum SILVER hair slicked back precisely, ice BLUE eyes, wearing an expensive fitted black suit (NOT a gi — he's visiting, not training). Tall athletic build (182cm). Standing in the doorway, backlit by cool blue light from outside. Arms at his sides, cold expression.

BACKGROUND: LUCIANO (55yo, dark skin, grey dreadlocks, blue gi) sits in shadow against the far wall, watching silently.

The contrast should be stark: Nagare = warm/traditional/humble, Rio = cool/modern/elite. Like a western standoff — two old friends who chose opposite paths.

Warm amber light from Nagare's side, cool blue light from Rio's side. The lighting clash in the middle of the room.

Reference character sheets:"""
    },
    {
        "path": "/Users/yuki/workspace/flow-anime/images/expressions/rin_expressions.png",
        "prompt": """Create an expression sheet for RIN from anime "FLOW".

CRITICAL: Match the CHARACTER SHEET exactly. Rin has SHARP, ANGULAR features — NOT round or soft. Strong jawline, fierce amber/gold eyes, dark red/burgundy PIXIE-CUT hair (short, spiky, edgy). Small scar on right eyebrow. Purple gi collar visible.

Expression sheet with 6 face close-ups arranged in 2 rows of 3, clean white background.
Expressions labeled in Japanese:
1) 通常 (Neutral) — calm, slightly bored, default resting face
2) 怒り (Angry/Battle) — bared teeth, narrowed fierce eyes, veins visible
3) 笑顔 (Smirk/Confident) — one-sided smirk, challenging, "come at me" energy
4) 驚き (Shocked) — wide eyes, but still maintaining angular face shape
5) 悲しみ (Sad/Pained) — downcast eyes, tight lips, stoic sadness
6) 決意 (Determined) — burning eyes, slight forward lean, ready to fight

Style: Clean anime character sheet style. Keep ALL 6 faces with the SAME angular bone structure, sharp jaw, and fierce energy. She should look like a fighter, not a schoolgirl.

Reference character sheet to match:"""
    }
]

for i, img in enumerate(IMAGES):
    out_path = Path(img["path"])
    # Back up old version
    backup = out_path.with_suffix('.old.png')
    if out_path.exists():
        out_path.rename(backup)
        print(f"[{i+1}/3] Backed up {out_path.name} -> {backup.name}")

    print(f"[{i+1}/3] Generating {out_path.name}...")
    try:
        contents = REFS + [img["prompt"]]
        r = client.models.generate_content(model=MODEL, contents=contents,
            config=types.GenerateContentConfig(response_modalities=["IMAGE","TEXT"]))
        for p in r.candidates[0].content.parts:
            if p.inline_data:
                out_path.write_bytes(p.inline_data.data)
                print(f"  [ok] saved {out_path}")
                break
        else:
            print(f"  [warn] no image generated")
            if backup.exists():
                backup.rename(out_path)
    except Exception as e:
        print(f"  [err] {e}")
        if backup.exists():
            backup.rename(out_path)

    if i < len(IMAGES)-1:
        time.sleep(5)

print("\nDone! All 3 images regenerated.")
