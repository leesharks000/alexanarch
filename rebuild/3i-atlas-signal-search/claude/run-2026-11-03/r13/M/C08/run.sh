#!/bin/bash
cd "$(dirname "$0")"; export SSL_CERT_FILE=/root/.ccr/ca-bundle.crt
for s in 0013 0014 0015 0016 0017 0018; do [ -f ../out2/cc08_$s.npz ] || (cd .. && python3 mv.py 8 $s) >> c08.log 2>&1; done
python3 c08z.py > z.json 2>> c08.log && echo "z done" >> c08.log
for s in 0013 0014 0015 0016 0017 0018; do [ -f v_$s.npz ] || python3 c08v.py $s >> c08.log 2>&1; done
echo "C08 DONE" >> c08.log
