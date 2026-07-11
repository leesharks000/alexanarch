#!/usr/bin/env python3
"""EA-EROSION registry-wide sweep: per-client findable-DOI counts across all of DataCite.

Method (EA-EROSION-01, deposit #1045, extended registry-wide per MANUS directive 2026-07-11):
  1. Enumerate all clients: GET api.datacite.org/clients (paginated, page[size]=1000)
  2. Per client: GET api.datacite.org/dois?client-id={id}&page[size]=1 -> meta.total
  3. Emit dated epoch capture; deltas between epochs = the public severance signal.
Rate discipline (empirical, 2026-07-11): <=6 concurrent, ~6 req/s ceiling, exponential backoff;
resumable — pass a prior partial epoch file to fill only missing counts.
"""
import json, sys, time, datetime, urllib.request, concurrent.futures

API = "https://api.datacite.org"

def get(url, timeout=25):
    req = urllib.request.Request(url, headers={"User-Agent": "EA-EROSION-01 sweep (alexanarch.org; leesharks00@gmail.com)"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)

def enumerate_clients():
    clients, page = {}, 1
    while True:
        d = get(f"{API}/clients?page%5Bsize%5D=1000&page%5Bnumber%5D={page}")
        for c in d["data"]:
            clients[c["id"]] = c["attributes"].get("name", "")[:80]
        if len(d["data"]) < 1000:
            return clients
        page += 1

def count(cid):
    for attempt in range(4):
        try:
            return cid, get(f"{API}/dois?client-id={cid}&page%5Bsize%5D=1")["meta"]["total"]
        except Exception:
            time.sleep(1.5 * (attempt + 1))
    return cid, None

def main():
    resume = json.load(open(sys.argv[1])) if len(sys.argv) > 1 else None
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    names = resume["client_names"] if resume else enumerate_clients()
    counts = dict(resume["per_client_findable"]) if resume else {}
    todo = [c for c in names if counts.get(c) is None]
    registry_total = get(f"{API}/dois?page%5Bsize%5D=1")["meta"]["total"]
    print(f"epoch sweep {now}: {len(todo)} clients to count; registry total findable {registry_total:,}")
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
        for i, (cid, n) in enumerate(ex.map(count, todo)):
            counts[cid] = n
            if i % 250 == 0:
                print(f"  {i}/{len(todo)}")
            time.sleep(0.03)
    failed = [c for c, v in counts.items() if v is None]
    out = {
        "captured_at": now,
        "registry_total_findable": registry_total,
        "clients_enumerated": len(names),
        "per_client_findable": counts,
        "client_names": names,
        "failed_counts": failed,
        "sum_of_client_totals": sum(v for v in counts.values() if v),
        "epoch_status": "COMPLETE" if not failed else f"PARTIAL — {len(failed)} counts missing",
        "method": "clients enumeration + per-client meta.total; 6-way parallel, backoff; EA-EROSION-01 registry-wide extension",
    }
    fn = f"data/datacite-registrywide-{now[:10]}.json"
    json.dump(out, open(fn, "w"), separators=(",", ":"))
    print(f"wrote {fn}: {out['epoch_status']}; sum {out['sum_of_client_totals']:,}")

if __name__ == "__main__":
    main()
