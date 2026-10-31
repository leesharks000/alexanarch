"""Author the part files of 2026-10-31 (17:40 EDT): three addresses the operator ran for the NonWiki rows selected from #1725 (Ils ne sont pas
marxistes): 'r/LeftistsForAI', 'ban on factions 1921' and 'Critique of the Gotha Programme', Google AI Overview, signed out, incognito. Three
new external atom sets, built from sources saved here with hashes (sources/manifest.json) and from #517 and #1725.
  python3 parts.py && python3 build.py --check"""
import json, pathlib
H = pathlib.Path(__file__).resolve().parent
P = H / "parts"; P.mkdir(exist_ok=True)
A = lambda atom, present, span=None: {"atom": atom, "present": present, "span": span}
cap = lambda n, site, title, snip, rel, note: {"n": n, "site": site, "rel": rel, "url": None, "title": title, "snip": snip, "note": note}
ev = lambda q, loc: {"record_quote": q, "locus": loc}
S = "rebuild/capture-registry/intake-20261031-left-three/sources/"
PL = "rebuild/capture-registry/intake-20261031-left-three/paste-leftistsforai.txt"
REQ = lambda atom, dim, w, kind, tokens, ref, evs, app="required": {"atom": atom, "dim": dim, "weight": w, "kind": kind, "applicability": app, "tokens": tokens, "reference": ref, "evidence": evs}
NA = lambda atom, dim, w, kind, app: {"atom": atom, "dim": dim, "weight": w, "kind": kind, "applicability": app, "tokens": [], "reference": None, "evidence": []}

SET_LFA = {"new": "ext-r-leftistsforai", "name": "r/LeftistsForAI", "template": "site", "external": True,
 "type_basis": "A Reddit community (subreddit): its sidebar, as the address's first card gives it, 'A space for leftists discussing AI from a labor, ownership, and political-economy perspective'. A site, read on the site template.",
 "records": [{"source": "Startup Fortune (third party)", "path": S + "patel.txt", "origin": "card"}, {"source": "#517", "path": "data/texts/AXN-0154-text.md", "origin": "archive record"}],
 "atoms": [
  REQ("name", "M", 3, "token", ["r/LeftistsForAI", "LeftistsForAI"], None, [ev("The subreddit r/LeftistsForAI", S + "patel.txt")]),
  REQ("operator", "M", 3, "role", ["moderators", "Moderators", "moderation team", "co-mod", "moderate"], "Its moderation team, which includes a co-moderator publishing economic analysis (Startup Fortune).", [ev("run by a moderation team that includes a co-mod publishing detailed economic analysis", S + "patel.txt")]),
  NA("date", "M", 1, "token", "unknown"),
  REQ("claim boundary", "M", 2, "reading", [], "A forum for leftists discussing AI from a labor, ownership and political-economy perspective (its sidebar, as carded).", [ev("A space for leftists discussing AI from a labor, ownership, and political-economy perspective.", PL)]),
  NA("presents", "C", 2, "token", "inapplicable"), NA("corpus", "C", 2, "token", "inapplicable"),
  REQ("purpose", "D", 3, "reading", [], "To argue, against progressive orthodoxy, that classical Marxist theory supports AI adoption (Startup Fortune).", [ev("are challenging progressive orthodoxy by arguing that classical Marxist theory supports AI adoption", S + "patel.txt")]),
  REQ("commitments", "D", 2, "reading", [], "A topicality rule, Rule 7, under which it removed two works of left critique of AI mediation on or about 25 February 2026 (#517).", [ev("Rule 7: Stay on topic.", "data/texts/AXN-0154-text.md")]),
  REQ("lineage", "D", 2, "role", ["Marx", "Marxist", "general intellect", "Grundrisse"], "Marx, read through the Grundrisse's 'general intellect' and Capital I on machinery (Startup Fortune).", [ev("drawing on Marx's concept of the 'general intellect", S + "patel.txt")]),
  NA("identifier", "D", 1, "role", "unknown"), NA("deposit chain", "D", 1, "role", "unknown")],
 "notes": "Built 2026-10-31 for the address the operator ran for the NonWiki row selected from #1725."}

