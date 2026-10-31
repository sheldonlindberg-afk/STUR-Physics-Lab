#!/usr/bin/env python3
"""
Refinement round 6: an angle-valued brane field fixes the twist at exactly pi.
See docs/REFINEMENT_R6.md. Requires numpy, scipy. Runs in ~30 s.

Brane term at y = 0:   L_0 > f_v^2 (d vartheta)^2 / 2 - V(vartheta)
                              - vartheta (q_psi J^y_psi + q_phi J^y_phi)
vartheta ~ vartheta + 2 pi requires integer q's; the y-currents are Z2-odd, so
vartheta is Z2-odd: vartheta -> -vartheta.

  A. Symmetry: any Z2-even, 2pi-periodic V has stationary points exactly at
     0 and pi; loop corrections are even too, so a minimum at pi stays at pi.
  B. Charges: at vartheta = pi the twist is (-1)^q per field. theta = 0 is a
     hilltop iff q_psi is odd and q_phi is even (vartheta = pi acts as a
     localized fermion-parity defect).
  C. Timing: if m_vartheta > H at birth, vartheta rolls 0 -> pi within a few
     e-folds, inside the single nucleated Hubble patch: coherent, no walls.
  D. Full chain: beta from theta's exact birth value plus its inflationary
     random walk.
"""
import os
import sys

import numpy as np
from scipy.integrate import solve_ivp

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import stur_final as F  # noqa: E402

BAR = "=" * 78
rng = np.random.default_rng(11)


def part_a():
    print(BAR + "\n A. Z2 symmetry pins the extrema of V(vartheta) at 0 and pi\n" + BAR)
    v = np.linspace(-np.pi, np.pi, 4001)
    n_pi, worst = 0, 0.0
    for _ in range(2000):
        c = rng.normal(0, 1, 5) / np.arange(1, 6) ** 1.5      # random even series
        V = sum(ck * np.cos((k + 1) * v) for k, ck in enumerate(c))
        dV = sum(-ck * (k + 1) * np.sin((k + 1) * v) for k, ck in enumerate(c))
        worst = max(worst, abs(dV[2000]), abs(dV[0]))         # at 0 and at -pi
        imin = V.argmin()
        n_pi += min(abs(v[imin] - np.pi), abs(v[imin] + np.pi)) < 1e-3
    print(f"   2000 random Z2-even periodic potentials: max |V'| at 0 and pi = {worst:.1e}")
    print(f"   global minimum exactly at pi in {n_pi}/2000 cases (else at 0 or at a")
    print("   symmetric pair +-v0, which breaks the orbifold parity)")
    print("   -> whenever the brane settles at pi, delta = pi EXACTLY; quantum")
    print("      corrections respect the orbifold parity and cannot move it.")
    print("   The psi loop adds an even term ~ -A cos(vartheta) of size ~ m_theta^2")
    print("   f_theta^2 <~ 1e-13 eV^4, negligible against any brane-scale V.")


def part_b():
    print("\n" + BAR + "\n B. Which charges make theta = 0 a hilltop at vartheta = pi?\n" + BAR)
    print("   late time (fermion-dominated, A_f > A_b), birth spin structure:")
    print("   V(theta) = -A_f cos(theta + q_psi vartheta) - A_b cos(theta + q_phi vartheta)")
    th = np.linspace(-np.pi, np.pi, 721)
    Af, Ab = 1.0, 0.3
    print(f"   {'q_psi':>6s} {'q_phi':>6s}   theta = 0 is")
    for qp in range(3):
        for qs in range(3):
            V = -Af * np.cos(th + qp * np.pi) - Ab * np.cos(th + qs * np.pi)
            kind = ("HILLTOP" if abs(th[V.argmax()]) < 1e-3
                    else "minimum" if abs(th[V.argmin()]) < 1e-3 else "-")
            print(f"   {qp:6d} {qs:6d}   {kind}")
    print("   -> q_psi odd, q_phi even: vartheta = pi inserts (-1) for psi only, a")
    print("      localized fermion-parity defect. It turns the antiperiodic (birth)")
    print("      spin structure seen by psi into the periodic one that stur_final.py")
    print("      assumed. (q_psi, q_phi both odd also works if A_f > A_b, but then")
    print("      the de Sitter-era scalar dominance would flip too; keep q_phi = 0.)")


def part_c():
    print("\n" + BAR + "\n C. vartheta's roll at birth (de Sitter, H = const)\n" + BAR)
    print("   vartheta'' + 3 vartheta' = (m/H)^2 sin(vartheta)   (N = e-folds)")
    print(f"   {'m/H':>5s} {'seed':>7s} {'N to reach 0.99 pi':>19s} {'then':>22s}")
    for mh in (1.0, 2.0, 5.0):
        for s in (1e-5, 1e-10):
            def rhs(N, y):
                return [y[1], -3 * y[1] + mh ** 2 * np.sin(y[0])]
            ev = lambda N, y: y[0] - 0.99 * np.pi
            ev.terminal = True
            sol = solve_ivp(rhs, [0, 200], [s, 0.0], events=ev, rtol=1e-10, atol=1e-14,
                            dense_output=True)
            nr = sol.t_events[0][0] if sol.t_events[0].size else np.nan
            late = solve_ivp(rhs, [0, nr + 20], [s, 0.0], rtol=1e-10, atol=1e-14).y[0, -1]
            print(f"   {mh:5.1f} {s:7.0e} {nr:19.1f}   settles at {late / np.pi:.6f} pi")
    print("   -> m >~ 2H: the brane twists within ~4-26 e-folds of birth (m ~ H: 50-90).")
    print("      The direction is fixed while the universe is still ~one Hubble patch;")
    print("      any walls from the first few e-folds lie beyond our horizon if inflation")
    print("      lasts >~ 60 + N_twist e-folds: no vartheta walls in the observable universe.")
    print("      vartheta is heavy, so it has no super-horizon fluctuations: no")
    print("      isocurvature. (Compare round 4: both problems are absent here.)")


def part_d():
    print("\n" + BAR + "\n D. Full chain: theta from its exact birth value\n" + BAR)
    print("   theta = 0 at birth; random walk s0 sqrt(N) during inflation (R2.4);")
    print("   after the twist, theta = 0 is the hilltop; roll at late times.")
    print(f"   {'s0 = H/2pi f':>13s} {'N':>4s} {'theta_i':>9s} {'beta_rec [deg]':>15s}"
          f" {'/ (alpha/2)':>12s}")
    a2 = np.degrees(F.ALPHA) / 2
    for s0 in (1e-4, 1e-3, 1e-2):
        for n in (60,):
            ti = s0 * np.sqrt(n)
            _, b, _ = F.roll(1e-30, ti)
            print(f"   {s0:13.0e} {n:4d} {ti:9.1e} {b:15.4f} {b / a2:12.4f}")
    print("   -> beta = alpha/2 to <~1 % for s0 <~ 1e-3 (H_nuc <~ 6e-3 f), and to")
    print("      3 % up to s0 ~ 1e-2: no initial-condition coincidence remains.")


if __name__ == "__main__":
    part_a()
    part_b()
    part_c()
    part_d()
