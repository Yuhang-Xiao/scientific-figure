---
name: scientific-figure-workflow
description: "Use when Codex needs to create, revise, debug, or convert top-journal-style scientific figures, research workflow diagrams, technical route maps, model architecture figures, mechanism diagrams, graphical abstracts, editable PPTX/SVG figures, or Image2-to-Presentation workflows. Supports prompt-to-figure from a drawing prompt and image-to-editable from existing PNG/JPG diagrams. Triggers include scientific figure, publication figure, workflow figure, flowchart, technical roadmap, model diagram, mechanism figure, graphical abstract, editable flowchart, transparent icon assets, image-to-editable, 科研绘图, 流程图, 技术路线图, 模型图, 机制图, 可编辑PPT, 顶刊风格图."
---

# Scientific Figure Workflow

Create publication-style scientific figures while preserving editability where it matters: native PowerPoint/SVG text, arrows, lanes, boxes, connectors, labels, charts, and data objects; separate transparent image assets for complex icons or scientific mini-illustrations.

## Load With

- Load `$imagegen` when generating an Image2 visual master or separated icon/illustration assets.
- Load `$editable-flowchart-from-image` when rebuilding a reference image into editable PPTX/SVG, removing icon backgrounds, validating PPTX packages, or rendering previews.
- Load `presentations:Presentations` when authoring/exporting editable PowerPoint content and previews.
- Load references only when needed:
  - `references/usage.md` for user-facing mode examples.
  - `references/output-structure.md` before creating the work package.
  - `references/debug-and-qa.md` before final QA or when an Image2/background/text bug appears.
  - `references/image-to-editable.md` for existing PNG/JPG conversion.
  - `references/vectorization.md` when the user asks for editable icon paths.
  - Existing standard references for journal policy, palettes, and editability boundaries.

## Mode Decision

Use **Mode A: Prompt-to-Figure** when the user gives a drawing prompt, research topic, figure idea, or desired scientific workflow. Generate an Image2 master and any separated icon assets, then rebuild the final figure as editable PPTX/SVG.

Use **Mode B: Image-to-Editable** when the user provides an existing PNG/JPG/screenshot/reference figure. Understand the image content and layout, extract or recreate transparent assets, and rebuild the framework as editable PPTX/SVG. Do not use the source image as the final background unless explicitly requested.

## Preflight Hook

Before generating or rebuilding any figure, always ask or explicitly confirm these choices. If the user already supplied a choice, restate it briefly, record it, and continue:

1. Mode: prompt-to-figure or image-to-editable.
2. Purpose: submission, presentation, grant/proposal, manuscript draft, internal concept.
3. Figure type: flowchart, technical roadmap, model architecture, mechanism/process diagram, multi-panel figure, graphical abstract.
4. Tone and palette: Okabe-Ito/Wong, Paul Tol, Viridis/Cividis, ColorBrewer, Minimal Journal, or custom.
5. Target standard: named journal/publisher when known; otherwise Nature-like with a colorblind-aware palette.
6. Editability boundary: default to editable framework plus transparent icon/image assets.
7. Output root and figure slug.
8. Other requirements: language, aspect ratio, panel count, icon editability, data/source constraints, and anything the user wants to avoid.

If the user already supplied a choice, record it in `00_request/preflight_choices.json` and continue.

## Core Workflow

1. Create a numbered work package using `references/output-structure.md`.
2. Save the user prompt, mode, preflight choices, and all input/reference images.
3. For Mode A, generate an Image2 visual master and separated icon/illustration assets. For Mode B, inspect the source image and identify text, arrows, panels, icons, charts, and asset regions.
4. Keep critical labels, captions, legends, axes, and bilingual text as native editable text; do not rely on generated in-image text.
5. Build or extract raw icon assets, remove backgrounds into transparent PNG/WebP assets, and create contact sheets plus alpha audits.
6. Rebuild the final figure with editable Presentation/SVG objects for framework elements and place transparent assets in matching positions.
7. Export PPTX, SVG, and full-size previews.
8. Write manifests, policy notes, known issues, and QA files before delivery.

## Output Contract

Every figure must be delivered as a self-contained package named:

```text
<figure_slug>_<YYYYMMDD_HHMM>/
```

Use the numbered directory contract from `references/output-structure.md`. The most important final files are:

```text
06_editable_pptx/<figure_slug>.pptx
07_svg_export/<figure_slug>.svg
08_previews/preview_pptx.png
08_previews/preview_svg.png
09_manifests/output_index.json
09_manifests/asset_manifest.json
09_manifests/editability_manifest.json
10_qa/QA_notes.md
```

`output_index.json` is the navigation entrypoint. It must point to the final PPTX, SVG, previews, selected master, transparent asset directory, QA notes, and known issue summary.

## Hard Rules

- Do not change the Image2 master composition or visual logic merely to simplify editability.
- Do not manually redraw complex icons or scientific mini-illustrations just to make them editable; preserve approved Image2/source assets as transparent images unless a trusted vector source exists.
- Do not call SVG wrappers around PNGs "true editable vectors"; label them as SVG image wrappers.
- Do not use generated in-image text as final scientific labels when editable text can be used.
- Do not let Image2 text pollution, non-flat chroma backgrounds, alpha halos, bilingual text crowding, or Chinese path encoding issues pass silently; record and fix or disclose them in QA.
- Do not deliver without PPTX package validation, rendered previews, manifest files, and a QA note.

## QA Checklist

- Output package follows the numbered structure and has `output_index.json`.
- Text, arrows, frames, connectors, labels, and core layout are editable objects in PPTX/SVG.
- Transparent icons align with the master/source image and preserve aspect ratio.
- No text overlap, clipping, edge spill, tiny labels, low contrast, or unreadable legend.
- Alpha audit and contact sheet exist when transparent assets are used.
- PPTX has no missing relationships, notes leftovers, or slide number placeholders.
- Submission-bound figures record whether AI-generated assets are excluded, replaced, disclosed, or explicitly accepted by the user.
