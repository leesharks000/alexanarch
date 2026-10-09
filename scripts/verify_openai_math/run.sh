#!/usr/bin/env bash
# Independent check of one headline result in openai/math, pinned to OAI_COMMIT.
# Called by .github/workflows/verify-openai-math.yml as: run.sh <stage> <target>
#   stages: fetch | deps | build | check | comparator | summary
# The kernel check (stage "check") proves a statement restated in scripts/verify_openai_math/<target>.lean,
# in standard Mathlib terms (Hadwiger: with a clique-minor definition written there), from OpenAI's theorem,
# and prints the axioms the proof uses. "comparator" runs OpenAI's own Comparator challenge where the tools build.
# Closure sizes measured 2026-10-09: Kaplansky 121 OAI files / 13k lines; Hadwiger 288 / 40k; zeta 2,924 / 486k.
set -euo pipefail
STAGE=$1; T=$2
HERE=$(cd "$(dirname "$0")" && pwd)
W=${GITHUB_WORKSPACE:-$PWD}
OAI_COMMIT=${OAI_COMMIT:-fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb}
case "$T" in
  kaplansky) MOD=OAI.RingTheory.DirectFiniteness.Main; CH=ComparatorChallenges/KaplanskyDirectFiniteness.json ;;
  hadwiger)  MOD=OAI.Combinatorics.HadwigerCounterexample.Main; CH=ComparatorChallenges/HadwigerCounterexample.json ;;
  zeta)      MOD=OAI.NumberTheory.DirichletL.Nonvanishing; CH=ComparatorChallenges/QuasiRiemannHypothesis.json ;;
  *) echo "unknown target $T"; exit 1 ;;
esac
L=$W/oai/lean
case "$STAGE" in
  fetch)
    sudo rm -rf /usr/share/dotnet /usr/local/lib/android /opt/ghc /opt/hostedtoolcache/CodeQL || true
    sudo sysctl -w vm.max_map_count=1048576 || true
    git init -q "$W/oai" && cd "$W/oai"
    git remote add origin https://github.com/openai/math.git
    git config core.sparseCheckout true
    echo "lean/" > .git/info/sparse-checkout
    git fetch -q --depth 1 --filter=blob:none origin "$OAI_COMMIT"
    git checkout -q FETCH_HEAD
    git rev-parse HEAD | tee "$W/commit.txt"
    curl -sSfL https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -o "$W/elan-init.sh"
    sh "$W/elan-init.sh" -y --default-toolchain none
    df -h / ;;
  deps)
    cd "$L"
    cp lake-manifest.json "$W/manifest.before.json"
    lake update 2>&1 | tail -40
    rev() { python3 -c "import json,sys;[print(p['name'],p.get('rev')) for p in json.load(open(sys.argv[1]))['packages']]" "$1"; }
    diff <(rev "$W/manifest.before.json") <(rev lake-manifest.json) > "$W/manifest.diff" || true
    echo "manifest changes after lake update:"; cat "$W/manifest.diff"
    python3 -c "import json;m=[p for p in json.load(open('lake-manifest.json'))['packages'] if p['name']=='mathlib'][0];print('mathlib',m['url'],m['rev'])" | tee "$W/mathlib.txt"
    lake exe cache get ;;
  build)
    cd "$L"
    lake build "$MOD" 2>&1 | tee "$W/build.log" | grep -E "error|✖|Build completed" | tail -60 ;;
  check)
    cd "$L"
    cp "$HERE/$T.lean" AlexanarchCheck.lean
    cat AlexanarchCheck.lean
    lake env lean AlexanarchCheck.lean 2>&1 | tee "$W/check.log" ;;
  comparator)
    cd "$L"
    TC=$(cat lean-toolchain)
    git clone -q --depth 1 https://github.com/leanprover/lean4export "$W/lean4export"
    git clone -q --depth 1 https://github.com/leanprover/comparator "$W/comparator"
    (cd "$W/lean4export" && echo "$TC" > lean-toolchain && lake build 2>&1 | tail -5)
    (cd "$W/comparator" && echo "$TC" > lean-toolchain && lake build 2>&1 | tail -5)
    go install github.com/zouuup/landrun/cmd/landrun@latest
    export PATH="$PATH:$HOME/go/bin:$W/lean4export/.lake/build/bin:$W/comparator/.lake/build/bin"
    lake env comparator "$CH" 2>&1 | tee "$W/comparator.log" ;;
  summary)
    {
      echo "## $T"
      echo "- openai/math commit: $(cat "$W/commit.txt" 2>/dev/null)"
      echo "- $(cat "$W/mathlib.txt" 2>/dev/null)"
      echo "- build: ${BUILD_OUTCOME:-?} · kernel check: ${CHECK_OUTCOME:-?} · comparator: ${COMPARATOR_OUTCOME:-?}"
      echo '```'; tail -20 "$W/check.log" 2>/dev/null; echo '```'
      echo "comparator:"; echo '```'; tail -20 "$W/comparator.log" 2>/dev/null; echo '```'
      echo "manifest changes from lake update:"; echo '```'; cat "$W/manifest.diff" 2>/dev/null; echo '```'
    } >> "${GITHUB_STEP_SUMMARY:-/dev/stdout}" ;;
esac
