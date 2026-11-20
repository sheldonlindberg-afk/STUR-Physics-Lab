"""Fermion-loop one-loop transverse self-energies of gamma, Z, W (SPEC.md); derivation in DERIVATION.md.

Route 1 (exports): Passarino-Veltman reduction, eq. (*) of DERIVATION.md, with MS-bar A0, B0, B1, B00 and
closed-form log moments. Route 2 (__main__): direct numerical Feynman-parameter integral (DERIVATION section 6).
"""
import mpmath as mp

DPS = 50


# ---------------------------------------------------------------- couplings (DERIVATION section 1)
def _sw_cw(MW, MZ):
    c = mp.mpf(MW) / mp.mpf(MZ)
    s2 = 1 - c * c
    return mp.sqrt(s2), c


def _z_couplings(Q, I3, s, c):
    Q, I3 = mp.mpf(Q), mp.mpf(I3)
    return (I3 - s * s * Q) / (s * c), -s * Q / c


# ---------------------------------------------------------------- log moments I_n = Int_0^1 x^n ln|Delta(x)/mu^2|
def _F(n, x, a):
    """Antiderivative of x^n ln(x - a); real a uses ln|x - a| with 0 ln 0 = 0."""
    d = x - a
    if isinstance(a, mp.mpc):
        L = mp.log(d)
    else:
        L = mp.log(abs(d)) if d != 0 else mp.mpf(0)
    if n == 0:
        return d * L - x if d != 0 else -x
    return ((x * x - a * a) / 2) * L - x * x / 4 - a * x / 2 if d != 0 else -x * x / 4 - a * x / 2


def _seg(n, a):
    v = _F(n, mp.mpf(1), a) - _F(n, mp.mpf(0), a)
    return mp.re(v)


def _moments(k2, m1, m2, mu):
    """(I0, I1) with Delta(x) = k2 x^2 + (m2^2 - m1^2 - k2) x + m1^2, or None if Delta == 0 identically."""
    A, B, C = k2, m2 * m2 - m1 * m1 - k2, m1 * m1
    lmu = mp.log(mu * mu)
    if A != 0:
        disc = B * B - 4 * A * C
        base = mp.log(abs(A)) - lmu
        if disc >= 0:
            r = mp.sqrt(disc)
            x1, x2 = (-B + r) / (2 * A), (-B - r) / (2 * A)
            return base + _seg(0, x1) + _seg(0, x2), base / 2 + _seg(1, x1) + _seg(1, x2)
        a = mp.mpc(-B / (2 * A), mp.sqrt(-disc) / (2 * abs(A)))
        return base + 2 * _seg(0, a), base / 2 + 2 * _seg(1, a)
    if B != 0:                                   # k2 = 0, m1 != m2: Delta = B (x - a)
        a = -C / B
        base = mp.log(abs(B)) - lmu
        return base + _seg(0, a), base / 2 + _seg(1, a)
    if C != 0:                                   # k2 = 0, m1 = m2 != 0
        L = mp.log(C) - lmu
        return L, L / 2
    return None                                  # scaleless: every use is multiplied by zero


def _A0(m, mu):
    return mp.mpf(0) if m == 0 else m * m * (1 - mp.log(m * m / (mu * mu)))


def _bubble(k2, m1, m2, Gp, Gm, mu):
    """Eq. (*) without the prefactor N_C alpha/(4 pi): G+[4B00 - A0 - A0 - (m1^2+m2^2-k^2)B0] + 2G- m1 m2 B0."""
    mom = _moments(k2, m1, m2, mu)
    if mom is None:
        return mp.mpf(0)
    B0, B1 = -mom[0], mom[1]
    A01, A02 = _A0(m1, mu), _A0(m2, mu)
    B00 = (A02 + 2 * m1 * m1 * B0 + (k2 + m1 * m1 - m2 * m2) * B1 + m1 * m1 + m2 * m2 - k2 / 3) / 6
    return Gp * (4 * B00 - A01 - A02 - (m1 * m1 + m2 * m2 - k2) * B0) + 2 * Gm * m1 * m2 * B0


