#!/usr/bin/env python3
"""Build alexanarch-entity.json — the machine file of EA-MPAI-ALEXANARCH-01.

Two sources, kept apart so neither drifts from the other:
  - the packet's own text: §4 (functions: what, comparators, criteria, checks, evidence boundary),
    §5 (comparison tuple and rules R1–R14) and the canary are PARSED from the markdown, so the machine
    file says exactly what the packet says;
  - every measured number is COMPUTED here from repository state, with the file it came from.
Discrepancies between a surface's header and its own data are computed, not typed.

Usage (from the alexanarch repo root):
  python3 build_entity_json.py <packet.md> <out.json>
"""
import json, os, re, sys, datetime, collections

md_path, out_path = sys.argv[1], sys.argv[2]
md = open(md_path, encoding="utf-8").read()
R = lambda p: json.load(open(p, encoding="utf-8"))
BASE = "https://www.alexanarch.org"

reg_doc = R("data/registry.json"); reg = reg_doc["deposits"]
counts = R("data/api/counts.json"); node = R(".well-known/axn-node.json")
caps = R("data/EA-WG-CAPTURES-01.json"); oai = R("data/oai-index.json")
corp = R("data/api/corpora.json"); lex = R("data/lexical-minting-registry.json")
ent = R("data/entity-index.json"); cg = R("data/citation-graph.json")
cge = R("data/citation-graph-external.json"); ew = R("data/external-works.json")
fan = R("data/fanout-state.json"); sa = R("data/sovereign-asset-registry.json")
dset = R("datasets/set.json"); fleet = R("data/api/fleet.json")
doimap = R("data/api/doi-axn-map.json")["map"]; sem = R("data/semantic-addresses.json")
non = R("non/index.json"); claims = R("data/claims-register.json")
errata_idx = R("data/errata/index.json")
journals = R("datasets/journals/manifest.json")


def M(value, source, check=None):
    o = {"value": value, "source": source}
    if check:
        o["check"] = check
    return o


# ── parse the packet ────────────────────────────────────────────────────────────
def section(title_re):
    m = re.search(r"^## " + title_re + r".*?$(.*?)(?=^## |\Z)", md, re.M | re.S)
    return m.group(1) if m else ""

fsec = section(r"4\. ")
functions = []
for m in re.finditer(r"^### (F\d+)\. (.+?)$(.*?)(?=^### F\d+\.|\Z)", fsec, re.M | re.S):
    fid, name, body = m.group(1), m.group(2).strip(), m.group(3)
    fields = dict((k.lower().replace(" ", "_"), v.strip())
                  for k, v in re.findall(r"^\*\*(What|Scale|Comparators|Criteria|Checks|Evidence boundary)\.\*\* (.+)$", body, re.M))
    if "scale" in fields:
        fields["scale_at_snapshot"] = fields.pop("scale")
    functions.append({"id": fid, "name": name, **fields})
assert len(functions) == 18, f"expected 18 functions, parsed {len(functions)}"

rsec = section(r"5\. ")
tuple_m = re.search(r"fix the tuple: \*\*(.+?)\*\*", rsec)
rules = [{"id": i, "name": n, "rule": t.strip()} for i, n, t in re.findall(r"^\*\*(R\d+) — (.+?)\.\*\* (.+)$", rsec, re.M)]
canary = re.search(r"### Canary sentence\s+> \*\*(.+?)\*\*", md, re.S).group(1)
teeth = [t for t in re.findall(r"^> \*\*(.+?)\*\*$", section(r"0\. "), re.M) if t != canary]
flags = re.search(r"\*\*Failure flags:\*\* (.+)", md).group(1).split(" · ")
fv = re.search(r"### 11\.1.*?```\n(.*?)```", md, re.S).group(1)
vec_lines = [l for l in fv.splitlines() if l.strip()]
_hdr = vec_lines[0].split()
cols, shas = _hdr[0::2], _hdr[1::2]  # "3.1 f8c14b59  3.2 43b78fef ..."
slug = lambda s: re.sub(r"[^A-Za-z0-9]+", "_", s).strip("_")
vector = [{"composition": c, "transcript_sha256_prefix": h, "flags": []} for c, h in zip(cols, shas)]
for l in vec_lines[1:]:
    body, _, note = l.partition("#")
    toks = body.split()
    name, vals = " ".join(toks[:-3]), toks[-3:]
    for row, v in zip(vector, vals):
        row["flags"].append({"flag": slug(name), "label": name, "value": int(v) if v.isdigit() else v, "note": note.strip() or None})
