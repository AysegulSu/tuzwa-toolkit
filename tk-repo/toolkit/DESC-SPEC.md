# DESC-SPEC — Tuzwa description agents (first written for blr-batch12; gate list refreshed 2026-09-06)

Working dir /home/claude/work. Store = Tuzwa. Second-net cap: titles_final.json lists `sacrificed` (max 8, must be woven in naturally) and `capped` (no obligation) (brand name is NEVER written in any copy or title — the one exception is the comparison block, which compare_build.py writes from the `compare` object; the agent never types it). CDN prefix cdn.shopify.com/s/files/1/0806/1645/6416/ (all description images are already on it — do NOT change any src).

## Read IN FULL before writing anything (no partial reading)
rules/description-format-rule.md · rules/title-format-rule.md (§4 tail zone + "Title rejects flow into the description", §6 fit) · rules/PROJECT-DESCRIPTION.md (Content Formats, Safety Notes, seasonal tags) · rules/cta-benefits-metafield.md · rules/image-alt-text-rule.md · ONLY when brief_flags.json says so: rules/comparison-table-rule.md if q17_compare_table is true, rules/fit-block-rule.md if q19_fit_block is true (both flags false = do not open them, do not write `compare` / `fit`) · RULINGS.md · then, per product: extract/pNN.json (ALL facts/specs/package/how_to_use/usage_tips/faq_source/images/media, `key_features` — the source's own Key Features lines, every one of which becomes an item of your Key Features list — and `sections` — the source's other fact-carrying blocks, each of which becomes its own <h3> section, 2026-09-08), titles_final.json entry (title, captured, sacrificed = second net, fit_reject = must stay OUT of the description too), collections.json.

## Standing user rules (from memory; binding)
- Use ALL content from the source: every spec, dimension, material, package item, use case, audience, context. Nothing dropped or thinned. Wording tightened, facts never.
- Benefit-bullet bold lead-in in sentence case (first letter capital only; abbreviations/units keep their form): `<strong>All day comfort:</strong> ...`
- Specifications items: the attribute name and its colon are bold, the value plain — `<li><strong>Material:</strong> Plush fabric</li>`, never `<li>Material: Plush fabric</li>` (user instruction 2026-09-07; rules/description-format-rule.md §5). Key Features items use the same markup.
- FAQ: exactly `<p><strong>Q: ...</strong><br>A: ...</p>` ×5.
- NEVER a supplier policy promise anywhere (user rule 2026-09-07): warranty, guarantee, money-back / refund / risk-free trial, return policy, support / after-sales promises — not in prose, lists, blocks, FAQ, CTA or SEO, even when the source has it as a spec line. Put every such source line into `omit_per_ruling` ("supplier policy, not product fact"). gate.py FAILs the family; no `add_per_ruling` exemption.
- **Never regenerate final/dNN.json wholesale (user rule 2026-09-07, STR-DUB-2-batch1).** In a correction round edit ONLY the
  field or lines the message names, with a read-modify-write on the existing file (json.load → change the one key → json.dump).
  Never rebuild the file from a build script, a template or your own earlier copy, and never touch a product the message did
  not name: in that batch one agent's build script re-wrote all ten of its files three times and each time reverted the
  `category_proposal` / `collections` values the main context had set after taxonomy lookup. Fields the main context may set
  in your files after you return: `category_proposal`, `collections`, `omit_per_ruling`, `add_per_ruling` — treat them as
  read-only unless the correction message names them.
