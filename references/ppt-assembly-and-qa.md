# Editable PowerPoint assembly and correction loop

Read this reference after `diagram.ir.json` passes semantic validation and its coordinate/debug SVG has been inspected. Load the Presentations skill and treat the IR as the single source of truth for object identity and geometry.

## Reconstruction contract

Use the draft as a layout reference. Build the final slide from independent objects:

- native rounded rectangles for panels and inner cards;
- native text boxes for every visible label;
- native arrows/connectors for data and control flow;
- native simple icons, nodes, axes, cluster boundaries, and mini charts only when their geometry remains unambiguous;
- separate embedded SVG/TikZ objects for geometry-sensitive scientific mechanisms, and true-alpha PNG images for real imagery, heatmaps, textures, or other raster scientific content, unless an opaque canvas is scientifically meaningful.

Never place the entire draft or SVG as a full-slide screenshot. A user must be able to move, recolor, resize, and rewrite the framework without editing a bitmap.

Each visually independent card or list item must be a separate background shape plus a separate text box. Each logical connector, including a multi-bend route, must be one editable PowerPoint connector, freeform polyline, or `custGeom` object. Never simulate one card set with a multiline text box or one polyline with separate line segments.

## Authoring sequence

1. Load the available **Presentations** skill and follow its required authoring, rendering, notes, and validation workflow.
2. Choose the slide size from the IR canvas and approved draft. Preserve their aspect ratio; do not independently select another layout ratio.
3. Resolve parent-relative frames to absolute canvas coordinates, then map them to slide coordinates by one uniform x/y scale. Do not estimate positions from the screenshot during assembly.
4. Render elements in parent and z-order. Keep connectors behind the modules they connect unless their IR z-order explicitly says otherwise.
5. Plan connector channels for the full slide, then connect the exact `from` and `to` ports and follow explicit waypoints. Do not replace a specified non-center connection with an auto-centered arrow. Map one IR connector to one PowerPoint object, even when it has several bends.
6. Use every IR element ID as the corresponding PowerPoint object name whenever the authoring backend permits it.
7. Insert image assets with byte-backed embedding, preserved aspect ratio, meaningful alt text, and no external path dependency. Honor `contain` or `cover`; reject unrequested stretching.
8. Put `[Sources]` notes on the slide for user assets, web assets, and non-trivial external claims. Generated subfigures may be described as generated specifically for the diagram.
9. Export the PPTX, render it, and enter the observable correction loop below rather than applying unrecorded visual nudges.

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
- Within the no-overflow, no-clipping, and no-occlusion limits, use the largest practical font size instead of conservatively small type. Set text colors for clear contrast against their actual panel fills, and verify the rendered contrast rather than assuming the theme default is readable.
- Set connector stroke widths and arrowhead sizes explicitly instead of accepting backend defaults. Main-flow arrows and important internal connectors should be proportionally bold and visibly directional at the full-slide scale, while remaining clear of labels and scientific content.
- Simple cluster boundaries and node groups are often clearer as native shapes than as generated images.
- Embedded scientific subfigures should resemble ordinary PowerPoint/Visio diagrams or MATLAB/Matplotlib exports. If an image looks like an elaborate AI infographic, regenerate it in a simpler approved style before insertion.
- Output cards should visually reuse the semantic color or miniature representation of the producing module.

## Observable correction loop

Read and execute [visual-qa-checklist.md](visual-qa-checklist.md). Do not treat this as a one-pass inspection.

1. **Render.** Export the actual PPTX to a full-slide PNG. Also produce enlarged crops for the primary subject, every dense connector junction, repeated-card region, feedback/trigger region, formula area, and complex scientific subfigure.
2. **Observe.** Inspect the whole-slide image at fit-to-page scale, then the enlarged regions, then trace every semantic connector class. Record visible evidence, not a generic “looks good”.
3. **Diagnose.** Assign every defect to one layer: `semantic hierarchy`, `IR layout`, `IR routing/style`, `object model`, `asset`, or `renderer`.
4. **Act.** Correct the owning layer. Change the algorithm plan or group hierarchy when the requested subject lacks prominence; change IR frames/constraints for alignment or overflow; change connector roles, channels, and waypoints for line confusion; split a false multiline-card text box into independent objects; replace segmented polylines with one object; edit only the asset for subfigure defects; correct renderer mappings for PowerPoint-specific drift.
5. **Verify.** Revalidate the IR, regenerate the debug overlay and PPTX, rerender the whole slide and affected crops, and rerun the checklist. Repeat until no blocking item remains.

Keep a concise defect log such as `region | visible evidence | layer | edit | verification`. This preserves decisions without relying on untracked visual nudges. Automated overflow and archive tests are necessary but never substitute for rendered visual inspection.

## Delivery gate

Deliver only when:

- `diagram.ir.json` passes schema, hierarchy, coordinate, port, and constraint validation;
- the coordinate/debug SVG has been inspected and agrees with the intended composition;
- the PPTX opens and passes archive/structure validation;
- the rendered slide matches the approved hierarchy and flow;
- all framework objects remain editable;
- every complex subfigure is embedded and self-contained;
- every draft region passes the regional fidelity comparison with no lower-information substitution;
- the user-designated primary subject is visually dominant and its input, processing, output, and constraint/destination paths are traceable;
- repeated cards use independent shape/text pairs, and every logical polyline remains one editable object;
- the whole-slide, regional zoom, semantic line-tracing, and editability sections of the visual QA checklist pass;
- the final visual review finds no remaining defect.
