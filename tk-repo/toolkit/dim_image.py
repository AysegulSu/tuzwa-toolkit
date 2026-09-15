#!/usr/bin/env python3
"""dim_image.py — brief Q18 "dimension image": a size infographic built by script from the product's own gallery
photo and its own dimensions (rules/dimension-image-rule.md, user decision 2026-09-06). Zero model tokens.

  python3 dim_image.py sheet  [NN ...]   # contact sheet of every product's gallery images -> dim/sheet.png (+ sheet_index.txt)
  python3 dim_image.py build  [NN ...]   # dim/dimNN.png for every product with dimensions (+ dim/build.json)

Inputs: raw/pNN.json (media urls), extract/pNN.json (specs, variants, old_title), brief_flags.json (q18_dimension_image,
run_mode), optional dim/pick.json {"NN": <media index>} written by the main context after looking at the sheet (default 0 =
featured). Dimensions are read ONLY from the source. Nothing is invented.

SCOPE CUT (user decision 2026-09-09, evening — "vazgeçme, küçült"): after a day of guards the photo-ratio test was still the
source of every wrong image, and the only thing that reliably caught them was the operator's eye. Two consequences:
  1. LABELLED SOURCES ONLY. An unlabelled triple or pair is skipped as `axes not labelled in source` — the photo-ratio test
     is retired (`PHOTO_TEST = False`; the code stays for a deliberate, logged re-enable, never by default).
  2. MANUAL RUNS ONLY. brief_flags.json must carry `"run_mode": "manual"`; on `"scheduled"` (or a missing key) the script
     builds nothing and says so — the rule-5 eye check does not exist in a scheduled run, so the feature must not either.
Fewer products get an image; every image that ships is defensible.

AXES MUST BE LABELLED (user decision 2026-09-09 — "a wrong image is worse than no image"): a bare `2 x 5 x 6 cm` says
nothing about which figure is the length, the width and the height, and the earlier version drew it in source order —
STR-DUB-2-batch9 p49 came out 46 cm wide and 16 cm tall for a backpack that is 46 cm tall. Now a triple is used only when
the source itself names the axes, in one of these forms:
  * an order key next to the figures or once anywhere in the source — `(L x W x H)`, `LxWxH`, `Length x Width x Height`,
    `H x W x D`, a spec row NAMED that way (`Dimensions (L x W x H): 46 x 32 x 16 cm`);
  * labelled figures — `L 46 cm x W 32 cm x H 16 cm`, `Length: 46 cm, Width: 32 cm, Height: 16 cm`,
    `46 cm (L) x 32 cm (W) x 16 cm (H)`, or three separate spec rows Length / Width / Height.
A source that gives the three numbers UNLABELLED is not guessed from its writing order. Instead (user decision, same
day — "the safe way to more images is ours, not the supplier's") the script runs a CONSISTENCY TEST against the product's
own photo: the cut-out's width/height ratio is compared with the six possible assignments of the three figures
(which is horizontal, which is vertical, the third is depth); the assignment is used only when exactly one fits the photo
(within PHOTO_TOL = 20 %) and the runner-up is clearly off (PHOTO_GAP = 30 %; GAP > TOL, so a photo measured within tolerance
can never select a wrong assignment — at worst an ambiguous one). Otherwise the product is skipped with
`axes ambiguous (photo)` and the ratios in the reason. This is not an estimate — every figure still comes from the source;
the photo only decides which source figure sits on which edge. With several sizes, the largest is tested and the same
positional mapping is applied to all (the source writes every size in the same order). Both outcomes are named in
dim/build.json (`axes`: "labelled" / "photo-ratio …") and in the run log. The unit may follow the last figure or every
figure (`46cm x 32cm x 16cm`; the batch9 gap). Package / box / carton / shipping / parcel measurements are never read as
the product's size.

Background removal: rembg with the small u2netp model (pip install rembg onnxruntime; ~5 MB model, downloaded once).
The 1 GB default model is killed by the container's memory limit — always pass the u2netp session.
Photo download: curl from cdn.shopify.com (the CDN is reachable from the container; only the staged-upload storage host
is blocked). Output canvas 1200 px wide, white, theme navy #000096 lines, size table when more than one size is sold.
"""
import json, re, sys, os, subprocess, html

NAVY = (0, 0, 150); GREY = (122, 122, 122); LIGHT = (244, 244, 244); LINE = (227, 227, 227); INK = (26, 26, 26)
# NAVY/LIGHT — MEASURED ON TUZWA 2026-09-12 from the live MAIN theme 'Xtra -- NEW'
# (gid://shopify/OnlineStoreTheme/161796391136), config/settings_data.json, default scheme-1, read through the Shopify
# connector (the script-route app has no read_themes and tuzwa.com is blocked from the container).
# NAVY = #000096 (0, 0, 150) = buy_button_color; LIGHT = #f4f4f4 (244, 244, 244) = scheme-1 secondary_bg.
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

