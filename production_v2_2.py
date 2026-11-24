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
    from the rank of the Jacobian of 10 weak-basis invariants, computed in exact
    integer arithmetic.
  Part K (preregistered in registrations/PART_K_Z3_OVERLAPS.md): whether quark
    profiles localized at the three Z3 points of a circle, with one shared width,
    a Higgs profile and a hypercharge holonomy, give the quark masses and the CKM
    matrix. Yukawas are exact triple overlaps; all four unknowns are scanned.

Run:  python3 production_v2_2.py                 (full report, about 3 minutes)
      python3 production_v2_2.py --json-out out.json
"""

from __future__ import annotations

import argparse
import cmath
from decimal import Decimal, localcontext
from fractions import Fraction as Fr
import itertools
import json
import math
import multiprocessing
import os
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
    # --- electroweak
    "G_F": {"value": "1.1663788e-5", "sigma": "0.0000006e-5", "unit": "GeV^-2", "source": "PDG 2024"},
    "M_Z": {"value": "91.1876", "sigma": "0.0021", "unit": "GeV", "source": "PDG (LEP Z pole)"},
    "alpha_em_inv_MZ": {"value": "127.951", "sigma": "0.009", "unit": "",
                        "source": "PDG 2024, MS-bar at M_Z"},
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
    "check_survey_tol": "1e-6",
    "symmetry_max_N": 6,              # Z_N searched exhaustively for N = 2 .. this
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
    "check_fd_rel_step": "1e-5",      # finite-difference step for the first-law check
    "check_fd_tol": "1e-8",
    "report_sci_below": "1e-3",       # print in scientific notation below / above these
    "report_sci_above": "1e5",
    # Part K (registrations/PART_K_Z3_OVERLAPS.md: every setting below is the registered one)
    "k_fourier_modes": 128,           # N: Fourier modes -N..N of each profile
    "k_quad_points": 576,             # M: trapezoid points (> 3N, divisible by 36)
    "k_fourier_modes_check": 192,     # K2
    "k_quad_points_check": 864,       # K2
    "k_log_a_lo": -2,                 # search range of log10 a_q and log10 a_H
    "k_log_a_hi": 4,
    "k_log_a_grid": 9,                # start grid: 9 x 9 x 12 x 24
    "k_theta_grid": 12,
    "k_flux_grid": 24,
    "k_starts": 10,                   # lowest grid points refined, per scale
    "k_starts_check": 20,             # K3 as registered (not run: too slow; replaced by the dense grid)
    "k_random_starts": 200,
    "k_dense_a": 17,                  # K3 replacement: dense grid 17 x 17 x 48 x 48 (on quadrature points)
    "k_dense_t": 48,
    "k_dense_f": 48,
    "k_dense_refine": 20,             # best dense-grid points refined, per scale
    "k_boundary_extend": 2,           # decades added once if the best point sits on a range edge
    "k_min_step": "1e-6",             # compass-search resolution in the search coordinates
    "k_mode_floor": "1e-18",          # Fourier coefficients below this (relative) are below double precision
    "k_shift_rel": "1e-10",           # inverse-iteration shift below the bisected ground-state energy
    "k_inverse_iterations": 4,
    "k_check_points": 20,             # K0a-c
    "k_tol_J": "1e-12",               # K0a
    "k_tol_unit": "1e-9",             # K0b, K0c
    "k_tol_converged": "1e-6",        # K2, K4 (determinant)
    "k_tol_search": "0.01",           # K3: a lower minimum by more than 1% fails it
    "k_tol_unitarity": "1e-12",       # K4
    "k_degenerate_ratio": 1000,       # eigenvalues of H counted distinct if the gap exceeds this x pair split
}
# Scales are never typed in: Parts B and C are evaluated at m_t(m_t) and at the superpartner
# scale M_S that Part I derives; Part J uses the unification scales it computes and M_Planck.


def inp(name: str) -> float:
    return float(INPUTS[name]["value"])


def sig(name: str) -> float:
    return float(INPUTS[name]["sigma"])


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


def pole_to_msbar_coeffs(n_light: int) -> Tuple[float, float]:
    """M / m(m) = 1 + k1 a + k2 a^2 with a = alpha_s(m)/pi (Gray, Broadhurst, Grafe, Schilcher 1990),
    light-quark masses in the loop neglected."""
    ca, cf, tf = su_n_casimirs(3)
    z2 = math.pi ** 2 / 6
    k1 = float(cf)
    k2 = (307 / 32 + 2 * z2 + 2 * z2 * math.log(2) / 3 - zeta3() / 6
          - n_light * (71 / 144 + z2 / 3))
    return k1, k2


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
                    thresholds: Sequence[float], steps_per_efold: int) -> List[float]:
    """RK4 in ln(mu), split exactly at the flavour thresholds."""
    l0, l1 = math.log(mu0), math.log(mu1)
    cuts = sorted(math.log(m) for m in thresholds if min(l0, l1) < math.log(m) < max(l0, l1))
    if l1 < l0:
        cuts.reverse()
    pts = [l0] + cuts + [l1]
    y = list(y0)
    for a, b in zip(pts[:-1], pts[1:]):
        if b == a:
            continue
        nf = _nf_at(math.exp((a + b) / 2), thresholds)
        n = max(1, math.ceil(abs(b - a) * steps_per_efold))
        h = (b - a) / n
        for _ in range(n):
            y = _rk4(lambda v: rhs(v, nf), y, h)
    return y


class FlavourRunner:
    """Runs alpha_s and the quark masses from the measured inputs. No free parameters."""

    def __init__(self, x: Dict[str, float], steps_per_efold: int):
        self.x = x
        self.steps = steps_per_efold
        self.alpha_em = 1 / x["alpha_em_inv_MZ"]
        self.coef = {}
        for nf in range(3, 7):
            b0, b1 = qcd_beta(nf)
            g0, g1 = qcd_gamma_m(nf)
            self.coef[nf] = (float(b0), float(b1), float(g0), float(g1))
        self.thresholds: List[float] = [x["m_c"], x["m_b"]]
        self.mt_msbar = self._top_msbar()
        self.thresholds = [x["m_c"], x["m_b"], self.mt_msbar]
        self.v = (math.sqrt(2) * x["G_F"]) ** (-1 / 2)

    # d alpha_s / d ln mu and d ln m / d ln mu (two-loop QCD, one-loop QED)
    def _qcd_rhs(self, y: List[float], nf: int, q2: float) -> List[float]:
        b0, b1, g0, g1 = self.coef[nf]
        al = y[0]
        a = al / (4 * math.pi)
        dal = -2 * (b0 * al * al / (4 * math.pi) + b1 * al ** 3 / (16 * math.pi ** 2))
        dlnm = -2 * (g0 * a + g1 * a * a) - 3 * q2 * self.alpha_em / (2 * math.pi)
        return [dal, dlnm]

    def alpha_s(self, mu: float) -> float:
        y = integrate_ln_mu([self.x["alpha_s_MZ"], 0.0], self.x["M_Z"], mu,
                            lambda v, nf: self._qcd_rhs(v, nf, 0.0), self.thresholds, self.steps)
        return y[0]

    def run_mass(self, m0: float, mu0: float, mu1: float, charge: Fr) -> float:
        y = integrate_ln_mu([self.alpha_s(mu0), math.log(m0)], mu0, mu1,
                            lambda v, nf: self._qcd_rhs(v, nf, float(charge) ** 2),
                            self.thresholds, self.steps)
        return math.exp(y[1])

    def _top_msbar(self) -> float:
        """Solve M_t = m (1 + k1 a(m) + k2 a(m)^2) for the MS-bar mass m = m_t(m_t)."""
        k1, k2 = pole_to_msbar_coeffs(5)
        big_m = self.x["M_t"]
        m = big_m
        for _ in range(100):
            a = self.alpha_s(m) / math.pi
            m_new = big_m / (1 + k1 * a + k2 * a * a)
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
                "r_ds": m["d"] / m["s"], "r_sb": m["s"] / m["b"], "alpha_s": self.alpha_s(mu0),
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
            b0, bb1, _, _ = self.coef[6]
            dal = -2 * (b0 * als * als / (4 * math.pi) + bb1 * als ** 3 / k)
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
            results.append(rec)
        return {"classes": results, "n_ordered_pairs": sum(len(v) for v in classes.values())}


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
# The Jacobian is computed exactly: at integer points the invariants and their
# derivatives are integers, and the rank is found by elimination modulo a large
# prime. Because 10 is the largest possible rank, finding rank 10 at any point
# proves the generic rank is 10. CP violation needs Im det[H_u, H_d] (which is
# proportional to J) to be nonzero; that is checked in exact Gaussian integers.
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
              "no_phase": 0, "candidates": 0, "rank": {}, "cp_impossible": 0, "predictive_with_cp": []}
    for key in sorted(classes):
        pu, pd = (frozenset(x) for x in key)
        if not _three_family_mixing(pu, pd):
            counts["no_three_family_mixing"] += 1
            continue
        if len(pu) + len(pd) - rephasing_rank(set(pu), set(pd)) < 1:
            counts["no_phase"] += 1
            continue
        counts["candidates"] += 1
        rk = max(invariant_rank(pu, pd, draw) for _ in range(tries))
        counts["rank"][rk] = counts["rank"].get(rk, 0) + 1
        if rk < 10:
            if cp_violation_possible(pu, pd, draw, tries):
                counts["predictive_with_cp"].append({"zeros_u": key[0], "zeros_d": key[1], "rank": rk})
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


def quantum_gravity(cosmo: Dict[str, Any], flav: Dict[str, Any]) -> Dict[str, Any]:
    x = _float_inputs()
    c, g, kb, alpha = x["c"], x["G"], x["k_B"], x["alpha_em"]
    hbar = x["h"] / (2 * math.pi)
    gev = x["e_charge"] * 10 ** 9                     # J per GeV
    out: Dict[str, Any] = {}

    # H1. Planck units
    lp, mp_planck = math.sqrt(hbar * g / c ** 3), math.sqrt(hbar * c / g)
    out["planck"] = {"l_P_m": lp, "t_P_s": lp / c, "m_P_kg": mp_planck, "E_P_GeV": mp_planck * c ** 2 / gev,
                     "T_P_K": mp_planck * c ** 2 / kb, "rho_P_kg_m3": c ** 5 / (hbar * g ** 2)}

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
    """(m_t(m_t), [g1, g2, g3, y_t, y_b, y_tau]) at mu = m_t(m_t) from the measured inputs."""
    x = _float_inputs()
    runner = flav["runner"]
    mt = runner.mt_msbar
    base = flav["ratios"][mt]
    v = runner.v
    a_em = 1 / x["alpha_em_inv_MZ"]
    s2 = x["s2_hat_Z"]
    sm1 = [float(b) for b in sm_gauge_b()]
    k = 16 * math.pi ** 2
    g1sq = 4 * math.pi * a_em / (1 - s2) / float(GUT_NORM)
    g2sq = 4 * math.pi * a_em / s2
    lt = math.log(mt / x["M_Z"])
    g1 = math.sqrt(1 / (1 / g1sq - 2 * sm1[0] / k * lt))
    g2 = math.sqrt(1 / (1 / g2sq - 2 * sm1[1] / k * lt))
    g3 = math.sqrt(4 * math.pi * base["alpha_s"])
    lep = lepton_masses_gev()
    m_tau = lepton_running_mass(lep["tau"], mt, inp("alpha_em"))
    rt2 = math.sqrt(2)
    return mt, [g1, g2, g3, rt2 * mt / v, rt2 * base["m_b"] / v, rt2 * m_tau / v]


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
# 6i. PART K: QUARK MASSES AND CKM FROM OVERLAPS ON THE Z3 CIRCLE (registered)
# =============================================================================
# The computation registered in registrations/PART_K_Z3_OVERLAPS.md (commit 7274f77) before
# any of its numbers was computed. Three generations sit at the Z3 points theta_k = 2 pi k/3 of a
# circle; every quark profile is the ground state of -(d - i s)^2 + a_q (1 - cos theta) with one
# shared a_q, and the Higgs that of the same operator with a_H, centred at theta_H. A constant
# hypercharge connection (holonomy Phi) enters as s = q Phi / 2 pi. Yukawas are triple overlaps;
# the four unknowns (a_q, a_H, theta_H, Phi) are scanned, never set; 8 data, 4 predictions.
K_SCALE_KEYS = ("r_uc", "r_ct", "r_ds", "r_sb")


def k_flux_units() -> Tuple[Dict[str, int], int]:
    """Hypercharges of Q, u_R, d_R, H as integers in units of their common denominator D.
    With f = Phi/(2 pi D) the shift s = q Phi/2 pi is (D q) f, and f has period 1."""
    y = {f[0]: f[3] for f in SM_FIELDS}
    q = {"Q": y["Q"], "u": -y["u^c"], "d": -y["d^c"], "H": y["H"]}
    den = 1
    for v in q.values():
        den = den * v.denominator // math.gcd(den, v.denominator)
    return {k: int(v * den) for k, v in q.items()}, den


class Z3Overlaps:
    """Profiles, Yukawa matrices and observables of the registered model, at fixed (N, M)."""

    def __init__(self, n_modes: int, m_points: int):
        if m_points <= 3 * n_modes or m_points % 36:
            raise ValueError("need M > 3N and M divisible by 36")
        self.n, self.m = n_modes, m_points
        self.units, self.den = k_flux_units()
        self.w = [cmath.exp(2 * 1j * math.pi * k / m_points) for k in range(m_points)]
        self.rows: Dict[int, List[complex]] = {}
        self.cache: Dict[Any, Any] = {}

    def _row(self, n: int) -> List[complex]:
        if n not in self.rows:
            self.rows[n] = [self.w[(n * k) % self.m] for k in range(self.m)]
        return self.rows[n]

    def ground_state(self, a: float, s: float) -> List[float]:
        """c_n, n = -N..N: ground state of T_nn = (n - s)^2 + a, T_n,n+-1 = -a/2 (D1); c_n > 0,
        2 pi sum c_n^2 = 1. Sturm bisection for the energy, then inverse iteration (T - sigma) x = b."""
        key = ("c", a, s)
        if key in self.cache:
            return self.cache[key]
        ns = range(-self.n, self.n + 1)
        d = [(n - s) ** 2 + a for n in ns]
        e2 = (a / 2) ** 2

        def below(x: float) -> int:
            cnt, q = 0, 1.0
            for k, dk in enumerate(d):
                q = dk - x - (e2 / q if k else 0)
                if q == 0:
                    q = math.ulp(abs(x) + 1)
                cnt += q < 0
            return cnt
        lo, hi = min(d) - a, min(d)
        while True:
            mid = (lo + hi) / 2
            if mid in (lo, hi):
                break
            lo, hi = (lo, mid) if below(mid) >= 1 else (mid, hi)
        sigma = lo - num("k_shift_rel") * (abs(lo) + a + 1)
        off = -a / 2
        x = [1.0] * len(d)
        for _ in range(int(num("k_inverse_iterations"))):
            # Thomas algorithm; T - sigma is positive definite since sigma lies below the spectrum
            cp, dp = [0.0] * len(d), [0.0] * len(d)
            for k in range(len(d)):
                den = d[k] - sigma - (off * cp[k - 1] if k else 0)
                cp[k] = off / den
                dp[k] = (x[k] - (off * dp[k - 1] if k else 0)) / den
            for k in range(len(d) - 1, -1, -1):
                x[k] = dp[k] - (cp[k] * x[k + 1] if k + 1 < len(d) else 0)
            big = max(abs(v) for v in x)
            x = [v / big for v in x]
        if sum(x) < 0:
            x = [-v for v in x]
        norm = math.sqrt(2 * math.pi * sum(v * v for v in x))
        c = [v / norm for v in x]
        self.cache[key] = c
        return c

    def profile(self, a: float, s: float, theta_c: float) -> List[complex]:
        """chi(theta_m - theta_c) on the M quadrature points, from its Fourier series."""
        key = ("p", a, s, theta_c)
        if key in self.cache:
            return self.cache[key]
        c = self.ground_state(a, s)
        floor = max(c) * num("k_mode_floor")
        coef = [complex()] * self.m                   # b_n at index n mod M (M > 2N + 1: no aliasing)
        for idx, cn in enumerate(c):
            if cn > floor:
                n = idx - self.n
                coef[n % self.m] = cn * cmath.exp(-1j * n * theta_c)
        vals = self._synth(coef)
        self.cache[key] = vals
        return vals

    def _synth(self, coef: List[complex]) -> List[complex]:
        """sum_k coef_k e^(2 pi i k m / L) for m = 0..L-1, L = len(coef) dividing M: a mixed-radix
        fast Fourier transform. It gives the same grid values as the direct Fourier sum."""
        size = len(coef)
        if size == 1:
            return list(coef)
        p = next((q for q in (2, 3, 5, 7) if size % q == 0), size)
        if p == size:
            stride = self.m // size
            return [sum(coef[k] * self.w[(k * j * stride) % self.m] for k in range(size)) for j in range(size)]
        sub_len = size // p
        subs = [self._synth(coef[r::p]) for r in range(p)]
        stride = self.m // size
        out = [complex()] * size
        for idx in range(size):
            k = idx % sub_len
            out[idx] = sum(subs[r][k] * self.w[(r * idx * stride) % self.m] for r in range(p))
        return out

    def profile_direct(self, a: float, s: float, theta_c: float) -> List[complex]:
        """The same grid values by the direct Fourier sum (used only to check _synth)."""
        c = self.ground_state(a, s)
        vals = [complex()] * self.m
        for idx, cn in enumerate(c):
            n = idx - self.n
            b = cn * cmath.exp(-1j * n * theta_c)
            vals = [v + b * r for v, r in zip(vals, self._row(n))]
        return vals

    def _rolled(self, vals: List[complex], shift: int) -> List[complex]:
        return [vals[(k - shift) % self.m] for k in range(self.m)]

    def quark_products(self, a_q: float, f: float):
        """conj(Psi_Q,i) Psi_q,j on the grid for both sectors (they depend on a_q and the flux only)."""
        key = ("P", a_q, f)
        if key in self.cache:
            return self.cache[key]
        third = self.m // 3
        gen = {}
        for sp in ("Q", "u", "d"):
            base = self.profile(a_q, self.units[sp] * f, 0.0)
            gen[sp] = [self._rolled(base, k * third) for k in range(3)]
        prods = {sec: [[[qi.conjugate() * qj for qi, qj in zip(gen["Q"][i], gen[sec][j])] for j in range(3)]
                       for i in range(3)] for sec in ("u", "d")}
        self.cache[key] = prods
        return prods

    def higgs(self, a_h: float, f: float, t: float) -> List[complex]:
        """Higgs profile centred at theta_H = t 2 pi/3."""
        s = self.units["H"] * f
        k = t * self.m / 3
        if math.isclose(k, round(k)):         # on a quadrature point: rotate the centred profile
            return self._rolled(self.profile(a_h, s, 0.0), round(k) % self.m)
        return self.profile(a_h, s, t * 2 * math.pi / 3)

    def yukawas(self, a_q: float, a_h: float, t: float, f: float):
        if len(self.cache) > 4096:            # bound the memory of the refinement stage
            self.cache = {}
        prods = self.quark_products(a_q, f)
        h = self.higgs(a_h, f, t)
        hc = [v.conjugate() for v in h]
        wgt = 2 * math.pi / self.m
        yu = [[wgt * sum(map(lambda p, x: p * x, prods["u"][i][j], hc)) for j in range(3)] for i in range(3)]
        yd = [[wgt * sum(map(lambda p, x: p * x, prods["d"][i][j], h)) for j in range(3)] for i in range(3)]
        return yu, yd

    def point(self, x: Sequence[float]) -> Dict[str, Any] | None:
        """Observables at search coordinates x = (log10 a_q, log10 a_H, t, f); theta_H = t 2 pi/3."""
        la_q, la_h, t, f = x
        yu, yd = self.yukawas(10 ** la_q, 10 ** la_h, t, f % 1)
        out: Dict[str, Any] = {"Y_u": yu, "Y_d": yd}
        sectors = {}
        for name, y in (("u", yu), ("d", yd)):
            big = max(abs(v) for row in y for v in row)
            if big == 0:
                return None
            yn = [[v / big for v in row] for row in y]
            h = [[sum(yn[i][k] * yn[j][k].conjugate() for k in range(3)) for j in range(3)] for i in range(3)]
            eig = hermitian_eigh(h)
            if eig is None or eig[0][0] <= 0:
                return None
            sectors[name] = (eig, yn)
        (eu, uu), (ed, ud) = sectors["u"][0], sectors["d"][0]
        v = [[sum(uu[k][a].conjugate() * ud[k][b] for k in range(3)) for b in range(3)] for a in range(3)]
        mu = [math.sqrt(e) for e in eu]
        md = [math.sqrt(e) for e in ed]
        # the four registered observables, with the formulas of ckm_observables (its ratios can divide by 0)
        obs = {"V_us": abs(v[0][1]), "V_cb": abs(v[1][2]), "V_ub": abs(v[0][2]),
               "J": (v[0][1] * v[1][2] * v[0][2].conjugate() * v[1][1].conjugate()).imag}
        out.update({"V": v, "m_u": mu, "m_d": md, "obs": obs,
                    "ratios": {"r_uc": mu[0] / mu[1], "r_ct": mu[1] / mu[2],
                               "r_ds": md[0] / md[1], "r_sb": md[1] / md[2]},
                    "Yn": {"u": sectors["u"][1], "d": sectors["d"][1]}})
        return out


def hermitian_eigh(h: List[List[complex]]):
    """Eigenvalues (ascending) and eigenvector columns of a 3x3 Hermitian matrix through its real 6x6
    embedding [[Re, -Im], [Im, Re]] (D3). None if two eigenvalues are not clearly distinct."""
    n = len(h)
    emb = [[0.0] * (2 * n) for _ in range(2 * n)]
    for i in range(n):
        for j in range(n):
            emb[i][j] = emb[i + n][j + n] = h[i][j].real
            emb[i][j + n] = -h[i][j].imag
            emb[i + n][j] = h[i][j].imag
    ev, o = jacobi_eigh(emb, num("jacobi_tol"))
    split = max(abs(ev[2 * k + 1] - ev[2 * k]) for k in range(n))
    gaps = [ev[2 * k + 2] - ev[2 * k + 1] for k in range(n - 1)]
    if min(gaps) <= num("k_degenerate_ratio") * split:
        return None
    vals, cols = [], []
    for k in range(n):
        col = [o[r][2 * k] for r in range(2 * n)]
        vec = [complex(col[r], col[r + n]) for r in range(n)]
        nrm = math.sqrt(sum(abs(z) ** 2 for z in vec))
        vals.append((ev[2 * k] + ev[2 * k + 1]) / 2)
        cols.append([z / nrm for z in vec])
    return vals, [[cols[k][r] for k in range(n)] for r in range(n)]


def k_measured(flav: Dict[str, Any], mu: float) -> Dict[str, Any]:
    """ln of the run mass ratios and their input-propagated errors at one scale, and the CKM data."""
    r = flav["ratios"][mu]
    out = {"ln": {k: math.log(r[k]) for k in K_SCALE_KEYS}, "sig": {}}
    for k in K_SCALE_KEYS:
        v2 = 0.0
        for name in FLAVOUR_UNCERTAIN:
            plus, minus = flav["varied"][name]
            v2 += ((math.log(plus[mu][k]) - math.log(minus[mu][k])) / 2) ** 2
        out["sig"][k] = math.sqrt(v2)
    out["ckm"] = {k: _comparison(k) for k in SURVEY_OBS}
    return out


def k_chi2(p: Dict[str, Any] | None, meas: Dict[str, Any]) -> float:
    if p is None:
        return math.inf
    tot = 0.0
    for k in K_SCALE_KEYS:
        tot += ((math.log(p["ratios"][k]) - meas["ln"][k]) / meas["sig"][k]) ** 2
    for k in SURVEY_OBS:
        m, up, dn = meas["ckm"][k]
        val = p["obs"][k]
        tot += ((val - m) / (up if val > m else dn)) ** 2
    return tot


_K_CONTEXT: Dict[str, Any] = {}


def _k_refine(task: Tuple[float, List[float]]) -> Tuple[float, List[float], float]:
    """One compass-search refinement (module level, so worker processes can run it)."""
    mu, x0 = task
    ctx = _K_CONTEXT
    lo, hi = ctx["range"]
    model, meas = ctx["model"], ctx["meas"][mu]

    def clamp(x: Sequence[float]) -> List[float]:
        return [min(max(x[0], lo), hi), min(max(x[1], lo), hi), x[2] % 1, x[3] % 1]
    x, val = _minimize(lambda y: k_chi2(model.point(clamp(y)), meas), list(x0), ctx["steps"], num("k_min_step"))
    return mu, clamp(x), val


def _k_refine_all(tasks: List[Tuple[float, List[float]]], workers: int) -> List[Tuple[float, List[float], float]]:
    """Refinements are independent: spread over worker processes where fork is available, else serial."""
    if workers > 1 and "fork" in multiprocessing.get_all_start_methods():
        out, t0 = [], time.perf_counter()
        with multiprocessing.get_context("fork").Pool(workers) as pool:
            for k, r in enumerate(pool.imap_unordered(_k_refine, tasks, chunksize=1), 1):
                out.append(r)
                if k % 20 == 0 or k == len(tasks):
                    print(f"  [K3 progress] {k}/{len(tasks)} refinements, {time.perf_counter() - t0:.0f} s",
                          file=sys.stderr, flush=True)
        return out
    return [_k_refine(t) for t in tasks]


def k_search(model: Z3Overlaps, meas_by_scale: Dict[float, Dict[str, Any]], la_range: Tuple[float, float],
             n_starts: int, extra_starts: Sequence[Sequence[float]] = (), workers: int = 1
             ) -> Dict[float, Dict[str, Any]]:
    """Registered search: the start grid (both scales at once), then the n_starts lowest grid points
    per scale, plus any extra starts, refined by compass search."""
    lo, hi = la_range
    step_a = (num("k_log_a_hi") - num("k_log_a_lo")) / (int(num("k_log_a_grid")) - 1)   # registered spacing
    las = [lo + k * step_a for k in range(int(round((hi - lo) / step_a)) + 1)]
    nt, nf = int(num("k_theta_grid")), int(num("k_flux_grid"))
    grid: Dict[float, List[Tuple[float, Tuple[float, ...]]]] = {mu: [] for mu in meas_by_scale}
    for la_q in las:
        for fi in range(nf):
            for la_h in las:
                for ti in range(nt):
                    x = (la_q, la_h, ti / nt, fi / nf)
                    p = model.point(x)
                    for mu, meas in meas_by_scale.items():
                        grid[mu].append((k_chi2(p, meas), x))

    tasks = []
    for mu in meas_by_scale:
        grid[mu].sort(key=lambda r: r[0])
        tasks += [(mu, list(x)) for _, x in grid[mu][:n_starts]] + [(mu, list(x)) for x in extra_starts]
    _K_CONTEXT.update({"model": model, "meas": meas_by_scale, "range": la_range,
                       "steps": [step_a, step_a, 1 / nt, 1 / nf]})
    results = _k_refine_all(tasks, workers)
    out = {}
    for mu in meas_by_scale:
        mine = [(val, x) for m_, x, val in results if m_ == mu]
        best = min(mine, key=lambda r: r[0])
        out[mu] = {"chi2": best[0], "x": best[1], "grid_best": grid[mu][0][0], "refined": [v for v, _ in mine],
                   "range": la_range}
    return out


def _k_dense_slab(task: Tuple[float, float]) -> Dict[float, List[Tuple[float, Tuple[float, ...]]]]:
    """All dense-grid points with one (log10 a_q, f): the quark products are computed once."""
    la_q, f = task
    ctx = _K_CONTEXT
    lo, hi = ctx["range"]
    na, nt = int(num("k_dense_a")), int(num("k_dense_t"))
    keep = int(num("k_dense_refine"))
    best: Dict[float, List[Tuple[float, Tuple[float, ...]]]] = {mu: [] for mu in ctx["meas"]}
    for ia in range(na):
        la_h = lo + (hi - lo) * ia / (na - 1)
        for it in range(nt):
            x = (la_q, la_h, it / nt, f)
            p = ctx["model"].point(x)
            for mu, meas in ctx["meas"].items():
                best[mu].append((k_chi2(p, meas), x))
    return {mu: sorted(v)[:keep] for mu, v in best.items()}


def k_dense_check(model: Z3Overlaps, meas: Dict[float, Dict[str, Any]], la_range: Tuple[float, float],
                  workers: int) -> Dict[float, Dict[str, Any]]:
    """Replacement for K3 (rule 5): a grid 28 times denser than the start grid, then the best
    k_dense_refine points per scale refined by the same compass search."""
    lo, hi = la_range
    na, nf = int(num("k_dense_a")), int(num("k_dense_f"))
    tasks = [(lo + (hi - lo) * i / (na - 1), j / nf) for i in range(na) for j in range(nf)]
    step_a = (num("k_log_a_hi") - num("k_log_a_lo")) / (int(num("k_log_a_grid")) - 1)
    _K_CONTEXT.update({"model": model, "meas": meas, "range": la_range,
                       "steps": [step_a, step_a, 1 / int(num("k_theta_grid")), 1 / int(num("k_flux_grid"))]})
    if workers > 1 and "fork" in multiprocessing.get_all_start_methods():
        with multiprocessing.get_context("fork").Pool(workers) as pool:
            slabs = pool.map(_k_dense_slab, tasks, chunksize=4)
    else:
        slabs = [_k_dense_slab(t) for t in tasks]
    keep = int(num("k_dense_refine"))
    out = {}
    refine_tasks = []
    for mu in meas:
        pts = sorted(r for sl in slabs for r in sl[mu])
        out[mu] = {"dense_best": pts[0][0], "n_points": len(tasks) * na * int(num("k_dense_t"))}
        refine_tasks += [(mu, list(x)) for _, x in pts[:keep]]
    for mu, x, val in _k_refine_all(refine_tasks, workers):
        if val < out[mu].get("chi2", math.inf):
            out[mu].update({"chi2": val, "x": x})
    return out


def k_box_points(n: int) -> List[List[float]]:
    """Deterministic points in the search box from the script's integer stream (seed closure_seed)."""
    draw = _IntStream(int(num("closure_seed")))
    lo, hi = num("k_log_a_lo"), num("k_log_a_hi")
    return [[lo + (hi - lo) * (draw() - 1) / 96, lo + (hi - lo) * (draw() - 1) / 96, (draw() - 1) / 97,
             (draw() - 1) / 97] for _ in range(n)]


