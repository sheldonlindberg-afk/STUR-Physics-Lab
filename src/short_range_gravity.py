#!/usr/bin/env python3
"""
Short-range gravity with the two-diamond experiment: how far design A could test Newton's
1/r law, against a Yukawa modification
    V(r) = -G m1 m2 / r * (1 + alpha exp(-r / lambda)).

Y1  Finite size. For two uniform spheres of radius R the Yukawa term is multiplied by
    Phi(R/lambda)^2, Phi(x) = 3 (x cosh x - sinh x) / x^3 (the shell theorem for a Yukawa
    potential: a shell of radius s acts as a point with weight sinh(s/l) / (s/l)). Derived
    symbolically; Phi -> 1 as R/lambda -> 0. Design A has R = 1.0 um, so Phi^2 differs from
    1 by less than 0.1% for lambda >= 20 um. (CHECK)
Y2  The phase. The Yukawa potential integrated along design A's branch trajectories (the same
    ramp profile that gives the 2.187 rad Newtonian phase):
        dphi(alpha, lambda) = dphi_N (1 + alpha k(lambda)),
    exactly linear in alpha. k -> 1 as lambda -> infinity (a rescaling of G), and k falls
    as exp(-gap/lambda) below the 181 um gap: k(30 um) = 4e-3, k(100 um) = 0.25,
    k(181 um) = 0.53, k(1 mm) = 0.96. (CHECK)
Y3  Statistical reach. With the phase read out to delta = 1/sqrt(N) after N runs (ideal
    projection noise, visibility 1: MODEL, optimistic), alpha_min = delta / (dphi_N k) at
    1 sigma. N = 1e4 runs (9 h at 3.24 s each): 8.6e-3 at the gap, 4.6e-3 for lambda >> gap;
    alpha = 1 for lambda > 30.6 um (22.0 um with N = 1e6, 38 days). (CHECK; MODEL readout)
Y4  Systematic floors. The phase also carries Casimir-Polder (rung 3; 7.2% of gravity's
    along design A's trajectories, the T = 0 formula holding since hbar c / k T = 1.5 cm at
    0.15 K) and the normalization G m^2 (the mass). Both enter like alpha:
      - Casimir known to a fraction f: alpha_sys = f (dphi_C / dphi_N) / k. The coefficient
        goes as K^2 R^6, so a 1% error in R alone is f = 6%.
      - Mass known to a fraction e: alpha_sys = 2 e / k.
    At the gap, f = 10% gives 0.014 and e = 1% gives 0.038, above the statistics of Y3.
    The ratio of the phases at gaps d and 2d cancels G m^2; Casimir mostly survives it
    (7% at d, 0.15% at 2d), and the ratio's sensitivity k(d) - k(2d) is computed. (CHECK;
    MODEL for f and e)
Y5  Against torsion balances, at the same 95% CL. Lee et al., PRL 124, 101101 (2020) exclude
    |alpha| = 1 for lambda < 38.6 um. Design A, absolute phase, 1e4 runs: 34.6 um with no
    systematics, 35.2 um with Casimir to 1% and the mass to 0.1%, 38.6 um at 3% / 0.3%,
    49.6 um at 10% / 1%. The gap ratio needs no mass but more runs: 50.0 um with 1e4,
    30.2 um (38.2 um with Casimir to 10%) with 1e6. (CHECK; LIT bound; MODEL readout)
    So the diamonds could edge past the torsion balance at gravitational strength: by
    about 10% in lambda with 1e4 runs, and only with Casimir to about 1% and the mass to
    about 0.1%; by 20-40% with 1e6 runs (a month). They cannot go much further: the gap is fixed at 181 um by
    Casimir and does not shrink with the mass (rung 3, P4), so exp(-gap/lambda) caps the
    reach, and a heavier diamond raises dphi_N but not that exponential. Their unique result
    remains the entanglement witness. (FOLLOWS)
Labels: CHECK, MODEL, FOLLOWS, LIT.
"""
import math
import os
import sys

