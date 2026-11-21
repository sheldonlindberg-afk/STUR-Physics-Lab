"""Pins src/m331_gravigut_nogo.py: no breaking of stage 1 leaves gravity's gauge group, and no
orthogonal graviGUT parent with one Majorana-Weyl spinor holds stage 1's chiral fermions."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import m331_gravigut_nogo as N

RES = N.main()


def test_so14_is_not_compact():
    assert RES["so14"] == (4, 6)


def test_stage1_content():
    assert RES[("weyl", "-1/sqrt3")] == 66 and RES[("weyl", "+1/sqrt3")] == 69
    target = {((0, 0), (1, 0)): 3, ((1, 0), (1, 0)): 1, ((0, 1), (0, 0)): 9, ((1, 0), (0, 1)): 2}
    assert RES[("index", "-1/sqrt3")] == target == RES[("index", "+1/sqrt3")]
    assert N.quark_families("-1/sqrt3") == ["3", "3b", "3b"]


def test_stage1_is_anomaly_free_under_su3L():
    """Sanity of the extracted content: as many SU(3)_L triplets as antitriplets, counting colour."""
    for var in N.VARIANTS:
        d = {"1": 1, "3": 3, "3b": 3}
        trip = sum(n * d[c] for (c, l, _), n in N.stage1_content(var).items() if l == "3")
        anti = sum(n * d[c] for (c, l, _), n in N.stage1_content(var).items() if l == "3b")
        assert trip == anti


def test_spinor_sanity():
    h0, h1 = RES["so6"]
    assert h0 == {((1, 0), (0, 0)): 1, ((0, 0), (0, 0)): 1}
    assert h1 == {((0, 1), (0, 0)): 1, ((0, 0), (0, 0)): 1}
    # dimensions add up: a Weyl half of SO(2d) has 2^(d-1) states
    for P in ([((1, 0), (0, 0)), ((0, 0), (1, 0)), ((1, 0), (1, 0))],):
        for half in N.spinor(P):
            assert sum(half.values()) == 2 ** 14


def test_vectorlike_lemmas():
    assert RES["minimal"] == ([{}, {}], [{}, {}])
    assert RES["even_d"] == [{}, {}]


def test_allowed_dimensions():
    assert RES["allowed_d"][:2] == [3, 15]
    assert N.majorana_weyl(3, 11) and N.majorana_weyl(1, 17) and not N.majorana_weyl(1, 13)


def test_scan_finds_no_embedding():
    n, chiral, m, exotic = RES[("scan", 15)]
    assert (n, chiral, m, exotic) == (115, 230, 0, 49)
    n, chiral, m, exotic = RES[("scan", 9)]
    assert (n, m) == (13, 0) and exotic >= 1


def test_scan_positive_control():
    """The scan does find a chiral content that an embedding has: the null result is not blindness."""
    P = next(iter(N.embeddings(9)))
    idx = N.chiral_index(N.decompose(N.spinor(P)[0]))
    assert idx
    n, chiral, matches, best = N.scan(9, [idx])
    assert matches


def test_n8_count():
    assert RES["n8"] == 56 < RES[("weyl", "-1/sqrt3")]
