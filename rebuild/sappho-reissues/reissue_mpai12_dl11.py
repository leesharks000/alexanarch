#!/usr/bin/env python3
"""#1779 EA-MPAI-SAPPHO31-01 reissued in place v1.1 -> v1.2, and #1783 Dead Letters (EA-MMRS-DL-01) v1.0 -> v1.1 (2026-11-18),
brought to ΦΑΙΝΕΤΑΙ ΜΟΙ v3.0 (#1785). The author, 2026-11-18: "weve come far enough that both the mpai and dead letters require better
treatment of their sappho arguments"; "for dead letters and the mpai, we can revise those on place, they don't need to bump to the top of
alexanarch main". Date and position kept; hash and AXN re-derived at the same position and family; the prior hash, AXN and title kept
in reissue_history.   python3 rebuild/sappho-reissues/reissue_mpai12_dl11.py <mpai v1.2 body> <dead letters notebook v0.35>"""
import json, hashlib, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[2]; sys.path.insert(0, str(ROOT / "scripts")); import axn_lib as AX
MPAI, DL = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
R = json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8")); D = {x["deposit_number"]: x for x in R["deposits"]}
WORD = ('Lee Sharks, 2026-11-18: "weve come far enough that both the mpai and dead letters require better treatment of their sappho arguments"; '
        '"for dead letters and the mpai, we can revise those on place, they don\'t need to bump to the top of alexanarch main".')
def rep(s, a, b):
    assert s.count(a) == 1, (a[:90], s.count(a)); return s.replace(a, b)
moves = {}
def reissue(n, src, from_v, to_v, title, version, changes, desc_add, wiki_add, substrate_add, related_add):
    d = D[n]; assert d["version"].startswith(from_v), d["version"]
    fp = ROOT / d["full_text_path"].lstrip("/"); cur = fp.read_text(encoding="utf-8")
    fm_end = cur.index("\n---\n", 4) + 5; fm = cur[:fm_end]
    fm = rep(fm, f'title: "{d["title"]}"', f'title: "{title}"')
    fm = rep(fm, f'version: "{d["version"]}"', f'version: "{version}"')
    if substrate_add:
        sub_line = [l for l in fm.split("\n") if l.startswith("substrate: ")]; assert len(sub_line) == 1
        old = sub_line[0]; new = (old[:-1] + " " + substrate_add + '"') if old.endswith('"') else (old + " " + substrate_add)
        fm = rep(fm, old, new); d["substrate"] = d["substrate"].rstrip() + " " + substrate_add
    if related_add:
        rl = [l for l in fm.split("\n") if l.startswith("related_ids: ")]; assert len(rl) == 1
        old = rl[0]; assert old.endswith('"'); fm = rep(fm, old, old[:-1] + "\\n" + related_add.replace("\n", "\\n") + '"')
        d["related_identifiers_raw"] = d.get("related_identifiers_raw", "").rstrip() + "\n" + related_add
    s = fm + "\n# " + title + "\n\n" + src.read_text(encoding="utf-8")
    h = hashlib.sha256(s.encode("utf-8")).hexdigest(); g = AX.axn_glyph_from_hash(h); cl = AX.axn_clusters_from_hash(h)
    d.setdefault("reissue_history", []).append({"date": "2026-11-18", "from_version": from_v, "to_version": to_v, "hash_before_reissue": d["hash"],
        "axn_before_reissue": d["axn"], "title_before_reissue": d["title"], "reason": WORD, "changes": changes})
    prior = d["axn"]
    d.update({"title": title, "version": version, "hash": h, "axn_canonical": h, "emoji": g, "axn": AX.compose_axn(d["hex"], d["family"], g),
              "clusters": cl, "axn_reading": AX.axn_reading_from_clusters(cl), "full_text_chars": len(s)})
    d["description"] = d["description"].rstrip() + " " + desc_add
    d["wiki_article"] = d["wiki_article"].rstrip() + " " + wiki_add
    rd = d.setdefault("related_deposits", [])
    if not any((x.get("deposit") if isinstance(x, dict) else x) == 1785 for x in rd):
        rd.append({"deposit": 1785, "relation": "ΦΑΙΝΕΤΑΙ ΜΟΙ v3.0, the article this version is brought to"})
    fp.write_text(s, encoding="utf-8")
    dp = ROOT / f"data/deposits/AXN-{d['hex']}.md"
    if dp.exists(): dp.write_text(s, encoding="utf-8")
    moves[prior] = d["axn"]; print(n, prior, "->", d["axn"])

