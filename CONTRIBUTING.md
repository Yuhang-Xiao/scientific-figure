# Contributing

Contributions should preserve the core workflow:

```text
Image2 visual master/assets -> transparent assets -> editable PPTX/SVG rebuild -> QA package
```

## Good Contributions

- Improve the skill instructions without making them bloated.
- Add focused references under `docs/` or `skill/scientific-figure-workflow/references/`.
- Add lightweight examples that do not include large generated artifacts.
- Improve QA checks for PPTX packages, alpha assets, text overflow, or manifest completeness.
- Clarify journal policy, palette, or editability guidance with sources.

## Avoid

- Replacing the workflow with a raster-only screenshot pipeline.
- Calling SVG wrappers around PNGs true editable vectors.
- Adding large generated packages to Git.
- Adding secrets, API keys, local cache files, or private research data.

## Validation

Run:

```powershell
python -X utf8 C:\Users\Administrator\.codex\skills\.system\skill-creator\scripts\quick_validate.py .\skill\scientific-figure-workflow
```

If a change touches examples, check that `examples/lightweight/09_manifests/output_index.json` still points to existing files.
