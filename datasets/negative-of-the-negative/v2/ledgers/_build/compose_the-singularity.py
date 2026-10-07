import json, hashlib, sys, pathlib, re
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from compose_common import *

E = "the-singularity"
field = json.loads((HERE / E / "field.json").read_text(encoding="utf-8"))
ledger = json.loads((HERE / E / "ledger.json").read_text(encoding="utf-8"))
tp = "datasets/negative-of-the-negative/v2/intake/battery-1c-20261007/paste-the-singularity.txt"
traw = (REPO / tp).read_text(encoding="utf-8")
body = traw.split("the singularitythe singularity", 1)[1].split("\nWikipedia\nTechnological singularity")[0]
body = re.sub(r"\(https?://[^)]*\)", "", re.sub(r"\[\[.*?\]\]", "", body))  # composition text without citation markup

FIELD_PARAS = [
 [("The technological singularity, often simply called the singularity, is a hypothetical event in which technological growth accelerates beyond human control, producing unpredictable changes in human civilization; other definitions place it at the point where AI surpasses human intelligence and can improve itself better than humans can, or describe a theoretical scenario in which technological growth becomes uncontrollable and irreversible.", ["F1", "F20", "F25", "F38"]),
  ("Britannica describes a theoretical condition that could arrive in the near future when a synthesis of several powerful new technologies will radically change the realities in which we find ourselves, and some writers use the term broadly for any radical change in society brought about by new technology, although Vinge and other writers say that without superintelligence such changes would not be a true singularity.", ["F44", "F17"])],
 [("John von Neumann is the first person known to have discussed a \"singularity\" in technological progress; Stanislaw Ulam reported in 1958 a discussion with him of approaching \"some essential singularity in the history of the race beyond which human affairs, as we know them, could not continue\".", ["F7", "F8"]),
  ("In the most popular version, I. J. Good's intelligence explosion model of 1965, an upgradable intelligent agent could enter a positive feedback loop of successive self-improvement cycles; on Good's account the first ultraintelligent machine is the last invention that man need ever make, provided that the machine is docile enough to tell us how to keep it under control.", ["F2", "F9", "F21", "F43"]),
  ("Vernor Vinge popularized the concept and the term, first in a 1983 op-ed in Omni magazine; in his 1993 essay \"The Coming Technological Singularity\" he wrote that the transition would signal the end of the human era, and that he would be surprised if it occurred before 2005 or after 2030.", ["F10", "F11", "F12"]),
  ("Ray Kurzweil's 2005 book The Singularity Is Near, which sets out a Law of Accelerating Returns predicting an exponential increase in technologies, gave wider circulation to the notion, and Kurzweil set the date for the Singularity as 2045; a sequel, The Singularity Is Nearer, was released on June 25, 2024.", ["F33", "F35", "F13", "F34", "F37"])],
 [("Good, Vinge and Kurzweil argue that it is difficult or impossible for present-day humans to predict what life would be like in a post-singularity world, Vinge's \"opaque wall across the future\", as Britannica reports it; one commentator puts it that the singularity is about us, the moment we lose the ability to see what's coming.", ["F14", "F45", "F30"]),
  ("Artificial general intelligence is placed one step before: Third Way holds that AGI will quickly lead to artificial superintelligence in a process known as the intelligence explosion, and Bernard Marr writes that AGI is a level of capability and the singularity is what could happen next, its key test whether AI can improve itself without human direction; the related concept of speed superintelligence describes an AI that can function like a human mind but much faster.", ["F22", "F39", "F40", "F15"])],
 [("Technology forecasters and researchers disagree about when, or whether, human intelligence will be surpassed: Third Way reports an emerging consensus among experts that AGI should arrive at least by the end of the decade, Marr quotes the view that \"we are now, like, in the singularity\", and Daniel Miessler notes that Vinge's thirty-year window from 1993 has basically closed while his specific claim remains outstanding.", ["F16", "F23", "F41", "F32"]),
  ("Prominent technologists and academics dispute the plausibility of a technological singularity, among them Paul Allen, Steven Pinker, Theodore Modis, Gordon Moore and Roger Penrose, and a critic's judgment is quoted that \"there is not the slightest reason to believe in a coming singularity\".", ["F3", "F19"]),
  ("One objection is that AI growth is likely to run into decreasing returns: Russell and Norvig observe that improvement in a particular area tends to follow an S curve, and, in the reception of Kurzweil's book, the reply that \"the key point about exponential growth is that it never lasts\", skeptics note a decline in the rate of technological innovation, and many critics argue that significant and perhaps insurmountable obstacles stand in the way; nor is a singularity required for machines that perform at or beyond a human level on certain tasks, whose existence does not imply its possibility.", ["F4", "F5", "F36", "F28", "F27", "F6"])],
 [("Its sign is unknown: it is unclear whether it would be beneficial or harmful, or even an existential threat, Britannica says it could be amazing or apocalyptic, but we cannot know the details, and reports Vinge's words that the new era is \"simply too different to fit into the classical frame of good and evil\".", ["F18", "F47", "F46"]),
  ("Britannica reports Kurzweil's expectation that \"in the future we will have the medical tools to banish disease and disease-related death\", while others voice concern that superintelligent machines could prioritize their own survival and goals over human needs.", ["F48", "F29"])],
]

