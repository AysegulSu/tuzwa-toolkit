#!/usr/bin/env python3
"""fit_build.py NN [NN ...] — render the "Right for you if" block into final/dNN.json (zero model tokens).

Rule: rules/fit-block-rule.md (brief Q19, user decision 2026-09-06). The description agent writes only the CONTENT —
a `fit` object {"for": [exactly 4 lines]} — or `"fit": null` with notes_for_log "fit: not applicable" for a product where the
block adds nothing (consumables, one-size accessories). This script owns the HTML: a single-column template in the theme
colours, inserted immediately before `<h3>FAQs</h3>`, replacing any block already there. Idempotent.

2026-09-06 (user decision, blr-batch26 test product): the block is ONE column — "Right for you if" only. The former right
column "Not the right fit if" (`not_for`) is removed entirely: a wrong "not for" line kills a sale silently and is never
seen, so no such line is written any more. A `not_for` key in the fit object is ignored and reported; the block moved from
before Key Features to directly before the FAQs (same user decision).

2026-09-07 (user decision, conversion revision): every line is `situation — proof`: the buyer's situation, an em dash
(` — `), then the source fact that answers it (`You want something weighted to hold in stressful moments — it weighs
1.2 lb`). A line without the dash + proof FAILs; a proof that is not traceable to the extract FAILs; length 30–110.
Generic-audience lines (`any age`, `anyone`, `everyone`) FAIL — they persuade nobody. The script also renders a FIXED
closing sentence under the four lines (CLOSE below); the agent never writes it.

Flag: brief_flags.json {"q19_fit_block": true|false}; false or missing = Skip: any existing block is removed, nothing required.

Units (2026-09-11, user decision): the rendered lines are IMPERIAL ONLY — `unit_dual.imperial_only()` converts a metric
figure and drops it before rendering ("155 cm" -> "61 in"); the traceability / foreign-number checks run on the agent's own
text against the source, the length check on the converted line. Same rule as compare_build.py.

Checks (FAIL = exit 1): for exactly 4 lines (fixed at 4 on 2026-09-06, user decision — 3 looks empty in one column), each 30–110 chars
with exactly one ` — ` (2026-09-07); the whole line AND the proof part traceable to the extract (one content word, same test
as compare_build.py); every number in the line present in the source; no comparison wording; no generic audience; no brand name.
"""
import json, re, sys, html
from compare_build import source_text, words, BRAND, foreign_numbers
FIT_COMPARE = re.compile(r'\b(?:unlike|ordinary|regular|typical|cheap(?:er|est)?|other brands?|competitors?|than (?:other|most|ordinary|cheap))\b', re.I)   # 'larger than the L size' is a legitimate limit
FIT_GENERIC = re.compile(r'\b(?:any age|anyone|everyone|everybody)\b', re.I)   # 2026-09-07: a line for everyone persuades no one
DASH = ' — '
CLOSE = 'If two or more of these sound like you, this is the one.'   # fixed closing sentence, script-owned (2026-09-07)

GREEN, NAVY = '#2e9e4f', '#000096'   # NAVY — MEASURED ON TUZWA 2026-09-12 from the live MAIN theme
# 'Xtra -- NEW' (gid://shopify/OnlineStoreTheme/161796391136), config/settings_data.json, default scheme-1
# buy_button_color, read through the Shopify connector (the script-route app has no read_themes and tuzwa.com is
# blocked from the container). GREEN is a fixed success colour, not from any theme.
BLOCK_RE = re.compile(r'<div class="vp-fit"[\s\S]*?</div>\s*</div>\s*</div>')

def q19():
    try: return bool(json.load(open('brief_flags.json')).get('q19_fit_block', False))
    except Exception: return False

def strip_block(h): return BLOCK_RE.sub('', h or '')

def imp(text):
    """Imperial-only text (2026-09-11). Lazy import: unit_dual imports this module's BLOCK_RE."""
    from unit_dual import imperial_only
    return imperial_only(text)

def li(text):
    icon = f'<span style="flex:none;width:22px;height:22px;border-radius:50%;border:2px solid {GREEN};color:{GREEN};font-size:13px;line-height:22px;text-align:center;font-weight:700">&#10003;</span>'
    return f'<li style="display:flex;gap:10px;margin:0 0 9px">{icon}<span>{html.escape(text.strip())}</span></li>'

