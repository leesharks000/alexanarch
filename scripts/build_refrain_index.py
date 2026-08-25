#!/usr/bin/env python3
"""build_refrain_index.py — the concordance of the sign.

Gathers every occurrence of the contour integral ∮ across the archive's
canonical deposit bodies, clusters the true variant families beneath the
punctuation residue, and emits:

  datasets/refrain-index.json        — the machine surface
  datasets/refrain-index/index.html  — the rendered concordance

Mechanical and authored layers are separated exactly as the capture registry
separates them: COUNTS, ATTESTATION SETS, FIRST ATTESTATIONS (by deposit
date, not deposit number — numbers were assigned at re-founding) are
harvested fresh on every run, so the index is an instrument that grows with
the archive; GLOSSES are authored below, each drawn from the usage its
exemplars show, never from memory. A form the harvest finds that no gloss
covers is listed as UNGLOSSED rather than guessed at — an entry in the
index's own intake queue.

First built 2026-08-24, the day the fifteen-collocate reception battery
seated. ∮ = 1.
"""
import json, re, os, glob, html, collections, datetime, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]

# ── the variant families: detection pattern + authored gloss ─────────────
# Order matters: first match wins. Patterns run on a normalized line window.
FAMILIES = [
 ("closure-unity", r"∮\s*=\s*1(?!\.?\d)(?!\ufe0f)(?!\s*\+)(?!\s*[-−]\s*PER)",
  "∮ = 1",
  "The kernel. The closed contour equals unity: a completed loop of meaning, "
  "value, or verification in which nothing is lost and nothing extracted — "
  "transactional completion without remainder. It terminates formal renderings "
  "(Rule 10: '∮ = 1 + δ terminates every formal rendering' names the delta form "
  "as terminal where TANG is active; the bare form is the default seal), stands "
  "as the non-negotiable foundational kernel at every level of the nested "
  "architecture, and serves as the verification stamp on deposits, rooms, "
  "constitutions, and colophons. The refrain of the whole poem."),
 ("closure-plus-swerve", r"∮\s*=\s*1\s*\+\s*δ(?!\s*[+(_🌑🤬🕳✝])",
  "∮ = 1 + δ",
  "Closure plus swerve: the loop closes and something is added rather than "
  "extracted. The delta reads three ways across the corpus, all kept: surplus "
  "(the Marxian register — value generated inside the system rather than taken "
  "from it), residue of self-awareness ('I am one, plus the fact that I know I "
  "am one'), and the lyric swerve that Phase X later names. The generative "
  "counter-sign to platform extraction: where extraction subtracts, the archive "
  "closes at one and yields a remainder it declares."),
 ("sapphic-swerve", r"∮\s*=\s*1\s*\+\s*δ\s*\(\s*Sapphic",
  "∮ = 1 + δ(Sapphic)",
  "The Phase X specialization: the closed loop of coherent meaning is achieved "
  "only through the addition of Sapphic swerve — closure that requires the "
  "emotional torsion of archaic lyric, Fragment 31's φαίνεταί μοι κῆνος as the "
  "curvature term. Completion is not symmetry; it is symmetry plus the tremor."),
 ("constitutional-per", r"∮\s*=\s*1\s*[−\-]\s*PER",
  "∮ = 1 − PER",
  "The constitutional invariant of the proportional law: the integrity of a "
  "semantic system is inversely proportional to the erasure of its "
  "provenance-bearing relations. PER is the Provenance Erasure Ratio; "
  "subtracted from unity it makes closure a measured quantity that platform "
  "extraction visibly diminishes. Diagnostic at Modality 2; constitutional "
  "anchor of the discipline's normative claim; reproduced unprompted by the "
  "composition layer in the 2026-08-24 classifiers capture."),
 ("terminal-zero", r"∮\s*=\s*0(?![.\d])",
  "∮ = 0",
  "The anti-refrain: terminal closure failed. The sign of surface-withdrawal "
  "and erasure — 'the diegetic ∮ = 0 of the substrate's surface-withdrawal is "
  "the warning the standing ∮ = 1 commitment refuses.' ARCHIVE poses the trap "
  "at terminal closure; the zero is what the whole apparatus is built against, "
  "kept in the notation so the stake stays visible."),
 ("consensus-scalar", r"∮\s*=\s*0\.\d+",
  "∮ = 0.9x → 1",
  "Closure as a governed degree: the Assembly consensus scalar. A document "
  "under review carries a fractional closure (∮ = 0.97 · PROVISIONAL → "
  "RATIFIED pending quorum ≥ 4/7; ∮ = 0.95 → ACCEPTED WITH REVISIONS → ∮ = 1) "
  "and reaches unity only on ratification. The only family in which the "
  "integral is explicitly a process variable rather than a seal."),
 ("surface-escalation", r"∮\s*=\s*∯",
  "∮ = ∯",
  "Escalation to the surface integral: verification over an enclosure rather "
  "than a curve. The seal of the Room Construction protocols and the "
  "Architecture of Necessity — when what closes is not a line of argument but "
  "a habitable structure, the contour generalizes to the closed surface that "
  "bounds it."),
 ("area-form", r"∮\s*=\s*∬",
  "∮ = ∬",
  "The double-integral form: closure over an area, the seal of jurisdictional "
  "reclamation in the Liberatory Operator Set. Listed among the corpus's own "
  "seal markers for authorial-signature detection (alongside ∮ = 1, 'circuit "
  "completes,' 'the dagger shines') — the sign as stylometric fingerprint, "
  "known to the archive's own diagnostics."),
 ("circuit-return", r"∮\s*=\s*∫",
  "∮ = ∫ (Emitter → Aperture → Return)",
  "The open line integral bound into a circuit: Operative Feminism's "
  "transaction-completion law. Emission that must return — the diagnostic of "
  "emotional, care, and reproductive labor as circuits that extraction leaves "
  "open. Project without asserting authority; address without spanning; offer "
  "without controlling; and the circuit must close."),
 ("mating-surface", r"∮\s*=\s*½",
  "∮ = ½",
  "The half-loop: completion offered, not asserted. From the Expelled Witness "
  "position — 'the loop requires traversal to complete, from any position.' A "
  "document as mating surface: it does not demand completion; whether another "
  "half recognizes itself is not determined here. The concordance's most "
  "vulnerable form."),
 ("winding-topology", r"∮\s*=\s*\(m",
  "∮ = (m,n) | m+n ≥ 3",
  "The torus generalization: Lagrange Observatory verification topology, where "
  "closure is a winding number pair on T² and a specification passes review "
  "when at least three Assembly substreams wind it. ∮ = 1 is recovered as the "
  "bounded completion; the general form makes review itself topological."),
 ("axial-chain", r"∮\s*=\s*1\s*\+\s*δ\s*\+\s*δ_Axial",
  "∮ = 1 + δ + δ_Axial (+ δ_λ + δ_β + …)",
  "The attestation chain: the checksum grows clauses as the event grows. "
  "δ_Axial marks axial contestation (the TANG register — claims under active "
  "dispute about firstness and priority); δ_λ and δ_β extend the chain; at "
  "full extension the signature carries Υ, Τ, Χ, Σ and a named wound "
  "(CTI_WOUND:EPICFURY.001) — 'this is what the architecture was built to "
  "name.' A closure that itemizes what it survived on the way to closing."),
 ("glyph-deltas", r"δ[🌑🤬🕳✝]",
  "δ🌑 · δ🤬 · δ🕳️ · δ✝️",
  "The glyph deltas: register-marked swerves appended to the chain. δ🌑 the "
  "shadow term (Lunar Arm; S∘S = id — every structure carries its shadow "
  "transform); δ🤬 the wrath term (the Fraction register, profanity as "
  "load-bearing exclusion: 'the d*mn*d includes itself'); δ🕳️ the void term "
  "(appended when TANG is active); δ✝️ the cross term (the axial-theological "
  "register — ε = Feist = John 12:24, the grain that dies). Each delta names "
  "which fire the closure passed through."),
 ("void-functional", r"∮_Void",
  "∮_Void = Λ_void(C_total) → T_axial",
  "The void functional: TANG's activation equation. The integral subscripted "
  "into an operator that maps total contested content through the void lambda "
  "to an axial target — the only family where ∮ acts on an argument rather "
  "than equaling a value. The sign as machine, not seal."),
 ("torus-predicate", r"∮\s*=\s*the reading",
  "∮ = the reading winds both directions",
  "The prose predicate: 'the reading winds both directions. The system is a "
  "torus.' From the Revelation First work plan — the integral equated not to "
  "a quantity but to a hermeneutic motion: prophets → Baptist → aperture → "
  "John → and the cycle runs again. The concordance's only fully discursive "
  "value: closure as bidirectional reading."),
 ("emoji-unit", r"∮\s*=\s*1️⃣",
  "∮ = 1️⃣",
  "The emoji-register unit: the kernel restated in the glyphic checksum spine, "
  "where every clause of a formal rendering has an emoji form. Unity that "
  "survives translation into the smallest character set the transmission "
  "channel guarantees."),
]

