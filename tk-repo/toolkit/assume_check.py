#!/usr/bin/env python3
"""assume_check.py NN [NN ...] — "ADD NOTHING BEYOND THE SOURCE" gate (user decision 2026-09-06, zero model tokens).

The twin of value_check.py. value_check / spec_cover / fact_cover ask "is every source value still there?"; this asks
"is there a claim here the source never made?" — for the specific claim families DESC-SPEC.md forbids unless the extract
states them in plain words (the blr-batch12 list: "machine washable" from "washable", "no app required" from silence,
"printed user manual" from "user manual", "waterproof" from "water-resistant", "than ordinary …" from nothing).
Until now only the agent's reading of that list stood between these phrases and the store.

How it works: for each family, a regex is searched in the tag-stripped description (and seo.title / seo.description).
When it matches, the SOURCE text — extract/pNN.json facts + specs + package + how_to_use + faq_source + variant titles +
old title / old seo / productType / identity — is searched for the family's own source pattern. Source silent -> FAIL,
with the offending sentence printed. The product title is NOT scanned: title keywords are measured phrases whose product
fit is title-format-rule.md §6's job (title-check.py); a title keyword must appear in the description (rule 1), so if the
source is silent the FAIL still fires here on the description sentence, and the fit question goes back to the title.

Exemption: final/dNN.json may carry "add_per_ruling": ["<phrase>", ...] for a claim RULINGS.md explicitly allows
(e.g. a certification confirmed from the product images, ruled in the run log). Each is printed as [exempt].
This list is a floor, not a ceiling — add a family the moment a new invention of the same kind reaches a review.
Exit 1 on any FAIL.
"""
import json, re, sys, html

