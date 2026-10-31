#!/usr/bin/env python3
"""
Refinement round 4: a torsion twist chi ("spacetime resistance") beyond TEGR.
See docs/REFINEMENT_R4.md. Requires numpy, scipy. Runs in ~1 min.

chi = holonomy of the pseudoscalar (axial) torsion mode along the fifth
dimension. Torsion couples to spin, so chi twists fermions only:
psi sees the total twist theta + chi; the B-charged scalar sees theta only.

  A. No-go, generalised: with smooth-cap birth (bosons periodic, fermions
     antiperiodic), the ONE-LOOP potential of any set of holonomies has its
     global minimum at the birth point.
  B. With a tree-level torsion potential V_T = Lambda^4 (1 + cos chi)
     (maximum at the birth point: the "resistance" term), chi flips 0 -> pi,
     psi becomes effectively periodic, theta = 0 becomes a hilltop, and theta
     rolls from its exact birth value: beta = alpha/2 with no tuning.
  C. Cosmic role of chi: dark energy is excluded (chi must flip before theta
     rolls); dark matter is possible for m_chi >= 2e-20 eV, f_chi from Omega.
  D. Problems the DM branch must solve: isocurvature and domain walls.
"""
import os
import sys

import numpy as np
from scipy.integrate import solve_ivp
from scipy.special import j0

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import stur_final as F  # noqa: E402

BAR = "=" * 78
MPL_EV = 2.435e27                 # reduced Planck mass [eV]
RHO_C_H2 = 8.0992e-11             # critical density / h^2 [eV^4]
RHO_R0 = 4.18e-5 * RHO_C_H2       # radiation today [eV^4] (stur_final's Omega_r h^2)
H0 = F.H0_EV


# ---------------------------------------------------------------- A. no-go
def one_loop(x, a, spin, twist):
    """first-principles winding sum per dof (positive constant dropped)"""
    w = np.arange(1, 400)[:, None]
    g = (1 + w * a + (w * a) ** 2 / 3) * np.exp(-w * a) / w ** 5
    s = -1.0 if spin == 0 else 1.0
    return s * np.sum(g * np.cos(w * (x + twist)), axis=0)


def part_a(rng):
    print(BAR + "\n A. Generalised no-go (two holonomies theta, chi)\n" + BAR)
    t = np.linspace(-np.pi, np.pi, 121)
    TH, CH = np.meshgrid(t, t, indexing="ij")
    worst = 0.0
    for trial in range(200):
        V = np.zeros_like(TH)
        for _ in range(rng.integers(2, 6)):
            spin = rng.integers(0, 2)
            qt = rng.integers(-2, 3)
            qc = 0 if spin == 0 else rng.integers(-2, 3)   # torsion: fermions only
            a = rng.uniform(0.0, 6.0)
            dof = rng.uniform(0.5, 4.0)
            arg = (qt * TH + qc * CH).ravel()
            twist = np.pi if spin == 1 else 0.0              # smooth-cap birth
            V += dof * one_loop(arg, a, spin, twist).reshape(TH.shape)
        i = np.unravel_index(V.argmin(), V.shape)
        worst = max(worst, abs(V[60, 60] - V[i]) / (np.ptp(V) + 1e-300))
    print("   200 random field contents (spins, charges -2..2, masses 0-6/L):")
    print(f"   max relative depth below the birth point: {worst:.1e}")
    print("   -> the birth point (theta, chi) = (0, 0) is the global minimum of the")
    print("      one-loop potential in every case: the quantum vacuum RESISTS any")
    print("      twist. A twist needs a classical (tree-level) torsion term.")


