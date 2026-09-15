# "Right for you if" block — brief Q19 (optional per batch)

User decision 2026-09-06 (now applied to Tuzwa). A short block that tells the shopper this product is for them. It speeds up the right
buyer — expected effect: CVR neutral to slightly positive. Most useful on products with a fit / size / expectation risk
(beds, apparel, cases, furniture); adds nothing on consumables and one-size accessories, so the writer may opt out per
product.

**Revision 2026-09-06 (user decision, after the blr-batch26 test product):** the block is ONE column — "Right for you if"
only. The former right column "Not the right fit if" (`not_for`) is removed entirely and is never written again; a wrong
"not for" line kills a sale silently and is never seen. The block also moved: it now sits directly before `<h3>FAQs</h3>`
(it used to sit before Key Features, after the comparison block). The comparison block stays before Key Features (user
decision, same day: the table persuades early, the fit block closes the decision late). Line count fixed at exactly 4.

**Revision 2026-09-07 (user decision, conversion pass):** the old block described the reader ("You want a portable comfort
item") but gave no reason to believe the product delivers, and stopped dead before the FAQs. Three changes: (a) every
line is now `situation — proof` — the buyer's situation, an em dash, then the source fact that answers it; (b) no
generic-audience line ("someone of any age", "anyone who…") — a line for everyone persuades no one; the fourth line is
the strongest concrete use moment or gift intent instead; (c) fit_build.py renders a fixed closing sentence under the four
lines — **If two or more of these sound like you, this is the one.** — so the block closes the decision instead of
dropping the reader into the FAQs. Unchanged: exactly 4 lines, one column, no `not_for`, position before FAQs.

```
Q19 — Fit block: (Add fit block / Skip fit block)
```

Unanswered = Skip. `brief_flags.json` carries `"q19_fit_block": true|false` (README step 1). fit_build.py,
struct-check.py, verify.py and gate.py read that one flag.

## What the block is

`<div class="vp-fit">` — a single column: navy heading **Right for you if**, exactly 4 green circle-tick lines, then the
fixed navy closing sentence. Same colours, radius and border as the comparison block (comparison-table-rule.md). Rendered
by `fit_build.py` from the description agent's `fit` object — the agent never writes the HTML and never writes the closing
sentence. Position: directly before `<h3>FAQs</h3>`, i.e. after Specifications, Package Includes, How to Use and the
remaining description images.

## Content rules (the agent's part — the `fit` object)

1. **`for`: exactly 4 lines, 30–110 characters, each `situation — proof`** (4 fixed on 2026-09-06; the proof half added
   2026-09-07, both user decisions). Left of the em dash (` — `, exactly one per line): the buyer's own situation, written to
   the reader. Right of it: the source fact that answers that situation — a number, a spec, a named feature — in the
   source's words. Examples:
   `You want something weighted to hold in stressful moments — 1.2 lb of soft weight`,
   `Your cat likes a covered, enclosed spot — the tent roof closes on three sides`,
   `You have a small dog — size L is 22.4 × 14.6 in`,
   `You are buying a gift that gets used every night — weighted plush comfort, not shelf décor`.
   The situations come from the source's use cases, audience, season, sizes, care — the same material as the benefit
   bullets, but phrased as *who you are*; the proof is what makes the line believable. A situation the source cannot
   back with a fact is not written. A product that cannot fill four honest `situation — proof` lines opts out per rule 4.
2. **No `not_for`.** The fit object carries only `for`. fit_build.py ignores a `not_for` key and prints that it was
   dropped; struct-check and verify.py fail a block that still shows the "Not the right fit if" column.
3. **Nothing beyond the source.** fit_build.py checks the whole line AND the proof half for a content word found in the
   extract (the same floor as the comparison rows), every number in a line for presence in the source, and rejects
   comparison wording (`unlike`, `ordinary`, `cheaper`, `other brands`, `than most`). assume_check.py runs over the
   rendered text; the 6c review by eye reads the lines with the bullets.
4. **No generic audience (2026-09-07).** `any age`, `anyone`, `everyone`, `everybody` FAIL in fit_build.py. "Someone of any
   age who could use comfort" is the line it replaces: it covers everyone and convinces no one. Write the concrete moment
   the source names instead (gift, bedtime, travel, a cold room).
5. **Opt-out per product:** `"fit": null` + `notes_for_log` containing `fit: not applicable`, for a product where the
   block would only repeat the bullets (a consumable, a one-size accessory). fit_build.py FAILs a null without the log
   line, so the omission is always visible in the run log.
6. Safety Notes apply; the brand name is never written in a line; nothing is written in the block that is not also
   true in the description. The proof half is a fact, never an outcome claim (no "relieves anxiety", "calms you down" —
   Backend doc Safety Notes).
7. **US units only (user decision 2026-09-11, same rule as comparison-table-rule.md rule 8).** A measurement in a line
   is shown in inches / feet, oz / lb, fl oz, °F — never metric, never a dual pair. The agent may write the source's own
   figure (the source checks run on the agent's text); `fit_build.py` passes every line through
   `unit_dual.imperial_only()` before the length check and the render, so `size L is 57 × 37 cm` reaches the page as
   `size L is 22.4 × 14.6 in`. The metric value still stands in parentheses in the Specifications list.

## Format rules (the script's part)

- Inline styles only; theme colours navy `#000096`, green `#2e9e4f`, border `#e3e3e3`; block words are outside the
  description word budget (struct-check strips it).
  **Colour provenance — measured on Tuzwa 2026-09-12.** Navy `#000096` (and the light `#f4f4f4` the comparison block
  uses) was read from Tuzwa's live MAIN theme ("Xtra -- NEW", `gid://shopify/OnlineStoreTheme/161796391136`), file
  `config/settings_data.json`, default scheme `scheme-1`: navy is that theme's `buy_button_color`, identical to
  `scheme-1`'s `primary_button_bg` (the Add-to-cart button); light is `scheme-1`'s `secondary_bg` (the light section
  band). Contrast measured on these values: white on navy 14.6:1, navy on light 13.3:1. This is Tuzwa's confirmed
  value and `fit_build.py` renders with it. Theme reads go through the **Shopify connector**, which has
  `read_themes`; the custom app used by the script route does not, and `tuzwa.com` is blocked by the container's
  egress proxy (403 CONNECT) — fetch, push and verification stay on the script route. If the theme or its default
  scheme changes, read the theme file again through the connector and update this rule doc AND `compare_build.py` /
  `fit_build.py` / `dim_image.py` together, in one change. See the colour-provenance block in
  comparison-table-rule.md.
- Closing sentence: fixed text `If two or more of these sound like you, this is the one.` in a navy bold `<p>` under the
  list, inside the column. Script constant `CLOSE` in fit_build.py — changed only there, never by an agent.
- struct-check: exactly one block when Q19 = Add and `fit` is not null, none otherwise; directly before `<h3>FAQs</h3>`;
  no "Not the right fit if" text; closing sentence present. verify.py: the same count, position and one-column condition
  live (check "fit block").
- Re-runs replace an existing block; with Q19 = Skip the script removes any block it finds.

## Cost

Four short lines from the same agent pass that writes the bullets — no extra agent, no extra round; the HTML and the
closing sentence are script. Same order of cost as the comparison table; the 2026-09-07 revision adds no step.