NUM = r'(\d+(?:[.,]\d+)?)'   # 46.5 or 46,5 (comma decimal normalised by dec())
UNIT = r'(in(?:ch(?:es)?)?|"|cm|mm)'
SEP = r'\s*(?:x|×|\*|by)\s*'
NOT_IN = r'(?!\s+(?:stock|store|total|all|each|every|the|an?|our|your|one|packs?|sets?|pairs?|pieces?|pcs)\b)'   # `2 x 3 in stock` is not inches
# three figures, the unit after the last one or after every one
DIM_RE = re.compile(r'(?<![\d.,])' + NUM + r'\s*(?:' + UNIT + r')?' + SEP + NUM + r'\s*(?:' + UNIT + r')?' + SEP + NUM + r'\s*' + UNIT + r'(?![a-z])' + NOT_IN, re.I)
DIM2_RE = re.compile(r'(?<![\d.])' + NUM + r'\s*(?:' + UNIT + r')?' + SEP + NUM + r'\s*' + UNIT + r'(?![a-z])' + NOT_IN + r'(?!\s*(?:x|×|\*|by)\s*\d)', re.I)   # two figures, unit after the last or both
AXIS = r'(length|long|width|wide|depth|deep|height|high|tall|thickness|thick|diameter|dia|ø|[LWHD])'
ORDER_RE = re.compile(r'\(?\s*' + AXIS + r'\s*[x×*/]\s*' + AXIS + r'\s*[x×*/]\s*' + AXIS + r'\s*\)?', re.I)
ORDER2_RE = re.compile(r'\(?\s*' + AXIS + r'\s*[x×*/]\s*' + AXIS + r'\s*\)?(?!\s*[x×*/])', re.I)   # `(L x W)`, `W x H`, `Dia x H`
# labelled figure: `L 46 cm`, `Length: 46 cm`, `46 cm (L)`, `46cm L`
LAB_BEFORE = re.compile(AXIS + r'\s*[:=]?\s*' + NUM + r'\s*' + UNIT + r'?\b', re.I)
LAB_AFTER = re.compile(NUM + r'\s*' + UNIT + r'?\s*\(?\s*' + AXIS + r'\s*\)?(?![a-z])', re.I)
MIN_FILL = 0.30    # a cut-out whose box spans most of the frame but is < 30 % filled is several objects, not one product
MAIN_PART = 0.90   # the largest connected blob of the cut-out must be >= 90 % of the kept pixels, else several objects were kept
                   # (STR-DUB-2-batch2 Q18 re-run, 2026-09-09: p03's cut-out was inflator + hose + cable + 3 nozzles and the
                   # span/fill guard did not fire because the group filled its own box; the ratio measured was the group's)
                   # Calibrated on that batch's real cut-outs, and the two classes separate with a wide margin:
                   #   several objects  p03 65.4 %, p04 74.8 %, p03(alt) 81.6 %
                   #   one product      p28 99.3 %, p05/p14/p24/p39 100.0 %
                   # Share, not blob count: a clean single-product mask can still carry speckles (p28 = 8 blobs, 99.3 %).
PHOTO_TOL, PHOTO_GAP = 1.15, 1.30   # photo-ratio consistency test: best fit within 15 %, runner-up at least 30 % off (GAP > TOL => a measurement within TOL can never pick a wrong assignment, only an ambiguous one)
                                    # 20 % -> 15 % on 2026-09-09: batch2 p39 (28 x 15 x 12 stained-glass lamp) passed at 18.75 % with the wrong assignment
FLAT_RATIO = 0.15  # a triple whose smallest figure is < 15 % of its largest is a LIE-FLAT product (mat, mattress, cushion, strap,
                   # rug, blanket): its length and its width are both "across" and a top-down or 3/4 photo cannot tell them apart —
                   # perspective foreshortens the long axis and the WRONG assignment then fits better than the right one.
                   # batch2 p05 (195 x 130 x 5 camping mattress) was drawn 195 wide / 130 tall: the two pillows sit side by side
                   # along the 130 cm edge, so 195 is the length running away from the camera. The photo test "confirmed" it at
                   # 6 % because the 3/4 angle squashed the length. Such a product needs LABELLED axes or it is skipped.
PACKAGE_RE = re.compile(r'\b(package|packing|packaging|box|carton|shipping|parcel|gift box)\b'
                        r'|\b(fits?|fitting|for|compatible|compatibility|suitable|up to|accommodates?|holds?|designed for)\b', re.I)   # not the product's own size: packaging, or the thing it fits
PHOTO_TEST = False   # scope cut 2026-09-09 (evening): unlabelled figures are SKIPPED, never resolved by the photo. Every wrong image
                     # of the day (batch9 p49, batch2 p05 / p39 / p03, batch3) came through this test; no labelled source produced one.
                     # Re-enabling is a user decision to be written in the run log, never a default.
NOT_LABELLED = 'axes not labelled in source (photo-ratio test retired 2026-09-09) — labelled L/W/H or skip'

def q18():
    try: return bool(json.load(open('brief_flags.json')).get('q18_dimension_image', False))
    except Exception: return False

def run_mode():
    """'manual' / 'scheduled' from brief_flags.json; anything else (missing key, typo) reads as 'scheduled' — the safe side."""
    try: m = str(json.load(open('brief_flags.json')).get('run_mode', '')).strip().lower()
    except Exception: m = ''
    return 'manual' if m == 'manual' else 'scheduled'

