"""Procedural ink-and-blood artwork shared by every panel.

Everything is generated (no clip-art): AZ monogram, hanko seal, sakura branches and falling
petals, sumi brush strokes with dry-bristle tails, ensō, sun, katana, sword slash, layered
mountains with mist, torii gates, a walking samurai and ink splatter.
"""
import math

from svgkit import C, f, rad, seeded

# =============================================================================== AZ monogram
# Redrawn from the user's logo: an A whose crossbar is a katana-like swoosh, fused with a Z.
# Box: 60 x 45.6 units.
AZ_PATH = ("M28.4 0L37.1 13.6L29.6 13.6L27.95 11.2L19 25.8C24 23.6 32 22.6 39.4 24.4"
           "C35 27.2 21 28.6 13 34L7.05 43.6L0 43.6Z"
           "M30.7 14.8L59.9 14.8L56.5 20.6L36.5 39.5L60 39.5L53.5 45.6L22.3 45.6L48 20.6L35 20.6Z")
AZ_W, AZ_H = 60.0, 45.6


def az(cx, cy, width, fill, op=1.0, extra=""):
    k = width / AZ_W
    return (f'<path transform="translate({f(cx - AZ_W*k/2)} {f(cy - AZ_H*k/2)}) scale({f(k, 4)})" '
            f'd="{AZ_PATH}" fill="{fill}" fill-opacity="{f(op, 2)}" {extra}/>')


def hanko(uid, cx, cy, size, rot=-4, seed=3, color=None, ink=None):
    """Red seal stamp with the AZ monogram carved out; speckled like real cinnabar ink."""
    color = color or C["blood"]
    ink = ink or C["rosary"]
    r = seeded(seed)
    s = size
    # slightly irregular rounded square
    pts = []
    for i in range(40):
        a = 2 * math.pi * i / 40
        sq = 1 / max(abs(math.cos(a)), abs(math.sin(a))) ** 0.92
        rr = s / 2 * min(sq, 1.32) * (1 + (r() - .5) * .025)
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d = "M" + "L".join(f"{f(x)} {f(y)}" for x, y in pts) + "Z"
    specks = "".join(
        f'<circle cx="{f(cx + (r() - .5) * s * .95)}" cy="{f(cy + (r() - .5) * s * .95)}" r="{f(.3 + r() ** 2 * s * .018, 2)}" fill="#000"/>'
        for _ in range(int(s * 1.1)))
    m = (f'<mask id="{uid}hk" maskUnits="userSpaceOnUse" x="{f(cx - s)}" y="{f(cy - s)}" width="{f(2*s)}" height="{f(2*s)}">'
         f'<rect x="{f(cx - s)}" y="{f(cy - s)}" width="{f(2*s)}" height="{f(2*s)}" fill="#fff"/>{specks}</mask>')
    inner = s * 0.82
    body = (f'<g transform="rotate({rot} {f(cx)} {f(cy)})" mask="url(#{uid}hk)">'
            f'<path d="{d}" fill="{color}"/>'
            f'<rect x="{f(cx - inner/2)}" y="{f(cy - inner/2)}" width="{f(inner)}" height="{f(inner)}" rx="{f(s*.06)}" fill="none" '
            f'stroke="{ink}" stroke-width="{f(s*.035)}" stroke-opacity=".9"/>'
            + az(cx, cy + s * .02, s * .62, ink, .95) + "</g>")
    return m, body


# =============================================================================== sakura
PETAL = ("M0 0C-5 -2 -7 -9 -4.6 -13C-3.2 -15.2 -1.2 -15.6 0 -13.6C1.2 -15.6 3.2 -15.2 4.6 -13"
         "C7 -9 5 -2 0 0Z")


