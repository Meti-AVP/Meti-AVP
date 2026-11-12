"""参 THE BLADES — projects as title cards, paired into diptychs whose art runs across the hinge.

Edit PROJECTS to change what is featured; every pair shares one continuous motif.
"""
import os

import art
import scene
from svgkit import C, doc, f, fit_size, grain_defs, kanji, measure, text, wrap, write

W = 1200
CW, CH, HINGE = 596, 420, 8   # card size; two cards + hinge = 1200

# (kanji, title, category, tagline, stack, link label, url)
PROJECTS = [
    ("夢", "AHMED ZAKI", "CINEMATIC WEB · WEBGL",
     "A scroll story shot like a film, opening into three 3D worlds: Product, AI and Full Stack.",
     "React · Vite · GSAP · Lenis · WebGL", "ahmedzaki.vercel.app", "https://ahmedzaki.vercel.app"),
    ("美", "RAPHAEL STUDIOS", "AGENCY SITE · PAINTED 3D",
     "Thirteen chapters, each opening over its own painted 3D scene of marble statues.",
     "Astro · WebGL2 · GSAP · TypeScript", "raphael-studios.vercel.app", "https://raphael-studios.vercel.app"),
    ("師", "HITU AI PLATFORM", "UNIVERSITY OS · AI SCHEDULING",
     "Timetables solved by OR-Tools CP-SAT, an LMS, analytics and role-based control.",
     "FastAPI · React · Supabase · Docker · Ollama", "hitu-1.vercel.app", "https://hitu-1.vercel.app"),
    ("勝", "PROJECT ASCENT", "ZEDNY · GAMIFIED LEARNING",
     "Corporate training rebuilt as a sport: 19 game arenas, duels, tournaments, a global ranking.",
     "React 18 · Vite · TypeScript · FastAPI", "pathway-builder-kappa.vercel.app", "https://pathway-builder-kappa.vercel.app"),
    ("心", "WORKFIT HUB", "3D SYSTEM EXPLAINER",
     "A whole product lifecycle as one living tree on a 3D canvas: seven phases, every step.",
     "Three.js · GSAP · Vite", "wfhworkflow.vercel.app", "https://wfhworkflow.vercel.app"),
    ("家", "DEEB BIM", "PRODUCT SITE · EN / AR",
     "Engineering-grade Revit add-ins: bilingual RTL site, accounts, signed webhooks, licenses.",
     "TypeScript · Auth · Webhooks · RTL", "deebbim.vercel.app", "https://deebbim.vercel.app"),
    ("緑", "GREEN VISION", "AI FOR THE PLANET",
     "AI that watches the desert: NDVI, rainfall and drought forecasts, plus a UE5 game.",
     "Python · ML · Remote sensing · Unreal Engine 5", "case study", "projects/green-vision.md"),
    ("鍛", "AV SAFETY QC", "AUTONOMOUS VEHICLES",
     "The QC desk behind three AV pipelines: decision-tree classification, shifts, production tracking.",
     "LiDAR & image QC · Web app", "meti-avp.github.io", "https://meti-avp.github.io/v-classification-system/"),
]
MOTIFS = ["katana", "sun", "branch", "ridge"]


# ------------------------------------------------------------------------------ header
def header(out_dir):
    u, H = "bh", scene.HEIGHT["blades"]
    defs, body = [], []
    defs.append(f'<linearGradient id="{u}bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0D0305"/>'
                f'<stop offset="1" stop-color="{C["night"]}"/></linearGradient>')
    body.append(f'<rect width="{W}" height="{H}" fill="url(#{u}bg)"/>')
    body.append(scene.ridges("blades", u, layers=[2]))
    body.append(kanji("参", 56, 150, 92, fill=C["blood_hi"], style="brush"))
    body.append(text(172, 112, "THE BLADES", "ser7", 56, C["rosary"], tracking=8))
    body.append(kanji("名刀", 174, 148, 17, fill=C["brass"], style="mincho", gap=.1))
    body.append(text(218, 147, "EIGHT BLADES, FORGED AND SHIPPED. EACH CARD OPENS THE LIVE WORK.", "san7", 11.5, C["brass"], tracking=3))
    body.append(text(W - 46, H - 24, "04 / 08", "san8", 10, C["ash"], tracking=4, anchor="end"))
    defs.append(grain_defs(u, .08))
    body.append(f'<rect width="{W}" height="{H}" fill="url(#{u}grain)"/>')
    svg = doc(W, H, "".join(body), defs="".join(defs), title="参 The Blades: projects",
              desc="Section header for the projects: eight blades, forged and shipped.")
    return write(os.path.join(out_dir, "03-blades.svg"), svg)


