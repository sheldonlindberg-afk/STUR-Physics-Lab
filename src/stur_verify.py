"""
STUR Resistance Equation -- numerical verification
Every number quoted in the derivation record is produced here.

Run:  python3 stur_verify.py
Needs: numpy, scipy
"""
import numpy as np
from scipy.optimize import minimize

print("=" * 70)
print("CHECK 1  Smarr relation from E_R = 1/2 kB T Phi^2 at the holographic ceiling")
print("=" * 70)
# SI constants (CODATA 2018)
G_, c_, hbar_, kB_ = 6.67430e-11, 2.99792458e8, 1.054571817e-34, 1.380649e-23
Msun_ = 1.98847e30
for m in [1e-3 * Msun_, Msun_, 4e6 * Msun_, 1e11 * Msun_]:
    rs = 2 * G_ * m / c_**2
    A = 4 * np.pi * rs**2
    lP2 = hbar_ * G_ / c_**3
    Phi2_max = A / (2 * lP2)                    # ceiling: Phi^2 <= A / (2 lP^2)
    S_R = 0.5 * kB_ * Phi2_max                  # postulate: S_R = 1/2 kB Phi^2
    S_BH = kB_ * A / (4 * lP2)                  # Bekenstein-Hawking entropy
    T_H = hbar_ * c_**3 / (8 * np.pi * G_ * m * kB_)
    E_R = 0.5 * kB_ * T_H * Phi2_max
    print(f"M = {m/Msun_:8.1e} Msun   S_R/S_BH = {S_R/S_BH:.12f}   "
          f"Phi_max^2 = {Phi2_max:.2e}   E_R/(Mc^2) = {E_R/(m*c_**2):.12f}")
print("Analytic: E_R = T_H * S_BH = Mc^2/2 for every M (Smarr: Mc^2 = 2 T S)")

print()
print("=" * 70)
print("CHECK 2  Gaussian phase noise:  <exp(i phi)> = exp(-sigma^2/2)")
print("=" * 70)
rng = np.random.default_rng(1)
for sigma in [0.5, 1.0, 1.5, 2.0]:
    phi = rng.normal(0, sigma, 2_000_000)
    mc = np.abs(np.mean(np.exp(1j * phi)))
    print(f"sigma={sigma:3.1f}  Monte Carlo V={mc:.4f}   exp(-s^2/2)={np.exp(-sigma**2/2):.4f}")
# Fixed phase: fringes shift, visibility stays 1
print("fixed phase 1.0 rad -> |<e^{i phi}>| =", abs(np.exp(1j * 1.0)), "(no loss of visibility)")

print()
print("=" * 70)
print("CHECK 3  Area-law tensions: QCD vs Planck")
print("=" * 70)
hbar_c_GeV_fm = 0.1973269804
sqrt_sigma_QCD = 0.44                       # GeV  (lattice ~0.42-0.44)
L_QCD = hbar_c_GeV_fm / sqrt_sigma_QCD * 1e-15  # m
sigma_QCD = 1 / L_QCD**2                    # m^-2
lP = 1.616255e-35
sigma_Pl = 1 / (4 * lP**2)
print(f"sigma_QCD   = (0.44 GeV)^2 = {sigma_QCD:.3e} m^-2  ({sqrt_sigma_QCD**2/hbar_c_GeV_fm:.2f} GeV/fm)")
print(f"sigma_Planck= 1/(4 lP^2)   = {sigma_Pl:.3e} m^-2")
print(f"ratio                       = {sigma_Pl/sigma_QCD:.2e}")

print()
print("=" * 70)
print("CHECK 4  Hawking evaporation times  t = 5120 pi G^2 M^3 / (hbar c^4)")
print("=" * 70)
Gn, cn, hb = 6.67430e-11, 2.99792458e8, 1.054571817e-34
Msun, yr = 1.98847e30, 3.15576e7
def t_evap(m):
    return 5120 * np.pi * Gn**2 * m**3 / (hb * cn**4) / yr
for label, m in [("1 solar mass", Msun), ("Sgr A* 4e6 Msun", 4e6 * Msun),
                 ("1e11 Msun (largest)", 1e11 * Msun),
                 ("observable-universe mass 1.5e53 kg", 1.5e53)]:
    print(f"{label:38s} {t_evap(m):.1e} yr")

