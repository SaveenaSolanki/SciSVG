# Contributing to SciSVG

Thank you for helping expand SciSVG.

## Asset requirements

- Submit SVG files only.
- Submit only original artwork or material you are authorised to release under CC BY 4.0.
- Keep vectors editable whenever practical; avoid embedding raster images.
- Remove unnecessary metadata and hidden layers.
- Use a `viewBox` of `0 0 512 512` so assets render consistently in the gallery.
- Prefer descriptive lowercase filenames separated by hyphens.
- Place the file in the most appropriate category folder.
- Do not include copyrighted logos, journal artwork, proprietary icons, or third-party illustrations without explicit permission.

## Embedded metadata

Each SVG should carry a `<title>`, a short `<desc>`, and the attribution comment.
The catalog builder (`scripts/build_catalog.py`) reads the title and description
for the gallery cards and search.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" role="img" aria-labelledby="title desc">
  <title id="title">Mitochondrion</title>
  <desc id="desc">Mitochondrion with inner membrane folds (cristae).</desc>
  <!-- SciSVG — Saveena Solanki, CC BY 4.0, https://github.com/SaveenaSolanki/SciSVG -->
</svg>
```

## Naming examples

```text
mitochondrion.svg
dna-double-helix.svg
protein-ligand-binding.svg
96-well-plate.svg
neural-network.svg
```

## Rebuilding the catalog

After adding or renaming assets, rebuild the catalog and commit it together with
the new SVGs:

```bash
python scripts/build_catalog.py
```

On `main`, the GitHub Action `.github/workflows/build-catalog.yml` does this
automatically.

## Attribution

By contributing an SVG to `library/`, you agree that the submitted asset may be
distributed under CC BY 4.0 and attributed to SciSVG and, where documented, the
individual contributor.