ARCHIVE_PARAS = [
 [("A further position, proposed in the archive's paper The Final Time, changes the singularity's object: the singularity literature is read as defining its singularity through a rapid increase in machine intelligence, a theory of runaway intelligence, and as a family of hypotheses, with Good supplying the recursive core, Vinge discontinuity and Kurzweil acceleration with the horizon still around 2045.", ["G1635-01", "G1635-03", "G1635-13", "G1635-08", "G1635-09", "G1635-10", "G1637-11"]),
  ("There a contingent singularity is defined as a historical threshold at which the material machinery that makes symbolic difference operable becomes capable of altering the viability of further dialectical difference itself; singularity is specified as a breakdown or transformation in the rule governing continuation, held nearer to Vinge's \"old models must be discarded\" than to an infinite rate of intelligence growth, and the paper's central contradiction is stated as a hypothesis, that a system can grow better at generating negations while growing worse at letting a negation acquire independent historical existence.", ["G1635-02", "G1635-16", "G1635-17", "G1635-04", "G1635-05"]),
  ("The singularity so defined is held double, terminal closure, in which no competing order retains a viable route to independently standing reproduction, or terminal reflexivity, durable invariance while future rivals remain viable, \"durability without finality\"; and more than one incompatible future, a field of competing contingent Omegas, is held able to remain viable from the same present.", ["G1635-19", "G1635-20", "G1635-21", "G1635-24", "G1635-22"])],
 [("The two singularities are held able to coexist: a technological singularity could accelerate a contingent singularity or be irrelevant to it, and a society could reach high machine capability without terminal symbolic closure, or approach closure without superintelligence; where the technological singularity's control problem is whether humans can control superintelligence, the contingent singularity's is whether any order can control the conditions of its own negation.", ["G1635-26", "G1635-27", "G1635-18"]),
  ("On this reading intelligence growth is not the decisive variable: Thorstad's critique of the growth assumptions is held not to be a problem for the theory in the way it is for the intelligence explosion, a finite system can be terminal for a field if it controls enough of the field's conditions of reproduction, and the catastrophe can be bureaucratic, smooth and finite, since \"nothing has to be superhuman for the exits to close\".", ["G1635-29", "G1635-14", "G1635-15", "G1635-30", "G1635-31"]),
  ("The final time is specified as a viability boundary, one that can be crossed without anyone noticing the day, and the paper holds that no apocalypse is required: the world, the platforms, the machines and language continue, and what ends is the structural possibility that contradiction becomes a durable outside.", ["G1635-34", "G1635-35"])],
 [("Another deposit states that in The Final Time the singularity is a point of closure, the technological singularity reread as an end of history in the bad sense; the paper itself also defines a positive singularity, with terminal reflexivity its criterion.", ["G1643-01", "G1643-02", "G1637-07", "G1635-19"]),
  ("The paper declines to claim that the boundary has been crossed, or that recursive self-improvement is impossible or irrelevant; in its seated text it also declines to claim that a technological singularity is impossible, or that the present decade is the final time, and it calls \"singularity\" a contested family-resemblance term to which it proposes \"a distinct member of the family\".", ["G1635-06", "G1637-02", "G1635-38", "G1637-03", "G1637-11"]),
  ("It predicts that intelligence explosion is neither necessary nor sufficient for the contingent singularity, and specifies as a counterexample a case where independent symbolic exteriority remains robust despite near-total concentration of the symbolic machinery, or where exteriority collapses solely as a function of intelligence growth.", ["G1635-36", "G1635-37"])],
]

