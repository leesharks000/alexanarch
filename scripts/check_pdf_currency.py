#!/usr/bin/env python3
"""check_pdf_currency.py — is every record's PDF present and current? (2026-11-10)

The HTML layer is what Google Scholar indexes, and each record page names its PDF in citation_pdf_url. Found on
2026-11-10: 22 ACTIVE records named a PDF that had never been built (HTTP 404), and reissued records kept PDFs rendered
before the reissue (their header page at the earlier title and version), because the builder's checkpoint hashed the
body alone. The builder now keys on the whole rendered input (wrapper and body); this check recomputes that key for every
record the builder would render and reports each one whose PDF is missing or whose checkpoint differs. It writes
data/pdf-currency.json and prints the count. A finding is recorded, never a failed build: the remedy is
`python3 scripts/build_deposit_pdfs.py --deposits <n,...>`, which deposit_pipeline.py's pdf stage and
propagate_record_state.py now run.

    python3 scripts/check_pdf_currency.py [--deposits n,n,...]"""
import json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build_deposit_pdfs as B


def key_for(d):
    n = d.get("deposit_number"); axn = d.get("axn", "")
    hx = axn.split(":")[1].split(".")[0] if ":" in axn and "." in axn else ""
    out = B.PAPERS_DIR / f"AXN-{hx.zfill(4) if hx else n}.pdf"
    body, _ = B._repaired_canonical(d) or B._load_body(hx, n)
    bs = (d.get("body_status") or {}).get("class", "full")
    if bs in B.FACSIMILE_CLASSES:
        return out, "facsimile"
    if not body and bs != "missing":
        return out, None
    body = body or "*No body text survives for this deposit. See §LACUNA above and the canonical record for surviving metadata.*"
    wrapper = B.build_wrapper_md(d, body)
    cleaned = B._clean_body_for_paper(B.strip_control_chars(body))
    return out, "w2:" + B.sha256_short(wrapper + "\n␞\n" + cleaned + ("\ncjk:" + B.CJK_FONT if B._has_cjk(wrapper + cleaned) else ""))


def main(argv):
    reg = json.loads(B.REGISTRY.read_text(encoding="utf-8"))["deposits"]
    want = None
    for a in argv:
        if a.startswith("--deposits"):
            want = {int(x) for x in a.split("=", 1)[1].split(",") if x.strip()}
    cp = B.load_checkpoint()
    missing, stale = [], []
    for d in reg:
        n = d.get("deposit_number")
        if not n or (want and n not in want):
            continue
        out, k = key_for(d)
        if k is None:
            continue
        if not out.exists():
            missing.append(n)
        elif k != "facsimile" and cp.get(str(n)) != k:
            stale.append(n)
    rep = {"rule": "every record the PDF builder renders has its PDF on disk, built from its current header and body",
           "missing": missing, "stale": stale}
    if want is None:
        (ROOT / "data/pdf-currency.json").write_text(json.dumps(rep, indent=1) + "\n", encoding="utf-8")
    print(f"pdf currency: {len(missing)} missing, {len(stale)} stale" + (f" — missing {missing[:15]}" if missing else "")
          + (f" — stale {stale[:15]}" if stale else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
