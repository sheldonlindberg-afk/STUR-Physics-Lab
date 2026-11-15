"""Pins src/chain_branches.py: the four branches of the force chain (FORCE_CHAIN.md)."""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import chain_branches as CB
import ladder_links as LL

A0 = 1 / 137.035999084
MPL = 1.220890e19                                   # GeV


def test_w_mass_tree_running_top():
    w = CB.w_mass(A0, LL.G_F_GEV)
    assert abs(w["tree"] - 80.939) < 0.003 and abs(w["running"] - 79.961) < 0.003
    assert abs(w["top"] - 80.531) < 0.003 and abs(w["top + QCD"] - 80.474) < 0.003
    assert abs(w["Delta rho"] - 0.00933) < 1e-5
    # the running alone overshoots downward; the top brings it back to within 0.2% of the measurement
    assert w["running"] < CB.M_W_MEAS[0] < w["top + QCD"] < w["tree"]
    assert abs(w["top + QCD"] / CB.M_W_MEAS[0] - 1) < 0.0015
    # with no running and no top the formula is the tree-level relation
    s2 = 1 - (w["tree"] / LL.M_Z) ** 2
    assert abs(s2 * (1 - s2) - math.pi * A0 / (math.sqrt(2) * LL.G_F_GEV * LL.M_Z**2)) < 1e-12


def test_neutron_phase_space_and_lifetime():
    assert abs(CB.phase_space(coulomb=False) - 1.6361) < 2e-4       # the textbook value without Coulomb
    assert abs(CB.phase_space() / 1.6887 - 1) < 0.003               # literature value with the full Fermi function
    tree, tau, err = CB.neutron_lifetime(LL.G_F_GEV, LL.V_UD[0])
    assert abs(tree - 913.2) < 0.5 and abs(tau - 880.6) < 0.1 and abs(err - 1.6) < 0.1
    assert abs(tau - CB.TAU_N_MEAS[0]) < 2 * math.hypot(err, CB.TAU_N_MEAS[1])
    assert 0.03 < tree / tau - 1 < 0.045                            # radiative corrections: about 4%


def test_expansion_and_freeze_out():
    h = CB.helium(880.6, MPL, A0, network=False)
    assert abs(h["T_nu/T"] - (4 / 11) ** (1 / 3)) < 1e-4            # entropy conservation through e+ e- annihilation
    assert abs(h["t(T = 1 MeV)"] - 0.746) < 0.01 and abs(h["t(T = 0.1 MeV)"] - 119) < 2
    assert abs(h["X_n at freeze-out"] - 0.160) < 0.002


def test_helium_and_its_sensitivities():
    h = CB.helium(880.6, MPL, A0)
    assert abs(h["Y_p"] - 0.2407) < 0.001 and abs(h["baryons"] - 1) < 1e-8
    assert abs(h["Y_p"] - CB.YP_MEAS[0]) < 0.006                    # a minimal network: within 2%
    assert 60e-3 < h["T at half helium"] < 80e-3
    assert abs(2 * h["X_n when helium forms"] - h["Y_p"]) < 0.002   # helium takes every neutron left
    assert 1.5 < h["D/H"] / CB.DH_MEAS[0] < 2.5                     # known limit: too much deuterium left
    for kw in (dict(s_dd=2 * CB.S_DD), dict(s_dd=CB.S_DD / 2)):     # helium barely depends on the nuclear inputs
        assert abs(CB.helium(880.6, MPL, A0, **kw)["Y_p"] - h["Y_p"]) < 0.003
    stronger = CB.helium(880.6, MPL / math.sqrt(1.1), A0)["Y_p"]    # G 10% larger: faster expansion, more helium
    assert 0.006 < stronger - h["Y_p"] < 0.011


