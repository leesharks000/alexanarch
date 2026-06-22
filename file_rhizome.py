#!/usr/bin/env python3
"""
File Rhizome — automatic chunking of append-only files with hash-anchored index.

Solves the infinite-append problem: any file configured to grow without bound
will break at scale. The rhizome sets a size threshold, rotates the current
file into an immutable hash-named chunk when the threshold is reached, and
maintains an index that maps chunks to their content ranges.

Design:
    data/ledger/
        index.json            -- chunk index
        cha.ledger           -- current active chunk (always present)
        chunks/
            cha.20260622-a3f2.ledger
            cha.20260815-7b1c.ledger
            ...

Index format (json):
    {
        "chunks": [
            {
                "id": "cha.20260622-a3f2.ledger",
                "filename": "chunks/cha.20260622-a3f2.ledger",
                "hash": "a3f2c891...",                 # SHA-256 of chunk content
                "first_line_preview": "[2026-06-22T...] | TX_MINT | ...",
                "last_line_preview":  "[2026-08-15T...] | TX_INVOKE | ...",
                "line_count": 49873,
                "size_bytes": 10485100,
                "closed_at": "2026-08-15T14:32:11Z"
            }
        ],
        "current": {
            "filename": "cha.ledger",
            "active_since": "2026-08-15T14:32:11Z",
            "line_count": 12,
            "size_bytes": 3024
        },
        "thresholds": {
            "max_size_bytes": 10485760,    # 10 MB
            "max_line_count": 50000        # safety cap
        }
    }

Usage:
    rh = FileRhizome(active_path='data/ledger/cha.ledger', index_path='data/ledger/index.json')
    rh.maybe_rotate()                       # check thresholds, rotate if needed
    rh.append_lines(['tx_line1', 'tx_line2'])
    for line in rh.read_all():              # iterate across all chunks + current
        process(line)
"""
import json, hashlib, shutil
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_MAX_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB
DEFAULT_MAX_LINE_COUNT = 50000             # safety cap


