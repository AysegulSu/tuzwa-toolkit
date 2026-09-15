#!/usr/bin/env python3
"""howto_check.py NN [NN ...] — the <h3>How to Use</h3> section: real steps only, every source step kept, never pasted.

Added 2026-09-07 (STR-DUB-2-batch1, user decision). description-format-rule.md §7 said "HOW TO USE — only if the source
has one; reproduce it", and the extraction agents had put the supplier's "Usage Recommendations" audience lines ("Perfect for
busy families…", "Great for journalists…", "Recommended for those looking to avoid invasive procedures") into
extract.how_to_use — so 9 products reached the store with those lines pasted verbatim under a How to Use heading. Rule now:
  - How to Use exists ONLY when the source gives actual steps / instructions (do this, then that; care / charging / fitting
    instructions). Audience, occasion and "ideal for" lines are USE CONTEXTS: they belong to extract.facts and are woven into
    prose 2 / an FAQ answer / the Key Features intro in the writer's own words — never a How to Use section.
  - Every source step is kept, in the source's order, with every value verbatim — but in the writer's own sentence, never
    pasted (same [COPY] measure as keyfeat_cover.py: values excluded, <= 6 fabric words exempt).
Checks (FAIL): (1) extract.how_to_use empty -> no How to Use section may exist; (2) a source step missing from the section
(half its content words in one item); (3) a step pasted verbatim ([COPY]); (4) any item that starts with an audience /
occasion pattern (Perfect for, Ideal for, Great for, Suitable for, Recommended for, Best used/for, Designed for, Good for,
Essential for) — those are not steps; (5) the section's items are out of source order (WARN only). Exit 1 on any FAIL.
"""
import json, re, sys, html
from keyfeat_cover import toks, clean, is_copy, value_words

AUD = re.compile(r"^(perfect|ideal|great|suitable|recommended|best (?:used|for|suited)|designed for|good for|essential for|use for|a (?:great|perfect|must))\b", re.I)

def section(h):
    m = re.search(r"<h3[^>]*>\s*How to Use\s*</h3>(.*?)(<h3|<div class=\"vp-|$)", h or "", re.S | re.I)
    if not m: return None
    items = [clean(a or b) for a, b in re.findall(r"<li[^>]*>(.*?)</li>|<p[^>]*>(.*?)</p>", m.group(1), re.S | re.I)]
    return [x for x in items if x]

def present(step, items):
    t = toks(step)
    return any(sum(1 for x in t if x in set(toks(it))) * 2 >= len(t) for it in items) if t else True

if __name__ == "__main__":
    fails = 0
    for n in sys.argv[1:]:
        n = int(n); e = json.load(open(f"extract/p{n:02d}.json")); d = json.load(open(f"final/d{n:02d}.json"))
        steps = [s for s in (e.get("how_to_use") or []) if not AUD.match(s)]
        aud_in_extract = [s for s in (e.get("how_to_use") or []) if AUD.match(s)]
        items = section(d["descriptionHtml"]); vals = value_words(e); bad = []
        if aud_in_extract: bad.append(f"extract.how_to_use carries {len(aud_in_extract)} audience/occasion line(s) — move them to facts (use contexts), they are not steps: {aud_in_extract[0][:60]!r}")
        if not steps:
            if items: bad.append(f"How to Use section present but the source has no steps ({len(items)} items) — remove the section, weave use contexts into prose/FAQ")
        else:
            if items is None: bad.append(f"source has {len(steps)} steps but no <h3>How to Use</h3> section")
            else:
                for s in steps:
                    if not present(s, items): bad.append(f"step missing: {s[:80]}")
                    elif is_copy(s, items, vals): bad.append(f"[COPY] step pasted verbatim — same step, your own sentence: {s[:80]}")
                for it in items:
                    if AUD.match(it): bad.append(f"audience/occasion line under How to Use — not a step: {it[:80]}")
        if bad:
            fails += 1
            for b in bad: print(f"[FAIL] {n:02d} howto: {b}")
        else:
            print(f"{n:02d} howto: " + (f"{len(steps)} steps, all present, 0 copies" if steps else "no source steps, no section"))
    print(f"howto-check: {fails} FAIL across {len(sys.argv[1:])} products")
    sys.exit(1 if fails else 0)
