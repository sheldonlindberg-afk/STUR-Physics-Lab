"""One-loop Higgs-containing contributions to Pi_WW(0), Pi_ZZ(0) and Delta rho (see DERIVATION.md)."""
import math
import mpmath as mp

PROVENANCE = {
    "self_energy_W": ("derived", "H-W bubble + H-phi bubble + H seagull in R_xi gauge, MS-bar, divided-difference closed forms"),
    "self_energy_Z": ("derived", "H-Z bubble + H-phi0 bubble + H seagull in R_xi gauge, MS-bar"),
    "rho_higgs_rel": ("derived", "Pi_WW/MW^2 - Pi_ZZ/MZ^2 at mH minus at mH=MW"),
    "log_coefficient": ("derived", "coefficient of ln mH^2 from large-mH expansion of the loop integrals"),
}

DPS = 50


def _dps(mH, MW, MZ):
    """Working precision: the m_H^2 terms cancel between W and Z, costing ~2 log10(mH/M) digits; add 3 per decade."""
    r = max(abs(math.log10(float(mH) / float(MW))), abs(math.log10(float(mH) / float(MZ))))
    return DPS + int(3 * r)


def _dd(ders, nodes):
    """Divided difference (with confluent nodes) of a function given by its derivatives ders[k](x)."""
    nodes = sorted(nodes)
    n = len(nodes) - 1
    if nodes[0] == nodes[-1]:
        return ders[n](nodes[0]) / mp.factorial(n)
    return (_dd(ders, nodes[1:]) - _dd(ders, nodes[:-1])) / (nodes[-1] - nodes[0])


def _funcs(mu2):
    """h(a) = a(1 - ln a/mu^2), g(a) = a h(a) and derivatives. At a = 0 (Landau gauge, node xi*M^2 = 0) the
    limits a ln a -> 0, a^2 ln a -> 0 are used: h(0) = g(0) = g'(0) = 0. (-ln a and g'' diverge at 0 but are
    only needed for a repeated node at 0, which never occurs for M > 0.)"""
    L = lambda a: mp.log(a / mu2)
    z = lambda f: (lambda a: mp.mpf(0) if a == 0 else f(a))
    h = [z(lambda a: a * (1 - L(a))), lambda a: -L(a)]
    g = [z(lambda a: a * a * (1 - L(a))), z(lambda a: a * (1 - 2 * L(a))), lambda a: -1 - 2 * L(a)]
    return h, g


def _F(m2, M2, xi, mu2):
    """MS-bar finite part of 16 pi^2 v^2 Pi_V / M_V^2 (DERIVATION.md section 2)."""
    h, g = _funcs(mu2)
    A0 = h[0](m2)
    B0 = _dd(h, [M2, m2])
    K = _dd(g, [xi * M2, M2, m2])
    L2 = _dd(g, [m2, xi * M2])
    return -A0 - 4 * M2 * B0 + (1 - xi) * M2 * (K + mp.mpf(1) / 2) + L2 + (m2 + xi * M2) / 2


def _pi(mH, MW, MZ, alpha, xi, mu, which):
    with mp.workdps(_dps(mH, MW, MZ)):
        mW2, mZ2 = mp.mpf(MW) ** 2, mp.mpf(MZ) ** 2
        M2 = mW2 if which == "W" else mZ2
        s2 = 1 - mW2 / mZ2
        return M2 * mp.mpf(alpha) * _F(mp.mpf(mH) ** 2, M2, mp.mpf(xi), mp.mpf(mu) ** 2) / (16 * mp.pi * s2 * mW2)


def self_energy_W(mH, MW, MZ, alpha, xi, mu):
    return float(_pi(mH, MW, MZ, alpha, xi, mu, "W"))


def self_energy_Z(mH, MW, MZ, alpha, xi, mu):
    return float(_pi(mH, MW, MZ, alpha, xi, mu, "Z"))


def _drho(mH, MW, MZ, alpha, xi, mu):
    return _pi(mH, MW, MZ, alpha, xi, mu, "W") / mp.mpf(MW) ** 2 - _pi(mH, MW, MZ, alpha, xi, mu, "Z") / mp.mpf(MZ) ** 2


def rho_higgs_rel(mH, MW, MZ, alpha, xi, mu):
    with mp.workdps(_dps(mH, MW, MZ)):
        return float(_drho(mH, MW, MZ, alpha, xi, mu) - _drho(MW, MW, MZ, alpha, xi, mu))


def log_coefficient(MW, MZ, alpha, xi):
    with mp.workdps(DPS):
        mW2, mZ2 = mp.mpf(MW) ** 2, mp.mpf(MZ) ** 2
        s2 = 1 - mW2 / mZ2
        return float(3 * mp.mpf(alpha) * (mW2 - mZ2) / (16 * mp.pi * s2 * mW2))


