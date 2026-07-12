#!/usr/bin/env bash
set -Eeuo pipefail

MANIFEST="${1:-counterinfra/estate-repos.tsv}"
OUT="${2:-estate-recovery}"
WORK="$OUT/.work"
TOKEN="${ESTATE_GH_TOKEN:-}"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"

mkdir -p "$OUT"/{bundles,worktrees,lfs,verification} "$WORK"
printf 'repository\tvisibility\ttier\tstatus\twarnings\n' > "$OUT/recovery-index.tsv"
cp "$MANIFEST" "$OUT/estate-repos.tsv"

cleanup() { rm -rf "$WORK"; }
trap cleanup EXIT

clone_private() {
  local url="$1" dest="$2" auth
  auth="$(printf 'x-access-token:%s' "$TOKEN" | base64 | tr -d '\n')"
  GIT_CONFIG_COUNT=1 \
  GIT_CONFIG_KEY_0=http.https://github.com/.extraheader \
  GIT_CONFIG_VALUE_0="AUTHORIZATION: basic $auth" \
  GIT_TERMINAL_PROMPT=0 \
  git clone --mirror "$url" "$dest"
}

while IFS=$'\t' read -r full visibility branch tier; do
  [[ "$full" == "full_name" || -z "$full" ]] && continue
  name="${full#*/}"
  mirror="$WORK/$name.git"
  url="https://github.com/$full.git"
  warnings=""
  echo "=== $full ==="

  if [[ "$visibility" == "private" && -z "$TOKEN" ]]; then
    printf '%s\t%s\t%s\t%s\t%s\n' "$full" "$visibility" "$tier" "skipped-private-no-token" "ESTATE_GH_TOKEN required" >> "$OUT/recovery-index.tsv"
    continue
  fi

  if [[ "$visibility" == "private" ]]; then
    clone_private "$url" "$mirror"
  else
    git clone --mirror "$url" "$mirror"
  fi

  if ! git --git-dir="$mirror" for-each-ref --format='%(refname)' | grep -q .; then
    printf '%s\t%s\t%s\t%s\t%s\n' "$full" "$visibility" "$tier" "empty-repository" "" >> "$OUT/recovery-index.tsv"
    rm -rf "$mirror"
    continue
  fi

  git --git-dir="$mirror" bundle create "$OUT/bundles/$name.bundle" --all
  git bundle verify "$OUT/bundles/$name.bundle" > "$OUT/verification/$name.bundle-verify.txt" 2>&1

  ref=""
  for candidate in "refs/heads/$branch" refs/heads/main refs/heads/master; do
    if git --git-dir="$mirror" show-ref --verify --quiet "$candidate"; then ref="$candidate"; break; fi
  done
  if [[ -z "$ref" ]]; then
    ref="$(git --git-dir="$mirror" for-each-ref --format='%(refname)' refs/heads | head -n1 || true)"
  fi
  if [[ -n "$ref" ]]; then
    git --git-dir="$mirror" archive --format=tar.gz -o "$OUT/worktrees/$name-${ref##*/}.tar.gz" "$ref"
    if git --git-dir="$mirror" cat-file -e "$ref:.gitmodules" 2>/dev/null; then
      warnings="submodules require independent capture"
    fi
  fi

  if git lfs version >/dev/null 2>&1; then
    if git --git-dir="$mirror" lfs fetch --all >/dev/null 2>&1; then
      if [[ -d "$mirror/lfs/objects" ]] && find "$mirror/lfs/objects" -type f -print -quit | grep -q .; then
        tar -C "$mirror" -czf "$OUT/lfs/$name-lfs-objects.tar.gz" lfs/objects
      fi
    else
      warnings="${warnings:+$warnings; }git-lfs fetch failed"
    fi
  else
    warnings="${warnings:+$warnings; }git-lfs unavailable"
  fi

  printf '%s\t%s\t%s\t%s\t%s\n' "$full" "$visibility" "$tier" "ok" "$warnings" >> "$OUT/recovery-index.tsv"
  rm -rf "$mirror"
done < "$MANIFEST"

printf '%s\n' "$STAMP" > "$OUT/CREATED-UTC.txt"
(
  cd "$OUT"
  find . -type f ! -name SHA256SUMS.txt -print0 | sort -z | xargs -0 sha256sum > SHA256SUMS.txt
  sha256sum -c SHA256SUMS.txt
)

if [[ "${UPLOAD_IA:-0}" == "1" ]]; then
  : "${IA_ACCESS:?IA_ACCESS required when UPLOAD_IA=1}"
  : "${IA_SECRET:?IA_SECRET required when UPLOAD_IA=1}"
  IA_IDENTIFIER="${IA_IDENTIFIER:-alexanarch-estate-recovery}"
  first=1
  while IFS= read -r -d '' file; do
    rel="${file#$OUT/}"
    headers=(-H "Authorization: LOW $IA_ACCESS:$IA_SECRET")
    if [[ "$first" == "1" ]]; then
      headers+=(-H 'x-archive-auto-make-bucket: 1' -H 'x-archive-meta-title: Alexanarch Estate Recovery Set' -H 'x-archive-meta-creator: Lee Sharks' -H 'x-archive-meta-mediatype: data' -H 'x-archive-meta-subject: Alexanarch; archival continuity; disaster recovery; Git bundles')
      first=0
    fi
    curl --fail --show-error --silent --retry 4 --retry-all-errors "${headers[@]}" --upload-file "$file" "https://s3.us.archive.org/$IA_IDENTIFIER/$STAMP/$rel"
  done < <(find "$OUT" -type f -print0 | sort -z)
fi

echo "Recovery set created at $OUT"
