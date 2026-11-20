"""Orchestrator's reference for the on-shell Delta r: Denner, Fortschr. Phys. 41 (1993) 307 (arXiv:0709.1075), eq. (8.14) with the self-energies of
appendix B ('t Hooft-Feynman gauge), transcribed from the printed page images. HIDDEN: never exported. Real parts, mpmath.
Sigma = -Pi (Denner's sign: M_eff^2 = M^2 - Sigma)."""
import functools
import mpmath as mp

DPS = 50


def _local(fn):
    @functools.wraps(fn)
    def w(*a, **k):
        with mp.workdps(max(DPS, mp.mp.dps)):
            return fn(*a, **k)
    return w


@functools.lru_cache(maxsize=None)
def _re_B0_cached(p2, m0, m1, mu, delta, dps):
    with mp.workdps(dps):
        return _re_B0(mp.mpf(p2), mp.mpf(m0), mp.mpf(m1), mp.mpf(mu), delta)


def re_B0(p2, m0, m1, mu, delta=0):
    return _re_B0_cached(mp.nstr(mp.mpf(p2), 45), mp.nstr(mp.mpf(m0), 45), mp.nstr(mp.mpf(m1), 45), mp.nstr(mp.mpf(mu), 45), delta, mp.mp.dps)


def _re_B0(p2, m0, m1, mu, delta=0):
    """Re B0 (Delta dropped, or shifted by `delta` to test pole cancellation): Delta - int_0^1 ln|(p2 x^2 - x(p2 - m0^2 + m1^2) + m1^2)/mu^2| dx."""
    f = lambda x: p2 * x * x - x * (p2 - m0 * m0 + m1 * m1) + m1 * m1
    pts = [mp.mpf(0), mp.mpf(1)]
    if p2 != 0:
        disc = (p2 - m0 * m0 + m1 * m1) ** 2 - 4 * p2 * m1 * m1
        if disc > 0:
            for sgn in (1, -1):
                r = ((p2 - m0 * m0 + m1 * m1) + sgn * mp.sqrt(disc)) / (2 * p2)
                if 0 < r < 1:
                    pts.append(r)
    pts = sorted(set(pts))
    sub = []
    for a, b in zip(pts[:-1], pts[1:]):
        sub += [a, (a + b) / 2, b]
    sub = sorted(set(sub))
    # small-mass endpoints need resolution
    extra = [mp.mpf(10) ** (-k) for k in range(2, 30, 2)]
    sub = sorted(set(sub + [e for e in extra] + [1 - e for e in extra]))
    return delta - mp.quad(lambda x: mp.log((abs(f(x)) + mp.mpf(10) ** (-95)) / mu**2), sub)


def A0(m, mu):
    m2 = mp.mpf(m) ** 2
    return m2 * (1 - mp.log(m2 / mp.mpf(mu) ** 2)) if m2 != 0 else mp.mpf(0)


class Params:
    def __init__(self, alpha, MZ, MW, MH, mt, mu=None, delta=0, leptons=(0.51099906e-3, 0.105658387, 1.7841),
                 quarks=((0.041, 0.041), (1.5, 0.15), (None, 4.5)), ckm=None):
        self.alpha, self.MZ, self.MW, self.MH, self.mt = (mp.mpf(t) for t in (alpha, MZ, MW, MH, mt))
        self.mu = mp.mpf(mu if mu is not None else MW)
        self.delta = delta
        self.leptons = [mp.mpf(t) for t in leptons]
        self.quarks = [(self.mt if u is None else mp.mpf(u), mp.mpf(d)) for u, d in quarks]
        self.ckm = ckm if ckm is not None else default_ckm()
        self.c2 = self.MW**2 / self.MZ**2
        self.s2 = 1 - self.c2
        self.s, self.c = mp.sqrt(self.s2), mp.sqrt(self.c2)


def default_ckm():
    s12, s23, s13 = mp.mpf("0.220"), mp.mpf("0.046"), mp.mpf("0.007")
    c12, c23, c13 = (mp.sqrt(1 - x * x) for x in (s12, s23, s13))
    return [[c12 * c13, s12 * c13, s13],
            [-s12 * c23 - c12 * s23 * s13, c12 * c23 - s12 * s23 * s13, s23 * c13],
            [s12 * s23 - c12 * c23 * s13, -c12 * s23 - s12 * c23 * s13, c23 * c13]]


def _B(P, p2, m0, m1):
    return re_B0(p2, m0, m1, P.mu, P.delta)


def _m2B00(P, m):
    """m^2 B0(0, m, m), zero for a massless fermion (the product is 0 x a singular value otherwise)."""
    return mp.mpf(0) if m == 0 else m * m * _B(P, 0, m, m)


def _small(k2):
    return mp.mpf("1e-18") if k2 == 0 else mp.mpf(k2)


def _gpm(P, Q, I3):
    return -(P.s / P.c) * Q, (I3 - P.s2 * Q) / (P.s * P.c)


