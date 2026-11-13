"""Pins src/m331_margin.py: the beta = +1/sqrt3 margin against physical mass floors."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import m331_margin as M


def test_split_reproduces_tied_scan():
    # m_J = m_E = r_J M_V, m_S = r_S M_V reproduces the section 3d worst case (1.262 M_Pl)
    r = M.rel(MV=2e3, mJ=1e3, mE=1e3, mS=2e3 / 3, n_light=2)
    assert abs(r - 1.262) < 0.002


def test_grid_corner_is_not_a_bound():
    rows = dict(M.grid_edge())
    assert rows[0.3] < 1.0 < rows[0.5]


def test_light_heavy_leptons_fail():
    assert abs(M.rel(**M.FLOORS) - 0.605) < 0.005


def test_heavy_lepton_threshold():
    assert abs(M.mE_critical() - 584) < 5
    assert abs(M.mE_critical(MV=30e3) - 1812) < 15


def test_nc5_still_excluded_at_floors():
    assert M.rel(Nc=5, **M.FLOORS) < 1e-6
