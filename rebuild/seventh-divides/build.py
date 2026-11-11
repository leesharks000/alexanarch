#!/usr/bin/env python3
"""Assemble EA-MIDST-01 v1.0, The Seventh That Divides, from the Philo draft (Part I) and the seven
notebook (Parts II-IV), with the review pass of 2026-11-10 20:37 applied. Every paragraph of the two
sources is carried; renumbering of the notebook and the rewritten paragraphs are listed in CHANGES."""
import re, pathlib, json
H = pathlib.Path(__file__).resolve().parent
P = H.parent / "philo-out-loud"
draft = (P / "DRAFT-v0.1.md").read_text(encoding="utf-8")
note = (P / "NOTEBOOK-the-seven.md").read_text(encoding="utf-8")
CHANGES = []

def take(src, start, end=None):
    i = src.index(start)
    j = src.index(end, i) if end else len(src)
    return src[i:j]

def sub1(s, old, new):
    assert s.count(old) == 1, old[:80]
    CHANGES.append(old[:70])
    return s.replace(old, new)

# ---------------- Part I: the Philo draft, sections 1-8 ----------------
part1 = take(draft, "### 1. The conventional reading, in full", "### 9. What is established")
part1 = part1.replace("### ", "## ")

# review (ChatGPT, 20:37): 5.4 overstates what the unsayable proper name establishes
part1 = sub1(part1,
    "The proper name of the Logos is unsayable by doctrine. What can be said are names in catachresis, given so that humans approaching the best name may be ordered by it: \"ἵν’, εἰ καὶ μὴ πράγματι, ὀνόματι γοῦν προσερχόμενοι ἀρίστῳ κατ’ αὐτὸ κοσμῶνται\" (Mut. 13). A Philo who named the Logos Ἰησοῦς in his own voice would break his own rule. The name he gives, Ἀνατολή, he gives through an oracle in another's mouth.",
    "The proper name of the Logos is unsayable by doctrine. What can be said are names in catachresis, given so that humans approaching the best name may be ordered by it: \"ἵν’, εἰ καὶ μὴ πράγματι, ὀνόματι γοῦν προσερχόμενοι ἀρίστῳ κατ’ αὐτὸ κοσμῶνται\" (Mut. 13). The doctrine governs the architecture of the paper: the Logos is approached through many names, Israel among them (Conf. 146), and each is a name of approach. It does not explain the absence of one name in particular. Ἰησοῦς said of the Logos would be one more name of approach, and Philo's rule would allow it as it allows Israel. The absence of Ἰησοῦς from the list is a fact of the text, and this paper reads it as one; the doctrine of Mut. 15 does not account for it. What the doctrine does account for is the manner of the one name of Conf. 62: Ἀνατολή is given through an oracle in another's mouth.")

# review: Joshua within a plurality
part1 = sub1(part1,
    "He builds the press, the coin, the impress and the one who receives it, and gives the receiver that name.",
    "He builds the press, the coin, the impress and the one who receives it, and gives the receiver that name.\n\n7a.7. The receiver is one of several. The same treatise re-strikes Abraham (Mut. 71), has the Logos rename Jacob Israel (Mut. 87), re-inspirits Caleb (Mut. 123–124), calls Moses many-named (Mut. 125) and Isaac the indwelling son (Mut. 131). Each is a different operation on a different life: a re-striking, a renaming by the Logos, a new spirit, a plurality of offices, an indwelling. Ἰησοῦς is the one Philo names as the imitator of Moses' character (Virt. 66), and his renaming is the one described as a quality struck into a state (Mut. 121–122). The passages do not make him the sole recipient of the pattern. The multiplicity is the finding: one pattern stays recognizable across distinct names, lives and offices. Justin's gathering of the names Israel, Ἰησοῦς and Ἀνατολή onto one person (§8) is then a further operation, a consolidation, and it is Justin's.")

# review: preserve the differences in access to the sealed name (7b)
part1 = sub1(part1,
    "The archive's reading of Pergamum (#165; #828) enters here as related work.",
    "The archive's reading of Pergamum (#165; #828) enters here as related work.\n\n7b.7a. The access differs, and the difference is the transformation. In Philo the sealed Name on the crown-plate may be heard and spoken by a class: \"μόνοις τοῖς ὦτα καὶ γλῶτταν σοφίᾳ κεκαθαρμένοις\", in the holy place (Vit. Mos. II.114). In the Apocalypse the new name on the stone is known by one: \"ὃ οὐδεὶς οἶδεν εἰ μὴ ὁ λαμβάνων\" (2:17); and the rider's written name by one: \"ὃ οὐδεὶς οἶδεν εἰ μὴ αὐτός\" (19:12). A name restricted to the purified who may speak it becomes a name held by its receiver alone. The office of hearing and saying moves from a priestly class to the individual conqueror, at a station, through a gift.")

# review: Justin's consolidation named as an operation
part1 = sub1(part1,
    "are the names under which the second century says Jesus out loud.",
    "are the names under which the second century says Jesus out loud. Justin's act is a consolidation: names that Philo distributes across the Logos, Israel, the renamed Hosea and the companion's oracle, Justin gathers on one person.")

