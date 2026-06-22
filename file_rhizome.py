#!/usr/bin/env python3
"""
File Rhizome v2 — Recursive append-only files with cascading rotation.

THE PRINCIPLE: the same rotation pattern applies at every level.

When the active file at level N reaches the size threshold, it is rotated
into an immutable hash-named chunk under archive/l{N}/. The metadata
describing that new chunk is then APPENDED as a JSON line to the active
file at level N+1.

When level N+1's active file reaches its threshold, IT is rotated. Its
chunk metadata gets appended to level N+2. And so on, cascading up.

This is turtles all the way up: a Merkle-like tree where each level is
a queryable catalogue of the level below, and each level itself becomes
chunked by the SAME mechanism. There is no special "top" level —
whenever the highest currently-existing active reaches threshold, a new
level above is born.

LAYOUT:

    data/ledger/
        cha.ledger              <- L0 active (plaintext transactions)
        cha.l1.idx              <- L1 active (JSONL of L0 chunk metadata)
        cha.l2.idx              <- L2 active (JSONL of L1 chunk metadata)
        cha.summary.json        <- always-present overview pointer
        archive/
            l0/
                cha.{ts}-{hash8}.l0    closed L0 chunks (plaintext)
            l1/
                cha.{ts}-{hash8}.l1    closed L1 chunks (JSONL)
            ...

SAFETY PROPERTIES:
  - Plaintext at L0 (truncation-safe; no JSON brackets to break)
  - JSONL at L1+ (each line is independently parseable)
  - Closed chunks are immutable; never modified after closure
  - SHA-256 hash anchors every chunk
  - Summary file is the only mutable top-level pointer
  - Cascading rotation is atomic per level
"""
import json, hashlib, shutil
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_MAX_SIZE_BYTES = 10 * 1024 * 1024
DEFAULT_MAX_LINE_COUNT = 50000


def _now():
    return datetime.now(timezone.utc).isoformat()

def _ts_compact():
    return datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')

def _hash_bytes(b):
    return hashlib.sha256(b).hexdigest()


class _Level:
    """One level of the recursive rhizome."""

    def __init__(self, base_path, basename, level=0,
                 max_size_bytes=DEFAULT_MAX_SIZE_BYTES,
                 max_line_count=DEFAULT_MAX_LINE_COUNT):
        self.base_path = Path(base_path)
        self.basename = basename
        self.level = level
        self.max_size_bytes = max_size_bytes
        self.max_line_count = max_line_count

    @property
    def active_path(self):
        if self.level == 0:
            return self.base_path / self.basename
        stem = self.basename.split('.', 1)[0]
        return self.base_path / f"{stem}.l{self.level}.idx"

    @property
    def archive_dir(self):
        return self.base_path / 'archive' / f'l{self.level}'

    def chunk_filename(self, hash8):
        stem = self.basename.split('.', 1)[0]
        return f"{stem}.{_ts_compact()}-{hash8}.l{self.level}"

    def file_stats(self):
        if not self.active_path.exists():
            return 0, 0
        size = self.active_path.stat().st_size
        with open(self.active_path) as f:
            line_count = sum(1 for _ in f)
        return size, line_count

    def needs_rotation(self):
        size, line_count = self.file_stats()
        return size >= self.max_size_bytes or line_count >= self.max_line_count

    def rotate(self):
        if not self.active_path.exists():
            return None
        content = self.active_path.read_bytes()
        if not content.strip():
            return None

        full_hash = _hash_bytes(content)
        hash8 = full_hash[:8]
        chunk_name = self.chunk_filename(hash8)

        self.archive_dir.mkdir(parents=True, exist_ok=True)
        chunk_path = self.archive_dir / chunk_name
        shutil.copy2(self.active_path, chunk_path)

        lines = content.decode('utf-8', errors='replace').splitlines()
        non_empty = [l for l in lines if l.strip() and not l.startswith('#')]
        first_preview = non_empty[0][:200] if non_empty else ''
        last_preview = non_empty[-1][:200] if non_empty else ''

        meta = {
            'level': self.level,
            'id': chunk_name,
            'filename': f"archive/l{self.level}/{chunk_name}",
            'hash': full_hash,
            'first_line_preview': first_preview,
            'last_line_preview': last_preview,
            'line_count': len(non_empty),
            'size_bytes': len(content),
            'closed_at': _now(),
        }

        # Preserve L0 header lines (file format documentation)
        header_lines = [l for l in lines if l.startswith('#')][:8] if self.level == 0 else []
        if header_lines:
            self.active_path.write_text('\n'.join(header_lines) + '\n')
        else:
            self.active_path.write_text('')

        return meta

    def append_lines(self, lines):
        self.active_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.active_path, 'a') as f:
            for line in lines:
                if not line.endswith('\n'):
                    line += '\n'
                f.write(line)

    def list_chunks(self):
        if not self.archive_dir.exists():
            return []
        return sorted(self.archive_dir.iterdir())


