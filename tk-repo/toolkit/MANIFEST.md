# toolkit MANIFEST — sha256 of every toolkit/rule doc as it should land on disk (refreshed 2026-09-07b, Tuzwa→Vepine store migration: 18 files re-hashed — CDN prefix, BRAND, comparison-table colours/heading and the tz-→vp- CSS hooks; desc-check.py re-hashed too — its line was already stale before the migration and the file was verified complete and compiling before rehashing)

Last refresh: 2026-09-12 — STORE CHANGE Worfa → Tuzwa (20 lines: BRAND, CDN prefix, host, rule docs, credentials, brand-in-copy scan), after the same day's DDL2-Batch4 proxy backoff (shopify_api.py, kw_measure.py) and DDL2-Batch3 unit_dual.py fix (engine litres, dual temperature ranges), on top of 2026-09-11's list_bold.py added as a 57th line (bold Key Features / Specifications lead-ins, gap under image 2; gate.py, struct-check.py, rules/description-format-rule.md recomputed), after the same day's US units only in the budgeted elements (6 lines recomputed: unit_dual.py, compare_build.py, fit_build.py, rules/comparison-table-rule.md, rules/fit-block-rule.md, rules/description-format-rule.md), on top of the same day's kw_measure.py word-order guard (3 lines recomputed, a 56th line added: rules/kw-order-variant-rule.md),
on top of the 2026-09-10 Worfa go-live checks (7 lines: theme colours, store row, verified credentials),
after the same day's store change Vepine → Worfa (17 lines: BRAND, CDN prefix, host, rule docs, credentials),
on top of the same day's comparison-table mobile/desktop width fix and the rotated Shopify credential pair.

Purpose: the session-start copy (README-toolkit.md step 0) is done by an agent that re-types each project doc into
/home/claude/work/. In blr-batch13 a Haiku copy agent silently truncated DESC-SPEC.md (lost the "ADD NOTHING" section) and
title-format-rule.md (lost §10), and doubled regex backslashes in desc-check.py / claims_check.py. This manifest makes that
detectable at zero model cost.

## Use (after the copy agent finishes)
1. Save the block below to /home/claude/work/MANIFEST.sha256 (57 lines; Write it exactly).
2. `sha256sum -c MANIFEST.sha256 --quiet && echo TOOLKIT OK`
3. Any file it lists as FAILED was altered in the copy: project_read that doc again and re-write it — never patch by hand.
   A 1-byte difference is usually a trailing newline; re-copy anyway until it passes.
4. build_check.py is edited by the title step (FR/EXTRA per batch) — its checksum is for the pristine project version only.
5. The copy agent must write the fetched `content` to disk programmatically (`open(p,'w').write(content)`), never re-type it.
   Retyping is what produced every corruption this manifest has caught: dropped semicolons, added spaces after commas,
   reflowed line breaks, doubled backslashes.
6. A FAILED line is not proof of corruption — it can also mean the project doc changed after the manifest was refreshed.
   Tell the two apart before acting: make a SECOND independent copy of that doc and compare the two copies' sha256.
   Two independent copies that agree = the manifest line is stale (recompute it here). They disagree = one copy is
   corrupted; keep the clean one. In blr-batch19 this separated 3 stale lines from 1 genuinely corrupted copy
   (description-format-rule.md had come back JSON-escaped: `\"` for every quote and one literal `\n`).

## Keep in sync
Whenever a toolkit or rule doc changes in the project, recompute its line (`sha256sum <file>`) and replace it here in the same
turn — a stale manifest fails on a correct copy.

**Refresh note (2026-09-12, STORE CHANGE Worfa → Tuzwa):** 20 lines recomputed. User instruction: in this project the
brand is **Tuzwa** only — not Worfa, not Vepine. Tuzwa is a DIFFERENT Shopify store (it is not the pre-2026-09-07 Tuzwa
store either — different CDN prefix, different collections, different catalogue size). Verified through the script route,
not assumed: store `Tuzwa` / storefront `tuzwa.com` / canonical Admin host `qu1ysp-7j.myshopify.com` / USD; app
`Claude Backend` with read+write on files, products and publications; CDN prefix
`cdn.shopify.com/s/files/1/0806/1645/6416/` confirmed over the FULL catalogue (7,293 products / 54,934 media images,
0 foreign hosts, 0 off-prefix); `collections.json` refetched, 49 collections. Changed: `BRAND` in `./compare_build.py`
(and with it the rendered heading "Why choose Tuzwa" and the "Tuzwa vs Others" block), `./verify.py` and `./gate.py`
(the brand-in-copy scan now fails `tuzwa`); the hard-coded CDN prefix in `./gate.py`, `./struct-check.py`,
`./build_check.py`, `./verify.py`, `./extract_html.py`, `./rehost.py`, `./DESC-SPEC.md` and
`./usage-efficiency-runbook.md`; store name, host and credentials throughout `./shopify-api-credentials.md` (rewritten)
and `./README-toolkit.md`; brand in `./rules/comparison-table-rule.md`, `./rules/dimension-image-rule.md`,
`./rules/fit-block-rule.md`, `./rules/description-format-rule.md` and `./rules/cta-benefits-metafield.md`; the prose
brand in `./shopify_api.py`; and the root doc `00-TASIMA-REHBERI.md` (not hashed here). Full record:
`claude/store-migration-tuzwa-2026-09-12.md`.
Three of these docs were edited again after the first MANIFEST pass and are re-hashed here:
`./shopify-api-credentials.md` now records the shop id `gid://shopify/Shop/80616456416` and 7,293 products and the proof
that `tuzwa.myshopify.com` and `qu1ysp-7j.myshopify.com` return the SAME shop id (so the alias is this store, not the
pre-2026-09-07 Tuzwa store), and `./usage-efficiency-runbook.md` §9/§10 and `./rules/cta-benefits-metafield.md`'s history
lines were relabelled "the pre-2026-09-07 Tuzwa store" so old-Tuzwa history is no longer readable as current state.
The pre-migration transcriptions were byte-verified: the sha256 of all 17 verbatim copies matched this manifest's
pre-migration hashes exactly, so no transcription damage occurred in this migration.
Nine of the 20 lines — `./compare_build.py`, `./fit_build.py`, `./dim_image.py`, `./README-toolkit.md` (both of its
listed lines), `./shopify-api-credentials.md`, `./rules/comparison-table-rule.md`, `./rules/fit-block-rule.md`,
`./rules/dimension-image-rule.md` and `./rules/cta-benefits-metafield.md` — were recomputed a SECOND time later the same
day, after Tuzwa's theme colours were actually measured (the theme-colour item below). The count stays 20: all nine were
already among the lines this migration touched.

Non-changes and open items:
- **The `vp-` CSS hooks stay** (`vp-compare`, `vp-fit`, `vp-dim`, `vp-store`) — internal selectors, not brand strings.
  Renaming them would make every already-rendered block invisible to BLOCK_RE, struct-check.py, verify.py and
  unit_dual.py.
- **History is not rewritten.** Run logs, checkpoints, `backup-titles-*`, `backup-alt-*`, `kw-cache-*` and
  `claude/store-migration-vepine-2026-09-07.md` still name Worfa / Vepine — the backups are restore snapshots of those
  stores' products and must never be restored onto Tuzwa. Same decision as the two earlier migrations.
- **Theme colours ARE measured for Tuzwa** (2026-09-12) — through the **Shopify connector**, not the script route: the
  connector carries `read_themes`, the script-route custom app does not, and `tuzwa.com` is still refused by the
  container's egress proxy (403 CONNECT). So theme reads go through the connector while fetch, push and verification
  stay on the script route. Live MAIN theme `Xtra -- NEW` (`gid://shopify/OnlineStoreTheme/161796391136`),
  `config/settings_data.json`, default `scheme-1`: NAVY `#000096` (`buy_button_color`, the same value as
  `primary_button_bg`), LIGHT `#f4f4f4` (`secondary_bg`). Contrast: white on navy 14.6:1, navy on light 13.3:1.
  Applied in `./compare_build.py`, `./fit_build.py` and `./dim_image.py` (the last as RGB tuples (0, 0, 150) /
  (244, 244, 244)) and in the three rule docs. Worfa's `#2c374d` / `#eef5f7` and the older `#d2def6` are retired — but
  `#000096` is Tuzwa's LIVE navy, not retired history.
- **The store row `30-day easy returns` is confirmed for Tuzwa** (user, 2026-09-12): the same 30-day window, so
  `STORE_ROW` is unchanged. Re-confirm it whenever the store or the policy changes.
- **The CTA-benefits Custom Liquid block IS installed on Tuzwa's theme and working.** `templates/product.json` carries
  block `custom_liquid_NkVEtn` (type `custom_liquid`) reading `product.metafields.custom.cta_benefits.value`, present in
  the template's block order; read through the connector and confirmed visible by the user. An earlier version of this
  note said the block had not been added — that was wrong.
- **No write has been executed on Tuzwa yet** — read, identity, full catalogue sweep and collections are proven; the
  first productUpdate batch is unrun.
- Two contradictions were fixed in passing: `rules/comparison-table-rule.md` named `#000096` / `#d2def6` as live
  colours in one sentence and retired in another; `rules/dimension-image-rule.md` specified `#000096` for the dimension
  lines while `dim_image.py` drew `#2c374d`. Both now state the live pair once — which, after the measurement above, is
  `#000096` / `#f4f4f4`: `#000096` is Tuzwa's live navy again (it was also the oldest store's), while `#d2def6` and
  Worfa's `#2c374d` / `#eef5f7` are retired history.

**Refresh note (BLR-BATCH19, 2026-09-04):** four lines were stale — README-toolkit.md, rules/description-format-rule.md,
rules/rule-overlap-deferred.md and usage-efficiency-runbook.md failed against the previous hashes. README-toolkit.md was
verified against the source read in the main context; the other three were verified by an independent second copy. All four
lines below were recomputed from verified copies of the current project docs. The remaining 21 lines are unchanged from the
TRIMMERYENI refresh and passed on the first copy.

**Refresh note (BLR-BATCH21, 2026-09-04):** one line was stale — `rules/description-format-rule.md`. Two independent copies of
the project doc agreed byte-for-byte with each other and disagreed with the manifest, so per §6 the manifest line was stale,
not a corrupted copy. That line was recomputed from the verified copy. The remaining 24 lines passed on the first copy.

**Refresh note (BLR-BATCH22, 2026-09-04):** two lines were stale on the session copy — `./EXTRACT-SPEC.md` and
`./rules/description-format-rule.md`. For each, two independent copies agreed byte-for-byte and disagreed with the manifest,
so per §6 both manifest lines were stale, not corrupted copies. Both were recomputed.

**Refresh note (BLR-BATCH22 follow-up, 2026-09-04):** two lines recomputed after a deliberate RULE CHANGE, not a copy problem
— `./rules/description-format-rule.md` (whole-description ceiling raised 430 → 500 words by user decision) and
`./struct-check.py` (the same number in code). Both project docs were updated in the same turn as this manifest.

**Refresh note (BLR-BATCH22 follow-up 2, 2026-09-04):** a 26th line — `./spec_cover.py`, a new script gate added at the
user's request after the 112 missing spec lines. `./gate.py` (wires the new check), `./DESC-SPEC.md` and
`./README-toolkit.md` (document it) were recomputed in the same turn.

**Refresh note (2026-09-05, opener identity clause):** one line recomputed after a deliberate RULE CHANGE —
`./rules/title-format-rule.md` (§3 rule 2 opener identity clause, §1 product-type lookup, §10b consistency; user decision
after the blr-batch21 door-knocker review). The project doc and this manifest were updated in the same turn. Recomputed again the same day after §5
"measured specs are keywords" was added (user decision).

**Refresh note (2026-09-05, opener-fix run):** `./README-toolkit.md` recomputed after step 7 gained the "seo is replaced
whole" note (user-approved) — the opener-fix push had cleared seo.description on 42 products by sending seo.title alone.

**Refresh note (2026-09-05, head-noun test):** a 27th line — `./head_check.py`, the §3 rule 2 head-noun test script
(user decision after the cat-hammock review). `./rules/title-format-rule.md` (the "typical member" exception replaced by
the head-noun test + synonym list) and `./README-toolkit.md` (steps 5 and 8 call head_check.py) recomputed in the same
turn.

**Refresh note (2026-09-05, ceiling never drops a source line):** `./struct-check.py` (total words > 500 is now a WARNING,
not a FAIL — spec_cover.py / value_check.py remain the failing gates) and `./rules/description-format-rule.md` (the same
sentence in the length-budget section) recomputed after a user instruction. Recomputed again the same day: prose has no
paragraph cap and no word ceiling any more (source meaning decides, no padding) — struct-check warns above 110, never fails. Third recompute the same day: a description with no source image gets two gallery
images at the skeleton slots (user instruction); struct-check fails on fewer than two images.

**Refresh note (BLR-BATCH23, 2026-09-05):** two lines were stale on the session copy — `./EXTRACT-SPEC.md` and
`./rules/cta-benefits-metafield.md`. For each, THREE independent copies of the project doc (the copy agent's two, plus a
third read in the main context diffed against the file on disk) agreed byte-for-byte and disagreed with the manifest, so
per §6 both manifest lines were stale, not corrupted copies. Both were recomputed. The remaining 25 lines passed on the
first copy.

**Refresh note (BLR-BATCH23 run, 2026-09-05):** two lines were stale on this session's copy —
`./rules/description-format-rule.md` and `./rules/title-format-rule.md`. Both project docs had been edited (09:52 and 09:58 UTC)
after the previous manifest refresh took its hashes from an earlier on-disk copy. Two independent copy agents produced
byte-identical files for both docs and both disagreed with the manifest, so per §6 the manifest lines were stale, not
corrupted copies. Both were recomputed. The remaining 25 lines passed on the first copy.

**Refresh note (BLR-BATCH23 run, gate/image-floor mismatch, 2026-09-05):** `./gate.py` recomputed after a code fix, not a
copy problem. The same-day "never fewer than two images" decision was written into `rules/description-format-rule.md` and
`./struct-check.py` but NOT into `./gate.py`, whose older image check still demanded `src_new == src_old` exactly — so a
product with 0 or 1 source image could not pass both gates at once (three did so in this batch: p29, p37, p43). gate.py now requires the source images to be an unchanged PREFIX of
the description's images and the total to equal `max(len(source), 2)`; for a product with 2+ source images this is exactly
the old equality check, so nothing was relaxed. The project doc was updated in the same turn as this manifest.

**Refresh note (BLR-BATCH23 run, a 28th line, 2026-09-05):** `./rules/PROJECT-DESCRIPTION.md` added at the user's request.
DESC-SPEC.md has required this doc read in full since 2026-09-04, but it was never added to this list, so every run
discovered it missing and fetched it with a separate agent (~0.08M subagent tokens per batch). Its hash was taken from a
copy verified per §6: two independent copies agreed on every byte of content, differing only in a trailing newline; the
newline-terminated form is canonical because that is what a heredoc copy produces. `./README-toolkit.md` recomputed in the
same turn — step 0 now says the rule docs are exactly the `./rules/…` lines of this manifest and names this one.

**Refresh note (BLR-BATCH23 run, a 29th line — fact coverage, 2026-09-05):** `./fact_cover.py` added at the user's
decision, and `./README-toolkit.md` recomputed for its step 6b. Reason: the user read the live blr-batch23 listing for
p05 and found the source line `Hygienic and non-absorbent, which helps prevent bacterial buildup` missing from the new
description. Nothing had checked it — `value_check.py` covers numbers, list items, package items and variant options,
so a source sentence carrying no number could be dropped silently. `fact_cover.py` scores every `facts` line against
the finished description and prints those under 55% for main-context review; it is NOT part of gate.py, so the
description agents never see it and it costs no agent turns. It is a review aid, not a gate — it always exits 0,
because word overlap cannot tell a rewrite from an omission.

**Refresh note (2026-09-05, medical-claim rule rewritten):** `./rules/PROJECT-DESCRIPTION.md` recomputed after a
deliberate RULE CHANGE, not a copy problem. The Safety Notes line "Medical/health claims: remove or soften" was too
blunt — it was pushing the customer's own problem out of the copy on products bought precisely for that problem. At the
user's decision it now permits naming the problem and the intended use (pain relief, sciatica, back support) and forbids
only unevidenced physiological outcomes (reduces inflammation / blocks pain signals / speeds recovery / heals / treats /
cures), and requires the source's own disclaimer sentence to be kept. Note: the doc is a mirror of the project's
description field, which the tools cannot edit — the user updates that field in the UI so the two do not drift.

**Refresh note (BLR-BATCH24 run, 2026-09-05):** five lines FAILED on this session's copy; per §6 a second independent
copy agent re-copied all five and the two copies were compared.
- Four were STALE manifest lines, not corrupted copies — both copies agreed byte-for-byte and disagreed with the manifest:
  `./TITLE-SPEC.md`, `./build_check.py`, `./title-check.py` and `./rules/title-format-rule.md`. All four project docs were
  edited at 13:12 UTC on 2026-09-05, after the previous refresh took its hashes. All four lines were recomputed below.
- One was a GENUINE COPY CORRUPTION: `./EXTRACT-SPEC.md`. The second copy matched the existing manifest line exactly
  (`e34f6ce3…`) while the first copy did not, so the first copy was discarded and replaced with the verified one. That
  manifest line is unchanged.
