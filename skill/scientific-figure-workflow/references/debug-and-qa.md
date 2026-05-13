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

## Required QA Files

- `06_editable_pptx/pptx_validation.json`
- `08_previews/preview_pptx.png`
- `08_previews/preview_svg.png`
- `09_manifests/output_index.json`
- `09_manifests/asset_manifest.json`
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

## Policy Gate

For submission-bound figures:

- Record target journal/publisher.
- Verify or summarize AI image policy.
- Mark Image2 assets as concept-only unless allowed.
- Record whether AI assets were excluded, replaced, disclosed, or accepted by the user.
