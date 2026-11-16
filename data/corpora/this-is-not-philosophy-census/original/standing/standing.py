"""Hand rulings on titles pulled by a text-standing lexicon (dpull2.tsv), 2026-11-15.
S = the title puts a work's standing in question (authenticity, authorship, date of composition, composition/redaction,
order, unity of a work, arrangement of a corpus). T = text or fragment (emendation, text of a passage, edition, fragment study).
Reviews of books, doctrinal 'unity of' titles and false hits are excluded."""
import json,collections
S="""agph-1180 agph-1318 agph-1228 agph-486 agph-495 agph-513 agph-499 agph-1339 agph-524 agph-1447 agph-1500 agph-2110 agph-844 agph-1117 agph-2904
ap-114 ap-190 ap-958 ap-1059 ap-1106 ap-265 ap-278 ap-1311 ap-1885 ap-2011 apeiron-608 apeiron-61 apeiron-1013 apeiron-1346
elenchos-117 elenchos-517 phronesis-724 phronesis-829 phronesis-523 phronesis-908 phronesis-183 phronesis-281 phronesis-1114 phronesis-1115 phronesis-1144 phronesis-1225""".split()
T="""agph-1969 agph-2594 agph-2825 agph-2887 ap-65 ap-687 ap-1429 apeiron-1161 elenchos-281 elenchos-310 elenchos-104 elenchos-580 elenchos-143 elenchos-327 elenchos-14
elenchos-39 elenchos-605 phronesis-793 phronesis-808 phronesis-419 phronesis-435 phronesis-526 phronesis-540 phronesis-893 phronesis-996 phronesis-1285 rhizomata-33 rhizomata-97""".split()
# ancient titles the object coder left unnamed (fragments, chronology), ruled by hand and added to numerator and denominator
S+="agph-1305 agph-494 agph-183 agph-228 ap-482 elenchos-172".split()
T+="agph-1278 agph-1281 agph-1282 agph-1178 agph-501 agph-514 agph-655 apeiron-663 phronesis-554 agph-965 phronesis-639 phronesis-216 elenchos-192 elenchos-193 elenchos-409 elenchos-410".split()
EXTRA=set("agph-1305 agph-494 agph-183 agph-228 ap-482 elenchos-172 agph-1278 agph-1281 agph-1282 agph-1178 agph-501 agph-514 agph-655 apeiron-663 phronesis-554 agph-965 phronesis-639 phronesis-216 elenchos-192 elenchos-193 elenchos-409 elenchos-410".split())
rows=[x for x in json.load(open('titles-all.json')) if x[4]!='none named' or f"{x[0]}-{x[2]}" in EXTRA]
def P(y):
    if y<1920: return '1888–1919'
    if y<1980: return '1950–79'
    if y<2000: return '1980–99'
    if y<2010: return '2000–09'
    if y<2020: return '2010–19'
    return '2020–26'
n=collections.Counter(); s=collections.Counter(); t=collections.Counter()
for j,y,i,ti,g,_,k in rows:
    if not y or (1920<=y<1950): continue
    key=f"{j}-{i}"; p=P(y); n[p]+=1; s[p]+=key in S; t[p]+=key in T
print("period      named   S   S%    T   T%   S+T%")
for p in ['1888–1919','1950–79','1980–99','2000–09','2010–19','2020–26']:
    print(f"{p:10} {n[p]:6} {s[p]:3} {100*s[p]/n[p]:4.1f} {t[p]:4} {100*t[p]/n[p]:4.1f} {100*(s[p]+t[p])/n[p]:5.1f}")
