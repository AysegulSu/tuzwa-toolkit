#!/usr/bin/env python3
"""dim_attach.py — upload the Q18 dimension images (dim/dimNN.png) and place each as gallery image 3 (zero model tokens).

  python3 dim_attach.py [NN ...]           # reads dim/build.json, final/dNN.json (alt), writes dim/media.json

Per product: stagedUploadsCreate -> curl PUT of the PNG to the staged URL -> productCreateMedia(originalSource=resourceUrl,
alt) -> poll until the media is READY -> productReorderMedia so the new image sits at position 3 (index 2): the featured
image and the source's 2nd image stay where they are, the "actual size" image is third, and every source image from the
3rd onwards moves down one place (nothing is removed). A product with fewer than two existing images gets it appended.
Ids are written
to dim/media.json after EVERY product, and a re-run skips products already in that file (nothing uploaded twice — the
rehost.py lesson).

POSITION RULE (user decision 2026-09-09, final): position 3. Position 2 was chosen earlier the same day and reverted
within the hour because most Shopify themes show the 2nd gallery image as the collection-card HOVER image — the size
diagram would have replaced the product's second photo on every collection page. Position 3 keeps the hover photo and
still puts the size picture before the rest of the gallery.

NETWORK: the staged-upload target is a Google Cloud Storage host (shopify-staged-uploads.storage.googleapis.com). The
Backend document notes the sandbox firewall blocked it in an earlier organisation; in this organisation the egress
allowlist is user-managed (api.dataforseo.com was added 2026-09-03). If the PUT fails with a connection error, the host must
be added to Settings -> Capabilities -> egress allowlist; the script prints that exact message and exits 1. Not yet tested
live (written 2026-09-06).

RE-RUN ACROSS BATCHES: before uploading, the live gallery is read and a media whose alt already ends with the dimension
suffix means the product was done in an earlier batch — it is skipped and recorded in dim/media_existing.json (NOT in
dim/media.json, whose entries verify.py reads as "inserted at this position"; the order of such a product is unchanged
by this run, so its snapshot comparison must stay plain) instead of getting a second copy. To REPLACE an old image, delete it in
Shopify first (or productDeleteMedia) and re-run.

ON THE PAGE TOO (user decision 2026-09-09): the same image is inserted into descriptionHtml directly under the
Specifications list as `<p><img class="vp-dim" src=<CDN url of the media> alt="<first title block> – actual size chart"></p>`,
written back to final/dNN.json (so verify.py's live == final comparison holds) and pushed with a productUpdate that carries
ONLY descriptionHtml. gate.py / struct-check.py leave a vp-dim image out of the source-image count. Idempotent: a
description already carrying a vp-dim image is left alone; a product whose gallery already had the image (earlier batch)
still gets the description insert when it is missing.

Alt text of the new image: "<first title block> – actual size and dimensions" (<= 125 chars), unique per product; the
existing media alts written by the description agents keep their ids, so they are unaffected by the position shift.

SCOPE CUT (user decision 2026-09-09, evening): runs only when brief_flags.json carries `"run_mode": "manual"` (via
dim_image.q18_gate) — a scheduled run never attaches a dimension image. REPLACE is now safe: when the gallery image was
deleted in Shopify and a new one is attached, the description's existing vp-dim tag gets the NEW src (it used to be left
untouched, i.e. a dead link). A later Q7 description rewrite that drops the vp-dim tag is restored by dim_keep.py
(README step 7) from the pre-push snapshot.
"""
import json, os, sys, subprocess, time, re
from shopify_api import gql

POSITION = 3   # 1-based gallery position of the dimension image (user decision 2026-09-09: 3 — position 2 would replace the collection-card hover image on most themes)

def staged(name, size):
    d = gql("""mutation($input:[StagedUploadInput!]!){ stagedUploadsCreate(input:$input){
        stagedTargets{ url resourceUrl parameters{ name value } } userErrors{ field message } } }""",
        {"input": [{"resource": "IMAGE", "filename": name, "mimeType": "image/png", "httpMethod": "PUT", "fileSize": str(size)}]})
    r = d['data']['stagedUploadsCreate']
    if r['userErrors']: raise SystemExit(f'stagedUploadsCreate: {r["userErrors"]}')
    return r['stagedTargets'][0]

