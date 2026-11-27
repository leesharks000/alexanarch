exec(open('../residue/r1.py').read().split("print('P1")[0])
import json,random,collections
MT=NT['MT']; RE=NT['RE']
def rng(s):
    out=set()
    for part in s.split(','):
        part=part.strip()
        if not part: continue
        c,vs=part.split(':'); a,_,b=vs.partition('-'); out|={(int(c),v) for v in range(int(a),int(b or a)+1)}
    return out
JREV=rng('1:17-20,2:1-29,3:1-22,16:15,22:7,22:12-13,22:16,22:20')
# Matthew: verses spoken by Jesus, from memory, written before the count
JMT=rng('3:15,4:4,4:7,4:10,4:17,4:19,5:3-48,6:1-34,7:1-27,8:3-4,8:7,8:10-13,8:20,8:22,8:26,8:32,9:2,9:4-6,9:9,9:12-13,9:15-17,9:22,9:24,9:28-30,9:37-38,10:5-42,11:4-19,11:21-30,12:3-8,12:11-13,12:25-37,12:39-45,12:48-50,13:3-9,13:11-33,13:37-52,13:57,14:16,14:18,14:27,14:29,14:31,15:3-11,15:13-20,15:24,15:26,15:28,15:32,15:34,16:2-4,16:6,16:8-11,16:13,16:15,16:17-19,16:23-28,17:7,17:9,17:11-12,17:17,17:20-23,17:25-27,18:3-20,18:22-35,19:4-6,19:8-9,19:11-12,19:14,19:17-19,19:21,19:23-24,19:26,19:28-30,20:1-16,20:18-19,20:21-23,20:25-28,20:32,21:2-3,21:13,21:16,21:19,21:21-22,21:24-25,21:27-44,22:1-14,22:18-21,22:29-32,22:37-40,22:42-45,23:2-39,24:2,24:4-51,25:1-46,26:2,26:10-13,26:18,26:21,26:23-29,26:31-32,26:34,26:36,26:38-42,26:45-46,26:50,26:52-56,26:64,27:11,27:46,28:10,28:18-20')
print('Matthew verses in his speech (my map):',len(JMT&set(MT)),'of',len(MT),round(100*len(JMT&set(MT))/len(MT)),'%')
Lr=json.load(open('../map/rev-matthew-ledger.json'))['rows']
def segs(V,s):
    o=[]
    for part in re.split(r'\s*[;+]\s*',str(s)):
        m=re.match(r'(\d+):(\d+)(?:-(\d+))?$',part.strip())
        if m:
            c=int(m.group(1)); a=int(m.group(2)); b=int(m.group(3) or a); o+=[(c,v) for v in range(a,b+1) if (c,v) in V]
    return o
rows=[]
for r in Lr:
    mk=segs(MT,r['matt']); rk=segs(RE,r['rev'])
    if not(mk and rk): continue
    sp=sum(k in JREV for k in rk)*2>len(rk); rows.append((sp, mk[0] in JMT, r))
T=collections.Counter((a,b) for a,b,_ in rows)
for a in (True,False):
    n=T[(a,True)]+T[(a,False)]; print('speaker rows' if a else 'vision rows ',n,'| land in his speech',T[(a,True)],f'({round(100*T[(a,True)]/n)}%)','| in narrative or others',T[(a,False)])
obs=T[(True,True)]/(T[(True,True)]+T[(True,False)])-T[(False,True)]/(T[(False,True)]+T[(False,False)])
random.seed(3); lab=[a for a,_,_ in rows]; ge=0
for _ in range(10000):
    random.shuffle(lab); t=collections.Counter(zip(lab,[b for _,b,_ in rows])); d=t[(True,True)]/(t[(True,True)]+t[(True,False)])-t[(False,True)]/(t[(False,True)]+t[(False,False)]); ge+= abs(d)>=abs(obs)
print('difference',round(100*obs),'points; p =',(ge+1)/10001)
print('Z2 speaker rows landing outside his speech:')
for a,b,r in rows:
    if a and not b: print('   Rev',r['rev'],'-> Mt',r['matt'],'|',str(r.get('matt_relation'))[:70])
