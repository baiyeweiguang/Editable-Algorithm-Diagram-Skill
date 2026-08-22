---
name: algorithm-diagram-ppt
description: Turn a raw academic or engineering algorithm description into a one-slide editable PowerPoint architecture or flow diagram, first asking the user to choose a detailed or concise content mode and a visual style, then generating a layout draft, preparing faithful OpenTikZ/LaTeX/raster assets, describing the full Visio/Illustrator-style composition in a semantic diagram IR with explicit hierarchy and coordinates, and rebuilding and visually validating the slide through the Presentations workflow. Use for algorithm framework, technical route, system architecture, or execution-flow diagrams requested as editable PPT/PPTX; do not use for ordinary multi-slide decks or simple text-only flowcharts.
---

# Editable Algorithm Diagram PPT

Create a polished algorithm figure whose framework remains editable in PowerPoint. The generated layout draft is a visual blueprint, not the deliverable.

## Required content and style selection

Before rewriting the algorithm or calling image generation, actively ask the user to choose a content mode:

1. **详细内容版（完整生图 Prompt）** — richer module internals and more scientific subfigures; best for project applications, technical reports, and cases where the mechanism must be shown clearly.
2. **简洁版（简短 Prompt）** — fewer internal elements, stronger visual hierarchy, larger effective text and subfigure areas; best for slides, compact Word figures, and fast overview communication.

Also ask the user to choose a visual style from [references/prompt-style-catalog.md](references/prompt-style-catalog.md). Initially supported choices are:

1. **浅色科研机制图** — the existing low-saturation PowerPoint/Visio scientific style, suitable for a single algorithm with mechanisms and scientific subfigures.
2. **黑白灰分层架构图** — a strict monochrome, top-down layered system architecture, suitable for project proposals and system-level relationships without decorative imagery.
3. **沿用参考草图 / 自定义风格** — follow a supplied reference or explicit visual specification.

Ask in the user's language. For a Chinese request, combine the two choices concisely:

> 请选择内容版本与视觉风格：
>
> 1. 详细内容版：使用完整生图 Prompt，保留更多模块内部机制与科研子图。
> 2. 简洁版：使用简短 Prompt，只保留核心数据流和关键机制。
>
> A. 浅色科研机制图
> B. 黑白灰分层架构图
> C. 沿用参考草图或自定义风格
>
> 可直接回复“简洁版 + B”。

These are blocking choices: do not generate the layout draft until both are resolved. Do not ask again for a choice already explicit in the request or unambiguous from a supplied reference. If the interface provides a compact user-choice control, present the unresolved options with a free-text alternative; otherwise ask in ordinary chat. If the user requests both content modes, generate two separate drafts and PPTX deliverables unless they ask for one combined file. If the user delegates the content choice, use detailed mode for proposals or technical reports and concise mode for presentation or overview use. If the user delegates the style choice, use the monochrome layered style for a system-level hierarchy and the pastel scientific style for a mechanism-rich single-algorithm diagram.

## Default interpretation

After the content mode and style are resolved, the raw algorithm description is normally sufficient. Unless the selected style or user specification says otherwise, assume:

- one landscape slide suitable for a proposal, paper, or Word insertion;
- horizontal left-to-right data flow with an output strip when useful;
- white background, clearly visible dark arrows, rounded rectangles, and low-saturation pastel module colors;
- concise Chinese labels when the source is Chinese;
- no 3D decoration, drop shadows, glossy gradients, poster styling, or dense prose.

Apart from the required content/style selection, ask only when another missing choice materially changes the result, such as multiple incompatible algorithms or an explicitly required house template.

## Workflow

