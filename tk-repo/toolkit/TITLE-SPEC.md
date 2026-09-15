# TITLE-SPEC — the single small-context title subagent (main model)

Inputs on disk: kw.txt (keyword|volume|comp|cpc), extract/pNN.json (identity + notes), RULINGS.md, candidates/cNN.json,
rules/title-format-rule.md (read IN FULL), cap.py, build_check.py, title-check.py, skip_reasons.json (you write it), source_windows.py + products.json (the
Phase 1 snapshot — title-check.py reads both). (§8 / ov.py is suspended in full — user decision 2026-09-05 — no overlap
check, no catalog titles needed.)

Procedure — for all N products in one context:
1. Per product: list the top ~25 measured candidates (volume, comp, cpc). Decide fit (§6) — every rejected keyword keeps its
   volume; put the regex families into build_check.py FR[i]. Add measured keywords used in a title but missing from the
   candidate set to EXTRA[i].
1b. If a keyword you need is not in kw.txt (the extraction agent's candidate list missed it), do NOT write it unmeasured: collect all
   such terms across the batch and measure them in ONE extra DataForSEO call (≤950 keywords, ~$0.09), append to kw.txt and
   to the product's EXTRA[i] in build_check.py, then continue. The candidate list never limits the title decision.
2. Build each title per §2–§4 and §7: highest-volume fitting keyword first, contiguous phrases, head noun ≤3 (prefer 2),
   70–120 chars; 120–135 only on trigger A/B and name the trigger; 145 never. Measure with `python3 cap.py "<title>"`.
   Units (§5 "Units in the title", user decision 2026-09-12): the store is a US store — any measurement in a title or SEO title
   is written in inch/ft/oz/lb (fl oz for liquids), never cm/mm/m/g/kg/ml/l. Convert the source value (`16 cm` → `6.3 in`,
   one decimal, drop `.0`); the converted value still has to pass §5 test 1 or 2 to enter at all.
3. Write producttype_draft.json ({"NN": "<§10b productType, Title Case singular>"}) next to titles_draft.json — title-check.py
   needs the head noun. Then `python3 build_check.py && python3 title-check.py kw.txt check_products.json` until 0 FAIL.
   Two FAILs are new and push-blocking (rule §3.2, 2026-09-05): an opener phrase that was never measured (fix: step 1b, measure
   it), and a captured higher-volume keyword that names the product type sitting behind the opener (fix: open on it, or
   fit-reject it with a written reason and remove it from the title). A third, batch-level FAIL (2026-09-06, rule §1): any
   2–4-word window of a source title missing from kw.txt — README step 4 was skipped; fix is to run
   `python3 source_windows.py products.json kw.txt`, measure the output in one DataForSEO call and append it to kw.txt, then
   re-check whether any title's opener changes (blr-batch24 #35: `essential oil diffuser` 74,000 had been unmeasured).
   A fourth FAIL (2026-09-06, §2/§3.7, user decision): a comma cluster with no measured 2+-word phrase inside it — the
   cluster's core must be a measured keyword; attributes before it and a for/with tail after it stay free (blr-batch24 #12
   had rewritten measured `robot vacuum for carpet` into unmeasured `Automatic Robotic Vacuum for Carpet`). Fix: rebuild
   the cluster around a measured keyword, or measure the phrase you mean (step 1b). Defining-number clusters (`10 Pack`,
   `Set of 4`) are exempt; apostrophes and word order do not matter.
   A fifth FAIL (2026-09-06, user decision): the OLD title captured more product-naming volume than the new one (keywords whose
   last word is the productType head, fit-rejects excluded on both sides) — "we changed it and made it worse". blr-batch24 #35:
   old `Salt Lamp Diffuser - 3-in-1 Essential Oil Diffuser` 96,460 vs new 15,060, because `essential oil diffuser` 74,000
   was dropped. Fix: put the lost keyword back (usually as the opener). A WARN on TOTAL volume (all keywords) is a hint
   only. check_products.json needs `old_title` (or `product_id` / a 2-digit index matching products.json).
   A sixth FAIL (2026-09-06, user decision, option b): a measured, fit-clean candidate (>= 1,000) that is not in the title and
   beats the WEAKEST non-opener cluster's value — the TRIMMERYENI #08 lesson (`cordless grass trimmer` 12,100 unused while
   `weed trimmer` 9,900 was written). Either put it in the title, or write ONE line per keyword in `skip_reasons.json`
   ({"NN": {"keyword": "reason"}} — e.g. "needs a 3rd Trimmer occurrence", "word order breaks the opener", "over 120 with
   no trigger"); a reason for a longer/shorter form of the phrase covers the family. With a reason the line becomes MANUAL
   and goes to rejects.json `skipped_with_reason` for the run log; without one it is a FAIL. "Sounded better" is not a reason.
   A seventh FAIL (2026-09-12, §5 Units, user decision): a number followed by a metric unit (cm, mm, m, g, kg, ml, l, or the
   spelled-out forms) in the title or the SEO title. Fix: convert to inch/ft/oz/lb, or drop the spec to the description.
   §8 overlap is not checked or reported.
4. Write titles_final.json (idx, product_id, handle, title, len, captured_volume, captured, sacrificed = rejects.json
   top-8, capped, fit_reject, tier reason) and backup-titles-<tag>.md (index, id, handle, old title, old SEO title, new title).
5. Return to the main context ONLY: total captured volume, count of titles per tier, the list of pairs still ≥60% (if any),
   and fit rejections ≥20,000 or >50% of captured volume with a one-line reason each. Nothing else.
