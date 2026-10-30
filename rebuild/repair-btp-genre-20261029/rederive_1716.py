"""Re-derive #1716's AXN after the operator's correction of 2026-10-29, with scripts/rederive_axns_20261027.py restricted to #1716
(the same restriction the repair of 2026-10-27 used: #3 and #4, whose AXNs already differed from their texts on main, are not touched).
  python3 rebuild/repair-btp-genre-20261029/rederive_1716.py [--apply]"""
import sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]; sys.path.insert(0, str(ROOT / "scripts"))
import rederive_axns_20261027 as R
R.ON = "2026-10-29"
R.RULED = ('Lee Sharks, 2026-10-29: "it is not a comic, parodic, or satirical ars poetica - it is a deeply serious ars poetica that contains '
           'and enacts those genres among almost every other genre, as well."')
_c = R.classify
R.classify = lambda d, hf: _c(d, hf) if d.get("deposit_number") == 1716 else None
R.WHY["text_changed"] = ("the canonical text was corrected at the author's word on 2026-10-29 (the seat 29/04 sentence that called "
                         "Belief & Technique for Telepathic Prose 'the comic ars poetica'); the AXN is re-derived from the corrected bytes")
if __name__ == "__main__":
    sys.argv += ["--sample", "1716"]
    R.main()
