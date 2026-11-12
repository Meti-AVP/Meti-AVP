"""Design system for every SVG on the profile — 道 THE WAY OF THE BUILDER.

Palette  "gothic romance": blood red + black lead; damask / rose for depth, gold brass for
         metal, rosary cream for type and petals.
Type     Cormorant Garamond (titles), Manrope (UI), JetBrains Mono (data). Japanese is drawn
         from pre-extracted glyph outlines (brush: Yuji Syuku, crisp: Shippori Mincho), so no
         CJK font is ever embedded and every SVG renders the same everywhere GitHub shows it.
Only the standard library is needed at render time (the GitHub Actions use this module too);
fontTools, when present, subsets the embedded Latin fonts to each file's characters.
"""
import base64
import html
import io
import json
import math
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "fonts")
DATA_DIR = os.path.join(HERE, "data")

C = dict(
    ink="#010000", night="#070304", coal="#0E0708", damask="#220B11", rose="#430102",
    wine="#5E070C", blood="#9F0A10", blood_hi="#C8141C", ember="#E0262C",
    brass="#C0914F", brass_hi="#E2BC7E", brass_lo="#7C5A2C",
    rosary="#EBE0C2", rosary_dim="#B9AE95", ash="#7D7268", smoke="#3A2F2E",
    blush="#E8C7BC", blush_deep="#C98A86",
)

FONTS = {  # alias -> (css family, file, fallback stack)
    "ser6": ("ZSerif6", "serif-600.woff", "'Cormorant Garamond',Garamond,'Times New Roman',serif"),
    "ser7": ("ZSerif7", "serif-700.woff", "'Cormorant Garamond',Garamond,'Times New Roman',serif"),
    "seri": ("ZSerifI", "serif-600i.woff", "'Cormorant Garamond',Garamond,'Times New Roman',serif"),
    "san5": ("ZSans5", "sans-500.woff", "Manrope,'Segoe UI',Ubuntu,Helvetica,Arial,sans-serif"),
    "san7": ("ZSans7", "sans-700.woff", "Manrope,'Segoe UI',Ubuntu,Helvetica,Arial,sans-serif"),
    "san8": ("ZSans8", "sans-800.woff", "Manrope,'Segoe UI',Ubuntu,Helvetica,Arial,sans-serif"),
    "mono": ("ZMono5", "mono-500.woff", "'JetBrains Mono',Consolas,'Courier New',monospace"),
    "mono7": ("ZMono7", "mono-700.woff", "'JetBrains Mono',Consolas,'Courier New',monospace"),
}

try:  # optional, build-time only
    from fontTools.ttLib import TTFont
    from fontTools import subset as _subset
except Exception:  # pragma: no cover
    TTFont = None
    _subset = None


# ----------------------------------------------------------------------------- numbers / text
def f(x, nd=1):
    s = f"{x:.{nd}f}".rstrip("0").rstrip(".")
    if s in ("-0", ""):
        return "0"
    if s.startswith("0.") and len(s) > 2:
        s = s[1:]
    elif s.startswith("-0.") and len(s) > 3:
        s = "-" + s[2:]
    return s


def esc(t):
    return html.escape(str(t), quote=True)


def rad(d):
    return d * math.pi / 180.0


def seeded(seed):
    """xorshift32 — deterministic art without touching the global `random` state."""
    s = [(seed * 2654435761) & 0xFFFFFFFF or 1]

    def r():
        x = s[0]
        x ^= (x << 13) & 0xFFFFFFFF
        x ^= x >> 17
        x ^= (x << 5) & 0xFFFFFFFF
        s[0] = x & 0xFFFFFFFF
        return s[0] / 4294967296.0
    return r


# ----------------------------------------------------------------------------- metrics
_METRICS = None


def _metrics():
    global _METRICS
    if _METRICS is None:
        p = os.path.join(FONT_DIR, "metrics.json")
        if not os.path.exists(p):
            build_metrics()
        with open(p, encoding="utf-8") as fh:
            _METRICS = json.load(fh)
    return _METRICS


