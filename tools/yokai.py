"""The five yokai of THE DUEL, drawn in vector. Each is a challenge from the CV.

    誤札鬼 MISLABEL ONI     — the demon of wrong annotations (autonomous-vehicle data QC)
    旱魃竜 DROUGHT DRAGON   — drinks the Nile, breathes sand (Green Vision)
    仕様鬼 SCOPE-CREEP ONI  — one more feature every sprint (product ownership)
    虫     THE BUG SWARM    — ten thousand bugs, one release night
    疑念将軍 SHOGUN OF DOUBT — the last boss lives in your head (graduation)
"""
import math

from svgkit import C, f, seeded

BOSSES = [
    dict(id="mislabel", kanji="誤札鬼", name="MISLABEL ONI", hp=80, atk=(8, 16),
         lore="Feeds on every mislabeled LiDAR frame.",
         defeat="Three AV pipelines purified. Promoted to QC Specialist in two months."),
    dict(id="drought", kanji="旱魃竜", name="DROUGHT DRAGON", hp=100, atk=(9, 18),
         lore="Drinks the Nile and breathes sand.",
         defeat="Green Vision forecasts NDVI and drought. The desert blooms."),
    dict(id="scope", kanji="仕様鬼", name="SCOPE-CREEP ONI", hp=120, atk=(10, 20),
         lore="Every sprint, one more feature.",
         defeat="A PRD so clear the scope cannot creep. Shipped on time."),
    dict(id="bugs", kanji="虫", name="THE BUG SWARM", hp=140, atk=(11, 22),
         lore="Ten thousand bugs, one release night.",
         defeat="Tests green. Production quiet. Users happy."),
    dict(id="doubt", kanji="疑念将軍", name="SHOGUN OF DOUBT", hp=180, atk=(12, 25),
         lore="The last boss lives in your head.",
         defeat="Graduated. The way continues: 二周目."),
]


def _smooth(points, closed=True):
    """Catmull-Rom through points -> cubic Bezier path."""
    n = len(points)
    d = f"M{f(points[0][0])} {f(points[0][1])}"
    rng = range(n) if closed else range(n - 1)
    for i in rng:
        p0 = points[(i - 1) % n] if closed or i > 0 else points[0]
        p1 = points[i]
        p2 = points[(i + 1) % n]
        p3 = points[(i + 2) % n] if closed or i + 2 < n else points[-1]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f"C{f(c1[0])} {f(c1[1])} {f(c2[0])} {f(c2[1])} {f(p2[0])} {f(p2[1])}"
    return d + ("Z" if closed else "")


def _mirror(half):
    """half: right-side points from top-centre clockwise to bottom-centre."""
    left = [(-x, y) for x, y in reversed(half[1:-1])]
    return half + left


FACE = _mirror([(0, -150), (62, -146), (108, -126), (132, -88), (142, -38), (138, 12), (124, 62), (100, 106),
                (68, 140), (34, 160), (0, 166)])


def _defs(u, skin_hi, skin, skin_lo):
    return (f'<radialGradient id="{u}skin" cx="40%" cy="30%" r="80%"><stop offset="0" stop-color="{skin_hi}"/>'
            f'<stop offset=".55" stop-color="{skin}"/><stop offset="1" stop-color="{skin_lo}"/></radialGradient>'
            f'<radialGradient id="{u}eye" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#FFF6DA"/>'
            f'<stop offset=".45" stop-color="{C["brass_hi"]}"/><stop offset="1" stop-color="{C["brass_lo"]}"/></radialGradient>'
            f'<linearGradient id="{u}horn" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#7A6A55"/>'
            f'<stop offset=".6" stop-color="{C["rosary"]}"/><stop offset="1" stop-color="#FFF8EA"/></linearGradient>'
            f'<radialGradient id="{u}glow" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="{C["ember"]}" stop-opacity=".9"/>'
            f'<stop offset="1" stop-color="{C["ember"]}" stop-opacity="0"/></radialGradient>')


