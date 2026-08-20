# Prompt rewriting for an algorithm-diagram draft

Read this reference after receiving the raw algorithm description and before calling image generation.

## Mode contract

The user must choose the content mode before this stage. Do not silently decide on their behalf.

| Mode | Prompt used | Information budget | Visual emphasis |
| --- | --- | --- | --- |
| 详细内容版 | Full prompt | Usually 3–6 major modules, with selected internal mechanisms and multiple scientific subfigures | mechanism completeness and technical explanation |
| 简洁版 | Compact prompt | Usually 3–5 major modules, one key mechanism per module, minimal secondary labels | core data flow, larger elements, immediate readability |

Generate only the selected prompt. Produce both versions only when the user explicitly requests both.

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
6. Use the full template for detailed mode or the compact template for concise mode.

## Copy-length budget

- Main module title: preferably 4–12 Chinese characters.
- Secondary label: preferably 4–10 Chinese characters.
- Input/output card: one noun phrase, not a sentence.
- A slide should normally show no more than two text levels inside a module.

If the source contains more detail, express it through small scientific subfigures or omit it from the overview diagram.

## Full prompt template

Use only when the user selects **详细内容版**. Preserve the important internal mechanisms, model assumptions, branch logic, and distinct outputs, preferably through subfigures rather than additional prose.

```text
绘制【使用场景】所用的算法架构流程图，白底扁平化2D科研框图，适合插入Word、论文或项目申请材料。该图首先用于确定最终可编辑PPT的版式草图。

【视觉风格】
使用圆角矩形作为主要功能模块，黑色或深灰色细实线箭头表示数据流；模块使用低饱和浅色填充，整体整齐对齐、层级清晰、留白均衡。模块内部的科研子图应采用人类常用的PowerPoint/Visio二维示意图风格，或MATLAB/Matplotlib科研绘图风格：几何结构规整、节点和连线数量克制、坐标轴和曲线清晰。禁止3D装饰、阴影、发光、强渐变、海报排版、华丽装饰、写实照片质感以及复杂的AI信息图案。

【算法】
算法名称：XXX
输入：XXX（字段：A、B、C）
模块1：输入XX；核心机制XX；输出XX
模块2：输入XX；核心机制XX；输出XX
模块3：输入XX；核心机制XX；输出XX
输出：XXX

【版式】
采用从左到右的数据流。主模块尺寸按内容复杂度分配；复杂模块内部预留子图区域；输出在右侧或底部统一汇总。箭头避免交叉，模块边界与内层卡片清晰。

【硬性约束】
框图只保留短标签，不放大段说明和复杂公式；中文文字必须准确，不生成乱码；不要遗漏输入输出，不要改变数据流方向；不要用随意的圆圈和箭头替代注意力机制、相机投影、概率分布、三维模型等复杂原理图；科研子图必须像研究人员使用PPT、Visio、MATLAB或Matplotlib制作的常规图形，避免密集伪网络、无意义连接、异形装饰和过度复杂细节。
```

## Compact prompt template

Use only when the user selects **简洁版**. Collapse secondary operations into the nearest major stage, retain one key mechanism per stage, and remove non-essential branches or repeated outputs.

```text
科研算法架构图版式草图，白底、扁平2D、圆角矩形、低饱和浅色模块、深色细箭头、适配Word/PPT；科研子图采用PPT/Visio常规二维示意图或MATLAB/Matplotlib科研绘图风格，结构简洁、线条规整、元素数量克制；无3D、无阴影发光、无复杂AI信息图案，文字精简准确。

算法：XXX。数据流：输入XXX → 模块A（机制/输出）→ 模块B（机制/输出）→ 模块C（机制/输出）→ 输出XXX。复杂机制预留科研子图区域，模块对齐，箭头少交叉，不用大段文字或公式。
```

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
- What are the major transformation stages?
- Which internal mechanisms need a visual rather than text?
- What leaves each stage and where does it go?
- Which outputs must remain visibly distinct?
- Is any arrow a control/state signal rather than data flow?
