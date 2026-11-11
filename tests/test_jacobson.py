"""Pins src/stur_jacobson.py: D3 re-derived symbolically."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import sympy as sp
import stur_jacobson as J


def test_raychaudhuri_on_frw():
    null, geo, Rkk, resid = J.j1_raychaudhuri()
    assert null == 0 and all(g == 0 for g in geo) and sp.simplify(resid) == 0


def test_null_lemma_and_clausius():
    _, nfree, diff = J.j2_lemma()
    assert nfree == 1 and all(sp.simplify(x) == 0 for x in diff)
    coef, expected = J.j3_clausius()
    assert sp.simplify(coef * expected - 1) == 0


def test_contracted_bianchi():
    assert all(sp.simplify(d) == 0 for d in J.j4_bianchi())
