# Advisory workspace organization

Use this layout when an algorithm-diagram task creates several intermediate files or may require later element-level revision. It is recommended rather than mandatory; adapt it to the available workspace and do not create empty directories unnecessarily.

```text
diagram-work/
├── 00-source/
│   ├── algorithm.md
│   └── references/              # user references and source URLs
├── 01-draft/
│   ├── layout-draft.png
│   └── regions/                 # numbered crops used as subfigure references
├── 02-assets/
│   ├── sources/                 # final SVG/PNG sources plus editable TeX/TikZ sources
│   ├── pptfast/                 # pptfast-compatible PNG/JPEG/GIF/WebP assets
│   └── manifest.json            # stable id, source, preview, provenance, target region
├── 03-ir/
│   └── deck.ir.json             # standard pptfast IR; no separate diagram IR
├── 04-preview/
│   ├── round-01/                # deterministic pptfast SVG/HTML preview
│   └── round-02/                # keep accepted rounds instead of overwriting them
├── 05-ppt/
│   └── pptfast-base.pptx        # untouched result of the accepted IR
├── 06-finalization/
│   ├── finalization.json        # replayable SVG replacement and narrow PPT fixes
│   └── apply-finalization.*     # create only when a task needs deterministic patching
├── 07-qa/
│   ├── rendered-final.png
│   ├── regions/                 # final crops paired with 01-draft/regions
│   └── qa-notes.md
└── deliverable/
    └── diagram-final.pptx
```

Use stable semantic identifiers across crop names, source assets, pptfast preview assets, IR `asset_id` values, the manifest, and PowerPoint object names, for example `feature-pyramid`, `deformable-grid`, and `joint-loss`. Prefer names such as `02-assets/sources/deformable-grid.svg`, `02-assets/pptfast/deformable-grid.png`, and `img-deformable-grid` over generic names such as `image3.svg`. Keep editable `.tex` or TikZ sources beside their derived SVGs through final acceptance.

Do not overwrite accepted intermediates during revision. For an IR problem, create a new preview round and regenerate `pptfast-base.pptx`. For an asset problem, update only the asset and rerender the same IR. For a recorded finalization problem, update and replay only that operation. If the user requests all sources, package `00-source/` through `07-qa/` together with the final PPTX; otherwise deliver only the requested PPTX.
