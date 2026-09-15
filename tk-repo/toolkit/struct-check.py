#!/usr/bin/env python3
"""struct-check.py final/dNN.json ... — structure/length/limits/image gate per description-format-rule.md"""
import json,re,sys,html
CDN='cdn.shopify.com/s/files/1/0806/1645/6416/'
try:
    from compare_build import q17; Q17=q17()
except Exception: Q17=False
try:
    from fit_build import q19, CLOSE as FIT_CLOSE; Q19=q19()
except Exception: Q19=False; FIT_CLOSE='If two or more of these sound like you, this is the one.'
def txt(h): return html.unescape(re.sub(r'<[^>]+>',' ',h)).split()
bad=0
for path in sys.argv[1:]:
    d=json.load(open(path));
    for p in (d if isinstance(d,list) else [d]):
        e=[]; h=p['descriptionHtml']; pid=p['product_id'].split('/')[-1]
        if h.count('<h2')!=1: e.append(f'h2 count {h.count("<h2")}')
        h3=re.findall(r'<h3[^>]*>(.*?)</h3>',h)
        for need in ('Key Features','Specifications','Package Includes:','FAQs'):
            if need not in h3: e.append(f'missing h3 {need}')
        if 'PACKAGE INCLUDES' in h: e.append('caps package heading')
        m=re.search(r'<h2[^>]*>(.*?)</h2>\s*<ul[^>]*>(.*?)</ul>',h,re.S)
        if not m: e.append('no bullet list after h2')
        else:
            nb=m.group(2).count('<li');
            if nb!=5: e.append(f'benefit bullets {nb}')
            h2w=len(txt(m.group(1)))
            if not 12<=h2w<=14: e.append(f'h2 words {h2w}')
            for li in re.findall(r'<li[^>]*>(.*?)</li>',m.group(2),re.S):
                lead=re.search(r'<strong>(.*?)</strong>',li)
                if not lead: e.append('bullet without bold lead-in'); continue
                lt=html.unescape(lead.group(1)).rstrip(':').strip()
                ws=lt.split()
                if len(ws)>1 and sum(1 for w in ws[1:] if w[:1].isupper() and not w.isupper() and len(w)>1 and w not in ('USB','LED','UV'))>=len(ws[1:]) and len(ws)>=3: e.append(f'title-case lead-in: {lt}')
                if re.search(r'\d',lt): e.append(f'digit in lead-in: {lt}')
        # How to Use = real steps only (2026-09-07, user decision): an item opening with an audience/occasion pattern is not a step
        mh=re.search(r'<h3[^>]*>\s*How to Use\s*</h3>(.*?)(<h3|<div class="vp-|$)',h,re.S)
        if mh:
            for li in re.findall(r'<li[^>]*>(.*?)</li>|<p[^>]*>(.*?)</p>',mh.group(1),re.S):
                t=html.unescape(re.sub(r'<[^>]+>','',li[0] or li[1])).strip()
                if re.match(r'^(perfect|ideal|great|suitable|recommended|best (?:used|for|suited)|designed for|good for|essential for|use for)\b',t,re.I): e.append(f'How to Use item is an audience/occasion line, not a step: {t[:50]}')
        if '<h3>Usage Tips</h3>' in h:
            pos=h.find('<h3>Usage Tips</h3>'); pk=h.find('<h3>Package Includes:</h3>'); fq=h.find('<h3>FAQs</h3>'); fit=h.find('<div class="vp-fit"')
            if pk!=-1 and pos<pk: e.append('Usage Tips before Package Includes')
            if (fit!=-1 and pos>fit) or (fq!=-1 and pos>fq): e.append('Usage Tips after the fit block / FAQs')
        # Additional source sections (2026-09-08, user decision; rules/description-format-rule.md §7c): any <h3> that is not a
        # skeleton heading sits after Package Includes (and after How to Use / Usage Tips) and before the fit block / FAQs.
        # Whether the section is allowed at all (source has it, canonical heading, every line, no copy) is sections.py's job.
        for mm in re.finditer(r'<h3[^>]*>(.*?)</h3>',h):
            hd=html.unescape(re.sub(r'<[^>]+>','',mm.group(1))).strip()
            if hd in ('Key Features','Specifications','Package Includes:','How to Use','Usage Tips','FAQs'): continue
            pos=mm.start(); pk=h.find('<h3>Package Includes:</h3>'); fq=h.find('<h3>FAQs</h3>'); fit=h.find('<div class="vp-fit"')
            ht=h.find('<h3>How to Use</h3>'); ut=h.find('<h3>Usage Tips</h3>')
            if pk!=-1 and pos<pk: e.append(f'section {hd} before Package Includes')
            if (ht!=-1 and pos<ht) or (ut!=-1 and pos<ut): e.append(f'section {hd} before How to Use / Usage Tips')
            if (fit!=-1 and pos>fit) or (fq!=-1 and pos>fq): e.append(f'section {hd} after the fit block / FAQs')
        pre=h[:h.find('<h3')] if '<h3' in h else h
        prose=re.findall(r'<p[^>]*>(.*?)</p>',pre,re.S)
        pw=sum(len(txt(x)) for x in prose)
        # Prose: no cap on paragraphs or words (user instruction 2026-09-05) — the source meaning decides; padding is a
        # review matter, not a script matter. Too-thin prose still fails; above the 110-word norm is a warning.
        if pw<65: e.append(f'prose words {pw}')
        elif pw>110: print(pid, '|', p.get('title','')[:40], f'| WARN prose words {pw} > 110, {len(prose)} paragraphs — only source meaning justifies this, never padding')
        # comparison block (rules/comparison-table-rule.md, 2026-09-06): exactly one, directly before <h3>Key Features</h3>;
        # its words are NOT part of the description word budget (it is a fixed-format table, not copy).
        # Brief Q17 decides whether the block must be present (brief_flags.json, read via compare_build.q17()).
        nblk=len(re.findall(r'<div class="vp-compare"',h))
        if Q17 and p.get('compare',0) is None:
            if nblk: e.append('compare is null but a block is present')
        elif Q17:
            if nblk!=1: e.append(f'comparison block count {nblk} (Q17 = Add table: need exactly 1 — run compare_build.py)')
            elif not re.search(r'</table>\s*</div>\s*<h3>Key Features</h3>',h): e.append('comparison block not directly before <h3>Key Features</h3>')
        elif nblk: e.append(f'comparison block present but Q17 = No table (run compare_build.py to remove it)')
        h_nb=re.sub(r'<div class="vp-compare"[\s\S]*?</table>\s*</div>','',h)
        # fit block (Q19, rules/fit-block-rule.md): exactly one, single column "Right for you if", directly before <h3>FAQs</h3>
        # (moved from before Key Features 2026-09-06, user decision); none when Q19 = Skip or fit is null; words outside the budget.
        # 2026-09-07: the block also carries the fixed closing sentence (fit_build.CLOSE) — an old-layout block without it FAILs.
        nfit=len(re.findall(r'<div class="vp-fit"',h))
        if Q19 and p.get('fit',0) is None:
            if nfit: e.append('fit is null but a fit block is present')
        elif Q19:
            if nfit!=1: e.append(f'fit block count {nfit} (Q19 = Add: need exactly 1 — run fit_build.py)')
            elif not re.search(r'<div class="vp-fit"[\s\S]*?</div>\s*</div>\s*</div>\s*<h3>FAQs</h3>',h): e.append('fit block not directly before <h3>FAQs</h3>')
            elif 'Not the right fit if' in h: e.append('fit block still carries the removed "Not the right fit if" column (re-run fit_build.py)')
            elif FIT_CLOSE not in h: e.append('fit block without the closing sentence (old layout — re-run fit_build.py)')
        elif nfit: e.append('fit block present but Q19 = Skip (run fit_build.py to remove it)')
        h_nb=re.sub(r'<div class="vp-fit"[\s\S]*?</div>\s*</div>\s*</div>','',h_nb)
        tw=len(txt(h_nb))
        if tw<350: e.append(f'total words {tw}')
        # Ceiling 500 is a WARNING, never a FAIL (user decision 2026-09-05): a source spec / package / value line is never
        # dropped to meet it. spec_cover.py + value_check.py are the gates that matter; an overrun is logged, not blocked.
        if tw>500: print(pid, '|', p.get('title','')[:40], f'| WARN total words {tw} > 500 — allowed only because the source is longer; tighten prose/FAQ wording, never drop a source line')
        faqs=re.findall(r'<p><strong>Q: .*?</strong><br>A: .*?</p>',h)
        if len(faqs)!=5: e.append(f'faqs {len(faqs)}')
        fw=sum(len(txt(f)) for f in faqs)
        if not 110<=fw<=145: e.append(f'faq words {fw}')
        if re.search(r'<p>\s*</p>|<li>\s*</li>|<ul>\s*</ul>',h): e.append('empty element')
        for pm in re.finditer(r'<p([^>]*)>[^<]*(?:<[^/][^>]*>[^<]*</[^>]+>[^<]*)*</p>\s*<ul([^>]*)>',h):
            if 'margin-bottom: 0' not in pm.group(1) or 'margin-top: 0' not in pm.group(2): e.append('p+ul margin pairing')
        # the Q18 dimension image (`<img class="vp-dim" …>`, inserted under Specifications by dim_attach.py after the push,
        # rules/dimension-image-rule.md 2026-09-09) is not a source image: outside the count, inside the CDN / alt checks
        imgs=re.findall(r'<img[^>]+src="([^"]+)"',re.sub(r'<img class="vp-dim"[^>]*>','',h))
        if any(CDN not in s for s in re.findall(r'<img class="vp-dim"[^>]+src="([^"]+)"',h)): e.append('dimension image not on our CDN')
        if h.count('<img class="vp-dim"')>1: e.append('dimension image inserted more than once')
        if any(CDN not in s for s in imgs): e.append('foreign image')
        if p.get('_expected_images') is not None and len(imgs)!=p['_expected_images']: e.append(f'image count {len(imgs)} != {p["_expected_images"]}')
        if len(imgs)<2: e.append(f'only {len(imgs)} image(s) — a description carries at least two (gallery images fill empty slots, rule 2026-09-05)')
        for im in re.findall(r'<img[^>]*>',h):
            if 'alt="' not in im or 'alt=""' in im: e.append('img without alt')
        # 2026-09-11 (user instruction, ddl2 pregnancy pillow live): every Key Features / Specifications item is
        # `<li><strong>Name:</strong> text</li>` — list_bold.py bolds a plain lead-in; an item with no "Name:" lead FAILs here.
        for heading in ('Key Features','Specifications'):
            ms=re.search(r'<h3>'+heading+r'</h3>.*?<ul[^>]*>(.*?)</ul>',h,re.S)
            if not ms: continue
            for li in re.findall(r'<li[^>]*>(.*?)</li>',ms.group(1),re.S):
                if not re.match(r'\s*<strong>[^<]+:</strong>\s',li): e.append(f'{heading} item without bold "Name:" lead-in: {html.unescape(re.sub(r"<[^>]+>","",li)).strip()[:40]}')
        # 2026-09-11 (same instruction): the second description image carries a bottom margin so the text after it does not sit flush
        im2=[m.group(0) for m in re.finditer(r'<img\b[^>]*>',h) if 'class="vp-dim"' not in m.group(0)]
        if len(im2)>=2 and 'margin-bottom' not in im2[1]: e.append('second image without the bottom margin (run list_bold.py)')
        if 'Note:' in txt(h) or 'Note:' in h: e.append('Note: present')
        st=p.get('seo',{}).get('title',''); sd=p.get('seo',{}).get('description','')
        if len(st)>=70: e.append(f'seo.title {len(st)}')
        if len(sd)>=160: e.append(f'seo.desc {len(sd)}')
        if not 70<=len(p.get('title',''))<=145: e.append(f'title len {len(p.get("title",""))}')
        if e: bad+=1; print(pid, '|', p.get('title','')[:40], '|', '; '.join(e))
print(f'{bad} products with structure issues')
sys.exit(1 if bad else 0)
