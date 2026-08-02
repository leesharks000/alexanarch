// api/register-symbolon.js — the symbolon witness layer.
//
// Per AXN-SYMBOLON-SPEC v0.2 §7 (deposit #1432): recording a symbolon is a
// provenance registration — the witnessed tuple ⟨AXN₀, AXN₁, timestamp,
// Seed A⟩. Lighter than deposit: only Seed A crosses; Seed B never does.
// The registry is a witness layer, not a storage layer.
//
// POST a Seed A sidecar (as produced by /mint/stamp/). The function:
//   1. validates structure and size;
//   2. RECOMPUTES the six-glyph checksum from axn0.sha256 and axn1.sha256
//      against the canonical table (derivation identical to axn_lib.py) —
//      a sidecar whose glyphs don't match its hashes is rejected;
//   3. commits the entry to data/symbolon-registry/entries/<sha16>.json via
//      the GitHub contents API (token from env SYMBOLON_TOKEN, never client);
//   4. returns the witnessed record URL.
//
// Entries are status "witnessed-unverified": the payload (Seed B) was never
// seen, so the registry witnesses the CLAIM and its internal consistency,
// not the artifact. Verification against bytes is a separate act (§9).
// If SYMBOLON_TOKEN is unset the endpoint answers 503 with a mail fallback.

const AXN_GLYPHS = ["🌑","🌒","🌓","🌔","🌕","🌖","🌗","🌘","⭐","🌟","💫","☀️","🌙","🪐","🌍","🌊","🔥","💧","🌪️","⚡","❄️","🌋","🏔️","🌿","🍃","🌱","🌾","🪨","💎","🧊","🌈","☁️","🏛️","🏗️","🧱","🪜","🚪","🪟","🏠","🏰","⛩️","🕌","🗼","🌉","⚓","🛡️","🔔","🏺","🔧","🔩","⚙️","🔗","🪝","🧲","⚖️","🔬","🔭","🧪","🧫","🧬","💡","🔮","🪄","🗝️","📜","📖","📝","✏️","🖊️","📋","📌","📎","🔖","📚","🗂️","📦","🏷️","🪧","📐","📏","🧭","🗺️","🏴","🚩","⛳","🎯","🔍","👁️","🔎","🪞","🗡️","🛤️","⛵","🚀","🛸","🌀","⌛","⏰","🕐","🕑","🕒","🕓","🕔","🕕","🕖","🕗","🕘","🕙","🕚","🕛","⌛","🔄","🌸","🌺","🌻","🌹","🍀","🌲","🌳","🍁","🍂","🍄","🐚","🪸","🦋","🐝","🕊️","🦅","♠️","❤️","♦️","♣️","🎭","🎪","🎨","🎵","🎶","🎹","🎻","🎺","🥁","🎲","🃏","🀄","➕","➖","✖️","➗","♾️","∮","⊕","⊗","△","▽","◇","○","●","□","■","▲","🜁","🝊","☿","♃","♄","♅","♆","☉","☽","♈","♉","♊","♋","♌","♍","♎","👁‍🗨","🤲","👐","🙏","✊","🤝","👆","👇","👈","👉","🫵","🖐️","✋","🫶","🤙","👋","🚨","🔴","🟠","🟡","🟢","🔵","🟣","⚪","⚫","🟤","💜","💙","💚","💛","🧡","❤️","🔺","🔻","◀️","▶️","🔼","🔽","⏩","⏪","⏫","⏬","↗️","↘️","↙️","↖️","🔃","🔀","🌅","🌄","🌃","🌆","🌇","🏙️","🌌","🎆","🎇","✨","🌠","💥","🔆","🔅","⭕","❌","🏁","🎬","🔚","🔙","🔛","🔝","🔜","⏹️","⏏️","🔒","🔓","🔐","🗿","🪦","♻️","∞"];

function glyphsFromHash(h) {
  const out = [];
  for (let i = 0; i < 12; i += 2) out.push(AXN_GLYPHS[parseInt(h.slice(i, i + 2), 16)]);
  return out.join("");
}
const HEX64 = /^[0-9a-f]{64}$/;

