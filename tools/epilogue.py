"""終 EPILOGUE — sunset, a haiku, the seal."""
import os

import art
from svgkit import C, doc, grain_defs, kanji, text, write

W, H = 1200, 440


def build(out_dir):
    u = "ep"
    defs, body, css = [], [], []
    defs.append(f'<linearGradient id="{u}sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{C["night"]}"/>'
                f'<stop offset=".7" stop-color="#2A060B"/><stop offset="1" stop-color="#4A0A10"/></linearGradient>')
    body.append(f'<rect width="{W}" height="{H}" fill="url(#{u}sky)"/>')
    defs.append(art.sun_defs(u))
    body.append(art.sun(u, 860, 360, 170))
    body.append(art.mountains(u, -20, W + 20, H + 40, heights=[170, 120, 70], colors=["#2A070C", "#14030A", "#060102"], seed=111, peaks=2.8))
    defs.append(art.blossom_defs(u))
    body.append(art.sakura_branch(u, 1236, 30, 172, 330, 17, seed=113, depth=2, bloom=.95, scale=.92, color="#2E0D10"))

    body.append(kanji("終", 76, 210, 120, fill=C["blood_hi"], style="brush"))
    for i, line in enumerate(("Petals fall on code,", "the desert learns to bloom green,", "one more blade is forged.")):
        body.append(text(238, 150 + i * 44, line, "seri", 34, C["rosary"] if i != 1 else C["blush"]))
    body.append(f'<rect x="240" y="294" width="60" height="1" fill="{C["brass"]}" fill-opacity=".6"/>')
    body.append(text(240, 322, "THANK YOU FOR WALKING THE PATH", "san8", 11.5, C["brass"], tracking=3.6))
    body.append(text(240, 346, "Ahmed Zaki Gabr  ·  Cairo, Egypt", "ser6", 18, C["rosary_dim"]))
    m, seal = art.hanko(u, 588, 330, 54, rot=-7, seed=7)
    defs.append(m)
    body.append(seal)

    pcss, petals = art.falling_petals(u, W, H, 16, seed=117, size=(.6, 1.15), op=(.55, .95), dur=(9, 15), wind=1.6)
    css.append(pcss)
    body.append(petals)
    body.append(text(W - 46, H - 26, "08 / 08", "san8", 10, C["ash"], tracking=4, anchor="end"))
    body.append(art.crop_marks(W, H, m=20, L=16, op=.45))
    defs.append(grain_defs(u, .09))
    body.append(f'<rect width="{W}" height="{H}" fill="url(#{u}grain)"/>')
    svg = doc(W, H, "".join(body), css="".join(css), defs="".join(defs), title="終 Epilogue",
              desc="A haiku over a setting red sun: Petals fall on code, the desert learns to bloom green, one more blade is forged.")
    return write(os.path.join(out_dir, "09-epilogue.svg"), svg)
