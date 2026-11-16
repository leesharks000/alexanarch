"""Reverse review, 2026-11-15: all 156 B rows from 2010 on read; 17 moved out of B where the abstract sets up an interpretive
problem or a scholarly dispute but no apparent defect in the author's text that the article defends the text against."""
import json
A=json.load(open('reach5-adjudicated.json')); log=json.load(open('adjudication-log.json'))
MOV={'agph-2878':'A'}
for k in "apeiron-1158 apeiron-1169 apeiron-1358 apeiron-1365 elenchos-223 elenchos-330 elenchos-488 elenchos-490 elenchos-498 elenchos-606 phronesis-1069 phronesis-1188 phronesis-1173 phronesis-1282 rhizomata-91 rhizomata-178".split(): MOV[k]='C'
for k,c in MOV.items():
    assert A[k]['code']=='B',k; log.append([k,'B',c]); A[k].update(code=c,code2='B',adjudicated=True)
json.dump(A,open('reach5-adjudicated.json','w'),ensure_ascii=False); json.dump(log,open('adjudication-log.json','w'),ensure_ascii=False,indent=0)
print(len(MOV),'moved;',len(log),'rulings total')
