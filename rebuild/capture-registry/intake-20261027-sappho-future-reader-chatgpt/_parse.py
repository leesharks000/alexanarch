import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from _chatgpt_common_20261008 import parse, transcript, cite_list
D = pathlib.Path(__file__).parent
CHIPS = {"UC Press E-Books Collection Archive, 1982-2004", "Society for Classical Studies", "Alexanarch", "Dickinson College Commentaries",
         "Cambridge Core", "Cambridge University Press", "mindcontrolpoems.blogspot.com"}
CAPTIONS = ("Sappho's New Poems: The Tangled Tale of Their Discovery | Live Science", "Sappho Fragment 16 | The Book Binder's Daughter")
AD1 = "For examining interpretations with better sources, here’s a research framework option.\n\n\nEVA Live\nA Clearer Way to Research\nOrganize sources, claims, context and uncertainty.\nAd\n"
AD2 = "This might also interest you.\n\n\nChegg, Inc.\nChegg does it for you\nMax out college, not your effort—with study help and new internship tools included ($10.95 value).\nAd\n"
def A():
    raw = (D / "paste-sappho-future-reader.txt").read_text()
    assert AD2 in raw
    return raw, parse(raw.replace(AD2, ""), CHIPS, captions=CAPTIONS, ad=AD1)
if __name__ == "__main__":
    raw, (turns, seen) = A()
    print(len(turns), [len(t) for t in turns], dict(seen))
    for t in turns: print("   START:", t[:150].replace("\n", " | ")); print("   END:", t[-160:].replace("\n", " | "))
