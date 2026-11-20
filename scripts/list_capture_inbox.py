#!/usr/bin/env python3
"""list_capture_inbox.py — transcripts received through /ask/ (api/submit-transcript.js), not yet seated.

Each entry is drafts/capture-inbox/<day>/<sha12>.json. An entry is seated when an intake draft built from it has been
seated (scripts/capture_intake.py) and the entry carries "seated_as": "<slug>". Usage: python3 scripts/list_capture_inbox.py
"""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
n = 0
for p in sorted((ROOT / 'drafts' / 'capture-inbox').glob('*/*.json')):
    e = json.loads(p.read_text())
    if e.get('seated_as'): continue
    n += 1
    print(f"{p.relative_to(ROOT)}  {e.get('received_at','')[:16]}  {e.get('surface')}  {e.get('date_run')}  "
          f"{e.get('transcript_bytes')} B  {e.get('submitter') or '-'}\n    {e.get('query','')[:150]}")
print(f'{n} unseated')