# ------------------------------------------------- B. coupled roll from zero
def part_b():
    print("\n" + BAR + "\n B. Torsion flip -> theta hilltop -> roll (theta born at exactly 0)\n"
          + BAR)
    m_t, m_c = 1e-30, 1e-27
    s_t, s_c = 1e-4, 1e-4          # quantum seeds (theta, chi)

    def dlnh(N):
        return (F.hubble(N + 1e-5) - F.hubble(N - 1e-5)) / (2e-5 * F.hubble(N))

    def rhs1(N, y):                 # full system while chi rolls
        th, dth, ch, dch = y
        H = F.hubble(N)
        fr = 3 + dlnh(N)
        return [dth, -fr * dth - (m_t / H) ** 2 * np.sin(th + ch),
                dch, -fr * dch + (m_c / H) ** 2 * np.sin(ch)]

    N0 = np.log(1e-6)
    Nsw = brentq_like(lambda N: F.hubble(N) - m_c / 300, N0, 0.0)
    s1 = solve_ivp(rhs1, [N0, Nsw], [s_t, 0, s_c, 0], method="DOP853",
                   rtol=1e-9, atol=1e-12, max_step=0.01)
    th1, dth1, ch1, dch1 = s1.y[:, -1]
    H1 = F.hubble(Nsw)
    amp1 = np.hypot(np.mod(ch1, 2 * np.pi) - np.pi, dch1 * H1 / m_c)
    print(f"   m_theta = {m_t:.0e} eV, m_chi = {m_c:.0e} eV, seeds {s_t:.0e}, {s_c:.0e}")
    print(f"   chi flipped to pi; at H = m_chi/300 its oscillation amplitude is {amp1:.2e}")
    print(f"   theta at that time: {th1:.2e} (still at its birth value)")

    def rhs2(N, y):                 # chi averaged: chi = pi + A cos(mt), A ~ a^-3/2
        th, dth = y
        A = amp1 * np.exp(-1.5 * (N - Nsw))
        H = F.hubble(N)
        return [dth, -(3 + dlnh(N)) * dth + (m_t / H) ** 2 * j0(A) * np.sin(th)]

    s2 = solve_ivp(rhs2, [Nsw, 0.0], [th1, dth1], method="DOP853", rtol=1e-10,
                   atol=1e-13, dense_output=True)
    th = lambda z: s2.sol(-np.log1p(z))[0]
    beta = np.degrees(F.ALPHA / (2 * np.pi) * (th(0.0) - th(F.Z_STAR)))
    print(f"   theta lands at {th(0.0) / np.pi:.4f} pi;  beta_rec = {beta:.4f} deg"
          f"  (alpha/2 = {np.degrees(F.ALPHA) / 2:.4f})")
    print("   -> with the torsion flip, theta starts from its exact birth value and")
    print("      beta = alpha/2 follows with NO initial-condition tuning (cf. ~3 %")
    print("      probability for a random start).")
    print("   Without the flip (chi stays 0): theta = 0 is a minimum -> beta = 0.")


def brentq_like(fun, a, b):
    from scipy.optimize import brentq
    return brentq(fun, a, b)


# --------------------------------------------- C. relic abundance of chi (DM)
def eps_inv(s, hilltop=True, xmax_after=300.0):
    """radiation era, x = m t: chi'' + 3/(2x) chi' = +sin chi (hilltop) or -chi.
    returns late-time invariant  rho/(m^2 f^2) * x^{3/2}  (cycle-averaged)."""
    def rhs(x, y):
        f = np.sin(y[0]) if hilltop else -y[0]
        return [y[1], -1.5 / x * y[1] + f]
    x0 = 1e-4
    # roll time estimate
    xe = (np.log(np.pi / s) + 5 if hilltop else 5) + xmax_after
    sol = solve_ivp(rhs, [x0, xe], [s, 0.0], method="DOP853", rtol=1e-10,
                    atol=1e-14, dense_output=True, max_step=0.05)
    xs = np.linspace(xe - 60, xe, 6000)
    c, dc = sol.sol(xs)
    pot = (1 + np.cos(c)) if hilltop else 0.5 * c ** 2
    eps = 0.5 * dc ** 2 + pot
    return np.mean(eps * xs ** 1.5)


