#!/usr/bin/env python3
"""spec_parse.py — split this supplier's run-on Specifications line into extract.specs rows.

ddl2-batch28: 37 of 50 sources write the whole spec table as ONE sentence in a single <p>
("Material: Metal Lamp Shade Material: Metal Dimensions: 25 cm (W) x 13.5 cm (H) Wall Light
Type: Sconce ..."), so extract_html.py's list parser found nothing and spec_cover.py would
have had no source side to enforce.

Splitting on "any capitalised words + colon" does NOT work here: the VALUES are capitalised
too ("Material: Metal"), so a value's trailing words get swallowed into the next label. The
label boundary is therefore decided by a LEXICON — the 47 spec names the structured products
in this same batch produced, plus the label tails seen in the run-on lines — matched
longest-first at each colon. A colon whose preceding words are not in the lexicon is left
alone rather than guessed.

Only products whose extract.specs is EMPTY are touched; the source line stays in facts, so
value_check.py still sees it. --dry prints without writing.
"""
import json, glob, re, sys

LABELS = sorted({
    "Accessory", "Accessories", "Application", "Applications", "Available Colours",
    "Available Sizes", "Battery", "Battery Capacity", "Battery Properties", "Battery Type",
    "Base Diameter", "Body Material", "Bulb Base", "Bulb Type", "Cable Length", "Capacity",
    "Care", "Care Instructions", "Charging Port", "Charging Time", "Color", "Colors", "Colour",
    "Colours", "Colour Options", "Colour Temperature", "Colours Available",
    "Contains Light Source", "Control", "Control Method", "Control Type", "Cord Length",
    "Depth", "Design", "Diameter", "Diameter Options", "Dimensions", "Dimmable", "Environment",
    "Finish", "Finish Options", "Finish Type", "Finishes", "Fixture Type", "Fixture Width",
    "Frame Material", "Function", "Functions", "Glass Type", "Hardwired", "Height",
    "Indoor/Outdoor Use", "Installation", "IP Rating", "Is Dimmable", "Item Name",
    "Lamp Shade Material", "Large", "Length", "Light Colour", "Light Colour Options",
    "Light Direction", "Light Fixture Type", "Light Source", "Light Source Type", "Lighting",
    "Lighting Area", "Lighting Direction", "Lighting Style", "Location", "Lumens", "Material",
    "Materials", "Medium", "Mount Type", "Mounting", "Mounting Type", "Movement",
    "Movement Type", "Number of Light Sources", "Operating Voltage", "Package",
    "Package Includes", "Pattern", "Photovoltaic Module", "Plug Type", "Pot Diameter", "Power",
    "Power Mode", "Power Source", "Power Supply", "Product Name", "Recommended Room Size",
    "Room Size", "Runtime", "Shade Diameter", "Shade Height", "Shade Material", "Shade Shape",
    "Shape", "Size", "Sizes", "Sizes Available", "Small", "Socket Type", "Solar Panel",
    "Special Feature", "Special Features", "Style", "Suggested Room Size", "Suitable For",
    "Switch Location", "Theme", "Type", "Usage", "Use", "Uses", "Variants", "Voltage",
    "Voltage Range", "Acceptable Voltage Range", "Wall Distance", "Warranty",
    "Water Resistance Level", "Waterproof Rating", "Wattage", "Weight", "Width",
    "Working Time", "Wall Light Type", "Water Resistance", "Wall Mount", "Usage Scenario",
    "Sensor", "Display Type", "Base Type", "Surface", "UV Protection", "Brightness", "Fixture Height", "Installation Type", "Certification", "Certifications", "Bulb Included", "Lamp Base", "Assembly", "Assembly Required", "Net Weight", "Gross Weight", "Cable", "Switch", "Switch Type", "Timer", "Remote", "Remote Control", "Colour Rendering", "Beam Angle", "Lifespan", "LED Quantity", "Number of LEDs", "Solar Panel Power", "Charging Method", "Waterproof", "Water Resistance Rating", "Indoor / Outdoor", "Suitable Rooms", "Occasion", "Care Tips", "Bulb Wattage", "Max Wattage", "Shade Colour", "Base Material", "Glass Colour", "Print", "Pot Size", "Planter Size", "Drainage", "Tier", "Shelf Depth", "Load Capacity", "Hanging Length", "Chain Length", "Rod Length", "Thickness", "Clock Type", "Numerals", "Hands", "Battery Life", "Included", "What You Get", "Lampshade Material", "Applicable Space", "Quantity", "Lighting Method", "Color Options",
}, key=lambda s: (-len(s), s))

LABEL_RE = re.compile(r"(?<![A-Za-z])(" + "|".join(re.escape(x) for x in LABELS) + r")\s*:\s*")
HEAD = re.compile(r"^(specifications?|specs?|technical\s+(details|specifications?)|product\s+details)\s*:?$", re.I)


def rows_from(line):
    hits = [(m.start(), m.end(), m.group(1)) for m in LABEL_RE.finditer(line)]
    rows, seen = [], set()
    for i, (s, e, name) in enumerate(hits):
        end = hits[i + 1][0] if i + 1 < len(hits) else len(line)
        val = line[e:end].strip().strip(";,.")
        key = name.lower()
        if val and key not in seen:
            seen.add(key)
            rows.append({"name": name, "value": val})
    return rows


def main():
    dry = "--dry" in sys.argv
    tot_p = tot_r = 0
    missed = []
    for f in sorted(glob.glob("extract/p*.json")):
        n = f[-7:-5]
        e = json.load(open(f))
        if e.get("specs"):
            continue
        facts = e.get("facts") or []
        best = []
        for i, ln in enumerate(facts):
            if HEAD.match(ln.strip()):
                for cand in facts[i + 1:i + 3]:
                    r = rows_from(cand)
                    if len(r) > len(best):
                        best = r
                break
        if not best:
            for ln in facts:
                r = rows_from(ln)
                if len(r) >= 4 and len(r) > len(best):
                    best = r
        if best:
            e["specs"] = best
            if not dry:
                json.dump(e, open(f, "w"), indent=1, ensure_ascii=False)
            tot_p += 1; tot_r += len(best)
            bleed = [r['name'] for r in best if ':' in r['value']]
            print(f"{n} specs: {len(best)} rows" + (f"  [BLEED after {', '.join(bleed)}]" if bleed else ""))
        else:
            missed.append(n)
            print(f"{n} specs: [none found]")
    print(f"spec_parse: {tot_p} products filled, {tot_r} spec rows" +
          (f"; no spec line on {', '.join(missed)}" if missed else ""))


if __name__ == "__main__":
    main()
