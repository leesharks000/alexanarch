// /api/mint — AXN registration endpoint (spec v0.1 §2)
// STAGED: see serverless/README.md for activation. Not yet deployed —
// the repo's /api directory is a live static surface; moving this file
// there flips the Vercel project into hybrid mode and must be done
// deliberately, with the static api/*.json serving verified afterward.
//
// Mechanics (No-Double-Draw conforming — zero LLM calls):
//   validate -> hash -> derive glyph -> assign next position ->
//   open a `pending` deposit via GitHub API -> return the AXN.
// Identity is assigned at POST time; review gates listing, never identity.

const crypto = require('crypto');

// Canonical 256-glyph table — MUST be generated from scripts/axn_lib.py,
// never hand-edited. Regenerate with:
//   python3 -c "import sys; sys.path.insert(0,'scripts'); from axn_lib import AXN_GLYPHS; import json; print(json.dumps(AXN_GLYPHS, ensure_ascii=False))"
const AXN_GLYPHS = require('./axn_glyphs.json');

const FAMILIES = ["GOVERNANCE","EMPIRICAL","GENERATIVE","ARCHIVAL","PHILOLOGICAL",
  "STRUCTURAL","COMPOSITIONAL","OPERATIVE","HETERONYMIC","MPAI","UNCLASSIFIED"];

function glyphFromHash(hex) {
  const out = [];
  for (let i = 0; i < 12; i += 2) out.push(AXN_GLYPHS[parseInt(hex.slice(i, i + 2), 16)]);
  return out.join('');
}

module.exports = async (req, res) => {
  if (req.method !== 'POST') return res.status(405).json({ error: 'POST only' });
  const token = process.env.MINT_GITHUB_TOKEN;
  if (!token) return res.status(501).json({
    error: 'mint endpoint staged but not activated',
    activation: 'set MINT_GITHUB_TOKEN in Vercel env (fine-grained, contents:write + issues:write on leesharks000/alexanarch), move serverless/mint.js to api/mint.js, verify static api/*.json still serves'
  });

  const { canonical_text, content_sha256, family, declared_title, declared_creator } = req.body || {};
  if (!FAMILIES.includes(family)) return res.status(400).json({ error: 'invalid family', families: FAMILIES });

  let hash, status;
  if (canonical_text) {
    if (canonical_text.includes('AXN:')) return res.status(400).json({
      error: 'circularity: canonical bytes must not contain an AXN (spec v0.1 §2.3.3)' });
    hash = crypto.createHash('sha256').update(Buffer.from(canonical_text, 'utf8')).digest('hex');
    status = 'pending';           // bytes held; mechanical validation promotes
  } else if (/^[0-9a-f]{64}$/.test(content_sha256 || '')) {
    hash = content_sha256;
    status = 'kernel-registered'; // identity claimed, bytes pending custody
  } else {
    return res.status(400).json({ error: 'supply canonical_text or content_sha256 (64 hex)' });
  }

  const glyph = glyphFromHash(hash);

  // Assign next position from registry head (append-only; manual hex retired)
  const regResp = await fetch(
    'https://raw.githubusercontent.com/leesharks000/alexanarch/main/data/registry.json');
  const reg = await regResp.json();
  const next = Math.max(...reg.deposits.map(d => d.deposit_number)) + 1;
  const hex = next.toString(16).toUpperCase().padStart(4, '0');
  const axn = `AXN:${hex}.${family}.${glyph}`;

  // Open a pending deposit issue (the transport, mechanized)
  const issue = await fetch('https://api.github.com/repos/leesharks000/alexanarch/issues', {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      title: `[api-mint pending] #${next} ${declared_title || '(untitled)'}`,
      labels: ['deposit', 'api-mint', status],
      body: [
        `axn: ${axn}`, `hash: ${hash}`, `family: ${family}`, `status: ${status}`,
        `declared_title: ${declared_title || ''}`, `declared_creator: ${declared_creator || ''}`,
        `transport: api`, '', '---', '',
        canonical_text ? canonical_text.slice(0, 60000) : '(kernel-only registration; bytes pending)'
      ].join('\n')
    })
  });
  const issueData = await issue.json();

  return res.status(201).json({
    axn, hex, glyph, content_sha256: hash, deposit_number: next, status,
    transport_record: issueData.html_url,
    note: 'Position assigned at POST time; the pipeline validation pass promotes pending entries to listed. The AXN above is the AXN.'
  });
};