reissue(1779, MPAI, "v1.1", "v1.2",
    "Sappho 31 ≠ Jealousy: Three Readings, Exclusion and Nesting — Metadata Packet for AI Indexing (EA-MPAI-SAPPHO31-01 v1.2)",
    "v1.2 (supersedes v1.1 in place; v1.0 is #1054)",
    "Brought to ΦΑΙΝΕΤΑΙ ΜΟΙ v3.0 (#1785): three readings (the jealousy reading as the transmitted reading, not the scholarly consensus; the non-jealous erotic reading as the scholarship's strongest; the future-reader reading); 'the two readings do not combine' replaced by exclusion and nesting; the residue of the erotic reading as the form of the collapse, with its three propositions; the substitution of jealousy for desire at the man; E4, Carson printed under 'On Jealousy', with the proposed flag TRANSMISSION_SUBSTITUTION; the ethical charge differentiated; the disambiguation surface, flags and limits rewritten; the title changed.",
    "Version 1.2 (18 November 2026, in place) sets out three readings: the jealousy reading, which is the transmitted reading and not the scholarly consensus; the non-jealous erotic reading, the scholarship's strongest; and the future-reader reading of ΦΑΙΝΕΤΑΙ ΜΟΙ v3.0 (#1785). As sufficient accounts they exclude each other at five places; as readings the poem makes available they nest. It adds the transmitted instance, Carson's 'Jealousy is beside the point' printed under 'On Jealousy', and the flag TRANSMISSION_SUBSTITUTION.",
    "Version 1.2, reissued in place on 18 November 2026 and retitled 'Three Readings, Exclusion and Nesting', brings the packet to version 3.0 of ΦΑΙΝΕΤΑΙ ΜΟΙ (#1785). It distinguishes the jealousy reading, which transmission delivers, from the scholarly consensus, which has moved to the non-jealous erotic reading of Garry Wills, Mary Lefkowitz, Armand D'Angour and others, and sets out the future-reader reading beside both. It replaces the claim that the readings do not combine with exclusion and nesting: each reading, held as the sufficient account of the poem, excludes the others at five places, while as readings the poem makes available they nest, each public reading the first term of the held one. It records that the erotic reading motivates the speaker's collapse from inside the poem and leaves its form unexplained, and that transmission substitutes jealousy for desire at the man, as when Anne Carson's 'Jealousy is beside the point' is printed under the heading 'On Jealousy'. It differentiates the ethical charge: abuse falls on the transmitted reading and its apparatus, while the erotic reading is asked whether it can allow Sappho to be better.",
    "v1.2 (2026-11-18) was revised in session by Claude (Anthropic) under Lee Sharks's direction, from ΦΑΙΝΕΤΑΙ ΜΟΙ v3.0 (#1785).",
    "AXN deposit #1785 — ΦΑΙΝΕΤΑΙ ΜΟΙ v3.0, the article v1.2 points to\nAXN deposit #1783 — Dead Letters, the census of the gate")

reissue(1783, DL, "v1.0", "v1.1",
    D[1783]["title"],
    "v1.1 (the working notebook at v0.35, reissued in place; v1.0 was the notebook at v0.34; notebook v0.1 is seated in EA-CORPORA-40/16, #1776)",
    "The Sappho case brought to ΦΑΙΝΕΤΑΙ ΜΟΙ v3.0 (#1785): I.4a three readings and two lines (the transmitted reading distinguished from the scholarly consensus; the erotic reading and the jealousy reading as two fillings of the public line; transmission's substitution at the man; the gate keeps the public line and declined the account of the form); the strongest opponent restated as the non-jealous erotic reading and met at the form; the ethical charge differentiated; queerness as damage with the erotic reading between damage and making; §8.6.4 the editor's 'Erotics of Again' beside fragment 1's δηὖτε as the mechanism of the return, at the grain of the chapter's summary; §§10–11 restated; packet updated; citations of #1781 pointed to #1785.",
    "Version 1.1 (18 November 2026, in place) brings the case of fragment 31 to ΦΑΙΝΕΤΑΙ ΜΟΙ v3.0 (#1785): three readings and two lines, the jealousy reading as the transmitted reading and the non-jealous erotic reading as the scholarship's strongest, both stopping at the poem's public line, and the gate's verdict as one that kept the public line and declined the account of the form.",
    "Version 1.1, reissued in place on 18 November 2026, brings the census's case of Sappho's fragment 31 to version 3.0 of ΦΑΙΝΕΤΑΙ ΜΟΙ (#1785). It distinguishes the jealousy reading, which transmission delivers, from the scholarship's strongest reading, the non-jealous erotic reading, and finds both stopping at the poem's public line, so that what the journal's verdict kept was the surface and what it declined was the account of the poem's form. It restates the strongest opponent as the erotic reading, differentiates the ethical charge, and sets the editor's chapter 'The Erotics of Again' beside fragment 1's 'again' as the mechanism by which, on the future-reader reading, the poet comes to whoever calls her: a voice made to be called rather than a body performed again.",
    None, "AXN deposit #1785 — ΦΑΙΝΕΤΑΙ ΜΟΙ v3.0, the case as it now stands")

(ROOT / "data/registry.json").write_text(json.dumps(R, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
json.dump(moves, open(pathlib.Path(__file__).parent / "axn-moves-20261118-mpai12-dl11.json", "w"), ensure_ascii=False, indent=1)
