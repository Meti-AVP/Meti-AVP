"""陸 THE DUEL — visuals: header panel, one arena per yokai, the live HUD and the move buttons.

The arena (static, one per boss) and the HUD (re-rendered on every move by game/engine.py)
are two leaves of the same screen: the HUD continues the arena's ground.
"""
import os

import art
import yokai
from svgkit import C, data_uri, doc, esc, f, fit_size, grain_defs, kanji, measure, text, write

W = 1200
NUM = "一二三四五"
ACTIONS = [
    ("slash", "斬", "SLASH", "9–16 DMG · 18% CRIT"),
    ("arrow", "弓", "ARROW", "3–24 DMG · 28% CRIT"),
    ("bloom", "桜", "BLOOM", "HEAL 14–24 KI"),
    ("tea", "茶", "FOCUS", "NEXT STRIKE ×2"),
]


# ------------------------------------------------------------------------------- header
def header(out_dir):
    u, H = "dh", 230
    defs, body, css = [], [], []
    defs.append(f'<linearGradient id="{u}bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{C["night"]}"/>'
                f'<stop offset="1" stop-color="#1E0509"/></linearGradient>')
    body.append(f'<rect width="{W}" height="{H}" fill="url(#{u}bg)"/>')
    body.append(kanji("陸", 56, 150, 92, fill=C["blood_hi"], style="brush"))
    body.append(text(172, 112, "THE DUEL", "ser7", 56, C["rosary"], tracking=8))
    body.append(kanji("決闘", 174, 148, 17, fill=C["brass"], style="mincho", gap=.1))
    body.append(text(218, 147, "A BOSS FIGHT FOUGHT BY EVERY VISITOR", "san7", 11.5, C["brass"], tracking=3.4))
    body.append(kanji("七転び八起き", 174, 196, 22, fill=C["rosary"], style="brush", gap=.08))
    body.append(text(340, 194, "Fall seven times, stand up eight.", "seri", 22, C["blush"]))
    kd, k1 = art.katana(u + "k", 900, 96, 300, angle=-24)
    _, k2 = art.katana(u + "k", 900, 150, 300, angle=200)
    defs.append(kd)
    body.append(k1 + k2)
    body.append(text(W - 46, H - 24, "07 / 08", "san8", 10, C["ash"], tracking=4, anchor="end"))
    defs.append(grain_defs(u, .08))
    body.append(f'<rect width="{W}" height="{H}" fill="url(#{u}grain)"/>')
    svg = doc(W, H, "".join(body), css="".join(css), defs="".join(defs), title="陸 The Duel",
              desc="Section header: a community boss fight played through GitHub issues. Fall seven times, stand up eight.")
    return write(os.path.join(out_dir, "duel", "head.svg"), svg)


