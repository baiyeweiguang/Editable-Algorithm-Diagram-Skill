# Sourcing and generating scientific subfigures

Read this reference after a usable layout draft exists and before assembling the PowerPoint.

## Classify every element

| Recreate with native PowerPoint | Use a separate raster subfigure |
| --- | --- |
| outer panels and cards | attention or transformer internals |
| titles and labels | camera projection/frustum geometry |
| straight or elbow arrows | 3D coordinate or motion-model illustration |
| dividers, legends, simple axes | multivariate probability surface and contours |
| simple nodes, clusters, bars, curves | dense clutter/measurement field |
| simple input/output icons | scientific image, sensor view, or mechanism that needs visual depth |

The boundary is semantic clarity. If a PowerPoint-native sketch would look generic or misrepresent the mechanism, use a proper subfigure.

## Required human-made style families

Every subfigure must belong to one of these familiar scientific styles:

### PowerPoint / Visio mechanism diagram

Use for attention blocks, projection geometry, data association, state transition, clustering, sensor models, and other mechanism illustrations.

- flat 2D geometry built from rectangles, circles, ellipses, axes, straight or gently curved connectors, dashed guide lines, and simple arrowheads;
- regular alignment and spacing, consistent stroke width, and at most three accent colors plus neutral gray/black;
- a small number of clearly meaningful objects; typically one mechanism, two or three visual layers, and no dense all-to-all graph unless scientifically essential;
- no lighting, texture, perspective decoration, isometric objects, floating glass panels, glow, particles, ornamental ribbons, or arbitrary abstract shapes.

### MATLAB / Matplotlib scientific plot

Use for probability distributions, contours, uncertainty ellipses, trajectories, scatter fields, histograms, heatmaps, and quantitative curves.

- conventional Cartesian or 3D plotting layout with clean axes, restrained gridlines, standard markers, contour lines, and legible data traces;
- white background and a familiar scientific palette such as blue, orange, green, gray, or a standard sequential colormap;
- no infographic embellishment, cinematic rendering, dramatic perspective, artificial lighting, or decorative background;
- remove axis labels and legends from the generated image when they can be added more reliably as native PowerPoint text.

Use the simplest style that explains the mechanism. A complex mechanism may justify a subfigure, but it does not justify visual complexity unrelated to the mechanism.

## Preferred sourcing order

1. Reuse a user-provided asset when it is accurate and visually compatible.
2. Generate a purpose-built subfigure with the image-generation tool.
3. Use web search for official, public-domain, or clearly reusable scientific material when generation is unsuitable.

Do not copy a paper figure merely because it is convenient. When a web image is used, preserve its source URL in speaker notes.

## Subfigure prompt template

```text
Use case: scientific-educational
Asset type: embedded scientific subfigure for an editable academic PowerPoint algorithm diagram
Primary request: [one precise mechanism only]
Scientific content: [required objects, geometry, and relationship]
Style family: looks like a human-created [PowerPoint/Visio 2D mechanism diagram OR MATLAB/Matplotlib scientific plot]
Style: clean conventional scientific drawing, regular geometry, thin consistent strokes, restrained low-saturation [palette], transparent background preferred, no AI-infographic aesthetic
Composition: [landscape/portrait and intended card aspect ratio], centered with tight but safe margins, readable at thumbnail size
Complexity budget: one mechanism only, two or three visual layers, limited meaningful nodes and connections, no dense decorative network
Constraints: no text, no letters, no numbers, no labels, no watermark, no outer frame, no glow, no strong gradient, no 3D decoration, no isometric styling, no particles, no abstract ornament, no unrelated objects
```

Generate distinct mechanisms with distinct prompts. Do not request a multi-asset sheet when the final PowerPoint needs separate image objects.

## Consistency rules

- Fix a shared line color, accent palette, background treatment, and level of detail across all subfigures.
- Use one of the two approved style families consistently; do not mix MATLAB axes, glossy infographic nodes, and 3D illustration in one image.
- Limit the palette to neutral strokes plus at most three semantic accent colors unless a heatmap requires a standard continuous colormap.
- Prefer sparse structure. For network-like mechanisms, show representative connections instead of a visually dense all-to-all mesh when the full mesh is not essential.
- Ask for exact intended aspect ratio before generation; do not stretch a square image into a wide card.
- Avoid embedded words, formulae, or variable names unless they are impossible to reproduce separately.
- Prefer transparent backgrounds. A white generation canvas is acceptable as an intermediate only when it will be converted to verified transparency before PowerPoint insertion.
- Retain enough contrast for Word export and print. Pale details must still be visible on a white page.

## Asset preparation

Before insertion:

1. inspect every image at original resolution;
2. follow [transparent-background-preparation.md](transparent-background-preparation.md) to convert the outer white or near-white canvas to a verified alpha channel;
3. crop excessive transparent margins without cutting axes, arrows, or uncertainty contours;
4. keep the source aspect ratio;
5. use PNG for line art and transparency;
6. give files semantic names such as `attention.png`, `camera_projection.png`, and `probability_distribution.png`;
7. embed bytes in the PPTX and give each image a descriptive object name and alt text.

## Rejection criteria

Regenerate or replace a subfigure if it contains:

- garbled text or accidental symbols;
- scientifically wrong direction, geometry, or grouping;
- generic decorative networks unrelated to the mechanism;
- excessive nodes, crisscrossing lines, micro-icons, particles, or secondary ornaments that make the image look machine-generated rather than researcher-made;
- glow, glassmorphism, strong gradients, 3D/isometric rendering, cinematic perspective, or decorative lighting;
- irregular geometry, inconsistent perspective, or connections that could not be reproduced naturally in PowerPoint/Visio;
- inconsistent visual style;
- an opaque white rectangle around the subfigure when the panel is tinted, or a checkerboard pattern baked into the image instead of a real alpha channel;
- excessive whitespace that makes it unreadable in the assigned card;
- blurry, over-sharpened, or photorealistic treatment that conflicts with the diagram.

Apply a final plausibility test: **could a researcher reasonably recreate this subfigure in PowerPoint/Visio or MATLAB/Matplotlib without specialist illustration software?** If not, simplify or regenerate it.
