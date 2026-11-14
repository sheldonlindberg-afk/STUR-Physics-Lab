"""photon: the electromagnetic coupling from M_Z to zero momentum (SPEC.md section 11).

Derivation (one-loop self-energy, on-shell subtraction, closed form, series) and the second routes
(direct quadrature, dispersion relation, asymptote, bisection): DERIVATION_photon.md.
Inputs are read as inputs.NAME at call time; inputs.ALPHA_0 is never read.
"""
import math
from fractions import Fraction

import inputs
import toolkit
import gauge331

PROVENANCE = {
    "vacuum_polarization": ("derived", "one-loop fermion loop in dim. reg.: transverse, Pi = -(2 alpha/pi) Int u(1-u)"
                                       " [2/eps - ... - ln(Delta/mu^2)], Delta = m^2 - u(1-u)s; on-shell subtraction"
                                       " leaves (2/pi) Int_0^1 u(1-u) ln|1 - u(1-u)s/m^2| du (sign: screening);"
                                       " integrated by parts to (1/pi)[-8/9 + B/3 + beta(3-B)/6 ln|(1+beta)/(1-beta)|],"
                                       " B = 1 - 4m^2/s = beta^2 (arctan branch for B < 0), the log evaluated as"
                                       " ln((1+beta)^2 |s|/4m^2) so no digits are lost at |s| >> m^2;"
                                       " power series for |s| < m^2/2"),
    "dalpha_lep": ("derived", "sum over e, mu, tau of Q^2 vacuum_polarization(MZ_MEAS^2, m_l); Q = component 2 of"
                              " gauge331.triplet_charges(X_L = -1/3, '-1/sqrt3') (rung 1), Q^2 = 1"),
    "alpha0_inv": ("derived", "SPEC 11 relation 1/alphahat = (1 - a L - C)/a is linear in 1/a:"
                              " 1/a = (ALPHA_MZ_INV + dalpha_lep())/(1 - C), C = DALPHA_HAD + DALPHA_CONV"
                              " (+ DALPHA_LEP_HIGHER if higher); the relation and the inputs DALPHA_CONV,"
                              " DALPHA_LEP_HIGHER are quoted inputs (PDG; Steinhauser 1998), DALPHA_HAD is measured"),
}


def _series(x):
    """-(2/pi) sum_{n>=1} x^n/n ((n+1)!)^2/(2n+3)!, for |x| < 4 (used for small |x|)."""
    total, power, coeff, n = 0.0, x, 1.0 / 30, 1
    while True:
        term = power * coeff / n
        total += term
        if abs(term) <= 1e-18 * abs(total) or n > 400:
            break
        coeff *= (n + 2) / (2.0 * (2 * n + 5))
        power *= x
        n += 1
    return -2 * total / math.pi


def _closed(x):
    """(2/pi) Int_0^1 u(1-u) ln|1 - u(1-u)x| du in closed form; B = 1 - 4/x."""
    B = 1 - 4.0 / x
    if B >= 0:
        beta = math.sqrt(B)
        if beta == 0:
            return -8.0 / (9 * math.pi)                    # the finite threshold limit
        # |1 - beta| = |1 - B|/(1 + beta) = (4/|x|)/(1 + beta): no cancellation when beta -> 1 (|x| >> 1)
        log = math.log((1 + beta) ** 2 * abs(x) / 4)
        return (-8.0 / 9 + B / 3 + beta * (3 - B) / 6 * log) / math.pi
    b = math.sqrt(-B)
    return (-8.0 / 9 + B / 3 + b * (3 - B) / 3 * math.atan(1 / b)) / math.pi


def vacuum_polarization(s, m):
    """One-loop Delta alpha(s)/alpha of one Dirac fermion of mass m (GeV), unit charge; s in GeV^2."""
    if not m > 0:
        raise ValueError("vacuum_polarization: m must be positive")
    x = s / (m * m)
    if x == 0:
        return 0.0
    if abs(x) < 0.5:
        return _series(x)
    return _closed(x)


def _lepton_charge():
    """Charged lepton = component 2 of the lepton triplet (SPEC 2: X_L = -1/3 for beta = -1/sqrt3)."""
    return Fraction(gauge331.triplet_charges(Fraction(-1, 3), "-1/sqrt3")[1])


def dalpha_lep():
    """The leptons' one-loop Delta alpha(M_Z^2)/alpha."""
    q2 = float(_lepton_charge() ** 2)
    s = inputs.MZ_MEAS ** 2
    return math.fsum(q2 * vacuum_polarization(s, ml) for ml in (inputs.M_E, inputs.M_MU, inputs.M_TAU))


def _constant_part(higher):
    c = inputs.DALPHA_HAD + inputs.DALPHA_CONV
    if higher:
        c += inputs.DALPHA_LEP_HIGHER
    return c


def alpha0_inv(higher=True):
    """1/alpha(q^2 = 0) from 1/alphahat(M_Z) = (1 - alpha(0) L - C)/alpha(0)."""
    return (inputs.ALPHA_MZ_INV + dalpha_lep()) / (1 - _constant_part(higher))


