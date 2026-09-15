#!/usr/bin/env python3
"""kf_review_input.py [--all] [--min-words N] [NN ...] — build kf_review_input.json for the independent KF/spec reader
(KF-REVIEW-SPEC.md). Zero model tokens. Added 2026-09-07 (STR-DUB-2-batch1, user decision).

Eligible product = its source paragraph text (outside lists and outside the spec / package / FAQ / how-to sections, as
para_feat.paragraphs() cuts it) has more than --min-words words (default 80). A shorter source is a heading plus the list the
script already copied into key_features — the reader would only find marketing sentences there. --all includes every product.
Prints `kf_review_input: N eligible of M (min N words)`; the run log quotes it.
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from para_feat import paragraphs

if __name__ == "__main__":
    args = sys.argv[1:]; allp = "--all" in args; args = [a for a in args if a != "--all"]; minw = 80
    if "--min-words" in args: i = args.index("--min-words"); minw = int(args[i+1]); args = args[:i] + args[i+2:]
    ids = [int(x) for x in args] or sorted(int(f[1:3]) for f in os.listdir("extract") if f.endswith(".json"))
    out = []
    for n in ids:
        e = json.load(open(f"extract/p{n:02d}.json")); r = json.load(open(f"raw/p{n:02d}.json"))
        sents = paragraphs(r.get("descriptionHtml")); words = sum(len(s.split()) for s in sents)
        if not allp and words <= minw: continue
        out.append({"idx": f"{n:02d}", "identity": e.get("identity", ""), "paragraph_words": words, "paragraphs": sents,
                    "key_features": e.get("key_features") or [],
                    "specs": [f"{s.get('name','')}: {s.get('value','')}" for s in e.get("specs") or []],
                    "package": e.get("package") or []})
    json.dump(out, open("kf_review_input.json", "w"), ensure_ascii=False, indent=1)
    print(f"kf_review_input: {len(out)} eligible of {len(ids)} (min {minw} words)" + ("" if out else " — nothing for the reader; log the line and continue"))