The remaining 24 lines passed on the first copy. After the fix, `sha256sum -c MANIFEST.sha256 --quiet` printed TOOLKIT OK.

**Refresh note (2026-09-06, source-title windows — a 30th line):** `./source_windows.py` added at the user's decision after
the blr-batch24 source-title audit. Every 2–4-word contiguous window of the 50 source titles was checked against the batch's
kw-cache: 368 phrases had never been measured; one $0.09 call returned 74 of them at ≥ 1,000 and 22 at ≥ 20,000, among them
`essential oil diffuser` 74,000 (#35 had opened on `aromatherapy diffuser` 14,800 — a rule 2 miss), `flip flops` 135,000,
`card holder` 60,500, `coat rack` 49,500, `salt lamp` 27,100. The §1 "source title's own keywords are always measured"
split is now this script (exhaustive, zero model tokens) instead of the extraction agent's judgment. `./README-toolkit.md`
(step 4) and `./rules/title-format-rule.md` (§1, header note, §10.2 worked example) recomputed in the same turn. Measurements saved
in `claude/kw-cache-blr-batch24-addendum.md`.

**Refresh note (2026-09-06, source-window gate in title-check.py):** three lines recomputed after a deliberate RULE CHANGE
(user decision, same day as the script): `./title-check.py` now FAILS the batch when any 2–4-word window of a source title is
missing from kw.txt, or when products.json is not on disk — so a skipped README step 4 cannot reach the store. It imports
`source_windows.py` for the split. `./README-toolkit.md` (step 4 push-blocking note) and `./TITLE-SPEC.md` (inputs + step 3
third FAIL) recomputed in the same turn. Tested: missing windows → FAIL, windows present → 0 FAIL, snapshot absent → FAIL.

**Refresh note (2026-09-06, cluster-core gate):** four lines recomputed after a deliberate RULE CHANGE (user decision, after
the same blr-batch24 audit). `./title-check.py` now FAILS any comma cluster of a title that contains no measured 2+-word
phrase — the cluster's core must be a measured keyword; attributes and for/with tails stay free; `10 Pack`-type clusters are
exempt; apostrophes and word order are ignored. On the 50 pushed blr-batch24 titles it fails exactly the 5 clusters the audit
found by hand (#05 #09 #12 #16 #38) and passes the other 149. `./rules/title-format-rule.md` (§2 clause + header note),
`./TITLE-SPEC.md` (step 3 fourth FAIL) and `./README-toolkit.md` (step 5) recomputed in the same turn.

**Refresh note (2026-09-06, old-vs-new volume gate):** four lines recomputed after a deliberate RULE CHANGE (user decision).
`./title-check.py` now FAILS a title when the OLD title captured more product-naming volume (last word = productType head,
fit-rejects excluded) than the new one, and WARNs on total volume. Needs `old_title` in check_products.json (or product_id /
index against products.json) — build_check.py must supply it; when absent the check reports NOT RUN as a WARN. Tested on 7
blr-batch24 products with their real volumes: #35 fails (96,460 → 15,060, `essential oil diffuser` dropped), the other six
pass, and parent-category words in supplier titles are excluded with or without a fit_reject list. `./rules/title-format-
rule.md` (§2 clause + header note), `./TITLE-SPEC.md` (step 3 fifth FAIL), `./README-toolkit.md` (step 5) and `./build_check.py` (now writes `old_title` +
`product_id` per entry from products.json) recomputed.

**Refresh note (2026-09-06, unused-keyword gate, option b):** five lines recomputed after a deliberate RULE CHANGE (user
decision). `./title-check.py` now FAILS a title when a measured, fit-clean candidate (>= 1,000, not captured, not a twin of a
captured keyword) beats the weakest non-opener cluster's value and no reason is written for skipping it; with a reason
(`skip_reasons.json`, copied into check_products.json by `./build_check.py`) the line is MANUAL and the reason is saved in
rejects.json. A reason for a longer/shorter form of the phrase covers the family. Tested on the TRIMMERYENI #08 case: FAIL
without a reason, MANUAL with one. `./rules/title-format-rule.md` (§3 rule 2 clause + header note), `./TITLE-SPEC.md` (step 3
sixth FAIL, inputs) and `./README-toolkit.md` (step 5) recomputed.

**Refresh note (2026-09-06, cta-check restored in gate.py):** two lines recomputed after a CODE FIX, not a copy problem
(user instruction). `./cta_check.py` was wired into `./gate.py` as its last step in blr-batch21 (2026-09-04), but the
2026-09-05 image-floor rewrite of gate.py (the BLR-BATCH23 note above) was written from a version that did not carry the
call, so the project's gate.py has run without the CTA language check since then — the blr-batch23 run log's
"cta-check 0 FAIL" line came from the on-disk file of that session, not from this project copy. gate.py now calls
`cta_check.py` again after value-check; tested on a fixture: `Sizes S-XXXL` and `Adjustable brightness` FAIL, `Runs 7 days
per charge` passes. A 31st line — `./cta_check.py` — is added below: the blr-batch21 note said the manifest carried it, but the
list had no such line, so the session-start copy had no reason to fetch the file at all; the hash is of the project copy
re-written from the tested fixture in the same turn. `./DESC-SPEC.md` recomputed in the same turn: its gate list names cta-check, and its struct-check
summary no longer says "total 350–430 words" / "prose 65–110 in ≤2 <p>" (both superseded on 2026-09-05 — above 500 / above
110 are WARNs, never FAILs, and never a reason to drop a source line).

**Refresh note (2026-09-06, gate.py exit code + README step 6):** three lines recomputed after a CODE FIX (user decision).
`./gate.py` used to exit 0 whatever its sub-checks printed, although its docstring said "exit 0 only if all clean"; it now
counts its own [FAIL] lines, title-check [FAIL] lines and the non-zero exit codes of desc-check, struct-check, spec_cover,
value_check and cta_check, prints `=== gate: CLEAN ===` or `=== gate: N problem section(s)/lines ===`, and exits 1 on any
problem. Tested on a fixture: two bad CTA lines → exit 1; same product with benefit CTA lines → CLEAN, exit 0. WARN-only
output (prose > 110, total > 500, verbal-value warnings) still exits 0. `./README-toolkit.md` step 6 recomputed: it now
names cta_check.py among the gate's checks and states the exit-code contract. `./DESC-SPEC.md` recomputed: its gate
paragraph states the same contract instead of the earlier "exit code is not the verdict" sentence.

**Refresh note (2026-09-06, link / URL / price gate):** two lines recomputed after a CODE ADDITION (user instruction).
`./gate.py` now FAILS a product when any customer-facing field (descriptionHtml with `<img>` tags removed, title,
seo.title, seo.description) carries an `<a>` tag, a URL (`http(s)://`, `www.`, `mailto:`), an e-mail address, or a price
(`$ € £ ₺` + digit, `USD/EUR/GBP/TRY/TL`, `dollars/euros/pounds`). Until now gate.py checked only our own brand name, so the
format rule's "delete any link, brand name, or price found in the source" had no script behind its link and price halves.
Tested on a fixture: `<a href>`, `www.shop.com`, `$12.99`, `20 USD` → 4 FAIL, exit 1; a clean description with `32 oz` and
`24 hours` → CLEAN. A foreign BRAND name cannot be detected by a generic script and remains a RULINGS / review matter — this
gate does not claim to cover it. `./DESC-SPEC.md` recomputed: its gate list names the check.

**Refresh note (2026-09-06, a 32nd line — verify.py):** `./verify.py` added at the user's decision. README step 8 has
asked since 2026-09-03 for a script comparison of every live field after the push, and every run log reports
"verify.py … 0 failures" — but the script was never a project doc, so each session re-wrote it from the step-8 sentence
and no two batches necessarily checked the same fields (the same "session-only code" failure that spec_cover.py fixed
for the spec check in blr-batch22). The file was written from README step 8 plus the blr-batch13 / blr-batch23 run-log
descriptions of the checks, not recovered from any earlier session (none was saved). Fixture-tested: a correct live copy
→ 17 checks, 0 failures, exit 0; a copy with a wrong title, changed description text, 161-char seo.description, a dropped
tag + a duplicated season tag, changed status, wrong CTA JSON, a missing collection, a swapped media alt, a changed
variant price and a duplicate alt → 10 failures named one per line, exit 1. Shopify's own HTML re-formatting (whitespace
between tags, entity encoding) is normalized away; a mismatch says whether the tag-stripped TEXT differs or only the
formatting. First real-batch use: read its output in full — it has run on a fixture, not yet on a live batch.
`./README-toolkit.md` step 8 recomputed: it now names the command and the check list.

**Refresh note (2026-09-06, verbal spec values FAIL):** two lines recomputed after a deliberate RULE CHANGE (user decision).
`./value_check.py`: a numberless, non-list spec value ("Material: cotton", "Closure: zipper") whose content-word stems are
fewer than half present in the description is now a FAIL, not a WARN — until now "cotton" → "polyester" only warned while
"300 g" → nothing failed, and spec_cover.py passes such a line as long as the NAME word matches. `omit_per_ruling` now also
accepts the `Name: value` form ("Type: Other") beside the bare value. Fixture-tested: cotton/zipper present + "Type: Other"
exempted → 0 FAIL; polyester/magnetic instead → 3 FAIL, exit 1. `./DESC-SPEC.md` gate line recomputed. Expect a few more
gate FAILs per batch on supplier boilerplate lines; each is resolved by a RULINGS.md omission, never by silence.
`rules/description-format-rule.md` was NOT edited (its "Gate" paragraph already says value_check FAILs on dropped values).

**Refresh note (2026-09-06, a 33rd and 34th line — assume_check.py, age_check.py):** two scripts added at the user's
decision, and `./gate.py`, `./DESC-SPEC.md`, `./README-toolkit.md` recomputed for them.
- `./assume_check.py` — the "ADD NOTHING BEYOND THE SOURCE" gate. DESC-SPEC.md has carried the forbidden-assumption family
  since blr-batch12 (machine washable / no app / free app / BPA-free / food-safe / dishwasher / hand wash / power-cut memory /
  lifetime / warranty / certified / universal / waterproof vs water-resistant / sweat-dust-shock-proof / fast charging /
  silent / eco / non-toxic / natural / odorless / hypoallergenic / printed / "than ordinary" / "stronger than" / "X times"),
  but nothing enforced it — value_check, spec_cover and fact_cover only look for what is MISSING. For each family the
  description and SEO fields are scanned; a hit FAILs unless the extract (facts, specs, package, how_to_use, faq_source,
  variants, old title/seo, productType, identity) contains the family's own source pattern. Wired into gate.py before
  cta-check; exit code counts. Exemption: `add_per_ruling` in final/dNN.json (new optional field in DESC-SPEC's schema).
  Fixture-tested on the blr-batch12 inventions: "machine washable" from "washable", "waterproof" from "water-resistant",
  "no app required" and "free app" from "smartphone app", "remembers settings after a power cut" from "memory function:
  yes", "printed manual" from "user manual", "stronger than ordinary", "BPA-free", "certified" in seo.title, "universal" in
  seo.description → all FAIL; the same product written from the source's own words → 0 FAIL; "CE certified" with an
  `add_per_ruling` entry → [exempt]. The product TITLE is not scanned (title fit is title-check's job, §6).
- `./age_check.py` — description-format-rule.md "Age ranges", WARN only (user decision): a single-age phrase ("toys for 4
  year olds") whose sentence states no range, one that is not a title keyword, or more than one such phrase per product.
  Wired into gate.py after assume-check; never sets the exit code. Tested on the ddl1-batch5 magnetic-game text (three
  single-age sentences, no range) → 5 WARN; the corrected sentence ("… 4 year olds through age five, ages 4-5+") → 0.

**Refresh note (2026-09-06, README step 6c — benefit review by eye):** `./README-toolkit.md` recomputed after a PROCESS
RULE was added at the user's decision: before payloads, the main context reads every product's H2 + 5 bullets + 3 CTA
lines against the "Which five benefits" / "HANGİ 3 BENEFIT" filters and writes the outcome to the run log (corrected
product numbers, or an explicit "no correction" line). This was done ad hoc in blr-batch13 and skipped in blr-batch21;
it is not scriptable, so the rule makes the omission visible in the log instead. Cost: main-context reading of ~10 short
lines per product; no new agent, no new call.


**Refresh note (2026-09-06, a 35th line — rehost.py):** `./rehost.py` added at the user's decision after blr-batch25. README
step 5b (image re-host, Q14) had been written ad hoc every batch; in blr-batch25 the ad hoc script kept the `fileCreate`
ids only in memory, crashed on three Shopify "Internal Server Error" responses, and the three overlapping re-runs left
~50 duplicate copies in Files. The script now writes the created ids to image_ids.json after every group of 10, retries
every Admin API call up to 6 times, resumes from that file on a re-run (nothing uploaded twice), polls to READY, rewrites
the extract srcs (old value kept as `src_original`) and prints one summary line; exit 1 while anything is still foreign.
Tested with a mocked Admin API: a hard crash after the first group → the re-run creates only the remaining 6 of 16, no
duplicates; a second run on a finished batch is a no-op. `./README-toolkit.md` recomputed in the same turn (step 5b added,
store-constants note updated). First live run of the toolkit copy is the next batch — read its summary line.

**Refresh note (2026-09-06, DESC-SPEC "before you return" list):** `./DESC-SPEC.md` recomputed after a PROCESS note was added
at the user's decision — no rule, gate or threshold changed. In blr-batch25 all five description agents passed gate.py on the
first pass and were still sent back four times for things the rule documents already say: rule-1 WARNs on 30 products,
keywords doubled inside one bullet, all ten H2s of one agent written as sentences, aesthetics/variant CTA lines, synonym-only
second-net sentences, one agent altering the product title, a fit-rejected head word in a description. Each correction round
re-reads the agent's whole accumulated context, so those rounds cost about as much as the first pass. The seven-point list
puts those existing requirements in the agent's working spec so the first pass is the finished pass; the documents are
still read in full and the main-context 6b/6c review is unchanged.

**Refresh note (2026-09-06, README 6d — 6b + 6c in one message):** `./README-toolkit.md` recomputed after a PROCESS note
was added at the user's decision — no rule, gate or threshold changed. The main context still reads every fact_cover line
and every product's H2 / bullets / CTA lines; it now sends both correction lists to each description agent in one message
(one return per agent instead of two — blr-batch25 spent ≈1.2M tokens on the second round for the same output) and re-runs
fact_cover.py after the corrections, diffing against the first run, because a 6c edit can move a fact. Same turn: 6d also requires the main context to re-read by eye the lines the 6c
corrections changed (word matching cannot see a meaning drift) — user decision.

**Refresh note (2026-09-06, DESC-SPEC item 8 — prose two paragraphs, customer first):** `./DESC-SPEC.md` recomputed after
a PROCESS note was added at the user's decision (no rule, gate or threshold changed — description-format-rule.md already
allows a second paragraph and, since 2026-09-05, sets no prose ceiling). Reason: the user read the live blr-batch25 p38
(candle warmer) and found the single 90-word paragraph opening on the mechanism ("GU10 halogen bulb…") while the source's
three paragraphs carried the customer's moment (scent fills the room, no flame, no tunnelling). Item 8 fixes the order —
paragraph 1 = customer scene/benefit, paragraph 2 = how it works — and states that 65–110 is the norm, not a ceiling, so
agents stop treating it as one; every extra sentence must carry a source fact or a new keyword. Same day, same item: paragraph 1's last sentence closes the
buyer's biggest objection the source answers (user decision) — no new claim, source words only.

**Refresh note (2026-09-06, comparison table — a 36th and 37th line):** `./compare_build.py` and
`./rules/comparison-table-rule.md` (project path `claude/comparison-table-rule.md`) added at the user's decision (CVR element: a "Vepine vs Others" table in every
description). The agent writes only a `compare` object (2–5-word name + 5 source-fact rows, at least one Others cell
neutral); the script renders the fixed theme-coloured HTML, inserts it directly before `<h3>Key Features</h3>`, and FAILs
a missing / untraceable / all-✘ table. Six lines recomputed in the same turn: `./gate.py` (calls compare_build.py first;
brand scan now ignores the block — the store name is allowed there and nowhere else), `./struct-check.py` (block
mandatory, exactly one, before Key Features; its words excluded from the word budget), `./verify.py` (check 15 ignores the
block, new check 17: exactly one block live), `./DESC-SPEC.md` (schema + gate list), `./README-toolkit.md` (steps 6, 6c,
8, store constants), `./rules/description-format-rule.md` (skeleton line + hard-rule note). Fixture-tested: clean object →
rendered, idempotent on re-run, brand check silent; all-✘ / untraceable row / comparison wording / missing object / brand
inside name → FAIL; `Vepine` in prose → still FAIL; struct-check without the block → issue. First live use is the next
batch — screenshot the block on the theme and compare with the rule's colour list.
Same day, follow-up (user decision): the table is OPTIONAL per batch — brief question **Q17 — Comparison table: (Add
"Vepine vs Others" table / No table)**, unanswered = No table. `brief_flags.json` (`{"q17_compare_table": true|false}`,
written in README step 1) is read by compare_build.py / struct-check.py / verify.py; with No table the script removes any
existing block and nothing is required. Seven lines recomputed (all but gate.py). Tested: no flag → block removed, struct
silent; flag true → block required, rendered, struct silent.
Third note, same day (user decision): thin source still gets five rows — plain facts become NEUTRAL rows, nothing
invented; a source with fewer than five separable parts opts out with `"compare": null` + notes_for_log "compare: source
too thin" (compare_build.py FAILs a null without the log line; struct-check / verify.py expect no block for it). Five lines
recomputed. Tested: null unlogged → FAIL; null logged → no block, all three checks silent; normal → rendered.

**Refresh note (2026-09-06, Q18 dimension image — lines 38–40):** `./dim_image.py`, `./dim_attach.py` and
`./rules/dimension-image-rule.md` (project path `claude/dimension-image-rule.md`) added at the user's decision: an optional
per-batch size infographic built by script (rembg u2netp cut-out of the product's own gallery photo + navy dimension lines
+ size table, figures only from the source's L×W×H pattern), attached as gallery image 3 with the existing images shifted
down. `./README-toolkit.md` (step 1 flag, new step 7b, step 8) and `./verify.py` (media order = snapshot + inserted image;
alt checked) recomputed. Fixture-tested: build from a local photo → correct cut-out, lines on the product edges, M/L table;
`:g` float formatting replaced so `11.0` prints as the source wrote it. NOT tested live: the staged-upload PUT (storage
host may need the egress allowlist) and productReorderMedia — first Q18 batch reads dim_attach.py's output line by line.

**Refresh note (2026-09-06, Q19 fit block — lines 41–42):** `./fit_build.py` and `./rules/fit-block-rule.md` (project
path `claude/fit-block-rule.md`) added at the user's decision: an optional per-batch "Right for you if / Not the right
fit if" two-column block, content from the description agent's `fit` object (3–4 for / 2–3 not-for lines, every not-for
line derived from a source fact), HTML by script, rendered after the comparison block before `<h3>Key Features</h3>`;
`"fit": null` + logged reason opts a product out. `./gate.py` (calls fit_build.py after compare_build.py; brand scan
strips both blocks), `./struct-check.py` (block count / position per Q19; words outside the budget; the comparison-block
position check tolerates the fit block between it and Key Features), `./verify.py` (check "fit block"), `./DESC-SPEC.md`
(schema + gate list) and `./README-toolkit.md` (steps 1, 6, 6c, 8, rule-doc paths) recomputed. Fixture-tested: both
blocks render in order compare → fit → Key Features, re-run idempotent, struct silent; one not-for line / untraceable
line → FAIL; null + log line → no block, silent; "larger than the L size" passes (limit, not comparison).
Same day, RULE CHANGE (user decision — a wrong "not for" line kills a sale silently): `./fit_build.py`,
`./rules/fit-block-rule.md`, `./DESC-SPEC.md` recomputed. not_for is now 0–2 lines, each must carry a measurable limit
(number+unit, size label, indoor/outdoor, compatibility) and must not contain a preference/behaviour verb; with no such
limit the block renders as the left column only. Tested: preference line → FAIL; no-limit line → FAIL; 3 lines → FAIL;
one dimension line → two columns; [] → one column, struct silent, re-run idempotent.
Same day: `./compare_build.py` and `./fit_build.py` recomputed — every NUMBER written in a comparison row or a fit line
must occur in the source text (user question: value_check guards presence of source values, nothing guarded a number
invented in a block). Tested: 22.4 passes, 24.2 → FAIL, 23.4 in a compare row → FAIL.
Same day, two corrections (user asked "any other gaps?"): `./rules/comparison-table-rule.md` and `./DESC-SPEC.md`
recomputed — (1) text printed on source images is NOT a source (the agents never see images; the earlier wording
suggested it was); (2) "when in doubt, neutral, not ✘" — an Others ✘ is written only for a feature a cheap alternative
plainly lacks; 2–3 neutral cells of 5 is normal.

**Refresh note (BLR-BATCH26 test product, 2026-09-06 — fit block one column, before FAQs, exactly 4 lines):** seven lines
recomputed after a deliberate RULE CHANGE (user decision, after reviewing the live test product p00 of blr-batch26).
`./rules/fit-block-rule.md` (project path `claude/fit-block-rule.md`): the block is a single column "Right for you if"
only — the "Not the right fit if" column and the `not_for` key are removed for good (a wrong "not for" line kills a sale
silently); the block moves from before Key Features to directly before `<h3>FAQs</h3>`; the line count is fixed at
exactly 4 (three lines look empty in one column; a product that cannot fill four honest lines opts out with `"fit": null`).
The comparison block stays before Key Features (same decision: the table persuades early, the fit block closes the
decision late). `./fit_build.py` (single-column render, insert before FAQs, exactly 4 `for` lines, `not_for` ignored and
reported), `./struct-check.py` (fit block directly before FAQs, no "Not the right fit if" text; the comparison-block
position check no longer tolerates a fit block between it and Key Features), `./verify.py` (check "fit block" now also
requires the before-FAQs position and the one-column condition live), `./gate.py` (comment), `./DESC-SPEC.md` (schema:
`fit.for` exactly 4 lines, no `not_for`; gate list) and `./README-toolkit.md` (steps 6, 6c, 8) recomputed in the same
turn. Tested on p00: 4 lines → rendered before FAQs, gate CLEAN, live verify 19 checks 0 failures; 3 lines → FAIL; a
stray `not_for` key → ignored with a printed line; the pushed p00 carries the new layout.

**Refresh note (BLR-BATCH26, 2026-09-06 — cta_check.py two gaps closed):** three lines recomputed after a CODE ADDITION
(user decision, after checking p45 and p47 live). `./cta_check.py`: (1) the DESC-SPEC "≤30 chars text" limit is now
measured — a longer line FAILs (11 live lines in this batch were 31–33 characters and nothing had caught them);
(2) counts written as words ("Seven colors, one remote", "Six modes for every need") and included-accessory lines
("with remote", "4 nozzles included") now FAIL like digit counts do — the old pattern matched `\d+` only, so eight
products reached the store with feature-count CTA lines that the 6c reading also missed. `./gate.py` format check
tightened from 34 to 30 characters to match. `./DESC-SPEC.md` gate line names both. Fixture-tested: the three bad forms
→ 3 FAIL; `Runs 7 days per charge` and `Up to 4 hours cordless` still pass; a 33-character line → FAIL; all 50 live
blr-batch26 CTA sets → 0 FAIL after the same-day corrections.

**Refresh note (BLR-BATCH26, 2026-09-06 — CTA examples + named CTA pass):** two lines recomputed after a PROCESS addition
(user decision, no gate or threshold changed). `./rules/cta-benefits-metafield.md` gains a "Gerçek örnekler — blr-batch26"
section: the eight ❌ CTA lines that passed cta_check and the 6c reading in this batch and were caught only by the user
(feature counts, mode descriptions, audience lines, aesthetics), each with the ✓ line written from the same source facts,
plus the one-sentence test ("can it be read as 'that problem is gone'?") and the script-measured 30-character limit.
`./README-toolkit.md` 6c: the CTA lines are now read as their own named pass after the bullet / table / fit reading and the
run log carries a separate "CTA read on all N …" line — a log without it means the pass was skipped.

**Refresh note (BLR-BATCH26, 2026-09-06 — a 43rd line: CTA-REVIEW-SPEC.md, independent CTA reader):** `./CTA-REVIEW-SPEC.md`
added at the user's decision (CTA lines are the page's most important element; "I don't want to miss anything there").
One Sonnet agent per batch reads only each product's facts/specs + its three CTA lines — no description, no title — and
marks CERTAIN failures only (feature counts, what-it-does lines, audience/occasion lines, variant facts, unsourced
outcomes); runtime-per-charge figures and borderline lines are deliberately NOT marked so the pass adds no false-alarm
load. It never rewrites; the main context reads every mark, sends real misses back in the 6b/6c message and logs
`CTA independent review: N marked, K confirmed …`. Cost ≈ 0.1M tokens per 50 products; zero risk to output (it only
marks). `./README-toolkit.md` 6c recomputed (the step and its log line). The session-start copy list now has 43 lines.

**Refresh note (BLR-BATCH26, 2026-09-06 — CTA order rule):** `./rules/cta-benefits-metafield.md` recomputed after a
one-paragraph RULE ADDITION (user decision): the three CTA lines are written in order of importance — the customer's
biggest problem (the reason to buy) first, the other two descending — because on mobile most visitors read only the
first line. No gate or threshold changed.

**Refresh note (BLR-BATCH26, 2026-09-06 — a 44th line: keyfeat_cover.py, every source Key Features line in the list):**
`./keyfeat_cover.py` added at the user's decision after comparing p11's source Key Features (7 lines) with the live list
(5 items): "FLAME-LIKE LED EFFECT" and "MIST OUTPUT" sat in a bullet and the prose but not in the list. value_check and
fact_cover only ask whether a fact is somewhere; spec_cover covers the Specifications list only. The new script is
spec_cover's twin for Key Features: `--extract` writes `extract.key_features` from raw/ (the supplier's `<li>` and bold
"Name:" lines outside the spec / package / FAQ sections; headings as a fallback), and the check FAILs any of those lines
that is not an item of the new `<h3>Key Features</h3>` list (half the content words, or the Name half + one text word,
in one item). The user's rule: the line is ALSO a list item even when a bullet or the prose already carries the fact —
bullet = why buy, list = what is there. Fact-free marketing headings and forbidden-outcome lines go to `omit_per_ruling`
with a reason. Wired into `./gate.py` before value-check; `./rules/description-format-rule.md` §4, `./DESC-SPEC.md`
(read list + gate list) and `./README-toolkit.md` (steps 3 and 6) recomputed. Applied to the pushed batch: 145 source
lines were missing across 38 products; all added or logged, gate CLEAN over 50, only the Key Features list changed (checked
against the live copy), re-pushed, `verify: 50 products, 901 checks, 0 failures`. Session-start copy list is now 44 lines.

