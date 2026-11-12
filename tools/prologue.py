"""序 PROLOGUE — the hero panel: portrait before a blood sun, ensō, sakura, name, seal, the first cut."""
import os

import art
import scene
from svgkit import C, data_uri, doc, f, grain_defs, kanji, measure, text, write

W, H = 1200, scene.HEIGHT["prologue"]
SUN = (884, 292, 226)
PORTRAIT = (628, 96, 660)  # x, y, size of the 800x800 cut-out


def build(out_dir):
    u = "pr"
    sx, sy, sr = SUN
    px, py, ps = PORTRAIT
    defs, body, css = [], [], []

    # ------------------------------------------------------------------ backdrop
    defs.append(f'<radialGradient id="{u}bg" cx="72%" cy="42%" r="75%"><stop offset="0" stop-color="#2A070B"/>'
                f'<stop offset=".45" stop-color="#110305"/><stop offset="1" stop-color="{C["night"]}"/></radialGradient>'
                f'<linearGradient id="{u}fade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{C["night"]}" stop-opacity="0"/>'
                f'<stop offset=".55" stop-color="{C["night"]}" stop-opacity=".75"/><stop offset="1" stop-color="{C["night"]}"/></linearGradient>'
                f'<linearGradient id="{u}lf" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{C["night"]}"/>'
                f'<stop offset="1" stop-color="{C["night"]}" stop-opacity="0"/></linearGradient>')
    body.append(f'<rect width="{W}" height="{H}" fill="url(#{u}bg)"/>')

    # ------------------------------------------------------------------ sun + ensō
    defs.append(art.sun_defs(u))
    body.append(art.sun(u, sx, sy, sr))
    enso_d, enso_streaks = art.enso(sx, sy, sr * 1.17, 21, seed=12, start_deg=-52, sweep=318)
    # draw-on mask that follows the brush direction
    import math
    a0 = math.radians(-52)
    r_m = sr * 1.17
    x0_, y0_ = sx + r_m * math.cos(a0), sy + r_m * math.sin(a0)
    a1 = math.radians(-52 - 330)
    x1_, y1_ = sx + r_m * math.cos(a1), sy + r_m * math.sin(a1)
    circ = 2 * math.pi * r_m * 330 / 360
    defs.append(f'<mask id="{u}em" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}">'
                f'<path d="M{f(x0_)} {f(y0_)}A{f(r_m)} {f(r_m)} 0 1 0 {f(x1_)} {f(y1_)}" fill="none" stroke="#fff" stroke-width="70" '
                f'stroke-dasharray="{f(circ)}" stroke-dashoffset="{f(circ)}" class="{u}draw"/></mask>')
    css.append(f"@keyframes {u}dr{{to{{stroke-dashoffset:0}}}}.{u}draw{{animation:{u}dr 2.6s .4s cubic-bezier(.55,.1,.25,1) forwards}}")
    body.append(f'<g mask="url(#{u}em)"><path d="{enso_d}" fill="{C["rosary"]}" fill-opacity=".9"/>'
                f'<path d="{enso_streaks}" fill="none" stroke="#1A0508" stroke-opacity=".6" stroke-width="1.3" stroke-linecap="round"/></g>')

    # ------------------------------------------------------------------ petals behind
    defs.append(art.blossom_defs(u))
    pcss, back_petals = art.falling_petals(u + "b", W, H, 12, seed=4, size=(.35, .65), op=(.25, .5), dur=(16, 24))
    css.append(pcss)
    defs.append(f'<path id="{u}bpt" d="{art.PETAL}" transform="translate(0 7)"/>')
    body.append(back_petals.replace(f"#{u}bpt", f"#{u}bpt"))

    # ------------------------------------------------------------------ sakura branch (between sun and portrait)
    body.append(art.sakura_branch(u, 1224, 176, 197, 270, 16, seed=23, depth=2, bloom=.85, scale=.9))

    # ------------------------------------------------------------------ portrait
    body.append(f'<image href="{data_uri("portrait.webp")}" x="{px}" y="{py}" width="{ps}" height="{ps}" preserveAspectRatio="xMidYMid meet"/>')
    body.append(f'<rect x="{px}" y="{H - 200}" width="{W - px}" height="200" fill="url(#{u}fade)"/>')


    # ------------------------------------------------------------------ the cut (continues into 壱)
    sd, sg, scss = scene.slash("prologue", u + "s")
    defs.append(sd)
    css.append(scss)
    body.append(sg)
    body.append(art.ink_splatter(560, 640, 70, 26, seed=8, color=C["blood"], op=.75, angle=14))

    # ------------------------------------------------------------------ identity
    kx = 92
    body.append(kanji("武士道", kx, 100, 70, fill=C["blood_hi"], style="brush", vertical=True, gap=.06))
    body.append(f'<rect x="{kx + 50}" y="104" width="1" height="236" fill="{C["brass"]}" fill-opacity=".45"/>')
    tx = 168
    body.append(kanji("序", tx, 131, 17, fill=C["brass"], style="mincho"))
    body.append(text(tx + 26, 130, "PROLOGUE  —  THE WAY OF THE BUILDER", "san7", 11.5, C["brass"], tracking=4.2))
    ns, track = 106, 9
    for i, word in enumerate(("AHMED", "ZAKI", "GABR")):
        body.append(text(tx - 4, 240 + i * 96, word, "ser7", ns, C["rosary"], tracking=track))
    gw = measure("GABR", "ser7", ns, track)
    hm, hb = art.hanko(u, tx + gw + 52, 402, 66, rot=-6, seed=5)
    defs.append(hm)
    body.append(hb)
    body.append(text(tx, 490, "AI ENGINEER  ·  PRODUCT OWNER  ·  CREATIVE TECHNOLOGIST", "san7", 12.5, C["rosary_dim"], tracking=2.6))
    body.append(text(tx, 546, "Discipline in the data.", "seri", 31, C["rosary"]))
    body.append(text(tx, 582, "Honor in the product.", "seri", 31, C["blush"]))

    # ------------------------------------------------------------------ petals in front
    fcss, front = art.falling_petals(u, W, H, 16, seed=9, size=(.7, 1.25), op=(.6, .95), dur=(10, 17), wind=1.3,
                                     area=[(-60, 560), (1090, 1190)])
    css.append(fcss)
    body.append(front)

    # ------------------------------------------------------------------ editorial frame
    body.append(art.crop_marks(W, H, m=20, L=16, op=.55))
    body.append(text(46, 46, "VOL. I", "san8", 10, C["brass"], tracking=4))
    body.append(text(W - 46, 46, "CAIRO  ·  EGYPT  ·  MMXXVI", "san8", 10, C["brass"], tracking=4, anchor="end"))
    body.append(text(W - 46, H - 34, "@Meti-AVP", "mono", 11, C["rosary_dim"], tracking=1.5, anchor="end"))

    defs.append(grain_defs(u, .09))
    body.append(f'<rect width="{W}" height="{H}" fill="url(#{u}grain)"/>')

    svg = doc(W, H, "".join(body), css="".join(css), defs="".join(defs),
              title="Ahmed Zaki Gabr — AI Engineer, Product Owner, Creative Technologist",
              desc="Prologue of a samurai-themed profile: portrait before a blood-red sun circled by an ensō brush stroke, "
                   "a sakura branch, falling petals, and a sword cut that continues into the next panel.")
    return write(os.path.join(out_dir, "00-prologue.svg"), svg)
