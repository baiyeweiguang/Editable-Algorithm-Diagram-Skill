# Visual QA checklist for editable algorithm diagrams

Read this reference after rendering the actual PPTX. The overflow test, archive test, IR validator, and debug overlay are prerequisites, not substitutes for this checklist.

Prepare:

- one full-slide PNG viewed at fit-to-page scale;
- enlarged crops for the primary subject, every connector-dense junction, repeated-card region, feedback/trigger region, formula area, and complex scientific subfigure;
- the accepted draft or corresponding draft-region crops;
- a concise defect log: `region | visible evidence | layer | edit | verification`.

Any failed blocking item requires correction and rerendering.

## 1. Whole-slide thumbnail

- [ ] The user-designated subject, if any, has the highest or clearly intended visual weight; it is not an ordinary side box.
- [ ] The subject's input, core processing, output, and constraint/destination paths can be identified within a few seconds.
- [ ] The main chain and secondary branches are immediately distinguishable.
- [ ] Major modules form a stable reading order; no region is unintentionally crowded or empty.
- [ ] Text remains readable at fit-to-page scale, with sufficient contrast against the actual rendered background.
- [ ] Main-flow arrows are visibly thick enough and their arrowheads are recognizable without zooming.
- [ ] Connector classes do not visually merge with module borders or with each other.

## 2. Regional zoom inspection

Inspect every major module and all dense or repeated structures.

- [ ] No text crosses a border, clips, overflows, wraps unexpectedly, or hides behind another object.
- [ ] Enlarged fonts and strokes have not introduced new collisions or reduced internal padding.
- [ ] Every independent card, capsule, state item, or list item has its own background shape and its own text box.
- [ ] Each card text box shares the intended center or alignment axis with its background; editing one item does not shift another.
- [ ] Repeated cards have consistent dimensions, gaps, padding, font size, and baseline.
- [ ] Arrow paths do not cross labels, formulas, scientific content, or unrelated card interiors.
- [ ] Arrow endpoints land on the intended named ports at the target boundary.
- [ ] Parallel, perspective, grid, trajectory, and one-to-one node/edge relations remain geometrically coherent.
- [ ] SVG/PNG scientific subfigures are crisp, correctly cropped, not stretched, and preserve required transparency.
- [ ] Formulas and variables from the source or draft remain present and render as intended.
- [ ] Legends reuse the actual object's shape, fill, border, line weight, and dash pattern.

## 3. Connector-channel and semantic tracing

Trace each semantic class separately: main data flow, semantic/supplementary flow, trigger/control flow, feedback/validation flow, and failure/degradation flow when present.

For every class:

- [ ] Its start, end, meaning, and direction are unambiguous.
- [ ] Adjacent semantic classes differ in at least two of color, dash, direction, or spatial channel.
- [ ] Different classes do not share the same narrow corridor unless their separation remains obvious.
- [ ] A dashed module border cannot be mistaken for a dashed connector.
- [ ] Crossings and long detours are minimized; unavoidable crossings are visually explicit.
- [ ] Labels sit beside a clear segment and do not overlap the line or arrowhead.
- [ ] Hiding other classes mentally or in a debug render leaves a coherent route.

## 4. Semantic fidelity

- [ ] Every region depicts the same object and function as the approved draft or algorithm plan.
- [ ] No real image, scientific plot, formula, explicit mechanism, or complex subfigure has been replaced by a lower-information placeholder.
- [ ] Module order and arrow direction match the algorithm.
- [ ] No required input, output, branch, trigger, feedback, or constraint path is missing.
- [ ] Complex subfigures pass the human-authorship test: regular geometry, restrained visual vocabulary, and a style reproducible in PowerPoint/Visio, MATLAB/Matplotlib, or clean TikZ/SVG.
- [ ] No decorative dense network, glow, glass effect, isometric rendering, arbitrary shape, watermark, or accidental artifact remains.

## 5. Editability and object structure

- [ ] Titles, labels, module frames, and simple diagrams remain native editable PowerPoint objects.
- [ ] Each logical connector is exactly one editable connector/freeform/`custGeom` object, including all bends; it is not assembled from separate lines.
- [ ] Only the final endpoint of a logical connector carries its terminal arrowhead.
- [ ] Moving or resizing a repeated-card item does not require editing an unrelated item's text.
- [ ] Complex scientific subfigures remain separate named SVG/PNG objects with alt text and embedded bytes.
- [ ] Images preserve aspect ratio; no external file path is required.
- [ ] The slide is not a flattened background image, and important text is not baked into one.

When a polyline or object-model defect is suspected, inspect the PPTX XML or object tree: one logical route should correspond to one shape/connector object with all path points stored together.

## 6. Final pass

- [ ] The full-slide view passes after every regional correction; a local fix has not created a new global imbalance.
- [ ] All corrected regions were rerendered from the actual PPTX, not judged from source SVG or IR alone.
- [ ] The defect log has no unresolved blocking item.
- [ ] The final PowerPoint opens, passes structure/overflow validation, and remains readable in fit-to-page and Word-insertion contexts.