def _neutral(which, k2, fermions, MW, MZ, alpha, mu):
    with mp.workdps(DPS):
        k2, mu, alpha = mp.mpf(k2), mp.mpf(mu), mp.mpf(alpha)
        s, c = _sw_cw(MW, MZ)
        tot = mp.mpf(0)
        for (m, Q, I3, NC) in fermions:
            m = mp.mpf(m)
            gA = mp.mpf(Q)
            zL, zR = _z_couplings(Q, I3, s, c)
            aL, aR, bL, bR = {"AA": (gA, gA, gA, gA), "AZ": (gA, gA, zL, zR), "ZZ": (zL, zR, zL, zR)}[which]
            Gp, Gm = aL * bL + aR * bR, aL * bR + aR * bL
            tot += NC * _bubble(k2, m, m, Gp, Gm, mu)
        return float(alpha / (4 * mp.pi) * tot)


def sigma_AA(k2, fermions, MW, MZ, alpha, mu):
    return _neutral("AA", k2, fermions, MW, MZ, alpha, mu)


def sigma_AZ(k2, fermions, MW, MZ, alpha, mu):
    return _neutral("AZ", k2, fermions, MW, MZ, alpha, mu)


def sigma_ZZ(k2, fermions, MW, MZ, alpha, mu):
    return _neutral("ZZ", k2, fermions, MW, MZ, alpha, mu)


def sigma_W(k2, doublets, MW, MZ, alpha, mu):
    with mp.workdps(DPS):
        k2, mu, alpha = mp.mpf(k2), mp.mpf(mu), mp.mpf(alpha)
        s, c = _sw_cw(MW, MZ)
        gL = 1 / (mp.sqrt(2) * s)
        tot = mp.mpf(0)
        for (mu_, md, w) in doublets:
            tot += mp.mpf(w) * _bubble(k2, mp.mpf(mu_), mp.mpf(md), gL * gL, mp.mpf(0), mu)
        return float(alpha / (4 * mp.pi) * tot)


PROVENANCE = {
    "sigma_AA": ("derived", "fermion bubble, PV reduction in d dims (B00 O(eps) term), MS-bar; G+=G-=2Q^2; DERIVATION sec. 3"),
    "sigma_AZ": ("derived", "couplings from SPEC rotation: photon Q, Z gL=(I3-s^2Q)/(sc), gR=-sQ/c; G+=G-=Q(gL+gR)"),
    "sigma_ZZ": ("derived", "G+=gL^2+gR^2, G-=2gLgR (mass insertion), same bubble formula (*)"),
    "sigma_W": ("derived", "W vertex e/(sqrt2 s) P_L, weight w=NC|V|^2, unequal-mass bubble (*), G-=0"),
}


# ---------------------------------------------------------------- route 2: direct Feynman-parameter quadrature
def _route2(k2, m1, m2, Gp, Gm, NC, alpha, mu):
    with mp.workdps(30):
        k2, m1, m2, mu = mp.mpf(k2), mp.mpf(m1), mp.mpf(m2), mp.mpf(mu)
        D = lambda x: (1 - x) * m1 ** 2 + x * m2 ** 2 - x * (1 - x) * k2
        f = lambda x: (-mp.log(abs(D(x)) / mu ** 2) * (Gp * (2 * x * (1 - x) * k2 - (1 - x) * m1 ** 2 - x * m2 ** 2) + Gm * m1 * m2)
                       if D(x) != 0 else mp.mpf(0))
        pts = [mp.mpf(0)]
        if k2 != 0:
            A, B, C = k2, m2 ** 2 - m1 ** 2 - k2, m1 ** 2
            disc = B * B - 4 * A * C
            if disc > 0:
                for r in sorted([(-B + mp.sqrt(disc)) / (2 * A), (-B - mp.sqrt(disc)) / (2 * A)]):
                    if 0 < r < 1:
                        pts.append(r)
        pts.append(mp.mpf(1))
        return float(NC * mp.mpf(alpha) / (2 * mp.pi) * mp.quad(f, pts))


