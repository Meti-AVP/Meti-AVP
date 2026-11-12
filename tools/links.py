"""Clickable plates: socials + the call to play. One small SVG per link (GitHub links whole images)."""
import os

from svgkit import C, doc, fit_size, kanji, text, write

ICONS = {
    "linkedin": ('<rect x="-13" y="-13" width="26" height="26" rx="4" fill="none" stroke="{c}" stroke-width="2.2"/>'
                 '<rect x="-8" y="-3" width="3.6" height="11" fill="{c}"/><circle cx="-6.2" cy="-7.4" r="2.2" fill="{c}"/>'
                 '<path d="M-1 8V-3H2.4V-1C3.6 -3 9 -3.6 9 1.6V8H5.4V2.4C5.4 -.4 1.4 -.2 2.4 2.6V8Z" fill="{c}"/>'),
    "instagram": ('<rect x="-13" y="-13" width="26" height="26" rx="8" fill="none" stroke="{c}" stroke-width="2.2"/>'
                  '<circle r="6" fill="none" stroke="{c}" stroke-width="2.2"/><circle cx="7.6" cy="-7.6" r="1.8" fill="{c}"/>'),
    "facebook": ('<circle r="13.5" fill="none" stroke="{c}" stroke-width="2.2"/>'
                 '<path d="M2.2 14V2.6H6L6.6 -1.8H2.2V-4.4C2.2 -5.8 2.8 -6.6 4.6 -6.6H6.8V-10.4C6 -10.6 4.6 -10.8 3.4 -10.8'
                 'C-.2 -10.8 -2.2 -8.6 -2.2 -5V-1.8H-6V2.6H-2.2V14Z" fill="{c}"/>'),
    "email": ('<rect x="-14" y="-10" width="28" height="20" rx="2" fill="none" stroke="{c}" stroke-width="2.2"/>'
              '<path d="M-13 -8.5L0 2L13 -8.5" fill="none" stroke="{c}" stroke-width="2.2" stroke-linejoin="round"/>'),
    "portfolio": ('<circle r="13" fill="none" stroke="{c}" stroke-width="2.2"/>'
                  '<path d="M-13 0H13M0 -13C6 -6 6 6 0 13C-6 6 -6 -6 0 -13Z" fill="none" stroke="{c}" stroke-width="2"/>'),
}

PLATES = [
    ("linkedin", "LINKEDIN", "ahmed-zaki-gabr"),
    ("instagram", "INSTAGRAM", "@ahmedzaki_27"),
    ("facebook", "FACEBOOK", "ahmed.zaki.gabr"),
    ("email", "EMAIL", "barkzaki1999@gmail.com"),
    ("portfolio", "PORTFOLIO", "ahmedzaki.vercel.app"),
]


def plate(key, label, sub, w=228, h=76, primary=False):
    u = "ln" + key
    defs = (f'<linearGradient id="{u}bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{"#7E0910" if primary else "#1E070B"}"/>'
            f'<stop offset="1" stop-color="{"#4A0509" if primary else "#0B0304"}"/></linearGradient>')
    icon = ICONS[key].replace("{c}", C["rosary"])
    body = (f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="5" fill="url(#{u}bg)" stroke="{C["brass"]}" stroke-opacity=".55"/>'
            f'<rect x="6" y="6" width="{h - 12}" height="{h - 12}" rx="3" fill="{C["blood"] if not primary else "#2A0306"}"/>'
            f'<g transform="translate({h / 2} {h / 2})">{icon}</g>'
            + text(h + 8, 34, label, "ser7", 19, C["rosary"], tracking=3)
            + text(h + 8, 54, sub, "san7", fit_size(sub, "san7", w - h - 18, 10.5), C["brass_hi"], tracking=.4))
    svg = doc(w, h, body, defs=defs, title=f"{label}: {sub}", desc=f"Link to {label.title()}")
    return svg


def build(out_dir):
    sizes = []
    for key, label, sub in PLATES:
        sizes.append(write(os.path.join(out_dir, "links", f"{key}.svg"), plate(key, label, sub)))
    return sizes