import numpy as np
import sympy as sp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stur_gravity_entanglement as g
from stur_gravity_entanglement import G, HBAR, C, KB
import stur_gravity_full as GF
from stur_gravity_full import ramp_profile, trajectory_dphi

LEE2020_LAMBDA = 38.6e-6     # m, |alpha| = 1 excluded below this, 95% CL (PRL 124, 101101)
T_ENV = 0.15                 # K, the experiment's environment (src/stur_gravity_full.py BASE_ENV)
NT = 40001                   # time samples along the trajectory


_DESIGN_A = []


def design_a():
    """Design A from its one source, src/stur_gravity_full.design_a(), computed once."""
    if not _DESIGN_A:
        _DESIGN_A.append(GF.design_a())
    return dict(_DESIGN_A[0])


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


# --------------------------------------------------------------------------- Y1
def sphere_form_factor():
    """Phi(x) from the Yukawa shell theorem: a thin shell of radius s, seen from distance
    D > s, gives exp(-D/l)/D * sinh(s/l)/(s/l); averaging over a uniform ball of radius R
    with weight 3 s^2 / R^3 gives Phi(R/l)."""
    s, R, l, D, mu = sp.symbols("s R lambda D mu", positive=True)
    # shell: average of exp(-r/l)/r over the sphere |x| = s, r = |x - D z|
    r = sp.sqrt(D**2 + s**2 - 2 * D * s * mu)
    shell = sp.integrate(sp.exp(-r / l) / r / 2, (mu, -1, 1))
    shell_expected = sp.exp(-D / l) / D * sp.sinh(s / l) / (s / l)
    pts = [(3.0, 1.0, 0.5), (2.0, 1.5, 4.0), (10.0, 0.3, 0.1)]
    shell_ok = all(abs(float((shell / shell_expected).subs({D: d_, s: s_, l: l_})) - 1) < 1e-12
                   for d_, s_, l_ in pts)
    phi = sp.simplify(sp.integrate(3 * s**2 / R**3 * sp.sinh(s / l) * l / s, (s, 0, R)))
    x = sp.symbols("x", positive=True)
    phi_x = sp.simplify(phi.subs(R, x * l))
    expected = 3 * (x * sp.cosh(x) - sp.sinh(x)) / x**3
    ok = sp.simplify((phi_x - expected).rewrite(sp.exp)) == 0
    limit = sp.limit(expected, x, 0)
    return shell_ok, ok, limit, sp.lambdify(x, expected, "numpy")


def phi_num(x):
    x = np.asarray(x, float)
    small = x < 1e-3
    xs = np.where(small, 1.0, x)
    full = 3 * (xs * np.cosh(xs) - np.sinh(xs)) / xs**3
    return np.where(small, 1 + x**2 / 10, full)


# --------------------------------------------------------------------------- Y2
def _trajectory(a=None, gap=None):
    a = design_a() if a is None else a
    gap = a["gap"] if gap is None else gap
    t = np.linspace(0, a["total"], NT)
    y = 0.5 * a["dx"] * ramp_profile(t, a["hold"], a["ramp"])
    return a, gap, t, np.sqrt(gap**2 + (2 * y) ** 2)


def newton_phase(gap=None):
    a, gap, t, rc = _trajectory(gap=gap)
    return 2 * G * a["m"] ** 2 / HBAR * np.trapezoid(1 / gap - 1 / rc, t)


def yukawa_phase(lam, gap=None):
    """Phase of the Yukawa term alone, per unit alpha, with the sphere form factor."""
    a, gap, t, rc = _trajectory(gap=gap)
    f = lambda r: np.exp(-r / lam) / r
    ff = phi_num(a["R"] / lam) ** 2
    return 2 * G * a["m"] ** 2 / HBAR * ff * np.trapezoid(f(gap) - f(rc), t)


def k_of(lam, gap=None):
    return yukawa_phase(lam, gap) / newton_phase(gap)


