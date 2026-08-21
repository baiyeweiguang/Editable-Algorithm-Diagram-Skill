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
│   ├── source/                  # editable TeX, TikZ, plotting code, and generation prompts
│   ├── media/                   # final SVG/PNG assets referenced uniformly by the IR
│   └── manifest.json            # stable id, media path, provenance, and target region
├── 03-ir/
│   ├── diagram.ir.json          # hierarchy, parent-relative frames, ports, z-order, constraints
│   └── layout-debug.svg         # coordinate grid, bounds, object ids, ports, routes, QA regions
├── 04-preview/
│   ├── round-01.png             # actual PowerPoint render
│   └── round-02.png             # keep accepted rounds instead of overwriting them
├── 05-ppt/
│   └── diagram-working.pptx
├── 06-qa/
│   ├── rendered-final.png
│   ├── regions/                 # final crops paired with 01-draft/regions
│   └── qa-notes.md
└── deliverable/
    └── diagram-final.pptx
```

Use stable semantic identifiers across crop names, source files, final media, IR `asset_id` values, element IDs, the manifest, and PowerPoint object names, for example `feature-pyramid`, `deformable-grid`, and `joint-loss`. Prefer names such as `02-assets/media/deformable-grid.svg` and `img-deformable-grid` over generic names such as `image3.svg`. Keep editable `.tex`, TikZ, or plotting sources through final acceptance.

Do not overwrite accepted intermediates during revision. For a hierarchy, position, size, spacing, route, or stacking problem, update `diagram.ir.json`, regenerate `layout-debug.svg`, and rebuild the affected objects or slide. For an asset-content problem, update only the media while preserving its IR frame. Keep every accepted PowerPoint render as a separate preview round. If the user requests all sources, package `00-source/` through `06-qa/` together with the final PPTX; otherwise deliver only the requested PPTX.
