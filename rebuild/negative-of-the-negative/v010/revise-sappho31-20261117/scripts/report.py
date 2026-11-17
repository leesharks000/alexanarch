"""Write REPORT.md from the staged row, ledgers and verification.   /tmp/py312/python3 report.py"""
import json, collections
from vlib import *
R = json.loads((STAGE / "row.json").read_text()); V = json.loads((STAGE / "verification.json").read_text())
A = json.loads((STAGE / "ledger-archive.json").read_text()); F = json.loads((STAGE / "field.json").read_text())
L = json.loads(LIVE_ROW.read_text()); A0 = json.loads((LIVE_LEDGERS / "ledger-archive.json").read_text())
deps0 = sorted({c["dep"] for c in A0}); deps1 = sorted({c["dep"] for c in A if c["dep"] != "capture-registry"})
cnt_new = collections.Counter(str(c["dep"]) for c in A if c["id"] not in {x["id"] for x in A0})
comp = R["composition"]["revision_20261117"]
ko = R["objects"]["KO"]["sentences"]
L_ = []
w = L_.append
w("# REPORT — revision in place of the /non row for Sappho 31 (2026-11-17)\n")
w("Brief: rebuild/negative-of-the-negative/v010/BRIEF-REVISE-ROW-SAPPHO-31.md. Stage: " + comp["stage"] + ". Nothing outside the stage was edited.\n")
w("## Outputs\n")
w("- `row.json` (shape of the live row, field by field; v0.10 fields added as the CRJ row shows them: `kernel_T`, `homonyms`, `notes`, `composition`, `field_by_origin`, `links`; `objects.T.words_note` and `transcripts`; `objects.KO.joins`, `plan`, `governing_question`, a `sense` on every KO sentence; `objects.P.body_words` and `body_words_rule`; `objects.P_B.body_words`; `ontology.composition_note`; `spec` = EA-NEGONT-02 v0.10, #1726).")
w("- `field.json`, `ledger-archive.json` (every quote verified by `scripts/verify.py`; counts in `verification.json`).")
w("- `sources/` (B1–B5 refetched as text, `fetch-records.json`), `traversal/` (D/R/O rerun and `reading-20261117.json`), `capture-checks.json`, `config-sappho-31.json` (the row's config, unchanged), `scripts/`.")
w(f"- Prior row sha256: `{comp['prior_row_sha256']}` (matches `non/sappho-31/entity.json` row_sha256). The AXN (AXN:0717.NON) stays the row's identity; the session records the prior hash in `earlier_versions`.\n")
w("## Verification\n")
w(f"- Field: {V['field_total']} (B1 29, B2 6, B3 2, B4 7, B5 4 against the pages refetched 2026-11-17 as saved text; B6 1 against the paste).")
w(f"- Archive: {V['archive_total']}. The one failure is A436-01 (see findings). New claims 104/104; the 153 other old claims verified.")
w(f"- KO {V['ko_sentences']} sentences; plan matches text: {V['plan_matches_text']}; unknown claim ids: none; kernels off the rail: none; ledger claims not in the KO: {', '.join(V['ledger_claims_not_in_KO'])} (A436-01 is carried on the rail, marked; the KO cites A1048-03 in its place).")
w(f"- Measure (§4.10): KO_B sentences surviving at ≥0.95: {V['measure']['v0.10']['surviving']} of {V['measure']['v0.10']['of']} (v0.9: 0 of 9). Opening run: no breach. Blocks: sequence `{V['measure']['blocks']['sequence']}`, field-only head 0, archive-only tail {V['measure']['blocks']['archive_only_tail']} (v0.9: 3): breach recorded in `status.breaches` (the closing sense, 'Its composition by machines', grows by the receptions added in date order).")
w(f"- P body: {R['objects']['P']['body_words']} words (bound 350; v0.9 348). The new compression material went to the open block, outside the bound.\n")
w("## Panel fields that change (for the session to seat)\n")
w("- `stage`: 'recomposed 2026-10-18 under EA-NEGONT-02 v0.9, #1690, equal case (draft, not frozen; ledgers unaudited); revised in place 2026-11-17 under EA-NEGONT-02 v0.10, #1726 (#1781, #1752, #1756, #1774, #1783 and sixteen captures admitted; draft, not frozen; ledgers unaudited)'.")
w("- `ontology`: unchanged — composition `equal`, E_F `C (public entity: a work)`, rho `extends`. The case and ρ were re-read at the new loci and kept (row `ontology.case.revision_20261117`, `ontology.rho.revision_20261117`). `E_A` may carry the revised definition's head (row `ontology.E_A.definition_revision_20261117`): the reading's current text #1781.")
w("- New, as v0.10 entries carry them: `homonym_names`: [] ; `homonym_basis`: the row's `homonyms.basis`.")
w("- `links` (row): `combined_audit` https://www.machinemediation.org/combined-audit/ and `classical_philology` /non/classical-philology/ — build_non.py must carry them.")
w("- `type`, `name`, `addresses`: unchanged.\n")
w("## Counts by pool, before → after\n")
w("| Pool | Before | After |\n|---|---|---|")
w("| B_D sources | 6 (B1–B6) | 6 (B1–B6; pools now marked) |")
w("| B_D claims | 49 | 49 (none added, changed or removed; all verified against saved text) |")
w("| B_R | — (no pools) | 0 (not extended: the brief names no reference source) |")
w(f"| Archive claims | {len(A0)} | {len(A)} (+{len(A)-len(A0)}) |")
w(f"| Archive deposits | {len(deps0)} | {len(deps1)} (+{len(set(deps1)-set(deps0))}: {', '.join('#'+str(d) for d in sorted(set(deps1)-set(deps0)))}) |")
w("| Capture Registry (CAP-) | 0 | 37 claims from 16 captures (CAP-1–CAP-16) |")
w(f"| KO sentences | {len(L['objects']['KO']['sentences'])} | {len(ko)} |")
w(f"| P open items | {len(L['objects']['P']['open'])} | {len(R['objects']['P']['open'])} |")
w(f"| P rail cards | {len(L['objects']['P']['rail'])} | {len(R['objects']['P']['rail'])} |\n")
w("New archive claims by source: " + ", ".join(f"{k if k=='capture-registry' else '#'+k} {v}" for k, v in sorted(cnt_new.items(), key=lambda x: -x[1])) + ".\n")
w("## Every change to the KO\n")
w("The 38 v0.9 sentences are kept in their order, their prose as composed (§4.5: rows composed under v0.9 stand as composed), except two edits. Each sentence now carries a `sense` (§4.12) and its v0.9 number (`v09_n`); added sentences carry `added: 2026-11-17`. Renumbering follows from the insertions.\n")
for ch in comp["ko_changes"]:
    if ch["change"] == "edited":
        w(f"- Edited: v0.9 sentence {ch['old_n']} → {ch['new_n']}. {ch['reason']}. Claims added {ch.get('claims_added', [])}, removed {ch.get('claims_removed', [])}.")
