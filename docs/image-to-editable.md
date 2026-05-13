# Image To Editable

Use this reference for Mode B when the user provides an existing PNG/JPG/screenshot/reference figure.

## Goal

Rebuild the figure as editable PPTX/SVG while preserving the original visual logic. The final figure should not be a screenshot pasted into a slide.

## Workflow

1. Save all source images in `01_inputs/source_images/`.
2. Inspect the image and write `01_inputs/notes/source_understanding.md`:
   - figure type
   - panel structure
   - domains/objects
   - text labels
   - arrows/connectors
   - icon/illustration regions
   - chart/table regions
3. Decide editability boundaries:
   - native editable: text, arrows, panels, boxes, lanes, routes, simple symbols, chart/table structures
   - transparent asset: complex icons, scientific mini-illustrations, microscopy-like imagery, highly styled generated glyphs
   - vectorization candidate: simple flat icons or line-art elements
4. Crop raw icon/source regions into `03_assets_raw/source_crops/`.
5. Cut out transparent assets into `04_assets_cutout/transparent_png/` and generate contact sheets.
6. Rebuild the framework with Presentation/SVG native objects.
7. Place transparent assets to match the source layout.
8. Export final files and write manifests.

## Source Mapping

For Mode B, `editability_manifest.json` must include a source-to-output mapping:

```json
{
  "source_element": "upper-left icon group",
  "source_region": [x, y, width, height],
  "final_element": "environment_sensor_asset",
  "final_path": "04_assets_cutout/transparent_png/environment_sensor.png",
  "editability": "transparent image asset"
}
```

Use approximate regions if exact computer-vision coordinates are not available.

## When To Regenerate Similar Assets

Generate a similar Image2 asset only when:

- the source icon is too low-resolution to crop cleanly,
- the user wants a cleaner top-journal style,
- the source asset has a background or compression artifact that cannot be removed well,
- or the source asset cannot be reused due to licensing/provenance concerns.

Generated replacements must be recorded in `asset_manifest.json` and must not alter the scientific meaning.

## Do Not

- Do not paste the original PNG/JPG as the final background.
- Do not invent labels or mechanisms that are not visible or requested.
- Do not redraw complex scientific illustrations by hand if that reduces quality.
- Do not claim extracted PNG icons are true editable vectors.
