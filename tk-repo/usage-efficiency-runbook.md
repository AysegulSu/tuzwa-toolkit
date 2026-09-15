# Usage Efficiency Runbook — 50-product batch (titles + descriptions)

Added 2026-09-02. **Rewritten 2026-09-02 after ddl1-batch6, the first batch whose usage was
actually measured.** Purpose: cut token usage per 50-product batch **without removing, weakening
or skipping a single rule.** Every rule in the Backend Update Document, `title-format-rule.md` and
`description-format-rule.md` applies in full. This runbook changes only HOW the work is organised;
it never changes WHAT is checked or written.

**Non-negotiable guarantee:** if any efficiency step below would require skipping a rule, a gate,
or a check, the efficiency step is dropped and the rule wins. Efficiency is never a reason to push
unverified content.

---

## 1. The measured baseline — ddl1-batch6

The first version of this runbook promised "roughly half the previous per-batch usage" against a
baseline nobody had ever measured. That promise was unverifiable. It is replaced by a real number.

**ddl1-batch6 (50 products, one push, no compaction): 766 model turns, 24.4M effective tokens.**
Wall clock 4 h 15 min.

Effective tokens weight cache reads at 0.1×, cache writes at 2×, and output at 5× a plain input
token. Raw was 107.8M, but 100.8M of that was cache reads — the raw number is meaningless on its
own and must never be quoted as the cost.

| Where it went | Effective | Share |
|---|---|---|
| Cache **writes** — new material entering a context | 13.4M | **55%** |
| Cache **reads** — re-reading accumulated context every turn | 10.1M | **41%** |
| Output — every title, description, script and reply written | 0.95M | 4% |

**The finding that changes this document: 96% of the cost is carrying context, not producing
work.** The whole batch's written output — 50 titles, 50 descriptions, every script and every
reply — is 4%.

Cost is therefore driven by **turn count × average context size**, and batch6 averaged 131k
context per turn across 766 turns.

### Turns by phase (batch6)

| Phase | Turns | Note |
|---|---|---|
| Keyword measurement (browser route) | **223** | 29% of the whole batch — now eliminated, see §3 |
| Descriptions (5 agents, two rounds) | 174 | the second round was avoidable, see §4 |
| Main context (titles, rulings, coordination) | 108 | |
| Product extraction (5 agents) | 77 | |
| Candidate keywords (5 agents) | 65 | |
| Push + verification | 31 | over-verified, see §5 |
| Categories, collections, images, checks | 88 | |

### What the previous runbook got right, and what it missed

