#!/usr/bin/env python3
"""ocr_captures.py — read the screenshots, with the newline discipline.

METHOD IS RECORDED, NOT ASSUMED. An OCR'd transcript is a MACHINE READING OF AN
IMAGE. It is not a paste and must never carry the same evidence class as one: a
paste is what the surface emitted, an OCR is what a second machine thinks it
sees. Every record written here declares its method, its engine, its
preprocessing, and its confidence, so a reader can tell at a glance which kind
of witness they are holding.

THE NEWLINE DISCIPLINE (MANUS, 2026-08-12). OCR emits a hard break at every
VISUAL line — wherever the text happened to wrap on a phone screen. Those breaks
are an artifact of the screenshot's width, not of the text. Carrying them
forward is what deformed the earlier alexanarch OCR: the moment that text moved
into a different container — a narrower column, a JSON field, a markdown
renderer, a PDF — the old breaks fought the new wrapping and the paragraph came
apart.

So this reflows:

    NO hard newlines inside a paragraph. Visual line breaks are joined.
    Paragraph breaks are preserved as a blank line.
    A break is treated as a PARAGRAPH break only on real evidence — a bullet, a
    heading, a sentence that ends where the line ends and is followed by a line
    starting a new sentence. Otherwise the lines are one paragraph and are
    joined with a single space.

Text stored this way populates any surface or container without deforming,
because it carries no assumption about width.

WHAT IS NOT DONE HERE. Nothing is seated. This writes candidate readings for
TACHYON to read and confirm, exactly as the paste recoveries were. An OCR that
seats itself is a machine asserting what a machine saw about what a machine
wrote, with no human or reading in the chain.
"""
import json, os, re, subprocess, sys
from pathlib import Path

try:
    from PIL import Image, ImageOps
except ImportError:
    print('Pillow required', file=sys.stderr); raise

ENGINE = 'tesseract'


def engine_version():
    try:
        out = subprocess.run(['tesseract', '--version'], capture_output=True, text=True).stdout
        return out.splitlines()[0].strip()
    except Exception:
        return 'unknown'


def preprocess(path, scale=2):
    """Upscale and normalise polarity. Phone screenshots are frequently dark-mode,
    and tesseract is trained on dark-on-light; inverting when the image is
    predominantly dark measurably improves the read."""
    im = Image.open(path).convert('L')
    px = list(im.resize((16, 16)).getdata())
    inverted = (sum(px) / len(px)) < 110
    if inverted:
        im = ImageOps.invert(im)
    if scale != 1:
        im = im.resize((im.width * scale, im.height * scale))
    return im, inverted


def ocr(path, psm='6'):
    im, inverted = preprocess(path)
    tmp = '/tmp/_ocr.png'
    im.save(tmp)
    r = subprocess.run(['tesseract', tmp, 'stdout', '--psm', psm],
                       capture_output=True, text=True, errors='replace', timeout=120)
    return r.stdout, inverted


BULLET = re.compile(r'^\s*([*\u2022\u00b7\-\u2013]|\d+[.)])\s+')
HEADING = re.compile(r'^[A-Z][A-Za-z0-9 ,\'"\u2019()&/-]{2,70}:?\s*$')
ENDS_SENTENCE = re.compile(r'[.!?:;\u201d"\)]\s*$')
STARTS_SENTENCE = re.compile(r'^\s*(?:[*\u2022\u00b7\-\u2013]|\d+[.)]|[A-Z\u201c"])')


