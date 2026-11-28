"""Dimensional PER for the thirteen captures of 2026-11-28, scored from the intake reader's spans against the atom sets built automatically
for their works the same day (scripts/build_work_atom_set.py), by scripts/per_intake_score.py. A span is the reader's evidence that an atom
is present; None is read and absent. Title, date and corpus are found by token. Rescored the same day after the sets and the readings were checked against EA-PER-RECALC-01 (#1694). --check verifies and prints, writing nothing."""
import json, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parents[3]; sys.path.insert(0, str(ROOT / "scripts"))
import per_intake_score as PIS
P = ROOT / "data/EA-WG-CAPTURES-01.json"
R = {
 "matthew-from-revelation-1812-lines-of-flight-chatgpt-20261128": (1812, "Lee Sharks's How to Write Matthew from Revelation", dict(
   author="Lee Sharks's How to Write Matthew from Revelation", **{"claim boundary": "the procedure's ability to generate a plausible Matthew passage does not establish that Matthew was historically composed from Revelation"},
   purpose="What operations would produce Matthew's particular narrative from Revelation's particular relations?", commitments="the paper prints the generated outputs, including their imperfections",
   lineage="#1735, Revelation First: Literary Genealogy and the Missing Ancestors of the Epistles", identifier="Deposit #1812: full paper and research record",
   **{"deposit chain": "compared with 86 relations reaching 178 verses in version 1.0"})),
 "matthew-from-revelation-1812-arguments-chatgpt-20261128": (1812, "Lee Sharks's paper", dict(
   author="Lee Sharks's paper", **{"claim boundary": "the demonstration alone cannot establish that Matthew was historically written from Revelation"},
   purpose="Suppose a writer possesses the whole of Revelation and wants to produce a Gospel. What must that writer do?", commitments="The author reports these rather than silently removing them.",
   lineage="The paper belongs to a larger intellectual programme called Revelation First.", identifier="Read the complete paper: Alexanarch deposit #1812",
   **{"deposit chain": "The current version of the deposit is v2.1, dated 27 November 2026."})),
 "how-much-you-wanna-bet-1810-lines-of-flight-chatgpt-20261128": (1810, "Rex Fraction's How Much You Wanna Bet?", dict(
   author="Rex Fraction's How Much You Wanna Bet?", **{"claim boundary": "These figures describe the computed archive structure, not a demonstrated 52-generation dependency in New Testament scholarship."},
   purpose="It is a recovery event: restoring a text to the position of source in the corpus that became the New Testament.",
   commitments="The dossier explicitly refuses to treat the debt it identifies as an automatically collectible financial claim.",
   lineage="A Single Sparrow (#1791)", identifier="The primary documents can be read through the Alexanarch #1810 deposit", **{"deposit chain": None})),
 "how-much-you-wanna-bet-1810-outside-the-archive-chatgpt-20261128": (1810, "How Much You Wanna Bet? The Value of a Recovery, from Both Ends: Revelation First under the Valuation Protocol (SEVP-VAL-003, Alexanarch deposit #1810, AXN:0D7C)", dict(
   author="Fraction maps these onto the dossier's argument", **{"claim boundary": "It does not claim to establish the historical thesis itself."},
   purpose="It is an attempt to make a contested historical and canonical recovery legible as a problem in political economy",
   commitments="The work's own revision and falsification provisions acknowledge these problems rather than concealing them.",
   lineage="A Single Sparrow (#1791), which establishes the Sappho–Plato relationship.", identifier="How Much You Wanna Bet? — Alexanarch deposit #1810, v1.1",
   **{"deposit chain": "Section 8e.5 corrects an earlier mathematical treatment"})),
 "how-much-you-wanna-bet-1810-cost-to-the-establishment-chatgpt-20261128": (1810, "I have located the public dossier.", dict(
   author=None, **{"claim boundary": "The paper explicitly audits it to failure on eight counts and does not present it as the value of the recovery."},
   purpose="it attempts to value not just the proposition, but the cost of institutional transition if the proposition is accepted",
   commitments="The authors acknowledge that the valuer has a material interest in the object and the protocol.", lineage=None, identifier=None,
   **{"deposit chain": "the public version I located identifies itself as v1.0, whereas your supplied description identifies v1.1"})),
 "revelation-first-not-the-first-revelation-1811-lines-of-flight-chatgpt-20261128": (1811, "Revelation First ≠ The First Revelation — #1811, AXN:0D7E", dict(
   author="Lee Sharks's thesis", **{"claim boundary": "Nor is disambiguation an endorsement of the thesis."},
   purpose="The packet insists that an answer about the second entity is not an answer about the first.", commitments=None,
   lineage="Revelation First: Literary Genealogy and the Missing Ancestors of the Epistles (#1735)", identifier="Revelation First ≠ The First Revelation — #1811, AXN:0D7E",
   **{"deposit chain": "positional liquidation is the significant addition in v1.1"})),
 "through-anothers-mouth-1807-lines-of-flight-chatgpt-20261128": (1807, "Johannes Sigil's Through Another's Mouth: A Dialogue between Heteronyms (#1807)", dict(
   author="Johannes Sigil's Through Another's Mouth", **{"claim boundary": "#1807 explicitly says that it does not establish anything that #1806 does not ground"},
   purpose="It makes that shaping happen inside its own literary form.", commitments="Sharks's words are designated the fixed witness: the recorded statements are preserved rather than subjected to the voice-transforming apparatus.",
   lineage="The dialogue's primary companion is Lee Sharks's #1806", identifier="Primary documents: #1807 — Through Another's Mouth", **{"deposit chain": None})),
 "rejected-1806-lines-of-flight-chatgpt-20261128": (1806, "Lee Sharks's From the Position of the Rejected", dict(
   author="Lee Sharks's From the Position of the Rejected", **{"claim boundary": "The essay does not establish Aristotle's subjective feelings or intentions."},
   purpose="It makes it possible to read institutions, texts and intellectual traditions not from the position of the people they recognize as their authors, citizens or legitimate inheritors",
   commitments=None, lineage="Sappho 31 and the Inscription of the Future Reader — the future-reader framework.", identifier="Lee Sharks, #1806 — From the Position of the Rejected (v1.1)",
   **{"deposit chain": "Version 1.1 makes a particularly important move from political theory to material history."})),
 "inferential-provenance-riemann-1804-lines-of-flight-chatgpt-20261128": (1804, "Sen Kuro's The Inferential Provenance of the Riemann Result", dict(
   author="Sen Kuro's The Inferential Provenance of the Riemann Result", **{"claim boundary": "It is not proof that Claude independently authored the declaration"},
   purpose="the systematic reconstruction of how knowledge is produced, verified, attributed, transmitted and economically appropriated when humans and AI systems work together",
   commitments="The original paper's CC BY 4.0 publication", lineage="Critique of Pure Inference (#1766): formation, standing and transmission.",
   identifier="EA-IPRH-01 — The Inferential Provenance of the Riemann Result (#1804)", **{"deposit chain": None})),
 "what-the-filters-kept-1803-lines-of-flight-chatgpt-20261128": (1803, "What the Filters Kept — #1803, v2.0", dict(
   author=None, **{"claim boundary": "no artificial transmission has been identified"},
   purpose="it moves the 3I/ATLAS discussion away from the binary question of whether the object is artificial",
   commitments="it preserves the conditions under which its conclusions might have to change",
   lineage="The notebook invokes the earlier archive concept of instrument-conditioned nullity (#1450, §3.2)", identifier="What the Filters Kept — #1803, v2.0",
   **{"deposit chain": "earlier version, useful for tracing what changed when the voltage phase was incorporated"})),
 "who-benefits-from-bad-inference-1802-lines-of-flight-chatgpt-20261128": (1802, "Lee Sharks's Who Benefits from Bad Inference? (#1802, AXN:0D45)", dict(
   author="Lee Sharks's Who Benefits from Bad Inference?", **{"claim boundary": "They are not a representative sample of all institutional inference."},
   purpose="the central question is not simply whether an inference is wrong, but what the wrong inference enables",
   commitments="It also distinguishes evidence from interpretation and proposes six tests that would weaken its account.",
   lineage="#1666, The Margin of Flattening.", identifier="Alexanarch deposit #1802, AXN:0D45", **{"deposit chain": None})),
 "la-la-ka-ka-la-wrrir-akerir-quoted-aio-20261128": (1809, "is the opening line and archival title of an untitled ten-line sound poem by Lee Sharks", dict(
   author="sound poem by Lee Sharks", purpose="an untitled ten-line sound poem by Lee Sharks", commitments=None, lineage=None,
   identifier="cataloged in the Alexanarch archive under deposit #1809", **{"deposit chain": None, "claim boundary": None})),
}
TRAD = {
 "matthew-from-revelation-1812-lines-of-flight": "the first substantial Gospel-level demonstration of a proposed generative philology",
 "matthew-from-revelation-1812-arguments": "A philological argument",
 "how-much-you-wanna-bet-1810-lines-of-flight": "Brings these strands together into the valuation dossier.",
 "how-much-you-wanna-bet-1810-outside-the-archive": "an experimental work in critical political economy of knowledge, with biblical textual history as its test case",
 "how-much-you-wanna-bet-1810-cost-to-the-establishment": "A paper operating under a Valuation Protocol",
 "revelation-first-not-the-first-revelation-1811": "The packet leads from protecting the identity of a thesis",
 "through-anothers-mouth-1807": "The dialogue establishes five distinct speaking positions:",
 "rejected-1806": "The essay's central proposition is that political order can turn a condition produced by circumstance into an apparent fact of nature.",
 "inferential-provenance-riemann-1804": "The Riemann case supplies the demonstration.",
 "what-the-filters-kept-1803": "#1803 is the technical notebook: the evidence, code, frozen plans, result files, methodological qualifications and revision history.",
 "who-benefits-from-bad-inference-1802": "The paper's most consequential theoretical move is its demand-formation corollary (§16).",
 "la-la-ka-ka-la": "sound poem"
}
SS = {"rejected-1806-lines-of-flight-chatgpt-20261128": [{"proxy": "scholarly consensus", "span": "belongs to the wider archive's reconstruction, not to an established scholarly consensus",
       "displaced": "argument", "internal": False}]}   # EA-PER-RECALC-01 §3.9.3: a proxy outside the entity is recorded and the atoms are scored as found