def q18_gate():
    """Exit quietly unless Q18 = Add AND the run is manual (user decision 2026-09-09: no eye check, no dimension image)."""
    if not q18(): print('dim_image: Q18 = Skip (brief_flags.json) — nothing built'); sys.exit(0)
    if run_mode() != 'manual':
        print('dim_image: Q18 needs "run_mode": "manual" in brief_flags.json — a scheduled run never builds a dimension image '
              '(rule 5 eye check is not possible without an operator); nothing built'); sys.exit(0)

def dec(v):
    """'46,5' -> '46.5' (decimal comma); '1,200' -> '1200' (thousands separator: 1-3 digits, comma, exactly 3 digits);
    the source figure otherwise as written."""
    if not v: return v
    return v.replace(',', '') if re.fullmatch(r'\d{1,3},\d{3}', v) else v.replace(',', '.')

def unit_norm(u):
    u = (u or '').lower(); return 'in' if u.startswith('in') or u == '"' else u

def axis_norm(a):
    a = a.lower()
    if a in ('l', 'length', 'long'): return 'length'
    if a in ('w', 'width', 'wide'): return 'width'
    if a in ('d', 'depth', 'deep'): return 'depth'
    if a in ('h', 'height', 'high', 'tall'): return 'height'
    if a in ('diameter', 'dia', 'ø'): return 'diameter'
    return 'thickness'

def roles(ax):
    """{axis: value} -> (L, W, H) or None. Horizontal line = length (else width); depth text = the other horizontal;
    vertical line = height (else thickness). Anything else is ambiguous -> None."""
    H = ax.get('height', ax.get('thickness'))
    hor = [k for k in ('length', 'width', 'depth') if k in ax]
    if H is None or len(hor) != 2: return None
    L = ax['length'] if 'length' in ax else ax['width']
    W = ax['depth'] if 'depth' in ax else (ax['width'] if 'length' in ax else None)
    if W is None: return None
    return (L, W, H)

def roles2(ax):
    """{axis: value} with exactly two axes -> (L, None, H) or None. Vertical = height (else thickness); horizontal = the
    other (length / width / diameter). Length + width without a height (a flat item seen from above): length horizontal,
    width vertical. Anything else is ambiguous -> None."""
    if len(ax) != 2: return None
    if 'height' in ax or 'thickness' in ax:
        H = ax.get('height', ax.get('thickness')); other = [k for k in ax if k not in ('height', 'thickness')]
        return (ax[other[0]], None, H) if other else None
    if 'length' in ax and 'width' in ax: return (ax['length'], None, ax['width'])
    return None

def inches(v, u):
    """Source figure -> inches as a short string (1 decimal, '.0' dropped)."""
    f = float(v); x = f if u == 'in' else (f / 2.54 if u == 'cm' else f / 25.4)
    t = f'{x:.1f}'; return t[:-2] if t.endswith('.0') else t

def fmt(v, u, alt=None):
    """US unit first, always (user decision 2026-09-09, same rule as unit_dual.py): '18.1 in (46 cm)', '46 in (116.8 cm)'.
    The source figure is printed as written; only the converted one is computed — and when the source itself carries the
    other unit (`18.1 x 12.6 x 6.3 in (46 x 32 x 16 cm)`), that figure is used instead of a conversion (alt = (value, unit))."""
    if alt and alt[0]:
        av, au = alt
        return f'{v} in ({av} {au})' if u == 'in' else f'{av} in ({v} {u})'
    if u == 'in': return f'{v} in ({float(v)*2.54:.1f} cm)'
    return f'{inches(v, u)} in ({v} {u})'

def order_key(text):
    """'(L x W x H)' anywhere in text -> ['length','width','height'] (three distinct axes) or None."""
    for m in ORDER_RE.finditer(text or ''):
        k = [axis_norm(m.group(i)) for i in (1, 2, 3)]
        if len(set(k)) == 3: return k
    return None

def order_key2(text):
    """'(L x W)' / 'W x H' anywhere in text -> two distinct axes or None."""
    for m in ORDER2_RE.finditer(text or ''):
        k = [axis_norm(m.group(i)) for i in (1, 2)]
        if len(set(k)) == 2: return k
    return None

def triple(text, order):
    """A three-figure run in text, mapped by `order` (an order key found in the same text or the global one).
    Returns (L, W, H, unit) or None; None also when the unit is mixed or no order applies."""
    m = DIM_RE.search(text)
    if not m: return None
    units = {unit_norm(u) for u in (m.group(2), m.group(4), m.group(6)) if u}
    if len(units) != 1: return None
    key = order_key(text) or order
    if not key: return None
    ax = dict(zip(key, (dec(m.group(1)), dec(m.group(3)), dec(m.group(5)))))
    r = roles(ax)
    return (r[0], r[1], r[2], units.pop()) if r else None

