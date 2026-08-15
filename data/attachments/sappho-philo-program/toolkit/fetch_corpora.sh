#!/usr/bin/env bash
# Reproducible corpus acquisition for the Sappho–Philo program.
# Two independent Philo corpora + the Longinus TEI. Independence matters:
# the name-census null was confirmed on non-identical corpora.
set -euo pipefail
OUT="${1:-/tmp/corpora}"; mkdir -p "$OUT"/{philo_wikisource,philo_first1k,longinus}

# --- Corpus A: 12 treatises, Greek Wikisource (Cohn–Wendland text) ---
declare -A W=(
 ["Περί_της_κατά_Μωυσέα_κοσμοποιίας"]=opif
 ["Περί_του_τις_ο_των_θείων_έστιν_κληρονόμος"]=her
 ["Περί_μέθης"]=ebr  ["Περί_βίου_θεωρητικού_ή_ικέτων"]=contempl
 ["Περί_των_μετονομαζομένων_και_ων_ένεκα_μετονομάζονται"]=mut
 ["Περί_γενέσεως_Άβελ"]=sacr
 ["Περί_του_το_χείρον_τω_κρείττονι_φίλειν_επιτίθεσθαι"]=det
 ["Περί_φυγής_και_ευρέσεως"]=fug ["Περί_Γιγάντων"]=gig
 ["Ότι_άτρεπτον_το_θείον"]=deus ["Περί_συγχύσεως_διαλέκτων"]=conf
 ["Περί_του_θεοπέμπτους_είναι_τους_ονείρους/λόγος_πρώτος"]=somn1
)
for slug in "${!W[@]}"; do
  curl -s --max-time 40 -L "https://el.wikisource.org/wiki/${slug}" \
    -o "$OUT/philo_wikisource/${W[$slug]}.html" || echo "WARN: ${W[$slug]}"
done

# --- Corpus B: all 31 works, OpenGreekAndLatin/First1KGreek (tlg0018) ---
# Needs a GitHub token in $GH_TOKEN (unauthenticated hits the rate limit).
: "${GH_TOKEN:?set GH_TOKEN}"
for i in $(seq -w 1 31); do
  w="tlg0$i"
  f=$(curl -s --max-time 20 -H "Authorization: token $GH_TOKEN" \
      "https://api.github.com/repos/OpenGreekAndLatin/First1KGreek/contents/data/tlg0018/$w" \
    | python3 -c "import json,sys;d=json.load(sys.stdin);x=[e['name'] for e in d if e['name'].endswith('.xml') and 'grc' in e['name']];print(x[0] if x else '')")
  [ -n "$f" ] && curl -s --max-time 40 \
    -o "$OUT/philo_first1k/$w.xml" \
    "https://raw.githubusercontent.com/OpenGreekAndLatin/First1KGreek/master/data/tlg0018/$w/$f"
done

# --- Longinus, Peri Hypsous (TEI) ---
echo "Longinus TEI: supply locally as $OUT/longinus/lon.xml (Perseus tlg2001.tlg001)"
echo "done -> $OUT"
