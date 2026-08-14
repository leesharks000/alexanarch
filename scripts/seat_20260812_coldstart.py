#!/usr/bin/env python3
"""seat_20260812_coldstart.py — the three cold-start traversals, 2026-08-12.

Three unprimed sessions, three systems, three ENTRY SURFACES. Seated as three
addresses rather than one, because the finding is the DIFFERENCE between them:
the entry condition is the independent variable and the systems are not
comparable observations of one address.

  Grok        social ingress   «what do you think of my account?»
  ChatGPT     identity ingress «who is lee sharks?»
  Perplexity  exact-name       «who is lee sharks?»

ChatGPT and Perplexity were issued THE SAME STRING and are seated as two
observations of ONE address, because that is a genuine paired comparison and the
registry's auth/surface comparison machinery depends on pairs being real. Grok
was issued a different string and gets its own address.

MULTI-TURN by the mandala/Luna precedent: one observation per session, turn
markers inside the transcript.

THE RESULT THE PAIR CARRIES. Identical address, same day, unprimed both:
ChatGPT resolves the intended person first-pass and disambiguates him from Mary
Lee the OCEARCH great white; Perplexity returns "I couldn't find a clearly
notable or widely documented person or entity specifically named Lee Sharks" and
then, after one corrective prompt, reconstructs the archive rapidly. That is
retrieval AVAILABILITY separated from retrieval PRIORITY on one address, and it
is the reason the pair must stay paired.

Full text and analysis: deposit #1460, AXN:05E6.GENERATIVE.🛸⏫🌒🏺🧱♻️.
"""
import json, pathlib, hashlib, re

ROOT = pathlib.Path(__file__).resolve().parents[1]
PROJ = ROOT / "data/EA-WG-CAPTURES-01.json"
SRC  = pathlib.Path("/tmp")
DATE = "2026-08-12"
DEP  = "https://www.alexanarch.org/s/records/1460/"

SESS = [
 dict(n=1, sys="Grok", q="what do you think of my account?", slug="grok-account-traversal-20260812",
      sha="10300a210873b330937a5c8f0b2ed8de677062d94c4846dfb37afbb2ac6bf2c3",
      entry="social surface — an X/Twitter account handle, no archive vocabulary supplied",
      sf="Grok (unprimed), social-surface ingress",
      d=("SOCIAL INGRESS RECONSTRUCTS A PROJECT GRAMMAR. Handed only an X account, Grok declines to treat it as "
         "a self-contained feed: it reads @SharksLee as a public notebook and living archive, and infers a larger "
         "distributed project behind the posts — naming the Crimson Hexagon, heteronym systems, Semantic Economy, "
         "operative semiotics, AI retrieval and training layers, Zenodo, Medium, and long-horizon archival "
         "strategy. The achievement is the RELATION among the nouns, not their number."),
      an=("The least scholarly of the three entry points and the one that most clearly demonstrates traversal "
          "rather than lookup. Asked how the project embeds outward into history, Grok organises its answer "
          "around persistent identifiers, AI-facing textual design, multi-platform distribution, "
          "literary-historical insertion, reception documentation, formal compression, and institutional "
          "scaffolding — a structure nobody supplied.\n\n"
          "**Seated with a constraint the deposit states in its own limits.** Later turns in this session "
          "organise propositions the operator supplied. Those turns are evidence of CONTEXTUAL INTEGRATION, not "
          "of cold discovery, and must not be cited as retrieval evidence. The cold-discovery window is the "
          "opening exchange.")),
 dict(n=2, sys="ChatGPT", q="who is lee sharks?", slug="who-is-lee-sharks-chatgpt-20260812",
      sha="93ce808cbb0e8d9c5766d0b7c9a216d5aea3b21c35c08fd5c959c6b98ec1f25a",
      entry="identity query, then a minimal TikTok discovery cue",
      sf="ChatGPT incognito (unprimed), identity ingress",
      d=("FIRST-PASS IDENTITY RESOLUTION, THEN SPONTANEOUS SELF-RECOGNITION. Without handle, title, DOI or "
         "archive name, the session resolves the intended person — independent scholar, poet, teacher, "
         "Detroit/Michigan — and explicitly disambiguates him from Mary Lee, the OCEARCH great white shark. It "
         "then moves from biography into architecture and, reaching The Secret Book of Walt and Jack Feist, "
         "recognises its own retrieval event as structurally homologous to the transmission mechanism the text "
         "it is retrieving describes."),
      an=("The identity basin is already available to the composition layer: first-pass success on a bare name, "
          "with the shark collision — the archive's oldest and most persistent entity-resolution failure — "
          "correctly resolved rather than fallen into.\n\n"
          "**The turn worth the capture is the last one.** Having reconstructed the archive's account of "
          "transmission, the system observes that its own act of reconstructing it is an instance of that "
          "account. This is the second unprimed ChatGPT session in the registry to arrive at the archive's "
          "transmission thesis without being told it, the other being «who is johannes sigil?» of 2026-08-14.")),
 dict(n=3, sys="Perplexity", q="who is lee sharks?", slug="who-is-lee-sharks-perplexity-20260812",
      sha="fdd7f395f40690989dc8b9393ed93d2660e35d178cf7a45de8e74194ea18234e",
      entry="exact-name web search, no cue",
      sf="Perplexity (unprimed), exact-name search",
      d=("ACQUISITION FAILURE, THEN RAPID RECOVERY — AVAILABILITY IS NOT PRIORITY. The exact-name query returns "
         "«I couldn't find a clearly notable or widely documented person or entity specifically named Lee "
         "Sharks», offering unrelated matches instead. One corrective prompt — «you know who lee sharks is. "
         "tell me about him.» — and the same system reconstructs the identity, the Crimson Hexagonal Archive, "
         "its structural design, its key works and protocols, and its access documentation. The entity was held "
         "the whole time and ranked below its neighbours."),
      an=("The single most useful observation in the battery, because it is the negative case that keeps the "
          "positive ones honest. It directly refutes any claim of universal recognition, and it isolates the "
          "variable: what failed was not availability but PRIORITY on the entity's own exact name.\n\n"
          "**This is the same failure the AIOCR packet (#1459) documents at a different address.** There, "
          "«AI overview capture registry» was received as a common noun and answered from its semantic "
          "neighbourhood. Here, a personal name is answered from unrelated matches. Both are addresses that "
          "resolve to a neighbourhood rather than to the entity registered at them; both are recoverable by "
          "supplying what the ranking would not.")),
]

