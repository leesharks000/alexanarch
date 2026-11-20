#!/bin/bash
cd "$(dirname "$0")"; export SSL_CERT_FILE=/root/.ccr/ca-bundle.crt
for s in 0013 0014 0015 0016 0017 0018; do [ -f v_$s.npz ] || python3 c19v.py $s >> c19.log 2>&1; done
echo "C19 DONE" >> c19.log
