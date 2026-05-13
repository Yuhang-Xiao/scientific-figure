# Vectorization

Use this reference when the user asks for icon internals to be editable or when a simple image asset might be converted into paths.

## Default

Keep complex scientific icons and mini-illustrations as transparent PNG/WebP assets. They are movable, scalable, crop-able, and replaceable in PPTX, but their internal paths are not editable.

## Candidate Tools

- VTracer: useful for colorful raster-to-SVG conversion.
- Potrace: useful for simple black-and-white or thresholded line art.
- Inkscape Trace Bitmap: useful for manual or CLI-assisted tracing and cleanup.
- PowerPoint SVG conversion/ungrouping: sometimes useful for simple SVGs, but can create many shapes or break visual fidelity.

## Decision Rule

Attempt vectorization only when all are true:

- the icon is simple, flat, and has clear edges;
- the result can remain visually close to the source or Image2 master;
- path complexity will not make the PPTX slow or fragile;
- the user asked for internal editability or the project requires it.

## Output Placement

- SVG wrappers around PNGs go in `05_assets_vector/svg_wrappers/`.
- True path-vector candidates go in `05_assets_vector/vectorized_candidates/`.
- Side-by-side comparison previews go in `05_assets_vector/vectorization_comparison/`.
- Decisions and failures go in `05_assets_vector/vectorization_notes.md`.

## QA

For each vectorized candidate, record:

- source asset path
- tool and command used
- whether the output is true path vector
- visual fidelity status
- node/shape complexity risk
- accepted or rejected

If the vectorized version diverges from the approved visual, reject it and use the transparent asset.

References:
- https://github.com/visioncortex/vtracer
- https://potrace.sourceforge.net/
- https://inkscape-manuals.readthedocs.io/en/latest/tracing-an-image.html