# ---------------- Parts II-IV: the notebook, renumbered ----------------
nb = take(note, "## 1. Philo: the planets are gods", "## 7. Scholarship on Philo and Revelation")
nb7 = take(note, "## 7. Scholarship on Philo and Revelation")
# the commission paragraphs 3.1c-3.1e move to their own section
com_start = nb.index("3.1c. The commission")
com_end = nb.index("3.1b. Two sevens kept distinct.")
commission = nb[com_start:com_end]
nb = nb[:com_start] + nb[com_end:]

MAP = {"1": "9", "2": "10", "3": "11", "4": "12", "5": "13", "6": "14", "7": "16"}
def renum_heads(text):
    text = re.sub(r"^## ([1-7])\. ", lambda m: "## " + MAP[m.group(1)] + ". ", text, flags=re.M)
    text = re.sub(r"^([1-7])\.(\d+[a-z]?)\. ", lambda m: MAP[m.group(1)] + "." + m.group(2) + ". ", text, flags=re.M)
    return text
nb = renum_heads(nb); nb7 = renum_heads(nb7)
commission = commission.replace("3.1c. ", "15.1. ").replace("3.1d. ", "15.2. ").replace("3.1e. ", "15.3. ")

# internal cross-references, one by one
XR = [
    ("Ginza (4) rejects", "Ginza (§12) rejects"),
    ("the Haran Gawaita (5.4) rejects", "the Haran Gawaita (13.4) rejects"),
    ("strong (6.6).", "strong (14.6)."),
    ("This sharpens the contrast with the Gawaita (3.3):", "This sharpens the contrast with the Gawaita (11.3):"),
    ("and the occupants are replaced (3.3).", "and the occupants are replaced (11.3)."),
    ("with the Ginza §192 (4.1: Nbu,", "with the Ginza §192 (12.1: Nbu,"),
    ("on the structure of 5.4 and 6 it is", "on the structure of 13.4 and §14 it is"),
    ("The letters do not yet meet it: 3.4 gives", "The letters do not yet meet it: 11.4 gives"),
    ("the constraint test of 3.5a.", "the constraint test of 11.5a."),
    ("On the reading of 3.4, before any test,", "On the reading of 11.4, before any test,"),
    ("is for the test of 3.5a.", "is for the test of 11.5a."),
    ("3.1d marks each step.", "15.2 marks each step."),
    ("3.1d–3.1e mark it and set out its test.", "15.2–15.3 mark it and set out its test."),
]
for a, b in XR:
    if a in nb: nb = sub1(nb, a, b)
    elif a in nb7: nb7 = sub1(nb7, a, b)
    elif a in commission: commission = sub1(commission, a, b)
    else: raise SystemExit("xref not found: " + a)
nb = nb.replace("(the author, 19:51: ", "(the author, 2026-11-10: ")

# the frame sentence of the notebook becomes 9.0
frame = "9.0. The author's frame (2026-11-10): \"the planets are the gods… revelation separates the seven lampstands and messengers from the seven churchs. the messengers are the senders, the churches are the receivers, and the logos speaks thru the station of each planet in turn… these are powers of the air, fallen or distorted, and this is the formula for bringing that distortion back into correct relation. but it doesn't dissolve the seven: it purifies.\" The syntax of the letters refines the first clause (11.1a): the messenger is the station addressed, and the speaker sends through it.\n\n"
nb = nb.replace("## 9. Philo: the planets are gods, the lampstand is the seven, the seventh is the Logos\n\n",
                "## 9. Philo: the planets are gods, the lampstand is the seven, the seventh is the Logos\n\n" + frame, 1)
nb = nb.replace("(the author, 20:00: ", "(the author, 2026-11-10: ")
nb7 = nb7.replace("The author, 20:00: ", "The author (2026-11-10): ")
nb7 = nb7.replace("(search of 2026-11-10; the author, 19:59: \"we need to do a thorough search for work connecting philo and revelation\")", "(searched 2026-11-10)")
commission = commission.replace("(the author, 20:20: ", "(the author, 2026-11-10: ").replace("The author, 20:20: ", "The author (2026-11-10): ")

commission_head = "## 15. The commission\n\nThe third task: whether the architecture of Parts I and II also authorizes further writing. The book's own grammar is read first (15.1), each crossing between agents is marked (15.2), and the downstream sequence the hypothesis needs is set out on the seated text (15.3).\n\n"

OUT = H / "EA-MIDST-01-v1.0.md"
head = (H / "head.md").read_text(encoding="utf-8")
tail = (H / "tail.md").read_text(encoding="utf-8")
bridge = (H / "bridge.md").read_text(encoding="utf-8")
spxi = (H / "spxi.md").read_text(encoding="utf-8")
i0 = head.index("## 0. Provenance")
head = head[:i0] + spxi.strip() + "\n\n" + head[i0:]
body = head + "# Part I. The Logos named, impressed and lived\n\n" + part1 + bridge + nb + "# Part III. The commission\n\n" + commission_head + commission + "# Part IV. The filing\n\n" + nb7 + "\n" + tail
for a, b in [("(2026-11-10 19:29)", "(2026-11-10)"), ("The author's frame (19:47)", "The author's frame (2026-11-10)"), ("the author's reading (20:20)", "the author's reading (2026-11-10)")]:
    body = body.replace(a, b)
body = re.sub(r"\n{3,}", "\n\n", body)
OUT.write_text(body, encoding="utf-8")
(H / "CHANGES.json").write_text(json.dumps(CHANGES, ensure_ascii=False, indent=1), encoding="utf-8")
print(OUT, len(body))
