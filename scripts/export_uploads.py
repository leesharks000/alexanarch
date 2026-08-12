#!/usr/bin/env python3
"""export_uploads.py — recover everything MANUS put INTO the conversations.

The companion to export_generated_files.py. That script recovered what was
written during sessions; this recovers what was brought to them.

TWO KINDS, and the distinction matters:

  NAMED UPLOADS (52) — attachments carrying a real filename and type: .md, .json,
  .txt, .html, .docx. These are files that existed before the conversation.

  PASTED BLOCKS (4,074) — attachments with file_type 'txt' and NO filename. When
  a long block is pasted into the chat it arrives this way. This is where the
  external creative work lives: poems, essays and manuscripts composed elsewhere
  and brought in, alongside Assembly Chorus responses from other substrates,
  blog posts, and correspondence.

61.8 MB in total — larger than the generated corpus.

CLASSIFICATION IS A GUESS AND IS LABELLED AS ONE. Pasted blocks are sorted into
likely kinds by their opening lines: a title heading, an Assembly-review
register, machine-transcript signatures, correspondence. The guess goes in a
manifest field named `provisional_kind` and never in a filename, because a
filename is read as a fact and this is not one. MANUS sorts at leisure; the
script's job is to recover and record, not to decide.

PRIVACY. This corpus is more personal than the generated files: correspondence,
health, relationships, and third-party creative work by named collaborators.
Nothing here is published anywhere by this script. It writes to a local
directory for MANUS to review. Credentials are redacted before any write.
"""
import argparse, json, re, sys, zipfile
from pathlib import Path

CREDENTIALS = [
    ('GITHUB_PAT',   re.compile(r'github_pat_[A-Za-z0-9_]{20,}')),
    ('GITHUB_TOKEN', re.compile(r'gh[opusr]_[A-Za-z0-9]{20,}')),
    ('LONG_TOKEN',   re.compile(r'\b[A-Za-z0-9]{60}\b')),
    ('BEARER',       re.compile(r'(?i)bearer\s+[A-Za-z0-9._\-]{24,}')),
    ('AWS_KEY',      re.compile(r'AKIA[0-9A-Z]{16}')),
    ('SLACK',        re.compile(r'xox[abprs]-[A-Za-z0-9-]{10,}')),
    ('OPENAI',       re.compile(r'sk-[A-Za-z0-9]{32,}')),
    ('ANTHROPIC',    re.compile(r'sk-ant-[A-Za-z0-9_\-]{20,}')),
]
REDACTED = {}


def redact(text):
    for name, pat in CREDENTIALS:
        def rep(m):
            REDACTED[name] = REDACTED.get(name, 0) + 1
            return '[REDACTED-%s-%dchars]' % (name, len(m.group(0)))
        text = pat.sub(rep, text)
    return text


# Ordered: the first match wins, so the most specific signatures come first.
KINDS = [
    ('machine_transcript', re.compile(
        r'AI can make mistakes|^\s*You said:|AI Mode Conversation|AI Overview', re.M)),
    ('assembly_response', re.compile(
        r'^\s*#{0,3}\s*(Overall Assessment|Verdict|Assessment|Review)\b|'
        r'\b(ChatGPT|Gemini|DeepSeek|Kimi|Grok|Muse Spark)\b.{0,40}\b(says|response|review)\b', re.I | re.M)),
    ('titled_work', re.compile(r'^\s*#\s+\S')),          # opens with a markdown H1
    ('front_matter', re.compile(r'^\s*---\s*\n\s*\w+:')),  # YAML header
    ('correspondence', re.compile(
        r'^\s*(Dear\b|Hi\b|Hello\b)|\bSincerely\b|\bBest regards\b|\bkind regards\b', re.I | re.M)),
    ('verse', re.compile(r'\A(?:[^\n]{0,70}\n){6,}\Z')),   # many short lines, no long prose
]


