"""Higgs part of Sirlin's Delta r at one loop (Feynman gauge, MS-bar). See DERIVATION.md for every formula used here.

Pi_V(q^2) = (g^2 / (16 pi^2 c_V^2)) h(q^2; m_H, M_V),   c_W = 1, c_Z = c,
h = -A0(m_H)/4 - M_V^2 B0(q^2; m_H, M_V) + B00(q^2; m_H, M_V)   (seagull, H-V loop, H-Goldstone loop).
"""
import math
import mpmath

DPS = 40


def _couplings(MW, MZ, alpha):
    c2 = mpmath.mpf(MW) ** 2 / mpmath.mpf(MZ) ** 2
    s2 = 1 - c2
    g2 = 4 * mpmath.pi * mpmath.mpf(alpha) / s2          # e = g s, alpha = e^2/(4 pi)
    return g2, c2, s2


def _feyn_integrals(q2, m1, m2):
    """I0 = int_0^1 ln X, I1 = int_0^1 X ln X, Xint = int_0^1 X, X = (1-x) m1^2 + x m2^2 - x(1-x) q2 (all in GeV units, mu = 1)."""
    q2, a, b = mpmath.mpf(q2), mpmath.mpf(m1) ** 2, mpmath.mpf(m2) ** 2
    if q2 >= (mpmath.sqrt(a) + mpmath.sqrt(b)) ** 2:
        raise ValueError("q^2 at or above threshold: self-energy not real")
    X = lambda x: (1 - x) * a + x * b - x * (1 - x) * q2
    xc = a / (a + b)
    pts = [0, xc, 1]
    I0 = mpmath.quad(lambda x: mpmath.log(X(x)), pts)
    I1 = mpmath.quad(lambda x: X(x) * mpmath.log(X(x)), pts)
    Xint = (a + b) / 2 - q2 / 6
    return I0, I1, Xint


def _h(q2, mH, M, mu):
    """h(q^2; m_H, M) in MS-bar at scale mu (mpf)."""
    m2, M2, lmu = mpmath.mpf(mH) ** 2, mpmath.mpf(M) ** 2, mpmath.log(mpmath.mpf(mu) ** 2)
    I0, I1, Xint = _feyn_integrals(q2, mH, M)
    A0 = m2 * (1 - (mpmath.log(m2) - lmu))
    B0 = -(I0 - lmu)
    B00 = (Xint - (I1 - lmu * Xint)) / 2
    return -A0 / 4 - M2 * B0 + B00


def _sigma(q2, mH, MV, MW, MZ, alpha, mu, cV2):
    with mpmath.workdps(DPS):
        g2, c2, s2 = _couplings(MW, MZ, alpha)
        return g2 / (16 * mpmath.pi ** 2 * cV2(c2)) * _h(q2, mH, MV, mu)


def sigma_W(q2, mH, MW, MZ, alpha, mu):
    return float(_sigma(q2, mH, MW, MW, MZ, alpha, mu, lambda c2: 1))


def sigma_Z(q2, mH, MW, MZ, alpha, mu):
    return float(_sigma(q2, mH, MZ, MW, MZ, alpha, mu, lambda c2: c2))


def _delta_r_H(mH, MW, MZ, alpha, mu):
    """Delta r_H = [Pi_W(MW^2)-Pi_W(0)]/MW^2 + (c^2/s^2)[Pi_Z(MZ^2)/MZ^2 - Pi_W(MW^2)/MW^2], with Pi_V/M_V^2 = (K/MW^2) h."""
    g2, c2, s2 = _couplings(MW, MZ, alpha)
    K = g2 / (16 * mpmath.pi ** 2)
    MW2, MZ2 = mpmath.mpf(MW) ** 2, mpmath.mpf(MZ) ** 2
    hW_MW = _h(MW2, mH, MW, mu)
    hW_0 = _h(0, mH, MW, mu)
    hZ_MZ = _h(MZ2, mH, MZ, mu)
    return K / MW2 * (hW_MW - hW_0 + c2 / s2 * (hZ_MZ - hW_MW))


def delta_r_higgs_rel(mH, MW, MZ, alpha, mu):
    with mpmath.workdps(DPS):
        return float(_delta_r_H(mH, MW, MZ, alpha, mu) - _delta_r_H(MW, MW, MZ, alpha, mu))


def _log_coeff_h(q2, M2):
    """Coefficient of ln m_H^2 in h(q^2; m_H, M) for m_H -> infinity (DERIVATION section 4): 3 M^2/4 + q^2/12."""
    return mpmath.mpf(3) / 4 * M2 + q2 / 12


def log_coefficient(MW, MZ, alpha):
    with mpmath.workdps(DPS):
        g2, c2, s2 = _couplings(MW, MZ, alpha)
        K = g2 / (16 * mpmath.pi ** 2)
        MW2, MZ2 = mpmath.mpf(MW) ** 2, mpmath.mpf(MZ) ** 2
        lW = _log_coeff_h(MW2, MW2)
        lW0 = _log_coeff_h(0, MW2)
        lZ = _log_coeff_h(MZ2, MZ2)
        return float(K / MW2 * (lW - lW0 + c2 / s2 * (lZ - lW)))


