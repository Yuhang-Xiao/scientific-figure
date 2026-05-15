# Debug And QA

Use this reference before final delivery and whenever the workflow hits a visual or asset bug.

## Known Failure Modes

### Image2 Text Pollution

Image2 may create unwanted labels, pseudo-text, black strips, or irrelevant words even when prompted with `no text`.

Required response:

- Keep polluted masters in `02_image2_master/rejected_or_buggy/` if useful for audit.
- Do not reuse generated text as final labels.
- Add all final text natively in PPTX/SVG.
- Record the issue in `10_qa/known_issues.md`.

### Non-flat Chroma Backgrounds

Image2 may produce gradients or shadows on a requested flat chroma-key background.

Required response:

- Use threshold-based keying, edge sampling, despill, and small connected-component cleanup.
- Validate transparent corners, no halos, no missing internal white details, and no orphan fragments.
- Write `04_assets_cutout/alpha_audit.csv` and a contact sheet.

### Chinese Path / Encoding Issues

Windows + PowerShell + Python can corrupt absolute paths with Chinese characters when passed through inline scripts.

Required response:

- Prefer `Path.cwd()` plus relative paths inside scripts.
- Use UTF-8 explicitly for JSON/Markdown read-write.
- When validating skills on Windows, use `python -X utf8` if the file contains Chinese trigger words.

### Bilingual Text Crowding

Chinese + English labels can wrap or clip in compact panels.

Required response:

- Use short bilingual labels in the figure.
- Move long explanations to `00_request/notes/`, captions, or QA notes.
- Re-render preview after any text change.

### SVG Wrapper Confusion

An SVG file that embeds a transparent PNG is scalable but not path-editable.

Required response:

- Store wrappers in `05_assets_vector/svg_wrappers/`.
- Store true path-vector candidates separately in `05_assets_vector/vectorized_candidates/`.
- Record the difference in `editability_manifest.json`.

### Master/Source Region Extraction Regression

The workflow must not create assets by cutting regions out of an Image2 master, source screenshot, or reference figure.

Required response:

- Delete any raw-asset package path dedicated to master/source-derived regions before delivery.
- Reject manifests that use extraction-type implementation values or describe assets as split from an Image2 master/sheet/source image.
- Regenerate each complex visual as its own no-text asset on a flat chroma-key background.
- Record the original master/source bbox only as `master_region_bbox` or `source_layout_bbox` for placement and parity.
- Add the failure and the correction to `10_qa/known_issues.md`.

### Coarse Asset / Same-Topic Redraw Regression

The workflow must not replace a detailed master/source with a simplified same-topic schematic or a few broad generated assets.

Required response:

- Reopen the selected master/source and create or repair the fine-region inventory before assembly.
- Split broad complex regions into independently placed semantic parts when clouds, rain marks, maps, gauges, state tiles, warning icons, legend symbols, route marks, or conclusion icons affect the visible structure.
- Regenerate mismatched complex items with reference-guided prompts that name the master/source role, style, viewpoint, proportions, and placement target.
- Keep text, frames, section bars, badges, legends, arrows, dashed routes, and conclusion boxes as native Presentation/PPTX/SVG objects.
- Set `parity_failure_reason` and `redo_required: true` in manifests until the rebuilt preview visibly matches the master/source structure.

### Missing Semantic Symbol Assets

The workflow must not hand-draw or omit meaning-bearing master/source symbols just because they are small.

Required response:

- Reopen the selected master/source and identify warning signs, result-card icons, inset maps, gauge/thermometer art, vapor-arrow groups, moisture-transport bundles, rain-mark groups, and conclusion/protection icons.
- Add each symbol to `fineRegions` or `smallIcons` with `semantic_symbol_required`, `symbol_family`, `master_symbol_bbox`, `symbol_parity_status`, and an implementation.
- Generate missing semantic symbols as independent no-text chroma-key assets using reference-guided prompts; do not draw them manually from memory.
- Keep plain framework geometry native only when it is a normal connector, title bar, divider, frame, legend swatch, or text label; record `native_exception_reason`.
- Set `semantic_symbol_coverage_gate` to failed until each required symbol is generated, placed, or explicitly approved as omitted.

### Missing Or Reversed Directional Route Symbols

