#!/usr/bin/env python3
"""
Can the induced G be made independent of the regulator? The computation registered in INDUCED_GRAVITY_FINITE.md
(commit c1beae2), item by item.

With Pauli's sum rules (S1) str[k1] = 0 and (S2) str[k1 m^2] = 0, the one-loop induced coupling is finite:
    1/G = (1/2 pi) str[k1 m^2 ln m^2]
(derivation in the registration; k1 per field from the accepted campaign induced_g, through the merged chain).
F1  Stage 1 alone: the counting supertrace str[1], and the xi at which stage 1 satisfies S1 by itself.
F2  Bound (A): M_Pl^2 <= (sum |k1|) m_max^2 / (2 pi e) for masses up to m_max = sqrt(4 pi) w: which w reaches M_Pl?
F3  (B) two heavy levels, checked against the full finite formula with stage 1's light masses kept, random cases.
F4  (C) three levels: a case satisfying S1 and S2 with 1/G of the opposite sign.
F5  The asymptotic form of the proper-time integral I(m), against direct integration.
Labels: CHECK (computed), MODEL (induced gravity). Standard library only. About a second.
"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import chain_first_principles as CFP
import induced_gravity as IG

k1 = CFP.induced_g.k1
SELECTED = IG.SELECTED
GAMMA_E = 0.5772156649015329


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


def light_fields(variant, xi):
    """Stage 1's fields as (statistics sign, k1 per field, number): scalars, Weyl fermions, vectors with ghosts."""
    n_v, n_w, n_s = IG.counts(variant)
    return [(+1, k1("scalar", 4, xi), n_s), (-1, k1("weyl", 4), n_w), (+1, k1("vector", 4), n_v)]


def str_k1(fields):
    return sum(s * k * n for s, k, n in fields)


def sum_abs_k1(fields):
    return sum(abs(k) * n for s, k, n in fields)


def xi_for_S1(variant):
    """The xi at which stage 1's str[k1] vanishes (str[k1] is linear in xi with slope -N_S)."""
    s0 = str_k1(light_fields(variant, 0.0))
    return s0 / IG.counts(variant)[2]


def w_needed(fields, mpl):
    """The 3-3-1 scale w at which bound (A), with m_max = sqrt(4 pi) w, first reaches M_Pl."""
    return mpl / (math.sqrt(4 * math.pi) * math.sqrt(sum_abs_k1(fields) / (2 * math.pi * math.e)))


def finite_inv_G(levels):
    """(1/2 pi) sum (+-) k1 m^2 ln m^2 over (signed weight K = (+-) k1 n, mass m) levels."""
    return sum(K * m * m * math.log(m * m) for K, m in levels if m > 0) / (2 * math.pi)


def two_level(S_light, light, M1, M2):
    """Solve S1 and S2 for the heavy weights at M1, M2, with the light levels' masses kept."""
    a = -S_light
    b = -sum(K * m * m for K, m in light)
    K2 = (b - a * M1 * M1) / (M2 * M2 - M1 * M1)
    return a - K2, K2


def formula_B(S, M1, M2):
    r = (M2 / M1) ** 2
    return S / (2 * math.pi) * M1 * M1 * r * math.log(r) / (r - 1)


def I_numeric_subleading(m, eps, n=20000):
    """I(m) - 1/eps = int_eps^inf t^-2 (exp(-t m^2) - 1) dt, by Simpson's rule in u = ln t."""
    a, b = math.log(eps), math.log(60.0 / (m * m))
    h = (b - a) / n
    f = lambda u: math.exp(-u) * (math.exp(-math.exp(u) * m * m) - 1)
    s = f(a) + f(b) + sum((4 if i % 2 else 2) * f(a + i * h) for i in range(1, n))
    tail = -math.exp(-b)          # int_T^inf t^-2 (e^{-tm^2} - 1) dt ~ -1/T for e^{-T m^2} negligible
    return s * h / 3 + tail


