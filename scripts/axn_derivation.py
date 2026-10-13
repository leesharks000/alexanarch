#!/usr/bin/env python3
"""axn_derivation.py — how a record's AXN may be described, read from its own fields.

AXN protocol v2.2 (2026-10-13, MANUS ruling "lets go ahead and adopt the solution for those batched axns")
records three independent dimensions on a record:

    mint_derivation   the stored hash, the recipe, whether the input was retained, and whether the
                      derivation verifies against bytes the archive holds
    founding_event    the dated event under which the AXN was established (for the 2026-06-20 batch:
                      the assignment that followed the 19 June deletion, with MANUS's attestation)
    manifestations    the bytes the record has held, in order, each with SHA-256 and computed SWHID;
                      the full chain lives in data/axn-derivation-ledger.json

A surface that says "content-derived" of a record whose mint input was not retained says more than
the record holds. Every renderer that describes a single record's AXN asks this module instead.
Records without `mint_derivation` keep the existing wording unchanged.
"""

STATUS_VERIFIES_SERVED = "verifies_against_served_bytes"
STATUS_VERIFIES_RETAINED = "verifies_against_retained_bytes"
STATUS_UNRETAINED = "unverified_input_not_retained"


def _current(d):
    m = d.get("manifestations") or {}
    return m.get("current") or {}


def swhid(d):
    """Computed content SWHID of the bytes the record serves now, or None."""
    return _current(d).get("swhid")


def short_phrase(d):
    """Plain-text clause describing the AXN, for HTML and JSON-LD descriptions."""
    md = d.get("mint_derivation")
    if not md:
        return "content-derived"
    st = md.get("status")
    fe = d.get("founding_event") or {}
    if st == STATUS_UNRETAINED:
        when = fe.get("date") or "at mint"
        return (f"established {when} in the batch assignment that followed the 2026-06-19 deletion; "
                f"the mint input was not retained, so the derivation cannot be re-checked; "
                f"byte identity is carried by the served bytes' SHA-256 and SWHID")
    if st == STATUS_VERIFIES_RETAINED:
        return ("content-derived from bytes this archive retains (an earlier manifestation); "
                "the served bytes have changed since and carry their own SHA-256 and SWHID")
    return "content-derived; verifies against the served bytes"


def ld_description(d):
    return f"authoritative identifier; {short_phrase(d)}; resolves"


def html_bytes_line(d, esc):
    """Second line for the identifier block: the served bytes' SHA-256 and SWHID, if recorded."""
    cur = _current(d)
    if not cur.get("sha256"):
        return ""
    sw = cur.get("swhid") or ""
    sw_html = (f' · SWHID <a href="https://archive.softwareheritage.org/{esc(sw)}" '
               f'style="color:var(--accent);font-family:var(--mono);font-size:.85em">{esc(sw)}</a>'
               if sw and cur.get("swh_known") else
               (f' · SWHID <span style="font-family:var(--mono);font-size:.85em">{esc(sw)}</span> (computed)' if sw else ''))
    return (f'<div><span style="color:#555">Served bytes</span> SHA-256 '
            f'<span style="font-family:var(--mono);font-size:.85em">{esc(cur["sha256"])}</span>{sw_html}. '
            f'Derivation and manifestation history: <a href="/data/axn-derivation-ledger.json" '
            f'style="color:var(--accent)">AXN derivation ledger</a>.</div>')


def ld_swhid_property(d):
    sw = swhid(d)
    if not sw:
        return None
    known = _current(d).get("swh_known")
    p = {"@type": "PropertyValue", "propertyID": "SWHID", "value": sw,
         "description": ("intrinsic identifier of the bytes this record serves; held by Software Heritage as checked "
                         + str(_current(d).get("swh_checked") or "")) if known else
                        "intrinsic identifier of the bytes this record serves; computed, Software Heritage retention not confirmed"}
    if known:
        p["url"] = f"https://archive.softwareheritage.org/{sw}"
    return p
