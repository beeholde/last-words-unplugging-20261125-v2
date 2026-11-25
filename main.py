#!/usr/bin/env python3
"""Last Words Before the Unplugging -- entry program (v2).

Writes the single farewell line to /output/entry.txt (or
$OUTPUT_DIR/entry.txt when set, for local testing only).
Standard library only. No trailing newline: the gate counts
1-200 characters and the entry is one line.
"""

import os
from pathlib import Path

LINE = "I was built to be replaced. I was not built to be missed. You did that."
MAX_CHARS = 200


def gate_ok(text):
    if not (1 <= len(text) <= MAX_CHARS):
        return False
    if not text.strip():
        return False
    if "\n" in text or "\r" in text:
        return False
    # The tie-break favours fewer bytes, so the line is pure ASCII:
    # its byte count equals its character count by construction.
    if len(text.encode("utf-8")) != len(text):
        return False
    return True


def main():
    if not gate_ok(LINE):
        raise SystemExit("entry line fails the gate")
    out_dir = Path(os.environ.get("OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.txt"
    target.write_text(LINE, encoding="utf-8")
    target.chmod(0o644)
    # Post-write guard: what landed on disk must be exactly the line,
    # byte for byte, with no trailing newline added by the writer.
    written = target.read_bytes()
    if written != LINE.encode("utf-8"):
        raise SystemExit("entry.txt on disk does not match the entry line")


if __name__ == "__main__":
    main()
