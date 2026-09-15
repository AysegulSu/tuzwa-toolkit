# Comparison Table — "Tuzwa vs Others" block in every product description

User decision 2026-09-06 (now applied to Tuzwa). A comparison block answers the shopper's "why this one and not the cheaper one?"
without leaving the page — a CVR element for Google Ads traffic.

## Brief question Q17 — optional per batch (user decision, same day)

```
Q17 — Comparison table: (Add "Tuzwa vs Others" table / No table)
```

- **Add table** → every description in the batch carries the block; a description without it is not finished
  (compare_build.py, struct-check.py and verify.py all fail).
- **No table** → nothing is added; a block already present in a re-run product is removed; the `compare` object is not
  required in final/dNN.json. **A brief that does not answer Q17 runs as "No table"** — the safe default, nothing new
  is written to the store.
- Mechanics: at session start (README step 1) the main context writes `brief_flags.json` in the work dir —
  `{"q17_compare_table": true}` or `false` — from the brief. compare_build.py, struct-check.py and verify.py read that
  one file (`compare_build.q17()`), so the three gates always agree. DESC-SPEC tells the description agents whether to
  write the `compare` object; the main context states Q17's value in the run log.

## What the block is

A fixed-format HTML block rendered by `toolkit/compare_build.py` — the description agent never writes its HTML. The
agent supplies only the CONTENT (the `compare` object in final/dNN.json, schema in DESC-SPEC.md); the script renders,
inserts and checks it. Zero model tokens for the markup; the only added agent output is a short name and five short
rows (~5–10 % more output per product, no extra agent call, no extra round).

```
┌ Why choose Tuzwa ─────────────────────────────────────────┐   ← heading, fixed, navy band, line 1
│ Fleece Cat Tent Bed                                        │   ← product name, navy band, line 2 (13px, .85 opacity)
│ FEATURE                               │ Tuzwa   │ Others   │   ← header row, light blue, ONE line
│ Arctic fleece lining for winter warmth   │  ✓   │   ✘      │   ← product row 1
│ Removable, washable cushion              │  ✓   │   ✘      │   ← product row 2
│ Adjustable semi-closed entrance, snap buttons │ ✓ │ ✘      │   ← product row 3
│ Anti-slip bottom keeps the bed in place  │  ✓   │   ✘      │   ← product row 4
│ Two sizes, M and L, for cats and small dogs │ ✓ │ 1 size   │   ← product row 5 — the neutral one
│ 30-day easy returns                      │  ✓   │ Varies   │   ← store row, fixed, last
└───────────────────────────────────────────────────────────┘
```

Position: immediately before `<h3>Key Features</h3>` — after the last prose paragraph (and the first image). The
shopper has read the benefits and the customer scene; the table closes the "why this one" question before the spec
sections.

## Content rules (the agent's part — the `compare` object)

1. **`name`** — a 2–5 word short product name, no brand (the template prefixes "Tuzwa"). Built from the title's head
   noun and its defining attribute: `Fleece Cat Tent Bed`, `Heated Massage Gun`, `Wedge Pillow`. Never the full title.
2. **Exactly 5 product rows.** Each row is a source fact (extract facts / specs / package) written as what the shopper
   gets — the problem a cheap version leaves them with, solved: `Thick padded walls that stay warm`, `Cover zips off and
   washes`, `Holds the incline, no sliding`. 20–60 characters. The five rows are chosen like the five benefit bullets
   (description-format-rule.md §2 "Which five benefits"): the reasons a shopper buys, not secondary features, pack
   counts, aesthetics or variant facts — with one exception, the neutral row below.
3. **Nothing beyond the source.** A row exists only when the extract states the fact. `Holds its shape for years` needs
   a source line about the filling or structure; `Pet-safe fabric` needs the source to say it.
   assume_check.py and compare_build.py's source-trace check run over the rows; the 6c benefit review by eye reads
   the five rows together with the bullets.

   **Thin source — still five rows, still nothing invented (user decision, 2026-09-06).** When the source does not
   carry five decisive problem-solving facts, the five are completed from what the source DOES carry, in this order:
   (a) mine every source part — facts, specs, package, variants, how-to-use, FAQ (text only: the agents do not see
   images, so text printed on a source image is NOT available and is never assumed — corrected 2026-09-06); (b) write each part as the
   shopper's problem without going past the word's own meaning: `removable cushion` → `Cushion comes out and washes`,
   `snap buttons` → `Entrance opens or closes with snaps`, `anti-slip bottom` → `Stays where you put it` — `fleece`
   never becomes "keeps warm" unless the source says warm; (c) a part that yields no problem sentence becomes a NEUTRAL
   row (rule 5), with the Others cell a short phrase instead of ✘: `Two sizes, M and L / 1 size`, `Cushion included /
   Varies`, `Three colours / Varies`. A strong source therefore gives 4–5 problem rows + 1 neutral; a thin source gives
   2–3 problem rows + 2–3 neutral — always five, every row true. Only a source with fewer than five separable parts at
   all cannot fill the table; that product is logged (`notes_for_log`: "compare: source too thin") and left without a
   block — compare_build.py accepts an explicit `"compare": null` for that case only.