The workflow must not simplify or reverse meaning-bearing routes and arrows. A route can be editable native geometry only when it is a plain framework connector; complex route artwork must be generated as a matching no-text asset.

Required response:

- Reopen the selected master/source and identify curved cascade arrows, multi-arc dashed routes, thick gradient transition arrows, route bundles, and embedded arrowhead artwork.
- Add each route symbol to `routeSegments` or `fineRegions` with `directional_symbol_required`, `route_symbol_family`, `master_route_bbox`, `arrowhead_expected_at`, `arrow_direction_status`, and an implementation.
- Generate missing route symbols as independent no-text chroma-key assets using reference-guided prompts; do not replace them with generic straight or curved hand-drawn lines.
- For native connectors, audit the saved PPTX/OpenXML and verify the visible arrowhead is at the recorded destination end; fix endpoint tags before passing QA.
- Set `directional_route_symbol_coverage_gate` or `route_arrow_parity_gate` to failed until route shape, arrow direction, dash pattern, and arrowhead placement match.

## Required QA Files

- `06_editable_pptx/pptx_validation.json`
- `08_previews/preview_pptx.png`
- `08_previews/preview_svg.png`
- `09_manifests/output_index.json`
- `09_manifests/asset_manifest.json`
- `09_manifests/master_layout_manifest.json`
- `09_manifests/visual_diff_report.json`
- `09_manifests/editability_manifest.json`
- `10_qa/QA_notes.md`
- `10_qa/visual_qa.md`
- `10_qa/policy_check.md`
- `10_qa/known_issues.md`

## PPTX Package Gate

Pass only when:

- `missingRelationshipTargets` is empty.
- `notesEntries` is 0.
- `slideNumberPlaceholders` is 0.
- Final PPTX is under `06_editable_pptx/`.
- Preview rendered from the saved PPTX or a documented fallback exists.

## Visual Gate

Inspect full-size previews for:

- clipped text
- text-on-text collision
- icon distortion
- arrow ambiguity
- low contrast
- busy or irrelevant Image2 artifacts
- tiny bilingual labels
- cutout halos or orphan fragments
- mismatch between source/master and editable reconstruction
- missing complex visual assets in `ppt/media/*` when the master/source contains complex visual regions
- broad replacement assets that hide smaller semantic icons, route marks, legends, or state-transition details
- missing semantic symbol assets such as warning signs, stump/result icons, affected-area inset icons, vapor-arrow groups, moisture bundles, or rain-mark groups
- missing directional route symbols such as curved cascade arrow bundles, thick gradient transition arrows, or embedded route arrowheads
- reversed PPTX arrowheads after saving the actual `.pptx`
- final preview that looks like a same-topic redesign rather than the selected master/source

## Parity Gate

Pass only when:

- `comparison_master_vs_editable.png` shows close layout alignment with the selected master/source.
- `master_layout_manifest.json` lists fine regions, route segments, legend items, and small icons.
- `visual_diff_report.json` passes layout, content, asset, route/arrow, small icon, semantic-symbol coverage, directional-route-symbol coverage, fine-region coverage, no-coarse-asset, reference-guided-asset, master-similarity, truthful-QA, and no-crop gates.
- Every complex visual asset has `single_asset_prompt`, `raw_chroma_path`, `transparent_path`, `placement_target_bbox`, and `alpha_status`.
- Every generated complex asset also has `reference_guided_prompt`, `region_granularity`, `master_visual_role`, `asset_similarity_target`, `coarse_asset_forbidden`, `parity_failure_reason`, and `redo_required`.
- Every required semantic symbol has `semantic_symbol_required`, `symbol_family`, `master_symbol_bbox`, `reference_guided_symbol_prompt` or `native_exception_reason`, and `symbol_parity_status`.
- Every required directional route symbol has `directional_symbol_required`, `route_symbol_family`, `master_route_bbox`, `reference_guided_route_prompt` or `native_connector_endpoint_policy`, `arrowhead_expected_at`, and `arrow_direction_status`.

## Policy Gate

For submission-bound figures:

- Record target journal/publisher.
- Verify or summarize AI image policy.
- Mark Image2 assets as concept-only unless allowed.
- Record whether AI assets were excluded, replaced, disclosed, or accepted by the user.
