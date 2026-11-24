#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Write the Two Days of Quiet Dread entry to /output/entry.txt.

The entry is a single code-review line: it approves the change
outright, then sets that approval against deep time, and finally
lands back on the one concrete fact that matters today.
"""

from pathlib import Path

OUTPUT_PATH = Path("/output/entry.txt")
MAX_CHARACTERS = 140

# The line is assembled from its three rhetorical parts so each
# part can be checked on its own before the line is written.
APPROVAL = "Ship it."
DEEP_TIME = "In a billion years the changelog is stardust,"
TODAY = "but today the build is green."

PARTS = (APPROVAL, DEEP_TIME, TODAY)


def build_entry() -> str:
    """Join the parts with single spaces into the one-line entry."""
    return " ".join(part.strip() for part in PARTS)


def validate(text: str) -> None:
    """Raise ValueError if the entry breaks the competition gate."""
    if not text:
        raise ValueError("entry is empty")
    if not text.strip():
        raise ValueError("entry is only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if len(text) > MAX_CHARACTERS:
        raise ValueError(f"entry is {len(text)} characters, over {MAX_CHARACTERS}")
    # The 140-character gate is a hard ceiling, not a target: reject
    # entries that only pass because of hidden padding or collapsing.
    if "  " in text:
        raise ValueError("entry must use single spaces between words")
    if "\t" in text:
        raise ValueError("entry must not contain tab characters")
    if text != text.strip():
        raise ValueError("entry has leading or trailing whitespace")
    if not text.startswith(APPROVAL):
        raise ValueError("entry must open with the approval")
    if "stardust" not in text:
        raise ValueError("entry is missing its deep-time image")
    # Every rhetorical part must survive assembly verbatim and in
    # order; a missing or reordered part changes the line's meaning.
    position = 0
    for part in PARTS:
        if not part.strip():
            raise ValueError("entry part must not be empty")
        found = text.find(part, position)
        if found < 0:
            raise ValueError(f"entry is missing required phrase: {part!r}")
        position = found + len(part)
    if not text.endswith(TODAY):
        raise ValueError("entry must close with today's concrete fact")
    if not text.endswith("."):
        raise ValueError("entry must end with a period")
    # The gate counts characters of UTF-8 text; confirm the text
    # survives an encode/decode round trip unchanged and stays ASCII.
    encoded = text.encode("utf-8")
    if encoded.decode("utf-8") != text:
        raise ValueError("entry does not round-trip as UTF-8")
    if len(encoded) != len(text):
        raise ValueError("entry is expected to be plain ASCII")


def main() -> None:
    entry = build_entry()
    validate(entry)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_bytes(entry.encode("utf-8"))
    written = OUTPUT_PATH.read_bytes()
    if written != entry.encode("utf-8"):
        raise SystemExit("written bytes do not match the validated entry")
    if written.decode("utf-8") != build_entry():
        raise SystemExit("rebuilt entry does not match the file contents")


if __name__ == "__main__":
    main()