def blossom_defs(uid):
    """Symbols: full bloom (#uidbF), red bloom (#uidbR), half-open (#uidbH), bud (#uidbB), petal (#uidpt)."""
    def flower(fid, grad, n=5, sc=1.0, stamen=True):
        petals = "".join(f'<path d="{PETAL}" transform="rotate({i * 360 / n}) scale({sc})" fill="url(#{grad})"/>' for i in range(n))
        st = ""
        if stamen:
            st = "".join(
                f'<path d="M0 0L{f(5.4*math.cos(rad(a)))} {f(5.4*math.sin(rad(a)))}" stroke="{C["blush_deep"]}" stroke-width=".55"/>'
                f'<circle cx="{f(5.8*math.cos(rad(a)))}" cy="{f(5.8*math.sin(rad(a)))}" r=".9" fill="{C["brass_hi"]}"/>'
                for a in range(10, 360, 40))
        return f'<g id="{fid}">{petals}<circle r="2.6" fill="{C["blush_deep"]}"/>{st}</g>'
    return (
        f'<radialGradient id="{uid}pg" cx="0" cy="0" r="16" gradientUnits="userSpaceOnUse">'
        f'<stop offset="0" stop-color="{C["blush_deep"]}"/><stop offset=".35" stop-color="{C["blush"]}"/>'
        f'<stop offset="1" stop-color="{C["rosary"]}"/></radialGradient>'
        f'<radialGradient id="{uid}rg" cx="0" cy="0" r="16" gradientUnits="userSpaceOnUse">'
        f'<stop offset="0" stop-color="{C["rose"]}"/><stop offset=".45" stop-color="{C["blood"]}"/>'
        f'<stop offset="1" stop-color="{C["blood_hi"]}"/></radialGradient>'
        + flower(f"{uid}bF", f"{uid}pg")
        + flower(f"{uid}bR", f"{uid}rg")
        + f'<g id="{uid}bH">'
        + "".join(f'<path d="{PETAL}" transform="rotate({a}) scale(.92 .8)" fill="url(#{uid}pg)"/>' for a in (-62, -24, 18, 58))
        + f'<circle r="2.2" cy="-1" fill="{C["blush_deep"]}"/></g>'
        + f'<g id="{uid}bB"><path d="M0 0C-3 -3 -3.4 -8 0 -11C3.4 -8 3 -3 0 0Z" fill="{C["blush"]}"/>'
          f'<path d="M0 0C-2 -2 -2.6 -5 -1.4 -7M0 0C2 -2 2.6 -5 1.4 -7" stroke="{C["wine"]}" stroke-width="1.1" fill="none"/></g>'
        + f'<path id="{uid}pt" d="{PETAL}" transform="translate(0 7)"/>'
    )


def _bez(p0, p1, p2, p3, t):
    u = 1 - t
    return (u**3 * p0[0] + 3*u*u*t * p1[0] + 3*u*t*t * p2[0] + t**3 * p3[0],
            u**3 * p0[1] + 3*u*u*t * p1[1] + 3*u*t*t * p2[1] + t**3 * p3[1])


def _limb(points, w0, w1, rnd, rough=0.12):
    """Tapered branch outline along a polyline."""
    n = len(points)
    L, R = [], []
    for i, (x, y) in enumerate(points):
        a = points[min(i + 1, n - 1)]
        b = points[max(i - 1, 0)]
        dx, dy = a[0] - b[0], a[1] - b[1]
        ln = math.hypot(dx, dy) or 1
        nx, ny = -dy / ln, dx / ln
        t = i / (n - 1)
        w = (w0 + (w1 - w0) * t ** 0.85) / 2
        w1_ = w * (1 + (rnd() - .5) * rough)
        w2_ = w * (1 + (rnd() - .5) * rough)
        L.append((x + nx * w1_, y + ny * w1_))
        R.append((x - nx * w2_, y - ny * w2_))
    pts = L + R[::-1]
    return "M" + "L".join(f"{f(x)} {f(y)}" for x, y in pts) + "Z"


