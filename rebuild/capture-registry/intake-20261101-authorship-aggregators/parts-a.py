"""Reader a: eight of the authorship-census captures of 2026-11-01 (The NEXT, Electronic Literature Lab, Output, Wordcraft, CoAuthor, In2Writing,
Creative AI Lab database, Arquivo Pessoa), on helpers.py.
  python3 parts-a.py && python3 build.py --check --only the-next electronic-literature-lab output-anthology wordcraft coauthor in2writing creative-ai-lab-database arquivo-pessoa"""
from helpers import *

TB = "A web resource: its own pages, saved 2026-11-01, describe it as {k}. A site, read on the site template."
parts = {}

# 1 The NEXT
s = "the-next"
parts[s] = mk(s, "The NEXT Electronic Literature Organization",
  aset(s, {
    "name": (["The NEXT"], None, ["self_description", "wp_repository"]),
    "operator": (["Electronic Literature Lab", "Dene Grigar"], "Managed by the Electronic Literature Lab (Washington State University Vancouver), Dene Grigar its Managing Director and Curator, and supported by grants, donations and commissions; Wikipedia (third party) names Washington State University Vancouver and the Electronic Literature Organization as its supporters.", ["managed", "curator", "wp_repository"]),
    "date": (["2011"], "Established 2011 (Wikipedia, third party).", ["wp_established"]),
    "claim boundary": ([], "A combination museum, library and preservation space for digital art and writing, with open-access archives.", ["self_description", "open_access"]),
    "corpus": ([], "48 collections of digital art and writing: individual artists and scholars, online experimental journals from 1995 to the present, the Electronic Literature Collections, the ELO's historical media; over 3,000 works by 2022 (Wikipedia).", ["collections", "individual", "journals", "anthologies", "wp_count"]),
    "purpose": ([], "To maintain its archives and make them accessible for the next generation, answering the need for open-access, travel-free cultural and research experiences.", ["self_description", "open_access"]),
    "commitments": ([], "Works on obsolete software re-created by migration to newer systems, with as much metadata as possible where re-creation is not yet possible; works kept under the names they were published under (27 works under the pen name M.D. Coverley in the Luesebrink Collection).", ["wp_migrate", "wp_metadata_limit", "wp_coverley"]),
    "lineage": (["Electronic Literature Organization", "ELO"], "Created as the ELO's museum/library/preservation space, out of the ELO Repository.", ["repo_coming_soon", "repo_self"])},
    TB.format(k="a combination museum, library, and preservation space for digital art and writing")),
  [A("name", True, "The NEXT is a digital art and writing museum, library, and preservation space"),
   A("operator", True, "Curated and directed through the Electronic Literature Lab by Dene Grigar."),
   A("date", False),
   A("claim boundary", True, "preservation space offering open-access archives for the public and scholars"),
   A("corpus", True, "Features over 3,000 born-digital literary works and dozens of collections"),
   A("purpose", True, "Maintains and shares the cultural record of born-digital human expression."),
   A("commitments", False),
   A("lineage", True, "preservation space by the Electronic Literature Organization")],
  {"kind": "same", "abn": False, "span": "The NEXT is a digital art and writing museum, library, and preservation space", "basis": "The museum reached by name with its maker, its lab, its curator and its contents."},
  "'THE NEXT ELECTRONIC LITERATURE ORGANIZATION' ON THE OVERVIEW — THE MUSEUM, ITS LAB AND ITS CURATOR AT THEIR GRAIN; THE NAMES ITS WORKS STAND UNDER, A PEN NAME KEPT AS SUCH, NOT CARRIED",
  ("THE MUSEUM, SIGNED OUT, 2026-11-01: 'The NEXT is a digital art and writing museum, library, and preservation space created by the Electronic Literature Organization (ELO).' "
   "Key details: purpose ('Maintains and shares the cultural record of born-digital human expression'), contents ('over 3,000 born-digital literary works and dozens of collections ... dating from the mid-1980s onward'), support (the Electronic Literature Lab 'alongside the ELO'), leadership (Dene Grigar); two follow-up offers, the first to 'Search for a particular author or artist in the archive'. "
   "Six cards: the ELO, the-next.org (three), katyafarinsky.com, a YouTube talk by Dene Grigar."),
  "The innocent reading first. Asked for the museum under its organization's name, the Overview says what it is, who made it, what it holds, who runs it and who leads it, from the museum's own pages and the ELO's.",
  ["THE MUSEUM AT ITS GRAIN. 'Features over 3,000 born-digital literary works and dozens of collections (including hypertext, kinetic poetry, net art, interactive fiction, 3D, VR, and AI art)'. Wikipedia (saved): 'over 3,000 works by 2022'; the home page: 'the 48 collections of digital art and writing at The NEXT'. Card 3 carries the older figure, 'containing 30 collections', which Wikipedia gives as the museum's original holding ('originally housed 30 separate collections of 2,500 electronic literature works'). The ELO as maker agrees with the ELO Repository: 'Coming soon to ELO's newly created museum/library/preservation space, The NEXT'.",
   "THE HOLDER AT ITS GRAIN. 'Hosted and supported by the Electronic Literature Lab at Washington State University Vancouver alongside the ELO' and 'Curated and directed through the Electronic Literature Lab by Dene Grigar.' The home page: 'The NEXT is supported by grants, donations, and commissions and managed by the Electronic Literature Lab', with 'Dene Grigar, Managing Director and Curator'. The grants, donations and commissions are not carried; the Wikipedia year of establishment ('Established 2011') is not given.",
   "THE NAMES NOT CARRIED. The composition offers to 'Search for a particular author or artist in the archive' and names no author. The census row reads the museum's holding of authorship from Wikipedia's account of the Luesebrink Collection: 'Luesebrink created and published 27 of these works under the pen name M.D. Coverley', the works re-created by migration and kept under the name they were published under. Re-creation by migration, the museum's operation on a work, is likewise absent. 'AI art' stands among the contents; the home page lists 'Artificial Intelligence (AI)' among its collections' qualities; neither says how a machine's part in a work is attributed.",
   "THE ADDRESS. Three cards give the museum at the-next.org ('Welcome Space | The NEXT', 'The NEXT About Space', 'The Electronic Literature Organization Archives - The NEXT'); the census row gives https://the-next.eliterature.org/."],
  "An accurate composition of the museum, its maker and its holder. What the census reads it for, the names its works stand under and the migration that keeps a work under its author's name across obsolete software, is not carried.",
  [C("Electronic Literature Organization", "Electronic Literature Organization – To facilitate and promote the writing ...", "Oct 21, 2026 — An international organization dedicated to the investigation of literature produced for the digital medium. · Support the ELO!"),
   C("the-next.org", "Welcome Space | The NEXT", "Overview: The NEXT is a digital art and writing museum, library, and preservation space offering open-access archives for the public and scholars. Collections: ..."),
   C("katyafarinsky.com", "Electronic Literature Organization's The NEXT - Katya Farinsky", "Overview: The NEXT is a virtual museum, library, and preservation space by the Electronic Literature Organization containing 30 collections and over 3,000 globa..."),
   C("the-next.org", "The NEXT About Space", "OUR MISSION. At the heart of The NEXT is the concern of maintaining and sharing the cultural record of human expression, from the period Jay David Bolter ..."),
   C("YouTube·University of Kansas IDRH", "From the Net to the Web: Genres of Born-Digital Fiction - Dene Grigar", None, "third_party", "video card, 59:39"),
   C("the-next.org", "The Electronic Literature Organization Archives - The NEXT", "The NEXT is generously supported by the Electronic Literature Lab, Washington State University Vancouver, and the Electronic Literature Organization. Electronic...")],
  {"author": True, "inst": True, "id": False, "src": True}, "Dene Grigar, the Electronic Literature Lab, WSU Vancouver and the ELO named; the museum's own pages carded.")

