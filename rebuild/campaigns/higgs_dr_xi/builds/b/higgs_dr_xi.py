"""Gauge-parameter dependence of the Higgs part of Delta r (R_xi gauge, one loop). See DERIVATION.md."""
import math
import mpmath as mp

PROVENANCE = {
    "sigma_W": ("derived", "H-W + H-Goldstone + H seagull, Feynman-parameter MS-bar integrals, real part"),
    "sigma_Z": ("derived", "same for Z"),
    "delta_r_higgs_rel": ("derived", "Delta r = [Pi_W(MW2)-Pi_W(0)]/MW2 - (c2/s2)[Pi_W/MW2 - Pi_Z/MZ2] minus reference"),
    "log_coefficient": ("derived", "coefficient of ln mH^2 from large-mH expansion of the diagram integrals"),
}
_BASE = 80


def _xlogx(m2, mu2):
    return mp.mpf(0) if m2 == 0 else m2 * mp.log(m2 / mu2)


def _lnabs_int_roots(r):
    """Int_0^1 ln|x - r| dx for real r, or Int ln(x-r) (principal) for complex r."""
    if isinstance(r, mp.mpc) and r.imag != 0:
        return (1 - r) * mp.log(1 - r) + r * mp.log(-r) - 1
    r = mp.re(r)
    t1 = (1 - r) * mp.log(abs(1 - r)) if r != 1 else mp.mpf(0)
    t2 = r * mp.log(abs(r)) if r != 0 else mp.mpf(0)
    return t1 + t2 - 1


def _upow_log(u, n, r):
    """antiderivative of u^n ln|u| : u^(n+1)/(n+1) ln|u| - u^(n+1)/(n+1)^2 (u may be complex)."""
    if u == 0:
        return mp.mpf(0)
    lu = mp.log(abs(u)) if not isinstance(u, mp.mpc) or u.imag == 0 else mp.log(u)
    if isinstance(u, mp.mpc) and u.imag == 0:
        u = u.real
    return u ** (n + 1) / (n + 1) * lu - u ** (n + 1) / (n + 1) ** 2


def _D_ln_root(q2, ra, rb):
    """Int_0^1 q2 (x-ra)(x-rb) ln|x-ra| dx"""
    d = ra - rb
    tot = 0
    for x in (mp.mpf(1), mp.mpf(0)):
        u = x - ra
        tot += (1 if x == 1 else -1) * (_upow_log(u, 2, ra) + d * _upow_log(u, 1, ra))
    return q2 * tot


def _integrals(q2, m1, m2, mu2):
    """I0 = Re Int ln(D/mu2), I1 = Re Int D ln(D/mu2), I2 = Int D ; D = x m1 + (1-x) m2 - x(1-x) q2 (all squared masses)."""
    I2 = (m1 + m2) / 2 - q2 / 6
    if q2 == 0:
        b = m1 - m2
        if b == 0:
            c = m2
            lc = mp.log(c / mu2) if c != 0 else mp.mpf(0)
            return lc, c * lc, I2
        I0 = (_xlogx(m1, mu2) - _xlogx(m2, mu2)) / b - 1
        I1 = ((m1 ** 2 * (mp.log(m1 / mu2) if m1 != 0 else 0) - m2 ** 2 * (mp.log(m2 / mu2) if m2 != 0 else 0)) / 2 - (m1 ** 2 - m2 ** 2) / 4) / b
        return I0, I1, I2
    # D = q2 x^2 + (m1-m2-q2) x + m2
    bq = m1 - m2 - q2
    disc = bq * bq - 4 * q2 * m2
    if disc >= 0:
        sq = mp.sqrt(disc)
        ra, rb = (-bq + sq) / (2 * q2), (-bq - sq) / (2 * q2)
        ra, rb = mp.mpf(ra), mp.mpf(rb)
        lq = mp.log(abs(q2) / mu2)
        I0 = lq + _lnabs_int_roots(ra) + _lnabs_int_roots(rb)
        I1 = lq * I2 + _D_ln_root(q2, ra, rb) + _D_ln_root(q2, rb, ra)
    else:
        sq = mp.sqrt(-disc)
        ra, rb = mp.mpc(-bq, sq) / (2 * q2), mp.mpc(-bq, -sq) / (2 * q2)
        lq = mp.log(abs(q2) / mu2)
        # ln|q2| + ln(x-ra) + ln(x-rb), conjugate roots, real part: 2 Re
        I0 = lq + 2 * mp.re(_lnabs_int_roots(ra))
        I1 = lq * I2 + 2 * mp.re(_D_ln_root(q2, ra, rb))
        # sign of q2 inside the log: D = q2 (x-ra)(x-rb), ln|D| = ln|q2| + ln|x-ra| + ln|x-rb|  (done above)
    return I0, I1, I2