# --------------------------------------------------------------------------- Y3
def alpha_stat(lam, runs):
    return 1 / math.sqrt(runs) / (newton_phase() * abs(k_of(lam)))


# --------------------------------------------------------------------------- Y4
def casimir_phase(gap=None):
    """Casimir-Polder's entangling phase along the same trajectories (rung 3's formula, the
    T = 0 retarded limit: hbar c / k T at 0.15 K is 1.5 cm, far above the gap)."""
    a, gap, t, rc = _trajectory(gap=gap)
    U = lambda r: g.casimir_energy(a["m"], r)
    return -2 / HBAR * np.trapezoid(U(gap) - U(rc), t)


def thermal_length():
    return HBAR * C / (KB * T_ENV)


def alpha_sys_casimir(lam, f):
    return f * abs(casimir_phase() / newton_phase()) / abs(k_of(lam))


def alpha_sys_mass(lam, e):
    return 2 * e / abs(k_of(lam))


def k_ratio(lam, factor=2.0):
    """d ln(dphi(d) / dphi(factor d)) / d alpha at alpha = 0: the gap-ratio sensitivity,
    free of G m^2."""
    gap = design_a()["gap"]
    return k_of(lam, gap) - k_of(lam, factor * gap)


# --------------------------------------------------------------------------- Y5
Z95 = 1.96                   # two-sided 95% CL, to compare with Lee et al.
RUNS = (1e4, 1e6)
ABS_CASES = [(0.0, 0.0), (0.01, 0.001), (0.03, 0.003), (0.1, 0.01)]   # (f Casimir, e mass)
F_RATIO = [0.0, 0.1]


def absolute_reach(lam, runs, f, e):
    """1-sigma alpha_min from the absolute phase at the gap: statistics, Casimir (fraction f)
    and the mass (fraction e, entering as 2e) in quadrature."""
    pN = newton_phase()
    stat = 1 / math.sqrt(runs) / pN
    cas = f * abs(casimir_phase() / pN)
    return math.sqrt(stat**2 + cas**2 + (2 * e) ** 2) / abs(k_of(lam))


def ratio_reach(lam, runs, f, factor=2.0):
    """1-sigma alpha_min from the ratio dphi(d) / dphi(factor d), runs split evenly between the
    two gaps (readout 1/sqrt(runs/2) each, MODEL), Casimir known to a fraction f. G m^2
    cancels; Casimir does not (7% of gravity at d, 0.15% at 2d)."""
    gap = design_a()["gap"]
    p1, p2 = newton_phase(gap), newton_phase(factor * gap)
    stat = math.sqrt(2 / runs) * math.hypot(1 / p1, 1 / p2)
    cas = f * abs(casimir_phase(gap) / p1 - casimir_phase(factor * gap) / p2)
    return math.hypot(stat, cas) / abs(k_ratio(lam, factor))


def lambda_at(reach, alpha, *args, lo=5e-6, hi=1.8e-4):
    """Smallest lambda below the gap at which reach(lambda, *args) <= alpha (the sensitivity
    rises with lambda there)."""
    for _ in range(50):
        mid = math.sqrt(lo * hi)
        lo, hi = (mid, hi) if reach(mid, *args) > alpha else (lo, mid)
    return math.sqrt(lo * hi)


def reach95(lam, reach, *args):
    return Z95 * reach(lam, *args)


def alpha_one_ranges():
    """Y5: the shortest lambda at which |alpha| = 1 is excluded at 95% CL, for each method."""
    out = {}
    for N in RUNS:
        for f, e in ABS_CASES:
            out[("abs", N, f, e)] = lambda_at(lambda l, *a: reach95(l, absolute_reach, *a), 1.0, N, f, e)
        for f in F_RATIO:
            out[("ratio", N, f)] = lambda_at(lambda l, *a: reach95(l, ratio_reach, *a), 1.0, N, f)
    return out


