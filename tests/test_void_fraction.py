"""Pins front 14: the cosmic-web void census vs timescape's required void fraction."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import god_eq_void_fraction as V


def test_lorenz_curve_exact_vs_monte_carlo():
    for s in (0.5, 1.2, 1.8):
        for m in (0.07, 0.18, 0.4):
            assert abs(V.lorenz_mc(s, m, n=400_000) - V.lorenz_V(m, s)) < 3e-3
            assert abs(V.lorenz_m(V.lorenz_V(m, s), s) - m) < 1e-12


def test_redshift_mapping_roundtrip():
    z = V.z_eff_volume_median()
    assert 0.083 < z < 0.086
    for f0 in (0.64, 0.695, 0.853):
        assert abs(V.f0_from_fv_at_z(V.fv_at_z(f0, z), z) - f0) < 1e-9
        assert V.fv_at_z(f0, z) < f0                       # voids grow with time


def test_verdict_numbers():
    r = V.main()
    assert abs(r["f0m"] - 0.639) < 0.002
    dens = {lab: (lo, hi) for lab, _, _, _, lo, hi in r["v1"]}
    assert dens["Pan+2012 VoidFinder"][0] < -0.85            # genuinely empty
    assert dens["Douglass+2023 V2/REVOLVER"][1] > -0.10      # ~ mean density
    sn = r["v3"][2]
    assert -0.76 < sn[4] < -0.72 and -0.52 < sn[5] < -0.48