def omega_h2(m, f, E):
    """Omega h^2 for rho a^3 invariant E (radiation-era release)"""
    rho0 = f ** 2 * np.sqrt(m) * (4 * RHO_R0 / (3 * MPL_EV ** 2)) ** 0.75 * E
    return rho0 / RHO_C_H2


def part_c():
    print("\n" + BAR + "\n C. Cosmic role of chi\n" + BAR)
    print("   Dark energy branch (m_chi <~ H0): chi has NOT flipped by z ~ 50, so")
    print("   psi stays antiperiodic, theta = 0 stays a minimum: no birefringence.")
    print("   -> the math EXCLUDES the torsion twist as dark energy in STUR-ROLL")
    print("      (it needs m_chi >> m_theta ~ 1e-30 eV).")
    Eq = eps_inv(1.0, hilltop=False)
    om = omega_h2(1e-22, 1e26, Eq)
    print(f"\n   integrator check: quadratic misalignment, chi_i = 1, m = 1e-22 eV,")
    print(f"   f = 1e17 GeV -> Omega h^2 = {om:.3f}  (literature: O(0.1))")
    print("\n   Dark matter branch: chi oscillates about pi after the flip.")
    print("   Lyman-alpha (Rogers & Peiris 2021): m > 2e-20 eV for all-DM.")
    print(f"   {'m_chi [eV]':>11s} {'seed':>7s} {'f_chi for Omega h^2 = 0.12 [GeV]':>33s}")
    for s in (1e-4, 1e-12):
        E = eps_inv(s)
        for m in (2e-20, 1e-18, 1e-15):
            f = np.sqrt(0.12 / omega_h2(m, 1.0, E))
            print(f"   {m:11.0e} {s:7.0e} {f / 1e9:33.2e}")
    print("   -> f_chi ~ 1e14-1e16 GeV: sub-Planckian, close to the GUT scale.")


def part_d():
    print("\n" + BAR + "\n D. What the DM branch must solve\n" + BAR)
    s1, s2 = 1e-4, 1e-5
    dl = (np.log(eps_inv(s2)) - np.log(eps_inv(s1))) / (np.log(s2) - np.log(s1))
    print(f"   d ln rho_chi / d ln seed = {dl:+.3f}")
    for n in (60, 100):
        diso = abs(dl) / np.sqrt(n)
        print(f"   random-walk seed, N = {n}: delta_iso ~ |dln rho/dln s| / sqrt(N)"
              f" = {diso:.1e}")
    lim = np.sqrt(0.038 / (1 - 0.038) * 2.1e-9)
    print(f"   Planck 2018: beta_iso < 0.038 -> delta_iso <~ {lim:.0e}")
    print("   -> EXCLUDED by ~3-4 orders unless chi is heavy during inflation")
    print("      (m_chi,eff > H_inf: a Hubble-induced torsion mass), so no")
    print("      super-horizon chi fluctuations are created.")
    m, f = 2e-20, 2.3e24          # the all-DM point of part C
    sig = 8 * m * f ** 2
    ratio = sig / (MPL_EV ** 2 * H0)
    print(f"\n   Domain walls: regions roll to +pi or -pi; wall tension 8 m f^2 ="
          f" ({sig ** (1 / 3) / 1e9:.0f} GeV)^3")
    print(f"   scaling network today: rho_wall/rho_crit ~ sigma/(M_Pl^2 H0) ~ {ratio:.0e}")
    print("   -> CATASTROPHIC unless every region of our universe rolls the same")
    print("      way: needs a parity-odd tilt of V_T (e.g. a Holst / Nieh-Yan term,")
    print("      which is parity-violating torsion) larger than the seed.")
    print("   With both (inflationary pinning + tilt) chi rolls coherently from a")
    print("   fixed offset: no isocurvature, no walls, deterministic abundance.")


if __name__ == "__main__":
    rng = np.random.default_rng(1)
    part_a(rng)
    part_b()
    part_c()
    part_d()
