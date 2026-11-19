"""Bosonic one-loop gauge-boson self-energies (gauge, Goldstone, Higgs and ghost loops, no fermions) of the
SU(2)xU(1) electroweak theory in the 't Hooft-Feynman gauge, d = 4 - 2 eps, MS-bar at scale mu.

The loop coefficients below were generated (builds/bos_se-b/gen/*.py) from the Lagrangian: every Feynman rule is
extracted from L (Yang-Mills + Higgs + gauge fixing + ghost terms) by plane-wave multilinear differentiation, every
diagram (bubbles, ghost loops, seagulls) is contracted in d dimensions and reduced to A0, B0 (see DERIVATION.md).
Sigma_T = alpha/(4 pi) * [ sum_i coeff_i * (finite loop function_i) + rational rest ],
A0f(m) = m^2 (1 - ln m^2/mu^2),  B0f(k2; m1, m2) = - int_0^1 dx ln[(x m2^2 + (1-x) m1^2 - x(1-x) k2 - i0)/mu^2]  (real part).
"""
import math
from mpmath import mp, mpf, mpc, log, sqrt, pi, quad, fabs, floor, ceil, log10

PROVENANCE = {
    "sigma_AA": ("derived", "photon bosonic self-energy from the Lagrangian: W, phi, ghost bubbles and seagulls, MS-bar"),
    "sigma_AZ": ("derived", "photon-Z bosonic mixing from the Lagrangian: W, phi, ghost bubbles and seagulls, MS-bar"),
    "sigma_ZZ": ("derived", "Z bosonic self-energy from the Lagrangian: W, phi, H-Z, H-chi, ghost bubbles and seagulls, MS-bar"),
    "sigma_W": ("derived", "W bosonic self-energy from the Lagrangian: all gauge/scalar/ghost bubbles and seagulls, MS-bar"),
}

_TINY = mpf(10) ** (-30)     # k^2 = 0 is evaluated as the limit k^2 -> _TINY * MW^2 (analytic point, working precision raised)


