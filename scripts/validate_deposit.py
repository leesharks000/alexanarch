#!/usr/bin/env python3
"""
validate_deposit.py — validates deposit submissions against the canonical
protocol at api/deposit-protocol.json.

Used by:
    1. .github/workflows/mint-axn.yml — to reject malformed [DEPOSIT] issues
    2. .github/workflows/validate-registry.yml — pre-commit CI on PRs
    3. Local development — agents can run this before submitting

USAGE
═════
    # Validate an issue body (parsed from GitHub Issue)
    python3 scripts/validate_deposit.py --issue-body issue.md

    # Validate a single registry entry (JSON)
    python3 scripts/validate_deposit.py --registry-entry deposit.json

    # Validate the entire registry against all invariants
    python3 scripts/validate_deposit.py --registry data/registry.json

    # Strict mode (exit non-zero on any failure)
    python3 scripts/validate_deposit.py --strict ...

The exit code is 0 on success, 1 on validation failure, 2 on script error.

VALIDATION RULES
════════════════
Rules are defined in api/deposit-protocol.json under validation_rules.
Each failure is reported as: [<RULE_ID>] <description> (<context>)
"""

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

PROTOCOL_PATH = REPO_ROOT / "data" / "api" / "deposit-protocol.json"


def count_emoji_graphemes(s):
    """Approximate emoji grapheme count, accounting for VS/ZWJ."""
    if not s:
        return 0
    out = 0
    i = 0
    chars = list(s)
    while i < len(chars):
        ch = chars[i]
        cp = ord(ch)
        if 0xFE00 <= cp <= 0xFE0F or 0xE0100 <= cp <= 0xE01EF:
            i += 1
            continue
        if cp == 0x200D:
            i += 1
            if i < len(chars):
                i += 1
            continue
        if cp < 0x80:
            i += 1
            continue
        out += 1
        i += 1
    return out


def load_index():
    """Load the central protocol index. Returns None if it doesn't exist
    (allows backwards compatibility with environments that haven't deployed
    the index yet)."""
    idx_path = REPO_ROOT / "data" / "api" / "index.json"
    if not idx_path.exists():
        return None
    with open(idx_path) as f:
        return json.load(f)


def verify_index_consistency(idx):
    """Check that every protocol/schema entry in the index matches its file's
    actual content_sha256. Returns list of (rule_id, msg)."""
    import hashlib
    failures = []
    if not idx:
        return failures
    for section_name in ("protocols", "schemas"):
        for key, entry in idx.get(section_name, {}).items():
            path = entry.get("canonical_path", "")
            claimed = entry.get("content_sha256")
            if not claimed or not path:
                continue
            # public path stays /api/*.json (canonical, rewrite-backed); the
            # bytes live outside the functions namespace. Resolve to disk.
            disk = path.lstrip("/")
            if disk.startswith("api/") and disk.endswith(".json"):
                disk = "data/" + disk
            file_path = REPO_ROOT / disk
            if not file_path.exists():
                failures.append(("IDX-001",
                                 f"index references {path} ({section_name}/{key}) but file is missing"))
                continue
            actual = hashlib.sha256(file_path.read_bytes()).hexdigest()
            if actual != claimed:
                failures.append(("IDX-002",
                                 f"content_sha256 mismatch for {path} ({section_name}/{key}): "
                                 f"index claims {claimed[:16]}…, actual is {actual[:16]}…. "
                                 f"Run `python3 scripts/protocol_update.py --protocol {key} "
                                 f"--description '...'` to reconcile."))
    return failures


def load_protocol():
    with open(PROTOCOL_PATH) as f:
        return json.load(f)


def extract_field_from_issue_body(body, label):
    """Extract a `### Label` field from a GitHub Issue body."""
    pattern = rf"###\s+{re.escape(label)}\s*\n\s*(.*?)(?=\n###|\Z)"
    m = re.search(pattern, body, re.DOTALL | re.IGNORECASE)
    if m:
        val = m.group(1).strip()
        if val in ("_No response_", "None", ""):
            return ""
        return val
    return ""


