#!/usr/bin/env python3
"""
STUR Physics Lab: production simulation v2.

One self-contained script. Python 3.8+, standard library only. Copy it, paste it
into any Python runner, notebook or AI assistant's code tool, and run it.

THE RULE: NOTHING IN THIS FILE IS TUNED OR FITTED.
  * Every measured number is in INPUTS, with its uncertainty and its source.
  * Every measured number used only to judge the results is in COMPARISONS. Those
    never enter a calculation.
  * Every numerical-method setting (step counts, grid sizes, precision) is in
    NUMERICS. The self-checks show the results do not depend on them.
  * Everything else is calculated: group-theory coefficients from Casimirs and
    field content, quark masses from the renormalization group, the quark-mixing
    matrix from an exact diagonalization, and the cosmology from the Friedmann
    equation.
  * Where the inputs cannot fix a quantity (the two phases of the quark mass
    matrices), the script does not choose a value. It scans the whole range,
    and the prediction is the band the scan sweeps out.
  tests/test_production.py enforces the rule: it fails if a non-integer number
  appears anywhere outside INPUTS, COMPARISONS and NUMERICS.

WHAT IT CALCULATES
  Part A, cosmology (flat LambdaCDM): the radiation density from the CMB
    temperature, the dark-energy density from flatness, the age of the universe,
    the deceleration parameter, the redshift where the expansion starts to
    accelerate, matter-radiation equality, and the horizon entropies.
  Part B, quark flavour: the six quark masses run with the renormalization group
    (two-loop QCD, one-loop QED, then one-loop Standard Model Yukawa and gauge
    running above the top mass) to m_t(m_t) and to the superpartner scale that
    Part I derives. They are then
    put into the Fritzsch six-zero texture, whose entries the masses fix exactly.
    Diagonalizing it gives the full CKM matrix for every value of the two free
    phases, and each element's band is compared with the measured value.
  Part C, every texture-zero pattern that makes a prediction: all pairs of
    Hermitian quark mass matrices with five or six zeros, grouped into classes
    under weak-basis permutations. Each sector's entries are solved exactly from
    its masses. Every unknown is scanned or tested, never fixed, and each class
    is judged against the measured CKM matrix.
  Part D, what the 3-3-1 gauge symmetry says about the mass matrices: the
    charges, the gauge-invariant Yukawa operators, and which entries they allow,
    for beta = -1/sqrt3 and +1/sqrt3.
  Part E, whether a flavour symmetry inside 3-3-1 can produce the surviving
    texture: an exhaustive scan of abelian Z_N charge assignments with the
    minimal scalars, a search for the fewest extra scalar triplets that give
    the survivor's zeros, and a parameter count of the model that results.
  Part H, where quantum theory and gravity meet: Planck units, the one-loop
    quantum correction to Newton's law, Hawking and de Sitter horizons, the
    Unruh effect, gravity-mediated entanglement, the logarithmic origin of the
    proton/Planck hierarchy, and the large dimensionless numbers with their status.
  Part I, whether alpha can be calculated from the other numbers: grand
    unification of the three gauge couplings at one and two loops, for the SM
    and the MSSM with its unknown superpartner scale scanned, plus a test of the
    closed formulas proposed for 1/alpha.
  Part F, whether ANY zero pattern of general mass matrices predicts the CKM
    matrix: the exact number of physical parameters of all 61,009 pattern pairs,
    from the rank of the Jacobian of 10 weak-basis invariants. Every rank is proved
    (an exact lower bound meets a symmetry upper bound) and J = 0 is proved by
    symbolic expansion where it holds.
  Parts N, O, P, what is left: closed mass formulas (Koide) at pole and running masses; the
    strong CP angle (its bound from the neutron EDM via the chiral logarithm, and the massless
    up quark, axion and parity explanations); neutrino masses (the lightest mass and Majorana
    phases scanned, against cosmology, KATRIN and KamLAND-Zen) and mixing patterns from discrete
    symmetries, with the unknowns of the corrected patterns solved exactly.
  Part M, which high-energy hypothesis survives: the SM up to M_P and the MSSM
    above M_S (its unknowns scanned), each against every combination of gauge
    unification, b-tau unification and the Higgs mass. None is chosen in advance.

THE MODEL AS ONE ALGORITHM
  The parts run as named stages (STAGES). Every read of a measured input and of
  another stage's result is recorded, and the report prints the graph the run
  followed, each stage's evidence level and assumptions, which stages each input
  reaches, whether the stages' assumptions are compatible, and the audit findings.
  --set NAME=VALUE changes a measured input and recalculates the whole model.

Run:  python3 production_v2_2.py                 (full report, about 7 minutes)
      python3 production_v2_2.py --json-out out.json
      python3 production_v2_2.py --set M_t=173.5   (change an input, recalculate everything)
"""

from __future__ import annotations

import argparse
import cmath
from decimal import Decimal, localcontext
from fractions import Fraction as Fr
import itertools
import json
import math
import sys
import time
from typing import Any, Callable, Dict, List, Sequence, Tuple

VERSION = "production v2.2"

# =============================================================================
# 1. MEASURED INPUTS (the only physics numbers that enter a calculation)
# =============================================================================
# Values are strings so that the high-precision cosmology sees them exactly.
INPUTS: Dict[str, Dict[str, str]] = {
    # --- SI defining constants (exact) and astronomical unit (exact, IAU 2012)
    "c": {"value": "299792458", "sigma": "0", "unit": "m/s", "source": "SI, exact"},
    "h": {"value": "6.62607015e-34", "sigma": "0", "unit": "J s", "source": "SI, exact"},
    "k_B": {"value": "1.380649e-23", "sigma": "0", "unit": "J/K", "source": "SI, exact"},
    "au": {"value": "149597870700", "sigma": "0", "unit": "m", "source": "IAU 2012, exact"},
    "G": {"value": "6.67430e-11", "sigma": "0.00015e-11", "unit": "m^3/(kg s^2)",
          "source": "CODATA 2018"},
    # --- cosmology
    "T_CMB": {"value": "2.7255", "sigma": "0.0006", "unit": "K", "source": "Fixsen 2009 (COBE/FIRAS)"},
    "N_eff": {"value": "3.044", "sigma": "0", "unit": "",
              "source": "Standard Model calculation of N_eff (Bennett et al. 2021); not measured"},
    "H0": {"value": "67.36", "sigma": "0.54", "unit": "km/s/Mpc",
           "source": "Planck 2018 VI, TT,TE,EE+lowE+lensing"},
    "Omega_m": {"value": "0.3153", "sigma": "0.0073", "unit": "",
                "source": "Planck 2018 VI, TT,TE,EE+lowE+lensing"},
    "Omega_b_h2": {"value": "0.02237", "sigma": "0.00015", "unit": "",
                   "source": "Planck 2018 VI, table 2, TT,TE,EE+lowE+lensing (Part S)"},
    # --- electroweak
    "G_F": {"value": "1.1663788e-5", "sigma": "0.0000006e-5", "unit": "GeV^-2", "source": "PDG 2024"},
    "M_Z": {"value": "91.1876", "sigma": "0.0021", "unit": "GeV", "source": "PDG (LEP Z pole)"},
    "M_W": {"value": "80.3692", "sigma": "0.0133", "unit": "GeV", "source": "PDG 2024, world average (pole)"},
    "alpha_em_inv_MZ": {"value": "127.951", "sigma": "0.009", "unit": "",
                        "source": "PDG 2024, MS-bar at M_Z"},
    "delta_alpha_had5": {"value": "0.02783", "sigma": "0.00006", "unit": "",
                         "source": "PDG 2024, Electroweak review: Delta alpha_had^(5)(M_Z) (Part W)"},
    # --- QCD
    "alpha_s_MZ": {"value": "0.1180", "sigma": "0.0009", "unit": "", "source": "PDG 2024"},
    # --- quark masses: u, d, s MS-bar at 2 GeV; c, b MS-bar at their own mass; t pole (direct)
    "m_u": {"value": "0.00216", "sigma": "0.00007", "unit": "GeV", "source": "PDG 2024, MS-bar(2 GeV)"},
    "m_d": {"value": "0.00470", "sigma": "0.00007", "unit": "GeV", "source": "PDG 2024, MS-bar(2 GeV)"},
    "m_s": {"value": "0.0935", "sigma": "0.0008", "unit": "GeV", "source": "PDG 2024, MS-bar(2 GeV)"},
    "mu_light": {"value": "2", "sigma": "0", "unit": "GeV", "source": "PDG convention for u, d, s"},
    "m_c": {"value": "1.2730", "sigma": "0.0046", "unit": "GeV", "source": "PDG 2024, m_c(m_c)"},
    "m_b": {"value": "4.183", "sigma": "0.007", "unit": "GeV", "source": "PDG 2024, m_b(m_b)"},
    "M_t": {"value": "172.57", "sigma": "0.29", "unit": "GeV", "source": "PDG 2024, direct measurements"},
    "s2_hat_Z": {"value": "0.23129", "sigma": "0.00004", "unit": "",
                 "source": "PDG 2024 (rev. April 2024) global fit, MS-bar sin^2 theta_W(M_Z)"},
    # --- atomic and astronomical constants (Part H)
    "e_charge": {"value": "1.602176634e-19", "sigma": "0", "unit": "C", "source": "SI, exact"},
    "alpha_em": {"value": "7.2973525693e-3", "sigma": "0.0000000011e-3", "unit": "",
                 "source": "CODATA 2018, fine-structure constant at zero momentum"},
    "m_p": {"value": "1.67262192369e-27", "sigma": "0.00000000051e-27", "unit": "kg", "source": "CODATA 2018"},
    "m_e": {"value": "9.1093837015e-31", "sigma": "0.0000000028e-31", "unit": "kg", "source": "CODATA 2018"},
    "m_mu_MeV": {"value": "105.6583755", "sigma": "0.0000023", "unit": "MeV", "source": "PDG 2024 (pole)"},
    "m_tau_MeV": {"value": "1776.93", "sigma": "0.09", "unit": "MeV", "source": "PDG 2024 (pole)"},
    "GM_sun": {"value": "1.3271244e20", "sigma": "0", "unit": "m^3/s^2", "source": "IAU 2015 B3, nominal (exact)"},
    "GM_earth": {"value": "3.986004418e14", "sigma": "0.000000008e14", "unit": "m^3/s^2", "source": "IERS 2010"},
    "R_earth": {"value": "6378137", "sigma": "0", "unit": "m", "source": "WGS 84 equatorial radius (defined)"},
    "m_pi_MeV": {"value": "139.57039", "sigma": "0.00018", "unit": "MeV", "source": "PDG 2024, charged pion"},
    # --- hadronic inputs of the strong CP angle (Part O)
    "m_pi0_MeV": {"value": "134.9768", "sigma": "0.0005", "unit": "MeV", "source": "PDG 2024, neutral pion"},
    "m_n": {"value": "1.67492749804e-27", "sigma": "0.00000000095e-27", "unit": "kg", "source": "CODATA 2018"},
    "f_pi_MeV": {"value": "130.2", "sigma": "0.8", "unit": "MeV",
                 "source": "PDG 2024, f_pi+ (130 MeV normalization; F_pi = f_pi/sqrt2)"},
    "g_A": {"value": "1.2754", "sigma": "0.0013", "unit": "", "source": "PDG 2024, |lambda| = |g_A/g_V|"},
    "delta_mN_QCD_MeV": {"value": "2.49", "sigma": "0.17", "unit": "MeV",
                         "source": "strong (quark-mass) part of m_n - m_p, lattice QCD average: de Vries, "
                                   "Mereghetti, Walker-Loud 2015 (arXiv:1506.06247), eq. 118"},
    "d_n_limit": {"value": "1.8e-26", "sigma": "0", "unit": "e cm",
                  "source": "Abel et al. 2020 (PSI), PRL 124, 081803: |d_n| < 1.8e-26 e cm, 90% CL"},
    # --- proton decay (Part Q): lattice matrix elements (stat and syst errors combined in quadrature)
    "W_pi0_RL": {"value": "-0.131", "sigma": "0.0136", "unit": "GeV^2",
                 "source": "<pi0|(ud)_R u_L|p>, MS-bar NDR at 2 GeV: Aoki, Izubuchi, Shintani, Soni 2017 "
                           "(arXiv:1705.01338), table 4: -0.131(4)(13)"},
    "W_pi0_LL": {"value": "0.134", "sigma": "0.0168", "unit": "GeV^2",
                 "source": "<pi0|(ud)_L u_L|p>, same: 0.134(5)(16)"},
    "V_ud": {"value": "0.97367", "sigma": "0.00032", "unit": "", "source": "PDG 2024, superallowed beta decays"},
    "CKM_lambda": {"value": "0.22501", "sigma": "0.00068", "unit": "", "source": "PDG 2024 CKM fit, Wolfenstein lambda"},
    "CKM_A": {"value": "0.826", "sigma": "0.0155", "unit": "", "source": "PDG 2024 CKM fit: +0.016 -0.015"},
    "CKM_rhobar": {"value": "0.1591", "sigma": "0.0094", "unit": "", "source": "PDG 2024 CKM fit"},
    "CKM_etabar": {"value": "0.3523", "sigma": "0.0072", "unit": "", "source": "PDG 2024 CKM fit: +0.0073 -0.0071"},
    "alpha_p_lattice": {"value": "-0.0144", "sigma": "0.0021", "unit": "GeV^3",
                        "source": "Aoki, Izubuchi, Shintani, Soni 2017 (arXiv:1705.01338), eq. 23: -0.0144(3)(21)"},
    "beta_p_lattice": {"value": "0.0144", "sigma": "0.0021", "unit": "GeV^3", "source": "same: 0.0144(3)(21)"},
    "baryon_D": {"value": "0.80", "sigma": "0", "unit": "", "source": "chiral Lagrangian D, as used by Hisano et al. 2013"},
    "baryon_F": {"value": "0.47", "sigma": "0", "unit": "", "source": "chiral Lagrangian F, as used by Hisano et al. 2013"},
    "m_K_MeV": {"value": "493.677", "sigma": "0.015", "unit": "MeV", "source": "PDG 2024, charged kaon"},
    "m_Sigma0_MeV": {"value": "1192.642", "sigma": "0.024", "unit": "MeV", "source": "PDG 2024"},
    "m_Lambda_MeV": {"value": "1115.683", "sigma": "0.006", "unit": "MeV", "source": "PDG 2024"},
    # --- neutrino oscillations (Part P): NuFIT 6.0 (arXiv:2410.05380, JHEP 12 (2024) 216), global fit
    # IC24 with SK atmospheric data; asymmetric 1 sigma errors symmetrized (mean of the two sides).
    # Delta m^2_3l = Delta m^2_31 > 0 for normal ordering (NO), Delta m^2_32 < 0 for inverted (IO).
    "nu_s12sq": {"value": "0.308", "sigma": "0.0115", "unit": "", "source": "NuFIT 6.0 (NO and IO): +0.012 -0.011"},
    "nu_dm21": {"value": "7.49e-5", "sigma": "0.19e-5", "unit": "eV^2", "source": "NuFIT 6.0 (NO and IO)"},
    "nu_s13sq_NO": {"value": "0.02215", "sigma": "0.00057", "unit": "", "source": "NuFIT 6.0 NO: +0.00056 -0.00058"},
    "nu_s23sq_NO": {"value": "0.470", "sigma": "0.015", "unit": "", "source": "NuFIT 6.0 NO: +0.017 -0.013"},
    "nu_delta_NO": {"value": "212", "sigma": "33.5", "unit": "deg",
                    "source": "NuFIT 6.0 NO: +26 -41 (far from Gaussian; 3 sigma range 124 to 364)"},
    "nu_dm3l_NO": {"value": "2.513e-3", "sigma": "0.020e-3", "unit": "eV^2",
                   "source": "NuFIT 6.0 NO, Delta m^2_31: +0.021 -0.019"},
    "nu_s13sq_IO": {"value": "0.02231", "sigma": "0.00056", "unit": "", "source": "NuFIT 6.0 IO: +-0.00056"},
    "nu_s23sq_IO": {"value": "0.550", "sigma": "0.0135", "unit": "", "source": "NuFIT 6.0 IO: +0.012 -0.015"},
    "nu_delta_IO": {"value": "274", "sigma": "23.5", "unit": "deg",
                    "source": "NuFIT 6.0 IO: +22 -25 (3 sigma range 201 to 335)"},
    "nu_dm3l_IO": {"value": "-2.484e-3", "sigma": "0.020e-3", "unit": "eV^2",
                   "source": "NuFIT 6.0 IO, Delta m^2_32: +-0.020"},
}

# The measured inputs whose uncertainties are propagated into the flavour bands.
FLAVOUR_UNCERTAIN = ("m_u", "m_d", "m_s", "m_c", "m_b", "M_t", "alpha_s_MZ")
COSMO_UNCERTAIN = ("H0", "Omega_m", "T_CMB")

# =============================================================================
# 2. COMPARISONS (measured results; used only to judge the output)
# =============================================================================
# (value, +sigma, -sigma)
COMPARISONS: Dict[str, Dict[str, Any]] = {
    "V_us": {"value": ("0.22501", "0.00068", "0.00068"), "source": "PDG 2024 CKM global fit, eq. 12.27"},
    "V_cb": {"value": ("0.04183", "0.00079", "0.00069"), "source": "PDG 2024 CKM global fit, eq. 12.27"},
    "V_ub": {"value": ("0.003732", "0.000090", "0.000085"), "source": "PDG 2024 CKM global fit, eq. 12.27"},
    "J": {"value": ("3.12e-5", "0.13e-5", "0.12e-5"), "source": "PDG 2024 CKM global fit"},
    "V_td/V_ts": {"value": ("0.207", "0.0032", "0.0032"),
                  "source": "PDG 2024 eq. 12.14, from Delta m_d / Delta m_s: "
                            "0.207 +/- 0.001 +/- 0.003, the two errors combined in quadrature"},
    "age_Gyr": {"value": ("13.787", "0.020", "0.020"), "source": "Planck 2018 VI, TT,TE,EE+lowE+lensing"},
    "Omega_Lambda": {"value": ("0.6847", "0.0073", "0.0073"), "source": "Planck 2018 VI, TT,TE,EE+lowE+lensing"},
    "m_h": {"value": ("125.20", "0.11", "0.11"), "source": "PDG 2024, Higgs boson mass (combined)"},
    # lower limits (Part Q): the value is the limit, the sigmas are zero
    "tau_p_e_pi0": {"value": ("2.4e34", "0", "0"),
                    "source": "Super-Kamiokande, Takenaka et al. 2020 (PRD 102, 112011): tau/B(p -> e+ pi0), "
                              "years, 90% CL"},
    "tau_p_K_nu": {"value": ("5.9e33", "0", "0"),
                   "source": "Super-Kamiokande, Abe et al. 2014 (PRD 90, 072005): tau/B(p -> nubar K+), "
                             "years, 90% CL"},
    "M_W_noCDF": {"value": ("80.360", "0.012", "0.012"),
                  "source": "PDG 2024, Electroweak review eq. 10.63: average without CDF II"},
    "M_W_SM_fit": {"value": ("80.353", "0.006", "0.006"),
                   "source": "PDG 2024, Electroweak review: global SM fit without the M_W measurements"},
    "sin2_eff_LEP_SLC": {"value": ("0.23151", "0.00016", "0.00016"),
                         "source": "PDG 2024, Electroweak review: sin^2 theta_eff^lept, LEP + SLC"},
    "sin2_eff_colliders": {"value": ("0.23149", "0.00013", "0.00013"),
                           "source": "PDG 2024, Electroweak review: sin^2 theta_eff^lept, hadron-collider average"},
    "Omega_c_h2": {"value": ("0.1200", "0.0012", "0.0012"),
                   "source": "Planck 2018 VI, table 2, TT,TE,EE+lowE+lensing (Part V)"},
    # upper limits (Part P): the value is the limit, the sigmas are zero
    "sum_mnu_Planck": {"value": ("0.12", "0", "0"),
                       "source": "Planck 2018 VI, TT,TE,EE+lowE+lensing+BAO, 95% upper limit (LambdaCDM)"},
    "sum_mnu_DESI": {"value": ("0.064", "0", "0"),
                     "source": "DESI DR2 BAO + CMB (arXiv:2503.14738), 95% upper limit (LambdaCDM)"},
    "m_beta_KATRIN": {"value": ("0.45", "0", "0"), "source": "KATRIN 2025, Science 388, 180: 90% CL"},
    "m_bb_KLZ_low": {"value": ("0.028", "0", "0"),
                     "source": "KamLAND-Zen 2025 (arXiv:2406.11438, PRL 135, 262501): 90% CL, most favourable "
                               "nuclear matrix element"},
    "m_bb_KLZ_high": {"value": ("0.122", "0", "0"),
                      "source": "KamLAND-Zen 2025: 90% CL, least favourable nuclear matrix element"},
}

# =============================================================================
# 3. NUMERICS (method settings only; the self-checks vary them)
# =============================================================================
NUMERICS: Dict[str, Any] = {
    "precision_digits": 50,           # Decimal digits for the cosmology
    "romberg_max_levels": 22,
    "romberg_rel_tol": "1e-30",
    "friedmann_check_steps": 20000,   # independent float quadrature of the age
    "friedmann_check_lna_min": -40,
    "rg_steps_per_efold": 200,        # RK4 steps per unit of ln(mu)
    "phase_grid": 120,                # coarse grid per phase (both phases in [0, 2 pi))
    "pattern_search_min_step": "1e-12",
    "jacobi_tol": "1e-30",
    "check_rel_tol": "1e-9",
    "check_lit_tol": "1e-4",          # two units of the last digit the literature prints (Part L checks)
    "check_lit_b4_tol": "1e-6",       # B4 is printed to six decimals
    "check_rg_tol": "1e-7",
    "check_age_tol": "1e-8",
    "survey_min_zeros": 5,            # 5 or 6 zeros: the patterns with at least one prediction
    "survey_curve_grid": 24,          # starting grid along a one-parameter family
    "survey_phase_grid": 16,          # starting grid per phase
    "survey_starts": 3,               # best grid points refined by compass search
    "survey_sigma_iterations": 3,     # re-evaluations of the input-induced errors at the point found
    "survey_min_step": "1e-9",
    "survey_residual_tol": "1e-6",    # relative mismatch of trace, minors, det for an accepted matrix
    "check_survey_eig_tol": "1e-6",   # float cancellation in hierarchical matrices; masses are known to ~1e-2
    "root_trim_rel": "1e-14",
    "root_merge_rel": "1e-13",
    "survival_sigma": 3,              # a pattern survives if its p-value is above the 3-sigma level
    "cert_round_rel": "1e-12",        # Part C certificates: outward widening of interval bounds (rounding)
    "cert_eval_rel": "1e-14",         # Part C certificates: rounding of one polynomial evaluation, relative
    "cert_min_width": "1e-12",        # Part C certificates: narrowest cell along a family
    "cert_budget": 1000000,           # Part C certificates: cells per variant before giving up
    "check_survey_tol": "1e-6",
    "symmetry_max_N": 6,              # Z_N searched exhaustively for N = 2 .. this
    "joint_ms_points": 20,            # Part M: grid in ln M_S from m_t(m_t) to Part I's scan top
    "joint_tan_beta_points": 20,      # Part M: grid in ln tan(beta) over its perturbative range
    "joint_bisections": 20,           # Part M: bisection steps for b-tau roots and perturbativity edges
    "joint_chi2_zero": "1e-6",        # Part M: a chi^2 below this is bisection residue, printed as 0
    "closure_seed": 20261123,         # integer points for the exact Jacobian ranks (any seed works)
    "closure_points": 2,              # points per pattern; the largest rank found is kept
    "unif_step": "0.02",              # RK4 step in ln(mu) for the gauge running
    "unif_bracket_lo": 20,            # search interval for 1/alpha(M_Z)
    "unif_bracket_hi": 200,
    "unif_iterations": 60,
    "unif_ms_deriv_step": "0.05",     # step in ln(M_S) for the slope
    "unif_tol": "1e-7",
    "unif_grid_points": 8,            # M_S scan: geometric grid from M_Z to the SM unification point
    "yukawa_tan_beta_points": 16,     # tan(beta) scan: geometric grid between its perturbative bounds
    "higgs_xt_points": 13,            # stop-mixing grid X_t/M_S from 0 to sqrt(12) (Part K)
    "higgs_ms_search_efolds": 40,     # search range in ln(M_S) above m_t for the backwards reading
    "higgs_iterations": 50,           # bisection steps for that reading
    "crit_tol": "1e-10",              # relative tolerance of the root solves (Part L)
    "crit_iterations": 40,
    "crit_steps_per_efold": 50,       # RK4 steps per e-fold for Part L's runs to the Planck scale
    "check_b0_points": 200000,       # midpoint quadrature points for the B0 check
    "check_b0_tol": "1e-5",          # (the integrand has integrable log singularities above threshold)
    "crit_yt_step": "1e-2",           # first relative step in y_t when bracketing beta_lambda = 0
    "check_fd_rel_step": "1e-5",      # finite-difference step for the first-law check
    "check_fd_tol": "1e-8",
    "nu_m0_min": "1e-5",              # Part P: smallest lightest-neutrino mass on the grid (eV); 0 is also used
    "nu_m0_points": 25,               # Part P: geometric grid of the lightest mass up to the cosmology limit
    "nu_phase_grid": 360,             # Part P: grid of the free phase of a corrected pattern, then bisection
    "nu_bisections": 80,
    "check_phase_grid": 96,           # Part P check: brute-force Majorana phases against the exact band
    "proton_phase_grid": 36,          # Part Q: grid per unknown GUT phase (phi_2, phi_3) for the dimension-five band
    "check_axion_tol": "0.05",        # Part V: eq. 170 is an approximation (their words); agreement within 5 %
    "heavy_mass_spread": 10,          # Part T8: each heavy GUT multiplet's mass within this factor of M_GUT (assumed)
    "potential_seed": 20261125,       # Part T9: any seed works; the scan is deterministic
    "potential_points": 30000,        # Parts T9-T11: coupling points tried
    "potential_lambda_max": 1,        # Part T9: |lambda_a| (normalized quartics) at most this (perturbative box, assumed)
    "potential_eta_max": 1,           # Part T9: |eta / v| at most this (assumed)
    "potential_directions": 32,       # Part T9: random directions for the bounded-below test
    "yukawa_fit_mass_rel": "0.01",    # Part Y: tolerance on the fitted lepton masses (one-loop running at M_GUT)
    "yukawa_ratio_theory_rel": "0.02",  # Part Y: floor on the error of a lepton/down mass ratio at M_I (running)
    "yukawa_fit_starts": 600,         # Part Y: seeded starts of the sum-rule search (half structured)
    "yukawa_fit_evals": 60000,        # Part Y: evaluation budget per start
    "yukawa_fit_polish": 12,          # Part Y: best starts refined by iterated local search
    "yukawa_fit_kicks": 25,           # Part Y: random kicks per refined start
    "yukawa_nu_seeds": 3,             # Part Y3: charged-lepton solutions the type-II fit starts from
    "yukawa_nu_kicks": 4,             # Part Y3: kicks per type-II start
    "yukawa_fit_min_step": "1e-6",    # Part Y: smallest compass step (in log-magnitudes and phases)
    "threshold_band": 1,              # Part T7: largest one-loop threshold per matching condition, in 1/alpha (an
                                      # assumption: one heavy multiplet with b ~ 2 a factor e off gives ~0.3)
    "report_sci_below": "1e-3",       # print in scientific notation below / above these
    "report_sci_above": "1e5",
}
# Scales are never typed in: Parts B and C are evaluated at m_t(m_t) and at the superpartner
# scale M_S that Part I derives; Part J uses the unification scales it computes and M_Planck.


# =============================================================================
# 3a. LITERATURE (published calculations the script quotes instead of repeating)
# =============================================================================
# Coefficients of calculations too long to reproduce here, each with its source. They
# are neither measured nor tuned. Self-checks reproduce published results with them.
# Rational coefficients are written as fractions; the others are as printed in the source.
LITERATURE: Dict[str, Dict[str, Any]] = {
    "sm_beta_3loop": {
        "source": "Buttazzo et al. 2013 (arXiv:1307.3536v2), appendix B: three-loop terms of the SM RGEs "
                  "(Mihaila-Salomon-Steinhauser; Chetyrkin-Zoller; Bednyakov et al.), for d/d ln(mu^2), "
                  "times (4 pi)^-6; y_b, y_tau neglected at three loops. Each term: (coefficient, powers of "
                  "lambda, y_t^2, g3^2, g2^2, g1^2), multiplying g1^4, g2^4, g3^4, y_t^2 or 1.",
        "value": {
             "g1": ["g1^4", [("189/16",0,2,0,0,0),("-29/5",0,1,1,0,0),("-471/32",0,1,0,1,0),("-2827/800",0,1,0,0,1),
                    ("-9/5",2,0,0,0,0),("9/10",1,0,0,1,0),("27/50",1,0,0,0,1),
                    ("297/5",0,0,2,0,0),("789/64",0,0,0,2,0),("-388613/24000",0,0,0,0,2),("-3/5",0,0,1,1,0),
                    ("-137/75",0,0,1,0,1),("123/160",0,0,0,1,1)]],
             "g2": ["g2^4", [("147/16",0,2,0,0,0),("-7",0,1,1,0,0),("-729/32",0,1,0,1,0),("-593/160",0,1,0,0,1),
                    ("-3",2,0,0,0,0),("3/2",1,0,0,1,0),("3/10",1,0,0,0,1),
                    ("81",0,0,2,0,0),("324953/1728",0,0,0,2,0),("-5597/1600",0,0,0,0,2),("39",0,0,1,1,0),
                    ("-1/5",0,0,1,0,1),("873/160",0,0,0,1,1)]],
             "g3": ["g3^4", [("15",0,2,0,0,0),("-40",0,1,1,0,0),("-93/8",0,1,0,1,0),("-101/40",0,1,0,0,1),
                    ("65/2",0,0,2,0,0),("109/8",0,0,0,2,0),("-523/120",0,0,0,0,2),("21",0,0,1,1,0),
                    ("77/15",0,0,1,0,1),("-3/40",0,0,0,1,1)]],
             "yt": ["yt^2", [("58.6028",0,3,0,0,0),("198",1,2,0,0,0),("-157",0,2,1,0,0),("-1593/16",0,2,0,1,0),("-2437/80",0,2,0,0,1),
                    ("15/4",2,1,0,0,0),("16",1,1,1,0,0),("-135/2",1,1,0,1,0),("-127/10",1,1,0,0,1),
                    ("363.764",0,1,2,0,0),("16.990",0,1,0,2,0),("-24.422",0,1,0,0,2),("48.370",0,1,1,1,0),("18.074",0,1,1,0,1),("34.829",0,1,0,1,1),
                    ("-36",3,0,0,0,0),("45",2,0,0,1,0),("9",2,0,0,0,1),
                    ("-171/16",1,0,0,2,0),("-1089/400",1,0,0,0,2),("117/40",1,0,0,1,1),
                    ("-619.35",0,0,3,0,0),("169.829",0,0,0,3,0),("16.099",0,0,0,0,3),("73.654",0,0,2,1,0),("-15.096",0,0,2,0,1),
                    ("-21.072",0,0,1,2,0),("-22.319",0,0,1,0,2),("-321/20",0,0,1,1,1),("-4.743",0,0,0,2,1),("-4.442",0,0,0,1,2)]],
             "lam": ["1", [("6011.35",4,0,0,0,0),("873",3,1,0,0,0),("-387.452",3,0,0,1,0),("-77.490",3,0,0,0,1),
                    ("1768.26",2,2,0,0,0),("160.77",2,1,1,0,0),("-359.539",2,1,0,1,0),("-63.869",2,1,0,0,1),
                    ("-790.28",2,0,0,2,0),("-185.532",2,0,0,0,2),("-316.64",2,0,0,1,1),
                    ("-223.382",1,3,0,0,0),("-662.866",1,2,1,0,0),("-5.470",1,2,0,1,0),("-21.015",1,2,0,0,1),
                    ("356.968",1,1,2,0,0),("-319.664",1,1,0,2,0),("-74.8599",1,1,0,0,2),("15.1443",1,1,1,1,0),("17.454",1,1,1,0,1),("5.615",1,1,0,1,1),
                    ("-57.144",1,0,1,2,0),("865.483",1,0,0,3,0),("79.638",1,0,0,2,1),
                    ("-8.381",1,0,1,0,2),("61.753",1,0,0,1,2),("28.168",1,0,0,0,3),
                    ("-243.149",0,4,0,0,0),("250.494",0,3,1,0,0),("74.138",0,3,0,1,0),("33.930",0,3,0,0,1),
                    ("-50.201",0,2,2,0,0),("15.884",0,2,0,2,0),("15.948",0,2,0,0,2),("13.349",0,2,1,1,0),("17.570",0,2,1,0,1),("-70.356",0,2,0,1,1),
                    ("16.464",0,1,1,2,0),("1.016",0,1,1,0,2),("11.386",0,1,1,1,1),
                    ("62.500",0,1,0,3,0),("13.041",0,1,0,2,1),
                    ("10.627",0,1,0,1,2),("11.117",0,1,0,0,3),
                    ("7.536",0,0,1,3,0),("0.663",0,0,1,0,3),("1.507",0,0,1,2,1),("1.105",0,0,1,1,2),
                    ("-114.091",0,0,0,4,0),("-1.508",0,0,0,0,4),("-37.889",0,0,0,3,1),("6.500",0,0,0,2,2),("-1.543",0,0,0,1,3)]],
            },
    },
    "g3_beta_4loop": {"source": "same, pure QCD: g3^10 (4 pi)^-8 x this, in d g3^2/d ln(mu^2)",
                      "value": "-2472.28"},
    "top_mass_3loop": {
        "source": "Melnikov, van Ritbergen 2000 (hep-ph/9912391), eq. (polethrms): the a^3 term of "
                  "M/m(m), a = alpha_s(m)/pi: c2 N_L^2 + c1 N_L + c0",
        "value": {"c2": "0.6527", "c1": "-26.655", "c0": "190.595"}},
    "lambda_2loop_matching": {
        "source": "Buttazzo et al. 2013, section 2.1: lambda^(2)(mu = M_t) = (4 pi)^-4 [g3^2 (a0 + a1 dM_h"
                  " + a2 dM_t) + (b0 + b1 dM_h + b2 dM_t)], dM_h = M_h/GeV - 125, dM_t = M_t/GeV - 173 "
                  "(their interpolation of the full two-loop result)",
        "value": {"qcd": ("-23.88", "0.12", "-0.64"), "ew": ("-9.45", "-0.12", "-0.21"),
                  "M_h0": "125", "M_t0": "173"}},
    "yt_2loop_matching": {
        "source": "Buttazzo et al. 2013, section 2.3: the electroweak and mixed QCD-electroweak two-loop "
                  "parts of y_t(mu = M_t), same form (the pure QCD part is the two-loop pole/MS-bar "
                  "conversion, already in this script)",
        "value": {"ew": ("6.48", "-0.01", "0.18"), "qcd_ew": ("-7.53", "0.09", "-0.23"),
                  "M_h0": "125", "M_t0": "173"}},
    "qcd_beta_3_4loop": {
        "source": "Chetyrkin, Kuehn, Steinhauser 2000, RunDec (hep-ph/0004189), eq. (betafct) "
                  "(van Ritbergen, Vermaseren, Larin 1997): mu^2 d(a)/d mu^2 = -sum beta_i a^(i+2), "
                  "a = alpha_s/pi. Terms (coefficient, power of n_f, zeta value), times norm",
        "value": {"beta2": {"norm": "1/64", "terms": [("2857/2", 0, ""), ("-5033/18", 1, ""), ("325/54", 2, "")]},
                  "beta3": {"norm": "1/256", "terms": [("149753/6", 0, ""), ("3564", 0, "z3"),
                                                       ("-1078361/162", 1, ""), ("-6508/27", 1, "z3"),
                                                       ("50065/162", 2, ""), ("6472/81", 2, "z3"),
                                                       ("1093/729", 3, "")]}}},
    "qcd_gamma_3_4loop": {
        "source": "RunDec, eq. after (defgamma) (Chetyrkin 1997; Vermaseren, Larin, van Ritbergen 1997): "
                  "mu^2 d m/d mu^2 = -m sum gamma_i a^(i+1), same form",
        "value": {"gamma2": {"norm": "1/64", "terms": [("1249", 0, ""), ("-2216/27", 1, ""), ("-160/3", 1, "z3"),
                                                        ("-140/81", 2, "")]},
                  "gamma3": {"norm": "1/256", "terms": [("4603055/162", 0, ""), ("135680/27", 0, "z3"),
                                                         ("-8800", 0, "z5"), ("-91723/27", 1, ""),
                                                         ("-34192/9", 1, "z3"), ("880", 1, "z4"),
                                                         ("18400/9", 1, "z5"), ("5242/243", 2, ""),
                                                         ("800/9", 2, "z3"), ("-160/3", 2, "z4"),
                                                         ("-332/243", 3, ""), ("64/27", 3, "z3")]}}},
    "qcd_decoupling": {
        "source": "RunDec eqs. (zetagSI), (zetamSI) at mu = mu_h = m_h(m_h), where every logarithm vanishes "
                  "(Chetyrkin, Kniehl, Steinhauser 1997, 1998): alpha_s^(n_l) = zeta_g^2 alpha_s^(n_f), "
                  "m^(n_l) = zeta_m m^(n_f), series in a = alpha_s^(n_f)/pi; terms (coefficient, power of "
                  "n_l, constant). B4 = 16 Li4(1/2) - 13/2 zeta4 - 4 zeta2 ln^2 2 + 2/3 ln^4 2",
        "value": {"g2": [("11/72", 0, "")],
                  "g3": [("564731/124416", 0, ""), ("-82043/27648", 0, "z3"), ("-2633/31104", 1, "")],
                  "m2": [("89/432", 0, "")],
                  "m3": [("2951/2916", 0, ""), ("-407/864", 0, "z3"), ("5/4", 0, "z4"), ("-1/36", 0, "B4"),
                         ("1327/11664", 1, ""), ("-2/27", 1, "z3")]}},
    "top_mass_4loop": {
        "source": "Marquard, Smirnov, Smirnov, Steinhauser 2015 (arXiv:1502.01030), eq. (cm4): the a^4 term "
                  "of M/m(m) for n_l = 5, a = alpha_s^(6)(m)/pi (+-21.5)",
        "value": {"c4_nl5": "827.37", "sigma": "21.5"}},
    "lambda_3loop_qcd": {
        "source": "Buttazzo et al. 2013, footnote in section 3.1 (from Martin 2013's three-loop effective "
                  "potential): lambda^(3)_QCD(mu = M_t) = norm g3^4 G_mu^2 M_t^4 (4 pi)^-6 [sum], leading "
                  "order in g3 and y_t, M_h, M_W, M_Z << M_t. Terms (coefficient, constant)",
        "value": {"norm": "-8/135",
                  "terms": [("176", "pi4"), ("720", "pi2"), ("960", "pi2_ln2sq"), ("1440", "pi2_ln2"),
                            ("9105", ""), ("-960", "ln2_4"), ("-23040", "li4half"), ("8640", "z3")]}},
    "smdr_reference": {
        "source": "Martin, Robertson 2019 (arXiv:1907.02500v5, SMDR), eqs. (referencemodelOS) and "
                  "(referencemodelMSbar): on-shell inputs and the MS-bar couplings at Q0 = 173.1 GeV that "
                  "reproduce them, with full two-loop plus leading three-loop matching and four-loop QCD. "
                  "Part L anchors its matching to this point and carries it to the measured inputs",
        "value": {"inputs": {"M_t": "173.1", "M_h": "125.1", "alpha_s_MZ": "0.1181", "G_F": "1.1663787e-5",
                             "M_Z": "91.1876"},
                  "Q0": "173.1",
                  "couplings": {"lambda": "0.12603842", "g3": "1.1636241", "g2": "0.64765961",
                                "gp": "0.35853877", "y_t": "0.93480082"}}},
    "check_rundec": {
        "source": "RunDec section 2 and table (alsMb), eq. (numdef): alpha_s^(5)(mu) from alpha_s^(5)(M_Z) "
                  "= 0.118 by exact integration, five flavours, at 3 and 4 loops; B4; Chetyrkin 1997 "
                  "(hep-ph/9703278), numerical gamma_m: gamma_2, gamma_3 coefficients of n_f^k",
        "value": {"alpha_MZ": "0.118", "M_Z": "91.18", "M_b": "4.7",
                  "alpha_Mb_4L": "0.2169467", "alpha_1GeV_3L": "0.4029", "alpha_1GeV_4L": "0.4065",
                  "B4": "-1.762800",
                  "gamma2": ("19.5156", "-2.28412", "-0.0270062"),
                  "gamma3": ("98.9434", "-19.1075", "0.276163", "0.00579322")}},
    "check_buttazzo": {
        "source": "Buttazzo et al. 2013: inputs (table 'values'), couplings at mu = M_t (section 3, with "
                  "the three-loop QCD part of y_t) and at the Planck mass (eq. sys:Pl); used only by "
                  "self-checks of the transcriptions above",
        "value": {"inputs": {"M_h": "125.15", "M_t": "173.34", "alpha_s_MZ": "0.1184", "M_W": "80.384",
                             "M_Z": "91.1876", "G_F": "1.1663787e-5"},
                  "at_Mt": {"lambda": "0.12604", "y_t": "0.93690", "g2": "0.64779", "gY": "0.35830",
                            "g3": "1.1666"},
                  "at_MPl": {"g1": "0.6154", "g2": "0.5055", "g3": "0.4873", "y_t": "0.3825",
                             "lambda": "-0.0143"},
                  "M_Pl": "1.2209e19", "lambda_th": "0.00030", "yt_th": "0.00050",
                  # lambda(M_Pl) = l0 + lt (M_t - 173.34) + la (alpha_s - 0.1184)/0.0007 + lh (M_h - 125.15),
                  # eq. (sys:Pl), and d lambda(M_t)/d M_h (section 3.1)
                  "lambda_MPl": {"l0": "-0.0143", "lt": "-0.0066", "la": "0.0018", "lh": "0.0029",
                                 "alpha_step": "0.0007"},
                  "dlambda_Mt_dMh": "0.00206"}},
    "dn_theta": {
        "source": "Full calculations of d_n / theta-bar, quoted to compare with Part O's chiral log: QCD sum "
                  "rules, Pospelov-Ritz 2000 (hep-ph/9908508v4), eq. 5; lattice QCD, Dragos et al. 2019 "
                  "(arXiv:1902.03254), -0.00152(71) theta e fm. Units: e cm per unit theta-bar",
        "value": {"QCD sum rules (Pospelov-Ritz)": ("2.4e-16", "1.0e-16"),
                  "lattice QCD (Dragos et al.)": ("1.52e-16", "0.71e-16")}},
    "proton_decay_d6": {
        "source": "Dimension-six proton decay through the SU(5) gauge bosons (Ellis, Garcia, Nagata, "
                  "Nanopoulos, Olive 2020, arXiv:2003.03285, eqs. 17, 20, 45). The two operators (lepton "
                  "doublet, lepton singlet) run as C ~ prod_i alpha_i^(-2 c_i / b_i): the one-loop "
                  "anomalous-dimension coefficients c_i (d ln C / d ln mu = -sum c_i alpha_i / pi) for SU(3), "
                  "SU(2), U(1)_GUT, in the SM and the MSSM; with the script's b_i they must reproduce the "
                  "printed exponents (a self-check). Below M_Z the QCD coefficient is the same c_3 = 1. "
                  "Two-loop long-distance factor A_L = 1.247, quoted only to compare",
        "value": {"SM": {"S1": ("11/40", "9/8", "1"), "S2": ("23/40", "9/8", "1")},
                  "MSSM": {"S1": ("11/60", "3/4", "2/3"), "S2": ("23/60", "3/4", "2/3")},
                  "printed_exponents": {"SM": {"S1": ("-11/82", "27/38", "2/7"), "S2": ("-23/82", "27/38", "2/7")},
                                        "MSSM": {"S1": ("-1/18", "-3/2", "4/9"), "S2": ("-23/198", "-3/2", "4/9")}},
                  "A_L_two_loop": "1.247"}},
    "proton_decay_d5_scaling": {
        "source": "Hisano, Kobayashi, Kuwahara, Nagata 2013 (arXiv:1304.3651), eq. 19: the higgsino-exchange "
                  "lifetime tau ~ C sin^4(2 beta) (0.1/Abar_R)^2 (M_S/100 TeV)^2 (M_HC/1e16 GeV)^2 years at "
                  "mu_H = M_S; C, quoted only to compare with Part Q's full calculation",
        "value": "4e35"},
    "ew_transition": {
        "source": "Lattice: the SM electroweak transition is first order only below the endpoint Higgs mass, "
                  "72.4 +/- 1.7 GeV (Csikor, Fodor, Heitger 1999, hep-ph/9809291); above it a crossover at "
                  "T_c = 159.5 +/- 1.5 GeV (D'Onofrio, Rummukainen 2016, arXiv:1508.07161)",
        "value": {"endpoint_m_h": ("72.4", "1.7"), "T_c": ("159.5", "1.5")}},
    "w_mass_fit": {
        "source": "Awramik, Czakon, Freitas, Weiglein 2004 (hep-ph/0311148v3), eqs. 6-8: parametrization of the "
                  "full two-loop SM prediction of M_W, better than 0.5 MeV for 10 GeV <= M_H <= 1 TeV; "
                  "Delta alpha_lept from Steinhauser (their text)",
        "value": {"coefficients": {"MW0": "80.3779", "c1": "0.05427", "c2": "0.008931", "c3": "0.0000882",
                                   "c4": "0.000161", "c5": "1.070", "c6": "0.5237", "c7": "0.0679", "c8": "0.00179",
                                   "c9": "0.0000664", "c10": "0.0795", "c11": "114.9"},
                  "reference": {"M_H": "100", "m_t": "174.3", "M_Z": "91.1875", "delta_alpha": "0.05907",
                                "alpha_s": "0.119"},
                  "delta_alpha_lept": "0.0314977", "fit_accuracy": "0.0005"}},
    "sin2_eff_fit": {
        "source": "Awramik, Czakon, Freitas 2006 (hep-ph/0608099v2), eqs. 48-49 and table 5 (leptons): the SM's "
                  "two-loop sin^2 theta_eff^lept, maximal deviation 4.5e-6 for 10 GeV <= M_H <= 1 TeV",
        "value": {"coefficients": {"s0": "0.2312527", "d1": "4.729e-4", "d2": "2.07e-5", "d3": "3.85e-6",
                                   "d4": "-1.85e-6", "d5": "2.07e-2", "d6": "-2.851e-3", "d7": "1.82e-4",
                                   "d8": "-9.74e-6", "d9": "3.98e-4", "d10": "-6.55e-1"},
                  "reference": {"M_H": "100", "m_t": "178.0", "M_Z": "91.1876", "delta_alpha": "0.05907",
                                "alpha_s": "0.117"},
                  "fit_accuracy": "4.5e-6"}},
    "axion_misalignment": {
        "source": "Di Luzio, Giannotti, Nardi, Visinelli 2020 (arXiv:2003.01100), sec. 3.3: m_a(T) = beta m_a "
                  "(T_C/T)^gamma (eq. 150, dilute instanton gas, beta from their ref. 184), g* at oscillation, "
                  "b = 1, the post-inflation <theta_i^2> = 2.15^2 with anharmonic terms; eq. 170, Omega h^2 = 0.12 "
                  "at f_a = 2.0e11 GeV, quoted only to check the calculation",
        "value": {"beta": "0.026", "gamma": "4", "T_C_GeV": "0.160", "g_star_osc": "61.75", "b": "1",
                  "theta_post": "2.15", "eq170_f_a_GeV": "2.0e11", "eq170_Omega_h2": "0.12"}},
    "axion_mass_nlo": {
        "source": "QCD axion mass at NLO in chiral perturbation theory with lattice input, Gorghetto-Villadoro "
                  "2019 (refining Grilli di Cortona et al. 2016): m_a = 5.69(5) micro-eV x (1e12 GeV / f_a)",
        "value": ("5.69", "0.05")},
}


def lit_num(v: str) -> float:
    """A LITERATURE coefficient as a float (fractions exactly)."""
    return float(Fr(v)) if "/" in v else float(v)


# =============================================================================
# 3b. ONE MODEL: EVERY STAGE, WHAT IT ASSUMES, AND WHAT IT READS
# =============================================================================
# The simulation is one algorithm. Each stage below runs once, in order; a number
# is calculated in the stage that produces it and handed to every later stage
# that needs it. The dependency graph is not typed in: every read of a measured
# input and every read of another stage's result is recorded while the stages
# run, so the graph in the report is the one the code actually follows.
#   level: proved / exact / numerical / conditional / parameter trade / validation
#   uv:    the field content the stage assumes above the electroweak scale, where
#          it assumes one. Stages that assume different ones cannot both hold.
STAGES: Dict[str, Dict[str, str]] = {
    "cosmology": {"part": "A", "level": "conditional",
                  "assumes": "flat LambdaCDM: Omega_Lambda = 1 - Omega_m - Omega_r"},
    "gauge_unification": {"part": "I", "level": "parameter trade", "uv": "MSSM above M_S",
                          "assumes": "one superpartner scale M_S; the measured alpha is spent to infer it"},
    "alpha_numerology": {"part": "I", "level": "exact", "assumes": "none (tests closed formulas)"},
    "flavour": {"part": "B", "level": "numerical",
                "assumes": "Fritzsch six-zero texture; phase bands from a finite grid plus local search"},
    "texture_survey": {"part": "C", "level": "numerical",
                       "assumes": "Hermitian textures; searches from finite grids (--certify proves the "
                                  "exclusions: 80 of 82)"},
    "survey_certificates": {"part": "C", "level": "proved",
                            "assumes": "only with --certify; exclusions proved cell by cell, at m_t(m_t)"},
    "gauge_331": {"part": "D", "level": "exact", "assumes": "3-3-1 representations, beta = -1/sqrt3, +1/sqrt3"},
    "flavour_symmetry_331": {"part": "E", "level": "exact",
                             "assumes": "abelian Z_N up to symmetry_max_N; scalar potential not solved"},
    "general_texture_closure": {"part": "F", "level": "proved",
                                "assumes": "equalities only: a rank-10 pattern may still miss the data"},
    "planck_units": {"part": "H1", "level": "exact", "assumes": "none; nothing derives G"},
    "quantum_gravity": {"part": "H", "level": "exact",
                        "assumes": "identities and effective field theory"},
    "yukawa_relations": {"part": "J", "level": "conditional", "uv": "MSSM above M_S",
                         "assumes": "M_S and M_GUT from Part I"},
    "higgs_mssm": {"part": "K", "level": "conditional", "uv": "MSSM above M_S",
                   "assumes": "M_S from Part I, tan(beta) from Part J, one-loop stop threshold"},
    "criticality": {"part": "L", "level": "conditional", "uv": "SM up to M_P",
                    "assumes": "lambda(M_P) = 0; three-loop running, matching anchored to SMDR, four-loop QCD"},
    "uv_joint_test": {"part": "M", "level": "numerical",
                      "assumes": "every hypothesis against every set of conditions; unknowns on a grid "
                                 "plus exact roots and edges; theory errors = last-order shifts"},
    "mass_formulas": {"part": "N", "level": "exact",
                      "assumes": "none (tests closed mass formulas at stated scales)"},
    "strong_cp": {"part": "O", "level": "conditional",
                  "assumes": "leading-order chiral perturbation theory for d_n and m_a; theta-bar the only "
                             "source of d_n"},
    "neutrinos": {"part": "P", "level": "numerical",
                  "assumes": "three light neutrinos; lightest mass and Majorana phases scanned; cosmological "
                             "limits assume flat LambdaCDM; unknowns of corrected patterns solved exactly"},
    "proton_decay": {"part": "Q", "level": "conditional", "uv": "MSSM above M_S",
                     "assumes": "minimal SU(5): gauge bosons at M_X = M_GUT, colour triplet at M_HC = M_GUT, every "
                                "superpartner at M_S (Part I), tan(beta) from Part J; GUT phases scanned; one-loop "
                                "operator running; GUT thresholds unknown"},
    "anomalies": {"part": "R", "level": "exact",
                  "assumes": "one family of the SM's representations (and Part D's 3-3-1 families); "
                             "Yukawa couplings for every charged fermion"},
    "baryon_asymmetry": {"part": "S", "level": "conditional",
                         "assumes": "lattice endpoint and T_c of the SM transition; leptogenesis: hierarchical "
                                    "right-handed neutrinos, thermal, efficiency kappa <= 1"},
    "so10": {"part": "T", "level": "conditional",
             "assumes": "SO(10) with one 16 per family; minimal Yukawas from one 10_H; the Pati-Salam chain with "
                        "scalars (1,2,2) + (10,1,3), one-loop running, no thresholds"},
    "scorecard": {"part": "U", "level": "conditional",
                  "assumes": "the SM, minimal SUSY SU(5) and four SO(10) chains (two loops), each condition judged "
                             "by the stage that computes it; for the chains the Higgs condition is lambda(M_I) = 0"},
    "dark_matter": {"part": "V", "level": "conditional",
                    "assumes": "QCD axion by misalignment; dilute-instanton m_a(T); string and domain-wall "
                               "production left out; f_a scanned and at each SO(10) chain's M_I"},
    "w_mass": {"part": "W", "level": "conditional",
               "assumes": "the SM's two-loop M_W in its published parametrization, at Part L's Higgs mass"},
    "closed_cosmology": {"part": "X", "level": "conditional",
                         "assumes": "Omega_m from Omega_b (measured), the axion at the surviving chain's M_I "
                                    "(misalignment, post-inflation) and the minimal neutrino masses; flat LambdaCDM"},
    "so10_yukawa": {"part": "Y", "level": "numerical",
                    "assumes": "symmetric Yukawas from a 10 and a 126; the selection rule exact at tree level; the "
                               "sum rule at the LR chain's M_GUT with SM running; unknowns searched, never set"},
    "ledger": {"part": "Z", "level": "conditional",
               "assumes": "every free number of the SM plus cosmology, with the status the stages computed for the "
                          "surviving hypothesis"},
    "self_checks": {"part": "-", "level": "validation", "assumes": "tests the calculation, not the physics"},
}

# What the dependency audit found that the traced graph cannot show by itself.
AUDIT_FINDINGS: Tuple[Tuple[str, str], ...] = (
    ("resolved", "The SM couplings at m_t(m_t) were derived by two copies of the same formulas "
                 "(Parts J/K and Part L). There is now one derivation, sm_state_at_mt."),
    ("open", "Part L rebuilds the quark-mass running instead of taking the flavour stage's: same "
             "function, same numbers, because its error propagation re-runs the chain per input."),
    ("resolved", "Parts I, J, K assume the MSSM above M_S; Part L assumes the SM up to M_P. Both cannot "
                 "hold, so neither is chosen: Part M runs each hypothesis against every combination of "
                 "the conditions and reports which survive."),
    ("resolved", "Part M's theory errors are calculated, not typed in: for every ingredient the change "
                 "from the last order the script computes to the one below it."),
    ("resolved", "Part L runs at three loops, matches at three loops (leading QCD part) and treats QCD at "
                 "four loops with three-loop decoupling, each published coefficient checked by a self-check."),
    ("resolved", "The electroweak and mixed higher-order thresholds Part L could not transcribe are taken "
                 "from SMDR's reference point (full two-loop plus leading three-loop): anchoring to it moves "
                 "M_h by about a MeV, so this script's matching is confirmed."),
    ("open", "If SM criticality's Part M verdict differs between the two error sets, it is decided by the "
             "last-order shifts, which four-loop QCD dominates. They are a conservative estimate: the QCD "
             "series of the top pole mass falls by about a factor of three per order."),
    ("open", "The MSSM with all three conditions still depends on the theory errors, through the one- to "
             "two-loop shift of unification. Settling it needs three-loop gauge running with superpartner "
             "and GUT thresholds, and the two-loop stop threshold."),
    ("open", "No stage feeds cosmology: H0 and Omega_m are inputs. A shared mechanism would need "
             "equations for the dark-matter density and Lambda."),
    ("resolved", "M_P was computed inside Part H, so every input of Part H (H0 among them) seemed to "
                 "reach Parts J and L. The Planck units are now their own stage."),
    ("open", "No stage derives G: M_P is calculated from it and handed to Parts H, J and L."),
    ("open", "The quark masses and mixing are inputs to the textures. Connecting them to 3-3-1 needs "
             "the scalar potential, its vacuum, and the vevs that multiply the Yukawa couplings."),
    ("open", "No common mechanism yet: no stage computes a quantity that two sectors both take "
             "from it except M_S, M_GUT (Part I) and M_P (Part H1)."),
    ("open", "Part L assumes the SM up to M_P, but neutrinos have mass (Part P). That holds only if they are "
             "Dirac particles with Yukawa couplings below 3e-13, which do not affect the running; a seesaw "
             "needs new states below about 8e15 GeV, whose couplings would enter lambda's running."),
    ("open", "Part V calculates the axion's dark-matter density as a function of f_a, but Part A still takes "
             "Omega_m as an input: feeding Part V back into Part A needs f_a fixed (at a chain's M_I, about two "
             "thirds of Omega_c for Pati-Salam) and the string yield."),
    ("open", "Theta-bar is bounded, not calculated (Part O). Each explanation adds something unmeasured: an "
             "axion scale f_a, or a parity symmetry whose Hermitian textures Part G excludes."),
)

_TRACE: Dict[str, Any] = {"stage": None, "inputs": {}, "uses": {}, "keys": {}, "set": {}}


def _note_input(name: str) -> None:
    if _TRACE["stage"]:
        _TRACE["inputs"].setdefault(_TRACE["stage"], set()).add(name)


def _note_use(producer: str, key: Any = "*") -> None:
    s = _TRACE["stage"]
    if s and s != producer:
        _TRACE["uses"].setdefault(s, set()).add(producer)
        _TRACE["keys"].setdefault((producer, str(key)), set()).add(s)


def _input_value(name: str) -> str:
    """The one place a measured value is read: recorded, and replaced if --set changed it."""
    _note_input(name)
    return _TRACE["set"].get(name, INPUTS[name]["value"])


def inp(name: str) -> float:
    return float(_input_value(name))


def sig(name: str) -> float:
    _note_input(name)
    return float(INPUTS[name]["sigma"])


def inp_decimal(name: str) -> Decimal:
    return Decimal(_input_value(name))


def sig_decimal(name: str) -> Decimal:
    _note_input(name)
    return Decimal(INPUTS[name]["sigma"])


class _InputView(dict):
    """All measured inputs as floats; each read is recorded for the stage that makes it."""

    def __getitem__(self, k: str) -> float:
        _note_input(k)
        return dict.__getitem__(self, k)


class _Output(dict):
    """A stage's result. Reading it from inside another stage records that dependency."""
    producer = ""

    def __getitem__(self, k: Any) -> Any:
        _note_use(self.producer, k)
        return dict.__getitem__(self, k)

    def get(self, k: Any, d: Any = None) -> Any:
        _note_use(self.producer, k)
        return dict.get(self, k, d)

    def items(self):
        _note_use(self.producer)
        return dict.items(self)

    def values(self):
        _note_use(self.producer)
        return dict.values(self)

    def __iter__(self):
        _note_use(self.producer)
        return dict.__iter__(self)


def _stage(name: str, thunk: Callable[[], Any]) -> Any:
    """Run one stage of the model with its reads recorded under its name."""
    prev, _TRACE["stage"] = _TRACE["stage"], name
    _TRACE["inputs"].setdefault(name, set())
    try:
        out = thunk()
    finally:
        _TRACE["stage"] = prev
    if isinstance(out, dict):
        out = _Output(out)
        out.producer = name
    return out


def num(name: str) -> float:
    return float(NUMERICS[name])


# =============================================================================
# 4. GROUP THEORY: every coefficient is computed, then cross-checked
# =============================================================================
def su_n_casimirs(n: int) -> Tuple[Fr, Fr, Fr]:
    """C_A, C_F, T_F of SU(N) with fundamental Dynkin index T_F = 1/2."""
    return Fr(n), Fr(n * n - 1, 2 * n), Fr(1, 2)


def qcd_beta(nf: int) -> Tuple[Fr, Fr]:
    """d a / d ln mu^2 = -b0 a^2 - b1 a^3 with a = alpha_s / (4 pi)."""
    ca, cf, tf = su_n_casimirs(3)
    b0 = Fr(11, 3) * ca - Fr(4, 3) * tf * nf
    b1 = Fr(34, 3) * ca * ca - 4 * cf * tf * nf - Fr(20, 3) * ca * tf * nf
    return b0, b1


def qcd_gamma_m(nf: int) -> Tuple[Fr, Fr]:
    """d ln m / d ln mu^2 = -(g0 a + g1 a^2) with a = alpha_s / (4 pi)."""
    ca, cf, tf = su_n_casimirs(3)
    g0 = 3 * cf
    g1 = cf * (Fr(3, 2) * cf + Fr(97, 6) * ca - Fr(10, 3) * tf * nf)
    return g0, g1


# Standard Model field content: (name, SU(3) dim, SU(2) dim, hypercharge Y, kind, copies)
SM_FIELDS = (
    ("Q", 3, 2, Fr(1, 6), "weyl", 3),
    ("u^c", 3, 1, Fr(-2, 3), "weyl", 3),
    ("d^c", 3, 1, Fr(1, 3), "weyl", 3),
    ("L", 1, 2, Fr(-1, 2), "weyl", 3),
    ("e^c", 1, 1, Fr(1, 1), "weyl", 3),
    ("H", 1, 2, Fr(1, 2), "complex_scalar", 1),
)
GUT_NORM = Fr(3, 5)  # g1^2 = (5/3) g'^2: the SU(5)-normalized hypercharge


def dynkin_fund(dim: int) -> Fr:
    return Fr(1, 2) if dim > 1 else Fr(0)


def casimir_fund(group_n: int, dim: int) -> Fr:
    return su_n_casimirs(group_n)[1] if dim > 1 else Fr(0)


def sm_gauge_b() -> Tuple[Fr, Fr, Fr]:
    """One-loop b_i in d g_i / d ln mu = b_i g_i^3 / (16 pi^2), from the field content."""
    b = [Fr(0), -Fr(11, 3) * su_n_casimirs(2)[0], -Fr(11, 3) * su_n_casimirs(3)[0]]
    for _, d3, d2, y, kind, copies in SM_FIELDS:
        w = Fr(2, 3) if kind == "weyl" else Fr(1, 3)
        b[0] += w * copies * GUT_NORM * y * y * d3 * d2
        b[1] += w * copies * dynkin_fund(d2) * d3
        b[2] += w * copies * dynkin_fund(d3) * d2
    return b[0], b[1], b[2]


def top_yukawa_gauge_coeffs() -> Tuple[Fr, Fr, Fr]:
    """c_i in 16 pi^2 d ln y_t / d ln mu  contains  -c_i g_i^2: 3 [C2(Q) + C2(u^c)] per group."""
    q = SM_FIELDS[0]
    u = SM_FIELDS[1]
    c1 = 3 * GUT_NORM * (q[3] ** 2 + u[3] ** 2)
    c2 = 3 * (casimir_fund(2, q[2]) + casimir_fund(2, u[2]))
    c3 = 3 * (casimir_fund(3, q[1]) + casimir_fund(3, u[1]))
    return c1, c2, c3


def top_yukawa_self_coeff() -> Fr:
    """16 pi^2 d ln y_t / d ln mu contains (3/2) y_t^2 + Y2, with Y2 = N_c y_t^2."""
    return Fr(3, 2) + su_n_casimirs(3)[0]


YUKAWA_SPLIT = Fr(3, 2)  # coefficient of (Y_u Y_u^dag - Y_d Y_d^dag) in the SM Yukawa RGE


def zeta3() -> float:
    """Apery's constant from zeta(3) = (5/2) sum (-1)^(n+1) / (n^3 binom(2n, n))."""
    total = 0.0
    for n in range(1, 40):
        total += (-1) ** (n + 1) / (n ** 3 * math.comb(2 * n, n))
    return 5 * total / 2


def zeta_int(n: int) -> float:
    """Riemann zeta(n), integer n >= 2: twenty terms plus the Euler-Maclaurin tail."""
    big = 20
    head = sum(k ** -n for k in range(1, big))
    return (head + big ** (1 - n) / (n - 1) + big ** -n / 2 + n * big ** (-n - 1) / 12
            - n * (n + 1) * (n + 2) * big ** (-n - 3) / 720)


def li4_half() -> float:
    """Li_4(1/2) = sum 1/(2^k k^4)."""
    return sum(1 / (2 ** k * k ** 4) for k in range(1, 60))


def qcd_constant(tag: str) -> float:
    """The transcendental constants the quoted QCD and matching coefficients multiply."""
    l2, z2, z4 = math.log(2), math.pi ** 2 / 6, math.pi ** 4 / 90
    return {"": 1.0, "z3": zeta3(), "z4": z4, "z5": zeta_int(5),
            "B4": 16 * li4_half() - 13 * z4 / 2 - 4 * z2 * l2 ** 2 + 2 * l2 ** 4 / 3,
            "pi4": math.pi ** 4, "pi2": math.pi ** 2, "pi2_ln2sq": math.pi ** 2 * l2 ** 2,
            "pi2_ln2": math.pi ** 2 * l2, "ln2_4": l2 ** 4, "li4half": li4_half()}[tag]


def _lit_poly(terms: Sequence[Tuple[str, int, str]], n: int) -> float:
    return sum(lit_num(c) * n ** p * qcd_constant(z) for c, p, z in terms)


def qcd_beta_pi(nf: int, loops: int) -> List[float]:
    """beta_i with a = alpha_s/pi: one and two loops from the Casimirs (b_i/4^(i+1)), three and
    four from LITERATURE."""
    b0, b1 = qcd_beta(nf)
    out = [float(b0) / 4, float(b1) / 16]
    for key in ("beta2", "beta3"):
        e = LITERATURE["qcd_beta_3_4loop"]["value"][key]
        out.append(lit_num(e["norm"]) * _lit_poly(e["terms"], nf))
    return out[:loops]


def qcd_gamma_pi(nf: int, loops: int) -> List[float]:
    """gamma_m,i with a = alpha_s/pi, the same way."""
    g0, g1 = qcd_gamma_m(nf)
    out = [float(g0) / 4, float(g1) / 16]
    for key in ("gamma2", "gamma3"):
        e = LITERATURE["qcd_gamma_3_4loop"]["value"][key]
        out.append(lit_num(e["norm"]) * _lit_poly(e["terms"], nf))
    return out[:loops]


def decoupling_g2(alpha_f: float, n_l: int, loops: int) -> float:
    """zeta_g^2 at mu = m_h(m_h): alpha_s^(n_l) / alpha_s^(n_f); (loops - 1)-loop matching
    for loops-loop running, so nothing below three loops."""
    e = LITERATURE["qcd_decoupling"]["value"]
    a = alpha_f / math.pi
    z = 1.0
    if loops >= 3:
        z += _lit_poly(e["g2"], n_l) * a * a
    if loops >= 4:
        z += _lit_poly(e["g3"], n_l) * a ** 3
    return z


def decoupling_m(alpha_f: float, n_l: int, loops: int) -> float:
    """zeta_m at mu = m_h(m_h): m^(n_l) / m^(n_f) for a lighter quark."""
    e = LITERATURE["qcd_decoupling"]["value"]
    a = alpha_f / math.pi
    z = 1.0
    if loops >= 3:
        z += _lit_poly(e["m2"], n_l) * a * a
    if loops >= 4:
        z += _lit_poly(e["m3"], n_l) * a ** 3
    return z


def alpha_up(alpha_l: float, n_l: int, loops: int) -> float:
    """alpha_s^(n_f) from alpha_s^(n_l) at the threshold: the downward relation, inverted exactly."""
    a_f = alpha_l
    for _ in range(50):
        new = alpha_l / decoupling_g2(a_f, n_l, loops)
        if new == a_f:
            break
        a_f = new
    return a_f


def pole_to_msbar_coeffs(n_light: int) -> Tuple[float, float]:
    """M / m(m) = 1 + k1 a + k2 a^2 with a = alpha_s(m)/pi (Gray, Broadhurst, Grafe, Schilcher 1990),
    light-quark masses in the loop neglected."""
    ca, cf, tf = su_n_casimirs(3)
    z2 = math.pi ** 2 / 6
    k1 = float(cf)
    k2 = (307 / 32 + 2 * z2 + 2 * z2 * math.log(2) / 3 - zeta3() / 6
          - n_light * (71 / 144 + z2 / 3))
    return k1, k2


def pole_to_msbar_k(n_light: int, loops: int) -> List[float]:
    """M / m(m) = 1 + sum k_i a^i, a = alpha_s^(n_l + 1)(m)/pi: two loops analytic (above), three
    (Melnikov-van Ritbergen) and four (Marquard et al., n_l = 5 only) from LITERATURE."""
    k1, k2 = pole_to_msbar_coeffs(n_light)
    c = LITERATURE["top_mass_3loop"]["value"]
    k3 = lit_num(c["c2"]) * n_light ** 2 + lit_num(c["c1"]) * n_light + lit_num(c["c0"])
    ks = [k1, k2, k3]
    if loops >= 4:
        if n_light != 5:
            raise ValueError("the four-loop coefficient is quoted for n_l = 5 only")
        ks.append(lit_num(LITERATURE["top_mass_4loop"]["value"]["c4_nl5"]))
    return ks[:loops]


# =============================================================================
# 5. RENORMALIZATION-GROUP RUNNING
# =============================================================================
def _rk4(f: Callable[[List[float]], List[float]], y: List[float], h: float) -> List[float]:
    k1 = f(y)
    k2 = f([a + h / 2 * b for a, b in zip(y, k1)])
    k3 = f([a + h / 2 * b for a, b in zip(y, k2)])
    k4 = f([a + h * b for a, b in zip(y, k3)])
    return [a + h / 6 * (b1 + 2 * b2 + 2 * b3 + b4) for a, b1, b2, b3, b4 in zip(y, k1, k2, k3, k4)]


def _nf_at(mu: float, thresholds: Sequence[float]) -> int:
    return 3 + sum(1 for m in thresholds if mu > m)


def integrate_ln_mu(y0: List[float], mu0: float, mu1: float,
                    rhs: Callable[[List[float], int], List[float]],
                    thresholds: Sequence[float], steps_per_efold: int,
                    match: Callable[[List[float], float, int, int], List[float]] | None = None) -> List[float]:
    """RK4 in ln(mu), split exactly at the flavour thresholds; match(y, mu, nf_from, nf_to)
    applies the decoupling relations where a threshold is crossed."""
    l0, l1 = math.log(mu0), math.log(mu1)
    cuts = sorted(math.log(m) for m in thresholds if min(l0, l1) < math.log(m) < max(l0, l1))
    if l1 < l0:
        cuts.reverse()
    pts = [l0] + cuts + [l1]
    y = list(y0)
    nf_prev = None
    for a, b in zip(pts[:-1], pts[1:]):
        if b == a:
            continue
        nf = _nf_at(math.exp((a + b) / 2), thresholds)
        if match is not None and nf_prev is not None and nf != nf_prev:
            y = match(y, math.exp(a), nf_prev, nf)
        nf_prev = nf
        n = max(1, math.ceil(abs(b - a) * steps_per_efold))
        h = (b - a) / n
        for _ in range(n):
            y = _rk4(lambda v: rhs(v, nf), y, h)
    return y


class FlavourRunner:
    """Runs alpha_s and the quark masses from the measured inputs. No free parameters."""

    def __init__(self, x: Dict[str, float], steps_per_efold: int, qcd_loops: int = 4):
        """QCD at qcd_loops loops: the beta function and the mass anomalous dimension at that
        order, (qcd_loops - 1)-loop decoupling at the quark thresholds, the top pole/MS-bar
        conversion at qcd_loops loops. Lowering it by one is Part M's estimate of the error
        from the orders not calculated."""
        self.x = x
        self.steps = steps_per_efold
        self.loops = qcd_loops
        self.alpha_em = 1 / x["alpha_em_inv_MZ"]
        self.beta = {nf: qcd_beta_pi(nf, qcd_loops) for nf in range(3, 7)}
        self.gamma = {nf: qcd_gamma_pi(nf, qcd_loops) for nf in range(3, 7)}
        self.thresholds: List[float] = [x["m_c"], x["m_b"]]
        self.mt_msbar = self._top_msbar()
        self.thresholds = [x["m_c"], x["m_b"], self.mt_msbar]
        self.v = (math.sqrt(2) * x["G_F"]) ** (-1 / 2)

    # d alpha_s / d ln mu and d ln m / d ln mu (two-loop QCD, one-loop QED)
    def _qcd_rhs(self, y: List[float], nf: int, q2: float) -> List[float]:
        """d alpha_s / d ln mu and d ln m / d ln mu (QCD at self.loops loops, one-loop QED)."""
        a = y[0] / math.pi
        dal = -2 * math.pi * sum(b * a ** (i + 2) for i, b in enumerate(self.beta[nf]))
        dlnm = (-2 * sum(g * a ** (i + 1) for i, g in enumerate(self.gamma[nf]))
                - 3 * q2 * self.alpha_em / (2 * math.pi))
        return [dal, dlnm]

    def _match(self, y: List[float], mu: float, nf_from: int, nf_to: int) -> List[float]:
        """Decouple (downward) or re-couple (upward) alpha_s and a light mass at a threshold."""
        if nf_to < nf_from:
            al_f = y[0]
            return [al_f * decoupling_g2(al_f, nf_to, self.loops),
                    y[1] + math.log(decoupling_m(al_f, nf_to, self.loops))]
        al_f = alpha_up(y[0], nf_from, self.loops)
        return [al_f, y[1] - math.log(decoupling_m(al_f, nf_from, self.loops))]

    def alpha_s(self, mu: float) -> float:
        y = integrate_ln_mu([self.x["alpha_s_MZ"], 0.0], self.x["M_Z"], mu,
                            lambda v, nf: self._qcd_rhs(v, nf, 0.0), self.thresholds, self.steps,
                            self._match)
        return y[0]

    def run_mass(self, m0: float, mu0: float, mu1: float, charge: Fr) -> float:
        y = integrate_ln_mu([self.alpha_s(mu0), math.log(m0)], mu0, mu1,
                            lambda v, nf: self._qcd_rhs(v, nf, float(charge) ** 2),
                            self.thresholds, self.steps, self._match)
        return math.exp(y[1])

    def _top_msbar(self) -> float:
        """Solve M_t = m (1 + sum_i k_i a(m)^i) for the MS-bar mass m = m_t(m_t), with
        a = alpha_s^(6)(m)/pi, to self.loops loops."""
        ks = pole_to_msbar_k(5, self.loops)
        big_m = self.x["M_t"]
        m = big_m
        for _ in range(100):
            a = alpha_up(self.alpha_s(m), 5, self.loops) / math.pi
            m_new = big_m / (1 + sum(k * a ** (i + 1) for i, k in enumerate(ks)))
            if abs(m_new - m) <= abs(m) * float(NUMERICS["check_rel_tol"]) / 1000:
                m = m_new
                break
            m = m_new
        return m

    def ratios_at(self, scales: Sequence[float]) -> Dict[float, Dict[str, float]]:
        """Same-type mass ratios at m_t(m_t) and at each scale above it."""
        x = self.x
        mu0 = self.mt_msbar
        up, dn = Fr(2, 3), Fr(-1, 3)
        m = {
            "u": self.run_mass(x["m_u"], x["mu_light"], mu0, up),
            "d": self.run_mass(x["m_d"], x["mu_light"], mu0, dn),
            "s": self.run_mass(x["m_s"], x["mu_light"], mu0, dn),
            "c": self.run_mass(x["m_c"], x["m_c"], mu0, up),
            "b": self.run_mass(x["m_b"], x["m_b"], mu0, dn),
            "t": mu0,
        }
        base = {"mu": mu0, "m_u": m["u"], "m_d": m["d"], "m_s": m["s"], "m_c": m["c"], "m_b": m["b"],
                "m_t": m["t"], "r_uc": m["u"] / m["c"], "r_ct": m["c"] / m["t"],
                "r_ds": m["d"] / m["s"], "r_sb": m["s"] / m["b"],
                "alpha_s": alpha_up(self.alpha_s(mu0), 5, self.loops),      # six flavours from here up
                "y_t": math.sqrt(2) * mu0 / self.v}
        out = {mu0: base}

        # Above m_t: alpha_s (nf = 6), g1, g2, y_t, ln(m_c/m_t), ln(m_s/m_b).
        # Same-type ratios feel only the Yukawa difference term; gauge and Y2 terms cancel.
        b1, b2, _ = (float(b) for b in sm_gauge_b())
        c1, c2, c3 = (float(c) for c in top_yukawa_gauge_coeffs())
        c_self = float(top_yukawa_self_coeff())
        split = float(YUKAWA_SPLIT)
        k = 16 * math.pi ** 2
        # electroweak couplings at M_Z from G_F, alpha(M_Z), M_Z (tree-level relation)
        al = self.alpha_em
        s2c2 = math.pi * al / (math.sqrt(2) * x["G_F"] * x["M_Z"] ** 2)
        s2 = (1 - math.sqrt(1 - 4 * s2c2)) / 2
        g2sq_mz = 4 * math.pi * al / s2
        g1sq_mz = 4 * math.pi * al / (1 - s2) / float(GUT_NORM)

        def g_sq(gsq_mz: float, b: float, mu: float) -> float:
            return 1 / (1 / gsq_mz - 2 * b / k * math.log(mu / x["M_Z"]))

        yb = math.sqrt(2) * m["b"] / self.v  # bottom Yukawa held at its m_t value (a y_b^2 ~ 3e-4 effect)
        state = [base["alpha_s"], math.sqrt(g_sq(g1sq_mz, b1, mu0)), math.sqrt(g_sq(g2sq_mz, b2, mu0)),
                 math.sqrt(2) * mu0 / self.v, math.log(base["r_ct"]), math.log(base["r_sb"])]
        self.ew = {"v_GeV": self.v, "sin2_theta_tree": s2, "y_t_at_mt": state[3], "y_b_at_mt": yb,
                   "g1_at_mt": state[1], "g2_at_mt": state[2]}

        def rhs(v: List[float], nf: int) -> List[float]:
            als, g1, g2, yt, _, _ = v
            dal = -2 * math.pi * sum(b * (als / math.pi) ** (i + 2) for i, b in enumerate(self.beta[6]))
            g3sq = 4 * math.pi * als
            dyt = yt * (c_self * yt * yt + split * yb * yb - c3 * g3sq - c2 * g2 * g2 - c1 * g1 * g1) / k
            return [dal, b1 * g1 ** 3 / k, b2 * g2 ** 3 / k, dyt,
                    split * (yb * yb - yt * yt) / k, split * (yt * yt - yb * yb) / k]

        mu_prev = mu0
        for mu in sorted(scales):
            # below m_t(m_t) the ratio running is only continued across the top-mass uncertainty
            # (input variations shift m_t(m_t) itself); anything lower is refused
            if mu < mu0 * (1 - 3 * sig("M_t") / inp("M_t")):
                raise ValueError(f"evaluation scale {mu} GeV is below m_t(m_t) = {mu0:.2f} GeV")
            if mu == mu0:
                continue
            state = integrate_ln_mu(state, mu_prev, mu, rhs, [], self.steps)
            mu_prev = mu
            out[mu] = {"mu": mu, "alpha_s": state[0], "y_t": state[3], "r_uc": base["r_uc"],
                       "r_ct": math.exp(state[4]), "r_ds": base["r_ds"], "r_sb": math.exp(state[5])}
        return out


# =============================================================================
# 6. THE FRITZSCH SIX-ZERO TEXTURE: exact entries, exact diagonalization
# =============================================================================
def fritzsch_entries(x1: float, x2: float) -> Tuple[Tuple[int, int, int], float, float, float]:
    """Real Fritzsch matrix [[0,A,0],[A,0,B],[0,B,C]] with eigenvalues (s1 x1, s2 x2, s3 * 1).

    The invariants fix every entry: C = trace, A^2 = -det / C, A^2 + B^2 = -(sum of 2x2 minors).
    All sign assignments (overall sign fixed by s3 = +1) are tried; exactly one gives real A, B.
    """
    sols = []
    for s1, s2 in itertools.product((1, -1), repeat=2):
        e = (s1 * x1, s2 * x2, 1.0)
        c = sum(e)
        det = e[0] * e[1] * e[2]
        minors = e[0] * e[1] + e[0] * e[2] + e[1] * e[2]
        a2 = -det / c
        b2 = -minors - a2
        if a2 > 0 and b2 > 0:
            sols.append(((s1, s2, 1), math.sqrt(a2), math.sqrt(b2), c))
    if len(sols) != 1:
        raise RuntimeError(f"expected one real Fritzsch solution, found {len(sols)}")
    return sols[0]


def jacobi_eigh(mat: List[List[float]], tol: float) -> Tuple[List[float], List[List[float]]]:
    """Cyclic Jacobi diagonalization of a real symmetric matrix. Columns of O are eigenvectors."""
    n = len(mat)
    a = [row[:] for row in mat]
    o = [[float(i == j) for j in range(n)] for i in range(n)]
    for _ in range(100):
        off = sum(a[i][j] ** 2 for i in range(n) for j in range(i + 1, n))
        if off <= tol:
            break
        for p in range(n):
            for q in range(p + 1, n):
                if a[p][q] == 0:
                    continue
                theta = (a[q][q] - a[p][p]) / (2 * a[p][q])
                t = math.copysign(1, theta) / (abs(theta) + math.sqrt(theta * theta + 1))
                cs = 1 / math.sqrt(t * t + 1)
                sn = t * cs
                for k in range(n):
                    akp, akq = a[k][p], a[k][q]
                    a[k][p], a[k][q] = cs * akp - sn * akq, sn * akp + cs * akq
                for k in range(n):
                    apk, aqk = a[p][k], a[q][k]
                    a[p][k], a[q][k] = cs * apk - sn * aqk, sn * apk + cs * aqk
                for k in range(n):
                    okp, okq = o[k][p], o[k][q]
                    o[k][p], o[k][q] = cs * okp - sn * okq, sn * okp + cs * okq
    evals = [a[i][i] for i in range(n)]
    order = sorted(range(n), key=lambda i: abs(evals[i]))
    return [evals[i] for i in order], [[o[r][i] for i in order] for r in range(n)]


def texture_rotation(x1: float, x2: float) -> Dict[str, Any]:
    signs, a, b, c = fritzsch_entries(x1, x2)
    mat = [[0.0, a, 0.0], [a, 0.0, b], [0.0, b, c]]
    evals, o = jacobi_eigh(mat, float(NUMERICS["jacobi_tol"]))
    return {"signs": signs, "A": a, "B": b, "C": c, "eigenvalues": evals, "O": o}


def ckm_coefficients(ou: List[List[float]], od: List[List[float]]) -> List[List[List[float]]]:
    """V = O_u^T diag(1, e^{i sigma}, e^{i tau}) O_d, so V_ij = sum_k coef[i][j][k] p_k."""
    return [[[ou[k][i] * od[k][j] for k in range(3)] for j in range(3)] for i in range(3)]


def ckm_matrix(coef: List[List[List[float]]], sigma: float, tau: float) -> List[List[complex]]:
    p = (1.0, cmath.exp(1j * sigma), cmath.exp(1j * tau))
    return [[sum(coef[i][j][k] * p[k] for k in range(3)) for j in range(3)] for i in range(3)]


OBSERVABLES = ("V_us", "V_cb", "V_ub", "V_ub/V_cb", "V_td/V_ts", "J")


def ckm_observables(v: List[List[complex]]) -> Dict[str, float]:
    vus, vcb, vub = abs(v[0][1]), abs(v[1][2]), abs(v[0][2])
    vtd, vts = abs(v[2][0]), abs(v[2][1])
    jarl = (v[0][1] * v[1][2] * v[0][2].conjugate() * v[1][1].conjugate()).imag
    return {"V_us": vus, "V_cb": vcb, "V_ub": vub, "V_ub/V_cb": vub / vcb,
            "V_td/V_ts": vtd / vts, "J": jarl}


def texture_at(r: Dict[str, float]) -> Dict[str, Any]:
    up = texture_rotation(r["r_uc"] * r["r_ct"], r["r_ct"])
    dn = texture_rotation(r["r_ds"] * r["r_sb"], r["r_sb"])
    return {"up": up, "down": dn, "coef": ckm_coefficients(up["O"], dn["O"])}


def _pattern_search(f: Callable[[float, float], float], s: float, t: float, step: float,
                    min_step: float) -> Tuple[float, float, float]:
    best = f(s, t)
    while step > min_step:
        moved = False
        for ds, dt in ((step, 0), (-step, 0), (0, step), (0, -step),
                       (step, step), (-step, -step), (step, -step), (-step, step)):
            val = f(s + ds, t + dt)
            if val > best:
                best, s, t, moved = val, s + ds, t + dt, True
                break
        if not moved:
            step /= 2
    return s, t, best


def phase_bands(coef: List[List[List[float]]], grid: int, min_step: float) -> Dict[str, Dict[str, Any]]:
    """Min and max of every observable over the full phase torus [0, 2 pi)^2."""
    two_pi = 2 * math.pi
    best: Dict[str, Dict[str, Any]] = {k: {"lo": (math.inf, 0.0, 0.0), "hi": (-math.inf, 0.0, 0.0)}
                                       for k in OBSERVABLES}
    for i in range(grid):
        s = two_pi * i / grid
        for j in range(grid):
            t = two_pi * j / grid
            obs = ckm_observables(ckm_matrix(coef, s, t))
            for k, val in obs.items():
                if val < best[k]["lo"][0]:
                    best[k]["lo"] = (val, s, t)
                if val > best[k]["hi"][0]:
                    best[k]["hi"] = (val, s, t)
    bands = {}
    for k in OBSERVABLES:
        _, s_lo, t_lo = best[k]["lo"]
        _, s_hi, t_hi = best[k]["hi"]
        s1, t1, neg_lo = _pattern_search(lambda a, b: -ckm_observables(ckm_matrix(coef, a, b))[k],
                                         s_lo, t_lo, two_pi / grid, min_step)
        s2, t2, hi = _pattern_search(lambda a, b: ckm_observables(ckm_matrix(coef, a, b))[k],
                                     s_hi, t_hi, two_pi / grid, min_step)
        bands[k] = {"lo": -neg_lo, "hi": hi,
                    "lo_phases": (s1 % two_pi, t1 % two_pi), "hi_phases": (s2 % two_pi, t2 % two_pi)}
    return bands


# =============================================================================
# 6b. TEXTURE SURVEY: every texture-zero pattern with at least one prediction
# =============================================================================
# Hermitian mass matrices, zeros counted per independent entry (a symmetric
# off-diagonal pair is one zero). Any pair of quark mass matrices can be made
# Hermitian by right-handed rotations, which leave the CKM matrix unchanged.
#
# A sector with 3 zeros has 3 nonzero entries, which its 3 masses fix exactly.
# With 2 zeros it has 4, leaving one free entry. Counting unknowns: 2 phases
# between the sectors, plus 1 per free entry, plus 1 per sector whose three
# off-diagonal entries are all nonzero (a phase that cannot be rotated away).
# The data are 4 numbers (|V_us|, |V_cb|, |V_ub|, J), so
# predictions = 4 - unknowns. Only patterns with at least one prediction (five
# or six zeros, no loop phase) are tested; the rest are counted.
#
# The unknowns are never given values. A pattern is tested in two steps:
#   1. Exact band test. For fixed rotations, each |V_ij| = |c0 + c1 e^(i s) + c2 e^(i t)|
#      sweeps exactly [max(0, 2 max|c| - sum|c|), sum|c|] over the phases. If any
#      measurement lies outside its band (with input and measurement errors) at
#      every value of the free entry, the pattern is excluded.
#   2. Joint test. Otherwise the script asks whether ANY point of the unknowns
#      reproduces all four data at once: it minimizes chi^2 over the unknowns and
#      converts it to a p-value with (predictions) degrees of freedom. This is a
#      hypothesis test. The point found is never reported as a determination and
#      never used anywhere else.
POSITIONS = ((0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2))
SURVEY_OBS = ("V_us", "V_cb", "V_ub", "J")
_ELEMENTS = {"V_us": (0, 1), "V_cb": (1, 2), "V_ub": (0, 2)}


def _comp(p: Tuple[int, int]) -> int:
    return 3 - p[0] - p[1]


def _invariants(e: Sequence[float]) -> Tuple[float, float, float]:
    return e[0] + e[1] + e[2], e[0] * e[1] + e[0] * e[2] + e[1] * e[2], e[0] * e[1] * e[2]


def _poly_coeffs(g: Callable[[float], float]) -> List[float]:
    """Coefficients of a polynomial of degree <= 3 from its values at 0, +-1, +-2.

    c0 = g(0) is read directly: rebuilding it from values at +-1, +-2 cancels O(1)
    terms down to a constant that can be ~1e-8 (the determinant of a hierarchical
    sector), losing most of its digits. The rest splits into odd and even parts."""
    c0 = g(0)
    o1, o2 = (g(1) - g(-1)) / 2, (g(2) - g(-2)) / 2            # c1 x + c3 x^3
    e1, e2 = (g(1) + g(-1)) / 2 - c0, (g(2) + g(-2)) / 2 - c0  # c2 x^2
    c3 = (o2 - 2 * o1) / 6
    return [c0, o1 - c3, (4 * e1 + e2) / 8, c3]


def real_roots(coefs: Sequence[float]) -> List[float]:
    """All real roots of sum c_k x^k: monotone brackets between critical points, then bisection."""
    c = list(coefs)
    scale = max(abs(v) for v in c) or 1
    while len(c) > 1 and abs(c[-1]) <= scale * num("root_trim_rel"):
        c.pop()
    deg = len(c) - 1
    if deg <= 0:
        return []
    if deg == 1:
        return [-c[0] / c[1]]

    def f(x: float) -> float:
        return sum(ck * x ** k for k, ck in enumerate(c))
    bound = 1 + max(abs(ck / c[-1]) for ck in c[:-1])
    crit = sorted(r for r in real_roots([k * c[k] for k in range(1, len(c))]) if -bound < r < bound)
    pts = [-bound] + crit + [bound]
    roots = []
    for a, b in zip(pts[:-1], pts[1:]):
        fa, fb = f(a), f(b)
        if fa == 0:
            roots.append(a)
            continue
        if (fa < 0) == (fb < 0):
            continue
        while True:
            m = (a + b) / 2
            if m in (a, b):
                break
            fm = f(m)
            if fm == 0:
                a = b = m
                break
            if (fa < 0) == (fm < 0):
                a, fa = m, fm
            else:
                b = m
        roots.append((a + b) / 2)
    if f(bound) == 0:
        roots.append(bound)
    out: List[float] = []
    for r in sorted(roots):
        if not out or abs(r - out[-1]) > num("root_merge_rel") * max(1, abs(r)):
            out.append(r)
    return out


def _sym_matrix(d: Dict[int, float], q: Dict[Tuple[int, int], float]) -> List[List[float]]:
    m = [[0.0] * 3 for _ in range(3)]
    for i, v in d.items():
        m[i][i] = v
    for p, v in q.items():
        m[p[0]][p[1]] = m[p[1]][p[0]] = math.sqrt(max(v, 0))
    return m


def _invariant_residual(m: List[List[float]], e: Sequence[float]) -> float:
    t, s2, det = _invariants(e)
    tr = m[0][0] + m[1][1] + m[2][2]
    minors = sum(m[i][i] * m[j][j] - m[i][j] ** 2 for i, j in ((0, 1), (0, 2), (1, 2)))
    dt = (m[0][0] * (m[1][1] * m[2][2] - m[1][2] ** 2) - m[0][1] * (m[0][1] * m[2][2] - m[1][2] * m[0][2])
          + m[0][2] * (m[0][1] * m[1][2] - m[1][1] * m[0][2]))
    # relative to each invariant: the determinant of a hierarchical sector is ~1e-8
    return max(abs(tr - t) / max(abs(v) for v in e), abs(minors - s2) / abs(s2), abs(dt - det) / abs(det))


def _q_solve(d: Dict[int, float], offs: Sequence[Tuple[int, int]], e: Sequence[float]):
    """Squared off-diagonal entries from the invariants, which are linear in them (no loop)."""
    _, s2, det = _invariants(e)
    dd = [d.get(i, 0) for i in range(3)]
    r1 = dd[0] * dd[1] + dd[0] * dd[2] + dd[1] * dd[2] - s2      # = sum of q
    r2 = dd[0] * dd[1] * dd[2] - det                              # = sum of d_comp(q) q
    if len(offs) == 2:
        a, b = offs
        ca, cb = dd[_comp(a)], dd[_comp(b)]
        if cb == ca:
            return None
        qb = (r2 - ca * r1) / (cb - ca)
        return {a: r1 - qb, b: qb}
    if len(offs) == 1:
        return {offs[0]: r1}
    return {}


def _split(nonzero: Sequence[Tuple[int, int]]):
    return [p[0] for p in nonzero if p[0] == p[1]], [p for p in nonzero if p[0] != p[1]]


def family_kinds(nonzero: Sequence[Tuple[int, int]]):
    """The solution families of a sector with these nonzero entries, or 'loop'."""
    diags, offs = _split(nonzero)
    if len(offs) == 3:
        return "loop"
    if len(nonzero) == 3:
        if len(diags) == 1:
            return [("fixed", 0)]
        if len(diags) == 2:
            return [("root", k) for k in range(3)]
        return [("perm", k) for k in range(6)]
    if len(diags) == 2:
        return [("curve", k) for k in range(3)]          # one free diagonal entry, q's linear
    return [("block", m) for m in range(3)]               # one state decouples with eigenvalue e_m


def fixed_matrix(nonzero, kind: str, br: int, e: Sequence[float]):
    diags, offs = _split(nonzero)
    t, _, det = _invariants(e)
    if kind == "fixed":
        d = {diags[0]: t}
        q = _q_solve(d, offs, e)
    elif kind == "root":
        i, j = diags
        a = offs[0]

        def g(x: float) -> float:
            dx = {i: x, j: t - x}
            qq = _q_solve(dx, offs, e)
            v = [dx.get(k, 0) for k in range(3)]
            return v[0] * v[1] * v[2] - v[_comp(a)] * qq[a] - det
        rts = real_roots(_poly_coeffs(g))
        if br >= len(rts):
            return None
        d = {i: rts[br], j: t - rts[br]}
        q = _q_solve(d, offs, e)
    else:
        perm = list(itertools.permutations(range(3)))[br]
        d = {k: e[perm[k]] for k in range(3)}
        q = {}
    if q is None or any(v < 0 for v in q.values()):
        return None
    m = _sym_matrix(d, q)
    return m if _invariant_residual(m, e) < num("survey_residual_tol") else None


def curve_interval(nonzero, kind: str, br: int, e: Sequence[float]):
    """The br-th interval of the free diagonal entry on which every q >= 0 (|entries| <= 1)."""
    diags, offs = _split(nonzero)
    t, s2, det = _invariants(e)
    if kind == "block":
        others = [e[i] for i in range(3) if i != br]
        return (min(others), max(others))
    i, j = diags
    a, b = offs

    def dd(x: float) -> List[float]:
        return [{i: x, j: t - x}.get(k, 0) for k in range(3)]

    def den(x: float) -> float:
        v = dd(x)
        return v[_comp(b)] - v[_comp(a)]

    def r1(x: float) -> float:
        v = dd(x)
        return v[0] * v[1] + v[0] * v[2] + v[1] * v[2] - s2

    def nb(x: float) -> float:
        v = dd(x)
        return (v[0] * v[1] * v[2] - det) - v[_comp(a)] * r1(x)

    def na(x: float) -> float:
        return r1(x) * den(x) - nb(x)

    breaks = {-1, 1}
    for f in (den, nb, na):
        breaks |= {r for r in real_roots(_poly_coeffs(f)) if -1 < r < 1}
    breaks_sorted = sorted(breaks)
    ivs: List[Tuple[float, float]] = []
    for lo, hi in zip(breaks_sorted[:-1], breaks_sorted[1:]):
        q = _q_solve({i: (lo + hi) / 2, j: t - (lo + hi) / 2}, offs, e)
        if q is not None and all(v >= 0 for v in q.values()):
            if ivs and ivs[-1][1] == lo:
                ivs[-1] = (ivs[-1][0], hi)
            else:
                ivs.append((lo, hi))
    return ivs[br] if br < len(ivs) else None


def curve_matrix(nonzero, kind: str, br: int, e: Sequence[float], t_unit: float):
    """The matrix at relative position t_unit in [0, 1] along the family (Chebyshev spacing)."""
    iv = curve_interval(nonzero, kind, br, e)
    if iv is None:
        return None
    x = iv[0] + (iv[1] - iv[0]) * (1 - math.cos(math.pi * t_unit)) / 2
    diags, offs = _split(nonzero)
    t, _, _ = _invariants(e)
    if kind == "block":
        a = offs[0]
        others = [e[i] for i in range(3) if i != br]
        d = {_comp(a): e[br], a[0]: x, a[1]: sum(others) - x}
        q = {a: x * (sum(others) - x) - others[0] * others[1]}
    else:
        i, j = diags
        d = {i: x, j: t - x}
        q = _q_solve(d, offs, e)
    if q is None:
        return None
    m = _sym_matrix(d, q)
    return m if _invariant_residual(m, e) < num("survey_residual_tol") else None


def _sector_matrix(nonzero, var, e_abs: Sequence[float], t_unit: float):
    signs, kind, br = var
    e = (signs[0] * e_abs[0], signs[1] * e_abs[1], e_abs[2])
    if kind in ("curve", "block"):
        return curve_matrix(nonzero, kind, br, e, t_unit)
    return fixed_matrix(nonzero, kind, br, e)


def sector_variants(nonzero, e_abs: Sequence[float]):
    """Every (eigenvalue signs, family, branch) with a real solution; 'loop' if a phase survives.
    The overall sign is fixed by the heaviest eigenvalue being positive (it does not change V)."""
    kinds = family_kinds(nonzero)
    if kinds == "loop":
        return "loop"
    out = []
    for signs in itertools.product((1, -1), repeat=2):
        e = (signs[0] * e_abs[0], signs[1] * e_abs[1], e_abs[2])
        for kind, br in kinds:
            ok = (curve_interval(nonzero, kind, br, e) if kind in ("curve", "block")
                  else fixed_matrix(nonzero, kind, br, e))
            if ok is not None:
                out.append((signs, kind, br))
    return out


def _permute_pattern(zeros, perm):
    return tuple(sorted(tuple(sorted((perm[i], perm[j]))) for i, j in zeros))


def pattern_class(zu, zd, perms=None):
    """Canonical representative of (zeros_u, zeros_d) under simultaneous index permutations,
    which are weak-basis changes and leave the CKM matrix unchanged."""
    perms = perms or list(itertools.permutations(range(3)))
    return min((_permute_pattern(zu, p), _permute_pattern(zd, p)) for p in perms)


def pattern_mask(zeros) -> str:
    rows = []
    for i in range(3):
        rows.append("".join("0" if tuple(sorted((i, j))) in zeros else "X" for j in range(3)))
    return "/".join(rows)


def _eigen_ratios(r: Dict[str, float]) -> Dict[str, Tuple[float, float, float]]:
    return {"u": (r["r_uc"] * r["r_ct"], r["r_ct"], 1.0), "d": (r["r_ds"] * r["r_sb"], r["r_sb"], 1.0)}


def _magnitude_band(coef, ij: Tuple[int, int]) -> Tuple[float, float]:
    c = [abs(v) for v in coef[ij[0]][ij[1]]]
    s = sum(c)
    return max(0, 2 * max(c) - s), s


def _survey_obs(coef, s: float, t: float) -> Tuple[float, float, float, float]:
    p1, p2 = cmath.exp(1j * s), cmath.exp(1j * t)

    def v(i: int, j: int) -> complex:
        c = coef[i][j]
        return c[0] + c[1] * p1 + c[2] * p2
    vus, vcb, vub, vcs = v(0, 1), v(1, 2), v(0, 2), v(1, 1)
    return abs(vus), abs(vcb), abs(vub), (vus * vcb * vub.conjugate() * vcs.conjugate()).imag


def _minimize(f: Callable[[List[float]], float], x: List[float], steps: List[float],
              min_step: float) -> Tuple[List[float], float]:
    """Compass search: deterministic, derivative-free."""
    best = f(x)
    steps = list(steps)
    while max(steps) > min_step:
        moved = False
        for d in range(len(x)):
            if steps[d] == 0:
                continue
            for sgn in (1, -1):
                y = list(x)
                y[d] += sgn * steps[d]
                v = f(y)
                if v < best:
                    best, x, moved = v, y, True
                    break
            if moved:
                break
        if not moved:
            steps = [s / 2 for s in steps]
    return x, best


def chi2_pvalue(chi2: float, dof: int) -> float:
    """Upper tail of the chi^2 distribution for integer dof (closed forms)."""
    if dof <= 0:
        return math.nan
    h = chi2 / 2
    if dof % 2 == 0:
        return math.exp(-h) * sum(h ** j / math.factorial(j) for j in range(dof // 2))
    tail = sum(h ** (j - 1 / 2) / math.gamma(j + 1 / 2) for j in range(1, (dof - 1) // 2 + 1))
    return math.erfc(math.sqrt(h)) + math.exp(-h) * tail


def pvalue_to_sigma(p: float) -> float:
    """Two-sided Gaussian equivalent: erfc(n / sqrt2) = p."""
    if p <= 0:
        return math.inf
    lo, hi = 0.0, 40.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if math.erfc(mid / math.sqrt(2)) > p:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


class TextureSurvey:
    """All texture pairs with >= 1 prediction at one evaluation scale."""

    def __init__(self, ratios_central: Dict[str, float], ratios_varied: Sequence[Tuple[Dict, Dict]]):
        self.E = [_eigen_ratios(ratios_central)]
        for plus, minus in ratios_varied:
            self.E += [_eigen_ratios(plus), _eigen_ratios(minus)]
        self.cache: Dict[Any, Any] = {}
        self.meas = {k: _comparison(k) for k in SURVEY_OBS}

    def rotation(self, sector: str, nonzero, var, ei: int, t_unit: float):
        key = (sector, tuple(nonzero), var, ei, t_unit)
        if key not in self.cache:
            m = _sector_matrix(nonzero, var, self.E[ei][sector], t_unit)
            self.cache[key] = None if m is None else jacobi_eigh(m, num("jacobi_tol"))[1]
        return self.cache[key]

    def coef(self, pair, t_unit: float, ei: int = 0):
        nu, vu, nd, vd = pair
        ou = self.rotation("u", nu, vu, ei, t_unit if vu[1] in ("curve", "block") else 0)
        od = self.rotation("d", nd, vd, ei, t_unit if vd[1] in ("curve", "block") else 0)
        return None if ou is None or od is None else ckm_coefficients(ou, od)

    def input_sigma(self, pair, f, t_unit: float) -> float:
        v2 = 0.0
        for k in range(1, len(self.E), 2):
            cp, cm = self.coef(pair, t_unit, k), self.coef(pair, t_unit, k + 1)
            if cp is not None and cm is not None:
                v2 += ((f(cp) - f(cm)) / 2) ** 2
        return math.sqrt(v2)

    def band_distance(self, pair, t_unit: float) -> float:
        """Largest n-sigma distance of a measured |V_ij| from its exact phase band."""
        c = self.coef(pair, t_unit)
        if c is None:
            return math.inf
        worst = 0.0
        for k, ij in _ELEMENTS.items():
            lo, hi = _magnitude_band(c, ij)
            m, up, dn = self.meas[k]
            if lo <= m <= hi:
                continue
            edge = 0 if m < lo else 1
            s = self.input_sigma(pair, lambda cc: _magnitude_band(cc, ij)[edge], t_unit)
            n = (lo - m) / math.hypot(s, up) if m < lo else (m - hi) / math.hypot(s, dn)
            worst = max(worst, n)
        return worst

    def chi2(self, o: Sequence[float], sig_in: Sequence[float]) -> float:
        tot = 0.0
        for k, val, si in zip(SURVEY_OBS, o, sig_in):
            m, up, dn = self.meas[k]
            tot += ((val - m) / math.hypot(up if val > m else dn, si)) ** 2
        return tot

    def joint(self, pair, n_curve: int, nt: int, nph: int):
        ts = [(i + 1 / 2) / nt for i in range(nt)] if n_curve else [0]
        zero = (0, 0, 0, 0)
        starts = []
        for t in ts:
            c = self.coef(pair, t)
            if c is None:
                continue
            for i in range(nph):
                for j in range(nph):
                    s, u = 2 * math.pi * i / nph, 2 * math.pi * j / nph
                    starts.append((self.chi2(_survey_obs(c, s, u), zero), t, s, u))
        starts.sort()

        def f(x: List[float], sig: Sequence[float]) -> float:
            if n_curve and not 0 <= x[0] <= 1:
                return math.inf
            c = self.coef(pair, x[0] if n_curve else 0)
            return math.inf if c is None else self.chi2(_survey_obs(c, x[1], x[2]), sig)
        best = (math.inf, None)
        for _, t, s, u in starts[:int(num("survey_starts"))]:
            x, sig = [t, s, u], zero
            for _ in range(int(num("survey_sigma_iterations"))):
                x, _ = _minimize(lambda y: f(y, sig), x,
                                 [1 / nt if n_curve else 0, 2 * math.pi / nph, 2 * math.pi / nph],
                                 num("survey_min_step"))
                sig = tuple(self.input_sigma(pair, lambda cc, k=k: _survey_obs(cc, x[1], x[2])[k],
                                             x[0] if n_curve else 0) for k in range(4))
            val = f(x, sig)
            if val < best[0]:
                best = (val, (x, sig))
        return best

    def bands(self, pair, n_curve: int, nt: int, nph: int) -> Dict[str, Tuple[float, float]]:
        """Range of each observable over ALL unknowns (free entry and both phases)."""
        ts = [(i + 1 / 2) / nt for i in range(nt)] if n_curve else [0]
        out = {}
        for k in range(4):
            res = []
            for sense in (1, -1):
                def f(x: List[float]) -> float:
                    if n_curve and not 0 <= x[0] <= 1:
                        return math.inf
                    c = self.coef(pair, x[0] if n_curve else 0)
                    return math.inf if c is None else sense * _survey_obs(c, x[1], x[2])[k]
                start = min(([t, 2 * math.pi * i / nph, 2 * math.pi * j / nph]
                             for t in ts for i in range(nph) for j in range(nph)), key=f)
                x, v = _minimize(f, start, [1 / nt if n_curve else 0, 2 * math.pi / nph, 2 * math.pi / nph],
                                 num("survey_min_step"))
                res.append(sense * v)
            out[SURVEY_OBS[k]] = (res[0], res[1])
        return out

    def prediction(self, rec: Dict[str, Any], nt: int, nph: int) -> List[Dict[str, float]]:
        """What a surviving pattern predicts. |V_us|, |V_cb|, |V_ub| fix its three unknowns (t and
        both phases) at isolated points, found from every grid point by compass search; at each,
        |J| and |V_td/V_ts| follow (CP-conjugate solutions, J -> -J, are merged). Errors: re-solve
        with each measured modulus moved by its error, and with each input moved by its error."""
        pair, n_curve = rec["pair"], rec["n_curve"]
        mods = SURVEY_OBS[:3]

        def at(x: List[float], ei: int = 0):
            if n_curve and not 0 <= x[0] <= 1:
                return None
            c = self.coef(pair, x[0] if n_curve else 0, ei)
            if c is None:
                return None
            v = ckm_matrix(c, x[1], x[2])
            return _survey_obs(c, x[1], x[2]), abs(v[2][0]) / abs(v[2][1])

        def solve(x0: List[float], target: Sequence[float], ei: int = 0):
            def f(x: List[float]) -> float:
                r = at(x, ei)
                if r is None:
                    return math.inf
                return sum(((r[0][k] - target[k]) / self.meas[name][1]) ** 2 for k, name in enumerate(mods))
            x, v = _minimize(f, list(x0), [1 / nt if n_curve else 0, 2 * math.pi / nph, 2 * math.pi / nph],
                             num("survey_min_step"))
            return x, v
        central = [self.meas[k][0] for k in mods]
        ts = [(i + 1 / 2) / nt for i in range(nt)] if n_curve else [0]
        starts = []
        for t in ts:
            for a in range(nph):
                for b in range(nph):
                    x = [t, 2 * math.pi * a / nph, 2 * math.pi * b / nph]
                    r = at(x)
                    if r is not None:
                        starts.append((sum(((r[0][k] - central[k]) / self.meas[n][1]) ** 2
                                           for k, n in enumerate(mods)), x))
        starts.sort(key=lambda z: z[0])
        sols: List[List[float]] = []
        tol = num("survey_residual_tol")
        for _, x0 in starts[:nt * int(num("survey_starts"))]:
            x, v = solve(x0, central)
            if v > tol:
                continue
            key = [x[0], x[1] % (2 * math.pi), x[2] % (2 * math.pi)]
            if all(sum(abs(a - b) for a, b in zip(key, y)) > tol for y in sols):
                sols.append(key)
        out: List[Dict[str, float]] = []
        for x in sols:
            r = at(x)
            j0, q0 = abs(r[0][3]), r[1]
            dj2 = dq2 = 0.0
            for k, name in enumerate(mods):                  # measured moduli moved by their errors
                tgt = list(central)
                tgt[k] += self.meas[name][1]
                xs, _ = solve(x, tgt)
                rs = at(xs)
                dj2 += (abs(rs[0][3]) - j0) ** 2
                dq2 += (rs[1] - q0) ** 2
            for e in range(1, len(self.E), 2):              # inputs moved by their errors
                pm = []
                for ei in (e, e + 1):
                    xs, _ = solve(x, central, ei)
                    rs = at(xs, ei)
                    pm.append(rs)
                dj2 += ((abs(pm[0][0][3]) - abs(pm[1][0][3])) / 2) ** 2
                dq2 += ((pm[0][1] - pm[1][1]) / 2) ** 2
            if not any(abs(j0 - o["J"]) < tol * j0 and abs(q0 - o["V_td/V_ts"]) < tol for o in out):
                out.append({"J": j0, "J_sigma": math.sqrt(dj2), "V_td/V_ts": q0, "V_td/V_ts_sigma": math.sqrt(dq2)})
        return sorted(out, key=lambda o: o["J"])

    def run(self, min_zeros: int) -> Dict[str, Any]:
        e = self.E[0]
        sector: Dict[Any, Dict[str, Any]] = {}
        for nz in (2, 3):
            for z in itertools.combinations(POSITIONS, nz):
                nonzero = [p for p in POSITIONS if p not in z]
                sector[tuple(sorted(z))] = {s: sector_variants(nonzero, e[s]) for s in ("u", "d")}
        classes: Dict[Any, List[Any]] = {}
        for zu, zd in itertools.product(sector, repeat=2):
            if len(zu) + len(zd) >= min_zeros:
                classes.setdefault(pattern_class(zu, zd), []).append((zu, zd))
        nt, nph = int(num("survey_curve_grid")), int(num("survey_phase_grid"))
        results = []
        for key in sorted(classes):
            zu, zd = key
            rec: Dict[str, Any] = {"zeros_u": zu, "zeros_d": zd, "zeros": len(zu) + len(zd),
                                   "orbit": len(classes[key])}
            vu, vd = sector[zu]["u"], sector[zd]["d"]
            if vu == "loop" or vd == "loop":
                rec["status"] = "loop"
                results.append(rec)
                continue
            if not vu or not vd:
                rec["status"] = "no_solution"
                results.append(rec)
                continue
            nu = [p for p in POSITIONS if p not in zu]
            nd = [p for p in POSITIONS if p not in zd]
            rec.update({"status": "tested", "band_sigma": math.inf, "chi2": math.inf, "variant": None})
            for a, b in itertools.product(vu, vd):
                pair = (nu, a, nd, b)
                n_curve = (a[1] in ("curve", "block")) + (b[1] in ("curve", "block"))
                rec["predictions"] = 4 - 2 - n_curve
                ts = [(i + 1 / 2) / nt for i in range(nt)] if n_curve else [0]
                bd = min(self.band_distance(pair, t) for t in ts)
                rec["band_sigma"] = min(rec["band_sigma"], bd)
                if bd > num("survival_sigma"):
                    continue
                c2, arg = self.joint(pair, n_curve, nt, nph)
                if c2 < rec["chi2"]:
                    rec.update({"chi2": c2, "variant": (a, b), "pair": pair, "n_curve": n_curve,
                                "input_sigma": arg[1]})
            if rec["chi2"] < math.inf:
                rec["sigma"] = pvalue_to_sigma(chi2_pvalue(rec["chi2"], rec["predictions"]))
            else:
                rec["sigma"] = rec["band_sigma"]
            rec["survives"] = rec["sigma"] <= num("survival_sigma")
            if rec["survives"]:
                rec["bands"] = self.bands(rec["pair"], rec["n_curve"], nt, nph)
                rec["prediction"] = self.prediction(rec, nt, nph)
            results.append(rec)
        return {"classes": results, "n_ordered_pairs": sum(len(v) for v in classes.values())}


# --- Part C certificates: is an exclusion true at EVERY point, not just where the search looked?
# The joint test and the band test of a family are evaluated at sampled points. A certificate
# covers the whole parameter space (position t along the family, both phases) with cells, and
# proves for each cell that no point in it can survive: a rigorous upper bound on how far every
# CKM element can move inside the cell gives a lower bound on its distance from the data.
#   * Matrix entries: along a family they are x, T - x, constants, or sqrt(N(x)/D(x)) with
#     polynomials N, D; their exact range on a cell comes from the endpoints and the roots of
#     N'D - N D' (found once per family), widened for rounding.
#   * Eigenvectors: every matrix of a family has the same eigenvalues (its invariants are
#     fixed). For the eigenvector v' of M + dM with eigenvalue lambda_i, its component along v_k
#     is a_k = v_k.dM.v' / (lambda_i - lambda_k), so |a_k| <= (|v_k.dM.v_i| + |dM| s) / gap_ik
#     with s = |v' - v_i| <= A + A^2, A = sum |a_k|: solved as a quadratic inequality.
#   * CKM elements: V_ij = u_i.P.d_j with P = diag(1, e^is, e^it), so the change of V_ij is at
#     most sum_k |a_k| B_kj + sum_l |b_l| B_il + (eta_u + eta_d + eta_u eta_d) B_ij + A_u A_d,
#     B_kl = sum of |coefficients| >= |V_kl| at any phase; a phase step dp moves V_ij by at
#     most |c_1| dp_1 + |c_2| dp_2; J from the product of the four disks.
#   * Input errors: the input-induced sigma is bounded above by the same radii.
# A cell is discarded if its band distance or its chi^2 is provably above the 3-sigma level;
# otherwise it is split (along t while the eigenvector part dominates, else the phases).
class _Iv:
    """A closed interval, widened outward by cert_round_rel at every operation."""
    __slots__ = ("lo", "hi")

    def __init__(self, lo: float, hi: float | None = None):
        hi = lo if hi is None else hi
        w = num("cert_round_rel") * max(abs(lo), abs(hi))
        self.lo, self.hi = lo - w, hi + w


def _padd(a: List[float], b: List[float]) -> List[float]:
    n = max(len(a), len(b))
    return [(a[k] if k < len(a) else 0) + (b[k] if k < len(b) else 0) for k in range(n)]


def _pneg(a: List[float]) -> List[float]:
    return [-v for v in a]


def _pmul(a: List[float], b: List[float]) -> List[float]:
    out = [0.0] * (len(a) + len(b) - 1)
    for i, u in enumerate(a):
        for j, w in enumerate(b):
            out[i + j] += u * w
    return out


def _pval(a: List[float], x: float) -> float:
    return sum(c * x ** k for k, c in enumerate(a))


def _pabs(a: List[float], x: float) -> float:
    return sum(abs(c) * abs(x) ** k for k, c in enumerate(a))


def _pder(a: List[float]) -> List[float]:
    return [k * a[k] for k in range(1, len(a))] or [0.0]


def _family_polys(nonzero, kind: str, br: int, e: Sequence[float]):
    """Diagonal entries as polynomials in x, and the squared off-diagonals as (position, N, D,
    critical points of N/D)."""
    diags, offs = _split(nonzero)
    t_, s2, det = _invariants(e)
    if kind == "block":
        a = offs[0]
        others = [e[i] for i in range(3) if i != br]
        tot = sum(others)
        dg = {_comp(a): [e[br]], a[0]: [0.0, 1.0], a[1]: [tot, -1.0]}
        qs = [(a, [-others[0] * others[1], tot, -1.0], [1.0])]
    else:
        i, j = diags
        a, b = offs
        dd: List[List[float]] = [[0.0], [0.0], [0.0]]
        dd[i], dd[j] = [0.0, 1.0], [t_, -1.0]
        r1 = _padd(_padd(_padd(_pmul(dd[0], dd[1]), _pmul(dd[0], dd[2])), _pmul(dd[1], dd[2])), [-s2])
        r2 = _padd(_pmul(_pmul(dd[0], dd[1]), dd[2]), [-det])
        ca, cb = dd[_comp(a)], dd[_comp(b)]
        nb, den = _padd(r2, _pneg(_pmul(ca, r1))), _padd(cb, _pneg(ca))
        dg = {k: dd[k] for k in range(3)}
        qs = [(a, _padd(_pmul(r1, den), _pneg(nb)), den), (b, nb, den)]
    out = []
    for pos, n_, d_ in qs:
        k_ = _padd(_pmul(_pder(n_), d_), _pneg(_pmul(n_, _pder(d_))))
        out.append((pos, n_, d_, sorted(real_roots(k_)) if any(k_) else []))
    return dg, out


def _rational_range(n_: List[float], d_: List[float], crit: Sequence[float], x0: float, x1: float):
    pts = [x0, x1] + [r for r in crit if x0 < r < x1]
    vals, wid = [], 0.0
    for x in pts:
        d = _pval(d_, x)
        vals.append(_pval(n_, x) / d)
        wid = max(wid, num("cert_eval_rel") * (_pabs(n_, x) + abs(vals[-1]) * _pabs(d_, x)) / abs(d))
    return min(vals) - wid, max(vals) + wid


class _Certifier:
    """Rigorous exclusion of one pattern pair over all of (t, sigma, tau), see the comment above."""
    ELEM = {"V_us": (0, 1), "V_cb": (1, 2), "V_ub": (0, 2), "V_cs": (1, 1)}

    def __init__(self, sv: "TextureSurvey"):
        self.sv = sv
        self.cache: Dict[Any, Any] = {}

    def _sector(self, nonzero, var, e_abs: Sequence[float], ta: float, tb: float):
        """(matrix at the cell centre, entrywise bound on its change over the cell) or None."""
        signs, kind, br = var
        e = (signs[0] * e_abs[0], signs[1] * e_abs[1], e_abs[2])
        key = (tuple(nonzero), var, tuple(e_abs))
        if kind not in ("curve", "block"):
            if key not in self.cache:
                self.cache[key] = fixed_matrix(nonzero, kind, br, e)
            m = self.cache[key]
            return None if m is None else (m, [[0.0] * 3 for _ in range(3)])
        if key not in self.cache:
            iv = curve_interval(nonzero, kind, br, e)
            self.cache[key] = (iv, None if iv is None else _family_polys(nonzero, kind, br, e))
        iv, polys = self.cache[key]
        if iv is None:
            return None

        def x_of(t: float) -> float:
            return iv[0] + (iv[1] - iv[0]) * (1 - math.cos(math.pi * t)) / 2
        xc, x0, x1 = x_of((ta + tb) / 2), x_of(ta), x_of(tb)
        dg, qs = polys
        mc = [[0.0] * 3 for _ in range(3)]
        dev = [[0.0] * 3 for _ in range(3)]
        for k, pk in dg.items():
            mc[k][k] = _pval(pk, xc)
            lo, hi = sorted((_pval(pk, x0), _pval(pk, x1)))
            r = _Iv(lo, hi)
            dev[k][k] = max(r.hi - mc[k][k], mc[k][k] - r.lo)
        for pos, n_, d_, crit in qs:
            v = math.sqrt(max(_pval(n_, xc) / _pval(d_, xc), 0))
            lo, hi = _rational_range(n_, d_, crit, x0, x1)
            r = _Iv(math.sqrt(max(lo, 0)), math.sqrt(max(hi, 0)))
            for p_ in (pos, pos[::-1]):
                mc[p_[0]][p_[1]] = v
                dev[p_[0]][p_[1]] = max(r.hi - v, v - r.lo)
        return mc, dev

    @staticmethod
    def _components(mc, dev):
        """Eigenvectors at the centre and, for each, bounds on its components along the others
        and on eta over the cell (None where the bound does not close)."""
        ev, o = jacobi_eigh(mc, num("jacobi_tol"))
        vec = [[o[r][i] for r in range(3)] for i in range(3)]
        dn = math.sqrt(sum(dev[r][c] ** 2 for r in range(3) for c in range(3)))
        comps = []
        for i in range(3):
            rk, alpha, beta = {}, 0.0, 0.0
            for k in range(3):
                if k == i:
                    continue
                g = abs(ev[i] - ev[k])
                rk[k] = (sum(abs(vec[k][r]) * dev[r][c] * abs(vec[i][c]) for r in range(3) for c in range(3)), g)
                alpha += rk[k][0] / g
                beta += dn / g
            s1 = None
            if beta < 1:
                qa, qb, qc = beta * beta, 2 * alpha * beta + beta - 1, alpha + alpha * alpha
                if qa == 0:
                    s1 = qc / -qb
                elif qb * qb - 4 * qa * qc >= 0:
                    rt = math.sqrt(qb * qb - 4 * qa * qc)
                    s1 = (-qb - rt) / (2 * qa) if (-qb + rt) / (2 * qa) > math.sqrt(2) else None
            if s1 is None or s1 >= 1:
                comps.append(None)
                continue
            a = {k: (r + dn * s1) / g for k, (r, g) in rk.items()}
            comps.append((a, min(1.0, sum(a.values()) ** 2)))
        return o, comps

    def tdata(self, pair, ta: float, tb: float):
        """For the central inputs and every input variation: CKM coefficients at the cell centre
        and the radius of each element over the cell (any phase)."""
        nu, vu, nd, vd = pair
        out = []
        for e in self.sv.E:
            su, sd = self._sector(nu, vu, e["u"], ta, tb), self._sector(nd, vd, e["d"], ta, tb)
            if su is None or sd is None:
                return None
            ou, cu = self._components(*su)
            od, cd = self._components(*sd)
            coef = ckm_coefficients(ou, od)
            bnd = [[sum(abs(x) for x in coef[i][j]) for j in range(3)] for i in range(3)]
            rad = {}
            for k, (i, j) in self.ELEM.items():
                if cu[i] is None or cd[j] is None:
                    rad[k] = 2.0
                    continue
                (au, etu), (ad, etd) = cu[i], cd[j]
                rad[k] = min(2.0, (etu + etd + etu * etd) * bnd[i][j] + sum(v * bnd[m][j] for m, v in au.items())
                             + sum(v * bnd[i][m] for m, v in ad.items()) + sum(au.values()) * sum(ad.values()))
            out.append((coef, rad))
        return out

    def _obs(self, coef, rad, sc: float, tc: float, hs: float, ht: float) -> Dict[str, Tuple[float, float, float, float]]:
        """(lower, upper, centre value, radius) of each survey observable over the cell."""
        p = (1, cmath.exp(1j * sc), cmath.exp(1j * tc))
        z = {}
        for k, (i, j) in self.ELEM.items():
            c = coef[i][j]
            z[k] = (sum(c[m] * p[m] for m in range(3)), rad[k] + abs(c[1]) * hs + abs(c[2]) * ht)
        out = {k: (max(0, abs(z[k][0]) - z[k][1]), abs(z[k][0]) + z[k][1], abs(z[k][0]), z[k][1])
               for k in ("V_us", "V_cb", "V_ub")}
        zs = [z["V_us"], z["V_cb"], z["V_ub"], z["V_cs"]]
        jc = (zs[0][0] * zs[1][0] * zs[2][0].conjugate() * zs[3][0].conjugate()).imag
        jr = math.prod(abs(v) + r for v, r in zs) - math.prod(abs(v) for v, _ in zs)
        out["J"] = (jc - jr, jc + jr, jc, jr)
        return out

    def _sigma_up(self, per_e: List[Any], k: str, idx: int) -> float:
        """Upper bound on the input-induced sigma: centre differences plus both radii."""
        v2 = 0.0
        for a in range(1, len(per_e), 2):
            v2 += ((abs(per_e[a][k][idx] - per_e[a + 1][k][idx]) + per_e[a][k][3] + per_e[a + 1][k][3]) / 2) ** 2
        return math.sqrt(v2)

    def chi2_lower(self, td, sc: float, tc: float, hs: float, ht: float) -> float:
        per_e = [self._obs(c, r, sc, tc, hs, ht) for c, r in td]
        tot = 0.0
        for k in SURVEY_OBS:
            lo, hi = per_e[0][k][0], per_e[0][k][1]
            m, up, dn = self.sv.meas[k]
            if lo <= m <= hi:
                continue
            s = self._sigma_up(per_e, k, 2)
            tot += ((lo - m) / math.hypot(up, s)) ** 2 if m < lo else ((m - hi) / math.hypot(dn, s)) ** 2
        return tot

    def band_lower(self, td, with_radii: bool = True) -> float:
        """Lower bound on the largest band distance of |V_us|, |V_cb|, |V_ub| over the cell."""
        worst = 0.0
        for k in ("V_us", "V_cb", "V_ub"):
            ij = self.ELEM[k]
            per_e = []
            for coef, rad in td:
                lo, hi = _magnitude_band(coef, ij)
                r = rad[k] if with_radii else 0.0
                per_e.append({k: (lo - r, hi + r, lo, r, hi)})
            lo, hi = per_e[0][k][0], per_e[0][k][1]
            m, up, dn = self.sv.meas[k]
            if lo <= m <= hi:
                continue
            v2 = 0.0
            edge = 2 if m < lo else 4
            for a in range(1, len(per_e), 2):
                v2 += ((abs(per_e[a][k][edge] - per_e[a + 1][k][edge]) + per_e[a][k][3] + per_e[a + 1][k][3]) / 2) ** 2
            s = math.sqrt(v2)
            worst = max(worst, (lo - m) / math.hypot(s, up) if m < lo else (m - hi) / math.hypot(s, dn))
        return worst

    def certify(self, pair, n_curve: int, dof: int) -> Tuple[bool, int]:
        """True if no point of the pair's parameter space survives; also the cells used."""
        sig3 = num("survival_sigma")
        lo_, hi_ = 0.0, 100 * sig3 * sig3
        for _ in range(int(num("crit_iterations"))):       # the chi^2 at the 3-sigma level
            mid = (lo_ + hi_) / 2
            lo_, hi_ = (mid, hi_) if pvalue_to_sigma(chi2_pvalue(mid, dof)) < sig3 else (lo_, mid)
        thr = hi_
        nt = int(num("survey_curve_grid"))
        two_pi = 2 * math.pi
        stack = [("b", i / nt, (i + 1) / nt, 0.0, two_pi, 0.0, two_pi) for i in range(nt)] if n_curve \
            else [("j", 0.0, 0.0, 0.0, two_pi, 0.0, two_pi)]
        tcache: Dict[Tuple[float, float], Any] = {}
        n, budget, wmin = 0, int(num("cert_budget")), num("cert_min_width")
        while stack:
            n += 1
            if n > budget:
                return False, n
            mode, ta, tb, s0, s1, u0, u1 = stack.pop()
            if (ta, tb) not in tcache:
                tcache[(ta, tb)] = self.tdata(pair, ta, tb)
            td = tcache[(ta, tb)]
            mid = (ta + tb) / 2
            if td is None:
                if tb - ta < wmin:
                    return False, n
                stack += [(mode, ta, mid, s0, s1, u0, u1), (mode, mid, tb, s0, s1, u0, u1)]
                continue
            if self.band_lower(td) > sig3:
                continue
            if mode == "b":                                   # phase-independent: refine t only
                if self.band_lower(td, False) > sig3 and tb - ta > wmin:
                    stack += [("b", ta, mid, s0, s1, u0, u1), ("b", mid, tb, s0, s1, u0, u1)]
                else:
                    stack.append(("j", ta, tb, s0, s1, u0, u1))
                continue
            hs, hu = (s1 - s0) / 2, (u1 - u0) / 2
            if self.chi2_lower(td, s0 + hs, u0 + hu, hs, hu) > thr:
                continue
            point = [(c, {k: 0.0 for k in r}) for c, r in td]          # the cell centre itself
            if self.band_lower(point) <= sig3 and self.chi2_lower(point, s0 + hs, u0 + hu, 0, 0) <= thr:
                return False, n                                       # a surviving point: not excluded
            tr = max(td[0][1].values())
            pr = max(abs(td[0][0][i][j][1]) * hs + abs(td[0][0][i][j][2]) * hu for i, j in self.ELEM.values())
            if n_curve and tr > pr and tb - ta > wmin:
                stack += [("j", ta, mid, s0, s1, u0, u1), ("j", mid, tb, s0, s1, u0, u1)]
            elif hs >= hu:
                stack += [("j", ta, tb, s0, s0 + hs, u0, u1), ("j", ta, tb, s0 + hs, s1, u0, u1)]
            else:
                stack += [("j", ta, tb, s0, s1, u0, u0 + hu), ("j", ta, tb, s0, s1, u0 + hu, u1)]
        return True, n


def _certify_class(args) -> Dict[str, Any]:
    sv, rec = args
    e = sv.E[0]
    nu = [p for p in POSITIONS if p not in rec["zeros_u"]]
    nd = [p for p in POSITIONS if p not in rec["zeros_d"]]
    cert, cells = _Certifier(sv), 0
    for a, b in itertools.product(sector_variants(nu, e["u"]), sector_variants(nd, e["d"])):
        n_curve = (a[1] in ("curve", "block")) + (b[1] in ("curve", "block"))
        ok, n = cert.certify((nu, a, nd, b), n_curve, rec["predictions"])
        cells += n
        if not ok:
            return {"zeros_u": rec["zeros_u"], "zeros_d": rec["zeros_d"], "certified": False, "cells": cells}
    return {"zeros_u": rec["zeros_u"], "zeros_d": rec["zeros_d"], "certified": True, "cells": cells}


def certify_survey(survey_at_scale: Dict[str, Any]) -> Dict[str, Any]:
    """Certify every exclusion of one scale's survey (all variants of each class), in parallel
    where the platform can fork."""
    sv = survey_at_scale["survey"]
    todo = [(sv, r) for r in survey_at_scale["classes"] if r["status"] == "tested" and not r["survives"]]
    t0 = time.perf_counter()
    try:
        import multiprocessing
        with multiprocessing.get_context("fork").Pool() as pool:
            results = pool.map(_certify_class, todo, chunksize=1)
    except (ValueError, OSError, ImportError):
        results = [_certify_class(a) for a in todo]
    return {"results": results, "certified": sum(r["certified"] for r in results), "excluded": len(results),
            "seconds": time.perf_counter() - t0}


# =============================================================================
# 6c. WHAT THE 3-3-1 GAUGE SYMMETRY SAYS ABOUT THE QUARK MASS MATRICES
# =============================================================================
def triplet_charges(b: int, x: Fr, anti: bool = False) -> Tuple[Fr, Fr, Fr]:
    """Q = T3 + beta T8 + X on an SU(3)_L (anti)triplet; with beta = b/sqrt3, beta T8 = (b/6) diag(1,1,-2)."""
    t3 = (Fr(1, 2), Fr(-1, 2), Fr(0))
    t8 = (Fr(b, 6), Fr(b, 6), Fr(-2 * b, 6))
    s = -1 if anti else 1
    return tuple(s * a + s * c + x for a, c in zip(t3, t8))


def model_331(b: int) -> Tuple[Dict[int, Dict[str, Any]], Dict[Fr, Dict[str, Any]]]:
    """Quarks and scalars of the 3-3-1 model with beta = b/sqrt3 (b = +1 or -1).

    Anomaly cancellation puts two families in antitriplets, (d, -u, exotic), and one in a
    triplet, (u, d, exotic). X is fixed by the first component: u has 2/3, d has -1/3.
    Scalars: one triplet for each component that can hold a neutral vev."""
    x3 = Fr(2, 3) - triplet_charges(b, Fr(0))[0]
    xa = Fr(-1, 3) - triplet_charges(b, Fr(0), anti=True)[0]
    quarks = {f: {"rep": "3bar", "X": xa, "content": ("d", "u", "exotic")} for f in (1, 2)}
    quarks[3] = {"rep": "3", "X": x3, "content": ("u", "d", "exotic")}
    for q in quarks.values():
        q["charges"] = triplet_charges(b, q["X"], anti=q["rep"] == "3bar")
    scalars: Dict[Fr, Dict[str, Any]] = {}
    for k in range(3):
        x = -triplet_charges(b, Fr(0))[k]
        ch = triplet_charges(b, x)
        scalars.setdefault(x, {"X": x, "charges": ch, "neutral": [i for i in range(3) if ch[i] == 0]})
    return quarks, scalars


def yukawa_structure_331(b: int) -> Dict[str, Any]:
    """Which entries of the quark mass matrices the gauge symmetry allows, and from which vev."""
    quarks, scalars = model_331(b)
    singlet_x = {"u": Fr(-2, 3), "d": Fr(1, 3)}        # X of u^c and d^c (all families alike)
    table = {}
    for fam, q in quarks.items():
        for flav, xc in singlet_x.items():
            ops = []
            for x, s in scalars.items():
                conj = q["rep"] == "3"                   # 3 x 3bar: a triplet quark needs S*
                if q["X"] + (-x if conj else x) + xc != 0:
                    continue
                for k in s["neutral"]:
                    if q["content"][k] == flav:
                        ops.append({"scalar_X": x, "conjugate": conj, "component": k + 1})
            table[(fam, flav)] = ops
    reps: Dict[str, List[int]] = {}
    for fam, q in quarks.items():
        reps.setdefault(q["rep"], []).append(fam)
    blocks = sorted(reps.values(), key=len, reverse=True)
    return {
        "b": b, "quarks": quarks, "scalars": scalars, "operators": table,
        # u^c_a (and d^c_a) are identical for all a, so an allowed (row, flavour) allows the whole row
        "all_entries_allowed": all(table[(f, fl)] for f in quarks for fl in ("u", "d")),
        "left_blocks": blocks,
        "shared_scalars": [s for s in scalars.values() if len(s["neutral"]) > 1],
    }


def residual_permutations(blocks: Sequence[Sequence[int]]) -> List[Tuple[int, int, int]]:
    """Index permutations that keep every gauge block in place (families labelled 1..3)."""
    keep = []
    for p in itertools.permutations(range(3)):
        if all({p[f - 1] + 1 for f in blk} == set(blk) for blk in blocks):
            keep.append(p)
    return keep


def versions_331(zu, zd, perms_331: Sequence[Tuple[int, int, int]]) -> List[Tuple[Any, Any]]:
    """The physically distinct 3-3-1 placements of one texture class (index 3 = triplet family)."""
    seen = {}
    for p in itertools.permutations(range(3)):
        pu, pd = _permute_pattern(zu, p), _permute_pattern(zd, p)
        seen.setdefault(pattern_class(pu, pd, perms_331), (pu, pd))
    return [seen[k] for k in sorted(seen)]


# =============================================================================
# 6d. CAN A FLAVOUR SYMMETRY PRODUCE THE SURVIVOR INSIDE 3-3-1?
# =============================================================================
# An abelian flavour symmetry Z_N gives each field a charge mod N. A Yukawa entry
# survives only if the charges of its three fields sum to 0 mod N. Every
# abelian symmetry is a product of such factors, and a product only removes
# more entries, so scanning Z_N covers the abelian case.
def yukawa_slots(y: Dict[str, Any]) -> Dict[Tuple[int, str], Tuple[Any, int]]:
    """For each (family row, flavour): the scalar that gives the mass and the sign of its
    charge in the operator (-1 if the conjugate appears). Exactly one per row in 3-3-1."""
    slots = {}
    for (fam, flav), ops in y["operators"].items():
        if len(ops) != 1:
            raise RuntimeError("expected exactly one mass operator per row and flavour")
        o = ops[0]
        slots[(fam, flav)] = ((o["scalar_X"], o["component"]), -1 if o["conjugate"] else 1)
    return slots


def row_shift_is_common(slots: Dict[Tuple[int, str], Tuple[Any, int]]) -> bool:
    """Is (down-sector scalar charge) - (up-sector scalar charge) the same combination of
    scalar charges for all three rows? If so, a symmetry groups the rows identically in
    both sectors."""
    def vec(fam: int, flav: str) -> Dict[Any, int]:
        key, sgn = slots[(fam, flav)]
        return {key: sgn}
    diffs = []
    for fam in (1, 2, 3):
        d = dict(vec(fam, "d"))
        for k, v in vec(fam, "u").items():
            d[k] = d.get(k, 0) - v
        diffs.append({k: v for k, v in d.items() if v})
    return all(dd == diffs[0] for dd in diffs)


def _structural_rank3(pat) -> bool:
    return any(all((i, p[i]) in pat for i in range(3)) for p in itertools.permutations(range(3)))


def _row_components(pat) -> List[set]:
    rows = [{a for (i, a) in pat if i == r} for r in range(3)]
    comps: List[set] = []
    for r in range(3):
        merged = {r}
        for c in [c for c in comps if any(rows[r] & rows[x] for x in c)]:
            merged |= c
            comps.remove(c)
        comps.append(merged)
    return comps


def _three_family_mixing(pu, pd) -> bool:
    """Can every CKM element be nonzero? Mass eigenstates live inside row components, so
    V_ab can be nonzero only if the up and down components overlap."""
    return all(a & b for a in _row_components(pu) for b in _row_components(pd))


def minimal_scalar_scan(slots, n_max: int) -> List[Dict[str, int]]:
    """Every Z_N (N <= n_max) charge assignment with the minimal scalars (one per row type)."""
    keys = sorted({k for k, _ in slots.values()}, key=str)
    out = []
    for n in range(2, n_max + 1):
        pairs = useful = 0
        for q_rest in itertools.product(range(n), repeat=2):
            q_q = (0,) + q_rest                              # one overall shift is unphysical
            for qs in itertools.product(range(n), repeat=len(keys)):
                q_s = dict(zip(keys, qs))
                pats = {}
                for flav in ("u", "d"):
                    rows = [(q_q[i] + slots[(i + 1, flav)][1] * q_s[slots[(i + 1, flav)][0]]) % n
                            for i in range(3)]
                    found = set()
                    for cols in itertools.product(range(n), repeat=3):
                        pat = frozenset((i, a) for i in range(3) for a in range(3) if (rows[i] + cols[a]) % n == 0)
                        if _structural_rank3(pat):
                            found.add(pat)
                    pats[flav] = found
                for pu in pats["u"]:
                    for pd in pats["d"]:
                        pairs += 1
                        if (len(pu) < 9 or len(pd) < 9) and _three_family_mixing(pu, pd):
                            useful += 1
        out.append({"N": n, "pattern_pairs": pairs, "with_zeros_and_mixing": useful})
    return out


def _nonzero_full(zeros) -> set:
    """Nonzero entries of a general (non-Hermitian) matrix with the same zero positions."""
    z = {(i, j) for a, b in zeros for (i, j) in ((a, b), (b, a))}
    return {(i, j) for i in range(3) for j in range(3)} - z


def _allowed(slots, charges: Dict[str, Any], n: int, flav: str, scalar_charges: Dict[Any, List[int]]) -> set:
    q_q, q_f = charges["Q"], charges[flav]
    out = set()
    for i in range(3):
        key, sgn = slots[(i + 1, flav)]
        for a in range(3):
            if any((q_q[i] + sgn * c + q_f[a]) % n == 0 for c in scalar_charges[key]):
                out.add((i, a))
    return out


def extended_scalar_search(slots, zu, zd, n_max: int) -> Dict[str, Any] | None:
    """Fewest scalar triplets (copies of the two mass-giving scalars, each with its own
    charge) and a Z_N, N <= n_max, whose allowed entries are exactly the nonzero entries."""
    keys = sorted({k for k, _ in slots.values()}, key=str)
    nz = {"u": _nonzero_full(zu), "d": _nonzero_full(zd)}
    best = None
    for n in range(2, n_max + 1):
        for q_rest in itertools.product(range(n), repeat=2):
            q_q = (0,) + q_rest
            for q_u in itertools.product(range(n), repeat=3):
                req = {k: set() for k in keys}
                forb = {k: set() for k in keys}
                for i in range(3):
                    key, sgn = slots[(i + 1, "u")]
                    for a in range(3):
                        (req if (i, a) in nz["u"] else forb)[key].add((-sgn * (q_q[i] + q_u[a])) % n)
                if any(req[k] & forb[k] for k in keys):
                    continue
                for q_d in itertools.product(range(n), repeat=3):
                    r2 = {k: set(v) for k, v in req.items()}
                    f2 = {k: set(v) for k, v in forb.items()}
                    for i in range(3):
                        key, sgn = slots[(i + 1, "d")]
                        for a in range(3):
                            (r2 if (i, a) in nz["d"] else f2)[key].add((-sgn * (q_q[i] + q_d[a])) % n)
                    if any(r2[k] & f2[k] for k in keys):
                        continue
                    count = sum(len(r2[k]) for k in keys)
                    if best is None or count < best["triplets"]:
                        best = {"N": n, "triplets": count, "Q": q_q, "u": q_u, "d": q_d,
                                "scalar_charges": {k: sorted(r2[k]) for k in keys}}
    return best


def rephasing_rank(nz_u: set, nz_d: set) -> int:
    """Rank of the phase redefinitions (Q_i shared, u^c_a, d^c_a) acting on the nonzero entries."""
    rows = []
    for nz, off in ((nz_u, 3), (nz_d, 6)):
        for i, a in sorted(nz):
            r = [Fr(0)] * 9
            r[i] = Fr(1)
            r[off + a] = Fr(1)
            rows.append(r)
    rank = 0
    for c in range(9):
        p = next((r for r in range(rank, len(rows)) if rows[r][c] != 0), None)
        if p is None:
            continue
        rows[rank], rows[p] = rows[p], rows[rank]
        for r in range(len(rows)):
            if r != rank and rows[r][c] != 0:
                f = rows[r][c] / rows[rank][c]
                rows[r] = [x - f * yv for x, yv in zip(rows[r], rows[rank])]
        rank += 1
    return rank


def general_texture_count(zu, zd) -> Dict[str, int]:
    """Parameters of general complex mass matrices with these zeros, against 10 observables
    (6 masses, 3 angles, 1 phase)."""
    nu, nd = _nonzero_full(zu), _nonzero_full(zd)
    n = len(nu) + len(nd)
    phases = n - rephasing_rank(nu, nd)
    return {"nonzero": n, "magnitudes": n, "phases": phases, "parameters": n + phases,
            "predictions": 10 - (n + phases)}


def symmetry_search(yuk: Dict[int, Dict[str, Any]], survivors: Sequence[Tuple[Any, Any]]) -> Dict[str, Any]:
    n_max = int(num("symmetry_max_N"))
    out: Dict[str, Any] = {"by_beta": {}}
    perms = residual_permutations(yuk[-1]["left_blocks"])
    for b, y in yuk.items():
        slots = yukawa_slots(y)
        entry = {"common_shift": row_shift_is_common(slots),
                 "minimal_scan": minimal_scalar_scan(slots, n_max),
                 # Hermiticity would relate Y(Q_i, q^c_a) to Y(Q_a, q^c_i)*; a flavour symmetry
                 # commutes with SU(3)_L and cannot map an (anti)triplet onto a singlet
                 "hermitian_possible": any(q["rep"] == "1" for q in y["quarks"].values()),
                 "survivors": []}
        for zu, zd in survivors:
            for pu, pd in versions_331(zu, zd, perms):
                ext = extended_scalar_search(slots, pu, pd, n_max)
                check = None
                if ext is not None:
                    sc = ext["scalar_charges"]
                    ch = {"Q": ext["Q"], "u": ext["u"], "d": ext["d"]}
                    check = (_allowed(slots, ch, ext["N"], "u", sc) == _nonzero_full(pu)
                             and _allowed(slots, ch, ext["N"], "d", sc) == _nonzero_full(pd))
                entry["survivors"].append({"zeros_u": pu, "zeros_d": pd, "symmetry": ext, "verified": check,
                                           "general_count": general_texture_count(pu, pd)})
        out["by_beta"][b] = entry
    return out


# =============================================================================
# 6e. DOES ANY TEXTURE OF GENERAL MASS MATRICES PREDICT THE CKM MATRIX?
# =============================================================================
# Part E shows that inside 3-3-1 a symmetry can only put zeros into general
# (non-Hermitian) mass matrices. This part asks, for EVERY zero pattern of
# general 3x3 matrices in both sectors, how many independent combinations of its
# parameters reach the 10 observables (6 masses, 3 angles, 1 phase). They are
# measured by 10 weak-basis invariants of H = M M^dag:
#     tr H_u, tr H_u^2, det H_u, the same for H_d, and tr(H_u^a H_d^b), a, b = 1, 2.
# The rank of their Jacobian with respect to the real and imaginary parts of the
# nonzero entries is the number of physical parameters; predictions = 10 - rank.
# Every count below is proved, not sampled:
#   * Lower bound. At integer points the invariants and their derivatives are
#     integers, and the rank is found by elimination modulo a large prime. The rank
#     mod p at one point is at most the rank over the rationals there, which is at
#     most the generic rank. Because 10 is the largest possible rank, rank 10 at any
#     point proves the generic rank is 10.
#   * Upper bound. Unitary weak-basis transformations that keep every zero a zero
#     (rephasings, and rotations of rows or columns with equal supports) leave all
#     10 invariants unchanged, so their tangent vectors lie in the Jacobian's kernel.
#     Rank <= 2 * (nonzero entries) - (their rank at a point, again a lower bound).
#     Where the two bounds meet, the generic rank is certified.
#   * CP. Im det[H_u, H_d] is proportional to J. A nonzero value at an integer point
#     (exact Gaussian integers) proves CP violation is possible; if none is found, the
#     polynomial is expanded symbolically, and an empty expansion proves J = 0.
_PRIME = (1 << 61) - 1


class _Dual:
    """A value and its gradient, integers modulo _PRIME (forward-mode exact derivatives)."""
    __slots__ = ("v", "g")

    def __init__(self, v: int, g: List[int]):
        self.v, self.g = v, g

    def __add__(self, o: "_Dual") -> "_Dual":
        return _Dual((self.v + o.v) % _PRIME, [(a + b) % _PRIME for a, b in zip(self.g, o.g)])

    def __sub__(self, o: "_Dual") -> "_Dual":
        return _Dual((self.v - o.v) % _PRIME, [(a - b) % _PRIME for a, b in zip(self.g, o.g)])

    def __mul__(self, o: "_Dual") -> "_Dual":
        return _Dual(self.v * o.v % _PRIME, [(self.v * b + o.v * a) % _PRIME for a, b in zip(self.g, o.g)])


class _Cx:
    """Complex number over any ring with + - * (here _Dual or int)."""
    __slots__ = ("r", "i")

    def __init__(self, r: Any, i: Any):
        self.r, self.i = r, i

    def __add__(self, o: "_Cx") -> "_Cx":
        return _Cx(self.r + o.r, self.i + o.i)

    def __sub__(self, o: "_Cx") -> "_Cx":
        return _Cx(self.r - o.r, self.i - o.i)

    def __mul__(self, o: "_Cx") -> "_Cx":
        return _Cx(self.r * o.r - self.i * o.i, self.r * o.i + self.i * o.r)

    def conj(self, zero: Any) -> "_Cx":
        return _Cx(self.r, zero - self.i)


def _cmm(a, b):
    out = []
    for i in range(3):
        row = []
        for j in range(3):
            acc = a[i][0] * b[0][j]
            for k in (1, 2):
                acc = acc + a[i][k] * b[k][j]
            row.append(acc)
        out.append(row)
    return out


def _cdag(a, zero):
    return [[a[j][i].conj(zero) for j in range(3)] for i in range(3)]


def _cdet(a):
    def t(p, q, r, s):
        return p * s - q * r
    return (a[0][0] * t(a[1][1], a[1][2], a[2][1], a[2][2]) - a[0][1] * t(a[1][0], a[1][2], a[2][0], a[2][2])
            + a[0][2] * t(a[1][0], a[1][1], a[2][0], a[2][1]))


class _IntStream:
    """Deterministic integers 1..97 (a 64-bit linear congruential generator)."""

    def __init__(self, seed: int):
        self.s = seed

    def __call__(self) -> int:
        self.s = (self.s * 6364136223846793005 + 1442695040888963407) % (1 << 64)
        return 1 + (self.s >> 40) % 97


def invariant_rank(pu, pd, draw: _IntStream) -> int:
    """Exact rank (mod a 61-bit prime) of the Jacobian of the 10 invariants at one integer point."""
    ents = [("u", e) for e in sorted(pu)] + [("d", e) for e in sorted(pd)]
    m = 2 * len(ents)
    zero = _Dual(0, [0] * m)
    mats = {s: [[_Cx(zero, zero) for _ in range(3)] for _ in range(3)] for s in "ud"}
    for k, (s, (i, a)) in enumerate(ents):
        gr, gi = [0] * m, [0] * m
        gr[2 * k], gi[2 * k + 1] = 1, 1
        mats[s][i][a] = _Cx(_Dual(draw(), gr), _Dual(draw(), gi))
    hu = _cmm(mats["u"], _cdag(mats["u"], zero))
    hd = _cmm(mats["d"], _cdag(mats["d"], zero))
    hu2, hd2 = _cmm(hu, hu), _cmm(hd, hd)

    def tr(a):
        return a[0][0].r + a[1][1].r + a[2][2].r
    f = [tr(hu), tr(hu2), _cdet(hu).r, tr(hd), tr(hd2), _cdet(hd).r,
         tr(_cmm(hu, hd)), tr(_cmm(hu2, hd)), tr(_cmm(hu, hd2)), tr(_cmm(hu2, hd2))]
    rows = [list(x.g) for x in f]
    rank = 0
    for c in range(m):
        p = next((r for r in range(rank, len(rows)) if rows[r][c]), None)
        if p is None:
            continue
        rows[rank], rows[p] = rows[p], rows[rank]
        inv = pow(rows[rank][c], _PRIME - 2, _PRIME)
        for r in range(len(rows)):
            if r != rank and rows[r][c]:
                fct = rows[r][c] * inv % _PRIME
                rows[r] = [(x - fct * y) % _PRIME for x, y in zip(rows[r], rows[rank])]
        rank += 1
    return rank


def cp_violation_possible(pu, pd, draw: _IntStream, tries: int) -> bool:
    """Is Im det[H_u, H_d] nonzero at some integer point? Exact Gaussian-integer arithmetic."""
    for _ in range(tries):
        mats = {s: [[_Cx(draw(), draw()) if (i, a) in p else _Cx(0, 0) for a in range(3)] for i in range(3)]
                for s, p in (("u", pu), ("d", pd))}
        hu = _cmm(mats["u"], _cdag(mats["u"], 0))
        hd = _cmm(mats["d"], _cdag(mats["d"], 0))
        a, b = _cmm(hu, hd), _cmm(hd, hu)
        comm = [[a[i][j] - b[i][j] for j in range(3)] for i in range(3)]
        if _cdet(comm).i != 0:
            return True
    return False


class _Poly:
    """Sparse polynomial with integer coefficients: {exponent tuple: coefficient}."""
    __slots__ = ("t",)

    def __init__(self, t: Dict[Tuple[int, ...], int]):
        self.t = t

    def __add__(self, o: "_Poly") -> "_Poly":
        t = dict(self.t)
        for k, c in o.t.items():
            v = t.get(k, 0) + c
            if v:
                t[k] = v
            else:
                t.pop(k, None)
        return _Poly(t)

    def __sub__(self, o: "_Poly") -> "_Poly":
        return self + _Poly({k: -c for k, c in o.t.items()})

    def __mul__(self, o: "_Poly") -> "_Poly":
        t: Dict[Tuple[int, ...], int] = {}
        for k1, c1 in self.t.items():
            for k2, c2 in o.t.items():
                k = tuple(a + b for a, b in zip(k1, k2))
                v = t.get(k, 0) + c1 * c2
                if v:
                    t[k] = v
                else:
                    t.pop(k, None)
        return _Poly(t)


def cp_identically_zero(pu, pd) -> bool:
    """Is Im det[H_u, H_d] the zero polynomial in the real and imaginary parts of the nonzero
    entries? Exact symbolic expansion, so True is a proof that J = 0 everywhere on the pattern."""
    ents = [("u", e) for e in sorted(pu)] + [("d", e) for e in sorted(pd)]
    n = 2 * len(ents)
    zero = _Poly({})

    def var(k: int) -> _Poly:
        return _Poly({tuple(1 if j == k else 0 for j in range(n)): 1})
    mats = {s: [[_Cx(zero, zero) for _ in range(3)] for _ in range(3)] for s in "ud"}
    for k, (s, (i, a)) in enumerate(ents):
        mats[s][i][a] = _Cx(var(2 * k), var(2 * k + 1))
    hu = _cmm(mats["u"], _cdag(mats["u"], zero))
    hd = _cmm(mats["d"], _cdag(mats["d"], zero))
    a, b = _cmm(hu, hd), _cmm(hd, hu)
    comm = [[a[i][j] - b[i][j] for j in range(3)] for i in range(3)]
    return not _cdet(comm).i.t


def _stabilizer_generators(pu, pd) -> List[Tuple[str, str, int, int, int]]:
    """Generators of the unitary weak-basis transformations that keep every zero a zero:
    a common left rotation of rows i, j (support equal in both sectors) and a right rotation
    of columns i, j of one sector (support equal). Each is (side, sector, i, j, kind) with
    kind 0 the phase (i = j), 1 the real and 2 the imaginary off-diagonal generator."""
    def rows(p, r):
        return {a for (i, a) in p if i == r}

    def cols(p, c):
        return {i for (i, a) in p if a == c}
    gens = []
    for i in range(3):
        for j in range(i, 3):
            kinds = (0,) if i == j else (1, 2)
            if i == j or all(rows(p, i) == rows(p, j) for p in (pu, pd)):
                gens += [("L", "ud", i, j, k) for k in kinds]
            for s, p in (("u", pu), ("d", pd)):
                if i == j or cols(p, i) == cols(p, j):
                    gens += [("R", s, i, j, k) for k in kinds]
    return gens


def stabilizer_rank(pu, pd, draw: _IntStream) -> int:
    """Rank (mod _PRIME, at one integer point) of the tangent vectors of those transformations.
    They leave all 10 invariants unchanged, so they lie in the kernel of the Jacobian, and
    2 * (nonzero entries) - this rank is an upper bound on the generic Jacobian rank."""
    ents = [("u", e) for e in sorted(pu)] + [("d", e) for e in sorted(pd)]
    mats = {s: [[_Cx(0, 0) for _ in range(3)] for _ in range(3)] for s in "ud"}
    for s, (i, a) in ents:
        mats[s][i][a] = _Cx(draw(), draw())
    rows = []
    for side, secs, i, j, kind in _stabilizer_generators(pu, pd):
        x = [[_Cx(0, 0) for _ in range(3)] for _ in range(3)]
        if kind == 0:
            x[i][i] = _Cx(0, 1)
        elif kind == 1:
            x[i][j], x[j][i] = _Cx(1, 0), _Cx(-1, 0)
        else:
            x[i][j], x[j][i] = _Cx(0, 1), _Cx(0, 1)
        delta = {s: (_cmm(x, mats[s]) if side == "L" else _cmm(mats[s], x)) for s in secs}
        vec = []
        for s, (r, c) in ents:
            d = delta[s][r][c] if s in delta else _Cx(0, 0)
            vec += [d.r % _PRIME, d.i % _PRIME]
        rows.append(vec)
    rank = 0
    for c in range(2 * len(ents)):
        p = next((r for r in range(rank, len(rows)) if rows[r][c]), None)
        if p is None:
            continue
        rows[rank], rows[p] = rows[p], rows[rank]
        inv = pow(rows[rank][c], _PRIME - 2, _PRIME)
        for r in range(len(rows)):
            if r != rank and rows[r][c]:
                fct = rows[r][c] * inv % _PRIME
                rows[r] = [(x - fct * y) % _PRIME for x, y in zip(rows[r], rows[rank])]
        rank += 1
    return rank


def general_texture_closure() -> Dict[str, Any]:
    entries = [(i, a) for i in range(3) for a in range(3)]
    perms = list(itertools.permutations(range(3)))
    pats = [frozenset(c) for k in range(3, 10) for c in itertools.combinations(entries, k)
            if _structural_rank3(set(c))]
    # canonical form under (common row permutation, separate column permutations)
    col_canon = {}
    for p in pats:
        for r in perms:
            col_canon[(p, r)] = min(tuple(sorted((r[i], c[j]) for i, j in p)) for c in perms)
    classes: Dict[Any, Tuple[Any, Any]] = {}
    for pu in pats:
        for pd in pats:
            key = min((col_canon[(pu, r)], col_canon[(pd, r)]) for r in perms)
            classes.setdefault(key, (pu, pd))
    draw = _IntStream(int(num("closure_seed")))
    tries = int(num("closure_points"))
    counts = {"ordered_pairs": len(pats) ** 2, "classes": len(classes), "no_three_family_mixing": 0,
              "no_phase": 0, "candidates": 0, "rank": {}, "rank_certified": 0, "rank_open": [],
              "cp_impossible": 0, "predictive_with_cp": []}
    for key in sorted(classes):
        pu, pd = (frozenset(x) for x in key)
        if not _three_family_mixing(pu, pd):
            counts["no_three_family_mixing"] += 1
            continue
        if len(pu) + len(pd) - rephasing_rank(set(pu), set(pd)) < 1:
            counts["no_phase"] += 1
            continue
        counts["candidates"] += 1
        # lower bound: the rank found at integer points (mod p it can only be smaller)
        rk = max(invariant_rank(pu, pd, draw) for _ in range(tries))
        # upper bound: 10, and the parameters left after the zero-preserving transformations
        upper = min(10, 2 * (len(pu) + len(pd)) - max(stabilizer_rank(pu, pd, draw) for _ in range(tries)))
        counts["rank"][rk] = counts["rank"].get(rk, 0) + 1
        if rk == upper:
            counts["rank_certified"] += 1
        else:
            counts["rank_open"].append({"zeros_u": key[0], "zeros_d": key[1], "lower": rk, "upper": upper})
        if upper < 10 or rk < 10:
            # a nonzero integer witness proves CP violation; otherwise expand the polynomial
            cp = cp_violation_possible(pu, pd, draw, tries) or not cp_identically_zero(pu, pd)
            if cp:
                counts["predictive_with_cp"].append({"zeros_u": key[0], "zeros_d": key[1], "rank": rk,
                                                     "rank_upper": upper})
            else:
                counts["cp_impossible"] += 1
    return counts


# =============================================================================
# 6f. PART H: WHERE QUANTUM THEORY AND GRAVITY MEET (established physics only)
# =============================================================================
# Everything here follows from G, hbar, c, k_B, measured masses and the Part A age,
# except one thing, labelled where it appears: the coefficient 41/(10 pi) of the
# one-loop quantum correction to Newton's potential, quoted from the published
# calculation (Bjerrum-Bohr, Donoghue, Holstein 2003).
EFT_NEWTON_COEFF_NUM, EFT_NEWTON_COEFF_DEN = 41, 10   # coefficient = 41 / (10 pi)


def _schwarzschild(m: float, c: float, g: float, hbar: float, kb: float) -> Dict[str, float]:
    return {
        "mass_kg": m,
        "r_s_m": 2 * g * m / c ** 2,
        "T_H_K": hbar * c ** 3 / (8 * math.pi * g * m * kb),
        "S_BH_kB": 4 * math.pi * g * m ** 2 / (hbar * c),
        # evaporation into massless quanta, geometric-optics estimate (photons only)
        "t_evap_s": 5120 * math.pi * g ** 2 * m ** 3 / (hbar * c ** 4),
    }


def _lambda_qcd_2loop(alpha_mz: float, mz: float, nf: int) -> float:
    """Lambda_MSbar from the two-loop formula alpha_s = 4 pi/(b0 t) [1 - b1 ln t/(b0^2 t)], t = ln(mu^2/L^2)."""
    b0, b1 = (float(v) for v in qcd_beta(nf))

    def alpha(lam: float) -> float:
        t = math.log(mz ** 2 / lam ** 2)
        return 4 * math.pi / (b0 * t) * (1 - b1 * math.log(t) / (b0 ** 2 * t))
    lo, hi = mz * 10 ** -6, mz / 10
    for _ in range(300):
        mid = math.sqrt(lo * hi)
        if alpha(mid) < alpha_mz:
            lo = mid
        else:
            hi = mid
    return math.sqrt(lo * hi)


def _two_qubit_entropy(amps: List[complex]) -> float:
    """Entanglement entropy (bits) from the reduced density matrix of a two-qubit pure state."""
    a00, a01, a10, a11 = amps
    r00 = abs(a00) ** 2 + abs(a01) ** 2
    r11 = abs(a10) ** 2 + abs(a11) ** 2
    r01 = a00 * a10.conjugate() + a01 * a11.conjugate()
    disc = math.sqrt(max(0, (r00 - r11) ** 2 + 4 * abs(r01) ** 2))
    ent = 0.0
    for lam in ((r00 + r11 + disc) / 2, (r00 + r11 - disc) / 2):
        if lam > 0:
            ent -= lam * math.log2(lam)
    return ent


def planck_units() -> Dict[str, float]:
    """H1. Planck units from G, hbar, c, k_B: calculated once, here, and handed to every stage
    that needs the Planck scale (Parts H, J, L)."""
    x = _float_inputs()
    c, g, kb = x["c"], x["G"], x["k_B"]
    hbar = x["h"] / (2 * math.pi)
    gev = x["e_charge"] * 10 ** 9                     # J per GeV
    lp, mp_planck = math.sqrt(hbar * g / c ** 3), math.sqrt(hbar * c / g)
    return {"l_P_m": lp, "t_P_s": lp / c, "m_P_kg": mp_planck, "E_P_GeV": mp_planck * c ** 2 / gev,
            "T_P_K": mp_planck * c ** 2 / kb, "rho_P_kg_m3": c ** 5 / (hbar * g ** 2)}


def quantum_gravity(cosmo: Dict[str, Any], flav: Dict[str, Any], planck: Dict[str, float]) -> Dict[str, Any]:
    x = _float_inputs()
    c, g, kb, alpha = x["c"], x["G"], x["k_B"], x["alpha_em"]
    hbar = x["h"] / (2 * math.pi)
    gev = x["e_charge"] * 10 ** 9                     # J per GeV
    out: Dict[str, Any] = {}

    # H1. Planck units (their own stage)
    out["planck"] = dict(planck)
    lp, mp_planck = planck["l_P_m"], planck["m_P_kg"]

    # H2. Newton's potential with its one-loop quantum correction
    #     V = -G m1 m2 / r [1 + 3 G (m1 + m2)/(r c^2) + (41/(10 pi)) G hbar/(r^2 c^3)]
    k_q = EFT_NEWTON_COEFF_NUM / (EFT_NEWTON_COEFF_DEN * math.pi)
    m_p = x["m_p"]
    out["newton"] = {
        "coefficient": k_q,
        "quantum_rel_sun_earth": k_q * lp ** 2 / x["au"] ** 2,
        "classical_rel_sun_earth": 3 * (x["GM_sun"] + x["GM_earth"]) / (x["au"] * c ** 2),
        # distance where the quantum term equals the relativistic one: r = k_q hbar / (3 (m1 + m2) c)
        "r_equal_two_protons_m": k_q * hbar / (3 * 2 * m_p * c),
        "proton_compton_m": hbar / (m_p * c),
        # distance where the quantum term reaches 1: the effective theory stops there
        "r_breakdown_m": math.sqrt(k_q) * lp,
    }

    # H3. Black holes and horizons
    m_sun = x["GM_sun"] / g
    t0_s = float(cosmo["age_Gyr"]) * 31557600 * 10 ** 9
    m_evap = (t0_s * hbar * c ** 4 / (5120 * math.pi * g ** 2)) ** (1 / 3)
    h0 = float(cosmo["H0_per_s"])
    h_l = h0 * math.sqrt(float(cosmo["Omega_Lambda"]))
    out["black_holes"] = {"sun": _schwarzschild(m_sun, c, g, hbar, kb),
                          "evaporating_now": _schwarzschild(m_evap, c, g, hbar, kb)}
    out["de_sitter"] = {"H_Lambda_per_s": h_l, "T_dS_K": hbar * h_l / (2 * math.pi * kb),
                        "S_area_law_kB": math.pi * (c / h_l) ** 2 / lp ** 2,
                        "S_part_A_kB": float(cosmo["S_deSitter_kB"])}

    # H4. Unruh effect
    g_earth = x["GM_earth"] / x["R_earth"] ** 2
    out["unruh"] = {"g_earth": g_earth, "T_at_g_K": hbar * g_earth / (2 * math.pi * c * kb),
                    "a_for_1K": 2 * math.pi * c * kb / hbar}

    # H5. The smallest mass gravity can ever entangle maximally. Two equal masses, each in two
    #     places; the branch phases are G m^2 tau/(hbar r). For any geometry the entangling phase
    #     d_phi = phi(d) + phi(d+2dx) - 2 phi(d+dx) is below G m^2 tau/(hbar d) (its limit for
    #     dx >> d). Maximal entanglement (concurrence 1) needs d_phi = pi. The time is at most the
    #     age of the universe (Part A), and a mass cannot be localized more tightly than its
    #     Compton wavelength, d >= hbar/(m c). Together: G m^3 c t0 / hbar^2 >= pi, so
    #     m >= (pi hbar^2 / (G c t0))^(1/3). No design number enters.
    mev = x["e_charge"] * 10 ** 6
    m_min = (math.pi * hbar ** 2 / (g * c * t0_s)) ** (1 / 3)
    d_min = hbar / (m_min * c)
    phase_close = g * m_min ** 2 * t0_s / (hbar * d_min)
    # limiting geometry (dx >> d): only the closest branch pair has a phase
    phases = {(0, 0): 0, (0, 1): 0, (1, 0): phase_close, (1, 1): 0}
    amps = [cmath.exp(1j * phases[k]) / 2 for k in ((0, 0), (0, 1), (1, 0), (1, 1))]
    dphi = phases[(1, 0)] + phases[(0, 1)] - phases[(0, 0)] - phases[(1, 1)]
    conc = abs(math.sin(dphi / 2))
    p = (1 + math.sqrt(max(0, 1 - conc ** 2))) / 2
    ent_formula = -(p * math.log2(p) + (1 - p) * math.log2(1 - p)) if 0 < p < 1 else 0.0
    out["entanglement"] = {"m_min_kg": m_min, "m_min_MeV": m_min * c ** 2 / mev, "d_min_m": d_min,
                           "t0_s": t0_s, "entangling_phase_rad": dphi, "concurrence": conc,
                           "entropy_bits": _two_qubit_entropy(amps), "entropy_formula_bits": ent_formula,
                           "m_min_over_m_p": m_min / x["m_p"]}

    # H6. Why gravity is weak for protons: the strong scale comes from logarithmic running
    runner = flav["runner"]
    mp_gev = mp_planck * c ** 2 / gev
    as_planck = runner.alpha_s(mp_gev)
    lam5 = _lambda_qcd_2loop(x["alpha_s_MZ"], x["M_Z"], 5)
    b0_6 = float(qcd_beta(6)[0])
    out["transmutation"] = {"alpha_s_at_M_P": as_planck, "Lambda5_GeV": lam5,
                            "ln_MP_over_Lambda": math.log(mp_gev / lam5),
                            "one_loop_2pi_over_b0_alpha": 2 * math.pi / (b0_6 * as_planck),
                            "m_p_over_Lambda": m_p * c ** 2 / gev / lam5}

    # H7. Dimensionless numbers (patterns; each labelled)
    rho_crit = 3 * h0 ** 2 / (8 * math.pi * g)
    rho_l = float(cosmo["Omega_Lambda"]) * rho_crit
    alpha_g_p = g * m_p ** 2 / (hbar * c)
    out["numbers"] = {
        "alpha": alpha, "alpha_G_proton": alpha_g_p, "alpha_G_electron": g * x["m_e"] ** 2 / (hbar * c),
        "m_p_over_m_e": m_p / x["m_e"], "m_p_over_M_P": m_p / mp_planck,
        "hubble_radius_over_proton_compton": (c / h0) / (hbar / (m_p * c)),
        "electric_over_gravity_p_e": alpha * hbar * c / (g * m_p * x["m_e"]),
        "rho_Lambda_over_rho_P": rho_l / out["planck"]["rho_P_kg_m3"],
        "S_dS_times_rho_ratio": float(cosmo["S_deSitter_kB"]) * rho_l / out["planck"]["rho_P_kg_m3"],
        # Weinberg (1972): (hbar^2 H0 / (G c))^(1/3) is close to the pion mass
        "weinberg_over_m_pi": (hbar ** 2 * h0 / (g * c)) ** (1 / 3) * c ** 2 / mev / x["m_pi_MeV"],
        "m_min_entangle_over_m_pi": out["entanglement"]["m_min_MeV"] / x["m_pi_MeV"],
    }
    return out


# =============================================================================
# 6g. PART I: CAN ALPHA BE CALCULATED FROM THE OTHER NUMBERS?
# =============================================================================
# No accepted theory derives alpha. One established framework relates it to other
# measured numbers: grand unification. If the three gauge couplings meet at one
# scale, alpha(M_Z) follows from alpha_s(M_Z) and sin^2 theta_W(M_Z) alone. The
# script runs the couplings at one and two loops (coefficients computed from the
# field content and checked against the textbook matrices) and solves for the
# alpha at which all three meet. It does this for the Standard Model and for its
# minimal supersymmetric extension (MSSM). The MSSM's superpartner mass scale M_S
# is unknown, so it is scanned over its whole range, not chosen. alpha is never
# used: the measured value is only a comparison. Threshold corrections at M_S and
# at the unification scale are unknown and are not included.
def _rep_indices(field) -> Tuple[List[Fr], List[Fr]]:
    """S_i(R) times the dimension under the other groups (summed over copies), and C2_i(R)."""
    _, d3, d2, y, _, copies = field
    s = [GUT_NORM * y * y * d3 * d2, dynkin_fund(d2) * d3, dynkin_fund(d3) * d2]
    c = [GUT_NORM * y * y, casimir_fund(2, d2), casimir_fund(3, d3)]
    return [v * copies for v in s], c


def sm_two_loop_b() -> List[List[Fr]]:
    """Gauge two-loop coefficients b_ij (Machacek-Vaughn, gauge part) from the SM content."""
    ca = [Fr(0), su_n_casimirs(2)[0], su_n_casimirs(3)[0]]
    b = [[Fr(0)] * 3 for _ in range(3)]
    for i in range(3):
        b[i][i] -= Fr(34, 3) * ca[i] ** 2
    for f in SM_FIELDS:
        s, c = _rep_indices(f)
        for i in range(3):
            for j in range(3):
                if f[4] == "weyl":
                    b[i][j] += s[i] * (2 * c[j] + (Fr(10, 3) * ca[i] if i == j else 0))
                else:
                    b[i][j] += s[i] * (4 * c[j] + (Fr(2, 3) * ca[i] if i == j else 0))
    return b


MSSM_HIGGS = (("H_u", 1, 2, Fr(1, 2), "chiral", 1), ("H_d", 1, 2, Fr(-1, 2), "chiral", 1))


def mssm_b() -> Tuple[List[Fr], List[List[Fr]]]:
    """One- and two-loop gauge coefficients of a supersymmetric theory from its chiral superfields:
    b_i = -3 C_A + sum S(R);  b_ij = -6 C_A^2 delta_ij + sum S_i(R) [2 C_A delta_ij + 4 C2_j(R)]."""
    ca = [Fr(0), su_n_casimirs(2)[0], su_n_casimirs(3)[0]]
    chiral = [f for f in SM_FIELDS if f[4] == "weyl"] + list(MSSM_HIGGS)
    b1 = [-3 * ca[i] for i in range(3)]
    b2 = [[Fr(0)] * 3 for _ in range(3)]
    for i in range(3):
        b2[i][i] -= 6 * ca[i] ** 2
    for f in chiral:
        s, c = _rep_indices(f)
        for i in range(3):
            b1[i] += s[i]
            for j in range(3):
                b2[i][j] += s[i] * (4 * c[j] + (2 * ca[i] if i == j else 0))
    return b1, b2


def _gauge_rhs(inv: List[float], b1: List[float], b2: List[List[float]], loops: int) -> List[float]:
    """d(1/alpha_i)/d ln mu = -b_i/(2 pi) - sum_j b_ij alpha_j / (8 pi^2)."""
    alphas = [1 / v for v in inv]
    out = []
    for i in range(3):
        d = -b1[i] / (2 * math.pi)
        if loops == 2:
            d -= sum(b2[i][j] * alphas[j] for j in range(3)) / (8 * math.pi ** 2)
        out.append(d)
    return out


def unification_mismatch(inv_alpha_em: float, s2: float, alpha_s: float, mz: float, m_s: float,
                         loops: int, step: float) -> Tuple[float, float, float]:
    """Run 1/alpha_i up; where 1/alpha_1 = 1/alpha_2, return (1/alpha_3 - 1/alpha_1, M_GUT, alpha_GUT)."""
    sm1 = [float(v) for v in sm_gauge_b()]
    sm2 = [[float(v) for v in r] for r in sm_two_loop_b()]
    ms1_f, ms2_f = mssm_b()
    ms1 = [float(v) for v in ms1_f]
    ms2 = [[float(v) for v in r] for r in ms2_f]
    ca = [0, float(su_n_casimirs(2)[0]), float(su_n_casimirs(3)[0])]
    inv = [float(GUT_NORM) * (1 - s2) * inv_alpha_em, s2 * inv_alpha_em, 1 / alpha_s]
    t, t_s = math.log(mz), math.log(m_s)
    switched = m_s <= mz
    if switched:   # MS-bar -> DR-bar at the start
        inv = [inv[i] - ca[i] / (12 * math.pi) for i in range(3)]
    prev = None
    while t < math.log(mz) + 60:
        if not switched and t + step >= t_s:
            h = t_s - t
            if h > 0:
                inv = _rk4(lambda v: _gauge_rhs(v, sm1, sm2, loops), inv, h)
            t = t_s
            inv = [inv[i] - ca[i] / (12 * math.pi) for i in range(3)]
            switched = True
            continue
        b1, b2 = (ms1, ms2) if switched else (sm1, sm2)
        new = _rk4(lambda v: _gauge_rhs(v, b1, b2, loops), inv, step)
        d_old, d_new = inv[0] - inv[1], new[0] - new[1]
        if d_old > 0 >= d_new:
            f = d_old / (d_old - d_new)
            cross = [a + f * (b - a) for a, b in zip(inv, new)]
            return cross[2] - cross[0], math.exp(t + f * step), 1 / cross[0]
        inv, t = new, t + step
        if any(v <= 0 for v in inv):
            break
    return math.nan, math.nan, math.nan


def predict_alpha(s2: float, alpha_s: float, mz: float, m_s: float, loops: int) -> Dict[str, float]:
    """The 1/alpha(M_Z) at which all three couplings meet (secant iteration on the mismatch)."""
    step = num("unif_step")
    lo, hi = num("unif_bracket_lo"), num("unif_bracket_hi")
    f_lo = unification_mismatch(lo, s2, alpha_s, mz, m_s, loops, step)[0]
    f_hi = unification_mismatch(hi, s2, alpha_s, mz, m_s, loops, step)[0]
    if not (f_lo * f_hi < 0):
        return {"inv_alpha": math.nan, "M_GUT": math.nan, "alpha_GUT": math.nan}
    root, side = lo, 0
    for _ in range(int(num("unif_iterations"))):          # Illinois variant of regula falsi
        mid = hi - f_hi * (hi - lo) / (f_hi - f_lo)
        f_mid = unification_mismatch(mid, s2, alpha_s, mz, m_s, loops, step)[0]
        if abs(mid - root) < num("unif_tol"):
            root = mid
            break
        root = mid
        if (f_mid < 0) == (f_lo < 0):
            lo, f_lo = mid, f_mid
            if side == -1:
                f_hi /= 2
            side = -1
        else:
            hi, f_hi = mid, f_mid
            if side == 1:
                f_lo /= 2
            side = 1
    _, m_gut, a_gut = unification_mismatch(root, s2, alpha_s, mz, m_s, loops, step)
    return {"inv_alpha": root, "M_GUT": m_gut, "alpha_GUT": a_gut}


def alpha_from_unification() -> Dict[str, Any]:
    x = _float_inputs()
    s2, s2_sig = x["s2_hat_Z"], sig("s2_hat_Z")
    a_s, a_s_sig, mz = x["alpha_s_MZ"], sig("alpha_s_MZ"), x["M_Z"]
    out: Dict[str, Any] = {"rows": []}
    # scan M_S from M_Z up to the scale where pure-SM couplings, forced to unify, meet (one loop):
    # above it there is no supersymmetric range left and every row is the SM row
    m12 = predict_alpha(s2, a_s, mz, mz * 10 ** 30, 1)["M_GUT"]
    n_pts = int(num("unif_grid_points"))
    grid = [mz * (m12 / mz) ** (k / (n_pts - 1)) for k in range(n_pts)] + [math.inf]
    out["scan_top_GeV"] = m12
    for m_s in grid:
        row: Dict[str, Any] = {"M_S": m_s}
        for loops in (1, 2):
            ms_eff = m_s if math.isfinite(m_s) else mz * 10 ** 30   # beyond M_GUT: pure SM
            c = predict_alpha(s2, a_s, mz, ms_eff, loops)
            if loops == 2:
                var = 0.0
                for name, val, sg in (("s2", s2, s2_sig), ("as", a_s, a_s_sig)):
                    p = predict_alpha(s2 + sg if name == "s2" else s2, a_s + sg if name == "as" else a_s,
                                      mz, ms_eff, loops)["inv_alpha"]
                    var += (p - c["inv_alpha"]) ** 2
                c["sigma_inputs"] = math.sqrt(var)
            row[f"loop{loops}"] = c
        out["rows"].append(row)
    out["measured_inv_alpha_MZ"] = x["alpha_em_inv_MZ"]
    out["measured_sigma"] = sig("alpha_em_inv_MZ")
    # read backwards: the superpartner scale at which the two-loop prediction equals the measurement
    def gap(log_ms: float, s2v: float = s2, asv: float = a_s, target: float = x["alpha_em_inv_MZ"]) -> float:
        return predict_alpha(s2v, asv, mz, math.exp(log_ms), 2)["inv_alpha"] - target
    lo, hi = math.log(mz), math.log(m12)
    if gap(lo) * gap(hi) < 0:
        for _ in range(int(num("unif_iterations"))):
            mid = (lo + hi) / 2
            if (gap(mid) > 0) == (gap(lo) > 0):
                lo = mid
            else:
                hi = mid
        l_ms = (lo + hi) / 2
        h = num("unif_ms_deriv_step")
        slope = (gap(l_ms + h) - gap(l_ms - h)) / (2 * h)            # d(1/alpha)/d ln M_S
        d_s2 = (gap(l_ms, s2v=s2 + s2_sig) - gap(l_ms)) / slope
        d_as = (gap(l_ms, asv=a_s + a_s_sig) - gap(l_ms)) / slope
        sig_ln = math.hypot(d_s2, d_as)
        at_ms = predict_alpha(s2, a_s, mz, math.exp(l_ms), 2)
        out["M_S_for_measured_alpha"] = {"M_S_GeV": math.exp(l_ms), "ln_sigma": sig_ln,
                                         "M_GUT_GeV": at_ms["M_GUT"], "alpha_GUT": at_ms["alpha_GUT"],
                                         "low_GeV": math.exp(l_ms - sig_ln), "high_GeV": math.exp(l_ms + sig_ln),
                                         "slope_per_efold": slope}
    return out


def predict_alpha_one_loop_exact(s2: float, alpha_s: float, mz: float, m_s: float, sm_only: bool = False) -> float:
    """One loop in closed form: X_i = 1/alpha_i(M_Z) - b_i^SM l_s/2pi - C_A,i/12pi - b_i^MSSM L/2pi
    equal for i = 1, 2, 3, linear in (1/alpha, L). Used to check the numerical solution."""
    sm1 = [float(v) for v in sm_gauge_b()]
    ms1 = sm1 if sm_only else [float(v) for v in mssm_b()[0]]
    ca = [0, 0, 0] if sm_only else [0, float(su_n_casimirs(2)[0]), float(su_n_casimirs(3)[0])]
    ls = 0 if sm_only else math.log(m_s / mz)
    k = [float(GUT_NORM) * (1 - s2), s2, 0]                  # coefficient of 1/alpha in 1/alpha_i
    const = [(1 / alpha_s if i == 2 else 0) - sm1[i] * ls / (2 * math.pi) - ca[i] / (12 * math.pi)
             for i in range(3)]
    lcoef = [-ms1[i] / (2 * math.pi) for i in range(3)]
    # (k1 - k3) A + (l1 - l3) L = c3 - c1 ;  (k2 - k3) A + (l2 - l3) L = c3 - c2
    a11, a12, r1 = k[0] - k[2], lcoef[0] - lcoef[2], const[2] - const[0]
    a21, a22, r2 = k[1] - k[2], lcoef[1] - lcoef[2], const[2] - const[1]
    return (r1 * a22 - r2 * a12) / (a11 * a22 - a12 * a21)


def alpha_numerology() -> List[Dict[str, Any]]:
    """Closed formulas proposed for 1/alpha(0), tested against CODATA. None is a derivation."""
    a_inv = 1 / inp("alpha_em")
    a_sig = sig("alpha_em") / inp("alpha_em") ** 2
    pi = math.pi
    cands = [
        ("Eddington 1929: 136", 136),
        ("Eddington 1931: 137", 137),
        ("4 pi^3 + pi^2 + pi", 4 * pi ** 3 + pi ** 2 + pi),
        ("Wyler 1969: (8 pi^4 / 9) (2^4 5! / pi^5)^(1/4)",
         8 * pi ** 4 / 9 * (2 ** 4 * math.factorial(5) / pi ** 5) ** (1 / 4)),
    ]
    return [{"formula": n, "value": v, "n_sigma": abs(v - a_inv) / a_sig} for n, v in cands]


# =============================================================================
# 6h. PART J: CAN THE YUKAWA COUPLINGS BE CALCULATED FROM THE OTHER NUMBERS?
# =============================================================================
# No accepted theory gives the Yukawa couplings. Two established ideas relate them:
#   * grand unification puts quarks and leptons in one multiplet, which fixes
#     quark/lepton mass ratios at the unification scale by group theory
#     (minimal SU(5): m_b = m_tau, m_s = m_mu, m_d = m_e; Georgi-Jarlskog with a
#     45-dimensional Higgs: m_s = m_mu/3, m_d = 3 m_e);
#   * a large top coupling at high scales is driven by running to an infrared
#     quasi-fixed point, set by the gauge couplings (Pendleton-Ross, Hill).
# Unknowns (the unification scale, the MSSM's tan(beta) and its superpartner
# scale) are scanned or taken from Part I; nothing is fitted.
PERTURBATIVE_LIMIT = math.sqrt(4 * math.pi)   # a coupling above sqrt(4 pi) is not perturbative


def lepton_masses_gev() -> Dict[str, float]:
    x = _float_inputs()
    me = x["m_e"] * x["c"] ** 2 / (x["e_charge"] * 10 ** 9)
    return {"e": me, "mu": x["m_mu_MeV"] / 1000, "tau": x["m_tau_MeV"] / 1000}


def lepton_running_mass(pole: float, mu: float, alpha: float) -> float:
    """One-loop QED: m(m) = M / (1 + alpha/pi), then d ln m / d ln mu = -3 alpha/(2 pi) (charge 1)."""
    m_m = pole / (1 + alpha / math.pi)
    return m_m * (mu / m_m) ** (-3 * alpha / (2 * math.pi))


def _pair_gauge_coeffs(left, right) -> Tuple[float, float, float]:
    """16 pi^2 d ln y/d ln mu contains -c_i g_i^2 with c_i = 3 [C2_i(left) + C2_i(right)] (SM)."""
    return (float(3 * GUT_NORM * (left[3] ** 2 + right[3] ** 2)),
            float(3 * (casimir_fund(2, left[2]) + casimir_fund(2, right[2]))),
            float(3 * (casimir_fund(3, left[1]) + casimir_fund(3, right[1]))))


def _susy_gauge_coeffs(fields) -> Tuple[float, float, float]:
    """MSSM: 16 pi^2 d ln y/d ln mu contains -2 sum over the three fields of C2_i g_i^2."""
    return (float(2 * sum(GUT_NORM * f[3] ** 2 for f in fields)),
            float(2 * sum(casimir_fund(2, f[2]) for f in fields)),
            float(2 * sum(casimir_fund(3, f[1]) for f in fields)))


def _fields() -> Dict[str, Any]:
    named = {f[0]: f for f in SM_FIELDS}
    named.update({f[0]: f for f in MSSM_HIGGS})
    return named


def yukawa_rhs(model: str):
    """Right-hand side for (g1, g2, g3, y_t, y_b, y_tau) in d/d ln mu, one loop."""
    f = _fields()
    k = 16 * math.pi ** 2
    nc = float(su_n_casimirs(3)[0])
    if model == "SM":
        gb = [float(v) for v in sm_gauge_b()]
        ct = _pair_gauge_coeffs(f["Q"], f["u^c"])
        cb = _pair_gauge_coeffs(f["Q"], f["d^c"])
        cl = _pair_gauge_coeffs(f["L"], f["e^c"])
        split = float(YUKAWA_SPLIT)

        def rhs(v: List[float], nf: int) -> List[float]:
            g1, g2, g3, yt, yb, yl = v
            y2 = nc * yt ** 2 + nc * yb ** 2 + yl ** 2
            gs = (g1 ** 2, g2 ** 2, g3 ** 2)
            return [gb[0] * g1 ** 3 / k, gb[1] * g2 ** 3 / k, gb[2] * g3 ** 3 / k,
                    yt * (split * (yt ** 2 - yb ** 2) + y2 - sum(c * g for c, g in zip(ct, gs))) / k,
                    yb * (split * (yb ** 2 - yt ** 2) + y2 - sum(c * g for c, g in zip(cb, gs))) / k,
                    yl * (split * yl ** 2 + y2 - sum(c * g for c, g in zip(cl, gs))) / k]
        return rhs
    gb = [float(v) for v in mssm_b()[0]]
    ct = _susy_gauge_coeffs((f["H_u"], f["Q"], f["u^c"]))
    cb = _susy_gauge_coeffs((f["H_d"], f["Q"], f["d^c"]))
    cl = _susy_gauge_coeffs((f["H_d"], f["L"], f["e^c"]))
    # anomalous dimensions: a superpotential term with N invariant terms gives each field
    # (N / its number of components) x y^2
    dims = {"H_u": 2, "H_d": 2, "Q": 6, "u^c": 3, "d^c": 3, "L": 2, "e^c": 1}
    terms = {"t": ("H_u", "Q", "u^c", 6), "b": ("H_d", "Q", "d^c", 6), "l": ("H_d", "L", "e^c", 2)}

    def rhs(v: List[float], nf: int) -> List[float]:
        g1, g2, g3, yt, yb, yl = v
        y = {"t": yt, "b": yb, "l": yl}
        gam = {name: 0.0 for name in dims}
        for key, (a, b, c, n) in terms.items():
            for fld in (a, b, c):
                gam[fld] += n / dims[fld] * y[key] ** 2
        gs = (g1 ** 2, g2 ** 2, g3 ** 2)
        out = [gb[0] * g1 ** 3 / k, gb[1] * g2 ** 3 / k, gb[2] * g3 ** 3 / k]
        for key, cc in (("t", ct), ("b", cb), ("l", cl)):
            a, b, c, _ = terms[key]
            out.append(y[key] * (gam[a] + gam[b] + gam[c] - sum(ci * g for ci, g in zip(cc, gs))) / k)
        return out
    return rhs


def couplings_at_mt(flav: Dict[str, Any]) -> Tuple[float, List[float]]:
    """(m_t(m_t), [g1, g2, g3, y_t, y_b, y_tau]) at mu = m_t(m_t), from the flavour stage's running."""
    mt, _, _, st = sm_state_at_mt(runner=flav["runner"])
    return mt, st


def run_to(state: List[float], mu0: float, mu1: float, model: str) -> List[float]:
    return integrate_ln_mu(state, mu0, mu1, yukawa_rhs(model), [], int(num("rg_steps_per_efold")))


def unification_point(state: List[float], mu0: float, model: str,
                       mu_stop: float | None = None) -> Tuple[float, List[float]]:
    """Run up until g1 = g2 (or until mu_stop, if given); NaN scale if a coupling leaves
    perturbation theory first."""
    rhs = yukawa_rhs(model)
    h = num("unif_step")
    t, v = math.log(mu0), list(state)
    while t < math.log(mu0) + 60:
        if mu_stop is not None and t + h >= math.log(mu_stop):
            new = _rk4(lambda s: rhs(s, 6), v, math.log(mu_stop) - t)
            if any(abs(c) > PERTURBATIVE_LIMIT for c in new):
                return math.nan, new
            return mu_stop, new
        new = _rk4(lambda s: rhs(s, 6), v, h)
        if mu_stop is None and v[0] < v[1] and new[0] >= new[1]:
            f = (v[1] - v[0]) / ((v[1] - v[0]) - (new[1] - new[0]))
            return math.exp(t + f * h), [a + f * (b - a) for a, b in zip(v, new)]
        if any(abs(c) > PERTURBATIVE_LIMIT for c in new):
            return math.nan, new
        v, t = new, t + h
    return math.nan, v


def yukawa_relations(flav: Dict[str, Any], m_s_susy: float | None, m_gut: float | None,
                     m_planck_gev: float) -> Dict[str, Any]:
    """m_s_susy and m_gut come from Part I (two-loop unification at the measured alpha)."""
    x = _float_inputs()
    out: Dict[str, Any] = {}
    mt, st = couplings_at_mt(flav)
    lep = lepton_masses_gev()
    a0 = inp("alpha_em")
    # J1. ratios (same-type ratios do not run with QCD; gauge and Yukawa terms cancel within a type)
    r_q = 1 / flav["ratios"][mt]["r_ds"]                                    # m_s/m_d
    r_l = lepton_running_mass(lep["mu"], mt, a0) / lepton_running_mass(lep["e"], mt, a0)
    sig_q = r_q * math.hypot(sig("m_s") / inp("m_s"), sig("m_d") / inp("m_d"))
    out["ratios"] = {"ms_over_md": r_q, "ms_over_md_sigma": sig_q, "mmu_over_me_at_mt": r_l,
                     "SU5": {"predicted": r_l, "n_sigma": abs(r_l - r_q) / sig_q},
                     "GJ": {"predicted": r_l / 9, "n_sigma": abs(r_l / 9 - r_q) / sig_q}}
    # J2. b-tau unification
    # the SM has no unification point: report where g1 = g2 and at M_Planck
    mu12, s12 = unification_point(st, mt, "SM")
    s_pl = run_to(st, mt, m_planck_gev, "SM")
    out["btau_SM"] = [{"mu": mu12, "where": "SM g1 = g2", "yb_over_ytau": s12[4] / s12[5]},
                      {"mu": m_planck_gev, "where": "M_Planck", "yb_over_ytau": s_pl[4] / s_pl[5]}]
    mssm = []
    if m_s_susy:
        s_ms = run_to(st, mt, m_s_susy, "SM")
        # tan(beta) range: y_t/sin(beta) and y_b/cos(beta) at M_S must stay below sqrt(4 pi)
        sb_min = s_ms[3] / PERTURBATIVE_LIMIT
        cb_min = s_ms[4] / PERTURBATIVE_LIMIT
        tb_lo = sb_min / math.sqrt(1 - sb_min ** 2)
        tb_hi = math.sqrt(1 - cb_min ** 2) / cb_min
        n_tb = int(num("yukawa_tan_beta_points"))
        out["tan_beta_range"] = (tb_lo, tb_hi)
        for k in range(n_tb):
            tb = tb_lo * (tb_hi / tb_lo) ** (k / (n_tb - 1))
            sb, cb = tb / math.sqrt(1 + tb * tb), 1 / math.sqrt(1 + tb * tb)
            s0 = [s_ms[0], s_ms[1], s_ms[2], s_ms[3] / sb, s_ms[4] / cb, s_ms[5] / cb]
            mg, sg = unification_point(s0, m_s_susy, "MSSM", m_gut)
            mssm.append({"tan_beta": tb, "M_GUT": mg,
                         "yb_over_ytau": sg[4] / sg[5] if math.isfinite(mg) else math.nan,
                         "yt_GUT": sg[3], "yb_GUT": sg[4]})
    out["btau_MSSM"] = mssm
    out["M_S"] = m_s_susy
    out["M_GUT"] = m_gut
    if m_s_susy:
        # where does y_b/y_tau reach 1 at low tan(beta)? (bisection between the last
        # non-perturbative point and the first perturbative one)
        def ratio_at(tb: float) -> Tuple[float, float]:
            sb, cb = tb / math.sqrt(1 + tb * tb), 1 / math.sqrt(1 + tb * tb)
            s0 = [s_ms[0], s_ms[1], s_ms[2], s_ms[3] / sb, s_ms[4] / cb, s_ms[5] / cb]
            mg, sg = unification_point(s0, m_s_susy, "MSSM", m_gut)
            return (sg[4] / sg[5] if math.isfinite(mg) else math.inf), sg[3]
        ok = [r for r in mssm if math.isfinite(r["M_GUT"])]
        first_ok = min((q["tan_beta"] for q in ok), default=math.inf)
        bad = [r for r in mssm if not math.isfinite(r["M_GUT"]) and r["tan_beta"] < first_ok]
        if ok and bad:
            lo, hi = max(r["tan_beta"] for r in bad), min(r["tan_beta"] for r in ok)
            if ratio_at(hi)[0] < 1:
                for _ in range(int(num("unif_iterations"))):
                    mid = (lo + hi) / 2
                    if ratio_at(mid)[0] >= 1:
                        lo = mid
                    else:
                        hi = mid
                r1, yt1 = ratio_at(hi)
                out["btau_MSSM_unity"] = {"tan_beta": (lo + hi) / 2, "yt_GUT": yt1, "ratio": r1,
                                          "tan_beta_nonperturbative_below": lo}
    # J3. top quasi-fixed point: start large at the unification scale, run down
    # a "large" top coupling: half the perturbative limit and the limit itself
    starts = (PERTURBATIVE_LIMIT / 2, PERTURBATIVE_LIMIT)
    fp = []
    mu_top = m_planck_gev
    s_up = run_to(st, mt, mu_top, "SM")
    for y0 in starts:
        s = list(s_up)
        s[3] = float(y0)
        down = run_to(s, mu_top, mt, "SM")
        fp.append({"yt_start": float(y0), "yt_mt": down[3], "mt_msbar": down[3] * flav["runner"].v / math.sqrt(2)})
    out["fixed_point_SM"] = {"scale": mu_top, "runs": fp, "measured_yt_mt": st[3], "measured_mt_msbar": mt}
    # MSSM quasi-fixed point: large y_t at M_GUT, MSSM running to M_S, y_t(SM) = y_t(MSSM) sin(beta),
    # SM running to m_t; solve for the sin(beta) that gives the measured top coupling
    if m_s_susy:
        s_ms = run_to(st, mt, m_s_susy, "SM")
        mg, s_g = unification_point([s_ms[0], s_ms[1], s_ms[2], s_ms[3], 0, 0], m_s_susy, "MSSM", m_gut)
        rows = []
        for y0 in starts:
            down = run_to([s_g[0], s_g[1], s_g[2], float(y0), 0, 0], mg, m_s_susy, "MSSM")

            def yt_mt(sb: float) -> float:
                return run_to([down[0], down[1], down[2], down[3] * sb, 0, 0], m_s_susy, mt, "SM")[3]
            lo, hi = 0, 1
            for _ in range(int(num("unif_iterations"))):
                mid = (lo + hi) / 2
                if yt_mt(mid) < st[3]:
                    lo = mid
                else:
                    hi = mid
            sb = (lo + hi) / 2
            rows.append({"yt_start": float(y0), "yt_MSSM_at_MS": down[3], "sin_beta": sb,
                         "tan_beta": sb / math.sqrt(1 - sb * sb)})
        out["fixed_point_MSSM"] = {"M_GUT": mg, "runs": rows}
    return out


# =============================================================================
# 6b. PART K: THE HIGGS MASS IN THE MSSM, FROM THE SCALES OF PARTS I AND J
# =============================================================================
# Effective theory: the MSSM above M_S, the SM below. Convention V = (lambda/2) (H^dag H)^2,
# so m_h^2 = lambda v^2 at tree level.
def sm_higgs_rhs():
    """(g1, g2, g3, y_t, y_b, y_tau, lambda) in d/d ln mu, one loop (lambda adds nothing to
    the others at one loop). 16 pi^2 beta_lambda = 12 lambda^2 - 3 lambda (3 g^2 + g'^2)
    + 12 lambda y_t^2 - 12 y_t^4 + (3/4) [2 g^4 + (g^2 + g'^2)^2]."""
    base = yukawa_rhs("SM")
    gn = float(GUT_NORM)
    k = 16 * math.pi ** 2

    def rhs(v: List[float], nf: int) -> List[float]:
        out = base(v[:6], nf)
        g1, g2, _, yt, _, _, lam = v
        gp2, g22 = gn * g1 ** 2, g2 ** 2
        out.append((12 * lam ** 2 - 3 * lam * (3 * g22 + gp2) + 12 * lam * yt ** 2 - 12 * yt ** 4
                    + 3 * (2 * g22 ** 2 + (g22 + gp2) ** 2) / 4) / k)
        return out
    return rhs


def stop_threshold(xt: float) -> float:
    """One-loop stop threshold to lambda at M_S, in units of 3 y_t^4/(8 pi^2):
    X^2 (1 - X^2/12), X = X_t/M_S. Its maximum over every mixing is 3, at X^2 = 6."""
    return xt ** 2 * (1 - xt ** 2 / 12)


def mssm_lambda_at_ms(state_ms: List[float], tan_beta: float, xt: float) -> float:
    """Matching at M_S: lambda = (g^2 + g'^2)/4 cos^2(2 beta) + stop threshold."""
    g1, g2, _, yt = state_ms[:4]
    c2b = (1 - tan_beta ** 2) / (1 + tan_beta ** 2)
    tree = (g2 ** 2 + float(GUT_NORM) * g1 ** 2) / 4 * c2b ** 2
    return tree + 3 * yt ** 4 / (8 * math.pi ** 2) * stop_threshold(xt)


def mssm_higgs_mass(flav: Dict[str, Any], m_s: float, tan_beta: float, xt: float,
                    steps: int | None = None) -> float:
    mt, st = couplings_at_mt(flav)
    steps = steps or int(num("rg_steps_per_efold"))
    s_ms = integrate_ln_mu(st, mt, m_s, yukawa_rhs("SM"), [], steps)
    lam_ms = mssm_lambda_at_ms(s_ms, tan_beta, xt)
    down = integrate_ln_mu(s_ms + [lam_ms], m_s, mt, sm_higgs_rhs(), [], steps)
    return math.sqrt(down[6]) * flav["runner"].v if down[6] > 0 else math.nan


def ms_for_higgs_mass(flav: Dict[str, Any], tan_beta: float, target: float) -> float:
    """Read backwards: the M_S at which the largest MSSM Higgs mass (maximal mixing) equals target."""
    mt = flav["runner"].mt_msbar
    x6 = math.sqrt(6)
    lo, hi = math.log(mt), math.log(mt) + int(num("higgs_ms_search_efolds"))
    if (mssm_higgs_mass(flav, math.exp(hi), tan_beta, x6) - target) < 0:
        return math.nan
    for _ in range(int(num("higgs_iterations"))):
        mid = (lo + hi) / 2
        if mssm_higgs_mass(flav, math.exp(mid), tan_beta, x6) < target:
            lo = mid
        else:
            hi = mid
    return math.exp((lo + hi) / 2)


def higgs_mass_mssm(flav: Dict[str, Any], alpha_unif: Dict[str, Any], yuk: Dict[str, Any]) -> Dict[str, Any]:
    """M_S (with its range) from Part I, tan(beta) from Part J's two determinations; the stop
    mixing X_t is unknown and scanned over all values: the threshold is largest at X_t^2 = 6 M_S^2,
    so that value gives an upper bound on m_h that holds for every mixing."""
    ms = alpha_unif.get("M_S_for_measured_alpha")
    if not ms or not yuk.get("btau_MSSM_unity") or not yuk.get("fixed_point_MSSM"):
        return {}
    tbs = [yuk["btau_MSSM_unity"]["tan_beta"]] + [r["tan_beta"] for r in yuk["fixed_point_MSSM"]["runs"]]
    x6 = math.sqrt(6)
    rows = []
    for label, m_s in (("low", ms["low_GeV"]), ("central", ms["M_S_GeV"]), ("high", ms["high_GeV"])):
        for tb in (min(tbs), max(tbs)):
            rows.append({"M_S_label": label, "M_S": m_s, "tan_beta": tb,
                         "mh_no_mixing": mssm_higgs_mass(flav, m_s, tb, 0),
                         "mh_max_mixing": mssm_higgs_mass(flav, m_s, tb, x6)})
    # dependence on X_t at the central point (the bound is the maximum of this curve)
    n_x = int(num("higgs_xt_points"))
    xt_max = math.sqrt(12)                    # beyond this the threshold is negative
    curve = [(xt_max * i / (n_x - 1), mssm_higgs_mass(flav, ms["M_S_GeV"], max(tbs), xt_max * i / (n_x - 1)))
             for i in range(n_x)]
    bound = max(r["mh_max_mixing"] for r in rows)
    return {"tan_betas": tbs, "rows": rows, "xt_curve": curve, "mh_upper_bound": bound,
            "M_S": ms["M_S_GeV"], "M_S_range": (ms["low_GeV"], ms["high_GeV"])}


# =============================================================================
# 6c. PART L: STANDARD MODEL CRITICALITY AT THE PLANCK SCALE (two-loop running)
# =============================================================================
# Convention of Buttazzo et al. 2013 (arXiv:1307.3536): V = lambda (|H|^2 - v^2/2)^2,
# m_h^2 = 2 lambda v^2 at tree level. Quoted two-loop coefficients (their appendix B,
# top Yukawa only at two loops; y_b and y_tau enter at one loop), in GUT normalization
# and d/d ln(mu^2), so each term below is (4 pi)^-4 x [coefficient]:
GAUGE_2L_YT = (Fr(17, 10), Fr(3, 2), Fr(2))             # -d_i y_t^2 in g_i^3 [...]
# top Yukawa: y_t [y_t^2 (c0 y_t^2 + c1 lambda + c2 g3^2 + c3 g2^2 + c4 g1^2) + c5 lambda^2
#                  + c6 g3^4 + c7 g2^4 + c8 g1^4 + c9 g3^2 g2^2 + c10 g3^2 g1^2 + c11 g2^2 g1^2]
YT_2L = (Fr(-12), Fr(-12), Fr(36), Fr(225, 16), Fr(393, 80), Fr(6), Fr(-108), Fr(-23, 4),
         Fr(1187, 600), Fr(9), Fr(19, 15), Fr(-9, 20))
# Higgs quartic, as (coefficient, powers of lambda, y_t^2, g3^2, g2^2, g1^2)
LAMBDA_2L = ((Fr(-156), 3, 0, 0, 0, 0), (Fr(-72), 2, 1, 0, 0, 0), (Fr(54), 2, 0, 0, 1, 0),
             (Fr(54, 5), 2, 0, 0, 0, 1), (Fr(-3, 2), 1, 2, 0, 0, 0), (Fr(40), 1, 1, 1, 0, 0),
             (Fr(45, 4), 1, 1, 0, 1, 0), (Fr(17, 4), 1, 1, 0, 0, 1), (Fr(-73, 16), 1, 0, 0, 2, 0),
             (Fr(1887, 400), 1, 0, 0, 0, 2), (Fr(117, 40), 1, 0, 0, 1, 1), (Fr(15), 0, 3, 0, 0, 0),
             (Fr(-16), 0, 2, 1, 0, 0), (Fr(-4, 5), 0, 2, 0, 0, 1), (Fr(-9, 8), 0, 1, 0, 2, 0),
             (Fr(-171, 200), 0, 1, 0, 0, 2), (Fr(63, 20), 0, 1, 0, 1, 1), (Fr(305, 32), 0, 0, 0, 3, 0),
             (Fr(-3411, 4000), 0, 0, 0, 0, 3), (Fr(-289, 160), 0, 0, 0, 2, 1), (Fr(-1677, 800), 0, 0, 0, 1, 2))


def sm_rge(loops: int):
    """(g1, g2, g3, y_t, y_b, y_tau, lambda) in d/d ln mu. One loop from the field content
    (Part J's Yukawa equations; lambda in this Part's convention), two loops from the
    quoted coefficients above plus the gauge b_ij from the field content, three loops (and
    the four-loop pure QCD term of g3) from LITERATURE["sm_beta_3loop"]."""
    base = yukawa_rhs("SM")
    gn = float(GUT_NORM)
    k = 16 * math.pi ** 2
    b2 = [[float(c) for c in row] for row in sm_two_loop_b()]
    dt = [float(c) for c in GAUGE_2L_YT]
    c = [float(v) for v in YT_2L]
    l2 = [(float(a), p) for a, *p in LAMBDA_2L]
    b3 = {key: [(lit_num(a), p) for a, *p in terms[1]] for key, terms in LITERATURE["sm_beta_3loop"]["value"].items()}
    g3_4 = lit_num(LITERATURE["g3_beta_4loop"]["value"])

    def rhs(v: List[float], nf: int) -> List[float]:
        g1, g2, g3, yt, _, _, lam = v
        out = base(v[:6], nf)
        a1, a2, a3, y2 = g1 ** 2, g2 ** 2, g3 ** 2, yt ** 2
        gp2 = gn * a1
        dl = (24 * lam ** 2 - 3 * lam * (3 * a2 + gp2) + 12 * lam * y2 - 6 * y2 ** 2
              + 3 * (2 * a2 ** 2 + (a2 + gp2) ** 2) / 8) / k
        if loops >= 2:
            for i, g in enumerate((g1, g2, g3)):
                out[i] += g ** 3 * (sum(b2[i][j] * a for j, a in enumerate((a1, a2, a3))) - dt[i] * y2) / k ** 2
            out[3] += yt * (y2 * (c[0] * y2 + c[1] * lam + c[2] * a3 + c[3] * a2 + c[4] * a1) + c[5] * lam ** 2
                            + c[6] * a3 ** 2 + c[7] * a2 ** 2 + c[8] * a1 ** 2 + c[9] * a3 * a2
                            + c[10] * a3 * a1 + c[11] * a2 * a1) / k ** 2
            # the quoted lambda coefficients are for d/d ln(mu^2): times 2 for d/d ln mu
            dl += 2 * sum(a * lam ** p[0] * y2 ** p[1] * a3 ** p[2] * a2 ** p[3] * a1 ** p[4]
                          for a, p in l2) / k ** 2
        if loops >= 3:
            pw = [[1.0, x, x * x, x ** 3, x ** 4] for x in (lam, y2, a3, a2, a1)]
            pl_, py_, p3_, p2_, p1_ = pw

            def bracket(key: str) -> float:
                return sum(a * pl_[p[0]] * py_[p[1]] * p3_[p[2]] * p2_[p[3]] * p1_[p[4]] for a, p in b3[key])
            # d g/d ln mu = (1/g) d g^2/d ln(mu^2), and the prefactor is g^4: g^3 [...]
            out[0] += g1 ** 3 * bracket("g1") / k ** 3
            out[1] += g2 ** 3 * bracket("g2") / k ** 3
            out[2] += g3 ** 3 * (bracket("g3") / k ** 3 + g3_4 * a3 ** 3 / k ** 4)
            out[3] += yt * bracket("yt") / k ** 3
            dl += 2 * bracket("lam") / k ** 3
        out.append(dl)
        return out
    return rhs


def sm_state_at_mt(overrides: Dict[str, float] | None = None, runner: "FlavourRunner | None" = None,
                   qcd_loops: int = 4) -> Tuple[float, float, float, List[float]]:
    """(m_t(m_t), v, M_t/m_t(m_t), [g1, g2, g3, y_t, y_b, y_tau]) at m_t(m_t), from the inputs
    (with optional changes, for propagating their errors). The one derivation of these
    couplings: pass a runner to reuse running that is already done."""
    if runner is None:
        runner = FlavourRunner(_float_inputs(overrides), int(num("rg_steps_per_efold")), qcd_loops)
    x = runner.x
    mt = runner.mt_msbar
    base = runner.ratios_at([mt])[mt]
    a_em, s2 = 1 / x["alpha_em_inv_MZ"], x["s2_hat_Z"]
    sm1 = [float(b) for b in sm_gauge_b()]
    k = 16 * math.pi ** 2
    lt = math.log(mt / x["M_Z"])
    g1 = math.sqrt(1 / (float(GUT_NORM) / (4 * math.pi * a_em / (1 - s2)) - 2 * sm1[0] / k * lt))
    g2 = math.sqrt(1 / (s2 / (4 * math.pi * a_em) - 2 * sm1[1] / k * lt))
    g3 = math.sqrt(4 * math.pi * base["alpha_s"])
    m_tau = lepton_running_mass(lepton_masses_gev()["tau"], mt, inp("alpha_em"))
    rt2 = math.sqrt(2)
    return mt, runner.v, x["M_t"] / mt, [g1, g2, g3, rt2 * mt / runner.v, rt2 * base["m_b"] / runner.v,
                                         rt2 * m_tau / runner.v]


def run_sm(state: List[float], mu0: float, mu1: float, loops: int, steps: int | None = None) -> List[float]:
    return integrate_ln_mu(state, mu0, mu1, sm_rge(loops), [], steps or int(num("rg_steps_per_efold")))


def _bracketed_root(f: Callable[[float], float], a: float, b: float, tol: float, iters: int) -> float:
    """Root of f in [a, b] with f(a), f(b) of opposite sign (Illinois false position)."""
    fa, fb = f(a), f(b)
    side = 0
    for _ in range(iters):
        c = b - fb * (b - a) / (fb - fa)
        fc = f(c)
        if abs(c - b) < tol * abs(c) or fc == 0:
            return c
        if (fc > 0) == (fb > 0):
            b, fb = c, fc
            if side == -1:
                fa /= 2
            side = -1
        else:
            a, fa = c, fc
            if side == 1:
                fb /= 2
            side = 1
    return c


def _lambda_at(state: List[float], lam0: float, mu0: float, mu1: float, loops: int,
               steps: int | None = None) -> float:
    """lambda(mu1); +inf if it runs into a Landau pole on the way."""
    try:
        out = run_sm(state + [lam0], mu0, mu1, loops, steps)[6]
    except OverflowError:
        return math.inf
    return out if math.isfinite(out) else math.inf


def critical_lambda(state: List[float], mt: float, mu: float, loops: int, steps: int | None = None,
                    guess: float | None = None) -> float:
    """The lambda(m_t) for which lambda(mu) = 0. Bracket: lambda = 0 (it runs negative) and the
    smallest of y_t^2 / 2^n, n = 1, 2, ..., above which lambda(mu) is positive; or, from a guess,
    guess (1 -+ crit_yt_step 2^n) until the sign changes."""
    steps = steps or int(num("crit_steps_per_efold"))

    def f(lam0: float) -> float:
        return _lambda_at(state, lam0, mt, mu, loops, steps)
    if guess:
        d = num("crit_yt_step")
        lo, hi = guess * (1 - d), guess * (1 + d)
        flo, fhi = f(lo), f(hi)
        while flo > 0 or fhi < 0:
            d *= 2
            if flo > 0:
                lo = guess * max(1 - d, 0)
                flo = f(lo)
            if fhi < 0:
                hi = guess * (1 + d)
                fhi = f(hi)
        return _bracketed_root(f, lo, hi, num("crit_tol"), int(num("crit_iterations")))
    lo, hi = 0, state[3] ** 2
    while f(hi / 2) > 0:
        hi /= 2
    def capped(lam0: float) -> float:
        return min(f(lam0), 1)                 # a Landau pole counts as "positive", finitely
    return _bracketed_root(capped, lo, hi, num("crit_tol"), int(num("crit_iterations")))


# --- one-loop matching of lambda and y_t to the pole masses (Buttazzo et al. 2013, appendix A,
# eqs. (89), (90), (93); M_b = M_tau = 0). Self-check: their mu dependence is the one-loop RGE.
def pv_a0(m2: float, mu2: float) -> float:
    """Finite part of A0: M^2 (1 - ln(M^2/mu^2))."""
    return 0 if m2 == 0 else m2 * (1 - math.log(m2 / mu2))


def _int_ln_abs(r: float) -> float:
    """int_0^1 ln|x - r| dx."""
    def f(t: float) -> float:
        return 0 if t == 0 else t * math.log(abs(t))
    return f(1 - r) + f(r) - 1


def pv_b0(p2: float, m12: float, m22: float, mu2: float) -> float:
    """Real part of the finite B0(p; M1, M2) = -int_0^1 ln[(x M1^2 + (1-x) M2^2 - x(1-x) p^2)/mu^2] dx,
    in closed form: the argument is the quadratic p^2 x^2 + (M1^2 - M2^2 - p^2) x + M2^2."""
    a, b, c = p2, m12 - m22 - p2, m22
    if a == 0:
        val = math.log(abs(c)) if b == 0 else math.log(abs(b)) + _int_ln_abs(-c / b)
    else:
        d = b * b - 4 * a * c
        if d >= 0:
            sq = math.sqrt(d)
            val = math.log(abs(a)) + _int_ln_abs((-b + sq) / (2 * a)) + _int_ln_abs((-b - sq) / (2 * a))
        else:
            u, w = -b / (2 * a), math.sqrt(-d) / (2 * a)

            def F(x: float) -> float:
                return (x - u) * math.log((x - u) ** 2 + w * w) - 2 * (x - u) + 2 * w * math.atan((x - u) / w)
            val = math.log(abs(a)) + F(1) - F(0)
    return math.log(mu2) - val


def lambda_one_loop(mh: float, mt: float, mw: float, mz: float, v: float, mu: float) -> float:
    """lambda^(1)(mu): lambda(mu) = M_h^2/(2 V^2) + this, V = (sqrt2 G_F)^(-1/2)."""
    h, t, w, z, m = mh * mh, mt * mt, mw * mw, mz * mz, mu * mu

    def A(x: float) -> float:
        return pv_a0(x, m)

    def B(p: float, x: float, y: float) -> float:
        return pv_b0(p, x, y, m)
    s = (3 * t * (h - 4 * t) * B(h, t, t) + 3 * h * A(t)
         + (h * h - 4 * h * z + 12 * z * z) / 4 * B(h, z, z) + h * (7 * w - 4 * z) / (2 * (z - w)) * A(z)
         + (h * h - 4 * h * w + 12 * w * w) / 2 * B(h, w, w) - 3 * h * w / (2 * (h - w)) * A(h)
         + h / 2 * (-11 + 3 * h / (h - w) - 3 * w / (z - w)) * A(w)
         + 9 * h * h / 4 * B(h, h, h) + (h * h + h * (z + 2 * w - 6 * t) - 8 * (z * z + 2 * w * w)) / 4)
    return s / (16 * math.pi ** 2 * v ** 4)


def yt_ew_one_loop(mh: float, mt: float, mw: float, mz: float, v: float, mu: float) -> float:
    """Electroweak part of y_t^(1)(mu) (eq. 93 without its g3^2 term; QCD is in the m_t conversion)."""
    h, t, w, z, m = mh * mh, mt * mt, mw * mw, mz * mz, mu * mu

    def A(x: float) -> float:
        return pv_a0(x, m)

    def B(p: float, x: float, y: float) -> float:
        return pv_b0(p, x, y, m)
    s = (-(h - 4 * t) * B(t, h, t)
         + (t * (80 * w * z - 64 * w * w - 7 * z * z) + 40 * w * z * z - 32 * w * w * z - 17 * z ** 3)
         / (9 * t * z) * B(t, t, z)
         + (t * w + t * t - 2 * w * w) / t * B(t, 0, w)
         + (3 * h / (h - w) + 2 * w / t + 3 * w / (w - z) - 10) * A(w) + (3 * w / (w - h) + 1) * A(h)
         + (36 * t * z - 56 * w * z + 64 * w * w - 17 * z * z) / (9 * t * z) * A(t)
         + (3 * w / (z - w) + (32 * w * w - 40 * w * z + 17 * z * z) / (9 * t * z) - 3) * A(z)
         + h / 2 - 3 * t - 9 * w + 7 * z / 18 + 64 * w * w / (9 * z))
    return mt / (math.sqrt(2) * v ** 3 * 16 * math.pi ** 2) * s


def higgs_mass_from_lambda(lam: float, mt: float, mw: float, mz: float, v: float, mu: float,
                           matched: bool, extra: Callable[[float], float] | None = None) -> float:
    """Invert lambda(mu) = M_h^2/(2V^2) [+ lambda^(1) [+ extra(M_h), the two-loop part]] for M_h."""
    tree = math.sqrt(2 * lam) * v
    if not matched:
        return tree

    def f(mh: float) -> float:
        return (mh * mh / (2 * v * v) + lambda_one_loop(mh, mt, mw, mz, v, mu)
                + (extra(mh) if extra else 0) - lam)
    lo, hi = tree, tree
    step = num("crit_yt_step")
    while f(lo) > 0:
        lo *= 1 - step
    while f(hi) < 0:
        hi *= 1 + step
    return _bracketed_root(f, lo, hi, num("crit_tol"), int(num("crit_iterations")))


def matched_couplings(overrides: Dict[str, float] | None, mh: float, matched: bool, qcd_loops: int = 4):
    """State at m_t(m_t) with y_t matched to the pole mass (QCD conversion of the script plus the
    one-loop electroweak part, which depends on M_h), and the mass inputs for the lambda matching."""
    mt, v, pole_ratio, st = sm_state_at_mt(overrides, qcd_loops=qcd_loops)
    x = _float_inputs(overrides)
    masses = (x["M_t"], x["M_W"], x["M_Z"])
    if matched:
        st = list(st)
        st[3] += yt_ew_one_loop(mh, masses[0], masses[1], masses[2], v, mt)
    return mt, v, pole_ratio, st, masses


def predict_higgs_mass(overrides: Dict[str, float] | None, mu: float, loops: int, matched: bool,
                       steps: int | None = None, mh_start: float | None = None) -> Dict[str, float]:
    """M_h from lambda(mu) = 0. With matching, y_t depends on M_h: iterate to the fixed point
    (from the tree-level answer, or from mh_start)."""
    mh = mh_start or 0
    lam = 0.0
    if not mh:
        mt, v, _, st, ms_ = matched_couplings(overrides, 0, False)
        lam = critical_lambda(st, mt, mu, loops, steps)
        mh = math.sqrt(2 * lam) * v
        if not matched:                  # tree level: that is the answer
            return {"m_h": mh, "lambda_mt": lam, "yt_mt": st[3]}
    for _ in range(int(num("crit_iterations")) if matched else 1):
        mt, v, _, st, ms_ = matched_couplings(overrides, mh, matched)
        # warm start from the last root (or the tree-level lambda of this M_h)
        lam = critical_lambda(st, mt, mu, loops, steps, guess=lam or mh * mh / (2 * v * v))
        new = higgs_mass_from_lambda(lam, ms_[0], ms_[1], ms_[2], v, mt, matched)
        done = abs(new - mh) < num("crit_tol") * mh
        mh = new
        if done:
            break
    return {"m_h": mh, "lambda_mt": lam, "yt_mt": st[3]}


def _fit_2loop(name: str, part: str, mh: float, mt: float) -> float:
    val = LITERATURE[name]["value"]
    c0, ch, ct = (lit_num(a) for a in val[part])
    return c0 + ch * (mh - lit_num(val["M_h0"])) + ct * (mt - lit_num(val["M_t0"]))


def lambda_two_loop(mh: float, mt_pole: float, g3: float) -> float:
    """lambda^(2)(mu = M_t): QCD and electroweak two-loop thresholds (LITERATURE)."""
    k2 = (16 * math.pi ** 2) ** 2
    return (g3 ** 2 * _fit_2loop("lambda_2loop_matching", "qcd", mh, mt_pole)
            + _fit_2loop("lambda_2loop_matching", "ew", mh, mt_pole)) / k2


def yt_two_loop(mh: float, mt_pole: float, g3: float) -> float:
    """The electroweak and mixed two-loop parts of y_t(mu = M_t) (LITERATURE)."""
    k2 = (16 * math.pi ** 2) ** 2
    return (_fit_2loop("yt_2loop_matching", "ew", mh, mt_pole)
            + g3 ** 2 * _fit_2loop("yt_2loop_matching", "qcd_ew", mh, mt_pole)) / k2


def lambda_three_loop_qcd(g3: float, v: float, mt_pole: float) -> float:
    """lambda^(3)(mu = M_t), its leading QCD part (LITERATURE); G_mu = 1/(sqrt2 V^2)."""
    e = LITERATURE["lambda_3loop_qcd"]["value"]
    g_mu = 1 / (math.sqrt(2) * v * v)
    bracket = sum(lit_num(c) * qcd_constant(t) for c, t in e["terms"])
    return lit_num(e["norm"]) * g3 ** 4 * g_mu ** 2 * mt_pole ** 4 / (16 * math.pi ** 2) ** 3 * bracket


def nnlo_state(overrides: Dict[str, float] | None, mh: float, loops: int, qcd_loops: int = 4):
    """(M_t, v, pole masses, [g1, g2, g3, y_t, y_b, y_tau] at mu = M_t) with two-loop matching:
    y_t from the QCD conversion (qcd_loops loops, in the flavour running) and the one-loop
    electroweak part at m_t(m_t) (Part L), run to mu = M_t, plus the two-loop electroweak and
    mixed parts."""
    mt, v, _, st, masses = matched_couplings(overrides, mh, True, qcd_loops)
    big_mt = masses[0]
    s_ = run_sm(list(st) + [mh * mh / (2 * v * v)], mt, big_mt, loops)[:6]
    s_[3] += yt_two_loop(mh, big_mt, s_[2])
    return big_mt, v, masses, s_


def lambda_nnlo(mh: float, masses: Tuple[float, float, float], v: float, g3: float, matching: int = 3) -> float:
    """lambda(mu = M_t) for a Higgs pole mass: tree + one loop + two loops (+ the leading QCD
    part of three loops)."""
    big_mt = masses[0]
    return (mh * mh / (2 * v * v) + lambda_one_loop(mh, big_mt, masses[1], masses[2], v, big_mt)
            + lambda_two_loop(mh, big_mt, g3) + (lambda_three_loop_qcd(g3, v, big_mt) if matching >= 3 else 0))


def smdr_offsets() -> Dict[str, float]:
    """SMDR's couplings at its reference point minus this script's (three-loop matching, four-loop
    QCD) at the same inputs: the electroweak and mixed higher-order thresholds this script lacks,
    plus its simpler electroweak inputs. Indices into the state: g1, g2, g3, y_t; and lambda."""
    c = LITERATURE["smdr_reference"]["value"]
    ins = {k: lit_num(v) for k, v in c["inputs"].items()}
    mh = ins.pop("M_h")
    big_mt, v, masses, st = nnlo_state(ins, mh, 3)
    q0 = lit_num(c["Q0"])
    st = run_sm(st + [lambda_nnlo(mh, masses, v, st[2], 3)], big_mt, q0, 3)
    ref = {k: lit_num(x) for k, x in c["couplings"].items()}
    return {"g1": ref["gp"] / math.sqrt(float(GUT_NORM)) - st[0], "g2": ref["g2"] - st[1],
            "g3": ref["g3"] - st[2], "y_t": ref["y_t"] - st[3], "lambda": ref["lambda"] - st[6],
            "ours": {"lambda": st[6], "y_t": st[3], "g3": st[2], "g2": st[1],
                     "gp": st[0] * math.sqrt(float(GUT_NORM))}, "smdr": ref}


def anchored_state(overrides: Dict[str, float] | None, mh: float, anchor: Dict[str, float] | None,
                   loops: int = 3):
    """(M_t, v, [g1, g2, g3, y_t, y_b, y_tau, lambda] at mu = M_t) for a Higgs pole mass, at Part L's
    central order: three-loop matching, four-loop QCD, shifted by SMDR's offsets if anchor."""
    big_mt, v, masses, s_ = nnlo_state(overrides, mh, loops)
    lam = lambda_nnlo(mh, masses, v, s_[2], 3)
    if anchor:
        s_ = [s_[0] + anchor["g1"], s_[1] + anchor["g2"], s_[2] + anchor["g3"], s_[3] + anchor["y_t"]] + s_[4:]
        lam += anchor["lambda"]
    return big_mt, v, list(s_) + [lam]


def predict_higgs_mass_nnlo(overrides: Dict[str, float] | None, mu: float, loops: int, mh_start: float,
                            matching: int = 3, qcd_loops: int = 4, steps: int | None = None,
                            anchor: Dict[str, float] | None = None) -> Dict[str, float]:
    """M_h from lambda(mu) = 0 with two- or three-loop matching at mu = M_t (iterated: y_t and
    the thresholds depend on M_h). With anchor (smdr_offsets()), the couplings at M_t are shifted
    by SMDR's offsets: its matching, carried to these inputs by this script's."""
    steps = steps or int(num("crit_steps_per_efold"))
    mh, lam, s_ = mh_start, 0.0, []
    for _ in range(int(num("crit_iterations"))):
        big_mt, v, masses, s_ = nnlo_state(overrides, mh, loops, qcd_loops)
        if anchor:
            s_ = [s_[0] + anchor["g1"], s_[1] + anchor["g2"], s_[2] + anchor["g3"], s_[3] + anchor["y_t"]] + s_[4:]
        lam = critical_lambda(s_, big_mt, mu, loops, steps, guess=lam or mh * mh / (2 * v * v))
        l3 = lambda_three_loop_qcd(s_[2], v, big_mt) if matching >= 3 else 0
        if anchor:
            l3 += anchor["lambda"]
        new = higgs_mass_from_lambda(lam, masses[0], masses[1], masses[2], v, big_mt, True,
                                     extra=lambda m: lambda_two_loop(m, big_mt, s_[2]) + l3)
        done = abs(new - mh) < num("crit_tol") * mh
        mh = new
        if done:
            break
    return {"m_h": mh, "lambda_Mt": lam, "yt_Mt": s_[3]}


def sm_criticality(planck_gev: float) -> Dict[str, Any]:
    """lambda(M_P) = 0 (Froggatt-Nielsen 1996; Shaposhnikov-Wetterich 2010): one condition at the
    Planck scale fixes m_h from the measured top mass and alpha_s. Both Planck masses (G only)."""
    out: Dict[str, Any] = {}
    m_red = planck_gev / math.sqrt(8 * math.pi)
    out["planck"] = {"M_P": planck_gev, "M_P_reduced": m_red}
    rows = []
    c_steps = int(num("crit_steps_per_efold"))
    for name, mu in (("M_P", planck_gev), ("M_P reduced", m_red)):
        for loops in (1, 2, 3):
            r = predict_higgs_mass(None, mu, loops, False, steps=c_steps if loops == 3 else None)
            rows.append({"scale": name, "mu": mu, "loops": loops, "matching": "tree", "matched": False, **r})
    out["tree_matching"] = [r for r in rows if r["scale"] == "M_P" and r["loops"] == 2][0]
    start = out["tree_matching"]["m_h"]
    for loops in (2, 3):              # one-loop matching at mu = m_t(m_t)
        rows.append({"scale": "M_P", "mu": planck_gev, "loops": loops, "matching": "one loop", "matched": True,
                     **predict_higgs_mass(None, planck_gev, loops, True, mh_start=start,
                                          steps=c_steps if loops == 3 else None)})
    for loops, matching, qcd, label in ((2, 2, 4, "two loops"), (3, 2, 3, "two loops, QCD 3"), (3, 2, 4, "two loops"),
                                        (2, 3, 4, "three loops"), (3, 3, 3, "three loops, QCD 3"),
                                        (3, 3, 4, "three loops")):
        r = predict_higgs_mass_nnlo(None, planck_gev, loops, start, matching, qcd)
        rows.append({"scale": "M_P", "mu": planck_gev, "loops": loops, "matching": label, "matched": True,
                     "lambda_mt": r["lambda_Mt"], **r})
    out["rows"] = rows

    def row(loops: int, matching: str) -> Dict[str, Any]:
        return [r for r in rows if r["scale"] == "M_P" and r["loops"] == loops and r["matching"] == matching][0]
    out["row"] = {f"{lp}L/{m}": row(lp, m) for lp, m in ((1, "tree"), (2, "tree"), (3, "tree"), (2, "one loop"),
                                                          (3, "one loop"), (2, "two loops"), (3, "two loops"),
                                                          (3, "two loops, QCD 3"), (2, "three loops"),
                                                          (3, "three loops, QCD 3"), (3, "three loops"))}
    out["two_loop_one_loop"] = row(2, "one loop")         # two-loop running, one-loop matching
    anchor = smdr_offsets()
    out["smdr"] = anchor
    r = predict_higgs_mass_nnlo(None, planck_gev, 3, row(3, "three loops")["m_h"], 3, 4, anchor=anchor)
    rows.append({"scale": "M_P", "mu": planck_gev, "loops": 3, "matching": "SMDR-anchored", "matched": True,
                 "lambda_mt": r["lambda_Mt"], **r})
    out["row"]["3L/SMDR-anchored"] = rows[-1]
    central = rows[-1]
    # input errors: M_t and alpha_s dominate; M_W enters only through the matching
    var = {}
    for name in ("M_t", "alpha_s_MZ", "M_W"):
        var[name] = predict_higgs_mass_nnlo({name: inp(name) + sig(name)}, planck_gev, 3,
                                            central["m_h"], 3, anchor=anchor)["m_h"] - central["m_h"]
    out["sigma_inputs"] = var
    out["sigma_total"] = math.sqrt(sum(d ** 2 for d in var.values()))
    out["central"] = central
    # both conditions at once, lambda(M_P) = 0 and beta_lambda(M_P) = 0: solve for lambda(m_t) and y_t(m_t)
    # (at two-loop running and one-loop matching)
    central = out["two_loop_one_loop"]
    mt, v, pole_ratio, st, masses = matched_couplings(None, central["m_h"], True)
    rhs2 = sm_rge(2)

    def beta_at_crit(yt0: float) -> Tuple[float, float]:
        s = list(st)
        s[3] = yt0
        lam = critical_lambda(s, mt, planck_gev, 2, guess=central["lambda_mt"])
        top = run_sm(s + [lam], mt, planck_gev, 2, int(num("crit_steps_per_efold")))
        return rhs2(top, 6)[6], lam
    # bracket in y_t: step from the measured value towards smaller |beta_lambda| until it changes sign
    step = num("crit_yt_step")
    y0, b0 = st[3], beta_at_crit(st[3])[0]
    y1, b1 = y0 * (1 + step), beta_at_crit(y0 * (1 + step))[0]
    sgn = 1 if abs(b1) < abs(b0) else -1
    while (b1 > 0) == (b0 > 0):
        y0, b0 = y1, b1
        step *= 2
        y1 = st[3] * (1 + sgn * step)
        b1 = beta_at_crit(y1)[0]
    yt_c = _bracketed_root(lambda y: beta_at_crit(y)[0], y0, y1, num("crit_tol"), int(num("crit_iterations")))
    lam_c = beta_at_crit(yt_c)[1]
    # translate (y_t, lambda) at m_t(m_t) back to pole masses: y_t = sqrt2 M_t/(r v) + y_t^EW(M_h, M_t),
    # r = M_t/m_t(m_t) of the measured top (QCD), and lambda = M_h^2/(2 v^2) + lambda^(1)(M_h, M_t)
    mh_c, mtp_c = central["m_h"], masses[0]
    for _ in range(int(num("crit_iterations"))):
        def g(mtp: float) -> float:
            return math.sqrt(2) * mtp / (pole_ratio * v) + yt_ew_one_loop(mh_c, mtp, masses[1], masses[2], v, mt) - yt_c
        lo, hi = mtp_c * (1 - step), mtp_c * (1 + step)
        mtp_new = _bracketed_root(g, lo, hi, num("crit_tol"), int(num("crit_iterations")))
        mh_new = higgs_mass_from_lambda(lam_c, mtp_new, masses[1], masses[2], v, mt, True)
        done = abs(mh_new - mh_c) < num("crit_tol") * mh_c and abs(mtp_new - mtp_c) < num("crit_tol") * mtp_c
        mh_c, mtp_c = mh_new, mtp_new
        if done:
            break
    out["double"] = {"yt_mt": yt_c, "lambda_mt": lam_c, "m_h": mh_c, "M_t": mtp_c}
    out["buttazzo"] = buttazzo_checks()
    out["qcd_checks"] = qcd_checks()
    out["state_mt"] = (mt, v, masses)
    return out


def sm_lambda_profile(crit: Dict[str, Any], m_h: float) -> Dict[str, Any]:
    """lambda(mu) at three loops for a given Higgs pole mass (Part L's central matching at M_t): its value
    at M_P and where it turns negative. Called by the report with the measured m_h."""
    big_mt, v, full = anchored_state(None, m_h, crit.get("smdr"))
    st, lam0 = full[:6], full[6]
    mp = crit["planck"]["M_P"]
    c_steps = int(num("crit_steps_per_efold"))
    top = run_sm(st + [lam0], big_mt, mp, 3, c_steps)
    lo, hi = math.log(big_mt), math.log(mp)
    if top[6] >= 0:
        return {"lambda_MP": top[6], "beta_MP": sm_rge(3)(top, 6)[6], "mu_zero": math.nan}
    for _ in range(int(num("crit_iterations"))):
        mid = (lo + hi) / 2
        if run_sm(st + [lam0], big_mt, math.exp(mid), 3, c_steps)[6] > 0:
            lo = mid
        else:
            hi = mid
    return {"lambda_MP": top[6], "beta_MP": sm_rge(3)(top, 6)[6], "mu_zero": math.exp((lo + hi) / 2)}


def qcd_checks() -> Dict[str, float]:
    """The quoted four-loop QCD coefficients against published numbers (LITERATURE["check_rundec"])."""
    c = LITERATURE["check_rundec"]["value"]
    steps = int(num("rg_steps_per_efold"))

    def run5(loops: int, mu: float) -> float:          # five flavours, exact integration
        beta = qcd_beta_pi(5, loops)
        return integrate_ln_mu([lit_num(c["alpha_MZ"])], lit_num(c["M_Z"]), mu,
                               lambda v, nf: [-2 * math.pi * sum(b * (v[0] / math.pi) ** (i + 2)
                                                                  for i, b in enumerate(beta))], [], steps)[0]
    out = {"alpha_Mb_4L": run5(4, lit_num(c["M_b"])), "alpha_1GeV_3L": run5(3, 1), "alpha_1GeV_4L": run5(4, 1)}
    out["dev_alpha_Mb"] = abs(out["alpha_Mb_4L"] / lit_num(c["alpha_Mb_4L"]) - 1)
    out["dev_alpha_1GeV"] = max(abs(out["alpha_1GeV_3L"] - lit_num(c["alpha_1GeV_3L"])),
                                abs(out["alpha_1GeV_4L"] - lit_num(c["alpha_1GeV_4L"])))
    dev_g = 0.0                                          # coefficient of each power of n_f
    for key in ("gamma2", "gamma3"):
        e = LITERATURE["qcd_gamma_3_4loop"]["value"][key]
        for k, want in enumerate(c[key]):
            got = lit_num(e["norm"]) * sum(lit_num(a) * qcd_constant(z) for a, p, z in e["terms"] if p == k)
            dev_g = max(dev_g, abs(got / lit_num(want) - 1))
    out["dev_gamma"] = dev_g
    out["dev_B4"] = abs(qcd_constant("B4") - lit_num(c["B4"]))
    al_f = lit_num(c["alpha_Mb_4L"])
    out["dev_roundtrip"] = abs(alpha_up(al_f * decoupling_g2(al_f, 4, 4), 4, 4) / al_f - 1)
    return out


def buttazzo_checks() -> Dict[str, float]:
    """Reproduce Buttazzo et al. 2013 with the quoted coefficients: (1) their couplings at M_t run
    to M_Pl at three loops (and at two, which must miss); (2) lambda(M_t) and y_t(M_t) from their
    inputs through this script's matching."""
    c = LITERATURE["check_buttazzo"]["value"]
    at, pl = {k: lit_num(v) for k, v in c["at_Mt"].items()}, {k: lit_num(v) for k, v in c["at_MPl"].items()}
    inputs = {k: lit_num(v) for k, v in c["inputs"].items()}
    g1 = at["gY"] / math.sqrt(float(GUT_NORM))
    st = [g1, at["g2"], at["g3"], at["y_t"], 0.0, 0.0, at["lambda"]]
    out: Dict[str, float] = {}
    for loops in (2, 3):
        top = run_sm(st, inputs["M_t"], lit_num(c["M_Pl"]), loops, int(num("crit_steps_per_efold")))
        out[f"dev_{loops}L"] = max(abs(top[i] - pl[k]) for i, k in ((0, "g1"), (1, "g2"), (2, "g3"),
                                                                     (3, "y_t"), (6, "lambda")))
    mh = inputs.pop("M_h")
    # at the paper's own order: two-loop matching, QCD (running, top mass) at three loops
    big_mt, v, masses, s_ = nnlo_state(inputs, mh, 3, qcd_loops=3)
    out["lambda_Mt"], out["yt_Mt"] = lambda_nnlo(mh, masses, v, s_[2], 2), s_[3]
    out["dev_lambda"], out["dev_yt"] = abs(out["lambda_Mt"] - at["lambda"]), abs(out["yt_Mt"] - at["y_t"])
    out["lambda_th"], out["yt_th"] = lit_num(c["lambda_th"]), lit_num(c["yt_th"])
    # their linear lambda(M_Pl) = 0, solved for M_h at this script's M_t and alpha_s
    lm = {k: lit_num(v) for k, v in c["lambda_MPl"].items()}
    lam_pl = (lm["l0"] + lm["lt"] * (inp("M_t") - lit_num(c["inputs"]["M_t"]))
              + lm["la"] * (inp("alpha_s_MZ") - lit_num(c["inputs"]["alpha_s_MZ"])) / lm["alpha_step"])
    out["mh_linear"] = mh - lam_pl / lm["lh"]
    out["mh_linear_tol"] = out["lambda_th"] / lit_num(c["dlambda_Mt_dMh"])     # their theory error, in GeV
    return out


# =============================================================================
# 6i. PART M: WHICH HIGH-ENERGY HYPOTHESIS SURVIVES EVERY CONDITION AT ONCE?
# =============================================================================
# The field content above the electroweak scale is not fixed by the inputs, so it
# is not chosen: every hypothesis is run against every combination of the
# conditions the other parts impose, and the data decide. Conditions:
#   U  gauge unification         predicts 1/alpha(M_Z)        (measured input)
#   B  b-tau unification         predicts y_b/y_tau = 1 at M_GUT (SM: where g1 = g2)
#   H  Higgs mass                SM: lambda(M_P) = 0 (Part L); MSSM: matching at M_S
# The MSSM has three unknowns (M_S, tan beta, the stop mixing X_t). They are scanned
# and the smallest chi^2 is found only to decide survival, as in Part C: the point
# is never reported or used. X_t enters only the stop threshold, and m_h rises with
# it, so for X_t in [0, sqrt12] m_h covers exactly [m_h(X_t = 0), m_h(X_t^2 = 6 M_S^2)].
# Every MSSM point must keep its Yukawa couplings perturbative up to M_GUT, the scale where
# the three gauge couplings meet for that M_S; b-tau unification is tested there (as in Part J).
# Errors, two ways, so each verdict is bracketed:
#   inputs           the measured inputs' errors only: the strongest exclusion
#   inputs + theory  plus, for every ingredient, the change from the last order the script
#                    calculates to the order below it (running: 2 loops vs 1; low-scale
#                    matching: one loop vs tree). The next order is usually much smaller
#                    than the last step, so this is the weakest exclusion.
# Not estimated: the two-loop stop threshold (the code has only the one-loop one, which is
# the leading effect, not a correction), GUT and superpartner thresholds of unification.
JOINT_CONDITIONS = ("U", "B", "H")


def mh_from_ms(state_ms: List[float], m_s: float, lam_k: float, x: Dict[str, float], v: float, mt: float,
               loops: int, matched: bool) -> float:
    """m_h from lambda (Part K convention, lambda_K = 2 lambda_L) at M_S: run down at one loop
    (Part K) or two (Part L), convert at m_t at tree level or with Part L's one-loop matching."""
    steps = int(num("rg_steps_per_efold"))
    if loops == 1:
        lam_l = integrate_ln_mu(state_ms + [lam_k], m_s, mt, sm_higgs_rhs(), [], steps)[6] / 2
    else:
        lam_l = run_sm(state_ms + [lam_k / 2], m_s, mt, 2)[6]
    if lam_l <= 0:
        return 0.0
    return higgs_mass_from_lambda(lam_l, x["M_t"], x["M_W"], x["M_Z"], v, mt, matched)


def _joint_verdict(chi2: float, n_cond: int, n_par: int) -> Dict[str, Any]:
    dof = n_cond - n_par
    if dof >= 1:
        p = chi2_pvalue(chi2, dof)
        n_sig = pvalue_to_sigma(p) if p > 0 else math.sqrt(chi2)     # beyond float range: asymptotic
    else:                            # no prediction: how far the data lie outside what it can reach
        n_sig = math.sqrt(max(chi2, 0.0))
    return {"chi2": chi2, "dof": dof, "n_sigma": n_sig, "survives": n_sig <= num("survival_sigma"),
            "predicts": dof >= 1}


def uv_joint_test(flav: Dict[str, Any], alpha_unif: Dict[str, Any], yuk: Dict[str, Any],
                  crit: Dict[str, Any]) -> Dict[str, Any]:
    x = _float_inputs()
    mh_meas, mh_err, _ = _comparison("m_h")
    a_meas, a_err = x["alpha_em_inv_MZ"], sig("alpha_em_inv_MZ")
    s2, a_s, mz = x["s2_hat_Z"], x["alpha_s_MZ"], x["M_Z"]
    runner = flav["runner"]
    mt, v = runner.mt_msbar, runner.v
    _, _, _, st = sm_state_at_mt(runner=runner)
    steps = int(num("rg_steps_per_efold"))
    # relative error of y_b(m_t), from the flavour stage's input variations (b-tau errors, linear)
    mb = flav["ratios"][mt]["m_b"]
    def mb_of(ratios: Dict[float, Dict[str, float]]) -> float:     # m_b(m_t) at that run's own m_t
        return next(e["m_b"] for e in ratios.values() if "m_b" in e)
    yb_rel = math.sqrt(sum(((mb_of(flav["varied"][n][0]) - mb_of(flav["varied"][n][1])) / 2) ** 2
                           for n in FLAVOUR_UNCERTAIN)) / mb
    out: Dict[str, Any] = {"yb_rel_sigma": yb_rel, "rows": []}

    # theory error of y_b(m_t): the last QCD order (running, decoupling) against the one below
    mb1 = FlavourRunner(x, steps, qcd_loops=runner.loops - 1)
    yb_rel_th = abs(mb1.ratios_at([mb1.mt_msbar])[mb1.mt_msbar]["m_b"] / mb - 1)

    # --- Standard Model up to M_P: no unknowns, every condition is a prediction
    sm_rows = [r for r in alpha_unif["rows"] if not math.isfinite(r["M_S"])][0]
    sm_row = sm_rows["loop2"]
    r_sm = yuk["btau_SM"][0]["yb_over_ytau"]
    crow = {k: r["m_h"] for k, r in crit["row"].items()}
    # Part L's last orders: three-loop running against two, three-loop matching against two,
    # four-loop QCD (running, decoupling, top mass) against three
    # matching: SMDR's (full two-loop plus leading three-loop) against this script's own three-loop
    c_ = crow["3L/three loops"]
    parts = {"running": c_ - crow["2L/three loops"], "matching": crow["3L/SMDR-anchored"] - c_,
             "QCD": c_ - crow["3L/three loops, QCD 3"]}
    sm_th = {"U": abs(sm_row["inv_alpha"] - sm_rows["loop1"]["inv_alpha"]),
             "B": yb_rel_th,
             "H": math.sqrt(sum(d * d for d in parts.values()))}
    out["SM_theory_H_parts"] = parts
    sm_in = {"U": math.hypot(sm_row["sigma_inputs"], a_err), "B": yb_rel,
             "H": math.hypot(crit["sigma_total"], mh_err)}
    sm_gap = {"U": sm_row["inv_alpha"] - a_meas, "B": (r_sm - 1) / r_sm, "H": crit["central"]["m_h"] - mh_meas}
    sm_pull = {c: sm_gap[c] / sm_in[c] for c in JOINT_CONDITIONS}
    sm_pull_th = {c: sm_gap[c] / math.hypot(sm_in[c], sm_th[c]) for c in JOINT_CONDITIONS}
    out["SM_pulls"], out["SM_pulls_theory"], out["SM_theory_sigma"] = sm_pull, sm_pull_th, sm_th

    # --- MSSM above M_S
    l_lo, l_hi = math.log(mt), math.log(alpha_unif["scan_top_GeV"])
    alpha_cache: Dict[float, Dict[str, float]] = {}

    def unif_at(l_ms: float) -> Dict[str, float]:
        if l_ms not in alpha_cache:
            alpha_cache[l_ms] = predict_alpha(s2, a_s, mz, math.exp(l_ms), 2)
        return alpha_cache[l_ms]

    def alpha_at(l_ms: float) -> float:
        return unif_at(l_ms)["inv_alpha"]

    def mh_from(state: List[float], m_s: float, lam: float, vev: float, mt_: float) -> float:
        down = integrate_ln_mu(state + [lam], m_s, mt_, sm_higgs_rhs(), [], steps)
        return math.sqrt(down[6]) * vev if down[6] > 0 else 0.0

    n_ms, n_tb = int(num("joint_ms_points")), int(num("joint_tan_beta_points"))
    grid_l = [l_lo + (l_hi - l_lo) * k / (n_ms - 1) for k in range(n_ms)]
    sig_u, sig_h, th_u, th_h = {}, {}, {}, {}
    for l_ms in grid_l:               # input errors at each grid M_S (used at the nearest one)
        d = [predict_alpha(s2 + sig("s2_hat_Z"), a_s, mz, math.exp(l_ms), 2)["inv_alpha"] - alpha_at(l_ms),
             predict_alpha(s2, a_s + sig("alpha_s_MZ"), mz, math.exp(l_ms), 2)["inv_alpha"] - alpha_at(l_ms)]
        sig_u[l_ms] = math.hypot(math.hypot(*d), a_err)
        dm = []
        ref = None
        for ov in (None, {"M_t": inp("M_t") + sig("M_t")}, {"alpha_s_MZ": a_s + sig("alpha_s_MZ")}):
            mt_o, v_o, _, st_o = sm_state_at_mt(ov) if ov else (mt, v, None, st)
            s_ms = integrate_ln_mu(st_o, mt_o, math.exp(l_ms), yukawa_rhs("SM"), [], steps)
            # tan(beta) = 0 gives cos^2(2 beta) = 1, the same tree value as tan(beta) -> infinity
            m = mh_from(s_ms, math.exp(l_ms), mssm_lambda_at_ms(s_ms, 0, math.sqrt(6)), v_o, mt_o)
            if ref is None:
                ref = m
            else:
                dm.append(m - ref)
        sig_h[l_ms] = math.hypot(math.hypot(*dm), mh_err)
        # theory: unification at one loop against two; m_h with two-loop running against one,
        # and with Part L's one-loop matching against tree level (at tan beta -> infinity, X_t^2 = 6 M_S^2)
        th_u[l_ms] = abs(alpha_at(l_ms) - predict_alpha(s2, a_s, mz, math.exp(l_ms), 1)["inv_alpha"])
        s_ms = integrate_ln_mu(st, mt, math.exp(l_ms), yukawa_rhs("SM"), [], steps)
        lam_k = mssm_lambda_at_ms(s_ms, 0, math.sqrt(6))
        m11 = mh_from_ms(s_ms, math.exp(l_ms), lam_k, x, v, mt, 1, False)
        th_h[l_ms] = math.hypot(mh_from_ms(s_ms, math.exp(l_ms), lam_k, x, v, mt, 2, False) - m11,
                                mh_from_ms(s_ms, math.exp(l_ms), lam_k, x, v, mt, 1, True) - m11)

    def nearest(l_ms: float) -> float:
        return min(grid_l, key=lambda g: abs(g - l_ms))

    def tb_range(s_ms: List[float]) -> Tuple[float, float]:
        sb_min, cb_min = s_ms[3] / PERTURBATIVE_LIMIT, s_ms[4] / PERTURBATIVE_LIMIT
        return sb_min / math.sqrt(1 - sb_min ** 2), math.sqrt(1 - cb_min ** 2) / cb_min

    def point(l_ms: float, s_ms: List[float], l_tb: float) -> Dict[str, Any] | None:
        """All three pulls at one (M_S, tan beta); None where a Yukawa coupling leaves
        perturbation theory below M_GUT (where the three gauge couplings meet for this M_S,
        Part I's two-loop running: the scale b-tau unification refers to, as in Part J)."""
        m_s, tb = math.exp(l_ms), math.exp(l_tb)
        sb, cb = tb / math.sqrt(1 + tb * tb), 1 / math.sqrt(1 + tb * tb)
        m_gut = unif_at(l_ms)["M_GUT"]
        if not math.isfinite(m_gut):
            return None
        mg, sg = unification_point([s_ms[0], s_ms[1], s_ms[2], s_ms[3] / sb, s_ms[4] / cb, s_ms[5] / cb],
                                   m_s, "MSSM", m_gut)
        if not math.isfinite(mg):
            return None
        g = nearest(l_ms)
        r = sg[4] / sg[5]
        m0 = mh_from(s_ms, m_s, mssm_lambda_at_ms(s_ms, tb, 0), v, mt)
        m3 = mh_from(s_ms, m_s, mssm_lambda_at_ms(s_ms, tb, math.sqrt(6)), v, mt)
        gap_h = (m0 - mh_meas) if mh_meas < m0 else (mh_meas - m3) if mh_meas > m3 else 0.0
        gaps = {"U": alpha_at(l_ms) - a_meas, "B": (r - 1) / r, "H": gap_h}
        sin = {"U": sig_u[g], "B": yb_rel, "H": sig_h[g]}
        sth = {"U": th_u[g], "B": yb_rel_th, "H": th_h[g]}
        return {"pull": {c: gaps[c] / sin[c] for c in JOINT_CONDITIONS},
                "pull_th": {c: gaps[c] / math.hypot(sin[c], sth[c]) for c in JOINT_CONDITIONS},
                "ratio": r}

    n_bis = int(num("joint_bisections"))

    def candidates(l_ms: float) -> List[Dict[str, Any]]:
        """Every tan(beta) worth testing at this M_S: a grid over the perturbative range, plus each
        root of y_b/y_tau = 1 and each edge of perturbation theory, located by bisection. b-tau is
        so sharp (the y_b error is 0.5 percent) that only its roots can satisfy it."""
        s_ms = integrate_ln_mu(st, mt, math.exp(l_ms), yukawa_rhs("SM"), [], steps)
        lo_tb, hi_tb = tb_range(s_ms)
        ls = [math.log(lo_tb) + (math.log(hi_tb) - math.log(lo_tb)) * k / (n_tb - 1) for k in range(n_tb)]
        pts = [(lt, point(l_ms, s_ms, lt)) for lt in ls]
        edges = []
        for (la, pa), (lb, pb) in zip(pts, pts[1:]):
            if (pa is None) != (pb is None):                     # edge of perturbation theory
                good, bad = (la, lb) if pa is not None else (lb, la)
                for _ in range(n_bis):
                    mid = (good + bad) / 2
                    if point(l_ms, s_ms, mid) is None:
                        bad = mid
                    else:
                        good = mid
                edges.append((good, point(l_ms, s_ms, good)))
        valid = sorted([(lt, p) for lt, p in pts + edges if p is not None], key=lambda z: z[0])
        roots = []
        for (la, pa), (lb, pb) in zip(valid, valid[1:]):        # b-tau roots between valid points
            if (pa["ratio"] - 1) * (pb["ratio"] - 1) < 0:
                a, b, fa = la, lb, pa["ratio"] - 1
                for _ in range(n_bis):
                    mid = (a + b) / 2
                    pm = point(l_ms, s_ms, mid)
                    if pm is None:
                        b = mid
                        continue
                    if (pm["ratio"] - 1) * fa > 0:
                        a, fa = mid, pm["ratio"] - 1
                    else:
                        b = mid
                pr = point(l_ms, s_ms, a)
                if pr is not None:
                    roots.append(pr)
        return [p for _, p in valid] + roots

    # M_S: the grid, plus where unification reproduces the measured alpha (Part I) and around it,
    # because the alpha condition is sharp in M_S (3.5 units of 1/alpha per e-fold)
    l_list = list(grid_l)
    ms_i = alpha_unif.get("M_S_for_measured_alpha")
    if ms_i:
        l_star, s_l = math.log(ms_i["M_S_GeV"]), ms_i["ln_sigma"]
        l_list += [l_star + k * s_l for k in (-2, -1, 0, 1, 2) if l_lo <= l_star + k * s_l <= l_hi]
    allpts = [p for l_ms in l_list for p in candidates(l_ms)]
    out["MSSM_points"] = len(allpts)

    def chi2_of(p: Dict[str, float], conds: Sequence[str]) -> float:
        return sum(p[c] ** 2 for c in conds)

    for k in range(1, len(JOINT_CONDITIONS) + 1):
        for conds in itertools.combinations(JOINT_CONDITIONS, k):
            out["rows"].append({"hypothesis": "SM up to M_P", "conditions": conds, "unknowns": 0,
                                **_joint_verdict(chi2_of(sm_pull, conds), len(conds), 0),
                                "with_theory": _joint_verdict(chi2_of(sm_pull_th, conds), len(conds), 0)})
            n_par = 1 + (("B" in conds or "H" in conds)) + ("H" in conds)     # M_S, tan beta, X_t
            best = min((chi2_of(p["pull"], conds) for p in allpts), default=math.inf)
            best_th = min((chi2_of(p["pull_th"], conds) for p in allpts), default=math.inf)
            out["rows"].append({"hypothesis": "MSSM above M_S", "conditions": conds, "unknowns": n_par,
                                **_joint_verdict(best, len(conds), n_par),
                                "with_theory": _joint_verdict(best_th, len(conds), n_par)})
    if ms_i:
        g = nearest(math.log(ms_i["M_S_GeV"]))
        out["MSSM_theory_sigma_at_part_I"] = {"U": th_u[g], "B": yb_rel_th, "H": th_h[g],
                                              "M_S": math.exp(g)}
    out["check_U_at_part_I"] = (alpha_at(math.log(ms_i["M_S_GeV"])) - a_meas) if ms_i else math.nan
    out["survivors"] = [(r["hypothesis"], r["conditions"]) for r in out["rows"] if r["survives"]]
    out["predictive_survivors"] = [(r["hypothesis"], r["conditions"]) for r in out["rows"]
                                   if r["survives"] and r["predicts"]]
    out["survivors_theory"] = [(r["hypothesis"], r["conditions"]) for r in out["rows"]
                               if r["with_theory"]["survives"]]
    out["predictive_survivors_theory"] = [(r["hypothesis"], r["conditions"]) for r in out["rows"]
                                          if r["with_theory"]["survives"] and r["with_theory"]["predicts"]]
    return out


# =============================================================================
# 6k. SHARED HELPERS FOR PARTS N, O, P
# =============================================================================
def _propagate(f: Callable[[Dict[str, float]], float], names: Sequence[str]) -> float:
    """Input-induced error of f(x): central differences, each input moved by its own sigma."""
    v2 = 0.0
    for name in names:
        s_ = sig(name)
        if s_ == 0:
            continue
        hi = f(_float_inputs({name: inp(name) + s_}))
        lo = f(_float_inputs({name: inp(name) - s_}))
        v2 += ((hi - lo) / 2) ** 2
    return math.sqrt(v2)


def _mev_per_kg(x: Dict[str, float]) -> float:
    return x["c"] ** 2 / (x["e_charge"] * 10 ** 6)


# =============================================================================
# 6l. PART N: CAN THE QUARK AND LEPTON MASSES BE CALCULATED? CLOSED MASS FORMULAS
# =============================================================================
# Part J tested what grand unification relates (quark/lepton ratios, b-tau, the top fixed
# point). What is left are closed formulas proposed for the masses themselves, the way Part I
# tests closed formulas for 1/alpha. The best known is Koide's (1982):
#   Q = (m_1 + m_2 + m_3) / (sqrt m_1 + sqrt m_2 + sqrt m_3)^2 = 2/3,
# which no accepted theory derives. Q lies between 1/3 (equal masses) and 1 (one mass). A
# relation among masses means something only at a stated scale: pole masses are not the
# couplings of any Lagrangian at one scale, and running masses change their ratios with mu.
# The formula is tested at the pole masses, at running masses, and for the quarks.
def koide_q(m: Sequence[float]) -> float:
    return sum(m) / sum(math.sqrt(v) for v in m) ** 2


def mass_formulas(flav: Dict[str, Any]) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    names_l = ("m_e", "m_mu_MeV", "m_tau_MeV")

    def lep(x: Dict[str, float]) -> List[float]:
        return [x["m_e"] * _mev_per_kg(x) / 1000, x["m_mu_MeV"] / 1000, x["m_tau_MeV"] / 1000]

    def q_pole(x: Dict[str, float]) -> float:
        return koide_q(lep(x))

    def q_run(alpha_of: Callable[[Dict[str, float]], float]) -> Callable[[Dict[str, float]], float]:
        def f(x: Dict[str, float]) -> float:
            return koide_q([lepton_running_mass(m, x["M_Z"], alpha_of(x)) for m in lep(x)])
        return f
    target = 2 / 3
    x0 = _float_inputs()
    rows = []
    for label, f in (("charged leptons, pole masses", q_pole),
                     ("charged leptons, MS-bar at M_Z (one-loop QED, alpha(0))",
                      q_run(lambda x: x["alpha_em"])),
                     ("charged leptons, MS-bar at M_Z (one-loop QED, alpha(M_Z))",
                      q_run(lambda x: 1 / x["alpha_em_inv_MZ"]))):
        q, s_ = f(x0), _propagate(f, names_l)
        rows.append({"set": label, "Q": q, "sigma": s_, "n_sigma": abs(q - target) / s_})
    # quarks: running masses at m_t(m_t), from the flavour stage's QCD running
    mu0 = flav["runner"].mt_msbar
    r0 = flav["ratios"][mu0]

    def q_sector(r: Dict[str, float], keys: Sequence[str]) -> float:
        return koide_q([r[k] for k in keys])
    for label, keys in (("up quarks u, c, t at m_t(m_t)", ("m_u", "m_c", "m_t")),
                        ("down quarks d, s, b at m_t(m_t)", ("m_d", "m_s", "m_b"))):
        q = q_sector(r0, keys)
        v2 = 0.0
        for name, pair in flav["varied"].items():
            plus, minus = (next(r for r in p.values() if "m_u" in r) for p in pair)   # each run's m_t(m_t)
            v2 += ((q_sector(plus, keys) - q_sector(minus, keys)) / 2) ** 2
        s_ = math.sqrt(v2)
        rows.append({"set": label, "Q": q, "sigma": s_, "n_sigma": abs(q - target) / s_})
    out["koide"] = rows
    # the scale dependence: how far running moves Q, against how well the pole value fits
    out["koide_running_shift"] = rows[1]["Q"] - rows[0]["Q"]
    out["koide_pole_sigma"] = rows[0]["sigma"]
    out["koide_qed_alpha_spread"] = abs(rows[2]["Q"] - rows[1]["Q"])
    # what Q = 2/3 at pole masses would predict for m_tau from m_e and m_mu (the classic use)
    me, mmu, _ = lep(x0)
    # me + mmu + u^2 = (2/3)(sqrt me + sqrt mmu + u)^2 with u = sqrt(m_tau):  u^2 - 4 a u + 3 b - 2 a^2 = 0
    a_, b_ = math.sqrt(me) + math.sqrt(mmu), me + mmu
    u = 2 * a_ + math.sqrt(6 * a_ ** 2 - 3 * b_)
    out["koide_m_tau_MeV"] = u * u * 1000
    out["m_tau_MeV"] = inp("m_tau_MeV")
    out["m_tau_sigma_MeV"] = sig("m_tau_MeV")
    return out


# =============================================================================
# 6m. PART O: THE STRONG CP ANGLE THETA-BAR
# =============================================================================
# QCD allows a term theta (g^2/32 pi^2) G G~ that violates P and CP. Only the combination
#   theta-bar = theta - arg det(M_u M_d)
# is physical: a chiral rotation of the quarks moves phase between the two pieces. The
# Standard Model gives it no value. It would give the neutron an electric dipole moment:
#   O1. d_n from theta-bar, calculated with the leading chiral logarithm (Crewther, Di Vecchia,
#       Veneziano, Witten 1979): theta-bar makes a CP-odd pion-nucleon coupling g0, fixed at
#       leading order by the strong part of the neutron-proton mass difference,
#         g0 = delta m_N m* theta / (m-bar eps),  eps = (m_d - m_u)/(m_d + m_u),
#         m* = m_u m_d m_s / (m_s (m_u + m_d) + m_u m_d)   (de Vries et al. 2015, eq. 33),
#       and the pion loop gives d_n = e g_piNN g0/(2 F_pi) ln(m_N/m_pi) / (4 pi^2 m_N),
#       with g_piNN = g_A m_N / F_pi (Goldberger-Treiman). The measured limit on d_n then
#       bounds theta-bar. The chiral log has an unknown counterterm beside it, so the
#       coefficient is compared with the full calculations (LITERATURE).
#   O2. The proposed explanations, each tested:
#       a massless up quark (theta-bar would be unphysical): against the measured m_u;
#       the axion (Peccei-Quinn): theta-bar relaxes to zero, but the decay constant f_a is
#       new; m_a f_a is calculated (leading-order chiral perturbation theory);
#       parity (Hermitian mass matrices by symmetry, theta = 0 by P): arg det M is 0 or pi.
#   O3. Can the Standard Model's own CP violation feed theta-bar? Only through the flavour
#       invariant Im det[H_u, H_d], whose size is calculated.
def theta_coefficient(x: Dict[str, float]) -> Dict[str, float]:
    """d_n per unit theta-bar from the chiral logarithm, in e cm; every factor from inputs."""
    hbar_c_mev_cm = x["h"] / (2 * math.pi) * x["c"] / (x["e_charge"] * 10 ** 6) * 100
    m_n = x["m_n"] * _mev_per_kg(x)
    f_pi = x["f_pi_MeV"] / math.sqrt(2)
    mu_, md_, ms_ = x["m_u"], x["m_d"], x["m_s"]
    eps = (md_ - mu_) / (md_ + mu_)
    mbar = (mu_ + md_) / 2
    mstar = mu_ * md_ * ms_ / (ms_ * (mu_ + md_) + mu_ * md_)
    g0 = x["delta_mN_QCD_MeV"] * mstar / (mbar * eps)            # MeV per unit theta-bar
    gbar = g0 / (2 * f_pi)                                        # the CP-odd pi-N coupling
    g_pinn = x["g_A"] * m_n / f_pi
    log = math.log(m_n / x["m_pi_MeV"])
    dn = g_pinn * gbar * log / (4 * math.pi ** 2 * m_n) * hbar_c_mev_cm
    return {"eps": eps, "m_star_GeV": mstar, "g0_MeV": g0, "gbar": gbar, "g_piNN": g_pinn,
            "chiral_log": log, "d_n_per_theta": dn, "F_pi_MeV": f_pi}


def axion_mass_times_fa(x: Dict[str, float]) -> float:
    """m_a f_a = sqrt(z)/(1 + z) m_pi F_pi at leading order, z = m_u/m_d; in MeV^2."""
    z = x["m_u"] / x["m_d"]
    return math.sqrt(z) / (1 + z) * x["m_pi0_MeV"] * x["f_pi_MeV"] / math.sqrt(2)


def strong_cp(flav: Dict[str, Any], survey: Dict[float, Dict[str, Any]], scales: Sequence[float],
              alpha_unif: Dict[str, Any], planck: Dict[str, float]) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    x0 = _float_inputs()
    had = ("m_u", "m_d", "m_s", "delta_mN_QCD_MeV", "f_pi_MeV", "g_A", "m_n", "m_pi_MeV")
    # O1. the coefficient and the bound
    co = theta_coefficient(x0)
    co["d_n_per_theta_sigma"] = _propagate(lambda x: theta_coefficient(x)["d_n_per_theta"], had)
    co["gbar_sigma"] = _propagate(lambda x: theta_coefficient(x)["gbar"], had)
    lim = inp("d_n_limit")
    co["d_n_limit"] = lim
    co["theta_max"] = lim / co["d_n_per_theta"]
    co["literature"] = []
    for label, (v, s_) in LITERATURE["dn_theta"]["value"].items():
        c_, e_ = float(v), float(s_)
        co["literature"].append({"method": label, "d_n_per_theta": c_, "sigma": e_,
                                 "theta_max": lim / c_, "theta_max_weakest": lim / (c_ - e_)})
    co["theta_max_weakest"] = max([lim / (co["d_n_per_theta"] - co["d_n_per_theta_sigma"])]
                                  + [r["theta_max_weakest"] for r in co["literature"]])
    out["bound"] = co
    # O2a. a massless up quark
    z = inp("m_u") / inp("m_d")
    z_sig = _propagate(lambda x: x["m_u"] / x["m_d"], ("m_u", "m_d"))
    out["massless_up"] = {"m_u_GeV": inp("m_u"), "sigma": sig("m_u"), "n_sigma": inp("m_u") / sig("m_u"),
                          "z": z, "z_sigma": z_sig}
    # O2b. the axion
    maf = axion_mass_times_fa(x0)
    maf_sig = _propagate(axion_mass_times_fa, ("m_u", "m_d", "f_pi_MeV", "m_pi0_MeV"))
    ref = 10 ** 12                                                # GeV: the unit the literature quotes in
    ueV_at_ref = maf * 10 ** 3 / ref * 10 ** 6                    # micro-eV at f_a = 1e12 GeV
    nlo, nlo_s = (float(v) for v in LITERATURE["axion_mass_nlo"]["value"])
    au_ms = alpha_unif.get("M_S_for_measured_alpha", {})
    scales_fa = [("M_GUT (Part I)", au_ms.get("M_GUT_GeV")), ("M_P (Part H1)", planck["E_P_GeV"])]
    out["axion"] = {"ma_fa_MeV2": maf, "ma_fa_sigma": maf_sig,
                    "m_a_ueV_at_1e12": ueV_at_ref, "m_a_ueV_at_1e12_sigma": maf_sig / maf * ueV_at_ref,
                    "nlo_ueV": nlo, "nlo_sigma": nlo_s, "lo_minus_nlo_rel": ueV_at_ref / nlo - 1,
                    "at_scales": [{"f_a": name, "f_a_GeV": fa, "m_a_eV": maf * 10 ** 3 / fa}
                                  for name, fa in scales_fa if fa]}
    # O2c. parity: Hermitian matrices have real determinants, arg det in {0, pi}. The overall
    # sign of a sector's matrix does not change V (same eigenvectors) but flips det (3 x 3), so
    # theta-bar = 0 at tree level is always reachable. Recorded for the Part C survivor.
    mu0 = scales[0]
    surv = [r for r in survey[mu0]["classes"] if r["status"] == "tested" and r["survives"]]
    herm = []
    sv = survey[mu0]["survey"]
    for r in surv:
        nu_, a_, nd_, b_ = r["pair"]
        dets = {}
        for sector, nz, var in (("u", nu_, a_), ("d", nd_, b_)):
            m = _sector_matrix(nz, var, sv.E[0][sector], 1 / 2)
            if m is None:
                continue
            det = (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
                   - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
                   + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))
            signs = var[0]
            want = signs[0] * signs[1] * math.prod(sv.E[0][sector])
            dets[sector] = {"det_over_mheaviest3": det, "signed_eigenvalue_product": want,
                            "eigenvalue_signs": (signs[0], signs[1], 1)}
        if len(dets) == 2:
            prod_sign = math.copysign(1, dets["u"]["det_over_mheaviest3"] * dets["d"]["det_over_mheaviest3"])
            herm.append({"up": pattern_mask(r["zeros_u"]), "down": pattern_mask(r["zeros_d"]),
                         "sectors": dets, "arg_det_over_pi": 0 if prod_sign > 0 else 1})
    out["parity"] = herm
    # O3. the Standard Model's own CP-odd flavour invariant (without J, which only judges: the
    # report multiplies it in). Im det[H_u, H_d] = 2 J prod_{i<j} (y_ui^2 - y_uj^2)(y_di^2 - y_dj^2)
    r0 = flav["ratios"][mu0]
    v = flav["runner"].v
    yu = [math.sqrt(2) * r0[k] / v for k in ("m_u", "m_c", "m_t")]
    yd = [math.sqrt(2) * r0[k] / v for k in ("m_d", "m_s", "m_b")]
    prod = 1.0
    for ys in (yu, yd):
        for i in range(3):
            for j in range(i + 1, 3):
                prod *= ys[j] ** 2 - ys[i] ** 2
    out["sm_invariant"] = {"scale": mu0, "mass_difference_product": 2 * prod,
                           "y_t": yu[2], "y_b": yd[2]}
    return out


# =============================================================================
# 6n. PART P: NEUTRINO MASSES AND MIXING
# =============================================================================
# Oscillations measure two mass-squared differences and the PMNS matrix (three angles and a
# Dirac phase, delta). Not measured: the lightest mass m_0, the ordering (normal: m1 < m2 <
# m3; inverted: m3 < m1 < m2), two Majorana phases if neutrinos are their own antiparticles,
# and the origin of the masses. Each unknown is scanned, never set:
#   P1. the spectrum against m_0 (from 0 up): the smallest possible sum of the masses in each
#       ordering, against the cosmological limits (which assume the same flat LambdaCDM as
#       Part A), and the neutrinos' share of Omega_m, calculated from T_CMB;
#   P2. the beta-decay mass m_beta = sqrt(sum |U_ei|^2 m_i^2) against KATRIN;
#   P3. the double-beta mass m_bb = |sum U_ei^2 m_i|: with the two free phases its exact band is
#       [max(0, 2 max c - sum c), sum c], c_i = |U_ei|^2 m_i (the band of Part C);
#   P4. mixing patterns from discrete flavour symmetries, tested like Part C's textures:
#       fixed patterns (tribimaximal, bimaximal, golden ratio, hexagonal) predict all three
#       angles; the corrected ones (TM1, TM2: one column of the tribimaximal matrix kept, a
#       rotation with angle and phase added) have two unknowns, which the measured theta13 and
#       theta23 fix exactly: they then predict theta12 and delta. Also quark-lepton
#       complementarity, theta12 + theta_C = 45 degrees.
#   P5. what the masses say about new physics: the seesaw scale, against Part I's M_GUT and
#       Part H's M_P, and the Dirac alternative.
NU_ORDERINGS = ("NO", "IO")


def nu_params(x: Dict[str, float], o: str) -> Dict[str, float]:
    return {"s12sq": x["nu_s12sq"], "s13sq": x["nu_s13sq_" + o], "s23sq": x["nu_s23sq_" + o],
            "delta": math.radians(x["nu_delta_" + o]), "dm21": x["nu_dm21"], "dm3l": x["nu_dm3l_" + o]}


def nu_masses(p: Dict[str, float], o: str, m0: float) -> List[float]:
    """(m1, m2, m3) in eV for lightest mass m0."""
    if o == "NO":
        return [m0, math.sqrt(m0 ** 2 + p["dm21"]), math.sqrt(m0 ** 2 + p["dm3l"])]
    m2 = math.sqrt(m0 ** 2 - p["dm3l"])                      # dm3l = dm32 < 0
    return [math.sqrt(m2 ** 2 - p["dm21"]), m2, m0]


def pmns(s12sq: float, s13sq: float, s23sq: float, delta: float) -> List[List[complex]]:
    """Standard parametrization (PDG)."""
    s12, s13, s23 = math.sqrt(s12sq), math.sqrt(s13sq), math.sqrt(s23sq)
    c12, c13, c23 = math.sqrt(1 - s12sq), math.sqrt(1 - s13sq), math.sqrt(1 - s23sq)
    e = cmath.exp(1j * delta)
    return [[c12 * c13, s12 * c13, s13 / e],
            [-s12 * c23 - c12 * s23 * s13 * e, c12 * c23 - s12 * s23 * s13 * e, s23 * c13],
            [s12 * s23 - c12 * c23 * s13 * e, -c12 * s23 - s12 * c23 * s13 * e, c23 * c13]]


def pmns_angles(u: List[List[complex]]) -> Dict[str, float]:
    """s12^2, s13^2, s23^2, delta (radians, [0, 2 pi)) and J from any unitary matrix."""
    ue3 = abs(u[0][2]) ** 2
    s12sq = abs(u[0][1]) ** 2 / (1 - ue3)
    s23sq = abs(u[1][2]) ** 2 / (1 - ue3)
    s12, s13, s23 = math.sqrt(s12sq), math.sqrt(ue3), math.sqrt(s23sq)
    c12, c13, c23 = math.sqrt(1 - s12sq), math.sqrt(1 - ue3), math.sqrt(1 - s23sq)
    jj = (u[0][0] * u[1][1] * u[0][1].conjugate() * u[1][0].conjugate()).imag
    norm = c12 * s12 * c23 * s23 * c13 ** 2 * s13
    if norm == 0:
        return {"s12sq": s12sq, "s13sq": ue3, "s23sq": s23sq, "delta": math.nan, "J": jj}
    cosd = (abs(u[1][0]) ** 2 - s12sq * c23 ** 2 - c12 ** 2 * s23sq * ue3) / (2 * s12 * c12 * s23 * c23 * s13)
    sind = jj / norm
    return {"s12sq": s12sq, "s13sq": ue3, "s23sq": s23sq,
            "delta": math.atan2(sind, cosd) % (2 * math.pi), "J": jj}


def _matmul(a: List[List[complex]], b: List[List[complex]]) -> List[List[complex]]:
    return [[sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)] for i in range(3)]


def tribimaximal() -> List[List[complex]]:
    r2, r3, r6 = math.sqrt(2), math.sqrt(3), math.sqrt(6)
    return [[2 / r6, 1 / r3, 0], [-1 / r6, 1 / r3, -1 / r2], [-1 / r6, 1 / r3, 1 / r2]]


def corrected_tbm(kind: str, theta: float, phi: float) -> List[List[complex]]:
    """TM1: U_TBM R_23(theta, phi) keeps the first column; TM2: U_TBM R_13 keeps the second."""
    c, s = math.cos(theta), math.sin(theta)
    e = cmath.exp(1j * phi)
    i, j = (1, 2) if kind == "TM1" else (0, 2)
    r: List[List[complex]] = [[1 if a == b else 0 for b in range(3)] for a in range(3)]
    r[i][i], r[j][j], r[i][j], r[j][i] = c, c, s / e, -s * e
    return _matmul(tribimaximal(), r)


def _angle_pull(pred: float, meas: float, sig_: float) -> float:
    return (pred - meas) / sig_


def solve_corrected(kind: str, s13sq: float, s23sq: float) -> List[Tuple[float, float]]:
    """Every (theta, phi) with the measured theta13 and theta23 (exactly: bisection)."""
    iters = int(num("nu_bisections"))

    def ue3(th: float) -> float:
        return abs(corrected_tbm(kind, th, 0)[0][2]) ** 2
    lo, hi = 0.0, math.pi / 4                                   # |U_e3|^2 rises on [0, pi/4]
    if not ue3(lo) <= s13sq <= ue3(hi):
        return []
    for _ in range(iters):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if ue3(mid) < s13sq else (lo, mid)
    th = (lo + hi) / 2

    def g(ph: float) -> float:
        return pmns_angles(corrected_tbm(kind, th, ph))["s23sq"] - s23sq
    n = int(num("nu_phase_grid"))
    grid = [2 * math.pi * k / n for k in range(n + 1)]
    sols = []
    for a, b in zip(grid[:-1], grid[1:]):
        ga, gb = g(a), g(b)
        if ga == 0:
            sols.append((th, a))
        elif ga * gb < 0:
            for _ in range(iters):
                mid = (a + b) / 2
                if g(a) * g(mid) <= 0:
                    b = mid
                else:
                    a = mid
            sols.append((th, (a + b) / 2))
    return sols


def nu_patterns(o: str) -> Dict[str, Any]:
    x0 = _float_inputs()
    p = nu_params(x0, o)
    meas = {k: (p[k], sig(f"nu_{k}" if k == "s12sq" else f"nu_{k}_{o}")) for k in ("s12sq", "s13sq", "s23sq")}
    d_meas, d_sig = inp("nu_delta_" + o), sig("nu_delta_" + o)
    phi_g = (1 + math.sqrt(5)) / 2
    fixed = (("tribimaximal", 1 / 3), ("bimaximal", 1 / 2), ("golden ratio, tan theta12 = 1/phi", 1 / (1 + phi_g ** 2)),
             ("golden ratio, cos theta12 = phi/2", 1 - phi_g ** 2 / 4), ("hexagonal, theta12 = 30 deg", 1 / 4))
    rows = []
    for name, s12 in fixed:
        pred = {"s12sq": s12, "s13sq": 0, "s23sq": 1 / 2}
        pulls = {k: _angle_pull(pred[k], *meas[k]) for k in pred}
        chi2 = sum(v * v for v in pulls.values())
        rows.append({"pattern": name, "unknowns": 0, "predictions": 3, "pred": pred, "pulls": pulls,
                     "chi2": chi2, "n_sigma": pvalue_to_sigma(chi2_pvalue(chi2, 3))})
    for kind in ("TM1", "TM2"):
        sols = solve_corrected(kind, p["s13sq"], p["s23sq"])
        preds = []
        for th, ph in sols:
            a = pmns_angles(corrected_tbm(kind, th, ph))
            preds.append({"theta": th, "phi": ph, "s12sq": a["s12sq"], "delta_deg": math.degrees(a["delta"])})
        rec: Dict[str, Any] = {"pattern": kind + (": first column of TBM kept" if kind == "TM1"
                                                  else ": second column of TBM kept"),
                               "unknowns": 2, "predictions": 2, "solutions": preds}
        if preds:
            # errors propagated from the two measured angles that fix the unknowns
            def pred_of(x: Dict[str, float], which: str, k: int) -> float:
                q = nu_params(x, o)
                ss = solve_corrected(kind, q["s13sq"], q["s23sq"])
                # follow the same solution (nearest phase)
                th, ph = min(ss, key=lambda t: abs(math.remainder(t[1] - preds[k]["phi"], 2 * math.pi)))
                a = pmns_angles(corrected_tbm(kind, th, ph))
                return a["s12sq"] if which == "s12sq" else math.degrees(a["delta"])
            names = ("nu_s13sq_" + o, "nu_s23sq_" + o)
            for k, pr in enumerate(preds):
                pr["s12sq_sigma"] = _propagate(lambda x: pred_of(x, "s12sq", k), names)
                pr["delta_sigma"] = _propagate(lambda x: pred_of(x, "delta", k), names)
                pr["s12_pull"] = (pr["s12sq"] - meas["s12sq"][0]) / math.hypot(pr["s12sq_sigma"], meas["s12sq"][1])
                dd = math.remainder(pr["delta_deg"] - d_meas, 360)
                pr["delta_pull"] = dd / math.hypot(pr["delta_sigma"], d_sig)
            # survival is decided by theta12, the Gaussian prediction; delta is far from Gaussian
            best = min(preds, key=lambda q_: abs(q_["s12_pull"]))
            rec["chi2"] = best["s12_pull"] ** 2
            rec["n_sigma"] = abs(best["s12_pull"])
        else:
            rec["chi2"], rec["n_sigma"] = math.inf, math.inf
        rows.append(rec)
    for r in rows:
        r["survives"] = r["n_sigma"] <= num("survival_sigma")
    # quark-lepton complementarity: theta12 + theta_C = pi/4 (theta_C from |V_us|, a comparison)
    vus = _comparison("V_us")[0]
    th12 = math.asin(math.sqrt(p["s12sq"]))
    th12_sig = meas["s12sq"][1] / (2 * math.sqrt(p["s12sq"] * (1 - p["s12sq"])))
    qlc = math.degrees(th12 + math.asin(vus))
    qlc_sig = math.degrees(th12_sig)
    return {"rows": rows, "qlc": {"sum_deg": qlc, "sigma_deg": qlc_sig, "n_sigma": abs(qlc - 45) / qlc_sig},
            "delta_meas": d_meas, "delta_sigma": d_sig}


def neutrino_cosmology_unit(x: Dict[str, float]) -> float:
    """The sum of neutrino masses (eV) that gives Omega_nu h^2 = 1: relic number density from
    T_CMB, T_nu = (4/11)^(1/3) T_gamma (instantaneous decoupling), three species of nu + nu-bar."""
    hbar = x["h"] / (2 * math.pi)
    kt = x["k_B"] * x["T_CMB"]
    n_gamma = 2 * zeta3() / math.pi ** 2 * (kt / (hbar * x["c"])) ** 3      # per m^3
    n_nu = Fr(3, 11) * n_gamma                                             # per species (nu + nu-bar)
    mpc = x["au"] * 648000 / math.pi * 10 ** 6
    h100 = 100 * 1000 / mpc
    rho_c = 3 * h100 ** 2 / (8 * math.pi * x["G"])                         # kg/m^3 for h = 1
    return rho_c * x["c"] ** 2 / (float(n_nu) * x["e_charge"])            # eV


def neutrinos(cosmo: Dict[str, Any], flav: Dict[str, Any], alpha_unif: Dict[str, Any],
              planck: Dict[str, float]) -> Dict[str, Any]:
    out: Dict[str, Any] = {"orderings": {}}
    x0 = _float_inputs()
    unit = neutrino_cosmology_unit(x0)
    h_ = inp("H0") / 100
    om_m = float(cosmo["Omega_m"])
    lims = {k: _comparison(k)[0] for k in ("sum_mnu_Planck", "sum_mnu_DESI")}
    n_m0 = int(num("nu_m0_points"))
    m0_min = num("nu_m0_min")
    v = flav["runner"].v
    for o in NU_ORDERINGS:
        names = ["nu_s12sq", "nu_dm21"] + [f"nu_{k}_{o}" for k in ("s13sq", "s23sq", "delta", "dm3l")]
        p = nu_params(x0, o)
        u = pmns(p["s12sq"], p["s13sq"], p["s23sq"], p["delta"])
        ue2 = [abs(u[0][i]) ** 2 for i in range(3)]

        def total(m0: float, x: Dict[str, float] = x0) -> float:
            return sum(nu_masses(nu_params(x, o), o, m0))

        def mbeta(m0: float, x: Dict[str, float] = x0) -> float:
            q = nu_params(x, o)
            uu = pmns(q["s12sq"], q["s13sq"], q["s23sq"], q["delta"])
            return math.sqrt(sum(abs(uu[0][i]) ** 2 * m ** 2 for i, m in enumerate(nu_masses(q, o, m0))))

        def mbb_band(m0: float, x: Dict[str, float] = x0) -> Tuple[float, float]:
            q = nu_params(x, o)
            uu = pmns(q["s12sq"], q["s13sq"], q["s23sq"], q["delta"])
            c = [abs(uu[0][i]) ** 2 * m for i, m in enumerate(nu_masses(q, o, m0))]
            return max(0.0, 2 * max(c) - sum(c)), sum(c)

        rec: Dict[str, Any] = {"masses_at_m0_0": nu_masses(p, o, 0), "sum_min": total(0),
                               "sum_min_sigma": _propagate(lambda x: total(0, x), names),
                               "U_e_sq": ue2}
        # largest m0 each cosmological limit allows (bisection), or None if even m0 = 0 is above it
        rec["m0_max"] = {}
        for k, lim in lims.items():
            if total(0) > lim:
                rec["m0_max"][k] = None
                continue
            lo, hi = 0.0, lim
            for _ in range(int(num("nu_bisections"))):
                mid = (lo + hi) / 2
                lo, hi = (mid, hi) if total(mid) < lim else (lo, mid)
            rec["m0_max"][k] = (lo + hi) / 2
        rec["vs_cosmology"] = {k: {"limit": lim, "allowed": total(0) <= lim, "sum_min_minus_limit": total(0) - lim}
                               for k, lim in lims.items()}
        rec["Omega_nu_h2_at_min"] = total(0) / unit
        rec["Omega_nu_over_Omega_m_at_min"] = total(0) / unit / h_ ** 2 / om_m
        # P2, P3 over the lightest mass: 0, then a geometric grid up to the loosest cosmology limit
        top = max(m for m in rec["m0_max"].values() if m is not None) if any(
            m is not None for m in rec["m0_max"].values()) else m0_min
        grid = [0.0] + [m0_min * (top / m0_min) ** (k / (n_m0 - 1)) for k in range(n_m0)]
        rec["scan"] = [{"m0": m0, "sum": total(m0), "m_beta": mbeta(m0),
                        "m_bb_lo": mbb_band(m0)[0], "m_bb_hi": mbb_band(m0)[1]} for m0 in grid]
        rec["m_beta_min"] = mbeta(0)
        rec["m_beta_max_cosmology"] = {k: (mbeta(m) if m is not None else None) for k, m in rec["m0_max"].items()}
        lo0, hi0 = mbb_band(0)
        rec["m_bb_at_m0_0"] = (lo0, hi0)
        rec["m_bb_at_m0_0_sigma"] = (_propagate(lambda x: mbb_band(0, x)[0], names),
                                     _propagate(lambda x: mbb_band(0, x)[1], names))
        # the range of m0 where full cancellation (m_bb = 0) is possible
        # the range of m0 where full cancellation (m_bb = 0) is possible: grid, then bisection at each edge
        sc_ = rec["scan"]
        edges = []
        for a_, b_ in zip(sc_[:-1], sc_[1:]):
            za, zb = a_["m_bb_lo"] == 0, b_["m_bb_lo"] == 0
            if za != zb:
                lo, hi = a_["m0"], b_["m0"]
                for _ in range(int(num("nu_bisections"))):
                    mid = (lo + hi) / 2
                    lo, hi = (mid, hi) if (mbb_band(mid)[0] == 0) == za else (lo, mid)
                edges.append((lo + hi) / 2)
        rec["m_bb_cancellation_m0"] = (min(edges), max(edges)) if len(edges) >= 2 else None
        rec["m_bb_max_cosmology"] = {k: (mbb_band(m)[1] if m is not None else None) for k, m in rec["m0_max"].items()}
        # P5. heaviest mass at m0 = 0 sets the seesaw scale: m = y^2 v^2 / (2 M)
        m_heavy = max(nu_masses(p, o, 0)) * 10 ** -9                       # GeV
        rec["seesaw"] = {"m_heaviest_eV": m_heavy * 10 ** 9,
                         "M_for_y_1": v ** 2 / (2 * m_heavy),
                         "M_max_perturbative": PERTURBATIVE_LIMIT ** 2 * v ** 2 / (2 * m_heavy),
                         "M_for_y_top": flav["ratios"][flav["runner"].mt_msbar]["y_t"] ** 2 * v ** 2 / (2 * m_heavy),
                         "dirac_yukawa": [math.sqrt(2) * m * 10 ** -9 / v for m in nu_masses(p, o, 0)]}
        rec["patterns"] = nu_patterns(o)
        out["orderings"][o] = rec
    au_ms = alpha_unif.get("M_S_for_measured_alpha", {})
    out["M_GUT"] = au_ms.get("M_GUT_GeV")
    out["M_P"] = planck["E_P_GeV"]
    out["sum_for_omega_h2_1_eV"] = unit
    me = inp("m_e") * _mev_per_kg(x0) / 1000
    out["electron_yukawa"] = math.sqrt(2) * me / v
    return out


# =============================================================================
# 6o. PART Q: PROTON DECAY, THE DIRECT TEST OF UNIFICATION
# =============================================================================
# If the gauge couplings unify (Part I), the quarks and leptons share multiplets and the heavy
# gauge bosons X, Y of SU(5) turn quarks into leptons: the proton decays. Dimension-six exchange
# gives p -> e+ pi0 with (Ellis et al. 2020, eq. 45, minimal SU(5))
#   Gamma = m_p/(32 pi) (1 - m_pi^2/m_p^2)^2 A_L^2 (g_GUT^2/M_X^2)^2
#           x [A_S1^2 W_RL^2 + (1 + |V_ud|^2)^2 A_S2^2 W_LL^2],
# W = lattice matrix elements at 2 GeV, A_S = the two operators' running from M_X to M_Z (one
# loop, exponents -2 c_i/b_i with the script's own b_i), A_L = their QCD running from M_Z to 2 GeV.
# Every scale comes from the algorithm: M_X = M_GUT and alpha_GUT from Part I (MSSM above M_S);
# for the SM, which does not unify, the point where g1 = g2 (Part J). GUT thresholds unknown.
def _alpha_one_loop(mu: float, x: Dict[str, float], m_s: float | None) -> List[float]:
    """alpha_1 (GUT-normalized), alpha_2, alpha_3 at mu: one loop from M_Z, MSSM above m_s if given."""
    a, s2 = 1 / x["alpha_em_inv_MZ"], x["s2_hat_Z"]
    inv = [float(GUT_NORM) * (1 - s2) / a, s2 / a, 1 / x["alpha_s_MZ"]]
    b_sm = [float(b) for b in sm_gauge_b()]
    b_ms = [float(b) for b in mssm_b()[0]]
    lo = min(mu, m_s) if m_s else mu
    out = [i - b / (2 * math.pi) * math.log(lo / x["M_Z"]) for i, b in zip(inv, b_sm)]
    if m_s and mu > m_s:
        out = [i - b / (2 * math.pi) * math.log(mu / m_s) for i, b in zip(out, b_ms)]
    return [1 / v for v in out]


def proton_exponents(model: str, op: str) -> List[float]:
    """-2 c_i / b_i for (alpha_1, alpha_2, alpha_3): the running of one dimension-six operator."""
    c = [float(Fr(v)) for v in LITERATURE["proton_decay_d6"]["value"][model][op]]
    b = [float(v) for v in (sm_gauge_b() if model == "SM" else mssm_b()[0])]
    return [-2 * ci / bi for ci, bi in zip(c, b)]


def proton_short_distance(x: Dict[str, float], m_x: float, m_s: float | None, op: str) -> float:
    """A_S: the operator's coefficient at M_Z over its value at M_X."""
    steps = [("MSSM", m_x, m_s), ("SM", m_s, x["M_Z"])] if m_s else [("SM", m_x, x["M_Z"])]
    a_s = 1.0
    for model, hi, lo in steps:
        a_hi, a_lo = _alpha_one_loop(hi, x, m_s), _alpha_one_loop(lo, x, m_s)
        for e, al, ah in zip(proton_exponents(model, op), a_lo, a_hi):
            a_s *= (al / ah) ** e
    return a_s


def proton_long_distance(runner: "FlavourRunner", x: Dict[str, float]) -> float:
    """A_L: QCD running of the operators from M_Z to the matrix elements' scale (one loop in the
    exponent 2 c_3 / b0 per flavour region, alpha_s from the script's four-loop running)."""
    c3 = float(Fr(LITERATURE["proton_decay_d6"]["value"]["SM"]["S1"][2]))
    pts = [(x["M_Z"], 5), (x["m_b"], 4), (x["mu_light"], 4)]
    a_l = 1.0
    for (hi, nf), (lo, _) in zip(pts[:-1], pts[1:]):
        b0 = float(qcd_beta(nf)[0])
        a_l *= (runner.alpha_s(lo) / runner.alpha_s(hi)) ** (2 * c3 / b0)
    return a_l


def proton_lifetime(x: Dict[str, float], m_x: float, alpha_gut: float, m_s: float | None, a_l: float) -> float:
    """tau(p -> e+ pi0) in years."""
    gev = x["e_charge"] * 10 ** 9
    m_p = x["m_p"] * x["c"] ** 2 / gev
    m_pi = x["m_pi0_MeV"] / 1000
    g2 = 4 * math.pi * alpha_gut
    s1, s2 = proton_short_distance(x, m_x, m_s, "S1"), proton_short_distance(x, m_x, m_s, "S2")
    amp2 = s1 ** 2 * x["W_pi0_RL"] ** 2 + (1 + x["V_ud"] ** 2) ** 2 * s2 ** 2 * x["W_pi0_LL"] ** 2
    width = m_p / (32 * math.pi) * (1 - m_pi ** 2 / m_p ** 2) ** 2 * a_l ** 2 * (g2 / m_x ** 2) ** 2 * amp2
    hbar_gev_s = x["h"] / (2 * math.pi) / gev
    return hbar_gev_s / width / 31557600                      # Julian year


# --- Q2. Dimension five: p -> K+ nubar through the colour-triplet Higgsinos of minimal SUSY SU(5)
# (Hisano, Kobayashi, Kuwahara, Nagata 2013, arXiv:1304.3651, eqs. 15-49). The triplet mass M_HC
# is set to Part I's M_GUT, every superpartner (sfermions, wino, higgsino) to Part I's M_S, and
# tan(beta) is Part J's. The unknown GUT phases phi_2, phi_3 (phi_1 = -phi_2 - phi_3) are scanned,
# and the band of lifetimes is reported. Yukawas: SM running to M_S (Parts B, J), MSSM above;
# operator running between M_HC and M_S with the Yukawas (eqs. 41, 42), gauge-only below (eqs. 37,
# 38, SM b_i), QCD to 2 GeV (eq. 24). Not included: the wino and higgsino thresholds between M_S and
# M_Z (taken at M_S), two-loop running, and the GUT-scale thresholds that fix M_HC.
def ckm_from_wolfenstein(x: Dict[str, float]) -> List[List[complex]]:
    """The CKM matrix from the PDG fit's Wolfenstein parameters, exactly (PDG convention)."""
    lam, a, rho, eta = x["CKM_lambda"], x["CKM_A"], x["CKM_rhobar"], x["CKM_etabar"]
    s12, s23 = lam, a * lam ** 2
    z = complex(rho, eta)
    s13e = a * lam ** 3 * z * math.sqrt(1 - a * a * lam ** 4) / (math.sqrt(1 - lam * lam) * (1 - a * a * lam ** 4 * z))
    s13, delta = abs(s13e), cmath.phase(s13e)
    return pmns(s12 ** 2, s13 ** 2, s23 ** 2, delta)          # same standard parametrization


def _f_susy(m: float, ms: float) -> float:
    """F(M, M_S^2) of eq. 16; its limit 1/(2 M_S) at M = M_S (eq. 18)."""
    if abs(m / ms - 1) < num("check_rel_tol"):
        return 1 / (2 * ms)
    d = ms ** 2 - m ** 2
    return m * (1 / d - m ** 2 / d ** 2 * math.log(ms ** 2 / m ** 2))


def proton_decay_d5(flav: Dict[str, Any], m_s: float, m_hc: float, tan_beta: float) -> Dict[str, Any]:
    x = _float_inputs()
    runner = flav["runner"]
    mt = runner.mt_msbar
    mz, mw = x["M_Z"], x["M_W"]
    q2 = x["mu_light"]
    up, dn = Fr(2, 3), Fr(-1, 3)
    sb, cb = tan_beta / math.sqrt(1 + tan_beta ** 2), 1 / math.sqrt(1 + tan_beta ** 2)
    s2b = 2 * sb * cb
    k = 16 * math.pi ** 2

    def drbar(m: float, mu: float) -> float:                  # eq. 21
        return m * (1 - runner.alpha_s(mu) / (3 * math.pi))
    # quark masses (MS-bar -> DR-bar) at m_Z and at 2 GeV
    src = {"d": (x["m_d"], q2, dn), "s": (x["m_s"], q2, dn), "c": (x["m_c"], x["m_c"], up),
           "b": (x["m_b"], x["m_b"], dn), "t": (mt, mt, up)}
    m_z = {q: drbar(runner.run_mass(m0, mu0, mz, ch), mz) for q, (m0, mu0, ch) in src.items()}
    m_2 = {q: drbar(runner.run_mass(m0, mu0, q2, ch) if mu0 != q2 else m0, q2) for q, (m0, mu0, ch) in src.items()}
    lep = lepton_masses_gev()
    a0 = inp("alpha_em")
    mtau_z = lepton_running_mass(lep["tau"], mz, a0)
    # third-generation couplings at M_S (SM), second generation from the flavour stage's ratios
    _, st = couplings_at_mt(flav)
    s_ms = run_to(st, mt, m_s, "SM")
    r_ms = flav["ratios"][min(flav["ratios"], key=lambda mu: abs(math.log(mu / m_s)))]
    # MSSM couplings at M_S: y_u / sin(beta), y_d, y_e / cos(beta) (eq. 30); then run to M_HC with
    # the ratios y_c/y_t and y_s/y_b (MSSM anomalous dimensions) and the operators' exponents
    y0 = [s_ms[0], s_ms[1], s_ms[2], s_ms[3] / sb, s_ms[4] / cb, s_ms[5] / cb,
          math.log(r_ms["r_ct"]), math.log(r_ms["r_sb"]), 0.0, 0.0, 0.0, 0.0, 0.0]
    gauge6 = yukawa_rhs("MSSM")
    r_mu_tau = lep["mu"] / lep["tau"]

    def rhs(v: List[float], nf: int) -> List[float]:
        g1, g2, g3, yt, yb, yl = v[:6]
        out = gauge6(v[:6], nf)
        yc, ys = yt * math.exp(v[6]), yb * math.exp(v[7])
        gg = 8 * g3 ** 2 + 6 * g2 ** 2 + Fr(2, 5) * g1 ** 2
        ups, dns, els = (yc, yt), (ys, yb), (yl * r_mu_tau, yl)
        ints = [(2 * (ups[i] ** 2 + dns[j] ** 2) + els[j] ** 2 - float(gg)) / k for i in range(2) for j in range(2)]
        cbar = (2 * (yt ** 2 + yl ** 2) - 8 * g3 ** 2 - float(Fr(12, 5)) * g1 ** 2) / k
        return out + [-(3 * yt ** 2 + yb ** 2) / k, -(3 * yb ** 2 + yt ** 2) / k] + ints + [cbar]
    top = integrate_ln_mu(y0, m_s, m_hc, rhs, [], int(num("rg_steps_per_efold")))
    f = {"t": top[3], "b": top[4], "tau": top[5], "c": top[3] * math.exp(top[6]), "s": top[4] * math.exp(top[7])}
    # C_ij(M_S)/C_ij(M_HC) = exp(-integral of the exponent from M_S to M_HC)
    c_ratio = {(i, j): math.exp(-top[8 + 2 * a + b]) for a, i in enumerate(("c", "t")) for b, j in enumerate(("s", "b"))}
    cbar_ratio = math.exp(-top[12])
    # gauge-only running from M_S to m_Z (eqs. 37, 38; SM b_i)
    b_sm = [float(b) for b in sm_gauge_b()]
    al_s, al_z = _alpha_one_loop(m_s, x, None), _alpha_one_loop(mz, x, None)
    ratio = [z_ / s_ for z_, s_ in zip(al_z, al_s)]
    c_wino = ratio[2] ** (-2 / b_sm[2]) * ratio[1] ** (-15 / (2 * b_sm[1])) * ratio[0] ** (-1 / (10 * b_sm[0]))
    c_higgsino = ratio[2] ** (-2 / b_sm[2]) * ratio[1] ** (-9 / (4 * b_sm[1])) * ratio[0] ** (-11 / (20 * b_sm[0]))
    a2_z, a2_s = al_z[1], al_s[1]
    # QCD below m_Z (eq. 24)
    as2, asb, asz = runner.alpha_s(q2), runner.alpha_s(x["m_b"]), runner.alpha_s(mz)
    a_l = (as2 / asb) ** Fr(-18, 25) * (asb / asz) ** Fr(-18, 23)
    abar_l = (as2 / asb) ** Fr(-6, 5) * (asb / asz) ** Fr(-30, 23)
    a_s = {(i, j): mw ** 2 * s2b * f[i] * f[j] / (4 * math.pi * m_z[i] * m_z[j]) * a2_s / a2_z ** 2
           * c_wino * c_ratio[(i, j)] for i in ("c", "t") for j in ("s", "b")}
    ybar_t_ms, ybar_tau_ms = s_ms[3] / sb, s_ms[5] / cb
    abar_s = (mw ** 4 * s2b ** 2 * f["t"] * ybar_t_ms * ybar_tau_ms * f["s"]
              / ((4 * math.pi) ** 2 * a2_z ** 2 * m_z["t"] ** 2 * mtau_z * m_z["s"]) * c_higgsino * cbar_ratio)
    a_r = {key: a_l * v for key, v in a_s.items()}
    abar_r = abar_l * abar_s
    # hadronic matrix elements and the width (eqs. 44-49)
    v = ckm_from_wolfenstein(x)
    gev = x["e_charge"] * 10 ** 9
    m_p = x["m_p"] * x["c"] ** 2 / gev
    m_k, m_bar = x["m_K_MeV"] / 1000, (x["m_Sigma0_MeV"] + x["m_Lambda_MeV"]) / 2000
    f_pi = x["f_pi_MeV"] / math.sqrt(2) / 1000
    d_, f_ = x["baryon_D"], x["baryon_F"]
    al_p, be_p = x["alpha_p_lattice"], x["beta_p_lattice"]
    f_w, f_h = _f_susy(m_s, m_s), _f_susy(m_s, m_s)            # wino and higgsino at M_S
    chi = 1 + (d_ + f_) * m_p / m_bar
    idx = {"u": 0, "c": 1, "t": 2, "d": 0, "s": 1, "b": 2}

    def amplitudes(ph2: float, ph3: float) -> Tuple[complex, complex]:
        ph = {"c": ph2, "t": ph3}
        ph1 = -ph2 - ph3
        wino = {j: sum(m_2[i] * v[idx[i]][0] * v[idx[i]][1] * cmath.exp(1j * ph[i]) * a_r[(i, j)] for i in ("c", "t"))
                for j in ("s", "b")}
        c_mu = 2 * be_p * f_w * chi * m_2["s"] * v[0][1].conjugate() * wino["s"]
        higg = (al_p * m_2["t"] ** 2 * mtau_z * v[2][2].conjugate() * cmath.exp(1j * ph1) / (mw ** 2 * s2b)
                * f_h * abar_r * (m_2["d"] * v[0][0] * v[2][1] * (1 + (d_ + 3 * f_) / 3 * m_p / m_bar)
                                  + m_2["s"] * v[0][1] * v[2][0] * 2 * d_ / 3 * m_p / m_bar))
        c_tau = 2 * be_p * f_w * chi * m_2["b"] * v[0][2].conjugate() * wino["b"] - higg
        return c_mu, c_tau

    pre = m_p * a2_z ** 4 / (64 * math.pi * f_pi ** 2 * m_hc ** 2 * mw ** 4 * s2b ** 2) * (1 - m_k ** 2 / m_p ** 2) ** 2
    hbar_gev_s = x["h"] / (2 * math.pi) / gev
    n_ph = int(num("proton_phase_grid"))
    taus = []
    for a in range(n_ph):
        for b in range(n_ph):
            cm, ct = amplitudes(2 * math.pi * a / n_ph, 2 * math.pi * b / n_ph)
            taus.append(hbar_gev_s / (pre * (abs(cm) ** 2 + abs(ct) ** 2)) / 31557600)
    cm0, ct0 = amplitudes(0, 0)
    higg_only = hbar_gev_s / (pre * abs(ct0 - 2 * be_p * f_w * chi * m_2["b"] * v[0][2].conjugate()
                                         * sum(m_2[i] * v[idx[i]][0] * v[idx[i]][1] * a_r[(i, "b")]
                                               for i in ("c", "t"))) ** 2) / 31557600
    return {"tan_beta": tan_beta, "M_S": m_s, "M_HC": m_hc, "A_L": a_l, "Abar_L": abar_l,
            "A_R": {f"{i}{j}": val for (i, j), val in a_r.items()}, "Abar_R": abar_r,
            "f_GUT": f, "tau_min": min(taus), "tau_max": max(taus), "tau_higgsino_only": higg_only}


def proton_decay(flav: Dict[str, Any], alpha_unif: Dict[str, Any], yukawa: Dict[str, Any]) -> Dict[str, Any]:
    x0 = _float_inputs()
    runner = flav["runner"]
    a_l = proton_long_distance(runner, x0)
    lim = _comparison("tau_p_e_pi0")[0]
    rows = []
    au = alpha_unif.get("M_S_for_measured_alpha", {})
    hyps = []
    if au.get("M_GUT_GeV"):
        hyps.append(("MSSM above M_S (Part I)", au["M_GUT_GeV"], au["alpha_GUT"], au["M_S_GeV"]))
    sm12 = yukawa["btau_SM"][0]["mu"]
    if math.isfinite(sm12):
        hyps.append(("SM, X bosons where g1 = g2 (Part J)", sm12, _alpha_one_loop(sm12, x0, None)[1], None))
    names = ("W_pi0_RL", "W_pi0_LL", "V_ud", "m_p", "m_pi0_MeV")
    for label, m_x, a_g, m_s in hyps:
        tau = proton_lifetime(x0, m_x, a_g, m_s, a_l)
        tau_sig = _propagate(lambda x: proton_lifetime(x, m_x, a_g, m_s, a_l), names)
        rows.append({"hypothesis": label, "M_X": m_x, "alpha_GUT": a_g, "M_S": m_s,
                     "A_S1": proton_short_distance(x0, m_x, m_s, "S1"),
                     "A_S2": proton_short_distance(x0, m_x, m_s, "S2"),
                     "tau_years": tau, "tau_sigma": tau_sig, "limit": lim, "allowed": tau > lim,
                     "ratio_to_limit": tau / lim, "M_X_needed": m_x * (lim / tau) ** (1 / 4)})
    d5 = []
    lim_k = _comparison("tau_p_K_nu")[0]
    if au.get("M_GUT_GeV") and yukawa.get("btau_MSSM_unity"):
        tbs = [yukawa["btau_MSSM_unity"]["tan_beta"]] + [r["tan_beta"] for r in yukawa.get("fixed_point_MSSM", {}).get("runs", [])]
        for tb in tbs:
            r5 = proton_decay_d5(flav, au["M_S_GeV"], au["M_GUT_GeV"], tb)
            r5["allowed_somewhere"] = r5["tau_max"] > lim_k
            r5["allowed_everywhere"] = r5["tau_min"] > lim_k
            # M_HC that the limit needs (the lifetime grows as M_HC^2, at the most favourable phases)
            r5["M_HC_needed"] = r5["M_HC"] * math.sqrt(lim_k / r5["tau_max"])
            r5["M_S_needed_scaling"] = r5["M_S"] * math.sqrt(lim_k / r5["tau_max"])
            d5.append(r5)
    return {"A_L": a_l, "A_L_two_loop_quoted": float(LITERATURE["proton_decay_d6"]["value"]["A_L_two_loop"]),
            "rows": rows, "limit_e_pi0": lim, "limit_K_nu": lim_k, "d5": d5}


# =============================================================================
# 6p. PART R: WHAT ANOMALY CANCELLATION FIXES (exact)
# =============================================================================
# A chiral gauge theory is consistent only if its gauge anomalies cancel. These are exact
# polynomial conditions on the charges, and they are the one place where the Standard Model's
# "free" quantum numbers are calculated:
#   R1. hypercharges: with one family of the SM's representations and unknown hypercharges,
#       [SU(3)]^2 U(1), [SU(2)]^2 U(1), [gravity]^2 U(1) and U(1)^3 leave the SM's assignment
#       (up to normalization and naming u^c <-> d^c) or a branch with Y_Q = 0; the Yukawa
#       couplings select the SM. Electric charge is then quantized: q_p + q_e = 0 exactly.
#       A right-handed neutrino reopens one direction (B - L); a Majorana mass closes it.
#   R2. Witten's global SU(2) anomaly: an even number of doublets.
#   R3. 3-3-1 (Part D): [SU(3)_L]^3 cancels only if the number of families is a multiple of the
#       number of colours; with QCD asymptotically free, exactly three families.
FIELDS_ONE_FAMILY = (("Q", 3, 2), ("u^c", 3, 1), ("d^c", 3, 1), ("L", 1, 2), ("e^c", 1, 1))


def sm_anomalies(y: Dict[str, Fr], extra: Sequence[Tuple[str, int, int]] = ()) -> Dict[str, Fr]:
    """The four hypercharge anomalies of one family (left-handed Weyl fields)."""
    fields = FIELDS_ONE_FAMILY + tuple(extra)
    return {"SU3^2 U1": sum(y[n] * d2 for n, d3, d2 in fields if d3 == 3),
            "SU2^2 U1": sum(y[n] * d3 for n, d3, d2 in fields if d2 == 2),
            "grav^2 U1": sum(y[n] * d3 * d2 for n, d3, d2 in fields),
            "U1^3": sum(y[n] ** 3 * d3 * d2 for n, d3, d2 in fields)}


def _rational_sqrt(q: Fr) -> Fr | None:
    if q < 0:
        return None
    n, d = math.isqrt(q.numerator), math.isqrt(q.denominator)
    return Fr(n, d) if n * n == q.numerator and d * d == q.denominator else None


def hypercharge_solutions() -> Dict[str, Any]:
    """Every hypercharge assignment of one family with cancelling anomalies (exact)."""
    # the three linear conditions give Y_L, Y_d, Y_e from Y_Q, Y_u; U(1)^3 is then quadratic in Y_u
    def complete(yq: Fr, yu: Fr) -> Dict[str, Fr]:
        return {"Q": yq, "u^c": yu, "d^c": -2 * yq - yu, "L": -3 * yq, "e^c": 6 * yq}
    yq = Fr(1, 6)                                   # the normalization (any nonzero value scales)
    pts = [Fr(k) for k in range(3)]
    vals = [sm_anomalies(complete(yq, p))["U1^3"] for p in pts]
    # quadratic through three points: a t^2 + b t + c
    c = vals[0]
    a = (vals[2] - 2 * vals[1] + vals[0]) / 2
    b = vals[1] - vals[0] - a
    disc = _rational_sqrt(b * b - 4 * a * c)
    roots = sorted({(-b + s_ * disc) / (2 * a) for s_ in (1, -1)}) if disc is not None and a != 0 else []
    sols = [complete(yq, r) for r in roots]
    ok = all(all(v == 0 for v in sm_anomalies(s_).values()) for s_ in sols)
    # the Y_Q = 0 branch: Y_L = Y_e = 0, Y_d = -Y_u, any Y_u (only right-handed quarks charged)
    branch = complete(Fr(0), Fr(1))
    branch_ok = all(v == 0 for v in sm_anomalies(branch).values())
    # Yukawa couplings Q H u^c, Q H* d^c, L H* e^c: Y_H = -Y_Q - Y_u = Y_Q + Y_d = Y_L + Y_e
    def yukawa_ok(s_: Dict[str, Fr]) -> bool:
        yh = -s_["Q"] - s_["u^c"]
        return yh == s_["Q"] + s_["d^c"] == s_["L"] + s_["e^c"] and yh != 0
    sm_like = [s_ for s_ in sols if yukawa_ok(s_)]
    out: Dict[str, Any] = {"solutions": sols, "all_cancel": ok, "Y_Q_zero_branch_cancels": branch_ok,
                           "Y_Q_zero_branch_has_yukawas": yukawa_ok(branch), "with_yukawas": sm_like}
    # charges: Q = T3 + Y / (2 Y_H), so that the Higgs' neutral component is neutral (a photon)
    if sm_like:
        s_ = sm_like[0]
        yh = -s_["Q"] - s_["u^c"]
        norm = 1 / (2 * yh)
        q_u, q_d = Fr(1, 2) + s_["Q"] * norm, -Fr(1, 2) + s_["Q"] * norm
        q_e = -Fr(1, 2) + s_["L"] * norm
        out["charges"] = {"u": q_u, "d": q_d, "e": q_e, "nu": Fr(1, 2) + s_["L"] * norm,
                          "proton_plus_electron": 2 * q_u + q_d + q_e, "neutron": q_u + 2 * q_d,
                          "Y_H": yh}
    # a right-handed neutrino nu^c (singlet): the SM plus eps (B - L) cancels for every eps
    bl = {"Q": Fr(1, 3), "u^c": Fr(-1, 3), "d^c": Fr(-1, 3), "L": Fr(-1), "e^c": Fr(1), "nu^c": Fr(1)}
    if sm_like:
        base = dict(sm_like[0])
        base["nu^c"] = Fr(0)
        fam = [{k: base[k] + e * bl[k] for k in bl} for e in (Fr(1, 7), Fr(-2, 3), Fr(5))]
        out["nu_R_family_cancels"] = all(all(v == 0 for v in sm_anomalies(f_, [("nu^c", 1, 1)]).values())
                                         for f_ in fam)
        f_ = fam[0]
        yh = -f_["Q"] - f_["u^c"]
        qu, qd = Fr(1, 2) + f_["Q"] / (2 * yh), -Fr(1, 2) + f_["Q"] / (2 * yh)
        qe = -Fr(1, 2) + f_["L"] / (2 * yh)
        # hydrogen has B - L = 0, so it stays neutral; the neutron (B - L = 1) does not
        out["nu_R_hydrogen_charge"] = 2 * qu + qd + qe
        out["nu_R_neutron_charge_per_eps"] = (qu + 2 * qd) / Fr(1, 7)
        # Dirac Yukawa L H nu^c holds for every eps; a Majorana mass nu^c nu^c needs Y(nu^c) = 0, so eps = 0
        out["nu_R_dirac_yukawa_ok"] = f_["L"] + yh + f_["nu^c"] == 0
    return out


def anomaly_constraints(yuk331: Dict[int, Dict[str, Any]]) -> Dict[str, Any]:
    out: Dict[str, Any] = {"hypercharge": hypercharge_solutions()}
    # R2. Witten: doublets per family (colour copies count)
    per_family = sum(d3 for _, d3, d2 in FIELDS_ONE_FAMILY if d2 == 2)
    out["witten_doublets_per_family"] = per_family
    # R3. 3-3-1: [SU(3)_L]^3 = (#triplets - #antitriplets); leptons in triplets, quarks with colour
    n_c = int(su_n_casimirs(3)[0])
    q331 = yuk331[-1]["quarks"]
    k_trip = sum(1 for q in q331.values() if q["rep"] == "3")
    n_f = len(q331)
    out["331_part_D"] = {"families": n_f, "quark_triplet_families": k_trip,
                         "SU3L_cubed": n_f + n_c * k_trip - n_c * (n_f - k_trip)}
    # every family number up to a bound, every split: which cancel?
    allowed = []
    for nf in range(1, 4 * n_c):
        for k in range(nf + 1):
            if nf + n_c * k - n_c * (nf - k) == 0:
                # QCD: each 3-3-1 family has three quark flavours (two SM, one exotic)
                b0 = Fr(11, 3) * n_c - Fr(2, 3) * 3 * nf
                allowed.append({"families": nf, "triplet_families": k, "qcd_b0": b0, "asymptotically_free": b0 > 0})
    out["331_allowed"] = allowed
    out["331_families_with_af"] = [a["families"] for a in allowed if a["asymptotically_free"]]
    return out


# =============================================================================
# 6q. PART S: THE BARYON ASYMMETRY
# =============================================================================
# The universe has baryons and almost no antibaryons: eta_B = n_B / n_gamma, calculated here from
# the measured baryon density and T_CMB. Making it needs Sakharov's three conditions (B violation,
# C and CP violation, departure from equilibrium).
#   S1. eta_B from Omega_b h^2 and T_CMB.
#   S2. The Standard Model alone: sphalerons violate B + L (Delta B = Delta L = N_f per transition,
#       from the SU(2) anomaly of Part R) and convert lepton number to baryon number by a factor
#       fixed by chemical equilibrium, solved exactly here. But the transition is a crossover for
#       the measured Higgs mass (lattice), and the CKM CP violation at T_c is the flavour invariant
#       of Part O over T_c^12: both fail.
#   S3. Leptogenesis (the seesaw of Part P): heavy right-handed neutrinos decay out of equilibrium.
#       eta_B = c_sph (3/4) (g*s today / g*) epsilon_1 kappa (kappa <= 1, the efficiency), with every
#       factor from the field content, and Davidson-Ibarra's bound |epsilon_1| <= 3 M_1 (m_3 - m_1) /
#       (8 pi <H>^2) (their eq. 17) turns eta_B into a lower bound on M_1, against Part P's window.
def sphaleron_conversion(n_f: int, n_h: int) -> Dict[str, Fr]:
    """B / (B - L) in chemical equilibrium (fast Yukawas, sphalerons, zero hypercharge), exactly.
    Unknowns per family (all families equal): mu_Q, mu_u, mu_d, mu_L, mu_e and mu_H."""
    hyp = {name: y for name, _, _, y, _, _ in SM_FIELDS}
    # right-handed fields carry minus the hypercharge of the conjugates in SM_FIELDS
    y_q, y_u, y_d, y_l, y_e, y_h = hyp["Q"], -hyp["u^c"], -hyp["d^c"], hyp["L"], -hyp["e^c"], hyp["H"]
    # solve with mu_L = 1: Yukawas give mu_u = mu_Q + mu_H, mu_d = mu_Q - mu_H, mu_e = mu_L - mu_H;
    # sphalerons n_f (3 mu_Q + mu_L) = 0 give mu_Q = -mu_L/3; hypercharge neutrality fixes mu_H.
    mu_l = Fr(1)
    mu_q = -mu_l / 3

    def charge(mu_h: Fr) -> Fr:
        mu_u, mu_d, mu_e = mu_q + mu_h, mu_q - mu_h, mu_l - mu_h
        ferm = n_f * (6 * y_q * mu_q + 3 * y_u * mu_u + 3 * y_d * mu_d + 2 * y_l * mu_l + y_e * mu_e)
        return ferm + 2 * 2 * y_h * mu_h * n_h            # bosons: twice the fermions' weight
    c0, c1 = charge(Fr(0)), charge(Fr(1)) - charge(Fr(0))
    mu_h = -c0 / c1
    mu_u, mu_d, mu_e = mu_q + mu_h, mu_q - mu_h, mu_l - mu_h
    b = n_f * (2 * mu_q + mu_u + mu_d)                 # 1/3 per quark times 3 colours
    l = n_f * (2 * mu_l + mu_e)
    return {"B_over_BminusL": b / (b - l), "L_over_BminusL": l / (b - l), "mu_H_over_mu_L": mu_h}


def relativistic_dof(extra_majorana: int = 0) -> Dict[str, Fr]:
    """g* of the SM plasma from the field content (and of today's photons + neutrinos, g*s)."""
    gauge = sum(n * n - 1 for n in (2, 3)) + 1
    bos = 2 * gauge + sum(2 * d3 * d2 * copies for _, d3, d2, _, kind, copies in SM_FIELDS if kind == "complex_scalar")
    ferm = sum(2 * d3 * d2 * copies for _, d3, d2, _, kind, copies in SM_FIELDS if kind == "weyl")
    g_star = bos + Fr(7, 8) * (ferm + 2 * extra_majorana)
    n_nu = sum(copies for name, _, _, _, _, copies in SM_FIELDS if name == "L")
    g_s_today = 2 + Fr(7, 8) * 2 * n_nu * Fr(4, 11)
    return {"g_star": g_star, "g_s_today": g_s_today, "bosons": Fr(bos), "fermions": Fr(ferm)}


def leptogenesis_efficiency(k_dec: float) -> Tuple[float, float]:
    """(z_B, kappa_f) for decay parameter K = m~_1 / m_*: z_B solves Buchmuller, Di Bari, Plumacher's
    eq. 59, (K/4) z^3 e^-z (1 + sqrt(pi z / 2)) = z - 1 (bisection, z > 1); kappa_f from their eq. 22
    (thermal initial abundance; scatterings neglected, which gives the largest efficiency)."""
    def g(z: float) -> float:
        return k_dec / 4 * z ** 3 * math.exp(-z) * (1 + math.sqrt(math.pi * z / 2)) - (z - 1)
    lo, hi = 1.0, 2.0
    while g(hi) > 0:
        hi *= 2
    # g(1) > 0 and g < 0 beyond the root: the largest root is where the asymmetry freezes
    for _ in range(int(num("nu_bisections"))):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if g(mid) > 0 else (lo, mid)
    z_b = (lo + hi) / 2
    return z_b, 2 / (k_dec * z_b) * (1 - math.exp(-k_dec * z_b / 2))


def equilibrium_neutrino_mass(v_h: float, m_planck: float, g_star: float) -> float:
    """m_* = 16 pi^(5/2) sqrt(g*) v^2 / (3 sqrt5 M_P) in eV (their eq. 10, v = <H> = 174 GeV)."""
    return 16 * math.pi ** Fr(5, 2) * math.sqrt(g_star) * v_h ** 2 / (3 * math.sqrt(5) * m_planck) * 10 ** 9


def baryon_asymmetry(cosmo: Dict[str, Any], flav: Dict[str, Any], nus: Dict[str, Any],
                     planck: Dict[str, float]) -> Dict[str, Any]:
    x = _float_inputs()
    out: Dict[str, Any] = {}
    # S1. eta_B
    def eta(xx: Dict[str, float]) -> float:
        hbar = xx["h"] / (2 * math.pi)
        n_gamma = 2 * zeta3() / math.pi ** 2 * (xx["k_B"] * xx["T_CMB"] / (hbar * xx["c"])) ** 3
        mpc = xx["au"] * 648000 / math.pi * 10 ** 6
        rho_c100 = 3 * (100 * 1000 / mpc) ** 2 / (8 * math.pi * xx["G"])
        return xx["Omega_b_h2"] * rho_c100 / xx["m_p"] / n_gamma
    out["eta_B"] = eta(x)
    out["eta_B_sigma"] = _propagate(eta, ("Omega_b_h2", "T_CMB", "G"))
    # S2. the Standard Model
    n_f = sum(copies for name, _, _, _, _, copies in SM_FIELDS if name == "L")
    n_h = sum(copies for _, _, _, _, kind, copies in SM_FIELDS if kind == "complex_scalar")
    sph = sphaleron_conversion(n_f, n_h)
    out["sphaleron"] = {"delta_B_per_transition": n_f, "n_f": n_f, "n_h": n_h, **sph}
    lat = LITERATURE["ew_transition"]["value"]
    m_end, m_end_s = (float(v) for v in lat["endpoint_m_h"])
    t_c, t_c_s = (float(v) for v in lat["T_c"])
    mh = _comparison("m_h")[0]
    out["transition"] = {"endpoint_m_h": m_end, "endpoint_sigma": m_end_s, "m_h": mh,
                         "n_sigma_above": (mh - m_end) / m_end_s, "T_c": t_c, "T_c_sigma": t_c_s}
    r0 = flav["ratios"][flav["runner"].mt_msbar]
    ups = [r0[k] for k in ("m_u", "m_c", "m_t")]
    dns = [r0[k] for k in ("m_d", "m_s", "m_b")]
    prod = 1.0
    for ms_ in (ups, dns):
        for i in range(3):
            for j in range(i + 1, 3):
                prod *= ms_[j] ** 2 - ms_[i] ** 2
    j_cp = _comparison("J")[0]
    out["cp_measure"] = {"J": j_cp, "delta_CP": j_cp * prod / t_c ** 12, "T": t_c}
    # S3. leptogenesis
    dof = relativistic_dof(extra_majorana=1)
    f_eta = float(sph["B_over_BminusL"]) * Fr(3, 4) * float(dof["g_s_today"] / dof["g_star"])
    out["leptogenesis"] = {"eta_per_epsilon_kappa": f_eta, "g_star": dof["g_star"], "g_s_today": dof["g_s_today"]}
    v_h = flav["runner"].v / math.sqrt(2)                       # <H> = v / sqrt2
    eps_min = out["eta_B"] / abs(f_eta)
    # the SM bound on the CP asymmetry, |epsilon_1| <= 3 M_1 (m_3 - m_1) / (16 pi <H>^2) (Buchmuller, Di Bari,
    # Plumacher, eq. 31; Davidson-Ibarra's eq. 17 is written for the MSSM, whose asymmetry is twice as large)
    rows = []
    for o, rec in nus["orderings"].items():
        ms_ = rec["masses_at_m0_0"]
        dm = (max(ms_) - min(ms_)) * 10 ** -9                    # GeV
        m1_min = eps_min * 16 * math.pi * v_h ** 2 / (3 * dm)
        rows.append({"ordering": o, "m3_minus_m1_eV": dm * 10 ** 9, "M1_min": m1_min,
                     "window_top": rec["seesaw"]["M_max_perturbative"],
                     "window_open": m1_min < rec["seesaw"]["M_max_perturbative"]})
    out["leptogenesis"]["epsilon_min"] = eps_min
    out["leptogenesis"]["rows"] = rows
    # the efficiency: kappa_f(K), K = m~_1 / m_*, over the natural range m_sol <= m~_1 <= m_atm (NO, m0 = 0)
    g_sm = relativistic_dof()["g_star"]
    m_star = equilibrium_neutrino_mass(v_h, planck["E_P_GeV"], float(g_sm))
    ms_no = nus["orderings"]["NO"]["masses_at_m0_0"]
    m_sol, m_atm_ = ms_no[1], ms_no[2]
    no_min = rows[0]["M1_min"]
    eff = []
    n_k = int(num("nu_m0_points"))
    for k in range(n_k):
        mt_ = m_sol * (m_atm_ / m_sol) ** (k / (n_k - 1))
        z_b, kap_ = leptogenesis_efficiency(mt_ / m_star)
        eff.append({"m_tilde_eV": mt_, "K": mt_ / m_star, "z_B": z_b, "kappa": kap_, "M1_min": no_min / kap_})
    out["leptogenesis"]["m_star_eV"] = m_star
    out["leptogenesis"]["efficiency"] = eff
    out["leptogenesis"]["M1_min_natural"] = (eff[0]["M1_min"], eff[-1]["M1_min"])
    # Davidson-Ibarra's own example: epsilon > 1e-6 needs M_1 > 4e9 GeV (their text, m_3 ~ the atmospheric mass)
    m_atm = nus["orderings"]["NO"]["seesaw"]["m_heaviest_eV"] * 10 ** -9
    out["leptogenesis"]["di_example_M1"] = 10 ** -6 * 8 * math.pi * v_h ** 2 / (3 * m_atm)   # their normalization
    return out


# =============================================================================
# 6r. PART T: SO(10)
# =============================================================================
# SO(10) puts a whole family, with a right-handed neutrino, into one 16. What that fixes:
#   T1. Group theory (exact): the 16's content is Part R's family plus nu^c; gauging B - L is
#       anomaly-free only with nu^c; the GUT normalization of hypercharge, sin^2 theta_W = 3/8 at
#       the unification scale, from traces over the 16.
#   T2. Minimal Yukawas (one 10_H): M_u ~ M_d ~ M_e ~ M_nu^D, so V = 1 and m_c/m_t = m_s/m_b =
#       m_mu/m_tau at M_GUT; tested with Part B's running ratios.
#   T3. t-b-tau unification (one 10_H in the MSSM): y_t = y_b = y_tau at M_GUT, with Part I's scales;
#       tan(beta) scanned; the SUSY threshold to m_b it would need.
#   T4. Non-supersymmetric SO(10) through Pati-Salam SU(4) x SU(2)_L x SU(2)_R at M_I: one-loop
#       running, b_i from the field content (fermions in (4,2,1) + (4bar,1,2), scalars (1,2,2) and
#       (10,1,3)); the three measured couplings fix M_I, M_GUT and alpha_GUT exactly (a linear
#       system), and then proton decay (Part Q) and the seesaw / leptogenesis scale (Parts P, S).
SO10_16 = (("Q", 3, 2), ("u^c", 3, 1), ("d^c", 3, 1), ("L", 1, 2), ("e^c", 1, 1), ("nu^c", 1, 1))
BL_CHARGE = {"Q": Fr(1, 3), "u^c": Fr(-1, 3), "d^c": Fr(-1, 3), "L": Fr(-1), "e^c": Fr(1), "nu^c": Fr(1)}


def bl_anomalies(with_nu_c: bool) -> Dict[str, Fr]:
    fields = [f for f in SO10_16 if with_nu_c or f[0] != "nu^c"]
    return {"SU3^2 (B-L)": sum(BL_CHARGE[n] * d2 for n, d3, d2 in fields if d3 == 3),
            "SU2^2 (B-L)": sum(BL_CHARGE[n] * d3 for n, d3, d2 in fields if d2 == 2),
            "grav^2 (B-L)": sum(BL_CHARGE[n] * d3 * d2 for n, d3, d2 in fields),
            "(B-L)^3": sum(BL_CHARGE[n] ** 3 * d3 * d2 for n, d3, d2 in fields)}


def weinberg_angle_at_unification() -> Dict[str, Fr]:
    """sin^2 theta_W = Tr T3^2 / Tr Q^2 over one 16 (any complete multiplet), and the GUT normalization."""
    hyp = {n: y for n, _, _, y, _, _ in SM_FIELDS}
    hyp["nu^c"] = Fr(0)
    t3sq = Fr(0)
    qsq = Fr(0)
    ysq = Fr(0)
    for n, d3, d2 in SO10_16:
        t3 = [Fr(1, 2), Fr(-1, 2)] if d2 == 2 else [Fr(0)]
        for t in t3:
            q = t + hyp[n]
            t3sq += d3 * t * t
            qsq += d3 * q * q
            ysq += d3 * hyp[n] ** 2
    return {"sin2_theta_W": t3sq / qsq, "GUT_norm": t3sq / ysq}


def _pati_salam_b() -> Dict[str, Fr]:
    """One-loop b for SU(4), SU(2)_L, SU(2)_R: gauge, three families of (4,2,1) + (4bar,1,2) Weyl
    fermions, complex scalars (1,2,2) and (10,1,3)."""
    def t_index(n: int, dim: int) -> Fr:
        return {1: Fr(0), n: Fr(1, 2)}.get(dim, {(4, 10): Fr(3), (4, 15): Fr(4), (2, 3): Fr(2)}.get((n, dim), Fr(0)))
    b = {"4": -Fr(11, 3) * 4, "2L": -Fr(11, 3) * 2, "2R": -Fr(11, 3) * 2}
    n_f = sum(copies for name, _, _, _, _, copies in SM_FIELDS if name == "L")
    reps = [((4, 2, 1), "weyl", n_f), ((4, 1, 2), "weyl", n_f), ((1, 2, 2), "scalar", 1), ((10, 1, 3), "scalar", 1)]
    for (d4, d2l, d2r), kind, copies in reps:
        w_ = Fr(2, 3) if kind == "weyl" else Fr(1, 3)
        b["4"] += w_ * copies * t_index(4, d4) * d2l * d2r
        b["2L"] += w_ * copies * t_index(2, d2l) * d4 * d2r
        b["2R"] += w_ * copies * t_index(2, d2r) * d4 * d2l
    return b


def pati_salam_unification(x: Dict[str, float]) -> Dict[str, Any]:
    """One loop: SM from M_Z to M_I, Pati-Salam from M_I to M_GUT; solve the linear system for
    (t_I = ln M_I/M_Z, D = ln M_GUT/M_I, 1/alpha_GUT)."""
    a, s2 = 1 / x["alpha_em_inv_MZ"], x["s2_hat_Z"]
    inv0 = [float(GUT_NORM) * (1 - s2) / a, s2 / a, 1 / x["alpha_s_MZ"]]     # 1/alpha_1, 1/alpha_2, 1/alpha_3
    bs = [float(b) for b in sm_gauge_b()]
    bp = {k: float(v) for k, v in _pati_salam_b().items()}
    tp = 2 * math.pi
    gn = float(GUT_NORM)
    # 1/alpha_1 = gn / alpha_2R + (1 - gn) / alpha_4 at M_I  ->  1/alpha_2R = (1/alpha_1 - (1 - gn)/alpha_3) / gn
    # unknowns u = (t_I, D, A): rows "value at M_I - b/(2 pi) D - A = 0"
    rows = [  # coefficients of (t_I, D, A) and the constant
        ([-bs[2] / tp, -bp["4"] / tp, -1], inv0[2]),
        ([-bs[1] / tp, -bp["2L"] / tp, -1], inv0[1]),
        ([(-bs[0] / tp - (1 - gn) * (-bs[2] / tp)) / gn, -bp["2R"] / tp, -1], (inv0[0] - (1 - gn) * inv0[2]) / gn),
    ]
    m = [r[0] + [-r[1]] for r in rows]
    for i in range(3):                                          # Gaussian elimination, partial pivoting
        piv = max(range(i, 3), key=lambda r: abs(m[r][i]))
        m[i], m[piv] = m[piv], m[i]
        for r in range(3):
            if r != i:
                f = m[r][i] / m[i][i]
                m[r] = [p - f * q for p, q in zip(m[r], m[i])]
    t_i, d, a_inv = (m[i][3] / m[i][i] for i in range(3))
    m_i = x["M_Z"] * math.exp(t_i)
    return {"b_PS": _pati_salam_b(), "M_I": m_i, "M_GUT": m_i * math.exp(d), "alpha_GUT": 1 / a_inv,
            "consistent": 0 < t_i and d > 0}


# --- T5. Every minimal SO(10) chain at one and two loops. A chain is the gauge group between M_I and
# M_GUT with its fields; its one- and two-loop b come from the field content by the same
# Machacek-Vaughn formulas as the SM's (gauge part). The SM runs at two loops below M_I (gauge part,
# as in Part I). Tree-level matching at M_I and M_GUT: the heavy-field thresholds are unknown.
#   PS     SU(4) x SU(2)_L x SU(2)_R, scalars (1,2,2) + (10,1,3)
#   PS+D   with D-parity: g_L = g_R above M_I; scalars add (10bar,3,1)
#   LR     SU(3) x SU(2)_L x SU(2)_R x U(1)_{B-L}, scalars (1,2,2,0) + (1,1,3,2)
#   LR+D   with D-parity: adds (1,3,1,2); g_L = g_R above M_I
# U(1)_{B-L} is normalized as in SO(10): X = sqrt(3/8) (B - L), so hypercharge matches as
# 1/alpha_1 = (3/5)/alpha_2R + (2/5)/alpha_X. Counting: each chain has exactly as many unknowns
# as conditions (M_I, M_GUT, alpha_GUT, and for LR without D-parity the split of hypercharge
# between SU(2)_R and B - L), so none predicts a coupling; the solution says where the scales are.
BL_NORM = Fr(3, 8)


def _rep_info(group: str, dim: int) -> Tuple[Fr, Fr]:
    """(Dynkin index T, Casimir C2) of an irreducible SU(N) representation, by dimension."""
    n = {"SU4": 4, "SU3": 3, "SU2": 2}[group]
    if dim == 1:
        return Fr(0), Fr(0)
    if dim == n:
        return Fr(1, 2), Fr(n * n - 1, 2 * n)
    if dim == n * n - 1:
        return Fr(n), Fr(n)
    if (n, dim) == (4, 10):                                  # symmetric tensor of SU(4)
        return Fr(n + 2, 2), Fr((n + 2) * (n - 1), n)
    if (n, dim) == (4, 6):                                   # antisymmetric tensor of SU(4)
        return Fr(n - 2, 2), Fr((n - 2) * (n + 1), n)
    raise ValueError(f"representation {dim} of {group} not tabulated")


def chain_b(groups: Sequence[str], fields, u1_norm: Fr = BL_NORM) -> Tuple[List[Fr], List[List[Fr]]]:
    """One- and two-loop gauge b of a product group. fields: (rep, kind, copies); rep lists the
    dimension under each SU(N) and, for the U(1), its charge (squared and normalized by u1_norm)."""
    k = len(groups)
    ca = [Fr(0) if g == "U1" else _rep_info(g, {"SU4": 15, "SU3": 8, "SU2": 3}[g])[1] for g in groups]
    b1 = [-Fr(11, 3) * c for c in ca]
    b2 = [[(-Fr(34, 3) * ca[i] ** 2 if i == j else Fr(0)) for j in range(k)] for i in range(k)]
    for rep, kind, copies in fields:
        dims = [1 if g == "U1" else r for g, r in zip(groups, rep)]
        size = math.prod(dims)
        s_i, c_i = [], []
        for g, r, d in zip(groups, rep, dims):
            t, c = (u1_norm * r * r, u1_norm * r * r) if g == "U1" else _rep_info(g, d)
            s_i.append(t * Fr(size, d))
            c_i.append(c)
        w1 = Fr(2, 3) if kind == "weyl" else Fr(1, 3)
        for i in range(k):
            b1[i] += w1 * copies * s_i[i]
            for j in range(k):
                if kind == "weyl":
                    b2[i][j] += copies * s_i[i] * (2 * c_i[j] + (Fr(10, 3) * ca[i] if i == j else 0))
                else:
                    b2[i][j] += copies * s_i[i] * (4 * c_i[j] + (Fr(2, 3) * ca[i] if i == j else 0))
    return b1, b2


def so10_chains() -> Dict[str, Dict[str, Any]]:
    n_f = sum(copies for name, _, _, _, _, copies in SM_FIELDS if name == "L")
    ps = [((4, 2, 1), "weyl", n_f), ((4, 1, 2), "weyl", n_f), ((1, 2, 2), "scalar", 1), ((10, 1, 3), "scalar", 1)]
    lr = [((3, 2, 1, Fr(1, 3)), "weyl", n_f), ((3, 1, 2, Fr(-1, 3)), "weyl", n_f),
          ((1, 2, 1, Fr(-1)), "weyl", n_f), ((1, 1, 2, Fr(1)), "weyl", n_f),
          ((1, 2, 2, Fr(0)), "scalar", 1), ((1, 1, 3, Fr(2)), "scalar", 1)]
    out = {"PS": {"groups": ("SU4", "SU2", "SU2"), "fields": ps, "D": False},
           "PS+D": {"groups": ("SU4", "SU2", "SU2"), "fields": ps + [((10, 3, 1), "scalar", 1)], "D": True},
           "LR": {"groups": ("SU3", "SU2", "SU2", "U1"), "fields": lr, "D": False},
           "LR+D": {"groups": ("SU3", "SU2", "SU2", "U1"), "fields": lr + [((1, 3, 1, Fr(2)), "scalar", 1)], "D": True}}
    for c in out.values():
        c["b1"], c["b2"] = chain_b(c["groups"], c["fields"])
    return out


def _run_inv(inv: List[float], b1: List[float], b2: List[List[float]], t0: float, t1: float, loops: int) -> List[float]:
    """1/alpha_i from ln mu = t0 to t1 (RK4, the script's unification step)."""
    n = max(1, math.ceil(abs(t1 - t0) / num("unif_step")))
    h = (t1 - t0) / n
    k = len(inv)

    def rhs(v: List[float]) -> List[float]:
        a = [1 / x_ for x_ in v]
        return [-b1[i] / (2 * math.pi) - (sum(b2[i][j] * a[j] for j in range(k)) / (8 * math.pi ** 2) if loops == 2 else 0)
                for i in range(k)]
    for _ in range(n):
        inv = _rk4(rhs, inv, h)
    return inv


def solve_chain(chain: Dict[str, Any], x: Dict[str, float], loops: int,
                shifts: Sequence[float] | None = None) -> Dict[str, Any]:
    """Newton's method on the chain's conditions; unknowns u = (t_I, t_G[, inv_2R(M_I)]) in ln mu.
    shifts: a threshold correction added to each matching condition (in 1/alpha)."""
    a, s2 = 1 / x["alpha_em_inv_MZ"], x["s2_hat_Z"]
    inv0 = [float(GUT_NORM) * (1 - s2) / a, s2 / a, 1 / x["alpha_s_MZ"]]
    sm1 = [float(v) for v in sm_gauge_b()]
    sm2 = [[float(v) for v in r] for r in (sm_two_loop_b() if loops == 2 else [[0] * 3] * 3)]
    b1 = [float(v) for v in chain["b1"]]
    b2 = [[float(v) for v in r] for r in chain["b2"]]
    gn = float(GUT_NORM)
    t_z = math.log(x["M_Z"])
    free_split = chain["groups"][0] == "SU3" and not chain["D"]

    def at_mi(u: List[float]) -> List[float]:
        s = _run_inv(inv0, sm1, sm2, t_z, u[0], loops)
        i1, i2, i3 = s
        if chain["groups"][0] == "SU4":                  # alpha_4 = alpha_3; 2R from hypercharge
            return [i3, i2, (i1 - (1 - gn) * i3) / gn]
        r = u[2] if free_split else i2                    # LR: inv_2R free, or = inv_2L with D-parity
        return [i3, i2, r, (i1 - gn * r) / (1 - gn)]

    def residuals(u: List[float]) -> List[float]:
        start = at_mi(u)
        top = _run_inv(start, b1, b2, u[0], u[1], loops)
        res = [top[0] - top[1]] + [top[i] - top[1] for i in range(2, len(top))]
        if chain["D"] and chain["groups"][0] == "SU4":
            res = [res[0], start[2] - start[1]]           # D-parity: g_R = g_L at M_I (then equal above)
        elif chain["D"]:
            res = [res[0], res[2]]                        # 2R = 2L above M_I automatically
        if shifts:
            res = [r_ + d_ for r_, d_ in zip(res, shifts)]
        return res
    u = [math.log(10 ** 11), math.log(10 ** 16)] + ([inv0[1]] if free_split else [])
    h_ = num("unif_ms_deriv_step")
    for _ in range(int(num("unif_iterations"))):
        f0 = residuals(u)
        if max(abs(v) for v in f0) < num("unif_tol"):
            break
        jac = []
        for k in range(len(u)):
            du = list(u)
            du[k] += h_
            jac.append([(fa - fb) / h_ for fa, fb in zip(residuals(du), f0)])
        # solve J^T rows: jac[k][i] = d res_i / d u_k
        n = len(u)
        m = [[jac[k][i] for k in range(n)] + [-f0[i]] for i in range(n)]
        for i in range(n):
            piv = max(range(i, n), key=lambda r_: abs(m[r_][i]))
            m[i], m[piv] = m[piv], m[i]
            for r_ in range(n):
                if r_ != i:
                    f = m[r_][i] / m[i][i]
                    m[r_] = [p - f * q for p, q in zip(m[r_], m[i])]
        u = [u[i] + m[i][n] / m[i][i] for i in range(n)]
    f0 = residuals(u)
    top = _run_inv(at_mi(u), b1, b2, u[0], u[1], loops)
    return {"M_I": math.exp(u[0]), "M_GUT": math.exp(u[1]), "alpha_GUT": 1 / top[1],
            "residual": max(abs(v) for v in f0), "consistent": t_z < u[0] < u[1]}


def sm_as_chain() -> Tuple[List[Fr], List[List[Fr]]]:
    """The SM's own content through chain_b: must equal sm_gauge_b and sm_two_loop_b (a check)."""
    fields = [((y, d2, d3), "weyl" if kind == "weyl" else "scalar", copies)
              for _, d3, d2, y, kind, copies in SM_FIELDS]
    return chain_b(("U1", "SU2", "SU3"), fields, GUT_NORM)


# --- T6. What lambda(M_I) is. Integrating out the heavy scalar whose vev breaks the chain at M_I
# shifts the SM quartic at tree level (Elias-Miro, Espinosa, Giudice, Lee, Strumia 2012, eq. 5):
#   lambda_SM(M_I) = lambda_H(M_I) - delta_lambda,  delta_lambda = lambda_HS^2 / lambda_S >= 0,
# with the same normalization as Part L (m_h^2 = 2 lambda v^2). delta_lambda is unknown, so
# lambda(M_I) = 0 is not a condition of the theory. What is fixed: below M_I the SM's own lambda
# must stay positive for a stable vacuum, and above it lambda_H = lambda_SM + delta_lambda can stay
# positive. So the threshold can stabilize the vacuum only if M_I lies below the scale mu_0 where the
# SM's lambda (measured m_h, Part L's running) turns negative; lambda(M_I) = 0 is the boundary M_I = mu_0.
def lambda_at_scale(crit: Dict[str, Any], m_h: float, mu: float, overrides: Dict[str, float] | None = None) -> float:
    big_mt, _, full = anchored_state(overrides, m_h, crit.get("smdr"))
    return run_sm(full[:6] + [full[6]], big_mt, mu, 3, int(num("crit_steps_per_efold")))[6]


def instability_scale(crit: Dict[str, Any], m_h: float, overrides: Dict[str, float] | None = None) -> float:
    """mu_0 where lambda turns negative (bisection in ln mu between M_t and M_P), or NaN if it never does."""
    big_mt = inp("M_t") if not overrides or "M_t" not in overrides else overrides["M_t"]
    lo, hi = math.log(big_mt), math.log(crit["planck"]["M_P"])
    if lambda_at_scale(crit, m_h, math.exp(hi), overrides) > 0:
        return math.nan
    for _ in range(int(num("crit_iterations"))):
        mid = (lo + hi) / 2
        if lambda_at_scale(crit, m_h, math.exp(mid), overrides) > 0:
            lo = mid
        else:
            hi = mid
    return math.exp((lo + hi) / 2)


def chain_vacuum(crit: Dict[str, Any], chains: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    mh = _comparison("m_h")[0]
    mu0 = instability_scale(crit, mh)
    s_t = sig("M_t")
    band = [instability_scale(crit, mh, {"M_t": inp("M_t") + k * s_t}) for k in (-1, 1)]
    rows = {}
    for nm, ch in chains.items():
        m_i = ch["loop2"]["M_I"]
        lam = lambda_at_scale(crit, mh, m_i)
        rows[nm] = {"M_I": m_i, "lambda_SM_at_MI": lam, "below_mu0": m_i < mu0,
                    "ln_MI_over_mu0": math.log(m_i / mu0), "stabilizable": lam > 0}
    return {"mu0": mu0, "mu0_band_Mt": sorted(b for b in band if math.isfinite(b)), "rows": rows}


def chain_thresholds(chain: Dict[str, Any], x: Dict[str, float], base: Dict[str, Any], a_l: float,
                     tau_limit: float, mu0: float, m1_nat: float) -> Dict[str, Any]:
    """Every corner of the threshold box |delta_k| <= threshold_band (in 1/alpha, one per matching
    condition), two loops: the ranges of M_I, M_GUT and tau_p, and whether any verdict flips."""
    d_max = num("threshold_band")
    n_cond = 3 if (chain["groups"][0] == "SU3" and not chain["D"]) else 2
    rows = []
    for signs in itertools.product((-1, 0, 1), repeat=n_cond):
        r_ = solve_chain(chain, x, 2, [s_ * d_max for s_ in signs])
        if not r_["consistent"] or r_["residual"] > num("unif_tol") * 100:
            continue
        r_["tau_p_years"] = proton_lifetime(x, r_["M_GUT"], r_["alpha_GUT"], None, a_l)
        rows.append(r_)
    mi = [r_["M_I"] for r_ in rows]
    mg = [r_["M_GUT"] for r_ in rows]
    tau = [r_["tau_p_years"] for r_ in rows]
    base_p = base["tau_p_years"] > tau_limit
    base_v = base["M_I"] < mu0
    base_a = base["M_I"] >= m1_nat
    return {"band": d_max, "corners": len(rows), "M_I": (min(mi), max(mi)), "M_GUT": (min(mg), max(mg)),
            "tau_p": (min(tau), max(tau)),
            "proton_flips": any((t_ > tau_limit) != base_p for t_ in tau),
            "vacuum_flips": any((m_ < mu0) != base_v for m_ in mi),
            "leptogenesis_flips": any((m_ >= m1_nat) != base_a for m_ in mi)}


# --- T8. The heavy spectrum at M_GUT, by group theory. SO(10) -> Pati-Salam without D-parity is broken
# by the D-odd singlet of a 210; the 126 (whose (10bar,1,3) breaks PS at M_I) and the 10 (whose (1,2,2) holds
# the light Higgs) have their other components at M_GUT. Under SU(4) x SU(2)_L x SU(2)_R:
#   210 = (1,1,1) + (15,1,1) + (15,3,1) + (15,1,3) + (6,2,2) + (10,2,2) + (10bar,2,2)
#   126 = (6,1,1) + (10,3,1) + (10bar,1,3) + (15,2,2)            10 = (6,1,1) + (1,2,2)
# The (6,2,2) of the 210 is eaten by the heavy vectors (6,2,2), whose mass defines M_GUT. Each remaining
# heavy multiplet h with mass M_h shifts the couplings at M_GUT by (b_i^h / 2 pi) ln(M_h / M_GUT) (leading
# log; b_i^h its one-loop contribution). The masses come from the unknown scalar potential: each is
# scanned within a factor heavy_mass_spread of M_GUT, the response is linear in the logs, so every
# extreme follows from one solve per multiplet.
SO10_TO_PS = {10: ((6, 1, 1), (1, 2, 2)),
              126: ((6, 1, 1), (10, 3, 1), (10, 1, 3), (15, 2, 2)),
              210: ((1, 1, 1), (15, 1, 1), (15, 3, 1), (15, 1, 3), (6, 2, 2), (10, 2, 2), (10, 2, 2))}
SO10_INDEX = {10: 1, 126: 35, 210: 56}                       # Dynkin indices, the 10 normalized to 1


def so10_decomposition_index(rep: int) -> List[Fr]:
    """Sum of the components' Dynkin indices under SU(4), SU(2)_L, SU(2)_R: each must equal the SO(10)
    index (embedding index 1), a check of the decompositions T8 uses."""
    tot = [Fr(0)] * 3
    for comp in SO10_TO_PS[rep]:
        size = math.prod(comp)
        for i, (g, d) in enumerate(zip(("SU4", "SU2", "SU2"), comp)):
            tot[i] += _rep_info(g, d)[0] * Fr(size, d)        # T(fund) = 1/2 gives T(10 of SO(10)) = 1
    return tot


PS_GUT_HEAVY = (("210: (15,1,1)", (15, 1, 1), "real"), ("210: (15,3,1)", (15, 3, 1), "real"),
                ("210: (15,1,3)", (15, 1, 3), "real"), ("210: (10,2,2) + conj.", (10, 2, 2), "complex"),
                ("126: (6,1,1)", (6, 1, 1), "complex"), ("126: (10,3,1)", (10, 3, 1), "complex"),
                ("126: (15,2,2)", (15, 2, 2), "complex"), ("10: (6,1,1)", (6, 1, 1), "real"))


def heavy_b(rep: Tuple[int, int, int], kind: str) -> List[Fr]:
    """One-loop b of one scalar multiplet under SU(4), SU(2)_L, SU(2)_R (real: 1/6, complex: 1/3 S)."""
    w_ = Fr(1, 6) if kind == "real" else Fr(1, 3)
    size = math.prod(rep)
    return [w_ * _rep_info(g, d)[0] * Fr(size, d) for g, d in zip(("SU4", "SU2", "SU2"), rep)]


def heavy_spectrum_band(chain: Dict[str, Any], x: Dict[str, float], base: Dict[str, Any], a_l: float) -> Dict[str, Any]:
    """d(ln M_I, ln M_GUT, ln tau_p)/d ln(M_h/M_GUT) per multiplet, and the extremes for |ln| <= ln(spread)."""
    spread = math.log(num("heavy_mass_spread"))
    rows = []
    for name, rep, kind in PS_GUT_HEAVY:
        bh = [float(v) for v in heavy_b(rep, kind)]
        delta = [bh_ / (2 * math.pi) for bh_ in bh]              # per unit ln(M_h/M_GUT)
        shifts = [delta[0] - delta[1], delta[2] - delta[1]]       # PS residuals: inv4 - inv2L, inv2R - inv2L
        r_ = solve_chain(chain, x, 2, shifts)
        tau = proton_lifetime(x, r_["M_GUT"], r_["alpha_GUT"], None, a_l)
        rows.append({"multiplet": name, "b": heavy_b(rep, kind),
                     "dlnMI": math.log(r_["M_I"] / base["M_I"]), "dlnMG": math.log(r_["M_GUT"] / base["M_GUT"]),
                     "dlntau": math.log(tau / base["tau_p_years"])})
    ext = {}
    for key in ("dlnMI", "dlnMG", "dlntau"):
        width = spread * sum(abs(r_[key]) for r_ in rows)
        ext[key] = width
    return {"spread": num("heavy_mass_spread"), "rows": rows,
            "M_I": (base["M_I"] * math.exp(-ext["dlnMI"]), base["M_I"] * math.exp(ext["dlnMI"])),
            "M_GUT": (base["M_GUT"] * math.exp(-ext["dlnMG"]), base["M_GUT"] * math.exp(ext["dlnMG"])),
            "tau_p": (base["tau_p_years"] * math.exp(-ext["dlntau"]), base["tau_p_years"] * math.exp(ext["dlntau"]))}


# --- T9. The 210's own potential: the masses T8 left unknown, calculated. The 210 is the antisymmetric
# tensor phi_ijkl of SO(10); its renormalizable potential is built from every invariant: the mass term
# S2 = phi.phi, the cubic C = phi_ijkl phi_klmn phi_mnij, and four quartics Q1 = S2^2,
# Q2 = A_lm A_ml (A_lm = phi_ijkl phi_ijkm), Q3 = B_(kl)(mn) B_(mn)(kl) (B = phi_ijkl phi_ijmn),
# Q4 = phi_ijkl phi_ijmn phi_kmop phi_lnop. With the vev on the Pati-Salam singlet phi_789,10 = v, each
# multiplet's mass is the curvature along one representative direction (SO(10) indices 0-5 for SO(6),
# 6-9 for SO(4)): (15,1,1) phi_0123; (6,2,2) phi_0789 (eaten: must be massless for every coupling, a
# check of the construction); (15,3,1) and (15,1,3) phi_0167 +- phi_0189; (10,2,2) phi_0126. The heavy
# vectors get M_V^2 = g^2 v^2 / 2 (generators normalized to index 1 on the 10), which defines M_GUT.
# The couplings are unknown: they are scanned (seeded) within a perturbative box, and a point counts
# only if the vacuum is a local minimum and the quartic part is positive along a fixed set of random
# directions (a necessary condition for a potential bounded below). Each viable point's masses then go
# into T8's responses: the fraction of viable potentials that passes each test is the calculated answer.
class _UniformStream:
    """Deterministic floats: the 64-bit linear congruential generator of _IntStream, top 53 bits."""

    def __init__(self, seed: int):
        self.s = seed

    def __call__(self) -> float:
        self.s = (self.s * 6364136223846793005 + 1442695040888963407) % (1 << 64)
        return (self.s >> 11) / (1 << 53)

    def uniform(self, lo: float, hi: float) -> float:
        return lo + (hi - lo) * self()

    def gauss(self) -> float:
        """Box-Muller."""
        u1 = self() or 1 / (1 << 53)
        return math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * self())


def _perm_sign(p: Sequence[int]) -> int:
    s_ = 1
    for i in range(len(p)):
        for j in range(i + 1, len(p)):
            if p[i] > p[j]:
                s_ = -s_
    return s_


def _full_tensor(phi: Dict[Tuple[int, ...], float]) -> Dict[Tuple[int, ...], float]:
    out: Dict[Tuple[int, ...], float] = {}
    for key, v in phi.items():
        if v:
            for p in itertools.permutations(range(4)):
                idx = tuple(key[q] for q in p)
                out[idx] = out.get(idx, 0) + _perm_sign(p) * v
    return out


def so10_210_invariants(phi: Dict[Tuple[int, ...], float]) -> Dict[str, float]:
    f = _full_tensor(phi)
    s2 = sum(v * v for v in f.values())
    by3: Dict[Tuple[int, ...], List[Tuple[int, float]]] = {}
    by2: Dict[Tuple[int, ...], List[Tuple[Tuple[int, int], float]]] = {}
    for (i, j, k, l), v in f.items():
        by3.setdefault((i, j, k), []).append((l, v))
        by2.setdefault((i, j), []).append(((k, l), v))
    a: Dict[Tuple[int, int], float] = {}
    for lst in by3.values():
        for l, v in lst:
            for m, w_ in lst:
                a[(l, m)] = a.get((l, m), 0) + v * w_
    b: Dict[Tuple[Tuple[int, int], Tuple[int, int]], float] = {}
    for lst in by2.values():
        for kl, v in lst:
            for mn, w_ in lst:
                b[(kl, mn)] = b.get((kl, mn), 0) + v * w_
    rows: Dict[Tuple[int, int], List[Tuple[Tuple[int, int], float]]] = {}
    g_ = {((i, j), (k, l)): v for (i, j, k, l), v in f.items()}
    for (r, c), v in g_.items():
        rows.setdefault(r, []).append((c, v))
    cub = sum(v * w_ * g_.get((c2, r), 0) for (r, c), v in g_.items() for c2, w_ in rows.get(c, []))
    return {"S2": s2, "C": cub, "Q1": s2 * s2,
            "Q2": sum(v * a.get((m, l), 0) for (l, m), v in a.items()),
            "Q3": sum(v * b.get((mn, kl), 0) for (kl, mn), v in b.items()),
            "Q4": sum(v * b.get(((k, m), (l, n)), 0) for ((k, l), (m, n)), v in b.items())}


PS_SINGLET_210 = (6, 7, 8, 9)
PS_210_DIRECTIONS = {"(1,1,1)": (((6, 7, 8, 9), 1),), "(15,1,1)": (((0, 1, 2, 3), 1),),
                     "(6,2,2)": (((0, 7, 8, 9), 1),),
                     "(15,3,1)": (((0, 1, 6, 7), 1), ((0, 1, 8, 9), 1)),
                     "(15,1,3)": (((0, 1, 6, 7), 1), ((0, 1, 8, 9), -1)),
                     "(10,2,2)": (((0, 1, 2, 6), 1),)}
QUARTICS_210 = ("Q1", "Q2", "Q3", "Q4")


def potential_210_curvatures() -> Dict[str, Dict[str, float]]:
    """Per multiplet, the coefficient of each normalized coupling in m^2 / v^2 at the vacuum:
    V = -mu^2 S2/48 + eta C/24 + sum_a lambda_a Q_a/576, mu^2 fixed by the minimum (the cubic vanishes
    on the singlet). Exact second derivatives of the quartic polynomials from five points."""
    q0 = so10_210_invariants({PS_SINGLET_210: 1})
    norm = {"S2": 48, "C": 24, "Q1": 576, "Q2": 576, "Q3": 576, "Q4": 576}
    out = {}
    for name, d_ in PS_210_DIRECTIONS.items():
        nrm = math.sqrt(sum(c_ * c_ for _, c_ in d_))
        vals = []
        for t in (-2, -1, 0, 1, 2):
            phi = {PS_SINGLET_210: 1}
            for key, c_ in d_:
                phi[key] = phi.get(key, 0) + t * c_ / nrm
            vals.append(so10_210_invariants(phi))
        dd = {k: (-vals[4][k] + 16 * vals[3][k] - 30 * vals[2][k] + 16 * vals[1][k] - vals[0][k]) / 12 for k in vals[0]}
        # the mass term's curvature is 1 per unit; at the minimum mu^2 = 4 sum_a lambda_a Q_a(e)/576
        out[name] = {"eta": dd["C"] / norm["C"]}
        for q in QUARTICS_210:
            out[name][q] = (dd[q] - 4 * q0[q] * dd["S2"] / norm["S2"]) / norm[q]
    return out


# --- T10. The 126's masses from its couplings to <210>. The 126 is the self-dual part (*S = -i S) of a
# complex 5-form S_ijklm. With the 210's vev phi_789,10 = v, its invariants with the 126 are bilinear in S:
# the norm S*S, one cubic phi_ijkl S*_ijmno S_klmno (odd under D-parity) and the quartics
# (phi phi)_kl,mn S*_klopq S_mnopq, phi_ijkl phi_mnop S*_ijmnq S_klopq and A_lm S*_lnopq S_mnopq. Each is a
# Hermitian matrix on the 252 5-forms; on the self-dual subspace the Pati-Salam multiplets are its
# eigenspaces: (6,1,1) and (15,2,2) single basis forms, (10,3,1) and (10bar,1,3) the two combinations
# that the D-odd cubic splits (SU(2)_L-triplet = the self-dual SO(4) 2-form, as for the 210). The chain
# needs (10bar,1,3) light (its vev breaks PS at M_I): that fixes the 126's mass term, and the rest follow:
# m^2(10,3,1) = 2 eta_2 v exactly (only the cubic tells the two apart).
FIVE_SETS = tuple(itertools.combinations(range(10), 5))
FIVE_INDEX = {a_: n_ for n_, a_ in enumerate(FIVE_SETS)}


def _signed(seq: Sequence[int]) -> int:
    """Sign of the permutation that sorts seq; 0 if an index repeats."""
    if len(set(seq)) < len(seq):
        return 0
    return _perm_sign(seq)


def so10_126_mass_matrices() -> Dict[str, Dict[Tuple[int, int], float]]:
    phi = {t: _signed(t) for t in itertools.permutations(PS_SINGLET_210)}
    by2: Dict[Tuple[int, ...], List[Tuple[Tuple[int, ...], float]]] = {}
    by3: Dict[Tuple[int, ...], List[Tuple[int, float]]] = {}
    for t, v in phi.items():
        by2.setdefault(t[:2], []).append((t[2:], v))
        by3.setdefault(t[:3], []).append((t[3], v))
    pp: Dict[Tuple[int, ...], List[Tuple[Tuple[int, ...], float]]] = {}
    acc: Dict[Tuple[Tuple[int, ...], Tuple[int, ...]], float] = {}
    for lst in by2.values():
        for kl, v in lst:
            for mn, w_ in lst:
                acc[(kl, mn)] = acc.get((kl, mn), 0) + v * w_
    for (kl, mn), v in acc.items():
        pp.setdefault(kl, []).append((mn, v))
    a3: Dict[int, Dict[int, float]] = {}
    for lst in by3.values():
        for l, v in lst:
            for m, w_ in lst:
                a3.setdefault(l, {})[m] = a3.get(l, {}).get(m, 0) + v * w_
    mats: Dict[str, Dict[Tuple[int, int], float]] = {k: {} for k in ("norm", "cubic", "D", "E", "F")}

    def add(name: str, a_: Tuple[int, ...], u: Tuple[int, ...], val: float) -> None:
        sb = _signed(u)
        if sb and val:
            key = (FIVE_INDEX[a_], FIVE_INDEX[tuple(sorted(u))])
            mats[name][key] = mats[name].get(key, 0) + val * sb
    for a_ in FIVE_SETS:
        for t in itertools.permutations(a_):
            sa = _signed(t)
            add("norm", a_, t, sa)
            for kl, pv in by2.get(t[:2], []):
                add("cubic", a_, kl + t[2:], pv * sa)
                for op, p2 in by2.get(t[2:4], []):
                    add("E", a_, kl + op + t[4:], pv * p2 * sa)
            for mn, pv in pp.get(t[:2], []):
                add("D", a_, mn + t[2:], pv * sa)
            for m, pv in a3.get(t[0], {}).items():
                add("F", a_, (m,) + t[1:], pv * sa)
    return mats


def _selfdual(a_: Tuple[int, ...]) -> Dict[int, complex]:
    """The self-dual 126 vector built on e_A: (e_A + i sigma e_Ac)/sqrt2 with *e_A = sigma e_Ac."""
    comp = tuple(x_ for x_ in range(10) if x_ not in a_)
    return {FIVE_INDEX[a_]: 1 / math.sqrt(2), FIVE_INDEX[comp]: 1j * _signed(a_ + comp) / math.sqrt(2)}


def _hodge_vec(u: Dict[int, complex]) -> Dict[int, complex]:
    out: Dict[int, complex] = {}
    for n_, z in u.items():
        a_ = FIVE_SETS[n_]
        comp = tuple(x_ for x_ in range(10) if x_ not in a_)
        out[FIVE_INDEX[comp]] = out.get(FIVE_INDEX[comp], 0) + _signed(a_ + comp) * z
    return out


def _bilinear(m: Dict[Tuple[int, int], float], x_: Dict[int, complex], y_: Dict[int, complex]) -> complex:
    return sum(x_[a_].conjugate() * v * y_[b_] for (a_, b_), v in m.items() if a_ in x_ and b_ in y_)


def _combine(x_: Dict[int, complex], y_: Dict[int, complex], s_: int) -> Dict[int, complex]:
    out = {k: v / math.sqrt(2) for k, v in x_.items()}
    for k, v in y_.items():
        out[k] = out.get(k, 0) + s_ * v / math.sqrt(2)
    return out


def so10_126_coefficients() -> Dict[str, Any]:
    """Per PS multiplet of the 126, each invariant's eigenvalue (normalized to the norm), and checks."""
    mats = so10_126_mass_matrices()
    a1, a2 = _selfdual((0, 1, 2, 6, 7)), _selfdual((0, 1, 2, 8, 9))
    reps = {"(6,1,1)": _selfdual((0, 1, 2, 3, 4)), "(15,2,2)": _selfdual((0, 1, 2, 3, 6)),
            "(10,3,1)": _combine(a1, a2, 1), "(10bar,1,3)": _combine(a1, a2, -1)}
    n0 = _bilinear(mats["norm"], reps["(6,1,1)"], reps["(6,1,1)"]).real
    coef = {r_: {k: _bilinear(m, x_, x_).real / n0 for k, m in mats.items()} for r_, x_ in reps.items()}
    # checks: self-duality; the two p = 3 combinations do not mix; D-even invariants equal on them
    sd = max(abs(z + 1j * u[k]) for u in reps.values() for k, z in _hodge_vec(u).items())
    mix = max(abs(_bilinear(m, reps["(10,3,1)"], reps["(10bar,1,3)"])) / n0 for m in mats.values())
    deven = max(abs(coef["(10,3,1)"][k] - coef["(10bar,1,3)"][k]) for k in ("norm", "D", "E", "F"))
    return {"coefficients": coef, "selfdual_dev": sd, "p3_mixing": mix, "d_even_dev": deven}


# --- T11. The 10's couplings. 10 x 10 = 1 + 45 + 54 holds no 210, so there is no cubic H H phi; the one
# quartic that splits the 10 is H_i H_j A_ij with A_ij = phi_iklm phi_jklm (the trace part is universal). At
# the vev A_ij is 6 v^2 on the SO(4) indices and 0 on the SO(6) ones: it splits the doublet (1,2,2) from the
# colour triplet (6,1,1). 10 x 126 holds the 210, so the cubic H_i S_ijklm phi_jklm exists; at the vev it
# picks S_i6789, the 126's own (6,1,1): the two colour triplets mix. The light Higgs needs the (1,2,2) light
# (at M_I, in this chain), which fixes the 10's mass term: the doublet-triplet splitting, a tuning of the
# 10's mass against its coupling to <210> to (M_I / M_GUT)^2.
def so10_10_splitting() -> Dict[Tuple[int, int], float]:
    """A_ij = phi_iklm phi_jklm at the unit Pati-Salam vev (full index sums)."""
    phi = {t: _signed(t) for t in itertools.permutations(PS_SINGLET_210)}
    by3: Dict[Tuple[int, ...], List[Tuple[int, float]]] = {}
    for t, v in phi.items():
        by3.setdefault(t[1:], []).append((t[0], v))
    a_: Dict[Tuple[int, int], float] = {}
    for lst in by3.values():
        for i, v in lst:
            for j, w_ in lst:
                a_[(i, j)] = a_.get((i, j), 0) + v * w_
    return a_


def potential_210_scan(heavy: Dict[str, Any], alpha_gut: float, tau0: float, m_i0: float, tau_limit: float,
                       mu0: float, m1_nat: float) -> Dict[str, Any]:
    curv = potential_210_curvatures()
    rng = _UniformStream(int(num("potential_seed")))
    lam_max, eta_max = num("potential_lambda_max"), num("potential_eta_max")
    # random directions for the bounded-below test (a fixed set; quartic invariants evaluated once)
    keys = list(itertools.combinations(range(10), 4))
    dirs = []
    for _ in range(int(num("potential_directions"))):
        vec = [rng.gauss() for _ in keys]
        nrm = math.sqrt(sum(v * v for v in vec))
        dirs.append(so10_210_invariants({k_: v / nrm for k_, v in zip(keys, vec)}))
    resp = {r_["multiplet"]: r_ for r_ in heavy["rows"]}
    names = {"(15,1,1)": "210: (15,1,1)", "(15,3,1)": "210: (15,3,1)", "(15,1,3)": "210: (15,1,3)",
             "(10,2,2)": "210: (10,2,2) + conj."}
    g2 = 4 * math.pi * alpha_gut
    # the 126: eigenvalues per invariant, normalized to unit largest magnitude; F is universal (absorbed)
    c126 = so10_126_coefficients()["coefficients"]
    scale = {k: max(abs(c126[r_][k]) for r_ in c126) for k in ("cubic", "D", "E")}
    light = "(10bar,1,3)"
    names126 = {"(6,1,1)": "126: (6,1,1)", "(10,3,1)": "126: (10,3,1)", "(15,2,2)": "126: (15,2,2)"}
    a10 = so10_10_splitting()
    a_max = max(abs(v_) for v_ in a10.values())
    split10 = (a10.get((0, 0), 0) - a10.get((6, 6), 0)) / a_max        # m^2(6,1,1) - m^2(1,2,2), per kappa v^2
    pts, pts_all, pts_10, tried = [], [], [], int(num("potential_points"))
    for _ in range(tried):
        lam = {q: rng.uniform(-lam_max, lam_max) for q in QUARTICS_210}
        eta = rng.uniform(-eta_max, eta_max)
        k126 = {"cubic": rng.uniform(-eta_max, eta_max), "D": rng.uniform(-lam_max, lam_max),
                "E": rng.uniform(-lam_max, lam_max)}
        k10, mix10 = rng.uniform(-lam_max, lam_max), rng.uniform(-eta_max, eta_max)
        m2 = {n_: sum(lam[q] * c_[q] for q in QUARTICS_210) + eta * c_["eta"] for n_, c_ in curv.items()}
        if any(m2[n_] <= 0 for n_ in curv if n_ != "(6,2,2)"):
            continue
        if any(sum(lam[q] * d_[q] for q in QUARTICS_210) <= 0 for d_ in dirs):
            continue
        ell = {n_: math.log(math.sqrt(2 * m2[n_] / g2)) for n_ in names}     # ln(M_h / M_V)
        dtau = sum(resp[names[n_]]["dlntau"] * ell[n_] for n_ in names)
        dmi = sum(resp[names[n_]]["dlnMI"] * ell[n_] for n_ in names)
        pts.append({"ell": ell, "tau_p": tau0 * math.exp(dtau), "M_I": m_i0 * math.exp(dmi)})
        # the 126, with its (10bar,1,3) light (the mass term set by that condition), in units of v^2
        m126 = {r_: sum(k126[k] * (c126[r_][k] - c126[light][k]) / scale[k] for k in k126) for r_ in names126}
        if any(v_ <= 0 for v_ in m126.values()):
            continue
        ell2 = dict(ell)
        ell2.update({r_: math.log(math.sqrt(2 * m126[r_] / g2)) for r_ in names126})
        dtau2 = dtau + sum(resp[names126[r_]]["dlntau"] * ell2[r_] for r_ in names126)
        dmi2 = dmi + sum(resp[names126[r_]]["dlnMI"] * ell2[r_] for r_ in names126)
        pts_all.append({"ell": ell2, "tau_p": tau0 * math.exp(dtau2), "M_I": m_i0 * math.exp(dmi2)})
        # the 10: doublet light, so m^2(6,1,1)_10 = kappa_10 * split10 v^2; it mixes (cubic, mix10 v^2) with one
        # real component of the 126's (6,1,1); the other real component keeps m126["(6,1,1)"]
        m_h6, m_s6 = k10 * split10, m126["(6,1,1)"]
        tr_, det_ = m_h6 + m_s6, m_h6 * m_s6 - mix10 ** 2
        if det_ <= 0 or tr_ <= 0:
            continue
        root = math.sqrt(max(tr_ * tr_ / 4 - det_, 0))
        eig = (tr_ / 2 - root, tr_ / 2 + root, m_s6)                   # three real colour-triplet 6's
        r6 = resp["10: (6,1,1)"]                                         # the response of one real 6
        old6 = resp["126: (6,1,1)"]
        ell6 = [math.log(math.sqrt(2 * e_ / g2)) for e_ in eig]
        # replace the 126's (6,1,1) term (two real 6's at m126) by the three eigenstates
        dtau3 = dtau2 - old6["dlntau"] * ell2["(6,1,1)"] + r6["dlntau"] * sum(ell6)
        dmi3 = dmi2 - old6["dlnMI"] * ell2["(6,1,1)"] + r6["dlnMI"] * sum(ell6)
        pts_10.append({"tau_p": tau0 * math.exp(dtau3), "M_I": m_i0 * math.exp(dmi3),
                       "triplet_light": math.sqrt(2 * eig[0] / g2)})
    n_ok = len(pts)

    def frac(cond: Callable[[Dict[str, Any]], bool], sample: List[Dict[str, Any]] | None = None) -> float:
        sample = pts if sample is None else sample
        return sum(1 for p_ in sample if cond(p_)) / len(sample) if sample else math.nan

    def quantiles(key: str, sample: List[Dict[str, Any]] | None = None) -> Tuple[float, float, float]:
        v_ = sorted(p_[key] for p_ in (pts if sample is None else sample))
        return (v_[len(v_) // 6], v_[len(v_) // 2], v_[(5 * len(v_)) // 6]) if v_ else (math.nan,) * 3
    with126 = {"viable": len(pts_all),
               "frac_proton_ok": frac(lambda p_: p_["tau_p"] > tau_limit, pts_all),
               "frac_vacuum_ok": frac(lambda p_: p_["M_I"] < mu0, pts_all),
               "frac_leptogenesis_ok": frac(lambda p_: p_["M_I"] >= m1_nat, pts_all),
               "frac_all": frac(lambda p_: p_["tau_p"] > tau_limit and p_["M_I"] >= m1_nat, pts_all),
               "tau_p_quantiles": quantiles("tau_p", pts_all), "M_I_quantiles": quantiles("M_I", pts_all),
               "coefficients_126": c126}
    with10 = {"viable": len(pts_10), "split_per_kappa": split10, "A_SO6": a10.get((0, 0), 0), "A_SO4": a10.get((6, 6), 0),
              "frac_proton_ok": frac(lambda p_: p_["tau_p"] > tau_limit, pts_10),
              "frac_vacuum_ok": frac(lambda p_: p_["M_I"] < mu0, pts_10),
              "frac_leptogenesis_ok": frac(lambda p_: p_["M_I"] >= m1_nat, pts_10),
              "frac_all": frac(lambda p_: p_["tau_p"] > tau_limit and p_["M_I"] >= m1_nat, pts_10),
              "tau_p_quantiles": quantiles("tau_p", pts_10), "M_I_quantiles": quantiles("M_I", pts_10),
              "triplet_light_quantiles": quantiles("triplet_light", pts_10)}
    return {"curvatures": curv, "tried": tried, "viable": n_ok, "lambda_max": lam_max, "eta_max": eta_max,
            "with_126": with126, "with_10": with10,
            "frac_proton_ok": frac(lambda p_: p_["tau_p"] > tau_limit),
            "frac_vacuum_ok": frac(lambda p_: p_["M_I"] < mu0),
            "frac_leptogenesis_ok": frac(lambda p_: p_["M_I"] >= m1_nat),
            "frac_all": frac(lambda p_: p_["tau_p"] > tau_limit and p_["M_I"] >= m1_nat),
            "tau_p_quantiles": quantiles("tau_p"), "M_I_quantiles": quantiles("M_I"),
            "ell_ranges": {n_: (min(p_["ell"][n_] for p_ in pts), max(p_["ell"][n_] for p_ in pts)) if pts else None
                           for n_ in names}}


def so10(flav: Dict[str, Any], alpha_unif: Dict[str, Any], yukawa: Dict[str, Any], scp: Dict[str, Any],
         bau: Dict[str, Any], pdk: Dict[str, Any], crit: Dict[str, Any]) -> Dict[str, Any]:
    x0 = _float_inputs()
    out: Dict[str, Any] = {}
    # T1
    out["bl_anomalies_with_nu_c"] = bl_anomalies(True)
    out["bl_anomalies_without_nu_c"] = bl_anomalies(False)
    out["weinberg"] = weinberg_angle_at_unification()
    out["weinberg"]["script_GUT_norm"] = GUT_NORM
    # T2. minimal Yukawas at the highest evaluation scale (Part I's M_S): same-type ratios
    mu_top = max(flav["ratios"])
    r = flav["ratios"][mu_top]
    lep = lepton_masses_gev()
    rmt = lep["mu"] / lep["tau"]
    sig_rel = {k: math.hypot(*(sig(n) / inp(n) for n in pair)) for k, pair in
               (("ct", ("m_c", "M_t")), ("sb", ("m_s", "m_b")))}
    out["minimal_10"] = {"scale": mu_top, "m_c/m_t": r["r_ct"], "m_s/m_b": r["r_sb"], "m_mu/m_tau": rmt,
                         "s_over_c": r["r_sb"] / r["r_ct"], "mu_over_s": rmt / r["r_sb"],
                         "n_sigma_s_c": abs(r["r_sb"] / r["r_ct"] - 1) / math.hypot(sig_rel["ct"], sig_rel["sb"]),
                         "n_sigma_mu_s": abs(rmt / r["r_sb"] - 1) / sig_rel["sb"]}
    # T3. t-b-tau in the MSSM: where y_t = y_b at M_GUT (large tan beta), y_b/y_tau there
    rows = [rw for rw in yukawa.get("btau_MSSM", []) if math.isfinite(rw["M_GUT"])]
    tbt = None
    for a_, b_ in zip(rows[:-1], rows[1:]):
        fa, fb = a_["yt_GUT"] - a_["yb_GUT"], b_["yt_GUT"] - b_["yb_GUT"]
        if fa * fb < 0:
            w_ = fa / (fa - fb)
            tb = math.exp(math.log(a_["tan_beta"]) + w_ * (math.log(b_["tan_beta"]) - math.log(a_["tan_beta"])))
            tbt = {"tan_beta": tb, "yb_over_ytau": a_["yb_over_ytau"] + w_ * (b_["yb_over_ytau"] - a_["yb_over_ytau"])}
    if tbt:
        tbt["m_b_threshold_needed"] = 1 / tbt["yb_over_ytau"] - 1
    out["t_b_tau"] = tbt
    # T4. non-SUSY SO(10) through Pati-Salam
    ps = pati_salam_unification(x0)
    runner = flav["runner"]
    a_l = proton_long_distance(runner, x0)
    ps["tau_p_years"] = proton_lifetime(x0, ps["M_GUT"], ps["alpha_GUT"], None, a_l)
    ps["tau_p_limit"] = pdk["limit_e_pi0"]
    ps["tau_p_allowed"] = ps["tau_p_years"] > pdk["limit_e_pi0"]
    lg = bau["leptogenesis"]["rows"]
    ps["M1_min_leptogenesis"] = min(r_["M1_min"] for r_ in lg)
    ps["seesaw_window_top"] = min(r_["window_top"] for r_ in lg)
    ps["M_I_in_leptogenesis_window"] = ps["M1_min_leptogenesis"] < ps["M_I"] < ps["seesaw_window_top"]
    ps["axion_m_a_eV_if_fa_MI"] = scp["axion"]["ma_fa_MeV2"] * 10 ** 3 / ps["M_I"]
    out["pati_salam"] = ps
    # T5. every minimal chain at one and two loops, with its proton lifetime, lambda(M_I) = 0 and windows
    chains = {}
    for name, ch in so10_chains().items():
        rec = {"b1": ch["b1"], "b2": ch["b2"], "D_parity": ch["D"], "groups": ch["groups"]}
        for loops in (1, 2):
            rec[f"loop{loops}"] = solve_chain(ch, x0, loops)
        two = rec["loop2"]
        two["tau_p_years"] = proton_lifetime(x0, two["M_GUT"], two["alpha_GUT"], None, a_l)
        two["tau_p_allowed"] = two["tau_p_years"] > pdk["limit_e_pi0"]
        two["m_h_lambda_MI_zero"] = predict_higgs_mass_nnlo(None, two["M_I"], 3, crit["central"]["m_h"],
                                                             anchor=crit["smdr"])["m_h"]
        two["in_leptogenesis_window"] = ps["M1_min_leptogenesis"] < two["M_I"] < ps["seesaw_window_top"]
        two["axion_m_a_eV_if_fa_MI"] = scp["axion"]["ma_fa_MeV2"] * 10 ** 3 / two["M_I"]
        rec["two_loop_shift_ln_MI"] = math.log(two["M_I"] / rec["loop1"]["M_I"])
        chains[name] = rec
    out["chains"] = chains
    out["vacuum"] = chain_vacuum(crit, chains)
    # T7. how robust each chain's verdicts are against the unknown thresholds
    m1_nat = bau["leptogenesis"]["M1_min_natural"][0]
    defs = so10_chains()
    out["thresholds"] = {nm: chain_thresholds(defs[nm], x0, ch["loop2"], a_l, pdk["limit_e_pi0"],
                                              out["vacuum"]["mu0"], m1_nat) for nm, ch in chains.items()}
    # T8. the Pati-Salam chain's heavy GUT multiplets, one by one
    hs = heavy_spectrum_band(defs["PS"], x0, chains["PS"]["loop2"], a_l)
    base = chains["PS"]["loop2"]
    for r_ in hs["rows"]:
        # the mass ratio M_h/M_GUT at which each verdict flips (linear in the log; None if it never does here)
        def flip(target: float, value: float, slope: float) -> float | None:
            return math.exp(math.log(target / value) / slope) if slope else None
        r_["proton_flip_ratio"] = flip(pdk["limit_e_pi0"], base["tau_p_years"], r_["dlntau"])
        r_["vacuum_flip_ratio"] = flip(out["vacuum"]["mu0"], base["M_I"], r_["dlnMI"])
    out["heavy_spectrum_PS"] = hs
    # T9. the 210's own potential: its four multiplets' masses calculated over the allowed couplings
    out["potential_210"] = potential_210_scan(hs, base["alpha_GUT"], base["tau_p_years"], base["M_I"],
                                              pdk["limit_e_pi0"], out["vacuum"]["mu0"], m1_nat)
    return out


# =============================================================================
# 6t. PART V: DARK MATTER FROM THE AXION
# =============================================================================
# Part A takes the dark-matter density as an input. The axion of Part O, if it exists, is made in the
# early universe by misalignment: the field sits at a random angle theta_i until the Hubble rate drops
# below its temperature-dependent mass, then oscillates and redshifts like matter. Calculated here
# (Di Luzio, Giannotti, Nardi, Visinelli 2020, eqs. 148-169), with every scale from the algorithm:
#   m_a(T) = beta m_a (T_C/T)^gamma above T_C (dilute instanton gas; beta, gamma, T_C quoted);
#   oscillation when 3 H(T_osc) = m_a(T_osc), H = sqrt(8 pi^3 g*/90) T^2 / M_P (M_P from Part H1);
#   n_a(T_osc) = (b/2) m_a(T_osc) f_a^2 <theta_i^2>, then n_a/s is conserved to today
#   (g_S today = 43/11 from Part S, T_0 from T_CMB); m_a f_a from Part O.
# Pre-inflation: theta_i is one unknown angle (scanned). Post-inflation: it averages over the universe,
# <theta_i^2> = 2.15^2 with anharmonic terms (quoted), and the string and domain-wall contribution,
# on which no quantitative agreement exists, is left out. f_a is scanned, and set to each SO(10) chain's
# M_I (where PQ symmetry would break with B - L).
def axion_relic(f_a: float, theta2: float, maf_mev2: float, m_planck: float, g_s0: float, x: Dict[str, float]) -> Dict[str, float]:
    lit = LITERATURE["axion_misalignment"]["value"]
    beta, gamma, t_c = float(lit["beta"]), float(lit["gamma"]), float(lit["T_C_GeV"])
    g_osc, b_ = float(lit["g_star_osc"]), float(lit["b"])
    m_a = maf_mev2 * 10 ** -6 / f_a                                       # GeV
    h_coef = math.sqrt(8 * math.pi ** 3 * g_osc / 90) / m_planck
    t_osc = (beta * m_a * t_c ** gamma / (3 * h_coef)) ** (1 / (2 + gamma))
    m_osc = beta * m_a * (t_c / t_osc) ** gamma
    if t_osc < t_c:                                                       # oscillates after QCD: m_a(T) = m_a
        t_osc = math.sqrt(m_a / (3 * h_coef))
        m_osc = m_a
    n_osc = b_ / 2 * m_osc * f_a ** 2 * theta2
    gev = x["e_charge"] * 10 ** 9
    hbar_c = x["h"] / (2 * math.pi) * x["c"] / gev                        # GeV m
    t_0 = x["k_B"] * x["T_CMB"] / gev
    n_0 = n_osc * g_s0 * t_0 ** 3 / (g_osc * t_osc ** 3)
    mpc = x["au"] * 648000 / math.pi * 10 ** 6
    rho_c100 = 3 * (100 * 1000 / mpc) ** 2 / (8 * math.pi * x["G"]) * x["c"] ** 2 / gev * hbar_c ** 3   # GeV^4
    return {"m_a_eV": m_a * 10 ** 9, "T_osc_GeV": t_osc, "Omega_h2": m_a * n_0 / rho_c100}


def dark_matter(scp: Dict[str, Any], s10: Dict[str, Any], planck: Dict[str, float], bau: Dict[str, Any]) -> Dict[str, Any]:
    x = _float_inputs()
    maf = scp["axion"]["ma_fa_MeV2"]
    m_p = planck["E_P_GeV"]
    g_s0 = float(bau["leptogenesis"]["g_s_today"])
    lit = LITERATURE["axion_misalignment"]["value"]
    th_post = float(lit["theta_post"])
    om_c, om_c_s, _ = _comparison("Omega_c_h2")

    def omega(f_a: float, th2: float) -> float:
        return axion_relic(f_a, th2, maf, m_p, g_s0, x)["Omega_h2"]
    # post-inflation: the f_a (and m_a) for which misalignment alone is all the dark matter
    lo, hi = math.log(10 ** 8), math.log(10 ** 16)
    for _ in range(int(num("nu_bisections"))):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if omega(math.exp(mid), th_post ** 2) < om_c else (lo, mid)
    f_dm = math.exp((lo + hi) / 2)
    post = axion_relic(f_dm, th_post ** 2, maf, m_p, g_s0, x)
    ref = axion_relic(float(lit["eq170_f_a_GeV"]), th_post ** 2, maf, m_p, g_s0, x)
    chains = {}
    for nm, ch in s10["chains"].items():
        m_i = ch["loop2"]["M_I"]
        r_ = axion_relic(m_i, th_post ** 2, maf, m_p, g_s0, x)
        th_need = th_post * math.sqrt(om_c / r_["Omega_h2"])               # pre-inflation, quadratic potential
        chains[nm] = {"f_a": m_i, "m_a_eV": r_["m_a_eV"], "Omega_h2_post": r_["Omega_h2"],
                      "fraction_post": r_["Omega_h2"] / om_c, "theta_i_pre_needed": th_need,
                      "pre_possible": th_need < math.pi}
    return {"Omega_c_h2": om_c, "Omega_c_h2_sigma": om_c_s, "theta_post": th_post,
            "f_a_all_dm_post": f_dm, "m_a_all_dm_post_eV": post["m_a_eV"], "T_osc_GeV": post["T_osc_GeV"],
            "check_eq170": {"f_a": float(lit["eq170_f_a_GeV"]), "Omega_h2": ref["Omega_h2"],
                            "printed": float(lit["eq170_Omega_h2"])},
            "chains": chains}


# =============================================================================
# 6u. PART W: THE W MASS, A TEST OF THE STANDARD MODEL ITSELF
# =============================================================================
# Given G_F, alpha, M_Z and the masses of the top and the Higgs, the SM fixes M_W through its quantum
# corrections. The full two-loop result is quoted in its published parametrization (Awramik, Czakon,
# Freitas, Weiglein 2004, eqs. 6-8: better than 0.5 MeV for 10 GeV <= M_H <= 1 TeV), with
# Delta alpha = Delta alpha_lept (quoted) + Delta alpha_had^(5) (an input). The Higgs mass is the one Part L
# calculates (lambda(M_P) = 0); the measured one is only a comparison here, and moving to it shifts
# M_W by about a MeV (the dependence is logarithmic).
def w_mass(x: Dict[str, float], m_h: float) -> float:
    c = {k: float(v) for k, v in LITERATURE["w_mass_fit"]["value"]["coefficients"].items()}
    ref = {k: float(v) for k, v in LITERATURE["w_mass_fit"]["value"]["reference"].items()}
    d_alpha = float(LITERATURE["w_mass_fit"]["value"]["delta_alpha_lept"]) + x["delta_alpha_had5"]
    dh_ = math.log(m_h / ref["M_H"])
    h2 = (m_h / ref["M_H"]) ** 2
    dt = (x["M_t"] / ref["m_t"]) ** 2 - 1
    dz = x["M_Z"] / ref["M_Z"] - 1
    da = d_alpha / ref["delta_alpha"] - 1
    das = x["alpha_s_MZ"] / ref["alpha_s"] - 1
    return (c["MW0"] - c["c1"] * dh_ - c["c2"] * dh_ ** 2 + c["c3"] * dh_ ** 4 + c["c4"] * (h2 - 1) - c["c5"] * da
            + c["c6"] * dt - c["c7"] * dt ** 2 - c["c8"] * dh_ * dt + c["c9"] * h2 * dt - c["c10"] * das + c["c11"] * dz)


def w_mass_test(crit: Dict[str, Any]) -> Dict[str, Any]:
    x0 = _float_inputs()
    m_h = crit["central"]["m_h"]
    mw = w_mass(x0, m_h)
    names = ("M_t", "alpha_s_MZ", "M_Z", "delta_alpha_had5")
    parts = {n: _propagate(lambda x, n_=n: w_mass(x, m_h), (n,)) for n in names}
    sig_in = math.sqrt(sum(v * v for v in parts.values()))
    sig_mh = abs(w_mass(x0, m_h + crit["sigma_total"]) - w_mass(x0, m_h - crit["sigma_total"])) / 2
    mh_meas = _comparison("m_h")[0]
    shift = w_mass(x0, mh_meas) - mw
    fit_err = float(LITERATURE["w_mass_fit"]["value"]["fit_accuracy"])
    sig_tot = math.sqrt(sig_in ** 2 + sig_mh ** 2 + fit_err ** 2)
    out = {"M_W": mw, "sigma": sig_tot, "sigma_parts": parts, "sigma_m_h": sig_mh, "fit_accuracy": fit_err,
           "m_h_used": m_h, "shift_to_measured_m_h": shift}
    meas = {"PDG 2024 average (the input M_W)": (inp("M_W"), sig("M_W")),
            "PDG 2024 average without CDF": _comparison("M_W_noCDF")[:2],
            "PDG 2024 global-fit prediction": _comparison("M_W_SM_fit")[:2]}
    out["comparisons"] = {k: {"value": v, "sigma": s_, "pull": (v - mw) / math.hypot(s_, sig_tot)}
                          for k, (v, s_) in meas.items()}
    return out


def sin2_eff(x: Dict[str, float], m_h: float) -> float:
    """sin^2 theta_eff^lept, the SM's two-loop fermionic result in its published parametrization
    (Awramik, Czakon, Freitas 2006, eqs. 48-49, table 5, leptons)."""
    lit = LITERATURE["sin2_eff_fit"]["value"]
    d = {k: float(v) for k, v in lit["coefficients"].items()}
    ref = {k: float(v) for k, v in lit["reference"].items()}
    d_alpha = float(LITERATURE["w_mass_fit"]["value"]["delta_alpha_lept"]) + x["delta_alpha_had5"]
    l_h = math.log(m_h / ref["M_H"])
    dh = m_h / ref["M_H"]
    da = d_alpha / ref["delta_alpha"] - 1
    dt = (x["M_t"] / ref["m_t"]) ** 2 - 1
    das = x["alpha_s_MZ"] / ref["alpha_s"] - 1
    dz = x["M_Z"] / ref["M_Z"] - 1
    return (d["s0"] + d["d1"] * l_h + d["d2"] * l_h ** 2 + d["d3"] * l_h ** 4 + d["d4"] * (dh ** 2 - 1)
            + d["d5"] * da + d["d6"] * dt + d["d7"] * dt ** 2 + d["d8"] * dt * (dh - 1) + d["d9"] * das + d["d10"] * dz)


def sin2_eff_test(crit: Dict[str, Any]) -> Dict[str, Any]:
    x0 = _float_inputs()
    m_h = crit["central"]["m_h"]
    s2 = sin2_eff(x0, m_h)
    names = ("M_t", "alpha_s_MZ", "M_Z", "delta_alpha_had5")
    parts = {n: _propagate(lambda x, n_=n: sin2_eff(x, m_h), (n,)) for n in names}
    sig_mh = abs(sin2_eff(x0, m_h + crit["sigma_total"]) - sin2_eff(x0, m_h - crit["sigma_total"])) / 2
    fit_err = float(LITERATURE["sin2_eff_fit"]["value"]["fit_accuracy"])
    sig_tot = math.sqrt(sum(v * v for v in parts.values()) + sig_mh ** 2 + fit_err ** 2)
    out = {"sin2_eff": s2, "sigma": sig_tot, "sigma_parts": parts, "sigma_m_h": sig_mh, "fit_accuracy": fit_err,
           "shift_to_measured_m_h": sin2_eff(x0, _comparison("m_h")[0]) - s2}
    out["comparisons"] = {}
    for k in ("sin2_eff_LEP_SLC", "sin2_eff_colliders"):
        v, s_, _ = _comparison(k)
        out["comparisons"][k] = {"value": v, "sigma": s_, "pull": (v - s2) / math.hypot(s_, sig_tot)}
    return out


# =============================================================================
# 6v. PART X: CLOSING THE LOOP, COSMOLOGY FROM THE PARTICLE PHYSICS
# =============================================================================
# Part A takes Omega_m as an input. With the axion at the surviving chain's M_I (Part V) the matter density
# follows instead: Omega_m h^2 = Omega_b h^2 (measured) + Omega_a h^2 (misalignment) + Omega_nu h^2 (Part P,
# normal-ordering minimum). Flatness then gives Omega_Lambda, and the Friedmann equation the age (Part A's
# float quadrature, the same function as its check). Against Planck's age this tests the closed loop; the
# string and domain-wall yield, the one unknown left, is what must make up any missing dark matter.
def closed_cosmology(cosmo: Dict[str, Any], dm: Dict[str, Any], nus: Dict[str, Any], chain: str) -> Dict[str, Any]:
    h_ = inp("H0") / 100
    om_r = float(cosmo["Omega_r"])
    h0 = float(cosmo["H0_per_s"])
    om_b = inp("Omega_b_h2") / h_ ** 2
    om_nu = nus["orderings"]["NO"]["Omega_nu_h2_at_min"] / h_ ** 2
    om_c_meas = dm["Omega_c_h2"]
    gyr = 31557600 * 10 ** 9

    def age(om_c_h2: float) -> Tuple[float, float, float]:
        om_m = om_b + om_c_h2 / h_ ** 2 + om_nu
        om_l = 1 - om_m - om_r
        t = age_by_float_quadrature(om_r, om_m, om_l, int(num("friedmann_check_steps")),
                                    num("friedmann_check_lna_min")) / h0 / gyr
        return om_m, om_l, t
    a_mis = dm["chains"][chain]["Omega_h2_post"]
    om_m, om_l, t_mis = age(a_mis)
    _, _, t_all = age(om_c_meas)
    t_meas, t_sig, _ = _comparison("age_Gyr")
    return {"chain": chain, "Omega_a_h2": a_mis, "Omega_m": om_m, "Omega_Lambda": om_l, "age_Gyr": t_mis,
            "age_with_all_dm_Gyr": t_all, "age_pull": (t_mis - t_meas) / t_sig,
            "string_fraction_needed": 1 - a_mis / om_c_meas, "Omega_m_input": float(cosmo["Omega_m"])}


def _herm3_eigvals(m: List[List[complex]]) -> List[float]:
    """Eigenvalues (ascending) of a 3x3 Hermitian matrix in closed form (trigonometric solution of the cubic)."""
    a, b, c = m[0][0].real, m[1][1].real, m[2][2].real
    d, e, f = m[0][1], m[1][2], m[0][2]
    q = (a + b + c) / 3
    p1 = abs(d) ** 2 + abs(e) ** 2 + abs(f) ** 2
    p2 = (a - q) ** 2 + (b - q) ** 2 + (c - q) ** 2 + 2 * p1
    if p2 <= 0:
        return [q, q, q]
    p = math.sqrt(p2 / 6)
    # B = (A - q I)/p ; r = det(B)/2
    aa, bb, cc = (a - q) / p, (b - q) / p, (c - q) / p
    dd, ee, ff = d / p, e / p, f / p
    det = (aa * bb * cc + 2 * (dd * ee * ff.conjugate()).real - aa * abs(ee) ** 2 - bb * abs(ff) ** 2 - cc * abs(dd) ** 2)
    r = max(-1.0, min(1.0, det / 2))
    phi = math.acos(r) / 3
    l1 = q + 2 * p * math.cos(phi)
    l3 = q + 2 * p * math.cos(phi + 2 * math.pi / 3)
    return sorted([l3, 3 * q - l1 - l3, l1])


def _herm3_eigvec(m: List[List[complex]], lam: float) -> List[complex]:
    """Unit eigenvector for a simple eigenvalue: the largest cross product of two rows of (A - lam I)."""
    rows = [[m[i][j] - (lam if i == j else 0) for j in range(3)] for i in range(3)]
    best, bn = None, -1.0
    for i, j in ((0, 1), (0, 2), (1, 2)):
        u, w = rows[i], rows[j]
        cr = [u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0]]   # rows . v = 0
        nrm = math.sqrt(sum(abs(z) ** 2 for z in cr))
        if nrm > bn:
            best, bn = cr, nrm
    return [z / bn for z in best]


# =============================================================================
# 6w. PART Y: THE SO(10) YUKAWA SECTOR, CAN IT GIVE THE CHARGED-FERMION MASSES?
# =============================================================================
# With a 10 and a 126 coupling to the fermions, the Yukawa matrices are symmetric and shared by all four
# sectors: M_u = a Y10 + b Y126, M_d = c Y10 + d Y126, M_e = c Y10 - 3 d Y126 (a-d: the light Higgs'
# components). Two tests, at the scale where the relations hold (each chain's M_I):
#   Y1. Pati-Salam selection rule (exact): between M_I and M_GUT SU(4) is unbroken and <210> is a PS singlet,
#       so nothing mixes the 10's bidoublet (1,2,2) (an SU(4) singlet) with the 126's (15,2,2) (an SU(4) 15);
#       T11's contraction H_i S_ijklm phi_jklm indeed reaches only the (6,1,1). The light Higgs then lies in
#       one SU(4) irrep: the 10 alone (M_e = M_d) or the 126 alone (M_e = -3 M_d), for every generation at
#       once. Tested on m_e/m_d, m_mu/m_s, m_tau/m_b at M_I.
#   Y2. Where the doublets can mix (SU(4) broken above M_I), eliminating Y10, Y126 gives the sum rule
#       M_e = c1 M_d + c2 M_u with any complex c1, c2. In the basis where M_u is diagonal,
#       M_d = Psi V diag(m_d e^{2ia}, m_s e^{2ib}, m_b) V^T Psi (with M_u real diagonal the up-quark phases
#       Psi = diag(e^{i psi1}, e^{i psi2}, 1) are physical). Eight unknowns for the three charged-lepton masses:
#       if no point reaches them, the sum rule is excluded whatever the neutrinos do.
def masses_at_scale(flav: Dict[str, Any], mu: float) -> Dict[str, List[float]]:
    """Running masses at mu (GeV): the third generation from the SM Yukawa running (Part J's), the lighter
    from the flavour stage's same-type ratios; leptons with their ratios at M_Z (QED; above it the gauge part
    is common to all three and y_tau^2 is negligible)."""
    mt, st = couplings_at_mt(flav)
    top = run_to(st, mt, mu, "SM")
    v = flav["runner"].v
    r = flav["runner"].ratios_at([mu])[mu]
    m_t, m_b, m_tau = (top[k] * v / math.sqrt(2) for k in (3, 4, 5))
    lep = lepton_masses_gev()
    a0, mz = inp("alpha_em"), inp("M_Z")
    lr = [lepton_running_mass(lep[k], mz, a0) for k in ("e", "mu", "tau")]
    return {"u": [m_t * r["r_ct"] * r["r_uc"], m_t * r["r_ct"], m_t],
            "d": [m_b * r["r_sb"] * r["r_ds"], m_b * r["r_sb"], m_b],
            "e": [m_tau * lr[0] / lr[2], m_tau * lr[1] / lr[2], m_tau]}


def _mm_dag(m: List[List[complex]]) -> List[List[complex]]:
    return [[sum(m[i][k] * m[j][k].conjugate() for k in range(3)) for j in range(3)] for i in range(3)]


def so10_yukawa_tests(flav: Dict[str, Any], s10: Dict[str, Any]) -> Dict[str, Any]:
    """Y1 at the Pati-Salam chain's M_I (where its relations hold); Y2 at the left-right chain's M_GUT (where
    SU(4) breaks and the doublets can mix; SM running stands in for the missing left-right Yukawa running)."""
    out = {"PS": so10_selection_rule(flav, s10["chains"]["PS"]["loop2"]["M_I"]),
           "LR": so10_sum_rule(flav, s10["chains"]["LR"]["loop2"]["M_GUT"])}
    return out


def so10_selection_rule(flav: Dict[str, Any], m_i: float) -> Dict[str, Any]:
    ms = masses_at_scale(flav, m_i)
    # Y1: lepton/down ratios per generation against 1 (10 alone) and 3 (126 alone); errors from the inputs
    rel = {"d": math.hypot(sig("m_d") / inp("m_d"), sig("m_s") / inp("m_s")) / math.sqrt(2),
           "s": sig("m_s") / inp("m_s"), "b": sig("m_b") / inp("m_b")}
    gens = []
    for k, (q, l, e_) in enumerate((("d", "e", rel["d"]), ("s", "mu", rel["s"]), ("b", "tau", rel["b"]))):
        ratio = ms["e"][k] / ms["d"][k]
        s_ = ratio * max(e_, num("yukawa_ratio_theory_rel"))
        gens.append({"pair": f"m_{l}/m_{q}", "ratio": ratio, "sigma": s_,
                     "pull_10": (ratio - 1) / s_, "pull_126": (ratio - 3) / s_})
    worst10 = max(abs(g_["pull_10"]) for g_ in gens)
    worst126 = max(abs(g_["pull_126"]) for g_ in gens)
    return {"scale": m_i, "masses": ms, "generations": gens, "worst_pull_10": worst10, "worst_pull_126": worst126,
            "excluded": min(worst10, worst126) > num("survival_sigma")}


def so10_sum_rule(flav: Dict[str, Any], mu: float) -> Dict[str, Any]:
    ms = masses_at_scale(flav, mu)
    # Y2: the general sum rule on the three charged-lepton masses (seeded multi-start compass search)
    x = _float_inputs()
    v_ckm = ckm_from_wolfenstein(x)
    tol_m = num("yukawa_fit_mass_rel")

    def matrices(u: List[float]) -> Tuple[List[List[complex]], List[List[complex]]]:
        # u = (ln|c1|, arg c1, ln|c2|, arg c2, a, b, psi_1, psi_2): relative steps for couplings of any size.
        # With M_u real diagonal the up-quark phases Psi are physical: M_d = Psi V X D_d X V^T Psi.
        c1, c2 = cmath.rect(math.exp(u[0]), u[1]), cmath.rect(math.exp(u[2]), u[3])
        ph = (cmath.exp(1j * 2 * u[4]), cmath.exp(1j * 2 * u[5]), 1)
        psi = (cmath.exp(1j * u[6]), cmath.exp(1j * u[7]), 1)
        dd = [ms["d"][k] * ph[k] for k in range(3)]
        md = [[psi[i] * psi[j] * sum(v_ckm[i][k] * dd[k] * v_ckm[j][k] for k in range(3)) for j in range(3)]
              for i in range(3)]
        me = [[c1 * md[i][j] + (c2 * ms["u"][i] if i == j else 0) for j in range(3)] for i in range(3)]
        return md, me

    def lepton_masses(u: List[float]) -> List[float]:
        return [math.sqrt(max(e_, 0)) for e_ in _herm3_eigvals(_mm_dag(matrices(u)[1]))]

    def chi2_masses(u: List[float]) -> float:
        return sum(((a_ / b_ - 1) / tol_m) ** 2 for a_, b_ in zip(lepton_masses(u), ms["e"]))

    # the type-II neutrinos: M_nu proportional to M_d - M_e; PMNS from the left eigenvectors
    p_no = nu_params(x, "NO")
    nu_data = {"s12sq": (p_no["s12sq"], sig("nu_s12sq")), "s13sq": (p_no["s13sq"], sig("nu_s13sq_NO")),
               "s23sq": (p_no["s23sq"], sig("nu_s23sq_NO"))}
    r_meas = p_no["dm21"] / p_no["dm3l"]
    r_sig = r_meas * math.hypot(sig("nu_dm21") / p_no["dm21"], sig("nu_dm3l_NO") / p_no["dm3l"])

    def neutrinos(u: List[float]) -> Dict[str, Any]:
        md, me = matrices(u)
        mn = [[md[i][j] - me[i][j] for j in range(3)] for i in range(3)]
        he, hn = _mm_dag(me), _mm_dag(mn)
        ee, en = _herm3_eigvals(he), _herm3_eigvals(hn)
        ue = [_herm3_eigvec(he, e_) for e_ in ee]
        un = [_herm3_eigvec(hn, e_) for e_ in en]
        pm = [[sum(ue[i][k].conjugate() * un[j][k] for k in range(3)) for j in range(3)] for i in range(3)]
        ang = pmns_angles(pm)
        ratio = (en[1] - en[0]) / (en[2] - en[0]) if en[2] > en[0] else math.inf
        return {"angles": ang, "ratio": ratio, "m_nu_rel": [math.sqrt(max(e_, 0) / en[2]) for e_ in en]}

    def chi2_full(u: List[float]) -> float:
        c = chi2_masses(u)
        n_ = neutrinos(u)
        c += sum(((n_["angles"][k] - v_) / s_) ** 2 for k, (v_, s_) in nu_data.items())
        return c + ((n_["ratio"] - r_meas) / r_sig) ** 2

    def compass(u: List[float], step: float, chi2: Callable[[List[float]], float] = chi2_masses) -> Tuple[List[float], float]:
        """Compass search with a hard evaluation budget."""
        best_c, steps, n_ev = chi2(u), [step] * len(u), 0
        while max(steps) > num("yukawa_fit_min_step") and n_ev < int(num("yukawa_fit_evals")):
            moved = False
            for d_ in range(len(u)):
                for sgn in (1, -1):
                    y_ = list(u)
                    y_[d_] += sgn * steps[d_]
                    c_ = chi2(y_)
                    n_ev += 1
                    if c_ < best_c:
                        best_c, u, moved = c_, y_, True
                        break
                if moved:
                    break
            if not moved:
                steps = [s_ / 2 for s_ in steps]
        return u, best_c
    rng = _UniformStream(int(num("potential_seed")) + 1)
    found: List[Tuple[float, List[float]]] = []
    for k_ in range(int(num("yukawa_fit_starts"))):
        if k_ % 2:
            # generic start
            u0 = [math.log(10) * rng.uniform(-1, 3 / 2), rng.uniform(0, 2 * math.pi), math.log(10) * rng.uniform(-6, 0),
                  rng.uniform(0, 2 * math.pi), rng.uniform(0, math.pi), rng.uniform(0, math.pi),
                  rng.uniform(0, 2 * math.pi), rng.uniform(0, 2 * math.pi)]
        else:
            # structured start: |c1| of a Georgi-Jarlskog size for the muon, and c2 m_t cancelling the excess of
            # c1 m_b in the 33 entry (arg c2 opposite to arg c1)
            c1m = rng.uniform(1, 8) * ms["e"][1] / ms["d"][1] / 3
            a1 = rng.uniform(0, 2 * math.pi)
            c2m = abs(c1m * ms["d"][2] - ms["e"][2]) / ms["u"][2] * rng.uniform(1 / 2, 2)
            u0 = [math.log(c1m), a1, math.log(c2m), a1 + math.pi + rng.uniform(-1 / 2, 1 / 2),
                  rng.uniform(0, math.pi), rng.uniform(0, math.pi), rng.uniform(0, 2 * math.pi), rng.uniform(0, 2 * math.pi)]
        u, c = compass(u0, 1 / 2)
        found.append((c, u))
    # iterated local search: kick the best points (every coordinate by up to one unit) and re-minimize
    found.sort(key=lambda t: t[0])
    best = found[0]
    for c0, u0 in found[:int(num("yukawa_fit_polish"))]:
        cur = (c0, u0)
        for _ in range(int(num("yukawa_fit_kicks"))):
            u, c = compass([v_ + rng.uniform(-1, 1) for v_ in cur[1]], 1 / 4)
            if c < cur[0]:
                cur = (c, u)
        if cur[0] < best[0]:
            best = cur
    fit_m = lepton_masses(best[1])
    out = {"scale": mu, "masses": ms, "chi2_min": best[0], "starts": int(num("yukawa_fit_starts")),
           "mass_tolerance": tol_m, "best_masses": fit_m,
           "worst_rel_miss": max(abs(a_ / b_ - 1) for a_, b_ in zip(fit_m, ms["e"])),
           "reaches": best[0] < 1}
    # Y3. add the neutrinos (type II): from the best charged-lepton points, then kicks; 8 unknowns, 7 data
    seeds = [best[1]] + [f_[1] for f_ in found[:int(num("yukawa_nu_seeds"))]]
    full_best, fits = (math.inf, None), []
    for u0 in seeds:
        cur = compass(u0, 1 / 4, chi2_full)
        for _ in range(int(num("yukawa_nu_kicks"))):
            u, c = compass([v_ + rng.uniform(-1, 1) for v_ in cur[0]], 1 / 4, chi2_full)
            if c < cur[1]:
                cur = (u, c)
            if c < 1:
                fits.append(neutrinos(u))
        if cur[1] < full_best[0]:
            full_best = (cur[1], cur[0])
    nb = neutrinos(full_best[1])
    out["type2"] = {"chi2_min": full_best[0], "data_points": 7, "unknowns": 8,
                    "angles": {k: nb["angles"][k] for k in nu_data}, "ratio": nb["ratio"], "ratio_meas": r_meas,
                    "lepton_masses": lepton_masses(full_best[1]),
                    "n_sigma_worst": max([abs(nb["angles"][k] - v_) / s_ for k, (v_, s_) in nu_data.items()]
                                         + [abs(nb["ratio"] - r_meas) / r_sig]),
                    "fits_found": len(fits),
                    "delta_deg_range": ((min(math.degrees(f_["angles"]["delta"]) for f_ in fits),
                                         max(math.degrees(f_["angles"]["delta"]) for f_ in fits)) if fits else None),
                    "m1_over_m3_range": ((min(f_["m_nu_rel"][0] for f_ in fits), max(f_["m_nu_rel"][0] for f_ in fits))
                                         if fits else None)}
    out["type2"]["reaches"] = full_best[0] < num("survival_sigma") ** 2
    # the reason, in one number: large theta_23 from M_d - M_e needs b and tau to converge (m_b ~ m_tau)
    out["type2"]["b_tau_mismatch"] = (ms["d"][2] - ms["e"][2]) / ms["d"][2]
    return out


# =============================================================================
# 6x. PART Z: THE LEDGER, EVERY FREE NUMBER AND WHAT THE ALGORITHM DOES WITH IT
# =============================================================================
# The algorithm closes when every free number of the Standard Model plus cosmology carries a status the
# stages computed, for the one hypothesis that survives every condition (Part U):
#   calculated  fixed by the algorithm with nothing measured spent on it
#   related     tied to other numbers by a relation that is tested
#   traded      exchanged for an unknown of the hypothesis: nothing predicted
#   bounded     only limited by measurements
#   open        no mechanism in the surviving hypothesis
#   input       measured, and used as such
def final_ledger(score: Dict[str, Any], s10: Dict[str, Any], s10y: Dict[str, Any], scp: Dict[str, Any],
                 nus: Dict[str, Any], bau: Dict[str, Any], dm: Dict[str, Any], crit: Dict[str, Any], anom: Dict[str, Any],
                 mf: Dict[str, Any], closed: Dict[str, Any], joint: Dict[str, Any]) -> Dict[str, Any]:
    surv = score["survivors"]
    chain = closed["chain"]
    two = s10["chains"][chain]["loop2"]
    t2 = s10y["LR"]["type2"]
    mh_pull = joint["SM_pulls"]["H"]
    rows = [
        ("hypercharges and electric charge", "5 per family", "calculated",
         "anomaly cancellation plus Yukawas fix them uniquely; charge is quantized (Part R, exact)"),
        ("number of families", "1 integer", "calculated" if anom["331_families_with_af"] == [3] else "open",
         "3-3-1: a multiple of 3, exactly 3 with asymptotic freedom (Part R); not in the SO(10) survivor"),
        ("gauge couplings", "3", "traded",
         f"{chain} chain: the three fix M_I = {two['M_I']:.1e}, M_GUT = {two['M_GUT']:.1e} GeV and alpha_GUT (Part T)"),
        ("weak mixing angle at unification", "1", "calculated", "sin^2 theta_W = 3/8 from the 16 (Part T1, exact)"),
        ("Higgs mass", "1", "open",
         f"lambda(M_P) = 0 misses by {abs(mh_pull):.1f} sigma (Part L); lambda(M_I) = 0 is not required (Part T6)"),
        ("Higgs vacuum value", "1", "input", "from G_F"),
        ("quark masses", "6", "input", "run to every scale (Parts B, L)"),
        ("quark mixing (CKM)", "4", "related",
         "one Hermitian texture predicts |V_td/V_ts| at 2.2 sigma (Part C), but it is not the surviving GUT's structure"),
        ("charged-lepton masses", "3", "traded" if s10y["LR"]["reaches"] else "open",
         "the 10 + 126 sum rule reaches them with 8 unknowns (Part Y2)"),
        ("neutrino masses and mixing", "7-9", "open" if not t2["reaches"] else "related",
         f"type II from the sum rule misses by {t2['n_sigma_worst']:.0f} sigma (Part Y3); type I not tested"),
        ("strong CP angle", "1", "bounded",
         f"|theta-bar| < {scp['bound']['theta_max']:.1e}; an axion at M_I would trade it for f_a (Part O)"),
        ("dark-matter density", "1", "open" if not dm["chains"][chain]["pre_possible"] else "traded",
         f"the axion at the survivor's M_I gives {100 * dm['chains'][chain]['fraction_post']:.1f} % (Part V)"),
        ("baryon asymmetry", "1", "traded",
         f"leptogenesis needs M_1 >= {bau['leptogenesis']['rows'][0]['M1_min']:.0e} GeV (Part S); M_1 is unknown"),
        ("cosmological constant", "1", "open", "Omega_Lambda follows from flatness; rho_Lambda is not calculated"),
        ("Newton's constant", "1", "input", "M_P is calculated from it (Part H1)"),
    ]
    counts: Dict[str, int] = {}
    for r_ in rows:
        counts[r_[2]] = counts.get(r_[2], 0) + 1
    return {"survivors": surv, "chain": chain, "rows": [{"quantity": a_, "count": b_, "status": c_, "how": d_}
                                                         for a_, b_, c_, d_ in rows], "counts": counts}


# =============================================================================
# 6s. PART U: THE SCORECARD, EVERY COMPLETE HYPOTHESIS AGAINST EVERY CONDITION
# =============================================================================
# Part M weighs the high-energy hypotheses against unification, b-tau and the Higgs mass. Parts
# P-T add neutrino masses, proton decay, the baryon asymmetry, the strong CP angle and a third
# hypothesis. Here each complete hypothesis meets every condition, with the verdict each earlier
# stage computed:
#   SM to M_P              nothing new below the Planck mass (neutrinos Dirac)
#   minimal SUSY SU(5)     the MSSM above Part I's M_S, unified at M_GUT (Parts I, J, K, Q)
#   SO(10) via Pati-Salam  the SM up to M_I, SU(4) x SU(2)_L x SU(2)_R up to M_GUT (Part T)
# Each entry is one of: pass, fail (with its sigma or reason), trade (an unknown absorbs the
# condition, so nothing is tested), or open (no mechanism in that hypothesis).
# For the Pati-Salam chain the Higgs condition is lambda(M_I) = 0, Part L's criticality moved to
# the scale where the SM ends: computed with Part L's own running and matching.
def scorecard(joint: Dict[str, Any], higgs: Dict[str, Any], crit: Dict[str, Any], pdk: Dict[str, Any],
              nus: Dict[str, Any], bau: Dict[str, Any], s10: Dict[str, Any], scp: Dict[str, Any],
              dm: Dict[str, Any], s10y: Dict[str, Any]) -> Dict[str, Any]:
    mh, mh_s, _ = _comparison("m_h")
    surv = num("survival_sigma")
    rows: Dict[str, Dict[str, Dict[str, Any]]] = {}

    def entry(status: str, detail: str, sigma: float | None = None) -> Dict[str, Any]:
        return {"status": status, "detail": detail, "sigma": sigma}
    # --- SM up to M_P
    sp = joint["SM_pulls"]
    sm = {"U": entry("fail", "the couplings do not meet", abs(sp["U"])),
          "B": entry("fail", "y_b/y_tau far from 1 where g1 = g2", abs(sp["B"])),
          "H": entry("fail" if abs(sp["H"]) > surv else "pass", "lambda(M_P) = 0 (Part L)", abs(sp["H"])),
          "N": entry("trade", f"Dirac Yukawas up to {max(nus['orderings']['NO']['seesaw']['dirac_yukawa']):.0e}, unexplained"),
          "P": entry("pass", "no grand unification: B is conserved in perturbation theory"),
          "A": entry("fail", "no out-of-equilibrium step, CP violation 14 orders short (Part S)"),
          "T": entry("open", "theta-bar bounded, not explained (Part O)")}
    rows["SM to M_P"] = sm
    # --- minimal SUSY SU(5)
    d5max = max((r["tau_max"] for r in pdk["d5"]), default=math.nan)
    mssm_rows = {tuple(r["conditions"]): r for r in joint["rows"] if r["hypothesis"].startswith("MSSM")}
    all3 = mssm_rows.get(("U", "B", "H"))
    su5 = {"U": entry("trade", "M_S chosen by the measured alpha (Part I)"),
           "B": entry("trade", "tan(beta) chosen by b-tau (Part J)"),
           "H": entry("fail", f"m_h <= {higgs['mh_upper_bound']:.1f} GeV at those scales (Part K)",
                      all3["n_sigma"] if all3 else None),
           "N": entry("trade", "seesaw available, scale unknown"),
           "P": entry("fail", f"p -> nubar K+ at most {d5max:.0e} years against {pdk['limit_K_nu']:.1e} (Part Q)"),
           "A": entry("trade", "leptogenesis possible above M_1 ~ 7e8 GeV; gravitinos not checked"),
           "T": entry("open", "needs an axion or another mechanism")}
    rows["minimal SUSY SU(5)"] = su5
    vac = s10["vacuum"]
    band = vac["mu0_band_Mt"]

    def vacuum_entry(v_: Dict[str, Any], nm: str) -> Dict[str, Any]:
        r_ = v_["rows"][nm]
        if r_["stabilizable"]:
            return entry("pass", f"M_I below mu_0 = {v_['mu0']:.1e} GeV: a scalar threshold can stabilize the vacuum")
        decided = bool(band) and r_["M_I"] > band[-1]
        return entry("open", "metastable between mu_0 and M_I" + ("" if decided else
                     f"; M_I lies inside mu_0's top-mass band ({band[0]:.0e} to {band[-1]:.0e} GeV)"))
    lg_ = bau["leptogenesis"]
    m1_full = min(r_["M1_min"] for r_ in lg_["rows"])
    m1_nat = lg_["M1_min_natural"][0]

    def leptogenesis_entry(m_i: float) -> Dict[str, Any]:
        if m_i < m1_full:
            return entry("fail", f"M_1 <~ M_I = {m_i:.0e} GeV is below even the full-efficiency bound {m1_full:.0e} GeV")
        if m_i < m1_nat:
            return entry("open", f"M_1 <~ M_I = {m_i:.0e} GeV needs weak washout: the natural range needs M_1 >= {m1_nat:.0e} GeV")
        return entry("trade", f"M_1 up to M_I = {m_i:.0e} GeV covers the natural range (M_1 >= {m1_nat:.0e} GeV)")
    def dark_matter_entry(d_: Dict[str, Any]) -> Dict[str, Any]:
        frac = f"axion at f_a = M_I: {100 * d_['fraction_post']:.2g} % of the dark matter by post-inflation misalignment"
        if d_["pre_possible"]:
            return entry("trade", frac + f" (strings add more); pre-inflation theta_i = {d_['theta_i_pre_needed']:.2f}"
                                         " gives all of it")
        return entry("open", frac + ", and no initial angle gives all of it: another candidate is needed")
    yps, ylr = s10y["PS"], s10y["LR"]

    def neutrino_entry(nm: str, y_needed: float) -> Dict[str, Any]:
        t2 = ylr["type2"]
        if nm.startswith("LR") and not t2["reaches"]:
            return entry("open", f"type II from the 10 + 126 sum rule misses the PMNS data by {t2['n_sigma_worst']:.0f} sigma"
                                 f" (b and tau do not converge: (m_b - m_tau)/m_b = {t2['b_tau_mismatch']:+.2f}); type I untested")
        return entry("pass", f"seesaw at M_I with a Dirac Yukawa of {y_needed:.3f} for the heaviest neutrino")

    def fermion_entry(nm: str) -> Dict[str, Any]:
        if nm.startswith("PS"):
            return entry("fail" if yps["excluded"] else "pass",
                         "the light doublet sits in one SU(4) irrep (exact selection rule): M_e = M_d or -3 M_d,"
                         f" missed by at least {min(yps['worst_pull_10'], yps['worst_pull_126']):.0f} sigma (Part Y)",
                         min(yps["worst_pull_10"], yps["worst_pull_126"]))
        return entry("trade" if ylr["reaches"] else "fail",
                     "M_e = c1 M_d + c2 M_u reaches the lepton masses" + ("" if ylr["reaches"] else " only within"
                     f" {100 * ylr['worst_rel_miss']:.0f} %") + " (8 unknowns, 3 masses: predictive only with neutrinos)")
    rows["SM to M_P"]["F"] = entry("trade", "the Yukawa couplings are free parameters")
    rows["minimal SUSY SU(5)"]["F"] = entry("fail", "m_s/m_d = m_mu/m_e (minimal SU(5)) excluded (Part J)")
    rows["SM to M_P"]["D"] = entry("open", "no dark-matter candidate; Omega_c is an input (Part A)")
    rows["minimal SUSY SU(5)"]["D"] = entry("trade", "the lightest superpartner, not calculated here")
    rows["SM to M_P"]["V"] = entry("open", f"metastable: lambda turns negative at {vac['mu0']:.1e} GeV (Part L)")
    rows["minimal SUSY SU(5)"]["V"] = entry("pass", "lambda is fixed positive by supersymmetry above M_S")
    # --- every SO(10) chain at two loops (Part T5)
    m3 = nus["orderings"]["NO"]["seesaw"]["m_heaviest_eV"] * 10 ** -9
    v = crit["state_mt"][1]
    sig_h = math.hypot(crit["sigma_total"], mh_s)
    higgs_rows = {}
    for nm, ch in s10["chains"].items():
        two = ch["loop2"]
        m_i = two["M_I"]
        pull_h = (two["m_h_lambda_MI_zero"] - mh) / sig_h
        higgs_rows[nm] = {"m_h": two["m_h_lambda_MI_zero"], "sigma": sig_h, "pull": pull_h, "M_I": m_i}
        y_needed = math.sqrt(2 * m_i * m3) / v
        rows[f"SO(10) via {nm}"] = {
            "U": entry("pass" if two["consistent"] else "fail",
                       f"M_I = {m_i:.1e}, M_GUT = {two['M_GUT']:.1e} GeV solve the three couplings (no prediction)"),
            "B": entry("open", "no b-tau relation without a Yukawa structure (minimal 10_H excluded, Part T)"),
            "H": entry("fail" if abs(pull_h) > surv else "pass",
                       f"lambda(M_I) = 0 gives m_h = {two['m_h_lambda_MI_zero']:.2f} GeV", abs(pull_h)),
            "N": neutrino_entry(nm, y_needed),
            "P": entry("pass" if two["tau_p_allowed"] else "fail",
                       f"p -> e+ pi0 in {two['tau_p_years']:.0e} years against {pdk['limit_e_pi0']:.1e}"),
            "A": leptogenesis_entry(m_i),
            "T": entry("trade", f"an axion at f_a = M_I would give m_a = {two['axion_m_a_eV_if_fa_MI'] * 10 ** 6:.2g} micro-eV"),
            "V": vacuum_entry(s10["vacuum"], nm),
            "D": dark_matter_entry(dm["chains"][nm]),
            "F": fermion_entry(nm)}
    conditions = {"U": "gauge unification", "B": "b-tau unification", "H": "Higgs mass", "N": "neutrino masses",
                  "P": "proton decay", "A": "baryon asymmetry", "T": "strong CP", "V": "vacuum stability",
                  "D": "dark matter", "F": "fermion masses"}
    verdict = {h: {"fails": [c for c, e in r.items() if e["status"] == "fail"],
                   "trades": [c for c, e in r.items() if e["status"] == "trade"],
                   "passes": [c for c, e in r.items() if e["status"] == "pass"],
                   "open": [c for c, e in r.items() if e["status"] == "open"]} for h, r in rows.items()}
    return {"rows": rows, "conditions": conditions, "verdict": verdict,
            "chain_higgs": higgs_rows,
            "survivors": [h for h, v_ in verdict.items() if not v_["fails"]]}


# =============================================================================
# 7. COSMOLOGY (Decimal arithmetic)
# =============================================================================
def dec_pi() -> Decimal:
    """pi to the current Decimal precision (series from the Python decimal documentation)."""
    with localcontext() as ctx:
        ctx.prec += 2
        three = Decimal(3)
        lasts, t, s, n, na, d, da = 0, three, three, 1, 0, 0, 24
        while s != lasts:
            lasts = s
            n, na = n + na, na + 8
            d, da = d + da, da + 32
            t = (t * n) / d
            s += t
    return +s


def romberg(f: Callable[[Decimal], Decimal], a: Decimal, b: Decimal, max_levels: int,
            rel_tol: Decimal) -> Tuple[Decimal, Decimal, int]:
    prev = [(b - a) * (f(a) + f(b)) / 2]
    err = Decimal(0)
    for k in range(1, max_levels):
        h = (b - a) / (2 ** k)
        s = sum(f(a + (2 * i - 1) * h) for i in range(1, 2 ** (k - 1) + 1))
        row = [prev[0] / 2 + h * s]
        for j in range(1, k + 1):
            row.append(row[j - 1] + (row[j - 1] - prev[j - 1]) / (4 ** j - 1))
        err = abs(row[-1] - prev[-1])
        prev = row
        if err <= rel_tol * abs(row[-1]):
            return row[-1], err, k
    return prev[-1], err, max_levels


def cosmology(x: Dict[str, Decimal], prec: int) -> Dict[str, Any]:
    with localcontext() as ctx:
        ctx.prec = prec
        one, two, three = Decimal(1), Decimal(2), Decimal(3)
        pi = dec_pi()
        c, kb, grav = x["c"], x["k_B"], x["G"]
        hbar = x["h"] / (2 * pi)
        mpc = x["au"] * 648000 / pi * 10 ** 6               # 1 pc = 648000/pi au
        h0 = x["H0"] * 1000 / mpc                            # s^-1
        rho_crit = three * h0 ** 2 / (8 * pi * grav)         # kg/m^3
        u_gamma = pi ** 2 / 15 * (kb * x["T_CMB"]) ** 4 / (hbar * c) ** 3  # J/m^3, Stefan-Boltzmann
        om_g = u_gamma / (rho_crit * c ** 2)
        nu_per_species = Decimal(7) / 8 * (Decimal(4) / 11) ** (Decimal(4) / 3)
        om_r = om_g * (one + x["N_eff"] * nu_per_species)
        om_m = x["Omega_m"]
        om_l = one - om_m - om_r                              # flatness

        # t0 = (1/H0) int_0^1 da / (a E(a)); with a = u^2 the integrand is smooth on [0, 1]
        def integrand(u: Decimal) -> Decimal:
            return u ** 3 / (om_r + om_m * u ** 2 + om_l * u ** 8).sqrt()

        integral, err, levels = romberg(integrand, Decimal(0), one, int(NUMERICS["romberg_max_levels"]),
                                        Decimal(NUMERICS["romberg_rel_tol"]))
        t0_s = two * integral / h0
        gyr_s = Decimal(31557600) * 10 ** 9                   # Julian year = 365.25 x 86400 s
        t0_gyr = t0_s / gyr_s

        q0 = om_r + om_m / 2 - om_l
        # q(z) = 0  <=>  2 om_r y^4 + om_m y^3 - 2 om_l = 0 with y = 1 + z (monotonic for y > 0)
        lo, hi = one, two
        while 2 * om_r * hi ** 4 + om_m * hi ** 3 - 2 * om_l < 0:
            hi *= 2
        for _ in range(4 * prec):  # each halving gains log10(2) of a digit
            mid = (lo + hi) / 2
            if 2 * om_r * mid ** 4 + om_m * mid ** 3 - 2 * om_l < 0:
                lo = mid
            else:
                hi = mid
        z_acc = (lo + hi) / 2 - one
        z_eq = om_m / om_r - one
        a_ml = (om_m / om_l) ** (one / three)
        s_h0 = pi * c ** 5 / (grav * hbar * h0 ** 2)          # Hubble-horizon entropy today, units of k_B
        s_ds = s_h0 / om_l                                    # de Sitter limit, H -> H0 sqrt(Omega_Lambda)
        return {
            "Omega_gamma": om_g, "Omega_r": om_r, "Omega_m": om_m, "Omega_Lambda": om_l,
            "age_Gyr": t0_gyr, "age_integral": integral, "romberg_error": err, "romberg_levels": levels,
            "q0": q0, "z_acc": z_acc, "z_eq": z_eq, "a_matter_Lambda": a_ml,
            "S_Hubble_today_kB": s_h0, "S_deSitter_kB": s_ds, "H0_per_s": h0,
        }


def age_by_float_quadrature(om_r: float, om_m: float, om_l: float, steps: int, lna_min: float) -> float:
    """Independent check: H0 t0 = int d(ln a) / E(a), composite Simpson in ln a (floats)."""
    def f(lna: float) -> float:
        a = math.exp(lna)
        return 1 / math.sqrt(om_r / a ** 4 + om_m / a ** 3 + om_l)
    n = steps + steps % 2
    h = -lna_min / n
    total = f(lna_min) + f(0.0)
    for i in range(1, n):
        total += (4 if i % 2 else 2) * f(lna_min + i * h)
    return total * h / 3


# =============================================================================
# 8. THE SIMULATION
# =============================================================================
def _float_inputs(overrides: Dict[str, float] | None = None) -> Dict[str, float]:
    x = _InputView({k: float(_TRACE["set"].get(k, INPUTS[k]["value"])) for k in INPUTS})
    if overrides:
        x.update(overrides)
    return x


def _comparison(name: str) -> Tuple[float, float, float]:
    v, up, dn = COMPARISONS[name]["value"]
    return float(v), float(up), float(dn)


def _tension(lo: float, hi: float, s_lo: float, s_hi: float, name: str) -> Dict[str, Any]:
    meas, up, dn = _comparison(name)
    if lo <= meas <= hi:
        return {"inside": True, "n_sigma": 0.0}
    if meas < lo:
        n = (lo - meas) / math.hypot(s_lo, up)
    else:
        n = (meas - hi) / math.hypot(s_hi, dn)
    return {"inside": False, "n_sigma": n}


def run_flavour(scales: Sequence[float], steps: int, grid: int) -> Dict[str, Any]:
    min_step = num("pattern_search_min_step")
    central = FlavourRunner(_float_inputs(), steps)
    ratios = central.ratios_at(scales)

    # input variations for uncertainty propagation (+/- 1 sigma, central differences)
    varied = {}
    for name in FLAVOUR_UNCERTAIN:
        varied[name] = tuple(FlavourRunner(_float_inputs({name: inp(name) + s * sig(name)}), steps)
                             .ratios_at(scales) for s in (1, -1))

    results = {}
    for mu in sorted(scales):
        r = ratios[mu]
        tex = texture_at(r)
        bands = phase_bands(tex["coef"], grid, min_step)
        tex_var = {name: tuple(texture_at(v[mu]) for v in pair) for name, pair in varied.items()}
        for k, band in bands.items():
            for edge in ("lo", "hi"):
                s, t = band[edge + "_phases"]
                var2 = 0.0
                for name in FLAVOUR_UNCERTAIN:
                    fp = ckm_observables(ckm_matrix(tex_var[name][0]["coef"], s, t))[k]
                    fm = ckm_observables(ckm_matrix(tex_var[name][1]["coef"], s, t))[k]
                    var2 += ((fp - fm) / 2) ** 2
                band["sigma_" + edge] = math.sqrt(var2)
            band["vs_measurement"] = _tension(band["lo"], band["hi"], band["sigma_lo"], band["sigma_hi"], k)
        results[mu] = {"ratios": r, "texture": tex, "bands": bands}
    return {"runner": central, "ratios": ratios, "scales": results, "varied": varied}


def run_survey(flav: Dict[str, Any], scales: Sequence[float]) -> Dict[float, Dict[str, Any]]:
    out = {}
    for mu in scales:
        varied = [(flav["varied"][name][0][mu], flav["varied"][name][1][mu]) for name in FLAVOUR_UNCERTAIN]
        sv = TextureSurvey(flav["ratios"][mu], varied)
        out[mu] = sv.run(int(num("survey_min_zeros")))
        out[mu]["survey"] = sv
    return out


def _derived_vub_over_vcb() -> None:
    """The measured |V_ub/V_cb|, formed from the two PDG fit values (correlation neglected)."""
    vub, ub_up, ub_dn = _comparison("V_ub")
    vcb, cb_up, cb_dn = _comparison("V_cb")
    ratio = vub / vcb
    up = ratio * math.hypot(ub_up / vub, cb_dn / vcb)
    dn = ratio * math.hypot(ub_dn / vub, cb_up / vcb)
    COMPARISONS["V_ub/V_cb"] = {"value": (repr(ratio), repr(up), repr(dn)),
                                "source": "ratio of the PDG 2024 fit values of |V_ub| and |V_cb|"}


def run_cosmology(prec: int) -> Dict[str, Any]:
    base = _InputView({k: Decimal(_TRACE["set"].get(k, INPUTS[k]["value"])) for k in INPUTS})
    out = cosmology(base, prec)
    var2 = 0.0
    var2_ol = 0.0
    for name in COSMO_UNCERTAIN:
        vals = []
        for s in (1, -1):
            x = _InputView(base)
            x[name] = base[name] + s * sig_decimal(name)
            vals.append(cosmology(x, prec))
        var2 += (float(vals[0]["age_Gyr"] - vals[1]["age_Gyr"]) / 2) ** 2
        var2_ol += (float(vals[0]["Omega_Lambda"] - vals[1]["Omega_Lambda"]) / 2) ** 2
    out["age_sigma_uncorrelated_Gyr"] = math.sqrt(var2)
    out["Omega_Lambda_sigma"] = math.sqrt(var2_ol)
    out["age_float_check_Gyr"] = (age_by_float_quadrature(float(out["Omega_r"]), float(out["Omega_m"]),
                                                          float(out["Omega_Lambda"]),
                                                          int(NUMERICS["friedmann_check_steps"]),
                                                          float(NUMERICS["friedmann_check_lna_min"]))
                                  / float(out["H0_per_s"]) / (31557600 * 10 ** 9))
    return out


# =============================================================================
# 9. SELF-CHECKS (correctness of the calculation, never agreement with data)
# =============================================================================
def self_checks(flav: Dict[str, Any], cosmo: Dict[str, Any], scales: Sequence[float], steps: int,
                grid: int, survey: Dict[float, Dict[str, Any]], yuk: Dict[int, Dict[str, Any]]
                ) -> List[Tuple[str, bool, str]]:
    tol = num("check_rel_tol")
    checks: List[Tuple[str, bool, str]] = []

    def add(name: str, ok: bool, detail: str) -> None:
        checks.append((name, bool(ok), detail))

    b0, b1 = qcd_beta(5)
    add("QCD beta coefficients from Casimirs: b0(nf=5) = 23/3, b1(nf=5) = 116/3",
        b0 == Fr(23, 3) and b1 == Fr(116, 3), f"b0 = {b0}, b1 = {b1}")
    g0, g1 = qcd_gamma_m(5)
    add("Quark-mass anomalous dimension: g0 = 4, g1(nf=5) = 202/3 - 100/9",
        g0 == 4 and g1 == Fr(202, 3) - Fr(100, 9), f"g0 = {g0}, g1 = {g1}")
    bsm = sm_gauge_b()
    add("SM gauge b_i from field content = (41/10, -19/6, -7)",
        bsm == (Fr(41, 10), Fr(-19, 6), Fr(-7)), f"b = {tuple(str(b) for b in bsm)}")
    add("SM b_3 equals -b0(nf=6) of the QCD formula", bsm[2] == -qcd_beta(6)[0], "")
    cy = top_yukawa_gauge_coeffs()
    add("Top-Yukawa gauge coefficients from Casimirs = (17/20, 9/4, 8)",
        cy == (Fr(17, 20), Fr(9, 4), Fr(8)), f"c = {tuple(str(c) for c in cy)}")
    n_direct = 1000
    z3_direct = sum(1 / n ** 3 for n in range(1, n_direct + 1)) + 1 / (2 * n_direct ** 2) - 1 / (2 * n_direct ** 3)
    add("zeta(3): fast series agrees with the direct sum plus Euler-Maclaurin tail",
        abs(zeta3() / z3_direct - 1) < tol, f"zeta(3) = {zeta3():.15f}")

    # texture: uniqueness, eigenvalues, unitarity, CP symmetry of the J band
    worst_eig = 0.0
    worst_unit = 0.0
    worst_jsym = 0.0
    for mu in scales:
        r = flav["ratios"][mu]
        tex = flav["scales"][mu]["texture"]
        for sector, (x1, x2) in (("up", (r["r_uc"] * r["r_ct"], r["r_ct"])),
                                 ("down", (r["r_ds"] * r["r_sb"], r["r_sb"]))):
            ev = [abs(e) for e in tex[sector]["eigenvalues"]]
            for got, want in zip(ev, (x1, x2, 1.0)):
                worst_eig = max(worst_eig, abs(got / want - 1))
        for s, t in ((1, 2), (2, 4), (5, 1)):  # sample phases in radians
            v = ckm_matrix(tex["coef"], s, t)
            for i in range(3):
                for j in range(3):
                    dot = sum(v[i][k] * v[j][k].conjugate() for k in range(3))
                    worst_unit = max(worst_unit, abs(dot - (1 if i == j else 0)))
        jb = flav["scales"][mu]["bands"]["J"]
        worst_jsym = max(worst_jsym, abs(jb["hi"] + jb["lo"]) / jb["hi"])
    add("Fritzsch texture: exactly one real sign assignment, (+, -, +) in both sectors",
        all(flav["scales"][mu]["texture"][s]["signs"] == (1, -1, 1) for mu in scales for s in ("up", "down")),
        "")
    add("Texture eigenvalues reproduce the RG mass ratios", worst_eig < tol, f"max rel err {worst_eig:.1e}")
    add("CKM matrix is unitary", worst_unit < tol, f"max |V V^dag - 1| = {worst_unit:.1e}")
    add("J band is symmetric (J_min = -J_max, CP conjugate phases)", worst_jsym < tol,
        f"max rel asym {worst_jsym:.1e}")

    # RG: doubling the step count does not move the ratios
    fine = FlavourRunner(_float_inputs(), 2 * steps).ratios_at(scales)
    worst_rg = max(abs(fine[mu][k] / flav["ratios"][mu][k] - 1)
                   for mu in scales for k in ("r_uc", "r_ct", "r_ds", "r_sb"))
    add("RG running converged (step count doubled)", worst_rg < num("check_rg_tol"),
        f"max rel change {worst_rg:.1e}")

    # phase scan: a finer coarse grid finds the same band edges
    mu = max(scales)
    fine_b = phase_bands(flav["scales"][mu]["texture"]["coef"], grid + grid // 2 + 1,
                         num("pattern_search_min_step"))
    worst_band = max(abs(fine_b[k][e] / flav["scales"][mu]["bands"][k][e] - 1)
                     for k in OBSERVABLES for e in ("lo", "hi"))
    add("Phase-band edges independent of the scan grid", worst_band < tol, f"max rel change {worst_band:.1e}")

    # cosmology
    add("Romberg quadrature of the age converged", cosmo["romberg_error"] <=
        Decimal(NUMERICS["romberg_rel_tol"]) * cosmo["age_integral"],
        f"{cosmo['romberg_levels']} levels, error {float(cosmo['romberg_error']):.1e}")
    rel = abs(cosmo["age_float_check_Gyr"] / float(cosmo["age_Gyr"]) - 1)
    add("Age agrees with an independent float quadrature in ln a", rel < num("check_age_tol"),
        f"rel diff {rel:.1e}")
    total = cosmo["Omega_r"] + cosmo["Omega_m"] + cosmo["Omega_Lambda"]
    add("Flatness holds exactly", total == 1, "")

    # texture survey
    fz = ((0, 0), (1, 1), (0, 2))                       # Fritzsch: zeros at 11, 22, 13
    nz = [p for p in POSITIONS if p not in fz]
    worst_f = 0.0
    for mu in scales:
        sv = survey[mu]["survey"]
        pair = (nz, ((1, -1), "fixed", 0), nz, ((1, -1), "fixed", 0))
        lo, hi = _magnitude_band(sv.coef(pair, 0), _ELEMENTS["V_cb"])
        pb = flav["scales"][mu]["bands"]["V_cb"]
        worst_f = max(worst_f, abs(lo / pb["lo"] - 1), abs(hi / pb["hi"] - 1))
    add("Survey reproduces Part B for the Fritzsch pattern (exact |V_cb| band vs phase scan)",
        worst_f < tol, f"max rel diff {worst_f:.1e}")
    worst_e = 0.0
    for mu in scales:
        sv = survey[mu]["survey"]
        for (sector, nonzero, var, ei, t_unit), o in sv.cache.items():
            if o is None or ei != 0:
                continue
            m = _sector_matrix(list(nonzero), var, sv.E[0][sector], t_unit)
            ev = sorted(abs(x) for x in jacobi_eigh(m, num("jacobi_tol"))[0])
            for got, want in zip(ev, sv.E[0][sector]):
                worst_e = max(worst_e, abs(got / want - 1))
    add("Every survey mass matrix has the RG-run masses as eigenvalues", worst_e < num("check_survey_eig_tol"),
        f"max rel err {worst_e:.1e}")
    mu = max(scales)
    sv = survey[mu]["survey"]
    worst_g = 0.0
    for rec in survey[mu]["classes"]:
        if rec.get("pair") is None:
            continue
        c2, _ = sv.joint(rec["pair"], rec["n_curve"], 2 * int(num("survey_curve_grid")),
                         2 * int(num("survey_phase_grid")))
        worst_g = max(worst_g, abs(c2 - rec["chi2"]) / max(1, rec["chi2"]))
    add("Joint-test chi^2 independent of the starting grids (both doubled)", worst_g < num("check_survey_tol"),
        f"max rel change {worst_g:.1e}")

    # 3-3-1 charges
    ok_charges = True
    ok_anomaly = True
    for b, y in yuk.items():
        for q in y["quarks"].values():
            want = {"u": Fr(2, 3), "d": Fr(-1, 3)}
            ok_charges &= all(q["charges"][k] == want[c] for k, c in enumerate(q["content"]) if c in want)
        # [SU(3)_C]^2 U(1)_X: left-handed colour triplets minus conjugate singlets, X-weighted
        x_left = sum(3 * q["X"] for q in y["quarks"].values())
        x_conj = sum(-q["charges"][k] for q in y["quarks"].values() for k in range(3))
        ok_anomaly &= x_left + x_conj == 0
        # [SU(3)_L]^3: N_c x (antitriplet families) = N_c x (triplet families) + 3 lepton triplets
        n3 = sum(1 for q in y["quarks"].values() if q["rep"] == "3")
        nb = sum(1 for q in y["quarks"].values() if q["rep"] == "3bar")
        ok_anomaly &= 3 * nb == 3 * n3 + 3
    add("3-3-1 charges: ordinary components come out as 2/3 and -1/3 (beta = +-1/sqrt3)", ok_charges, "")
    add("3-3-1 anomalies cancel: [SU(3)_L]^3 and [SU(3)_C]^2 U(1)_X", ok_anomaly, "")
    return checks


# =============================================================================
# 10. REPORT
# =============================================================================
def _fmt(x: float, nd: int = 5) -> str:
    if x == 0:
        return "0"
    if abs(x) < float(NUMERICS["report_sci_below"]) or abs(x) >= float(NUMERICS["report_sci_above"]):
        return f"{x:.{nd - 1}e}"
    return f"{x:.{nd}g}"


def run(scales: Sequence[float] | None = None, prec: int | None = None, certify: bool = False) -> Dict[str, Any]:
    prec = int(prec or NUMERICS["precision_digits"])
    steps = int(NUMERICS["rg_steps_per_efold"])
    grid = int(NUMERICS["phase_grid"])
    _derived_vub_over_vcb()
    _TRACE.update(stage=None, inputs={}, uses={}, keys={})
    cosmo = _stage("cosmology", lambda: run_cosmology(prec))
    alpha_unif = _stage("gauge_unification", alpha_from_unification)   # Part I first: it supplies M_S
    alpha_num = _stage("alpha_numerology", alpha_numerology)

    def flavour() -> Dict[str, Any]:
        sc = scales
        if not sc:
            m_s = alpha_unif.get("M_S_for_measured_alpha", {}).get("M_S_GeV")
            sc = [FlavourRunner(_float_inputs(), steps).mt_msbar] + ([m_s] if m_s else [])
        sc = sorted(float(v) for v in sc)
        out = run_flavour(sc, steps, grid)
        out["evaluation_scales"] = sc
        return out
    flav = _stage("flavour", flavour)
    scales = dict.__getitem__(flav, "evaluation_scales")
    survey = _stage("texture_survey", lambda: run_survey(flav, scales))
    certs = _stage("survey_certificates", lambda: certify_survey(survey[scales[0]])) if certify else None
    yuk = _stage("gauge_331", lambda: {b: yukawa_structure_331(b) for b in (-1, 1)})

    def survivors() -> List[Tuple[Any, Any]]:
        return [(r["zeros_u"], r["zeros_d"]) for r in survey[scales[0]]["classes"]
                if r["status"] == "tested" and all(
                    next(x for x in survey[mu]["classes"]
                         if (x["zeros_u"], x["zeros_d"]) == (r["zeros_u"], r["zeros_d"]))["survives"]
                    for mu in scales)]
    symm = _stage("flavour_symmetry_331", lambda: symmetry_search(yuk, survivors()))
    closure = _stage("general_texture_closure", general_texture_closure)
    planck = _stage("planck_units", planck_units)
    qg = _stage("quantum_gravity", lambda: quantum_gravity(cosmo, flav, planck))
    yukawa = _stage("yukawa_relations", lambda: yukawa_relations(
        flav, alpha_unif.get("M_S_for_measured_alpha", {}).get("M_S_GeV"),
        alpha_unif.get("M_S_for_measured_alpha", {}).get("M_GUT_GeV"), planck["E_P_GeV"]))
    higgs = _stage("higgs_mssm", lambda: higgs_mass_mssm(flav, alpha_unif, yukawa))
    crit = _stage("criticality", lambda: sm_criticality(planck["E_P_GeV"]))
    joint = _stage("uv_joint_test", lambda: uv_joint_test(flav, alpha_unif, yukawa, crit))
    masses = _stage("mass_formulas", lambda: mass_formulas(flav))
    scp = _stage("strong_cp", lambda: strong_cp(flav, survey, scales, alpha_unif, planck))
    nus = _stage("neutrinos", lambda: neutrinos(cosmo, flav, alpha_unif, planck))
    pdk = _stage("proton_decay", lambda: proton_decay(flav, alpha_unif, yukawa))
    anom = _stage("anomalies", lambda: anomaly_constraints(yuk))
    bau = _stage("baryon_asymmetry", lambda: baryon_asymmetry(cosmo, flav, nus, planck))
    s10 = _stage("so10", lambda: so10(flav, alpha_unif, yukawa, scp, bau, pdk, crit))
    dm = _stage("dark_matter", lambda: dark_matter(scp, s10, planck, bau))
    s10y = _stage("so10_yukawa", lambda: so10_yukawa_tests(flav, s10))
    mw = _stage("w_mass", lambda: {**w_mass_test(crit), "z_pole": sin2_eff_test(crit)})
    score = _stage("scorecard", lambda: scorecard(joint, higgs, crit, pdk, nus, bau, s10, scp, dm, s10y))

    def survivor_chain() -> str:
        chains = [h.replace("SO(10) via ", "") for h in score["survivors"] if h.startswith("SO(10) via ")]
        return chains[0] if chains else "PS"
    closed = _stage("closed_cosmology", lambda: closed_cosmology(cosmo, dm, nus, survivor_chain()))
    ledger = _stage("ledger", lambda: final_ledger(score, s10, s10y, scp, nus, bau, dm, crit, anom, masses, closed, joint))
    _TRACE["stage"] = "self_checks"                 # everything below validates the stages above
    _TRACE["inputs"].setdefault("self_checks", set())
    checks = self_checks(flav, cosmo, scales, steps, grid, survey, yuk)
    # Part K checks
    k16 = 16 * math.pi ** 2
    hr = sm_higgs_rhs()
    gn = float(GUT_NORM)
    got_l = [hr([0, 0, 0, 1, 0, 0, 0], 6)[6] * k16, hr([0, 0, 0, 0, 0, 0, 1], 6)[6] * k16,
             hr([0, 1, 0, 0, 0, 0, 0], 6)[6] * k16, hr([1 / math.sqrt(gn), 0, 0, 0, 0, 0, 0], 6)[6] * k16]
    want_l = [-12, 12, 9 / 4, 3 / 4]
    checks.append(("SM beta_lambda coefficients: -12 y_t^4, 12 lambda^2, (9/4) g^4, (3/4) g'^4",
                   all(abs(a - b) < num("check_rel_tol") for a, b in zip(got_l, want_l)),
                   ", ".join(f"{a:.4f}" for a in got_l)))
    if higgs:
        r0 = max(higgs["rows"], key=lambda r: r["mh_max_mixing"])
        m2 = mssm_higgs_mass(flav, r0["M_S"], r0["tan_beta"], math.sqrt(6), steps=2 * steps)
        rel = abs(m2 / r0["mh_max_mixing"] - 1)
        checks.append(("Higgs-mass running converged (step count doubled)", rel < num("check_rg_tol"),
                       f"rel change {rel:.1e}"))
        xs = [c[0] for c in higgs["xt_curve"]]
        peak = max(higgs["xt_curve"], key=lambda c: c[1])[0]
        spacing = xs[1] - xs[0]
        checks.append(("Largest Higgs mass over the X_t scan sits at X_t^2 = 6 M_S^2 (the bound used)",
                       abs(peak - math.sqrt(6)) <= spacing, f"peak at X_t/M_S = {peak:.3f}"))
    # Part L checks
    pt = [2 / 5, 3 / 5, 11 / 10, 9 / 10, 0, 0, 1 / 10]
    one_l = sm_rge(1)(pt, 6)[6]
    k_conv = sm_higgs_rhs()(pt[:6] + [2 * pt[6]], 6)[6] / 2
    checks.append(("One-loop beta_lambda: Part L convention = Part K convention (lambda_K = 2 lambda)",
                   abs(one_l / k_conv - 1) < num("check_rel_tol"), f"rel diff {abs(one_l / k_conv - 1):.1e}"))
    # the quoted coefficients, rewritten for hypercharge g'^2 = (3/5) g1^2 and d/d ln mu, must give
    # the independently published form (Ford, Jack, Jones 1992; Degrassi et al. 2012)
    lam_terms = {tuple(p): a for a, *p in LAMBDA_2L}
    gn_ = GUT_NORM
    conv = [2 * lam_terms[(3, 0, 0, 0, 0)], 2 * lam_terms[(1, 0, 0, 0, 2)] / gn_ ** 2,
            2 * lam_terms[(0, 0, 0, 0, 3)] / gn_ ** 3, 2 * lam_terms[(2, 0, 0, 0, 1)] / gn_,
            2 * lam_terms[(0, 1, 0, 1, 1)] / gn_]
    want_c = [Fr(-312), Fr(629, 24), Fr(-379, 48), Fr(36), Fr(21, 2)]
    checks.append(("Two-loop beta_lambda coefficients agree with the hypercharge-normalized literature form",
                   conv == want_c, " ".join(str(v_) for v_ in conv)))
    mt_c, _, _, st_c, _ = matched_couplings(None, crit["two_loop_one_loop"]["m_h"], True)
    lam_fine = critical_lambda(st_c, mt_c, crit["planck"]["M_P"], 2, steps=2 * int(num("crit_steps_per_efold")))
    rel = abs(lam_fine / crit["two_loop_one_loop"]["lambda_mt"] - 1)
    big_c, _, s_c = anchored_state(None, crit["central"]["m_h"], crit["smdr"])
    lam_fine3 = critical_lambda(s_c[:6], big_c, crit["planck"]["M_P"], 3, steps=2 * int(num("crit_steps_per_efold")),
                                guess=crit["central"]["lambda_Mt"])
    rel3 = abs(lam_fine3 / crit["central"]["lambda_Mt"] - 1)
    checks.append(("Criticality solve converged (step count doubled; two and three loops)",
                   max(rel, rel3) < num("check_rg_tol"), f"rel change {max(rel, rel3):.1e}"))
    bz = crit["buttazzo"]
    tol_l = num("check_lit_tol")
    checks.append(("Three-loop RGEs: Buttazzo et al.'s couplings at M_t reproduce their Planck-scale values"
                   " (two loops must miss)", bz["dev_3L"] < tol_l < bz["dev_2L"],
                   f"max dev {bz['dev_3L']:.1e} at 3 loops, {bz['dev_2L']:.1e} at 2"))
    m_paper = crit["row"]["3L/two loops, QCD 3"]["m_h"]
    checks.append(("Part L at Buttazzo et al.'s order = their lambda(M_Pl) = 0, solved at our M_t, alpha_s"
                   " (their theory error)", abs(m_paper - bz["mh_linear"]) < bz["mh_linear_tol"],
                   f"{m_paper:.2f} against {bz['mh_linear']:.2f} GeV"))
    qc = crit["qcd_checks"]
    checks.append(("Four-loop QCD beta function: RunDec's alpha_s(M_b) (7 digits) and alpha_s(1 GeV) at 3, 4 loops",
                   qc["dev_alpha_Mb"] < num("check_lit_tol") / 10 and qc["dev_alpha_1GeV"] < num("check_lit_tol") / 2,
                   f"alpha_s(M_b) = {qc['alpha_Mb_4L']:.7f}, alpha_s(1 GeV) = {qc['alpha_1GeV_4L']:.4f}"))
    checks.append(("Four-loop mass anomalous dimension = Chetyrkin's numerical form (each power of n_f); B4;"
                   " decoupling inverted exactly", qc["dev_gamma"] < num("check_lit_tol") / 10
                   and qc["dev_B4"] < num("check_lit_b4_tol") and qc["dev_roundtrip"] < num("check_rel_tol"),
                   f"max rel dev {qc['dev_gamma']:.1e}, B4 dev {qc['dev_B4']:.1e}"))
    sm_ = crit["smdr"]
    checks.append(("This script's own matching = SMDR's at its reference point, within Buttazzo et al.'s"
                   " theory errors (lambda, y_t)", abs(sm_["lambda"]) < bz["lambda_th"] and abs(sm_["y_t"]) < bz["yt_th"],
                   f"lambda {sm_['lambda']:+.1e}, y_t {sm_['y_t']:+.1e}"))
    checks.append(("Two-loop matching: their inputs give their lambda(M_t) and y_t(M_t) within their theory errors",
                   bz["dev_lambda"] < bz["lambda_th"] and bz["dev_yt"] < bz["yt_th"],
                   f"lambda {bz['lambda_Mt']:.5f}, y_t {bz['yt_Mt']:.5f}"))
    # matching: B0 in closed form against direct quadrature (midpoint rule, below and above threshold)
    n_q = int(num("check_b0_points"))
    worst_b = 0.0
    xm = _float_inputs()
    mt_p, mw_p, mz_p = xm["M_t"], xm["M_W"], xm["M_Z"]
    mh_p = (mt_p + mw_p) / 2                 # any test point: the checks are identities
    for p2, m1, m2 in ((mh_p ** 2, mt_p ** 2, mt_p ** 2), (mt_p ** 2, 0, mw_p ** 2), (mt_p ** 2, mt_p ** 2, mz_p ** 2)):
        quad = -sum(math.log(abs(((i + 1 / 2) / n_q) * m1 + (1 - (i + 1 / 2) / n_q) * m2
                                 - ((i + 1 / 2) / n_q) * (1 - (i + 1 / 2) / n_q) * p2) / mt_p ** 2)
                    for i in range(n_q)) / n_q
        worst_b = max(worst_b, abs(pv_b0(p2, m1, m2, mt_p ** 2) - quad))
    checks.append(("Passarino-Veltman B0 in closed form = direct quadrature (below and above threshold)",
                   worst_b < num("check_b0_tol"), f"max abs diff {worst_b:.1e}"))
    # the mu dependence of the one-loop thresholds must be the one-loop RGE (tree couplings from masses)
    vv = crit["state_mt"][1]
    g2t = 2 * mw_p / vv
    g1t = 2 * math.sqrt((mz_p ** 2 - mw_p ** 2) / float(GUT_NORM)) / vv
    yt_t, lam_t = math.sqrt(2) * mt_p / vv, mh_p ** 2 / (2 * vv ** 2)
    beta1 = sm_rge(1)([g1t, g2t, 0, yt_t, 0, 0, lam_t], 6)
    h_ = num("check_fd_rel_step")
    worst_m = 0.0
    for f_, want_ in ((lambda m_: lambda_one_loop(mh_p, mt_p, mw_p, mz_p, vv, m_), beta1[6]),
                      (lambda m_: yt_ew_one_loop(mh_p, mt_p, mw_p, mz_p, vv, m_), beta1[3])):
        for mu_ in (mz_p, mt_p, 2 * mt_p):
            d_ = (f_(mu_ * math.exp(h_)) - f_(mu_ * math.exp(-h_))) / (2 * h_)
            worst_m = max(worst_m, abs(d_ / want_ - 1))
    checks.append(("One-loop matching of lambda and y_t: d/d ln mu reproduces the one-loop RGE exactly",
                   worst_m < num("check_fd_tol") * 100, f"max rel diff {worst_m:.1e}"))
    checks.append(("Every symmetry found reproduces its target zeros exactly (recomputed from the charges)",
                   all(sv["verified"] for e in symm["by_beta"].values() for sv in e["survivors"]
                       if sv["symmetry"] is not None), ""))
    full = frozenset((i, a) for i in range(3) for a in range(3))
    diag = frozenset((i, i) for i in range(3))
    draw = _IntStream(int(num("closure_seed")))
    r_full, r_diag = invariant_rank(full, full, draw), invariant_rank(diag, diag, draw)
    checks.append(("Invariant-rank method: general matrices give 10 physical parameters, diagonal ones 6",
                   (r_full, r_diag) == (10, 6), f"ranks {r_full}, {r_diag}"))
    u_full = 2 * (len(full) + len(full)) - stabilizer_rank(full, full, draw)
    u_diag = 2 * (len(diag) + len(diag)) - stabilizer_rank(diag, diag, draw)
    upper_tri = frozenset((i, a) for i in range(3) for a in range(i, 3))
    cp_ok = cp_identically_zero(diag, diag) and not cp_identically_zero(upper_tri, diag)
    checks.append(("Part F certificates: symmetry upper bounds meet the ranks (10, 6); J = 0 proved"
                   " for diagonal matrices and refuted for triangular ones", (u_full, u_diag) == (10, 6) and cp_ok,
                   f"upper bounds {u_full}, {u_diag}"))
    # Part H
    tol = num("check_rel_tol")
    xf = _float_inputs()
    hb, cc, gg, kk = xf["h"] / (2 * math.pi), xf["c"], xf["G"], xf["k_B"]
    msun = qg["black_holes"]["sun"]["mass_kg"]
    step = msun * num("check_fd_rel_step")
    s_p = _schwarzschild(msun + step, cc, gg, hb, kk)["S_BH_kB"]
    s_m = _schwarzschild(msun - step, cc, gg, hb, kk)["S_BH_kB"]
    ds_de = (s_p - s_m) / (2 * step * cc ** 2)                # dS/dE in units of k_B per joule
    inv_kt = 1 / (kk * qg["black_holes"]["sun"]["T_H_K"])
    checks.append(("Black-hole first law: dS/dE = 1/(k_B T_H) (entropy and temperature consistent)",
                   abs(ds_de / inv_kt - 1) < num("check_fd_tol"), f"rel diff {abs(ds_de / inv_kt - 1):.1e}"))
    kappa = cc ** 4 / (4 * gg * msun)                        # surface gravity
    t_unruh = hb * kappa / (2 * math.pi * cc * kk)
    rel = abs(t_unruh / qg["black_holes"]["sun"]["T_H_K"] - 1)
    checks.append(("Hawking temperature = Unruh temperature at the horizon's surface gravity", rel < tol,
                   f"rel diff {rel:.1e}"))
    ds = qg["de_sitter"]
    rel = abs(ds["S_area_law_kB"] / ds["S_part_A_kB"] - 1)
    checks.append(("de Sitter entropy: area law A/(4 l_P^2) = Part A's pi c^5/(G hbar H^2)", rel < tol,
                   f"rel diff {rel:.1e}"))
    rel = abs(qg["numbers"]["S_dS_times_rho_ratio"] / (3 / 8) - 1)
    checks.append(("Identity: S_dS x (rho_Lambda / rho_Planck) = 3/8 exactly", rel < tol, f"rel diff {rel:.1e}"))
    en = qg["entanglement"]
    rel = abs(en["entropy_bits"] - en["entropy_formula_bits"])
    checks.append(("Entanglement entropy: reduced density matrix = concurrence formula", rel < tol,
                   f"abs diff {rel:.1e}"))
    lam = qg["transmutation"]["Lambda5_GeV"]
    b0, b1 = (float(v) for v in qcd_beta(5))
    t = math.log(xf["M_Z"] ** 2 / lam ** 2)
    back = 4 * math.pi / (b0 * t) * (1 - b1 * math.log(t) / (b0 ** 2 * t))
    sm2 = sm_two_loop_b()
    want_sm2 = [[Fr(199, 50), Fr(27, 10), Fr(44, 5)], [Fr(9, 10), Fr(35, 6), Fr(12)], [Fr(11, 10), Fr(9, 2), Fr(-26)]]
    mb1, mb2 = mssm_b()
    want_m2 = [[Fr(199, 25), Fr(27, 5), Fr(88, 5)], [Fr(9, 5), Fr(25), Fr(24)], [Fr(11, 5), Fr(9), Fr(14)]]
    checks.append(("Two-loop gauge coefficients from field content = textbook matrices (SM and MSSM)",
                   sm2 == want_sm2 and mb1 == [Fr(33, 5), Fr(1), Fr(-3)] and mb2 == want_m2, ""))
    worst_u = 0.0
    for row in alpha_unif["rows"]:
        finite = math.isfinite(row["M_S"])
        exact = predict_alpha_one_loop_exact(xf["s2_hat_Z"], xf["alpha_s_MZ"], xf["M_Z"],
                                             row["M_S"] if finite else 1, sm_only=not finite)
        worst_u = max(worst_u, abs(row["loop1"]["inv_alpha"] / exact - 1))
    checks.append(("Unification solver at one loop = closed-form solution (every M_S, and pure SM)",
                   worst_u < num("check_survey_tol"), f"max rel diff {worst_u:.1e}"))
    f_ = _fields()
    got = (_pair_gauge_coeffs(f_["Q"], f_["u^c"]), _pair_gauge_coeffs(f_["Q"], f_["d^c"]),
           _pair_gauge_coeffs(f_["L"], f_["e^c"]),
           _susy_gauge_coeffs((f_["H_u"], f_["Q"], f_["u^c"])), _susy_gauge_coeffs((f_["H_d"], f_["Q"], f_["d^c"])),
           _susy_gauge_coeffs((f_["H_d"], f_["L"], f_["e^c"])))
    want = ((17 / 20, 9 / 4, 8), (1 / 4, 9 / 4, 8), (9 / 4, 9 / 4, 0),
            (13 / 15, 3, 16 / 3), (7 / 15, 3, 16 / 3), (9 / 5, 3, 0))
    ok_y = all(abs(a - b) < tol for g_, w_ in zip(got, want) for a, b in zip(g_, w_))
    checks.append(("Yukawa-RGE gauge coefficients from Casimirs = textbook (SM and MSSM; t, b, tau)", ok_y, ""))
    yt_test = yukawa_rhs("MSSM")([0, 0, 0, 1, 0, 0], 6)[3] * 16 * math.pi ** 2
    yl_test = yukawa_rhs("MSSM")([0, 0, 0, 0, 1, 1], 6)[5] * 16 * math.pi ** 2
    checks.append(("MSSM Yukawa self-terms from field multiplicities: 6 y_t^3, (3 y_b^2 + 4 y_tau^2) y_tau",
                   abs(yt_test - 6) < tol and abs(yl_test - 7) < tol, f"{yt_test:.3f}, {yl_test:.3f}"))
    checks.append(("Lambda_QCD (2-loop) reproduces alpha_s(M_Z)", abs(back / xf["alpha_s_MZ"] - 1) < tol,
                   f"rel diff {abs(back / xf['alpha_s_MZ'] - 1):.1e}"))
    checks.append(("Part M at Part I's M_S reproduces the measured alpha (the two stages agree)",
                   abs(joint["check_U_at_part_I"]) < num("unif_tol") * 100,
                   f"diff {joint['check_U_at_part_I']:.1e}"))
    # Parts N, O, P
    xn = _float_inputs()
    worst_p = 0.0
    for o in NU_ORDERINGS:
        q_ = nu_params(xn, o)
        back_ = pmns_angles(pmns(q_["s12sq"], q_["s13sq"], q_["s23sq"], q_["delta"]))
        worst_p = max(worst_p, *(abs(back_[k] / q_[k] - 1) for k in ("s12sq", "s13sq", "s23sq", "delta")))
        # J in the PDG form: (1/8) sin 2th12 sin 2th23 sin 2th13 cos th13 sin delta
        s2 = [2 * math.sqrt(q_[k] * (1 - q_[k])) for k in ("s12sq", "s23sq", "s13sq")]
        j_pdg = s2[0] * s2[1] * s2[2] * math.sqrt(1 - q_["s13sq"]) * math.sin(q_["delta"]) / 8
        worst_p = max(worst_p, abs(back_["J"] / j_pdg - 1))
    checks.append(("PMNS matrix: angles, delta and J recovered exactly from the matrix built from them",
                   worst_p < tol, f"max rel diff {worst_p:.1e}"))
    tb_ = pmns_angles(tribimaximal())
    cols_ok = True
    for kind, col in (("TM1", 0), ("TM2", 1)):
        um = corrected_tbm(kind, 1 / 3, 1)                 # any point: the checks are identities
        cols_ok &= all(abs(abs(um[i][col]) - abs(tribimaximal()[i][col])) < tol for i in range(3))
        cols_ok &= all(abs(sum(abs(um[i][j]) ** 2 for j in range(3)) - 1) < tol for i in range(3))
    checks.append(("Tribimaximal = (1/3, 0, 1/2); TM1/TM2 keep their TBM column and stay unitary",
                   abs(tb_["s12sq"] - 1 / 3) < tol and tb_["s13sq"] < tol and abs(tb_["s23sq"] - 1 / 2) < tol
                   and cols_ok, ""))
    # m_bb: the exact band against brute force over the two Majorana phases
    nph_ = int(num("check_phase_grid"))
    worst_b2 = 0.0
    for o in NU_ORDERINGS:
        q_ = nu_params(xn, o)
        uu = pmns(q_["s12sq"], q_["s13sq"], q_["s23sq"], q_["delta"])
        for m0 in (0.0, nus["orderings"]["NO"]["m_bb_cancellation_m0"][0] / 2, num("nu_m0_min") * 1000):
            cc = [abs(uu[0][i]) ** 2 * m for i, m in enumerate(nu_masses(q_, o, m0))]
            vals = [abs(cc[0] + cc[1] * cmath.exp(1j * 2 * math.pi * a / nph_) + cc[2] * cmath.exp(1j * 2 * math.pi * b / nph_))
                    for a in range(nph_) for b in range(nph_)]
            lo_, hi_ = max(0.0, 2 * max(cc) - sum(cc)), sum(cc)
            worst_b2 = max(worst_b2, abs(max(vals) - hi_) / hi_, (min(vals) - lo_) / hi_)
    checks.append(("m_bb: exact band over the Majorana phases = brute force on a phase grid (to grid accuracy)",
                   worst_b2 < (2 * math.pi / nph_) ** 2, f"max rel diff {worst_b2:.1e}"))
    kq = (koide_q([1, 1, 1]), koide_q([0, 0, 1]))
    worst_k = abs(kq[0] - 1 / 3) + abs(kq[1] - 1)
    m_tau_k = masses["koide_m_tau_MeV"] / 1000
    lep_ = lepton_masses_gev()
    worst_k += abs(koide_q([lep_["e"], lep_["mu"], m_tau_k]) - 2 / 3)
    checks.append(("Koide Q: 1/3 for equal masses, 1 for one mass; the m_tau solved from Q = 2/3 gives Q = 2/3",
                   worst_k < tol, f"abs diff {worst_k:.1e}"))
    par_ok = all(abs(sec["det_over_mheaviest3"] / sec["signed_eigenvalue_product"] - 1) < num("check_survey_eig_tol")
                 for r_ in scp["parity"] for sec in r_["sectors"].values())
    checks.append(("Part O: each survivor sector's det = product of its signed eigenvalues (real: arg det = 0 or pi)",
                   par_ok and bool(scp["parity"]), f"{len(scp['parity'])} survivor(s)"))
    # Part Q: the operator-running exponents from the script's own b_i = the printed ones
    pr_ = LITERATURE["proton_decay_d6"]["value"]["printed_exponents"]
    worst_q = max(abs(a_ - float(Fr(b_))) for m_ in ("SM", "MSSM") for o_ in ("S1", "S2")
                  for a_, b_ in zip(proton_exponents(m_, o_), pr_[m_][o_]))
    checks.append(("Proton decay: operator-running exponents -2 c_i/b_i from the script's b_i = Ellis et al.'s eq. 17",
                   worst_q < tol, f"max abs diff {worst_q:.1e}"))
    # Part S: the chemical-equilibrium solution satisfies every condition it imposed
    sph_ = sphaleron_conversion(3, 1)
    checks.append(("Sphaleron conversion: B/(B - L) = 28/79 and L/(B - L) = -51/79 (exact, three families, one Higgs)",
                   (sph_["B_over_BminusL"], sph_["L_over_BminusL"]) == (Fr(28, 79), Fr(-51, 79)), ""))
    # Part T: the one-loop Pati-Salam solution satisfies its three matching conditions
    ps_ = s10["pati_salam"]
    a_i = _alpha_one_loop(ps_["M_I"], xn, None)
    bp_ = {k_: float(v_) for k_, v_ in ps_["b_PS"].items()}
    ln_ = math.log(ps_["M_GUT"] / ps_["M_I"]) / (2 * math.pi)
    gn_ = float(GUT_NORM)
    at_g = [1 / a_i[2] - bp_["4"] * ln_, 1 / a_i[1] - bp_["2L"] * ln_,
            (1 / a_i[0] - (1 - gn_) / a_i[2]) / gn_ - bp_["2R"] * ln_]
    worst_t = max(abs(v_ * ps_["alpha_GUT"] - 1) for v_ in at_g)
    checks.append(("SO(10) via Pati-Salam: the solved M_I, M_GUT make SU(4), SU(2)_L, SU(2)_R meet at 1/alpha_GUT",
                   worst_t < tol, f"max rel diff {worst_t:.1e}"))
    # Part S: each z_B solves the freeze-out condition, and kappa_f -> 1 as K -> 0 (thermal initial abundance)
    worst_z = 0.0
    for e_ in bau["leptogenesis"]["efficiency"]:
        z_, k_ = e_["z_B"], e_["K"]
        worst_z = max(worst_z, abs(k_ / 4 * z_ ** 3 * math.exp(-z_) * (1 + math.sqrt(math.pi * z_ / 2)) - (z_ - 1)) / z_)
    k_small = leptogenesis_efficiency(num("nu_m0_min"))[1]
    checks.append(("Leptogenesis efficiency: z_B solves its freeze-out equation; kappa_f -> 1 in weak washout",
                   worst_z < num("check_survey_tol") and abs(k_small - 1) < num("check_fd_rel_step") * 10,
                   f"max rel residual {worst_z:.1e}, kappa(K -> 0) = {k_small:.6f}"))
    # Part W: at the parametrization's own reference point it returns M_W^0
    lw = LITERATURE["w_mass_fit"]["value"]
    xr = dict(xn)
    d_ref = float(lw["reference"]["delta_alpha"]) - float(lw["delta_alpha_lept"])
    xr.update({"M_t": float(lw["reference"]["m_t"]), "M_Z": float(lw["reference"]["M_Z"]),
               "alpha_s_MZ": float(lw["reference"]["alpha_s"]), "delta_alpha_had5": d_ref})
    w_ref = w_mass(xr, float(lw["reference"]["M_H"]))
    checks.append(("M_W parametrization returns M_W^0 at its reference point (transcription check)",
                   abs(w_ref - float(lw["coefficients"]["MW0"])) < num("check_rel_tol") * 100, f"{w_ref:.5f} GeV"))
    ls_ = LITERATURE["sin2_eff_fit"]["value"]
    xs_ = dict(xn)
    xs_.update({"M_t": float(ls_["reference"]["m_t"]), "M_Z": float(ls_["reference"]["M_Z"]),
                "alpha_s_MZ": float(ls_["reference"]["alpha_s"]),
                "delta_alpha_had5": float(ls_["reference"]["delta_alpha"]) - float(lw["delta_alpha_lept"])})
    s_ref = sin2_eff(xs_, float(ls_["reference"]["M_H"]))
    checks.append(("sin^2 theta_eff parametrization returns s0 at its reference point (transcription check)",
                   abs(s_ref - float(ls_["coefficients"]["s0"])) < num("check_rel_tol") * 100, f"{s_ref:.7f}"))
    cl_ = closed["age_with_all_dm_Gyr"]
    checks.append(("Part X with all of Omega_c reproduces Part A's age (the same Friedmann equation)",
                   abs(cl_ / float(cosmo["age_Gyr"]) - 1) < num("check_axion_tol") / 10,
                   f"{cl_:.3f} against {float(cosmo['age_Gyr']):.3f} Gyr"))
    c170 = dm["check_eq170"]
    checks.append(("Axion misalignment from its ingredients reproduces Di Luzio et al.'s eq. 170 (their approximation)",
                   abs(c170["Omega_h2"] / c170["printed"] - 1) < num("check_axion_tol"),
                   f"Omega h^2 = {c170['Omega_h2']:.4f} at f_a = {c170['f_a']:.1e} GeV against {c170['printed']}"))
    idx_ok = all(so10_decomposition_index(r_) == [Fr(SO10_INDEX[r_])] * 3 for r_ in SO10_TO_PS)
    checks.append(("SO(10) -> Pati-Salam decompositions of 10, 126, 210: component indices add up to the SO(10)"
                   " index under every factor", idx_ok, ", ".join(f"{r_}: {SO10_INDEX[r_]}" for r_ in SO10_TO_PS)))
    cv_ = s10["potential_210"]["curvatures"]
    q0_ = so10_210_invariants({PS_SINGLET_210: 1})
    gold = max(abs(v_) for v_ in cv_["(6,2,2)"].values())
    rad = max(abs(cv_["(1,1,1)"][q] - 8 * q0_[q] / 576) for q in QUARTICS_210)
    checks.append(("210 potential: the eaten (6,2,2) is massless for every coupling (Goldstone); the radial mode has"
                   " twice the vacuum curvature", gold < tol and rad < tol, f"max {max(gold, rad):.1e}"))
    c126_ = so10_126_coefficients()
    checks.append(("126: the self-dual basis is self-dual, (10,3,1) and (10bar,1,3) do not mix, and every D-even"
                   " invariant is equal on them", max(c126_["selfdual_dev"], c126_["p3_mixing"], c126_["d_even_dev"]) < tol,
                   f"max {max(c126_['selfdual_dev'], c126_['p3_mixing'], c126_['d_even_dev']):.1e}"))
    a10_ = so10_10_splitting()
    a10_ok = all(abs(a10_.get((i, i), 0) - (6 if i >= 6 else 0)) < tol for i in range(10)) and all(
        abs(v_) < tol for (i, j), v_ in a10_.items() if i != j)
    checks.append(("10: A_ij = phi phi at the vev is 6 v^2 on SO(4) indices, 0 on SO(6), diagonal (splits (1,2,2) from"
                   " (6,1,1))", a10_ok, ""))
    mt_ = [[complex(2, 0), complex(1, 1), complex(0, 2)], [complex(1, -1), complex(3, 0), complex(1, 0)],
           [complex(0, -2), complex(1, 0), complex(1, 0)]]
    ev_ = _herm3_eigvals(mt_)
    tr_ok = abs(sum(ev_) - 6) < tol and all(
        max(abs(sum(mt_[i][k] * v_[k] for k in range(3)) - e_ * v_[i]) for i in range(3)) < tol
        for e_ in ev_ for v_ in [_herm3_eigvec(mt_, e_)])
    checks.append(("Closed-form 3x3 Hermitian eigenvalues: trace preserved and every eigenvector satisfies A v = lambda v",
                   tr_ok, ", ".join(f"{e_:.4f}" for e_ in ev_)))
    sm_c1, sm_c2 = sm_as_chain()
    ps1 = s10["chains"]["PS"]["loop1"]
    rel_c = max(abs(ps1["M_I"] / ps_["M_I"] - 1), abs(ps1["M_GUT"] / ps_["M_GUT"] - 1))
    checks.append(("SO(10) chains: the general two-loop formula on the SM content = sm_gauge_b, sm_two_loop_b;"
                   " the Newton solver at one loop = the linear solution", sm_c1 == list(sm_gauge_b())
                   and sm_c2 == sm_two_loop_b() and rel_c < num("check_survey_tol") * 10, f"rel diff {rel_c:.1e}"))
    _TRACE["stage"] = None
    lin = model_lineage()
    checks.append(("Model graph: every stage registered, acyclic, and run in dependency order",
                   lin["registered"] and lin["acyclic"] and lin["in_order"],
                   f"{len(lin['order'])} stages, {sum(len(u) for u in lin['uses'].values())} edges"))
    return {"scales": scales, "cosmology": cosmo, "flavour": flav, "survey": survey, "yukawa_331": yuk,
            "symmetry": symm, "closure": closure, "quantum_gravity": qg, "alpha_unification": alpha_unif,
            "alpha_numerology": alpha_num, "yukawa": yukawa, "higgs": higgs, "criticality": crit,
            "joint": joint, "mass_formulas": masses, "strong_cp": scp, "neutrinos": nus, "proton_decay": pdk,
            "anomalies": anom, "baryon_asymmetry": bau, "so10": s10, "scorecard": score,
            "dark_matter": dm, "w_mass": mw, "closed_cosmology": closed, "so10_yukawa": s10y, "ledger": ledger,
            "survey_certificates": certs, "checks": checks, "lineage": lin,
            "changed_inputs": dict(_TRACE["set"]),
            "precision": prec}


def model_lineage() -> Dict[str, Any]:
    """The dependency graph the last run followed, read from the trace, and what it implies:
    which stages each measured input reaches, and which stage assumptions conflict."""
    order = list(_TRACE["inputs"])                      # stages in the order they ran
    uses = {st: sorted(_TRACE["uses"].get(st, ()), key=order.index) for st in order}
    reads = {st: sorted(_TRACE["inputs"][st]) for st in order}
    # every stage downstream of each stage (transitive)
    down: Dict[str, set] = {st: set() for st in order}
    for st in reversed(order):
        for consumer in order:
            if st in uses[consumer]:
                down[st] |= {consumer} | down[consumer]
    reaches = {}
    for name in INPUTS:
        direct = {st for st in order if name in reads[st]}
        allst = set(direct)
        for st in direct:
            allst |= down[st]
        reaches[name] = sorted(allst, key=order.index)
    uv: Dict[str, List[str]] = {}
    for st in order:
        if "uv" in STAGES.get(st, {}):
            uv.setdefault(STAGES[st]["uv"], []).append(st)
    takers = {f"{p}[{k}]": sorted(v - {"self_checks"}, key=order.index) for (p, k), v in _TRACE["keys"].items()}
    return {"order": order, "uses": uses, "reads": reads, "reaches": reaches, "takers": takers,
            "registered": all(st in STAGES for st in order)
            and all(st in order for st in STAGES if st != "survey_certificates"),
            "acyclic": all(st not in down[st] for st in order),
            "in_order": all(order.index(u) < order.index(st) for st in order for u in uses[st]),
            "uv_hypotheses": uv, "uv_consistent": len(uv) <= 1}


def _wrap(text: str, indent: int, width: int = 78) -> str:
    lines, cur = [], " " * indent
    for word in text.split():
        if len(cur) + len(word) + 1 > width and cur.strip():
            lines.append(cur.rstrip())
            cur = " " * (indent + 2)
        cur += word + " "
    lines.append(cur.rstrip())
    return "\n".join(lines)


def report(res: Dict[str, Any]) -> str:
    out: List[str] = []
    w = out.append
    bar = "=" * 78
    cos = res["cosmology"]
    flav = res["flavour"]
    runner = flav["runner"]
    w(bar)
    w(f"STUR Physics Lab, {VERSION}: nothing tuned, nothing fitted")
    w(bar)
    w(f"Inputs: {len(INPUTS)} measured or defined constants (INPUTS). Comparisons: {len(COMPARISONS)}"
      f" measured results, never used in a calculation.")
    for name, val in res["changed_inputs"].items():
        w(f"  CHANGED INPUT (--set): {name} = {val} instead of {INPUTS[name]['value']}; every stage it"
          " reaches is recalculated")
    w("")
    w("PART A. COSMOLOGY (flat Lambda-CDM, Friedmann equation)")
    w("-" * 78)
    w(f"  Omega_gamma  from T_CMB (Stefan-Boltzmann)    {_fmt(float(cos['Omega_gamma']), 6)}")
    w(f"  Omega_r      photons + N_eff neutrinos         {_fmt(float(cos['Omega_r']), 6)}")
    w(f"  Omega_Lambda = 1 - Omega_m - Omega_r           {float(cos['Omega_Lambda']):.6f}"
      f" +/- {cos['Omega_Lambda_sigma']:.4f}")
    ol, ol_up, _ = _comparison("Omega_Lambda")
    w(f"      measured (Planck 2018)                    {ol} +/- {ol_up}"
      f"   pull {(float(cos['Omega_Lambda']) - ol) / math.hypot(ol_up, cos['Omega_Lambda_sigma']):+.2f} sigma")
    age = float(cos["age_Gyr"])
    w(f"  Age of the universe t0                         {age:.4f} Gyr"
      f" +/- {cos['age_sigma_uncorrelated_Gyr']:.3f} (H0, Omega_m, T_CMB uncorrelated)")
    a_meas, a_up, _ = _comparison("age_Gyr")
    w(f"      measured (Planck 2018)                    {a_meas} +/- {a_up} Gyr"
      f"   difference {age - a_meas:+.4f} Gyr")
    w(f"      (the Planck error is smaller because Planck's H0 and Omega_m are anticorrelated)")
    w(f"  Deceleration parameter q0                      {float(cos['q0']):+.5f}")
    w(f"  Acceleration began at redshift z_acc           {float(cos['z_acc']):.5f}")
    w(f"  Matter-radiation equality z_eq                 {float(cos['z_eq']):.1f}")
    w(f"  Matter-Lambda equality a                       {float(cos['a_matter_Lambda']):.5f}")
    w(f"  Hubble-horizon entropy today                   {float(cos['S_Hubble_today_kB']):.4e} k_B")
    w(f"  de Sitter horizon entropy (t -> infinity)      {float(cos['S_deSitter_kB']):.4e} k_B")
    w(f"  Age to {res['precision']} digits: {cos['age_Gyr']} Gyr (numerical, not physical, precision)")
    w("")
    w("PART B. QUARK FLAVOUR: RG-run masses in the Fritzsch six-zero texture")
    w("-" * 78)
    base = flav["ratios"][runner.mt_msbar]
    w(f"  m_t(m_t) MS-bar from the pole mass ({runner.loops}-loop)    {runner.mt_msbar:.3f} GeV")
    w(f"  v = (sqrt2 G_F)^(-1/2)                         {runner.v:.3f} GeV")
    w(f"  y_t(m_t) = sqrt2 m_t(m_t) / v                  {runner.ew['y_t_at_mt']:.4f}")
    w(f"  sin^2 theta_W (tree level, from G_F, alpha, M_Z) {runner.ew['sin2_theta_tree']:.5f}")
    w(f"  Running masses at m_t(m_t) (GeV): u {base['m_u']:.4e}  d {base['m_d']:.4e}  s {base['m_s']:.4e}"
      f"  c {base['m_c']:.4f}  b {base['m_b']:.4f}")
    w("")
    w("  The texture fixes every matrix entry from the masses. Its two phases are not")
    w("  fixed by anything, so each prediction is the band swept by ALL phase values;")
    w("  the band edges carry the propagated input uncertainty.")
    for mu in res["scales"]:
        blk = flav["scales"][mu]
        r = blk["ratios"]
        w("")
        w(f"  Scale mu = {mu:.0f} GeV   alpha_s = {r['alpha_s']:.5f}   y_t = {r['y_t']:.4f}")
        w(f"    sqrt(m_d/m_s) = {math.sqrt(r['r_ds']):.5f}  sqrt(m_u/m_c) = {math.sqrt(r['r_uc']):.5f}"
          f"  sqrt(m_s/m_b) = {math.sqrt(r['r_sb']):.5f}  sqrt(m_c/m_t) = {math.sqrt(r['r_ct']):.5f}")
        w(f"    {'observable':<10} {'band over all phases':<34} {'measured':<22} verdict")
        for k in OBSERVABLES:
            b = blk["bands"][k]
            meas, up, dn = _comparison(k)
            band = f"[{_fmt(b['lo'])} +/- {_fmt(b['sigma_lo'], 2)}, {_fmt(b['hi'])} +/- {_fmt(b['sigma_hi'], 2)}]"
            m_s = f"{_fmt(meas)} +{_fmt(up, 2)}/-{_fmt(dn, 2)}"
            vm = b["vs_measurement"]
            verdict = "inside band" if vm["inside"] else f"outside by {vm['n_sigma']:.1f} sigma"
            w(f"    {k:<10} {band:<34} {m_s:<22} {verdict}")
    w("")
    excluded = [(k, flav["scales"][mu]["bands"][k]["vs_measurement"]["n_sigma"])
                for mu in res["scales"] for k in OBSERVABLES
                if not flav["scales"][mu]["bands"][k]["vs_measurement"]["inside"]]
    if excluded:
        worst = {}
        for k, n in excluded:
            worst[k] = min(worst.get(k, math.inf), n)
        w("  RESULT: at every evaluation scale and for every value of the two phases, the")
        w("  six-zero texture misses: " + ", ".join(f"{k} (at least {n:.0f} sigma)" for k, n in worst.items())
          + ".")
        w("  The masses alone do not produce the measured mixing in this texture.")
    else:
        w("  RESULT: every measured value lies inside its band at every evaluation scale.")
    w("")
    w("PART C. EVERY TEXTURE-ZERO PATTERN THAT MAKES A PREDICTION")
    w("-" * 78)
    w("  Hermitian mass matrices; a symmetric off-diagonal pair counts as one zero.")
    w("  Unknowns (2 phases, 1 per free entry) are scanned or tested, never fixed;")
    w("  predictions = 4 data (|V_us|, |V_cb|, |V_ub|, J) - unknowns.")
    sv0 = res["survey"][res["scales"][0]]
    recs = {mu: {(r["zeros_u"], r["zeros_d"]): r for r in res["survey"][mu]["classes"]} for mu in res["scales"]}
    n_loop = sum(1 for r in sv0["classes"] if r["status"] == "loop")
    n_none = sum(1 for r in sv0["classes"] if r["status"] == "no_solution")
    tested = [r for r in sv0["classes"] if r["status"] == "tested"]
    w(f"  {sv0['n_ordered_pairs']} ordered pattern pairs with 5 or 6 zeros fall into {len(sv0['classes'])} classes"
      f" under weak-basis permutations:")
    w(f"    {n_none:3d} cannot give three nonzero masses with real entries")
    w(f"    {n_loop:3d} keep a phase inside one sector, so they predict nothing (not tested)")
    w(f"    {len(tested):3d} make predictions and are tested")
    w("")
    sc = res["scales"]
    w("  zeros  up mass matrix  down mass matrix  pred   n-sigma at " + "  ".join(f"{m / 1000:g} TeV" for m in sc)
      + "   verdict")

    def key_sigma(r: Dict[str, Any]) -> float:
        return max(recs[mu][(r["zeros_u"], r["zeros_d"])]["sigma"] for mu in sc)
    for r in sorted(tested, key=key_sigma):
        k = (r["zeros_u"], r["zeros_d"])
        sig_s = "  ".join(f"{recs[mu][k]['sigma']:9.1f}" if recs[mu][k]["sigma"] < 1000 else "    >1000"
                          for mu in sc)
        surv = all(recs[mu][k]["survives"] for mu in sc)
        how = "joint" if recs[sc[0]][k].get("pair") is not None else "band"
        verdict = "SURVIVES" if surv else f"excluded ({how})"
        w(f"  {r['zeros']:5d}  {pattern_mask(r['zeros_u']):<14}  {pattern_mask(r['zeros_d']):<16}  {r['predictions']:4d}"
          f"   {sig_s}   {verdict}")
    w("  (masks: rows of the matrix, X = nonzero, 0 = texture zero; 'band' = one |V_ij| alone")
    w("   is out of reach for every value of the unknowns; 'joint' = all four data at once)")
    survivors = [r for r in tested if all(recs[mu][(r["zeros_u"], r["zeros_d"])]["survives"] for mu in sc)]
    for r in survivors:
        k = (r["zeros_u"], r["zeros_d"])
        w("")
        w(f"  Survivor  up {pattern_mask(k[0])}  down {pattern_mask(k[1])}:"
          f" {r['predictions']} prediction(s), class of {r['orbit']} equivalent orderings")
        for mu in sc:
            rr = recs[mu][k]
            bands = "  ".join(f"{name} [{_fmt(lo, 3)}, {_fmt(hi, 3)}]" for name, (lo, hi) in rr["bands"].items())
            w(f"    {mu / 1000:g} TeV: chi^2 = {rr['chi2']:.2f} for {rr['predictions']} dof"
              f" ({rr['sigma']:.1f} sigma);  ranges over all unknowns: {bands}")
    if survivors:
        w("  (the free entry and the phases sweep each observable over a wide range on its own; the")
        w("   prediction is a relation among the four, which the joint test checks)")
        for r in survivors:
            k = (r["zeros_u"], r["zeros_d"])
            w("  What it predicts: |V_us|, |V_cb|, |V_ub| fix its three unknowns at isolated points; at each,")
            w("  |J| and |V_td/V_ts| follow (errors: the three moduli and the inputs, re-solved):")
            mj, sj, _ = _comparison("J")
            mq, sq, _ = _comparison("V_td/V_ts")
            for mu in sc:
                for o in recs[mu][k]["prediction"]:
                    pj = (o["J"] - mj) / math.hypot(o["J_sigma"], sj)
                    pq = (o["V_td/V_ts"] - mq) / math.hypot(o["V_td/V_ts_sigma"], sq)
                    w(f"    {mu / 1000:g} TeV: |J| = {o['J']:.3e} +/- {o['J_sigma']:.1e} ({pj:+.1f} sigma)   |V_td/V_ts| ="
                      f" {o['V_td/V_ts']:.4f} +/- {o['V_td/V_ts_sigma']:.4f} ({pq:+.1f} sigma)")
            w(f"    measured: J = {mj:.3e} +/- {sj:.1e}, |V_td/V_ts| = {mq} +/- {sq}")
            best = []
            for mu in sc:
                c2 = [((o["J"] - mj) / math.hypot(o["J_sigma"], sj)) ** 2
                      + ((o["V_td/V_ts"] - mq) / math.hypot(o["V_td/V_ts_sigma"], sq)) ** 2
                      for o in recs[mu][k]["prediction"]]
                best.append(pvalue_to_sigma(chi2_pvalue(min(c2), 2)) if c2 else math.inf)
            w(f"    Both predictions at once (2 dof), best solution: " + ", ".join(
                f"{b:.1f} sigma at {mu / 1000:g} TeV" for b, mu in zip(best, sc)))
            w("    |V_td/V_ts| is not used by the survey, but the PDG fit behind the measured moduli and J")
            w("    includes B-mixing data, so this test is not fully independent of them.")
            w("    (|V_td/V_ts| is used nowhere in the survey: it is an independent test)")
    cert_ = res.get("survey_certificates")
    w("")
    if cert_:
        bad = [r for r in cert_["results"] if not r["certified"]]
        w(f"  Certificates (at m_t(m_t)): {cert_['certified']} of {cert_['excluded']} exclusions are proved over the")
        w("    whole parameter space (every point of every family, both phases), by interval bounds on")
        w("    the matrix entries, perturbation bounds on the eigenvectors and branch-and-bound;")
        w(f"    {cert_['seconds']:.0f} s.")
        if bad:
            w("    Not proved (excluded by the numerical search only): " + "; ".join(
                f"{pattern_mask(r['zeros_u'])} / {pattern_mask(r['zeros_d'])}" for r in bad))
        w("    A survival needs no certificate: the search exhibits a point that fits.")
    else:
        w("  Certificates: not run here (python3 production_v2_2.py --certify proves each exclusion over")
        w("    the whole parameter space; it takes several minutes).")
    if not survivors:
        w("  RESULT: no texture-zero pattern with a prediction survives.")
    else:
        w("")
        w(f"  RESULT: {len(survivors)} of {len(tested)} predictive patterns survive at every scale;"
          f" {len(tested) - len(survivors)} are excluded.")
    w("")
    w("PART D. WHAT 3-3-1 SAYS ABOUT THE MASS MATRICES (from the gauge charges)")
    w("-" * 78)
    for b, y in res["yukawa_331"].items():
        sign = "-" if b < 0 else "+"
        w(f"  beta = {sign}1/sqrt3:")
        for fam, q in y["quarks"].items():
            ch = ", ".join(str(c) for c in q["charges"])
            w(f"    family {fam}: {q['rep']:<4} X = {str(q['X']):>4}  components ({', '.join(q['content'])})"
              f" with charges ({ch})")
        for (fam, flav), ops in y["operators"].items():
            if fam == 2:
                continue
            desc = "; ".join(f"Q_{fam} S{'*' if o['conjugate'] else ''}(X={o['scalar_X']}) {flav}^c,"
                             f" vev in component {o['component']}" for o in ops)
            w(f"    row {'1, 2' if fam == 1 else '3   '} of M_{flav}: {desc}")
        for s_ in y["shared_scalars"]:
            w(f"    note: the scalar with X = {s_['X']} has {len(s_['neutral'])} neutral components"
              f" (two triplets with identical charges)")
    y = res["yukawa_331"][-1]
    perms = residual_permutations(y["left_blocks"])
    w("  Consequences, identical for both values of beta:")
    w(f"    * every entry of both mass matrices is allowed: {y['all_entries_allowed']}. The gauge symmetry forces")
    w("      no texture zero, so 3-3-1 alone neither rescues nor selects a pattern.")
    w("    * rows 1, 2 get one vev and row 3 another: M = diag(v_A, v_A, v_B) x (free Yukawas).")
    w(f"    * the left-handed families split into gauge blocks {y['left_blocks']}, so only"
      f" {len(perms)} of the 6 index permutations stay basis changes.")
    w("      A texture class therefore becomes several distinct 3-3-1 hypotheses, which differ in")
    w("      which index is the triplet family (index 3 below). They give the same CKM matrix")
    w("      but different flavour-changing Z' couplings.")
    for r in survivors:
        vs = versions_331(r["zeros_u"], r["zeros_d"], perms)
        w(f"    survivor up {pattern_mask(r['zeros_u'])} down {pattern_mask(r['zeros_d'])}:"
          f" {len(vs)} distinct 3-3-1 placements")
        for zu, zd in vs:
            w(f"      up {pattern_mask(zu)}   down {pattern_mask(zd)}")
    w("")
    w("PART E. CAN A FLAVOUR SYMMETRY PRODUCE THE SURVIVOR INSIDE 3-3-1?")
    w("-" * 78)
    sy = res["symmetry"]["by_beta"]
    nmax = int(num("symmetry_max_N"))
    for b, e in sy.items():
        sign = "-" if b < 0 else "+"
        w(f"  beta = {sign}1/sqrt3:")
        w(f"    E1. Minimal scalars (one per row and sector). Down-minus-up scalar charge is the same")
        w(f"        for all three rows: {e['common_shift']}. So any abelian symmetry groups the rows the")
        w(f"        same way in both sectors. Exhaustive scan of Z_N, N = 2..{nmax}:")
        for m in e["minimal_scan"]:
            w(f"          Z_{m['N']}: {m['pattern_pairs']:6d} realizable pattern pairs, {m['with_zeros_and_mixing']}"
              f" with a texture zero and three-family mixing")
        w(f"    E2. Hermitian mass matrices: a symmetry would have to map Q_i (SU(3)_L (anti)triplets)")
        w(f"        onto u^c, d^c (singlets). Possible: {e['hermitian_possible']}.")
        w(f"    E3. The survivor's zeros alone, with extra copies of the two mass-giving scalars:")
        for sv in e["survivors"]:
            ext, gc = sv["symmetry"], sv["general_count"]
            tag = f"up {pattern_mask(sv['zeros_u'])}  down {pattern_mask(sv['zeros_d'])}"
            if ext is None:
                w(f"        {tag}: no Z_N with N <= {nmax} does it")
            else:
                sc = "; ".join(f"X={k[0]} scalar charges {v}" for k, v in ext["scalar_charges"].items())
                w(f"        {tag}: Z_{ext['N']} with {ext['triplets']} scalar triplets (minimal: 2)")
                w(f"          charges Q {ext['Q']}, u^c {ext['u']}, d^c {ext['d']}; {sc}")
            w(f"          as general complex matrices these zeros leave {gc['magnitudes']} magnitudes +"
              f" {gc['phases']} phases = {gc['parameters']} parameters for 10 observables:"
              f" {gc['predictions']} predictions")
    all_sv = [sv for e in sy.values() for sv in e["survivors"]]
    found = [sv["symmetry"] for sv in all_sv if sv["symmetry"] is not None]
    none_minimal = all(m["with_zeros_and_mixing"] == 0 for e in sy.values() for m in e["minimal_scan"])
    no_herm = not any(e["hermitian_possible"] for e in sy.values())
    max_pred = max(sv["general_count"]["predictions"] for sv in all_sv) if all_sv else None
    if none_minimal and no_herm and (max_pred is None or max_pred < 1):
        w("  RESULT: no flavour symmetry inside 3-3-1 produces the survivor as a predictive model.")
    else:
        w("  RESULT: see E1-E3; at least one route is open.")
    w(f"    * with the minimal scalars, abelian symmetries make no zero that keeps three-family")
    w(f"      mixing (E1: {'none found' if none_minimal else 'some found'} for N <= {nmax});")
    if found:
        nmin = min(f["N"] for f in found)
        tmin = min(f["triplets"] for f in found)
        w(f"    * with extra scalars, Z_{nmin} and {tmin} triplets give exactly the survivor's zeros, but the")
        w(f"      matrices are then general, not Hermitian, and make {max_pred} predictions (E3);")
    w("    * the survivor's one prediction comes from Hermiticity, which needs a symmetry that")
    w("      exchanges left- and right-handed quarks: not possible with SU(3)_L acting on one side")
    w("      only (E2). It needs a left-right extension of the gauge group, which is outside 3-3-1.")
    w("")
    w("PART F. DOES ANY TEXTURE OF GENERAL MASS MATRICES PREDICT THE CKM MATRIX?")
    w("-" * 78)
    cl = res["closure"]
    w("  Every zero pattern of two general 3x3 mass matrices. Physical parameters = exact rank of")
    w("  the Jacobian of 10 weak-basis invariants of H = M M^dag (6 masses, 4 mixing invariants).")
    w(f"    {cl['ordered_pairs']} ordered pairs of patterns with three nonzero masses, {cl['classes']} classes")
    w(f"    {cl['no_three_family_mixing']:5d} cannot mix all three families (measured: all nine |V_ij| nonzero)")
    w(f"    {cl['no_phase']:5d} have no phase left, so J = 0 (measured: J = 3.12e-5)")
    w(f"    {cl['candidates']:5d} candidates; physical parameters (rank) per class: "
      + ", ".join(f"rank {k}: {v}" for k, v in sorted(cl["rank"].items(), reverse=True)))
    w(f"    {cl['rank_certified']:5d} of these ranks proved (exact lower bound = symmetry upper bound),"
      f" {len(cl['rank_open'])} open")
    w(f"    {cl['cp_impossible']:5d} of the classes with rank below 10 have J = 0 identically"
      " (symbolic expansion)")
    w(f"    {len(cl['predictive_with_cp']):5d} make a prediction and allow CP violation")
    if not cl["predictive_with_cp"] and not cl["rank_open"]:
        w("  RESULT (proved): no texture-zero pattern of general quark mass matrices predicts")
        w("    an equality. Every viable pattern has exactly as many physical parameters as there")
        w("    are observables (10), so zeros alone, however a symmetry makes them, fix nothing.")
        w("    Scope: this is a statement about relations. A rank-10 pattern can still fail to")
        w("    reach the measured values (an inequality); that is not tested here.")
    w("")
    w("PART G. OTHER GAUGE FRAMEWORKS")
    w("-" * 78)
    sc_all = res["scales"]
    par = [r for r in res["survey"][sc_all[0]]["classes"] if r["status"] == "tested" and r["zeros_u"] == r["zeros_d"]]
    par_surv = [r for r in par if all(next(x for x in res["survey"][mu]["classes"]
                                           if (x["zeros_u"], x["zeros_d"]) == (r["zeros_u"], r["zeros_d"]))["survives"]
                                      for mu in sc_all)]
    w("  Standard Model with any number of Higgs doublets: an abelian symmetry makes zeros in")
    w("    general matrices; Part F: none of those predicts anything.")
    w("  Left-right symmetric model with parity: Yukawa matrices are Hermitian, but every")
    w("    bidoublet feeds both sectors (M_u and M_d mix the same couplings through its two")
    w("    vevs), so zeros sit in the same places in up and down: parallel textures.")
    w(f"    Part C tested {len(par)} parallel Hermitian classes with a prediction;"
      f" {len(par_surv)} survive at every scale.")
    w("  RESULT: texture zeros calculate no CKM number in the Standard Model, in left-right")
    w("    models or in 3-3-1, with abelian flavour symmetries.")
    w("-" * 78)
    w("  * Hermitian textures (B, C): one pattern survives, with one prediction.")
    w("  * Inside 3-3-1 no symmetry can make mass matrices Hermitian (E2), and with its own")
    w("    scalars no abelian symmetry makes a usable zero (E1).")
    w("  * Zeros in general matrices, the only kind a symmetry inside 3-3-1 can make, never")
    w("    predict anything (F).")
    w("  * In the Standard Model and in left-right models the same holds (G).")
    w("  So with abelian flavour symmetries and any number of scalars, in all three frameworks, the quark")
    w("  sector closes with 10 measured inputs: 6 masses and 4 CKM parameters. None of the")
    w("  four CKM numbers can be calculated from zeros. Calculating them needs relations")
    w("  between nonzero entries (non-abelian flavour symmetries or grand unification),")
    w("  which this script does not search.")
    w("")
    w("PART H. WHERE QUANTUM THEORY AND GRAVITY MEET (established physics)")
    w("-" * 78)
    qg = res["quantum_gravity"]
    pl = qg["planck"]
    w("  H1. Planck units from G, hbar, c, k_B")
    w(f"      l_P = {pl['l_P_m']:.4e} m   t_P = {pl['t_P_s']:.4e} s   m_P = {pl['m_P_kg']:.4e} kg"
      f"   E_P = {pl['E_P_GeV']:.4e} GeV   T_P = {pl['T_P_K']:.4e} K")
    nw = qg["newton"]
    w("  H2. Newton's law with its one-loop quantum correction (gravity as an effective field theory)")
    w("      V = -G m1 m2 / r [1 + 3 G (m1+m2)/(r c^2) + (41/10pi) G hbar/(r^2 c^3)]")
    w(f"      coefficient 41/(10 pi) = {nw['coefficient']:.5f}  [quoted: Bjerrum-Bohr, Donoghue, Holstein 2003]")
    w(f"      Sun-Earth at 1 au: relativistic term {nw['classical_rel_sun_earth']:.2e},"
      f" quantum term {nw['quantum_rel_sun_earth']:.2e}")
    w(f"      for two protons the quantum term overtakes the relativistic one below r = {nw['r_equal_two_protons_m']:.2e} m"
      f" ({nw['r_equal_two_protons_m'] / nw['proton_compton_m']:.3f} proton Compton lengths)")
    w(f"      the quantum term reaches 1 (the effective theory ends) at r = {nw['r_breakdown_m']:.2e} m"
      f" = {nw['r_breakdown_m'] / pl['l_P_m']:.3f} l_P")
    w("  H3. Black holes and horizons (Hawking, Bekenstein)")
    for name, bh in qg["black_holes"].items():
        label = "the Sun's mass" if name == "sun" else "mass evaporating in exactly the age of Part A"
        w(f"      {label}: M = {bh['mass_kg']:.4e} kg, r_s = {bh['r_s_m']:.4e} m, T_H = {bh['T_H_K']:.4e} K,"
          f" S = {bh['S_BH_kB']:.4e} k_B, t_evap = {bh['t_evap_s'] / (31557600 * 10 ** 9):.4e} Gyr")
    ds = qg["de_sitter"]
    w(f"      de Sitter horizon of the Part A cosmology: T = {ds['T_dS_K']:.4e} K,"
      f" S = A/(4 l_P^2) = {ds['S_area_law_kB']:.4e} k_B")
    w("      (t_evap counts photon emission only; more particle species shorten it)")
    un = qg["unruh"]
    w("  H4. Unruh effect: an accelerated observer sees the vacuum as thermal")
    w(f"      at g = {un['g_earth']:.4f} m/s^2: T = {un['T_at_g_K']:.4e} K;  1 K needs a = {un['a_for_1K']:.4e} m/s^2")
    en = qg["entanglement"]
    w("  H5. The smallest mass that gravity can ever entangle maximally (two masses, each in two places)")
    w("      limits: entangling phase pi (concurrence 1); time <= age of the universe (Part A);")
    w("      separation >= the Compton wavelength hbar/(m c). Then m >= (pi hbar^2 / (G c t0))^(1/3).")
    w(f"      m_min = {en['m_min_kg']:.4e} kg = {en['m_min_MeV']:.1f} MeV/c^2 = {en['m_min_over_m_p']:.3f} m_p,"
      f" at separation {en['d_min_m']:.3e} m")
    w(f"      check: phase {en['entangling_phase_rad']:.6f} rad, concurrence {en['concurrence']:.6f},"
      f" entropy {en['entropy_bits']:.6f} bits")
    w("      Anything lighter cannot be fully entangled by gravity in the lifetime of the universe.")
    w("      A classical gravitational field cannot entangle at all (concurrence 0): measuring")
    w("      gravity-made entanglement in any system is the open test of whether gravity is quantum.")
    tr = qg["transmutation"]
    w("  H6. Why gravity is so weak for a proton: the strong scale comes from logarithmic running")
    w(f"      alpha_s(M_P) = {tr['alpha_s_at_M_P']:.5f} (Standard Model running to M_P, no new physics assumed)")
    w(f"      Lambda_QCD(5 flavours, 2-loop) = {tr['Lambda5_GeV']:.4f} GeV;  ln(M_P/Lambda) = {tr['ln_MP_over_Lambda']:.2f};"
      f"  one-loop 2pi/(b0 alpha_s(M_P)) = {tr['one_loop_2pi_over_b0_alpha']:.2f}")
    w(f"      m_p / Lambda = {tr['m_p_over_Lambda']:.2f}: the proton mass is set by Lambda (computing it needs lattice QCD)")
    nb = qg["numbers"]
    w("  H7. Dimensionless numbers, each with its status")
    rows = [
        ("alpha (electromagnetic coupling)", nb["alpha"], "measured input; not derived by any theory"),
        ("alpha_G (proton) = G m_p^2/(hbar c)", nb["alpha_G_proton"], "= (m_p/M_P)^2 exactly; small because of H6"),
        ("alpha_G (electron)", nb["alpha_G_electron"], "the electron mass is a Higgs coupling: not derived"),
        ("m_p / m_e", nb["m_p_over_m_e"], "QCD scale over a Yukawa coupling: not derived"),
        ("electric/gravitational force, p-e", nb["electric_over_gravity_p_e"], "= alpha hbar c/(G m_p m_e): follows from rows above"),
        ("Hubble radius / proton Compton length", nb["hubble_radius_over_proton_compton"],
         "Dirac's large number; its closeness to 1/alpha_G is unexplained"),
        ("rho_Lambda / rho_Planck", nb["rho_Lambda_over_rho_P"], "the cosmological-constant problem: open"),
        ("S_dS x rho_Lambda / rho_Planck", nb["S_dS_times_rho_ratio"], "= 3/8 exactly: the 10^122 and 10^-123 are one fact"),
        ("(hbar^2 H0/(G c))^(1/3) / m_pi", nb["weinberg_over_m_pi"], "Weinberg 1972: same order as 1; unexplained"),
        ("H5 smallest entangled mass / m_pi", nb["m_min_entangle_over_m_pi"],
         "same combination as Weinberg's (t0 ~ 1/H0)"),
    ]
    for name, val, status in rows:
        w(f"      {name:<38} {val:12.4e}   log10 {math.log10(val):8.2f}   {status}")
    w("  RESULT: every number above is calculated from G, hbar, c, k_B and measured masses. Two of")
    w("    the apparent large-number coincidences are exact identities (alpha_G = (m_p/M_P)^2 and")
    w("    S_dS rho_Lambda/rho_P = 3/8). One has a known mechanism (the proton/Planck hierarchy from")
    w("    logarithmic running). Open: alpha, the Yukawa couplings, rho_Lambda, and whether gravity")
    w("    carries entanglement (H5) - the measurement that would decide if gravity is quantum.")
    w(f"    A coincidence to watch: the smallest mass gravity can entangle within the age of the universe")
    w(f"    (H5) is {nb['m_min_entangle_over_m_pi']:.2f} m_pi - the same combination of hbar, G, c and the Hubble")
    w("    time as Weinberg's 1972 large-number relation. Same order of magnitude, no known mechanism.")
    w("")
    w("PART I. CAN ALPHA BE CALCULATED FROM THE OTHER NUMBERS?")
    w("-" * 78)
    au = res["alpha_unification"]
    w("  No accepted theory derives alpha. Grand unification relates it to other measured numbers:")
    w("  if the three gauge couplings meet at one scale, 1/alpha(M_Z) follows from alpha_s(M_Z) and")
    w("  sin^2 theta_W(M_Z) alone. The script solves for the alpha at which they meet, running at")
    w("  one and two loops (coefficients from the field content). Superpartner scale M_S unknown:")
    w("  scanned. Unknown threshold corrections (superpartner spectrum, GUT particles): not included.")
    w(f"    measured 1/alpha(M_Z), MS-bar: {au['measured_inv_alpha_MZ']} +/- {au['measured_sigma']}")
    w("    content                     1/alpha(M_Z) 1-loop   2-loop (+/- inputs)     M_GUT (GeV)   1/alpha_GUT")
    for row in au["rows"]:
        name = (f"MSSM above M_S = {row['M_S']:.3g} GeV" if math.isfinite(row["M_S"])
                else "Standard Model only")
        l1, l2 = row["loop1"], row["loop2"]
        w(f"    {name:<30} {l1['inv_alpha']:9.2f}        {l2['inv_alpha']:8.2f} +/- {l2['sigma_inputs']:.2f}"
          f"      {l2['M_GUT']:.2e}     {1 / l2['alpha_GUT']:.2f}")
    sm_row = [r for r in au["rows"] if not math.isfinite(r["M_S"])][0]
    miss = sm_row["loop2"]["inv_alpha"] / au["measured_inv_alpha_MZ"] - 1
    w(f"  Standard Model: forcing unification gives 1/alpha = {sm_row['loop2']['inv_alpha']:.1f},"
      f" {100 * miss:+.0f}% from the measurement. The SM couplings do not meet.")
    ms = au.get("M_S_for_measured_alpha")
    if ms:
        w(f"  MSSM: the prediction slides with the unknown M_S by {ms['slope_per_efold']:.2f} per e-fold. It equals")
        w(f"    the measured alpha at M_S = {ms['M_S_GeV'] / 1000:.2f} TeV ({ms['low_GeV'] / 1000:.2f} to"
          f" {ms['high_GeV'] / 1000:.2f} TeV from the alpha_s and sin^2 theta_W errors alone),")
        w(f"    with unification at M_GUT = {ms['M_GUT_GeV']:.3e} GeV, 1/alpha_GUT = {1 / ms['alpha_GUT']:.2f}."
          " Parts B, C and J use these scales.")
    w("  Numerology: closed formulas proposed for 1/alpha(0), tested against CODATA 2018")
    for c_ in res["alpha_numerology"]:
        w(f"    {c_['formula']:<48} {c_['value']:.7f}   off by {c_['n_sigma']:.2e} sigma")
    w(f"    CODATA 2018: 1/alpha = {1 / inp('alpha_em'):.9f}")
    w("  RESULT: alpha is not calculated. Unification turns it into a function of one unknown, the")
    w("    superpartner scale; equivalently, the measured alpha points to M_S of a few TeV in the MSSM")
    w("    (before unknown threshold corrections). The SM alone cannot unify, and every closed")
    w("    formula tested is excluded by thousands of standard deviations or more. Getting from")
    w("    alpha(M_Z) to alpha(0) also needs the hadronic vacuum polarization, a measured input.")
    w("")
    w("PART J. CAN THE YUKAWA COUPLINGS BE CALCULATED FROM THE OTHER NUMBERS?")
    w("-" * 78)
    yk = res["yukawa"]
    ra = yk["ratios"]
    w("  J1. Quark/lepton mass ratios fixed by grand unification (group theory, at the unification")
    w("      scale; same-charge ratios hardly run, so they can be compared at m_t)")
    w(f"      measured m_s/m_d = {ra['ms_over_md']:.2f} +/- {ra['ms_over_md_sigma']:.2f};"
      f" m_mu/m_e at m_t = {ra['mmu_over_me_at_mt']:.2f}")
    w(f"      minimal SU(5), m_s/m_d = m_mu/m_e:            {ra['SU5']['predicted']:8.2f}   off by {ra['SU5']['n_sigma']:.0f} sigma")
    w(f"      Georgi-Jarlskog, m_s/m_d = m_mu/(9 m_e):      {ra['GJ']['predicted']:8.2f}   off by {ra['GJ']['n_sigma']:.1f} sigma")
    w("  J2. b-tau unification: y_b = y_tau at the unification scale (MSSM: M_GUT from Part I)")
    for p_ in yk["btau_SM"]:
        w(f"      SM at {p_['where']} ({p_['mu']:.2e} GeV): y_b/y_tau = {p_['yb_over_ytau']:.3f}")
    if yk.get("btau_MSSM"):
        lo_, hi_ = yk["tan_beta_range"]
        w(f"      MSSM above M_S = {yk['M_S'] / 1000:.2f} TeV, up to M_GUT = {yk['M_GUT']:.2e} GeV (both Part I);")
        w(f"      tan(beta) scanned over its perturbative"
          f" range {lo_:.2f} to {hi_:.1f}:")
        line = []
        for r_ in yk["btau_MSSM"]:
            v_ = f"{r_['yb_over_ytau']:.3f}" if math.isfinite(r_["yb_over_ytau"]) else "n.p."
            line.append(f"{r_['tan_beta']:.3g}: {v_}")
        for i in range(0, len(line), 6):
            w("        " + "   ".join(line[i:i + 6]))
        w("        (y_b/y_tau at the unification point; n.p. = a coupling leaves perturbation theory)")
        u_ = yk.get("btau_MSSM_unity")
        if u_:
            w(f"      y_b/y_tau = 1 only at tan(beta) = {u_['tan_beta']:.3f}, where y_t(M_GUT) = {u_['yt_GUT']:.2f}:"
              f" the edge of perturbation theory")
    fs = yk["fixed_point_SM"]
    w("  J3. Top quasi-fixed point: a large y_t at high scale is driven to a value set by the gauge couplings")
    for r_ in fs["runs"]:
        w(f"      SM, y_t = {r_['yt_start']:.2f} at M_Planck -> m_t(m_t) = {r_['mt_msbar']:.1f} GeV")
    w(f"      measured m_t(m_t) = {fs['measured_mt_msbar']:.1f} GeV")
    if yk.get("fixed_point_MSSM"):
        for r_ in yk["fixed_point_MSSM"]["runs"]:
            w(f"      MSSM, y_t = {r_['yt_start']:.2f} at M_GUT (Part I):"
              f" the measured top mass needs tan(beta) = {r_['tan_beta']:.3f}")
    w("  RESULT: no Yukawa coupling is calculated. Minimal SU(5) and Georgi-Jarlskog mass ratios are")
    w("    excluded. In the SM, b-tau unification and the top fixed point both fail.")
    if yk.get("btau_MSSM_unity") and yk.get("fixed_point_MSSM"):
        tbs = [r_["tan_beta"] for r_ in yk["fixed_point_MSSM"]["runs"]]
        w(f"    In the MSSM (scales from Part I), b-tau unification needs tan(beta) ="
          f" {yk['btau_MSSM_unity']['tan_beta']:.2f} and the top fixed point")
        w(f"    gives tan(beta) = {min(tbs):.2f} to {max(tbs):.2f}: the same narrow region, at the edge of"
          " perturbation theory.")
        w("    That is one number (tan beta), not a calculation of the Yukawas. Part K tests it against")
        w("    the Higgs mass.")
    w("")
    hg = res.get("higgs")
    if hg:
        mh, mh_up, _ = _comparison("m_h")
        w("PART K. THE HIGGS MASS IN THE MSSM, FROM THE SCALES OF PARTS I AND J")
        w("-" * 78)
        w("  In the MSSM the Higgs self-coupling is not free: at M_S it is fixed by the gauge couplings,")
        w("  tan(beta) and the stop mixing X_t. Effective theory: lambda(M_S) = (g^2 + g'^2)/4 cos^2(2 beta)")
        w("  + (3 y_t^4 / 8 pi^2) X^2 (1 - X^2/12), X = X_t/M_S; SM running of lambda down to m_t; m_h = sqrt(lambda) v.")
        w(f"  Inputs from the algorithm: M_S = {hg['M_S'] / 1000:.2f} TeV ({hg['M_S_range'][0] / 1000:.2f} to"
          f" {hg['M_S_range'][1] / 1000:.2f}, Part I);")
        w(f"  tan(beta) = {min(hg['tan_betas']):.3f} to {max(hg['tan_betas']):.3f} (Part J: b-tau unification and the top fixed point).")
        w("  X_t is unknown: scanned. The threshold is largest at X^2 = 6, so maximal mixing bounds m_h from above.")
        w("      M_S (TeV)   tan(beta)   m_h, no mixing   m_h, maximal mixing  (GeV)")
        for r_ in hg["rows"]:
            w(f"      {r_['M_S'] / 1000:7.2f}     {r_['tan_beta']:7.3f}      {r_['mh_no_mixing']:8.1f}          {r_['mh_max_mixing']:8.1f}")
        w(f"      m_h against X_t/M_S at M_S = {hg['M_S'] / 1000:.2f} TeV, tan(beta) = {max(hg['tan_betas']):.3f}:")
        line = [f"{x_:.2f}: {m_:.1f}" if math.isfinite(m_) else f"{x_:.2f}: unstable" for x_, m_ in hg["xt_curve"]]
        for i in range(0, len(line), 5):
            w("        " + "   ".join(line[i:i + 5]))
        gap_ = mh - hg["mh_upper_bound"]
        w(f"  Upper bound over every mixing and the whole M_S, tan(beta) range: m_h <= {hg['mh_upper_bound']:.1f} GeV")
        w(f"      measured m_h = {mh:.2f} +/- {mh_up:.2f} GeV: the bound is {gap_:.1f} GeV short")
        need = ms_for_higgs_mass(res["flavour"], max(hg["tan_betas"]), mh)
        if math.isfinite(need):
            w(f"  Read backwards: at tan(beta) = {max(hg['tan_betas']):.3f} and maximal mixing, m_h = {mh:.1f} GeV needs"
              f" M_S = {need:.2e} GeV,")
            w(f"      {math.log(need / hg['M_S']):.1f} e-folds above Part I's M_S.")
        w("  Not included: two-loop thresholds and the pole-to-MS-bar Higgs-mass conversion (a few GeV in")
        w("  the literature), heavy-Higgs and gaugino thresholds. None closes a gap of this size.")
        w("  RESULT: the MSSM route of Parts I and J is excluded by the Higgs mass. The superpartner scale")
        w("    that gives the measured alpha and the tan(beta) that gives b-tau unification together")
        w(f"    predict m_h <= {hg['mh_upper_bound']:.0f} GeV. Unification (Part I), b-tau unification and the top")
        w("    fixed point (Part J) cannot all hold in the minimal model with one superpartner scale.")
        w("")
    cr = res.get("criticality")
    if cr:
        mh, mh_up, _ = _comparison("m_h")
        c_ = cr["central"]
        w("PART L. STANDARD MODEL CRITICALITY: THE HIGGS MASS FROM ONE CONDITION AT THE PLANCK SCALE")
        w("-" * 78)
        w("  If nothing new enters below the Planck scale, the Higgs self-coupling can be fixed there:")
        w("  lambda(M_P) = 0 (Froggatt-Nielsen 1996; Shaposhnikov-Wetterich 2010). Running it down to m_t")
        w("  with the measured top mass and alpha_s then predicts m_h. No free parameter, no new particle.")
        w("  Running: one, two and three loops (two-loop gauge b_ij from the field content; y_t and lambda")
        w("  two-loop terms and all three-loop terms quoted from Buttazzo et al. 2013, appendix B). Matching")
        w("  to the pole masses M_h, M_t, M_W, M_Z and G_F: tree level; one loop at mu = m_t(m_t) (their")
        w("  appendix A, Passarino-Veltman functions in closed form); two loops at mu = M_t (their section 2")
        w("  interpolations of lambda^(2) and of the electroweak parts of y_t^(2)); three loops: the leading")
        w("  QCD part of lambda^(3) (their footnote, from Martin 2013). QCD: alpha_s and the quark masses run")
        w("  at four loops with three-loop decoupling (RunDec), the top pole/MS-bar conversion at four loops")
        w("  (Melnikov-van Ritbergen 2000, Marquard et al. 2015).")
        w("      condition                 loops   matching            predicted M_h (GeV)")
        for r_ in cr["rows"]:
            w(f"      lambda({r_['scale']:<11}) = 0       {r_['loops']}      {r_['matching']:18s}  {r_['m_h']:8.2f}")
        si = cr["sigma_inputs"]
        rw = cr["row"]
        sm_ = cr["smdr"]
        w("  Anchored to SMDR (Martin-Robertson 2019: full two-loop plus leading three-loop matching, four-loop")
        w("  QCD) at its reference point. Couplings at Q0 = 173.1 GeV for SMDR's inputs, this script vs SMDR:")
        w("      " + "   ".join(f"{k} {sm_['ours'][k]:.5f} / {sm_['smdr'][k]:.5f}" for k in ("lambda", "y_t", "g3")))
        w("      " + "   ".join(f"{k} {sm_['ours'][k]:.5f} / {sm_['smdr'][k]:.5f}" for k in ("g2", "gp")))
        w("  The differences (this script's missing electroweak and mixed thresholds and its simpler")
        w("  electroweak inputs) are added at M_t; this script's own matching carries them to the inputs.")
        w(f"  Three-loop running, SMDR-anchored matching, four-loop QCD: M_h = {c_['m_h']:.2f} GeV +/-"
          f" {cr['sigma_total']:.2f}")
        w(f"      (inputs: M_t {si['M_t']:+.2f}, alpha_s {si['alpha_s_MZ']:+.2f}, M_W {si['M_W']:+.3f})")
        cm_ = c_["m_h"]
        own = rw["3L/three loops"]["m_h"]
        w(f"      against this script's own three-loop matching ({own:.2f} GeV): {cm_ - own:+.2f} GeV. Last orders of")
        w(f"      its own calculation: running (3 loops vs 2) {own - rw['2L/three loops']['m_h']:+.2f} GeV, matching"
          f" (3 vs 2) {own - rw['3L/two loops']['m_h']:+.2f} GeV,")
        w(f"      QCD running, decoupling and top mass (4 loops vs 3) {own - rw['3L/three loops, QCD 3']['m_h']:+.2f}"
          " GeV")
        w(f"      measured M_h = {mh:.2f} +/- {mh_up:.2f} GeV: the prediction is {c_['m_h'] - mh:.1f} GeV high,"
          f" {(c_['m_h'] - mh) / math.hypot(cr['sigma_total'], mh_up):.1f} sigma on the input errors")
        bz = cr["buttazzo"]
        w(f"      cross-check at Buttazzo et al.'s own order (two-loop matching, QCD at three loops):"
          f" {rw['3L/two loops, QCD 3']['m_h']:.2f} GeV;")
        w(f"      their lambda(M_Pl), linear in M_h, M_t, alpha_s, gives {bz['mh_linear']:.2f} GeV here")
        w("      This script's own three-loop matching is its leading QCD part (lambda: O(alpha_s^2 y_t^4); y_t:")
        w("      pure QCD, to four loops); the anchor adds SMDR's full two loops and leading three loops. Not")
        w("      included: the rest of three-loop matching, and four-loop running beyond pure QCD.")
        d_ = cr["double"]
        w("  Both conditions at the Planck scale, lambda(M_P) = 0 and beta_lambda(M_P) = 0, fix two numbers")
        w("  (at two loops, one-loop matching):")
        w(f"      M_h = {d_['m_h']:.1f} GeV and M_t = {d_['M_t']:.1f} GeV"
          f" (measured {mh:.1f} and {inp('M_t'):.2f}; QCD pole/MS-bar ratio of the measured top kept)")
        pr = sm_lambda_profile(cr, mh)
        w(f"  Read backwards, with the measured M_h (Part L's central order): lambda(M_P) = {pr['lambda_MP']:+.4f},"
          f" beta_lambda(M_P) = {pr['beta_MP']:+.1e}")
        if math.isfinite(pr["mu_zero"]):
            w(f"      lambda turns negative at mu = {pr['mu_zero']:.2e} GeV: the electroweak vacuum is not the")
            w("      lowest state. Whether it is long-lived (metastable) needs the tunnelling rate, not")
            w("      calculated here.")
        w(f"  RESULT: one condition at the Planck scale gives the Higgs mass to"
          f" {100 * abs(c_['m_h'] / mh - 1):.0f} percent with nothing adjusted:")
        w(f"    {c_['m_h']:.1f} GeV against {mh:.2f}. Against two-loop running with one-loop matching (same QCD),")
        w(f"    the higher orders move it by {c_['m_h'] - cr['two_loop_one_loop']['m_h']:+.2f} GeV and do not close"
          " the gap: the measured Higgs mass makes lambda slightly")
        w("    negative at M_P and the SM vacuum is not stable. The top mass dominates the input error; the")
        w("    second condition (beta_lambda = 0) lands near the measured top mass.")
        w("")
    jt = res["joint"]
    w("PART M. WHICH HIGH-ENERGY HYPOTHESIS SURVIVES EVERY CONDITION AT ONCE?")
    w("-" * 78)
    w("  The field content above the electroweak scale is not chosen. Each hypothesis is tested")
    w("  against every combination of the conditions the other parts impose:")
    w("    U  gauge unification      predicts 1/alpha(M_Z)")
    w("    B  b-tau unification      predicts y_b/y_tau = 1 at M_GUT (SM: where g1 = g2)")
    w("    H  Higgs mass             SM: lambda(M_P) = 0 (Part L); MSSM: matching at M_S (Part K)")
    w("  SM up to M_P has no unknowns. The MSSM has M_S, tan(beta) and the stop mixing X_t. M_S is")
    w("  scanned on a grid plus where unification gives the measured alpha; tan(beta) on a grid plus")
    w("  every root of y_b/y_tau = 1 and every edge of perturbation theory (bisection); X_t is")
    w(f"  eliminated exactly. {jt['MSSM_points']} perturbative points; the best one only decides survival.")
    w("  With no prediction (dof <= 0) the number is the distance in sigma between the data and")
    w("  everything the hypothesis can reach. Two error sets bracket every verdict:")
    w("    inputs           measured inputs only: the strongest exclusion")
    w("    +theory          plus, per ingredient, the change from the last order calculated to the")
    w("                     one below (running 2 loops vs 1, matching one loop vs tree); the next")
    w("                     order is usually smaller, so this is the weakest exclusion")
    th, tm = jt["SM_theory_sigma"], jt.get("MSSM_theory_sigma_at_part_I")
    w(f"  Theory errors, SM:   1/alpha {th['U']:.2f}   y_b {100 * th['B']:.1f} %   m_h {th['H']:.2f} GeV"
      " (from Parts I, J, L)")
    if tm:
        w(f"  Theory errors, MSSM at M_S = {_fmt(tm['M_S'] / 1000, 3)} TeV:   1/alpha {tm['U']:.2f}   y_b"
          f" {100 * tm['B']:.1f} %   m_h {tm['H']:.2f} GeV")
    w("  Not estimated: the two-loop stop threshold, GUT and superpartner thresholds.")
    sp, st_ = jt["SM_pulls"], jt["SM_pulls_theory"]
    w(f"  SM pulls, inputs:  U {sp['U']:+.1f}  B {sp['B']:+.1f}  H {sp['H']:+.1f} sigma;"
      f"  +theory:  U {st_['U']:+.1f}  B {st_['B']:+.1f}  H {st_['H']:+.2f} sigma")
    w("    hypothesis        conditions  unknowns  dof  |  sigma   verdict    |  sigma   verdict")
    w("                                                 |  (inputs)           |  (+theory)")

    def verdict(v: Dict[str, Any]) -> str:
        return ("predicts" if v["predicts"] else "survives") if v["survives"] else "excluded"

    for r in jt["rows"]:
        cols = []
        for v in (r, r["with_theory"]):
            zero = v["chi2"] < num("joint_chi2_zero")
            cols.append(f"{'0' if zero else _fmt(v['n_sigma'], 3):>7s}   {verdict(v):9s}")
        w(f"    {r['hypothesis']:17s} {'+'.join(r['conditions']):10s} {r['unknowns']:5d} {r['dof']:6d}"
          f"  | {cols[0]}  | {cols[1]}".rstrip())
    w("    (survives: no prediction, the unknowns absorb the conditions; predicts: survives and")
    w("    predicts at least one number)")
    for label, key in (("inputs only", "predictive_survivors"), ("with theory errors", "predictive_survivors_theory")):
        preds = jt[key]
        w(_wrap(f"RESULT ({label}): " + ("survives and predicts: " + "; ".join(
            f"{h} with {'+'.join(c)}" for h, c in preds) if preds else
            "no hypothesis and set of conditions both survives and predicts anything."), 2))
    flips = [r for r in jt["rows"] if r["survives"] != r["with_theory"]["survives"]]
    if flips:
        w(_wrap("Verdicts that depend on the theory errors: " + "; ".join(
            f"{r['hypothesis']} with {'+'.join(r['conditions'])}" for r in flips)
            + ". Deciding them needs the next order, not a different error estimate.", 4))
    w("")
    mf = res["mass_formulas"]
    w("PART N. CAN THE QUARK AND LEPTON MASSES BE CALCULATED? CLOSED MASS FORMULAS")
    w("-" * 78)
    w("  Part J tested what grand unification relates. Left to test are closed formulas for the masses")
    w("  themselves, as Part I tests them for 1/alpha. Koide (1982): Q = (m1 + m2 + m3)/(sqrt m1 + sqrt m2")
    w("  + sqrt m3)^2 = 2/3. No accepted theory derives it; Q lies between 1/3 (equal) and 1 (one mass).")
    w("  A mass relation needs a scale: pole masses are not the couplings of a Lagrangian at one scale,")
    w("  and running masses change their ratios with mu.")
    w("      masses                                                        Q           off by")
    for r_ in mf["koide"]:
        w(f"      {r_['set']:<58s} {r_['Q']:.7f} +/- {_fmt(r_['sigma'], 2):<8s} {r_['n_sigma']:7.1f} sigma")
    w(f"  Q = 2/3 at pole masses, solved for m_tau from m_e and m_mu: {mf['koide_m_tau_MeV']:.3f} MeV"
      f" (measured {mf['m_tau_MeV']:.2f} +/- {mf['m_tau_sigma_MeV']:.2f})")
    w(f"  Running from the pole masses to M_Z moves Q by {mf['koide_running_shift']:.2e}, about"
      f" {mf['koide_running_shift'] / mf['koide_pole_sigma']:.0f} times its error;")
    w(f"  alpha(0) or alpha(M_Z) in the QED running changes that by {mf['koide_qed_alpha_spread']:.1e}.")
    kr = mf["koide"]
    w(_wrap(f"RESULT: Koide's relation holds for the charged-lepton pole masses ({kr[0]['n_sigma']:.1f} sigma), but at "
            f"no scale where the masses are couplings: at M_Z it fails by {min(r_['n_sigma'] for r_ in kr[1:3]):.0f} "
            f"sigma or more, and for the quarks at m_t(m_t) by {min(r_['n_sigma'] for r_ in kr[3:]):.0f} sigma or "
            "more. A relation that holds only for pole masses has no known mechanism; it stays a coincidence "
            "to watch. No quark or lepton mass is calculated.", 2))
    w("")
    sc = res["strong_cp"]
    bd = sc["bound"]
    w("PART O. THE STRONG CP ANGLE THETA-BAR")
    w("-" * 78)
    w("  QCD allows theta (g^2/32 pi^2) G G~, which violates P and CP. Only theta-bar = theta - arg det(M_u M_d)")
    w("  is physical, and the Standard Model gives it no value. It would give the neutron an electric")
    w("  dipole moment.")
    w("  O1. d_n per unit theta-bar, leading chiral logarithm (Crewther, Di Vecchia, Veneziano, Witten 1979):")
    w("      g0 = delta m_N m* theta/(m-bar eps), from the strong part of m_n - m_p (de Vries et al. 2015);")
    w("      d_n = e g_piNN [g0/(2 F_pi)] ln(m_N/m_pi) / (4 pi^2 m_N), g_piNN = g_A m_N/F_pi (Goldberger-Treiman)")
    w(f"      eps = (m_d - m_u)/(m_d + m_u) = {bd['eps']:.3f}; g0/(2 F_pi) = ({1000 * bd['gbar']:.1f} +/-"
      f" {1000 * bd['gbar_sigma']:.1f}) x 10^-3 theta-bar; g_piNN = {bd['g_piNN']:.2f}; ln(m_N/m_pi) = {bd['chiral_log']:.3f}")
    w(f"      d_n = ({bd['d_n_per_theta'] * 1e16:.2f} +/- {bd['d_n_per_theta_sigma'] * 1e16:.2f}) x 10^-16 theta-bar e cm"
      " (input errors; the counterterm beside the log is unknown)")
    for r_ in bd["literature"]:
        w(f"      {r_['method']:<32s} ({r_['d_n_per_theta'] * 1e16:.2f} +/- {r_['sigma'] * 1e16:.2f}) x 10^-16 theta-bar e cm")
    w(f"      measured: |d_n| < {_fmt(bd['d_n_limit'], 2)} e cm (90% CL)  ->  |theta-bar| < {bd['theta_max']:.1e}"
      f" (chiral log); < {bd['theta_max_weakest']:.1e} with the")
    w("      weakest coefficient above, each lowered by its 1 sigma error")
    mu_ = sc["massless_up"]
    w("  O2. The explanations proposed, each tested:")
    w(f"      a. massless up quark (theta-bar unphysical): m_u = {1000 * mu_['m_u_GeV']:.2f} +/-"
      f" {1000 * mu_['sigma']:.2f} MeV, {mu_['n_sigma']:.0f} sigma from zero;")
    w(f"         m_u/m_d = {mu_['z']:.3f} +/- {mu_['z_sigma']:.3f}. Excluded.")
    ax = sc["axion"]
    w("      b. axion (Peccei-Quinn): theta-bar relaxes to zero, at the cost of a new scale f_a.")
    w(f"         m_a f_a = sqrt(z)/(1 + z) m_pi0 F_pi = {ax['ma_fa_MeV2']:.0f} +/- {ax['ma_fa_sigma']:.0f} MeV^2:"
      f" m_a = {ax['m_a_ueV_at_1e12']:.2f} +/- {ax['m_a_ueV_at_1e12_sigma']:.2f} micro-eV x (1e12 GeV/f_a)")
    w(f"         (leading order; NLO with lattice input: {ax['nlo_ueV']:.2f} +/- {ax['nlo_sigma']:.2f},"
      f" {100 * ax['lo_minus_nlo_rel']:+.1f} %). At the algorithm's scales:")
    for r_ in ax["at_scales"]:
        w(f"           f_a = {r_['f_a']:<15s} = {r_['f_a_GeV']:.2e} GeV  ->  m_a = {r_['m_a_eV']:.2e} eV")
    w("         One unknown (f_a) replaces one (theta-bar): a parameter trade, not a calculation.")
    w("      c. parity: if a symmetry makes M_u and M_d Hermitian and sets theta = 0, then det M is real")
    w("         and arg det(M_u M_d) is 0 or pi. Flipping the sign of a sector's matrix keeps V (same")
    w("         eigenvectors) and flips its det (3 x 3), so theta-bar = 0 at tree level is always reachable.")
    for r_ in sc["parity"]:
        sg = {k: "".join("+" if s_ > 0 else "-" for s_ in v["eigenvalue_signs"]) for k, v in r_["sectors"].items()}
        w(f"         Part C survivor (up {r_['up']}, down {r_['down']}): eigenvalue signs up {sg['u']}, down"
          f" {sg['d']}; arg det(M_u M_d) = {'pi' if r_['arg_det_over_pi'] else '0'}")
    w("         as found (heaviest eigenvalue positive), so theta-bar = 0 needs " +
      ("no sign flip." if all(r_["arg_det_over_pi"] == 0 for r_ in sc["parity"]) else "one sector's sign flipped."))
    w("         But Hermiticity needs a left-right parity (Part E), and the textures that parity gives are")
    w("         excluded (Part G); radiative corrections then move theta-bar off zero. Not a calculation either.")
    inv = sc["sm_invariant"]
    j_meas = _comparison("J")[0]
    w("  O3. Can the SM's own CP violation make theta-bar? Only through the flavour invariant")
    w("      Im det[H_u, H_d] = 2 J prod_(i<j) (y_ui^2 - y_uj^2)(y_di^2 - y_dj^2), H = Y Y^dagger, which")
    w(f"      vanishes if any two same-charge quarks were degenerate. At m_t(m_t), with the measured J:"
      f" {j_meas * inv['mass_difference_product']:.1e}.")
    w("      Its first divergent contribution to theta-bar is at seven loops (Ellis-Gaillard 1979), so the")
    w(f"      SM's own theta-bar lies many orders below the bound {bd['theta_max']:.0e}.")
    w(f"  RESULT: theta-bar is bounded, |theta-bar| < {bd['theta_max']:.1e} (up to {bd['theta_max_weakest']:.1e}"
      " with the hadronic uncertainty),")
    w("    but not calculated. The massless-up-quark solution is excluded; the axion trades theta-bar for")
    w("    f_a and predicts m_a f_a; parity sets it to zero at tree level but needs Hermitian textures,")
    w("    and the predictive ones are excluded. Theta-bar is the one free number whose smallness the")
    w("    Standard Model's own CP violation cannot explain.")
    w("")
    nu = res["neutrinos"]
    w("PART P. NEUTRINO MASSES AND MIXING")
    w("-" * 78)
    w("  Oscillations (NuFIT 6.0) measure two mass-squared differences and the PMNS matrix. Not measured:")
    w("  the lightest mass m0, the ordering, two Majorana phases, and the origin of the masses. Each")
    w("  unknown is scanned, never set.")
    lims = {"sum_mnu_Planck": "Planck 2018", "sum_mnu_DESI": "DESI DR2 + CMB"}
    for o, rec in nu["orderings"].items():
        lab = "normal (m1 < m2 < m3)" if o == "NO" else "inverted (m3 < m1 < m2)"
        ms_ = rec["masses_at_m0_0"]
        w(f"  {o}, {lab}:")
        w(f"    P1. at m0 = 0: masses {', '.join(f'{1000 * m:.2f}' for m in ms_)} meV; sum ="
          f" {1000 * rec['sum_min']:.2f} +/- {1000 * rec['sum_min_sigma']:.2f} meV (the smallest possible)")
        for k, v_ in rec["vs_cosmology"].items():
            m0m = rec["m0_max"][k]
            tail = (f"allowed; m0 < {1000 * m0m:.1f} meV" if v_["allowed"] else
                    f"EXCLUDED at 95%: the minimum is {1000 * v_['sum_min_minus_limit']:.1f} meV above it")
            w(f"        vs {lims[k]:<15s} sum < {1000 * v_['limit']:.0f} meV (95%): {tail}")
        w(f"        Omega_nu h^2 at the minimum = {rec['Omega_nu_h2_at_min']:.2e}: {100 * rec['Omega_nu_over_Omega_m_at_min']:.2f} %"
          " of Part A's Omega_m")
        mbm = rec["m_beta_max_cosmology"]["sum_mnu_Planck"]
        w(f"    P2. m_beta = {1000 * rec['m_beta_min']:.1f} meV at m0 = 0" +
          (f", at most {1000 * mbm:.1f} meV under Planck's limit" if mbm else "") +
          f"; KATRIN: < {1000 * _comparison('m_beta_KATRIN')[0]:.0f} meV (90%)")
        lo0, hi0 = rec["m_bb_at_m0_0"]
        sl, sh = rec["m_bb_at_m0_0_sigma"]
        w(f"    P3. m_bb band over the Majorana phases at m0 = 0: {1000 * lo0:.2f} +/- {1000 * sl:.2f} to"
          f" {1000 * hi0:.2f} +/- {1000 * sh:.2f} meV")
        cz = rec["m_bb_cancellation_m0"]
        if cz:
            w(f"        m_bb can vanish (phases cancel) for {1000 * cz[0]:.2f} < m0 < {1000 * cz[1]:.2f} meV")
        else:
            w("        m_bb cannot vanish for any m0: the inverted ordering has a floor")
        mbb = rec["m_bb_max_cosmology"]["sum_mnu_Planck"]
        if mbb:
            w(f"        largest m_bb under Planck's limit: {1000 * mbb:.1f} meV")
        line = [f"{1000 * r_['m0']:.3g}: {1000 * r_['m_bb_lo']:.2f}-{1000 * r_['m_bb_hi']:.2f}" for r_ in rec["scan"][::4]]
        w("        m0 (meV): m_bb band (meV)")
        for i in range(0, len(line), 4):
            w("          " + "   ".join(line[i:i + 4]))
    klo, khi = _comparison("m_bb_KLZ_low")[0], _comparison("m_bb_KLZ_high")[0]
    io_lo, io_hi = nu["orderings"]["IO"]["m_bb_at_m0_0"]
    w(f"    KamLAND-Zen: m_bb < {1000 * klo:.0f} to {1000 * khi:.0f} meV (90%, by nuclear matrix element). The inverted")
    w(f"    band at m0 = 0, {1000 * io_lo:.1f} to {1000 * io_hi:.1f} meV, is tested only above {1000 * klo:.0f} meV and only with the")
    w("    most favourable matrix elements: neither ordering is excluded by double-beta decay yet.")
    w("  P4. Mixing patterns from discrete flavour symmetries (tested like Part C's textures; delta is")
    w("      far from Gaussian, so only theta12 decides survival, at the 3 sigma level)")
    for o, rec in nu["orderings"].items():
        pt = rec["patterns"]
        w(f"    {o}:  pattern                             unknowns  predicts   pulls / prediction            verdict")
        for r_ in pt["rows"]:
            verdict = "survives" if r_["survives"] else "excluded"
            if r_["unknowns"] == 0:
                pl = r_["pulls"]
                w(f"        {r_['pattern']:<36s} {r_['unknowns']:4d} {r_['predictions']:8d}     theta12 {pl['s12sq']:+5.1f},"
                  f" theta13 {pl['s13sq']:+5.1f}, theta23 {pl['s23sq']:+4.1f}   {verdict}")
            else:
                w(f"        {r_['pattern']:<36s} {r_['unknowns']:4d} {r_['predictions']:8d}     theta13, theta23 fix the"
                  f" unknowns                {verdict}")
                for q_ in r_["solutions"]:
                    w(f"            sin^2 theta12 = {q_['s12sq']:.4f} +/- {q_['s12sq_sigma']:.4f} ({q_['s12_pull']:+.1f} sigma);"
                      f" delta = {q_['delta_deg']:.0f} +/- {q_['delta_sigma']:.0f} deg ({q_['delta_pull']:+.1f} sigma)")
        w(f"        measured: sin^2 theta12 = {inp('nu_s12sq'):.3f}, delta = {pt['delta_meas']:.0f} +/- {pt['delta_sigma']:.1f} deg")
    qlc = nu["orderings"]["NO"]["patterns"]["qlc"]
    w(f"    Quark-lepton complementarity, theta12 + theta_C = 45 deg: {qlc['sum_deg']:.2f} +/- {qlc['sigma_deg']:.2f} deg,"
      f" {qlc['n_sigma']:.1f} sigma")
    no_ = nu["orderings"]["NO"]["seesaw"]
    w("  P5. Where the masses come from. Seesaw: m = y^2 v^2/(2 M), with the heaviest mass at m0 = 0")
    w(f"      ({1000 * no_['m_heaviest_eV']:.1f} meV, NO):  M = {no_['M_for_y_1']:.1e} GeV for y = 1,"
      f" {no_['M_for_y_top']:.1e} GeV for y = y_t,")
    w(f"      at most {no_['M_max_perturbative']:.1e} GeV for y = sqrt(4 pi) (perturbative). Part I's M_GUT ="
      f" {_fmt(nu['M_GUT'] or math.nan, 3)} GeV and")
    w(f"      M_P = {nu['M_P']:.2e} GeV lie above it: a seesaw needs new states below the unification scale.")
    w(f"      Dirac alternative: y_nu up to {max(no_['dirac_yukawa']):.1e}, against y_e = {nu['electron_yukawa']:.1e}"
      " (a new hierarchy, no new scale).")
    no_rec, io_rec = nu["orderings"]["NO"], nu["orderings"]["IO"]
    io_out = [lims[k] for k, v_ in io_rec["vs_cosmology"].items() if not v_["allowed"]]
    fixed_ = [r_ for r_ in no_rec["patterns"]["rows"] if r_["unknowns"] == 0]
    t13 = min(abs(r_["pulls"]["s13sq"]) for o_ in NU_ORDERINGS for r_ in nu["orderings"][o_]["patterns"]["rows"]
              if r_["unknowns"] == 0)
    corr = {r_["pattern"].split(":")[0]: max(nu["orderings"][o_]["patterns"]["rows"][i]["n_sigma"] for o_ in NU_ORDERINGS)
            for i, r_ in enumerate(no_rec["patterns"]["rows"]) if r_["unknowns"]}
    surv_ = [k for k, s_ in corr.items() if s_ <= num("survival_sigma")]
    w(_wrap("RESULT: the masses and the mixing are measured, not calculated. "
            + (f"Cosmology ({', '.join(io_out)}, flat LambdaCDM) excludes the inverted ordering at 95%; the normal "
               f"one keeps m0 below {1000 * min(m for m in no_rec['m0_max'].values() if m):.1f} meV. " if io_out else "")
            + f"Every fixed mixing pattern ({len(fixed_)}: tribimaximal, bimaximal, golden ratio, hexagonal) is "
            f"excluded by theta13 at {t13:.0f} sigma or more. "
            + (f"Surviving corrected patterns: {', '.join(f'{k} (theta12 at {corr[k]:.1f} sigma)' for k in surv_)}; "
               "each predicts sin^2 theta12 and delta from theta13 and theta23, a test for DUNE and Hyper-Kamiokande."
               if surv_ else "No corrected pattern survives."), 2))
    w("    Neutrino masses also test Part L's assumption: the SM up to M_P holds only for Dirac neutrinos.")
    w("")
    pq = res["proton_decay"]
    w("PART Q. PROTON DECAY: THE DIRECT TEST OF UNIFICATION")
    w("-" * 78)
    w("  If the couplings unify (Part I), the SU(5) gauge bosons X, Y turn quarks into leptons. Their")
    w("  exchange gives p -> e+ pi0 (Ellis et al. 2020, minimal SU(5)):")
    w("    Gamma = m_p/(32 pi) (1 - m_pi^2/m_p^2)^2 A_L^2 (g_GUT^2/M_X^2)^2 [A_S1^2 W_RL^2 + (1 + |V_ud|^2)^2 A_S2^2 W_LL^2]")
    w("  W: lattice matrix elements at 2 GeV (Aoki et al. 2017). A_S: one-loop running of the two operators")
    w("  from M_X to M_Z, exponents -2 c_i/b_i with this script's b_i. A_L: their QCD running to 2 GeV with")
    w(f"  this script's alpha_s: A_L = {pq['A_L']:.3f} (one-loop exponent; two loops: {pq['A_L_two_loop_quoted']:.3f}, quoted).")
    w("  M_X and alpha_GUT come from the algorithm; GUT thresholds (M_X against M_GUT) are unknown.")
    w("      hypothesis                            M_X (GeV)   alpha_GUT  A_S1   A_S2   tau (years)")
    for r_ in pq["rows"]:
        w(f"      {r_['hypothesis']:<37s} {r_['M_X']:.2e}   {r_['alpha_GUT']:.4f}   {r_['A_S1']:.2f}   {r_['A_S2']:.2f}"
          f"   {r_['tau_years']:.1e} +/- {r_['tau_sigma']:.0e}")
    w(f"  Super-Kamiokande: tau/B(p -> e+ pi0) > {pq['limit_e_pi0']:.1e} years (90% CL)")
    for r_ in pq["rows"]:
        verdict = (f"allowed, {r_['ratio_to_limit']:.1f} times the limit" if r_["allowed"] else
                   f"EXCLUDED: {r_['ratio_to_limit']:.0e} of the limit")
        w(f"      {r_['hypothesis']:<37s} {verdict}; the limit needs M_X > {r_['M_X_needed']:.1e} GeV")
    w("  Q2. Dimension five, p -> nubar K+, through the colour-triplet Higgsinos of minimal SUSY SU(5)")
    w("      (Hisano et al. 2013, eqs. 15-49): M_HC = M_GUT and every superpartner at M_S (Part I),")
    w("      tan(beta) from Part J; Yukawas run in the SM to M_S and in the MSSM to M_HC; the operators run")
    w("      with the Yukawas above M_S, with the gauge couplings below, with QCD to 2 GeV. The two unknown")
    w("      GUT phases are scanned: the band is every lifetime they allow.")
    for r_ in pq["d5"]:
        w(f"      tan(beta) = {r_['tan_beta']:.3f}: tau = {r_['tau_min']:.1e} to {r_['tau_max']:.1e} years"
          f"   (A_L = {r_['A_L']:.2f}, Abar_R = {r_['Abar_R']:.2f}, y_t(M_HC) = {r_['f_GUT']['t']:.2f})")
    if pq["d5"]:
        r0 = pq["d5"][0]
        w(f"      Super-Kamiokande: tau/B(p -> nubar K+) > {pq['limit_K_nu']:.1e} years (90% CL). Even at the best")
        w(f"      phases the limit needs M_HC > {r0['M_HC_needed']:.1e} GeV (tau ~ M_HC^2), or superpartners near"
          f" {r0['M_S_needed_scaling'] / 1000:.0f} TeV (tau ~ M_S^2).")
        w(f"      Check: the higgsino part alone gives {r0['tau_higgsino_only']:.1e} years; Hisano et al.'s scaling formula,")
        eq19 = float(LITERATURE["proton_decay_d5_scaling"]["value"]) * (2 * r0["tan_beta"] / (1 + r0["tan_beta"] ** 2)) ** 4 * (1 / (10 * r0["Abar_R"])) ** 2 \
            * (r0["M_S"] / 10 ** 5) ** 2 * (r0["M_HC"] / 10 ** 16) ** 2
        w(f"      eq. 19, gives {eq19:.1e} with the same Abar_R (a factor {eq19 / r0['tau_higgsino_only']:.1f}; to be"
          " debugged).")
    mss = [r_ for r_ in pq["rows"] if r_["M_S"]]
    sms = [r_ for r_ in pq["rows"] if not r_["M_S"]]
    d5_out = [r_ for r_ in pq["d5"] if not r_["allowed_somewhere"]]
    w(_wrap("RESULT: " + (f"with superpartners at Part I's M_S, the gauge-boson channel gives "
                          f"{mss[0]['tau_years']:.1e} years, {mss[0]['ratio_to_limit']:.0f} times the Super-K limit: "
                          f"{'allowed' if mss[0]['allowed'] else 'excluded'}, and within reach of Hyper-Kamiokande. "
                          if mss else "")
            + (f"But the Higgsino channel of minimal SUSY SU(5) at the same scales lives at most "
               f"{max(r_['tau_max'] for r_ in pq['d5']):.0e} years: excluded for every phase and every tan(beta) of "
               "Part J. Minimal SUSY SU(5) with one superpartner scale M_S fails proton decay, as Part K's Higgs mass "
               "already found; a heavier colour triplet or superpartners above about 100 TeV are needed. "
               if pq["d5"] and len(d5_out) == len(pq["d5"]) else "")
            + (f"In the SM, X bosons where g1 = g2 would make the proton live {sms[0]['tau_years']:.0e} years: "
               "excluded, one more reason the SM cannot unify." if sms else ""), 2))
    w("")
    an = res["anomalies"]
    hy = an["hypercharge"]
    w("PART R. WHAT ANOMALY CANCELLATION FIXES (exact)")
    w("-" * 78)
    w("  A chiral gauge theory is consistent only if its gauge anomalies cancel: exact conditions on the")
    w("  charges, and the one place where the SM's quantum numbers are calculated, not measured.")
    w("  R1. One family with the SM's representations and unknown hypercharges Y_Q, Y_u, Y_d, Y_L, Y_e:")
    w("      [SU(3)]^2 U(1), [SU(2)]^2 U(1), [gravity]^2 U(1), U(1)^3. The three linear ones give Y_L, Y_d,")
    w("      Y_e; U(1)^3 is then a quadratic, solved exactly (Y_Q = 1/6 sets the normalization):")
    for s_ in hy["solutions"]:
        w("        " + ", ".join(f"Y({k}) = {v}" for k, v in s_.items()))
    w("      the two differ only by naming u^c and d^c. A branch with Y_Q = 0 also cancels"
      f" ({hy['Y_Q_zero_branch_cancels']}), but only the")
    w(f"      right-handed quarks are charged and no Yukawa coupling exists ({hy['Y_Q_zero_branch_has_yukawas']}).")
    w("      With Yukawa couplings for every fermion: the SM's hypercharges, uniquely.")
    ch = hy.get("charges")
    if ch:
        w(f"      Electric charge Q = T3 + Y/(2 Y_H): u {ch['u']}, d {ch['d']}, e {ch['e']}, nu {ch['nu']}."
          f" Proton + electron: {ch['proton_plus_electron']};")
        w(f"      neutron: {ch['neutron']}. Charge is quantized: atoms are neutral because the anomalies cancel.")
    w(f"      With a right-handed neutrino, SM + eps (B - L) cancels for every eps ({hy['nu_R_family_cancels']}) and keeps")
    w(f"      a Dirac Yukawa ({hy['nu_R_dirac_yukawa_ok']}): hydrogen stays neutral ({hy['nu_R_hydrogen_charge']}) but the"
      f" neutron gets charge {hy['nu_R_neutron_charge_per_eps']} x eps.")
    w("      A Majorana mass for nu^c (the seesaw of Part P) needs Y(nu^c) = 0, so eps = 0: quantization returns.")
    w(f"  R2. Witten's SU(2) anomaly: {an['witten_doublets_per_family']} doublets per family (3 colours of Q, plus L): even, consistent.")
    d3 = an["331_part_D"]
    w(f"  R3. 3-3-1 (Part D): [SU(3)_L]^3 = #triplets - #antitriplets = {d3['SU3L_cubed']} for Part D's"
      f" {d3['families']} families ({d3['quark_triplet_families']} quark family in a triplet).")
    w("      With N_f families of lepton triplets and k quark families in triplets (N_c colours), it cancels")
    w("      only if N_f (N_c - 1) = 2 N_c k. For N_c = 3:")
    for a_ in an["331_allowed"]:
        w(f"        N_f = {a_['families']}, k = {a_['triplet_families']}: QCD b0 = {a_['qcd_b0']}"
          f" ({'asymptotically free' if a_['asymptotically_free'] else 'not asymptotically free'})")
    fam = an["331_families_with_af"]
    w(_wrap("RESULT: the SM's hypercharges and the quantization of electric charge follow from anomaly "
            "cancellation and the Yukawa couplings: calculated, not measured. A right-handed neutrino leaves one "
            "free direction, closed by a Majorana mass. In 3-3-1 the number of families must be a multiple of the "
            "number of colours, and asymptotic freedom of QCD leaves "
            + (f"exactly {fam[0]}" if len(fam) == 1 else ", ".join(str(f_) for f_ in fam))
            + ": the one free integer of the SM that a gauge theory calculates.", 2))
    w("")
    ba = res["baryon_asymmetry"]
    w("PART S. THE BARYON ASYMMETRY")
    w("-" * 78)
    w(f"  S1. eta_B = n_B/n_gamma from Omega_b h^2 = {inp('Omega_b_h2')} (Planck 2018) and T_CMB:"
      f" ({ba['eta_B'] * 1e10:.3f} +/- {ba['eta_B_sigma'] * 1e10:.3f}) x 10^-10")
    w("      Making it needs B violation, C and CP violation, and a departure from equilibrium (Sakharov).")
    sp, tr, cp = ba["sphaleron"], ba["transition"], ba["cp_measure"]
    w("  S2. The Standard Model alone")
    w(f"      B violation: sphalerons change B and L by N_f = {sp['delta_B_per_transition']} each (the SU(2) anomaly, Part R).")
    w(f"      Chemical equilibrium (Yukawas, sphalerons, zero hypercharge), solved exactly for N_f = {sp['n_f']},"
      f" N_H = {sp['n_h']}:")
    w(f"        B = {sp['B_over_BminusL']} (B - L), L = {sp['L_over_BminusL']} (B - L)  (Harvey-Turner's 28/79)")
    w(f"      Departure from equilibrium: the transition is first order only for m_h < {tr['endpoint_m_h']} +/-"
      f" {tr['endpoint_sigma']} GeV (lattice);")
    w(f"        measured m_h = {tr['m_h']:.2f} GeV, {tr['n_sigma_above']:.0f} sigma above: a smooth crossover at"
      f" T_c = {tr['T_c']} GeV. Fails.")
    w(f"      CP violation: J prod(m_i^2 - m_j^2) / T_c^12 = {cp['delta_CP']:.1e} (running masses at m_t(m_t)),")
    w(f"        {math.log10(ba['eta_B'] / cp['delta_CP']):.0f} orders of magnitude below eta_B. Fails.")
    lg = ba["leptogenesis"]
    w("  S3. Leptogenesis (the seesaw of Part P): eta_B = c_sph (3/4) (g*s,0 / g*) epsilon_1 kappa, kappa <= 1")
    w(f"      g* = {lg['g_star']} (SM plus N_1, from the field content), g*s,0 = {lg['g_s_today']}, c_sph ="
      f" {sp['B_over_BminusL']}: eta_B = {lg['eta_per_epsilon_kappa']:.3e} epsilon_1 kappa")
    w(f"      so epsilon_1 >= {lg['epsilon_min']:.1e}. SM bound: |epsilon_1| <= 3 M_1 (m_3 - m_1) / (16 pi <H>^2):")
    for r_ in lg["rows"]:
        w(f"        {r_['ordering']}: m_3 - m_1 = {1000 * r_['m3_minus_m1_eV']:.1f} meV  ->  M_1 >= {r_['M1_min']:.1e} GeV;"
          f" Part P's window up to {r_['window_top']:.1e} GeV: {'open' if r_['window_open'] else 'closed'}")
    w(f"      (Davidson-Ibarra's MSSM form has 8 pi; their example, epsilon > 1e-6 needs M_1 > 4e9 GeV: here"
      f" {lg['di_example_M1']:.1e} GeV)")
    w(f"      Efficiency: kappa_f = 2/(K z_B) (1 - e^(-K z_B / 2)), K = m~_1/m_*, m_* = {1000 * lg['m_star_eV']:.3f} meV"
      " (from g* and M_P);")
    w("      z_B solves (K/4) z^3 e^-z (1 + sqrt(pi z/2)) = z - 1 (Buchmuller, Di Bari, Plumacher, eqs. 22, 59). Over")
    w("      the natural range m_sol <= m~_1 <= m_atm:")
    eff_ = lg["efficiency"]
    shown = sorted({0, len(eff_) - 1} | set(range(0, len(eff_), max(1, len(eff_) // 4))))
    for e_ in (eff_[i] for i in shown):
        w(f"        m~_1 = {1000 * e_['m_tilde_eV']:5.1f} meV: K = {e_['K']:5.1f}, z_B = {e_['z_B']:.2f}, kappa_f = {e_['kappa']:.4f}"
          f"  ->  M_1 >= {e_['M1_min']:.1e} GeV")
    w("      Thermal production also needs a reheating temperature above M_1.")
    w(_wrap("RESULT: eta_B is measured, not calculated. The Standard Model fails two of Sakharov's conditions: its "
            f"transition is a crossover ({tr['n_sigma_above']:.0f} sigma above the lattice endpoint) and its CP "
            f"violation is {math.log10(ba['eta_B'] / cp['delta_CP']):.0f} orders too small. Leptogenesis works if the "
            f"lightest right-handed neutrino is above {min(r_['M1_min'] for r_ in lg['rows']):.0e} GeV (at full "
            f"efficiency; {lg['M1_min_natural'][0]:.0e} to {lg['M1_min_natural'][1]:.0e} GeV over the natural washout range), inside the "
            "seesaw window of Part P: it ties eta_B to the neutrino masses but adds unmeasured parameters (M_1, the "
            "phases, kappa). Part L's SM up to M_P, with Dirac neutrinos, has no seesaw and so no such mechanism.", 2))
    w("")
    so = res["so10"]
    w("PART T. SO(10)")
    w("-" * 78)
    w("  SO(10) puts a whole family, with a right-handed neutrino, into one 16.")
    wa = so["weinberg"]
    w("  T1. Group theory (exact)")
    w("      B - L anomalies of one family, " + ", ".join(f"{k} = {v}" for k, v in so["bl_anomalies_without_nu_c"].items())
      + " without nu^c;")
    w("        all zero with it: gauging B - L (inside SO(10)) requires the right-handed neutrino.")
    w(f"      Over a complete 16: sin^2 theta_W = Tr T3^2 / Tr Q^2 = {wa['sin2_theta_W']} at unification;"
      f" Tr T3^2 / Tr Y^2 = {wa['GUT_norm']},")
    w(f"        the hypercharge normalization this script uses throughout ({wa['script_GUT_norm']}).")
    mn = so["minimal_10"]
    w(f"  T2. Minimal Yukawas (one 10_H): M_u ~ M_d ~ M_e, so V = 1 and equal mass ratios. At"
      f" {_fmt(mn['scale'], 3)} GeV:")
    w(f"      m_c/m_t = {mn['m_c/m_t']:.4f}, m_s/m_b = {mn['m_s/m_b']:.4f}, m_mu/m_tau = {mn['m_mu/m_tau']:.4f}:"
      f" (m_s/m_b)/(m_c/m_t) = {mn['s_over_c']:.1f}, (m_mu/m_tau)/(m_s/m_b) = {mn['mu_over_s']:.1f}")
    w("      Excluded (and V = 1 contradicts every CKM measurement). Adding a 126_H gives each sector its own")
    w("      matrix: enough parameters to fit, none predicted (Part F's closure).")
    tb = so["t_b_tau"]
    if tb:
        w(f"  T3. t-b-tau unification (MSSM, Part I's scales): y_t = y_b at M_GUT for tan(beta) = {tb['tan_beta']:.0f},"
          f" where y_b/y_tau = {tb['yb_over_ytau']:.3f}.")
        w(f"      It needs a supersymmetric threshold correction of {100 * tb['m_b_threshold_needed']:+.0f} % to m_b: a"
          " function of the unknown superpartner spectrum, so a trade, not a test.")
    ps = so["pati_salam"]
    bp = ps["b_PS"]
    w("  T4. Non-supersymmetric SO(10) through Pati-Salam SU(4) x SU(2)_L x SU(2)_R at M_I (one loop)")
    w(f"      b from the field content: SU(4) {bp['4']}, SU(2)_L {bp['2L']}, SU(2)_R {bp['2R']} (three families of")
    w("      (4,2,1) + (4bar,1,2), scalars (1,2,2) and (10,1,3)). The three measured couplings fix the three")
    w("      unknowns exactly (a linear system):")
    w(f"        M_I = {ps['M_I']:.2e} GeV, M_GUT = {ps['M_GUT']:.2e} GeV, 1/alpha_GUT = {1 / ps['alpha_GUT']:.1f}"
      f" ({'consistent: M_Z < M_I < M_GUT' if ps['consistent'] else 'inconsistent ordering'})")
    w(f"      Proton decay (Part Q's formula, SM running throughout): tau = {ps['tau_p_years']:.1e} years against"
      f" {ps['tau_p_limit']:.1e}: {'allowed' if ps['tau_p_allowed'] else 'excluded'}")
    w(f"      M_I is where B - L breaks and the right-handed neutrinos get mass: inside leptogenesis's window"
      f" ({ps['M1_min_leptogenesis']:.0e} to {ps['seesaw_window_top']:.0e} GeV): {ps['M_I_in_leptogenesis_window']}")
    w(f"      If the axion scale is M_I (as in SO(10) axion models), m_a = {ps['axion_m_a_eV_if_fa_MI'] * 1e6:.1f} micro-eV.")
    w("  T5. Every minimal chain, one and two loops (b from the field content; SM two loops below M_I; tree-level")
    w("      matching, thresholds unknown). Each chain has as many unknowns as conditions: none predicts a coupling.")
    w("      chain   b (one loop)                M_I, M_GUT (1 loop)    M_I, M_GUT (2 loops)  1/a_GUT  tau_p (yr)")
    for nm, c_ in so["chains"].items():
        l1, l2 = c_["loop1"], c_["loop2"]
        w(f"      {nm:<6s}  {', '.join(str(v_) for v_ in c_['b1']):<26s}  {l1['M_I']:.1e}, {l1['M_GUT']:.1e}"
          f"     {l2['M_I']:.1e}, {l2['M_GUT']:.1e}   {1 / l2['alpha_GUT']:5.1f}   {l2['tau_p_years']:.1e}"
          f" {'ok' if l2['tau_p_allowed'] else 'EXCLUDED'}")
    w("      lambda(M_I) = 0 at each chain's two-loop M_I (Part L's running and matching):")
    for nm, c_ in so["chains"].items():
        w(f"        {nm:<6s} m_h = {c_['loop2']['m_h_lambda_MI_zero']:.2f} GeV")
    vac = so["vacuum"]
    w("  T6. What lambda(M_I) is. The heavy scalar that breaks the chain at M_I shifts the SM quartic at tree level")
    w("      (Elias-Miro et al. 2012, eq. 5): lambda_SM(M_I) = lambda_H - lambda_HS^2/lambda_S, a shift that is >= 0")
    w("      and unknown. So lambda(M_I) = 0 is not a condition of the theory. What is fixed: the vacuum is stable")
    w("      only if the SM's lambda stays positive up to M_I, i.e. M_I below the scale mu_0 where it turns negative.")
    band = vac["mu0_band_Mt"]
    w(f"      mu_0 = {vac['mu0']:.2e} GeV for the measured m_h" + (f" ({band[0]:.1e} to {band[-1]:.1e} for M_t +/- 1 sigma)"
                                                                     if band else ""))
    for nm, r_ in vac["rows"].items():
        verdict = "the threshold can stabilize the vacuum" if r_["stabilizable"] else "metastable SM between mu_0 and M_I"
        w(f"        {nm:<6s} M_I = {r_['M_I']:.1e}: lambda_SM(M_I) = {r_['lambda_SM_at_MI']:+.4f}  ->  {verdict}")
    w("      The 'lambda(M_I) = 0' Higgs masses above only say how close each chain's M_I lies to mu_0.")
    th_ = so["thresholds"]
    band_ = next(iter(th_.values()))["band"] if th_ else 0
    w(f"  T7. Thresholds: each matching condition shifted by up to +/- {band_} in 1/alpha (an assumed band, typical of")
    w("      one-loop thresholds), every corner solved at two loops. Ranges, and which verdicts can flip:")
    for nm, t_ in th_.items():
        flips = [n_ for n_, f_ in (("proton decay", t_["proton_flips"]), ("vacuum", t_["vacuum_flips"]),
                                   ("leptogenesis", t_["leptogenesis_flips"])) if f_]
        w(f"        {nm:<6s} M_I {t_['M_I'][0]:.1e} - {t_['M_I'][1]:.1e}, M_GUT {t_['M_GUT'][0]:.1e} - {t_['M_GUT'][1]:.1e},"
          f" tau_p {t_['tau_p'][0]:.0e} - {t_['tau_p'][1]:.0e}: " + (", ".join(flips) + " can flip" if flips else "robust"))
    hs_ = so["heavy_spectrum_PS"]
    w("  T8. Pati-Salam's heavy GUT multiplets (SO(10) broken by a 210, plus the 126 and 10): each shifts the")
    w("      couplings at M_GUT by (b^h/2 pi) ln(M_h/M_GUT). Per unit of that log, and the mass ratio M_h/M_GUT")
    w("      (that multiplet alone) at which proton decay or vacuum stability would flip:")
    w("        multiplet               b (4, 2L, 2R)       d ln M_I  d ln tau_p   proton flips   vacuum flips")
    for r_ in hs_["rows"]:
        pf = f"{r_['proton_flip_ratio']:.2g}" if r_["proton_flip_ratio"] else "-"
        vf = f"{r_['vacuum_flip_ratio']:.2g}" if r_["vacuum_flip_ratio"] else "-"
        w(f"        {r_['multiplet']:<23s} {', '.join(str(v_) for v_ in r_['b']):<18s} {r_['dlnMI']:+8.3f}  {r_['dlntau']:+9.3f}"
          f"   at {pf:<9s}   at {vf}")
    w(f"      All eight within a factor {hs_['spread']} of M_GUT: M_I {hs_['M_I'][0]:.0e} - {hs_['M_I'][1]:.0e} GeV,"
      f" M_GUT {hs_['M_GUT'][0]:.0e} - {hs_['M_GUT'][1]:.0e} GeV,")
    w(f"      tau_p {hs_['tau_p'][0]:.0e} - {hs_['tau_p'][1]:.0e} years: the heavy spectrum, not the running, decides.")
    pz = so["potential_210"]
    w("  T9. The 210's own potential calculates four of those masses. Invariants: S2, the cubic C, quartics Q1-Q4;")
    w("      vev on the Pati-Salam singlet; mass^2/v^2 per multiplet (quartics per 576, cubic per 24, eta in units of v):")
    for nm, c_ in pz["curvatures"].items():
        w(f"        {nm:<9s} " + "  ".join(f"{k_} {v_:+.4f}" for k_, v_ in c_.items()))
    w(f"      Couplings scanned: |lambda_a| <= {_fmt(pz['lambda_max'], 2)}, |eta/v| <= {_fmt(pz['eta_max'], 2)};"
      f" {pz['viable']} of {pz['tried']} points give a local minimum bounded")
    w("      below along the test directions. Their masses (the 126's and 10's still at M_GUT) give, as fractions of")
    w("      the viable potentials:")
    tq, mq = pz["tau_p_quantiles"], pz["M_I_quantiles"]
    w(f"        proton decay passes {100 * pz['frac_proton_ok']:.0f} %; tau_p 16-50-84 %: {tq[0]:.1e}, {tq[1]:.1e}, {tq[2]:.1e} years")
    w(f"        M_I 16-50-84 %: {mq[0]:.1e}, {mq[1]:.1e}, {mq[2]:.1e} GeV; natural leptogenesis {100 * pz['frac_leptogenesis_ok']:.0f} %;"
      f" stabilizable vacuum {100 * pz['frac_vacuum_ok']:.0f} %")
    w(f"        proton decay and natural leptogenesis together: {100 * pz['frac_all']:.0f} %")
    p6 = pz["with_126"]
    c6 = p6["coefficients_126"]
    w("  T10. The 126's masses from its couplings to <210> (self-dual 5-forms; norm, the D-odd cubic, quartics D, E;")
    w("       a universal quartic absorbed). Eigenvalues per multiplet, relative to the norm:")
    for r_, c_ in c6.items():
        w(f"        {r_:<11s} " + "  ".join(f"{k_} {v_:+.4f}" for k_, v_ in c_.items()))
    w("       Only the cubic tells (10,3,1) from (10bar,1,3). The chain needs (10bar,1,3) light at M_I, so")
    w("       m^2(10,3,1) = 2 eta_2 v exactly: the dominant multiplet of T8 is set by one coupling.")
    tq, mq = p6["tau_p_quantiles"], p6["M_I_quantiles"]
    w(f"       With the 126's couplings scanned too ({p6['viable']} jointly viable potentials):")
    w(f"        proton decay passes {100 * p6['frac_proton_ok']:.0f} %; tau_p 16-50-84 %: {tq[0]:.1e}, {tq[1]:.1e}, {tq[2]:.1e} years")
    w(f"        M_I 16-50-84 %: {mq[0]:.1e}, {mq[1]:.1e}, {mq[2]:.1e} GeV; natural leptogenesis {100 * p6['frac_leptogenesis_ok']:.0f} %;"
      f" stabilizable vacuum {100 * p6['frac_vacuum_ok']:.0f} %")
    w(f"        proton decay and natural leptogenesis together: {100 * p6['frac_all']:.0f} %")
    p10 = pz["with_10"]
    w("  T11. The 10's couplings. No cubic H H phi exists (10 x 10 holds no 210); the quartic H_i H_j A_ij,")
    w(f"       A_ij = phi_iklm phi_jklm, is {p10['A_SO4']:.0f} v^2 on SO(4) indices and {p10['A_SO6']:.0f} on SO(6): it alone"
      " splits the doublet (1,2,2) from")
    w("       the colour triplet (6,1,1). The cubic H_i S_ijklm phi_jklm mixes that triplet with the 126's (6,1,1).")
    w("       The light doublet fixes the 10's mass term: a cancellation to (M_I/M_GUT)^2, the doublet-triplet")
    w("       splitting problem, assumed here as in every SO(10) model.")
    tq, mq, lq = p10["tau_p_quantiles"], p10["M_I_quantiles"], p10["triplet_light_quantiles"]
    w(f"       With the 10's couplings scanned too ({p10['viable']} jointly viable potentials):")
    w(f"        lighter colour triplet / M_GUT 16-50-84 %: {lq[0]:.2f}, {lq[1]:.2f}, {lq[2]:.2f}")
    w(f"        proton decay passes {100 * p10['frac_proton_ok']:.0f} %; tau_p 16-50-84 %: {tq[0]:.1e}, {tq[1]:.1e}, {tq[2]:.1e} years")
    w(f"        M_I 16-50-84 %: {mq[0]:.1e}, {mq[1]:.1e}, {mq[2]:.1e} GeV; natural leptogenesis {100 * p10['frac_leptogenesis_ok']:.0f} %;"
      f" stabilizable vacuum {100 * p10['frac_vacuum_ok']:.0f} %")
    w(f"        proton decay and natural leptogenesis together: {100 * p10['frac_all']:.0f} %")
    w("       Not included: proton decay through the colour triplets' own Yukawa couplings (scalar exchange), which")
    w("       needs the Yukawa matrices at M_GUT.")
    w(_wrap("RESULT: SO(10) calculates the hypercharges' normalization (sin^2 theta_W = 3/8 at unification) and "
            "requires the right-handed neutrino; its minimal Yukawa relations are excluded. Without supersymmetry, "
            f"the Pati-Salam route unifies the three couplings with M_I = {ps['M_I']:.0e} GeV and M_GUT = "
            f"{ps['M_GUT']:.0e} GeV, passes proton decay, and puts the seesaw scale where leptogenesis needs it: one "
            "chain that joins Parts I, P, Q and S. It predicts nothing yet (three couplings fix three unknowns); "
            "two-loop running and the thresholds at M_I and M_GUT decide whether it holds, and Part L's SM then "
            "runs only up to M_I.", 2))
    w("")
    dmr = res["dark_matter"]
    w("PART V. DARK MATTER FROM THE AXION")
    w("-" * 78)
    w("  The axion of Part O is made by misalignment: frozen at an angle theta_i until 3 H = m_a(T), then")
    w("  oscillating and redshifting like matter (Di Luzio et al. 2020, eqs. 148-169). m_a f_a from Part O,")
    w("  M_P from Part H1, g_S today = 43/11 from Part S, T_0 from T_CMB; m_a(T) from the dilute instanton gas")
    w("  (beta, gamma, T_C quoted). Strings and domain walls (post-inflation only) are left out: their yield is")
    w("  not agreed on.")
    c170 = dmr["check_eq170"]
    w(f"  Check: at f_a = {c170['f_a']:.1e} GeV, Omega_a h^2 = {c170['Omega_h2']:.4f} (their eq. 170: {c170['printed']})")
    w(f"  Post-inflation (<theta_i^2> = {dmr['theta_post']}^2): all of Omega_c h^2 = {dmr['Omega_c_h2']} needs f_a ="
      f" {dmr['f_a_all_dm_post']:.2e} GeV,")
    w(f"    m_a = {1e6 * dmr['m_a_all_dm_post_eV']:.1f} micro-eV (oscillation at T = {1000 * dmr['T_osc_GeV']:.0f} MeV)."
      " Larger f_a overcloses, smaller leaves room for strings.")
    w("  At each SO(10) chain's M_I (PQ broken with B - L):")
    for nm, c_ in dmr["chains"].items():
        pre = (f"pre-inflation theta_i = {c_['theta_i_pre_needed']:.2f}" if c_["pre_possible"]
               else "pre-inflation impossible (theta_i > pi)")
        w(f"    {nm:<6s} f_a = {c_['f_a']:.1e} GeV, m_a = {1e6 * c_['m_a_eV']:7.1f} micro-eV: {100 * c_['fraction_post']:6.2f} %"
          f" of the dark matter post-inflation; {pre}")
    w(_wrap("RESULT: the dark-matter density, an input until now, becomes a function of one unknown, f_a. Put at "
            "the Pati-Salam scale, the axion makes about two thirds of the dark matter by misalignment alone (strings "
            "add more), at m_a near 40 micro-eV: unification, neutrino masses, the strong CP problem and dark matter "
            "would share one scale. At the left-right scale it cannot be the dark matter. Not yet a prediction: the "
            "string yield and m_a(T) near T_C are the open inputs.", 2))
    w("")
    wm = res["w_mass"]
    w("PART W. THE W MASS: A TEST OF THE STANDARD MODEL ITSELF")
    w("-" * 78)
    w("  The SM fixes M_W from G_F, alpha, M_Z, m_t and m_h through its quantum corrections. The full two-loop")
    w("  result in its published parametrization (Awramik, Czakon, Freitas, Weiglein 2004; accurate to 0.5 MeV),")
    w(f"  Delta alpha_had^(5) = {inp('delta_alpha_had5')} (PDG 2024), at Part L's Higgs mass m_h = {wm['m_h_used']:.2f} GeV:")
    pts = ", ".join(f"{k} {1000 * v:.1f}" for k, v in wm["sigma_parts"].items())
    w(f"    M_W = {wm['M_W']:.4f} +/- {wm['sigma']:.4f} GeV  (MeV: {pts}, m_h {1000 * wm['sigma_m_h']:.1f},"
      f" fit {1000 * wm['fit_accuracy']:.1f})")
    w(f"    at the measured m_h instead: {1000 * wm['shift_to_measured_m_h']:+.1f} MeV")
    for k, c_ in wm["comparisons"].items():
        w(f"    {k:<36s} {c_['value']:.4f} +/- {c_['sigma']:.4f}: {c_['pull']:+.1f} sigma")
    zp = wm["z_pole"]
    w("  The effective weak mixing angle of the Z couplings (Awramik, Czakon, Freitas 2006, two loops, leptons):")
    w(f"    sin^2 theta_eff = {zp['sin2_eff']:.5f} +/- {zp['sigma']:.5f}; at the measured m_h:"
      f" {zp['shift_to_measured_m_h']:+.5f}")
    for k, c_ in zp["comparisons"].items():
        w(f"    {COMPARISONS[k]['source'].split(': ')[-1]:<36s} {c_['value']:.5f} +/- {c_['sigma']:.5f}: {c_['pull']:+.1f} sigma")
    w(_wrap("RESULT: the Standard Model's M_W, with every input but Delta alpha_had measured or calculated here, "
            "agrees with the measurements and reproduces the PDG's global fit. No new physics is needed at the weak "
            "scale; the heavy states of the SO(10) chains decouple, so this tests the SM below M_I, not the chains.", 2))
    w("")
    cc_ = res["closed_cosmology"]
    w("PART X. CLOSING THE LOOP: COSMOLOGY FROM THE PARTICLE PHYSICS")
    w("-" * 78)
    w("  Part A takes Omega_m as an input. Here it follows from the rest: Omega_b (measured), the axion at the")
    w(f"  surviving chain's M_I (Part U: {cc_['chain']}) by misalignment (Part V: Omega_a h^2 = {cc_['Omega_a_h2']:.4f}) and the"
      " minimal neutrino masses")
    w("  (Part P). Flatness gives Omega_Lambda; the Friedmann equation the age.")
    w(f"    Omega_m = {cc_['Omega_m']:.4f} (Part A's input: {cc_['Omega_m_input']:.4f}), Omega_Lambda = {cc_['Omega_Lambda']:.4f},"
      f" age = {cc_['age_Gyr']:.3f} Gyr")
    w(f"    against Planck's {_comparison('age_Gyr')[0]} +/- {_comparison('age_Gyr')[1]} Gyr: {cc_['age_pull']:+.0f} sigma"
      f" (with all of Omega_c: {cc_['age_with_all_dm_Gyr']:.3f} Gyr)")
    w(_wrap(f"RESULT: misalignment alone leaves the universe too old by {cc_['age_pull']:.0f} sigma: closing the loop needs "
            f"{100 * cc_['string_fraction_needed']:.0f} % of the dark matter from the axion's strings and domain walls "
            "(post-inflation), or a second component. That fraction is now the single number on which the "
            "particle-physics side of the cosmology hangs; the lattice and simulation results for the string "
            "yield are what would test it.", 2))
    w("")
    yy = res["so10_yukawa"]
    yp, yl = yy["PS"], yy["LR"]
    w("PART Y. THE SO(10) YUKAWA SECTOR: CAN IT GIVE THE CHARGED-FERMION MASSES?")
    w("-" * 78)
    w("  With a 10 and a 126 the Yukawas are symmetric and shared: M_u = a Y10 + b Y126, M_d = c Y10 + d Y126,")
    w("  M_e = c Y10 - 3 d Y126 (a-d: the light Higgs' components).")
    w(f"  Y1. Pati-Salam (at M_I = {yp['scale']:.1e} GeV). SU(4) is unbroken up to M_GUT and <210> is a PS singlet, so")
    w("      nothing mixes the 10's (1,2,2) (SU(4) singlet) with the 126's (15,2,2): the light Higgs lies in one")
    w("      SU(4) irrep, and M_e = M_d (10) or M_e = -3 M_d (126) for every generation (exact at tree level).")
    for g_ in yp["generations"]:
        w(f"        {g_['pair']:<11s} = {g_['ratio']:.3f} +/- {g_['sigma']:.3f}:  {g_['pull_10']:+.0f} sigma from 1,"
          f" {g_['pull_126']:+.0f} sigma from 3")
    w(f"      Excluded: {yp['excluded']}. The minimal Pati-Salam chain cannot give the charged-fermion masses; it needs")
    w("      more Yukawa structure (a 120, or a vev that breaks SU(4) at M_GUT).")
    w(f"  Y2. Where the doublets can mix (the left-right chain, SU(4) broken at M_GUT = {yl['scale']:.1e} GeV): eliminating")
    w("      Y10, Y126 gives M_e = c1 M_d + c2 M_u, c1, c2 complex. With M_u real diagonal, M_d = Psi V X D_d X V^T Psi")
    w("      (the up-quark phases Psi are physical for symmetric Yukawas). Eight unknowns, three lepton masses:")
    w(f"      best of {yl['starts']} seeded starts: chi^2 = {_fmt(yl['chi2_min'], 2)} at {100 * yl['mass_tolerance']:.0f} % per mass;"
      f" masses {', '.join(f'{m_:.4g}' for m_ in yl['best_masses'])} GeV")
    w(f"      against {', '.join(f'{m_:.4g}' for m_ in yl['masses']['e'])} GeV (worst miss {100 * yl['worst_rel_miss']:.3f} %)."
      " Reached; the prediction must come from the")
    w("      neutrinos (type-II seesaw: M_nu proportional to M_d - M_e), the next step.")
    w(_wrap("RESULT: SO(10)'s Yukawa sector is a real test. The minimal Pati-Salam chain fails it: its unbroken SU(4) "
            "keeps the light Higgs in one irrep, which gives the wrong lepton/down ratios by tens of sigma. Where "
            "SU(4) breaks at M_GUT (left-right chain), the 10 + 126 sum rule reaches the charged leptons, with "
            "parameters to spare: whether it calculates the neutrino mixing is the open question.", 2))
    w("")
    sc_ = res["scorecard"]
    w("PART U. THE SCORECARD: EVERY COMPLETE HYPOTHESIS AGAINST EVERY CONDITION")
    w("-" * 78)
    w("  Each hypothesis meets every condition, with the verdict the earlier parts computed:")
    w("    pass / fail (sigma or reason) / trade (an unknown absorbs the condition: nothing tested) /")
    w("    open (no mechanism in that hypothesis).")
    for h, r_ in sc_["rows"].items():
        w(f"  {h}")
        for c, e in r_.items():
            sg = f" ({e['sigma']:.1f} sigma)" if e["sigma"] is not None else ""
            w(_wrap(f"{sc_['conditions'][c]:<18s} {e['status']:<6s}{sg}: {e['detail']}", 4, 100))
    w("  The chains' Higgs condition, lambda(M_I) = 0 where the SM ends (Part L's running and matching):")
    for nm, ph in sc_["chain_higgs"].items():
        w(f"    {nm:<6s} M_I = {ph['M_I']:.2e} GeV: m_h = {ph['m_h']:.2f} +/- {ph['sigma']:.2f} GeV, {ph['pull']:+.1f} sigma")
    w("    Why lambda should vanish at M_I is not established (the scalar sector changes there): a test.")
    thr = res["so10"]["thresholds"]
    for h, v_ in sc_["verdict"].items():
        rob = ""
        nm_ = h.replace("SO(10) via ", "")
        if nm_ in thr:
            t_ = thr[nm_]
            flips = [c for c, f_ in (("P", t_["proton_flips"]), ("V", t_["vacuum_flips"]), ("A", t_["leptogenesis_flips"])) if f_]
            rob = (" Thresholds (Part T7) can flip: " + ", ".join(sc_["conditions"][c] for c in flips) + "."
                   if flips else " Robust against the thresholds of Part T7.")
        w(_wrap(f"{h}: fails {', '.join(sc_['conditions'][c] for c in v_['fails']) or 'nothing'}; trades "
                f"{len(v_['trades'])}, open {len(v_['open'])}, passes {len(v_['passes'])}." + rob, 2))
    w(_wrap("RESULT: " + ("surviving every condition tested so far: " + ", ".join(sc_["survivors"])
                          + ". It predicts nothing yet: its scales are solved from the couplings, and its passes are "
                            "consistency, not calculation; two-loop running and thresholds come next."
                          if sc_["survivors"] else "no complete hypothesis survives every condition."), 2))
    w("")
    lg_ = res["ledger"]
    w("PART Z. THE LEDGER: EVERY FREE NUMBER AND WHAT THE ALGORITHM DOES WITH IT")
    w("-" * 78)
    w("  For the hypothesis that survives every condition (Part U): " + (", ".join(lg_["survivors"]) or "none")
      + f"; scales from its {lg_['chain']} chain.")
    w("  calculated = fixed with nothing measured spent; related = tied to others by a tested relation;")
    w("  traded = exchanged for an unknown; bounded = only limited; open = no mechanism; input = measured.")
    for r_ in lg_["rows"]:
        w(_wrap(f"{r_['quantity']:<34s} {r_['count']:<12s} {r_['status']:<10s} {r_['how']}", 4, 110))
    w("  Totals: " + ", ".join(f"{k} {v}" for k, v in sorted(lg_["counts"].items())))
    w(_wrap("RESULT: the algorithm closes: one pass, every stage run in dependency order, every assumption of the "
            "surviving hypothesis consistent with every condition tested, and every free number assigned a status. "
            "What it calculates is discrete and exact (the charges, their quantization, sin^2 theta_W at unification, "
            "the family number in 3-3-1). Every continuous number is still an input, traded for an unknown, bounded or "
            "open: no free number of the Standard Model is calculated. The surviving hypothesis' open entries "
            "(neutrino masses through type I, the dark matter, the Higgs mass) are where it must predict or fail next.", 2))
    w("")
    w("THE MODEL AS ONE ALGORITHM: WHERE EVERY NUMBER COMES FROM (traced while it ran)")
    w("-" * 78)
    lin = res["lineage"]
    w("  Stage (part, evidence level): measured inputs read; results taken from earlier stages")
    for st in lin["order"]:
        info = STAGES[st]
        ins = lin["reads"][st]
        w(f"  {st} ({info['part']}, {info['level']})")
        w(_wrap("inputs: " + (", ".join(ins) if ins else "none"), 6))
        if lin["uses"][st]:
            w(_wrap("takes:  " + ", ".join(lin["uses"][st]), 6))
        w(_wrap("assumes: " + info["assumes"], 6))
    au_ms = res["alpha_unification"].get("M_S_for_measured_alpha", {})
    w("  Numbers calculated once and handed on:")
    handoffs = (("M_S, M_GUT", f"{_fmt(au_ms.get('M_S_GeV') or math.nan)}, {_fmt(au_ms.get('M_GUT_GeV') or math.nan)}",
                 "gauge_unification[M_S_for_measured_alpha]"),
                ("M_P", _fmt(res["quantum_gravity"]["planck"]["E_P_GeV"]), "planck_units[E_P_GeV]"),
                ("m_t(m_t)", _fmt(res["flavour"]["runner"].mt_msbar), "flavour[runner]"))
    for name, val, key in handoffs:
        w(_wrap(f"{name} = {val} GeV, from {key}, taken by " + (", ".join(lin["takers"].get(key, [])) or "none"), 4))
    w("  Changing one measured input recalculates every stage it reaches, for example:")
    for name in ("M_t", "alpha_s_MZ", "G", "H0"):
        w(_wrap(f"{name}: " + ", ".join(st for st in lin["reaches"][name] if st != "self_checks"), 4))
    unused = [k for k, v in lin["reaches"].items() if not v]
    if unused:
        w(_wrap("Inputs no stage reads: " + ", ".join(unused), 4))
    w("  Global consistency of the stage assumptions:")
    for hyp, sts in lin["uv_hypotheses"].items():
        w(f"    {hyp:16s}: " + ", ".join(sts))
    if not lin["uv_consistent"]:
        w("    These field contents exclude each other. No stage chooses: Part M tests every")
        w("    hypothesis against every combination of conditions.")
    w(f"  The graph is acyclic ({lin['acyclic']}), so one pass in order is self-consistent: no stage")
    w("  needs a value that a later stage changes. A shared mechanism would add such feedback.")
    w("  Audit findings:")
    for status, text in AUDIT_FINDINGS:
        w(_wrap(f"[{status}] {text}", 4))
    w("")
    w("SELF-CHECKS (correctness of the calculation, not agreement with data)")
    w("-" * 78)
    for name, ok, detail in res["checks"]:
        w(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  ({detail})" if detail else ""))
    n_pass = sum(1 for _, ok, _ in res["checks"] if ok)
    w(f"  {n_pass}/{len(res['checks'])} checks pass")
    w(bar)
    return "\n".join(out)


def to_jsonable(res: Dict[str, Any]) -> Dict[str, Any]:
    def conv(o: Any) -> Any:
        if isinstance(o, Decimal):
            return str(o)
        if isinstance(o, Fr):
            return str(o)
        if isinstance(o, dict):
            return {str(k): conv(v) for k, v in o.items()
                    if k not in ("coef", "runner", "survey", "varied", "pair")}
        if isinstance(o, (list, tuple)):
            return [conv(v) for v in o]
        if isinstance(o, float) and not math.isfinite(o):
            return str(o)
        return o
    flav = res["flavour"]
    return conv({
        "version": VERSION, "inputs": INPUTS, "comparisons": COMPARISONS, "numerics": NUMERICS,
        "cosmology": res["cosmology"],
        "flavour": {"m_t_msbar": flav["runner"].mt_msbar, "electroweak": flav["runner"].ew,
                    "ratios": flav["ratios"], "scales": flav["scales"]},
        "texture_survey": {mu: sv["classes"] for mu, sv in res["survey"].items()},
        "yukawa_331": {f"b={b}": {"operators": {f"{f}{fl}": v for (f, fl), v in y["operators"].items()},
                                   "all_entries_allowed": y["all_entries_allowed"],
                                   "left_blocks": y["left_blocks"]} for b, y in res["yukawa_331"].items()},
        "symmetry_331": {f"b={b}": e for b, e in res["symmetry"]["by_beta"].items()},
        "general_texture_closure": res["closure"],
        "quantum_gravity": res["quantum_gravity"],
        "alpha_unification": res["alpha_unification"], "alpha_numerology": res["alpha_numerology"],
        "yukawa": res["yukawa"], "scales": res["scales"],
        "checks": [{"name": n, "pass": ok, "detail": d} for n, ok, d in res["checks"]],
        "uv_joint_test": res["joint"],
        "mass_formulas": res["mass_formulas"], "strong_cp": res["strong_cp"], "neutrinos": res["neutrinos"],
        "proton_decay": res["proton_decay"], "anomalies": res["anomalies"],
        "baryon_asymmetry": res["baryon_asymmetry"], "so10": res["so10"],
        "scorecard": res["scorecard"], "dark_matter": res["dark_matter"],
        "w_mass": res["w_mass"], "closed_cosmology": res["closed_cosmology"], "so10_yukawa": res["so10_yukawa"],
        "ledger": res["ledger"],
        "survey_certificates": res["survey_certificates"],
        "model": {"stages": STAGES, "lineage": res["lineage"], "changed_inputs": res["changed_inputs"],
                  "audit_findings": [{"status": a, "finding": b} for a, b in AUDIT_FINDINGS]},
    })


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=f"STUR Physics Lab {VERSION}")
    ap.add_argument("--scales", type=float, nargs="+", default=None,
                    help="evaluation scales in GeV (default: m_t(m_t) and the superpartner scale from Part I)")
    ap.add_argument("--precision", type=int, default=None, help="Decimal digits for the cosmology")
    ap.add_argument("--json-out", type=str, default=None, help="write every number to this JSON file")
    ap.add_argument("--certify", action="store_true",
                    help="prove every texture exclusion of Part C over its whole parameter space (minutes)")
    ap.add_argument("--set", action="append", default=[], metavar="NAME=VALUE",
                    help="change one measured input (repeatable); the whole model is recalculated")
    args = ap.parse_args(argv)
    _TRACE["set"] = {}
    for item in args.set:
        name, _, value = item.partition("=")
        if name not in INPUTS:
            ap.error(f"--set: unknown input {name!r}")
        Decimal(value)                                  # must be a number
        _TRACE["set"][name] = value
    t0 = time.perf_counter()
    res = run(args.scales, args.precision, args.certify)
    print(report(res))
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            json.dump(to_jsonable(res), fh, indent=2)
    print(f"Elapsed: {time.perf_counter() - t0:.1f} s")
    return 0 if all(ok for _, ok, _ in res["checks"]) else 1


if __name__ == "__main__":
    sys.exit(main())