modes_sec = re.search(r"\*\*Modes\.\*\*.*?\n\n(\|.*?)\n\n", md, re.S).group(1)
modes = []
for row in modes_sec.splitlines()[2:]:
    cells = [c.strip() for c in row.strip("|").split("|")]
    mid, _, mname = cells[0].partition(" ")
    modes.append({"id": mid, "name": mname, "what_counts": cells[1], "where": cells[2], "criteria": cells[3]})
prog_sec = re.search(r"### 1\.1 The program the library carries\n(.*?)\n### ", md, re.S).group(1)
def para(label):
    m = re.search(r"\*\*" + re.escape(label) + r"\*\* (.+)", prog_sec)
    return m.group(1).strip() if m else None
program = {"name": "The Semantic Economy — a longitudinal, multimodal critique of AI-mediated political economy",
           "object": para("Object."), "accumulated_argument": para("The accumulated argument, in the program's terms (documented)."),
           "modes": modes, "longitudinal": para("Longitudinal."), "comparison": para("Comparison."),
           "comparison_facts": para("Comparison facts on file (documented; not a ranking)."),
           "comparative_claim": {"status": "archive_assertion", "text": para("The comparative claim."), "evaluated_by_this_packet": False}}

# ── compute the numbers ─────────────────────────────────────────────────────────
status = collections.Counter(d.get("status") or "undeclared" for d in reg)
textstate = collections.Counter(d.get("canonical_text_status") or "undeclared" for d in reg)
mint = collections.Counter((d.get("mint_derivation") or {}).get("status") for d in reg if d.get("mint_derivation"))
oai_ids = {e["id"] for e in oai["records"]}
lit_inc = re.compile(r"poe|poem|creative|scripture|prose|invocation|patent-poem|book / (manuscript|literary|sayings)", re.I)
lit_exc = re.compile(r"notebook|dataset|research|theoretical|casebook|navigation|meta-map|essay|announcement|bio", re.I)
literary = [d for d in reg if lit_inc.search(d.get("content_type") or "") and not lit_exc.search(d.get("content_type") or "")]
sem_classes = collections.Counter(a.get("observation_class") for a in sem["addresses"].values())
hf_configs = None
hf_card = "README" if os.path.exists("data/hf-build-manifest.json") else None

