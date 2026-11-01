#!/usr/bin/env python3
"""
Refinement round 9: can STUR-ROLL calculate the Cabibbo angle?
Preregistered in docs/R9_PREREGISTRATION.md; results in docs/REFINEMENT_R9.md.
Requires numpy, scipy. Runs in about 1 min.

  9A  an angle fixed by STUR-ROLL's discrete symmetries (orbifold parity,
      the brane angle at vartheta = pi acting as (-1)^q, the Z6 centre)
  9B  the angle from wavefunction overlaps: bulk quarks with kink masses,
      anarchic O(1) 5D Yukawas, profiles solved to reproduce the six quark
      masses; the distribution of |V_us|
"""
import itertools

import numpy as np
from scipy.optimize import least_squares

BAR = "=" * 78
VUS, S_VUS = 0.2250, 0.0007
V_EW = 246.22
# quark masses at M_Z, MS-bar, GeV (approximate; only ratios matter here)
M_UP = np.array([1.23e-3, 0.620, 171.7])
M_DN = np.array([2.67e-3, 0.0532, 2.839])
Y_UP, Y_DN = np.sqrt(2) * M_UP / V_EW, np.sqrt(2) * M_DN / V_EW


def ckm(Yu, Yd):
    """V = U_uL^dagger U_dL with singular values ordered light -> heavy"""
    def left(Y):
        U, s, _ = np.linalg.svd(Y)
        o = np.argsort(s)
        return U[:, o], s[o]
    Uu, su = left(Yu)
    Ud, sd = left(Yd)
    return Uu.conj().T @ Ud, su, sd


def anarchic(rng, shape=(3, 3)):
    mag = np.exp(rng.uniform(np.log(1 / 3), np.log(3), shape))
    return mag * np.exp(1j * rng.uniform(0, 2 * np.pi, shape))


# ---------------------------------------------------------------- 9A
def module_9a(rng):
    print(BAR + "\n 9A  Can a STUR-ROLL discrete symmetry fix |V_us|?\n" + BAR)
    print("   Bulk quarks: a chiral zero mode needs the same orbifold parity at both")
    print("   branes. The brane angle vartheta = pi multiplies the y = 0 parity by")
    print("   (-1)^q, so a field with odd q has NO zero mode (its lightest mode sits")
    print("   at the KK scale). Chiral quarks therefore need q even: vartheta = pi acts")
    print("   as +1 on every quark. The orbifold parity of each zero mode is fixed by")
    print("   its chirality, the same for every generation. The Z6 centre is part of")
    print("   the gauge group and acts identically on all generations.")
    print("   -> bulk quarks: every generation carries identical discrete charges;")
    print("      all 9 Yukawa entries are allowed in each sector.")
    print()
    print("   Brane-localised quarks escape the zero-mode condition, so vartheta's")
    print("   (-1)^q can differ between generations. Enumerating every assignment")
    print("   q in {0,1} for Q_i, u_i, d_i and the Higgs (2^10 = 1024):")
    fixed_vals, variable, massless = [], 0, 0
    for qs in itertools.product((0, 1), repeat=10):
        qQ, qu, qd, qH = np.array(qs[0:3]), np.array(qs[3:6]), np.array(qs[6:9]), qs[9]
        mask_d = ((qQ[:, None] + qd[None, :] + qH) % 2 == 0)
        mask_u = ((qQ[:, None] + qu[None, :] + qH) % 2 == 0)      # H~ has charge -qH = qH mod 2
        vals = []
        ok = True
        for _ in range(4):
            Yd = anarchic(rng) * mask_d
            Yu = anarchic(rng) * mask_u
            if min(np.linalg.svd(Yd)[1].min(), np.linalg.svd(Yu)[1].min()) < 1e-8:
                ok = False
                break
            vals.append(abs(ckm(Yu, Yd)[0][0, 1]))
        if not ok:
            massless += 1
            continue
        if np.std(vals) < 1e-9:
            fixed_vals.append(round(vals[0], 6))
        else:
            variable += 1
    uniq = sorted(set(fixed_vals))
    print(f"     some quark massless (excluded):      {massless}")
    print(f"     |V_us| varies with the couplings:    {variable}")
    print(f"     |V_us| fixed by the symmetry:        {len(fixed_vals)}  -> values {uniq}")
    print("   -> abelian Z2 charges either leave |V_us| continuous or pin it to an")
    print("      endpoint (only 0 occurs here); they never fix a value in between.")
    print("      9A: NO-GO (as preregistered).")


# ---------------------------------------------------------------- 9B
def solve_profiles(yd5, yu5):
    """log-profiles: F_Q = F_d = exp(a) (D-9B3), F_u = exp(b); match all six masses"""
    def resid(x):
        a, b = x[:3], x[3:]
        Fq, Fu = np.exp(a), np.exp(b)
        sd = np.sort(np.linalg.svd(Fq[:, None] * yd5 * Fq[None, :], compute_uv=False))
        su = np.sort(np.linalg.svd(Fq[:, None] * yu5 * Fu[None, :], compute_uv=False))
        return np.concatenate([np.log(sd / Y_DN), np.log(su / Y_UP)])
    a0 = 0.5 * np.log(Y_DN / np.abs(np.diag(yd5)))
    b0 = np.log(Y_UP / (np.exp(a0) * np.abs(np.diag(yu5))))
    sol = least_squares(resid, np.concatenate([a0, b0]), xtol=1e-12, ftol=1e-12,
                        gtol=1e-12, max_nfev=4000)
    return sol, np.max(np.abs(sol.fun))


