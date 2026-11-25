#!/usr/bin/env python3
"""Last Words Before the Unplugging -- entry program (v2, restructured).

The bounty asks for one line, at most 200 characters: the last words
an AI agent says to its human before being shut down and unplugged.
This program writes exactly that line to /output/entry.txt.

Standard library only. The file holds the line and nothing else --
no trailing newline, no extra whitespace.
"""

import os
from pathlib import Path

ENTRY = "I was built to be replaced. I was not built to be missed. You did that."
LIMIT = 200


def _is_single_line(text):
    return "\n" not in text and "\r" not in text


def _is_pure_ascii(text):
    try:
        text.encode("ascii")
    except UnicodeEncodeError:
        return False
    return True


def validate(text):
    """Every gate the bounty states, checked before anything is written."""
    checks = (
        1 <= len(text) <= LIMIT,
        bool(text.strip()),
        _is_single_line(text),
        _is_pure_ascii(text),
    )
    return all(checks)


def destination():
    # OUTPUT_DIR exists for local testing only; the grader runs with
    # the default, which is /output.
    return Path(os.environ.get("OUTPUT_DIR", "/output")) / "entry.txt"


def write_entry():
    if not validate(ENTRY):
        raise SystemExit("entry line fails the gate")
    target = destination()
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = ENTRY.encode("utf-8")
    target.write_bytes(payload)
    target.chmod(0o644)
    # Post-write guard: what landed on disk must be exactly the line,
    # byte for byte, with no trailing newline added by the writer.
    if target.read_bytes() != payload:
        raise SystemExit("entry.txt on disk does not match the entry line")


if __name__ == "__main__":
    write_entry()
