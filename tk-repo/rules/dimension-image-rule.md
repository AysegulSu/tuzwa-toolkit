# Dimension Image — brief Q18 (optional per batch)

User decision 2026-09-06 (now applied to Tuzwa). "M 17.7 × 11.8 in" on its own means nothing to a shopper; a picture of the product
with its measurements drawn on it answers "how big is it?" — the most common reason for size returns. Built entirely by
script from the product's own gallery photo and its own source dimensions: no AI generation, no image credits, zero model
tokens per product, nothing invented.

```
Q18 — Dimension image: (Add dimension image / Skip dimension image)
```

Unanswered = Skip. The main context writes `brief_flags.json` with `"q18_dimension_image": true|false` (README step 1,
beside Q17's flag) and, since 2026-09-09, `"run_mode": "manual" | "scheduled"` from the brief's run-mode question.

## Scope cut (user decision 2026-09-09, evening — "vazgeçme, küçült": keep the feature, shrink it)

After a day of guards (rules 1c–1g) the picture was clear: every wrong image that reached the store came through the
photo-ratio test, no labelled source produced one, and the only reliable catch was the operator's eye (rule 5). So the
feature is not withdrawn but cut to the part that is defensible without luck:

1. **Labelled sources only.** A product is drawn only when the source NAMES the axes (rule 1b, or a labelled pair under
   rule 1d). An unlabelled triple or pair is skipped as `axes not labelled in source` — the photo-ratio test of rule 1c is
   **retired** (`PHOTO_TEST = False` in dim_image.py). Rules 1c, 1e(b), 1f and the photo half of 1d stay in this document
   as the record of why, and as the conditions under which the test would have to be re-enabled — a user decision written
   in the run log, never a default. No photo is downloaded for a product that will not be drawn.
2. **Manual runs only.** dim_image.py and dim_attach.py run only when `brief_flags.json` carries `"run_mode": "manual"`;
   on `"scheduled"` or a missing key they build and attach nothing and print why. Reason: the rule-5 eye check is what
   this feature's safety rests on, and a scheduled run has no eye. Q18 = Add in a scheduled brief is therefore a no-op,
   not an error — the batch's other steps run as usual.
3. **Two live-bug fixes.** (a) *Replace left a dead link:* the documented way to replace an image is "delete it in Shopify,
   re-run" — but the description insert was idempotent on the `vp-dim` class alone, so the page kept the deleted media's
   url. Now a vp-dim tag with a different src is rewritten to the new media's url. (b) *A later rewrite dropped the image:*
   the vp-dim tag is inserted after the description is written; a later batch with Q7 = Rewrite descriptions writes a fresh
   descriptionHtml and the tag vanished from the page while the gallery kept the image, and no gate saw it (gate.py and
   struct-check.py ignore vp-dim by design). New `dim_keep.py` (README step 7, before the payloads, independent of Q18 and
   of the run mode) restores the tag from the pre-push snapshot under the new Specifications list — only when its media is
   still in the live gallery; otherwise it warns and leaves it out, never re-publishing a dead link.

Expected effect: fewer products per batch get an image (only those whose supplier wrote `L x W x H` or labelled figures);
every image that ships has its axes from the source and was looked at by a person.

## What is produced

`dim/dimNN.png` — 1200 px wide, white background: the product cut out of its gallery photo (rembg, small u2netp model),
navy `#000096` dimension lines on the product's own edges (length below, height right, depth as text), **every figure
US-unit first** with the source unit in brackets (`18.1 in (46 cm)`; an inch source reads `22.4 in (56.9 cm)`) — the same
imperial-first rule as unit_dual.py, user decision 2026-09-09 — a size table in inches under the picture when more than
one size is sold, heading `Actual size — <productType>`. Theme colours as in comparison-table-rule.md.

**Colour provenance — measured on Tuzwa 2026-09-12.** The navy above is `#000096`, which is what `dim_image.py`
actually draws with (`NAVY = (0, 0, 150)`; the light the comparison block uses is `#f4f4f4`, `LIGHT = (244, 244,
244)`). Both were read from Tuzwa's live MAIN theme ("Xtra -- NEW",
`gid://shopify/OnlineStoreTheme/161796391136`), file `config/settings_data.json`, default scheme `scheme-1`: navy is
that theme's `buy_button_color`, identical to `scheme-1`'s `primary_button_bg` (the Add-to-cart button), and light is
`scheme-1`'s `secondary_bg` (the light section band). Contrast measured on these values: white on navy 14.6:1, navy
on light 13.3:1. `#000096` is Tuzwa's LIVE navy — it is NOT retired history; it simply happens to match the
Vepine-era navy. The retired values are the PREVIOUS store's `#2c374d` / `#eef5f7` (Worfa, "Vault" theme, 2026-09-10)
and the oldest store's `#d2def6` (vepine.com, 2026-09-07); those must not be reintroduced here or in the scripts.
Theme reads go through the **Shopify connector**, which has `read_themes` — the custom app used by the script route
does not, and `tuzwa.com` is blocked by the container's egress proxy (403 CONNECT); fetch, push and verification stay
on the script route. If the theme or its default scheme changes, read the theme file again through the connector and
update this rule doc AND `compare_build.py` / `fit_build.py` / `dim_image.py` together, in one change. See the
colour-provenance block in comparison-table-rule.md.

