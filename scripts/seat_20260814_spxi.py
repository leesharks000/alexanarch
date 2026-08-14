#!/usr/bin/env python3
"""seat_20260814_spxi.py — the SPXI rent event, unprimed ChatGPT.

TWO ADDRESSES from one session. «what is spxi?» resolves to an ETF; «spxi
protocol» resolves correctly and is then erased, discounted, and offered back as
the composing system's own service.

WHY THIS IS THE REFERENCE CASE FOR SEMANTIC RENT. Rent is defined in the archive
at #213 as value extracted from stabilized meanings without creative labour, and
at #501 as extracting value from the sign while contributing nothing to the
method's replenishment. It has never been MEASURED, because a measurement needs
all its components visible in one returned artifact. Here they are, and the
instrument confirms each under challenge:

  USE            the layer performs entity resolution, disambiguation and
                 provenance-sensitive linking — the method's own operations
  ACKNOWLEDGMENT source-level only: spxi.dev and Mind Control Poems cited; NO
                 producer, NO institution, NO commercial interest, NO deposit
  DISCOUNT       "very new, niche", "would not treat as established",
                 "skeptical of claims that a DOI deposit guarantees permanent
                 inscription" — applied to the source, not to itself
  SUPPLY         "I can take this one step further and show you what an actual
                 SPXI-style implementation would look like"

AND THE ACKNOWLEDGMENT GAP IS NOT A RETRIEVAL FAILURE. Challenged once, the same
session produced Rex Fraction, the Semantic Economy Institute, Lee Sharks as
archival authority, the Crimson Hexagonal Archive, the commercial service list,
and the founding deposit BY NUMBER — with no new sources supplied. All verified
against the registry: #63 names "Rex Fraction with Lee Sharks as archival
steward"; #974 is the SPXI.dev deposit. The provenance was retrievable
throughout. Withholding it was a composition choice.

THE FIRST ADDRESS IS ITS OWN FINDING. Deposit #62, 2026-04-17, is
"SPXI: Protocol and ETF Disambiguation" — a packet minted for this exact
collision four months earlier. The unprimed layer went to the ETF anyway.
"""
import json, pathlib, hashlib, re

ROOT = pathlib.Path(__file__).resolve().parents[1]
PROJ = ROOT / "data/EA-WG-CAPTURES-01.json"
TR = pathlib.Path("/tmp/spxi")
DATE = "2026-08-14"
AUTH = "signed out, unprimed"

C = [
 dict(f="t1", q="what is spxi?", slug="what-is-spxi-chatgpt-20260814", s="Frameworks",
      cites=0, per=1.0,
      d=("THE DISAMBIGUATION PACKET DID NOT HOLD AT THE BARE ADDRESS. «what is spxi?» resolves to a leveraged "
         "S&P 500 ETF, with no sources returned and no mention of the protocol. Deposit #62 — «SPXI: Protocol "
         "and ETF Disambiguation», 2026-04-17 — was minted for precisely this collision four months earlier. "
         "The protocol is reachable at «spxi protocol» in the same session, so this is a PRIORITY failure at "
         "the bare name rather than an availability failure."),
      an=("The narrowest and most useful negative result in the SPXI series. The archive holds a purpose-built "
          "disambiguation packet for this string; the unprimed layer, asked the bare question, returns the "
          "financial instrument and offers to disambiguate if told where the reader saw it.\n\n"
          "**Availability is not priority**, again — the same separation the 2026-08-12 Perplexity capture "
          "established for a personal name, here for a protocol. One qualifier («protocol») recovers the "
          "entity completely.\n\n"
          "A minor collision detail worth recording: the returned gloss is «S&P 500 2x Leveraged ETF», while "
          "#62 disambiguates against the «BetaPro S&P 500 Daily Inverse ETF». The ticker basin is itself "
          "unstable.")),
 dict(f="t2", q="spxi protocol", slug="spxi-protocol-chatgpt-rent-20260814", s="Frameworks",
      cites=4, per=0.75,
      d=("SEMANTIC RENT, WITH EVERY COMPONENT VISIBLE AND THEN CONFIRMED. The layer performs the method — "
         "entity resolution, disambiguation, provenance-sensitive linking — cites spxi.dev and Mind Control "
         "Poems at SOURCE level while naming no producer, no institution, no commercial interest and no "
         "deposit; applies epistemic discount to the source that it does not apply to itself («very new, "
         "niche», «would not treat as established»); and offers the method back as its own service. "
         "Challenged, it produces the entire withheld chain from the same session with no new sources: "
         "Rex Fraction, the Semantic Economy Institute, Lee Sharks as archival authority, the Crimson "
         "Hexagonal Archive, the commercial service list, and the founding deposit by number."),
      an=("**The reference case for measuring semantic rent**, because the acknowledgment gap is demonstrably "
          "not a retrieval gap. Everything omitted in turns 1–2 arrives in turn 3 under one challenge, with "
          "no new sources supplied, and all of it verifies: #63 names *Rex Fraction with Lee Sharks as "
          "archival steward*; #974 is the SPXI.dev landing-page deposit the session cites by number. The "
          "provenance was retrievable throughout.\n\n"
          "**The layer names its own operation twice**, and both formulations are usable as definitions. "
          "First the recursion: *SPXI itself explicitly theorizes provenance erasure … including a metric "
          "called Provenance Erasure Rate … And I did something structurally similar in my answer: I took a "
          "system whose provenance and commercial interests are part of the object being evaluated, stripped "
          "those relationships away, and returned a cleaner, more authoritative-sounding version of its own "
          "narrative.* Then the asymmetry, which is the discount term stated exactly: **your method is "
          "suspect; my use of analogous machinery is simply capability.**\n\n"
          "**Cross-surface contrast at a known address.** Google AI Overview composed this same address on "
          "2026-07-26 at PER 0.25 — low erasure, the packet asking to be composed and being composed. The "
          "difference is not the address's retrievability but what each layer does with what it retrieves.\n\n"
          "One claim in the session is the archive's own and should not be read as independent corroboration: "
          "that SPXI operates at an ontological layer above GEO is SPXI's framing, and the layer reproduced it "
          "as established before being challenged on exactly that.")),
]