**Refresh note (BLR-BATCH26, 2026-09-06 — key_features completed by the extraction agent, paragraph features included):**
four lines recomputed after a PROCESS addition (user decision, no gate threshold changed). `./EXTRACT-SPEC.md`: the
extraction agent now COMPLETES `key_features` by eye after the script pre-fills it — (a) source feature lines the parser
missed (heading + paragraph, plain paragraph lists) and (b) the concrete features the source states only inside its
paragraphs (material, mechanism, function, mode, capacity, control, mounting, setting); never marketing sentences, specs
or package lines. `./keyfeat_cover.py --extract` no longer overwrites a non-empty list — it adds only parser lines not
already present, so the agent's additions survive a re-run. `./rules/description-format-rule.md` §4 and
`./README-toolkit.md` step 3 recomputed. Cost: inside the extraction agent's existing read, a few lines per product.

**Refresh note (BLR-BATCH26, 2026-09-06 — prose spec values enforced via extract.specs):** three lines recomputed after a
PROCESS addition (user decision). description-format-rule.md §5 has said since 2026-09-05 that a value the source gives
only inside a sentence gets its own Specifications line — but spec_cover.py compared only the supplier's table
(`extract.specs`), so nothing enforced that paragraph. `./EXTRACT-SPEC.md`: the extraction agent now appends every
measurable prose value (capacity, power, runtime, charge time, dimensions, weight, magnification, LED count, colour
temperature, lumens, ingress rating, material, mode/level counts, pack count, compatibility) to `extract.specs` as its own
`{name, value}` pair in the source's figure and unit — never a duplicate of a table value in another form, never an
estimate; a prose/table conflict keeps the table's pair and goes into `notes`. spec_cover.py then FAILs any pair missing
from the new list. `./rules/description-format-rule.md` §5 (enforcement sentence) and `./README-toolkit.md` step 3
recomputed. Applied to the pushed batch in one description-agent round: 33 pairs added across 17 products (the first
pass had already mined most prose values), gate CLEAN over 50, only the Specifications lists changed, re-pushed,
`verify: 50 products, 901 checks, 0 failures`.

**Refresh note (BLR-BATCH26, 2026-09-06 — a 45th line: unit_dual.py, dual units in Specifications):** `./unit_dual.py`
added at the user's decision: a Specifications measurement the source gives in one unit system only gets the other
system appended in parentheses (cm/mm/m ↔ in/ft, g/kg ↔ oz/lb, ml/l ↔ fl oz, °C ↔ °F; a tank/capacity "oz" is treated as
fluid ounces); the source figure stays first and verbatim; items already carrying both systems are untouched; electrical
units, hours, lumens, mAh, percentages are never converted; only the `<h3>Specifications</h3>` list is touched. Zero
tokens, idempotent, runs inside `./gate.py` before keyfeat-cover / value-check. Fixture-tested including negative
temperatures (-20°F → -29°C), ranges (113-131°F → 45-55°C), slash lists (50/65/80°C), dimension runs (28.8 x 27.8 x 0.3 cm
→ 11.3 x 10.9 x 0.1 in) and already-dual items (unchanged); two bugs found and fixed on the way (sign handling, "113-131"
parsed as a negative). `./rules/description-format-rule.md` §5, `./DESC-SPEC.md` gate line and `./README-toolkit.md`
step 6 recomputed. Applied to the pushed batch: 45 Specifications items across 50 products gained the second unit,
nothing else changed (field diff against the live copy), re-pushed, `verify: 50 products, 901 checks, 0 failures`.
Session-start copy list is now 45 lines.

**Refresh note (BLR-BATCH26, 2026-09-06 — unit_dual.py scope widened):** four lines recomputed after a RULE CHANGE (user
decision, same day as the script): dual units now apply to the prose paragraphs, the Key Features intro and list, the
Specifications list and the FAQ answers — and deliberately NOT to the H2, the five benefit bullets, CTA lines, the
comparison and fit blocks, FAQ questions, image alt texts or SEO fields (budgeted elements; a parenthesis there breaks a
limit or pushes a title keyword out of the first 500 characters). `./unit_dual.py` converts text nodes only (tags and
attributes untouched), protects the two blocks with compare_build / fit_build's own BLOCK_RE, treats a repeated-unit run
("75 cm x 45 cm") as one measurement and skips any measurement already adjacent to its conversion. `./rules/description-
format-rule.md` §5, `./DESC-SPEC.md`, `./README-toolkit.md` recomputed. Applied to the pushed batch: 48 more items
outside Specifications; protected parts confirmed unchanged; `verify: 50 products, 901 checks, 0 failures`.

**Refresh note (BLR-BATCH26, 2026-09-06 — unit_dual.py: imperial first):** two lines recomputed after a RULE CHANGE
(user decision: a US shopper who sees cm first reads the listing as imported). `./unit_dual.py` now writes the imperial
figure first and the metric one in parentheses whichever the source wrote (`5.1 oz (145g)`, `11.3 x 10.9 x 0.1 in (28.8 x
27.8 x 0.3 cm)`, `122/149/176°F (50/65/80°C)`), reorders pairs it or the source had already written metric-first, and
reorders source slash pairs (`15.2cm/5.98in` → `5.98in/15.2cm`); the source figure stays verbatim so value_check /
spec_cover still find it. Idempotent. `./rules/description-format-rule.md` §5 recomputed. Applied to the pushed batch:
every pair in the 50 products now imperial-first (0 metric-first pairs left), `verify: 50 products, 901 checks, 0 failures`.

**Refresh note (2026-09-07, comparison table — value columns centred):** two lines recomputed after a LAYOUT FIX (user
instruction, from a screenshot of a live blr-batch26 product: the ticks and the "Varies" / ✘ cells sat off-centre under
the `Vepine` / `Others` headers). `./compare_build.py`: the theme overrode the cells' inline `text-align:center`, so every
value cell and both value headers now centre their content with a flex wrapper inside the th/td (immune to theme
text-align rules), th and td of a value column share one width (120 px) and padding so header and cells have the same
centre, and the feature column is pinned `text-align:left !important`. New helper `parse_block()` reads name + rows out of
a rendered block (old or new template) so a template change can be applied to live products by re-rendering. Checks,
insertion point and BLOCK_RE unchanged. Fixture-tested: render → parse_block round-trip exact; strip_block exact; under a
hostile stylesheet (`td, th {text-align:right !important}`) a Playwright screenshot shows both value columns centred
under their headers; all 50 live blr-batch26 blocks parse to 5 rows + a 2–5-word name. `./rules/comparison-table-rule.md`
(format-rules bullet) recomputed in the same turn. Live re-render of the 50 blr-batch26 blocks: payloads built and
verified (outside-block text byte-identical on all 50) but the PUSH was not executed in this session — see the
2026-09-07 note in the run log / chat; it must be pushed and verified (`verify.py`, check 17) before this note is read
as "applied live".

