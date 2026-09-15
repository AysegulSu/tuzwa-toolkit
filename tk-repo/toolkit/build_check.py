import json,glob,re
T=json.load(open('titles_draft.json'))
# §10b productType per product (the title agent's decision, Title Case singular) — title-check.py needs it for the §3 rule 2
# hard checks. Missing index -> the extract's old productType is used, which is usually the parent category: fill PT.
PT=json.load(open('producttype_draft.json')) if glob.glob('producttype_draft.json') else {}
KW={}
for ln in open('kw.txt'):
    k,v,c,p=ln.rstrip('\n').split('|'); KW[k]=int(v)
# fit-reject patterns per product (regex, applied to candidate keywords). Reasons in RULINGS/run log.
FR={
0:[r'beard|tweezer|clipper|razor|shaver|women$|for women|bikini|body|mens grooming|best |kit'],
1:[r'chair|bar stool|step stool|stadium|cane|shooting|seat$|ladder|bench|walker'],
2:[r'lint|vacuum|brush|glove|rake|roller|comb|deshedding|sweeper'],
3:[r'sofa bedding|sofa bed|stretch|sectional|loveseat|futon|recliner|waterproof|slipcover|cushion cover|blanket|bedding'],
4:[r'box fan|portable|neck|tower|handheld|floor|bladeless|battery|clip|computer|ceiling|bedroom fan|mini fan|cooling fan|air'],
5:[r'clipper|nail grinder|scissor|brush|shaver|grooming tools|grooming kit|dog grooming|best |professional|horse|human'],
6:[r'sata cable|enclosure|nvme|docking|dock$|m\.2|ssd|data recovery|recovery software|cable$'],
7:[r'^pop up tent|^pop up tents|camping tent|beach umbrella|canopy|2 person|dog beach|kiddie pool$|playpen|umbrella'],
8:[r'dog|cat|pet|nail file|glass|electric|senior|elderly|manicure set|pedicure|ingrown|clippers set|baby'],
9:[r'grater|cheese|spiralizer|mandolin|chopper|cutter$|apple|kitchen gadgets|kitchen tools|slicer'],
10:[r'flat feet|arch|heel|orthotic|memory foam|gel|running|plantar|podiatr|custom|superfeet|dr scholl'],
11:[r'duct|teflon|plumb|electrical tape|flex|butyl|silicone|insulat|gorilla|rubber|heat resistant|kapton|foil|gaffer|masking|double sided'],
12:[r'rear|helmet|reflector|tail|mtb|mountain|strobe|car|head lamp|headlamp|flashlight'],
13:[r'water shoes|rain boots|waterproof shoes|galoshes|disposable|booties|rain gear|boot covers|rain shoes|socks|gaiters'],
14:[r'sleep sack|kids|down|liner|bivy|pad|camping gear|backpacking gear|cot|hammock|quilt|adults|2 person|double'],
15:[r'string|pathway|path light|lantern|motion|security|flood|spotlight|landscape|outdoor lights$|outdoor lighting|patio lights|deck|step light|post light|string lights|wall light'],
16:[r'grater|zester|mandolin|chopper|spiralizer|potato|apple|kitchen utensils|kitchen gadgets|kitchen tools|cheese|slicer'],
17:[r'grater|chopper|fry cutter|spiralizer|salad|mandolin|onion|cabbage|potato|cheese|kitchen utensils|kitchen gadgets|kitchen tools|slicer$'],
18:[r'duvet|comforter|bedding|mattress|cooling|flannel|microfiber|cotton|bamboo|linen|deep pocket|queen|king|twin|full|set$|sets$'],
19:[r'duvet|comforter|bedding|mattress|cooling|flannel|microfiber|cotton|bamboo|linen|sateen|percale'],
20:[r'toilet seat$|bidet toilet seat|portable|travel|sprayer|electric bidet|handheld|best |toilet$|heated|smart'],
21:[r'beard|clipper|shaver|razor|dermaplan|bikini|body|mens grooming|kit|women|remover'],
22:[r'^gloves$|mitten|heated|ski gloves|skiing gloves|work gloves|neoprene|leather|waterproof|cycling gloves|golf|latex|snow gloves|mens gloves|womens gloves'],
23:[r'air mattress|yoga|sleeping bag|cot|self inflating|foam|hammock|cushion'],
24:[r'pop up|2 person|4 season|bivy|camping gear|backpacking gear|tent$|tents$|beach|canopy|family|instant'],
25:[r'bark box|whistle|collar|shock|training aid|treat|handheld'],
26:[r'trap|house|removal|netting|exclusion|how to|bait|poison|spray|exterminator'],
27:[r'treatment|control|bites|pest control|spray|mattress|trap|earth|interceptor|killer|steamer|prevention|how to|get rid|heater|powder|cover'],
28:[r'scarecrow|netting|spikes|decoy|owl|how to|control$|feeder|bird bath|spray|gel'],
29:[r'peppermint|trap|bait|poison|how to|spray|mothball|chipmunk|mole'],
30:[r'skunk|raccoon|spray|sprinkler|plants|deer|dog|how to|trap|granule|collar'],
31:[r'skunk|raccoon|trap|how to|get rid|control|feeder|deer|gopher|vole|mouse|granule|spray'],
32:[r'retainer|denture|polishing|coin|solution|best |gold|steam|dental|parts|gun|carburetor|professional|large'],
33:[r'retainer|denture|silver|solution|best |gold|steam|dental|parts|gun|carburetor|professional|large|coin'],
34:[r'bark box|whistle|collar|clicker|shock|spray|treat|leash|rechargeable|cat'],
35:[r'treats|whistle|collar|clicker|leash|shock|repellent|repeller|cat|vibration|corrector|stray|spray'],
36:[r'trap|poison|peppermint|bait|for cars|car|how to|do ultrasonic|spray|insect|bug|plug in|plug-in|sound$|outdoor'],
37:[r'trap|swatter|zapper|catcher|sticky|spray|how to|get rid|fan|for dogs|fruit fly|mouse|mice|paper|ribbon|light$'],
38:[r'trap|poison|peppermint|bait|for car|how to|spray|sound$|do ultrasonic|insect|bug|outdoor|car'],
39:[r'killer|bait|trap|zapper|how to|do ultrasonic|pest control|spray|bed bug|safe for pets|rat repellent$|mouse repellent$'],
40:[r'parts|coin|solution|silver|gold|steam|best |professional|dental|gun|carburetor|large|glasses cleaner$'],
41:[r'zapper|trap|killer|plug in night light|nursery night light|outdoor|thermacell|spray|candle|coil'],
42:[r'trap|poison|peppermint|bait|how to|spray|do ultrasonic|outdoor|car|sound$'],
43:[r'trap|poison|peppermint|bait|how to|spray|do ultrasonic|outdoor|car|sound$|humane|roach|flea|fly'],
44:[r'trap|bait|control|pest control|how to|rabbit|raccoon|squirrel|chipmunk|best |granule|spray|poison|castor'],
45:[r'natural|thermacell|for yard|deet|tick|for dogs|spray|patio|flea|candle|coil|lantern|zapper|bracelet|wristband|sticker'],
46:[r'natural|deet|for dogs|spray|sticker|patch|citronella|candle|zapper|clip|thermacell|lotion'],
47:[r'tablets|cleanser|invisalign|night guard|jewelry|glasses|solution|brush|bath|best '],
48:[r'trap|deer|skunk|raccoon|cat|squirrel|fence|how to|best |spray|granule|dog|bird'],
49:[r'trap|poison|bait|how to|pest control|peppermint|spray|mouse|mice|bat|outdoor|car'],
}
EXTRA={26:["mouse repellent","mice repellent"]}
P={"_config":{"cdn_prefix":"cdn.shopify.com/s/files/1/0806/1645/6416/"}}
# old titles from the Phase 1 snapshot, by product id — title-check.py's old-vs-new volume gate (2026-09-06) needs them
OLD={}
if glob.glob('products.json'):
    _s=json.load(open('products.json')); _e=_s["data"]["products"]["edges"] if "data" in _s else _s
    OLD={(x["node"] if "node" in x else x)["id"]:(x["node"] if "node" in x else x)["title"] for x in _e}