class FileRhizome:
    """Recursive rhizome rooted at level 0."""

    def __init__(self, active_path,
                 max_size_bytes=DEFAULT_MAX_SIZE_BYTES,
                 max_line_count=DEFAULT_MAX_LINE_COUNT,
                 max_levels=8):
        active_path = Path(active_path)
        self.base_path = active_path.parent
        self.basename = active_path.name
        self.max_size_bytes = max_size_bytes
        self.max_line_count = max_line_count
        self.max_levels = max_levels

    def _level(self, n):
        return _Level(self.base_path, self.basename, level=n,
                      max_size_bytes=self.max_size_bytes,
                      max_line_count=self.max_line_count)

    @property
    def active_path(self):
        return self._level(0).active_path

    @property
    def summary_path(self):
        stem = self.basename.split('.', 1)[0]
        return self.base_path / f"{stem}.summary.json"

    def cascading_rotate(self, level=0):
        """Rotate at level if needed, cascading up. Returns list of rotations."""
        if level >= self.max_levels:
            return []
        L = self._level(level)
        if not L.needs_rotation():
            return []
        meta = L.rotate()
        if meta is None:
            return []
        parent = self._level(level + 1)
        parent.append_lines([json.dumps(meta, ensure_ascii=False)])
        downstream = self.cascading_rotate(level + 1)
        return [meta] + downstream

    def append_lines(self, lines):
        self.cascading_rotate(level=0)
        self._level(0).append_lines(lines)
        self.refresh_summary()

    def _all_chunks_at(self, level):
        """Walk levels above to enumerate all chunks at a given level."""
        chunks = []
        parent = self._level(level + 1)
        if parent.active_path.exists():
            with open(parent.active_path) as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    try:
                        entry = json.loads(line)
                        if entry.get('level') == level:
                            chunks.append(entry)
                    except json.JSONDecodeError:
                        continue
        if level + 1 < self.max_levels:
            parent_chunks = self._all_chunks_at(level + 1)
            for pc in parent_chunks:
                chunk_path = self.base_path / pc['filename']
                if chunk_path.exists():
                    with open(chunk_path) as f:
                        for line in f:
                            line = line.strip()
                            if not line:
                                continue
                            try:
                                entry = json.loads(line)
                                if entry.get('level') == level:
                                    chunks.append(entry)
                            except json.JSONDecodeError:
                                continue
        chunks.sort(key=lambda e: e.get('closed_at', ''))
        return chunks

    def read_all(self):
        """Yield all L0 transaction lines, oldest chunk first, active last."""
        for chunk_meta in self._all_chunks_at(0):
            chunk_path = self.base_path / chunk_meta['filename']
            if chunk_path.exists():
                with open(chunk_path) as f:
                    for line in f:
                        yield line.rstrip('\n')
        if self.active_path.exists():
            with open(self.active_path) as f:
                for line in f:
                    yield line.rstrip('\n')

    def stats(self):
        out = {
            'thresholds': {
                'max_size_bytes': self.max_size_bytes,
                'max_line_count': self.max_line_count,
            },
            'levels': [],
        }
        for n in range(self.max_levels):
            L = self._level(n)
            size, lc = L.file_stats()
            chunks_at_level = L.list_chunks()
            if not L.active_path.exists() and not chunks_at_level:
                break
            level_info = {
                'level': n,
                'active': L.active_path.name if L.active_path.exists() else None,
                'active_size_bytes': size,
                'active_line_count': lc,
                'closed_chunks_count': len(chunks_at_level),
            }
            out['levels'].append(level_info)
        total_lines = sum(c['line_count'] for c in self._all_chunks_at(0))
        if self.active_path.exists():
            with open(self.active_path) as f:
                total_lines += sum(1 for l in f
                                   if l.strip() and not l.startswith('#'))
        out['total_l0_transactions_across_rhizome'] = total_lines
        return out

    def refresh_summary(self):
        s = self.stats()
        s['updated_at'] = _now()
        with open(self.summary_path, 'w') as f:
            json.dump(s, f, indent=2, ensure_ascii=False)

    def migrate_from_v1(self, old_index_path):
        """One-time migration from v1 layout (chunks/, index.json) to v2."""
        old_index_path = Path(old_index_path)
        if not old_index_path.exists():
            return 'no v1 index to migrate'
        with open(old_index_path) as f:
            v1 = json.load(f)
        l1 = self._level(1)
        l0 = self._level(0)
        l0.archive_dir.mkdir(parents=True, exist_ok=True)
        migrated = []
        for chunk in v1.get('chunks', []):
            old_filename = chunk.get('filename', '')
            old_path = self.base_path / old_filename
            if not old_path.exists():
                continue
            old_basename = Path(old_filename).name
            new_basename = old_basename.replace('.ledger', '.l0')
            new_path = l0.archive_dir / new_basename
            shutil.move(str(old_path), str(new_path))
            new_meta = {
                'level': 0,
                'id': new_basename,
                'filename': f"archive/l0/{new_basename}",
                'hash': chunk.get('hash', ''),
                'first_line_preview': chunk.get('first_line_preview', ''),
                'last_line_preview': chunk.get('last_line_preview', ''),
                'line_count': chunk.get('line_count', 0),
                'size_bytes': chunk.get('size_bytes', 0),
                'closed_at': chunk.get('closed_at', _now()),
            }
            l1.append_lines([json.dumps(new_meta, ensure_ascii=False)])
            migrated.append(new_basename)
        old_chunks_dir = self.base_path / 'chunks'
        if old_chunks_dir.exists() and not any(old_chunks_dir.iterdir()):
            old_chunks_dir.rmdir()
        old_index_path.unlink()
        self.refresh_summary()
        return f"migrated {len(migrated)} chunks to v2 layout"


def cli():
    import sys
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    cmd = sys.argv[1]
    path = sys.argv[2] if len(sys.argv) > 2 else 'data/ledger/cha.ledger'
    rh = FileRhizome(active_path=path)
    if cmd == 'stats':
        print(json.dumps(rh.stats(), indent=2))
    elif cmd == 'rotate':
        cascade = rh.cascading_rotate(level=0)
        print(f"Cascade rotated {len(cascade)} level(s):")
        for meta in cascade:
            print(f"  L{meta['level']}: {meta['id']} ({meta['size_bytes']} bytes, {meta['line_count']} lines)")
    elif cmd == 'migrate':
        old = sys.argv[3] if len(sys.argv) > 3 else 'data/ledger/index.json'
        result = rh.migrate_from_v1(old)
        print(result)
    elif cmd == 'summary':
        rh.refresh_summary()
        print(f"summary written to {rh.summary_path}")
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == '__main__':
    cli()
