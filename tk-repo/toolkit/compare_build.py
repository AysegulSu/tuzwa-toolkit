#!/usr/bin/env python3
"""compare_build.py NN [NN ...] — render the "Tuzwa vs Others" comparison block into final/dNN.json (zero model tokens).

Rule: rules/comparison-table-rule.md (user decision 2026-09-06). The description agent writes only the CONTENT of the
table into final/dNN.json — a `compare` object with a short product name and five product rows (see the schema in
DESC-SPEC.md). This script owns the HTML: it renders the block from the fixed template (theme colours, fixed heading,
fixed store row), removes any block already in descriptionHtml, inserts the new one immediately before
`<h3>Key Features</h3>`, and writes the file back. Idempotent — run it as often as gate.py runs.

Checks (FAIL = exit 1, the product is not finished):
  - `compare` present, `name` 2–5 words, brand name not inside `name` (the template adds it)
  - exactly 5 product rows; feature 20–60 characters; no digit-only / spec-only row; no comparison wording
    (than / unlike / ordinary / cheap / other brands …) — the Others column IS the comparison, the row text is our fact
  - `others` is "✘" or a short neutral phrase (2–14 chars); at least ONE of the 5 product rows is neutral, never ✘ on all five
  - every feature row is traceable to the source: at least one content word (4+ letters) of the row appears in extract/pNN.json
    (facts, specs, package, how_to_use, faq_source, variants, old title). assume_check.py still runs over the rendered text.
  - `<h3>Key Features</h3>` exists in descriptionHtml (insertion point)
Prints one line per product and a summary; exit 1 on any FAIL.

Units (2026-09-11, user decision — ddl2 pregnancy pillow, the live table read "155 x 75 x 60 cm" on a US-only store):
the rendered name, feature rows and Others cells are IMPERIAL ONLY. The agent may write the source's metric figure (the
traceability / foreign-number checks run on what the agent wrote, against the source); `unit_dual.imperial_only()` then
converts metric -> imperial and drops the metric figure before rendering ("155 x 75 x 60 cm" -> "61 x 29.5 x 23.6 in").
The metric source value still stands, in parentheses, in the Specifications list. The length check (20–60) runs on the
converted row, which is what the shopper sees. Idempotent: an imperial row is returned unchanged.

Brief Q17 (optional table, user decision 2026-09-06): the flag file brief_flags.json in the work dir carries
{"q17_compare_table": true|false}. false or no file = "No table": any existing block is REMOVED from descriptionHtml,
no `compare` object is required, and the script exits 0. struct-check.py and verify.py read the same file
(helper `q17()` below) so all three agree on whether a block must be present.

Layout note (2026-09-07, user instruction after seeing blr-batch26 live): the Tuzwa / Others columns are centred by a
flex wrapper INSIDE every th/td, not by the cell's text-align — the live theme overrode the inline `text-align:center`
and the ticks / "Varies" sat off-centre under their headers. th and td of a value column share one width and padding so
header and cells have the same centre; the feature column is pinned left the same way. The 50 live blr-batch26 blocks
were re-rendered with this template the same day (rows parsed from the live HTML, nothing else in the description touched).

Layout note (2026-09-10, user instruction from a live phone screenshot): the 120 px value columns ate 240 px of a 360 px
phone, leaving ~100 px for the feature text — "Looks and works like a real charger" broke into five lines and the block
ran ~1400 px tall. Four changes: (a) the product name left the first <th> and became the SECOND LINE of the navy heading
band, so the header row is one line ("Feature · Tuzwa · Others") instead of a five-line product title; (b) the value
columns are PERCENTAGES — Tuzwa 14 %, Others 24 % — with 4 px side padding; (c) `table-layout:fixed` so the theme cannot
redistribute the columns by content, plus `max-width:none;margin:0` on the table to close the theme's right-hand gap;
(d) the table is 14 px / 10 px row padding and the Others text 12 px / 1.25 and wrappable ("Blurry footage" over two
lines is fine). Height drops from ~1400 px to ~560 px on a phone.
`clamp()` widths were tried FIRST and do not work: under `table-layout:fixed` the browser ignores a clamp() column width
and splits the table into three equal columns (measured with Playwright, 2026-09-10). Percentages are what holds.
Desktop: the outer div carries `max-width:680px` — with percentage columns and no cap, a 1470 px container gave the
feature column ~1300 px and stranded the ticks against the right edge. Measured after the change: phone (328 px block)
186 / 54 / 86 px, desktop (680 px block) 406 / 103 / 171 px, Others phrases on one line.
"""
import json, re, sys, html

