"""Legal-name guard, held as hashes so the guard itself does not publish the name.

The archive's absolute rule: the legal name never appears in any public-facing
output, deposit, metadata, or document. Until 2026-09-23 the guard carried the
name as a plain regex in scripts/check_state_conformance.py and
scripts/restore_from_blog.py, in a public repository -- the rule's own
enforcement was one of its violations. The name is now held only as SHA-256
digests of its lowercase forms.

contains_legal_name(text, substring=False)
  default   -- token match: any run of ASCII letters whose lowercase form hashes
               to a held digest. Matches everything the old conformance regex
               matched, and additionally a name token followed by digits.
  substring -- sliding match over every letter run, for the restore gate, which
               previously matched the bare substring anywhere in fetched HTML.
"""
import hashlib
import re

_HELD = frozenset({
    "00b1fbe3f2b837687740659947ca21c6b528898b798e0f35c0b933eceb3dd451",
    "70603d41740ad3c3b343e6f1c6af5005ad972fef5c138e95ce36df7b04e8e2c2",
})
_LENGTHS = (5, 6)
_RUN = re.compile(r"[A-Za-z]+")


def _h(s: str) -> str:
    return hashlib.sha256(s.encode("ascii")).hexdigest()


def contains_legal_name(text, substring: bool = False) -> bool:
    if not text:
        return False
    for m in _RUN.finditer(text):
        tok = m.group(0).lower()
        if not substring:
            if len(tok) in _LENGTHS and _h(tok) in _HELD:
                return True
            continue
        for n in _LENGTHS:
            for i in range(len(tok) - n + 1):
                if _h(tok[i:i + n]) in _HELD:
                    return True
    return False


class _Guard:
    """Drop-in for the old compiled regex: LEGAL_NAME.search(text) is truthy on a hit."""
    def search(self, text):
        return contains_legal_name(text)


LEGAL_NAME = _Guard()
