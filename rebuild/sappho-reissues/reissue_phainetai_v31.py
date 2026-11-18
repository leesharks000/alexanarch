#!/usr/bin/env python3
"""#1785 ΦΑΙΝΕΤΑΙ ΜΟΙ reissued in place v3.0 -> v3.1 (2026-11-18). The author, 13:40: "lets address these small items and version";
earlier, "seating includes landing. lets go ahead and version or deposit". Date and position kept; hash and AXN re-derived at the
same position and family; the prior hash, AXN and title kept in reissue_history.
    python3 rebuild/sappho-reissues/reissue_phainetai_v31.py <PHAINETAI-MOI-v3.1.md>"""
import json, hashlib, pathlib, sys, re
ROOT = pathlib.Path(__file__).resolve().parents[2]; sys.path.insert(0, str(ROOT / "scripts")); import axn_lib as AX
SRC = pathlib.Path(sys.argv[1])
R = json.loads((ROOT / "data/registry.json").read_text(encoding="utf-8")); D = {x["deposit_number"]: x for x in R["deposits"]}
WORD = 'Lee Sharks, 2026-11-18, 13:40: "lets address these small items and version".'
def rep(s, a, b, n=1):
    assert s.count(a) == n, (a[:90], s.count(a)); return s.replace(a, b)
d = D[1785]; assert d["version"] == "v3.0", d["version"]
OLD_T = d["title"]; NEW_T = "ΦΑΙΝΕΤΑΙ ΜΟΙ: Sappho 31 and the Inscription of the Future Reader (v3.1)"
KW_SWAP = {"fragment 1": "poem 1", "fragment 16": "poem 16", "fragment 147": "Svenbro", "cletic hymn": "summoning", "beside the point": "exchange of bodies"}
CHANGES = ("Poems, not fragments: poems 1 and 31 so called, the Voigt numbers kept as addresses and 'Sappho fragment 31' kept as a retrieval keyword (§V.5a); "
    "poem 1 as a summoning spell, and the effective act at the head, 'I, Lee Sharks, do hereby summon Sappho.'; the edge counted as three words, ἐπεὶ †καὶ πένητα†, "
    "with three readings of the cut, Longinus completing and extending the socket held as the stronger reading and the attribution not a falsifier (§§V.1a, V.5a); "
    "the archive's Sappho corpus swept and its findings taken in; the poem read whole, as a preview after the abstract and in full at §VI.1; the voice without a body "
    "as sacrifice and erotic approach, an investment of substance in the medium, with magical parallels as an open seam; ποίας and ποιέω; Svenbro's Phrasikleia ch. 8 "
    "read whole and distinguished in seven places, the first on what the reader undergoes; the reader as the site where the invested substance rematerializes, which is "
    "why the dare, why the reader must choose, and what Catullus does; the eroticism as an exchange of bodies; Antiphanes' Sappho in §IV.8; Philo not cited for poem 31; "
    "at a reader's report: §I.2's closing sentence, Longinus as the transmitter whose quotation preserves the poem, §IV.9's first parting; "
    "at the author's answer to an AI Overview stress test: the reader in two stages, hearing in the seat, passive as the gods, and speaking the voice, undone in turn and investing it again, the reader becoming the poet, "
    "and the eros three ways through the voice, the poet to her voice, the voice to the reader, the reader to the voice (§§II.3, IV.7, IV.9, V.2a, VI, VI.1, VII.6); "
    "the sheet more χλωρός than grass in both senses, dead and greener for holding her life as word, with grass as a standing figure (Iliad 6.146, LXX Isaiah 40:6–8, Whitman 1855) (§IV.4); "
    "Herodotus 2.178 (§IV.6); supplement and inference distinguished (§VII.4); the treatise's second person granted as habit (§V.1a).")

