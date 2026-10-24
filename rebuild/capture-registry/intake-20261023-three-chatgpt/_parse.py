import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from _chatgpt_common_20261008 import parse, transcript, cite_list
D = pathlib.Path(__file__).parent
AD_A = "This might also interest you.\n\n\nLucid Software\nTurn Ideas Into Action with Lucidspark\nBring teams together with AI-powered brainstorming, sticky notes, and collaborative whiteboards.\nAd\n"
AD_B = "For mapping evolving thought, here’s a diagramming software option.\nLucid SoftwareDiagramming Software For Cross-Functional TeamsCreate professional diagrams for teams, projects, systems, and business processes using Lucid.\nAd\n"
MATH_B = ("T=(S,R,D)\nT=(S,R,D)\nHere, SS is the source, RR the receiver, and DD the change", "[math: T=(S,R,D)]\nHere, S is the source, R the receiver, and D the change")
FOOT_C = "Log in to upload a file and get help with it.\n\n\nLog in\n\nSign up for free\n"
def A():
    raw = (D / "paste-relationally-moral.txt").read_text()
    return raw, parse(raw, {"Alexanarch", "Goodreads", "Medium"}, ad=AD_A)
def B():
    raw = (D / "paste-october-1-23.txt").read_text()
    assert MATH_B[0] in raw
    return raw, parse(raw.replace(*MATH_B), {"Alexanarch", "The Self-Governing Library"}, ad=AD_B)
def C():
    raw = (D / "paste-gospel-of-antioch.txt").read_text()
    assert FOOT_C in raw
    return raw, parse(raw.replace(FOOT_C, ""), {"SciVora", "Crimson Hexagonal Archive", "Operative Semiotics", "Medium"})
if __name__ == "__main__":
    for f in (A, B, C):
        raw, (turns, seen) = f()
        print(f.__name__, len(turns), [len(t) for t in turns], dict(seen))
        for t in turns: print("   START:", t[:120].replace("\n", " | ")); print("   END:", t[-200:].replace("\n", " | "))
