# Lightweight Example

This example is a small public-safe slice of a larger regression package.

Included:

- `08_previews/preview_pptx.png`
- `09_manifests/output_index.json`
- `09_manifests/asset_manifest.json`
- `09_manifests/editability_manifest.json`
- `09_manifests/master_layout_manifest.json`
- `09_manifests/visual_diff_report.json`
- `10_qa/QA_notes.md`

Excluded:

- full PPTX/SVG deliverables
- raw Image2 images
- transparent icon PNGs
- intermediate build output

The full package layout is documented in `docs/output-structure.md`.

See also `examples/amazon_regression_v2` for a focused regression record that checks the Reference-Guided Asset Factory and master-similarity QA gates against an Image2-to-editable mechanism figure.
