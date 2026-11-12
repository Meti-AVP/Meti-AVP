"""伍 ARSENAL — skills as a dojo name-plate board (nafuda-kake) under a katana rack."""
import os

import art
from svgkit import C, doc, f, fit_size, grain_defs, kanji, text, write

W, H = 1200, 650

SCHOOLS = [
    ("AI & DATA", ["Python*", "Machine Learning*", "Deep Learning", "SQL", "Data Analysis*", "Excel",
                   "LiDAR / Image QC*", "Data Labeling", "OR-Tools", "Ollama · LLMs"]),
    ("ENGINEERING", ["TypeScript*", "React*", "Three.js / WebGL*", "GSAP", "Astro", "Vite", "FastAPI*", "Docker",
                     "Supabase", "HTML & CSS", "Java · C", "DS & Algorithms"]),
    ("PRODUCT", ["Product Ownership*", "PRDs*", "User Stories", "Acceptance Criteria", "Prioritization",
                 "Stakeholders", "Team Leadership*", "Project Mgmt"]),
    ("CREATIVE", ["Unreal Engine 5*", "Blender", "Motion Design*", "Photoshop", "Illustrator", "Premiere Pro",
                  "Filmora", "Creative Design"]),
]


def build(out_dir):
    u = "ar"
    defs, body, css = [], [], []
    defs.append(f'<radialGradient id="{u}bg" cx="30%" cy="0%" r="95%"><stop offset="0" stop-color="#22070B"/>'
                f'<stop offset=".6" stop-color="#0D0305"/><stop offset="1" stop-color="{C["night"]}"/></radialGradient>'
                f'<linearGradient id="{u}wood" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1F0B0C"/>'
                f'<stop offset="1" stop-color="#110506"/></linearGradient>'
                f'<linearGradient id="{u}tag" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2E1314"/>'
                f'<stop offset="1" stop-color="#1C0A0B"/></linearGradient>'
                f'<linearGradient id="{u}tagr" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{C["blood_hi"]}"/>'
                f'<stop offset="1" stop-color="{C["blood"]}"/></linearGradient>'
                f'<linearGradient id="{u}lac" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#050102"/>'
                f'<stop offset=".5" stop-color="#1E0709"/><stop offset="1" stop-color="#050102"/></linearGradient>')
    body.append(f'<rect width="{W}" height="{H}" fill="url(#{u}bg)"/>')

    body.append(kanji("伍", 56, 150, 92, fill=C["blood_hi"], style="brush"))
    body.append(text(172, 112, "ARSENAL", "ser7", 56, C["rosary"], tracking=8))
    body.append(kanji("武器", 174, 148, 17, fill=C["brass"], style="mincho", gap=.1))
    body.append(text(218, 147, "THE SCHOOLS I FIGHT WITH", "san7", 11.5, C["brass"], tracking=3.4))

    # katana rack (katana-kake)
    for px in (712, 1112):
        body.append(f'<path d="M{px - 9} 186L{px - 6} 66C{px - 6} 58 {px + 6} 58 {px + 6} 66L{px + 9} 186Z" fill="url(#{u}lac)"/>')
        for yy in (92, 134):
            body.append(f'<path d="M{px - 14} {yy + 6}C{px - 14} {yy - 8} {px + 14} {yy - 8} {px + 14} {yy + 6}Z" fill="#0B0304" stroke="{C["brass"]}" stroke-opacity=".6"/>')
        body.append(f'<rect x="{px - 12}" y="184" width="24" height="5" rx="2" fill="{C["brass"]}"/>')
    kd, k1 = art.katana(u + "k", 806, 86, 330, angle=-1.2)
    _, k2 = art.katana(u + "k", 846, 128, 262, angle=-.8)
    defs.append(kd)
    body.append(k1 + k2)

    # the board
    bx, by, bw, bh = 56, 214, W - 112, 396
    body.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="6" fill="url(#{u}wood)" stroke="{C["brass"]}" stroke-opacity=".55" stroke-width="1.5"/>')
    body.append(f'<rect x="{bx + 8}" y="{by + 8}" width="{bw - 16}" height="{bh - 16}" rx="3" fill="none" stroke="{C["brass"]}" stroke-opacity=".18"/>')
    for k in range(1, 12):
        body.append(f'<rect x="{bx + 10}" y="{by + k * 33}" width="{bw - 20}" height="1" fill="#000" fill-opacity=".22"/>')

    col_gap = 14
    cw = (bw - 32 - 3 * col_gap) / 4
    css.append(f"@keyframes {u}sw{{0%{{transform:rotate(-1.4deg)}}100%{{transform:rotate(1.4deg)}}}}")
    n = 0
    for ci, (school, skills) in enumerate(SCHOOLS):
        cx0 = bx + 16 + ci * (cw + col_gap)
        # school header plaque
        body.append(f'<rect x="{f(cx0)}" y="{by + 18}" width="{f(cw)}" height="44" rx="3" fill="url(#{u}tagr)"/>')
        body.append(f'<rect x="{f(cx0 + 3)}" y="{by + 21}" width="{f(cw - 6)}" height="38" rx="2" fill="none" stroke="{C["rosary"]}" stroke-opacity=".35"/>')
        body.append(text(cx0 + 16, by + 47, school, "ser7", 19, C["rosary"], tracking=2.4))
        body.append(kanji("流", cx0 + cw - 16, by + 52, 26, fill=C["rosary"], style="brush", anchor="end"))
        tw = (cw - 10) / 2
        for si, sk in enumerate(skills):
            star = sk.endswith("*")
            name = sk.rstrip("*")
            col, row = si % 2, si // 2
            tx = cx0 + col * (tw + 10)
            ty = by + 82 + row * 50
            pivot_x = tx + tw / 2
            fs = fit_size(name, "san7", tw - 14, 12.5)
            body.append(
                f'<g style="transform-origin:{f(pivot_x)}px {f(ty)}px;animation:{u}sw {f(3.8 + (n % 5) * .5)}s ease-in-out {f(-(n * .7) % 4)}s infinite alternate">'
                f'<path d="M{f(pivot_x)} {f(ty - 6)}L{f(tx + 10)} {f(ty + 4)}M{f(pivot_x)} {f(ty - 6)}L{f(tx + tw - 10)} {f(ty + 4)}" stroke="{C["brass"]}" stroke-opacity=".45"/>'
                f'<rect x="{f(tx)}" y="{f(ty + 3)}" width="{f(tw)}" height="34" rx="3" fill="url(#{u}{"tagr" if star else "tag"})" '
                f'stroke="{C["brass"] if not star else C["rosary"]}" stroke-opacity="{".35" if not star else ".3"}"/>'
                f'<circle cx="{f(pivot_x)}" cy="{f(ty - 6)}" r="2.6" fill="{C["brass_hi"]}"/>'
                + text(pivot_x, ty + 24.5, name, "san7", fs, C["rosary"], anchor="middle", op=1 if star else .9)
                + "</g>")
            n += 1

    body.append(text(bx + 18, by + bh + 26, "RED PLATES  ·  SIGNATURE TECHNIQUES", "san8", 9.5, C["brass"], tracking=3, op=.8))
    defs.append(art.blossom_defs(u))
    pcss, petals = art.falling_petals(u, W, H, 12, seed=81, size=(.55, 1.0), op=(.5, .85), dur=(12, 19), wind=1.3)
    css.append(pcss)
    body.append(petals)
    body.append(text(W - 46, H - 30, "06 / 08", "san8", 10, C["ash"], tracking=4, anchor="end"))
    body.append(art.crop_marks(W, H, m=20, L=16, op=.45))
    defs.append(grain_defs(u, .08))
    body.append(f'<rect width="{W}" height="{H}" fill="url(#{u}grain)"/>')
    svg = doc(W, H, "".join(body), css="".join(css), defs="".join(defs),
              title="伍 Arsenal: skills",
              desc="A dojo name-plate board with four schools (AI & Data, Engineering, Product, Creative) and the skills of each; "
                   "a rack with two katanas above it.")
    return write(os.path.join(out_dir, "05-arsenal.svg"), svg)
