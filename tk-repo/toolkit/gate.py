#!/usr/bin/env python3
"""gate.py NN [NN ...] — run every pre-push gate on final/dNN.json files.
Exit 1 when ANY section reports a problem (own [FAIL] lines, title-check FAIL, desc-check hits, struct-check issues,
spec-cover / value-check / assume-check / cta-check FAIL; age-check is WARN-only and never sets the exit code); exit 0 only when every section is clean. Fixed 2026-09-06 — before that the
exit code was always 0 regardless of output, so "exit 0" never meant "clean". The printed lines remain the detail."""
bad=0
import json,sys,subprocess,re,os
ids=sys.argv[1:]
P={"_config":{"cdn_prefix":"cdn.shopify.com/s/files/1/0806/1645/6416/"}}
chk=json.load(open('check_products.json'))
docs=[]
# comparison block (rules/comparison-table-rule.md, user decision 2026-09-06): compare_build.py renders the "Tuzwa vs
# Others" table from the doc's `compare` object into descriptionHtml (idempotent) BEFORE the other checks read the file,
# so every gate below runs on the final HTML. Its own checks (5 source-traceable rows, one neutral Others cell …) count.
print('--- compare-build (comparison block rendered + checked) ---'); r0=subprocess.run(['python3','compare_build.py']+ids,capture_output=True,text=True); print(r0.stdout.strip()); bad+=r0.returncode!=0
import compare_build, fit_build
# fit block (rules/fit-block-rule.md, Q19, 2026-09-06): one column "Right for you if", rendered before the FAQs, same contract.
print('--- fit-build (who-it-is-for block rendered + checked) ---'); r0b=subprocess.run(['python3','fit_build.py']+ids,capture_output=True,text=True); print(r0b.stdout.strip()); bad+=r0b.returncode!=0
print('--- list-bold (Key Features / Specifications lead-ins bolded, gap under image 2; script, idempotent — 2026-09-11) ---'); rlb=subprocess.run(['python3','list_bold.py']+ids,capture_output=True,text=True); print(rlb.stdout.strip())
for n in ids:
    n=int(n); d=json.load(open(f'final/d{n:02d}.json')); ex=json.load(open(f'extract/p{n:02d}.json'))
    key=[k for k in chk if k.startswith(f"{n:02d}_")][0]
    e=dict(chk[key]); e['title']=d['title']; e['seo_title']=d['seo']['title']; e['seo_desc']=d['seo']['description']; e['description']=d['descriptionHtml']
    P[key]=e
    # description-format-rule.md 2026-09-05: a description with 0 or 1 source image gets gallery
    # image(s) added so the total is never below 2; expected count reflects that floor.
    exp_src=len(ex['images']); exp_total=exp_src if exp_src>=2 else 2
    d['_expected_images']=exp_total; docs.append(d)
    # image tags: the ORIGINAL source images must be unchanged and in their original order (prefix
    # match); anything appended beyond that is an allowed gallery addition, already CDN-hosted.
    # The Q18 dimension image (rules/dimension-image-rule.md, 2026-09-09) is inserted by dim_attach.py AFTER the push as
    # `<img class="vp-dim" …>` under the Specifications list; it is not a source image and is left out of this count.
    src_old=[im['src'] for im in ex['images']]; src_new=re.findall(r'<img[^>]+src="([^"]+)"',re.sub(r'<img class="vp-dim"[^>]*>','',d['descriptionHtml']))
    if src_new[:len(src_old)]!=src_old or len(src_new)!=exp_total: print(f"[FAIL] {n:02d} image src list changed / reordered"); bad+=1
    # facts coverage: every spec value string should appear (numbers)
    txt=re.sub(r'<[^>]+>',' ',d['descriptionHtml']).lower()
    miss=[s for s in ex['specs'] if re.sub(r'\s+',' ',str(s['value']).lower())[:25] not in re.sub(r'\s+',' ',txt) and not any(w in txt for w in re.findall(r'\d+(?:\.\d+)?',str(s['value']))[:1])]
    if miss: print(f"[WARN] {n:02d} spec values possibly missing: {[m['name'] for m in miss][:6]}")
    cta=d.get('cta_benefits',[])
    if len(cta)!=3 or any('|' not in c or len(c.split('|')[1])>30 for c in cta): print(f"[FAIL] {n:02d} cta_benefits must be 3 x 'icon|text<=30ch': {cta}"); bad+=1
    for a in d.get('media_alts',[]):
        if len(a['alt'])>125 or not a['alt']: print(f"[FAIL] {n:02d} media alt empty/over 125"); bad+=1
    alts=[a['alt'] for a in d.get('media_alts',[])]+re.findall(r'alt="([^"]*)"',d['descriptionHtml'])
    if len(alts)!=len(set(alts)): print(f"[FAIL] {n:02d} duplicate alt text within product"); bad+=1
    if not d.get('productType') or not d.get('season') in ('winter','spring','summer','fall','evergreen') or not d.get('collections'): print(f"[FAIL] {n:02d} productType/season/collections missing"); bad+=1
    # brand name: forbidden in every copy EXCEPT inside the comparison block, where the template writes it on purpose
    # (rules/comparison-table-rule.md) — the block is removed before this scan.
    txt_nb=re.sub(r'<[^>]+>',' ',fit_build.strip_block(compare_build.strip_block(d['descriptionHtml']))).lower()
    if 'tuzwa' in txt_nb or 'tuzwa' in d['title'].lower(): print(f"[FAIL] {n:02d} brand name in copy (outside the comparison block)"); bad+=1
    # description-format-rule.md hard rule "Delete any link, brand name, or price found in the source description"
    # (added to the gate 2026-09-06, user instruction): no <a> tag, no URL / e-mail, no price in any customer-facing field.
    # <img src> URLs are the only URLs allowed, so they are removed before the scan. Brand names other than our own cannot
    # be detected by a generic script and remain a RULINGS / review matter.
    body_nolinks=re.sub(r'<img[^>]*>',' ',d['descriptionHtml'])
    if re.search(r'<a\b|</a>',body_nolinks,re.I): print(f"[FAIL] {n:02d} <a> link tag in description"); bad+=1
    for fname,fval in (('descriptionHtml',re.sub(r'<[^>]+>',' ',body_nolinks)),('title',d['title']),('seo.title',d['seo']['title']),('seo.description',d['seo']['description'])):
        m=re.search(r'https?://|www\.|mailto:|\b[\w.-]+@[\w-]+\.[a-z]{2,}\b',fval,re.I)
        if m: print(f"[FAIL] {n:02d} URL / e-mail in {fname}: {m.group(0)}"); bad+=1
        m=re.search(r'[$€£₺]\s?\d|\d\s?(?:USD|EUR|GBP|TRY|TL)\b|\b\d+(?:[.,]\d+)?\s?(?:dollars|euros|pounds)\b',fval,re.I)
        if m: print(f"[FAIL] {n:02d} price in {fname}: {m.group(0)}"); bad+=1
        # Supplier policy promises are never product facts (user rule 2026-09-07, DENEME batch): warranty, guarantee,
        # money-back / refund / risk-free trial, return policy, customer-support promises. FAIL wherever they appear —
        # prose, lists, comparison block, fit block, FAQ, CTA lines, SEO. No add_per_ruling exemption exists for this family.
        m=re.search(r'\b(?:warrant(?:y|ies|ed)|guarantee[ds]?|money[- ]back|refund(?:s|ed|able)?|risk[- ]free|free trial|return polic(?:y|ies)|(?:24/7|responsive|customer|dedicated) support|after[- ]sales)\b',fval,re.I)
        if m: print(f"[FAIL] {n:02d} supplier policy promise in {fname}: {m.group(0)}"); bad+=1
    for c in d.get('cta_benefits',[]):
        m=re.search(r'\b(?:warrant(?:y|ies|ed)|guarantee[ds]?|money[- ]back|refund(?:s|ed|able)?|risk[- ]free|free trial)\b',c,re.I)
        if m: print(f"[FAIL] {n:02d} supplier policy promise in CTA line: {m.group(0)}"); bad+=1