PROVENANCE = {
    "sigma_W": ("derived", "Feynman-gauge H seagull + H-W + H-phi loops, MS-bar, Feynman-parameter quadrature (DERIVATION 1-2)"),
    "sigma_Z": ("derived", "same for Z: H seagull + H-Z + H-chi loops (DERIVATION 1-2)"),
    "delta_r_higgs_rel": ("derived", "Delta r_H from bare g0, s0 and pole-mass shifts (DERIVATION 3), minus its value at mH = MW"),
    "log_coefficient": ("derived", "large-mH expansion of the Feynman-parameter integrals: (11/12) alpha/(4 pi s^2) (DERIVATION 4)"),
}


if __name__ == "__main__":
    import numpy as np
    MW, MZ, AL = 80.38, 91.19, 1 / 128.0
    s2 = 1 - MW ** 2 / MZ ** 2
    g2 = 4 * math.pi * AL / s2
    xs, ws = np.polynomial.legendre.leggauss(400)

    def gl(f, a, b):
        return sum(w * f(0.5 * (b - a) * x + 0.5 * (b + a)) for x, w in zip(xs, ws)) * 0.5 * (b - a)

    def A0(m, mu):
        return m * m * (1 - math.log(m * m / mu ** 2))

    def B0(p2, m1, m2, mu):          # double-precision Gauss-Legendre, independent of mpmath route
        X = lambda x: (1 - x) * m1 ** 2 + x * m2 ** 2 - x * (1 - x) * p2
        xc = m1 ** 2 / (m1 ** 2 + m2 ** 2)
        return -(gl(lambda x: math.log(X(x) / mu ** 2), 0, xc) + gl(lambda x: math.log(X(x) / mu ** 2), xc, 1))

    def B00_pv(p2, m0, m1, mu):       # Passarino-Veltman reduction (Denner), p2 != 0
        b0 = B0(p2, m0, m1, mu)
        b1 = (A0(m0, mu) - A0(m1, mu) - (p2 - m1 ** 2 + m0 ** 2) * b0) / (2 * p2)
        return (A0(m1, mu) + 2 * m0 ** 2 * b0 + (p2 + m0 ** 2 - m1 ** 2) * b1 + m0 ** 2 + m1 ** 2 - p2 / 3) / 6

    print("Route 2 (i): self-energies, quadrature vs PV reduction")
    for mH in (50.0, 125.2, 400.0):
        for q2 in (0.3 * MW ** 2, MW ** 2):
            hw = -A0(mH, MW) / 4 - MW ** 2 * B0(q2, mH, MW, MW) + B00_pv(q2, mH, MW, MW)
            print(f"  mH={mH:7.1f} q2={q2:9.1f}  sigma_W {sigma_W(q2, mH, MW, MZ, AL, MW): .12e}  PV {g2 / (16 * math.pi ** 2) * hw: .12e}")
        hz = -A0(mH, MW) / 4 - MZ ** 2 * B0(MZ ** 2, mH, MZ, MW) + B00_pv(MZ ** 2, mH, MZ, MW)
        print(f"  mH={mH:7.1f} q2=MZ^2      sigma_Z {sigma_Z(MZ ** 2, mH, MW, MZ, AL, MW): .12e}  PV {g2 / (16 * math.pi ** 2 * (MW / MZ) ** 2) * hz: .12e}")

    print("Route 2 (ii): large-mH asymptotics  Delta r_H(mH) - Delta r_H(mH') vs B*ln(mH^2/mH'^2)")
    B = log_coefficient(MW, MZ, AL)
    print(f"  log_coefficient B = {B:.12e};  (11/12) alpha/(4 pi s^2) = {11 / 12 * AL / (4 * math.pi * s2):.12e}")
    K = AL / (4 * math.pi * s2)
    for mH in (1e3, 1e4, 1e5):
        a = delta_r_higgs_rel(mH, MW, MZ, AL, MW)
        b = delta_r_higgs_rel(10 * mH, MW, MZ, AL, MW)
        # constant check: Delta r_H(mH) - (11/12) K (ln(mH^2/mu^2) - 5/6) should become mH-independent
        with mpmath.workdps(DPS):
            full = float(_delta_r_H(mH, MW, MZ, AL, MW)) - 11 / 12 * K * (math.log(mH ** 2 / MW ** 2) - 5 / 6)
        print(f"  mH={mH:8.0e}: slope {(b - a) / math.log(100):.10e}  ratio to B {(b - a) / math.log(100) / B:.8f}   "
              f"remainder of full Delta r_H after asymptotic form: {full:.6e}")
    print("Route 2 (iii): mu independence and values")
    for mH in (125.0, 300.0, 1000.0):
        print(f"  mH={mH:6.1f}: {delta_r_higgs_rel(mH, MW, MZ, AL, MW):.12e}  (mu=5 MW) {delta_r_higgs_rel(mH, MW, MZ, AL, 5 * MW):.12e}")
    print(f"  sigma_W(0) {sigma_W(0.0, 200.0, MW, MZ, AL, MW):.12e}  sigma_W(1e-6) {sigma_W(1e-6, 200.0, MW, MZ, AL, MW):.12e}")
