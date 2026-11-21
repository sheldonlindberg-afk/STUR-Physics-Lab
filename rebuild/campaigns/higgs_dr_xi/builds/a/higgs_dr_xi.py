"""Higgs-containing one-loop W and Z self-energies in the R_xi gauge and the Higgs part of Delta r (see DERIVATION.md).

All arithmetic is done with mpmath at a precision set locally (mp.workdps) inside each export; the global mp.dps is never changed.
"""
import math
import mpmath as mp

PROVENANCE = {
    "sigma_W": ("derived", "H-W (R_xi propagator split by partial fractions), H-phi+- and HH-seagull loops; MS-bar A0, B0, B00 closed forms (DERIVATION 3-4)"),
    "sigma_Z": ("derived", "same as sigma_W with g -> g/c, M_W -> M_Z (DERIVATION 4)"),
    "delta_r_higgs_rel": ("derived", "Delta r_H = [Pi_W(MW^2)-Pi_W(0)]/MW^2 + c^2/s^2 [Pi_Z(MZ^2)/MZ^2 - Pi_W(MW^2)/MW^2], minus its value at mH = MW (DERIVATION 6)"),
    "log_coefficient": ("derived", "ln mH^2 coefficient of the large-mH expansion of A0, B0, B00 combined as in Delta r_H (DERIVATION 8)"),
}


# ----------------------------------------------------------------------------------------------------------------------------
# Feynman-parameter integrals  J_n = int_0^1 x^n ln|D(x)| dx,  D = a x^2 + b x + c  (D > 0 on [0,1] below threshold)

def _ulogu(u, k):
    """u^k ln u with the limit 0 at u = 0 (k >= 1)."""
    if u == 0:
        return mp.mpf(0)
    return u**k * mp.log(u)


def _G(u, r):
    """Antiderivatives in u = x - r of ln u, x ln u, x^2 ln u (x = u + r)."""
    g0 = _ulogu(u, 1) - u
    h2 = _ulogu(u, 2) / 2 - u**2 / 4
    g1 = h2 + r * g0
    g2 = _ulogu(u, 3) / 3 - u**3 / 9 + 2 * r * h2 + r**2 * g0
    return g0, g1, g2


def _J_root(r):
    """(int_0^1 x^n ln|x - r| dx for n = 0,1,2), r real or complex, never inside [0,1]."""
    u1, u0 = 1 - r, -r
    A, B = _G(u1, r), _G(u0, r)
    return [mp.re(A[i] - B[i]) for i in range(3)]


def _J(a, b, c):
    """J_0, J_1, J_2 for D = a x^2 + b x + c."""
    if a != 0:
        big = max(abs(b / a), abs(c / a), 1)
        extra = int(3 * float(mp.log10(1 + big))) + 10
        with mp.extradps(extra):
            disc = mp.mpc(b * b - 4 * a * c)
            sq = mp.sqrt(disc)
            s = b + sq if abs(b + sq) >= abs(b - sq) else b - sq
            q = -s / 2
            if q == 0:                                           # b = c = 0: double root at 0 (massless line, equal-scale point)
                r1 = r2 = mp.mpc(0)
            else:
                r1, r2 = q / a, c / q
            la = mp.log(abs(a))
            j1, j2 = _J_root(r1), _J_root(r2)
            out = [la / (n + 1) + j1[n] + j2[n] for n in range(3)]
        return [+v for v in out]
    if b != 0:
        big = max(abs(c / b), 1)
        extra = int(3 * float(mp.log10(1 + big))) + 10
        with mp.extradps(extra):
            r = -c / b
            lb = mp.log(abs(b))
            j = _J_root(mp.mpf(r))
            out = [lb / (n + 1) + j[n] for n in range(3)]
        return [+v for v in out]
    lc = mp.log(c)
    return [lc / (n + 1) for n in range(3)]


def _coeffs(p2, m0, m1):
    return p2, m1**2 - m0**2 - p2, m0**2


def B0(p2, m0, m1, mu):
    """MS-bar B0 = -int_0^1 ln(D/mu^2)."""
    a, b, c = _coeffs(p2, m0, m1)
    J = _J(a, b, c)
    return mp.log(mu**2) - J[0]


def B00(p2, m0, m1, mu):
    """MS-bar B00 = (1/2) int_0^1 D [1 - ln(D/mu^2)]  (the +1 is the O(eps) part of 1/d times the pole)."""
    a, b, c = _coeffs(p2, m0, m1)
    J = _J(a, b, c)
    SD = a / 3 + b / 2 + c
    SDlnD = a * J[2] + b * J[1] + c * J[0]
    return (SD * (1 + mp.log(mu**2)) - SDlnD) / 2


