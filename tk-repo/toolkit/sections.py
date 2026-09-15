#!/usr/bin/env python3
"""sections.py --extract [NN ...]  |  sections.py NN [NN ...]  — every OTHER fact-carrying section of the source becomes its
own <h3> section on our page (added 2026-09-08, user decision; applies from the first batch run after this date — no pushed
product is re-processed).

Until now the extraction kept only the known blocks as fields (specs, package, how_to_use, usage_tips, key_features,
faq_source); every other headed block of the supplier's description — Care Instructions, Warnings, Materials, Design,
Applications, Compatibility, Storage, Charging, Installation, Size Guide, Notes … — fell into `facts` as loose lines, the
heading was lost, and the writer dissolved the content into the prose. Rule now (description-format-rule.md §7c):

  Tip A — a source section that carries at least one PRODUCT FACT (a figure, a unit, a value word of the extract, a material,
          a care / warning / installation instruction, a compatibility statement) is reproduced as `<h3>{Heading}</h3>` +
          `<ul>` (list source) or `<p>` (prose source): every source line = one item / paragraph, in the writer's own
          sentence, values verbatim, never pasted ([COPY]), never merged ([MERGED]); RULINGS apply via omit_per_ruling
          (a supplier-policy line, a medical outcome, a "colour may differ" disclaimer …). A fact already carried by the
          prose or the Key Features list is STILL written here — same fact, different sentence (same rule as §4).
  Tip B — a section with no product fact at all (a marketing heading + adjective sentences, "Elegance That Takes Off")
          is NOT a section: it dissolves into the prose as before. The script lists it in `sections_dismissed` so the run
          log shows what was set aside. Since 2026-09-09 two SHAPE tests dismiss the same way, before the fact test:
          a heading longer than MAX_HEAD_WORDS is a marketing headline, not a section heading; and the source's FIRST
          heading over prose is the description's own lead (see the note at MAX_HEAD_WORDS).
  Heading — NORMALISED VOCABULARY (user decision): the page never carries the supplier's own heading; the script maps it
          to one canonical name (CANON below). An unmapped heading is written with `"heading": null` + the source text in
          `heading_source` and printed [UNMAPPED]; the extraction agent (or the main context) picks the closest canonical
          name — or, when none fits, a 1–3-word title-case name of its own — and the check requires the page heading to
          equal `extract.sections[i].heading` exactly. A new family that recurs is added to CANON here (floor, not ceiling).
  Position — after Package Includes, after How to Use and Usage Tips when present, in source order, before the fit block
          / <h3>FAQs</h3>. Their words count toward the total like Usage Tips do (the 500 ceiling is a WARN and never
          removes a source line). unit_dual.py converts inside them.

--extract: reads raw/pNN.json; every heading (h2–h4, or a bold-only line / bold lead of a <p>) whose text is NOT a known
block (spec / package / FAQ / how-to-use / usage-tips / key-features / a generic "Description" / "Overview" heading) opens a
section that runs to the next heading; its <li> lines (kind "list") or <p> paragraphs (kind "prose") are the lines. Writes
`extract.sections` (never overwrites a non-empty list — the agent may complete it by eye) and `extract.sections_dismissed`;
then REMOVES every section line from `extract.key_features` (the section is now its home, so keyfeat_cover.py does not
demand it twice). Run it AFTER `keyfeat_cover.py --extract` and `usage_tips.py --extract`.

Check mode (inside gate.py): (1) a `<h3>` on the page that is neither a skeleton heading nor an extract section heading is
a FAIL (no invented sections); (2) every extract section not fully ruled out has its `<h3>` exactly once; (3) every line
present (half its content words in one item / paragraph) unless in omit_per_ruling; (4) no [COPY]; (5) no [MERGED] (list
kind); (6) position after Package Includes / How to Use / Usage Tips and before the fit block / FAQs; (7) source order
(WARN only). Exit 1 on any FAIL.
"""
import json, re, sys, os, html
from keyfeat_cover import toks, clean, is_copy, value_words, match_item, present, SECTION_END

