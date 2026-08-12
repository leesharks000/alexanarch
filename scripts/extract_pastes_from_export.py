#!/usr/bin/env python3
"""extract_pastes_from_export.py — recover capture transcripts from the export.

WHY. conversation_search returns ONE semantically-ranked chunk per thread, with
no role filter, no date filter and no literal matching. For a corpus where the
author has written extensively about every term he also captured, the paste can
never outrank the surrounding discussion — 242 captures were unreachable by
search for that structural reason. The export removes the problem entirely:
literal matching does not care how common a term is.

WHAT IT DOES. Streams conversations.json out of the zip (888 MB uncompressed;
never written to disk), walks every conversation and every message, and keeps
only HUMAN turns that carry a capture-paste signature. Assistant turns are
skipped: a paste is something MANUS supplied, and text the assistant produced
about a capture is analysis, not evidence — the distinction whose collapse
destroyed the withdrawn registry.

PRIVACY. The export contains every conversation, most of it personal and none
of it the archive's business. This script writes out ONLY messages matching a
capture-paste signature, and records nothing else — no summaries, no adjacent
turns, no conversation bodies. Personal material is not read, not indexed and
not carried anywhere.

ALSO COLLECTED. Per-message `files` and `attachments` entries, so image
references offered in-thread can be checked against what actually reached the
live archive — MANUS reports capture shots that never landed.
"""
import json, re, sys, zipfile
from pathlib import Path

ZIP = Path('/home/claude/export.zip')
OUT = Path('/home/claude/palette/export-pastes.json')
FILES_OUT = Path('/home/claude/palette/export-file-refs.json')

# A paste signature, not a topic match. Each of these is a literal artifact of
# copying from a machine surface, and none of them occurs in ordinary prose.
SIGNATURES = [
    ('footer',           re.compile(r'AI can make mistakes')),
    ('you_said',         re.compile(r'You said:')),
    ('ai_mode_conv',     re.compile(r'AI Mode Conversation')),
    ('sources_shown',    re.compile(r'Sources shown:')),
    ('full_transcript',  re.compile(r'[Ff]ull AI (?:Mode|Overview)? ?transcript')),
    ('ai_overview_lead', re.compile(r'^\s*AI Overview\b', re.M)),
]
MIN_LEN = 200  # a paste is a body of text, not a mention

# CREDENTIAL REDACTION — mandatory, not optional.
#
# 2026-08-12: the first run of this extractor carried a GitHub Personal Access
# Token out of a thread and into the rebuild. GitHub's push protection caught it
# at the remote; nothing was published. But the lesson is structural, not lucky:
# an export of every conversation contains every credential ever pasted into
# one, and any extractor that copies message text verbatim will carry them.
#
# The archive's standing rule is that private material never enters a deposit or
# any public record, and is redacted on sight. A credential is the sharpest case
# of that rule, so redaction happens HERE, at extraction, before the text is
# written anywhere — not as a cleanup pass that can be forgotten.
CREDENTIALS = [
    ('GITHUB_PAT', re.compile(r'github_pat_[A-Za-z0-9_]{20,}')),
    ('GITHUB_TOKEN', re.compile(r'gh[opusr]_[A-Za-z0-9]{20,}')),
    ('LONG_TOKEN', re.compile(r'\b[A-Za-z0-9]{60}\b')),   # Zenodo-style
    ('BEARER', re.compile(r'(?i)bearer\s+[A-Za-z0-9._\-]{24,}')),
    ('AWS_KEY', re.compile(r'AKIA[0-9A-Z]{16}')),
    ('SLACK', re.compile(r'xox[abprs]-[A-Za-z0-9-]{10,}')),
    ('OPENAI', re.compile(r'sk-[A-Za-z0-9]{32,}')),
]
REDACTED = {}


def redact(text):
    """Replace any credential with a marker recording its class and length."""
    for name, pat in CREDENTIALS:
        def rep(m):
            REDACTED[name] = REDACTED.get(name, 0) + 1
            return '[REDACTED-%s-%dchars]' % (name, len(m.group(0)))
        text = pat.sub(rep, text)
    return text


def message_text(m):
    """Prefer the content blocks; fall back to the flat text field."""
    parts = []
    for c in (m.get('content') or []):
        if c.get('type') == 'text' and c.get('text'):
            parts.append(c['text'])
    if parts:
        return '\n'.join(parts)
    return m.get('text') or ''


def main():
    try:
        import ijson
    except ImportError:
        print('ijson required: pip install ijson --break-system-packages', file=sys.stderr)
        return 2

    z = zipfile.ZipFile(ZIP)
    pastes, file_refs = [], []
    n_conv = n_msg = 0

    with z.open('conversations.json') as f:
        for conv in ijson.items(f, 'item'):
            n_conv += 1
            cname = conv.get('name') or ''
            cuuid = conv.get('uuid')
            for idx, m in enumerate(conv.get('chat_messages') or []):
                n_msg += 1
                # file/attachment references — collected for BOTH senders, since
                # an image offered in-thread may have been referenced by either.
                for kind in ('files', 'attachments'):
                    for fr in (m.get(kind) or []):
                        file_refs.append({
                            'conversation_uuid': cuuid,
                            'conversation_name': cname,
                            'message_index': idx,
                            'sender': m.get('sender'),
                            'created_at': m.get('created_at'),
                            'kind': kind,
                            'ref': fr if isinstance(fr, (str, int)) else
                                   {k: v for k, v in fr.items()
                                    if k in ('file_name', 'file_size', 'file_type',
                                             'extracted_content', 'file_uuid')
                                    and k != 'extracted_content'},
                        })
                if m.get('sender') != 'human':
                    continue
                txt = message_text(m)
                if len(txt) < MIN_LEN:
                    continue
                hits = [name for name, pat in SIGNATURES if pat.search(txt)]
                if not hits:
                    continue
                txt = redact(txt)
                pastes.append({
                    'conversation_uuid': cuuid,
                    'conversation_name': cname,
                    'conversation_created': conv.get('created_at'),
                    'message_index': idx,
                    'message_uuid': m.get('uuid'),
                    'created_at': m.get('created_at'),
                    'signatures': hits,
                    'chars': len(txt),
                    'footer_present': 'AI can make mistakes' in txt,
                    'text': txt,
                })

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(pastes, ensure_ascii=False), encoding='utf-8')
    FILES_OUT.write_text(json.dumps(file_refs, ensure_ascii=False), encoding='utf-8')

    print('conversations walked : %d' % n_conv)
    print('messages walked      : %d' % n_msg)
    print('human paste-bearing  : %d  (%.1f MB of text)'
          % (len(pastes), sum(p['chars'] for p in pastes) / 1e6))
    print('  with footer seal   : %d' % sum(1 for p in pastes if p['footer_present']))
    print('file/attachment refs : %d' % len(file_refs))
    if REDACTED:
        print('credentials redacted : %s' % REDACTED)
    else:
        print('credentials redacted : none found')
    print('\nwrote %s' % OUT)
    print('wrote %s' % FILES_OUT)
    return 0


if __name__ == '__main__':
    sys.exit(main())
