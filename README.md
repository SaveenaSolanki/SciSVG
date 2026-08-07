<p align="center">
  <img src="branding/scisvg-banner.svg" alt="SciSVG — editable scientific SVG assets" width="100%">
</p>

# SciSVG

**Free, editable SVG assets for scientific figures, presentations, posters, teaching, and publications.**

SciSVG is an open scientific illustration library designed to make clean, reusable vector graphics easy to find, edit, and cite. Assets are organised by scientific domain and can be previewed in the online gallery or downloaded directly from this repository.

> **Free to use and modify. Attribution is required.**

## Browse the library

Once GitHub Pages is enabled for the `docs/` folder, the interactive gallery will provide search, category filtering, previews, direct SVG downloads, and one-click citation copying.

**Gallery:** `https://saveenasolanki.github.io/SciSVG/`

## Library categories

| Category | Folder | Examples |
|---|---|---|
| Biology | `library/biology/` | cells, tissues, organelles, pathways |
| Chemistry | `library/chemistry/` | molecules, reactions, lab chemistry |
| Genomics | `library/genomics/` | DNA, RNA, chromosomes, sequencing |
| Bioinformatics | `library/bioinformatics/` | networks, ML, workflows, omics |
| Laboratory | `library/laboratory/` | instruments, tubes, plates, equipment |
| General | `library/general/` | arrows, annotations, generic scientific elements |

## How to use an SVG

1. Browse the gallery or the `library/` folders.
2. Download the `.svg` file.
3. Edit it in Illustrator, Inkscape, Figma, PowerPoint, Keynote, Affinity Designer, or another SVG-compatible application.
4. Add attribution to SciSVG in the figure legend, acknowledgements, slide footer, website, or references as appropriate.

## Required attribution

All SVG assets under `library/` are released under **Creative Commons Attribution 4.0 International (CC BY 4.0)** unless a file explicitly states otherwise.

A compact attribution is sufficient for slides, websites, posters, and figures:

> **SciSVG — Saveena Solanki, CC BY 4.0, https://github.com/SaveenaSolanki/SciSVG**

For academic manuscripts, please cite:

> **Solanki, S. (2026). SciSVG: Editable scientific SVG assets. GitHub. https://github.com/SaveenaSolanki/SciSVG**

GitHub also exposes citation metadata from [`CITATION.cff`](CITATION.cff). If a DOI is added through Zenodo later, the DOI-based citation can replace the repository citation.

## What you may do

Under CC BY 4.0, you may use, copy, redistribute, modify, recolour, combine, and adapt SciSVG assets, including for commercial work, provided appropriate attribution is given.

## Adding new SVGs

Place each SVG in the most relevant folder under `library/`. Use descriptive lowercase filenames with hyphens, for example:

```text
library/biology/mitochondrion.svg
library/genomics/dna-double-helix.svg
library/laboratory/96-well-plate.svg
```

After a push to `main`, the included GitHub Action rebuilds `docs/catalog.json`, so the asset appears automatically in the gallery.

## Repository structure

```text
SciSVG/
├── README.md
├── CITATION.cff
├── LICENSE
├── LICENSE-CODE.md
├── CONTRIBUTING.md
├── branding/
│   └── scisvg-banner.svg
├── library/
│   ├── biology/
│   ├── chemistry/
│   ├── genomics/
│   ├── bioinformatics/
│   ├── laboratory/
│   └── general/
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

- **SVG assets in `library/`: CC BY 4.0 — attribution required.**
- **Gallery and utility code in `docs/` and `scripts/`: MIT License.**

See [`LICENSE`](LICENSE) and [`LICENSE-CODE.md`](LICENSE-CODE.md).

---

<p align="center"><strong>SciSVG</strong> — open scientific vectors, designed to be reused and cited.</p>
