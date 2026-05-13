# Journal Figure Standards

Use this reference for publication-bound scientific figures. Always verify the exact target journal instructions when the user names a journal.

## Baseline Standard

- Prefer editable vector structure for line art, diagrams, labels, axes, arrows, and text. Use raster assets only for images or complex illustrations that are meant to remain image-like.
- Keep final labels native and editable whenever possible. Avoid relying on generated text inside the Image2 master.
- Use high contrast and colorblind-aware palettes. Color must encode meaning deliberately and remain readable in grayscale where possible.
- Use consistent typography, line weight, arrow style, margins, panel labels, and legend placement.
- Keep figure text large enough for final print/export scale. Avoid shrinking dense explanations into panels.
- Preserve data integrity: do not beautify charts by changing values, smoothing trends, omitting outliers, or redrawing unsupported relationships.

## Resolution And Format Defaults

- Editable diagram deliverables: PPTX plus SVG/PDF/EPS-style vector export when possible.
- Raster previews and image assets: PNG/WebP for transparent assets; TIFF/PNG for journal-oriented raster export.
- Common minimums: 300 dpi for continuous-tone images, 600 dpi for mixed text/image artwork, and 1000 dpi for pure line art when a raster export is required.
- Keep the editable source (`.pptx`, `.svg`, or source script/config) together with submission exports.

## Publisher Notes

- Nature figure guidance emphasizes preparing figures to specification before submission and checking dimensions, file types, resolution, fonts, line weights, and color mode.
- Elsevier artwork guidance distinguishes vector, bitmap, and combination artwork and expects suitable formats/resolution for each.
- PLOS and similar open journals emphasize readable labels, accessibility, and file preparation quality.

## Figure Design Gate

Reject or revise a figure if any of these are true:

- The visual depends on a raster screenshot as the only final layer.
- Critical text is embedded in a generated image instead of editable text.
- A palette has no semantic roles or colorblind consideration.
- Labels, arrows, icons, panel boundaries, or legends collide.
- Visual polish changes the scientific meaning.
- The output lacks a validated preview and an editability note.

Primary references:
- https://research-figure-guide.nature.com/figures/preparing-figures-our-specifications/
- https://www.elsevier.com/about/policies-and-standards/author/artwork-and-media-instructions
- https://plos.org/resource/how-to-prepare-figures/
