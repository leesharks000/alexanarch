#!/usr/bin/env python3
"""sync_mint_mirrors.py — propagate the canonical /mint/ page to fleet mirrors.

SOURCE OF TRUTH: alexanarch/mint/index.html. Never edit mirror copies directly.
Config: data/mint-mirrors.json  →  {"mirrors": [{"repo": "...", "note": "..."}]}

Usage (in a TACHYON session with a fleet PAT):
  python3 scripts/sync_mint_mirrors.py --pat $PAT [--dry-run]

For each configured repo: clone shallow, write mint/index.html with a mirror
provenance banner injected (HTML comment; canonical bytes of the page proper
unchanged below the banner), commit + push only if changed. Idempotent.
"""
import argparse, json, subprocess, tempfile, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
BANNER = ("<!-- MINT MIRROR — canonical source: https://www.alexanarch.org/mint/ "
          "(repo leesharks000/alexanarch, path mint/index.html). Synced by "
          "scripts/sync_mint_mirrors.py; do not edit here. All computation is "
          "client-side; this mirror verifies identically to canon. -->\n")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pat', required=True)
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()
    src = (ROOT / 'mint' / 'index.html').read_text(encoding='utf-8')
    payload = BANNER + src
    kidx = (ROOT / 'api' / 'kernel-index.json').read_text(encoding='utf-8')
    cfg = json.loads((ROOT / 'data' / 'mint-mirrors.json').read_text())
    for m in cfg['mirrors']:
        repo = m['repo']
        print(f"── {repo}")
        with tempfile.TemporaryDirectory() as td:
            url = f"https://leesharks000:{a.pat}@github.com/leesharks000/{repo}.git"
            subprocess.run(['git','clone','-q','--depth','1',url,td], check=True)
            p = pathlib.Path(td) / 'mint'
            p.mkdir(exist_ok=True)
            f = p / 'index.html'
            ap = pathlib.Path(td) / 'api'; ap.mkdir(exist_ok=True)
            kf = ap / 'kernel-index.json'
            same = (f.exists() and f.read_text(encoding='utf-8') == payload and
                    kf.exists() and kf.read_text(encoding='utf-8') == kidx)
            if same:
                print('   unchanged'); continue
            if a.dry_run:
                print('   would update'); continue
            f.write_text(payload, encoding='utf-8')
            kf.write_text(kidx, encoding='utf-8')
            subprocess.run(['git','-C',td,'add','mint/index.html','api/kernel-index.json'], check=True)
            subprocess.run(['git','-C',td,'-c','user.email=tachyon@alexanarch.org',
                            '-c','user.name=TACHYON','commit','-q','-m',
                            'Sync /mint/ mirror from alexanarch canonical'], check=True)
            subprocess.run(['git','-C',td,'push','-q','origin','HEAD'], check=True)
            print('   updated + pushed')

if __name__ == '__main__':
    main()
