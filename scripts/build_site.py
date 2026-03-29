#!/usr/bin/env python3
"""Build the full FLOW site with embedded story content."""
import re
from pathlib import Path

BASE = Path(__file__).parent.parent
STORY_DIR = BASE / "story"

def md_to_html(md_text):
    """Simple markdown to HTML converter for episode guides."""
    lines = md_text.strip().split('\n')
    html_parts = []
    for line in lines:
        line = line.rstrip()
        if not line:
            html_parts.append('')
            continue
        # Headers
        if line.startswith('# '):
            continue  # Skip top-level headers (we handle them separately)
        if line.startswith('## '):
            title = line[3:]
            html_parts.append(f'<h3 class="ep-h">{title}</h3>')
            continue
        if line.startswith('### '):
            html_parts.append(f'<h4>{line[4:]}</h4>')
            continue
        # Bold
        line = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', line)
        # Italic
        line = re.sub(r'\*(.+?)\*', r'<em>\1</em>', line)
        # Horizontal rules
        if line.startswith('---'):
            html_parts.append('<hr class="ep-hr">')
            continue
        # Tables (skip for now, too complex)
        if line.startswith('|'):
            continue
        # Regular paragraph
        html_parts.append(f'<p>{line}</p>')
    return '\n'.join(html_parts)

# Read all episode guides
seasons_data = []
for i in range(1, 6):
    path = STORY_DIR / f"episode_guide_s{i}.md"
    if path.exists():
        text = path.read_text()
        # Extract title from first line
        title_match = re.search(r'#\s+FLOW\s+(.+)', text)
        title = title_match.group(1) if title_match else f"Season {i}"
        html_content = md_to_html(text)
        seasons_data.append({"num": i, "title": title, "html": html_content})

# Read series bible
bible_path = STORY_DIR / "series_bible.md"
bible_html = md_to_html(bible_path.read_text()) if bible_path.exists() else ""

