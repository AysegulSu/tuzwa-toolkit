#!/usr/bin/env python3
"""shopify_api.py — script access to the Tuzwa Admin API (no MCP, no model tokens).
Reads client credentials from secrets/shopify.json (copy them from the project doc
shopify-api-credentials.md at session start), caches a 24 h token in secrets/token.json.

  from shopify_api import gql
  gql(query, variables) -> dict            # raises on HTTP/GraphQL errors, retries on throttle

CLI:  python3 shopify_api.py fetch <tag> products.json     # all products of a tag, full fields (paginated)
      python3 shopify_api.py mutate push/mut0.json         # fire one {"query","variables"} file, print userErrors
"""
import json, subprocess, sys, time, os
API = "2025-07"
def _creds():
    return json.load(open(os.path.join(os.path.dirname(__file__), "secrets", "shopify.json")))
def token(force=False):
    p = os.path.join(os.path.dirname(__file__), "secrets", "token.json")
    if not force and os.path.exists(p):
        t = json.load(open(p))
        if time.time() < t.get("exp", 0) - 300: return t["token"]
    c = _creds()
    out = subprocess.run(["curl", "-sS", "-m", "30", "-X", "POST", f"https://{c['shop']}/admin/oauth/access_token",
                          "-H", "Content-Type: application/json",
                          "-d", json.dumps({"client_id": c["client_id"], "client_secret": c["client_secret"], "grant_type": "client_credentials"})],
                         capture_output=True, text=True).stdout
    d = json.loads(out)
    if "access_token" not in d: raise SystemExit(f"token error: {out[:300]}")
    json.dump({"token": d["access_token"], "exp": time.time() + d.get("expires_in", 86000)}, open(p, "w"))
    return d["access_token"]
def gql(query, variables=None, retries=6):
    c = _creds()
    for attempt in range(retries):
        body = json.dumps({"query": query, "variables": variables or {}})
        tmp = f"/tmp/gql_{os.getpid()}.json"; open(tmp, "w").write(body)
        out = subprocess.run(["curl", "-sS", "-m", "120", f"https://{c['shop']}/admin/api/{API}/graphql.json",
                              "-H", "Content-Type: application/json", "-H", f"X-Shopify-Access-Token: {token()}", "-d", f"@{tmp}"],
                             capture_output=True, text=True).stdout
        try: d = json.loads(out)
        except Exception:
            # 2026-09-11: the sandbox egress proxy intermittently refuses CONNECT (403) for ~20 s — retry with backoff
            if attempt < retries - 1:
                wait = (10, 30, 60)[min(attempt, 2)]
                sys.stderr.write(f"shopify_api: non-JSON/empty response (proxy?) — retry in {wait}s\n"); time.sleep(wait); continue
            raise SystemExit(f"non-JSON response: {out[:300]}")
        if d.get("errors") and any("THROTTLED" in json.dumps(e) for e in d["errors"]):
            time.sleep(5); continue
        if d.get("errors") and any("nvalid API key" in json.dumps(e) or "401" in json.dumps(e) for e in d["errors"]):
            token(force=True); continue
        if d.get("errors"): raise SystemExit(f"GraphQL errors: {json.dumps(d['errors'])[:500]}")
        return d
    raise SystemExit("gql: retries exhausted")
PRODUCT_FIELDS = """id handle title descriptionHtml vendor productType tags status updatedAt category { id name fullName }
 seo { title description } variants(first: 100) { edges { node { id price title selectedOptions { name value } updatedAt } } }
 media(first: 50) { edges { node { id alt mediaContentType ... on MediaImage { image { url } } } } }
 collections(first: 30) { edges { node { id } } } metafield(namespace: "custom", key: "cta_benefits") { value }"""
def fetch_tag(tag):
    nodes, after = [], None
    while True:
        d = gql("query($q:String!,$after:String){ products(query:$q, first:50, after:$after){ edges{ node{ %s } } pageInfo{ hasNextPage endCursor } } }" % PRODUCT_FIELDS,
                {"q": f"tag:{tag}", "after": after})["data"]["products"]
        nodes += [e["node"] for e in d["edges"]]
        if not d["pageInfo"]["hasNextPage"]: return nodes
        after = d["pageInfo"]["endCursor"]
if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "fetch":
        nodes = fetch_tag(sys.argv[2]); json.dump({"data": {"products": {"edges": [{"node": n} for n in nodes]}}}, open(sys.argv[3], "w"))
        print(len(nodes), "products ->", sys.argv[3])
    elif cmd == "mutate":
        m = json.load(open(sys.argv[2])); d = gql(m["query"], m["variables"])
        errs = {k: v.get("userErrors") for k, v in d["data"].items() if isinstance(v, dict) and v.get("userErrors")}
        print(sys.argv[2], "clean" if not errs else errs)
    elif cmd == "shop":
        print(gql("{ shop { name } }"))
