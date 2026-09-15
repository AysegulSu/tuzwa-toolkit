#!/usr/bin/env python3
"""value_check.py NN [NN ...] — "no source value is dropped" gate (user decision 2026-09-04, zero model tokens).

Compares every VALUE in extract/pNN.json against the tag-stripped text of final/dNN.json descriptionHtml.
Wording is free (the description is a rewrite); values are not.

HARD (FAIL — product cannot be pushed):
  - every number in specs values, package items, how_to_use steps, variant titles and spec-like facts lines ("Name: value")
    must appear in the description (12.5FT -> 12.5; 155 x 120 x 60 mm -> 155, 120, 60; both units of a dual-unit value)
  - every item of a list-valued spec (>= 3 comma/slash-separated items: resolution options, colors, materials, modes,
    frequency bands) must appear (an item = at least one of its content-word stems present)
  - every package item and every variant option value (color / size names) must appear
  - verbal spec values (no number, < 3 items — "Material: cotton", "Closure: zipper"): at least half of the content-word
    stems must appear. Was a WARN until 2026-09-06 (user decision): a numberless value could be changed or dropped and the
    product still passed — "cotton" -> "polyester" was only a warning while "300 g" -> nothing was a FAIL. A value the
    writer must not print (supplier boilerplate such as "Type: Other") goes into omit_per_ruling via RULINGS.md, exactly
    like a dropped number; the description itself stays silent about it.

Exemptions: final/dNN.json may carry "omit_per_ruling": ["<exact source value or item>" or "<Name: value>", ...] for values RULINGS.md
says to drop (e.g. a wrong colour list, carton dimensions). Each exemption is printed so the log shows it.
Exit 1 on any FAIL.
"""
import json, re, sys, html
STOP = {"with", "that", "this", "your", "from", "into", "than", "then", "them", "they", "have", "will", "when", "while",
        "also", "each", "every", "over", "just", "more", "most", "about", "after", "before", "their", "there", "these",
        "those", "which", "what", "where", "even", "both", "make", "makes", "made", "keep", "keeps", "gets", "give",
        "gives", "take", "takes", "come", "comes", "need", "needs", "like", "same", "much", "very", "only", "and", "the",
        "for", "you", "our", "its", "all", "any", "can", "are", "not", "but", "one", "two", "use", "used", "using"}
def txt(h): return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', h))).lower()
def nums(s): return re.findall(r'\d+(?:\.\d+)?', s)
def stem(w): return w[:5] if len(w) > 5 else w
def cw(s): return [w for w in re.findall(r'[a-z]{3,}', s.lower()) if w not in STOP]
def items(v):
    # a real list: >=3 comma/slash/semicolon-separated SHORT items (each <=4 words, <=30 chars), not a sentence
    if v.strip().endswith('.') or len(v) > 160: return []
    parts = [re.sub(r'^(and|or)\s+', '', p.strip()) for p in re.split(r',|/|;', v) if p.strip()]
    return parts if len(parts) >= 3 and all(len(p.split()) <= 4 and len(p) <= 30 for p in parts) else []
fails = 0
for n in sys.argv[1:]:
    n = int(n); d = json.load(open(f'final/d{n:02d}.json')); ex = json.load(open(f'extract/p{n:02d}.json'))
    T = txt(d['descriptionHtml']); Tn = set(nums(T)); Ts = {stem(w) for w in re.findall(r'[a-z]{3,}', T)}
    omit = [o.lower() for o in d.get('omit_per_ruling', [])]
    def exempt(v, name=''):
        # an omit_per_ruling entry may be the bare value ("Other") or the "Name: value" form ("Type: Other")
        return any(o == v.lower() or o in v.lower() or (name and o == f"{name}: {v}".lower()) for o in omit)
    def F(kind, name, detail):
        global fails; fails += 1; print(f"[FAIL] {n:02d} {kind} — {name}: {detail}")
    def W(kind, name, detail): print(f"[WARN] {n:02d} {kind} — {name}: {detail}")
    # collect (name, value, source) pairs
    vals = [(s['name'], str(s['value']), 'specs') for s in ex['specs']]
    for f in ex['facts']:
        m = re.match(r'^([A-Z][A-Za-z0-9 /()\-]{2,40}):\s*(.+)$', f)
        # spec-like facts line: short value, not a sentence, not a writer/source note
        if m and len(m.group(2)) < 120 and not m.group(2).rstrip().endswith('.') and not re.search(r'the source|listed|stated|not applicable', m.group(2), re.I):
            vals.append((m.group(1), m.group(2), 'facts'))
    for p in ex['package']: vals.append(('Package', p, 'package'))
    for h in ex['how_to_use']: vals.append(('How to use', h, 'how_to_use'))
    seen = set()
    for name, v, src in vals:
        key = (name.lower(), v.lower())
        if key in seen: continue
        seen.add(key)
        if exempt(v, name): print(f"[exempt] {n:02d} {name}: {v[:60]}"); continue
        miss_n = [x for x in nums(v) if x not in Tn and x.rstrip('0').rstrip('.') not in Tn]
        if miss_n: F('number', name, f"{miss_n} missing (source: {v[:80]})")
        li = items(v)
        if li:
            def item_ok(it):
                w = cw(it); hit = sum(stem(x) in Ts for x in w)
                return (not w) or any(x in Tn for x in nums(it)) or (hit == len(w) if len(w) <= 2 else hit / len(w) >= 0.5)
            miss_i = [it for it in li if not item_ok(it)]
            if miss_i: F('list item', name, f"{miss_i} missing (source: {v[:80]})")
        elif src == 'package':
            w = cw(v)
            if w and sum(stem(x) in Ts for x in w) / len(w) < 0.5: F('package item', name, f"'{v}' not found")
        elif not nums(v):
            w = cw(v)
            if w and sum(stem(x) in Ts for x in w) / len(w) < 0.5: F('verbal value', name, f"'{v[:80]}' — {sum(stem(x) in Ts for x in w)}/{len(w)} words present (FAIL since 2026-09-06; ruling -> omit_per_ruling)")
    # variants: every option value
    opts = set()
    for var in ex['variants']:
        for part in var['title'].split(' / '):
            if part.strip() and part.strip().lower() != 'default title': opts.add(part.strip())
    for o in sorted(opts):
        if exempt(o): print(f"[exempt] {n:02d} variant: {o}"); continue
        ok = any(x in Tn for x in nums(o)) or any(stem(w) in Ts for w in cw(o)) or o.lower() in T
        if not ok: F('variant', 'option', f"'{o}' not found")
    print(f"{n:02d} value-check: {len(vals)} values, {len(opts)} variant options checked")
print(f"value-check: {fails} FAIL")
sys.exit(1 if fails else 0)
