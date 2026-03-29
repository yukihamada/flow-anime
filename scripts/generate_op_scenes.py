#!/usr/bin/env python3
"""Generate OP scene images for 「0.2%の証明」 — 3 patterns each, parallel."""

import os, sys, time, threading, concurrent.futures
from pathlib import Path
from google import genai
from google.genai import types

API_KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
if not API_KEY:
    sys.exit("Error: GOOGLE_API_KEY not set")

client = genai.Client(api_key=API_KEY)
MODEL = "gemini-3-pro-image-preview"

OUT_DIR = Path(__file__).parent.parent / "images" / "op_scenes"
OUT_DIR.mkdir(parents=True, exist_ok=True)

CHAR_DIR = Path(__file__).parent.parent / "images" / "characters"

def load_ref(name):
    path = CHAR_DIR / f"{name}_sheet.png"
    if not path.exists():
        path = CHAR_DIR / f"{name}_sheet_v2.png"
    if path.exists():
        return types.Part.from_bytes(data=path.read_bytes(), mime_type="image/png")
    return None

refs = {n: load_ref(n) for n in ["nagare", "rio", "marcelo", "rin", "sage"]}

STYLE = """Anime style, cinematic 16:9 widescreen composition. Dark atmosphere with neon blue/cyan accents.
High contrast, dramatic lighting. Studio Bones / MAPPA quality animation frames.
Brazilian Jiu-Jitsu anime set in 2030. Consistent character designs across all scenes."""

SCENES = [
    {
        "id": "intro",
        "lyric": "Perfect logic？ くだらないね / 俺のここには、まだ熱があるんだ",
        "prompt": f"""Close-up of NAGARE's face in shadows. Half his face lit by blue AI holographic screens showing data/numbers.
He's smirking defiantly. His left hand is clenched, wrapped in black bandage, faint heat shimmer rising from it.
Background: dark, cold AI server room aesthetic with floating ERROR text.
{STYLE}""",
        "refs": ["nagare"],
    },
    {
        "id": "v1_shutter",
        "lyric": "錆びついたシャッター 閉ざされた場所 / 手首に巻いた黒帯だけがサイン",
        "prompt": f"""NAGARE (17yo, messy black hair, school uniform) standing alone in front of a RUSTED METAL SHUTTER of an abandoned dojo.
Evening light, long shadows. A black belt is wrapped around his right wrist like a bracelet.
He's touching the rusty shutter with his right hand. Melancholic but determined expression.
Old Japanese neighborhood alley setting, utility poles, warm sunset light contrasting cold shadows.
{STYLE}""",
        "refs": ["nagare"],
    },
    {
        "id": "v1_tatami",
        "lyric": "こいつはもう言うこと聞かない / それでも畳の上に立つ理由がある",
        "prompt": f"""NAGARE standing on old tatami mats in a dimly lit underground dojo. Barefoot.
His LEFT ARM hangs limply, wrapped in dark bandage — clearly damaged/non-functional.
His RIGHT HAND grips a jiu-jitsu gi collar with intense determination.
Single overhead light creating dramatic shadows. Old, worn mats. No AI screens. Analog dojo.
{STYLE}""",
        "refs": ["nagare"],
    },
    {
        "id": "pc1_breath",
        "lyric": "触れれば分かる 呼吸のウソ / データじゃ絶対読めない この一手を",
        "prompt": f"""EXTREME CLOSE-UP of two hands gripping a gi collar during sparring. NAGARE's right hand gripping opponent's collar.
Visible detail: sweat, fabric texture, knuckle tension. Faint blue energy/aura around the grip point.
Background is blurred — abstract water-ink brushstroke effects suggesting "flow state".
Opponent wears an earpiece (AI coaching device) that's glitching with ERROR symbols.
{STYLE}""",
        "refs": ["nagare"],
    },
    {
        "id": "ch1_error",
        "lyric": "水面下で静かに 流れが始まる / 画面の数字を塗り替えろ ERROR ERROR",
        "prompt": f"""WIDE SHOT: NAGARE in white gi mid-technique on the mat, executing a flowing sweep.
ALL SCREENS in the arena showing "ERROR ERROR" in red — AI prediction has failed.
Water/ink visual effects swirling around Nagare like a current beneath the surface.
Spectators' phones and tablets all showing glitched screens. Blue and purple light effects.
The moment of FLOW activation — the world seems to slow down.
{STYLE}""",
        "refs": ["nagare"],
    },
    {
        "id": "ch1_real",
        "lyric": "誰かのコピーじゃない これが俺のリアルだ / 滴から渦へ 巻き込んでいく",
        "prompt": f"""NAGARE standing victoriously on the mat, right fist raised. Behind him, massive water-ink vortex visual effect.
His left arm hangs at his side, bandaged. Sweat and determination on his face.
Above him, shattered holographic AI screens raining down like glass.
The vortex effect transitions from small water drops to a massive whirlpool.
Epic, heroic composition. Title card moment energy.
{STYLE}""",
        "refs": ["nagare"],
    },
    {
        "id": "v2_rio",
        "lyric": "「逃げたんだ」と嗤う 銀髪の友よ / システムの檻で 何を守ってる？",
        "prompt": f"""SPLIT COMPOSITION: Left side — RIO (18yo, silver/light hair, sharp features, SAGE corporate suit)
smirking coldly with holographic AI data floating around him, earpiece glowing blue.
Right side — NAGARE in worn white gi, looking back over his shoulder with defiant eyes.
Between them: a visual divide — cold blue corporate AI world vs warm analog dojo world.
Tension between former friends. Rio's expression hides pain beneath the mockery.
{STYLE}""",
        "refs": ["nagare", "rio"],
    },
    {
        "id": "v2_ocean",
        "lyric": "99.8%の壁だろうと / 残り0.2の空白に 海は広がってる",
        "prompt": f"""SURREAL COMPOSITION: NAGARE standing at the edge of a vast dark ocean.
Above him: massive holographic display showing "99.8%" cracking apart.
Through the crack, an infinite ocean is visible — deep blue, mysterious, beautiful.
NAGARE reaching toward the 0.2% gap with his right hand. His left arm bandaged at his side.
The ocean represents the unknown, the unpredictable — "Flow".
Water-ink art style blending with futuristic holographic elements.
{STYLE}""",
        "refs": ["nagare"],
    },
    {
        "id": "bridge_style",
        "lyric": "残像を追いかけるのは もうやめた / 右手一本で紡ぐ 新しいスタイル",
        "prompt": f"""NAGARE in a unique one-armed fighting stance on the mat. His style is unlike any textbook.
Right hand forward, left arm tucked/wrapped against his body.
Behind him: fading ghost images (afterimages/残像) of his MASTER KAIDO dissolving into mist.
In front of him: his OWN PATH forming as water-ink trails on the ground.
Multiple exposure effect showing his movement creating something new.
Dojo setting with old mats, warm-cool light contrast.
{STYLE}""",
        "refs": ["nagare"],
    },
    {
        "id": "last_flow",
        "lyric": "滴から渦、そして未知の海へ / 流れる水は、終わらない",
        "prompt": f"""EPIC FINAL COMPOSITION — Title card quality.
NAGARE at center, surrounded by all stages of FLOW:
- Small water DROPS (滴/shizuku) at his feet
- FLOWING water (流/nagare) spiraling around his legs
- A massive VORTEX (渦/uzu) behind him
- And above: an infinite OCEAN (海/umi) stretching to the horizon
His allies visible in the background: RIN (red-haired girl), RIO (silver-haired rival), LUCIANO (old Brazilian master).
All water effects in blue/cyan/purple gradient. Stars and aurora in the sky.
The feeling of an endless journey. "The flowing water never ends."
{STYLE}""",
        "refs": ["nagare", "rio", "marcelo", "rin"],
    },
]