# ------------------------------------------------------------------------------- arena
def arena(out_dir, i):
    b = yokai.BOSSES[i]
    u, H = "da", 540
    defs, body, css = [], [], []
    defs.append(f'<radialGradient id="{u}bg" cx="72%" cy="45%" r="75%"><stop offset="0" stop-color="#4A0C12"/>'
                f'<stop offset=".5" stop-color="#1A0408"/><stop offset="1" stop-color="{C["night"]}"/></radialGradient>'
                f'<radialGradient id="{u}moon" cx="40%" cy="35%" r="70%"><stop offset="0" stop-color="#FBF3DF"/>'
                f'<stop offset=".7" stop-color="{C["blush"]}"/><stop offset="1" stop-color="{C["blush_deep"]}"/></radialGradient>'
                f'<radialGradient id="{u}rim" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="{C["blood_hi"]}" stop-opacity=".55"/>'
                f'<stop offset="1" stop-color="{C["blood_hi"]}" stop-opacity="0"/></radialGradient>'
                f'<linearGradient id="{u}fade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{C["night"]}" stop-opacity="0"/>'
                f'<stop offset="1" stop-color="{C["night"]}"/></linearGradient>')
    body.append(f'<rect width="{W}" height="{H}" fill="url(#{u}bg)"/>')
    # moon behind the yokai
    body.append(f'<circle cx="880" cy="262" r="212" fill="url(#{u}moon)" fill-opacity=".93"/>')
    body.append("".join(f'<circle cx="880" cy="262" r="{r}" fill="none" stroke="#7A3A3A" stroke-opacity=".08" stroke-width="2"/>' for r in (90, 140, 180)))
    body.append(art.mountains(u, -20, W + 20, H + 10, heights=[150, 90], colors=["#14040A", "#080203"], seed=91, peaks=3.2))
    # the yokai
    bx, by, bs = {"doubt": (880, 352, .8), "drought": (880, 318, .86)}.get(b["id"], (880, 300, .92))
    yd, yg, ycss = yokai.oni(u + "y", b["id"], bx, by, bs)
    defs.append(yd)
    css.append(ycss)
    body.append(yg)
    body.append(kanji(b["kanji"], W - 58, 70, 54, fill=C["blood_hi"], style="brush", vertical=True, gap=.04))
    # the builder (mirrored portrait, facing the yokai)
    defs.append(art.blossom_defs(u))
    bcss, storm = art.falling_petals(u, W, H, 22, seed=195 + i, size=(.5, 1.1), op=(.45, .85), dur=(5, 9), wind=4.2,
                                     area=[(-300, 900)])
    css.append(bcss)
    body.append(storm)
    body.append(f'<ellipse cx="300" cy="300" rx="300" ry="280" fill="url(#{u}rim)"/>')
    S, X, Y = 560, 486, 46
    body.append(f'<image href="{data_uri("portrait.webp")}" x="0" y="0" width="{S}" height="{S}" transform="translate({X} {Y}) scale(-1 1)"/>')
    body.append(f'<rect x="0" y="{H - 150}" width="{W}" height="150" fill="url(#{u}fade)"/>')
    # versus
    body.append(art.ink_splatter(600, 290, 110, 40, seed=93, color="#050102", op=.8))
    sd, sg, scss = art.slash(u + "s", 470, 170, 740, 420, bow=-30, thick=10, period=5.0)
    defs.append(sd)
    css.append(scss)
    body.append(sg)
    body.append(kanji("対", 600, 340, 132, fill=C["rosary"], style="brush", anchor="middle"))
    body.append(kanji(f"第{NUM[i]}章", 600, 70, 22, fill=C["brass"], style="mincho", anchor="middle", gap=.15))
    body.append(text(600, 96, f"CHAPTER {i + 1} OF 5  ·  {b['name']}", "san8", 11, C["rosary_dim"], tracking=3.4, anchor="middle"))
    pcss, petals = art.falling_petals(u + "f", W, H, 9, seed=95 + i, size=(.7, 1.3), op=(.6, .95), dur=(5, 9), wind=2.2,
                                      area=[(560, 1120)])
    css.append(pcss)
    defs.append(f'<path id="{u}fpt" d="{art.PETAL}" transform="translate(0 7)"/>')
    body.append(petals)
    defs.append(grain_defs(u, .09))
    body.append(f'<rect width="{W}" height="{H}" fill="url(#{u}grain)"/>')
    svg = doc(W, H, "".join(body), css="".join(css), defs="".join(defs),
              title=f"The Duel, chapter {i + 1}: {b['name']}",
              desc=f"Ahmed faces {b['name']} ({b['kanji']}) under a pale moon in a storm of sakura petals. {b['lore']}")
    return write(os.path.join(out_dir, "duel", f"arena-{b['id']}.svg"), svg)


# ------------------------------------------------------------------------------- HUD (live)
def _bar(x, y, w, h, frac, u, flip=False):
    frac = max(0.0, min(1.0, frac))
    fw = w * frac
    fx = x + (w - fw if flip else 0)
    return (f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{h}" rx="2" fill="#1A0608" stroke="{C["brass"]}" stroke-opacity=".45"/>'
            f'<rect x="{f(fx)}" y="{f(y)}" width="{f(fw)}" height="{h}" rx="2" fill="url(#{u}{"bb" if flip else "kb"})"/>'
            f'<rect x="{f(fx)}" y="{f(y)}" width="{f(fw)}" height="{h / 2.6:.1f}" rx="2" fill="#fff" fill-opacity=".14"/>'
            + "".join(f'<rect x="{f(x + w * k / 10)}" y="{f(y)}" width="1" height="{h}" fill="#000" fill-opacity=".35"/>' for k in range(1, 10)))


