"""FLOW 90秒PV — 30カット画像生成 (Gemini 2.0 Flash)
Usage: python3 gen_pv_shots.py
"""
import os, time, json
from pathlib import Path
from google import genai
from google.genai import types

API_KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
if not API_KEY:
    raise SystemExit("GEMINI_API_KEY not set")

client = genai.Client(api_key=API_KEY)
OUT_DIR = Path(__file__).parent.parent / "images" / "pv_shots"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Reference images for style consistency
REF_DIR = Path(__file__).parent.parent / "images"

def load_ref(path):
    """Load reference image as Part."""
    full = REF_DIR / path
    if not full.exists():
        return None
    with open(full, "rb") as f:
        return types.Part.from_bytes(data=f.read(), mime_type="image/png")

# Load key reference images for style
ref_nagare = load_ref("characters/nagare_sheet.png")
ref_rio = load_ref("characters/rio_sheet.png")
ref_rin = load_ref("characters/rin_sheet.png")
ref_kv = load_ref("keyvisual/kv_main.png")

STYLE = """Anime art style, high quality, cinematic lighting, 16:9 aspect ratio,
dark moody atmosphere with teal and orange color grading,
Brazilian jiu-jitsu anime aesthetic, detailed character art.
Style reference: modern seinen anime like Vinland Saga or Blue Lock,
with sci-fi holographic UI elements in fight scenes."""

