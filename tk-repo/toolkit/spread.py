"""spread.py — description image layout (user decision 2026-09-26, Fewpe).

Rule: a description never shows two images back to back. Whenever 2+ images sit next to each other (bare top-level
<img>, or a <p>/<div> wrapper that holds exactly one <img> and no text), the run is spread out:
  1. one image per free slot, in source order — a slot is a section boundary (before a top-level h2/h3/h4/div) that
     lies between the previous image and the next one, is not next to another image, and is not inside / before FAQs;
  2. images left over when the slots run out stay at the run's position inside ONE grid:
     <div class="fewpe-img-grid"> — 2 columns on desktop, 1 column under 750px (a <style> tag at the top of the
     description; Shopify keeps it); an odd last image spans the full width.
Image count, order, src and every attribute stay unchanged; only positions move (approved exception to
"image position stays exactly as it was", PROJECT-DESCRIPTION.md). A Q18 `<img class="vp-dim">` is never moved, and
when Q18 is on (brief_flags.json q18 + manual) the slot right under Specifications is kept free for it.
Idempotent: a description that already carries the grid or no run is returned unchanged.

Usage (zero model tokens):
  python3 spread.py final                  README step 7: rewrite final/dNN.json descriptionHtml in place (after dim_keep,
                                           before the payloads) — prints `spread: N changed (G with grid), M untouched`
  python3 spread.py check live_after.json  exit 1 when any product still shows adjacent images outside the grid
  python3 spread.py store [--status active] [--apply]
                                           whole-store fix: fetch, backup to /mnt/user-data/outputs/, dry-run summary;
                                           --apply pushes descriptionHtml-only productUpdate in batches of 10 and
                                           re-fetches to verify (order/count unchanged, 0 adjacent, style present)
"""
import re, sys, json, os, glob, time
from html.parser import HTMLParser

VOID = {'img', 'br', 'hr', 'input', 'meta', 'source', 'wbr'}
IMG = re.compile(r'<img\b[^>]*>')
GRID_CSS = ('<style>.fewpe-img-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;margin:16px 0}'
            '.fewpe-img-grid .full{grid-column:1/-1}@media(max-width:749px){.fewpe-img-grid{grid-template-columns:1fr}}</style>')
GRID_RE = re.compile(r'<div class="fewpe-img-grid">.*?</div></div>', re.S)


def q18_on():
    try:
        f = json.load(open('brief_flags.json'))
        return bool(f.get('q18_dimension_image') or f.get('q18')) and f.get('run_mode') == 'manual'
    except Exception:
        return False


def blocks(h):
    """Top-level blocks as [kind, html]. kind = tag name, 'img' for a bare image or an image-only wrapper."""
    ls = [0] + [m.end() for m in re.finditer('\n', h)]

    class P(HTMLParser):
        def __init__(s):
            super().__init__(convert_charrefs=False); s.d = 0; s.st = []
        def off(s):
            l, c = s.getpos(); return ls[l - 1] + c
        def handle_starttag(s, t, a):
            if s.d == 0: s.st.append((s.off(), t))
            if t not in VOID: s.d += 1
        def handle_startendtag(s, t, a):
            if s.d == 0: s.st.append((s.off(), t))
        def handle_endtag(s, t):
            if t not in VOID: s.d -= 1

    p = P(); p.feed(h); p.close()
    st = p.st
    if not st or h[:st[0][0]].strip(): return None
    out = []
    for i, (o, t) in enumerate(st):
        e = st[i + 1][0] if i + 1 < len(st) else len(h)
        chunk = h[o:e]; kind = t
        n_img = len(IMG.findall(chunk))
        if t in ('p', 'div') and 'fewpe-img-grid' not in chunk and n_img >= 1 \
                and not re.sub(r'<[^>]+>|&nbsp;|\s', '', chunk):
            kind = 'img'
        if kind == 'img' and n_img >= 2 and t in ('p', 'div'):
            # 2026-09-26 patch: a wrapper holding several images (<p><img><img></p>) is a run of image blocks —
            # split it so each image gets its own wrapper and the run is detected / verified like bare images
            op = re.match(r'\s*<[^>]+>', chunk).group(0).strip(); cl = f'</{t}>'
            tail = chunk[chunk.rfind(cl) + len(cl):]
            for q, im in enumerate(IMG.findall(chunk)):
                out.append(['dim' if 'vp-dim' in im else 'img', op + im + cl + (tail if q == n_img - 1 else '')])
            continue
        if kind == 'img' and 'vp-dim' in chunk: kind = 'dim'
        out.append([kind, chunk])
    return out


