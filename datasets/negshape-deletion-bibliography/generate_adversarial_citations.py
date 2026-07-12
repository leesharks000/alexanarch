#!/usr/bin/env python3
"""
generate_adversarial_citations.py — Appendix A of EA-NEGSHAPE-01.

Reads the deletion-event corpus (DataCite full backup + DOI resolution index)
and renders each work referenced by the citing authority's bulk deletion of
2026-06-19 as a formal citation in MLA 9, Chicago 17, APA 7, and BibTeX.

The premise, stated plainly: a bulk deletion file identifies, individuates,
attributes, timestamps, and judges each work it enumerates. That is the
complete functional anatomy of a citation. This script converts the citing
authority's own records of the works it destroyed into the standard formats
of scholarly reference. Where the authority also destroyed the metadata, the
citation renders the wound as a field.

Strata:
  A — RECOVERED: full DataCite metadata survives in independent capture.
      Complete formal citations.
  B — SEVERED:   DOI returns 404/410 from the authority's registry; title
      and date recovered from the DOI Resolution Index where available.
      Citations carry '[creator record destroyed by citing authority,
      19 June 2026]' in the author field.

Outputs (to ./out/):
  adversarial-citations.json   — full dataset, all strata, all formats
  adversarial-citations.csv    — flat table
  SAMPLE-MLA.md / SAMPLE-CHICAGO.md / SAMPLE-APA.md / SAMPLE-BIBTEX.md
  STATS.json                   — counts used by the paper
"""

import csv
import json
import os
import re
import sys
import unicodedata
from collections import OrderedDict

REPO = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/axn-work"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)

DELETION_DATE_HUMAN = "19 June 2026"
DELETION_DATE_ISO = "2026-06-19"
AUTHORITY = "CERN / Zenodo"
SEVERED_AUTHOR = "[creator record destroyed by citing authority, 19 June 2026]"
SEVERED_AUTHOR_BIB = "{[creator record destroyed by citing authority, 19 June 2026]}"

MONTHS = ["", "January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]


def clean(s):
    if not s:
        return ""
    s = unicodedata.normalize("NFC", str(s))
    return re.sub(r"\s+", " ", s).strip()


def parse_date(rec):
    """Return (year, month, day) ints where known, else Nones."""
    for d in rec.get("dates", []):
        if d.get("dateType") == "Issued" and d.get("date"):
            m = re.match(r"(\d{4})(?:-(\d{2}))?(?:-(\d{2}))?", d["date"])
            if m:
                return (int(m.group(1)),
                        int(m.group(2)) if m.group(2) else None,
                        int(m.group(3)) if m.group(3) else None)
    y = rec.get("publicationYear")
    return (int(y) if y else None, None, None)


def names_from_creators(creators):
    """Return list of (family, given, literal) tuples."""
    out = []
    for c in creators or []:
        fam = clean(c.get("familyName"))
        giv = clean(c.get("givenName"))
        lit = clean(c.get("name"))
        if not fam and lit and "," in lit:
            fam, giv = [clean(x) for x in lit.split(",", 1)]
        out.append((fam, giv, lit))
    return out


# ── format renderers ────────────────────────────────────────────────────────

def mla_authors(names):
    if not names:
        return SEVERED_AUTHOR
    def inv(n):
        fam, giv, lit = n
        return f"{fam}, {giv}" if fam and giv else (lit or fam or giv)
    def fwd(n):
        fam, giv, lit = n
        return f"{giv} {fam}".strip() if fam or giv else lit
    if len(names) == 1:
        return inv(names[0])
    if len(names) == 2:
        return f"{inv(names[0])}, and {fwd(names[1])}"
    return f"{inv(names[0])}, et al"


def chicago_authors(names):
    if not names:
        return SEVERED_AUTHOR
    def inv(n):
        fam, giv, lit = n
        return f"{fam}, {giv}" if fam and giv else (lit or fam or giv)
    def fwd(n):
        fam, giv, lit = n
        return f"{giv} {fam}".strip() if fam or giv else lit
    if len(names) == 1:
        return inv(names[0])
    parts = [inv(names[0])] + [fwd(n) for n in names[1:]]
    if len(parts) == 2:
        return f"{parts[0]}, and {parts[1]}"
    return ", ".join(parts[:-1]) + f", and {parts[-1]}"


def apa_authors(names):
    if not names:
        return SEVERED_AUTHOR
    def one(n):
        fam, giv, lit = n
        if fam and giv:
            initials = " ".join(f"{p[0]}." for p in giv.split() if p)
            return f"{fam}, {initials}"
        return lit or fam or giv
    parts = [one(n) for n in names]
    if len(parts) == 1:
        return parts[0]
    return ", ".join(parts[:-1]) + f", & {parts[-1]}"


def date_mla(y, m, d):
    if y and m and d:
        return f"{d} {MONTHS[m][:3]}. {y}" if MONTHS[m][:3] not in ("May",) else f"{d} May {y}"
    return str(y) if y else "n.d."


def date_chicago(y, m, d):
    if y and m and d:
        return f"{MONTHS[m]} {d}, {y}"
    return str(y) if y else "n.d."


def date_apa(y, m, d):
    if y and m and d:
        return f"{y}, {MONTHS[m]} {d}"
    return str(y) if y else "n.d."


def render(entry):
    """Produce all four formats + the adversarial tail."""
    names, title, (y, m, d), doi, stratum, status = (
        entry["names"], entry["title"], entry["date_parts"],
        entry["doi"], entry["stratum"], entry["status"])
    doi_url = f"https://doi.org/{doi}"
    tail = (f" Cited by {AUTHORITY} in the bulk deletion of {DELETION_DATE_HUMAN}; "
            f"reference maintained by the citing authority as DOI tombstone ({status}).")

    mla = (f"{mla_authors(names)}. \u201c{title}.\u201d *Zenodo*, "
           f"{date_mla(y, m, d)}, {doi_url}.{tail}")

    chi = (f"{chicago_authors(names)}. \u201c{title}.\u201d Zenodo, "
           f"{date_chicago(y, m, d)}. {doi_url}.{tail}")

    apa = (f"{apa_authors(names)} ({date_apa(y, m, d)}). *{title}*. Zenodo. "
           f"{doi_url}{tail}")

    key = "cha" + re.sub(r"\D", "", doi)[-8:]
    bib_author = SEVERED_AUTHOR_BIB if not names else " and ".join(
        (f"{n[0]}, {n[1]}" if n[0] and n[1] else n[2]) for n in names)
    bib = (f"@misc{{{key},\n"
           f"  author       = {{{bib_author}}},\n"
           f"  title        = {{{title}}},\n"
           f"  publisher    = {{Zenodo}},\n"
           f"  year         = {{{y if y else 'n.d.'}}},\n"
           f"  doi          = {{{doi}}},\n"
           f"  url          = {{{doi_url}}},\n"
           f"  note         = {{Cited by {AUTHORITY} in the bulk deletion of "
           f"{DELETION_DATE_HUMAN}; DOI tombstoned ({status}). Stratum {stratum}.}}\n"
           f"}}")

    return {"mla9": mla, "chicago17": chi, "apa7": apa, "bibtex": bib}


# ── load corpus ─────────────────────────────────────────────────────────────

backup = json.load(open(os.path.join(REPO, "data/datacite-full-backup.json")))
residx = json.load(open(os.path.join(REPO, "data/doi-resolution-index.json")))

# Membership audit results from Appendix B (run generate_deletion_bibliography first)
_bpath = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "out-b", "deletion-bibliography.json")
MEMBERSHIP = {}
if os.path.exists(_bpath):
    for _r in json.load(open(_bpath))["entries"]:
        MEMBERSHIP[_r["doi"]] = {
            "status": _r["membership_review_status"],
            "basis": _r["membership_basis"],
        }

