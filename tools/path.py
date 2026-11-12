"""弐 THE PATH — the career as a mountain trail; a ronin walks it and pauses at every gate."""
import math
import os

import art
import scene
from svgkit import C, doc, f, grain_defs, kanji, measure, text, wrap, write

W, H = 1200, scene.HEIGHT["path"]

# (x, y, year, kanji, title, detail, label side)
STATIONS = [
    (122, 500, "2022", "入門", "ENTERED THE DOJO", "B.Sc. Artificial Intelligence at MITU", "br"),
    (286, 442, "2023", "修行", "TRAINING", "Graph theory: radio k-coloring (Laxman Saha)", "al"),
    (450, 470, "2024", "初陣", "FIRST BATTLES", "QCare health app · Heal-Me hazard robot", "br"),
    (614, 382, "2024", "鍛錬", "THE FORGE", "Labeling to AV data QC, three pipelines", "al"),
    (778, 360, "2025", "緑", "GREEN VISION", "NASA Space Apps · EU · IEEE · Ministry", "br"),
    (944, 268, "2025", "将", "COMMAND", "Product Owner at Zedny for E-Learning", "al"),
    (1088, 186, "2026", "頂", "THE SUMMIT", "Graduation, and shipping at scale", "ar"),
]


def catmull(points, samples=24):
    pts = [points[0]] + points + [points[-1]]
    out = []
    for i in range(1, len(pts) - 2):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[i + 1], pts[i + 2]
        for s in range(samples):
            t = s / samples
            t2, t3 = t * t, t * t * t
            out.append(tuple(0.5 * ((2 * p1[k]) + (-p0[k] + p2[k]) * t + (2 * p0[k] - 5 * p1[k] + 4 * p2[k] - p3[k]) * t2
                                    + (-p0[k] + 3 * p1[k] - 3 * p2[k] + p3[k]) * t3) for k in (0, 1)))
    out.append(points[-1])
    return out


