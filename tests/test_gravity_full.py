"""Pins the numbers of src/stur_gravity_full.py (fast subset plus one coarse search)."""
import os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import stur_gravity_entanglement as g
import stur_gravity_full as f

B = g.BASE
GAP = g.casimir_vs_gravity_gap(B["m"], B["dx"], B["tau"], "parallel")


def test_casimir_gap_mass_independent():
    gaps = [g.casimir_vs_gravity_gap(m, B["dx"], B["tau"], "parallel") for m in (1e-16, 1e-13)]
    assert abs(gaps[0] - gaps[1]) < 1e-9 and abs(GAP * 1e6 - 181.2) < 0.2


def test_ramps_and_closed_form():
    assert abs(f.trajectory_dphi(B["m"], B["dx"], GAP, B["tau"], 0.0) - f.hold_dphi(B["m"], B["dx"], GAP, B["tau"])) < 1e-3
    r = f.trajectory_dphi(B["m"], B["dx"], GAP, B["tau"], 0.5) / f.hold_dphi(B["m"], B["dx"], GAP, B["tau"])
    assert abs(r - 1.184) < 2e-3
    for tr in (0.2, 1.0):
        assert abs(f.dphi_fast(B["m"], B["dx"], GAP, 1.0, tr) - f.trajectory_dphi(B["m"], B["dx"], GAP, 1.0, tr)) < 1e-3


def test_blackbody():
    assert f.lambda_bb_scatter(B["m"], 0.15) * B["dx"] ** 2 < 1e-14
    budget = 0.289 / (B["tau"] + 1.0) / 3
    assert abs(f.max_internal_T(B["m"], B["dx"], budget, 0.15, 0.01) - 1.03) < 0.02


def test_phase_noise_and_acceleration():
    ph = g.phases(**B, geometry="parallel")
    s_ind, s_com = f.sigma_threshold(ph, "indep"), f.sigma_threshold(ph, "common")
    assert abs(s_ind - 0.710) < 0.005 and abs(s_com - 1.319) < 0.005
    assert abs(f.accel_phase_sigma(B["m"], B["dx"], B["tau"], 1.0) - B["m"] * B["dx"] / g.HBAR * np.sqrt(1.25)) < 1e6


def test_split_force():
    assert abs(f.max_split(1e-14, 0.5) * 1e6 - 115.9) < 0.1


def test_em_fakes():
    assert f.em_entangling_ratio(1.5e-14, 721e-6, GAP, 3.24, q=f.E_CH) > 1e10
    p = f.max_dipole(1.5e-14, 721e-6, GAP, 3.24)
    assert abs(f.em_entangling_ratio(1.5e-14, 721e-6, GAP, 3.24, p=p) - 0.1) < 1e-3


def test_coarse_design_search():
    dphi_grid = np.linspace(0, np.pi, 61)
    gt_grid = np.linspace(0, 0.8, 41)
    table = (dphi_grid, gt_grid, f.runs_table(dphi_grid, gt_grid))
    args = (np.geomspace(3e-15, 5e-14, 9), np.geomspace(100e-6, 2e-3, 9),
            np.geomspace(0.05, 5, 9), np.geomspace(0.2, 3, 9), GAP, table)
    env = dict(P=1e-15, T_env=0.15, T_int=0.15, im_K=0.01, asd=0.0, T2=1e9, m_gas=g.M_N2)
    assert f.design_search(env, *args) is not None
    assert f.design_search({**env, "P": 1e-14}, *args) is None
    assert f.design_search({**env, "asd": f.LPF_ASD}, *args) is None
    assert f.design_search({**env, "P": 1e-17}, *args)["runs"] >= f.MIN_RUNS
