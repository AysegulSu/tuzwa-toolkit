# Extraction spec (per product) — write extract/pNN.json

Read raw/pNN.json fully (descriptionHtml, title, productType, tags, category, variants with selectedOptions, media list incl. filenames of image urls).

extract/pNN.json fields:
- idx, id, handle, old_title, old_seo_title, old_seo_description, productType, category{id,name}, tags, status
- identity: one-line plain statement of WHAT the product is (head noun + defining attributes), based on the DOMINANT evidence (spec table, package contents, gallery image filenames, variants) — the old supplier/previous title is the WEAKEST evidence
- notes: any contradiction inside the source (two size sets, two capacities, materials disagreeing, "leather" only in a filename, boilerplate spec lines that belong to another product, plug types not matching variants). Write full sentences. Empty string if none.
- facts: EVERY product-specific fact from the source, unchanged: dimensions, weight, material, capacity, power, battery, frequencies, coverage area, colors, sizes, compatibility, modes, use contexts, target audience/animal, how-to-use steps, warnings. As a list of strings. Nothing thinned out.
- specs: list of {name, value} pairs exactly as in the source spec/attribute list
  **Completed by eye (added 2026-09-06, user decision):** after the script's pairs, add every MEASURABLE product value the
  source states only inside its paragraphs or feature lines and never in the spec table — capacity (mAh, oz, ml), power,
  runtime, charge time, dimensions, weight, magnification, LED count, colour temperature, ingress rating, material, number
  of modes/levels, pack count, compatibility range — as its own `{name, value}` pair in the source's own figure and unit
  (`{"name": "Battery capacity", "value": "1200mAh"}`). Rules: never a value already in the list (different unit of the same
  value is the same value); never an estimate, never a rounded or converted figure; a contradiction with the spec table is
  NOT resolved here — keep the table's pair and write the conflict in `notes`. Every pair becomes an item of the new
  Specifications list (spec_cover.py in gate.py enforces it), so a pair here is a line on the page.
- package: list of strings (Package Includes)
- how_to_use: list of STEPS / instructions only (do this, then that; charging, fitting, care steps) or [] — NEVER audience /
  occasion lines ("Ideal for…", "Perfect for…", "Great for…", "Best suited for…"): those go to `facts` as use contexts (2026-09-07,
  user decision — 9 products of STR-DUB-2-batch1 had them pasted under How to Use)
- usage_tips: pre-filled by `python3 usage_tips.py --extract` from the source's Usage Tips / Usage Recommendations / Tips block
  (every line, verbatim, in order); complete it by eye if the parser missed a line of that block; [] when the source has no such
  block. Every line becomes an item of our <h3>Usage Tips</h3> list (usage_tips.py in gate.py enforces it)
