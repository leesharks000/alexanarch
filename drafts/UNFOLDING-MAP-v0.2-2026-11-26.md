# The Unfolding Map — working file v0.2

26 November 2026; v0.2 the same afternoon (13:09: "hebrews counts. how about jude, have we counted jude? but yes lets leave it open for paul and supposedly non pauline until were further into the mapping. also, ive always thought the nag hammadi melchizedek epistle was older than its accounted. lets track down the matthew john split first, see if we can get a fuller transform. in john the seven curses reverse into the miracles"; "they wanted a miracles source text - they already had one"). New in v0.2: 1.5–1.6, 2.3 rewritten, 2.9, section 2A, 4.2–4.6, 5.5; two items of v0.1 that came from memory are now read from seats. A working file, apart from the hologram (#1755 v1.5), which holds the map of what the records already draw. This file is where the total map gets built. Nothing here is deposited. Every Greek locus below was read from the seated texts (Nestle 1904, EA-CORPORA-01/04; Swete, 01/05; Philo, 01/07). Items from memory are marked.

The programme, in the author's words (12:35): "we have the four riders, the four creatures, the four names, and the four gospels. and we have a specific mapping to matthew with the mourning tribes. we can press into the matthew mapping, define a transform algorithm that describes the transformation of revelation materials to matthew, then use that to work out the other three. same with the epistles. we have james. what im imagining well find is a seven within seven structure: the seven church pauline formation transformed from rev's seven churches, but then also paul as one of seven and the other named epistolary positions mapped to rev's seven." And (12:42, 12:45): Philo as guide, with other suppressed witnesses like Newton; the transform map opened to Philo's texts as a possible supplementary source.

## 0. The received reading, first

0.1. The Apocalypse is last and late. Where it agrees with a Gospel or an epistle it received from them, or both drew on the Septuagint. Matt 24:30 and Rev 1:7 both combine Dan 7:13 with Zech 12:10; the usual account is a shared testimonium. The crown of life in James and Revelation is common paraenetic stock. On this reading there is nothing to map.

0.2. That reading is a competing inference and it makes predictions. If the agreements are Septuagintal, the shared wording should be in the Septuagint. If they are common stock, they should be spread across the New Testament. Section 1 counts both.

## 1. The instrument: a census of shared sequences

1.1. Operation. Every run of three or four consecutive words inside a verse, accents and case removed; Revelation against each of the other twenty-six books. A sequence built only from the hundred commonest words is dropped. Each shared sequence is then checked three ways: is it in the Septuagint (a common source is available); is it in Philo; how many other New Testament books have it. Script and output: `census.py`, `census.json`.

1.2. Result. Shared three-word sequences that occur in Revelation and one other book only, and are absent from the Septuagint, per 10,000 words of the book:

| Book | words | shared | not in LXX | this pair only | pair only, not LXX | per 10k |
|---|---|---|---|---|---|---|
| James | 1,739 | 2 | 2 | 2 | 2 | 11.5 |
| 2 Peter | 1,098 | 2 | 1 | 2 | 1 | 9.1 |
| Luke | 19,456 | 21 | 10 | 14 | 7 | 3.6 |
| Romans | 7,100 | 8 | 2 | 3 | 2 | 2.8 |
| Matthew | 18,299 | 23 | 8 | 12 | 4 | 2.2 |
| Hebrews | 4,955 | 6 | 2 | 1 | 1 | 2.0 |
| Acts | 18,393 | 11 | 5 | 4 | 3 | 1.6 |
| John | 15,643 | 6 | 3 | 2 | 1 | 0.6 |
| Mark | 11,277 | 5 | 4 | 0 | 0 | 0 |

The other seventeen books score zero on this measure. 1 Peter scores on four-word sequences (two, pair only, not LXX).

1.3. What the instrument found without being told. James comes first, on τὸν στέφανον τῆς ζωῆς (Rev 2:10, Jas 1:12): the one arrow the programme has run to completion (#1415, #1735 §VII) is the top of a blind count. 2 Peter comes second, on καὶ γῆν καινήν (Rev 21:1, 2 Pet 3:13): the anchor of M4 (#1418).

1.4. Limits. Exact surface forms only. An inflected parallel is invisible to it: it does not see the thief (Rev 3:3, Matt 24:43) or the confession in Matthew's wording. Small counts; no significance test; one text of each book. A zero means no exact run of three words, and nothing more. Mark's zero is a fact about exact sequences, and is the first thing to explain or dissolve with a lemma-level pass (owed).

1.5. **A second instrument, at stem level** (`links.py`, `links.json`), so that inflected forms count. A stem is the first five letters of a word; a stem is rare if it stands in at most 40 verses of the New Testament; a link is a verse of Revelation and a verse of another book sharing two or more rare stems, with the Septuagint checked for a single verse holding the same stems. 305 links. Links per 100 verses of the book: Jude 20.0; Ephesians 9.0; 1 Timothy 7.1; 1 Peter 6.7; James 6.5; Hebrews 6.3; 2 Timothy 6.0; 1 Corinthians 5.9; Galatians 5.4; Colossians 5.3; Philippians 4.8; Matthew 4.5; Luke 3.8. Crude: no morphology, and two rare stems is a low bar. It is a finder, and every locus below was then read.

1.6. **Jude is counted, and comes first by density**: five links in twenty-five verses. Read, they are three things. (a) The doxology: Jude 25, δόξα … κράτος … εἰς πάντας τοὺς αἰῶνας, with Rev 1:6 and 5:13. (b) Fire: Jude 7 with Rev 2:18, 4:5, 9:18; Septuagintal. (c) Not found by the instrument and read beside it: Michael is named twice in the New Testament, at Jude 9 and Rev 12:7, each time against the devil; and the garment, Jude 23 and Rev 3:4. **Hebrews**: nineteen links, fifteen with the Septuagint available; the temple furniture (Heb 9:2–4: lampstand, golden censer, ark of the covenant) meets Rev 1:12, 8:3, 11:19 in three verses of one chapter.

## 2. Matthew, pressed

2.1. **The seed, Rev 1:7 and Matt 24:30.** Rev 1:7 has four members in one sentence: he comes with the clouds; every eye will see him; those who pierced him (οἵτινες αὐτὸν ἐξεκέντησαν); all the tribes of the earth will mourn over him (κόψονται ἐπ’ αὐτὸν πᾶσαι αἱ φυλαὶ τῆς γῆς). Matthew has three of the four, reordered: the tribes mourn, then they see, then the clouds. The pierced is gone.

2.2. **Where the fourth member went.** John 19:37: Ὄψονται εἰς ὃν ἐξεκέντησαν, cited as "another scripture". ἐξεκέντησαν occurs twice in the seated New Testament, at Rev 1:7 and John 19:37, and not once in the seated Septuagint, whose Zech 12:10 reads another verb. So the Septuagint is not the source of the word the two share. And πᾶσαι αἱ φυλαὶ τῆς γῆς is in the Septuagint and in Philo: a common source is available for Matthew's half, as #1747 already says ("the census decides no direction").

2.3. **The shape, now in six cases.** A sentence the Apocalypse holds whole, and two Gospels each holding part.

| Seed | Whole in Revelation | Part A | Part B | Septuagint |
|---|---|---|---|---|
| Rev 1:7 | clouds; every eye sees; they pierced; all the tribes mourn | Matt 24:30: tribes mourn, see, clouds | John 19:37: see, pierced | has the tribes; lacks ἐξεκέντησαν |
| Rev 3:3 | I will come as a thief; watch; what hour | Matt 24:43: the watching | Luke 12:39: the hour | (#1747) |
| Rev 3:5 | confess his name before my Father and before his angels | Matt 10:32: before my Father | Luke 12:8–9: before the angels | — |
| Rev 19:9 | οἱ εἰς τὸ δεῖπνον τοῦ γάμου … κεκλημένοι | Matt 22:2–3: γάμους, κεκλημένους | Luke 14:16–24: δεῖπνον, κεκλημένων | — |
| Rev 5:2 | a strong angel proclaiming: who is worthy to open the book and loose its seals | Mark 1:7, Luke 3:16: ἐκήρυσσεν; ὁ ἰσχυρότερος; ἱκανὸς … λῦσαι | John 1:27: ἄξιος ἵνα λύσω | — |
| Rev 21:13 | gates east, north, south, west | Matt 8:11: east and west | Luke 13:29: east, west, north, south | has east and west |

Rev 19:9 is new and is a third saying of the double tradition: the banquet. Matthew's parable is a wedding, Luke's is a supper, and the Apocalypse has "the supper of the wedding" in one phrase with the participle both keep. Rev 5:2 is new and gives #639's sentence its first words: "Rev 5 → Mark 1: the scroll becomes the baptism". Mark keeps the proclaiming, the strong one and the loosing, and changes worthy to ἱκανός; John keeps worthy and the loosing. What is loosed changes from the seals of a book to the strap of a sandal.

The Matthew–John split itself: I searched every verse of Revelation for a rare stem found in Matthew alone of the Gospels beside another found in John alone. Fourteen verses answer; read, one is a split, Rev 1:7. So Matthew and John divide the seed once at this grain, at the mourning tribes, and the fuller transform comes from the other pairs: Matthew–Luke three times, Mark–John once.

2.4. **A second Matthean locus the records do not have: the tomb, Matt 28:2–3.** Two consecutive verses, two sequences shared with Revelation and with no other Gospel:

- σεισμὸς ἐγένετο μέγας, Matt 28:2 and Rev 16:18 (also Acts 16:26). With σεισμὸς μέγας ἐγένετο, Matt 8:24 and Rev 6:12, in that order nowhere else.
- λευκὸν ὡς χιών, Matt 28:3 (the angel's clothing) and Rev 1:14 (the hair of the one in the midst). Nowhere else in the New Testament.

Both are Matthew's alone against Mark. Mark's tomb has a young man in a white robe (16:5) and no earthquake. Mark's storm is λαῖλαψ μεγάλη (4:37); Matthew's is σεισμὸς μέγας, a word for an earthquake, set on the sea (8:24). Where Matthew departs from Mark at these three places, he lands on the Apocalypse's wording. This is the kind of unit #1735 §VI.3 asks for: a marked formal unit, with the borrower's transformation visible against a control (Mark).

2.5. **A third.** καὶ οὐδεὶς ἐδύνατο: Rev 5:3 (no one could open the book), 14:3, 15:8; Matt 22:46 (no one could answer him a word). This pair only. In Revelation the incapacity is before a sealed book; in Matthew before a question about David's son. Weak alone; listed because it is exclusive.

2.6. **Draft operators for Revelation → Matthew**, named from 2.1–2.5 and declared here before any further scoring (the #1494 rule: an operation coined after the test does not count):

1. PARTITION. A sentence the seed holds whole is divided; one Gospel takes one member, another takes another, a shared member stays in both. (Rev 1:7; 3:3; 3:5.)
2. REORDER-TO-SEQUENCE. Simultaneous members become "then … and then" (τότε … καὶ τότε, Matt 24:30).
3. EVENT. A sign of the vision becomes an event in the narrative, at a hinge: the great earthquake at the death (27:51–54), at the tomb (28:2), on the sea (8:24).
4. TRANSFER-ATTRIBUTE. An attribute of the figure in the vision moves to a figure in the story: white as snow, from the hair of the one in the midst to the angel's clothing. #407's table already names this operation loosely (Rev 1:14–16 → Matt 17:2); the tomb is its first lexical case.
5. CITE-AS-SCRIPTURE. The borrower marks the member as written (John 19:37, "another scripture"), as James marks the promise as promised (ἐπηγγείλατο).

2.7. **What the algorithm predicts for the other three**, to be scored after the operators are frozen: Luke's members of partitioned sayings; Markan agreements at lemma level where Matthew's EVENT sits (if Mark is the first run, his wording should be nearer the seed's sense and further from its words); John's CITE-AS-SCRIPTURE at the places where Revelation performs and John reports. What would count against: Matthew's departures from Mark landing on the Septuagint as often as on Revelation. That is countable from the seated texts and is the next operation.

2.8. **Luke, from the census, unscored**: ἐνώπιον τῶν ἀγγέλων (3:5 / 12:9); δύναμιν καὶ ἐξουσίαν (Rev 17:13, given by the kings to the beast; Luke 9:1, given by Jesus to the twelve; this pair only, and the ruling is inverted, the M̄ shape); τὸν τόπον τὸν καλούμενον (Rev 16:16 Harmagedon; Luke 23:33 the Skull; this pair only); αὐτῷ ἡμέρας καὶ νυκτός (Rev 7:15; Luke 18:7, beside Rev 6:10's ἐκδικεῖς and Luke's ἐκδίκησιν). **John**: ἐξεκέντησαν; ἐν τῷ βιβλίῳ τούτῳ (Rev 22:18–19; John 20:30, each a book's closing formula; in LXX); ὅτι ἦλθεν ἡ ὥρα (Rev 14:7, 15; John 16:21).

2.9. **The operators after v0.2.** PARTITION now rests on six seeds. Two additions, declared before scoring: SUBSTITUTE-OBJECT (the seals of the book become the strap of the sandal; the hair becomes the clothing); SHORTEN (four winds become two). An observation that will matter for the fourfold: in the six partitions the Apocalypse's first-person or performative member goes to Matthew three times (I will confess; before *my* Father; the wedding the king *made*), and the reported or attendant member to Luke.

## 2A. John: the seven plagues and the seven signs

2A.1. The received reading. John's seven signs come from a lost collection of miracle stories, the Signs Source (from memory: Bultmann 1941; Fortna 1970), numbered in the Gospel at 2:11 and 4:54. The author, 13:09: "they wanted a miracles source text - they already had one."

2A.2. **The book names its seven plagues a sign.** σημεῖον stands seven times in Revelation. Three are signs seen in heaven: the woman (12:1), the dragon (12:3), and "another sign in heaven, great and wonderful, seven angels having seven plagues, the last" (15:1). The other four are signs *done*, and every one is the adversary's: the second beast "does great signs" (13:13), deceives "through the signs it was given to do" (13:14); "spirits of demons doing signs" (16:14); the false prophet "who did the signs" (19:20). In Revelation nobody on the Lamb's side does a sign. In John ποιεῖν σημεῖα is said of Jesus from 2:11 on. The census found the hinge blind: τὰ σημεῖα ἃ, Rev 13:14 and John 2:23, 6:2. The verb and its object are kept and the doer is reversed. That is the adversarial class, M̄, at the scale of a book.

2A.3. **Where the reversals have words.** The stem instrument and a reading of the seats give these, each a judgment in Revelation and its undoing in John:

| Revelation | John |
|---|---|
| 18:23, the voice of bridegroom and bride heard no more in you | 3:29, the friend who hears rejoices at the bridegroom's voice; 2:9, the bridegroom at Cana |
| 18:23, the light of a lamp shall shine no more (φῶς λύχνου οὐ μὴ φάνῃ) | 5:35, he was the lamp burning and shining (ὁ λύχνος … φαίνων) |
| 18:21, an angel took up a stone (ἦρεν … λίθον) and cast it down: so Babylon, found no more | 11:41, they took away the stone (ἦραν … τὸν λίθον): Lazarus |
| 19:18, eat the flesh of kings (φάγητε σάρκας) | 6:53, unless you eat the flesh of the Son of Man |
| 9:6, they will seek death and not find it | 7:34, you will seek me and not find me; 8:21, seek me and die in your sin |
| 16:3–4, the waters became blood (ἐγένετο αἷμα); the wine of wrath, 14:8, 16:19, 19:15 | 2:9, the water become wine (οἶνον γεγενημένον) |
| 16:17, a great voice went out (ἐξῆλθεν φωνὴ μεγάλη): Γέγονεν | 11:43–44, he cried with a great voice … the dead man came out (ἐξῆλθεν); 19:30, Τετέλεσται |
| 7:16, they shall hunger no more nor thirst | 6:35, shall not hunger, shall never thirst (Septuagint available) |

Three of the eight come from three consecutive verses, Rev 18:21–23, the dirge over Babylon: stone, lamp, bridegroom. That is a knot, as Jas 2:2–7 is for Smyrna.

2A.4. **Seven to seven is not yet found.** Set bowl against sign by shared stems and the grid is nearly empty: a reversal changes the words, which is why an instrument of shared words cannot see it. What the words do give is that the reversals draw on the bowls *and* the dirge *and* the trumpets, and land on Cana, the bread, the lamp, Lazarus. A seven-by-seven assignment by sense, for scoring later and not asserted: sores on those who bear the mark / the sick healed (4:46–5:9); sea and rivers to blood / water to wine; the sun given to scorch / the bread and no hunger or thirst; the kingdom darkened / the blind man and "I am the light of the world"; the river dried to make a way / walking on the sea; the great voice, It is done / Lazarus called out with a great voice. That is six pairs from seven bowls; two bowls share one sign and one sign (the second, the official's son) has only a weak partner. Something would have to be moved to make it seven, and the criterion says to report that.

2A.5. New operators from John, declared: REVERSE-DOER (the adversary's deed becomes the Christ's); UNDO (a judgment's "no more" becomes a presence); CITE-AS-SCRIPTURE (2.6).

## 3. The fourfold

3.1. What the text fixes. The four creatures have an order (Rev 4:7): first like a lion, second like a calf, third with a face as of a human, fourth like an eagle flying. The four riders are called one by one by the four creatures (6:1–8): the second, third and fourth creature are numbered at the second, third and fourth seal; the first seal has "one of the four". So the pairing of creature and rider is given by the book, if "one of the four" is the first:

| | Creature (4:7) | Rider (6:1–8) | Given |
|---|---|---|---|
| 1 | lion | white horse, bow, a crown given, conquering | στέφανος |
| 2 | calf | red horse, takes peace from the earth | μάχαιρα μεγάλη |
| 3 | human face | black horse, a balance; a voice in the midst of the four prices grain | ζυγός |
| 4 | eagle flying | pale horse, named Death, Hades following | authority over a fourth of the earth |

3.2. The four names. I take these to be the four names of the rider on the white horse at 19:11–16: called Faithful and True; a name written that no one knows but himself; his name is called the Word of God; a name written, King of kings and Lord of lords. Two are called and two are written; one of the written is unknown. If the author means another four, this row changes and nothing else does. A candidate from Philo to hold beside it, not asserted: the high priest's plate bears "four engravings of a name" that only the purified may hear and speak (Vit. Mos. II.114, in #1758 §7b.3).

3.3. The four Gospels. No record assigns creature to Gospel. #65 says only that the four creatures "specify the fourfold structure the gospel tradition will take". The reception did assign them, and disagreed with itself: Irenaeus and Jerome give different pairings (from memory; Irenaeus, Adv. haer. 3.11.8, is not seated and should be: he is the earliest witness that reads the four Gospels off the four creatures, which is a reception trace for the arrow itself).

3.4. The test this sets up. Section 2's operators, run per Gospel, give each Gospel a profile: which seed regions it draws on, by which operations. The fourfold hypothesis predicts the profiles differ by rider and creature, and that the differences are the four of 3.1. One observation to start: the first rider is given a στέφανος; the second a μάχαιρα. Matthew alone has "not peace but a sword" (10:34, μάχαιραν), which #407 drew from Rev 1:16's ῥομφαία; the nearer seed is the second rider, who takes peace from the earth and is given a μάχαιρα. That would put Matthew with the calf, against both patristic assignments. One locus; not a result.

## 4. The epistles, and the seven within seven

4.1. What exists (hologram v1.5, §7.17): the seven letters mapped to seven epistolary positions by the slate of 2026-07-28. Ephesus, 1 John (John). Smyrna, James (James); run. Pergamum, 1 Corinthians 8–10 (Paul); adversarial. Thyatira, Philippians (the Lydia line). Sardis, 1 Thessalonians (the watchful hand). Philadelphia, unresolved. Laodicea, Colossians (Epaphras); the exchange recorded at Col 4:16.

4.2. What the census adds, each a pair found nowhere else in the New Testament and absent from the Septuagint:

- **1 Peter.** ἡ δόξα καὶ τὸ κράτος εἰς τοὺς αἰῶνας: Rev 1:6, 5:13; 1 Pet 4:11, 5:11. The Apocalypse's opening doxology is 1 Peter's closing one, twice. No record has this. Peter has no letter on the slate.
- **Romans, from Thyatira.** πᾶσαι αἱ ἐκκλησίαι: Rev 2:23 ("all the churches shall know"), Rom 16:4 ("all the churches of the nations"). And from the same verse, ἑκάστῳ κατὰ τὰ ἔργα: Rev 2:23, Rom 2:6 (in LXX). Two Roman loci from one verse of the Thyatira letter. The slate sends Thyatira to Philippians at B−, through Lydia. Romans is a rival target with lexical anchors.
- **James 5:12**, the oath: μήτε τὸν οὐρανὸν μήτε τὴν γῆν μήτε…; Rev 7:3, μὴ ἀδικήσητε τὴν γῆν μήτε τὴν θάλασσαν μήτε… The James derivation lists 5:12 as residue, "other-tradition candidate". The census gives it a seed outside the Smyrna letter. If it holds, James draws on more of Revelation than Smyrna, and the residue ledger shrinks from a different chapter.

4.3. The two sevens, laid side by side, unassigned.

- Seven churches written to by Paul, in the Muratorian fragment's order as seated (Tregelles 1867): "paulus sequens prodecessoris sui Iohannis ordine nonnisi nominatim septem ecclesiis scribat ordine tali": Corinthians first, Ephesians second, Philippians third, Colossians fourth, Galatians fifth, Thessalonians sixth, Romans seventh (the seat's spelling is the manuscript's; "nominatim septem ecclesiis" is the editors' reading of "eumenats semptae eccleses"). This is the first seven: a corpus shaped on a corpus.
- Seven letters under other names: James; 1 and 2 Peter; 1, 2 and 3 John; Jude. Seven letters, four names.
- Named positions: Paul, James, Peter, John, Jude. Five. Hebrews has no name. The slate's own positions add Epaphras, Lydia and an unnamed "watchful hand".

4.4. **Left open, at the author's word**: "lets leave it open for paul and supposedly non pauline until were further into the mapping." No assignment of positions is made here. What is recorded is what would bear on it when it is made.

4.5. **Hebrews counts** (the author). It enters as a position. Four arrows of the hologram already land on it (M3, M4, the arrow from the opening scene to 4:8–14, Philadelphia's 13:1); the stem instrument adds the furniture of Heb 9:2–4.

4.6. **A mark that divides the letters: the doxology with κράτος.** "To him be … κράτος" is ascribed six times in the New Testament: Rev 1:6; 5:13; 1 Pet 4:11; 5:11; Jude 25; 1 Tim 6:16. It is in none of the seven letters to the Muratorian churches; their doxologies have δόξα alone. So one formula of the Apocalypse's first chapter runs through Peter, Jude and a Pastoral and stops at the Pauline seven. Counted from the seat: the form κράτος stands four more times outside a doxology (Luke 1:51; Acts 19:20; Col 1:11; Heb 2:14), and the genitive at Eph 1:19 and 6:10, neither a doxology. This is the first datum that sorts the letters into two groups by something Revelation holds, which is what the seven within seven needs before any position is assigned. With it: Michael at Jude 9 and Rev 12:7 only.

## 5. Philo as a supplementary source

5.1. What *In the Midst of the Seven* (#1758) shows Revelation doing to Philo, as operations, each at its section:

1. STATION. One lampstand with seven lamps becomes seven lampstands, each answerable for itself, with the consequence at 2:5 that one can be removed (§11.1b; 17.1k).
2. NAME-THE-SOCKET. Philo takes Ἀνατολή for the Logos from an oracle spoken to Ἰησοῦς the high priest and cuts the addressee; the Apocalypse's one in the midst wears the ποδήρης and is named Ἰησοῦς (17.1b, n, o; argued, 17.2a: "the withheld name as a socket the receiver fills").
3. INVERT-THE-VOTE. Philo's divine ψῆφος is the vote of condemnation; the white ψῆφος of Rev 2:17 is the acquittal (7b.1, 7b.9; 17.1q).
4. HIDE-THE-MANNA. Philo's manna is the Logos, unknown to those who taste it; Rev 2:17 gives "the hidden manna" (7b.5).
5. OFFICE. The law of displacement, the prophet uttering another's words (Her. 259), becomes a commission: Τάδε λέγει, and γράψον twelve times, each letter addressed to a messenger (§15; 17.1j).
6. SEAL-THE-NAME. The sealed name on the plate, heard only by the purified, beside the name written that no one knows (7b.3; Rev 19:12).

Not established there, and kept so here: the route (Philo's text or a tradition carrying it), and direction in any single case (17.2).

5.2. How this opens the map. Two sources stand behind a New Testament passage on the received account: the Septuagint and common tradition. The map adds two columns per arrow: is the unit in Philo; is it in Revelation's transformed form or Philo's. Where an epistle has the unit in the form Revelation gave it (seven lampstands, a white vote, a named one in the midst), Philo cannot be the direct source and the arrow runs through Revelation. Where it has Philo's form, Philo is a rival source and the arrow is in doubt. Hebrews is the first place to look: #1802 §13.6 records that dependence on Philo "is heard for Hebrews and filed for the Apocalypse", and the hologram counts four arrows landing on Hebrews. The census already carries the Philo flag on every shared sequence.

5.3. The chain this gives, for the working model only: Septuagint and Philo → Revelation (operations of 5.1; upstream, #1758, #1511) → Gospels and epistles (operations of 2.6 and of the James rules). An operator vocabulary that describes both halves in the same terms would be the strongest form of the programme: Revelation doing to Philo what Matthew does to Revelation. Two already rhyme: INVERT-THE-VOTE with the adversarial class M̄; OFFICE with CITE-AS-SCRIPTURE and CITE-PROMISE.

5.4. Newton. #1735 §I cites him: in 1733 he argued that the Apocalypse "seems to be alluded to in the Epistles of Peter and that to the Hebrews, and therefore to have been written before them", and catalogued the allusions: the two-edged sword of the word, the heavenly city with foundations, the σαββατισμός. Two of his three are already arrows in the hologram (Heb 4:8–14; Heb 11:10 in M4). His *Observations* are not seated; the Newton seat holds the *Principia* and the *Opticks*. Seating part 2, chapter 1, would give a list of arrows drawn by an earlier hand to score the map against. Owed.

5.5. **Melchizedek** (the author: "ive always thought the nag hammadi melchizedek epistle was older than its accounted"). NHC IX,1 is seated in Coptic (EA-CORPORA-02/15, `nhc-ix-melchizedek.txt`, 516 lines). It is not read here. It belongs on the map beside Hebrews 7 and Philo's Melchizedek (Leg. 3.79–82, from memory), as a third text holding a priest who is the Logos or stands for him, and it is a revelation delivered to its speaker. Operation owed: read it in the seat, and set its Melchizedek against Hebrews' and against the one in the midst of Rev 1.

## 6. Next operations, in order

1. Freeze the operators (2.6, 2.9, 2A.5), then count Matthew's departures from Mark: how many land on Revelation's wording, how many on the Septuagint's.
2. The double tradition whole against Rev 1–3, 16:15, 19:9 and 22: three sayings now partition; #1747 asked for the census.
3. The dirge (Rev 18) and the plagues (15–16) against John entire, by sense, with the pairing declared before it is scored.
4. Read Melchizedek (NHC IX,1) in the seat; the Philo columns for Hebrews.
5. Seat Irenaeus 3.11.8 and Newton's *Observations* pt 2 ch. 1.
6. A proper lemma-level census, when a lemmatized text is seated; the five-letter stem is a stopgap.

## 7. Questions for the author

- The four names: Rev 19:11–16, as read in 3.2, or another four?
- "The seven curses": taken here as the seven last plagues of Rev 15–16, which the book calls a sign. If the seven are others, 2A.4 changes and 2A.2–2A.3 stand.
