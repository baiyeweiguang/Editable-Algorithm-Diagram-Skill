# Prompt style catalog

Read this catalog after the content mode is known. Resolve the visual style with the user, then load only the selected template.

| Choice | Style | Best use | Template |
| --- | --- | --- | --- |
| A | 浅色科研机制图 | A single algorithm, mechanism-rich flow, scientific subfigures, formulas, proposal/paper figures | [prompt-styles/pastel-scientific.md](prompt-styles/pastel-scientific.md) |
| B | 黑白灰分层架构图 | System-level hierarchy, parallel processing chains, proposal architecture overview, few or no scientific subfigures | [prompt-styles/monochrome-layered-architecture.md](prompt-styles/monochrome-layered-architecture.md) |
| C | 沿用参考草图 / 自定义风格 | The user supplies a sketch, house style, or explicit visual specification | Use the supplied reference as the template; do not load A or B unless needed for a specific missing convention. |

Do not blend the rounded pastel mechanism style into a strict monochrome architecture, or strip scientific mechanisms from style A merely to imitate style B. Content mode controls information density; visual style controls geometry, palette, and visual vocabulary.

When the user has not chosen a style, ask alongside the detailed/concise question. If the user delegates the decision, choose B for a high-level system hierarchy and A for a mechanism-rich single-algorithm diagram.

To add another supported style later, add one focused template under `prompt-styles/` and one catalog row. Keep shared semantic rewriting rules in `prompt-rewriting.md` instead of duplicating them in every template.
