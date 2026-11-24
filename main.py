#!/usr/bin/env python3
"""Entry point for the news-image-20261124 entry.

Copies the baked poster (entry.png, drawn by poster.py) into the output
directory. Standard library only; no network.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    # Clear only the contents of the output dir, never the dir itself.
    for name in os.listdir(out_dir):
        path = os.path.join(out_dir, name)
        if os.path.isdir(path) and not os.path.islink(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
    shutil.copyfile(SRC, os.path.join(out_dir, "entry.png"))
    dest = os.path.join(out_dir, "entry.png")
    size = os.path.getsize(dest)
    if size > 1048576:
        raise SystemExit("entry.png exceeds 1 MiB: %d bytes" % size)
    print("wrote %s (%d bytes)" % (dest, size))


if __name__ == "__main__":
    sys.exit(main())
