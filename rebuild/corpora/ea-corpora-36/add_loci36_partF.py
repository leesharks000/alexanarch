"""EA-CORPORA-36 v1.1 Part F loci (36/33–36/40): each asserted present, whitespace-normalized, in the text layer it names, in the layer's
own readings, then written into the seat's spec.   python3 add_loci36_partF.py"""
import json, pathlib
H = pathlib.Path(__file__).resolve().parent; C = H.parents[2] / "data/corpora"
norm = lambda s: " ".join(s.split())
L = {
'hermann-elementa-1816': [
 ("Hermann 1816: the jealousy reading stated as the sense of fr. 31's last line (OCR)", "hermann-1816.ocr",
  "Si hic, quemputo, sensus est horum verborum, invidens Sap- pho viro illi, omnia sibi audenda dicit, quoniam puellam nimis securam amore illius calefieri sentiat."),
 ("Hermann: the last line held to be the poet's words, not her quoter's (OCR)", "hermann-1816.ocr",
  "Vltimum versum non scri- ptoris, qui affert carmen hoc, sed ipsius poetriae verha continere")],
'plutarch-demetrius-amatorius': [
 ("Plutarch, Demetrius 38: the things of Sappho in Antiochus at Stratonice's coming", "plutarch-demetrius",
  "ἐγίνετο τὰ τῆς Σαπφοῦς ἐκεῖνα περὶ αὐτὸν πάντα, φωνῆς ἐπίσχεσις, ἐρύθημα πυρῶδες, ὄψεων ὑπολείψεις, ἱδρῶτες ὀξεῖς"),
 ("Plutarch, Amatorius 18 (763a): fr. 31 as what happens at the beloved's appearing", "plutarch-amatorius",
  "ἐν οἷς ἡ καλὴ Σαπφὼ λέγει τῆς ἐρωμένης ἐπιφανείσης τήν τε φωνὴν ἴσχεσθαι")],
'erasistratus-witnesses': [
 ("Valerius Maximus 5.7 ext. 1: the physician reads the blush and the pallor", "valerius-maximus",
  "ut eum ad introitum Stratonices rubore perfundi et spiritu increbrescere eaque egrediente pallescere"),
 ("Appian, Syriaca 59: Erasistratus names the woman", "appian-syriaca", "ὁ Ἐρασίστρατος ἔφη· τῆς ἐμῆς γυναικὸς ἐρᾷ")],
'gellius-noctes-atticae': [
 ("Gellius 19.9.11: Valerius Aedituus, the Latin fr. 31 before Catullus", "gellius",
  "Aeditui versus: Dicere cum conor curam tibi, Pamphila, cordis, Quid mi abs te quaeram? verba labris abeunt")],
'maximus-tyrius': [
 ("Maximus of Tyre 18.9: Sappho's rivals as Socrates's", "maximus-dissertationes",
  "ὅ τιπερ Σωκράτει οἱ ἀντίτεχνοι, Πρόδικος καὶ Γοργίας καὶ Θρασύμαχος καὶ Πρωταγόρας, τοῦτο τῇ Σαπφοῖ Γοργὼ καὶ Ἀνδρομέδα")],
'racine-phedre': [
 ("Racine, Phèdre I.3: the avowal", "phedre-acte-i", "Je le vis, je rougis, je pâlis à sa vue ;")],
'smollett-roderick-random': [
 ("Smollett's fr. 31, its added close", "roderick-random", "Unheard I mourn, unknown I sigh, Unfriended live, unpitied die!")],
'wikipedia-sappho-31': [
 ("Wikipedia, 'Sappho 31': the jealousy reading dated to the eighteenth century", "wikipedia-sappho-31",
  "As far back as the eighteenth century, it has been proposed that the poem is about Sappho's jealousy of the man who sits with her beloved."),
 ("Wikipedia, 'Sappho 31': the first modern translations through Catullus", "wikipedia-sappho-31",
  "The first translations of the poem into modern languages derived from [[Catullus]]' re-visitation of the poem, [[Catullus 51]], painting Sappho with a green taint of jealousy.")],
}
for corpus, loci in L.items():
    f = H / f"spec36-{corpus}.json"; s = json.loads(f.read_text(encoding="utf-8")); out = []
    for label, slug, find in loci:
        p = next((C / corpus / "text").glob(slug + ".*"))
        assert norm(find) in norm(p.read_text(encoding="utf-8")), (corpus, find[:50])
        out.append({"label": label, "text": f"text/{p.name}", "find": find})
    s["loci"] = out; f.write_text(json.dumps(s, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"); print("ok", corpus, len(out))
