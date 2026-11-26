#!/usr/bin/env python3
"""The seat read at the places conj.py pointed to. Fetches verses and counts where a wording stands; the reading is in the file.
   python3 read.py <alexanarch root> <engine dir> read.json"""
import sys, re, json, pathlib
sys.path.insert(0, sys.argv[2]); import midrash as E
root = pathlib.Path(sys.argv[1]) / "data/corpora"
def sq(s): return re.sub(r"\s+", " ", E.norm(s)).strip()
def load(c):
    o = []
    for p in sorted((root / c / "text").glob("*.txt")):
        seen = set()
        for l in p.read_text(encoding="utf-8", errors="ignore").splitlines():
            if "\t" in l:
                r, t = l.split("\t", 1); r = r.strip()
                if re.search(r"\d+:\d+$", r) and r not in seen: seen.add(r); o.append((r, sq(t)))
    return o
NT, LXX = load("gnt-nestle1904"), load("lxx-swete"); D = dict(NT); OUT = dict(verses={}, counts={})
def V(*refs):
    for r in refs:
        for x in ([r] if "-" not in r.split(":")[1] else [f"{r.split(':')[0]}:{i}" for i in range(int(r.split(':')[1].split('-')[0]), int(r.split('-')[1]) + 1)]):
            OUT["verses"][x] = D[x]; print("  ", x, D[x][:330])
def L(book, ref):
    for r, t in LXX:
        if r.startswith(book) and r.endswith(" " + ref): print("  ", r, t[:260]); OUT["verses"][r] = t; return
def C(lab, rx, n=14):
    c = re.compile(rx); a = [r for r, t in NT if c.search(t)]; b = [r for r, t in LXX if c.search(t)]; OUT["counts"][lab] = dict(nt=a, lxx_n=len(b), lxx=b[:8]); print(f"  # {lab}: NT {len(a)} {a[:n]} | LXX {len(b)} {b[:5]}")
print("== the seventy"); V("Luke 10:1", "Luke 10:12-13", "Luke 10:17-20", "Rev 9:1", "Rev 9:3-5", "Rev 9:10", "Rev 9:19", "Rev 11:3", "Rev 11:8", "Rev 12:9", "Matt 11:21"); L("Δευτερονόμιον", "8:15"); L("Ψαλμοί", "90:13"); L("Ἠσαΐας", "14:12")
C("scorpion", r"σκορπι"); C("scorpion with authority, one verse", r"σκορπι.*εξουσι|εξουσι.*σκορπι"); C("serpent with scorpion, one verse", r"οφ(ισ|εων|εσιν|ιν).*σκορπι|σκορπι.*οφ(ισ|εων|εσιν|ιν)")
C("hurt (ἀδικέω) with not/nothing", r"(ουδεν|μη|ου) (υμασ )?(ου μη )?αδικησ"); C("fallen from heaven", r"εκ του ουρανου πε(σοντα|πτωκοτα)|εξεπεσεν εκ του ουρανου|επεσεν εκ του ουρανου"); C("Satan with heaven, one verse", r"σαταν.*ουραν|ουραν.*σαταν")
C("names written, in heaven or the book", r"ονομα\w* (υμων |αυτων |αυτου )?(εν)?γεγρα\w+ (εν|επι)|γεγραπται το ονομα"); C("sackcloth with Sodom within the passage is by reading; sackcloth", r"σακκ"); C("Sodom", r"σοδομ")
print("== the supper, Luke 22"); V("Luke 22:28-32", "Rev 2:10", "Rev 2:26-28", "Rev 3:2", "Rev 3:10", "Rev 3:20-21", "Matt 19:28")
C("strengthen, as a command (στήρισον)", r"στηρισον"); C("κἀγώ with 'my Father', one verse", r"καγω.*πατ\w+ μου|πατ\w+ μου.*καγω"); C("as … I also / as my Father … I also (καθώς or ὡς, κἀγώ, Father)", r"(καθωσ|ωσ) .*πατ.*καγω|καγω.*(καθωσ|ωσ) .*πατ")
C("throne with eating or supper, within a verse", r"θρον.*(εσθ[ιη]|δειπν|τραπεζ)|(εσθ[ιη]|δειπν|τραπεζ).*θρον"); C("sit on throne(s), promised (καθίσαι, καθήσεσθε, καθίσεσθε)", r"καθ(ισαι|ησεσθε|ισεσθε).*θρον"); C("temptation(s), the noun", r"πειρασμ")
print("== the woes"); V("Matt 23:16", "Matt 23:25-28", "Matt 23:35", "Luke 11:39", "Luke 11:50", "Rev 17:4", "Rev 17:6", "Rev 18:24", "Rev 16:6", "Rev 18:10")
C("cup with full (γέμω)", r"ποτηρι.*γεμ|γεμ.*ποτηρι"); C("full (γέμω) with unclean", r"γεμ.*ακαθαρ|ακαθαρ.*γεμ"); C("γέμω, any", r"\bγεμ(ει|ον|οντα|ουσ|ουσιν|ουσασ|ιζ)"); C("blood with prophets, one verse", r"αιμα.*προφητ|προφητ.*αιμα"); C("blood … on the earth, shed or slain", r"αιμα.*επι τησ γησ")
C("woe in Matt 23 and Rev 18 (all woes)", r"\bουαι\b", 60)
print("== the sower"); V("Mark 4:5-8", "Mark 4:29", "Matt 13:6", "Rev 14:15", "Rev 16:8-9", "Rev 16:12"); L("Ἰωήλ", "3:13"); C("scorched (καυματίζω)", r"καυματι"); C("dried (ἐξηράνθη)", r"εξηρανθη"); C("sickle with harvest", r"δρεπαν.*θερισ|θερισ.*δρεπαν")
print("== the mountain's frame"); V("Matt 16:27-28", "Matt 17:1-4", "Rev 21:3", "Rev 21:10", "Rev 22:12"); C("tent (σκηνή, σκηνόω)", r"\bσκην(η|ην|ησ|ασ|αι|ωσει|ουντ|ουσιν)\b"); C("to pay each according to", r"αποδ\w+ εκαστω")
print("== Gethsemane"); V("Matt 26:38-41", "Rev 3:2-3", "Rev 3:10"); C("hour with temptation, one verse", r"ωρα.*πειρασμ|πειρασμ.*ωρα"); C("watch with hour, one verse", r"γρηγορ.*ωρα|ωρα.*γρηγορ"); C("watch (γρηγορέω)", r"γρηγορ", 30)
print("== John 21"); V("John 21:15", "Rev 7:17"); C("ἀρνίον outside Revelation", r"\bαρνι(ον|ου|ω|α)\b(?!.*zzz)", 4)
json.dump(OUT, open(sys.argv[3], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