def sakura_branch(uid, x0, y0, angle, length, width, seed=1, depth=2, bloom=1.0, color=None,
                  red_ratio=0.18, bud_ratio=0.18, scale=1.0, up_only=False):
    """Returns svg: limbs (ink silhouette) + blossoms (<use> of blossom_defs symbols).
    up_only keeps every child limb rising (for branches that must stay in a top band)."""
    color = color or "#0B0405"
    rnd = seeded(seed)
    limbs, flowers = [], []
    sag = 0.0 if up_only else 1.0

    def grow(x, y, ang, L, w, d):
        bend = (rnd() - .5) * 0.9
        if up_only:
            bend = -abs(bend) * (1 if math.cos(rad(ang)) >= 0 else -1)
        a0 = rad(ang)
        p0 = (x, y)
        p1 = (x + math.cos(a0) * L * .35, y + math.sin(a0) * L * .35)
        a1 = a0 + bend
        p2 = (x + math.cos(a1) * L * .7, y + math.sin(a1) * L * .7 + L * .06 * sag)
        a2 = a1 + bend * .6
        p3 = (x + math.cos(a2) * L, y + math.sin(a2) * L + L * .08 * sag)
        n = max(8, int(L / 7))
        pts = [_bez(p0, p1, p2, p3, i / (n - 1)) for i in range(n)]
        w_end = max(1.0, w * 0.18)
        limbs.append(_limb(pts, w, w_end, rnd))
        # children
        if d > 0:
            kids = 2 + int(rnd() * 2.2)
            for k in range(kids):
                t = 0.28 + 0.62 * (k + rnd() * .6) / kids
                i = int(t * (n - 1))
                cx, cy = pts[i]
                seg = (pts[min(i + 1, n - 1)][0] - pts[i - 1][0], pts[min(i + 1, n - 1)][1] - pts[i - 1][1])
                base = math.degrees(math.atan2(seg[1], seg[0]))
                side = 1 if rnd() < .5 else -1
                child = base + side * (24 + rnd() * 34)
                if up_only and math.sin(rad(child)) > -0.05:
                    child = base - side * (24 + rnd() * 34)
                    if math.sin(rad(child)) > 0.25:
                        child = base
                grow(cx, cy, child, L * (0.32 + rnd() * .3),
                     max(1.2, (w + (w_end - w) * t) * 0.62), d - 1)
        # flowers along the outer half + a cluster at the tip
        nf = int((3 + L / 26) * bloom)
        for _ in range(nf):
            t = 0.45 + rnd() * 0.55
            i = int(t * (n - 1))
            px, py = pts[i]
            off = 4 + rnd() * 9
            a = rnd() * 2 * math.pi
            flowers.append((px + math.cos(a) * off, py + math.sin(a) * off))
        tx, ty = pts[-1]
        for _ in range(int(3 * bloom)):
            flowers.append((tx + (rnd() - .5) * 18, ty + (rnd() - .5) * 18))

    grow(x0, y0, angle, length, width, depth)
    uses = []
    for (x, y) in flowers:
        u = rnd()
        kind = "bR" if u < red_ratio else ("bB" if u < red_ratio + bud_ratio else ("bH" if u < red_ratio + bud_ratio + .2 else "bF"))
        s = (0.55 + rnd() * 0.65) * scale * (0.6 if kind == "bB" else 1)
        uses.append(f'<use href="#{uid}{kind}" transform="translate({f(x)} {f(y)}) rotate({int(rnd()*360)}) scale({f(s, 2)})"/>')
    return f'<g fill="{color}">{"".join(f"<path d=\"{d}\"/>" for d in limbs)}</g>' + "".join(uses)


PETAL_CSS_DONE = set()


def falling_petals(uid, w, h, n, seed=5, size=(0.55, 1.15), op=(0.55, 0.95), dur=(11, 19), red=0.25,
                   area=None, wind=1.0):
    """Petals drifting across the panel with a 3D tumble. Returns (css, svg)."""
    r = seeded(seed)
    css = (
        f"@keyframes {uid}fa{{0%{{transform:translate(0,-40px)}}25%{{transform:translate({f(60*wind)}px,{f(h*.27)}px)}}"
        f"50%{{transform:translate({f(20*wind)}px,{f(h*.52)}px)}}75%{{transform:translate({f(95*wind)}px,{f(h*.77)}px)}}"
        f"100%{{transform:translate({f(70*wind)}px,{f(h+40)}px)}}}}"
        f"@keyframes {uid}fb{{0%{{transform:translate(0,-40px)}}30%{{transform:translate({f(-30*wind)}px,{f(h*.3)}px)}}"
        f"60%{{transform:translate({f(40*wind)}px,{f(h*.62)}px)}}100%{{transform:translate({f(10*wind)}px,{f(h+40)}px)}}}}"
        f"@keyframes {uid}tm{{0%{{transform:rotate(0) scale(1,1)}}25%{{transform:rotate(90deg) scale(.25,1)}}"
        f"50%{{transform:rotate(180deg) scale(1,.7)}}75%{{transform:rotate(270deg) scale(.3,1)}}100%{{transform:rotate(360deg) scale(1,1)}}}}"
        f".{uid}fa{{animation:{uid}fa linear infinite}}.{uid}fb{{animation:{uid}fb linear infinite}}"
        f".{uid}tm{{animation:{uid}tm ease-in-out infinite}}"
    )
    ranges = area if isinstance(area, list) else [area or (0, w)]
    total = sum(b - a for a, b in ranges)
    out = []
    for i in range(n):
        pick = r() * total
        for a, b in ranges:
            if pick <= b - a:
                x = a + pick
                break
            pick -= b - a
        d = dur[0] + r() * (dur[1] - dur[0])
        delay = -r() * d
        s = size[0] + r() * (size[1] - size[0])
        o = op[0] + r() * (op[1] - op[0])
        fill = C["blood"] if r() < red else (C["blush"] if r() < .55 else C["rosary"])
        kind = "fa" if r() < .5 else "fb"
        out.append(
            f'<g transform="translate({f(x)} 0)"><g class="{uid}{kind}" style="animation-duration:{f(d)}s;animation-delay:{f(delay)}s">'
            f'<g transform="scale({f(s, 2)})"><use href="#{uid}pt" class="{uid}tm" fill="{fill}" fill-opacity="{f(o, 2)}" '
            f'style="animation-duration:{f(2.6 + r()*3)}s;animation-delay:{f(-r()*4)}s"/></g></g></g>')
    return css, "".join(out)


