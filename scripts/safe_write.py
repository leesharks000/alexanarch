"""safe_write.py — never truncate the registry again.

json.dump writes INCREMENTALLY. When it hits a character it cannot encode it
raises mid-write, leaving the destination truncated — a corrupted registry that
the next cp then propagates into the repository. That happened once, on a lone
surrogate produced by writing an emoji as \\ud83d\\udddd in a Python literal
instead of \\U0001F5DD.

This serialises to a STRING FIRST, so an encoding failure raises before the file
is touched, then writes to a temporary file and moves it into place atomically.
The destination is either the old valid file or the new valid file, never a
half-written one. It also re-reads and parses what it wrote, because a write
that cannot be read back is not a write.
"""
import json, os, tempfile


def safe_json_write(obj, path):
    text = json.dumps(obj, ensure_ascii=False, indent=1)   # raises HERE, before any write
    text.encode('utf-8')                                    # and surrogates raise HERE
    d = os.path.dirname(os.path.abspath(path))
    fd, tmp = tempfile.mkstemp(dir=d, suffix='.tmp')
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(text)
        with open(tmp, encoding='utf-8') as f:
            json.load(f)                                    # read-back check
        os.replace(tmp, path)                               # atomic
    except Exception:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise
    return len(text)
