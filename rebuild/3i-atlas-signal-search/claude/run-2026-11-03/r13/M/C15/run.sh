#!/bin/bash
cd "$(dirname "$0")"; export SSL_CERT_FILE=/root/.ccr/ca-bundle.crt
for s in 0013 0014 0015 0016 0017 0018; do [ -f ../out2/cc15_$s.npz ] || (cd .. && python3 mv.py 15 $s) >> c15.log 2>&1; done
python3 c15z.py > z.json 2>> c15.log && echo "z done" >> c15.log
for s in 0013 0014 0015 0016 0017 0018; do [ -f v_$s.npz ] || python3 c15v.py $s >> c15.log 2>&1; done
echo "C15 DONE" >> c15.log