def adjacent(h):
    """Number of places where two images touch outside the grid (the post-push check)."""
    rest = GRID_RE.sub('<hr data-grid>', h or '')
    B = blocks(rest)
    if B is None: return len(re.findall(r'<img\b[^>]*>\s*<img', rest))
    return sum(1 for a, b in zip(B, B[1:]) if a[0] in ('img', 'dim') and b[0] in ('img', 'dim'))


def _grid(items):
    n = len(items)
    cells = ''.join(f'<div class="full">{x.strip()}</div>' if (n % 2 and i == n - 1) else f'<div>{x.strip()}</div>'
                    for i, x in enumerate(items))
    return ['grid', f'<div class="fewpe-img-grid">{cells}</div>']


def spread(h, keep_spec_slot=False):
    """Returns (new_html, status) — status: ok / no-run / skip-done / skip-parse."""
    if not h or 'fewpe-img-grid' in h: return h, 'skip-done'
    B = blocks(h)
    if B is None: return h, 'skip-parse'
    changed = False
    while True:
        i = 0; run = None
        while i < len(B):
            if B[i][0] == 'img':
                j = i
                while j < len(B) and B[j][0] == 'img': j += 1
                if j - i >= 2: run = (i, j); break
                i = j
            else: i += 1
        if not run: break
        i, j = run; k = j - i; imgs = [b[1] for b in B[i:j]]
        isimg = lambda x: B[x][0] in ('img', 'dim', 'grid')
        prev = max([x for x in range(i) if isimg(x)], default=-1)
        nxt = min([x for x in range(j, len(B)) if isimg(x)], default=len(B))
        faq = min([x for x in range(len(B)) if B[x][0] in ('h2', 'h3', 'h4') and re.search(r'faq', B[x][1][:120], re.I)],
                  default=len(B))

        def ok(g):
            if g <= 0 or g >= len(B) or g >= faq: return False
            if B[g][0] not in ('h2', 'h3', 'h4', 'div'): return False
            if isimg(g - 1) or isimg(g): return False
            if keep_spec_slot:
                hs = [x for x in range(g) if B[x][0] in ('h2', 'h3', 'h4')]
                if hs and re.search(r'Specifications', B[hs[-1]][1][:80]): return False
            return True

        before = [g for g in range(prev + 1, i) if ok(g)]
        after = [g for g in range(j + 1, min(nxt, faq)) if ok(g)]
        slots = before + ['RUN'] + after
        if len(slots) >= k:
            pick = sorted(set(round(n * (len(slots) - 1) / (k - 1)) for n in range(k)))
            chosen = [slots[x] for x in pick]
            if 'RUN' not in chosen:
                c = min(range(len(chosen)), key=lambda c: abs(slots.index(chosen[c]) - len(before)))
                chosen[c] = 'RUN'
            for s in slots:
                if len(set(chosen)) >= k: break
                if s not in chosen: chosen.append(s)
            chosen = sorted(set(chosen), key=slots.index)
            assign = {s: [imgs[n]] for n, s in enumerate(chosen)}
        else:
            nb, na = len(before), len(after); mid = k - nb - na; assign = {}
            for n, s in enumerate(before): assign[s] = [imgs[n]]
            assign['RUN'] = imgs[nb:nb + mid]
            for n, s in enumerate(after): assign[s] = [imgs[nb + mid + n]]
        at_run = assign['RUN']
        NB = []
        for x, b in enumerate(B):
            if x in assign: NB.append(['img', assign[x][0]])
            if i <= x < j:
                if x == i: NB.append(_grid(at_run) if len(at_run) >= 2 else ['img', at_run[0]])
                continue
            NB.append(b)
        B = NB; changed = True
    if not changed: return h, 'no-run'
    out = ''.join(b[1] for b in B)
    if 'fewpe-img-grid' in out: out = GRID_CSS + out
    if IMG.findall(out) != IMG.findall(h): return h, 'skip-mismatch'   # safety: never lose or reorder an image
    return out, 'ok'