not_found = set(backup.get("not_found_dois", []))
records = backup["records"]

entries = OrderedDict()

# Stratum A — recovered full metadata
for r in records:
    at = r.get("attributes", {})
    doi = clean(at.get("doi") or r.get("id"))
    if not doi or doi in entries:
        continue
    titles = at.get("titles") or []
    title = clean(titles[0].get("title")) if titles else ""
    if not title:
        continue
    entries[doi] = {
        "doi": doi,
        "title": title,
        "names": names_from_creators(at.get("creators")),
        "date_parts": parse_date(at),
        "stratum": "A-RECOVERED",
        "status": "Zenodo record destroyed 2026-06-19; DataCite metadata extant",
        "metadata_source": "DataCite full backup (independent capture, pre/post-severance sweep)",
    }

# Stratum B — severed; recover title/date from resolution index
by_dead = {}
for mp in residx.get("mappings", []):
    dd = clean(mp.get("dead_doi"))
    if dd and dd not in by_dead:
        by_dead[dd] = mp

sev_with_title = 0
for doi in sorted(not_found):
    if doi in entries:
        continue
    mp = by_dead.get(doi, {})
    mtype = clean(mp.get("mapping_type")) or "no_mapping"
    unresolved_parent = "unresolved" in (clean(mp.get("note")) or "").lower()
    stratum = ("C-REFERENCED-UNRESOLVED"
               if (mtype in ("registry_referenced", "misclassified_other_author",
                             "no_mapping") or unresolved_parent)
               else "B-SEVERED")
    title = clean(mp.get("title")) if not unresolved_parent else ""
    date = clean(mp.get("date"))
    dp = (None, None, None)
    if date:
        m = re.match(r"(\d{4})(?:-(\d{2}))?(?:-(\d{2}))?", date)
        if m:
            dp = (int(m.group(1)),
                  int(m.group(2)) if m.group(2) else None,
                  int(m.group(3)) if m.group(3) else None)
    status = clean(mp.get("status")) or "404_NOT_FOUND"
    entries[doi] = {
        "doi": doi,
        "title": title or "[title record destroyed by citing authority, 19 June 2026]",
        "names": [],  # creator record severed
        "date_parts": dp,
        "stratum": stratum,
        "status": status.replace("_", " ").title(),
        "mapping_type": mtype,
        "metadata_source": ("DOI Resolution Index (title/date recovered from "
                            "independent surfaces)") if title else
                           "none recoverable — full severance",
    }
    if title and stratum == "B-SEVERED":
        sev_with_title += 1

