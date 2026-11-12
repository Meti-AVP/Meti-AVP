#!/usr/bin/env python3
"""決闘 THE DUEL — a community boss fight played through GitHub issues.

    python game/engine.py play     resolve every open "duel|<move>" issue, re-render, update README
    python game/engine.py reply    comment on + close the issues resolved by `play` (run after the push)
    python game/engine.py render   re-render the HUD and README block from the saved state

Moves: slash, arrow, bloom, tea. Every visitor fights the same yokai; each one defeated
unlocks the next chapter of Ahmed's story. Fall seven times, stand up eight: the builder
always rises again. Only the standard library is needed (plus the `gh` CLI on the runner).
"""
import datetime
import json
import os
import random
import re
import subprocess
import sys
import time
import urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import duel  # noqa: E402
import yokai  # noqa: E402

STATE = os.path.join(ROOT, "game", "state.json")
RESULTS = os.path.join(ROOT, "game", ".results.json")
README = os.path.join(ROOT, "README.md")
HUD_DIR = os.path.join(ROOT, "assets", "duel")
REPO = os.environ.get("REPO", "Meti-AVP/Meti-AVP")
OWNER = REPO.split("/")[0]
TITLE_RE = re.compile(r"^\s*duel\s*\|\s*(slash|arrow|bloom|tea)\s*$", re.I)
MAX_PER_HOUR = 8
KANJI = {"slash": "斬", "arrow": "弓", "bloom": "桜", "tea": "茶"}
NAMES = {"slash": "SLASH", "arrow": "ARROW", "bloom": "BLOOM", "tea": "FOCUS"}


def nice(name):
    small = {"of", "the"}
    return " ".join(w.lower() if i and w.lower() in small else w.capitalize() for i, w in enumerate(name.split()))


# ------------------------------------------------------------------------------ state
def boss_max(chapter, season):
    return int(round(yokai.BOSSES[chapter]["hp"] * (1 + 0.35 * (season - 1))))


def new_state():
    return dict(season=1, chapter=0, boss_hp=boss_max(0, 1), boss_max=boss_max(0, 1), ki=100, ki_max=100,
                focus=False, turn=0, falls=0, last=None, log=[], players={}, slain=[], recent={})


def load():
    if os.path.exists(STATE):
        with open(STATE, encoding="utf-8") as fh:
            return json.load(fh)
    return new_state()


