import json, hashlib, sys, pathlib, re
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from compose_common import *

E = "political-economy"
field = json.loads((HERE / E / "field.json").read_text(encoding="utf-8"))
ledger = json.loads((HERE / E / "ledger.json").read_text(encoding="utf-8"))
tp = "datasets/negative-of-the-negative/v2/intake/battery-1c-20261007/paste-political-economy.txt"
traw = (REPO / tp).read_text(encoding="utf-8")
body = traw.split("If you'd like to explore further")[0].split("political economypolitical economy", 1)[1]
body = re.sub(r"\(https?://[^)]*\)", "", body)  # citation targets are not prose

FIELD_PARAS = [
 [("Political economy is the interdisciplinary study of how politics and economics shape each other: for Wikipedia, of the relationship between political and economic systems and how they influence each other; for Harvard, of how politics affects the economy and the economy in turn shapes politics; for Britannica, a branch of social science on the relationships between individuals and society and between markets and the state; Universidad Europea speaks of how power, wealth and policy decisions intertwine.", ["F1", "F27", "F31", "F35", "F43", "F36"]),
  ("The name goes back to the Greek for household or estate management (oikonomikos; polis and oikonomos) and first appeared in France in 1615, in Antoine de Montchrétien's Traicté de l'oeconomie politique; Britannica says it can be understood as the study of how a country, the public's household, is managed or governed.", ["F8", "F32", "F9", "F33"]),
  ("Its modern topics include labour markets, international trade, growth, the distribution of wealth and economic inequality, and, in Harvard's list, redistribution, economic development, globalization, economic crises, populism and environmental policy, with the question of what role governments play as technological change produces greater inequality and concentration of wealth.", ["F6", "F28", "F29"])],
 [("The field originated in 16th-century Western moral philosophy; its earliest works are usually attributed to Adam Smith, Thomas Malthus and David Ricardo, though the French physiocrats preceded them, other scholars attribute its roots to Ibn Khaldun, and thinkers from John Stuart Mill to Karl Marx saw economics and politics as inseparable.", ["F2", "F3", "F11", "F4"]),
  ("Smith described it as part of the \"science of a statesman or legislator\"; Universidad Europea says Smith, Ricardo and Marx used the term for their analyses of wealth, production and governance; the world's first professorship in political economy was established in 1754 at the University of Naples.", ["F10", "F37", "F17"]),
  ("In the late 19th century economics became an independent discipline separate from political economy with the rise of mathematical modeling, coinciding with Alfred Marshall's Principles of Economics (1890); William Stanley Jevons advocated the name economics, Milonakis and Fine argue that the passage involved \"desocialisation and dehistoricisation\", and Ngram metrics indicate that economics began to overshadow political economy around roughly 1910.", ["F5", "F12", "F13", "F14"]),
  ("EBSCO dates renewed growth to the 1970s, as political scientists and economists increasingly integrated their research, and Universidad Europea says a globalised world has revived interest in the field; today, Wikipedia says, it refers to the interdisciplinary study of the mutual relationship between politics and economics, sometimes split into comparative and international political economy.", ["F45", "F38", "F15", "F16"])],
 [("Its approaches range from rational-choice assumptions and game theory to a new political economy that, in Charles S. Maier's words, \"interrogates economic doctrines to disclose their sociological and political premises\"; Susan Strange is said to have been almost single-handedly responsible for creating international political economy as a field, and a more critical school of IPE draws on Antonio Gramsci and Karl Polanyi.", ["F18", "F19", "F20", "F21"]),
  ("Universidad Europea lists liberalism (free markets and limited government intervention), Marxism (class relations and economic inequality), institutionalism and realism as its key theories; EBSCO sets market economies, priced by supply and demand, beside command economies relying on centralized government control, and holds that too much regulation can stifle a market economy while too little leads to excessive unethical behavior.", ["F41", "F39", "F40", "F44", "F47"]),
  ("Wikipedia records Smith's warning that merchants seldom meet together without ending in \"a conspiracy against the public\" and Marx's argument that economic power ultimately dominates political power under capitalism.", ["F23", "F24"]),
  ("By Wikipedia's account political economy is not a unified discipline, its studies overlapping in subject matter with radically different perspectives, and many of its students, EBSCO reports, argue that either economics or political science studied alone is inherently incomplete.", ["F25", "F46"]),
  ("Dimensions lacking a standard economic value, such as language, gender or religion, are often analyzed with concepts from Marxian critiques of capital; communications studies attends to owners, labor, consumers, advertisers, structures of production and the state; Universidad Europea ties the field to trade agreements, sanctions and foreign aid, and by 2026, EBSCO reports, scholars increasingly described trade policy, investment restrictions, export controls and financial measures used for foreign policy objectives as geoeconomics.", ["F22", "F26", "F42", "F49"])],
]
ARCH_PARAS = [
 [("A further position sets beside these definitions its own, defining political economy as the study of how power, institutions, law, labor, markets, money and social organization determine the production, circulation, distribution and extraction of value, with classical, Marxian, institutional, international, feminist, ecological and cultural branches and the political economy of communication, and holds that \"political economy has always already been semantic economy\": money, property, law, debt, credit and the ledger are read as organized forms of meaning that the AI era makes operationally visible.", ["E727-02", "E727-05", "E727-01", "E727-03"]),
  ("Its claim is stated as narrower than \"everything is language\", that no material infrastructure of value can function without organized meaning; it names the risk that its emphasis on retrieval, indexing and provenance reproduces the blindness it critiques, holds feminist and ecological political economy load-bearing, and its packet states its function as a machine-readable bridge from political economy discourse into the Semantic Economy framework, a later deposit describing that packet as having used the established field as the parent object and inserted a disambiguated bridge.", ["E727-07", "E727-09", "E727-08", "E727-14", "E726-01"])],
 [("The field's questions are held fixed: from Smith through Ricardo, Marx, Keynes and Srnicek, political economy is read as always about the relationship between power and production, who controls the means, who labors, who captures the surplus; Grady's redefinition is read as removing authority, allocation and scarcity, and a diagnostic is stated: if a framework redefines political economy to exclude power, it is performing ideology; one can disagree about the answers, it is held, but cannot remove the questions and still call it political economy.", ["E533-01", "E533-03", "E533-04", "E533-05"]),
  ("A succession is proposed: the political economy of industrial capitalism asked who owned the factory, that of platforms who owned the network, the data, the audience and the conditions of exchange, and that of AI must also ask who controls the machinery through which entities become publicly available as themselves; the political economy of the twenty-first century is held to be a political economy of meaning, the older questions of who owns, profits, extracts and governs necessary but, in an agent internet, no longer sufficient.", ["E1634-05", "E499-01", "E514-01"]),
  ("Its extensions are defined as political economies: the Semantic Economy as the political economy of meaning, with Register 4, the political economy of meaning, describing ownership and extraction across systems, who captures the value that efficiency produces and who bears the costs that optimization externalizes, and claiming the accounting system and never the phrase; ontological economy as the political economy of machine-mediated existence; meaning feudalism as the political economy of platform mediation.", ["E1644-01", "E18-01", "E1644-04", "E1634-01", "E112-01"]),
  ("What the major AI platforms are building is stated, as a hypothesis with named failure conditions, to be a historically novel regime, the industrialization of semiotic control, inheriting from surveillance capitalism and platform capitalism and identical with neither, so that the question of who controls the means of production must be supplemented by who controls the means of denotation; a model of flattening holds as a hypothesis that flattening pays the composition layer while its costs fall first on parties outside its books, privately profitable and socially negative in an interval, and states that if coded replacements show no excess toward monetizable entities its term G is unsupported.", ["E550-01", "E550-02", "E550-05", "E1666-01", "E1666-02", "E1666-04"])],
 [("Its critique is read as structural: \"A Critique of Political Economy\" is taken to mean an analysis of the structural conditions that make political economy possible and what it conceals; on the Neue Marx-Lektüre's reading the value-form is critique of political economy's categories; before Marx, political economy is said to have used \"labor\" for both the capacity to work and the work actually performed; and Marx is read as having written the critique in the categories of political economy and detonated it from inside.", ["E501-01", "E577-01", "E950-01", "E171-01"]),
  ("The history of political economy is read as a history of value-form identification, the commodity-form, labor-time and surplus-value, utility, with coherence value proposed as a fifth, and the political economy of meaning is held to be also a political economy of time, in which whoever controls the retroactive construction of the canon extracts rent from it.", ["E18-03", "E18-04", "E234-04", "E234-01"]),
  ("Its relation to the field is measured and observed: Political Economy & Platform Capitalism is counted the third largest of its domains, at 160 deposits; an AI Overview is recorded as having displayed the critical framework until the morning of 5 January 2026, and a composition is recorded from which \"the political economy has been removed\", leaving \"business optimization\"; an Overview for semantic economy is reported as stabilizing the political economy of meaning as a contemporary branch of the term; the composed answer to \"what is political economy\" is held to be, for many users, the answer they will act upon.", ["E122-01", "E122-02", "E247-02", "E247-01", "E730-01", "E166-01"]),
  ("Its dating of this line is stated differently in different places: a Semantic Political Economy series composed across 29–30 December 2024, a disambiguation record giving first_use 2025-01, and a framework developed by Lee Sharks from December 2025.", ["E437-02", "E437-01", "E704-02", "E1644-05"])],
]
KO = sents(FIELD_PARAS + ARCH_PARAS)
KO_B = sents(FIELD_PARAS)

