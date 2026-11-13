"""Pins rung 6 of the ladder: black holes (src/black_holes.py, SYMMETRY_LADDER.md)."""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import black_holes as BH


def test_surface_gravity_and_euclidean_period():
    assert BH.surface_gravity_from_spin_connection() == 0
    assert BH.euclidean_ratio() == 0
    out = BH.euclidean_checks()
    for rh, k, smooth, cone in out.values():
        assert abs(smooth - 1) < 1e-5 and abs(cone - 1.1) < 1e-5
    kb, kc = out["black hole"][1], out["cosmological"][1]
    assert abs(kb / kc - 1) > 0.5                       # two horizons, two temperatures


def test_thermodynamics_exact():
    assert all(v == 0 for v in BH.thermodynamics().values())


def test_nariai():
    rN, l2N, res = BH.nariai()
    assert rN == 3 * BH.M and l2N == 27 * BH.M**2 and res == 0
    rb, rc, kb, kc = BH.sds_temperatures(0.9999)
    assert abs(rb - 3) < 0.02 and abs(rc - 3) < 0.02 and kb < 2e-3 and kc < 2e-3
    m, msun, rad, tds = BH.nariai_numbers()
    assert abs(m / 4.269e52 - 1) < 1e-3 and abs(rad / 9.51e25 - 1) < 1e-3


def test_geodesics():
    r_ph, b_c, r_isco, L2, E2, stab = BH.geodesics()
    M = BH.M
    assert r_ph == 3 * M and (b_c**2 - 27 * M**2).simplify() == 0
    assert r_isco == 6 * M and L2 == 12 * M**2 and E2 == BH.sp.Rational(8, 9)


def test_eht_shadows():
    out = BH.eht()
    p87, _, _, z87, gas = out["M87*"]
    pS, _, _, zS, _ = out["Sgr A*"]
    assert abs(p87 - 37.8) < 0.1 and abs(pS - 52.3) < 0.1
    assert abs(z87) < 2 and abs(zS) < 2 and gas < 21


def test_gw250114():
    a_i, a_f, a_i_max, a_f_min, (mf, chif) = BH.area_law()
    assert abs(a_i / 2.374e5 - 1) < 1e-3 and abs(a_f / 4.065e5 - 1) < 1e-3
    assert a_f_min > a_i_max
    assert abs(mf - 66.7) < 0.1 and abs(chif - 0.75) < 0.01
    f, g, df, dg = BH.ringdown()
    assert abs(f - BH.F220) < 2 * BH.F220_ERR and BH.G220 - 2 * BH.G220_LO < g < BH.G220 + 2 * BH.G220_HI


def test_links():
    rs, ratio, mpl, kT, frac, rs_pl = BH.links()
    assert abs(rs / 2.180e-41 - 1) < 1e-3 and abs(ratio / 1.349e-6 - 1) < 1e-3
    assert abs(mpl / BH.M_PLANCK_GEV - 1) < 1e-6
    assert abs(frac - 1) < 1e-6 and abs(rs_pl - 2) < 1e-12
