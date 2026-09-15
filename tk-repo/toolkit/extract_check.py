#!/usr/bin/env python3
"""extract_check.py [--claims extract_claims.json] [--table coverage.md] [NN ...] — did the extraction agents really add what
they said they added? Zero model tokens. Added 2026-09-07 (STR-DUB-2-batch1, user decision).

EXTRACT-SPEC.md makes every extraction agent reply `NN | script X | paragraph features added Y | prose specs added Z` with a
reason for every 0. Until now that line was only read. This script measures the truth: it rebuilds the SCRIPT baseline
(extract_html.py + keyfeat_cover.py --extract into _base/, from the same products.json) and counts, per product, how many
key_features lines and specs pairs the agent's extract/pNN.json carries beyond the baseline.

  --claims FILE   {"NN": {"kf": Y, "spec": Z, "reason": "..."}} written by the main context from the agents' reply lines.
                  FAIL when a claimed count differs from the measured one, or when a measured 0 has no reason.
  --table FILE    coverage table for the run log (README step 8): per product, KF source / added by agent / added by
                  para_feat review / final list items, and the same for Specifications; final counts read from final/dNN.json
                  when it exists. Lines marked "(main)" were added after extraction by the main context (para_feat triage) —
                  they are counted separately so an agent that added nothing still shows 0 in its own column.
Exit 1 on any FAIL; exit 0 otherwise. Works without --claims (measurement only).
"""
import json, os, re, sys, subprocess, shutil, html

def baseline():
    if not os.path.exists("_base/extract"):
        os.makedirs("_base", exist_ok=True); shutil.copy("products.json", "_base/products.json")
        for f in ("extract_html.py", "keyfeat_cover.py", "spec_cover.py"): shutil.copy(f, f"_base/{f}")
        subprocess.run(["python3", "extract_html.py", "products.json"], cwd="_base", capture_output=True)
        subprocess.run(["python3", "keyfeat_cover.py", "--extract"], cwd="_base", capture_output=True)
    return "_base/extract"

def norm(s): return re.sub(r"\s+", " ", str(s)).strip().lower()
def kf_items(h):
    m = re.search(r"<h3[^>]*>\s*Key Features\s*</h3>(.*?)(<h3|$)", h or "", re.S | re.I)
    return len(re.findall(r"<li[^>]*>", m.group(1))) if m else 0
def sp_items(h):
    m = re.search(r"<h3[^>]*>\s*Specifications[^<]*</h3>(.*?)(<h3|$)", h or "", re.S | re.I)
    return len(re.findall(r"<li[^>]*>", m.group(1))) if m else 0

if __name__ == "__main__":
    args = sys.argv[1:]; claims = None; table = None
    if "--claims" in args: i = args.index("--claims"); claims = json.load(open(args[i+1])); args = args[:i] + args[i+2:]
    if "--table" in args: i = args.index("--table"); table = args[i+1]; args = args[:i] + args[i+2:]
    ids = [int(x) for x in args] or sorted(int(f[1:3]) for f in os.listdir("extract") if f.endswith(".json"))
    bdir = baseline(); fails = 0; rows = []
    main_added = json.load(open("para_feat_added.json")) if os.path.exists("para_feat_added.json") else {}
    for n in ids:
        nn = f"{n:02d}"; e = json.load(open(f"extract/p{nn}.json")); b = json.load(open(f"{bdir}/p{nn}.json"))
        bkf = {norm(x) for x in b.get("key_features") or []}; bsp = {norm(f"{s.get('name')}: {s.get('value')}") for s in b.get("specs") or []}
        ma = main_added.get(nn, {}); mkf = {norm(x) for x in ma.get("kf", [])}; msp = {norm(f"{s.get('name')}: {s.get('value')}") for s in ma.get("spec", [])}
        akf = [x for x in e.get("key_features") or [] if norm(x) not in bkf and norm(x) not in mkf]
        asp = [s for s in e.get("specs") or [] if norm(f"{s.get('name')}: {s.get('value')}") not in bsp and norm(f"{s.get('name')}: {s.get('value')}") not in msp]
        fk = fs = "-"
        if os.path.exists(f"final/d{nn}.json"):
            h = json.load(open(f"final/d{nn}.json"))["descriptionHtml"]; fk, fs = kf_items(h), sp_items(h)
        rows.append((nn, len(bkf), len(akf), len(mkf), fk, len(bsp), len(asp), len(msp), fs))
        line = f"{nn} | script KF {len(bkf)} | agent KF +{len(akf)} | main KF +{len(mkf)} | script spec {len(bsp)} | agent spec +{len(asp)} | main spec +{len(msp)}"
        if claims is not None:
            c = claims.get(nn)
            if c is None: print(f"[FAIL] {nn} no claim line for this product"); fails += 1
            else:
                if int(c.get("kf", -1)) != len(akf): print(f"[FAIL] {nn} claimed {c.get('kf')} paragraph features added, measured {len(akf)}"); fails += 1
                if int(c.get("spec", -1)) != len(asp): print(f"[FAIL] {nn} claimed {c.get('spec')} prose spec pairs added, measured {len(asp)}"); fails += 1
                if (len(akf) == 0 or len(asp) == 0) and not (c.get("reason") or "").strip(): print(f"[FAIL] {nn} measured 0 additions without a reason"); fails += 1
        print(line)
    print(f"extract-check: {fails} FAIL across {len(ids)} products; agent additions total KF {sum(r[2] for r in rows)}, spec {sum(r[6] for r in rows)}; "
          f"main-context additions KF {sum(r[3] for r in rows)}, spec {sum(r[7] for r in rows)}")
    if table:
        with open(table, "w") as f:
            f.write("| # | KF source (script) | KF added by agent | KF added by main | KF final items | Spec source (script) | Spec added by agent | Spec added by main | Spec final items |\n|---|---|---|---|---|---|---|---|---|\n")
            for r in rows: f.write("| " + " | ".join(str(x) for x in r) + " |\n")
        print(f"table -> {table}")
    sys.exit(1 if fails else 0)