def render(for_):
    return (f'<div class="vp-fit" style="margin:28px 0;border:1px solid #e3e3e3;border-radius:12px;overflow:hidden;background:#fff"><div style="display:flex;flex-wrap:wrap">'
            f'<div style="flex:1 1 260px;padding:16px 18px;"><div style="font-weight:700;font-size:16px;color:{NAVY};margin-bottom:10px">Right for you if</div>'
            f'<ul style="list-style:none;margin:0;padding:0;font-size:15px;line-height:1.4">{"".join(li(imp(t)) for t in for_)}</ul>'
            f'<p style="margin:12px 0 0;font-size:15px;font-weight:700;color:{NAVY}">{CLOSE}</p></div>'
            f'</div></div>')

if __name__ == '__main__':
    fails = 0
    if not q19():
        for n in sys.argv[1:]:
            n = int(n); path = f'final/d{n:02d}.json'; d = json.load(open(path))
            h = strip_block(d['descriptionHtml']); removed = h != d['descriptionHtml']
            if removed: d['descriptionHtml'] = h; json.dump(d, open(path, 'w'), ensure_ascii=False, indent=1)
            print(f'{n:02d} fit: Q19 = Skip — no block' + (' (existing block removed)' if removed else ''))
        print('fit-build: Q19 = Skip, 0 FAIL'); sys.exit(0)
    for n in sys.argv[1:]:
        n = int(n); path = f'final/d{n:02d}.json'; d = json.load(open(path)); ex = json.load(open(f'extract/p{n:02d}.json'))
        e = []; c = d.get('fit'); h = strip_block(d['descriptionHtml'])
        if 'fit' in d and c is None:
            if h != d['descriptionHtml']: d['descriptionHtml'] = h; json.dump(d, open(path, 'w'), ensure_ascii=False, indent=1)
            if 'fit: not applicable' not in (d.get('notes_for_log') or ''): fails += 1; print(f'[FAIL] {n:02d} fit: null without "fit: not applicable" in notes_for_log')
            else: print(f'{n:02d} fit: null — not applicable (logged), no block')
            continue
        if not isinstance(c, dict): e.append('fit object missing')
        else:
            src = source_text(ex)
            for0 = [str(x).strip() for x in (c.get('for') or [])]
            for_ = [imp(t) for t in for0]   # what the shopper sees (2026-09-11: imperial only)
            if c.get('not_for'): print(f'  {n:02d} fit: not_for ignored — the block is one column since 2026-09-06 ({len(c["not_for"])} line(s) dropped)')
            if len(for_) != 4: e.append(f'for: {len(for_)} lines (need exactly 4)')
            for side, lines in (('for', for_),):
                for i, t in enumerate(lines, 1):
                    t0 = for0[i - 1]   # the agent's own text — source checks run on it
                    if not 30 <= len(t) <= 110: e.append(f'{side} {i} length {len(t)} (30-110): {t!r}')
                    if FIT_COMPARE.search(t): e.append(f'{side} {i} comparison wording: {t!r}')
                    if FIT_GENERIC.search(t): e.append(f'{side} {i} generic audience (any age / anyone / everyone): {t!r}')
                    if BRAND.lower() in t.lower(): e.append(f'{side} {i} brand name')
                    if t.count(DASH) != 1: e.append(f'{side} {i} needs exactly one " — " (situation — proof): {t!r}')
                    else:
                        proof = t0.split(DASH, 1)[1].strip()
                        if len(proof) < 8: e.append(f'{side} {i} proof too short: {proof!r}')
                        elif not any(w in src for w in words(proof)): e.append(f'{side} {i} proof not traceable to source: {proof!r}')
                    if not any(w in src for w in words(t0)): e.append(f'{side} {i} not traceable to source: {t0!r}')
                    fn = foreign_numbers(t0, src)
                    if fn: e.append(f'{side} {i} number not in source {fn}: {t0!r}')
        if '<h3>FAQs</h3>' not in h: e.append('no <h3>FAQs</h3> — nowhere to insert the block')
        if e: fails += 1; print(f'[FAIL] {n:02d} fit: ' + '; '.join(e)); continue
        d['descriptionHtml'] = h.replace('<h3>FAQs</h3>', render(for_) + '<h3>FAQs</h3>', 1)
        json.dump(d, open(path, 'w'), ensure_ascii=False, indent=1)
        print(f'{n:02d} fit: {len(for_)} for + close line | block rendered before FAQs')
    print(f'fit-build: {fails} FAIL')
    sys.exit(1 if fails else 0)
