# Deterministic pptfast generation and review

Use this reference for ordinary algorithm-diagram production. It overrides the retained upstream pptfast guide only where this composite skill explicitly adds scientific-asset fidelity, regional visual comparison, and a recorded Presentation finalization pass.

## Operating contract

- Use standard pptfast IR directly. Do not invent an `AlgorithmDiagramIR` sidecar.
- Read the current CLI schema at the start of each pptfast session; schema output outranks remembered fields.
- Infer the target layout visually from the approved draft: visible regions, relative proportions, ordering, hierarchy, branches, formulas, legends, inputs, and outputs.
- Fix `seed` and explicitly pin `layout` when a selected composition must remain stable.
- Treat every externally prepared SVG or raster subfigure as one semantic image asset. Do not create different IR content types for formulas, plots, OpenTikZ diagrams, or generated scientific images.
- Keep pptfast as the primary layout and rendering path. Use the Presentations skill only after the pptfast preview is accepted and only for unsupported finalization.

The bundled launchers pin the tested CLI version:

```bash
bash <skill-dir>/scripts/pptfast/run.sh <args>                                       # macOS/Linux
powershell -ExecutionPolicy Bypass -File <skill-dir>\scripts\pptfast\run.ps1 <args> # Windows
```

If the upstream guide shows another invocation, use these bundled launchers instead. Run `doctor --json` when the launcher or CLI behaves unexpectedly. An exit code of 78 means no compatible JavaScript runtime is available; report the launcher's structured diagnosis rather than retrying blindly.

## Asset preparation

Use stable semantic IDs across the draft crop, source asset, pptfast asset, IR `asset_id`, and final PowerPoint object name.

The pinned pptfast 0.20.0 external asset pipeline accepts PNG, JPEG, GIF, and WebP. It uses SVG internally for its own render chain, but an external SVG source is not accepted directly through `assets.images`. Keep the SVG as the final source and create a same-aspect PNG preview for pptfast:

```text
02-assets/
├── sources/
│   ├── deformable-grid.svg
│   ├── attention-formula.svg
│   └── infrared-sequence.png
├── pptfast/
│   ├── deformable-grid.png
│   ├── attention-formula.png
│   └── infrared-sequence.png
└── manifest.json
```

The preview PNG must use the SVG's exact viewBox/aspect ratio, remove accidental outer whitespace, and preserve the intended transparent or opaque background. Raster sources can be reused directly. Record the relationship in `manifest.json`, including stable ID, source path, pptfast path, draft-region path, source/license or generation prompt, and whether final vector replacement is required.

Use `asset-brief` after the first valid IR render to obtain the actual image frame and crop behavior. If the final asset is regenerated to that brief, preserve the same asset ID and rerender the unchanged IR.

## IR and CLI loop

For the normal one-slide task, a single IR file is sufficient. Run the following through the bundled launcher:

```bash
pptfast schema
pptfast themes --json
pptfast narratives --json
pptfast validate deck.ir.json
pptfast asset-brief deck.ir.json
pptfast audit deck.ir.json
pptfast preview deck.ir.json -o 04-preview/round-01/ --html
pptfast render deck.ir.json -o 05-ppt/pptfast-base.pptx
```

Do not treat deterministic as synonymous with correct. A fixed IR and seed reproduce the same output, but the Agent must still compare the preview with the draft. Keep accepted rounds rather than overwriting them so a later regression is visible.

## Visual evaluation and issue routing

Run pptfast `audit` and visual regional comparison; neither replaces the other. Audit catches mechanical geometry and content-loss defects. Regional comparison catches scientific-semantic loss, wrong proportions, incorrect subfigures, missing formulas, or a mismatch with the approved draft.

Route each finding to exactly one primary layer:

| Finding | Corrective action |
|---|---|
| Wrong component, module order, hierarchy, layout, density, fit, or text budget | Edit IR, then validate/audit/preview/render again |
| Wrong crop, transparency, scientific content, padding, or asset aspect ratio | Edit the asset, keep the IR stable, then rerender |
| Unsupported external SVG embedding, PowerPoint-only rendering defect, or correction that cannot be represented in pptfast IR | Accept the base preview first, then use the recorded Presentation finalization pass |

Do not use the Presentations skill to compensate for an IR problem. A correction that moves or resizes several modules belongs in the IR loop.

## Recorded Presentation finalization

Apply finalization to a copy, keeping `pptfast-base.pptx` intact. For each SVG source represented by a preview PNG:

1. Identify the corresponding image object through its stable asset/object name.
2. Record its slide, x/y/w/h, crop, rotation, z-order, and alt text.
3. Replace only the picture payload with the source SVG while preserving those geometry values.
4. Record the operation in `06-finalization/finalization.json` or a replayable task script.
5. Apply any other pptfast-unrepresentable correction as another explicit, narrowly scoped operation.

The finalization record is part of the reproducibility contract: after any IR revision, regenerate `pptfast-base.pptx` and replay finalization instead of reproducing edits by eye.

After finalization, render the actual final PPTX to a full-resolution image, rerun the Presentations skill's overflow/structure test, and repeat the draft-versus-final regional comparison. A clean pptfast preview does not prove that PowerPoint rendered the post-finalized deck correctly.
