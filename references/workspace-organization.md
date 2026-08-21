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
│   ├── svg/                     # TikZ/OpenTikZ and geometry-sensitive diagrams
│   ├── raster/                  # generated or sourced PNGs and transparency-ready assets
│   ├── tex/                     # formula and custom TikZ sources
│   └── manifest.json            # asset id, source, license, prompt, and target region
├── 03-ppt/
│   └── diagram-working.pptx
├── 04-qa/
│   ├── rendered-slide.png
│   ├── regions/                 # final crops paired with 01-draft/regions
│   └── qa-notes.md
└── deliverable/
    └── diagram-final.pptx
```

Use stable semantic identifiers across crop names, asset files, the manifest, and PowerPoint object names, for example `feature-pyramid`, `deformable-grid`, and `joint-loss`. Prefer names such as `02-assets/svg/deformable-grid.svg` and `img-deformable-grid` over generic names such as `image3.svg`. Keep editable `.tex` sources beside their derived SVGs through final acceptance.

Do not overwrite accepted intermediates during revision. Update only the relevant asset and PPT object, then regenerate the corresponding QA crop. If the user requests all sources, package `00-source/` through `04-qa/` together with the final PPTX; otherwise deliver only the requested PPTX.
