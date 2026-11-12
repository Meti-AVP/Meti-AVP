"""The byōbu: panels stacked on the profile share ONE painting.

Each full-width panel knows where it sits on the long vertical scroll, and elements that
cross a panel boundary (the katana cut, the mountain range...) are defined once in these
global coordinates, then drawn into every panel they touch. On GitHub the panels sit a few
pixels apart, like the hinged leaves of a folding screen, and the art continues across them.
"""
import art

W = 1200
STACK = [("prologue", 680), ("virtues", 700), ("path", 640), ("blades", 230)]
OFFSET = {}
_y = 0
for _name, _h in STACK:
    OFFSET[_name] = _y
    _y += _h
HEIGHT = dict(STACK)

# the cut that starts in the prologue and ends in chapter one
SLASH = dict(x1=70, y1=606, x2=1030, y2=812, bow=-58, thick=13)

# mountain range whose far peaks rise into chapter one and whose body is chapter two
RIDGES = [  # global base y, height, colour, seed
    (1700, 380, "#360A10", 31),
    (1800, 300, "#1A0609", 47),
    (1990, 230, "#0D0305", 59),
]


def slash(panel, uid):
    oy = OFFSET[panel]
    s = SLASH
    return art.slash(uid, s["x1"], s["y1"] - oy, s["x2"], s["y2"] - oy, bow=s["bow"], thick=s["thick"], period=8.0)


def ridges(panel, uid, layers=None):
    oy = OFFSET[panel]
    out = []
    for i, (base, h, col, seed) in enumerate(RIDGES):
        if layers is not None and i not in layers:
            continue
        out.append(art.mountains(uid, -20, W + 20, base - oy, heights=[h], colors=[col], seed=seed, peaks=2.4))
    return "".join(out)
