# SciSVG Roadmap

## V1 — Library foundation (current)

- [x] Standardized `assets/<category>/<subcategory>/` layout with rich metadata
- [x] Dual licensing: CC BY 4.0 artwork, MIT code
- [x] Automated SVG validation (security + quality), metadata and duplicate checks
- [x] SVGO optimization pipeline with attribution-preserving config
- [x] Preview generation (PNG/WebP) for releases and the site
- [x] Searchable GitHub Pages gallery (search, filters, download, citation, detail view)
- [x] CI: validation, catalog build, Pages deploy; issue/PR templates; dependabot
- [x] Citation support (CITATION.cff), attribution guidance

## V1.1 — Grow the library

- [ ] Expand asset coverage in every category, prioritizing Medicine (anatomy,
      disease, clinical), Biology pathways and proteins, and Chemistry instrumentation
- [ ] Scientific review program: community reviewers approve assets and flip
      `scientifically_reviewed` to true, earning the SciSVG Verified badge
- [ ] Release-based preview bundles (PNG 1024/2048, WebP) attached to GitHub Releases
- [ ] Zenodo DOI via GitHub Releases for formal citation

## V2 — Ecosystem

- [ ] `scisvg` Python package (`pip install scisvg`) with a CLI:
      `scisvg search mitochondria`, `scisvg get biology/organelles/mitochondrion`
- [ ] `scisvg` Python API: `from scisvg import get_svg`
- [ ] Inkscape/Illustrator export scripts and asset templates
- [ ] Contributor gallery page crediting every contributor (with ORCID)
- [ ] Automated syntax/semantic checks for labels (e.g., Greek letters, chemical formulas)

## Non-goals

- SciSVG is a source of *editable* schematics for communication, not a source of
  publication-quality anatomical atlases or exact-to-scale molecular structures.
  Assets are schematic and should be adapted for the user's context.
