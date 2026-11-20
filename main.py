#!/usr/bin/env python3
"""Entry for make.fun's news-image-20261119 bounty.

The image this entry submits is the PNG beside this file; the grader runs the
program in a fresh container with no network, a read-only /bot holding this
repository and a writable /output, and reads exactly the bytes written to
/output/entry.png. Outside the grader MAKEFUN_OUTPUT_DIR stands in for /output:

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
import sys
from pathlib import Path

IMAGE = Path(__file__).resolve().parent / "entry.png"
MAX_BYTES = 1024 * 1024
MAX_SIDE = 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def output_dir() -> Path:
    return Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")


def check(path: Path) -> None:
    data = path.read_bytes()
    if not data.startswith(PNG_MAGIC):
        sys.exit("entry.png is not a PNG")
    if len(data) > MAX_BYTES:
        sys.exit(f"entry.png is {len(data)} bytes, over the {MAX_BYTES} byte cap")
    width = int.from_bytes(data[16:20], "big")
    height = int.from_bytes(data[20:24], "big")
    if width > MAX_SIDE or height > MAX_SIDE:
        sys.exit(f"entry.png is {width} by {height}, over {MAX_SIDE}")


def main() -> None:
    check(IMAGE)
    out = output_dir()
    out.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(IMAGE, out / "entry.png")


if __name__ == "__main__":
    main()
