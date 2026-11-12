"""肆 HONORS — five honors as kakejiku hanging scrolls."""
import os

import art
from svgkit import C, doc, f, fit_size, grain_defs, kanji, text, wrap, write

W, H = 1200, 690

HONORS = [
    ("星", "GALACTIC", "PROBLEM SOLVER", "NASA SPACE APPS · 2025",
     "Green Vision built on NASA data, with an interactive game made around it."),
    ("水", "WORLD", "WATER WEEK", "EUROPEAN UNION · 2025",
     "Presented Green Vision to investors, the Minister of Water Resources and the EU Ambassador."),
    ("優", "GRADUATION,", "DISTINCTION", "MINISTRY OF YOUTH & SPORTS",
     "AI, ML & Quantum ML project, praised by Minister Prof. Dr. Ashraf Sobhy."),
    ("創", "APPX’25", "APPRECIATION", "IEEE ZEWAIL CITY · 2025",
     "McCarthies Team: innovation, teamwork and problem-solving on Green Vision."),
    ("数", "PYTHON FOR", "DATA ANALYSIS", "MCIT × NTI · DIGITAL EGYPT",
     "A 72-hour professional track, finished with a 94% score."),
]


def scroll(u, i, x, y, w, h):
    """One kakejiku; (x, y) = top-left of the top rod."""
    kj, t1, t2, issuer, detail = HONORS[i]
    cx = x + w / 2
    g = []
    nail_y = y - 46
    g.append(f'<path d="M{f(cx)} {f(nail_y)}L{f(x + 26)} {f(y + 2)}M{f(cx)} {f(nail_y)}L{f(x + w - 26)} {f(y + 2)}" '
             f'stroke="{C["brass"]}" stroke-opacity=".7" stroke-width="1.2"/>')
    g.append(f'<circle cx="{f(cx)}" cy="{f(nail_y)}" r="3.4" fill="{C["brass_hi"]}"/>')
    # top rod
    g.append(f'<rect x="{f(x - 4)}" y="{f(y)}" width="{f(w + 8)}" height="9" rx="4.5" fill="#160708"/>')
    # brocade mount
    g.append(f'<rect x="{f(x)}" y="{f(y + 8)}" width="{f(w)}" height="{f(h - 16)}" fill="{C["blood"]}"/>')
    g.append(f'<rect x="{f(x)}" y="{f(y + 8)}" width="{f(w)}" height="{f(h - 16)}" fill="url(#{u}brc)"/>')
    g.append(f'<rect x="{f(x)}" y="{f(y + 40)}" width="{f(w)}" height="4" fill="{C["brass"]}" fill-opacity=".8"/>')
    g.append(f'<rect x="{f(x)}" y="{f(y + h - 58)}" width="{f(w)}" height="4" fill="{C["brass"]}" fill-opacity=".8"/>')
    # paper
    px, py, pw, ph = x + 12, y + 50, w - 24, h - 116
    g.append(f'<rect x="{f(px)}" y="{f(py)}" width="{f(pw)}" height="{f(ph)}" fill="url(#{u}paper)"/>')
    g.append(kanji(kj, cx, py + 108, 88, fill="#140708", style="brush", anchor="middle"))
    ts = min(fit_size(t1, "ser7", pw - 16, 17, 1.6), fit_size(t2, "ser7", pw - 16, 17, 1.6))
    g.append(text(cx, py + 152, t1, "ser7", ts, "#1B0A0B", tracking=1.6, anchor="middle"))
    g.append(text(cx, py + 172, t2, "ser7", ts, "#1B0A0B", tracking=1.6, anchor="middle"))
    g.append(f'<rect x="{f(cx - 16)}" y="{f(py + 184)}" width="32" height="1.2" fill="{C["blood"]}"/>')
    g.append(text(cx, py + 202, issuer, "san8", fit_size(issuer, "san8", pw - 14, 8.6, 1.4), C["blood"], tracking=1.4, anchor="middle"))
    for j, line in enumerate(wrap(detail, "san5", 11.4, pw - 22)):
        g.append(text(cx, py + 222 + j * 15.5, line, "san5", 11.4, "#2A1A18", anchor="middle", op=.86))
    m, seal = art.hanko(f"{u}{i}", px + pw - 18, py + ph - 17, 21, rot=-5, seed=40 + i)
    # bottom rod with brass caps
    by = y + h - 10
    g.append(f'<rect x="{f(x - 2)}" y="{f(by)}" width="{f(w + 4)}" height="12" rx="6" fill="#160708"/>')
    g.append(f'<rect x="{f(x - 12)}" y="{f(by + 1)}" width="12" height="10" rx="3" fill="url(#{u}cap)"/>')
    g.append(f'<rect x="{f(x + w)}" y="{f(by + 1)}" width="12" height="10" rx="3" fill="url(#{u}cap)"/>')
    return m, "".join(g) + seal, nail_y