if __name__ == "__main__":
    MW, MZ, AL = 80.38, 91.19, 1 / 128.0
    with mp.workdps(30):
        s, c = _sw_cw(MW, MZ)
    fe = [(0.000511, -1, -0.5, 1), (0.0, 0, 0.5, 1), (172.5, 2 / 3, 0.5, 3), (4.7, -1 / 3, -0.5, 3)]
    mu = 1.7 * MW
    print("route 1 (PV, closed form) vs route 2 (Feynman-parameter quadrature)")
    worst = 0.0
    for k2 in (-3e4, -10.0, 0.0, 0.3 * MW ** 2, MZ ** 2, 4 * 172.5 ** 2 * 1.2):
        for f in fe:
            m, Q, I3, NC = f
            zL, zR = (float(v) for v in _z_couplings(Q, I3, s, c))
            for name, (aL, aR, bL, bR) in (("AA", (Q, Q, Q, Q)), ("AZ", (Q, Q, zL, zR)), ("ZZ", (zL, zR, zL, zR))):
                r1 = globals()["sigma_" + name](k2, (f,), MW, MZ, AL, mu)
                r2 = _route2(k2, m, m, aL * bL + aR * bR, aL * bR + aR * bL, NC, AL, mu)
                worst = max(worst, abs(r1 - r2) / max(abs(r2), 1e-12))
        for d in ((172.5, 4.7, 3.0), (0.0, 0.000511, 1.0), (1.5, 0.15, 0.15)):
            r1 = sigma_W(k2, (d,), MW, MZ, AL, mu)
            r2 = _route2(k2, d[0], d[1], 1 / (2 * float(s) ** 2), 0.0, d[2], AL, mu)
            r3 = sigma_W(k2, ((d[1], d[0], d[2]),), MW, MZ, AL, mu)
            worst = max(worst, abs(r1 - r2) / max(abs(r2), 1e-12), abs(r1 - r3) / max(abs(r1), 1e-12))
        print(f"  k2={k2:>12.4g}: AA={sigma_AA(k2, tuple(fe), MW, MZ, AL, mu):+.8e}  AZ={sigma_AZ(k2, tuple(fe), MW, MZ, AL, mu):+.8e}"
              f"  ZZ={sigma_ZZ(k2, tuple(fe), MW, MZ, AL, mu):+.8e}  W={sigma_W(k2, ((0, 0.000511, 1), (172.5, 4.7, 3)), MW, MZ, AL, mu):+.8e}")
    print(f"  worst relative route1-route2 (and W up<->down) difference: {worst:.2e}")
    print("Ward:", sigma_AA(0.0, tuple(fe), MW, MZ, AL, mu), sigma_AZ(0.0, tuple(fe), MW, MZ, AL, mu))
    # mu dependence vs UV pole coefficient: dSigma/dln mu^2 = NC alpha/(4pi)[G+(2k^2/3 - m1^2 - m2^2) + 2G- m1 m2]
    k2, f = 0.4 * MW ** 2, fe[2]
    m, Q, I3, NC = f
    zL, zR = (float(v) for v in _z_couplings(Q, I3, s, c))
    h = 1e-4
    num = (sigma_ZZ(k2, (f,), MW, MZ, AL, mu * mp.e ** (h / 4)) - sigma_ZZ(k2, (f,), MW, MZ, AL, mu * mp.e ** (-h / 4))) / h
    ana = NC * AL / (4 * float(mp.pi)) * ((zL ** 2 + zR ** 2) * (2 * k2 / 3 - 2 * m * m) + 4 * zL * zR * m * m)
    print(f"ZZ top dSigma/dln mu^2: numeric {num:.10e}  pole coefficient {ana:.10e}")
    d = (172.5, 4.7, 3.0)
    num = (sigma_W(k2, (d,), MW, MZ, AL, mu * mp.e ** (h / 4)) - sigma_W(k2, (d,), MW, MZ, AL, mu * mp.e ** (-h / 4))) / h
    ana = 3 * AL / (4 * float(mp.pi)) / (2 * float(s) ** 2) * (2 * k2 / 3 - d[0] ** 2 - d[1] ** 2)
    print(f"W tb dSigma/dln mu^2:  numeric {num:.10e}  pole coefficient {ana:.10e}")
    # heavy fermion limit
    M, k2 = 1e4, 100.0
    lead = AL / (3 * float(mp.pi)) * 3 * (2 / 3) ** 2 * k2 * (-float(mp.log(M ** 2 / mu ** 2)))
    print(f"heavy fermion AA: {sigma_AA(k2, ((M, 2 / 3, 0.5, 3),), MW, MZ, AL, mu):.10e} vs (alpha/3pi)NcQ^2 k^2(-ln m^2/mu^2) {lead:.10e}")
    k2 = -500.0
    ml = AL / (3 * float(mp.pi)) * k2 * (5 / 3 - float(mp.log(-k2 / mu ** 2)))
    print(f"massless AA: {sigma_AA(k2, ((0.0, -1, -0.5, 1),), MW, MZ, AL, mu):.12e} vs {ml:.12e}")
