"""Pins PREREGISTRATION.md: no registration in the registry has been edited since it was registered."""
import os
import re
import sys

ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, os.path.join(ROOT, "tools"))
import prereg  # noqa: E402


def registry():
    rows = []
    for line in open(os.path.join(ROOT, "PREREGISTRATION.md"), encoding="utf-8"):
        m = re.match(r"\|\s*\[([^\]]+)\]\([^)]+\)\s*\|\s*([0-9a-f]{7,40})\s*\|\s*([0-9a-f]{64})\s*\|", line)
        if m:
            rows.append(m.groups())
    return rows


def test_registry_is_not_empty():
    assert registry()


def test_registrations_are_unchanged():
    for doc, commit, h in registry():
        text = open(os.path.join(ROOT, doc), encoding="utf-8").read()
        assert prereg.digest(text) == h, f"{doc}: the registration above its result was edited after commit {commit}"


def test_results_sit_below_the_separator():
    for doc, _, _ in registry():
        text = open(os.path.join(ROOT, doc), encoding="utf-8").read()
        assert prereg.SEPARATOR in text, doc


def test_the_hash_catches_an_edit_and_ignores_the_status_line():
    text = open(os.path.join(ROOT, registry()[0][0]), encoding="utf-8").read()
    assert prereg.digest(text.replace("Status:", "Status: (changed)", 1)) == prereg.digest(text)
    head, sep, tail = text.partition(prereg.SEPARATOR)
    assert prereg.digest(head.replace("str[k₁]", "str[k1]", 1) + sep + tail) != prereg.digest(text)
