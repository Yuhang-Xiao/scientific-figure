---
name: scientific-figure-workflow
description: "Create, revise, debug, or convert top-journal-style scientific figures, research workflow diagrams, route maps, model architecture figures, mechanism diagrams, graphical abstracts, and Image2-to-editable PPTX/SVG packages. Use for scientific figure, publication figure, workflow figure, flowchart, technical roadmap, model diagram, mechanism figure, graphical abstract, editable flowchart, transparent icon assets, image-to-editable, 科研绘图, 流程图, 技术路线图, 模型图, 机制图, 可编辑PPT, 顶刊风格图."
---

# Scientific Figure Workflow

Create publication-style scientific figures while preserving editability where it matters: native PowerPoint/SVG text, arrows, lanes, boxes, connectors, labels, charts, and data objects; separate transparent image assets for complex icons or scientific mini-illustrations. The selected Image2 master or user source image is the structure contract only: final PPTX/SVG output must preserve panels, frames, title bars, text content, hierarchy, legends, arrow paths, relative coordinates, small icons, and overall layout unless the user explicitly asks for redesign, but no part of the master/source/reference image may be cut out and reused as an asset.

## Load With

- Load `$imagegen` when generating an Image2 visual master or separated icon/illustration assets.
- Load `$editable-flowchart-from-image` when rebuilding a reference image into editable PPTX/SVG, removing generated asset backgrounds, validating PPTX packages, or rendering previews.
- Load `presentations:Presentations` when authoring/exporting editable PowerPoint content and previews.
- Load references only when needed:
  - `references/usage.md` for user-facing mode examples.
  - `references/output-structure.md` before creating the work package.
  - `references/debug-and-qa.md` before final QA or when an Image2/background/text bug appears.
  - `references/image-to-editable.md` for existing PNG/JPG conversion.
  - `references/vectorization.md` when the user asks for editable icon paths.
  - Existing standard references for journal policy, palettes, and editability boundaries.

## Mode Decision

Use **Mode A: Prompt-to-Figure** when the user gives a drawing prompt, research topic, figure idea, or desired scientific workflow. This mode has three required stages: (1) generate a full labeled Image2 master for visual comparison and layout anchoring only; (2) generate each complex visual element as a separate no-text Image2/procedural asset on a flat chroma-key background and remove that background into a transparent PNG/WebP; (3) assemble the final editable PPTX/SVG from transparent assets plus native editable text, arrows, labels, frames, charts, and callouts while preserving the full labeled master structure. The full master must never be cut into local assets.

Use **Mode B: Image-to-Editable** when the user provides an existing PNG/JPG/screenshot/reference figure. Understand the image content and layout, then rebuild the framework as editable PPTX/SVG using native objects and newly generated matching no-text assets. The source/reference image is the structure contract, not an asset source. Do not freely rearrange it into a new figure, do not cut any source/reference region into an asset, and do not use the source image as the final background unless explicitly requested.

## Master/Source Structure Lock

Default behavior for all modes is structure-preserving reconstruction, not same-topic redesign.

- Treat the selected Image2 master or user source/reference image as the layout contract.
- Use the master/source/reference image only for structure, coordinates, text transcription, and parity checking; never use local regions from it as intermediate or final assets.
- Rebuild panels, section bars, frames, callout boxes, dividers, legends, conclusion boxes, routes, arrows, and label hierarchy in their original relative positions.
- Preserve text content, numeric values, legend items, panel order, visual grouping, and scientific logic unless the user explicitly asks to edit them.
- Complex visuals can differ in texture or rendering details, but their master/source regions, proportions, and role in the layout must match.
- If the user asks for redesign, simplification, or rearrangement, record that permission in `00_request/preflight_choices.json`, `09_manifests/master_layout_manifest.json`, and `10_qa/known_issues.md`.

## Fine Region Inventory

Before rebuilding, inspect the master/source and create a fine-grained inventory. Do not start assembly from only broad panel boxes.