def build(out_dir):
    u = "pa"
    defs, body, css = [], [], []
    defs.append(f'<linearGradient id="{u}sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1A0509"/>'
                f'<stop offset="1" stop-color="{C["night"]}"/></linearGradient>'
                f'<linearGradient id="{u}mist" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{C["rosary"]}" stop-opacity="0"/>'
                f'<stop offset=".5" stop-color="{C["rosary"]}" stop-opacity=".07"/><stop offset="1" stop-color="{C["rosary"]}" stop-opacity="0"/></linearGradient>')
    body.append(f'<rect width="{W}" height="{H}" fill="url(#{u}sky)"/>')

    # sun sinking behind the middle range
    defs.append(art.sun_defs(u))
    body.append(scene.ridges("path", u, layers=[0]))
    body.append(art.sun(u, 1000, 250, 112))
    body.append(f'<rect class="{u}m1" x="-80" y="150" width="{W + 160}" height="90" fill="url(#{u}mist)"/>')
    body.append(scene.ridges("path", u, layers=[1]))
    body.append(f'<rect class="{u}m2" x="-80" y="330" width="{W + 160}" height="80" fill="url(#{u}mist)"/>')
    body.append(scene.ridges("path", u, layers=[2]))
    body.append(f'<rect class="{u}m1" x="-80" y="520" width="{W + 160}" height="90" fill="url(#{u}mist)"/>')
    css.append(f"@keyframes {u}dr{{0%{{transform:translateX(-40px)}}100%{{transform:translateX(40px)}}}}"
               f".{u}m1{{animation:{u}dr 18s ease-in-out infinite alternate}}"
               f".{u}m2{{animation:{u}dr 23s ease-in-out -7s infinite alternate-reverse}}")

    # heading
    body.append(kanji("弐", 56, 150, 92, fill=C["blood_hi"], style="brush"))
    body.append(text(172, 112, "THE PATH", "ser7", 56, C["rosary"], tracking=8))
    body.append(kanji("道", 174, 148, 17, fill=C["brass"], style="mincho"))
    body.append(text(200, 147, "FROM THE FIRST LESSON TO THE SUMMIT", "san7", 11.5, C["brass"], tracking=3.4))
    body.append(text(W - 46, H - 30, "03 / 08", "san8", 10, C["ash"], tracking=4, anchor="end"))

    # the trail
    pts = [(30, 610)] + [(s[0], s[1]) for s in STATIONS] + [(1150, 150)]
    curve = catmull(pts, 26)
    d = "M" + "L".join(f"{f(x)} {f(y)}" for x, y in curve)
    defs.append(f'<path id="{u}trail" d="{d}"/>')
    body.append(f'<path d="{d}" fill="none" stroke="{C["rosary"]}" stroke-opacity=".06" stroke-width="10" stroke-linecap="round"/>')
    body.append(f'<path d="{d}" fill="none" stroke="{C["brass"]}" stroke-opacity=".75" stroke-width="1.5" stroke-dasharray="3 7" class="{u}ants"/>')
    css.append(f"@keyframes {u}an{{to{{stroke-dashoffset:-100}}}}.{u}ants{{animation:{u}an 6s linear infinite}}")

    # cumulative length → where each gate sits along the trail
    cum = [0.0]
    for a, b in zip(curve, curve[1:]):
        cum.append(cum[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
    total = cum[-1]

    def frac(pt):
        i = min(range(len(curve)), key=lambda k: (curve[k][0] - pt[0]) ** 2 + (curve[k][1] - pt[1]) ** 2)
        return cum[i] / total

    # gates + labels
    for i, (x, y, year, kj, title, detail, side) in enumerate(STATIONS):
        body.append(f'<ellipse cx="{x}" cy="{y + 1}" rx="16" ry="4" fill="#000" fill-opacity=".5"/>')
        body.append(art.torii(x, y, 30, 34, color=C["blood_hi"] if i != len(STATIONS) - 1 else C["brass"]))
        yw = measure(year, "ser7", 26)
        lines = wrap(detail, "san5", 12.5, 158)
        bw = max(yw + 12 + 30 * len(kj), measure(title, "san8", 11, 2.2), max(measure(l, "san5", 12.5) for l in lines))
        bh = 40 + 17 * len(lines)
        if side == "br":
            lx, ly = x + 18, y + 40
        elif side == "al":
            lx, ly = x - 18 - bw, y - 30 - bh
        else:  # above-right, right-aligned to the panel margin
            lx, ly = min(x + 18, W - 50 - bw), y - 40 - bh
        ax, ay = (lx, ly - 4) if side == "br" else (lx + bw, ly + bh - 6)
        body.append(f'<path d="M{x} {y - (6 if side == "br" else 30)}L{f(ax)} {f(ay)}" stroke="{C["brass"]}" stroke-opacity=".35"/>')
        body.append(text(lx, ly + 20, year, "ser7", 26, C["brass_hi"]))
        body.append(kanji(kj, lx + yw + 10, ly + 20, 26, fill=C["blood_hi"], style="brush", gap=.05))
        body.append(text(lx, ly + 38, title, "san8", 11, C["rosary"], tracking=2.2))
        for j, line in enumerate(lines):
            body.append(text(lx, ly + 56 + j * 17, line, "san5", 12.5, C["rosary_dim"]))

    # the ronin walks the path, pausing at each gate
    stops = [frac((s[0], s[1])) for s in STATIONS]
    kp, kt = [0.0], [0.0]
    dur = 34.0
    move_share = 0.72
    seg_total = 1.0
    t = 0.0
    prev = 0.0
    pause = (1 - move_share) / len(stops)
    for s in stops:
        t += move_share * (s - prev) / seg_total
        kp.append(s)
        kt.append(t)
        t += pause
        kp.append(s)
        kt.append(t)
        prev = s
    kp.append(1.0)
    kt.append(1.0)
    kt = [min(1.0, v) for v in kt]
    for i in range(1, len(kt)):  # keep keyTimes strictly increasing
        if kt[i] <= kt[i - 1]:
            kt[i] = kt[i - 1] + 1e-4
    kt[-1] = 1.0
    walker = (f'<g><animateMotion dur="{dur}s" repeatCount="indefinite" calcMode="linear" '
              f'keyPoints="{";".join(f(v, 4) for v in kp)}" keyTimes="{";".join(f(v, 4) for v in kt)}">'
              f'<mpath href="#{u}trail"/></animateMotion>'
              f'<circle r="26" fill="url(#{u}lamp)"/>'
              f'<g class="{u}bob">' + art.samurai(0, 2, 38, fill=C["rosary"], sword=C["blood_hi"]) + "</g></g>")
    defs.append(f'<radialGradient id="{u}lamp"><stop offset="0" stop-color="{C["blood_hi"]}" stop-opacity=".55"/>'
                f'<stop offset="1" stop-color="{C["blood_hi"]}" stop-opacity="0"/></radialGradient>')
    css.append(f"@keyframes {u}bb{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-1.6px)}}}}"
               f".{u}bob{{animation:{u}bb .55s ease-in-out infinite}}")
    body.append(walker)

    defs.append(art.blossom_defs(u))
    pcss, petals = art.falling_petals(u, W, H, 12, seed=51, size=(.55, 1.0), op=(.5, .85), dur=(12, 19), wind=1.4)
    css.append(pcss)
    body.append(petals)
    body.append(art.crop_marks(W, H, m=20, L=16, op=.45))
    defs.append(grain_defs(u, .08))
    body.append(f'<rect width="{W}" height="{H}" fill="url(#{u}grain)"/>')
    svg = doc(W, H, "".join(body), css="".join(css), defs="".join(defs),
              title="弐 The Path: from 2022 to 2026",
              desc="A mountain trail with seven torii gates, from entering the AI program in 2022 to the summit in 2026; "
                   "a small ronin walks it and pauses at each gate.")
    return write(os.path.join(out_dir, "02-path.svg"), svg)
