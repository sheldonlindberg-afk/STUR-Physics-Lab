"""Higgs-containing one-loop W and Z self-energies at q = 0 in R_xi gauge, MS-bar (see DERIVATION.md).

16 pi^2 h(M) = -M^2 B0(0; mH, M) + B00(0; mH, M) - A0(mH)/4   (xi drops out exactly)
Pi_WW = g^2 h(MW),  Pi_ZZ = (g/c)^2 h(MZ),  g^2 = 4 pi alpha / s^2,  c = MW/MZ.
"""
import math

import mpmath as mp

_DPS = 50


def _dps(mH, MW, MZ):
    """Working precision: the mH^2 terms cancel only between W and Z, costing ~2 log10(mH/M) digits."""
    r = max(float(mH), float(MW), float(MZ)) / min(float(mH), float(MW), float(MZ))
    return _DPS + int(2 * math.log10(r)) + 1


def _A0(m2, mu2):
    return m2 * (1 - mp.log(m2 / mu2))


def _m2A0_ratio(m1, m2, mu2):
    """(m1 A0(m1) - m2 A0(m2)) / (m1 - m2), arguments are masses squared."""
    if abs(m1 - m2) <= mp.mpf(10) ** (-30) * max(m1, m2):
        return m1 * (1 - 2 * mp.log(m1 / mu2))
    return (m1 * _A0(m1, mu2) - m2 * _A0(m2, mu2)) / (m1 - m2)


def _B0(m1, m2, mu2):
    if abs(m1 - m2) <= mp.mpf(10) ** (-30) * max(m1, m2):
        return -mp.log(m1 / mu2)
    return (_A0(m1, mu2) - _A0(m2, mu2)) / (m1 - m2)


def _B00(m1, m2, mu2):
    return (_m2A0_ratio(m1, m2, mu2) + (m1 + m2) / 2) / 4


def _h(mH, M, mu):
    """16 pi^2 Pi_VV / kappa^2 (MS-bar), mpmath."""
    mH2, M2, mu2 = mp.mpf(mH) ** 2, mp.mpf(M) ** 2, mp.mpf(mu) ** 2
    return -M2 * _B0(mH2, M2, mu2) + _B00(mH2, M2, mu2) - _A0(mH2, mu2) / 4


def _g2(MW, MZ, alpha):
    s2 = 1 - (mp.mpf(MW) / mp.mpf(MZ)) ** 2
    return 4 * mp.pi * mp.mpf(alpha) / s2


def _piW(mH, MW, MZ, alpha, mu):
    return _g2(MW, MZ, alpha) * _h(mH, MW, mu) / (16 * mp.pi ** 2)


def _piZ(mH, MW, MZ, alpha, mu):
    c2 = (mp.mpf(MW) / mp.mpf(MZ)) ** 2
    return _g2(MW, MZ, alpha) / c2 * _h(mH, MZ, mu) / (16 * mp.pi ** 2)


def _drho(mH, MW, MZ, alpha, mu):
    return _piW(mH, MW, MZ, alpha, mu) / mp.mpf(MW) ** 2 - _piZ(mH, MW, MZ, alpha, mu) / mp.mpf(MZ) ** 2


def self_energy_W(mH, MW, MZ, alpha, xi, mu):
    with mp.workdps(_dps(mH, MW, MZ)):
        return float(_piW(mH, MW, MZ, alpha, mu))


def self_energy_Z(mH, MW, MZ, alpha, xi, mu):
    with mp.workdps(_dps(mH, MW, MZ)):
        return float(_piZ(mH, MW, MZ, alpha, mu))


def rho_higgs_rel(mH, MW, MZ, alpha, xi, mu):
    with mp.workdps(_dps(mH, MW, MZ)):
        return float(_drho(mH, MW, MZ, alpha, mu) - _drho(MW, MW, MZ, alpha, mu))


def log_coefficient(MW, MZ, alpha, xi):
    """From 16 pi^2 h(M) -> (3/4) M^2 ln mH^2 + M-independent: B = g^2 (3/4)(MW^2 - MZ^2) / (16 pi^2 MW^2)."""
    with mp.workdps(_DPS):
        MW2, MZ2 = mp.mpf(MW) ** 2, mp.mpf(MZ) ** 2
        return float(_g2(MW, MZ, alpha) * mp.mpf(3) / 4 * (MW2 - MZ2) / (16 * mp.pi ** 2 * MW2))


PROVENANCE = {
    "self_energy_W": ("derived", "seagull + H-phi + H-W diagrams from |D Phi|^2 in R_xi, PV reduction, MS-bar; xi cancels"),
    "self_energy_Z": ("derived", "same diagrams with kappa = g/c, M = MZ"),
    "rho_higgs_rel": ("derived", "Pi_WW/MW^2 - Pi_ZZ/MZ^2 at mH minus at MW; poles (-3/4 M^2/eps) are mH-independent"),
    "log_coefficient": ("derived", "analytic B = g^2 a (MW^2-MZ^2)/(16 pi^2 MW^2), a = 3/4 = M^2-coefficient of ln mH^2 in the large-mH "
                        "expansion of 16 pi^2 h (hand expansion, DERIVATION 5; sympy limit and numerical limit of rho_higgs_rel in __main__)"),
}