# ---- what is NOT a section (already a field, or generic) ----------------------------------------------------------------
KNOWN = re.compile(r"^\s*(?:"
                   r"(?:key |main |product |core )?features?(?: & benefits)?|highlights?|"
                   r"specifications?|specs?|technical (?:details?|data|specifications?)|product (?:details?|information|parameters?)|parameters?|attributes?|"
                   r"package(?: includes?| contents?| list)?:?|what'?s (?:in the box|included)|in the box|box contents?|"
                   r"faqs?|frequently asked questions?|q&a|"
                   r"how to use|instructions?(?: for use)?|directions?(?: for use)?|operation|user guide|"
                   r"usage tips?|usage recommendations?|usage suggestions?|tips?(?: for use| & tricks)?|pro tips?|recommended uses?|"
                   r"(?:product )?descriptions?|overview|about(?: this item| this product| the product)?|introduction|summary"
                   r")\s*:?\s*$", re.I)

# ---- canonical headings (normalised vocabulary, user decision 2026-09-08) — floor, not ceiling ------------------------------
CANON = [
    ("Care Instructions", r"\b(care|caring|clean|cleaning|wash|washing|maintenance|maintain|upkeep)\b"),
    ("Safety Warnings",   r"\b(warning|warnings|caution|cautions|safety|precaution|precautions|attention|important|danger|hazard)\b"),
    ("Materials",         r"\b(material|materials|fabric|fabrics|construction|composition|made of|what it'?s made)\b"),
    ("Design",            r"\b(design|designs|structure|appearance|style|aesthetic|look)\b"),
    ("Applications",      r"\b(application|applications|uses?|use cases?|scenarios?|occasions?|where to use|suitable for|ideal for|perfect for|great for|who (?:is it|it'?s) for)\b"),
    ("Compatibility",     r"\b(compatib\w*|fits|works with|suitable (?:models|devices)|supported)\b"),
    ("Storage",           r"\b(storage|store|storing)\b"),
    ("Charging",          r"\b(charg\w*|battery|batteries|power supply|power)\b"),
    ("Installation",      r"\b(install\w*|assembl\w*|set ?up|mounting|mount|fitting)\b"),
    ("Size Guide",        r"\b(size|sizes|sizing|size chart|size guide|fit guide|measurements?|dimensions?)\b"),
    ("Notes",             r"\b(notes?|kind reminder|kindly note|please note|reminder|disclaimer)\b"),
]
def canon(heading):
    t = clean(heading).rstrip(":")
    for name, pat in CANON:
        if re.search(pat, t, re.I): return name
    return None

# ---- Tip A / Tip B: does the block carry a product fact? -------------------------------------------------------------------
FACT = re.compile(r"\b(?:do not|don'?t|never|avoid|keep|store|wash|clean|wipe|rinse|dry|iron|bleach|tumble|hand[- ]wash|machine[- ]wash|"
                  r"charge|charging|plug|unplug|insert|remove|install|mount|attach|tighten|loosen|place|use only|only use|"
                  r"away from|out of reach|supervis\w*|adult|children|kids|pets?|"
                  r"cotton|polyester|nylon|wool|silk|linen|leather|steel|stainless|aluminum|aluminium|iron|copper|brass|plastic|abs|pvc|silicone|rubber|"
                  r"wood|wooden|bamboo|glass|ceramic|foam|fleece|velvet|canvas|mesh|acrylic|"
                  r"compatible|fits?|works with|suitable for|ideal for|perfect for|great for|"
                  r"waterproof|water[- ]resistant|dishwasher|microwave|oven|freezer|indoor|outdoor|"
                  r"before|after|first|then|until|while)\b", re.I)
UNIT = re.compile(r"\d\s*(?:mm|cm|m|in|inch|inches|ft|feet|\"|oz|lb|lbs|kg|g|ml|l|mah|w|v|hz|db|°|%|hours?|hrs?|minutes?|min|days?|weeks?|months?|years?|pcs?|pack|x)\b", re.I)
def has_fact(line, vals):
    return bool(re.search(r"\d", line) or UNIT.search(line) or FACT.search(line) or any(w in vals for w in re.findall(r"[a-z]{4,}", line.lower())))

