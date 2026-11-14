import json, yaml
from vlib import *
import claims_new as C
def walk(o):
    if isinstance(o,dict):
        for v in o.values(): yield from walk(v)
    elif isinstance(o,list):
        for v in o: yield from walk(v)
    elif isinstance(o,str): yield o
bad=0
for c in C.A:
    if c['dep']=='capture-registry': hay=entry_text(c['locus'].split(',')[0])
    elif 'kernel' in c['file']:
        hay="\n".join(s for f in c['file'].split(' + ') for s in walk(yaml.safe_load((ROOT/f).read_text())))
    else: hay=deposit_text(c['file'])
    if not found(c['quote'],hay): bad+=1; print('FAIL',c['id'],c['quote'][:120])
print('A new',len(C.A),'bad',bad)
srcs,cl=C.fieldnew()
for k,c in cl.items():
    if not found(c['quote'], entry_text(C.OBS)): print('FAIL',k)
for k,c in C.BR_CLAIMS.items():
    f={'B31':'oup-ai-disclosure.txt','B32':'camws-ajcr.txt','B35':'ora-postcolonial-sparagmos.txt'}[c['source']]
    if not found(c['quote'], (STAGE/'sources'/f).read_text()): print('FAIL',k,c['quote'][:100])
print(len(cl),len(C.BR_CLAIMS))
