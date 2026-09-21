# Backend batch toolkit — how a NEW session runs a batch with these files (2026-09-03)

Every file here is a project doc; at session start a small agent copies them to /home/claude/work/
(`project_read` → disk), plus title-check.py and desc-check.py which are also project docs, and the rule
docs into rules/ — the rule docs are exactly the `./rules/…` lines of toolkit/MANIFEST.md, and that list
includes `rules/PROJECT-DESCRIPTION.md` (the Backend document itself, which DESC-SPEC.md requires read in
full); it was missing from the manifest until 2026-09-05 and had to be fetched by a separate agent every run. Rule docs
live at the project root except the three 2026-09-06 rule docs, whose project paths are `claude/comparison-table-rule.md`,
`claude/dimension-image-rule.md` and `claude/fit-block-rule.md` (the tool cannot write to the root). **Never use Haiku anywhere in this toolkit — every agent (copy, extraction, titles, descriptions, verification) runs on Sonnet or above** (user rule 2026-09-04) (user rule 2026-09-04; blr-batch13: Haiku truncated 2 docs and
doubled regex backslashes in 2 scripts). Then, in order:

**Where run artefacts go (user decision 2026-09-08, project at its 2 MB cap):** only two docs per batch are written to
the project — `claude/backup-titles-<tag>.md` (BEFORE the push, title-format-rule.md §13) and `claude/run-log-<tag>.md`
(after verify). `kw-cache-<tag>.md` and `backup-alt-<tag>.md` are NOT project docs any more: write them to
/mnt/user-data/outputs/ and send them to the chat with SendUserFile (backup-alt before the alt push, kw-cache after the
DataForSEO call). Nothing else from a run goes into the project. If a project_write fails on the cap, stop and report — never
push with a backup-titles doc missing. Runs before this date wrote all four to the project; those older docs were moved to
Google Drive `Vepine/<tag>/` on 2026-09-08 and deleted from the project (45 of 145 at the time of writing) — the
Drive folder keeps the old store's name; Worfa runs archive under `Worfa/<tag>/`, and Tuzwa runs archive under
`Tuzwa/<tag>/`.

0. Verify the copy before anything reads it: save toolkit/MANIFEST.md's block as MANIFEST.sha256 and run
   `sha256sum -c MANIFEST.sha256 --quiet` — re-copy every FAILED file from the project until it passes (added 2026-09-04).

1. `secrets/shopify.json` from toolkit/shopify-api-credentials.md; `python3 shopify_api.py shop` → Tuzwa. Write
   `brief_flags.json` from the brief: `{"q17_compare_table": true}` when Q17 = "Add table", `false` when "No table" or
   Q17 is not answered (rules/comparison-table-rule.md, 2026-09-06) — compare_build.py, struct-check.py and verify.py read it.
   Same file, `"q19_fit_block": true|false` from Q19 (rules/fit-block-rule.md, project path claude/fit-block-rule.md; unanswered =
   false) and `"q18_dimension_image": true|false` from Q18 (rules/dimension-image-rule.md; unanswered = false). When true:
   `pip install rembg onnxruntime --break-system-packages` now, so step 7b does not wait for it. Same file, always:
   `"run_mode": "manual" | "scheduled"` from the brief's run-mode question (Q10) — since 2026-09-09 dim_image.py and
   dim_attach.py refuse to run without `"manual"` (a missing key reads as scheduled), so Q18 = Add in a scheduled brief is a
   documented no-op, not an error.