# one-line reasons for measured keywords deliberately left out of a title (title-check.py unused-keyword gate, 2026-09-06):
# skip_reasons.json = {"NN": {"keyword": "reason"}} written by the title agent; a reason for a longer/shorter form of the phrase counts
SR=json.load(open('skip_reasons.json')) if glob.glob('skip_reasons.json') else {}
allrej={}
for f in sorted(glob.glob('candidates/c*.json')):
    d=json.load(open(f)); i=d['idx']
    ex=json.load(open(f'extract/p{i:02d}.json'))
    cl=sorted(set(k.strip().lower() for k in d["candidates"])|set(EXTRA.get(i,[])))
    pats=[re.compile(p) for p in FR.get(i,[])]
    rej=[k for k in cl if any(p.search(k) for p in pats)]
    pid=ex['id'].split('/')[-1]
    P[f"{i:02d}_{pid}"]={"title":T[str(i)],"productType":PT.get(str(i)) or ex.get("productType") or "","cluster":cl,"fit_reject":rej,
                         "product_id":ex['id'],"old_title":OLD.get(ex['id']) or ex.get("title") or ex.get("old_title"),
                         "skip_reasons":SR.get(str(i)) or SR.get(f"{i:02d}") or {}}
    allrej[i]=sorted(((KW.get(k,0),k) for k in rej),reverse=True)
json.dump(P,open('check_products.json','w'),indent=1)
json.dump(allrej,open('fit_rejects.json','w'),indent=1)
big=[(i,v,k) for i,r in allrej.items() for v,k in r if v>=20000]
print(len(big),'fit rejects >=20k')