def classify(text):
    head = text[:1500]
    for name, pat in KINDS:
        if pat.search(head):
            return name
    return 'unclassified'


def safe(s, limit=70):
    s = re.sub(r'[^A-Za-z0-9._-]+', '-', (s or '').strip())
    return (re.sub(r'-{2,}', '-', s).strip('-.')[:limit] or 'untitled')


def title_of(text):
    """A human-legible hint from the content, for the manifest only."""
    for line in text.split('\n')[:12]:
        s = line.strip().lstrip('#').strip()
        if 8 <= len(s) <= 90 and not s.startswith(('```', '|', '<')):
            return s
    return ''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--zip', default='/home/claude/export.zip')
    ap.add_argument('--out', default='/home/claude/uploads-corpus')
    ap.add_argument('--min-chars', type=int, default=400)
    a = ap.parse_args()
    try:
        import ijson
    except ImportError:
        print('ijson required', file=sys.stderr)
        return 2

    out = Path(a.out)
    (out / 'named-uploads').mkdir(parents=True, exist_ok=True)
    (out / 'pasted').mkdir(parents=True, exist_ok=True)
    manifest, seen = [], {}
    n = skipped = 0

    z = zipfile.ZipFile(a.zip)
    with z.open('conversations.json') as f:
        for conv in ijson.items(f, 'item'):
            cname = conv.get('name') or 'untitled'
            cdate = (conv.get('created_at') or '')[:10]
            for mi, m in enumerate(conv.get('chat_messages') or []):
                if m.get('sender') != 'human':
                    continue
                for ai, att in enumerate(m.get('attachments') or []):
                    text = att.get('extracted_content') or ''
                    if len(text) < a.min_chars:
                        skipped += 1
                        continue
                    text = redact(text)
                    fn = att.get('file_name') or ''
                    named = bool(fn)
                    kind = 'named_upload' if named else classify(text)
                    sub = 'named-uploads' if named else 'pasted'
                    stem = safe(fn.rsplit('.', 1)[0]) if named else safe(title_of(text) or 'paste')
                    ext = ('.' + fn.rsplit('.', 1)[-1]) if named and '.' in fn else '.txt'
                    d = out / sub / ('%s_%s' % (cdate, safe(cname, 44)))
                    d.mkdir(parents=True, exist_ok=True)
                    key = (str(d), stem)
                    seen[key] = seen.get(key, 0) + 1
                    name = '%s%s' % (stem, ext) if seen[key] == 1 else '%s-%d%s' % (stem, seen[key], ext)
                    (d / name).write_text(text, encoding='utf-8')
                    n += 1
                    manifest.append({
                        'written_to': str((d / name).relative_to(out)),
                        'provisional_kind': kind,
                        'kind_is_a_guess': not named,
                        'original_file_name': fn or None,
                        'file_type': att.get('file_type'),
                        'declared_size': att.get('file_size'),
                        'chars': len(text),
                        'title_hint': title_of(text),
                        'conversation': cname,
                        'conversation_uuid': conv.get('uuid'),
                        'message_uuid': m.get('uuid'),
                        'message_created': m.get('created_at'),
                        'message_index': mi,
                        'attachment_index': ai,
                    })

    (out / 'MANIFEST.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=1),
                                       encoding='utf-8')
    import collections
    print('written        : %d  (%.1f MB)' % (n, sum(x['chars'] for x in manifest) / 1e6))
    print('skipped (<%d ch): %d' % (a.min_chars, skipped))
    print('named uploads  : %d' % sum(1 for x in manifest if not x['kind_is_a_guess']))
    print('pasted blocks  : %d' % sum(1 for x in manifest if x['kind_is_a_guess']))
    print('provisional kinds:', dict(collections.Counter(x['provisional_kind'] for x in manifest)))
    print('credentials    :', REDACTED or 'none found')
    return 0


if __name__ == '__main__':
    sys.exit(main())