BRAND = 'Tuzwa'
HEADING = f'Why choose {BRAND}'
STORE_ROW = ('30-day easy returns', 'Varies')   # CONFIRMED FOR TUZWA by the user 2026-09-12 (the window is
# also 30 days). Printed on every product page, so re-confirm whenever the store or its policy changes.
# Theme colours — MEASURED ON TUZWA 2026-09-12 from the live MAIN theme 'Xtra -- NEW'
# (gid://shopify/OnlineStoreTheme/161796391136), config/settings_data.json, default scheme-1, read through the
# Shopify connector (the connector has read_themes; the app used by the script route does not, and tuzwa.com is
# blocked from the container — the connector is the route for theme reads).
# NAVY = buy_button_color / scheme-1 primary_button_bg (the Add-to-cart button), LIGHT = scheme-1 secondary_bg.
# GREEN is a fixed success colour, not from any theme. Contrast checked on Tuzwa: white on NAVY 14.6:1,
# NAVY on LIGHT 13.3:1.
NAVY, LIGHT, GREEN, GREY, XGREY, LINE = '#000096', '#f4f4f4', '#2e9e4f', '#7a7a7a', '#b5b5b5', '#ececec'
TICK = (f'<span style="display:inline-block;width:22px;height:22px;border-radius:50%;border:2px solid {GREEN};'
        f'color:{GREEN};font-size:13px;line-height:22px;font-weight:700;text-align:center">&#10003;</span>')
# Value columns (Tuzwa / Others): PERCENTAGE width (see the 2026-09-10 layout note — px starved the feature column on a
# phone, clamp() is ignored under table-layout:fixed), centred by a flex wrapper inside the cell — theme CSS that
# overrides td/th text-align cannot move a flex-centred child. th and td share width + padding → same centre line.
MAXW = '680px'   # cap on the whole block: percentage columns in a 1470 px theme container strand the ticks at the edge
COL_V = 'width:14%;padding:10px 4px;text-align:center !important;vertical-align:middle'
COL_O = 'width:24%;padding:10px 4px;text-align:center !important;vertical-align:middle'
CENTER = '<div style="display:flex;justify-content:center;align-items:center;width:100%">'
# Others cells wrap (12px / 1.25), so the flex wrapper also needs text-align for the second line.
CENTER_T = '<div style="display:flex;justify-content:center;align-items:center;width:100%;text-align:center">'
BLOCK_RE = re.compile(r'<div class="vp-compare"[\s\S]*?</table>\s*</div>')
STOP = set('with for and the that this your from into onto over under after before while when than then them they their our its are was were will can any all one two three four five six each every more most very just only also stay stays keep keeps'.split())
COMPARE_WORDS = re.compile(r'\b(?:than|unlike|ordinary|regular|typical|cheap(?:er|est)?|other brands?|competitors?|others|most \w+s)\b', re.I)

def imp(text):
    """Imperial-only text for the rendered block (2026-09-11). Lazy import: unit_dual imports this module's BLOCK_RE."""
    from unit_dual import imperial_only
    return imperial_only(text)

def cell_others(v):
    if v.strip() == '✘':
        return f'<td style="{COL_O};border-top:1px solid {LINE};color:{XGREY};font-size:18px;line-height:22px">{CENTER}&#10005;</div></td>'
    return f'<td style="{COL_O};border-top:1px solid {LINE};color:{GREY};font-size:12px;line-height:1.25">{CENTER_T}{html.escape(v.strip())}</div></td>'

def row(feature, others, cls=''):
    c = f' class="{cls}"' if cls else ''
    return (f'<tr{c}><td style="padding:10px 16px;border-top:1px solid {LINE};vertical-align:middle;text-align:left !important">{html.escape(feature.strip())}</td>'
            f'<td style="{COL_V};border-top:1px solid {LINE}">{CENTER}{TICK}</div></td>{cell_others(others)}</tr>')

