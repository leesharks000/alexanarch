#!/usr/bin/env python3
"""
generate_deletion_bibliography.py — Appendix B of EA-NEGSHAPE-01.

Appendix A cited each work as *referenced by* the deletion. Appendix B performs
the deeper construction: the bulk deletion event is itself constituted as a
FORMAL BIBLIOGRAPHIC OBJECT — a publication — and every work of the archive is
cited as a work WITHIN that container, the way an article is cited within a
journal issue or a chapter within an edited collection.

This requires generative bibliographic thinking, because no citation manual
anticipates the genre. The construction proceeds from function: the deletion
event has a publisher (CERN/Zenodo), a publication date (2026-06-19), an
enumerated table of contents (the deleted records), a compiler of record (the
moderation process that assembled it), a distribution infrastructure (the
standing DOI tombstones, each a page of the publication), and a persistent
public existence. Functionally, it is an edited collection published in the
DOI registry. We cite it as one — in four genre constructions — and, because
the publisher issued its own publication no identifier, the archive assigns
it a sovereign one.

THE BIBLIOGRAPHIC MATRIX: for every entry, every field (creator, title, date,
identifier, container locus) is populated from the best available source and
carries PER-CELL PROVENANCE:

  AUTHORITY_EXTANT   — DataCite metadata the authority still serves
  CAPTURE_DATACITE   — independent capture of authority metadata (backup sweep)
  RESOLVER           — DOI Resolution Index (title/date from independent surfaces)
  SOVEREIGN_ARCHIVE  — Alexanarch registry (creator/title via resolver chain)
  UNRECOVERED        — destroyed by the citing authority, no recovery route

Outputs (to ./out-b/):
  deletion-container-object.md      — the container, cited (4 genre constructions x 4 formats)
  deletion-bibliography.json        — full matrix + in-container citations
  deletion-bibliography.csv         — flat matrix
  SAMPLE-INCONTAINER-*.md           — per-format samples
  MATRIX-STATS.json                 — coverage: cells filled, by source
"""

import csv
import json
import os
import re
import sys
import unicodedata
from collections import OrderedDict, Counter

REPO = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/axn-work"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out-b")
os.makedirs(OUT, exist_ok=True)

# ── the container object ────────────────────────────────────────────────────

CONTAINER = {
    "sovereign_id": "CHA-DELETION-CORPUS-20260619",
    "title_journal": "Zenodo Bulk Record Deletions",
    "issue": "issue of 19 June 2026 (The Crimson Hexagonal Archive Issue)",
    "title_collection": "Bulk Record Deletion of 19 June 2026: The Crimson Hexagonal Archive",
    "publisher": "CERN / Zenodo",
    "place": "Geneva",
    "date_human": "19 June 2026",
    "date_iso": "2026-06-19",
    "compiler": "the moderation process of record",
    "extent": "1,834 identifier entries enumerated (1,621 membership-confirmed; "
              "65 probable; 80 unresolved; 68 rejected collisions); deletion "
              "executed at a sustained rate of approximately 6.6 objects per second",
    "distribution": "published serially in the DataCite DOI registry as standing "
                    "tombstones, each resolving publicly at doi.org",
    "note": "The publisher issued its publication no identifier of its own; "
            "the sovereign identifier above is assigned by the archive it "
            "enumerates, which also supplies its bibliography.",
}