def run_part_k(flav: Dict[str, Any], scales: Sequence[float], full_checks: bool = False) -> Dict[str, Any]:
    model = Z3Overlaps(int(num("k_fourier_modes")), int(num("k_quad_points")))
    meas = {mu: k_measured(flav, mu) for mu in scales}
    lo, hi = num("k_log_a_lo"), num("k_log_a_hi")
    res: Dict[str, Any] = {"measured": meas, "units": model.units, "flux_period_over_2pi": model.den}
    search = k_search(model, meas, (lo, hi), int(num("k_starts")))
    # boundary rule: extend once by k_boundary_extend decades on the side the best point touches
    ext = num("k_boundary_extend")
    extended = {}
    for mu, r in search.items():
        la = r["x"][:2]
        new_lo = lo - ext if any(v <= lo + num("k_min_step") for v in la) else lo
        new_hi = hi + ext if any(v >= hi - num("k_min_step") for v in la) else hi
        if (new_lo, new_hi) != (lo, hi):
            extended[mu] = k_search(model, {mu: meas[mu]}, (new_lo, new_hi), int(num("k_starts")))[mu]
    res["search"], res["extended"] = search, extended
    final = {mu: (extended[mu] if mu in extended and extended[mu]["chi2"] < search[mu]["chi2"] else search[mu])
             for mu in scales}
    res["final"] = final
    for mu, r in final.items():
        r["sigma"] = pvalue_to_sigma(chi2_pvalue(r["chi2"], 4))
        r["survives"] = r["sigma"] <= num("survival_sigma")
        p = model.point(r["x"])
        r["point_obs"] = {"ratios": p["ratios"], "obs": p["obs"]}
    # K0: the theorems, at deterministic points with no flux
    pts = k_box_points(int(num("k_check_points")))
    # points where two masses are degenerate have no defined V (D3); they are counted, not used
    gen_pts = [model.point([x[0], x[1], x[2], 0.0]) for x in pts]
    sym_pts = [model.point([x[0], x[1], t, 0.0]) for x in pts for t in (0, 1 / 2, 2)]
    k0a = max(abs(p["obs"]["J"]) for p in gen_pts if p is not None)
    k0b = min(max(abs(v) for row in p["V"] for v in row) for p in sym_pts if p is not None)
    k0c_v, k0c_r = 0.0, 0.0
    for p in gen_pts:
        if p is None:
            continue
        k0c_v = max(k0c_v, max(abs(1 - abs(p["V"][i][i])) for i in range(3)))
        rr = p["ratios"]
        k0c_r = max(k0c_r, abs(rr["r_uc"] / rr["r_ds"] - 1), abs(rr["r_ct"] / rr["r_sb"] - 1))
    res["K0"] = {"max_abs_J": k0a, "min_max_abs_V": k0b, "max_1_minus_Vii": k0c_v, "max_ratio_diff": k0c_r,
                 "degenerate": {"generic": sum(p is None for p in gen_pts), "symmetric": sum(p is None for p in sym_pts),
                                "of": (len(gen_pts), len(sym_pts))}}
    # K2: finer numerics at each best point
    fine = Z3Overlaps(int(num("k_fourier_modes_check")), int(num("k_quad_points_check")))
    res["K2"] = {mu: abs(k_chi2(fine.point(r["x"]), meas[mu]) / r["chi2"] - 1) for mu, r in final.items()}
    # K4: determinant and unitarity at each best point
    k4 = {}
    for mu, r in final.items():
        p = model.point(r["x"])
        det_rel = 0.0
        for sec, masses in (("u", p["m_u"]), ("d", p["m_d"])):
            dt = _cdet([[_Cx(z.real, z.imag) for z in row] for row in p["Yn"][sec]])
            det2 = dt.r ** 2 + dt.i ** 2
            prod = (masses[0] * masses[1] * masses[2]) ** 2
            det_rel = max(det_rel, abs(prod / det2 - 1))
        v = p["V"]
        unit = max(abs(sum(v[i][k] * v[j][k].conjugate() for k in range(3)) - (i == j))
                   for i in range(3) for j in range(3))
        k4[mu] = {"det_rel": det_rel, "unitarity": unit}
    res["K4"] = k4
    # K3 (long; run with --part-k-search-check): more starts and random starts
    if full_checks:
        k3 = {}
        by_range: Dict[Any, List[float]] = {}
        for mu, r in final.items():
            by_range.setdefault(tuple(r["range"]), []).append(mu)
        for rng, mus in by_range.items():
            chk = k_dense_check(model, {mu: meas[mu] for mu in mus}, rng, os.cpu_count() or 1)
            for mu in mus:
                k3[mu] = dict(chk[mu], lower_by=(final[mu]["chi2"] - chk[mu]["chi2"]) / final[mu]["chi2"])
        res["K3"] = k3
    return res


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
    x = {k: inp(k) for k in INPUTS}
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
    base = {k: Decimal(INPUTS[k]["value"]) for k in INPUTS}
    out = cosmology(base, prec)
    var2 = 0.0
    var2_ol = 0.0
    for name in COSMO_UNCERTAIN:
        vals = []
        for s in (1, -1):
            x = dict(base)
            x[name] = base[name] + s * Decimal(INPUTS[name]["sigma"])
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


