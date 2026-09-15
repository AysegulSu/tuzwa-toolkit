#!/usr/bin/env python3
"""para_feat.py [NN ...] [--report kf-report.md] — what the source PARAGRAPHS say that extract.key_features / extract.specs
do not carry. Review aid for the main context, zero model tokens; always exits 0 (a flagged line is a question, not a verdict).

Added 2026-09-07 (STR-DUB-2-batch1, user decision). EXTRACT-SPEC.md has asked the extraction agent since 2026-09-06 to
COMPLETE key_features with the concrete features the source states only inside paragraphs, and to append every measurable
prose value to specs — but nothing made an omission visible: in that batch 45 of 48 products left the extraction step with
exactly the script's pre-filled list (0 additions), and nobody could tell whether the agent had looked. This script reads the
paragraphs itself and prints, per product:

  [KF MISSING?]   a paragraph sentence that carries a feature marker (mechanism / material / mode / control / mounting /
                  capacity / "no more X" / "without X" …) and whose content words are not covered by any key_features line
  [SPEC MISSING?] a number+unit, material, ingress rating, compatibility or count figure found in a paragraph sentence and
                  absent (same figure) from extract.specs

The main context sorts every line: (a) real feature/value → add it to extract/pNN.json (key_features / specs) so
keyfeat_cover / spec_cover then ENFORCE it in the description; (b) marketing sentence, restatement of a listed line, or
a figure that is a package/variant fact → dismiss. The run log carries `para_feat: N KF flagged, K added, N-K dismissed |
M spec flagged, J added, M-J dismissed` — a log without this line means the step was skipped.
`--report FILE` writes a per-product table (source list count / paragraph additions / final list count) for the operator.
`--gate` (added 2026-09-07, user decision — "measurable values are mandatory, sentences are advice"): every [SPEC MISSING?]
figure becomes a FAIL and the exit code is 1 while any remains — a number+unit, count or IP rating the paragraphs state must be
in extract.specs, or listed as an explicit omission (final/dNN.json omit_per_ruling, or — at extraction time, before any final
exists — rulings_omit.json `{"NN": ["21 grams", …]}` written by the main context beside RULINGS.md), before the title step starts. [KF MISSING?] sentences stay
a report in both modes (marketing sentences are caught too; the main context decides). README step 3b runs `--gate`.
"""
import json, re, sys, os, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from keyfeat_cover import present, toks, clean, SECTION_END, STOP

FEATURE = re.compile(r"\b(adjust\w*|foldab\w*|collaps\w*|detach\w*|removab\w*|rechargeab\w*|wireless|bluetooth|magnet\w*|"
                     r"waterproof|water[- ]resistant|breathab\w*|insulat\w*|non[- ]slip|anti[- ]\w+|built[- ]in|integrated|"
                     r"automatic\w*|timer|remote|touch|sensor|mode[s]?|setting[s]?|level[s]?|speed[s]?|program[s]?|"
                     r"stainless|steel|silicone|bamboo|leather|wood\w*|acrylic|aluminum|aluminium|abs|tpu|polycarbonate|"
                     r"cotton|polyester|nylon|mesh|glass|ceramic|plastic|memory foam|foam|fabric|"
                     r"dishwasher|machine wash\w*|hand wash\w*|wipe|usb|type[- ]c|led|lcd|display|screen|battery|charg\w*|"
                     r"capacity|holds?|fits?|compatib\w*|mount\w*|clip|hook|strap|handle|pocket|compartment\w*|"
                     r"no more \w+|without (?:the )?\w+|no need|hands[- ]free|one[- ]touch|one[- ]click|self[- ]\w+)\b", re.I)
MARKETING = re.compile(r"^(discover|introducing|experience|transform|elevate|say goodbye|say hello|upgrade|imagine|enjoy|"
                       r"treat yourself|whether you|perfect for|ideal for|great for|the (?:perfect|ultimate))\b", re.I)
UNIT = (r"(?:mm|cm|m|in|inch|inches|\"|ft|feet|oz|fl oz|lb|lbs|kg|g|grams?|ml|l|liters?|litres?|mah|w|watts?|v|volts?|hz|db|lumens?|lm|"
        r"hours?|hrs?|h|minutes?|mins?|seconds?|sec|days?|°c|°f|degrees?|%|tb|gb|mb/s|rpm|psi|k)")
VALUE = re.compile(r"\b(\d+(?:[.,]\d+)?(?:\s*(?:-|to|x|×)\s*\d+(?:[.,]\d+)?)*)\s*(" + UNIT + r")\b", re.I)
VALUE2 = re.compile(r"\b(ipx?\d+|ip\d{2}|\d+\s*(?:-|to)?\s*\d*\s*(?:modes?|levels?|speeds?|programs?|settings?|colou?rs?|sizes?|pieces?|pcs|blades?|heads?|nutrients?))\b", re.I)

