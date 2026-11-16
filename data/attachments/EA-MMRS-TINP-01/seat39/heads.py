"""Running heads: a line that, with digits and punctuation removed, recurs 4 or more times in a file is taken as a running
head (or a repeated title line) and dropped before counting, so that a title word printed on every page is not counted as use."""
import re,collections
def body(text):
    L=text.split("\n"); key=lambda l: re.sub(r"[\W\d_]+"," ",l).strip().lower()
    c=collections.Counter(key(l) for l in L if key(l))
    return "\n".join(l for l in L if not key(l) or c[key(l)]<4)
