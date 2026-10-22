#!/usr/bin/env python3
"""
================================================================================
GENESIS v10 -- searching STUR's own structure for a birefringence suppression
================================================================================
genesis_v10_beta_from_action.py showed that STUR's chiral R-Yukawa (c_g = 8,
colour c_s = 3) plus a phase ROTATING at omega = 2 pi^2 per unit ln t gives
beta ~ 110 deg, excluded, and rolls theta_QCD. Matching 0.277 deg needs a
suppression of ~400. This script tests only mechanisms built from structure
already in the repo; no ratio is hunted to produce the number 400.

  M1  Z3 generation charges summing to zero (the 1 + w + w^2 = 0 structure the
      repo uses for anomaly cancellation): c_g = c_s = 0.
  M2  Only leptons carry R-charge: c_s = 0 (strong CP safe), c_g = 3.
  M3  The chronomagnetic mode OSCILLATES rather than rotates. The repo's own
      equation (DERIVATION_CHAIN_INFINITY.md 2.3b; infinity_helix_dynamics.py
      'theta_twist = 2pi/3 + delta theta(t)') is a real mode W = A sin(w ln t):
        theta(t) = A(t) sin(w' ln(t/t0) + delta)
      (a) repo friction 1/t:       A = A0,                 w' = w
      (b) FRW friction 3H = 2/t:   A = A0 (t/t0)^(-1/2),   w' = sqrt(w^2 - 1/4)
      Then beta(t_emit) = K [theta(t0) - theta(t_emit)], K = c_g alpha / 2 pi.
      The bounded excursion replaces Delta phi = 207 rad by ~A0, and the spread of
      ln t across each visibility window averages the oscillating part away.
      Paired with M2 (c_g = 3), because any colour anomaly would make
      theta_QCD = 2 c_s theta oscillate with amplitude ~ A0, far above 1e-10.

For M3, A0 is solved for at each phase delta so that the high-l (recombination)
angle equals beta_now; the reionization angle then follows from the exact CAMB
sources (Stage 10b machinery). Outputs: the A0 required (is it natural?), the
predicted ratio and Delta beta over all delta, and the recombination-era
depolarisation.

Usage:  python genesis_v10_phase_suppression.py
================================================================================
"""
import importlib.util
import os

import camb
import numpy as np
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("g10b", os.path.join(HERE, "genesis_v10b_boltzmann.py"))
G = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(G)

ALPHA = 1 / 137.035999
OMEGA = 2 * np.pi ** 2
BETA_OBS, S_BETA_OBS = 0.277, 0.057
gates = []


def gate(name, ok, detail):
    gates.append(bool(ok))
    print(f"  gate: {name:54s} {detail:34s} {'PASS' if ok else 'FAIL'}")


def header(s):
    print("\n" + "=" * 80 + "\n  " + s + "\n" + "=" * 80)


def theta_mode(variant, A0, delta, t0):
    if variant == "a":
        return lambda t: A0 * np.sin(OMEGA * np.log(t / t0) + delta)
    wp = np.sqrt(OMEGA ** 2 - 0.25)
    return lambda t: A0 * (t / t0) ** -0.5 * np.sin(wp * np.log(t / t0) + delta)


