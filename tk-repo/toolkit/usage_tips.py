#!/usr/bin/env python3
"""usage_tips.py --extract [NN ...]  |  usage_tips.py NN [NN ...]  — the source's "Usage Tips" block becomes our own
<h3>Usage Tips</h3> list (added 2026-09-07, STR-DUB-2-batch1, user decision).

Rule (description-format-rule.md §7b): when the source carries a section headed Usage Tips / Usage Recommendations / Tips /
Usage Suggestions, our page carries a `<h3>Usage Tips</h3><ul>…</ul>` list with EVERY line of that block — one line = one
item, in the writer's own sentence (values verbatim, never pasted; same [COPY] measure as keyfeat_cover.py), with RULINGS
applied (a line that makes a forbidden claim — CPAP comparison, medical outcome, supplier policy — goes to omit_per_ruling).
Audience / occasion lines ("Perfect for busy families…") ARE usage tips when the source lists them there; they are never
written under How to Use (howto_check.py), which stays for real steps. Position: after Package Includes (and after How to
Use when present), before the fit block / <h3>FAQs</h3>. A product whose source has no such block gets no Usage Tips section.

--extract: reads raw/pNN.json, finds the block (heading text matching the pattern, list items or lines until the next
heading / spec / package / FAQ section) and writes extract.usage_tips (never overwrites a non-empty list — the extraction
agent may complete it by eye). Check mode (inside gate.py): (1) section present iff usage_tips non-empty; (2) every tip
present as an item (half its content words in one item) unless in omit_per_ruling; (3) no [COPY]; (4) one item per tip
([MERGED]); (5) position before the fit block / FAQs and after Package Includes. Exit 1 on any FAIL.
"""
import json, re, sys, os, html
from keyfeat_cover import toks, clean, is_copy, value_words, match_item, SECTION_END

HEAD = re.compile(r"^\s*(usage tips?|usage recommendations?|usage suggestions?|tips?(?: for use| & tricks)?|pro tips?|recommended uses?)\s*:?\s*$", re.I)

def source_tips(raw_html):
    h = raw_html or ""
    # find the heading (h2-h4, strong/b paragraph, or bare <p>) whose text matches HEAD
    for m in re.finditer(r"<(h[2-4]|strong|b|p)[^>]*>(.*?)</\1>", h, re.S | re.I):
        if HEAD.match(clean(m.group(2))):
            rest = h[m.end():]
            # cut at next heading or a section-ending bold/heading line
            cut = len(rest)
            for m2 in re.finditer(r"<(?:h[2-4]|strong|b)[^>]*>\s*([^<]{3,60})", rest, re.I):
                t = clean(m2.group(1))
                if SECTION_END.search(t) or HEAD.match(t) or re.match(r"^(key features?|features?|specifications?|package|faq|why choose|about)", t, re.I):
                    cut = m2.start(); break
            block = rest[:cut]
            items = [clean(x) for x in re.findall(r"<li[^>]*>(.*?)</li>", block, re.S | re.I)]
            if not items: items = [clean(x) for x in re.findall(r"<p[^>]*>(.*?)</p>", block, re.S | re.I)]
            if not items:
                items = [s.strip() for s in re.split(r"(?<=[.!?])\s+|<br\s*/?>", clean(block)) if len(s.split()) >= 3]
            return [x for x in items if x and len(x.split()) >= 3][:12]
    return []

def section(h):
    m = re.search(r"<h3[^>]*>\s*Usage Tips\s*</h3>(.*?)(<h3|<div class=\"vp-|$)", h or "", re.S | re.I)
    if not m: return None
    return [clean(x) for x in re.findall(r"<li[^>]*>(.*?)</li>", m.group(1), re.S | re.I) if clean(x)]

def present(t, items):
    w = toks(t)
    return any(sum(1 for x in w if x in set(toks(it))) * 2 >= len(w) for it in items) if w else True

if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "--extract":
        ids = [int(x) for x in args[1:]] or sorted(int(f[1:3]) for f in os.listdir("extract") if f.endswith(".json"))
        n_with = 0
        for n in ids:
            p = f"extract/p{n:02d}.json"; e = json.load(open(p)); r = json.load(open(f"raw/p{n:02d}.json"))
            if e.get("usage_tips"): n_with += 1; continue
            e["usage_tips"] = source_tips(r.get("descriptionHtml")); n_with += bool(e["usage_tips"])
            json.dump(e, open(p, "w"), ensure_ascii=False, indent=1)
            print(f"{n:02d} usage_tips: {len(e['usage_tips'])} source lines")
        print(f"usage_tips --extract: {n_with} of {len(ids)} products carry a Usage Tips block"); sys.exit(0)
    fails = 0
    for n in args:
        n = int(n); e = json.load(open(f"extract/p{n:02d}.json")); d = json.load(open(f"final/d{n:02d}.json")); h = d["descriptionHtml"]
        tips = e.get("usage_tips") or []; omit = [o.lower() for o in d.get("omit_per_ruling", [])]
        tips_req = [t for t in tips if not any(o and o in t.lower() for o in omit)]
        items = section(h); vals = value_words(e); bad = []
        if not tips_req:
            if items: bad.append(f"Usage Tips section present but the source has no usage-tips block (or every line is ruled out)")
        else:
            if items is None: bad.append(f"source has {len(tips_req)} usage-tip lines but no <h3>Usage Tips</h3> list")
            else:
                seen = {}
                for t in tips_req:
                    if not present(t, items): bad.append(f"tip missing: {t[:80]}")
                    else:
                        if is_copy(t, items, vals): bad.append(f"[COPY] tip pasted verbatim — same tip, your own sentence: {t[:80]}")
                        mi = match_item(t, items)
                        if mi is not None: seen.setdefault(mi, []).append(t)
                for k, v in seen.items():
                    if len(v) > 1: bad.append(f"[MERGED] one item carries {len(v)} tips — one tip = one item: {items[k][:60]!r}")
                pos = h.find("<h3>Usage Tips</h3>"); pk = h.find("<h3>Package Includes:</h3>"); fq = h.find("<h3>FAQs</h3>"); fit = h.find('<div class="vp-fit"')
                if pk != -1 and pos < pk: bad.append("Usage Tips must come after Package Includes")
                if (fit != -1 and pos > fit) or (fq != -1 and pos > fq): bad.append("Usage Tips must come before the fit block / FAQs")
                for t in tips:
                    if any(o and o in t.lower() for o in omit): print(f"  {n:02d} usage-tips [exempt] {t[:70]}")
        if bad:
            fails += 1
            for b in bad: print(f"[FAIL] {n:02d} usage-tips: {b}")
        else:
            print(f"{n:02d} usage-tips: " + (f"{len(tips_req)} tips, all present, 0 copies" if tips_req else "no source block, no section"))
    print(f"usage-tips: {fails} FAIL across {len(args)} products")
    sys.exit(1 if fails else 0)