KO = sents(FIELD_PARAS + ARCHIVE_PARAS)
KO_B = sents(FIELD_PARAS)

sec_def = {"icon": "🧭", "head": "Definitions", "items": [
    {"label": "Hypothetical event:", "text": "technological growth accelerating beyond human control.", "claims": ["F1", "F25"]},
    {"label": "AI that surpasses us", "text": "and improves itself beyond our control or prediction.", "claims": ["F20", "F38"]},
    {"label": "Broader sense, disputed:", "text": "any radical technology-driven change; for Vinge no true singularity without superintelligence.", "claims": ["F17", "F44"]}]}
sec_lin = {"icon": "📜", "head": "Lineage", "items": [
    {"label": "Von Neumann, Ulam 1958:", "text": "a singularity beyond which human affairs could not continue.", "claims": ["F7", "F8"]},
    {"label": "Good 1965:", "text": "the intelligence explosion; the last invention, if docile enough.", "claims": ["F2", "F9", "F21"]},
    {"label": "Vinge 1983, 1993:", "text": "popularized the term; the end of the human era.", "claims": ["F10", "F11"]},
    {"label": "Kurzweil 2005:", "text": "accelerating returns; the date set as 2045.", "claims": ["F13", "F34", "F35"]}]}
sec_time = {"icon": "⏳", "head": "Timing and dispute", "items": [
    {"label": "No agreed date:", "text": "AGI by the decade's end, 'in the singularity' now, Vinge's window closed.", "claims": ["F16", "F23", "F41", "F32"]},
    {"label": "Plausibility disputed:", "text": "Allen, Pinker, Modis, Moore, Penrose.", "claims": ["F3", "F19"]},
    {"label": "Saturation:", "text": "S curves, exponentials that never last, obstacles.", "claims": ["F4", "F5", "F36", "F27"]}]}
sec_out = {"icon": "⚖️", "head": "Outcomes", "items": [
    {"label": "Unpredictable:", "text": "an opaque wall across the future.", "claims": ["F14", "F45", "F30"]},
    {"label": "Sign unknown:", "text": "beneficial, harmful, or an existential threat.", "claims": ["F18", "F47"]},
    {"label": "Hopes and fears:", "text": "disease banished; machine goals over human needs.", "claims": ["F48", "F29"]}]}
