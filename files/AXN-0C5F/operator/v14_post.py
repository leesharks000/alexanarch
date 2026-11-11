# v1.4 of EA-HK-REVFIRST-01 (2026-11-11), executed in build_hk_revfirst.py after v12_post when HKVER=1.4: the fold-in of In the Midst of the Seven v1.1
# (#1758) and Revelation First v9 (#1735), at the author's word ("this is a new folding in, separate from the sappho chain, for revfirst"; "ready").
# The Tenth Muse and the Historical Logos are not versioned on this pass.
K.BUILT = "2026-11-11"; kernel["built"] = "2026-11-11"
for _r in kernel["records_search_v12"]["evidence"]["records"]:
    if _r["deposit"] == 1758:
        _r["note"] = _r["note"].replace("(EA-MIDST-01 v1.0), the Philo piece of the search, deposited 2026-11-10.", "(EA-MIDST-01), the Philo piece of the search, deposited 2026-11-10, at v1.1 since 2026-11-11.")
kernel["records_search_v12"]["evidence"]["argument_layer"] = ("these records entered the kernel at v1.2 without moves; at v1.3 (the author, 2026-11-10 21:31: \"lets do the argument moves\") each was read in full "
    "and its argument compressed into moves, each quotation asserted verbatim against the seated text (args/build_s*.py, mlib.py), and written into 04-arguments.jsonl; at v1.4 the moves of #1758 were brought to its v1.1 (args/v14_moves.py)")
_r58, _r35 = K.REG[1758], K.REG[1735]
kernel["fold_in_v14"] = {
 "date": "2026-11-11",
 "rulings": [{"at": "2026-11-11 04:23", "text": "and this is a new folding in, separate from the sappho chain, for revfirst"}, {"at": "2026-11-11 05:00", "text": "ready"}],
 "records": [{"record": "rec:1758", "deposit": 1758, "version": _r58["version"], "axn": _r58["axn"], "sha256": _r58["hash"],
              "note": "In the Midst of the Seven v1.1: the dependence argued with the alternatives inside the test (16.7); Zechariah 3 and the name Philo withholds, read as a socket (2.6, 4.1a-4.5); the two Joshuas, Hebrews 4 and Justin (7a.8-7a.9); the white stone as acquittal (7b.9-7b.10); the letters' sequence against the Chaldean order (11.5b); the Haran Gawaita as key (13.0, 13.6, 13.7); Wolfson and Barker (16.5b)"},
             {"record": "rec:1735", "deposit": 1735, "version": _r35["version"], "axn": _r35["axn"], "sha256": _r35["hash"],
              "note": "Revelation First v9: the Philonic organization and Zechariah 3 as extant antecedents of the figure in the midst (VI.1); the Gawaita as a late witness (IV.1); the arrow to Hebrews 4.8-14, drawn and not run (VI.3); their conditions (VIII)"}],
 "claims_added": ["claim:rf-1758-withheld", "claim:rf-1758-dependence", "claim:rf-1758-sequence", "claim:rf-1758-gawaita-key", "claim:rf-1735-v9-asymmetry", "claim:rf-1735-v9-hebrews", "claim:rf-1735-v9-hebrews-open"],
 "moves": "#1758: twelve moves re-quoted from the paragraphs v1.1 revised, ids kept, thirty-three new; #1735: thirteen new; every quotation asserted by check_args.py",
 "not_versioned": "EA-HK-TENTHMUSE-01 (#1756) and EA-HK-HISTLOGOS-01 (#1757), at the author's word: the fold-in is for Revelation First, separate from the Sappho chain"}
