import json,re,itertools,sys
def words(s): return set(re.findall(r"[a-z0-9]+", s.lower()))
T=json.load(open(sys.argv[1] if len(sys.argv)>1 else 'titles_draft.json'))
for a,b in itertools.combinations(sorted(T,key=int),2):
    wa,wb=words(T[a]),words(T[b]); ov=len(wa&wb)/min(len(wa),len(wb))
    if ov>=0.55: print(f"{a}/{b} {ov:.0%} shared={sorted(wa&wb)}  |A|={len(wa)} |B|={len(wb)}")
