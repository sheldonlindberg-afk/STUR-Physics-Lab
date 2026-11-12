"""Pins the symmetry-breaking ladder below 3-3-1: chiral breaking, Casimir-Polder,
graviton exchange and MacDowell-Mansouri (SYMMETRY_LADDER.md)."""
import os, sys
import sympy as sp
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import chiral_breaking as CB
import casimir_diamonds as CP
import graviton_exchange as GX
import macdowell_mansouri as MM


def test_chiral_breaking():
    grad, zeros, evs = CB.goldstone_count()
    assert all(x == 0 for x in grad) and zeros == 3
    stat, resid, msig2 = CB.gmor()
    assert resid == 0
    mpi, _, _ = CB.gmor_numbers()
    assert abs(mpi - 0.1276) < 1e-3
    V, rng = CB.yukawa()
    m, r = sp.symbols("m r", positive=True)
    assert sp.simplify(V - sp.exp(-m * r) / (4 * sp.pi * r)) == 0 and abs(rng - 1.414) < 1e-3
    assert CB.ope_structure()
    g, _ = CB.goldberger_treiman()
    assert abs(g - 13.01) < 0.01


def test_casimir_polder_derived():
    a, resid = CP.sphere_polarizability()
    assert resid == 0
    helm, div, trc = CP.green_tensor()
    assert helm < 1e-25 and div < 1e-25 and trc == 0
    assert CP.frequency_integral() == sp.Rational(23, 4)
    mine, theirs, grav, R = CP.compare_with_experiment_code()
    assert abs(mine / theirs - 1) < 1e-12


def test_graviton_exchange():
    hb, h, Phi, gamma = GX.linearized_point_mass()
    G, M, r = sp.symbols("G M r", positive=True)
    assert sp.simplify(Phi + G * M / r) == 0 and gamma == 1
    TPT, Uq, Ur, rp = GX.one_graviton()
    m1, m2 = sp.symbols("m1 m2", positive=True)
    assert sp.simplify(Ur + G * m1 * m2 / r) == 0 and rp == 2
    mine, theirs, _, _ = GX.branch_phases()
    assert abs(mine - theirs) < 1e-9 and abs(mine - 2.187) < 1e-3


def test_macdowell_mansouri():
    pp, stab, broken = MM.algebra()
    assert pp and len(stab) == 6 and len(broken) == 4
    f = sp.Function("f")(MM.r)
    s_vals, ok, tors, dR, *_ = MM.curvature_split(f)
    assert s_vals == {-1} and ok and tors and dR == 0
    assert MM.de_sitter_vacuum()
    RR, REE, EEEE, cR, cV, e, Rs = MM.action_terms(f)
    assert cR == 2 and cV == 24
