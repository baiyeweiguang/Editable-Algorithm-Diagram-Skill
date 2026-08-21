---
name: algorithm-diagram-ppt
description: Turn a raw academic or engineering algorithm description into a one-slide editable PowerPoint architecture or flow diagram, first asking the user to choose a detailed or concise content mode, then generating a layout draft, preparing faithful OpenTikZ/LaTeX/raster assets, describing the full Visio/Illustrator-style composition in a semantic diagram IR with explicit hierarchy and coordinates, and rebuilding and visually validating the slide through the Presentations workflow. Use for algorithm framework, technical route, system architecture, or execution-flow diagrams requested as editable PPT/PPTX; do not use for ordinary multi-slide decks or simple text-only flowcharts.
---

# Editable Algorithm Diagram PPT

Create a polished algorithm figure whose framework remains editable in PowerPoint. The generated layout draft is a visual blueprint, not the deliverable.

## Required mode selection

Before rewriting the algorithm or calling image generation, actively ask the user to choose one of these modes:

1. **详细内容版（完整生图 Prompt）** — richer module internals and more scientific subfigures; best for project applications, technical reports, and cases where the mechanism must be shown clearly.
2. **简洁版（简短 Prompt）** — fewer internal elements, stronger visual hierarchy, larger effective text and subfigure areas; best for slides, compact Word figures, and fast overview communication.

Ask in the user's language. For a Chinese request, use a concise question such as:

> 请选择需要的绘图版本：
>
> 1. 详细内容版：使用完整生图 Prompt，保留更多模块内部机制与科研子图。
> 2. 简洁版：使用简短 Prompt，只保留核心数据流和关键机制。

This is a blocking choice: do not generate the layout draft until the user answers. If the interface provides a compact user-choice control, present these two options with a free-text alternative; otherwise ask in ordinary chat. If the user already explicitly requested a detailed/full or concise/compact version, honor that choice without asking again. If the user requests both, generate two separate drafts and PPTX deliverables unless they ask for one combined file. If the user delegates the choice, use detailed mode for proposals or technical reports and concise mode for presentation or overview use.

## Default interpretation

After the user selects a mode, the raw algorithm description is normally sufficient. Unless the user specifies otherwise, assume:

- one landscape slide suitable for a proposal, paper, or Word insertion;
- horizontal left-to-right data flow with an output strip when useful;
- white background, thin dark arrows, rounded rectangles, low-saturation pastel module colors;
- concise Chinese labels when the source is Chinese;
- no 3D decoration, drop shadows, glossy gradients, poster styling, or dense prose.

Apart from the required mode selection, ask only when another missing choice materially changes the result, such as multiple incompatible algorithms or an explicitly required house template.

## Workflow

1. **Select the content mode.** Ask the required detailed-versus-concise question unless the user has already made the choice.
2. **Extract the drawable algorithm for the selected mode.** Identify inputs, major modules, internal mechanisms, cross-module data flow, control flow, and outputs. Remove background prose, derivations, and implementation details that do not belong in the figure. The concise mode applies a stricter information budget.
3. **Design and generate a layout draft.** Read [references/prompt-rewriting.md](references/prompt-rewriting.md). Use the full prompt only for detailed mode and the compact prompt only for concise mode; do not automatically generate both. With OpenAI image generation, use GPT-Image2 or the current built-in image tool backed by it. Generate a draft that establishes hierarchy, proportions, palette, and subfigure placement. For jobs that create several intermediate assets, also read [references/workspace-organization.md](references/workspace-organization.md) and use its advisory project layout.
4. **Decompose the draft by scientific fidelity, not maximum native editability.** Read [references/subfigure-sourcing.md](references/subfigure-sourcing.md). Recreate the outer framework, labels, arrows, dividers, simple axes, and genuinely simple diagrams with native PowerPoint objects. Preserve complex or geometry-sensitive mechanisms as unified SVG/TikZ objects, and preserve real imagery, heatmaps, or scientific textures as separate raster assets; never downgrade them to generic PowerPoint placeholders. When an icon, ML/system mechanism, mathematical diagram, or reusable architecture template is needed, read [references/opentikz-asset-reuse.md](references/opentikz-asset-reuse.md) and use the vendored OpenTikZ workflow before web search or image generation. Treat OpenTikZ as a composable construction kit: read its retained guidance, combine suitable icons, templates, layout, annotations, and palette rules, adapt copied TikZ sources through their `edit_contract`, and compile a complete scientific subfigure. Directly reuse one catalog SVG only when the required subfigure is genuinely that simple. A weak result after both catalog search and reasonable component composition must fall through to the normal sourcing or generation workflow. Keep pure mathematical formulas on the separate LaTeX-to-SVG path. Constrain all complex scientific subfigures to familiar human-made PowerPoint, Visio, MATLAB, Matplotlib, or clean TikZ visual conventions.
5. **Prepare transparent scientific subfigures.** Before any raster subfigure is embedded, read [references/transparent-background-preparation.md](references/transparent-background-preparation.md). For a transparency-only conversion, do not call an image-generation or generative image-editing tool: use deterministic ImageMagick edge-connected flood filling or an equivalent pixel operation. Convert the outer white or near-white canvas to a genuine alpha channel while preserving enclosed white content, pale scientific traces, bright infrared targets, plot interiors, and image-frame contents. Reject baked checkerboards and visually simulated transparency; verify the PNG's actual alpha channel and inspect it on the intended panel color.
6. **Describe the accepted draft as semantic diagram IR.** Read [references/diagram-semantic-ir.md](references/diagram-semantic-ir.md) and write `diagram.ir.json` against [references/diagram-ir.schema.json](references/diagram-ir.schema.json). Preserve the draft visually rather than reducing it to a structure-only textual outline. Represent every group, native shape, text box, image asset, connector, port, z-order, and QA region explicitly. Use parent-relative coordinates so a module and its internal objects move as one unit. Treat SVG, PNG, plots, formulas, and generated scientific subfigures uniformly as image assets. Run `python3 scripts/diagram_ir.py validate diagram.ir.json` and generate a coordinate/debug overlay before authoring.
7. **Build the PowerPoint from the IR.** Read [references/ppt-assembly-and-qa.md](references/ppt-assembly-and-qa.md), load and follow the available **Presentations** skill, and use `diagram.ir.json` as the single source of truth for geometry and object identity. Convert parent-relative frames to slide coordinates deterministically, render groups in z-order, connect explicit ports, preserve image aspect ratios, and keep the outer framework editable. Whenever mathematical notation is required, also read [references/latex-formula-in-pptx.md](references/latex-formula-in-pptx.md) and use its LaTeX-to-SVG workflow.
8. **Render, compare, and revise at the correct layer.** Export the actual PPTX to an image and compare it with the draft region by region. If hierarchy, position, size, spacing, routing, or stacking is wrong, edit the IR and regenerate the affected objects or slide. If a scientific subfigure is wrong, edit only the asset while preserving its IR frame. If the PowerPoint renderer differs from the intended IR geometry, correct the renderer or explicit IR values and record the change; do not accumulate untracked visual nudges. Rerun IR validation, the debug overlay, the presentation overflow/structure test, and regional visual QA before delivery.

