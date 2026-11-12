"""参 THE BLADES — projects as title cards, paired into diptychs whose art runs across the hinge.

Edit PROJECTS to change what is featured; every pair shares one continuous motif.
"""
import os

import art
import scene
from svgkit import C, doc, f, fit_size, grain_defs, kanji, measure, text, wrap, write

W = 1200
CW, CH, HINGE = 596, 420, 8   # card size; two cards + hinge = 1200
SUN_X, SUN_DY, SUN_R = 930, 36, 168  # sun centred just below the header's bottom edge

# The featured blade, full width, right under the section header.
FEATURED = dict(
    kanji="智", title="SYRA ONE", cat="AI · HUMAN CAPABILITY PLATFORM",
    tagline="Intelligence that proposes, people who decide: learning, assessment, talent and work on one "
            "evidence layer, with ten AI agents that cite their sources.",
    stack="AI agents · Evidence layer · Role copilots · Interactive prototype",
    label="syra-one-app.vercel.app", url="https://syra-one-app.vercel.app",
    roles=[("HEAD OF HR", "SYRA Command"), ("DIRECTOR · SPONSOR", "SYRA Briefing"),
           ("SENIOR EXPERT", "SYRA ECHO"), ("LINE MANAGER", "Manager Copilot")],
)

# (kanji, title, category, tagline, stack, link label, url) — read in pairs, left then right
PROJECTS = [
    ("健", "WORKFIT HUB", "OCCUPATIONAL HEALTH · GUIDED JOURNEY",
     "Fitness for work, measured, not assumed: a health declaration, five camera-based assessments and a physician's decision.",
     "Nine checkpoints · Camera assessments · Physician review", "meti-avp.vercel.app", "https://meti-avp.vercel.app"),
    ("美", "RAPHAEL STUDIOS", "AGENCY · EDITORIAL & CINEMATIC",
     "An agency for what comes next: the cinematic home of a Cairo studio trusted by 55+ brands since 2011.",
     "Astro · GSAP · Lenis · WebGL2", "raphael-studios-v5.vercel.app", "https://raphael-studios-v5.vercel.app"),
    ("学", "SYRA", "ENTERPRISE LEARNING MANAGEMENT",
     "Learning infrastructure for organizations that mean it: multi-tenant, SCORM & xAPI, live rooms, AI analytics, SSO.",
     "Multi-tenant · RBAC · SCORM / xAPI · AI analytics", "syra-lms-tau.vercel.app", "https://syra-lms-tau.vercel.app"),
    ("知", "SYRA LMS", "STRUCTURED LEARNING",
     "One platform to run training: learning paths with prerequisites, grading, certifications and renewals across branches.",
     "Learning paths · Certifications · Live sessions · Reports", "syra-local.vercel.app", "https://syra-local.vercel.app"),
    ("映", "SITUATIONAL SYRA", "SCENARIO FILMS FOR LEARNING",
     "Workplace situations, streamed like cinema: a browse-and-watch library of scenario films.",
     "Streaming UI · Scenario library · Learning by situation", "syra-situ-videos.vercel.app", "https://syra-situ-videos.vercel.app/browse"),
    ("問", "THE PITCH", "SYRA ONE · STORY-DRIVEN PITCH",
     "Who would you hate to lose? A swipe-through storyboard on where capability leaks: when people leave, join or move up.",
     "Storyboard · Scroll & swipe narrative", "syra-pitch.vercel.app", "https://syra-pitch.vercel.app"),
]
MOTIFS = ["katana", "sun", "brush"]


# ------------------------------------------------------------------------------ header
def header(out_dir):
    u, H = "bh", scene.HEIGHT["blades"]
    defs, body = [], []
    defs.append(f'<linearGradient id="{u}bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0D0305"/>'
                f'<stop offset="1" stop-color="{C["night"]}"/></linearGradient>')
    body.append(f'<rect width="{W}" height="{H}" fill="url(#{u}bg)"/>')
    defs.append(art.sun_defs(u))
    body.append(art.sun(u, SUN_X, H + SUN_DY, SUN_R, glow=True))
    body.append(kanji("参", 56, 150, 92, fill=C["blood_hi"], style="brush"))
    body.append(text(172, 112, "THE BLADES", "ser7", 56, C["rosary"], tracking=8))
    body.append(kanji("名刀", 174, 148, 17, fill=C["brass"], style="mincho", gap=.1))
    body.append(text(218, 147, "SEVEN BLADES, FORGED AND SHIPPED. EACH CARD OPENS THE LIVE WORK.", "san7", 11.5, C["brass"], tracking=3))
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
    else:  # "brush": one sumi stroke dragged across both screens
        import math
        pts = [(40 + i * 11.2, 78 - 26 * math.sin(i / 100 * math.pi) + 6 * math.sin(i / 9)) for i in range(101)]
        body = art.brush_stroke(pts, 30, seed=221, tail=.3, bristles=9, w_end=.5, start_blob=1.5)
        streaks = art.brush_streaks(pts, 30, seed=221, n=12, t0=.15)
        g.append(f'<path d="{body}" fill="{C["blood"]}" fill-opacity=".92"/>'
                 f'<path d="{streaks}" fill="none" stroke="{C["night"]}" stroke-opacity=".55" stroke-width="1.4" stroke-linecap="round"/>')
    return "".join(defs), "".join(g)


