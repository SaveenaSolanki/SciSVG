#!/usr/bin/env python3
"""Validate SciSVG assets against the library quality standard.

Errors (a file fails):
  * XML not well-formed, or root is not an SVG element with the SVG namespace
  * missing or malformed viewBox
  * <script> elements, event-handler attributes, or javascript: URLs
  * <foreignObject> elements
  * raster content: <image> elements, base64 data URIs, external image URLs
  * external resources: href/xlink:href pointing outside the file
  * duplicate element IDs
  * broken fragment references (url(#id) / href="#id" with no matching ID)
  * filename not lowercase kebab-case
  * missing CC BY 4.0 attribution comment

Warnings:
  * missing <title> or <desc>
  * viewBox other than 0 0 512 512
  * unused <defs> definitions
  * <metadata> remnants or file larger than 512 KB

Usage:
    python scripts/validate_svgs.py [paths...]     # default: assets/**
    python scripts/validate_svgs.py --json         # machine-readable report
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TARGETS = [ROOT / "assets"]

SVG_NS = "{http://www.w3.org/2000/svg}"
XLINK_NS = "{http://www.w3.org/1999/xlink}"

FILENAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*\.svg$")
ID_REF_RE = re.compile(r"url\(#([^)]+)\)")
MAX_SIZE = 512 * 1024
MAX_ELEMENTS = 2000


class Issues:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []


def _local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _attr_value(el, name: str) -> str | None:
    for key in (name, f"{XLINK_NS}{name}"):
        if key in el.attrib:
            return el.attrib[key]
    return None


def validate_file(path: Path) -> Issues:
    issues = Issues()
    rel = path.relative_to(ROOT).as_posix() if str(path).startswith(str(ROOT)) else str(path)

    if not FILENAME_RE.match(path.name):
        issues.errors.append(f"{rel}: filename not lowercase kebab-case: {path.name}")

    text = path.read_text(encoding="utf-8", errors="replace")
    if not re.search(r"CC\s?BY[- ]4\.0", text):
        issues.errors.append(f"{rel}: missing CC BY 4.0 attribution comment")

    try:
        import lxml.etree as ET  # type: ignore
    except ImportError:  # pragma: no cover
        import xml.etree.ElementTree as ET  # type: ignore

    try:
        tree = ET.parse(str(path))
    except ET.XMLSyntaxError as exc:
        issues.errors.append(f"{rel}: XML parse error: {exc}")
        return issues

    root = tree.getroot()
    if root.tag != f"{SVG_NS}svg":
        issues.errors.append(f"{rel}: root element is not an SVG in the SVG namespace")
        return issues

    viewbox = root.get("viewBox")
    if not viewbox:
        issues.errors.append(f"{rel}: missing viewBox")
    else:
        try:
            parts = [float(x) for x in viewbox.split()]
            if len(parts) != 4:
                raise ValueError
        except ValueError:
            issues.errors.append(f"{rel}: malformed viewBox: {viewbox!r}")
        else:
            if parts != [0.0, 0.0, 512.0, 512.0]:
                issues.warnings.append(
                    f"{rel}: viewBox is {viewbox!r} (library standard is 0 0 512 512)"
                )

    if root.find(f"{SVG_NS}title") is None:
        issues.warnings.append(f"{rel}: missing <title> (recommended)")
    if root.find(f"{SVG_NS}desc") is None:
        issues.warnings.append(f"{rel}: missing <desc> (recommended)")

    if path.stat().st_size > MAX_SIZE:
        issues.warnings.append(f"{rel}: file larger than 512 KB ({path.stat().st_size} bytes)")

    ids: dict[str, list[str]] = {}
    refs: list[str] = []
    defs_ids: set[str] = set()
    used_ids: set[str] = set()
    element_count = 0

    for el in root.iter():
        if not isinstance(el.tag, str):  # lxml comment/PI nodes
            continue
        element_count += 1
        tag = _local(el.tag)

        if tag == "script":
            issues.errors.append(f"{rel}: <script> element detected")
        if tag == "foreignObject":
            issues.errors.append(f"{rel}: <foreignObject> element detected")
        if tag == "image":
            issues.errors.append(f"{rel}: embedded raster image (<image>) detected")

        for attr, value in el.attrib.items():
            aname = _local(attr)
            if aname.startswith("on") and value.strip():
                issues.errors.append(f"{rel}: event-handler attribute {aname!r} detected")
            if aname in ("href", "xlink:href"):
                v = value.strip()
                if v.lower().startswith("data:image"):
                    issues.errors.append(f"{rel}: embedded base64 raster in {aname}")
                elif v.lower().startswith("javascript:"):
                    issues.errors.append(f"{rel}: javascript: URL in {aname}")
                elif v.startswith(("http://", "https://", "//")) or "://" in v:
                    issues.errors.append(f"{rel}: external resource in {aname}: {v[:60]}")
                elif v.startswith("#"):
                    refs.append(v[1:])
                elif v:
                    issues.errors.append(f"{rel}: external file reference in {aname}: {v[:60]}")
            if aname == "id":
                ids.setdefault(value, []).append(rel)
            for m in ID_REF_RE.finditer(value):
                refs.append(m.group(1))

        if tag == "defs":
            for child in el.iter():
                cid = child.get("id")
                if cid:
                    defs_ids.add(cid)

    for ref in refs:
        used_ids.add(ref)
        if ref not in ids:
            issues.errors.append(f"{rel}: broken reference to #{ref}")

    for dup, where in ids.items():
        if len(where) > 1:
            issues.errors.append(f"{rel}: duplicate element ID: {dup!r} ({len(where)} uses)")

    for unused in sorted(defs_ids - used_ids):
        issues.warnings.append(f"{rel}: unused definition: #{unused}")

    if root.find(f"{SVG_NS}metadata") is not None:
        issues.warnings.append(f"{rel}: <metadata> block present (editor metadata)")

    if element_count > MAX_ELEMENTS:
        issues.warnings.append(f"{rel}: very large file ({element_count} elements)")

    return issues


def collect_targets(args: list[str]) -> list[Path]:
    if not args:
        return DEFAULT_TARGETS
    targets = []
    for a in args:
        p = Path(a)
        targets.append(p if p.is_absolute() else (ROOT / p))
    return targets


def main(argv: list[str]) -> int:
    as_json = "--json" in argv
    paths = [a for a in argv if a != "--json"]

    files: list[Path] = []
    for target in collect_targets(paths):
        if target.is_dir():
            files.extend(sorted(target.rglob("*.svg")))
        elif target.is_file() and target.suffix == ".svg":
            files.append(target)

    files = sorted(set(files))
    report: dict[str, dict] = {}
    errors = warnings = 0
    for f in files:
        rel = f.relative_to(ROOT).as_posix() if str(f).startswith(str(ROOT)) else str(f)
        iss = validate_file(f)
        errors += len(iss.errors)
        warnings += len(iss.warnings)
        report[rel] = {"errors": iss.errors, "warnings": iss.warnings}

    if as_json:
        print(
            json.dumps(
                {
                    "checked": len(files),
                    "valid": len(files) - sum(1 for r in report.values() if r["errors"]),
                    "errors": errors,
                    "warnings": warnings,
                    "files": report,
                },
                indent=2,
            )
        )
        return 1 if errors else 0

    print("SciSVG Validation Report")
    print("-" * 45)
    print(f"SVG files checked:  {len(files)}")
    print(f"Valid SVGs:         {len(files) - sum(1 for r in report.values() if r['errors'])}")
    print(f"Errors:             {errors}")
    print(f"Warnings:           {warnings}")
    print()
    for rel, r in report.items():
        for e in r["errors"]:
            print(f"\u2717 {e}")
        for w in r["warnings"]:
            print(f"\u26a0 {w}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
