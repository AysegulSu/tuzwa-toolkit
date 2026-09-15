#!/usr/bin/env python3
"""rehost.py — re-host every foreign description image to our own CDN (Backend doc Q14), zero model tokens.
Added to the toolkit 2026-09-06 after blr-batch25, where this step was written ad hoc, crashed on Shopify
"Internal Server Error" responses with the created file ids only in memory, and left ~50 duplicate files in Files.

  python3 rehost.py [cdn_prefix]          # default cdn_prefix = cdn.shopify.com/s/files/1/0806/1645/6416/ (Tuzwa)

Reads extract/pNN.json (images[].src). For every src not on cdn_prefix:
  1. fileCreate in groups of 10 (originalSource = the foreign URL, Shopify fetches server-side; no staged upload).
     The returned ids are written to image_ids.json AFTER EVERY GROUP — a crash or re-run continues from that file,
     nothing is uploaded twice.
  2. Polls the ids until READY, writes foreign_url -> new CDN url to image_map.json. FAILED files are logged with the
     product index and URL and left untouched (the Backend doc: never push a broken image; never delete a source image).
  3. Rewrites images[].src in extract/pNN.json (old value kept as src_original) and clears foreign_images.
Every Admin API call retries up to 6 times on errors. Prints one summary line at the end; exit 1 if anything is
still foreign.
"""
import json, os, sys, time, glob
from shopify_api import gql

CDN = sys.argv[1] if len(sys.argv) > 1 else "cdn.shopify.com/s/files/1/0806/1645/6416/"
IDS, MAP = "image_ids.json", "image_map.json"

def g(q, v=None):
    for a in range(6):
        try: return gql(q, v)
        except BaseException as ex:
            print(f"  api retry {a}: {str(ex)[:80]}"); time.sleep(8)
    raise SystemExit("rehost: Admin API failed 6 times — re-run later; image_ids.json keeps what was created")

def load(p): return json.load(open(p)) if os.path.exists(p) else {}

# 1. collect foreign urls (in product order, deduped)
urls, owner = [], {}
for p in sorted(glob.glob("extract/p*.json")):
    e = json.load(open(p))
    for im in e["images"]:
        if CDN not in im["src"] and im["src"] not in owner:
            urls.append(im["src"]); owner[im["src"]] = e["idx"]
ids, M = load(IDS), load(MAP)
print(f"rehost: {len(urls)} foreign images; {len(ids)} already created, {sum(1 for u in urls if M.get(u))} already mapped")

# 2. create the missing ones, saving ids after every group
todo = [u for u in urls if u not in ids and not M.get(u)]
Q = "mutation($files:[FileCreateInput!]!){ fileCreate(files:$files){ files{ id fileStatus } userErrors{ field message } } }"
for b in range(0, len(todo), 10):
    chunk = todo[b:b + 10]
    fc = g(Q, {"files": [{"originalSource": u, "contentType": "IMAGE"} for u in chunk]})["data"]["fileCreate"]
    if fc["userErrors"]: print("  userErrors:", fc["userErrors"])
    for u, f in zip(chunk, fc["files"]):
        if f and f.get("id"): ids[u] = f["id"]
    json.dump(ids, open(IDS, "w"), indent=1)
    print(f"  created {min(b + 10, len(todo))}/{len(todo)}"); time.sleep(1)

# 3. poll to READY
pending = {u: i for u, i in ids.items() if not M.get(u)}
for attempt in range(60):
    if not pending: break
    time.sleep(6)
    d = g("query($ids:[ID!]!){ nodes(ids:$ids){ ... on MediaImage { id fileStatus fileErrors { code message } image { url } } } }",
          {"ids": list(pending.values())})
    by = {n["id"]: n for n in d["data"]["nodes"] if n}
    for u, fid in list(pending.items()):
        n = by.get(fid)
        if not n: continue
        if n["fileStatus"] == "READY" and n.get("image") and n["image"].get("url"):
            M[u] = n["image"]["url"]; del pending[u]
        elif n["fileStatus"] == "FAILED":
            M[u] = None; del pending[u]; print(f"  FAILED p{owner[u]:02d} {u} {n.get('fileErrors')}")
    json.dump(M, open(MAP, "w"), indent=1)
    print(f"  poll {attempt}: {len(pending)} pending")

# 4. rewrite extract srcs
n = 0
for p in sorted(glob.glob("extract/p*.json")):
    e = json.load(open(p))
    for im in e["images"]:
        if CDN not in im["src"] and M.get(im["src"]):
            im["src_original"] = im["src"]; im["src"] = M[im["src"]]; n += 1
    e["foreign_images"] = [im["src"] for im in e["images"] if CDN not in im["src"]]
    json.dump(e, open(p, "w"), indent=1, ensure_ascii=False)
still = sum(len(json.load(open(p))["foreign_images"]) for p in glob.glob("extract/p*.json"))
print(f"rehost: {sum(1 for u in urls if M.get(u))} mapped, {sum(1 for u in urls if u in M and not M[u])} failed, {n} srcs rewritten, {still} still foreign")
sys.exit(1 if still else 0)
