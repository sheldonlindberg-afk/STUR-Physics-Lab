"""Higgs-mass dependence of Delta r at one loop (see DERIVATION.md)."""
import math
import mpmath as mp

PROVENANCE = {
    "sigma_W": ("derived", "V-H + phi-H + seagull, Feynman gauge, MS-bar (DERIVATION s2)"),
    "sigma_Z": ("derived", "same with Z/phi0 couplings"),
    "delta_r_higgs_rel": ("derived", "Pi_W(MW^2)-Pi_W(0) and mixing-angle shift (DERIVATION s3)"),
    "log_coefficient": ("derived", "coefficient of ln mH^2 from the pole structure (DERIVATION s4)"),
}

DPS = 90  # local working precision (mp.workdps), enough for mH = 1 GeV .. 1e14 MW


def _pts():
    return [mp.mpf(0), mp.mpf("0.5")] + [1 - mp.mpf(10) ** (-k) for k in range(1, 45)] + [mp.mpf(1)]


def _A0(m2, mu2):
    return m2 * (1 - mp.log(m2 / mu2)) if m2 != 0 else mp.mpf(0)


def _integrals(q2, mH2, M2, mu2):
    """Return (B0 finite part, int Delta(1-ln Delta/mu^2)) with Delta_x = x M^2 + (1-x) mH^2 - x(1-x) q^2."""
    D = lambda x: x * M2 + (1 - x) * mH2 - x * (1 - x) * q2
    B = -mp.quad(lambda x: mp.log(D(x) / mu2), _pts())
    S = mp.quad(lambda x: D(x) * (1 - mp.log(D(x) / mu2)), _pts())
    return B, S


def _pi_core(q2, mH, M2, mu, c2inv, g2):
    q2, mH2, mu2 = mp.mpf(q2), mp.mpf(mH) ** 2, mp.mpf(mu) ** 2
    M2 = mp.mpf(M2)
    B, S = _integrals(q2, mH2, M2, mu2)
    return g2 * c2inv / (16 * mp.pi**2) * (-M2 * B + S / 2 - _A0(mH2, mu2) / 4)


def _g2(MW, MZ, alpha):
    s2 = 1 - mp.mpf(MW) ** 2 / mp.mpf(MZ) ** 2
    return 4 * mp.pi * mp.mpf(alpha) / s2, s2


def _sW(q2, mH, MW, MZ, alpha, mu):
    g2, s2 = _g2(MW, MZ, alpha)
    return _pi_core(q2, mH, mp.mpf(MW) ** 2, mu, 1, g2)


def _sZ(q2, mH, MW, MZ, alpha, mu):
    g2, s2 = _g2(MW, MZ, alpha)
    return _pi_core(q2, mH, mp.mpf(MZ) ** 2, mu, 1 / (1 - s2), g2)


def sigma_W(q2, mH, MW, MZ, alpha, mu):
    with mp.workdps(DPS):
        return float(_sW(q2, mH, MW, MZ, alpha, mu))


def sigma_Z(q2, mH, MW, MZ, alpha, mu):
    with mp.workdps(DPS):
        return float(_sZ(q2, mH, MW, MZ, alpha, mu))


def _dr(mH, MW, MZ, alpha, mu):
    MW2, MZ2 = mp.mpf(MW) ** 2, mp.mpf(MZ) ** 2
    s2 = 1 - MW2 / MZ2
    c2 = 1 - s2
    pw_M = _sW(MW2, mH, MW, MZ, alpha, mu)
    pw_0 = _sW(0, mH, MW, MZ, alpha, mu)
    pz_M = _sZ(MZ2, mH, MW, MZ, alpha, mu)
    return (pw_M - pw_0) / MW2 + c2 / s2 * (pz_M / MZ2 - pw_M / MW2)


def delta_r_higgs_rel(mH, MW, MZ, alpha, mu):
    if mH == MW:
        return 0.0
    with mp.workdps(DPS):
        return float(_dr(mH, MW, MZ, alpha, mu) - _dr(MW, MW, MZ, alpha, mu))


def log_coefficient(MW, MZ, alpha):
    with mp.workdps(DPS):
        return _log_coefficient(MW, MZ, alpha)


def _log_coefficient(MW, MZ, alpha):
    g2, s2 = _g2(MW, MZ, alpha)
    c2 = 1 - s2
    # coefficient of L = ln(mH^2/mu^2) in Pi_V: (g^2/16pi^2)(3/4 M^2 + q^2/12) (x 1/c^2 for Z)
    kW = mp.mpf(3) / 4 + mp.mpf(1) / 12          # Pi_W(MW^2)/MW^2
    kZ = (mp.mpf(3) / 4 + mp.mpf(1) / 12) / c2   # Pi_Z(MZ^2)/MZ^2
    b = mp.mpf(1) / 12                           # [Pi_W(MW^2)-Pi_W(0)]/MW^2
    return float(g2 / (16 * mp.pi**2) * (b + c2 / s2 * (kZ - kW)))


if __name__ == "__main__":
    MW, MZ, al = 80.38, 91.19, 1 / 128.0
    print("B (derived):", log_coefficient(MW, MZ, al))
    f = lambda h: delta_r_higgs_rel(h, MW, MZ, al, MW)
    print("slope 1e5-1e6 MW:", (f(1e6 * MW) - f(1e5 * MW)) / math.log(100.0))
    # second route: q^2=0, closed form B0(0;m1,m2)=(A0(m1)-A0(m2))/(m1^2-m2^2) (finite part, same A0 convention)
    m1, m2, mu2 = mp.mpf(200) ** 2, mp.mpf(MW) ** 2, mp.mpf(MW) ** 2
    mp.mp.dps = DPS
    B, _ = _integrals(0, m1, m2, mu2)
    Bc = (_A0(m1, mu2) - _A0(m2, mu2)) / (m1 - m2)
    print("B0(0) quad vs closed:", B, Bc)
    print("delta_r(125,300,1000):", [f(h) for h in (125.0, 300.0, 1000.0)])
