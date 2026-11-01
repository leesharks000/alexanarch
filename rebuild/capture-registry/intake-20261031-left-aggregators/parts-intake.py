"""Author the part files of 2026-10-31 (18:44 EDT): the fifteen names of the maryleelabor left-and-labor census (data/left-census, built the same day
from sources fetched once and saved with hashes), run by the operator for their NonWiki rows. Twelve on the Google AI Overview, expanded; three in AI
Mode, where the operator reports no Overview popup ('no aio popup - ai mode'; 'this one linked to wikipedia instead of popup, so ai mode'; 'linked to
wikipedia in place of popup, so ai mode'). Labor Vector at 'laborvector' ('labor vector pulled up totally unrelated, so laborvector'; the 'labor vector'
run is not pasted and is not seated). Signed out, incognito (operator default). Fourteen new external atom sets, their evidence the census's verified
quotes in the saved sources (sources/, manifest.json); Labor Vector against the archive's set ENT-d56958a10a.
  python3 parts.py && python3 build.py --check"""
import json, pathlib
H = pathlib.Path(__file__).resolve().parent
P = H / "parts"; P.mkdir(exist_ok=True)
R = json.load(open(H / "census-rows.json", encoding="utf-8"))
S = "rebuild/capture-registry/intake-20261031-left-aggregators/sources/"
A = lambda atom, present, span=None: {"atom": atom, "present": present, "span": span}
DIM = {"name": ("M", 3, "token"), "operator": ("M", 3, "role"), "date": ("M", 1, "token"), "claim boundary": ("M", 2, "reading"), "presents": ("C", 2, "token"),
       "corpus": ("C", 2, "reading"), "purpose": ("D", 3, "reading"), "commitments": ("D", 2, "reading"), "lineage": ("D", 2, "role"), "identifier": ("D", 1, "role"),
       "deposit chain": ("D", 1, "role")}
ORDER = list(DIM)


def ev(slug, key):
    q = R[slug]["evidence"][key]
    return {"record_quote": q["q"], "locus": S + q["src"] + ".txt"}


def aset(sid, slug, name, spec, type_basis):
    """spec: {atom: (tokens, reference, [evidence keys])}; atoms absent from spec are recorded unknown (no saved source states them) or inapplicable."""
    atoms = []
    for a in ORDER:
        d, w, k = DIM[a]
        if a in spec:
            tok, ref, keys = spec[a]
            atoms.append({"atom": a, "dim": d, "weight": w, "kind": k, "applicability": "required", "tokens": tok, "reference": ref, "evidence": [ev(slug, x) for x in keys]})
        else:
            app = "inapplicable" if a in ("presents", "deposit chain") else "unknown"
            atoms.append({"atom": a, "dim": d, "weight": w, "kind": k, "applicability": app, "tokens": [], "reference": None, "evidence": []})
    srcs = sorted({x["locus"] for at in atoms for x in at["evidence"]})
    return {"new": sid, "name": name, "template": "site", "external": True, "type_basis": type_basis,
            "records": [{"source": R[slug]["name"] + " (its own pages, saved 2026-10-31)", "path": p, "origin": "primary"} for p in srcs],
            "atoms": atoms, "notes": "Built 2026-10-31 from the maryleelabor census row '" + slug + "' (its quotes verified verbatim in the saved sources), for the operator's run of the census names."}


C = lambda site, title, note=None: {"site": site, "title": title, "snip": None, "rel": "third_party", "note": note}
OP = ("with the pastes (18:44 EDT), the census names as printed for him at 18:21 EDT ('if you could present the aggregators in one line copyable blocks without their urls'; "
      "'ill search those up so we can write their /nons'). His notes, in the paste: 'no aio popup - ai mode'; 'this one linked to wikipedia instead of popup, so ai mode'; "
      "'linked to wikipedia in place of popup, so ai mode'; 'labor vector pulled up totally unrelated, so laborvector'.")
AIM_HEAD = ("[Google AI Mode at the query, signed out and incognito (operator default of 2026-10-14). The operator, with the paste: '{note}'. The paste opens on the page header "
            "('Halloween 2026') and its tab row, with no 'You said' line; the query is the census name as printed for him at 18:21 EDT. The web results above the answer are kept in the raw paste and are not part of the composition. Received 2026-10-31 18:44 EDT.]")


def turns_aio(paste):
    L = (H / paste).read_text(encoding="utf-8").split("\n")
    return [[2, len(L)]]


def turns_aim(paste, first):
    L = (H / paste).read_text(encoding="utf-8").split("\n")
    a = next(i for i, l in enumerate(L) if l.startswith(first))
    b = next(i for i, l in enumerate(L) if l.strip() == "Ask anything")
    return [[a, b]]


def mk(key, slug, q, paste, aset_, obs_atoms, reached, mt, d, reading, findings, analysis, cites, per_v, per_note, aimode=None, first=None, target=None, originator=None, related=None):
    p = {"n": 1725, "slug": slug, "paste": paste, "surface": "Google AI Mode" if aimode else "Google AI Overview", "received": "2026-10-31 18:44 EDT", "s": "Machine Reception",
         "qs": [q], "turns": turns_aim(paste, first) if aimode else turns_aio(paste), "entity_type": "site", "group": "Xagg-" + key,
         "obs": {"scored_object": "the AI Mode answer, with its source cards" if aimode else "the Overview expanded, with its source cards", "reached": reached,
                 "atoms": obs_atoms, "inversions": [], "standing_substitutions": [], "src": True, "tombstone_pointer": False, "after_challenge": None, "notes": analysis},
         "mt": mt, "d": d, "reading": reading, "findings": findings, "analysis": analysis, "q_kind": "the census name; NEW address.",
         "per_v": per_v, "per_note": per_note, "cite_list": [dict(c, n=i + 1, url=None) for i, c in enumerate(cites)], "related_deposits": related or [1725],
         "notes_operator": OP}
    if aset_:
        p["atomset"] = aset_; p["target_id"] = "NEW:" + aset_["new"]
        p["originator"] = originator or {"name": R[aset_["notes"].split("'")[1]]["name"], "relation": "external", "entity_type": "site", "spxi_treatment": "partial",
                                         "basis": "Not the archive's: an external resource, entered in the maryleelabor left-and-labor census on 2026-10-31 (data/left-census, its own pages saved with hashes). Recorded 2026-10-31."}
    else:
        p["target_id"] = target; p["originator_basis"] = originator
    if aimode:
        p["head_full"] = AIM_HEAD.format(note=aimode)
        p["surface_basis"] = "The operator's report with the paste ('" + aimode + "'); the paste shows the AI Mode page (tab row, 'AI Mode response is ready')."
        p["transcript_class"] = "CAPTURE-TIME VERBATIM RECORD — paste of the AI Mode page; the composition and its cards read, the web results above it kept in the raw paste"
    else:
        p["head"] = "The 'You said' line carries the query twice, run together, and is given once here. Inline links are Google redirect URLs, kept as pasted."
    return p


SITE_TB = "A web resource: its own pages, saved 2026-10-31, describe it as {k}. A site, read on the site template."
parts = {}

