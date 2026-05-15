# Image To Editable

Use this reference for Mode B when the user provides an existing PNG/JPG/screenshot/reference figure.

## Goal

Rebuild the figure as editable PPTX/SVG while preserving the original visual logic. The final figure should not be a screenshot pasted into a slide, and no local region of the source image may be reused as a final or intermediate asset.

The source image is a structure contract: use it for layout, coordinates, text transcription, hierarchy, and parity checking only.

## Workflow

1. Save all source images in `01_inputs/source_images/`.
2. Inspect the image and write `01_inputs/notes/source_understanding.md`:
   - figure type
   - panel structure
   - domains/objects
   - text labels
   - arrows/connectors/routes
   - icon/illustration regions
   - chart/table regions
   - small semantic icons and legend symbols
3. Write `09_manifests/master_layout_manifest.json` before rebuilding. Include canvas size, panel boxes, text zones, asset regions, route geometry, `fineRegions`, `routeSegments`, `legendItems`, and `smallIcons`.
4. Decide implementation boundaries for every visible item:
   - native editable: text, arrows, panels, boxes, lanes, routes, simple symbols, chart/table structures
   - generated matching asset: complex icons, scientific mini-illustrations, microscopy-like imagery, highly styled generated glyphs
   - vectorization candidate: only simple flat icons or line-art elements when the user requires path editability
   - approved omission: only when explicitly accepted and recorded
5. Run the Reference-Guided Asset Factory. Generate each complex visual element as an independent no-text asset on a flat chroma-key background, using the source/master only as a reference for style, role, angle, proportions, and placement. Store raw outputs in `03_assets_raw/generated_single_assets/`.
6. Remove only the generated asset backgrounds into `04_assets_cutout/transparent_png/`, then create contact sheets and alpha audits.
7. Rebuild the framework with Presentation/SVG native objects.
8. Place generated transparent assets to match the source layout and proportions.
9. Export final files and write manifests, visual diff notes, and QA files.

## Reference-Guided Asset Factory

This stage is mandatory for all complex image-like content after a master/source has been selected.

- Do not generate replacement assets from the topic alone. Prompt each asset to match the selected master/source region's visual role, viewpoint, style, object density, and target proportions.
- Do not satisfy a detailed figure with a few broad assets. Split composite regions when the master/source contains independently positioned clouds, rain groups, maps, gauges, state tiles, warning symbols, legend icons, or result-card icons.
- Keep all text, arrows, route geometry, frames, section bars, legend labels, badges, and conclusion boxes as native editable objects unless the user explicitly approves otherwise.
- If an asset is visibly unlike the master/source role, contains generated text, has a bad matte, or forces the layout to drift, reject it and record `parity_failure_reason` plus `redo_required: true`.

## Source Mapping

For Mode B, `asset_manifest.json` or `editability_manifest.json` must include a source-to-output mapping. Source coordinates are layout references only, not extraction instructions:

```json
{
  "source_element": "upper-left cell illustration",
  "source_layout_bbox": [120, 90, 260, 180],
  "final_element": "environment_sensor_asset",
  "implementation_type": "generated_matching_asset",
  "single_asset_prompt": "no-text environmental sensor illustration matching the source role and style",
  "reference_guided_prompt": "generate one no-text environmental sensor matching the source region's style, angle, and proportions on a flat chroma-key background",
  "region_granularity": "single semantic complex asset",
  "master_visual_role": "upper-left cell illustration",
  "asset_similarity_target": "same role, similar viewpoint, similar scale, no source pixels reused",
  "coarse_asset_forbidden": true,
  "raw_chroma_path": "03_assets_raw/generated_single_assets/environment_sensor_raw.png",
  "transparent_path": "04_assets_cutout/transparent_png/environment_sensor.png",
  "placement_target_bbox": [120, 90, 260, 180],
  "alpha_status": "passed",
  "parity_failure_reason": null,
  "redo_required": false,
  "editability_type": "transparent image asset; movable/scalable/replaceable, internal paths not editable"
}
```

Use approximate regions if exact computer-vision coordinates are not available.

## When To Generate Similar Assets

Generate a similar no-text Image2/procedural asset when:

- the source region is a complex image-like illustration;
- the source asset cannot be reused due to licensing/provenance concerns;
- the user wants a cleaner top-journal style;
- background removal would otherwise require cutting from the source image;
- the source is too low-resolution or compressed to reproduce cleanly as an editable package.

Generated replacements must be recorded in `asset_manifest.json` and must not alter the scientific meaning.

## Do Not

- Do not paste the original PNG/JPG as the final background.
- Do not cut, mask, extract, trace, or background-remove any region from the source image for use as an asset.
- Do not create raw-asset folders for master/source-derived regions.
- Do not write extraction-type implementation values into any manifest.
- Do not invent labels or mechanisms that are not visible or requested.
- Do not redraw complex scientific illustrations by hand if that reduces quality.
- Do not let a simplified same-topic redraw pass as an editable rebuild. If `comparison_master_vs_editable.png` obviously does not match the source/master structure, mark QA failed and redo.
- Do not claim transparent PNG/WebP assets or SVG wrappers are true editable path vectors.