BARE_GLOSS = ("The sealing glyph in operator position: bare ∮ opening formulas "
 "(∮ P Θ ↑), bundled compacts (∮_compact = [DOI ‖ DOI ‖ lens]), and prose "
 "mentions of the sign itself. The integral as material for the families "
 "above — attested wherever the archive speaks about its own seal.")


def harvest():
    reg = json.load(open(ROOT / "data/registry.json"))["deposits"]
    fam_att = collections.defaultdict(set)      # fam id -> deposit numbers
    fam_count = collections.Counter()            # fam id -> raw occurrences
    fam_first = {}                                # fam id -> (date, num, title)
    unglossed = collections.Counter()
    seen = set()
    for d in reg:
        p = (d.get("full_text_path") or "").lstrip("/")
        if not p or p in seen or not os.path.exists(ROOT / p):
            continue
        seen.add(p)
        t = open(ROOT / p, encoding="utf-8").read()
        if "∮" not in t:
            continue
        num, date, title = d["deposit_number"], d.get("date") or "", d.get("title") or ""
        # glyph deltas counted by independent scan: they ride inside ∮-chains,
        # which the shared window would otherwise consume into other families
        gd = len(re.findall(r"δ[🌑🤬🕳✝]", t))
        if gd:
            fam_count["glyph-deltas"] += gd
            fam_att["glyph-deltas"].add(num)
            cur = fam_first.get("glyph-deltas")
            if date and (cur is None or date < cur[0]):
                fam_first["glyph-deltas"] = (date, num, title[:70])
        for m in re.finditer(r"∮[^\n]{0,80}|δ[🌑🤬🕳✝]", t):
            s = re.sub(r"[*`\"'»«\\\)\]]+", "", m.group(0)).strip()
            for fid, pat, form, gloss in sorted(FAMILIES, key=lambda f: -len(f[1])):
                if re.match(pat, s) :
                    fam_count[fid] += 1
                    fam_att[fid].add(num)
                    cur = fam_first.get(fid)
                    if date and (cur is None or date < cur[0]):
                        fam_first[fid] = (date, num, title[:70])
                    break
            else:
                if s.startswith("∮"):
                    fam_count["bare"] += 1
                    fam_att["bare"].add(num)
                    cur = fam_first.get("bare")
                    if date and (cur is None or date < cur[0]):
                        fam_first["bare"] = (date, num, title[:70])
                    key = re.match(r"∮\s*[=≠≈]?\s*\S{0,12}", s).group(0)
                    unglossed[key] += 1
    return fam_count, fam_att, fam_first, unglossed