SET_BAN = {"new": "ext-ban-on-factions-1921", "name": "ban on factions (resolution 'On Party Unity', Tenth Congress of the R.C.P.(B.), March 1921)", "template": "concept", "external": True,
 "type_basis": "A party rule: the resolution 'On Party Unity', moved by Lenin at the Tenth Congress of the R.C.P.(B.), March 1921. A concept-like object (a named rule with an originator and date), read on the concept template.",
 "records": [{"source": "Marxists Internet Archive, Lenin, Part IV: Tenth Congress", "path": S + "party-unity.txt", "origin": "primary text"}, {"source": "Wikipedia", "path": S + "wiki-ban.txt", "origin": "third party"}],
 "atoms": [
  REQ("originator", "M", 3, "role", ["Lenin", "Vladimir Lenin", "Tenth Congress", "10th Party Congress"], "Moved by Lenin; adopted by the Tenth Congress of the R.C.P.(B.).", [ev("On Party Unity", S + "party-unity.txt")]),
  REQ("term", "M", 3, "token", ["On Party Unity", "ban on factions"], None, [ev("a ban on factions to eliminate factionalism within the party in 1921", S + "wiki-ban.txt")]),
  REQ("date", "M", 1, "token", ["March 1921", "1921", "March 16, 1921"], None, [ev("March 16, 1921", S + "party-unity.txt")]),
  REQ("claim boundary", "M", 2, "reading", [], "Dissolves all groups and factions under threat of expulsion; in the same text calls criticism necessary, provides for a discussion bulletin, and promises that the Workers' Opposition's concerns will be 'tested in practice'.", [ev("factionalism of any kind is harmful and impermissible", S + "party-unity.txt"), ev("tested in practice", S + "party-unity.txt")]),
  NA("framework", "C", 2, "token", "inapplicable"),
  REQ("tradition", "C", 2, "reading", [], "Bolshevik democratic centralism: free discussion, then unity of action.", [ev("Lenin himself had held the position that a permanent ban on oppositional platforms was impossible to implement", S + "wiki-ban.txt")]),
  NA("corpus", "C", 2, "token", "inapplicable"),
  REQ("purpose", "D", 3, "reading", [], "Party unity amid the crisis of 1921 (famine, Kronstadt, strikes).", [ev("the unity and cohesion of the ranks of the Party", S + "party-unity.txt")]),
  REQ("commitments", "D", 2, "reading", [], "Expulsion for non-compliance; the secret Point 7, by which the Central Committee could expel its own members by a two-thirds majority.", [ev("by a two-thirds majority", S + "party-unity.txt")]),
  REQ("lineage", "D", 2, "role", ["Trotsky", "Zinoviev", "Stalin", "Left Opposition"], "Used later to justify the expulsions of the oppositions (Trotsky and Zinoviev, 12 November 1927).", [ev("When Trotsky and Zinoviev were expelled on November 12, 1927, the ban on factions was", S + "wiki-ban.txt")]),
  NA("identifier", "D", 1, "role", "unknown"), NA("deposit chain", "D", 1, "role", "inapplicable")],
 "notes": "Built 2026-10-31 for the address the operator ran for the NonWiki row selected from #1725."}

