#!/usr/bin/env python3
"""harvest_palette.py — build the capture-registry repair palette.

PURPOSE. The Capture Registry is broken in different ways across different
seatings, and the repair cannot proceed from any single copy. This script
gathers EVERY version of EVERY capture-bearing file from EVERY source, keeps
each strictly separate and attributed, and writes them into one working
database. Nothing is merged, reconciled, deduplicated by content, or preferred
over anything else. The database is a palette, not an answer.

SOURCES (four repositories, full history):
  alexanarch             data/EA-WG-CAPTURES-01*.json and archived variants
  leesharks.com          captures/registry.json  (its OWN registry, not a mirror)
  godkinggoogle          captures/registry.json  (its OWN registry, not a mirror)
  machinemediation-org   data/registry.json, captures/<slug>.md companion
                         transcript files, data/captures/<dir>/manifest.json

METHOD. For each source and each tracked path, walk every commit that touched
it, resolve the blob at that commit, and extract distinct blobs only — the same
bytes appearing in fifty commits is one version, recorded with its first and
last appearance. Each extracted version is decomposed to the field level so
that any capture, any field, can be asked: what values has this ever held,
where, and when.

WHAT IS DELIBERATELY NOT DONE. No precedence rules. No "latest wins". No
normalization of field names across sources. No repair. Those are judgements to
be made later, per field, with the palette in view.
"""
import json, os, re, sqlite3, subprocess, sys, hashlib

HOME = '/home/claude'
DB = os.path.join(HOME, 'palette', 'capture-palette.sqlite')
SOURCES = {
    'alexanarch': ('src-alexanarch', [
        'data/EA-WG-CAPTURES-01.json',
        'data/EA-WG-CAPTURES-01-v8.3.json',
        'data/EA-WG-CAPTURES-01-v8.11.json',
        'data/EA-WG-CAPTURES-01-v9.6.json',
        'data/archive/EA-WG-CAPTURES-01-v9.42-pre-transcript-extraction-20260811.json',
        'datasets/capture-registry/EA-WG-CAPTURES-01.json',
    ]),
    'leesharks.com': ('src-leesharks.com', ['captures/registry.json']),
    'godkinggoogle': ('src-godkinggoogle', ['captures/registry.json']),
    'machinemediation': ('src-machinemediation-org', ['data/registry.json']),
}


def git(repo, *args):
    return subprocess.run(['git', '-C', os.path.join(HOME, repo)] + list(args),
                          capture_output=True, text=True, errors='replace').stdout


def commits_for(repo, path):
    out = git(repo, 'log', '--all', '--format=%H|%ad', '--date=short', '--', path)
    return [l.split('|') for l in out.strip().split('\n') if l.strip()]


