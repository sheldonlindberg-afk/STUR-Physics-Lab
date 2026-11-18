"""Hidden oracle for the Casimir-Polder campaign.
Far zone: U = -23 hbar c alpha1 alpha2 / (4 pi r^7) (Casimir and Polder 1948), near zone: London, -(3/4) w0 alpha0^2 / r^6.
Crossover: the repository's own imaginary-frequency route, U = -(1/2 pi) int dxi alpha(i xi)^2 Tr G.G with
alpha(i xi) = alpha0 w0^2/(w0^2 + xi^2) and Tr G.G = 2 e^(-2u)(3 + 6u + 5u^2 + 2u^3 + u^4)/r^6, u = xi r (src/casimir_diamonds.py P2-P3);
it is a different route from the builders' mandatory perturbation theory, so agreement is evidence of both."""
import math, random, time
import mpmath as mp

FAR, NEAR = 23 / (4 * math.pi), 0.75
LINT_TARGETS = [FAR, 1.8302, 1.83]
LINT_EXACT = [FAR, NEAR]                      # integer-built or short literals: 23/(4*math.pi), 3/4, 0.75


def ref_rho(rho):
    """-U r^7 ... : the imaginary-frequency integral in the variable s = xi r at w0 = alpha0 = 1, accurate for any rho (mpmath).
    Returns U in units alpha0^2 w0^7 for r w0 = rho."""
    mp.mp.dps = 30
    r = mp.mpf(rho)
    f = lambda s: (1 / (1 + (s / r) ** 2)) ** 2 * 2 * mp.exp(-2 * s) * (3 + 6 * s + 5 * s**2 + 2 * s**3 + s**4)
    return float(-mp.quad(f, [0, 1, 5, 20, 60, mp.inf]) / (2 * mp.pi) / r**7)


def reference(r, w0, alpha0):
    return ref_rho(r * w0) * alpha0**2 * w0**7


def cross(rw):
    def f(m):
        v, ref = m.cp_energy(rw, 1.0, 1.0), reference(rw, 1.0, 1.0)
        return abs(v / ref - 1) < 2e-4, f"derived {v:.6e}, reference {ref:.6e} ({100 * (v / ref - 1):+.4f}%)"
    return f


ORACLE = [
    ("far-zone coefficient 23/(4 pi)", lambda m: (abs(m.far_coefficient() / FAR - 1) < 1e-4, f"derived {m.far_coefficient():.6f}, target {FAR:.6f}")),
    ("near-zone coefficient 3/4 (London)", lambda m: (abs(m.near_coefficient() / NEAR - 1) < 1e-4, f"derived {m.near_coefficient():.6f}")),
] + [(f"U(r w0 = {rw}) against the imaginary-frequency route", cross(rw)) for rw in (0.05, 0.5, 1.0, 3.0, 20.0)]


def dense(m):
    """12 random log-uniform r w0 in [1e-8, 1e5] with random w0, alpha0; a fresh seed each run (printed) so nothing can be fitted to the points."""
    seed = time.time_ns() % 10**9
    rnd, worst = random.Random(seed), 0.0
    for _ in range(12):
        rho, w0, al = 10 ** rnd.uniform(-8, 5), 10 ** rnd.uniform(-1, 1), 10 ** rnd.uniform(-1, 1)
        worst = max(worst, abs(m.cp_energy(rho / w0, w0, al) / reference(rho / w0, w0, al) - 1))
    return worst < 1e-6, f"worst relative deviation {worst:.2e} over 12 random points (seed {seed})"


def coeff_tight(m):
    tc, td = -ref_rho(1e7) * 1e49 / 1e0, -ref_rho(1e-4) * 1e-24 / (1 - 1e-8 / 3)
    C, D = m.far_coefficient(), m.near_coefficient()
    return abs(C / FAR - 1) < 1e-8 and abs(D / NEAR - 1) < 1e-8, f"C rel {C / FAR - 1:.1e}, D rel {D / NEAR - 1:.1e}"


def extremes(m):
    """Fixed extreme separations, the region where a build's integration can quietly fail (the first accepted build a was low by 4e-4 below 1e-7)."""
    worst, where = 0.0, None
    for rho in (1e-8, 1e-7, 1e-6, 1e-5, 1e3, 1e4, 1e5):
        d = abs(m.cp_energy(rho, 1.0, 1.0) / ref_rho(rho) - 1)
        if d > worst:
            worst, where = d, rho
    return worst < 1e-7, f"worst relative deviation at r w0 in 1e-8 .. 1e5: {worst:.1e} at {where}"


ORACLE += [("dense random points against the accurate reference", dense), ("coefficients to 1e-8", coeff_tight),
           ("extreme separations r w0 = 1e-8 .. 1e5 to 1e-7", extremes)]


import itertools, os as _os2, sys as _sys2
_sys2.path.insert(0, _os2.path.dirname(_os2.path.abspath(__file__)))
import reference_damped as _RD


def sum_reference(k, q, a, b):
    """The auditor's independent enumeration: 24 orderings of four vertex events, intermediate energies by toggling."""
    W, E = {"A": a, "B": b}, {"k": k, "q": q}
    tot = 0.0
    for perm in itertools.permutations([("A", "k"), ("A", "q"), ("B", "k"), ("B", "q")]):
        ex, ph, den = {"A": 0, "B": 0}, {"k": 0, "q": 0}, 1.0
        for at, p in perm[:3]:
            ex[at] ^= 1
            ph[p] ^= 1
            den *= sum(W[z] for z in ex if ex[z]) + sum(E[z] for z in ph if ph[z])
        tot += 1.0 / den
    return tot / 2


def denominator_sum_check(m):
    pts = [(0.7, 1.9, 1.0, 1.0), (2.3, 0.4, 1.3, 0.6), (5.0, 3.0, 0.8, 2.2), (0.05, 40.0, 2.0, 0.3), (1e-3, 2e-3, 1.0, 1.0)]
    worst = max(abs(m.denominator_sum(*p) / sum_reference(*p) - 1) for p in pts)
    return worst < 1e-12, f"worst relative deviation from the independent 24-ordering enumeration: {worst:.1e}"


def damped_energy_check(m):
    """Finite-eps energy against the orchestrator's separable double integral (which, extrapolated to eps -> 0 with a degree-4 fit
    of five eps values, reproduces the main route at rho = 1 to 1e-8)."""
    worst, where = 0.0, None
    for rho, eps, w0, al in ((1.0, 0.5, 1.0, 1.0), (1.0, 0.25, 1.0, 1.0), (0.5, 0.4, 1.0, 1.0), (3.0, 0.5, 1.0, 1.0), (2.0, 0.6, 0.7, 1.9)):
        ref = _RD.F(rho * w0, eps * w0) * al**2 * w0**7
        d = abs(m.damped_energy(rho / w0, w0, al, eps) / ref - 1)
        if d > worst:
            worst, where = d, (rho, eps, w0, al)
    return worst < 1e-6, f"worst relative deviation over 5 points: {worst:.1e} at (r w0, eps, w0, alpha0) = {where}"


ORACLE += [("denominator_sum against the independent 24-ordering enumeration to 1e-12", denominator_sum_check),
           ("damped_energy against the independent separable double integral to 1e-6", damped_energy_check)]