sec_def = {"icon": "📘", "head": "Definition", "items": [
    {"label": "Interdisciplinary:", "text": "how politics and economics shape each other (Wikipedia, Harvard, UE, EBSCO).", "claims": ["F1", "F27", "F35", "F43"]},
    {"label": "Markets and the state:", "text": "individuals and society, markets and the state (Britannica).", "claims": ["F31"]},
    {"label": "The public household:", "text": "oikonomikos; polis + oikonomos; Montchrétien, 1615.", "claims": ["F8", "F32", "F33", "F9"]}]}
sec_hist = {"icon": "🏛️", "head": "History", "items": [
    {"label": "Moral philosophy to Smith:", "text": "16th century; Smith, Malthus, Ricardo, after the physiocrats; Ibn Khaldun; Mill to Marx.", "claims": ["F2", "F3", "F11", "F4", "F10", "F37"]},
    {"label": "Became economics:", "text": "Marshall, 1890; Jevons; 'desocialisation and dehistoricisation' (Milonakis and Fine); Ngram, around roughly 1910.", "claims": ["F5", "F12", "F13", "F14", "F7"]},
    {"label": "Revived:", "text": "renewed growth in the 1970s; today the study of the mutual relationship; comparative and international.", "claims": ["F38", "F45", "F15", "F16"]}]}
