#!/bin/sh
# deletion-semantics-cross-implementation-test v1.0 — full reproduction from clean clones.
# Pins in sources/source-lock.json. Requires python3 (stdlib only) and git.
set -e
git clone https://github.com/andrewcrenshaw/remember-okf-sample-bundle && \
  git -C remember-okf-sample-bundle checkout ea18185f49948a6832e052a1f0c9c6a935076b95
git clone https://github.com/inkxel/throughline && \
  git -C throughline checkout c512e8b9e77803b5b59be703caaad02c74b80d92
curl -sLO https://www.alexanarch.org/datasets/deletion-conformance-fixture/cases.json
CK=throughline/scripts/never_landed.py
CP='\*\*(?:Record|Lesson) created\*\*: lesson ([a-z0-9-]+)'
CB='\*\*Lesson created\*\*: lesson ([a-z0-9-]+)'
echo "== 01 baseline: fixture mode (reproduces inkxel 2026-07-29) =="
python3 $CK --fixture cases.json --json
echo "== 01 baseline: log mode on the published bundle (reproduces crenshaw 2026-07-31) =="
(cd remember-okf-sample-bundle && sha256sum -c SHA256SUMS)
python3 $CK --log remember-okf-sample-bundle/bundle/log.md --store remember-okf-sample-bundle/bundle --claim-pattern "$CB" --json
echo "== 01 negative: --id-key at a nonexistent key =="
python3 $CK --log remember-okf-sample-bundle/bundle/log.md --store remember-okf-sample-bundle/bundle --claim-pattern "$CB" --id-key nosuchkey --json
echo "== 02/03 translation, both modes, with receipts =="
python3 translator/receipt.py
echo "== 04 A/B/C collision (current consumer) =="
python3 $CK --log fixtures/abc/source/log.md --store fixtures/abc/source/store --claim-pattern "$CB" --json
echo "== 05/06 necessity + sufficiency =="
python3 translator/repair.py
echo "== 07 corpus tombstone fit =="
python3 translator/tomb.py
