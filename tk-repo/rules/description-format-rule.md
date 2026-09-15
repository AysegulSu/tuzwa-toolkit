# Product Description Format — Q7 + Q11 Custom Format

The user's own description structure. When a brief answers Q7 with "Rewrite descriptions"
and points to this document (or pastes this structure), this document IS the format. It
works together with `title-format-rule.md` — titles are built first; the
description is then optimized against the finished title.

Saved 2026-08-29 from the user's brief text, plus refinements agreed the same day.

---

## Structure — in this exact order

1. **H2 headline** — built from the highest-CTR / highest-volume Google Shopping
   keywords for this product (normally a close variant of the product title's main
   clusters). Rendered as `<h2>`.
2. **Benefit bullets** — a short bullet list of the product's key benefits.
   Customer-focused, conversion-oriented. Each bullet: **bold lead-in** + very short
   payoff, e.g. `**All-day comfort:** cushioned insole softens every step`. Only
   benefits genuinely supported by the product's actual features — never invent,
   assume, or exaggerate.

   **The lead-in is a benefit, never a spec.** The bold lead-in names what the buyer
   gets, feels or avoids — never a number, dimension, count, material or tech term.
   The payoff states the outcome in plain words; a figure belongs in the payoff only
   when the figure itself is the selling point and reads naturally ("holds for over
   7 hours"). All other figures live in Key Features / Specifications, which exist
   for exactly that.

   ```html
   ✅ <li><strong>All-day comfort:</strong> cushioned insole softens every step</li>
   ✅ <li><strong>Clear in sunlight:</strong> the anti-glare screen stays readable at noon</li>
   ❌ <li><strong>22 cm IPS Touchscreen:</strong> anti-glare, clear in sunlight</li>
   ❌ <li><strong>Four sizes:</strong> 16x24 in up to 32x48 in</li>
   ❌ <li><strong>Three colours:</strong> Gray, Yellow or White</li>
   ```

   Variant facts (sizes, colours) are Specifications content, not benefits. A figure
   removed from a bullet must already exist in Key Features or Specifications — facts
   are never dropped from the description as a whole. (Applied retroactively to
   ddl1-batch3 on 2026-08-31: 114 of 250 bullets were spec-led and were rewritten
   benefit-first.)
   **Which five benefits (added 2026-09-04, user decision after blr-batch12).** The five slots hold ONLY the
   product's most decisive, problem-solving benefits — the reasons a shopper buys. Each bullet is written as
   *what you live with now → what you will not live with any more*, and the payoff is the fact that makes it
   believable. Secondary features, pack counts, aesthetics, category definitions ("goes hands-free", "one pan")
   and variant facts stay out of the bullets; they live in Key Features / Specifications. Wedge pillow, same
   facts, before → after:

   ```
   ❌ Eases nighttime discomfort: the wedge elevates you for acid reflux and snoring relief
   ❌ Cradles you all night: memory foam molds to your head, neck and back
   ❌ Stays fresh with ease: the cover lifts off and washes whenever it needs a refresh
   ❌ Holds its place: a non-slip base keeps the pillow from sliding
   ❌ Keeps essentials in reach: two side pockets hold a phone or glasses      ← not a reason to buy; Specifications

   ✅ Reflux won't wake you at 2 a.m.: the wedge keeps your upper body elevated so acid stays where it belongs
   ✅ Your partner finally sleeps too: the raised angle opens the airway, so snoring eases
   ✅ You wake up where you fell asleep: memory foam holds the incline and the non-slip base stops the slide
   ✅ No stiff neck, no flat spots: the foam molds to your head, neck and back and springs back every night
   ✅ Sweat and spills never settle in: the cover zips off and washes in minutes
   ```

   The ✅ set states no fact the ❌ set did not; it spends the five slots on the problems that decide the purchase
   and writes each one as a concrete scene, not an adjective. Safety Notes still apply: the scene is comfort
   language, never a medical claim.

3. **Short keyword prose** — a brief description that naturally weaves in ALL keywords
   from the product title. ADD ONLY, DELETE NOTHING: every existing product-specific
   detail (size, dimensions, color, material, capacity, weight, specs, compatibility…)
   is preserved unchanged. Normally ONE paragraph; it may be split into TWO when one
   paragraph cannot carry everything — paragraph 2 then sits below the first image and
   above `<h3>Key Features</h3>`, and stays short; more paragraphs follow when the source
   meaning needs them — no cap, no padding (see the length budget). 65–110 words is the
   norm — see the length budget below. Use the highest-volume, highest-CTR keywords that fit
   naturally.

   **Benefit-led prose (added 2026-09-04, user decision).** The prose is written in the same
   customer-focused, benefit-led voice as the bullets — it tells the shopper what the product
   does for them, not what the product is. Keywords and source details sit inside sentences
   about outcomes, not in a catalogue-style recital ("This X is a Y with Z"). Nothing else
   changes: every title keyword still appears, the second net still lands in paragraph 2,
   every source detail is preserved unchanged, the 65–110-word budget holds, and the
   never-invent / no-medical-claim rules apply exactly as before. No new gate, no new step.

   ```
   ❌ This stainless steel insulated water bottle is a reusable water bottle for gym with a straw and handle. It holds 32 oz and keeps drinks cold for 24 hours.
   ✅ Fill this stainless steel insulated water bottle before you leave and it is still ice-cold 24 hours later — 32 oz is enough for a full gym session, the straw lets you drink one-handed, and the handle rides on any bag.
   ```

   The ✅ states no fact the ❌ did not and carries the same keywords; it just spends the words on
   what the buyer gets.
4. **Key Features list** — bulleted; use ALL specifications from the source. An
   optional short intro sentence may precede the bullets.
   **Every Key Features line of the source is an item of this list (user decision 2026-09-06, blr-batch26):** the
   supplier's own feature list (its `<li>` lines and bold "Name:" lines outside the spec / package / FAQ sections,
   collected in `extract.key_features`) is reproduced here one-for-one as short `Name: one sentence` items — even when
   the same fact already sits in a benefit bullet, the prose or the comparison table. The bullet answers "why buy", the
   list answers "what is there"; same fact, different sentence, never a pasted copy. A source line that carries no
   product fact (a marketing heading such as "Elegance That Takes Off") or only a forbidden outcome claim is not
   invented into a feature: it goes into `omit_per_ruling` with the reason in `notes_for_log`. Since 2026-09-06 (user
   decision) `extract.key_features` also carries the concrete features the source states only inside its paragraphs
   (material, mechanism, function, mode, capacity, control, mounting, setting) — the extraction agent adds them; they are
   list items here like the listed ones. `keyfeat_cover.py`
   (in gate.py) FAILs a missing line, exactly as spec_cover.py does for the Specifications list — and, since 2026-09-07
   (STR-DUB-2-batch1, user decision: 88 of 240 source lines had reached the store verbatim), it also FAILs a PASTED line
   ([COPY]): the sentence fabric of the item must differ from the source line; the values inside it (numbers, units,
   materials, names) stay verbatim and are excluded from the measure, so rewording never touches a fact. Paragraph-only
   features and prose spec values are surfaced by `para_feat.py` (README step 3) so the list is never just the supplier's
   own list count. **A source line that belongs to an additional source section (§7c — a Care Instructions or Safety
   Warnings `<li>`, say) is NOT a Key Features item: `sections.py --extract` moves it out of `extract.key_features`, and its
   home on the page is that section (2026-09-08).** Format: **Bold Feature
   Name:** one-sentence explanation — markup `<li><strong>Name:</strong> text</li>`, the name AND its colon inside
   `<strong>`, exactly as in §5 (user instruction 2026-09-11, after `U-Shape Support: Back, hips, legs …` reached the
   store unbolded on the ddl2 pregnancy pillow). Enforced: `list_bold.py` (gate.py, right after fit-build, zero tokens,
   idempotent) wraps a plain leading `Name:` in `<strong>` in both lists; `struct-check.py` FAILs any Key Features or
   Specifications item still without a bold `Name:` lead — an item with no name at all is written by the agent, never
   invented by the script. Reference example:

   > There's more! The smart LED display shows power levels and has a travel lock to
   > avoid accidental use. It's IPX5 waterproof for easy cleaning and offers dual blade
   > performance. Plus, it's USB charger compatible for convenience.
   > - **Floating Blade Head:** The upgraded blade head adjusts to facial contours, capturing long and short hairs for a close shave.
   > - **Ergonomic Design:** The planetary shape and smooth surface offer a better grip, ensuring easy and intuitive shaving.
   > - **All-In-One Machine:** Includes five detachable accessories: rotary shaver, hair clipper, nose trimmer, facial brush, and body trimmer.
   > - **Wireless Charging And Led Display:** Supports wireless charging, Type-C fast charging, and has a digital display showing remaining battery time.
   > - **IPX5 Waterproof:** Fully washable body for wet or dry shaving, easily cleanable by rinsing or soaking in water.