# ── render ──────────────────────────────────────────────────────────────────

dataset = []
for doi, e in entries.items():
    mem = MEMBERSHIP.get(doi, {"status": "unresolved", "basis": "inferred_from_context"})
    confirmed = mem["status"] == "confirmed"
    row = {
        "membership_review_status": mem["status"],
        "membership_basis": mem["basis"],
        "doi": doi,
        "doi_url": f"https://doi.org/{doi}",
        "title": e["title"],
        "creators": ["{} {}".format(n[1], n[0]).strip() or n[2] for n in e["names"]] or
                    ["[severed]"],
        "date": "-".join(str(x).zfill(2) for x in e["date_parts"] if x) or "n.d.",
        "stratum": e["stratum"],
        "tombstone_status": e["status"],
        "metadata_source": e["metadata_source"],
        "mapping_type": e.get("mapping_type", "datacite_backup"),
        "citing_authority": AUTHORITY,
        "citation_act": f"bulk deletion of {DELETION_DATE_ISO}",
        "citation_locus": "DataCite DOI registry (standing tombstone reference)",
        "citations": (render(e) if confirmed else None),
        "citation_rendering": ("rendered" if confirmed else
                               "withheld_pending_membership"),
    }
    dataset.append(row)

from collections import Counter as _C
stats = {
    "identifier_entries_total": len(dataset),
    "membership": dict(_C(r["membership_review_status"] for r in dataset)),
    "membership_confirmed": sum(1 for r in dataset
                                if r["membership_review_status"] == "confirmed"),
    "citations_rendered": sum(1 for r in dataset if r["citations"]) * 4,
    "total_works_cited_by_authority": len(dataset),
    "stratum_A_recovered_full_metadata": sum(1 for r in dataset if r["stratum"] == "A-RECOVERED"),
    "stratum_B_severed": sum(1 for r in dataset if r["stratum"] == "B-SEVERED"),
    "stratum_B_with_recovered_title": sev_with_title,
    "stratum_B_fully_dark": sum(1 for r in dataset
                                if r["stratum"] == "B-SEVERED" and
                                r["title"].startswith("[title record destroyed")),
    "stratum_C_referenced_unresolved": sum(1 for r in dataset
                                           if r["stratum"] == "C-REFERENCED-UNRESOLVED"),
    "headline_confirmed_works": sum(1 for r in dataset
                                    if r["stratum"] in ("A-RECOVERED", "B-SEVERED")),
    "formats_per_work": 4,
    "citing_authority": AUTHORITY,
    "citation_act_date": DELETION_DATE_ISO,
}

with open(os.path.join(OUT, "adversarial-citations.json"), "w") as f:
    json.dump({
        "name": "Adversarial Citations of the Crimson Hexagonal Archive",
        "description": ("Formal renderings (MLA 9, Chicago 17, APA 7, BibTeX) of every "
                        "work referenced by the citing authority's bulk deletion of "
                        "2026-06-19 and its standing DOI tombstones. Appendix A of "
                        "EA-NEGSHAPE-01."),
        "stats": stats,
        "works": dataset,
    }, f, indent=1, ensure_ascii=False)

with open(os.path.join(OUT, "adversarial-citations.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["doi", "title", "creators", "date", "stratum", "tombstone_status",
                "mla9", "chicago17", "apa7"])
    for r in dataset:
        c = r["citations"] or {}
        w.writerow([r["doi"], r["title"], "; ".join(r["creators"]), r["date"],
                    r["stratum"], r["tombstone_status"],
                    c.get("mla9", "[withheld pending membership confirmation]"),
                    c.get("chicago17", ""), c.get("apa7", "")])

SAMPLE_N = 25
for fmt, keyname in [("MLA", "mla9"), ("CHICAGO", "chicago17"),
                     ("APA", "apa7"), ("BIBTEX", "bibtex")]:
    lines = [f"# Appendix A sample — {fmt} renderings of the citing authority's references",
             "",
             f"First {SAMPLE_N} of {len(dataset)} works cited by {AUTHORITY} "
             f"in the bulk deletion of {DELETION_DATE_HUMAN}. Full dataset: "
             f"adversarial-citations.json / .csv.", ""]
    for r in [x for x in dataset if x["citations"]][:SAMPLE_N]:
        body = r["citations"][keyname]
        if fmt == "BIBTEX":
            lines += ["```bibtex", body, "```", ""]
        else:
            lines += [body, ""]
    with open(os.path.join(OUT, f"SAMPLE-{fmt}.md"), "w") as f:
        f.write("\n".join(lines))

with open(os.path.join(OUT, "STATS.json"), "w") as f:
    json.dump(stats, f, indent=1)

print(json.dumps(stats, indent=1))
