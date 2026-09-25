# Estate Recovery Runbook

## 1. Verify the custody set

From the recovery directory:

```bash
sha256sum -c SHA256SUMS.txt
```

Do not restore from a set that fails verification.

## 2. Restore Alexanarch from its Git bundle

```bash
git clone bundles/alexanarch.bundle alexanarch
cd alexanarch
git fsck --full
```

A bundle preserves Git objects and refs. It does not automatically contain Git LFS payloads or independent submodule repositories; consult `recovery-index.tsv` and the `lfs/` directory.

## 3. Restore without any Git forge

The default-branch worktree archive can be unpacked directly:

```bash
mkdir alexanarch-static
cd alexanarch-static
tar -xzf ../worktrees/alexanarch-main.tar.gz
python3 -m http.server 8080
```

Open `http://localhost:8080/`.

## 4. Restore the resolution graph

Confirm that the restored tree contains:

- `data/registry.json`;
- canonical texts under `data/texts/`;
- static records under `s/records/`;
- AXN resolver pages under `s/axn/`;
- DOI-resolution data;
- checksum manifests;
- deposit schema and machine-facing manifests.

A homepage-only mirror is not an archive restoration.

## 5. Restore to a new forge

Create an empty repository at an unrelated provider, then:

```bash
cd alexanarch
git remote remove origin 2>/dev/null || true
git remote add origin git@example.org:archive/alexanarch.git
git push --mirror origin
```

Restore tier 0 repositories before tiers 1 and 2, using `estate-repos.tsv`.

## 6. Serve without Vercel

Copy the restored site to `/srv/alexanarch` and use `counterinfra/Caddyfile` with Caddy or translate its small set of redirects and headers to another static server. Vercel is a delivery provider, not a computational requirement of the archive.

## 7. Domain failover

1. Deploy to the replacement server under a temporary hostname.
2. Verify HTTPS, canonical URLs, redirects, JSON endpoints, and AXN resolution.
3. Change the relevant DNS records.
4. Preserve the former deployment as a mirror rather than deleting it.
5. Record the new custody and serving locations outside the affected provider.

Registrar, DNS-provider, renewal, recovery-contact, and transfer-lock data belong in a private custody manifest.

## 8. Clean-room acceptance test

A person with no access to CERN, the original GitHub account, or Vercel must be able to:

1. verify all checksums;
2. clone the Alexanarch bundle;
3. recover the registry and canonical corpus;
4. serve the static site;
5. resolve an AXN to its record and text;
6. push the restored history to another forge.

Record every test date, recovery-set identifier, failure, warning, and repair.
