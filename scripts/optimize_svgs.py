#!/usr/bin/env python3
"""Optimize distributed SVGs with SVGO.

Runs the SVGO CLI with the repository's svgo.config.js, which is configured to
preserve the CC BY 4.0 attribution comments, <title>, <desc> and viewBox.

Usage:
    python scripts/optimize_svgs.py [paths...]     # default: assets/**

Requires Node.js and SVGO (npm install).
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TARGETS = [ROOT / "assets"]
CONFIG = ROOT / "svgo.config.js"


def find_svgo() -> str | None:
    exe = shutil.which("svgo")
    if exe:
        return exe
    npx = shutil.which("npx")
    if npx:
        return npx
    return None


def main(argv: list[str]) -> int:
    targets = [Path(a) for a in argv] if argv else DEFAULT_TARGETS

    svgo = find_svgo()
    if not svgo:
        print("SVGO not found. Install it with: npm install")
        print("(the repo ships a package.json with svgo as a devDependency)")
        return 2

    files: list[Path] = []
    for t in targets:
        p = t if t.is_absolute() else (ROOT / t)
        if p.is_dir():
            files.extend(sorted(p.rglob("*.svg")))
        elif p.is_file():
            files.append(p)

    cmd = [svgo, "--config", str(CONFIG)]
    if svgo.endswith("npx"):
        cmd = [svgo, "--yes", "svgo", "--config", str(CONFIG)]
    cmd += [str(f) for f in files]

    print("Running:", " ".join(cmd))
    result = subprocess.run(cmd, cwd=ROOT)
    if result.returncode == 0:
        print(f"Optimized {len(files)} SVGs")
    return result.returncode


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