def hud(state, last_html=None):
    """Live HUD under the arena. `state` is the engine state dict."""
    u, H = "dh2", 250
    b = yokai.BOSSES[state["chapter"]]
    defs, body, css = [], [], []
    defs.append(f'<linearGradient id="{u}bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{C["night"]}"/>'
                f'<stop offset="1" stop-color="#140306"/></linearGradient>'
                f'<linearGradient id="{u}kb" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{C["wine"]}"/>'
                f'<stop offset="1" stop-color="{C["ember"]}"/></linearGradient>'
                f'<linearGradient id="{u}bb" x1="1" y1="0" x2="0" y2="0"><stop offset="0" stop-color="#5A4A2A"/>'
                f'<stop offset="1" stop-color="{C["brass_hi"]}"/></linearGradient>')
    body.append(f'<rect width="{W}" height="{H}" fill="url(#{u}bg)"/>')
    # the builder
    body.append(text(60, 46, "AHMED ZAKI", "ser7", 26, C["rosary"], tracking=3))
    body.append(kanji("侍", 60 + measure("AHMED ZAKI", "ser7", 26, 3) + 10, 46, 22, fill=C["blood_hi"], style="brush"))
    body.append(text(60, 64, "THE BUILDER  ·  KI", "san8", 9.5, C["brass"], tracking=3))
    body.append(_bar(60, 74, 430, 16, state["ki"] / state["ki_max"], u))
    body.append(text(490, 64, f"{state['ki']} / {state['ki_max']}", "san8", 11, C["rosary"], tracking=1.5, anchor="end"))
    if state.get("focus"):
        body.append(kanji("茶", 60, 113, 15, fill=C["brass_hi"], style="brush"))
        body.append(text(80, 111, "FOCUSED  ·  NEXT STRIKE ×2", "san8", 9.5, C["brass_hi"], tracking=2.4))
    # the yokai
    body.append(text(W - 60, 46, b["name"], "ser7", 26, C["rosary"], tracking=3, anchor="end"))
    body.append(kanji(b["kanji"], W - 60 - measure(b["name"], "ser7", 26, 3) - 14, 46, 22, fill=C["blood_hi"], style="brush", anchor="end"))
    body.append(text(W - 60, 64, "YOKAI  ·  HP", "san8", 9.5, C["brass"], tracking=3, anchor="end"))
    body.append(_bar(W - 490, 74, 430, 16, state["boss_hp"] / state["boss_max"], u, flip=True))
    body.append(text(W - 490, 64, f"{state['boss_hp']} / {state['boss_max']}", "san8", 11, C["rosary"], tracking=1.5))
    # centre: turn / season
    body.append(kanji("対", 600, 74, 40, fill=C["rosary"], style="brush", anchor="middle", op=.9))
    body.append(text(600, 98, f"TURN {state['turn']}  ·  SEASON {state['season']}", "san8", 9.5, C["rosary_dim"], tracking=2.6, anchor="middle"))
    # last move banner
    last = state.get("last")
    body.append(f'<rect x="60" y="124" width="{W - 120}" height="62" fill="#000" fill-opacity=".35" stroke="{C["blood"]}" stroke-opacity=".5"/>')
    body.append(f'<rect x="60" y="124" width="5" height="62" fill="{C["blood_hi"]}"/>')
    if last:
        kj = {"slash": "斬", "arrow": "弓", "bloom": "桜", "tea": "茶"}[last["action"]]
        body.append(kanji(kj, 92, 168, 34, fill=C["blood_hi"], style="brush", anchor="middle"))
        who = "@" + last["user"]
        body.append(text(124, 152, who, "san8", 15, C["rosary"], tracking=.5))
        body.append(text(124 + measure(who, "san8", 15, .5) + 14, 152, last["headline"], "san7", 13.5, C["brass_hi"], tracking=1.2))
        body.append(text(124, 174, last["detail"], "san5", 12.5, C["rosary_dim"]))
        if last.get("crit"):
            body.append(kanji("一閃", W - 84, 168, 34, fill=C["rosary"], style="brush", anchor="end", gap=.05))
    else:
        body.append(text(92, 162, "THE DUEL AWAITS — STRIKE FIRST.", "san8", 14, C["rosary"], tracking=3))
    # chapter track
    for k in range(5):
        cx = 600 + (k - 2) * 64
        done = k < state["chapter"]
        cur = k == state["chapter"]
        col = C["blood"] if done else (C["brass"] if cur else "#2A1416")
        body.append(f'<circle cx="{cx}" cy="218" r="17" fill="{"#120406" if not done else C["wine"]}" stroke="{col}" stroke-width="{2 if cur else 1.2}"/>')
        body.append(kanji(NUM[k], cx, 225, 17, fill=C["rosary"] if (done or cur) else "#4A3436", style="mincho", anchor="middle"))
        if done:
            body.append(f'<path d="M{cx - 14} 231L{cx + 14} 205" stroke="{C["rosary"]}" stroke-width="2"/>')
        if cur:
            body.append(f'<circle cx="{cx}" cy="218" r="22" fill="none" stroke="{C["brass_hi"]}" stroke-opacity=".6" class="{u}pl"/>')
    css.append(f"@keyframes {u}p{{0%{{transform:scale(.8);opacity:.9}}100%{{transform:scale(1.35);opacity:0}}}}"
               f".{u}pl{{transform-box:fill-box;transform-origin:center;animation:{u}p 1.8s ease-out infinite}}")
    body.append(text(60, 224, f"FALLS {state['falls']}  ·  RISES {state['falls']}", "san8", 9.5, C["ash"], tracking=2.6))
    body.append(text(W - 60, 224, f"YOKAI SLAIN {len(state['slain'])}", "san8", 9.5, C["ash"], tracking=2.6, anchor="end"))
    defs.append(grain_defs(u, .08))
    body.append(f'<rect width="{W}" height="{H}" fill="url(#{u}grain)"/>')
    return doc(W, H, "".join(body), css="".join(css), defs="".join(defs), title="The Duel: live status",
               desc=f"Turn {state['turn']}. Ki {state['ki']}/{state['ki_max']}. {b['name']} HP {state['boss_hp']}/{state['boss_max']}.")


