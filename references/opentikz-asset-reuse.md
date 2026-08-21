# Reusing OpenTikZ assets in algorithm-diagram PowerPoints

Read this reference when an algorithm diagram needs an icon, an ML/system mechanism, a mathematical diagram, or a reusable TikZ architecture template. The vendored OpenTikZ library is a read-only source library at `assets/opentikz/`, pinned to upstream commit `359befbf8e8af7ce08e7e387b2c2a198e0ca735d`.

For advanced OpenTikZ template adaptation, also read the retained upstream guidance at `assets/opentikz/skills/using-opentikz/UPSTREAM_SKILL.md`. It keeps the useful nested-Skill instructions under a filename that the ChatGPT package registry does not mistake for a second top-level Skill.

OpenTikZ is an optional accelerator, not a mandatory visual language. Use its full composition ability rather than treating the catalog as a flat icon picker: a complete subfigure may combine several icons, a template, annotations, layout patterns, palette definitions, and edited TikZ. Reuse components only when their combined semantics can closely match the intended subfigure and the layout draft. If a faithful composition is not reasonable, continue with the normal subfigure sourcing or generation workflow.

## Routing decision

| Need | Preferred path |
| --- | --- |
| simple boxes, arrows, labels, or axes | native PowerPoint objects |
| matching OpenTikZ icon | copy the committed SVG and embed it directly |
| matching template/example with no structural changes | copy its committed `preview.svg` |
| matching template that needs labels, colors, or supported structural edits | copy the `.tex`, read its `edit_contract`, edit the copy, compile it, and embed the resulting SVG |
| complex subfigure assembled from several OpenTikZ parts | read `UPSTREAM_SKILL.md`, copy every needed source into the task workspace, compose them in one TikZ coordinate system, compile, and embed the unified SVG |
| mathematical formula rather than a diagram | use `latex-formula-in-pptx.md`, not OpenTikZ |
| no sufficiently close OpenTikZ match | continue with web search, deterministic plotting/TikZ, or image generation |

An imported SVG remains an independent vector image object in PowerPoint; it is not a collection of native PowerPoint shapes. Keep the surrounding framework, labels, arrows, and simple geometry native and editable.

## Discover without loading the full catalog

Use the adapter script from the Skill root:

```bash
python3 scripts/opentikz_asset.py search --query "attention" --type icon --domain ml
python3 scripts/opentikz_asset.py search --query "encoder decoder" --type template
python3 scripts/opentikz_asset.py info --id encoder-decoder
```

Search by the requested mechanism, not by a merely related field. Inspect the top few candidates' metadata and SVG previews before choosing. A zero-result or low-quality result is a valid outcome; do not invent an item or force a poor match.

Do not stop after failing to find one finished catalog item with the exact requested name. Search separately for the subfigure's meaningful components—such as model blocks, attention, datasets, matrices, servers, annotations, or an architecture template—and judge whether the retained OpenTikZ guidance supports a faithful composition. Component composition is preferred over a low-information placeholder, but it must not invent unsupported mechanisms.

## Complete subfigure composition

For any subfigure more complex than a single symbol, read `assets/opentikz/skills/using-opentikz/UPSTREAM_SKILL.md` and the relevant `reference/` material. Start from the closest template when one exists; otherwise create a standalone TikZ figure that imports or adapts the selected components. Keep all nodes and connections in one coordinate system, preserve template invariants and semantic node names, use the OpenTikZ palette and spacing rules, and add annotations through its documented patterns. Compile and visually inspect the complete SVG before embedding it as one scientific subfigure object.

The catalog assets are primitives, not a completeness ceiling. It is acceptable—and often preferred—to build a richer, draft-faithful subfigure from several retained assets. It is not acceptable to insert a lone generic icon when the draft requires a mechanism, topology, or multi-stage process.

## Direct SVG reuse

For an exact icon or an unchanged template/example, copy the existing SVG to the current task's temporary asset directory:

```bash
python3 scripts/opentikz_asset.py copy \
  --id attention \
  --format svg \
  --out /tmp/algorithm-diagram-assets
```