w("- Kept unchanged (v0.9 → new number): " + "; ".join(f"{c['old_n']}→{c['new_n']}" for c in comp["ko_changes"] if c["change"] == "kept") + ".")
w(f"- Added ({len(comp['ko_added'])}):")
for a in comp["ko_added"]:
    w(f"  - {a['new_n']} ({a['sense']}): {', '.join(a['claims'])}")
w("- New senses: 'The two readings on one scale' (42–46) and 'The decline, and where the decision is made' (47–51); the v0.9 paragraph 4 is now headed 'Readings, and the making of the jealousy reading' and 'The future-reader reading'; the other headings name the v0.9 paragraphs.\n")
w("## Capture-record findings the ledger shows wrong (report only)\n")
w("- None found. The archive quotations inside the admitted findings were checked against the deposits they name (13 quotations in six findings, and the three absence claims of sappho-future-reader-framework-aio-20261030 findings[1] against #134, #281, #1270, #1054, #1548, #1645, #1646): all hold (`capture-checks.json`). The field ledger (B1–B6) bears on no admitted finding.")
w("- Reported, on the archive's own quotation of a capture (not a capture-record finding): #1781 §VII.5 quotes the v2.5 capture's 'The latter is more comprehensive.' where the transcript continues ', but it must earn that comprehensiveness …', and 'He is challenging the legitimacy of continuing to treat the jealousy interpretation as the default.' where the transcript continues 'once a more coherent account of the poem's construction …'. #1781 n. 37's transcript sha256 2685a3e6… matches the registry's `transcript_raw` of phainetai-v27-arguments-chatgpt-20261116.")
w("- Reported, a ledger defect (not a capture record): A436-01's quote ('Future citations of Cranes's reconstruction should prefer the stable formulation …') is not in #436's text as it now stands (AXN-00FB, re-seated 2026-10-19, after the row's extraction of 2026-10-07); it is found verbatim in #1048 (AXN-0424) and carried as A1048-03, which the KO cites. A436-01 is kept with quote_ok false and a note.\n")
w("## Other notes for the session\n")
w("- The decision letter in #1774's record names the journal's editor; the name stands in the ledger quote (A1774-01) and is not composed in the KO, whose object is the poem. No reader of the report is named.")
w("- The operator's statement of the stake (2026-11-17) is in `notes` and `KO.governing_question`, not quoted in the article.")
w("- Captures read and not admitted (bearing on the Sappho Room, the phrase 'Sappho, Mother of the Logos', or the Revelation First address): listed with reasons in `traversal/reading-20261117.json`.")
w("- D/R/O rerun (row config unchanged, O-class not run, no hop): D 1832/266, R 433/153, O 803/223; of the deposits new to the pass, 12 admitted at loci (five named by the brief, #1779, #1749, #1748, #1058, #1670, #1766, and #1048 for A1048-03), 30 read and not admitted, with reasons.")
w("- Disk: under 35 MB free during the run; the raw HTML of the refetched pages was not kept (sha256 recorded).\n")
w("## The knowledge object, as plain prose\n")
w("Sappho 31\n")
prev = None
for s in ko:
    if s["sense"] != prev:
        w("\n" + s["sense"] + "\n"); prev = s["sense"]
    w(s["text"])
(STAGE / "REPORT.md").write_text("\n".join(L_) + "\n", encoding="utf-8")
print("ok", len("\n".join(L_)))