# ------------------------------------------------------------------------------ continuous motif
def motif(kind, u, row):
    """Art in row coordinates (0..1200 x 0..CH) shared by the two cards of a diptych."""
    defs, g = [], []
    if kind == "katana":
        kd, k = art.katana(u + "k", 930, 62, 620, angle=180)
        defs.append(kd)
        g.append(k)
    elif kind == "sun":
        defs.append(art.sun_defs(u))
        g.append(art.sun(u, W / 2, 26, 110, glow=True))
    elif kind == "branch":
        # two boughs reaching for each other across the hinge
        defs.append(art.blossom_defs(u))
        g.append(art.sakura_branch(u, -24, 132, -7, 600, 18, seed=203, depth=2, bloom=1.0, scale=.85, color="#4A1418", up_only=True))
        g.append(art.sakura_branch(u, W + 24, 126, 187, 560, 16, seed=207, depth=2, bloom=1.0, scale=.85, color="#4A1418", up_only=True))
    else:
        # one sumi stroke dragged across both screens
        import math
        pts = [(40 + i * 11.2, 78 - 26 * math.sin(i / 100 * math.pi) + 6 * math.sin(i / 9)) for i in range(101)]
        body = art.brush_stroke(pts, 30, seed=221, tail=.3, bristles=9, w_end=.5, start_blob=1.5)
        streaks = art.brush_streaks(pts, 30, seed=221, n=12, t0=.15)
        g.append(f'<path d="{body}" fill="{C["blood"]}" fill-opacity=".92"/>'
                 f'<path d="{streaks}" fill="none" stroke="{C["night"]}" stroke-opacity=".55" stroke-width="1.4" stroke-linecap="round"/>')
    return "".join(defs), "".join(g)


def card(out_dir, idx):
    row, side = divmod(idx, 2)
    kj, title, cat, tagline, stack, link_label, _url = PROJECTS[idx]
    u = f"bc{idx}"
    ox = 0 if side == 0 else CW + HINGE  # where this card sits in the row
    defs, body, css = [], [], []
    defs.append(f'<radialGradient id="{u}bg" cx="{"30%" if side == 0 else "70%"}" cy="55%" r="85%">'
                f'<stop offset="0" stop-color="#1F060A"/><stop offset="1" stop-color="{C["night"]}"/></radialGradient>')
    body.append(f'<rect width="{CW}" height="{CH}" fill="url(#{u}bg)"/>')
    md, mg = motif(MOTIFS[row % len(MOTIFS)], f"bm{row}", row)
    defs.append(md)
    body.append(f'<g transform="translate({-ox} 0)">{mg}</g>')

    # emblem + number
    body.append(kanji(kj, 40, 300, 150, fill=C["blood_hi"], style="brush", op=.95))
    body.append(text(44, 352, f"{idx + 1:02d}", "ser7", 22, C["brass_hi"], tracking=2))
    body.append(f'<rect x="80" y="344" width="80" height="1" fill="{C["brass"]}" fill-opacity=".5"/>')

    tx, tw = 214, CW - 214 - 34
    body.append(text(tx, 178, cat, "san8", 9.8, C["brass"], tracking=2.6))
    ts = fit_size(title, "ser7", tw, 40, tracking=3)
    body.append(text(tx, 222, title, "ser7", ts, C["rosary"], tracking=3))
    for j, line in enumerate(wrap(tagline, "seri", 18.5, tw)[:3]):
        body.append(text(tx, 254 + j * 23, line, "seri", 18.5, C["blush"]))
    body.append(text(tx, 340, stack, "san7", fit_size(stack, "san7", tw, 11, 1.2), C["rosary_dim"], tracking=1.2))
    lab = "LIVE  ↗" if link_label != "case study" else "READ  ↗"
    body.append(f'<rect x="{tx}" y="358" width="{f(measure(lab, "san8", 11, 3) + 18)}" height="26" fill="{C["blood"]}"/>')
    body.append(text(tx + 9, 375, lab, "san8", 11, C["rosary"], tracking=3))
    body.append(text(tx + measure(lab, "san8", 11, 3) + 30, 376, link_label, "mono", 12, C["brass_hi"]))

    # frame: crop marks only on the outer edges, a hairline on the hinge
    m, L = 18, 14
    d = []
    for (x, y, sx, sy) in ((m, m, 1, 1), (CW - m, m, -1, 1), (m, CH - m, 1, -1), (CW - m, CH - m, -1, -1)):
        outer = (side == 0 and sx == 1) or (side == 1 and sx == -1)
        if outer:
            d.append(f"M{f(x - sx * 6)} {f(y)}h{f(sx * (L + 6))}M{f(x)} {f(y - sy * 6)}v{f(sy * (L + 6))}")
    body.append(f'<path d="{"".join(d)}" stroke="{C["brass"]}" stroke-opacity=".45" fill="none"/>')
    hx = CW - .5 if side == 0 else .5
    body.append(f'<rect x="{f(hx - .5)}" y="0" width="1" height="{CH}" fill="{C["brass"]}" fill-opacity=".25"/>')

    defs.append(art.blossom_defs(u))
    pcss, petals = art.falling_petals(u, CW, CH, 6, seed=300 + idx, size=(.55, 1.0), op=(.5, .85), dur=(10, 16), wind=1.2)
    css.append(pcss)
    body.append(petals)
    defs.append(grain_defs(u, .08))
    body.append(f'<rect width="{CW}" height="{CH}" fill="url(#{u}grain)"/>')
    svg = doc(CW, CH, "".join(body), css="".join(css), defs="".join(defs), title=f"{title}: {cat.title()}",
              desc=f"{tagline} Built with {stack}. Opens {link_label}.")
    return write(os.path.join(out_dir, "blades", f"{idx + 1:02d}-{side and 'r' or 'l'}.svg"), svg)


def build(out_dir):
    return [header(out_dir)] + [card(out_dir, i) for i in range(len(PROJECTS))]
