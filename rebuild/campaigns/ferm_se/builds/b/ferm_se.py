"""Fermionic one-loop gauge boson self-energies, 't Hooft-Feynman gauge, MS-bar (see DERIVATION.md)."""
import math
import mpmath as mp

PROVENANCE = {
    "sigma_AA": ("derived", "fermion bubble, Feynman-parameter integral with closed-form logs, MS-bar"),
    "sigma_AZ": ("derived", "fermion bubble, vector/axial couplings derived from the Lagrangian"),
    "sigma_ZZ": ("derived", "fermion bubble, vector/axial couplings derived from the Lagrangian"),
    "sigma_W": ("derived", "doublet bubble with V-A coupling g/sqrt2, weight w"),
}

_DPS = 120


def _G(n, r):
    """int_0^1 x^n ln|x-r| dx (real part), r real or complex (mp numbers)."""
    poly = sum(r ** (n - j) / (j + 1) for j in range(n + 1))
    if isinstance(r, mp.mpf) or (isinstance(r, mp.mpc) and r.imag == 0):
        r = mp.re(r)
        l1 = mp.log(abs(1 - r)) if r != 1 else mp.mpf(0)
        l0 = mp.log(abs(r)) if r != 0 else mp.mpf(0)
        if r == 1:
            tail = r ** (n + 1) * (0 - l0)
            main = -poly - tail
        else:
            main = l1 - poly - r ** (n + 1) * (l1 - l0)
        return main / (n + 1)
    l = mp.log(1 - r) - mp.log(-r)
    return mp.re((mp.log(1 - r) - poly - r ** (n + 1) * l) / (n + 1))


def _J(n, k2, m1s, m2s, mu2):
    """int_0^1 x^n ln|Delta/mu^2| dx, Delta = x m2s + (1-x) m1s - x(1-x) k2."""
    if k2 == 0:
        if m1s == m2s:
            return mp.log(m1s / mu2) / (n + 1) if m1s != 0 else None
        # Delta = m1s + (m2s-m1s) x, linear
        b = m2s - m1s
        # int x^n ln|m1s + b x| = ln|b|/(n+1) + int x^n ln|x - r|, r = -m1s/b
        return mp.log(abs(b) / mu2) / (n + 1) + _G(n, -m1s / b)
    a = k2
    bq = m2s - m1s - k2
    disc = bq * bq - 4 * a * m1s
    if disc >= 0:
        sq = mp.sqrt(disc)
        q = -(bq + (sq if bq >= 0 else -sq)) / 2          # stable roots
        r1 = q / a
        r2 = (m1s / q) if q != 0 else r1
    else:
        sq = mp.sqrt(-disc)
        r1 = mp.mpc(-bq, sq) / (2 * a)
        r2 = mp.conj(r1)
    return mp.log(abs(a) / mu2) / (n + 1) + _G(n, r1) + _G(n, r2)


def _bubble(k2, m1, m2, A, B, N, mu):
    """(N/16pi^2) int P(x) (-ln|Delta/mu^2|) dx with P = 2A[2x(1-x)k2 - x m2^2 - (1-x) m1^2] + 2B m1 m2."""
    with mp.workdps(_DPS):
        k2 = mp.mpf(k2); m1s = mp.mpf(m1) ** 2; m2s = mp.mpf(m2) ** 2; mu2 = mp.mpf(mu) ** 2
        A = mp.mpf(A); B = mp.mpf(B); N = mp.mpf(N)
        # P = c0 + c1 x + c2 x^2
        c0 = -2 * A * m1s + 2 * B * mp.mpf(m1) * mp.mpf(m2)
        c1 = 2 * A * (2 * k2 - m2s + m1s)
        c2 = -4 * A * k2
        if c0 == 0 and c1 == 0 and c2 == 0:
            return 0.0
        tot = mp.mpf(0)
        for n, c in ((0, c0), (1, c1), (2, c2)):
            if c != 0:
                J = _J(n, k2, m1s, m2s, mu2)
                if J is None:      # k2 = 0, m = 0: Delta = 0, but then the polynomial vanishes
                    continue
                tot += c * J
        return float(-N * tot / (16 * mp.pi ** 2))


def _couplings(alpha, MW, MZ):
    e2 = 4 * math.pi * alpha
    c2 = MW ** 2 / MZ ** 2
    s2 = 1 - c2
    return math.sqrt(e2), math.sqrt(e2 / (s2 * c2)), e2 / s2, s2


def _zc(Q, I3, s2, gz):
    return gz * (I3 - s2 * Q), -gz * s2 * Q


