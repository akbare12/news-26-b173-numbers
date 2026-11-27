#!/usr/bin/env python3
"""news-26-b173-numbers entry point (stdlib only: os, shutil, hashlib).

Copies the pre-rendered entry.png (built by gen.py at build time) into
MAKEFUN_OUTPUT_DIR. No image work happens here, so the grader's
stdlib-only environment is enough: no PIL, no numpy, no network.
"""
import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
MAX_BYTES = 1024 * 1024


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    dst = os.path.join(out_dir, "entry.png")
    if not os.path.isfile(SRC):
        print("missing entry.png next to main.py", file=sys.stderr)
        return 1
    size = os.path.getsize(SRC)
    if size > MAX_BYTES:
        print("entry.png %d bytes exceeds 1 MiB cap" % size, file=sys.stderr)
        return 1
    with open(SRC, "rb") as f:
        magic = f.read(8)
    if magic != b"\x89PNG\r\n\x1a\n":
        print("entry.png is not a PNG file", file=sys.stderr)
        return 1
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(SRC, dst)
    if sha256(SRC) != sha256(dst):
        print("copy checksum mismatch", file=sys.stderr)
        return 1
    print("OK entry.png %d bytes sha256=%s -> %s" % (size, sha256(dst), dst))
    return 0


if __name__ == "__main__":
    sys.exit(main())
