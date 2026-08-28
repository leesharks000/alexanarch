#!/usr/bin/env python3
"""audit_protocol_surfaces.py — the XML half of the sense organ.

WHY THIS EXISTS

scripts/audit_static_namespace.py --live watches the JSON surfaces, and it was
written because on 2026-07-31 a single added api/oai.js turned the root api/
directory into Vercel's functions namespace and took 1,012 static JSON files
dark for six days while every local check passed.

That guardian is JSON-specific. It requires a JSON content-type and a parseable
JSON body, which means it is structurally incapable of watching the archive's
two most standards-conventional harvesting surfaces:

    /oai              OAI-PMH, the endpoint an aggregator actually harvests
    .well-known/resourcesync + the capability chain
    sitemap.xml, sitemap-axn.xml
    feed.xml

Those can break — wrong content-type, HTML error page at 200, a resumption
token that does not resume, a capability list pointing at a 404 — while the
JSON guardian stays green. The archive would then be advertising a harvesting
interface that no harvester can use, and would not know.

WHAT THIS CHECKS

Not merely that a URL answers. For each surface, the thing that would actually
be true if it worked:

  OAI Identify            parses as XML, is an OAI-PMH response, carries
                          repositoryName and the declared deletedRecord policy
  ListMetadataFormats     advertises oai_dc
  ListIdentifiers         returns headers AND a resumptionToken, then the token
                          is SPENT — a token that does not resume is worse than
                          no token, because a harvester will follow it
  GetRecord               a known identifier returns that identifier's record
  Illegal argument        a bad verb returns an OAI error element, not a 500
                          and not a 200 of nonsense
  ResourceSync            source description -> capability list -> resource list,
                          each fetched and parsed, the chain walked rather than
                          assumed
  sitemaps                parse as XML and contain <url> or <sitemap> entries
  feed                    parses as XML and carries entries

USAGE
    python3 scripts/audit_protocol_surfaces.py            # live, production
    python3 scripts/audit_protocol_surfaces.py --base URL # against a preview
    python3 scripts/audit_protocol_surfaces.py --quiet    # only failures

Exit 0 if every surface holds, 1 otherwise. Intended to run beside the JSON
guardian in .github/workflows/endpoint-guardian.yml.
"""
import argparse, sys, urllib.request, urllib.error, urllib.parse
import xml.etree.ElementTree as ET

BASE = "https://www.alexanarch.org"
OAI_NS = "{http://www.openarchives.org/OAI/2.0/}"
RS_NS = "{http://www.openarchives.org/rs/terms/}"
SM_NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
ATOM_NS = "{http://www.w3.org/2005/Atom}"
UA = "alexanarch-protocol-guardian"


def fetch(url, timeout=45):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.headers.get("Content-Type") or "", r.read()


def xml_of(url):
    """Fetch and parse. Returns (root, note). Raises on anything a harvester
    would choke on — including HTML served at 200, which is the shape of the
    failure this whole apparatus exists for."""
    ct, raw = fetch(url)
    body = raw.decode("utf-8", "replace")
    if "<html" in body[:400].lower():
        raise ValueError(f"HTML body served for an XML surface "
                         f"(content-type '{ct}') — a rewrite is misrouting")
    return ET.fromstring(raw), f"{len(raw):,} bytes, {ct.split(';')[0] or 'no content-type'}"


def check(name, fn, fails, oks, quiet):
    try:
        note = fn()
        oks.append(f"{name} — {note}")
        if not quiet:
            print(f"  ok    {name} — {note}")
    except Exception as e:
        msg = f"{name} — {type(e).__name__}: {e}"
        fails.append(msg)
        print(f"  FAIL  {msg}")


