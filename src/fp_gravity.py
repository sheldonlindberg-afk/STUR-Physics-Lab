#!/usr/bin/env python3
"""
Fullness-phase theory (working name), part 1: the gravity law.

Postulates (the user's):
  P1  Density has a ceiling rho_max >= rho_Planck ("1"), beyond what can be measured.
      Fullness phi = rho / rho_max runs from 0 (empty) to 1 (full).
  P2  Gravity is teleparallel (TEGR: gravity = torsion of a tetrad field, torsion scalar T),
      modified so that the ceiling is respected: a new law f(T) in place of T.
  P3  Matter degrades with time itself (part 2, fp_degradation.py).
  P4  What is measured is the energy needed to phase-lock a probe to the system
      (part 3, fp_phase_lock.py).

The law.  Teleparallel f(T) gravity, flat FRW tetrad e^a_mu = diag(1, a, a, a), T = -6H^2,
gives the Friedmann equation (KNOWN, e.g. Bengochea & Ferraro 2009)
        12 H^2 f_T + f = 16 pi G rho .                                          (F)
Demand the "dance" form  H^2 = (8 pi G / 3) rho (1 - phi)  (zero expansion rate at both
0 and 1).  Solving (F) for f (sympy, done in this project) gives, with T_b = -4 pi G rho_max
and the inert sqrt(-T) homogeneous term fixed so f is smooth:

        phi = sin^2(u/2),   T = T_b sin^2 u = 4 T_b phi (1 - phi),
        f   = 2 T_b (u sin u + cos u - 1),     f_T = u / sin u,      u in [0, pi]   (FP)

  FOLLOWS: fullness is an ANGLE u; torsion (the gravitational field) is zero at empty and
  at full and maximal at half full: |T| <= 4 pi G rho_max.  In u the law is single-valued
  through phi = 1/2, where written in T alone it has two branches.
  LIT (recalled): the same Friedmann equation is the effective dynamics of loop quantum
  cosmology, where the same angle is a holonomy (rho = rho_c sin^2); an f(T) realisation
  of it is Amoros, de Haro & Odintsov 2013.  The postulates force this structure.

Consequences computed here:
  G1  checks: (F) holds identically; f -> T (TEGR = GR) at low fullness; f_T continuous.
  G2  a collapsing universe stops at phi = 1 exactly and re-expands (no singularity).
  G3  a collapsing star (Oppenheimer-Snyder dust ball with the same law inside) stops at
      a pure-matter core of radius R_b = (3M / 4 pi rho_max)^(1/3) -- far inside its horizon.
"""
import numpy as np
from scipy.integrate import solve_ivp, quad

G, c, hbar = 6.67430e-11, 2.99792458e8, 1.054571817e-34
M_SUN = 1.98892e30
RHO_P = c ** 5 / (hbar * G ** 2)
M_P = np.sqrt(hbar * c / G)
L_P = np.sqrt(hbar * G / c ** 3)


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


# ----------------------------------------------------------------- the law (FP)
def law(u, Tb=-1.0):
    """Parametric law: returns phi, T, f, f_T at angle u (units with T_b given)."""
    s = np.sin(u)
    phi = np.sin(u / 2) ** 2
    T = Tb * s * s
    f = 2 * Tb * (u * s + np.cos(u) - 1)
    fT = np.where(s > 1e-300, u / np.where(s == 0, 1, s), 1.0)
    return phi, T, f, fT


def friedmann_residual(u, Tb=-1.0):
    """12 H^2 f_T + f - 16 pi G rho with H^2 = -T/6 and 16 pi G rho = -4 T_b phi."""
    phi, T, f, fT = law(u, Tb)
    return (-2 * T * fT + f) - (-4 * Tb * phi)


# ----------------------------------------------------------------- G2 cosmology
def bounce(w=0.0, phi0=1e-4, t_end=None):
    """Units: rho_max = 1, 8 pi G / 3 = 1.  H^2 = rho (1 - rho);
    dH/dt = -(3/2)(1 + w) rho (1 - 2 rho);  d rho/dt = -3 H (1 + w) rho.  Start collapsing."""
    H0 = -np.sqrt(phi0 * (1 - phi0))

    def rhs(t, y):
        rho, H, lna = y
        return [-3 * H * (1 + w) * rho, -1.5 * (1 + w) * rho * (1 - 2 * rho), H]

    t_end = t_end or 2 * 2 / (3 * (1 + w) * abs(H0))
    sol = solve_ivp(rhs, [0, t_end], [phi0, H0, 0.0], rtol=1e-11, atol=1e-14,
                    dense_output=True, max_step=t_end / 4000)
    rho, H, lna = sol.y
    cons = np.max(np.abs(H ** 2 - rho * (1 - rho))) / phi0
    return sol.t, rho, H, lna, cons


