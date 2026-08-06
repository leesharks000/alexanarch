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
  const store = seed.store; delete seed.store;
  if (JSON.stringify(seed).length > 60000)
    return res.status(413).json({ error: "sidecar too large (60KB cap)" });
  if (store && (typeof store.content_b64 !== "string" || store.content_b64.length > 4200000))
    return res.status(413).json({ error: "stored file too large for this transport (~3 MB cap) — use the deposit transport for larger works" });

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
  if (existing.status === 200) {
    const ej = await existing.json();
    const ent = JSON.parse(Buffer.from(ej.content, "base64").toString("utf8"));
    // ONE KERNEL, ONE POSITION — but a witnessed entry may still receive its sealed core:
    // storing against an existing entry hash-verifies the bytes and upgrades the record.
    if (store && !ent.retrieval) {
      const crypto = require("crypto");
      const bytes = Buffer.from(store.content_b64, "base64");
      const sha = crypto.createHash("sha256").update(bytes).digest("hex");
      if (sha !== h0)
        return res.status(422).json({ error: "stored bytes do not hash to axn0.sha256 — refusing to store a file that is not the sealed core" });
      const safe = String(store.filename || "file").replace(/[^A-Za-z0-9._-]/g, "_").slice(0, 80);
      const fpath = `data/symbolon-registry/files/${key}-${safe}`;
      const fr = await fetch(`https://api.github.com/repos/leesharks000/alexanarch/contents/${fpath}`, {
        method: "PUT", headers: { ...gh, "Content-Type": "application/json" },
        body: JSON.stringify({ message: `SYMBOLON STORE (upgrade) ${ent.position} · ${key} — sealed core attached to existing entry, hash-verified`, content: store.content_b64 }),
      });
      if (fr.ok) {
        ent.retrieval = `https://www.alexanarch.org/${fpath}`;
        ent.status = "witnessed-verified";
        ent.verified_at = new Date().toISOString();
        await fetch(api, {
          method: "PUT", headers: { ...gh, "Content-Type": "application/json" },
          body: JSON.stringify({ message: `SYMBOLON UPGRADE ${ent.axn || ent.position} → witnessed-verified (sealed core stored)`,
            content: Buffer.from(JSON.stringify(ent, null, 1)).toString("base64"), sha: ej.sha }),
        });
        return res.status(200).json({ status: "upgraded to witnessed-verified — sealed core stored against the existing entry",
          axn: ent.axn, retrieval: ent.retrieval, record: `https://www.alexanarch.org/${path}` });
      }
    }
    // Stamp is scaffold: if the sealed core matches but the stamped form (AXN1) changed
    // — e.g. re-stamped with improved geometry — refresh AXN1 and record the re-stamp.
    let axn1_refreshed = false;
    if (ent.tuple && ent.tuple.axn1 && ent.tuple.axn1.sha256 !== h1) {
      ent.stamp_history = ent.stamp_history || [{ axn1: ent.tuple.axn1, until: new Date().toISOString() }];
      ent.stamp_history.push({ axn1_replaced: ent.tuple.axn1.sha256, at: new Date().toISOString() });
      ent.tuple.axn1 = { glyphs: g1, sha256: h1 };
      ent.note = (ent.note || "") + " [Stamp re-applied " + new Date().toISOString().slice(0,10) + "; AXN1 refreshed to the current stamped form. Sealed core (AXN0) unchanged.]";
      await fetch(api, { method: "PUT", headers: { ...gh, "Content-Type": "application/json" },
        body: JSON.stringify({ message: `SYMBOLON RE-STAMP ${ent.axn || ent.position} — AXN1 refreshed (sealed core unchanged)`,
          content: Buffer.from(JSON.stringify(ent, null, 1)).toString("base64"), sha: ej.sha }) });
      axn1_refreshed = true;
    }
    return res.status(200).json({
      status: "already-witnessed" + (ent.retrieval ? " (sealed core already stored)" : "") + (axn1_refreshed ? " — stamp re-applied, AXN1 refreshed" : ""),
      axn: ent.axn, retrieval: ent.retrieval || null,
      record: `https://www.alexanarch.org/${path}`,
    });
  }

  // --- ONE KERNEL, ONE POSITION: refuse a second position for a kernel the main registry already holds ---
  try {
    const ki = await fetch("https://www.alexanarch.org/api/kernel-index.json").then(r => r.json());
    const hit = ki?.kernels?.[h0];
    if (hit)
      return res.status(200).json({
        status: "already-positioned",
        axn: hit.axn,
        record: "https://www.alexanarch.org" + hit.record,
        note: "This kernel already holds a position in the main registry (deposit #" + hit.deposit_number + "). One kernel, one position — no second address is allocated.",
      });
  } catch (e) { /* index unreachable: proceed; the pipeline-side guard is the second lock */ }

  // --- allocate a registry position from the shared ledger (compare-and-swap) ---
  const ledgerApi = "https://api.github.com/repos/leesharks000/alexanarch/contents/data/symbolon-registry/allocation.json";
  let hexPos = null;
  for (let attempt = 0; attempt < 4 && !hexPos; attempt++) {
    const lr = await fetch(ledgerApi, { headers: gh });
    if (!lr.ok) break;
    const lj = await lr.json();
    const ledger = JSON.parse(Buffer.from(lj.content, "base64").toString("utf8"));
    // WAVE-HEXPOS-01 defense-in-depth: even if a deposit-side mint failed to bump
    // this ledger, never allocate at or below the highest position the central
    // registry already holds (contested 05AF, 2026-08-05, was exactly this gap).
    let candidate = ledger.next_hex;
    try {
      const cr = await fetch("https://www.alexanarch.org/data/axn-central-registry.json");
      if (cr.ok) {
        const cj = await cr.json();
        let maxPos = 0;
        for (const k in (cj.positions || {})) {
          const v = parseInt(k, 16);
          if (!isNaN(v) && v > maxPos) maxPos = v;
        }
        if (maxPos >= parseInt(candidate, 16)) {
          candidate = (maxPos + 1).toString(16).toUpperCase().padStart(4, "0");
        }
      }
    } catch (e) { /* registry unreachable: ledger candidate stands */ }
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

  // optional storage: bytes seen → true verification of AXN₀
  let retrieval = null, verified = false;
  if (store) {
    const crypto = require("crypto");
    const bytes = Buffer.from(store.content_b64, "base64");
    const sha = crypto.createHash("sha256").update(bytes).digest("hex");
    if (sha !== h0)
      return res.status(422).json({ error: "stored bytes do not hash to axn0.sha256 — refusing to store a file that is not the sealed core" });
    verified = true;
    const safe = String(store.filename || "file").replace(/[^A-Za-z0-9._-]/g, "_").slice(0, 80);
    const fpath = `data/symbolon-registry/files/${key}-${safe}`;
    const fr = await fetch(`https://api.github.com/repos/leesharks000/alexanarch/contents/${fpath}`, {
      method: "PUT", headers: { ...gh, "Content-Type": "application/json" },
      body: JSON.stringify({ message: `SYMBOLON STORE ${hexPos} · ${key} (sealed core, hash-verified at ingest)`, content: store.content_b64 }),
    });
    if (fr.ok) retrieval = `https://www.alexanarch.org/${fpath}`;
  }

  const entry = {
    axn: fullAxn,
    position: hexPos,
    family,
    registered: new Date().toISOString(),
    status: verified ? "witnessed-verified" : "witnessed-unverified",
    // VERIFICATION IS DATED (2026-08-06): a status without a timestamp is a
    // memory, not a measurement. Entries previously read "witnessed-verified"
    // with verified_at null, so a depositor could not tell WHEN her bytes were
    // last checked. Both fields are set at ingest and re-stamped on every run
    // of scripts/verify_symbolon_store.py, which re-hashes stored cores against
    // their kernels — the identifier IS the expected hash, so re-verification
    // needs no external truth and can run forever.
    verified_at: verified ? new Date().toISOString() : null,
    last_verified_at: verified ? new Date().toISOString() : null,
    verification_method: verified
      ? "sha256 of stored bytes compared to the AXN₀ kernel at ingest"
      : null,
    core_stored: !!retrieval,
    custody: {
      terms: "Stored cores live in this archive's public version-controlled repository and are served without account, login, or expiry. Any change or removal appears as a dated commit; nothing is silently deleted.",
      single_point_of_failure: "One administrator, one code host, one serving platform. Durable against link rot, accidental overwrite and quiet editing; NOT durable against a platform decision — this archive was itself terminated elsewhere in June 2026. A registry entry is a record, not a promise of perpetual hosting.",
      mirror_freely: "Listed with hash and length in /resourcesync/resourcelist.xml and /data/symbolon-registry/MANIFEST.json, and checksummed in /SHA256SUMS.txt. Fetch, hash, compare — copying requires no permission and verification requires no trust in this archive. Independent custody means a copy held by someone who is not this archive's administrator, on a platform it does not use.",
      depositor_holds: "The depositor's own original plus the Seed A sidecar can prove the work anywhere, with or without this archive. That is the point of splitting the identifier in two.",
    },
    retrieval,
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
    status: verified ? "witnessed-verified (bytes stored; AXN₀ confirmed against the sealed core)" : "witnessed",
    axn: fullAxn,
    retrieval,
    axn0: g0,
    axn1: g1,
    record: `https://www.alexanarch.org/${path}`,
    note: "Witnessed as a provenance registration (witnessed-unverified). The record publishes with the next deploy, typically within two minutes.",
  });
};
