# Semantic diagram IR

Use this IR as the single geometric source of truth between the approved draft and the editable PowerPoint. It is designed for free Visio/Illustrator-style compositions rather than template-based slide layouts.

## Contents

1. Design principles
2. Coordinate and hierarchy model
3. Elements and assets
4. Ports, connectors, and constraints
5. Authoring and revision loop
6. Minimal example

## 1. Design principles

- Preserve what is visibly present in the draft. Do not reduce the draft to a structure-only textual outline before assigning geometry.
- Separate semantics from rendering: an element has a stable ID, role, parent, frame, and z-order independent of the PowerPoint API used later.
- Keep one flat `elements` table. Express hierarchy with `parent`; do not duplicate an element inside nested child arrays.
- Make every coordinate explicit. The renderer may convert units but must not invent placement, alignment, or connector endpoints.
- Keep text separate from shapes. A colored module panel and its title are two elements sharing a parent group, so either can be edited independently.
- Treat SVG, PNG, generated scientific subfigures, plots, and formula SVGs uniformly as image assets.
- Keep complex geometry-sensitive scientific mechanisms as one image asset. Use the IR to place them accurately, not to explode them into fragile PowerPoint primitives.

## 2. Coordinate and hierarchy model

Set `canvas.width` and `canvas.height` to the actual composition aspect ratio. For a 16:9 slide, `1600 × 900` is a convenient default; for a Word figure, match the approved draft instead of forcing 16:9.

Every non-connector element has a `frame`:

```json
{ "x": 40, "y": 72, "w": 360, "h": 520 }
```

Coordinates are local to the element's parent group. Root elements omit `parent` and use canvas coordinates. Moving a group therefore moves its panel, title, subfigure, labels, legend, and internal arrows together without rewriting child frames.

Flatten coordinates before PowerPoint authoring:

```text
absolute_x(child) = absolute_x(parent) + child.frame.x
absolute_y(child) = absolute_y(parent) + child.frame.y
```

Map absolute diagram units to the slide without guessing:

```text
ppt_x = absolute_x / canvas.width  × slide_width
ppt_y = absolute_y / canvas.height × slide_height
ppt_w = frame.w / canvas.width     × slide_width
ppt_h = frame.h / canvas.height    × slide_height
```

Use `z` within each parent: lower values render first. Keep sibling z-values unique when overlap matters. Use `allow_overflow: true` only for a deliberate element such as an arrow or badge crossing its parent boundary.

## 3. Elements and assets

The IR supports five element kinds:

| Kind | Purpose |
|---|---|
| `group` | movable module, lane, panel, legend, or nested coordinate system |
| `shape` | editable rectangle, rounded rectangle, ellipse, polygon, freeform path, or divider |
| `text` | editable title, label, annotation, caption, or legend text |
| `image` | SVG/PNG scientific subfigure, formula, plot, photograph, heatmap, or icon |
| `connector` | straight, orthogonal, polyline, or curved arrow between explicit ports |

Give every element a stable semantic ID such as `module-motion`, `panel-motion`, `img-motion-prior`, `label-motion-title`, or `edge-motion-to-update`. Use the same ID as the PowerPoint object name whenever possible.

Declare assets once under `assets`:

```json
"assets": {
  "motion-prior": {
    "src": "02-assets/svg/motion-prior.svg",
    "mime": "image/svg+xml",
    "alt": "Self-attention motion prediction prior",
    "intrinsic": { "w": 920, "h": 420 }
  }
}
```

Use `fit: "contain"` by default. Use `cover` only when cropping is intentional. `stretch` requires an explicit reason and must not be used for ordinary scientific subfigures.

For a polygon, store points in the shape's local frame coordinate system. For a custom SVG path used as an editable native shape, store the local `svg_path`; use an image asset instead when the mechanism is complex or geometry-sensitive.

## 4. Ports, connectors, and constraints

Define ports on groups or shapes. A port may use a side plus normalized offset:

```json
{ "id": "out", "side": "right", "offset": 0.5 }
```

or an exact local point:

```json
{ "id": "loss-in", "x": 18, "y": 92 }
```

Connectors reference ports, never approximate centers:

