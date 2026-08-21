---
name: algorithm-diagram-ppt
description: Turn a raw academic or engineering algorithm description into a one-slide editable PowerPoint architecture or flow diagram, first asking the user to choose a detailed or concise content mode, then generating a layout draft, reusing suitable OpenTikZ vector assets or sourcing complex scientific subfigures, converting raster backgrounds to verified transparency, rebuilding the frame with native PPT objects, and rendering for visual QA. Use for algorithm framework, technical route, system architecture, or execution-flow diagrams requested as editable PPT/PPTX; do not use for ordinary multi-slide decks or simple text-only flowcharts.
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
4. **Decompose the draft by scientific fidelity, not maximum native editability.** Read [references/subfigure-sourcing.md](references/subfigure-sourcing.md). Recreate the outer framework, labels, arrows, dividers, simple axes, and genuinely simple diagrams with native PowerPoint objects. Preserve complex or geometry-sensitive mechanisms as unified SVG/TikZ objects, and preserve real imagery, heatmaps, or scientific textures as separate raster assets; never downgrade them to generic PowerPoint placeholders. When an icon, ML/system mechanism, mathematical diagram, or reusable architecture template is needed, read [references/opentikz-asset-reuse.md](references/opentikz-asset-reuse.md) and search the vendored OpenTikZ catalog before web search or image generation. Reuse only an exact or close semantic match; a weak or absent match must fall through to the normal sourcing or generation workflow. Keep pure mathematical formulas on the separate LaTeX-to-SVG path. Constrain all complex scientific subfigures to familiar human-made PowerPoint, Visio, MATLAB, Matplotlib, or clean TikZ visual conventions.
5. **Prepare transparent scientific subfigures.** Before any raster subfigure is embedded, read [references/transparent-background-preparation.md](references/transparent-background-preparation.md). For a transparency-only conversion, do not call an image-generation or generative image-editing tool: use deterministic ImageMagick edge-connected flood filling or an equivalent pixel operation. Convert the outer white or near-white canvas to a genuine alpha channel while preserving enclosed white content, pale scientific traces, bright infrared targets, plot interiors, and image-frame contents. Reject baked checkerboards and visually simulated transparency; verify the PNG's actual alpha channel and inspect it on the intended panel color.
6. **Rebuild the slide in PowerPoint.** Read [references/ppt-assembly-and-qa.md](references/ppt-assembly-and-qa.md). Load and follow the available **Presentations** skill before authoring. Match the draft's aspect ratio and spatial hierarchy, embed verified transparent raster subfigures or validated OpenTikZ SVGs as independent image objects, and keep all framework text and shapes editable. Whenever mathematical notation is required, also read [references/latex-formula-in-pptx.md](references/latex-formula-in-pptx.md) and use its LaTeX-to-SVG embedding workflow instead of approximating the formula with ordinary text boxes.
7. **Render, compare by region, and correct.** Export every slide to an image, inspect it at full size, and compare the draft and rendered slide region by region. Each retained scientific subfigure, formula, legend, branch, input, and output must express the same object with no lower-information substitution; geometry-sensitive relations must remain correct in the actual PowerPoint rendering. Run the presentation overflow test when available, fix every semantic or visual defect, then render again. Deliver only the validated PPTX.

## Default draft-fidelity contract

Unless the user explicitly requests a redesign, the final PowerPoint must preserve the draft's visible module composition, scientific subfigure types, formulas, relative placement, and visual encoding. Crop the corresponding draft region as the working reference for each complex subfigure. A concise version may reduce modules and prose, but it must not reduce a retained scientific subfigure to a lower-information symbol or placeholder.

Scientific correctness takes priority over the percentage of native PowerPoint objects. Keep the framework editable, but implement subfigures that depend on strict parallelism, collinearity, perspective, one-to-one node/edge correspondence, grids, trajectories, or transformations as one validated SVG/TikZ object. Keep formulas that appear in the source or draft unless the user asks to remove them, and render them through the LaTeX-to-SVG workflow.

## Non-negotiable quality rules

- Never insert the full draft as a flattened slide background and call it editable.
- All titles, module names, annotations, main-flow arrows, panel frames, and genuinely simple diagrams must be native PowerPoint elements; this rule does not apply to geometry-sensitive scientific subfigures.
- Complex subfigures must be separate embedded image objects with descriptive names and alt text; the PPTX must not depend on external paths.
- Treat the vendored `assets/opentikz/` directory as read-only. Copy a selected SVG or TikZ source into the task workspace before adapting it, and never force an OpenTikZ item whose semantics do not match the draft.
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