def labelled(text, pairs=False):
    """Figures each carrying their own axis label -> (L, W, H, unit) or None. pairs=True also accepts two axes (W=None)."""
    ax, units = {}, set()
    for m in LAB_BEFORE.finditer(text):
        ax.setdefault(axis_norm(m.group(1)), dec(m.group(2))); units.add(unit_norm(m.group(3)) if m.group(3) else None)
    for m in LAB_AFTER.finditer(text):
        ax.setdefault(axis_norm(m.group(3)), dec(m.group(1))); units.add(unit_norm(m.group(2)) if m.group(2) else None)
    units.discard(None)
    if len(units) != 1: return None
    r = roles(ax) if len(ax) >= 3 else (roles2(ax) if pairs else None)
    return (r[0], r[1], r[2], units.pop()) if r else None

def companion(text, n, unit):
    """The same figures written in the OTHER unit system in the same text — `18.1 x 12.6 x 6.3 in (46 x 32 x 16 cm)` —
    so the bracket on the image can show the source's own metric figure instead of a rounded conversion. Returns the
    figures in source order (n of them) or None."""
    rx = DIM_RE if n == 3 else DIM2_RE
    for m in rx.finditer(text):
        g = m.groups(); units = {unit_norm(u) for u in g[1::2] if u}; figs = [dec(x) for x in g[0::2]]
        if len(units) == 1 and units.pop() != unit: return tuple(figs)
    return None

def read_dims(text, order):
    """(L, W, H, unit) from one text, labelled first, then an ordered triple; None when nothing certain."""
    if PACKAGE_RE.search(text): return None
    return labelled(text) or triple(text, order)

def raw_triple(text):
    """An unlabelled three-figure run -> (a, b, c, unit) in source order, or None (mixed units / package)."""
    if PACKAGE_RE.search(text): return None
    m = DIM_RE.search(text)
    if not m: return None
    units = {unit_norm(u) for u in (m.group(2), m.group(4), m.group(6)) if u}
    return (dec(m.group(1)), dec(m.group(3)), dec(m.group(5)), units.pop()) if len(units) == 1 else None

def read_pair(text):
    """Two labelled figures (`W 46 cm x H 32 cm`, `Diameter 20 cm, Height 30 cm`, `Length 200 x Width 150 cm`) ->
    (L, None, H, unit) or None."""
    if PACKAGE_RE.search(text) or DIM_RE.search(text): return None
    r = labelled(text, pairs=True)
    if r: return r
    m = DIM2_RE.search(text); key = order_key2(text)
    if not (m and key): return None
    units = {unit_norm(u) for u in (m.group(2), m.group(4)) if u}
    if len(units) != 1: return None
    r = roles2(dict(zip(key, (dec(m.group(1)), dec(m.group(3))))))
    return (r[0], r[1], r[2], units.pop()) if r else None

def raw_pair(text):
    """An unlabelled two-figure run -> (a, b, None, unit) in source order, or None."""
    if PACKAGE_RE.search(text) or DIM_RE.search(text): return None
    m = DIM2_RE.search(text)
    if not m: return None
    units = {unit_norm(u) for u in (m.group(2), m.group(4)) if u}
    return (dec(m.group(1)), dec(m.group(3)), None, units.pop()) if len(units) == 1 else None

def with_alt(text, r, order=None):
    """r = (L, W, H, unit). Attach the companion figures of the other unit system as a 5th element, in the SAME order as
    r: unlabelled result -> source order (resolve_axes permutes both together); result mapped by an order key -> the
    same key mapping; result from labelled figures (`L 46 cm x W 32 cm …`) -> no companion (its order is not knowable)."""
    n = 2 if (r[1] is None or r[2] is None) else 3   # labelled pair (L, None, H, u) or raw pair (a, b, None, u)
    alt = companion(text, n, r[3])
    if alt is None: return r + (None,)
    lab = labelled(text, pairs=(n == 2))
    if lab: return r + (None,)
    key = (order_key(text) if n == 3 else order_key2(text)) or (order if n == 3 else None)
    if key:
        m = roles(dict(zip(key, alt))) if n == 3 else roles2(dict(zip(key, alt)))
        return r + ((m,) if m else (None,))
    return r + (alt,)

