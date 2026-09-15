#!/usr/bin/env python3
"""keyfeat_cover.py NN [NN ...] — every source Key Features line must appear as an item of the NEW <h3>Key Features</h3> list.

Added 2026-09-06 (blr-batch26, user decision): the user compared p11's source Key Features (7 lines) with the live list
(5 items) — "FLAME-LIKE LED EFFECT" and "MIST OUTPUT" were carried by a benefit bullet and the prose, but not by the list.
value_check / fact_cover only ask whether the information is somewhere; spec_cover covers the Specifications list only.
This is spec_cover's twin for Key Features: the user's rule is that every source Key Features line is ALSO a list item,
whatever else in the page already says it (a bullet, the prose, the table). The list item is short "Name: one sentence";
the bullet stays benefit-led — same fact, different sentence.

Source side (`extract/pNN.json["key_features"]`, written by `python3 keyfeat_cover.py --extract` from raw/pNN.json):
  - every <li> of the source description that is NOT inside the Specifications / Package / FAQ / How-to-Use sections and
    is not itself a spec line (Name: value already in extract.specs) — this is the supplier's feature list;
  - every paragraph opening with a bold "Name:" lead outside those sections;
  - fallback when a source has none of those: its <h2>/<h3>/<h4> section headings (suppliers that write features as
    heading + paragraph pairs).
  A product whose source has no key-features material gets [] and is printed as [no source key features].
  The script PRE-FILLS the list; the extraction agent completes it by eye (EXTRACT-SPEC.md, 2026-09-06): lines the parser
  missed and the concrete features the source states only inside paragraphs. `--extract` therefore never overwrites an
  existing non-empty key_features list — it only adds parser lines that are not already present.
Match rule = spec_cover's: a source line counts as present when at least half of its content words (stop-words removed)
occur in one <li> of the new Key Features list (name + explanation); a reworded item passes, an absent one does not.
Lines in the doc's `omit_per_ruling` are skipped and printed as [exempt]. Exit 0 only when nothing is missing.

Copy check (added 2026-09-07, STR-DUB-2-batch1, user decision): a source line that is PASTED into the list is a FAIL —
description-format-rule.md §4 "same fact, different sentence, never a pasted copy". In that batch 88 of 240 source lines
reached the store verbatim because this script only asked "is it present?", and pasting is the cheapest way to be present.
The measure deliberately ignores the facts: numbers, units, measurements and value words (materials, colours, ratings,
model names — every token of extract.specs / package / variants) are removed from BOTH sides before comparing, so an agent
can never pass by altering a value; only the sentence fabric (word sequence of the remaining words) is compared. A line
whose fabric is 90%+ identical in sequence to the matched item is a copy. Lines with <= 6 remaining words are exempt
("Easy Care: Dishwasher safe" has no fabric to rewrite). Printed as [COPY]; counts as FAIL.
One source line = one item (added 2026-09-07, same batch, user decision): when one list item is the best match for two or
more source lines, the agent has merged them (p23 of that batch passed the presence check that way) → [MERGED], FAIL.
"""
import json, re, sys, html, os

STOP = set("a an the and or of for with to in on at is are be by from as it its your you not no this that can".split())
SECTION_END = re.compile(r"(specification|technical detail|what'?s (?:in the box|included)|package (?:include|content|list)|"
                         r"in the box|faq|frequently asked|how to use|instructions?|shipping|warranty|note:)", re.I)

def toks(s):
    s = re.sub(r"(\d+)\s*(?:h|hr|hrs|hours?)\b", r"\1 hour", s.lower())
    return [w.strip(".") for w in re.findall(r"[a-z0-9.]+", s) if w.strip(".") and w.strip(".") not in STOP]
def clean(s): return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()