# ----------------------------------------------------------------- G3 star cores
def core_radius(M, rho_max=RHO_P):
    return (3 * M / (4 * np.pi * rho_max)) ** (1 / 3)


def horizon_to_core_time(M, rho_max=RHO_P):
    """Proper time on the dust surface from R = r_s to the bounce, with
    (dR/dtau)^2 = (2GM/R)(1 - (R_b/R)^3)  (flat OS interior, same law)."""
    rs, Rb = 2 * G * M / c ** 2, core_radius(M, rho_max)
    # substitute R = Rb * y to keep the integrable 1/sqrt singularity tame
    g = lambda y: Rb / np.sqrt(2 * G * M / (Rb * y) * (1 - y ** -3))
    return quad(g, 1, rs / Rb, limit=500, points=[1.0001, 10])[0] if rs > Rb else np.nan


def no_horizon_mass(rho_max=RHO_P):
    """Mass below which the full core is bigger than its own Schwarzschild radius."""
    return np.sqrt(3 * c ** 6 / (32 * np.pi * G ** 3 * rho_max))


# ----------------------------------------------------------------- main
def main():
    banner("G1  The law and its checks")
    u = np.linspace(1e-6, np.pi - 1e-6, 20001)
    res = np.max(np.abs(friedmann_residual(u)))
    print(f"   Friedmann (F) residual over u in (0, pi): {res:.1e}")
    us = np.array([1e-3, 1e-2, 0.1])
    phi, T, f, fT = law(us)
    for ui, p, Ti, fi in zip(us, phi, T, f):
        print(f"   phi = {p:.2e}:  f/T = {fi/Ti:.10f}   (TEGR = GR limit is 1; FOLLOWS:"
              f" 1 + phi/3 + ...)")
    e = 1e-7
    _, _, _, fl = law(np.pi / 2 - e)
    _, _, _, fr = law(np.pi / 2 + e)
    print(f"   f_T just below / above half-full: {fl:.8f} / {fr:.8f}  (pi/2 = {np.pi/2:.8f})")
    print("   torsion T = 4 T_b phi (1 - phi): zero at empty AND full, max |T| = 4 pi G rho_max"
          " at phi = 1/2")
    print(f"   with rho_max = rho_Planck: max |T| = {4*np.pi*G*RHO_P:.3e} s^-2"
          f" = 4 pi / t_P^2")

    banner("G2  A collapsing universe: stops at full, re-expands")
    out = {"res": res}
    for w, lab in [(0.0, "dust"), (1 / 3, "radiation")]:
        t, rho, H, lna, cons = bounce(w)
        i = np.argmax(rho)
        print(f"   {lab:9s}: max fullness = {rho[i]:.9f}  (H there = {H[i]:+.1e});"
              f"  a_min/a_start = {np.exp(lna[i]):.4e};  ends expanding: {H[-1] > 0};"
              f"  constraint drift {cons:.1e}")
        out[lab] = rho[i]
    a_th = 1e-4 ** (1 / 3)
    print(f"   CHECK dust: a_min/a_start = (phi0)^(1/3) = {a_th:.4e}")

    banner("G3  Collapsing stars: a pure-matter core inside the horizon")
    print("   object          M (kg)       r_s (m)      core R_b (m)   R_b/r_s     "
          "horizon->core (s)")
    rows = []
    for lab, m in [("1 solar mass", 1), ("Sgr A*", 4.3e6), ("M87*", 6.5e9)]:
        M = m * M_SUN
        rs, Rb, tau = 2 * G * M / c ** 2, core_radius(M), horizon_to_core_time(M)
        rows.append((lab, M, rs, Rb, tau))
        print(f"   {lab:14s} {M:.3e}   {rs:.3e}    {Rb:.3e}      {Rb/rs:.1e}    {tau:.3e}"
              f"   (2 r_s / 3c = {2*rs/(3*c):.3e})")
    Mn = no_horizon_mass()
    print(f"   Only masses below {Mn:.2e} kg = {Mn/M_P:.3f} m_P ({Mn*1e9:.1f} micrograms) have")
    print("   a full core bigger than their horizon.  rho_max above rho_P lowers this further.")
    print("   FOLLOWS: for every astrophysical black hole the horizon forms at LOW fullness")
    print("   (M87*: about 0.4 kg/m^3), so no density ceiling can remove the horizon.  What the")
    print("   law removes is the singularity: the inside is pure matter at phi = 1.  After the")
    print("   bounce the core re-expands (a white-hole phase inside).  What the outside sees")
    print("   needs the static spherical solution of (FP): OPEN.")
    out.update(rows=rows, Mn=Mn)
    return out


if __name__ == "__main__":
    main()