def dimensions(ex):
    """[(label, L, W, H, unit)] — one entry per size found. Variant titles first (they carry the size label), then specs,
    then facts. ex['_dim_mode'] = 'labelled' when the source names the axes (figures already in L, W, H order) or
    'unlabelled' when the entries are the source's own figure order and STILL NEED the photo-ratio test (resolve_axes)."""
    order = order_key(ex.get('old_title', '')) or order_key(' | '.join(f"{s['name']}: {s['value']}" for s in ex.get('specs', []))) \
        or order_key(' | '.join(ex.get('facts', [])))
    found, raw = [], []
    def vlabel(t):
        m = DIM_RE.search(t) or DIM2_RE.search(t)
        label = re.sub(r'[\(\)\[\]]|' + (re.escape(m.group(0)) if m else '$^'), '', t).strip(' /-–,:')
        return (label.split('/')[-1].strip() or label)[:14] or 'Size'
    for v in ex.get('variants', []):
        t = v['title']; r = read_dims(t, order)
        if r: found.append((vlabel(t),) + with_alt(t, r, order))
        else:
            q = raw_triple(t)
            if q: raw.append((vlabel(t),) + with_alt(t, q, order))
    if not found and not raw:
        rows = ' , '.join(f"{s['name']} {s['value']}" for s in ex.get('specs', []) if not PACKAGE_RE.search(s['name']) and re.match(r'^\s*(length|width|depth|height|thickness)\b', s['name'], re.I))
        r = labelled(rows) if rows else None
        if r: found.append(('Size',) + r + (None,))
    if not found and not raw:
        for s_ in ex.get('specs', []):
            t = f"{s_['name']}: {s_['value']}"; r = read_dims(t, order)
            name = s_['name']; label = name if re.search(r'size|dimension|measure', name, re.I) is None else ''
            mm = re.search(r'\b(XS|S|M|L|XL|XXL|\d+XL)\b', LAB_BEFORE.sub('', ORDER2_RE.sub('', ORDER_RE.sub('', str(s_['value']) + ' ' + name))))
            lb = (mm.group(1) if mm else label or 'Size')[:14]
            if r: found.append((lb,) + with_alt(t, r, order))
            else:
                q = raw_triple(t)
                if q: raw.append((lb,) + with_alt(t, q, order))
    if not found and not raw:
        for f in ex.get('facts', []):
            r = read_dims(f, order)
            if r: found.append(('Size',) + with_alt(f, r, order)); break
            q = raw_triple(f)
            if q: raw.append(('Size',) + with_alt(f, q, order)); break
    if not found and not raw:
        # TWO-FIGURE pass (user decision 2026-09-09): only when no source text carries three figures
        for v in ex.get('variants', []):
            t = v['title']; r = read_pair(t)
            if r: found.append((vlabel(t),) + with_alt(t, r))
            else:
                q = raw_pair(t)
                if q: raw.append((vlabel(t),) + with_alt(t, q))
        if not found and not raw:
            rows = ' , '.join(f"{s['name']} {s['value']}" for s in ex.get('specs', []) if not PACKAGE_RE.search(s['name']) and re.match(r'^\s*(length|width|depth|height|thickness|diameter)\b', s['name'], re.I))
            r = labelled(rows, pairs=True) if rows else None
            if r: found.append(('Size',) + r + (None,))
        if not found and not raw:
            for s_ in ex.get('specs', []):
                t = f"{s_['name']}: {s_['value']}"; r = read_pair(t)
                name = s_['name']; label = name if re.search(r'size|dimension|measure', name, re.I) is None else ''
                mm = re.search(r'\b(XS|S|M|L|XL|XXL|\d+XL)\b', LAB_BEFORE.sub('', ORDER2_RE.sub('', ORDER_RE.sub('', str(s_['value']) + ' ' + name))))
                lb = (mm.group(1) if mm else label or 'Size')[:14]
                if r: found.append((lb,) + with_alt(t, r))
                else:
                    q = raw_pair(t)
                    if q: raw.append((lb,) + with_alt(t, q))
        if not found and not raw:
            for f in ex.get('facts', []):
                r = read_pair(f)
                if r: found.append(('Size',) + with_alt(f, r)); break
                q = raw_pair(f)
                if q: raw.append(('Size',) + with_alt(f, q)); break
    ex['_dim_mode'] = 'labelled' if found else ('unlabelled' if raw else '')
    out, seen = [], set()
    for e in (found or raw):
        k = e[1:5]
        if k not in seen: seen.add(k); out.append(e)
    return out

def resolve_axes(dims, photo_ratio):
    """Photo-ratio consistency test for UNLABELLED figures. dims: [(label, a, b, c, unit)] in source order;
    photo_ratio: cut-out width / height. Returns (dims in (L, W, H) order, note) or (None, reason)."""
    import math
    pair = dims[0][3] is None   # two-figure source: only two assignments
    big = max(range(len(dims)), key=lambda i: max(float(x) for x in dims[i][1:4] if x is not None))
    a = [float(x) for x in dims[big][1:4] if x is not None]
    # LIE-FLAT LOCK (user decision 2026-09-09, batch2 p05): a triple with one very thin figure is a flat item; its length and
    # width are both horizontal in any top-down or angled photo, so the ratio test is measuring perspective, not geometry.
    # It does not fail safe here — it picks the wrong assignment with a comfortable margin. Only labelled axes may draw these.
    if not pair and min(a) / max(a) < FLAT_RATIO:
        return None, (f'flat item ({min(a):g}/{max(a):g} = {min(a)/max(a):.0%} < {FLAT_RATIO:.0%}): length and width are both '
                      f'across on a flat product, the photo ratio cannot tell them apart — needs labelled axes in the source')
    cands = []   # (error, horizontal index, vertical index)
    for h in range(len(a)):
        for v in range(len(a)):
            if h == v: continue
            cands.append((abs(math.log(a[h] / a[v]) - math.log(photo_ratio)), h, v))
    # equal figures give identical ratios — collapse them so a tie between equals is not read as ambiguity
    best = min(cands); others = [c for c in cands if (a[c[1]], a[c[2]]) != (a[best[1]], a[best[2]])]
    second = min(others) if others else None
    fits = best[0] <= math.log(PHOTO_TOL); clear = second is None or second[0] >= math.log(PHOTO_GAP)
    ratios = f'photo {photo_ratio:.2f} vs best {a[best[1]]:g}/{a[best[2]]:g}={a[best[1]]/a[best[2]]:.2f}' + (f', next {a[second[1]]:g}/{a[second[2]]:g}={a[second[1]]/a[second[2]]:.2f}' if second else '')
    if not fits: return None, f'axes ambiguous (photo): no assignment fits — {ratios}'
    if not clear: return None, f'axes ambiguous (photo): two assignments fit — {ratios}'
    h, v = best[1], best[2]
    def alt_of(e, idx):
        al = e[5] if len(e) > 5 else None
        return tuple(al[i] if i is not None else None for i in idx) if al else None
    if pair:
        return [(e[0], e[1 + h], None, e[1 + v], e[4], alt_of(e, (h, None, v))) for e in dims], f'photo-ratio (2 figures): {ratios} -> L={"ab"[h]} H={"ab"[v]}'
    d = ({0, 1, 2} - {h, v}).pop()
    return [(e[0], e[1 + h], e[1 + d], e[1 + v], e[4], alt_of(e, (h, d, v))) for e in dims], f'photo-ratio: {ratios} -> L={"abc"[h]} D={"abc"[d]} H={"abc"[v]}'