# 1 Marxists Internet Archive (AI Mode)
s = "marxists-internet-archive"
parts["mia"] = mk("mia", "marxists-internet-archive-aimode-20261031", "Marxists Internet Archive", "paste-marxists-internet-archive.txt",
  aset("ext-marxists-internet-archive", s, "Marxists Internet Archive (marxists.org)", {
    "name": (["Marxists Internet Archive", "MIA", "marxists.org"], None, ["self_description"]),
    "operator": (["volunteer", "volunteers", "volunteer-run", "all-volunteer"], "An all-volunteer non-profit with a Steering Committee and an Admin Committee; 76 active volunteers (July 2025).", ["self_description", "volunteers"]),
    "date": (["1998"], "Established in its present form in 1998, with an earlier history on its history page (unread).", ["self_description"]),
    "claim boundary": ([], "The writings of close to 1000 authors, Marxist or relevant to the understanding of Marxism, in 83 languages.", ["record_object"]),
    "corpus": ([], "Over 400,000 documents and 1.1 TB of data in 83 languages (April 2026).", ["count"]),
    "purpose": ([], "To maintain an archive of any and all writings which are Marxist or relevant to the understanding of Marxism and can be lawfully published.", ["aim"]),
    "commitments": ([], "A seven-tenet Charter (free, non-profit, democratic, full disclosure, politically independent, does not 'judge' writers, archival priority); the 2007 end of the Marxist/non-Marxist division; public domain unless noted.", ["charter", "losing_side_2007", "license"])},
    SITE_TB.format(k="an all-volunteer, non-profit public library")),
  [A("name", True, "The Marxists Internet Archive (MIA), located at marxists.org, is a non-profit, volunteer-run digital library"),
   A("operator", True, "Works are transcribed, translated, and proofread into dozens of languages by a distributed network of global volunteers."),
   A("date", False), A("claim boundary", True, "hosts a vast multilingual collection of communist, socialist, anarchist, and left-wing texts"),
   A("corpus", True, "Over 180,000 documents across 80+ languages"), A("purpose", False),
   A("commitments", True, "The repository relies heavily on public domain materials or works distributed under Creative Commons licenses")],
  {"kind": "same", "abn": False, "span": "The Marxists Internet Archive (MIA), located at marxists.org, is a non-profit, volunteer-run digital library", "basis": "The archive reached by name and domain; its collections, scope, licensing and the 2014 takedown given."},
  "'MARXISTS INTERNET ARCHIVE' IN AI MODE — THE LIBRARY AT ITS GRAIN, ITS COUNT A FIFTH-SIZED; THE CHARTER THAT KEEPS EVERY WRITER UNJUDGED NOT CARRIED; THE 2014 TAKEDOWN GIVEN",
  ("THE LIBRARY, SIGNED OUT, 2026-10-31, AI MODE: 'The Marxists Internet Archive (MIA), located at marxists.org, is a non-profit, volunteer-run digital library that hosts a vast multilingual collection of communist, socialist, anarchist, and left-wing texts.' "
   "Fact table (founded 1990, 'Zodiac'; over 180,000 documents across 80+ languages); core collections; MIA Publications; copyright controversies (the 2014 MECW takedown)."),
  "The innocent reading first. Asked for the library, AI Mode describes it, its collections and scope, its print arm and its licensing, and the takedown of 2014.",
  ["THE LIBRARY AT ITS GRAIN. Author archives, subject sections, volunteer translation and the public-domain basis are carried; the 2014 removal of the English Collected Works at Lawrence & Wishart's order is given ('The 2014 MECW Takedown').",
   "THE COUNT AND THE DATE. 'Over 180,000 documents across 80+ languages' and 'Founded 1990 (Originally by a user known as \"Zodiac\")'. The MIA's introduction (last updated 21 April 2026) gives 'over 400,000 documents and 1.1 TB of data (April 2026)' in 83 languages, and dates its present form to 1998, with an earlier history on a page not read here.",
   "THE CHARTER NOT CARRIED. The MIA's sixth tenet, 'We do not ‘judge’ writers', and its 2007 end of 'dividing all writers into Marxists and non-Marxists' are absent. #1725 reads that as the holder condition: a writer stays in the record whatever verdict a party passed on them."],
  "The library composed accurately at the level of its sections, with a count from an earlier state of the site. What it leaves out is the terms on which it holds: its charter's refusal to judge writers, which is what keeps the losing side of every split on its shelves.",
  [C("Marxists Internet Archive", "Marxists Internet Archive"), C("Wikipedia", "Marxists Internet Archive - Wikipedia"), C("Library of Congress", "Marxists Internet Archive | Library of Congress"),
   C("Erythros Press and Media", "Marxists Internet Archive Publications - Erythros Press and Media"), C("Falvey Library Blog", "Falvey Library Blog"), C("ResearchGate", "PDF) Marxists Internet Archive Takedown"),
   C("Reddit", "r/communism", "the takedown line")],
  {"author": False, "inst": True, "id": False, "src": True}, "The library named with its domain; no operator body named.",
  aimode="no aio popup - ai mode", first="The Marxists Internet Archive (MIA)")

# 2 MEGAdigital (substituted)
s = "mega-digital"
parts["mega"] = mk("mega", "megadigital-aio-20261031", "MEGAdigital", "paste-mega-digital.txt",
  aset("ext-megadigital", s, "MEGAdigital (the online division of the Marx-Engels-Gesamtausgabe, BBAW)", {
    "name": (["MEGAdigital", "Marx-Engels-Gesamtausgabe", "MEGA"], None, ["kind"]),
    "operator": (["Berlin-Brandenburgische Akademie der Wissenschaften", "BBAW", "Berlin-Brandenburg Academy"], "The Berlin-Brandenburgische Akademie der Wissenschaften, as an academy project.", ["operator", "academy_project"]),
    "date": (["1970s", "1970er"], "Begun in the 1970s in Berlin and Moscow.", ["founded"]),
    "claim boundary": ([], "The historical-critical edition of all the publications, manuscripts, drafts and correspondence of Marx and Engels; MEGAdigital its online division.", ["self_description"]),
    "corpus": ([], "The edited texts of ten volumes of the Second Division (Capital and its preparatory works) online, and a growing digital continuation of the Third and Fourth Divisions.", ["holdings_online", "limit_digital"]),
    "lineage": (["Moscow", "Berlin", "IMES", "1989"], "Begun in Berlin and Moscow; carried on after 1989 by scholars of many countries (IMES).", ["founded", "after_1989"])},
    SITE_TB.format(k="the online division of the historical-critical Marx-Engels edition")),
  [A("name", False), A("operator", False), A("date", False), A("claim boundary", False), A("corpus", False), A("lineage", False)],
  {"kind": "substitute", "abn": False, "span": "is a digital marketing and software agency based in Southeast Asia", "basis": "The name reached as Mega Digital JSC, a marketing agency in Hanoi, Ho Chi Minh City and Singapore; the edition does not appear."},
  "'MEGADIGITAL' ON THE OVERVIEW — THE MARX-ENGELS EDITION SUBSTITUTED BY A VIETNAMESE AD AGENCY OF THE SAME NAME; AD-ACCOUNT RENTALS IN ITS PLACE",
  ("THE EDITION, SIGNED OUT, 2026-10-31: 'Mega Digital is a digital marketing and software agency based in Southeast Asia, with primary offices in Hanoi and Ho Chi Minh City, Vietnam, as well as an office in Singapore.' "
   "Founded May 2021; Mega Digital JSC; TikTok, Google and Microsoft partner; ad account rentals 'with unlimited spending capabilities'. Cards: TikTok, Trustpilot, Instagram, Crunchbase, YouTube (two), Clutch."),
  "The innocent reading first. Given a bare compound name, the Overview resolves it to the company that most uses it and asks what platform the user wants to advertise on.",
  ["THE EDITION SUBSTITUTED. Every sentence and every card is the agency's: 'Ad Account Rentals & Management: Agency ad accounts for rent with unlimited spending capabilities across platforms like TikTok, Google, Facebook, and Microsoft.' No sentence names Marx, Engels, the MEGA or the Berlin-Brandenburg Academy.",
   "THE NAME HELD BY COMMERCE. The edition's own page names itself 'Online-Abteilung der historisch-kritischen Gesamtausgabe von Karl Marx und Friedrich Engels' (sources/mega-digital--mega.txt). At the bare name the field holds a company founded in May 2021, and the composition's follow-up offers campaign management."],
  "A substitution at the name: the critical edition of Marx and Engels, the record of their texts in the state their drafts left them, is absent from a composition about an advertising agency that shares its name.",
  [C("TikTok", "MEGA DIGITAL: TikTok Marketing Partners"), C("Trustpilot", "Mega Digital Reviews | Read Customer Service Reviews of megadigital.ai"), C("Instagram", "Megadigital (@megadigitaljsc) · Hanoi"),
   C("Crunchbase", "Mega Digital - Crunchbase Company Profile & Funding"), C("YouTube", "Mega Digital"), C("YouTube", "INTRODUCING MEGA DIGITAL AGENCY - WE ARE THE CHANGEMAKER"), C("Clutch", "Mega Digital JSC Reviews (2), Pricing, Services & Verified Ratings - Clutch")],
  {"author": False, "inst": False, "id": False, "src": True}, "No source of the edition; every card the agency's.")