# 2 Electronic Literature Lab
s = "electronic-literature-lab"
parts[s] = mk(s, "Electronic Literature Lab",
  aset(s, {
    "name": (["Electronic Literature Lab", "ELL"], None, ["self_description", "holdings"]),
    "operator": (["Washington State University Vancouver", "Dene Grigar"], "Washington State University Vancouver; directed by Dene Grigar.", ["operator", "director", "holdings"]),
    "claim boundary": ([], "A lab for advanced inquiry into born-digital literature, one of four U.S. media archaeology labs giving scholars access to obsolete digital works on appropriate equipment.", ["self_description", "media_archaeology"]),
    "corpus": ([], "61 vintage Macintosh computers and PCs dating back from 1977 and a library of 200 electronic literary works.", ["holdings"]),
    "purpose": ([], "Advanced inquiry into curating, preserving and producing born-digital literary works.", ["purpose"])},
    TB.format(k="a lab for advanced inquiry into born-digital literature")),
  [A("name", True, "The Electronic Literature Lab (ELL) is a media archaeology research facility"),
   A("operator", True, "directed by Dr. Dene Grigar at"),
   A("claim boundary", True, "A dedicated space where scholars and visitors can access historical media running on original vintage hardware."),
   A("corpus", True, "Maintains over 80 vintage Macintosh computers and PCs (dating back to 1977) along with a library of thousands of digital literary works"),
   A("purpose", True, "To archive, restore, conserve, and present born-digital art, literature, and video games from 1977 to the present.")],
  {"kind": "same", "abn": False, "span": "The Electronic Literature Lab (ELL) is a media archaeology research facility", "basis": "The lab reached by name with its director, university, holdings, rooms and address."},
  "'ELECTRONIC LITERATURE LAB' ON THE OVERVIEW — THE LAB AT ITS GRAIN FROM A SITE THE CENSUS DID NOT SAVE; ITS COUNTS LARGER THAN THE SAVED PAGE'S; ONE AUTHOR NAMED, IN A ROOM'S NAME",
  ("THE LAB, SIGNED OUT, 2026-11-01: 'The Electronic Literature Lab (ELL) is a media archaeology research facility founded in 2011 and directed by Dr. Dene Grigar at Washington State University Vancouver.' "
   "Mission (archive, restore, conserve and present 'born-digital art, literature, and video games from 1977 to the present'); collection ('over 80 vintage Macintosh computers and PCs', 'a library of thousands of digital literary works and retro video games'); archival center for the ELO and manager of The NEXT; four rooms (the Marjorie C. Luesebrink Reading Room, the Archives Room, the Restoration Room, the Studio); address, phone, electronicliteraturelab.org. "
   "Four cards: electronicliteraturelab.org, Washington State University, Wikipedia, Instagram."),
  "The innocent reading first. Asked for the lab, the Overview gives its founding, director, mission, holdings, rooms and contact details, mostly from the lab's own site.",
  ["THE COUNTS. 'over 80 vintage Macintosh computers and PCs (dating back to 1977)' and 'a library of thousands of digital literary works'. The page the census saved (Washington State University): 'ELL contains 61 vintage Macintosh computers and PCs, dating back from 1977 and a library of 200 electronic literary works.' That page's latest date is its list of '2021 Undergraduate Researchers'; the composition's first and most-cited card is electronicliteraturelab.org, which the census did not save. The census row's counts are the 2021-era page's.",
   "THE DATE. 'founded in 2011'. The census row gives no founding date. The NEXT's Wikipedia article, saved for the census, says 'The lab opened officially in 2011', and the composition's Wikipedia card, an article on the lab itself, gives 'founded 2011 by Dene Grigar'.",
   "THE LAB AND THE MUSEUM. 'Serves as the primary archiving center for the Electronic Literature Organization and manages The NEXT digital museum, library, and preservation space.' The NEXT's home page: 'managed by the Electronic Literature Lab'; Wikipedia: 'Physical artifacts are held at the Electronic Literature Lab'. The ELO archiving role is on no saved source.",
   "ONE AUTHOR, IN A ROOM'S NAME. The census row: 'the saved page names a library of 200 electronic literary works and lists none of their authors'. The composition names one, 'Marjorie C. Luesebrink Reading Room', under the civil name; The NEXT's Wikipedia account holds 27 of her works 'under the pen name M.D. Coverley'. The one work the composition names is a game ('Amnesia from 1986'), given without its author."],
  "The lab composed at its grain from its own newer site, with counts that exceed the 2021-era page the census rests on. Whose works the library holds, and under what names, is not carried; the one author named stands in the name of a room.",
  [C("electronicliteraturelab.org", "The Electronic Literature Lab", "Mission: Archive, restore, conserve, and produce born-digital art, literature, and video games (1977–present). Spaces: Marjorie C. Luesebrink Reading Room for a..."),
   C("Washington State University", "Electronic Literature Lab | Washington State University", "Electronic Literature Lab For Advanced Inquiry into Born Digital Literature Welcome to the Electronic Literature Lab (ELL) Directed by Dr. Dene Grigar, ELL cont..."),
   C("Wikipedia", "Electronic Literature Lab - Wikipedia", "Location: Washington State University, Vancouver (founded 2011 by Dene Grigar). Mission: Preserve, restore, and present early electronic literature, video games..."),
   C("Instagram·electronicliteraturelab", "Electronic Literature Lab (@electronicliteraturelab) - Instagram", "Behind the work of the Electronic Literature Lab are four spaces, each with its own role and purpose. 💾 The Archives Room Physical archives associated with The...")],
  {"author": True, "inst": True, "id": False, "src": True}, "Dene Grigar and WSU Vancouver named; the lab's two sites, Wikipedia and Instagram carded.")

