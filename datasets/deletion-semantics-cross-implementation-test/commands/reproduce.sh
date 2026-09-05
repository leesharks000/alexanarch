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
echo "== 08 the producer's own repair, live (v1.1, 2026-09-03) =="
git -C remember-okf-sample-bundle fetch -q --tags && git -C remember-okf-sample-bundle checkout -q 55e6493945a51c77e8a002630dc4890e90d7123e
(cd remember-okf-sample-bundle && sha256sum -c SHA256SUMS)
python3 translator/live_repair.py remember-okf-sample-bundle
git -C remember-okf-sample-bundle checkout -q pre-absence-records
echo "== 09 the key-form repair, live (v1.2, 2026-09-05) =="
git -C remember-okf-sample-bundle fetch -q --tags && git -C remember-okf-sample-bundle checkout -q 3806111cad1a058585242f7ad78716c4a767c782
(cd remember-okf-sample-bundle && sha256sum -c SHA256SUMS)
python3 translator/key_form.py remember-okf-sample-bundle
git -C remember-okf-sample-bundle checkout -q pre-absence-records