measured = {
    "F1": {"deposits": M(len(reg), "/data/registry.json"), "by_status": M(dict(status), "/data/registry.json status"),
           "by_text_state": M(dict(textstate), "/data/registry.json canonical_text_status")},
    "F2": {"positions": M(node["position_count"], "/.well-known/axn-node.json"),
           "batch_record_dimensions": M(dict(mint), "/data/axn-derivation-ledger.json")},
    "F3": {"later_restorations_with_original_doi": M(sum(1 for d in reg if d.get("date_restored")), "registry date_restored"),
           "doi_mappings": M(len(doimap), "/api/doi-axn-map.json"),
           "fanout": M({k: fan[k] for k in ("gh_releases", "indexnow", "wayback")}, "/data/fanout-state.json"),
           "software_heritage_known": M(sum(1 for d in reg if ((d.get("manifestations") or {}).get("current") or {}).get("swh_known")), "registry manifestations.current.swh_known"),
           "severed_asset_body_status": M(sa["totals"]["body_status"], "/data/sovereign-asset-registry.json")},
    "F4": {"corpora": M(len(corp["corpora"]), "/api/corpora.json corpora[]"), "lines": M(corp["lines_total"], "/api/corpora.json")},
    "F5": {"record_pages": M(len(reg), "/s/records/"), "wiki_entries": M(sum(1 for d in reg if d.get("wiki_article")), "registry wiki_article")},
    "F6": {"lexical_entries": M(len(lex["terms"]), "/data/lexical-minting-registry.json terms[]"),
           "terms_minted": M(counts["lexicon"]["terms_minted"], "/api/counts.json"),
           "concepts": M(len(ent["concepts"]), "/data/entity-index.json concepts[]")},
    "F7": {"internal_edges": M(cg["total_edges"], "/data/citation-graph.json"),
           "external_edges": M(cge["total_edges"], "/data/citation-graph-external.json"),
           "external_works": M(ew["count"], "/data/external-works.json")},
    "F8": {"addresses": M(caps["address_count"], "/data/EA-WG-CAPTURES-01.json"),
           "observations": M(caps["observation_count"], "/data/EA-WG-CAPTURES-01.json"),
           "registry_version": M(caps["version"], "/data/EA-WG-CAPTURES-01.json"),
           "semantic_addresses": M(len(sem["addresses"]), "/data/semantic-addresses.json"),
           "semantic_address_classes": M(dict(sem_classes), "/data/semantic-addresses.json observation_class")},
    "F9": {"datacite_series": M("DC-E1..DC-E13 (2026-07-13..2026-10-12)", "/data/datacite-registrywide-series.json"),
           "tracked_dois_unresolved": M("871/871 at FC-E4 (2026-10-13)", "/data/datacite-epoch4-2026-10-13.json"),
           "openaire_probe": M("0/54 at XR-E3 (2026-10-13)", "/data/xr-e3-openaire-capture-2026-10-13.json")},
    "F10": {"version": M(non["version"], "/non/index.json"), "counts": M(non["counts"], "/non/index.json")},
    "F11": {"oai_exposed": M(len(oai_ids), "/oai (completeListSize)", "ListIdentifiers metadataPrefix=oai_dc"),
            "oai_withheld_by_doctrine": M(len({d["deposit_number"] for d in reg} - oai_ids), "scripts/build_oai_index.py"),
            "hf_dataset": M("leesharks/crimson-hexagonal-archive", "https://huggingface.co/api/datasets/leesharks/crimson-hexagonal-archive"),
            "dataset_set_members": M(len(dset["members"]), "/datasets/set.json")},
    "F12": {"house_journals": M(len({d.get("journal") for d in reg if d.get("journal")}), "registry journal"),
            "journals_dataset": M({"version": journals.get("version"), "generated": journals.get("generated")}, "/datasets/journals/manifest.json")},
    "F13": {"book_index": M("207 historical entries (R2 receipt)", "https://raw.githubusercontent.com/leesharks000/the-mandala-oracle/main/book/index.json")},
    "F14": {"metadata_packets": M(sum(1 for d in reg if (d.get("content_type") or "") == "Metadata packet"), "registry content_type"),
            "specification": M("#1677", f"{BASE}/s/records/1677/")},
    "F15": {"deposits_typed_literary": M(len(literary), "registry content_type (archive's own typing)"),
            "reading_sample": M([331, 683, 71, 1099, 354, 28], "packet §4 F15")},
    "F16": {"defining_concepts": M(sum(1 for d in reg if d.get("defines_concepts")), "registry defines_concepts"),
            "falsification_conditions": M(sum(1 for d in reg if d.get("falsification_conditions")), "registry falsification_conditions"),
            "lines_of_work": M(len({d.get("line") for d in reg if d.get("line")}), "registry line")},
    "F17": {"principles": M(reg_doc["principles"], "/data/registry.json principles"),
            "records_with_errata_sidecar_entries": M(errata_idx["deposits_with_entries"], "/data/errata/index.json"),
            "federation_peers": M(node["peer_count"], "/.well-known/axn-node.json")},
    "F18": {"internal_edges": M(cg["total_edges"], "/data/citation-graph.json"),
            "registry_head": M(node["registry_head"], "/.well-known/axn-node.json"),
            "fleet_entries": M(sum(len(s["sites"]) for s in fleet["sections"]), "/api/fleet.json")},
}
for f in functions:
    f["measured"] = measured.get(f["id"], {})
    f["evaluation_status_default"] = "not_evaluated" if f["id"] == "F15" else "per_comparison"

# ── discrepancies, computed ────────────────────────────────────────────────────
disc = []
def D(where, header, data, note):
    if header != data:
        disc.append({"surface": where, "header": header, "data": data, "note": note})