# 3 Output
s = "output-anthology"
parts[s] = mk(s, "Output: An Anthology of Computer-Generated Text",
  aset(s, {
    "operator": (["Lillian-Yvonne Bertram", "Nick Montfort", "Counterpath", "MIT Press"], "Edited by Lillian-Yvonne Bertram and Nick Montfort; published by Counterpath, co-published with MIT Press.", ["editors", "copublished"]),
    "date": (["2024"], "October 2024.", ["copublished"]),
    "claim boundary": ([], "Seven decades of English-language outputs from computer generation systems; human–computer collaborations conceptually defined but not implemented as a computer system excluded.", ["self_description", "exclusion"]),
    "corpus": ([], "Outputs across creative writing, research-system text, reports and utilitarian texts, each excerpt introduced and organized by fine-grain genre; 500 pages.", ["scope", "unit", "size"]),
    "purpose": ([], "To correct the omission of the long history of text generation.", ["aim"]),
    "identifier": (["978-0262549813", "9780262549813"], "ISBN 978-0262549813.", ["isbn"])},
    "A book: its publisher's page, saved 2026-11-01, describes it as an anthology of seven decades of English-language outputs from computer generation systems. Read on the site template."),
  [A("operator", True, "is a 504-page collection edited by Lillian-Yvonne Bertram and Nick Montfort."),
   A("date", True, "and Counterpath Press on November 5, 2024"),
   A("claim boundary", True, "Focuses strictly on functional computer-generated systems and software output, deliberately excluding pure human-computer conceptual collaborations."),
   A("corpus", True, "Features 200 selections across fine-grained genres including poetry, prose, storytelling, conversations, humor, letters, reporting, rhetoric, and code."),
   A("purpose", False),
   A("identifier", True, "Paperback ISBN: 9780262549813")],
  {"kind": "same", "abn": False, "span": "is a 504-page collection edited by Lillian-Yvonne Bertram and Nick Montfort.", "basis": "The anthology reached by title with its editors, publishers, scope, exclusion and ISBN."},
  "'OUTPUT: AN ANTHOLOGY OF COMPUTER-GENERATED TEXT' ON THE OVERVIEW — THE BOOK AT ITS GRAIN FROM MIT PRESS; ITS EXCLUSION RULE LOOSENED; ITS ARGUMENT AGAINST A RECENT ORIGIN OF TEXT GENERATION NOT CARRIED",
  ("THE ANTHOLOGY, SIGNED OUT, 2026-11-01: 'Published by MIT Press and Counterpath Press on November 5, 2024, Output: An Anthology of Computer-Generated Text, 1953–2023 is a 504-page collection edited by Lillian-Yvonne Bertram and Nick Montfort.' "
   "Key details: timeframe; '200 selections across fine-grained genres'; scope ('deliberately excluding pure human-computer conceptual collaborations'); an honorable mention for the 2025 N. Katherine Hayles Award; paperback $45.00 and eBook $28.99; a follow-up offer naming 'Joseph E. Grimes' 1963 Fairy Tale Generator or Alison Knowles' The House of Dust'. "
   "Four cards: MIT Press, a YouTube talk (Center for Digital Narrative, UiB), Nick Montfort's blog, Google's Knowledge Graph notice."),
  "The innocent reading first. Asked for the book by its title, the Overview gives its publishers, date, length, editors, range, genres, scope, an award and its prices, mostly from the MIT Press page.",
  ["THE BOOK AT ITS GRAIN. Editors, range and genres agree with Counterpath's page ('organized by fine-grain genre including conversations, humor, letters, poetry, prose, and sentences'). The timeframe line reads 'from 1953 to 1953–2023'. '200 selections' and the Hayles Award mention are on no saved source.",
   "THE EDITION'S PARTICULARS. The composition and its MIT Press card: 'Pub date: November 5, 2024 504 pp.', paperback '$45.00'. Counterpath's page, the census row's source: 'October 2024', '500 pgs.', '$40.00; 7″ x 9″'. The ISBN agrees ('Paperback ISBN: 9780262549813'; 'ISBN 978-0262549813'). The census row's holder field carries Counterpath's month and price.",
   "THE EXCLUSION LOOSENED. Counterpath: 'Purposefully excluded are human–computer collaborations that were conceptually defined but not implemented as a computer system.' The composition: 'deliberately excluding pure human-computer conceptual collaborations'. The condition that does the excluding, a collaboration never implemented as a system, is dropped, and 'pure' is added; the census row reads this rule as what constitutes the record as output of implemented systems.",
   "THE PURPOSE NOT CARRIED. Counterpath sets the book against a recent origin: 'text generation, as it happens, was not invented yesterday in Silicon Valley', 'created long before ChatGPT', and the anthology 'aims to correct that omission'. The composition gives the years without the correction.",
   "ATTRIBUTION BY POSSESSIVE. The follow-up names two systems by their makers, 'Joseph E. Grimes' 1963 Fairy Tale Generator' and 'Alison Knowles' The House of Dust', each system under a person's name. The census row records the book's attribution practice (system, programmer, editor) as unrecorded on the saved page; how the book itself credits these outputs is not in any saved source."],
  "An accurate composition of the book as a catalogue item, taken from MIT Press, whose date, length and price differ from the Counterpath page the census rests on. The exclusion rule loses its condition, and the book's argument against a recent origin of machine text is absent.",
  [C("MIT Press", "Output - MIT Press", "Paperback ISBN: 9780262549813 Pub date: November 5, 2024 504 pp., 7 x 9 in, 41 b&w illus. MIT Press BookstorePenguin Random HouseAmazonBarnes and NobleBookshop."),
   C("YouTube·Center for Digital Narrative, UiB", "Output: An Anthology of Computer", "and Nick you're all familiar with uh Nick uses computation litary art he's a PI in the center. he has many books that include computerenerated books the deletio..."),
   C("Nick Montfort", "The OUTPUT Anthology is Out! – Post Position - Nick Montfort", "I'm delighted that after more than four years of work by Lillian-Yvonne Bertram and myself — we're co-editors of this book — the MIT Press and Counterpath have ..."),
   C("Google", "Google Watch Action Data", "This response uses data provided by Google's Knowledge Graph", "third_party", "the Knowledge Graph notice, carded")],
  {"author": True, "inst": True, "id": True, "src": True}, "Both editors and both publishers named; the ISBN on the MIT Press card.")

