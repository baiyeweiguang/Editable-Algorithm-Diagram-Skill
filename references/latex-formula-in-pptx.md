# LaTeX formulas as SVG objects in PowerPoint

Use this workflow whenever an algorithm diagram contains a mathematical formula that ordinary PowerPoint text cannot reproduce reliably. Compile the formula with LaTeX, convert the tightly cropped PDF to SVG, inspect the SVG visually, and embed it as an independent vector image in the PPTX.

## Preferred toolchain

- `pdflatex`: compile LaTeX source to a tightly cropped PDF.
- `pdftocairo`: convert the compiled PDF to SVG while preserving mathematical glyph placement.
- `inkscape`: rasterize the SVG only for visual inspection; it may also be used for SVG cleanup when necessary.
- `@oai/artifact-tool`: embed the SVG bytes into the editable PowerPoint frame and export the PPTX.
- Presentation render and overflow helpers: verify the final slide rather than trusting the source SVG alone.

Prefer the pipeline

```text
formula.tex -> pdflatex -> formula.pdf -> pdftocairo -svg -> formula.svg -> PPTX image object
```

Do not approximate fractions, roots, superscripts, subscripts, matrices, or operators with several manually aligned text boxes. That approach is fragile across fonts, PowerPoint versions, and later layout edits.

## 1. Write a tightly cropped LaTeX source

Use the `standalone` document class so the PDF page is cropped to the formula rather than a full sheet of paper.

```tex
\documentclass[border=10pt]{standalone}
\usepackage{amsmath,amssymb}
\usepackage{xcolor}

\begin{document}
{\color[HTML]{111827}\Huge
$\displaystyle
\operatorname{Attention}(Q,K,V)
=
\operatorname{softmax}\!\left(
  \frac{QK^{\mathsf T}}{\sqrt{d_k}}
\right)V
$}
\end{document}
```

Practical guidance:

- Use `\displaystyle` for display-style fractions, roots, sums, and integrals.
- Use `\operatorname{...}` for named operators such as `softmax`, `Attention`, `argmin`, or `KL` when no built-in operator exists.
- Set the formula color in LaTeX so it matches the slide palette.
- Prefer standard size commands such as `\Large`, `\LARGE`, or `\Huge`. Scale the resulting SVG in PowerPoint. Arbitrary very large `\fontsize` values may trigger Computer Modern font substitution warnings without improving vector quality.
- Keep labels and explanatory prose as native PowerPoint text. The SVG should normally contain only the mathematical expression.
- Use a small standalone border, commonly `6pt` to `12pt`, to prevent glyph clipping while avoiding excessive whitespace.

## 2. Compile LaTeX to PDF

Run LaTeX in non-interactive, fail-fast mode:

```bash
pdflatex -interaction=nonstopmode -halt-on-error formula.tex
```

Expected output:

```text
formula.tex
formula.pdf
formula.log
formula.aux
```

Stop on a nonzero exit code. Inspect `formula.log` when packages, commands, or fonts are missing. Do not continue to SVG conversion after a failed or partial compilation.

## 3. Convert the PDF to SVG

Use Poppler's Cairo converter as the default:

```bash
pdftocairo -svg formula.pdf formula.svg
```

This conversion produced correct glyph positions, fractions, radicals, delimiters, and superscripts in the validated Attention example.

Avoid using direct Inkscape PDF import as the first conversion method:

```bash
# Not the preferred default for LaTeX PDFs
inkscape formula.pdf --export-filename=formula.svg
```

Direct PDF import may reconstruct LaTeX glyphs with incorrect transforms. In the tested Attention formula, this caused overlapping `softmax`, displaced fraction contents, and malformed delimiters. If Inkscape PDF import is used as a fallback, the result must be visually inspected before embedding.

## 4. Render a preview and inspect it

SVG files are not always supported by the local image viewer. Rasterize a temporary high-resolution preview:

```bash
inkscape formula.svg \
  --export-filename=formula-preview.png \
  --export-width=1600
```

Inspect the preview at full size. Check:

- fraction bars and square roots are complete;
- superscripts and subscripts are attached to the correct symbols;
- large parentheses and brackets enclose the intended expression;
- operator names do not overlap neighboring terms;
- no glyph is missing, duplicated, or displaced;
- the outer canvas is not padded with excessive whitespace.

The preview PNG is only a QA artifact. Embed the SVG, not this PNG, unless SVG support fails.

## 5. Embed the SVG with `@oai/artifact-tool`

Read the SVG as bytes and add it as a separate image object. Use `fit: "contain"` so PowerPoint preserves the full formula.

```js
import fs from "node:fs/promises";

const formula = await fs.readFile("formula.svg");
const formulaBytes = formula.buffer.slice(
  formula.byteOffset,
  formula.byteOffset + formula.byteLength,
);

slide.images.add({
  blob: formulaBytes,
  contentType: "image/svg+xml",
  alt: "Scaled dot-product attention equation rendered from LaTeX",
  fit: "contain",
  position: {
    left: 650,
    top: 300,
    width: 560,
    height: 150,
  },
});
```

Placement guidance:

- Size the formula primarily by width; preserve its aspect ratio.
- Give fractions, matrices, and multi-line equations more vertical room than single-line expressions.
- Keep the SVG as an independent image object rather than flattening it into the full-slide draft.
- Add descriptive alt text that identifies the equation.
- Recreate captions, equation numbers, callouts, and symbol definitions as editable PowerPoint text unless they are mathematically inseparable from the expression.
- Keep the source `.tex` during construction so the equation can be corrected and regenerated deterministically.

PowerPoint exports may include both the original SVG and a PNG compatibility fallback. This is acceptable as long as the SVG remains embedded.

## 6. Verify the exported PPTX

Confirm that an SVG object is present inside the PowerPoint package:

```bash
unzip -l output.pptx | rg 'ppt/media/.*\.(svg|png)'
```

Then render the final deck and run the presentation overflow test. When using the bundled Presentations helpers, provide the required runtime paths:

```bash
export RUNTIME_NODE="$CODEX_PRIMARY_RUNTIME_NODE"
export RUNTIME_NODE_MODULES="$CODEX_PRIMARY_RUNTIME_NODE_MODULES"
export RUNTIME_BIN_DIR="$CODEX_PRIMARY_RUNTIME_ROOT/dependencies/bin/override"

python3 "$SKILL_DIR/container_tools/render_slides.py" output.pptx
python3 "$SKILL_DIR/container_tools/slides_test.py" output.pptx
```

Inspect the rendered slide at full size. A correct standalone SVG can still become too small, clipped, or visually unbalanced after placement in the slide.

## Raster fallback

Use a high-resolution transparent PNG only when the presentation runtime or target PowerPoint environment cannot preserve SVG. Generate it from the validated PDF or SVG rather than taking a screenshot:

```bash
pdftocairo -png -r 300 -transp formula.pdf formula
```

Embed the resulting PNG with `contentType: "image/png"` and `fit: "contain"`. Treat this as a compatibility fallback; SVG is preferred for normal delivery.

## Completion checklist

- The formula compiles without LaTeX errors.
- `pdftocairo -svg` is used as the default PDF-to-SVG conversion.
- A high-resolution preview has been visually inspected.
- The SVG contains only the formula and has sensible outer padding.
- The SVG is embedded as a separate PowerPoint image object with alt text.
- Captions and explanations remain editable PowerPoint text.
- The exported PPTX contains an SVG media object.
- The final rendered slide shows no formula deformation, clipping, or overflow.
