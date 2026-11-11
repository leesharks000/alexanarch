#!/usr/bin/env python3
"""Reissue in place: #1758 In the Midst of the Seven, v1.0 -> v1.1, at the author's word of 2026-11-11 04:14 ("were ready. lets version the deposit").
The body is rebuild/midst-v11/EA-MIDST-01-v1.1-draft.md (four passes, §19.9-19.11), Greek quotations asserted by rebuild/philo-out-loud/quotecheck.py.
Front matter kept from v1.0 with title, version, substrate and keywords brought forward. Hash and AXN re-derived at the same position and family;
the prior hash, AXN and title kept in reissue_history.   python3 rebuild/midst-v11/reissue_v11.py"""
import json, hashlib, pathlib, subprocess, sys
ROOT = pathlib.Path(__file__).resolve().parents[2]; sys.path.insert(0, str(ROOT / "scripts")); import axn_lib as A
raw = (ROOT / "data/registry.json").read_text(encoding="utf-8"); R = json.loads(raw); D = {x["deposit_number"]: x for x in R["deposits"]}
n = 1758; d = D[n]; assert d["version"] == "v1.0", d["version"]
H = pathlib.Path(__file__).parent; body = (H / "EA-MIDST-01-v1.1-draft.md").read_text(encoding="utf-8")
q = subprocess.run([sys.executable, str(ROOT / "rebuild/philo-out-loud/quotecheck.py"), str(H / "EA-MIDST-01-v1.1-draft.md")], capture_output=True, text=True)
assert q.returncode == 0, q.stdout[-500:]; print(q.stdout.strip().splitlines()[-1])
p = ROOT / d["full_text_path"].lstrip("/"); old = p.read_text(encoding="utf-8")
fm_end = old.index("\n---\n", 4) + 5; fm = old[:fm_end]
T0 = "In the Midst of the Seven: Philo, the Logos Named and Lived, and the Seven Stations of Revelation (EA-MIDST-01 v1.0)"
T1 = T0.replace("v1.0)", "v1.1)")
fm = fm.replace(f'title: "{T0}"', f'title: "{T1}"', 1).replace("\nversion: v1.0\n", "\nversion: v1.1\n", 1)
SUB = "The Crimson Hexagonal Archive is credited as a contributor: the work is built from its deposits, seatings, protocols and registries.\""
assert SUB in fm
fm = fm.replace(SUB, SUB[:-1] + " Version 1.1 (11 November 2026) composed by Claude (Anthropic, Claude Opus 5.5) in session on the author's points of that day (the dependence, the two Joshuas and the withheld name, the white stone, the sequence, the Haran Gawaita as key, read whole in the author's copy of Drower) and on two further reviews, recorded in §19.9–19.11.\"", 1)
KW = "  - heavenly and common Aphrodite\n"; assert KW in fm
fm = fm.replace(KW, KW + "".join(f"  - {k}\n" for k in ["the socket", "Zechariah 3", "Joshua the high priest", "Hebrews 4", "white stone as acquittal", "Chaldean order", "Great Revelation", "Wolfson", "Barker", "literary dependence"]), 1)
s = fm + "\n" + body.lstrip("\n")
for chk in (f'title: "{T1}"', "\nversion: v1.1\n", f"# {T1}", "EA-MIDST-01 v1.1 ·", "19.11."): assert chk in s, chk
h = hashlib.sha256(s.encode("utf-8")).hexdigest(); g = A.axn_glyph_from_hash(h); cl = A.axn_clusters_from_hash(h)
d.setdefault("reissue_history", []).append({"date": "2026-11-11", "from_version": "v1.0", "to_version": "v1.1", "hash_before_reissue": d["hash"], "axn_before_reissue": d["axn"],
    "title_before_reissue": d["title"], "reason": 'Lee Sharks, 2026-11-11: "why the hell is that not relatively obvious literary dependence?"; "lets draft it all"; "yup lets fold that all in"; "were ready. lets version the deposit"',
    "changes": "The dependence argued with the alternatives inside the test (16.7); the two Joshuas, Zechariah 3 and the withheld name read as a socket, with Philo's practice inventoried (2.6, 4.1a-4.5, 7a.8-7a.9); the white stone as the vote of acquittal (7b.9-7b.10); the sequence against the Chaldean order, with a table (11.5b); the Haran Gawaita read whole and taken as key (13.0, 13.6, 13.7); Wolfson and Barker (16.5b); the author's points and two reviews recorded (19.9-19.11). Hash and AXN re-derived."})
prior = d["axn"]
d.update({"title": T1, "version": "v1.1", "hash": h, "axn_canonical": h, "emoji": g, "axn": A.compose_axn(d["hex"], d["family"], g), "clusters": cl,
          "axn_reading": A.axn_reading_from_clusters(cl), "full_text_chars": len(s), "date_modified": "2026-11-11"})
OLDD = "The shared architecture is read on the seated texts; dependence is left undecided."
assert d["description"].rstrip().endswith(OLDD)
d["description"] = d["description"].rstrip()[:-len(OLDD)] + ("The shared architecture is read on the seated texts. Version 1.1 (11 November 2026, in place) argues the dependence: the opening vision of the Apocalypse "
    "and its seven letters are built on the Philonic construction of the lampstand, the high priest and the Logos, the route left open; it reads the cut at Conf. 62, where Philo takes the name "
    "Ἀνατολή from an oracle spoken to Ἰησοῦς the high priest and withholds the addressee, as a socket the Apocalypse fills; it joins the white stone as the vote of acquittal, sets the letters' "
    "planetary sequence against the Chaldean order, and reads the Haran Gawaita, which calls itself the Great Revelation, as a key to the seven stations.")
OLDW = "The paper leaves dependence and date undecided."
assert d["wiki_article"].rstrip().endswith(OLDW)
d["wiki_article"] = d["wiki_article"].rstrip()[:-len(OLDW)] + ("Version 1.1 (11 November 2026) argues the literary dependence of the Apocalypse's opening vision and letters on Philo's construction, with the route "
    "and the date left undecided; it reads Philo's omission of the addressee of Zechariah 6:12, Ἰησοῦς the high priest, as a socket the Apocalypse fills, and adds the Haran Gawaita as a key to the seven stations.")
if isinstance(d.get("keywords"), list):
    for k in ["the socket", "Zechariah 3", "Great Revelation", "literary dependence"]:
        if k not in d["keywords"]: d["keywords"].append(k)
p.write_text(s, encoding="utf-8"); dp = ROOT / f"data/deposits/AXN-{d['hex']}.md"
if dp.exists(): dp.write_text(s, encoding="utf-8")
ind = 1 if raw.startswith('{\n "') else (2 if raw.startswith('{\n  "') else None)
(ROOT / "data/registry.json").write_text(json.dumps(R, ensure_ascii=False, indent=ind) + ("\n" if raw.endswith("\n") else ""), encoding="utf-8")
json.dump({prior: d["axn"]}, open(H / "axn-moves-20261111-v11.json", "w"), ensure_ascii=False, indent=1)
print(n, prior, "->", d["axn"])
