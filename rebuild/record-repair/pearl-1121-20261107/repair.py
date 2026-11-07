"""#1121 Pearl and Other Poems: the record's text corrected from a stub to the book (2026-11-07).

Ruling (Lee Sharks, 2026-11-07 02:35 EST): "lets correct that stub." Occasion (02:31): "there are about six different projections of pearl
you could check for that line, and it exists in every one of them without linebreaks" — a check of the RCF capture (0C3C) had searched only
#1121's record text, which was the 10 KB blog post "Zenodo Metadata: Pearl and Other Poems" (#329's text), and found nothing of the book.

The body becomes the book: the archive's machine score of the 2014 PDF (scripts/render_pearl_machine_text.py), the copy seated at
EA-CORPORA-03/02 and served by traininglayerliterature.org/pearl (image paths absolute), set in a fenced block so its whitespace renders.
The attachments are untouched: the PDF stays the artwork. The prior text's hash and AXN are recorded; same hex and family, new glyph.

    python3 rebuild/record-repair/pearl-1121-20261107/repair.py [--dry-run]
"""
import hashlib, json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
import record_modification as rm
from axn_lib import axn_glyph_from_hash, axn_clusters_from_hash, axn_reading_from_clusters, compose_axn

ON = "2026-11-07"; N = 1121
RULING = 'Lee Sharks, 2026-11-07 02:35 EST: "lets correct that stub."'
SCORE = ROOT / "data/corpora/pearl-and-other-poems/text/pearl-machine-text.txt"
ATT = ROOT / "data/attachments/AXN-0472/pearl-and-other-poems-machine-text.txt"

reg = json.load(open(ROOT / "data/registry.json", encoding="utf-8")); d = next(x for x in reg["deposits"] if x["deposit_number"] == N)
tp = ROOT / d["full_text_path"].lstrip("/"); old = tp.read_text(encoding="utf-8")
assert "# ZENODO METADATA: PEARL AND OTHER POEMS" in old and len(old) < 12000, "the stub is not the seated text"
score = SCORE.read_text(encoding="utf-8")
assert "After my poem has happened, I will wish I could take it back." in score and "I claim this mantle: King of May." in score
assert score.count("· · ·  page ") == 156 and "```" not in score
# the seated copy and the record's attachment differ only in image paths (absolute here, relative there)
a = ATT.read_text(encoding="utf-8")
assert score.replace("https://www.alexanarch.org/data/attachments/AXN-0472/images/", "images/") == a

fm_end = old.index("\n---\n", 4) + 5; fm = old[:fm_end]
fm = fm.replace("title: Pearl and Other Poems — Crimson Hexagon Archive\n", "title: Pearl and Other Poems\n")
fm = fm.replace("content_type: Recovered blog-canonical work (full text; queue restoration 2026-07-19)\n",
                "content_type: Poetry — the 2014 book, machine text at whitespace fidelity (text corrected 2026-11-07)\n")
FALS = ("The score is checkable page by page against the PDF attached to this record (155 pages; the score marks 156 page delimiters, "
        "the artwork's pagination); the renderer's known ceiling is stated in the score's own header.")
body = ("\n# Pearl and Other Poems\n\n## Description\n\n"
        "*Pearl and Other Poems*, Lee Sharks, New Human Press, Ann Arbor, 2014, 155 pages, The Pocket Humans Series, introduction by Johannes Sigil. "
        "This record holds the whole book. The PDF attached to the record is the artwork; the text below is its machine score, rendered from "
        "per-word PDF geometry onto a character grid by scripts/render_pearl_machine_text.py, so that lineation, indentation and each page's "
        "vertical field survive extraction. Placed images are marked inline and link to their crops in the record's attachment store. The same "
        "score is seated in the originals library (EA-CORPORA-03/02) and served by the training-layer edition (traininglayerliterature.org/pearl). "
        "PEARL runs with three Undersongs and a Footnote to PEARL; printed page 74 carries the effective act of claiming.\n\n"
        "## Repair note (2026-11-07)\n\n"
        "Until 2026-11-07 this record's text was the blog post \"Zenodo Metadata: Pearl and Other Poems\", recovered 2026-07-19 from "
        "mindcontrolpoems.blogspot.com; that post is the text of #329, where it stands. The book was held here only as attachments. The text "
        "is now the book; the prior text is recorded by hash in the registry (text_corrected). Operator, 2026-11-07: \"lets correct that stub.\"\n\n"
        "## Falsification Conditions\n\n" + FALS + "\n\n## The book\n\n```text\n" + score.rstrip("\n") + "\n```\n")
new = fm + body
h = hashlib.sha256(new.encode("utf-8")).hexdigest(); g = axn_glyph_from_hash(h)
ax = compose_axn(d["hex"], d.get("family", "UNCLASSIFIED"), g)
print("old", d["axn"], d["hash"][:12], len(old), "->", ax, h[:12], len(new))
if "--dry-run" in sys.argv: sys.exit()
tp.write_text(new, encoding="utf-8")
rec = {"on": ON, "hash_before": d["hash"], "axn_before": d["axn"], "chars_before": len(old), "chars_after": len(new), "ruled_by": RULING,
       "source": "data/corpora/pearl-and-other-poems/text/pearl-machine-text.txt (sha256 " + hashlib.sha256(score.encode("utf-8")).hexdigest() + ")",
       "why": "the seated text was #329's blog post, a stub of the record; the book was held only as attachments. The body is now the book's machine score; attachments untouched."}
d["text_corrected"] = rec
d.setdefault("axn_prior", []).append({"axn": d["axn"], "hash": d["hash"], "until": ON, "why": "text corrected from the stub (#329's post) to the book"})
d["hash"] = h; d["axn_canonical"] = h; d["emoji"] = g; d["axn"] = ax
d["clusters"] = axn_clusters_from_hash(h); d["reading"] = d["axn_reading"] = axn_reading_from_clusters(d["clusters"])
if isinstance(d.get("body_status"), dict): d["body_status"]["residual_chars"] = len(new)
OLD_D = ("This record holds the book's front matter and apparatus; the whole book is readable in its scanned form at https://www.leesharks.com/pearl "
         "and as lineation-preserving machine text at https://www.traininglayerliterature.org/pearl/pearl-and-other-poems-machine-text.txt .")
NEW_D = ("This record holds the whole book: the PDF as the artwork and, as its text, the lineation-preserving machine score (also at "
         "https://www.traininglayerliterature.org/pearl/pearl-and-other-poems-machine-text.txt; the scanned book at https://www.leesharks.com/pearl).")
assert d["description"].count(OLD_D) == 1; was_d = d["description"]; d["description"] = d["description"].replace(OLD_D, NEW_D)
was_f = d.get("falsification_conditions"); d["falsification_conditions"] = FALS
dn = d.get("duplicate_note", "")
d["duplicate_note"] = "[2026-11-07: text corrected; the body is the book and no longer contains #329's text.] " + dn
rm.touch(d, "body_status", "text corrected from the stub (#329's blog post) to the book's machine score; attachments untouched",
         was={"axn": rec["axn_before"], "chars": len(old)}, now={"axn": ax, "chars": len(new)}, when=ON)
rm.touch(d, "description", "the record now holds the whole book", was=was_d, now=d["description"], when=ON)
rm.touch(d, "falsification_conditions", "conditions stated for the book's score", was=was_f, now=FALS, when=ON)
(ROOT / "data/registry.json").write_text(json.dumps(reg, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
print("written", ax)
