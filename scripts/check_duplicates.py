#!/usr/bin/env python3
"""Find duplicate or near-duplicate assets.

Compares normalized filenames (case/separator insensitive) and SVG <title>
values across the library, so contributors avoid uploading the same concept
twice with names like mitochondrion1.svg / mitochondrion2.svg.

Usage: python scripts/check_duplicates.py
"""

from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
SVG_NS = "{http://www.w3.org/2000/svg}"


def normalize(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", name.lower())


def main() -> int:
    files = sorted(ASSETS.rglob("*.svg"))
    by_name: dict[str, list[Path]] = defaultdict(list)
    by_title: dict[str, list[Path]] = defaultdict(list)

    for f in files:
        by_name[normalize(f.stem)].append(f)
        try:
            root = ET.parse(f).getroot()
            t = root.find(f"{SVG_NS}title")
            if t is not None and t.text:
                by_title[normalize(t.text)].append(f)
        except ET.ParseError:
            pass

    problems: list[str] = []
    notes: list[str] = []

    for key, group in sorted(by_name.items()):
        if len(group) > 1:
            problems.append(
                "duplicate concept: " + ", ".join(str(p.relative_to(ROOT)) for p in group)
            )

    for key, group in sorted(by_title.items()):
        if len(group) > 1:
            notes.append(
                "duplicate title: " + ", ".join(str(p.relative_to(ROOT)) for p in group)
            )

    print(f"SciSVG Duplicate Check ({len(files)} files)")
    print("-" * 45)
    print(f"Duplicate filenames:   {len(problems)}")
    print(f"Duplicate titles:      {len(notes)}")
    for p in problems:
        print(f"\u2717 {p}")
    for n in notes:
        print(f"\u26a0 {n}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