# =============================================================================== sumi brush
def brush_streaks(points, width, seed=1, n=9, t0=0.25):
    """Dry-brush texture: thin hair-lines inside a stroke (paint them in the background colour)."""
    rnd = seeded(seed + 101)
    npt = len(points)
    normals = []
    for i in range(npt):
        a = points[min(i + 1, npt - 1)]
        b = points[max(i - 1, 0)]
        dx, dy = a[0] - b[0], a[1] - b[1]
        ln = math.hypot(dx, dy) or 1
        normals.append((-dy / ln, dx / ln))
    out = []
    for _ in range(n):
        lane = (rnd() - .5) * .8
        s = t0 + rnd() * (1 - t0) * .6
        e = min(1.0, s + .15 + rnd() * .5)
        pts = []
        for i in range(int(s * (npt - 1)), int(e * (npt - 1))):
            t = i / (npt - 1)
            w = width * (1.3 - 0.75 * t)
            x, y = points[i]
            nx, ny = normals[i]
            pts.append((x + nx * lane * w * .5, y + ny * lane * w * .5))
        if len(pts) > 2:
            out.append("M" + "L".join(f"{f(x)} {f(y)}" for x, y in pts))
    return "".join(out)


def brush_stroke(points, width, seed=1, start_blob=1.25, tail=0.32, bristles=6, rough=0.08, w_end=0.55):
    """Ink stroke: a solid body with a dry-bristle tail. points: dense centreline."""
    rnd = seeded(seed)
    n = len(points)
    cum = [0.0]
    for i in range(1, n):
        cum.append(cum[-1] + math.hypot(points[i][0] - points[i-1][0], points[i][1] - points[i-1][1]))
    total = cum[-1] or 1
    T = [c / total for c in cum]
    normals = []
    for i in range(n):
        a = points[min(i + 1, n - 1)]
        b = points[max(i - 1, 0)]
        dx, dy = a[0] - b[0], a[1] - b[1]
        ln = math.hypot(dx, dy) or 1
        normals.append((-dy / ln, dx / ln))

    ph = rnd() * 6.28

    def wprof(t):
        if t < 0.06:
            base = 0.7 + (start_blob - 0.7) * (t / 0.06) ** .5
        elif t < 0.16:
            base = start_blob + (1 - start_blob) * (t - .06) / .1
        else:
            base = 1 - (1 - w_end) * (t - .16) / .84
        # brush pressure breathes along the stroke
        return width * base * (1 + 0.11 * math.sin(7.5 * t + ph) + 0.05 * math.sin(19 * t + ph * 2))

    body_end = 1 - tail
    L, R = [], []
    for i in range(n):
        t = T[i]
        if t > body_end + 0.04:
            break
        w = wprof(t) / 2
        nx, ny = normals[i]
        e1 = w * (1 + (rnd() - .5) * rough)
        e2 = w * (1 + (rnd() - .5) * rough)
        x, y = points[i]
        L.append((x + nx * e1, y + ny * e1))
        R.append((x - nx * e2, y - ny * e2))
    paths = ["M" + "L".join(f"{f(x)} {f(y)}" for x, y in L + R[::-1]) + "Z"]
    # bristles: thin lanes that run dry at different points
    for b in range(bristles):
        lane = -0.5 + (b + 0.5) / bristles
        stop = body_end + (1 - body_end) * (0.35 + 0.65 * rnd() ** .7)
        lw = 0.5 / bristles * (0.7 + rnd() * .6)
        Lb, Rb = [], []
        for i in range(n):
            t = T[i]
            if t < body_end - 0.02:
                continue
            if t > stop:
                break
            w = wprof(t)
            k = 1 - max(0.0, (t - (stop - .06)) / .06)
            nx, ny = normals[i]
            c = lane * w * (1 + (t - body_end) * 0.6)
            h = lw * w * max(0.15, k)
            x, y = points[i]
            Lb.append((x + nx * (c + h), y + ny * (c + h)))
            Rb.append((x + nx * (c - h), y + ny * (c - h)))
        if len(Lb) > 1:
            paths.append("M" + "L".join(f"{f(x)} {f(y)}" for x, y in Lb + Rb[::-1]) + "Z")
    return "".join(paths)


