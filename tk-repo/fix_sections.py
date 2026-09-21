#!/usr/bin/env python3
"""fix_sections.py — main-context triage of sections.py --extract output (ddl2-batch28).

Three deterministic corrections, all of them the [UNMAPPED] decision the README hands to the
main context (README step 3e), applied here as code so all 50 products are treated identically:

 1. "Why You'll Love It" is this supplier's KEY FEATURES block, not a fact section. Its lines go
    back into extract.key_features (sections.py had moved them out) and the section is dropped.
 2. A pseudo-section whose heading_source is a spec label already carried by extract.specs
    (Product Name / Material / Dimensions / Light Source / Voltage / Cord Length / Finishes /
    Application / Sizes Available ...) is a Specifications ROW, not a section: dropped, because
    spec_cover.py already enforces it from extract.specs.
 3. A comma-pair marketing headline over prose ("Refined Glow, Architectural Design") is the
    source description's own LEAD, not a section — sections.py auto-mapped some of these to a
    canonical name off a stray keyword ("Design", "Care Instructions"), the exact failure the
    2026-09-09 shape tests were added to catch. Dismissed to prose; the paragraph stays in facts.

Junk headings the keyfeat parser had left in key_features (a heading_source, "Why You'll Love It",
"Specifications") are removed in the same pass. Prints one line per product; --dry to inspect only.
"""
import json, glob, re, sys

WYLI = re.compile(r"why\s+you.?\s*ll\s+love\s+it", re.I)
JUNK_KF = re.compile(r"^(why\s+you.?\s*ll\s+love\s+it|specifications?|key\s+features|package\s+includes)\s*:?$", re.I)
LEAD = re.compile(r"^[^,]{3,40},\s*[^,]{3,40}$")          # two short clauses, no third comma


def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).strip()


def clean_bullet(s):
    s = re.sub(r"^\s*(?:[✔✅☆★●▶→️•\-–—\*]\s*)+", "", s or "")
    return s.strip()


def main():
    dry = "--dry" in sys.argv
    tot = {"wyli": 0, "kf_back": 0, "specrow": 0, "lead": 0, "kept": 0, "junk": 0}
    for f in sorted(glob.glob("extract/p*.json")):
        n = f[-7:-5]
        e = json.load(open(f))
        secs = e.get("sections") or []
        dismissed = e.get("sections_dismissed") or []
        kf = list(e.get("key_features") or [])
        spec_names = {norm(s.get("name")) for s in (e.get("specs") or []) if isinstance(s, dict)}
        keep, notes = [], []

        # sections.py sometimes files the Why-You'll-Love-It block under sections_dismissed
        # (it reads as the description's lead when the source has no other heading over prose).
        # It is still the key-features block, so pull it back out of the dismissal list first.
        still_dismissed = []
        for s in dismissed:
            hs = s.get("heading_source") or ""
            if WYLI.search(hs):
                added = 0
                for ln in [clean_bullet(x) for x in (s.get("lines") or []) if clean_bullet(x)]:
                    if not any(norm(ln) == norm(x) for x in kf):
                        kf.append(ln); added += 1
                tot["wyli"] += 1; tot["kf_back"] += added
                notes.append(f"WYLI(dismissed)->key_features({added})")
            else:
                still_dismissed.append(s)
        dismissed = still_dismissed

        for s in secs:
            hs = s.get("heading_source") or ""
            lines = [clean_bullet(x) for x in (s.get("lines") or []) if clean_bullet(x)]
            if WYLI.search(hs):
                added = 0
                for ln in lines:
                    if not any(norm(ln) == norm(x) for x in kf):
                        kf.append(ln); added += 1
                tot["wyli"] += 1; tot["kf_back"] += added
                notes.append(f"WYLI->key_features({added})")
                continue
            if norm(hs) in spec_names:
                dismissed.append({"heading_source": hs, "kind": s.get("kind"),
                                  "lines": s.get("lines"), "why": "specification row (extract.specs)"})
                tot["specrow"] += 1; notes.append(f"specrow:{hs}")
                continue
            if LEAD.match(hs.strip()) and (s.get("kind") == "prose"):
                dismissed.append({"heading_source": hs, "kind": s.get("kind"),
                                  "lines": s.get("lines"), "why": "description lead (marketing headline)"})
                tot["lead"] += 1; notes.append(f"lead:{hs}")
                continue
            keep.append(s); tot["kept"] += 1; notes.append(f"KEPT:{s.get('heading') or '?'}<-{hs}")

        before = len(kf)
        kf = [x for x in kf if not JUNK_KF.match(x.strip())
              and not any(norm(x) == norm(s.get("heading_source")) for s in secs + dismissed)]
        tot["junk"] += before - len(kf)

        e["sections"] = keep
        e["sections_dismissed"] = dismissed
        e["key_features"] = kf
        if not dry:
            json.dump(e, open(f, "w"), indent=1, ensure_ascii=False)
        print(f"{n} kf={len(kf)} sections={len(keep)} | " + ", ".join(notes))
    print("fix_sections: WYLI blocks {wyli} -> {kf_back} key_features lines restored, "
          "{specrow} spec-row pseudo-sections dropped, {lead} description leads dismissed, "
          "{junk} junk key_features headings removed, {kept} real sections kept".format(**tot))


if __name__ == "__main__":
    main()
