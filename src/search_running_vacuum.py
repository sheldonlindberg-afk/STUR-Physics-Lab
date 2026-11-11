#!/usr/bin/env python3
"""
Unifying-equation search, front 2: running vacuum - the bridge from our own unified equation.

R1 (FOLLOWS from U3, stur_unification.py): the horizon tension runs with the number of
   species, 1/(4G(mu)) = 1/(4G0) + c N mu^2  (c = 0.02424 per real scalar, Planck units).
   Evaluated at the cosmic scale mu = H (hbar = c = 1):  delta G / G = 4 c N (H / M_P)^2.

R2 (KNOWN family: running vacuum models, Shapiro & Sola; vacuum exchanges energy with matter):
       rho_vac(H) = rho_0 + (3 nu / 8 pi) M_P^2 (H^2 - H0^2)
   with the standard exact solution for flat matter + vacuum (G constant):
       rho_m(a)   = rho_m0 a^{-3(1-nu)}
       rho_vac(a) = rho_vac0 + nu/(1-nu) rho_m0 (a^{-3(1-nu)} - 1)
   An observer who assumes conserved matter (rho_m0 a^-3) infers
       rho_de,eff(a) = rho_m(a) + rho_vac(a) - rho_m0 a^-3,
       w_eff = -1 - (1/3) d ln rho_de,eff / d ln a,
   projected on CPL w0 + wa (1 - a) over 0.5 <= a <= 1, compared with DESI DR2 (LIT).
"""
import numpy as np

hbar, c, G = 1.054571817e-34, 2.99792458e8, 6.67430e-11
EP = np.sqrt(hbar * c**5 / G)                               # J
H0 = 67.4e3 / 3.0857e22


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


def rvm_weff(nu, Om0=0.31, a_lo=0.5):
    a = np.linspace(0.3, 1.0, 2001)
    rm = Om0 * a ** (-3 * (1 - nu))
    rv = (1 - Om0) + nu / (1 - nu) * Om0 * (a ** (-3 * (1 - nu)) - 1)
    rde = rm + rv - Om0 * a**-3
    with np.errstate(invalid="ignore", divide="ignore"):
        w = -1 - np.gradient(np.log(np.where(rde > 0, rde, np.nan)), np.log(a)) / 3
    s = a >= a_lo
    s = s & np.isfinite(w)
    w0, wa = np.linalg.lstsq(np.c_[np.ones(s.sum()), 1 - a[s]], w[s], rcond=None)[0]
    return a, w, rde, w0, wa


def main():
    banner("R1  Our species running evaluated at mu = H")
    HP = hbar * H0 / EP                                     # H0 in Planck units
    for N in [1, 100, 1e4]:
        print(f"   N = {N:8.0f}:  delta G/G = 4 c N (H0/M_P)^2 = {4*0.02424*N*HP**2:.1e}")
    print(f"   (H0/M_P)^2 = {HP**2:.1e}.  -> no cosmological effect: the bridge from our equation")
    print("      to dark energy is suppressed by ~1e-122. Running vacuum needs a DIFFERENT source")
    print("      (heavy-field contributions, nu ~ sum M_i^2 / M_P^2 in Sola's QFT derivation, LIT).")

    banner("R2  Running vacuum: effective w0, wa seen by a conserved-matter analysis")
    print("    nu        w0_eff    wa_eff   crosses -1?   rho_de,eff > 0 on 0.3<a<1?")
    rows = []
    for nu in [-0.03, -0.01, -0.003, -0.001, 0.0, 0.001, 0.003, 0.01, 0.03]:
        a, w, rde, w0, wa = rvm_weff(nu)
        good = np.isfinite(w)
        dev = w[good] + 1
        dev = dev[abs(dev) > 1e-6]                       # ignore round-off around w = -1
        cross = bool(np.all(rde > 0) and np.any(np.diff(np.sign(dev)) != 0))
        rows.append((nu, w0, wa))
        print(f"   {nu:+7.3f}   {w0:8.4f}  {wa:8.4f}   {str(bool(cross)):10s}   {bool(np.all(rde > 0))}")
    print("\n   DESI DR2+CMB+SNe (LIT): DESY5 w0 = -0.752 +- 0.057, wa = -0.86; Union3 w0 = -0.667, wa = -1.09")
    # what nu would reproduce w0 = -0.75?
    nus = np.linspace(-0.2, 0.2, 401)
    w0s = np.array([rvm_weff(n)[3] for n in nus])
    i = np.argmin(abs(w0s + 0.752))
    print(f"   nu needed for w0_eff = -0.752: {nus[i]:+.3f}  (then wa_eff = {rvm_weff(nus[i])[4]:+.3f})")

    banner("R3  Early-universe check: matter density at recombination")
    print("   rho_m(a) / [rho_m0 a^-3] = a^(3 nu).  Planck 2018 (LIT): Omega_c h^2 = 0.120 +- 0.001 (~1%).")
    ar = 1 / 1100
    for nu in [nus[i], 0.03, 0.01, 1e-3]:
        print(f"   nu = {nu:+.4f}:  matter density at z = 1100 shifted by factor {ar**(3*nu):.3f}")
    nu_max = 0.01 / (3 * np.log(1100))
    _, _, _, w0m, wam = rvm_weff(nu_max)
    print(f"   1% criterion -> |nu| <~ {nu_max:.1e}  ->  w0_eff = {w0m:.4f}, wa_eff = {wam:.4f}")
    print("   -> the running vacuum sits in DESI's quadrant only with nu too large for the CMB by")
    print(f"      a factor {nus[i]/nu_max:.0f}; at the CMB-allowed nu its signal is ~{abs(w0m+1)/0.25*100:.1f}% of DESI's.")
    return rows


if __name__ == "__main__":
    main()