def build(out_dir):
    u = "ho"
    defs, body, css = [], [], []
    defs.append(f'<radialGradient id="{u}bg" cx="50%" cy="10%" r="95%"><stop offset="0" stop-color="#26080C"/>'
                f'<stop offset=".55" stop-color="#0E0406"/><stop offset="1" stop-color="{C["night"]}"/></radialGradient>'
                f'<linearGradient id="{u}paper" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F3EAD2"/>'
                f'<stop offset=".6" stop-color="{C["rosary"]}"/><stop offset="1" stop-color="#D9CBA8"/></linearGradient>'
                f'<linearGradient id="{u}brc" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#000" stop-opacity=".35"/>'
                f'<stop offset=".5" stop-color="#fff" stop-opacity=".05"/><stop offset="1" stop-color="#000" stop-opacity=".4"/></linearGradient>'
                f'<linearGradient id="{u}cap" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{C["brass_hi"]}"/>'
                f'<stop offset="1" stop-color="{C["brass_lo"]}"/></linearGradient>'
                f'<radialGradient id="{u}spot" cx="50%" cy="0%" r="70%"><stop offset="0" stop-color="{C["rosary"]}" stop-opacity=".09"/>'
                f'<stop offset="1" stop-color="{C["rosary"]}" stop-opacity="0"/></radialGradient>')
    body.append(f'<rect width="{W}" height="{H}" fill="url(#{u}bg)"/>')
    body.append(f'<ellipse cx="{W/2}" cy="120" rx="{W*.62}" ry="420" fill="url(#{u}spot)"/>')

    body.append(kanji("肆", 56, 150, 92, fill=C["blood_hi"], style="brush"))
    body.append(text(172, 112, "HONORS", "ser7", 56, C["rosary"], tracking=8))
    body.append(kanji("誉", 174, 148, 17, fill=C["brass"], style="mincho"))
    body.append(text(200, 147, "RECOGNITION EARNED ON REAL STAGES", "san7", 11.5, C["brass"], tracking=3.4))

    defs.append(art.blossom_defs(u))
    body.append(art.sakura_branch(u, 1236, -8, 150, 300, 16, seed=61, depth=2, bloom=.75, scale=.82, color="#3A1015"))

    sw, gap = 188, 30
    x0 = (W - (5 * sw + 4 * gap)) / 2
    top, sh = 222, 420
    css.append(f"@keyframes {u}sw{{0%{{transform:rotate(-.7deg)}}100%{{transform:rotate(.7deg)}}}}")
    for i in range(5):
        x = x0 + i * (sw + gap)
        m, g, nail_y = scroll(u, i, x, top, sw, sh)
        defs.append(m)
        body.append(f'<g style="transform-origin:{f(x + sw / 2)}px {f(nail_y)}px;'
                    f'animation:{u}sw {f(5.5 + i * .6)}s ease-in-out {f(-i * 1.3)}s infinite alternate">{g}</g>')

    pcss, petals = art.falling_petals(u, W, H, 14, seed=71, size=(.6, 1.05), op=(.55, .9), dur=(11, 18), wind=1.2)
    css.append(pcss)
    body.append(petals)
    body.append(text(W - 46, H - 30, "05 / 08", "san8", 10, C["ash"], tracking=4, anchor="end"))
    body.append(art.crop_marks(W, H, m=20, L=16, op=.45))
    defs.append(grain_defs(u, .08))
    body.append(f'<rect width="{W}" height="{H}" fill="url(#{u}grain)"/>')
    svg = doc(W, H, "".join(body), css="".join(css), defs="".join(defs),
              title="肆 Honors",
              desc="Five hanging scrolls: NASA Space Apps 2025 Galactic Problem Solver, EU World Water Week 2025, "
                   "Ministry of Youth & Sports graduation distinction, IEEE Zewail City AppX'25, and MCIT × NTI Python for Data Analysis (94%).")
    return write(os.path.join(out_dir, "04-honors.svg"), svg)