# 3 BannedThought.net
s = "bannedthought"
parts["bannedthought"] = mk("bannedthought", "bannedthought-net-aio-20261031", "bannedthought.net", "paste-bannedthought.txt",
  aset("ext-bannedthought", s, "BannedThought.net", {
    "name": (["BannedThought.net", "BANNEDTHOUGHT.NET", "bannedthought"], None, ["independent"]),
    "claim boundary": ([], "Suppressed progressive documents and publications, posted to publicize their suppression.", ["self_description"]),
    "corpus": ([], "Party documents by country, the parties of each split listed side by side (the CPI(M-L) of 1969, People's War, Satyanarayan Singh; the CPN Maoist and its successors), the Great Debate, Mao and MLM theory.", ["cpiml_original", "cpiml_pw", "nepal_rm", "great_debate"]),
    "purpose": ([], "To struggle against the suppression of progressive ideas and make suppressed documents available.", ["self_description"]),
    "commitments": ([], "Independent and unaffiliated with any political party; sympathies stated; posting usually only in English.", ["independent", "limit_language"])},
    SITE_TB.format(k="a site against the suppression of progressive ideas")),
  [A("name", True, "BANNEDTHOUGHT.NET - Struggling against the suppression of progressive ideas."),
   A("claim boundary", True, "is an online digital archive that collects, preserves, and publishes censored documents, periodicals, and writings related to international communist movements, Maoist theory, and revolutionary left-wing struggles worldwide."),
   A("corpus", True, "including materials from the Communist Party of the Philippines (CPP), the Communist Party of India (Maoist), and broader Marxist-Leninist-Maoist movements."),
   A("purpose", True, "It aims to oppose the suppression of progressive or radical ideas by making rare, out-of-print, and politically censored texts freely accessible."),
   A("commitments", False)],
  {"kind": "same", "abn": False, "span": "is an online digital archive that collects, preserves, and publishes censored documents", "basis": "The site reached by name; purpose, scope and its own ban given."},
  "'BANNEDTHOUGHT.NET' ON THE OVERVIEW — THE ARCHIVE OF THE SUPPRESSED AT ITS GRAIN; ITS INDEPENDENCE FROM EVERY PARTY NOT CARRIED; THE SPLITS IT HOLDS SIDE BY SIDE GIVEN AS 'BROADER' MOVEMENTS",
  ("THE SITE, SIGNED OUT, 2026-10-31: '[BannedThought.net] is an online digital archive that collects, preserves, and publishes censored documents, periodicals, and writings related to international communist movements, Maoist theory, and revolutionary left-wing struggles worldwide.' "
   "Purpose; content scope (CPP, CPI (Maoist)); censorship status. Three cards: the site, Philippine E-Journals, YUMPU."),
  "The innocent reading first. Asked for the site, the Overview gives its purpose, its holdings and the bans on the site itself, from the site.",
  ["THE PURPOSE AT ITS GRAIN. 'It aims to oppose the suppression of progressive or radical ideas by making rare, out-of-print, and politically censored texts freely accessible.' The site: 'This site exists to struggle against the fascist-like suppression of progressive ideas and thought by reactionary governments and their agents anywhere in the world.'",
   "THE INDEPENDENCE NOT CARRIED. 'BANNEDTHOUGHT.NET is independent and unaffiliated with any political party.' The composition does not say who holds the site or on whose behalf.",
   "THE SPLITS FOLDED. The site lists the parties of each split side by side ('CPI(M-L) [Original Party formed in 1969]', 'Communist Party of India (Marxist-Leninist) [People’s War]', 'CPI(M-L) [Satyanaran Singh] / PCC-CPI(M-L)'; the CPN Maoist and its successors). The composition gives 'broader Marxist-Leninist-Maoist movements'. #1725 reads such a page as an organ that keeps both sides of a split in one record."],
  "Faithful at the level of purpose and scope. The holder (independent of every party) and the form of the holdings (each split's parties kept in parallel) are the two features #1725 asks of an archive of the left, and both are absent.",
  [C("BANNEDTHOUGHT.NET", "BANNEDTHOUGHT.NET - Struggling against the suppression of progressive ideas."), C("Philippine E-Journals", "Interrogating Mao and Locating the Philippine Left’s Position within ..."), C("YUMPU", "8 free Magazines from BANNEDTHOUGHT.NET")],
  {"author": False, "inst": False, "id": False, "src": True}, "The site named and cited; no holder named (the site names none).")

# 4 EROL
s = "erol"
parts["erol"] = mk("erol", "encyclopedia-of-anti-revisionism-on-line-aio-20261031", "Encyclopedia of Anti-Revisionism On-Line", "paste-erol.txt",
  aset("ext-erol", s, "Encyclopedia of anti-Revisionism On-Line (EROL)", {
    "name": (["Encyclopedia of anti-Revisionism On-Line", "Encyclopedia of Anti-Revisionism On-Line", "EROL"], None, ["name"]),
    "operator": (["Marxists Internet Archive", "EROL Administrator"], "An EROL Administrator, within the Marxists Internet Archive's History section.", ["administrator"]),
    "claim boundary": ([], "Information on and primary documents from anti-revisionist movements, organizations and parties, by country.", ["self_description"]),
    "corpus": ([], "Country sections; for the United States the New Communist Movement in periods, including its crises, splits, failed unity and collapse; periodicals by country.", ["us_ncm_origins", "splits", "unable_to_unite", "collapse", "periodicals"])},
    SITE_TB.format(k="an encyclopedia of primary documents from anti-revisionist movements")),
  [A("name", True, "Encyclopedia of anti-Revisionism On-Line Background: Definitions and representative materials from China and Albania."),
   A("operator", True, "is a digital archive developed by the Marxists Internet Archive"),
   A("claim boundary", True, "containing primary source documents, translations, and organizational records from the international anti-revisionist and Marxist-Leninist/Maoist movements."),
   A("corpus", True, "Includes documentation, background materials, and party histories from:")],
  {"kind": "same", "abn": False, "span": "is a digital archive developed by the Marxists Internet Archive containing primary source documents", "basis": "The encyclopedia reached by name, with its definition, timeframe, countries and periodicals."},
  "'ENCYCLOPEDIA OF ANTI-REVISIONISM ON-LINE' ON THE OVERVIEW — THE ENCYCLOPEDIA AT ITS GRAIN; ITS RECORD OF THE NEW COMMUNIST MOVEMENT'S SPLITS AND COLLAPSE NOT CARRIED",
  ("THE ENCYCLOPEDIA, SIGNED OUT, 2026-10-31: 'The Encyclopedia of Anti-Revisionism On-Line (EROL) is a digital archive developed by the Marxists Internet Archive containing primary source documents, translations, and organizational records from the international anti-revisionist and Marxist-Leninist/Maoist movements.' "
   "Core definition; timeframe 1946 to 1983; geographic coverage; periodicals. Five cards: three Marxists Internet Archive pages, Harvard University, one more MIA page."),
  "The innocent reading first. Asked for the encyclopedia, the Overview defines its subject, gives its period and countries, names periodicals and points to its index.",
  ["THE SCOPE AT ITS GRAIN. Definition, period, countries and periodicals are carried from EROL's own pages, with the split between Chinese and Albanian alignments.",
   "THE SPLITS NOT CARRIED. EROL's United States section is periodized by its crises: 'The New Communist Movement: Crises, Splits and More New Parties, 1977-1980', 'Anti-Dogmatists Unable to Unite, 1978-1980', 'Collapse and Aftermath'. The composition gives the movement as a country entry. #1725 reads EROL as a record kept of a movement's failure to hold its own critiques, organized by that failure."],
  "Faithful to the encyclopedia's subject and range. The feature that makes EROL a record of the left's internal history, its periodization by splits, unity attempts and collapse, is not in the composition.",
  [C("Marxists Internet Archive", "Encyclopedia of anti-Revisionism On-Line"), C("Marxists Internet Archive", "What is Anti-Revisionism: Encyclopedia of anti-Revisionism On-Line"), C("Marxists Internet Archive", "MIA: History: Encyclopedia of anti-Revisionism On-Line"),
   C("Harvard University", "The Encyclopedia of anti-Revisionism On"), C("Marxists Internet Archive", "Encyclopedia of anti-Revisionism On-Line")],
  {"author": False, "inst": True, "id": False, "src": True}, "The MIA named as its host; EROL's own pages cited.")