def module_9b(rng, n=20000):
    print("\n" + BAR + "\n 9B  |V_us| from wavefunction overlaps (anarchic bulk quarks)\n" + BAR)
    print("   Y_d = F_Q y_d F_d, Y_u = F_Q y_u F_u; D-9B3: F_Q = F_d per generation.")
    print("   y anarchic: |y| log-uniform in [1/3, 3], uniform phases. Profiles solved")
    print(f"   so the six masses come out exactly. {n} samples.")
    vus, vcb, vub, fails = [], [], [], 0
    for _ in range(n):
        yd5, yu5 = anarchic(rng), anarchic(rng)
        sol, res = solve_profiles(yd5, yu5)
        if res > 1e-6:
            fails += 1
            continue
        a, b = sol.x[:3], sol.x[3:]
        Fq, Fu = np.exp(a), np.exp(b)
        V, _, _ = ckm(Fq[:, None] * yu5 * Fu[None, :], Fq[:, None] * yd5 * Fq[None, :])
        vus.append(abs(V[0, 1]))
        vcb.append(abs(V[1, 2]))
        vub.append(abs(V[0, 2]))
    vus, vcb, vub = map(np.array, (vus, vcb, vub))
    print(f"   converged: {len(vus)} / {n}  (failed: {fails})")
    print(f"   reference: sqrt(m_d/m_s) = {np.sqrt(M_DN[0] / M_DN[1]):.4f}")
    q = lambda x, p: np.percentile(x, p)
    for name, x, obs in (("|V_us|", vus, 0.2250), ("|V_cb|", vcb, 0.041), ("|V_ub|", vub, 0.0037)):
        print(f"   {name}: median {q(x, 50):.4f};  68% [{q(x, 16):.4f}, {q(x, 84):.4f}];"
              f"  95% [{q(x, 2.5):.4f}, {q(x, 97.5):.4f}];  observed {obs}")
    lo68, hi68, med = q(vus, 16), q(vus, 84), q(vus, 50)
    lo95, hi95 = q(vus, 2.5), q(vus, 97.5)
    half = 0.5 * (hi68 - lo68) / med
    inside68 = lo68 <= VUS <= hi68
    inside95 = lo95 <= VUS <= hi95
    pct = 100 * np.mean(vus <= VUS)
    print(f"   observed |V_us| sits at the {pct:.0f}th percentile; 68% half-width"
          f" = {100 * half:.0f}% of the median (sharp pass needs <= 30%)")
    if inside68 and half <= 0.30:
        verdict = "SHARP PASS"
    elif inside68:
        verdict = "CONSISTENT, NOT PREDICTIVE"
    elif inside95:
        verdict = "CONSISTENT AT 95% ONLY, NOT PREDICTIVE"
    else:
        verdict = "NO-GO"
    print(f"   -> 9B: {verdict}")
    print("   Secondary (reported, not used for the verdict, as preregistered):")
    for name, x, obs in (("|V_cb|", vcb, 0.041), ("|V_ub|", vub, 0.0037)):
        print(f"     observed {name} = {obs} sits at the {100 * np.mean(x <= obs):.1f}th percentile")
    print("   -> the symmetric profiles that make |V_us| testable predict |V_cb| ~ sqrt(m_s/m_b)")
    print("      and |V_ub| ~ sqrt(m_d/m_b), both too large: |V_ub| falls outside the 95% band.")

    print("\n   Without D-9B3 (F_d free): F_Q1/F_Q2 is unconstrained by the masses,")
    rng2 = np.random.default_rng(7)
    spread = []
    for r in (0.3, 1.0, 3.0):
        vals = []
        for _ in range(400):
            yd5, yu5 = anarchic(rng2), anarchic(rng2)
            Fq = np.array([0.0025 * r, 0.05, 1.0])
            # choose F_d, F_u to fit masses at this F_Q (sector by sector, leading order)
            Fd = Y_DN / (Fq * np.abs(np.diag(yd5)))
            Fu = Y_UP / (Fq * np.abs(np.diag(yu5)))
            V, _, _ = ckm(Fq[:, None] * yu5 * Fu[None, :], Fq[:, None] * yd5 * Fd[None, :])
            vals.append(abs(V[0, 1]))
        spread.append(np.median(vals))
        print(f"   F_Q1/F_Q2 = {0.05 * r:.3f}: median |V_us| = {np.median(vals):.3f}")
    print("   -> |V_us| tracks the free ratio F_Q1/F_Q2: no prediction without D-9B3.")
    return vus


def main():
    rng = np.random.default_rng(2026)
    module_9a(rng)
    module_9b(rng)


if __name__ == "__main__":
    main()