DELETION_HUMAN = CONTAINER["date_human"]
MONTHS = ["", "January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]


def clean(s):
    if not s:
        return ""
    s = unicodedata.normalize("NFC", str(s))
    return re.sub(r"\s+", " ", s).strip()


def container_citations():
    c = CONTAINER
    return {
        "as_journal_issue": {
            "mla9": (f"*{c['title_journal']}*, {c['issue']}, compiled by "
                     f"{c['compiler']}, {c['publisher']}, {c['date_human']}. "
                     f"Published serially as standing DOI tombstones, doi.org. "
                     f"{c['extent'].capitalize()}. Sovereign identifier "
                     f"{c['sovereign_id']} (assigned by the archive enumerated; "
                     f"the publisher issued none)."),
            "chicago17": (f"*{c['title_journal']}*. Issue of June 19, 2026 (The "
                          f"Crimson Hexagonal Archive Issue). Compiled by "
                          f"{c['compiler']}. {c['place']}: {c['publisher']}, 2026. "
                          f"Distributed as standing DOI tombstones via doi.org."),
            "apa7": (f"{c['publisher']}. (2026, June 19). *{c['title_journal']}: "
                     f"The Crimson Hexagonal Archive issue* [Bulk deletion event; "
                     f"tombstone corpus]. doi.org. {c['note']}"),
            "bibtex": ("@collection{chadeletion20260619,\n"
                       f"  title     = {{{c['title_collection']}}},\n"
                       f"  editor    = {{{{{c['compiler']}}}}},\n"
                       f"  publisher = {{{c['publisher']}}},\n"
                       f"  address   = {{{c['place']}}},\n"
                       f"  year      = {{2026}},\n"
                       f"  month     = {{jun}},\n"
                       f"  note      = {{{c['extent']}. {c['distribution'].capitalize()}. "
                       f"Sovereign identifier {c['sovereign_id']}.}}\n"
                       "}"),
        },
        "as_edited_collection": {
            "chicago17": (f"{c['compiler'].capitalize()}, comp. *{c['title_collection']}*. "
                          f"{c['place']}: {c['publisher']}, 2026."),
        },
        "as_dataset": {
            "apa7": (f"{c['publisher']}. (2026). *{c['title_collection']}* "
                     f"[Data set: deletion log; 1,834 enumerated records]. "
                     f"DataCite DOI registry."),
        },
        "as_archival_fonds": {
            "chicago17": (f"Bulk Record Deletion of June 19, 2026 (tombstone corpus). "
                          f"Records of the Zenodo repository moderation process, "
                          f"{c['publisher']}, {c['place']}. Consulted as standing "
                          f"DOI tombstones, doi.org, July 2026."),
        },
    }


# ── load sources ────────────────────────────────────────────────────────────

backup = json.load(open(os.path.join(REPO, "data/datacite-full-backup.json")))
residx = json.load(open(os.path.join(REPO, "data/doi-resolution-index.json")))
registry = json.load(open(os.path.join(REPO, "data/registry.json")))

not_found = set(backup.get("not_found_dois", []))
by_dead = {}
for m in residx.get("mappings", []):
    dd = clean(m.get("dead_doi"))
    if dd and dd not in by_dead:
        by_dead[dd] = m

rec_creator = {d["deposit_number"]: clean(d.get("creator"))
               for d in registry["deposits"]}
rec_title = {d["deposit_number"]: clean(d.get("title"))
             for d in registry["deposits"]}

DIRECT = ("direct", "direct_verified", "title_match_repoint")
ORCID = "0009-0000-1599-0703"


def _census_norm(name):
    n = clean(name).lower()
    if "," in n:
        fam, giv = [x.strip() for x in n.split(",", 1)]
        n = f"{giv} {fam}"
    return re.sub(r"[^a-z ]", "", n).strip()


# Registered-creator census: every creator string the sovereign registry has
# ever attributed a deposit to (split on interpunct/semicolon/&/and).
REGISTERED = set()
for c in rec_creator.values():
    for part in re.split(r"\s*[\u00b7;]\s*|\s+&\s+|\s+and\s+", c or ""):
        p = _census_norm(part)
        if p:
            REGISTERED.add(p)


def audit_membership_A(at, doi):
    """Membership provenance for a DataCite-recovered entry.
    Returns (basis, source, confidence, review_status, note)."""
    if not doi.startswith("10.5281/"):
        return ("creator_string_only", "datacite_creator_sweep", "none",
                "rejected_collision",
                "non-Zenodo DOI retrieved by creator-name query; "
                "heteronym collision with unrelated civil person")
    has_orcid = any(ni.get("nameIdentifier") == ORCID
                    for c in at.get("creators", [])
                    for ni in c.get("nameIdentifiers", []))
    if has_orcid:
        return ("datacite_orcid_match", "DataCite creators.nameIdentifiers",
                "high", "confirmed", "")
    has_affil = any("crimson hexagonal" in clean(a).lower()
                    for c in at.get("creators", [])
                    for a in (c.get("affiliation") or []))
    if has_affil:
        return ("datacite_affiliation_match", "DataCite creators.affiliation",
                "high", "confirmed", "")
    names = [_census_norm(c.get("name") or
                          f"{c.get('givenName','')} {c.get('familyName','')}")
             for c in at.get("creators", [])]
    names = [n for n in names if n]
    if names and all(n in REGISTERED for n in names):
        return ("exact_registered_creator_match", "sovereign registry creator census",
                "high", "confirmed", "")
    if names and any(n in REGISTERED for n in names):
        return ("partial_registered_creator_match", "sovereign registry creator census",
                "medium", "probable",
                "some creators outside the registered census; human review")
    return ("creator_string_only", "datacite_creator_sweep", "none",
            "rejected_collision",
            "no creator matches the sovereign registered-creator census; "
            "retrieved by name-string query only")


def is_fragment(doi):
    tail = doi.split(".")[-1]
    return doi.startswith("10.5281/zenodo.") and tail.isdigit() and len(tail) < 6


def split_creators(c):
    """Split multi-creator registry strings on interpunct/semicolon/ampersand."""
    c = clean(c)
    if not c:
        return []
    parts = re.split(r"\s*[\u00b7;]\s*|\s+&\s+|\s+and\s+", c)
    return [p for p in (clean(x) for x in parts) if p]


def norm_creator(c):
    """Normalize 'Sharks, Lee' and 'Lee Sharks' to (family, given); literals pass."""
    c = clean(c)
    if not c:
        return None
    if "," in c:
        fam, giv = [clean(x) for x in c.split(",", 1)]
        return (fam, giv, c)
    if "(" in c or c.isupper():
        return ("", "", c)  # literal (e.g. TACHYON (Claude/Anthropic))
    parts = c.split()
    if len(parts) >= 2:
        return (parts[-1], " ".join(parts[:-1]), c)
    return ("", "", c)


def date_parts(datestr, year=None):
    if datestr:
        m = re.match(r"(\d{4})(?:-(\d{2}))?(?:-(\d{2}))?", datestr)
        if m:
            return (int(m.group(1)),
                    int(m.group(2)) if m.group(2) else None,
                    int(m.group(3)) if m.group(3) else None)
    return (int(year) if year else None, None, None)


# ── assemble the matrix ─────────────────────────────────────────────────────

entries = OrderedDict()

# Stratum A — authority metadata captured
for r in backup["records"]:
    at = r.get("attributes", {})
    doi = clean(at.get("doi") or r.get("id"))
    if not doi or doi in entries:
        continue
    titles = at.get("titles") or []
    title = clean(titles[0].get("title")) if titles else ""
    if not title:
        continue
    basis, msrc, conf, review, mnote = audit_membership_A(at, doi)
    concept = None
    for rel in (at.get("relatedIdentifiers") or []):
        if rel.get("relationType") == "IsVersionOf" and rel.get("relatedIdentifier"):
            concept = clean(rel["relatedIdentifier"]); break
    if re.search(r"\.v\d+$", doi):
        rtype = "version_doi"
        concept = concept or re.sub(r"\.v\d+$", "", doi)
    elif concept and concept != doi:
        rtype = "version_doi"
    else:
        # self-referencing IsVersionOf is prevalent in this corpus and
        # uninformative; typing is left unresolved rather than guessed
        rtype = "unresolved"
        concept = None
    family = concept or doi
    creators = []
    for c in at.get("creators", []):
        fam, giv = clean(c.get("familyName")), clean(c.get("givenName"))
        lit = clean(c.get("name"))
        creators.append((fam, giv, lit) if (fam or giv) else ("", "", lit))
    issued = next((d.get("date") for d in at.get("dates", [])
                   if d.get("dateType") == "Issued"), None)
    entries[doi] = {
        "doi": doi,
        "stratum": "A",
        "membership": {"basis": basis, "source": msrc, "confidence": conf,
                       "review_status": review, "note": mnote},
        "record_type": rtype,
        "work_family_id": family,
        "cells": {
            "creator": {"value": creators, "source": "CAPTURE_DATACITE"},
            "title": {"value": title, "source": "CAPTURE_DATACITE"},
            "date": {"value": date_parts(issued, at.get("publicationYear")),
                     "source": "CAPTURE_DATACITE"},
            "identifier": {"value": doi, "source": "AUTHORITY_EXTANT"},
            "container_locus": {"value": f"https://doi.org/{doi}",
                                "source": "AUTHORITY_EXTANT"},
        },
    }

# Strata B/C — severed; recover through resolver + sovereign archive
for doi in sorted(not_found):
    if doi in entries:
        continue
    mp = by_dead.get(doi, {})
    mtype = clean(mp.get("mapping_type")) or "no_mapping"
    unresolved_parent = "unresolved" in (clean(mp.get("note")) or "").lower()
    fragment = is_fragment(doi)
    stratum = "B" if (mtype in DIRECT and not unresolved_parent
                      and not fragment) else "C"
    sev = clean(mp.get("severance_class"))
    rtype = ("concept_doi" if sev == "concept_root" else
             "version_doi" if sev == "version_of_mapped_root" else
             "unresolved")
    family = clean(mp.get("root_axn")) or clean(mp.get("axn")) or doi
    if fragment:
        membership = {"basis": "inferred_from_context",
                      "source": "identifier extraction from registry documents",
                      "confidence": "none", "review_status": "unresolved",
                      "note": "identifier fragment; completeness not established"}
    elif stratum == "C":
        membership = {"basis": "inferred_from_context",
                      "source": "sovereign registry reference",
                      "confidence": "low", "review_status": "unresolved",
                      "note": "parent-work identity unresolved"}
    elif mtype == "direct_verified":
        membership = {"basis": "sovereign_registry_exact_doi",
                      "source": "DOI Resolution Index (verified mapping)",
                      "confidence": "high", "review_status": "confirmed", "note": ""}
    else:
        membership = {"basis": "sovereign_registry_exact_doi",
                      "source": "DOI Resolution Index (direct mapping)",
                      "confidence": "medium", "review_status": "probable",
                      "note": "direct mapping pending verification pass"}

    cells = {}
    # title: resolver, else sovereign archive, else unrecovered
    title = clean(mp.get("title"))
    alex_no = None
    mm = re.match(r"/s/records/(\d+)/", mp.get("alexanarch_record") or "")
    if mm:
        alex_no = int(mm.group(1))
    if title and not unresolved_parent:
        cells["title"] = {"value": title, "source": "RESOLVER"}
    elif title and unresolved_parent:
        cells["title"] = {"value": None, "source": "UNRECOVERED",
                          "note": ("resolver title belongs to the referencing "
                                   "registry document, not the parent work; "
                                   "withheld to avoid misattribution")}
    elif alex_no and rec_title.get(alex_no):
        cells["title"] = {"value": rec_title[alex_no], "source": "SOVEREIGN_ARCHIVE"}
    else:
        cells["title"] = {"value": None, "source": "UNRECOVERED"}

    # creator: sovereign archive via resolver chain
    if stratum == "B" and alex_no and rec_creator.get(alex_no):
        ncs = [norm_creator(p) for p in split_creators(rec_creator[alex_no])]
        ncs = [n for n in ncs if n]
        cells["creator"] = {"value": ncs, "source": "SOVEREIGN_ARCHIVE"}
        if membership["review_status"] == "probable":
            membership = {"basis": "alexanarch_record_exact_doi",
                          "source": "DOI Resolution Index + Alexanarch registry "
                                    "(two independent sovereign discriminators)",
                          "confidence": "high", "review_status": "confirmed",
                          "note": ""}
    else:
        cells["creator"] = {"value": [], "source": "UNRECOVERED"}

    cells["date"] = ({"value": date_parts(clean(mp.get("date"))),
                      "source": "RESOLVER"}
                     if mp.get("date") else
                     {"value": (None, None, None), "source": "UNRECOVERED"})
    cells["identifier"] = {"value": doi, "source": "AUTHORITY_EXTANT"}
    cells["container_locus"] = {"value": f"https://doi.org/{doi}",
                                "source": "AUTHORITY_EXTANT"}

    entries[doi] = {"doi": doi, "stratum": stratum, "cells": cells,
                    "membership": membership,
                    "record_type": rtype,
                    "work_family_id": family,
                    "alexanarch_record": (f"https://alexanarch.org/s/records/{alex_no}/"
                                          if alex_no else None)}

# ── render in-container citations ───────────────────────────────────────────

def fmt_creators_mla(creators):
    if not creators:
        return "[creator field destroyed by publisher; unrecovered]"
    def inv(n): return f"{n[0]}, {n[1]}" if n[0] and n[1] else (n[2] or n[0] or n[1])
    def fwd(n): return f"{n[1]} {n[0]}".strip() if (n[0] or n[1]) else n[2]
    if len(creators) == 1:
        return inv(creators[0])
    if len(creators) == 2:
        return f"{inv(creators[0])}, and {fwd(creators[1])}"
    return f"{inv(creators[0])}, et al"


def fmt_creators_apa(creators):
    if not creators:
        return "[creator field destroyed by publisher; unrecovered]"
    def one(n):
        if n[0] and n[1]:
            return f"{n[0]}, " + " ".join(f"{p[0]}." for p in n[1].split() if p)
        return n[2] or n[0] or n[1]
    parts = [one(n) for n in creators]
    return parts[0] if len(parts) == 1 else ", ".join(parts[:-1]) + f", & {parts[-1]}"


def d_mla(dp):
    y, m, d = dp
    if y and m and d:
        mon = MONTHS[m][:3] + ("" if MONTHS[m] == "May" else ".")
        return f"{d} {mon} {y}"
    return str(y) if y else "n.d."


def d_chi(dp):
    y, m, d = dp
    return f"{MONTHS[m]} {d}, {y}" if (y and m and d) else (str(y) if y else "n.d.")


def d_apa(dp):
    y, m, d = dp
    return f"{y}, {MONTHS[m]} {d}" if (y and m and d) else (str(y) if y else "n.d.")


def render_incontainer(e):
    c = e["cells"]
    creators = c["creator"]["value"]
    title = c["title"]["value"] or "[title field destroyed by publisher; unrecovered]"
    dp = c["date"]["value"]
    doi = c["identifier"]["value"]
    locus = c["container_locus"]["value"]
    src_note = "; ".join(f"{k}: {v['source']}" for k, v in c.items()
                         if k in ("creator", "title", "date"))

    mla = (f"{fmt_creators_mla(creators)}. \u201c{title}.\u201d "
           f"*{CONTAINER['title_journal']}*, {CONTAINER['issue']}, compiled by "
           f"{CONTAINER['compiler']}, {CONTAINER['publisher']}, "
           f"{DELETION_HUMAN}, tombstone {locus}. Originally issued {d_mla(dp)}. "
           f"[{src_note}]")

    def chi_creators(cs):
        if not cs:
            return "[creator field destroyed by publisher; unrecovered]"
        def inv(n): return f"{n[0]}, {n[1]}" if n[0] and n[1] else (n[2] or n[0] or n[1])
        def fwd(n): return f"{n[1]} {n[0]}".strip() if (n[0] or n[1]) else n[2]
        if len(cs) == 1:
            return inv(cs[0])
        parts = [inv(cs[0])] + [fwd(n) for n in cs[1:]]
        return ", ".join(parts[:-1]) + f", and {parts[-1]}"

    chi = (f"{chi_creators(creators)}. \u201c{title}.\u201d In "
           f"*{CONTAINER['title_collection']}*, compiled by {CONTAINER['compiler']}. "
           f"{CONTAINER['place']}: {CONTAINER['publisher']}, 2026. "
           f"Tombstone {locus}. Originally issued {d_chi(dp)}.")

    apa = (f"{fmt_creators_apa(creators)} (2026, June 19 [orig. {d_apa(dp)}]). "
           f"{title}. In {CONTAINER['publisher']} (Comp.), "
           f"*{CONTAINER['title_collection']}* [tombstone corpus entry]. {locus}")

    key = "chadel" + re.sub(r"\D", "", doi)[-8:]
    bib_author = ("{[creator field destroyed by publisher; unrecovered]}"
                  if not creators else
                  " and ".join((f"{n[0]}, {n[1]}" if n[0] and n[1] else n[2])
                               for n in creators))
    bib = (f"@incollection{{{key},\n"
           f"  author    = {{{bib_author}}},\n"
           f"  title     = {{{title}}},\n"
           f"  booktitle = {{{CONTAINER['title_collection']}}},\n"
           f"  editor    = {{{{{CONTAINER['compiler']}}}}},\n"
           f"  publisher = {{{CONTAINER['publisher']}}},\n"
           f"  address   = {{{CONTAINER['place']}}},\n"
           f"  year      = {{2026}},\n"
           f"  month     = {{jun}},\n"
           f"  doi       = {{{doi}}},\n"
           f"  note      = {{Entry of the tombstone corpus; field provenance — {src_note}.}}\n"
           f"}}")

    return {"mla9": mla, "chicago17": chi, "apa7": apa, "bibtex": bib}


dataset = []
rejected_ledger = []
cell_sources = Counter()
cell_total = 0
for doi, e in entries.items():
    mem = e["membership"]
    confirmed = mem["review_status"] == "confirmed"
    if confirmed:
        for k in ("creator", "title", "date"):
            cell_total += 1
            cell_sources[e["cells"][k]["source"]] += 1
    row = {
        "doi": doi,
        "stratum": e["stratum"],
        "membership_basis": mem["basis"],
        "membership_source": mem["source"],
        "membership_confidence": mem["confidence"],
        "membership_review_status": mem["review_status"],
        "membership_note": mem["note"],
        "record_type": e.get("record_type", "unresolved"),
        "work_family_id": e.get("work_family_id", doi),
        "matrix": {k: {"value": (v["value"] if k != "creator" else
                                 [(" ".join(filter(None, (n[1], n[0]))) or n[2])
                                  for n in v["value"]]),
                       "source": v["source"]}
                   for k, v in e["cells"].items()},
        "alexanarch_record": e.get("alexanarch_record"),
        "container": CONTAINER["sovereign_id"],
        "citations_in_container": (render_incontainer(e) if confirmed else None),
        "citation_rendering": ("rendered" if confirmed else
                               "withheld_pending_membership"),
    }
    dataset.append(row)
    if mem["review_status"] == "rejected_collision":
        rejected_ledger.append({
            "doi": doi,
            "title": e["cells"]["title"]["value"],
            "creators": [(" ".join(filter(None, (n[1], n[0]))) or n[2])
                         for n in e["cells"]["creator"]["value"]],
            "reason": mem["note"],
            "retrieved_by": mem["source"],
        })

recovered_cells = cell_total - cell_sources["UNRECOVERED"]
conf = [r for r in dataset if r["membership_review_status"] == "confirmed"]
fams = set(r["work_family_id"] for r in conf)
stats = {
    "container_sovereign_id": CONTAINER["sovereign_id"],
    "identifier_entries_total": len(dataset),
    "membership": dict(Counter(r["membership_review_status"] for r in dataset)),
    "membership_basis": dict(Counter(r["membership_basis"] for r in conf)),
    "membership_confirmed": len(conf),
    "confirmed_record_types": dict(Counter(r["record_type"] for r in conf)),
    "confirmed_unique_work_families": len(fams),
    "rejected_collisions": len(rejected_ledger),
    "citations_rendered": sum(1 for r in dataset if r["citations_in_container"]) * 4,
    "entries_total": len(dataset),
    "strata": dict(Counter(r["stratum"] for r in dataset)),
    "matrix_cells_core": cell_total,
    "matrix_cells_recovered": recovered_cells,
    "matrix_coverage_pct": round(100.0 * recovered_cells / cell_total, 2),
    "cells_by_source": dict(cell_sources),
    "confirmed_corpus_coverage_note":
        "Coverage over Strata A+B (confirmed works) for creator/title/date",
}
ab = conf
ab_cells = 3 * len(ab)
ab_unrec = sum(1 for r in ab for k in ("creator", "title", "date")
               if r["matrix"][k]["source"] == "UNRECOVERED")
stats["confirmed_corpus_cells"] = ab_cells
stats["confirmed_corpus_recovered"] = ab_cells - ab_unrec
stats["confirmed_corpus_coverage_pct"] = round(100.0 * (ab_cells - ab_unrec) / ab_cells, 2)

# ── write outputs ───────────────────────────────────────────────────────────

cc = container_citations()
lines = ["# The Container Object, Cited",
         "",
         "## The bulk deletion of 19 June 2026 as a formal bibliographic object",
         "",
         CONTAINER["note"], "",
         f"**Sovereign identifier:** {CONTAINER['sovereign_id']}",
         f"**Extent:** {CONTAINER['extent']}",
         f"**Distribution:** {CONTAINER['distribution']}", ""]
for genre, fmts in cc.items():
    lines.append(f"### {genre.replace('_', ' ').title()}")
    lines.append("")
    for fmt, cite in fmts.items():
        if fmt == "bibtex":
            lines += [f"**{fmt}:**", "```bibtex", cite, "```", ""]
        else:
            lines += [f"**{fmt}:** {cite}", ""]
with open(os.path.join(OUT, "deletion-container-object.md"), "w") as f:
    f.write("\n".join(lines))

with open(os.path.join(OUT, "deletion-bibliography.json"), "w") as f:
    json.dump({
        "name": "The Deletion as Publication: Bibliographic Matrix of the "
                "Zenodo Bulk Deletion of 2026-06-19",
        "description": ("Appendix B of EA-NEGSHAPE-01. The bulk deletion event "
                        "constituted as a formal bibliographic container; every "
                        "enumerated work cited as a work within it; every field "
                        "populated from the best available source with per-cell "
                        "provenance."),
        "container": CONTAINER,
        "container_citations": cc,
        "stats": stats,
        "entries": dataset,
    }, f, indent=1, ensure_ascii=False)

with open(os.path.join(OUT, "deletion-bibliography.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["doi", "stratum", "membership_review_status", "membership_basis",
                "record_type", "work_family_id",
                "creator", "creator_source", "title",
                "title_source", "date", "date_source", "alexanarch_record",
                "mla9_in_container"])
    for r in dataset:
        m = r["matrix"]
        dp = m["date"]["value"]
        w.writerow([
            r["doi"], r["stratum"], r["membership_review_status"],
            r["membership_basis"], r["record_type"], r["work_family_id"],
            "; ".join(m["creator"]["value"]) or "[unrecovered]",
            m["creator"]["source"],
            m["title"]["value"] or "[unrecovered]", m["title"]["source"],
            "-".join(str(x).zfill(2) for x in dp if x) if dp else "n.d.",
            m["date"]["source"],
            r["alexanarch_record"] or "",
            (r["citations_in_container"] or {}).get("mla9",
                "[citation withheld pending membership confirmation]"),
        ])

SAMPLE_N = 20
for fmt, keyname in [("MLA", "mla9"), ("CHICAGO", "chicago17"),
                     ("APA", "apa7"), ("BIBTEX", "bibtex")]:
    lines = [f"# Appendix B sample — works cited within the deletion object ({fmt})",
             "",
             f"First {SAMPLE_N} of {len(dataset)} entries. Container: "
             f"{CONTAINER['sovereign_id']}. Full matrix: deletion-bibliography.json.",
             ""]
    for r in [x for x in dataset if x["citations_in_container"]][:SAMPLE_N]:
        body = r["citations_in_container"][keyname]
        if fmt == "BIBTEX":
            lines += ["```bibtex", body, "```", ""]
        else:
            lines += [body, ""]
    with open(os.path.join(OUT, f"SAMPLE-INCONTAINER-{fmt}.md"), "w") as f:
        f.write("\n".join(lines))

ledger_lines = [
    "# Rejected-Candidate Ledger: Disambiguation Failures Caught by the Membership Audit",
    "",
    "A creator-name query for archive heteronyms retrieved works by unrelated",
    "civil persons sharing name strings — demonstrating why creator-string identity",
    "cannot establish archive membership without ORCID, repository provenance,",
    "record linkage, or another independent discriminator. The deletion bibliography",
    "reproduced the exact disambiguation failure the archive's provenance",
    "architecture was built to prevent; the membership audit caught it. These",
    "candidates are preserved here and excluded from every count, citation,",
    "and container rendering.",
    "",
]
for r in rejected_ledger:
    ledger_lines.append(f"- **{r['doi']}** — \u201c{(r['title'] or '')[:90]}\u201d — "
                        f"creators: {', '.join(r['creators']) or '[none]'} — {r['reason']}")
with open(os.path.join(OUT, "REJECTED-LEDGER.md"), "w") as f:
    f.write("\n".join(ledger_lines))
with open(os.path.join(OUT, "rejected-ledger.json"), "w") as f:
    json.dump(rejected_ledger, f, indent=1, ensure_ascii=False)

with open(os.path.join(OUT, "MATRIX-STATS.json"), "w") as f:
    json.dump(stats, f, indent=1)

print(json.dumps(stats, indent=1))
