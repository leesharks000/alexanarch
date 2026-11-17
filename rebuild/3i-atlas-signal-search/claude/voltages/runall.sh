#!/bin/bash
cd "$(dirname "$0")"
for s in 0013 0014 0015 0016 0017 0018; do python3 voltreduce.py $s 7 > out/log_${s}_7.txt 2>&1; done
for s in 0013 0014 0015 0016 0017 0018; do python3 voltreduce.py $s 8 > out/log_${s}_8.txt 2>&1; done
echo ALLDONE > out/ALLDONE