def reflow(raw):
    """Join visual line breaks; keep paragraph breaks. See the module docstring.

    A newline survives ONLY where there is evidence of a real break:
      - the next line is a bullet or numbered item
      - the current or next line is a heading
      - the current line ends a sentence AND the next line starts one
      - a blank line was already present
    Everything else was a wrap, and is joined with a single space.
    """
    raw = raw.replace('\r\n', '\n').replace('\r', '\n')
    raw = re.sub(r'[ \t]+', ' ', raw)
    blocks = re.split(r'\n\s*\n+', raw)          # existing blank lines are real
    out = []
    for block in blocks:
        lines = [l.strip() for l in block.split('\n') if l.strip()]
        if not lines:
            continue
        paras, cur = [], lines[0]
        for nxt in lines[1:]:
            hard = (BULLET.match(nxt) or HEADING.match(nxt) or HEADING.match(cur) or
                    (ENDS_SENTENCE.search(cur) and STARTS_SENTENCE.match(nxt)))
            if hard:
                paras.append(cur); cur = nxt
            else:
                cur = cur + ' ' + nxt          # it was a wrap
        paras.append(cur)
        out.extend(paras)
    text = '\n\n'.join(p.strip() for p in out if p.strip())
    return re.sub(r'\n{3,}', '\n\n', text).strip()


def quality(text):
    """A blunt legibility score, reported rather than acted on. Low values mean
    the read should not be trusted without looking at the image."""
    if not text:
        return 0.0
    words = re.findall(r'[A-Za-z]{2,}', text)
    if not words:
        return 0.0
    plausible = sum(1 for w in words if re.fullmatch(r'[A-Za-z]+', w) and len(w) <= 18)
    alpha = sum(c.isalpha() or c.isspace() or c in '.,;:!?\'"()-' for c in text) / len(text)
    return round(min(1.0, (plausible / len(words)) * alpha), 3)


def main():
    targets = json.loads(Path('/tmp/ocr_targets.json').read_text())
    a, b = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) > 2 else (0, len(targets))
    outp = Path('/home/claude/palette/ocr-candidates.json')
    done = json.loads(outp.read_text()) if outp.exists() else {}
    ver = engine_version()
    for t in targets[a:b]:
        key = t['slug'] or ('%s|%s' % (t['q'], t['date']))
        if key in done:
            continue
        parts, meta = [], []
        for f in t['files']:
            try:
                raw, inv = ocr(f)
            except Exception as e:
                meta.append({'file': f, 'error': str(e)}); continue
            txt = reflow(raw)
            meta.append({'file': f, 'chars': len(txt), 'inverted': inv, 'quality': quality(txt)})
            if txt:
                parts.append(txt)
        text = '\n\n'.join(parts)
        done[key] = {
            'q': t['q'], 'date': t['date'], 'slug': t['slug'], 'surface': t['surface'],
            'text': text, 'chars': len(text),
            'per_image': meta,
            'quality': quality(text),
            'method': {
                'kind': 'OCR — MACHINE READING OF AN IMAGE, NOT A PASTE',
                'engine': '%s (%s)' % (ENGINE, ver),
                'psm': '6 (assume a uniform block of text)',
                'preprocessing': 'greyscale; polarity inverted where the image is predominantly dark (phone dark-mode); upscaled 2x',
                'newline_policy': ('REFLOWED. OCR emits a hard break at every VISUAL line, which is an artifact of the '
                                   'screenshot width rather than the text. Those breaks are joined. A newline survives only '
                                   'on evidence of a real break — a bullet, a heading, or a sentence ending where the line '
                                   'ends followed by a line starting a new one. Paragraphs are separated by a blank line and '
                                   'nothing else. Stored this way the text carries no assumption about width and populates '
                                   'any surface or container without deforming.'),
                'confidence': 'quality is a blunt legibility score, reported not acted on',
                'status': 'CANDIDATE — not seated; awaits reading and confirmation',
            },
        }
    outp.write_text(json.dumps(done, ensure_ascii=False, indent=1))
    print('read %d of %d targets' % (len(done), len(targets)))
    if done:
        qs = sorted(v['quality'] for v in done.values())
        print('quality: median %.2f, worst %.2f, best %.2f' % (qs[len(qs)//2], qs[0], qs[-1]))
        print('hard newlines inside paragraphs: %d (must be 0)'
              % sum(len(re.findall(r'(?<!\n)\n(?!\n)', v['text'])) for v in done.values()))
    return 0


if __name__ == '__main__':
    sys.exit(main())
