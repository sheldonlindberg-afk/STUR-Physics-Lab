#!/usr/bin/env python3
"""The hash that freezes a registration (PREREGISTRATION.md).

The registration is the part of the document above its result separator ("\\n---\\n\\n## Result"), with the title line
("# ...") and any line containing "Status:" left out, since those may change when the result is added. Whitespace at
line ends is ignored.

    python3 tools/prereg.py <file>            # print the hash of the file's registration as it is now
    python3 tools/prereg.py <file> <commit>   # the hash at a commit (needs git history)
"""
import hashlib
import subprocess
import sys

SEPARATOR = "\n---\n\n## Result"


def registration_text(text):
    head = text.split(SEPARATOR)[0]
    keep = [ln.rstrip() for ln in head.splitlines() if not ln.startswith("# ") and "Status:" not in ln]
    return "\n".join(keep).strip() + "\n"


def digest(text):
    return hashlib.sha256(registration_text(text).encode("utf-8")).hexdigest()


if __name__ == "__main__":
    path = sys.argv[1]
    text = (subprocess.run(["git", "show", f"{sys.argv[2]}:{path}"], capture_output=True, text=True, check=True).stdout
            if len(sys.argv) > 2 else open(path, encoding="utf-8").read())
    print(digest(text))