def validate_issue_body(body, protocol):
    """Validate a deposit issue body against the protocol. Returns list of (rule_id, msg)."""
    failures = []
    current_pv = protocol["protocol_version"]

    # PV-001: protocol_version field present and matches current
    declared_pv = extract_field_from_issue_body(body, "Protocol Version")
    if not declared_pv:
        failures.append(("PV-001",
                         f"Missing required field '### Protocol Version'. "
                         f"Must equal '{current_pv}'. See {protocol['canonical_docs']['this_protocol']}."))
    elif declared_pv != current_pv:
        failures.append(("PV-001",
                         f"Protocol version mismatch. Declared '{declared_pv}', current is '{current_pv}'. "
                         f"Re-read {protocol['canonical_docs']['this_protocol']} and update."))

    # REQ-001..005: required fields present and non-empty
    required = protocol["required_deposit_fields"]
    label_map = {
        "title": "Title",
        "creator": "Creator",
        "description": "Description",
        "content_type": "Content Type",
        "license": "License",
        "substrate": "Substrate Disclosure",
    }
    for i, (field_key, label) in enumerate(label_map.items(), start=1):
        rule_id = f"REQ-{i:03d}"
        val = extract_field_from_issue_body(body, label)
        if not val:
            failures.append((rule_id, f"Missing or empty required field '### {label}'."))

    # Terms acknowledgement — must include the protocol-read confirmation
    terms_section = extract_field_from_issue_body(body, "Terms")
    if "deposit-protocol.json" not in terms_section and "I read the deposit protocol" not in terms_section:
        failures.append(("PV-002",
                         "Terms section must include the checked confirmation: "
                         "'- [x] I read the deposit protocol at https://alexanarch.org/api/deposit-protocol.json'"))

    return failures


# ─────────────────────────────────────────────────────────────────────────────
# REQUIRED-FIELD ENFORCEMENT ON THE REGISTRY ENTRY
#
# Added 2026-07-28 after deposit #1412 passed --strict with an empty title,
# creator, date, description, content_type and license, and reported 0 failures.
# The protocol has declared REQ-001..005 since v1; they were implemented only in
# validate_issue_body, i.e. only on the pre-mint path. Anything that wrote a
# registry entry by another route — a repair script, a direct edit, a pipeline
# stage — was never checked against them.
#
# A validator that reports success on a record with no title is worse than no
# validator: it converts an absent check into a positive assurance.
# ─────────────────────────────────────────────────────────────────────────────

# field -> (rule id, human description)
REQUIRED_ENTRY_FIELDS = {
    "title":         ("REQ-001", "title is non-empty"),
    "creator":       ("REQ-002", "creator is non-empty"),
    "description":   ("REQ-003", "description is non-empty"),
    "license":       ("REQ-004", "license is non-empty"),
    "substrate":     ("REQ-005", "substrate disclosure is non-empty"),
    "date":          ("REQ-006", "date is non-empty and ISO 8601 (YYYY-MM-DD)"),
    "content_type":  ("REQ-007", "content_type is non-empty"),
}

# the mechanical wiki template, emitted when the registry entry was empty.
# Its presence means the in-session authoring step was skipped.
WIKI_STUB = re.compile(r'^""\s+is a 0-word work by\s*,\s*dated\s*\.')
# TEMPLATE SHAPE (MANUS ruling 2026-08-05): the retired auto-generator emitted
# '"TITLE" is a N-word TYPE by CREATOR, dated DATE. It is registered as AXN:…
# under the FAMILY semantic family.' — the record's own fields read back. A
# deposit carrying this has no article, whatever the field length says.
WIKI_TEMPLATE = re.compile(
    # The generator emitted several surface forms of the same reverse-grep.
    # All of them restate the record's fields and then inscribe the AXN.
    r'(?:is a [\d,]+-word |is a recovered work with its full text seated'
    r'|is a \d+-word semi-restored record).{0,200}?'
    r'It is registered as AXN:', re.S)
WIKI_MIN_WORDS = 40


# Rules added 2026-07-28 bind deposits minted from that date. Earlier deposits
# carry 245 pre-existing failures — overwhelmingly WIKI-001, from the period when
# the in-session authoring step was not enforced. Those are a remediation backlog,
# reported under --backlog, and are not blocking: making them blocking would stop
# every future deposit until the backlog cleared, which puts the cost back on the
# archive instead of on the handler who skips a procedure today.
ENFORCEMENT_FROM = "2026-07-28"
ENFORCE_ALL = [False]   # set by --backlog


def _minted_on_or_after(entry, iso):
    m = str(entry.get("minted_at") or entry.get("date") or "")
    return m[:10] >= iso if len(m) >= 10 else False


