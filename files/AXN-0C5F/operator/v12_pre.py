# v1.2 of the framework holograms, executed inside each builder before record_nodes (2026-11-10). At the author's word of 20:48: "lets address, deposit,
# and turn to incorporating it into rev first and versioning all four holographic frames... also - if the framed themselves have not yet been spxi
# treated, they need to be". The records search of 2026-11-10 (rebuild/hk-frameworks/v12-staging) enters: evidence records as a new stratum, the Philo
# piece deposited as #1758 (In the Midst of the Seven) among them; related work, history, joins and flags carried in the kernel (v12_post.py).
# Rule of the search (18:45): additive; nothing already in a kernel is removed.
import json as _json, pathlib as _pl
V12_STAGE = _json.loads((K.ROOT / "rebuild/hk-frameworks/v12-staging" / f"{K.ID}.json").read_text(encoding="utf-8"))
V12_PHILO = 1758
V12_BODIES = {
 "EA-HK-REVFIRST-01": {1415: ("G", []), 1418: ("G", []), 1502: ("C", []), 1509: ("D", []), 1499: ("H", []), 1698: ("R", []), 1758: ("G", ["C", "R"])},
 "EA-HK-TENTHMUSE-01": {503: ("T", []), 134: ("I", []), 1458: ("T", ["I"]), 496: ("T", []), 1477: ("T", []), 1051: ("P", []), 1052: ("P", []), 1474: ("P", []),
                        897: ("I", []), 752: ("R", ["I"]), 1485: ("R", ["P"]), 1615: ("R", []), 1500: ("P", []), 1504: ("P", []), 1505: ("P", []), 1758: ("T", ["I"])},
 "EA-HK-HISTLOGOS-01": {1758: ("T", ["P", "R"]), 1505: ("P", []), 1503: ("P", [])}}[K.ID]
_have = {n for _k, (_l, _ns) in STRATA.items() for n in _ns}
V12_NEW = []
for _e in V12_STAGE["evidence"]:
    _n = _e.get("deposit") or V12_PHILO
    if _n in _have or _n in V12_NEW: continue
    V12_NEW.append(_n)
assert sorted(V12_NEW) == sorted(V12_BODIES), (sorted(V12_NEW), sorted(V12_BODIES))
for _n, (_b, _sec) in V12_BODIES.items():
    BODY[_n] = _b
    if _sec: SECOND[_n] = _sec
STRATA = {"S0-records-search-v12": ("The records search of 10 November 2026, and In the Midst of the Seven (#1758)", sorted(V12_NEW, key=lambda n: (n != V12_PHILO, n))), **STRATA}
import os as _os
K.VERSION, K.BUILT = _os.environ.get("HKVER", "1.2"), "2026-11-10"   # v1.3 (2026-11-10 21:31): HKVER=1.3, the argument moves of the S0 records
# the Philo piece's claims for this kernel, each a verbatim quotation of #1758
V12_CLAIMS = []
def _v12c(cid, quote, kind, state, body=None):
    K.claim(cid, V12_PHILO, quote, kind, state, body=body); V12_CLAIMS.append(cid)
if K.ID == "EA-HK-REVFIRST-01":
    _v12c("rf-1758-midst", "The Apocalypse sets one figure in the midst of seven lampstands, speaks to each station through its messenger, judges, corrects or confirms each, keeps each on condition of response, and commands writing.", "interpretation", {"assertion": "asserted", "rung": "VI"})
    _v12c("rf-1758-stations", "One instrument becomes seven stations, each answerable for itself", "interpretation", {"assertion": "asserted", "rung": "III", "corpus": "seven_separate_lampstands"})
    _v12c("rf-1758-commission", "The book is a commission of writing still to be done.", "interpretation", {"assertion": "asserted", "rung": "IV", "generation": "commission_drawn_not_run"})
    _v12c("rf-1758-direction", "Direction is not tested here.", "generality", {"assertion": "asserted", "rung": "IV", "generation": "direction_open"})
    _v12c("rf-1758-warrant", "An internal order counted for him as evidence of design.", "observation", {"assertion": "bears_on_rival", "rival": "fw:current-consensus-chronology", "body": "R"}, body="R")
    if _os.environ.get("HKVER") == "1.4":   # v1.4 (2026-11-11): the fold-in of #1758 v1.1 and #1735 v9, for Revelation First
        _v12c("rf-1758-withheld", "Philo quotes the oracle and withholds the name at the place it attaches.", "observation", {"assertion": "asserted", "rung": "VI"})
        _v12c("rf-1758-dependence", "On these grounds the paper states the dependence", "interpretation", {"assertion": "asserted", "rung": "VI", "ancestry": "extant_antecedent_route_open"})
        _v12c("rf-1758-sequence", "Each pair runs downward, the higher sphere first. The pairs climb, lowest, middle, highest.", "observation", {"assertion": "asserted", "rung": "III", "corpus": "sequence_described_not_tested"})
        _v12c("rf-1758-gawaita-key", "Seven named occupants, each over a community's place: on the Gawaita's own terms these are the seven communities, and the Apocalypse's seven messengers over seven churches are the same figure.", "interpretation", {"assertion": "asserted", "rung": "III"})
        K.claim("rf-1735-v9-asymmetry", 1735, "On the ancestry test this is the asymmetry at its sharpest", "interpretation", {"assertion": "asserted", "rung": "VI", "ancestry": "extant_antecedent"})
        K.claim("rf-1735-v9-hebrews", 1735, "A second arrow runs from the same scene, and Newton drew part of it.", "generality", {"assertion": "asserted", "rung": "IV", "generation": "arrow_drawn_not_run"})
        K.claim("rf-1735-v9-hebrews-open", 1735, "The direction is not run here.", "generality", {"assertion": "asserted", "rung": "IV", "generation": "direction_open"})
elif K.ID == "EA-HK-TENTHMUSE-01":
    _v12c("tm-1758-one-treatise", "One treatise of Philo holds the three operations this paper follows.", "observation", {"assertion": "asserted"})
    _v12c("tm-1758-one-vocabulary", "One author holds the displacement law and the naming of the Logos in one vocabulary of rising, setting and utterance.", "interpretation", {"assertion": "asserted"})
    _v12c("tm-1758-two-aphrodites", "The genealogy of two goddesses is the precedent for the division; the rule for acts is the precedent for the purification.", "interpretation", {"assertion": "asserted"})