fp = ROOT / d["full_text_path"].lstrip("/"); cur = fp.read_text(encoding="utf-8")
fm = cur[:cur.index("\n---\n", 4) + 5]
fm = rep(fm, f'title: "{OLD_T}"', f'title: "{NEW_T}"')
vl = [l for l in fm.split("\n") if l.startswith("version: ")]; assert len(vl) == 1; fm = rep(fm, vl[0], 'version: "v3.1"')
for a, b in KW_SWAP.items(): fm = rep(fm, f"\n  - {a}\n", f"\n  - {b}\n")
sl = [l for l in fm.split("\n") if l.startswith("substrate: ")]; assert len(sl) == 1
SUB_OLD, SUB_NEW = "- **v2.1–3.0** were revised in session on 16–18 November 2026", "- **v2.1–3.1** were revised in session on 16–18 November 2026"
SUB_ADD = (" In v3.1: poem, not fragment, \"the editorial device eclipses the poem\"; poem 1 as a summoning spell, and \"I, Lee Sharks, do hereby summon Sappho.\"; "
    "the edge as three words, and Longinus \"both completing and extending the socket\", the stronger reading and \"not a falsifying condition\"; the full embodied reading; "
    "the voice without body as \"a sacrifice, a self dissolution, and *also* an erotic approach\", \"an *investment* of substance in the medium\"; the reader as \"the site where "
    "sappho's invested substance rematerializes\", \"thats why the dare, thats why the reader must choose, and thats what catullus does\"; \"that is also the eroticism: it is an "
    "exchange of bodies\". Svenbro's chapter was read in a public copy and is cited, not seated or reproduced.")
new_sl = rep(sl[0], SUB_OLD, SUB_NEW); assert new_sl.endswith('"'); new_sl = new_sl[:-1] + SUB_ADD.replace('"', '\\"') + '"'
fm = rep(fm, sl[0], new_sl)
d["substrate"] = rep(d["substrate"], SUB_OLD, SUB_NEW).rstrip() + SUB_ADD

s = fm + "\n# " + NEW_T + "\n\n" + SRC.read_text(encoding="utf-8")
h = hashlib.sha256(s.encode("utf-8")).hexdigest(); g = AX.axn_glyph_from_hash(h); cl = AX.axn_clusters_from_hash(h)
d.setdefault("reissue_history", []).append({"date": "2026-11-18", "from_version": "v3.0", "to_version": "v3.1", "hash_before_reissue": d["hash"],
    "axn_before_reissue": d["axn"], "title_before_reissue": OLD_T, "reason": WORD, "changes": CHANGES})
prior = d["axn"]
d.update({"title": NEW_T, "version": "v3.1", "hash": h, "axn_canonical": h, "emoji": g, "axn": AX.compose_axn(d["hex"], d["family"], g),
          "clusters": cl, "axn_reading": AX.axn_reading_from_clusters(cl), "full_text_chars": len(s)})
d["keywords"] = [KW_SWAP.get(k, k) for k in d["keywords"]]
for e in d.get("entities", []):
    for k in ("subject", "object"):
        if e.get(k) == OLD_T: e[k] = NEW_T

