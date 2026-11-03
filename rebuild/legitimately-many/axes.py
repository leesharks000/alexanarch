#!/usr/bin/env python3
"""Legitimately Many — the second coding of the locus table (2026-11-02, after the third review). The first coding (code_attr,
code_count in loci.py) put a kind of change and a kind of justification on one scale: "argues for" sat beside "revises", so a
reader who revised an attribution by arguing for it had to be given one or the other, and "count" took in three different
things. The second coding separates three questions for each locus and keeps the first coding beside it, unaltered.

  object   — what the count at this locus is a count of:
             composing     the historical persons who composed the writings
             speakers      the dramatic speakers, and who owns their movement
             contributors  contributors to an edited work, a library or a school
             names         what a name counts (kinds under names, shapes under a name)
  position — the position the locus takes, on the attribution and on the count:
             does_not_address, presupposes, affirms (states it, with or without ground), considers_excludes (names an
             alternative and sets it aside), holds_open, revises
  warrant  — what the locus offers for its position:
             none          no ground on the page
             report        another's word (φασίν, "said to", a cited authority)
             argument      reasons given on the page (style, cross-reference, system, philosophy)
             instrument    a will, catalogue, succession, title or record
             consensus     what the many or the school hold
             person        the alternative is assigned to a named person, and that assignment is the reason given

A position with no stance has the warrant none. The coding is the session's reading; the operator rules.
Each entry: (attribution position, attribution warrant, count object, count position, count warrant)."""