def validate_entry_required_fields(entry, enforce_all=False):
    """REQ-001..007, BODY-001, WIKI-001. Returns list of (rule_id, msg).

    Binding for deposits minted on or after ENFORCEMENT_FROM. For earlier
    deposits the same checks run under --backlog and report without blocking."""
    if not enforce_all and not _minted_on_or_after(entry, ENFORCEMENT_FROM):
        return []
    failures = []
    for field, (rid, desc) in REQUIRED_ENTRY_FIELDS.items():
        v = entry.get(field)
        if v is None or (isinstance(v, str) and not v.strip()):
            failures.append((rid, f"{desc} — deposit #{entry.get('deposit_number')} has {field}={v!r}"))
    d = entry.get("date")
    if isinstance(d, str) and d.strip() and not re.match(r"^\d{4}-\d{2}-\d{2}$", d.strip()):
        failures.append(("REQ-006", f"date must be ISO 8601 YYYY-MM-DD; got {d!r}"))

    # MATH-001 (ratified 2026-08-12, MANUS, after deposits #1452-#1454).
    # LaTeX renders in a PDF. The CANONICAL BODY is what the record page, the
    # wiki, the body index, the OAI dissemination and every machine reader
    # actually see, and there it is raw backslash macros — a reader meets
    # "\[ X_0 \xrightarrow{T_1} X_1 \]" where the paper says an acquisition
    # chain. Canonical text therefore uses PLAIN-TEXT mathematical notation;
    # scripts/detex_canonical.py performs the conversion.
    _hex = entry.get("hex")
    if _hex:
        _p = REPO_ROOT / "data" / "texts" / f"AXN-{_hex}-text.md"
        if _p.exists():
            try:
                _t = _p.read_text(encoding="utf-8")
            except Exception:
                _t = ""
            # YAML frontmatter carries strings with escaped \n; not LaTeX.
            if _t.startswith("---"):
                _j = _t.find("\n---\n", 3)
                if _j > 0:
                    _t = _t[_j + 5:]
            _disp = len(re.findall(r"\\\[", _t)) + _t.count("$$") // 2
            _inl = len(re.findall(r"\\\(", _t))
            _mac = len(set(m for m in re.findall(r"\\[A-Za-z]{2,}", _t) if m[1] not in "ntr" or len(m) < 3 or m[2].islower() is False))
            if _disp or _inl or _mac:
                failures.append((
                    "MATH-001",
                    f"canonical text carries LaTeX ({_disp} display, {_inl} inline, "
                    f"{_mac} distinct macros); use plain-text notation in the body "
                    f"(LaTeX is fine in the PDF) — run "
                    f"scripts/detex_canonical.py --deposits {entry.get('deposit_number')} --apply"))

    # TEXT-001 / IMG-001 (2026-08-09, mint-forward from #1445; #1443/#1444 are
    # the precedent defects, sealed and grandfathered like the WIKI-001 cohort
    # above). TEXT-001: canonical bodies FLOW — a hard-wrapped body renders as
    # fragment-paragraphs and its wraps are frozen into the identity-bearing
    # bytes forever; reject BEFORE sealing. Detector mirrors wire_deposit W14:
    # mid-length prose lines without terminal punctuation whose next line
    # continues lowercase. IMG-001: every body image reference must resolve to
    # a staged file — an image the record promises and does not hold is a
    # broken deposit at birth.
    try:
        _dn = int(entry.get("deposit_number") or 0)
    except Exception:
        _dn = 0
    if _dn >= 1445:
        from pathlib import Path as _P
        _root = _P(__file__).resolve().parent.parent
        _tp = str(entry.get("full_text_path") or "").lstrip("/")
        _body = ""
        if _tp and (_root / _tp).exists():
            _raw = (_root / _tp).read_text(encoding="utf-8")
            # FRONTMATTER IS AT THE TOP OR IT IS NOT FRONTMATTER (2026-08-09).
            # This split on "\n---\n" was meant to drop a YAML header, but --- is
            # also a markdown horizontal rule, so on any body carrying rules it kept
            # only the text after the LAST one. On #1445 that was 566 of 11,842
            # characters: TEXT-001 was inspecting 5% of the deposit and reporting a
            # pass on the other 95%. Same defect as the regex that ate 25,023
            # characters of a document and the decimal point that broke the
            # forensics strip — a pattern written against how a marker LOOKS rather
            # than where it can legally appear. Frontmatter is anchored at position
            # zero and nowhere else.
            import re as _reF
            _mF = _reF.match(r"^---\n.*?\n---\n", _raw, _reF.S)
            _body = _raw[_mF.end():] if _mF else _raw
        if _body:
            _lines = _body.split("\n")
            _pi = [i for i, l in enumerate(_lines)
                   if l.strip() and l[:1] not in (" ", "\t")
                   and not l.lstrip().startswith(("#", "|", "-", ">", "`", "!", "<"))]
            def _nx(i):
                for j in range(i + 1, len(_lines)):
                    if _lines[j].strip():
                        return _lines[j].lstrip()
                return ""
            # ONE DEFINITION OF THE DEFECT, shared with the repair (2026-08-09).
            # The previous detector flagged mid-length lines lacking terminal
            # punctuation whose successor continued lowercase. That fires on
            # ENJAMBMENT, which is a poet's deliberate break, and it happened not to
            # fire on the archive's verse only because those bodies yielded a single
            # candidate line each — luck, not robustness.
            #
            # MANUS: an artificially rendered linebreak due to container width is not
            # a linebreak; a deliberately encoded linebreak or tab is. The signal that
            # separates them is MECHANICAL REGULARITY. A tool wrapping at a column
            # leaves every line but the last crowding the same maximum. Verse does not,
            # because its lines are chosen.
            #
            # scripts/unwrap_deposit.py holds that test and is deliberately built to
            # refuse: it skips indented blocks, markers, fenced code, markdown hard
            # breaks, and any run under three lines. Validation now asks it directly,
            # so the thing that detects a wrap and the thing that repairs one can never
            # disagree.
            _uw = 0
            try:
                import importlib.util as _ilu
                _spec = _ilu.spec_from_file_location(
                    "_unwrap", str(_root / "scripts" / "unwrap_deposit.py"))
                _m = _ilu.module_from_spec(_spec)
                _spec.loader.exec_module(_m)
                _, _uw = _m.unwrap(_body)
            except Exception:
                _uw = 0
            _wr = list(range(_uw))
            # The guard my own edit deleted. Replacing a detector without keeping
            # the condition that consumes it made TEXT-001 fire on every deposit,
            # including one it had just been used to repair — a check that always
            # fails is exactly as useless as one that never can.
            if _uw >= 3:
                failures.append(("TEXT-001",
                    f"body carries {_uw} mechanically wrapped line break(s); "
                    "canonical bodies flow — wrapping is display's job and sealed "
                    "bytes cannot be reflowed later. Run scripts/unwrap_deposit.py, "
                    "which preserves verse, indentation, lists, tables and code"))
            import re as _re
            for _ref in _re.findall(r"!\[[^\]]*\]\((/(?:data/attachments|files)/[^\s\)]+)\)", _body):
                if not (_root / _ref.lstrip("/")).exists():
                    failures.append(("IMG-001",
                        f"body image reference does not resolve on disk: {_ref}"))

    # BODY-001: canonical bytes must not be a template stub.
    bs = entry.get("body_status") or {}
    wc = bs.get("word_count") if isinstance(bs, dict) else None
    if isinstance(wc, int) and wc < 25 and str(bs.get("class")) not in ("pointer", "tether", "notice"):
        failures.append(("BODY-001",
                         f"canonical bytes are {wc} words — below the threshold at which a deposit "
                         f"can be distinguished from an unfilled template. If this is intentional, "
                         f"set body_status.class to pointer, tether or notice."))

    # WIKI-001: the wiki article must have been authored, not templated.
    wa = str(entry.get("wiki_article") or "")
    if not wa.strip():
        failures.append(("WIKI-001", "wiki_article is empty; internal deposits author it in-session "
                                     "(see deposit_pipeline.py, transport D)"))
    elif WIKI_STUB.match(wa.strip()):
        failures.append(("WIKI-001", "wiki_article is the mechanical template stub, which means the "
                                     "in-session authoring step was skipped"))
    elif WIKI_TEMPLATE.search(wa):
        failures.append(("WIKI-002", "wiki_article carries the RETIRED auto-generator's shape "
                                     "('is a N-word TYPE by CREATOR, dated DATE. It is registered as AXN:…') "
                                     "— the record's own fields read back, not an article about the work. "
                                     "Write it from the body."))
    elif len(wa.split()) < WIKI_MIN_WORDS:
        failures.append(("WIKI-003", f"wiki_article is {len(wa.split())} words; an article that describes "
                                     f"the work runs to at least {WIKI_MIN_WORDS}. A one-sentence gloss of "
                                     "the record header is not an article."))
    return failures