module.exports = async (req, res) => {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  if (req.method === "OPTIONS") return res.status(204).end();
  if (req.method !== "POST")
    return res.status(405).json({ error: "POST a Seed A sidecar (application/json)." });

  const token = process.env.SYMBOLON_TOKEN;
  if (!token)
    return res.status(503).json({
      error: "witnessing offline",
      fallback: "email the .axn.json sidecar to leesharks00@gmail.com and it will be witnessed manually",
    });

  let seed = req.body;
  if (typeof seed === "string") { try { seed = JSON.parse(seed); } catch { seed = null; } }
  if (!seed || typeof seed !== "object")
    return res.status(400).json({ error: "body must be the Seed A JSON object" });
  if (JSON.stringify(seed).length > 60000)
    return res.status(413).json({ error: "sidecar too large (60KB cap)" });

  const h0 = seed?.axn0?.sha256, g0 = seed?.axn0?.glyphs;
  const h1 = seed?.axn1?.sha256, g1 = seed?.axn1?.glyphs;
  if (!HEX64.test(h0 || "") || !HEX64.test(h1 || ""))
    return res.status(400).json({ error: "axn0.sha256 and axn1.sha256 must be 64-char lowercase hex" });
  if (glyphsFromHash(h0) !== g0)
    return res.status(422).json({ error: "axn0 glyphs do not derive from axn0.sha256 — sidecar internally inconsistent" });
  if (glyphsFromHash(h1) !== g1)
    return res.status(422).json({ error: "axn1 glyphs do not derive from axn1.sha256 — sidecar internally inconsistent" });

  const FAMILIES=["GOVERNANCE","UNCLASSIFIED","EMPIRICAL","ARCHIVAL","GENERATIVE","STRUCTURAL","OPERATIVE","PHILOLOGICAL"];
  const family = FAMILIES.includes(seed.family) ? seed.family : "UNCLASSIFIED";
  const key = h0.slice(0, 16);
  const path = `data/symbolon-registry/entries/${key}.json`;
  const api = `https://api.github.com/repos/leesharks000/alexanarch/contents/${path}`;
  const gh = { Authorization: `Bearer ${token}`, Accept: "application/vnd.github+json", "User-Agent": "alexanarch-symbolon-witness" };

  // dedupe: already witnessed?
  const existing = await fetch(api, { headers: gh });
  if (existing.status === 200)
    return res.status(200).json({
      status: "already-witnessed",
      axn0: g0,
      record: `https://www.alexanarch.org/${path}`,
    });

  // --- allocate a registry position from the shared ledger (compare-and-swap) ---
  const ledgerApi = "https://api.github.com/repos/leesharks000/alexanarch/contents/data/symbolon-registry/allocation.json";
  let hexPos = null;
  for (let attempt = 0; attempt < 4 && !hexPos; attempt++) {
    const lr = await fetch(ledgerApi, { headers: gh });
    if (!lr.ok) break;
    const lj = await lr.json();
    const ledger = JSON.parse(Buffer.from(lj.content, "base64").toString("utf8"));
    const candidate = ledger.next_hex;
    const bumped = { ...ledger, next_hex: (parseInt(candidate, 16) + 1).toString(16).toUpperCase().padStart(4, "0"), last_allocated: candidate, last_allocated_at: new Date().toISOString() };
    const cas = await fetch(ledgerApi, {
      method: "PUT",
      headers: { ...gh, "Content-Type": "application/json" },
      body: JSON.stringify({
        message: `AXN ALLOCATE ${candidate} (symbolon witness)`,
        content: Buffer.from(JSON.stringify(bumped, null, 1)).toString("base64"),
        sha: lj.sha,
      }),
    });
    if (cas.ok) hexPos = candidate;           // CAS won
    else if (cas.status === 409) continue;    // lost race; re-read and retry
    else break;
  }
  if (!hexPos)
    return res.status(502).json({ error: "position allocation failed; kernel remains valid without a position — retry shortly or email the sidecar" });
  const fullAxn = `AXN:${hexPos}.${family}.${g0}`;

  const entry = {
    axn: fullAxn,
    position: hexPos,
    family,
    registered: new Date().toISOString(),
    status: "witnessed-unverified",
    note: "The registry witnesses the tuple and its internal consistency (glyphs recomputed from hashes at ingest). Seed B was not seen; verification against bytes is a separate act per SPEC §9.",
    spec: "AXN-SYMBOLON-SPEC v0.2 · https://www.alexanarch.org/s/records/1432/",
    tuple: { axn0: { glyphs: g0, sha256: h0 }, axn1: { glyphs: g1, sha256: h1 } },
    position_note: "The hex position is a registry address allocated from the shared AXN sequence (data/symbolon-registry/allocation.json). An address is not a verification.",
    seed_a: seed,
  };
  const put = await fetch(api, {
    method: "PUT",
    headers: { ...gh, "Content-Type": "application/json" },
    body: JSON.stringify({
      message: `SYMBOLON WITNESS ${fullAxn} · ${key} (witnessed-unverified via /api/register-symbolon)`,
      content: Buffer.from(JSON.stringify(entry, null, 1)).toString("base64"),
    }),
  });
  // position-keyed pointer for registry-style lookup
  await fetch(`https://api.github.com/repos/leesharks000/alexanarch/contents/data/symbolon-registry/positions/${hexPos}.json`, {
    method: "PUT",
    headers: { ...gh, "Content-Type": "application/json" },
    body: JSON.stringify({
      message: `SYMBOLON POSITION ${hexPos} → ${key}`,
      content: Buffer.from(JSON.stringify({ axn: fullAxn, entry: `entries/${key}.json` }, null, 1)).toString("base64"),
    }),
  }).catch(() => {});
  if (!put.ok) {
    const t = await put.text();
    return res.status(502).json({ error: "witness commit failed", detail: t.slice(0, 200) });
  }
  return res.status(201).json({
    status: "witnessed",
    axn: fullAxn,
    axn0: g0,
    axn1: g1,
    record: `https://www.alexanarch.org/${path}`,
    note: "Witnessed as a provenance registration (witnessed-unverified). The record publishes with the next deploy, typically within two minutes.",
  });
};
