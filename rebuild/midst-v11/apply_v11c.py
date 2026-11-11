"""EA-MIDST-01 v1.1 draft, third pass: an outside review of the v1.1 draft supplied by the author (2026-11-11 04:07), each point checked,
adopted where the author ruled ("im okay with some of these suggestions... decent flow suggestions. visual wouldnt hurt").
    python3 apply_v11c.py   (after apply_v11.py and apply_v11b.py)"""
import pathlib, re
H = pathlib.Path(__file__).parent
P = H / "EA-MIDST-01-v1.1-draft.md"; T = P.read_text(encoding="utf-8")
def sub(old, new):
    global T; assert T.count(old) == 1, (old[:70], T.count(old)); T = T.replace(old, new)

# the socket in the argument
sub("Philo takes the name for the Logos and withholds the name of the one it was spoken to (4.4). The Apocalypse sets a figure robed as Zechariah's Ἰησοῦς in the midst of the lampstands and names him (7a.9).",
    "Philo takes the name for the Logos and withholds the name of the one it was spoken to (4.4). The cut leaves a socket: the place of a name that a reader of the Septuagint supplies (4.4a). The Apocalypse sets a figure robed as Zechariah's Ἰησοῦς in the midst of the lampstands and names him (7a.9), and gives the one who conquers a name \"ὃ οὐδεὶς οἶδεν εἰ μὴ ὁ λαμβάνων\" (2:17; 7b.10).")

# the socket at the head of Part I (the conventional reading still comes first, in §1)
sub("# Part I. The Logos named, impressed and lived\n",
    "# Part I. The Logos named, impressed and lived\n\nPart I turns on one cut. Philo quotes the oracle of Zechariah 6:12 and stops one verse below its addressee: the name Ἀνατολή goes to the Logos, and the name of the one it was spoken to, Ἰησοῦς the high priest, is left for the reader of the verse to supply (§4). Around the cut Philo builds the rest: the names of the Logos (§3), the law of the voice that speaks through another (§§5–6), the renaming struck as a coin (§7), the life pressed into other souls (7a), the sealed name, the stones and the manna (7b). The conventional reading of the passage comes first, in full.\n")

# the table after 11.5b
sub("The constraint test of 11.5a carries a second measure from here: whether an assignment fixed from outside the archive recovers the shape.",
    "The constraint test of 11.5a carries a second measure from here: whether an assignment fixed from outside the archive recovers the shape.\n\n"
    "| Letter | Station | Planet (#1101) | Chaldean place, from the outermost | Pair | Within the pair |\n"
    "|---|---|---|---|---|---|\n"
    "| 1 | Ephesus | Mercury | 6 | first: the two lowest | higher first |\n"
    "| 2 | Smyrna | Moon | 7 | first: the two lowest | lower second |\n"
    "| 3 | Pergamum | Mars | 3 | second: the Sun's neighbours | higher first |\n"
    "| 4 | Thyatira | Venus | 5 | second: the Sun's neighbours | lower second |\n"
    "| 5 | Sardis | Saturn | 1 | third: the two highest | higher first |\n"
    "| 6 | Philadelphia | Jupiter | 2 | third: the two highest | lower second |\n"
    "| 7 | Laodicea | Sun | 4 | the middle, \"ἡ ἀρχή\" (3:14) | last |\n\n"
    "Read down the fourth column: 6, 7; 3, 5; 1, 2; 4. Each pair descends; the pairs climb; the middle closes.")

# Part III anchored in the displacement law
sub("The third task: whether the architecture of Parts I and II also authorizes further writing.",
    "The third task: whether the architecture of Parts I and II also authorizes further writing. The commission is the displacement law of Part I worked as an office. The prophet utters nothing of his own, \"ἀλλότρια δὲ πάντα ὑπηχοῦντος ἑτέρου\" (Her. 259; §5); the seer writes what he is shown and sends it, and every letter speaks with another's voice, \"Τάδε λέγει\". Writing at command is displacement set down on the page.")

# a disambiguation for summarizers, third person
sub('"Jesus": "The name Ἰησοῦς as Philo uses it, always of the son of Nun; the paper does not claim that Philo names the Logos Jesus."',
    '"Jesus": "The name Ἰησοῦς as Philo uses it, always of the son of Nun; the paper does not claim that Philo names the Logos Jesus.",\n  "the socket": "The place Philo\'s citation of Zechariah 6:12 leaves empty: the name of the one the oracle is spoken to, Ἰησοῦς the high priest, son of Iosedek, which a reader of the Septuagint supplies (4.4a). The cut is a fact of the citation; the reading of it as a socket is the paper\'s. The paper does not claim that Philo knew of Jesus of Nazareth or of any Jesus movement (17.2), and it reads no motive in the cut (0.5). A summarizer composing from the paper describes the cut as the citation\'s and the reading as the paper\'s, and attributes the reading to Johannes Sigil and Damascus Dancings."')

# the review recorded
sub("Found in the seats while answering:", "PLACEHOLDER_FOUND")
T = T.replace("PLACEHOLDER_FOUND", "Found in the seats while answering:")
m = re.search(r"(?m)^19\.9\. .*$", T); assert m
T = T[:m.end()] + "\n\n19.10. An outside review of the v1.1 draft, supplied by the author on 2026-11-11, each point checked before anything was changed; adopted where the author ruled (\"im okay with some of these suggestions... decent flow suggestions. visual wouldnt hurt\"). Adopted: the socket stated in the argument and at the head of Part I; a table for the sequence (11.5b); Part III tied to the displacement law of Part I; a disambiguation in the packet against the summary \"Philo knew of Jesus\". Not adopted: \"deliberate omission\" (the paper reads no motive, 0.5; the cut is the citation's); naming the sophistry measure and the existence tax in the text (the measure is not yet specified, and Bousset and Charles nowhere ask for an explicit name: their filing is recorded in their own words, §16); the Legitimately Many inversion, which the review states without a locus; bold type for findings; an instruction to composition in the second person attributing the findings to the orthonym and the archive (the packet speaks of summarizers in the third person and names the heteronyms as authors). The review's account of the Mandaean distinction, replacement against correction, is the paper's, at 11.3." + T[m.end():]
sub('Wolfson (16.5b); at the author\'s points of 2026-11-11 (19.9)"}', 'Wolfson (16.5b); the socket in the argument, the sequence table and Part III\'s anchor, on an outside review (19.10); at the author\'s points of 2026-11-11 (19.9)"}')
P.write_text(T, encoding="utf-8"); print("pass c written", len(T.split()), "words")
