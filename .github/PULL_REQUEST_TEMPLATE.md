# Pull Request Checklist

Thanks for contributing to SciSVG. Before submitting, please confirm:

## Artwork and rights

- [ ] I created this artwork, or I have the legal right to contribute it.
- [ ] I agree to release the asset under **CC BY 4.0**.
- [ ] No copyrighted third-party artwork, logos, or journal figures were traced or copied.
- [ ] The SVG is original and does not embed raster images, scripts, or external resources.

## Technical checks

- [ ] The SVG passes automated validation: `python scripts/validate_svgs.py`.
- [ ] The SVG has a `viewBox` of `0 0 512 512`, a `<title>`, a `<desc>`, and the SciSVG attribution comment.
- [ ] The filename follows lowercase kebab-case (e.g. `mitochondrion-outline.svg`, not `Final2.svg`).
- [ ] The asset is placed in the correct category/subcategory under `assets/`.
- [ ] Metadata is up to date: `python scripts/build_catalog.py` was run.

## Scientific checks

- [ ] Scientific labels have been verified against a reliable source.
- [ ] The illustration does not intentionally misrepresent scale or structure.
- [ ] I have described the scientific context in the PR description.

## PR description

Please include:
- What the asset depicts and where it should be used.
- The category/subcategory it belongs to.
- Any scientific references used to verify accuracy.