2. `python3 shopify_api.py fetch <tag> products.json` (script, no model).
3. `python3 extract_html.py products.json` builds raw/ and extract/ skeletons (specs, package, images, media, variants, facts)
   with zero model tokens; then `python3 keyfeat_cover.py --extract` pre-fills `key_features` (the source's own Key Features lines; the extraction agent then completes it by eye with the lines the script missed and the concrete features stated only in paragraphs — EXTRACT-SPEC.md, 2026-09-06;
   2026-09-06, user decision — every one becomes an item of the new Key Features list, keyfeat_cover.py in gate.py enforces it); then per EXTRACT-SPEC.md a Sonnet agent per 10 products (not Haiku — batch12 and batch13: Haiku output unusable) fills identity, notes,
   safety_flags, season_hint, completes `key_features` and `specs` by eye (paragraph features and paragraph values — EXTRACT-SPEC.md, 2026-09-06) and candidates/cNN.json (40–70 per product, neighbouring families included so they are
   measured). Main model reads every `notes`, writes RULINGS.md, shows it in Manual mode.
   **3b. Paragraph sweep (added 2026-09-07, STR-DUB-2-batch1, user decision; zero model tokens):** `python3 para_feat.py
   --report kf-report.md` prints every source-paragraph sentence with a feature marker that no `key_features` line covers
   ([KF MISSING?]) and every prose figure absent from `extract.specs` ([SPEC MISSING?]). The main context sorts each line —
   (a) real feature / value → written into extract/pNN.json so keyfeat_cover / spec_cover ENFORCE it, (b) marketing or
   restatement → dismissed — and the run log carries `para_feat: N KF flagged, K added, N-K dismissed | M SPEC flagged, J
   added, M-J dismissed`. The extraction agents' reply must carry `NN | script X | paragraph features added Y | prose specs
   added Z` with a reason for every 0 (EXTRACT-SPEC.md). Reason: in that batch 45 of 48 products had exactly the script's
   list after extraction and nothing showed it; a log without the para_feat line means the step was skipped.
   A prose figure RULINGS.md drops is declared in `rulings_omit.json` (`{"NN": ["21 grams", …]}`, written with RULINGS.md) —
   para_feat recognises only explicit omissions (that file, or omit_per_ruling once a final exists), never a text search.
   Same day, three hardenings (user decision): (1) `python3 para_feat.py --gate` — every prose FIGURE (number+unit, count,
   IP rating) missing from extract.specs is a FAIL (exit 1) unless ruled out (omit_per_ruling / RULINGS.md); sentences stay
   a report. (2) `python3 extract_check.py --claims extract_claims.json --table coverage.md` — the main context writes the
   agents' reply lines into extract_claims.json (`{"NN": {"kf": Y, "spec": Z, "reason": "…"}}`); the script rebuilds the
   script baseline in _base/ and FAILs a claim that differs from the measured additions or a measured 0 without a reason;
   main-context additions from the para_feat triage go into para_feat_added.json so they are counted in their own column.
   (3) keyfeat_cover.py FAILs [MERGED] — one list item carrying two source lines (one source line = one item).
   coverage.md (per product: KF source / added by agent / added by main / final items, same for Specifications) is pasted
   into the run log at step 8 — the operator's one-look check that the lists are not just the supplier's counts.
   **3c. Independent KF/spec reader (added 2026-09-07, user decision; KF-REVIEW-SPEC.md):** `python3 kf_review_input.py`
   (eligible = source paragraphs > 80 words; `--all` forces every product) → one Sonnet agent reads ONLY the source
   paragraphs + extract.key_features + extract.specs (never the description, never the title) and marks CERTAIN misses in
   kf_review.json; it never writes. The main context confirms each mark into extract/pNN.json + para_feat_added.json or
   dismisses it, re-runs `para_feat.py --gate`, and the run log carries `KF/spec independent review: N eligible of M, K
   marked, J confirmed and added (pNN …), K-J dismissed` — `0 eligible` is a valid line. Validation run on the live
   STR-DUB-2-batch1 (`--all`, 47 products): 8 marked, 8 confirmed (p16 military-grade, p17 dual-purpose, p18 maskless,
   p24 quiet operation, p30 airflow, p41 Filling: memory foam, p43 ×2) — every one had passed para_feat's word match.
   Cost 0.14M tokens for 47 products with --all; a few thousand per eligible product otherwise.
   **3d. Usage Tips + How to Use (added 2026-09-07, user decision):** `python3 usage_tips.py --extract` fills
   `extract.usage_tips` from the source's Usage Tips / Usage Recommendations / Tips block (23 of 47 products in
   STR-DUB-2-batch1). Our page then carries `<h3>Usage Tips</h3>` with every line as its own item in the writer's own
   sentence (after Package Includes, before the fit block / FAQs; RULINGS via omit_per_ruling). `extract.how_to_use` holds
   REAL steps only — audience / occasion lines go to `facts`; the main context moves any that the extraction agent left
   there. Gates in gate.py: `howto_check.py` (steps only, every step kept, no copy, no audience line under How to Use — 9
   products had the supplier's recommendations pasted verbatim under that heading) and `usage_tips.py` (section iff
   tips, every tip, no copy, no merge, position); struct-check.py also rejects an audience line under How to Use.
   **3e. Additional source sections (added 2026-09-08, user decision; rules/description-format-rule.md §7c; applies from the
   first batch after this date — no pushed product is re-processed):** `python3 sections.py --extract` — run AFTER
   `keyfeat_cover.py --extract` and `usage_tips.py --extract`, BEFORE the extraction agents — writes `extract.sections`: every
   other headed block of the source that carries a product fact (Care / Cleaning, Warnings / Safety, Materials, Design,
   Applications, Compatibility, Storage, Charging, Installation, Size Guide, Notes …) as `{heading, heading_source, kind,
   lines}` with the heading mapped to the script's CANONICAL vocabulary, and `extract.sections_dismissed`: the blocks set
   aside — marketing-only (no fact: Tip B → prose, as before) and supplier policy (never in copy). **Two SHAPE tests dismiss
   the same way, before the fact test (added 2026-09-09, user decision after STR-DUB-2-batch8, the script's first live run:
   it proposed a section on 42 of 50 products and every one was the supplier's LEAD HEADLINE + intro paragraph, 7 of them
   already auto-mapped to a canonical name by a stray keyword in that marketing sentence — `Charging` over a laser-pointer
   intro, `Safety Warnings` from "for Enhanced Safety"):** a heading longer than `MAX_HEAD_WORDS` (4) is a marketing headline,
   not a section heading; and the source's FIRST heading over prose is the description's own lead — kept only when it is a
   short heading that names a canonical family. gate.py cannot catch this class of error (once a block is in
   `extract.sections` it only asks whether the page reproduces it), so the shape tests are the guard, not the operator's eye.
   It also removes every
   section line from `key_features` (the section is the line's home). Read its summary line: `N of M products carry a fact
   section, D dismissed (marketing M / policy P / description lead L / long marketing heading H), U UNMAPPED heading(s),
   K key_features line(s) moved`; every [UNMAPPED] heading is named by the
   extraction agent (canonical name when one fits, else a 1–3-word title-case name — EXTRACT-SPEC.md) or by the main context
   before descriptions start, and a family that recurs unmapped is added to `CANON` in sections.py (floor, not ceiling). Our
   page then carries one `<h3>{heading}</h3>` + `<ul>` / `<p>`s per section, every line in the writer's own sentence, after
   Usage Tips, before the fit block / FAQs. Gate in gate.py: `sections.py` (section iff source block, canonical heading, every
   line, no copy, no merge, no invented `<h3>`, position; source order WARN); struct-check.py rejects a non-skeleton `<h3>`
   outside that position; unit_dual.py converts inside these sections; fact_cover.py skips their lines. The run log carries
   `sections: N products with K sections, D dismissed (marketing M / policy P / lead L / long heading H), U unmapped named
   (pNN "…" → …)` — a log without this line means the step was skipped.
   **3f. Two repair scripts for the extract (added 2026-09-21, user decision; written in ddl2-batch28; zero model tokens;
   both take `--dry` — run `--dry` first and read every line, then run without it):**
   (1) `python3 spec_parse.py` — run right after `extract_html.py`, BEFORE the extraction agents. Some suppliers write the
   whole spec table as ONE run-on sentence in a single `<p>` ("Material: Metal Lamp Shade Material: Metal Dimensions: …"),
   so extract_html.py finds no spec list and spec_cover.py has nothing to enforce (ddl2-batch28: 37 of 50; DDL2-Batch1: 13 of
   50). The script splits that line into `extract.specs` rows at the colons whose preceding words are in its `LABELS`
   lexicon (longest match first); a colon after words NOT in the lexicon is left alone, never guessed. Only products whose
   `extract.specs` is EMPTY are touched; the source line stays in `facts`. A `[BLEED after …]` mark on a product's line means
   a value still contains a colon — an unknown label was swallowed into it: add the label to `LABELS` (the lexicon is a
   floor, not a ceiling — it was built from a lighting / home-decor supplier) and re-run, or fix the row by hand. The
   extraction agents still complete `specs` by eye as before.
   (2) `python3 fix_sections.py` — run right after `sections.py --extract` (3e), BEFORE the extraction agents. It applies
   three of the reclassifications that 3e otherwise leaves to the main context, identically on every product: a "Why You'll
   Love It" block is the source's Key Features list → its lines go back into `key_features` and the section is dropped
   (also when sections.py had filed it under `sections_dismissed`); a pseudo-section whose heading is a spec name already in
   `extract.specs` → dropped as a specification row; a two-clause comma headline over prose ("Refined Glow, Architectural
   Design") → dismissed as the description's lead. Junk heading lines left in `key_features` are removed in the same pass.
   It does NOT replace reading the `sections.py --extract` summary and the [UNMAPPED] list in full: a "What's in the Box?"
   block and any other family are still sorted by hand. The run log carries both summary lines (`spec_parse: N products
   filled, R spec rows…` and `fix_sections: WYLI blocks …`) — a log without them means the step was skipped.
4. `python3 source_windows.py products.json > candidates/source_windows.txt` (script, zero model tokens; added 2026-09-06,
   user decision). Every contiguous 2–4-word window of every source title becomes a candidate — title-format-rule.md §1
   "the source title's own keywords are always measured", done exhaustively instead of by the extraction agent's judgment.
   blr-batch24 audit: 386 such windows had never been measured; `essential oil diffuser` 74,000 was one of them and the title
   had opened on `aromatherapy diffuser` 14,800. The script only ADDS candidates — fit (§6) and the head-noun test decide
   later, in the title step, what enters a title. Then DataForSEO: all cNN.json candidates ∪ source_windows.txt, ≤950 per
   call, → kw.txt (keyword|volume|comp|cpc), kw-cache-<tag>.md to /mnt/user-data/outputs/ and sent to the chat (NOT a project
   doc since 2026-09-08 — see "Where run artefacts go"). Expected extra cost: ~400 keywords per 50 products,
   i.e. at most one more call (~$0.09).
   **Word-order guard (2026-09-11):** `kw_measure.py` sends keywords that are the same words in a different order
   (`noise cancelling headphones` / `headphones noise cancelling`) in SEPARATE rounds/calls — in one request Google folds
   them and returns the low variant's volume for both (ddl2-batch1 p00: 165,000 read as 2,400). Expect one extra call
   per batch; copy the `… over R round(s) — V word-order variant(s)` stderr line into the run log. Rule:
   `rules/kw-order-variant-rule.md` (project path `claude/kw-order-variant-rule.md`).
   **Push-blocking:** `title-check.py` (step 5) FAILS the whole batch when any of these
   windows is missing from kw.txt or when products.json is not on disk — so a skipped step 4 cannot reach the store.
5. Titles in ONE small-context subagent (main model) per TITLE-SPEC.md: cap.py to measure capture, ov.py for the 8.2 shared-word
   report, build_check.py (edit its FR fit-reject patterns + EXTRA) → check_products.json, `python3 title-check.py
   kw.txt check_products.json` until 0 FAIL; emits rejects.json (top-8 second net + capped) and titles_final.json.
   title-check.py is push-blocking on: unmeasured opener, outranked opener, unmeasured source-title windows (2026-09-06) and,
   also from 2026-09-06, any comma cluster without a measured core phrase (blr-batch24: 5 of 154 clusters, e.g. `Automatic
   Robotic Vacuum for Carpet` where `robot vacuum for carpet` 2,400 had been measured). Attributes and for/with tails stay free.
   Fifth push-blocker (2026-09-06): the old title must not capture more product-naming volume than the new one — build_check.py
   writes `old_title` + `product_id` (from products.json) into each check_products.json entry so the comparison can run.
   Sixth (2026-09-06, option b): an unused measured keyword that beats the weakest non-opener cluster FAILs unless the title
   agent writes a one-line reason in skip_reasons.json (build_check.py copies it in); reasons land in rejects.json for the run log.
   **`python3 head_check.py titles_final.json` must print 0 FAIL** (title-format-rule.md §3 rule 2 head-noun test, added
   2026-09-05: the opener phrase is built on the productType's own head noun — `Cat Beds` cannot open a cat hammock; the
   script's synonym list is the master copy of the rule's list). backup-titles-<tag>.md to the project BEFORE anything is pushed.
5b. **Image re-host (Q14), before any description is written:** `python3 rehost.py` (toolkit script since 2026-09-06, zero model
   tokens). Every extract/pNN.json `images[].src` not on our CDN goes through `fileCreate` in groups of 10; the created ids are
   written to image_ids.json after EVERY group, so an Admin API error or a crash never loses them and a re-run continues from
   that file instead of uploading again (blr-batch25: the ad hoc version kept the ids in memory, crashed on three Shopify
   "Internal Server Error" responses and left ~50 duplicate files in Files). Polls to READY, writes image_map.json, rewrites
   the extract srcs (old value kept as `src_original`), logs any FAILED file with product index + URL and leaves that src
   untouched. Read its one summary line: `N mapped, 0 failed, N srcs rewritten, 0 still foreign` — exit 1 otherwise. CDN
   prefix is its optional argument (Tuzwa default).
6. Descriptions: 5 Sonnet agents × 10 products per DESC-SPEC.md; each runs `python3 gate.py NN…` until clean (gate now
   includes the keyfeat_cover.py [COPY] check — a source Key Features line pasted verbatim FAILs, 2026-09-07 — plus
   howto_check.py and usage_tips.py (same day) and sections.py (2026-09-08: every `extract.sections` entry its own <h3> with the
   canonical heading, every line own words, no copy / merge / invented section, position) and
   includes unit_dual.py — a measurement given in one unit system gets the other appended in parentheses in prose, Key Features, Specifications, every <h3> section after Package Includes and FAQ answers (never H2 / bullets / CTA / blocks / questions / alts / SEO),
   script, idempotent (2026-09-06, user decision) — and keyfeat_cover.py — every source Key Features line is an item of the new Key Features list (2026-09-06) — and value_check.py — no source value dropped — and spec_cover.py — every source spec line present as an item of the
   new Specifications list, which value_check does not catch when the spec only appears in a bullet — and, restored
   2026-09-06, cta_check.py — each of the 3 CTA lines is a benefit, not a spec — and, added 2026-09-06, assume_check.py —
   no forbidden-family claim (machine washable, no app, BPA-free, certified, universal, waterproof, lifetime, non-toxic, "than
   ordinary" …) the extract never states, FAIL; plus age_check.py — single-age phrase without its range, WARN only; all script,
   zero tokens; and, added 2026-09-06 at the user's decision, compare_build.py — runs FIRST inside gate.py, renders the
   "Tuzwa vs Others" comparison block from the doc's `compare` object (5 product rows + fixed store row) into descriptionHtml
   before `<h3>Key Features</h3>` and FAILs on a missing / untraceable / all-✘ table — only when brief Q17 = "Add table" (brief_flags.json); with "No table" it
   removes any existing block and requires nothing; rules/comparison-table-rule.md. Then fit_build.py (Q19, same contract,
   rules/fit-block-rule.md): the single-column "Right for you if" block from the doc's `fit` object (exactly 4 `for` lines — the
   "Not the right fit if" column was removed 2026-09-06, user decision), rendered directly before `<h3>FAQs</h3>`;
   `"fit": null` + notes_for_log "fit: not applicable" opts a product out. The
   agent writes only the five rows and a short name, never the HTML; the brand name is allowed inside that block only);
   main context re-runs gate.py over all 50. **gate.py exits 1 when any section reports a problem and 0 only when every
   section is clean (fixed 2026-09-06 — until then the exit code was always 0, so "exit 0" never meant clean); the printed
   FAIL / hits / issues lines are still the detail to read and fix.**
6b. **Fact coverage sweep (main context, before payloads, zero model tokens; added 2026-09-05 after the user found
   `Hygienic and non-absorbent` missing from blr-batch23 p05).** `python3 fact_cover.py` scores every line of every
   product's `facts` against the finished description and prints those under 55%. value_check guards numbers, list
   items, package items and variant options; this guards the sentences that carry no number, which until now nothing
   checked. It is deliberately NOT wired into gate.py — the description agents never see it, so it adds no agent
   turns. Lines that are usage tips or section lines (2026-09-07 / 2026-09-08) are skipped — usage_tips.py / sections.py
   enforce those item by item. The main context reads the printed lines and sorts them: (a) a value RULINGS.md dropped on purpose — leave
   it, `omit_per_ruling` already covers it and the script skips those; (b) the same meaning in different words —
   leave it, the script matches words, not meaning; (c) genuinely missing — send ONLY those products back to their
   description agent with the instruction to weave the fact in IN ITS OWN WORDS; a pasted source sentence is sent
   back again, and a source-stated health benefit is woven in too (Safety Notes 2026-09-21; only disease-treatment claims stay out). Nothing is pushed until (c) is empty or the
   remaining line carries a written reason in that product's `notes_for_log`.
6c. **Benefit review by eye (main context, before payloads; added 2026-09-06, user decision).** No script can judge
   whether a bullet is a reason to buy, so this step is a written rule, not an option: the main context reads, for EVERY
   product, the H2, the five benefit bullets, the three CTA lines and (since 2026-09-06) the five comparison-table rows and the fit block's "Right for you if" lines, against description-format-rule.md §2 "Which five
   benefits", cta-benefits-metafield.md "HANGİ 3 BENEFIT" and comparison-table-rule.md — each slot a problem the shopper lives with now and will not
   any more, the payoff a fact that makes it believable; no secondary feature, pack count, aesthetics, category definition
   or variant fact; H2 a keyword headline, not a sentence. A product that misses goes back to its description agent with
   the failing line named. The run log states the result explicitly: the product numbers corrected, or "6c read on all N
   products, no correction" — a log without this line means the step was skipped. (blr-batch13 did this and fixed 10 of 50;
   blr-batch21 did not and 48 of 50 CTA lines reached the store in spec language.)
   **Key Features list read (added 2026-09-07, STR-DUB-2-batch1, user decision):** the main context also reads every
   product's new `<h3>Key Features</h3>` list next to `extract.key_features` — one item per source line, own sentence, the
   paragraph additions present — and the run log carries `KF read on all N products: copies 0 (keyfeat_cover), paragraph
   additions on K products`. keyfeat_cover.py FAILs a pasted line since the same day, so the read is for meaning, not copies.
   **CTA lines are read as their own named pass (added 2026-09-06, user decision after blr-batch26):** after the bullet /
   table / fit reading, the main context reads the 150 CTA lines once more on their own, against cta-benefits-metafield.md
   "HANGİ 3 BENEFIT" and its blr-batch26 ❌/✓ examples — the test is "can this line be read as 'that problem is gone'?" — and
   the run log carries a separate line: "CTA read on all N products, corrected: pNN …" or "CTA read on all N, no correction".
   In blr-batch26 the CTA lines were read inside the general 6c pass and 8 feature-count / audience lines were passed by eye
   and caught only by the user (p45, p47); a log without the CTA line means this pass was skipped.
   **Then an INDEPENDENT CTA reader (added 2026-09-06, user decision):** one Sonnet agent per batch, per CTA-REVIEW-SPEC.md
   (toolkit doc), sees only each product's facts/specs and its three CTA lines — never the description, never the title — and
   marks CERTAIN failures only (feature counts, what-it-does lines, audience/occasion lines, variant facts, unsourced
   outcomes); borderline lines and runtime-per-charge figures are not marked (user decision: no false-alarm load). It never
   rewrites. The main context writes `cta_review_input.json` (script, zero tokens: idx, identity, facts, specs, cta), reads
   every marked line itself, sends real misses back with the 6b/6c message, dismisses wrong marks, and the run log carries
   `CTA independent review: N marked, K confirmed and corrected (pNN …), N-K dismissed`. Cost ≈ 0.1M tokens per 50 products.
6d. **6b and 6c go back to the agents in ONE message (added 2026-09-06, user decision, no rule change).** The main context
   does both readings first — the fact_cover.py triage (6b) and the benefit review by eye (6c) — and sends each agent a
   single correction message carrying both lists, so each agent returns once instead of twice (blr-batch25: two separate
   rounds × 5 agents ≈ 1.2M tokens for no difference in output). After the agents return: re-run gate.py over all 50 as
   before, AND re-run `python3 fact_cover.py` once more and diff it against the pre-correction output — a 6c edit can move
   a fact out of a bullet, and 6b was read on the pre-edit text. Any newly flagged line is triaged the same way (a/b/c). Zero
   model tokens; the run log quotes both fact_cover runs. **Then the main context re-reads, by eye, every H2 / bullet / CTA
   line the 6c corrections changed** (the changed lines only, ~30–60 short lines, not all 50 products) — fact_cover matches
   words, not meaning, so a corrected sentence whose meaning drifted is caught only by eye. The run log states this
   re-read was done and names any product corrected again.
7. **First `python3 dim_keep.py` (added 2026-09-09, every batch, whatever Q18 or the run mode says):** a product whose LIVE
   description (products.json) carries a Q18 `<img class="vp-dim">` and whose new final/dNN.json does not — a Q7 rewrite
   drops it, and gate.py / struct-check.py ignore vp-dim by design, so nothing else would notice — gets the same tag restored
   under the new Specifications list, but only while its media is still in the live gallery (a gone media is a [WARN] for
   the operator, never a re-published dead link). Its `dim-keep: N restored, W warned, M untouched` line goes into the run
   log. Then payloads: rewrites.json → push/mutN.json (10 aliased productUpdate incl. collectionsToJoin + category), cta
   metafieldsSet ×2, fileUpdate alt batches; backup-alt-<tag>.md to /mnt/user-data/outputs/ and sent to the chat BEFORE the
   alt push (NOT a project doc since 2026-09-08 — see "Where run artefacts go"); then
   `for f in push/mut*.json push/cta*.json push/alt*.json; do python3 shopify_api.py mutate $f; done`.
   **`seo` is replaced whole, never merged (added 2026-09-05, opener-fix run):** `ProductUpdateInput.seo` overwrites the
   entire SEO object — sending `seo: { title }` alone set `seo.description` to null on 42 products. Every payload that
   touches SEO must carry BOTH `seo.title` and `seo.description`; when only one half is being rewritten, copy the other
   half from the Phase 1 snapshot into the payload. The verify step (8) compares both against the snapshot, so a repeat
   would be caught, but the payload builder must not rely on that.
7b. **Dimension image (Q18 = Add AND run_mode manual; rules/dimension-image-rule.md, 2026-09-06; scope cut 2026-09-09).**
   `python3 dim_image.py sheet` → look at
   dim/sheet.png once, write dim/pick.json for products whose featured image is not a single product on a plain background
   → `python3 dim_image.py build` (script: rembg cut-out + navy dimension lines + size table from the source's L×W×H; a
   product with no such pattern is skipped and named in the run log; **labelled sources only** — axes the source NAMES, an
   order key like `(L x W x H)` or labelled figures (rule 1b) or a labelled pair (rule 1d), are used as written, and a bare
   `2 x 5 x 6 cm` / `200 x 150 cm` is skipped as `axes not labelled in source`: the photo-ratio test of rule 1c is retired
   (`PHOTO_TEST = False`; every wrong live image of 2026-09-09 came through it) — the run log quotes the build's summary
   line, `N built (K labelled, 0 by photo-ratio), S skipped — U axes not labelled: …`, and a `[WARN] … PHOTO_TEST is on`
   line may never appear without the user's logged re-enable decision; package and "fits …" measurements
   are never the product's size) → look at the built dim/dim*.png once, asking rule 5's question by name → `python3
   dim_attach.py` (staged upload, productCreateMedia, reorder to gallery position 3 — featured and 2nd image stay, the
   "actual size" image is third, every source image from the 3rd onwards moves down one place, nothing removed; user
   decision 2026-09-09 — position 2 was tried and reverted the same day because most themes use the 2nd image as the
   collection-card hover image; dim/media.json written per product, re-run safe; a product whose live gallery
   already carries a dimension image from an earlier batch is skipped into dim/media_existing.json, never duplicated; after the
   attach the same image is inserted under the description's Specifications list as `<img class="vp-dim">`, written to
   final/dNN.json and pushed as a descriptionHtml-only productUpdate — gate.py / struct-check.py ignore it in the image count,
   verify.py compares live with the updated final; to REPLACE an image delete the media in Shopify and re-run — the
   description's vp-dim src is rewritten to the new media, since 2026-09-09, instead of being left as a dead link). First live run: if the
   staged PUT fails on the connection, the storage host needs the egress allowlist — report it, do not retry blindly. Zero
   model tokens per product; two contact-sheet looks per batch.
8. Verify: `python3 shopify_api.py fetch <tag> live_after.json`, then **`python3 verify.py products.json live_after.json
   collections.json`** (toolkit script since 2026-09-06 — before that every batch re-wrote its own verify.py and the checked
   fields varied silently; user decision after the 2026-09-06 checker audit). It compares EVERY product's live fields against
   final/dNN.json and the pre-push snapshot: title, normalized descriptionHtml, seo (+ 70/160 limits), productType, tags =
   snapshot ∪ season (nothing dropped, no duplicate), status unchanged (pass `--status ACTIVE` only when the brief changed
   it), category (KEEP or proposal), CTA metafield JSON, collections joined, media alts (≤125, unique in product and across
   the batch), media order, description img src order + all on our CDN, variant prices vs snapshot, brand name absent
   (outside the comparison block), comparison block live exactly once when Q17 = Add table / none when No table, fit block likewise for Q19 (one column, directly before the FAQs), and for
   Q18 products the media order = snapshot + the dimension image at position 3 (the position recorded in dim/media.json) with its alt — 17
   checks per product + 1 batch check, exit 1 on any failure; the run log also carries the coverage.md table from
   extract_check.py (2026-09-07); a check it cannot run is printed as a [note], never skipped
   silently. Then `python3 head_check.py live_after.json` → 0 FAIL (verify.py does not replace it). Run log to project — quote
   verify.py's summary line as printed; runbook §8+ measurement.

## Store-specific constants (change for a store other than Tuzwa)
- Store: brand / store name `Tuzwa` (capital T, rest lower case — never TUZWA), storefront `tuzwa.com`, canonical
  Admin host `qu1ysp-7j.myshopify.com` (the alias `tuzwa.myshopify.com` also answers — record the canonical host),
  currency USD. App `Claude Backend`, scopes granted: read/write_files, read/write_products, read/write_publications —
  `read_themes` is NOT granted. Egress from the container: `qu1ysp-7j.myshopify.com` and `cdn.shopify.com` work
  (measured 2026-09-12 and unchanged since). **`tuzwa.com` was refused with 403 CONNECT on 2026-09-12 but is
  REACHABLE as of 2026-09-15** — `https://tuzwa.com/` returned 200 on three consecutive requests, `www.` 301s to it.
  Treat egress as a per-session fact and re-measure rather than trusting either line: the allowlist can change
  between sessions. Note this does NOT change the theme rule below — `read_themes` is what blocks the script
  route there, not the storefront host. Previous store: Worfa, host `ymjviw-rz.myshopify.com`.