## Where it goes on the product page

**Gallery position 3** (user decision 2026-09-09, final). The featured image and the source's 2nd image stay where they
are; the "actual size" image is third; every source image from the 3rd onwards moves down one place. No source image is
ever removed or replaced. A product with fewer than two gallery images gets it appended; a product with no gallery image
has no dimension image at all (rule 2 — the picture is built from that photo). Why not position 2: most Shopify themes
show the 2nd gallery image as the collection-card hover image, so the diagram would replace the product's second photo on
every collection page (position 2 was chosen earlier the same day and reverted for this reason). Alt text: `<first title
block> – actual size and dimensions` (≤ 125 chars). Existing media alts are unaffected (they follow the media id, not the
position). `dim/media.json` records the position actually used and verify.py checks against that record.

**On the page as well (user decision 2026-09-09):** when an image was drawn, the same image is also placed in the
description directly under the Specifications list — `<p><img class="vp-dim" src="<the media's CDN url>" alt="<first
title block> – actual size chart"></p>` — by dim_attach.py after the gallery attach: written into final/dNN.json and
pushed with a productUpdate carrying only descriptionHtml, so verify.py's live == final comparison still holds. The
`vp-dim` class is the marker: gate.py and struct-check.py leave that image out of the source-image count (source images
stay an unchanged prefix, total = max(source, 2)); struct-check FAILs a vp-dim image off our CDN or inserted twice. The
insert is idempotent, and a product that already had the gallery image from an earlier batch still gets the description
insert when it is missing. A product without a drawn image gets nothing on the page. (A `?width=1200` on description
srcs was tried and reverted the same day: measured on 24 live products / 58 images, the CDN already serves WebP and every
image was ≤ 1200 px — total saving 18 KB. Description images need no parameter.)

## Rules

1. **Dimensions come only from the source.** dim_image.py reads a three-figure `L × W × H unit` pattern from the variant
   titles (which carry the size label), else from the Specifications, else from the facts. The unit may follow the last
   figure or every figure (`46cm x 32cm x 16cm`). No pattern → no image; the product is listed in
   `dim/build.json["skipped"]` and named in the run log. A dimension is never typed by hand and never estimated from a
   photo. A package / box / carton / shipping / parcel measurement is never read as the product's size, and neither is the
   measurement of the thing the product FITS (`fits mattresses up to 200 x 150 cm`, `for 15 inch laptops`, `compatible
   with 40 x 60 cm frames` — a sheet, a case or a frame would otherwise get the other object's size, and the photo test
   cannot tell them apart because the proportions match). Decimal commas (`46,5 cm`) and thousands separators (`1,200 mm`)
   are read correctly; `2 x 3 in stock` is not inches. (All three added 2026-09-09 after the user asked what was missing.)
