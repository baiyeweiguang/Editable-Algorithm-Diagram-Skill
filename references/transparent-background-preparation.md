# Preparing scientific subfigures with real transparency

Read this reference after the scientific subfigures have been generated or sourced and before any raster image is embedded in PowerPoint.

## Required outcome

Each raster scientific subfigure should normally be a PNG whose outer canvas is genuinely transparent. The slide's module fill must remain visible around the mechanism instead of being covered by a white rectangle.

Transparency is a file property, not a visual convention. A gray-and-white checkerboard rendered into the pixels is an opaque image and must be rejected.

Keep an opaque canvas only when the background itself carries scientific meaning, when transparency would make the figure inaccurate, or when the user explicitly requests it.

## Preparation sequence

1. Inspect the original at full resolution and identify which light regions are removable outer canvas versus meaningful scientific content.
2. If the file already contains an alpha channel, verify that the outer region is actually non-opaque. Do not reprocess a correct transparent asset unnecessarily.
3. Otherwise remove the white or near-white background from the image edge inward. Prefer an edge-connected flood fill or equivalent background extraction over global white-key deletion.
4. Preserve the original pixel dimensions and aspect ratio during extraction. Crop only excessive transparent margins afterward.
5. Save a new non-destructive PNG derivative with a semantic name such as `motion_model_transparent.png`; retain the source asset for recovery.
6. Verify the actual channel data, then inspect the result composited on the intended module fill and on one contrasting temporary background.

## Required deterministic method

For a transparency-only conversion, **do not call image generation or generative image editing**. Those tools may redraw scientific content, alter geometry, or return an opaque checkerboard preview. Use a deterministic raster operation so that the foreground pixels remain unchanged.

The preferred method for a white or near-white outer canvas is ImageMagick edge-connected flood filling. It starts at the image boundary and removes only the light background connected to that boundary. It does not globally delete every white pixel.

### ImageMagick 6 command

```bash
convert input.png \
  -alpha on \
  -bordercolor white -border 1 \
  -fuzz 8% \
  -fill none \
  -draw 'matte 0,0 floodfill' \
  -shave 1x1 \
  -strip \
  output_transparent.png
```

### ImageMagick 7 command

```bash
magick input.png \
  -alpha on \
  -bordercolor white -border 1 \
  -fuzz 8% \
  -fill none \
  -draw 'alpha 0,0 floodfill' \
  -shave 1x1 \
  -strip \
  output_transparent.png
```

The temporary one-pixel white border provides a reliable flood-fill seed. `-fuzz 8%` treats nearby off-white antialiased background pixels as connected background. `-shave 1x1` removes the temporary border. `-strip` removes metadata without flattening the alpha channel.

Use `8%` as the normal starting tolerance. If a light halo remains, increase it cautiously; if pale axes or guides disappear, reduce it. A typical inspection range is approximately `3%` to `12%`. Do not use a high tolerance without comparing the foreground against the source.

If ImageMagick is unavailable, use another deterministic pixel-processing tool with the same edge-connected semantics. Do not substitute a generative image tool merely to obtain transparency. Regenerate the subfigure only when its scientific content or geometry also needs redesign.

## Content that must be protected

Do not globally delete every white or pale pixel. Preserve:

- white areas enclosed by plot borders, grids, matrices, cards, camera frames, or other closed geometry;
- bright infrared targets, highlights, white markers, zero-valued heatmap cells, and pale uncertainty regions;
- anti-aliased edges, light gray axes, dashed guides, contour lines, and thin scientific traces;
- white regions inside embedded photographs or sensor images;
- deliberate plot backgrounds when their removal would reduce readability or change meaning.

When a light region touches the outer canvas through an open gap, use a mask or a more conservative edge-connected tolerance rather than erasing scientifically meaningful content.

## Tool behavior and fallback

- A generation prompt may request a transparent background for a new subfigure, but never assume the result is transparent merely because its preview displays a checkerboard.
- Once a usable scientific subfigure exists, do not send it back to a generative image tool solely to remove its background.
- If a generated asset is opaque or contains a checkerboard baked into its RGB pixels, reject that transparency result and apply the deterministic method above to the original subfigure.
- Avoid aggressive global color selection. A small color tolerance around the edge background is safer than removing all high-luminance pixels.
- Do not redraw, restyle, sharpen, recolor, crop, or rearrange the scientific mechanism during a background-only edit.

## Verification gate

Before insertion, confirm all of the following:

- the PNG has an alpha channel and the intended outer pixels are non-opaque;
- no checkerboard is baked into the RGB pixels;
- the module fill shows cleanly around the subfigure when composited;
- no white rectangular canvas, light fringe, or dirty halo remains;
- enclosed white content, pale traces, and bright target pixels remain intact;
- the source aspect ratio and mechanism geometry are unchanged.

Check the real channel data rather than trusting the preview:

```bash
identify -format '%f %[channels] opaque=%[opaque]\n' output_transparent.png
```

A valid result normally reports an alpha-bearing channel such as `srgba` and `opaque=false`. An `opaque=true` result is not a successfully transparent asset.

Create a temporary colored-background preview without overwriting the transparent PNG:

```bash
convert output_transparent.png \
  -background '#DDECF8' \
  -alpha background -alpha remove \
  transparency_preview.png
```

Inspect this preview for a residual white rectangle, checkerboard pixels, light fringe, clipped thin lines, or missing enclosed white content. Delete or ignore the temporary preview after QA; embed `output_transparent.png`, not the flattened preview.

If any check fails, correct the asset before PowerPoint assembly. Do not defer transparency defects to the final slide QA stage.
