# KF-REVIEW-SPEC — the independent Key Features / Specifications reader (one Sonnet agent per batch; added 2026-09-07, STR-DUB-2-batch1, user decision)

Purpose: a second, independent reading of the source PARAGRAPHS against the extract's `key_features` and `specs` lists by an
agent that did NOT write the descriptions and does not see them — only the supplier's own paragraphs and the two lists we
extracted. para_feat.py matches words; this agent reads meaning. It marks; it never writes a list item, never edits a file.
Reason: in STR-DUB-2-batch1 45 of 48 products left extraction with exactly the script's list, and the paragraph-only
features (p08 "no soaking or straining", p22 "the wood diffuses a soft glow", p30 "ABS shell", p44 "4-inch cushioning")
were found only by the main context reading para_feat's output by hand. Cost ≈ 0.05–0.1M tokens per 50 products.

Runs in README step 3c, after para_feat.py and BEFORE the title step (so the extract is complete when titles and
descriptions are written). Never Haiku.

## Inputs (working dir /home/claude/work)
- `kf_review_input.json` — written by `python3 kf_review_input.py` (zero tokens): one entry per ELIGIBLE product:
  `{"idx": NN, "identity": "...", "paragraphs": ["sentence", ...], "key_features": [...], "specs": ["Name: value", ...], "package": [...]}`.
  Eligible = the source's paragraph text (outside lists / spec / package / FAQ sections) is longer than 80 words; shorter
  sources are a heading plus the list the script already copied and are skipped (`--all` forces every product). The
  script prints `kf_review_input: N eligible of M`.
- rules/description-format-rule.md §4 (Key Features) and §5 (Specifications) — read those two sections; nothing else.
- RULINGS.md — a value or line RULINGS.md drops is not marked.

## What to mark — CERTAIN misses only
For each product read the paragraphs sentence by sentence and mark:
1. **KF miss** — a CONCRETE feature the paragraphs state (mechanism, material, function, mode, capacity, control, mounting,
   use setting, what the user no longer has to do: "no soaking or straining") that no `key_features` line and no `specs`
   pair carries. Same fact in other words in a list line = NOT a miss.
2. **SPEC miss** — a measurable or categorical VALUE the paragraphs state (number+unit, count, rating, material name,
   colour, compatibility, care instruction such as "machine washable") that no `specs` pair carries, in the source's own
   figure and unit. A package item or a variant option is not a spec miss.
Do NOT mark: marketing sentences ("elevates your space", "perfect for any occasion"), restatements of a listed line, use
audiences / occasions, anything the source only implies, anything RULINGS.md drops. When in doubt, do not mark.

## Output — `kf_review.json` and nothing else in the reply
`[{"idx": NN, "kind": "KF"|"SPEC", "source": "<the paragraph sentence verbatim>", "suggest": "<Name: one short sentence
in the source's words — a proposal only, the main context decides>"}]`; `[]` when none.
Reply to the main context with ONLY: `kf-review: N marked (K KF, J SPEC) on M products` and the list `NN | kind | source
sentence (first 80 chars)`.

## Main-context part (README 3c)
Read every mark: a real miss → add it to `extract/pNN.json` (key_features or specs) and to `para_feat_added.json` (so
extract_check.py counts it in the "added by main" column); a wrong mark → dismiss, no action. Then re-run
`python3 para_feat.py --gate` (a spec figure just added must resolve) and continue to step 4. The run log carries
`KF/spec independent review: N eligible of M, K marked, J confirmed and added (pNN …), K-J dismissed` — a log without
this line means the step was skipped; `0 eligible` is a valid line (structured sources) and says so.