# ---- source parsing ------------------------------------------------------------------------------------------------------
HEAD_RE = re.compile(r"<(h[2-4])[^>]*>(.*?)</\1>|<p[^>]*>\s*<(?:strong|b)[^>]*>([^<]{3,60}?):?\s*</(?:strong|b)>\s*(?::\s*)?</p>|<(?:strong|b)[^>]*>([^<]{3,60}?):?\s*</(?:strong|b)>\s*(?:<br\s*/?>|:)", re.S | re.I)
POLICY = re.compile(r"\b(shipping|delivery|warranty|guarantee|returns?|refunds?|payment|about us|contact(?: us)?|feedback|why (?:choose|buy from) us|our (?:promise|service)|customer service|after[- ]sales)\b", re.I)
HOWTO_OR_TIPS = re.compile(r"^\s*(usage tips?|usage recommendations?|usage suggestions?|tips?(?: for use| & tricks)?|pro tips?|recommended uses?|how to use|instructions?)\s*:?\s*$", re.I)

# ---- what a section HEADING may look like (added 2026-09-09, user decision after STR-DUB-2-batch8) --------------------------
# First live run of this script: it proposed a section on 42 of 50 products and every one was the supplier's LEAD HEADLINE +
# intro paragraph — the description's own opening, not an additional block. Seven had already been auto-mapped to a canonical
# name by an accidental keyword inside that marketing sentence ("Charging" from "High Power Blue Laser Pointer for
# Long-Distance Targeting", "Safety Warnings" from "Reflective Cat GPS Tracker Collar for Enhanced Safety"), so a run whose
# operator did not read the --extract summary would have published <h3>Safety Warnings</h3> over a marketing sentence.
# gate.py cannot catch that: once a block is in extract.sections it only asks whether the page reproduces it.
# Two shape tests, either of which would have dismissed all 42 by script:
#   MAX_HEAD_WORDS — a real section heading is a short noun phrase ("Care Instructions", "Safety", "Size Guide"). All 42
#     mis-detected headings were 5-8 words; every heading the fixtures keep is 1-3.
#   lead position   — the source's FIRST heading, when its block is prose, opens the description. A genuine section that is
#     also the first heading survives via the exception below (short heading that maps to a canonical family).
MAX_HEAD_WORDS = 4

def source_sections(raw_html, vals):
    h = raw_html or ""
    heads = []
    for m in HEAD_RE.finditer(h):
        text = clean(m.group(2) or m.group(3) or m.group(4) or "")
        if not text or len(text) > 60 or len(text.split()) > 8: continue
        if re.search(r"[.!?]\s*\S", text): continue     # a sentence, not a heading
        heads.append((m.start(), m.end(), text))
    out, dismissed = [], []
    for i, (s, e, text) in enumerate(heads):
        nxt = heads[i + 1][0] if i + 1 < len(heads) else len(h)
        if KNOWN.match(text) or HOWTO_OR_TIPS.match(text): continue
        block = h[e:nxt]
        if POLICY.search(text):   # a seller-policy block is never copy (user rule 2026-09-07) — logged, never a section
            lines = [clean(x) for x in re.findall(r"<li[^>]*>(.*?)</li>|<p[^>]*>(.*?)</p>", block, re.S | re.I) for x in [x[0] or x[1]] if clean(x)]
            dismissed.append({"heading_source": text, "reason": "supplier policy, not product fact — never in copy", "lines": lines[:15]}); continue
        items = [clean(x) for x in re.findall(r"<li[^>]*>(.*?)</li>", block, re.S | re.I)]
        kind = "list"
        if not items:
            items = [clean(x) for x in re.findall(r"<p[^>]*>(.*?)</p>", block, re.S | re.I)]; kind = "prose"
        if not items:
            items = [t.strip() for t in re.split(r"<br\s*/?>|(?<=[.!?])\s+", clean(block)) if len(t.split()) >= 3]; kind = "prose"
        items = [x for x in items if x and len(x.split()) >= 2 and not re.match(r"^\s*<img", x)]
        if not items: continue
        if kind == "prose" and sum(len(x.split()) for x in items) > 220:
            continue   # a long narrative under a heading is the description body, not a section — prose carries it
        nw = len(text.split())
        # the source's first heading over prose is the description's own lead — unless it is a short heading that names a
        # canonical family (a source that genuinely opens with "Care Instructions" is kept)
        if i == 0 and kind == "prose" and not (nw <= MAX_HEAD_WORDS and canon(text)):
            dismissed.append({"heading_source": text,
                              "reason": "description lead headline + intro paragraph — the prose's own opening, not an additional section",
                              "lines": items}); continue
        if nw > MAX_HEAD_WORDS:
            dismissed.append({"heading_source": text,
                              "reason": f"heading is a {nw}-word marketing headline, not a section heading (limit {MAX_HEAD_WORDS} words)",
                              "lines": items}); continue
        if not any(has_fact(x, vals) for x in items):
            dismissed.append({"heading_source": text, "reason": "marketing-only, no product fact — prose", "lines": items}); continue
        out.append({"heading": canon(text), "heading_source": text, "kind": kind, "lines": items[:15]})
    return out, dismissed

