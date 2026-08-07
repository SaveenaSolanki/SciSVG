#!/usr/bin/env python3
"""SciSVG Contributor Tool - add a new SVG asset the easy way.

Validates an SVG against the library standard, copies it into the right
category folder with a kebab-case name, records the contributor, and rebuilds
the catalog.

Interactive (recommended):

    python scripts/add_svg.py my_figure.svg

Fully automatic:

    python scripts/add_svg.py my_figure.svg \
        --category biology --subcategory organelles --name "Mitochondrion" \
        --tags "mitochondria,metabolism,ATP" --contributor "Jane Smith" --orcid "0000-..."
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
METADATA = ROOT / "metadata"
VALIDATE = ROOT / "scripts" / "validate_svgs.py"

CATEGORY_LABELS = {
    "biology": "Biology",
    "chemistry": "Chemistry",
    "medicine": "Medicine",
    "laboratory": "Laboratory",
    "bioinformatics": "Bioinformatics",
    "general-science": "General Science",
}

KEBAB_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def ask(prompt: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    value = input(f"{prompt}{suffix}: ").strip()
    return value or default


def pick(prompt: str, options: list[str]) -> str:
    for i, opt in enumerate(options, 1):
        print(f"  {i}. {opt}")
    while True:
        raw = input(f"{prompt} (1-{len(options)}): ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(options):
            return options[int(raw) - 1]
        if raw in options:
            return raw
        print("  Please pick a valid option.")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("svg", help="path to the SVG to add")
    parser.add_argument("--category")
    parser.add_argument("--subcategory")
    parser.add_argument("--name")
    parser.add_argument("--tags", help="comma-separated keywords")
    parser.add_argument("--contributor")
    parser.add_argument("--orcid")
    parser.add_argument("--yes", action="store_true", help="skip confirmations")
    args = parser.parse_args(argv)

    source = Path(args.svg)
    if not source.is_file():
        print(f"\u2717 Not found: {source}")
        return 1

    # 1. Validate the source SVG against the library standard.
    print("\nChecking SVG...")
    import subprocess

    proc = subprocess.run(
        [sys.executable, str(VALIDATE), str(source)],
        capture_output=True,
        text=True,
    )
    print(proc.stdout.strip())
    if proc.returncode != 0:
        print("\u2717 SVG does not pass validation. Fix the errors above and retry.")
        return 1

    # 2. Collect metadata.
    interactive = not any(
        [args.category, args.subcategory, args.name, args.tags, args.contributor]
    )
    if interactive:
        print("\nSciSVG Contributor Tool")
        print("=" * 30)
        category = pick("Category", list(CATEGORY_LABELS))
    else:
        category = args.category or ""
        if category not in CATEGORY_LABELS:
            print(f"\u2717 Unknown category {category!r}. Choose from: {', '.join(CATEGORY_LABELS)}")
            return 1

    categories = json.loads((METADATA / "categories.json").read_text(encoding="utf-8"))
    subcats = list(categories.get(category, {}).get("subcategories", {}).keys())

    if interactive:
        subcategory = ask(
            "Subcategory", subcats[0] if subcats else ""
        )
        name = ask("Asset name", source.stem.replace("-", " ").title())
        tags = ask("Keywords (comma separated)", "")
        contributor = ask("Your name", "")
    else:
        subcategory = args.subcategory or ""
        name = args.name or source.stem.replace("-", " ").title()
        tags = args.tags or ""
        contributor = args.contributor or ""

    orcid = args.orcid or ""

    if subcategory and subcats and subcategory not in subcats:
        print(f"\u26a0 Subcategory {subcategory!r} not in {category}; adding it.")

    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    if not KEBAB_RE.match(slug):
        slug = re.sub(r"[^a-z0-9]+", "-", source.stem.lower()).strip("-")
    if not KEBAB_RE.match(slug):
        print("\u2717 Could not derive a kebab-case filename.")
        return 1

    dest_dir = ASSETS / category / subcategory if subcategory else ASSETS / category
    dest = dest_dir / f"{slug}.svg"
    dest_dir.mkdir(parents=True, exist_ok=True)

    # 3. Ensure title/desc and attribution comment are present.
    text = source.read_text(encoding="utf-8")
    if not re.search(r"CC\s?BY[- ]4\.0", text):
        comment = "\n  <!-- SciSVG \u2014 Saveena Solanki, CC BY 4.0, https://github.com/SaveenaSolanki/SciSVG -->\n"
        text = re.sub(r"(<svg[^>]*>)", r"\1" + comment, text, count=1)
    if contributor:
        text = re.sub(
            r"(<!-- SciSVG)",
            f"<!-- Contributor: {contributor}" + (f" (ORCID {orcid})" if orcid else "") + "\n  \\1",
            text,
            count=1,
        )
    dest.write_text(text, encoding="utf-8")

    # 4. Record the contributor.
    contributors_path = METADATA / "contributors.json"
    contributors = json.loads(contributors_path.read_text(encoding="utf-8"))
    if contributor and not any(c.get("name") == contributor for c in contributors["contributors"]):
        contributors["contributors"].append({"name": contributor, "orcid": orcid})
        contributors_path.write_text(
            json.dumps(contributors, indent=2) + "\n", encoding="utf-8"
        )

    # 5. Rebuild the catalog.
    import build_catalog  # type: ignore

    build_catalog.main()

    print("\nCreated:")
    print(f"  {dest.relative_to(ROOT)}")
    print("\nMetadata updated. Next steps:")
    print("  1. Run: python scripts/validate_svgs.py")
    print("  2. Run: python scripts/generate_previews.py")
    print("  3. Commit and open a pull request (see CONTRIBUTING.md)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
