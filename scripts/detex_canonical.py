#!/usr/bin/env python3
"""detex_canonical.py — plain-text mathematical notation in canonical deposit text.

THE DEFECT THIS CLOSES
Deposits #1452-#1454 were seated with the LaTeX their source manuscripts carry:
21-27 display environments and 26-36 inline spans each. A PDF build renders that
correctly. The FULL-TEXT DISPLAY does not: the record page, the wiki article, the
body index, the OAI dissemination, and every machine reading the text see raw
backslash macros. A reader of the record encounters

    \\[ X_0 \\xrightarrow{T_1} X_1 \\xrightarrow{T_2} \\cdots \\]

where the paper says: an acquisition chain X_0 -> X_1 -> ... under transforms.
The bytes are correct and the presentation is unreadable — the same class as the
capture-gallery escaped-emphasis defect and the record-page renderer repairs.

THE RULE (ratified 2026-08-12, MANUS):
  Canonical deposit text uses PLAIN-TEXT mathematical notation. LaTeX is fine in
  a PDF, where it renders; it is not fine in the canonical body, which is what
  the record page, the harvesters, and the composition layer actually read.
  validate_deposit.py enforces this going forward (MATH-001).

WHAT THIS DOES
  Converts the LaTeX constructs actually present in the corpus to plain text:
  display and inline delimiters, subscripts and superscripts, common macros,
  set and relation symbols, arrows, and spacing commands. Display environments
  become indented plain-text lines so they still read as displayed equations.
  Unicode is used only where it is unambiguous and widely supported (times,
  arrows, Greek, set membership); everything else degrades to ASCII.

  It is conservative by construction: anything it does not recognize is left
  alone and reported, so an unrecognized macro is visible rather than silently
  mangled.

USAGE
  python3 scripts/detex_canonical.py --check            # report only
  python3 scripts/detex_canonical.py --deposits 1452,1453,1454 --apply
"""
import argparse, json, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
REG = ROOT / 'data' / 'registry.json'

# ordered: longest / most specific first
MACROS = [
    (r'\\boxed\{', ''),
    (r'\\begin\{[a-z*]+\}', ''),
    (r'\\end\{[a-z*]+\}', ''),
    (r'\\widehat\s*', 'est. '),
    (r'\\mathbf\s+1', 'indicator'),
    (r'\\mathbf\{([^{}]*)\}', r'\1'),
    (r'\\mathbf\s*', ''),
    (r'\\mathcal\s+([A-Za-z])', r'\1'),
    (r'\\getau', ' >= tau'),
    (r'\\simBernoulli', ' ~ Bernoulli'),
    (r'\\inR', ' in R'),
    (r'\\succ', ' > '),
    (r'\\xrightarrow\{([^{}]*)\}', r' --[\1]--> '),
    (r'\\xleftarrow\{([^{}]*)\}', r' <--[\1]-- '),
    (r'\\mathrm\{([^{}]*)\}', r'\1'),
    (r'\\mathbb\{([^{}]*)\}', r'\1'),
    (r'\\mathcal\{([^{}]*)\}', r'\1'),
    (r'\\mathfrak\{([^{}]*)\}', r'\1'),
    (r'\\operatorname\{([^{}]*)\}', r'\1'),
    (r'\\text(?:rm|it|bf|sf|tt)?\{([^{}]*)\}', r'\1'),
    (r'\\frac\{([^{}]*)\}\{([^{}]*)\}', r'(\1)/(\2)'),
    (r'\\sqrt\{([^{}]*)\}', r'sqrt(\1)'),
    (r'\\hat\{([^{}]*)\}', r'\1-hat'),
    (r'\\bar\{([^{}]*)\}', r'\1-bar'),
    (r'\\tilde\{([^{}]*)\}', r'\1-tilde'),
    (r'\\left', ''), (r'\\right', ''),
    (r'\\,', ' '), (r'\\;', ' '), (r'\\!', ''), (r'\\quad', '   '), (r'\\qquad', '      '),
    (r'\\\\', '\n'),
]
SYMBOLS = {
    r'\\times': '×', r'\\cdot': '·', r'\\cdots': '...', r'\\dots': '...', r'\\ldots': '...',
    r'\\leq': '<=', r'\\geq': '>=', r'\\neq': '!=', r'\\approx': '≈', r'\\sim': '~',
    r'\\equiv': '=', r'\\propto': '∝', r'\\pm': '±', r'\\ll': '<<', r'\\gg': '>>',
    r'\\in': '∈', r'\\notin': '∉', r'\\subset': '⊂', r'\\subseteq': '⊆',
    r'\\cap': '∩', r'\\cup': '∪', r'\\emptyset': '{}', r'\\setminus': '\\',
    r'\\rightarrow': '->', r'\\to': '->', r'\\leftarrow': '<-', r'\\Rightarrow': '=>',
    r'\\mapsto': '|->', r'\\longrightarrow': '-->', r'\\implies': '=>',
    r'\\forall': 'for all ', r'\\exists': 'there exists ', r'\\land': ' and ', r'\\lor': ' or ',
    r'\\neg': 'not ', r'\\infty': 'infinity', r'\\partial': 'd', r'\\nabla': 'grad',
    r'\\sum': 'sum', r'\\prod': 'product', r'\\int': 'integral', r'\\max': 'max', r'\\min': 'min',
    r'\\log': 'log', r'\\exp': 'exp', r'\\Pr': 'P', r'\\mid': '|',
    r'\\alpha': 'alpha', r'\\beta': 'beta', r'\\gamma': 'gamma', r'\\delta': 'delta',
    r'\\Delta': 'Delta', r'\\epsilon': 'epsilon', r'\\varepsilon': 'epsilon',
    r'\\theta': 'theta', r'\\lambda': 'lambda', r'\\mu': 'mu', r'\\nu': 'nu',
    r'\\pi': 'pi', r'\\rho': 'rho', r'\\sigma': 'sigma', r'\\Sigma': 'Sigma',
    r'\\tau': 'tau', r'\\phi': 'phi', r'\\varphi': 'phi', r'\\Phi': 'Phi',
    r'\\chi': 'chi', r'\\psi': 'psi', r'\\Psi': 'Psi', r'\\omega': 'omega', r'\\Omega': 'Omega',
    r'\\mathfrak I': 'I', r'\\ast': '*', r'\\star': '*', r'\\circ': 'o',
}


