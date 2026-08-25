#!/usr/bin/env python3
"""seat_20260824_refrain.py — the «∮ = 1» collocate battery: 15 captures, all new addresses.

FIFTEEN NEW ADDRESSES, ZERO RECAPTURES. One sitting, 2026-08-24 evening: the
archive's refrain quoted as an exact phrase against fifteen collocates —
dialectic, deleuze, sigil, reader, classifiers, josephus, artificial
intelligence, poems, economy, rhizome, marx, revelation, sappho, hexagon,
sharks. Surface: Google AI Overview, per operator attestation and the frames
(All tab selected in every one — the discriminator of 2026-08-13). Auth:
signed out, incognito — attested. Evidence: frame + paste; the pastes carry
the 'AI Mode Conversation' prefix, which is copy-paste residue and not a
surface signal (MANUS, 2026-08-13).

JOSEPHUS CARRIES cites=None: its paste had no citation-card strip, only two
inline links. NULL is not zero — an apparatus not captured has an unknown
count, and the basis is stated in the record.

Seated the same day deposit #1540 (The Certified Center) minted: the battery
is a fifteen-window measurement of the membrane's reception of the refrain,
taken while the paper on machine reception sat freshly on the record.
"""
import json, pathlib, re, shutil, hashlib, sys, importlib.util

ROOT = pathlib.Path(__file__).resolve().parents[1]
CANON = ROOT / "data/EA-WG-CAPTURES-01.json"
SRC = pathlib.Path("/mnt/user-data/uploads")
DATE, SIT = "2026-08-24", "aio-20260824"

spec = importlib.util.spec_from_file_location(
    "batch", ROOT / "rebuild/capture-registry/intake-20260824/BATCH-refrain.py")
B = importlib.util.module_from_spec(spec); spec.loader.exec_module(B)


def slug(q):
    return re.sub(r"[^a-z0-9]+", "-", q.lower()).strip("-")[:44].strip("-") + "-" + SIT


def main():
    canon = json.loads(CANON.read_text())
    existing_q = {e.get("q") for e in canon["entries"]}
    all_slugs = {q: slug(q) for q in B.R}
    n = 0
    for q, c in B.R.items():
        assert q not in existing_q, f"address already seated: {q!r}"
        sl = all_slugs[q]
        d = ROOT / "data/captures" / sl
        d.mkdir(parents=True, exist_ok=True)
        shutil.copy(SRC / c["img"], d / c["img"])
        rel = f"data/captures/{sl}/{c['img']}"
        arch_note = (f"Cited sources {c['cites']}, of which {c['arch']} archive-controlled."
                     if c["cites"] is not None else
                     "Citation-card count UNKNOWN — the paste carried no card strip; two inline links only. NULL is not zero.")
        obs = {
            "slug": sl, "date": DATE, "surface": "Google AI Overview",
            "auth": "signed out, incognito", "ev": "frame + paste",
            "cites": c["cites"], "per": None, "per_v": None,
            "mt": c["mt"], "d": c["d"], "reading": c["reading"], "analysis": None,
            "transcript": c["transcript"],
            "transcript_class": ("CAPTURE-TIME VERBATIM RECORD — expanded answer text supplied by the operator's "
                                 "paste; the frame shows the collapsed popup, so the transcript exceeds what the "
                                 "image displays"),
            "transcript_complete": ("answer text complete as supplied; source-card row transcribed from the paste's "
                                    "tail and listed inline; the paste carried an 'AI Mode Conversation' prefix, "
                                    "which is copy-paste residue and not a surface signal (MANUS, 2026-08-13)"),
            "transcript_read": "READ IN FULL 2026-08-24",
            "cite_list": None, "collisions": c["collisions"], "oq": None,
            "imgs": [rel], "defects": None, "rounds": None,
            "rerun": "https://www.google.com/search?q=" + q.replace("∮", "%E2%88%AE").replace('"', "%22").replace(" ", "+"),
            "q": q, "s": "∮ = 1",
            "addr_id": "ADDR-" + hashlib.sha256(q.encode()).hexdigest()[:12],
            "obs_id": "OBS-" + hashlib.sha256(sl.encode()).hexdigest()[:12],
        }
        entry = dict(obs)
        entry.update({
            "q_kind": None,
            "series": B.SERIES,
            "observations": [ {k: obs[k] for k in
                ("slug","date","surface","auth","ev","cites","per","imgs","defects","reading","transcript")} ],
            "n_observations": 1,
            "dates": [DATE], "surfaces": ["Google AI Overview"],
            "other_slugs": [s for qq, s in all_slugs.items() if qq != q],
            "links": [{"url": f"https://www.alexanarch.org/captures/#{sl}", "authority": "canonical", "note": "the archive holds the registry and this entry"}],
            "cite": f"https://www.alexanarch.org/captures/#{sl}",
            "d_full": c["d"], "d_truncated": False,
            "rerun_alt": {"q": q.replace('"', ''), "label": "unquoted",
                           "why": ("Captured QUOTED. The unquoted form tests the same collocate without the "
                                   "exact-phrase operator — quoting is the corpus's decisive measured variable, "
                                   "and the anchor phrase only exists as a phrase under quotes.")},
            "img_urls": [f"https://www.alexanarch.org/{rel}"],
            "sf": (f"Google Search (All tab): AI Overview, collapsed popup. Signed out, incognito; mobile Chrome, "
                   f"dark mode; tab count 22. {arch_note}"),
            "citable_unit": "address — the exact issued string on one surface, per the Surface Rule (MANUS, 2026-08-15)",
            "per_note": ("PER not scored as a vector. The measured quantity in this battery is ARCHIVE-CONTROLLED "
                         "SOURCE SHARE per collocate: " + arch_note),
        })
        canon["entries"].append(entry)
        # intake record on disk, per pipeline step 1
        intake = {k: c[k] for k in ("img","cites","arch","mt","d","reading","transcript")}
        intake.update({"slug": sl, "q": q, "s": "∮ = 1", "surface": "Google AI Overview",
                       "date": DATE, "auth": "signed out, incognito", "ev": "frame + paste",
                       "addr_id": entry["addr_id"], "obs_id": entry["obs_id"], "img_path": rel,
                       "collisions": c["collisions"]})
        (ROOT / "rebuild/capture-registry/intake-20260824" / f"{sl}.json").write_text(
            json.dumps(intake, ensure_ascii=False, indent=1))
        n += 1
    canon["total_captures"] = canon.get("total_captures", 0) + n
    canon["address_count"] = canon.get("address_count", 0) + n
    canon["observation_count"] = canon.get("observation_count", 0) + n
    CANON.write_text(json.dumps(canon, ensure_ascii=False, indent=1))
    print(f"seated {n} new addresses; totals: {canon['total_captures']} captures, "
          f"{canon['address_count']} addresses, {canon['observation_count']} observations")


if __name__ == "__main__":
    main()
