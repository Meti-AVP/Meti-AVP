"""Rebuild the static panels in assets/.      python tools/build.py [panel ...]"""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets")

PANELS = ["prologue", "virtues", "path", "blades", "honors", "arsenal", "duel", "links", "epilogue"]


def main(names):
    for n in names or PANELS:
        t = time.time()
        mod = __import__(n)
        res = mod.build(OUT)
        print(f"{n:10s} {time.time() - t:5.1f}s  {res}")


if __name__ == "__main__":
    main(sys.argv[1:])