def A0(m, mu):
    return m**2 * (1 - mp.log(m**2 / mu**2))


# ----------------------------------------------------------------------------------------------------------------------------
# diagrams (g^{mu nu} parts), in units of g_V^2/(16 pi^2), g_W = g, g_Z = g/c

def _diagrams(q2, mH, MV, xi, mu):
    """Return the four g^{mu nu} pieces (a1, a2, b, c) of DERIVATION step 4, each without the factor g_V^2/(16 pi^2)."""
    mG = mp.sqrt(xi) * MV                                    # Goldstone mass (xi = 0: massless, Landau gauge)
    a1 = -(MV**2 * B0(q2, MV, mH, mu) - B00(q2, MV, mH, mu))  # H-V loop, (g - kk/M^2)/(k^2 - M^2) part of the propagator
    bxi = B00(q2, mG, mH, mu)
    a2 = -bxi                                                # H-V loop, -i kk/(M^2 (k^2 - xi M^2)) part
    b = +bxi                                                 # H-Goldstone loop
    c = -A0(mH, mu) / 4                                      # HHVV seagull
    return a1, a2, b, c


def _pi(q2, mH, MV, xi, mu, coupling):
    return coupling / (16 * mp.pi**2) * mp.fsum(_diagrams(q2, mH, MV, xi, mu))


def _dps(mH, MW, MZ, q2=0.0):
    r = max(mH**2 / MW**2, MW**2 / mH**2, 1.0)
    return 40 + int(2 * math.log10(r)) + int(math.log10(1 + abs(q2) / MW**2))


def _couplings(MW, MZ, alpha):
    c2 = MW**2 / MZ**2
    s2 = 1 - c2
    g2 = 4 * mp.pi * alpha / s2
    return c2, s2, g2


def _sigma_W_mp(q2, mH, MW, MZ, alpha, xi, mu):
    c2, s2, g2 = _couplings(MW, MZ, alpha)
    return _pi(q2, mH, MW, xi, mu, g2)


def _sigma_Z_mp(q2, mH, MW, MZ, alpha, xi, mu):
    c2, s2, g2 = _couplings(MW, MZ, alpha)
    return _pi(q2, mH, MZ, xi, mu, g2 / c2)


def _cast(*xs):
    return [mp.mpf(x) for x in xs]


def sigma_W(q2, mH, MW, MZ, alpha, xi, mu):
    with mp.workdps(_dps(mH, MW, MZ, q2)):
        return float(_sigma_W_mp(*_cast(q2, mH, MW, MZ, alpha, xi, mu)))


def sigma_Z(q2, mH, MW, MZ, alpha, xi, mu):
    with mp.workdps(_dps(mH, MW, MZ, q2)):
        return float(_sigma_Z_mp(*_cast(q2, mH, MW, MZ, alpha, xi, mu)))


def _delta_r_mp(mH, MW, MZ, alpha, xi, mu):
    c2, s2, g2 = _couplings(MW, MZ, alpha)
    PW_M = _sigma_W_mp(MW**2, mH, MW, MZ, alpha, xi, mu)
    PW_0 = _sigma_W_mp(mp.mpf(0), mH, MW, MZ, alpha, xi, mu)
    PZ_M = _sigma_Z_mp(MZ**2, mH, MW, MZ, alpha, xi, mu)
    return (PW_M - PW_0) / MW**2 + c2 / s2 * (PZ_M / MZ**2 - PW_M / MW**2)


def delta_r_higgs_rel(mH, MW, MZ, alpha, xi, mu):
    with mp.workdps(_dps(mH, MW, MZ, MZ**2)):
        mH_, MW_, MZ_, al, xi_, mu_ = _cast(mH, MW, MZ, alpha, xi, mu)
        return float(_delta_r_mp(mH_, MW_, MZ_, al, xi_, mu_) - _delta_r_mp(MW_, MW_, MZ_, al, xi_, mu_))


def log_coefficient(MW, MZ, alpha, xi):
    with mp.workdps(30):
        MW_, MZ_, al = _cast(MW, MZ, alpha)
        c2, s2, g2 = _couplings(MW_, MZ_, alpha)
        MW2, MZ2 = MW_**2, MZ_**2
        # ln mH^2 coefficient of f_V(p^2) = M^2 B0 - B00 at large mH (B0 -> -ln mH^2, B00 -> -[(M^2+mH^2)/4 - p^2/12] ln mH^2),
        # with the mH^2/4 term dropped: it is q^2-independent and common to W and Z, so it cancels in Delta r.
        k = lambda MV2, p2: (-MV2 + MV2 / 4 - p2 / 12)
        bracket = (k(MW2, MW2) - k(MW2, 0)) + c2 / s2 * (k(MZ2, MZ2) - k(MW2, MW2))
        return float(-(al / (4 * mp.pi * s2)) * bracket / MW2)