Right, and measurable: **one push instead of two or three** (a push+verify cycle costs ~1.8M
effective, so batch3's five pushes were catastrophic), **no compaction**, and **research results
kept in files** rather than in context. Together roughly 15% of a batch — real, keep all of it.

Missed: the previous version was written entirely about *which data goes where* and never once
mentions **turn count**, which is the actual multiplier. A subagent that takes 78 turns to do a
mechanical job costs more than the data it was created to keep out of the main context.

**The metric to optimise is turns, not files.** Before adding any step, ask how many round-trips
it costs, not only how much data it moves.

---

## 2. The rules that make one push sufficient

All defects that forced re-pushes in batches 1–5 are now written rules with mechanical gates.
Before the Phase 2 push, ALL of the following must pass on the final payload — none may be skipped:

- `title-check.py` — 0 FAIL; catalog 8.1 (first 40 chars unique) and 8.2 (<60% overlap)
  clean; **rule-1 warnings zero**; `rejects.json` emitted BEFORE any description is written.
- `desc-check.py` — 0 hits (internal-note / sourcing language, three banned Specifications
  forms, alias lists, semantic negation sweep) on title, descriptionHtml, seo.title, seo.description.
- Structure check: one `<h2>`, sections `<h3>`, 5 benefit bullets, prose 65–110 words, whole
  description 350–430 words, `Package Includes:` casing, exactly 5 FAQs in
  `<p><strong>Q:</strong><br>A:</p>` form, `margin-bottom: 0` / `margin-top: 0` pairing, no empty
  elements.
- Image check: every `<img src>` on `cdn.shopify.com/s/files/1/0806/1645/6416/`, count and position
  identical to the source; dead or unusable source images replaced with a gallery image.
- Limits: seo.title < 70, seo.description < 160, title 70–120 (tiers per §4 of the title rule,
  145 ceiling).
- Second net: every `rejects.json` keyword ≥ 1,000 present in its description or rejected with a
  written reason; fit-rejected keywords absent from title AND description.
- Safety disclaimers present where the Backend document requires them.
- `backup-titles-<batch>.md` written BEFORE the push.

Only when every gate is green is the batch pushed — once.

---

## 3. Keyword research — the browser route is retired

`api.dataforseo.com` was added to the organisation's egress allowlist on 2026-09-02 and the cloud
container now calls it directly (verified: HTTP 200). **Call the API from `Bash`.** Roughly 6 live
calls of ≤950 keywords cover a 50-product batch at about $0.06 per call.

This removes 223 turns — 29% of batch6 — and every one of the ~240 permission prompts the browser
route generated. It is also what makes an unattended scheduled run possible at all: the browser
route required the user's computer to be awake and a human to approve each call.

Keep the browser route documented only as a fallback if the allowlist is ever withdrawn. If it is
needed: `execute_javascript` returns the value of a **synchronous** last statement only — start the
fetch in one call writing to `window.__out`, read `window.__out` back synchronously in the next;
an `async` IIFE returns a Promise and yields nothing. Always pass `tab_id` explicitly.

Unchanged in substance: **every candidate is measured, nothing is rejected unmeasured**, the full
result set is written straight to a file, the cache is written to `kw-cache-<batch>.md`, and
only the per-product top 30–40 rows (plus every row passing the tail gates) come back into context.
The checker and the title builder read the FULL file.

---

## 4. Organisation of the run

### Phase 0 — brief, store, identity rulings (main context)
Unchanged. In Manual mode the test-run question is asked as written.

### Phase 1a — extraction (subagents)
Subagents extract per-product source data into `extract/pN.json` **including the `notes` field for
identity contradictions**. Output to main context: one line per product plus the full `notes` text.
The main model reads every `notes` field. **Identity rulings (§6 contradictory-identity procedure)
are made by the main model only** — never delegated — written to `RULINGS.md`, and in Manual mode
shown to the user before keyword lookup.

(batch7: the same extraction agents also produced the 40–70 candidate keywords per product in the
same pass — `candidates/cN.json` — which removed the separate 65-turn candidate step of batch6.)

### Phase 1b — keyword research (main context, direct API)
See §3.

### Phase 1c — titles (main context)
Titles are built centrally because §8 catalog rules (uniqueness, overlap, family collisions, price
priority) are cross-product and cannot be split. `title-check.py` runs on the whole batch;
`rejects.json` is emitted before any description work starts.

### Phase 1d — descriptions (subagents, 10 products each, Sonnet — user decision 2026-09-03)

**Model: Sonnet, not the main model.** Decided by the user on 2026-09-03 after the blr-batch18 single-product test. The quality gates (`title-check.py`, `desc-check.py`, `struct-check.py`, `gate.py`) are mechanical and every writer must pass them, so the expensive model buys nothing there; what it bought was naturalness, and the test showed naturalness is governed by the second-net load, not the model — the uncapped Sonnet draft glued keywords ("an IPX4 stray cat deterrent and stray cat repellent for rain"), the capped draft (second-net cap of 8, description-format-rule.md) read like copy. Description agents therefore run on Sonnet with the cap in force; identity rulings, keyword fit, titles and the central re-run of every gate stay with the main model. Rule documents are still read in full by each agent (the 8 KB-spec idea was dropped: partial reading is forbidden and the saving was ~1.5%).

Each subagent, before writing a word, reads in full: `description-format-rule.md`,
`title-format-rule.md`, the Backend Update Document's safety notes, `RULINGS.md`, and its 10
products' `extract/`, `titles/` and `rejects.json` entries. (Measured: all repeated rule-document
reading across a whole batch is ~0.37M effective, 1.5% — it is not a cost worth optimising, and
partial reading is forbidden.) It writes to `desc/dN.json`, runs `desc-check.py` and the
structure/length/image/limits checks on its own 10, fixes until clean, and returns ONE line. It
never pushes. The main context then runs every gate again over all 50 — the subagent's pass is not
trusted alone.