def _horns(u, kind="oni"):
    if kind == "antler":
        out = []
        for sx in (-1, 1):
            main = [(sx * 70, -128), (sx * 100, -190), (sx * 92, -250), (sx * 120, -300)]
            d = "M" + "L".join(f"{f(x)} {f(y)}" for x, y in main)
            br = (f"M{f(sx*100)} -190L{f(sx*150)} -222M{f(sx*95)} -232L{f(sx*60)} -270M{f(sx*108)} -270L{f(sx*150)} -292")
            out.append(f'<path d="{d}{br}" fill="none" stroke="url(#{u}horn)" stroke-width="13" stroke-linecap="round" stroke-linejoin="round"/>')
        return "".join(out)
    out = []
    for sx in (-1, 1):
        d = (f"M{f(sx*92)} -126C{f(sx*104)} -170 {f(sx*112)} -214 {f(sx*136)} -262"
             f"C{f(sx*114)} -232 {f(sx*82)} -196 {f(sx*52)} -146Z")
        rings = "".join(f'<path d="M{f(sx*(88 + k*7))} {f(-142 - k*22)}l{f(sx*-30)} 8" stroke="#3A2A1C" stroke-opacity=".5" stroke-width="2.4"/>'
                        for k in range(4))
        out.append(f'<path d="{d}" fill="url(#{u}horn)"/>{rings}')
    return "".join(out)


def _mane(u, color, seed=3, r0=180, r1=236, spikes=21):
    r = seeded(seed)
    pts = []
    for i in range(spikes * 2 + 1):
        a = math.radians(175 + 190 * i / (spikes * 2))
        rr = (r1 + r() * 30) if i % 2 == 0 else (r0 - r() * 14)
        pts.append((rr * math.cos(a), -30 + rr * math.sin(a) * 1.05))
    pts += [(150, 140), (-150, 140)]
    return f'<path d="M{"L".join(f"{f(x)} {f(y)}" for x, y in pts)}Z" fill="{color}"/>'


def _features(u, eye_cls, mouth=True, brows="#0B0304", eyes=2, extra_eyes=0):
    g = []
    # brows (angry, inner ends low)
    for sx in (-1, 1):
        pts = [(sx * 124, -98), (sx * 74, -112), (sx * 16, -74), (sx * 22, -60), (sx * 74, -86), (sx * 120, -78)]
        g.append(f'<path d="{_smooth(pts)}" fill="{brows}"/>')
    # forehead wrinkles
    g.append('<path d="M-46 -124Q0 -136 46 -124M-36 -108Q0 -118 36 -108" fill="none" stroke="#000" stroke-opacity=".35" stroke-width="3.2" stroke-linecap="round"/>')
    # eyes
    for sx in (-1, 1):
        eye = [(sx * 104, -54), (sx * 72, -72), (sx * 34, -56), (sx * 64, -36)]
        g.append(f'<path d="{_smooth(eye)}" fill="url(#{u}eye)" stroke="#0B0304" stroke-width="3"/>')
        g.append(f'<circle cx="{sx * 66}" cy="-54" r="22" fill="url(#{u}glow)" class="{eye_cls}"/>')
        g.append(f'<circle cx="{sx * 66}" cy="-54" r="7.5" fill="#120203"/><circle cx="{sx * 63}" cy="-57" r="2.4" fill="#FFF6DA"/>')
    for k in range(extra_eyes):
        ex = (k - (extra_eyes - 1) / 2) * 34
        ey = -118 - (12 if k % 2 else 0)
        g.append(f'<path d="M{ex - 14} {ey}Q{ex} {ey - 12} {ex + 14} {ey}Q{ex} {ey + 9} {ex - 14} {ey}Z" fill="url(#{u}eye)" stroke="#0B0304" stroke-width="2.2"/>')
        g.append(f'<circle cx="{ex}" cy="{ey}" r="12" fill="url(#{u}glow)" class="{eye_cls}" style="animation-delay:-{k * .4}s"/>')
        g.append(f'<circle cx="{ex}" cy="{ey}" r="4" fill="#120203"/>')
    # nose
    g.append('<path d="M-14 -30Q-18 6 -34 16Q-22 30 -6 22Q0 28 6 22Q22 30 34 16Q18 6 14 -30" fill="#000" fill-opacity=".22"/>')
    g.append('<ellipse cx="-17" cy="18" rx="8" ry="5" fill="#120203"/><ellipse cx="17" cy="18" rx="8" ry="5" fill="#120203"/>')
    # cheek wrinkles
    g.append('<path d="M-104 6Q-90 40 -96 70M104 6Q90 40 96 70M-74 34Q-70 52 -78 66M74 34Q70 52 78 66" fill="none" stroke="#000" stroke-opacity=".3" stroke-width="3" stroke-linecap="round"/>')
    if mouth:
        g.append('<path d="M-92 52Q-46 34 0 44Q46 34 92 52Q72 112 0 126Q-72 112 -92 52Z" fill="#120203"/>')
        g.append('<path d="M-70 92Q0 104 70 92Q50 118 0 122Q-50 118 -70 92Z" fill="#6E0A10"/>')
        teeth = "".join(f'<path d="M{x - 8} {48 + abs(x) * .06}L{x + 8} {48 + abs(x) * .06}L{x} {66 + abs(x) * .02}Z" fill="{C["rosary"]}"/>'
                        for x in (-54, -34, -14, 6, 26, 46))
        g.append(teeth)
        for sx in (-1, 1):
            g.append(f'<path d="M{sx * 44} 116L{sx * 62} 116L{sx * 60} 46Q{sx * 52} 64 {sx * 44} 116Z" fill="{C["rosary"]}" stroke="#2A1A10" stroke-width="1.5"/>')
        g.append('<path d="M-92 52Q-46 34 0 44Q46 34 92 52" fill="none" stroke="#0B0304" stroke-width="5" stroke-linecap="round"/>')
    return "".join(g)