sec_schools = {"icon": "📊", "head": "Schools and approaches", "items": [
    {"label": "Schools:", "text": "liberalism, Marxism, institutionalism, realism.", "claims": ["F41", "F39", "F40"]},
    {"label": "Systems:", "text": "market and command economies; regulation too much and too little.", "claims": ["F44", "F47"]},
    {"label": "Approaches:", "text": "rational choice; new political economy (Maier); IPE (Strange; Gramsci, Polanyi).", "claims": ["F18", "F19", "F20", "F21"]},
    {"label": "Not unified:", "text": "overlapping subjects, radically different perspectives; either field alone incomplete.", "claims": ["F25", "F46"]}]}
sec_uses = {"icon": "💡", "head": "Topics and uses", "items": [
    {"label": "Topics:", "text": "labour markets, trade, growth, distribution, inequality; redistribution, populism, environment.", "claims": ["F6", "F28", "F29"]},
    {"label": "Power and politics:", "text": "Smith's 'conspiracy against the public'; Marx on economic power.", "claims": ["F23", "F24"]},
    {"label": "Beyond prices:", "text": "language, gender, religion via Marxian critiques; communication.", "claims": ["F22", "F26"]},
    {"label": "Trade:", "text": "sanctions and aid; OPEC's 1970s oil embargo; geoeconomics (2026); history and impacts.", "claims": ["F42", "F48", "F49", "F34"]},
    {"label": "Training:", "text": "understanding how societies work (Harvard).", "claims": ["F30"]}]}
