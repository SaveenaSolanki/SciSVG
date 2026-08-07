# Contributing to SciSVG

Thank you for helping expand SciSVG. The goal is simple: **anyone should be
able to add a good scientific SVG without understanding the whole repository.**

## Quick start

```bash
# 1. Fork SciSVG and clone your fork
git clone https://github.com/<you>/SciSVG.git
cd SciSVG

# 2. Add your SVG with the contributor tool
python scripts/add_svg.py my_figure.svg

# 3. Check everything passes
python scripts/validate_svgs.py
python scripts/check_metadata.py
python scripts/check_duplicates.py
pytest -q

# 4. Commit and open a pull request
```

The contributor tool (`scripts/add_svg.py`) validates the file, asks for the
category, keywords, and your name, places the SVG in the right folder with a
kebab-case filename, records you in `metadata/contributors.json`, and rebuilds
the catalog.

## Asset requirements

- Submit SVG files only.
- Submit only original artwork or material you are authorised to release under CC BY 4.0.
- Keep vectors editable: no embedded raster images, no `<script>`, no external resources.
- Use a `viewBox` of `0 0 512 512` so assets render consistently in the gallery.
- Use lowercase kebab-case filenames: `mitochondrion-outline.svg`, not `Final2.svg`.
- Place the file in the most appropriate folder under `assets/`.
- Do not include copyrighted logos, journal artwork, proprietary icons, or third-party illustrations without explicit permission.

## Embedded metadata

Each SVG must carry a `<title>`, a short `<desc>`, and the attribution comment.
The catalog builder reads the title and description for gallery cards and search.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" role="img" aria-labelledby="title desc">
  <title id="title">Mitochondrion</title>
  <desc id="desc">Mitochondrion with inner membrane folds (cristae).</desc>
  <!-- SciSVG — Saveena Solanki, CC BY 4.0, https://github.com/SaveenaSolanki/SciSVG -->
</svg>
```

## Validation standard

Every contribution must pass `python scripts/validate_svgs.py`:

| Requirement | Rule |
|---|---|
| `viewBox` | Required (standard: `0 0 512 512`) |
| XML validity | Required |
| Raster / base64 images | Not allowed |
| External image URLs / resources | Not allowed |
| `<script>`, event handlers, `javascript:` | Not allowed |
| `<foreignObject>` | Not allowed |
| Duplicate IDs / broken references | Not allowed |
| Filename | lowercase kebab-case |
| Attribution comment (CC BY 4.0) | Required |
| `<title>` / `<desc>` | Recommended |

## Naming conventions

Duplicate concepts should use descriptive suffixes rather than numbers:

```text
mitochondrion-outline.svg
mitochondrion-detailed.svg
mitochondrion-flat.svg
```

not `mitochondrion1.svg` / `mitochondrion2.svg`.

## Optimization

Distributed SVGs are optimized with SVGO:

```bash
npm install
python scripts/optimize_svgs.py        # or: npm run optimize
```

`svgo.config.js` is configured to preserve the CC BY 4.0 attribution comments,
`<title>`, `<desc>`, and `viewBox`. Do not optimize your master file — keep it
in `source/` if you have an Illustrator/Inkscape original.

## Scientific review

Technical validation and scientific review are separate. A technically perfect
illustration can still be scientifically wrong. The PR template therefore asks
you to confirm that labels are verified, structure is not misrepresented, and
the artwork is your own. Assets start with `scientifically_reviewed: false`
and can be flagged for review in the issue tracker.

## Attribution

By contributing an SVG, you agree that the submitted asset may be distributed
under CC BY 4.0 and attributed to SciSVG and, where documented, you as the
contributor (with ORCID if you provide one).