# ------------------------------------------------------------------------------ featured blade
def featured(out_dir):
    u, H = "bf", 470
    F = FEATURED
    defs, body, css = [], [], []
    defs.append(f'<radialGradient id="{u}bg" cx="22%" cy="60%" r="90%"><stop offset="0" stop-color="#25070B"/>'
                f'<stop offset="1" stop-color="{C["night"]}"/></radialGradient>')
    body.append(f'<rect width="{W}" height="{H}" fill="url(#{u}bg)"/>')
    defs.append(art.sun_defs(u))
    body.append(art.sun(u, SUN_X, SUN_DY, SUN_R, glow=True))  # the sun rising out of the header above
    body.append(kanji(F["kanji"], 46, 336, 236, fill=C["blood_hi"], style="brush", op=.96))
    body.append(text(52, 398, "01", "ser7", 24, C["brass_hi"], tracking=2))
    body.append(f'<rect x="92" y="390" width="120" height="1" fill="{C["brass"]}" fill-opacity=".5"/>')
    body.append(text(96, 384, "FEATURED", "san8", 9.5, C["brass"], tracking=3))
    tx, tw = 326, 450
    body.append(text(tx, 150, F["cat"], "san8", 10.5, C["brass"], tracking=3))
    body.append(text(tx - 4, 232, F["title"], "ser7", fit_size(F["title"], "ser7", tw, 96, 12), C["rosary"], tracking=12))
    for j, line in enumerate(wrap(F["tagline"], "seri", 22, tw)[:3]):
        body.append(text(tx, 274 + j * 28, line, "seri", 22, C["blush"]))
    body.append(text(tx, 372, F["stack"], "san7", fit_size(F["stack"], "san7", tw, 11.5, 1.2), C["rosary_dim"], tracking=1.2))
    lab = "LIVE  ↗"
    lw = measure(lab, "san8", 11.5, 3) + 20
    body.append(f'<rect x="{tx}" y="392" width="{f(lw)}" height="28" fill="{C["blood"]}"/>')
    body.append(text(tx + 10, 411, lab, "san8", 11.5, C["rosary"], tracking=3))
    body.append(text(tx + lw + 12, 412, F["label"], "mono", 13, C["brass_hi"]))
    rx = 818
    body.append(text(rx, 252, "EVERY ROLE MEETS ITS OWN ASSISTANT", "san8", 9.8, C["brass"], tracking=2.2))
    body.append(f'<rect x="{rx}" y="262" width="330" height="1" fill="{C["brass"]}" fill-opacity=".3"/>')
    for i, (role, agent) in enumerate(F["roles"]):
        y = 292 + i * 42
        body.append(f'<path d="M{rx + 4} {y - 9}l5 5-5 5-5-5z" fill="{C["blood_hi"]}"/>')
        body.append(text(rx + 20, y - 5, role, "san8", 10, C["rosary_dim"], tracking=2))
        body.append(text(rx + 20, y + 16, agent, "seri", 19, C["rosary"]))
    d = []
    m, L = 18, 14
    for (x, y, sx, sy) in ((m, m, 1, 1), (W - m, m, -1, 1), (m, H - m, 1, -1), (W - m, H - m, -1, -1)):
        d.append(f"M{f(x - sx * 6)} {f(y)}h{f(sx * (L + 6))}M{f(x)} {f(y - sy * 6)}v{f(sy * (L + 6))}")
    body.append(f'<path d="{"".join(d)}" stroke="{C["brass"]}" stroke-opacity=".45" fill="none"/>')
    defs.append(art.blossom_defs(u))
    pcss, petals = art.falling_petals(u, W, H, 10, seed=401, size=(.6, 1.1), op=(.5, .9), dur=(10, 16), wind=1.3,
                                      area=[(-60, 300), (780, 1180)])
    css.append(pcss)
    body.append(petals)
    defs.append(grain_defs(u, .08))
    body.append(f'<rect width="{W}" height="{H}" fill="url(#{u}grain)"/>')
    svg = doc(W, H, "".join(body), css="".join(css), defs="".join(defs), title=f"{F['title']}: {F['cat'].title()}",
              desc=f"Featured project. {F['tagline']} Opens {F['label']}.")
    return write(os.path.join(out_dir, "blades", "featured.svg"), svg)


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
    body.append(text(44, 352, f"{idx + 2:02d}", "ser7", 22, C["brass_hi"], tracking=2))
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
    return write(os.path.join(out_dir, "blades", f"p{row + 1}-{side and 'r' or 'l'}.svg"), svg)


def build(out_dir):
    return [header(out_dir), featured(out_dir)] + [card(out_dir, i) for i in range(len(PROJECTS))]
