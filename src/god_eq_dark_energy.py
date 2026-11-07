#!/usr/bin/env python3
"""
God-equation search, front 1: dark energy from holography (STUR's founding axiom).

KNOWN model (Li 2004, holographic dark energy, future event horizon L as IR cutoff):
    rho_de = 3 c^2 M_P^2 / L^2
Flat universe, matter + dark energy (radiation negligible at z < 3), x = ln a:
    dOmega/dx = Omega (1 - Omega) (1 + (2/c) sqrt(Omega))
    w(Omega)  = -1/3 - (2 / (3c)) sqrt(Omega)
One free parameter c.  Project onto the CPL form w = w0 + wa (1 - a) by least squares
over 0.5 <= a <= 1 (the range BAO/SNe constrain best) and compare with DESI DR2.

DESI DR2 + CMB + SNe (LIT, DESI DR2 Results II, arXiv 2503.14738):
    DESY5 : w0 = -0.752 +- 0.057, wa = -0.86
    Union3: w0 = -0.667 +- 0.088, wa = -1.09
sigma(wa) and the w0-wa correlation were NOT retrieved; sigma(wa) = 0.25 is an ASSUMPTION
and only the sign/size of wa is used for the verdict.
"""
import numpy as np
from scipy.integrate import solve_ivp


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


def hde_w_of_a(c, Om_de0=0.69, a_min=0.3):
    rhs = lambda x, O: O * (1 - O) * (1 + 2 / c * np.sqrt(np.clip(O, 0, 1)))
    sol = solve_ivp(rhs, [0, np.log(a_min)], [Om_de0], dense_output=True, rtol=1e-10, atol=1e-12)
    a = np.linspace(a_min, 1, 400)
    O = sol.sol(np.log(a))[0]
    return a, -1 / 3 - 2 / (3 * c) * np.sqrt(O)


def cpl_fit(a, w, a_lo=0.5):
    s = a >= a_lo
    X = np.c_[np.ones(s.sum()), 1 - a[s]]
    w0, wa = np.linalg.lstsq(X, w[s], rcond=None)[0]
    return w0, wa


def main():
    banner("D1  Holographic dark energy (event horizon) vs DESI DR2")
    print("   c       w(z=0)    CPL w0    CPL wa    w(z=2)   wa - wa_DESY5 (in sigma=0.25, assumed)")
    rows = []
    for c in [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.2, 1.5, 2.0]:
        a, w = hde_w_of_a(c)
        w0, wa = cpl_fit(a, w)
        wz2 = np.interp(1 / 3, a, w)
        rows.append((c, w0, wa))
        print(f"   {c:4.1f}   {w[-1]:8.3f}  {w0:8.3f}  {wa:8.3f}  {wz2:8.3f}   {(wa + 0.86)/0.25:+6.1f}")
    print("\n   DESY5:  w0 = -0.752 +- 0.057,  wa = -0.86;   Union3: w0 = -0.667, wa = -1.09")
    print("   Sign check (exact, FOLLOWS): dw/d ln a = -(1/3c) sqrt(Om)(1-Om)(1+2 sqrt(Om)/c) < 0")
    print("   for every c > 0, so w DECREASES with time: CPL wa > 0 always. DESI prefers wa < 0.")
    print("   Also w -> -1/3 in the past (HDE), while DESI's fit implies w0 + wa ~ -1.6 to -1.8")
    print("   in the past (phantom). The holographic model crosses -1 in the OPPOSITE direction.")
    return rows


if __name__ == "__main__":
    main()
