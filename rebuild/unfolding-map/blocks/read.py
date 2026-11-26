#!/usr/bin/env python3
"""The seat read at the section-and-block pairs blocks.py pointed to. Fetches and counts; the reading is in the file.
   python3 read.py <alexanarch root> <engine dir> read.json"""
import sys, re, json, pathlib
sys.path.insert(0, sys.argv[2]); import midrash as E
root = pathlib.Path(sys.argv[1]) / "data/corpora"
def load(c):
    o = []
    for p in sorted((root / c / "text").glob("*.txt")):
        seen = set()
        for l in p.read_text(encoding="utf-8", errors="ignore").splitlines():
            if "\t" in l:
                r, t = l.split("\t", 1); r = r.strip()
                if re.search(r"\d+:\d+$", r) and r not in seen: seen.add(r); o.append((r, re.sub(r"\s+", " ", E.norm(t)).strip()))
    return o
NT, LXX = load("gnt-nestle1904"), load("lxx-swete"); D = dict(NT); OUT = dict(verses={}, counts={})
def V(*refs):
    for r in refs:
        b, cv = r.rsplit(" ", 1); c, v = cv.split(":"); a, z = (v.split("-") + [v])[:2]
        for i in range(int(a), int(z) + 1): x = f"{b} {c}:{i}"; OUT["verses"][x] = D[x]; print("  ", x, D[x][:300])
def C(lab, rx, n=16):
    c = re.compile(rx); a = [r for r, t in NT if c.search(t)]; b = [r for r, t in LXX if c.search(t)]; OUT["counts"][lab] = dict(nt=a, lxx_n=len(b), lxx=b[:6]); print(f"  # {lab}: NT {len(a)} {a[:n]} | LXX {len(b)} {b[:4]}")
print("== Rev 4-5 and John 20-21"); V("John 20:11-15", "John 20:19", "John 20:26-28", "John 20:30", "Rev 4:1-2", "Rev 4:4", "Rev 4:11", "Rev 5:1-6")
C("Lord and God, with a possessive, addressed", r"ο κυριοσ (μου |ημων )?και ο θεοσ (μου|ημων)"); C("stood / standing in the midst", r"εστη (εισ το μεσον|εν μεσω)|εν μεσω .{0,60}εστηκοσ|εστηκοσ .{0,30}εν μεσω"); C("weep, forbidden or questioned", r"μη κλαιε|τι κλαιεισ")
C("wept, imperfect (ἔκλαιον, ἔκλαιεν)", r"εκλαιον|εκλαιεν"); C("in white, sitting", r"καθ\w+ .{0,40}εν (ιματιοισ )?λευκοισ|εν λευκοισ καθ"); C("a book with 'written' and 'not/no one'", r"βιβλι.*γεγραμμεν|γεγραμμεν.*βιβλι")
print("== Rev 21-22 and Luke 13:22-19:27"); V("Luke 13:24-29", "Luke 14:17", "Luke 15:22", "Luke 16:10", "Luke 16:15", "Luke 16:19-21", "Luke 17:29", "Rev 21:8", "Rev 21:12-13", "Rev 21:25-27", "Rev 22:11", "Rev 22:14-15", "Rev 22:17")
C("north (βορρᾶς)", r"βορρα"); C("east with west", r"ανατολ.*δυσμ|δυσμ.*ανατολ"); C("dogs", r"\bκυν(εσ|ασ|ων|αρι)|\bκυων"); C("gate (πυλών)", r"πυλων", 24); C("outside, with stand or dogs", r"εξω (εσταναι|οι κυνεσ)|εστηκ\w+ εξω")
C("sulfur (θεῖον)", r"\bθει(ον|ου|ω)\b"); C("purple with fine linen", r"πορφυρ.*βυσσ|βυσσ.*πορφυρ"); C("robe (στολή)", r"\bστολ(η|ην|ασ|αισ|αι)\b"); C("abomination (βδέλυγμα)", r"βδελυγμα"); C("enter by the gate(s) / door", r"εισελθ\w+ (δια τησ στενησ (θυρασ|πυλησ)|.{0,30}τοισ πυλωσιν)|πυλωσιν εισελθ")
print("== Rev 21-22 and Matt 19:27-20:16"); V("Matt 19:27-30", "Rev 21:5", "Rev 21:7", "Rev 21:12", "Rev 21:14")
C("the twelve tribes", r"δωδεκα φυλ|δωδεκαφυλ"); C("will inherit (κληρονομήσει)", r"κληρονομησ(ει|ουσιν|ω)\b"); C("twelve tribes with twelve apostles/thrones within a verse or the next is by reading; twelve twice in a verse", r"δωδεκα.*δωδεκα"); C("regeneration / I make new", r"παλινγενεσ|παλιγγενεσ|καινα ποιω")
print("== the seals and Luke 21"); V("Luke 21:22", "Luke 21:24", "Luke 21:36", "Rev 6:4", "Rev 6:10", "Rev 6:17", "Mark 13:33"); C("to stand, to be stood (σταθῆναι)", r"σταθηναι"); C("vengeance, avenge (ἐκδικ-)", r"εκδικ", 20); C("the sword (μάχαιρα) with fall, slay, given", r"μαχαιρ")
json.dump(OUT, open(sys.argv[3], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
