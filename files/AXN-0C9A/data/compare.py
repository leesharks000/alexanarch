"""Same counts on Classical Receptions Journal and the International Journal of the Classical Tradition (Crossref, read 2026-11-14).
Book reviews, notices and front matter are separated by rule; the rule and the separated titles are written out so the split can be checked."""
import json, re, html, collections, pathlib
H = pathlib.Path(__file__).resolve().parent
clean = lambda s: re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s or ""))).strip()
REVIEW = re.compile(r"(\(\s*[A-Z][^()]*:\s*[^()]*\d{4}\)|\d+\s*pp\.|\bpp\.\s*$|ISBN|^Publications received|^Books received|^Review of|^Book review)", re.I)
FRONT = re.compile(r"^(International Journal of the Classical Tradition|Editorial|Editor'?s? note|Introduction|Afterword|Erratum|Corrigendum|Correction to|OUP accepted manuscript|In Memoriam|Obituary|Preface|Foreword)\b", re.I)
MACH = re.compile(r"\b(artificial intelligence|AI|ChatGPT|GPT|large language model|LLM|language model|chatbot|algorithm\w*|machine learning|neural|search engine|Google|Wikipedia|AI Overview\w*|generative)\b")
def load(files):
    it = []
    for f in files: it += json.loads((H / f).read_text())["message"]["items"]
    return [i for i in it if i.get("type") == "journal-article"]
def kind(t):
    if FRONT.search(t): return "front"
    if REVIEW.search(t): return "review"
    return "article"
def run(name, files, self_titles, self_prefix):
    it = load(files); rows = []
    for i in it:
        t = clean((i.get("title") or [""])[0]); y = i.get("issued", {}).get("date-parts", [[None]])[0][0]
        refs = i.get("reference", [])
        rows.append({"doi": i["DOI"], "year": y, "title": t, "kind": kind(t), "abstract": clean(i.get("abstract")) or None,
                     "cited_by": i.get("is-referenced-by-count", 0), "refs": refs,
                     "cc": any("creativecommons" in l["URL"] for l in i.get("license", []))})
    art = [r for r in rows if r["kind"] == "article"]
    refs = [x for r in art for x in r["refs"]]
    reftext = lambda x: " ".join(str(x.get(k, "")) for k in ("unstructured", "article-title", "volume-title", "journal-title", "series-title"))
    jt = collections.Counter(x.get("journal-title") for x in refs if x.get("journal-title"))
    selfj = sum(c for j, c in jt.items() if j and j.strip().lower() in self_titles)
    selfd = sum(1 for x in refs if (x.get("DOI") or "").lower().startswith(self_prefix))
    mach_t = [(r["year"], r["title"]) for r in art if MACH.search(r["title"])]
    mach_a = [(r["year"], r["title"], MACH.search(r["abstract"]).group(0)) for r in art if r["abstract"] and MACH.search(r["abstract"])]
    mach_r = [(m.group(0), reftext(x)[:140]) for x in refs for m in [MACH.search(reftext(x))] if m]
    def per(a, b):
        s = [r for r in art if r["year"] and a <= r["year"] <= b]
        return {"works": len(s), "cited_by": sum(r["cited_by"] for r in s), "mean": round(sum(r["cited_by"] for r in s) / max(1, len(s)), 2), "zero": sum(1 for r in s if r["cited_by"] == 0)}
    out = {"journal": name, "items": len(rows), "kinds": collections.Counter(r["kind"] for r in rows),
           "articles": len(art), "years": [min(r["year"] for r in art if r["year"]), max(r["year"] for r in art if r["year"])],
           "abstracts": sum(1 for r in art if r["abstract"]), "with_refs": sum(1 for r in art if r["refs"]), "refs": len(refs),
           "self_refs_by_title": selfj, "self_refs_by_doi": selfd, "self_share": round(selfj / max(1, len(refs)), 4),
           "top_journals": jt.most_common(8), "cc": sum(1 for r in art if r["cc"]),
           "cited_by": sum(r["cited_by"] for r in art), "zero_cited": sum(1 for r in art if r["cited_by"] == 0),
           "per_2009_2014": per(2009, 2014), "per_2015_2020": per(2015, 2020), "per_2021_2026": per(2021, 2026),
           "machine_in_titles": mach_t, "machine_in_abstracts": mach_a, "machine_in_refs": mach_r[:40], "machine_in_refs_n": len(mach_r),
           "top_cited": sorted(((r["cited_by"], r["year"], r["title"][:90]) for r in art), reverse=True)[:10]}
    (H / f"compare-{name}.json").write_text(json.dumps(out, ensure_ascii=False, indent=1, default=list))
    (H / f"compare-{name}-split.txt").write_text("\n".join(f"{r['kind']}\t{r['year']}\t{r['title']}" for r in sorted(rows, key=lambda r: (r['kind'], r['year'] or 0))))
    return out
A = run("crj", ["raw/crossref-crj-20261114.json"], {"classical receptions journal"}, "10.1093/crj")
B = run("ijct", ["raw/crossref-ijct-a.json", "raw/crossref-ijct-b.json"], {"international journal of the classical tradition"}, "10.1007/s12138")
for o in (A, B):
    print(o["journal"], {k: o[k] for k in ("items", "kinds", "articles", "years", "abstracts", "with_refs", "refs", "self_refs_by_title", "self_share", "cc", "cited_by", "zero_cited", "machine_in_refs_n")})
    print("  periods", o["per_2009_2014"], o["per_2015_2020"], o["per_2021_2026"])
    print("  top journals", o["top_journals"][:4])
    print("  machine titles", o["machine_in_titles"]); print("  machine abstracts", o["machine_in_abstracts"])
    print("  machine refs", o["machine_in_refs"][:12])