5. **Structured attribute list** (bottom of description) — every available
   product-specific attribute in a clear list: size, dimensions, color, material,
   capacity, weight, specs, compatibility, etc. Do NOT write "Note:" at the end.

   **Format — the attribute name before the colon is bold (user instruction, 2026-09-07).**
   Every Specifications item is `<li><strong>Name:</strong> value</li>` — the name and its
   colon inside `<strong>`, the value in plain text after a space. Example:
   `<li><strong>Material:</strong> Plush fabric</li>` renders as **Material:** Plush fabric.
   No item is ever written as plain `Material: Plush fabric`. Same markup as the Key
   Features list (§4) and the benefit bullets (§2).

   **Prose specs go into the list too (user instruction, 2026-09-05).** "Every available
   attribute" means every attribute the SOURCE states anywhere — not only its own spec
   table. A value that the source gives only inside a sentence (a wattage in the feature
   copy, a cutting width in the package line, a battery capacity in an FAQ, a material
   in the opening paragraph) is still a source value and gets its own Specifications
   line. The source's spec list is copied whole (rule above); the prose is then mined for
   what that list did not carry.
   **Enforcement (2026-09-06, user decision):** the mining is done in the extraction step — the
   extraction agent adds every such prose value to `extract.specs` as its own `{name, value}` pair
   (EXTRACT-SPEC.md), and spec_cover.py in gate.py then FAILs any pair missing from the new
   Specifications list. Until then this paragraph had no script behind it: spec_cover compared only
   the supplier's own table.

   **Dual units (2026-09-06, user decision; scope widened the same day).** A measurement the source
   gives in one system only gets the other system in parentheses after it — in the prose paragraphs,
   the Key Features intro and list, the Specifications list, the Usage Tips and How to Use lists (added 2026-09-07), every additional source section of §7c (added 2026-09-08) and the FAQ answers:
   **imperial first, metric in parentheses, whichever the source wrote** (user decision, same day —
   a US shopper who sees cm first reads the listing as imported): `Weight: 5.1 oz (145g)`,
   `Dimensions: 11.3 x 10.9 x 0.1 in (28.8 x 27.8 x 0.3 cm)`, `Cold resistance: -20°F (-29°C)`,
   `Heat: 122/149/176°F (50/65/80°C)`; a source slash pair is reordered the same way
   (`15.2cm/5.98in` → `5.98in/15.2cm`). A conversion is arithmetic, not an invented value; the
   source figure stays verbatim (in the parentheses when it is metric), so value_check and
   spec_cover still find it. Done by `unit_dual.py` inside gate.py (zero tokens,
   idempotent) — the agent never converts by hand; items the source already gives in both
   systems are left as they are. Electrical units, hours, lumens, mAh and percentages are not
   converted. Engine displacement (`engines up to 10.0 L`, `2.0 L diesel`) stays in litres — the US writes it that way
   too — and a temperature range the source already gives in both scales (`-20°F to 70°F / -29°C to 21°C`) is left as
   written in the dual pass and reduced to its °F half in the budgeted elements (2026-09-12, DDL2-Batch3 p17: the script
   had produced `338.1 fl oz (10.0 L)` and `-29°C to 70°F (21°C)`). Budgeted elements — the H2, the five benefit bullets, the comparison and fit blocks, FAQ questions — get
   IMPERIAL ONLY, never a parenthesis (user decision 2026-09-11, after the ddl2 pregnancy pillow's comparison table
   read `155 x 75 x 60 cm` live: the store sells only in the USA and no metric figure may stand alone anywhere on the
   page, and a "(155 cm)" parenthesis would break a limit or push a title keyword out of the first 500 characters). There
   `unit_dual.imperial_only()` converts metric → imperial and DROPS the metric figure: `155 x 75 x 60 cm` → `61 x 29.5
   x 23.6 in`, `40°C` → `104°F`; imperial text is left as it is. unit_dual.py does this for the H2, bullets and FAQ
   questions; compare_build.py and fit_build.py do it for their blocks at render. The metric source value still stands,
   verbatim and in parentheses, in the Specifications list — that is where value_check / spec_cover find it — so a
   figure that appears ONLY in a bullet or the H2 fails value_check and must also be given its Specifications line.
   CTA lines (metafield, cta-benefits-metafield.md), image alt texts and SEO fields are not touched by any script: a
   measurement written there is written in US units by the agent in the first place. Nothing is invented — a line exists only when the source
   states the value; a product whose source has no more facts keeps a short list.
