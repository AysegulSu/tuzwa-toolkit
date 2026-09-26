# Description image layout rule (user decision 2026-09-26)

**Rule:** a product description never shows two images back to back.

- When 2+ images sit next to each other (bare top-level `<img>`, or a `<p>`/`<div>` wrapper that holds only images and no
  text — including one wrapper holding several images, `<p><img><img></p>`), the run is spread out **one image per
  section break**: right before a top-level `h2` / `h3` / `h4` or `div` block, between the previous image and the next
  one, never next to another image, never inside or before the **FAQs** section.
- Images left over when the section breaks run out stay at the run's position inside **one** 2-column grid:
  `<div class="fewpe-img-grid">` (1 column under 750 px; an odd last image spans the full width). The grid's `<style>`
  tag is written once at the top of the description.
- **Image count, order, `src` and every attribute never change — only the position moves.** This is the approved
  exception to "image position stays exactly as it was" in PROJECT-DESCRIPTION.md.
- A Q18 dimension image (`<img class="vp-dim">`) is never moved; when Q18 is on, the slot under Specifications is kept
  free for it.
- Idempotent: a description with no run, or one that already carries the grid, is returned unchanged.

**Tool:** `spread.py` (toolkit root, zero model tokens).

- `python3 spread.py final` — README step 7, after `dim_keep`, before the payloads: rewrites `final/dNN.json` in place.
- `python3 spread.py check live_after.json` — verify.py check 18: exit 1 when any product still shows adjacent images
  outside the grid.
- `python3 spread.py store --status active [--apply]` — whole-store fix: fetch, back up every description that will
  change to `/mnt/user-data/outputs/desc-spread-backup-<stamp>.json`, dry-run summary; `--apply` pushes
  descriptionHtml-only `productUpdate` in batches of 10, then re-fetches and prints
  `verify: order/count mismatch 0, adjacent 0, style missing 0` — all three must be 0.
- `--handle <handle>` limits a store run to one product (manual test run).

**Safety:** the script refuses (status `skip-mismatch`) whenever the image list of the output differs from the input.

**Patch 2026-09-26:** `blocks()` splits a wrapper holding several images into one image block per image, so
`<p><img><img></p>` is detected as a run and counted by `adjacent()`.

**First sweep 2026-09-26 (active products):** 3,171 active, 9 with adjacent images (all pairs), 0 needed the grid.
