#!/bin/bash
# PLAN-M4 orchestration. usage: m4.sh PARITY(0|1)
cd "$(dirname "$0")"; export SSL_CERT_FILE=/root/.ccr/ca-bundle.crt
P=$1; mkdir -p M4 volt
for cc in $(seq 0 63); do
  [ $((cc % 2)) -ne $P ] && continue
  case $cc in 0|26|40|63) continue;; esac
  c=$(printf "%02d" $cc); [ -f volt/cc$c.json ] && continue
  for s in 0013 0014 0015 0016 0017 0018; do
    f=out2/cc${c}_$s.npz; [ -f $f ] && python3 -c "import numpy as np;np.load('$f').files" 2>/dev/null && continue
    for i in 1 2; do python3 mv.py $cc $s >> m4.log 2>&1 && break; echo "retry $cc $s $i" >> m4.log; done
  done
  for i in 1 2 3; do
    python3 mhits.py > M4/tmp$P.json 2>> m4.err && python3 -c "
import json,sys;R=json.load(open('M4/tmp$P.json'));e=R['channels'].get('cc$c')
assert e, 'missing'; json.dump({'plan':R['plan'],'cc$c':e},open('M4/cc$c.json','w'),indent=1)" && break; sleep 20
  done
  python3 mvolt.py $cc >> m4.log 2>&1 || { echo "fail volt $cc" >> m4.log; continue; }
  sha256sum out2/cc${c}_*.npz >> M4-PRODUCTS.sha256 && rm -f out2/cc${c}_*.npz
  echo "M4 cc$c done $(python3 -c "import json;print(len(json.load(open('volt/cc$c.json'))['nominations']))") nominations" >> m4.log
done
echo "M4 worker $P DONE" >> m4.log