# Build the full HTML
html = f'''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta property="og:title" content="FLOW — AIに読めない柔術で、世界の頂点へ">
<meta property="og:description" content="BJJ x AI anime — 60 episodes, 5 seasons, complete production bible">
<meta property="og:image" content="/images/keyvisual/kv_main.png">
<title>FLOW — AIに読めない柔術で、世界の頂点へ</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;700;900&display=swap');
*{{margin:0;padding:0;box-sizing:border-box}}
:root{{--bg:#08080d;--s1:#111119;--s2:#1a1a26;--s3:#222233;--ac:#4a9eff;--ac2:#00d4ff;--ac3:#7c5cff;
  --tx:#e8e8f0;--dim:#7777aa;--nagare:#3366cc;--rio:#99bbee;--luciano:#cc8844;--rin:#cc3344;--sage:#44ddff}}
body{{background:var(--bg);color:var(--tx);font-family:'Noto Sans JP',sans-serif;overflow-x:hidden}}
::-webkit-scrollbar{{width:5px}}::-webkit-scrollbar-thumb{{background:var(--s3);border-radius:3px}}
a{{color:var(--ac);text-decoration:none}}a:hover{{color:var(--ac2)}}

nav{{position:fixed;top:0;left:0;right:0;z-index:100;background:rgba(8,8,13,0.92);backdrop-filter:blur(16px);
  border-bottom:1px solid rgba(255,255,255,0.04);display:flex;align-items:center;height:50px;padding:0 1.5rem}}
.nav-logo{{font-weight:900;font-size:1.1rem;letter-spacing:0.15em;margin-right:2rem;
  background:linear-gradient(90deg,#fff,var(--ac2));-webkit-background-clip:text;-webkit-text-fill-color:transparent}}
nav a{{color:var(--dim);font-size:0.72rem;letter-spacing:0.06em;padding:0 0.7rem;line-height:50px;
  border-bottom:2px solid transparent;transition:all 0.2s;white-space:nowrap}}
nav a:hover,nav a.active{{color:var(--tx);border-bottom-color:var(--ac)}}
.nav-links{{display:flex;gap:0;overflow-x:auto;flex:1}}

.hero{{height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;
  position:relative;background:url('images/keyvisual/kv_main.png') center/cover}}
.hero::before{{content:'';position:absolute;inset:0;background:rgba(8,8,13,0.72)}}
.hero *{{position:relative;z-index:1}}
.hero-title{{font-size:clamp(5rem,14vw,11rem);font-weight:900;letter-spacing:0.3em;
  background:linear-gradient(135deg,#fff,var(--ac2),var(--ac));-webkit-background-clip:text;-webkit-text-fill-color:transparent}}
.hero-sub{{font-size:clamp(0.8rem,2vw,1.1rem);color:var(--dim);letter-spacing:0.4em;font-weight:300;margin-top:0.5rem}}
.hero-tag{{font-size:clamp(1rem,2.5vw,1.4rem);margin-top:1.5rem;font-weight:400}}
.hero-cta{{margin-top:2.5rem;display:flex;gap:1rem;flex-wrap:wrap;justify-content:center}}
.btn{{padding:0.7rem 2rem;border-radius:100px;border:none;font-family:inherit;font-size:0.85rem;font-weight:700;cursor:pointer;transition:all 0.2s}}
.btn-p{{background:linear-gradient(135deg,var(--ac),var(--ac3));color:#fff}}
.btn-p:hover{{transform:scale(1.05);box-shadow:0 8px 30px rgba(74,158,255,0.3)}}
.btn-g{{background:transparent;color:var(--tx);border:1px solid rgba(255,255,255,0.15)}}
.btn-g:hover{{border-color:var(--ac)}}
.scroll-hint{{position:absolute;bottom:2rem;color:var(--dim);font-size:0.7rem;letter-spacing:0.15em;
  animation:float 3s ease infinite;z-index:1}}
@keyframes float{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-8px)}}}}

section{{padding:4rem 2rem;max-width:1400px;margin:0 auto}}
.stitle{{font-size:1.6rem;font-weight:900;background:linear-gradient(90deg,var(--ac),var(--ac2));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent}}
.ssub{{color:var(--dim);margin-bottom:2rem;font-size:0.8rem;margin-top:0.3rem}}
.divider{{height:1px;background:linear-gradient(90deg,transparent,rgba(74,158,255,0.15),transparent);margin:0 auto;max-width:600px}}

.g2{{display:grid;grid-template-columns:repeat(2,1fr);gap:1.2rem}}
.g3{{display:grid;grid-template-columns:repeat(3,1fr);gap:1.2rem}}
.g4{{display:grid;grid-template-columns:repeat(4,1fr);gap:1rem}}
.g5{{display:grid;grid-template-columns:repeat(5,1fr);gap:1rem}}
@media(max-width:900px){{.g5,.g4{{grid-template-columns:repeat(2,1fr)}}.g3{{grid-template-columns:1fr 1fr}}}}
@media(max-width:500px){{.g5,.g4,.g3,.g2{{grid-template-columns:1fr}}}}

.card{{background:var(--s1);border-radius:14px;overflow:hidden;cursor:pointer;transition:all 0.3s;border:2px solid transparent}}
.card:hover{{transform:translateY(-5px);border-color:var(--ac);box-shadow:0 16px 50px rgba(0,0,0,0.4)}}
.card img{{width:100%;aspect-ratio:1;object-fit:cover;object-position:top}}
.card .ci{{padding:0.8rem 1rem}}
.card .cn{{font-weight:900;font-size:0.95rem}}
.card .cs{{font-size:0.72rem;color:var(--dim);margin-top:0.15rem}}

/* Flow cards */
.fc{{background:var(--s2);border-radius:14px;overflow:hidden;border-left:3px solid;cursor:pointer;transition:all 0.3s}}
.fc:hover{{transform:scale(1.02);box-shadow:0 10px 30px rgba(0,0,0,0.3)}}
.fc img{{width:100%;aspect-ratio:1;object-fit:cover}}
.fc-b{{padding:1rem}}
.fc-lv{{font-size:0.65rem;color:var(--dim);text-transform:uppercase;letter-spacing:0.12em}}
.fc-nm{{font-size:1.3rem;font-weight:900;margin:0.15rem 0}}
.fc-fx{{font-size:0.75rem;color:var(--dim);line-height:1.4}}
.fc-cost{{font-size:0.7rem;color:#ff6666;margin-top:0.3rem}}

/* SAGE compare */
.sage-wrap{{position:relative;border-radius:16px;overflow:hidden;cursor:col-resize;user-select:none;aspect-ratio:1;max-width:700px;margin:0 auto}}
.sage-wrap img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
.sage-wrap .sa{{clip-path:inset(0 0 0 50%)}}
.sage-slider{{position:absolute;top:0;bottom:0;width:3px;background:var(--ac);left:50%;z-index:5}}
.sage-slider::after{{content:'\\2194';position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
  width:32px;height:32px;border-radius:50%;background:var(--ac);display:flex;align-items:center;justify-content:center;
  font-size:0.8rem;color:#fff;box-shadow:0 0 15px rgba(74,158,255,0.5)}}
.sage-labels{{display:flex;justify-content:space-between;margin-top:0.8rem}}
.sage-labels span{{font-size:0.75rem;font-weight:700}}

/* Story reader */
.story-tabs{{display:flex;gap:0.3rem;flex-wrap:wrap;margin-bottom:1.5rem}}
.story-tab{{padding:0.4rem 1rem;border-radius:100px;border:1px solid rgba(255,255,255,0.08);background:transparent;
  color:var(--dim);cursor:pointer;font-size:0.72rem;transition:all 0.2s;font-family:inherit}}
.story-tab.active{{background:var(--ac);color:var(--bg);border-color:var(--ac);font-weight:700}}
.story-tab:hover:not(.active){{border-color:var(--ac)}}
.story-content{{background:var(--s1);border-radius:16px;padding:2rem;line-height:2;font-size:0.88rem;max-height:70vh;overflow-y:auto}}
.story-content h3.ep-h{{font-size:1.1rem;font-weight:900;color:var(--ac);margin:2rem 0 0.5rem;padding-top:1.5rem;border-top:1px solid rgba(255,255,255,0.05)}}
.story-content h3.ep-h:first-child{{margin-top:0;padding-top:0;border-top:none}}
.story-content p{{margin-bottom:0.5rem;color:var(--dim)}}
.story-content p strong{{color:var(--tx)}}
.story-content hr.ep-hr{{border:none;height:1px;background:rgba(255,255,255,0.06);margin:1.5rem 0}}

/* Scene cards */
.sc{{background:var(--s1);border-radius:14px;overflow:hidden;cursor:pointer;transition:all 0.3s;border:2px solid transparent}}
.sc:hover{{transform:translateY(-5px);border-color:var(--ac);box-shadow:0 16px 50px rgba(0,0,0,0.4)}}
.sc img{{width:100%;aspect-ratio:1;object-fit:cover}}
.sc-i{{padding:0.8rem 1rem}}
.sc-ep{{font-size:0.65rem;color:var(--ac);font-weight:700;letter-spacing:0.08em}}
.sc-t{{font-weight:900;margin-top:0.15rem;font-size:0.9rem}}
.sc-d{{font-size:0.72rem;color:var(--dim);margin-top:0.2rem;line-height:1.4}}

/* Modal */
.mo{{display:none;position:fixed;inset:0;background:rgba(0,0,0,0.9);backdrop-filter:blur(12px);z-index:1000;align-items:center;justify-content:center;padding:1rem}}
.mo.on{{display:flex}}.mo-c{{background:var(--s1);border-radius:20px;max-width:900px;width:100%;max-height:92vh;overflow-y:auto;
  position:relative;border:1px solid rgba(255,255,255,0.08)}}
.mo-x{{position:sticky;top:0.8rem;float:right;margin-right:0.8rem;width:34px;height:34px;border-radius:50%;
  border:none;background:rgba(255,255,255,0.08);color:white;font-size:1rem;cursor:pointer;z-index:10}}
.mo-x:hover{{background:rgba(255,255,255,0.15)}}
.mo-c img.mi{{width:100%;border-radius:20px 20px 0 0}}
.mo-c .mb{{padding:1.5rem}}

footer{{text-align:center;padding:3rem;color:var(--dim);font-size:0.7rem;border-top:1px solid rgba(255,255,255,0.04)}}
footer a{{color:var(--ac)}}
</style>
</head>
<body>

<nav>
  <div class="nav-logo">FLOW</div>
  <div class="nav-links">
    <a href="#kv">Key Visual</a>
    <a href="#chars">Characters</a>
    <a href="#expr">Expressions</a>
    <a href="#flow">Flow System</a>
    <a href="#ui">SAGE UI</a>
    <a href="#scenes">Scenes</a>
    <a href="#story">Story</a>
    <a href="#review">Review</a>
  </div>
</nav>

<div class="hero">
  <div class="hero-title">FLOW</div>
  <div class="hero-sub">COMPLETE PRODUCTION BIBLE</div>
  <div class="hero-tag">AIに読めない柔術で、世界の頂点へ</div>
  <div class="hero-cta">
    <button class="btn btn-p" onclick="document.getElementById('story').scrollIntoView({{behavior:'smooth'}})">Read Story</button>
    <a href="review.html" class="btn btn-g">Review & Vote</a>
  </div>
  <div class="scroll-hint">SCROLL</div>
</div>

<!-- KEY VISUALS -->
<section id="kv">
  <div class="stitle">KEY VISUALS</div><div class="ssub">Click to enlarge</div>
  <div class="g3">
    <div class="card" onclick="showImg(this)"><img src="images/keyvisual/kv_main.png"><div class="ci"><div class="cn">MAIN POSTER</div><div class="cs">全キャラ集合メインビジュアル</div></div></div>
    <div class="card" onclick="showImg(this)"><img src="images/keyvisual/kv_flow_awakening.png"><div class="ci"><div class="cn">FLOW AWAKENING</div><div class="cs">現実と水墨画の境界が溶ける覚醒シーン</div></div></div>
    <div class="card" onclick="showImg(this)"><img src="images/keyvisual/kv_rivals.png"><div class="ci"><div class="cn">RIVALS</div><div class="cs">流 vs 理央 — 人間の直感 vs 機械の最適解</div></div></div>
  </div>
</section><div class="divider"></div>

<!-- CHARACTERS -->
<section id="chars">
  <div class="stitle">CHARACTERS</div><div class="ssub">5 main characters</div>
  <div class="g5">
    <div class="card" onclick="showImg(this)"><img src="images/characters/nagare_sheet.png"><div class="ci"><div class="cn" style="color:var(--nagare)">NAGARE</div><div class="cs">流 — 主人公</div></div></div>
    <div class="card" onclick="showImg(this)"><img src="images/characters/rio_sheet.png"><div class="ci"><div class="cn" style="color:var(--rio)">RIO</div><div class="cs">理央 — ライバル</div></div></div>
    <div class="card" onclick="showImg(this)"><img src="images/characters/marcelo_sheet.png"><div class="ci"><div class="cn" style="color:var(--luciano)">LUCIANO</div><div class="cs">ルシアーノ — 師匠</div></div></div>
    <div class="card" onclick="showImg(this)"><img src="images/characters/rin_sheet.png"><div class="ci"><div class="cn" style="color:var(--rin)">RIN</div><div class="cs">凛 — 同志</div></div></div>
    <div class="card" onclick="showImg(this)"><img src="images/characters/sage_sheet.png"><div class="ci"><div class="cn" style="color:var(--sage)">SAGE</div><div class="cs">セージ — AI</div></div></div>
  </div>
</section><div class="divider"></div>

<!-- EXPRESSIONS -->
<section id="expr">
  <div class="stitle">EXPRESSION SHEETS</div><div class="ssub">6 expressions per character</div>
  <div class="g5">
    <div class="card" onclick="showImg(this)"><img src="images/expressions/nagare_expressions.png"><div class="ci"><div class="cn" style="color:var(--nagare)">NAGARE</div></div></div>
    <div class="card" onclick="showImg(this)"><img src="images/expressions/rio_expressions.png"><div class="ci"><div class="cn" style="color:var(--rio)">RIO</div></div></div>
    <div class="card" onclick="showImg(this)"><img src="images/expressions/marcelo_expressions.png"><div class="ci"><div class="cn" style="color:var(--luciano)">LUCIANO</div></div></div>
    <div class="card" onclick="showImg(this)"><img src="images/expressions/rin_expressions.png"><div class="ci"><div class="cn" style="color:var(--rin)">RIN</div></div></div>
    <div class="card" onclick="showImg(this)"><img src="images/expressions/sage_expressions.png"><div class="ci"><div class="cn" style="color:var(--sage)">SAGE</div></div></div>
  </div>
</section><div class="divider"></div>

<!-- FLOW SYSTEM -->
<section id="flow">
  <div class="stitle">FLOW SYSTEM</div><div class="ssub">4 levels of awakening</div>
  <div class="g4">
    <div class="fc" style="border-color:#6699cc" onclick="showImg(this)"><img src="images/flow_art/flow_lv1_shizuku.png"><div class="fc-b"><div class="fc-lv">Level 1</div><div class="fc-nm" style="color:#6699cc">滴 Shizuku</div><div class="fc-fx">一瞬だけAI予測を外す</div><div class="fc-cost">代償: 軽い疲労</div></div></div>
    <div class="fc" style="border-color:#4488dd" onclick="showImg(this)"><img src="images/flow_art/flow_lv2_nagare.png"><div class="fc-b"><div class="fc-lv">Level 2</div><div class="fc-nm" style="color:#4488dd">流 Nagare</div><div class="fc-fx">3〜5手が連続する水の流れ</div><div class="fc-cost">代償: 左半身の痺れ</div></div></div>
    <div class="fc" style="border-color:#2266ee" onclick="showImg(this)"><img src="images/flow_art/flow_lv3_uzu.png"><div class="fc-b"><div class="fc-lv">Level 3</div><div class="fc-nm" style="color:#2266ee">渦 Uzu</div><div class="fc-fx">相手もフロウに引き込む。全AI停止</div><div class="fc-cost">代償: 意識朦朧</div></div></div>
    <div class="fc" style="border-color:#0044ff" onclick="showImg(this)"><img src="images/flow_art/flow_lv4_umi.png"><div class="fc-b"><div class="fc-lv">Level 4</div><div class="fc-nm" style="color:#0044ff">海 Umi</div><div class="fc-fx">海堂だけが到達した未知の領域</div><div class="fc-cost">代償: ???</div></div></div>
  </div>
</section><div class="divider"></div>

<!-- SAGE UI -->
<section id="ui">
  <div class="stitle">SAGE UI DESIGN</div><div class="ssub">Drag slider to compare Normal vs Glitch</div>
  <div class="sage-wrap" id="sw">
    <img src="images/sage_ui/sage_ui_normal.png" class="sb">
    <img src="images/sage_ui/sage_ui_glitch.png" class="sa">
    <div class="sage-slider" id="ss"></div>
  </div>
  <div class="sage-labels"><span style="color:var(--ac2)">NORMAL</span><span style="color:#ff4466">GLITCH — FLOW DETECTED</span></div>
</section><div class="divider"></div>

<!-- SCENES -->
<section id="scenes">
  <div class="stitle">SCENE CONCEPT ART</div><div class="ssub">Key story moments</div>
  <div class="g3">
    <div class="sc" onclick="showImg(this)"><img src="images/scenes/scene_ep1_kaido.png"><div class="sc-i"><div class="sc-ep">EP.01</div><div class="sc-t">残像</div><div class="sc-d">海堂 vs ヴィクトル。SAGE予測99.7%を覆す</div></div></div>
    <div class="sc" onclick="showImg(this)"><img src="images/scenes/scene_ep6_rin_spider.png"><div class="sc-i"><div class="sc-ep">EP.06</div><div class="sc-t">蜘蛛</div><div class="sc-d">凛の登場。足関節の蜘蛛の巣</div></div></div>
    <div class="sc" onclick="showImg(this)"><img src="images/scenes/scene_ep10_awakening.png"><div class="sc-i"><div class="sc-ep">EP.10</div><div class="sc-t">流</div><div class="sc-d">フロウ初発動。全AI画面にERR</div></div></div>
    <div class="sc" onclick="showImg(this)"><img src="images/scenes/scene_ep12_reunion.png"><div class="sc-i"><div class="sc-ep">EP.12</div><div class="sc-t">逃亡者</div><div class="sc-d">理央が道場に現れる</div></div></div>
    <div class="sc" onclick="showImg(this)"><img src="images/scenes/scene_s4_sage_reveal.png"><div class="sc-i"><div class="sc-ep">S4</div><div class="sc-t">SAGEの真実</div><div class="sc-d">サーバー室。取り込まれた海堂</div></div></div>
  </div>
</section><div class="divider"></div>

<!-- STORY -->
<section id="story">
  <div class="stitle">FULL STORY — 全60話</div>
  <div class="ssub">Complete episode guide for all 5 seasons</div>
  <div class="story-tabs" id="storyTabs"></div>
  <div class="story-content" id="storyContent"></div>
</section>

<footer>
  FLOW Production Bible v1.1 — <a href="review.html">Review & Vote</a>
</footer>

<!-- Modal -->
<div class="mo" id="mo" onclick="if(event.target===this)this.classList.remove('on')">
  <div class="mo-c"><button class="mo-x" onclick="document.getElementById('mo').classList.remove('on')">x</button><div id="mi"></div></div>
</div>

<script>
// Story data
const storyData = [
''' + ',\n'.join([
    f'  {{num:{s["num"]},title:{repr(s["title"])},html:{repr(s["html"])}}}'
    for s in seasons_data
]) + '''
];

// Story tabs
const stabs = document.getElementById('storyTabs');
const scont = document.getElementById('storyContent');
storyData.forEach((s, i) => {
  const btn = document.createElement('button');
  btn.className = 'story-tab' + (i === 0 ? ' active' : '');
  btn.textContent = `S${s.num} ${s.title.split('」')[0]}」`;
  btn.onclick = () => {
    document.querySelectorAll('.story-tab').forEach(t => t.classList.remove('active'));
    btn.classList.add('active');
    scont.innerHTML = s.html;
    scont.scrollTop = 0;
  };
  stabs.appendChild(btn);
});
scont.innerHTML = storyData[0].html;

// Image modal
function showImg(el) {
  const img = el.querySelector('img');
  const name = el.querySelector('.cn,.fc-nm,.sc-t');
  const desc = el.querySelector('.cs,.fc-fx,.sc-d');
  document.getElementById('mi').innerHTML =
    `<img class="mi" src="${img.src}" style="cursor:zoom-in" onclick="window.open('${img.src}','_blank')">` +
    `<div class="mb"><h2 style="font-size:1.3rem;font-weight:900">${name?name.textContent:''}</h2>` +
    `${desc?'<p style="color:var(--dim);margin-top:0.5rem">'+desc.textContent+'</p>':''}` +
    `<p style="font-size:0.7rem;color:var(--dim);margin-top:0.8rem">Click image for full size</p></div>`;
  document.getElementById('mo').classList.add('on');
}
document.addEventListener('keydown', e => { if (e.key === 'Escape') document.getElementById('mo').classList.remove('on'); });

// SAGE slider
const sw = document.getElementById('sw');
const sa = sw.querySelector('.sa');
const ss = document.getElementById('ss');
let dragging = false;
function updateSlider(x) {
  const r = sw.getBoundingClientRect();
  let p = Math.max(0, Math.min(100, (x - r.left) / r.width * 100));
  sa.style.clipPath = `inset(0 0 0 ${p}%)`;
  ss.style.left = p + '%';
}
sw.addEventListener('mousedown', () => dragging = true);
document.addEventListener('mousemove', e => { if (dragging) updateSlider(e.clientX); });
document.addEventListener('mouseup', () => dragging = false);
sw.addEventListener('touchmove', e => { updateSlider(e.touches[0].clientX); e.preventDefault(); }, { passive: false });

// Smooth nav
document.querySelectorAll('nav a').forEach(a => a.addEventListener('click', e => {
  e.preventDefault();
  const t = document.querySelector(a.getAttribute('href'));
  if (t) t.scrollIntoView({ behavior: 'smooth', block: 'start' });
}));
</script>
</body>
</html>'''

out_path = BASE / "index.html"
out_path.write_text(html)
print(f"Built {out_path} ({len(html)} bytes)")
print(f"Embedded {len(seasons_data)} seasons of story content")
