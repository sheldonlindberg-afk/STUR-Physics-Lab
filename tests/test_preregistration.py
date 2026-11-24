"""Pins archive/PREREGISTRATION.md: no registration in its registry has been edited since it was registered.

The hash is the one of the former tools/prereg.py, unchanged: the part of the document above its result
separator ("\\n---\\n\\n## Result"), with the title line ("# ...") and any line containing "Status:" left out,
since those may change when the result is added. Whitespace at line ends is ignored.

    python3 tests/test_preregistration.py <file>     # print the registration hash of a file
"""
import hashlib
import os
import re
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
REGISTRY = os.path.join(ROOT, "archive", "PREREGISTRATION.md")
SEPARATOR = "\n---\n\n## Result"


def registration_text(text):
    head = text.split(SEPARATOR)[0]
    keep = [ln.rstrip() for ln in head.splitlines() if not ln.startswith("# ") and "Status:" not in ln]
    return "\n".join(keep).strip() + "\n"


def digest(text):
    return hashlib.sha256(registration_text(text).encode("utf-8")).hexdigest()


def registry():
    rows = []
    for line in open(REGISTRY, encoding="utf-8"):
        m = re.match(r"\|\s*\[[^\]]+\]\(([^)]+)\)\s*\|\s*([0-9a-f]{7,40})\s*\|\s*([0-9a-f]{64})\s*\|", line)
        if m:
            rows.append((os.path.normpath(os.path.join(os.path.dirname(REGISTRY), m.group(1))),
                         m.group(2), m.group(3)))
    return rows


def test_registry_lists_every_registration():
    docs = {os.path.basename(d) for d, _, _ in registry()}
    assert {"INDUCED_GRAVITY_FINITE.md", "PART_K_Z3_OVERLAPS.md"} <= docs, docs


def test_registrations_are_unchanged():
    for doc, commit, h in registry():
        text = open(doc, encoding="utf-8").read()
        assert digest(text) == h, f"{doc}: the registration above its result was edited after commit {commit}"


def test_results_sit_below_the_separator():
    for doc, _, _ in registry():
        assert SEPARATOR in open(doc, encoding="utf-8").read(), doc


def test_the_hash_catches_an_edit_and_ignores_the_status_line():
    doc = registry()[0][0]
    text = open(doc, encoding="utf-8").read()
    assert digest(text.replace("Status:", "Status: (changed)", 1)) == digest(text)
    head, sep, tail = text.partition(SEPARATOR)
    assert digest(head.replace("str[k₁]", "str[k1]", 1) + sep + tail) != digest(text)


if __name__ == "__main__":
    print(digest(open(sys.argv[1], encoding="utf-8").read()))
