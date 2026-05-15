# Output Structure

Every run creates one self-contained work package:

```text
<figure_slug>_<YYYYMMDD_HHMM>/
```

Use ASCII slugs when possible. Keep user-facing titles inside request notes and manifests.

## Directory Contract

```text
00_request/
  user_prompt.md
  preflight_choices.json
  mode.json

01_inputs/
  source_images/
  user_assets/
  notes/

02_image2_master/
  master_raw/
  master_selected/
  rejected_or_buggy/
  master_prompt.md

03_assets_raw/
  generated_single_assets/
  rejected_or_buggy/

04_assets_cutout/
  transparent_png/
  contact_sheets/
  alpha_audit.csv
  background_removal_notes.md

05_assets_vector/
  svg_wrappers/
  vectorized_candidates/
  vectorization_comparison/
  vectorization_notes.md

06_editable_pptx/
  <figure_slug>.pptx
  pptx_validation.json

07_svg_export/
  <figure_slug>.svg
  svg_render_notes.md

08_previews/
  preview_pptx.png
  preview_svg.png
  contact_sheet.png
  comparison_master_vs_editable.png

09_manifests/
  asset_manifest.json
  editability_manifest.json
  master_layout_manifest.json
  visual_diff_report.json
  output_index.json

10_qa/
  QA_notes.md
  visual_qa.md
  policy_check.md
  known_issues.md

_archive/
  intermediate_build/
  discarded_versions/
```

## Directory Meaning

- `00_request`: original user request, preflight gate choices, and selected mode.
- `01_inputs`: only user-provided images, reference files, local icons, or notes.
- `02_image2_master`: Image2 master images. Keep failed/problematic masters in `rejected_or_buggy/`. These images are layout contracts, not asset sources.
- `03_assets_raw`: unprocessed independently generated no-text assets. Do not store master/source-derived regions here.
- `04_assets_cutout`: transparent-background PNG/WebP assets plus alpha/contact-sheet QA.
- `05_assets_vector`: SVG wrappers, true vectorization candidates, and comparison previews. Never mix wrappers with true path vectors without notes.
- `06_editable_pptx`: final editable PPTX and PPTX package validation.
- `07_svg_export`: final SVG and SVG render notes.
- `08_previews`: human-facing previews and comparison images.
- `09_manifests`: machine-readable navigation, layout contract, parity, asset, and editability records.
- `10_qa`: human QA, policy notes, known issues, and visual inspection notes.
- `_archive`: intermediate build output and discarded versions. Final delivery must not depend on it.

Forbidden package content: any raw asset created by cutting, splitting, masking, tracing, or background-removing a local region from an Image2 master, user source image, screenshot, or reference figure.

## Manifest Requirements

`output_index.json` must include:

- `figure_slug`
- `mode`
- `package_root`
- `final_pptx`
- `final_svg`
- `preview_pptx`
- `preview_svg`
- `comparison_master_vs_editable`
- `selected_master`
- `transparent_asset_dir`
- `asset_manifest`
- `editability_manifest`
- `master_layout_manifest`
- `visual_diff_report`
- `qa_notes`
- `known_issues`

`master_layout_manifest.json` must include:

- canvas size and aspect ratio
- panel structure, title bars, frames, legends, and conclusion boxes
- text zones and source/master text transcription
- complex visual regions with `master_region_bbox` or `source_layout_bbox`
- `fineRegions`, `routeSegments`, `legendItems`, and `smallIcons`
- `region_granularity` for each meaningful region, so composite areas cannot hide missing sub-elements
- semantic symbol coverage for warning signs, result-card icons, inset maps, gauge/thermometer art, vapor-arrow groups, moisture-transport bundles, rain-mark groups, and conclusion/protection icons
- directional route symbol coverage for curved cascade arrows, multi-arc dashed routes, thick gradient transition arrows, route bundles, and embedded arrowhead artwork
- reference-guided asset factory status for each complex item
- approved deviations, if any

`asset_manifest.json` must include for each generated asset:

- asset key and role
- `implementation_type` set to `generated_matching_asset` unless it is native geometry or an approved omission
- `master_region_bbox` or `source_layout_bbox` as layout reference only
- `region_granularity`
- `master_visual_role`
- `asset_similarity_target`
- `semantic_symbol_required` when the asset is a meaning-bearing symbol from the master/source
- `symbol_family`
- `master_symbol_bbox`
- `single_asset_prompt` or procedural generation note
- `reference_guided_prompt`
- `reference_guided_symbol_prompt` when applicable
- `directional_symbol_required` when the asset is meaning-bearing route or arrow artwork
- `route_symbol_family`
- `master_route_bbox`
- `reference_guided_route_prompt`
- `arrow_direction_status`
- `arrowhead_expected_at`
- `native_connector_endpoint_policy`
- `coarse_asset_forbidden`
- `chroma_key_color`
- `raw_chroma_path`
- `transparent_path`
- `placement_target_bbox`
- `alpha_status`
- `symbol_parity_status` when applicable
- `native_exception_reason` only when a semantic-looking symbol is intentionally represented by native framework geometry
- `parity_failure_reason`
- `redo_required`
- `editability_type`
- policy risk

`editability_manifest.json` must include:

- native editable PPTX/SVG elements
- route geometry and arrow editability notes
- directional route symbol coverage status
- saved PPTX connector endpoint audit status
- transparent image assets
- SVG wrappers
- true vectorized candidates
- non-editable or unresolved elements
- explicit statement that no master/source-derived regions were used as assets

`visual_diff_report.json` must include:

- layout parity status
- content parity status
- asset parity status
- route/arrow parity status
- small icon and legend parity status
- semantic symbol coverage status
- directional route symbol coverage status
- fine region coverage status
- no coarse asset status
- reference-guided asset status
- master similarity status
- truthful QA status
- no-crop gate status
- unresolved issues or accepted deviations

Gate values must be truthful. If the final preview is visibly a simplified same-topic redesign rather than a master/source-aligned rebuild, set the relevant gate to `failed`, write `parity_failure_reason`, and set `redo_required: true`.

## Naming Rules

- Final deliverables use the figure slug: `<figure_slug>.pptx`, `<figure_slug>.svg`.
- Previews use stable names: `preview_pptx.png`, `preview_svg.png`.
- Use `_archive/intermediate_build/` for tool-specific build names or temporary outputs.
- Do not leave final files only in `_archive` or `build`.