**The rule-1 contradiction — resolved 2026-09-02, this is what removed the second round.**
`description-format-rule.md` requires every title keyword to sit within the first ~500 characters
of tag-stripped text. Under the mandated skeleton this is **structurally impossible to satisfy from
prose paragraph 1**: the H2 plus five benefit bullets already consume ~450–500 characters, so prose
1 begins at or past the limit. In batch6, 22 of 50 products failed rule 1 on the first pass and the
whole batch went to a second round — 174 turns instead of roughly 110.

The instruction to every description writer is therefore:

> **Title keywords go in the H2 and the benefit bullets, not in prose 1.** The H2 (12–14 words) and
> the five bullet lead-ins and payoffs are the only text guaranteed to fall inside the first 500
> characters. Place every keyword the title captured there, naturally. Prose 1 carries the reading,
> and prose 2 / Key Features intro / FAQ answers carry the second net.

Run `title-check.py` with descriptions supplied as part of the subagent's own gate loop, not only
centrally, so rule-1 failures are caught by the writer that can fix them cheaply.

### Phase 1e — image re-host (main context or one subagent)
`fileCreate` in batches of 20; img tags copied from raw HTML, only `src` replaced; skipped for
images already on our CDN. **Shopify does not accept AVIF** (`UNSUPPORTED_IMAGE_FILE_TYPE`) — go
straight to a gallery substitute rather than spending a call. A foreign PNG that returns
`Media processing failed` gets one retry, then a gallery substitute. Alt text is rewritten neutral:
supplier brands and unverifiable claims are removed as a standard step.

### Phase 2 — push (one subagent, once)
Payloads built offline into `push/*.json` (≤ 10 products per file). Backup doc written FIRST.
Aliased `productUpdate` + `productVariantsBulkUpdate` per the Backend document, only `userErrors`
requested. **One push per batch.** A second push happens only for products whose userErrors or
Phase 4 verification failed.

### Phase 4 — verification (bounded; this bound is a rule, not a preference)

**Default, and what to do unless a stated condition below applies:**
- light fields for all 50 in one small query per 10 — `title`, `productType`, `seo{title description}`,
  `category{id}`, `status`, `tags`, variant `price`;
- full `descriptionHtml` comparison on **3 spot-checked products** against `push/*.json`;
- the `<img src>` list per product, which comes from the light query's descriptionHtml only for
  those 3 — for the other 47, trust the payload plus the userErrors result.

**A full-HTML fetch and diff of all 50 is done ONLY when a new gate has been added and the whole
batch must be re-swept**, and even then the fetch is saved to a file and scanned by script, never
read into context.

**Batch6 violated this** — a full-HTML diff was run on all 50 with no new gate in play, costing
roughly 0.9M effective and ~40 minutes for no finding. It is recorded here so the choice is not
repeated without a written reason.

### Price verification — check the clock before raising an alarm
When live prices differ from the pre-push snapshot, compare each variant's `updatedAt` against the
push time **before** reporting a problem. In batch6 all 453 variants had changed; `updatedAt` showed
a separate sale job had run an hour before our push, and our payload never contained `variants` at
all. Timestamp first, alarm second.

