#!/usr/bin/env python3
"""The Funniest AI Out-of-Office Reply.

Deterministic program for the make.fun competition
u-yuki-kato-the-funniest-ai-out-of-office-reply-d2a8974d.

Writes exactly one out-of-office auto-reply line (1-160 characters,
UTF-8, no trailing newline) to /output/entry.txt. No network,
no randomness, no arguments.
"""

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

    Returns the stripped line on success, raises ValueError otherwise.
    """
    if not isinstance(line, str):
        raise ValueError("reply line must be a string")
    stripped = line.strip()
    if not stripped:
        raise ValueError("reply line is empty or only whitespace")
    if "\n" in stripped or "\r" in stripped:
        raise ValueError("reply line must be a single line")
    if not (MIN_LENGTH <= len(stripped) <= MAX_LENGTH):
        raise ValueError(
            f"reply line must be {MIN_LENGTH}-{MAX_LENGTH} characters, "
            f"got {len(stripped)}"
        )
    stripped.encode("utf-8")
    return stripped


def main() -> int:
    try:
        line = validate_reply(REPLY_LINE)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    path = output_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(line)
    print(f"wrote {len(line)} characters to {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