def put(target, path):
    args = ['curl', '-sS', '-m', '120', '-o', '/dev/null', '-w', '%{http_code}', '-X', 'PUT', '--upload-file', path]
    for p in target['parameters']: args += ['-H', f'{p["name"]}: {p["value"]}']
    r = subprocess.run(args + [target['url']], capture_output=True, text=True)
    if r.returncode or r.stdout.strip() not in ('200', '201'):
        raise SystemExit(f'staged PUT failed (http {r.stdout.strip() or "-"}: {r.stderr.strip()[:200]}). If this is a connection error, add '
                         f'shopify-staged-uploads.storage.googleapis.com to Settings -> Capabilities -> egress allowlist and re-run.')

def create_media(pid, url, alt):
    d = gql("""mutation($id:ID!,$media:[CreateMediaInput!]!){ productCreateMedia(productId:$id, media:$media){
        media{ id status } mediaUserErrors{ field message } } }""",
        {"id": pid, "media": [{"originalSource": url, "alt": alt, "mediaContentType": "IMAGE"}]})
    r = d['data']['productCreateMedia']
    if r['mediaUserErrors']: raise SystemExit(f'productCreateMedia: {r["mediaUserErrors"]}')
    return r['media'][0]['id']

ALT_SUFFIX = ' – actual size and dimensions'

def existing_dim_media(pid):
    """The id of a dimension image already in the product's gallery (alt ends with ALT_SUFFIX), or None. Guards a product
    that enters a second batch or a re-push (user question 2026-09-09): without it the gallery would get a second copy."""
    d = gql("query($id:ID!){ product(id:$id){ media(first:50){ edges{ node{ id alt } } } } }", {"id": pid})
    for e in d['data']['product']['media']['edges']:
        if (e['node'].get('alt') or '').endswith(ALT_SUFFIX): return e['node']['id']
    return None

def media_url(pid, mid):
    """CDN url of a READY MediaImage."""
    d = gql("query($id:ID!){ product(id:$id){ media(first:50){ edges{ node{ id ... on MediaImage { image { url } } } } } } }", {"id": pid})
    for e in d['data']['product']['media']['edges']:
        if e['node']['id'] == mid: return (e['node'].get('image') or {}).get('url')
    return None

DESC_TAG = '<img class="vp-dim" src="{src}" alt="{alt}">'
DESC_ALT_SUFFIX = ' – actual size chart'   # differs from the gallery alt: alts are unique per product (gate / verify)
VP_DIM_RE = re.compile(r'<img\s+class="vp-dim"\s+src="([^"]*)"\s+alt="([^"]*)"\s*/?>')

def insert_in_description(html, src, alt):
    """The dimension image under the Specifications list (user decision 2026-09-09: "put the drawn image on the page under
    Specifications, when it was drawn"): directly after the first </ul> that follows <h3>Specifications</h3>. Idempotent —
    a description already carrying a vp-dim image with the SAME src is returned unchanged. A vp-dim image with a DIFFERENT
    src (the gallery image was deleted in Shopify and re-attached — the documented way to replace one) has its src and alt
    rewritten in place, so the page never keeps a dead CDN link (gap found 2026-09-09: the old form returned unchanged on
    any vp-dim image, which left the deleted media's url in the description after a replace). Returns (html, changed)."""
    m = VP_DIM_RE.search(html)
    if m:
        if m.group(1) == src: return html, False
        return html[:m.start()] + DESC_TAG.format(src=src, alt=alt) + html[m.end():], True
    m = re.search(r'<h3>Specifications</h3>', html)
    if not m: return html, False
    end = html.find('</ul>', m.end())
    if end == -1: return html, False
    end += len('</ul>')
    return html[:end] + '<p>' + DESC_TAG.format(src=src, alt=alt) + '</p>' + html[end:], True

def push_description(pid, html):
    d = gql("""mutation($p:ProductUpdateInput!){ productUpdate(product:$p){ userErrors{ field message } } }""",
            {"p": {"id": pid, "descriptionHtml": html}})
    r = d['data']['productUpdate']
    if r['userErrors']: raise SystemExit(f'productUpdate(descriptionHtml): {r["userErrors"]}')

