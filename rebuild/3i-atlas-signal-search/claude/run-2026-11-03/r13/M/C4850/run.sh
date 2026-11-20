#!/bin/bash
cd "$(dirname "$0")"; export SSL_CERT_FILE=/root/.ccr/ca-bundle.crt; cc=$1
for s in 0013 0014 0015 0016 0017 0018; do [ -f v_cc${cc}_$s.npz ] || python3 c4850v.py $cc $s >> c$cc.log 2>&1; done
echo "cc$cc DONE" >> c$cc.log
