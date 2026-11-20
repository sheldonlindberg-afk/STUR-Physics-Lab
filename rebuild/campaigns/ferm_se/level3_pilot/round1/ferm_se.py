"""Fermionic one-loop transverse self-energies of gamma, Z, W ('t Hooft-Feynman gauge, NDR, MS-bar). See DERIVATION.md.

Sigma_T = -(1/4 pi^2) Int_0^1 dx P(x) ln(|Delta(x)|/mu^2),
  Delta = (1-x) m1^2 + x m2^2 - x(1-x) k^2,
  P = A [2x(1-x)k^2 - (1-x) m1^2 - x m2^2] + B m1 m2,  A = v v' + a a', B = v v' - a a'.
"""
import math
import cmath

PROVENANCE = {
    "sigma_AA": ("derived", "fermion bubble, couplings eQ; Feynman-parameter integral of DERIVATION.md section 2, MS-bar"),
    "sigma_AZ": ("derived", "fermion bubble, photon eQ times Z vector coupling; DERIVATION.md section 2"),
    "sigma_ZZ": ("derived", "fermion bubble, vector+axial Z couplings with mass term; DERIVATION.md section 2"),
    "sigma_W": ("derived", "fermion bubble, pure left coupling g/sqrt2, unequal masses; DERIVATION.md section 2"),
}

# ---------------------------------------------------------------- tanh-sinh nodes (x = A + (B-A) fA, distances from both ends)
_H = 1.0 / 16.0
_NODES = []
for _i in range(-int(6.0 / _H), int(6.0 / _H) + 1):
    _t = _i * _H
    _s = math.pi * math.sinh(_t)
    _fa = 1.0 / (1.0 + math.exp(_s))
    _fb = 1.0 / (1.0 + math.exp(-_s))
    _w = _H * math.pi * math.cosh(_t) * _fa * _fb
    if _fa > 1e-290 and _fb > 1e-290 and _w > 0.0:
        _NODES.append((_t >= 0.0, _fa, _fb, _w))


def _int_direct(k2, m1sq, m2sq, A, B, m1m2):
    """Int_0^1 P(x) ln(Delta) dx for Delta > 0 on [0,1] (no real roots inside); anchored at the nearer end."""
    tot = 0.0
    for left, fa, fb, w in _NODES:
        if left:
            x, u = fa, 1.0 - fa
            dist = fa
        else:
            x, u = 1.0 - fb, fb
            dist = fb
        # Delta = u m1^2 + x m2^2 - x u k^2 with accurate x, u (x*u computed from the small distance)
        xu = dist * (1.0 - dist)
        D = u * m1sq + x * m2sq - xu * k2
        if D <= 0.0:
            continue
        P = A * (2.0 * xu * k2 - u * m1sq - x * m2sq) + B * m1m2
        tot += w * P * math.log(D)
    return tot


def _int_roots(k2, m1sq, m2sq, A, B, m1m2):
    """Same for k2 > (m1+m2)^2: Delta = k2 (x-r_s)(x-r_b); Re ln = ln|k2| + ln|x-r_s| + ln|x-r_b|."""
    b = -(k2 + m1sq - m2sq)
    lam = (k2 - (math.sqrt(m1sq) + math.sqrt(m2sq)) ** 2) * (k2 - (math.sqrt(m1sq) - math.sqrt(m2sq)) ** 2)
    q = 0.5 * (-b + math.sqrt(max(lam, 0.0)))
    rb = min(q / k2, 1.0)
    rs = m1sq / q if q > 0 else 0.0
    rs = min(rs, rb)
    lk = math.log(k2)
    tot = 0.0
    for lo, hi in ((0.0, rs), (rs, rb), (rb, 1.0)):
        L = hi - lo
        if L <= 0.0:
            continue
        for left, fa, fb, w in _NODES:
            if left:
                d = L * fa
                x = lo + d
                u = (1.0 - lo) - d
                d1 = (lo - rs) + d
                d2 = (lo - rb) + d
            else:
                d = L * fb
                x = hi - d
                u = (1.0 - hi) + d
                d1 = (hi - rs) - d
                d2 = (hi - rb) - d
            if d1 == 0.0 or d2 == 0.0 or d <= 0.0:
                continue
            P = A * (2.0 * x * u * k2 - u * m1sq - x * m2sq) + B * m1m2
            tot += w * L * P * (lk + math.log(abs(d1)) + math.log(abs(d2)))
    return tot


