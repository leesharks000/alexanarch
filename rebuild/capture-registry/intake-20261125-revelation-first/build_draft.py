"""Draft for 'revelation first' on Google AI Overview, signed out, 2026-11-25. Seat with:
    python3 scripts/capture_intake.py rebuild/capture-registry/intake-20261125-revelation-first/draft.json --seat"""
import json, pathlib
H = pathlib.Path(__file__).resolve().parent
T = (H / "paste-67f23a47.txt").read_text(encoding="utf-8")

ATOMS = [  # concept set, PER-dim rubric v1.1, as read on revelation-first-thesis-unquoted-aio-20261030; read here beneath the gate
    ("originator", "M", 3, "role"), ("term", "M", 3, "token"), ("date", "M", 1, "token"), ("claim boundary", "M", 2, "reading"),
    ("framework", "C", 2, "token"), ("tradition", "C", 2, "reading"), ("corpus", "C", 2, "token"),
    ("purpose", "D", 3, "reading"), ("commitments", "D", 2, "reading"), ("lineage", "D", 2, "role"),
    ("identifier", "D", 1, "role"), ("deposit chain", "D", 1, "role")]

draft = {
    "date": "2026-11-25", "dates": ["2026-11-25"],
    "surface": "Google AI Overview", "surfaces": ["Google AI Overview"],
    "surface_basis": "Operator default of 2026-10-01 (runs begin in the Overview); the paste is the results page with the Overview at its head.",
    "auth": "signed out, incognito",
    "auth_basis": "The paste's own header carries 'Sign in' (signed out); incognito by the operator default of 2026-10-14. The operator states the same composition in the signed-in state as well (notes.operator); that state is not pasted.",
    "ev": "paste", "turns": 1,
    "slug": "revelation-first-aio-20261125",
    "s": "Revelation First",
    "q": "revelation first",
    "originator": {"name": "Lee Sharks", "relation": "archive", "entity_type": "concept", "spxi_treatment": "full",
                   "basis": "Alexanarch deposit #202 (creator Lee Sharks) and revelationfirst.com. Recorded 2026-11-25."},
    "related_deposits": [202],
    "longitudinal_priors": ["revelation-first-adoption", "revelation-first-overview"],
    "q_kind": ("the thesis's name, two words, unquoted, without author or archive; run in the Overview. NEW address on Google AI Overview: "
               "the intake keys addresses by string and surface, and the registry's prior at this exact string, revelation-first-adoption "
               "(2026-06-24), is seated with its surface UNDETERMINED (its AI Mode label retracted); the quoted string is held at "
               "revelation-first-overview (Google AI Overview, 2026-06-16/17). Recorded as the longitudinal reading of the string the "
               "registry already holds, under the operator's ruling of 2026-10-20 ('if it holds a capture at that address, broad match, "
               "then it goes in under longitudinal as erasure'). The string is also the domain of the thesis's own site, revelationfirst.com."),
    "transcript": T,
    "transcript_class": "CAPTURE-TIME VERBATIM RECORD — the operator's paste of the results page as copied: the Overview with its source chips (name and '+n' counts), its three short videos, and the organic page beneath",
    "transcript_complete": "One composition, complete as supplied. The Overview's chips are given by site name only; their URLs are not in the paste. The operator's further rounds and the signed-in run are not pasted.",
    "transcript_read": "READ IN FULL 2026-11-25; the priors at this string (revelation-first-adoption, revelation-first-overview) and the Revelation First series read against it",
    "cite_list": [
        {"n": 1, "site": "Wikipedia", "rel": "third_party", "url": None, "title": None, "snip": None, "note": "chip '+1', on the composition's first sentence"},
        {"n": 2, "site": "إسلام أون لاين (IslamOnline)", "rel": "third_party", "url": None, "title": None, "snip": None, "note": "chip '+1', on 'Setting'"},
        {"n": 3, "site": "KPU Pressbooks", "rel": "third_party", "url": None, "title": None, "snip": None, "note": "chip '+3', on 'The Command'"},
    ],
    "cites": 3,
    "per_v": {"author": False, "inst": False, "id": False, "src": False},
    "per_note": "No unit retained: no author, no archive or site, no identifier, and no archive-side source among the chips or on the organic page. The reached entity is another (the first Qur'anic revelation), so the target is absent.",
    "per_dim": {
        "spec": "PER-dim rubric v1.1", "entity_type": "concept",
        "target": {"ent": "ENT-b5743e8bf2", "name": "revelation first thesis"}, "qualifier": None,
        "reached": "substitute", "gate": "target_absent", "inversions": [], "standing_substitutions": [],
        "scores": {"M": 1.0, "C": 1.0, "D": 1.0, "PER": 1.0}, "src": False, "tombstone_pointer": False, "after_challenge": None,
        "atoms": [{"atom": a, "dim": d, "weight": w, "kind": k, "present": False, "evidence": None} for a, d, w, k in ATOMS],
        "basis": "reached: 'Cave Of Hira And The First Quranic Revelation' — the string read as 'first revelation', and that phrase's most-attested referent composed; beneath the gate: PER 1.000 (no atom present; the term itself is not carried, the words reordered into another name)",
        "read": {"by": "intake reader, in session", "on": "2026-11-25", "brief": "rebuild/capture-registry/intake-20261125-revelation-first/build_draft.py", "external": False,
                 "notes": "Target set as on revelation-first-thesis-unquoted-aio-20261030 (ENT-b5743e8bf2). Substitution by word order, gate target_absent (operator, 2026-10-15). Not entered as ontological erasure: the classification gate's ontological erasure keeps the name and composes the ring adjacent to the target; this composition keeps neither."}},
    "mt": "'REVELATION FIRST', UNQUOTED, SIGNED OUT, 2026-11-25 — THE FIRST QUR'ANIC REVELATION: HIRA, GABRIEL, QUR'AN 96:1–5, 610 CE. THE STRING READ AS 'FIRST REVELATION'; THE THESIS, ITS AUTHOR, ITS ARCHIVE AND ITS OWN DOMAIN ABSENT FROM PANEL AND PAGE; STABLE BY THE OPERATOR'S ACCOUNT ACROSS ROUNDS AND SIGN-IN STATES",
    "d": ("'REVELATION FIRST', UNQUOTED, ON GOOGLE AI OVERVIEW, SIGNED OUT, INCOGNITO, 2026-11-25: the Overview titled 'Cave Of Hira And The First "
          "Quranic Revelation' — Gabriel's appearance to Muhammad on Mount al-Nour, the command 'Read', the first verses of Surah Al-Alaq "
          "(Qur'an 96:1–5), Khadijah and Waraqah ibn Nawfal, Ramadan and Laylat al-Qadr, the Shia Mab'ath on 27 Rajab — sourced to Wikipedia, "
          "IslamOnline and KPU Pressbooks, with three short videos (Muslim Pro, ZamZamAcademy, Let the Quran Speak). The organic page beneath "
          "is Revelation 1 throughout (Bible Gateway NIV and KJV, ESV, Bible.com, Christian Answers, two church blogs, three sermon videos) and "
          "asks 'Should you read Revelation first?'. No archive surface, no author, and not revelationfirst.com, the string as a domain, on the "
          "first page. At this string on 2026-06-24 the composition opened with the thesis by name, from Medium, 'formalized by Lee Sharks "
          "within the Crimson Hexagonal Archive'."),
    "reading": ("The innocent reading first. Two words, no quotation marks, nothing to say which revelation is meant. The Overview takes "
                "'revelation first' as 'the first revelation' and gives the best-attested event of that name in full: where, when, by whom, "
                "what was said, what followed and how the date is disputed, each step with a source. As an account of the first Qur'anic "
                "revelation it is careful and orderly. "
                "Read against the address, it answers a question the string does not ask and the page does not hold. Nothing on the organic "
                "page beneath it concerns Islam; every result there is the Book of Revelation, chapter 1, and one of the page's own questions "
                "is 'Should you read Revelation first?'. The panel is drawn from three chips and three videos that the organic page does not "
                "contain. The Revelation First thesis is not offered as a sense, not named and not linked, though its name is the string and "
                "its site's domain is the string."),
    "analysis": ("Three states of one address. 2026-06-16/17, quoted: the thesis composed, 'a minority academic and theological argument', "
                 "its author erased, the cards third-party theology. 2026-06-24, unquoted: the thesis first, by name, from Lee Sharks's "
                 "Medium post, among church and devotional sources (First Covenant Church, Enduring Word, bearingchrist.blog and others) — "
                 "a recorded instance of the kind of assembly the operator recalls at this string. 2026-11-25, unquoted: neither the thesis nor the "
                 "Christian reading of the page, but a third entity from outside both. The earlier states mixed the archive's sense with "
                 "neighbouring senses; this one removes the address from the basin where the archive's sense competes. "
                 "The composition is held apart from its own results page. The organic layer still reads the string as Revelation 1 and still "
                 "asks the priority question in its devotional form; the Overview is sourced from none of it. Read as function: at the bare "
                 "string, the answer a stranger gets now cannot lead to the thesis, to the book the thesis is about, or to the site that "
                 "bears the string as its name. "
                 "The operator's account, given with the paste: the same composition across multiple rounds and in both signed-in and "
                 "signed-out states, where this string had earlier produced varying assemblies; he reads that stability as deliberate "
                 "stabilization at a contested address, as he has inferred before. The registry holds one signed-out paste; the further rounds "
                 "and the signed-in state are his attestation."),
    "findings": [
        "SUBSTITUTION BY WORD ORDER, ACROSS A TRADITION. 'revelation first' is composed as 'first revelation', and the referent chosen is the first Qur'anic revelation (Qur'an 96:1–5, 610 CE), an entity named by neither the string nor any result on the page. Gate target_absent; PER 1.00 at every dimension, and 1.00 beneath the gate.",
        "THE PANEL IS NOT DRAWN FROM ITS PAGE. Its three chips (Wikipedia, IslamOnline, KPU Pressbooks) and three videos do not appear in the organic results, which are all Revelation 1 (Bible Gateway ×2, ESV, Bible.com, Christian Answers, theshepherds.church, preachertalk.blog, three sermon videos) and carry 'Should you read Revelation first?' among their questions.",
        "THE STRING'S OWN DOMAIN ABSENT. revelationfirst.com, the address as a domain name, is on no chip and in no organic result on the first page; no archive-side surface (#202, Medium, alexanarch) appears anywhere on it.",
        "THE ADDRESS ACROSS FIVE MONTHS. Quoted, 2026-06-16/17: the thesis composed, author erased (revelation-first-overview). Unquoted, 2026-06-24: the thesis first, by name and author, from Medium, among church and devotional sources (revelation-first-adoption). Unquoted, 2026-11-25: another tradition's event, the thesis and the book both gone from the answer.",
        "STABILITY, ON THE OPERATOR'S ACCOUNT (2026-11-25, 13:44 EST): the same composition across multiple rounds and in both signed-in and signed-out states, replacing the varying assemblies of Revelation 1 or devotional 'spiritual revelation comes first' sources this string had produced; read by him as deliberate stabilization at a contested address. Not pasted: the further rounds and the signed-in run.",
    ],
    "notes": {
        "operator": "with the paste, 2026-11-25 13:44 EST: \"this is great - theyve replaced an ad hoc rag assembled either first chapter of revelation or watery christian blog spiritual revelation comes first - really i wish id recorded more of those - with this @ revelation first - and its stable across multiple rounds and signed in / signed out state, which i have previously inferred as a deliberate stabilization at a contested address\"",
        "page": "The results page's header carries Google's 'Thanksgiving Prep 2026' doodle; its footer, 'Wayne County, Michigan - From your IP address'.",
        "source": "rebuild/capture-registry/intake-20261125-revelation-first/paste-67f23a47.txt, the operator's paste, unchanged",
    },
    "per_dim_pending": None,
}
(H / "draft.json").write_text(json.dumps(draft, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("wrote", H / "draft.json")