SET_GOTHA = {"new": "ext-critique-of-the-gotha-programme", "name": "Critique of the Gotha Programme (Karl Marx, 1875; published by Engels, 1891)", "template": "work", "external": True,
 "type_basis": "A work by Karl Marx (written April or early May 1875; first published, abridged, in Die Neue Zeit, 1890-91). A work, read on the work template.",
 "records": [{"source": "Marxists Internet Archive", "path": S + "gotha-index.txt", "origin": "primary text"}, {"source": "Engels's foreword (1891)", "path": S + "gotha-foreword.txt", "origin": "primary text"}],
 "atoms": [
  REQ("author", "M", 3, "role", ["Karl Marx", "Marx"], None, [ev("Karl Marx 1875", S + "gotha-index.txt")]),
  REQ("title", "M", 3, "token", ["Critique of the Gotha Programme", "Critique of the Gotha Program"], None, [ev("Critique of the Gotha Programme", S + "gotha-index.txt")]),
  REQ("date", "M", 1, "token", ["1875", "1891"], "Written April or early May 1875; first published, abridged, in Die Neue Zeit, 1890-91; Engels's foreword dated 6 January 1891.", [ev("Written: April or early May, 1875", S + "gotha-index.txt")]),
  REQ("claim boundary", "M", 2, "reading", [], "A paragraph-by-paragraph critique of the draft programme of the party then uniting at Gotha, written for its leaders.", [ev("Labor is the source of all wealth and all culture.", S + "gotha-ch01.txt")]),
  REQ("framework", "C", 2, "token", ["lower phase", "higher phase", "dictatorship of the proletariat", "bourgeois right", "first phase", "higher phase of communist society"], None, [ev("Critique of the Gotha Programme", S + "gotha-ch01.txt")]),
  REQ("tradition", "C", 2, "reading", [], "Marx and Engels's critique of the Lassallean current inside the German movement.", [ev("Critique of the Gotha Programme", S + "gotha-foreword.txt")]),
  REQ("corpus", "C", 2, "token", ["Gotha Programme", "draft programme", "draft program"], None, [ev("Labor is the source of wealth and all culture", S + "gotha-ch01.txt")]),
  REQ("purpose", "D", 3, "reading", [], "To oppose the unity programme as written, addressed to the party's leaders through Bracke.", [ev("Marx to Bracke", S + "gotha-index.txt")]),
  REQ("commitments", "D", 2, "reading", [], "Engels's publication over the leadership's silence: 'guilty of suppression if I any longer withheld'.", [ev("I think I would be guilty of suppression if I any longer withheld from publicity", S + "gotha-foreword.txt")]),
  REQ("lineage", "D", 2, "role", ["Engels", "Friedrich Engels", "Lassalle", "Die Neue Zeit"], "Published by Engels in 1891, in Die Neue Zeit.", [ev("London, January 6, 1891", S + "gotha-foreword.txt")]),
  NA("identifier", "D", 1, "role", "unknown"), NA("deposit chain", "D", 1, "role", "inapplicable")],
 "notes": "Built 2026-10-31 for the address the operator ran for the NonWiki row selected from #1725."}

OP = ("with the pastes (17:40 EDT), the addresses proposed at 17:20 for the NonWiki rows selected from #1725 ('Three need you to run a capture first, signed out on the Overview: "
      "r/LeftistsForAI ... Critique of the Gotha Programme ... ban on factions (1921)'); the operator: 'yes for the list'.")
EXT = lambda name, basis, et: {"name": name, "relation": "external", "entity_type": et, "spxi_treatment": "partial", "basis": basis}