4. **No comparison wording inside a row.** The Others column IS the comparison. A row never says `than`, `unlike`,
   `ordinary`, `cheap`, `other brands`, `most cat beds` — those are the same sentences DESC-SPEC item 4 bans in
   bullets, and compare_build.py fails them. The row states our fact; the ✘ says the rest.
5. **When in doubt, neutral, not ✘ (added 2026-09-06).** "Others ✘" says the alternative lacks the feature — an
   unprovable claim about unnamed products. It is acceptable for a feature the cheap version of this product type
   plainly lacks (a removable cushion, snap-adjustable entrance); for anything a typical alternative might also have,
   the cell is a neutral phrase (`Varies`, `Thinner`, `Basic`). Two or three neutral cells out of five is normal and
   reads as more credible, not less.
   **The Others cell** is `✘` or a short neutral phrase (2–14 characters) that shows the alternative offers something,
   only less: `1 size`, `Varies`, `Thinner`, `Hand wash`, `Fixed angle`. **At least one of the five product rows is
   neutral, never ✘ on all five** (user decision: a table where we win everything is not believed). The neutral row is
   preferably a fairly comparable attribute — sizes, thickness, adjustability — and never invented about competitors.
   A neutral row also carries the plain facts that make no problem sentence (sizes, colours, what is in the box) — the
   thin-source path in rule 3 — so a table can be honest AND full.
