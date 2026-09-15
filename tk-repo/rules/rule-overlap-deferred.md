# Rule 8.2 — catalog-wide title overlap (DEFERRED until the catalog is fully rewritten; re-issue then)

Deferred by the user on 2026-09-04 after blr-batch12. Not run per batch. To be run ONCE, as its own batch, after the last
product batch is pushed.

## The rule (title-format-rule.md §8, verbatim)
- 8.1 — The first 40 characters of a title must be unique across the catalog. On a collision, the lower-priority product moves
  its own distinguishing cluster to the front — its opener must still be its highest-volume keyword (rule 3.2).
- 8.2 — Word overlap between any two titles must stay under 60%. Report every pair that exceeds it.
- Priority when deciding which product keeps the contested title: highest price first, then best seller, then most complete
  product data.
- Product fit outranks uniqueness (§6): never misrepresent a product to reduce overlap; re-cut the differentiating cluster
  using genuine attributes, or accept the overlap and report the pair. Report beats misrepresent.

## How it will be run (catalog end)
1. Fetch every product's id, title, status, price (script, read-only; ~7,300 products, no model tokens).
2. Scope: all products, or ACTIVE only — the user decides at re-issue time (draft products are not in the Shopping feed).
3. Overlap = shared content words / min(word count of the two titles), stop-words removed (ov.py definition). Report every
   pair ≥60% where both titles have ≥4 content words; list 2–3-word legacy titles separately (denominator artefact).
4. For each pair: decide the keeper by the priority order; rewrite the other product's title per the full title procedure
   (measured keywords, §2–§7, tail zone, alts regenerated from the new title, backup-titles doc before push, verify after).
5. Run log: every pair, the keeper, the rewrite, and any pair left overlapping with its reason.

## Known state at deferral
blr-batch12 audit (2026-09-04): 68 pairs ≥60% against titles with ≥4 content words, plus 70 against 2–3-word legacy titles.
List reproducible with `python3 audit.py | grep 8.2` in the batch12 workspace; examples: #06 vs "Night Vision Binoculars"
(100%), #35 vs "RC Cars for Kids, Wall Climbing Car with LED Lights…" (71%), #23 vs "Vegetable Chopper Manual Stainless
Steel Food Chopper…" (73%).
