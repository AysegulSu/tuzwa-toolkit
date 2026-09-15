#!/usr/bin/env python3
"""extract_html.py — mechanical part of extraction (no model tokens).
  python3 extract_html.py products.json          # -> raw/pNN.json + extract/pNN.json (skeleton) for every product
Fills from HTML/JSON: idx, id, handle, old_title, old_seo_*, productType, category, tags, status, specs, package,
how_to_use, faq_source, images, media, variants, facts (every text line of the description), foreign_images.
Leaves for the Sonnet extraction agent (EXTRACT-SPEC.md; never Haiku): identity, notes, candidates, safety_flags, season_hint.

"""
import json, re, sys, os, html
def txt(h): return html.unescape(re.sub(r"<[^>]+>", " ", h)).strip()
def clean(s): return re.sub(r"\s+", " ", s).strip()
def section(h, names):
    # returns inner html between a heading whose text matches names and the next <h2/h3>
    for m in re.finditer(r"<h[23][^>]*>(.*?)</h[23]>", h, re.I | re.S):
        if any(n in txt(m.group(1)).lower() for n in names):
            rest = h[m.end():]; nxt = re.search(r"<h[23][^>]*>", rest, re.I)
            return rest[:nxt.start()] if nxt else rest
    return ""
def items(block): return [clean(txt(li)) for li in re.findall(r"<li[^>]*>(.*?)</li>", block, re.S) if clean(txt(li))]
doc = json.load(open(sys.argv[1]))
nodes = [e["node"] for e in doc["data"]["products"]["edges"]] if "data" in doc else doc
os.makedirs("raw", exist_ok=True); os.makedirs("extract", exist_ok=True); os.makedirs("candidates", exist_ok=True)
cdn = sys.argv[2] if len(sys.argv) > 2 else "/s/files/1/0806/1645/6416/"
for i, n in enumerate(nodes):
    n["_idx"] = i; json.dump(n, open(f"raw/p{i:02d}.json", "w"), indent=1)
    h = n["descriptionHtml"] or ""
    specs = []
    for it in items(section(h, ["specification", "attribute", "details"])):
        m = re.match(r"([^:]{2,40}):\s*(.+)", it)
        if m: specs.append({"name": m.group(1).strip(), "value": m.group(2).strip()})
    imgs = [{"src": s, "alt": a, "position": k + 1} for k, (s, a) in enumerate(re.findall(r'<img[^>]+src="([^"]+)"[^>]*?(?:alt="([^"]*)")?', h))]
    faqs = [{"q": clean(txt(q)), "a": clean(txt(a))} for q, a in re.findall(r"<strong>\s*Q:(.*?)</strong>\s*(?:<br>|</p>\s*<p>)\s*A:(.*?)</p>", h, re.S)]
    facts = [clean(t) for t in re.split(r"</(?:p|li|h[1-6])>", h) if clean(txt(t))]
    facts = [clean(txt(t)) for t in facts if not re.match(r"\s*<img", t)]
    ex = {"idx": i, "id": n["id"], "handle": n.get("handle"), "old_title": n["title"], "old_seo_title": (n.get("seo") or {}).get("title"),
          "old_seo_description": (n.get("seo") or {}).get("description"), "productType": n.get("productType"), "category": n.get("category"),
          "tags": n.get("tags", []), "status": n.get("status"), "identity": "", "notes": "", "facts": facts, "specs": specs,
          "package": items(section(h, ["package", "in the box", "what's included"])),
          "how_to_use": items(section(h, ["how to use", "instructions", "usage"])), "faq_source": faqs, "images": imgs,
          "foreign_images": [im["src"] for im in imgs if cdn not in im["src"]],
          "media": [{"id": e["node"]["id"], "type": e["node"].get("mediaContentType"), "alt": e["node"].get("alt") or "",
                     "filename": ((e["node"].get("image") or {}).get("url") or "").split("/")[-1].split("?")[0]} for e in n["media"]["edges"]],
          "variants": [{"id": v["node"]["id"], "price": v["node"]["price"], "title": v["node"]["title"]} for v in n["variants"]["edges"]],
          "safety_flags": [], "season_hint": ""}
    json.dump(ex, open(f"extract/p{i:02d}.json", "w"), indent=1)
print(len(nodes), "products -> raw/ + extract/ skeletons;", sum(1 for i in range(len(nodes)) if json.load(open(f'extract/p{i:02d}.json'))['foreign_images']), "with foreign images")