lock = threading.Lock()
success_count = 0
fail_count = 0

def generate_scene(scene, pattern):
    global success_count, fail_count
    scene_id = scene["id"]
    out_path = OUT_DIR / f"{scene_id}_{pattern}.png"
    if out_path.exists():
        with lock:
            print(f"  [SKIP] {scene_id}_{pattern} (exists)")
            success_count += 1
        return

    ref_parts = [refs[r] for r in scene.get("refs", []) if refs.get(r)]
    variation = ["dramatic low angle", "eye-level cinematic", "overhead bird's eye"][pattern - 1]

    prompt_text = f"""{scene['prompt']}

Camera angle variation: {variation}. Pattern {pattern} of 3 — make this distinct from other angles.
Add slight variation in lighting and composition while keeping the same scene concept.
Output a single anime illustration in 16:9 widescreen aspect ratio."""

    parts = ref_parts + [prompt_text]

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=parts,
                config=types.GenerateContentConfig(
                    response_modalities=["image", "text"],
                    temperature=1.0,
                ),
            )
            for part in response.candidates[0].content.parts:
                if part.inline_data and part.inline_data.mime_type.startswith("image/"):
                    out_path.write_bytes(part.inline_data.data)
                    with lock:
                        success_count += 1
                        print(f"  [OK] {scene_id}_{pattern} -> {out_path.name}")
                    return
            with lock:
                print(f"  [WARN] {scene_id}_{pattern} — no image in response")
                fail_count += 1
            return
        except Exception as e:
            err = str(e)
            if "429" in err or "RESOURCE_EXHAUSTED" in err:
                wait = 15 * (attempt + 1)
                with lock:
                    print(f"  [RATE] {scene_id}_{pattern} — waiting {wait}s...")
                time.sleep(wait)
            else:
                with lock:
                    print(f"  [ERR] {scene_id}_{pattern} — {err[:100]}")
                    fail_count += 1
                return


if __name__ == "__main__":
    print(f"=== FLOW OP Scene Generator ===")
    print(f"Scenes: {len(SCENES)}, Patterns: 3 each, Total: {len(SCENES) * 3}")
    print(f"Output: {OUT_DIR}\n")

    tasks = []
    for scene in SCENES:
        for pat in [1, 2, 3]:
            tasks.append((scene, pat))

    # Use 3 workers to avoid rate limiting
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(generate_scene, s, p) for s, p in tasks]
        concurrent.futures.wait(futures)

    print(f"\n=== Done: {success_count} OK, {fail_count} failed ===")
