#!/usr/bin/env python3
"""verify.py products.json live_after.json [collections.json] — post-push live verification, EVERY product, zero model tokens.

Added to the toolkit 2026-09-06 (user decision). README-toolkit.md step 8 has asked for this comparison since 2026-09-03,
but the script itself was never a project doc, so every batch re-wrote its own verify.py from the step-8 sentence and the
checked fields silently varied from run to run. This file fixes the list. The checks are README step 8 + the blr-batch13 /
blr-batch23 run-log descriptions ("800 checks / 50 products", "0 duplicates across the batch", "all img on our CDN").

Inputs (all already produced by a normal run — nothing new is required):
  products.json    pre-push snapshot (`shopify_api.py fetch <tag> products.json`, taken BEFORE any mutation)
  live_after.json  post-push fetch of the same tag (`shopify_api.py fetch <tag> live_after.json`)
  collections.json optional; needed for the collections check. Accepted in ANY of the shapes a run produces (2026-09-08,
                   after STR-DUB-2-batch4): the {title: id} map, the raw GraphQL response of the README refresh snippet
                   ({"data": {"collections": {"edges": [{"node": {"id", "title"}}]}}}), that response's inner
                   {"collections": …} / {"edges": […]} objects, or a plain list of {id, title} / {node: {id, title}}.
                   Until then only the map was read: written the README way, every title was "not in collections.json",
                   check 10 printed a [note] on every product and NEVER ACTUALLY RAN while the summary line looked
                   clean. Now an unrecognised shape, or a file that yields no titles, is a hard exit — never a [note].
  final/dNN.json   the per-product outputs the payloads were built from (DESC-SPEC.md output schema)

Per product (each is one check; a check that cannot run is reported, never silently skipped):
   1 title            live == final.title
   2 descriptionHtml  normalized live == normalized final (entities unescaped, whitespace collapsed); on mismatch the
                      tag-stripped text is compared too so the log shows "formatting" vs "content" difference
   3 seo.title        live == final and < 70 chars
   4 seo.description  live == final and < 160 chars
   5 productType      live == final.productType
   6 tags             set(live) == set(snapshot) ∪ {final.season}; no tag of the snapshot dropped; no duplicate in the list
   7 status           live == snapshot (a backend batch never changes status unless the brief says so — pass --status X)
   8 category         final.category_proposal == KEEP -> live category id == snapshot id; else live category name == proposal
   9 cta metafield    json.loads(live custom.cta_benefits) == final.cta_benefits (skipped with a note when final has none)
  10 collections      live collection ids ⊇ snapshot ids ∪ ids of final.collections titles (NEW: … titles reported, not failed)
  11 media alts       every final.media_alts id: live alt == final alt, non-empty, ≤ 125 chars
  12 media order      live media id order == snapshot order — or, for a product in dim/media.json (Q18), the snapshot
                      order with the dimension image inserted at its recorded position (+ its alt checked)
  13 description imgs live <img src> list == final's, every src on our CDN
  14 variant prices   live price per variant id == snapshot (or == final.variants price when the brief changed prices)
  15 brand            our brand name absent from title / description / seo (case-insensitive) — the comparison block
                      (`<div class="vp-compare">`, rules/comparison-table-rule.md) is the one place it is allowed and is
                      removed before the scan; a 17th check confirms exactly one such block is live when brief Q17 = Add table, none when No table
                      (brief_flags.json {"q17_compare_table": true|false}, read via compare_build.q17()); the fit block check
                      (Q19) expects exactly one single-column "Right for you if" block directly before <h3>FAQs</h3> (2026-09-06)
  16 alt uniqueness   no duplicate alt inside the product (media alts + description img alts)
Batch level: every final/dNN.json product present in live_after.json; no alt text repeated across the batch.

Exit 1 on any failure. Output: one line per product + a summary line; failures name the check and show the two values.
Run `python3 head_check.py live_after.json` separately as README step 8 says — this script does not replace it.
"""
import json, re, sys, html, glob, os, argparse
CDN = 'cdn.shopify.com/s/files/1/0806/1645/6416/'
BRAND = 'tuzwa'
try:
    from compare_build import q17; Q17 = q17()   # brief Q17: is the comparison block expected live?
