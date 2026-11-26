#!/usr/bin/env python3
"""A seventh slot (a reviewer, on v0.17, section 4): MODALITY, the standing of the deed: DONE, PREDICTED, PROMISED, REQUIRED, PERMITTED, PROHIBITED, ASKED.
Entered for the pairs of the Revelation 20 cluster and the loci of 2P; the forty and thirty-seven earlier pairs are owed. Three axes kept apart:
ROLE (who is agent and who is object: exchanged or not), ACTION (kept, changed, or opposed by the table of 2P.5), MODALITY (kept or changed).
   python3 modal.py out.json"""
import json, sys
P = [  # name, role, action, modality in Revelation, modality in the Gospel
("the sealing (Matt 27:66)", "exchanged: the sealer passes from the angel to the adversaries, the sealed from the adversary to Jesus", "kept", "DONE", "DONE"),
("at the closure (Matt 28:2)", "kept: the angel", "opposed: shut / roll away", "DONE", "DONE"),
("the deceiving (Matt 27:64)", "exchanged: the deceiver passes from the dragon to the disciples", "kept", "PROHIBITED (ἵνα μὴ πλανήσῃ)", "PROHIBITED (μήποτε …)"),
("bound by Satan (Luke 13:16)", "exchanged: Satan passes from bound to binder", "kept", "DONE", "DONE"),
("must be loosed (Luke 13:16)", "the one loosed passes from the adversary to a daughter of Abraham", "kept", "REQUIRED (δεῖ)", "REQUIRED (ἔδει)"),
("into the abyss (Luke 8:31)", "kept: the adversary is the one sent", "kept in sense (cast / command to go)", "DONE", "ASKED NOT (παρεκάλουν ἵνα μή)"),
("authority (Luke 19:17)", "exchanged in side: the ten kings / the good slave", "changed", "PERMITTED for one hour", "PERMITTED as reward"),
("seated (Mark 14:62)", "kept: the son of man", "kept", "DONE (seen)", "PREDICTED (ὄψεσθε)"),
("to buy (Luke 22:36)", "agent passes from anyone to the one who has not", "kept", "PROHIBITED (ἵνα μή τις δύνηται)", "REQUIRED (ἀγορασάτω)"),
("the tomb (Mark 15:46)", "the one who acts passes from the peoples to a friend", "kept", "PROHIBITED (οὐκ ἀφίουσιν)", "DONE"),
("after three days (Matt 27:63)", "the two / the one", "changed (stand / be raised)", "DONE", "PROMISED, as reported by adversaries"),
("the prepared place (John 14:2)", "God / the Christ; the woman / you", "kept", "DONE", "PROMISED"),
]
base = lambda m: m.split(" ")[0] + (" NOT" if " NOT" in m else "")
rows = [dict(name=n, role=r, action=a, rev=x, gospel=y, modality="kept" if base(x) == base(y) else f"{base(x)} → {base(y)}") for n, r, a, x, y in P]
for r in rows: print(f"{r['name']:32} | modality {r['modality']}")
print("modality kept:", sum(1 for r in rows if r["modality"] == "kept"), "of", len(rows)); json.dump(rows, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
