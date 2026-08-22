# Prompt rewriting for an algorithm-diagram draft

Read this reference after receiving the raw algorithm description and before calling image generation.

## Content-mode and style contract

The user must choose the content mode and visual style before this stage. Do not silently decide on their behalf unless they explicitly delegate the choice. Read [prompt-style-catalog.md](prompt-style-catalog.md), then load only the selected style template.

| Mode | Prompt used | Information budget | Visual emphasis |
| --- | --- | --- | --- |
| 详细内容版 | Full prompt | Usually 3–6 major modules, with selected internal mechanisms and multiple scientific subfigures | mechanism completeness and technical explanation |
| 简洁版 | Compact prompt | Usually 3–5 major modules, one key mechanism per module, minimal secondary labels | core data flow, larger elements, immediate readability |

Generate only the selected content/style combination. Produce alternatives only when the user explicitly requests them.

Both modes still use short, accurate native PowerPoint labels. “详细内容版” means more meaningful mechanisms and subfigures, not paragraphs of visible text.

## Communication goal

The prompt should make the image model design a useful composition, not typeset the original paper. Separate algorithm semantics from visible slide copy.

## Rewrite procedure

1. State the use case and output type in the first sentence: academic proposal/paper/Word-ready algorithm architecture diagram, white background, flat 2D.
2. Put visual constraints before algorithm details so layout and style are established early.
3. Convert the source into a drawable sequence:
   - input and its fields;
   - three to six major modules;
   - each module's input, core operation, and output;
   - final outputs;
   - any essential branch, feedback, or control relation.
4. Remove long motivation text, proofs, equations, hyperparameters, citations, and code-level details unless the figure's purpose explicitly requires them.
5. End with failure-prevention constraints: short labels, accurate Chinese, aligned modules, few crossing lines, no decorative clutter.
6. If the user names a module as the subject, core, or focus, rewrite the layout around that visual subject. Its inputs, core processing, outputs, and constraint/destination paths must all remain explicit.
7. Use the full or compact variant from the selected style template. Do not blend visual rules from unselected templates.

## Copy-length budget

- Main module title: preferably 4–12 Chinese characters.
- Secondary label: preferably 4–10 Chinese characters.
- Input/output card: one noun phrase, not a sentence.
- A slide should normally show no more than two text levels inside a module.

If the source contains more detail, express it through small scientific subfigures or omit it from the overview diagram.

## Style-template routing

Do not keep a universal visual template here. Read the selected entry from [prompt-style-catalog.md](prompt-style-catalog.md), then read exactly one linked template:

- [prompt-styles/pastel-scientific.md](prompt-styles/pastel-scientific.md) for a mechanism-rich low-saturation scientific diagram;
- [prompt-styles/monochrome-layered-architecture.md](prompt-styles/monochrome-layered-architecture.md) for a strict black/white/gray layered system architecture.

If the user supplies a reference sketch or custom visual specification, use it as the selected template and do not load unrelated built-in templates.

## Draft-generation rules

- Use GPT-Image2 when the environment exposes OpenAI image generation for this task.
- The draft's job is composition: hierarchy, scale, grouping, palette, and visual rhythm.
- Scientific inserts in the draft must use recognizable PowerPoint/Visio diagram language or MATLAB/Matplotlib plot language. Treat ornate AI-generated visual complexity as a defect, not added value.
- Treat generated text as untrusted. Copy the intended labels from the rewritten algorithm plan into native PowerPoint text later.
- If one draft has strong composition but weak subfigures, keep the composition and regenerate subfigures separately instead of repeatedly regenerating the entire figure.
- Generate another draft only when the overall hierarchy or flow is unusable; local defects belong to the reconstruction stage.

## Extraction checklist

Before generation, verify that the rewritten plan answers:

- What enters the algorithm?
- Did the user designate a visual subject, and does the plan expose its input → processing → output → constraint/destination story?
- What are the major transformation stages?
- Which internal mechanisms need a visual rather than text?
- What leaves each stage and where does it go?
- Which outputs must remain visibly distinct?
- Is any arrow a control/state signal rather than data flow?