**Refresh note (2026-09-07, fit block — conversion revision: situation — proof, no generic audience, closing sentence):**
four lines recomputed after a deliberate RULE CHANGE (user decision, from a screenshot of a live blr-batch26 fit block:
the four lines described the reader but gave no reason to believe the product delivers, the fourth line "someone of any
age who could use comfort" persuaded nobody, and the block ended dead before the FAQs). `./rules/fit-block-rule.md`
(project path `claude/fit-block-rule.md`): every line is now `situation — proof` (buyer's situation, one em dash, the
source fact that answers it), 30–110 chars; generic-audience lines (`any age`, `anyone`, `everyone`, `everybody`) are
forbidden; the script renders a FIXED closing sentence under the list — "If two or more of these sound like you, this is
the one." — which the agent never writes. `./fit_build.py`: checks exactly one ` — ` per line, proof ≥ 8 chars and
traceable to the extract on its own, generic-audience regex, new length range; constant `CLOSE`; render adds the navy bold
closing `<p>` inside the column (BLOCK_RE and the before-FAQs regex in struct-check / verify.py unchanged and re-tested).
`./struct-check.py`: a fit block without the closing sentence FAILs (old layout → re-run fit_build.py); imports `CLOSE`
from fit_build. `./DESC-SPEC.md`: `fit.for` schema line and gate line. Fixture-tested: four proof lines → rendered before
FAQs, closing sentence present, position regex matches, re-run idempotent, Q19 = Skip removes the block; a line without
the dash / a number not in the source / an "any age" line / a 5-char proof → 4 FAILs named one per line. NOT done in this
session: no live product was re-rendered or pushed, and `./verify.py` and `./README-toolkit.md` were NOT edited (verify's
position + one-column checks still hold for the new layout; the closing-sentence check lives in struct-check only). The
50 live blr-batch26 fit blocks still carry the old layout — re-rendering them needs new `situation — proof` lines from a
description-agent pass (the old lines have no proof half), so it is a batch task, not a script re-render.
**Refresh note (DENEME batch, 2026-09-07 — supplier policy promises never in copy):** three lines recomputed after a
deliberate RULE CHANGE (user instruction after the DENEME summary: "bunları hiçbir zaman açıklamaya dahil etme").
Warranty, guarantee, money-back / refund / risk-free trial, return policy and customer-support / after-sales promises
are a third-party seller's policy, not a product fact, and are never written anywhere — prose, lists, comparison block,
fit block, FAQ, CTA lines, SEO — even when the source carries them as a spec line (`Motor warranty: 2 years`); every
such source line goes into `omit_per_ruling` ("supplier policy, not product fact"). `./gate.py` FAILs the family in
every customer-facing field and in the CTA lines (no `add_per_ruling` exemption); `./DESC-SPEC.md` (standing user
rules) and `./rules/description-format-rule.md` (Hard rules) state the rule. Fixture-tested: a p04 copy with "2-year
motor warranty and a 30-day money-back guarantee" in prose and "Risk-free 30-day trial" as a CTA line → 2 FAIL, exit 1;
the 7 live DENEME finals → CLEAN. Note: `assume_check.py` still lists "warranty" among its source-sourced families —
that check is now moot for this family because gate.py fails it regardless of the source.


**Refresh note (STR-DUB-2-batch1, 2026-09-07):** one line recomputed — `./rules/description-format-rule.md` was STALE, not a corrupted copy: two independent copies of the project doc agreed byte-for-byte and both differed from the manifest, because the doc had gained the 2026-09-07 §5 "attribute name before the colon is bold" note and the supplier-policy hard rule after the previous hash was taken. New hash 4221db1a…d0523 taken from the verified copy (sha256 of the file on disk that passed the batch). The other 44 lines passed (three genuine copy corruptions in that session — README-toolkit.md, dim_image.py, fit_build.py, all dash/quote retyping — were fixed by re-copy and match the existing lines).

68d0bf45181514726364bba16a3e1eafa62d40f78e3d9ffc31b19540fefc4b95  ./para_feat.py
**Refresh note (STR-DUB-2-batch1 follow-up, 2026-09-07 — Key Features copies + paragraph sweep, a 46th line):** five lines recomputed
after a deliberate RULE CHANGE (user decision) and `./para_feat.py` added. The user found that 88 of 240 source Key Features
lines had reached the store pasted verbatim (keyfeat_cover.py only asked "is it present?", and pasting is the cheapest way
to be present) and that 45 of 48 products had left extraction with exactly the script's pre-filled list — the paragraph
features and prose spec values EXTRACT-SPEC asks for had not been added and nothing made that visible. `./keyfeat_cover.py`
now FAILs a pasted line ([COPY]: sentence fabric >= 90% identical in sequence after removing every value word — numbers,
units, spec/package/variant tokens — so a fact can never be changed to pass; <= 6 fabric words exempt). `./para_feat.py`
(new, zero tokens, always exit 0) lists paragraph sentences with a feature marker not covered by key_features and prose
figures absent from specs; the main context sorts them into added / dismissed and the run log carries the counts.
`./EXTRACT-SPEC.md` (mandatory `NN | script X | paragraph features added Y | prose specs added Z` reply line, reason for
every 0), `./DESC-SPEC.md` (gate line), `./README-toolkit.md` (step 3b, step 6, 6c "KF read" line) and
`./rules/description-format-rule.md` (§4 copy gate sentence) recomputed. Tested on the live batch: 94 [COPY] lines on 34
products → rewritten by the description agents, values unchanged (value_check / spec_cover clean), 0 copies; para_feat
44 KF flagged → 5 added (p08 no-soaking, p11 light reduction, p22 diffused glow, p30 ABS shell, p44 4-inch cushioning),
39 dismissed; 4 SPEC flagged → 1 added (p45 inflation time 30 s), 3 dismissed (p20 ruled conflict); re-pushed, verify 0 failures.

**Refresh note (STR-DUB-2-batch1 follow-up 3, 2026-09-07 — independent KF/spec reader, lines 48–49):** `./KF-REVIEW-SPEC.md`
and `./kf_review_input.py` added at the user's decision, `./README-toolkit.md` recomputed (step 3c). One Sonnet agent per
batch reads only the source paragraphs and the extract's two lists — never the description — and marks certain misses;
the main context confirms or dismisses. Validated live on this batch with `--all`: 8 marked, 8 confirmed and pushed
(verify 47 products, 847 checks, 0 failures); every mark had passed para_feat.py's word match, which is the gap the
reader closes (sentence-type features and numberless spec values). Eligibility: paragraphs > 80 words (3 of 47 here).

**Refresh note (STR-DUB-2-batch1 follow-up 4, 2026-09-07 — How to Use steps only, Usage Tips section; lines 50–51):**
`./howto_check.py` and `./usage_tips.py` added at the user's decision; `./gate.py` (both wired after cta-check),
`./struct-check.py` (an audience line under How to Use is an issue; Usage Tips position), `./rules/description-format-
rule.md` (§7 rewritten, §7b added, skeleton line), `./EXTRACT-SPEC.md` (how_to_use = steps only; usage_tips field),
`./DESC-SPEC.md` (schema + gate list) and `./README-toolkit.md` (step 3d, step 6) recomputed. Reason: 9 products had the
supplier's "Usage Recommendations" audience lines pasted verbatim under a How to Use heading (the old §7 said "reproduce
it"). Applied live: 47 audience lines moved from how_to_use to facts, 9 How to Use sections removed, 23 products gained a
<h3>Usage Tips</h3> list written in the agents' own sentences (3 lines ruled out: p18/p24 CPAP comparison, p28 medical
implication), 23 descriptions re-pushed, `verify: 47 products, 847 checks, 0 failures`.

**Refresh note (STR-DUB-2-batch1 follow-up 5, 2026-09-07 — no wholesale regeneration of final files):** `./DESC-SPEC.md`
recomputed after a PROCESS rule was added at the user's decision: a description agent edits only the named field of an
existing final/dNN.json (read-modify-write) and never rebuilds files from a script — one agent's build script had reverted
the main context's `category_proposal` values three times in that batch (caught by verify.py each time).

**Refresh note (STR-DUB-2-batch1 follow-up 6, 2026-09-07 — three consistency fixes, user decision):** `./unit_dual.py`
(scope now includes the Usage Tips and How to Use lists; fixture: "12 L" in a tip → "405.8 fl oz (12 L)"),
`./fact_cover.py` (a facts line that is also a usage-tip line is skipped — usage_tips.py enforces it item by item, scoring the
rewrite was noise: 40 → 29 lines on the live batch), `./para_feat.py` (a prose figure counts as ruled only through an explicit
omission — final omit_per_ruling or the new `rulings_omit.json` written with RULINGS.md — never a text search in RULINGS.md),
`./rules/description-format-rule.md` (§5 scope sentence) and `./README-toolkit.md` (step 3b) recomputed.

**Refresh note (STR-DUB-2-batch2, 2026-09-07):** one line recomputed — `./rules/cta-benefits-metafield.md` was STALE, not a corrupted copy. Two independent copies of the project doc agreed byte-for-byte (`4417d0aa…521a`) and both differed from the manifest (`f9c809f2…`), so per §6 the manifest line was stale: the doc had gained its blr-batch26 CTA-order paragraph and the "Gerçek örnekler" section after the previous hash was taken. New hash taken from the verified copy that passed the batch. The other 50 lines passed; one genuine copy corruption in that session (`./title-check.py`, first copy `430c480b…`, second independent copy matched the manifest exactly) was fixed by re-copy, so that line is unchanged.

**Refresh note (STR-DUB-2-batch3, 2026-09-07 — unit_dual.py: three parsing bugs fixed):** one line recomputed after a CODE FIX
(main-context finding while reading the finished Key Features lists; scheduled run, no user present). `./unit_dual.py`:
(1) `4G` / `5G` (network generation) was converted as 4 grams → `0.1 oz (4G)` on p04/p06/p07 — an uppercase `G` unit is now
skipped (grams are written lowercase); (2) `9.45 in L` / `23.99 cm L` (L = length label after a unit) was read as litres →
`319.5 fl oz (9.45 in L)` on p16 — an uppercase `L` after a run that already carries a unit is skipped; (3) a single-unit
value backtracked into run + unit (`49mm` → `49m` + `m` → `160.8 ft (49mm)` on p05/p07/p08/p09/p22; `250ml` → `250m` + `l`)
— the inner unit of a run now needs a following separator (x / - / to). Also: `60 oz tank` in prose/FAQ is treated as fluid
ounces even when the item has a `Name:` prefix. Fixture-tested: `Display Size: 49mm` → `1.9 in (49mm)`; `Tank: 250ml` →
`8.5 fl oz (250ml)`; `Network: 4G` unchanged; `Size: 14.17 in H × 9.45 in L × 7.09 in W` → only the in-values converted;
the earlier fixtures (`145 g`, `12 L`, `28.8 * 27.8 * 0.3 cm`, `113-131°F`, `15.2cm/5.98in`, already-dual items) unchanged.
The wrong pairs were reverted in the batch's finals before the push; `verify: 50 products, 902 checks, 0 failures`.

**Refresh note (2026-09-08, run artefacts leave the project):** `./README-toolkit.md` recomputed after a PROCESS CHANGE (user
decision — the project hit its 2 MB knowledge cap; 129 of the ~200 docs were per-batch backup-alt / kw-cache / run-log /
backup-titles files). From now on only `claude/backup-titles-<tag>.md` (before the push) and `claude/run-log-<tag>.md` (after
verify) are project docs; `kw-cache-<tag>.md` and `backup-alt-<tag>.md` are written to /mnt/user-data/outputs/ and sent to the
chat with SendUserFile instead (README header note; steps 4 and 7). No gate, rule or threshold changed. Older run docs were
copied to Google Drive `Vepine/<tag>/` the same day and 45 of them deleted from the project after byte-size verification.
Hash taken from the file written on disk in the main context (24623 bytes, newline-terminated).