# description
de = d["description"]
de = rep(de, "A reading of Sappho fragment 31", "A reading of Sappho 31")
de = rep(de, "at τόλματον or through the six words assigned to Longinus (§V.5a)", "at τόλματον or through the three words, ἐπεὶ †καὶ πένητα†, assigned to Longinus (§V.5a)")
AB = " […abridged for the catalogue; full description in this deposit's record]"
de = rep(de, AB, "\n- Version 3.1 (in place): poems, not fragments; poem 1 as a summoning, and the effective act at the head; the edge as three words with three readings of the cut, the Longinian held as stronger, not as a falsifier; the poem read whole; Svenbro read whole and distinguished: the reader as the site where the invested substance rematerializes, and the poem's eroticism as an exchange of bodies (§IV.9)." + AB)
d["description"] = de
# falsification: the attribution of the edge is no longer a falsifier (v3.1, the author: "not a falsifying condition")
fc = d["falsification_conditions"]
fc = rep(fc, " The conjecture of §V.1a fails on a witness to the poem independent of Longinus that carries verse past τόλματον, or on a reading of the transmitted words as Sapphic verse without emendation.", "")
fc = rep(fc, "if fragment 1's goddess", "if poem 1's goddess"); fc = rep(fc, "if fragment 1's receivers take up a body as fragment 31's do", "if poem 1's receivers take up a body as poem 31's do")
d["falsification_conditions"] = fc
d["methodology"] = d["methodology"].rstrip() + (" For v3.1: the archive's Sappho corpus read through by parallel readers with provenance; Svenbro's Phrasikleia (1988) ch. 8 read whole in a public copy, "
    "cited and not seated; Iliad 6.146, LXX Isaiah 40:6–8, Herodotus 2.178 and Whitman's Leaves of Grass (1855) read in the archive's seats; Catullus 51 read in the Vivien 1903 seat; Antiphanes' Sappho (fr. 196 Kock, Athenaeus 10.450e–451b) read in the archive's seat of Kaibel's Athenaeus.")
# wiki
w = d["wiki_article"]
w = rep(w, "is an article by Lee Sharks on Sappho's fragment 31, deposited on 18 November 2026 as version 3.0", "is an article by Lee Sharks on Sappho's poem 31, deposited on 18 November 2026 as version 3.0, revised in place the same day as version 3.1,")
w = w.rstrip() + (" Version 3.1, revised in place, calls poems 1 and 31 poems, not fragments: neither was received as a fragment, and the editorial label eclipses the poem. "
    "It reads poem 1 as a summoning spell, which calls Aphrodite to embodied presence, and opens with an effective act: 'I, Lee Sharks, do hereby summon Sappho.' "
    "It counts the edge as three words, ἐπεὶ †καὶ πένητα†, gives three readings of the cut, and holds as the stronger the reading on which Longinus, the transmitter whose "
    "quotation preserves the poem, both completes and extends the opening, without making the attribution a condition of the argument. It gives a preview reading of the "
    "poem after the abstract and a full embodied reading once the argument is built: the speaker imagines the life of a voice without a body, a sacrifice and an erotic "
    "approach at once, an investment of substance in the medium. It reads Jesper Svenbro's 'Death by Writing' (Phrasikleia, 1988) whole, credits him with the reader's seat, "
    "its renewal and the breath the reader returns to the poem, and parts from him in seven places, first on what the reader undergoes: on this reading the reader is the "
    "site where the substance Sappho invested rematerializes, which is why the poem ends in a dare the reader must choose, and what Catullus does in poem 51. The poem's "
    "eroticism is then an exchange of bodies, hers given into the medium and the reader's lent to her. The reader passes through two stages: in the seat the one who "
    "hears is passive, like the gods, while the one whom desire for the voice leads to speak it is undone in turn and must invest the substance again, and so becomes the "
    "poet. The eros runs three ways through the voice: the poet is struck by her own voice, the voice wants the reader's body, to possess and invest it, and the reader "
    "wants the voice. The version reads the dried sheet as more χλωρός than grass in both senses, pale and dead and greener than the living plant because it holds her "
    "life as word, and sets grass as a standing figure for flesh against what lasts, from Glaukos's leaves in the Iliad and Isaiah's 'all flesh is grass' to Whitman's "
    "'beautiful uncut hair of graves'.")
d["wiki_article"] = w

fp.write_text(s, encoding="utf-8")
dp = ROOT / f"data/deposits/AXN-{d['hex']}.md"
if dp.exists(): dp.write_text(s, encoding="utf-8")
(ROOT / "data/registry.json").write_text(json.dumps(R, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
json.dump({prior: d["axn"]}, open(pathlib.Path(__file__).parent / "axn-moves-20261118-phainetai-v31.json", "w"), ensure_ascii=False, indent=1)
print(1785, prior, "->", d["axn"])