P = {"title": "The (technological) singularity", "genre": "popup — the compression: AIO's interaction grammar (lede, headed clusters, bolded terms, card rail), modality in the typography, a rail of claim lineages",
     "status": "composed 2026-10-07 from the entity's ledgers (field %d claims; archive %d); not frozen" % (len(field["field_claims"]), len(ledger)),
     "entity": "The entity evolves: the field's singularity (runaway intelligence, unpredictable, dated and disputed) is kept in full and first; with the archive admitted, it gains a proposed re-objection, the contingent singularity, a threshold in the viability of further dialectical difference, double and contingent, independent of intelligence growth, stated with its limits and a specified counterexample, and unsettled within the archive on its sign.",
     "lede": {"text": "is a hypothetical event in which technological growth accelerates beyond human control, most often pictured as AI that surpasses human intelligence and improves itself; a further position, proposed, re-objects it as a contingent singularity, a threshold in the viability of further dialectical difference.",
              "claims": ["F1", "F20", "F2", "G1635-01", "G1635-02"]},
     "sections": [sec_def, sec_lin, sec_time, sec_out,
      {"icon": "🔁", "head": "Re-objected (proposed)", "items": [
        {"label": "Contingent singularity:", "text": "the machinery of symbolic difference altering the viability of further dialectical difference.", "claims": ["G1635-02", "G1635-01"]},
        {"label": "A rule-change:", "text": "a breakdown in the rule governing continuation, nearer Vinge than infinite growth.", "claims": ["G1635-16", "G1635-17"]},
        {"label": "Hypothesis:", "text": "better at generating negations, worse at letting them stand.", "claims": ["G1635-04"]}]},
      {"icon": "🌓", "head": "Double and contingent", "items": [
        {"label": "Two finals:", "text": "terminal closure, or terminal reflexivity (durability without finality).", "claims": ["G1635-19", "G1635-20", "G1635-21"]},
        {"label": "Competing contingent Omegas:", "text": "several futures can remain viable from one present.", "claims": ["G1635-22", "G1635-24"]},
        {"label": "Beside the technological singularity:", "text": "may coincide, need not; nothing has to be superhuman.", "claims": ["G1635-26", "G1635-18", "G1635-31"]}]},
      {"icon": "⚠️", "head": "Limits and contest", "items": [
        {"label": "Non-claims:", "text": "declines to claim the boundary crossed, or a technological singularity impossible; 'final' names a viability boundary.", "claims": ["G1635-06", "G1637-02", "G1637-03"]},
        {"label": "Counterexample specified:", "text": "robust exteriority under near-total concentration, or collapse by intelligence growth alone.", "claims": ["G1635-36", "G1635-37"]},
        {"label": "Sign, contested within:", "text": "a point of closure, an end of history in the bad sense (#1643); closure or reflexivity, a positive singularity defined (#1635, #1637).", "claims": ["G1643-01", "G1643-02", "G1635-19", "G1637-07"]}]}],
     "rail": []}

# rail: one entry per lineage, in order of first appearance; field lineages first
fc = field["field_claims"]
order = []
for k, v in fc.items():
    if v["lineage"] not in [o[0] for o in order]:
        order.append((v["lineage"], "F"))
for c in ledger:
    if c["lineage"] not in [o[0] for o in order]:
        order.append((c["lineage"], "G"))
for lin, kind in order:
    if kind == "F":
        cl = [k for k, v in fc.items() if v["lineage"] == lin]
        P["rail"].append({"lineage": lin, "claims": cl, "earliest": fc[cl[0]]["source"]})
    else:
        cl = [c["id"] for c in ledger if c["lineage"] == lin]
        P["rail"].append({"lineage": lin, "claims": cl, "earliest": min(c["dep"] for c in ledger if c["lineage"] == lin)})
nF = sum(1 for _, k in order if k == "F")

P_B = {"title": "The (technological) singularity", "arm": "B (the field alone)", "genre": P["genre"], "status": "composed 2026-10-07 from the field ledger alone; not frozen",
       "entity": "The entity does not evolve: with no archive claims admitted, the entry is the field's singularity at its full resolution.",
       "lede": {"text": "is a hypothetical event in which technological growth accelerates beyond human control, most often pictured as AI that surpasses human intelligence and improves itself; its date and its plausibility are disputed.", "claims": ["F1", "F20", "F2", "F16", "F3"]},
       "sections": [sec_def, sec_lin, sec_time, sec_out], "rail": P["rail"][:nF]}

KOo = {"title": "The (technological) singularity", "genre": "The (technological) singularity encyclopedic knowledge object (the plan of L(B ∪ A), realized without provenance in the prose)",
       "status": "draft 2026-10-07; composed from the entity's ledgers on the operator's instruction; not frozen; ledger unaudited",
       "sentences": KO}
