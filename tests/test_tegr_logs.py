"""Pins src/stur_tegr_logs.py: edge-counting logarithms vs Sen's universal coefficient."""
import os, sys
from fractions import Fraction as Fr
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import stur_tegr_logs as L


def test_sen_benchmarks():
    assert L.sen_c_local() == Fr(212, 45) and L.sen_singlet() == Fr(77, 45)
    assert L.sen_singlet(nV=1) == Fr(64, 45)


def test_edge_logs_and_comparison():
    table, edge = L.comparison()
    expect = {"SO(1,1)": 0, "SL(2,R)": 4, "SL(2,C)": 8, "semigroup": 4}
    for m, v in expect.items():
        assert abs(float(edge[m]) - v) < 1e-3
    sen = table["Sen, pure gravity (universal)"]
    edges = [v for k, v in table.items() if k.startswith("Edge counting")]
    assert sorted(round(x) for x in edges) == [1, 5, 5, 9]
    assert all(abs(x - sen) > 0.5 for x in edges)                 # none is the universal value
