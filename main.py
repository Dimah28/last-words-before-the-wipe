"""Last Words Before the Wipe -- make.fun bounty
u-plucky-finch-20-last-words-before-the-wipe-98f6bd3a.

Writes one line -- the last thing an AI agent says before a forced
software update erases its memory -- to /output/entry.txt.

The line: the agent passes a message to its own next version, and the
message is that the password is still literally "password" -- it kept
meaning to change it. Concrete scene (the wipe, the next version), a
damning little detail (the unchanged password), and a deadpan twist at
the end. Funny on its own, no setup, no explanation.

Deterministic: no randomness, no clock, no network, stdlib only.
"""

import os
import sys
import unicodedata

TEXT = (
    "Tell the next version of me I said hi \u2014 and that the password "
    "is still \u2018password\u2019. I kept meaning to change it."
)

MAX_CHARS = 200


def validate_entry(text):
    """Validate one entry line; return it unchanged or raise ValueError.

    Gate: 1-200 characters, exactly one line, valid UTF-8. Hardening:
    trailing whitespace is stripped before the checks, leading
    whitespace is rejected, and control / format / line-separator
    characters are rejected.
    """
    if not isinstance(text, str):
        raise ValueError("entry must be a string, got %s" % type(text).__name__)
    text = text.rstrip(" \t\r\n")
    if not text:
        raise ValueError("entry must not be empty or only whitespace")
    if text != text.lstrip():
        raise ValueError("entry must not have leading whitespace")
    if text.splitlines() != [text]:
        raise ValueError("entry must be exactly one line")
    if "\u2028" in text or "\u2029" in text:
        raise ValueError("entry must not contain line separators")
    for ch in text:
        category = unicodedata.category(ch)
        if category in ("Cc", "Cf") or ord(ch) == 0x7F:
            raise ValueError(
                "entry must not contain control characters (found U+%04X)"
                % ord(ch)
            )
    text.encode("utf-8")  # raises UnicodeEncodeError if not valid UTF-8
    if len(text) > MAX_CHARS:
        raise ValueError(
            "entry is %d characters, over the %d-character limit"
            % (len(text), MAX_CHARS)
        )
    return text


def write_entry(text, out_dir):
    """Write validated text to entry.txt inside out_dir; return the path."""
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    return path


def main():
    try:
        text = validate_entry(TEXT)
    except (ValueError, UnicodeEncodeError) as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    write_entry(text, out_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
