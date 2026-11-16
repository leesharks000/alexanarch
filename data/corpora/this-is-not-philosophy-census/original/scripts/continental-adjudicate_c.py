"""Lead-coder rulings on the continental readers' 31 flagged hard calls, 2026-11-15. 26 stand; 5 change.
Rule carried from the analytic note: critique of a contemporary's position in a live debate is G."""
import json
O=json.load(open("reachc-coded.json"))
R={"phiToday-3091":("C","D",""),"phiToday-2999":("G","C",""),"phiToday-3001":("G","C",""),"phiToday-2769":("A","F",""),"phiToday-2642":("G","E","")}
log=[]
for k,(c,c2,d) in R.items(): log.append([k,O[k]["code"],c]); O[k].update(code=c,code2=c2,dir=d,adjudicated=True)
json.dump(O,open("reachc-adjudicated.json","w"),ensure_ascii=False); json.dump(log,open("adjudication-log-c.json","w"),indent=0)