def source_key_features(raw_html, specs, package=()):
    h = raw_html or ""
    # cut the description at the first heading/bold line that opens a non-feature section
    cut = len(h)
    for m in re.finditer(r"<(?:h\d|strong|b|p)[^>]*>\s*([^<]{3,60})", h, re.I):
        if SECTION_END.search(m.group(1)) and len(clean(m.group(1))) < 60:
            cut = min(cut, m.start()); break
    body = h[:cut]
    known = [toks(f"{s.get('name','')}: {s.get('value','')}") for s in specs] + [toks(p) for p in package]
    def is_known(t):   # a spec or package line the extract already carries elsewhere
        w = toks(t)
        return any(k and sum(1 for x in w if x in set(k)) * 2 >= len(w) for k in known)
    out = []
    for li in re.findall(r"<li[^>]*>(.*?)</li>", body, re.S | re.I):
        t = clean(li)
        if not t or len(t) < 4 or is_known(t) or re.match(r"^(key )?features?:?$", t, re.I): continue
        out.append(t)
    for p in re.findall(r"<p[^>]*>\s*<(?:strong|b)[^>]*>([^<]{3,80}:)\s*</(?:strong|b)>(.*?)</p>", body, re.S | re.I):
        t = clean(p[0] + " " + p[1])
        if t and t not in out: out.append(t)
    if not out:
        for hd in re.findall(r"<h[2-4][^>]*>(.*?)</h[2-4]>", body, re.S | re.I):
            t = clean(hd)
            if 3 <= len(t) <= 80 and t not in out: out.append(t)
    return out

def kf_items(h):
    m = re.search(r"<h3[^>]*>\s*Key Features\s*</h3>(.*?)(<h3|$)", h or "", re.S | re.I)
    if not m: return None
    return [clean(li) for li in re.findall(r"<li[^>]*>(.*?)</li>", m.group(1), re.S | re.I)]

def match_item(line, items):
    """index of the item that carries this source line (same rule as present()), or None"""
    t = toks(line)
    if not t: return None
    name, _, text = line.partition(":")
    nt, tt = (toks(name), toks(text)) if _ and len(toks(name)) <= 6 else ([], t)
    best = None
    for i, it in enumerate(items):
        w = set(toks(it)); sc = 0
        if sum(1 for x in t if x in w) * 2 >= len(t): sc = sum(1 for x in t if x in w) / max(len(t), 1) + 1
        elif nt and sum(1 for x in nt if x in w) * 2 >= len(nt) and (not tt or any(x in w for x in tt)): sc = 1
        elif nt and tt and sum(1 for x in tt if x in w) * 2 >= len(tt): sc = 0.9
        if sc and (best is None or sc > best[0]): best = (sc, i)
    return best[1] if best else None

def present(line, items):
    """spec_cover's rule (half the content words in one item), plus the Name: text form — the NAME half matched (>= half
    of its words) together with at least one content word of the text half counts as present, because supplier lines
    carry marketing padding ("PAIN-FREE PARADISE: Bid farewell to back and neck discomfort as this pillow provides…")."""
    t = toks(line)
    if not t: return True
    name, _, text = line.partition(":")
    nt, tt = (toks(name), toks(text)) if _ and len(toks(name)) <= 6 else ([], t)
    for it in items:
        w = set(toks(it))
        if sum(1 for x in t if x in w) * 2 >= len(t): return True
        if nt and sum(1 for x in nt if x in w) * 2 >= len(nt) and (not tt or any(x in w for x in tt)): return True
        if nt and tt and sum(1 for x in tt if x in w) * 2 >= len(tt): return True
    return False

def fabric(s, values):
    w = [x for x in re.findall(r"[a-z]+", s.lower()) if x not in STOP and x not in values and len(x) > 2]
    return w
def lcs(a, b):
    m = [[0]*(len(b)+1) for _ in range(len(a)+1)]
    for i in range(len(a)):
        for j in range(len(b)):
            m[i+1][j+1] = m[i][j]+1 if a[i] == b[j] else max(m[i][j+1], m[i+1][j])
    return m[len(a)][len(b)]