def save(state):
    with open(STATE, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(state, fh, ensure_ascii=False, indent=1)


# ------------------------------------------------------------------------------ rules
def resolve(state, user, action, issue_no):
    rng = random.Random(f"{state['season']}-{state['turn']}-{issue_no}-{user}")
    boss = yokai.BOSSES[state["chapter"]]
    state["turn"] += 1
    p = state["players"].setdefault(user, {"dmg": 0, "moves": 0, "kills": 0, "heal": 0})
    p["moves"] += 1

    dmg, heal, crit = 0, 0, False
    if action == "slash":
        dmg, crit = rng.randint(9, 16), rng.random() < 0.18
    elif action == "arrow":
        dmg, crit = rng.randint(3, 24), rng.random() < 0.28
    elif action == "bloom":
        heal, dmg = rng.randint(14, 24), 3
    else:  # tea
        heal = 6
    if crit:
        dmg *= 2
    focused = False
    if action in ("slash", "arrow") and state["focus"]:
        dmg *= 2
        focused = True
        state["focus"] = False
    if action == "tea":
        state["focus"] = True

    dmg = min(dmg, state["boss_hp"])
    state["boss_hp"] -= dmg
    p["dmg"] += dmg
    if heal:
        real = min(heal, state["ki_max"] - state["ki"])
        state["ki"] += real
        p["heal"] += real
        heal = real

    if action == "slash":
        headline = f"SLASH  ·  {dmg} DAMAGE" + ("  ·  CRITICAL" if crit else "")
        detail = "A clean cut." if not crit else "One flash, one cut. Issen."
    elif action == "arrow":
        headline = f"ARROW  ·  {dmg} DAMAGE" + ("  ·  CRITICAL" if crit else "")
        detail = "The arrow finds its mark." if dmg >= 12 else "The arrow grazes the yokai."
    elif action == "bloom":
        headline = f"BLOOM  ·  +{heal} KI  ·  {dmg} DAMAGE"
        detail = "Petals close the wounds."
    else:
        headline = f"FOCUS  ·  +{heal} KI  ·  NEXT STRIKE ×2"
        detail = "A cup of tea. Breathe. The next strike lands twice."
    if focused:
        detail += " Focus doubled it."

    event = "hit"
    if state["boss_hp"] <= 0:
        event = "slain"
        p["kills"] += 1
        state["slain"].append(dict(season=state["season"], boss=boss["id"], slayer=user, turn=state["turn"],
                                   date=datetime.date.today().isoformat()))
        detail = f"{boss['name']} falls. {boss['defeat']}"
        state["chapter"] += 1
        if state["chapter"] >= len(yokai.BOSSES):
            state["chapter"] = 0
            state["season"] += 1
        state["boss_max"] = boss_max(state["chapter"], state["season"])
        state["boss_hp"] = state["boss_max"]
        state["ki"] = state["ki_max"]
        state["focus"] = False
    else:
        chance = 0.62 if action in ("slash", "arrow") else 0.72
        if rng.random() < chance:
            lo, hi = boss["atk"]
            hit = int(rng.randint(lo, hi) * (1 + 0.2 * (state["season"] - 1)))
            special = state["turn"] % 6 == 0
            if special:
                hit = int(hit * 1.6)
            state["ki"] -= hit
            detail += f" {nice(boss['name'])} strikes back{' with fury' if special else ''}: -{hit} Ki."
            if state["ki"] <= 0:
                event = "fall"
                state["falls"] += 1
                state["ki"] = int(state["ki_max"] * 0.6)
                state["boss_hp"] = min(state["boss_max"], state["boss_hp"] + int(state["boss_max"] * 0.2))
                detail += " Ahmed falls... and rises again."
        else:
            detail += f" {nice(boss['name'])} staggers."

    state["last"] = dict(user=user, action=action, dmg=dmg, heal=heal, crit=crit, headline=headline,
                         detail=detail, issue=issue_no, event=event)
    state["log"] = ([dict(turn=state["turn"], user=user, action=action, dmg=dmg, heal=heal, crit=crit, event=event,
                          boss=boss["id"])] + state["log"])[:8]
    return state["last"], boss


# ------------------------------------------------------------------------------ github
def gh(*args, input_text=None):
    r = subprocess.run(["gh", *args], capture_output=True, text=True, input=input_text)
    if r.returncode != 0:
        raise RuntimeError(f"gh {' '.join(args[:3])} failed: {r.stderr.strip()[:300]}")
    return r.stdout


def open_moves():
    out = gh("issue", "list", "--repo", REPO, "--state", "open", "--limit", "100",
             "--json", "number,title,author,createdAt")
    items = []
    for it in json.loads(out):
        if it["title"].strip().lower().startswith("duel"):
            items.append(it)
    return sorted(items, key=lambda it: (it["createdAt"], it["number"]))


def issue_link(action):
    q = urllib.parse.urlencode({
        "title": f"duel|{action}",
        "body": (f"## 👇 Press the green **Create** button below to strike with {KANJI[action]} {NAMES[action]}\n\n"
                 "That's all: no need to write anything or change the title. The dojo bot resolves your move "
                 "within a minute, replies here, and the duel on the profile updates. 七転び八起き"),
    })
    return f"https://github.com/{REPO}/issues/new?{q}"


# ------------------------------------------------------------------------------ README
def render(state):
    for name in os.listdir(HUD_DIR):
        if name.startswith("hud") and name.endswith(".svg"):
            os.remove(os.path.join(HUD_DIR, name))
    hud_name = f"hud-{state['turn']}.svg"
    with open(os.path.join(HUD_DIR, hud_name), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(duel.hud(state))

    boss = yokai.BOSSES[state["chapter"]]
    lines = [
        "<!-- DUEL:START -->",
        '<p align="center">',
        f'  <img src="assets/duel/arena-{boss["id"]}.svg" width="100%" alt="Ahmed versus {boss["name"]}, chapter {state["chapter"] + 1} of 5"/>',
        f'  <img src="assets/duel/{hud_name}" width="100%" alt="Live status: Ki {state["ki"]}/{state["ki_max"]}, {boss["name"]} HP {state["boss_hp"]}/{state["boss_max"]}"/>',
        "</p>",
        '<p align="center">',
    ]
    for key, _, label, _ in duel.ACTIONS:
        lines.append(f'  <a href="{issue_link(key)}"><img src="assets/duel/act-{key}.svg" width="24%" alt="{label}"/></a>')
    lines += [
        "</p>",
        "",
        f'<p align="center"><b>{boss["kanji"]} · {nice(boss["name"])}</b>: <i>{boss["lore"]}</i><br/>',
        "<sub><b>COMMUNITY DUEL</b> · every visitor fights the same yokai. Pick a move ➜ GitHub opens an issue ➜ "
        "press the green <b>Create</b> button. The bot resolves it within a minute and this screen updates.</sub></p>",
        "",
    ]
    # recent moves + hall of honor side by side
    log_rows = []
    for e in state["log"][:6]:
        what = f'{KANJI[e["action"]]} {NAMES[e["action"]].title()}'
        res = []
        if e.get("dmg"):
            res.append(f'{e["dmg"]} dmg' + (" **一閃**" if e.get("crit") else ""))
        if e.get("heal"):
            res.append(f'+{e["heal"]} Ki')
        if e.get("event") == "slain":
            res.append("**slain!**")
        elif e.get("event") == "fall":
            res.append("fell, rose")
        log_rows.append(f'<tr><td>{e["turn"]}</td><td><a href="https://github.com/{e["user"]}">@{e["user"]}</a></td>'
                        f'<td>{what}</td><td>{", ".join(res) or "—"}</td></tr>')
    if not log_rows:
        log_rows.append('<tr><td colspan="4" align="center"><i>No blood drawn yet. Strike first.</i></td></tr>')
    top = sorted(state["players"].items(), key=lambda kv: (-kv[1]["dmg"], -kv[1]["kills"], kv[0]))[:5]
    hall = []
    for rank, (user, p) in enumerate(top, 1):
        hall.append(f'<tr><td>{"一二三四五"[rank - 1]}</td><td><img src="https://github.com/{user}.png?size=40" width="20" height="20"/> '
                    f'<a href="https://github.com/{user}">@{user}</a></td><td>{p["dmg"]}</td><td>{p["kills"]}</td></tr>')
    if not hall:
        hall.append('<tr><td colspan="4" align="center"><i>The hall is empty. Your name could be first.</i></td></tr>')
    lines += [
        '<table align="center"><tr><td valign="top">',
        "",
        "**Last moves**",
        "",
        "<table><tr><th>Turn</th><th>Fighter</th><th>Move</th><th>Result</th></tr>",
        *log_rows,
        "</table>",
        "",
        '</td><td valign="top">',
        "",
        "**殿堂 · Hall of honor**",
        "",
        "<table><tr><th></th><th>Fighter</th><th>Damage</th><th>Slain</th></tr>",
        *hall,
        "</table>",
        "",
        "</td></tr></table>",
        "",
    ]
    if state["slain"]:
        recent = state["slain"][-5:]
        items = " · ".join(f'{next(b["kanji"] for b in yokai.BOSSES if b["id"] == s["boss"])} by '
                           f'<a href="https://github.com/{s["slayer"]}">@{s["slayer"]}</a>' for s in recent)
        lines.append(f'<p align="center"><sub>Yokai slain: {items}</sub></p>')
    lines.append("<!-- DUEL:END -->")
    block = "\n".join(lines)
    with open(README, encoding="utf-8") as fh:
        text = fh.read()
    new = re.sub(r"<!-- DUEL:START -->.*?<!-- DUEL:END -->", lambda _: block, text, flags=re.S)
    with open(README, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(new)


# ------------------------------------------------------------------------------ commands
def play():
    state = load()
    results = []
    now = time.time()
    recent = {u: [t for t in ts if now - t < 3600] for u, ts in state.get("recent", {}).items()}
    for it in open_moves():
        user = (it.get("author") or {}).get("login") or "ghost"
        m = TITLE_RE.match(it["title"])
        if not m:
            results.append(dict(number=it["number"], ok=False,
                                body=("That move isn't known in this dojo. Use one of the buttons on the profile "
                                      f"(slash, arrow, bloom, tea): https://github.com/{OWNER}")))
            continue
        if len(recent.get(user, [])) >= MAX_PER_HOUR:
            results.append(dict(number=it["number"], ok=False,
                                body=(f"@{user}, your blade needs rest: {MAX_PER_HOUR} moves per hour. "
                                      "Come back soon. The yokai isn't going anywhere.")))
            continue
        action = m.group(1).lower()
        boss_before = yokai.BOSSES[state["chapter"]]
        last, boss = resolve(state, user, action, it["number"])
        recent.setdefault(user, []).append(now)
        results.append(dict(number=it["number"], ok=True, body=reply_body(state, last, boss_before)))
    state["recent"] = recent
    save(state)
    render(state)
    with open(RESULTS, "w", encoding="utf-8") as fh:
        json.dump(results, fh)
    print(f"resolved {sum(r['ok'] for r in results)} move(s), skipped {sum(not r['ok'] for r in results)}")


def reply_body(state, last, boss):
    k = KANJI[last["action"]]
    lines = [f"### {k} {NAMES[last['action']]}" + (" · 一閃 critical" if last["crit"] else ""), "",
             f"**@{last['user']}** · {last['detail']}", ""]
    if last["event"] == "slain":
        lines += [f"**{boss['kanji']} {boss['name']} is slain.** A new chapter of the story opens. 🌸", ""]
    cur = yokai.BOSSES[state["chapter"]]
    lines += ["| Ahmed's Ki | " + f"{cur['kanji']} {nice(cur['name'])} |", "|:-:|:-:|",
              f"| {state['ki']} / {state['ki_max']} | {state['boss_hp']} / {state['boss_max']} |", "",
              f"Back to the duel: https://github.com/{OWNER} · Thanks for fighting alongside me. 七転び八起き"]
    return "\n".join(lines)


def reply():
    if not os.path.exists(RESULTS):
        return
    with open(RESULTS, encoding="utf-8") as fh:
        results = json.load(fh)
    for r in results:
        n = str(r["number"])
        try:
            gh("issue", "comment", n, "--repo", REPO, "--body-file", "-", input_text=r["body"])
            gh("issue", "close", n, "--repo", REPO, "--reason", "completed" if r["ok"] else "not planned")
        except RuntimeError as e:  # keep going: one failed reply must not block the rest
            print(e, file=sys.stderr)
    os.remove(RESULTS)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "render"
    if cmd == "play":
        play()
    elif cmd == "reply":
        reply()
    else:
        s = load()
        save(s)
        render(s)
