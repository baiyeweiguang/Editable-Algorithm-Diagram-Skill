# Monochrome layered architecture style

Use this template only when the user selects **黑白灰分层架构图**. It is intended for system-level relationships rather than detailed internal mechanisms.

## Style contract

- pure white background and black/white/gray palette only;
- top-down layered hierarchy, with parallel chains aligned by column when appropriate;
- straight-corner rectangles, thin black borders, light-gray solid fills, centered bold Chinese text;
- black solid connectors with clearly visible closed triangular arrowheads;
- no icons, illustrations, gradients, shadows, 3D effects, decorative patterns, or colored accents;
- express hierarchy and dependency through rectangle size, alignment, spacing, and arrow direction;
- keep the user-designated system or module as the dominant tier and show its inputs, downstream outputs, and supporting/deployment relationships.

## Detailed-mode template

```text
生成一张「【系统或算法名称】整体架构图」，科技项目申报书专用配图，采用极简工程制图风格，纯白色背景，无装饰、无渐变、无阴影、无立体效果，全程黑白灰单色系，整体严谨规整，符合正式科研申报文档配图规范。

整体采用自上而下的分层纵向布局，【核心层】按业务关系组织为【并行或串行结构】，清晰呈现模块间的上下游承接关系、并行逻辑和统一支撑关系；不深入单个算法内部技术细节，仅突出模块层级、输入、输出和关联关系。

【层级与模块】
1. 输入层：XXX。
2. 第一处理层：左侧XXX；右侧XXX；由输入分别向下连接。
3. 第二处理层：左侧XXX；右侧XXX；与上一层一一对齐并承接其输出。
4. 统一支撑或部署层：通栏模块XXX；由上层相关模块分别连接。
5. 输出层：XXX；居中承接上一层结果。

若用户指定【XXX】为视觉主体，使其成为占据显著面积的一级层级，并明确呈现其输入、核心职责、输出和去向，不得降为普通旁路方框。

【细节规范】
所有功能模块使用直角矩形框、黑色边框和浅灰色纯色填充；模块文字使用中文黑体，字号统一、居中排列；模块间关系使用黑色实线箭头，箭头为标准闭合三角箭头，线宽与箭头尺寸在整页缩略图中仍清晰可见；起止点和列对齐工整。多个独立条目分别使用独立矩形，不用一个多行文本框模拟。先规划全局线路通道，避免箭头交叉、重叠、贴边或穿过文字。整体布局对称均衡，无冗余视觉信息。
```

## Concise-mode template

```text
生成「【系统或算法名称】分层架构图」，科技项目申报书风格，纯白背景、黑白灰单色、极简工程制图、无图标、无装饰、无渐变阴影和立体效果。

采用自上而下布局：输入层XXX → 并行/串行处理层XXX → 核心主体层XXX → 通栏支撑或部署层XXX → 输出层XXX。用户指定的主体必须成为一级视觉结构，并明确输入、职责、输出和去向。所有模块使用直角矩形、黑色边框、浅灰填充、中文黑体居中；使用线宽和箭头头部均清晰可见的黑色实线箭头；模块按列对齐、间距均衡、线路通道分离，不深入算法内部细节。
```
