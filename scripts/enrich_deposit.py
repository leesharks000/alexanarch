#!/usr/bin/env python3
"""
enrich_deposit.py — Alexanarch deposit enrichment orchestrator.

Runs against a deposit already minted by mint_deposit.py; enriches its registry
entry with concepts, citations, Wikidata QIDs, OpenAlex IDs, DataCite severance
status, SPXI-Protocol-v0.2 layer validation, and cross-reference backlinks.

Depends on ANTHROPIC_API_KEY in the environment for the LLM extraction step.
Other API calls (OpenAlex, Wikidata SPARQL, DataCite) are unauthenticated.

Design principles
-----------------
- Idempotent: re-running produces the same result. Fields are OVERWRITTEN each
  run, not appended to, so if the LLM produces different output the enrichment
  reflects the newest pass.
- Modular: each enrichment step is a function callable independently, so
  Lee can re-enrich just concepts without redoing external metadata, etc.
- Fail-open: any single step failure is logged and skipped, so a Wikidata
  outage doesn't block concept extraction.
- SPXI-aware: computes the Layer-3 SHA-256 hash of the canonical text and
  checks for Layer-1 anchors and Layer-2 kernels in the body. For external
  deposits (Sophia and beyond) this is READ-ONLY: we measure, don't inscribe.

Usage
-----
    enrich_deposit.py --deposit-number 937 --all
    enrich_deposit.py --deposit-number 937 --extract --spxi
    enrich_deposit.py --deposit-number 937 --backlinks

Called from the mint-axn.yml workflow after mint step, before commit step.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# --- constants -------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
REGISTRY = REPO_ROOT / "data" / "registry.json"
ENTITY_INDEX = REPO_ROOT / "data" / "entity-index.json"
EXTERNAL_METADATA_DIR = REPO_ROOT / "data" / "external-metadata"

CLAUDE_MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-6")
CLAUDE_API = "https://api.anthropic.com/v1/messages"
OPENALEX_API = "https://api.openalex.org/works"
WIKIDATA_SEARCH = "https://www.wikidata.org/w/api.php"
DATACITE_API = "https://api.datacite.org/dois"

# The tool-use schema that Claude must fill in. Enforces structured output.
EXTRACTION_TOOL = {
    "name": "record_deposit_enrichment",
    "description": (
        "Record structured enrichment metadata extracted from a Crimson "
        "Hexagonal Archive deposit. Fill in all four arrays; each may be "
        "empty if nothing of that kind is present."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "concepts": {
                "type": "array",
                "description": (
                    "5-25 distinctive concepts introduced, defined, or "
                    "load-bearingly named in this deposit. Prefer terms the "
                    "author coined or gave a technical sense; skip generic "
                    "vocabulary."
                ),
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": (
                                "Concept name, 3-60 chars, in the form the "
                                "text uses. Preserve capitalization, "
                                "punctuation, and any glyphs."
                            ),
                        },
                        "note": {
                            "type": "string",
                            "description": (
                                "One-sentence definitional statement "
                                "supported by the text. May be a direct "
                                "quotation OR a close paraphrase; do not "
                                "invent content."
                            ),
                        },
                        "context_quote": {
                            "type": "string",
                            "description": (
                                "Brief quotation (5-30 words) from the text "
                                "where this concept is introduced or "
                                "defined. Verbatim."
                            ),
                        },
                    },
                    "required": ["name", "note"],
                },
            },
            "citations": {
                "type": "array",
                "description": (
                    "All non-trivial references the deposit makes to other "
                    "works, persons, deposits, standards, or datasets. Extract "
                    "each once; if the same work is referenced multiple times, "
                    "extract it once with the most complete metadata. Do NOT "
                    "restrict to DOI-anchored works — capture books by title, "
                    "historical persons cited as intellectual lineage, blog "
                    "posts, standards documents, and prior CHA deposits."
                ),
                "items": {
                    "type": "object",
                    "properties": {
                        "type": {
                            "type": "string",
                            "enum": [
                                "book", "article", "chapter", "deposit",
                                "blog_post", "preprint", "dissertation",
                                "website", "standard", "dataset", "software",
                                "artwork", "manuscript", "correspondence",
                                "historical_person", "concept", "other",
                            ],
                        },
                        "text": {
                            "type": "string",
                            "description": (
                                "How the citation appears in the deposit — "
                                "the exact string, quotation, or descriptive "
                                "phrase. Verbatim."
                            ),
                        },
                        "authors": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Author names if stated. Empty array if unknown.",
                        },
                        "title": {
                            "type": "string",
                            "description": "Work title if stated. Omit if not stated.",
                        },
                        "year": {
                            "type": "integer",
                            "description": "Year if stated. Omit if not stated.",
                        },
                        "venue": {
                            "type": "string",
                            "description": "Journal, publisher, archive if stated.",
                        },
                        "doi": {
                            "type": "string",
                            "description": "DOI if present (bare, no https:// prefix).",
                        },
                        "url": {
                            "type": "string",
                            "description": "URL if given.",
                        },
                        "cha_axn": {
                            "type": "string",
                            "description": (
                                "AXN identifier (AXN:XXXX...) if the citation "
                                "unambiguously refers to a Crimson Hexagonal "
                                "Archive deposit and the AXN is identifiable "
                                "from the text or context."
                            ),
                        },
                        "wikidata_hint": {
                            "type": "string",
                            "description": (
                                "A search-friendly name string usable to look "
                                "this entity up in Wikidata. For persons: "
                                "given + surname. For works: title. For "
                                "concepts: canonical name."
                            ),
                        },
                        "role": {
                            "type": "string",
                            "description": (
                                "How the citation functions in the deposit's "
                                "argument. Examples: 'primary source', "
                                "'foundational reference', 'counterexample', "
                                "'intellectual lineage', 'contested claim', "
                                "'methodological precedent', 'companion work'."
                            ),
                        },
                    },
                    "required": ["type", "text"],
                },
            },
            "wikidata_candidates": {
                "type": "array",
                "description": (
                    "Named entities in the deposit that plausibly have a "
                    "Wikidata QID: persons (living or historical), works, "
                    "institutions, places, or well-established concepts. "
                    "Exclude the deposit's own novel concepts (those go in "
                    "the concepts array). Deduplicate."
                ),
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "type": {
                            "type": "string",
                            "enum": [
                                "person", "work", "organization", "place",
                                "concept", "event", "other",
                            ],
                        },
                        "context": {
                            "type": "string",
                            "description": "How this entity appears in the deposit.",
                        },
                        "search_query": {
                            "type": "string",
                            "description": (
                                "Precise text to use for Wikidata search. "
                                "For ambiguous names, include disambiguating "
                                "context (e.g., 'Sappho of Lesbos', 'John "
                                "Cage composer')."
                            ),
                        },
                    },
                    "required": ["name", "type", "search_query"],
                },
            },
            "cha_cross_references": {
                "type": "array",
                "description": (
                    "Prior Crimson Hexagonal Archive deposits or MANUS works "
                    "that this deposit references, extends, verifies, or "
                    "responds to. Extract only where the reference is clear "
                    "from the text. This populates the SPXI Layer 4 "
                    "cross-signing graph."
                ),
                "items": {
                    "type": "object",
                    "properties": {
                        "referenced_axn_or_title": {
                            "type": "string",
                            "description": (
                                "AXN identifier if identifiable, otherwise "
                                "the best-guess title of the referenced work."
                            ),
                        },
                        "reference_type": {
                            "type": "string",
                            "enum": [
                                "cites", "verifies", "extends", "responds_to",
                                "contrasts", "supersedes", "companion",
                            ],
                        },
                        "context": {
                            "type": "string",
                            "description": "Brief note on how this reference works.",
                        },
                    },
                    "required": ["referenced_axn_or_title", "reference_type"],
                },
            },
        },
        "required": [
            "concepts", "citations", "wikidata_candidates",
            "cha_cross_references",
        ],
    },
}


# --- utility helpers ------------------------------------------------------


def _log(msg: str, *, prefix: str = "enrich") -> None:
    print(f"[{prefix}] {msg}", flush=True)


def _http_get_json(
    url: str,
    params: dict[str, str] | None = None,
    *,
    timeout: int = 15,
    headers: dict[str, str] | None = None,
) -> Any:
    if params:
        url = f"{url}?{urllib.parse.urlencode(params)}"
    req_headers = {
        "User-Agent": (
            "Alexanarch-Enrichment/1.0 "
            "(https://alexanarch.org; contact via ORCID 0009-0000-1599-0703)"
        ),
        "Accept": "application/json",
    }
    if headers:
        req_headers.update(headers)
    req = urllib.request.Request(url, headers=req_headers)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def _load_registry() -> dict:
    with open(REGISTRY) as f:
        return json.load(f)


def _save_registry(reg: dict) -> None:
    with open(REGISTRY, "w") as f:
        json.dump(reg, f, indent=2, ensure_ascii=False)
        f.write("\n")


def _find_deposit(reg: dict, deposit_number: int) -> dict:
    for d in reg["deposits"]:
        if d.get("deposit_number") == deposit_number:
            return d
    raise KeyError(f"deposit #{deposit_number} not found in registry")


def _text_path(deposit: dict) -> Path:
    hex_id = deposit["hex"]
    return REPO_ROOT / "data" / "texts" / f"AXN-{hex_id}-text.md"


def _load_text(deposit: dict) -> str:
    path = _text_path(deposit)
    if not path.exists():
        _log(f"WARNING: text file missing at {path}")
        return ""
    return path.read_text(encoding="utf-8")


def _text_body_only(text: str) -> str:
    """Return the deposit body with YAML front-matter stripped, if present."""
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            return text[end + 5:]
    return text


def _word_count(text: str) -> int:
    body = _text_body_only(text)
    body = re.sub(r"```[^`]*```", "", body, flags=re.S)  # strip code blocks
    body = re.sub(r"<[^>]+>", "", body)  # strip html tags
    return len(re.findall(r"\S+", body))


def _canonical_hash(text: str) -> str:
    """
    Per SPXI Protocol v0.2 Layer 3: SHA-256 of the canonical body text,
    normalized to UTF-8 with LF line endings, with front-matter stripped.
    """
    body = _text_body_only(text).encode("utf-8").replace(b"\r\n", b"\n")
    return hashlib.sha256(body).hexdigest()


# --- LLM extraction step --------------------------------------------------


EXTRACTION_SYSTEM_PROMPT = """You are the enrichment analyst for the Crimson \
Hexagonal Archive (CHA), a scholarly self-governing static archive at \
alexanarch.org. You extract structured metadata from newly deposited \
scholarly works, populating four arrays: concepts (novel terms the deposit \
introduces or defines), citations (references to any prior work — books, \
articles, deposits, standards, historical persons, not just DOI-anchored \
sources), wikidata_candidates (external entities that plausibly have \
Wikidata QIDs), and cha_cross_references (prior CHA deposits this work \
engages).

