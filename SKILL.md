---
name: algorithm-diagram-ppt
description: Turn a raw academic or engineering algorithm description into a one-slide editable PowerPoint architecture or flow diagram, first asking the user to choose a detailed or concise content mode, then generating a layout draft, creating or sourcing complex scientific subfigures, converting their outer backgrounds to verified transparency, rebuilding the frame with native PPT objects, and rendering for visual QA. Use for algorithm framework, technical route, system architecture, or execution-flow diagrams requested as editable PPT/PPTX; do not use for ordinary multi-slide decks or simple text-only flowcharts.
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
3. **Design and generate a layout draft.** Read [references/prompt-rewriting.md](references/prompt-rewriting.md). Use the full prompt only for detailed mode and the compact prompt only for concise mode; do not automatically generate both. With OpenAI image generation, use GPT-Image2 or the current built-in image tool backed by it. Generate a draft that establishes hierarchy, proportions, palette, and subfigure placement.
4. **Decompose the draft into editable and raster parts.** Read [references/subfigure-sourcing.md](references/subfigure-sourcing.md). Recreate panels, labels, arrows, dividers, simple axes, and simple node groups with native PowerPoint objects. Obtain genuinely complex scientific subfigures through image generation or web search, but constrain them to familiar human-made PowerPoint, Visio, MATLAB, or Matplotlib visual conventions. Do not replace attention, projection, probability, geometry, or model mechanisms with arbitrary circles and arrows.
5. **Prepare transparent scientific subfigures.** Before any raster subfigure is embedded, read [references/transparent-background-preparation.md](references/transparent-background-preparation.md). For a transparency-only conversion, do not call an image-generation or generative image-editing tool: use deterministic ImageMagick edge-connected flood filling or an equivalent pixel operation. Convert the outer white or near-white canvas to a genuine alpha channel while preserving enclosed white content, pale scientific traces, bright infrared targets, plot interiors, and image-frame contents. Reject baked checkerboards and visually simulated transparency; verify the PNG's actual alpha channel and inspect it on the intended panel color.
6. **Rebuild the slide in PowerPoint.** Read [references/ppt-assembly-and-qa.md](references/ppt-assembly-and-qa.md). Load and follow the available **Presentations** skill before authoring. Match the draft's aspect ratio and spatial hierarchy, embed the verified transparent subfigures as independent images, and keep all framework text and shapes editable.
7. **Render, inspect, and correct.** Export every slide to an image, inspect it at full size, run the presentation overflow test when available, fix all visible defects, then render again. Deliver only the validated PPTX.

## Non-negotiable quality rules

- Never insert the full draft as a flattened slide background and call it editable.
- All titles, module names, annotations, arrows, panel frames, and simple diagrams must be native PowerPoint elements.
- Complex subfigures must be separate embedded image objects with descriptive names and alt text; the PPTX must not depend on external paths.
- Raster scientific subfigures must normally be true-alpha PNGs before embedding. Do not accept an opaque white canvas or a checkerboard pattern baked into the pixels as transparency. Keep an opaque background only when it is scientifically meaningful or explicitly requested.
- Every scientific subfigure must plausibly look human-authored in PowerPoint/Visio or exported from MATLAB/Matplotlib. Reject elaborate AI-infographic patterns, dense decorative networks, glowing effects, excessive micro-elements, and irregular shapes that a researcher would not normally draw.
- Generated subfigures should contain no important text. Recreate every required label as native PowerPoint text so spelling and typography remain reliable.
- Preserve the algorithm's semantics. Do not invent modules, reverse arrow direction, merge distinct outputs, or add decorative mechanisms unsupported by the source.
- Keep labels short. Prefer a two-level hierarchy—module title plus one short mechanism label—over paragraphs inside boxes.
- Maintain consistent stroke widths, corner radii, image treatment, and color meaning across the slide.
- When web assets are embedded, prefer official or clearly reusable sources and record the URL in the slide's `[Sources]` speaker-notes block.

## Deliverable

Return the final editable `.pptx`. Provide the draft prompt, preview image, or source list only when the user asks for them.
