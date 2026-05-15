# Scientific Figure Workflow Test QA

## Test Intent

This package stress-tests the `scientific-figure-workflow` skill with one composite bilingual figure that intentionally covers multiple scientific domains and figure types.

Defaults used:
- Purpose: internal QA / workflow stress test.
- Target standard: Nature-like clean scientific figure.
- Palette: Okabe-Ito / Wong plus Paul Tol Bright roles.
- Editability boundary: native editable framework plus transparent icon/image assets.
- Submission policy: Image2 assets are concept/test assets only, not cleared for journal submission.

## Coverage

Figure types included:
- Research flowchart / 科研流程图
- Technical roadmap / 技术路线图
- Model architecture / 模型结构图
- Mechanism diagram / 机制机制图
- Graphical abstract / 图形摘要
- Multi-panel cross-domain legend / 多组图跨领域图例

Domains included:
- Environmental sensing / 环境监测
- Agriculture and biology / 农业与生物
- Medical translation / 医学转化
- Artificial intelligence / 人工智能
- Materials science / 材料科学
- Clean engineering / 清洁工程

## Deliverables

- Original Image2 master with bug: `originals/image2_master_with_unwanted_text_bug.png`
- Independently generated no-text raw assets: `assets/raw/`
- Transparent cutout icons: `assets/cutout/`
- SVG wrappers for transparent cutouts: `assets/cutout_svg_wrappers/`
- Editable PPTX: `editable/cross_domain_stress_figure.pptx`
- SVG figure: `vector/cross_domain_stress_figure.svg`
- PPTX preview: `previews/preview_pptx.png`
- SVG preview: `previews/preview_svg.png`
- Asset manifest: `asset_manifest.json`
- Alpha audit: `qa/asset_alpha_audit.csv`

## Editability Notes

- PPTX panels, text, cards, arrows, route nodes, model boxes, and section headers are native editable PowerPoint objects.
- The six domain icons are transparent PNG picture objects. They can be moved, scaled, masked, rotated, or replaced, but their internal paths are not editable.
- The final SVG has vector framework elements and embeds icon assets as image data URIs.
- `assets/cutout_svg_wrappers/` contains SVG wrappers around transparent PNGs; these are scalable containers, not true path-vectorized icons.
- Complete workflow runs must use a Reference-Guided Asset Factory after the master/source is selected: every semantic complex visual item gets a master/source-role-guided prompt, a chroma raw asset, a transparent output, and a placement bbox.
- A few broad assets are not accepted when the selected master/source contains independently meaningful clouds, routes, maps, legends, warning symbols, state tiles, or small result icons.

## QA Results

PPTX package validation:
- Slides: 1
- Media files: 26
- Native shape tags: 100
- Text bodies: 43
- Notes entries: 0
- Slide number placeholders: 0
- Missing relationship targets: 0

Visual QA:
- PPTX preview rendered successfully through artifact-tool import of the saved PPTX.
- SVG preview rendered successfully.
- A first preview pass exposed clipped/wrapped labels in panels A, B, and C; the layout was revised and re-exported.
- Final preview has readable bilingual labels at slide scale. Some sublabels are intentionally small because this is a dense stress-test figure.
- Master similarity, fine-region coverage, no-coarse-asset, reference-guided-asset, and truthful-QA gates are required in complete runs. If the side-by-side comparison looks like a simplified same-topic redraw, the package must be marked failed and rebuilt.

Icon cutout QA:
- Initial single-asset backgrounds were not perfectly flat green despite the prompt.
- Local chroma-key removal succeeded after thresholding and small connected-component cleanup.
- One early generated medical asset contained a small background fragment; this was cleaned and the contact sheet was rebuilt.

## Bugs / Workflow Findings

1. Image2 did not fully obey `no text, no labels`: the master image contains unwanted black English labels and unrelated photoreal objects.
2. Image2 did not fully obey `flat #00ff00 background`: the icon sheet background had a visible green gradient.
3. A first Python asset-processing pass failed when an absolute Chinese path was injected through PowerShell; using `Path.cwd()` avoided the encoding issue.
4. Dense bilingual cards need shorter English labels than a normal English-only figure; otherwise PowerPoint wrapping can clip or crowd text.

## Recommendation

The skill behavior is sound only when the selected Image2 master/source remains the structure contract. Use Image2 as a visual master/layout contract plus reference-guided, independently generated no-text transparent assets, then rebuild final figures as editable Presentation/SVG geometry. For real submissions, do not use the Image2-generated raster assets without checking the journal policy and recording disclosure or replacement decisions.