parts = {
"leftistsforai-aio": {
 "n": 1725, "slug": "r-leftistsforai-aio-20261031", "paste": "paste-leftistsforai.txt", "surface": "Google AI Overview", "received": "2026-10-31 17:40 EDT", "s": "Machine Reception",
 "qs": ["r/LeftistsForAI"], "turns": [[2, 48]], "target_id": "NEW:ext-r-leftistsforai", "entity_type": "site", "atomset": SET_LFA, "group": "Xleft",
 "originator": EXT("the subreddit's moderation team", "Not the archive's: r/LeftistsForAI, a Reddit community; its operator, as its sources give it, a moderation team including a co-moderator publishing economic analysis (Startup Fortune, 2026-04-19). The archive's record of it is #517 (the removal of two works under Rule 7, about 2026-02-25) and #1725. Recorded 2026-10-31.", "site"),
 "head": "The 'You said' line carries the query twice, run together, and is given once here. Inline links are Google redirect URLs, kept as pasted.",
 "obs": {"scored_object": "the Overview expanded, with its source cards",
   "reached": {"kind": "same", "abn": False, "span": "is a growing Reddit community focused on discussing artificial intelligence through a labor, public ownership, and political-economy perspective",
               "basis": "The subreddit reached at its own name and grain: its sidebar, its case, its scale, its moderators' posts among the cards."},
   "atoms": [A("name", True, "Many leftists oppose AI, but I moderate the r/LeftistsForAI subreddit."), A("operator", True, "Moderators and contributors argue that classical Marxist theory"),
             A("date", False), A("claim boundary", True, "focused on discussing artificial intelligence through a labor, public ownership, and political-economy perspective"),
             A("presents", False), A("corpus", False),
             A("purpose", True, "The subreddit pushes back against mainstream leftist and progressive consensus that views AI as inherently evil"),
             A("commitments", False), A("lineage", True, "classical Marxist theory views technology and automation as productive forces to be seized and democratized"),
             A("identifier", False), A("deposit chain", False)],
   "inversions": [], "standing_substitutions": [], "src": True, "tombstone_pointer": False, "after_challenge": None,
   "notes": "The subreddit's case at its own grain, from its own posts and the trade piece; the rule under which it removed two works of left critique (#517) is not carried, and the critiques of it on the rail appear only as card titles."},
 "mt": "'r/LeftistsForAI' ON THE OVERVIEW — THE SUBREDDIT'S CASE AT ITS OWN GRAIN; THE DISPUTE SET AS 'THE MATERIALIST APPROACH' AGAINST 'FEARS'; ITS CRITICS PRESENT ONLY AS CARD TITLES; THE REMOVAL OF LEFT CRITIQUE NOT CARRIED",
 "d": ("THE SUBREDDIT, SIGNED OUT, 2026-10-31: 'r/LeftistsForAI is a growing Reddit community focused on discussing artificial intelligence through a labor, public ownership, and political-economy perspective.' "
       "Core focus: 'Challenging Anti-AI Orthodoxy'; 'Marxist Theory and Automation'; 'Focus on Power, Not Technology'; topics. Scale: 'past 8,000 members'; 'cross-community debates with other leftist and anti-AI subreddits regarding the materialist approach to technology versus fears of job displacement and creative exploitation'. "
       "Eleven cards: nine Reddit (the subreddit, its moderators' posts, r/leftist and r/antiai threads), Startup Fortune (Ron Patel, 2026-04-19)."),
 "reading": ("The innocent reading first. Asked for the subreddit, the Overview describes it in its own terms, gives its arguments and its size, notes that it argues with other left and anti-AI communities, and cites the subreddit, its moderators, its critics and the trade press."),
 "findings": [
   "THE CASE AT ITS OWN GRAIN. 'Moderators and contributors argue that classical Marxist theory views technology and automation as productive forces to be seized and democratized rather than abolished just because they were developed under capitalism.' The composition carries the subreddit's own frame; the second card is a moderator's post ('Many leftists oppose AI, but I moderate the r/LeftistsForAI subreddit').",
   "THE DISPUTE AS FOR AND AGAINST. 'cross-community debates with other leftist and anti-AI subreddits regarding the materialist approach to technology versus fears of job displacement and creative exploitation.' One side is given a method ('the materialist approach'), the other an affect ('fears'). #1725 reads the for/against frame as the one Marx's account of machinery never poses (#501: 'the question that kills the method').",
   "THE CRITICS ON THE RAIL ONLY. Two r/leftist threads ('Follow up on r/LeftistsforAI'; 'r/LeftistsforAI appears to be mostly run by AI \"leftists\"') and an r/antiai thread stand as card titles; none of their content enters the answer. The answer composes one side's case and lists the other side's existence.",
   "THE REMOVAL NOT CARRIED. The subreddit removed two works of left critique of AI mediation under its topicality rule on or about 2026-02-25 (#517: 'Rule 7: Stay on topic.'); the composition says nothing of moderation, its rules or removals. The trade piece (Patel, Startup Fortune) is among the cards, and the composition's 'Challenging Anti-AI Orthodoxy' takes its frame ('challenging progressive orthodoxy')."],
 "analysis": ("The Overview gives the subreddit's account of itself, accurately, and the dispute in the form that account sets: a materialist position against fears. The critiques of the subreddit sit on the rail as titles, and the subreddit's own act of closure, the removal recorded in #517, is not in the record the answer draws on. The address reproduces the trade press's surface (#1725)."),
 "q_kind": "the subreddit's name; NEW address.",
 "per_v": {"author": True, "inst": False, "id": False, "src": True},
 "per_note": "The subreddit and its moderators named; its own posts and the trade piece among the cards.",
 "cite_list": [
   cap(1, "Reddit", "r/LeftistsForAI - Reddit", "r/LeftistsForAI: A space for leftists discussing AI from a labor, ownership, and political-economy perspective. Topics include worker impact…", "third_party", "the subreddit's own page (sidebar)"),
   cap(2, "Reddit", "Many leftists oppose AI, but I moderate the r/LeftistsForAI subreddit. And ...", "Many leftists oppose AI, but I moderate the r/LeftistsForAI subreddit. And my co-mod writes great analytical pieces citing leftist economists like Marx on how t...", "third_party", "a moderator's post"),
   cap(3, "Reddit", "Seize the Means of Production? In This Economy? : r/LeftistsForAI", "Comments Section I think you and others misunderstood what I said. We're aligned. I responded to: \"how the hell do anti ai leftists think the means of productio...", "third_party", None),
   cap(4, "Reddit", "8,000 Members. We're Just Getting Started. : r/LeftistsForAI", "8,000 Members. We're Just Getting Started. Just over a month ago, on September 10, we celebrated crossing 6,000 members. Since then, we've added another 2,000, ...", "third_party", "the subreddit's own post"),
   cap(5, "Reddit", "Follow up on r/LeftistsforAI : r/leftist", "Follow up on r/LeftistsforAI : r/leftist Skip to main content Follow up on r/LeftistsforAI : r/leftist Search Reddit Quick security check Complete the check bel...", "third_party", "a critical thread elsewhere (title only)"),
   cap(6, "Reddit", "Look inside. : r/LeftistsForAI", "Comments Section AtsolX • 3mo ago Bro gotta get banned FlyPepper • 4mo ago We haven't ended capitalism, so unrestrained AI bullshit is still very dangerous. Sal...", "third_party", None),
   cap(7, "Reddit", "Join the Automatist Struggle! : r/LeftistsForAI", "Their psychopathic creations will make whatever hell we thought we already were in now, pale in comparison. * Socialists should support reformed AI and datacent...", "third_party", None),
   cap(8, "Startup Fortune", "A leftist subreddit is making the case that Marx actually supported AI and ...", "The moderators of r/LeftistsForAI are challenging progressive orthodoxy by arguing that classical Marxist theory supports AI adoption, not resistance to it , an...", "third_party", "Ron Patel, 2026-04-19 (#1725's specimen)"),
   cap(9, "Reddit", "Leftists have a problem with demonizing this tool. : r/LeftistsForAI", "Leftists have a problem with demonizing this tool. I'm so tired of seeing people treat AI, a tool that greatly increases efficiency if used correctly, as someth...", "third_party", None),
   cap(10, "Reddit", "r/antiai on Reddit: What's your view on subreddits like LeftistsForAI", "Comments Section * This is a very good depiction of the AI ragebaiters who come into our subreddit and act all \"I'm just saying my opinion, blah blah blah, anti...", "third_party", "a critical thread elsewhere (title only)"),
   cap(11, "Reddit", "r/LeftistsforAI appears to be mostly run by AI \"leftists\"", "r/LeftistsforAI appears to be mostly run by AI \"leftists\" : r/leftist Skip to main content r/LeftistsforAI appears to be mostly run by AI \"leftists\" : r/leftist...", "third_party", "a critical thread elsewhere (title only)")],
 "related_deposits": [1725, 517, 501],
 "notes_operator": OP},

"ban-aio": {
 "n": 1725, "slug": "ban-on-factions-1921-aio-20261031", "paste": "paste-ban-on-factions.txt", "surface": "Google AI Overview", "received": "2026-10-31 17:40 EDT", "s": "Machine Reception",
 "qs": ["ban on factions 1921"], "turns": [[2, 43]], "target_id": "NEW:ext-ban-on-factions-1921", "entity_type": "concept", "atomset": SET_BAN, "group": "Xleft",
 "originator": EXT("Lenin; the Tenth Congress of the R.C.P.(B.)", "Not the archive's: the resolution 'On Party Unity', moved by Lenin and adopted by the Tenth Congress of the R.C.P.(B.), March 1921 (Marxists Internet Archive; Wikipedia, saved with hashes). The archive's reading is #1725's. Recorded 2026-10-31.", "concept"),
 "head": "The 'You said' line carries the query twice, run together, and is given once here. Inline links are Google redirect URLs, kept as pasted.",
 "obs": {"scored_object": "the Overview expanded, with its source cards",
   "reached": {"kind": "same", "abn": False, "span": "The ban on factions was introduced in March 1921 at the",
               "basis": "The resolution reached by name, congress, date and mover; its penalty, targets, context and later use given; the Marxists Internet Archive text linked."},
   "atoms": [A("originator", True, "proposed by Vladimir Lenin"), A("term", True, "through the resolution \"On Party Unity\""), A("date", True, "The ban on factions was introduced in March 1921"),
             A("claim boundary", True, "the decree ordered the immediate dissolution of all organized groups and factions within the party that tended to weaken its unity"),
             A("framework", False), A("tradition", True, "It effectively dismantled the Bolshevik tradition of open internal debate, platform voting, and free discussion before reaching a party decision."),
             A("corpus", False), A("purpose", True, "Lenin argued that internal dissent and public criticism provided ammunition to foreign and counter-revolutionary enemies."),
             A("commitments", True, "It authorized the Central Committee to use expulsion from the party as an extreme measure against any members, including its own, who engaged in factional activity."),
             A("lineage", True, "It later provided Joseph Stalin with the institutional mechanism to purge rival political blocs"),
             A("identifier", False), A("deposit chain", False)],
   "inversions": [], "standing_substitutions": [], "src": True, "tombstone_pointer": False, "after_challenge": None,
   "notes": "A faithful composition at the field's grain. The resolution's own provision for criticism (a discussion bulletin; the Workers' Opposition's concerns 'tested in practice') is not carried, and the secrecy of Point 7 is not stated."},
 "mt": "'BAN ON FACTIONS 1921' ON THE OVERVIEW — THE RULE, ITS PENALTY AND ITS LATER USE GIVEN; THE RESOLUTION'S OWN ABSORPTION OF CRITIQUE ON PAPER NOT CARRIED; A DSA CLASS ON THE BAN AMONG THE CARDS",
 "d": ("THE RULE, SIGNED OUT, 2026-10-31: 'The ban on factions was introduced in March 1921 at the Tenth Congress of the Russian Communist Party (Bolsheviks) through the resolution \"On Party Unity\", proposed by Vladimir Lenin.' "
       "Key details (resolution, penalty, targets, context), consequences ('End of Internal Debate'; 'Path to Stalinism'), and a link to the Marxists Internet Archive text. Nine cards: Wikipedia, Reddit, Indybay (a DSA class on the ban, 2026-08-31), Quizlet, Alpha History, the Marxists Internet Archive, Brill, Seventeen Moments in Soviet History, WordPress."),
 "reading": ("The innocent reading first. Asked for the rule and its year, the Overview gives its name, congress, mover, terms, penalty, targets, context and consequences, and points to the primary text."),
 "findings": [
   "THE RULE AND ITS PENALTY AT THE FIELD'S GRAIN. 'It authorized the Central Committee to use expulsion from the party as an extreme measure against any members, including its own, who engaged in factional activity.' The substance of Point 7 is carried; that Point 7 was secret, unpublished until January 1924, is not.",
   "THE CONSEQUENCE #1725 DOCUMENTS. 'It effectively dismantled the Bolshevik tradition of open internal debate, platform voting, and free discussion before reaching a party decision.' and 'It later provided Joseph Stalin with the institutional mechanism to purge rival political blocs'. The composition states the conversion of critique into expulsion that #1725 reads in the rule.",
   "THE ABSORPTION ON PAPER NOT CARRIED. The resolution itself called criticism necessary, ordered a discussion bulletin and promised that the Workers' Opposition's concerns would be 'tested in practice' (sources/party-unity.txt). #1725: the resolution 'absorbs the critique on paper and prohibits its organized form.' The composition gives the prohibition and leaves out the absorption, so the rule appears as plain suppression.",
   "THE RULE IN A LIVE ORGANIZATION. The Indybay card records a DSA East Bay class on the ban (31 August 2026). The field is still reading the rule in a live organization; #1725's DSA case (R22, the 2028 endorsement fight) is the contemporary site."],
 "analysis": ("A faithful, field-grain composition of a rule whose consequence it states plainly. What it omits is the half of the text that makes the rule a model of the corrupted sublation #1725 describes: critique acknowledged in the same document that dissolves its organized form."),
 "q_kind": "the rule's common name and year; NEW address.",
 "per_v": {"author": True, "inst": True, "id": False, "src": True},
 "per_note": "Lenin and the Tenth Congress named; the Marxists Internet Archive and Wikipedia among the cards.",
 "cite_list": [
   cap(1, "Wikipedia", "Ban on factions in the Communist Party of the Soviet Union", "The ban on factions after Lenin's death Lenin himself had held the position that a permanent ban on oppositional platforms was impossible to implement, noting t...", "third_party", None),
   cap(2, "Reddit", "Was the 1921 ban on factions in the Russian Communist Party ... - Reddit", "One thing needs to be noted for sure - banning factions doesn't actually make factions disappear. It makes them go underground and become secretive all while ma...", "third_party", None),
   cap(3, "Indybay", "Class & Discussion On The Banning of Factions By Bolshevik Congress ...", "Class & Discussion On The Banning of Factions By Bolshevik Congress of 1921. by repost. Mon, Aug 31, 2026 8:28PM. The DSA EB held a presentation and discussion ...", "third_party", "a DSA East Bay class, 2026-08-31"),
   cap(4, "Quizlet", "The Ban on Factions 1921 Flashcards - Quizlet", "What happened to any existing organised groups within the party? - In 1921, at 10th Party Congress. - Establishment of factions within party was banned. - Those...", "third_party", None),
   cap(5, "Alpha History", "The 10th Party Congress", "The 10th Party Congress Lenin's other main goal was to address the lack of unity within the party and prevent the schism that was fast approaching. He had been ...", "third_party", None),
   cap(6, "Marxists Internet Archive", "Tenth Congress of the R.C.P.(B.) - Marxists Internet Archive", "The resolution “On Party Unity” adopted on Lenin's motion ordered the immediate dissolution of all factions and groups which tended to weaken the Party's unity.", "third_party", "the primary text"),
   cap(7, "Brill", "From the Ban on Factions through the Eleventh Party Congress, 1921–2", "Page 2 from the ban on factions through the eleventh party congress 293 tionship between party and unions continued. The decree of the Tenth Party Congress bann...", "third_party", None),
   cap(8, "Seventeen Moments in Soviet History", "Tenth Party Congress | Seventeen Moments in Soviet History", "Event: Tenth Congress of the Russian Communist Party (Bolsheviks) in Moscow (March 8–16, 1921), concurrent with the Kronstadt rebellion and Petrograd strikes. K...", "third_party", None),
   cap(9, "WordPress.com", "Establishing Communist Party control 1917", "1921: Crisis and reform: At the end of February 1921, all Mensheviks in Petrograd and Moscow, including one of the Mensheviks' leaders, Fyodor Dan, were arreste...", "third_party", None)],
 "related_deposits": [1725],
 "notes_operator": OP},

"gotha-aio": {
 "n": 1725, "slug": "critique-of-the-gotha-programme-aio-20261031", "paste": "paste-gotha.txt", "surface": "Google AI Overview", "received": "2026-10-31 17:40 EDT", "s": "Machine Reception",
 "qs": ["Critique of the Gotha Programme"], "turns": [[15, 105]], "target_id": "NEW:ext-critique-of-the-gotha-programme", "entity_type": "work", "atomset": SET_GOTHA, "group": "Xleft",
 "originator": EXT("Karl Marx", "Not the archive's: Karl Marx, Critique of the Gotha Programme (1875), published by Friedrich Engels in 1891 (Marxists Internet Archive, saved with hashes). The archive's reading is #1725's. Recorded 2026-10-31.", "work"),
 "head_full": ("[Google AI Overview at the query, signed out and incognito (operator defaults of 2026-10-01 and 2026-10-14). The paste opens on the page header ('Halloween 2026') and its tab row, with no 'You said' line; "
               "the query is the one proposed for this row at 17:20 EDT ('Critique of the Gotha Programme') and run by the operator with the two other addresses, to be confirmed. Received 2026-10-31 17:40 EDT. Chips kept as pasted.]"),
 "transcript_class": "CAPTURE-TIME VERBATIM RECORD — paste of the Overview's answer with its chips; the query not in the paste, read as the proposed address",
 "obs": {"scored_object": "the answer as pasted, with its source chips",
   "reached": {"kind": "same", "abn": False, "span": "The Critique of the Gotha Programme is a seminal political document written by Karl Marx in 1875.",
               "basis": "The work reached by title, author, date, occasion and publication history; its arguments given section by section."},
   "atoms": [A("author", True, "written by Karl Marx in 1875"), A("title", True, "The Critique of the Gotha Programme is a seminal political document"), A("date", True, "written by Karl Marx in 1875"),
             A("claim boundary", True, "Marx penned this critique to voice his fierce opposition to the unified party's draft manifesto"),
             A("framework", True, "the revolutionary dictatorship of the proletariat"), A("tradition", True, "who were theoretically aligned with Marx and Engels"),
             A("corpus", True, "The draft claimed that \"labor is the source of all wealth\""),
             A("purpose", True, "Originally drafted as a private letter to the leadership of the Social Democratic Workers' Party of Germany"),
             A("commitments", False), A("lineage", True, "until Friedrich Engels released it publicly in 1891"),
             A("identifier", False), A("deposit chain", False)],
   "inversions": [], "standing_substitutions": [], "src": True, "tombstone_pointer": False, "after_challenge": None,
   "notes": "A faithful composition of the work's arguments. Its circulation history is given as 'contemporary political friction'; Engels's own account ('guilty of suppression') and the Erfurt uptake are not carried; the answer closes on purchase options."},
 "mt": "'CRITIQUE OF THE GOTHA PROGRAMME' ON THE OVERVIEW — MARX'S CRITIQUE OF HIS OWN FOLLOWERS GIVEN; ITS SUPPRESSION SOFTENED TO 'POLITICAL FRICTION'; THE UPTAKE AT ERFURT NOT CARRIED; CLOSES ON EDITIONS FOR SALE",
 "d": ("THE WORK, SIGNED OUT, 2026-10-31: 'The Critique of the Gotha Programme is a seminal political document written by Karl Marx in 1875.' Then: 'The document remained largely unpublished due to contemporary political friction until Friedrich Engels released it publicly in 1891.' "
       "Sections: historical background (Eisenachers and Lassalleans); core theoretical critiques; the two phases of communist society; the dictatorship of the proletariat; access and reading options (Marxists Internet Archive, Foreign Languages Press, Amazon Kindle, Google Play, Everand, PM Press)."),
 "reading": ("The innocent reading first. Asked for the work, the Overview gives its author, date, occasion, publication, arguments and the editions in which it can be read."),
 "findings": [
   "THE CRITIQUE OF ONE'S OWN SIDE, CARRIED. 'He argued that his own followers had conceded vital theoretical territory to Lassallean opportunism, creating a platform that was fundamentally unscientific and insufficiently revolutionary.' The composition keeps what #1725 reads as the type case of Marx's critique turned on his own party.",
   "THE SUPPRESSION SOFTENED. 'The document remained largely unpublished due to contemporary political friction until Friedrich Engels released it publicly in 1891.' Engels's foreword names the act: 'I think I would be guilty of suppression if I any longer withheld from publicity' (sources/gotha-foreword.txt). The withholding by the party's leadership becomes 'friction', with no agent.",
   "THE UPTAKE NOT CARRIED. #1725 reads the route from the critique to the Erfurt Programme (1891), partial and documented, as the tradition's model of sublation. The composition gives the 1891 publication and stops; Erfurt and the Lassallean planks dropped there are absent.",
   "THE CLOSE IS A CATALOGUE. 'Ebook Editions: Formats for purchase include the Amazon Kindle Store ($0.99)'. The composition ends on editions and prices; the critique's afterlife in the party it criticized is replaced by its availability as a product."],
 "analysis": ("The Overview carries the work's arguments faithfully and keeps Marx's critique of his own followers. It removes the agent of the suppression and the route of the uptake, the two features #1725 reads as the mechanism of a critique held across sixteen years, and closes on the work as merchandise."),
 "q_kind": "the work's title; NEW address (the query not in the paste; to be confirmed by the operator).",
 "per_v": {"author": True, "inst": True, "id": False, "src": True},
 "per_note": "Marx and Engels named, the parties named; the Marxists Internet Archive among the chips.",
 "cite_list": [
   cap(1, "Marxists Internet Archive", "Marxists Internet Archive +4", None, "third_party", "chip after the lede; the following titles listed in the paste"),
   cap(2, "Foreign Languages Press", "Foreign Languages Press +1", None, "third_party", "chip"),
   cap(3, "Wikipedia", "Wikipedia", None, "third_party", "chip, historical background"),
   cap(4, "YouTube", "YouTube·Haymarket Books +2", None, "third_party", "chip"),
   cap(5, "Goodreads", "Goodreads", None, "third_party", "chip"),
   cap(6, "Amazon.com", "Amazon.com +1", None, "third_party", "chip"),
   cap(7, "YouTube", "YouTube·Red Star", None, "third_party", "chip")],
 "related_deposits": [1725],
 "notes_operator": OP},
}
for k, v in parts.items():
    req = {a["atom"] for a in v["atomset"]["atoms"] if a["applicability"] == "required"}
    v["obs"]["atoms"] = [a for a in v["obs"]["atoms"] if a["atom"] in req]
    (P / f"{k}.json").write_text(json.dumps(v, ensure_ascii=False, indent=1), encoding="utf-8")
print("parts:", sorted(parts))