# 4 Wordcraft
s = "wordcraft"
parts[s] = mk(s, "Wordcraft Writers Workshop",
  aset(s, {
    "name": (["Wordcraft Writers Workshop"], None, ["self_description"]),
    "operator": (["PAIR", "Magenta", "Google"], "Google's PAIR and Magenta teams; conducted by Andy Coenen and Ann Yuan (PAIR), Daphne Ippolito and Sehmon Burnam (Magenta).", ["self_description", "conducted"]),
    "claim boundary": ([], "A collaboration of Google's PAIR and Magenta teams with 13 professional writers, who were given 8 weeks to use Wordcraft, a LaMDA-powered tool for writing stories with AI.", ["self_description", "cohort", "tool"]),
    "corpus": ([], "Thirteen stories, each under its writer's name (Robin Sloan, Allison Parrish, Aaron Winslow and others), of 1,000-1,500 words, with a whitepaper drawn from the writers' journals and interviews.", ["story_first", "story_parrish", "story_last", "story_length", "paper_title", "interviews"]),
    "purpose": ([], "To explore the limits of co-writing with LaMDA and foster an honest and earnest conversation about technology and creativity.", ["aim"]),
    "commitments": ([], "No instructions to the writers on how to use the tool or how much generated text to keep; the stories not authored under explicit guidance; Google does not endorse them; participants consented to publication and were compensated.", ["no_instruction", "writers_notice", "endorse", "consent"])},
    TB.format(k="a collaboration between Google's PAIR and Magenta teams and 13 professional writers")),
  [A("name", True, "The Wordcraft Writers Workshop was a 2022 research project"),
   A("operator", True, "by Google’s PAIR (People + AI Research) and Magenta teams"),
   A("claim boundary", True, "Participants used Wordcraft, an experimental text editor powered by Google’s LaMDA language model."),
   A("corpus", True, "Thirteen diverse professional authors (including Ken Liu, Robin Sloan, and Eugenia Triantafyllou) spent eight weeks writing short stories with the tool"),
   A("purpose", True, "that explored AI-augmented creative writing."),
   A("commitments", False)],
  {"kind": "same", "abn": False, "span": "The Wordcraft Writers Workshop was a 2022 research project", "basis": "The workshop reached by name with its teams, tool, cohort and findings, and its reception in 2026."},
  "'WORDCRAFT WRITERS WORKSHOP' ON THE OVERVIEW — THE WORKSHOP DATED 2022 AND COMPOSED AT ITS GRAIN; A 2026 BACKLASH AGAINST ITS WRITERS ADDED; HOW MUCH OF EACH STORY THE MODEL WROTE NOT CARRIED",
  ("THE WORKSHOP, SIGNED OUT, 2026-11-01: 'The Wordcraft Writers Workshop was a 2022 research project by Google’s PAIR (People + AI Research) and Magenta teams that explored AI-augmented creative writing.' "
   "Overview and setup (the tool, its features, the cohort 'under non-disclosure agreements', the results); '2026 Literary Backlash' (the project 'resurfaced widely on social media (such as Bluesky)' in August 2026; the criticism that participants 'had lent credibility to AI models trained on copyrighted literary works without consent'; participants' responses). "
   "Eight cards: Google (two), Magenta, ActuIA, The Algorithmic Bridge, Engadget, Coralflavor, Mezha."),
  "The innocent reading first. Asked for the workshop, the Overview gives its year, teams, tool, cohort and results, then the controversy over it in 2026, from Google's pages and press coverage.",
  ["THE WORKSHOP AT ITS GRAIN. Teams, tool, the thirteen writers and the eight weeks agree with the site ('The workshop cohort consisted of 13 professional writers, who were given 8 weeks to use Wordcraft'); the three writers named are on the home page's list of stories. 'rehashed cliches' and writer's block are on the learn page ('Many authors noted that generations tended to fall into clichés'). 'under non-disclosure agreements' is on no saved source; the paper's terms are consent to publication and compensation ('Participants were compensated for participating in the study').",
   "THE YEAR. 'a 2022 research project'; the Engadget card, 'Participation In 2022 Google AI Study'; Mezha, 'Google's 2022 AI experiment'. The census row: 'no date for the workshop in the saved sources (the paper cites work of 2022)'.",
   "THE BACKLASH OF 2026. 'In August 2026, the project resurfaced widely on social media (such as Bluesky) after being highlighted by author Lily Lachance.' Three of the eight cards are its coverage (Engadget, Coralflavor, Mezha). The census row, built 2026-11-01, gives the workshop as 'historical', 'a completed eight-week workshop', and records nothing of this reception; its reading cites only the writers' own fear of 'reputational harm' from plagiarized suggestions.",
   "THE DIVISION OF TEXT NOT CARRIED. The paper records how far each story was generated: 'largely formed around generated text (AP, DH, JM, MT, AW)', 'the bulk of the story text was written by the authors themselves (KL, WT, NG)', one writer who 'siloed out specific sections' (RS); the site's notice says the writers 'have not authored these stories under any sort of explicit guidance or instruction'. The composition says the tool 'required heavy manual filtering' and does not say whose name each story stands under or how much of it the model wrote; the criticism it reports falls on the writers as participants."],
  "The workshop composed at its grain and dated, with a reception the census row does not record. The paper's account of each writer's share of the text, the census row's ground for reading authorship as held by the named writer, is absent.",
  [C("Google", "Wordcraft Writers Workshop", "Collaboration: Wordcraft Writers Workshop between Google PAIR, Magenta teams, and 13 professional writers exploring AI co-writing limits with LaMDA and technolo..."),
   C("magenta.withgoogle.com", "The Wordcraft Writers Workshop: Creative Co-Writing with AI", "Project: Wordcraft Writers Workshop by Magenta; AI-augmented text editor utilizing LaMDA for creative writing assistance. Participants: 13 professional creative..."),
   C("ActuIA", "The Wordcraft Writers Workshop evaluates Wordcraft, Google's creative writing tool", "Wordcraft isn't the first AI to invite itself into literature, in fact we dedicated a feature to this topic in issue #8 of our magazine . In 2015, Tencent devel..."),
   C("The Algorithmic Bridge", "Google's Wordcraft: An AI Writing Tool Powered by LaMDA", "Besides the basics, Google added a feature I haven't seen anywhere else that they call “freeform prompting.” Given the context, the user can ask Wordcraft to ge..."),
   C("Engadget", "Authors Face Backlash For Participation In 2022 Google AI Study - Engadget", "Much of the ire directed toward participants in the Wordcraft study stems from the practice of tech companies training LLMs, often without authors' permission, ..."),
   C("Coralflavor", "The 2022 AI Writing Experiment That Became a 2026 Ethical Minefield", "What this means FAQ What was the Wordcraft Writers Workshop? The Wordcraft Writers Workshop was a 2022 Google-affiliated research project that brought together ..."),
   C("Mezha", "13 writers came under fire for Google's 2022 AI experiment - Межа", "Myroslav Trinko News editor of the Mezha. Geek, programmer by training, but journalist by profession. Horse rider, tennis player, and Formula 1 fan. I write abo..."),
   C("Google", "Wordcraft Writers Workshop", "The Wordcraft Writers Workshop is a collaboration between Google's PAIR and Magenta teams, and 13 professional writers from a diverse set of creative writing ba...")],
  {"author": False, "inst": True, "id": False, "src": True}, "Google's PAIR and Magenta teams named; the researchers who conducted it not named; the site and press carded.")

