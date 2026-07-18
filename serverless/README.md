# Staged serverless functions

`mint.js` implements /api/mint per data/specs/AXN-MINT-ENDPOINT-SPEC-v0.1.md §2.
It is STAGED, not deployed, because the repo's /api directory is a live static
surface (network.json feeds the 25-site fleet; registry chunks, protocol
catalogs). Moving a .js file into /api flips the Vercel project into hybrid
mode; that transition must be deliberate.

Activation checklist (MANUS):
1. Vercel dashboard → project env → add MINT_GITHUB_TOKEN
   (fine-grained PAT: contents:write + issues:write on leesharks000/alexanarch,
   short expiry, rotate on schedule)
2. `git mv serverless/mint.js api/mint.js && git mv serverless/axn_glyphs.json api/axn_glyphs.json`
3. Push; after deploy, VERIFY static api/*.json still serves
   (curl https://www.alexanarch.org/api/network.json — content-match, not just 200)
4. Smoke-test: POST to /api/mint with a canonical_text; confirm 201 + issue opened
5. If static api/ breaks: revert the move, escalate to vercel.json `functions`
   config with an alternate path (e.g. /fn/mint)

axn_glyphs.json is GENERATED from scripts/axn_lib.py (canonical source).
Never hand-edit. Regeneration command in mint.js header.