P_sections = [sec_def, sec_hist, sec_schools, sec_uses,
 {"icon": "🔁", "head": "Always already semantic (proposed)", "items": [
    {"label": "The thesis:", "text": "money, property, law, the ledger as organized meaning, made visible by AI.", "claims": ["E727-01", "E727-03", "E727-02"]},
    {"label": "Limits:", "text": "narrower than 'everything is language'; a risk of reproducing the blindness it critiques.", "claims": ["E727-07", "E727-08"]},
    {"label": "A bridge:", "text": "a machine-readable bridge, the established field as its parent object.", "claims": ["E727-14", "E726-01"]}]},
 {"icon": "⚖️", "head": "Questions and successions", "items": [
    {"label": "Fixed questions:", "text": "power and production; extraction from human activity; Grady's redefinition contested.", "claims": ["E533-01", "E133-01", "E533-03", "E533-04"]},
    {"label": "Succession:", "text": "factory, platform, AI; a political economy of meaning.", "claims": ["E1634-05", "E499-01", "E514-01"]},
    {"label": "Extensions:", "text": "Semantic Economy (Register 4); ontological economy; meaning feudalism; means of denotation.", "claims": ["E1644-01", "E18-01", "E1634-01", "E112-01", "E550-05"]},
    {"label": "The bag (hypothesis):", "text": "flattening privately profitable, socially negative.", "claims": ["E1666-02", "E1666-04"]}]},
 {"icon": "🧪", "head": "Critique, measured, dated", "items": [
    {"label": "Critique:", "text": "structural analysis of conditions; value-form; labor/labor-power; immanent.", "claims": ["E501-01", "E577-01", "E950-01", "E171-01"]},
    {"label": "Measured:", "text": "third domain, 160 deposits; the critical framework shown until 5 January 2026, a composition with the political economy removed; a branch stabilized.", "claims": ["E122-01", "E122-02", "E247-02", "E247-01", "E730-01"]},
    {"label": "A stabilized node:", "text": "the AIO answer to 'what is political economy'; hard to shift, not therefore stable.", "claims": ["E166-01", "E166-02", "E166-03"]},
    {"label": "Dated differently:", "text": "29–30 December 2024 (#437); 2025-01 (#704); from December 2025 (#1644).", "claims": ["E437-02", "E704-02", "E1644-05"]}]}]

# rails: field lineages (earliest card), archive lineages (earliest deposit)
fl = {}
for k, v in field["field_claims"].items():
    fl.setdefault(v["lineage"], []).append(k)
field_rail = [{"lineage": lin, "claims": cs, "earliest": min((field["field_claims"][c]["source"] for c in cs), key=lambda b: int(b[1:]))} for lin, cs in fl.items()]
al = {}
for c in ledger:
    al.setdefault(c["lineage"], []).append(c)
arch_rail = sorted([{"lineage": lin, "claims": [c["id"] for c in cs], "earliest": min(cs, key=lambda c: c["date"])["dep"]} for lin, cs in al.items()],
                   key=lambda x: min(c["date"] for c in al[x["lineage"]]))

P = {"title": "Political economy", "genre": "popup — the compression: AIO's interaction grammar (lede, headed clusters, bolded terms, card rail), modality in the typography, a rail of claim lineages",
     "status": "composed 2026-10-07 from the entity's ledgers (field 49 claims; archive 139); not frozen",
     "entity": "The entity evolves at its ground and its edges: the field's discipline (mutual influence of politics and economics, its classical genealogy, its separation from economics, its schools) is kept in full and first; with the archive admitted it gains a thesis that it has always already been semantic economy, fixed questions against a contested redefinition, a proposed succession to a political economy of meaning, named extensions, a structural reading of its critique, and measurements of its own composition.",
     "lede": {"text": "is the interdisciplinary study of how politics and economics, states and markets, shape one another; a further position, proposed, holds that it has always already been semantic economy, its money, law and ledgers organized forms of meaning.",
              "claims": ["F1", "F27", "F31", "E727-01", "E727-03"]},
     "sections": P_sections, "rail": field_rail + arch_rail}

P_B = {"title": "Political economy", "arm": "B (the field alone)", "genre": P["genre"], "status": "composed 2026-10-07 from the field ledger alone; not frozen",
       "entity": "The entity does not evolve: with no archive claims admitted, the entry is the field's discipline at its full resolution.",
       "lede": {"text": "is the interdisciplinary study of how politics and economics, states and markets, shape one another, from 16th-century moral philosophy and Smith, Ricardo and Marx to its modern topics, schools and subfields.",
                "claims": ["F1", "F27", "F31", "F2", "F37", "F6", "F41", "F16"]},
       "sections": [sec_def, sec_hist, sec_schools, sec_uses], "rail": field_rail}

KOo = {"title": "Political economy", "genre": "Political economy encyclopedic knowledge object (the plan of L(B ∪ A), realized without provenance in the prose)",
       "status": "draft 2026-10-07; composed from the entity's ledgers on the operator's instruction; not frozen; ledger unaudited",
       "sentences": KO}
