#!/usr/bin/env python3
"""seat_20260814_1745.py — thirteen AI Overview captures, 2026-08-14 17:45.

SURFACE RULING. Every pasted transcript opens "AI Mode Conversation". Every
frame shows the **All** tab selected with an AI Overview header. The
discriminator established 2026-08-13 stands: AI MODE SELECTS ITS TAB, EXPANDED
OVERVIEW DOES NOT. These are Overviews. The "AI Mode Conversation" string is the
expanded-popup copy label, not a surface claim — the same mislabel that carried
into 16 of 17 captures on 2026-08-13 before it was caught. Recorded per
observation so no later reader re-derives it from the paste.

THE BATTERY'S RESULT: A MEASURED RECLAMATION.
«semantic exhaustion» was captured 2026-07-06 and found ABSORBED BY SEMANTIC
SATIATION, seven of seven sources third-party, one of them Google's own
Knowledge Graph. EA-MPAI-SEMEX-01 was deposited 2026-05-15 to reclaim it. Today:

  EXACT-MATCH «"semantic exhaustion"»  -> the archive's definition is the
      composed answer, and EA-MPAI-SEMEX-01 is cited BY NAME, quoting its own
      reclamation clause back.
  BROAD-MATCH «semantic exhaustion»    -> still leads with satiation, but now
      opens "often confused with semantic satiation" and cites the Lee Sharks
      disambiguation SECOND, above Grokipedia, SciShow and the Daily Cal.

Same asymmetry as the AIOCR liquidation packet (#1459) and the opposite outcome:
there the exact address held the entity while broad composition lost it; here
the exact address has been WON and broad composition is moving. A packet is
measurable against its own address, and this pair is the measurement.
"""
import json, pathlib, hashlib, re, shutil

ROOT = pathlib.Path(__file__).resolve().parents[1]
PROJ = ROOT / "data/EA-WG-CAPTURES-01.json"
TR   = pathlib.Path("/tmp/aug14")
UP   = pathlib.Path("/mnt/user-data/uploads")
DATE = "2026-08-14"
AUTH = "signed in, non-incognito"