class FileRhizome:
    def __init__(self, active_path, index_path=None,
                 max_size_bytes=DEFAULT_MAX_SIZE_BYTES,
                 max_line_count=DEFAULT_MAX_LINE_COUNT):
        self.active = Path(active_path)
        self.index_path = Path(index_path) if index_path else self.active.parent / 'index.json'
        self.chunks_dir = self.active.parent / 'chunks'
        self.max_size_bytes = max_size_bytes
        self.max_line_count = max_line_count
        self.basename = self.active.stem  # e.g. 'cha' from 'cha.ledger'
        self.extension = self.active.suffix  # e.g. '.ledger'

    # ---- Index management ----

    def load_index(self):
        if not self.index_path.exists():
            return {
                'chunks': [],
                'current': {
                    'filename': self.active.name,
                    'active_since': datetime.now(timezone.utc).isoformat(),
                    'line_count': 0,
                    'size_bytes': 0,
                },
                'thresholds': {
                    'max_size_bytes': self.max_size_bytes,
                    'max_line_count': self.max_line_count,
                },
            }
        with open(self.index_path) as f:
            return json.load(f)

    def save_index(self, idx):
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.index_path, 'w') as f:
            json.dump(idx, f, indent=2, ensure_ascii=False)

    def _refresh_current(self, idx):
        """Update 'current' block with actual file state."""
        if self.active.exists():
            text = self.active.read_text()
            lines = [l for l in text.splitlines() if l.strip()]
            idx['current']['line_count'] = len(lines)
            idx['current']['size_bytes'] = self.active.stat().st_size
        else:
            idx['current']['line_count'] = 0
            idx['current']['size_bytes'] = 0
        return idx

    # ---- Rotation ----

    def needs_rotation(self):
        if not self.active.exists():
            return False
        size = self.active.stat().st_size
        if size >= self.max_size_bytes:
            return True
        # Also count lines
        with open(self.active) as f:
            line_count = sum(1 for _ in f)
        if line_count >= self.max_line_count:
            return True
        return False

    def maybe_rotate(self, force=False):
        """Rotate active → chunk if thresholds exceeded. Returns chunk metadata or None."""
        if not force and not self.needs_rotation():
            return None
        if not self.active.exists():
            return None

        content = self.active.read_bytes()
        if not content.strip():
            return None  # nothing to rotate

        # Compute hash
        full_hash = hashlib.sha256(content).hexdigest()
        hash_prefix = full_hash[:8]
        timestamp = datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')

        # Build chunk filename
        chunk_id = f"{self.basename}.{timestamp}-{hash_prefix}{self.extension}"
        self.chunks_dir.mkdir(parents=True, exist_ok=True)
        chunk_path = self.chunks_dir / chunk_id

        # Get previews
        lines = content.decode('utf-8', errors='replace').splitlines()
        non_empty = [l for l in lines if l.strip() and not l.startswith('#')]
        first_preview = non_empty[0][:200] if non_empty else ''
        last_preview = non_empty[-1][:200] if non_empty else ''

        # Move active → chunk
        shutil.copy2(self.active, chunk_path)

        # Build chunk metadata
        chunk_meta = {
            'id': chunk_id,
            'filename': f"chunks/{chunk_id}",
            'hash': full_hash,
            'first_line_preview': first_preview,
            'last_line_preview': last_preview,
            'line_count': len(non_empty),
            'size_bytes': len(content),
            'closed_at': datetime.now(timezone.utc).isoformat(),
        }

        # Update index
        idx = self.load_index()
        idx['chunks'].append(chunk_meta)
        idx['current'] = {
            'filename': self.active.name,
            'active_since': datetime.now(timezone.utc).isoformat(),
            'line_count': 0,
            'size_bytes': 0,
        }
        idx['thresholds'] = {
            'max_size_bytes': self.max_size_bytes,
            'max_line_count': self.max_line_count,
        }
        self.save_index(idx)

        # Reset active file (preserve any header/comment lines)
        header_lines = [l for l in lines if l.startswith('#')][:5]
        if header_lines:
            self.active.write_text('\n'.join(header_lines) + '\n')
        else:
            self.active.write_text('')

        return chunk_meta

    # ---- Append ----

    def append_lines(self, lines):
        """Append lines to the active file, rotating first if needed."""
        self.maybe_rotate()
        with open(self.active, 'a') as f:
            for line in lines:
                if not line.endswith('\n'):
                    line += '\n'
                f.write(line)
        # Refresh index 'current' counters
        idx = self.load_index()
        idx = self._refresh_current(idx)
        self.save_index(idx)

    # ---- Read across all chunks + active ----

    def read_all(self):
        """Yield lines from all chunks in order, then from current active."""
        idx = self.load_index()
        for chunk in idx.get('chunks', []):
            chunk_path = self.active.parent / chunk['filename']
            if chunk_path.exists():
                with open(chunk_path) as f:
                    for line in f:
                        yield line.rstrip('\n')
        if self.active.exists():
            with open(self.active) as f:
                for line in f:
                    yield line.rstrip('\n')

    def stats(self):
        """Return total statistics across all chunks + current."""
        idx = self.load_index()
        idx = self._refresh_current(idx)
        chunks = idx.get('chunks', [])
        total_chunks = len(chunks)
        total_lines = sum(c['line_count'] for c in chunks) + idx['current'].get('line_count', 0)
        total_bytes = sum(c['size_bytes'] for c in chunks) + idx['current'].get('size_bytes', 0)
        return {
            'total_chunks_closed': total_chunks,
            'current_active': idx['current']['filename'],
            'total_lines_across_rhizome': total_lines,
            'total_bytes_across_rhizome': total_bytes,
            'current_size_bytes': idx['current'].get('size_bytes', 0),
            'thresholds': idx.get('thresholds', {}),
        }


def cli():
    import sys
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == 'rotate':
        path = sys.argv[2] if len(sys.argv) > 2 else 'data/ledger/cha.ledger'
        rh = FileRhizome(active_path=path)
        meta = rh.maybe_rotate(force=True)
        if meta:
            print(f"Rotated: {meta['id']} ({meta['size_bytes']} bytes, {meta['line_count']} lines)")
            print(f"  hash: {meta['hash'][:16]}...")
        else:
            print("Nothing to rotate.")
    elif cmd == 'stats':
        path = sys.argv[2] if len(sys.argv) > 2 else 'data/ledger/cha.ledger'
        rh = FileRhizome(active_path=path)
        print(json.dumps(rh.stats(), indent=2))
    elif cmd == 'check':
        path = sys.argv[2] if len(sys.argv) > 2 else 'data/ledger/cha.ledger'
        rh = FileRhizome(active_path=path)
        print(f"needs_rotation: {rh.needs_rotation()}")
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == '__main__':
    cli()