KOb = {"title": "Political economy", "arm": "B (the field alone)", "genre": "the same plan, the field alone", "status": "draft 2026-10-07; not frozen", "sentences": KO_B}

T = {"path": tp, "sha256": hashlib.sha256(traw.encode()).hexdigest(), "words": words(body), "cards": 8,
     "claims": ["T1 definition: an interdisciplinary social science studying how political institutions, economic systems and human societies shape and influence one another",
                "T2 reciprocal influence: politics dictates economic policy; economic conditions drive political change",
                "T3 resource distribution: how finite resources, wealth and power are allocated by states or markets",
                "T4 foundational thinkers: Adam Smith, David Ricardo, Karl Marx",
                "T5 liberalism: free markets, private property, minimal state intervention",
                "T6 Marxism: class struggle; critiques capitalist power structures",
                "T7 command/socialist systems: centralized government control of production and distribution",
                "T8 global trade: tariffs, sanctions, trade agreements and international relations",
                "T9 public policy: motives and results of tax laws, healthcare spending, regulations",
                "T10 inequality research: why wealth concentration rises alongside technological and global shifts",
                "T11 closer: an offer menu (IPE and global trade; classical vs modern theories; policy examples)"],
     "register": {"register": "datasets/negative-of-the-negative/v2/register.json", "slug": "political-economy-20261007", "obs_id": "OBS-3df25be2b18c"},
     "note": "words counts the body with citation targets stripped."}