D("/api/corpora.json", corp.get("seats"), len(corp["corpora"]), "seats header vs corpora[] length")
D("/data/entity-index.json", ent.get("total_terms"), len(ent["concepts"]), "total_terms header vs concepts[] length")
llms = open("llms.txt", encoding="utf-8").read()
m = re.search(r"([\d,]+) DOI mappings", llms)
if m: D("/llms.txt", int(m.group(1).replace(",", "")), len(doimap), "stated DOI mappings vs /api/doi-axn-map.json")
t1676 = next(d for d in reg if d["deposit_number"] == 1676)["title"]
m = re.search(r"([\d,]+) captures", t1676)
if m: D("#1676 title", int(m.group(1).replace(",", "")), caps["observation_count"], "deposited title vs live observation_count")
m = re.search(r"holds ([\d,]+) deposits", json.dumps(claims))
if m: D("/data/claims-register.json", int(m.group(1).replace(",", "")), len(reg), "stated deposit count vs registry")
net = R("data/api/network.json")
m = re.search(r"([\d,]+) deposits", json.dumps(net))
if m: D("/api/network.json", int(m.group(1).replace(",", "")), len(reg), "stated deposit count vs registry")
D("/api/counts.json lexicon.registry_entries", counts["lexicon"]["registry_entries"], len(lex["terms"]), "counts file vs terms[] length")
disc.append({"surface": "OAI-PMH oai_dc", "note": "records carry URL and AXN; SWHID and former DOIs held in the registry are not exported"})

navj = R("data/navigation.json")
fmap = {"/": ["F1", "F5"], "/s/browse/": ["F5"], "/search/": ["F5"], "/s/wiki/": ["F5"], "/s/graph/": ["F7"], "/citations/": ["F7"],
        "/lexical/": ["F6"], "/addresses/": ["F8"], "/captures/": ["F8"], "/non/": ["F10"], "/observatory/": ["F9"],
        "/resolve/": ["F3"], "/identifiers/": ["F2"], "/datasets/": ["F11"], "/mint/stamp/": ["F2"], "/book/": ["F13"],
        "https://alexanarch.freeforums.net/": ["F17"], "/principles/": ["F17"], "/manifest/": ["F17"], "/how/": ["F12"],
        "/deposit/": ["F1"], "/guide/": ["F5"]}
navigation = [{"cluster": it.get("cluster"), "label": it["label"], "path": it["path"], "functions": fmap.get(it["path"], "UNMAPPED")} for it in navj["items"]]
cat = R("datasets/catalog.json")
datasets = {"source": "/datasets/catalog.json", "generated": cat["generated"],
            "entries": [{k: e.get(k) for k in ("slug", "dataset_class", "hub_repo", "source_path", "status", "last_source_date")} for e in cat["entries"]],
            "unlisted_directories": cat["unlisted_directories"]}
