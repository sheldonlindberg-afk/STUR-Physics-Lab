"""Stage `photon` (build 2026-11-b): the electromagnetic coupling from M_Z to zero momentum.

Postulates: SPEC.md section 11. Derivation: DERIVATION_photon.md (same directory); equation numbers are cited
below. Measured and quoted numbers come from `inputs`, read inside the functions; rung 1 is called as
`gauge331.<function>` at call time. `inputs.ALPHA_0` is not read by any export (only printed for comparison
under `__main__`).
"""
import math
from fractions import Fraction

import inputs
import toolkit
import gauge331

PROVENANCE = {
    "vacuum_polarization": ("derived", "one fermion loop from the QED Feynman rules in dimensional regularization:"
                                       " trace, Feynman parameter, Wick rotation give a transverse Pi^{mu nu} with"
                                       " Pi(q^2) - Pi(0) = (2 alpha/pi) int_0^1 dx x(1-x) ln(1 - x(1-x) s/m^2); the"
                                       " pole, gamma_E and mu cancel in the subtraction. Sign from the resummed"
                                       " propagator (screening for s < 0). Real part integrated in closed form by"
                                       " parts and polynomial division (eq. 1.4); exact-rational Taylor series"
                                       " (eq. 1.5) for |s| <= m^2. Checked against the regulator-free dispersion"
                                       " integral over the tree-level cut R(s) (eq. 1.7)"),
    "dalpha_lep": ("derived", "each vertex carries Q, so the loop scales as Q^2: sum over e, mu, tau of Q^2"
                              " vacuum_polarization(MZ_MEAS^2, m_l), Q = component 2 of"
                              " gauge331.triplet_charges(X_L, variant) with the SPEC section 2 lepton X_L"
                              " (eq. 2.1)"),
    "alpha0_inv": ("derived", "SPEC section 11's relation 1/alpha-hat = (1 - alpha0 L - H)/alpha0 is linear in"
                              " 1/alpha0: 1/alpha0 = (ALPHA_MZ_INV + L)/(1 - H), L = dalpha_lep(), H = DALPHA_HAD"
                              " + DALPHA_CONV (+ DALPHA_LEP_HIGHER if higher), the quoted/measured terms being"
                              " read from inputs (eq. 3.1); checked by bisection on the unsolved relation"),
}

_SERIES_RANGE = 1          # |s/m^2| up to which the Taylor series (1.5) is used instead of the closed form


# ------------------------------------------------------------------------------------------
# the one-fermion loop
# ------------------------------------------------------------------------------------------
def _series(t):
    """Eq. (1.5): -(2/pi) sum_{n>=1} a_n t^n/n, a_n = int_0^1 [x(1-x)]^(n+1) dx = ((n+1)!)^2/(2n+3)! (exact)."""
    a = Fraction(1, 6)                                   # a_0 = int_0^1 x(1-x) dx
    total, power, n = 0.0, 1.0, 0
    while True:
        a *= Fraction(n + 2, 2 * (2 * n + 5))            # a_{n+1}/a_n
        n += 1
        power *= t
        term = float(a) * power / n
        total += term
        if abs(term) <= abs(total) * 2.0 ** -60 or term == 0.0:
            break
    return -2 * total / math.pi


def _closed(t):
    """Eq. (1.4): the real part of the Feynman-parameter integral in closed form, b = 1 - 4/t."""
    b = 1 - 4 / t
    constant = -Fraction(8, 3)
    if b > 0:
        root = math.sqrt(b)
        log = math.log((1 + root) ** 2 * abs(t) / 4)     # = ln|(1 + root)/(1 - root)|, without cancellation
        bracket = float(constant) + b + (3 - b) * root / 2 * log
    elif b < 0:
        c = -b
        root = math.sqrt(c)
        bracket = float(constant) - c + (3 + c) * root * math.atan(1 / root)
    else:
        raise ValueError("s = 4 m^2 is excluded (threshold)")
    return bracket / (3 * math.pi)


def vacuum_polarization(s, m):
    """Delta alpha(s)/alpha of one Dirac fermion of mass m (GeV), unit charge; s in GeV^2 (> 0 timelike)."""
    if m <= 0:
        raise ValueError("the fermion mass must be positive")
    t = s / (m * m)
    if abs(t) <= _SERIES_RANGE:
        return _series(t)
    return _closed(t)


