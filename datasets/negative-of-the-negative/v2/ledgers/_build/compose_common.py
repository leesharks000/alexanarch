"""Shared writer for the /non entity rows composed 2026-10-07 (Howl, Theophrastus, the Socratic problem).

Each compose_<entity>.py defines the plan (sentences, compression, rail, T, delta, kernel) and calls write_row().
Checks before writing: every claim id cited exists in the field ledger or the archive ledger; every field claim
carries source/locus/quote; the archive ledger rows carry what claim_li needs.
"""
import json, pathlib, re, hashlib, shutil

REPO = pathlib.Path("/home/claude/alexanarch")
V2 = REPO / "datasets/negative-of-the-negative/v2"
HERE = pathlib.Path(__file__).resolve().parent


def words(t):
    return len(re.findall(r"[A-Za-z0-9'’-]+", t or ""))


def sents(paras):
    out, n = [], 0
    for pi, para in enumerate(paras):
        for text, claims in para:
            n += 1
            out.append({"para": pi, "text": text, "n": n, "claims": claims})
    return out


def write_row(entity, row, field, ledger_src, reading_src=None):
    fc = field["field_claims"]
    fs = {x["id"]: x["card"] for x in field["field"] if x["id"].startswith("B") and x["id"][1:].isdigit()}
    L = json.loads(pathlib.Path(ledger_src).read_text(encoding="utf-8"))
    ids = {c["id"] for c in L}
    for c in L:
        for k in ("id", "dep", "date", "locus", "modality", "quote"):
            assert c.get(k) not in (None, ""), (c.get("id"), k)
    used = set()
    o = row["objects"]
    for key in ("KO", "KO_B"):
        for s in o[key]["sentences"]:
            used.update(s["claims"])
    for key in ("P", "P_B"):
        used.update(o[key]["lede"]["claims"])
        for sec in o[key]["sections"]:
            for it in sec["items"]:
                used.update(it["claims"])
        for ln in o[key]["rail"]:
            used.update(ln["claims"])
    for k in row["kernel"]:
        used.add(k["claim"].strip("`"))
    missing = sorted(c for c in used if c not in fc and c not in ids)
    assert not missing, missing
    for key in ("KO_B", "P_B"):
        bad = []
        if key == "KO_B":
            bad = [c for s in o[key]["sentences"] for c in s["claims"] if c not in fc]
        else:
            bad = [c for c in o[key]["lede"]["claims"] if c not in fc] + [c for sec in o[key]["sections"] for it in sec["items"] for c in it["claims"] if c not in fc]
        assert not bad, (key, bad)
    # place ledgers and reading in the repo
    ld = V2 / "ledgers" / entity
    ld.mkdir(parents=True, exist_ok=True)
    (ld / "ledger-archive.json").write_text(json.dumps(L, ensure_ascii=False, indent=1), encoding="utf-8")
    (ld / "field.json").write_text(json.dumps(field, ensure_ascii=False, indent=1), encoding="utf-8")
    if reading_src:
        shutil.copy(reading_src, V2 / "traversal" / entity / "reading.json")
    row["field_claims"] = {k: {kk: v[kk] for kk in ("source", "locus", "quote")} | {"modality": v.get("modality")} for k, v in fc.items()}
    row["field_sources"] = fs
    o["KO"]["field_claims"] = row["field_claims"]
    o["KO"]["field_sources"] = fs
    o["KO_B"]["field_claims"] = row["field_claims"]
    o["KO_B"]["field_sources"] = fs
    o["L_B"] = {"words": words(" ".join(s["text"] for s in o["KO_B"]["sentences"])), "text": " ".join(s["text"] for s in o["KO_B"]["sentences"]),
                "note": "L(B) is realized as the field arm's expansion (objects.KO_B): the same plan, the field alone."}
    o["L_BA"] = {"words": words(" ".join(s["text"] for s in o["KO"]["sentences"])), "text": " ".join(s["text"] for s in o["KO"]["sentences"]), "rail": [],
                 "note": "L(B ∪ A) is realized as the knowledge object (objects.KO); its rail is the compression's, by lineage (§5.2)."}
    row["ledger"] = {"archive": f"datasets/negative-of-the-negative/v2/ledgers/{entity}/ledger-archive.json",
                     "field": f"datasets/negative-of-the-negative/v2/ledgers/{entity}/field.json",
                     "selection": f"datasets/negative-of-the-negative/v2/traversal/{entity}/",
                     "audit": None}
    row["_field_claims_note"] = "The field ledger (ledgers/%s/field.json), extracted 2026-10-07 from the sources the layer surfaced, by WebFetch excerpt; shared by both arms." % entity
    (V2 / "rows" / f"{entity}.json").write_text(json.dumps(row, ensure_ascii=False, indent=1), encoding="utf-8")
    nf = len({c for s in o["KO"]["sentences"] for c in s["claims"] if c in fc})
    na = len({c for s in o["KO"]["sentences"] for c in s["claims"] if c not in fc})
    print(f"{entity}: KO {len(o['KO']['sentences'])} sentences, {o['L_BA']['words']} words, {nf} field + {na} archive claims; "
          f"KO_B {len(o['KO_B']['sentences'])} sentences; P rail {len(o['P']['rail'])}; kernel {len(row['kernel'])}")
