#!/usr/bin/env python3
"""
Make It Make Sense theory, part 7: the ceiling at every point (local fullness).

L1  Correction to part 6.  The "local fullness 6-94, rising with resolution" reported in
    v0.4 was a numerical ARTIFACT: in the one cell holding the shock, the stored phase is an
    average of b ~ pi (inside) and b ~ 0 (outside), i.e. ~pi/2 ("full"), and converting it
    to mass gives a spurious (4 pi/3) R^3 rho_max.  RETRACTED.  What stands: in the exact
    weak solution the mass function jumps from 0 to M at one radius -- a zero-thickness
    shell, so local fullness is unbounded and P1 is broken in the continuum.

L2  A local law tried: each layer's active mass weighted by its OWN fullness,
        d^2 R_i/dtau^2 = -(G / R_i^2) sum_{j<=i} dm_j (1 - 4 phi_j)            (NEW)
    which is exact for a uniform star (it is the homogeneous law).  Result: local fullness
    stays <= 1 (P1 kept), but the model has no equation for the geometry outside the
    matter, and the star comes straight back out through its own horizon in a few
    Planck times per Planck mass -- part 4's case (b), excluded by observation.  Not viable
    on its own.

L3  What the shell is.  Across the shock the phase jumps by ~pi in b = one full turn of
    the dance (u = 2b): the inner layers have completed collapse -> full -> re-expansion,
    the outer ones have not started.  A conservation law's shock speed is [F]/[B], so it
    depends on how that turn is counted (KNOWN: weak solutions need a rule).
      winding (count the turn; parts 5-6):  the phase inside the shell passes FULL
        (b = pi/2).  A smooth shell would then hold (4 pi/3) R^3 rho_max of mass, which is
        (32 pi/3) M^2 times the star's mass at R = r_s: impossible, so the shell must be
        infinitely thin and P1 fails.                                            (FOLLOWS)
      angle (one turn = no change): the phase passes EMPTY (b = pi); a finite shell at
        phi <= 1 is possible.                                                   (FOLLOWS)
    => P1 forces the angle rule.  Part 5's lifetime ~ 24 sqrt(chi) M^2 came from the
       winding rule, so it is NOT yet the theory's answer.  A valid angle-rule solver
       (conserving mass, not the winding) is OPEN; an attempt that re-wrapped the stored
       phase broke conservation and is not used.

L4  Independent check from GR.  Outside r_s the law is GR to 1e-77 (part 4), so a thin
    shell of pure matter (rest mass mu = M, marginally bound) obeys the Israel junction
    condition (KNOWN):  M = mu sqrt(1 + Rdot^2) - G mu^2 / 2R  =>  Rdot^2 = M/R + M^2/4R^2.
    It moves at 0.7 c near r_s; the winding solution's drift (0.019/M c) is ~100x too slow
    at M = 3 and ~1e31x too slow for a real primordial hole.  The slow drift is an
    artifact of the winding rule.  Once outside r_s, the matter leaves promptly: the TeV
    flash of part 6 is the theory's burst, if the shell gets out.
"""
import numpy as np
from scipy.integrate import solve_ivp

import fp_collapse_shock as S


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


# ----------------------------------------------------------------- L1
def artifact_check(M=3.0, dR=0.05, t_over_T=1.5):
    k, Rf, Rc, B = S.setup(M, 1.0, dR, 3.0, 1.5)
    t = 0.0
    while t < t_over_T * 24.1 * M ** 2:
        B, dt = S.step(B, k, Rf, Rc, dR, 0.45)
        t += dt
    b = np.clip(B / Rc ** 2, 0, np.pi)
    m = 4 * np.pi / 3 * Rc ** 3 * np.sin(b) ** 2
    j = np.argmax(m)
    rs = 2 * M
    inside = m[np.searchsorted(Rc, 0.95 * rs)] / M
    # width of the 0 -> M rise, ignoring the single spurious cell
    good = np.abs(m - M) < 0.01 * M
    first_full = Rc[np.argmax(good & (Rc > rs))]
    last_empty = Rc[np.where((m < 0.01 * M) & (Rc < first_full))[0].max()]
    return dict(spurious=m[j] / M, b_cell=b[j] / np.pi, inside=inside,
                width=(first_full - last_empty) / dR)