def _inner(s, _passes=2):
    """Convert the contents of a math span to plain text.

    Two passes: stripping a wrapper macro can expose a new literal beneath it
    (\\sim\\operatorname{Bernoulli} becomes \\simBernoulli after the first pass),
    so the substitution set is applied again over its own output.
    """
    for _ in range(_passes):
        s = _one_pass(s)
    return s


def _one_pass(s):
    for entry in MACROS:
        if len(entry) == 3:
            s = re.sub(entry[0], entry[1], s, flags=entry[2])
        else:
            s = re.sub(entry[0], entry[1], s)
    for pat, rep in sorted(SYMBOLS.items(), key=lambda kv: -len(kv[0])):
        s = re.sub(pat + r'(?![A-Za-z])', rep.replace('\\', '\\\\'), s)
    # subscripts / superscripts: X_{i-1} -> X_(i-1); X^{*} -> X*
    s = re.sub(r'\^\{\\?\*\}', '*', s)
    s = re.sub(r'\^\{([^{}]*)\}', r'^(\1)', s)
    s = re.sub(r'_\{([^{}]*)\}', r'_(\1)', s)
    s = re.sub(r'\^\\ast', '*', s)
    s = s.replace('\\{', '{').replace('\\}', '}').replace('\\%', '%').replace('\\&', '&')
    s = re.sub(r'[ \t]+', ' ', s)
    return s.strip()


def detex(text):
    """Return (converted_text, list_of_unrecognized_macros)."""
    def disp(m):
        body = _inner(m.group(1))
        lines = [l.strip() for l in body.split('\n') if l.strip()]
        return '\n\n' + '\n'.join('    ' + l for l in lines) + '\n'
    out = re.sub(r'\\\[(.*?)\\\]', disp, text, flags=re.S)
    out = re.sub(r'\$\$(.*?)\$\$', disp, out, flags=re.S)
    out = re.sub(r'\\\((.*?)\\\)', lambda m: _inner(m.group(1)), out, flags=re.S)
    out = re.sub(r'(?<!\$)\$(?!\$)([^$\n]{1,200}?)(?<!\$)\$(?!\$)', lambda m: _inner(m.group(1)), out)
    left = sorted(set(re.findall(r'\\[A-Za-z]+', out)))
    out = re.sub(r'\n{3,}', '\n\n', out)
    return out, left


def scan(text):
    """Count LaTeX constructs remaining in a body (the validation measure)."""
    return {
        'display': len(re.findall(r'\\\[', text)) + len(re.findall(r'\$\$', text)) // 2,
        'inline': len(re.findall(r'\\\(', text)),
        'macros': len(set(re.findall(r'\\[A-Za-z]+', text))),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--deposits', help='comma-separated deposit numbers')
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--check', action='store_true')
    a = ap.parse_args()
    reg = json.loads(REG.read_text())
    D = {d['deposit_number']: d for d in reg['deposits']}
    nums = [int(x) for x in a.deposits.split(',')] if a.deposits else sorted(D)
    hits = 0
    for n in nums:
        d = D.get(n)
        if not d:
            continue
        p = ROOT / 'data' / 'texts' / ('AXN-%s-text.md' % d['hex'])
        if not p.exists():
            continue
        t = p.read_text(encoding='utf-8')
        before = scan(t)
        if before['display'] == 0 and before['inline'] == 0:
            continue
        hits += 1
        out, left = detex(t)
        after = scan(out)
        print('#%d %s  display %d->%d  inline %d->%d  residual macros: %s'
              % (n, d['hex'], before['display'], after['display'],
                 before['inline'], after['inline'], ', '.join(left[:8]) or 'none'))
        if a.apply:
            p.write_text(out, encoding='utf-8')
            (ROOT / 'data' / 'deposits' / ('AXN-%s.md' % d['hex'])).write_text(out, encoding='utf-8')
    if not hits:
        print('no deposit bodies carry LaTeX math delimiters')
    return 0


if __name__ == '__main__':
    sys.exit(main())