def oni(u, kind, cx, cy, scale=1.0):
    """Returns (defs, svg, css) for boss `kind`, centred at (cx, cy)."""
    eye_cls = f"{u}ey"
    css = (f"@keyframes {u}ek{{0%,100%{{opacity:.55}}50%{{opacity:1}}}}.{eye_cls}{{animation:{u}ek 1.8s ease-in-out infinite}}")
    g = []
    if kind == "mislabel":
        defs = _defs(u, C["ember"], C["blood_hi"], C["rose"])
        g.append(_mane(u, "#0B0304", seed=5))
        g.append(_horns(u))
        g.append(f'<path d="{_smooth(FACE)}" fill="url(#{u}skin)" stroke="#0B0304" stroke-width="4"/>')
        g.append(_features(u, eye_cls))
        # misaligned bounding boxes and wrong labels
        g.append(f'<g fill="none" stroke="{C["rosary"]}" stroke-width="2" stroke-dasharray="7 5" class="{u}bb">'
                 f'<rect x="-168" y="-196" width="300" height="352"/><rect x="-120" y="-150" width="296" height="330" stroke="{C["brass_hi"]}"/></g>')
        g.append(f'<g class="{u}bb"><rect x="-168" y="-222" width="92" height="22" fill="{C["rosary"]}"/>'
                 f'<text x="-160" y="-206" class="mono7" font-size="13" fill="#120203">CAR 0.31</text>'
                 f'<rect x="96" y="-176" width="80" height="22" fill="{C["brass_hi"]}"/>'
                 f'<text x="104" y="-160" class="mono7" font-size="13" fill="#120203">PED ??</text></g>')
        css += (f"@keyframes {u}bk{{0%,100%{{transform:translate(0,0)}}25%{{transform:translate(6px,-4px)}}50%{{transform:translate(-5px,3px)}}75%{{transform:translate(3px,5px)}}}}"
                f".{u}bb{{animation:{u}bk 3.2s steps(4) infinite}}")
        g.append(f'<rect x="-190" y="-210" width="380" height="3" fill="{C["rosary"]}" fill-opacity=".55" class="{u}scan"/>')
        css += (f"@keyframes {u}sc{{0%{{transform:translateY(0);opacity:0}}10%{{opacity:.9}}90%{{opacity:.9}}100%{{transform:translateY(380px);opacity:0}}}}"
                f".{u}scan{{animation:{u}sc 3.6s linear infinite}}")
    elif kind == "drought":
        defs = _defs(u, "#E2B26E", "#A8743A", "#4E2C14")
        g.append(_mane(u, "#2A1508", seed=9, r0=176, r1=214, spikes=26))
        g.append(_horns(u, "antler"))
        g.append(f'<path d="{_smooth(FACE)}" fill="url(#{u}skin)" stroke="#1A0C05" stroke-width="4"/>')
        # cracked earth
        r = seeded(14)
        cracks = []
        for _ in range(16):
            x, y = (r() - .5) * 220, (r() - .5) * 230 - 10
            seg = [(x, y)]
            for _ in range(4):
                x += (r() - .5) * 30
                y += (r() - .5) * 30
                seg.append((x, y))
            cracks.append("M" + "L".join(f"{f(a)} {f(b)}" for a, b in seg))
        g.append(f'<path d="{"".join(cracks)}" fill="none" stroke="#2A1508" stroke-width="1.8" stroke-opacity=".7"/>')
        g.append(_features(u, eye_cls, brows="#1A0C05"))
        # whiskers
        for sx in (-1, 1):
            g.append(f'<path class="{u}wk" d="M{sx * 30} 22C{sx * 120} 10 {sx * 170} 60 {sx * 210} 20C{sx * 240} -10 {sx * 262} 20 {sx * 250} 50" '
                     f'fill="none" stroke="{C["brass_hi"]}" stroke-width="4" stroke-linecap="round" style="transform-origin:{sx * 30}px 22px"/>')
        css += (f"@keyframes {u}wkk{{0%,100%{{transform:rotate(-3deg)}}50%{{transform:rotate(4deg)}}}}"
                f".{u}wk{{animation:{u}wkk 4s ease-in-out infinite}}")
        # sand breath
        sand = "".join(f'<circle cx="{f((r() - .5) * 90)}" cy="{f(130 + r() * 40)}" r="{f(1 + r() * 2.4)}" fill="{C["brass_hi"]}" '
                       f'class="{u}sd" style="animation-delay:-{f(r() * 3)}s"/>' for _ in range(26))
        g.append(sand)
        css += (f"@keyframes {u}sdk{{0%{{transform:translate(0,0);opacity:0}}20%{{opacity:.9}}100%{{transform:translate(-160px,90px);opacity:0}}}}"
                f".{u}sd{{animation:{u}sdk 3s linear infinite}}")
    elif kind == "scope":
        defs = _defs(u, "#3A2224", "#1A0B0D", "#050102")
        g.append(_mane(u, C["blood"], seed=11, r0=178, r1=226, spikes=18))
        g.append(_horns(u))
        g.append(f'<path d="{_smooth(FACE)}" fill="url(#{u}skin)" stroke="{C["blood"]}" stroke-width="3"/>')
        g.append('<path d="M-118 -10L-60 20L-120 30ZM118 -10L60 20L120 30ZM-12 -150L0 -96L12 -150Z" fill="#9F0A10" fill-opacity=".9"/>')
        g.append(_features(u, eye_cls, brows=C["blood"], extra_eyes=3))
        # scrolls of extra features hanging from the mouth
        for k, (x, txt) in enumerate(((-48, "+1"), (-6, "+1"), (36, "+1"))):
            g.append(f'<g class="{u}sl" style="transform-origin:{x + 14}px 110px;animation-delay:-{k * .7}s">'
                     f'<rect x="{x}" y="110" width="28" height="{70 + k * 18}" fill="{C["rosary"]}"/>'
                     f'<text x="{x + 14}" y="{140 + k * 9}" text-anchor="middle" class="mono7" font-size="13" fill="#120203">{txt}</text></g>')
        css += (f"@keyframes {u}slk{{0%,100%{{transform:rotate(-4deg)}}50%{{transform:rotate(4deg)}}}}"
                f".{u}sl{{animation:{u}slk 2.6s ease-in-out infinite}}")
    elif kind == "bugs":
        defs = _defs(u, "#3A2224", "#1A0B0D", "#050102")
        r = seeded(21)
        bugs = []
        face_pts = FACE

        def inside(x, y):
            j = len(face_pts) - 1
            hit = False
            for i in range(len(face_pts)):
                xi, yi = face_pts[i]
                xj, yj = face_pts[j]
                if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi + 1e-9) + xi:
                    hit = not hit
                j = i
            return hit
        tries = 0
        while len(bugs) < 150 and tries < 4000:
            tries += 1
            x, y = (r() - .5) * 330, (r() - .5) * 360 - 10
            if not inside(x * .95, y * .95) and not (abs(x) < 170 and -260 < y < -120 and r() < .5):
                continue
            a = r() * 360
            s = 0.7 + r() * .6
            col = ["#1C0A0C", "#2E0F12", C["wine"], "#120607"][int(r() * 4)]
            jit = f' class="{u}jt" style="animation-delay:-{f(r() * 2, 2)}s"' if r() < .3 else ""
            bugs.append(f'<g transform="translate({f(x)} {f(y)}) rotate({int(a)}) scale({f(s, 2)})"{jit}>'
                        f'<path d="M-9 -5L-14 -9M-9 0L-15 0M-9 5L-14 9M9 -5L14 -9M9 0L15 0M9 5L14 9" stroke="#050102" stroke-width="1.6"/>'
                        f'<ellipse rx="9" ry="12" fill="{col}" stroke="#050102" stroke-width="1.2"/>'
                        f'<path d="M0 -12V12" stroke="#000" stroke-opacity=".55" stroke-width="1.2"/>'
                        f'<circle cy="-13" r="5" fill="#050102"/><ellipse cx="-3" cy="-4" rx="2.5" ry="5" fill="#fff" fill-opacity=".14"/></g>')
        g.append("".join(bugs))
        for sx in (-1, 1):
            g.append(f'<circle cx="{sx * 62}" cy="-50" r="34" fill="url(#{u}glow)" class="{eye_cls}"/>'
                     f'<circle cx="{sx * 62}" cy="-50" r="13" fill="#FFE9B0"/><circle cx="{sx * 62}" cy="-50" r="6" fill="#120203"/>')
        g.append('<path d="M-70 70Q0 100 70 70Q40 120 0 124Q-40 120 -70 70Z" fill="#050102"/>')
        css += (f"@keyframes {u}jk{{0%,100%{{transform:translate(0,0)}}50%{{transform:translate(1.5px,-1.5px)}}}}"
                f".{u}jt{{animation:{u}jk .35s steps(2) infinite}}")
    else:  # doubt — shogun: kabuto + menpō
        defs = _defs(u, "#4A3A3A", "#1F1414", "#060303")
        # shikoro (neck guard) lames
        for k in range(5):
            y = -36 + k * 30
            w = 190 + k * 18
            g.append(f'<path d="M{-w} {y}Q0 {y - 40} {w} {y}L{w - 14} {y + 30}Q0 {y - 8} {-w + 14} {y + 30}Z" fill="{C["blood"] if k % 2 == 0 else C["wine"]}" '
                     f'stroke="#0B0304" stroke-width="3"/>')
            g.append(f'<path d="M{-w + 20} {y + 8}Q0 {y - 30} {w - 20} {y + 8}" fill="none" stroke="{C["brass"]}" stroke-width="2" stroke-dasharray="4 8"/>')
        # fukigaeshi
        for sx in (-1, 1):
            g.append(f'<path d="M{sx * 120} -90L{sx * 196} -112L{sx * 186} -40L{sx * 128} -30Z" fill="{C["blood"]}" stroke="#0B0304" stroke-width="3"/>'
                     f'<circle cx="{sx * 160}" cy="-74" r="10" fill="none" stroke="{C["brass_hi"]}" stroke-width="3"/>')
        # bowl
        g.append('<path d="M-140 -70Q-140 -230 0 -236Q140 -230 140 -70Z" fill="#0E0607" stroke="#2A1012" stroke-width="3"/>')
        g.append("".join(f'<path d="M{x} -232Q{x * 1.25} -150 {x * 1.4} -72" fill="none" stroke="#2C1416" stroke-width="3"/>'
                         for x in (-60, -30, 0, 30, 60)))
        # crescent maedate
        g.append(f'<path d="M-150 -330Q0 -170 150 -330Q0 -200 -150 -330Z" fill="url(#{u}horn)" stroke="{C["brass_lo"]}" stroke-width="2"/>')
        g.append(f'<path d="M-150 -330Q0 -170 150 -330" fill="none" stroke="{C["brass_hi"]}" stroke-width="5"/>')
        g.append(f'<rect x="-12" y="-232" width="24" height="44" fill="{C["brass"]}"/>')
        # brim
        g.append(f'<path d="M-160 -76Q0 -110 160 -76L150 -58Q0 -88 -150 -58Z" fill="{C["blood"]}" stroke="#0B0304" stroke-width="3"/>')
        # menpō face
        mp = _mirror([(0, -56), (70, -50), (112, -20), (118, 30), (96, 92), (56, 140), (0, 158)])
        g.append(f'<path d="{_smooth(mp)}" fill="url(#{u}skin)" stroke="#0B0304" stroke-width="4"/>')
        for sx in (-1, 1):
            g.append(f'<path d="M{sx * 92} -40L{sx * 30} -30L{sx * 42} -16L{sx * 90} -22Z" fill="#050102"/>')
            g.append(f'<ellipse cx="{sx * 62}" cy="-28" rx="22" ry="9" fill="url(#{u}glow)" class="{eye_cls}"/>')
        g.append('<path d="M0 -20Q-10 20 -22 32Q0 40 22 32Q10 20 0 -20Z" fill="#2C1C1C" stroke="#0B0304" stroke-width="2"/>')
        g.append(f'<path d="M-80 54Q-40 40 0 52Q40 40 80 54Q60 60 46 74Q20 62 0 70Q-20 62 -46 74Q-60 60 -80 54Z" fill="{C["rosary_dim"]}"/>')
        g.append('<path d="M-46 92H46M-36 110H36" stroke="#000" stroke-opacity=".6" stroke-width="5" stroke-linecap="round"/>')
        g.append(f'<text x="0" y="-262" text-anchor="middle" class="ser7" font-size="64" fill="{C["rosary"]}" fill-opacity=".9">?</text>')
    body = f'<g transform="translate({f(cx)} {f(cy)}) scale({f(scale, 3)})">{"".join(g)}</g>'
    return defs, body, css