# ----------------------------------------------------------------- L2
def local_law(M, N=200, chi=1.0, R0fac=1.5, tfac=1.0):
    rs = 2 * M
    R0 = R0fac * rs
    dm = np.full(N, M / N)
    m = np.cumsum(dm)
    r = R0 * (m / M) ** (1 / 3)
    v = -np.sqrt(2 * m / r * (1 - 3 * M / (4 * np.pi * chi * R0 ** 3)))

    def phis(r):
        rin = np.concatenate([[0.0], r[:-1]])
        return dm / (chi * 4 * np.pi / 3 * np.maximum(r ** 3 - rin ** 3, 1e-300))

    def rhs(t, y):
        r, v = y[:N], y[N:]
        return np.concatenate([v, -np.cumsum(dm * (1 - 4 * phis(r))) / r ** 2])

    sol = solve_ivp(rhs, [0, tfac * 24.1 * M ** 2], np.concatenate([r, v]),
                    method="DOP853", rtol=1e-8, atol=1e-10, max_step=0.5)
    R, V = sol.y[:N], sol.y[N:]
    phmax = max(phis(R[:, i]).max() for i in range(len(sol.t)))
    trapped = (R[-1] < rs) | (V.min(axis=0) < -1)
    t_out = sol.t[np.where(trapped)[0][-1]]
    return dict(phmax=phmax, t_out=t_out, final=R[-1, -1] / rs)


# ----------------------------------------------------------------- L3, L4
def smooth_winding_shell_ratio(M):
    """Mass a smooth shell would need where its phase passes full, at R = r_s, over M."""
    rs = 2 * M
    return 4 * np.pi / 3 * rs ** 3 / M          # rho_max = 1 (chi = 1), Planck units


def israel_speed(R_over_rs):
    R = 2 * R_over_rs                            # M = 1
    return np.sqrt(1 / R + 1 / (4 * R * R))


def main():
    banner("L1  Correction: the v0.4 'local fullness 6-94' was an artifact")
    a = artifact_check()
    print(f"   one cell holds phase b = {a['b_cell']:.2f} pi (average of ~pi and ~0) and a"
          f" spurious mass {a['spurious']:.0f} M")
    print(f"   true profile: m(<0.95 r_s) = {a['inside']:.4f} M; mass rises 0 -> M across"
          f" {a['width']:.0f} cells (unresolved)")
    print("   -> RETRACTED: the numbers.  STANDS: the exact solution is a zero-thickness shell.")

    banner("L2  A local law: full matter repels (each layer weighted by 1 - 4 phi_local)")
    out = {"art": a}
    for M in (2.0, 3.0):
        r = local_law(M)
        out[M] = r
        print(f"   M = {M}: max local fullness {r['phmax']:.4f};  horizon gone at t = "
              f"{r['t_out']:.1f} = {r['t_out']/M:.2f} M;  surface ends at {r['final']:.1f} r_s")
    print("   P1 holds, but the star re-emerges through its own horizon after ~3.6 M Planck")
    print("   times (solar mass: ~1e-5 s) -- part 4's excluded case (b).  The model has no")
    print("   equation for the geometry outside the matter, so this is not a consistent answer.")

    banner("L3  The shell is a one-turn phase slip; P1 decides how to count it")
    for M in (3.0, 5.8e29):
        print(f"   M = {M:.1e} m_P: a smooth winding shell would need "
              f"{smooth_winding_shell_ratio(M):.1e} x the star's mass")
    print("   -> under winding the shell must be infinitely thin (P1 broken); under the angle")
    print("      rule it passes through EMPTY and can be finite (P1 kept).  P1 forces angle.")
    print("   -> part 5's M^2 lifetime used winding: downgraded to OPEN.")

    banner("L4  GR check: how fast a thin shell of pure matter moves outside r_s")
    for x in (1.0, 1.14, 1.26, 2.0):
        print(f"   R = {x:4.2f} r_s:  Israel junction speed {israel_speed(x):.3f} c")
    drift = 0.019 / 3
    print(f"   winding drift at M = 3: {drift:.4f} c ({israel_speed(1.14)/drift:.0f}x slower);"
          f" at a real primordial hole {0.019/5.8e29:.1e} c")
    print("   -> the slow drift is an artifact of the winding rule.  Outside r_s the matter")
    print("      leaves at ~0.7 c: the prompt TeV flash (part 6) is the theory's burst.")
    print("   OPEN: WHEN the shell gets outside r_s (the lifetime) needs an angle-rule solver.")
    out.update(israel=israel_speed(1.14), ratio=smooth_winding_shell_ratio(3.0))
    return out


if __name__ == "__main__":
    main()