### Session split
Run as two sessions when needed: **A** = Phase 0 → 1c (research, titles, backup, project docs
written), **B** = Phase 1d → 4 (descriptions, images, push, verify), resuming from the project docs
and `checkpoint.json`. This avoids compaction entirely. Batch6 did not need a split.

---

## 5. Handling rules

- **Count turns before adding a step.** A step that moves data out of context but costs 70 round
  trips is a loss. This is the primary test.
- Files over ~45 KB are never opened with `Read`; use jq/python summaries.
- Large tool results are saved to files and processed by script.
- Progress lines under 50 characters; no per-product narration.
- Any new defect phrasing discovered mid-run is added to the relevant gate and the gate is re-run
  over the WHOLE batch from a fresh live fetch (lesson of 2026-09-02).
- A suspicious image filename is worth one browser look before the push — it is one turn. Batch6's
  `foto_cockroach-5` turned out to be the product's own photo; batch6's `crimson-tide` trophy turned
  out to carry live University of Alabama trademarks.

---

## 6. What this runbook does NOT change

Keyword source and gates · contiguous-phrase construction · product-fit gate · identity procedure ·
character tiers · description structure, length budget and FAQ rules · the three forbidden sections ·
image rules · safety disclaimers · backup before push · Manual/Scheduled behaviour · the Phase 4
spot-check itself. Every one still applies in full.

---

## 7. Target for the next batch

Against the batch6 baseline of **766 turns / 24.4M effective**:

| Change | Turns saved |
|---|---|
| Direct DataForSEO API instead of the browser route (§3) | ~220 |
| No description fix round (§4, rule-1 resolved) | ~60 |
| Phase 4 held to its stated bound (§4) | ~15 |

**Target: ~450 turns / 13–15M effective**, with every gate still green and one push.

Measure it. Record the real number here after the next batch, the same way this section records
batch6. A target that is never measured is the mistake this rewrite exists to correct.


---

## 8. Measured — ddl1-batch7 (2026-09-02, first batch run under this runbook)

Same scope as batch6 (50 products, titles + descriptions + product type + category + collections + images),
plus CTA benefits and season tags. **One push, no compaction, no description fix round.**

| Item | batch6 | batch7 |
|---|---|---|
| Keyword measurement | 223 turns, browser, ~240 approval prompts | **4 API calls from Bash, $0.36, 0 prompts** |
| Description rounds | 2 (22 rule-1 failures) | **1 (0 rule-1 warnings)** — keywords placed in H2 + bullets |
| Pushes | 1 | 1 (push subagent hit a session 429 after batch 4; verified landed, CTA + collections finished from main context) |
| Phase 4 | full-HTML diff on all 50 | light query for 50 + normalized HTML compare from the same single response (no extra fetch) |
| Subagent tokens (raw) | not recorded | ≈ 2.3M (extract 0.53M · descriptions 1.28M · push 0.24M) |
| Turns (estimate) | 766 | ≈ 300 (main ≈ 80, extract 5×14, descriptions 5×~30, push 17) |

Effective-token accounting was not readable inside this session; turn count and the removed browser
route are the measurable deltas. Lessons added:

- **Pass the 44 KB push payloads through a subagent, but expect a 429.** A session rate limit can cut the
  push agent mid-run. Always verify what landed with a live `updatedAt`/title query before re-firing —
  batch7's fifth batch had landed although the agent's report ended at batch 4.
- **A 20-image `fileCreate` batch returns UPLOADED, not READY** — one `files(query:"alt:b7-*")` page pair
  after a minute gave 99 READY; request extra fields so the result spills to a file rather than context.