# 30 cuts for 90-second PV, ~3 seconds each
# Structured: Intro(0-8s) → Verse1(8-28s) → Pre-Chorus(28-38s) → Chorus(38-52s) → Verse2(52-65s) → Chorus2(65-83s) → Outro(83-90s)
SHOTS = [
    # === INTRO (0-8s) — Mood setting ===
    {"id": "01_water_drop", "time": "0-3s", "section": "INTRO",
     "prompt": f"A single water droplet falling onto a dark tatami mat, creating ripples of light. Close-up macro shot. The ripple glows with faint teal holographic light. {STYLE}",
     "ref": None},

    {"id": "02_dojo_dawn", "time": "3-6s", "section": "INTRO",
     "prompt": f"An empty traditional Japanese dojo at dawn, sunlight streaming through wooden shutters. A single black belt hangs on the wall. Dust particles in golden light. Cinematic wide shot. {STYLE}",
     "ref": None},

    {"id": "03_title", "time": "6-8s", "section": "INTRO",
     "prompt": f"Anime title card 'FLOW' in bold stylized typography, with water/liquid effect swirling around the letters. Dark background with teal and blue energy streams. The 'O' in FLOW has a water ripple effect. {STYLE}",
     "ref": None},

    # === VERSE 1 (8-28s) — Nagare's backstory ===
    {"id": "04_nagare_bandage", "time": "8-11s", "section": "VERSE1",
     "prompt": f"Close-up of a young man's left arm wrapped in black bandages, clenching his fist. The bandages have faint teal energy lines running through them. Dramatic lighting from above. 17-year-old boy with messy black hair, wearing white jiu-jitsu gi. {STYLE}",
     "ref": ref_nagare},

    {"id": "05_nagare_tatami", "time": "11-14s", "section": "VERSE1",
     "prompt": f"A 17-year-old boy with messy black hair standing alone on a jiu-jitsu tatami mat, wearing a white gi with black belt. His left arm hangs slightly limp. Shot from behind, looking at an empty dojo. Melancholic atmosphere. {STYLE}",
     "ref": ref_nagare},

    {"id": "06_flashback_child", "time": "14-17s", "section": "VERSE1",
     "prompt": f"Flashback scene: A small child (5 years old) lying on a hospital bed, left arm in a cast. Muted, desaturated colors with soft light. A black belt rests on the bedside table. Emotional, tender anime scene. {STYLE}",
     "ref": None},

    {"id": "07_master_back", "time": "17-20s", "section": "VERSE1",
     "prompt": f"The silhouette of a large man walking away down a dojo corridor, seen from behind. He's wearing a coral-colored belt (red and white). The boy stands small in the foreground watching him leave. Dramatic backlighting. {STYLE}",
     "ref": None},

    {"id": "08_earpiece", "time": "20-23s", "section": "VERSE1",
     "prompt": f"Close-up of a futuristic translucent earpiece with holographic blue data streaming from it. Numbers and fight prediction percentages float in the air: '99.8%'. Cyberpunk aesthetic mixed with martial arts. {STYLE}",
     "ref": None},

    {"id": "09_nagare_refuse", "time": "23-26s", "section": "VERSE1",
     "prompt": f"A 17-year-old boy with messy black hair crushing a translucent earpiece in his right hand. Sparks and data fragments scatter. His expression is defiant, jaw clenched. Close-up from below, dramatic angle. {STYLE}",
     "ref": ref_nagare},

    {"id": "10_breathe", "time": "26-28s", "section": "VERSE1",
     "prompt": f"The boy in white gi sitting in seiza position on the tatami, eyes closed, breathing deeply. Faint water ripples emanate from beneath him. Peaceful moment before the storm. Soft teal glow. {STYLE}",
     "ref": ref_nagare},

    # === PRE-CHORUS (28-38s) — Rising tension ===
    {"id": "11_ai_screen", "time": "28-31s", "section": "PRE-CHORUS",
     "prompt": f"A massive holographic screen showing fight analytics — body heat maps, skeletal wireframes, probability percentages. The text 'SAGE v4.2' glows in the corner. Dark arena with spectators in silhouette. {STYLE}",
     "ref": None},

    {"id": "12_rio_stance", "time": "31-34s", "section": "PRE-CHORUS",
     "prompt": f"An 18-year-old young man with silver hair and ice-blue eyes, wearing a sleek black AI-enhanced rashguard with holographic arm patches. He stands in a perfect fighting stance. Cold, calculating expression. Blue data streams around him. {STYLE}",
     "ref": ref_rio},

    {"id": "13_face_off", "time": "34-36s", "section": "PRE-CHORUS",
     "prompt": f"Split screen: Left side — a boy in white gi (messy black hair, defiant eyes). Right side — a young man in black AI suit (silver hair, cold eyes). A crack of light divides them. Tension building. {STYLE}",
     "ref": ref_kv},

    {"id": "14_arena_wide", "time": "36-38s", "section": "PRE-CHORUS",
     "prompt": f"A massive futuristic martial arts arena in 2030. Holographic displays surround the mat. Thousands of spectators. Two fighters walking toward the center from opposite ends. Dramatic wide shot with volumetric lighting. {STYLE}",
     "ref": None},

    # === CHORUS 1 (38-52s) — Peak action ===
    {"id": "15_flow_activate", "time": "38-40s", "section": "CHORUS",
     "prompt": f"The boy in white gi with eyes glowing teal, water-like energy exploding from his body. All holographic screens around the arena display 'ERROR'. His black bandaged left arm emanates dark energy. Full body action shot. {STYLE}",
     "ref": ref_nagare},

    {"id": "16_guard_pull", "time": "40-42s", "section": "CHORUS",
     "prompt": f"Dynamic jiu-jitsu action: the boy in white pulling guard, wrapping his legs around the silver-haired opponent. Water effects trail their movements. AI prediction numbers shatter like glass. Intense close combat. {STYLE}",
     "ref": None},

    {"id": "17_sweep", "time": "42-44s", "section": "CHORUS",
     "prompt": f"A dramatic scissor sweep in jiu-jitsu. The boy in white flips the silver-haired opponent with a fluid motion. Water trails follow the sweep arc. The opponent's blue data HUD flickers and glitches. Dynamic motion lines. {STYLE}",
     "ref": None},

    {"id": "18_error_screens", "time": "44-46s", "section": "CHORUS",
     "prompt": f"Multiple holographic screens all showing 'ERR' in red, glitching and breaking apart. The crowd gasps. The AI system SAGE is malfunctioning. Cyberpunk glitch art aesthetic with red warning colors. {STYLE}",
     "ref": None},

    {"id": "19_mount", "time": "46-48s", "section": "CHORUS",
     "prompt": f"The boy in white gi achieving mount position over the silver-haired opponent on a dark tatami. Teal energy ripples spread across the mat. The boy's expression is calm, almost meditative despite the intensity. Bird's eye view. {STYLE}",
     "ref": None},

    {"id": "20_submission", "time": "48-50s", "section": "CHORUS",
     "prompt": f"Close-up of an armbar attempt — the boy in white controlling the silver-haired opponent's arm. Water energy wraps around the arm like a river. The opponent's AI HUD shows 'PREDICTION: IMPOSSIBLE'. Ultra-dramatic angle. {STYLE}",
     "ref": None},

    {"id": "21_stand_up", "time": "50-52s", "section": "CHORUS",
     "prompt": f"The boy in white gi standing up on the mat, fist raised, teal energy dissipating around him like mist. The arena screens still show ERROR. His black bandaged arm steams. Victory moment but restrained emotion. {STYLE}",
     "ref": ref_nagare},

    # === VERSE 2 (52-65s) — Other characters ===
    {"id": "22_rin_spider", "time": "52-55s", "section": "VERSE2",
     "prompt": f"A 19-year-old girl with short dark red hair in a purple gi, performing a devastating heel hook. Red thread-like lines extend from her limbs like a spider web, trapping her opponent's leg. Intense, confident smirk. {STYLE}",
     "ref": ref_rin},

    {"id": "23_rin_walk", "time": "55-58s", "section": "VERSE2",
     "prompt": f"The red-haired girl in a leather jacket walking through neon-lit city streets at night. A spider tattoo visible on her neck. She's listening to music, looking unbothered. Cool, rebellious vibe. {STYLE}",
     "ref": ref_rin},

    {"id": "24_marcelo", "time": "58-61s", "section": "VERSE2",
     "prompt": f"A large Brazilian man in his 50s with dark skin, grey dreadlocks, and a warm smile, wearing a coral belt (red and white). He sits cross-legged on a beach at sunset, waves behind him. Wise mentor aura. {STYLE}",
     "ref": None},

    {"id": "25_training", "time": "61-65s", "section": "VERSE2",
     "prompt": f"A montage-style composition: multiple panels showing different fighters training — drilling techniques, sparring, doing solo drills. Energy and sweat. The dojo is old but alive with spirit. Manga panel layout style. {STYLE}",
     "ref": None},

    # === CHORUS 2 (65-83s) — Climax ===
    {"id": "26_all_fighters", "time": "65-70s", "section": "CHORUS2",
     "prompt": f"Five fighters standing in a line facing the viewer: center is the boy in white gi (messy black hair), left is silver-haired rival in black, right is red-haired girl in purple, behind them a large Brazilian mentor and a translucent blue AI hologram. Epic group shot. {STYLE}",
     "ref": ref_kv},

    {"id": "27_final_clash", "time": "70-75s", "section": "CHORUS2",
     "prompt": f"The ultimate clash: the boy in white and the silver-haired rival gripping each other's gi, both surrounded by swirling energy — teal water on one side, blue digital data on the other. The energies collide in a shockwave. Maximum intensity. {STYLE}",
     "ref": None},

    {"id": "28_flow_ocean", "time": "75-79s", "section": "CHORUS2",
     "prompt": f"Surreal scene: the boy in white gi floating in a vast dark ocean, eyes closed peacefully. Above the water surface, the arena and spectators are visible. Below, an infinite deep blue. The fourth level of Flow — 'The Ocean'. {STYLE}",
     "ref": None},

    {"id": "29_back_shot", "time": "79-83s", "section": "CHORUS2",
     "prompt": f"The boy in white gi walking into a bright light at the end of a dojo corridor, seen from behind. His left arm's bandages trail in the wind. A faint silhouette of his master appears in the light ahead. Emotional, hopeful. {STYLE}",
     "ref": None},

    # === OUTRO (83-90s) ===
    {"id": "30_logo_final", "time": "83-90s", "section": "OUTRO",
     "prompt": f"The word 'FLOW' dissolving into water droplets against a black background. Below it: 'AIに読めない残像で、世界頂点へ'. Elegant, minimal. The water droplets reform into a small ripple at the bottom. {STYLE}",
     "ref": None},
]

