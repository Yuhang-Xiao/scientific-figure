# scientific-figure

`scientific-figure` is a Codex skill project for building top-journal-style scientific diagrams as editable deliverables. It turns either a drawing prompt or an existing PNG/JPG figure into a structured work package with editable PowerPoint, SVG export, transparent icon assets, previews, manifests, and QA notes.

The workflow keeps the visual power of Image2 while avoiding the usual trap of shipping a flat screenshot. Image2 is used as a visual master and asset source; the final figure is rebuilt with editable Presentation/SVG objects for text, arrows, panels, routes, labels, and data structure. Complex icons and mini-illustrations remain transparent assets by default.

![Example PPTX preview](examples/lightweight/08_previews/preview_pptx.png)

## Why This Exists

Scientific figures often need two things at once:

- publication-grade visual polish
- editable structure for papers, slides, revisions, and reviewer feedback

Generated images are good at composition and style, but poor at stable text and editability. Manual PowerPoint rebuilding is editable, but can look plain. This skill combines both approaches with explicit QA and file organization.

## What It Does

- Creates new scientific workflow figures from prompts.
- Converts existing PNG/JPG diagrams into editable PPTX/SVG reconstructions.
- Separates complex icons into transparent image assets.
- Keeps final labels, arrows, panels, routes, and boxes editable.
- Records preflight choices before drawing.
- Produces a numbered output package so every file has a clear purpose.
- Warns when Image2 assets are concept-only for journal submission.

## Two Workflows

### Mode A: Prompt-to-Figure

Use this when you have a research topic or figure prompt.

```text
用 $scientific-figure-workflow 画一个食品安全风险预测技术路线图，顶刊风格，中英文标签，输出PPTX、SVG、原图和透明图标。
```

### Mode B: Image-to-Editable

Use this when you already have a PNG/JPG/screenshot/reference figure.

```text
用 $scientific-figure-workflow 把 D:\path\figure.png 转成可编辑流程图，提取其中图标并抠透明，输出PPTX和SVG。
```

## Preflight Hook

Before drawing or rebuilding, the skill asks or confirms:

- mode: prompt-to-figure or image-to-editable
- purpose: submission, presentation, proposal, manuscript draft, or internal concept
- figure type
- tone and palette
- target journal/style standard
- editability boundary
- output root and figure slug
- other requirements such as language, aspect ratio, panel count, or icon editability

The choices are saved to:

```text
00_request/preflight_choices.json
```

## Output Package

Each run creates:

```text
<figure_slug>_<YYYYMMDD_HHMM>/
```

Start here:

```text
09_manifests/output_index.json
08_previews/preview_pptx.png
06_editable_pptx/<figure_slug>.pptx
07_svg_export/<figure_slug>.svg
10_qa/QA_notes.md
```

Full package structure is documented in [docs/output-structure.md](docs/output-structure.md).

## Installation

Copy the skill folder into your Codex skills directory:

```powershell
Copy-Item -Recurse .\skill\scientific-figure-workflow "$env:USERPROFILE\.codex\skills\scientific-figure-workflow" -Force
```

Restart Codex if the skill list does not refresh automatically.

## Documentation

- [Usage](docs/usage.md)
- [Output structure](docs/output-structure.md)
- [Debug and QA](docs/debug-and-qa.md)
- [Image-to-editable workflow](docs/image-to-editable.md)
- [Vectorization boundaries](docs/vectorization.md)
- [Journal standards](docs/journal-standards.md)
- [AI image policy](docs/ai-policy.md)
- [Palettes](docs/palettes.md)
- [Editability boundaries](docs/editability-boundaries.md)

## Example

The lightweight example in [examples/lightweight](examples/lightweight) includes:

- a final preview image
- output index
- asset manifest
- editability manifest
- QA notes

Large generated images, PPTX files, and intermediate build artifacts are intentionally excluded from the public example.

## Limitations

- Transparent PNG/WebP icon assets are movable and scalable, but their internal paths are not editable.
- SVG wrappers around PNG assets are not true path-vectorized icons.
- Image2 may generate unwanted text or non-flat chroma backgrounds; the workflow records and fixes or discloses these issues.
- For real journal submission, always check the target journal policy before using AI-generated image assets in final artwork.

## Validation

Skill validation:

```powershell
python -X utf8 C:\Users\Administrator\.codex\skills\.system\skill-creator\scripts\quick_validate.py .\skill\scientific-figure-workflow
```

Installed-skill validation:

```powershell
python -X utf8 C:\Users\Administrator\.codex\skills\.system\skill-creator\scripts\quick_validate.py C:\Users\Administrator\.codex\skills\scientific-figure-workflow
```

## Project Status

Early public release. The workflow has been tested with a bilingual cross-domain scientific figure package and is designed to be extended through examples and stricter QA scripts.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT. See [LICENSE](LICENSE).