except Exception: Q17 = False
DIM = json.load(open('dim/media.json')) if os.path.exists('dim/media.json') else {}   # brief Q18: attached dimension images
try:
    from fit_build import q19; Q19 = q19()   # brief Q19: is the fit block expected live?
except Exception: Q19 = False

ap = argparse.ArgumentParser()
ap.add_argument('snapshot'); ap.add_argument('live'); ap.add_argument('collections', nargs='?')
ap.add_argument('--final', default='final', help='directory of dNN.json files (default final/)')
ap.add_argument('--status', help='expected live status when the brief changed it (ACTIVE/DRAFT); default: unchanged')
a = ap.parse_args()

def nodes(path):
    d = json.load(open(path)); return {n['id']: n for n in (e['node'] for e in d['data']['products']['edges'])}
def norm_html(h):
    h = html.unescape(h or ''); h = re.sub(r'>\s+<', '><', h); h = re.sub(r'\s+', ' ', h); return h.strip()
def text(h): return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', h or ''))).strip()
def imgs(h): return re.findall(r'<img[^>]+src="([^"]+)"', h or '')
def img_alts(h): return re.findall(r'<img[^>]+alt="([^"]*)"', h or '')

def load_colmap(path):
    """collections.json in any shape a run produces -> {title: id}. Exits on an unrecognised shape or an empty result,
    so the collections check can never degrade to a [note] on every product (STR-DUB-2-batch4, 2026-09-08)."""
    d = json.load(open(path))
    for _ in range(3):                                   # unwrap {"data": {"collections": {"edges": [...]}}} step by step
        if isinstance(d, dict) and 'data' in d: d = d['data']
        elif isinstance(d, dict) and 'collections' in d: d = d['collections']
        elif isinstance(d, dict) and 'edges' in d: d = d['edges']
    if isinstance(d, dict):
        if d and all(isinstance(v, str) and v.startswith('gid://') for v in d.values()): return d      # {title: id}
        sys.exit(f'{path}: unrecognised collections.json shape (dict keys {list(d)[:5]}) — want {{title: id}} or the raw GraphQL response')
    if isinstance(d, list):
        m = {}
        for e in d:
            n = e.get('node', e) if isinstance(e, dict) else {}
            if isinstance(n, dict) and n.get('id') and n.get('title'): m[n['title']] = n['id']
        if m: return m
    sys.exit(f'{path}: no collections found in it — refresh it (README "Store-specific constants") before verifying')

snap = nodes(a.snapshot); live = nodes(a.live)
colmap = load_colmap(a.collections) if a.collections else None
finals = sorted(glob.glob(os.path.join(a.final, 'd*.json')))
if not finals: sys.exit(f'no {a.final}/dNN.json files — nothing to verify')

checks = fails = 0; batch_alts = {}; failed_products = []
def report(nn, name, ok, detail=''):
    global checks, fails
    checks += 1
    if not ok:
        fails += 1; probs.append(name); print(f'  [FAIL] {nn} {name}: {detail}'[:400])

