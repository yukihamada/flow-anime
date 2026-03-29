"""FLOW PV — 10 selected cuts → Veo 3 video with dialogue
Usage: python3 gen_pv_veo3.py
"""
import os, time, json, base64
from pathlib import Path
from google import genai
from google.genai import types

API_KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
client = genai.Client(api_key=API_KEY)

SHOTS_DIR = Path(__file__).parent.parent / "images" / "pv_shots"
OUT_DIR = Path(__file__).parent.parent / "videos" / "pv_veo3"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# 10 selected cuts with scene direction + dialogue
CUTS = [
    {
        "id": "02_dojo_dawn",
        "dur": 5,
        "prompt": "Slow cinematic pan across an empty traditional Japanese dojo at dawn. Dust particles float in golden sunlight streaming through wooden shutters. A black belt hangs on the wall, swaying slightly in a gentle breeze. Peaceful, serene atmosphere. No dialogue, ambient sounds of birds and wind.",
    },
    {
        "id": "04_nagare_bandage",
        "dur": 5,
        "prompt": "Close-up of a young anime man with messy black hair slowly raising his left arm wrapped in black bandages. His fist clenches tight, teal energy lines pulse through the bandages. He speaks with quiet intensity. Male teen voice says in Japanese: 'この左手にはまだ熱があるんだ' (This left hand still has fire in it). Dark moody lighting.",
    },
    {
        "id": "05_nagare_tatami",
        "dur": 5,
        "prompt": "A young man in white jiu-jitsu gi stands alone on a tatami mat, seen from behind. He slowly turns his head to look over his shoulder with determined eyes. Atmospheric wind blows his gi. Male teen voice whispers in Japanese: '畳の上に立つ理由がある' (There's a reason I stand on this mat). Melancholic, emotional.",
    },
    {
        "id": "10_breathe",
        "dur": 5,
        "prompt": "A boy in white gi sitting in seiza meditation position on tatami. Water-like energy ripples slowly emanate from beneath him, expanding outward. He breathes deeply, chest rising and falling. Calm before the storm. Sound of deep breathing and water droplets echoing. No dialogue.",
    },
    {
        "id": "13_face_off",
        "dur": 5,
        "prompt": "Split-screen dramatic face-off: left side a boy with messy black hair in white gi, right side a young man with silver hair in black AI suit. Both stare intensely at each other. A crack of light divides them, growing brighter. Silver-haired rival speaks coldly in Japanese: '感覚？そんな曖昧なものに命を預けるのか' (Instinct? You'd trust your life to something so vague?). Tension building, dramatic music swell.",
    },
    {
        "id": "15_flow_activate",
        "dur": 5,
        "prompt": "The boy in white gi's eyes suddenly glow teal. Water-like energy EXPLODES from his body in a shockwave. Holographic ERROR screens shatter around the arena. His black bandaged arm crackles with dark energy. He yells in Japanese: '流れろ！' (FLOW!). Massive energy burst, camera shakes, epic moment. Crowd gasps.",
    },
    {
        "id": "18_error_screens",
        "dur": 4,
        "prompt": "Multiple holographic screens in a dark arena all glitching simultaneously, displaying 'ERR' and 'ERROR' in red. Numbers scrambling. The AI system is crashing. Screens crack and shatter like glass. A robotic female voice says: 'PREDICTION FAILURE. ALL MODELS OFFLINE.' Cyberpunk glitch aesthetic with alarm sounds.",
    },
    {
        "id": "20_submission",
        "dur": 5,
        "prompt": "Intense jiu-jitsu armbar scene. The boy in white gi controls his opponent's arm on the ground, applying pressure. Water energy wraps around the arm like a flowing river. Close-up of faces showing effort and determination. The boy says through gritted teeth in Japanese: 'これが俺の柔術だ' (This is MY jiu-jitsu). Sounds of exertion and the mat creaking.",
    },
    {
        "id": "23_rin_walk",
        "dur": 5,
        "prompt": "A cool young woman with short dark red hair in a leather jacket walking through neon-lit city streets at night. A spider tattoo is visible on her neck. She pulls out earbuds and smirks confidently. She says casually in Japanese: '足を取ったら終わり。つまらないから、AIなんて使わない' (Once I grab your leg, it's over. AI is boring, so I don't use it). City ambient sounds, confident attitude.",
    },
    {
        "id": "29_back_shot",
        "dur": 6,
        "prompt": "The boy in white gi walking toward a bright light at the end of a dojo corridor, seen from behind. His black bandages trail in the wind. A faint silhouette of his master appears in the light ahead. He walks steadily forward. Male voice narrates in Japanese: '流れる水は、もう誰にも止められない' (Flowing water can no longer be stopped by anyone). Emotional, hopeful, the light grows brighter. Fade to white.",
    },
]