# 5 Amiel Melburn Trust Archive
s = "banmarchive"
parts["banmarchive"] = mk("banmarchive", "amiel-melburn-trust-archive-aio-20261031", "Amiel Melburn Trust Archive", "paste-banmarchive.txt",
  aset("ext-amiel-melburn-trust-archive", s, "Amiel Melburn Trust Archive (banmarchive.org.uk)", {
    "name": (["Amiel Melburn Trust Archive", "Amiel Melburn Archive", "Amiel & Melburn Trust"], None, ["self_description"]),
    "operator": (["Barry Amiel and Norman Melburn Trust", "Barry Amiel & Norman Melburn Trust"], "The Barry Amiel and Norman Melburn Trust, a registered charity.", ["holder", "charity"]),
    "claim boundary": ([], "An online database of socialist and radical writings.", ["self_description"]),
    "corpus": ([], "Runs of journals: The Reasoner, New Reasoner, Universities & Left Review, Marxism Today, Black Dwarf, 7 Days, Red Rag, Soundings and others.", ["h_marxism_today", "h_new_reasoner", "h_reasoner", "h_black_dwarf"]),
    "lineage": (["Reasoner", "Thompson", "Saville", "1956"], "The Reasoner, the journal of two Communist Party members ordered to close it, relaunched as the New Reasoner after their suspension, later New Left Review.", ["reasoner_case", "merger"])},
    SITE_TB.format(k="an online database of socialist and radical writings")),
  [A("name", True, "Amiel Melburn Trust Archive - Amiel Melburne Trust Archive"),
   A("operator", True, "The Barry Amiel and Norman Melburn Trust runs an online archive of historical socialist and radical writings."),
   A("claim boundary", True, "runs an online archive of historical socialist and radical writings."),
   A("corpus", True, "including prominent titles such as Marxism Today, New Reasoner, Black Dwarf, and others."),
   A("lineage", False)],
  {"kind": "same", "abn": False, "span": "The Barry Amiel and Norman Melburn Trust runs an online archive of historical socialist and radical writings.", "basis": "The archive reached by name with its trust, range and titles."},
  "'AMIEL MELBURN TRUST ARCHIVE' ON THE OVERVIEW — THE ARCHIVE AND ITS TRUST AT THEIR GRAIN; THE NEW REASONER LISTED AS A TITLE, THE CRITICS THE PARTY ORDERED SILENT NOT CARRIED",
  ("THE ARCHIVE, SIGNED OUT, 2026-10-31: 'The Barry Amiel and Norman Melburn Trust runs an online archive of historical socialist and radical writings.' The archive (titles, 1956 to 2024); the trust (history, grants). Six cards: the archive, the trust (three), commonknowledge.coop, Bath and North East Somerset."),
  "The innocent reading first. Asked for the archive, the Overview names its trust, its range and its best-known titles, and the trust's history and grants.",
  ["THE TITLES AT THEIR GRAIN. 'It spans nearly 70 years of radical publications, journals, and pamphlets from 1956 to 2024, including prominent titles such as Marxism Today, New Reasoner, Black Dwarf, and others.'",
   "THE ORIGIN OF THE NEW REASONER NOT CARRIED. The archive's own introduction to the title: 'When E.P. Thompson and John Saville were instructed by the leadership of the Communist Party of Great Britain to close down their journal The Reasoner , which had been critical of what the editors saw as the Party’s dogmatism, they refused.' #1725 counts the line from The Reasoner to the New Left as a critique that survived its party by keeping an organ; the composition gives the journal as a title.",
   "THE START DATE KEPT. '1956' is the year of The Reasoner (three issues, 1956, in the archive's holdings list); the composition gives the year without the event."],
  "An accurate composition of what the archive holds and who funds it. The archive's own account of why its first titles exist, an organ kept by critics after their party ordered it closed, is not carried.",
  [C("Amiel Melburn Archive", "Amiel Melburn Trust Archive - Amiel Melburne Trust Archive"), C("Barry Amiel & Norman Melburn Trust", "Barry Amiel & Norman Melburn Trust: Home"), C("commonknowledge.coop", "Barry Amiel and Norman Melburn Trust Archive"),
   C("Barry Amiel & Norman Melburn Trust", "Awards Archive - Barry Amiel & Norman Melburn Trust"), C("Barry Amiel & Norman Melburn Trust", "General Archives - Page 2 of 4"), C("Bath and North East Somerset", "The Barry Amiel and Norman Melburn Trust | Bath and North East Somerset ...")],
  {"author": False, "inst": True, "id": False, "src": True}, "The trust named; the archive and the trust's pages cited.")

# 6 libcom.org Collections
s = "libcom-library"
parts["libcom"] = mk("libcom", "libcom-org-collections-aio-20261031", "libcom.org Collections", "paste-libcom-collections.txt",
  aset("ext-libcom-collections", s, "libcom.org Collections", {
    "name": (["libcom.org", "libcom", "Libcom"], None, ["kind"]),
    "claim boundary": ([], "Collections, tags, archives, authors, reading guides, blogs and galleries of libertarian communist and anarchist history.", ["kind"]),
    "corpus": ([], "Tagged collections on strikes and movements and on writers of the anarchist and left-communist currents (Bordiga, Pannekoek, Dauvé, Debord, the CNT).", ["tags_strikes", "tags_flint", "tags_writers", "tags_pannekoek", "tags_dauve"])},
    SITE_TB.format(k="the collections of an anarchist and libertarian communist library")),
  [A("name", True, "Collections | libcom.org"),
   A("claim boundary", True, "an extensive digital archive dedicated to anarchist, libertarian socialist, communist, and radical working-class history."),
   A("corpus", True, "Curated resources on major events, strikes, and struggles")],
  {"kind": "same", "abn": False, "span": "an extensive digital archive dedicated to anarchist, libertarian socialist, communist, and radical working-class history.", "basis": "The collections reached by name, section by section, from the site's own pages."},
  "'LIBCOM.ORG COLLECTIONS' ON THE OVERVIEW — THE LIBRARY'S SECTIONS AT THEIR GRAIN; THE CURRENTS THE THIRD INTERNATIONAL EXPELLED GIVEN AS NAMES",
  ("THE COLLECTIONS, SIGNED OUT, 2026-10-31: 'Explore the libcom.org Collections to find an extensive digital archive dedicated to anarchist, libertarian socialist, communist, and radical working-class history.' Collections; biographies and thinkers; archives; galleries; reading guides. Six cards, all libcom.org."),
  "The innocent reading first. Asked for the collections, the Overview walks the site's sections and names what each holds.",
  ["THE SECTIONS AT THEIR GRAIN. Strikes, movements, writers, journals and galleries are given as the site's tabs give them, from the site alone.",
   "THE CURRENTS AS NAMES. 'Emma Goldman, Anton Pannekoek, Amadeo Bordiga, CLR James, David Graeber, and Gilles Dauvé'. Pannekoek's council communists and Bordiga's left were the currents the Communist International expelled; libcom keeps their texts. The composition lists them as 'prominent radical figures'.",
   "NO HOLDER NAMED. Neither the composition nor the site's saved pages name who runs the library (its pages are submitted under the account 'libcom')."],
  "A faithful map of the site's sections. Who holds the library is unstated on both sides, and the composition flattens the losing currents of the Third International into a list of figures.",
  [C("Libcom.org", "Collections | libcom.org"), C("Libcom.org", "Archives | libcom.org"), C("Libcom.org", "Collections | libcom.org"), C("Libcom.org", "Blogs"), C("Libcom.org", "Galleries - Libcom.org"), C("Libcom.org", "Galleries")],
  {"author": False, "inst": False, "id": False, "src": True}, "The site cited throughout; no holder named.")

