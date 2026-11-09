#!/usr/bin/env python3
"""repair_636_1484_20261109.py — #636 Space Ark ARCHON: its Part II chapter slots and its citations of the separately deposited Greek text made
clickable links to #638; #1484 the Ω erratum: a mislabelled citation date and a mislabelled verb form corrected.

Repair scope as ruled 2026-10-15: broken, missing and mislabelled files and citations; standard, the text as published.

#636. Part II of the text as published holds 22 placeholders ("[INSERT REVELATION CHAPTER 1 — STEPHANUS 1550]", "[INSERT CHAPTER 2]" …), present
since the first seating, and states that the Greek "has been deposited separately as *The Apocalypse of Sharks*", cited four times at DOI
10.5281/zenodo.19476949, severed at the 2026-06-19 termination. The DOI resolution index already maps that DOI to #638 (EA-ARK-SHARKS-01,
2026-04-08, same day). Ruled 2026-11-09 (the author's answer: "Link to #638"): the text keeps its words; each placeholder becomes a link to its
chapter on #638's page, and each citation of the DOI carries a link to #638. Not changed, and recorded in the registry: #636 declares Stephanus
1550; #638 seats the Textus Receptus of 1894.

#1484. Note 13 dates D'Angour's article "CQ 56 (2026)"; note 8 cites the same article as "CQ 56 (2006)", its year. And §I calls ζώοι, in μολπὰ
γράμμασι ζώοι, an aorist optative: it is a present optative (ζώω, the epic and Ionic present of "live"). Ruled 2026-11-09 ("Correct in #1484
only"): both corrected in #1484; #436 and #576, which carry the same label, stand as published.

Each record rehashed with a new AXN at the same hex and family; axn_prior and modifications record the change.
    python3 scripts/repair_636_1484_20261109.py [--apply]"""
import hashlib, json, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import record_modification as rm
from axn_lib import axn_glyph_from_hash, axn_clusters_from_hash, axn_reading_from_clusters, compose_axn

ON = "2026-11-09"
REC638 = "https://www.alexanarch.org/s/records/638/"
ANCH = ("α β γ δ ε στ ζ η θ ι ια ιβ ιγ ιδ ιε ιστ ιζ ιη ιθ κ κα κβ").split()
DOI = "(DOI: 10.5281/zenodo.19476949)"
DOI_NEW = f"(DOI: 10.5281/zenodo.19476949; [#638]({REC638}))"


def fix_636(t):
    n = 0
    def slot(m):
        nonlocal n
        k = int(m.group(2)); n += 1
        return f"**[{m.group(1)}]({REC638}#κεφάλαιον-{ANCH[k-1]}-chapter-{k})**"
    t2 = re.sub(r"\*\*(\[INSERT (?:REVELATION )?CHAPTER (\d+)(?: — STEPHANUS 1550)?\])\*\*", slot, t)
    assert n == 22, n
    c = t2.count(DOI); assert c == 4, c
    return t2.replace(DOI, DOI_NEW)


def fix_1484(t):
    a, b = "D'Angour, CQ 56 (2026)", "D'Angour, CQ 56 (2006)"
    assert t.count(a) == 1 and t.count("D'Angour, CQ 56 (2006)") == 1
    t = t.replace(a, b)
    a, b = "closing on an aorist optative, μολπὰ γράμμασι ζώοι", "closing on a present optative, μολπὰ γράμμασι ζώοι"
    assert t.count(a) == 1 and t.count("aorist optative") == 1
    return t.replace(a, b)


JOBS = {636: ("01EC", fix_636,
              "Part II's 22 chapter placeholders made links to their chapters on #638 (The Apocalypse of Sharks), and the four citations of DOI "
              "10.5281/zenodo.19476949 given a link to #638; the text's words unchanged",
              {"slots_linked": 22, "doi_citations_linked": 4, "target": REC638,
               "edition_note": "#636 declares Stephanus 1550; #638 seats the Textus Receptus of 1894. Recorded, not changed.",
               "ruled_by": "Lee Sharks, 2026-11-09, at the question on #636's Part II: 'Link to #638 (Recommended)'"}),
        1484: ("05FF", fix_1484,
               "note 13's date for D'Angour, CQ 56, corrected from (2026) to (2006), as note 8 has it; §I's 'aorist optative' for ζώοι corrected to "
               "'present optative'",
               {"citation": "D'Angour, CQ 56: (2026) → (2006), note 13", "verb_form": "ζώοι: aorist optative → present optative, §I",
                "not_changed": "#436 and #576 carry the same verb-form label and stand as published",
                "ruled_by": "Lee Sharks, 2026-11-09: 'yes, lets repair 636 and 1484'; at the question on ζώοι: 'Correct in #1484 only'"})}

reg_p = ROOT / "data/registry.json"; reg = json.loads(reg_p.read_text(encoding="utf-8"))
out = {}
for n, (hx, fx, note, detail) in JOBS.items():
    tp = ROOT / f"data/texts/AXN-{hx}-text.md"; dp = ROOT / f"data/deposits/AXN-{hx}.md"
    t = tp.read_text(encoding="utf-8"); new = fx(t)
    dnew = fx(dp.read_text(encoding="utf-8")) if dp.exists() else None
    out[n] = (tp, dp, new, dnew)
    print(n, "text", len(t), "→", len(new), "| deposit copy", "repaired" if dnew else "absent")
if "--apply" in sys.argv:
    for n, (hx, fx, note, detail) in JOBS.items():
        tp, dp, new, dnew = out[n]
        tp.write_text(new, encoding="utf-8")
        if dnew is not None: dp.write_text(dnew, encoding="utf-8")
        x = next(r for r in reg["deposits"] if r["deposit_number"] in (n, str(n)))
        h = hashlib.sha256(new.encode("utf-8")).hexdigest(); g = axn_glyph_from_hash(h)
        before = {"axn": x["axn"], "hash": x["hash"]}
        x.setdefault("axn_prior", []).append({"axn": x["axn"], "hash": x["hash"], "until": ON, "why": note + " (repair_636_1484_20261109.py)"})
        x["hash"] = h; x["axn_canonical"] = h; x["emoji"] = g
        x["axn"] = compose_axn(x["hex"], x.get("family", "ARCHIVAL"), g)
        x["clusters"] = axn_clusters_from_hash(h); x["reading"] = axn_reading_from_clusters(x["clusters"]); x["axn_reading"] = x["reading"]
        x["full_text_chars"] = len(new)
        x["citation_repaired_20261109"] = {"on": ON, **detail, "hash_before": before["hash"], "axn_before": before["axn"]}
        rm.touch(x, "axn", note, was=before["axn"], now=x["axn"], when=ON)
        print("applied", n, x["axn"])
    reg_p.write_text(json.dumps(reg, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")  # the registry's compact form, as it stands