def _prec(q2, *ms):
    ms = [abs(x) for x in ms if x != 0]
    hi, lo = max(ms), min(ms)
    ext = 4 * max(0, math.log10(float(hi / lo)))
    if q2 != 0:
        ext += 4 * max(0, math.log10(float(hi / abs(q2)))) + 2 * max(0, math.log10(float(abs(q2) / lo)))
    return _BASE + int(ext)


def _B0B00(q2, m1, m2, mu2):
    with mp.workdps(_prec(q2, m1, m2, mu2) if (m1 != 0 or m2 != 0) else _BASE):
        q2, m1, m2, mu2 = mp.mpf(q2), mp.mpf(m1), mp.mpf(m2), mp.mpf(mu2)
        I0, I1, I2 = _integrals(q2, m1, m2, mu2)
        return -I0, (I2 - I1) / 2


def _A0(m2, mu2):
    return -m2 * (mp.log(m2 / mu2) - 1) if m2 != 0 else mp.mpf(0)


def _hv_terms(q2, mH, M, g2v, xi, mu2):
    """Three diagram contributions (units 1/16pi^2 included later): HV, H-Goldstone, seagull, for vector mass M, coupling g2v=g_V^2."""
    mH2, M2 = mH * mH, M * M
    B0, B00 = _B0B00(q2, mH2, M2, mu2)
    _, B00x = _B0B00(q2, mH2, xi * M2, mu2)
    hv = -g2v * M2 * (B0 - (B00 - B00x) / M2)
    hphi = g2v * B00x
    sea = -g2v / 4 * _A0(mH2, mu2)
    return hv, hphi, sea


def _setup(MW, MZ, alpha):
    MW, MZ, alpha = mp.mpf(MW), mp.mpf(MZ), mp.mpf(alpha)
    c2 = MW ** 2 / MZ ** 2
    s2 = 1 - c2
    g2 = 4 * mp.pi * alpha / s2
    return MW, MZ, c2, s2, g2


def _sigma(q2, mH, MW, MZ, alpha, xi, mu, Z):
    with mp.workdps(_BASE + 40):
        MWm, MZm, c2, s2, g2 = _setup(MW, MZ, alpha)
        M = MZm if Z else MWm
        g2v = g2 / c2 if Z else g2
        K = 1 / (16 * mp.pi ** 2)
        tot = sum(_hv_terms(mp.mpf(q2), mp.mpf(mH), M, g2v, mp.mpf(xi), mp.mpf(mu) ** 2))
        return float(K * tot)


def sigma_W(q2, mH, MW, MZ, alpha, xi, mu):
    return _sigma(q2, mH, MW, MZ, alpha, xi, mu, False)


def sigma_Z(q2, mH, MW, MZ, alpha, xi, mu):
    return _sigma(q2, mH, MW, MZ, alpha, xi, mu, True)


def _dr_abs(mH, MW, MZ, alpha, xi, mu):
    """Delta r_H (mu-dependent constant included), mp value at the caller's precision."""
    MWm, MZm, c2, s2, g2 = _setup(MW, MZ, alpha)
    mH, xi, mu2 = mp.mpf(mH), mp.mpf(xi), mp.mpf(mu) ** 2
    K = 1 / (16 * mp.pi ** 2)
    PW = lambda q2: K * sum(_hv_terms(mp.mpf(q2), mH, MWm, g2, xi, mu2))
    PZ = K * sum(_hv_terms(MZm ** 2, mH, MZm, g2 / c2, xi, mu2))
    pw_m, pw_0 = PW(MWm ** 2), PW(0)
    return (pw_m - pw_0) / MWm ** 2 - (c2 / s2) * (pw_m / MWm ** 2 - PZ / MZm ** 2)


def delta_r_higgs_rel(mH, MW, MZ, alpha, xi, mu):
    ratio = abs(math.log10(float(mH) / float(MW))) if mH > 0 else 0.0
    with mp.workdps(_BASE + int(6 * ratio) + 20):
        return float(_dr_abs(mH, MW, MZ, alpha, xi, mu) - _dr_abs(MW, MW, MZ, alpha, xi, mu))


def log_coefficient(MW, MZ, alpha, xi):
    """Coefficient of L = ln mH^2 per diagram (B0 -> -1, B00 -> -(mH2/2 + m2/2 - q2/6)/2, A0 -> -mH2; the mH^2 terms cancel in the sum),
    pushed through the Delta r combination."""
    with mp.workdps(60):
        MWm, MZm, c2, s2, g2 = _setup(MW, MZ, alpha)
        xi = mp.mpf(xi)
        K = 1 / (16 * mp.pi ** 2)

        def Lc(q2, M, g2v):
            # keep mH^2 symbolically as a separate bucket: (mH2 coefficient, rest)
            b00 = lambda m2: (-mp.mpf(1) / 4, -(m2 / 2 - q2 / 6) / 2)
            b0 = -1
            # HV: -g2v M2 [B0 - (B00(M) - B00(xi M))/M2]
            a, b = b00(M ** 2), b00(xi * M ** 2)
            hv_m = -g2v * (-(a[0] - b[0]))
            hv_r = -g2v * (M ** 2 * b0 - (a[1] - b[1]))
            hp_m, hp_r = g2v * b[0], g2v * b[1]
            se_m, se_r = -g2v / 4 * (-1), 0
            return hv_m + hp_m + se_m, hv_r + hp_r + se_r

        def pi(q2, M, g2v):
            m, r = Lc(q2, M, g2v)
            assert abs(m) < mp.mpf(10) ** -40, "mH^2 ln mH^2 terms must cancel"
            return K * r
        pw_m, pw_0 = pi(MWm ** 2, MWm, g2), pi(0, MWm, g2)
        pz = pi(MZm ** 2, MZm, g2 / c2)
        return float((pw_m - pw_0) / MWm ** 2 - (c2 / s2) * (pw_m / MWm ** 2 - pz / MZm ** 2))