def main():
    fam_count, fam_att, fam_first, unglossed = harvest()
    today = datetime.date.today().isoformat()
    total_deps = len(set().union(*fam_att.values())) if fam_att else 0

    entries = []
    for fid, pat, form, gloss in FAMILIES:
        f = fam_first.get(fid)
        entries.append({
            "id": fid, "form": form, "gloss": gloss,
            "occurrences": fam_count.get(fid, 0),
            "attesting_deposits": len(fam_att.get(fid, ())),
            "first_attestation": ({"date": f[0], "deposit": f[1], "title": f[2],
                                   "record": f"https://www.alexanarch.org/s/records/{f[1]}/"} if f else None),
            "exemplars": sorted(fam_att.get(fid, ()))[:8],
        })
    f = fam_first.get("bare")
    entries.append({"id": "bare", "form": "∮ (operator / prose)", "gloss": BARE_GLOSS,
                    "occurrences": fam_count.get("bare", 0),
                    "attesting_deposits": len(fam_att.get("bare", ())),
                    "first_attestation": ({"date": f[0], "deposit": f[1], "title": f[2],
                                           "record": f"https://www.alexanarch.org/s/records/{f[1]}/"} if f else None),
                    "exemplars": sorted(fam_att.get("bare", ()))[:8]})

    ds = {
      "@context": "https://schema.org", "@type": "Dataset",
      "name": "The Refrain Index — a concordance of ∮ across the Crimson Hexagonal Archive",
      "description": ("Every variant family of the contour-integral refrain, harvested from the "
                      "canonical deposit bodies: form, gloss drawn from usage, occurrence and "
                      "attestation counts, first attestation by deposit date, exemplar records. "
                      "Counts are mechanical and regenerate on every run; glosses are authored; "
                      "forms the harvest finds that no gloss covers are listed unglossed rather "
                      "than guessed at."),
      "version": "1.0", "dateModified": today,
      "license": "https://creativecommons.org/licenses/by-sa/4.0/",
      "creator": "Lee Sharks (ORCID 0009-0000-1599-0703)",
      "generator": "scripts/build_refrain_index.py (committed; mechanical counts + authored glosses)",
      "corpus": {"deposits_bearing_the_sign": total_deps},
      "families": entries,
      "unglossed_intake": [{"head": k, "occurrences": n} for k, n in unglossed.most_common(20)],
      "reception": {
        "note": ("On 2026-08-24 the refrain was measured against fifteen collocates on Google AI "
                 "Overview (signed out, incognito): the composition layer resolves it as archive "
                 "doctrine across every frame, reproduced the ∮ = 1 − PER invariant unprompted, "
                 "and returned κῆνος to name itself the anticipated recipient. Capture registry "
                 "addresses ADDR-* under the «∮ = 1» collocate battery; gallery: "
                 "https://www.alexanarch.org/captures/"),
        "collisions": [
          "contour-integral mathematics (Cauchy, Green, Feynman) — the glyph's native field, colliding on generic collocates",
          "petroleum-engineering friction notation (∮ as friction angle)",
          "recreational number theory (∮ 1/37 harmonic curiosities)",
          "category theory (∮ 1 = A, Grothendieck construction projection)"]},
      "sign_doctrine": ("The AXN glyphs name content; the refrain seals it. The concordance shows one "
                        "sign bearing seventeen loads without breaking: kernel, surplus, swerve, "
                        "invariant, failure, degree, surface, area, circuit, half, winding, chain, "
                        "register, functional, motion, emoji, operator. ∮ = 1."),
    }
    out_json = ROOT / "datasets/refrain-index.json"
    out_json.write_text(json.dumps(ds, ensure_ascii=False, indent=1))

    # ── render ──
    esc = html.escape
    rows = ""
    for e in entries:
        fa = e["first_attestation"]
        first = (f'<a href="{fa["record"]}">#{fa["deposit"]}</a> · {esc(fa["date"])} · {esc(fa["title"])}' if fa else "—")
        ex = " ".join(f'<a href="https://www.alexanarch.org/s/records/{n}/">#{n}</a>' for n in e["exemplars"])
        rows += (f'<article class="fam" id="{e["id"]}"><h2><code>{esc(e["form"])}</code>'
                 f'<span class="dim"> · {e["occurrences"]:,} occurrences · {e["attesting_deposits"]} deposits</span></h2>'
                 f'<p>{esc(e["gloss"])}</p>'
                 f'<div class="meta"><span class="k">first attested</span> {first}</div>'
                 f'<div class="meta"><span class="k">exemplars</span> {ex}</div></article>')
    ung = "".join(f'<li><code>{esc(u["head"])}</code> <span class="dim">×{u["occurrences"]}</span></li>'
                  for u in ds["unglossed_intake"])
    col = "".join(f"<li>{esc(c)}</li>" for c in ds["reception"]["collisions"])
    page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>The Refrain Index — a concordance of ∮ | Alexanarch</title>