def blob_at(repo, commit, path):
    r = subprocess.run(['git', '-C', os.path.join(HOME, repo), 'rev-parse',
                        '%s:%s' % (commit, path)], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else None


def cat_blob(repo, sha):
    r = subprocess.run(['git', '-C', os.path.join(HOME, repo), 'cat-file', '-p', sha],
                       capture_output=True, text=True, errors='replace')
    return r.stdout


def entries_of(doc):
    """Return the capture list from whatever shape this registry version uses."""
    if isinstance(doc, list):
        return doc
    if isinstance(doc, dict):
        for k in ('entries', 'captures', 'records', 'items'):
            if isinstance(doc.get(k), list):
                return doc[k]
    return []


def key_of(e):
    """A stable-ish identity for a capture WITHOUT assuming any source's scheme."""
    for k in ('slug', 'id', 'capture_id'):
        v = e.get(k)
        if v not in (None, ''):
            return str(v)
    q = e.get('q') or e.get('query') or ''
    d = e.get('date') or ''
    return ('QUERY:%s|%s' % (str(q)[:80], d)) if q else 'UNKEYED'


def main():
    os.makedirs(os.path.dirname(DB), exist_ok=True)
    if os.path.exists(DB):
        os.remove(DB)
    db = sqlite3.connect(DB)
    db.executescript("""
    CREATE TABLE versions(
      id INTEGER PRIMARY KEY, source TEXT, path TEXT, blob TEXT,
      first_commit TEXT, first_date TEXT, last_commit TEXT, last_date TEXT,
      n_commits INT, doc_version TEXT, n_entries INT, bytes INT);
    CREATE TABLE observations(
      version_id INT, source TEXT, path TEXT, date TEXT, blob TEXT,
      capture_key TEXT, field TEXT, value TEXT, value_len INT, value_sha TEXT);
    CREATE TABLE files(
      source TEXT, path TEXT, blob TEXT, first_date TEXT, last_date TEXT,
      n_commits INT, slug TEXT, kind TEXT, content TEXT, bytes INT);
    CREATE INDEX obs_key ON observations(capture_key, field);
    CREATE INDEX obs_src ON observations(source, field);
    CREATE INDEX ver_src ON versions(source, path);
    """)
    vid = 0
    for source, (repo, paths) in SOURCES.items():
        for path in paths:
            cs = commits_for(repo, path)
            if not cs:
                continue
            seen = {}
            for commit, date in cs:              # newest first
                sha = blob_at(repo, commit, path)
                if not sha:
                    continue
                if sha not in seen:
                    seen[sha] = {'first_commit': commit, 'first_date': date,
                                 'last_commit': commit, 'last_date': date, 'n': 0}
                s = seen[sha]
                s['n'] += 1
                if date <= s['first_date']:
                    s['first_commit'], s['first_date'] = commit, date
                if date >= s['last_date']:
                    s['last_commit'], s['last_date'] = commit, date
            for sha, meta in seen.items():
                raw = cat_blob(repo, sha)
                try:
                    doc = json.loads(raw)
                except Exception:
                    continue
                es = entries_of(doc)
                dv = str(doc.get('version')) if isinstance(doc, dict) else None
                vid += 1
                db.execute("INSERT INTO versions VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
                           (vid, source, path, sha, meta['first_commit'], meta['first_date'],
                            meta['last_commit'], meta['last_date'], meta['n'], dv,
                            len(es), len(raw)))
                rows = []
                for e in es:
                    if not isinstance(e, dict):
                        continue
                    k = key_of(e)
                    for field, val in e.items():
                        sval = val if isinstance(val, str) else json.dumps(val, ensure_ascii=False)
                        if sval is None:
                            sval = ''
                        rows.append((vid, source, path, meta['last_date'], sha, k, field,
                                     sval, len(sval),
                                     hashlib.sha256(sval.encode('utf-8')).hexdigest()[:16]))
                db.executemany("INSERT INTO observations VALUES(?,?,?,?,?,?,?,?,?,?)", rows)
                db.commit()
            print('%-18s %-58s %2d versions' % (source, path[-58:], len(seen)), flush=True)

    # companion transcript files and per-capture manifests, all versions
    for source, repo, pattern, kind in [
            ('machinemediation', 'src-machinemediation-org', r'^captures/.*\.md$', 'companion_md'),
            ('machinemediation', 'src-machinemediation-org', r'^data/captures/.*/manifest\.json$', 'manifest'),
            ('machinemediation', 'src-machinemediation-org', r'^data/captures/.*\.(md|json)$', 'capture_dir_file')]:
        allpaths = sorted(set(l for l in git(repo, 'log', '--all', '--pretty=format:',
                                            '--name-only').split('\n') if re.match(pattern, l)))
        n = 0
        for path in allpaths:
            cs = commits_for(repo, path)
            seen = {}
            for commit, date in cs:
                sha = blob_at(repo, commit, path)
                if not sha:
                    continue
                seen.setdefault(sha, {'first': date, 'last': date, 'n': 0})
                seen[sha]['n'] += 1
                seen[sha]['first'] = min(seen[sha]['first'], date)
                seen[sha]['last'] = max(seen[sha]['last'], date)
            for sha, m in seen.items():
                content = cat_blob(repo, sha)
                slug = os.path.basename(path).rsplit('.', 1)[0]
                if kind in ('manifest', 'capture_dir_file'):
                    slug = path.split('/')[2] if len(path.split('/')) > 2 else slug
                db.execute("INSERT INTO files VALUES(?,?,?,?,?,?,?,?,?,?)",
                           (source, path, sha, m['first'], m['last'], m['n'], slug, kind,
                            content, len(content)))
                n += 1
        db.commit()
        print('%-18s %-58s %2d file versions' % (source, kind, n), flush=True)

    v, o, f = (db.execute('SELECT COUNT(*) FROM %s' % t).fetchone()[0]
               for t in ('versions', 'observations', 'files'))
    k = db.execute('SELECT COUNT(DISTINCT capture_key) FROM observations').fetchone()[0]
    print('\nPALETTE: %d registry versions | %d field observations | %d distinct capture keys | %d file versions'
          % (v, o, k, f))
    db.close()


if __name__ == '__main__':
    main()