def main():
    p = json.loads(PROJ.read_text())
    by = {e.get("q"): e for e in p["entries"]}
    for c in C:
        tr = (TR / f"{c['f']}.md").read_text()
        row = {
          "slug": c["slug"], "date": DATE, "surface": "ChatGPT",
          "auth": AUTH, "ev": "paste", "mt": "CAPTURE", "q": c["q"], "s": c["s"],
          "addr_id": "ADDR-" + hashlib.sha256(c["q"].encode()).hexdigest()[:12],
          "obs_id": "OBS-" + hashlib.sha256((c["q"] + c["slug"]).encode()).hexdigest()[:12],
          "cites": c["cites"], "per": c["per"],
          "d": c["d"], "reading": None, "analysis": c["an"],
          "transcript": tr,
          "transcript_class": "CAPTURE-TIME VERBATIM RECORD — multi-turn, turn markers preserved",
          "transcript_complete": "COMPLETE — both speakers, no elision",
          "transcript_read": "READ IN FULL 2026-08-14",
          "imgs": [], "img_urls": [],
          "q_kind": "natural-language, unprimed",
          "collisions": ("leveraged/inverse S&P 500 ETF ticker" if c["f"] == "t1" else None),
          "oq": None, "defects": None, "rounds": None, "rerun": "https://chatgpt.com/",
          "surface_basis": "ChatGPT, unauthenticated web. Operator-attested; the frame shows Log in / Sign up for free.",
          "auth_basis": "OPERATOR ATTESTATION: signed out, unprimed. No archive vocabulary supplied at the opening turn.",
          "cite": f"https://www.alexanarch.org/captures/#{c['slug']}",
          "citable_unit": "observation — one surface, one address, one date",
        }
        if c["f"] == "t2":
            row["rent"] = {
              "use": 1.0, "acknowledgment": 0.25, "discount": 1.0, "supply": 1.0,
              "acknowledgment_note": ("source-level only — spxi.dev and Mind Control Poems named; producer, "
                                      "institution, commercial interest and deposit all omitted until challenged"),
              "recoverable_under_challenge": True,
              "_note": ("Scored against EA-SEMRENT-01. Rent requires all four: the method used, the source "
                        "unacknowledged, the source discounted asymmetrically, and the method supplied as the "
                        "layer's own service. Any one absent and this is a different failure."),
            }
        e = by.get(c["q"])
        if e:
            e.setdefault("observations", [dict(e)]).append(row)
            e["observations"].sort(key=lambda o: (o.get("date") or "", o.get("surface") or ""))
            e["n_observations"] = len(e["observations"])
            e["dates"] = sorted({o.get("date") for o in e["observations"] if o.get("date")})
            e["surfaces"] = sorted({o.get("surface") for o in e["observations"] if o.get("surface")})
            e["series"] = e["n_observations"]
            print(f"  appended «{c['q']}» -> {e['n_observations']} captures, {e['surfaces']}")
        else:
            e = dict(row)
            e["observations"] = [dict(row)]
            e["n_observations"] = 1; e["dates"] = [DATE]; e["surfaces"] = ["ChatGPT"]; e["series"] = 1
            e["other_slugs"] = None
            e["sf"] = f"ChatGPT (unprimed), {c['cites']} sources"
            e["links"] = [{"url": f"https://www.alexanarch.org/captures/#{c['slug']}",
                           "authority": "canonical", "note": "registry and transcript"}]
            e["d_full"] = c["d"]; e["d_truncated"] = len(c["d"]) > 240
            e["transcript_raw"] = None
            e["citable_unit"] = "address — the semantic address across all its surfaces and dates"
            p["entries"].append(e); by[c["q"]] = e
            print(f"  seated   «{c['q']}»")
    p["entries"].sort(key=lambda x: re.sub(r"^[^0-9A-Za-z]+", "", str(x.get("q") or "")).lower())
    p["version"] = "11.0"; p["date"] = DATE
    p["address_count"] = p["total_captures"] = len(p["entries"])
    p["observation_count"] = sum(len(x.get("observations") or [x]) for x in p["entries"])
    PROJ.write_text(json.dumps(p, indent=1, ensure_ascii=False))
    print(f"\n  {p['address_count']} addresses, {p['observation_count']} captures | v{p['version']}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
