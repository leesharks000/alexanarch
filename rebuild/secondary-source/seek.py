"""seek.py <seated text> <needle> [before after] — find a needle in a seated text with diacritics, case and whitespace ignored, and print the
seated text's own wording around it. A reading tool for the locus table; it changes nothing."""
import sys, unicodedata as U, re
def base(s): return "".join(c for c in U.normalize("NFD", s) if not U.combining(c)).lower()
t = " ".join(open(sys.argv[1], encoding="utf-8", errors="replace").read().split())
b = base(t); idx = []
for i, c in enumerate(t):
    idx += [i] * len(base(c))
n = base(" ".join(sys.argv[2].split())); a = int(sys.argv[3]) if len(sys.argv) > 3 else 200; z = int(sys.argv[4]) if len(sys.argv) > 4 else 600
hits = [m.start() for m in re.finditer(re.escape(n), b)]
print(f"[{len(hits)} hit(s)]")
for h in hits[:3]:
    s = idx[h]; print("…" + t[max(0, s - a):s + z] + "…\n")
