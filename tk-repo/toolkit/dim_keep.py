#!/usr/bin/env python3
"""dim_keep.py — keep an EXISTING dimension image on the page across a description rewrite (zero model tokens).

  python3 dim_keep.py [products.json]      # default products.json; edits final/dNN.json in place, prints one line per change

Gap found 2026-09-09 (user question "what did we miss?"): the Q18 `<img class="vp-dim">` tag is inserted into
descriptionHtml AFTER the description is written (dim_attach.py). When a later batch re-processes the same product with
Q7 = Rewrite descriptions, the agents write a fresh descriptionHtml from the source — the vp-dim tag is not in the source,
so it silently disappears from the page while the gallery still carries the image. Nothing flagged it: gate.py and
struct-check.py IGNORE vp-dim images by design, and verify.py compares live with the new final.

This script runs BEFORE the payloads (README step 7), independent of Q18 and of the run mode: for every final/dNN.json it
looks at the pre-push snapshot (products.json, README step 2) and, when the LIVE description carried a vp-dim image that
the new final does not, re-inserts the same tag (same src, same alt) under the new Specifications list through
dim_attach.insert_in_description. Guards:
  * the src must still be one of the product's live gallery media (compared by file name — Shopify appends `?v=` to
    CDN urls); a src whose media is gone is NOT restored (that would re-publish a dead link) — printed as [WARN] for the
    operator: delete the tag for good, or re-attach with dim_attach.py.
  * a final that already carries a vp-dim tag is left alone (dim_attach.py owns it in that run).
  * a final without a Specifications list cannot take the tag — printed as [WARN].
Exit 0 always; the summary line goes into the run log: `dim-keep: N restored, W warned, M untouched`.
"""
import json, os, re, sys
from dim_attach import insert_in_description, VP_DIM_RE

def fname(url):
    return (url or '').split('?')[0].rsplit('/', 1)[-1].lower()

def snapshot(path):
    d = json.load(open(path))
    nodes = d.get('data', {}).get('products', {}).get('edges', []) if isinstance(d, dict) else []
    return {e['node']['id']: e['node'] for e in nodes if isinstance(e, dict) and 'node' in e}

if __name__ == '__main__':
    snap_path = sys.argv[1] if len(sys.argv) > 1 else 'products.json'
    if not os.path.exists(snap_path): raise SystemExit(f'dim_keep: {snap_path} not on disk — run README step 2 first')
    snap = snapshot(snap_path)
    restored, warned, untouched = 0, 0, 0
    for f in sorted(os.listdir('final')) if os.path.isdir('final') else []:
        if not re.fullmatch(r'd\d\d\.json', f): continue
        nn = f[1:3]; fp = f'final/{f}'
        ex_p = f'extract/p{nn}.json'
        if not os.path.exists(ex_p): untouched += 1; continue
        pid = json.load(open(ex_p))['id']; node = snap.get(pid)
        if not node: untouched += 1; continue
        live = VP_DIM_RE.search(node.get('descriptionHtml') or '')
        if not live: untouched += 1; continue
        d = json.load(open(fp)); html = d.get('descriptionHtml') or ''
        if VP_DIM_RE.search(html): untouched += 1; continue
        src, alt = live.group(1), live.group(2)
        media_files = {fname((e['node'].get('image') or {}).get('url')) for e in node.get('media', {}).get('edges', [])}
        if fname(src) not in media_files:
            warned += 1; print(f'[WARN] {nn} dim-keep: live description carried a vp-dim image whose media is no longer in the gallery ({fname(src)}) — NOT restored; re-attach with dim_attach.py or leave it out'); continue
        new, changed = insert_in_description(html, src, alt)
        if not changed:
            warned += 1; print(f'[WARN] {nn} dim-keep: new description has no Specifications list — vp-dim image could not be restored'); continue
        d['descriptionHtml'] = new; json.dump(d, open(fp, 'w'), indent=1, ensure_ascii=False)
        restored += 1; print(f'{nn} dim-keep: vp-dim image restored under Specifications ({fname(src)[:40]})')
    print(f'dim-keep: {restored} restored, {warned} warned, {untouched} untouched')
