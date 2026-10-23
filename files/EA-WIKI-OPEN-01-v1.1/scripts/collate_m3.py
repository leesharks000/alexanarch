import re,json,glob,sys
S='/tmp/claude-0/-home-claude/97be5201-55d8-50c9-b9d9-c76c8dde5ac6/scratchpad/'; R='/home/claude/drafts/wiki-open/assembly-02/'
def norm(s):
    for a,b in [('‘‘','"'),('’’','"'),('‘',"'"),('’',"'"),('“','"'),('”','"')]: s=s.replace(a,b)
    return re.sub(r'\s+',' ',s).strip().lower()
M3=norm(open(R+'message-3-break-cases.txt',encoding='utf-8').read()); M1=norm(open(R+'message-1-blind-reading.txt',encoding='utf-8').read())
F={'SE34GR':S+'src/se34-seated-1574-s1.md','MIT':S+'src/mit-se.flat.txt','SEPLOGIC':S+'src/sep-aristotle-logic.flat.txt','SEPANC':S+'m3/src/sep-logic-ancient.flat.txt','APRGR':S+'m3/src/apr-gr.flat.txt','APRMIT':S+'m3/src/pa-mit.flat.txt','NEGR':S+'m3/src/ne-gr.flat.txt','NEMIT':S+'m3/src/ne-mit.flat.txt','GRANT':S+'m3/src/grant.flat.txt','CATGR':S+'m3/src/cat-gr.flat.txt','CATMIT':S+'m3/src/cat-mit.flat.txt','LSJ':S+'m3/src/lsj-arete.flat.txt'}
FULL={k:norm(open(v,encoding='utf-8').read()) for k,v in F.items()}; FULL['BARNES']=norm("History's first logic has also been the most influential...")
tab={}
for fam in ['deepseek','gemini','chatgpt']:
    t=open(R+f'replies/{fam}-m3.txt',encoding='utf-8').read(); a=json.loads(t[t.index('['):t.rindex(']')+1])
    shown=M3+' '+M1; n=s=0; out=[]
    for o in a:
        sp=list(o.get('spans',[]))
        hm=o.get('holder_and_mood') or {}
        for side in ('source','sentence'):
            if hm.get(side,{}).get('span'): sp.append(hm[side]['span'])
        for x in sp:
            q=x.get('quote') or ''
            parts=[p.strip(' .…') for p in re.split(r'\s*(?:\.\.\.|…)\s*',q) if len(p.strip(' .…'))>4]
            if not parts: continue
            n+=1; ok=all(norm(p) in shown for p in parts)
            full=x['source'] in FULL and all(norm(p) in FULL[x['source']] for p in parts)
            s+=ok
            if not ok: out.append(f"   {'SOURCE-ONLY' if full else 'BREACH'} {o['case']} {x['source']} | {q[:110]}")
        tab.setdefault(o['case'],{})[fam]=(o.get('attributization','-'),(o.get('retained_authority') or {}).get('value','-'),(hm or {}).get('match','-') if hm else '-', ', '.join(o.get('support',[]))[:60])
    print(f'== {fam}: {n} spans, {s} in the text shown'); print('\n'.join(out))
print()
for c,d in tab.items():
    print(c); [print(f'   {f:9} attr={v[0]:8} RA={v[1]:8} match={str(v[2]):10} | {v[3]}') for f,v in d.items()]