def render(name, rows):
    """rows = [(feature, others)]. Every text the shopper sees is passed through imp() — imperial only (2026-09-11)."""
    rows = [(imp(f), o if o.strip() == '✘' else imp(o)) for f, o in rows]
    body = ''.join(row(f, o) for f, o in rows) + row(STORE_ROW[0], STORE_ROW[1], 'vp-store')
    return (f'<div class="vp-compare" style="margin:28px 0;max-width:{MAXW};border:1px solid #e3e3e3;border-radius:12px;overflow:hidden;background:#fff">'
            f'<div style="padding:12px 16px;background:{NAVY};color:#fff;line-height:1.3">'
            f'<div style="font-weight:700;font-size:17px">{HEADING}</div>'
            f'<div style="font-size:13px;opacity:.85;margin-top:2px">{html.escape(imp(name).strip())}</div></div>'
            f'<table style="width:100%;max-width:none;margin:0;border-collapse:collapse;font-size:14px;line-height:1.3;table-layout:fixed"><thead><tr style="background:{LIGHT}">'
            f'<th style="text-align:left !important;padding:10px 16px;font-weight:600;font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:#1a1a1a">Feature</th>'
            f'<th style="{COL_V};font-weight:800;font-size:12px;color:{NAVY};white-space:nowrap;letter-spacing:.04em">{CENTER}{BRAND}</div></th>'
            f'<th style="{COL_O};font-weight:600;font-size:12px;color:{GREY};white-space:nowrap">{CENTER}Others</div></th>'
            f'</tr></thead><tbody>{body}</tbody></table></div>')

def strip_block(h): return BLOCK_RE.sub('', h or '')

def parse_block(h):
    """(name, rows) from a rendered block (old or new template) — used to re-render live descriptions after a template change.
    Returns None when the description has no block. The store row is dropped (render adds it)."""
    m = BLOCK_RE.search(h or '')
    if not m: return None
    b = m.group(0)
    # Template from 2026-09-10: the name is the SECOND line of the navy heading band. Older blocks (name in the first
    # <th> as "Tuzwa <name>") still parse — the th fallback keeps a live re-render possible from either template.
    band = re.search(r'>' + re.escape(HEADING) + r'</div>\s*<div[^>]*>([\s\S]*?)</div>', b)
    if band:
        raw = band.group(1)
    else:
        th = re.search(r'<th[^>]*>\s*(?:<div[^>]*>)?\s*([\s\S]*?)\s*(?:</div>)?\s*</th>', b)
        raw = th.group(1)
    name = html.unescape(re.sub(r'<[^>]+>', '', raw)).strip()
    if name.lower().startswith(BRAND.lower() + ' '): name = name[len(BRAND) + 1:]
    rows = []
    for tr in re.findall(r'<tr(?![^>]*vp-store)[^>]*>([\s\S]*?)</tr>', b):
        tds = re.findall(r'<td[^>]*>([\s\S]*?)</td>', tr)
        if len(tds) != 3: continue
        feat = html.unescape(re.sub(r'<[^>]+>', '', tds[0])).strip()
        oth = html.unescape(re.sub(r'<[^>]+>', '', tds[2])).strip()
        if oth in ('✕', '✕', '✘'): oth = '✘'
        rows.append((feat, oth))
    return name, rows

def q17():
    """True when the brief's Q17 says 'Add table'. Missing file or key = No table."""
    try: return bool(json.load(open('brief_flags.json')).get('q17_compare_table', False))
    except Exception: return False

def source_text(ex):
    parts = ex.get('facts', []) + [f"{s['name']} {s['value']}" for s in ex.get('specs', [])] + ex.get('package', []) \
        + ex.get('how_to_use', []) + [f"{q['q']} {q['a']}" for q in ex.get('faq_source', [])] \
        + [v['title'] for v in ex.get('variants', [])] + [str(ex.get(k, '')) for k in ('old_title', 'identity', 'productType')]
    return html.unescape(re.sub(r'<[^>]+>', ' ', ' '.join(parts))).lower()

def words(s): return [w for w in re.findall(r'[a-z]{4,}', s.lower()) if w not in STOP]

def foreign_numbers(text, src):
    """Numbers in a line that the source never states (user question 2026-09-06: value_check only guards that source values
    are PRESENT; nothing guarded that a number written in a block is one the source gave). Unit-free compare: '22.4' must
    occur in the source as 22.4 (also accepts 22,4)."""
    nums = re.findall(r'\d+(?:[.,]\d+)?', text)
    return [x for x in nums if x not in src and x.replace('.', ',') not in src and x.replace(',', '.') not in src]

