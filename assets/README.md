# SciSVG asset library

Reusable, validated SVG assets live in the category folders below this directory.

| Category | Subcategories | Status |
|---|---|---|
| `biology/` | cells, organelles, proteins, dna-rna, pathways, organisms | populated |
| `chemistry/` | molecules, reactions, glassware, instrumentation | populated |
| `bioinformatics/` | genomics, networks, machine-learning, workflows, databases | populated |
| `laboratory/` | equipment, workflows, consumables | populated |
| `general-science/` | — | populated |
| `medicine/` | anatomy, disease, clinical | open for contributions |

Assets here are distributed under **CC BY 4.0** unless explicitly stated
otherwise. Attribution to SciSVG is required:

> SciSVG — Saveena Solanki, CC BY 4.0, https://github.com/SaveenaSolanki/SciSVG

## Metadata convention

Each asset includes a `<title>`, a `<desc>`, and the attribution comment so the
gallery can display it properly:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" role="img" aria-labelledby="title desc">
  <title id="title">Asset Name</title>
  <desc id="desc">One short sentence describing the asset.</desc>
  <!-- SciSVG — Saveena Solanki, CC BY 4.0, https://github.com/SaveenaSolanki/SciSVG -->
</svg>
```

See [`CONTRIBUTING.md`](../CONTRIBUTING.md) for the full guidelines, including
the validation standard.