AX = {
 "L01": ("revises", "none", "composing", "revises", "none"),
 "L02": ("presupposes", "none", "composing", "presupposes", "none"),
 "L03": ("does_not_address", "none", "composing", "does_not_address", "none"),
 "L04": ("does_not_address", "none", "contributors", "does_not_address", "none"),
 "L05": ("does_not_address", "none", "contributors", "does_not_address", "none"),
 "L06": ("presupposes", "none", "contributors", "presupposes", "none"),
 "L07": ("presupposes", "none", "contributors", "presupposes", "none"),
 "L08": ("presupposes", "none", "contributors", "presupposes", "none"),
 "L09": ("holds_open", "instrument", "composing", "does_not_address", "none"),
 "L10": ("considers_excludes", "instrument", "composing", "presupposes", "none"),
 "L11": ("presupposes", "none", "composing", "presupposes", "none"),
 "L12": ("presupposes", "instrument", "composing", "presupposes", "instrument"),
 "L13": ("presupposes", "none", "contributors", "presupposes", "none"),
 "L14": ("presupposes", "none", "contributors", "presupposes", "none"),
 "L15": ("presupposes", "none", "contributors", "presupposes", "none"),
 "L16": ("does_not_address", "none", "composing", "does_not_address", "none"),
 "L17": ("affirms", "argument", "speakers", "considers_excludes", "argument"),
 "L18": ("affirms", "argument", "speakers", "considers_excludes", "argument"),
 "L19": ("presupposes", "none", "speakers", "does_not_address", "none"),
 "L20": ("does_not_address", "none", "composing", "does_not_address", "none"),
 "L21": ("considers_excludes", "argument", "composing", "does_not_address", "none"),
 "L22": ("considers_excludes", "argument", "composing", "does_not_address", "none"),
 "L23": ("affirms", "argument", "composing", "considers_excludes", "argument"),
 "L24": ("considers_excludes", "argument", "composing", "considers_excludes", "argument"),
 "L25": ("presupposes", "instrument", "composing", "presupposes", "instrument"),
 "L26": ("considers_excludes", "argument", "composing", "considers_excludes", "argument"),
 "L27": ("affirms", "argument", "composing", "considers_excludes", "argument"),
 "L28": ("does_not_address", "none", "composing", "does_not_address", "none"),
 "L29": ("does_not_address", "none", "composing", "does_not_address", "none"),
 "L30": ("presupposes", "none", "composing", "does_not_address", "none"),
 "L31": ("considers_excludes", "argument", "composing", "does_not_address", "none"),
 "L32": ("affirms", "argument", "composing", "does_not_address", "none"),
 "L33": ("holds_open", "report", "composing", "does_not_address", "none"),
 "L34": ("presupposes", "report", "composing", "presupposes", "report"),
 "L35": ("presupposes", "none", "composing", "does_not_address", "none"),
 "L36": ("presupposes", "report", "composing", "presupposes", "report"),
 "L37": ("presupposes", "report", "composing", "presupposes", "report"),
 "L38": ("affirms", "argument", "composing", "presupposes", "none"),
 "L39": ("affirms", "argument", "composing", "presupposes", "none"),
 "L40": ("does_not_address", "none", "composing", "does_not_address", "none"),
 "L41": ("considers_excludes", "argument", "composing", "presupposes", "none"),
 "L42": ("does_not_address", "none", "composing", "does_not_address", "none"),
 "L43": ("does_not_address", "none", "composing", "does_not_address", "none"),
 "L44": ("does_not_address", "none", "composing", "does_not_address", "none"),
 "L45": ("does_not_address", "none", "composing", "does_not_address", "none"),
 "L46": ("presupposes", "none", "composing", "does_not_address", "none"),
 "L47": ("considers_excludes", "instrument", "composing", "does_not_address", "none"),
 "L48": ("affirms", "report", "composing", "presupposes", "none"),
 "L49": ("does_not_address", "none", "composing", "does_not_address", "none"),
 "L50": ("presupposes", "none", "contributors", "holds_open", "none"),
 "L51": ("presupposes", "none", "contributors", "presupposes", "none"),
 "L52": ("does_not_address", "none", "contributors", "does_not_address", "none"),
 "L53": ("presupposes", "none", "contributors", "does_not_address", "none"),
 "L54": ("presupposes", "none", "contributors", "presupposes", "none"),
 "L55": ("presupposes", "none", "contributors", "presupposes", "none"),
 "L56": ("presupposes", "none", "contributors", "presupposes", "none"),
 "L57": ("affirms", "report", "composing", "presupposes", "none"),
 "L58": ("does_not_address", "none", "composing", "does_not_address", "none"),
 "L59": ("revises", "argument", "composing", "presupposes", "none"),
 "L60": ("presupposes", "none", "composing", "presupposes", "none"),
 "L61": ("presupposes", "none", "composing", "presupposes", "none"),
 "L62": ("considers_excludes", "argument", "composing", "does_not_address", "none"),
 "L63": ("revises", "argument", "composing", "does_not_address", "none"),
 "L64": ("affirms", "argument", "speakers", "revises", "argument"),
 "L65": ("affirms", "argument", "speakers", "revises", "argument"),
 "L66": ("affirms", "argument", "speakers", "revises", "argument"),
 "L67": ("considers_excludes", "argument", "speakers", "considers_excludes", "argument"),
 "L68": ("presupposes", "report", "composing", "presupposes", "report"),
 "L69": ("presupposes", "argument", "composing", "presupposes", "argument"),
 "L70": ("does_not_address", "none", "composing", "does_not_address", "none"),
 "L71": ("revises", "argument", "contributors", "revises", "argument"),
 "L72": ("presupposes", "report", "composing", "presupposes", "report"),
 "L73": ("revises", "argument", "composing", "presupposes", "none"),
 "L74": ("presupposes", "report", "composing", "presupposes", "report"),
 "L75": ("holds_open", "argument", "contributors", "holds_open", "argument"),
 "L76": ("considers_excludes", "argument", "contributors", "revises", "argument"),
 "L77": ("does_not_address", "none", "composing", "presupposes", "report"),
 "L78": ("presupposes", "instrument", "contributors", "presupposes", "instrument"),
 "L79": ("holds_open", "none", "composing", "presupposes", "none"),
 "L80": ("holds_open", "none", "composing", "holds_open", "none"),
 "L81": ("presupposes", "consensus", "contributors", "does_not_address", "none"),
 "L82": ("does_not_address", "none", "names", "holds_open", "none"),
 "L83": ("presupposes", "report", "composing", "presupposes", "report"),
 "L84": ("presupposes", "report", "composing", "presupposes", "report"),
 "L85": ("presupposes", "instrument", "composing", "presupposes", "instrument"),
 "L86": ("does_not_address", "none", "contributors", "holds_open", "instrument"),
 "L87": ("does_not_address", "none", "composing", "presupposes", "report"),
 "L88": ("holds_open", "instrument", "composing", "holds_open", "instrument"),
 "L89": ("revises", "instrument", "composing", "presupposes", "none"),
 "L90": ("presupposes", "argument", "composing", "presupposes", "none"),
 "L91": ("presupposes", "argument", "contributors", "presupposes", "argument"),
 "L92": ("does_not_address", "none", "contributors", "presupposes", "none"),
 "L93": ("considers_excludes", "instrument", "composing", "presupposes", "none"),
 "L94": ("presupposes", "none", "contributors", "holds_open", "none"),
 "L95": ("considers_excludes", "argument", "composing", "considers_excludes", "argument"),
 "L96": ("does_not_address", "none", "composing", "does_not_address", "none"),
 "L97": ("holds_open", "argument", "names", "does_not_address", "none"),
 "L98": ("presupposes", "none", "composing", "presupposes", "none"),
 "L99": ("presupposes", "none", "composing", "presupposes", "none"),
 "L100": ("presupposes", "none", "composing", "presupposes", "none"),
 "L101": ("presupposes", "none", "composing", "presupposes", "none"),
 "L102": ("affirms", "instrument", "composing", "affirms", "instrument"),
 "L103": ("affirms", "instrument", "composing", "affirms", "instrument"),
 "L104": ("considers_excludes", "person", "composing", "considers_excludes", "person"),
 "L105": ("revises", "argument", "composing", "revises", "argument"),
 "L106": ("presupposes", "none", "composing", "presupposes", "none"),
 "L107": ("does_not_address", "none", "composing", "presupposes", "none"),
 "L108": ("does_not_address", "none", "composing", "presupposes", "none"),
 "L109": ("does_not_address", "none", "composing", "presupposes", "instrument"),
 "L110": ("does_not_address", "none", "composing", "presupposes", "none"),
 "L111": ("does_not_address", "none", "composing", "presupposes", "instrument"),
 "L112": ("presupposes", "none", "composing", "presupposes", "none"),
}
OBJECTS = ["composing", "speakers", "contributors", "names"]
POSITIONS = ["does_not_address", "presupposes", "affirms", "considers_excludes", "holds_open", "revises"]
WARRANTS = ["none", "report", "argument", "instrument", "consensus", "person"]