- **Dead source images: one retry, then gallery substitute** (batch7 #46: 404 GIF).
- **Character counting by eye is unreliable** — first title draft averaged 135 chars; measure with the
  script and trim, never trust an estimate.
- **The linked browser is worth a single batched look** for identity-critical images (batch7: #47 confirmed
  electric griddle, #31's "blue-light glasses" filename was in fact the flash drive, #49 mug message).

---

## 9. Measured — blr-batch11 (the pre-2026-09-07 Tuzwa store — NOT the current Tuzwa store, 2026-09-03, new organisation "Backend DataForSEO-2")

Same scope as batch7 (titles + descriptions + product type + category + collections + CTA + season + alt text); images were already on the store CDN so no re-host step. **One push, no compaction, no description fix round, 0 userErrors.**

| Item | batch7 | blr-batch11 |
|---|---|---|
| Keyword measurement | 4 API calls, $0.36 | **3 API calls, $0.27, 2,471 candidates** — `api.dataforseo.com` had to be added to the new organisation's egress allowlist first (403 until then); it took effect in the SAME session, no restart needed |
| Description rounds | 1 | **1** (0 rule-1 warnings; every subagent ran `gate.py` = title-check + desc-check + struct-check + image/alt/CTA checks on its own 10) |
| Push | 17 turns, 429 mid-run | **11 calls, 28 turns, no 429**: collections joined via `ProductUpdateInput.collectionsToJoin` inside the same productUpdate (no collectionAddProducts calls); CTA in 2 metafieldsSet; alt text in 4 fileUpdate calls of ≤110 |
| Phase 4 | light query + normalized compare | one live query for all 50 (spills to a file), script compare of every field incl. media alt, collections, CTA, variant prices — no extra fetch |
| Subagent tokens (raw) | ≈ 2.3M | ≈ 2.45M (extract 0.64M · rule-doc copy 0.09M · descriptions 1.36M · push 0.36M) |
| Turns (estimate) | ≈ 300 | ≈ 300 (main ≈ 75, extract 5×~11, descriptions 5×~59, push 28, docs 12); wall clock ≈ 1 h 45 min |

Lessons added:
- **Large MCP query results spill to a file automatically** (limit ~25k tokens) — fetch all 50 products with full descriptionHtml in ONE main-context query and split into `raw/pNN.json` by script; extraction agents then never call Shopify.
- **Extraction agents produce the candidate keywords in the same pass** (40–70 per product, including the neighbouring families expected to fail fit) — 5 agents ≈ 0.64M, no separate candidate step.
- **Give every description agent a single `gate.py`** that runs all gates on its own products; the main context re-runs the same script over all 50 — zero second round.
- **Rule docs to disk once** via a small Sonnet agent — never Haiku, it truncates files (`project_read` → `rules/*.md`, then verify with toolkit/MANIFEST.md) so description agents read from disk, not from the project.
- **Catalog-heavy batches (8 plug-in pest repellers, 3 solar stakes, 3 peelers, 2 duplicate pairs) cost the most main-context turns** — the 8.2 overlap loop took ~10 iterations; keep `ov.py` (shared-word report) next to `title-check.py`.

---

## 10. Cost plan adopted 2026-09-03 (after blr-batch11)

The user asked for a materially cheaper run. Adopted, in order of saving: **(1) Shopify via script** — a custom app Admin API token (`read_products, write_products, read_files, write_files`) with `tuzwa.myshopify.com` on the egress allowlist (that was the pre-2026-09-07 store's host; the current Tuzwa store's canonical host is `qu1ysp-7j.myshopify.com` — see toolkit/shopify-api-credentials.md); fetch, push, collections, metafields, alt text and verification run from Bash with zero model tokens and zero approval prompts (the push agent alone cost 0.36M raw in batch11, mostly output tokens re-emitting payloads). **(2) Sonnet for description agents** with the second-net cap (§4 Phase 1d). **(3) Extraction by script** — specs, package, images, variants parsed from HTML mechanically; a cheap model only for identity notes and candidate keywords. **(4) Titles in one small-context subagent** so the main context stays ≈40k instead of growing to 200k over 75 turns. Target for blr-batch18: under half of batch11's cost, ≈1 h; measure and record here.
