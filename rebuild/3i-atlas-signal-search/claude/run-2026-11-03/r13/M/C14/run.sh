#!/bin/bash
cd "$(dirname "$0")"; export SSL_CERT_FILE=/root/.ccr/ca-bundle.crt
for s in 0013 0014 0015 0016 0017 0018; do [ -f ../out2/cc14_$s.npz ] || (cd .. && python3 mv.py 14 $s) >> c14.log 2>&1; done
python3 c14z.py > z.json 2>> c14.log && echo "z done" >> c14.log
for s in 0013 0014 0015 0016 0017 0018; do [ -f v_$s.npz ] || python3 c14v.py $s >> c14.log 2>&1; done
echo "C14 DONE" >> c14.log