def enso_points(cx, cy, r, seed=2, start_deg=-58, sweep=322, wobble=0.025, n=140):
    rnd = seeded(seed)
    pts = []
    ph = rnd() * 6
    for i in range(n):
        t = i / (n - 1)
        a = rad(start_deg - sweep * t)  # counter-clockwise on screen
        rr = r * (1 + wobble * math.sin(3 * a + ph) + (t ** 3) * 0.045)
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return pts


def enso(cx, cy, r, width, seed=2, start_deg=-58, sweep=322, wobble=0.025):
    """(body path, dry-streak path) of a zen circle."""
    pts = enso_points(cx, cy, r, seed, start_deg, sweep, wobble)
    body = brush_stroke(pts, width, seed=seed, tail=0.34, bristles=8, w_end=0.42, start_blob=1.45)
    return body, brush_streaks(pts, width, seed=seed, n=11, t0=0.2)


def ink_splatter(cx, cy, spread, n, seed=4, color="#000", op=0.9, angle=None):
    r = seeded(seed)
    out = []
    for _ in range(n):
        a = rad(angle + (r() - .5) * 50) if angle is not None else r() * 2 * math.pi
        d = spread * r() ** 1.6
        x, y = cx + math.cos(a) * d, cy + math.sin(a) * d
        rad_ = 0.4 + (1 - d / spread) * r() * 3.4
        if angle is not None and r() < .4:
            out.append(f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(rad_*2.2)}" ry="{f(rad_*.7)}" '
                       f'transform="rotate({f(math.degrees(a))} {f(x)} {f(y)})"/>')
        else:
            out.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(rad_, 2)}"/>')
    return f'<g fill="{color}" fill-opacity="{op}">{"".join(out)}</g>'


# =============================================================================== sun / sky
def sun_defs(uid):
    return (f'<radialGradient id="{uid}sun" cx="42%" cy="38%" r="65%">'
            f'<stop offset="0" stop-color="{C["ember"]}"/><stop offset=".45" stop-color="{C["blood_hi"]}"/>'
            f'<stop offset=".85" stop-color="{C["blood"]}"/><stop offset="1" stop-color="{C["wine"]}"/></radialGradient>'
            f'<radialGradient id="{uid}glow" cx="50%" cy="50%" r="50%">'
            f'<stop offset=".45" stop-color="{C["blood"]}" stop-opacity=".45"/><stop offset=".7" stop-color="{C["blood"]}" stop-opacity=".12"/>'
            f'<stop offset="1" stop-color="{C["blood"]}" stop-opacity="0"/></radialGradient>')


def sun(uid, cx, cy, r, glow=True):
    g = f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r*1.9)}" fill="url(#{uid}glow)"/>' if glow else ""
    rings = "".join(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r*k)}" fill="none" stroke="#000" stroke-opacity=".05" stroke-width="{f(r*.012)}"/>'
                    for k in (0.55, 0.7, 0.84))
    return g + f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="url(#{uid}sun)"/>' + rings


