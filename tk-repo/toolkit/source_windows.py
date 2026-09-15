#!/usr/bin/env python3
"""source_windows.py — every contiguous 2–4-word phrase of every source title, as DataForSEO candidates.

title-format-rule.md §1 (2026-09-05): "the source title's own keywords are always measured". Until 2026-09-06 the
splitting was done by the extraction agent and it missed obvious phrases (blr-batch24: `essential oil diffuser`
74,000 never measured; the title opened on `aromatherapy diffuser` 14,800). This script makes the split exhaustive
and model-free: no judgment, every window goes to the same DataForSEO call, fit and head-noun decide later.

  python3 source_windows.py products.json [kw.txt] > candidates/source_windows.txt

Reads the Phase 1 snapshot (shopify_api.py fetch format). Emits one lowercase keyword per line, deduped, sorted;
windows already present in kw.txt (if given) are skipped. Windows that start or end on a stop-word (for/with/and/
the/of/in/your/a/to) are dropped — they are not queries. The whole title is emitted too, when it fits. Output is
ADDED to the extraction agent's candidates before step 4; nothing is removed or ranked here.

DataForSEO length gate (added 2026-09-08, after STR-DUB-2-batch4): google_ads/search_volume/live rejects any
keyword over 80 characters or 10 words with `40501 Invalid Field: 'keywords'. Keyword text exceeds the allowed
limit`, and ONE bad keyword voids the WHOLE task — the call comes back with a top-level `20000 Ok` and zero
results, which reads as a successful call. In batch4, 49 of 1,277 windows were whole product titles over that
limit and the first attempt returned nothing on every chunk; the run recovered only because the empty result was
noticed. `windows()` now drops anything over the limit, so the phrase is absent from BOTH sides at once: it is not
offered as a candidate, and `title-check.py` — which imports `windows()` for its push-blocking "source windows NOT
measured" gate — no longer demands a phrase DataForSEO cannot measure. Nothing measurable is lost: an over-limit
window is always a whole supplier title, and every 2–4-word phrase inside it is emitted separately anyway.
"""
import json, re, sys

STOP = {"for", "with", "and", "the", "of", "in", "your", "a", "to", "on", "by", "or", "at"}
MIN_N, MAX_N = 2, 4

# DataForSEO google_ads/search_volume/live hard limits, per keyword.
MAX_CHARS, MAX_WORDS = 80, 10


def measurable(kw):
    """False for a phrase DataForSEO will reject — see the length-gate note in the module docstring."""
    return len(kw) <= MAX_CHARS and len(kw.split()) <= MAX_WORDS


def norm(title):
    s = title.lower()
    s = re.sub(r"\(.*?\)", " ", s)              # "(Random Color)"
    s = s.replace("&", " and ").replace("-", " ").replace("/", " ")
    s = re.sub(r"[^a-z0-9 ]", " ", s)           # drop apostrophes too — DataForSEO rejects them
    return s.split()


def windows(words, keep_oversize=False):
    """The 2–4-word windows plus the whole title. Over-limit phrases are dropped unless keep_oversize."""
    out = set()
    if len(words) >= 2:
        out.add(" ".join(words))                # the full title, as the rule already required
    for n in range(MIN_N, MAX_N + 1):
        for i in range(len(words) - n + 1):
            seg = words[i:i + n]
            if seg[0] in STOP or seg[-1] in STOP:
                continue
            if not any(re.search(r"[a-z]", w) for w in seg):   # "3 in 1" fine, "360 8" not
                continue
            out.add(" ".join(seg))
    if keep_oversize:
        return out
    return {w for w in out if measurable(w)}


def main():
    snap = json.load(open(sys.argv[1]))
    known = set()
    if len(sys.argv) > 2:
        for line in open(sys.argv[2]):
            if "|" in line:
                known.add(line.split("|", 1)[0].strip().lower())
    edges = snap["data"]["products"]["edges"] if "data" in snap else snap
    cands = set()
    for e in edges:
        node = e["node"] if "node" in e else e
        cands |= windows(norm(node.get("title", "")), keep_oversize=True)
    oversize = sorted(c for c in cands if not measurable(c))
    cands -= set(oversize)
    new = sorted(c for c in cands if c not in known)
    sys.stdout.write("\n".join(new) + ("\n" if new else ""))
    sys.stderr.write(
        f"source_windows: {len(edges)} titles -> {len(cands)} windows, {len(new)} not yet measured, "
        f"{len(oversize)} dropped over the DataForSEO limit ({MAX_CHARS} chars / {MAX_WORDS} words)\n"
    )
    for c in oversize:
        sys.stderr.write(f"  [oversize] {len(c)}c {len(c.split())}w  {c[:70]}…\n")


if __name__ == "__main__":
    main()