def _S(k2, m1, m2, A, B, mu, ref):
    """Sigma_T contribution of one loop, with couplings entering via A, B (already containing all constants)."""
    m1sq, m2sq = m1 * m1, m2 * m2
    m1m2 = m1 * m2
    if k2 == 0.0 and m1sq == 0.0 and m2sq == 0.0:
        return 0.0
    pint = A * (k2 / 3.0 - 0.5 * (m1sq + m2sq)) + B * m1m2              # Int_0^1 P dx (exact)
    scale = ref * ref
    if k2 > 0.0 and k2 > (m1 + m2) ** 2:
        I = _int_roots(k2 / scale, m1sq / scale, m2sq / scale, A, B, m1m2 / scale) * scale
    else:
        I = _int_direct(k2 / scale, m1sq / scale, m2sq / scale, A, B, m1m2 / scale) * scale
    return -(I - math.log(mu * mu / scale) * pint) / (4.0 * math.pi ** 2)


def _couplings(MW, MZ, alpha):
    c2 = (MW / MZ) ** 2
    s2 = 1.0 - c2
    e = math.sqrt(4.0 * math.pi * alpha)
    return e, math.sqrt(s2), math.sqrt(c2), s2


def _vz_az(f, e, s, c, s2):
    m, Q, I3, NC = f
    vA, aA = e * Q, 0.0
    vZ = e * (I3 - 2.0 * s2 * Q) / (2.0 * s * c)
    aZ = e * I3 / (2.0 * s * c)
    return vA, aA, vZ, aZ


def _ferm_sum(kind, k2, fermions, MW, MZ, alpha, mu):
    e, s, c, s2 = _couplings(MW, MZ, alpha)
    ref = MW
    tot = 0.0
    for f in fermions:
        m, Q, I3, NC = f
        vA, aA, vZ, aZ = _vz_az(f, e, s, c, s2)
        if kind == "AA":
            v1, a1, v2, a2 = vA, aA, vA, aA
        elif kind == "AZ":
            v1, a1, v2, a2 = vA, aA, vZ, aZ
        else:
            v1, a1, v2, a2 = vZ, aZ, vZ, aZ
        A = v1 * v2 + a1 * a2
        B = v1 * v2 - a1 * a2
        tot += NC * _S(float(k2), float(m), float(m), A, B, mu, ref)
    return float(tot)


def sigma_AA(k2, fermions, MW, MZ, alpha, mu):
    return _ferm_sum("AA", k2, fermions, MW, MZ, alpha, mu)


def sigma_AZ(k2, fermions, MW, MZ, alpha, mu):
    return _ferm_sum("AZ", k2, fermions, MW, MZ, alpha, mu)


def sigma_ZZ(k2, fermions, MW, MZ, alpha, mu):
    return _ferm_sum("ZZ", k2, fermions, MW, MZ, alpha, mu)


def sigma_W(k2, doublets, MW, MZ, alpha, mu):
    e, s, c, s2 = _couplings(MW, MZ, alpha)
    g2 = e * e / s2
    A, B = g2 / 4.0, 0.0
    tot = 0.0
    for (mu_, md, w) in doublets:
        tot += w * _S(float(k2), float(mu_), float(md), A, B, mu, MW)
    return float(tot)


# ------------------------------------------------------------------------------------------ second routes
def _analytic(k2, m1, m2, A, B, mu):
    """Independent closed form (complex roots), valid for generic nonzero masses, moderate k2."""
    a, b, c = k2, -(k2 + m1 * m1 - m2 * m2), m1 * m1
    disc = complex(b * b - 4 * a * c) ** 0.5
    roots = [(-b + disc) / (2 * a), (-b - disc) / (2 * a)]

    def Fn(n, r):                      # Int_0^1 x^n ln(x-r) dx
        t = ((1 - r ** (n + 1)) / (n + 1)) * cmath.log(1 - r)
        t -= ((0 - r ** (n + 1)) / (n + 1)) * cmath.log(-r) if r != 0 else 0
        return t - sum(r ** (n - j) / (j + 1) for j in range(n + 1)) / (n + 1)

    # P(x) = p0 + p1 x + p2 x^2
    p0 = A * (-m1 * m1) + B * m1 * m2
    p1 = A * (2 * k2 - m2 * m2 + m1 * m1)
    p2 = -2 * A * k2
    tot = 0.0
    for n, p in ((0, p0), (1, p1), (2, p2)):
        tot += p * (math.log(abs(a)) / (n + 1) + sum(Fn(n, r) for r in roots).real)
    pint = A * (k2 / 3.0 - 0.5 * (m1 * m1 + m2 * m2)) + B * m1 * m2
    return -(tot - math.log(mu * mu) * pint) / (4 * math.pi ** 2)


