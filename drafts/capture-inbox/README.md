# Capture inbox

Transcripts sent from alexanarch.org/ask/ (Submit a transcript) through api/submit-transcript.js. Each file is one transcript as received, keyed by the first 12 hex digits of its sha256, under the UTC day it arrived. An entry is not a capture until it is read and seated in the Capture Registry through scripts/capture_intake.py; seated entries carry "seated_as". List the unseated: python3 scripts/list_capture_inbox.py