def validate_registry_entry(entry, protocol):
    """Validate a single registry entry."""
    failures = []
    rules = {r["id"]: r for r in protocol["validation_rules"]["rules"]}

    # AXN-001: AXN format
    axn = entry.get("axn", "")
    if not re.match(r"^AXN:[0-9A-F]{2,4}\.[A-Z]+\.[^.]{1,}$", axn):
        failures.append(("AXN-001", f"AXN does not match canonical format: {axn!r}"))

    # AXN-002: emoji count = 6
    parts = axn.split(".", 2)
    if len(parts) >= 3:
        emoji = parts[2]
        n = count_emoji_graphemes(emoji)
        if n != 6:
            failures.append(("AXN-002", f"AXN emoji must be 6 graphemes per AXN v2; got {n} in {axn!r}"))

    # AXN-003: hash is 64-char hex
    h = entry.get("hash", "")
    if not re.match(r"^[0-9a-f]{64}$", h or ""):
        failures.append(("AXN-003", f"hash must be a 64-char lowercase hex SHA-256; got {h!r}"))

    failures.extend(validate_entry_required_fields(entry, enforce_all=ENFORCE_ALL[0]))

    return failures


def validate_registry(reg, protocol):
    """Validate the full registry against consistency invariants."""
    failures = []

    # CONSISTENCY-001: total_deposits == len(deposits)
    if reg.get("total_deposits") != len(reg.get("deposits", [])):
        failures.append(("CONS-001",
                         f"total_deposits ({reg.get('total_deposits')}) != len(deposits) ({len(reg.get('deposits', []))})"))

    # AXN-004: deposit_numbers are contiguous from 1
    deposit_numbers = [d.get("deposit_number") for d in reg["deposits"]]
    if sorted(deposit_numbers) != list(range(1, len(deposit_numbers) + 1)):
        failures.append(("AXN-004",
                         f"deposit_numbers are not contiguous 1..N (N={len(deposit_numbers)})"))

    # Per-entry validation
    for d in reg["deposits"]:
        entry_failures = validate_registry_entry(d, protocol)
        for rid, msg in entry_failures:
            failures.append((rid, f"#{d.get('deposit_number')}: {msg}"))

    return failures


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--issue-body", type=Path, help="path to a GitHub Issue body markdown file")
    parser.add_argument("--registry-entry", type=Path, help="path to a single deposit JSON")
    parser.add_argument("--registry", type=Path, help="path to data/registry.json (full validation)")
    parser.add_argument("--strict", action="store_true", help="exit non-zero on any failure")
    args = parser.parse_args()

    protocol = load_protocol()
    idx = load_index()
    all_failures = []
    targets_validated = 0

    # Index consistency is checked every time — if the central index disagrees
    # with the protocol files on disk, the whole validation chain is suspect.
    if idx:
        idx_failures = verify_index_consistency(idx)
        if idx_failures:
            all_failures.extend(idx_failures)
            print(f"Index consistency check: {len(idx_failures)} failure(s)")
        else:
            print(f"Index consistency check: OK ({idx.get('index_version')})")

    if args.issue_body:
        with open(args.issue_body) as f:
            body = f.read()
        failures = validate_issue_body(body, protocol)
        all_failures.extend(failures)
        targets_validated += 1
        print(f"Validated issue body {args.issue_body}: {len(failures)} failure(s)")

    if args.registry_entry:
        with open(args.registry_entry) as f:
            entry = json.load(f)
        failures = validate_registry_entry(entry, protocol)
        all_failures.extend(failures)
        targets_validated += 1
        print(f"Validated registry entry: {len(failures)} failure(s)")

    if args.registry:
        with open(args.registry) as f:
            reg = json.load(f)
        failures = validate_registry(reg, protocol)
        all_failures.extend(failures)
        targets_validated += 1
        print(f"Validated registry ({len(reg['deposits'])} deposits): {len(failures)} failure(s)")

    if targets_validated == 0:
        print("No targets specified. Pass --issue-body, --registry-entry, or --registry.")
        sys.exit(2)

    if all_failures:
        print()
        print("FAILURES:")
        for rid, msg in all_failures:
            print(f"  [{rid}] {msg}")
        print()
        print(f"Current protocol_version: {protocol['protocol_version']}")
        print(f"Protocol JSON: {protocol['canonical_docs']['this_protocol']}")
        print(f"Deposit flow doc: {protocol['canonical_docs']['deposit_flow']}")
        if args.strict:
            sys.exit(1)
    else:
        print()
        print(f"✓ All checks passed against protocol {protocol['protocol_version']}")


if __name__ == "__main__":
    main()
