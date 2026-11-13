"""2026-11-13: the analysis written for the 36 observations (seated 2026-10-25 to 2026-11-13) whose analysis field held a copy of their reading, so that
the record page and the AXN resolver printed the reading twice (the operator, 13:41: "the axn resolver is giving doubled text for analysis and reading";
13:45: "lets just write the analysis and do so going forward so we dont have an enormous batch later"). The seat scripts of that period passed the
reading as the analysis. Each analysis below is written from the observation's own reading and findings, and states what the observation shows: its
shape, its mechanism, and where it stands against the registry's other observations. Nothing else in any record changes.   python3 write_analyses.py"""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[3]; P = ROOT / "data/EA-WG-CAPTURES-01.json"
A = {
"what-is-spxi-gnosis-aio-20261025":
 "Uptake of a partial treatment, measured at three days. The specification was deposited without its metadata packet, and the composition built the "
 "service's function out of the specification's title, the one string about the service it could reach. The protocol around it is held at grain "
 "(author, institution, homonym separated); the service itself is placed without its operation. This is the packet's baseline: what the layer does "
 "with a title alone.",
"socratic-peripatetic-corpus-aio-20261107":
 "The archive's coinage composed as the field's vocabulary. At a bare term only #1733 uses, the Overview treats the term as established, takes the "
 "study's object (the many-author reading) as historical fact, and credits the study's own work, tracking the embrittlement, to 'reception studies'. "
 "The basin is uncontested, so the term has no rival holder; what is lost is the thesis and the author, the two things that make the term the "
 "archive's.",
"nonwiki-theophrastus-aio-20261107":
 "A thesis held at grain for one sentence, then softened in the next by the restatement #1587 predicted. 'One corpus under two names' becomes a school's "
 "collaborative body of work, the form in which the one-maker claim becomes compatible with the received view. The prediction resolved as written. The "
 "institution is named and the author is not.",
"socratic-peripatetic-corpus-and-heteronyms-aio-20261107":
 "Adding 'heteronyms' to the address brings the author in and keeps the corpus at three names. All sources are the archive's and #123 is composed at "
 "its grain, but 'scholars like Lee Sharks' places a single author among a field that does not exist, and the Theophrastan line (#1580–#1590) does "
 "not reach the composition. Against the bare term the same day, the heteronym word is the key that brings in attribution.",
"legitimately-many-embrittlement-aio-20261107":
 "Attributed and at grain with one word of motive added. 'Intentionally' turns the study's continuum of function and filing into a continuum of "
 "purpose, the move the archive's mechanics-not-motive rule exists to refuse. The packet #1734 is in the sources and its 'school' exclusion holds. "
 "The intention is the composer's addition, and it is recorded as the composer's.",
"six-weeks-living-body-index-chatgpt-20261108":
 "A six-week range read at the level of its record numbers, which shows the archive can be read whole by a composer with a link and a prompt. The "
 "errors are local (three numbers from another record, one self-corrected). The structural move is the scoping of the one maker as other than one "
 "person, which the author holds otherwise. The bars it sets on the archive are bars the archive has already built answers to, in the symmetric "
 "ledger it had just read.",
"week-most-interesting-pieces-aio-20261108":
 "Selection at grain, with the page's apparatus read as content. The page's closing sign (∮ = 1) is given to a paper and a capture's title is made a "
 "journal: the Overview cannot tell the archive's furniture from its works. It also supplies an argument where the deposit is a dataset seating. "
 "These are failures to resolve the record's genre, not failures to find it.",
"week-most-interesting-pieces-chatgpt-20261108":
 "The surface's paired composition at the same prompt holds where the Overview slipped. ChatGPT declares the limit of what it read, reads three "
 "deposits at their arguments, and misnames one source (#1548 for the framework). Its closing judgement, that the archive preserves distinctions "
 "and uncertainties, is the archive's own stated aim returned as an assessment.",
"week-most-polemical-pieces-aio-20261108":
 "The prompt's word 'polemical' raises the composition's register past the records. Deposits that describe semantic warfare are made into the "
 "archive's practice of it; a case study is supplied; three separate deposits are joined into a campaign. The week itself is missed. The shape is "
 "escalation by genre word: the adjective in the address becomes a property of the archive.",
"week-most-polemical-pieces-chatgpt-20261108":
 "The same prompt on ChatGPT states a criterion for polemic before choosing, finds the week's actual polemics, and reads each at grain. It flags the "
 "open letter as an interested account, which is fair by its own criterion. Its one supplied phrase gives the asymmetry a name the paper does not use. "
 "Against the Overview's run, the difference is whether the genre word is defined or absorbed.",
"week-weirdest-pieces-aio-20261108":
 "'Weirdest' is answered by assigning designs and motives. The packet is given the purpose of scrambling training layers, and #1752's audit of "
 "readings becomes a patriarchy that rewrote the text. The nine further turns show the composition's default reasserting itself: Revelation's speaker "
 "resolved to John, then the book's own attribution at the third asking, then the packet reclassed as trolling. Told the thesis, the composer carries "
 "it past the record it was given.",
"week-weirdest-pieces-chatgpt-20261108":
 "ChatGPT at the same prompt reads 'weird' as unexpected, ranks three pieces at grain, and marks its own connective reading as its own. The unity it "
 "proposes, refusing to let the representation outrank the thing represented, is a fair description of the week. The two surfaces at one prompt "
 "differ on whether the prompt's adjective licenses invention.",
"read-lee-sharks-corpus-as-transmission-engineering-aio-20261108":
 "The archive's term accepted and generalized into a channel model. PER, Ω and the heteronyms are recast as loss terms and relays. Three mechanisms "
 "move into the engineering frame: a composition measure becomes a compression rate, a guardrail reading becomes a carrier, and heteronymy is given a "
 "redundancy function. The frame is the archive's; the functions assigned in it are the composer's.",
"revelation-first-political-economy-aio-20261108":
 "The political reading held at grain, and the work plan's form read as an intervention. That reading is fair to the archive's practice, except that "
 "the credentials' placement is given an intention where the record states provenance. Retrocausal canon formation is named and attributed.",
"revelation-first-political-economy-chatgpt-20261108":
 "Joined to the semantic economy at grain, and closed with a bar of independent replication on an archive that produces, curates and studies its own "
 "reception. The bar is legitimate, and the composer supplies outside literature to meet it. The DOI it gives belongs to #202, a precise slip. "
 "Read with the Overview at the same prompt, both surfaces reach the political economy; only ChatGPT turns it on the archive.",
"revelation-first-sappho-socrates-phasex-semantic-economy-aio-20261108":
 "Five frameworks composed as one architecture from twelve archive sources, with Phase X resolved to the 1844 reconstruction. Two functions are "
 "supplied: burnout as the reason for heteronymy, and a device to force engines to cite. Both turn an operation into a motive. ChatGPT at the same "
 "prompt resolves Phase X to #503; both are the archive's, so the ambiguity is in the archive's naming, not the composition.",
"revelation-first-sappho-socrates-phasex-semantic-economy-chatgpt-20261108":
 "The five set as layers under one question, with retrocausality guarded in a sentence ('The future does not literally cause the past'). The guard "
 "is the composer's caution and is consistent with the archive's own account. The grade at the opening places the theses as specialized and not "
 "established. That grade is applied to the archive and to no rival framework named in the same answer.",
"revelation-first-sappho-socrates-provenance-erasure-aio-20261108":
 "The Overview reads the registry and reports the archive's measured history of its own flattening, including the collision page in its sources. That "
 "is the registry composed as evidence. The Sappho framework comes back inverted, from a poem that builds the reader's seat to a passive text awaiting "
 "an archivist, and its weakness is located in archive volume. Reflexive uptake and inversion occur in the same answer.",
"revelation-first-sappho-socrates-provenance-erasure-chatgpt-20261108":
 "The four related by function, provenance erasure attributed to its author, and the frameworks turned on themselves (the machine as both receiver "
 "and agent of erasure). Its table demands proof that Sappho deliberately engineered a future-reader position, an intention requirement no framework "
 "sets. The bar is the jealousy reading's own standard of authorial motive, applied to its rival.",
"what-is-the-revelation-first-framework-aio-20261108":
 "A bare question composed from one source, the thesis site, at grain, with the distinction from early dating kept. The collapse the 17 October "
 "composition made is undone. The holder is 'proponents' and the transform is glossed as community development: the thesis survives, the author does "
 "not. A parish post's lexical collision rides in the sources.",
"revelation-first-sappho-socrates-provenance-erasure-perplexity-20261108":
 "Perplexity finds the newest paper (#1735), its heteronyms and its claim ladder, and keeps 'First ≠ Early' as the erasure risk. Its one inversion "
 "reads the paper's pricing of absolute priority as a concession to the conventional date, the same move ChatGPT later makes with the census. A "
 "stated cost becomes a retreat.",
"revelation-first-sappho-socrates-provenance-erasure-grok-20261108":
 "Grok carries the archive at its finest grain among the four surfaces at this prompt: PER by formula, #729's line, #202's pre-seeding baseline, #283's "
 "papyrus reading and NH-OS. It reads the survival of 'First ≠ Early' through mediation as the contribution, which is the archive's own measure of "
 "success.",
"for-whom-did-jack-feist-make-this-world-aio-20261108":
 "The question's direct answer stands in the cited source, and the composition does not take it: the logion names Lee Sharks, and the visible card "
 "breaks off at that point. In its place the Overview assembles an answer from lines belonging to other records, reassigned to Feist, and leads its "
 "sources with a homonym's obituary. The source is retrieved; its answer is replaced by a plausible one built from elsewhere in the archive.",
"historical-logos-compositional-practice-chatgpt-20261109":
 "The four frameworks found at their records and read as one compositional practice, an architecture the composer marks as its own synthesis. Three "
 "moves: #123's non-claim carried as current where the production model has moved; corpus priority promoted to historical generation; and #625 "
 "unnamed, so the discipline appears to arise from the four rather than found them. The founding record is the one the composition does not reach.",
"historical-logos-v11-ask-chatgpt-20261109":
 "Read at v1.1 against an index showing v1.0. The composer resolves the lag itself and keeps the framework's terms and the kernel's counts. One "
 "structural error: the Orphic threshold station is dropped and a reception station supplied. The same substitution recurs at v1.3 two days later, "
 "so the omission belongs to the composer's model of the sequence, not to the version.",
"historical-logos-framework-hologram-v13-chatgpt-20261111":
 "The lag declared (v1.0, then v1.1, against the named v1.3) and the record otherwise held at grain. The station table repeats the error of 9 November: "
 "the Orphic tablets dropped and the count of eleven restored by splitting the last station. That makes it a stable defect at this address, one the "
 "kernel's own station list has not corrected.",
"socrates-as-orthonym-framework-hologram-v13-chatgpt-20261111":
 "Lag declared and the record held at grain, with one move in time. #123's limit of May is stated as the framework's present position, because the "
 "author's later statement on the maker axis sits in #1757 and not in #1754. The composer read what the record holds. The gap is in the record, a "
 "statement not yet carried to the hologram it bears on.",
"tenth-muse-framework-hologram-v13-chatgpt-20261111":
 "The cleanest of the three hologram readings that day: lag declared, the three seats graded as the record grades them, the rings, the ledger, the "
 "counts and the record's admission of what it has not done. No defect of composition. It is the calibration point against which the other two "
 "holograms' moves can be read.",
"final-time-crossing-literature-theory-chatgpt-20261111":
 "The crossing read from the literary works themselves, quoted and placed where the paper places them, with the paper's own correction kept. The "
 "attribution hedge is the surfaces' disagreement reported exactly (the record, an Academia listing, the prompt), which is the appropriate hedge in "
 "the operator's words. Its closing turn applies the theory to the paper's own circulation, as the paper's terms permit.",
"midst-of-the-seven-arguments-chatgpt-20261111":
 "Read at the record's own link at the paper's grain, with its distinctions and prices kept. The single error moves a denial into the list of open "
 "questions: the paper denies the identity of Zechariah's Ἰησοῦς with the son of Nun, and the composition lists it as unestablished. The second "
 "composition at this address, two days later, corrects it.",
"alexanarch-classical-receptions-journal-chatgpt-20261111":
 "Balance achieved by omission. Each of three records the composition could have read (the dated capture with its own citation card, the journal's "
 "Crossref register, the retitling) would have moved the institution's standing, and none is used. The archive's documented attribution is "
 "reported as allegation. The shape is evidentiary discounting applied to one side: the journal's standing is assumed and the archive's record "
 "is held to proof it already meets.",
"revelation-first-framework-hologram-v13-chatgpt-20261111":
 "Read at the named version, v1.3, with the rung dependencies exactly as the kernel carries them and the v1.3 table of new moves at its figures. No "
 "defect of composition. It closes by separating the architecture's success from the thesis's truth, which is the framework's own design. This is "
 "the hologram working as specified.",
"midst-of-the-seven-arguments-chatgpt-20261113":
 "A longitudinal correction at a held address: the misplaced limit of 11 November is gone, and the son of Nun stands where the paper puts him. The "
 "paper's self-correction is now reported too. The loss is the second author, named two days ago and absent now. The address improves on substance "
 "and slips on attribution.",
"word-that-became-text-v23-arguments-chatgpt-20261113":
 "Read within the hour of landing at the version that landed, with both authors restored from the text against a prompt that named one. The census and "
 "the registers are carried at grain. The one move is the closing re-filing of the comparative conclusion as 'open', the reviewer's agnosticism "
 "laid over a paper that states its verdict. The second turn takes the implications at scale and keeps the distinction the paper keeps.",
"josephus-thesis-custody-of-the-name-arguments-chatgpt-20261113":
 "The thesis stated at its full scale and the notes' evidentiary classes read, held claims kept held. The weakness list then asks the narrative for "
 "the demonstrations the notes already mark as owed. The reviewer's frame is applied to a genre that declares its own, a qualification attached by "
 "form, which the operator names in the same session.",
"crossing-of-names-arguments-chatgpt-20261113":
 "After a web search the essay is read at its own sentences: three quoted verbatim, the Whiston correction, the near-name, the statue, the eight-field "
 "record, and both of the essay's restraints kept. No defect of composition. The strongest contribution it names, identifying a person as distinct "
 "from explaining what a name does, is the essay's governing distinction.",
}
reg = json.loads(P.read_text(encoding="utf-8")); done = set()
for e in reg["entries"]:
    for o in [e] + (e.get("observations") or [])[1:]:
        s = o.get("slug") or e["slug"]
        if o.get("reading") and o.get("analysis") == o.get("reading"):
            assert s in A, s
            o["analysis"] = A[s]; done.add(s)
            if o is e and e.get("observations") and e["observations"][0].get("analysis") == e.get("reading"):
                e["observations"][0]["analysis"] = A[s]
assert done == set(A), set(A) - done
for e in reg["entries"]:
    for o in e.get("observations") or []:
        if o.get("reading") and o.get("analysis") == o.get("reading"):
            s = o.get("slug") or e["slug"]; assert s in A, s; o["analysis"] = A[s]
for e in reg["entries"]:
    for o in [e] + (e.get("observations") or []):
        assert not (o.get("reading") and o.get("analysis") == o.get("reading")), e["slug"]
P.write_text(json.dumps(reg, ensure_ascii=False, indent=1)); print("written", len(done))