def _cmd_final(d='final'):
    ks = q18_on(); ch = gr = un = 0
    for f in sorted(glob.glob(os.path.join(d, 'd*.json'))):
        doc = json.load(open(f)); new, st = spread(doc.get('descriptionHtml') or '', ks)
        if st == 'ok':
            doc['descriptionHtml'] = new; json.dump(doc, open(f, 'w'), ensure_ascii=False, indent=1)
            ch += 1; gr += 'fewpe-img-grid' in new
        else: un += 1
    print(f'spread: {ch} changed ({gr} with grid), {un} untouched')


def _cmd_check(path):
    d = json.load(open(path)); bad = []
    for e in d['data']['products']['edges']:
        n = e['node']; a = adjacent(n.get('descriptionHtml'))
        if a: bad.append((n['id'], a))
    for i, a in bad: print(f'  [FAIL] {i} adjacent images outside grid: {a}')
    print(f'spread-check: {len(bad)} FAIL'); sys.exit(1 if bad else 0)


def _cmd_store(status='active', apply=False, handle=None):
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from shopify_api import gql
    Q = ('query($a:String,$q:String){products(first:100,after:$a,query:$q){edges{node{id handle descriptionHtml}}'
         'pageInfo{hasNextPage endCursor}}}')
    def fetch():
        out, a = [], None
        while True:
            # 2026-09-26: --handle <h> limits the run to one product (manual test run)
            r = gql(Q, {'a': a, 'q': f'handle:{handle}' if handle else f'status:{status}'})['data']['products']
            out += [e['node'] for e in r['edges']]
            if not r['pageInfo']['hasNextPage']: return out
            a = r['pageInfo']['endCursor']
    P = fetch(); new = {}
    for p in P:
        h, st = spread(p['descriptionHtml'] or '')
        if st == 'ok': new[p['id']] = h
    stamp = time.strftime('%Y-%m-%d-%H%M')
    os.makedirs('/mnt/user-data/outputs', exist_ok=True)
    bk = f'/mnt/user-data/outputs/desc-spread-backup-{stamp}.json'
    json.dump({p['id']: {'handle': p['handle'], 'descriptionHtml': p['descriptionHtml']} for p in P if p['id'] in new},
              open(bk, 'w'), ensure_ascii=False)
    print(f'spread store: {len(P)} {status}, {len(new)} to change '
          f'({sum("fewpe-img-grid" in h for h in new.values())} with grid); backup -> {bk}')
    if not apply: print('dry run — add --apply to push'); return
    ids = list(new); fails = []
    for s in range(0, len(ids), 10):
        b = ids[s:s + 10]
        m = 'mutation(%s){%s}' % (','.join(f'$p{k}:ProductUpdateInput!' for k in range(len(b))),
                                  ' '.join(f'u{k}:productUpdate(product:$p{k}){{userErrors{{field message}}}}' for k in range(len(b))))
        r = gql(m, {f'p{k}': {'id': i, 'descriptionHtml': new[i]} for k, i in enumerate(b)})
        for k, i in enumerate(b):
            u = (r.get('data') or {}).get(f'u{k}')
            if not u or u['userErrors']: fails.append((i, u['userErrors'] if u else r.get('errors')))
        print(f'Products {s + 1}–{s + len(b)} done')
    old = {p['id']: p['descriptionHtml'] for p in P}
    L = {p['id']: p['descriptionHtml'] for p in fetch()}
    mism = [i for i in ids if IMG.findall(L.get(i) or '') and
            re.findall(r'src="([^"]+)"', L[i]) != re.findall(r'src="([^"]+)"', old[i])]
    adj = [i for i in ids if adjacent(L.get(i))]
    sty = [i for i in ids if 'fewpe-img-grid' in new[i] and '<style>' not in (L.get(i) or '')]
    print(f'pushed {len(ids) - len(fails)} ok / {len(fails)} failed · verify: order/count mismatch {len(mism)}, '
          f'adjacent {len(adj)}, style missing {len(sty)}')
    for f in fails: print('  [FAIL]', f)


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a: print(__doc__); sys.exit(0)
    if a[0] == 'final': _cmd_final(a[1] if len(a) > 1 else 'final')
    elif a[0] == 'check': _cmd_check(a[1])
    elif a[0] == 'store':
        st = a[a.index('--status') + 1] if '--status' in a else 'active'
        hd = a[a.index('--handle') + 1] if '--handle' in a else None
        _cmd_store(st, '--apply' in a, hd)
    else: print(__doc__); sys.exit(2)
