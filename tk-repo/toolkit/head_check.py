#!/usr/bin/env python3
"""head_check.py — title-format-rule.md §3 rule 2 head-noun test (added 2026-09-05, user decision).

The opener phrase must be built on the product's own head noun (the productType's last word after §10b) —
singular/plural or a listed synonym; attribute words may follow it inside the opener. Zero model tokens.

  python3 head_check.py titles_final.json          # [{"title":..., "productType":...}, ...] or {"id": {...}}
  python3 head_check.py products.json              # Shopify fetch format is also accepted

Prints one line per FAIL and a summary. Exit code 1 when any FAIL.
The synonym list mirrors the rule doc — extend it only with the user's approval, in both places.
"""
import json, re, sys

SYN = [
    {"cam", "camera"}, {"skillet", "pan"}, {"charger", "bank"}, {"cover", "slipcover"},
    {"couch", "sofa"}, {"torch", "flashlight"}, {"eater", "wacker", "trimmer", "whacker"},
    {"repeller", "repellent", "deterrent"}, {"beanie", "hat"}, {"sneaker", "shoe"},
    {"earbud", "earphone"}, {"purse", "handbag"}, {"pant", "trouser"}, {"adapter"},
    {"insert", "insole"}, {"holder", "mount"}, {"light", "lamp", "sconce"},
    {"scarf", "scarve"}, {"coat", "jacket", "overcoat", "raincoat"}, {"top", "blouse", "shirt"},
    {"jogger", "sweatpant"}, {"squeezer", "juicer"}, {"cane", "stick"}, {"binder", "belt"},
    {"stopper", "device"}, {"flusher", "sensor"}, {"compressor", "inflator"}, {"dispenser", "holder"},
    {"stand", "holder", "caddy"}, {"suit", "swimsuit"}, {"remover", "removal"}, {"tool", "puller", "weeder", "head"},
    {"wedge", "sandal"}, {"cover", "protector", "cap", "sleeve"}, {"shoe", "boot", "sneaker"}, {"band", "headband"},
    {"extension", "extender"}, {"scratcher", "pad"}, {"beanie", "beany"}, {"watering", "irrigation"},
]
GENERIC_TAIL = {"set", "kit", "system", "pack", "tool"}   # skipped when finding the productType head noun
STOP = {"for", "with", "in", "on", "and", "or", "to", "of", "the", "a"}


def sing(w):
    w = w.lower()
    if w.endswith("ies") and len(w) > 5 and w[-4] not in "aeiou": return w[:-3] + "y"   # batteries -> battery, beanies -> beanie
    if w.endswith(("sses", "xes", "shes", "ches")): return w[:-2]
    if w.endswith("s") and not w.endswith("ss"): return w[:-1]
    return w


def same(a, b):
    if a == b: return True
    return any(a in s and b in s for s in SYN)


def opener_words(title):
    """Words of the opener phrase (first comma segment, before any 'for/with' clause).
    Attribute words may follow the head noun inside the opener (`Shower Caddy No Drill`); the test is
    that the product's own noun is IN the opener phrase — `Cat Beds for Indoor Cats` has no 'hammock'."""
    seg = title.split(",")[0]
    seg = re.split(r"\b(for|with)\b", seg, 1, flags=re.I)[0]
    return [sing(w) for w in re.findall(r"[A-Za-z]+", seg) if w.lower() not in STOP]


def pt_head(pt):
    """Head noun of the productType: last word of the part before any 'for/with' clause
    (`Raincoat for Dogs` -> raincoat, `Cane with Seat` -> cane, `Toilet Brush and Plunger Set` -> set)."""
    seg = re.split(r"\b(for|with)\b", pt, 1, flags=re.I)[0]
    words = [w for w in re.findall(r"[A-Za-z]+", seg) if w.lower() not in STOP]
    while len(words) > 1 and words[-1].lower() in GENERIC_TAIL: words.pop()
    return sing(words[-1]) if words else ""


def load(path):
    d = json.load(open(path))
    if isinstance(d, dict) and "data" in d:
        d = [e["node"] for e in d["data"]["products"]["edges"]]
    if isinstance(d, dict):
        d = list(d.values())
    return d


def main():
    items = load(sys.argv[1]); fails = 0
    for it in items:
        t = it.get("title") or ""; pt = it.get("productType") or it.get("product_type") or ""
        if not t or not pt: continue
        ow = opener_words(t); p = pt_head(pt)
        if not any(same(w, p) for w in ow):
            fails += 1
            print(f"FAIL  opener '{t.split(',')[0]}' lacks productType head '{p}' | {pt}")
    print(f"head-check: {fails} FAIL of {len(items)}")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