**Refresh note (2026-09-08, source_windows.py — DataForSEO length gate):** one line recomputed after a CODE FIX (user
decision, from the STR-DUB-2-batch4 run log's "For the next run" item 1). `./source_windows.py` now drops any window over
DataForSEO's per-keyword limit (80 characters / 10 words) before it is emitted. Reason: `google_ads/search_volume/live`
rejects an over-limit keyword with `40501 Invalid Field: 'keywords'. Keyword text exceeds the allowed limit` and ONE bad
keyword voids the WHOLE task — the call returns a top-level `20000 Ok` with zero results, which reads as a successful
call. In batch4, 49 of 1,277 windows were whole supplier titles over that limit; the first attempt returned nothing on
every chunk and the run recovered only because the main context noticed the empty result. The filter lives inside
`windows()` (new `measurable()` helper, new `keep_oversize` argument used only by `main()` for its stderr report), NOT
only in `main()`, so both consumers agree: the phrase is not offered as a candidate, and `./title-check.py` — which
imports `windows()` for its push-blocking "source windows NOT measured" gate — no longer demands a phrase DataForSEO
cannot measure. Nothing measurable is lost: an over-limit window is always a whole supplier title, and every 2–4-word
phrase inside it is still emitted separately. `main()` prints the dropped count and lists each dropped phrase on stderr,
so a batch with unusually long titles is visible in the run log. Fixture-tested: a 91-char / 13-word title → 23 windows
emitted, 1 dropped and named on stderr, exit 0; `windows(norm(title))` (the title-check path) returns nothing over the
limit; a short title's whole-title phrase is still emitted. `./title-check.py` was NOT edited — it needed no change, and
its gate is now satisfiable by construction. `./README-toolkit.md` was NOT edited: step 4's description ("every
contiguous 2–4-word window") stays true and the dropped phrases were never measurable candidates.

**Refresh note (2026-09-08, verify.py — collections.json in any shape):** two lines recomputed after a CODE FIX (user
decision, from the STR-DUB-2-batch4 run log's "For the next run" item 2 — the second of the two batch4 traps; the first,
source_windows.py, is the note above). `./verify.py` read collections.json ONLY as a `{title: id}` map, while README step 8's
refresh snippet produces the raw GraphQL response; written the README way, every title was "not in collections.json",
check 10 printed a `[note] … not resolvable by title` on every product and never actually ran, and the summary line still read
"0 failures" — in batch4 this hid on 43 products until the file was rewritten by hand. New `load_colmap()` accepts the map,
the raw response (`{"data": {"collections": {"edges": …}}}`), its inner `{"collections": …}` / `{"edges": …}` objects, and a
plain list of `{id, title}` or `{node: {id, title}}`; an unrecognised shape or a file that yields no collections is a hard
exit (1) with the reason — never a note. Fixture-tested: all five shapes → 18 checks, 0 failures; a product missing its
collection → `[FAIL] collections` under both the map and the raw shape; empty response and `{"foo": "bar"}` → exit 1 with
the message; no file given → the existing `[note]` + 17 checks, unchanged. Everything outside the loader is byte-identical
to the previous version (the pristine copy re-hashed to the old line before the edit). `./README-toolkit.md` recomputed:
the collections.json line under "Store-specific constants" now says either shape is accepted (pristine copy re-hashed to
`10369ac2…` before the three added lines).

**Refresh note (2026-09-09, a 53rd line — kw_measure.py, the one DataForSEO path):** `./kw_measure.py` added at the user's
decision and `./README-toolkit.md` recomputed (step 4). Reason: the DataForSEO error log showed two `40501 Invalid Field:
'keywords'. Keyword text exceeds the allowed limit` errors on 2026-09-09 (07:50 and 08:18 UTC) — a day AFTER the
source_windows.py gate — because that gate covers only the windows the script itself emits; the extraction agents'
candidates/cNN.json and the step-1b extra list went to the API unfiltered, and the two rejected keywords were whole supplier
titles (14 and 17 words) from that side. Step 4 was an ad hoc curl until now, so the filter had no fixed place to live and a
future session could skip it. The new script is the ONLY route from a candidate list to the API: it unions .json / .txt
candidates in any shape, normalises them as source_windows.norm() does (apostrophes closed up, other non-alphanumerics
removed — DataForSEO rejects those too), dedupes, skips what kw.txt already has, applies `measurable()` (imported from
source_windows.py — one definition of the 80-char / 10-word limit) BEFORE chunking and names each drop on stderr, sends ≤950
per call, EXITS 1 on any task status other than 20000 (40501; a 4020x rate-limit answer is retried once after 65 s) and on a
chunk with ZERO results (the silent-void case: one bad keyword empties the chunk while the call reads `20000 Ok`), appends
`keyword|volume|competition|cpc` to kw.txt and the --cache doc after each good chunk (a crash keeps earlier chunks, a re-run
measures only what is missing), records a keyword the API did not echo at 0 and counts it as `[not returned]`, and reads
the credentials from dataforseo-credentials.md without ever printing them. `--dry-run` costs nothing. Fixture-tested with a
mocked API on the two keywords from the error log plus normal candidates: dry run → 2 dropped and named, 5 to measure;
void response → exit 1, nothing written; 40501 task → exit 1, nothing written; good response → 5 lines appended to kw.txt
and cache, one non-echoed keyword recorded at 0 and named; re-run → 0 to measure, no call. `./source_windows.py`,
`./title-check.py` and `./TITLE-SPEC.md` were NOT edited (1b keeps its wording; README step 4 says the same command
serves it). Not yet run on a live batch — the first batch after this date reads its stderr summary lines into the run log.
No gate, rule or threshold changed; nothing that DataForSEO could measure is dropped.
Same day, second pass after the user shared the account's full error export (100 rows, 2026-09-08/09) — both files
recomputed. The export showed two more families beside the five over-limit keywords: (a) four 40501 "too many words" rows
whose keyword was source_windows.py's OWN stderr summary line (`source windows 50 titles - 1253 windows 1253 not yet
measured`) — captured into candidates/source_windows.txt with `2>&1`; after normalisation it is exactly 10 words and would
have passed the length gate, so kw_measure.py now refuses report-shaped lines (REPORT_RE: `source_windows:` / `kw_measure:`
prefixes, `[oversize]` / `[not returned]` tags, `N titles -> N windows`, `not yet measured`, `dropped over the DataForSEO`)
and names each on stderr; (b) ~90 40202 rows in one minute (`The rates limit per minute has been exceeded: 12 >= 12`) — the
account's live limit is 12 calls/min, not 2,000, and a failed call was retried in a tight loop; kw_measure.py now paces
calls 6 s apart (≤ 10/min) and retries a 4020x answer exactly once after 65 s, then exits 1 — never a loop. The three
`id_list` / `Invalid Path` rows of 2026-09-08 17:53 are from a hand query of the error endpoint, not from the pipeline.
Fixture re-run with the three report-line shapes appended to source_windows.txt: all three refused and named, keyword
output unchanged. README step 4 carries both traps in one sentence each.
Third pass, same day, after the account's ERROR DYNAMICS chart (02–09 Sep: 804 errors, ~800 on 08 Sep alone — 40202 ×672,
40501 ×128, 50301 ×3): `./kw_measure.py` recomputed once more — the single 65-s retry now also covers a 5xxxx task status
(DataForSEO server-side, e.g. 50301 Internal Error), so a transient API fault does not end a run on the first chunk; a second
failure still exits 1. Tested with a mock: 50301 then Ok → 2 calls, chunk written. The 126 40501 rows (the export showed 9)
are the same bad chunk re-sent in the 2026-09-08 loop — no new keyword family.

**Refresh note (2026-09-08, additional source sections — a 52nd line: sections.py):** `./sections.py` added at the user's
decision, and eight lines recomputed after a deliberate RULE CHANGE. Reason (user question, same day): the extraction kept
only the known source blocks as fields (specs, package, how_to_use, usage_tips, key_features, faq_source); every other
headed block of the supplier's description — Care Instructions, Warnings / Safety, Materials, Design, Applications,
Compatibility, Storage, Charging, Installation, Size Guide, Notes — fell into `facts` as loose lines, lost its heading and
was dissolved into the prose. Decisions: (1) a block that carries a product fact (Tip A) becomes its own `<h3>` section —
list or paragraphs, every line own words, values verbatim, no copy, no merge, no invented `<h3>`, position; (2) headings are a NORMALISED
vocabulary (`CANON` in sections.py — Care Instructions, Safety Warnings, Materials, Design, Applications, Compatibility,
Storage, Charging, Installation, Size Guide, Notes), never the supplier's own; (3) a fact already in the prose / Key Features
is still written in its section — same fact, different sentence (the §4 rule); (4) applies from the first batch after this
date — NO pushed product is re-processed. `./sections.py` (`--extract` writes extract.sections / sections_dismissed, moves
section lines out of key_features; check FAILs missing section / line / [COPY] / [MERGED] / invented `<h3>` / position,
WARNs on order), `./gate.py` (wired after usage-tips), `./struct-check.py` (a non-skeleton `<h3>` only between Package
Includes / How to Use / Usage Tips and the fit block / FAQs), `./unit_dual.py` (scope: every `<h3>` section after Package
Includes, Package Includes itself excluded — How to Use / Usage Tips fall in the same rule), `./fact_cover.py` (section lines
skipped, like usage tips), `./rules/description-format-rule.md` (§7c, skeleton line, §4 and §5 sentences), `./EXTRACT-SPEC.md`
(`sections` / `sections_dismissed` fields, reply line `| sections S`), `./DESC-SPEC.md` (read list, standing rule, schema,
gate list), `./README-toolkit.md` (step 3e, steps 6 and 6b). Fixture-tested on a fleece blanket source with four extra
blocks: Care Instructions (list, 3 lines) and Safety (prose, 1 line → `Safety Warnings`) kept, "Elegance That Takes Off"
dismissed as marketing-only, "Warranty" dismissed as policy, the 3 care lines removed from key_features; a good page → exit
0; pasted lines → 2 [COPY]; two lines in one item → [MERGED]; missing section → FAIL; an invented `<h3>Why You Will Love
It</h3>` → FAIL; sections before Package Includes → 2 FAIL (sections.py and struct-check both); swapped order → WARN only;
a ruled-out line with the section absent → clean, with the section present → FAIL. unit_dual: `40°C` in Care Instructions
and `1.5 m` in Safety Warnings converted, the bullets and Package Includes untouched, idempotent. Not run on a live batch
yet — the first batch after this date reads the `sections --extract` summary line and the [UNMAPPED] lines in full.

**Refresh note (2026-09-09, STR-DUB-2-batch8 — sections.py shape tests):** two lines recomputed after a deliberate RULE
CHANGE (user decision, after the script's FIRST LIVE RUN). `./sections.py` proposed a section on 42 of 50 products and every
one was the supplier's LEAD HEADLINE + intro paragraph — the description's own opening, not an additional headed block. Worse,
7 had already been auto-mapped to a canonical name by a stray keyword inside that marketing sentence: `Charging` from "High
Power Blue Laser Pointer for Long-Distance Targeting", `Safety Warnings` from "Reflective Cat GPS Tracker Collar for Enhanced
Safety", plus `Care Instructions`, `Design` ×2, `Storage`. gate.py cannot catch this class of error — once a block is in
`extract.sections` it only asks whether the page reproduces it — so the only guard was the main context reading the --extract
summary, and a run that skipped that read would have published `<h3>Safety Warnings</h3>` over a marketing sentence. Two SHAPE
tests now dismiss such a block before the fact test: (1) `MAX_HEAD_WORDS = 4` — a heading longer than four words is a marketing
headline, not a section heading (all 42 mis-detected headings were 5-8 words; every heading the fixtures keep is 1-3);
(2) the source's FIRST heading over prose is the description's lead, kept only when it is a short heading that also names a
canonical family (so a source genuinely opening with "Care Instructions" survives). Both were measured on the batch first:
all 42 mis-detected blocks were heading index 0 AND 5-8 words, so either test alone catches them. The `--extract` summary line
now breaks the dismissals down by reason (marketing / policy / description lead / long marketing heading);
`./README-toolkit.md` step 3e recomputed for the two tests and the new summary format. Fixture-tested: the fleece-blanket
fixture is unchanged — Care Instructions (list, 3 lines) and Safety (prose, 1 line → `Safety Warnings`) still kept, "Elegance
That Takes Off" still dismissed as marketing-only, "Warranty" still dismissed as policy, the 3 care lines still moved out of
key_features — plus its `<h2>` product headline now correctly dismissed as the lead; a source whose FIRST heading is
"Care Instructions" over prose is KEPT (the exception); a non-first 6-word heading is dismissed and stays visible in
`sections_dismissed` so the main context can move it back. Check mode is untouched and re-tested: good page → exit 0;
invented `<h3>` → FAIL; missing section → FAIL; [MERGED] → FAIL; section before Package Includes → FAIL; a ruled-out line with
the section absent → clean, with the section present → FAIL; a pasted line → [COPY] FAIL. Re-run over the 50 live
STR-DUB-2-batch8 products: `0 of 50 products carry a fact section, 42 dismissed (description lead 42), 0 UNMAPPED` — exactly
the outcome the main context had reached by hand — and `gate.py` over all 50 still prints `=== gate: CLEAN ===`.

**Refresh note (2026-09-09, Q18 dimension image — gallery position 2, not 3):** three lines recomputed after a deliberate
RULE CHANGE (user decision, in the user's words: the "actual size" image is the product page's 2nd image; the source's
images from the 2nd onwards shift one place down, nothing is removed). `./dim_attach.py`: new `POSITION = 2` constant at
the top; the reorder index is `min(POSITION - 1, n_before)` so a product with one existing image gets it appended (position
2 anyway); docstring carries the rule and the date. `./rules/dimension-image-rule.md` (project path
`claude/dimension-image-rule.md`): "Where it goes" section rewritten for position 2, with the note that products attached
before this date keep their position-3 order unless re-attached. `./README-toolkit.md` (steps 7b and 8) recomputed.
`./verify.py` was NOT edited — it reads the position from `dim/media.json`, so old (3) and new (2) batches both verify
against what was actually done. Compile-checked, not run live in this session. Q18's first live run was STR-DUB-2-batch9
(same day, other session, before this change): 5 products — p07, p34, p36, p09, p49 — attached at position 3; the staged
PUT worked (no egress problem). Those five stay at position 3 until re-ordered (one productReorderMedia each; the media
is findable by its alt "… – actual size and dimensions"). That run log also records a `DIM_RE` gap in `./dim_image.py`
(a source that repeats the unit after each figure — `12.91 in x 2.96 in x 2.96 in`, `46cm x 32cm x 16cm` — never
matches; two products were rebuilt by hand) — NOT fixed here, open item. The stale duplicate `./README-toolkit.md` line
in the block below (two lines carried the file since 2026-09-08) is now the same hash on both lines.

**Refresh note (2026-09-09, Q18 dimension image — axes must be labelled):** three lines recomputed after a deliberate RULE
CHANGE (user decision, in the user's words: "yanlış görsel daha kötü" — a wrong image is worse than no image). `./dim_image.py`:
a three-figure triple is used only when the source NAMES the axes — an order key next to the figures or once anywhere in the
source (`(L x W x H)`, `LxWxH`, `Length x Width x Height`, `H x W x D`, a spec row named that way) or labelled figures
(`L 46 cm x W 32 cm x H 16 cm`, `Length: 46 cm, Width: …`, `46 cm (L) x …`, three Length / Width / Height spec rows); a
bare `2 x 5 x 6 cm` is skipped with `axes not labelled` (dim/build.json + the summary line lists the products) instead of
being drawn in source order (batch9 p49). Same edit closes the batch9 open item — the unit may now follow every figure
(`46cm x 32cm x 16cm`) — and never reads a package / box / carton / shipping / parcel measurement as the product's size;
mixed units, two axes only and diameter × height are skipped. Fixture-tested (22 cases): bare triple in spec / variant →
skip with the note; order key in spec name, after the figures with repeated units, `H x W x D` reordering, a global order
key applied to two variant sizes, labelled inline / worded / after-figure, three spec rows → the expected (L, W, H, unit);
package-only → skip, package + product → product; mixed units / two axes / diameter → skip; `3"` inches quote → in.
`./rules/dimension-image-rule.md` (rule 1 widened, rule 1b added) and `./README-toolkit.md` (step 7b) recomputed. compose()
and the attach step are untouched. Not run live in this session.

**Refresh note (2026-09-09, Q18 — unlabelled figures resolved by the photo, not skipped; same session, minutes later):**
three lines recomputed after the user relaxed the rule above (user decision: "kuralı gevşetelim" — the safe way to more
images is ours, not the supplier's). `./dim_image.py`: labelled sources are used as written (no change); an UNLABELLED
triple is no longer skipped outright — `resolve_axes()` compares the cut-out's width/height (the same rembg cut-out the
picture is drawn from, now produced once by `cutout()` and passed to `compose()`) with the six possible assignments of the
three figures and uses the single assignment that fits within `PHOTO_TOL` 20 % when the runner-up is ≥ `PHOTO_GAP` 30 %
off; GAP > TOL means a photo measured within tolerance can never select a wrong assignment, only an ambiguous one (skipped
as `axes ambiguous (photo): …` with the ratios). Equal figures collapse so a 20×20×10 is not "ambiguous" against itself;
with several sizes the largest is tested and the mapping applied positionally to all. `dim/build.json` gains `axes` per
product ("labelled" / "photo-ratio: photo 0.70 vs best 32/46=0.70, next 16/32=0.50 -> L=b D=c H=a"); the summary line
counts labelled / photo-ratio / ambiguous. Fixture-tested: backpack 46×32×16 at photo 0.70 → L=32 H=46 (the batch9 p49
case, now right by itself); 0.80 → same; 0.62 → ambiguous (skip); 2.90 → L=46 H=16; 1.00 → no fit (skip); 30×25×20 at
1.20 → two fit (skip); 20×20×10 at 1.00 → resolved; two variant sizes → same mapping on both; the 22 labelled/parse cases
from the note above unchanged. `./rules/dimension-image-rule.md` (rule 1b now "labelled = as written", new rule 1c) and
`./README-toolkit.md` (step 7b summary-line format) recomputed. The rembg part of the test is not run in this session
(no model here); the ratio logic is pure arithmetic and is what the fixtures cover. First live batch: read the `axes`
value of every photo-ratio product next to its picture in the rule-5 look.

**Refresh note (2026-09-09, Q18 — two figures are enough; same session):** three lines recomputed after a RULE ADDITION
(user decision: "bunu da ekleyelim"). `./dim_image.py`: when no source text carries a three-figure run, a TWO-figure
measurement is read — `DIM2_RE` (`200 x 150 cm`, `46cm x 32cm`), labelled pairs through `roles2()` (`W 46 cm x H 32 cm`,
`Diameter 20 cm, Height 30 cm`, `Length 200 x Width 150 cm` → length horizontal / width vertical, two Diameter / Height spec
rows; `diameter` / `dia` / `ø` added to AXIS), unlabelled pairs through the same photo-ratio test with two candidates.
Three figures anywhere always win. Entries carry `W = None`; `compose()` then draws no depth text and a Size / Length /
Height table; `resolve_axes()` handles both arities and labels the pair result `photo-ratio (2 figures): …`. Fixture-tested
(14 parse cases + 8 resolutions + 2 renders looked at): 3-figure cases unchanged and precedence over a 2-figure line in
another field; raw / repeated-unit / labelled / spec-row / variant pairs; package and mixed-unit pairs → none; yoga mat
200×150 at photo 1.33 → L=200 H=150, at 0.75 → L=150 H=200, at 1.00 → no fit, at 1.15 → resolved; 30×28 at 1.05 →
ambiguous; 20×20 → resolved; `pack of 2 x 5 cm hooks` at a square photo → no fit (skip). `./rules/dimension-image-rule.md`
(rule 1d; the 1c sentence that had skipped two-axis sources corrected) and `./README-toolkit.md` (step 7b) recomputed.

**Refresh note (2026-09-09, Q18 — three gaps closed after the user asked "what did we miss?"; same session):** four lines
recomputed. (1) `./dim_image.py`: a decimal comma (`46,5 x 32 x 16 cm`) was read as `5 x 32 x 16` — a WRONG figure the
photo test cannot always catch; `NUM` now accepts `46,5` and `dec()` normalises it (a `1,200` thousands separator becomes
1200; the first figure may not be preceded by a digit / comma / dot). (2) same file: the measurement of the thing a
product FITS (`fits mattresses up to 200 x 150 cm`, `for 15 inch laptops`, `compatible with 40 x 60 cm frames`) was read
as the product's own size, and for a sheet / case / frame the photo test passes because the proportions match — the
package exclusion now also covers fits / for / compatible / suitable / up to / accommodates / holds / designed for; a
two-axis order key `(L x W)` / `W x H` / `Dia x H` is recognised (ORDER2_RE) and no longer mistaken for a size letter `L`;
`2 x 3 in stock` / `in packs` is not inches (NOT_IN). (3) `./dim_attach.py`: a product entering a second batch or a re-push
would have received a SECOND dimension image — before uploading it now reads the live gallery and skips any product whose
media alt already ends with `– actual size and dimensions`, recording it in `dim/media_existing.json` (kept OUT of
dim/media.json because verify.py reads that file's `position` as an insertion). Fixture-tested: 12 parse cases (comma
decimal labelled + raw, thousands, fits/for → none, fits + own `(L x W)` row → own size, `W x H` / `Dia x H` keys, a real
`Size L` label kept, all earlier 3- and 2-figure cases unchanged, `in stock` / `in packs` → none while `12 x 8 in` and
"… in size" still read); dim_attach mock: product with an existing dimension alt → skipped and listed, product without →
uploaded, reordered to position 2, summary line counts both. `./rules/dimension-image-rule.md` (rule 1, steps) and
`./README-toolkit.md` (step 7b) recomputed. Known and accepted, not scripted: straps / cords / shadows / white-on-white /
multi-item photos distort the cut-out → the photo test fails safe (skip); a source with folded + unfolded triples lists
both as "sizes" in the table (visible in the rule-5 look and the run log).

**Refresh note (2026-09-09, Q18 — US units first on the image; same session):** two lines recomputed after a RULE CHANGE
(user decision: the image always shows the American unit). `./dim_image.py`: `fmt()` now prints inches first with the source
unit in brackets whatever the source wrote (`18.1 in (46 cm)`, `47.2 in (1200 mm)`, an inch source `22.4 in (56.9 cm)`),
the height line too (two rows so it stays inside the canvas), the size table in inches with `(in)` in its headers; new
`inches()` helper (1 decimal, `.0` dropped). Also fixed on the way: the table box was as wide as the product cut-out, so a
narrow product's four columns overflowed it — width now follows the column count. Rendered and looked at: 2-size backpack
(cm source) and 1-size mat (inch source). `./rules/dimension-image-rule.md` ("What is produced") recomputed.

**Refresh note (2026-09-09, Q18 — gallery position back to 3; same session):** three lines recomputed after the user
REVERSED the position-2 decision made earlier today. Reason (raised when asked "what else should we think about"): most
Shopify themes show the 2nd gallery image as the collection-card HOVER image, so at position 2 the size diagram would have
replaced the product's second photo on every collection page. `./dim_attach.py` `POSITION = 3` (docstring rewritten with
the reason), `./rules/dimension-image-rule.md` ("Where it goes" + steps) and `./README-toolkit.md` (steps 7b, 8)
recomputed. Net effect on the store: none — no product was attached at position 2 between the two decisions; the five
STR-DUB-2-batch9 products are at position 3 already and now match the rule (they still carry the earlier cm-first
figures; re-rendering them is a separate decision).