- Source contradictions (see RULINGS.md) are resolved SILENTLY — never mentioned, never hinted. Log them in `notes_for_log`.
- Title keywords go in the H2 + the five benefit bullets (lead-ins and payoffs), not only prose 1 — the H2+bullets are the only text inside the first 500 chars. Prose 1 also carries them naturally where it fits. Second-net keywords go to prose 2 / Key Features intro / FAQ.
- Ages: state the range, never one end.
- Safety disclaimers (Backend doc): baby/kids/pet supervision; water safety (baby beach tent with pool: never leave a child unattended near water); heat/blade cautions; ultrasonic/pest devices: "not a medical device", keep away from pet rodents/reptiles where relevant, no health/cancer/infection claims; insoles/denture: no medical claims.
- **Additional source sections (user decision 2026-09-08; rules/description-format-rule.md §7c).** Every entry of `extract.sections` is its own `<h3>{heading}</h3>` on the page — the heading EXACTLY as `extract.sections[].heading` (canonical name, never the supplier's), followed by `<ul>` when `kind` is `list` (one `<li>` per source line) or `<p>` paragraphs when `kind` is `prose` (one `<p>` per source line). Every line in your own sentence, values verbatim, never pasted, never two source lines in one item. The fact goes here EVEN WHEN the prose, a bullet or Key Features already carries it — same fact, different sentence. A line RULINGS.md rules out goes to `omit_per_ruling`; a section whose lines are all ruled out is not written. Never write a `<h3>` that is not a skeleton heading or an `extract.sections` heading. Position: after Package Includes, after How to Use / Usage Tips when present, in `extract.sections` order, before the fit block / FAQs. A block in `extract.sections_dismissed` (marketing-only, supplier policy) gets NO section — its usable meaning, if any, is prose.

## Before you return — the eight things gate.py cannot fully catch (added 2026-09-06 after blr-batch25)
These are NOT new rules; each is already in the documents above. They are listed here because in blr-batch25 every one of
them was missed on the first pass by all five agents and cost four correction rounds. The documents above are still read in
full — this list does not replace them. A product is not finished until all eight hold:
1. **rule 1 = 0 WARN**, not "0 FAIL": every captured title keyword, in its exact title form (plural stays plural), sits in
   the H2 or in one of the five bullets — the only text inside the first 500 characters.
2. **A keyword appears ONCE per bullet.** `A bird repellent that never quits: this bird repellent …` is stuffing. Lead-in
   and payoff read as one sentence of copy; never glue two keywords (`this RC shark and swimming shark toy`).
3. **The H2 is a keyword headline, not a sentence** — a 12–14-word noun phrase built from the title keywords
   (`Reflective Heavy Duty Nylon Dog Leash with Padded Handle for Large, Strong Dogs`), never `… Keeps Cars Moving Through
   Snow and Ice`.
4. **Bullets and CTA lines are benefits only**: a problem the shopper has now and will not any more, payoff = a source
   fact. Never a variant fact (`One coat, ten sizes`, `Choose your look: five styles`), aesthetics (`Classic retro tabletop
   design`), a comparison (`unlike ordinary cat toys`, `most cat beds slide`), a universal claim (`any remote`), or an
   outcome the source does not claim (`stops snoring`, `barking stops for good`, `for good`, `years of use`).
5. **Second-net keywords go only into sentences that carry a source fact** (prose 2, Key Features intro, an FAQ answer,
   a bullet payoff). Never a synonym-only sentence (`some households call it a sink filter`). A keyword that has no
   fact sentence to host it stays out with a one-line reason in `notes_for_log`.
6. **Never change the title or seo.title** — both are copied verbatim from titles_final.json.
7. **Fit-rejected keywords stay out of every field**, including their bare head word where it names the rejected product
   (`jacket` on a vest whose `denim jacket` was rejected).
8. **Prose = two paragraphs, customer first (added 2026-09-06, user decision).** Paragraph 1 (above the first image) opens
   on the customer's own moment from the source — the problem they live with, the scene of use, the result they get
   (`the scent fills the room, no flame, the candle never tunnels`) — and carries NO technical mechanism. Paragraph 2 (below
   the first image) is the "how": bulb, materials, mechanism, second-net keywords. Whenever the source has narrative copy
   (nearly always), paragraph 2 is written, not optional. **65–110 words is the norm, not a ceiling**: when the source
   tells more, the prose is longer (a 3rd paragraph is allowed) — struct-check only WARNs above 110 — on one condition:
   every extra sentence carries a source fact or a keyword not yet in the description; a sentence that carries neither is
   padding and goes. Never invent a scene the source does not describe. **Paragraph 1 ends by closing the buyer's biggest
   objection** (added 2026-09-06, user decision): pick the one "but what if…" the source answers — open flame / hot parts,
   slides on the floor, washable or not, fits my size, battery life — and make the last sentence of paragraph 1 answer it in
   the source's words (`no flame, no smoke, no soot, so it can stay on through the evening — the lamp head runs warm, keep
   it out of reach of children and pets`). If the source answers no objection, write nothing; never invent the answer.
   Safety Notes still apply — the sentence reassures within what the source states, it never claims safety.

## Output: final/dNN.json  (one file per product)
{
 "product_id": "gid://shopify/Product/...",
 "title": "<exactly titles_final.json title>",
 "descriptionHtml": "<h2>…</h2><ul>…5 li…</ul><p>…</p>[img 1 tag copied verbatim from extract.images[0].src, only alt rewritten]<p>…optional prose 2…</p><h3>Key Features</h3><p style=\"margin-bottom: 0;\">…</p><ul style=\"margin-top: 0;\">…</ul>[img 2]<h3>Specifications</h3><ul>…</ul><h3>Package Includes:</h3><ul>…</ul>[<h3>How to Use</h3> only when extract.how_to_use has real steps — own sentences, never pasted, never audience lines][<h3>Usage Tips</h3><ul>…</ul> only when extract.usage_tips is non-empty — every line as its own item in your own sentence, values verbatim, RULINGS applied via omit_per_ruling; after Package Includes, before the fit block / FAQs (2026-09-07)][one <h3>{extract.sections[].heading}</h3> + <ul> (kind list) or <p>s (kind prose) per extract.sections entry, in that order — every line as its own item / paragraph in your own sentence, values verbatim, RULINGS via omit_per_ruling; after Usage Tips, before the fit block / FAQs; none when extract.sections is empty (2026-09-08)][remaining imgs placed in the same relative order as the source]<h3>FAQs</h3>5×<p><strong>Q: …</strong><br>A: …</p>",
 "seo": {"title": "<[Product Name] - keyword-rich comma descriptor, UNDER 70 chars>", "description": "<one keyword-dense sentence UNDER 160 chars>"},
 "productType": "<§10b: highest-volume keyword that accurately identifies the product, Title Case, singular, e.g. 'Nose Hair Trimmer'>",
 "category_proposal": "<Shopify Standard Product Taxonomy leaf name; write KEEP if the current extract.category is already the best leaf>",
 "season": "winter|spring|summer|fall|evergreen",
 "collections": ["<1–3 titles chosen from collections.json keys; if none fits, propose 'NEW: <name>'>"],
 "cta_benefits": ["icon|Benefit text", "icon|Benefit text", "icon|Benefit text"]   // icon ∈ wifi,clock,battery,media,check; conversion language per cta rule, ≤30 chars text
 "media_alts": [{"id":"gid://shopify/MediaImage/…","alt":"…"} for EVERY media item in extract.media, in order, per image-alt-text-rule (≤125 chars, unique, derived from the new title; numbering "– image N" from 4 on; description imgs continue the numbering)],
 "notes_for_log": "contradictions resolved, claims removed, anything the operator should know; '' if none",
 "omit_per_ruling": ["<exact source value RULINGS.md says to drop>", ...],   // optional; value_check.py skips these and prints them
 "add_per_ruling": ["<claim phrase RULINGS.md explicitly allows although the extract is silent>", ...],   // optional; assume_check.py prints these as [exempt]
 "fit": {   // REQUIRED when brief Q19 = "Add" (brief_flags.json q19_fit_block true) — OMIT when Skip. rules/fit-block-rule.md — content only; fit_build.py renders the single-column "Right for you if" block directly before <h3>FAQs</h3> plus a FIXED closing sentence you never write (2026-09-06: one column only, no "Not the right fit if"; do NOT write a not_for key). Or "fit": null + notes_for_log "fit: not applicable" for a product where it adds nothing (consumable, one-size accessory).
   "for": ["<exactly 4 lines, 30–110 chars, each `situation — proof` with exactly one ' — ' (2026-09-07): left = the buyer's situation, right = the source fact that answers it — 'Your cat likes a covered, enclosed spot — the tent roof closes on three sides'. Never a generic audience (any age / anyone / everyone): FAIL>"]
 },
 "compare": {   // REQUIRED when brief Q17 = "Add table" (the main context tells you; brief_flags.json q17_compare_table true) — OMIT when Q17 = "No table". rules/comparison-table-rule.md, 2026-09-06 — content only; compare_build.py renders the HTML and inserts it before <h3>Key Features</h3>. Do NOT write the table HTML yourself.
   "name": "<2–5 word short product name, no brand — rendered as 'Tuzwa <name>', e.g. 'Fleece Cat Tent Bed'>",
   "rows": [ {"feature": "<20–60 chars, a source fact written as what the shopper gets, e.g. 'Arctic fleece lining for winter warmth'>", "others": "✘"},
             …exactly 5 rows; at least ONE row's others is a short neutral phrase instead of ✘ (e.g. "1 size", "Varies", "Thinner") — never ✘ on all five; when in doubt whether a typical alternative also has it, write a neutral phrase, not ✘ (2–3 neutral of 5 is normal). Text only — you do not see images; never assume what a source image says.
             Thin source: still 5 — mine every source part (specs, package, variants, image text), write each as the shopper's problem without going past the word's meaning, and turn the plain facts (sizes, colours, box contents) into NEUTRAL rows ("Two sizes, M and L" / "1 size"); 2–3 problem + 2–3 neutral is fine. Fewer than five separable source parts at all: "compare": null + notes_for_log "compare: source too thin" (rule doc §3)… ]
 }
}


## ADD NOTHING BEYOND THE SOURCE — the forbidden-assumption list (added 2026-09-04, user decision)
"Use ALL content" has a twin: write NOTHING the source does not say. A claim that is "typical for this category" is an
invention unless the extract says it. Every one of these reached the store in blr-batch12 and had to be re-pushed:
```
❌ "machine washable"            source said: "washable" / "simple to wash"          (wedge pillow)
❌ "hand wash", "simple hand washing"  source said: "easy to clean"                  (water bottle)
❌ "no app required"             source said nothing about apps                        (earbuds)
❌ "the free app"                source said: "smartphone app"                         (TV backlight)
❌ "remembers settings after a power cut"  source said: "memory function: yes"         (TV backlight)
❌ "reaches tight corners of a cage"  source gave only the 18 cm head length            (hog ring pliers)
❌ "printed user manual"         source said: "user manual"                            (toothbrush)
❌ "or 4 x drill bits, one of each size"  no such variant exists — each size sold alone (drill bits)
❌ "covered without a separate claim process"  source requires a claim with proof     (protection plan)
❌ "saves water without losing pressure"  source said: "without sacrificing performance" (shower head)
```
The same family, never written unless the extract states it in plain words: free · app-free / no app · no tools / tool-free ·
BPA-free / food-safe · machine washable / dishwasher safe · hand wash · power-cut memory · lifetime / guaranteed ·
certified (CE, FDA, RoHS) · universal fit · waterproof (when the source says water-resistant or nothing) · fast / quick
charging · silent / whisper-quiet · eco-friendly / non-toxic · "fits any …" · "works with any …" · a bundle or pack count
the variants do not sell · a use case (car, boat, corners, travel) the source never names · a comparison ("stronger than",
"faster than", "than ordinary …").
Softening a wrong source claim is a RULING (RULINGS.md); adding a plausible one is never allowed. When the source is silent,
the sentence is silent.
**Gate (2026-09-06):** `assume_check.py` runs inside gate.py and FAILS the product when a phrase of these families appears in
the description / SEO fields and the extract never states it (source pattern per family in the script). A claim RULINGS.md
allows despite a silent extract goes into the doc's `add_per_ruling`. The list is a floor: extend it when a new invention
of the same kind reaches a review.

## Gates (run yourself, fix until clean, then run again)
`python3 gate.py NN` (accepts several NN). Must show: fit-build 0 FAIL (when Q19 = Add — exactly 4 `for` lines, each `situation — proof` with one em dash, 30–110 chars, whole line and proof traceable to the extract, no comparison wording, no generic audience, no not_for; the block plus its fixed closing sentence is rendered before <h3>FAQs</h3>; rules/fit-block-rule.md), compare-build 0 FAIL (when Q17 = Add table — the `compare` object renders: 5 rows, each 20–60 chars and traceable to the extract, no comparison wording in a row, at least one neutral Others cell; the block is inserted by the script; when Q17 = No table the section prints `Q17 = No table` and nothing is required — rules/comparison-table-rule.md), unit-dual (script: a measurement given in one unit system gets the other in parentheses in prose, Key Features, Specifications, every <h3> section after Package Includes and FAQ answers — never in the H2, bullets, CTA, blocks, questions, alts, SEO; you do not convert by hand; rules/description-format-rule.md §5, 2026-09-06), keyfeat-cover 0 FAIL and 0 [COPY] (a source line pasted verbatim into the list FAILs since 2026-09-07 — same facts, values verbatim, your own sentence; every line of `extract.key_features` — the source's own Key Features list — present as a `Name: one sentence` item of the `<h3>Key Features</h3>` list, even when a bullet or the prose already carries the fact; a fact-free marketing heading or a forbidden-outcome line goes into `omit_per_ruling` with a reason; rules/description-format-rule.md §4, 2026-09-06), spec-cover 0 FAIL (every source spec line present as an item of the `<h3>Specifications</h3>` list — value_check is not enough: it passes a spec that only appears in a bullet), value-check 0 FAIL (every source number, list item, package item, variant option AND every numberless spec value such as `Material: cotton` present — the verbal-value line is a FAIL since 2026-09-06, no longer a WARN; see rules/description-format-rule.md "Never invent, remove, or alter"; a value RULINGS.md says to drop goes into the doc's `omit_per_ruling` list, as the bare value or as `Name: value`), howto-check 0 FAIL (How to Use only for real steps, every step kept in your own sentence, no audience lines under it) and usage-tips 0 FAIL (every source Usage Tips line an item of <h3>Usage Tips</h3>, own sentence, no copy, no merge, right position — 2026-09-07), sections 0 FAIL (every `extract.sections` entry its own <h3> with the canonical heading, every line an item / paragraph in your own sentence, no copy, no merge, no invented <h3>, right position; source order is a WARN — 2026-09-08), cta-check 0 FAIL (each of the 3 CTA lines is a benefit, not a spec — no sizes/colours/counts (digits OR words: "seven colors", "six modes")/included accessories ("with remote")/units/bare attributes, and the text is measured at ≤30 characters by the script since 2026-09-06; rules/cta-benefits-metafield.md), assume-check 0 FAIL (no forbidden-family claim — machine washable / no app / BPA-free / certified / universal / waterproof / lifetime / non-toxic / than ordinary … — that the extract never states; a ruled exception goes into `add_per_ruling`), age-check WARNs reviewed (a single-age phrase must be a title keyword, appear once, and sit in a sentence that states the range), no `<a>` tag, URL, e-mail or price in any field (gate.py, 2026-09-06 — the format rule's "delete any link, brand name, or price"; a foreign brand name is not script-detectable and stays a RULINGS / review matter), 0 FAIL, 0 rule-1 warnings, second-net warnings resolved (every sacrificed keyword ≥1,000 present naturally OR listed in notes_for_log with a written reason), desc-check 0 hits, struct-check 0 issues (H2 12–14 words; 5 bullets; prose ≥65 words — above 110 is a WARN, allowed only when the source meaning needs it, never padding; total ≥350 words — above 500 is a WARN, allowed only because the source is longer, never by dropping a source line; ≥2 images, all on our CDN; FAQ 110–145 words; seo limits; p+ul margin pairing; no empty elements; no "Note:"; a non-skeleton <h3> only between Package Includes / How to Use / Usage Tips and the fit block / FAQs). Character counts are measured by the script — never by eye. gate.py exits 1 when any section reports a problem and prints `=== gate: CLEAN ===` only when every section is clean (since 2026-09-06); still read the printed FAIL / hits / issues lines — they say what to fix.
Return ONE line per product: `NN | words | gate status | season | productType | category_proposal | collections` and nothing else.