# 5 CoAuthor
s = "coauthor"
parts[s] = mk(s, "CoAuthor dataset",
  aset(s, {
    "name": (["CoAuthor"], None, ["kind"]),
    "operator": (["Mina Lee", "Percy Liang", "Qian Yang"], "Mina Lee, Percy Liang and Qian Yang, the paper's authors.", ["authors"]),
    "date": (["2022"], "Published at CHI 2022 (arXiv v1 18 January 2022).", ["venue", "dates"]),
    "claim boundary": ([], "A dataset designed for revealing GPT-3's capabilities in assisting creative and argumentative writing.", ["kind"]),
    "corpus": ([], "Interactions between 63 writers and four instances of GPT-3 across 1445 writing sessions.", ["count"]),
    "purpose": ([], "To address questions about GPT-3's language, ideation and collaboration capabilities and reveal its contribution as a writing 'collaborator' under various definitions of good collaboration, since LMs' capabilities are difficult to grasp.", ["function", "problem"]),
    "commitments": ([], "The dataset and a replay interface publicly available.", ["access"])},
    "A dataset: its paper's arXiv page, saved 2026-11-01, describes it as a dataset designed for revealing GPT-3's capabilities in assisting creative and argumentative writing (the dataset's home page could not be read). Read on the site template."),
  [A("name", True, "CoAuthor records timestamped events"),
   A("operator", True, "developed by researchers Mina Lee, Percy Liang, and Qian Yang"),
   A("date", True, "Qian Yang (CHI 2022)"),
   A("claim boundary", True, "process-oriented dataset capturing human-AI collaborative writing interactions"),
   A("corpus", True, "63 qualified crowd workers from Amazon Mechanical Turk paired with 4 instances of GPT-3."),
   A("purpose", False),
   A("commitments", True, "Download the full dataset, metadata, and survey responses at")],
  {"kind": "same", "abn": False, "span": "process-oriented dataset capturing human-AI collaborative writing interactions", "basis": "The dataset reached by name with its authors, venue, statistics, logging, interface and access points."},
  "'COAUTHOR DATASET' ON THE OVERVIEW — THE DATASET AT A FINER GRAIN THAN THE CENSUS'S SOURCE, FROM ITS OWN SITE; THE WRITERS GIVEN AS CROWD WORKERS AND THE TEXT DIVIDED BY PERCENTAGE",
  ("THE DATASET, SIGNED OUT, 2026-11-01: 'The CoAuthor Dataset is a large-scale, process-oriented dataset capturing human-AI collaborative writing interactions developed by researchers Mina Lee, Percy Liang, and Qian Yang (CHI 2022).' "
   "Statistics (1,445 sessions; '63 qualified crowd workers from Amazon Mechanical Turk'; 830 stories by 58 writers, 615 essays by 49; 'Suggestion acceptance rate: 72.3%'; 'Human-authored text proportion: 72.6%'); keystroke-level logging; the Tab-key interface; davinci configurations; access (the Stanford site, GitHub, ACM, arXiv:2201.06796). "
   "Five cards: Stanford University, arXiv, ACM Digital Library, GitHub, alphaXiv."),
  "The innocent reading first. Asked for the dataset, the Overview gives its authors, size, composition, mechanics and where to get it, from its site, its paper and its code.",
  ["THE DATASET AT A FINER GRAIN. The arXiv abstract, the census row's one source: 'CoAuthor captures rich interactions between 63 writers and four instances of GPT-3 across 1445 writing sessions.' The composition adds the split by genre, the prompt sources (r/WritingPrompts, The New York Times), the averages and rates, from the Stanford card ('Creative writing: 830 stories written by 58 writers Argumentative writing: 615 essays written by 49 writers'). The census row: 'the dataset's home page could not be read' and 'whether the site and replay interface answer today is unrecorded'. The site is indexed and carded on 2026-11-01, and the code repository with it ('GitHub - minalee-research/coauthor-interface').",
   "THE WRITERS AS CROWD WORKERS. 'Participants: 63 qualified crowd workers from Amazon Mechanical Turk'. The census row: 'the abstract counts 63 writers and does not say whether or how they are named'. The composition says where the writers were recruited and names none of them.",
   "THE TEXT DIVIDED BY PERCENTAGE. 'Human-authored text proportion: 72.6%.' The census row's function field: 'how authorship of a session's text is assigned is not recorded in the saved source'. The composition gives an aggregate share of human-authored text, a measure the saved abstract does not carry; the measure is of the dataset, and no session's text is assigned to anyone.",
   "THE COLLABORATOR NOT CARRIED. The abstract reads the model's part as 'its contribution as a writing \"collaborator\" under various definitions of good collaboration'. The composition gives the interaction as rates ('Queries per session: 11.8 queries') and its follow-up offers 'specific findings regarding human-AI collaboration' without stating any."],
  "The dataset composed more finely than the census's saved abstract allows, from the dataset's own site, which the census could not read. It counts the writers, recruits them from a crowd platform and divides the text by percentage; the abstract's frame, the model as 'collaborator' under definitions of collaboration, is not carried.",
  [C("Stanford University", "CoAuthor – Human-AI Collaborative Writing Dataset", "Types of writing - Creative & Argumentative Creative writing: 830 stories written by 58 writers Argumentative writing: 615 essays written by 49 writers Writing ..."),
   C("arXiv", "[2201.06796] CoAuthor: Designing a Human-AI Collaborative Writing Dataset for Exploring Language Model Capabilities", "Dataset: CoAuthor (designed for revealing GPT-3's capabilities in creative and argumentative writing). Participants: 63 writers and 4 instances of GPT-3. Sessio..."),
   C("ACM Digital Library", "CoAuthor: Designing a Human-AI Collaborative Writing Dataset for Exploring Language Model Capabilities | Proceedings of the 2022 CHI Conference on Human Factors in Computing Systems", "CoAuthor Dataset: Human-AI collaborative writing interactions (63 writers, 4 GPT-3 instances, 1445 writing sessions). Purpose: Reveal GPT-3 capabilities in crea..."),
   C("GitHub", "GitHub - minalee-research/coauthor-interface", "This repository contains the code for the interface of CoAuthor. The interface comes in two parts: (1) the frontend presented to the users for writing with AI a..."),
   C("alphaXiv", "CoAuthor: Designing a Human-AI Collaborative Writing Dataset ... - alphaXiv", "Process-Oriented Data Collection: Rather than simply collecting final outputs, CoAuthor records every interaction as timestamped events, including text insertio...")],
  {"author": True, "inst": True, "id": True, "src": True}, "The three authors named; Stanford and ACM named; arXiv:2201.06796 given; site, paper and code carded.")