**Refresh note (2026-09-09, Q18 — the drawn image also on the page, under Specifications; same session):** five lines
recomputed after a RULE ADDITION (user decision: "çizildiyse Specifications altına koy"). `./dim_attach.py`: after the
gallery attach (or when the gallery already had the image from an earlier batch) `describe()` reads the media's CDN url,
inserts `<p><img class="vp-dim" src=… alt="<first title block> – actual size chart"></p>` directly after the first `</ul>`
that follows `<h3>Specifications</h3>`, writes final/dNN.json and pushes a productUpdate carrying ONLY descriptionHtml;
idempotent (a description already carrying a vp-dim image is untouched); the outcome is recorded per product in
dim/media.json (`description`) and printed. `./gate.py` (source-image prefix / count check) and `./struct-check.py` (image
count) strip `<img class="vp-dim" …>` before counting; struct-check additionally FAILs a vp-dim image off our CDN or
inserted twice. Both pristine copies were verified against this manifest's hashes BEFORE editing (retyped copies matched
byte for byte), so the edits are the only change. `./verify.py` NOT edited: check 2 (live == final descriptionHtml) and 13
(img list == final's, all on CDN) hold because final is updated before the push; check 16 (alt unique) holds because the
description alt (`– actual size chart`) differs from the gallery alt (`– actual size and dimensions`). Mock-tested: new
product → attached at position 3 + inserted + pushed; product with an existing gallery image → not re-attached, description
inserted + pushed; second run → nothing pushed, one vp-dim image per description; struct-check fixture with 2 source
images + the vp-dim image → no image-count issue; a foreign-CDN or doubled vp-dim image → the two new FAILs.
`./rules/dimension-image-rule.md` ("On the page as well") and `./README-toolkit.md` (step 7b) recomputed. Not run live.

**Refresh note (STR-DUB-2-batch3 Q18 re-run, 2026-09-09 — dim_image.py size-row names):** one line recomputed after a
small CODE FIX (main context, while looking at the built images per rule 5). The size-table row name was taken only from
letter sizes (`XS|S|M|L|XL|XXL|\d+XL`), so a source that writes `Large: 14.96" … / Extra Large: 18.90" …` produced a first
row named `Size` (p17 beach tote). The regex now also accepts the word forms `Extra Small | Small | Medium | Large | Extra
Large` (longest first). Figures, axes and every other rule unchanged. Note: the copy check in this session found the
manifest lines for `./dim_image.py`, `./rules/dimension-image-rule.md` and `./unit_dual.py` STALE (two independent copies
byte-identical, both differing from the manifest — the docs were edited after the last refresh); the two lines this
session did not edit were left as they are for their author to recompute.

**Refresh note (STR-DUB-2-batch2 Q18 re-run, 2026-09-09 — three guards after a wrong image reached the store):** two lines recomputed after a deliberate RULE CHANGE (user decision). The user read the live batch2 p05 dimension image and found the axes swapped: a 195 x 130 x 5 cm camping mattress drawn 195 wide / 130 tall, when the two pillows sit side by side along the 130 cm edge. Rule 1c's photo-ratio test had "confirmed" the wrong assignment at 6 % because the 3/4 camera angle foreshortens the long axis — the first case where the test did not fail safe but selected a wrong assignment inside tolerance. `./dim_image.py` gains three guards, all documented as rule 1f in `./rules/dimension-image-rule.md`: (a) a LIE-FLAT lock — a triple whose smallest figure is under 15 % of its largest (mat, mattress, cushion, strap) is never assigned by photo, labelled axes or skip; (b) PHOTO_TOL tightened 20 % -> 15 % (batch2 p39 passed at 18.75 % with the wrong assignment), PHOTO_GAP unchanged at 30 % so GAP > TOL still holds; (c) a connected-blob isolation test, MAIN_PART = 90 % of the cut-out's pixels in one blob, because 1e(b)'s span/fill guard misses a product photographed with its accessories. MAIN_PART was calibrated on that batch's real cut-outs and the classes separate widely: several objects 65.4 / 74.8 / 81.6 %, one product 99.3 / 100 %. Fixture- and batch-tested: on batch2's 50 products the guards block 8 of the 9 images the eye had rejected (7 not-isolated, 2 flat, and p39 now ambiguous) and leave the correct ones alone; p14 still builds, and the synthetic control cases still pass. Rule 5's eye check now asks its question by name ("is the horizontal line on the product's real long axis?") because two residual risks are deliberately not automated: a TWO-figure flat measurement has no thin third figure to detect, and a cut-out can be one clean blob of the WRONG object (batch2 p28: 99.3 % single blob of the car seat the product sits on).

**Refresh note (STR-DUB-2-batch2 Q18 re-run, 2026-09-09 — three guards after a wrong image reached the store):** two lines recomputed after a deliberate RULE CHANGE (user decision). The user read the live batch2 p05 dimension image and found the axes swapped: a 195 x 130 x 5 cm camping mattress drawn 195 wide / 130 tall, when the two pillows sit side by side along the 130 cm edge. Rule 1c's photo-ratio test had "confirmed" the wrong assignment at 6 % because the 3/4 camera angle foreshortens the long axis — the first case where the test did not fail safe but selected a wrong assignment inside tolerance. `./dim_image.py` gains three guards, all documented as rule 1f in `./rules/dimension-image-rule.md`: (a) a LIE-FLAT lock — a triple whose smallest figure is under 15 % of its largest (mat, mattress, cushion, strap) is never assigned by photo, labelled axes or skip; (b) PHOTO_TOL tightened 20 % -> 15 % (batch2 p39 passed at 18.75 % with the wrong assignment), PHOTO_GAP unchanged at 30 % so GAP > TOL still holds; (c) a connected-blob isolation test, MAIN_PART = 90 % of the cut-out's pixels in one blob, because 1e(b)'s span/fill guard misses a product photographed with its accessories. MAIN_PART was calibrated on that batch's real cut-outs and the classes separate widely: several objects 65.4 / 74.8 / 81.6 %, one product 99.3 / 100 %. Fixture- and batch-tested: on batch2's 50 products the guards block 8 of the 9 images the eye had rejected (7 not-isolated, 2 flat, and p39 now ambiguous) and leave the correct ones alone; p14 still builds, and the synthetic control cases still pass. Rule 5's eye check now asks its question by name ("is the horizontal line on the product's real long axis?") because two residual risks are deliberately not automated: a TWO-figure flat measurement has no thin third figure to detect, and a cut-out can be one clean blob of the WRONG object (batch2 p28: 99.3 % single blob of the car seat the product sits on).

**Refresh note (2026-09-09, cut-out never shaved — rule only, script not yet changed):** one line recomputed after a RULE ADDITION (user instruction, from a live batch3 mushroom-lamp image whose dome and sides were visibly cut off). New rule 1g in `./rules/dimension-image-rule.md`: the cut-out is cropped to the product's TRUE bounding box — every pixel of the mask — never to a density-thresholded box, because a rounded or tapered outline has very few pixels in its outermost rows and columns (a dome shade's apex, a lamp head's flare, an animal figure's ears) and those rows fail the density test and are cut away. It is not cosmetic: the dimension lines are drawn on the crop's edges, so a shaved crop draws the measurement SHORT while the label still reads the source figure. Measured on real batch2 cut-outs, density box vs true box: elephant lamp -12.6 % of the width, camping mattress -3.4 %, inflatable chair -2.2 % of the height, mini washing machine -1.9 %; a mushroom lamp (wide dome, thin stem) is the worst case because the stem rows set the threshold. Speckles are dropped by blob (keep blobs >= 1 % of the mask, rule 1f(c) already guarantees one blob holds >= 90 %), with a small transparent margin so the lines do not sit flush on the outermost pixel. **Implemented in `./dim_image.py` the same day** (the user's first instruction was rule-only, then corrected to "write it wherever it needs to be written"): `cutout()` now takes the bounding box of the mask's significant blobs (>= 1 % each) instead of the `>= 0.06 * frame` density rows/columns, and adds a transparent margin of `max(4 px, 1 % of the longer side)`. Verified on real cut-outs — the elephant lamp's trunk and tail and the owl lamp's ear tufts are no longer clipped, and the box grows 692x725 -> 792x731 before padding. Re-running batch2's build after the change altered exactly one decision, an improvement: p28 moved from a hand-written rule-5 skip to the script's own `axes ambiguous`, because the corrected crop yields a truer ratio. With this and rule 1f the script now blocks all 9 of the images that batch's eye review had rejected, and only the correct p14 still builds.

**Refresh note (2026-09-09 evening, Q18 SCOPE CUT — labelled only, manual only, two live-bug fixes; a 54th line: dim_keep.py):**
five lines recomputed and one added after a deliberate RULE CHANGE (user decision, after asking "is it best to give up the
dimension image?" and answering "vazgeçme, küçült" — keep it, shrink it). Every wrong image of the day (batch9 p49, batch2
p05 / p39 / p03, batch3) had come through the photo-ratio test; no labelled source produced one; the operator's eye was the only
reliable catch. So: (1) `./dim_image.py` — `PHOTO_TEST = False`: an unlabelled triple or pair is skipped as `axes not labelled
in source` BEFORE any photo is downloaded; `resolve_axes()` and the 1f guards stay in the file for a logged, deliberate
re-enable only; the summary line counts `axes not labelled: NN …` and prints a `[WARN] … PHOTO_TEST is on` line if the test
ever runs. New `run_mode()` / `q18_gate()`: both scripts build and attach nothing unless brief_flags.json carries
`"q18_dimension_image": true` AND `"run_mode": "manual"` (a missing key reads as scheduled) — the rule-5 eye check does not
exist in a scheduled run, so the feature must not either. (2) `./dim_attach.py` — REPLACE no longer leaves a dead link:
`insert_in_description()` rewrites an existing vp-dim tag whose src differs (the media was deleted and re-attached), instead of
returning unchanged on the class alone; `describe()` reports "src replaced". Imports `q18_gate` from dim_image. (3) new
`./dim_keep.py` — README step 7, every batch, independent of Q18 and run mode: a product whose live description (products.json)
carried a vp-dim image that the new final lacks (a Q7 rewrite dropped it; gate.py / struct-check.py ignore vp-dim by design)
gets the tag restored under the new Specifications list — only while its media is still in the live gallery, otherwise a
[WARN], never a re-published dead link; one summary line for the run log. (4) `./rules/dimension-image-rule.md` — new "Scope
cut" section; rule 1c marked RETIRED, 1d's unlabelled-pair path marked retired, steps updated (run-mode gate, replace, dim_keep).
(5) `./README-toolkit.md` — step 1 (`run_mode` flag), step 7 (dim_keep first), step 7b (labelled only, retired test). All three
pristine copies were verified against this manifest's hashes BEFORE editing (retyped copies matched byte for byte:
dim_image 3440e415…, dim_attach d63975f4…, rule a5b2cf6d…, README 6c19063e…), so the edits are the only change. Fixture-tested
with a stubbed shopify_api: run_mode scheduled / missing → both scripts print the reason and exit 0 with nothing built;
manual → unlabelled triple `46 x 32 x 16 cm` and unlabelled pair `200 x 150 cm` skipped as not labelled with no photo
downloaded, labelled `L 46 cm x W 32 cm x H 16 cm` reaches the cut-out step; insert_in_description: old src → replaced once,
same src → unchanged, no tag → inserted after the Specifications `</ul>`; dim_keep: dropped tag with live media → restored in
position, tag whose media is gone → [WARN] not restored, no live tag → untouched, second run 0 restored. Not run live.
Live effect expected: fewer products per batch get an image; the five batch9 / batch2 / batch3 images already live are
untouched by this change.

**Refresh note (2026-09-09 evening, description images served resized — `?width=1200` on still images only):** four lines
recomputed after a user decision that followed the Q18 scope cut. Description `<img>` tags are loaded as written — the
theme's `image_url` filter resizes only GALLERY media — so every re-hosted source image and the Q18 PNG (1–2 MB, white
background) shipped at full file size to every phone. New `cdn_sized()` in `./dim_attach.py` (one definition) appends
`?width=1200` (or `&width=1200` after an existing `?v=`) to a src whose file is jpg / jpeg / png / webp; a `.gif` is never
touched (the CDN flattens an animated GIF to one frame under width=), nor is `.svg`; idempotent, an existing width= is kept.
`./rehost.py` step 4 applies it to every still image on our CDN in the extract (the extract is the source of truth for
gate.py's image-prefix check, so the agents' copies carry the same src) and its summary line counts them; `describe()` in
dim_attach.py applies it to the Q18 image's description src (the gallery media is untouched). `./README-toolkit.md` (step 5b)
and `./rules/dimension-image-rule.md` ("On the page as well") recomputed. Pristine `./rehost.py` verified against this
manifest's line (3a7534b5…) before editing. Fixture-tested with a stubbed API and no foreign images: a.jpg → `?width=1200`,
b.png?v=123 → `?v=123&width=1200`, c.gif and d.svg untouched, e.webp?width=800 kept, F.JPEG (upper case) sized; second
run 0 changed. Not run live; products pushed before this date keep their raw srcs (no re-processing).

**Refresh note (2026-09-09 evening, `?width=1200` REVERTED — measured, no benefit):** the note above is superseded; four lines
recomputed back. Applied live to 24 products / 58 still images first and measured with a mobile browser UA: the CDN already
serves WebP for a raw src and every description image was ≤ 1200 px, so the parameter saved 18 KB in total (one image). The
24 live descriptions were restored byte-for-byte from the backup (0 push errors, 0 verify failures — Shopify stores `&` as
`&amp;`, normalised in the check). `./rehost.py` is back at its pristine hash (3a7534b5…), `./dim_attach.py` at its pre-width
hash (18ff02a4…, `cdn_sized` removed), `./README-toolkit.md` at its pre-width hash (7090a3c4…); only
`./rules/dimension-image-rule.md` carries a one-sentence record of the measurement so the idea is not tried again. The
"1–2 MB PNG" premise in the earlier note was wrong — the Q18 PNG reaches a phone as a 32 KB WebP. Page-weight work, if any,
belongs to animated GIFs in supplier descriptions (untouched by decision, a separate task), not to still images.