```json
{
  "id": "edge-motion-to-update",
  "kind": "connector",
  "parent": "main-flow",
  "z": 5,
  "from": { "element": "module-motion", "port": "out" },
  "to": { "element": "module-update", "port": "in" },
  "route": "orthogonal",
  "waypoints": [{ "x": 620, "y": 250 }],
  "style": { "stroke": "#1F2937", "stroke_width": 2, "end_arrow": "triangle" }
}
```

Waypoints use the connector parent's coordinate system. Omit them only when the route is visually unambiguous. Use explicit waypoints for non-endpoint attachment, crowded branches, and arrows that must avoid labels.

Use constraints to document and validate intended relationships:

- `align`: shared left/right/top/bottom/center axis;
- `equal_gap`: equal horizontal or vertical spacing in the authored item order;
- `same_size`: equal width, height, or both;
- `contain`: children stay inside a module with padding;
- `no_overlap`: specified items must not overlap and may require a minimum gap.

Constraints validate authored coordinates; they are not an automatic layout engine. Correct the IR when a constraint fails.

## 5. Authoring and revision loop

1. Crop the draft into named QA regions and prepare the final SVG/PNG assets.
2. Write `diagram.ir.json` against `diagram-ir.schema.json` while looking at the draft.
3. Validate structure and coordinate relationships:

```bash
python3 <skill-dir>/scripts/diagram_ir.py validate diagram.ir.json
```

4. Generate a coordinate/debug SVG:

```bash
python3 <skill-dir>/scripts/diagram_ir.py debug-svg diagram.ir.json \
  -o 03-ir/layout-debug.svg --grid 50
```

5. Inspect the debug SVG for parent bounds, object IDs, z-order intent, ports, arrow routes, and QA regions.
6. Load the Presentations skill and build the PPTX by flattening the IR coordinates deterministically.
7. Render the actual PPTX and compare each `qa_region` with its draft crop.
8. Route revisions correctly:
   - hierarchy, position, size, spacing, route, or stacking problem → edit IR and regenerate;
   - subfigure content, transparency, or crop problem → edit the asset without changing its frame;
   - PowerPoint rendering discrepancy → correct the renderer or explicit IR value and record it.

Do not make an unrecorded visual nudge directly in the PPTX. If the final position changes, the accepted IR must change too.

## 6. Minimal example

```json
{
  "version": "1.0",
  "canvas": { "width": 1600, "height": 900, "background": "#FFFFFF", "grid": 50 },
  "assets": {
    "attention": {
      "src": "02-assets/svg/attention.svg",
      "mime": "image/svg+xml",
      "alt": "Attention mechanism"
    }
  },
  "elements": [
    {
      "id": "module-motion",
      "kind": "group",
      "role": "algorithm-module",
      "frame": { "x": 120, "y": 180, "w": 420, "h": 430 },
      "z": 10,
      "ports": [{ "id": "out", "side": "right", "offset": 0.5 }]
    },
    {
      "id": "panel-motion",
      "kind": "shape",
      "parent": "module-motion",
      "frame": { "x": 0, "y": 0, "w": 420, "h": 430 },
      "z": 0,
      "geometry": { "type": "round_rect", "radius": 18 },
      "style": { "fill": "#EAF2FB", "stroke": "#56789A", "stroke_width": 2 }
    },
    {
      "id": "label-motion-title",
      "kind": "text",
      "parent": "module-motion",
      "frame": { "x": 24, "y": 18, "w": 372, "h": 48 },
      "z": 20,
      "text": "运动先验建模",
      "style": { "font_size": 25, "font_weight": 700, "align": "center", "valign": "middle", "color": "#172033" }
    },
    {
      "id": "img-attention",
      "kind": "image",
      "parent": "module-motion",
      "frame": { "x": 36, "y": 92, "w": 348, "h": 250 },
      "z": 10,
      "asset_id": "attention",
      "fit": "contain"
    }
  ],
  "constraints": [
    { "kind": "contain", "container": "module-motion", "items": ["label-motion-title", "img-attention"], "padding": 12 }
  ],
  "qa_regions": [
    { "id": "motion", "frame": { "x": 110, "y": 170, "w": 440, "h": 450 }, "draft_crop": "01-draft/regions/motion.png", "element_ids": ["module-motion"] }
  ]
}
```
