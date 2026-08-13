#!/usr/bin/env python3
"""Assemble an authored capture record. Constants for the 2026-08-13 batch are
fixed; transcript, cite_list, analysis and finding are supplied per capture."""
import json, re, collections, pathlib
HERE = pathlib.Path(__file__).parent

def wc(s): return re.sub(r'[^0-9A-Za-z\u00C0-\u024F]', '', s or '')

def build(n, q, img, transcript, cites, analysis, finding, per, conditions=None, discards=None):
    raw = (HERE / f"src/raw-{n:02d}.txt").read_text()
    cardtext = "".join((c.get('site') or '')+(c.get('title') or '')+
                       (c.get('date_shown') or '')+(c.get('snip') or '') for c in cites)
    src = collections.Counter(wc(raw))
    parts = collections.Counter(wc(transcript) + wc(cardtext) + wc("".join((discards or {}).values())))
    missing, extra = sum((src-parts).values()), sum((parts-src).values())
    rec = {
        "q": q, "date": "2026-08-13", "surface": "Google AI Overview",
        "auth": {"authenticated": False, "incognito": True},
        "surface_basis": f"collapsed frame — All tab active, AI Overview panel present, {img}",
        "capture_conditions": conditions or {"interaction_required_to_reveal_more": True},
        "evidence": {"images": [{"filename": img,
            "repo_path": f"data/captures/{q.replace(' ','-').replace(':','-').replace('\"','')[:56]}-20260813/{img}",
            "resolved": False,
            "_note": "committed at repo root in 90bacc3d; moves to the capture directory at seating"}]},
        "transcript": transcript,
        "source_transcription": {"channel": "clipboard", "path": f"src/raw-{n:02d}.txt", "chars": len(raw)},
        "transcript_wrapper": {"status": "granted", "granted": "2026-08-13", "granted_by": "TACHYON",
            "operations": ["lineation restored","cards extracted","query echo removed","chrome discarded"],
            "card_count_basis": "AUTHORED against the frame; extractor output was a proposal only",
            "conservation": {"source_chars": len(wc(raw)), "missing": missing, "extra": extra,
                             "reconstructs": missing == 0 and extra == 0}},
        "cite_list": cites, "cites": len(cites),
        "analysis": analysis, "finding": finding, "per_v": per,
    }
    return rec

def emit(rec, n):
    p = HERE / f"capture-{n:02d}.json"
    p.write_text(json.dumps(rec, indent=2, ensure_ascii=False))
    c = rec["transcript_wrapper"]["conservation"]
    print(f"capture-{n:02d}  «{rec['q'][:44]}»  cites={rec['cites']:<3} "
          f"conservation {'OK' if c['reconstructs'] else 'FAIL missing=%d extra=%d'%(c['missing'],c['extra'])}")
    return p
