# AI Image Policy For Scientific Figures

Use this reference whenever a figure may be submitted to a journal, publisher, thesis repository, grant body, or conference.

## Default Rule

For real submission, treat Image2 outputs as visual masters, concept drafts, or style references. The final deliverable should be rebuilt from editable, author-controlled objects plus transparent assets whose use is documented.

Do not assume AI-generated images are allowed in the final submitted figure. Ask for the target journal or publisher and verify its policy when the figure is intended for submission.

## Operational Policy

- If the user says the figure is for manuscript submission, ask for the target journal/publisher before finalizing.
- If the target policy is unknown, mark Image2 assets as "concept/reference only" in `QA_notes.md`.
- If Image2 assets remain in the final figure, record this in `asset_manifest.json` and `QA_notes.md`.
- If the journal prohibits AI-generated artwork, replace generated assets with author-created data graphics, user-provided images, or verifiable licensed/official assets.
- Never hide AI asset provenance in internal QA notes; do not add provenance text to the visual figure unless required by the venue.

## Known Publisher Direction

- Springer Nature editorial policy states that generative AI images are generally not permitted for publication unless specifically allowed in limited circumstances.
- Elsevier journal policy states that generative AI or AI-assisted tools must not be used to create or alter images in submitted manuscripts, including graphical abstracts, unless part of the research design or permitted under a specific exception.
- Policies change; verify the current target venue before relying on a generated asset.

Primary references:
- https://www.springer.com/us/editorial-policies/artificial-intelligence--ai-/25428500
- https://www.elsevier.com/about/policies-and-standards/generative-ai-policies-for-journals