if __name__ == "__main__":
    MW, MZ, al, mu = 80.38, 91.19, 1 / 128.0, 80.38
    e, s, c, s2 = _couplings(MW, MZ, al)
    print("route 1 (tanh-sinh) vs route 2 (analytic complex-log closed form):")
    for (k2, m1, m2, A, B) in ((-3000.0, 172.5, 172.5, 0.7, 0.3), (5000.0, 172.5, 4.7, 0.5, 0.0), (0.3 * MW ** 2, 4.7, 4.7, 0.2, 0.1),
                               (3.0e5, 172.5, 4.7, 0.5, 0.0), (9000.0, 1.5, 0.15, 0.5, 0.0)):
        r1 = _S(k2, m1, m2, A, B, mu, MW)
        r2 = _analytic(k2, m1, m2, A, B, mu)
        print(f"  k2={k2:10.1f} m=({m1},{m2}): {r1:.15e} {r2:.15e} rel diff {abs(r1 / r2 - 1):.1e}")
    # route (ii): dispersion relation for QED-like loop, k2<0
    m, A, B = 172.5, 1.0, 1.0
    k2 = -5000.0
    S0 = _S(0.0, m, m, A, B, mu, MW)
    h = 1e-3
    d1 = (_S(h, m, m, A, B, mu, MW) - _S(-h, m, m, A, B, mu, MW)) / (2 * h)
    # Im Sigma(s) = (1/4pi) Int_{Delta<0} |P| ... computed via roots: Im ln(-|D|-i0) = -pi -> Im Sigma = +(1/4pi) Int_{D<0} P dx
    def imS(sv):
        r = math.sqrt(1 - 4 * m * m / sv)
        xm, xp = 0.5 * (1 - r), 0.5 * (1 + r)
        F = lambda x: A * (2 * sv * (x * x / 2 - x ** 3 / 3) - m * m * x) + B * m * m * x
        return (F(xp) - F(xm)) / (4 * math.pi)
    th = 4 * m * m
    # s = th/(1-y^2)?  use s = th / (1 - z), z in (0,1): ds = th/(1-z)^2 dz, Gauss-free tanh-sinh via midpoint on z=1-w^2
    tot, N = 0.0, 200000
    for i in range(N):
        wv = (i + 0.5) / N
        z = 1 - wv * wv                      # s = th/wv^2 ; ds = -2 th / wv^3 dwv
        sv = th / (wv * wv)
        tot += imS(sv) / (sv * sv * (sv - k2)) * 2 * th / wv ** 3 / N
    disp = S0 + k2 * d1 + k2 * k2 / math.pi * tot
    print(f"dispersion (ii) at k2={k2}: {disp:.12e}  direct {_S(k2, m, m, A, B, mu, MW):.12e}  rel {abs(disp / _S(k2, m, m, A, B, mu, MW) - 1):.1e}")
    # checks
    fs = ((172.5, 2 / 3, 0.5, 3), (4.7, -1 / 3, -0.5, 3))
    print("Ward: AA(0), AZ(0) =", sigma_AA(0.0, fs, MW, MZ, al, mu), sigma_AZ(0.0, fs, MW, MZ, al, mu))
    for kk in (-10.0, 10.0):
        m_ = 172.5
        ex = -(al / (3 * math.pi)) * 3 * (2 / 3) ** 2 * kk * (math.log(m_ ** 2 / mu ** 2) - kk / (5 * m_ ** 2))
        got = sigma_AA(kk, ((172.5, 2 / 3, 0.5, 3),), MW, MZ, al, mu)
        print(f"heavy fermion AA k2={kk}: {got:.10e} vs decoupling {ex:.10e}")
    d = lambda k2: sigma_ZZ(k2, fs, MW, MZ, al, 2 * mu) - sigma_ZZ(k2, fs, MW, MZ, al, mu)
    print("mu-derivative is linear in k2: second diff", d(-1000.0) - 2 * d(0.0) + d(1000.0), "vs scale", d(1000.0))
    print("sigma_W(top doublet, k2=MW^2) =", sigma_W(MW ** 2, ((172.5, 4.7, 3.0),), MW, MZ, al, mu))