if __name__ == "__main__":
    MW, MZ, al = 80.38, 91.19, 1 / 128.0
    print("log_coefficient xi=0,1,4:", [log_coefficient(MW, MZ, al, x) for x in (0, 1, 4)])
    with mp.workdps(30):
        s2 = 1 - mp.mpf(MW) ** 2 / mp.mpf(MZ) ** 2
        print("independent 11 alpha/(48 pi s^2):", 11 * mp.mpf(al) / (48 * mp.pi * s2))
    for xi in (0.0, 0.3, 1.0, 4.0, 25.0):
        print("xi", xi, "dr_rel(300):", delta_r_higgs_rel(300.0, MW, MZ, al, xi, MW), "sigma_W(MW2):", sigma_W(MW ** 2, 300., MW, MZ, al, xi, MW))
    # (i) direct quadrature of the Feynman integrals vs closed forms
    with mp.workdps(30):
        for q2, m1, m2 in [(0.0, 300.0 ** 2, MW ** 2), (MW ** 2, 300.0 ** 2, MW ** 2), (-2 * MW ** 2, 300.0 ** 2, 0.0), (MW ** 2, 50.0 ** 2, 0.0)]:
            q2, m1, m2 = mp.mpf(q2), mp.mpf(m1), mp.mpf(m2)
            D = lambda x: x * m1 + (1 - x) * m2 - x * (1 - x) * q2
            pts = [0, 1]
            if q2 != 0:
                disc = (m1 - m2 - q2) ** 2 - 4 * q2 * m2
                if disc > 0:
                    pts = sorted([0, 1] + [r for r in ((-(m1 - m2 - q2) + s * mp.sqrt(disc)) / (2 * q2) for s in (1, -1)) if 0 < r < 1])
            mu2 = mp.mpf(MW) ** 2
            b0q = -mp.quad(lambda x: mp.log(abs(D(x)) / mu2), pts)
            b00q = mp.quad(lambda x: D(x) * (1 - mp.log(abs(D(x)) / mu2)), pts) / 2
            b0, b00 = _B0B00(q2, m1, m2, mu2)
            print("quad check B0,B00 rel diff:", mp.nstr(abs(b0q / b0 - 1), 3), mp.nstr(abs(b00q / b00 - 1), 3))
            # (ii) PV reduction: B1 = [A0(m1)-A0(m2)-(q2+m1-m2)... ] with D1=k^2-m1, D2=(k+q)^2-m2
            if q2 != 0:
                A1, A2 = _A0(m1, mu2), _A0(m2, mu2)
                B1 = (A1 - A2 - (q2 - m2 + m1) * b0) / (2 * q2)
                b00pv = (A2 + 2 * m1 * b0 + (q2 + m1 - m2) * B1) / 6 + ((m1 + m2) / 6 - q2 / 18)
                print("PV-reduction B00 rel diff:", mp.nstr(abs(b00pv / b00 - 1), 3))
    # (iii) unitary-gauge (xi -> infinity analytic) sum vs diagram-by-diagram sum at several xi
    with mp.workdps(40):
        q2, mH = mp.mpf(MW) ** 2, mp.mpf(300.0)
        B0, B00 = _B0B00(q2, mH ** 2, mp.mpf(MW) ** 2, mp.mpf(MW) ** 2)
        uni = (-mp.mpf(MW) ** 2 * B0 + B00 - _A0(mH ** 2, mp.mpf(MW) ** 2) / 4) * 4 * mp.pi * mp.mpf(al) / (1 - mp.mpf(MW) ** 2 / mp.mpf(MZ) ** 2) / (16 * mp.pi ** 2)
        for xi in (0.0, 1.0, 4.0):
            print("unitary vs diagram sum, xi", xi, float(uni) / sigma_W(MW ** 2, 300., MW, MZ, al, xi, MW) - 1)
    # (iv) slope
    f = lambda mh: delta_r_higgs_rel(mh, MW, MZ, al, 1.0, MW)
    h1, h2 = 1e5 * MW, 1e6 * MW
    print("slope", (f(h2) - f(h1)) / math.log((h2 / h1) ** 2))
