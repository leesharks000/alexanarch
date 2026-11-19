#!/bin/bash
# PLAN-M4b orchestration: M4's per-channel steps with mvb.py in place of mv.py, plus the drift events. usage: m4b.sh PARITY(0|1)
cd "$(dirname "$0")"; export SSL_CERT_FILE=/root/.ccr/ca-bundle.crt
P=$1; mkdir -p M4 M4b/events volt
for cc in $(seq 0 63); do
  [ $((cc % 2)) -ne $P ] && continue
  c=$(printf "%02d" $cc); [ -f M4b/events/cc$c.json ] && continue
  for s in 0013 0014 0015 0016 0017 0018; do
    f=out2/cc${c}_$s.npz; g=out3/cc${c}_$s.npz
    [ -f $f ] && [ -f $g ] && python3 -c "import numpy as np;np.load('$f').files;np.load('$g').files" 2>/dev/null && continue
    for i in 1 2; do python3 mvb.py $cc $s >> m4b.log 2>&1 && break; echo "retry $cc $s $i" >> m4b.log; done
  done
  case $cc in 0|26|40|63) M4X=1;; *) M4X=0;; esac   # M2/M3 channels: not M4's
  if [ $M4X -eq 0 ] && [ ! -f volt/cc$c.json ]; then   # an M4 channel not yet done: M4's stages 2-3 as frozen
    for i in 1 2 3; do
      python3 mhits.py > M4/tmp$P.json 2>> m4b.err && python3 -c "
import json;R=json.load(open('M4/tmp$P.json'));e=R['channels'].get('cc$c')
assert e, 'missing'; json.dump({'plan':R['plan'],'cc$c':e},open('M4/cc$c.json','w'),indent=1)" && break; sleep 20
    done
    python3 mvolt.py $cc >> m4b.log 2>&1 || { echo "fail volt $cc" >> m4b.log; continue; }
  fi
  python3 mdhits.py $cc > M4b/events/tmp$P.json 2>> m4b.err && mv M4b/events/tmp$P.json M4b/events/cc$c.json || { echo "fail events $cc" >> m4b.log; continue; }
  sha256sum out2/cc${c}_*.npz out3/cc${c}_*.npz >> M4b-PRODUCTS.sha256 && rm -f out2/cc${c}_*.npz out3/cc${c}_*.npz
  echo "M4b cc$c done $(python3 -c "import json;e=json.load(open('M4b/events/cc$c.json'));print('A',e['n']['A'],'B',e['n']['B'],'| control A',e['control_n']['A'],'B',e['control_n']['B'])")" >> m4b.log
done
echo "M4b worker $P DONE" >> m4b.log