# ----------------------------------------------------------------------------------------------------------------------------
# second route (DERIVATION step 9): unsplit R_xi propagator, direct numerical Feynman-parameter quadrature

def _B00_quad(p2, m0, m1, mu):
    D = lambda x: x * m1**2 + (1 - x) * m0**2 - x * (1 - x) * p2
    return mp.quad(lambda x: D(x) * (1 - mp.log(D(x) / mu**2)), [0, 1]) / 2


def _B0_quad(p2, m0, m1, mu):
    D = lambda x: x * m1**2 + (1 - x) * m0**2 - x * (1 - x) * p2
    return -mp.quad(lambda x: mp.log(D(x) / mu**2), [0, 1])


def _C00_quad(q2, M, mH, xi, mu):
    """(1/2) int_simplex [-ln(Delta3/mu^2)], Delta3 = x xi M^2 + y M^2 + z mH^2 - z(1-z) q^2."""
    def inner(z):
        return mp.quad(lambda y: -mp.log(((1 - y - z) * xi * M**2 + y * M**2 + z * mH**2 - z * (1 - z) * q2) / mu**2), [0, 1 - z])
    return mp.quad(inner, [0, 1]) / 2


def _sigma_route2(q2, mH, MV, coupling, xi, mu):
    pre = coupling / (16 * mp.pi**2)
    hw = -MV**2 * (_B0_quad(q2, MV, mH, mu) - (1 - xi) * _C00_quad(q2, MV, mH, xi, mu))
    hphi = _B00_quad(q2, mp.sqrt(xi) * MV, mH, mu)
    seagull = -A0(mH, mu) / 4
    return pre * (hw + hphi + seagull)


if __name__ == "__main__":
    MW, MZ, AL = 80.38, 91.19, 1 / 128.0
    with mp.workdps(20):
        c2, s2, g2 = _couplings(mp.mpf(MW), mp.mpf(MZ), mp.mpf(AL))
        print("route 2: unsplit R_xi propagator, numerical Feynman-parameter quadrature")
        for xi in (0.0, 0.3, 1.0, 4.0, 25.0):
            for q2 in (-2 * MW**2, 0.0, MW**2, MZ**2):
                w2 = _sigma_route2(mp.mpf(q2), mp.mpf(300), mp.mpf(MW), g2, mp.mpf(xi), mp.mpf(MW))
                z2 = _sigma_route2(mp.mpf(q2), mp.mpf(300), mp.mpf(MZ), g2 / c2, mp.mpf(xi), mp.mpf(MW))
                w1 = sigma_W(q2, 300.0, MW, MZ, AL, xi, MW)
                z1 = sigma_Z(q2, 300.0, MW, MZ, AL, xi, MW)
                print(f"  xi={xi:5.1f} q2={q2:10.1f}  Pi_W {w1:+.12e} vs {float(w2):+.12e}   Pi_Z {z1:+.12e} vs {float(z2):+.12e}")
    print("delta_r_higgs_rel(mH) for xi = 0, 1, 4, 25, and mu = MW vs 3.7 MW:")
    for mh in (1.0, 125.2, 300.0, 1000.0, 1e4):
        v = [delta_r_higgs_rel(mh, MW, MZ, AL, xi, MW) for xi in (0.0, 1.0, 4.0, 25.0)]
        print(f"  mH={mh:9.1f}: {v}  mu-shift {delta_r_higgs_rel(mh, MW, MZ, AL, 1.0, 3.7 * MW) - v[1]:.1e}")
    B = log_coefficient(MW, MZ, AL, 1.0)
    with mp.workdps(30):
        print("B =", B, " 11 alpha/(48 pi s^2) =", float(11 * mp.mpf(AL) / (48 * mp.pi * (1 - mp.mpf(MW)**2 / mp.mpf(MZ)**2))))
    for h1, h2 in ((1e3, 1e4), (1e6, 1e8), (1e12, 1e14)):
        f1, f2 = delta_r_higgs_rel(h1 * MW, MW, MZ, AL, 0.0, MW), delta_r_higgs_rel(h2 * MW, MW, MZ, AL, 0.0, MW)
        print(f"  slope between mH = {h1:.0e} and {h2:.0e} MW: {(f2 - f1) / math.log(h2**2 / h1**2):.15e}  constant: {f2 - B * math.log(h2**2):.12f}")
