#!/usr/bin/env python3
"""novel_words.py NN [NN ...] — zero-cost invention scan (added 2026-09-04, user decision).
Lists every content word (≥4 letters) in the description that appears NOWHERE in the product's source
(extract facts/specs/package/how_to_use/faq_source/variants/old title), nor in the new title, nor in the
product's measured keywords (candidates/cNN.json), nor in the small store-voice allowlist below.
Output is a review list, not a verdict: a fact-bearing novel word (free, machine, printed, corners, sunset…)
is an invention; a connective or a synonym is fine. The writer clears or justifies each word before finishing."""
import json, re, sys, html
ALLOW = set("""about above across after again against almost along already also always among another anyone anything anywhere around
because become becomes been before behind being below beside between beyond both bring brings built call came cannot
choose comes could daily does done down during each either else enough even ever every everything exactly first from full
gets give gives goes going gone great half having here high home hour hours idea inside instead into itself just keep
keeps kept know large last later least less life light like little long look looks lower made make makes making many
matter maybe meet more most much must near need needs never next nothing often once only onto other others ours over
place plus quickly rather ready really right room same says seat sets shape should side simple simply since small some
something soon space stay stays still such sure take takes than that their them then there these they thing things
think this those though three through time today together took turn turns under until upon used uses using very want
wants ways well were what when where whether which while whole will with within without work works would wrap year years
your yours yourself shopper shoppers customer customers order orders store ship shipping delivery deliver buyer buyers
brings gets lets puts adds gives pairs pair helps keeps means minutes seconds moment morning night evening days week
everyday anytime anywhere everywhere wherever whenever whatever whichever look feel feels looking feeling reach reaches
handle handles handled fits fitting fit stays stay ready reach start starts stop stops step steps way ways one two four
five six seven eight nine ten dozens""".split())
def words(s): return re.findall(r'[a-z]{4,}', s.lower())
def stems(ws): return {w[:5] if len(w) > 5 else w for w in ws}
for n in sys.argv[1:]:
    n = int(n); d = json.load(open(f'final/d{n:02d}.json')); ex = json.load(open(f'extract/p{n:02d}.json'))
    src = ' '.join(ex['facts'] + [f"{s['name']} {s['value']}" for s in ex['specs']] + ex['package'] + ex['how_to_use']
                   + [f"{q['q']} {q['a']}" for q in ex['faq_source']] + [v['title'] for v in ex['variants']]
                   + [ex['old_title'], ex['old_seo_title'], ex['old_seo_description'], ex['productType'], ex['identity']])
    try: kws = ' '.join(json.load(open(f'candidates/c{n:02d}.json'))['candidates'])
    except Exception: kws = ''
    known = stems(words(src)) | stems(words(kws)) | stems(words(d['title'])) | stems(ALLOW)
    body = html.unescape(re.sub(r'<img[^>]+>', ' ', d['descriptionHtml'])); body = re.sub(r'<[^>]+>', ' ', body)
    novel = sorted({w for w in words(body) if (w[:5] if len(w) > 5 else w) not in known})
    print(f"{n:02d} novel words ({len(novel)}): {' '.join(novel)}")