# 7 Irish Left Archive
s = "irish-left-archive"
parts["ila"] = mk("ila", "irish-left-archive-aio-20261031", "Irish Left Archive", "paste-irish-left-archive.txt",
  aset("ext-irish-left-archive", s, "Irish Left Archive (leftarchive.ie)", {
    "name": (["Irish Left Archive"], None, ["kind"]),
    "operator": (["Cedar Lounge Revolution"], "Initiated by the Cedar Lounge Revolution.", ["operator"]),
    "claim boundary": ([], "An online archive of materials relating to Irish left politics, freely accessible and easy to download and reproduce.", ["kind"]),
    "corpus": ([], "1231 documents, 436 organisations, 217 publications, 875 people; an interactive timeline of Irish left organisations from 1900.", ["count", "timeline"]),
    "purpose": ([], "To collate first-hand political reminiscences from people involved, beside the documents.", ["personal_accounts"]),
    "commitments": ([], "Freely accessible and easy to download and reproduce.", ["kind"])},
    SITE_TB.format(k="an online archive of materials relating to Irish left politics")),
  [A("name", True, "The Irish Left Archive is a digital project and online repository"),
   A("operator", False),
   A("claim boundary", True, "dedicated to collecting, preserving, and sharing material related to left-wing politics, activism, and history in Ireland."),
   A("corpus", True, "Holds over 1,200 documents, hundreds of organizations, publications, profiles, and collections"),
   A("purpose", True, "Collects first-hand observations and reminiscences from activists and participants in Irish left movements."),
   A("commitments", True, "Freely accessible documents, manifestos, pamphlets, and publications")],
  {"kind": "same", "abn": False, "span": "The Irish Left Archive is a digital project and online repository", "basis": "The archive reached by name with its holdings, timeline, personal accounts and podcast."},
  "'IRISH LEFT ARCHIVE' ON THE OVERVIEW — THE ARCHIVE AT ITS GRAIN, ITS TIMELINE OF ORGANISATIONS GIVEN; ITS ORIGIN IN THE CEDAR LOUNGE REVOLUTION NOT CARRIED",
  ("THE ARCHIVE, SIGNED OUT, 2026-10-31: 'The Irish Left Archive is a digital project and online repository dedicated to collecting, preserving, and sharing material related to left-wing politics, activism, and history in Ireland.' Digital collection; timeline; scope; personal accounts; the podcast. Four cards: the archive, Spotify, Pocket Casts, mastodon.online."),
  "The innocent reading first. Asked for the archive, the Overview gives its holdings, its timeline of organisations, its personal accounts and its podcast.",
  ["THE HOLDINGS AT THEIR GRAIN. 'An interactive timeline tracking Irish left organizations and parties from 1900 to the present.' The archive keeps every organisation of a fissile left, its rival parties included, on one record and one timeline.",
   "THE ORIGIN NOT CARRIED. 'It was initiated by the Cedar Lounge Revolution .' (the archive's home page). The composition names the podcast's hosts and no holder of the archive."],
  "Faithful at the level of holdings and features. The archive's founding by a left blog's community, which is who holds the record, is absent.",
  [C("Irish Left Archive", "Irish Left Archive — Digital archive of Irish left politics"), C("Spotify", "Irish Left Archive Podcast | Podcast on Spotify"), C("Pocket Casts", "Irish Left Archive Podcast - Pocket Casts"), C("mastodon.online", "Irish Left Archive (@LeftArchive@mastodon.online)")],
  {"author": False, "inst": False, "id": False, "src": True}, "The archive and its podcast cited; no holder named.")

# 8 IISH (AI Mode)
s = "iish"
parts["iish"] = mk("iish", "international-institute-of-social-history-aimode-20261031", "International Institute of Social History", "paste-iish.txt",
  aset("ext-iish", s, "International Institute of Social History (IISH, IISG)", {
    "name": (["International Institute of Social History", "IISH", "IISG", "Internationaal Instituut voor Sociale Geschiedenis"], None, ["collections"]),
    "operator": (["Royal Netherlands Academy of Arts and Sciences", "KNAW"], "An Institute of the Royal Netherlands Academy of Arts and Sciences.", ["operator"]),
    "date": (["1935"], None, ["founded"]),
    "claim boundary": ([], "Collections in socio-economic history on organisations and persons in labour and social and emancipatory movements, online and in the reading room.", ["collections"]),
    "corpus": ([], "More than 50 kilometres of archives, publications and audiovisual collections; thousands of datasets on wages, prices and labour relations.", ["collections", "data"])},
    SITE_TB.format(k="an institute and archive of socio-economic history")),
  [A("name", True, "The International Institute of Social History (IISH; Dutch: Internationaal Instituut voor Sociale Geschiedenis, IISG)"),
   A("operator", True, "Royal Netherlands Academy of Arts and Sciences (KNAW)"),
   A("date", True, "November 25, 1935"),
   A("claim boundary", True, "is one of the world's premier archives and research centers dedicated to global labor and social history."),
   A("corpus", True, "over one million volumes, three million digital files, and thousands of linear feet of manuscripts")],
  {"kind": "same", "abn": False, "span": "The International Institute of Social History (IISH; Dutch: Internationaal Instituut voor Sociale Geschiedenis, IISG)", "basis": "The institute reached by name, with its founding, affiliation, holdings and data."},
  "'INTERNATIONAL INSTITUTE OF SOCIAL HISTORY' IN AI MODE — THE INSTITUTE AT ITS GRAIN; THE PAPERS OF MARX, ENGELS AND BAKUNIN NAMED IN ONE CUSTODY",
  ("THE INSTITUTE, SIGNED OUT, 2026-10-31, AI MODE: 'The International Institute of Social History (IISH; Dutch: Internationaal Instituut voor Sociale Geschiedenis, IISG) is one of the world's premier archives and research centers dedicated to global labor and social history.' "
   "Fact table (founded 25 November 1935, Posthumus, KNAW); core pillars: the archive, radical papers, rescue of endangered heritage, the data hub."),
  "The innocent reading first. Asked for the institute, AI Mode gives its founding, affiliation, holdings, rescues and data, and offers to help plan a visit.",
  ["ONE CUSTODY FOR BOTH SIDES OF THE HAGUE. 'Its vaults contain the irreplaceable personal papers and manuscripts of major historical figures like Karl Marx, Friedrich Engels, Mikhail Bakunin, Emma Goldman, and Leon Trotsky.' The parties to the First International's 1872 expulsion (#1725) are held by one institution.",
   "THE RESCUE CARRIED. 'Originally founded to rescue endangered heritage from totalitarian regimes (such as Nazi Germany and Franco's Spain)'. The institute's saved pages state its founding year ('The IISH was officially established in 1935') and do not carry the rescue; the composition cites it to the International Consortium of Critical Theory."],
  "A faithful account of the institute, with the feature #1725 values in an archive of the left: the papers of the winning and losing sides of a split in one custody.",
  [C("Internationaal Instituut voor Sociale Geschiedenis", "International Institute of Social History - IISG"), C("Wikipedia", "International Institute of Social History - Wikipedia"), C("KNAW", "International Institute of Social History (IISH) - KNAW"),
   C("International Consortium of Critical Theory", "International Consortium of Critical Theory"), C("ESSHC", "About IISH | ESSHC")],
  {"author": False, "inst": True, "id": False, "src": True}, "The institute and its academy named; the institute's site among the cards.",
  aimode="this one linked to wikipedia instead of popup, so ai mode", first="The International Institute of Social History (IISH;")

