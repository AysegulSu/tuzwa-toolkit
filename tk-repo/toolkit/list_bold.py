#!/usr/bin/env python3
"""list_bold.py NN [NN ...] — two zero-token fixes on final/dNN.json (user instruction 2026-09-11, ddl2 pregnancy pillow live):

1. BOLD LEAD-INS in the Key Features and Specifications lists. Every <li> of `<h3>Key Features</h3>` and
   `<h3>Specifications</h3>` is `<li><strong>Name:</strong> text</li>` — the name AND its colon inside <strong>, one space,
   then the text. A plain `U-Shape Support: Back, hips …` reached the store although description-format-rule.md §4 / §5
   have asked for the bold form since 2026-09-07; nothing enforced it. This script wraps a plain leading `Name:` (1–7
   words, no tag inside) in <strong>, normalises `<strong>Name</strong>:` and `<strong>Name: </strong>` to the canonical
   form, and leaves an item that already has it untouched. An item with NO `Name:` lead at all is not invented — it is
   reported and struct-check.py FAILs it (the agent writes the name).

2. SPACE UNDER THE SECOND IMAGE. The second description image (the one between Key Features and Specifications; the
   Q18 `vp-dim` image is not counted) sits flush on the heading that follows it. The <img> gets
   `display:block;margin-bottom:24px` (appended to an existing style attribute, or a new one). Idempotent: an <img> that
   already carries `margin-bottom` is left alone. Only the src list is what gate.py / verify.py compare, so the added
   style does not disturb the image checks; the tag's other attributes are untouched (re-host rule).

Runs inside gate.py right after fit-build, BEFORE the gate loads the finals for the other checks. Prints one line per
product and a summary; exit 0 always (struct-check.py is the gate that fails a remaining plain lead-in).
"""
import json, re, sys

LEAD = re.compile(r'^(\s*)([^<:]{1,80}?):(\s*)')          # plain "Name:" at the start of an <li>
STRONG_A = re.compile(r'^(\s*)<strong>\s*([^<]*?)\s*</strong>\s*:\s*')   # <strong>Name</strong>: text
STRONG_B = re.compile(r'^(\s*)<strong>\s*([^<]*?)\s*:\s*</strong>\s*')   # <strong>Name:</strong> text / <strong>Name: </strong>text
GAP = 'display:block;margin-bottom:24px'

def fix_li(inner):
    """Return (new_inner, status): status = 'ok' (already canonical), 'fixed', or 'plain' (no Name: lead at all)."""
    m = STRONG_B.match(inner) or STRONG_A.match(inner)
    if m:
        new = f'<strong>{m.group(2).strip()}:</strong> ' + inner[m.end():].lstrip()
        return (inner, 'ok') if new == inner else (new, 'fixed')
    m = LEAD.match(inner)
    if m and len(m.group(2).split()) <= 7:
        return f'<strong>{m.group(2).strip()}:</strong> ' + inner[m.end():].lstrip(), 'fixed'
    return inner, 'plain'

def fix_list(h, heading):
    """Fix every <li> of the <ul> that follows <h3>heading</h3>. Returns (html, fixed, plain_items)."""
    start = h.find(f'<h3>{heading}</h3>')
    if start < 0: return h, 0, []
    ul0 = h.find('<ul', start); ul1 = h.find('</ul>', ul0)
    nxt = h.find('<h3', start + 5)
    if ul0 < 0 or ul1 < 0 or (nxt >= 0 and ul0 > nxt): return h, 0, []
    seg = h[ul0:ul1]; fixed = 0; plain = []
    def rep(m):
        nonlocal fixed
        new, st = fix_li(m.group(2))
        if st == 'fixed': fixed += 1
        elif st == 'plain': plain.append(re.sub(r'<[^>]+>', '', m.group(2)).strip()[:50])
        return m.group(1) + new + '</li>'
    seg = re.sub(r'(<li[^>]*>)(.*?)</li>', rep, seg, flags=re.S)
    return h[:ul0] + seg + h[ul1:], fixed, plain

def gap_second_image(h):
    """Add the bottom margin to the second non-vp-dim <img>. Returns (html, changed)."""
    tags = [m for m in re.finditer(r'<img\b[^>]*>', h) if 'class="vp-dim"' not in m.group(0)]
    if len(tags) < 2: return h, False
    m = tags[1]; tag = m.group(0)
    if 'margin-bottom' in tag: return h, False
    sm = re.search(r'\sstyle="([^"]*)"', tag)
    if sm:
        old = sm.group(1).rstrip().rstrip(';')
        new = tag[:sm.start(1)] + (old + ';' if old else '') + GAP + tag[sm.end(1):]
    else:
        new = tag[:-1].rstrip('/').rstrip() + f' style="{GAP}"' + ('/>' if tag.endswith('/>') else '>')
    return h[:m.start()] + new + h[m.end():], True

if __name__ == '__main__':
    tf = tp = tg = 0
    for a in sys.argv[1:]:
        n = int(a); p = f'final/d{n:02d}.json'; d = json.load(open(p)); h = d['descriptionHtml']
        h, f1, p1 = fix_list(h, 'Key Features'); h, f2, p2 = fix_list(h, 'Specifications'); h, g = gap_second_image(h)
        if h != d['descriptionHtml']: d['descriptionHtml'] = h; json.dump(d, open(p, 'w'), ensure_ascii=False, indent=1)
        plain = [f'KF: {x}' for x in p1] + [f'Spec: {x}' for x in p2]
        print(f'{n:02d} list-bold: {f1} KF + {f2} spec lead-ins bolded, image-2 gap {"added" if g else "present/none"}'
              + (f' | NO "Name:" lead (agent must add): {plain}' if plain else ''))
        tf += f1 + f2; tp += len(plain); tg += g
    print(f'list-bold: {tf} lead-in(s) bolded, {tg} image gap(s) added, {tp} item(s) without a "Name:" lead across {len(sys.argv) - 1} products')