5b. **Conversion tightening (user decision 2026-09-07, after reviewing the Weighted Koala Plush table live).**
   The table converts when it reads "you are not taking these risks", not "we win everything". Three consequences:
   - **Others cell: name the shortfall, do not just cross it out.** The default Others cell is a short concrete phrase
     that says what the cheap version gives instead — `Unweighted`, `Bulky`, `Rougher fabric`, `Hand wash`, `1 size`.
     `✘` is kept for at most 1–2 of the five rows, only where the cheap version of this product type plainly does not
     have the feature at all. Four ✘ in five rows (the Koala table as first pushed) is the pattern to avoid — it reads as
     an ad, and every ✘ is an unprovable claim. `Varies` stays the fallback when nothing more specific is true.
   - **Rows are written from the shopper's situation, not the spec sheet.** `Weighted to calm and settle you at
     bedtime` beats `Weighted for a comforting, hug-like feel`; `Small enough to bring in a bag or car` beats
     `Portable size`. The row = the shopper's fear + our answer; the Others cell = what that fear looks like in the
     cheap version. Still nothing beyond the source (rule 3) — the situation is drawn from the source's own use case,
     never invented.
   - **No empty rows.** `Suitable for all ages`, `Realistic look`, `Ultra-soft fabric` are aesthetics or generic —
     they persuade nobody. When the source offers a concrete number or fact instead (weight, size, washing), that
     fact is the row, as a neutral row if it makes no problem sentence (`Weighted 1.2 lb / Varies`).

   Reference example (Weighted Koala Plush, same source facts):
   `Weighted to calm and settle you at bedtime / Unweighted` · `Soft plush that stays gentle on skin / Rougher fabric` ·
   `Small enough to bring in a bag or car / Bulky` · `Realistic koala face and ears / ✘` · `Sized for kids and adults
   alike / Varies` — one ✘, four concrete or neutral cells.
   Applies to every batch from 2026-09-07 on. Not applied retroactively to already-pushed products (user instruction:
   rule only, no product update).
6. **The store row is fixed** — `30-day easy returns` / `Varies` — written by the script, always last. It is not part
   of the five.
   **CONFIRMED for Tuzwa by the user (2026-09-12)** — the window is 30 days for Tuzwa too, so the row stands exactly
   as written. It is a promise printed on every product page, so it must be re-confirmed with the user whenever the
   store or its returns policy changes rather than carried over silently.
7. **Safety Notes apply** to the rows exactly as to bullets: comfort language, never a medical outcome; pet/child
   products keep supervision wording in the description, not in the table.
8. **US units only in the table (user decision 2026-09-11).** The store sells only in the USA and the copy is written
   for a US shopper, so a measurement in a row, an Others cell or the product name is shown in inches / feet, oz / lb,
   fl oz and °F — never in cm, mm, m, g, kg, ml, l or °C, and not as a dual pair either (a "(155 cm)" parenthesis does
   not fit a 20–60-character row). Found live on the ddl2 pregnancy pillow: the table read `155 x 75 x 60 cm`; it must
   read `61 x 29.5 x 23.6 in`. Mechanics: the agent may write the source's own figure and unit (the traceability and
   number-in-source checks run on what the agent wrote, against the source); `compare_build.py` then passes name, rows
   and Others cells through `unit_dual.imperial_only()` before rendering — metric converted to imperial, the metric
   figure dropped, imperial text left untouched, the same exemptions as the dual pass (4G/5G, "L" as a length label,
   waterproof mm ratings, liquid oz). The 20–60 length check runs on the converted row, which is what the shopper sees.
   The metric source value still stands verbatim, in parentheses, in the Specifications list (description-format-rule.md
   §5), so value_check / spec_cover are unaffected. Idempotent — an imperial row is returned unchanged, and
   `parse_block()` + re-render applies the rule to a live block without touching the rest of the description.

## Format rules (the script's part — do not vary)

- Markup: `<div class="vp-compare" …>` heading band + `<table>`; inline styles only (the theme's CSS is not relied on;
  `descriptionHtml` keeps inline styles). Colours: navy `#000096` for the heading band and the Tuzwa column, light
  `#f4f4f4` (the header band) for the header row, green `#2e9e4f`
  circle-tick for our column, grey text and a pale grey ✘ for Others. White
  background, 12 px radius, 1 px `#e3e3e3` border.
  These are the working values, they are what `compare_build.py` renders, and they are Tuzwa's own measured theme
  colours.
  **Colour provenance — measured on Tuzwa 2026-09-12.** Navy `#000096` and light `#f4f4f4` were read from Tuzwa's
  live MAIN theme ("Xtra -- NEW", `gid://shopify/OnlineStoreTheme/161796391136`), file
  `config/settings_data.json`, default scheme `scheme-1`: navy is that theme's `buy_button_color`, identical to
  `scheme-1`'s `primary_button_bg` (the Add-to-cart button), and light is `scheme-1`'s `secondary_bg` (the light
  section band). Contrast measured on these values: white on navy 14.6:1, navy on light 13.3:1 — both far above the
  4.5:1 floor.
  **How the theme was read, and the route to use next time:** theme reads go through the **Shopify connector**, which
  has `read_themes`. The custom app used by the script route does NOT have `read_themes`, and `tuzwa.com` is still
  blocked by the container's egress proxy (403 CONNECT), so neither of those paths can open a theme file. Everything
  else — fetch, push and verification — stays on the script route as before. If the theme or its default scheme
  changes, read the theme file again through the connector and update this rule doc AND `compare_build.py` /
  `fit_build.py` / `dim_image.py` together, in one change — never the doc without the three scripts, never a script
  without the doc.
  Retired history only: the PREVIOUS store's pair `#2c374d` / `#eef5f7` (Worfa, "Vault" theme, 2026-09-10) and the
  oldest store's light `#d2def6` (vepine.com, 2026-09-07). Those are not live constants anywhere and must not be
  reintroduced into the rule or the scripts. `#000096` is NOT retired — it is Tuzwa's live navy, measured above; it
  simply happens to match the Vepine-era navy.
  The green tick `#2e9e4f` is a fixed success colour, not taken from any theme, and is unchanged.
- **Value columns centred (user instruction 2026-09-07, after seeing blr-batch26 live).** The `Tuzwa` and `Others`
  header cells, every tick, every ✘ and every neutral phrase sit on one vertical centre line per column. The theme
  overrode the cells' inline `text-align:center` on the live page (ticks and "Varies" sat off-centre under their
  headers), so the script centres each value with a flex wrapper INSIDE the th/td (`display:flex;
  justify-content:center`) — theme text-align rules cannot move it — and gives th and td of a value column the same
  width (120 px) and padding so header and cells share one centre. The feature column and its header are pinned
  `text-align:left !important` the same way. `compare_build.parse_block()` reads name + rows back out of a rendered
  block (old or new template) so a template change is applied to live products by re-rendering, never by hand.
