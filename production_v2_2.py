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
    "M_W": {"value": "80.3692", "sigma": "0.0133", "unit": "GeV", "source": "PDG 2024, world average (pole)"},
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
    "m_h": {"value": ("125.20", "0.11", "0.11"), "source": "PDG 2024, Higgs boson mass (combined)"},
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
    "higgs_xt_points": 13,            # stop-mixing grid X_t/M_S from 0 to sqrt(12) (Part K)
    "higgs_ms_search_efolds": 40,     # search range in ln(M_S) above m_t for the backwards reading
    "higgs_iterations": 50,           # bisection steps for that reading
    "crit_tol": "1e-10",              # relative tolerance of the root solves (Part L)
    "crit_iterations": 40,
    "check_b0_points": 200000,       # midpoint quadrature points for the B0 check
    "check_b0_tol": "1e-5",          # (the integrand has integrable log singularities above threshold)
    "crit_yt_step": "1e-2",           # first relative step in y_t when bracketing beta_lambda = 0
    "check_fd_rel_step": "1e-5",      # finite-difference step for the first-law check
    "check_fd_tol": "1e-8",
    "report_sci_below": "1e-3",       # print in scientific notation below / above these
    "report_sci_above": "1e5",
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
    quoted coefficients above plus the gauge b_ij from the field content."""
    base = yukawa_rhs("SM")
    gn = float(GUT_NORM)
    k = 16 * math.pi ** 2
    b2 = [[float(c) for c in row] for row in sm_two_loop_b()]
    dt = [float(c) for c in GAUGE_2L_YT]
    c = [float(v) for v in YT_2L]
    l2 = [(float(a), p) for a, *p in LAMBDA_2L]

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
        out.append(dl)
        return out
    return rhs


def sm_state_at_mt(overrides: Dict[str, float] | None = None) -> Tuple[float, float, float, List[float]]:
    """(m_t(m_t), v, M_t/m_t(m_t), [g1, g2, g3, y_t, y_b, y_tau]) at m_t(m_t), from the inputs
    (with optional changes, for propagating their errors)."""
    x = _float_inputs(overrides)
    runner = FlavourRunner(x, int(num("rg_steps_per_efold")))
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


def critical_lambda(state: List[float], mt: float, mu: float, loops: int, steps: int | None = None) -> float:
    """The lambda(m_t) for which lambda(mu) = 0. Bracket: lambda = 0 (it runs negative) and the
    smallest of y_t^2 / 2^n, n = 1, 2, ..., above which lambda(mu) is positive."""
    def f(lam0: float) -> float:
        return _lambda_at(state, lam0, mt, mu, loops, steps)
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
                           matched: bool) -> float:
    """Invert lambda(mu) = M_h^2/(2V^2) [+ lambda^(1)] for the pole mass M_h."""
    tree = math.sqrt(2 * lam) * v
    if not matched:
        return tree

    def f(mh: float) -> float:
        return mh * mh / (2 * v * v) + lambda_one_loop(mh, mt, mw, mz, v, mu) - lam
    lo, hi = tree, tree
    step = num("crit_yt_step")
    while f(lo) > 0:
        lo *= 1 - step
    while f(hi) < 0:
        hi *= 1 + step
    return _bracketed_root(f, lo, hi, num("crit_tol"), int(num("crit_iterations")))


def matched_couplings(overrides: Dict[str, float] | None, mh: float, matched: bool):
    """State at m_t(m_t) with y_t matched to the pole mass (QCD conversion of the script plus the
    one-loop electroweak part, which depends on M_h), and the mass inputs for the lambda matching."""
    mt, v, pole_ratio, st = sm_state_at_mt(overrides)
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
    if not mh:
        mt, v, _, st, ms_ = matched_couplings(overrides, 0, False)
        mh = math.sqrt(2 * critical_lambda(st, mt, mu, loops, steps)) * v
    lam = 0
    for _ in range(int(num("crit_iterations")) if matched else 1):
        mt, v, _, st, ms_ = matched_couplings(overrides, mh, matched)
        lam = critical_lambda(st, mt, mu, loops, steps)
        new = higgs_mass_from_lambda(lam, ms_[0], ms_[1], ms_[2], v, mt, matched)
        done = abs(new - mh) < num("crit_tol") * mh
        mh = new
        if done:
            break
    return {"m_h": mh, "lambda_mt": lam, "yt_mt": st[3]}


def sm_criticality(planck_gev: float) -> Dict[str, Any]:
    """lambda(M_P) = 0 (Froggatt-Nielsen 1996; Shaposhnikov-Wetterich 2010): one condition at the
    Planck scale fixes m_h from the measured top mass and alpha_s. Both Planck masses (G only)."""
    out: Dict[str, Any] = {}
    m_red = planck_gev / math.sqrt(8 * math.pi)
    out["planck"] = {"M_P": planck_gev, "M_P_reduced": m_red}
    rows = []
    for name, mu in (("M_P", planck_gev), ("M_P reduced", m_red)):
        for loops in (1, 2):
            r = predict_higgs_mass(None, mu, loops, False)
            rows.append({"scale": name, "mu": mu, "loops": loops, "matched": False, **r})
    out["tree_matching"] = [r for r in rows if r["scale"] == "M_P" and r["loops"] == 2][0]
    central = {"scale": "M_P", "mu": planck_gev, "loops": 2, "matched": True,
               **predict_higgs_mass(None, planck_gev, 2, True, mh_start=out["tree_matching"]["m_h"])}
    rows.append(central)
    out["rows"] = rows
    # input errors: M_t and alpha_s dominate; M_W enters only through the matching
    var = {}
    for name in ("M_t", "alpha_s_MZ", "M_W"):
        var[name] = predict_higgs_mass({name: inp(name) + sig(name)}, planck_gev, 2, True,
                                       mh_start=central["m_h"])["m_h"] - central["m_h"]
    out["sigma_inputs"] = var
    out["sigma_total"] = math.sqrt(sum(d ** 2 for d in var.values()))
    out["central"] = central
    # both conditions at once, lambda(M_P) = 0 and beta_lambda(M_P) = 0: solve for lambda(m_t) and y_t(m_t)
    mt, v, pole_ratio, st, masses = matched_couplings(None, central["m_h"], True)
    rhs2 = sm_rge(2)

    def beta_at_crit(yt0: float) -> Tuple[float, float]:
        s = list(st)
        s[3] = yt0
        lam = critical_lambda(s, mt, planck_gev, 2)
        top = run_sm(s + [lam], mt, planck_gev, 2)
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
    out["state_mt"] = (mt, v, masses)
    return out


def sm_lambda_profile(crit: Dict[str, Any], m_h: float) -> Dict[str, Any]:
    """lambda(mu) at two loops for a given Higgs pole mass (one-loop matching at m_t): its value at
    M_P and where it turns negative. Called by the report with the measured m_h."""
    mt, v, _, st, ms_ = matched_couplings(None, m_h, True)
    lam0 = m_h ** 2 / (2 * v ** 2) + lambda_one_loop(m_h, ms_[0], ms_[1], ms_[2], v, mt)
    mp = crit["planck"]["M_P"]
    top = run_sm(st + [lam0], mt, mp, 2)
    lo, hi = math.log(mt), math.log(mp)
    if top[6] >= 0:
        return {"lambda_MP": top[6], "beta_MP": sm_rge(2)(top, 6)[6], "mu_zero": math.nan}
    for _ in range(int(num("crit_iterations"))):
        mid = (lo + hi) / 2
        if run_sm(st + [lam0], mt, math.exp(mid), 2)[6] > 0:
            lo = mid
        else:
            hi = mid
    return {"lambda_MP": top[6], "beta_MP": sm_rge(2)(top, 6)[6], "mu_zero": math.exp((lo + hi) / 2)}


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


def run(scales: Sequence[float] | None = None, prec: int | None = None) -> Dict[str, Any]:
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
    higgs = higgs_mass_mssm(flav, alpha_unif, yukawa)
    crit = sm_criticality(qg["planck"]["E_P_GeV"])
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
    mt_c, _, _, st_c, _ = matched_couplings(None, crit["central"]["m_h"], True)
    lam_fine = critical_lambda(st_c, mt_c, crit["planck"]["M_P"], 2, steps=2 * steps)
    rel = abs(lam_fine / crit["central"]["lambda_mt"] - 1)
    checks.append(("Criticality solve converged (step count doubled)", rel < num("check_rg_tol"),
                   f"rel change {rel:.1e}"))
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
    return {"scales": scales, "cosmology": cosmo, "flavour": flav, "survey": survey, "yukawa_331": yuk,
            "symmetry": symm, "closure": closure, "quantum_gravity": qg, "alpha_unification": alpha_unif,
            "alpha_numerology": alpha_num, "yukawa": yukawa, "higgs": higgs, "criticality": crit,
            "checks": checks,
            "precision": prec}


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
        w("  Running: two-loop SM (gauge b_ij from the field content; y_t and lambda two-loop terms quoted from")
        w("  Buttazzo et al. 2013, cross-checked below). Matching at mu = m_t(m_t) to the pole masses M_h, M_t,")
        w("  M_W, M_Z and G_F: tree level, and one loop (their appendix A, Passarino-Veltman functions in closed")
        w("  form; checked: the mu dependence of each threshold is exactly the one-loop RGE).")
        w("      condition                 loops   matching   lambda(m_t)   predicted M_h (GeV)")
        for r_ in cr["rows"]:
            w(f"      lambda({r_['scale']:<11}) = 0       {r_['loops']}      {'one loop' if r_['matched'] else 'tree    '}"
              f"   {r_['lambda_mt']:.5f}       {r_['m_h']:8.2f}")
        si = cr["sigma_inputs"]
        tm = cr["tree_matching"]
        w(f"  Two loops, one-loop matching: M_h = {c_['m_h']:.2f} GeV +/- {cr['sigma_total']:.2f}"
          f" (inputs: M_t {si['M_t']:+.2f}, alpha_s {si['alpha_s_MZ']:+.2f}, M_W {si['M_W']:+.3f})")
        w(f"      the one-loop matching moves it by {c_['m_h'] - tm['m_h']:+.2f} GeV: at mu = m_t(m_t) both one-loop")
        w("      thresholds (lambda and the electroweak part of y_t) nearly vanish, so the tree-level result stood")
        w(f"      measured M_h = {mh:.2f} +/- {mh_up:.2f} GeV: the prediction is {c_['m_h'] - mh:.1f} GeV high,"
          f" {(c_['m_h'] - mh) / math.hypot(cr['sigma_total'], mh_up):.1f} sigma on the input errors")
        w("      Still not included: two-loop matching (QCD x top-Yukawa terms in lambda and y_t), the three-loop")
        w("      QCD top-mass conversion, three-loop running.")
        d_ = cr["double"]
        w("  Both conditions at the Planck scale, lambda(M_P) = 0 and beta_lambda(M_P) = 0, fix two numbers:")
        w(f"      M_h = {d_['m_h']:.1f} GeV and M_t = {d_['M_t']:.1f} GeV"
          f" (measured {mh:.1f} and {inp('M_t'):.2f}; QCD pole/MS-bar ratio of the measured top kept)")
        pr = sm_lambda_profile(cr, mh)
        w(f"  Read backwards, with the measured M_h (one-loop matching): lambda(M_P) = {pr['lambda_MP']:+.4f},"
          f" beta_lambda(M_P) = {pr['beta_MP']:+.1e}")
        if math.isfinite(pr["mu_zero"]):
            w(f"      lambda turns negative at mu = {pr['mu_zero']:.2e} GeV: the electroweak vacuum is not the")
            w("      lowest state. Whether it is long-lived (metastable) needs the tunnelling rate, not")
            w("      calculated here.")
        w(f"  RESULT: one condition at the Planck scale gives the Higgs mass to"
          f" {100 * abs(c_['m_h'] / mh - 1):.0f} percent with nothing adjusted:")
        w(f"    {c_['m_h']:.1f} GeV against {mh:.2f}. The one-loop matching does not close the gap, so at this")
        w("    order the gap is real: the measured Higgs mass makes lambda slightly negative at M_P and the SM")
        w("    vacuum is not stable. The top mass dominates the input error; the second condition")
        w("    (beta_lambda = 0) lands near the measured top mass.")
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
    })


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=f"STUR Physics Lab {VERSION}")
    ap.add_argument("--scales", type=float, nargs="+", default=None,
                    help="evaluation scales in GeV (default: m_t(m_t) and the superpartner scale from Part I)")
    ap.add_argument("--precision", type=int, default=None, help="Decimal digits for the cosmology")
    ap.add_argument("--json-out", type=str, default=None, help="write every number to this JSON file")
    args = ap.parse_args(argv)
    t0 = time.perf_counter()
    res = run(args.scales, args.precision)
    print(report(res))
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            json.dump(to_jsonable(res), fh, indent=2)
    print(f"Elapsed: {time.perf_counter() - t0:.1f} s")
    return 0 if all(ok for _, ok, _ in res["checks"]) else 1


if __name__ == "__main__":
    sys.exit(main())