# ------------------------------------------------------------------------------------------
# the leptons at M_Z and alpha at q = 0
# ------------------------------------------------------------------------------------------
def _lepton_X(variant):
    """SPEC section 2: X_L = -1/3 (beta = -1/sqrt3), -2/3 (beta = +1/sqrt3)."""
    table = {"-1/sqrt3": Fraction(-1, 3), "+1/sqrt3": Fraction(-2, 3)}
    return table[variant]


def _charged_lepton_charge(variant="-1/sqrt3"):
    """Component 2 of the lepton triplet, from rung 1 (a Fraction)."""
    return gauge331.triplet_charges(_lepton_X(variant), variant)[1]


def dalpha_lep():
    """One-loop leptonic Delta alpha(M_Z^2)/alpha (eq. 2.1)."""
    q = _charged_lepton_charge()
    s = inputs.MZ_MEAS ** 2
    return sum(float(q * q) * vacuum_polarization(s, m) for m in (inputs.M_E, inputs.M_MU, inputs.M_TAU))


def _beyond_one_lepton_loop(higher):
    """H of eq. (3.1): the terms of Delta alpha-hat that are not proportional to alpha(0)."""
    extra = inputs.DALPHA_HAD + inputs.DALPHA_CONV
    if higher:
        extra += inputs.DALPHA_LEP_HIGHER
    return extra


def alpha0_inv(higher=True):
    """1/alpha at q^2 = 0 from 1/alpha-hat(M_Z) (eq. 3.1)."""
    return (inputs.ALPHA_MZ_INV + dalpha_lep()) / (1 - _beyond_one_lepton_loop(higher))


# ------------------------------------------------------------------------------------------
# self-check: second routes (DERIVATION_photon.md sections 1.6, 2, 3)
# ------------------------------------------------------------------------------------------
def _dispersion(s, m, n=2 * 10 ** 5 + 1):
    """Eq. (1.7): -(t/3pi) PV int_0^inf dv tanh^2 v (3 - tanh^2 v)/(4 cosh^2 v - t), s' = 4 m^2 cosh^2 v.

    No loop integral, no regulator: the cut R(s') = beta(3 - beta^2)/2 and a once-subtracted dispersion relation."""
    t = s / (m * m)
    top = math.log(abs(t) + 4) / 2 + 25                  # the integrand has fallen by e^-50 beyond the plateau

    def numerator(v):
        th = math.tanh(v)
        return th * th * (3 - th * th)

    def plain(v):
        return numerator(v) / (4 * math.cosh(v) ** 2 - t)

    def integrate(f, lo, hi):
        dx = (hi - lo) / (n - 1)
        return toolkit.trapezoid([f(lo + i * dx) for i in range(n)], dx)

    if t < 4:
        integral = integrate(plain, 0.0, top)
    else:
        v0 = math.acosh(math.sqrt(t) / 2)

        def regular(v):                                   # numerator/(4 sinh(v + v0)): the pole factored out
            return numerator(v) / (4 * math.sinh(v + v0))

        def folded(u):
            if u == 0.0:
                h = 1e-5
                return (regular(v0 + h) - regular(v0 - h)) / h        # 2 G'(v0)
            return (regular(v0 + u) - regular(v0 - u)) / math.sinh(u)

        integral = integrate(folded, 0.0, v0) + integrate(plain, 2 * v0, top)
    return -t * integral / (3 * math.pi)


def _feynman_numeric(s, m, n=2 * 10 ** 5 + 1):
    """Eq. (1.2) by the trapezoid rule; only where the integrand is smooth (s < 4 m^2)."""
    t = s / (m * m)
    dx = 1.0 / (n - 1)
    ys = []
    for i in range(n):
        x = i * dx
        w = x * (1 - x)
        ys.append(w * math.log(abs(1 - w * t)))
    return 2 * toolkit.trapezoid(ys, dx) / math.pi