def generate_video(cut, retry=2):
    out_path = OUT_DIR / f"{cut['id']}.mp4"
    if out_path.exists():
        print(f"  ✓ {cut['id']} already exists, skipping")
        return True

    img_path = SHOTS_DIR / f"{cut['id']}.png"
    if not img_path.exists():
        print(f"  ✗ {cut['id']} image not found")
        return False

    print(f"  → Generating {cut['id']} ({cut['dur']}s) with Veo 3...")

    with open(img_path, "rb") as f:
        img_data = f.read()

    image_part = types.Image(image_bytes=img_data, mime_type="image/png")

    for attempt in range(retry + 1):
        try:
            op = client.models.generate_videos(
                model="veo-3.0-generate-001",
                prompt=cut["prompt"],
                image=image_part,
                config=types.GenerateVideosConfig(
                    aspect_ratio="16:9",
                    number_of_videos=1,
                    duration_seconds=8,
                    person_generation="allow_adult",
                ),
            )

            print(f"  ⏳ Waiting for video generation (operation: {op.name})...")

            while not op.done:
                time.sleep(10)
                op = client.operations.get(op)
                print(f"    ... still processing")

            if op.result and op.result.generated_videos:
                video = op.result.generated_videos[0]
                print(f"  📥 Downloading video...")
                # Try different download methods
                try:
                    vid_data = video.video
                    if hasattr(vid_data, 'uri') and vid_data.uri:
                        # Download from URI via files API
                        resp = client.files.download(file=vid_data)
                        video_bytes = resp if isinstance(resp, bytes) else resp.read()
                    elif hasattr(vid_data, 'video_bytes') and vid_data.video_bytes:
                        video_bytes = vid_data.video_bytes
                    elif hasattr(video, 'video_bytes') and video.video_bytes:
                        video_bytes = video.video_bytes
                    else:
                        # Try direct attribute access
                        import httpx
                        uri = str(vid_data.uri if hasattr(vid_data, 'uri') else vid_data)
                        print(f"  📥 Downloading from URI: {uri[:80]}...")
                        r = httpx.get(uri, timeout=120)
                        video_bytes = r.content
                except Exception as dl_err:
                    print(f"  ⚠ Download method 1 failed: {dl_err}")
                    # Fallback: try to get bytes directly
                    video_bytes = getattr(video, 'video_bytes', None) or getattr(video.video, 'video_bytes', None)

                if video_bytes:
                    with open(out_path, "wb") as f:
                        f.write(video_bytes)
                    print(f"  ✓ {cut['id']} saved ({out_path.stat().st_size // 1024}KB)")
                    return True
                else:
                    print(f"  ✗ {cut['id']} could not extract video bytes")
                    print(f"    video attrs: {dir(video)}")
                    print(f"    video.video attrs: {dir(video.video) if hasattr(video, 'video') else 'N/A'}")
            else:
                print(f"  ✗ {cut['id']} no video in result")
                if op.result:
                    print(f"    result attrs: {dir(op.result)}")

        except Exception as e:
            err = str(e)
            print(f"  ✗ {cut['id']} error (attempt {attempt+1}): {err[:200]}")
            if "429" in err or "quota" in err.lower():
                print("  ⏳ Rate limited, waiting 60s...")
                time.sleep(60)
            elif attempt < retry:
                time.sleep(10)

    return False


def main():
    print(f"=== FLOW PV — Veo 3 Video Generation ({len(CUTS)} cuts) ===")
    print(f"Output: {OUT_DIR}\n")

    success = 0
    for i, cut in enumerate(CUTS):
        print(f"[{i+1}/{len(CUTS)}] {cut['id']}")
        if generate_video(cut):
            success += 1
        time.sleep(5)

    print(f"\n=== Done: {success}/{len(CUTS)} videos generated ===")
    print(f"Output: {OUT_DIR}")

    # List results
    for f in sorted(OUT_DIR.glob("*.mp4")):
        print(f"  {f.name} ({f.stat().st_size // 1024}KB)")


if __name__ == "__main__":
    main()
