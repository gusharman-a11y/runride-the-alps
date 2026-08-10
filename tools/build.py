#!/usr/bin/env python3
"""Build the trip journal and photo gallery from ig/manifest.json + tools/days.py.

    python3 tools/build.py

Writes journal.html, journal/<slug>.html and gallery.html. Everything it emits is
generated: edit the data in tools/days.py or the templates here, never the output.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from days import DAYS, PROFILE, TOTALS  # noqa: E402

SITE = "https://www.thesouthend.co"

# ---------------------------------------------------------------- shared chrome

CSS = """
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --ink:#16161A;--paper:#EDEBE5;--paper-2:#E4E1D8;--stone:#9A988F;
  --line:rgba(22,22,26,0.13);--line-soft:rgba(22,22,26,0.08);--clay:#B5613D;
}
html{scroll-behavior:smooth}
body{background:var(--paper);color:var(--ink);font-family:'Inter',sans-serif;font-weight:300;-webkit-font-smoothing:antialiased;overflow-x:hidden}
a{color:inherit}
img{max-width:100%;display:block}
.disp{font-family:'Schibsted Grotesk',sans-serif}
/* A scrim rather than mix-blend-mode: the trip photographs are far brighter than the
   stock shots this nav was built against, and difference blending made it illegible. */