- sections (added 2026-09-08, user decision; rules/description-format-rule.md §7c): pre-filled by `python3 sections.py --extract`
  (run AFTER keyfeat_cover.py --extract and usage_tips.py --extract) — every OTHER headed block of the source that carries a
  product fact, as `{heading, heading_source, kind: "list"|"prose", lines: [...]}` in source order: Care / Cleaning, Warnings /
  Safety / Precautions, Materials, Design, Applications / Occasions, Compatibility, Storage, Charging / Battery, Installation /
  Assembly, Size Guide, Notes … `heading` is the CANONICAL name (the script's CANON list: Care Instructions, Safety Warnings,
  Materials, Design, Applications, Compatibility, Storage, Charging, Installation, Size Guide, Notes); `heading_source` is the
  supplier's own text; `lines` are the block's <li> lines (kind list) or paragraphs (kind prose), verbatim. Complete it by eye:
  (a) a block the parser missed (a heading written as a bold sentence, a block the script took for the description body) is
  added the same way; (b) a `"heading": null` entry ([UNMAPPED] in the script's output) gets the closest canonical name — or,
  when none fits, a 1–3-word title-case name of your own; (c) a block that is only marketing (no figure, unit, material,
  instruction, compatibility statement — "Elegance That Takes Off" over adjective sentences) is NOT a section: leave it out
  of `sections` (the script lists it in `sections_dismissed`); (d) a supplier-policy block (Shipping, Warranty, Returns, About
  Us) is never a section. Every line of every section becomes an item / paragraph of that <h3> section on our page in the
  writer's own words (sections.py in gate.py enforces it — missing line, pasted line, merged lines, invented section all FAIL),
  so a line here is a line on the page. A line that is also in `key_features` belongs to the section only — the script removes
  it from `key_features`; do not add it back. [] when the source has no such block.
- sections_dismissed: written by the script — the blocks it set aside `{heading_source, reason, lines}` (marketing-only → prose;
  supplier policy → never in copy). Read-only for you unless you move a wrongly dismissed block into `sections` (then delete it
  here). The run log carries the count.
- faq_source: existing Q/A pairs from the source if any (list of {q,a})
- images: list of {src, alt, position} for every <img> in descriptionHtml, in order
- media: list of {id, type, alt, filename}
- variants: list of {id, price, title}
- safety_flags: subset of ["kids","baby","pet","water","heat","blade","medical","electrical","chemical"] that apply per the Backend doc Safety Notes
- season_hint: one of winter/spring/summer/fall/evergreen with a 5-word reason
- key_features (added 2026-09-06, user decision): `python3 keyfeat_cover.py --extract` pre-fills this list by script with the
  source's own feature lines (its `<li>` and bold "Name:" lines outside the spec / package / FAQ sections). You then COMPLETE
  it by eye from the whole raw description: (a) add every source feature line the script missed — a feature written as a
  heading + paragraph, a plain paragraph list, a run-on sentence of features; (b) add every CONCRETE product feature that
  the source states only inside a paragraph and never lists — material, mechanism, function, mode, capacity, control,
  mounting, use setting (e.g. "combines mist output with LED lighting to create a flame-like visual effect" → `Flame-like
  LED effect: mist and LED light together create a flame-style glow`). Never add marketing sentences ("wraps you like a
  hug", "suits any mood"), never a spec line already in `specs`, never a package line, never anything the source does not
  say, and (2026-09-08) never a line that belongs to one of the `sections` blocks — that line's home is its section. Each entry `Name: one short sentence` in the source's words. The description agent must reproduce every entry as an
  item of the new Key Features list (keyfeat_cover.py in gate.py enforces it), so a line here is a line on the page.

  **Return format (added 2026-09-07, STR-DUB-2-batch1, user decision):** your reply carries one line per product,
  `NN | script key_features X | paragraph features added Y | prose spec pairs added Z | sections S` — and for every product with Y = 0 or
  Z = 0 a one-line reason ("the paragraphs restate the list", "no measurable prose value"). A 0 without a reason is sent back.
  `S` (2026-09-08) is the number of `sections` entries after your completion, followed by `+K` when you added a block the script
  missed or named an [UNMAPPED] heading (`sections 2+1`); `0` is valid when the source has no such block.
  In STR-DUB-2-batch1 45 of 48 products left this step with exactly the script's list and nobody could tell whether the
  paragraphs had been read; the main context now also runs `python3 para_feat.py` (zero tokens) over the paragraphs and
  adds what you missed, so an unread paragraph shows up in the run log either way. Your Y and Z are MEASURED by
  `extract_check.py` against the script baseline — a claimed count that differs from the real one, or a 0 without a
  reason, sends the product back to you.

candidates/cNN.json: {"idx":N, "candidates":[...]} — 40–70 keyword strings a US Google shopper would type for this product: head nouns in singular AND plural, modifier+noun clusters, use-case/audience tails, synonyms, and ALSO the neighbouring product families you expect to FAIL product fit (they must be measured, never rejected unmeasured). Lowercase, no brand names, no specs like "48khz". Include the exact words of the old title's first phrase.