1b. **The axes must be named by the source (user decision 2026-09-09 — a wrong image is worse than no image).** A bare
   `2 x 5 x 6 cm` does not say which figure is the length, the width and the height, and until this date the script drew
   it in source order (STR-DUB-2-batch9 p49: a 46 cm-tall backpack drawn 46 cm wide). Now a triple is used only when the
   source names the axes: an order key next to the figures or once anywhere in the source (`(L x W x H)`, `LxWxH`,
   `Length x Width x Height`, `H x W x D`, a spec row named that way), or labelled figures (`L 46 cm x W 32 cm x H 16 cm`,
   `Length: 46 cm, Width: 32 cm, Height: 16 cm`, `46 cm (L) x 32 cm (W) x 16 cm (H)`, or three separate Length / Width /
   Height spec rows). Labelled figures are used as written, no test.
1c. **[RETIRED 2026-09-09 evening — see Scope cut. Unlabelled figures are now skipped. Kept as the record.]**
   **Unlabelled figures pass a photo-consistency test, never a guess (user decision, same day — "the safe way to more
   images is ours, not the supplier's").** For a bare `46 x 32 x 16 cm` the script takes the product's own cut-out (the
   same rembg cut-out the picture is drawn from) and compares its width ÷ height with the six possible assignments of the
   three figures (which is horizontal, which is vertical, the third is depth). The assignment is used only when exactly
   one fits the photo (within 20 %) and the runner-up is at least 30 % off; because the gap is wider than the tolerance, a
   photo measured within tolerance can never select a wrong assignment — at worst an ambiguous one. Otherwise the product
   is skipped with `axes ambiguous (photo)` and the ratios in the reason. This is not estimating from a photo: every figure
   still comes from the source; the photo only decides which source figure sits on which edge. With several sizes the
   largest is tested and the same positional mapping is applied to every size (the source writes all sizes in the same
   order). `dim/build.json` records `axes: "labelled"` or `axes: "photo-ratio: …"` per product and the build's summary
   line counts both; the run log carries that line and names the ambiguous products. The main context never supplies the
   order by hand. Mixed units are skipped; two figures (labelled or not) follow rule 1d. Rule 2
   matters more here: a lifestyle photo, a 3/4 angle or two products in frame distort the ratio — the test then fails
   safe (skip), but a plain front-on product photo is what makes it succeed.
1d. **Two figures are enough (user decision 2026-09-09).** When no source text carries three figures, a two-figure
   measurement (`200 x 150 cm`, `46cm x 32cm`, `W 46 cm x H 32 cm`, `Diameter 20 cm, Height 30 cm`, `Length 200 x Width
   150 cm`, or two Diameter / Height spec rows) is used the same way: labelled pairs as written (height vertical; a
   length × width pair — a flat item seen from above — length horizontal, width vertical). **Since the Scope cut an
   unlabelled pair (`200 x 150 cm`) is skipped like an unlabelled triple**; the rest of this rule describes the retired
   photo path: unlabelled pairs through the
   photo test, which has only two candidate assignments (a/b or b/a) and so decides more often than with three; a
   near-square pair (30 × 28) is the one case that stays ambiguous and is skipped — likewise a near-square depth / height
   (28.5 × 14 × 15: the belt bag p34), and that is right: on p34 the photo's hanging strap made the bag look tall and the
   "fitting" assignment would have drawn 28.5 cm as the depth. Three figures anywhere in the source
   always take precedence over two. The picture then carries the two lines and no depth text; with several sizes the
   table has Size / Length / Height columns. A two-figure run that is not a size (`pack of 2 x 5 cm hooks`) is caught by
   the same photo test (a square photo fits neither 2/5 nor 5/2) — but rule 5's look is the final guard, as before.
1f. **Three guards added after the batch2 Q18 re-run (2026-09-09, user decision — the user caught a wrong image the
   review had passed).** The photo-ratio test of 1c does NOT always fail safe: on a product photographed at an angle it can
   select a WRONG assignment with a comfortable margin, because perspective foreshortens the long axis.
   (a) **Lie-flat lock (`FLAT_RATIO` = 15 %).** A triple whose smallest figure is under 15 % of its largest is a flat product
   — mat, mattress, cushion, strap, rug, blanket. Its length and its width are both "across", so no top-down or 3/4 photo can
   tell them apart, and the ratio the test measures is perspective, not geometry. Such a triple is never assigned by photo:
   labelled axes or skip. Case: batch2 p05, a 195 x 130 x 5 cm camping mattress drawn 195 wide / 130 tall. The two pillows sit
   side by side along the 130 cm edge, so 195 is the length running away from the camera; the 3/4 angle squashed it to a
   measured ratio of 1.41 and the wrong assignment (1.50) fitted within 6 %. The lock also catches a strap-type item whose
   figures describe the band, not the object (p37: 1.25 x 25 x 1.9 cm).
   (b) **Tolerance 20 % -> 15 % (`PHOTO_TOL`).** batch2 p39 (28 x 15 x 12 cm stained-glass lamp) passed at 18.75 % with the
   wrong assignment — 28 cm placed on depth, the elephant drawn 12 cm wide when the photo shows it clearly wider than tall.
   `PHOTO_GAP` stays 30 %, so GAP > TOL still holds.
   (c) **Connected-blob isolation (`MAIN_PART` = 90 %).** 1e(b)'s span/fill guard only fires when the group happens to span
   the frame; a product photographed WITH its accessories fills its own box perfectly well and slips through, and the ratio
   then measured is the group's. The largest connected blob of the cut-out must now be at least 90 % of the kept pixels.
   Calibrated on that batch's real cut-outs, where the two classes separate with a wide margin: several objects 65.4 %
   (p03 inflator + hose + cable + 3 nozzles), 74.8 % (p04 pillow + pouch + inset circle), 81.6 %; one product 99.3 %, 100 %.
   Share, not blob count — a clean mask still carries speckles (p28 = 8 blobs, 99.3 %).
   Effect on that batch: the three guards block 8 of the 9 images the eye had rejected, and leave the correct ones alone.
   **Two residual risks, deliberately not automated:** a TWO-figure flat measurement has no thin third figure to detect and so
   still goes through the photo test (`195 x 130` alone would be assigned); and a cut-out can be one clean object that is the
   WRONG object — batch2 p28's photo is a single 99.3 % blob of the car seat and headrest the product sits on. Both stay
   rule 5's job, which is why the eye check below now asks its question by name.
1e. **Three refinements from the batch9 re-run (2026-09-09).** (a) The bracket figure is the source's own: when the source
   writes both systems (`18.1 x 12.6 x 6.3 in (46 x 32 x 16 cm)` — every description of ours does, unit_dual.py), the image
   shows `18.1 in (46 cm)`, not `18.1 in (46.0 cm)`; companion figures follow the same axis mapping. (b) A cut-out that is
   several objects (fan + hand + remote: box spans > 60 % of the frame both ways yet is < 30 % filled) is refused as
   `cut-out not isolated` — the photo test would otherwise pass on garbage (p09 did exactly that before this guard; rule 5
   caught it). (c) `dim_image.py build NN` merges into dim/build.json instead of overwriting it, so a single-product
   rebuild no longer drops the batch's other entries (batch9 "for the next run" item 3).
1g. **The cut-out is never shaved — crop to the product's TRUE bounding box (user instruction 2026-09-09, from a live
   batch3 mushroom-lamp image).** The crop must include every pixel of the product mask. It must NOT be taken from a
   density-thresholded box (the "keep a row only if at least 6 % of the frame width is product in it" form), because a
   rounded or tapered outline has very few pixels in its outermost rows and columns — the apex of a dome shade, the flare of
   a lamp head, an animal figure's ears — and those rows fail the density test and are cut away. The product then reaches
   the page with its edges and its head visibly shaved off.
   **This is not cosmetic.** The dimension lines are drawn on the edges of the crop, so a shaved crop draws the measurement
   SHORT: the label still reads the source figure while the line spans less than the product. Measured on real batch2
   cut-outs, density box vs true box: elephant lamp **-12.6 % of the width**, camping mattress -3.4 %, inflatable chair
   -2.2 % of the height, mini washing machine -1.9 %. A mushroom lamp — wide dome on a thin stem — is the worst case of all,
   because the stem rows are what set the density threshold.
   Speckles are removed by blob, not by density: keep the connected blobs that are at least 1 % of the mask and take their
   bounding box (rule 1f(c) already guarantees one blob holds >= 90 %). Leave a small transparent margin around that box so
   the lines do not sit flush on the product's outermost pixel.

