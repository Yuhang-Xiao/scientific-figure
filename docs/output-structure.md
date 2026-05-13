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
  icon_sheets/
  split_icons/
  generated_single_assets/
  source_crops/

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
- `02_image2_master`: Image2 master images. Keep failed/problematic masters in `rejected_or_buggy/`.
- `03_assets_raw`: unprocessed assets: icon sheets, split icons, single generated assets, and crops from source images.
- `04_assets_cutout`: transparent-background PNG/WebP assets plus alpha/contact-sheet QA.
- `05_assets_vector`: SVG wrappers, true vectorization candidates, and comparison previews. Never mix wrappers with true path vectors without notes.
- `06_editable_pptx`: final editable PPTX and PPTX package validation.
- `07_svg_export`: final SVG and SVG render notes.
- `08_previews`: human-facing previews and comparison images.
- `09_manifests`: machine-readable navigation and editability records.
- `10_qa`: human QA, policy notes, known issues, and visual inspection notes.
- `_archive`: intermediate build output and discarded versions. Final delivery must not depend on it.

## Manifest Requirements

`output_index.json` must include:

- `figure_slug`
- `mode`
- `package_root`
- `final_pptx`
- `final_svg`
- `preview_pptx`
- `preview_svg`
- `selected_master`
- `transparent_asset_dir`
- `asset_manifest`
- `editability_manifest`
- `qa_notes`
- `known_issues`

`asset_manifest.json` must include for each asset:

- asset key and role
- source path or generation prompt
- raw path
- cutout path, if any
- SVG wrapper path, if any
- placement target
- editability type
- policy risk

`editability_manifest.json` must include:

- native editable PPTX/SVG elements
- transparent image assets
- SVG wrappers
- true vectorized candidates
- non-editable or unresolved elements

## Naming Rules

- Final deliverables use the figure slug: `<figure_slug>.pptx`, `<figure_slug>.svg`.
- Previews use stable names: `preview_pptx.png`, `preview_svg.png`.
- Use `_archive/intermediate_build/` for tool-specific build names or temporary outputs.
- Do not leave final files only in `_archive` or `build`.
