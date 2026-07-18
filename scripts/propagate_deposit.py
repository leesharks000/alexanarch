#!/usr/bin/env python3
"""propagate_deposit.py — post-mint propagation (spec v0.2 §7.2).

Wayback Save-Page-Now (anonymous) for a deposit's record page and canonical
text; records snapshot receipts into the external-metadata sidecar.
Usage: python3 scripts/propagate_deposit.py --deposit-number N
IPFS pinning: stub pending pinning-service credentials (MANUS).
"""
import argparse, json, pathlib, urllib.request, datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent

def spn(url):
    req = urllib.request.Request("https://web.archive.org/save/" + url,
                                 headers={"User-Agent": "alexanarch-propagate/0.1"})
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            loc = r.headers.get("Content-Location") or r.geturl()
            return {"requested": url, "status": r.status, "snapshot": loc,
                    "at": datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')}
    except Exception as e:
        return {"requested": url, "error": str(e)[:200]}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--deposit-number', type=int, required=True)
    n = ap.parse_args().deposit_number
    reg = json.loads((ROOT/'data/registry.json').read_text())
    d = next(x for x in reg['deposits'] if x['deposit_number'] == n)
    hexid = d['axn'].split(':')[1].split('.')[0]
    urls = [f"https://www.alexanarch.org/s/records/{n}/",
            f"https://www.alexanarch.org/data/texts/AXN-{hexid}-text.md"]
    receipts = [spn(u) for u in urls]
    side = ROOT/f'data/external-metadata/AXN-{hexid}.json'
    meta = json.loads(side.read_text()) if side.exists() else {}
    meta.setdefault('propagation', {}).setdefault('wayback', []).extend(receipts)
    side.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + '\n')
    for r in receipts: print(r)

if __name__ == '__main__':
    main()