def _route_euclid(mH, MW, MZ, alpha, xi):
    """Second route: 4D Euclidean radial integral with explicit R_xi propagators (DERIVATION section 6(i))."""
    mH2, W2, Z2 = mp.mpf(mH) ** 2, mp.mpf(MW) ** 2, mp.mpf(MZ) ** 2
    xi = mp.mpf(xi)

    def I(K, h2, M2):
        a = K / (4 * (K + h2)) - K / (4 * (K + h2) * (K + xi * M2))
        b = -M2 * (1 / ((K + h2) * (K + M2)) - (1 - xi) * (K / 4) / ((K + h2) * (K + M2) * (K + xi * M2)))
        return K * (a + b)

    f = lambda K: (I(K, mH2, W2) - I(K, mH2, Z2)) - (I(K, W2, W2) - I(K, W2, Z2))
    # integrate in u = ln K up to K_max (the leading O(K) pieces cancel, so this needs high working precision),
    # then add the tail of f ~ C/K^2 analytically: int_{Kmax}^inf C/K^2 = f(Kmax) Kmax
    lo = mp.log(min(W2, mH2)) - 25
    hi = mp.log(max(mH2, Z2)) + 30
    val = mp.quad(lambda u: f(mp.e ** u) * mp.e ** u, mp.linspace(lo, hi, int(hi - lo) + 1))
    Kmax = mp.e ** hi
    val += f(Kmax) * Kmax
    return _g2(MW, MZ, alpha) * val / (16 * mp.pi ** 2 * W2)


if __name__ == "__main__":
    import sympy as sp
    MW, MZ, ALPHA = 80.38, 91.19, 1 / 128.0
    with mp.workdps(90):
        for mh in (50.0, 125.0, 300.0, 1000.0):
            for xi in (1.0, 0.4, 3.0, 0.0):
                print(f"mH={mh:7.1f} xi={xi}: rho_higgs_rel={rho_higgs_rel(mh, MW, MZ, ALPHA, xi, MW): .12e}"
                      f"  euclid route={float(_route_euclid(mh, MW, MZ, ALPHA, xi)): .12e}")
    # B by sympy series of the closed form (route ii)
    mH, M, mu, L = sp.symbols('mH M mu L', positive=True)
    A0 = lambda m2: m2 * (1 - sp.log(m2 / mu**2))
    h = -M**2 * (A0(mH**2) - A0(M**2)) / (mH**2 - M**2) \
        + ((mH**2 * A0(mH**2) - M**2 * A0(M**2)) / (mH**2 - M**2) + (mH**2 + M**2) / 2) / 4 - A0(mH**2) / 4
    D = mH / 2 * sp.diff(h, mH)                              # d(16 pi^2 h)/d ln mH^2
    coef = sp.limit(sp.diff(D, M) / (2 * M), mH, sp.oo)      # its M^2-dependence at mH -> oo
    print("sympy: lim d/dM^2 [d(16pi^2 h)/d ln mH^2] =", coef, " -> B = g^2 coef (MW^2-MZ^2)/(16 pi^2 MW^2) =",
          float(_g2(MW, MZ, ALPHA) * float(coef) * (MW**2 - MZ**2) / (16 * mp.pi**2 * MW**2)))
    print("log_coefficient:", log_coefficient(MW, MZ, ALPHA, 1.0),
          " slope at 1e5-1e6 MW:", (rho_higgs_rel(1e6 * MW, MW, MZ, ALPHA, 1.0, MW) - rho_higgs_rel(1e5 * MW, MW, MZ, ALPHA, 1.0, MW)) / mp.log(100))
    # numerical limit of Delta rho_rel / ln(mH^2/MW^2) taken from rho_higgs_rel itself (DERIVATION section 5)
    B = log_coefficient(MW, MZ, ALPHA, 1.0)
    print("numerical limit from rho_higgs_rel (B =", B, "):")
    prev = None
    for n in (2, 4, 8, 16, 32, 64):
        mh = MW * 10.0 ** n
        Lh = 2 * n * math.log(10)
        r = rho_higgs_rel(mh, MW, MZ, ALPHA, 1.0, MW)
        line = f"  mH = 1e{n:<2d} MW: ratio/B = {r / Lh / B:.10f}"
        if prev is not None:
            # ratio = B + C/L: one Richardson step on (L, 2L) removes the 1/L term
            line += (f"   Richardson 2*ratio(2L)-ratio(L), /B = {(2 * r / Lh - prev[1] / prev[0]) / B:.12f}"
                     f"   secant slope/B = {(r - prev[1]) / (Lh - prev[0]) / B:.12f}")
        print(line)
        prev = (Lh, r)