## Default draft-fidelity contract

Unless the user explicitly requests a redesign, the final PowerPoint must preserve the draft's visible module composition, scientific subfigure types, formulas, relative placement, and visual encoding. Crop the corresponding draft region as the working reference for each complex subfigure. A concise version may reduce modules and prose, but it must not reduce a retained scientific subfigure to a lower-information symbol or placeholder.

Scientific correctness takes priority over the percentage of native PowerPoint objects. Keep the framework editable, but implement subfigures that depend on strict parallelism, collinearity, perspective, one-to-one node/edge correspondence, grids, trajectories, or transformations as one validated SVG/TikZ object. Keep formulas that appear in the source or draft unless the user asks to remove them, and render them through the LaTeX-to-SVG workflow.

## Non-negotiable quality rules

- Never insert the full draft as a flattened slide background and call it editable.
- All titles, module names, annotations, main-flow arrows, panel frames, and genuinely simple diagrams must remain native editable PowerPoint elements generated from the semantic IR; this rule does not apply to geometry-sensitive scientific subfigures.
- Complex subfigures must be separate embedded image objects with descriptive names and alt text; the PPTX must not depend on external paths. Treat PNG and SVG as one semantic image-resource class in the IR.
- Treat the vendored `assets/opentikz/` directory as read-only. Copy selected SVG/TikZ components into the task workspace before adapting or composing them. Use the full OpenTikZ guidance to build a coherent subfigure from multiple primitives when appropriate; do not reduce OpenTikZ usage to inserting whichever simple stock icon happens to exist, and never force components whose combined semantics do not match the draft.
- Raster scientific subfigures must normally be true-alpha PNGs before embedding. Do not accept an opaque white canvas or a checkerboard pattern baked into the pixels as transparency. Keep an opaque background only when it is scientifically meaningful or explicitly requested.
- Every scientific subfigure must plausibly look human-authored in PowerPoint/Visio, exported from MATLAB/Matplotlib, or intentionally constructed in clean TikZ/SVG. Reject elaborate AI-infographic patterns, dense decorative networks, glowing effects, excessive micro-elements, and irregular shapes that a researcher would not normally draw.
- Generated subfigures should contain no important text. Recreate every required label as native PowerPoint text so spelling and typography remain reliable.
- Preserve the algorithm's semantics. Do not invent modules, reverse arrow direction, merge distinct outputs, or add decorative mechanisms unsupported by the source.
- Never replace a real image, scientific plot, formula, or explicit mechanism in the draft with generic rectangles, circles, Unicode symbols, or arbitrary arrows. Legends must reuse the actual objects' shape, fill, stroke, and line style rather than text-character imitations.
- Keep labels short. Prefer a two-level hierarchy—module title plus one short mechanism label—over paragraphs inside boxes.
- Maintain consistent stroke widths, corner radii, image treatment, and color meaning across the slide.
- When web or OpenTikZ assets are embedded, prefer official or clearly reusable sources and record the URL or OpenTikZ item path in the slide's `[Sources]` speaker-notes block.

## Deliverable

Return the final editable `.pptx`. Provide the draft prompt, preview image, or source list only when the user asks for them.
