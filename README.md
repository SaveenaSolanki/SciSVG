<p align="center">
  <img src="branding/scisvg-banner.svg" alt="SciSVG — editable scientific SVG assets" width="100%">
</p>

# SciSVG

**Open scientific vectors for figures, presentations, and publications.**

**Free to use. Free to modify. Attribution required.**

<p>
  <a href="LICENSE"><img alt="SVG assets: CC BY 4.0" src="https://img.shields.io/badge/assets-CC%20BY%204.0-3157a4"></a>
  <a href="LICENSE-CODE.md"><img alt="Code: MIT" src="https://img.shields.io/badge/code-MIT-2a7b70"></a>
  <a href="CITATION.cff"><img alt="Cite this repository" src="https://img.shields.io/badge/cite-this%20repository-b26b36"></a>
</p>

SciSVG is an open scientific illustration library of clean, editable vector graphics — designed to be found, edited, and cited. Assets are organised by scientific domain and can be previewed in the online gallery or downloaded directly from this repository.

## Browse the library

The interactive gallery provides search, category filtering, live SVG previews, direct SVG downloads, and one-click citation copying.

**Gallery:** <https://saveenasolanki.github.io/SciSVG/>

## What's inside

| Category | Folder | Assets |
|---|---|---|
| Biology | [`library/biology/`](library/biology/) | mitochondrion, cell membrane, animal cell, neuron, ribosome |
| Chemistry | [`library/chemistry/`](library/chemistry/) | protein–ligand binding, benzene ring, Erlenmeyer flask, peptide bond, reaction arrow |
| Genomics | [`library/genomics/`](library/genomics/) | DNA double helix, chromosome, plasmid, gene structure, sequencing reads |
| Bioinformatics | [`library/bioinformatics/`](library/bioinformatics/) | neural network, workflow pipeline, heatmap, sequence alignment, phylogenetic tree |
| Laboratory | [`library/laboratory/`](library/laboratory/) | 96-well plate, microscope, test tube rack, micropipette, petri dish |
| General | [`library/general/`](library/general/) | arrow right, curved arrow, axes, magnifier, layers |

Every asset is a hand-structured, editable SVG (no raster content) with a `512×512` `viewBox`, named layers, and embedded `<title>`/`<desc>` metadata that also powers gallery search.

## How to use an SVG

1. Browse the gallery or the `library/` folders.
2. Download the `.svg` file.
3. Edit it in Illustrator, Inkscape, Figma, PowerPoint, Keynote, Affinity Designer, or any SVG-compatible application.
4. Add attribution to SciSVG in the figure legend, acknowledgements, slide footer, website, or references as appropriate.

## Required attribution

All SVG assets under `library/` (and the banner under `branding/`) are released under **Creative Commons Attribution 4.0 International (CC BY 4.0)** unless a file explicitly states otherwise.

A compact attribution is sufficient for slides, websites, posters, and figures:

> **SciSVG — Saveena Solanki, CC BY 4.0, https://github.com/SaveenaSolanki/SciSVG**

For academic manuscripts, please cite:

> **Solanki, S. (2026). SciSVG: Editable scientific SVG assets. GitHub. https://github.com/SaveenaSolanki/SciSVG**

GitHub also exposes citation metadata from [`CITATION.cff`](CITATION.cff). If a DOI is added through Zenodo later, the DOI-based citation can replace the repository citation.

## What you may do

Under CC BY 4.0, you may use, copy, redistribute, modify, recolour, combine, and adapt SciSVG assets, including for commercial work, provided appropriate attribution is given.

## Adding new SVGs

1. Place each SVG in the most relevant folder under `library/`.
2. Use descriptive lowercase filenames separated by hyphens, e.g. `library/biology/mitochondrion.svg`.
3. Include a `<title>` and `<desc>` inside the SVG, plus the attribution comment:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
  <title id="title">Mitochondrion</title>
  <desc id="desc">Mitochondrion with inner membrane folds (cristae).</desc>
  <!-- SciSVG — Saveena Solanki, CC BY 4.0, https://github.com/SaveenaSolanki/SciSVG -->
</svg>
```

4. Push to `main`. The included GitHub Action ([`.github/workflows/build-catalog.yml`](.github/workflows/build-catalog.yml)) runs `scripts/build_catalog.py` and updates `docs/catalog.json`, so the asset appears automatically in the gallery. You can also run the script locally: `python scripts/build_catalog.py`.

## Repository structure

```text
SciSVG/
├── README.md
├── CITATION.cff
├── LICENSE               ← CC BY 4.0 for SVG artwork
├── LICENSE-CODE.md       ← MIT for gallery and utility code
├── CONTRIBUTING.md
├── branding/
│   └── scisvg-banner.svg
├── library/
│   ├── biology/          ← 5 assets
│   ├── chemistry/        ← 5 assets
│   ├── genomics/         ← 5 assets
│   ├── bioinformatics/   ← 5 assets
│   ├── laboratory/       ← 5 assets
│   └── general/          ← 5 assets
├── scripts/
│   └── build_catalog.py
├── docs/
│   ├── index.html
│   ├── style.css
│   ├── app.js
│   └── catalog.json
└── .github/workflows/
    └── build-catalog.yml
```

## Contributing

Contributions are welcome. Please read [`CONTRIBUTING.md`](CONTRIBUTING.md) before submitting new assets. Contributors should submit only artwork they created themselves or artwork they have the legal right to release under CC BY 4.0.

## License

- **SVG artwork in `library/` and `branding/`: CC BY 4.0 — attribution required.** See [`LICENSE`](LICENSE).
- **Gallery and utility code in `docs/` and `scripts/`: MIT License.** See [`LICENSE-CODE.md`](LICENSE-CODE.md).

---

<p align="center"><strong>SciSVG</strong> — open scientific vectors, designed to be reused and cited.</p>