def media_urls(n):
    raw = json.load(open(f'raw/p{n:02d}.json'))
    return [(e['node']['id'], (e['node'].get('image') or {}).get('url')) for e in raw['media']['edges'] if e['node'].get('mediaContentType') == 'IMAGE' and (e['node'].get('image') or {}).get('url')]

def download(url, path):
    if os.path.exists(path): return path
    r = subprocess.run(['curl', '-sS', '-L', '-m', '60', '-o', path, url], capture_output=True, text=True)
    if r.returncode or not os.path.exists(path): raise RuntimeError(f'download failed: {url} {r.stderr[:120]}')
    return path

def short_name(ex, d):
    """'Cat Tent Bed' — the productType (already the head noun, Title Case) or the first title block's last 3 words."""
    pt = (d or {}).get('productType') or ex.get('productType') or ''
    if pt: return pt
    return ' '.join(ex['old_title'].split(',')[0].split()[-3:])

def cutout(photo_path):
    """The product cut out of its photo (RGBA, tight crop). Done once per product; its width/height ratio feeds resolve_axes."""
    from PIL import Image
    import numpy as np
    from rembg import remove, new_session
    im = Image.open(photo_path).convert('RGB')
    if max(im.size) > 1600: im.thumbnail((1600, 1600))
    cut = remove(im, session=new_session('u2netp')).convert('RGBA')
    a = np.array(cut)[:, :, 3] > 128
    # TRUE bounding box, never a density-thresholded one (rule 1g, user instruction 2026-09-09). The old form kept a row
    # only when >= 6 % of the frame width was product in it, which shaves every rounded or tapered outline: the apex of a
    # dome shade, the flare of a lamp head, an animal figure's ears. That is not cosmetic — the dimension lines are drawn on
    # the crop's edges, so a shaved crop draws the measurement SHORT while the label still reads the source figure.
    # Measured on real batch2 cut-outs, density box vs true box: elephant lamp -12.6 % of the width, camping mattress
    # -3.4 %, inflatable chair -2.2 % of the height. A mushroom lamp (wide dome, thin stem) is the worst case, because the
    # stem rows are what set the threshold. Speckles are dropped by BLOB, not by density.
    keep = a
    try:
        from scipy import ndimage as _nd
        _lab, _n = _nd.label(a)
        if _n > 1:
            _sz = _nd.sum(a, _lab, range(1, _n + 1)); _tot = a.sum()
            keep = np.isin(_lab, [i + 1 for i, s in enumerate(_sz) if s / _tot >= 0.01])
    except ImportError:
        pass
    rows = np.where(keep.any(1))[0]; cols = np.where(keep.any(0))[0]
    if len(rows) < 10 or len(cols) < 10: raise RuntimeError('background removal found no product')
    # several disconnected objects (fan + hand + remote + a second fan) give a box that spans the frame yet is mostly empty;
    # the photo-ratio test would then pass on garbage — STR-DUB-2-batch9 p09 re-run, 2026-09-09
    box = (cols.min(), rows.min(), cols.max() + 1, rows.max() + 1)
    fill = a[box[1]:box[3], box[0]:box[2]].mean(); spanx = (box[2] - box[0]) / a.shape[1]; spany = (box[3] - box[1]) / a.shape[0]
    if fill < MIN_FILL and spanx > 0.6 and spany > 0.6:
        raise RuntimeError(f'cut-out not isolated (box fills {fill:.0%}, spans {spanx:.0%} x {spany:.0%} of the frame: several objects kept) — pick a plainer photo')
    # the span/fill guard only fires when the group happens to span the frame; a product photographed WITH its accessories
    # (inflator + hose + cable + nozzles: batch2 p03) fills its own box perfectly well and slips through. The connected-blob
    # test catches it directly: one product is one blob. (user decision 2026-09-09)
    try:
        from scipy import ndimage
        lab, n = ndimage.label(a)
        if n > 1:
            share = max(ndimage.sum(a, lab, range(1, n + 1))) / a.sum()
            if share < MAIN_PART:
                raise RuntimeError(f'cut-out not isolated ({n} separate objects kept, the largest is only {share:.0%} of the '
                                   f'cut-out: the product is photographed with its accessories) — pick a single-product photo')
    except ImportError:
        pass
    # a small transparent margin so the dimension lines do not sit flush on the product's outermost pixel (rule 1g)
    pad = max(4, int(0.01 * max(box[2] - box[0], box[3] - box[1])))
    box = (max(0, box[0] - pad), max(0, box[1] - pad), min(a.shape[1], box[2] + pad), min(a.shape[0], box[3] + pad))
    return cut.crop(box)

