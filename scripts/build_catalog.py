#!/usr/bin/env python3
"""Build docs/catalog.json from SVG files stored under library/.

Reads the <title> and <desc> embedded in each SVG (falling back to a
pretty-printed filename) and records the asset license and attribution so
the gallery can display richer cards.
"""

from __future__ import annotations

import json
import re
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIBRARY = ROOT / "library"
OUTPUT = ROOT / "docs" / "catalog.json"

LICENSE = "CC BY 4.0"
ATTRIBUTION = (
    "SciSVG \u2014 Saveena Solanki, CC BY 4.0, "
    "https://github.com/SaveenaSolanki/SciSVG"
)

SVG_NS = "{http://www.w3.org/2000/svg}"

# Acronyms that should stay uppercase in auto-generated titles.
UPPER = {"dna", "rna", "mrna", "trna", "pcr", "utr", "ml", "ai"}


def prettify(stem: str) -> str:
    """Turn a hyphenated filename into a display title."""
    words = [w for w in re.split(r"[-_\s]+", stem.strip()) if w]
    return " ".join(w.upper() if w.lower() in UPPER else w.capitalize() for w in words)


def svg_meta(path: Path) -> tuple[str, str]:
    """Return (title, description) from the SVG, or empty strings."""
    title = desc = ""
    try:
        root = ET.parse(path).getroot()
        t = root.find(f"{SVG_NS}title")
        d = root.find(f"{SVG_NS}desc")
        if t is not None and t.text:
            title = " ".join(t.text.split())
        if d is not None and d.text:
            desc = " ".join(d.text.split())
    except (ET.ParseError, OSError):
        pass
    return title, desc


def main() -> None:
    assets = []
    for svg in sorted(LIBRARY.rglob("*.svg")):
        rel = svg.relative_to(ROOT).as_posix()
        category = svg.parent.relative_to(LIBRARY).as_posix()
        if category == ".":
            category = "general"
        title, desc = svg_meta(svg)
        title = title or prettify(svg.stem)
        tags = [t for t in re.split(r"[-_\s]+", svg.stem.lower()) if t]
        assets.append(
            {
                "title": title,
                "description": desc,
                "category": category,
                "path": rel,
                "filename": svg.name,
                "tags": tags,
                "license": LICENSE,
                "attribution": ATTRIBUTION,
            }
        )

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "count": len(assets),
        "assets": assets,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(assets)} assets to {OUTPUT}")


if __name__ == "__main__":
    main()
