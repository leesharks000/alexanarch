#!/usr/bin/env python3
"""Lexicon pass 2 (2026-10-12): flag deformed definitions by their form; repair them from the deposit's own text
where the repair is mechanically certain. Follows the 2026-08-14 _CLEANING principle: NOTHING IS DELETED.

FLAG — definition_status, set only on entries without one, for definitions whose FORM shows they are not a definition
of the term (the term itself is not judged; 'Hexagonal Licensing Protocol' is a coinage whose recorded definition
happens to be its citation):
  heading        the definition is a markdown heading ('## XIX. THE LIQUIDATION OF INTERVENTIONS')
  citation       the definition is a bibliographic citation or a bare DOI
  mid-sentence   the definition begins with punctuation: the term was cut from the head of a sentence
  question       the definition is a question
  endpoint       the definition is a URL or an API route
REPAIR WAS TRIED AND WITHDRAWN (2026-10-12). Searching each deposit's text for the one definitional construction of
the term ('**Term** — …', 'Term: …', 'Term is …') yielded 147 candidates, and on reading they were not repairs: the
terms sit in bulleted lists, the 'sentence after' runs into the next items ('Dormant' -> 'Archived but activatable -
**Dead**: Surface preserved, function lost …'), and the recorded short glosses were mostly right. No repair here is
mechanically certain, so none is made; the code path is kept, disabled, as the record of the attempt.
"""
import json, re, sys, pathlib, collections
ROOT = pathlib.Path(__file__).resolve().parents[2]
LEX = ROOT / "data/lexical-minting-registry.json"
REG = ROOT / "data/registry.json"
FORM = [
    ("heading", lambda d: re.match(r"^\s*#{1,6}\s", d) is not None),
    ("citation", lambda d: re.match(r"^\s*(?:[A-Z][\w'’\-]+,\s(?:[A-Z]\.\s?)+(?:,|&|and|\(|$)|\(?(?:DOI|doi):?\s*10\.\d{4,})", d) is not None),
    ("mid-sentence", lambda d: re.match(r"^\s*[.,;:)\]]", d) is not None),
    ("question", lambda d: d.strip().endswith("?") and not re.search(r"[.!]\s", d.strip()[:-1][-200:] or "")),
    ("endpoint", lambda d: re.match(r"^\s*(?:https?://|POST |GET |PUT )", d) is not None),
]


def sentence_after(text, i):
    s = text[i:i + 900]
    s = re.split(r"(?<=[.!?])\s+(?=[A-Z*#\[])|\n\s*\n", s, maxsplit=1)[0]
    return re.sub(r"\s+", " ", s).strip(" *_")


def definitional(text, term):
    t = re.escape(term.strip())
    pats = [rf"\*\*{t}\*\*\s*(?:\([^)]*\))?\s*[:—–-]\s*", rf"(?m)^\s*[-*]?\s*{t}\s*:\s+", rf"(?<![\w*])\*?{t}\*?\s+(?:is|refers to|names|denotes)\s+(?=\w)"]
    hits = []
    for k, p in enumerate(pats):
        for m in re.finditer(p, text):
            body = sentence_after(text, m.end())
            if k == 2:
                body = term.strip() + " " + text[m.end() - len(m.group(0)) + len(term):m.end()].strip() + " " + body
            hits.append(body)
    hits = [h for h in dict.fromkeys(hits) if 40 <= len(h) <= 600 and not FORM_BAD(h)]
    return hits[0] if len(hits) == 1 else None


def FORM_BAD(d):
    return any(f(d) for _, f in FORM)


def main():
    write = "--write" in sys.argv
    lex = json.loads(LEX.read_text(encoding="utf-8")); T = lex["terms"]
    deps = {d["deposit_number"]: d for d in json.loads(REG.read_text(encoding="utf-8"))["deposits"]}
    texts = {}
    def text_of(n):
        if n not in texts:
            p = (deps.get(n) or {}).get("full_text_path") or ""
            f = ROOT / p.lstrip("/") if p else None
            texts[n] = f.read_text(encoding="utf-8", errors="ignore") if f and f.exists() else ""
        return texts[n]
    flagged, repaired, kept = collections.Counter(), collections.Counter(), collections.Counter()
    sample = []
    for t in T:
        d = t.get("definition") or ""
        st = t.get("definition_status")
        if not st and t.get("mint_mode") in ("batch", "bulk-extraction", "deliberate") and not t.get("entry_class"):
            for k, f in FORM:
                if f(d):
                    st = k; flagged[k] += 1
                    if write: t["definition_status"] = k
                    break
        if not st:
            continue
        new = definitional(text_of(t.get("defined_in_deposit")), t.get("term") or "") if "--try-repair" in sys.argv else None
        if new:
            repaired[st] += 1; sample.append((st, t["term"][:40], d[:50], new[:140]))
            if write:
                t["definition_prior"] = d; t["definition"] = new
                t["definition_repair"] = {"date": "2026-10-12", "from": f"deposit #{t.get('defined_in_deposit')} text, the one definitional construction of the term",
                                          "prior_status": st}
                t.pop("definition_status", None)
        else:
            kept[st] += 1
    print("newly flagged:", dict(flagged), sum(flagged.values()))
    print("repaired:", dict(repaired), sum(repaired.values()))
    print("still flagged (for reading):", dict(kept), sum(kept.values()))
    if "--show" in sys.argv:
        import random; random.seed(7)
        for s in random.sample(sample, min(30, len(sample))): print("  ", s)
    if write:
        c = lex.setdefault("_CLEANING", {}); c.setdefault("passes", [])
        c["passes"].append({"date": "2026-10-12", "pass": 2, "script": "rebuild/lexicon/repair_definitions_20261012.py",
                            "flagged_by_form": dict(flagged), "repair": "tried and withdrawn: list-item continuations, not definitions; none made",
                            "still_flagged": dict(kept), "principle": "nothing deleted; prior definitions kept as definition_prior"})
        LEX.write_text(json.dumps(lex, ensure_ascii=False, indent=1), encoding="utf-8"); print("written")


if __name__ == "__main__":
    main()