KOb = {"title": "The (technological) singularity", "arm": "B (the field alone)", "genre": "the same plan, the field alone", "status": "draft 2026-10-07; not frozen", "sentences": KO_B}

T = {"path": tp, "sha256": hashlib.sha256(traw.encode()).hexdigest(), "words": words(body), "cards": 11,
     "words_note": "words of the composition before the card list, citation link markup removed",
     "claims": ["T1 definition: a hypothetical future moment when AI surpasses human capability, triggering runaway self-improvement",
                "T2 Good 1965: an ultra-intelligent machine designing smarter successors, a feedback loop into ASI",
                "T3 loss of predictability, by analogy with the centre of a black hole",
                "T4 Vinge popularized the term in a 1993 essay; Kurzweil expanded it in The Singularity is Near",
                "T5 AGI as the gateway to recursive self-improvement",
                "T6 Kurzweil's 2045; some modern tech executives suggest sooner",
                "T7 optimistic views: human-machine integration, the end of severe disease, the end of physical labor scarcity",
                "T8 existential risks: permanent loss of human control, economic disruption, existential threats"],
     "register": {"register": "datasets/negative-of-the-negative/v2/register.json", "slug": "the-singularity-20261007", "obs_id": "OBS-6ed827398719"}}

row = {"row": E, "entity": E, "address": "the singularity", "addresses": ["the singularity"], "epoch": "2026-10-07", "type": "C (public entity)",
       "surface": "Google AI Overview (expanded)", "auth": "signed out, incognito",
       "status": {"procedure": "EA-NEGONT-02 v0.7 (#1665); entity before address (ruled 2026-10-07); archive selected by D/R/O, first reading 2026-10-07 (3 of 81 admitted), hop not run",
                  "ledger": "unaudited (§3.8: one extractor per ledger; field excerpts by WebFetch, archive quotes verified verbatim %d/%d); the archive's statements of the singularity's sign are carried as contested within the pool (#1635/#1637 against #1643)" % (sum(1 for c in ledger if c.get("quote_ok")), len(ledger)), "frozen": False},
       "spec": "EA-NEGONT-02 v0.7, #1665",
       "objects": {"T": T, "KO": KOo, "P": P, "P_B": P_B, "KO_B": KOb},
       "field": [{"id": x["id"], "card": x["card"], "fetched": x["fetched"]} for x in field["field"]],
       "delta": {"T_vs_LB": "T composes the definition (F1, F20, F25, F38), Good's intelligence explosion (F2, F21, F43), loss of predictability (F14, F30, F45), Vinge and Kurzweil (F11, F13, F33, F34), AGI as the step before (F22, F39), Kurzweil's 2045 and nearer dates (F13, F23, F41), and optimistic and catastrophic outcomes (F48, F29). T dates Vinge's popularization to the 1993 essay; the field dates it first to a 1983 Omni op-ed (F10). Available in the field and not composed: von Neumann and Ulam's 1958 report (F7, F8); Good's docility proviso (F9); Vinge's 2005–2030 window (F12) and its closing (F32); the dispute of plausibility and the named critics (F3, F19); decreasing returns, the S curve, exponentials that never last, the declining rate of innovation, perhaps insurmountable obstacles (F4, F5, F36, F28, F27); that human-level task performance neither requires nor implies a singularity (F6); the broader sense and Vinge's denial of it (F17, F44, F49); the forecasters' disagreement (F16); the unknown sign (F18, F46, F47); speed superintelligence (F15); the policy frame (F24). T's black-hole analogy and its 'human-machine integration' and 'elimination of physical labor scarcity' are not in the field ledger's quotes.",
                 "LB_vs_LBA": "Admission adds a position the field does not hold: the singularity re-objected from runaway intelligence to the viability of further dialectical difference (the contingent singularity); singularity specified as a rule-change in continuation, aligned with Vinge's discontinuity against the growth criterion; the field's literature taken as coordinates, a family of hypotheses (Good, Vinge, Kurzweil, Chalmers, Bostrom, Thorstad); a double singularity (terminal closure or terminal reflexivity) and a field of competing contingent Omegas; coexistence with the technological singularity, which it may accelerate or leave untouched; closure without superintelligence, the catastrophe bureaucratic, smooth and finite; the final time as a viability boundary; and its non-claims, prediction and specified counterexample. The field's own skeptics (saturation, S curves) are met by the archive as not touching its variable. Carried as contested: #1643 states the thesis as closure, the technological singularity reread as an end of history in the bad sense; the paper (#1635, #1637) defines a double sign. The field's singularity is kept whole and first; with the archive it gains a further member of the family at stated grades."},
       "kernel": [
        {"K": "K1", "claim": "`G1635-01`", "source": "#1635 (t: #1637)", "M_src": "interpretation", "sense": "the singularity re-objected", "qualifiers carried": "G1635-03", "f (source's own falsifiers)": "—", "contrast": "missing distinction"},
        {"K": "K2", "claim": "`G1635-02`", "source": "#1635 (t: #1637)", "M_src": "stipulation", "sense": "contingent singularity defined", "qualifiers carried": "G1637-04", "f (source's own falsifiers)": "—", "contrast": "missing category"},
        {"K": "K3", "claim": "`G1635-16`", "source": "#1635 (t: #1637)", "M_src": "stipulation", "sense": "singularity as rule-change", "qualifiers carried": "G1635-17", "f (source's own falsifiers)": "—", "contrast": "missing distinction"},
        {"K": "K4", "claim": "`G1635-04`", "source": "#1635 (t: #1637)", "M_src": "hypothesis", "sense": "generate against reproduce", "qualifiers carried": "G1635-05", "f (source's own falsifiers)": "—", "contrast": "missing relation"},
        {"K": "K5", "claim": "`G1635-19`", "source": "#1635 (t: #1637)", "M_src": "stipulation", "sense": "a double singularity", "qualifiers carried": "G1635-20, G1635-21, G1637-07", "f (source's own falsifiers)": "—", "contrast": "missing category"},
        {"K": "K6", "claim": "`G1635-22`", "source": "#1635 (t: #1637)", "M_src": "interpretation", "sense": "competing contingent Omegas", "qualifiers carried": "G1635-24", "f (source's own falsifiers)": "—", "contrast": "missing category"},
        {"K": "K7", "claim": "`G1635-26`", "source": "#1635 (t: #1637)", "M_src": "interpretation", "sense": "the two singularities coexist", "qualifiers carried": "G1635-18, G1635-27", "f (source's own falsifiers)": "—", "contrast": "missing relation"},
        {"K": "K8", "claim": "`G1635-31`", "source": "#1635 (t: #1637)", "M_src": "interpretation", "sense": "closure without superintelligence", "qualifiers carried": "G1635-30, G1637-05", "f (source's own falsifiers)": "exteriority collapsing solely as a function of intelligence growth (G1635-37)", "contrast": "missing distinction"},
        {"K": "K9", "claim": "`G1635-36`", "source": "#1635 (t: #1637)", "M_src": "hypothesis", "sense": "independent of intelligence growth", "qualifiers carried": "G1635-15, G1635-29", "f (source's own falsifiers)": "robust exteriority despite near-total concentration (G1635-37)", "contrast": "missing limit"},
        {"K": "K10", "claim": "`G1637-02`", "source": "#1637 (t: #1635)", "M_src": "self-description", "sense": "the reading's limits", "qualifiers carried": "G1635-06, G1637-03, G1635-38, G1637-11", "f (source's own falsifiers)": "—", "contrast": "missing limit"},
        {"K": "K11", "claim": "`G1643-02`", "source": "#1643 against #1635 and #1637", "M_src": "interpretation (contested in the pool)", "sense": "the singularity's sign unsettled", "qualifiers carried": "G1643-01, G1635-19, G1637-07", "f (source's own falsifiers)": "—", "contrast": "contested"}]}

write_row(E, row, field, HERE / E / "ledger.json", HERE / E / "reading.json")