6. **Package Includes:** — bulleted list. The heading is written in title case exactly
   as `Package Includes:` — NEVER in all caps ("PACKAGE INCLUDES:" is wrong). Added
   2026-08-31 at the user's instruction; the ddl1-batch1 headings were corrected to
   this casing the same day.
7. **HOW TO USE** — only when the source gives real steps / instructions (do this, then that; charging, fitting, care
   steps). Every step kept, in order, values verbatim — in the writer's own sentence, never pasted (`howto_check.py`,
   2026-09-07). Audience / occasion / "Ideal for…" lines are NOT steps and never sit under this heading: they are use
   contexts (extract.facts) woven into prose 2 / an FAQ answer / the Key Features intro — or, when the source lists them
   under a Usage Tips block, they are the Usage Tips list below. (STR-DUB-2-batch1: 9 products had reached the store
   with the supplier's "Usage Recommendations" pasted verbatim under How to Use; user decision.)
7b. **USAGE TIPS** (added 2026-09-07, user decision) — when the source carries a block headed Usage Tips / Usage
   Recommendations / Tips / Recommended Uses, our page carries `<h3>Usage Tips</h3><ul>…</ul>`: every line of the block,
   one line = one item, in the writer's own sentence with values verbatim — never pasted (`usage_tips.py`, in gate.py).
   RULINGS apply (a CPAP comparison, a medical outcome, a supplier policy line goes to `omit_per_ruling`). Position: after
   Package Includes (and after How to Use when present), before the fit block / FAQs. No source block → no section.
7c. **ADDITIONAL SOURCE SECTIONS** (added 2026-09-08, user decision; applies from the first batch run after this date —
   no pushed product is re-processed) — every OTHER headed block of the supplier's description that carries a product
   fact becomes its own `<h3>` section on our page. Until now only the known blocks (Key Features, Specifications,
   Package Includes, How to Use, Usage Tips, FAQs) survived as sections; a Care Instructions, Warnings, Materials, Design,
   Applications, Compatibility, Storage, Charging, Installation, Size Guide or Notes block lost its heading in extraction
   and its lines dissolved into the prose. Rule now:

   - **Tip A → section.** A source block that carries at least one product fact (a figure, a unit, a material, a care /
     warning / installation instruction, a compatibility statement, a value word of the extract) is reproduced as
     `<h3>{Heading}</h3>` followed by `<ul>` (when the source block is a list) or `<p>` paragraphs (when it is prose):
     **every source line = one item / paragraph**, in the writer's own sentence, values verbatim — never pasted ([COPY]),
     never two source lines in one item ([MERGED]). RULINGS apply exactly as in §7b: a supplier-policy line, a medical
     outcome, a "colour may differ due to the monitor" disclaimer goes to `omit_per_ruling`; a block that is ruled out
     whole gets no section.
   - **Tip B → prose.** A block with no product fact at all — a marketing heading over adjective sentences ("Elegance
     That Takes Off. Turn heads wherever you go.") — is NOT a section. It dissolves into the prose as before, and the
     run log shows it (`extract.sections_dismissed`). A supplier-policy block (Shipping, Warranty, Returns, About Us) is
     dismissed the same way and never reaches the page (hard rule below).
   - **Heading = normalised vocabulary.** The page never carries the supplier's own heading; each block is mapped to
     one canonical name — `Care Instructions`, `Safety Warnings`, `Materials`, `Design`, `Applications`,
     `Compatibility`, `Storage`, `Charging`, `Installation`, `Size Guide`, `Notes` (the master list is `CANON` in
     `sections.py`; a family that recurs unmapped is added there — floor, not ceiling). A block the script cannot map
     is written with `heading: null` + `heading_source` and printed [UNMAPPED]; the extraction agent or the main context
     sets the heading by eye (a canonical name when one fits, otherwise a 1–3-word title-case name), and the page
     heading must equal `extract.sections[].heading` exactly.
   - **Same fact, different sentence — even when it is already elsewhere.** A fact in one of these sections is written
     here even when the prose, a bullet or the Key Features list already carries it (the same rule §4 applies to Key
     Features: the prose answers "why", the section answers "what / how", and a shopper looks for care or safety
     information under its heading, not in the middle of a paragraph). A section line is never also a Key Features
     item: `sections.py --extract` moves it out of `extract.key_features`.
   - **Position:** after Package Includes, after How to Use and Usage Tips when present, the sections in the source's
     own order, before the fit block / `<h3>FAQs</h3>`. Their words count toward the total like Usage Tips do (the 500
     ceiling is a WARN and never removes a source line). Dual units apply inside them (§5).
   - **No invented section.** A `<h3>` on the page that is neither a skeleton heading nor a heading in
     `extract.sections` is a FAIL — the page carries the source's sections, not the writer's.
   - **Gate:** `sections.py` (in gate.py): `--extract` writes `extract.sections` / `extract.sections_dismissed` from
     raw/ (run after `keyfeat_cover.py --extract` and `usage_tips.py --extract`); the check FAILs a missing section, a
     missing line, a [COPY], a [MERGED], a wrong position, an invented heading, and WARNs on source order.
     `struct-check.py` also rejects a non-skeleton `<h3>` outside the allowed position.
8. **FAQs** — exactly 5 questions, fully product-related, conversion-oriented, the
   questions real customers would ask. Use the strongest keywords as long-tail phrases
   in both questions and answers. **The question and its answer live in ONE element,
   separated by `<br>`** — never two separate `<p>` elements, which renders a visible
   paragraph gap. Exactly this markup:

   ```html
   <p><strong>Q: What is the size of the blanket?</strong><br>A: Approximately 27.5 in long and 33 in wide.</p>
   ```

   This is the markup already used by the ddl1-batch1 and ddl1-batch2 catalogue and the
   FAQs must match it. The same principle governs the rule below — a question and its
   answer are one block, an intro and its list are one block; never let a default
   paragraph margin split something that should read as a unit.

### No gap between an intro paragraph and the list under it

Where a `<p>` intro sentence sits directly above a `<ul>` — typically the Key Features
lead-in — the two elements' default margins render an unwanted gap. The intro and its
list must read as one block. Required markup:

```html
<p style="margin-bottom: 0;">There is more to this …</p><ul style="margin-top: 0;"><li>…</li></ul>
```

The `<p>` carries `style="margin-bottom: 0;"` and the `<ul>` immediately after it carries
`style="margin-top: 0;"`. This applies anywhere a paragraph is immediately followed by a
list, not only in Key Features. Applied retroactively on 2026-08-31 across ddl1-batch1
(50 products), ddl1-batch2 (4 products) and ddl1-batch3 (27 products).

## HTML skeleton — exact element order and heading levels

```html
<h2>Headline</h2>
<ul> 5 benefit bullets </ul>
<p> keyword prose, paragraph 1 </p>
[image 1]   ← always present: source image, or gallery image 2 when the source has none
<p> keyword prose, paragraph 2 — only if needed, short </p>
<p> keyword prose, paragraph 3 … — only when the source meaning needs it </p>
<div class="vp-compare"> … </div>   ← comparison block "Tuzwa vs Others", present when brief Q17 = "Add table", rendered by compare_build.py — see comparison-table-rule.md (added 2026-09-06)
<h3>Key Features</h3> optional intro + <ul>
[image 2]   ← always present: source image, or gallery image 3 when the source has none — carries style="display:block;margin-bottom:24px" so the Specifications heading does not sit flush under it (user instruction 2026-09-11; added by list_bold.py, checked by struct-check.py)
<h3>Specifications</h3> <ul>
<h3>Package Includes:</h3> <ul>
<h3>How to Use</h3>   (only when the source has real steps — never audience lines)
<h3>Usage Tips</h3> <ul>   (only when the source has a Usage Tips / Usage Recommendations block — every line, own words; 2026-09-07)
<h3>Care Instructions</h3> <ul> / <h3>Safety Warnings</h3> <p> / <h3>Materials</h3> …   (§7c: one <h3> per fact-carrying source block, canonical heading, source order, every line own words; 2026-09-08 — none when the source has none)
<h3>FAQs</h3> five <p><strong>Q: …</strong><br>A: …</p>
```

Only the top headline is `<h2>`; every section heading is `<h3>`. ddl1-batch3 used
`<h2>` for every section where the catalogue uses `<h3>` and had to be re-pushed.

**Comparison block (user decision, 2026-09-06).** When the brief's Q17 says "Add table" (optional
per batch; unanswered = No table), every description carries one "Tuzwa vs Others" table directly
before `<h3>Key Features</h3>`: 5 product rows (source facts written
as what the shopper gets, at least one Others cell neutral such as `1 size` instead of ✘)
plus a fixed store row `30-day easy returns`. The writer supplies only the five rows and a
2–5-word product name (`compare` object, DESC-SPEC.md); `compare_build.py` renders the fixed
theme-coloured HTML and inserts it. It is the one place the store name is written — the
brand ban holds everywhere else. Its words are outside the length budget below. Full rule:
`comparison-table-rule.md`.

## Length budget (measured from the ddl1-batch2 catalogue)

| Part | Budget |
|---|---|
| Whole description, visible text | 350–500 words |
| H2 headline | 12–14 words |
| Benefit bullets | exactly 5 `<li>`, ~60 words total |
| Keyword prose | **as many `<p>` as the source meaning needs — usually one or two, three when the source is long; no hard cap. 65–110 words is the norm, more only when the source carries it; never padded** |
| FAQs | 110–145 words for all five pairs |

- The keyword prose is normally ONE paragraph, but it **may be split into TWO** when the
  first one cannot carry everything. Paragraph 1 sits above the first image; paragraph 2
  sits **below the first image and above `<h3>Key Features</h3>`** and stays short.
  Prefer splitting at a natural point over letting paragraph 1 run long.
- **No paragraph cap (user instruction, 2026-09-05).** The prose is as long as the source
  MEANING needs — nothing the source says is cut for a word count, and nothing is added to
  fill one. Usually that is one or two paragraphs; a third is normal when the source is long
  (how the product is used, what it is made of and why, the situation it solves — content
  that has no list home). Extra paragraphs sit after paragraph 2, still above
  `<h3>Key Features</h3>`. The test for every sentence beyond the 110-word norm: it carries a
  source fact or a keyword that is not already in the description — otherwise it is padding
  and it goes. `struct-check.py` fails below 65 words, warns above 110, and never fails on
  prose length or paragraph count; `value_check.py` / `spec_cover.py` remain the gates that
  guarantee nothing from the source is missing.
- Paragraph 1 keeps the title keywords — they must stay inside the first ~500 characters
  of the tag-stripped text. Paragraph 2 is where second-net keywords that would not fit
  go. Revised 2026-08-31; the earlier rule allowed only one prose paragraph.
- The combined budget does not move for the normal case: both paragraphs together 65–110
  words, and the whole description 350–500 words (three-paragraph exception above). Unchecked prose is what inflated ddl1-batch3 (prose median
  130 words against a 79-word ddl1-batch2 house standard, descriptions median 589 words
  against 385).

  **Ceiling raised 430 → 500 (user decision, 2026-09-04, after blr-batch22).** The 430
  ceiling was colliding with rule 5 and with "DELETING A SHORT SPEC LINE" below: on 32 of
  the 50 blr-batch22 products, 112 source spec lines had been left out of the
  `<h3>Specifications</h3>` list because the description was already at 420–430 words.
  A spec line is never the thing that gives way — the ceiling is. The sub-budgets do NOT
  move with it: H2 12–14, exactly 5 bullets, prose 65–110 combined, FAQ 110–145 all stay
  as they are, so the extra room goes to the attribute and package lists, never to prose.
  **When the copy itself grows, the answer is the two-paragraph split, not a longer single
  paragraph: split the prose and put paragraph 2 below the first image**, per the bullet
  above (user instruction, 2026-09-04).
- Second-net overflow goes to paragraph 2 first. Whatever still does not fit goes into the
  Key Features intro sentence or into FAQ answers — those remain available after
  paragraph 2. Second-net keywords must still be present in the description, just not
  necessarily in the prose.
- Where the two rules collide — "all title keywords and recovered rejects inside the
  first ~500 characters" versus the prose budget — the prose budget wins for the
  recovered rejects; title keywords always stay in the head.
- The only permitted overrun is a product whose own source data is longer than the
  budget (for example a garment with full men's and women's size charts, ddl1-batch3 #29
  at 612 words). Facts are never dropped to hit the budget; wording is tightened instead.
  **The ceiling never removes a source line (user instruction, 2026-09-05).** Nothing the
  source states — a spec line, a package item, a value, a list item, a range end, a unit —
  is ever left out because of the 500-word ceiling. When the source is longer, the
  description is longer: `struct-check.py` reports > 500 as a WARNING, not a failure, and
  `spec_cover.py` / `value_check.py` (which do fail) are the gates that decide. Every overrun
  is noted in the batch run log with its word count.

## Hard rules

- Delete any link, brand name, or price found in the source description. Our own store name
  appears only inside the comparison block (`comparison-table-rule.md`), never in copy,
  title, SEO fields or alt text.
- **Never include supplier policy promises (user rule 2026-09-07, DENEME batch):** warranty, guarantee,
  money-back / refund / risk-free trial, return policy, customer-support or after-sales promises are a
  third-party seller's policy, not a product fact — they are NEVER written anywhere (prose, lists,
  comparison block, fit block, FAQ, CTA lines, SEO), even when the source lists them as a spec line
  (`Motor warranty: 2 years`). Every such source line goes into `omit_per_ruling` with the reason
  "supplier policy, not product fact". gate.py FAILs the family; there is no exemption.