def _fermions(P):
    """(m, Q, I3, N_C) for every fermion in the sums of Sigma^AA, Sigma^ZZ."""
    out = []
    for m in P.leptons:
        out += [(m, -1, -mp.mpf(1) / 2, 1), (mp.mpf(0), 0, mp.mpf(1) / 2, 1)]
    for mu_, md_ in P.quarks:
        out += [(mu_, mp.mpf(2) / 3, mp.mpf(1) / 2, 3), (md_, -mp.mpf(1) / 3, -mp.mpf(1) / 2, 3)]
    return out


@_local
def sigma_AA(P, k2, part):
    k2 = _small(k2)
    pref = -P.alpha / (4 * mp.pi)
    if part == "ferm":
        t = 0
        for m, Q, I3, NC in _fermions(P):
            if Q == 0:
                continue
            t += NC * 2 * Q**2 * (-(k2 + 2 * m * m) * _B(P, k2, m, m) + 2 * _m2B00(P, m) + k2 / 3)
        return pref * mp.mpf(2) / 3 * t
    MW2 = P.MW**2
    return pref * ((3 * k2 + 4 * MW2) * _B(P, k2, P.MW, P.MW) - 4 * MW2 * _B(P, 0, P.MW, P.MW))


@_local
def dsigma_AA_0(P, part):
    h = mp.mpf("1e-14")
    return (sigma_AA(P, h, part) - sigma_AA(P, -h, part)) / (2 * h)


@_local
def sigma_AZ_0(P, part):
    if part == "ferm":
        return mp.mpf(0)
    return P.alpha / (4 * mp.pi) * 2 * P.MW**2 * _B(P, 0, P.MW, P.MW) / (P.s * P.c)


@_local
def sigma_ZZ(P, k2, part):
    k2 = _small(k2)
    pref = -P.alpha / (4 * mp.pi)
    c2, s2, c4 = P.c2, P.s2, P.c2**2
    MW2, MZ2, MH2 = P.MW**2, P.MZ**2, P.MH**2
    if part == "ferm":
        t = 0
        for m, Q, I3, NC in _fermions(P):
            gp, gm = _gpm(P, Q, I3)
            t += NC * ((gp**2 + gm**2) * (-(k2 + 2 * m * m) * _B(P, k2, m, m) + 2 * _m2B00(P, m) + k2 / 3) + 3 / (4 * s2 * c2) * m * m * (_B(P, k2, m, m) if m != 0 else 0))
        return pref * mp.mpf(2) / 3 * t
    w = (((18 * c4 + 2 * c2 - mp.mpf(1) / 2) * k2 + (24 * c4 + 16 * c2 - 10) * MW2) * _B(P, k2, P.MW, P.MW)
         - (24 * c4 - 8 * c2 + 2) * MW2 * _B(P, 0, P.MW, P.MW) + (4 * c2 - 1) * k2 / 3) / (6 * s2 * c2)
    h = ((2 * MH2 - 10 * MZ2 - k2) * _B(P, k2, P.MZ, P.MH) - 2 * MZ2 * _B(P, 0, P.MZ, P.MZ) - 2 * MH2 * _B(P, 0, P.MH, P.MH)
         - (MZ2 - MH2) ** 2 / k2 * (_B(P, k2, P.MZ, P.MH) - _B(P, 0, P.MZ, P.MH)) - mp.mpf(2) / 3 * k2) / (12 * s2 * c2)
    return pref * (w + h)


@_local
def sigma_W(P, k2, part):
    k2 = _small(k2)
    pref = -P.alpha / (4 * mp.pi)
    c2, s2 = P.c2, P.s2
    MW2, MZ2, MH2 = P.MW**2, P.MZ**2, P.MH**2
    if part == "ferm":
        t = 0
        for m in P.leptons:
            t += (-(k2 - m * m / 2) * _B(P, k2, 0, m) + k2 / 3 + _m2B00(P, m) + m**4 / (2 * k2) * (_B(P, k2, 0, m) - _B(P, 0, 0, m)))
        t *= mp.mpf(2) / 3 / (2 * s2)
        tq = 0
        for i, (mu_, md_) in enumerate([(q[0], None) for q in P.quarks]):
            pass
        ups = [q[0] for q in P.quarks]
        downs = [q[1] for q in P.quarks]
        for i, mu_ in enumerate(ups):
            for j, md_ in enumerate(downs):
                V2 = P.ckm[i][j] ** 2
                tq += V2 * (-(k2 - (mu_**2 + md_**2) / 2) * _B(P, k2, mu_, md_) + k2 / 3 + _m2B00(P, mu_) + _m2B00(P, md_)
                            + (mu_**2 - md_**2) ** 2 / (2 * k2) * (_B(P, k2, mu_, md_) - _B(P, 0, mu_, md_)))
        tq *= mp.mpf(2) / 3 / (2 * s2) * 3
        return pref * (t + tq)
    ph = mp.mpf(2) / 3 * ((2 * MW2 + 5 * k2) * _B(P, k2, P.MW, 0) - 2 * MW2 * _B(P, 0, P.MW, P.MW)
                          - MW2**2 / k2 * (_B(P, k2, P.MW, 0) - _B(P, 0, P.MW, 0)) + k2 / 3)
    wz = (((40 * c2 - 1) * k2 + (16 * c2 + 54 - 10 / c2) * MW2) * _B(P, k2, P.MW, P.MZ)
          - (16 * c2 + 2) * (MW2 * _B(P, 0, P.MW, P.MW) + MZ2 * _B(P, 0, P.MZ, P.MZ)) + (4 * c2 - 1) * mp.mpf(2) / 3 * k2
          - (8 * c2 + 1) * (MW2 - MZ2) ** 2 / k2 * (_B(P, k2, P.MW, P.MZ) - _B(P, 0, P.MW, P.MZ))) / (12 * s2)
    hh = ((2 * MH2 - 10 * MW2 - k2) * _B(P, k2, P.MW, P.MH) - 2 * MW2 * _B(P, 0, P.MW, P.MW) - 2 * MH2 * _B(P, 0, P.MH, P.MH)
          - (MW2 - MH2) ** 2 / k2 * (_B(P, k2, P.MW, P.MH) - _B(P, 0, P.MW, P.MH)) - mp.mpf(2) / 3 * k2) / (12 * s2)
    return pref * (ph + wz + hh)


