#!/usr/bin/env python3
"""claims_check.py NN [NN ...] — source-citation gate (added 2026-09-04, user decision after blr-batch12).

Every sentence and every <li> of final/dNN.json descriptionHtml must be covered by an entry in the doc's
`claims` list, and every entry must point at a real source line whose content actually supports it.

claims entry: {"text": "<exact tag-stripped sentence or <li> text as it appears in the description>",
               "src": "facts[12]" | "specs[3]" | "package[0]" | "how_to_use[1]" | "faq_source[2]" | "variants"
                      | "title" | "ruling:NN" | "safety" | "marketing"}
  facts/specs/package/how_to_use/faq_source/variants -> extract/pNN.json lines (0-based index)
  title      -> the sentence only carries title/second-net keywords, no product fact
  ruling:NN  -> a value set by RULINGS.md for that product (e.g. 22 inches, 26 per-size inches)
  safety     -> Backend Safety Notes disclaimer (supervision, not a medical device, blade/heat caution)
  marketing  -> a sentence with NO factual content (no number, no material, no capability, no feature)

Checks (each failure is a FAIL line; exit 1 on any FAIL):
  1. coverage   — every sentence / <li> in the description is contained in some claim text (headings, img, FAQ questions exempt)
  2. existence  — src index exists in the extract
  3. grounding  — for facts/specs/package/how_to_use/faq_source (several lines may be cited: facts[4]+facts[9]): every number
                  in the claim appears in the cited line(s), every ASSUMPTION-family word in the claim appears there too,
                  and ≥35% of the claim's content-word stems appear there (paraphrase is fine, invention is not)
  4. marketing  — a 'marketing' claim must contain no digit and none of the ASSUMPTION words
  5. safety     — a 'safety' claim must contain a disclaimer word (supervis|unattended|not a medical|caution|sharp|hot|consult)
"""
import json, re, sys, html
ASSUMPTION = r"\b(free|machine|hand wash|hand-wash|app|apps|printed|power cut|bpa|tools?|toolless|corners?|lifetime|guarantee|warranty|certified|fda|ce\b|rohs|universal|compatible|waterproof|wireless|rechargeable|cordless|heated|adjustable|premium|professional|medical|organic|eco|natural|safe|non-?toxic|odorless|silent|quiet|fast|instant)\b"
DISCLAIM = r"supervis|unattended|not a medical|caution|sharp|hot surface|keep .*away|out of reach|consult"
STOP = {"with", "that", "this", "your", "from", "into", "than", "then", "them", "they", "have", "will", "when", "while",
        "also", "each", "every", "over", "onto", "just", "more", "most", "about", "after", "before", "their", "there",
        "these", "those", "which", "what", "where", "even", "both", "make", "makes", "made", "keep", "keeps", "gets",
        "give", "gives", "take", "takes", "come", "comes", "need", "needs", "like", "same", "much", "very", "only"}
def strip(h): return html.unescape(re.sub(r'<[^>]+>', ' ', h))
def norm(s): return re.sub(r'\s+', ' ', strip(s)).strip().lower()
def nums(s): return re.findall(r'\d+(?:\.\d+)?', s)
def cwords(s): return [w for w in re.findall(r'[a-z]{4,}', s.lower()) if w not in STOP]
def units(h):
    """sentences and li texts of the description that must be covered"""
    out = []
    body = re.sub(r'<h[23][^>]*>.*?</h[23]>', ' ', h, flags=re.S)
    body = re.sub(r'<img[^>]+>', ' ', body)
    for li in re.findall(r'<li[^>]*>(.*?)</li>', body, re.S): out.append(norm(li))
    body = re.sub(r'<ul[^>]*>.*?</ul>', ' ', body, flags=re.S)
    for p in re.findall(r'<p[^>]*>(.*?)</p>', body, re.S):
        if '<strong>Q:' in p:
            a = p.split('<br>', 1)[1] if '<br>' in p else ''
            p = re.sub(r'^\s*A:\s*', '', strip(a))
        for s in re.split(r'(?<=[.!?])\s+', norm(p)):
            if len(s) > 3: out.append(s)
    return [u for u in out if u]
def src_line(ex, src):
    """src may cite several lines joined with '+': facts[4]+facts[9]"""
    parts = []
    for one in src.split('+'):
        m = re.match(r'(facts|specs|package|how_to_use|faq_source)\[(\d+)\]$', one.strip())
        if not m: return None
        k, i = m.group(1), int(m.group(2))
        arr = ex.get(k, [])
        if i >= len(arr): return None
        v = arr[i]
        parts.append(f"{v['name']}: {v['value']}" if k == 'specs' else f"{v['q']} {v['a']}" if k == 'faq_source' else v)
    return ' '.join(parts)
def stem(w): return w[:5] if len(w) > 5 else w
fails = 0
for n in sys.argv[1:]:
    n = int(n); d = json.load(open(f'final/d{n:02d}.json')); ex = json.load(open(f'extract/p{n:02d}.json'))
    claims = d.get('claims')
    if not claims: print(f"[FAIL] {n:02d} no `claims` list in final/d{n:02d}.json"); fails += 1; continue
    ctexts = [norm(c['text']) for c in claims]
    # 1. coverage
    for u in units(d['descriptionHtml']):
        if not any(u in c or c in u and len(c) > 20 for c in ctexts):
            print(f"[FAIL] {n:02d} uncited text: \"{u[:90]}\""); fails += 1
    for c in claims:
        t = norm(c['text']); s = c['src']
        if s in ('title', 'safety', 'marketing', 'variants') or s.startswith('ruling:'):
            if s == 'marketing' and (nums(t) or re.search(ASSUMPTION, t)):
                print(f"[FAIL] {n:02d} marketing claim carries a fact/assumption word: \"{t[:80]}\""); fails += 1
            if s == 'safety' and not re.search(DISCLAIM, t):
                print(f"[FAIL] {n:02d} safety claim without disclaimer wording: \"{t[:80]}\""); fails += 1
            if s == 'variants':
                vt = ' '.join(v['title'] for v in ex['variants']).lower()
                if not any(w in vt for w in cwords(t)) and not any(x in vt for x in nums(t)):
                    print(f"[FAIL] {n:02d} variants claim not supported by variant titles: \"{t[:80]}\""); fails += 1
            continue
        line = src_line(ex, s)
        if line is None: print(f"[FAIL] {n:02d} src {s} does not exist"); fails += 1; continue
        L = line.lower(); Ls = {stem(w) for w in re.findall(r'[a-z]{3,}', L)}
        missing_nums = [x for x in nums(t) if x not in L]
        # assumption words are the invention family: each one in the claim must appear in the cited source line
        bad_assump = [w for w in re.findall(ASSUMPTION, t) if stem(w.split()[0]) not in Ls]
        cw = cwords(t); hit = sum(1 for w in cw if stem(w) in Ls)
        if missing_nums or bad_assump or (cw and hit / len(cw) < 0.35):
            print(f"[FAIL] {n:02d} claim not grounded in {s}: \"{t[:70]}\" | missing nums {missing_nums}, unsupported words {bad_assump}, stem hit {hit}/{len(cw)}"); fails += 1
    print(f"{n:02d} claims: {len(claims)} entries checked")
print(f"claims-check: {fails} FAIL")
sys.exit(1 if fails else 0)
