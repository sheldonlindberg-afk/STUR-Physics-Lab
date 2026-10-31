#!/usr/bin/env python3
"""Can a generic axion-like particle (ALP) mimic STUR-ROLL's beta(l)?
STUR: hilltop roll 0 -> pi, amplitude fixed at alpha/2 (k = 1), shape set by m.
ALP: V = m^2 f^2 (1 - cos theta) from rest at small theta_i (oscillation),
amplitude free. Both projected with CLASS's exact E-mode source.
Usage: python alp_vs_stur.py <class run directory>   (see class_check.py)"""
import sys
import numpy as np
from scipy.integrate import solve_ivp
from scipy.special import spherical_jn, gammaln
rdir = sys.argv[1]
sys.argv = [sys.argv[0]]
import stur_final as F

raw = np.fromfile(f"{rdir}/stur_esource.txt", sep=" ")
nk, nt, tau0 = int(raw[0]), int(raw[1]), raw[2]
k, tau = raw[3:3 + nk], raw[3 + nk:3 + nk + nt]
S = raw[3 + nk + nt:].reshape(nt, nk).T
th = np.loadtxt(f"{rdir}/stur_00_thermodynamics.dat")
zt = np.interp(tau, th[::-1, 2], th[::-1, 1])
wk = k ** (0.9649 - 1) * np.gradient(np.log(k))
wt = np.gradient(tau)
LS = [2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 30]
SP = {}
for l in LS:
    x = np.maximum(np.outer(k, np.maximum(tau0 - tau, 1e-8)), 1e-8)
    Nl = np.exp(0.5 * (gammaln(l + 3) - gammaln(l - 1)))
    SP[l] = S * Nl * spherical_jn(l, x) / x ** 2 * wt[None, :]


def beta_l(hist):
    s2 = np.sin(2 * np.radians(hist(zt)))[None, :]
    out = []
    for l in LS:
        dE, dB = SP[l].sum(1), (SP[l] * s2).sum(1)
        r = np.sum(wk * dE * dB) / np.sum(wk * dE * dE)
        out.append(0.5 * np.degrees(np.arcsin(np.clip(r, -1, 1))))
    return np.array(out)


def alp_shape(m):
    """quadratic-regime ALP, theta from rest; returns beta(z) / beta_plateau-ish"""
    def rhs(N, y):
        H = F.hubble(N)
        dlnH = (F.hubble(N + 1e-5) - F.hubble(N - 1e-5)) / (2e-5 * H)
        return [y[1], -(3 + dlnH) * y[1] - (m / H) ** 2 * y[0]]
    s = solve_ivp(rhs, [np.log(1e-4), 0.0], [1.0, 0.0], method="DOP853",
                  rtol=1e-10, atol=1e-13, dense_output=True)
    thz = lambda z: s.sol(-np.log1p(np.asarray(z, float)))[0]
    return lambda z: thz(0.0) - thz(z)


def fit_amp(shape_curve, target):
    """least-squares amplitude for a linear-in-amplitude curve"""
    return np.dot(shape_curve, target) / np.dot(shape_curve, shape_curve)


masses = np.geomspace(3e-34, 3e-29, 61)
alp = {}
for m in masses:
    h = alp_shape(m)
    unit = beta_l(lambda z, h=h: 1e-3 * h(z)) / 1e-3      # linear response
    alp[m] = unit
print("STUR-ROLL vs best-fit ALP (free mass AND free amplitude), CLASS projection")
print("beta in millidegrees (1 mdeg = 0.001 deg)")
print("l:          " + "".join(f"{l:>6d}" for l in LS))
for ms in (1e-31, 3e-31, 1e-30):
    _, _, hist = F.roll(ms, 1e-4)
    st = beta_l(hist)
    best = None
    for m, u in alp.items():
        a = fit_amp(u, st)
        res = st - a * u
        rms = np.sqrt(np.mean(res ** 2))
        if best is None or rms < best[0]:
            best = (rms, m, a, a * u)
    print(f"m_STUR = {ms:.0e} eV")
    print("  STUR      " + "".join(f"{1e3 * v:6.1f}" for v in st))
    print("  ALP fit   " + "".join(f"{1e3 * v:6.1f}" for v in best[3]))
    print("  residual  " + "".join(f"{1e3 * v:+6.1f}" for v in st - best[3]))
    print(f"  best ALP mass {best[1]:.1e} eV; rms residual {best[0]:.4f} deg")
    d = st[0] - st[-1]
    print(f"  calibration-free difference beta(l=2) - beta(l=30): {d:+.4f} deg")
print("Miscalibration rotates every l by the same angle, so beta(l) - beta(30)")
print("is calibration-free; STUR fixes its size (plateau alpha/2), an ALP")
print("scales it with a free amplitude.")


EXPECTED_OUTPUT = r"""
STUR-ROLL vs best-fit ALP (free mass AND free amplitude), CLASS projection
beta in millidegrees (1 mdeg = 0.001 deg)
l:               2     3     4     5     6     8    10    12    15    20    30
m_STUR = 1e-31 eV
  STUR       124.4 163.2 185.0 196.5 202.0 206.7 205.7 204.1 202.5 201.7 201.9
  ALP fit    131.6 166.9 182.9 191.1 195.5 199.6 202.2 204.1 206.2 207.7 207.9
  residual    -7.3  -3.7  +2.1  +5.4  +6.5  +7.0  +3.5  +0.0  -3.7  -6.0  -6.0
  best ALP mass 1.1e-32 eV; rms residual 0.0051 deg
  calibration-free difference beta(l=2) - beta(l=30): -0.0775 deg
m_STUR = 3e-31 eV
  STUR        21.2  34.9  49.4  65.1  80.4  95.8 117.8 140.1 178.0 203.5 205.5
  ALP fit     28.7  43.0  57.7  72.3  85.5 104.3 123.8 144.0 173.9 195.0 196.2
  residual    -7.5  -8.2  -8.4  -7.3  -5.1  -8.5  -6.1  -3.9  +4.1  +8.6  +9.3
  best ALP mass 4.4e-32 eV; rms residual 0.0072 deg
  calibration-free difference beta(l=2) - beta(l=30): -0.1843 deg
m_STUR = 1e-30 eV
  STUR         0.0   0.9   2.3   5.1  10.9  34.5  52.4  88.2 150.7 202.9 207.5
  ALP fit      0.4   1.2   2.6   5.3  11.0  34.5  52.8  88.6 150.7 202.7 207.4
  residual    -0.4  -0.4  -0.3  -0.2  -0.0  +0.0  -0.4  -0.3  +0.0  +0.2  +0.1
  best ALP mass 3.6e-31 eV; rms residual 0.0003 deg
  calibration-free difference beta(l=2) - beta(l=30): -0.2074 deg
Miscalibration rotates every l by the same angle, so beta(l) - beta(30)
is calibration-free; STUR fixes its size (plateau alpha/2), an ALP
scales it with a free amplitude.
"""
