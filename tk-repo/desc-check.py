#!/usr/bin/env python3
"""desc-check.py — pre-push gate for internal-note leakage in customer copy.

Implements the "FORBIDDEN — writer's internal notes leaking into customer copy"
section of description-format-rule.md (added 2026-09-02 after ddl1-batch5).

Any match is a HARD STOP for that product: regenerate the field, re-check, push.
Never push and fix later.

Usage:
    python3 desc-check.py products.json          # scan a Shopify query dump
    python3 desc-check.py --fields rewrites.json # scan a rewrites payload
"""
import json, re, sys, html

# Phrases that mean the writer is talking about the writing, the sourcing, or its
# own decisions — never allowed in any customer-facing field.
BLOCKED = [
    r"\bthe supplier\b", r"\bsupplier(?:'s)? (?:states?|says?|names?|gives?|omits?|makes?|calls?|describes?|lists?)\b",
    r"\bby the supplier\b", r"\bthe maker\b", r"\bthe manufacturer states\b",
    r"\bthe source\b", r"\bsource (?:states?|omits?|says?|names?|leaves?|does not)\b",
    r"\bthis listing\b", r"\bthe listing\b", r"\banother listing\b", r"\bthe original listing\b",
    r"\bleftover text\b", r"\bon the images\b", r"\bthe images say\b", r"\bimage text\b",
    r"\bwe claim\b", r"\bwe make no\b", r"\bwe quote no\b", r"\bwe omit\b", r"\bwe state\b",
    r"\bnor do we\b", r"\bneither do we\b", r"\bso we claim\b", r"\bclaim none\b",
    r"\bno .{0,30}claim is made\b",
    r"\b(?:is|are|was|were) (?:not )?(?:claimed|quoted|stated|specified|cited)\b",
    r"\bnot (?:stated|specified|given|claimed|quoted|cited|named|provided|disclosed)\b",
    r"\bno .{0,40}(?:is|are) (?:given|stated|listed|named|provided|specified|quoted)\b",
    r"\bnone is (?:claimed|quoted|stated|given)\b", r"\bis not (?:stated|specified|given|claimed|named)\b",
    r"\bdoes not (?:state|specify|name|give|tie)\b", r"\bnever the\b",
    r"\bwhat is not claimed\b", r"\bno safety certification\b",
    r"\bwording (?:the|that)\b", r"\bthe .{0,20}wording\b", r"\bas written\b",
    r"\bper the spec sheet\b", r"\bthe spec sheet\b", r"\bthe writer\b",
    r"\bthis rewrite\b", r"\bthis description\b", r"\bin (?:the supplier|its own) terms\b",
    r"\bfigures contradict\b", r"\bcontradicts?\b", r"\bboilerplate\b",
    r"\bno .{0,40}(?:is|are) published\b", r"\b(?:is|are) not published\b", r"\bnot published\b",
    r"\bunconfirmed\b", r"\buncertified\b", r"\bspec list\b", r"\bsource spec\b", r"\bsource (?:line|listing|text|copy|page)\b", r"\bcontradicted\b", r"\(source\b", r"\bsource says\b", r"\bunverified\b", r"\bunspecified\b", r"\bnot certified\b", r"\bstated safety\b",
    r"\b(?:figures|percentages|specs?|specifications) conflict\b",
    r"\bno .{0,40}(?:certification|rating|figure|claim|count|percentages?) (?:is|are)?\s?(?:stated|cited|given|listed|claimed)?\b",
    r"\bclaims? no\b", r"\bno .{0,30}(?:performance|protection) claimed\b",
    r"\bnone (?:is|are) (?:invented|claimed|quoted|published)\b", r"\bso none\b",
    r"\bwe (?:do not|don't|cannot|can't) (?:print|claim|quote|state)\b",
    # keyword-alias lists — banned outright (2026-09-02)
    r"\balso sold as\b", r"\balso known as\b", r"\baka\s*:", r"\bother names\b",
    r"\balternative names\b", r"\bsearch terms\b", r"\brelated terms\b",
    r"\balso called\b", r"\bsometimes called\b", r"\bunder other names\b",
    r"\bthe same .{0,30} under other\b",
    # softer source-attribution language (round 4, 2026-09-02)
    r"\b(?:is|are|was|were)? ?(?:listed|stated|described|quoted|labelled|labeled) (?:as|for|only as|in)\b",
    r"\bnothing states\b", r"\bthe (?:feature|body) copy\b", r"\bthe spec (?:table|sheet)\b",
    r"\bspec sheet\b", r"\bthe specification\b", r"\bspec table\b", r"\bby the manufacturer\b",
    r"\bper the spec\b", r"\b(?:is|are) (?:listed|stated|described)\b",
    r"\bno (?:further |wash |care |size )?(?:chart|instructions|dimensions|figures?|measurements|details?)\b[^.]{0,25}\b(?:supplied|given|provided|available)\b",
    r"\bwhat is not supplied\b", r"\bno further measurements\b",
    r"\bthe only figure given\b", r"\bper a typical\b", r"\bfeature list\b", r"\bfeature line\b", r"\bbox list\b", r"\bunstated\b",
    r"\(\s*(?:maker|manufacturer|supplier)[^)]*\)", r"\bmaker (?:stated|states|labels|lists|says)\b",
]
PAT = re.compile("|".join(BLOCKED), re.I)

# Semantic sweep: negation near an information-word (catches phrasings the fixed list misses).
NEG = re.compile(r"\b(?:no|not|none|never|without|nothing)\b.{0,60}?\b(?:stated|specified|given|listed|published|named|cited|claimed|quoted|confirmed|disclosed|declared|percentages?|content)\b", re.I)
ALLOW = re.compile(r"\b(?:not included|no .{0,20}included|not for submersion|not a medical device|not personal protective|without opening)\b", re.I)

# Fields that are customer-facing and therefore gated.
FIELDS = ("title", "descriptionHtml", "seo.title", "seo.description")


def strip(h):
    return html.unescape(re.sub(r"<[^>]+>", " ", h or ""))


def sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.?!:])\s+", text) if s.strip()]


def check(pid, label, field, value):
    out = []
    for s in sentences(strip(value)):
        m = PAT.search(s)
        if m:
            out.append((pid, label, field, m.group(0), s[:240]))
            continue
        m = NEG.search(s)
        if m and not ALLOW.search(s):
            out.append((pid, label, field, "SEMANTIC:" + m.group(0)[:40], s[:240]))
    return out


def main():
    path = sys.argv[-1]
    doc = json.load(open(path))
    nodes = []
    if isinstance(doc, dict) and "data" in doc:
        nodes = [e["node"] for e in doc["data"]["products"]["edges"]]
    elif isinstance(doc, list):
        nodes = doc
    hits = []
    for n in nodes:
        pid = n.get("id", "?").split("/")[-1]
        label = (n.get("title") or "")[:55]
        for f in FIELDS:
            v = n
            for part in f.split("."):
                v = (v or {}).get(part) if isinstance(v, dict) else None
            if isinstance(v, str):
                hits += check(pid, label, f, v)
    bad = sorted({h[0] for h in hits})
    for h in hits:
        print(f"{h[0]} | {h[1]} | {h[2]} | <{h[3]}> | {h[4]}")
    print(f"\n{len(hits)} hits across {len(bad)} of {len(nodes)} products")
    sys.exit(1 if hits else 0)


if __name__ == "__main__":
    main()