def mountains(uid, x0, x1, base, heights, colors, seed=9, peaks=2.2, steps=90):
    """Layered ridge silhouettes, back to front. heights/colors per layer."""
    r = seeded(seed)
    out = []
    for li, (H, col) in enumerate(zip(heights, colors)):
        ph = [r() * 6.28 for _ in range(3)]
        fr = [peaks * (0.8 + r() * .5), peaks * (2.1 + r()), peaks * (4.7 + r() * 2)]
        pts = []
        for i in range(steps + 1):
            u = i / steps
            x = x0 + (x1 - x0) * u
            v = (0.6 * (1 - abs(math.sin(u * fr[0] + ph[0]))) + 0.28 * (1 - abs(math.sin(u * fr[1] + ph[1])))
                 + 0.12 * (1 - abs(math.sin(u * fr[2] + ph[2]))))
            pts.append((x, base - H * (0.25 + 0.75 * v)))
        d = f"M{f(x0)} {f(base + 400)}L" + "L".join(f"{f(x)} {f(y)}" for x, y in pts) + f"L{f(x1)} {f(base + 400)}Z"
        out.append(f'<path d="{d}" fill="{col}"/>')
    return "".join(out)


# =============================================================================== katana
def katana(uid, x, y, L, angle=0, scale=1.0):
    """Side view, blade pointing +x, edge down; (x, y) = tsuba centre."""
    w0 = 0.034 * L
    sori = 0.035 * L
    n = 40
    tip_start = 0.92
    spine, edge = [], []
    for i in range(n + 1):
        t = i / n
        xx = 0.03 * L + t * 0.97 * L
        yc = -sori * t ** 2
        w = w0 * (1 - 0.28 * t)
        sp = yc - w / 2
        ed = yc + w / 2
        if t > tip_start:
            k = (t - tip_start) / (1 - tip_start)
            ed = ed - (ed - (sp + w * 0.08)) * k ** 1.6
        spine.append((xx, sp))
        edge.append((xx, ed))
    blade = "M" + "L".join(f"{f(a)} {f(b)}" for a, b in spine) + "L" + "L".join(f"{f(a)} {f(b)}" for a, b in reversed(edge)) + "Z"
    ridge = "M" + "L".join(f"{f(a)} {f(b + (e - b) * .38)}" for (a, b), (_, e) in zip(spine[:int(n*tip_start)], edge[:int(n*tip_start)]))
    hamon = []
    for i in range(int(n * tip_start * 4) + 1):
        t = i / (n * 4)
        xx = 0.04 * L + t * 0.97 * L
        yc = -sori * t ** 2
        w = w0 * (1 - 0.28 * t)
        yy = yc + w / 2 - w * (0.3 + 0.09 * math.sin(t * 95) + 0.05 * math.sin(t * 233))
        hamon.append((xx, yy))
    hamon_d = "M" + "L".join(f"{f(a)} {f(b)}" for a, b in hamon)
    hl = 0.3 * L  # handle length
    th = 0.044 * L  # handle thickness
    diamonds = []
    k = 9
    for i in range(k):
        cx_ = -0.045 * L - (i + .5) * (hl - 0.03 * L) / k
        dw = (hl - 0.03 * L) / k * 0.48
        diamonds.append(f"M{f(cx_ - dw)} 0L{f(cx_)} {f(-th*.32)}L{f(cx_ + dw)} 0L{f(cx_)} {f(th*.32)}Z")
    defs = (f'<linearGradient id="{uid}steel" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="#5E5650"/><stop offset=".3" stop-color="#A9A08F"/>'
            f'<stop offset=".42" stop-color="#F3EBD7"/><stop offset=".62" stop-color="#C7BEAB"/>'
            f'<stop offset=".9" stop-color="#F6F0E2"/><stop offset="1" stop-color="#8D857A"/></linearGradient>'
            f'<linearGradient id="{uid}brs" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{C["brass_hi"]}"/>'
            f'<stop offset=".5" stop-color="{C["brass"]}"/><stop offset="1" stop-color="{C["brass_lo"]}"/></linearGradient>')
    g = (f'<g transform="translate({f(x)} {f(y)}) rotate({f(angle)}) scale({f(scale, 3)})">'
         f'<path d="{blade}" fill="url(#{uid}steel)"/>'
         f'<path d="{ridge}" fill="none" stroke="#fff" stroke-opacity=".35" stroke-width="{f(L*.0015, 2)}"/>'
         f'<path d="{hamon_d}" fill="none" stroke="#fff" stroke-opacity=".75" stroke-width="{f(L*.0022, 2)}"/>'
         # habaki
         f'<path d="M{f(.008*L)} {f(-w0*.62)}L{f(.05*L)} {f(-w0*.58)}L{f(.05*L)} {f(w0*.56)}L{f(.008*L)} {f(w0*.62)}Z" fill="url(#{uid}brs)"/>'
         # seppa + tsuba (edge-on)
         f'<rect x="{f(-.004*L)}" y="{f(-w0*.95)}" width="{f(.012*L)}" height="{f(w0*1.9)}" fill="{C["brass_hi"]}"/>'
         f'<rect x="{f(-.022*L)}" y="{f(-.068*L)}" width="{f(.018*L)}" height="{f(.136*L)}" rx="{f(.006*L)}" fill="url(#{uid}brs)"/>'
         f'<rect x="{f(-.019*L)}" y="{f(-.06*L)}" width="{f(.006*L)}" height="{f(.12*L)}" fill="#000" fill-opacity=".35"/>'
         # tsuka
         f'<rect x="{f(-.024*L - hl)}" y="{f(-th/2)}" width="{f(hl)}" height="{f(th)}" rx="{f(th*.35)}" fill="#0B0607"/>'
         f'<path d="{"".join(diamonds)}" fill="{C["rosary"]}" fill-opacity=".88"/>'
         f'<rect x="{f(-.04*L)}" y="{f(-th*.56)}" width="{f(.018*L)}" height="{f(th*1.12)}" rx="{f(th*.1)}" fill="url(#{uid}brs)"/>'
         f'<rect x="{f(-.024*L - hl - .012*L)}" y="{f(-th*.56)}" width="{f(.022*L)}" height="{f(th*1.12)}" rx="{f(th*.4)}" fill="url(#{uid}brs)"/>'
         f'<path d="M{f(-.024*L - hl*.62)} {f(-th*.18)}c{f(L*.012)} {f(-th*.28)} {f(L*.03)} {f(-th*.28)} {f(L*.04)} 0" fill="none" stroke="{C["brass_hi"]}" stroke-width="{f(th*.18)}" stroke-linecap="round"/>'
         f"</g>")
    return defs, g