def _J(r):
    """Re int_0^1 ln(x - r) dx = Re[(1-r) ln(1-r) + r ln(-r)] - 1 (r a root of the Feynman-parameter quadratic)."""
    r = mpc(r)
    t = mpf(0)
    if fabs(1 - r) > mpf(10) ** (-(mp.dps // 2)):
        t += ((1 - r) * log(1 - r)).real
    if fabs(r) > mpf(10) ** (-(mp.dps // 2)):
        t += (r * log(-r)).real
    return t - 1


def _A0f(m2, mu2):
    return mpf(0) if m2 == 0 else m2 * (1 - log(m2 / mu2))


def _B0f(k2, a, b, mu2):
    """finite part (Delta removed) of Re B0(k2; sqrt a, sqrt b); k2 != 0."""
    p = b - a - k2
    disc = p * p - 4 * k2 * a
    sq = sqrt(mpc(disc))
    r1 = (-p + sq) / (2 * k2)
    r2 = (-p - sq) / (2 * k2)
    return -(log(fabs(k2)) + _J(r1) + _J(r2)) + log(mu2)


def _prec(k2, mw, mz, mh, mu):
    big = max(mw * mw, mz * mz, mh * mh, fabs(k2), mu * mu)
    small = min(x for x in (mw * mw, mz * mz, mh * mh, fabs(k2), mu * mu) if x > 0)
    return int(70 + 4 * ceil(log10(big / small)))
def _terms_AA(kk, mw, mh, c, s):
    # returns (coefficients of the finite loop functions {name: coeff}, rational rest, UV-pole coefficient); units alpha/(4 pi)
    co = {}
    co['A0f_W'] = 4
    co['B0f_WW'] = -3*kk - 4*mw**2
    rest = -4*mw**2
    pole = -3*kk
    return co, rest, pole

def _terms_AZ(kk, mw, mh, c, s):
    # returns (coefficients of the finite loop functions {name: coeff}, rational rest, UV-pole coefficient); units alpha/(4 pi)
    co = {}
    co['A0f_W'] = 2*(6*c**2 - 1)/(3*c*s)
    co['B0f_WW'] = -(18*c**2*kk + 24*c**2*mw**2 + kk + 8*mw**2)/(6*c*s)
    rest = -(36*c**2*mw**2 + kk - 6*mw**2)/(9*c*s)
    pole = -(18*c**2*kk + kk + 12*mw**2)/(6*c*s)
    return co, rest, pole

def _terms_ZZ(kk, mw, mh, c, s):
    # returns (coefficients of the finite loop functions {name: coeff}, rational rest, UV-pole coefficient); units alpha/(4 pi)
    co = {}
    co['A0f_H'] = -(2*c**2*kk - c**2*mh**2 + mw**2)/(12*c**4*kk*(c - 1)*(c + 1))
    co['A0f_W'] = -(12*c**4 - 4*c**2 + 1)/(3*c**2*(c - 1)*(c + 1))
    co['A0f_Z'] = -(2*c**2*kk + c**2*mh**2 - mw**2)/(12*c**4*kk*(c - 1)*(c + 1))
    co['B0f_HZ'] = -(c**4*kk**2 - 2*c**4*kk*mh**2 + c**4*mh**4 + 10*c**2*kk*mw**2 - 2*c**2*mh**2*mw**2 + mw**4)/(12*c**6*kk*(c - 1)*(c + 1))
    co['B0f_WW'] = (36*c**4*kk + 48*c**4*mw**2 + 4*c**2*kk + 32*c**2*mw**2 - kk - 20*mw**2)/(12*c**2*(c - 1)*(c + 1))
    rest = (72*c**6*mw**2 + 4*c**4*kk - 24*c**4*mw**2 - 2*c**2*kk + 3*c**2*mh**2 + 6*c**2*mw**2 + 3*mw**2)/(18*c**4*(c - 1)*(c + 1))
    pole = (18*c**6*kk + 2*c**4*kk + 24*c**4*mw**2 - c**2*kk - 12*c**2*mw**2 - 6*mw**2)/(6*c**4*(c - 1)*(c + 1))
    return co, rest, pole

def _terms_W(kk, mw, mh, c, s):
    # returns (coefficients of the finite loop functions {name: coeff}, rational rest, UV-pole coefficient); units alpha/(4 pi)
    co = {}
    co['A0f_H'] = -(2*kk - mh**2 + mw**2)/(12*kk*(c - 1)*(c + 1))
    co['A0f_W'] = -(20*c**2*kk + c**2*mh**2 - 2*c**2*mw**2 + mw**2)/(12*c**2*kk*(c - 1)*(c + 1))
    co['A0f_Z'] = -(8*c**2 + 1)*(2*c**2*kk + c**2*mw**2 - mw**2)/(12*c**2*kk*(c - 1)*(c + 1))
    co['B0f_0W'] = -2*(5*kk**2 + 2*kk*mw**2 - mw**4)/(3*kk)
    co['B0f_HW'] = -(kk**2 - 2*kk*mh**2 + 10*kk*mw**2 + mh**4 - 2*mh**2*mw**2 + mw**4)/(12*kk*(c - 1)*(c + 1))
    co['B0f_WZ'] = (40*c**6*kk**2 + 16*c**6*kk*mw**2 - 8*c**6*mw**4 - c**4*kk**2 + 54*c**4*kk*mw**2 + 15*c**4*mw**4 - 10*c**2*kk*mw**2 - 6*c**2*mw**4 - mw**4)/(12*c**4*kk*(c - 1)*(c + 1))
    rest = (2*c**2*kk + 3*c**2*mh**2 + 54*c**2*mw**2 + 3*mw**2)/(18*c**2*(c - 1)*(c + 1))
    pole = (19*c**2*kk + 12*c**2*mw**2 - 6*mw**2)/(6*c**2*(c - 1)*(c + 1))
    return co, rest, pole

_MASS2 = {}


def _loopvals(co, kk, mw, mz, mh, mu2):
    m2 = {'0': mpf(0), 'W': mw * mw, 'Z': mz * mz, 'H': mh * mh}
    tot = mpf(0)
    for name, cf in co.items():
        kind, tags = name.split('_')[0], name.split('_')[1]
        if kind == 'A0f':
            tot += cf * _A0f(m2[tags], mu2)
        else:
            tot += cf * _B0f(kk, m2[tags[0]], m2[tags[1]], mu2)
    return tot


def _sigma(which, k2, MW, MZ, MH, alpha, mu):
    mw0, mz0, mh0, mu0 = mpf(MW), mpf(MZ), mpf(MH), mpf(mu)
    k20 = mpf(k2)
    with mp.workdps(_prec(k20 if k20 != 0 else _TINY * mw0 * mw0, mw0, mz0, mh0, mu0)):
        mw, mz, mh, mu_ = mpf(MW), mpf(MZ), mpf(MH), mpf(mu)
        kk = mpf(k2)
        if kk == 0:
            kk = _TINY * mw * mw
        c = mw / mz
        s = sqrt(1 - c * c)
        fn = {'AA': _terms_AA, 'AZ': _terms_AZ, 'ZZ': _terms_ZZ, 'W': _terms_W}[which]
        co, rest, pole = fn(kk, mw, mh, c, s)
        val = _loopvals(co, kk, mw, mz, mh, mu_ * mu_) + rest
        val = val * mpf(alpha) / (4 * pi)
        return float(val)


def sigma_AA(k2, MW, MZ, MH, alpha, mu):
    return _sigma('AA', k2, MW, MZ, MH, alpha, mu)


def sigma_AZ(k2, MW, MZ, MH, alpha, mu):
    return _sigma('AZ', k2, MW, MZ, MH, alpha, mu)


def sigma_ZZ(k2, MW, MZ, MH, alpha, mu):
    return _sigma('ZZ', k2, MW, MZ, MH, alpha, mu)


def sigma_W(k2, MW, MZ, MH, alpha, mu):
    return _sigma('W', k2, MW, MZ, MH, alpha, mu)


def _pole(which, k2, MW, MZ, MH):
    """coefficient of alpha/(4 pi) * Delta (UV pole), from the same generated reduction"""
    with mp.workdps(60):
        mw, mz, mh = mpf(MW), mpf(MZ), mpf(MH)
        c = mw / mz
        fn = {'AA': _terms_AA, 'AZ': _terms_AZ, 'ZZ': _terms_ZZ, 'W': _terms_W}[which]
        return fn(mpf(k2) + _TINY, mw, mh, c, sqrt(1 - c * c))[2]


if __name__ == "__main__":
    MW, MZ, MH, AL = 80.38, 91.19, 125.0, 1 / 128.0
    mu = 1.7 * MW
    print("sigma_AA(0), sigma_AZ(0), sigma_ZZ(0), sigma_W(0):",
          [f(0.0, MW, MZ, MH, AL, mu) for f in (sigma_AA, sigma_AZ, sigma_ZZ, sigma_W)])
    print("sigma at k2 = MW^2:", [f(MW**2, MW, MZ, MH, AL, mu) for f in (sigma_AA, sigma_AZ, sigma_ZZ, sigma_W)])
    # second route 1: closed-form B0 against direct numerical Feynman-parameter integration
    with mp.workdps(30):
        for (k2, a, b) in [(-3e3, 80.38**2, 91.19**2), (2e3, 80.38**2, 125.0**2), (0.5e3, 0.0, 80.38**2),
                           (3e4, 80.38**2, 91.19**2), (1.2e4, 80.38**2, 0.0)]:
            k2, a, b, mu2 = mpf(k2), mpf(a), mpf(b), mpf(80.38) ** 2
            Q = lambda x: k2 * x * x + (b - a - k2) * x + a
            disc = (b - a - k2) ** 2 - 4 * k2 * a
            pts = [mpf(0), mpf(1)]
            if disc >= 0:
                for sg in (1, -1):
                    rt = (-(b - a - k2) + sg * sqrt(disc)) / (2 * k2)
                    if 0 < rt < 1:
                        pts.append(rt)
            pts = sorted(pts)
            num = -quad(lambda x: log(fabs(Q(x)) / mu2), pts)
            print("B0f closed form vs quadrature:", float(_B0f(k2, a, b, mu2)), float(num))
    # second route 2: mu dependence is +pole: d Sigma / d ln mu^2 = +(alpha/4 pi) * pole(k2)  (Delta enters with + ln mu^2)
    for nm, f in (("AA", sigma_AA), ("AZ", sigma_AZ), ("ZZ", sigma_ZZ), ("W", sigma_W)):
        k2 = 0.37 * MW**2
        h = 1e-4
        d = (f(k2, MW, MZ, MH, AL, mu * (1 + h)) - f(k2, MW, MZ, MH, AL, mu * (1 - h))) / (2 * h) / 2   # d/d ln mu^2 = (1/2) d/d ln mu
        print(f"mu-dependence {nm}: numeric dSigma/dln mu^2 = {d:.6e}  vs  +alpha/4pi*pole = {float(_pole(nm, k2, MW, MZ, MH) * AL / (4 * pi)):.6e}")
    # second route 3: Delta rho from the Higgs (heavy-Higgs logarithm): Sigma_ZZ(0)/MZ^2 - Sigma_W(0)/MW^2
    def drho(mh):
        return sigma_ZZ(0.0, MW, MZ, mh, AL, MW) / MZ**2 - sigma_W(0.0, MW, MZ, mh, AL, MW) / MW**2
    c2 = (MW / MZ) ** 2
    for mh in (1e4, 1e6):
        sl = (drho(mh * 10) - drho(mh)) / math.log(100.0)
        print(f"d(drho)/d ln MH^2 at MH={mh:g}: {sl:.6e}   expected -3 alpha/(16 pi c^2) = {-3 * AL / (16 * 3.141592653589793 * c2):.6e}")
    # Sigma_AZ(0) = -(alpha/2pi) MW^2/(s c) B0(0; MW, MW)
    with mp.workdps(30):
        c = mpf(MW) / MZ
        s = sqrt(1 - c * c)
        b0 = _A0f(mpf(MW) ** 2, mpf(mu) ** 2) / mpf(MW) ** 2 - 1
        print("Sigma_AZ(0):", sigma_AZ(0.0, MW, MZ, MH, AL, mu), " closed form -alpha/(2pi) MW^2/(sc) B0(0;W,W):",
              float(-mpf(AL) / (2 * pi) * mpf(MW) ** 2 / (s * c) * b0))
