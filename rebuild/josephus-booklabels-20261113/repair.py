"""Repair of 2026-11-13: in seat 01/01 (Josephus, #1499) the last section of every book of the War, the Antiquities and Against Apion
was labelled with the next book's number and carried the next book's heading at its end (26 lines). Found in the census for EA-LOGOS-01
v2.3 (Appendix IV §8). Each line is relabelled with its own book; the heading, which belongs to the next book's head and not to the
section, is removed from the line and kept verbatim in source.json errata. The manifest is rebuilt and the seat's AXN re-derived, the
prior kept in axn_prior. Ruling of 2026-11-12: the repair travels with the version of the paper that carries the census.
    python3 rebuild/josephus-booklabels-20261113/repair.py
"""
import hashlib, json, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parents[2]; sys.path.insert(0, str(ROOT / "scripts"))
from axn_lib import axn_glyph_from_hash
SEAT = ROOT / "data/corpora/josephus"
HEAD = re.compile(r"\s*(Φλα[υΐ]ί?ου Ἰωσήπου .*|Τάδε ἔνεστιν ἐν τῇ .*)$")
moved = []
for w in ("BJ", "AJ", "CA"):
    p = SEAT / f"text/{w}.txt"; L = p.read_text(encoding="utf-8").split("\n"); prev = None
    for i, l in enumerate(L):
        m = re.match(r"(\w+) (\d+)\.(\d+)\t(.*)", l)
        if not m: continue
        b, s, t = int(m.group(2)), int(m.group(3)), m.group(4)
        if prev and b != prev[0] and s != 1:
            assert s == prev[1] + 1, (w, i, b, s, prev)
            h = HEAD.search(t); assert h, (w, i)
            L[i] = f"{w} {prev[0]}.{s}\t{t[:h.start()].rstrip()}"
            moved.append({"work": w, "line": i + 1, "was": f"{w} {b}.{s}", "now": f"{w} {prev[0]}.{s}", "heading_removed": h.group(1).strip()})
            prev = (prev[0], s); continue
        prev = (b, s)
    p.write_text("\n".join(L), encoding="utf-8")
assert len(moved) == 26, len(moved)
# manifest
man = SEAT / "MANIFEST.sha256"; old_man = hashlib.sha256(man.read_bytes()).hexdigest()
lines = man.read_text(encoding="utf-8").splitlines(); out = []
for ln in lines:
    h, path = ln.split(None, 1)
    fp = ROOT / path.strip()
    out.append(f"{hashlib.sha256(fp.read_bytes()).hexdigest()}  {path.strip()}" if fp.exists() else ln)
man.write_text("\n".join(out) + "\n", encoding="utf-8")
new_man = hashlib.sha256(man.read_bytes()).hexdigest()
src = json.loads((SEAT / "source.json").read_text(encoding="utf-8"))
old_axn = src["axn"]; new_axn = f"AXN:060E.ORIGINAL.{axn_glyph_from_hash(new_man)}"
assert old_man == src["axn_basis"]["sha256"]
src.setdefault("axn_prior", []).append({"axn": old_axn, "manifest_sha256": old_man, "until": "2026-11-13",
    "why": "book-end labels repaired in BJ, AJ and CA: 26 last sections had been labelled with the next book's number and carried its heading; relabelled, headings removed to errata. The text of each section is unchanged."})
src["axn"] = new_axn; src["axn_basis"]["sha256"] = new_man; src["axn_basis"]["assigned"] = "2026-11-13"
src.setdefault("errata", []).append({"date": "2026-11-13", "severity": "reference",
    "found": "The last section of every book of the War (6), the Antiquities (19) and Against Apion (1) was labelled with the next book's number (e.g. 'BJ 2.673' for War 1.673), and carried the next book's heading at its end. A search for a book's last section found nothing; a search for '2.673' found Book I.",
    "cause": "Book-boundary handling in normalization: the milestone of each book's last section was read after the next book's div had opened.",
    "repair": "Each line relabelled with its own book; the heading removed from the line and kept here. The text of the sections is unchanged.",
    "lines": moved, "found_in": "EA-LOGOS-01 v2.3, Appendix IV §8 (the census)", "raised_by": "Lee Sharks (ruling of 2026-11-12)"})
(SEAT / "source.json").write_text(json.dumps(src, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
for f in ("data/api/corpora.json", "datasets/corpora/corpora.json", "s/axn/060E/index.html"):
    fp = ROOT / f; t = fp.read_text(encoding="utf-8"); assert t.count(old_axn) >= 1, f; fp.write_text(t.replace(old_axn, new_axn), encoding="utf-8")
reg = json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8"))
recs = reg["deposits"]
d = next(x for x in recs if x.get("deposit_number") == 1499)
d.setdefault("errata", []).append({"date": "2026-11-13", "kind": "reference repair", "locus": "text/BJ.txt, text/AJ.txt, text/CA.txt (book ends)",
    "was": "26 book-final sections labelled with the next book's number and carrying the next book's heading (e.g. 'BJ 2.673' for War 1.673)",
    "now": f"each labelled with its own book; the headings removed from the lines and kept in source.json errata; the Greek of the sections is unchanged. The seat's AXN is re-derived from the new manifest: {new_axn}, prior {old_axn} (source.json axn_prior).",
    "reason": "Found in the census of the Slavonic and Greek War, EA-LOGOS-01 v2.3, Appendix IV §8.", "raised_by": "Lee Sharks (2026-11-12)", "status": "corrected in the seat"})
(ROOT / "data/registry.json").write_text(json.dumps(reg, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
print(old_axn, "->", new_axn)
