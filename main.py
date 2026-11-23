#!/usr/bin/env python3
"""The Funniest AI Out-of-Office Reply.

Deterministic program for the make.fun competition
u-yuki-kato-the-funniest-ai-out-of-office-reply-d2a8974d.

Writes exactly one out-of-office auto-reply line (1-160 characters,
UTF-8, no trailing newline) to /output/entry.txt. No network,
no randomness, no arguments.

Length gate (competition rule, enforced in validate_reply):
the reply must be a single line of 1-160 characters. The gate counts
Unicode code points (Python len), not bytes, because the brief limits
"characters". A line that is empty, whitespace-only, multi-line, or
outside 1-160 characters is rejected before anything is written, so
an invalid entry can never reach the output file.
"""

import argparse
import os
import sys

REPLY_LINE = (
    "I'm on vacation, so I trained a smaller model to answer for me. "
    "It has already asked for a raise and a window seat."
)

MIN_LENGTH = 1
MAX_LENGTH = 160


def output_path() -> str:
    """Return the entry file path.

    Honors MAKEFUN_OUTPUT_DIR when set, otherwise /output/entry.txt.
    """
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return os.path.join(out_dir, "entry.txt")


def validate_reply(line: str) -> str:
    """Validate the reply line before it is written out.

    Rules (from the competition brief):
    - exactly one line, 1-160 characters, UTF-8 encodable
    - must not be empty or whitespace only
    - must not contain control characters other than plain spaces,
      which would break the "one line of plain text" requirement

    The length check uses len() on the stripped string, i.e. Unicode
    code points, matching the brief's "characters" wording. Validation
    happens before any file is created, so a bad line fails fast with
    exit code 1 and leaves no partial output behind.

    Returns the stripped line on success, raises ValueError otherwise.
    """
    if not isinstance(line, str):
        raise ValueError("reply line must be a string")
    stripped = line.strip()
    if not stripped:
        raise ValueError("reply line is empty or only whitespace")
    if "\n" in stripped or "\r" in stripped:
        raise ValueError("reply line must be a single line")
    if any(ord(ch) < 0x20 and ch != "\t" for ch in stripped):
        raise ValueError("reply line must not contain control characters")
    if not (MIN_LENGTH <= len(stripped) <= MAX_LENGTH):
        raise ValueError(
            f"reply line must be {MIN_LENGTH}-{MAX_LENGTH} characters, "
            f"got {len(stripped)}"
        )
    try:
        stripped.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise ValueError(f"reply line is not valid UTF-8: {exc}") from exc
    return stripped


def self_test() -> int:
    """Verify the entry end to end without touching /output.

    Validates the reply line, writes it to a temp directory, reads it
    back and checks byte-for-byte identity, length, single-line shape
    and absence of a trailing newline. Returns 0 when every check
    passes, 1 otherwise. Used by `python3 main.py --self-test`.
    """
    import tempfile

    checks = []
    try:
        line = validate_reply(REPLY_LINE)
    except ValueError as exc:
        print(f"self-test FAILED: validation: {exc}", file=sys.stderr)
        return 1
    checks.append(("length 1-160 chars", MIN_LENGTH <= len(line) <= MAX_LENGTH))
    checks.append(("single line", "\n" not in line and "\r" not in line))
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "entry.txt")
        with open(path, "w", encoding="utf-8", newline="") as fh:
            fh.write(line)
        data = open(path, "rb").read()
    checks.append(("no trailing newline", not data.endswith(b"\n")))
    checks.append(("round-trip identical", data.decode("utf-8") == line))
    checks.append(("byte length equals char length (ASCII)", len(data) == len(line)))
    failed = [name for name, ok in checks if not ok]
    if failed:
        print(f"self-test FAILED: {', '.join(failed)}", file=sys.stderr)
        return 1
    print(f"self-test OK: {len(line)} characters, {len(checks)} checks passed")
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="verify the entry end to end and exit (writes nothing to /output)",
    )
    args = parser.parse_args(argv)
    if args.self_test:
        return self_test()
    try:
        line = validate_reply(REPLY_LINE)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    path = output_path()
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="") as fh:
            fh.write(line)
    except OSError as exc:
        print(f"error: cannot write {path}: {exc}", file=sys.stderr)
        return 1
    print(f"wrote {len(line)} characters to {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
