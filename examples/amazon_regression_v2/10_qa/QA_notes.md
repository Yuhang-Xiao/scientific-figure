# Amazon Regression V2 QA Notes

## Purpose

This lightweight example records the Amazon deforestation/drought threshold v2 regression run used to verify the global Reference-Guided Asset Factory workflow. The complete generated package remains local-only under `scientific_figure_workflow_test/` and is ignored by git.

## Included

- `08_previews/comparison_master_vs_editable.png`
- `09_manifests/output_index.json`
- `09_manifests/asset_manifest.json`
- `09_manifests/master_layout_manifest.json`
- `09_manifests/visual_diff_report.json`
- `09_manifests/editability_manifest.json`
- `build_amazon_threshold_package_v2.py`

## Omitted

- Editable PPTX and SVG deliverables
- Image2 master images
- Raw chroma assets
- Transparent PNG assets
- Intermediate build files

## QA Results

PPTX package validation from the complete local v2 package:

```json
{
  "pptx": "06_editable_pptx/amazon_deforestation_drought_threshold.pptx (omitted from lightweight example)",
  "slides": 1,
  "media_files": 10,
  "notesEntries": 0,
  "slideNumberPlaceholders": 0,
  "missingRelationshipTargets": [],
  "status": "passed"
}
```

Alpha audit summary: all 11 transparent assets passed.

```json
[
  {
    "asset_key": "warming_earth_thermometer",
    "alpha_status": "passed",
    "transparent_corners": "True",
    "subject_alpha_coverage": "0.4799"
  },
  {
    "asset_key": "amazon_deforestation_map",
    "alpha_status": "passed",
    "transparent_corners": "True",
    "subject_alpha_coverage": "0.413"
  },
  {
    "asset_key": "forest_evapotranspiration_scene",
    "alpha_status": "passed",
    "transparent_corners": "True",
    "subject_alpha_coverage": "0.4202"
  },
  {
    "asset_key": "deforested_agriculture_road_patch",
    "alpha_status": "passed",
    "transparent_corners": "True",
    "subject_alpha_coverage": "0.4512"
  },
  {
    "asset_key": "healthy_rainforest_state",
    "alpha_status": "passed",
    "transparent_corners": "True",
    "subject_alpha_coverage": "0.6148"
  },
  {
    "asset_key": "degraded_savanna_state",
    "alpha_status": "passed",
    "transparent_corners": "True",
    "subject_alpha_coverage": "0.523"
  },
  {
    "asset_key": "rain_cloud",
    "alpha_status": "passed",
    "transparent_corners": "True",
    "subject_alpha_coverage": "0.2536"
  },
  {
    "asset_key": "healthy_forest_panorama",
    "alpha_status": "passed",
    "transparent_corners": "True",
    "subject_alpha_coverage": "0.2842"
  },
  {
    "asset_key": "deforested_dry_panorama",
    "alpha_status": "passed",
    "transparent_corners": "True",
    "subject_alpha_coverage": "0.3225"
  },
  {
    "asset_key": "cascade_amazon_map",
    "alpha_status": "passed",
    "transparent_corners": "True",
    "subject_alpha_coverage": "0.3124"
  },
  {
    "asset_key": "conservation_leaf_shield",
    "alpha_status": "passed",
    "transparent_corners": "True",
    "subject_alpha_coverage": "0.2772"
  }
]
```

## Regression Finding

The v2 rebuild restores the selected Image2 master structure more faithfully than v1: title bars, left numbered cards, map legend, middle upper/lower subpanels, bottom cascade map, right result cards, threshold marker, and bottom conclusion icon are represented in the editable reconstruction.

## Boundary

The complex visual internals remain transparent PNG assets, not editable paths. Text, title bars, frames, arrows, routes, legend labels, result cards, threshold line, and conclusion box are editable framework objects.
