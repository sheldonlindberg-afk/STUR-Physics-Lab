#!/usr/bin/env python3
"""
The cheapest experiment that decides STUR's original corollary P2: one trapped ion.

Setup (KNOWN technique: spin-dependent kicks on a trapped ion, as in trapped-ion
"Schrodinger cat" experiments, LIT recalled: Monroe et al., Science 272, 1131 (1996)):
  - one motional mode of frequency omega, prepared thermal with mean phonon number nbar
    (temperature T: nbar = 1/(exp(x) - 1), x = hbar omega / k_B T);
  - a spin superposition (|up> + |down>)/sqrt2, then a spin-dependent kick that displaces
    the motion by +alpha for |up> and -alpha for |down>;
  - Ramsey contrast of the spin gives the visibility V; sideband spectroscopy before and
    after gives the phonon-number change dN (a two-point measurement).

Predictions, at FIXED mean energy deposited <dE> = hbar omega |alpha|^2 (per branch):
  Standard quantum mechanics (FOLLOWS; checked here in Fock space):
      Gamma = -ln V = 2 |alpha|^2 (2 nbar + 1) = 2 (<dE>/hbar omega) coth(x/2)
      Gamma = 2 Var(dN)                                  (the identity of ASSUMPTIONS.md 2)
  STUR corollary P2 (E = k_B T Gamma):
      Gamma = <dE> / k_B T = (<dE>/hbar omega) x

  The two have OPPOSITE temperature dependence at fixed <dE>:
      d ln Gamma / d ln T  =  x / sinh(x)  in [0, 1]   (standard: hotter loses MORE)
                           =  -1                        (P2: colder loses more)
  They cross only at x = 2.3994 (the coincidence line of ASSUMPTIONS.md 3).
  So two runs, at nbar = 0.1 and nbar = 5 with the same kick, settle the sign.
"""
import numpy as np
from scipy.linalg import expm
from scipy.optimize import brentq

NMAX = 160


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


def displacement(alpha, nmax=NMAX):
    a = np.diag(np.sqrt(np.arange(1, nmax)), 1)
    return expm(alpha * a.conj().T - np.conj(alpha) * a)


def thermal_weights(nbar, nmax=NMAX):
    n = np.arange(nmax)
    if nbar == 0:
        p = (n == 0).astype(float)
    else:
        q = nbar / (nbar + 1)
        p = (1 - q) * q ** n
    return p / p.sum()


def fock_space(alpha, nbar, nmax=NMAX):
    """Exact V, <dN>, Var(dN) for a thermal mode kicked by +alpha / -alpha."""
    p = thermal_weights(nbar, nmax)
    Dp, Dm = displacement(alpha, nmax), displacement(-alpha, nmax)
    # Visibility: |sum_n p_n <n| D(-alpha)^dag D(alpha) |n>|
    overlap = Dm.conj().T @ Dp
    V = abs(np.sum(p * np.diag(overlap)))
    # Two-point measurement on one branch: P(n -> m) = |<m|D(alpha)|n>|^2
    T = np.abs(Dp) ** 2                      # T[m, n]
    n = np.arange(nmax)
    dN = n[:, None] - n[None, :]
    w = T * p[None, :]
    mean = np.sum(w * dN)
    var = np.sum(w * dN ** 2) - mean ** 2
    return V, mean, var


def gamma_standard(dN, x):
    return 2 * dN / np.tanh(x / 2)


def gamma_P2(dN, x):
    return dN * x


def slope_standard(x):
    return x / np.sinh(x)


def main():
    banner("L1  Exact Fock-space check of the standard prediction (FOLLOWS)")
    print("   nbar   |alpha|^2  -lnV (Fock)  2|a|^2(2nbar+1)  2Var(dN)   <dN>")
    worst = 0.0
    for nbar in (0.0, 0.1, 1.0, 5.0):
        for a2 in (0.02, 0.1, 0.5):
            V, m, v = fock_space(np.sqrt(a2), nbar)
            g = -np.log(V)
            ana = 2 * a2 * (2 * nbar + 1)
            worst = max(worst, abs(g / ana - 1), abs(2 * v / g - 1), abs(m / a2 - 1))
            print(f"   {nbar:4.1f}   {a2:6.2f}    {g:10.6f}   {ana:12.6f}   {2*v:10.6f}  {m:7.4f}")
    print(f"   largest relative deviation: {worst:.1e}")
    print("   So -ln V = 2 Var(dN) = 2 <dN> (2 nbar + 1): visibility loss counts the spread")
    print("   of quanta exchanged, and grows with temperature at fixed energy deposited.")

    banner("L2  Standard QM vs STUR P2 at fixed energy deposited, <dN> = |alpha|^2 = 0.1")
    print("   nbar    k_BT/hbar.omega   V standard   V under P2   ratio Gamma_std/Gamma_P2")
    a2 = 0.1
    for nbar in (0.05, 0.1, 0.5, 1.0, 2.0, 5.0, 10.0):
        x = np.log(1 + 1 / nbar)
        gs, gp = gamma_standard(a2, x), gamma_P2(a2, x)
        print(f"   {nbar:5.2f}   {1/x:10.3f}        {np.exp(-gs):.4f}       {np.exp(-gp):.4f}"
              f"       {gs/gp:8.3f}")
    xc = brentq(lambda x: 2 / np.tanh(x / 2) - x, 0.5, 5)
    print(f"   Crossing (the only place they agree): hbar omega = {xc:.4f} k_B T"
          f"  (nbar = {1/np.expm1(xc):.3f})")

    banner("L3  The discriminator: sign of d ln Gamma / d ln T at fixed <dE>")
    for nbar in (0.05, 0.5, 5.0):
        x = np.log(1 + 1 / nbar)
        print(f"   nbar = {nbar:4.2f}:  standard {slope_standard(x):+.3f}   P2 -1.000")
    g1 = gamma_standard(a2, np.log(1 + 1 / 0.1))
    g2 = gamma_standard(a2, np.log(1 + 1 / 5.0))
    p1 = gamma_P2(a2, np.log(1 + 1 / 0.1))
    p2 = gamma_P2(a2, np.log(1 + 1 / 5.0))
    print(f"   Two runs, nbar 0.1 -> 5, same kick |alpha|^2 = 0.1:")
    print(f"     standard: -lnV {g1:.3f} -> {g2:.3f}  (x{g2/g1:.2f}, contrast {np.exp(-g1):.3f} -> {np.exp(-g2):.3f})")
    print(f"     P2:       -lnV {p1:.3f} -> {p2:.3f}  (x{p2/p1:.3f}, contrast {np.exp(-p1):.3f} -> {np.exp(-p2):.3f})")
    print("   nbar = 0.1 sits on the crossing, so both start from the same contrast. At nbar = 5")
    print(f"   they differ by {np.exp(-p2) - np.exp(-g2):.2f} in contrast, far above Ramsey-contrast errors")
    print("   of a few per cent. Standard QM fixes the outcome in")
    print("   advance, so this is a kill test for P2, not a test that could favour STUR.")


if __name__ == "__main__":
    main()