Inspect the SVG at the intended size and panel color. Preserve its aspect ratio, crop only genuinely excessive outer margins, embed the SVG bytes in the PPTX, and give the image object a semantic name and alt text. Do not run raster transparency conversion on SVG assets.

## Editable TikZ template path

Never modify `assets/opentikz/`. Copy the source into the task workspace:

```bash
python3 scripts/opentikz_asset.py copy-source \
  --id encoder-decoder \
  --out /tmp/opentikz-edit
```

Before editing a template, read its `template.meta.json` through `info --id ...` and follow its `edit_contract`:

- change the declared parameters for labels, dimensions, and spacing;
- use only the listed operations for structural edits;
- preserve `node_naming` and every invariant;
- keep the source standalone-compilable;
- retain the named OpenTikZ palette rather than introducing arbitrary inline colors.

Compile the copied source and convert the PDF to SVG:

```bash
python3 scripts/opentikz_asset.py compile \
  --tex /tmp/opentikz-edit/template.tex \
  --out /tmp/algorithm-diagram-assets/encoder-decoder.svg
```

The helper prefers `latexmk`, falls back to `pdflatex`, then uses `pdftocairo -svg` or `dvisvgm --pdf`. If the LaTeX packages required by the catalog entry are unavailable, do not return a partially compiled figure; use the committed SVG when it is still accurate or fall back to the normal subfigure workflow.

## Visual and semantic QA

- Compare the selected asset with the corresponding regional crop from the layout draft when that crop is usable. Preserve its intended subject, composition, and visual role without forcing a mismatch.
- Check arrow direction, mathematical structure, grouping, labels, aspect ratio, padding, and consistency with the slide palette.
- If labels are not integral to the scientific geometry, remove them from the source asset and recreate them as native PowerPoint text.
- For template edits, inspect the compiled SVG rather than trusting successful compilation alone.
- Render the final PPTX and confirm that the SVG remains an embedded media object.

## Provenance and limits

OpenTikZ code is MIT licensed and its graphic content is CC0 1.0. All distributed copies of this Skill carry the same runtime subset containing the retained nested OpenTikZ guidance, examples, brand/ML/system icons, templates, reference material, and runtime tools. Record the repository URL and the selected item path in the slide's `[Sources]` speaker-notes block for traceability, for example:

```text
[Sources]
- https://github.com/opentikz/opentikz/tree/main/icons/ml/attention (CC0-1.0; vendored commit 359befb)
[/Sources]
```

Brand icons are retained as reusable diagram assets. Their TikZ implementation may be CC0, but the underlying marks can still be protected trademarks; use them only for identification, follow the owner's brand rules, and do not imply endorsement.

The packaged catalog is strongest for ML, system architecture, and brand icons. It may not contain a faithful Gaussian distribution, probability-density plot, diffusion trajectory, or other requested mathematical diagram. Treat absence as a normal fallback condition and use Matplotlib, purpose-built TikZ, a reusable public-domain vector, or the approved subfigure-generation workflow instead.

## Maintainer update procedure

Normal Skill execution must never update the vendored library. When intentionally updating the Skill repository, check out a reviewed upstream revision in a temporary directory, then synchronize it through the committed packaging exclusions:

```bash
git clone https://github.com/opentikz/opentikz.git /tmp/opentikz-upstream
git -C /tmp/opentikz-upstream checkout <reviewed-commit>
rsync -a --delete \
  --exclude='/.git/' \
  --exclude='/.gitignore' \
  --exclude-from=assets/opentikz/.gitignore \
  /tmp/opentikz-upstream/ assets/opentikz/
```

The nested guidance at `assets/opentikz/skills/using-opentikz/UPSTREAM_SKILL.md` is an intentional runtime reference and must remain present. Update `opentikz.lock.json` to the reviewed upstream commit, rebuild or filter `catalog.json` so every entry resolves to a retained item, and run:

```bash
python3 scripts/opentikz_asset.py validate
python3 /path/to/skill-creator/scripts/quick_validate.py .
```

Re-test one direct SVG copy, one template compilation, and one known no-match query before publishing the Skill update.
