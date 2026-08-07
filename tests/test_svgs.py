"""SciSVG test suite.

Run with: pytest -q
"""

from __future__ import annotations

import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_catalog  # noqa: E402
import validate_svgs  # noqa: E402

ASSETS = ROOT / "assets"
SVG_NS = "{http://www.w3.org/2000/svg}"


def all_svgs() -> list[Path]:
    return sorted(ASSETS.rglob("*.svg"))


def test_all_assets_are_svgs():
    assert all(p.suffix == ".svg" for p in all_svgs())


def test_assets_pass_validation():
    issues_by_file = {}
    for f in all_svgs():
        issues = validate_svgs.validate_file(f)
        assert not issues.errors, f"{f.relative_to(ROOT)}: {issues.errors}"
        issues_by_file[f] = issues
    # Warnings are tolerated, but the standard set should be small.
    total_warnings = sum(len(i.warnings) for i in issues_by_file.values())
    assert total_warnings == 0, f"{total_warnings} warnings: " + "; ".join(
        w for i in issues_by_file.values() for w in i.warnings
    )


def test_filename_convention():
    pattern = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*\.svg$")
    bad = [p.name for p in all_svgs() if not pattern.match(p.name)]
    assert not bad, f"non-kebab-case filenames: {bad}"


def test_attribution_comment_present():
    for f in all_svgs():
        text = f.read_text(encoding="utf-8")
        assert re.search(r"CC\s?BY[- ]4\.0", text), f"{f.name}: no CC BY 4.0 comment"
        assert "Saveena Solanki" in text, f"{f.name}: no attribution"


def test_no_scripts_or_raster():
    for f in all_svgs():
        text = f.read_text(encoding="utf-8").lower()
        for bad in ("<script", "<image", "foreignobject", "javascript:", "data:image"):
            assert bad not in text, f"{f.name}: contains {bad!r}"


def test_no_duplicate_ids():
    for f in all_svgs():
        root = ET.parse(f).getroot()
        ids = [el.get("id") for el in root.iter() if el.get("id")]
        assert len(ids) == len(set(ids)), f"{f.name}: duplicate ids"


def test_catalog_builds_and_matches_disk():
    build_catalog.main()
    catalog = json.loads((ROOT / "website" / "catalog.json").read_text(encoding="utf-8"))
    disk = {p.relative_to(ROOT).as_posix() for p in all_svgs()}
    indexed = {a["path"] for a in catalog["assets"]}
    assert catalog["count"] == len(catalog["assets"]) == len(disk)
    assert indexed == disk


def test_metadata_schema():
    assets = json.loads((ROOT / "metadata" / "assets.json").read_text(encoding="utf-8"))[
        "assets"
    ]
    categories = json.loads(
        (ROOT / "metadata" / "categories.json").read_text(encoding="utf-8")
    )
    required = {
        "id", "name", "category", "tags", "description", "contributor", "license",
        "version", "scientifically_reviewed", "editable", "vector_only", "safe_svg",
        "path", "filename",
    }
    for a in assets:
        assert required <= set(a), f"{a.get('id')}: missing {required - set(a)}"
        assert a["license"] == "CC-BY-4.0"
        assert a["category"] in categories
        if a.get("subcategory"):
            assert a["subcategory"] in categories[a["category"]]["subcategories"]
        assert a["scientifically_reviewed"] in (True, False)


def test_every_disk_svg_is_indexed():
    assets = json.loads((ROOT / "metadata" / "assets.json").read_text(encoding="utf-8"))[
        "assets"
    ]
    indexed = {a["path"] for a in assets}
    disk = {p.relative_to(ROOT).as_posix() for p in all_svgs()}
    assert disk == indexed
