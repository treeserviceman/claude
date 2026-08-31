#!/usr/bin/env bash
# Deploys every site under sites/<slug>/ to its own Netlify site (name = slug).
# Run this on YOUR machine (not in the Claude sandbox) with normal internet access.
#
# Prereqs:
#   npm install -g netlify-cli
#   netlify login
#
# Usage:
#   ./deploy-all.sh                      # uses your default Netlify team
#   NETLIFY_ACCOUNT=my-team ./deploy-all.sh   # deploy under a specific team slug
#
# Output: data/live-urls.csv (keyword,slug,url) — the final list of live root URLs.
# Safe to re-run: sites already created (by name) are detected and reused, not duplicated.

set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

if ! command -v netlify >/dev/null 2>&1; then
  echo "netlify-cli not found. Install it first: npm install -g netlify-cli"
  exit 1
fi

if ! netlify status >/dev/null 2>&1; then
  echo "Not logged in to Netlify. Run: netlify login"
  exit 1
fi

ACCOUNT_FLAG=()
if [ -n "${NETLIFY_ACCOUNT:-}" ]; then
  ACCOUNT_FLAG=(--account-slug "$NETLIFY_ACCOUNT")
fi

OUT="data/live-urls.csv"
echo "keyword,slug,url" > "$OUT"

echo "Fetching your existing Netlify sites (to avoid duplicates on re-run)..."
EXISTING_JSON="$(netlify sites:list --json 2>/dev/null || echo '[]')"

lookup_keyword() {
  awk -F',' -v s="$1" '$1==s{ $1=""; sub(/^,/,""); print; exit }' data/slug-keyword.csv
}

find_existing_id() {
  local name="$1"
  echo "$EXISTING_JSON" | node -e "
    let d='';process.stdin.on('data',c=>d+=c);
    process.stdin.on('end',()=>{
      try {
        const arr = JSON.parse(d);
        const m = arr.find(s => s.name === process.argv[1]);
        console.log(m ? (m.site_id || m.id || '') : '');
      } catch (e) { console.log(''); }
    });
  " "$name" 2>/dev/null
}

total=$(find sites -mindepth 1 -maxdepth 1 -type d | wc -l | tr -d ' ')
i=0
fail_count=0

for dir in sites/*/; do
  i=$((i+1))
  slug="$(basename "$dir")"
  keyword="$(lookup_keyword "$slug")"
  printf '[%d/%s] %s ... ' "$i" "$total" "$slug"

  site_id="$(find_existing_id "$slug")"
  final_name="$slug"

  if [ -z "$site_id" ]; then
    create_out="$(netlify sites:create --name "$slug" "${ACCOUNT_FLAG[@]}" --json 2>&1)"
    site_id="$(echo "$create_out" | node -e "let d='';process.stdin.on('data',c=>d+=c);process.stdin.on('end',()=>{try{const o=JSON.parse(d);console.log(o.id||o.site_id||'')}catch(e){console.log('')}})" 2>/dev/null)"

    if [ -z "$site_id" ]; then
      # Name likely taken globally on Netlify — retry with a numeric suffix.
      for suffix in 2 3 4 5; do
        try_name="${slug}-${suffix}"
        create_out="$(netlify sites:create --name "$try_name" "${ACCOUNT_FLAG[@]}" --json 2>&1)"
        site_id="$(echo "$create_out" | node -e "let d='';process.stdin.on('data',c=>d+=c);process.stdin.on('end',()=>{try{const o=JSON.parse(d);console.log(o.id||o.site_id||'')}catch(e){console.log('')}})" 2>/dev/null)"
        if [ -n "$site_id" ]; then final_name="$try_name"; break; fi
      done
    fi
  fi

  if [ -z "$site_id" ]; then
    echo "FAILED (could not create/find site)"
    fail_count=$((fail_count+1))
    continue
  fi

  deploy_out="$(netlify deploy --prod --dir "$dir" --site "$site_id" --json 2>&1)"
  url="$(echo "$deploy_out" | node -e "let d='';process.stdin.on('data',c=>d+=c);process.stdin.on('end',()=>{try{const o=JSON.parse(d);console.log(o.deploy_url||o.url||'')}catch(e){console.log('')}})" 2>/dev/null)"
  if [ -z "$url" ]; then
    url="https://${final_name}.netlify.app"
  fi

  echo "$url"
  printf '"%s",%s,%s\n' "$keyword" "$slug" "$url" >> "$OUT"
done

echo ""
echo "Done: $((i-fail_count))/$total deployed. $fail_count failed (see output above)."
echo "Live URLs written to $OUT"