def slash(uid, x1, y1, x2, y2, bow=26, thick=7, glow=True, anim=True, period=7.0, begin=0.0):
    """Crescent sword-cut from (x1,y1) to (x2,y2)."""
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    dx, dy = x2 - x1, y2 - y1
    ln = math.hypot(dx, dy)
    nx, ny = -dy / ln, dx / ln

    def cres(b, t):
        c1 = (mx + nx * b, my + ny * b)
        c2 = (mx + nx * (b - t), my + ny * (b - t))
        return (f"M{f(x1)} {f(y1)}Q{f(c1[0])} {f(c1[1])} {f(x2)} {f(y2)}"
                f"Q{f(c2[0])} {f(c2[1])} {f(x1)} {f(y1)}Z")
    defs = (f'<linearGradient id="{uid}sl" gradientUnits="userSpaceOnUse" x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}">'
            f'<stop offset="0" stop-color="{C["rosary"]}" stop-opacity="0"/><stop offset=".35" stop-color="#FFF8EA"/>'
            f'<stop offset=".7" stop-color="{C["rosary"]}"/><stop offset="1" stop-color="{C["rosary"]}" stop-opacity="0"/></linearGradient>'
            f'<linearGradient id="{uid}slg" gradientUnits="userSpaceOnUse" x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}">'
            f'<stop offset="0" stop-color="{C["blood_hi"]}" stop-opacity="0"/><stop offset=".4" stop-color="{C["blood_hi"]}" stop-opacity=".55"/>'
            f'<stop offset="1" stop-color="{C["blood_hi"]}" stop-opacity="0"/></linearGradient>')
    g = ""
    if glow:
        g += f'<path d="{cres(bow + 7, thick + 14)}" fill="url(#{uid}slg)" opacity=".35"/>'
        g += f'<path d="{cres(bow + 3, thick + 6)}" fill="url(#{uid}slg)" opacity=".6"/>'
    g += f'<path d="{cres(bow, thick)}" fill="url(#{uid}sl)"/>'
    css = ""
    if anim:
        css = (f"@keyframes {uid}cut{{0%{{opacity:0;transform:scale(.6)}}4%{{opacity:1;transform:scale(1)}}"
               f"55%{{opacity:1}}80%,100%{{opacity:.45}}}}"
               f".{uid}cut{{transform-box:fill-box;transform-origin:0 0;animation:{uid}cut {period}s cubic-bezier(.2,.9,.2,1) {f(begin)}s infinite}}")
        g = f'<g class="{uid}cut">{g}</g>'
    return defs, g, css