- List every visible non-text object that affects structure or meaning: frames, section bars, arrows, routes, cloud groups, rain lines, vapor arrows, state-transition mini-panels, legend symbols, conclusion icons, gauges, maps, and small decorative-but-semantic icons.
- Assign each item one implementation type: `native_vector`, `native_text`, `route_geometry`, `generated_matching_asset`, or `approved_omission`. Source-derived asset implementations are forbidden.
- For composite regions, split into subregions whenever separate parts have independent positions, directions, or scientific roles. A cloud-rain-vapor cluster, legend row, or state-transition inset is not one acceptable asset if its internal placement must match the master.
- Do not satisfy this inventory with a few broad assets such as "left panel image", "middle scene", or "six icon set". If a region contains independently meaningful clouds, rain marks, gauges, state tiles, maps, legend symbols, route arrows, or conclusion icons, inventory those items separately.
- Treat master/source semantic symbols as first-class coverage items. Warning signs, stump icons, inset maps, affected-area glyphs, thermometer/gauge art, vapor-arrow groups, moisture-transport arrow bundles, rain marks, result-card icons, and protection/conclusion icons must be listed in `fineRegions` or `smallIcons`.
- Treat directional route symbols as first-class coverage items. Curved cascade arrows, multi-arc dashed routes, gradient transition arrows, thick directional bars, multi-arrow bundles, and other meaning-bearing route artwork must be listed in `routeSegments` or `fineRegions`; do not hide them inside generic native straight connectors.
- Default implementation for semantic symbols is `generated_matching_asset`, using the master/source as reference. Use `native_framework_geometry` only for plain framework marks such as simple rectangles, section bars, dividers, connector arrows, legend swatches, and text; record `native_exception_reason` when a semantic-looking item is intentionally kept native.
- Default implementation for complex directional route artwork is `generated_matching_asset`, using the master/source as reference. Use native connectors only for plain framework arrows; record connector start/end anchors, expected arrowhead end, and `arrow_direction_status`.
- Store the inventory in `master_layout_manifest.json` as `fineRegions`, `routeSegments`, `legendItems`, and `smallIcons`.
- Store the corresponding rebuild mapping in `asset_manifest.json` or `editability_manifest.json`; every listed item must have a final implementation path or an explicit, user-approved exception.

## Reference-Guided Asset Factory

After the Image2 master/source is selected and before PPTX/SVG assembly, run a mandatory reference-guided asset factory for every complex visual item in the fine-region inventory.