def describe(nn, pid, mid, title):
    """Insert the (new or pre-existing) dimension image into final/dNN.json's descriptionHtml and push it. Returns a note."""
    fp = f'final/d{nn}.json'
    if not os.path.exists(fp): return 'no final/dNN.json — description not updated'
    d = json.load(open(fp)); url = media_url(pid, mid)
    if not url: return 'media url not found — description not updated'
    alt = (title.split(',')[0].strip() + DESC_ALT_SUFFIX)[:125]
    had = VP_DIM_RE.search(d['descriptionHtml']) is not None
    new, changed = insert_in_description(d['descriptionHtml'], url, alt)
    if not changed: return 'description already carries the image (or has no Specifications list) — unchanged'
    d['descriptionHtml'] = new; json.dump(d, open(fp, 'w'), indent=1, ensure_ascii=False)
    push_description(pid, new)
    return f'description: image {"src replaced (old media gone)" if had else "inserted under Specifications"} and pushed ({url.split("/")[-1][:40]})'

def wait_ready(pid, mid, tries=30):
    for _ in range(tries):
        d = gql("query($id:ID!){ product(id:$id){ media(first:50){ edges{ node{ id status } } } } }", {"id": pid})
        st = {e['node']['id']: e['node'].get('status') for e in d['data']['product']['media']['edges']}
        if st.get(mid) == 'READY': return [e['node']['id'] for e in d['data']['product']['media']['edges']]
        if st.get(mid) == 'FAILED': raise SystemExit(f'media {mid} FAILED processing')
        time.sleep(2)
    raise SystemExit(f'media {mid} not READY after {tries*2}s')

def reorder(pid, mid, position):
    d = gql("""mutation($id:ID!,$moves:[MoveInput!]!){ productReorderMedia(id:$id, moves:$moves){ job{ id } userErrors{ field message } } }""",
            {"id": pid, "moves": [{"id": mid, "newPosition": str(position)}]})
    r = d['data']['productReorderMedia']
    if r['userErrors']: raise SystemExit(f'productReorderMedia: {r["userErrors"]}')

if __name__ == '__main__':
    from dim_image import q18_gate; q18_gate()   # Q18 = Add AND run_mode manual, else nothing is uploaded (scope cut 2026-09-09)
    build = json.load(open('dim/build.json'))['built']
    ids = [f'{int(x):02d}' for x in sys.argv[1:]] or sorted(build)
    done = json.load(open('dim/media.json')) if os.path.exists('dim/media.json') else {}
    for nn in ids:
        if nn not in build: print(f'{nn} attach: no dimension image built — skipped'); continue
        if nn in done: print(f'{nn} attach: already done ({done[nn]["media_id"]}) — skipped'); continue
        ex = json.load(open(f'extract/p{nn}.json')); d = json.load(open(f'final/d{nn}.json')) if os.path.exists(f'final/d{nn}.json') else {}
        pid = ex['id']; title = d.get('title') or ex['old_title']
        alt = (title.split(',')[0].strip() + ALT_SUFFIX)[:125]
        old = existing_dim_media(pid)
        if old:
            ex_ = json.load(open('dim/media_existing.json')) if os.path.exists('dim/media_existing.json') else {}
            ex_[nn] = {'media_id': old, 'product_id': pid, 'note': 'already had a dimension image (earlier batch) — not re-attached'}
            json.dump(ex_, open('dim/media_existing.json', 'w'), indent=1)
            note = describe(nn, pid, old, title)
            print(f'{nn} attach: gallery already carries a dimension image ({old}) — not duplicated; {note}'); continue
        path = build[nn]['file']; size = os.path.getsize(path)
        t = staged(os.path.basename(path), size); put(t, path)
        mid = create_media(pid, t['resourceUrl'], alt)
        order = wait_ready(pid, mid)
        n_before = len(order) - 1; pos = min(POSITION - 1, n_before)   # 0-based index; appended when fewer images exist
        reorder(pid, mid, pos); time.sleep(1)
        note = describe(nn, pid, mid, title)
        done[nn] = {'media_id': mid, 'position': pos + 1, 'alt': alt, 'product_id': pid, 'description': note}
        json.dump(done, open('dim/media.json', 'w'), indent=1)
        print(f'{nn} attach: {mid} -> position {pos+1} of {n_before+1}; {note}')
    ex_n = len(json.load(open('dim/media_existing.json'))) if os.path.exists('dim/media_existing.json') else 0
    print(f'dim-attach: {len([n for n in ids if n in done])} attached / {len(ids)} requested (dim/media.json)' + (f', {ex_n} already had one — not duplicated (dim/media_existing.json)' if ex_n else ''))
