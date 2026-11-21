"""Auditor's independent route: exact-d Feynman-parameter integrals (no PV reduction, no 1/d tensor reduction),
my own Feynman rules (AUDIT.md section 1).  Units: Pi per kappa^2, times 1/(16 pi^2).

  Pi_a (seagull)      = -A0(mH^2)/4
  Pi_b (H-Goldstone)  = +C2(mH^2, xi M^2)          C2 = g^{mu nu} coeff of int k k /(D_H D_phi)
  Pi_c (H-gauge)      = -M^2 [ B0(mH^2, M^2) - (1-xi) C3(mH^2, M^2, xi M^2) ]
with, in MS-bar (Delta_UV dropped), from the exact-d formula
  int l^mu l^nu/(l^2-D)^n = (-1)^(n-1) i/(4pi)^(d/2) g/2 Gamma(n-d/2-1)/Gamma(n) D^(1-n+d/2):
  A0 = m^2 (1 - ln m^2),  B0 = -int_0^1 ln D,  C2 = 1/2 int_0^1 D (1 - ln D),  C3 = 1/2 int_simplex (-ln D).
"""
import mpmath as mp

mp.mp.dps = 30


def A0(a, mu2):
    return a * (1 - mp.log(a / mu2))


def B0(a, b, mu2):
    return -mp.quad(lambda x: mp.log((x * a + (1 - x) * b) / mu2), [0, 1])


def C2(a, b, mu2):
    return mp.quad(lambda x: (x * a + (1 - x) * b) * (1 - mp.log((x * a + (1 - x) * b) / mu2)), [0, 1]) / 2


def C3(a, b, c, mu2):
    f = lambda x: mp.quad(lambda y: -mp.log((x * a + y * b + (1 - x - y) * c) / mu2), [0, 1 - x])
    return mp.quad(f, [0, 1]) / 2


def h(mH, M, xi, mu, parts=False):
    m2, M2, mu2, xi = mp.mpf(mH) ** 2, mp.mpf(M) ** 2, mp.mpf(mu) ** 2, mp.mpf(xi)
    pa = -A0(m2, mu2) / 4
    pb = C2(m2, xi * M2, mu2)
    pc = -M2 * (B0(m2, M2, mu2) - ((1 - xi) * C3(m2, M2, xi * M2, mu2) if xi != 1 else 0))
    return (pa, pb, pc) if parts else pa + pb + pc


def g2(MW, MZ, alpha):
    return 4 * mp.pi * alpha / (1 - (mp.mpf(MW) / MZ) ** 2)


def piW(mH, MW, MZ, alpha, xi, mu):
    return g2(MW, MZ, alpha) * h(mH, MW, xi, mu) / (16 * mp.pi ** 2)


def piZ(mH, MW, MZ, alpha, xi, mu):
    return g2(MW, MZ, alpha) / (mp.mpf(MW) / MZ) ** 2 * h(mH, MZ, xi, mu) / (16 * mp.pi ** 2)


def drho(mH, MW, MZ, alpha, xi, mu):
    return piW(mH, MW, MZ, alpha, xi, mu) / mp.mpf(MW) ** 2 - piZ(mH, MW, MZ, alpha, xi, mu) / mp.mpf(MZ) ** 2


def rho_rel(mH, MW, MZ, alpha, xi, mu):
    return drho(mH, MW, MZ, alpha, xi, mu) - drho(MW, MW, MZ, alpha, xi, mu)


# second independent route: 4D Euclidean radial integral of the double difference, my own integrand
def euclid_rel(mH, MW, MZ, alpha, xi):
    """Wick: int d^4k/(2pi)^4 F(k^2) = i/(16pi^2) int_0^inf K dK F(-K); k^mu k^nu -> g k^2/4 (4D; polynomial differences cancel)."""
    xi = mp.mpf(xi)

    def I(K, m2, M2):
        DH, DV, DP = -(K + m2), -(K + M2), -(K + xi * M2)          # k^2 - m^2 with k^2 = -K
        ksq = -K
        sea = -mp.mpf(1) / 4 * (1 / DH)                              # Pi_a integrand: -1/4 * 1/(k^2-m^2)
        gold = (ksq / 4) / (DH * DP)                                 # Pi_b: k k/(DH DP) -> k^2/4
        gauge = -M2 * (1 / (DH * DV) - (1 - xi) * (ksq / 4) / (DH * DV * DP))
        return K * (sea + gold + gauge)

    m2, W2, Z2 = mp.mpf(mH) ** 2, mp.mpf(MW) ** 2, mp.mpf(MZ) ** 2
    f = lambda K: (I(K, m2, W2) - I(K, m2, Z2)) - (I(K, W2, W2) - I(K, W2, Z2))
    with mp.workdps(80):
        lo, hi = mp.log(min(W2, m2)) - 30, mp.log(max(m2, Z2)) + 40
        val = mp.quad(lambda u: f(mp.e ** u) * mp.e ** u, mp.linspace(lo, hi, int(hi - lo) + 1))
        val += f(mp.e ** hi) * mp.e ** hi                            # tail ~ C/K^2
    # Pi/M^2 difference: g^2/MW^2 [h(W)-h(Z)] since c^2 MZ^2 = MW^2 ; overall 1/(16pi^2) from the Wick measure
    return g2(MW, MZ, alpha) * val / (16 * mp.pi ** 2 * W2)
