#!/usr/bin/env python3
"""spec_cover.py NN [NN ...] — every source spec line must appear in the NEW <h3>Specifications</h3> list.

Why this exists and why value_check.py is not enough (added 2026-09-04, user decision after blr-batch22):
value_check.py asks "does this source value appear ANYWHERE in the description?" — a spec satisfied by a
benefit bullet passes it. This check asks the stricter question the format rule actually requires
(description-format-rule.md §5 "Structured attribute list — every available product-specific attribute in a
clear list", and the forbidden "DELETING A SHORT SPEC LINE"): is the source spec line present AS AN ITEM of
the Specifications list? In blr-batch22 the two answers differed by 112 lines across 32 of 50 products.

Compares extract/pNN.json["specs"] against the <li> items under <h3>Specifications</h3> in
final/dNN.json["descriptionHtml"]. A line counts as present when at least half of its content words
(name + value, stop-words removed) appear in one <li>, so a reworded line
("Available sizes: S and L" -> "Sizes: S, L") passes and a genuinely absent one does not.
Lines listed in the doc's `omit_per_ruling` are skipped and printed as [exempt].

Exit 0 only when nothing is missing.
"""
import json, re, sys, html

STOP = set("a an the and or of for with to in on at is are be by from as it its your you not no".split())

def toks(s):
    return [w for w in re.findall(r"[a-z0-9.]+", s.lower()) if w not in STOP]

def spec_items(h):
    m = re.search(r"<h3[^>]*>\s*Specifications[^<]*</h3>(.*?)(<h3|$)", h or "", re.S | re.I)
    if not m:
        return None
    return [html.unescape(re.sub(r"<[^>]+>", "", li)).strip()
            for li in re.findall(r"<li[^>]*>(.*?)</li>", m.group(1), re.S)]

def main(ids):
    missing = 0
    checked = 0
    for n in ids:
        n = int(n)
        ex = json.load(open(f"extract/p{n:02d}.json"))
        d = json.load(open(f"final/d{n:02d}.json"))
        items = spec_items(d["descriptionHtml"])
        if items is None:
            print(f"[FAIL] {n:02d} no <h3>Specifications</h3> list in the description")
            missing += 1
            continue
        sets = [set(toks(i)) for i in items]
        omit = " ".join(d.get("omit_per_ruling", [])).lower()
        for s in ex["specs"]:
            name, val = s["name"], str(s["value"])
            if (val.lower()[:18] and val.lower()[:18] in omit) or name.lower() in omit:
                print(f"[exempt] {n:02d} {name}: {val[:60]}")
                continue
            want = set(toks(val)) | set(toks(name))
            if not want:
                continue
            checked += 1
            best = max((len(want & g) / len(want) for g in sets), default=0)
            if best < 0.5:
                print(f"[FAIL] {n:02d} spec line missing from the Specifications list — {name}: {val[:70]}")
                missing += 1
    print(f"spec-cover: {missing} FAIL ({checked} source spec lines checked across {len(ids)} products)")
    return 1 if missing else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