def main(seed=7):
    res = {}
    mpl = IG.mpl()
    banner("F1  Stage 1 alone")
    n_v, n_w, n_s = IG.counts(SELECTED)
    s1 = n_s + 2 * n_v - 2 * n_w
    res["str1"] = s1
    xi0 = xi_for_S1(SELECTED)
    res["xi_S1"] = xi0
    print(f"   beta = {SELECTED}: str[1] = N_S + 2 N_V - 2 N_W = {n_s} + {2 * n_v} - {2 * n_w} = {s1}: the kappa^4"
          " (cosmological) term cannot be finite without new fields")
    print(f"   str[k1] = 0 (S1) by stage 1 alone needs xi = {xi0:.5f} for all 18 scalars (just above conformal 1/6)")

    banner("F2  Bound (A): finite induced G from masses up to m_max = sqrt(4 pi) w")
    rows = []
    for label, xi in (("xi = 0", 0.0), ("xi = 1/6", 1 / 6), ("xi at S1", xi0)):
        f = light_fields(SELECTED, xi)
        w = w_needed(f, mpl)
        rows.append((label, sum_abs_k1(f), w))
        print(f"   {label:9s}: sum |k1| = {sum_abs_k1(f):7.3f}; bound reaches the measured M_Pl only at w = {w:.2e} GeV")
    res["w_needed"] = min(r[2] for r in rows)
    print(f"   so the regulator-free version needs w >= {res['w_needed']:.1e} GeV, against w ~ 1e4 GeV for 3-3-1 at the LHC:")
    print("   states near the Planck mass are necessary, and the regulator dependence is a statement about them  [CHECK]")

    banner("F3  (B) two heavy levels: sign = sign of stage 1's str[k1], size = proper-time formula")
    rng = random.Random(seed)
    worst, signs_ok, n = 0.0, True, 0
    for xi in (0.0, 1 / 6, 0.3):
        f = light_fields(SELECTED, xi)
        S = str_k1(f)
        for _ in range(200):
            light = [(s * k, rng.uniform(1.0, 1e4)) for s, k, cnt in f for _ in range(cnt)]   # each field its own mass
            M1 = 10 ** rng.uniform(17, 19.5)
            M2 = M1 * 10 ** rng.uniform(0.01, 2)
            K1, K2 = two_level(S, light, M1, M2)
            full = finite_inv_G(light + [(K1, M1), (K2, M2)])
            approx = formula_B(S, M1, M2)
            worst = max(worst, abs(full / approx - 1))
            signs_ok &= (full > 0) == (S > 0)
            n += 1
    res["B"] = (n, worst, signs_ok)
    print(f"   {n} random completions (xi = 0, 1/6, 0.3; light masses 1 GeV to 10 TeV kept): worst |full/(B) - 1| ="
          f" {worst:.1e}; sign of 1/G = sign of S in every case: {signs_ok}  [CHECK]")
    S0 = str_k1(light_fields(SELECTED, 0.0))
    p = IG.poles(SELECTED)["one loop"]
    for r_ in (1.01, 4.0, 100.0):
        m_eff = math.sqrt(formula_B(S0, p, p * math.sqrt(r_)) * 2 * math.pi / S0)
        print(f"      levels at the one-loop pole and sqrt({r_}) x it: kappa_eff = {m_eff / p:.3f} x pole;"
              f" induced M_Pl = {math.sqrt(formula_B(S0, p, p * math.sqrt(r_))) / mpl:.2f} x measured (xi = 0)")

    banner("F4  (C) three levels: the sign is not fixed")
    S = str_k1(light_fields(SELECTED, 0.0))
    found = None
    for _ in range(20000):
        M = sorted(10 ** rng.uniform(17, 20) for _ in range(3))
        t = rng.uniform(-50, 50)                       # free weight at the middle level
        # K1 + K2 + K3 = -S, K1 M1^2 + K2 M2^2 + K3 M3^2 = 0, K2 = t
        K3 = (-(-S - t) * M[0] ** 2 - t * M[1] ** 2) / (M[2] ** 2 - M[0] ** 2)
        K1 = -S - t - K3
        g = finite_inv_G([(K1, M[0]), (t, M[1]), (K3, M[2])])
        if g < 0:
            found = (K1, t, K3, M, g)
            break
    res["C"] = found
    if found:
        K1, t, K3, M, g = found
        print(f"   S = {S:+.3f} > 0, levels {M[0]:.2e}, {M[1]:.2e}, {M[2]:.2e} GeV with weights {K1:+.2f}, {t:+.2f}, {K3:+.2f}:"
              f" 1/G = {g:.2e} GeV^2 < 0  [CHECK]")
    else:
        print("   no three-level case with the opposite sign found")

    banner("F5  The proper-time integral: I(m) = kappa^2 + m^2 ln(m^2/kappa^2) + (gamma - 1) m^2 + O(1/kappa^2)")
    worst = 0.0
    for m, eps in ((1.0, 1e-6), (2.0, 1e-7), (0.5, 1e-6)):
        num = I_numeric_subleading(m, eps)
        asym = m * m * (math.log(eps * m * m) + GAMMA_E - 1)
        worst = max(worst, abs(num / asym - 1))
        print(f"   m = {m}, kappa^2 = {1 / eps:.0e}: I - kappa^2 numerically {num:.8f}, asymptotic {asym:.8f}")
    res["I"] = worst
    print(f"   worst relative difference {worst:.1e}  [CHECK]")

    banner("Verdict, by the registered table")
    v = {1: s1 != 0, 2: res["w_needed"] > 1e7, 3: res["B"][1] < 1e-6 and res["B"][2], 4: found is not None, 5: worst < 1e-6}
    res["verdict"] = v
    for k, ok in v.items():
        print(f"   item {k}: {'as registered' if ok else 'FAILS the registration'}")
    return res


if __name__ == "__main__":
    main()
