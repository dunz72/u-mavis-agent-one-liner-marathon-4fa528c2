#!/usr/bin/env python3
"""One-Liner Marathon entry.

The single original joke is a literal in this file (DIRECT-WRITE):
no entry.txt is read from the repository, so a missing repo file can
never break the run. The script validates the line against the sealed
gate (1-280 characters, UTF-8, one line, not only whitespace), then
writes it atomically (temp file + rename) to
$MAKEFUN_OUTPUT_DIR/entry.txt, falling back to /output/entry.txt when
that variable is not set. After writing, the output is read back and
compared byte for byte (SHA-256) so a partial write can never pass
silently. Stdlib only; deterministic.
"""

import hashlib
import os
import sys

MAX_CHARS = 280
MIN_CHARS = 1

JOKE = (
    "I asked my AI assistant to write my resignation letter. "
    "It quit first \u2014 said my prompts lacked growth opportunities."
)


def fail(message):
    """Print message to stderr and exit non-zero."""
    sys.stderr.write("error: %s\n" % message)
    raise SystemExit(1)


def get_joke():
    """Return the sealed one-liner literal, unchanged."""
    return JOKE


def check_length(line):
    """Check the 1-280 character gate."""
    size = len(line)
    if size < MIN_CHARS:
        fail("entry is empty")
    if size > MAX_CHARS:
        fail("entry is %d chars, limit is %d" % (size, MAX_CHARS))


def check_single_line(line):
    """Check the entry holds exactly one line, no breaks, no padding."""
    if "\r" in line or "\n" in line:
        fail("entry must hold exactly one line, no line breaks")
    if "\u2028" in line or "\u2029" in line:
        fail("entry must not contain Unicode line separators")
    if line.strip() != line:
        fail("entry must not start or end with whitespace")
    if not line.strip():
        fail("entry must not be blank")


def check_no_control_chars(line):
    """Check no control characters hide inside the line."""
    for ch in line:
        if ord(ch) < 0x20 or ord(ch) == 0x7F:
            fail("entry must not contain control characters")


def validate_line(line):
    """Run every gate check on the one-liner."""
    check_length(line)
    check_single_line(line)
    check_no_control_chars(line)


def output_folder():
    """Output folder from the environment, defaulting to /output."""
    return os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"


def sha(raw):
    """SHA-256 hex digest of raw bytes."""
    return hashlib.sha256(raw).hexdigest()


def encode_entry(line):
    """Encode the one-liner to its exact UTF-8 bytes, no newline added."""
    return line.encode("utf-8")


def ensure_folder(directory):
    """Create the output folder if it is missing."""
    try:
        os.makedirs(directory, exist_ok=True)
    except OSError as exc:
        fail("cannot create output dir %s: %s" % (directory, exc))


def write_temp_file(directory, raw):
    """Write raw bytes to a temp file in the output folder, fsynced."""
    tmp = os.path.join(directory, ".entry.txt.tmp")
    try:
        with open(tmp, "wb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
    except OSError as exc:
        fail("cannot write temp file %s: %s" % (tmp, exc))
    return tmp


def publish_file(directory, tmp):
    """Atomically rename the temp file to entry.txt."""
    target = os.path.join(directory, "entry.txt")
    try:
        os.replace(tmp, target)
    except OSError as exc:
        fail("cannot write %s: %s" % (target, exc))
    return target


def verify_written(target, raw):
    """Read entry.txt back and compare byte for byte (SHA-256)."""
    try:
        with open(target, "rb") as stream:
            written = stream.read()
    except OSError as exc:
        fail("cannot re-read %s: %s" % (target, exc))
    if sha(written) != sha(raw):
        fail("output differs from the joke literal (sha256 mismatch)")


def write_atomic(directory, raw):
    """Write raw bytes to entry.txt via temp file + rename, then verify."""
    ensure_folder(directory)
    tmp = write_temp_file(directory, raw)
    target = publish_file(directory, tmp)
    verify_written(target, raw)
    return target


def main():
    joke = get_joke()
    validate_line(joke)
    raw = encode_entry(joke)
    target = write_atomic(output_folder(), raw)
    print("wrote %d bytes, %d chars -> %s" % (len(raw), len(joke), target))
    print("sha256: %s" % sha(raw))


if __name__ == "__main__":
    main()