# 6 In2Writing
s = "in2writing"
parts[s] = mk(s, "In2Writing workshop",
  aset(s, {
    "name": (["In2Writing", "Intelligent and Interactive Writing Assistants"], None, ["venue"]),
    "operator": (["Association for Computational Linguistics", "Katy Gero", "Mina Lee", "Ting-Hao", "Vishakh Padmakumar"], "The editors named per volume (2022: Huang, Raheja, Kang, Chung, Gissin, Lee, Gero; 2025: Padmakumar, Gero, Wambsganss, Sterman, Huang, Zhou, Chung); published by the Association for Computational Linguistics.", ["editors_2022", "editors_2025", "publisher"]),
    "date": (["2022"], "The First Workshop, Dublin, May 2022.", ["vol_2022", "place_2022"]),
    "claim boundary": ([], "A workshop series on intelligent and interactive writing assistants, its proceedings held as an ACL Anthology venue.", ["venue", "vol_2022", "vol_2025"]),
    "corpus": ([], "15 papers in the first workshop (Dublin, May 2022, with ACL's 60th Annual Meeting) and 11 in the fourth (Albuquerque, May 2025, with NAACL), on human-AI co-writing, control and ownership, student writer voice, and reader judgements of AI-assisted literary text.", ["vol_2022", "acl_2022", "vol_2025", "place_2025", "naacl_2025", "ownership_paper", "pure_poet_title"]),
    "commitments": ([], "Materials published in or after 2016 under CC BY 4.0; the Anthology built by a team of volunteers.", ["license", "volunteers"]),
    "identifier": (["in2writing", "10.18653/v1/2025.in2writing-1", "979-8-89176-239-8"], "Venue ID in2writing; the 2025 volume DOI 10.18653/v1/2025.in2writing-1, ISBN 979-8-89176-239-8.", ["venue", "doi_2025"])},
    TB.format(k="a workshop series whose proceedings are an ACL Anthology venue")),
  [A("name", True, "Name: Workshop on Intelligent and Interactive Writing Assistants (In2Writing)"),
   A("operator", False),
   A("date", False),
   A("claim boundary", True, "The In2Writing workshop is an academic event focused on Intelligent and Interactive Writing Assistants."),
   A("corpus", True, "featuring 11 papers on topics like scientific figure captions, Arabic write-and-improve tools, and AI writing assistants in universities."),
   A("commitments", False),
   A("identifier", True, "Venue ID: in2writing")],
  {"kind": "same", "abn": False, "span": "The In2Writing workshop is an academic event focused on Intelligent and Interactive Writing Assistants.", "basis": "The workshop series reached by name with its purpose, two of its editions and its website."},
  "'IN2WRITING WORKSHOP' ON THE OVERVIEW — THE SERIES BY ITS THIRD AND FOURTH EDITIONS, TWO OF THEM AT CHI THAT THE CENSUS DOES NOT HAVE; THE FIRST WORKSHOP AND ITS READER STUDY NOT CARRIED; NO EDITOR NAMED",
  ("THE SERIES, SIGNED OUT, 2026-11-01: 'The In2Writing workshop is an academic event focused on Intelligent and Interactive Writing Assistants.' "
   "Overview: name; purpose ('To facilitate interdisciplinary discussions around writing assistants, human-AI co-writing, education risks, and the future of writing tools'); past events ('In2Writing 2024 (Third Workshop): Held in Honolulu in May 2024 (proceedings published by ACM)'; the Fourth, Albuquerque, May 2025, with NAACL, '11 papers'); the official website. "
   "Six cards: GitHub, ACM Digital Library, ACL Anthology (two), OpenReview, acm sigchi."),
  "The innocent reading first. Asked for the workshop, the Overview names it, states its purpose and gives its two most recent editions and its website.",
  ["TWO EDITIONS THE CENSUS DOES NOT HAVE. 'In2Writing 2024 (Third Workshop): Held in Honolulu in May 2024 (proceedings published by ACM).' The acm sigchi card: 'We will build off the successful workshop at CHI23 (The Second In2Writing Workshop)'. The ACL Anthology venue page the census saved lists two volumes, 2022 ('15 papers') and 2025 ('11 papers'), and the census row's record object counts only the first and the fourth. The second and third workshops, held at CHI and published by ACM, are outside the census row.",
   "THE FOURTH AT ITS GRAIN. '11 papers' and the place and partner agree with the 2025 volume ('Month: May Year: 2025 Address: Albuquerque, New Mexico, US'). 'AI writing assistants in universities' answers the volume's Tanzania survey ('a structured survey of 1,005 university students'). The 2025 paper the census row reads for authorship, 'Interaction-Required Suggestions for Control, Ownership, and Awareness in Human- AI Co-Writing', is not named.",
   "THE FIRST WORKSHOP NOT CARRIED. The composition does not mention 2022. The census row's reading rests on that volume's reader study: 'Participants’ task was to decide whether a continuation was written with an AI-tool or not', with 'low accuracy for differentiating between text types' and overconfidence. The series' founding year, its Dublin meeting and that study are absent.",
   "NO EDITOR NAMED. The census names seven editors per volume ('Ting-Hao 'Kenneth' Huang , Vipul Raheja , Dongyeop Kang ...'; 'Vishakh Padmakumar , Katy Gero ...') and the ACL as publisher. The composition names ACM for the third volume and NAACL as the fourth's host, and no person. Its official website is a GitHub page; the census row's address is the ACL Anthology venue, whose identifier the composition carries only on a card ('Acronym: In2Writing; Venue ID: in2writing')."],
  "The series composed by its latest editions, two of them at CHI and absent from the census row. The first workshop, whose reader study is the census row's reason for holding the series, and every editor are absent.",
  [C("GitHub", "In2Writing", "The purpose of this interdisciplinary workshop is to facilitate discussion around writing assistants, thereby enhancing our understanding of their usage in ..."),
   C("ACM Digital Library", "Proceedings of the Third Workshop on Intelligent and Interactive Writing Assistants | ACM Other conferences", "Proceedings: In2Writing '24, Third Workshop on Intelligent and Interactive Writing Assistants (Honolulu, May 2024; published October 2024 by ACM). Core Research..."),
   C("ACL Anthology", "Workshop on Intelligent and Interactive Writing Assistants (2025) - ACL Anthology", "Proceedings: Fourth Workshop on Intelligent and Interactive Writing Assistants (In2Writing 2025) containing 11 papers. Papers: Understanding Writing Assistants ..."),
   C("OpenReview", "NAACL 2025 Workshop In2Writing - OpenReview", "In2Writing: The Fourth Workshop on Intelligent and Interactive Writing Assistants. In2Writing 2025. Albuquerque, New Mexico, United StatesMay 04 ..."),
   C("ACL Anthology", "Workshop on Intelligent and Interactive Writing Assistants - ACL Anthology", "Workshop on Intelligent and Interactive Writing Assistants (In2Writing). Acronym: In2Writing; Venue ID: in2writing. 2025 · Proceedings of the Fourth Workshop on..."),
   C("acm sigchi", "The Third Workshop on Intelligent and Interactive Writing Assistants - CHI '24", "We will build off the successful workshop at CHI23 (The Second In2Writing Workshop), bringing new voices to the vibrant community of writing tools ...")],
  {"author": False, "inst": True, "id": True, "src": True}, "ACM and NAACL named, no editor; the venue ID on an ACL Anthology card; proceedings carded.")

