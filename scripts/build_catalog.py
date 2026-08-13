#!/usr/bin/env python3
"""Build website/catalog.json and metadata/assets.json from SVGs in assets/.

Every asset is indexed with a rich, searchable schema (id, name, category,
subcategory, tags, description, contributor, license, version, quality flags)
so the website can search beyond filenames.
"""

from __future__ import annotations

import json
import re
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
WEBSITE = ROOT / "website"
METADATA = ROOT / "metadata"
CATALOG_OUT = WEBSITE / "catalog.json"
ASSETS_OUT = METADATA / "assets.json"

LICENSE = "CC-BY-4.0"
VERSION = "1.0.0"
DEFAULT_CONTRIBUTOR = "Saveena Solanki"

SVG_NS = "{http://www.w3.org/2000/svg}"
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


def load_json(path: Path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default


def main() -> None:
    categories = load_json(METADATA / "categories.json", {})
    contributors = load_json(METADATA / "contributors.json", {"contributors": []})
    orcid_by_name = {
        c.get("name"): c.get("orcid", "") for c in contributors.get("contributors", [])
    }

    assets = []
    for svg in sorted(ASSETS.rglob("*.svg")):
        rel = svg.relative_to(ROOT).as_posix()
        parts = svg.relative_to(ASSETS).parts
        category = parts[0]
        subcategory = parts[1] if len(parts) > 2 else ""
        rel_assets = svg.relative_to(ASSETS).as_posix()

        title, desc = svg_meta(svg)
        title = title or prettify(svg.stem)
        tags = [t for t in re.split(r"[-_\s]+", svg.stem.lower()) if t]
        contributor = DEFAULT_CONTRIBUTOR
        asset_id = "-".join(
            p for p in [category, subcategory or "misc", svg.stem] if p
        ).lower()
        assets.append(
            {
                "id": asset_id,
                "name": title,
                "category": category,
                "subcategory": subcategory or None,
                "tags": tags,
                "description": desc,
                "contributor": contributor,
                "orcid": orcid_by_name.get(contributor, ""),
                "license": LICENSE,
                "version": VERSION,
                "scientifically_reviewed": False,
                "editable": True,
                "vector_only": True,
                "safe_svg": True,
                "path": rel,
                "filename": svg.name,
                "preview": f"previews/{rel_assets.removesuffix('.svg')}.png",
            }
        )

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "count": len(assets),
        "assets": assets,
    }
    # Avoid timestamp churn: keep the previous generated_at when the asset
    # content is unchanged, so the catalog bot does not commit on every run.
    for out in (CATALOG_OUT, ASSETS_OUT):
        if out.exists():
            try:
                existing = json.loads(out.read_text(encoding="utf-8"))
                if existing.get("assets") == assets:
                    payload["generated_at"] = existing.get(
                        "generated_at", payload["generated_at"]
                    )
            except (OSError, json.JSONDecodeError):
                pass
    CATALOG_OUT.parent.mkdir(parents=True, exist_ok=True)
    ASSETS_OUT.parent.mkdir(parents=True, exist_ok=True)
    CATALOG_OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    ASSETS_OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(assets)} assets to {CATALOG_OUT} and {ASSETS_OUT}")


if __name__ == "__main__":
    main()
