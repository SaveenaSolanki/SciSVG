# Changelog

All notable changes to SciSVG are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-08-07

### Added

- Initial library of **30 editable SVG assets** across 6 categories:
  - Biology (cells, organelles, DNA/RNA)
  - Chemistry (molecules, reactions, glassware)
  - Bioinformatics (genomics, networks, machine learning, workflows)
  - Laboratory (equipment, consumables)
  - General Science (arrows, axes, icons)
- Category/subcategory structure under `assets/` with `metadata/categories.json`.
- Rich, searchable metadata schema (`metadata/assets.json`, generated).
- SVG validation tool with the library quality standard (`scripts/validate_svgs.py`).
- SVGO optimization pipeline (`scripts/optimize_svgs.py`, `svgo.config.js`).
- Preview generation (`scripts/generate_previews.py`, PNG/WebP, gitignored).
- Contributor CLI (`scripts/add_svg.py`) for painless asset submissions.
- Metadata and duplicate checks (`scripts/check_metadata.py`, `scripts/check_duplicates.py`).
- Test suite (`tests/test_svgs.py`).
- GitHub Actions: `validate-svg.yml`, `build-catalog.yml`, `deploy-pages.yml`.
- Issue templates (asset request, scientific error, bug report) and PR template.
- Dependabot configuration for Actions and npm.
- Community files: `CODE_OF_CONDUCT.md`, `SECURITY.md`, `ROADMAP.md`, `CHANGELOG.md`.
- Dual licensing: `LICENSE` (MIT, code) and `LICENSE-ASSETS` (CC BY 4.0, artwork).
- Interactive gallery at `website/` with search (Fuse.js), category filters,
  download, citation copying, and an asset detail view.

## [Unreleased]

- Repository banner is the official asset: `branding/scisvg-banner.png`
  ("SciSVG Scientific Asset Library Banner"); the editable vector banner
  remains at `branding/scisvg-banner.svg`.
- More assets across all categories, especially Medicine (open for contributions).
- Scientific review program and review badges.
- Zenodo DOI once a first stable release is tagged.