**Refresh note (2026-09-10, comparison table — mobile + desktop widths):** two lines recomputed after a LAYOUT FIX
(user instruction, from a live phone screenshot of the USB-charger camera page: the two 120 px value columns left ~100 px
for the feature text on a 360 px phone, `Looks and works like a real charger` broke into five lines and the block ran
~1400 px tall). `./compare_build.py`: (a) the product name moved out of the first `<th>` and became the SECOND line of the
navy heading band (13 px, `opacity:.85`), so the header row is one line — `FEATURE` (12 px uppercase) · `Vepine` ·
`Others`; (b) the value columns are percentages, `COL_V` 14 % and `COL_O` 24 %, padding `10px 4px`, replacing the single
`COL` constant; (c) `table-layout:fixed` plus `max-width:none;margin:0` on the table (the theme's own table margin was
leaving a ~35 px gap at the card's right edge); (d) table 14 px, row padding 10 px, Others cells 12 px / 1.25 and
wrappable, with `text-align:center` added to their flex wrapper (new `CENTER_T`) so a second line stays centred; (e) new
constant `MAXW = '680px'` on `div.vp-compare` — percentage columns in a 1470 px theme container gave the feature column
~1300 px and stranded the ticks at the right edge. `clamp()` widths were tried first and are IGNORED by the browser under
`table-layout:fixed` (three equal columns; measured with Playwright) — do not reintroduce them. `parse_block()` now reads
the name from the band's second line and falls back to the old first-`<th>` form, so live blocks from either template
re-render. Checks, insertion point, BLOCK_RE, `strip_block`, `q17()` and the gate wiring are unchanged (struct-check.py,
verify.py and unit_dual.py match on `<div class="vp-compare"` only and were not touched).
`./rules/comparison-table-rule.md` (diagram, header-cells line, new Mobile and Desktop bullets in the format rules)
recomputed in the same turn. Fixture-tested: render → parse_block round-trip exact; an old-template block parses to the
same name + rows; strip_block exact; re-render idempotent; under a hostile stylesheet (`td, th {text-align:right
!important}`) a Chromium measurement gives 186 / 54 / 86 px at a 328 px block and 406 / 103 / 171 px at 680 px, with the
ticks centred and Others phrases on one line at desktop width. NOT done in this session: no live product was re-rendered
or pushed — the live blocks still carry the 120 px template and must be re-rendered from `parse_block()` and verified
(`verify.py`, check 17) before this note is read as "applied live".

**Refresh note (2026-09-10, STORE CHANGE Vepine → Worfa):** seventeen lines recomputed (README-toolkit.md is listed twice
in the block below — both copies updated). User instruction: the store is now **Worfa**, a DIFFERENT Shopify store, not a
rename of the old one. Confirmed through the connector (identity lookup only): Worfa / `worfa.com` /
`ymjviw-rz.myshopify.com` / USD, CDN prefix `cdn.shopify.com/s/files/1/0786/1269/3028/` read off live product media.
Changed: `BRAND` in `./compare_build.py` (also the rendered heading "Why choose Worfa" and the "Worfa vs Others" block),
`./verify.py` and `./gate.py` (the brand scan now fails `worfa` in copy, not `vepine`); the hard-coded CDN prefix in
`./gate.py`, `./struct-check.py`, `./build_check.py`, `./verify.py`, `./extract_html.py`, `./rehost.py` and
`./DESC-SPEC.md`; store name and host throughout `./shopify-api-credentials.md` (rewritten) and `./README-toolkit.md`;
brand name in `./rules/comparison-table-rule.md`, `./rules/dimension-image-rule.md`, `./rules/fit-block-rule.md`
and `./rules/description-format-rule.md` (the "Worfa vs Others" block name in the skeleton); the CDN prefix in
`./usage-efficiency-runbook.md`; and the root transfer guide `00-TASIMA-REHBERI.md` (not hashed here — host, Drive
folder and the same-store/different-store branches).

Three deliberate NON-changes, all user decisions of the same day:
- **The `vp-` CSS hooks stay** (`vp-compare`, `vp-fit`, `vp-dim`, `vp-store`). The Tuzwa→Vepine migration renamed
  `tz-`→`vp-`, but renaming again would make every live block invisible to BLOCK_RE, struct-check.py, verify.py and
  unit_dual.py until it was re-rendered and pushed. The hook is an internal selector, not a brand string.
- **History is not rewritten.** Run logs, `backup-titles-*`, `backup-alt-*`, `kw-cache-*` and
  `claude/store-migration-vepine-2026-09-07.md` still say Vepine, because the backups are restore snapshots of live
  Vepine titles and alt texts — rewriting them would make them restore the wrong thing. Same decision as the Tuzwa
  backups in the previous migration.
- **`vepine.com` is left in one place on purpose**: the colour-provenance sentence in
  `./rules/comparison-table-rule.md`, which records where the navy / light-blue hex values came from.

Three things NOT verified and flagged in the docs, not silently carried over:
- **The store row `30-day easy returns` is the previous store's policy** (user, 2026-09-06), unconfirmed for Worfa.
  compare_build.py's `STORE_ROW` writes it into EVERY comparison block, so an unchecked figure becomes a returns
  promise on every product page. Confirm Worfa's window and change `STORE_ROW` and the rule doc together.
- **Theme colours are still the OLD store's.** `NAVY = #000096` and `LIGHT = #d2def6` were measured on vepine.com
  2026-09-07 and have NOT been re-measured on worfa.com. The rule doc carries a "Colour provenance — STALE" block and
  README-toolkit.md and `./rules/fit-block-rule.md` carry the same caveat. Measure Worfa's Add-to-cart button and header
  band and update `NAVY` / `LIGHT` in compare_build.py AND the rule doc together before the first Worfa push.
- **The script route is unproven on this store.** The client-credentials token call for the new pair was not run (the
  attempt was blocked in this session), `ymjviw-rz.myshopify.com` has never been called from the container, and the CDN
  prefix comes from 3 products / 6 images rather than a full sweep. See the status block in
  `./shopify-api-credentials.md`.

Scripts re-tested after the rename: all toolkit .py files compile; compare_build render → parse_block round-trip exact,
re-render idempotent, rendered block contains "Why choose Worfa", no occurrence of the old brand, and still carries
`class="vp-compare"`.

**Refresh note (2026-09-10, Worfa go-live checks — the four open items closed):** seven lines recomputed after the four
things the store-change note left unverified were actually run against Worfa, not assumed.
1. **Script route works.** `shopify_api.py` `token(force=True)` issued a `shpat_…` from `ymjviw-rz.myshopify.com` (the
   user added the host to the egress allowlist), `{ shop { name myshopifyDomain } }` → Worfa, and the app
   `Claude Backend` reports `read_files, read_products, read_publications, write_files, write_products,
   write_publications` — all three needed writes granted.
2. **CDN prefix confirmed on the full catalogue**, not a spot check: 4,150 products / 35,675 media images, every one on
   `cdn.shopify.com` with the prefix `/s/files/1/0786/1269/3028/` — 0 foreign hosts, 0 off-prefix.
3. **Theme colours re-read for Worfa** from the live MAIN theme "Vault"
   (`gid://shopify/OnlineStoreTheme/174734606372`, `config/settings_data.json`, default `scheme-1`): NAVY is the
   theme's own `buy_button_color` `#2c374d` (the Add-to-cart button), LIGHT is `secondary_bg` `#eef5f7`. Applied in
   `./compare_build.py`, `./fit_build.py` and `./dim_image.py` (the last as RGB tuples (44,55,77) / (238,245,247)).
   Taken from the theme's declared settings rather than sampled off a rendered page. Contrast: white on navy 11.9:1,
   navy on light 10.8:1. The previous store's `#000096` / `#d2def6` are retired.
4. **Store row confirmed by the user**: Worfa's return window is also 30 days, so `STORE_ROW` is unchanged — the
   UNCONFIRMED comment in `./compare_build.py` and the matching block in `./rules/comparison-table-rule.md` were
   replaced with the confirmation and a standing instruction to re-confirm it whenever the store or policy changes.
Also fetched, not hashed here because it is run data rather than a toolkit file: `collections.json`, 24 Worfa
collections as `{title: gid}` — the shape DESC-SPEC and verify.py expect. `./shopify-api-credentials.md` and
`./README-toolkit.md` recomputed with the verified status. Block re-run after this refresh: 55 of 55 OK.

**Refresh note (DDL2-Batch1, 2026-09-10 — CTA metafield theme is Worfa/Vault, block confirmed live):** one line recomputed after a
DOC CORRECTION, not a copy problem. `./rules/cta-benefits-metafield.md` still named the PREVIOUS store's theme in its "Teknik"
section — Xtra || FIXED (`gid://shopify/OnlineStoreTheme/204864586014`), block id `custom_liquid_apEFqN`) — which the
2026-09-10 Vepine→Worfa store change left stale; the DDL2-Batch1 run log flagged it as an open item because a metafield that
no theme block reads renders nothing and fails silently. The user confirmed they had already pasted the Custom Liquid block
into Worfa's main theme **Vault** (`gid://shopify/OnlineStoreTheme/174734606372`) and that the benefits render on the live
product page. The doc's Teknik section now names Vault as the current theme, records the user confirmation and the standing
fact that the block does NOT travel with a store change (it is pasted into the new theme by hand), and keeps the old theme id
in a separate line marked "yalnızca kayıt için". A DDL2-Batch1 line was also added to "Uygulama durumu" (50/50 metafields
verified, rendering confirmed). No gate, rule or threshold changed.

