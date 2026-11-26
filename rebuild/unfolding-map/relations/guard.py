#!/usr/bin/env python3
"""The guard at the tomb as relations (the form and rules of relations.py, unchanged). python3 guard.py <alexanarch root> <engine dir> out.json"""
import sys, json
root, eng, outp = sys.argv[1:4]; sys.argv = [sys.argv[0], root, eng, outp]
import relations as R
r = R.r
P = [
("the sealing", "gnt:Rev 20:1-3", "gnt:Matt 27:62-66", r(("ANGEL","αγγελον"),("σφραγιζω","εσφραγισεν"),("ADVERSARY","πλανοσ","πλανηση"),mode="VISION-EVENT"), r(("ADVERSARY","αρχιερεισ"),("σφραγιζω","σφραγισαντεσ"),("CHRIST","πλανοσ","πλανοσ"),mode="NARRATIVE-EVENT")),
("the descent", "gnt:Rev 20:1", "gnt:Matt 28:2", r(("ANGEL","αγγελον"),("καταβαινω","καταβαινοντα"),(None,"ουρανοσ","εκ του ουρανου"),mode="VISION-EVENT"), r(("ANGEL","αγγελοσ"),("καταβαινω","καταβασ"),(None,"ουρανοσ","εξ ουρανου"),mode="NARRATIVE-EVENT")),
("what the angel does at the closure", "gnt:Rev 20:3", "gnt:Matt 28:2", r(("ANGEL",None),("κλειω","εκλεισεν"),(None,"επανω αυτου","επανω αυτου"),mode="VISION-EVENT"), r(("ANGEL","αγγελοσ"),("αποκυλιω","απεκυλισεν"),(None,"επανω αυτου","επανω αυτου"),mode="NARRATIVE-EVENT")),
("the deceiving", "gnt:Rev 20:3", "gnt:Matt 27:64", r(("ADVERSARY",None),("πλαναω","πλανηση"),("ALL","εθνοσ","τα εθνη"),pol="-",mode="VISION-EVENT"), r(("FAITHFUL","μαθηται"),("πλαναω","πλανη"),("ALL","λαοσ","τω λαω"),pol="-",mode="STATEMENT")),
("the seizing", "gnt:Rev 20:2", "gnt:Matt 28:9", r(("ANGEL",None),("κρατεω","εκρατησεν"),("ADVERSARY","δρακων","δρακοντα"),mode="VISION-EVENT"), r(("FAITHFUL",None),("κρατεω","εκρατησαν"),("CHRIST","πους","τουσ ποδασ"),mode="NARRATIVE-EVENT")),
]
S = R.M.Seats(root); rows, bad = [], []
for name, sl, tl, s, t in P:
    st, tt = R.sq(S.get(sl)), R.sq(S.get(tl))
    for rel, txt, wh in ((s, st, "seed"), (t, tt, "target")):
        for f in R.forms(rel):
            if f not in txt: bad.append((name, wh, f))
        if rel["pol"] == "-" and not R.NEG.search(txt): bad.append((name, wh, "minus without a particle"))
    F, O = R.DERIVE(s, t); rows.append(dict(name=name, seed=sl, target=tl, features=sorted(F), operators=sorted(O))); print(f"{name:36} {sorted(F)} => {sorted(O)}")
print("forms not found:", bad or "none"); json.dump(dict(rows=rows, bad=bad), open(outp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
