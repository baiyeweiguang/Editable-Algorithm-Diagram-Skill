# Editable PowerPoint assembly and visual QA

Read this reference after `diagram.ir.json` passes semantic validation and its coordinate/debug SVG has been inspected. Load the Presentations skill and treat the IR as the single source of truth for object identity and geometry.

## Reconstruction contract

Use the draft as a layout reference. Build the final slide from independent objects:

- native rounded rectangles for panels and inner cards;
- native text boxes for every visible label;
- native arrows/connectors for data and control flow;
- native simple icons, nodes, axes, cluster boundaries, and mini charts only when their geometry remains unambiguous;
- separate embedded SVG/TikZ objects for geometry-sensitive scientific mechanisms, and true-alpha PNG images for real imagery, heatmaps, textures, or other raster scientific content, unless an opaque canvas is scientifically meaningful.

Never place the entire draft or SVG as a full-slide screenshot. A user must be able to move, recolor, resize, and rewrite the framework without editing a bitmap.

## Authoring sequence

1. Load the available **Presentations** skill and follow its required authoring, rendering, notes, and validation workflow.
2. Choose the slide size from the IR canvas and approved draft. Preserve their aspect ratio; do not independently select another layout ratio.
3. Resolve parent-relative frames to absolute canvas coordinates, then map them to slide coordinates by one uniform x/y scale. Do not estimate positions from the screenshot during assembly.
4. Render elements in parent and z-order. Keep connectors behind the modules they connect unless their IR z-order explicitly says otherwise.
5. Connect the exact `from` and `to` ports and follow explicit waypoints. Do not replace a specified non-center connection with an auto-centered arrow.
6. Use every IR element ID as the corresponding PowerPoint object name whenever the authoring backend permits it.
7. Insert image assets with byte-backed embedding, preserved aspect ratio, meaningful alt text, and no external path dependency. Honor `contain` or `cover`; reject unrequested stretching.
8. Put `[Sources]` notes on the slide for user assets, web assets, and non-trivial external claims. Generated subfigures may be described as generated specifically for the diagram.
9. Export the PPTX, render it, and revise the IR rather than applying unrecorded visual nudges when geometry changes.

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

- rendered object bounds match the accepted IR frames within a small explicit tolerance;
- parent-relative placement has been flattened correctly, so moving a group in the IR does not change its children's internal offsets;
- panels and cards align to a grid;
- gutters and outer margins are balanced;
- arrows start and end at the named IR ports, follow their intended waypoints, and do not cross labels;
- no object extends outside the slide;
- no image is distorted or cropped through important content.

### Visual quality

- complex subfigures are crisp at their final displayed size;
- every raster subfigure has a genuine alpha channel where expected; no opaque white rectangle, baked checkerboard, light halo, clipped pale trace, or accidentally removed enclosed white content remains;
- inspect transparent subfigures on the actual panel fill and, when edges are ambiguous, on a contrasting temporary background before delivery;
- every scientific subfigure passes the human-authorship test: regular geometry, restrained colors, limited meaningful elements, and a visual language reproducible in PowerPoint/Visio or MATLAB/Matplotlib;
- no dense decorative network, glow, glass effect, isometric rendering, excessive micro-detail, arbitrary shape, or unexplained connection remains;
- line weights and color saturation are consistent; important connectors are visibly thick enough and their arrowheads remain easy to distinguish at fit-to-page scale;
- the slide remains legible when inserted into Word or viewed at fit-to-page scale; where unused space permits, text has been enlarged, and every text color has sufficient contrast with its rendered background;
- no draft artifact, watermark, accidental letter, or external-link placeholder remains.

Run the presentation overflow/structure test provided by the Presentations skill. Fix every unintended overlap, overflow, clipping, or wrap, rerender, and inspect again. The absence of a test error does not replace visual review.

## Delivery gate

Deliver only when:

- `diagram.ir.json` passes schema, hierarchy, coordinate, port, and constraint validation;
- the coordinate/debug SVG has been inspected and agrees with the intended composition;
- the PPTX opens and passes archive/structure validation;
- the rendered slide matches the approved hierarchy and flow;
- all framework objects remain editable;
- every complex subfigure is embedded and self-contained;
- every draft region passes the regional fidelity comparison with no lower-information substitution;
- the final visual review finds no remaining defect.
