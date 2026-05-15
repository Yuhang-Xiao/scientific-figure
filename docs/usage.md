# Usage

Use this reference when explaining how to invoke the workflow or when deciding which mode to run.

## Mode A: Prompt-to-Figure

Use when the user gives a figure idea, research topic, technical workflow, model design, or drawing prompt.

Example prompts:

```text
用 $scientific-figure-workflow 画一个食品安全风险预测技术路线图，顶刊风格，中英文标签，输出PPTX、SVG、原图和透明图标。
```

```text
Use $scientific-figure-workflow to create a Nature-like graphical abstract for a multimodal crop disease forecasting model. Keep labels editable and export PPTX/SVG.
```

Required flow:

1. Record the request in `00_request/user_prompt.md`.
2. Confirm preflight choices and write `00_request/preflight_choices.json`.
3. Generate the Image2 master under `02_image2_master/` and independent reference-guided no-text assets under `03_assets_raw/`.
4. Remove backgrounds only from independently generated assets under `04_assets_cutout/`.
5. Rebuild the figure as editable PPTX/SVG under `06_editable_pptx/` and `07_svg_export/`.
6. Write previews, manifests, and QA.

## Mode B: Image-to-Editable

Use when the user provides an existing PNG/JPG/screenshot/reference figure and asks to make it editable.

Example prompts:

```text
用 $scientific-figure-workflow 把 D:\path\figure.png 转成可编辑流程图，重新生成匹配的无文字图标资产并处理成透明背景，输出PPTX和SVG。
```

```text
Use $scientific-figure-workflow to rebuild this JPG mechanism diagram as editable PPTX/SVG. Keep icons as transparent assets unless simple vectorization works.
```

Required flow:

1. Save source images under `01_inputs/source_images/`.
2. Inspect the image and write a content/layout understanding note.
3. Rebuild text, arrows, boxes, panels, routes, legends, and charts as native objects.
4. Generate matching no-text icon/mini-illustration assets as needed and remove backgrounds only from those generated assets.
5. Map source elements to final editable elements in `09_manifests/editability_manifest.json`.
6. Export final PPTX/SVG and previews.

## Result Navigation

Tell the user to open these first:

```text
09_manifests/output_index.json
08_previews/preview_pptx.png
06_editable_pptx/<figure_slug>.pptx
10_qa/QA_notes.md
```

Do not ask the user to guess file purposes from filenames. The package directory must explain itself through numbered folders and manifests.