# 9 Reuther Library
s = "reuther-library"
parts["reuther"] = mk("reuther", "walter-p-reuther-library-aio-20261031", "Walter P. Reuther Library, Archives of Labor and Urban Affairs", "paste-reuther-library.txt",
  aset("ext-reuther-library", s, "Walter P. Reuther Library, Archives of Labor and Urban Affairs (Wayne State University)", {
    "name": (["Walter P. Reuther Library", "Reuther Library", "Archives of Labor and Urban Affairs"], None, ["history"]),
    "operator": (["Wayne State University"], None, ["history"]),
    "date": (["1960"], "Established as the Labor History Archives in 1960.", ["history"]),
    "claim boundary": ([], "The largest labor archives in North America, home to the collections of numerous unions, with Detroit's political and community life.", ["kind", "strengths"]),
    "corpus": ([], "Union collections (AFSCME, AFT, ALPA, IWW, SEIU, UAW, UFW and others) and the Wayne State University Archives.", ["categories", "university_archives"]),
    "purpose": ([], "To collect and preserve original source materials relating to the development of the American labor movement.", ["history"]),
    "commitments": ([], "Collections freely open to the public; appointments not required.", ["access"]),
    "lineage": (["United Automobile", "UAW", "Woodcock"], "The building constructed in 1975 with funds given by the UAW; the Leonard Woodcock Wing, a later UAW gift, 1991.", ["building", "wing"])},
    SITE_TB.format(k="the largest labor archives in North America")),
  [A("name", True, "is the largest labor archive in North America, located on the campus of Wayne State University"),
   A("operator", True, "located on the campus of Wayne State University"),
   A("date", True, "Established in 1960 as the Labor History Archives"),
   A("claim boundary", True, "is the largest labor archive in North America"),
   A("corpus", True, "Serves as the official repository for major labor unions and organizations"),
   A("purpose", True, "the library preserves millions of primary documents chronicling the American labor movement"),
   A("commitments", False), A("lineage", False)],
  {"kind": "same", "abn": False, "span": "is the largest labor archive in North America, located on the campus of Wayne State University", "basis": "The library reached by its full name, with its history, collections and research access."},
  "'WALTER P. REUTHER LIBRARY' ON THE OVERVIEW — THE LIBRARY AT ITS GRAIN; AN APPOINTMENT ADVISED WHERE THE LIBRARY SAYS NONE IS REQUIRED; THE UAW'S GIFT OF THE BUILDING NOT CARRIED",
  ("THE LIBRARY, SIGNED OUT, 2026-10-31: 'The Walter P. Reuther Library, Archives of Labor and Urban Affairs is the largest labor archive in North America, located on the campus of Wayne State University at 5401 Cass Ave in Detroit, Michigan.' "
   "History (1960, 1975, 1991); labor, urban and university collections; visiting and research. Seven cards: the library, Wayne State (three), Wikipedia, Project MUSE, DETROITography."),
  "The innocent reading first. Asked for the library, the Overview gives its history, its collections and how to use them, and offers to guide a visit.",
  ["THE ACCESS RULE RESTATED. 'Researchers should schedule a research appointment in advance with Reference Archivist Kristen Chinery.' The library's About page, saved the same day: 'The collections housed in the Reuther Library are freely open to the public. Appointments are not required'.",
   "THE CUSTODIAN OF THE UNIONS' OWN RECORDS. 'Serves as the official repository for major labor unions and organizations, including the United Automobile Workers (UAW)'. The building was 'constructed with funds given to Wayne State University by the United Automobile, Aerospace, and Agricultural Implement Workers of America' (the library's page); the composition gives the years of the building and wing without the gift. #1725 asks of such an archive whether it keeps the records of the oppositions inside the unions it holds; neither the composition nor the saved pages say."],
  "An accurate account of the library's history and holdings, with one access rule stated against the library's own page and its funding by the union whose records it keeps not carried.",
  [C("Walter P. Reuther Library", "Walter P. Reuther Library"), C("Wayne State University", "Home - Walter P. Reuther Library, Archives of Labor and Urban Affairs - Research Guides at Wayne State University"), C("Wayne State University", "Walter P. Reuther Library, Archives of Labor and Urban Affairs"),
   C("Wikipedia", "Walter P. Reuther Library - Wikipedia"), C("Project MUSE", "The Evolution of the Walter P. Reuther Library - Project MUSE"), C("DETROITography", "Walter P. Reuther Library, Archives of Labor and Urban Affairs"), C("Wayne State University", "Walter P. Reuther Library - Museums - Wayne State University")],
  {"author": False, "inst": True, "id": False, "src": True}, "The library and university named; the library's site among the cards.")

# 10 Labor Action Tracker
s = "cornell-labor-action-tracker"
parts["lat"] = mk("lat", "labor-action-tracker-aio-20261031", "Labor Action Tracker", "paste-labor-action-tracker.txt",
  aset("ext-labor-action-tracker", s, "Labor Action Tracker (Cornell ILR and Illinois LER)", {
    "name": (["Labor Action Tracker", "ILR Labor Action Tracker"], None, ["self_description"]),
    "operator": (["Cornell", "ILR School", "University of Illinois", "LER School"], "Cornell University's ILR School and the University of Illinois' LER School, together since January 2024.", ["operator", "rebrand"]),
    "date": (["2020", "2021"], "Begun at the ILR School in late 2020; public on 1 May 2021.", ["founded"]),
    "claim boundary": ([], "A comprehensive database of strike and labor protest activity across the United States.", ["self_description"]),
    "corpus": ([], "Strikes from late 2020 and labor protests from early 2021, from public sources entered by hand; strikes most accurate as of 2021.", ["coverage_period", "method", "limit_accuracy"]),
    "lineage": (["China Labour Bulletin"], "Thanks the China Labour Bulletin for inspiring the project.", ["inspiration"])},
    SITE_TB.format(k="a database of strike and labor protest activity")),
  [A("name", True, "ILR Labor Action Tracker"),
   A("operator", True, "is a joint research project by Cornell University's ILR School and the University of Illinois' LER School."),
   A("date", False),
   A("claim boundary", True, "provides a comprehensive database and interactive map tracking labor strikes, lockouts, and worker protest activity across the United States."),
   A("corpus", True, "the Labor Action Tracker captures work stoppages of all sizes (involving six or more workers) as well as non-strike labor protests."),
   A("lineage", False)],
  {"kind": "same", "abn": False, "span": "is a joint research project by Cornell University's ILR School and the University of Illinois' LER School.", "basis": "The tracker reached by name, with its operators, scope against the BLS and tools."},
  "'LABOR ACTION TRACKER' ON THE OVERVIEW — THE TRACKER AT ITS GRAIN, SET AGAINST THE BLS THRESHOLD; ITS DEBT TO THE CHINA LABOUR BULLETIN NOT CARRIED",
  ("THE TRACKER, SIGNED OUT, 2026-10-31: 'The ILR Labor Action Tracker is a joint research project by Cornell University's ILR School and the University of Illinois' LER School.' Database scope (against the BLS's 1,000-worker threshold); tools; recent trends. Five cards: the tracker, Cornell ILR (two), Facebook·The Daily Illini, BLS."),
  "The innocent reading first. Asked for the tracker, the Overview gives its operators, sets its scope against the federal statistics and points to its reports.",
  ["THE SCOPE AGAINST THE STATE'S COUNT. 'Unlike official federal statistics—such as the U.S. Bureau of Labor Statistics Work Stoppages Program, which only records large stoppages involving 1,000 or more workers'. The composition carries the tracker's reason to exist: the strikes the state's series does not count.",
   "THE LINEAGE NOT CARRIED. 'We also thank the staff of the China Labour Bulletin for inspiring and encouraging us to develop this project.' (the tracker's About page)."],
  "Faithful, and at its best where it sets the tracker against the BLS threshold. Its start date and its lineage from the China Labour Bulletin's strike map are not carried.",
  [C("ILR Labor Action Tracker", "ILR Labor Action Tracker"), C("Cornell's ILR School", "Labor Action Tracker"), C("Cornell ILR School", "Labor Action Tracker 2025"),
   C("Facebook·The Daily Illini", "UI and Cornell launch labor action tracker in Illinois"), C("Bureau of Labor Statistics (.gov)", "Work Stoppages Home Page : U.S. Bureau of Labor Statistics")],
  {"author": True, "inst": True, "id": False, "src": True}, "Both schools named; the tracker's own pages among the cards.")