def _F_exact_d(m2, M2, xi, mu2, eps):
    """Same F in exact d = 4-2eps with MS-bar normalisation, poles NOT removed."""
    A = lambda a: -mp.gamma(-1 + eps) * mp.exp(mp.euler * eps) * a * (a / mu2) ** (-eps)
    gA = lambda a: a * A(a)
    B0 = (A(M2) - A(m2)) / (M2 - m2)
    a1, a2, a3 = xi * M2, M2, m2
    if a1 == a2:
        a1 = a1 * (1 + mp.mpf(10) ** -30)           # exact-d check only: tiny split of the degenerate node
    K = gA(a1) / ((a1 - a2) * (a1 - a3)) + gA(a2) / ((a2 - a1) * (a2 - a3)) + gA(a3) / ((a3 - a1) * (a3 - a2))
    L2 = (gA(m2) - gA(xi * M2)) / (m2 - xi * M2)
    f4d = 4 / (4 - 2 * eps)
    return -A(m2) - 4 * M2 * B0 + (1 - xi) * M2 * f4d * K + f4d * L2


if __name__ == "__main__":
    MW, MZ, AL = 80.38, 91.19, 1 / 128.0
    mp.mp.dps = 50
    print("rho_higgs_rel(125,300,1000):", [rho_higgs_rel(x, MW, MZ, AL, 1.0, MW) for x in (125., 300., 1000.)])
    print("log_coefficient:", log_coefficient(MW, MZ, AL, 1.0))
    # route 1: exact-d with pole subtraction
    for xi in (1.0, 0.4):
        for M2n in (MW, MZ):
            m2, M2, mu2 = mp.mpf(400) ** 2, mp.mpf(M2n) ** 2, mp.mpf(MW) ** 2
            eps = mp.mpf(10) ** -12
            ex = _F_exact_d(m2, M2, mp.mpf(xi), mu2, eps) + 3 * M2 / eps
            print("exact-d vs closed form F:", mp.nstr(ex, 12), mp.nstr(_F(m2, M2, mp.mpf(xi), mu2), 12))
    # route 2: Feynman-parameter quadrature of the divided differences
    m2, M2, mu2 = mp.mpf(300) ** 2, mp.mpf(MZ) ** 2, mp.mpf(MW) ** 2
    xi = mp.mpf("0.4")
    h, g = _funcs(mu2)
    ln = lambda a: mp.log(a / mu2)
    B0q = mp.quad(lambda x: -ln((1 - x) * M2 + x * m2), [0, 1])
    Kq = mp.quad(lambda x, y: -1 - 2 * ln(x * xi * M2 + y * M2 + (1 - x - y) * m2), [0, 1], [0, 1]) if False else \
        mp.quad(lambda x: mp.quad(lambda y: -1 - 2 * ln(x * xi * M2 + y * M2 + (1 - x - y) * m2), [0, 1 - x]), [0, 1])
    print("B0  closed/quad:", mp.nstr(_dd(h, [M2, m2]), 12), mp.nstr(B0q + 0 * 1, 12), "(quad is B0 - 1 + 1 offset check:", mp.nstr(_dd(h, [M2, m2]) - B0q, 12), ")")
    print("K   closed/quad:", mp.nstr(_dd(g, [xi * M2, M2, m2]), 12), mp.nstr(Kq, 12))
    # large-mH accuracy: ratio of rho_higgs_rel to B ln(mH^2/MW^2) -> 1 (corrections ~ O(1/ln) from the mH-independent constant)
    B = log_coefficient(MW, MZ, AL, 1.0)
    for e in (8, 16, 24, 32):
        d = f_ = rho_higgs_rel(10.0 ** e * MW, MW, MZ, AL, 1.0, MW)
        d2 = rho_higgs_rel(10.0 ** (e + 1) * MW, MW, MZ, AL, 1.0, MW)
        print("1e%d MW: local slope / B =" % e, (d2 - d) / (B * 2 * math.log(10.0)))
    # xi independence, mu independence, slope
    print("xi scan:", [rho_higgs_rel(400., MW, MZ, AL, x, MW) for x in (1.0, 0.4, 3.0, 17.0)])
    print("mu scan:", [rho_higgs_rel(400., MW, MZ, AL, 1.0, u) for u in (MW, 3.7 * MW)])
    f = lambda mh: rho_higgs_rel(mh, MW, MZ, AL, 1.0, MW)
    h1, h2 = 1e5 * MW, 1e6 * MW
    print("slope", (f(h2) - f(h1)) / math.log((h2 / h1) ** 2))
