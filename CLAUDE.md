# WorldPolicies — agent guide

The **validated index of Robocurve's published robot-policy checkpoints**. Sibling of
[worldevals](https://github.com/robocurve/worldevals) (benchmarks); same conventions:
typed registry in `src/worldpolicies/catalog.py`, CI-validated entries, 100% coverage gate.

## Adding a checkpoint (the usual task here)

1. The model must already be on the HF robocurve org with a card passing
   https://github.com/robocurve/worldevals/blob/main/docs/model-cards.md (gating checklist).
2. Add it to the HF Collection: `huggingface_hub.add_collection_item(collection_slug,
   item_id=<hf_id>, item_type="model")` — slug via `list_collections(owner="robocurve")`.
3. Append a `Policy(...)` to `catalog.py`. `tests/test_catalog.py` validates every field
   (hf_id under robocurve/, method/metric enums, GitHub URL shape, nonempty fields) — a
   malformed entry fails CI. Update the README table too (kept by hand; keep rows sorted
   with the newest last, and note protocol comparability).

## Gotchas

- `main` is expected to gain branch protection like worldevals (PRs + checks). Dev loop:
  `uv venv && uv pip install -e ".[dev]" && uv run pytest --cov` (coverage must stay 100%).
- Eval numbers across rows are NOT comparable unless the protocol matches — never present
  the table as a leaderboard; per-protocol comparisons only.
- **PyPI readme is transformed at build time** — `hatch-fancy-pypi-readme` rewrites
  GitHub-only alert syntax (`> [!NOTE]` etc.) in README.md into bold blockquotes
  (`> **Note:**`) that PyPI renders; keep using alert syntax in the README itself.
  Config lives at the bottom of pyproject.toml.

## Writing style (public-facing text)

READMEs, docs pages, repo/collection descriptions, and HF model cards must
avoid AI-writing tells. The full rule with the gating checklist lives in
[worldevals docs/model-cards.md, "Writing style"](https://github.com/robocurve/worldevals/blob/main/docs/model-cards.md);
short version:

- No em dashes in prose. Use periods, colons, commas, or parentheses (`—` is
  fine as an empty table cell and inside code blocks).
- Bold only for definition-list lead-ins (`**term:**`) and at most one critical
  imperative per safety bullet. Never mid-sentence for emphasis.
- No decorative emoji (functional ✅/⚠️ marks and 🤗 for Hugging Face are fine),
  no slogans or chiasmus, no "not just X, but Y".
- Headers use colons, never em dashes or italics.

Style-only edits must never touch YAML frontmatter, code blocks, numbers,
links, or safety qualifiers.