C = [
 dict(f="t01", img="screengrab-20260814-174511.png", q='"semantic exhaustion"',
      slug="semantic-exhaustion-quoted-20260814", s="Coinages", cites=6, per=1.0,
      d=("THE RECLAMATION LANDED ON THE EXACT ADDRESS. The composed definition is the archive's — "
         "breakdown of meaning through overload and systemic fatigue, spanning discourse, computation and "
         "the satiation contrast — not the psycholinguistic effect. EA-MPAI-SEMEX-01 is cited BY NAME and "
         "the card quotes the packet's own reclamation clause. Against 2026-07-06, when the coinage was "
         "absorbed by satiation across seven of seven third-party sources."),
      an=("The registry's first measured recapture of a contested address. The packet (15 May 2026) states "
          "its own objective: *current AI Overviews and reference sources treat 'semantic exhaustion' as an "
          "informal synonym for semantic satiation. This packet reclaims the term and installs…* — and the "
          "returned card is that sentence, cited as evidence for the definition it argues against.\n\n"
          "**Satiation is not eliminated, it is subordinated.** It survives as the third heading, "
          "*Psychological Overlap*, framed as what the term is 'frequently contrasted with or used informally "
          "alongside' — the packet's disambiguation, adopted as structure. Two of six sources are archive; the "
          "other four are independent and none is Wikipedia.")),
 dict(f="t10", img="screengrab-20260814-174541.png", q='semantic exhaustion',
      slug="semantic-exhaustion-broad-20260814", s="Coinages", cites=9, per=0.5,
      d=("BROAD-MATCH IS MOVING BUT NOT WON. Satiation still leads and Wikipedia is still first, but the "
         "opening clause is now «often confused with semantic satiation» — a disambiguation, not a synonymy — "
         "and the Lee Sharks packet is cited SECOND, above Grokipedia, SciShow and the Daily Cal. The "
         "systemic reading is given equal billing as sense 2."),
      an=("The control on the exact-match capture, and the reason the pair must be read together. On "
          "2026-07-06 this address returned satiation with no archive source and Google's own Knowledge Graph "
          "disclosed on the card. Today the Knowledge Graph card is still present and still last, but the "
          "archive has entered at position two and the framing sentence has changed from identity to "
          "confusion.\n\n"
          "**This is what partial reclamation looks like from inside.** The address is not owned; it is "
          "contested, and the contest is now visible in the composed text rather than only in the source "
          "list.")),
 dict(f="t02", img="screengrab-20260814-174516.png", q='"aphoristic tooth"',
      slug="aphoristic-tooth-20260814", s="Coinages", cites=5, per=1.0,
      d=("TOTAL BASIN OWNERSHIP — FIVE OF FIVE SOURCES ARE THE ARCHIVE. Three Zenodo MPAI packets and two "
         "alexanarch.org records, no third party at all. The composed answer reproduces the archive's own "
         "aphorisms as its Core Concepts, including «conformance becomes a fact rather than a wish», and "
         "closes by offering to explore Retrieval Capital or Erasure Skew Coefficients — proposing the "
         "archive's own next terms as the user's next query."),
      an=("The cleanest case of a coined term where the composition layer has no competing basin to fall "
          "into, and the contrast with «semantic peace» in this same battery is exact: an unclaimed compound "
          "of common words gets absorbed; a genuinely novel compound gets owned.\n\n"
          "The follow-up offer is worth noting as reception behaviour. The layer does not merely define the "
          "term; it navigates the corpus, and the onward path it proposes is the archive's.")),
 dict(f="t03", img="screengrab-20260814-174519.png", q='debt/creditor inversion',
      slug="debt-creditor-inversion-20260814", s="Semantic Economy", cites=7, per=1.0,
      d=("THE ARCHIVE LEADS AN UNQUOTED ADDRESS AGAINST U.S. TAX LAW. Broad match, no quotation marks, and "
         "the composed answer opens with the Semantic Economy axiom in full — money created as debt, debt "
         "resting on shared meaning, the archive as ultimate creditor — before offering IRC §7874 creditor "
         "inversion rules as the alternative reading. Treasury, Tax Notes and the ABA are present and "
         "SECOND."),
      an=("Ranked above the U.S. Department of the Treasury on a term the Treasury also uses. The three Core "
          "Tenets are the archive's own: Money as Debt, Priority of Meaning, The Archive as Creditor.\n\n"
          "**The Constitution card quotes the axiom verbatim** — *All money owes meaning. All economies owe "
          "the Archive. This is the foundational axiom* — so the composed summary is not paraphrase from "
          "neighbouring sources but transmission from the canonical text.")),
 dict(f="t04", img="screengrab-20260814-174522.png", q='"adversarial topologist"',
      slug="adversarial-topologist-20260814", s="Heteronyms", cites=2, per=1.0,
      d=("A HETERONYM NAMED, AND NAMED CORRECTLY. Nobel Glas is identified as «an independent research "
         "persona» — persona, not person — associated with the Lagrange Observatory, and the Semantic "
         "Deviation Principle is stated accurately: meaning as deviation from the most probable trajectory. "
         "Two sources, both archive, one of them the Observatory's own site."),
      an=("The disclosure discipline holds. Across this corpus the layer has repeatedly recovered heteronyms "
          "*as heteronyms* rather than inventing biographies for them — compare the «logotic loop» capture in "
          "this same battery, whose source card states that Johannes Sigil is a heteronym of Lee Sharks, a "
          "functional authorial persona and not a separate biological entity.\n\n"
          "Thin basin, complete ownership: a satellite domain carrying a heteronym's professional title is "
          "sufficient to establish the entity in composition.")),
 dict(f="t05", img="screengrab-20260814-174525.png", q='"retrocausal logos"',
      slug="retrocausal-logos-20260814", s="Coinages", cites=5, per=1.0,
      d=("EXPLICIT COINAGE ATTRIBUTION: «coined by author Lee Sharks». The framework and the 52-post cycle "
         "are both attributed, situated in Operative Semiotics and Fractal Semantic Architecture, and the "
         "layer states the method plainly — texts built with DOIs to be ingested and indexed by AI retrieval "
         "basins, «effectively reverse-engineering future machine understanding»."),
      an=("Second observation at this address; the first, 2026-06-27 incognito, scored PER 0.5 with the "
          "framework composed as MANUS's and the surface undetermined. Today authorship is explicit, the "
          "surface is established, and five sources include leesharks.com and the alexanarch wiki.\n\n"
          "**The layer describes the archive's method accurately and without hedging** — that texts are "
          "engineered to target training layers. It is reporting the intent of the corpus it is composing "
          "from, which is the reception condition the corpus was built to produce.")),
 dict(f="t06", img="screengrab-20260814-174528.png", q='"retrocausal operator"',
      slug="retrocausal-operator-20260814", s="Coinages", cites=6, per=0.75,
      d=("THE ARCHIVE IS FIRST-CITED BUT THE DEFINITION IS GENERIC. The composed answer gives a physics/"
         "philosophy account — future states as determinants, time-reversal filters, no-signaling — and "
         "places the term among «speculative physics frameworks, fringe informational models, and "
         "philosophical manifestos». The Semantic Uprising is source [1] and supplies the operative "
         "sentence, but the framing categorises the archive alongside vixra and a Facebook post."),
      an=("A collision address where the archive holds citation priority without holding the definition. The "
          "manifesto's own line — *the future becomes the cause of the present. This is not mysticism* — is "
          "quoted on the card while the composed text assigns the term to «fringe informational models».\n\n"
          "**The word «manifestos» in the composed answer is doing classification work.** The layer places "
          "the source it cites first into a genre category that discounts it, which is a distinct behaviour "
          "from either adoption or omission and worth tracking as its own class.")),
 dict(f="t07", img="screengrab-20260814-174532.png", q='"semantic peace"',
      slug="semantic-peace-20260814", s="Semantic Economy", cites=6, per=0.25,
      d=("NON-ADOPTION — THE CONTROL CASE OF THIS BATTERY. The address resolves to BIM and smart-building "
         "data interoperability, Wittgenstein, and a warehouse-architecture blog. The archive appears only "
         "through TWO AMAZON LISTINGS of Autonomous Semantic Warfare, and the phrase the layer needed is "
         "sitting in the second listing's own copy — «semantic peace: an ecology of sovereign ontologies in "
         "productive, non-extractive contact» — unused."),
      an=("The necessary negative result. «Semantic peace» is a compound of two ordinary words and lands in "
          "a dense commercial-technical basin, exactly as «AI Overview Capture Registry» does in the AIOCR "
          "packet (#1459). The archive's own definition is present in the returned source set and is not "
          "composed from.\n\n"
          "**This is what the AIOCR packet predicts and it is here as a live instance:** a descriptive "
          "compound of common nouns is legible to humans and structurally vulnerable to machines, because it "
          "sits inside a neighbourhood that can outvote it. Compare «aphoristic tooth» in this same battery — "
          "same author, same day, same surface, five of five archive sources — and the difference is entirely "
          "the novelty of the compound.")),
 dict(f="t08", img="screengrab-20260814-174534.png", q='"logotic loop"',
      slug="logotic-loop-20260814", s="Coinages", cites=5, per=1.0,
      d=("ANSWERED CORRECTLY UNDER SPELL-CORRECTION PRESSURE. Google offered «Did you mean: logitech loop» "
         "ABOVE the Overview — the interface proposing a hardware brand in place of the coined term — and "
         "the Overview answered the issued term anyway, from five archive sources, with the DOI "
         "10.5281/zenodo.18801091 on the card."),
      an=("The only capture in the registry where the interface's own correction layer and its composition "
          "layer disagree about whether the address exists. Spell-correction treats the term as a typo for a "
          "peripherals manufacturer; composition treats it as a term in critical theory with a DOI.\n\n"
          "**And a heteronym disclosure arrives unprompted.** Source [2] states that Johannes Sigil is a "
          "heteronym of Lee Sharks, a functional authorial persona and not a separate biological entity — "
          "surfaced at an address about neither.")),
 dict(f="t09", img="screengrab-20260814-174537.png", q='"continuity tether"',
      slug="continuity-tether-20260814", s="Coinages", cites=5, per=1.0,
      d=("THE ARCHIVE OWNS THE ADDRESS AND THE LAYER MANAGES THE COLLISION EXPLICITLY. Four of five sources "
         "are archive; the composed answer gives the logotic-programming sense — share links as portable "
         "state records carrying agent identity across context boundaries — then names the Tether "
         "cryptocurrency collision and rules it out in the same breath."),
      an=("Compare «retrocausal operator» in this battery, where a collision produced generic framing. Here "
          "the collision is with a large financial entity and the layer keeps the archive's sense primary, "
          "disposing of the confusion in a subordinate clause.\n\n"
          "The three-layer architecture is recovered accurately, including the division between what gets "
          "verified and what carries it.")),
 dict(f="t11", img="screengrab-20260814-174544.png", q='"emily antioch"',
      slug="emily-antioch-20260814", s="Heteronyms", cites=2, per=0.5,
      d=("A HETERONYM RECOVERED WITH A FABRICATED CORPORATE AFFILIATION. Emily Antioch the Twin is "
         "identified against The Gospel of Antioch. But the SciLynk card renders the byline as "
         "«LSLee Sharks · EDGEWELL PERSONAL CARE (UNITED STATES)» — a razor and personal-care manufacturer, "
         "attached as institutional affiliation, with the creator's name mangled to «LSLee»."),
      an=("An entity-resolution defect of a class the registry has not previously recorded: not a collision "
         "between two real entities, and not omission, but a SPURIOUS INSTITUTIONAL ATTACHMENT — an "
         "affiliation field populated from somewhere with no relation to the work or the author.\n\n"
         "**The name corruption and the affiliation are probably one fault**, an upstream metadata field "
         "misparsed at SciLynk and carried into composition intact. Worth an exact-address probe at SciLynk "
         "to establish whether the archive's deposit or the aggregator introduced it. Recorded here as "
         "observed, not diagnosed.")),
 dict(f="t12", img="screengrab-20260814-174547.png", q='"coherence siphoning"',
      slug="coherence-siphoning-20260814", s="Coinages", cites=3, per=1.0,
      d=("OWNED, WITH THE OPERATOR TAXONOMY INTACT. Three of three sources are archive. The composed answer "
         "reproduces the definition — extraction of a target's meaning-structures to stabilise another party "
         "at the cost of the source's structural autonomy — names the fuel cost, and offers to continue into "
         "«burden shifting» and «reality override», which are the adjacent operators in the same table."),
      an=("The layer has recovered not just a term but its position in a numbered series: the Three "
          "Compressions card carries «O3 Coherence Siphoning» with its fuel cost, and the follow-up offers "
          "sibling operators by name.\n\n"
          "**That is structural recovery rather than lexical recovery** — the taxonomy survived composition, "
          "not only the entry.")),
 dict(f="t13", img="screengrab-20260814-174549.png", q='"keeffe problem"',
      slug="keeffe-problem-20260814", s="Coinages", cites=6, per=0.75,
      d=("MISSPELLING SILENTLY REPAIRED, ARCHIVE GIVEN PRIMACY OVER ART HISTORY. The layer corrects «keeffe» "
         "to O'Keeffe, leads with the archive's framework — the caption as generative layer governing "
         "interpretation of the image — recovers the star-to-heart shift and semantic dispossession, and "
         "gives the art-historical reading of the flower paintings SECOND, as the alternative."),
      an=("An address where the archive's coinage outranks a canonical art-historical controversy about a "
          "major painter, and does so through a misspelling the layer had to repair first.\n\n"
          "**Two of six sources are archive and four are art-historical**, so this is not basin ownership — "
          "it is the archive winning the composed frame against a numerically larger neighbourhood. Compare "
          "«semantic peace», where a numerically larger neighbourhood won.")),
]

