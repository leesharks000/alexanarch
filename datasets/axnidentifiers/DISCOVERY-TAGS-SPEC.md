# FLEET DISCOVERY TAGS v1.0 (MANUS-directed 2026-08-03)
Machine-visible on EVERY fleet surface (all ~28 sites), in <head>:
```html
<link rel="alternate" type="application/xml" title="OAI-PMH repository — Alexanarch" href="https://www.alexanarch.org/oai">
<link rel="axn-stamper" title="AXN Stamp &amp; Verify" href="https://www.alexanarch.org/mint/stamp/">
<meta name="axn-registry" content="https://www.alexanarch.org/data/axn-central-registry.json">
```
Human-visible on SOME: alexanarch (nav/footer — already links stamper; add "OAI-PMH" to footer),
axnidentifiers.org (stamper is the primary CTA; OAI stays machine-only), machinemediation +
persistentidentifiers (footer line "Harvest this archive: OAI-PMH"). Satellites: machine tags only.
ROLLOUT: msp_apply.py-style stateless pass over the fleet (discovers via msp.json), injecting the
block into <head> where absent; alexanarch record pages get it via the wire_deposit template + one
regen pass. Applied 2026-08-03: axnidentifiers-site, /axn/constitution/, alexanarch homepage,
stamper page. Remainder queued for next tooled session.