- Never invent, remove, or alter product specifications.
- Safety notes still apply (Backend Update Document): baby/kids/pet supervision
  disclaimers, water-safety warnings, soften/remove medical claims.
- Image handling per the brief's Q14: never delete embedded images; re-host foreign
  ones; count and position unchanged.
- **A description with no image gets two (user instruction, 2026-09-05).** When the source
  description carries no `<img>`, insert two of the product's own gallery images
  (`product.media`, already on our CDN) at the skeleton positions: image 1 between prose
  paragraph 1 and paragraph 2 / Key Features, image 2 between Key Features and
  Specifications — so there is always prose between the two images. Use the second and
  third gallery images (the featured image already heads the page); with fewer gallery
  images use what exists, never a foreign URL, never a duplicate of the featured image.
  Alt text per image-alt-text-rule.md. A description with one source image gets one
  gallery image added at the empty slot. `struct-check.py` fails a description with fewer
  than two images.
- **Never invent, remove, or alter — the four ways it actually happened (blr-batch12, 2026-09-04, user instruction:
  never again).** Every value in the source appears in the description, whole. The four patterns that shipped and
  had to be re-pushed:

  ```
  ❌ SUMMARISING A LIST   source: Picture resolution options 36MP, 32MP, 30MP, 24MP, 20MP, 16MP, 12MP, 10MP, 8MP, 5MP, 3MP, VGA
                          written: (nothing — five whole spec lines dropped)                              (night vision binoculars)
                          source: Frequency band, Asia version: FDD 1.3.5.8 TDD 38.39.40.41 WCDMA 1.5.8 / European version …
                          written: "Asia version and European version"                                    (mobile hotspot)
  ❌ CUTTING A RANGE TO ONE END   source: up to 350-450 rpm  →  written: up to 450 rpm                     (spin scrubber)
  ❌ DROPPING ONE OF TWO UNITS    source: 6.1 x 4.7 x 2.4 in (155 x 120 x 60 mm), 10.6 oz (300 g)
                                  written: 6.1 x 4.7 x 2.4 in / 10.6 oz                                    (night vision binoculars)
  ❌ DELETING A SHORT SPEC LINE   source: Handling: ergonomic grip, lightweight and durable construction → written: (nothing)
                                  also: "triple-layer technology", "Current: 70-200mA", "military use", "UHS-II/I" → "UHS-II",
                                  "sides, feet" in a support list, Style / Finish Type / Surface Recommendation lines
  ```

  A list is written out in full, every item. A range keeps both ends. Two units stay two units. A spec line is never
  deleted to make the word budget — the budget is met by tightening prose and FAQ wording, and if the source is
  genuinely longer than the budget the overrun is the permitted exception. "Nothing dropped" is checked value by
  value against the extract before the product is finished, not assumed.
  **Gate:** `value_check.py` (toolkit, script, zero model tokens) runs inside `gate.py` and FAILS the product when any source
  number, list item, package item or variant option is absent from the description; a value a ruling drops is listed in the
  doc's `omit_per_ruling` so the omission is explicit in the log. Added 2026-09-04 at the user's instruction.