1. **Select content mode and visual style.** Ask for any unresolved detailed-versus-concise and style-catalog choices.
2. **Extract the drawable algorithm for the selected mode.** Identify the input, outputs, major modules, internal mechanisms, cross-module data flow, control flow, and any user-designated visual subject. When the user calls a module the subject, core, or focus, make it the primary visual structure and preserve its full input → processing → output → constraint/destination story. Remove background prose, derivations, and implementation details that do not belong in the figure. The concise mode applies a stricter information budget.
3. **Design and generate a layout draft.** Read [references/prompt-rewriting.md](references/prompt-rewriting.md), then read [references/prompt-style-catalog.md](references/prompt-style-catalog.md) and only the template selected there. Use the full prompt only for detailed mode and the compact prompt only for concise mode; do not automatically generate both. With OpenAI image generation, use GPT-Image2 or the current built-in image tool backed by it. Generate a draft that establishes hierarchy, proportions, palette, and subfigure placement. For jobs that create several intermediate assets, also read [references/workspace-organization.md](references/workspace-organization.md) and use its advisory project layout.
4. **Decompose the draft by scientific fidelity, not maximum native editability.** Read [references/subfigure-sourcing.md](references/subfigure-sourcing.md). Recreate the outer framework, labels, arrows, dividers, simple axes, and genuinely simple diagrams with native PowerPoint objects. Preserve complex or geometry-sensitive mechanisms as unified SVG/TikZ objects, and preserve real imagery, heatmaps, or scientific textures as separate raster assets; never downgrade them to generic PowerPoint placeholders. When an icon, ML/system mechanism, mathematical diagram, or reusable architecture template is needed, read [references/opentikz-asset-reuse.md](references/opentikz-asset-reuse.md) and use the vendored OpenTikZ workflow before web search or image generation. Treat OpenTikZ as a composable construction kit: read its retained guidance, combine suitable icons, templates, layout, annotations, and palette rules, adapt copied TikZ sources through their `edit_contract`, and compile a complete scientific subfigure. Directly reuse one catalog SVG only when the required subfigure is genuinely that simple. A weak result after both catalog search and reasonable component composition must fall through to the normal sourcing or generation workflow. Keep pure mathematical formulas on the separate LaTeX-to-SVG path. Constrain all complex scientific subfigures to familiar human-made PowerPoint, Visio, MATLAB, Matplotlib, or clean TikZ visual conventions.
5. **Prepare transparent scientific subfigures.** Before any raster subfigure is embedded, read [references/transparent-background-preparation.md](references/transparent-background-preparation.md). For a transparency-only conversion, do not call an image-generation or generative image-editing tool: use deterministic ImageMagick edge-connected flood filling or an equivalent pixel operation. Convert the outer white or near-white canvas to a genuine alpha channel while preserving enclosed white content, pale scientific traces, bright infrared targets, plot interiors, and image-frame contents. Reject baked checkerboards and visually simulated transparency; verify the PNG's actual alpha channel and inspect it on the intended panel color.
6. **Describe the accepted draft as semantic diagram IR.** Read [references/diagram-semantic-ir.md](references/diagram-semantic-ir.md) and write `diagram.ir.json` against [references/diagram-ir.schema.json](references/diagram-ir.schema.json). Preserve the draft visually rather than reducing it to a structure-only textual outline. Represent every group, native shape, text box, image asset, connector, port, z-order, and QA region explicitly. Use parent-relative coordinates so a module and its internal objects move as one unit. Give each independent card its own shape and text element, and give each logical connector one connector element with its complete route. Treat SVG, PNG, plots, formulas, and generated scientific subfigures uniformly as image assets. Run `python3 scripts/diagram_ir.py validate diagram.ir.json` and generate a coordinate/debug overlay before authoring.
7. **Build the PowerPoint from the IR.** Read [references/ppt-assembly-and-qa.md](references/ppt-assembly-and-qa.md) and [references/visual-qa-checklist.md](references/visual-qa-checklist.md), load and follow the available **Presentations** skill, and use `diagram.ir.json` as the single source of truth for geometry and object identity. Convert parent-relative frames to slide coordinates deterministically, render groups in z-order, connect explicit ports, preserve image aspect ratios, and keep the outer framework editable. Whenever mathematical notation is required, also read [references/latex-formula-in-pptx.md](references/latex-formula-in-pptx.md) and use its LaTeX-to-SVG workflow.
8. **Render, diagnose, revise, and verify.** Use the observable correction loop in `ppt-assembly-and-qa.md`: render the actual PPTX, inspect it at whole-slide and regional scales with the visual QA checklist, classify each visible defect, edit the correct IR/asset/renderer layer, and rerender. Rerun IR validation, the debug overlay, the presentation overflow/structure test, semantic line tracing, and regional visual QA before delivery.

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
- A user-designated subject must determine the composition rather than appear as an ordinary side box. It must have clear visual priority and visibly expose its inputs, core operation, outputs, and constraint or destination paths.
- Never replace a real image, scientific plot, formula, or explicit mechanism in the draft with generic rectangles, circles, Unicode symbols, or arbitrary arrows. Legends must reuse the actual objects' shape, fill, stroke, and line style rather than text-character imitations.
- Each visually independent card, capsule, state item, or list item must use its own background shape and its own text box. Never simulate several cards with one multiline text box.
- Plan connector channels across the whole slide before authoring individual paths. Each logical polyline must remain one editable PowerPoint connector/freeform object with all waypoints in that object; never assemble it from separate line segments.
- Keep labels short. Prefer a two-level hierarchy—module title plus one short mechanism label—over paragraphs inside boxes.
- Maintain consistent stroke widths, corner radii, image treatment, and color meaning across the slide.
- When web or OpenTikZ assets are embedded, prefer official or clearly reusable sources and record the URL or OpenTikZ item path in the slide's `[Sources]` speaker-notes block.

## Deliverable

Return the final editable `.pptx`. Provide the draft prompt, preview image, or source list only when the user asks for them.