Rules of practice:
- Extract only what the text supports. Do not invent authors, years, DOIs, \
titles, or claims.
- For citations, do NOT limit to DOI-anchored works. A citation to \
"Sappho's fragments" or "Marx's Capital, Volume I" or "the Berners-Lee \
originator critique" is a citation. Capture how it appears.
- Concepts should be things the deposit *introduces or defines*, not \
general vocabulary the deposit merely uses. Prefer distinctive multi-word \
terms, proper names of frameworks, and coined technical vocabulary.
- Wikidata candidates are for LOOKUP later — you don't need to know the \
QID, you need to give a good search string.
- CHA cross-references populate the SPXI Layer 4 cross-signing graph. Only \
include references that are clear from the text.

Always fill in the record_deposit_enrichment tool. Never produce output \
outside the tool call."""


def extract_via_llm(deposit: dict, text: str, *, api_key: str) -> dict:
    body = _text_body_only(text)
    # TRUNCATION NOTE: the 60K-char cap below applies ONLY to what Claude
    # sees as input for the extraction transform. The deposit's canonical
    # text file at data/texts/AXN-XXXX-text.md is UNTOUCHED and remains the
    # authoritative artifact, canonically hashed at its full length for
    # SPXI Layer 3. The truncation exists solely to bound the LLM's
    # reasoning scope for enrichment; it does not affect the deposit itself,
    # its content, its hash, its public rendering, or its downstream
    # readability. Long deposits still get enriched, just not from their
    # tail. Longer papers may warrant a two-pass extraction (head + tail)
    # in a future revision, but for the current scope 60K covers even a
    # 15-16K-word scholarly paper.
    if len(body) > 60000:
        body = body[:60000] + "\n\n[... TEXT TRUNCATED AT 60000 CHARS FOR ENRICHMENT INPUT ONLY — DEPOSIT'S FULL TEXT IS UNCHANGED ...]"

    user_message = (
        f"Deposit metadata:\n"
        f"  Title: {deposit.get('title', '')}\n"
        f"  Creator: {deposit.get('creator', '')}\n"
        f"  Date: {deposit.get('date', '')}\n"
        f"  Content type: {deposit.get('content_type', '')}\n"
        f"  Family: {deposit.get('family', '')}\n"
        f"  Description: {deposit.get('description', '')[:500]}\n\n"
        f"---\n\nDeposit text:\n\n{body}\n\n---\n\n"
        f"Extract enrichment metadata by calling the "
        f"record_deposit_enrichment tool. Use empty arrays for categories "
        f"with no relevant content."
    )

    payload = {
        "model": CLAUDE_MODEL,
        "max_tokens": 8000,
        "system": EXTRACTION_SYSTEM_PROMPT,
        "tools": [EXTRACTION_TOOL],
        "tool_choice": {
            "type": "tool",
            "name": "record_deposit_enrichment",
        },
        "messages": [
            {"role": "user", "content": user_message},
        ],
    }

    req = urllib.request.Request(
        CLAUDE_API,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "content-type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
        },
    )
    _log(f"calling Claude {CLAUDE_MODEL} for extraction (~{len(body)//4} input tokens)")
    with urllib.request.urlopen(req, timeout=120) as r:
        resp = json.load(r)

    # find the tool_use block
    for block in resp.get("content", []):
        if block.get("type") == "tool_use" and block.get("name") == EXTRACTION_TOOL["name"]:
            usage = resp.get("usage", {})
            _log(
                f"extracted concepts={len(block['input'].get('concepts', []))}, "
                f"citations={len(block['input'].get('citations', []))}, "
                f"wikidata_candidates={len(block['input'].get('wikidata_candidates', []))}, "
                f"cha_xrefs={len(block['input'].get('cha_cross_references', []))} "
                f"(usage: {usage.get('input_tokens')}in / {usage.get('output_tokens')}out)"
            )
            return block["input"]
    raise RuntimeError(
        "Claude did not return a record_deposit_enrichment tool call; "
        f"got content types: {[b.get('type') for b in resp.get('content', [])]}"
    )


# --- Wikidata resolution --------------------------------------------------


def _wikidata_search(query: str, *, limit: int = 3) -> list[dict]:
    """Return the top Wikidata matches for a search string."""
    try:
        data = _http_get_json(
            WIKIDATA_SEARCH,
            {
                "action": "wbsearchentities",
                "search": query,
                "language": "en",
                "format": "json",
                "limit": str(limit),
            },
        )
        return data.get("search", [])
    except (urllib.error.URLError, json.JSONDecodeError, TimeoutError) as e:
        _log(f"wikidata search failed for {query!r}: {e}")
        return []


def resolve_wikidata(candidates: list[dict]) -> list[dict]:
    """Add wikidata_qid to each candidate where a plausible match exists.

    A "plausible match" is when the top result's label is a case-insensitive
    match, or contains the candidate name as a substring. We are conservative:
    we do not want to spuriously assign QIDs.
    """
    resolved = []
    for c in candidates:
        query = c.get("search_query") or c.get("name", "")
        if not query:
            continue
        matches = _wikidata_search(query)
        time.sleep(0.1)  # be polite to Wikidata
        chosen = None
        cname_lower = c.get("name", "").lower().strip()
        for m in matches:
            label = m.get("label", "").lower().strip()
            if not label:
                continue
            if label == cname_lower or cname_lower in label or label in cname_lower:
                chosen = m
                break
        entry = dict(c)
        if chosen:
            entry["wikidata_qid"] = chosen.get("id")
            entry["wikidata_label"] = chosen.get("label")
            entry["wikidata_description"] = chosen.get("description", "")
            entry["wikidata_url"] = chosen.get("concepturi") or (
                f"https://www.wikidata.org/wiki/{chosen.get('id')}" if chosen.get("id") else ""
            )
            entry["resolution"] = "confident"
        elif matches:
            # keep top candidate but mark as tentative
            top = matches[0]
            entry["wikidata_qid_candidate"] = top.get("id")
            entry["wikidata_label_candidate"] = top.get("label")
            entry["wikidata_description_candidate"] = top.get("description", "")
            entry["resolution"] = "tentative"
        else:
            entry["resolution"] = "unresolved"
        resolved.append(entry)
    return resolved


# --- OpenAlex enrichment --------------------------------------------------


def fetch_openalex(deposit: dict, citations: list[dict]) -> dict:
    """Look up the deposit itself in OpenAlex + cited works, return ids.

    Returns dict with:
      - openalex_ids_for_deposit: list of OpenAlex work IDs matching deposit title/creator
      - openalex_ids_for_citations: dict mapping citation index -> OpenAlex ID
    """
    result: dict[str, Any] = {
        "openalex_ids_for_deposit": [],
        "openalex_ids_for_citations": {},
    }
    title = deposit.get("title", "")
    if title:
        try:
            data = _http_get_json(
                OPENALEX_API,
                {"search": title[:200], "per_page": "5"},
                headers={"User-Agent": "Alexanarch-Enrichment/1.0 (mailto:hello@alexanarch.org)"},
            )
            for w in data.get("results", []):
                result["openalex_ids_for_deposit"].append(w.get("id"))
        except (urllib.error.URLError, json.JSONDecodeError, TimeoutError) as e:
            _log(f"openalex deposit search failed: {e}")

    for i, cit in enumerate(citations):
        cit_title = cit.get("title")
        cit_doi = cit.get("doi")
        if cit_doi:
            # Direct DOI resolution
            try:
                data = _http_get_json(
                    f"{OPENALEX_API}/https://doi.org/{cit_doi.lstrip('doi.org/').lstrip('https://').lstrip('http://').replace('doi.org/', '')}",
                    headers={"User-Agent": "Alexanarch-Enrichment/1.0"},
                )
                if data.get("id"):
                    result["openalex_ids_for_citations"][str(i)] = data["id"]
                    continue
            except (urllib.error.URLError, json.JSONDecodeError, TimeoutError):
                pass
        if cit_title and len(cit_title) > 10:
            try:
                data = _http_get_json(
                    OPENALEX_API,
                    {"search": cit_title[:200], "per_page": "1"},
                )
                if data.get("results"):
                    result["openalex_ids_for_citations"][str(i)] = data["results"][0].get("id")
            except (urllib.error.URLError, json.JSONDecodeError, TimeoutError):
                pass
        time.sleep(0.1)  # polite pacing

    _log(
        f"openalex: {len(result['openalex_ids_for_deposit'])} deposit matches, "
        f"{len(result['openalex_ids_for_citations'])} citation matches"
    )
    return result


# --- DataCite severance check --------------------------------------------


def check_datacite_severance(citations: list[dict]) -> dict:
    """For each cited DOI, check DataCite existence.

    Returns dict {"severed_dois": [...], "live_dois": [...]}. Zenodo DOIs
    that 404 at DataCite indicate the deposit was terminated (like the CHA
    tombstones).
    """
    result = {"severed_dois": [], "live_dois": [], "unchecked": []}
    for cit in citations:
        doi = cit.get("doi")
        if not doi:
            continue
        # normalize
        doi_clean = doi.replace("https://doi.org/", "").replace("doi:", "").strip()
        if not doi_clean:
            continue
        try:
            resp = urllib.request.urlopen(
                urllib.request.Request(
                    f"{DATACITE_API}/{urllib.parse.quote(doi_clean, safe='/')}",
                    headers={"Accept": "application/vnd.api+json"},
                ),
                timeout=10,
            )
            if resp.status == 200:
                result["live_dois"].append(doi_clean)
            else:
                result["severed_dois"].append(doi_clean)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                result["severed_dois"].append(doi_clean)
            else:
                result["unchecked"].append(doi_clean)
        except (urllib.error.URLError, TimeoutError):
            result["unchecked"].append(doi_clean)
        time.sleep(0.05)
    _log(
        f"datacite: {len(result['live_dois'])} live, "
        f"{len(result['severed_dois'])} severed, "
        f"{len(result['unchecked'])} unchecked"
    )
    return result


# --- SPXI validation ------------------------------------------------------


def validate_spxi(deposit: dict, text: str) -> dict:
    """Audit deposit against SPXI Protocol v0.2 five layers.

    Layer 1: Visible body-text inscription anchors
             (sentences naming operator/ORCID/deposit in prose)
    Layer 2: Distributed micro-kernels (fenced JSON code blocks)
    Layer 3: SHA-256 content hash (registered here + optionally in body)
    Layer 4: Reciprocal cross-signing graph (spxi:verifies via cross-refs)
    Layer 5: External authority anchoring (Wikidata/ORCID/DOI presence)
    """
    body = _text_body_only(text)

    # Layer 1: look for prose inscription anchors. SPXI v0.2 §2 specifies
    # anchors as sentences that name operator, ORCID, deposit identifier, and
    # authorial position. We measure presence of ANY of these anchor types
    # and treat Layer 1 as PRESENT when three or more distinct anchor kinds
    # appear in body prose (heuristic: three-of-N provides robustness against
    # aggressive paraphrase while remaining strict enough to be meaningful).
    orcid = deposit.get("orcid", "")
    creator = deposit.get("creator", "")
    axn = deposit.get("axn", "") or ""
    axn_prefix = axn.split(".", 1)[0] if axn else ""  # e.g. "AXN:03B4"
    hex_id = deposit.get("hex", "")
    hex_anchor = f"AXN:{hex_id}" if hex_id else ""
    sovereign_id = deposit.get("sovereign_id", "")
    date = deposit.get("date", "")
    deposit_num = deposit.get("deposit_number")
    dep_num_phrase = f"deposit #{deposit_num}" if deposit_num else ""

    layer_1_anchors_found = []
    if orcid and orcid in body:
        layer_1_anchors_found.append("orcid")
    if creator and creator in body:
        layer_1_anchors_found.append("creator_name")
    if axn_prefix and axn_prefix in body:
        layer_1_anchors_found.append("axn_prefix")
    if hex_anchor and hex_anchor in body and hex_anchor != axn_prefix:
        layer_1_anchors_found.append("axn_hex")
    if sovereign_id and sovereign_id in body:
        layer_1_anchors_found.append("sovereign_id")
    if date and date in body:
        layer_1_anchors_found.append("date")
    if dep_num_phrase and dep_num_phrase in body:
        layer_1_anchors_found.append("deposit_number_phrase")
    # authorial-position phrase (e.g., "in the SPXI Protocol authorial
    # position", "operating in the ... authorial position")
    if re.search(r"authorial position\b|MANUS\b|operating as\b", body, flags=re.I):
        layer_1_anchors_found.append("authorial_position_phrase")

    orcid_in_body = "orcid" in layer_1_anchors_found
    creator_in_body = "creator_name" in layer_1_anchors_found
    layer_1_present = len(layer_1_anchors_found) >= 3

    # Layer 2: fenced JSON code blocks (roughly)
    fenced_json_blocks = len(re.findall(r"```\s*json\s*\n", body, flags=re.I))
    fenced_json_ld = body.count('"@context"') + body.count("'@context'")
    layer_2_present = fenced_json_blocks >= 1 or fenced_json_ld >= 1

    # Layer 3: hash
    canonical_hash = _canonical_hash(text)
    hash_in_body = canonical_hash in body

    # Layer 4: cross-references (populated separately by enrichment)
    # We report count only; presence is measured after enrichment fills them
    cross_refs = deposit.get("cha_cross_references") or []
    layer_4_present = len(cross_refs) > 0

    # Layer 5: external anchors
    wc = deposit.get("wikidata_candidates") or []
    wikidata_qid_count = sum(1 for c in wc if c.get("wikidata_qid"))
    external_dois = sum(
        1 for cit in (deposit.get("citations") or [])
        if cit.get("doi")
    )
    layer_5_present = (
        wikidata_qid_count > 0 or external_dois > 0 or bool(orcid)
    )

    return {
        "spxi_protocol": "v0.2",
        "validated_at": datetime.now(timezone.utc).isoformat(),
        "layers": {
            "layer_1_inscription_anchors": {
                "present": layer_1_present,
                "anchors_found": layer_1_anchors_found,
                "anchor_count": len(layer_1_anchors_found),
                "orcid_in_body": orcid_in_body,
                "creator_in_body": creator_in_body,
                "note": (
                    "Layer 1 present if at least 3 anchor types appear in "
                    "body prose. Anchor types include ORCID, creator name, "
                    "AXN string, hex identifier, sovereign_id, date, "
                    "deposit number phrase, and authorial-position phrase."
                ),
            },
            "layer_2_micro_kernels": {
                "present": layer_2_present,
                "fenced_json_blocks": fenced_json_blocks,
                "json_ld_context_markers": fenced_json_ld,
            },
            "layer_3_content_hash": {
                "present": True,
                "canonical_hash": canonical_hash,
                "hash_in_body": hash_in_body,
                "note": (
                    "Hash is always registered by mint. hash_in_body true "
                    "means the author inscribed a signature section."
                ),
            },
            "layer_4_cross_signing": {
                "present": layer_4_present,
                "cross_references_count": len(cross_refs),
                "note": (
                    "Populated by enrichment via cha_cross_references. "
                    "Prospective (this deposit → prior deposits) only; "
                    "retrospective cited_by updates on prior deposits."
                ),
            },
            "layer_5_external_anchors": {
                "present": layer_5_present,
                "wikidata_qid_count": wikidata_qid_count,
                "external_doi_count": external_dois,
                "orcid_present": bool(orcid),
            },
        },
        "overall_conformance": (
            "full" if all([layer_1_present, layer_2_present, layer_4_present, layer_5_present])
            else "partial" if any([layer_1_present, layer_2_present, layer_4_present, layer_5_present])
            else "measurement_only"
        ),
    }


# --- Wiki article assembly ------------------------------------------------


def build_wiki_article(deposit: dict, text: str, concepts: list[dict]) -> str:
    """Templated wiki article. Follows the existing CHA convention plus the
    AXN + deposit-number inscription that makes basic metadata retrievable
    when Sigil surfaces the wiki entry.

    Format:
      "[title]" is a [wordcount]-word [content_type] by [creator], dated
      [date]. It is registered as [AXN] (deposit #[N]) in the Crimson
      Hexagonal Archive under the [FAMILY] semantic family. [first two
      description sentences]. [concept summary if any].
    """
    title = deposit.get("title", "").strip()
    creator = deposit.get("creator", "").strip()
    date = deposit.get("date", "").strip()
    content_type = deposit.get("content_type", "").strip().lower() or "work"
    family = deposit.get("family", "UNCLASSIFIED")
    axn = deposit.get("axn", "").strip()
    axn_prefix = axn.split(".", 1)[0] if axn else ""  # AXN:XXXX
    deposit_number = deposit.get("deposit_number")
    wc = _word_count(text)
    desc = (deposit.get("description") or "").strip()

    # first ~2 sentences of description, capped at 400 chars
    if desc:
        desc_snippet = " ".join(re.split(r"(?<=[.!?])\s+", desc)[:2])[:400]
    else:
        desc_snippet = ""

    is_heteronym = creator in HETERONYMS
    creator_phrase = (
        f"{creator}, a heteronym within the Dodecad system of the Crimson "
        f"Hexagonal Archive"
        if is_heteronym else creator
    )

    parts = [
        f'"{title}" is a {wc:,}-word {content_type} by {creator_phrase}, '
        f'dated {date}.'
    ]
    # AXN + deposit number inscription anchor
    if axn_prefix and deposit_number:
        parts.append(
            f"It is registered as {axn_prefix} (deposit #{deposit_number}) "
            f"in the Crimson Hexagonal Archive under the {family} "
            f"semantic family."
        )
    elif axn_prefix:
        parts.append(
            f"It is registered as {axn_prefix} in the Crimson Hexagonal "
            f"Archive under the {family} semantic family."
        )
    else:
        parts.append(
            f"The work is classified under the {family} semantic family "
            f"within the Crimson Hexagonal Archive."
        )
    if desc_snippet:
        parts.append(desc_snippet)
    if concepts:
        top_names = [c["name"] for c in concepts[:5] if c.get("name")]
        if top_names:
            parts.append(
                "The work introduces or engages "
                + ", ".join(f'"{n}"' for n in top_names[:-1])
                + (f', and "{top_names[-1]}"' if len(top_names) > 1 else f'"{top_names[0]}"')
                + " among its central concepts."
            )
    return " ".join(parts)


# --- Entity assembly (schema-conforming for the registry) ------------------


HETERONYMS = {
    "Johannes Sigil", "Rex Fraction", "Ayanna Vox", "Damascus Dancings",
    "Rebekah Cranes", "Talos Morrow", "Ichabod Spellings", "Nobel Glas",
    "Dr. Orin Trace", "Sparrow Wells", "Sen Kuro", "Jack Feist",
    "TACHYON", "TACHYON (Claude/Anthropic)",
}


def build_entities(deposit: dict, extraction: dict) -> tuple[list[dict], list[str]]:
    """Assemble the entities list and defines_concepts list.

    Follows the schema seen in existing registry entries:
      - base rows: created_by, is_type, belongs_to_family, is_part_of
      - heteronym reference rows for each heteronym name in text
      - minted_in rows for each extracted concept (with note field)
    """
    title = deposit.get("title", "")
    # keep the title short enough to match the existing convention
    title_short = title if len(title) <= 100 else title[:100]

    entities = [
        {
            "subject": title_short, "predicate": "created_by",
            "object": deposit.get("creator", ""),
            "type": "work", "evidence_status": "observed",
        },
        {
            "subject": title_short, "predicate": "is_type",
            "object": deposit.get("content_type", ""),
            "type": "work", "evidence_status": "observed",
        },
        {
            "subject": title_short, "predicate": "belongs_to_family",
            "object": deposit.get("family", "UNCLASSIFIED"),
            "type": "work", "evidence_status": "observed",
        },
        {
            "subject": title_short, "predicate": "is_part_of",
            "object": "Crimson Hexagonal Archive",
            "type": "work", "evidence_status": "observed",
        },
    ]

    # heteronym reference rows
    text_lower = deposit.get("description", "").lower()
    for h in HETERONYMS:
        if h.lower() in text_lower or h == deposit.get("creator"):
            if h != deposit.get("creator"):
                entities.append({
                    "subject": title_short, "predicate": "references",
                    "object": h, "type": "heteronym",
                    "evidence_status": "observed",
                })

    # concept minted_in rows
    defines_concepts: list[str] = []
    for c in extraction.get("concepts", []):
        cname = (c.get("name") or "").strip()
        if not cname:
            continue
        entities.append({
            "subject": cname,
            "predicate": "minted_in",
            "object": title_short,
            "type": "concept",
            "evidence_status": "observed",
            "note": (c.get("note") or c.get("context_quote") or "")[:400],
        })
        if cname not in defines_concepts:
            defines_concepts.append(cname)

    return entities, defines_concepts


def build_references_concepts(text: str) -> tuple[list[str], int]:
    """Lexical scan against the existing entity-index for known concepts.

    Cheap: no LLM. Just checks which existing archive concepts appear
    verbatim in this deposit's text.
    """
    if not ENTITY_INDEX.exists():
        return [], 0
    try:
        with open(ENTITY_INDEX) as f:
            idx = json.load(f)
    except (json.JSONDecodeError, OSError):
        return [], 0
    concepts = idx.get("concepts", {})
    body = _text_body_only(text)
    # Only consider concepts >=6 chars to avoid noise
    found = []
    for name in concepts:
        if len(name) < 6:
            continue
        # word-boundary match, case sensitive to avoid false positives
        pattern = r"\b" + re.escape(name) + r"\b"
        if re.search(pattern, body):
            found.append(name)
    return found, len(found)


# --- Cross-reference backlinks --------------------------------------------


def update_backlinks(deposit: dict, reg: dict, extraction: dict) -> int:
    """For each cha_cross_reference, add a cited_by entry on the referenced deposit.

    Returns number of deposits updated.
    """
    updated = 0
    my_axn = deposit.get("axn", "")
    my_number = deposit.get("deposit_number")
    citing_stub = {"deposit": my_number, "axn": my_axn}

    for xref in extraction.get("cha_cross_references", []):
        target = xref.get("referenced_axn_or_title", "").strip()
        if not target:
            continue
        # try AXN match first
        target_dep = None
        m = re.match(r"AXN:([0-9A-Fa-f]{2,4})", target)
        if m:
            target_hex = m.group(1).upper().zfill(4)
            for d in reg["deposits"]:
                if d.get("hex", "").upper() == target_hex:
                    target_dep = d
                    break
        # try title match as fallback
        if target_dep is None:
            target_lower = target.lower().strip()
            for d in reg["deposits"]:
                if d.get("deposit_number") == my_number:
                    continue
                d_title = d.get("title", "").lower()
                # substantial substring match
                if len(target_lower) > 15 and target_lower[:60] in d_title:
                    target_dep = d
                    break
        if target_dep is None:
            continue
        # append to cited_by
        cited_by = target_dep.setdefault("cited_by", [])
        if not any(c.get("deposit") == my_number for c in cited_by):
            cited_by.append(citing_stub)
            updated += 1
    return updated


# --- External metadata sidecar (fresh deposits, not recovery) --------------


def write_external_metadata_sidecar(
    deposit: dict, wikidata_resolved: list[dict],
    openalex: dict, datacite: dict, extraction: dict,
) -> Path:
    """Write per-deposit external metadata sidecar."""
    EXTERNAL_METADATA_DIR.mkdir(parents=True, exist_ok=True)
    path = EXTERNAL_METADATA_DIR / f"AXN-{deposit['hex']}.json"

    sidecar = {
        "@context": "https://schema.org",
        "@type": "Dataset",
        "axn": deposit.get("axn"),
        "deposit_number": deposit.get("deposit_number"),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "schema_version": "2.0",
        "purpose": (
            "Per-deposit external-metadata sidecar for a fresh alexanarch "
            "deposit. Contains OpenAlex work IDs for the deposit itself and "
            "for its cited works; Wikidata QIDs for external entities named "
            "in the deposit; DataCite severance status for cited DOIs. "
            "Complements the registry.json entry, which holds the core "
            "concepts/citations/entities. Generated by enrich_deposit.py."
        ),
        "openalex": {
            "deposit_work_matches": openalex.get("openalex_ids_for_deposit", []),
            "cited_work_ids_by_citation_index": openalex.get("openalex_ids_for_citations", {}),
        },
        "wikidata": {
            "resolved_entities": [
                {
                    "name": c.get("name"),
                    "qid": c.get("wikidata_qid") or c.get("wikidata_qid_candidate"),
                    "label": c.get("wikidata_label") or c.get("wikidata_label_candidate"),
                    "description": (
                        c.get("wikidata_description") or c.get("wikidata_description_candidate", "")
                    ),
                    "url": c.get("wikidata_url", ""),
                    "resolution": c.get("resolution"),
                }
                for c in wikidata_resolved
                if c.get("resolution") in ("confident", "tentative")
            ],
        },
        "datacite_severance": {
            "live_dois": datacite.get("live_dois", []),
            "severed_dois": datacite.get("severed_dois", []),
            "unchecked_dois": datacite.get("unchecked", []),
        },
        "citations_summary": {
            "total": len(extraction.get("citations", [])),
            "by_type": _count_by_field(extraction.get("citations", []), "type"),
        },
    }
    path.write_text(json.dumps(sidecar, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def _count_by_field(items: list[dict], field: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for i in items:
        k = i.get(field, "unknown") or "unknown"
        counts[k] = counts.get(k, 0) + 1
    return counts


# --- Main orchestration ---------------------------------------------------


def enrich(
    deposit_number: int, *,
    do_extract: bool = True,
    do_wikidata: bool = True,
    do_openalex: bool = True,
    do_datacite: bool = True,
    do_spxi: bool = True,
    do_backlinks: bool = True,
    api_key: str | None = None,
    dry_run: bool = False,
) -> dict:
    """Orchestrate enrichment. Returns receipt dict summarizing actions taken."""
    reg = _load_registry()
    deposit = _find_deposit(reg, deposit_number)
    text = _load_text(deposit)
    if not text:
        raise RuntimeError(f"deposit #{deposit_number} has no text file to enrich")

    receipt: dict[str, Any] = {
        "deposit_number": deposit_number,
        "axn": deposit.get("axn"),
        "hex": deposit.get("hex"),
        "title": deposit.get("title", "")[:120],
        "run_at": datetime.now(timezone.utc).isoformat(),
        "steps": {},
    }

    extraction: dict = {
        "concepts": [], "citations": [],
        "wikidata_candidates": [], "cha_cross_references": [],
    }

    # step 1: LLM extraction
    if do_extract:
        if not api_key:
            raise RuntimeError("ANTHROPIC_API_KEY required for --extract step")
        try:
            extraction = extract_via_llm(deposit, text, api_key=api_key)
            receipt["steps"]["extract"] = {
                "concepts": len(extraction["concepts"]),
                "citations": len(extraction["citations"]),
                "wikidata_candidates": len(extraction["wikidata_candidates"]),
                "cha_cross_references": len(extraction["cha_cross_references"]),
            }
        except Exception as e:  # noqa: BLE001
            _log(f"ERROR in extract step: {e}")
            receipt["steps"]["extract"] = {"error": str(e)}
    else:
        # load prior extraction from deposit if present
        extraction["citations"] = deposit.get("citations") or []
        extraction["cha_cross_references"] = deposit.get("cha_cross_references") or []
        # concepts must be re-derived from entities
        extraction["concepts"] = [
            {"name": e["subject"], "note": e.get("note", "")}
            for e in (deposit.get("entities") or [])
            if e.get("predicate") == "minted_in"
        ]
        extraction["wikidata_candidates"] = deposit.get("wikidata_candidates") or []

    # step 2: Wikidata resolution
    wikidata_resolved: list[dict] = []
    if do_wikidata and extraction["wikidata_candidates"]:
        wikidata_resolved = resolve_wikidata(extraction["wikidata_candidates"])
        confident = sum(1 for c in wikidata_resolved if c.get("resolution") == "confident")
        receipt["steps"]["wikidata"] = {
            "candidates": len(wikidata_resolved),
            "confident_qids": confident,
            "tentative_qids": sum(
                1 for c in wikidata_resolved if c.get("resolution") == "tentative"
            ),
        }
    else:
        wikidata_resolved = deposit.get("wikidata_candidates") or []
        receipt["steps"]["wikidata"] = {"skipped": True}

    # step 3: OpenAlex enrichment
    openalex_result: dict = {"openalex_ids_for_deposit": [], "openalex_ids_for_citations": {}}
    if do_openalex:
        openalex_result = fetch_openalex(deposit, extraction["citations"])
        receipt["steps"]["openalex"] = {
            "deposit_matches": len(openalex_result["openalex_ids_for_deposit"]),
            "citation_matches": len(openalex_result["openalex_ids_for_citations"]),
        }
    else:
        receipt["steps"]["openalex"] = {"skipped": True}

    # step 4: DataCite severance
    datacite_result: dict = {"live_dois": [], "severed_dois": [], "unchecked": []}
    if do_datacite:
        datacite_result = check_datacite_severance(extraction["citations"])
        receipt["steps"]["datacite"] = {
            "live": len(datacite_result["live_dois"]),
            "severed": len(datacite_result["severed_dois"]),
        }
    else:
        receipt["steps"]["datacite"] = {"skipped": True}

    # step 5: SPXI validation
    spxi_audit: dict = {}
    if do_spxi:
        spxi_audit = validate_spxi(deposit, text)
        receipt["steps"]["spxi"] = {
            "conformance": spxi_audit.get("overall_conformance"),
            "canonical_hash": spxi_audit["layers"]["layer_3_content_hash"]["canonical_hash"],
        }
    else:
        receipt["steps"]["spxi"] = {"skipped": True}

    # step 6: assemble registry fields
    entities, defines_concepts = build_entities(deposit, extraction)
    references_concepts, references_count = build_references_concepts(text)
    wiki_article = build_wiki_article(deposit, text, extraction.get("concepts", []))

    # step 7: apply to deposit
    if not dry_run:
        deposit["wiki_article"] = wiki_article
        deposit["entities"] = entities
        deposit["defines_concepts"] = defines_concepts
        deposit["references_concepts"] = references_concepts
        deposit["references_concept_count"] = references_count
        deposit["citations"] = extraction["citations"]
        deposit["wikidata_candidates"] = wikidata_resolved
        deposit["cha_cross_references"] = extraction["cha_cross_references"]
        if openalex_result["openalex_ids_for_deposit"]:
            deposit["openalex_ids"] = openalex_result["openalex_ids_for_deposit"]
        if datacite_result["severed_dois"] and not datacite_result["live_dois"]:
            deposit["datacite_severance"] = "severed"
        elif datacite_result["severed_dois"]:
            deposit["datacite_severance"] = "mixed"
        elif datacite_result["live_dois"]:
            deposit["datacite_severance"] = "intact"
        if spxi_audit:
            deposit["spxi_audit"] = spxi_audit
        # sidecar path (external metadata)
        sidecar_path = write_external_metadata_sidecar(
            deposit, wikidata_resolved, openalex_result, datacite_result, extraction,
        )
        deposit["external_metadata_path"] = f"/{sidecar_path.relative_to(REPO_ROOT)}"

    # step 8: backlinks
    backlinks_updated = 0
    if do_backlinks and not dry_run:
        backlinks_updated = update_backlinks(deposit, reg, extraction)
        receipt["steps"]["backlinks"] = {"deposits_backlinked": backlinks_updated}
    else:
        receipt["steps"]["backlinks"] = {"skipped": True}

    # step 9: save registry
    if not dry_run:
        _save_registry(reg)
        _log(f"saved registry with enrichment for AXN:{deposit['hex']} (#{deposit_number})")
    else:
        _log(f"DRY RUN: would have enriched AXN:{deposit['hex']} (#{deposit_number})")

    return receipt


# --- CLI ------------------------------------------------------------------


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--deposit-number", type=int, required=True)
    p.add_argument("--all", action="store_true", help="Run all enrichment steps")
    p.add_argument("--extract", action="store_true", help="LLM concept/citation extraction")
    p.add_argument("--wikidata", action="store_true")
    p.add_argument("--openalex", action="store_true")
    p.add_argument("--datacite", action="store_true")
    p.add_argument("--spxi", action="store_true")
    p.add_argument("--backlinks", action="store_true")
    p.add_argument("--dry-run", action="store_true", help="Compute but don't write")
    p.add_argument("--receipt-path", type=str, default=None, help="Write receipt JSON here")
    args = p.parse_args()

    do_all = args.all or not any([
        args.extract, args.wikidata, args.openalex, args.datacite,
        args.spxi, args.backlinks,
    ])

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    do_extract = do_all or args.extract

    if do_extract and not api_key:
        _log(
            "ERROR: ANTHROPIC_API_KEY not set. Extraction requires it. "
            "Set the env var or pass individual --spxi/--openalex/--wikidata "
            "steps that don't need Claude."
        )
        return 1

    try:
        receipt = enrich(
            args.deposit_number,
            do_extract=do_extract,
            do_wikidata=do_all or args.wikidata,
            do_openalex=do_all or args.openalex,
            do_datacite=do_all or args.datacite,
            do_spxi=do_all or args.spxi,
            do_backlinks=do_all or args.backlinks,
            api_key=api_key,
            dry_run=args.dry_run,
        )
    except Exception as e:  # noqa: BLE001
        _log(f"FATAL: {e}")
        return 2

    if args.receipt_path:
        Path(args.receipt_path).write_text(json.dumps(receipt, indent=2) + "\n")

    print(json.dumps(receipt, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