# ---- page parsing --------------------------------------------------------------------------------------------------------
SKELETON = {"key features", "specifications", "package includes:", "package includes", "how to use", "usage tips", "faqs"}
def page_sections(h):
    """[(heading, start, [items])] for every <h3> on the page; items = li texts, or p texts when the section has no ul"""
    out = []
    for m in re.finditer(r"<h3[^>]*>(.*?)</h3>", h or "", re.S | re.I):
        nxt = [x for x in (h.find("<h3", m.end()), h.find('<div class="vp-', m.end())) if x > 0]
        block = h[m.end():min(nxt) if nxt else len(h)]
        items = [clean(x) for x in re.findall(r"<li[^>]*>(.*?)</li>", block, re.S | re.I)]
        if not items: items = [clean(x) for x in re.findall(r"<p[^>]*>(.*?)</p>", block, re.S | re.I)]
        out.append((clean(m.group(1)), m.start(), [x for x in items if x]))
    return out

if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "--extract":
        ids = [int(x) for x in args[1:]] or sorted(int(f[1:3]) for f in os.listdir("extract") if f.endswith(".json"))
        n_with = n_dis = n_unm = kf_moved = 0
        by_reason = {"marketing": 0, "policy": 0, "lead": 0, "headline": 0}
        for n in ids:
            p = f"extract/p{n:02d}.json"; e = json.load(open(p)); r = json.load(open(f"raw/p{n:02d}.json"))
            if e.get("sections"):
                n_with += 1; print(f"{n:02d} sections: kept the existing {len(e['sections'])} (agent-completed)"); continue
            secs, dis = source_sections(r.get("descriptionHtml"), value_words(e))
            e["sections"] = secs; e["sections_dismissed"] = dis
            # the section is now the home of its lines: take them out of key_features so keyfeat_cover does not demand them twice
            lines = [l for s in secs for l in s["lines"]]
            kf = e.get("key_features") or []
            keep = [k for k in kf if not any(present(k, [l]) and present(l, [k]) for l in lines)]
            kf_moved += len(kf) - len(keep); e["key_features"] = keep
            json.dump(e, open(p, "w"), ensure_ascii=False, indent=1)
            n_with += bool(secs); n_dis += len(dis)
            for d in dis:
                r_ = d["reason"]
                k_ = ("policy" if "supplier policy" in r_ else "lead" if "lead headline" in r_
                      else "headline" if "marketing headline" in r_ else "marketing")
                by_reason[k_] += 1
            for s in secs:
                if s["heading"] is None: n_unm += 1; print(f"  {n:02d} [UNMAPPED] source heading {s['heading_source']!r} — set extract.sections[].heading by eye (canonical name preferred)")
            print(f"{n:02d} sections: {len(secs)} kept ({', '.join((s['heading'] or '?') + '/' + s['kind'] + '/' + str(len(s['lines'])) for s in secs) or '-'})"
                  + (f", {len(dis)} dismissed ({', '.join(d['heading_source'] for d in dis)})" if dis else ""))
        print(f"sections --extract: {n_with} of {len(ids)} products carry a fact section, {n_dis} block(s) dismissed to prose"
              f" (marketing {by_reason['marketing']} / policy {by_reason['policy']} / description lead {by_reason['lead']}"
              f" / long marketing heading {by_reason['headline']}), {n_unm} UNMAPPED heading(s),"
              f" {kf_moved} key_features line(s) moved into sections")
        sys.exit(0)
    fails = 0
    for n in args:
        n = int(n); e = json.load(open(f"extract/p{n:02d}.json")); d = json.load(open(f"final/d{n:02d}.json")); h = d["descriptionHtml"]
        secs = e.get("sections") or []; omit = [o.lower() for o in d.get("omit_per_ruling", [])]
        vals = value_words(e); bad = []; warn = []
        page = page_sections(h)
        allowed = SKELETON | {(s["heading"] or "").lower() for s in secs}
        for hd, pos, items in page:
            if hd.lower() not in allowed: bad.append(f"<h3>{hd}</h3> is neither a skeleton heading nor a source section — no invented sections")
        pk = h.find("<h3>Package Includes:</h3>"); fq = h.find("<h3>FAQs</h3>"); fit = h.find('<div class="vp-fit"')
        ht = h.find("<h3>How to Use</h3>"); ut = h.find("<h3>Usage Tips</h3>")
        last = -1
        for s in secs:
            hd = s.get("heading")
            req = [l for l in s["lines"] if not any(o and o in l.lower() for o in omit)]
            if not hd: bad.append(f"extract section {s.get('heading_source')!r} has no heading — set extract.sections[].heading"); continue
            found = [(p_, it) for h_, p_, it in page if h_.lower() == hd.lower()]
            if not req:
                if found: bad.append(f"<h3>{hd}</h3> present but every source line is ruled out — remove the section")
                for l in s["lines"]: print(f"  {n:02d} sections [exempt] {hd}: {l[:70]}")
                continue
            if len(found) != 1: bad.append(f"<h3>{hd}</h3> count {len(found)} (source has {len(req)} line(s) under it — need exactly one section)"); continue
            pos, items = found[0]
            if not items: bad.append(f"<h3>{hd}</h3> has no items / paragraphs"); continue
            seen = {}
            for l in req:
                if not present(l, items): bad.append(f"{hd}: line missing: {l[:80]}")
                else:
                    if is_copy(l, items, vals): bad.append(f"{hd}: [COPY] source line pasted — same facts, your own sentence: {l[:80]}")
                    mi = match_item(l, items)
                    if mi is not None: seen.setdefault(mi, []).append(l)
            if s.get("kind") == "list":
                for k, v in seen.items():
                    if len(v) > 1: bad.append(f"{hd}: [MERGED] one item carries {len(v)} source lines — one line = one item: {items[k][:60]!r}")
            for l in s["lines"]:
                if any(o and o in l.lower() for o in omit): print(f"  {n:02d} sections [exempt] {hd}: {l[:70]}")
            if pk != -1 and pos < pk: bad.append(f"<h3>{hd}</h3> must come after Package Includes")
            if ht != -1 and pos < ht: bad.append(f"<h3>{hd}</h3> must come after How to Use")
            if ut != -1 and pos < ut: bad.append(f"<h3>{hd}</h3> must come after Usage Tips")
            if (fit != -1 and pos > fit) or (fq != -1 and pos > fq): bad.append(f"<h3>{hd}</h3> must come before the fit block / FAQs")
            if pos < last: warn.append(f"<h3>{hd}</h3> is out of source order")
            last = max(last, pos)
        for w in warn: print(f"[WARN] {n:02d} sections: {w}")
        if bad:
            fails += 1
            for b in bad: print(f"[FAIL] {n:02d} sections: {b}")
        else:
            print(f"{n:02d} sections: " + (f"{len(secs)} section(s) ({', '.join(s.get('heading') or '?' for s in secs)}), every line present, 0 copies" if secs else "no source section, none on the page"))
    print(f"sections: {fails} FAIL across {len(args)} products")
    sys.exit(1 if fails else 0)
