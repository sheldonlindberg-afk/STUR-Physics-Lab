"""Pins the fullness-phase theory (working name): gravity law, degradation, phase locking."""
import os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import fp_gravity as Gr
import fp_degradation as D
import fp_phase_lock as P


def test_gravity_law():
    u = np.linspace(1e-6, np.pi - 1e-6, 5001)
    assert np.max(np.abs(Gr.friedmann_residual(u))) < 1e-12        # (F) holds
    phi, T, f, fT = Gr.law(np.array([1e-3]))
    assert abs(f[0] / T[0] - 1 - phi[0] / 3) < 1e-9                  # TEGR limit, 1 + phi/3
    assert np.allclose(T, 4 * -1.0 * phi * (1 - phi))                # torsion = 4 T_b phi(1-phi)
    lo, hi = Gr.law(np.pi / 2 - 1e-7)[3], Gr.law(np.pi / 2 + 1e-7)[3]
    assert abs(lo - hi) < 1e-6                                       # smooth through half-full


def test_bounce_and_cores():
    for w in (0.0, 1 / 3):
        t, rho, H, lna, cons = Gr.bounce(w)
        assert 0.99999 < rho.max() <= 1 + 1e-9 and H[-1] > 0 and cons < 1e-6
    M = Gr.M_SUN
    assert abs(Gr.core_radius(M) - 4.516e-23) < 0.01e-23
    rs = 2 * Gr.G * M / Gr.c ** 2
    assert abs(Gr.horizon_to_core_time(M) / (2 * rs / (3 * Gr.c)) - 1) < 1e-3
    assert abs(Gr.no_horizon_mass() / Gr.M_P - 0.1727) < 1e-3


def test_degradation_bounds():
    r = D.main()
    assert 3.5e20 < r["earth"] < 3.7e20
    m, rr = D.solve_static(2.0, 1.0)
    assert abs(m - np.exp(-0.5)) < 1e-9 and abs(m + rr - 1) < 1e-11


def test_phase_lock():
    assert abs(P.adler_slip_rate(0.5, 1.0, t_end=400, n=40001)) < 1e-6
    assert abs(P.adler_slip_rate(3.0, 1.0, t_end=400, n=40001) - np.sqrt(8)) < 5e-3
    assert abs(P.probe_wall(None, "HL") / P.L_P - np.sqrt(2)) < 1e-12
    assert P.probe_wall(1e-6, "HL") < 1e-60                          # probe alone: sub-Planck
    assert abs(P.backaction_wall(1.0, P.c) / P.L_P - 1) < 1e-12      # mutual lock: l_P
    assert abs(P.main()["phi_wall"] - 0.0597) < 1e-3


def test_black_hole_exterior():
    import fp_black_hole_exterior as X
    r = np.array([1.01, 1.5, 3.0, 50.0])
    A = 1 - 1 / r
    assert np.allclose(X.torsion_general(r, A, 1 / A, 1 / r ** 2), X.torsion_schw(r, 1.0))
    assert abs(X.torsion_schw(1e3, 1.0) / (-2 * 0.25 / 1e12) - 1) < 2e-3    # -2M^2/r^4
    assert abs(X.torsion_schw(1 + 1e-8, 1.0)) > 1e4                           # diverges
    assert abs(X.cap_exact(1e4) - X.cap(1e4 * X.L_P)["ln_inv_delta"]) < 1e-5  # cap formula
    M62 = 62 * X.M_SUN
    assert abs(X.echo_delay(M62) - 0.455) < 0.002                             # echo delay
    assert abs(X.t_escape(M62) / X.t_hawking(M62) - 1 / 480) < 1e-12
    assert abs(X.mass_escaping_now() / 1.35e12 - 1) < 0.01