- CDN prefix `cdn.shopify.com/s/files/1/0806/1645/6416/` is hard-coded in gate.py, struct-check.py, build_check.py and
  DESC-SPEC.md and verify.py; extract_html.py and rehost.py take it as an argument. For a store other than Tuzwa,
  replace it everywhere — the value above is Tuzwa's, set 2026-09-12 and verified the same day over the FULL
  catalogue: 7,293 products / 54,934 media images, every image on cdn.shopify.com and on this prefix, 0 foreign hosts,
  0 off-prefix. The previous store's prefix was `cdn.shopify.com/s/files/1/0786/1269/3028/` (Worfa).
- Comparison block: store name, heading, store row (`30-day easy returns`) and theme colours are constants at the top of
  compare_build.py (BRAND in gate.py / verify.py too); BRAND is `Tuzwa` from 2026-09-12. **The theme colours NAVY
  #000096 / LIGHT #f4f4f4 were MEASURED on Tuzwa 2026-09-12.** They were read from Tuzwa's live MAIN theme
  `Xtra -- NEW` (`gid://shopify/OnlineStoreTheme/161796391136`), file config/settings_data.json, default scheme
  `scheme-1`: NAVY is that theme's `buy_button_color`, identical to `scheme-1`'s `primary_button_bg` (the Add-to-cart
  button); LIGHT is `scheme-1`'s `secondary_bg` (the light section band). Contrast measured on these values: white on
  NAVY 14.6:1, NAVY on LIGHT 13.3:1. They are also applied in fit_build.py (`NAVY = '#000096'`) and dim_image.py
  (`NAVY = (0, 0, 150)`, `LIGHT = (244, 244, 244)`). **Theme reads go through the Shopify connector**, which has
  `read_themes`; the custom app used by the script route does NOT have it — so open theme files through the
  connector and keep fetch, push and verification on the script route. (Until 2026-09-15 this sentence also gave
  a blocked `tuzwa.com` as a reason; the storefront is reachable again, but the missing scope is reason enough
  on its own and the rule is unchanged.) The previous store's `#2c374d` / `#eef5f7` (Worfa, Vault) and the oldest store's
  `#d2def6` are retired history; `#000096` is NOT retired — it is Tuzwa's live navy. The store row `30-day easy
  returns` is CONFIRMED for Tuzwa by the user (2026-09-12), window 30 days. Read the theme file again through the
  connector if the theme or its default scheme changes.
- collections.json must be refreshed per store: `gql("{ collections(first:100){ edges{ node{ id title } } } }}")`.
  Refreshed for Tuzwa on 2026-09-12: 49 collections (the previous store had 24).
  Save that call's response as it comes, or as a `{title: id}` map — verify.py reads either (2026-09-08, after STR-DUB-2-batch4:
  until then only the map was read, and a file written this way made the collections check print a [note] on every product
  instead of running; now an unreadable or empty file is a hard exit, never a note).
- Foreign images: extract_html.py lists them in `foreign_images`; `python3 rehost.py <cdn_prefix>` re-hosts them (step 5b)
  before descriptions are written — first full run blr-batch25, 129/129.