if __name__ == '__main__':
    fails = 0
    if not q17():
        for n in sys.argv[1:]:
            n = int(n); path = f'final/d{n:02d}.json'; d = json.load(open(path))
            h = strip_block(d['descriptionHtml']); removed = h != d['descriptionHtml']
            if removed: d['descriptionHtml'] = h; json.dump(d, open(path, 'w'), ensure_ascii=False, indent=1)
            print(f'{n:02d} compare: Q17 = No table — no block' + (' (existing block removed)' if removed else ''))
        print('compare-build: Q17 = No table, 0 FAIL'); sys.exit(0)
    for n in sys.argv[1:]:
        n = int(n); path = f'final/d{n:02d}.json'; d = json.load(open(path)); ex = json.load(open(f'extract/p{n:02d}.json'))
        e = []; c = d.get('compare')
        if 'compare' in d and c is None:
            # rule doc §3: source with fewer than five separable parts — explicit opt-out, must be logged
            h = strip_block(d['descriptionHtml'])
            if h != d['descriptionHtml']: d['descriptionHtml'] = h; json.dump(d, open(path, 'w'), ensure_ascii=False, indent=1)
            if 'source too thin' not in (d.get('notes_for_log') or ''): fails += 1; print(f'[FAIL] {n:02d} compare: null without "compare: source too thin" in notes_for_log')
            else: print(f'{n:02d} compare: null — source too thin (logged), no block')
            continue
        if not isinstance(c, dict): e.append('compare object missing'); rows = []; name = ''
        else:
            name = str(c.get('name', '')).strip(); rows = c.get('rows') or []
            nw = len(name.split())
            if not 2 <= nw <= 5: e.append(f'name must be 2-5 words ({nw}): {name!r}')
            if BRAND.lower() in name.lower(): e.append('brand name inside name (the template adds it)')
            if len(rows) != 5: e.append(f'{len(rows)} product rows, need exactly 5')
            src = source_text(ex); neutral = 0
            for i, r in enumerate(rows, 1):
                f0 = str(r.get('feature', '')).strip(); o0 = str(r.get('others', '')).strip()
                f = imp(f0); o = o0 if o0 == '✘' else imp(o0)   # what the shopper sees (2026-09-11: imperial only)
                if not 20 <= len(f) <= 60: e.append(f'row {i} feature length {len(f)} (20-60): {f!r}')
                if COMPARE_WORDS.search(f): e.append(f'row {i} comparison wording in feature: {f!r}')
                if re.fullmatch(r'[\d\s.x×/\-–]+(?:in|cm|mm|kg|lb|oz|g|l|ml)?', f.lower()): e.append(f'row {i} spec-only row: {f!r}')
                if not (o == '✘' or 2 <= len(o) <= 14): e.append(f'row {i} others must be ✘ or 2-14 chars: {o!r}')
                if o != '✘': neutral += 1
                if not any(w in src for w in words(f0)): e.append(f'row {i} not traceable to source: {f0!r}')
                fn = foreign_numbers(f0, src)   # checked on the agent's text: the source figure may be metric, the rendered one is not
                if fn: e.append(f'row {i} number not in source {fn}: {f0!r}')
            if rows and neutral == 0: e.append('all five Others cells are ✘ — at least one product row must be neutral (e.g. "1 size", "Varies")')
        h = strip_block(d['descriptionHtml'])
        if '<h3>Key Features</h3>' not in h: e.append('no <h3>Key Features</h3> — nowhere to insert the block')
        if e:
            fails += 1; print(f'[FAIL] {n:02d} compare: ' + '; '.join(e))
        else:
            block = render(name, [(r['feature'], r['others']) for r in rows])
            d['descriptionHtml'] = h.replace('<h3>Key Features</h3>', block + '<h3>Key Features</h3>', 1)
            json.dump(d, open(path, 'w'), ensure_ascii=False, indent=1)
            print(f'{n:02d} compare: {BRAND} {imp(name)} | 5 rows, {neutral} neutral | block rendered before Key Features')
    print(f'compare-build: {fails} FAIL')
    sys.exit(1 if fails else 0)
