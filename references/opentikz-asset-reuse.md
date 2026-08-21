# Reusing OpenTikZ assets in algorithm-diagram PowerPoints

Read this reference when an algorithm diagram needs an icon, an ML/system mechanism, a mathematical diagram, or a reusable TikZ architecture template. The vendored OpenTikZ library is a read-only source library at `assets/opentikz/`, pinned to upstream commit `359befbf8e8af7ce08e7e387b2c2a198e0ca735d`.

OpenTikZ is an optional accelerator, not a mandatory visual language. Reuse an item only when it is an exact or close semantic match to the intended subfigure and the layout draft. If the match is weak, continue with the normal subfigure sourcing or generation workflow.

## Routing decision

| Need | Preferred path |
| --- | --- |
| simple boxes, arrows, labels, or axes | native PowerPoint objects |
| matching OpenTikZ icon | copy the committed SVG and embed it directly |
| matching template/example with no structural changes | copy its committed `preview.svg` |
| matching template that needs labels, colors, or supported structural edits | copy the `.tex`, read its `edit_contract`, edit the copy, compile it, and embed the resulting SVG |
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

OpenTikZ code is MIT licensed and its graphic content is CC0 1.0. All distributed copies of this Skill carry the same research-focused runtime subset containing the nested OpenTikZ Skill, examples, ML/system icons, templates, and reference material. Record the repository URL and the selected item path in the slide's `[Sources]` speaker-notes block for traceability, for example:

```text
[Sources]
- https://github.com/opentikz/opentikz/tree/main/icons/ml/attention (CC0-1.0; vendored commit 359befb)
[/Sources]
```

Brand assets are intentionally omitted from the compact runtime package. If a brand mark is needed, use an official reusable source, follow the owner's brand rules, and record its source URL.

The packaged catalog is strongest for ML and system architecture. It may not contain a faithful Gaussian distribution, probability-density plot, diffusion trajectory, or other requested mathematical diagram. Treat absence as a normal fallback condition and use Matplotlib, purpose-built TikZ, a reusable public-domain vector, or the approved subfigure-generation workflow instead.

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

The nested `assets/opentikz/skills/using-opentikz/SKILL.md` is an intentional runtime reference and must remain present. Update `opentikz.lock.json` to the reviewed upstream commit, rebuild or filter `catalog.json` so every entry resolves to a retained item, and run:

```bash
python3 scripts/opentikz_asset.py validate
python3 /path/to/skill-creator/scripts/quick_validate.py .
```

Re-test one direct SVG copy, one template compilation, and one known no-match query before publishing the Skill update.
