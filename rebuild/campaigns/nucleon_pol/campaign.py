"""Campaign: nucleon polarizabilities from the pion cloud, leading order heavy-baryon chiral perturbation theory (SPEC.md)."""
import math

NAME = "nucleon_pol"
MODULE = "nucleon_pol"
ALLOWED_IMPORTS = {"math", "cmath", "fractions", "itertools", "functools", "numpy", "scipy", "mpmath", "sympy"}
QUOTED_ALLOWED = []
EXPORTS = {
    "alpha_E": "alpha_E(gA, fpi, mpi, alpha) -> float: electric polarizability in MeV^-3 (SPEC section 2 convention).",
    "beta_M": "beta_M(gA, fpi, mpi, alpha) -> float: magnetic polarizability in MeV^-3.",
    "to_fm3": "to_fm3(x) -> float: x (MeV^-3) in fm^3, using hbar c = 197.3269804 MeV fm.",
}
GA, FPI, MPI, ALPHA = 1.27, 92.4, 139.57, 1 / 137.035999


def b_scaling(m):
    a = m.alpha_E(GA, FPI, MPI, ALPHA)
    ok = (abs(m.alpha_E(2 * GA, FPI, MPI, ALPHA) / a - 4) < 1e-12 and abs(m.alpha_E(GA, 2 * FPI, MPI, ALPHA) / a - 0.25) < 1e-12
          and abs(m.alpha_E(GA, FPI, 2 * MPI, ALPHA) / a - 0.5) < 1e-12 and abs(m.alpha_E(GA, FPI, MPI, 3 * ALPHA) / a - 3) < 1e-12)
    return ok, "alpha_E scales as gA^2, 1/f^2, 1/m_pi and alpha (leading order, finite loop)"


def b_ratio_constant(m):
    r = [m.beta_M(*p) / m.alpha_E(*p) for p in ((GA, FPI, MPI, ALPHA), (1.0, 80.0, 300.0, 1 / 100.0), (2.0, 120.0, 90.0, 1 / 150.0))]
    return max(r) - min(r) < 1e-12 and 0 < r[0] < 1, f"beta_M / alpha_E is a pure number: {r}"


def b_positive_dimension(m):
    a = m.alpha_E(GA, FPI, MPI, ALPHA)
    v = m.to_fm3(a)
    return a > 0 and m.beta_M(GA, FPI, MPI, ALPHA) > 0 and abs(m.to_fm3(1.0) / 197.3269804**3 - 1) < 1e-12 and 1e-5 < v < 1e-2, f"alpha_E > 0, beta_M > 0, to_fm3 is (hbar c)^3, alpha_E = {v:.3e} fm^3 is of hadronic size"


BLIND = [("alpha_E scales as gA^2, 1/f^2, 1/m_pi, alpha", b_scaling),
         ("beta_M / alpha_E is a pure number", b_ratio_constant),
         ("positive, dimensionally consistent, hadronic size", b_positive_dimension)]
