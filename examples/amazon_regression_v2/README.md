# Amazon Regression V2

This is a lightweight tracked record of the Amazon deforestation/drought threshold regression run used to verify the global Reference-Guided Asset Factory workflow.

The complete generated package remains local-only under:

```text
scientific_figure_workflow_test/amazon_deforestation_drought_threshold_v2_20260514_2221/
```

That directory is intentionally ignored by git because it contains heavy PPTX/SVG deliverables, Image2 masters, raw chroma assets, transparent PNG assets, and intermediate build files.

## Included

- `08_previews/comparison_master_vs_editable.png`
- `09_manifests/output_index.json`
- `09_manifests/asset_manifest.json`
- `09_manifests/master_layout_manifest.json`
- `09_manifests/visual_diff_report.json`
- `09_manifests/editability_manifest.json`
- `10_qa/QA_notes.md`
- `build_amazon_threshold_package_v2.py`

## Regression Purpose

The v2 package demonstrates that the workflow must not simplify an Image2 master into a same-topic schematic. It records a rebuild that restores the mother figure's title bars, numbered cards, map legend, middle subpanels, cascade map, right result cards, threshold marker, and bottom conclusion icon.

## QA Summary

- PPTX package validation: passed.
- Transparent assets: 11.
- Alpha audit: all passed.
- No crop/split-source workflow terms were found in the complete v2 package.
- Complex visual internals remain transparent PNG assets; framework text, frames, arrows, routes, legend labels, result cards, and conclusion box remain editable objects.