# =============================================================================== architecture / figures
def torii(x, y, w, h, color=None, top=None, op=1.0):
    color = color or C["blood"]
    top = top or "#0B0405"
    pw = w * 0.075
    p = []
    for sx in (-1, 1):
        cx = x + sx * w * 0.32
        p.append(f"M{f(cx - pw/2 + sx*w*.012)} {f(y - h*.9)}L{f(cx + pw/2 + sx*w*.012)} {f(y - h*.9)}"
                 f"L{f(cx + pw*.62)} {f(y)}L{f(cx - pw*.62)} {f(y)}Z")
    p.append(f"M{f(x - w*.47)} {f(y - h*.73)}h{f(w*.94)}v{f(h*.055)}h{f(-w*.94)}Z")
    p.append(f"M{f(x - pw*.35)} {f(y - h*.86)}h{f(pw*.7)}v{f(h*.13)}h{f(-pw*.7)}Z")
    p.append(f"M{f(x - w*.5)} {f(y - h*.875)}h{f(w)}v{f(h*.045)}h{f(-w)}Z")
    kasagi = (f"M{f(x - w*.62)} {f(y - h*1.0)}Q{f(x)} {f(y - h*.9)} {f(x + w*.62)} {f(y - h*1.0)}"
              f"L{f(x + w*.56)} {f(y - h*.93)}Q{f(x)} {f(y - h*.85)} {f(x - w*.56)} {f(y - h*.93)}Z")
    return (f'<g fill-opacity="{f(op, 2)}"><path d="{"".join(p)}" fill="{color}"/>'
            f'<path d="{kasagi}" fill="{top}"/></g>')


SAMURAI = (  # walking ronin, 64 x 100 box, facing right, feet at y=100. Hair styled like the portrait.
    "M27 6C28 1.5 33 -.5 37.5 1.5C40.5 0 44 2 43.6 5.4C46 6.6 46.2 10 44.2 11.6C45.2 14.6 44.4 18.2 42.4 19.8"
    "L42 23.5C43.5 23.7 44.6 25 44.4 26.6L43.6 28.2L46.8 29.6C50.5 31.4 52.8 35.6 53.2 40L54.2 50.5"
    "L58.5 49.2L60.2 51.8L54.6 55.2L52.4 54.4L51.2 46.6L49.2 47.8L50.6 60.6C56 74 60.4 86 63.2 98.6L63.4 100"
    "L50.4 100L47.2 88L42.4 77.4L38.4 88.8L37.8 100L22.4 100L23.8 96C24.6 84 26.6 72 30.4 61.2L29.6 50.4"
    "L25 56.6L17.2 58.6L15.8 55.6L22.8 51.8L26 41.6C26.8 36.4 29.6 31.8 33.6 29.6L35.4 28.6L34.2 26.6"
    "C33 25.4 32.8 23.6 33.6 22.4C31.8 20.2 31 17.6 31.4 15.2C29 14.4 27.4 12.4 27.6 10C26.4 9.2 26.2 7.6 27 6Z")
SAMURAI_SWORD = "M28.4 52.2L1.2 63.8L.4 62L27.6 50.4ZM30.2 51L46.8 44.2L47.6 46L31 52.8Z"


def samurai(x, y, h, fill=None, sword=None, flip=False, extra=""):
    fill = fill or "#0B0405"
    sword = sword or C["brass"]
    k = h / 100.0
    sx = -k if flip else k
    return (f'<g transform="translate({f(x)} {f(y - h)}) scale({f(sx, 4)} {f(k, 4)}) translate(-32 0)" {extra}>'
            f'<path d="{SAMURAI_SWORD}" fill="{sword}"/><path d="{SAMURAI}" fill="{fill}"/></g>')


# =============================================================================== editorial details
def hair_rule(x, y, w, color=None, op=0.35):
    color = color or C["brass"]
    return f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="1" fill="{color}" fill-opacity="{f(op, 2)}"/>'


def crop_marks(w, h, m=18, L=14, color=None, op=0.5):
    color = color or C["brass"]
    d = []
    for (x, y, sx, sy) in ((m, m, 1, 1), (w - m, m, -1, 1), (m, h - m, 1, -1), (w - m, h - m, -1, -1)):
        d.append(f"M{f(x - sx*6)} {f(y)}h{f(sx*(L+6))}M{f(x)} {f(y - sy*6)}v{f(sy*(L+6))}")
    return f'<path d="{"".join(d)}" stroke="{color}" stroke-opacity="{f(op, 2)}" stroke-width="1" fill="none"/>'
