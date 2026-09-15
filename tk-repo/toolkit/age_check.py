#!/usr/bin/env python3
"""age_check.py NN [NN ...] — "state the range, never one end of it" review sweep (user decision 2026-09-06, zero model tokens).

Rule: description-format-rule.md "Age ranges". A single-age phrase ("toys for 4 year olds", "gifts for a 3 year old")
may appear in the description ONLY when it is a keyword captured by the product title, at most once, and inside a
sentence that also states the full range or its upper end ("ages 4-5+", "2 to 5", "3 years and up", "through age five").

WARN, never FAIL (user decision): a single-age phrase whose sentence carries no range wording; a single-age phrase not in
the product title; more than one single-age sentence in the description. Nothing to scan -> one "clean" line.
Fields scanned: description (tag-stripped), seo.title, seo.description. Exit 0 always.
"""
import json, re, sys, html
SINGLE = re.compile(r"\b(?:for |gifts? for |toys? for )?(?:a |an )?(\d{1,2}|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)[- ]year[- ]olds?\b", re.I)
RANGE = re.compile(r"\b(?:ages?\s*\d{1,2}\s*(?:-|–|to|through)\s*\d{1,2}\+?|\d{1,2}\s*(?:-|–|to|through)\s*\d{1,2}\s*(?:\+|years?|yrs?)|\d{1,2}\+|(?:years?|yrs?|age)\s*(?:and|or|&)\s*(?:up|over|older|above)|and up\b|through age\b|up to (?:age )?\d{1,2}|from (?:age )?\d{1,2}\b|between \d{1,2} and \d{1,2})", re.I)
def strip(h): return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', h or '')))
def sentences(t): return [s.strip() for s in re.split(r'(?<=[.!?])\s+', t) if s.strip()]
warns = 0
for n in sys.argv[1:]:
    n = int(n); d = json.load(open(f'final/d{n:02d}.json'))
    title = d.get('title', '').lower()
    fields = [('description', strip(d['descriptionHtml'])), ('seo.title', (d.get('seo') or {}).get('title', '')),
              ('seo.description', (d.get('seo') or {}).get('description', ''))]
    found = 0
    for fname, text in fields:
        for s in sentences(text):
            for m in SINGLE.finditer(s):
                found += 1; phrase = m.group(0).strip()
                if not RANGE.search(s):
                    warns += 1; print(f"[WARN] {n:02d} single-age phrase without a range in the same sentence — {fname}: \"{s[:140]}\"")
                if phrase.lower() not in title:
                    warns += 1; print(f"[WARN] {n:02d} single-age phrase {phrase!r} is not a title keyword — {fname} (rule: only a captured title keyword may carry a single age)")
    if found > 1: warns += 1; print(f"[WARN] {n:02d} {found} single-age phrases — the rule allows at most one")
    print(f"{n:02d} age-check: {found} single-age phrase(s)" + (" — clean" if found == 0 else ""))
print(f"age-check: {warns} WARN (review, not blocking)")
