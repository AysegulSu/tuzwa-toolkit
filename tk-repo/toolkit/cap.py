import json,sys,re,glob
KW={}
for ln in open('kw.txt'):
    k,v,c,p=ln.rstrip('\n').split('|'); KW[k]=(int(v),c,p)
def cap(title):
    tl=title.lower(); got=[(KW[k][0],k) for k in KW if k in tl]
    got.sort(reverse=True)
    # dedupe word-order/plural variants
    seen=[];vol=0
    for v,k in got:
        ws=frozenset(re.findall(r'[a-z0-9]+',k))-{'for','the','and','with','of','a','in','to','on'}
        if any(ws==s[1] or (v==s[0] and (k in s[2] or s[2] in k)) for s in seen): continue
        seen.append((v,ws,k)); vol+=v
    return len(title),vol,[(v,k) for v,ws,k in seen]
if __name__=='__main__':
    for t in sys.argv[1:]:
        L,vol,got=cap(t); print(f"{L}ch {vol:,}  {t}\n   "+' · '.join(f"{k} {v:,}" for v,k in got))