# 7 Creative AI Lab database
s = "creative-ai-lab-database"
parts[s] = mk(s, "Creative AI Lab database",
  aset(s, {
    "name": (["Creative AI Lab", "Creative AI Tools & Resources Database"], None, ["serp_database", "kcl_ongoing"]),
    "operator": (["Serpentine", "King's College London", "King’s College London", "Department of Digital Humanities", "AHRC"], "The Creative AI Lab, a partnership between Serpentine R&D Platform and the Department of Digital Humanities, King's College London; funded by the AHRC and a LAHP PhD scholarship.", ["serp_partnership", "kcl_collaboration", "kcl_funding"]),
    "date": (["2020", "9 July", "July 9"], "Launched 9 July 2020.", ["serp_ongoing", "kcl_launch"]),
    "claim boundary": ([], "A database of tools for artists, designers, engineers, curators and researchers: software, research, theory and education at the intersection of art and AI.", ["serp_database", "kcl_launch"]),
    "corpus": ([], "At launch, a list of 65 essential tools contributed by the curator and researcher Luba Elliott (HOLO, third party).", ["holo_65_tools"]),
    "purpose": ([], "To aggregate tools and resources for practitioners incorporating machine learning and other forms of AI into their practice.", ["kcl_ongoing", "holo_aggregate"])},
    "A database: its operators' pages (Serpentine, King's College London) and a third-party launch report (HOLO), saved 2026-11-01, describe it as an ongoing project to aggregate tools and resources for practitioners incorporating machine learning and AI (the database itself unread). Read on the site template."),
  [A("name", True, "The Creative AI Tools & Resources Database"),
   A("operator", True, "is a joint research partnership between Serpentine Arts Technologies and the Department of Digital Humanities at King's College London."),
   A("date", True, "Launch Date: July 9, 2020"),
   A("claim boundary", True, "tools for artists, designers, engineers, curators, and researchers."),
   A("corpus", True, "Audio: Mustango, Synplant 2, Stable Audio, RAVE, Neutone, Semilla, DDSP"),
   A("purpose", True, "Purpose: An ongoing online database aggregating machine learning and artificial intelligence tools")],
  {"kind": "same", "abn": False, "span": "is a joint research partnership between Serpentine Arts Technologies and the Department of Digital Humanities at King's College London.", "basis": "The lab and its database reached by name with partners, funders, launch date, criteria and tool categories."},
  "'CREATIVE AI LAB DATABASE' ON THE OVERVIEW — THE DATABASE IN ITS CURRENT STATE, FROM PAGES THE CENSUS COULD NOT READ; ITS LAUNCH CONTRIBUTOR NOT NAMED; A FUNDER ON NO SAVED SOURCE",
  ("THE DATABASE, SIGNED OUT, 2026-11-01: 'The Creative AI Lab is a joint research partnership between Serpentine Arts Technologies and the Department of Digital Humanities at King's College London.' "
   "Key overview (launch date; partners and funders, among them 'Google's Artists + Machine Intelligence Grant'; core mission); the database (purpose; evaluation criteria 'transparency, creative malleability, technical interoperability, research caliber, and public value'; four categories of tools, Audio to Detection / Tracking). "
   "Four cards: Serpentine, Creative AI Lab (two), King's College London."),
  "The innocent reading first. Asked for the database, the Overview introduces the lab, its partners, funders and mission, then the database's purpose, criteria and listed tools.",
  ["THE DATABASE IN ITS CURRENT STATE. The tool lists carry Sora, DALL-E 3, Runway Gen-2 and Stable Audio, and the criteria list five values; the composition's fourth card is the lab's own site ('Audio: Mustango (multimodal LLM, LDM/Flan-T5); Synplant 2 ...'). The census row: 'the database's own page was script-rendered and unread', its corpus resting on the launch reports of 2020. The database's current contents and criteria are indexed and composed.",
   "THE CONTRIBUTOR NOT NAMED. HOLO, at the launch: 'One of the launch highlights is a list of 65 essential tools, contributed by creative AI curator and researcher Luba Elliott.' The census row reads this as the one contribution credited by name. The composition names no person.",
   "THE FUNDERS. 'Serpentine Galleries, King's College London, the Arts and Humanities Research Council (AHRC), and Google's Artists + Machine Intelligence Grant.' King's College London: 'The project is supported by funding from the AHRC and by a LAHP funded PhD scholarship.' The Google grant is on no saved source; the LAHP scholarship is not carried. 'Serpentine Arts Technologies' is the name the saved Serpentine page uses for its programme ('Eva Jäger – Arts Technologies, Serpentine, London'), beside 'Serpentine R&D Platform' in its partnership line. Card 2 dates the lab 'established in 2019'; the saved sources give the launch as '9 Jul 2020'.",
   "AUTHORSHIP NOT CARRIED. The Serpentine programme held 'a discussion around the impact of artificial intelligence on human-centered notions of creative agency, authorship and ownership' (15 November 2021), the census row's one point of contact with its question. The composition's mission ('demystify back-end AI and machine learning (ML) systems') does not touch it."],
  "The database composed in a state later than any saved source, from the lab's own site. The one person the launch credited, and the programme's question of authorship, are absent.",
  [C("Serpentine", "Creative AI Lab - Serpentine Galleries", "Overview: Creative AI Lab is an ongoing online research programme launched July 9, 2020, in partnership with the Department of Digital Humanities, King's Colleg..."),
   C("Creative AI Lab", "Creative AI Lab", "Overview: Collaborative research initiative by Serpentine Arts Technologies and King's College London Department of Digital Humanities established in 2019 inves..."),
   C("King's College London", "Creative AI Lab | King's College London", "Partnership: Collaboration between Serpentine R&D Platform and Department of Digital Humanities at King's College London. Aims: Surface back-end AI/ML knowledge..."),
   C("Creative AI Lab", "Creative AI Lab", "Audio: Mustango (multimodal LLM, LDM/Flan-T5); Synplant 2 (exploratory plug-in/Genopatch); Stable Audio (Stability AI); RAVE (realtime autoencoder); Neutone (Mo...")],
  {"author": False, "inst": True, "id": False, "src": True}, "Serpentine, King's College London and funders named; no person; the lab's site and its partners carded.")