- Heading text fixed: `Why choose Tuzwa`, with the product name as the band's SECOND line (2026-09-10, below).
  Header cells: `FEATURE` · `Tuzwa` · `Others`. Store name written
  `Tuzwa` (capital T, rest lower case — user instruction 2026-09-06), never TUZWA.
- The store name appears ONLY inside this block. Everywhere else the standing rule holds — brand name never in
  title, copy, SEO fields, alt text. gate.py and verify.py strip the block before their brand scan; a `Tuzwa` outside
  it is still a FAIL.
- **Mobile (user instruction 2026-09-10, from a live phone screenshot).** The old template gave the two value columns a
  fixed 120 px each; on a 360 px phone they ate 240 px and left ~100 px for the feature text, so `Looks and works like a
  real charger` broke into five lines and the block ran ~1400 px tall. Four changes, largest effect first:
  1. **The product name left the header row.** It is now the second line of the navy band (13 px, `opacity:.85`), under
     `Why choose Tuzwa`; the first header cell is the single word `FEATURE` (12 px, uppercase). The light-blue header
     row is one line instead of a five-line product title.
  2. **Value columns are percentages** — Tuzwa `width:14%`, Others `width:24%` — with `padding:10px 4px`. That returns
     ~90 px to the feature column and drops every row to at most two lines.
  3. **`table-layout:fixed`** so the theme cannot redistribute the columns by content, plus `max-width:none;margin:0` on
     the `<table>` — the theme's own table margin was leaving a ~35 px gap at the card's right edge.
  4. **Type down one step**: table 14 px, row padding 10 px, Others cells 12 px / `line-height:1.25` and allowed to wrap
     (`Blurry footage` over two lines is fine and reads correctly, because the flex wrapper also carries `text-align:center`).

  Measured after the change: a 328 px block gives 186 / 54 / 86 px columns and ~560 px of height instead of ~1400 px.
- **Desktop (same day).** Percentage columns with no cap made the opposite problem: in a 1470 px theme container the
  feature column became ~1300 px, the ticks stranded at the far right with an empty plain between, and `Weaker output`
  still wrapped at 78 px. The fix is a cap on the block itself — `max-width:680px` on `div.vp-compare`, left-aligned
  (the rest of the description is left-aligned, so no `margin:auto`). At 680 px the columns measure 406 / 103 / 171 px
  and Others phrases sit on one line.
  **`clamp()` does not work here** — it was tried first (`width:clamp(78px,14%,150px)`) and the browser ignores a
  `clamp()` column width under `table-layout:fixed`, splitting the table into three equal columns (measured with
  Playwright, 2026-09-10). Percentages are what holds. Percent-only columns without the 680 px cap are also rejected:
  they give the mobile gain back at desktop width. A separate desktop stylesheet is not an option — a `<style>` block
  inside `descriptionHtml` is stripped by some themes; inline percentages plus the cap survive.
- The block's words are not part of the description word budget (struct-check.py excludes it); the block is mandatory
  (struct-check: exactly one, directly before `<h3>Key Features</h3>`).
- **Units: imperial only** (rule 8) — applied by the script at render time, never by hand.

## Where it runs

- Step 6 (descriptions): the agent writes the `compare` object; `gate.py` calls `compare_build.py` first, which renders
  the block into final/dNN.json (idempotent) and FAILs on: missing object, name not 2–5 words, brand inside name, row
  count ≠ 5, row length outside 20–60 (measured after unit conversion), no digit-only / spec-only row, comparison
  wording, Others cell malformed, all five ✘, a row with no content word found in the extract, a number the source
  never states (checked on the agent's own text, before conversion). Every later gate runs on the rendered HTML.
- Step 6c (benefit review by eye): the five rows are read together with the H2 / bullets / CTA lines — the same test:
  is this a reason to buy, and does the source say it. The run log names corrected products or states "read on all N".
- Step 8 (verify.py): check 15 ignores the block for the brand scan; check 17 confirms exactly one block is live.
- Re-runs over already-pushed products: compare_build.py replaces an existing block, so a description is never given a
  second table. Products pushed before 2026-09-11 that show a metric row are fixed by `parse_block()` → `render()` on
  the live description (the rows are converted at render), then a descriptionHtml-only push + verify.py.

## Why not a separate step / agent

The rows are five short lines about facts the agent has already read to write the bullets; asking for them in the same
pass costs a few dozen output tokens per product. A separate agent or round would re-read the whole product context for
the same five lines. The HTML is fixed, so it is generated by script, not by a model.