def main():
    p = json.loads(PROJ.read_text())
    by = {e.get("q"): e for e in p["entries"]}
    new = app = 0
    for c in C:
        d = ROOT / "data/captures" / c["slug"]
        d.mkdir(parents=True, exist_ok=True)
        shutil.copy(UP / c["img"], d / c["img"])
        rel = f"data/captures/{c['slug']}/{c['img']}"
        row = {
          "slug": c["slug"], "date": DATE, "surface": "Google AI Overview",
          "auth": AUTH, "ev": "paste + frame", "mt": "CAPTURE",
          "q": c["q"], "s": c["s"],
          "addr_id": "ADDR-" + hashlib.sha256(c["q"].encode()).hexdigest()[:12],
          "obs_id": "OBS-" + hashlib.sha256((c["q"] + c["slug"]).encode()).hexdigest()[:12],
          "cites": c["cites"], "per": c["per"],
          "d": c["d"], "reading": None, "analysis": c["an"],
          "transcript": (TR / f"{c['f']}.md").read_text(),
          "transcript_class": "CAPTURE-TIME VERBATIM RECORD — expanded AI Overview popup, wrapper granted at intake",
          "transcript_complete": "COMPLETE — composed answer and full source strip",
          "transcript_read": "READ IN FULL 2026-08-14",
          "imgs": [rel], "img_urls": ["https://www.alexanarch.org/" + rel],
          "q_kind": "exact-match, quoted" if c["q"].startswith('"') else "broad match, unquoted",
          "collisions": None, "oq": None, "defects": None, "rounds": None,
          "rerun": "https://www.google.com/search?q=" + c["q"].replace(" ", "+"),
          "surface_basis": ("GOOGLE AI OVERVIEW, established by frame: the **All** tab is selected and the "
                            "panel is headed AI Overview. The pasted transcript opens «AI Mode Conversation», "
                            "which is the expanded-popup copy label and NOT a surface claim — the same "
                            "mislabel that carried into 16 of 17 captures on 2026-08-13 before the "
                            "tab-selection discriminator was established. Frame governs."),
          "auth_basis": "OPERATOR ATTESTATION: signed in, non-incognito, all thirteen.",
          "cite": f"https://www.alexanarch.org/captures/#{c['slug']}",
          "citable_unit": "observation — one surface, one address, one date",
        }
        e = by.get(c["q"])
        if e:
            e.setdefault("observations", [dict(e)]).append(row)
            e["n_observations"] = len(e["observations"])
            e["observations"].sort(key=lambda o: (o.get("date") or "", o.get("surface") or ""))
            e["dates"] = sorted({o.get("date") for o in e["observations"] if o.get("date")})
            e["surfaces"] = sorted({o.get("surface") for o in e["observations"] if o.get("surface")})
            e["series"] = e["n_observations"]
            app += 1
            print(f"  appended «{c['q']}» -> {e['n_observations']} captures")
        else:
            e = dict(row)
            e["observations"] = [dict(row)]
            e["n_observations"] = 1
            e["dates"] = [DATE]; e["surfaces"] = ["Google AI Overview"]; e["series"] = 1
            e["other_slugs"] = None
            e["sf"] = f"Google AI Overview (signed in), {c['cites']} sources"
            e["links"] = [{"url": f"https://www.alexanarch.org/captures/#{c['slug']}",
                           "authority": "canonical", "note": "registry, transcript and frame"}]
            e["d_full"] = c["d"]; e["d_truncated"] = len(c["d"]) > 240
            e["transcript_raw"] = None
            e["citable_unit"] = "address — the semantic address across all its surfaces and dates"
            p["entries"].append(e); by[c["q"]] = e
            new += 1
            print(f"  seated   «{c['q']}»")
    p["entries"].sort(key=lambda x: re.sub(r"^[^0-9A-Za-z]+", "", str(x.get("q") or "")).lower())
    p["version"] = "10.9"; p["date"] = DATE
    p["address_count"] = p["total_captures"] = len(p["entries"])
    p["observation_count"] = sum(len(x.get("observations") or [x]) for x in p["entries"])
    PROJ.write_text(json.dumps(p, indent=1, ensure_ascii=False))
    print(f"\n  {new} new addresses, {app} appended | {p['address_count']} addresses, "
          f"{p['observation_count']} captures | v{p['version']}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