@_local
def delta_vb(P):
    return P.alpha / (4 * mp.pi * P.s2) * (6 + (7 - 4 * P.s2) / (2 * P.s2) * mp.log(P.c2))


@_local
def delta_r(P, part="all"):
    """Delta r, eq. (8.14); part = 'all', 'ferm' (fermion loops only), 'bos' (everything else, including delta_VB)."""
    parts = ("ferm", "bos") if part == "all" else (part,)
    tot = 0
    for p in parts:
        t = dsigma_AA_0(P, p)
        t += -(P.c2 / P.s2) * (sigma_ZZ(P, P.MZ**2, p) / P.MZ**2 - sigma_W(P, P.MW**2, p) / P.MW**2)
        t += (sigma_W(P, 0, p) - sigma_W(P, P.MW**2, p)) / P.MW**2
        t += 2 * (P.c / P.s) * sigma_AZ_0(P, p) / P.MZ**2
        if p == "bos":
            t += delta_vb(P)
        tot += t
    return tot


# ----------------------------------------------------------------------------- bosonic-only float API used by the bos_se oracle
def _P(MW, MZ, MH, alpha, mu):
    return Params(alpha, MZ, MW, MH, 0, mu=mu)


def _real(x):
    return float(mp.re(x))


def _dps(MW, MH, k2=0.0):
    """Working precision: the M_H^2 terms cancel against each other and against the k^2 -> 0 limit (k^2 = 1e-18): 8 digits per decade of the mass ratio."""
    return int(60 + 8 * max(0.0, mp.log10(max(abs(MH), abs(MW)) / abs(MW))) + 4 * max(0.0, mp.log10(max(abs(MW), abs(MH)) ** 2 / 1.0) - 6))


def sig_AA(k2, MW, MZ, MH, alpha, mu):
    with mp.workdps(_dps(MW, MH)):
        return _real(sigma_AA(_P(MW, MZ, MH, alpha, mu), k2, "bos"))


def sig_AZ(k2, MW, MZ, MH, alpha, mu):
    """Denner (B.2), bosonic part, at general k^2."""
    with mp.workdps(_dps(MW, MH)):
        P = _P(MW, MZ, MH, alpha, mu)
        k2 = _small(k2)
        pref = -P.alpha / (4 * mp.pi)
        c2, MW2 = P.c2, P.MW**2
        B = lambda a, b, c: _B(P, a, b, c)
        t = (((9 * c2 + mp.mpf(1) / 2) * k2 + (12 * c2 + 4) * MW2) * B(k2, P.MW, P.MW) - (12 * c2 - 2) * MW2 * B(0, P.MW, P.MW) + k2 / 3)
        return _real(pref * (-1 / (3 * P.s * P.c)) * t)


def sig_ZZ(k2, MW, MZ, MH, alpha, mu):
    with mp.workdps(_dps(MW, MH)):
        return _real(sigma_ZZ(_P(MW, MZ, MH, alpha, mu), k2, "bos"))


def sig_W(k2, MW, MZ, MH, alpha, mu):
    with mp.workdps(_dps(MW, MH)):
        return _real(sigma_W(_P(MW, MZ, MH, alpha, mu), k2, "bos"))


def dr_bos(MW, MZ, MH, alpha):
    """The non-fermionic part of the on-shell Delta r (eq. 8.14), bosonic self-energies + delta_VB, 't Hooft-Feynman gauge. mu drops out (UV finite)."""
    with mp.workdps(_dps(MW, MH)):
        P = Params(alpha, MZ, MW, MH, 0, mu=MW)
        return _real(delta_r(P, "bos"))