def is_copy(line, items, values, thr=0.9, minwords=7):
    a = fabric(line, values)
    if len(a) < minwords: return None
    best = None
    for it in items:
        b = fabric(it, values)
        if not b: continue
        r = lcs(a, b) / max(len(a), 1)
        if best is None or r > best[0]: best = (r, it)
    return best[1] if best and best[0] >= thr else None
def value_words(e):
    v = set()
    for sp in e.get("specs", []): v |= set(re.findall(r"[a-z]+", f"{sp.get('name','')} {sp.get('value','')}".lower()))
    for pk in e.get("package", []): v |= set(re.findall(r"[a-z]+", pk.lower()))
    for vr in e.get("variants", []): v |= set(re.findall(r"[a-z]+", (vr.get("title") or "").lower()))
    v |= set("mm cm in inch inches ft oz lb lbs kg g ml l mah w v hz db lumens lumen hours hour hrs min minutes".split())
    return v - STOP

if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "--extract":
        for n in args[1:] or sorted(int(f[1:3]) for f in os.listdir("extract") if f.endswith(".json")):
            n = int(n); p = f"extract/p{n:02d}.json"; e = json.load(open(p)); r = json.load(open(f"raw/p{n:02d}.json"))
            found = source_key_features(r.get("descriptionHtml"), e.get("specs", []), e.get("package", []))
            have = e.get("key_features") or []
            e["key_features"] = have + [x for x in found if not present(x, have)]   # keep the agent's additions
            json.dump(e, open(p, "w"), ensure_ascii=False, indent=1)
            print(f"{n:02d} key_features: {len(e['key_features'])} source lines")
        sys.exit(0)
    fails = 0; checked = 0
    for n in args:
        n = int(n); e = json.load(open(f"extract/p{n:02d}.json")); d = json.load(open(f"final/d{n:02d}.json"))
        src = e.get("key_features")
        if src is None:
            print(f"[FAIL] {n:02d} keyfeat: extract has no key_features — run `python3 keyfeat_cover.py --extract {n:02d}` first"); fails += 1; continue
        if not src: print(f"{n:02d} keyfeat: [no source key features]"); continue
        items = kf_items(d["descriptionHtml"])
        if items is None: print(f"[FAIL] {n:02d} keyfeat: no <h3>Key Features</h3> list"); fails += 1; continue
        omit = [o.lower() for o in d.get("omit_per_ruling", [])]
        missing = []; copies = []; merged = {}; vals = value_words(e)
        for line in src:
            checked += 1
            if any(o and o in line.lower() for o in omit): print(f"  {n:02d} keyfeat [exempt] {line[:70]}"); continue
            if not present(line, items): missing.append(line); continue
            mi = match_item(line, items)
            if mi is not None: merged.setdefault(mi, []).append(line)
            c = is_copy(line, items, vals)
            if c: copies.append((line, c))
        merged = {k: v for k, v in merged.items() if len(v) > 1}   # one item carrying 2+ source lines (2026-09-07, user decision)
        if missing or copies or merged:
            fails += 1
            for mline in missing: print(f"[FAIL] {n:02d} keyfeat missing from Key Features list: {mline[:110]}")
            for line, it in copies: print(f"[FAIL] {n:02d} keyfeat [COPY] source line pasted into the list — same facts, your own sentence: {line[:90]}")
            for k, v in merged.items(): print(f"[FAIL] {n:02d} keyfeat [MERGED] one item carries {len(v)} source lines — one source line = one item: {items[k][:60]!r} <- {[x[:40] for x in v]}")
        else:
            print(f"{n:02d} keyfeat: {len(src)} source lines, all in the list, 0 copies, 0 merged")
    print(f"keyfeat-cover: {fails} FAIL ({checked} source key-feature lines checked across {len(args)} products; copy + merge check on)")
    sys.exit(1 if fails else 0)