def main():
    header("M1  Z3 generation charges summing to zero")
    print("  X_g = (1, 1, -2) or (1, 0, -1) over generations: c_g = (8/3) sum X_g = 0, c_s = 0.")
    print(f"  => beta = 0 exactly; observed {BETA_OBS} +/- {S_BETA_OBS} deg -> {BETA_OBS / S_BETA_OBS:.1f} sigma tension.")
    print("     Strong-CP safe, but predicts no birefringence (STUR-B would be false).")

    header("M2  only leptons carry R-charge (rotation at omega)")
    K2 = 3 * ALPHA / (2 * np.pi)
    print(f"  c_g = 3, c_s = 0: beta = {np.degrees(K2 * OMEGA * 10.5217):.1f} deg (excluded; see beta_from_action)")

    header("M3  oscillating chronomagnetic mode, leptons only (c_g = 3)")
    src = G.Sources(r=0.0035)
    t0 = src.t0
    # recombination: visibility-weighted <exp(2 i beta)> on the high-l eta grid
    gh = src.grids["hi"]
    vis = src.res.get_background_time_evolution(gh['eta'], ['visibility'])['visibility'] * gh['w']
    wv = vis / vis.sum()
    t_rec = gh['t']

    def rec_angle(variant, A0, delta):
        th = theta_mode(variant, A0, delta, t0)
        b = K2 * (th(t0) - th(t_rec))
        z2 = np.sum(wv * np.exp(2j * b))
        return np.degrees(np.angle(z2) / 2), abs(z2)

    deltas = np.linspace(0, 2 * np.pi, 13)[:-1]
    sol = {}
    for variant in ("a", "b"):
        for d in deltas:
            f = lambda A: rec_angle(variant, A, d)[0] - BETA_OBS
            grid = np.linspace(1e-3, 3.0, 600)
            vals = np.array([f(A) for A in grid])
            idx = np.where(np.sign(vals[:-1]) != np.sign(vals[1:]))[0]
            if len(idx) == 0:
                sol[(variant, d)] = None
                continue
            A0 = brentq(f, grid[idx[0]], grid[idx[0] + 1])
            sol[(variant, d)] = (A0, rec_angle(variant, A0, d)[1])
    # reionization from exact sources (l = 2-10), all solutions in one Bessel pass
    ells = np.arange(2, 11)
    H = {}
    for (variant, d), s_ in sol.items():
        if s_ is None:
            continue
        th = theta_mode(variant, s_[0], d, t0)
        H[(variant, d)] = (lambda z, t, th=th: np.degrees(K2 * (th(t0) - th(t))))
    cee, ceb = src.transfers(ells, H)
    wlo = (2 * ells + 1) * cee
    res = {}
    for key in H:
        b = G.beta_eff(cee, ceb[key])
        breio = float(np.sum(wlo * b) / np.sum(wlo))
        res[key] = (sol[key][0], sol[key][1], breio)
    for variant, lab in (("a", "(a) repo friction, constant amplitude"),
                         ("b", "(b) FRW friction, A ~ t^-1/2")):
        print(f"\n  {lab}")
        print(f"    {'delta':>6s} {'A0 [rad]':>9s} {'A(t*)':>8s} {'pol.frac':>9s} {'beta_reio':>10s} {'ratio':>7s} {'Delta beta':>11s}")
        for d in deltas:
            if (variant, d) not in res:
                print(f"    {d:6.2f}   no A0 <= 3 rad reproduces beta_now")
                continue
            A0, pol, br = res[(variant, d)]
            At = A0 * ((src.tstar / t0) ** -0.5 if variant == "b" else 1)
            print(f"    {d:6.2f} {A0:9.3f} {At:8.2f} {pol:9.4f} {br:9.3f}° {br / BETA_OBS:7.3f} {br - BETA_OBS:+10.3f}°")
    ok_a = [res[k] for k in res if k[0] == "a"]
    ok_b = [res[k] for k in res if k[0] == "b"]
    if ok_a:
        A0s = [r[0] for r in ok_a]
        ratios = [r[2] / BETA_OBS for r in ok_a]
        print(f"\n  (a): A0 needed {min(A0s):.2f}-{max(A0s):.2f} rad; ratio spans {min(ratios):.2f} to {max(ratios):.2f}")
        gate("(a) natural amplitude: some delta needs A0 <= 1 rad", min(A0s) <= 1.0, f"min A0 = {min(A0s):.2f} rad")
        gate("(a) ratio is a prediction (spread over delta < 0.1)", max(ratios) - min(ratios) < 0.1,
             f"spread = {max(ratios) - min(ratios):.2f}")
    if ok_b:
        pols = [r[1] for r in ok_b]
        print(f"  (b): solutions at {len(ok_b)}/12 phases; recombination polarisation fraction {min(pols):.3f}-{max(pols):.3f}")
        gate("(b) depolarisation at recombination < 1%", min(pols) > 0.99, f"min pol. fraction = {min(pols):.3f}")
    print("\n  today: d beta/dt = K A0 w cos(delta)/t0 ~ "
          f"{np.degrees(K2 * 1.0 * OMEGA / (t0 * 1e9)):.1e} deg/yr per rad of A0 (unobservable)")

    header("VERDICT")
    print("""  M1 removes the problem by removing the signal (beta = 0, 4.9 sigma from current data).
  M2 fixes strong CP but not the size. M3 is the only STUR-internal mechanism that gives a
  natural size: a bounded O(1)-radian oscillation of the R-phase replaces 207 rad of winding.
  What it predicts is set out in the table above: read the A0 column for naturalness and
  the ratio column for whether the tomographic shape survives as a prediction.""")
    print(f"\n  gates: {sum(gates)}/{len(gates)} passed")


if __name__ == "__main__":
    main()