- **Dead source image (re-host fails with 404 / dead link):** do not leave the foreign
  `src` in place. Replace the `src` with one of the product's own gallery images
  (`product.media`, already on our CDN), preferring one that is not the featured image
  so the page does not show the same photo twice. Keep the `<img>` tag, its wrapper and
  every other attribute unchanged, so image count and position stay the same. Log the
  product, the dead URL and the gallery image used. Decided by the user 2026-09-02
  (ddl1-batch4 #31 puffer jacket, `1/0654/9028/8866/...FLORA-Jacket_Model_Image` →
  gallery image `..._Black_8_...jpg`). This replaces the batch4-era practice of leaving
  the dead src untouched and waiting for a decision.
- **No description is written before `rejects.json` exists.** Build every title in the
  batch first, run `title-check.py`, and let it emit `rejects.json` — the
  per-product list of keywords the title could not capture. Each product's sacrificed
  list is an INPUT to its description (second net, below), not a check performed
  afterwards. Added 2026-08-29 at the user's instruction, after blr-batch4 where the
  descriptions were written straight from product data and the second net was missed.
- **ABSOLUTELY FORBIDDEN: internal reasoning, working notes, or editorial commentary in
  customer-facing text.** See the dedicated section below — this is a push-blocking
  rule, not a style preference.