def _alpha0_inv_by_root(higher=True):
    """SPEC 11's relation, unsolved, handed to toolkit.bisect: (1 - L/x - H) x - 1/alpha-hat = 0 in x = 1/alpha0."""
    L, H = dalpha_lep(), _beyond_one_lepton_loop(higher)
    f = lambda x: (1 - L / x - H) * x - inputs.ALPHA_MZ_INV
    return toolkit.bisect(f, inputs.ALPHA_MZ_INV, 10 * inputs.ALPHA_MZ_INV)


def _alpha0_inv_by_iteration(higher=True, steps=60):
    L, H = dalpha_lep(), _beyond_one_lepton_loop(higher)
    x = inputs.ALPHA_MZ_INV
    for _ in range(steps):
        x = inputs.ALPHA_MZ_INV / (1 - L / x - H)
    return x


if __name__ == "__main__":
    print("== vacuum_polarization: closed form / series  vs  dispersion integral (1.7)  [vs Feynman integral (1.2)] ==")
    mz2 = inputs.MZ_MEAS ** 2
    probes = [(-7.0, 0.3), (2.0, 0.9), (-1e-2, 1.0), (0.5, 1.0), (-1.0, 1.0), (1.0, 1.0), (3.0, 1.0), (3.9, 1.0),
              (5.0, 1.0), (-1e8, 1.0), (1e8, 1.0),
              (mz2, inputs.M_E), (mz2, inputs.M_MU), (mz2, inputs.M_TAU), (-mz2, inputs.M_E)]
    for s, m in probes:
        main, disp = vacuum_polarization(s, m), _dispersion(s, m)
        line = f"  s/m^2 = {s / m / m: .6e}: main {main: .12e}   dispersion {disp: .12e}   rel {abs(disp / main - 1):.1e}"
        if s < 4 * m * m and abs(s / m / m) < 1e4:
            fe = _feynman_numeric(s, m)
            line += f"   Feynman-numeric {fe: .12e} rel {abs(fe / main - 1):.1e}"
        print(line)
    print("  series (1.5) vs closed form (1.4) at the junction: t = +1:", _series(1.0), _closed(1.0),
          "  t = -1:", _series(-1.0), _closed(-1.0))
    print("  leading term: vp(-1e-4 m^2) / (1e-4/(15 pi)) =", vacuum_polarization(-1e-4, 1.0) * 15 * math.pi / 1e-4)
    slope = (vacuum_polarization(1e10, 1.0) - vacuum_polarization(1e8, 1.0)) / math.log(100)
    print("  high-energy slope in ln s x 3 pi:", slope * 3 * math.pi, " (derived: 1)")

    print("== dalpha_lep ==")
    L = dalpha_lep()
    leading = sum((math.log(mz2 / ml ** 2) - float(Fraction(5, 3))) / (3 * math.pi)
                  for ml in (inputs.M_E, inputs.M_MU, inputs.M_TAU))
    disp_sum = sum(_dispersion(mz2, ml) for ml in (inputs.M_E, inputs.M_MU, inputs.M_TAU))
    print("  lepton charge from rung 1:", _charged_lepton_charge("-1/sqrt3"), _charged_lepton_charge("+1/sqrt3"))
    print("  dalpha_lep (closed form):", L)
    print("  second route, dispersion integrals summed:", disp_sum, " rel", abs(disp_sum / L - 1))
    print("  leading logarithm sum (ln(MZ^2/m^2) - 5/3)/(3 pi):", leading, " difference", L - leading,
          " expected -sum 6 m^2/MZ^2/(3 pi) =",
          -sum(6 * ml ** 2 / mz2 for ml in (inputs.M_E, inputs.M_MU, inputs.M_TAU)) / (3 * math.pi))

    print("== alpha0_inv ==")
    for higher in (True, False):
        a = alpha0_inv(higher)
        print(f"  higher={higher}: closed form {a!r};  second route bisect {_alpha0_inv_by_root(higher)!r};"
              f"  iteration {_alpha0_inv_by_iteration(higher)!r}")
        print(f"     alpha0 x dalpha_lep = {L / a:.8f};  derived/measured (1/inputs.ALPHA_0, comparison only) ="
              f" {a * inputs.ALPHA_0:.8f}")
    shift = inputs.DALPHA_HAD_ERR * alpha0_inv() / (1 - _beyond_one_lepton_loop(True))
    print("  shift of 1/alpha(0) from DALPHA_HAD_ERR alone:", shift)