2. **The photo is the product's own gallery image.** Default: the featured image. Before building, the main context looks
   at `dim/sheet.png` (one contact sheet of every product's first six images, one look for the whole batch) and writes
   `dim/pick.json` for any product whose featured image is unsuitable — two products side by side (the lines would span
   both), a lifestyle scene where the product is small, a model wearing it. Preferred: one product, plain background.
3. **Largest size is drawn**, the table lists all sizes. The heading uses the batch's productType (head noun), never the
   long title.
4. **Nothing else is written on the image** — no claims, no "fits cats up to X lb" unless the source states it (then it is
   a Specifications line, not an image caption).
5. **Every built image is looked at before attach**, and the look asks ONE question by name (added 2026-09-09 after the
   batch2 p05 miss — the reviewer passed a swapped-axis image because the picture looked tidy): **"is the horizontal line on
   the product's real long axis?"** Answer it from what the product IS, not from the drawing — where the pillows / head end /
   opening / feet sit, which way a person lies on it, which edge the hinge or the handle is on. A tidy image with the axes
   swapped is the failure this step exists to catch; the script's ratio test cannot, because perspective is exactly what
   fools it. Then, as before: — the batch's `dim/dim*.png` files as one contact sheet, again one
   look: a bad cut-out (background remnant, chair leg, half a product) means that product is re-picked (rule 2) or skipped
   with the reason in the run log. The cut-out is reliable on plain backgrounds and only fair on busy scenes.
   A set of DIFFERENT shapes sold as variants (six wall sculptures, p07 of batch9) is not "sizes of one shape": the
   photo-ratio mapping of the largest cannot be applied to the others — skip by judgement, log the reason.

## Steps (README 7b)

- `python3 dim_image.py sheet` → look → `dim/pick.json` → `python3 dim_image.py build` → look at the results →
  `python3 dim_attach.py` (staged upload → productCreateMedia → wait READY → productReorderMedia to position 3; ids saved to
  `dim/media.json` after every product, re-run safe). The position is the `POSITION` constant at the top of dim_attach.py.
  **Across batches (2026-09-09):** before uploading, dim_attach.py reads the live gallery; a media whose alt already ends
  with `– actual size and dimensions` means the product was done in an earlier batch or re-push — it is skipped and listed
  in `dim/media_existing.json`, never duplicated. To replace an old image, delete it in Shopify first and re-run — the
  description's vp-dim tag then gets the new media's url (Scope cut 3a); it is never left pointing at the deleted one.
- Both scripts exit at once, building nothing, unless `brief_flags.json` has `"q18_dimension_image": true` AND
  `"run_mode": "manual"` (Scope cut 2). The build's summary line now also counts `axes not labelled: NN NN …`; the run
  log quotes it, and a `[WARN] … PHOTO_TEST is on` line must never appear in a log without the user's re-enable decision.
- `python3 dim_keep.py` runs in README step 7, before the payloads, in EVERY batch (Q18 = Add or Skip, manual or
  scheduled): a product whose live description carried a vp-dim image keeps it through a Q7 rewrite (Scope cut 3b). Its
  summary line `dim-keep: N restored, W warned, M untouched` goes into the run log; a [WARN] names a product whose image
  media is gone from the gallery — decide by hand (re-attach or leave out).
- verify.py (step 8) reads `dim/media.json`: media order = snapshot with the new image inserted at its recorded position;
  its alt checked; every other check unchanged.
- **Network, not yet tested live (2026-09-06):** the staged-upload PUT goes to `shopify-staged-uploads.storage.googleapis.com`.
  The Backend document records it as blocked in the previous organisation; in this organisation the egress allowlist is
  user-managed. If dim_attach.py reports a connection error on the PUT, add that host to Settings → Capabilities →
  egress allowlist and re-run; the batch's other steps are unaffected either way.
- rembg + onnxruntime are pip-installed at session start when Q18 = Add (`pip install rembg onnxruntime
  --break-system-packages`); the u2netp model (~5 MB) downloads on first use. Never the default 1 GB model — it exceeds the
  container's memory and the process is killed.

## Cost

Per product: a few seconds of script, one CDN download, one upload. Model tokens: two contact-sheet looks per batch
(rules 2 and 5), nothing per product.