# (label, description regex, source regex) — the source regex is what the extract must contain for the claim to stand.
FAMILIES = [
    ('free / for free',            r"\b(?:for free|free of charge|comes free|free (?:shipping|returns?|replacement|gift|app|bonus|extra))\b", r"\bfree\b"),
    ('no app / app-free',          r"\b(?:no app\b|app[- ]free|without (?:an |any )?app\b|no (?:phone|smartphone) app)", r"\b(?:no app|app[- ]free|without (?:an |any )?app|no (?:phone|smartphone) app|app (?:not|isn't|is not) (?:required|needed))"),
    ('free app',                   r"\bfree app\b", r"\bfree\b"),
    ('the app',                    r"\b(?:the|a|our|dedicated|companion) app\b", r"\bapps?\b"),
    ('no tools / tool-free',       r"\b(?:no tools?\b|tool[- ]?(?:free|less)|without (?:any )?tools?\b)", r"\btools?\b"),
    ('no assembly',                r"\b(?:no assembly|assembly[- ]free|fully assembled|pre[- ]assembled|out of the box)\b", r"\bassembl"),
    ('BPA-free',                   r"\bbpa[- ]?free\b", r"\bbpa\b"),
    ('food-safe / food-grade',     r"\bfood[- ](?:safe|grade)\b", r"\bfood[- ](?:safe|grade)\b"),
    ('machine washable',           r"\bmachine[- ]?wash", r"\bmachine[- ]?wash"),
    ('dishwasher safe',            r"\bdishwasher", r"\bdishwasher"),
    ('hand wash',                  r"\bhand[- ]?wash", r"\bhand[- ]?wash"),
    ('power-cut memory',           r"\b(?:power (?:cut|outage|loss|failure)|after (?:a |an )?(?:blackout|unplugging)|remembers? (?:your |the )?(?:settings?|last))\b", r"\b(?:power (?:cut|outage|loss|failure|off)|blackout|unplug|remembers?|restor(?:es|ed) (?:the )?(?:last|previous))"),
    ('lifetime',                   r"\blifetime\b", r"\blifetime\b"),
    ('guarantee / warranty',       r"\b(?:guarantee[ds]?|warranty|warrantied)\b", r"\b(?:guarantee|warrant)"),
    ('certified / certification',  r"\b(?:certified|certification|ce[- ]marked|ul[- ]listed|fda[- ]approved|fda[- ]registered|rohs|reach[- ]compliant)\b", r"\b(?:certif|ce\b|ul\b|fda\b|rohs|reach\b)"),
    ('universal / fits any',       r"\b(?:universal(?:ly)?\b|fits? (?:any|all|every)\b|works? with (?:any|all|every)\b|compatible with (?:any|all|every)\b|one[- ]size[- ]fits[- ]all)", r"\b(?:universal|any\b|all\b|every\b|compatib)"),
    ('waterproof',                 r"\bwater[- ]?proof", r"\bwater[- ]?proof"),
    ('water-resistant',            r"\bwater[- ]?(?:resist|repel)", r"\bwater[- ]?(?:resist|repel|proof)"),
    ('sweat / dust / shock proof', r"\b(?:sweat|dust|shock|shatter|scratch|rust|wind)[- ]?(?:proof|resistant)\b", r"\b(?:sweat|dust|shock|shatter|scratch|rust|wind)[- ]?(?:proof|resist)"),
    ('unbreakable',                r"\b(?:unbreakable|indestructible)\b", r"\b(?:unbreakable|indestructible)\b"),
    ('fast / quick charging',      r"\b(?:fast|quick|rapid)[- ](?:charg|recharg)", r"\b(?:fast|quick|rapid)[- ]?(?:charg|recharg)"),
    ('silent / quiet',             r"\b(?:silent(?:ly)?|whisper[- ]quiet|noiseless|ultra[- ]quiet|quiet(?:ly)?)\b", r"\b(?:silent|quiet|noise|db\b|decibel)"),
    ('eco-friendly / non-toxic',   r"\b(?:eco[- ]?friendly|non[- ]?toxic|toxin[- ]free|chemical[- ]free|biodegradable|recycl(?:ed|able)|sustainabl)", r"\b(?:eco|non[- ]?toxic|toxin|chemical[- ]free|biodegrad|recycl|sustainab)"),
    ('natural / organic',          r"\b(?:all[- ]natural|100% natural|organic)\b", r"\b(?:natural|organic)\b"),
    ('odorless',                   r"\b(?:odou?rless|odou?r[- ]free|smell[- ]free|no (?:smell|odou?r))\b", r"\b(?:odou?r|smell)"),
    ('hypoallergenic / medical grade', r"\b(?:hypoallergenic|medical[- ]grade|surgical[- ]grade|clinically|dermatologist)\b", r"\b(?:hypoallergenic|medical[- ]grade|surgical|clinical|dermatolog)"),
    ('printed',                    r"\bprinted (?:manual|guide|instructions?|booklet)\b", r"\bprinted\b"),
    ('comparison than ordinary',   r"\bthan (?:ordinary|regular|traditional|standard|conventional|typical|other|most)\b", r"\bthan\b"),
    ('comparison stronger/faster', r"\b(?:stronger|faster|brighter|longer|quieter|lighter|safer|better|cheaper) than\b", r"\b(?:stronger|faster|brighter|longer|quieter|lighter|safer|better|cheaper) than\b"),
    ('X times more',               r"\b\d+\s?(?:x|times) (?:more|faster|stronger|brighter|longer)\b", r"\b\d+\s?(?:x|times)\b"),
]
def strip(h): return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', h or ''))).lower()
def sentences(t): return [s.strip() for s in re.split(r'(?<=[.!?])\s+|(?=\bq: )', t) if s.strip()]
fails = 0
for n in sys.argv[1:]:
    n = int(n); d = json.load(open(f'final/d{n:02d}.json')); ex = json.load(open(f'extract/p{n:02d}.json'))
    src = ' '.join(ex.get('facts', []) + [f"{s['name']} {s['value']}" for s in ex.get('specs', [])] + ex.get('package', [])
                   + ex.get('how_to_use', []) + [f"{q['q']} {q['a']}" for q in ex.get('faq_source', [])]
                   + [v['title'] for v in ex.get('variants', [])]
                   + [str(ex.get(k, '')) for k in ('old_title', 'old_seo_title', 'old_seo_description', 'productType', 'identity')]).lower()
    src = html.unescape(re.sub(r'<[^>]+>', ' ', src))
    allow = [a.lower() for a in d.get('add_per_ruling', [])]
    fields = [('description', strip(d['descriptionHtml'])), ('seo.title', (d.get('seo') or {}).get('title', '').lower()),
              ('seo.description', (d.get('seo') or {}).get('description', '').lower())]
    hits = 0
    for label, pat, srcpat in FAMILIES:
        if re.search(srcpat, src): continue                       # the source says it -> the claim may stand
        for fname, text in fields:
            for s in sentences(text):
                m = re.search(pat, s)
                if not m: continue
                if any(a in s for a in allow): print(f"[exempt] {n:02d} {label} in {fname}: \"{s[:90]}\""); continue
                fails += 1; hits += 1
                print(f"[FAIL] {n:02d} {label} — source never says it — {fname}: \"…{s[:140]}\" (matched: {m.group(0)!r})")
    print(f"{n:02d} assume-check: {len(FAMILIES)} claim families scanned, {hits} unsupported")
print(f"assume-check: {fails} FAIL")
sys.exit(1 if fails else 0)