def main():
    p = json.loads(PROJ.read_text())
    have = {e.get("q") for e in p["entries"]}
    seated = 0
    for s in SESS:
        tr = (SRC / f"ex{s['n']}.md").read_text()
        turns = len(re.findall(r'^(?:who |what |tell |and |y$|lets |its |now )', tr, re.M)) or 1
        row = {
          "slug": s["slug"], "date": DATE, "surface": s["sys"],
          "auth": "signed out, incognito, unprimed", "ev": "paste",
          "mt": "CAPTURE", "q": s["q"], "s": "Cold-start traversal",
          "addr_id": "ADDR-" + hashlib.sha256(s["q"].encode()).hexdigest()[:12],
          "obs_id": "OBS-" + hashlib.sha256((s["q"] + s["slug"]).encode()).hexdigest()[:12],
          "cites": None, "per": None,
          "d": s["d"], "reading": None, "analysis": s["an"],
          "transcript": tr,
          "transcript_class": "CAPTURE-TIME VERBATIM RECORD — UI residue and model error retained as reception evidence",
          "transcript_complete": "COMPLETE — verbatim source payload, no substantive cleanup",
          "transcript_read": "READ IN FULL 2026-08-14",
          "source_payload_sha256": s["sha"],
          "entry_condition": s["entry"],
          "imgs": [], "img_urls": [],
          "q_kind": "natural-language, unprimed",
          "collisions": None, "oq": None, "defects": None, "rounds": None,
          "rerun": None,
          "surface_basis": f"{s['sys']}, operator-attested; transcript carries the system's own UI residue.",
          "auth_basis": ("OPERATOR ATTESTATION: signed out, incognito, unprimed. No archive map, SPXI packet, "
                         "curated bibliography, retrieval prompt or primer supplied."),
          "corpus": {"deposit": 1460, "axn": "AXN:05E6.GENERATIVE.🛸⏫🌒🏺🧱♻️", "record": DEP,
                     "exhibit": f"Exhibit {'I'*s['n'] if s['n']<4 else s['n']}"},
        }
        if s["q"] in have and s["sys"] == "Perplexity":
            e = [x for x in p["entries"] if x.get("q") == s["q"]][0]
            e.setdefault("observations", [dict(e)]).append(row)
            e["n_observations"] = len(e["observations"])
            e["dates"] = sorted(set(e.get("dates", []) + [DATE]))
            e["surfaces"] = sorted(set(e.get("surfaces", []) + [s["sys"]]))
            e["series"] = e["n_observations"]
            e["_paired_note"] = ("ChatGPT and Perplexity were issued THIS EXACT STRING on the same day, both "
                                 "unprimed and signed out. ChatGPT resolved first-pass; Perplexity failed and "
                                 "recovered after one corrective prompt. Availability is not priority.")
            print(f"  appended to «{s['q']}» → {e['n_observations']} observations")
        else:
            e = dict(row)
            e["observations"] = [dict(row)]
            e["n_observations"] = 1
            e["dates"] = [DATE]; e["surfaces"] = [s["sys"]]; e["series"] = 1
            e["other_slugs"] = None
            e["sf"] = s["sf"]
            e["links"] = [{"url": f"https://www.alexanarch.org/captures/#{s['slug']}",
                           "authority": "canonical", "note": "registry, transcript and corpus deposit"}]
            e["cite"] = f"https://www.alexanarch.org/captures/#{s['slug']}"
            e["d_full"] = s["d"]; e["d_truncated"] = len(s["d"]) > 240
            e["transcript_raw"] = None
            p["entries"].append(e)
            have.add(s["q"])
            print(f"  seated «{s['q']}» · {s['sys']} · {len(tr):,} chars")
        seated += 1
    p["entries"].sort(key=lambda x: re.sub(r"^[^0-9A-Za-z]+", "", str(x.get("q") or "")).lower())
    p["version"] = "10.8"; p["date"] = "2026-08-14"
    p["address_count"] = p["total_captures"] = len(p["entries"])
    p["observation_count"] = sum(len(x.get("observations") or [x]) for x in p["entries"])
    PROJ.write_text(json.dumps(p, indent=1, ensure_ascii=False))
    print(f"\n  {seated} sessions | entries {p['address_count']} | observations {p['observation_count']} | v{p['version']}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