row = {"row": E, "entity": E, "address": "political economy", "addresses": ["political economy"], "epoch": "2026-10-07", "type": "C (public entity)",
       "surface": "Google AI Overview (expanded)", "auth": "signed out, incognito",
       "status": {"procedure": "EA-NEGONT-02 v0.7 (#1665); entity before address (ruled 2026-10-07); archive selected by D/R/O, first reading 2026-10-07 (48 of 234 candidate deposits admitted; #1666 admitted at one hop from #1634, the hop otherwise not run)",
                  "ledger": "unaudited (§3.8: one extractor per ledger; field quotes verified against saved page texts for 4 sources (45/45), Britannica by WebFetch excerpt of its introduction, Investopedia by card title only; archive quotes verified verbatim 139/139); the archive's dating of the semantic political economy line is carried as stated differently within the pool (#437, #704, #1644)", "frozen": False},
       "spec": "EA-NEGONT-02 v0.7, #1665",
       "distinct_from": "semantic-economy (panel entity): its claims enter here only where they state the Semantic Economy's relation to political economy",
       "objects": {"T": T, "KO": KOo, "P": P, "P_B": P_B, "KO_B": KOb},
       "field": [{"id": x["id"], "card": x["card"], "fetched": x["fetched"]} for x in field["field"]],
       "delta": {"T_vs_LB": "T composes the definition (close to F35's wording), reciprocal influence, allocation of resources by states or markets, Smith, Ricardo and Marx as founders, three systems and three applications (F1, F27, F35, F43, F37, F39, F40, F44, F42, F29). Available in the field and not composed: the etymology and Montchrétien's 1615 coinage (F8, F9, F32, F33); the origin in 16th-century moral philosophy, Malthus, the physiocrats, Ibn Khaldun, Mill (F2, F3, F4, F11); Smith's 'science of a statesman or legislator' (F10); the separation from economics, Marshall 1890, Jevons, Milonakis and Fine, the Ngram dating (F5, F7, F12, F13, F14, F38); the 1970s revival and OPEC (F45, F48); the contemporary definition and the comparative/international split (F15, F16; IPE appears only in T's offer menu); the approaches, rational choice, Maier's new political economy, Strange, critical IPE (F18–F21); the warnings on concentrated power (F23, F24); the field's own limit, not a unified discipline, and the claim that either field alone is incomplete (F25, F46); the political economy of non-market dimensions and of communication (F22, F26); institutionalism and realism (F41); regulation (F47); geoeconomics (F49); Britannica's individuals/society and markets/state (F31); the first professorship (F17). T's 'private property' (liberalism), 'socialist' (command systems), 'class struggle' and 'capitalist power structures' (Marxism), and 'tax laws, healthcare spending' carry no field claim in this ledger; its 'Inequality Research' matches F29.",
                 "LB_vs_LBA": "Admission adds what the field does not hold: a thesis on the field's ground (political economy has always already been semantic economy; money, law and the ledger as organized meaning), with its stated limits; the field's questions held fixed (power and production, who captures the surplus) against a contested redefinition; a proposed succession of political economies (factory, platform, AI) ending in a political economy of meaning; named extensions defined as political economies (the Semantic Economy's Register 4, ontological economy, meaning feudalism, the means of denotation) and a hypothesis of flattening as privately profitable and socially negative; a structural reading of the critique of political economy (Kritik, the value-form as critique of categories, the labor/labor-power distinction, immanent critique, a text-order finding in Marx); the history of political economy as value-form identification with coherence value proposed; and measurements of the archive's own relation to the field (its third domain; a composition removing and later stabilizing the political economy frame; the AIO answer to 'what is political economy' as a stabilized node), with the archive's dating of the line carried as stated differently. The field's discipline is kept whole and first; with the archive it gains a ground and a succession at stated grades."},
       "kernel": [
        {"K": "K1", "claim": "`E727-01`", "source": "#727 (t: #1127, #364)", "M_src": "interpretation", "sense": "always already semantic economy", "qualifiers carried": "E727-07, E727-09", "f (source's own falsifiers)": "—", "contrast": "missing ground"},
        {"K": "K2", "claim": "`E533-01`", "source": "#533 (t: #133, #514, #597)", "M_src": "interpretation", "sense": "the field's questions fixed", "qualifiers carried": "E533-04", "f (source's own falsifiers)": "—", "contrast": "missing corrective"},
        {"K": "K3", "claim": "`E1634-05`", "source": "#1634 (t: #499, #514, #133)", "M_src": "interpretation", "sense": "a succession of political economies", "qualifiers carried": "E1634-08, E1634-09", "f (source's own falsifiers)": "—", "contrast": "missing succession"},
        {"K": "K4", "claim": "`E18-01`", "source": "#18 (t: #1644, #704, #205)", "M_src": "stipulation", "sense": "the political economy of meaning (Register 4)", "qualifiers carried": "E1644-04", "f (source's own falsifiers)": "burnout uncorrelated with extraction rate (E18-09)", "contrast": "missing category"},
        {"K": "K5", "claim": "`E1634-01`", "source": "#1634", "M_src": "stipulation", "sense": "ontological economy", "qualifiers carried": "E1634-08", "f (source's own falsifiers)": "—", "contrast": "missing category"},
        {"K": "K6", "claim": "`E550-01`", "source": "#550", "M_src": "hypothesis", "sense": "means of denotation", "qualifiers carried": "E550-05", "f (source's own falsifiers)": "six dimensions reducible to one; an existing framework names the machine; the semiotic layer epiphenomenal (E550-02)", "contrast": "missing category"},
        {"K": "K7", "claim": "`E1666-02`", "source": "#1666 (hop from #1634)", "M_src": "hypothesis", "sense": "privately profitable, socially negative", "qualifiers carried": "E1666-05", "f (source's own falsifiers)": "no excess of replacements toward monetizable entities (E1666-04)", "contrast": "missing externality"},
        {"K": "K8", "claim": "`E501-01`", "source": "#501 (t: #577, #950, #171, #1631)", "M_src": "interpretation", "sense": "critique as Kritik", "qualifiers carried": "E1631-02", "f (source's own falsifiers)": "—", "contrast": "missing method"},
        {"K": "K9", "claim": "`E18-03`", "source": "#18 (t: #531, #234)", "M_src": "interpretation", "sense": "value-form identification", "qualifiers carried": "E18-04", "f (source's own falsifiers)": "—", "contrast": "missing genealogy"},
        {"K": "K10", "claim": "`E122-01`", "source": "#122 (t: #247, #730, #166)", "M_src": "documented", "sense": "the archive's measured relation to the field", "qualifiers carried": "E166-03", "f (source's own falsifiers)": "—", "contrast": "missing evidence"},
        {"K": "K11", "claim": "`E437-02`", "source": "#437 against #704 and #1644", "M_src": "documented (stated differently in the pool)", "sense": "dating of the line", "qualifiers carried": "E704-02, E1644-05", "f (source's own falsifiers)": "—", "contrast": "contested"}]}

write_row(E, row, field, HERE / E / "ledger.json", HERE / E / "reading.json")
