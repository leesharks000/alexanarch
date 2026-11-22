"""Attach a recorded read-aloud (e.g. Chrome's AI playback) to a record page as audio.

    python3 scripts/attach_playback.py DEPOSIT_NUMBER RECORDING [--source "Chrome AI playback (Android)"]
        [--recorded "2026-11-21 21:16 EST"] [--label "Listen: AI playback"] [--note "..."]

RECORDING may be a screen recording (.mp4) or an audio file. From a video the audio stream is copied
out without re-encoding (ffmpeg -vn -c:a copy); the recording's own sha256 is kept with the entry.
The audio is served beside the record page (s/records/N/AXN-HEX-playback-…), listed in the registry
entry's `playback`, logged as a modification, and rendered as the page's player. The canonical file,
and so the AXN, is not touched (operator, 2026-11-21 21:54: "nothing that changes the axn")."""
import argparse, datetime, hashlib, json, os, pathlib, shutil, subprocess, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "scripts"))


def sha(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("n", type=int); ap.add_argument("rec")
    ap.add_argument("--source", default="Chrome AI playback (Android)"); ap.add_argument("--recorded", default=None)
    ap.add_argument("--label", default="Listen: AI playback"); ap.add_argument("--note", default=None)
    a = ap.parse_args()
    from record_modification import touch
    rp = ROOT / "data/registry.json"; reg = json.loads(rp.read_text())
    d = next(x for x in reg["deposits"] if x["deposit_number"] == a.n); hx = str(d.get("hex") or "").zfill(4)
    probe = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type,codec_name",
                                       "-of", "json", a.rec], capture_output=True, text=True, check=True).stdout)
    codecs = {s["codec_type"]: s["codec_name"] for s in probe["streams"]}; assert "audio" in codecs, "no audio stream"
    ext = {"aac": "m4a", "mp3": "mp3", "opus": "ogg", "vorbis": "ogg"}.get(codecs["audio"], "m4a")
    day = (a.recorded or datetime.date.today().isoformat())[:10].replace("-", "")
    k = 1 + sum(1 for p in (d.get("playback") or []) if day in p.get("file", ""))
    name = f"AXN-{hx}-playback-{day}{'' if k == 1 else '-' + str(k)}.{ext}"
    out = ROOT / "s/records" / str(a.n) / name; out.parent.mkdir(parents=True, exist_ok=True)
    if "video" in codecs:
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a.rec, "-vn", "-c:a", "copy", str(out)], check=True); method = "audio stream copied from a screen recording, not re-encoded"
    else:
        shutil.copyfile(a.rec, out); method = "audio file as recorded"
    dur = float(json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(out)],
                                          capture_output=True, text=True, check=True).stdout)["format"]["duration"])
    entry = {"file": f"/s/records/{a.n}/{name}", "label": a.label, "source": a.source, "recorded": a.recorded, "duration_s": round(dur, 2),
             "bytes": out.stat().st_size, "sha256": sha(out), "codec": codecs["audio"], "method": method,
             "recording_sha256": sha(a.rec), "recording_bytes": os.path.getsize(a.rec), "note": a.note}
    entry = {k2: v for k2, v in entry.items() if v is not None}
    d.setdefault("playback", []).append(entry)
    from zoneinfo import ZoneInfo
    local = datetime.datetime.now(ZoneInfo("America/Detroit")).date().isoformat()   # Michigan local, as the archive dates
    touch(d, "playback", f"audio playback attached ({a.source}); presentation only, the canonical file and AXN untouched", now=entry["file"], when=local)
    rp.write_text(json.dumps(reg, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(entry, ensure_ascii=False, indent=1))
    print(f"now re-render: python3 scripts/deposit_pipeline.py --deposit-number {a.n} --stages validate,record --no-push")


if __name__ == "__main__":
    main()
