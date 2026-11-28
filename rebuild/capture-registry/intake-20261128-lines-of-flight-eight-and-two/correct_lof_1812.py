"""Correction, 2026-11-28: the lines-of-flight capture of #1812 reported two terms as not found in the seated v2.1 text. Both are there.
'T_Μ v0.4' is the paper's own designation, and the five forms are 'F1 STAGE, F2 ENACT, F3 LIKEN, F4 FORETELL, F5 HAPPEN'; the intake searched
for 'version 0.4', 'likening' and 'foretelling' as spelled in the answer. The entry's analysis and fourth finding are rewritten, the was/now logged."""
import json, pathlib, re
ROOT = pathlib.Path(__file__).resolve().parents[3]; P = ROOT / "data/EA-WG-CAPTURES-01.json"; r = json.loads(P.read_text(encoding="utf-8"))
e = [x for x in r["entries"] if x["slug"] == "matthew-from-revelation-1812-lines-of-flight-chatgpt-20261128"][0]
was = {"analysis": e["analysis"], "findings": list(e["findings"])}
a0 = "Second, two of its terms were not found in the seated v2.1 text: the five forms under the names 'likening' and 'foretelling', and 'version 0.4' as a version (0.4 is a section number there)."
a1 = ("Second, where the earlier state comes from can be named. The record's description and its wiki article, as they stood on 2026-11-28, open on the v1.0 state ('a ledger of 86 relations', '178 of Matthew's 1,067 verses') and add v1.1 and v2.1 as closing paragraphs; "
      "a reader who takes the opening and the v1.1 paragraph has the answer given here. The procedure as 'version 0.4' and the five forms (stage, enact, liken, foretell, happen) are the paper's own and are in the seated v2.1 text.")
assert a0 in e["analysis"]; e["analysis"] = e["analysis"].replace(a0, a1).replace("What the composer was served is not established here. ", "")
f0 = [f for f in e["findings"] if f.startswith("TWO TERMS NOT FOUND")]; assert len(f0) == 1
e["findings"][e["findings"].index(f0[0])] = ("THE EARLIER STATE IS IN THE RECORD'S OWN METADATA. The description and wiki article of #1812 opened on v1.0's figures and carried v2.1 only as a closing paragraph (as of 2026-11-28). "
                                              "'T_Μ v0.4' and the five forms are the paper's own terms and are in the text.")
for k in ("analysis", "findings"):
    for o in e.get("observations") or []:
        if k in o and o[k] == was[k]: o[k] = e[k]
r["correction_log"].append({"date": "2026-11-28", "slug": e["slug"], "fields": ["analysis", "findings"], "was": was, "now": {"analysis": e["analysis"], "findings": e["findings"]},
    "reason": "the intake reported 'version 0.4' and the form names as not found in the seated text of #1812; they are there ('T_Μ v0.4'; 'F1 STAGE, F2 ENACT, F3 LIKEN, F4 FORETELL, F5 HAPPEN'). The search used the answer's spellings. The source of the answer's earlier state is now named: the record's description and wiki article, which led with v1.0.",
    "by": "the session (2026-11-28), after an unprimed ChatGPT reading of the live record pasted by the operator at 13:37 EST"})
m = re.fullmatch(r"(\d+)\.(\d+)", r["version"]); r["version"] = f"{m.group(1)}.{int(m.group(2)) + 1}"
P.write_text(json.dumps(r, ensure_ascii=False, indent=1), encoding="utf-8"); print("corrected; registry", r["version"])
