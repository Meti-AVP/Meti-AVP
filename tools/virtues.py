"""壱 THE CODE — the seven virtues of bushidō as nobori banners, each earned on the CV."""
import os

import art
import scene
from svgkit import C, doc, f, grain_defs, kanji, text, wrap, write

W, H = 1200, scene.HEIGHT["virtues"]

VIRTUES = [
    ("義", "GI", "RECTITUDE", "Labeling to QC Specialist in two months, across three AV pipelines."),
    ("勇", "YŪ", "COURAGE", "Pitched Green Vision to ministers, investors and the EU Ambassador."),
    ("仁", "JIN", "BENEVOLENCE", "Builds AI that forecasts drought so the land can heal."),
    ("礼", "REI", "RESPECT", "A team player first, a team leader when it counts."),
    ("誠", "MAKOTO", "HONESTY", "PRDs and acceptance criteria that say exactly what ships."),
    ("名誉", "MEIYO", "HONOR", "Five honors: NASA, the EU, IEEE, MCIT and the Ministry."),
    ("忠義", "CHŪGI", "LOYALTY", "Owns the product from the first MVP to the production release."),
]
NUMS = "一二三四五六七"


def build(out_dir):
    u = "vc"
    defs, body, css = [], [], []
    defs.append(f'<radialGradient id="{u}bg" cx="50%" cy="0%" r="90%"><stop offset="0" stop-color="#22070B"/>'
                f'<stop offset=".6" stop-color="#0D0305"/><stop offset="1" stop-color="{C["night"]}"/></radialGradient>'
                f'<linearGradient id="{u}fold" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#000" stop-opacity=".38"/>'
                f'<stop offset=".22" stop-color="#fff" stop-opacity=".05"/><stop offset=".55" stop-color="#000" stop-opacity="0"/>'
                f'<stop offset=".8" stop-color="#fff" stop-opacity=".04"/><stop offset="1" stop-color="#000" stop-opacity=".42"/></linearGradient>'
                f'<linearGradient id="{u}shade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".06"/>'
                f'<stop offset=".5" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".35"/></linearGradient>')
    body.append(f'<rect width="{W}" height="{H}" fill="url(#{u}bg)"/>')

    # far peaks of the range that becomes chapter two
    body.append(scene.ridges("virtues", u, layers=[0]))

    # the cut arriving from the prologue
    sd, sg, scss = scene.slash("virtues", u + "s")
    defs.append(sd)
    css.append(scss)
    body.append(sg)
    body.append(art.ink_splatter(1030, 132, 60, 22, seed=17, color=C["blood"], op=.7, angle=14))

    # heading
    body.append(kanji("壱", 56, 152, 96, fill=C["blood_hi"], style="brush"))
    body.append(text(172, 116, "THE CODE", "ser7", 56, C["rosary"], tracking=8))
    body.append(kanji("武士道", 174, 152, 17, fill=C["brass"], style="mincho", gap=.12))
    body.append(text(244, 151, "SEVEN VIRTUES OF THE WARRIOR, LIVED BY A BUILDER", "san7", 11.5, C["brass"], tracking=3.4))
    body.append(text(W - 46, H - 30, "02 / 08", "san8", 10, C["ash"], tracking=4, anchor="end"))

    # banners
    defs.append(art.blossom_defs(u))
    bw, gap, x0, top = 142, 15, 56, 206
    fab_h = 404
    css.append(f"@keyframes {u}sw{{0%{{transform:rotate(-.9deg)}}100%{{transform:rotate(.9deg)}}}}")
    for i, (kj, romaji, eng, desc) in enumerate(VIRTUES):
        x = x0 + i * (bw + gap)
        red = i % 2 == 0
        fab = C["blood"] if red else "#14050A"
        kcol = C["rosary"] if red else C["blood_hi"]
        tcol = C["rosary"] if red else C["rosary_dim"]
        ecol = C["rosary"] if red else C["brass"]
        cx = x + 5 + (bw - 5) / 2
        g = [f'<g style="transform-origin:{x}px {top - 6}px;animation:{u}sw {f(6.2 + i * .45)}s ease-in-out {f(-i * 1.1)}s infinite alternate">']
        g.append(f'<rect x="{x - 1.5}" y="{top - 14}" width="3" height="{fab_h + 60}" fill="{C["brass_lo"]}"/>')
        g.append(f'<rect x="{x - 1.5}" y="{top - 4}" width="{bw + 4}" height="3" rx="1.5" fill="{C["brass"]}"/>')
        g.append(f'<circle cx="{x}" cy="{top - 16}" r="3.6" fill="{C["brass"]}"/>')
        g.append(f'<rect x="{x + 5}" y="{top}" width="{bw - 5}" height="{fab_h}" fill="{fab}"/>')
        if not red:
            g.append(f'<rect x="{x + 5.5}" y="{top + .5}" width="{bw - 6}" height="{fab_h - 1}" fill="none" stroke="{C["blood"]}" stroke-opacity=".55"/>')
        g.append(f'<rect x="{x + 5}" y="{top}" width="{bw - 5}" height="{fab_h}" fill="url(#{u}fold)"/>')
        g.append(f'<rect x="{x + 5}" y="{top}" width="{bw - 5}" height="{fab_h}" fill="url(#{u}shade)"/>')
        for k in range(7):
            g.append(f'<circle cx="{x + 3}" cy="{top + 26 + k * 58}" r="3.4" fill="none" stroke="{C["brass"]}" stroke-width="1.4"/>')
        # glyphs
        if len(kj) == 1:
            g.append(kanji(kj, cx, 316, 76, fill=kcol, style="brush", anchor="middle"))
        else:
            g.append(kanji(kj, cx, 222, 56, fill=kcol, style="brush", vertical=True, gap=.02))
        g.append(text(cx, 390, romaji, "ser7", 25, tcol, tracking=2, anchor="middle"))
        g.append(text(cx, 410, eng, "san8", 10, ecol, tracking=2.6, anchor="middle", op=.85))
        g.append(f'<rect x="{f(cx - 22)}" y="424" width="44" height="1" fill="{tcol}" fill-opacity=".35"/>')
        for j, line in enumerate(wrap(desc, "san5", 13.2, bw - 26)):
            g.append(text(cx, 450 + j * 19, line, "san5", 13.2, tcol, anchor="middle", op=.92))
        g.append(kanji(NUMS[i], cx, top + fab_h - 18, 17, fill=tcol, style="mincho", anchor="middle", op=.5))
        g.append("</g>")
        body.append("".join(g))

    pcss, petals = art.falling_petals(u, W, H, 14, seed=33, size=(.6, 1.1), op=(.55, .9), dur=(11, 18), wind=1.2)
    css.append(pcss)
    body.append(petals)
    body.append(art.crop_marks(W, H, m=20, L=16, op=.45))
    defs.append(grain_defs(u, .08))
    body.append(f'<rect width="{W}" height="{H}" fill="url(#{u}grain)"/>')
    svg = doc(W, H, "".join(body), css="".join(css), defs="".join(defs),
              title="壱 The Code: seven virtues of bushidō",
              desc="Seven swaying nobori banners: rectitude, courage, benevolence, respect, honesty, honor and loyalty, "
                   "each tied to a real step in Ahmed's career.")
    return write(os.path.join(out_dir, "01-code.svg"), svg)
