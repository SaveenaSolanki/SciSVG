# SciSVG asset library

Reusable SVG assets live in the category folders below this directory:

- `biology/` — cells, organelles, tissues, physiology
- `chemistry/` — molecules, reactions, lab chemistry
- `genomics/` — DNA, RNA, chromosomes, sequencing
- `bioinformatics/` — networks, ML, workflows, omics
- `laboratory/` — instruments, tubes, plates, equipment
- `general/` — arrows, annotations, generic scientific elements

Assets in this directory are distributed under **CC BY 4.0** unless explicitly
stated otherwise. Attribution to SciSVG is required:

> SciSVG — Saveena Solanki, CC BY 4.0, https://github.com/SaveenaSolanki/SciSVG

## Metadata convention

Each asset should include a `<title>`, a `<desc>`, and the attribution comment
so the gallery can display it properly:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" role="img" aria-labelledby="title desc">
  <title id="title">Asset Name</title>
  <desc id="desc">One short sentence describing the asset.</desc>
  <!-- SciSVG — Saveena Solanki, CC BY 4.0, https://github.com/SaveenaSolanki/SciSVG -->
</svg>
```

See the repository [`CONTRIBUTING.md`](../CONTRIBUTING.md) for the full
guidelines.