def build_metrics():
    if TTFont is None:
        raise RuntimeError("tools/fonts/metrics.json missing and fontTools unavailable")
    out = {}
    for alias, (_, file, _) in FONTS.items():
        font = TTFont(os.path.join(FONT_DIR, file))
        upm = font["head"].unitsPerEm
        hmtx = font["hmtx"]
        out[alias] = {chr(cp): round(hmtx[g][0] * 1000 / upm, 1) for cp, g in font.getBestCmap().items()}
    with open(os.path.join(FONT_DIR, "metrics.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, separators=(",", ":"))


def measure(text, alias, size, tracking=0.0):
    m = _metrics()[alias]
    fb = m.get("n", 520)
    return sum(m.get(ch, fb) for ch in text) * size / 1000.0 + tracking * len(text)


def fit_size(text, alias, max_w, size, tracking=0.0, min_size=8):
    while size > min_size and measure(text, alias, size, tracking) > max_w:
        size -= 0.5
    return size


def wrap(text, alias, size, max_w, tracking=0.0):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if not cur or measure(t, alias, size, tracking) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text(x, y, s, alias, size, fill, tracking=0, anchor=None, op=None, extra=""):
    a = f' text-anchor="{anchor}"' if anchor else ""
    o = f' fill-opacity="{f(op, 2)}"' if op is not None else ""
    t = f' letter-spacing="{f(tracking, 2)}"' if tracking else ""
    return f'<text x="{f(x)}" y="{f(y)}" class="{alias}" font-size="{f(size)}" fill="{fill}"{t}{a}{o} {extra}>{esc(s)}</text>'


# ----------------------------------------------------------------------------- kanji as paths
_KANJI = None


def _kanji():
    global _KANJI
    if _KANJI is None:
        with open(os.path.join(FONT_DIR, "kanji.json"), encoding="utf-8") as fh:
            _KANJI = json.load(fh)
    return _KANJI


def kanji(s, x, y, size, fill="#000", style="brush", anchor="start", vertical=False, gap=0.0,
          op=None, extra=""):
    """Japanese text as glyph paths. (x, y) is the baseline start; for vertical text it is
    the centre-top of the column."""
    table = _kanji()[style]
    k = size / 1000.0
    parts = []
    if vertical:
        for i, ch in enumerate(s):
            adv, d = table[ch]
            gx = x - adv * k / 2
            gy = y + (i + 0.86) * size * (1 + gap)
            parts.append(f'<path transform="translate({f(gx)} {f(gy)}) scale({f(k, 4)})" d="{d}"/>')
    else:
        total = sum(table[ch][0] for ch in s) * k + gap * size * (len(s) - 1)
        cx = x - (total if anchor == "end" else total / 2 if anchor == "middle" else 0)
        for ch in s:
            adv, d = table[ch]
            parts.append(f'<path transform="translate({f(cx)} {f(y)}) scale({f(k, 4)})" d="{d}"/>')
            cx += adv * k + gap * size
    o = f' fill-opacity="{f(op, 2)}"' if op is not None else ""
    return f'<g fill="{fill}"{o} {extra}>{"".join(parts)}</g>'


# ----------------------------------------------------------------------------- fonts
def _font_b64(alias, chars):
    path = os.path.join(FONT_DIR, FONTS[alias][1])
    if _subset is not None and chars:
        font = TTFont(path)
        o = _subset.Options()
        o.flavor = "woff"
        o.layout_features = ["kern", "liga"]
        o.hinting = False
        o.name_IDs = []
        o.notdef_outline = True
        sub = _subset.Subsetter(o)
        sub.populate(text="".join(sorted(chars)))
        sub.subset(font)
        font.flavor = "woff"
        buf = io.BytesIO()
        font.save(buf)
        data = buf.getvalue()
    else:
        with open(path, "rb") as fh:
            data = fh.read()
    return base64.b64encode(data).decode("ascii")


_TEXT_RE = re.compile(r'<(?:text|tspan)\b[^>]*class="([a-z0-9]+)"[^>]*>([^<]*)')


def _used(body):
    """{alias: chars} for every font class used by a <text>/<tspan>."""
    used = {}
    for alias, t in _TEXT_RE.findall(body):
        if alias in FONTS:
            used.setdefault(alias, set()).update(html.unescape(t))
    return used


def font_css(body):
    css = []
    used = _used(body)
    # inherited tspans: add their characters to the parent text's font
    for m in re.finditer(r'<text\b[^>]*class="([a-z0-9]+)"[^>]*>(.*?)</text>', body, re.S):
        alias = m.group(1)
        if alias in FONTS:
            inner = re.sub(r"<[^>]+>", "", m.group(2))
            used.setdefault(alias, set()).update(html.unescape(inner))
    for alias in FONTS:
        if alias not in used:
            continue
        fam, _, stack = FONTS[alias]
        chars = used[alias] | {" "}
        css.append("@font-face{font-family:%s;src:url(data:font/woff;base64,%s) format('woff')}" % (fam, _font_b64(alias, chars)))
        css.append(".%s{font-family:%s,%s}" % (alias, fam, stack))
    return "".join(css)


# ----------------------------------------------------------------------------- raster data
def data_uri(name, mime=None):
    path = os.path.join(DATA_DIR, name)
    mime = mime or {"webp": "image/webp", "png": "image/png", "jpg": "image/jpeg"}[name.rsplit(".", 1)[1]]
    with open(path, "rb") as fh:
        return f"data:{mime};base64," + base64.b64encode(fh.read()).decode("ascii")


def grain_defs(uid, op=0.07):
    """Film grain: a tiny noise tile repeated (cheap to paint, unlike feTurbulence)."""
    return (f'<pattern id="{uid}grain" width="64" height="64" patternUnits="userSpaceOnUse">'
            f'<image href="{data_uri("grain.png")}" width="64" height="64" opacity="{op}"/></pattern>')


# ----------------------------------------------------------------------------- document
def doc(w, h, body, css="", defs="", title="", desc=""):
    style = font_css(body) + css
    out = "".join([
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-labelledby="t d">',
        f'<title id="t">{esc(title)}</title><desc id="d">{esc(desc)}</desc>',
        f"<style>{style}</style>" if style else "",
        f"<defs>{defs}</defs>" if defs else "",
        body, "</svg>",
    ])
    return re.sub(r">\s+<", "><", out)


def write(path, svg):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(svg)
    return len(svg.encode("utf-8"))
