#!/usr/bin/env python3
"""
================================================================================
GENESIS v10 -- no-fit audit of the tensor-to-scalar ratio r
================================================================================
The pre-registration commits to r = 0.0035 (GENESIS Starobinsky R^2, N* = 55);
the repo's own scripts/stur_inflation.py claims r_eff = 0.0139 (D status). This
script asks, for each, whether it follows from the STUR Master Action with
nothing chosen to fit.

  1. Is there an R^2 (scalaron) term in the STUR action?
  2. Recompute stur_inflation.py's own model consistently:
       V = m^2 R^2 / 2,  R_ddot + beta_H H R_dot + V' = 0,  beta_H = 3 + 2 pi,
       r = 16 eps_H,  P_R = H^2 / (8 pi^2 eps_H)  (its own assumptions)
     The script fixed eps at the standard-friction value 1/(2N) and rescaled it
     by (3/beta_H)^2. But extra friction also changes N(R), so the field value
     at the pivot moves. Done consistently (slow roll, M_Pl = 1):
       N = (beta_H/3) (R^2 - R_end^2)/4,  eps_H = (9/beta_H^2)(2/R^2)
       => eps_H = 3/(2 beta_H N),  r = 16 eps_H = 24/(beta_H N)
     With friction, H_dot = -(beta_H/3) R_dot^2/2, so -H_dot/H^2 = (beta_H/3) eps_H and
     n_s - 1 = -2/N is unchanged (the repo is right about n_s). Inflation ends at
     -H_dot/H^2 = 1. All of this is checked by direct numerical integration below.

Usage:  python genesis_v10_r_from_action.py
================================================================================
"""
import numpy as np
from scipy.integrate import solve_ivp

BETA_H = 3 + 2 * np.pi
R_BK = 0.036                    # BICEP/Keck 2021, 95% CL
NS, S_NS = 0.9649, 0.0042       # Planck 2018

gates = []


def gate(name, ok, detail):
    gates.append(bool(ok))
    print(f"  gate: {name:54s} {detail:34s} {'PASS' if ok else 'FAIL'}")


def header(s):
    print("\n" + "=" * 80 + "\n  " + s + "\n" + "=" * 80)


def part1():
    header("1. Is Starobinsky R^2 in the STUR Master Action?")
    print("""  Master Action (stur_master_action_derivation.html eq. 2.5): 1/2|dR|^2 - V(|R|)
  + chi|R|^2 d_X phi + alpha|R| T + L_matter. Gravity enters only through the TEGR
  torsion scalar T, linearly. There is no R_Ricci^2 (or T^2) term, and sec. 3.1 of the
  same page excludes higher-derivative terms explicitly. f(T) theories are second
  order and do not propagate the R^2 scalaron, so no T-analogue supplies it either.
  => r = 0.0035 is a GENESIS modelling choice (Starobinsky R^2), not a STUR output.""")


def slow_roll_numeric(beta, Npiv):
    """integrate R_ddot + beta H R_dot + R = 0 (m = 1, M_Pl = 1) from R = 30 to the end"""
    def rhs(t, y):
        R, Rd, N = y
        H = np.sqrt((0.5 * Rd ** 2 + 0.5 * R ** 2) / 3)
        return [Rd, -beta * H * Rd - R, H]
    def end(t, y):
        R, Rd, _ = y
        H = np.sqrt((0.5 * Rd ** 2 + 0.5 * R ** 2) / 3)
        return beta / 3 * Rd ** 2 / (2 * H ** 2) - 1   # -H_dot/H^2 = (beta/3) eps_H = 1
    end.terminal = True
    R0 = 30.0
    H0 = R0 / np.sqrt(6)
    s = solve_ivp(rhs, [0, 1e5], [R0, -R0 / (beta * H0), 0.0], events=end, rtol=1e-10,
                  atol=1e-12, dense_output=True, max_step=1.0)
    tend = s.t_events[0][0]
    Nend = s.sol(tend)[2]
    tt = np.linspace(0, tend, 200001)
    R, Rd, N = s.sol(tt)
    H = np.sqrt((0.5 * Rd ** 2 + 0.5 * R ** 2) / 3)
    eps = Rd ** 2 / (2 * H ** 2)
    Nleft = Nend - N
    lnk = N + np.log(H)                            # k = aH at exit
    lnP = np.log(H ** 2 / (8 * np.pi ** 2 * eps))
    i = np.argmin(np.abs(Nleft - Npiv))
    sl = slice(max(i - 200, 0), i + 200)
    ns = 1 + np.polyfit(lnk[sl], lnP[sl], 1)[0]
    return 16 * eps[i], ns


def part2():
    header("2. stur_inflation.py recomputed with its own assumptions")
    for Npiv in (55, 60):
        r_repo = 16 / (2 * Npiv) * (3 / BETA_H) ** 2
        r_an = 24 / (BETA_H * Npiv)
        ns_an = 1 - 2 / Npiv
        r_num, ns_num = slow_roll_numeric(BETA_H, Npiv)
        print(f"\n  N* = {Npiv}:  repo formula r = r0 (3/beta_H)^2 = {r_repo:.4f}, n_s = {1 - 2 / Npiv:.4f}")
        print(f"          consistent slow roll: r = 24/(beta_H N) = {r_an:.4f}, n_s = {ns_an:.4f}")
        print(f"          numerical integration: r = {r_num:.4f}, n_s = {ns_num:.4f}")
        if Npiv == 60:
            gate("numerics confirm r = 24/(beta_H N) (N = 60)", abs(r_num / r_an - 1) < 0.03,
                 f"{r_num:.4f} vs {r_an:.4f}")
            gate("standard friction (beta = 3) recovers r = 8/N", abs(slow_roll_numeric(3.0, 60)[0] / (8 / 60) - 1) < 0.03,
                 f"{slow_roll_numeric(3.0, 60)[0]:.4f} vs {8 / 60:.4f}")
            gate("corrected stur_inflation r below BICEP/Keck 0.036", r_num < R_BK, f"r = {r_num:.4f}")
            gate("n_s = 1 - 2/N unchanged by friction (repo claim)", abs(ns_num - ns_an) < 0.002,
                 f"{ns_num:.4f} vs {ns_an:.4f}")
    print("""
  The repo's 0.0139 rescaled eps at fixed N; friction also stretches N(R), which moves
  the pivot to smaller R and raises eps_H by beta_H/3. Its claim that Hubble-proportional
  friction leaves n_s unchanged does hold.""")


def main():
    part1()
    part2()
    header("VERDICT")
    print("""  Neither r value is a no-fit STUR prediction:
    * r = 0.0035 (pre-registered) assumes Starobinsky R^2, which is not in the STUR action.
    * stur_inflation.py's r = 0.0139 is an arithmetic slip: computed consistently its own
      model gives r ~ 0.043-0.047 (excluded by BICEP/Keck r < 0.036 at 95%); n_s = 1 - 2/N
      is unaffected and fine.
  The Master Action's only scalar, |R| with V = lambda/4 (|R|^2 - v^2)^2 and gravity
  coupling alpha|R|T, has not been worked out as an inflaton anywhere in the repo.""")
    print(f"\n  gates: {sum(gates)}/{len(gates)} passed (the FAILs are the result, not a code error)")


if __name__ == "__main__":
    main()
