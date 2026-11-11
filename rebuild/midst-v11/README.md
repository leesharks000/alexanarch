# EA-MIDST-01 v1.1 — draft (not deposited)

The v1.1 draft of #1758 (AXN-0C67), "In the Midst of the Seven", made 2026-11-11 at the author's word ("lets draft it all"; "yup lets fold that all in").

- `EA-MIDST-01-v1.1-draft.md` — the paper, v1.0 transformed in place (§19.9 records what changed and why).
- `apply_v11.py` — pass one, from the v1.0 seated text (`sed -n 44,600p data/texts/AXN-0C67-text.md > v10-body.md`).
- `apply_v11d.py` — pass four, ChatGPT's review of the draft (§19.11).
- `apply_v11c.py` — pass three, an outside review of the draft, adopted in part at the author's ruling (§19.10).
- `apply_v11b.py` — pass two, the Haran Gawaita read whole; it asserts every new Gawaita quotation against the author's copy of Drower's translation (the Gnostic Society Library page), which is not committed: Drower's translation is under copyright.
- Greek: `python3 rebuild/philo-out-loud/quotecheck.py rebuild/midst-v11/EA-MIDST-01-v1.1-draft.md` (311 quotations, 0 misses on 2026-11-11).

Drafts stay drafts until the author says deposit.