nav{position:fixed;top:0;left:0;right:0;z-index:100;display:flex;justify-content:space-between;align-items:center;padding:26px 48px;transition:background .3s ease}
nav::before{content:'';position:absolute;inset:0;z-index:-1;pointer-events:none;transition:opacity .3s ease;background:linear-gradient(180deg,rgba(22,22,26,0.78) 0%,rgba(22,22,26,0.42) 55%,rgba(22,22,26,0) 100%)}
nav.scrolled{background:rgba(22,22,26,0.95);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px)}
nav.scrolled::before{opacity:0}
.nav-mark{font-family:'Schibsted Grotesk',sans-serif;font-weight:700;font-size:15px;letter-spacing:0.32em;text-transform:uppercase;color:#fff;text-decoration:none;text-shadow:0 1px 12px rgba(22,22,26,0.5)}
.nav-links{display:flex;gap:30px;list-style:none}
.nav-links a{font-size:11px;letter-spacing:0.24em;text-transform:uppercase;color:#fff;text-decoration:none;opacity:.9;text-shadow:0 1px 12px rgba(22,22,26,0.5)}
.nav-links a:hover{opacity:1}
.hero{position:relative;min-height:78vh;display:flex;flex-direction:column;justify-content:flex-end;overflow:hidden}
.hero-img{position:absolute;inset:0;background-size:cover;background-position:center;filter:saturate(0.88) contrast(1.05) sepia(0.09)}
.hero::after{content:'';position:absolute;inset:0;background:linear-gradient(180deg,rgba(22,22,26,0.52),rgba(22,22,26,0.30) 40%,rgba(22,22,26,0.85))}
.hero-body{position:relative;z-index:3;padding:0 48px 56px;color:var(--paper)}
/* Split hero. The IG title card is a finished design with its own typography,
   so it is shown whole at its native 4:5 rather than cropped behind text. */
.hero-split{background:var(--ink);color:var(--paper);display:grid;grid-template-columns:minmax(0,0.85fr) minmax(0,1fr);align-items:center;gap:0}
.hs-card{padding:88px 0 48px 48px}
.hs-card img{width:100%;height:auto;aspect-ratio:4/5;object-fit:contain;background:#0f0f12}
.hs-body{padding:88px 48px 48px}
.hs-eyebrow{font-size:11px;letter-spacing:0.4em;text-transform:uppercase;color:rgba(237,235,229,0.75);margin-bottom:20px;display:block}
.hs-title{font-family:'Schibsted Grotesk',sans-serif;font-weight:800;font-size:clamp(2.2rem,4.6vw,4rem);line-height:0.92;letter-spacing:-0.025em;margin-bottom:20px}
.hs-sub{font-size:15px;line-height:1.7;max-width:520px;color:rgba(237,235,229,0.85)}
.hs-where{font-size:11px;letter-spacing:0.25em;text-transform:uppercase;color:var(--clay);margin-top:26px;display:block}
.hb-eyebrow{font-size:11px;letter-spacing:0.4em;text-transform:uppercase;color:rgba(237,235,229,0.96);text-shadow:0 1px 14px rgba(22,22,26,0.75);margin-bottom:20px;display:block}
.hb-title{font-family:'Schibsted Grotesk',sans-serif;font-weight:800;font-size:clamp(2.6rem,8vw,7rem);line-height:0.9;letter-spacing:-0.025em;margin-bottom:22px}
.hb-sub{font-size:15px;line-height:1.6;max-width:620px;color:rgba(237,235,229,0.9)}
.stats{display:flex;flex-wrap:wrap;border-bottom:1px solid var(--line)}
.stat{flex:1;min-width:140px;padding:30px 36px;border-right:1px solid var(--line)}
.stat:last-child{border-right:none}
.stat-val{font-family:'Schibsted Grotesk',sans-serif;font-weight:700;font-size:2rem;line-height:1;letter-spacing:-0.01em;margin-bottom:7px;display:block}
.stat-lbl{font-size:10px;letter-spacing:0.22em;text-transform:uppercase;color:var(--stone)}
.sec{max-width:1180px;margin:0 auto;padding:80px 48px}
.sec-tag{font-family:'Schibsted Grotesk',sans-serif;font-size:11px;font-weight:500;letter-spacing:0.35em;text-transform:uppercase;color:var(--stone);margin-bottom:16px;display:block}
.sec-h{font-family:'Schibsted Grotesk',sans-serif;font-weight:700;font-size:clamp(2rem,4.5vw,3.4rem);line-height:0.98;letter-spacing:-0.015em;margin-bottom:26px}
.prose{font-size:clamp(1.02rem,1.6vw,1.3rem);font-weight:300;line-height:1.75;max-width:780px;margin-bottom:20px}
.chain{display:flex;flex-wrap:wrap;align-items:center;gap:8px;font-size:12px;color:var(--stone);line-height:1.5;margin-bottom:34px}
.chain b{font-weight:500;color:var(--ink)}
.chain-sep{color:var(--line);font-size:10px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:2px;background:var(--line-soft);border:1px solid var(--line)}
.shot{position:relative;background:var(--paper-2);border:none;padding:0;cursor:zoom-in;aspect-ratio:4/5;overflow:hidden}
.shot img{width:100%;height:100%;object-fit:cover;filter:saturate(0.9) contrast(1.04) sepia(0.07);transition:transform .6s ease}
.shot:hover img{transform:scale(1.03)}
.map-wrap{border:1px solid var(--line);margin-top:2px}
.map-wrap img{width:100%}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:1px;background:var(--line);border:1px solid var(--line)}
.card{background:var(--paper);text-decoration:none;display:flex;flex-direction:column}
.card-img{aspect-ratio:4/5;background-size:cover;background-position:center}
.card-body{padding:26px 28px 30px}
.card-tag{font-family:'Schibsted Grotesk',sans-serif;font-size:10px;font-weight:500;letter-spacing:0.3em;text-transform:uppercase;color:var(--clay);display:block;margin-bottom:10px}
.card-h{font-family:'Schibsted Grotesk',sans-serif;font-weight:700;font-size:1.35rem;line-height:1.05;letter-spacing:-0.01em;margin-bottom:10px}
.card-date{font-size:11px;letter-spacing:0.16em;text-transform:uppercase;color:var(--stone);margin-bottom:12px}
.card-blurb{font-size:13.5px;line-height:1.65;color:#46443e}
.ig-link{display:inline-flex;align-items:center;gap:10px;font-family:'Schibsted Grotesk',sans-serif;font-size:11px;font-weight:500;letter-spacing:0.2em;text-transform:uppercase;padding:14px 22px;background:var(--ink);color:var(--paper);text-decoration:none;margin-top:8px}
.ig-link:hover{background:var(--clay)}
.next{display:flex;justify-content:space-between;align-items:center;gap:30px;flex-wrap:wrap;padding:56px 48px;border-top:1px solid var(--line)}
.next-back{font-family:'Schibsted Grotesk',sans-serif;font-size:11px;font-weight:500;letter-spacing:0.25em;text-transform:uppercase;color:var(--stone);text-decoration:none}
.next-back:hover{color:var(--ink)}
.next-link{text-decoration:none;text-align:right}
.next-tag{font-family:'Schibsted Grotesk',sans-serif;font-size:10px;font-weight:500;letter-spacing:0.3em;text-transform:uppercase;color:var(--stone);display:block;margin-bottom:6px}
.next-title{font-family:'Schibsted Grotesk',sans-serif;font-weight:800;font-size:clamp(1.6rem,3.4vw,2.4rem);line-height:0.95;letter-spacing:-0.02em}
footer{padding:46px 48px;border-top:1px solid var(--line);font-size:11px;letter-spacing:0.16em;text-transform:uppercase;color:var(--stone);text-align:center}
footer a{color:var(--clay);text-decoration:none}
.lb{position:fixed;inset:0;z-index:200;background:rgba(22,22,26,0.94);display:none;align-items:center;justify-content:center;padding:24px}
.lb.on{display:flex}
.lb img{max-width:94vw;max-height:88vh;object-fit:contain;width:auto}
.lb-x{position:absolute;top:20px;right:26px;background:none;border:none;color:var(--paper);font-size:30px;cursor:pointer;line-height:1}
.lb-nav{position:absolute;top:50%;transform:translateY(-50%);background:none;border:none;color:var(--paper);font-size:38px;cursor:pointer;padding:16px;opacity:.7}
.lb-nav:hover{opacity:1}
.lb-prev{left:8px}.lb-next{right:8px}
@media(max-width:820px){
 nav{padding:16px 20px}.nav-links{gap:14px}
 .nav-links a{font-size:10px;letter-spacing:0.16em}
 .hero-body{padding:0 22px 40px}
 .stat{min-width:50%;border-bottom:1px solid var(--line)}
 .sec{padding:56px 22px}
 .next{padding:40px 22px}
 footer{padding:34px 22px}
 .hero-split{grid-template-columns:1fr}
 .hs-card{padding:76px 22px 0}
 .hs-body{padding:30px 22px 44px}
 .lb-nav{font-size:28px;padding:10px}
}
"""

LIGHTBOX = """
<div class="lb" id="lb">
 <button class="lb-x" aria-label="Close">&times;</button>
 <button class="lb-nav lb-prev" aria-label="Previous">&#8249;</button>
 <img id="lbimg" alt="">
 <button class="lb-nav lb-next" aria-label="Next">&#8250;</button>
</div>
<script>
(function(){
 var shots=[].slice.call(document.querySelectorAll('.shot')),lb=document.getElementById('lb'),
     im=document.getElementById('lbimg'),i=0;
 if(!shots.length)return;
 function show(n){i=(n+shots.length)%shots.length;im.src=shots[i].dataset.full;
   im.alt=shots[i].querySelector('img').alt;}
 function open(n){show(n);lb.classList.add('on');document.body.style.overflow='hidden';}
 function close(){lb.classList.remove('on');document.body.style.overflow='';im.src='';}
 shots.forEach(function(s,n){s.addEventListener('click',function(){open(n);});});
 lb.querySelector('.lb-x').addEventListener('click',close);
 lb.querySelector('.lb-prev').addEventListener('click',function(e){e.stopPropagation();show(i-1);});
 lb.querySelector('.lb-next').addEventListener('click',function(e){e.stopPropagation();show(i+1);});
 lb.addEventListener('click',function(e){if(e.target===lb)close();});
 document.addEventListener('keydown',function(e){
   if(!lb.classList.contains('on'))return;
   if(e.key==='Escape')close();
   if(e.key==='ArrowLeft')show(i-1);
   if(e.key==='ArrowRight')show(i+1);
 });
})();
</script>
"""


def head(title, desc, canonical, og_image, up=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="author" content="South End">
<link rel="canonical" href="{canonical}">
<meta name="theme-color" content="#16161A">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 48 48'%3E%3Crect width='48' height='48' rx='9' fill='%2316161A'/%3E%3Ctext x='24' y='33' font-family='Helvetica,Arial,sans-serif' font-size='23' font-weight='700' fill='%23EDEBE5' text-anchor='middle'%3ESE%3C/text%3E%3C/svg%3E">
<meta property="og:type" content="article">
<meta property="og:site_name" content="South End">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE}/{og_image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{SITE}/{og_image}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Schibsted+Grotesk:wght@400;500;700;800&family=Inter:wght@300;400;500&display=swap">
<style>{CSS}</style>
</head>
<body>
{nav(up)}
"""


def nav(up=""):
    return f"""<nav>
 <a href="{up}index.html" class="nav-mark">South End</a>
 <ul class="nav-links">
  <li><a href="{up}trips.html">Our Trips</a></li>
  <li><a href="{up}journal.html">Journal</a></li>
  <li><a href="{up}gallery.html">Photos</a></li>
  <li><a href="{up}alps-register.html">Register</a></li>
 </ul>
</nav>"""


NAV_JS = """<script>
(function(){var n=document.querySelector('nav');if(!n)return;
var f=function(){n.classList.toggle('scrolled',(window.scrollY||window.pageYOffset)>60)};
f();window.addEventListener('scroll',f,{passive:true});})();
</script>
"""


def foot(up=""):
    return NAV_JS + f"""<footer>
 South End · Run.Ride the Alps · 14–23 July 2026 ·
 <a href="{PROFILE}" target="_blank" rel="noopener">@thesouthend.co</a>
</footer>
</body>
</html>
"""


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def chain_html(parts):
    out = []
    for n, p in enumerate(parts):
        if n:
            out.append('<span class="chain-sep">/</span>')
        out.append(f"<b>{esc(p)}</b>" if n in (0, len(parts) - 1) else esc(p))
    return '<div class="chain">' + "\n".join(out) + "</div>"


def stats_html(stats):
    if not stats:
        return ""
    cells = "".join(
        f'<div class="stat"><span class="stat-val disp">{esc(v)}</span>'
        f'<span class="stat-lbl">{esc(l)}</span></div>' for v, l in stats)
    return f'<div class="stats">{cells}</div>'


# ------------------------------------------------------------------- photo sets

def have(f):
    return bool(f) and os.path.exists(os.path.join(ROOT, "ig", f))


def load_sets():
    """manifest.json is the base set per day. days.py may then override the title
    card or map with a newer revision, and append hand-picked frames. Newer card
    versions land in ig/ as v9_/v10_ files without the manifest being regenerated."""
    with open(os.path.join(ROOT, "ig", "manifest.json")) as fh:
        man = json.load(fh)
    by_slug = {d["slug"]: d for d in DAYS}
    extra = {"stelvio": ["v8_stelvio_hp_bend.jpg", "v8_stelvio_hp_rider.jpg"]}
    sets = {}
    for slug, files in man.items():
        files = [f for f in files if have(f)]
        title = next((f for f in files if "_title" in f), None)
        mapimg = next((f for f in files if "_map" in f), None)
        shots = [f for f in files if f not in (title, mapimg)]

        day = by_slug.get(slug, {})
        if have(day.get("title_img")):
            title = day["title_img"]
        if have(day.get("map_img")):
            mapimg = day["map_img"]
        for f in extra.get(slug, []) + list(day.get("extra_shots", [])):
            if have(f) and f not in shots:
                shots.append(f)

        sets[slug] = {"title": title, "map": mapimg, "shots": shots,
                      "all": ([title] if title else []) + shots}
    return sets


def pick_photo(sets, slug):
    """First real photograph in a set. Never a title card or a map."""
    shots = sets.get(slug, {}).get("shots") or []
    return shots[0] if shots else ""


def tiles_for(sets, slug):
    """Everything shown in a photo grid: the title card first, then the photographs.
    The 4:5 grid matches the images' native aspect, so nothing is cropped."""
    s = sets.get(slug, {})
    return ([s["title"]] if s.get("title") else []) + (s.get("shots") or [])


def alt_for(day, n):
    return f"{day['title']}. {day['where']}, {day['date']} ({n})"


def shots_html(day, files, up=""):
    if not files:
        return ""
    out = []
    for n, f in enumerate(files, 1):
        src = f"{up}ig/{f}"
        out.append(
            f'<button class="shot" data-full="{src}">'
            f'<img src="{src}" loading="lazy" decoding="async" '
            f'alt="{esc(alt_for(day, n))}"></button>')
    return '<div class="grid">' + "\n".join(out) + "</div>"


# ----------------------------------------------------------------- journal post

def build_post(day, sets, prev_day, next_day):
    s = sets.get(day["slug"], {"title": None, "map": None, "shots": [], "all": []})
    # The hero is a photograph, never the title card: the card already carries the
    # route name and the day's numbers as baked-in type, so pairing it with the HTML
    # h1 and the stats bar would state the same thing three times. The card is shown
    # whole, at its native 4:5, as the first tile of the grid below.
    hero = pick_photo(sets, day["slug"]) or s["title"] or ""
    tiles = ([s["title"]] if s["title"] else []) + s["shots"]
    url = f"{SITE}/journal/{day['slug']}.html"
    desc = day["blurb"]
    ig = day["ig_url"] or PROFILE
    ig_label = "View the carousel on Instagram" if day["ig_url"] else "Follow @thesouthend.co"

    h = [head(f"{day['title']} | {day['part']} | Run.Ride the Alps",
              esc(desc), url, f"ig/{hero}" if hero else "", up="../")]

    notes_html = "\n ".join(
        '<p class="prose">%s</p>' % esc(n) for n in day["notes"])

    h.append(f"""<article>
<header class="hero-split">
 <div class="hs-card">
  <img src="../ig/{hero}" alt="{esc(day['title'])}. {esc(day['where'])}, {esc(day['date'])}"
       width="1080" height="1350" fetchpriority="high" decoding="async">
 </div>
 <div class="hs-body">
  <span class="hs-eyebrow">{esc(day['part'])} · {esc(day['date'])}</span>
  <h1 class="hs-title">{esc(day['title'])}</h1>
  <p class="hs-sub">{esc(day['blurb'])}</p>
  <span class="hs-where">{esc(day['where'])}</span>
 </div>
</header>
{stats_html(day['stats'])}
<section class="sec">
 <span class="sec-tag">The line we took</span>
 {chain_html(day['chain'])}
 {notes_html}
</section>""")

    if tiles:
        h.append(f'<section class="sec" style="padding-top:0">'
                 f'<span class="sec-tag">The day in photographs</span>'
                 f'{shots_html(day, tiles, up="../")}</section>')

    if s["map"]:
        h.append(f'<section class="sec" style="padding-top:0">'
                 f'<span class="sec-tag">The route</span>'
                 f'<div class="map-wrap"><img src="../ig/{s["map"]}" loading="lazy" '
                 f'alt="{esc(day["title"])} route map"></div></section>')

    h.append(f'<section class="sec" style="padding-top:0">'
             f'<a class="ig-link" href="{ig}" target="_blank" rel="noopener">'
             f'{esc(ig_label)} ↗</a></section>')

    back = f'<a class="next-back" href="../journal.html">← All entries</a>'
    if next_day:
        nxt = (f'<a class="next-link" href="{next_day["slug"]}.html">'
               f'<span class="next-tag">Next · {esc(next_day["date"])}</span>'
               f'<span class="next-title disp">{esc(next_day["title"])}</span></a>')
    elif prev_day:
        nxt = (f'<a class="next-link" href="../gallery.html">'
               f'<span class="next-tag">Every photograph</span>'
               f'<span class="next-title disp">The gallery</span></a>')
    else:
        nxt = ""
    h.append(f'<div class="next">{back}{nxt}</div></article>')
    h.append(LIGHTBOX)
    h.append(foot("../"))
    return "\n".join(h)


# ---------------------------------------------------------------- journal index

def build_index(sets):
    url = f"{SITE}/journal.html"
    # A photograph, not a title card; the cards carry their own typography.
    hero = pick_photo(sets, "run2")
    h = [head("Journal | Run.Ride the Alps | South End",
              "Eleven days across the Alps, day by day: four days trail running the "
              "Dolomites' Alta Via 2, then a road traverse over the Stelvio and Gavia "
              "to Alpe d'Huez.", url, f"ig/{hero}")]
    h.append(f"""<header class="hero">
 <div class="hero-img" style="background-image:url('ig/{hero}')"></div>
 <div class="hero-body">
  <span class="hb-eyebrow">Cohort 01 · 13–23 July 2026</span>
  <h1 class="hb-title">The journal</h1>
  <p class="hb-sub">Eleven days from Bressanone to the bottom of Alpe d'Huez. Four on
  foot through the Dolomites, then the long road west. Every day, as it happened.</p>
 </div>
</header>
{stats_html([(TOTALS['distance'], 'Total distance'), (TOTALS['ascent'], 'Total ascent'),
             (TOTALS['days'], 'On the move'), (TOTALS['high'], 'High point')])}
<section class="sec">
 <span class="sec-tag">Day by day</span>
 <h2 class="sec-h">Eleven days, one line</h2>""")

    cards = []
    for d in DAYS:
        s = sets.get(d["slug"], {})
        img = s.get("title") or (s.get("shots") or [""])[0]
        cards.append(f"""<a class="card" href="journal/{d['slug']}.html">
 <div class="card-img" style="background-image:url('ig/{img}')"></div>
 <div class="card-body">
  <span class="card-tag">{esc(d['part'])}</span>
  <div class="card-date">{esc(d['date'])}</div>
  <h3 class="card-h">{esc(d['title'])}</h3>
  <p class="card-blurb">{esc(d['blurb'])}</p>
 </div>
</a>""")
    h.append('<div class="cards">' + "\n".join(cards) + "</div></section>")
    h.append(f"""<div class="next">
 <a class="next-back" href="index.html">← Home</a>
 <a class="next-link" href="gallery.html">
  <span class="next-tag">Every photograph</span>
  <span class="next-title disp">The gallery</span></a>
</div>""")
    h.append(foot())
    return "\n".join(h)


# ----------------------------------------------------------------------- gallery

def build_gallery(sets):
    url = f"{SITE}/gallery.html"
    hero = pick_photo(sets, "stelvio")
    total = sum(len(tiles_for(sets, d["slug"])) for d in DAYS)
    h = [head("Photographs | Run.Ride the Alps | South End",
              f"{total} photographs from eleven days across the Alps: the Dolomites' "
              "Alta Via 2, the Stelvio, the Gavia and the road to Alpe d'Huez.",
              url, f"ig/{hero}")]
    h.append(f"""<header class="hero">
 <div class="hero-img" style="background-image:url('ig/{hero}')"></div>
 <div class="hero-body">
  <span class="hb-eyebrow">Cohort 01 · 13–23 July 2026</span>
  <h1 class="hb-title">Photographs</h1>
  <p class="hb-sub">{total} frames from the Dolomites to Alpe d'Huez, in the order they
  happened. Click any image to open it full size.</p>
 </div>
</header>""")
    for d in DAYS:
        tiles = tiles_for(sets, d["slug"])
        if not tiles:
            continue
        h.append(f"""<section class="sec" style="padding-bottom:40px">
 <span class="sec-tag">{esc(d['part'])} · {esc(d['date'])}</span>
 <h2 class="sec-h">{esc(d['title'])}</h2>
 {shots_html(d, tiles)}
 <p style="margin-top:18px"><a class="next-back" href="journal/{d['slug']}.html">
  Read the entry →</a></p>
</section>""")
    h.append(f"""<div class="next">
 <a class="next-back" href="index.html">← Home</a>
 <a class="next-link" href="journal.html">
  <span class="next-tag">Day by day</span>
  <span class="next-title disp">The journal</span></a>
</div>""")
    h.append(LIGHTBOX)
    h.append(foot())
    return "\n".join(h)


def build_sitemap():
    urls = [("", "1.0"), ("trips.html", "0.9"), ("journal.html", "0.9"), ("gallery.html", "0.8"),
            ("alps-run.html", "0.8"), ("alps-ride.html", "0.8"),
            ("alps-calendar.html", "0.6"), ("alps-register.html", "0.9"),
            ("alps-adventure.html", "0.8"), ("brand-guide.html", "0.3")]
    urls += [(f"journal/{d['slug']}.html", "0.7") for d in DAYS]
    rows = "\n".join(
        f"  <url><loc>{SITE}/{p}</loc><priority>{pr}</priority></url>"
        for p, pr in urls)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            f"{rows}\n</urlset>\n")


def main():
    sets = load_sets()
    os.makedirs(os.path.join(ROOT, "journal"), exist_ok=True)
    for n, d in enumerate(DAYS):
        prev_d = DAYS[n - 1] if n else None
        next_d = DAYS[n + 1] if n + 1 < len(DAYS) else None
        with open(os.path.join(ROOT, "journal", d["slug"] + ".html"), "w") as fh:
            fh.write(build_post(d, sets, prev_d, next_d))
    with open(os.path.join(ROOT, "journal.html"), "w") as fh:
        fh.write(build_index(sets))
    with open(os.path.join(ROOT, "gallery.html"), "w") as fh:
        fh.write(build_gallery(sets))
    with open(os.path.join(ROOT, "sitemap.xml"), "w") as fh:
        fh.write(build_sitemap())
    with open(os.path.join(ROOT, "robots.txt"), "w") as fh:
        fh.write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    tiles = sum(len(tiles_for(sets, d["slug"])) for d in DAYS)
    print(f"built {len(DAYS)} entries + journal.html + gallery.html "
          f"+ sitemap.xml ({tiles} images)")


if __name__ == "__main__":
    main()
