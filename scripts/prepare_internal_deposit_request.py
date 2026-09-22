#!/usr/bin/env python3
"""Prepare a Transport D request body before mint.

Internal chat sessions may preserve LaTeX in their working manuscript while the
Alexanarch canonical body requires plain-text mathematical notation (MATH-001).
When packet.json sets "canonicalize_math": true, this script converts only the
### Body field with the archive's canonical detex implementation before mint.
The staged/source manuscript is not rewritten.

Any residual LaTeX macro fails closed before identity-bearing bytes are minted.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from detex_canonical import detex

EXTRA_SYMBOLS = {
    r"\\Pi": "Pi",
    r"\\iota": "iota",
    r"\\langle": "<",
    r"\\rangle": ">",
    r"\\ominus": "⊖",
    r"\\prec": "<",
    r"\\wedge": " and ",
    r"\\rm": "",
}


def canonicalize_body(issue_body: str) -> str:
    pattern = re.compile(
        r"(###\\s+Body\\s*\\n\\s*)(.*?)(?=\\n###\\s+Terms\\s*\\n|\\Z)",
        re.S | re.I,
    )
    match = pattern.search(issue_body)
    if not match:
        raise SystemExit("request has no ### Body field")

    source = match.group(2).rstrip()
    converted, _left = detex(source)
    for old, new in EXTRA_SYMBOLS.items():
        converted = converted.replace(old, new)

    residual = sorted(set(re.findall(r"\\\\[A-Za-z]+", converted)))
    if residual:
        raise SystemExit(
            "canonical math conversion left unsupported macro(s): "
            + ", ".join(residual[:20])
        )

    return issue_body[:match.start(2)] + converted.rstrip() + issue_body[match.end(2):]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--body", required=True)
    ap.add_argument("--packet", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    body_path = Path(args.body)
    packet = json.loads(Path(args.packet).read_text(encoding="utf-8"))
    text = body_path.read_text(encoding="utf-8")

    if packet.get("canonicalize_math") is True:
        text = canonicalize_body(text)
        print("canonicalized ### Body math to plain-text notation before mint")
    else:
        print("canonicalize_math not requested; request body copied unchanged")

    Path(args.output).write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