# ------------------------------------------------------------------------------------------
# second routes (DERIVATION_photon.md 1g, 2, 3)
# ------------------------------------------------------------------------------------------
def _feynman_quadrature(x, n=2 * 10 ** 5 + 1):
    """(2/pi) Int_0^1 u(1-u) ln|1 - u(1-u)x| du by the trapezoid rule (no closed form, no series)."""
    du = 1.0 / (n - 1)
    ys = []
    for i in range(n):
        u = i * du
        t = u * (1 - u)
        a = abs(1 - t * x)
        ys.append(t * math.log(a) if a > 0 else 0.0)
    return 2 / math.pi * toolkit.trapezoid(ys, du)


def _dispersion(x, n=2 * 10 ** 5 + 1):
    """-(x/6pi) Int_0^{pi/2} sin(th) cos^2(th) (1 + sin^2(th)/2)/(1 - x sin^2(th)/4) dth, for x < 4."""
    dth = (math.pi / 2) / (n - 1)
    ys = []
    for i in range(n):
        sn, cs = math.sin(i * dth), math.cos(i * dth)
        ys.append(sn * cs * cs * (1 + sn * sn / 2) / (1 - x * sn * sn / 4))
    return -x / (6 * math.pi) * toolkit.trapezoid(ys, dth)


if __name__ == "__main__":
    print("== vacuum_polarization(x m^2, m = 1): main | Feynman quadrature | dispersion integral")
    for x in (-1e6, -100.0, -7.0 / 0.09, -1.0, -0.3, -0.01, 0.01, 0.3, 1.0, 2.0 / 0.81, 3.5):
        print(f"  x = {x:12.5g}: {vacuum_polarization(x, 1.0):+.12e} | {_feynman_quadrature(x):+.12e} |"
              f" {_dispersion(x):+.12e}")
    print("== above threshold (dispersion route needs a principal value; quadrature has log singularities)")
    for x in (4.5, 10.0, 1e3, 1e6):
        print(f"  x = {x:12.5g}: {vacuum_polarization(x, 1.0):+.12e} | {_feynman_quadrature(x):+.12e}")
    print("== series vs closed form in the overlap")
    for x in (-3.0, -1.0, -0.5, 0.5, 1.0, 3.0):
        print(f"  x = {x:5.1f}: series {_series(x):+.15e}, closed {_closed(x):+.15e}")
    print("== leading term -x/(15 pi) and the asymptote (ln|x| - 5/3)/(3 pi)")
    print(f"  x = -1e-4: {vacuum_polarization(-1e-4, 1.0):.9e} vs {1e-4 / (15 * math.pi):.9e}")
    for x in (-1e10, 1e10, -1e14, 1e14, -1e20, 1e20):
        print(f"  x = {x:g}: {vacuum_polarization(x, 1.0):.12f} vs {(math.log(abs(x)) - 5.0 / 3) / (3 * math.pi):.12f}")

    want = 1 / (3 * math.pi)
    for lo in (1e8, 1e12, 1e18):
        sl = [(vacuum_polarization(sg * 100 * lo, 1.0) - vacuum_polarization(sg * lo, 1.0)) / math.log(100) / want - 1
              for sg in (-1, 1)]
        print(f"  slope in ln|x| over [{lo:g}, {100 * lo:g}] / (1/3pi) - 1: spacelike {sl[0]:+.2e}, timelike {sl[1]:+.2e}"
              f" (expected O(1/x): {6 / lo:.1e})")
    print("== dalpha_lep")
    s = inputs.MZ_MEAS ** 2
    q = _lepton_charge()
    q_other = gauge331.triplet_charges(Fraction(-2, 3), "+1/sqrt3")[1]
    print(f"  lepton charge (rung 1): {q} (variant -1/sqrt3), {q_other} (variant +1/sqrt3)")
    asym = 0.0
    for name, ml in (("e", inputs.M_E), ("mu", inputs.M_MU), ("tau", inputs.M_TAU)):
        a = (math.log(s / (ml * ml)) - 5.0 / 3) / (3 * math.pi)
        asym += a
        print(f"  {name:3s}: closed {vacuum_polarization(s, ml):.12f}, asymptote {a:.12f}")
    L = dalpha_lep()
    print(f"  dalpha_lep() = {L:.12f}; asymptote sum = {asym:.12f}")

    print("== alpha0_inv")
    for higher in (True, False):
        main = alpha0_inv(higher)
        C = _constant_part(higher)
        root = toolkit.bisect(lambda a: (1 - a * L - C) / a - inputs.ALPHA_MZ_INV,
                              1 / (2 * inputs.ALPHA_MZ_INV), 1 / inputs.ALPHA_MZ_INV)
        back = (1 - L / main - C) * main
        print(f"  higher={higher!s:5s}: 1/alpha(0) = {main:.9f}; bisect route {1 / root:.9f};"
              f" relation rebuilt 1/alphahat = {back:.9f} (input {inputs.ALPHA_MZ_INV});"
              f" Delta alpha_lep(M_Z^2) = {L / main + (inputs.DALPHA_LEP_HIGHER if higher else 0.0):.8f}")
    shift = alpha0_inv() * inputs.DALPHA_HAD_ERR / (1 - _constant_part(True))
    print(f"  DALPHA_HAD_ERR moves 1/alpha(0) by +-{shift:.5f}")