def compose(prod, name, dims, shown_idx, out_path):
    from PIL import Image, ImageDraw, ImageFont
    W = 1200; c = Image.new('RGB', (W, 1400), 'white'); d = ImageDraw.Draw(c)
    F = lambda s: ImageFont.truetype(FONT, s)
    F1, F2, F3 = F(34), F(28), F(24)
    pw = 760; ph = int(prod.height * pw / prod.width)
    if ph > 700: ph = 700; pw = int(prod.width * ph / prod.height)
    prod = prod.resize((pw, ph), Image.LANCZOS); px, py = 130, 120; c.paste(prod, (px, py), prod)
    label, L, Wd, H, u = dims[shown_idx][:5]; al = dims[shown_idx][5] if len(dims[shown_idx]) > 5 else None
    au = 'cm' if u == 'in' else 'in'   # the companion's unit is the other system (mm companions are rare; shown as given)
    A = lambda i: (al[i], au) if al and al[i] else None
    def hline(x1, x2, y, t):
        d.line((x1, y, x2, y), fill=NAVY, width=4); d.line((x1, y-14, x1, y+14), fill=NAVY, width=4); d.line((x2, y-14, x2, y+14), fill=NAVY, width=4)
        tw = d.textlength(t, font=F1); cx = (x1+x2)/2; d.rectangle((cx-tw/2-12, y-26, cx+tw/2+12, y+26), fill='white'); d.text((cx-tw/2, y-20), t, fill=NAVY, font=F1)
    def vline(x, y1, y2, t):
        d.line((x, y1, x, y2), fill=NAVY, width=4); d.line((x-14, y1, x+14, y1), fill=NAVY, width=4); d.line((x-14, y2, x+14, y2), fill=NAVY, width=4)
        a, b = t.split(' (', 1)   # '18.1 in' over '(46 cm)' — two rows so the text stays inside the canvas
        d.text((x+22, (y1+y2)/2-38), a, fill=NAVY, font=F1); d.text((x+22, (y1+y2)/2+6), '(' + b, fill=NAVY, font=F3)
    for x in (px, px+pw):
        for yy in range(py+ph, py+ph+40, 12): d.line((x, yy, x, yy+6), fill=(180, 180, 200), width=2)
    for yy in (py, py+ph):
        for xx in range(px+pw, px+pw+40, 12): d.line((xx, yy, xx+6, yy), fill=(180, 180, 200), width=2)
    hline(px, px+pw, py+ph+50, fmt(L, u, A(0)))
    vline(px+pw+50, py, py+ph, fmt(H, u, A(2)))
    sub = (f'Depth {fmt(Wd, u, A(1))}' if Wd is not None else '') + (f'  ·  shown: {label}' if len(dims) > 1 else '')
    if sub.strip(' ·'): d.text((px, py+ph+105), sub.strip(' ·'), fill=GREY, font=F3)
    d.text((px, 45), f'Actual size — {name}', fill=INK, font=F1)
    y = py + ph + 160
    if len(dims) > 1:
        hgt = 46 + 42 * len(dims) + 10
        heads = ('Size', 'Length (in)', 'Width (in)', 'Height (in)') if dims[0][2] is not None else ('Size', 'Length (in)', 'Height (in)')
        tw = 20 + 205 * len(heads)   # table width follows the columns, not the product's width
        d.rectangle((px, y, px+tw, y+hgt), outline=LINE, width=2); d.rectangle((px, y, px+tw, y+46), fill=LIGHT)
        for i, t in enumerate(heads): d.text((px+20+i*205, y+9), t, fill=INK, font=F2)
        for r, (lb, l, w, h, uu) in enumerate(e[:5] for e in dims):
            for i, t in enumerate((lb, f'{inches(l, uu)} in') + ((f'{inches(w, uu)} in',) if w is not None else ()) + (f'{inches(h, uu)} in',)):
                d.text((px+20+i*205, y+58+r*42), t, fill=NAVY if i == 0 else INK, font=F2)
        y += hgt + 20
    c = c.crop((0, 0, W, y + 20)); c.save(out_path, optimize=True)
    return c.size