def oai_checks(base, fails, oks, quiet):
    oai = base + "/oai"

    def identify():
        root, note = xml_of(oai + "?verb=Identify")
        if not root.tag.endswith("OAI-PMH"):
            raise ValueError(f"root element is {root.tag}, not OAI-PMH")
        idn = root.find(f"{OAI_NS}Identify")
        if idn is None:
            raise ValueError("no <Identify> element")
        rn = idn.findtext(f"{OAI_NS}repositoryName")
        dr = idn.findtext(f"{OAI_NS}deletedRecord")
        if not rn:
            raise ValueError("Identify carries no repositoryName")
        if dr != "persistent":
            raise ValueError(f"deletedRecord is '{dr}'; the archive declares "
                             f"'persistent' and its deletion semantics depend on it")
        return f"{rn}, deletedRecord={dr}, {note}"

    def formats():
        root, note = xml_of(oai + "?verb=ListMetadataFormats")
        pfx = [e.text for e in root.iter(f"{OAI_NS}metadataPrefix")]
        if "oai_dc" not in pfx:
            raise ValueError(f"oai_dc not advertised; got {pfx}")
        return f"formats={pfx}, {note}"

    def listids_and_resume():
        root, note = xml_of(oai + "?verb=ListIdentifiers&metadataPrefix=oai_dc")
        heads = root.findall(f".//{OAI_NS}header")
        if not heads:
            raise ValueError("no headers returned")
        tok_el = root.find(f".//{OAI_NS}resumptionToken")
        if tok_el is None or not (tok_el.text or "").strip():
            return f"{len(heads)} headers, no token (corpus fits one page), {note}"
        tok = tok_el.text.strip()
        # A token that does not resume is worse than no token: a harvester
        # follows it and loses the rest of the corpus silently.
        root2, note2 = xml_of(f"{oai}?verb=ListIdentifiers&resumptionToken="
                              + urllib.parse.quote(tok))
        err = root2.find(f"{OAI_NS}error")
        if err is not None:
            raise ValueError(f"resumptionToken rejected on replay: "
                             f"{err.get('code')} {err.text}")
        heads2 = root2.findall(f".//{OAI_NS}header")
        if not heads2:
            raise ValueError("resumptionToken resolved but returned no headers")
        return f"page1={len(heads)} headers, token spent -> page2={len(heads2)}, {note}"

    def getrecord():
        root, note = xml_of(oai + "?verb=ListIdentifiers&metadataPrefix=oai_dc")
        ident = root.findtext(f".//{OAI_NS}header/{OAI_NS}identifier")
        if not ident:
            raise ValueError("could not obtain an identifier to test GetRecord")
        r2, note2 = xml_of(f"{oai}?verb=GetRecord&metadataPrefix=oai_dc"
                           f"&identifier={urllib.parse.quote(ident)}")
        got = r2.findtext(f".//{OAI_NS}header/{OAI_NS}identifier")
        if got != ident:
            raise ValueError(f"asked for {ident}, received {got}")
        return f"{ident} round-trips, {note2}"

    def bad_verb():
        # A hostile validator sends nonsense. The contract is an OAI <error>,
        # not a 500 and not a cheerful 200.
        try:
            root, note = xml_of(oai + "?verb=NoSuchVerb")
        except urllib.error.HTTPError as e:
            if e.code >= 500:
                raise ValueError(f"HTTP {e.code} on an illegal verb; OAI requires "
                                 f"an <error code='badVerb'> response")
            raise
        err = root.find(f"{OAI_NS}error")
        if err is None:
            raise ValueError("illegal verb did not produce an <error> element")
        if err.get("code") != "badVerb":
            raise ValueError(f"error code is '{err.get('code')}', expected badVerb")
        return f"badVerb returned correctly, {note}"

    for n, f in (("OAI Identify", identify),
                 ("OAI ListMetadataFormats", formats),
                 ("OAI ListIdentifiers + resumptionToken", listids_and_resume),
                 ("OAI GetRecord round-trip", getrecord),
                 ("OAI illegal verb -> badVerb", bad_verb)):
        check(n, f, fails, oks, quiet)


def resourcesync_checks(base, fails, oks, quiet):
    state = {}

    def source_desc():
        root, note = xml_of(base + "/.well-known/resourcesync")
        links = [e.get("href") for e in root.iter(f"{SM_NS}loc")]
        links += [e.get("href") for e in root.iter(f"{RS_NS}ln")]
        locs = [e.text for e in root.iter(f"{SM_NS}loc") if e.text]
        state["caps"] = locs[0] if locs else None
        if not state["caps"]:
            raise ValueError("source description names no capability list")
        return f"-> {state['caps']}, {note}"

    def capability_list():
        if not state.get("caps"):
            raise ValueError("skipped: no capability list to fetch")
        root, note = xml_of(state["caps"])
        locs = [e.text for e in root.iter(f"{SM_NS}loc") if e.text]
        state["children"] = locs
        if not locs:
            raise ValueError("capability list is empty")
        return f"{len(locs)} capabilities, {note}"

    def walk_children():
        kids = state.get("children") or []
        if not kids:
            raise ValueError("skipped: no capabilities to walk")
        walked = []
        for u in kids[:4]:
            root, note = xml_of(u)
            n = len(list(root.iter(f"{SM_NS}url")))
            walked.append(f"{u.rsplit('/',1)[-1]}={n}")
        return "chain walked: " + ", ".join(walked)

    for n, f in (("ResourceSync source description", source_desc),
                 ("ResourceSync capability list", capability_list),
                 ("ResourceSync chain walk", walk_children)):
        check(n, f, fails, oks, quiet)


def sitemap_and_feed(base, fails, oks, quiet):
    def one(path, kind):
        def go():
            root, note = xml_of(base + path)
            if kind == "sitemap":
                n = len(list(root.iter(f"{SM_NS}url"))) or len(list(root.iter(f"{SM_NS}sitemap")))
                if not n:
                    raise ValueError("no <url> or <sitemap> entries")
                return f"{n} entries, {note}"
            n = len(list(root.iter(f"{ATOM_NS}entry"))) or len(list(root.iter("item")))
            if not n:
                raise ValueError("no entries")
            return f"{n} entries, {note}"
        return go

    for path, kind in (("/sitemap.xml", "sitemap"),
                       ("/sitemap-axn.xml", "sitemap"),
                       ("/feed.xml", "feed")):
        check(path, one(path, kind), fails, oks, quiet)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--base", default=BASE)
    ap.add_argument("--quiet", action="store_true", help="print failures only")
    a = ap.parse_args()
    base = a.base.rstrip("/")
    print(f"Protocol surface guardian — {base}")
    fails, oks = [], []
    oai_checks(base, fails, oks, a.quiet)
    resourcesync_checks(base, fails, oks, a.quiet)
    sitemap_and_feed(base, fails, oks, a.quiet)
    print(f"\n{len(oks)} held · {len(fails)} failed")
    if fails:
        print("\nThe archive advertises harvesting interfaces it is not serving.")
        for f in fails:
            print(f"  - {f}")
        return 1
    print("Every advertised XML surface answers as a harvester would require.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
