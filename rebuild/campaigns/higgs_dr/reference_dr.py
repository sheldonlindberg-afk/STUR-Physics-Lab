"""Orchestrator's independent reference for the Higgs-dependent part of Delta r (Feynman gauge, xi = 1). Hidden: never exported.

Self-energy (g^{mu nu} coefficient, M^2_eff(q^2) = M^2 + Pi(q^2)), Higgs-containing diagrams, MS-bar, in the structure found at q^2 = 0 by the accepted
higgs_rho campaign:  16 pi^2 Pi_V(q^2) = kappa^2 [ -M^2 B0(q^2; m_H, M) + B00(q^2; m_H, M) - A0(m_H)/4 ],  kappa_W = g, kappa_Z = g/c.
The B functions are the Feynman-parameter integrals (x on the Higgs line, no Passarino-Veltman reduction):
  Delta(x) = (1 - x) M^2 + x m_H^2 - x (1 - x) q^2,   B0 = -int ln(Delta/mu^2),   B00 = (1/2) int Delta [1 - ln(Delta/mu^2)],  A0(m) = m^2 (1 - ln(m^2/mu^2)).
Delta r (Higgs part), derived from muon decay in the on-shell scheme (see SPEC.md):
  Delta r_H = -[Pi_W(0) - Pi_W(MW^2)]/MW^2 - (c^2/s^2) [Pi_W(MW^2)/MW^2 - Pi_Z(MZ^2)/MZ^2].
"""
import mpmath as mp

import functools

DPS = 40          # working precision, applied locally to every public function: this module never changes the global mpmath precision


def _pts():
    return [mp.mpf(0)] + [mp.mpf(10) ** (-k) for k in range(44, 0, -1)] + [mp.mpf(1) / 2, mp.mpf(1)]   # x ~ M^2/m_H^2 can be tiny: resolve the scales


def _local(fn):
    @functools.wraps(fn)
    def w(*a, **k):
        with mp.workdps(DPS):
            return fn(*a, **k)
    return w


def _A0(m2, mu2):
    return m2 * (1 - mp.log(m2 / mu2))


def _B0(q2, M2, mh2, mu2):
    return -mp.quad(lambda x: mp.log(((1 - x) * M2 + x * mh2 - x * (1 - x) * q2) / mu2), _pts())


def _B00(q2, M2, mh2, mu2):
    return mp.quad(lambda x: (((1 - x) * M2 + x * mh2 - x * (1 - x) * q2) / 2) * (1 - mp.log(((1 - x) * M2 + x * mh2 - x * (1 - x) * q2) / mu2)), _pts())


@_local
def pi_v(q2, mh, M, kappa2, mu):
    """Pi_V(q^2) in units where the overall 1/16 pi^2 is included."""
    mh2, M2, mu2 = mp.mpf(mh) ** 2, mp.mpf(M) ** 2, mp.mpf(mu) ** 2
    q2 = mp.mpf(q2)
    return kappa2 / (16 * mp.pi**2) * (-M2 * _B0(q2, M2, mh2, mu2) + _B00(q2, M2, mh2, mu2) - _A0(mh2, mu2) / 4)


@_local
def couplings(MW, MZ, alpha):
    c2 = (mp.mpf(MW) / MZ) ** 2
    s2 = 1 - c2
    g2 = 4 * mp.pi * alpha / s2
    return g2, c2, s2


@_local
def drho(mh, MW, MZ, alpha, mu):
    mh, MW, MZ, alpha, mu = (mp.mpf(t) for t in (mh, MW, MZ, alpha, mu))
    g2, c2, s2 = couplings(MW, MZ, alpha)
    return pi_v(0, mh, MW, g2, mu) / MW**2 - pi_v(0, mh, MZ, g2 / c2, mu) / MZ**2


@_local
def dr_h(mh, MW, MZ, alpha, mu):
    mh, MW, MZ, alpha, mu = (mp.mpf(t) for t in (mh, MW, MZ, alpha, mu))
    g2, c2, s2 = couplings(MW, MZ, alpha)
    pw0, pwm = pi_v(0, mh, MW, g2, mu), pi_v(MW**2, mh, MW, g2, mu)
    pzm = pi_v(MZ**2, mh, MZ, g2 / c2, mu)
    return -(pw0 - pwm) / MW**2 - (c2 / s2) * (pwm / MW**2 - pzm / MZ**2)


@_local
def dr_h_rel(mh, MW, MZ, alpha, mu):
    return dr_h(mh, MW, MZ, alpha, mu) - dr_h(MW, MW, MZ, alpha, mu)


@_local
def drho_rel(mh, MW, MZ, alpha, mu):
    return drho(mh, MW, MZ, alpha, mu) - drho(MW, MW, MZ, alpha, mu)
