// api/submit-transcript.js — the capture inbox.
//
// Operator, 2026-11-19 20:22: "there really should be a function to upload transcripts on the ask page.
// even if that was, not strictly automated for now, a place to paste them to GitHub for later processing".
//
// POST {query, surface, date, auth, transcript, notes?, submitter?, source_url?} as JSON. The function:
//   1. validates the fields and size (transcript ≤ 1.5 MB of text);
//   2. hashes the transcript (sha256 of its UTF-8 bytes) — the hash is the inbox key;
//   3. commits drafts/capture-inbox/<date-received>/<sha12>.json via the GitHub contents API
//      (token from env CAPTURE_TOKEN or SYMBOLON_TOKEN, never the client);
//   4. returns the inbox path and its GitHub URL.
//
// An inbox entry is not a capture. It is a transcript received, unseated; seating goes through
// scripts/capture_intake.py, which applies the registry's rule (source engagement in composition;
// the transcript is the capture) and records the address. Nothing is refused for its content here;
// the record of who sent what, when, is kept. drafts/ does not trigger a site build.
// If no token is set the endpoint answers 503 and the page offers the entry as a file instead.

const crypto = require("crypto");
const SURFACES = ["ChatGPT", "Google AI Overview", "Google AI Mode", "Google Search results page (no AI surface)",
  "Perplexity", "Claude", "Gemini", "Copilot", "Grok", "DeepSeek", "Kimi", "other"];
const MAX = 1_500_000;

module.exports = async (req, res) => {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  if (req.method === "OPTIONS") return res.status(204).end();
  if (req.method !== "POST") return res.status(405).json({ error: "POST the transcript as JSON." });

  const token = process.env.CAPTURE_TOKEN || process.env.SYMBOLON_TOKEN;
  if (!token) return res.status(503).json({ error: "inbox offline", fallback: "download the entry and send it to the archive" });

  let b = req.body;
  if (typeof b === "string") { try { b = JSON.parse(b); } catch { b = null; } }
  if (!b || typeof b !== "object") return res.status(400).json({ error: "body must be a JSON object" });
  const str = (v, n) => (typeof v === "string" ? v.trim().slice(0, n) : "");
  const transcript = typeof b.transcript === "string" ? b.transcript.replace(/\r\n/g, "\n") : "";
  const query = str(b.query, 4000);
  if (!transcript.trim()) return res.status(400).json({ error: "the transcript is empty" });
  if (!query) return res.status(400).json({ error: "the query (the prompt as typed) is required: it is the address" });
  if (Buffer.byteLength(transcript, "utf8") > MAX) return res.status(413).json({ error: "transcript over 1.5 MB; split it by round" });

  const sha = crypto.createHash("sha256").update(transcript, "utf8").digest("hex");
  const now = new Date();
  const day = now.toISOString().slice(0, 10);
  const path = `drafts/capture-inbox/${day}/${sha.slice(0, 12)}.json`;
  const entry = {
    status: "inbox — received, not seated",
    received_at: now.toISOString(),
    query,
    surface: SURFACES.includes(b.surface) ? b.surface : (str(b.surface, 80) || "unstated"),
    date_run: /^\d{4}-\d{2}-\d{2}$/.test(b.date || "") ? b.date : "unstated",
    auth: str(b.auth, 120) || "unstated",
    rounds_note: str(b.rounds_note, 2000),
    notes: str(b.notes, 4000),
    submitter: str(b.submitter, 200),
    source_url: str(b.source_url, 1000),
    from_page: str(b.from_page, 300),
    transcript_sha256: sha,
    transcript_bytes: Buffer.byteLength(transcript, "utf8"),
    transcript,
  };
  const api = `https://api.github.com/repos/leesharks000/alexanarch/contents/${path}`;
  const gh = { Authorization: `Bearer ${token}`, Accept: "application/vnd.github+json", "User-Agent": "alexanarch-capture-inbox" };

  const ex = await fetch(api, { headers: gh });
  if (ex.status === 200)
    return res.status(200).json({ status: "already received (same transcript bytes)", path, sha256: sha,
      url: `https://github.com/leesharks000/alexanarch/blob/main/${path}` });

  const put = await fetch(api, {
    method: "PUT", headers: { ...gh, "Content-Type": "application/json" },
    body: JSON.stringify({
      message: `CAPTURE INBOX ${day} · ${entry.surface} · ${sha.slice(0, 12)} — transcript received, not seated`,
      content: Buffer.from(JSON.stringify(entry, null, 1)).toString("base64"),
    }),
  });
  if (!put.ok) return res.status(502).json({ error: `GitHub refused the write (${put.status}); download the entry instead` });
  return res.status(201).json({ status: "received", path, sha256: sha, url: `https://github.com/leesharks000/alexanarch/blob/main/${path}` });
};
