"""2026-11-13: erratum on #625 and its second deposit #902 (same text, same date), Prolegomena to the Historical Logos (Johannes Sigil, 2026-04-05). The operator: "the prolegomena to the historical
logos also contains the einexestein error - we need to add an erratum note clarifying that that is a hypothetical reconstruction of josephus' greek
from the slavonic that assumes the slavonic is a translation of the original greek, then give the actual linguistic form". The text stands as
deposited; the erratum is entered at the three loci. Forms asserted against the seated witnesses as #1762 aligns them.   python3 add_erratum.py"""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]; P = ROOT / "data/registry.json"
reg = json.loads(P.read_text(encoding="utf-8")); D = {d["deposit_number"]: d for d in reg["deposits"]}
T625 = (ROOT / D[625]["full_text_path"].lstrip("/")).read_text(encoding="utf-8"); T1762 = (ROOT / D[1762]["full_text_path"].lstrip("/")).read_text(encoding="utf-8")
SLAV = "Тогда явися мужь нѣкыи, и аще мужем достоино есть его нарещи … Тѣмь немощно ми есть нарещи его человѣком"
GRK = "Ἰησοῦς σοφὸς ἀνήρ, εἴγε ἄνδρα αὐτὸν λέγειν χρή"
for s in (SLAV, GRK, "The archive's earlier *ei exestin* is Whiston's English put back into Greek."): assert s in T1762, s
for s in ("the Slavonic Josephus's Greek Vorlage (date uncertain)", "the *ei exestin* of the Slavonic Josephus", "The Slavonic Josephus reproduces the identical structure as *ei exestin* (\"if it is lawful to call him man\")"): assert s in T625, s
E = {"date": "2026-11-13", "kind": "reconstruction given as attested text",
     "locus": "§III.1 Textual Stratum; §V, principle 2; §VI First Cycle (the three-term chain phainetai moi → si fas est → ei exestin)",
     "was": "*ei exestin* (\"if it is lawful to call him man\"), given as the Greek of the Slavonic Josephus ('the Slavonic Josephus's Greek Vorlage'; 'The Slavonic Josephus reproduces the identical structure as *ei exestin*')",
     "now": ("*ei exestin* is a hypothetical reconstruction of Josephus's Greek from the Slavonic, which assumes that the Slavonic is a translation of the original Greek; "
             "no Greek, Latin or Slavonic witness carries the phrase. The attested forms: the Slavonic War, after 2.174 (Meshcherskii 1958, Vilna Chronograph, EA-CORPORA-37/01): "
             "«" + SLAV + "», 'if it is fitting to call him a man … therefore it is impossible for me to call him a human being', the qualifier достоино, 'fitting'; "
             "the Greek Testimonium, Antiquities 18.63 (Niese, EA-CORPORA-01/01): «" + GRK + "», the qualifier χρή, 'needful'. The chain's third term in attested form is "
             "аще мужем достоино есть его нарещи, beside the Greek's εἴγε ἄνδρα αὐτὸν λέγειν χρή."),
     "reason": ("The reconstruction's wording, ἔξεστιν for 'lawful', follows Whiston's English of the Testimonium (1737: 'if it be lawful to call him a man') rather than the Slavonic's достоино. "
                "Traced in The Crossing of Names (#1762, §6); withdrawn in The Word That Became Text v2.0 (#1761) and entered as an erratum on v1.0 (#626)."),
     "raised_by": "Lee Sharks (2026-11-13)", "status": "recorded", "deposit_number": 1762}
for n in (625, 902):
    t = (ROOT / D[n]["full_text_path"].lstrip("/")).read_text(encoding="utf-8")
    assert "the Slavonic Josephus's Greek Vorlage (date uncertain)" in t, n
    d = D[n]; d.setdefault("errata", [])
    if not any(x.get("kind") == E["kind"] for x in d["errata"]): d["errata"].append(dict(E))
P.write_text(json.dumps(reg, ensure_ascii=False, separators=(",", ":")), encoding="utf-8"); print("ok", len(D[625]["errata"]), len(D[902]["errata"]))