- **ABSOLUTELY FORBIDDEN: a Specifications line that reports an absence, a hedge or a
  source contradiction.** Three named forms, all banned outright — see "Three banned
  Specifications forms" below.
- **ABSOLUTELY FORBIDDEN: keyword-alias lists such as `Also Sold As:`.** See the last
  forbidden section — also push-blocking.

## FORBIDDEN — writer's internal notes leaking into customer copy

Added 2026-09-02 after the ddl1-batch5 review. Products carried the writer's own
decision-making inside FAQ answers and spec lines — sentences written for the operator,
not the shopper. Examples that actually reached the store:

- "the supplier states no level count, so we claim none"
- "the safety wording the source omits"
- "we make no leather claim"
- Winter Boots (#47): "leather wording on the images is leftover text from another
  listing"
- Heated Vest (batch4): "Product type: heated vest (source spec line says heated cotton
  vest; contradicted)" and "Stated safety (uncertified):"
- Humidifier (batch3): "Water tank: Refillable (capacity unstated)", "The spec list gives
  16 x 15 x 18 cm"

Every one of these is a defect. The customer never sees "the supplier", "the source",
"the listing", "the spec list", "the images say", or any sentence explaining what we do
or do not claim and why. The description is the store speaking to the buyer — it is
never the writer speaking to the user, to a reviewer, or to itself.

**The rule:**

- The description must contain ZERO meta-commentary: no explanation of sourcing, no
  justification of a decision, no note about missing or conflicting source data, no
  reference to the supplier, the source description, the spec sheet/list/table, the
  original listing, the product images' text, another listing, or the writing process
  itself.
- If the source lacks a fact, simply do not state that fact. Silence is the only correct
  handling. Never write "we don't claim X", "X is not specified", "the source does not
  say", "no X is stated", "(capacity unstated)", "uncertified" or any equivalent. A FAQ
  whose honest answer would be "we don't know" is the wrong FAQ — pick a question the
  source CAN answer.
- If the source contradicts itself or the images (e.g. "leather" on an image, no leather
  in the specs), resolve it silently: state only what the specs support, and never
  mention the contradiction. A contradiction the writer needs to flag goes into the run
  log (`run-log-<batch>.md`), never into `descriptionHtml`.
