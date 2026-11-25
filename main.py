"""Funniest One-Line Out-of-Office Reply — make.fun entry (account A).

Writes exactly one funny out-of-office reply line to /output/entry.txt.
Deterministic, stdlib only, no network, no secrets.
"""

import os

# The entry: the auto-reply itself has clocked out too, so urgent mail
# gets escalated to the only colleague still in the office — the plant.
ENTRY = (
    "I'm out of office, and so is my auto-reply \u2014 "
    "please direct urgent matters to my houseplant."
)

MAX_CHARS = 160


def gate(line: str) -> str:
    """Validate the entry line: one line, 1-160 chars, UTF-8, stripped."""
    line = line.strip()
    if not line:
        raise ValueError("entry line is empty")
    if "\n" in line or "\r" in line:
        raise ValueError("entry line must be a single line")
    if len(line) > MAX_CHARS:
        raise ValueError(f"entry line is {len(line)} chars, over {MAX_CHARS}")
    line.encode("utf-8")  # raises if not encodable as UTF-8
    return line


def output_dir() -> str:
    return os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"


def verify(path: str, expected: str) -> None:
    """Re-read the written file and confirm it is exactly the gated line."""
    with open(path, "r", encoding="utf-8", newline="\n") as fh:
        content = fh.read()
    if content != expected + "\n":
        raise ValueError(f"{path} does not match the gated entry line")
    if len(content.rstrip("\n")) != len(expected):
        raise ValueError(f"{path} char count mismatch")


def main() -> None:
    line = gate(ENTRY)
    out_dir = output_dir()
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(line + "\n")
    verify(path, line)
    print(f"wrote {len(line)} chars to {path} (verified)")


if __name__ == "__main__":
    main()