json.dump(P,open(f'/tmp/chk_{os.getpid()}.json','w')); json.dump(docs,open(f'/tmp/docs_{os.getpid()}.json','w'))
print('--- title-check (rule 1 / second net) ---')
r=subprocess.run(['python3','title-check.py','kw.txt',f'/tmp/chk_{os.getpid()}.json'],capture_output=True,text=True)
print('\n'.join(l for l in r.stdout.splitlines() if 'rule 1' in l or 'second net' in l or 'seo.' in l or 'foreign' in l or l.startswith('[FAIL]') or l.startswith('summary')))
bad+=sum(1 for l in r.stdout.splitlines() if l.startswith('[FAIL]'))
print('--- desc-check ---'); r2=subprocess.run(['python3','desc-check.py','--fields',f'/tmp/docs_{os.getpid()}.json'],capture_output=True,text=True); print(r2.stdout.strip()); bad+=r2.returncode!=0
print('--- struct-check ---'); r3=subprocess.run(['python3','struct-check.py',f'/tmp/docs_{os.getpid()}.json'],capture_output=True,text=True); print(r3.stdout.strip()); bad+=r3.returncode!=0

print('--- spec-cover (every source spec line in the Specifications list) ---'); r7=subprocess.run(['python3','spec_cover.py']+ids,capture_output=True,text=True); print(r7.stdout.strip()); bad+=r7.returncode!=0
print('--- unit-dual (second unit system appended in Specifications; script, idempotent) ---'); rud=subprocess.run(['python3','unit_dual.py']+ids,capture_output=True,text=True); print(rud.stdout.strip().splitlines()[-1])
print('--- keyfeat-cover (every source Key Features line is an item of the new Key Features list) ---'); rkf=subprocess.run(['python3','keyfeat_cover.py']+ids,capture_output=True,text=True); print(rkf.stdout.strip()); bad+=rkf.returncode!=0
print('--- value-check (no source value dropped) ---'); r6=subprocess.run(['python3','value_check.py']+ids,capture_output=True,text=True); print(r6.stdout.strip()); bad+=r6.returncode!=0
# assume-check (2026-09-06, user decision): DESC-SPEC "ADD NOTHING BEYOND THE SOURCE" — a forbidden-family claim the
# extract never states FAILs. age-check (same day): single-age phrase without its range — WARN only, review aid.
print('--- assume-check (no claim the source never made) ---'); r9=subprocess.run(['python3','assume_check.py']+ids,capture_output=True,text=True); print(r9.stdout.strip()); bad+=r9.returncode!=0
print('--- age-check (state the range, never one end — WARN only) ---'); r10=subprocess.run(['python3','age_check.py']+ids,capture_output=True,text=True); print(r10.stdout.strip())
# cta-check: CTA line LANGUAGE (benefit, not spec) per rules/cta-benefits-metafield.md. Added to gate.py in blr-batch21
# (2026-09-04); the 2026-09-05 image-floor rewrite of this file dropped the call — restored 2026-09-06 (user instruction).
print('--- cta-check (CTA lines are benefits, not specs) ---'); r8=subprocess.run(['python3','cta_check.py']+ids,capture_output=True,text=True); print(r8.stdout.strip()); bad+=r8.returncode!=0
print('--- howto-check (How to Use: real steps only, every step kept, never pasted; 2026-09-07) ---'); r11=subprocess.run(['python3','howto_check.py']+ids,capture_output=True,text=True); print(r11.stdout.strip()); bad+=r11.returncode!=0
print('--- usage-tips (source Usage Tips block -> own <h3>Usage Tips</h3> list, every line, never pasted; 2026-09-07) ---'); r12=subprocess.run(['python3','usage_tips.py']+ids,capture_output=True,text=True); print(r12.stdout.strip()); bad+=r12.returncode!=0
# sections (2026-09-08, user decision, rules/description-format-rule.md §7c): every other fact-carrying source section
# (Care Instructions, Safety Warnings, Materials, …) is its own <h3> section on the page — canonical heading, every line in
# the writer's own sentence, no copy, no merge, no invented section, after Package Includes / How to Use / Usage Tips, before
# the fit block / FAQs. Marketing-only blocks stay prose (extract.sections_dismissed).
print('--- sections (every other fact-carrying source section -> own <h3> section, canonical heading, every line, never pasted; 2026-09-08) ---'); r13=subprocess.run(['python3','sections.py']+ids,capture_output=True,text=True); print(r13.stdout.strip()); bad+=r13.returncode!=0
print(f'=== gate: {"CLEAN" if not bad else str(bad)+" problem section(s)/lines"} ===')
sys.exit(1 if bad else 0)