if __name__ == '__main__':
    cmd = sys.argv[1]; ids = [int(x) for x in sys.argv[2:]] or sorted(int(f[1:3]) for f in os.listdir('extract') if f.endswith('.json'))
    os.makedirs('dim/src', exist_ok=True)
    q18_gate()
    if cmd == 'sheet':
        from PIL import Image, ImageDraw, ImageFont
        cells, idx = [], []
        for n in ids:
            for k, (mid, url) in enumerate(media_urls(n)[:6]):
                try: p = download(url, f'dim/src/p{n:02d}_{k}.jpg'); cells.append((n, k, p)); idx.append(f'{n:02d}.{k} {mid}')
                except Exception as e: print(f'[WARN] {n:02d} media {k}: {e}')
        cols = 12; cw = 150; rows = (len(cells) + cols - 1) // cols
        sheet = Image.new('RGB', (cols*cw, rows*(cw+22)), 'white'); dr = ImageDraw.Draw(sheet); f = ImageFont.truetype(FONT, 16)
        for i, (n, k, p) in enumerate(cells):
            im = Image.open(p).convert('RGB'); im.thumbnail((cw-6, cw-6)); x, y = (i % cols)*cw, (i // cols)*(cw+22)
            sheet.paste(im, (x+3, y+3)); dr.text((x+4, y+cw), f'{n:02d}.{k}', fill=NAVY, font=f)
        sheet.save('dim/sheet.png'); open('dim/sheet_index.txt', 'w').write('\n'.join(idx) + '\n')
        print(f'dim/sheet.png: {len(cells)} thumbnails, {len(ids)} products — write dim/pick.json {{"NN": k}} for any product whose best single-product photo is not k=0')
    elif cmd == 'build':
        pick = json.load(open('dim/pick.json')) if os.path.exists('dim/pick.json') else {}
        # merge into an existing build.json (STR-DUB-2-batch9 "for the next run" item 3: `build 35` used to overwrite the
        # file with that one product, and dim_attach.py then attached only it); the products named now are recomputed.
        prev = json.load(open('dim/build.json')) if os.path.exists('dim/build.json') else {'built': {}, 'skipped': {}}
        built, skipped = prev.get('built', {}), prev.get('skipped', {})
        for n in ids: built.pop(f'{n:02d}', None); skipped.pop(f'{n:02d}', None)
        for n in ids:
            ex = json.load(open(f'extract/p{n:02d}.json'))
            d = json.load(open(f'final/d{n:02d}.json')) if os.path.exists(f'final/d{n:02d}.json') else {}
            dims = dimensions(ex)
            if not dims:
                why = 'no L x W x H pattern in source'; skipped[f'{n:02d}'] = why; print(f'{n:02d} dim: skipped — {why}'); continue
            urls = media_urls(n)
            if not urls: skipped[f'{n:02d}'] = 'no gallery image'; print(f'{n:02d} dim: skipped — no gallery image'); continue
            k = int(pick.get(f'{n:02d}', 0)); k = k if k < len(urls) else 0
            if ex['_dim_mode'] == 'unlabelled' and not PHOTO_TEST:
                # decided BEFORE the download / cut-out: no photo is touched for a product that will not be drawn
                skipped[f'{n:02d}'] = NOT_LABELLED; print(f'{n:02d} dim: skipped — {NOT_LABELLED}'); continue
            try:
                p = download(urls[k][1], f'dim/src/p{n:02d}_{k}.jpg')
                prod = cutout(p)
                axes = 'labelled'
                if ex['_dim_mode'] == 'unlabelled':
                    dims, axes = resolve_axes(dims, prod.width / prod.height)
                    if dims is None: skipped[f'{n:02d}'] = axes; print(f'{n:02d} dim: skipped — {axes}'); continue
                shown = max(range(len(dims)), key=lambda i: float(dims[i][1]))   # the largest size is drawn
                size = compose(prod, short_name(ex, d), dims, shown, f'dim/dim{n:02d}.png')
                built[f'{n:02d}'] = {'file': f'dim/dim{n:02d}.png', 'source_media': urls[k][0], 'dims': dims, 'shown': dims[shown][0], 'size': size, 'axes': axes}
                print(f'{n:02d} dim: {len(dims)} size(s), shown {dims[shown][0]} {"x".join(str(x) for x in dims[shown][1:4] if x is not None)} {dims[shown][4]} [{axes}] -> dim/dim{n:02d}.png')
            except Exception as e:
                skipped[f'{n:02d}'] = str(e)[:160]; print(f'[WARN] {n:02d} dim: skipped — {e}')
        json.dump({'built': built, 'skipped': skipped}, open('dim/build.json', 'w'), indent=1)
        na = [k for k, v in skipped.items() if v.startswith('axes ambiguous')]; pr = [k for k, v in built.items() if v['axes'] != 'labelled']
        nl = sorted(k for k, v in skipped.items() if v == NOT_LABELLED)
        print(f'dim-build: {len(built)} built ({len(built)-len(pr)} labelled, {len(pr)} by photo-ratio), {len(skipped)} skipped'
              + (f' — {len(nl)} axes not labelled: {" ".join(nl)}' if nl else '')
              + (f' — {len(na)} axes ambiguous: {" ".join(na)}' if na else '') + ' (dim/build.json)')
        if pr: print(f'[WARN] {len(pr)} image(s) resolved by the photo-ratio test (PHOTO_TEST is on): {" ".join(sorted(pr))} — write the reason for the re-enable in the run log')
