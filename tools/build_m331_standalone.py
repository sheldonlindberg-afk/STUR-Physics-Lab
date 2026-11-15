#!/usr/bin/env python3
"""Keep the one-paste 3-3-1 script in step with the shared core.

    python3 tools/build_m331_standalone.py            # rewrite the core block of the standalone
    python3 tools/build_m331_standalone.py --check    # exit 1 if that block is stale

src/m331_standalone.py must run from a single paste, so it cannot import src/m331_core.py.
Instead it carries a verbatim copy of the core between the markers '# >>> core' and
'# <<< core'. This tool writes that copy; tests/test_331_core.py runs the check.
"""
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
CORE = os.path.join(ROOT, "src", "m331_core.py")
STANDALONE = os.path.join(ROOT, "src", "m331_standalone.py")
BEGIN, END = "# >>> core", "# <<< core"
NOTE = " (copied from src/m331_core.py by tools/build_m331_standalone.py; edit the core, not this copy)"


def block(text):
    """The text between the two marker lines (exclusive), and the offsets of that span."""
    i = text.index(BEGIN)
    i = text.index("\n", i) + 1
    j = text.index(END)
    return text[i:j], i, j


def build():
    core, _, _ = block(open(CORE, encoding="utf8").read())
    text = open(STANDALONE, encoding="utf8").read()
    _, i, j = block(text)
    head = text[:i]
    k = head.rindex(BEGIN)
    head = head[:k] + BEGIN + NOTE + "\n"
    return head + core + text[j:]


def main():
    new = build()
    if "--check" in sys.argv:
        if new != open(STANDALONE, encoding="utf8").read():
            print("src/m331_standalone.py is stale: run python3 tools/build_m331_standalone.py")
            return 1
        print("src/m331_standalone.py is current")
        return 0
    open(STANDALONE, "w", encoding="utf8").write(new)
    print("wrote src/m331_standalone.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
