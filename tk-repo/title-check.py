#!/usr/bin/env python3
import json, re, sys, statistics, itertools, os
from head_check import opener_words, pt_head, same, sing   # §3 rule 2 head-noun test (toolkit/head_check.py)
KWF = sys.argv[1] if len(sys.argv) > 1 else "kw.txt"
PRF = sys.argv[2] if len(sys.argv) > 2 else "products.json"
STOP = {"for","the","and","with","of","a","in","to","on"}
def words(s):  return re.findall(r"[a-z0-9]+", s.lower())
def wset(s):   return frozenset(words(s)) - STOP
KW = {}
for ln in open(KWF):
    ln = ln.rstrip("\n")
    if not ln or ln.startswith("#"): continue
    k, v, c, p = ln.split("|")
    KW[k] = {"v": int(v), "c": c, "cpc": float(p) if p else None}
P = json.load(open(PRF))
_KWSETS = {frozenset(k.replace("'", "").split()) for k in KW}
fails, warns, manual = [], [], []
def F(pid, msg): fails.append(f"[FAIL] {pid}  {msg}")
def W(pid, msg): warns.append(f"[WARN] {pid}  {msg}")
def M(pid, msg): manual.append(f"[MANUAL] {pid}  {msg}")
report, rejects = {}, {}
# §5 "Units in the title" — HARD (user decision 2026-09-12): US store, US units. A number followed by a metric unit
# (cm, mm, m, g, kg, ml, l, and their spelled-out forms) never appears in the product title or the SEO title; the value
# is converted to in/ft/oz/lb (fl oz) or the spec goes to the description. Case-sensitive for the one-letter units so
# `5G`/`4G` (network) and `3M` are not caught; `cm`/`mm`/`kg`/`ml` and the words match in any case.
_METRIC = re.compile(r"\d+(?:\.\d+)?\s*(?:[cCmM][mM]|[kK][gG]|[mM][lL]|[cC]entimet(?:er|re)s?|[mM]illimet(?:er|re)s?|[kK]ilograms?|"
                     r"[mM]illilit(?:er|re)s?|[gG]rams?|[mM]et(?:er|re)s?|[lL]it(?:er|re)s?|m|g|l)(?![A-Za-z])")
def metric_hit(s):
    m = _METRIC.search(s)
    return m.group(0) if m else None
# §1 source-title windows — HARD check (user decision 2026-09-06, after the blr-batch24 audit: 368 source-title phrases had
# never been measured, `essential oil diffuser` 74,000 among them). README step 4 runs source_windows.py and measures its
# output; this verifies that it happened. Reads the Phase 1 snapshot (products.json in the working dir, or _config.snapshot).
SNAP = P.get("_config", {}).get("snapshot", "products.json")
try:
    from source_windows import norm as _sw_norm, windows as _sw_windows
    if not os.path.exists(SNAP):
        F("batch", f"source-title window check cannot run — snapshot '{SNAP}' not found (README step 4 / source_windows.py)")
    else:
        _snap = json.load(open(SNAP))
        _edges = _snap["data"]["products"]["edges"] if "data" in _snap else _snap
        _want = set()
        for _e in _edges:
            _n = _e["node"] if "node" in _e else _e
            _want |= _sw_windows(_sw_norm(_n.get("title", "")))
        _miss = sorted(w for w in _want if w not in KW)
        if _miss:
            F("batch", f"source windows NOT measured — {len(_miss)} of {len(_want)} source-title phrases missing from {KWF} "
                       f"(e.g. {_miss[:3]}). Run README step 4: python3 source_windows.py {SNAP} {KWF} → measure → append to {KWF}.")
except ImportError:
    F("batch", "source_windows.py not on disk — toolkit copy incomplete (MANIFEST step 0)")