def test_lane_emden_and_chandrasekhar():
    x1, om = CB.lane_emden(3)
    assert abs(x1 - 6.89685) < 1e-5 and abs(om - 2.01824) < 1e-5
    x1, om = CB.lane_emden(1)                                       # exact: theta = sin(xi)/xi
    assert abs(x1 - math.pi) < 1e-7 and abs(om - math.pi) < 1e-6
    assert abs(CB.chandrasekhar_number() - 3.0980) < 1e-3


def test_oppenheimer_volkoff_and_the_neutron_star():
    import black_holes as BH
    m, r, xc = CB.oppenheimer_volkoff_number()
    assert abs(m - 0.3843) < 5e-4
    assert CB.ov_star(0.5)[0] < m > CB.ov_star(1.4)[0]              # a true maximum
    s = CB.collapse_limits(MPL, LL.G_NEWTON, BH.GM_SUN)
    assert abs(s["M_Ch"] - 1.456) < 0.002 and abs(s["M_OV"] - 0.710) < 0.002
    assert abs(s["M_Pl^3/m_n^2"] - 1.848) < 0.002 and 2.1e57 < s["nucleons"] < 2.3e57
    assert CB.M_NS_MEAS[0] - 3 * CB.M_NS_MEAS[1] > 2.5 * s["M_OV"]  # the measured star needs more than Pauli pressure
    assert min(BH.GW_M1, BH.GW_M2) > 10 * s["M_OV"]


def test_electron_moment_series_inverts_to_the_published_alpha():
    assert abs(CB.alpha_from_a_e() - CB.AINV_FROM_AE[0]) < CB.AINV_FROM_AE[1] / 5
    assert abs(CB.a_e(CB.AINV_FROM_AE[0]) - CB.A_E_MEAS[0]) < CB.A_E_MEAS[1] / 5
    x = 1 / (137.036 * math.pi)                                     # Schwinger's term is 99.85% of it
    assert abs(0.5 * x / CB.a_e(137.036) - 1.0015) < 2e-4


def test_weak_angle_runs_to_the_measured_low_energy_value():
    assert CB.mixing_lambda(CB.LEPTONS) == 0.25
    assert abs(CB.mixing_lambda(CB.QUARKS5) - 21 / 44) < 1e-15
    assert abs(CB.mixing_lambda(CB.LEPTONS + CB.QUARKS5 + [(3, 2 / 3, 0.5)]) - 3 / 8) < 1e-15   # the unified value
    s0, lep, had = CB.weak_angle_at_zero(LL.DALPHA_LEP_3LOOP, LL.DALPHA_HAD[0])
    assert abs(s0 - CB.S2_ZERO_PDG[0]) < 3e-5 and had > 10 * lep > 0
    assert abs(s0 - CB.S2_QWEAK[0]) < CB.S2_QWEAK[1]
    assert (CB.S2_QWEAK[0] - CB.S2_MZ[0]) / CB.S2_QWEAK[1] > 6      # the running is seen


def test_w_mass_with_the_complete_correction():
    w = CB.w_mass(A0, LL.G_F_GEV)
    assert abs(w["full"] - CB.M_W_MEAS[0]) < 0.02                   # the PDG's Delta r closes the gap


def test_mass_difference_controls_lifetime_and_helium():
    (mu, _), (md, _) = CB.M_U_D
    L = CB.DM_NP_LATTICE
    assert abs(L["QCD"][0] + L["QED"][0] - L["total"][0]) < 0.02 and abs((md - mu) - L["QCD"][0]) < 0.1
    assert abs(L["total"][0] - CB.DM_NP) < L["total"][1]
    rows = CB.splitting_consequences(LL.G_F_GEV, LL.V_UD[0], MPL, A0, (CB.DM_NP, 1.01 * CB.DM_NP))
    assert abs(rows[0][2] - 880.6) < 0.1 and abs(rows[0][3] - 0.2407) < 0.001
    assert 5.5 < (rows[0][2] / rows[1][2] - 1) * 100 < 8            # 1% in delta: about 6.7% in the lifetime
    slope = (rows[1][3] - rows[0][3]) / (0.01 * CB.DM_NP)
    assert -0.65 < slope < -0.57