def paragraphs(raw_html):
    """sentences of the source's own paragraphs, outside lists and outside the spec/package/FAQ/how-to sections"""
    h = raw_html or ""
    cut = len(h)
    for m in re.finditer(r"<(?:h\d|strong|b|p)[^>]*>\s*([^<]{3,60})", h, re.I):
        if SECTION_END.search(m.group(1)) and len(clean(m.group(1))) < 60: cut = m.start(); break
    body = re.sub(r"<ul[^>]*>.*?</ul>|<ol[^>]*>.*?</ol>|<table.*?</table>", " ", h[:cut], flags=re.S | re.I)
    body = re.sub(r"<h\d[^>]*>.*?</h\d>", " ", body, flags=re.S | re.I)
    out = []
    for p in re.findall(r"<p[^>]*>(.*?)</p>|<div[^>]*>([^<]{20,})</div>", body, re.S | re.I):
        t = clean(p[0] or p[1])
        for s in re.split(r"(?<=[.!?])\s+", t):
            s = s.strip()
            if len(s.split()) >= 5: out.append(s)
    return out

def spec_figures(specs):
    f = set()
    for sp in specs:
        for m in VALUE.finditer(f"{sp.get('name','')} {sp.get('value','')}"): f.add(re.sub(r"\s", "", m.group(0).lower()))
        for m in VALUE2.finditer(f"{sp.get('name','')} {sp.get('value','')}"): f.add(re.sub(r"\s", "", m.group(0).lower()))
    return f

if __name__ == "__main__":
    args = sys.argv[1:]; report = None
    if "--report" in args: i = args.index("--report"); report = args[i+1]; args = args[:i] + args[i+2:]
    gate = "--gate" in args; args = [a for a in args if a != "--gate"]
    ids = [int(x) for x in args] or sorted(int(f[1:3]) for f in os.listdir("extract") if f.endswith(".json"))
    kf_tot = sp_tot = 0; rows = []
    for n in ids:
        e = json.load(open(f"extract/p{n:02d}.json")); r = json.load(open(f"raw/p{n:02d}.json"))
        kfs = e.get("key_features") or []; specs = e.get("specs") or []; figs = spec_figures(specs)
        covered = kfs + [f"{s.get('name','')}: {s.get('value','')}" for s in specs] + list(e.get("package") or [])
        kf_flags, sp_flags = [], []
        for s in paragraphs(r.get("descriptionHtml")):
            if MARKETING.match(s) and not FEATURE.search(s): continue
            if FEATURE.search(s) and not present(s, covered): kf_flags.append(s)
            for m in list(VALUE.finditer(s)) + list(VALUE2.finditer(s)):
                fig = re.sub(r"\s", "", m.group(0).lower())
                if fig not in figs and not any(fig in x or x in fig for x in figs): sp_flags.append((m.group(0), s))
        seen = set(); sp_flags = [x for x in sp_flags if not (x[0].lower() in seen or seen.add(x[0].lower()))]
        kf_tot += len(kf_flags); sp_tot += len(sp_flags)
        print(f"== {n:02d}  key_features {len(kfs)} | specs {len(specs)} | paragraph flags: KF {len(kf_flags)}, SPEC {len(sp_flags)}")
        for s in kf_flags: print(f"  [KF MISSING?]   {s[:150]}")
        omit = []
        if os.path.exists(f"final/d{n:02d}.json"): omit = [o.lower() for o in json.load(open(f"final/d{n:02d}.json")).get("omit_per_ruling", [])]
        ro = json.load(open("rulings_omit.json")) if os.path.exists("rulings_omit.json") else {}   # {"NN": ["21 grams", ...]} written by the main context with RULINGS.md
        omit += [o.lower() for o in ro.get(f"{n:02d}", [])]
        for fig, s in sp_flags:
            ruled = any(fig.lower() in o or o in fig.lower() for o in omit)   # 2026-09-07: only explicit omissions count, never a text search in RULINGS.md
            tag = "[SPEC ruled]" if ruled else ("[FAIL] SPEC MISSING" if gate else "[SPEC MISSING?]")
            print(f"  {tag} {fig}  ← {s[:120]}")
            if gate and not ruled: gate_fails = globals().get("gate_fails", 0) + 1; globals()["gate_fails"] = gate_fails
        rows.append((n, len(kfs), len(kf_flags), len(specs), len(sp_flags)))
    print(f"para_feat: {kf_tot} KF flagged, {sp_tot} SPEC flagged across {len(ids)} products — main context sorts each into added / dismissed and writes the counts to the run log")
    gf = globals().get("gate_fails", 0)
    if gate: print(f"para_feat --gate: {gf} unruled prose spec figure(s) missing from extract.specs" + (" — add them to extract/pNN.json specs (or rule them out) before the title step" if gf else ""))
    if report:
        with open(report, "w") as f:
            f.write("| # | extract.key_features | paragraph KF flags | extract.specs | paragraph SPEC flags |\n|---|---|---|---|---|\n")
            for n, a, b, c, d in rows: f.write(f"| {n:02d} | {a} | {b} | {c} | {d} |\n")
        print(f"report -> {report}")
    if gate and gf: sys.exit(1)
