"""Pins src/short_range_gravity.py: how far design A tests Newton's 1/r law against a Yukawa
term alpha exp(-r/lambda), and how that compares with the torsion-balance bound."""
import os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import short_range_gravity as S
import stur_gravity_full as GF


def test_sphere_form_factor():
    shell_ok, ok, lim, phi = S.sphere_form_factor()
    assert shell_ok and ok and lim == 1
    x = np.array([1e-4, 0.05, 0.5, 2.0])
    assert np.allclose(S.phi_num(x), [1 + 1e-9, phi(0.05), phi(0.5), phi(2.0)], rtol=1e-8)
    # design A is a point mass for every lambda that matters
    a = S.design_a()
    assert S.phi_num(a["R"] / 20e-6) ** 2 - 1 < 1e-3


def test_newtonian_phase_is_design_a():
    a = GF.design_a()
    ref = GF.trajectory_dphi(a["m"], a["dx"], a["gap"], a["hold"], a["ramp"])
    assert abs(S.newton_phase() / ref - 1) < 1e-6 and abs(S.newton_phase() - 2.1868) < 1e-4


def test_yukawa_sensitivity_limits():
    # long range: a rescaling of G; short range: exp(-gap/lambda)
    assert abs(S.k_of(1.0) - 1) < 1e-6
    assert abs(S.k_of(1e-2) - 0.9995) < 1e-4
    assert S.k_of(5e-6) < 1e-15
    ks = [S.k_of(l) for l in S.LAMS]
    assert all(b > a for a, b in zip(ks, ks[1:]))
    for lam, k in [(30e-6, 4.080e-3), (100e-6, 0.2523), (181e-6, 0.5308), (1e-3, 0.9597)]:
        assert abs(S.k_of(lam) / k - 1) < 2e-3, lam


def test_phase_is_linear_in_alpha():
    # the Yukawa phase per unit alpha against a direct finite-alpha integration
    a, gap, t, rc = S._trajectory()
    lam, alpha = 100e-6, 0.37
    f = lambda r: (1 + alpha * np.exp(-r / lam)) / r
    direct = 2 * S.G * a["m"] ** 2 / S.HBAR * np.trapezoid(f(gap) - f(rc), t)
    ff = S.phi_num(a["R"] / lam) ** 2
    assert abs(direct / (S.newton_phase() * (1 + alpha * S.k_of(lam) / ff)) - 1) < 1e-12


def test_statistical_reach():
    assert abs(S.alpha_stat(181e-6, 1e4) / 8.61e-3 - 1) < 3e-3
    assert abs(S.alpha_stat(1e-2, 1e4) / 4.58e-3 - 1) < 3e-3
    assert abs(S.lambda_at(S.alpha_stat, 1.0, 1e4) * 1e6 - 30.6) < 0.1
    assert abs(S.lambda_at(S.alpha_stat, 1.0, 1e6) * 1e6 - 22.0) < 0.1


def test_systematic_floors():
    assert abs(S.casimir_phase() / S.newton_phase() - 0.072) < 1e-3
    assert S.thermal_length() > 50 * S.design_a()["gap"]           # T = 0 Casimir-Polder holds
    assert abs(S.alpha_sys_casimir(181e-6, 0.1) / 1.35e-2 - 1) < 5e-3
    assert abs(S.alpha_sys_mass(181e-6, 0.01) / 3.77e-2 - 1) < 5e-3
    # the gap ratio removes G m^2 but keeps most of Casimir: its sensitivity is k(d) - k(2d)
    assert abs(S.k_ratio(181e-6) - 0.2633) < 1e-3
    assert abs(S.casimir_phase(2 * S.design_a()["gap"]) / S.newton_phase(2 * S.design_a()["gap"])
               - 0.00155) < 2e-5


def test_alpha_one_against_torsion_balance():
    r = S.alpha_one_ranges()
    um = lambda key: r[key] * 1e6
    lee = S.LEE2020_LAMBDA * 1e6
    # 1e4 runs, absolute phase: past the torsion balance only with Casimir to ~1-3%, mass to ~0.1-0.3%
    assert abs(um(("abs", 1e4, 0.0, 0.0)) - 34.6) < 0.1
    assert abs(um(("abs", 1e4, 0.01, 0.001)) - 35.2) < 0.1 and um(("abs", 1e4, 0.01, 0.001)) < lee
    assert abs(um(("abs", 1e4, 0.03, 0.003)) - 38.6) < 0.1
    assert um(("abs", 1e4, 0.1, 0.01)) > lee
    assert um(("ratio", 1e4, 0.0)) > lee
    # 1e6 runs: the gap ratio gets past it without knowing the mass
    assert abs(um(("ratio", 1e6, 0.0)) - 30.2) < 0.1
    assert um(("ratio", 1e6, 0.1)) < lee
    # at best, about 10-40% shorter in lambda: exp(-gap/lambda) caps the reach
    assert min(r.values()) * 1e6 > 0.6 * lee
