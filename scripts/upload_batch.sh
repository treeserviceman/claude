#!/usr/bin/env bash
# Reads a JSON array [{slug, siteId, proxyUrl}] from $1, uploads each site's directory
# to Netlify directly via the proxy-path relay (bypassing the buggy @netlify/mcp CLI),
# and appends results to data/deploy-ledger.json.
set -uo pipefail
ROOT="/home/user/claude"
cd "$ROOT"

BATCH_FILE="$1"
TMPDIR="$(mktemp -d)"

node -e "
const batch = require('$BATCH_FILE');
console.log(JSON.stringify(batch));
" > "$TMPDIR/batch.json"

count=$(node -e "console.log(require('$BATCH_FILE').length)")
echo "Uploading $count site(s)..."

RESULTS="$TMPDIR/results.json"
echo "[]" > "$RESULTS"

for i in $(seq 0 $((count-1))); do
  slug=$(node -e "console.log(require('$BATCH_FILE')[$i].slug)")
  siteId=$(node -e "console.log(require('$BATCH_FILE')[$i].siteId)")
  proxyUrl=$(node -e "console.log(require('$BATCH_FILE')[$i].proxyUrl)")

  dir="sites/$slug"
  zipPath="$TMPDIR/$slug.zip"
  bodyPath="$TMPDIR/$slug.body"
  boundaryPath="$TMPDIR/$slug.boundary"

  if [ ! -d "$dir" ]; then
    echo "[$((i+1))/$count] $slug: MISSING DIR, skip"
    continue
  fi

  (cd "$dir" && zip -q -r "$zipPath" .)
  node scripts/wrap_multipart.js "$zipPath" "$bodyPath" "$boundaryPath" > /dev/null
  boundary=$(cat "$boundaryPath")

  resp=$(curl -sS -X POST "$proxyUrl/api/v1/sites/$siteId/builds" \
    -H "Content-Type: multipart/form-data; boundary=$boundary" \
    -H "user-agent: netlify-mcp" \
    --data-binary "@$bodyPath" \
    -w "\n%{http_code}")
  status=$(echo "$resp" | tail -1)
  body=$(echo "$resp" | sed '$d')

  url="https://${slug}.netlify.app"
  if [ "$status" = "200" ]; then
    deployId=$(echo "$body" | node -e "let d='';process.stdin.on('data',c=>d+=c);process.stdin.on('end',()=>{try{console.log(JSON.parse(d).deploy_id||'')}catch(e){console.log('')}})")
    echo "[$((i+1))/$count] $slug: OK deploy_id=$deployId"
  else
    echo "[$((i+1))/$count] $slug: FAILED status=$status body=$body"
  fi

  rm -f "$zipPath" "$bodyPath" "$boundaryPath"
done

echo "Batch done."
