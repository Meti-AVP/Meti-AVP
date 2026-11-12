"""Build-time only: grade the portrait into the palette and cut it out.

    python tools/make_portrait.py <photo.png> <alpha.png>

alpha.png is the subject matte (a U2-Net-P person prior refined with a colour matte on
the red backdrop). Output: tools/data/portrait.webp (800x800, RGBA) used by the SVGs.
"""
import os
import sys

import numpy as np
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))


def hexc(h):
    return np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)], np.float32) / 255.0


def lut(stops):
    xs = np.array([s[0] for s in stops])
    cs = np.stack([hexc(s[1]) for s in stops])

    def f(v):
        out = np.empty(v.shape + (3,), np.float32)
        for c in range(3):
            out[..., c] = np.interp(v, xs, cs[:, c])
        return out
    return f


def main(photo, alpha_path):
    S = 800
    img = Image.open(photo).convert("RGB").resize((S, S), Image.LANCZOS)
    img = img.filter(ImageFilter.UnsharpMask(radius=2.2, percent=70, threshold=2))
    a = np.asarray(img).astype(np.float32) / 255.0
    lum = 0.30 * a[..., 0] + 0.59 * a[..., 1] + 0.11 * a[..., 2]
    lo, hi = np.percentile(lum, 1), np.percentile(lum, 99.7)
    v = np.clip((lum - lo) / (hi - lo), 0, 1)
    v = 1 / (1 + np.exp(-1.1 * 6 * (v - 0.43)))
    tri = lut([(0, "#030001"), (0.18, "#1A0508"), (0.40, "#5E070C"), (0.62, "#9F0A10"),
               (0.82, "#DDBFA6"), (1, "#F6EEDA")])(v)
    natural = np.clip((a - 0.02) * 1.22, 0, 1) ** 0.92
    out = 0.56 * tri + 0.44 * natural
    out = out ** 0.94  # lift the face a touch
    rng = np.random.default_rng(7)
    out = np.clip(out + rng.normal(0, 0.028, out.shape[:2])[..., None] * (0.5 + 0.5 * (1 - v[..., None])), 0, 1)
    alpha = np.asarray(Image.open(alpha_path).convert("L").resize((S, S), Image.LANCZOS)).astype(np.float32) / 255.0
    rgba = np.dstack([out, alpha])
    im = Image.fromarray((rgba * 255).astype(np.uint8), "RGBA")
    dst = os.path.join(HERE, "data", "portrait.webp")
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    im.save(dst, "WEBP", quality=84, method=6, alpha_quality=90)
    print(dst, os.path.getsize(dst), "bytes")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