- Use the master/source only as visual reference for style, angle, object role, proportions, and target placement. Never crop, mask, split, trace, or background-remove pixels from it.
- Generate each complex item as its own no-text Image2/procedural asset on a flat chroma-key background. The prompt must mention the referenced master/source role and request a similar single isolated object, not a redesigned same-topic substitute.
- Keep generated assets granular enough to preserve the master/source structure. Separate independently positioned scene parts such as a map, cloud, rain group, forest tile, degraded-state tile, equipment icon, legend symbol, warning icon, or result-card icon when their placement matters.
- Record `region_granularity`, `master_visual_role`, `reference_guided_prompt`, `asset_similarity_target`, and `coarse_asset_forbidden` for each generated complex item in `asset_manifest.json`.
- For semantic symbols, also record `semantic_symbol_required`, `symbol_family`, `master_symbol_bbox`, `reference_guided_symbol_prompt`, `native_exception_reason`, and `symbol_parity_status`. If the symbol is generated, these fields live with the asset entry; if it is a justified native framework object, they live in `editability_manifest.json`.
- For directional route symbols, also record `directional_symbol_required`, `route_symbol_family`, `master_route_bbox`, `reference_guided_route_prompt`, `arrow_direction_status`, `arrowhead_expected_at`, and `native_connector_endpoint_policy`. If the route artwork is generated, these fields live with the asset entry; if it is a plain native connector, they live in `editability_manifest.json`.
- If a generated asset is too different, contains text/pseudo-text, has a non-flat background, or cannot be cleanly keyed, reject it, regenerate it, or record `parity_failure_reason` and `redo_required: true`. Do not quietly pass it.
- Use Presentation/PPTX/SVG native objects for all editable framework elements: text, title bars, numbered badges, frames, dividers, legend labels, threshold lines, arrows, dashed routes, brackets, axes, simple symbols, and conclusion boxes.
- Use `presentations:Presentations` for editable authoring/render QA when available. Use `python-pptx` as the deterministic PPTX build/package-validation path when exact coordinates or runtime fallback are needed; ask before installing any missing runtime dependency.

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
3. For Mode A, generate a full labeled Image2 visual master and save it under `02_image2_master/`. The master is for composition, comparison, and user-facing review; final scientific text is still rebuilt as native editable text.
4. For every mode, write `09_manifests/master_layout_manifest.json` before rebuilding. Record the canvas size, panel structure, title bars, frames, legend zones, conclusion boxes, arrow/route paths, main asset regions, text zones, `fineRegions`, `routeSegments`, `legendItems`, `smallIcons`, and any approved deviations.
5. Run the Reference-Guided Asset Factory. For Mode A, write `01_inputs/notes/master_understanding.md` and identify every complex visual element that needs its own no-text asset prompt. Generate matching elements one-by-one on flat chroma-key backgrounds; remove backgrounds into `04_assets_cutout/transparent_png/`; audit alpha quality. Store raw outputs only under `03_assets_raw/generated_single_assets/`.
6. For Mode B, inspect the source image and identify text, arrows, panels, icons, charts, and asset regions. Rebuild each item as native text/vector/route geometry or generate a matching no-text asset. Do not cut out, mask, trace-raster-extract, or background-remove any local region from the source/reference image.
7. Create a source-to-output mapping before rebuilding. For every major visual asset, semantic symbol, small icon, legend symbol, directional route symbol, and generated asset, record `master_region_bbox` or `source_layout_bbox` as layout reference only, plus `placement_target_bbox`, `layout_role`, `parity_status`, `region_granularity`, `master_visual_role`, `asset_similarity_target`, and editability type. For generated assets, also record `single_asset_prompt`, `reference_guided_prompt`, `chroma_key_color`, `raw_chroma_path`, `transparent_path`, alpha status, `coarse_asset_forbidden`, `semantic_symbol_required` when applicable, `symbol_family`, `master_symbol_bbox`, `reference_guided_symbol_prompt`, `symbol_parity_status`, `directional_symbol_required` when applicable, `route_symbol_family`, `master_route_bbox`, `reference_guided_route_prompt`, `arrow_direction_status`, `arrowhead_expected_at`, `native_connector_endpoint_policy`, `parity_failure_reason`, and `redo_required`. For routes/arrows, record start/end anchors, intermediate points or Bezier controls, direction, dash pattern, stroke width, arrowhead count/locations, and whether the final object is native geometry or a newly generated no-text transparent asset.
8. Keep critical labels, captions, legends, axes, and bilingual text as native editable text; do not rely on generated in-image text.
9. Rebuild the final figure with editable Presentation/SVG objects for framework elements and place newly generated transparent assets in matching positions and proportions. Preserve the master/source composition unless the user explicitly asks for a redesign.
10. Export PPTX, SVG, and full-size previews.
11. Write manifests, policy notes, known issues, parity reports, and QA files before delivery.

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
09_manifests/master_layout_manifest.json
09_manifests/visual_diff_report.json
09_manifests/editability_manifest.json
10_qa/QA_notes.md
```

`output_index.json` is the navigation entrypoint. It must point to the final PPTX, SVG, previews, selected master, transparent asset directory, QA notes, and known issue summary.

## Hard Rules

- Do not change the Image2 master or source composition, panel order, title-bar structure, legend, explanation boxes, conclusion box, arrow routes, or visual grouping merely to simplify editability.
- **No Image Cropping Rule:** never crop, cut, mask, extract, or background-remove a local region from an Image2 master, user source image, screenshot, or reference image for use as an intermediate or final asset. This applies to every mode.
- Do not treat an Image2 master or source image as inspiration only. It is the structure contract unless the user explicitly authorizes redesign.
- Do not freely rearrange a figure into a new same-topic schematic when the task is to make a master/source image editable.
- Do not skip the Fine Region Inventory. A rebuild that only maps broad panels and a few large assets cannot pass QA.
- Do not represent a master/source area as one coarse asset when it contains independently positioned clouds, arrows, rain, icons, or legend details that affect the visible structure.
- Do not treat "5-6 complex assets exist" as proof of coverage. Asset count is not the gate; every semantic visual item in the master/source must be mapped or explicitly approved as omitted.
- Do not generate new complex visuals from the topic alone after a master/source exists. Prompts for complex assets must be reference-guided by the selected master/source role, style, orientation, proportions, and placement target.
- Do not approximate dashed routes, cascade paths, direction arrows, or multi-arrow flows with generic straight lines. Capture route geometry, direction, dash pattern, and arrowhead positions, or generate a matching no-text route asset.
- Do not treat complex directional route artwork as a plain framework arrow. Multi-arc cascade paths, curved dashed route bundles, thick gradient transition arrows, and route artwork with embedded arrowheads must come from the reference-guided asset factory unless the user explicitly approves a native simplification.
- Do not let PPTX connector endpoints drift. Native arrows must be checked in the saved PPTX/OpenXML so the visible arrowhead appears at the recorded destination, not merely in the raster preview.
- Do not omit small master/source icons such as conclusion-box icons, tree clusters, mini transition states, or legend symbols. They must be rebuilt, generated, or explicitly listed as user-approved omissions.
- Do not hand-draw semantic symbols from scratch. Warning signs, result-card icons, gauge/thermometer art, inset maps, vapor-arrow groups, moisture bundles, rain-mark groups, and other meaning-bearing symbol art must come from the reference-guided asset factory unless they are plain framework geometry with a recorded native exception.
- Do not manually redraw complex icons, landscapes, maps, instruments, tissue/organism scenes, ecosystem scenes, or scientific mini-illustrations just to make them editable; generate matching no-text assets and remove their backgrounds unless a trusted vector source exists.
- Do not replace an Image2-guided rebuild with a fresh vector schematic that only resembles the prompt. If the final preview would fail a side-by-side comparison with the selected master, reject and rebuild with per-element transparent assets.
- Do not drop master/source layout elements such as frames, subpanels, legends, section bars, explanatory boxes, state-transition mini-panels, or bottom icon legends just because they are tedious to recreate.
- Do not create any raw-asset folder for master/source-derived regions, do not write extraction-type implementation values into manifests, and do not treat any image cut from a master/source as a valid implementation.
- When the selected master contains complex visual regions, the final PPTX should contain actual media assets (`ppt/media/*`) and `asset_manifest.json` must not claim that all such regions are native editable geometry.
- Do not call SVG wrappers around PNGs "true editable vectors"; label them as SVG image wrappers.
- Do not use generated in-image text as final scientific labels when editable text can be used.
- Do not pass QA by checking only `ppt/media/*` and alpha. Layout, content, and asset parity are required gates.
- Do not mark visual parity gates as passed when the final preview is only a simplified same-topic redesign. If `comparison_master_vs_editable.png` is obviously unlike the selected master/source in panel structure, object count, title bars, legends, arrows, or relative placement, set the relevant gates to failed and redo the build.
- Do not let Image2 text pollution, non-flat chroma backgrounds, alpha halos, bilingual text crowding, or Chinese path encoding issues pass silently; record and fix or disclose them in QA.
- Do not deliver without PPTX package validation, rendered previews, manifest files, and a QA note.

## QA Checklist

- Output package follows the numbered structure and has `output_index.json`.
- `master_layout_manifest.json` records the master/source structure contract.
- Text, arrows, frames, connectors, labels, and core layout are editable objects in PPTX/SVG.
- Transparent icons align with the master/source image and preserve aspect ratio.
- `comparison_master_vs_editable.png` shows close visual alignment with the selected master/source image.
- `visual_diff_report.json` passes the Layout Parity Gate, Content Parity Gate, and Asset Parity Gate.
- Fine Region Inventory Gate: `master_layout_manifest.json` lists all visually meaningful non-text objects under `fineRegions`, `routeSegments`, `legendItems`, and `smallIcons`.
- Route/Arrow Parity Gate: each route or arrow records and matches direction, path shape, dash style, stroke weight, and arrowhead count/locations.
- Directional Route Symbol Coverage Gate: every complex route/arrow artwork in the master/source is present in `routeSegments` or `fineRegions`, has `directional_symbol_required` metadata, and is either a generated matching route asset or a justified plain-native-connector exception.
- Small Icon & Legend Parity Gate: conclusion icons, mini transition icons, legend symbols, and other small semantic visuals are present and mapped in the manifests.
- Semantic Symbol Asset Coverage Gate: every master/source semantic symbol is present in `fineRegions` or `smallIcons`, has `semantic_symbol_required` metadata, and is either a generated matching asset or a justified `native_framework_geometry` exception.
- No Coarse Asset Gate: composite visual regions are split into subregions or explicitly justified; broad assets cannot hide missing clouds, arrows, rain, icons, or legend details.
- Reference-Guided Asset Gate: every complex generated item has a prompt tied to the selected master/source role and a similarity target; topic-only replacement prompts fail.
- Master Similarity Gate: the final preview visibly preserves the selected master/source structure, not just the same scientific topic.
- Truthful QA Gate: failed parity, missing fine regions, or obvious preview divergence must be recorded as failed with `parity_failure_reason` and `redo_required: true`; never write `passed` to make the package look complete.
- No Crop Gate: `asset_manifest.json`, package folders, and final PPTX/SVG contain no master/source-derived asset regions and no extraction-type manifest values.
- Generated Asset Gate: every complex raster asset has an independent no-text prompt or procedural generation note, raw chroma image, transparent PNG/WebP, placement target, and alpha audit.
- No Text In Asset Gate: generated assets contain no text, numbers, titles, or legend wording; all scientific wording is native editable text.
- Canvas Bounds Gate: every PPTX/SVG object is within the declared canvas.
- Anti-Regression Gate: old crop/extraction fields and folders are absent from the package and manifests.
- No text overlap, clipping, edge spill, tiny labels, low contrast, or unreadable legend.
- Alpha audit and contact sheet exist when transparent assets are used.
- PPTX has no missing relationships, notes leftovers, or slide number placeholders.
- Submission-bound figures record whether AI-generated assets are excluded, replaced, disclosed, or explicitly accepted by the user.
