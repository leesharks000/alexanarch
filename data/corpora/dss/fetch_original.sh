#!/bin/bash
# Reproduce original/ from the pinned commit (EA-CORPORA-02/01)
set -e
PIN=f051578775b77b36164cfa16c402563d7d211a55
git clone --filter=blob:none --sparse https://github.com/ETCBC/dss.git /tmp/dss-repin
cd /tmp/dss-repin && git sparse-checkout set tf/1.9 docs/assets && git checkout $PIN
echo "verify against MANIFEST.sha256"
