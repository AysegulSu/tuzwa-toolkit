#!/usr/bin/env python3
"""fact_cover.py [NN ...] — "no source FACT is dropped" sweep (user decision 2026-09-05, zero model tokens).

Companion to value_check.py. value_check guards numbers, list items, package items and variant options;
this guards the sentences that carry no number — the adjective/claim/use-case lines a description agent can
quietly leave out with nothing to catch it (blr-batch23: p05 lost "Hygienic and non-absorbent", which the
user found in the live listing).

Scores every line of extract/pNN.json "facts" against the tag-stripped text of final/dNN.json descriptionHtml
by content-word stem overlap and prints the lines under 55%. Wording is free — the description is a rewrite —
so a low score is a CANDIDATE, never a verdict. This script is deliberately NOT wired into gate.py: the
description agents never see it, so it adds no agent turns.

Reading the output (main context, before payloads are built):
  a) a value RULINGS.md dropped on purpose -> leave it; it is already in that doc's omit_per_ruling
  b) the same meaning in different words -> leave it; this script matches words, not meaning
  c) a source line genuinely missing -> send ONLY those products back to their description agent, with the
     instruction to weave the fact into the right section IN ITS OWN WORDS. Never paste the source sentence.
     A health benefit the source states is woven in too (Safety Notes 2026-09-21); only a disease-treatment claim stays out.
Nothing is pushed until (c) is empty or the remaining line has a written reason in notes_for_log.

Usage: python3 fact_cover.py            # all products in final/
       python3 fact_cover.py 5 12 40    # only these
Exit 0 always — this is a review aid, not a gate.
"""
import json, glob, re, html, sys, os
STOP = set("""with that this your from into than then them they have will when while also each every over just more
most about after before their there these those which what where even both make makes made keep keeps gets give
gives take takes come comes need needs like same much very only and the for you our its all any can are not but one
two use used using such it's on in of to a is as at by or be it""".split())
def txt(h): return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', h or ''))).lower()
def stem(w): return w[:5] if len(w) > 5 else w
def cw(s): return [w for w in re.findall(r"[a-z]{3,}", s.lower()) if w not in STOP]
THRESHOLD = 0.55
ids = [int(a) for a in sys.argv[1:]] or None
files = sorted(glob.glob('final/d*.json'))
tot = 0; low = []
for f in files:
    n = int(os.path.basename(f)[1:3])
    if ids is not None and n not in ids: continue
    d = json.load(open(f)); ex = json.load(open(f'extract/p{n:02d}.json'))
    T = {stem(w) for w in re.findall(r'[a-z]{3,}', txt(d['descriptionHtml']))}
    omit = [o.lower() for o in d.get('omit_per_ruling', [])]
    tips = {t.strip().lower() for t in (ex.get('usage_tips') or [])}   # 2026-09-07: audience lines moved to facts are also usage tips
    # 2026-09-08: lines of the additional source sections (extract.sections) are enforced item by item by sections.py —
    # scoring their rewrite here is the same noise as scoring the usage-tip lines was.
    tips |= {l.strip().lower() for s in (ex.get('sections') or []) for l in s.get('lines', [])}
    for fact in ex['facts']:
        if fact.strip().lower() in tips:
            continue                      # covered by usage_tips.py / sections.py (every line an item, own words) — scoring the rewrite here is noise
        words = cw(fact)
        if len(words) < 3: continue
        tot += 1
        if any(o in fact.lower() or fact.lower() in o for o in omit):
            continue                      # case (a): RULINGS dropped it on purpose
        r = sum(1 for w in words if stem(w) in T) / len(words)
        if r < THRESHOLD: low.append((n, r, fact))
print(f"fact-cover: {tot} source fact lines scored (usage-tip and section lines skipped — usage_tips.py / sections.py cover them), {len(low)} below {int(THRESHOLD*100)}% — REVIEW EACH, none is a verdict")
for n, r, fact in sorted(low):
    print(f"  [{r:.2f}] {n:02d} {fact[:150]}")
