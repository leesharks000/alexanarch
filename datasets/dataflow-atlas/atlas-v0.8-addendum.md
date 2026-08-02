# Dataflow Atlas — v0.8 addendum (2026-08-02)
## Capture-registry image host + symbolon copy/verify surfaces

**CAPTURE IMAGE HOST (canonical rule).** The AI Overview Capture Registry renders
at machinemediation.org/captures/ (captures/index.html), but its images are served
from a SEPARATE host declared in that page as:

    IMG_BASE = 'https://godkinggoogle.vercel.app/captures/'

Therefore: capture screenshots go to the **godkinggoogle** repo under captures/,
referenced by **bare filename** in registry.json (imgs / images[].src) — the
renderer supplies the base. NOT to leesharks.com/captures/ (a different gallery
surface) and NEVER as an absolute URL (which double-prefixes and 404s). The
2026-08-02 anti-suppression display failure was exactly this: Aug-1 PNGs pushed
only to leesharks.com and a Jul-25 entry using an absolute URL; fixed by placing
all in godkinggoogle/captures/ with bare-filename references. (Note: godkinggoogle
has Vercel deployment protection, so server-side curl returns 403 even for present
files; a real browser session renders them — 403≠absent, 404=absent.)

**SYMBOLON COPY/VERIFY (mint/stamp/).** The result now renders a visible
tap-to-copy AXN box (iOS-safe: clipboard API → execCommand fallback → user-select:all
long-press), bound after any storage rewrite so the element persists. Verify accepts
(a) a dropped file (hashed, looked up by kernel) and (b) a pasted AXN / hex position
/ sha256 kernel — both resolve against data/axn-central-registry.json.

**RE-STAMP semantics.** Re-submitting a file with the same sealed core (AXN0) but a
new stamped form (AXN1 — e.g. after a stamp-geometry fix) dedupes to the existing
position and REFRESHES AXN1, logging the change in the entry's stamp_history. The
stamp is scaffold; the kernel is identity. One kernel, one position, throughout.