def _neutral(kind, k2, fermions, MW, MZ, alpha, mu):
    e, gz, g2, s2 = _couplings(alpha, MW, MZ)
    tot = 0.0
    for (m, Q, I3, NC) in fermions:
        zl, zr = _zc(Q, I3, s2, gz)
        if m == 0 and Q == 0:
            zr = 0.0
        if kind == "AA":
            A = B = 2 * (e * Q) ** 2
        elif kind == "AZ":
            A = B = e * Q * (zl + zr)
        else:
            A, B = zl * zl + zr * zr, 2 * zl * zr
        tot += _bubble(k2, m, m, A, B, NC, mu)
    return tot


def sigma_AA(k2, fermions, MW, MZ, alpha, mu):
    return _neutral("AA", k2, fermions, MW, MZ, alpha, mu)


def sigma_AZ(k2, fermions, MW, MZ, alpha, mu):
    return _neutral("AZ", k2, fermions, MW, MZ, alpha, mu)


def sigma_ZZ(k2, fermions, MW, MZ, alpha, mu):
    return _neutral("ZZ", k2, fermions, MW, MZ, alpha, mu)


def sigma_W(k2, doublets, MW, MZ, alpha, mu):
    _, _, g2, _ = _couplings(alpha, MW, MZ)
    return sum(_bubble(k2, mu_, md, g2 / 2, 0.0, w, mu) for (mu_, md, w) in doublets)


if __name__ == "__main__":
    MW, MZ, al = 80.38, 91.19, 1 / 128.0
    top = ((172.5, 2 / 3, 0.5, 3), (4.7, -1 / 3, -0.5, 3))
    mu = MW
    e2 = 4 * math.pi * al

    def quad(k2, m1, m2, A, B, N):
        with mp.workdps(30):
            k2m, m1s, m2s = mp.mpf(k2), mp.mpf(m1) ** 2, mp.mpf(m2) ** 2
            D = lambda x: x * m2s + (1 - x) * m1s - x * (1 - x) * k2m
            P = lambda x: 2 * A * (2 * x * (1 - x) * k2m - x * m2s - (1 - x) * m1s) + 2 * B * m1 * m2
            f = lambda x: -P(x) * mp.log(abs(D(x)) / mp.mpf(mu) ** 2)
            pts = [0, 1]
            d = (m2s - m1s - k2m) ** 2 - 4 * k2m * m1s if k2m != 0 else -1
            if k2m != 0 and d > 0:
                for r in ((-(m2s - m1s - k2m) + s * mp.sqrt(d)) / (2 * k2m) for s in (1, -1)):
                    if 0 < r < 1:
                        pts.append(r)
            return float(N * mp.quad(f, sorted(pts)) / (16 * mp.pi ** 2))

    for k2 in (-5000.0, 0.3 * MW ** 2, MZ ** 2, 4 * 172.5 ** 2 * 1.2):
        m, Q = 172.5, 2 / 3
        main = sigma_AA(k2, top[:1], MW, MZ, al, mu)
        r1 = quad(k2, m, m, 2 * e2 * Q * Q, 2 * e2 * Q * Q, 3)
        # Denner-form equal-mass: -(a/4pi)(4/3)N Q^2[-(k2+2m^2)B0(k2) + 2m^2 B0(0) + k2/3], B0 = -int ln|D|/mu^2 (finite part)
        with mp.workdps(30):
            B0 = lambda s: -mp.quad(lambda x: mp.log(abs(m * m - x * (1 - x) * s) / mu ** 2), [0, 0.5, 1])
            den = -(al / (4 * math.pi)) * (4 / 3) * 3 * Q * Q * (-(k2 + 2 * m * m) * B0(k2) + 2 * m * m * B0(0) + k2 / 3)
        print(f"k2={k2:10.1f} AA(top) closed={main:.10e} quad={r1:.10e} Denner-form={float(den):.10e}")
    # heavy fermion limit (decoupling) and mu derivative
    k2 = 1.0
    print("heavy limit", sigma_AA(k2, top[:1], MW, MZ, al, mu), (al / (3 * math.pi)) * 3 * (2 / 3) ** 2 * k2 * math.log(mu ** 2 / 172.5 ** 2))
    d = sigma_AA(2000.0, top, MW, MZ, al, 2 * mu) - sigma_AA(2000.0, top, MW, MZ, al, mu)
    print("mu dep AA", d, (al / (4 * math.pi)) * (4 / 3) * 2000.0 * (3 * (4 / 9 + 1 / 9)) * math.log(4))
    print("W", sigma_W(-3000.0, ((172.5, 4.7, 2.7),), MW, MZ, al, mu), quad(-3000.0, 172.5, 4.7, (4 * math.pi * al / (1 - MW**2/MZ**2)) / 2, 0, 2.7))