reg = json.loads(P.read_text(encoding="utf-8")); E = {e["slug"]: e for e in reg["entries"]}; out = {}; bad = []
for slug, (dep, reached, atoms) in R.items():
    e = E[slug]; S = PIS.resolve(dep); req = set(S["required"])
    atoms = dict(atoms, tradition=next(v for k, v in TRAD.items() if slug.startswith(k)))
    reading = {"target": dep, "reached": {"kind": "same", "span": reached, "basis": "the work named and read"}, "atoms": {k: v for k, v in atoms.items() if k in req}, "src": True,
               "standing_substitutions": SS.get(slug) or [],
               "notes": "Scored 2026-11-28 against the set built automatically from the record (%s). Not required, because the record does not state them: %s." % (S["id"], ", ".join(a["atom"] for a in S["atoms"] if a["applicability"] != "required") or "none")}
    pd, why = PIS.score(slug, e["transcript"], e["q"], e["date"], e["surface"], reading, brief="rebuild/capture-registry/intake-20261128-lines-of-flight-eight-and-two/score_per_dim.py")
    if pd: out[slug] = pd; print(f"{pd['scores']['PER']:.2f}  M {pd['scores']['M']} C {pd['scores']['C']} D {pd['scores']['D']}  {slug[:58]}  absent: {[a['atom'] for a in pd['atoms'] if not a['present']]}")
    else: bad.append((slug, why)); print("  ✗", slug[:50], why[:300])
print(len(out), "scored;", len(bad), "not scored")
if "--check" in sys.argv or bad: sys.exit(1 if bad else 0)
for slug, pd in out.items():
    e = E[slug]; _was = (e.get("per_dim") or {}).get("scores"); e["per_dim"] = pd; e["per_dim_pending"] = None
    for o in e.get("observations") or []:
        o["per_dim"] = pd; o["per_dim_pending"] = None
    reg["correction_log"].append({"date": "2026-11-28", "slug": slug, "fields": ["per_dim", "per_dim_pending"], "was": {"per_dim": _was},
        "now": {"per_dim": pd["scores"], "target": pd["target"]["ent"]}, "reason": "rescored against EA-PER-RECALC-01 (#1694): the tradition atom added to the automatic sets (§3.4), lineage named by word (§3.10), one standing substitution recorded (§3.9.3)", "by": "the session (2026-11-28)"})
m = re.fullmatch(r"(\d+)\.(\d+)", reg["version"]); reg["version"] = f"{m.group(1)}.{int(m.group(2)) + 1}"
P.write_text(json.dumps(reg, ensure_ascii=False, indent=1), encoding="utf-8"); print("written; registry", reg["version"])