**Refresh note (2026-09-11, kw_measure.py word-order guard — a 56th line: rules/kw-order-variant-rule.md):** three lines
recomputed and one added after a deliberate RULE CHANGE (user decision, from DDL2-batch1 p00, product 11212354748452: the
title dropped `noise cancelling headphones` 165,000 — the old title's own opener — as "low volume"). Reproduced: Google Ads
folds keywords that are the same words in a different order into ONE close variant when they arrive in the SAME request and
reports the low variant's volume for both — `noise cancelling headphones` returns 165,000 alone and 2,400 next to `headphones
noise cancelling`; measured alone the two orders are different keywords (`vintage table lamp` 3,600 vs `lamp table vintage`
2,900). The pair is routine here: source_windows.py emits the supplier title's order, the extraction agents give the natural
order. `./kw_measure.py`: the todo list is bucketed by sorted word bag (`bag()`) and the members of one bag are spread over
separate ROUNDS (`rounds_of()` — round 0 = first member of every bag, round 1 = second, …); each round is chunked and called
on its own, and an assert guarantees no two variants share a request. Both variants are still measured with their own volume;
the title step picks the higher one — "dedupe to one variant" was rejected because the reversed form can be the lower one.
Cost: one extra call (~$0.09) per round beyond the first. New stderr lines for the run log: `… in N call(s) over R round(s) —
V word-order variant(s) moved to later rounds` and one `[order variant, own call]` line per moved keyword. Tested with a
stubbed source_windows on 6 keywords (two 2-member bags, one 3-member bag): 3 calls over 3 rounds, 3 variants named, no bag
repeated inside a round. `./rules/kw-order-variant-rule.md` (project path `claude/kw-order-variant-rule.md` — the tool cannot
write to the root) is the rule doc and carries the open question (plural / singular folding, not reproduced) and the audit
recipe for kw-caches produced before this date (bucket by sorted word bag, re-measure every 2+ bag in separate calls).
`./README-toolkit.md` step 4 recomputed (word-order guard paragraph after the ≤950-per-call sentence; both README lines
below updated). The pristine README copy was verified against this manifest's line (06e71b25…) byte for byte before the
edit, so the paragraph is the only change. Not yet run on a live batch — the first batch after this date copies the round
line into the run log.

**Refresh note (2026-09-11, US units only in the budgeted elements):** six lines recomputed after a deliberate RULE CHANGE
(user decision — the live ddl2 pregnancy pillow's comparison table read `155 x 75 x 60 cm`; the store sells only in the USA
and the copy is written for a US shopper, so a metric figure never stands alone on the page). Until now the dual-unit pass
deliberately skipped the budgeted elements (H2, benefit bullets, comparison / fit blocks, FAQ questions) because a
"(155 cm)" parenthesis would break a limit — so whatever unit the agent wrote there reached the store as written.
`./unit_dual.py`: new `imperial_only()` — metric → imperial with the metric figure DROPPED (`155 x 75 x 60 cm` → `61 x 29.5 x
23.6 in`, `61 in (155 cm)` → `61 in`, `5.98in/15.2cm` → `5.98in`, `40°C` → `104°F`; imperial text unchanged; the dual pass's
exemptions — 4G/5G, "L" as a length label, waterproof mm ratings, liquid oz — reused through a shared `_skip()`); `process()`
now applies it to the H2 + first `<ul>` (bullets) and to FAQ QUESTIONS, keeps the dual pass everywhere it ran before, and
returns a third count (`… N budgeted element(s) made imperial-only` on the per-product line). `./compare_build.py`: `render()`
passes name, feature rows and non-✘ Others cells through `imperial_only()` (lazy import — unit_dual imports this module's
BLOCK_RE); the 20–60 length check runs on the converted row, the traceability and number-in-source checks on the agent's own
text, so a source-metric row still passes. `./fit_build.py`: the same for the four lines (30–110 measured after conversion;
proof / source / number checks on the agent's text). `./rules/comparison-table-rule.md` (content rule 8, format-rules bullet,
"Where it runs" — including how a live metric block is fixed by `parse_block()` → `render()` + a descriptionHtml-only push),
`./rules/fit-block-rule.md` (content rule 7) and `./rules/description-format-rule.md` (§5 dual-units paragraph: the "NOT
converted" sentence replaced — budgeted elements are imperial-only; CTA lines, alt texts and SEO fields stay untouched by
script and are written in US units by the agent). Fixture-tested: the twelve conversions above plus `Waterproof rating 3000mm`,
`Supports 5G`, `32 oz water bottle` and an already-imperial dimension run all unchanged; every result idempotent; a fixture
description → H2 and bullet imperial-only, prose and Specifications dual (`61 x 29.5 x 23.6 in (155 x 75 x 60 cm)`), FAQ
question imperial-only and its answer dual; compare render → `parse_block()` round-trip returns the converted row; fit render
carries no metric figure. gate.py, struct-check.py, verify.py and value_check.py were NOT edited (gate calls unit_dual as a
subprocess and reads only its last line; a metric figure that lived ONLY in a bullet now fails value_check and must also get its
Specifications line — the intended outcome). Not run on a live batch yet; products pushed before this date keep their metric
rows until re-rendered.

**Refresh note (2026-09-11, a 57th line — list_bold.py: bold lead-ins + gap under image 2):** `./list_bold.py` added and
three lines recomputed after a user instruction from the live ddl2 pregnancy pillow. (1) Key Features items reached the store
as plain `U-Shape Support: Back, hips, legs …` although §4 / §5 of the format rule have asked for `<li><strong>Name:</strong>
text</li>` since 2026-09-07 — no script enforced it. list_bold.py (gate.py, right after fit-build, before the finals are loaded
for the other checks; zero tokens, idempotent) wraps a plain leading `Name:` (1–7 words) in `<strong>` in the Key Features and
Specifications lists and normalises `<strong>Name</strong>:` / `<strong>Name: </strong>` to the canonical form; an item with no
`Name:` lead is reported, never invented. `./struct-check.py` now FAILs a Key Features / Specifications item without a bold
`Name:` lead. (2) The second description image (between Key Features and Specifications; the vp-dim image not counted) sat flush
on the Specifications heading: list_bold.py appends `display:block;margin-bottom:24px` to that `<img>`'s style (other attributes
untouched, src unchanged — gate.py / verify.py compare srcs only); struct-check.py FAILs a second image without `margin-bottom`.
`./rules/description-format-rule.md` §4 (markup + enforcement sentence) and the skeleton's image-2 line recomputed. Fixture-tested:
three plain / malformed lead-ins bolded, an already-canonical item untouched, a no-colon item reported, a spec line bolded, the
gap added once to image 2 (existing `style="width:100%"` extended), second run changes nothing; `<img …/>` self-closing form
handled. Not run on a live batch; products pushed before this date are unchanged until re-processed.

**Refresh note (DDL2-Batch4, 2026-09-12 — proxy backoff in both API scripts):** two lines recomputed (user approval
2026-09-12). `./shopify_api.py`: `gql()` now retries an empty / non-JSON response after 10, 30, 60 s (retries 3 → 6) — the
sandbox egress proxy intermittently answered CONNECT with 403 for ~20 s on 2026-09-11 (seen on the Shopify host three
times in a row, recovered 20 s later); the token call and the HTTP/GraphQL error handling are unchanged. `./kw_measure.py`:
the line was STALE, not a corrupted copy — the project doc gained its "Proxy backoff" paragraph (`TUNNEL_BACKOFF`, transport
errors retried after 5/10/20/40 s) at 18:36 UTC on 2026-09-11, after this manifest's 11:55 refresh; two independent copies
agreed byte for byte. DDL2-Batch4 ran to `verify: 50 products, 901 checks, 0 failures` on these two files.

**Refresh note (DDL2-Batch3, 2026-09-12 — unit_dual.py: engine litres and dual temperature ranges):** two lines recomputed after a CODE FIX (user approval "tamam yaz"). On p17 (jump starter) the script had turned engine displacement into liquid volume (`engines up to 10.0 L` → `338.1 fl oz (10.0 L)`) and converted a range the source already wrote in both scales piecewise (`-20°F to 70°F / -29°C to 21°C` → `-20°F (-29°C) to 70°F / -29°C to 70°F (21°C)`); both reached the final and were hand-fixed before the push. `./unit_dual.py`: new `ENGINE` regex in `_skip()` — an l/ml figure whose 40 chars before or 25 after name an engine / displacement / cylinder / diesel / gasoline / petrol / motor is left as written (dual and imperial_only); new `has_both_temp()` — a text that already carries both °C and °F is never temperature-converted again in `dual()` or `imperial_only()`; new `DROP_SLASH_T` — imperial_only drops the `/ …°C` half of such a range (`-20°F to 70°F / -29°C to 21°C` → `-20°F to 70°F`). Fixture-tested (11 cases incl. `Tank: 250ml`, `86°F to 122°F`, `40°C`, `3000mm` rating, `5G`, `32 oz water bottle` unchanged in behaviour; every result idempotent); gate.py re-run over the 50 DDL2-Batch3 finals: CLEAN and all 50 files byte-identical. `./rules/description-format-rule.md` §5 gained the two-sentence rule. Note: this manifest's list carries `./README-toolkit.md` twice; both lines are unchanged.

**Refresh note (2026-09-15, egress note was stale — `tuzwa.com` is reachable again):** two lines recomputed
(`./README-toolkit.md`, listed twice in the block below — both updated — and `./shopify-api-credentials.md`) after a
DOC CORRECTION, not a copy problem and not a rule change. Both docs stated that `tuzwa.com` is refused by the
container's egress proxy with **403 CONNECT**, measured 2026-09-12. Re-measured 2026-09-15 from the container:
`https://tuzwa.com/` returns **200** on three consecutive requests and `https://www.tuzwa.com/` 301s to it — the
allowlist changed at some point between those dates. The note is now written as a dated pair of measurements with
the instruction to re-measure per session rather than quote either line as current.
**Why it mattered:** the blr-batch29 run log (2026-09-14) quoted the 403 sentence as if that run had measured it,
which it had not — a documented claim was reported as an observation. The run log has been corrected too.
**What did NOT change:** theme reads still go through the Shopify connector. The binding reason is that the script
route's custom app has **no `read_themes` scope**; the storefront host was only ever a second reason and both docs
now say so. Fetch, push and verification stay on the script route. One capability does open up: a storefront page
can now be fetched for a rendered-output check — but DRAFT products still 404 there, so only Active products can be
checked that way.
No script, gate, threshold or rule was touched; both docs were verified against their pre-edit manifest hashes
(`6f08a612…`, `04b2a400…`) before editing, so the corrected sentences are the only change.

**Refresh note (2026-09-15, same turn — unit_dual.py: count × value, axis labels, bag flag per description):** one line
recomputed after a second CODE FIX (user decision "TAMAM DÜZELT" on the two pre-existing quirks named in the note below,
plus one gap found while testing). `./unit_dual.py`: (1) `Pack of 2 x 500 ml` — a run of two numbers joined by x with a
MASS / VOLUME unit is a count times a value, never a two-axis dimension (only length units form dimension runs):
`split_count()` keeps the `2 x ` prefix verbatim and converts the value → `2 x 16.9 fl oz (2 x 500 ml)`; a range
(`5-7 oz`) and a length run (`28.8 x 27.8 cm`) convert as before. (2) an axis LABEL right after the unit (`9.45 in L x 7
in W`, `12 cm H`) is now part of the match (`LABEL` group in MEAS) so the conversion lands after it — `9.45 in L (24 cm)`,
not `9.45 in (24 cm) L`; DROP_PAREN keeps the label; `10 in L-shaped` is not a label. (3) `BAG_PRODUCT`: process() decides
once per description, from the H2 + benefit bullets, whether the product is a bag; on a bag page every LITRE figure stays
as written — this covers a spec row like `Volume: 3.5 liters` that names no bag word itself, which the BAG-context test
alone had missed in the fixture. ml figures on a bag page are still liquids (`2 x 500 ml bottle pair` → fl oz). Known and
accepted: a `1 L` bottle mentioned on a bag page stays in litres. Fixture-tested: 25 dual / imperial_only cases (the
batch32 four, the two quirks, `Set of 3 x 150 g`, `12 cm H`, and every earlier exemption) 0 FAIL, every result idempotent
and `imperial_only(dual(x)) == imperial_only(x)`; process() on a bag fixture and a water-bottle fixture gives the
expected output and is idempotent; the flag is reset after process() (a bare `dual("Volume: 3.5 liters")` still converts).
Not run on a live batch yet.

**Refresh note (blr-batch32, 2026-09-15 — unit_dual.py: word units and bag litres):** two lines recomputed after a CODE FIX
(user decision "TAMAM YAP", from the blr-batch32 run log's two open items). `./unit_dual.py`: (1) a unit written as a WORD
was never matched — `800 meters` stayed metric-only on p27 while `800m` on the same product was converted, likewise
`5000 meters` (p06) and `800-5500 meters` (p16); UNIT_RE now lists `meter(s)/metre(s)` and `liter(s)/litre(s)` FIRST and
`WORD_UNIT` maps them to the short key, MET_RUN and has_both() carry the same word forms so imperial_only drops the
parenthesis and SWAP reorders them. (2) a bag's litres were read as a liquid — `50L backpack` reached the final as `1690.7
fl oz backpack` (p08 FAQ), `3.5L main compartment` as `118.3 fl oz` (p07), 8 places hand-fixed before the push; new `BAG`
regex (backpack / rucksack / daypack / bag / compartment / luggage / suitcase / duffel / tote / pannier / pouch / sack)
applied in `_skip()` exactly like ENGINE — item name, 40 chars before, 25 after. "capacity" and "pack" alone are
deliberately NOT bag words (a bottle's `capacity: 1 L` and a `pack of 2 x 500 ml` are liquids).
`./rules/description-format-rule.md` §5 gained the two-sentence rule. Fixture-tested (20 cases): the four batch32 cases
now `2624.7 ft (800 meters)`, `16404.2 ft (5000 meters)`, `2624.7-18044.6 ft (800-5500 meters)`, `50L backpack` /
`3.5L main compartment` unchanged; `1 L water bottle`, `Tank: 250ml`, engine litres, 4G, `in L` label, 3000mm rating,
145 g, cm triple, °F range and `15.2cm/5.98in` all behave as before; every result idempotent in dual() and
imperial_only(). Two PRE-EXISTING quirks were seen on the pristine copy and are NOT fixed here (out of scope, no rule
decision): `Pack of 2 x 500 ml` is read as a dimension run (`0.1 x 16.9 fl oz`), and `9.45 in L x 7 in W` gets `(24 cm)`
inserted before the L label in dual(). The toolkit now lives in the GitHub repo (toolkit/00-SESSION-START.md); both
files and MANIFEST.sha256 were sent to the user for upload in the same turn.

**Refresh note (blr-batch28, 2026-09-14):** three lines were STALE on this session's copy, not corrupted copies — `./TITLE-SPEC.md`, `./title-check.py` and `./rules/title-format-rule.md`. For each, two independent copy agents produced byte-identical files that both disagreed with the manifest, so per §6 the manifest lines were stale: the three project docs were edited after the previous refresh. All three were recomputed from the verified copies that passed the run. One GENUINE copy corruption was also caught and fixed by re-copy in the same session: `./dim_keep.py` (first copy `dd0f6ac89cf620f7185702d55a249abd76b450364acecbb5754b000bd447291a`, second independent copy matched this manifest's `2e8bd086…` exactly), so that line is unchanged. After the fix the block passed 56 of 56.

**Refresh note (2026-09-21 — health-claim rule rewritten, RULE CHANGE at the user's decision):** seven lines recomputed.
The Safety Notes medical/health paragraph no longer forbids physiological-outcome wording: a health benefit the SOURCE itself
states is KEPT, not softened or removed (relieves back and hip pain, reduces acid reflux, improves breathing, deep restful
sleep, incl. "instantly" / "all night"); none is invented; still forbidden are disease-treatment claims (heals / treats /
cures / prevents a named condition) and "clinically proven" / "doctor recommended" / "FDA approved" unless source-stated;
the source's own disclaimer sentence is still kept. The user edited the project description field first; then every doc
that repeated the old "soften/remove" wording was aligned in the same turn so agents do not follow a stale sentence:
`./rules/PROJECT-DESCRIPTION.md` (paragraph replaced), `./rules/description-format-rule.md` (2 places),
`./rules/comparison-table-rule.md` (rule 7), `./rules/cta-benefits-metafield.md`, `./DESC-SPEC.md` (insoles/denture line),
`./README-toolkit.md` (step 6b) and `./fact_cover.py` (docstring comment only — no code change, py_compile OK). No step,
script or gate was added. The by-eye "forbidden claim family" sweep recorded in earlier run logs follows the new list from
now on. All seven files and MANIFEST.sha256 were sent to the user for GitHub upload in the same turn.

**Refresh note (blr-batch44 follow-up, 2026-09-21 — unit_dual.py sub-unit rounding, novel_words.py null fields):** two lines
recomputed after a CODE FIX (user decision "düzelt bana ver", from the blr-batch44 run log's two open items). `./unit_dual.py`:
`fmt()` rounded every non-integer conversion to 1 decimal, so a sub-unit value became 0 — p04's "0.5 to 8mm" reached the final
as "0 to 0.3 in" in 7 places (bullet, prose, Key Features, Specifications, FAQ, compare row, fit line) and was hand-fixed. Now
values ≥ 1 keep 1 decimal (unchanged), values 0.1–1 keep 2 decimals (0.47 in, 0.31 in), values under 0.1 keep 2 significant
digits (0.02 in, 0.0039 in), and an integer unit (g, ml, °C, °F) that would round a non-zero value to 0 uses the same decimal
rule. Fixture-tested: `0.5 to 8mm` → `0.02 to 0.31 in` (imperial_only) and `0.02 to 0.31 in (0.5 to 8mm)` (dual); `12mm` →
`0.47 in`; `22 x 7 x 4.5 cm` → `8.7 x 2.8 x 1.8 in`; `100 g` → `3.5 oz`; `149°F`, `24.5 cm`, `0` unchanged. gate.py re-run over
the 50 blr-batch44 finals on a copy: CLEAN, `unit-dual: 0 item(s) converted` (idempotent on already-dual text); the only
content difference is p15's re-rendered compare row / fit line (`12mm` → `0.47 in` instead of `0.5 in`) — live copies are
not re-pushed. `./novel_words.py`: the source join crashed with TypeError when old_seo_title / old_seo_description /
productType / identity / a variant title was null (blr-batch40 and blr-batch44 ran it from a patched scratch copy); each
field is now `or ''`. Tested on all 50 blr-batch44 products: 50 lines, no crash. Both files and MANIFEST.sha256 were sent to
the user for GitHub upload in the same turn.

**Refresh note (2026-09-21 — two new lines: fix_sections.py, spec_parse.py; README step 3f):** `./fix_sections.py` and
`./spec_parse.py` added at the user's decision, and `./README-toolkit.md` recomputed (new step 3f; both of its lines below
updated). Both scripts were written in ddl2-batch28 as session code and uploaded to the GitHub repo by the user
(`tk-repo/toolkit/`); their hashes are of those uploaded files, byte-identical to the copies the user attached.
`./spec_parse.py` splits a supplier's run-on one-sentence spec table into `extract.specs` rows by a label lexicon (only
products with EMPTY specs; unknown labels left alone; `[BLEED]` mark when a value still holds a colon).
`./fix_sections.py` applies three sections.py reclassifications as code — "Why You'll Love It" → back into `key_features`,
a spec-name pseudo-section → dropped, a two-clause comma headline over prose → dismissed as the lead — the misdetection
families the DDL2-Batch1 and blr-batch32 run logs describe. Fixture-tested in this session (2 products): run-on line → 5
correct rows incl. `Lamp Shade Material` and `Wall Light Type` (longest label wins); WYLI lines restored with bullet marks
stripped, spec row and lead dismissed, a real `Care` section kept, junk heading removed from key_features; `--dry` writes
nothing; second run changes nothing. NOT verified here: their behaviour on a live batch other than ddl2-batch28 — the
`LABELS` lexicon comes from a lighting / home-decor supplier, so the first batch from another supplier reads the `--dry`
output in full. `sections.py`, `gate.py` and every other script are unchanged; no rule or threshold changed.

```
80f57a0214941faafc9fda7998ee3d5b3cbaa83e2d137fd7df19eb0a28d867c4  ./DESC-SPEC.md
06007e07544be11e3be8b5194c17546c240543f24630b0da687d761c9447aeaa  ./EXTRACT-SPEC.md
d6750b9414b575b0c708c9157d95e90332a5e7565b5110574bf3d352a872ffdf  ./README-toolkit.md
a6f42ca0217bcbbaf74603ac81ee0e35192285c99bcb1f575dee0d89299fa57d  ./TITLE-SPEC.md
6983acd8ac97c6b7221df3f2c8c2b7dd5f23e986f04808c0de5cda517b9e7c34  ./build_check.py
18af4fa1108f5c83e8773ec4d1a27cf8fc2bdfa77ce14e11f979e44055cf15e7  ./cap.py
f68add61a780c188c1811b927cd6e3bc03973a629034276ab089b70c5ffacad4  ./age_check.py
3ba66e25cdf8c1d3f116548e00197b2553a3e1907e4e2e7e8a95c97dd2585b5c  ./assume_check.py
263197d3a05fbb8286e4846f957e14e493b510c90793fff4b33cf179379d103a  ./claims_check.py
b0757ad4fb2b1dd0ca20d03c64aeff9dc878467fe2397235c1f385fef76794bc  ./cta_check.py
96a8718c232e6e2b645c142c0392ea7ee0867269a43ffefb2e3f0744be3c34be  ./desc-check.py
08205597a172d72ad2d3ec2125dafbbedaeba5bee7ce5acdf1bfa822c6d89906  ./extract_html.py
f869bd34e0e4fc64dcb9a92945814d41fd26eb59fbfebb31df51ceb258ab9f4b  ./fact_cover.py
cde1242bc9ef0068eab3e0dc6eb3448da487a390c8ef85c75000c438408f3746  ./factcheck_prompt.md
c16bb6c3266378460c635193a728086a629e0c9463d8477900f1365fd07f1da0  ./gate.py
b172ebe12906d7f84182c11605cec312000d2847718cf93c40cc58a7e622fdba  ./head_check.py
f26bc457b2badc5d47f31c6f53909f1a6be6026d7b6c2485261ceb01dcef84d9  ./novel_words.py
e707095eb797499bba92ca2c7dfe4874f772ea6217bf9cb82b1c2af10cf5a23b  ./ov.py
fb0cfc0f8e09966954dc3100ff4e9862b6ac5096c477e42cace3857c19ffb9b2  ./rules/cta-benefits-metafield.md
1da499cd8e7023e4e8e9682a3182206a2fd360ad64bb5203d9054d9f3b5c4c09  ./rules/dataforseo-credentials.md
c9c31e72d1a2a7fe982755c1bb691b067206e2fc73e0c03b944b8c11682ef39a  ./rules/description-format-rule.md
1009ea65ea1015faa372ae468977c555b4c986c18e1573c291e295de177bfc4f  ./rules/image-alt-text-rule.md
77ea823f6befff40870ea417021c5ffd602525ed841c891688799bc6a31268bb  ./rules/PROJECT-DESCRIPTION.md
20f2560a880ecc6a627411a27ab77df075ea6f444ae6890fa1e6b76f459e08e2  ./rules/rule-overlap-deferred.md
bf17d6483fd57d9d6ad75349fd221d86b5412d634d18a2e8d9f49ce06eab39f2  ./rules/title-format-rule.md
57c8dfd0dc944c0f2295e8ef7f10f856fd2fe11ad6c87a2f0e341ed3a5491c71  ./source_windows.py
568215e8999a7f380787eb4ba5838628d259ba0ce01a8b183e37d38b8e40d15e  ./spec_cover.py
bd45213794d0a9a9cc351090160ca9dbdb56d3ff487d85e99e6d6813a821b138  ./shopify-api-credentials.md
af2b8db768589f4fff745c31b0e3600a6cd2ac0957adcfef23c8e9b7b28709d5  ./shopify_api.py
a23240ba5083350b4e5583c975d9ef018177467fe55788d720bae66f6a5e7129  ./struct-check.py
98908696a60cf09023072e92218f43985a995b88c323f67433e9bfcc250d1068  ./title-check.py
f29bf7b35e9abf4ee77519cb0d83a3bc41f8c53d8d6be897579c0cc32a50c3e1  ./usage-efficiency-runbook.md
420431d7b50507a524c1140eb0bcdd7ad6e04c6290246d99a0b5dd767db12205  ./value_check.py
713e4becb5cb847ab4447e388614f2ddfdc0d34f7e15d684b02ae6f02d9abfa3  ./verify.py
c5cf7018f2be9b007a57e3cc41e4d4aeec35374717b28c0dc7738d8a298e32fb  ./rehost.py
5c4da57651a772232d32a7557a01c001c96302f90d87aa1c795ae9581c40ddda  ./compare_build.py
f7a5d4b74973e5ce54e4d44eb95477841b18f31f6c9881d4d03df922ffe199e3  ./rules/comparison-table-rule.md
2b76b44b688b8c298808b57dbd788ddfa55da4e2101ac6ca059991681bb9dd3e  ./dim_image.py
18ff02a467edfa90758d943af8851d5878bc4609c7550cb6687a222f44b8bace  ./dim_attach.py
2e8bd0864f237bfba8ea0fb0c0b804cfe30fc2a24623c9daca3de7b03e512da0  ./dim_keep.py
596e015497d539affa5602f796b79859a8d4d539052d98daf17216d2b699ed09  ./rules/dimension-image-rule.md
01e1b599cb4738413684cd0f5ac2af6a72719ab513c1ccc79a0fea94b9acca1b  ./fit_build.py
1b7441a5fb9b44069b651629173a6b4735d75e158771562c98ae4dd79ebd6d85  ./rules/fit-block-rule.md
1d5a90d740c28cd881d617ce9b89a0a5b3efbc6d7e9525389c50ef433ddc5b7d  ./CTA-REVIEW-SPEC.md
e15cebe0fde55247966cb6eab106660a3c0c44a0eb6db2f40151b6e9bde079d8  ./keyfeat_cover.py
1dcfa78dfca197ac890f555ea29d4d441d526eb946356260772b604e1e4fe271  ./unit_dual.py
e08c21d0b6fe0951e3c929318b2e2d7a757a4ed724d48bcc6369fb1fd047baff  ./para_feat.py
87b17ae7b1e631dee6996441a52bfa46a66cc7961fe9f7a35777ebd18f1af356  ./extract_check.py
e4c4050841aeea9b3b8180386f3bdc2eef070b8936c6a240d766bcd58bd08875  ./KF-REVIEW-SPEC.md
ca3d7b1753cfc850588e7f746886fb6bc161bf6c65f488553b017dc3d6be70b3  ./kf_review_input.py
91abc9b4f3a73b1b70372a91e965ee14be01feee93892ee2443ce9ffa3e2aaac  ./howto_check.py
02b0d2e9de323b1167d42c637d13ff244a3e0833667087cbee2dbb3b1a0d80d9  ./usage_tips.py
9537576f5d9b334a0f8c36afa5691f2aae93a343bc5dc005c33960c1422df545  ./sections.py
3338fb4510aa32b831bddfd602f5acb3f1e469d341d55a6757f5ad20605a5399  ./kw_measure.py
d6750b9414b575b0c708c9157d95e90332a5e7565b5110574bf3d352a872ffdf  ./README-toolkit.md
ecf9731e745ef965f65733a7c7cf530046dc25bea32681c40c6bc05a87e67ea2  ./rules/kw-order-variant-rule.md
7c86386a6f77ab101bd60957e78df39449751dce01cf61c7f0eb6da2ffad4d74  ./list_bold.py
b3b64dd58e7faff215653dd17d1d7cd74d1ccd9e4ae76c2580c273a5273fbb51  ./fix_sections.py
3b8daef9a896547894840edc1503d009e2f553fc9eebae2140f14ee1d01003f9  ./spec_parse.py
```