# ------------------------------------------------------------------------------- buttons
def buttons(out_dir):
    out = []
    for key, kj, label, sub in ACTIONS:
        u, w, h = "bt" + key, 285, 96
        defs = (f'<linearGradient id="{u}bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#22080C"/>'
                f'<stop offset="1" stop-color="#0D0305"/></linearGradient>')
        body = (f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="6" fill="url(#{u}bg)" stroke="{C["brass"]}" stroke-opacity=".6"/>'
                f'<rect x="7" y="7" width="{w - 14}" height="{h - 14}" rx="3" fill="none" stroke="{C["blood"]}" stroke-opacity=".6"/>'
                f'<rect x="7" y="7" width="74" height="{h - 14}" rx="3" fill="{C["blood"]}"/>'
                + kanji(kj, 44, 66, 46, fill=C["rosary"], style="brush", anchor="middle")
                + text(100, 50, label, "ser7", 28, C["rosary"], tracking=4)
                + text(100, 72, sub, "san8", 9.5, C["brass"], tracking=1.8)
                + f'<path d="M{w - 34} 40l10 8-10 8" fill="none" stroke="{C["brass_hi"]}" stroke-width="2"/>')
        svg = doc(w, h, body, defs=defs, title=f"{label}: open an issue to play", desc=f"{label} — {sub}")
        out.append(write(os.path.join(out_dir, "duel", f"act-{key}.svg"), svg))
    return out


# ------------------------------------------------------------------------------ instant-play plate
def play_plate(out_dir):
    u, w, h = "pl", 1200, 128
    defs = (f'<linearGradient id="{u}bg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8E0A11"/>'
            f'<stop offset=".6" stop-color="#5A060B"/><stop offset="1" stop-color="#2A0306"/></linearGradient>'
            + art.blossom_defs(u) + grain_defs(u, .1))
    pcss, petals = art.falling_petals(u, w, h, 9, seed=501, size=(.45, .8), op=(.5, .85), dur=(5, 8), wind=3)
    body = (f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="6" fill="url(#{u}bg)" stroke="{C["brass"]}" stroke-opacity=".7"/>'
            f'<rect x="8" y="8" width="{w - 16}" height="{h - 16}" rx="3" fill="none" stroke="{C["rosary"]}" stroke-opacity=".18"/>'
            + kanji("居合", 44, 92, 62, fill=C["rosary"], style="brush", gap=.02)
            + f'<rect x="188" y="30" width="1" height="68" fill="{C["rosary"]}" fill-opacity=".3"/>'
            + text(214, 66, "PLAY THE QUICK-DRAW", "ser7", 36, C["rosary"], tracking=6)
            + text(216, 92, "ONE CLICK  ·  IN YOUR BROWSER  ·  FIVE YOKAI FROM A REAL CAREER", "san8", 11, C["brass_hi"], tracking=3)
            + petals
            + f'<circle cx="{w - 92}" cy="{h / 2}" r="34" fill="none" stroke="{C["rosary"]}" stroke-width="2"/>'
            + f'<circle cx="{w - 92}" cy="{h / 2}" r="42" fill="none" stroke="{C["rosary"]}" stroke-opacity=".35" class="{u}pu"/>'
            + f'<path d="M{w - 102} {h / 2 - 16}L{w - 74} {h / 2}L{w - 102} {h / 2 + 16}Z" fill="{C["rosary"]}"/>'
            + text(w - 150, h / 2 + 6, "PLAY", "san8", 13, C["rosary"], tracking=4, anchor="end")
            + f'<rect width="{w}" height="{h}" fill="url(#{u}grain)"/>')
    css = (pcss + f"@keyframes {u}p{{0%{{transform:scale(.85);opacity:.9}}100%{{transform:scale(1.25);opacity:0}}}}"
           f".{u}pu{{transform-box:fill-box;transform-origin:center;animation:{u}p 1.8s ease-out infinite}}")
    svg = doc(w, h, body, css=css, defs=defs, title="Play the quick-draw duel instantly",
              desc="Opens a browser game: wait for the brush mark, then strike first. Five yokai from a real career.")
    return write(os.path.join(out_dir, "duel", "play.svg"), svg)


def build(out_dir):
    sizes = [header(out_dir)] + [arena(out_dir, i) for i in range(5)] + buttons(out_dir) + [play_plate(out_dir)]
    return sizes