def generate_shot(shot, retry=2):
    """Generate a single PV shot with Gemini."""
    out_path = OUT_DIR / f"{shot['id']}.png"
    if out_path.exists():
        print(f"  ✓ {shot['id']} already exists, skipping")
        return True

    print(f"  → Generating {shot['id']} ({shot['time']}, {shot['section']})")

    contents = []
    if shot.get("ref"):
        contents.append(shot["ref"])
        contents.append(f"Using the character design above as reference, generate this scene:\n\n{shot['prompt']}")
    else:
        contents.append(shot["prompt"])

    for attempt in range(retry + 1):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash-image",
                contents=contents,
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE", "TEXT"],
                )
            )

            for part in response.candidates[0].content.parts:
                if part.inline_data and part.inline_data.mime_type.startswith("image/"):
                    with open(out_path, "wb") as f:
                        f.write(part.inline_data.data)
                    print(f"  ✓ {shot['id']} saved ({out_path.stat().st_size // 1024}KB)")
                    return True

            print(f"  ✗ {shot['id']} no image in response")

        except Exception as e:
            err = str(e)
            print(f"  ✗ {shot['id']} error (attempt {attempt+1}): {err[:100]}")
            if "429" in err or "quota" in err.lower():
                print("  ⏳ Rate limited, waiting 30s...")
                time.sleep(30)
            elif attempt < retry:
                time.sleep(5)

    return False

def main():
    print(f"=== FLOW 90s PV — Generating {len(SHOTS)} shots ===")
    print(f"Output: {OUT_DIR}")
    print()

    success = 0
    for i, shot in enumerate(SHOTS):
        print(f"[{i+1}/{len(SHOTS)}] {shot['section']}: {shot['id']}")
        if generate_shot(shot):
            success += 1
        time.sleep(3)  # Rate limit buffer

    print(f"\n=== Done: {success}/{len(SHOTS)} shots generated ===")
    print(f"Output: {OUT_DIR}")

    # Save shot list for video assembly
    manifest = OUT_DIR / "manifest.json"
    with open(manifest, "w") as f:
        json.dump([{"id": s["id"], "time": s["time"], "section": s["section"]} for s in SHOTS], f, indent=2)
    print(f"Manifest: {manifest}")

if __name__ == "__main__":
    main()
