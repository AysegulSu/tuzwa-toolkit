# Product Title Format — Q9 Custom Format

The user's own title format. When the brief answers Q9 with "I'll specify my own", this
document IS the format. It replaces the "Use default format" title rules in the Backend
Update Document (whose "title under 60 characters" limit does NOT apply here).

Updated 2026-08-29: data source moved from Semrush to DataForSEO; tiered character
structure (70–120 / 135 / 145) and the CPC tail zone added — all approved by the user.

Updated 2026-09-05: opener identity clause added to §3 rule 2 (the opener must name the
product's own type, not a parent category), the product-type lookup requirement in §1, and
the title / productType / category consistency rule in §10b — all approved by the user after
the blr-batch21 door-knocker review. Same day: §5 "measured specs are keywords" — a numeric
attribute enters the title when it is searched (≥ 1,000) or purchase-defining.

Updated 2026-09-05 (evening, user decision): **§8 catalog-level uniqueness suspended in full** — 8.1
(first 40 chars unique) and 8.2 (60% overlap), including the in-batch ov.py pair check. No title is
built, changed or reported for uniqueness/overlap until the user re-issues the rule at catalog end.

Updated 2026-09-05 (later the same day): the "typical member" exception in §3 rule 2 replaced by the
**head-noun test** — the opener's last word must be the product's own last word (plural or listed
synonym). No judgment, no grey list. User decision after the cat-hammock review (`Cat Beds` had opened
a hammock). §10b follows the same test.

Updated 2026-09-05 (user decision, blr-batch23 audit): **§3 rule 2 opener checks are now push-blocking in
`title-check.py`** — an unmeasured opener phrase, or a higher-volume fitting keyword sitting behind the opener,
is a FAIL, not a manual note. Six of 49 blr-batch23 titles had gone live against rule 2 under the old warning.

Updated 2026-09-05 (user decision): **the source title's own keywords are always measured** — §1
last bullet. The existing title is a working title; its phrases go into the same DataForSEO call as
every other candidate, and the ones that carry volume compete for slots on equal terms.

Updated 2026-09-06 (user decision, option b): **unused higher-volume keywords need a written reason** — §3 rule 2; a
measured, fit-clean candidate that beats the weakest non-opener cluster is a FAIL unless `skip_reasons.json` says why.

Updated 2026-09-06 (user decision): **the new title never captures less product-naming volume than the old one** — §2,
push-blocking in `title-check.py` (blr-batch24 #35 would have failed: 96,460 → 15,060).

Updated 2026-09-06 (user decision, same audit): **every cluster has a measured core** — §2. A comma cluster with no
measured 2+-word phrase inside it is a push-blocking FAIL in `title-check.py`; attributes and for/with tails stay free.

Updated 2026-09-06 (user decision, blr-batch24 source-title audit): the §1 source-title split is now done by
**`toolkit/source_windows.py`**, not by the extraction agent — every contiguous 2–4-word window of every source
title is measured, no judgment. The audit found 386 such windows unmeasured in blr-batch24; `essential oil
diffuser` 74,000 was among them while the title had opened on `aromatherapy diffuser` 14,800 (a rule 2 miss).

Updated 2026-09-12 (user decision): **measurements in the title are US units only** — §5 "Units in the title".
The store is a US store and its customers search in inches, feet, ounces and pounds; a metric unit (cm, mm, m,
g, kg, ml, l) never appears in a title, the value is converted. Push-blocking FAIL in `title-check.py`.

---

## 1. Keyword data source — DataForSEO (Google Ads data)

Pull keyword data from the **DataForSEO API** before writing any title. Never write a
title from assumption — **every word in a title that is meant to carry search value must
have been looked up first.** Inserting a plausible-sounding phrase without checking it is
a process failure, even when the phrase turns out to be real.

- Endpoint: `POST /v3/keywords_data/google_ads/search_volume/live`
  (`location_code: 2840` = US, `language_code: "en"`). Returns exact Google Ads volume,
  competition (LOW/MEDIUM/HIGH), and CPC per keyword.
- Up to 1,000 keywords per task (~$0.06 standard queue / ~$0.09 live). Batch a whole
  category's candidates into one call. Cache every result in the project
  (`kw-cache-*.md`) so re-runs cost nothing.
- `api.dataforseo.com` is on the sandbox allowlist since 2026-09-02 — call it directly
  from the container with `curl`. Credentials and the standard call live in
  `dataforseo-credentials.md` (saved at the user's request); read them from there,
  never echo the password into chat or logs. (Before 2026-09-02 the firewall blocked the
  host and calls went through the user's browser — see older kw-cache docs.)
- Semrush (`phrase_related` / `phrase_these`) and Google Keyword Planner remain fallbacks.
  GKP shows only volume bands unless the account has qualifying Search spend; the
  sort-on-volume trick gives exact *ranking* even when values are banded.
- **The product's own type name is always measured** (singular and plural — `door knocker`,
  `door knockers`, `kitchen tongs`), whether or not the extraction agent listed it as a
  candidate. blr-batch21 #01 was titled `Halloween Decoration …` partly because `door
  knocker` had never been looked up, so there was nothing to compare 135,000 against.
  (added 2026-09-05)
- **The source title's own keywords are always measured** (added 2026-09-05, user decision).
  The product's existing title is a title that already works, so its phrases are candidates by
  default: split the source title into its contiguous phrases (each cluster phrase, plus the
  2–3-word sub-phrases inside it) and add every one to the candidate list for the same
  DataForSEO call — no separate call, no extra cost. They are then treated exactly like every
  other candidate: measured, passed through the §6 fit gate, and placed by volume. A source
  phrase that carries volume keeps its place on merit; one that measures 0/null or below the
  gates drops and its slot goes to a better measured keyword. This adds candidates only — it
  never gives a source phrase priority over a higher-volume measured keyword (§3 rule 2 and the
  §10.2 trimmer lesson still decide the slots), and it never bypasses the fit gate.

  **The split is a script, not a judgment (added 2026-09-06, user decision).** `toolkit/source_windows.py`
  reads the Phase 1 snapshot and emits every contiguous 2–4-word window of every source title (plus the
  whole title), dropping only windows that start or end on a stop-word; the output is added to the
  candidate set before the DataForSEO call (README-toolkit.md step 4). Nobody decides in advance which
  window "looks like a query" — that decision is exactly what the extraction agent got wrong in blr-batch24
  (`essential oil diffuser` 74,000, `flip flops` 135,000, `coat rack` 49,500, `salt lamp` 27,100 all
  unmeasured). Measuring a window that turns out irrelevant (`christmas costume` 8,100 on a dog costume)
  costs a fraction of a cent and is then fit-rejected with its volume on record, per §6; not measuring a
  relevant one is an invisible rule 2 miss. Cost: ~400 extra keywords per 50 products, at most one more call.

**Selection criteria, in order:**

1. **Volume** — highest goes first
2. **Intent** — commercial and transactional qualify; informational and navigational are
   dropped, except in the final long-tail slot where a use-case phrase may be informational
3. **Competition / CPC** — at similar volume, lower competition and lower CPC win; these
   are also the deciding factors for the tail zone (section 4)
4. **Product fit** — see section 6. This is a gate, not a tiebreaker: a keyword that fails
   it is discarded before volume is even considered

---

## 2. The contiguous-phrase rule — the core mechanism

**A keyword only counts when its words appear in the title contiguously and in order.**
Scattering the words across the title does not capture the phrase.

- ✅ `Escape Proof Cat Harness` → captures `escape proof cat harness`
- ❌ `Escape Proof Adjustable Reflective Cat Walking Vest Harness` → captures nothing;
  the words are there but the phrase is not

This is why stacking adjectives in front of the head noun destroys coverage. Build the
title as a series of **complete phrases**, not as one long adjective pile.

**Every cluster has a measured core (added 2026-09-06, user decision, blr-batch24 audit).** Each comma-separated
cluster of the title must contain at least one measured 2+-word keyword — its core. The words around the core are
free: attributes before it (`Outdoor` in `Outdoor Fly Trap Bags for Horses and Barn`, core `fly trap bags` 2,900) and
the for/with tail after it. This is NOT a "measure every word" rule — that would turn titles into keyword lists,
which §3.7 forbids. It catches one specific failure: an agent taking a measured phrase and editing *inside* it until
it no longer matches any query. blr-batch24 #12: `robot vacuum for carpet` 2,400 was in kw.txt; the title carried
`Automatic Robotic Vacuum for Carpet and Hard Floor` — nothing in that cluster had ever been measured. Five of the
batch's 154 clusters were like this (`Funny Dog Xmas Outfit`, `RGB Color Changing Night Light`, `5 Piece Burr Set
for Drill`, `Oil and Protector`). `title-check.py` FAILs such a cluster (push-blocking); the fix is to rebuild it around
a measured keyword or to measure the phrase meant. Exempt: a cluster that is only a §5 defining number (`10 Pack`,
`Set of 4`). Apostrophes and word order are ignored when matching (§2: `yard christmas decoration` = `christmas yard
decoration`). Tail keywords are measured by definition (§4 gates), so this changes nothing for them.

**What is measured is not the number of phrases but the TOTAL CAPTURED VOLUME.** Write
few phrases, order their words so each phrase yields several searched keywords at once
(overlapping capture). Example with exact data: `Maxi Dresses for Women` (22 chars)
captures `maxi dresses` 165,000 + `maxi dress` 165,000 + `dresses for women` 135,000 +
`maxi dresses for women` 40,500.

### Overlapping phrases — one occurrence, several keywords

Order the words so a single occurrence of the head noun serves several keywords at once:
`Escape Proof Cat Harness and Leash Set` captures, from one `Cat Harness`:
`escape proof cat harness` · `cat harness and leash` · `cat harness and leash set`.

### The plural trick — free volume for one character

A plural head noun contains its own singular as a substring, so the plural form captures
**both** keywords (`Table Lamps` → `table lamps` and `table lamp`). Always check singular
and plural volumes; where the singular is larger, the singular is the head.

### Do not sum word-order variants

`heavy duty dog leash` and `dog leash heavy duty` are the same query to Google — count
once. Genuine synonyms may be summed.

### Resolving collisions

Two keywords that both need the same head noun adjacent to them cannot both be captured
without repeating the head noun. **The higher-volume one wins** (exact-data example:
`cashmere sweater` 74,000 beat `turtleneck sweater` 27,100 for the slot adjacent to
`Sweater`). On an exact volume tie, the more product-defining modifier wins. The losing
modifier can still appear elsewhere in the title as a selling attribute.

---

### The new title never captures less than the old one (added 2026-09-06, user decision)

The rewrite must be an improvement in the one number this document is built on. Once the source title's own
windows are measured (§1), the volume the old title captured is known; `title-check.py` compares it with the new
title's and FAILs when the old one captured more **product-naming** volume (keywords whose last word is the
productType head — the same test as §3 rule 2; fit-rejected keywords excluded on both sides). Parent-category
words in a supplier title (`washing machines` 201,000 on a shoe wash bag, `tennis shoe` 135,000) do not count —
that volume was never the product's to lose. blr-batch24 #35: old `Salt Lamp Diffuser - 3-in-1 Essential Oil
Diffuser` captured 96,460 on diffuser keywords; the pushed title captured 15,060, because `essential oil diffuser`
74,000 had been dropped. A drop in TOTAL volume (all keywords) is reported as a warning only.

---

## 3. Hard rules

1. **No brand name in the title.** Ever.
2. **HIGHEST-VOLUME KEYWORD ALWAYS FIRST. This is never changed, for any reason.**
   No modifier, no attribute, no cluster phrase opens the title ahead of it.

   **Opener identity clause (added 2026-09-05, user decision after blr-batch21 #01):**
   "highest-volume keyword" means the highest-volume keyword **that names this product's
   own type** — the §10b productType, its plural, or a direct synonym. A parent-category
   keyword never opens the title, whatever its volume. Test: *would someone typing this
   query be satisfied to see this product as the first result?*

   **Head-noun test (replaces the "typical member" exception, user decision 2026-09-05):** the
   opener's **last word** must be the same word as the product's own last word — singular/plural
   or a listed synonym. The product's own last word is the noun the supplier title, the spec table
   and the package line use for the product (a hammock, a knocker, a pair of tongs). If the last
   words differ, the keyword is a parent category: it may still go INTO the title (it keeps its
   volume) but it never opens it, whatever its volume. This is a script check (toolkit/head_check.py),
   not a judgment — there is no "typical member" ruling any more and no `opener` row in RULINGS.

   - Passes: shower speaker → `Portable Bluetooth Speakers` (Speaker = Speakers, 368,000).
   - Fails: cat hammock → `Cat Beds` (Bed ≠ Hammock); skeleton door knocker → `Halloween Decoration`
     (Decoration ≠ Knocker); tongs → `Kitchen Utensils`; heatless curlers → `Hair Styling Tools`;
     dog blanket → `Couch Cover for Dogs` (Cover ≠ Blanket); camera backpack → `Camera Bag` (Bag ≠
     Backpack); mosquito lamp → `Indoor Mosquito Repellent` (Repellent ≠ Lamp).
   - Attribute words may follow the head noun inside the opener segment (`Shower Caddy No Drill`,
     `Scar Tape Silicone Roll 1.6 x 59 in` — written in inches since the §5 unit rule); the test is that the product's own noun is the noun of the
     opener phrase. `Set`, `Kit`, `System`, `Pack`, `Tool` at the end of a productType are not the head
     (`Toilet Brush and Plunger Set` → plunger; `Apple Corer Remover Tool` → remover).
   - Synonyms that count as the same word (the list in toolkit/head_check.py is the master copy — extend
     both only with the user's approval): cam = camera · skillet = pan · portable charger = power bank ·
     cover = slipcover = protector = cap = sleeve · couch = sofa · torch = flashlight · weed eater = weed
     wacker = trimmer · repeller = repellent = deterrent · beanie = hat · sneaker = shoe = boot · earbud =
     earphone · purse = handbag · pants = trousers · insert = insole · holder = mount = stand = caddy ·
     light = lamp = sconce · coat = jacket = overcoat = raincoat · top = blouse = shirt ·
     jogger = sweatpants · squeezer = juicer · cane = stick · binder = belt · stopper = device · flusher =
     sensor · compressor = inflator · dispenser = holder · suit = swimsuit · remover = removal · tool =
     puller = weeder = head · wedge = sandal · band = headband · extension = extender · scratcher = pad ·
     watering = irrigation.

   **Script-enforced, push-blocking (user decision 2026-09-05, after the blr-batch23 audit):** `title-check.py`
   FAILS — not warns — a title on either of two opener conditions, and nothing is pushed until it passes:
   - **(a) the opener phrase is unmeasured.** The words from the start of the title up to and including the head
     noun must be a keyword that was looked up in DataForSEO (present in kw.txt, even at 0 volume), or must contain
     a measured keyword that ends on the head noun (`Car Scratch Remover Pen` carries `scratch remover pen`).
     Unmeasured openers that reached the store in blr-batch23: `Wall Art`, `Cordless Headphones`, `Rompers`,
     `Mens Jacket`. The fix is TITLE-SPEC step 1b — measure the phrase in the one extra DataForSEO call — never
     to push it unmeasured.
   - **(b) a higher-volume fitting keyword sits behind the opener.** Among the keywords the title captures that
     pass the head-noun test, the highest-volume one must lie inside the opener phrase (a tie is fine). If it sits
     later in the title, either it opens the title or it is fit-rejected with a written reason and leaves the
     title. blr-batch23: `presser foot` 2,400 opened while `sewing machine presser foot` 8,100 sat later;
     `womens suit set` 12,100 opened ahead of `tailored suit women` 18,100.
   Before this change the opener check was a MANUAL note that the title agent resolved itself; six of 49 titles
   went live against rule 2. The check costs no model tokens; `build_check.py` carries each product's §10b
   productType (producttype_draft.json) so the script knows the head noun.

   **Every slot, not only the opener — script-enforced with a written-reason escape (added 2026-09-06, user decision):**
   the §10.2 trimmer lesson ("every cluster slot goes to the highest-volume measured phrase that fits") is now checked.
   A measured, fit-clean candidate of >= 1,000 that is absent from the title and larger than the weakest non-opener
   cluster's value is a FAIL in `title-check.py` — unless the title agent writes a one-line reason for leaving it out
   (`skip_reasons.json`; the reason is printed in the run log). Legitimate reasons exist — a 4th head-noun occurrence,
   a length tier with no trigger, a word order that would break the opener — and the rule does not overrule them; it
   only refuses the silent version. "Sounded better" is not a reason.

   A parent-category keyword that passes §6 fit still goes INTO the title (it keeps its volume) — it
   just does not open it. A broad opener buys impressions on queries the product cannot convert, which
   lowers CTR and raises CPC in Shopping.
3. **Head Product Type right after** — the term that unambiguously identifies the product.
4. **As many further high-volume keywords as fit naturally**, each as a contiguous phrase.
5. **Long-tail phrase at the end** — use case, problem solved, or audience/context.
6. **Character count: tiered — see section 4.** Base range 70–120; 120–135 opens only on
   a trigger; 135–145 exceptional; **145 absolute ceiling** (safety margin under Google's
   150). Under 70 is a violation too — unspent base budget is unclaimed clusters. But
   never fill leftover space with a keyword that fails any gate.
7. **Natural language, no keyword stuffing.**
8. **No size and no color** unless that attribute is genuinely defining for the product.
9. **Never join two head nouns with "and" — use a comma.** (added 2026-09-04, blr-batch21)
   Two separate product names joined by "and" read as two products in one listing:
   ❌ `Automatic Cat Feeder and Automatic Dog Feeder, WiFi Smart Pet Feeder`
   ✅ `Automatic Cat Feeder, Automatic Dog Feeder, WiFi Smart Pet Feeder`
   The rule is about **head nouns only**. "and" stays wherever it joins something that is not a
   product name — audiences, surfaces, materials, seasons, components, features, contents:
   ✅ `for Men and Women` · `for Indoor and Outdoor` · `for Face and Neck` · `Lick Mat for Dogs and Cats`
   ✅ `with Heart Rate and Sleep Monitor` · `with Powder and Sponge` · `for Chocolate, Candy and Bath Bombs`
   ✅ `for Spring and Fall` · `with Heating and Cooling` · `for Curved and Irregular Surfaces`
   Test: if both sides of the "and" could each be sold as their own listing, it is two head nouns —
   comma. If one side only describes the other, or they share a head noun ("Scratching Pad and
   Board"), "and" stays. Applies to the product title and the SEO title alike; the comma costs the
   same or fewer characters, so it never breaks a tier.

### Skeleton

`[Top Keyword] [+ qualifier], [Cluster Phrase 2] with [Attribute], [Attribute] [Cluster Phrase 3], [Tail Phrase]`

Comma-separated cluster phrases, each one contiguous and complete. A guide, not a template.

---

## 4. Character tiers and the CPC tail zone

### Tiers

| Zone | When |
|---|---|
| **70–120** | Normal zone. Most titles end here. |
| **120–135** | Opens ONLY on a trigger: **(A)** a cluster keyword **≥ 20,000** volume that could not be built contiguously within 120, or **(B)** a tail keyword that passes the tail gates below. |
| **135–145** | Exception: a single additional ≥ 20,000 contiguous cluster does not fit by 135, or triggers A and B are both present and cannot fit together. **145 is the absolute ceiling — no exceptions.** |

An extension is legal only if the construction obeys every other rule. If adding the
big cluster would require an excessive head-noun repetition or unnatural reading, the
extension is DECLINED and the keyword is sacrificed (worked example: `waterproof
backpack` 27,100 refused because it needed a 4th "Backpack" occurrence).

The tail keyword's physical position in the title is flexible — capture is
position-independent; the tail keyword is what legitimizes the length, not what sits
after character 120.

### Tail zone purpose

Lower average CPC by adding eligibility for cheap, high-intent mid-tail queries.
Adding a tail term does not reduce CPC on existing queries; it shifts the traffic mix
toward queries with thinner competition (plus a small relevance/CTR benefit).

### Tail gates — in order (all must pass)

1. **Product fit** (section 6)
2. **Contiguous constructible** and fits the remaining budget without breaking the
   head-noun repetition cap
3. **Volume ≥ 1,000**
4. **Competition LOW or MEDIUM, OR candidate CPC below its cluster's median CPC.**
   (The relative-CPC arm matters: in apparel nearly every keyword is HIGH competition,
   so the median comparison is what usually opens gate B. Compute the median over the
   product's own candidate cluster. Example: slippers cluster median $0.95 →
   `funny slippers` $0.48 passes.)
5. **Commercial/transactional intent** (use-case phrasing allowed)
6. **Not a subset/repeat of an already-captured keyword family** — the tail must open a
   new query family

### Ranking among passers

Volume (desc) → tie: lower competition → lower CPC → fewer characters.
Use at most 1–2 tail keywords per title.

### Title rejects flow into the description (second net)

Every keyword sacrificed during title construction has a home: the product description.
Collision losers (`waterproof backpack` 27,100 refused a 4th occurrence), runner-up tails
(`cute slippers`), gate-passers that failed construction (`beach slippers`), and
below-median leftovers all get woven **naturally** into the description prose during the
Q7 rewrite. The title's matching claim is reinforced (title keywords all appear in the
description) and the value of what the title could not capture is recovered — at zero
title-budget cost. Product-fit still applies: a keyword rejected for fit (e.g. `shower
slippers`) stays out of the description too. Keep title keywords and recovered rejects
within the first ~500 characters of the description where feed truncation cannot cut
them.

---

## 5. Keyword vs. spec

A **keyword** is what people type. A **spec** is the number that proves the claim. Specs
belong in the description and bullet list, never in a title keyword slot
(`Waterproof` not `IPX7`, `Fast Charging` not `65W PD`). The replacement must be verified
too — run each candidate through the data source before trusting it.

### Measured specs are keywords (added 2026-09-05, user decision)

Google's own title guidance asks for defining numbers in some categories — pack count and
volume for consumables, capacity and model for electronics, dimensions for furniture — and
people search those numbers (`2 pack`, `16 oz`, `queen size`, `32gb`). A number is not banned
because it is a number; it is banned when nobody searches it. A numeric attribute may enter
the title when EITHER test passes:

1. **Measured:** the phrase it sits in has **≥ 1,000** DataForSEO volume (the same threshold
   as the tail gates) — `32gb flash drive`, `2 pack`, `queen size sheets`. Below 1,000 it stays
   a spec and goes to the description.
2. **Defining:** the product is sold by that number — pack count, volume, capacity, size —
   the numeric extension of §3 rule 8. No volume threshold, because a buyer cannot choose the
   product without it.

Either way: never in the opener (it follows the product name), never in place of a
searched word (`Waterproof` stays even when `IPX7` is also added), and written the way Google
formats it — `16 oz`, `2 Pack`, `Queen`, not `16OZ`/`2PCS`/`Q-size`. `IPX7` fails both tests
(140 volume, not a purchase-defining number) and stays out; `2100W` on a heater is a spec
unless the measured phrase carries it. Before this clause, batch titles already carried
`10 Pack`, `1 lb Pair`, `7 9 and 12 Inch` — those were correct under test 2; this clause makes
the practice explicit.

### Units in the title — US units only (added 2026-09-12, user decision)

The store is a US store and its customers use US units. **A measurement that enters the title is
always written in inch / ft / oz / lb (fl oz for liquids); it is never written in a metric unit.**
When the source gives cm, mm, m, g, kg, ml or l, the value is converted before it goes anywhere near
the title — `16 cm` → `6.3 in`, `1.5 m` → `59 in`, `500 ml` → `16.9 fl oz`, `2 kg` → `4.4 lb`.
Metric never appears in the title, not even as a second value in parentheses; the dual form
(imperial first, metric after) belongs to the description only (`unit_dual.py`).

- The conversion does not bypass §5 tests 1 and 2: the *converted* value still has to be measured
  (≥ 1,000 in the phrase it sits in) or purchase-defining. A converted value that comes out as an odd
  decimal nobody searches (`6.3 in`) usually fails test 1 and stays a spec in the description — that is
  the intended result, not a problem. Whole-number sizes people search (`12 inch`, `24 inch`) pass as
  before.
- Rounding: convert to one decimal, drop a trailing `.0` (`30.48 cm` → `12 in`, `4 cm` → `1.6 in`).
  Where the source itself already gives an imperial value, use that value as given — never re-derive
  it from the metric figure.
- Unit spelling follows the measured keyword (`12 Inch` when the keyword is `12 inch shelf`, `in` in
  a dimension pair `1.6 x 59 in`, `oz`, `lb`, `ft`).
- **Push-blocking:** `title-check.py` FAILs any title containing a number followed by `cm`, `mm`,
  `m`, `g`, `kg`, `ml`, `l`, `liter/litre`, `gram`, `meter/metre` or `centimeter`. The fix is to convert
  (or drop the spec to the description), never to push the metric value.
- The same rule applies to the SEO title.

Why: the title's job is to match what the customer types. A US shopper types `12 inch`, not
`30 cm`; a metric figure in the title captures nothing and reads foreign on a US listing.

---

## 6. Product fit — ABSOLUTE, NON-NEGOTIABLE

**A keyword that describes a different product NEVER goes in the title. No exceptions,
whatever its volume. Wrong Shopping matches are never acceptable.**

This is not a trade-off to weigh, an option to present, or a question to ask the user.
A keyword that fails this test is silently discarded — never offered as an "alternative",
never included in a variant for the user to choose from.

Rejected examples from real runs: `prong collar` (22,200) for an e-collar; `night light` /
`desk lamp` for a table lamp; `catnip toys` for a robotic cat toy; `hot pads` for a
trivet; `camping lantern` for a lamp; `shower slippers` (2,400, $0.51 — cheap AND
qualifying on every other gate) for EVA slides whose product data never mentions showers.

**Attribute sourcing.** Every keyword and attribute must come from the product's own
data — title, product type, tags, description, or specs. An attribute not verifiable
from the product does not go in the title. Never assume category-standard features.
When product data is unavailable, leave the attribute out — do not guess.

### Fit rejections are measured, never invisible (added 2026-09-01, ddl1-batch4)

The fit gate still decides what enters the title, but **every candidate keyword — including
ones expected to fail the gate — goes into the DataForSEO lookup.** A rejection made before
measurement is invisible: nothing in the run shows what it cost. In ddl1-batch4 the entire
GPS family of a kids' GPS tracker (`gps tracker` 60,500) was rejected at the candidate stage,
never measured, and the error surfaced only when the user challenged the pushed title.

Enforcement, every batch:
1. All candidates are measured; `fit_reject` entries keep their measured volume.
2. After titles are built, audit the rejects: any rejected keyword **≥ 20,000 volume, or larger
   than 50% of the product's captured volume,** is listed in the run log with its written reason.
3. A rejection that would remove the product's own **headline feature** — the leading words of
   the supplier title, or a capability the spec table itself lists — is not a fit rejection at
   all: it is an identity ruling, and the contradictory-identity procedure above applies
   (volumes pulled for BOTH candidate identities, evidence tally written out; in Manual mode
   the ruling is shown to the user before any title is built).
4. Evidence weighing: package contents and physical dimensions are strong identity evidence
   (a charging cable implies a rechargeable device; an 11 mm-thick case is not a coin tag).
   Two isolated spec lines do not outweigh the title, the gallery filenames, the package
   contents and the rest of the spec table combined — count the evidence on both sides, and
   remember boilerplate: suppliers paste spec lines between unrelated listings (ddl1-batch4:
   a foundation's "20 g" weight on a gift box; an item-finder's "CR2032/Bluetooth" pair on a
   GPS tracker).
5. An attribute or use the source states in plain words is usable, whatever a reviewer's
   instinct says (ddl1-batch4 #39: "suitable for running, cycling, walking" was in the source,
   so `running shoes` 301,000 belonged in the title). Caution is for what the source does NOT
   say — it never overrides what it does say.

**Product fit outranks the catalog-uniqueness rules (§8 — currently suspended in full).** Misrepresenting a product is
a §6 failure even when it is done to satisfy a formatting rule. When two near-identical
products must be told apart, differentiate on a genuine distinguishing attribute — never
by suppressing half of what the product actually is. If the only way to bring a pair
under the 60% overlap limit is to describe a product inaccurately, do not do it: re-cut
the differentiating cluster, or accept the overlap and report the pair. Report beats
misrepresent. Worked failure (blr-batch4): a camera whose own spec sheet reads *"Usage:
Indoor and outdoor"*, IP65, was titled `Wireless Security Camera Outdoor, …` purely so it
would not overlap the indoor-only camera in the same batch — the indoor half of the
product was dropped for a formatting reason. Added 2026-08-29 at the user's instruction.

### Contradictory product identity — resolve before keyword selection

When the source data disagrees with itself about WHAT the product is, the identity must
be settled before any keyword is looked up, and volumes must be pulled for BOTH candidate
identities before choosing. The extraction step's `notes` field flags these; it must be
read, not just the summary line.

Worked failure (ddl1-batch3 #4, 2026-08-31): the old supplier title and one line of body
copy said "eucalyptus rattan", while the feature copy ("mimic real olive branches"), the
package contents ("2 x Enchanted Olive Branches"), the spec colour ("Olive green"), the
spec material ("plastic", contradicting "rattan") and all five of the store's own gallery
image filenames said olive branch. The title was built on the eucalyptus wording, whose
best keyword was `eucalyptus garland` 3,600. `olive branch` / `olive branches` measures
**74,000 with LOW competition**. Captured volume went from 16,820 to ~105,900 once
corrected. The dominant evidence wins; the old supplier title is the weakest evidence in
the file and is precisely what the rewrite replaces.

---

## 7. Google Merchant Center compliance

- No promotional text — "free shipping", "sale", "best", "cheapest", "50% off"
- No ALL CAPS words; no excessive punctuation, emoji, or special characters
- Repetition of the head noun is acceptable when it builds a distinct cluster phrase —
  keep to two occurrences where possible, three when the captured volume justifies it
  (precedent: the makeup-mirror and cat-harness examples), never four
- Under 150 characters (the tier system in section 4 is already stricter)
- Attributes true to the actual product — never invent a feature

---

## 8. Catalog-level uniqueness — SUSPENDED (user decision 2026-09-05)

> **This whole section is out of force until the user re-issues it.** Neither 8.1 (first 40 characters
> unique) nor 8.2 (word overlap under 60%) is applied — not catalog-wide and **not in-batch either**:
> the in-batch `ov.py` pair check is no longer run, no opener or cluster is moved for a collision, and
> run logs do not report overlap pairs. Title construction follows §1–§7 and §10b only. The full rule
> text and the plan for the one-time catalog-end pass are kept in `claude/rule-overlap-deferred.md`.
> (Earlier state, 2026-09-04: only the catalog-wide check was deferred and the in-batch check still ran.)

---

## 9. Goals

Ranks highly in Google Shopping · Maximizes CTR and sales conversion · Lowers average
CPC via the tail zone · Highest-volume keyword at the front · Fits any product type ·
100% Merchant Center compliant · **zero wrong-product matches** · no duplicate-looking
titles in the catalog (goal kept; the §8 mechanism is suspended until catalog end).

---

## 10. Worked examples

(Examples in §10.1 use 2026-08 Semrush volumes; §10.2 uses exact DataForSEO volumes —
the current source.)

### 10.1 Semrush-era examples (mechanism unchanged)

- **Table lamp**: `Table Lamps for Bedroom, Cordless Table Lamp with Touch Dimming, Small
  Dimmable LED Bedside Lamps` — 97 chars, 7 matches ≈ 80K. Plural trick; `Cordless` beat
  `Rechargeable` for the adjacent slot; 23 chars left unused rather than spent on
  `camping lantern` (product fit).
- **Magnifying mirror**: `Makeup Mirror with Lights, Lighted Magnifying Mirror with
  Light, Rechargeable Wall Mounted Double Sided Mirror` — 110 chars, 7 matches.
- **Cat harness**: `Cat Harness and Leash Set, Escape Proof Cat Harness for Kittens,
  Adjustable Reflective Cat Vest for Walking` — the adjective-pile failure that produced
  the contiguous-phrase rule.

### 10.2 DataForSEO-era examples (exact volumes, tiers + tail zone)

**Fleece lined leggings — tail zone stays closed**

`Fleece Lined Leggings for Women, Thick High Waisted Leggings, Warm Thermal Leggings for Winter Cold Weather` — 107 chars, ~114,300:
fleece lined leggings 60,500 · leggings for women 22,200 · high waisted leggings 22,200 ·
thermal leggings 8,100 · lined leggings 1,300 (substring). Trigger A: none left ≥20K.
Trigger B: every candidate HIGH and above the cluster median → zone closed, title ends 107.

**Hiking backpack — trigger A declined by construction rules**

`Travel Backpacks for Women, Large Waterproof Hiking Backpack with USB Port, Nylon Laptop Backpack and Daypack` — 109 chars, ~188,500:
travel backpack 74,000 · hiking backpack 40,500 · laptop backpack 27,100 · travel
backpack for women 22,200 · backpacks for women 18,100 (substring) · daypack 6,600
(free single word). `waterproof backpack` 27,100 qualifies for trigger A but needs a 4th
"Backpack" → declined; `waterproof` stays as attribute. Category surprise: the product
is named "hiking backpack" but `travel backpack` is the true head (74K vs 40.5K).

**Puppy slippers — trigger B opens the zone**

`Slippers for Women, Funny Slippers with Cute Puppy Design, Non Slip Open Toe House Slippers, Indoor Outdoor Womens Slides for Beach` — 131 chars, ~80,000:
slippers for women 33,100/$1.50 · house slippers 22,200/$1.64 · womens slides
18,100/$0.91 · **funny slippers 6,600/$0.48 (tail)**. Cluster median $0.95; `funny
slippers` at $0.48 passes the relative-CPC arm → 120–135 legal. `cute slippers` (equal
volume, higher CPC) is the runner-up and cannot be captured simultaneously; `beach
slippers` passed the gates but failed construction (4th occurrence); `shower slippers`
failed product fit despite the best CPC.

**Cashmere turtleneck sweater — collision lesson**

Exact data showed `cashmere sweater` 74,000 vs `turtleneck sweater` 27,100 — banded data
had hidden this. Revised target: `Sweaters for Women, Cashmere Sweater, Oversized
Turtleneck Sweater, Soft Warm Knit Pullover Jumper for Winter` (~423K captured vs ~382K
in the first push).

**Skeleton door knocker — the opener identity clause (blr-batch21 #01, 2026-09-05)**

Pushed: `Halloween Decoration Skeleton Door Knocker, Gothic Skull Decor, Halloween Door Decor,
Skeleton Decoration for Porch` — opener `halloween decoration` 135,000, productType set to
"Halloween Decoration", category "Seasonal & Holiday Decorations". A person searching
"halloween decoration" does not expect a door knocker; the product is a sub-branch of that
category, and `door knocker` itself had never been measured. Corrected shape:
`Door Knocker Skeleton, Gothic Skull Door Knocker for Front Door, Halloween Decoration for
Porch and Outdoor Door Decor` — `halloween decoration` keeps its 135,000 inside the title,
`skull door knocker` 170 / `gothic door knocker` 210 become contiguous, productType and
category move to Door Knocker. Contrast: a shower speaker keeps `Portable Bluetooth
Speakers` (368,000, LOW) as its opener — it IS a typical portable Bluetooth speaker
(user decision, option A, 2026-09-05).

**Cordless grass trimmer — every slot goes to the highest measured phrase (TRIMMERYENI #08, corrected 2026-09-05)**

Pushed 2026-09-04: `Weed Wacker with Charger and Battery, 24V Handheld Weed Trimmer and Lawn Edger,
Lightweight Garden Tool for Small Yards`. The opener was right (`weed wacker` 90,500 beats
`cordless grass trimmer` 12,100 — §3 rule 2), but the second cluster was not: `weed trimmer` 9,900
was used while `cordless grass trimmer` 12,100 — measured, in the cache, product-fit clean — was left
out entirely, and `24V` / `handheld` carried no volume (`24v weed eater` 20, `handheld weed wacker`
720, neither phrase measured with "weed trimmer"). The run log had no reason for the choice: a
selection miss, not a ruling. Corrected (user decision): `Weed Wacker with Battery and Charger,
Cordless Grass Trimmer and Lawn Edger, Lightweight Garden Tool for Small Yards` — 116 chars, same
length, +12,100 (`cordless grass trimmer` 12,100 + `grass trimmer` 6,600 substring replace `weed
trimmer` 9,900). Lesson: **rule 2 is not only for the opener — every cluster slot goes to the
highest-volume measured phrase that fits; a lower-volume synonym never replaces a higher one, and an
unmeasured attribute (`24V`, `handheld`) never displaces a measured keyword.** Alt texts were
regenerated from the new title in the same push; SEO title/description unchanged.

**Salt lamp diffuser — the source-title window audit (blr-batch24 #35, 2026-09-06)**

Source title `Salt Lamp Diffuser - 3-in-1 Essential Oil Diffuser`. Pushed 2026-09-05: `Aromatherapy Diffuser,
Himalayan Salt Lamp Diffuser, Cool Mist Humidifier for Bedroom, 3 in 1 Essential Oil Warmer` — opener
`aromatherapy diffuser` 14,800. The extraction agent had listed `salt lamp diffuser`, `3 in 1 essential oil
diffuser` and `essential oil diffuser lamp` as candidates but not `essential oil diffuser` itself; a
window-by-window re-measure of all 50 source titles (368 unmeasured phrases, one $0.09 call) returned
`essential oil diffuser` **74,000** — the product's own noun, passes the head-noun test, five times the
opener. A rule 2 miss that no check could catch, because the keyword was never in kw.txt. This is why the
§1 source-title split became `source_windows.py`: the same audit found `flip flops` 135,000 (#36), `coat
rack` 49,500 (#29), `card holder` 60,500 (#08), `salt lamp` 27,100 unmeasured — most of those were already
captured inside the pushed titles and only under-reported, but #35 was a wrong opener.

## 10b. Product type (brief Q12)

"Use the keyword with the highest search volume" is filtered through the product-fit
gate: the product type is the **highest-volume keyword among those that accurately
identify the product** — never a higher-volume neighbor that mislabels it.
(Test product: "Turtleneck Sweater", not "Sweaters"; hiking backpack: "Hiking
Backpack", not "Travel Backpack".) Approved by the user 2026-08-29.

**Consistency (added 2026-09-05):** the title opener (§3 rule 2), the productType and the
Google taxonomy category all name the same product type — same last word under the head-noun
test. A parent category is never the productType (`Halloween Decoration` for a door knocker,
`Cat Bed` for a hammock fail exactly as they fail as openers). When the head-noun test changes a
product's opener, productType and category change with it in the same push.

## 11. Note on SEO title

This document covers the **product title** only. The SEO title (`seo.title`) keeps the
Backend Update Document's rule: under 70 characters, format
`[Product Name] - [keyword-rich descriptor]`.

## 12. Note on the project description

Where the Backend Update Document (project description) states "product title: under 60
characters" under Q9's default format, this document supersedes it for Q9 = "I'll specify
my own": the format is this document and the data source is DataForSEO (section 1).

---

## 13. Pre-push backup (added 2026-09-02 at the user's request)

Before any batch is pushed, the run must save a backup of what is being overwritten, as a
project doc named `backup-titles-<batch tag>.md`. Session workspace files are not a
backup — the container is discarded when the session ends.

Minimum contents, one row per product: index, product ID, handle, **old title**, **old SEO
title**, and the new title being pushed. The batch snapshot the run already fetches in Phase 1
is the source; no extra Shopify call is needed.

Write the doc BEFORE the Phase 2 push, not after — a failed or wrong push is exactly when the
backup is needed. If the user asks for a full backup, add old descriptionHtml, productType,
category, tags, status and variant prices as well; the title table is the default.

Precedent: ddl1-batch5 (`backup-titles-ddl1-batch5.md`). Batches 1–4 have no backup —
for those, Shopify's own product history is the only route back.
