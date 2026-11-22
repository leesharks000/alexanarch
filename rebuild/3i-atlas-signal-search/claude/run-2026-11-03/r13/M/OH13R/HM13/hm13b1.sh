#!/bin/bash
# PLAN-HM13 B1: rerun M4's frozen per-channel steps for the ten lost channels. usage: hm13b1.sh "CC CC ..."
M="$(cd "$(dirname "$0")/../.." && pwd)"; H="$(cd "$(dirname "$0")" && pwd)"; cd "$M"; export SSL_CERT_FILE=/root/.ccr/ca-bundle.crt
mkdir -p "$H/volt" volt; L="$H/hm13b1.log"
for cc in $1; do
  c=$(printf "%02d" $cc)
  for s in 0013 0014 0015 0016 0017 0018; do
    f=out2/cc${c}_$s.npz; g=out3/cc${c}_$s.npz
    [ -f $f ] && [ -f $g ] && python3 -c "import numpy as np;np.load('$f').files;np.load('$g').files" 2>/dev/null && continue
    for i in 1 2 3; do python3 mvb.py $cc $s >> "$L" 2>&1 && break; echo "retry $cc $s $i" >> "$L"; sleep 30; done
  done
  ok=1
  for x in out2/cc${c}_*.npz out3/cc${c}_*.npz; do
    want=$(grep "  $x\$" M4b-PRODUCTS.sha256 | tail -1 | cut -d' ' -f1); got=$(sha256sum $x | cut -d' ' -f1)
    [ "$want" = "$got" ] || { ok=0; echo "G1 FAIL cc$c $x want $want got $got" >> "$L"; }
  done
  echo "G1 cc$c $([ $ok -eq 1 ] && echo PASS || echo FAIL)" >> "$L"
  sha256sum out2/cc${c}_*.npz out3/cc${c}_*.npz >> "$H/HM13-STACKS.sha256"
  mkdir -p "$H/v0"; python3 -c "import numpy as np,json;json.dump({s:float(np.load('out2/cc${c}_'+s+'.npz')['f0_v0']) for s in ['0013','0014','0015','0016','0017','0018']},open('$H/v0/cc$c.json','w'))"
  for i in 1 2; do python3 mvolt.py $cc >> "$L" 2>&1 && break; echo "retry volt $cc $i" >> "$L"; done
  [ -f volt/cc$c.json ] && cp volt/cc$c.json "$H/volt/" && (cd "$H" && sha256sum volt/cc$c.json >> VOLT-HM13.sha256)
  rm -f out2/cc${c}_*.npz out3/cc${c}_*.npz
  echo "HM13 cc$c done $(python3 -c "import json;print(len(json.load(open('volt/cc$c.json'))['nominations']))" 2>/dev/null) nominations" >> "$L"
done
echo "HM13 B1 worker DONE: $1" >> "$L"
