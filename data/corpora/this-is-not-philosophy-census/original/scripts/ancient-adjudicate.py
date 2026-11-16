"""Lead-coder adjudication, 2026-11-15: rulings on the readers' flagged hard calls and on the B-skew review
(A/C rows from 2010 on whose abstracts set up an apparent defect; 181 read, 27 moved to B).
Rule for B: the abstract frames the author's text or doctrine as apparently inconsistent, defective, unconvincing or
conflicting, and the article defends it. Rule for D direction: an argument against the printed standard edition counts as open."""
import json
C=json.load(open('reach5-coded.json'))
R={ # id: (code, code2, dir)
 'rhizomata-184':('B','',''),'phronesis-1066':('B','D',''),'phronesis-316':('C','',''),'elenchos-484':('X','',''),
 'elenchos-539':('C','',''),'elenchos-129':('E','',''),'elenchos-530':('E','',''),'agph-3105':('C','F',''),'agph-2939':('C','',''),
 'apeiron-1356':('E','',''),'apeiron-1311':('B','A',''),'apeiron-1389':('B','A','')}
DIR={'phronesis-3':'open','phronesis-1040':'open','rhizomata-170':'open','phronesis-329':'neutral'}
TOB=['agph-2615','agph-2924','apeiron-1152','apeiron-1156','apeiron-1166','apeiron-1204','apeiron-1218','apeiron-1224','apeiron-1238',
 'apeiron-1243','apeiron-1253','apeiron-1256','apeiron-1275','apeiron-1343','apeiron-1357','apeiron-1392','apeiron-1393','apeiron-1403',
 'elenchos-308','elenchos-531','elenchos-577','phronesis-1005','phronesis-1025','phronesis-1185','phronesis-1264','phronesis-980','rhizomata-172']
log=[]
for k,(c,c2,d) in R.items(): log.append((k,C[k]['code'],c)); C[k].update(code=c,code2=c2,dir=d)
for k,d in DIR.items(): log.append((k,C[k].get('dir'),d)); C[k]['dir']=d
for k in TOB: log.append((k,C[k]['code'],'B')); C[k]['code2']=C[k]['code']; C[k]['code']='B'
for k in C: C[k].setdefault('adjudicated',False)
for k,_,_ in log: C[k]['adjudicated']=True
json.dump(C,open('reach5-adjudicated.json','w'),ensure_ascii=False)
json.dump(log,open('adjudication-log.json','w'),ensure_ascii=False,indent=0)
print(len(log),'rulings')
