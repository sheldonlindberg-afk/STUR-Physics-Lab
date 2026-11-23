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
    running above the top mass) to each benchmark 3-3-1 scale. They are then
    put into the Fritzsch six-zero texture, whose entries the masses fix exactly.
    Diagonalizing it gives the full CKM matrix for every value of the two free
    phases, and each element's band is compared with the measured value.

Run:  python3 production_v2_2.py                 (full report, about 10 s)
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
    "report_sci_below": "1e-3",       # print in scientific notation below / above these
    "report_sci_above": "1e5",
    # Scales at which the flavour bands are reported: the four 3-3-1 benchmark
    # scales of production v1. All four are always reported; none is selected.
    "evaluation_scales_GeV": ("1500", "3500", "7000", "10000"),
}


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
                "r_ds": m["d"] / m["s"], "r_sb": m["s"] / m["b"], "alpha_s": self.alpha_s(mu0)}
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
            if mu < mu0:
                raise ValueError(f"evaluation scale {mu} GeV is below m_t(m_t) = {mu0:.2f} GeV")
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
    return {"runner": central, "ratios": ratios, "scales": results}


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
                grid: int) -> List[Tuple[str, bool, str]]:
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
    scales = sorted(float(s) for s in (scales or NUMERICS["evaluation_scales_GeV"]))
    prec = int(prec or NUMERICS["precision_digits"])
    steps = int(NUMERICS["rg_steps_per_efold"])
    grid = int(NUMERICS["phase_grid"])
    _derived_vub_over_vcb()
    cosmo = run_cosmology(prec)
    flav = run_flavour(scales, steps, grid)
    checks = self_checks(flav, cosmo, scales, steps, grid)
    return {"scales": scales, "cosmology": cosmo, "flavour": flav, "checks": checks, "precision": prec}


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
            return {str(k): conv(v) for k, v in o.items() if k not in ("coef", "runner")}
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
        "checks": [{"name": n, "pass": ok, "detail": d} for n, ok, d in res["checks"]],
    })


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=f"STUR Physics Lab {VERSION}")
    ap.add_argument("--scales", type=float, nargs="+", default=None,
                    help="evaluation scales in GeV (default: the four 3-3-1 benchmark scales)")
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