for f in finals:
    nn = os.path.basename(f)[1:3]; d = json.load(open(f)); pid = d['product_id']; probs = []
    L = live.get(pid); S = snap.get(pid)
    if L is None or S is None:
        checks += 1; fails += 1; failed_products.append(nn)
        print(f'{nn} | FAIL: product {pid} missing from {"live_after" if L is None else "snapshot"}'); continue
    # 1 title
    report(nn, 'title', L['title'] == d['title'], f'live={L["title"]!r} final={d["title"]!r}')
    # 2 descriptionHtml
    same = norm_html(L['descriptionHtml']) == norm_html(d['descriptionHtml'])
    if not same:
        kind = 'formatting only (text identical)' if text(L['descriptionHtml']) == text(d['descriptionHtml']) else 'CONTENT differs'
        a1, b1 = norm_html(L['descriptionHtml']), norm_html(d['descriptionHtml'])
        i = next((k for k in range(min(len(a1), len(b1))) if a1[k] != b1[k]), min(len(a1), len(b1)))
        report(nn, 'descriptionHtml', False, f'{kind}; first difference at char {i}: live=…{a1[max(0,i-30):i+40]!r} final=…{b1[max(0,i-30):i+40]!r}')
    else: report(nn, 'descriptionHtml', True)
    # 3-4 seo
    ls, fs = (L.get('seo') or {}), (d.get('seo') or {})
    report(nn, 'seo.title', ls.get('title') == fs.get('title') and len(ls.get('title') or '') < 70, f'live={ls.get("title")!r} ({len(ls.get("title") or "")}) final={fs.get("title")!r}')
    report(nn, 'seo.description', ls.get('description') == fs.get('description') and len(ls.get('description') or '') < 160, f'live={ls.get("description")!r} ({len(ls.get("description") or "")}) final={fs.get("description")!r}')
    # 5 productType
    report(nn, 'productType', L.get('productType') == d.get('productType'), f'live={L.get("productType")!r} final={d.get("productType")!r}')
    # 6 tags
    lt, st = L.get('tags') or [], S.get('tags') or []
    want = set(st) | ({d['season']} if d.get('season') else set())
    report(nn, 'tags', set(lt) == want and len(lt) == len(set(lt)), f'live={sorted(lt)} expected={sorted(want)} dropped={sorted(set(st)-set(lt))} dup={len(lt)!=len(set(lt))}')
    # 7 status
    exp_status = a.status or S.get('status')
    report(nn, 'status', L.get('status') == exp_status, f'live={L.get("status")} expected={exp_status}')
    # 8 category
    prop = (d.get('category_proposal') or 'KEEP').strip(); lc, sc = L.get('category') or {}, S.get('category') or {}
    if prop.upper() == 'KEEP': report(nn, 'category', lc.get('id') == sc.get('id'), f'live={lc.get("name")!r} snapshot={sc.get("name")!r}')
    else: report(nn, 'category', (lc.get('name') or '').lower() == prop.lower(), f'live={lc.get("name")!r} proposal={prop!r}')
    # 9 cta metafield
    if d.get('cta_benefits'):
        mv = (L.get('metafield') or {}).get('value')
        try: lv = json.loads(mv) if mv else None
        except Exception: lv = mv
        report(nn, 'cta_benefits', lv == d['cta_benefits'], f'live={lv} final={d["cta_benefits"]}')
    else: print(f'  [note] {nn} cta_benefits: final has none — not checked')
    # 10 collections
    lcol = {e['node']['id'] for e in (L.get('collections') or {}).get('edges', [])}
    scol = {e['node']['id'] for e in (S.get('collections') or {}).get('edges', [])}
    if colmap is None: print(f'  [note] {nn} collections: no collections.json given — NOT checked')
    else:
        want_ids, new_titles = set(scol), []
        for t in d.get('collections') or []:
            if t.startswith('NEW:'): new_titles.append(t)
            elif t in colmap: want_ids.add(colmap[t])
            else: new_titles.append(t + ' (not in collections.json)')
        report(nn, 'collections', want_ids <= lcol, f'missing={sorted(want_ids-lcol)} unresolved={new_titles}')
        if new_titles and want_ids <= lcol: print(f'  [note] {nn} collections not resolvable by title: {new_titles}')
    # 11-12 media alts + order
    lmedia = [e['node'] for e in (L.get('media') or {}).get('edges', [])]; smedia = [e['node'] for e in (S.get('media') or {}).get('edges', [])]
    lalt = {m['id']: (m.get('alt') or '') for m in lmedia}
    bad = [(m['id'].split('/')[-1], lalt.get(m['id']), m['alt']) for m in d.get('media_alts') or [] if lalt.get(m['id']) != m['alt'] or not m['alt'] or len(m['alt']) > 125]
    report(nn, 'media alts', (not d.get('media_alts')) or not bad, f'mismatch/empty/over125={bad[:3]}')
    if not d.get('media_alts'): print(f'  [note] {nn} media_alts: final has none — not checked')
    # Q18 dimension image (rules/dimension-image-rule.md): dim/media.json says which product got a new gallery image and
    # where; the expected order is then the snapshot with that id inserted at its position, and its alt must match.
    exp_order = [m['id'] for m in smedia]
    dm = DIM.get(nn)
    if dm:
        exp_order = exp_order[:dm['position']-1] + [dm['media_id']] + exp_order[dm['position']-1:]
        report(nn, 'dimension image', lalt.get(dm['media_id']) == dm['alt'], f'media {dm["media_id"]} alt live={lalt.get(dm["media_id"])!r} expected={dm["alt"]!r}')
    report(nn, 'media order', [m['id'] for m in lmedia] == exp_order, f'live={len(lmedia)} expected={len(exp_order)}{" (incl. Q18 image at " + str(dm["position"]) + ")" if dm else ""} (order or count differs)')
    # 13 description images
    li, fi = imgs(L['descriptionHtml']), imgs(d['descriptionHtml'])
    report(nn, 'description imgs', li == fi and all(CDN in s for s in li), f'live={len(li)} final={len(fi)} foreign={[s for s in li if CDN not in s][:2]} order_same={li==fi}')
    # 14 variant prices
    lv_ = {e['node']['id']: e['node']['price'] for e in (L.get('variants') or {}).get('edges', [])}
    if d.get('variants'): exp = {v['id']: str(v['price']) for v in d['variants']}
    else: exp = {e['node']['id']: e['node']['price'] for e in (S.get('variants') or {}).get('edges', [])}
    diff = {k: (lv_.get(k), v) for k, v in exp.items() if str(lv_.get(k)) != str(v)}
    report(nn, 'variant prices', not diff, f'{list(diff.items())[:3]} (live, expected)')
    # 15 brand — absent everywhere EXCEPT inside the comparison block, which carries it by design
    # (rules/comparison-table-rule.md, 2026-09-06); the block is removed before the scan, and its presence live is checked
    live_nb = re.sub(r'<div class="vp-compare"[\s\S]*?</table>\s*</div>', '', L['descriptionHtml'] or '')
    blob = ' '.join([L['title'], text(live_nb), ls.get('title') or '', ls.get('description') or '']).lower()
    report(nn, 'brand absent', BRAND not in blob, f'"{BRAND}" found in live copy outside the comparison block')
    nblk = len(re.findall(r'<div class="vp-compare"', L['descriptionHtml'] or ''))
    exp_blk = 1 if (Q17 and not ('compare' in d and d['compare'] is None)) else 0   # compare: null = source too thin, no block
    report(nn, 'comparison block', nblk == exp_blk, f'live vp-compare blocks={nblk}, expected {exp_blk} (brief Q17 {"Add table" if Q17 else "No table"})')
    nfit = len(re.findall(r'<div class="vp-fit"', L['descriptionHtml'] or ''))
    exp_fit = 1 if (Q19 and not ('fit' in d and d['fit'] is None)) else 0
    fit_pos_ok = (exp_fit == 0) or bool(re.search(r'<div class="vp-fit"[\s\S]*?</div>\s*</div>\s*</div>\s*<h3>FAQs</h3>', L['descriptionHtml'] or ''))
    fit_one_col = 'Not the right fit if' not in (L['descriptionHtml'] or '')
    report(nn, 'fit block', nfit == exp_fit and fit_pos_ok and fit_one_col, f'live vp-fit blocks={nfit}, expected {exp_fit} (brief Q19 {"Add" if Q19 else "Skip"}); before FAQs={fit_pos_ok}; one column={fit_one_col}')
    # 16 alt uniqueness within product (+ collect for batch)
    alts = [m.get('alt') or '' for m in lmedia] + img_alts(L['descriptionHtml'])
    report(nn, 'alt unique in product', len(alts) == len(set(alts)), f'dups={[x for x in set(alts) if alts.count(x)>1][:3]}')
    for x in alts: batch_alts.setdefault(x, []).append(nn)
    print(f'{nn} | {"ok" if not probs else "FAIL: " + ", ".join(probs)}')
    if probs: failed_products.append(nn)

# batch-level: alt uniqueness across the batch
dups = {k: sorted(set(v)) for k, v in batch_alts.items() if k and len(set(v)) > 1}
checks += 1
if dups: fails += 1; print(f'  [FAIL] batch alt text repeated across products: {list(dups.items())[:5]}')
extra = [p for p in live if p not in snap]
if extra: print(f'  [note] {len(extra)} products in live_after.json are not in the snapshot (tag changed mid-run?)')
print(f'verify: {len(finals)} products, {checks} checks, {fails} failures' + (f' — failed products: {failed_products}' if failed_products else ''))
print('reminder: run `python3 head_check.py live_after.json` separately (README step 8).')
sys.exit(1 if fails else 0)
