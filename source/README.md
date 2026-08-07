# source/

Reserved for **editable master files** — the Illustrator/Inkscape originals
(`.ai`, `.svg`, `.xcf`, ...) behind complex assets.

Current SciSVG assets are already fully editable SVGs (named layers, no raster
content), so `assets/` doubles as the master for now. If you contribute an
asset from a native drawing tool and want to preserve the higher-fidelity
master alongside the optimized `assets/` version, place the master here with a
matching name, e.g.:

```text
source/biology/organelles/mitochondrion.svg
assets/biology/organelles/mitochondrion.svg   ← optimized, distributed
```

Masters in `source/` are NOT distributed by the gallery and are not run
through SVGO. Keep them out of `assets/`.
