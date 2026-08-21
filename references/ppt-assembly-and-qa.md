# Presentation finalization and visual QA

Read this reference only after the pptfast preview has been accepted and either a pptfast-unrepresentable correction is required or the final PPTX needs PowerPoint-level validation. Load the Presentations skill at that point. Do not bypass the pptfast IR loop for ordinary layout changes.

## Finalization boundary

Keep `pptfast-base.pptx` unchanged. Apply finalization to a copy and record every operation so it can be replayed after an IR revision. Appropriate operations include replacing a same-aspect preview PNG with its source SVG, correcting a PowerPoint-only rendering defect, adding required object metadata, or making a narrowly scoped adjustment that pptfast cannot represent.

Do not use this stage to rearrange several modules, change the information hierarchy, repair content density, or compensate for a poor component/layout choice. Return those issues to the IR, rerun pptfast, accept the new preview, and then replay finalization.

## Reconstruction contract

Use the accepted pptfast deck as the editable base and the draft as the fidelity reference. Preserve its independent objects:

- native rounded rectangles for panels and inner cards;
- native text boxes for every visible label;
- native arrows/connectors for data and control flow;
- native simple icons, nodes, axes, cluster boundaries, and mini charts only when their geometry remains unambiguous;
- separate embedded SVG/TikZ objects for geometry-sensitive scientific mechanisms, and true-alpha PNG images for real imagery, heatmaps, textures, or other raster scientific content, unless an opaque canvas is scientifically meaningful.

Never place the entire draft or a full-slide SVG as a screenshot. A user must be able to move, recolor, resize, and rewrite the framework without editing a bitmap.

## Authoring sequence

1. Load the available **Presentations** skill and follow its editing, rendering, notes, and validation workflow.
2. Copy the accepted `pptfast-base.pptx` to the working final deck.
3. Resolve each target through its stable asset/object name; do not select an object by approximate visual position when a semantic ID is available.
4. For SVG replacement, preserve the preview object's x/y/w/h, crop, rotation, z-order, alt text, and aspect ratio. The SVG source and preview PNG must share the same viewBox ratio and visible bounds.
5. Apply only the recorded narrow corrections. Store their target, old/new asset, geometry, and rationale in the task finalization manifest or replay script.
6. Keep related objects named consistently, for example `panel-motion`, `card-attention`, `img-camera`, and `label-output-state`.
7. Insert images with byte-backed embedding, meaningful alt text, and no external path dependency.
8. Preserve or add `[Sources]` notes for user assets, web assets, OpenTikZ items, and non-trivial external claims.
9. Export the final PPTX only after rendering and correction.

## Layout rules learned from reconstruction

- Allocate panel width by internal complexity, not evenly. A module with four mechanisms needs more width than a simple input or output stage.
- Use a consistent header band and card padding. Keep all module titles aligned to a common baseline.
- Keep arrows outside panel borders except for deliberate internal flow arrows.
- Use one color family per major stage and neutral white inner cards; color is for grouping, not decoration.
- Crop generated images before insertion. Large white margins make an otherwise correct subfigure appear tiny.
- Do not use an opaque white subfigure canvas to cover a tinted module panel. The panel fill should remain visible through the transparent outer region.
- Do not stretch images. Use contain/cover intentionally and inspect the crop.
- Put text above or beside the subfigure, not baked into it.
- Reduce words before reducing font size. Avoid unexpected three-line wrapping in narrow module headers.
- Simple cluster boundaries and node groups are often clearer as native shapes than as generated images.
- Embedded scientific subfigures should resemble ordinary PowerPoint/Visio diagrams or MATLAB/Matplotlib exports. If an image looks like an elaborate AI infographic, regenerate it in a simpler approved style before insertion.
- Output cards should visually reuse the semantic color or miniature representation of the producing module.

## Mandatory visual QA loop

Render every slide to PNG at full-slide resolution and inspect it individually. A contact sheet alone is insufficient.

Check all of the following:

### Regional fidelity and semantics

- crop or isolate corresponding regions from the draft and rendered slide, then compare every major module, complex subfigure, formula/loss area, legend, branch, input, and output;
- each region depicts the same object and retains its essential information; no real image, formula, mechanism, or scientific plot has been replaced by a lower-information placeholder;
- formulas and variables present in the source or draft remain present unless the user explicitly removed them;
- legend markers reuse the actual object's shape, fill, border, and line style;
- perspective, parallelism, collinearity, grids, and one-to-one node/edge relations remain mathematically coherent in the rendered PowerPoint;
- module order and arrow direction match the algorithm plan;
- no required input, branch, or output is missing;
- subfigures depict the claimed mechanism rather than a generic placeholder;
- data-flow and control-flow line styles are consistent when both exist.

### Typography

- all Chinese text is accurate and uses a compatible font;
- no title wraps unexpectedly;
- no text is clipped, shrunk to unreadability, or hidden behind an image;
- repeated labels use consistent size and weight.

### Geometry

- panels and cards align to a grid;
- gutters and outer margins are balanced;
- arrows touch the intended modules without crossing labels;
- no object extends outside the slide;
- no image is distorted or cropped through important content.

### Visual quality

- complex subfigures are crisp at their final displayed size;
- every raster subfigure has a genuine alpha channel where expected; no opaque white rectangle, baked checkerboard, light halo, clipped pale trace, or accidentally removed enclosed white content remains;
- inspect transparent subfigures on the actual panel fill and, when edges are ambiguous, on a contrasting temporary background before delivery;
- every scientific subfigure passes the human-authorship test: regular geometry, restrained colors, limited meaningful elements, and a visual language reproducible in PowerPoint/Visio or MATLAB/Matplotlib;
- no dense decorative network, glow, glass effect, isometric rendering, excessive micro-detail, arbitrary shape, or unexplained connection remains;
- line weights and color saturation are consistent;
- the slide remains legible when inserted into Word or viewed at fit-to-page scale;
- no draft artifact, watermark, accidental letter, or external-link placeholder remains.

Run the presentation overflow/structure test provided by the Presentations skill. Fix every unintended overlap, overflow, clipping, or wrap, rerender, and inspect again. The absence of a test error does not replace visual review.

## Delivery gate

Deliver only when:

- the PPTX opens and passes archive/structure validation;
- the rendered slide matches the approved hierarchy and flow;
- all framework objects remain editable;
- every complex subfigure is embedded and self-contained;
- every draft region passes the regional fidelity comparison with no lower-information substitution;
- the final visual review finds no remaining defect.
