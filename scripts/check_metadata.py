#!/usr/bin/env python3
"""Check metadata/assets.json against the library and the metadata schema.

Verifies that:
  * every asset entry has all required fields
  * every asset on disk is indexed and every indexed asset exists
  * categories and subcategories exist in metadata/categories.json
  * contributors exist in metadata/contributors.json

Usage: python scripts/check_metadata.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
METADATA = ROOT / "metadata"
ASSETS_DIR = ROOT / "assets"

REQUIRED_FIELDS = [
    "id",
    "name",
    "category",
    "tags",
    "description",
    "contributor",
    "license",
    "version",
    "scientifically_reviewed",
    "editable",
    "vector_only",
    "safe_svg",
    "path",
    "filename",
]


def load(name: str):
    return json.loads((METADATA / name).read_text(encoding="utf-8"))


def main() -> int:
    data = load("assets.json")
    categories = load("categories.json")
    contributors = load("contributors.json")
    assets = data["assets"]

    errors: list[str] = []
    warnings: list[str] = []

    disk_svgs = sorted(
        p.relative_to(ROOT).as_posix() for p in ASSETS_DIR.rglob("*.svg")
    )
    indexed = {a["path"] for a in assets}

    for a in assets:
        for field in REQUIRED_FIELDS:
            if field not in a:
                errors.append(f"{a.get('id', '?')}: missing field {field!r}")
        if a["category"] not in categories:
            errors.append(f"{a['id']}: unknown category {a['category']!r}")
        elif a.get("subcategory"):
            subs = categories[a["category"]].get("subcategories", {})
            if a["subcategory"] not in subs:
                errors.append(
                    f"{a['id']}: unknown subcategory {a['subcategory']!r} "
                    f"in {a['category']!r}"
                )
        if a["license"] != "CC-BY-4.0":
            errors.append(f"{a['id']}: unexpected license {a['license']!r}")
        if not a["path"] or not (ROOT / a["path"]).is_file():
            errors.append(f"{a['id']}: file missing on disk: {a['path']}")
        if not a.get("description"):
            warnings.append(f"{a['id']}: empty description")

    names = {c.get("name") for c in contributors.get("contributors", [])}
    for a in assets:
        if a["contributor"] not in names:
            errors.append(f"{a['id']}: contributor {a['contributor']!r} not in contributors.json")

    for p in disk_svgs:
        if p not in indexed:
            errors.append(f"{p}: on disk but not indexed in assets.json")

    print(f"SciSVG Metadata Report ({len(assets)} assets)")
    print("-" * 45)
    print(f"Indexed assets:     {len(assets)}")
    print(f"SVGs on disk:       {len(disk_svgs)}")
    print(f"Errors:             {len(errors)}")
    print(f"Warnings:           {len(warnings)}")
    for e in errors:
        print(f"\u2717 {e}")
    for w in warnings:
        print(f"\u26a0 {w}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