def run(scales: Sequence[float] | None = None, prec: int | None = None,
        part_k_search_check: bool = False) -> Dict[str, Any]:
    prec = int(prec or NUMERICS["precision_digits"])
    steps = int(NUMERICS["rg_steps_per_efold"])
    grid = int(NUMERICS["phase_grid"])
    _derived_vub_over_vcb()
    cosmo = run_cosmology(prec)
    alpha_unif = alpha_from_unification()                         # Part I first: it supplies M_S
    alpha_num = alpha_numerology()
    m_susy = alpha_unif.get("M_S_for_measured_alpha", {}).get("M_S_GeV")
    if not scales:
        scales = [FlavourRunner(_float_inputs(), steps).mt_msbar] + ([m_susy] if m_susy else [])
    scales = sorted(float(v) for v in scales)
    flav = run_flavour(scales, steps, grid)
    survey = run_survey(flav, scales)
    yuk = {b: yukawa_structure_331(b) for b in (-1, 1)}
    survivors = [(r["zeros_u"], r["zeros_d"]) for r in survey[scales[0]]["classes"]
                 if r["status"] == "tested" and all(
                     next(x for x in survey[mu]["classes"]
                          if (x["zeros_u"], x["zeros_d"]) == (r["zeros_u"], r["zeros_d"]))["survives"]
                     for mu in scales)]
    symm = symmetry_search(yuk, survivors)
    closure = general_texture_closure()
    qg = quantum_gravity(cosmo, flav)
    m_gut = alpha_unif.get("M_S_for_measured_alpha", {}).get("M_GUT_GeV")
    yukawa = yukawa_relations(flav, m_susy, m_gut, qg["planck"]["E_P_GeV"])
    part_k = run_part_k(flav, scales, part_k_search_check)
    checks = self_checks(flav, cosmo, scales, steps, grid, survey, yuk)
    checks.append(("Every symmetry found reproduces its target zeros exactly (recomputed from the charges)",
                   all(sv["verified"] for e in symm["by_beta"].values() for sv in e["survivors"]
                       if sv["symmetry"] is not None), ""))
    full = frozenset((i, a) for i in range(3) for a in range(3))
    diag = frozenset((i, i) for i in range(3))
    draw = _IntStream(int(num("closure_seed")))
    r_full, r_diag = invariant_rank(full, full, draw), invariant_rank(diag, diag, draw)
    checks.append(("Invariant-rank method: general matrices give 10 physical parameters, diagonal ones 6",
                   (r_full, r_diag) == (10, 6), f"ranks {r_full}, {r_diag}"))
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
    k0 = part_k["K0"]
    checks.append(("Part K, K0a: with no flux every profile is real, so J = 0", k0["max_abs_J"] <= num("k_tol_J"),
                   f"max |J| {k0['max_abs_J']:.1e}"))
    checks.append(("Part K, K0b: no flux and the Higgs on a symmetry point give some |V_ij| = 1 (theorem D6)",
                   k0["min_max_abs_V"] >= 1 - num("k_tol_unit"),
                   f"min max|V_ij| = {k0['min_max_abs_V']:.12f}; {k0['degenerate']['symmetric']} of"
                   f" {k0['degenerate']['of'][1]} points have degenerate masses, so no V"))
    checks.append(("Part K, K0c: no flux makes the two sectors identical, V = 1 (theorem D8)",
                   k0["max_1_minus_Vii"] <= num("k_tol_unit") and k0["max_ratio_diff"] <= num("k_tol_unit"),
                   f"max |1 - |V_ii|| {k0['max_1_minus_Vii']:.1e}, ratio diff {k0['max_ratio_diff']:.1e}"))
    k2 = max(part_k["K2"].values())
    checks.append(("Part K, K2: chi^2 at the best point unchanged with N = 192, M = 864", k2 < num("k_tol_converged"),
                   f"max rel change {k2:.1e}"))
    k4d = max(v["det_rel"] for v in part_k["K4"].values())
    k4u = max(v["unitarity"] for v in part_k["K4"].values())
    checks.append(("Part K, K4: |det Y|^2 = product of the masses^2, and V unitary, at the best point",
                   k4d < num("k_tol_converged") and k4u < num("k_tol_unitarity"),
                   f"det rel diff {k4d:.1e}, |VV^dag - 1| {k4u:.1e}"))
    if "K3" in part_k:
        k3 = max(v["lower_by"] for v in part_k["K3"].values())
        checks.append(("Part K, K3 (replaced, rule 5): a 28x denser grid, best 20 refined, finds no lower minimum",
                       k3 <= num("k_tol_search"), f"largest relative improvement {k3:.1e}"))
    return {"part_k": part_k, "scales": scales, "cosmology": cosmo, "flavour": flav, "survey": survey, "yukawa_331": yuk,
            "symmetry": symm, "closure": closure, "quantum_gravity": qg, "alpha_unification": alpha_unif,
            "alpha_numerology": alpha_num, "yukawa": yukawa, "checks": checks, "precision": prec}


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
    w(f"  m_t(m_t) MS-bar from the pole mass (2-loop)    {runner.mt_msbar:.3f} GeV")
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
    w(f"    {cl['cp_impossible']:5d} of the classes with rank below 10 have J = 0 identically")
    w(f"    {len(cl['predictive_with_cp']):5d} make a prediction and allow CP violation")
    if not cl["predictive_with_cp"]:
        w("  RESULT: no texture-zero pattern of general quark mass matrices predicts anything.")
        w("    Every viable pattern has exactly as many physical parameters as there are")
        w("    observables (10), so zeros alone, however a symmetry makes them, fix nothing.")
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
        w("    That is one number (tan beta), not a calculation of the Yukawas, and it is not checked")
        w("    here against the Higgs mass.")
    w("")
    w("PART K. QUARK MASSES AND CKM FROM OVERLAPS ON THE Z3 CIRCLE (preregistered)")
    w("-" * 78)
    pk = res["part_k"]
    w("  Registered before computing: registrations/PART_K_Z3_OVERLAPS.md (commit 7274f77).")
    w("  Three generations at the Z3 points of a circle; every quark profile the ground state of")
    w("  -(d - i s)^2 + a_q (1 - cos theta) with ONE a_q for Q, u, d; the Higgs the same with a_H at")
    w("  theta_H; a hypercharge holonomy Phi, s = q Phi/2pi; Yukawas = triple overlaps, diagonalized.")
    w(f"  Flux units (6 q): Q {pk['units']['Q']}, u {pk['units']['u']}, d {pk['units']['d']}, H {pk['units']['H']};"
      f" Phi has period {2 * pk['flux_period_over_2pi']} pi.")
    w("  Unknowns a_q, a_H, theta_H, Phi: all scanned. 8 data (4 mass ratios, |V_us|, |V_cb|, |V_ub|, J):")
    w("  4 predictions, chi^2 with 4 dof. Registered expectation: excluded (theorems D6, D8; estimate D7).")
    w("  Exact results checked numerically (self-checks K0a-c): with no flux J = 0, V = 1 and the up and")
    w("  down mass ratios are equal, whatever the widths; with the Higgs on a fixed point (v7.0) some")
    w("  |V_ij| = 1. So only the holonomy can separate the two sectors.")
    for mu in res["scales"]:
        r = pk["final"][mu]
        ms = pk["measured"][mu]
        po = r["point_obs"]
        ext = " (after the registered range extension)" if mu in pk["extended"] else ""
        sig_s = (f"{r['sigma']:.1f} sigma" if math.isfinite(r["sigma"]) else
                 f"p below double precision, beyond {math.floor(pvalue_to_sigma(sys.float_info.min))} sigma")
        w(f"  mu = {mu:.0f} GeV: chi^2_min = {r['chi2']:.1f} for 4 dof, {sig_s}{ext}:"
          f" {'SURVIVES' if r['survives'] else 'EXCLUDED'}")
        w("    at the point of least chi^2 (a hypothesis test, not a determination):")
        w("      " + "  ".join(f"{k} {po['ratios'][k]:.3e} (meas {math.exp(ms['ln'][k]):.3e})" for k in K_SCALE_KEYS))
        w("      " + "  ".join(f"{k} {_fmt(po['obs'][k], 3)} (meas {_fmt(ms['ckm'][k][0], 3)})" for k in SURVEY_OBS))
    if "K3" in pk:
        for mu, v in pk["K3"].items():
            w(f"  K3 replacement at {mu:.0f} GeV: {v['n_points']} dense-grid points (best {v['dense_best']:.1f}),"
              f" best 20 refined: chi^2_min = {v['chi2']:.1f}")
    else:
        w("  K3 (search completeness) runs with --part-k-search-check; its result is in the registration document.")
    surv = [mu for mu in res["scales"] if pk["final"][mu]["survives"]]
    if surv:
        w("  RESULT: the Z3 overlap model survives at " + ", ".join(f"{m:.0f} GeV" for m in surv)
          + ": a candidate with 4 predictions, against the registered expectation.")
    else:
        w("  RESULT: excluded at every scale, as registered. The Z3 overlap geometry with one quark width and")
        w("    no typed factors cannot give the quark masses and the CKM matrix together.")
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
        "part_k": {k: v for k, v in res["part_k"].items() if k != "measured"},
        "checks": [{"name": n, "pass": ok, "detail": d} for n, ok, d in res["checks"]],
    })


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=f"STUR Physics Lab {VERSION}")
    ap.add_argument("--scales", type=float, nargs="+", default=None,
                    help="evaluation scales in GeV (default: m_t(m_t) and the superpartner scale from Part I)")
    ap.add_argument("--precision", type=int, default=None, help="Decimal digits for the cosmology")
    ap.add_argument("--json-out", type=str, default=None, help="write every number to this JSON file")
    ap.add_argument("--part-k-search-check", action="store_true",
                    help="also run Part K's search-completeness check (a 28x denser grid; minutes on 4 cores)")
    args = ap.parse_args(argv)
    t0 = time.perf_counter()
    res = run(args.scales, args.precision, args.part_k_search_check)
    print(report(res))
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            json.dump(to_jsonable(res), fh, indent=2)
    print(f"Elapsed: {time.perf_counter() - t0:.1f} s")
    return 0 if all(ok for _, ok, _ in res["checks"]) else 1


if __name__ == "__main__":
    sys.exit(main())