# --------------------------------------------------------------------------- main
LAMS = [20e-6, 30e-6, 38.6e-6, 50e-6, 100e-6, 300e-6, 1e-3, 1e-2]   # plus the gap, in main()


def main():
    a = design_a()
    lams = sorted(LAMS + [a["gap"]])
    banner("Y1  Finite size: the Yukawa sphere form factor")
    shell_ok, ok, lim, _ = sphere_form_factor()
    print(f"   shell of radius s acts as a point x sinh(s/l)/(s/l): {shell_ok}")
    print(f"   Phi(x) = 3 (x cosh x - sinh x) / x^3: {ok};  Phi(0) = {lim}")
    print(f"   design A: R = {a['R']*1e6:.3f} um; Phi^2 - 1 at lambda = 20 um: "
          f"{phi_num(a['R'] / 20e-6)**2 - 1:.1e}")

    banner("Y2  The phase: dphi = dphi_N (1 + alpha k(lambda))")
    pN = newton_phase()
    ref = trajectory_dphi(a["m"], a["dx"], a["gap"], a["hold"], a["ramp"])
    print(f"   dphi_N = {pN:.4f} rad (src/stur_gravity_full.py: {ref:.4f})")
    for lam in lams:
        print(f"   lambda = {lam*1e6:8.1f} um   k = {k_of(lam):.3e}")

    banner("Y3  Statistical reach (1 sigma), delta phi = 1/sqrt(N) (MODEL: ideal readout)")
    print(f"   {'lambda (um)':>12} {'N = 1e4':>10} {'N = 1e6':>10}")
    for lam in lams:
        print(f"   {lam*1e6:12.1f} {alpha_stat(lam, 1e4):10.2e} {alpha_stat(lam, 1e6):10.2e}")
    for N in RUNS:
        print(f"   alpha = 1 at 1 sigma for lambda > {lambda_at(alpha_stat, 1.0, N)*1e6:.1f} um, "
              f"N = {N:.0e} ({N * a['total'] / 3600:.0f} h of runs)")

    banner("Y4  Systematic floors, 1 sigma (MODEL: f = 10% on Casimir, e = 1% on the mass)")
    pC = casimir_phase()
    print(f"   Casimir/gravity phase = {pC / pN:+.3f};  hbar c / k T at {T_ENV} K = "
          f"{thermal_length()*100:.1f} cm (so the T = 0 formula holds)")
    print(f"   {'lambda (um)':>12} {'Casimir':>10} {'mass':>10} {'k (gap ratio d, 2d)':>22}")
    for lam in lams:
        print(f"   {lam*1e6:12.1f} {alpha_sys_casimir(lam, 0.1):10.2e} {alpha_sys_mass(lam, 0.01):10.2e}"
              f" {k_ratio(lam):22.3e}")

    banner("Y5  |alpha| = 1 at 95% CL, against Lee et al., PRL 124, 101101 (2020)")
    print(f"   torsion balance: excluded for lambda < {LEE2020_LAMBDA*1e6:.1f} um")
    r = alpha_one_ranges()
    for N in RUNS:
        print(f"   N = {N:.0e} runs:")
        for f, e in ABS_CASES:
            la = r[("abs", N, f, e)]
            print(f"      absolute phase, Casimir to {f:4.0%}, mass to {e:5.1%}: {la*1e6:5.1f} um"
                  f"  ({'shorter' if la < LEE2020_LAMBDA else 'not shorter'})")
        for f in F_RATIO:
            la = r[("ratio", N, f)]
            print(f"      gap ratio d/2d, Casimir to {f:4.0%}               : {la*1e6:5.1f} um"
                  f"  ({'shorter' if la < LEE2020_LAMBDA else 'not shorter'})")
    print("   The gap is fixed by Casimir and does not shrink with the mass, so exp(-gap/lambda)")
    print("   caps the reach; a heavier diamond raises dphi_N but not that exponential.")


if __name__ == "__main__":
    main()
