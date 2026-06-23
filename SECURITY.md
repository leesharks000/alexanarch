# Security policy

Alexanarch is operated by one person. There is no on-call team, no support contract, and no service-level commitment. Security reports are handled best-effort within the constraints of that reality.

## Reporting a vulnerability

**Email**: leesharks00@gmail.com

Please use the subject prefix `[ALEXANARCH SECURITY]` so the report doesn't get lost in regular correspondence.

In your report, please include:

- A description of the issue
- The URL or file path affected
- Steps to reproduce
- The impact you observed
- Any mitigation suggestions

For a hostile-content example (XSS payload, injection attempt, etc.), please describe the construction in prose rather than including a working exploit in the email body.

## Disclosure timeline

Best-effort: I aim to acknowledge within 7 days, propose a remediation within 14 days for confirmed issues, and ship a fix within 30 days. Critical issues (active exploitation, broad data exposure, identifier integrity compromise) are prioritized over routine ones. I'll keep you updated through the cycle.

Please give a reasonable window before public disclosure. Coordinated disclosure is welcomed; I'm happy to credit reporters in the commit message and the security log.

## Supported surfaces

The current canonical deployment is `https://alexanarch.org/` (and `https://www.alexanarch.org/`, which serves the same release). Reports about:

- Static record pages at `/s/records/<N>/`
- The browse, wiki, graph, captures, resolve, observatory, lexical, citations, addresses, datasets routes
- The home page, deposit form, identifiers, principles, guide, manifest pages
- The mint workflow (`.github/workflows/mint-axn.yml`) and validator (`scripts/validate_deposit.py`)
- Registry, chunk, and protocol data files

are in scope. Reports about third-party services Alexanarch integrates with (GoatCounter analytics, Vercel hosting, GitHub) should generally go to those vendors directly; please cc this address if the issue affects Alexanarch users specifically.

## Known categories of concern

These are documented gaps that I'm actively working on; new reports in these areas are still useful but I'm aware of them:

- **Stored content rendering**: the dynamic record path at `/records/?id=N` performs Markdown-to-HTML rendering with a permissive raw-HTML pass-through. The static counterpart at `/s/records/<N>/` is safer. As of 2026-06, dynamic `/records/?id=N` redirects to the static record via `vercel.json`.
- **Deposit-side sanitization**: the mint workflow's sanitizer handles URL schemes, control characters, BIDI overrides, and length limits, but does not currently strip arbitrary HTML from free-text fields. The fix is part of the open-deposit hardening track.
- **Artifact custody**: uploaded files attached to deposit issues remain hosted on GitHub. Alexanarch retains the deposit's metadata record and the file's URL, not the file's bytes. This is being addressed (planned: artifact ingestion + manifest hashing).

## Emergency mint suspension

If a vulnerability affects the mint pathway and external deposits should be temporarily disabled, the operator (Lee Sharks) can:

1. Toggle the `.github/workflows/mint-axn.yml` workflow to "Disable workflow" via the GitHub Actions UI
2. Add a `pre-flight check failed — manual review required` block at the top of the validator
3. Post a notice on the home page banner

Past suspension events are recorded in commit messages tagged `mint-suspension:`.

## Bug bounty

No formal bug bounty. Acknowledgment in the commit message + credit in the security log + my genuine gratitude. If you want a more formal arrangement, please reach out.

---

*Last updated 2026-06-23.*