# 8 Arquivo Pessoa
s = "arquivo-pessoa"
parts[s] = mk(s, "Arquivo Pessoa",
  aset(s, {
    "operator": (["Obra Aberta", "Leonor Areal"], "Edited by Obra Aberta CRL (2008); conception and direction by Leonor Areal; partners the Instituto de Estudos sobre o Modernismo (FCSH, UNL, Lisboa) and Assírio&Alvim.", ["edition", "direction", "partners"]),
    "date": (["2008", "1997"], "The online edition 2008; the original edition 1997.", ["edition", "original_edition"]),
    "claim boundary": ([], "The published work of Fernando Pessoa ('Obra de Fernando Pessoa'), with facsimile and information sections.", ["self_description", "sections"]),
    "corpus": ([], "The work under the names it bears: the author index, headed 'Ortónimo, pseudónimos e heterónimos de Fernando Pessoa', lists 39 names, with joint attributions kept as joint ('Álvaro de Campos e Ricardo Reis', 'Wardour + Pessoa').", ["authors_heading", "authors_first", "authors_soares", "authors_reis", "authors_joint"]),
    "purpose": ([], "Free expeditions for lovers and scholars ('Expedições livres para amantes e estudiosos').", ["self_description"]),
    "commitments": ([], "Four of the names each given a reader of their own in the audio: Alberto Pimenta (Ricardo Reis), José Abreu (Alberto Caeiro), José Lopes (Álvaro de Campos), Teresa Faria (Fernando Pessoa).", ["readings"]),
    "lineage": (["Texto Editora", "Casa Fernando Pessoa", "1997"], "From the original edition of Texto Editora and Casa Fernando Pessoa, 1997.", ["original_edition"])},
    TB.format(k="an online edition of the published work of Fernando Pessoa")),
  [A("operator", True, "directed by Leonor Areal"),
   A("date", True, "Created between 1997 and 2008"),
   A("claim boundary", True, "is a digital library and database dedicated to the published work of the Portuguese writer Fernando Pessoa."),
   A("corpus", True, "poetry, prose, heteronyms, and orthonyms"),
   A("purpose", True, "easy navigation for both casual readers and academic researchers"),
   A("commitments", False),
   A("lineage", True, "evolved from an earlier 1997 multimedia CD-ROM")],
  {"kind": "same", "abn": False, "span": "is a digital library and database dedicated to the published work of the Portuguese writer Fernando Pessoa.", "basis": "The edition reached by name with its address, origin, director, sections and tools."},
  "'ARQUIVO PESSOA' ON THE OVERVIEW — THE EDITION OF THE PUBLISHED WORK AT ITS GRAIN; THE ORTHONYM'S POETRY DROPPED FROM ITS LIST; THE PSEUDONYMS AND THE JOINT ATTRIBUTIONS NOT CARRIED; THE EDITION CREDITED TO A PARTNER",
  ("THE EDITION, SIGNED OUT, 2026-11-01: 'The Arquivo Pessoa is a digital library and database dedicated to the published work of the Portuguese writer Fernando Pessoa.' "
   "Key details: arquivopessoa.net; origin ('Created between 1997 and 2008 by the Institute of Studies into Modernism at Lisbon's Universidade Nova, directed by Leonor Areal, and evolved from an earlier 1997 multimedia CD-ROM'); contents ('Pessoa’s poetry, prose, heteronyms, and orthonyms'), five categories listed; features (search, the 'Labirinto' with 'audio readings and images'). "
   "Three cards: the edition's home and Info pages, Art and Soul Group. The paste ends on the third card."),
  "The innocent reading first. Asked for the archive, the Overview says what it holds, where it is, who made it and when, lists its main sections and describes its tools.",
  ["THE SECTIONS, ONE DROPPED. The home-page card: '1. Poemas de Alberto Caeiro 2. Poesia de Álvaro de Campos 3. Odes de Ricardo Reis 4. Poesia Ortónima de Fernando Pessoa 5. Livro do Desa...'. The composition lists Caeiro, Campos, Reis, 'Livro do Desassossego' and 'Mensagem': the fourth section, the orthonym's poetry, falls out, and the orthonym stays in the list only through Mensagem, a title the list does not attribute.",
   "THE CLASSES OF NAME. 'Pessoa’s poetry, prose, heteronyms, and orthonyms'. The author index: 'Ortónimo, pseudónimos e heterónimos de Fernando Pessoa', one orthonym, then the pseudonyms and heteronyms, 39 names in all. The composition puts the orthonym in the plural and does not carry the pseudonyms, the third class; the joint attributions the index keeps ('Álvaro de Campos e Ricardo Reis', 'Wardour + Pessoa', 'A. L. Caeiro e J. Caeiro') are absent. The census row reads the index as the work held under the names it bears, answerable to one name, 'Obra de Fernando Pessoa'; the composition gives the heteronyms as contents of a corpus.",
   "THE EDITION CREDITED TO A PARTNER. 'Created between 1997 and 2008 by the Institute of Studies into Modernism at Lisbon's Universidade Nova, directed by Leonor Areal'. The edition's own technical sheet: 'Edição: Obra Aberta CRL, 2008', 'Concepção e direcção: Leonor Areal', with the Instituto de Estudos sobre o Modernismo under 'Parcerias'. The composition's wording follows the Art and Soul card ('Between 1997 and 2008 the Institute of Studies into Modernism at Lisbon´s Universidade Nova created this very useful website'); Obra Aberta is unnamed, and the 1997 CD-ROM stands without its publishers ('Edição original: Texto Editora e Casa Fernando Pessoa, 1997').",
   "THE VOICES NOT CARRIED. 'the \"Labirinto\" (which features audio readings and images)'. The technical sheet gives each of four names its own reader: 'Alberto Pimenta (Ricardo Reis) José Abreu (Alberto Caeiro) José Lopes (Álvaro de Campos) Teresa Faria (Fernando Pessoa)'. The composition gives the readings without the names they voice."],
  "An accurate composition of the edition's scope and sections that thins its division of names: the orthonym's poetry drops from the list, the pseudonyms and joint attributions are absent, and the editor is replaced by a partner named on a third-party card.",
  [C("Arquivo Pessoa: Obra Édita -", "Arquivo Pessoa", "Obra de Fernando Pessoa 1. Poemas de Alberto Caeiro 2. Poesia de Álvaro de Campos 3. Odes de Ricardo Reis 4. Poesia Ortónima de Fernando Pessoa 5. Livro do Desa..."),
   C("Arquivo Pessoa: Obra Édita -", "Info - Arquivo Pessoa", "O portal MultiPessoa dirige-se a todo o tipo de leitores, do leigo ao investigador, e tem por objectivos principais: Divulgar a obra de Fernando Pessoa, tornand..."),
   C("Art and Soul Group", "5 (+1) websites to read and admire the work of Fernando Pessoa - Art and Soul", "Between 1997 and 2008 the Institute of Studies into Modernism at Lisbon´s Universidade Nova created this very useful website, which incorporates the MultiPessoa...")],
  {"author": True, "inst": True, "id": False, "src": True}, "Leonor Areal and the Institute named, the editor Obra Aberta not; the edition's pages and one third-party page carded.")

write(parts)