# 11 Crowd Counting Consortium
s = "crowd-counting-consortium"
parts["ccc"] = mk("ccc", "crowd-counting-consortium-aio-20261031", "Crowd Counting Consortium", "paste-crowd-counting-consortium.txt",
  aset("ext-crowd-counting-consortium", s, "Crowd Counting Consortium (Harvard Kennedy School and the University of Connecticut)", {
    "name": (["Crowd Counting Consortium", "CCC"], None, ["operator"]),
    "operator": (["Harvard", "University of Connecticut", "Chenoweth", "Pressman"], "Harvard Kennedy School and the University of Connecticut, part of the Nonviolent Action Lab; begun by Jeremy Pressman and Erica Chenoweth.", ["operator", "founded"]),
    "date": (["2017"], None, ["founded"]),
    "claim boundary": ([], "A public interest and scholarly project to document protests and demonstrations in the United States.", ["self_description"]),
    "corpus": ([], "Publicly reported political crowds in the United States, in three phases from 2017, published monthly on Dataverse.", ["unit", "phases", "data_access"]),
    "commitments": ([], "Only records confirmed by fact-checking; no identifying information not already public.", ["limit_verified", "limit_identity"])},
    SITE_TB.format(k="a public interest and scholarly project documenting protests")),
  [A("name", True, "The Crowd Counting Consortium (CCC) is a joint research project"),
   A("operator", True, "Co-founded in 2017 by Erica Chenoweth (Harvard University) and Jeremy Pressman (University of Connecticut)"),
   A("date", True, "Co-founded in 2017"),
   A("claim boundary", True, "tracks and collects public data on political protests, marches, rallies, strikes, and acts of civil disobedience across the United States."),
   A("corpus", True, "Published regularly on Harvard Dataverse."),
   A("commitments", False)],
  {"kind": "same", "abn": False, "span": "The Crowd Counting Consortium (CCC) is a joint research project", "basis": "The consortium reached by name with founders, home, scope and data access."},
  "'CROWD COUNTING CONSORTIUM' ON THE OVERVIEW — THE CONSORTIUM AT ITS GRAIN; ITS VERIFICATION AND PRIVACY RULES NOT CARRIED",
  ("THE CONSORTIUM, SIGNED OUT, 2026-10-31: 'The Crowd Counting Consortium (CCC) is a joint research project that tracks and collects public data on political protests, marches, rallies, strikes, and acts of civil disobedience across the United States.' Founders, home, scope, scale, data access. Six cards: Harvard, Counting Crowds (two), boB Rudis, Policy Commons, X."),
  "The innocent reading first. Asked for the consortium, the Overview gives its founders, institutional home, scope and data.",
  ["THE SCOPE AT ITS GRAIN, WITH A NARROWING. 'Systematically logs public, nonviolent (and broader political) crowd events'. The consortium's page: 'We collect publicly available data on political crowds reported in the United States'; it does not restrict its count to nonviolent events.",
   "THE RULES NOT CARRIED. 'We only post records that we can confirm and verify through fact-checking.' and 'We will never post, release, or share identifying information that has not already been reported in the public' (the consortium's page)."],
  "Faithful on founders, home and data. The composition puts 'nonviolent' first in a scope the consortium states without it, and leaves out the verification and privacy rules that bound the record.",
  [C("Harvard University", "Crowd Counting Consortium – Ash Center"), C("Counting Crowds", "About - Counting Crowds"), C("boB Rudis", "Crowd Counting Consortium 2025 U.S. Protest Event Data"),
   C("Counting Crowds", "crowdcounters – Counting Crowds"), C("Policy Commons", "Crowd Counting Consortium - Policy Commons"), C("X·crowdcounting", "Crowd Counting (@crowdcounting) / X")],
  {"author": True, "inst": True, "id": False, "src": True}, "Founders and institutions named; the consortium's pages among the cards.")

# 12 Union Membership and Coverage Database
s = "unionstats"
parts["unionstats"] = mk("unionstats", "union-membership-and-coverage-database-aio-20261031", "Union Membership and Coverage Database", "paste-unionstats.txt",
  aset("ext-unionstats", s, "Union Membership and Coverage Database (Unionstats.com)", {
    "name": (["Union Membership and Coverage Database", "Unionstats"], None, ["title"]),
    "operator": (["Barry Hirsch", "Hirsch", "Macpherson", "William Even"], None, ["operator"]),
    "claim boundary": ([], "Private and public sector union membership, coverage and density estimates compiled from the monthly household Current Population Survey.", ["self_description"]),
    "corpus": ([], "Economy-wide estimates from 1973; by state, industry and occupation from 1983; by metropolitan area from 1986; the 2025 compilation completed 23 January 2026.", ["coverage_period", "latest"]),
    "commitments": ([], "Use of the data requires citation; small cells to be used cautiously.", ["citation_required", "limit_cells"])},
    SITE_TB.format(k="an Internet data resource of union membership and coverage")),
  [A("name", True, "Union Membership and Coverage Database from the CPS (Unionstats.com)"),
   A("operator", True, "is an annual internet data resource created and maintained by economists Barry Hirsch, David Macpherson, and William Even."),
   A("claim boundary", True, "Compiles private- and public-sector labor union membership, coverage, and density estimates from the monthly household Current Population Survey (CPS)"),
   A("corpus", True, "Economy-wide estimates: 1973–present"),
   A("commitments", False)],
  {"kind": "same", "abn": False, "span": "is an annual internet data resource created and maintained by economists Barry Hirsch, David Macpherson, and William Even.", "basis": "The database reached by name with its makers, source and series."},
  "'UNION MEMBERSHIP AND COVERAGE DATABASE' ON THE OVERVIEW — THE DATABASE AT ITS GRAIN; ITS CITATION RULE AND ITS SMALL-CELL CAUTION NOT CARRIED",
  ("THE DATABASE, SIGNED OUT, 2026-10-31: 'The Union Membership and Coverage Database is an annual internet data resource created and maintained by economists Barry Hirsch, David Macpherson, and William Even.' Source material; timeline; latest data; a request for the user's role. Three cards: the database, BLS, EPI."),
  "The innocent reading first. Asked for the database, the Overview gives its makers, its source survey and series, and the latest figure.",
  ["THE SERIES AT ITS GRAIN. The three start years (1973, 1983, 1986) are the database's own.",
   "THE TERMS NOT CARRIED. 'Use of data requires citation.' and 'CPS sample sizes are very small for some cells. Use such estimates cautiously.' (the database's pages). The composition asks the user's role ('academic research, labor organizing, policy analysis, or journalism') and does not carry the database's own conditions of use."],
  "Faithful on what the database is and where it comes from; its conditions of use, the citation it requires and the caution it attaches to small cells, are left out.",
  [C("Union Membership and Coverage Database", "Union Membership and Coverage Database"), C("Bureau of Labor Statistics (.gov)", "Union Members Summary - 2025 A01 Results - Bureau of Labor Statistics"), C("Economic Policy Institute", "Union membership data | Economic Policy Institute")],
  {"author": True, "inst": False, "id": False, "src": True}, "The three economists named; the database cited.")

# 13 Global Nonviolent Action Database
s = "gnad"
parts["gnad"] = mk("gnad", "global-nonviolent-action-database-aio-20261031", "Global Nonviolent Action Database", "paste-gnad.txt",
  aset("ext-gnad", s, "Global Nonviolent Action Database (Swarthmore College)", {
    "name": (["Global Nonviolent Action Database", "GNAD"], None, ["operator"]),
    "operator": (["Swarthmore College", "Swarthmore"], "Swarthmore College, with its Peace and Conflict Studies Program, the Peace Collection and the Lang Center.", ["operator"]),
    "claim boundary": ([], "Campaigns of nonviolent action, not movements: 1,200+ cases, 100+ countries, 400+ years.", ["unit", "count_cases", "count_years"]),
    "corpus": ([], "1,200+ case studies from 100+ countries.", ["count_cases", "count_countries"]),
    "commitments": ([], "Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 unless otherwise noted; a page of the database's limitations.", ["license", "limits_page"])},
    SITE_TB.format(k="a database of nonviolent action campaigns")),
  [A("name", True, "Global Nonviolent Action Database: Home"),
   A("operator", True, "is a free online project hosted by Swarthmore College"),
   A("claim boundary", True, "catalogues more than 1,200 nonviolent campaign case studies from over 100 countries."),
   A("corpus", True, "more than 1,200 nonviolent campaign case studies from over 100 countries"),
   A("commitments", False)],
  {"kind": "same", "abn": False, "span": "is a free online project hosted by Swarthmore College", "basis": "The database reached by name with its host, scope, clusters and tools."},
  "'GLOBAL NONVIOLENT ACTION DATABASE' ON THE OVERVIEW — THE DATABASE AT ITS GRAIN; '400 YEARS' AND 'ANCIENT EGYPT' IN ONE SENTENCE; ITS LIMITS AND LICENSE NOT CARRIED",
  ("THE DATABASE, SIGNED OUT, 2026-10-31: 'The Global Nonviolent Action Database is a free online project hosted by Swarthmore College that catalogues more than 1,200 nonviolent campaign case studies from over 100 countries.' Scope and timeline; clusters; waves; search; origin (2011). Six cards: the database (two), CNCR, Discuss Data, Policy Commons, Swarthmore."),
  "The innocent reading first. Asked for the database, the Overview gives its host, its scale, its clusters and how to search it.",
  ["THE RANGE IN ONE SENTENCE. 'Features historical and modern campaigns spanning over 400 years, with some records dating as far back as ancient Egypt and the 12th century BCE.' The database's home page gives '400+ years covered'.",
   "THE UNIT KEPT ON A CARD. The database's rule 'Campaigns, Not Movements' reaches the composition only through a card snippet ('excluding broad moveme...').",
   "THE LIMITS NOT CARRIED. The database links a page of its own 'Limitations of the Database' and a Creative Commons license (BY-NC-ND 4.0); the composition carries neither."],
  "Faithful on host and scale. The composition joins the database's stated range to an older case in one sentence, and leaves out the database's own statement of its unit, limits and license.",
  [C("Global Nonviolent Action Database", "Global Nonviolent Action Database: Home"), C("Global Nonviolent Action Database", "Nonviolent Action Case Map | Global Nonviolent Action Database"), C("www.nonviolent-conflict.org", "Swarthmore College's Global Nonviolent Action Database | CNCR"),
   C("Discuss Data", "Global Nonviolent Action Database - Discuss Data"), C("Policy Commons", "GNAD: Global Nonviolent Action Database - Policy Commons"), C("Swarthmore College", "Global Nonviolent Action Database - Peace & Conflict Studies Blog")],
  {"author": False, "inst": True, "id": False, "src": True}, "Swarthmore named; the database's pages among the cards.")

