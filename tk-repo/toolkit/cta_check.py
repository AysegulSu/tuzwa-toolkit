#!/usr/bin/env python3
"""cta_check.py NN [NN ...] — CTA benefit LANGUAGE gate (added 2026-09-04, blr-batch21).

The format check in gate.py only proves a line is `icon|text` under 34 chars. It never proved the
line is a benefit rather than a spec, so spec lines reached the store batch after batch
("Adjustable brightness", "Sizes S-XXXL", "40 bands included"). This script is that missing gate.
Zero model tokens. Rule source: rules/cta-benefits-metafield.md, section BENEFIT DILI.

2026-09-06 (blr-batch26, user decision after checking p45/p47 live): two gaps closed. (1) The DESC-SPEC limit "<=30 chars
text" was written in the document only — nothing measured it, and 11 live lines were 31-33 characters; a line over 30 is
now a FAIL. (2) Counts written as WORDS ("Seven colors, one remote", "Six modes for every need") and included-accessory
lines ("with remote", "4 nozzles included") passed the digit-only count pattern; word numbers and the accessory family
now FAIL like digits do. Both are the same rule the doc already states: a line names a problem that is gone, never a
count or a feature.
"""
MAX_TEXT = 30
NUM = r'(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|dual|triple)'
COUNT_NOUN = (r'(?:colors?|colours?|shades?|shapes?|sizes?|pcs?|pieces?|pack|bands?|compartments?|cubes?|slots?|scents?|'
              r'options?|modes?|settings?|functions?|pockets?|heads?|levels?|speeds?|filters?|trays?|clips?|nozzles?|tips?|'
              r'brush(?:es)?|attachments?|remotes?|finishes|tones?|styles?|patterns?|designs?)')
import json
import re
import sys

# (pattern, why it fails) — each targets a category the rule forbids outright.
BAD = [
    (r'\bsizes?\s+[a-z0-9]', 'size variant info'),
    (r'\b(?:xs|s|m|l|xl|xxl|xxxl)\s*(?:-|to|through)\s*(?:xs|s|m|l|xl|xxl|xxxl)\b', 'size range'),
    # NOTE: a bare numeric range is NOT banned — the rule explicitly allows numeric proof attached
    # to a result ("Up to 4 hours cordless", "2-7 days per charge"). Only counts and units below.
    (r'\b(?:black|white|red|blue|green|grey|gray|pink|gold|silver|bronze|beige|brown|yellow|orange|purple)\b'
     r'(?:\s*(?:,|/|or|and)\s*\w+)*', 'colour variant info'),
    (r'\b' + NUM + r'\s+(?:\w+\s+){0,2}' + COUNT_NOUN + r'\b', 'pack / count spec (digits or words)'),
    (r'\b(?:with|includes?|included|plus|comes with)\b[^,]*\b(?:remote(?: control)?|nozzles?|brush heads?|heads|case|cable|charger|'
     r'adapter|manual|strap|hook|stand|holder)\b|\b(?:one|a)\s+remote\b', 'included accessory, not a benefit'),
    (r'\b\d+\s*(?:mah|wh|w|v|db|hz|khz|ghz|mm|cm|m|in|ft|oz|lb|kg|g|ml|l|mp|p|k|met(?:re|er)s?|'
     r'inch(?:es)?|feet|pounds?|grams?|litres?|liters?)\b', 'raw unit spec'),
    # A line that is ONLY attributes chained together ("Cordless, battery powered"). Both sides must
    # be attributes — "Cordless, goes anywhere" is a real benefit and must not trip this.
    (r'^\s*(?:cordless|battery[- ]powered|usb[- ]powered|wireless|rechargeable|portable|reusable|'
     r'waterproof|water[- ]resistant|foldable|washable|non[- ]?slip|breathable|lightweight|'
     r'compact|durable|adjustable)\b\s*(?:[,/]|and)\s*'
     r'(?:cordless|battery[- ]powered|battery|usb[- ]powered|wireless|rechargeable|portable|reusable|'
     r'waterproof|water[- ]resistant|foldable|washable|non[- ]?slip|breathable|lightweight|'
     r'compact|durable|adjustable)\b\s*\w*\s*$', 'bare attribute list, not a benefit'),
    (r'\b\d+\s*x\s*(?:-|to)\s*\d+\s*x\b|\bmagnification\b', 'magnification / range spec'),
    (r'\bip[x]?\d+\b', 'ingress rating spec'),
    (r'\bbluetooth\s*\d', 'protocol version spec'),
    (r'\badjustable\b(?!\s+(?:up|to)\b.*\byou\b)', 'feature description, not a result'),
    (r'\b(?:waterproof|water[- ]resistant|rechargeable|reusable|portable|foldable|washable|'
     r'dishwasher safe|non[- ]?slip|breathable|lightweight)\b\s*$', 'bare attribute, no benefit'),
    (r'\b(?:made of|material|built from)\b', 'material spec'),
    (r'^\s*(?:not a medical device|multi[- ]use|multi[- ]purpose)\b', 'category label / disclaimer'),
]
ICON_HINT = [
    (r'\b(?:cordless|battery|charge|charged|recharge|power cut|runs on)\b', 'battery'),
    (r'\b(?:timer|schedule[ds]?|daily alarms?|reminder)\b', 'clock'),
    (r'\b(?:wifi|wi-fi|from your phone|alerts to your phone)\b', 'wifi'),
    (r'\b(?:video|night vision|music|languages?)\b', 'media'),
]

fails = warns = 0
for n in sys.argv[1:]:
    n = int(n)
    d = json.load(open('final/d%02d.json' % n))
    for line in d.get('cta_benefits', []):
        icon, _, text = line.partition('|')
        t = text.strip()
        low = t.lower()
        if len(t) > MAX_TEXT:
            print('[FAIL] %02d cta "%s" — %d chars, limit %d (DESC-SPEC <=30)' % (n, t, len(t), MAX_TEXT))
            fails += 1
            continue
        for pat, why in BAD:
            if re.search(pat, low):
                print('[FAIL] %02d cta "%s" — %s' % (n, t, why))
                fails += 1
                break
        else:
            if icon == 'check':
                for pat, want in ICON_HINT:
                    if re.search(pat, low):
                        print('[WARN] %02d cta "%s" — icon could be %s, not check' % (n, t, want))
                        warns += 1
                        break
print('cta-check: %d FAIL, %d WARN' % (fails, warns))
sys.exit(1 if fails else 0)
