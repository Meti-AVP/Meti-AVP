"""Build-time only: produce the committed font assets from the full Google Fonts TTFs.

    python tools/make_fonts.py <dir-with-ttfs>

Outputs (tools/fonts/):
  *.woff        Latin subsets (ASCII + typographic extras) embedded into the SVGs
  metrics.json  advance widths, so layout code can measure text without fontTools
  kanji.json    brush (Yuji Syuku) and mincho (Shippori Mincho) glyphs as SVG path data,
                so Japanese renders identically everywhere with no CJK font embedded
"""
import json
import os
import sys

from fontTools import subset
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "fonts")

EXTRAS = "ŪūŌōĀāĒēĪī·—–’‘“”…•→←↑↓↗↘×°±©®™§¶†‡№★☆◆◇▲▼▶◀●○■□▸"
LATIN = {
    "CormorantGaramond-600.ttf": "serif-600.woff",
    "CormorantGaramond-700.ttf": "serif-700.woff",
    "CormorantGaramond-600i.ttf": "serif-600i.woff",
    "Manrope-500.ttf": "sans-500.woff",
    "Manrope-700.ttf": "sans-700.woff",
    "Manrope-800.ttf": "sans-800.woff",
}
# every Japanese character the profile and the game may draw
KANJI = ("侍創る者の道序壱弐参肆伍陸漆終武士義勇仁礼誠名誉忠入門修行初陣鍛錬緑将頂刀星水優数器流決闘"
         "三四五六七転び八起き誤札鬼旱魃竜仕様虫疑念軍斬弓桜茶二周目殿堂勝負必殺一閃年天下無双心技体残花散風月"
         "夢魂己火家紋和美刃影光剣師匠弟子極意氣気大阪京都東西南北中央日本埃及開拓鬼退治挑戦者対浪人第章撃破回復集矢吹雪利敗番")


def latin(src_dir):
    ascii_ = "".join(chr(c) for c in range(32, 127))
    for src, dst in LATIN.items():
        font = TTFont(os.path.join(src_dir, src))
        have = set(font.getBestCmap())
        text = "".join(ch for ch in ascii_ + EXTRAS if ord(ch) in have)
        opts = subset.Options()
        opts.flavor = "woff"
        opts.layout_features = ["kern", "liga"]
        opts.hinting = False
        opts.name_IDs = ["*"]
        opts.notdef_outline = True
        s = subset.Subsetter(opts)
        s.populate(text=text)
        s.subset(font)
        font.flavor = "woff"
        font.save(os.path.join(OUT, dst))
        print(f"{dst:16s} {os.path.getsize(os.path.join(OUT, dst)):7d} B")


def glyph_paths(path, chars):
    font = TTFont(path)
    upm = font["head"].unitsPerEm
    cmap = font.getBestCmap()
    gs = font.getGlyphSet()
    k = 1000.0 / upm
    out = {}
    for ch in dict.fromkeys(chars):
        g = cmap.get(ord(ch))
        if g is None:
            print("  missing", ch, "in", os.path.basename(path))
            continue
        pen = SVGPathPen(gs, ntos=lambda v: ("%.0f" % v))
        gs[g].draw(TransformPen(pen, (k, 0, 0, -k, 0, 0)))
        out[ch] = [round(gs[g].width * k), pen.getCommands()]
    return out


def main(src_dir):
    latin(src_dir)
    kanji = {
        "brush": glyph_paths(os.path.join(src_dir, "YujiSyuku-400.ttf"), KANJI),
        "mincho": glyph_paths(os.path.join(src_dir, "ShipporiMincho-800.ttf"), KANJI),
    }
    with open(os.path.join(OUT, "kanji.json"), "w", encoding="utf-8") as fh:
        json.dump(kanji, fh, ensure_ascii=False, separators=(",", ":"))
    print("kanji.json", os.path.getsize(os.path.join(OUT, "kanji.json")), "B")


if __name__ == "__main__":
    main(sys.argv[1])