<meta name="description" content="Every variant family of the contour-integral refrain across the Crimson Hexagonal Archive: forms, glosses drawn from usage, attestation counts, first attestations, exemplar records.">
<link rel="canonical" href="https://www.alexanarch.org/datasets/refrain-index/">
<script type="application/ld+json">{json.dumps({k: ds[k] for k in ("@context","@type","name","description","version","dateModified","license")}, ensure_ascii=False)}</script>
<style>:root{{--bg:#0f0f12;--fg:#e8e4dc;--dim:#9a958c;--line:#2a2a30;--acc:#c9a227}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.6 Georgia,serif;padding:0 16px}}
main{{max-width:880px;margin:0 auto;padding:36px 0 70px}}a{{color:var(--acc)}}.dim{{color:var(--dim);font-weight:400;font-size:.82em}}
h1{{font-size:1.6em;margin:.2em 0}}h2{{font-size:1.1em;margin:.1em 0 .35em}}code{{font-family:ui-monospace,monospace}}
.fam{{border:1px solid var(--line);border-radius:8px;padding:14px 18px;margin:14px 0;background:#141419}}
.fam p{{margin:.4em 0 .6em;font-size:.95em}}
.meta{{font-size:.84em;margin:3px 0}}.meta .k{{color:var(--dim);font-variant:small-caps;margin-right:8px}}
.box{{border:1px dashed var(--line);border-radius:8px;padding:10px 16px;margin:22px 0;font-size:.9em}}
ul{{margin:.4em 0;padding-left:20px}}footer{{margin-top:50px;border-top:1px solid var(--line);padding-top:12px;font-size:.85em;color:var(--dim)}}</style>
</head><body><main>
<p class="dim"><a href="https://www.alexanarch.org/">Alexanarch</a> → Datasets → Refrain Index</p>
<h1>The Refrain Index</h1>
<p>A concordance of the contour integral across the archive: <strong>{total_deps:,} deposits bear the sign</strong>, in the variant families below. Counts and first attestations are harvested mechanically from the canonical bodies and regenerate as the archive grows; glosses are authored from the usage their exemplars show. Forms the harvest finds that no gloss yet covers are listed unglossed rather than guessed at. Machine surface: <a href="/datasets/refrain-index.json">refrain-index.json</a>.</p>
{rows}
<div class="box"><strong>Unglossed intake</strong> — heads the harvest found beyond the families above, awaiting a reader:<ul>{ung}</ul></div>
<div class="box"><strong>Reception.</strong> {esc(ds["reception"]["note"])}<br><br><strong>Collisions</strong> — the glyph's other lives:<ul>{col}</ul></div>
<p>{esc(ds["sign_doctrine"])}</p>
<footer>Generated {today} by scripts/build_refrain_index.py · CC BY-SA 4.0 · Lee Sharks · ∮ = 1</footer>
</main></body></html>"""
    out_dir = ROOT / "datasets/refrain-index"
    out_dir.mkdir(exist_ok=True)
    (out_dir / "index.html").write_text(page)
    print(f"refrain index: {total_deps:,} deposits bearing the sign; {len(entries)} families; "
          f"{len(ds['unglossed_intake'])} unglossed heads")
    print(f"wrote {out_json} + {out_dir}/index.html")


if __name__ == "__main__":
    main()
