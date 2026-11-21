"""Pins CLAIMS.md: every claim has a valid label, assumptions and a falsifier, and every test it names exists."""
import os
import re

ROOT = os.path.join(os.path.dirname(__file__), "..")
LABELS = {"CHECK", "RESULT", "DATA", "MODEL", "NEGATIVE", "ASSESSMENT"}


def rows():
    out = []
    for line in open(os.path.join(ROOT, "CLAIMS.md"), encoding="utf-8"):
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 6 and re.fullmatch(r"[A-Z]\d+", cells[0]):
            out.append(cells)
    return out


def test_ledger_has_claims_with_unique_ids():
    ids = [r[0] for r in rows()]
    assert len(ids) >= 15 and len(ids) == len(set(ids))


def test_every_row_is_complete():
    for cid, claim, label, pinned, assumes, falsifier in rows():
        assert label in LABELS, (cid, label)
        assert claim and assumes and falsifier and pinned, cid


def test_every_named_test_exists():
    missing = []
    for cid, _, _, pinned, _, _ in rows():
        for node in [p.strip() for p in pinned.split(",")]:
            path, _, name = node.partition("::")
            f = os.path.join(ROOT, path)
            if not (os.path.exists(f) and re.search(rf"^def {re.escape(name)}\(", open(f, encoding="utf-8").read(), re.M)):
                missing.append((cid, node))
    assert not missing, missing


def test_readme_points_to_the_ledger():
    assert "CLAIMS.md" in open(os.path.join(ROOT, "README.md"), encoding="utf-8").read()