print()
print("=" * 70)
print("CHECK 5  Resistance to collapse: Skyrme model (Derrick scaling)")
print("=" * 70)
# Energy in Skyrme units, rational-map ansatz (B=1 is the exact hedgehog):
# E = 4 pi Int [ r^2 f'^2 + 2B sin^2 f (f'^2 + 1) + I sin^4 f / r^2 ] dr
# E2 (collapse-driving) = 4pi Int [ r^2 f'^2 + 2B sin^2 f ]
# E4 (resisting term)   = 4pi Int [ 2B sin^2 f f'^2 + I sin^4 f / r^2 ]
N, R = 1200, 12.0
r = np.linspace(R / N, R, N)
dr = r[1] - r[0]

def parts(f, B, I):
    fp = np.gradient(f, dr)
    s2 = np.sin(f) ** 2
    e2 = 4 * np.pi * np.sum(r**2 * fp**2 + 2 * B * s2) * dr
    e4 = 4 * np.pi * np.sum(2 * B * s2 * fp**2 + I * s2**2 / r**2) * dr
    return e2, e4

def energy(p, B, I):
    f = 2 * np.arctan((abs(p[0]) / r) ** abs(p[1]))   # trial profile, f(0)=pi, f(inf)=0
    e2, e4 = parts(f, B, I)
    return e2 + e4

def relax(B, I, n=4000, Rmax=20.0):
    """Minimise the discretised radial energy with an analytic gradient."""
    h = Rmax / n
    grid = np.linspace(0.0, Rmax, n + 1)
    rm = 0.5 * (grid[1:] + grid[:-1])          # segment midpoints
    def E_and_grad(inner):
        g = np.concatenate([[np.pi], inner, [0.0]])
        fp = np.diff(g) / h
        gm = 0.5 * (g[1:] + g[:-1])
        s2 = np.sin(gm) ** 2
        s2g = np.sin(2 * gm)
        dens = rm**2 * fp**2 + 2 * B * s2 * (fp**2 + 1) + I * s2**2 / rm**2
        dfp = 2 * rm**2 * fp + 4 * B * s2 * fp
        dgm = 2 * B * s2g * (fp**2 + 1) + 2 * I * s2 * s2g / rm**2
        E = 4 * np.pi * h * dens.sum()
        # node j (1..n-1) touches segment j-1 (as right end) and segment j (as left end)
        gr = 4 * np.pi * h * (dfp[:-1] / h + 0.5 * dgm[:-1] - dfp[1:] / h + 0.5 * dgm[1:])
        return E, gr
    x0 = 2 * np.arctan((1.0 / np.maximum(grid[1:-1], 1e-9)) ** 2)
    out = minimize(E_and_grad, x0, jac=True, method="L-BFGS-B",
                   options={"maxiter": 50000, "gtol": 1e-10, "ftol": 1e-14})
    g = np.concatenate([[np.pi], out.x, [0.0]])
    fp = np.diff(g) / h
    s2 = np.sin(0.5 * (g[1:] + g[:-1])) ** 2
    e2 = 4 * np.pi * h * np.sum(rm**2 * fp**2 + 2 * B * s2)
    e4 = 4 * np.pi * h * np.sum(2 * B * s2 * fp**2 + I * s2**2 / rm**2)
    return out.fun, e2, e4

bound = 12 * np.pi**2
E1, e2, e4 = relax(1, 1.0)
E2, _, _ = relax(2, 5.81)          # I_2 = 5.81 (Houghton-Manton-Sutcliffe 1998)
print(f"B=1  E = {E1:8.2f}   E/(12 pi^2 B) = {E1/bound:.4f}   (literature 1.232)")
print(f"B=2  E = {E2:8.2f}   E/(12 pi^2 B) = {E2/(2*bound):.4f}   (rational map, literature 1.208)")
print(f"binding of two B=1 lumps: 2*E1 - E2 = {2*E1-E2:.2f}  ({(2*E1-E2)/(2*E1)*100:.1f}% of 2*E1)")

# Derrick scaling curve for the relaxed B=1 solution: x -> lambda x gives E2 -> lambda E2, E4 -> E4/lambda
print(f"\nDerrick split at minimum: E2 = {e2:.2f}, E4 = {e4:.2f}  (virial theorem: E2 = E4)")
print("lambda   E(with resistance)   E(no resistance term)")
lams = [0.25, 0.4, 0.6, 0.8, 1.0, 1.25, 1.6, 2.0, 2.5, 3.0]
for lam in lams:
    print(f"{lam:5.2f}   {lam*e2 + e4/lam:10.1f}          {lam*e2:10.1f}")