# 14 Labor Notes (AI Mode)
s = "labor-notes"
parts["labornotes"] = mk("labornotes", "labor-notes-aimode-20261031", "Labor Notes", "paste-labor-notes.txt",
  aset("ext-labor-notes", s, "Labor Notes", {
    "name": (["Labor Notes"], None, ["self_description"]),
    "operator": (["Labor Education and Research Project", "Labor Notes"], "Labor Notes; the site footer names the Labor Education and Research Project.", ["operator"]),
    "date": (["1979"], None, ["self_description"]),
    "claim boundary": ([], "A media and organizing project, the voice of union activists who want to put the movement back in the labor movement.", ["self_description"]),
    "corpus": ([], "The monthly magazine (11 issues a year), books and manuals, a biennial national conference and Troublemakers Schools.", ["magazine", "subscription", "conference", "schools"]),
    "purpose": ([], "To promote organizing, aggressive strategies and union democracy through a rank-and-file network.", ["what_we_promote", "network"]),
    "commitments": ([], "An independent publication, free to print the voices who say the movement could be doing better.", ["independent", "critique_leaders"])},
    SITE_TB.format(k="a media and organizing project of union activists")),
  [A("name", True, "Labor Notes is an American media and organizing project"),
   A("operator", False),
   A("date", True, "founded in 1979 by labor activist Kim Moody"),
   A("claim boundary", True, "it reports on rank-and-file union democracy, strikes, and independent worker-led organizing efforts."),
   A("corpus", True, "Publishes 11 issues annually covering shop-floor strategy, union elections, and grassroots campaigns across major sectors."),
   A("purpose", True, "Operating as a voice for the \"troublemaking wing\" of the labor movement"),
   A("commitments", False)],
  {"kind": "same", "abn": False, "span": "Labor Notes is an American media and organizing project", "basis": "The project reached by name with its founding, magazine, conference, schools and caucus work."},
  "'LABOR NOTES' IN AI MODE — THE PROJECT AT ITS GRAIN, ITS SUPPORT FOR REFORM CAUCUSES AND TDU GIVEN; ITS INDEPENDENCE TO PRINT CRITICISM OF LEADERS NOT CARRIED",
  ("THE PROJECT, SIGNED OUT, 2026-10-31, AI MODE: 'Labor Notes is an American media and organizing project founded in 1979 by labor activist Kim Moody.' Fact table (1979, Kim Moody, Detroit); core initiatives: the magazine, the biennial conference, workshops, movement building ('historically supporting factions like the Teamsters for a Democratic Union (TDU)')."),
  "The innocent reading first. Asked for the project, AI Mode gives its founding, its headquarters and its four lines of work, and offers more.",
  ["THE CAUCUSES CARRIED. 'Bridges isolated reform caucuses to help democratize major organizations, historically supporting factions like the Teamsters for a Democratic Union (TDU).' #1725 counts TDU among the structures that held critique inside a union by building a constituency able to replace officials.",
   "THE INDEPENDENCE NOT CARRIED. 'And as an independent publication, we’re free to include the voices who say we could be doing better—and tell how.' and 'For the most part, our leaders are doing a poor job of navigating us through the crisis.' (the project's About page). The organ that prints criticism of union leadership is the condition #1725 names; the composition gives the magazine's subjects and not its standing."],
  "Faithful, and close to #1725 where it names the caucuses Labor Notes supports. The project's own statement of why it can carry that criticism, its independence as a publication, is absent.",
  [C("Labor Notes", "Labor Notes |"), C("Wikipedia", "Labor Notes - Wikipedia"), C("Labor Notes", "Labor Notes | Brooklyn NY"), C("Labor Notes", "2024 Labor Notes Conference: April 19-21 | Labor Notes"),
   C("Labor Network for Sustainability", "Labor Notes 2024 Recap - Labor Network for Sustainability")],
  {"author": True, "inst": False, "id": False, "src": True}, "The founder named; the project's site and Wikipedia among the cards.",
  aimode="linked to wikipedia in place of popup, so ai mode", first="Labor Notes is an American media and organizing project")

# 15 Labor Vector (the archive's own site; existing set)
parts["laborvector"] = mk("laborvector", "laborvector-aio-20261031", "laborvector", "paste-laborvector.txt", None,
  [A("name", True, "www.laborvector.org"),
   A("operator", True, "a conceptual framework by Lee Sharks"),
   A("claim boundary", True, "maps the path semantic labor travels through a system: C → T → R → O → A (Capacity, Task-origin, Retrieval, Output, Attribution)."),
   A("presents", True, "Directionality of Semantic Labor — Lee Sharks | Labor Vector"),
   A("corpus", False)],
  {"kind": "same", "abn": False, "span": "Labor Vector is a conceptual framework by Lee Sharks", "basis": "The site reached at its run-together name as its framework, Directionality of Semantic Labor, attributed to Lee Sharks; the VectorStock homonym noted."},
  "'LABORVECTOR' ON THE OVERVIEW — THE SITE COMPOSED AS ITS FRAMEWORK, ATTRIBUTED; THE META-AGGREGATOR OF LABOR AND AI NOT CARRIED; THE SPACED NAME REACHES AN UNRELATED FIELD",
  ("THE SITE, SIGNED OUT, 2026-10-31: 'Labor Vector is a conceptual framework by Lee Sharks on the Labor Vector Website that maps the path semantic labor travels through a system: C → T → R → O → A (Capacity, Task-origin, Retrieval, Output, Attribution).' "
   "The five stages; a note on the VectorStock homonym. Two cards: laborvector.org ('Directionality of Semantic Labor — Lee Sharks | Labor Vector'), VectorStock."),
  "The innocent reading first. Asked for the run-together name, the Overview gives the site's framework stage by stage, attributes it, and separates the stock-graphics sense.",
  ["THE FRAMEWORK, ATTRIBUTED. The five stages are given at the site's grain and credited: 'a conceptual framework by Lee Sharks'.",
   "THE SITE'S TURN NOT CARRIED. The site's home page, saved the same day: '15 resources across five intersections, compiled 2026-10-29.' The meta-aggregator of labor and AI, the site's current work and a source of the maryleelabor census, is absent; the site is composed as its definition surface alone.",
   "THE SPACED NAME. The operator: 'labor vector pulled up totally unrelated, so laborvector'. That run is not pasted and is not seated; at the spaced name the field held another object."],
  "An attributed composition of the site's framework. The site's present work, the census of labor and AI, does not reach the composition, and the spaced form of the name belongs to another field.",
  [{"site": "www.laborvector.org", "title": "Directionality of Semantic Labor — Lee Sharks | Labor Vector", "snip": None, "rel": "archive_controlled", "note": "the archive's own site"}, C("VectorStock", "Labor Vector Images & Graphics for Commercial Use")],
  {"author": True, "inst": False, "id": False, "src": True}, "Lee Sharks named; the site cited.",
  target="ENT-d56958a10a", originator="laborvector.org, the archive's own site (Lee Sharks; Semantic Economy Institute / Crimson Hexagonal Archive; deposit #771 on its home page). Recorded 2026-10-31.", related=[1725, 771])

for k, v in parts.items():
    if v.get("atomset"):
        req = {a["atom"] for a in v["atomset"]["atoms"] if a["applicability"] == "required"}
        v["obs"]["atoms"] = [a for a in v["obs"]["atoms"] if a["atom"] in req]
    (P / f"{k}.json").write_text(json.dumps(v, ensure_ascii=False, indent=1), encoding="utf-8")
print("parts:", len(parts))