- First person plural is allowed only as the store addressing the customer ("we ship
  within 24 hours"). It is never allowed as the writer describing its own choices
  ("we claim", "we make no claim", "we omit", "we state").
- The same ban covers every field: benefit bullets, prose, Key Features, Specifications,
  FAQs, SEO title and SEO description.

### Three banned Specifications forms

Named explicitly by the user on 2026-09-02, from live examples. A Specifications line
carries a VALUE. It never carries an absence, a hedge about the value, or a note about
the sources disagreeing. If there is no value, the line does not exist.

**1. A heading that names an absence.** Winter Boots (#47) shipped with a literal spec
heading `What Is Not Claimed:`.

```html
❌ <li><strong>What Is Not Claimed:</strong> no material, waterproofing or temperature rating is stated by the supplier, so none is claimed.</li>
✅ (delete the line entirely)
```

Never write a heading whose subject is what the product does not have or what we decline
to say: `What Is Not Claimed`, `Not Stated`, `Unknown`, `Unspecified`, `Missing Data`,
`Not Confirmed`, `Stated Safety`.

**2. A parenthetical hedge inside a spec value.** Driving Gloves (#48) shipped
`touchscreen-compatible fingers (which fingers is not stated)`.

```html
❌ <li><strong>Touchscreen:</strong> touchscreen-compatible fingers (which fingers is not stated)</li>
✅ <li><strong>Touchscreen:</strong> touchscreen-compatible fingers</li>
```

The parenthetical is the writer telling the reader what the writer could not find out.
Keep the value, delete the bracket. If nothing survives the deletion, delete the whole
`<li>`. This covers every variant: `(no percentages stated)`, `(no grade number stated)`,
`(type and count not stated)`, `(no polymer named)`, `(no fibre content stated)`,
`(capacity unstated)`, `(uncertified)`, `(maker stated)`, `(spec list)`.

**3. A line reporting that the sources disagree.** Cat Play Mat (#46) shipped "The
supplier's two timer figures contradict, so no duration is quoted."

```html
❌ <li><strong>Automatic Shut-Off:</strong> the unit powers down by itself. The supplier's two timer figures contradict, so no duration is quoted.</li>
✅ <li><strong>Automatic Shut-Off:</strong> the unit powers down by itself to save battery.</li>
```

A conflict between two source figures is resolved silently — state the part that is not
in dispute, drop the disputed figure, and record the conflict in the batch run log where
the operator can see it. The customer is never shown the seam.

**Blocked phrases — the push script must grep the tag-stripped text of every rewritten
field and REFUSE to push any product that matches (case-insensitive). The full, current
regex list lives in `desc-check.py`; the families are:**

```
the supplier | supplier states/says/omits | by the supplier | the maker | maker states |
the manufacturer states | by the manufacturer | the source | source omits/states/says |
source spec | source line | (source … ) | the listing | another listing |
the original listing | leftover text | on the images | the images say | image text |
spec sheet | spec table | spec list | feature list | feature line | box list |
the specification | per the spec | we claim | we make no | we quote no | we omit |
claim none | no .* claim is made | claims no | so none | none is claimed/quoted/stated |
is/are not claimed/quoted/stated/specified/cited | not stated/specified/given/claimed/
quoted/cited/named/provided/disclosed | no .* is given/stated/listed/named/provided |
does not state/specify/name/give | what is not claimed | what is not supplied |
no size chart is supplied | the only figure given | per a typical | unstated |
unspecified | unconfirmed | uncertified | unverified | not certified | stated safety |
not published | contradict | contradicted | figures/percentages/specs conflict |
wording the/that | as written | the writer | this rewrite | this description |
listed as/for | described as | stated as | nothing states | we do not print/claim |
also sold as | also known as | aka: | other names | alternative names | search terms |
related terms | also called | sometimes called | under other names
```

Plus a **semantic sweep** that catches the phrasings a fixed list always misses: flag any
sentence where a negation (`no`, `not`, `none`, `never`, `without`, `nothing`) sits within
about 60 characters of an information-word (`stated`, `specified`, `given`, `listed`,
`published`, `named`, `cited`, `claimed`, `quoted`, `confirmed`, `disclosed`, `declared`,
`percentages`, `figures`, `content`). This is what caught "given without percentages",
"fibre content is not listed" and "no figures published" and "no temperature range stated"
after fixed-list passes had already reported clean.

Deliberately NOT blocked, so the gate does not over-fire on store voice: "sold as / sold
in / sold for", "not included / no X included" (package fact), "not for submersion", "not
a medical device / not personal protective equipment" (liability wording), "no child
sizing is offered". The banned thing is the writer's *sourcing* voice, not a plain
customer-facing fact stated in the negative.

The blocked list is a floor, not a ceiling. It was widened nine times during the
2026-09-02 sweep. Whenever a new phrasing of the same defect turns up, add it and re-run
the gate over EVERY batch — from a fresh live fetch, not from the products already in
the fix set. (The last three defective products of the sweep were missed precisely
because a widened gate was re-run only over the fix set.)

A hit is a hard stop for that product: regenerate the field, re-check, then push. Never
push and "fix later". The gate lives in `desc-check.py` and runs as part of the
pre-push checks, alongside the length and image checks. Log every hit (product #, field,
matched phrase) in the batch run log.

**Retroactive sweep, 2026-09-02 — completed and verified live.** The gate was run over
ddl1-batch1 through ddl1-batch5 (250 products), and all five batches were re-fetched
from Shopify after the final push. **111 products were defective and were rewritten and
re-pushed: 2 in batch1, 0 in batch2, 21 in batch3, 45 in batch4, 43 in batch5.** The
count grew well past the first estimate of ~25 because the widened patterns also caught
spec lines reading `Weight: not stated by the supplier`, Key Features intros ending
"...plus the safety wording the supplier omits:", attribution ("listed for", "the maker
rates"), and the three banned Specifications forms above.

Final live verification: fixed-list gate 0 hits in all five batches; semantic sweep 0
true hits; every `<img>` src list identical to the pre-sweep snapshot (no image added,
removed or moved); all SEO titles < 70 and SEO descriptions < 160; five FAQs per product;
no empty `<p>/<li>/<ul>`.

Fix patterns used, for reuse in future sweeps:

- A spec line whose value is only "not stated" → **delete the whole `<li>`.**
- A spec line with a real value plus a "not stated" parenthetical → **keep the value,
  drop the parenthetical** (`Material: wood (species not stated)` → `Material: wood`).
- A Key Features intro naming what the source omits → neutral intro
  ("...plus the pet-safety wording the supplier omits:" → "...plus how to keep play
  safe:").
- An FAQ whose answer was "we don't know" → **replace the question** with one the source
  can answer. Never leave fewer than 5 FAQs.
- A safety-relevant absence ("no load capacity is stated, so do not sit on it") → keep
  the instruction, drop the sourcing: "It is an accent surface rather than seating, so
  do not sit or stand on it."
- Manufacturer attribution on a spec ("the maker rates it to 440°F") → the passive
  form, "**rated to 440°F**". This keeps the liability hedge while removing the source
  language; "up to" is likewise a hedge that survives. Attribution to "the maker" or
  "the supplier" is never the way to hedge.
- A certification hedge ("uncertified", "Stated safety (uncertified)") → state the
  feature plainly ("Safety features: overheat protection …") or, where the point is a
  liability disclaimer, state the class plainly ("a fabric face covering only: not
  personal protective equipment and not a medical device").
- A dimension attributed to a document ("the spec list gives 16 x 15 x 18 cm") →
  "About 16 x 15 x 18 cm".

## Age ranges — state the range, never one end of it

Added 2026-09-02 at the user's instruction, after the batch5 magnetic matching game
(age 4-5+) read "toys for 4 year olds", "gifts for 4 year olds" and "educational toys for
4 year olds" three times and never mentioned five — a shopper with a five-year-old would
read it as a four-year-old's toy.

- **A product with an age range is described with the range**, in the form the source
  gives it: `ages 4-5+`, `ages 2-5+`, `3 years and up`. This is the customer-facing
  statement in the prose, the Specifications line, the FAQ answer and the SEO description.
- **Single-age keyword phrases (`toys for 4 year olds`, `gifts for 3 year olds`) are never
  the way the age is communicated.** They confuse the customer when the product covers
  more than that one age. A single-age phrase may appear in the description ONLY when it
  is a keyword captured by the product title (rule: every title keyword appears in the
  description), and then at most once, inside a sentence that also states the full range
  or its upper end ("toys for 2 year olds through age five").
- **Measured age keywords are never stacked on one end of the range.** If the second net
  holds both the 4-year-old and the 5-year-old families, neither is woven in as a bare
  list; the range form carries the meaning and the title keyword (if any) carries the
  single-age phrase once. Second-net age keywords that cannot be placed this way are
  rejected with the written reason "age range — single-age phrasing would mislead".
- An open-ended lower bound ("ages 3 and up") may be paired with its single-age keyword
  ("toys for 3 year olds") because the keyword IS the lower bound and the "and up" is
  stated beside it — the ddl1-batch2 construction trucks pattern.

Applied retroactively 2026-09-02 to four batch5 products (felt board 2-5+, travel busy
board 2-5+, transforming magnetic toys 3-5+, magnetic matching game 4-5+). Titles were not
changed: a title cluster such as `Toys for 2 Year Olds` is a measured keyword phrase and
stays; the description is where the full range is made explicit.

## FORBIDDEN — keyword-alias lists ("Also Sold As:")

Added 2026-09-02 at the user's instruction, after this line was found live on the
travel makeup bag (ddl1-batch5):

```html
❌ <li><strong>Also Sold As:</strong> makeup travel case, cosmetic travel case, cosmetic pouch, makeup box, travel makeup organizer</li>
```

A naked list of alternative product names is keyword stuffing in plain sight. It tells
the shopper nothing, it reads as SEO plumbing left on the page, and Google treats a bare
synonym dump as exactly that. **NEVER, under any circumstance, write a line of this
kind** — not in Specifications, not in Key Features, not anywhere.

Banned headings and constructions, in every casing and punctuation variant:

```
Also Sold As: | Also Known As: | AKA: | Other Names: | Alternative Names: |
Search Terms: | Keywords: | Related Terms: | Also Called: | Sometimes Called: |
"<x>, <y> or <z>: the same <thing> under other names"
```

The last form is the same defect wearing a sentence. ddl1-batch3's ratchet straps
carried "Truck straps, trailer straps or cargo straps: the same tie downs under other
names." — an alias list with a colon in front of it. It was rewritten to "Whether they
ride in a truck bed, on a trailer or over cargo, these tie downs do the same job:" —
the same three keywords, doing actual work in a sentence.

**What to do instead:** synonyms belong in running prose, in a benefit bullet, in a Key
Features line or in an FAQ question, where each one sits inside a sentence a shopper
would read anyway. The second net is satisfied by natural placement, never by a list.
If a synonym cannot be placed naturally, it does not go in the description.

The pre-push gate refuses any product whose tag-stripped text matches the constructions
above. Applied retroactively 2026-09-02 to the two products carrying it (makeup bag
ddl1-batch5, ratchet straps ddl1-batch3); the makeup bag's five orphaned keywords were
rewoven into its two prose paragraphs rather than dropped.

## Keyword placement rules (agreed 2026-08-29)

- **Title–description consistency:** every keyword captured by the product title must
  appear naturally in the description. Google cross-checks title + description +
  landing page; "in the title but not on the page" leaks relevance.
- **First ~500 characters carry the load:** all title keywords (and recovered rejects,
  next rule) must appear within the H2 + first prose paragraph, because the shopping
  feed truncates long descriptions. Lower sections (specs, FAQ) serve the PDP and
  organic search.
- **Second net:** keywords sacrificed during title construction — collision losers,
  runner-up tails, gate-passers that failed construction, below-median leftovers — are
  woven naturally into the description (see "Title rejects flow into the description"
  in `title-format-rule.md`). A keyword rejected for PRODUCT FIT stays out of
  the description too. Natural placement only — never an alias list, see the forbidden
  section above.
- **Expectation note:** the description does not change the Shopping card's CTR (the
  card shows title/image/price/rating). Its job is matching quality — more and better
  impressions. CTR levers are title, image, price, ratings, promotions.

## Brief usage

In future briefs, Q7 can simply say:
`Rewrite descriptions — use description-format-rule.md`
and Q11 is covered by the same document (sections 1–2).

## Second-net cap — at most 8 recovered keywords per product (added 2026-09-03, user decision)

Added after the blr-batch18 Sonnet test and the blr-batch11 review: with 10–15 sacrificed
keywords per product, writers of every model end up gluing near-identical phrases together
("an outdoor cat repellent and animal repellent") to satisfy the second net, and the description
stops reading like copy. The keywords sacrificed by the title are therefore **capped**:

- Of the keywords the title could not capture (volume ≥ 1,000, product-fit passed), only the
  **top 8 by volume** are the second net that must appear in the description. Ties are broken
  by which phrase describes the product better, then by fewer characters.
- The remainder is rejected automatically with the written reason "second-net cap" — it stays in
  `rejects.json` (field `capped`) so nothing is lost or invisible, but it carries no obligation.
- Word-order / singular-plural twins of a keyword already inside the 8 do not count as new
  entries: the checker collapses them first, so the 8 are eight distinct query families.
- The writer may still use a capped keyword when it fits naturally; it is never required, and
  the natural-placement rule and the alias-list ban apply exactly as before.
- Title keywords (rule 1) are unaffected: every captured title keyword still appears in the
  description, inside the head.

`title-check.py` emits the capped list and runs the second-net check only over the 8.