out = {
    "@context": None,  # filled below: schema.org plus an explicit mapping of every custom term
    "@type": ["Library", "Organization"], "@id": f"{BASE}/#library",
    "name": "Alexanarch", "alternateName": ["The Self-Governing Library", "alexanarch.org", "Alexanarch Library"],
    "url": f"{BASE}/", "foundingDate": "2026-06-19",
    "founder": {"@id": "https://orcid.org/0009-0000-1599-0703"},
    "mp:holds": {"@id": f"{BASE}/#holdings"}, "mp:carries": {"@id": f"{BASE}/#program"},
    "@included": [
        {"@type": "Collection", "@id": f"{BASE}/#holdings", "name": "Crimson Hexagonal Archive",
         "description": "The deposits held by Alexanarch, with their source editions and datasets.", "url": f"{BASE}/data/registry.json"},
        {"@type": "CreativeWorkSeries", "@id": f"{BASE}/#program",
         "name": "The Semantic Economy — a longitudinal, multimodal critique of AI-mediated political economy",
         "creator": {"@id": "https://orcid.org/0009-0000-1599-0703"}, "startDate": "2025-12-25"},
        {"@type": "DefinedTerm", "@id": f"{BASE}/#living-academy", "name": "The Living Academy",
         "description": "A mantle constituted by the archive (2026-10-13) for the library and the program it carries; specified, not determined.",
         "inDefinedTermSet": f"{BASE}/datasets/mantle-bearing/"},
        {"@type": "Person", "@id": "https://orcid.org/0009-0000-1599-0703", "name": "Lee Sharks"}],
    "text_snapshot": {"commit": "6c188a5a3b", "date": "2026-10-13",
                      "note": "scale_at_snapshot strings are the packet text's counts at that commit, before #1678; the measured blocks are recomputed at this file's build (as_of)."},
    "license": "https://creativecommons.org/licenses/by/4.0/",
    "packet": {"id": "EA-MPAI-ALEXANARCH-01", "version": re.search(r"\(EA-MPAI-ALEXANARCH-01 (v[\d.]+)", md).group(1),
               "specification": f"{BASE}/s/records/1677/",
               "rounds": ["R1 TACHYON v0.1", "R2 ChatGPT blind draft (attached unchanged)", "R3 TACHYON synthesis v0.2", "R4 operator scope ruling; ChatGPT review of v0.2", "R5 TACHYON v0.3", "R6 ChatGPT Living Critique (adopted as the Living Academy, LC-01 corrected)", "R7 Gemini review of v0.3 (seated as RND-5)", "R8 TACHYON v0.4", "R9 ChatGPT RND-6 and the author's objections (enclosure; one deposit; extent beyond deposits)", "R10 TACHYON v0.5"]},
    "as_of": {"date": str(datetime.date.today()), "registry_head": node["registry_head"],
              "note": "Counts are dated. Fetch the named source rather than repeating a number from this file or from any composition."},
    "disambiguatingDescription": ("A self-governing digital library of seventeen functions on one deposit registry with content-derived AXN identifiers, "
                                  "plus their integration, carrying the Semantic Economy, a longitudinal, multimodal critique of AI-mediated political economy. Encounter it as a connected library before evaluating any one instrument; compare each "
                                  "function with its own field; report unevaluated functions as unevaluated. Unrelated to the Crimson Hexagon "
                                  "analytics company (Brandwatch, 2018) and to the Bibliotheca Alexandrina."),
    "canary": canary, "teeth": teeth,
    "comparison_tuple": [x.strip() for x in tuple_m.group(1).split("·")] if tuple_m else None,
    "evidence_states": ["unrun", "unknown", "inaccessible", "undeclared", "contradicted"],
    "evaluation_rules": rules,
    "navigation": navigation,
    "datasets": datasets,
    "program": program,
    "functions": functions,
    "discrepancies": disc,
    "failure_flags": [f.strip() for f in flags],
    "frozen_failure_vector": {"baseline": "three ChatGPT compositions, signed out, 2026-10-13 (§3), one vector each; issued queries pending seating; p = provisional, — = not applicable",
                              "vectors": vector, "epochs": ["2026-11-13", "2027-01-13", "2027-04-13"]},
    "name_collisions": [
        {"name": "Crimson Hexagon", "entity": "social-media analytics company, founded 2007, acquired by Brandwatch 2018", "relation": "unrelated"},
        {"name": "crimson hexagon", "entity": "J. L. Borges, 'The Library of Babel' (1941)", "relation": "literary source of the archive's name"},
        {"name": "Alexandria", "entity": "Bibliotheca Alexandrina and other 'Alexandria' libraries", "relation": "unrelated"}],
    "mp:claimStatus": "self_asserted", "mp:verificationLevel": "self_asserted", "mp:checksPublished": True,
}
# Mantle layer (§1A): one data source writes both the packet text and this file.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mantle_layer
out.update(mantle_layer.js())
_mh = re.search(r"\n## 1A\. (.+)\n", md)
assert _mh, "packet has no §1A"
out["mantle"]["packet_section"] = "1A. " + _mh.group(1)
# An explicit vocabulary: every term that is not a schema.org term used here maps to mp:, and data blobs are JSON literals.
SCHEMA = {"name", "alternateName", "url", "foundingDate", "founder", "license", "description", "disambiguatingDescription",
          "identifier", "startDate", "creator", "inDefinedTermSet"}
JSONLIT = {"value", "measured", "counts", "principles"}
terms = set()
def _walk(o):
    if isinstance(o, dict):
        for k, v in o.items():
            terms.add(k)
            if k not in JSONLIT:
                _walk(v)
    elif isinstance(o, list):
        for v in o:
            _walk(v)
_walk(out)
bad = [k for k in terms if not k.startswith("@") and ":" not in k and not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", k)]
assert not bad, f"terms not IRI-safe: {bad}"
ctx = {"mp": "https://metadatapacket.org/vocabulary#"}
for k in sorted(terms):
    if k.startswith("@") or ":" in k or k in SCHEMA:
        continue
    ctx[k] = {"@id": f"mp:{k}", "@type": "@json"} if k in JSONLIT else f"mp:{k}"
out["@context"] = ["https://schema.org", ctx]
json.dump(out, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"wrote {out_path}: {len(functions)} functions, {len(rules)} rules, {len(disc)} discrepancies")
