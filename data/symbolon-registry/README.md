# Symbolon Registry — the witness layer
Per AXN-SYMBOLON-SPEC v0.2 §7 (deposit #1432, AXN:05A9.OPERATIVE.🐚🌪️🕖🫵⏩○):
recording a symbolon is a provenance registration — the witnessed tuple
⟨AXN₀, AXN₁, timestamp, Seed A⟩. Only Seed A crosses; Seed B never does.
Entries land as `entries/<axn0-sha16>.json`, status `witnessed-unverified`
(internal consistency checked at ingest: glyphs recomputed from hashes;
byte verification is a separate act per §9). Witnessing transport:
POST to /api/register-symbolon, or the button at /mint/stamp/, or email
the sidecar to the archive.