for pid, d in P.items():
    if pid.startswith("_"): continue
    t = d["title"]; tl = t.lower(); L = len(t)
    if L > 145:               F(pid, f"title {L} chars > 145 hard ceiling")
    elif L > 135:             W(pid, f"title {L} chars — 135-145 exceptional tier, needs a >=20K cluster that would not fit by 135")
    elif L > 120:             M(pid, f"title {L} chars — 120-135 tier: name the trigger (A: >=20K cluster, or B: a tail keyword passing all 6 gates)")
    elif L < 70:              F(pid, f"title {L} chars < 70 — unspent base budget is unclaimed clusters (rule 6)")
    ws = words(t)
    if ws:
        noun, n = max(((w, ws.count(w)) for w in set(ws)), key=lambda x: x[1])
        if n >= 4:            F(pid, f"head noun '{noun}' x{n} — cap is 3, never 4")
        elif n == 3:          M(pid, f"head noun '{noun}' x3 — allowed only if the captured volume justifies it")
    for bad in ("free shipping","sale","best","cheapest","% off"):
        if bad in tl:         F(pid, f"promotional text in title: '{bad}'")
    if re.search(r"\b[A-Z]{3,}\b", re.sub(r"\b(LED|RGB|USB|IPX?\d+|HD|DVR|PU|TPR|CCTV|RV|PC|TF|AUX|WiFi|SATA|IDE|UV)\b", "", t)):
        W(pid, "possible ALL-CAPS word in title")
    # §5 units — metric in the title is a FAIL (user decision 2026-09-12): convert to in/ft/oz/lb or move the spec to the description
    _mh = metric_hit(t)
    if _mh:                   F(pid, f"metric unit in title: '{_mh.strip()}' — US store, write it in inch/ft/oz/lb (§5 Units) or drop the spec to the description")
    if d.get("seo_title") and metric_hit(d["seo_title"]):
        F(pid, f"metric unit in seo.title: '{metric_hit(d['seo_title']).strip()}' — write it in inch/ft/oz/lb (§5 Units)")
    if d.get("seo_title") and len(d["seo_title"]) >= 70:
        F(pid, f"seo.title {len(d['seo_title'])} chars >= 70")
    if d.get("seo_desc") and len(d["seo_desc"]) >= 160:
        F(pid, f"seo.description {len(d['seo_desc'])} chars >= 160")
    cluster = [k for k in d["cluster"] if k in KW and KW[k]["v"] > 0]
    missing = [k for k in d["cluster"] if k not in KW]
    if missing:               W(pid, f"{len(missing)} cluster keywords have no measured data: {missing[:3]}")
    captured = [k for k in cluster if k in tl]
    capsets  = {k: wset(k) for k in captured}
    vol, seen = 0, []
    for k in sorted(captured, key=lambda x: -KW[x]["v"]):
        if any(wset(k) == wset(s) or (KW[k]["v"] == KW[s]["v"] and k in s or s in k) for s in seen): continue
        seen.append(k); vol += KW[k]["v"]
    # §3 rule 2 — HARD checks (user decision 2026-09-05, blr-batch23 audit: 6 of 49 openers were unmeasured or outranked
    # while this was only a MANUAL note). Both need the §10b productType in check_products.json ("productType").
    pt = d.get("productType") or ""
    seg = re.split(r"\b(for|with)\b", t.split(",")[0], 1, flags=re.I)[0]
    segw = re.findall(r"[A-Za-z0-9]+", seg)
    if not pt:
        F(pid, "no productType in check_products.json — the §3 rule 2 opener checks cannot run (producttype_draft.json)")
    else:
        # head candidates: the productType's own last word first (`Leather Fix Kit` -> kit), then the generic-tail-stripped head
        ptw = [w for w in re.findall(r"[A-Za-z]+", re.split(r"\b(for|with)\b", pt, 1, flags=re.I)[0]) if w.lower() not in STOP]
        heads = [sing(ptw[-1])] if ptw else []
        if pt_head(pt) not in heads: heads.append(pt_head(pt))
        hi = next((i for i in range(len(segw) - 1, -1, -1) if any(same(sing(segw[i]), h) for h in heads)), None)
        if hi is None:
            F(pid, f"opener '{seg.strip()}' has no word matching productType head {heads} ({pt}) — head-noun test")
        else:
            phrase = " ".join(segw[:hi + 1]).lower(); pset = wset(phrase)
            # keywords that live inside the opener phrase: contiguous substring, or the same words in another order
            # (word-order variants are one query, §2)
            fullset = wset(seg)
            inside = [k for k in KW if k in phrase or wset(k) == pset or wset(k) == fullset]
            # (a) the opener phrase must be measured: the phrase itself, or a measured keyword inside it that ends on the
            # head noun (`car scratch remover PEN` carries measured `scratch remover pen`). Unmeasured openers reached the
            # store in blr-batch23: 'wall art', 'rompers', 'mens jacket', 'cordless headphones'.
            ok = any(any(same(sing(k.split()[-1]), h) for h in heads) for k in inside)
            if not ok:
                F(pid, f"opener phrase '{phrase}' was never measured — look it up (one DataForSEO call, TITLE-SPEC 1b) before it may open a title")
            # (b) the highest-volume captured keyword that names the product type must sit inside the opener phrase;
            # a tie is fine, a lower-volume opener is not (`presser foot` 2,400 opening while `sewing machine presser foot`
            # 8,100 sits later; `womens suit set` 12,100 ahead of `tailored suit women` 18,100).
            fitting = [k for k in captured if any(same(sing(w), h) for h in heads for w in re.findall(r"[a-z]+", k))]
            top_in = max((KW[k]["v"] for k in inside), default=0)
            if fitting:
                top = max(fitting, key=lambda k: KW[k]["v"])
                if KW[top]["v"] > top_in:
                    F(pid, f"rule 2: '{top}' ({KW[top]['v']:,}) is the highest captured keyword that names the product type, but the opener is '{phrase}' ({top_in:,}) — it must open the title, or be fit-rejected with a written reason")
    # §2/§3.7 cluster-core check — HARD (user decision 2026-09-06, blr-batch24 audit: 5 of 154 comma clusters carried no
    # measured phrase at all — `Automatic Robotic Vacuum for Carpet` had rewritten measured `robot vacuum for carpet`).
    # Every comma cluster must contain at least one measured 2+-word phrase (its "core"); the words around the core —
    # leading attributes, a trailing for/with tail — stay free. Not a keyword-list rule: only the core must be measured.
    # Exceptions: a cluster that is only a §5 defining number (`10 Pack`, `Set of 4`, `2 Pack`); apostrophes are ignored
    # on both sides; a word-order variant of a measured keyword counts as measured (§2: one query).
    _clusters = []
    for c in t.split(","):
        cw = re.findall(r"[a-z0-9']+", c.lower())
        cw = [w for w in cw if w not in ("'",)]
        while cw and cw[0].strip("'") in STOP: cw.pop(0)
        while cw and cw[-1].strip("'") in STOP: cw.pop()
        if len(cw) < 2: continue
        if not [w for w in cw if not re.fullmatch(r"\d+|pack|piece|pieces|pcs|pair|pairs|count|set|of|in|x|inch|inches|ft|fl|oz|lb|lbs|gal|qt", w)]:
            continue                                            # §5 defining-number cluster, no keyword expected (US units only, 2026-09-12)
        def _m(ph):
            a = ph.replace("'", ""); b = ph
            if a in KW or b in KW: return True
            for cand in (a, b):
                w = cand.split()
                alts = [" ".join(w[:-1] + [w[-1][:-1]])] if w[-1].endswith("s") else [" ".join(w[:-1] + [w[-1] + "s"])]
                if any(x in KW for x in alts): return True
            fs = frozenset(a.split())
            return fs in _KWSETS
        core = next((" ".join(cw[i:j]) for n in range(len(cw), 1, -1) for i in range(len(cw) - n + 1) for j in [i + n] if _m(" ".join(cw[i:j]))), None)
        if core is None:
            F(pid, f"cluster '{c.strip()}' has no measured phrase in it — rebuild it around a measured keyword (§2), or measure the phrase you mean (TITLE-SPEC 1b)")
        else:
            # the cluster's value = the biggest measured keyword inside it (used by the unused-keyword check below)
            _ph = [" ".join(cw[i:j]) for n in range(len(cw), 1, -1) for i in range(len(cw) - n + 1) for j in [i + n]]
            _vals = [KW[x]["v"] for ph in _ph for x in (ph, ph.replace("'", "")) if x in KW]
            _clusters.append((c.strip(), max(_vals) if _vals else 0))
    # Old-vs-new captured volume — HARD (user decision 2026-09-06). The source title's windows are measured now (source_windows.py),
    # so the volume the OLD title captured is computable. Compared on PRODUCT-NAMING keywords only (last word = productType head,
    # same test as rule 2): a supplier title full of parent-category words (`washing machines` 201,000 on a shoe bag) must not win
    # on volume it cannot convert. Fit-rejected keywords are excluded on both sides. New < old on fitting volume = FAIL; new < old
    # on total measured volume = WARN (worth a look, not a block). Needs the old title: d["old_title"], or the snapshot by index/id.
    def _cap(title, keys):
        tl_ = title.lower().replace("'", ""); got = []
        for k in keys:
            kk = k.replace("'", "")
            if kk and kk in tl_: got.append(k)
        vol_, seen_ = 0, []
        for k in sorted(got, key=lambda x: -KW[x]["v"]):
            if any(wset(k) == wset(s_) or (KW[k]["v"] == KW[s_]["v"] and (k in s_ or s_ in k)) for s_ in seen_): continue
            seen_.append(k); vol_ += KW[k]["v"]
        return vol_, seen_
    old = d.get("old_title")
    if old is None and os.path.exists(SNAP):
        try:
            _snap2 = json.load(open(SNAP)); _edges2 = _snap2["data"]["products"]["edges"] if "data" in _snap2 else _snap2
            _nodes2 = [e_["node"] if "node" in e_ else e_ for e_ in _edges2]
            gid = d.get("product_id") or d.get("id")
            if gid: old = next((n_["title"] for n_ in _nodes2 if n_.get("id") == gid), None)
            elif pid.isdigit() and int(pid) < len(_nodes2): old = _nodes2[int(pid)]["title"]
        except Exception: old = None
    if old is None:
        W(pid, "old-vs-new volume check NOT RUN — old title not found (add old_title or product_id to check_products.json)")
    elif pt:
        _rej = set(d.get("fit_reject", []))
        _all = [k for k in KW if KW[k]["v"] > 0 and k not in _rej]
        _fit = [k for k in _all if any(same(sing(w_), h) for h in heads for w_ in re.findall(r"[a-z]+", k))]
        ov, ok_ = _cap(old, _fit); nv, nk_ = _cap(t, _fit)
        if ov > nv:
            F(pid, f"old title captured MORE product-naming volume than the new one: old {ov:,} vs new {nv:,} — old had {[k for k in ok_ if k not in nk_][:3]}")
        ot, _ = _cap(old, _all); nt, _ = _cap(t, _all)
        if ot > nt:
            W(pid, f"old title captured more TOTAL measured volume: old {ot:,} vs new {nt:,} (includes non-product keywords; check nothing fitting was dropped)")
        report.setdefault(pid, {})
        d["_oldnew"] = (ov, nv, ot, nt)
    # Unused higher-volume keyword — HARD unless a reason is written (user decision 2026-09-06, option b). The TRIMMERYENI #08
    # lesson for the non-opener slots: `weed trimmer` 9,900 was written while measured, fit-clean `cordless grass trimmer` 12,100
    # sat unused. Any measured candidate (>= 1,000, not fit-rejected, not already captured or a twin of a captured keyword)
    # whose volume beats the WEAKEST non-opener cluster's value must either enter the title or carry a one-line reason in
    # d["skip_reasons"] (skip_reasons.json -> build_check.py). No reason = FAIL. Reasons go to rejects.json for the run log.
    _sr = {k.lower(): v for k, v in (d.get("skip_reasons") or {}).items()}
    if len(_clusters) >= 2:
        _floor = min(v for _, v in _clusters[1:])
        _rejk = set(d.get("fit_reject", []))
        _unused = []
        for k in cluster:
            if k in _rejk or KW[k]["v"] < 1000 or KW[k]["v"] <= _floor: continue
            if k.replace("'", "") in tl.replace("'", ""): continue
            ks_ = wset(k)
            if any(ks_ == cs or k in c_ or c_ in k for c_, cs in capsets.items()): continue
            if any(KW[c_]["v"] == KW[k]["v"] and len(ks_ & cs) / max(1, min(len(ks_), len(cs))) >= 0.5 for c_, cs in capsets.items()): continue
            _unused.append(k)
        _unused.sort(key=lambda x: -KW[x]["v"])
        _weak = min(_clusters[1:], key=lambda x: x[1])
        def _reason(k):   # a reason written for a longer/shorter form of the same phrase covers it too (one query family)
            return _sr.get(k) or next((r for kk, r in _sr.items() if kk in k or k in kk), None)
        for k in _unused:
            if _reason(k):
                _sr[k] = _reason(k)
                M(pid, f"unused '{k}' {KW[k]['v']:,} > weakest cluster '{_weak[0]}' {_weak[1]:,} — skipped with reason: {_sr[k]}")
            else:
                F(pid, f"unused measured keyword '{k}' {KW[k]['v']:,} beats the weakest cluster '{_weak[0]}' ({_weak[1]:,}) — put it in the title, or write a one-line reason in skip_reasons.json")
        d["_unused_reasoned"] = [{"kw": k, "volume": KW[k]["v"], "reason": _sr[k]} for k in _unused if k in _sr]
    rej  = set(d.get("fit_reject", []))
    # second-net cap (description-format-rule.md, 2026-09-03): top 8 distinct query families by volume
    sac = sorted((k for k in cluster if k not in captured and k not in rej and KW[k]["v"] >= 1000), key=lambda x: (-KW[x]["v"], len(x)))
    fams, second_net, capped = [(wset(c), c) for c in captured], [], []
    def _twin(k, ks, f, f2):
        same_v = KW[k]["v"] == KW[f2]["v"]
        jac = len(ks & f) / max(1, len(ks | f))
        return ks == f or (same_v and (k in f2 or f2 in k or jac >= 0.5))
    for k in sac:
        ks = wset(k)
        twin = any(_twin(k, ks, f, f2) for f, f2 in fams)
        if twin: continue
        if len(second_net) < 8: second_net.append(k); fams.append((ks, k))
        else: capped.append(k)
    cpcs = [KW[k]["cpc"] for k in cluster if KW[k]["cpc"] is not None]
    med  = statistics.median(cpcs) if cpcs else None
    rej  = set(d.get("fit_reject", []))
    tail = []
    for k in cluster:
        if k in captured or k in rej: continue
        e = KW[k]
        if e["v"] < 1000: continue
        g4 = e["c"] in ("L","M") or (e["cpc"] is not None and med is not None and e["cpc"] < med)
        if not g4: continue
        if any(k in c or c in k for c in captured): continue
        ks = wset(k)
        if any(ks == cs for cs in capsets.values()): continue
        if any(KW[c]["v"] == e["v"] and len(ks & cs) / max(1, min(len(ks), len(cs))) >= 0.5
               for c, cs in capsets.items()): continue
        arm = f"comp {e['c']}" if e["c"] in ("L","M") else f"CPC ${e['cpc']:.2f} < med ${med:.2f}"
        tail.append((e["v"], k, arm))
    tail.sort(reverse=True)
    for v, k, arm in tail[:3]:
        M(pid, f"tail candidate '{k}' {v:,} [{arm}] — decide gate 1 (product fit) and gate 2 (contiguous, within {135-L} chars, head-noun cap)")
    if "description" in d:
        dl = re.sub(r"<[^>]+>", " ", d["description"]).lower()
        dl = re.sub(r"\s+", " ", dl)
        head = dl[:500]
        def variant(k):
            w = k.split()
            alt = {" ".join(w[:-1] + [w[-1].rstrip("s")]), " ".join(w[:-1] + [w[-1] + "s"])} - {k}
            return next((a for a in alt if a in dl), None)
        gone, tail_only, varonly = [], [], []
        for k in captured:
            if k in head: continue
            if k in dl:   tail_only.append(k); continue
            v = variant(k)
            (varonly if v else gone).append(f"{k}" + (f" (only '{v}')" if v else ""))
        if gone:
            W(pid, f"rule 1 — {len(gone)} title keyword(s) ABSENT from the description: " + ", ".join(gone))
        if varonly:
            W(pid, f"rule 1 — {len(varonly)} title keyword(s) present only as a singular/plural variant: " + ", ".join(varonly))
        if tail_only:
            W(pid, f"rule 1 — {len(tail_only)} title keyword(s) appear only after the first 500 chars (feed truncation risk): " + ", ".join(tail_only[:4]))
        absent = [k for k in second_net if k not in dl]
        if absent:
            W(pid, f"second net: {len(absent)} sacrificed keywords absent from the description, top: " + ", ".join(f"{k} ({KW[k]['v']:,})" for k in sorted(absent, key=lambda x:-KW[x]['v'])[:3]))
    else:
        W(pid, "second net NOT CHECKED — no description supplied")
    if "description" in d and "cdn_prefix" in P.get("_config", {}):
        for src in re.findall(r'<img[^>]+src="([^"]+)"', d["description"]):
            if P["_config"]["cdn_prefix"] not in src:
                F(pid, f"foreign-CDN image still in description: {src[:70]}")
    rejects[pid] = {
        "title": t,
        "captured": sorted(({"kw": k, "volume": KW[k]["v"]} for k in captured), key=lambda x: -x["volume"]),
        "sacrificed": [{"kw": k, "volume": KW[k]["v"], "competition": KW[k]["c"]} for k in second_net],
        "capped": [{"kw": k, "volume": KW[k]["v"], "reason": "second-net cap"} for k in capped],
        "twins_collapsed": [k for k in sac if k not in second_net and k not in capped],
        "skipped_with_reason": d.get("_unused_reasoned", []),
    }
    report[pid] = {"len": L, "captured_volume": vol, "tail": tail, "old_vs_new": d.get("_oldnew")}
ids = [k for k in P if not k.startswith("_")]
# §8 (8.1 first-40-chars, 8.2 word overlap) is SUSPENDED in full (user decision 2026-09-05) — not checked here, not in-batch,
# not reported. The rule text and the catalog-end plan live in claude/rule-overlap-deferred.md.
print(f"title-check — {len(ids)} products, {len(KW)} measured keywords\n")
for line in fails:  print(line)
for line in warns:  print(line)
for line in manual: print(line)
print(f"\nsummary: {len(fails)} FAIL, {len(warns)} WARN, {len(manual)} MANUAL REVIEW")
print(f"products with an open tail candidate: {sum(1 for r in report.values() if r['tail'])}/{len(ids)}")
json.dump(rejects, open("rejects.json", "w"), indent=1)
json.dump(report, open("title-report.json", "w"), indent=1)
n = sum(1 for r in rejects.values() for k in r["sacrificed"] if k["volume"] >= 1000)
print(f"\nrejects.json written — {n} second-net keywords (top 8 per product) across {len(ids)} products; capped: {sum(len(r['capped']) for r in rejects.values())}.")
if fails: print("\nDO NOT PUSH — resolve the failures first.")
sys.exit(1 if fails else 0)
