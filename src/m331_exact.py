#!/usr/bin/env python3
"""
Unifying-equation search, front 7b: firming up 'N_c = N_g = 3' with exact charges and
two-loop gauge running.

Model: 3-3-1 with beta = -1/sqrt3 (Q = T3 + beta T8 + X), N_g = N_c generations, quark
charges from anomaly cancellation for general N_c (front 5):
    Q_u = (N_c+1)/(2N_c), Q_d = (1-N_c)/(2N_c).
Left-handed Weyl content:
    leptons   L   = (1, 3, -1/3) x N_g,       e^c = (1, 1, +1) x N_g
    quarks    Q_t = (N_c, 3,  Q_u - 1/3) x (N_g - n)     [u, d, T]
              Q_a = (N_c, 3b, Q_d + 1/3) x n             [d, -u, D],   n = (1+N_c)/2
              u^c, d^c (Nb_c, 1, -Q_u / -Q_d) per generation, plus T^c (-Q_u) or D^c (-Q_d)
    scalars   eta = (1, 3, -1/3), rho = (1, 3, +2/3), chi = (1, 3, -1/3)   (complex;
              X fixed by the Yukawa couplings, N_c-independent)
Checks: every gauge anomaly vanishes for general N_c; the two-loop machinery reproduces
the Standard Model's known one- and two-loop gauge coefficients (GUT-normalised):
    a = (41/10, -19/6, -7),  b = [[199/50, 27/10, 44/5], [9/10, 35/6, 12], [11/10, 9/2, -26]].
Yukawa contributions to the two-loop running are NOT included (they slow the growth of
U(1) couplings in the SM; labelled).
"""
from fractions import Fraction as F
from math import log, pi, sqrt
import numpy as np
from scipy.integrate import solve_ivp

MZ, ainv, s2 = 91.1880, 127.930, 0.23129      # PDG 2024 (MS-bar)
M_PLANCK = 1.22089e19


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


# Group invariants, the general coefficients and the 3-3-1 field content live in m331_core.py
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import m331_core as _core
from m331_core import Group, coefficients                      # noqa: E402,F401


def sm_check():
    gs = [Group("Y"), Group("SU2", 2), Group("SU3", 3)]
    ferm = []
    for _ in range(3):
        ferm += [(1, (None, 2, 3), F(1, 6)), (1, (None, 1, 3), F(-2, 3)), (1, (None, 1, 3), F(1, 3)),
                 (1, (None, 2, 1), F(-1, 2)), (1, (None, 1, 1), F(1))]
    scal = [(1, (None, 2, 1), F(1, 2))]
    a, b = coefficients(gs, ferm, scal)
    # GUT normalisation g1 = sqrt(5/3) g_Y:  a1 = 3/5 a_Y, b11 = 9/25 b_YY, b1j = 3/5 b_Yj, bj1 = 3/5 b_jY
    a = [a[0] * F(3, 5), a[1], a[2]]
    b = [[b[0][0] * F(9, 25), b[0][1] * F(3, 5), b[0][2] * F(3, 5)],
         [b[1][0] * F(3, 5), b[1][1], b[1][2]],
         [b[2][0] * F(3, 5), b[2][1], b[2][2]]]
    return a, b


def model_331(Nc, Ng=None):
    """beta = -1/sqrt3 (m331_core.model): (groups, fermions, scalars, (Xt, Xa, Qu, Qd, Ng, nA))."""
    return _core.model(Nc, "-1/sqrt3", Ng)


def model_331_plus(Nc, Ng=None):
    """beta = +1/sqrt3: leptons (nu, e, E-) with a heavy charged lepton E (m331_core.model)."""
    return _core.model(Nc, "+1/sqrt3", Ng)


MODELS = {"-1/sqrt3": model_331, "+1/sqrt3": model_331_plus}
_VARIANT = {model_331: "-1/sqrt3", model_331_plus: "+1/sqrt3"}


def anomalies(Nc, model=model_331, Ng=None):
    A = _core.anomalies(Nc, _VARIANT[model], Ng)
    A["SU3L^3 (3 - 3bar)"] = A.pop("SU3L^3")
    return A


def run_two_loop(Nc, mu0=4e3, loops=2, model=model_331, gmax=4 * pi, Ng=None, ainv0=None, rtol=1e-9):
    """ainv0: (1/alpha_X, 1/alpha_L, 1/alpha_3) at mu0, replacing the measured couplings."""
    gs, ferm, scal, _ = model(Nc, Ng)
    a, b = coefficients(gs, ferm, scal)
    a = np.array([float(x) for x in a]); b = np.array([[float(x) for x in r] for r in b])
    L0 = log(mu0 / MZ) / (2 * pi)
    aY_inv = (1 - s2) * ainv - 41 / 6 * L0
    a2_inv = s2 * ainv + 19 / 6 * L0
    from qcd_running import alpha_s_run
    a3_inv = 1 / alpha_s_run(mu0)
    aL_inv = a2_inv
    aX_inv = aY_inv - (1 / 3) * aL_inv                        # 1/g_Y^2 = 1/g_X^2 + beta^2/g_L^2
    if ainv0 is not None:
        aX_inv, aL_inv, a3_inv = ainv0
    g0 = np.sqrt(4 * pi / np.array([aX_inv, aL_inv, a3_inv]))
    if max(g0) >= gmax:
        return mu0, a, b, aX_inv

    def rhs(t, g):
        two = (b @ (g**2)) / (16 * pi**2) if loops == 2 else 0
        return g**3 / (16 * pi**2) * (a + two)

    def blow(t, g):
        return gmax - max(g)                                   # default g = 4 pi: non-perturbative
    blow.terminal = True
    tmax = log(1e40 / mu0)
    sol = solve_ivp(rhs, [0, tmax], g0, events=blow, rtol=rtol, atol=1e-12, max_step=0.5)
    if sol.t_events[0].size:
        return mu0 * np.exp(sol.t_events[0][0]), a, b, aX_inv
    return None, a, b, aX_inv


def main():
    banner("E1  CHECK: general two-loop machinery vs the Standard Model")
    a, b = sm_check()
    print("   one-loop a  =", [str(x) for x in a], "  (expected 41/10, -19/6, -7)")
    for row in b:
        print("   two-loop b  =", [str(x) for x in row])
    print("   expected    = [199/50, 27/10, 44/5] [9/10, 35/6, 12] [11/10, 9/2, -26]")
    exp = [[F(199, 50), F(27, 10), F(44, 5)], [F(9, 10), F(35, 6), F(12)], [F(11, 10), F(9, 2), F(-26)]]
    print(f"   all 9 two-loop entries exact: {b == exp}")

    banner("E2  CHECK: all gauge anomalies vanish for general N_c (exact charges)")
    for Nc in [3, 5, 7]:
        A = anomalies(Nc)
        print(f"   N_c = {Nc}: " + ", ".join(f"{k} = {v}" for k, v in A.items()))

    banner("E3  Two-loop gauge running from 4 TeV: where does a coupling reach g = 4 pi?")
    for Nc in [3, 5, 7]:
        for loops in [1, 2]:
            mp, a, b, aXi = run_two_loop(Nc, loops=loops)
            print(f"   N_c = N_g = {Nc}, {loops}-loop: a = ({a[0]:.2f}, {a[1]:.2f}, {a[2]:.2f})  "
                  f"1/alpha_X(4 TeV) = {aXi:.2f}  ->  "
                  f"{'no blow-up below 1e40 GeV' if mp is None else f'blow-up at {mp:.1e} GeV'}"
                  f"  {'' if mp is None else ('BELOW' if mp < M_PLANCK else 'above') + ' Planck'}")
    aXi = run_two_loop(3)[3]
    a_crit = 2 * pi * aXi / log(M_PLANCK / 4e3)
    print(f"\n   one-loop U(1)_X coefficient that puts the pole exactly at the Planck scale: {a_crit:.2f}")
    for Nc in (3, 5):
        aX = float(coefficients(*model_331(Nc)[:3])[0][0])
        print(f"   N_c = {Nc}: a_X = {aX:.2f}  ->  margin {a_crit - aX:+.2f}")
    print("   (charges and scalar content exact; two-loop Yukawa terms NOT included - they enter only")
    print("    at two loops, while the verdict is already set at one loop with margins of 4.6 and 6.1)")
    print("\n   3-3-1 scale dependence (two-loop):")
    for mu0 in [2e3, 4e3, 1e4, 3e4]:
        res = [run_two_loop(Nc, mu0=mu0)[0] for Nc in (3, 5)]
        print(f"     mu_331 = {mu0/1e3:5.0f} TeV:  N_c = 3 -> "
              f"{'none' if res[0] is None else f'{res[0]:.1e}'}   N_c = 5 -> "
              f"{'none' if res[1] is None else f'{res[1]:.1e}'}")


def variant_plus():
    banner("E4  The other viable variant: beta = +1/sqrt3 (exact charges, two loops)")
    for Nc in [3, 5, 7]:
        A = anomalies(Nc, model_331_plus)
        print(f"   N_c = {Nc} anomalies: " + ", ".join(f"{k} = {v}" for k, v in A.items()))
    for Nc in [3, 5, 7]:
        mp, a, b, aXi = run_two_loop(Nc, model=model_331_plus)
        print(f"   N_c = N_g = {Nc}: a = ({a[0]:.2f}, {a[1]:.2f}, {a[2]:.2f})  ->  "
              f"{'no blow-up below 1e40 GeV' if mp is None else f'blow-up at {mp:.1e} GeV'}"
              f"  {'' if mp is None else ('BELOW' if mp < M_PLANCK else 'above') + ' Planck'}")
    print("   criterion for 'non-perturbative' (blow-up scale, GeV; Planck = 1.2e19):")
    for name, m in MODELS.items():
        for crit, gm in [("g = 4 pi", 4 * pi), ("alpha = 1", sqrt(4 * pi)), ("g = 1 (alpha = 0.08)", 1.0)]:
            r = [run_two_loop(Nc, model=m, gmax=gm)[0] for Nc in (3, 5)]
            print(f"     beta = {name:8s} {crit:22s} N_c = 3: {r[0]:.1e}   N_c = 5: {r[1]:.1e}")
    for mu0 in [2e3, 1e4, 3e4]:
        res = [run_two_loop(Nc, mu0=mu0, model=model_331_plus)[0] for Nc in (3, 5)]
        print(f"     mu_331 = {mu0/1e3:5.0f} TeV:  N_c = 3 -> "
              f"{'none' if res[0] is None else f'{res[0]:.1e}'}   N_c = 5 -> "
              f"{'none' if res[1] is None else f'{res[1]:.1e}'}")


def anomaly_solutions(Nc_max=9, k_max=4):
    """Every (N_c, N_g) with 2 <= N_c <= Nc_max, N_g <= k_max N_c that cancels the SU(3)_L
    anomaly, N_g (1 + N_c) = 2 n N_c. Asymptotic freedom of colour is NOT imposed."""
    return [(Nc, Ng) for Nc in range(2, Nc_max + 1) for Ng in range(1, k_max * Nc + 1)
            if (Ng * (1 + Nc)) % (2 * Nc) == 0]


def survivors(gmax=4 * pi, mus=(2e3, 4e3, 1e4, 3e4), loops=2):
    """Anomaly solutions whose couplings all stay below gmax up to M_Pl, for every 3-3-1
    scale in mus, without requiring asymptotic freedom of colour. {variant: [(N_c, N_g)]}."""
    out = {}
    for name, m in MODELS.items():
        out[name] = []
        for Nc, Ng in anomaly_solutions():
            poles = [run_two_loop(Nc, mu0=mu, model=m, gmax=gmax, Ng=Ng, loops=loops)[0] for mu in mus]
            if all(p is None or p > M_PLANCK for p in poles):
                out[name].append((Nc, Ng))
    return out


def baryon(Nc):
    """The baryons of SU(N_c) colour, N_c quarks each: (is a fermion, the electric charges
    k Q_u + (N_c - k) Q_d for k = 0..N_c). The charges are (1 - N_c)/2 + k: integers
    for odd N_c, half-integers for even N_c."""
    Qu, Qd = F(Nc + 1, 2 * Nc), F(1 - Nc, 2 * Nc)
    return Nc % 2 == 1, [k * Qu + (Nc - k) * Qd for k in range(Nc + 1)]


def aX_per_generation(Nc, variant="-1/sqrt3"):
    """Exact increase of the one-loop U(1)_X coefficient per added generation at fixed N_c
    (N_g -> N_g + 2 N_c for even N_c, + N_c for odd, divided by the step): always positive,
    so more generations only bring the U(1)_X pole down."""
    m = MODELS[variant]
    step = Nc if Nc % 2 else 2 * Nc
    a1 = coefficients(*m(Nc, step)[:3])[0][0]
    a2 = coefficients(*m(Nc, 2 * step)[:3])[0][0]
    return (a2 - a1) / step


def flipped_anomaly(Nc, Ng, n6):
    """SU(3)_L^3 anomaly of a 'flipped' 3-3-1 assignment (Fonseca and Hirsch, JHEP 08 (2016)
    003) for general N_c: every quark generation in the anti-triplet (N_c each), n6 lepton
    generations in the sextet (A(6) = 7 A(3)) and N_g - n6 in the triplet. It vanishes iff
    N_g (N_c - 1) = 6 n6; at N_c = 3 that is N_g = 3 n6. A different relation from
    N_g (1 + N_c) = 2 n N_c: the selection of this note does not cover these models."""
    return -Nc * Ng + 7 * n6 + (Ng - n6)


def colourless(Ng, variant="-1/sqrt3", mu0=4e3):
    """N_c = 1: no colour group, Q_u = 1, Q_d = 0, and the SU(3)_L anomaly puts every 'quark'
    generation in the anti-triplet (n = N_g, any N_g). Returns the exact one-loop
    (a_X, a_L) and the one-loop U(1)_X pole in GeV. Built by hand here as a cross-check of
    MODELS[variant](1, Ng), which run_two_loop and m331_threshold use for the two-loop runs."""
    s = 1 if variant == "-1/sqrt3" else 2                 # leptons X = -s/3, anti-triplet X = +s/3
    ferm = [(Ng, (None, 3), F(-s, 3)), (Ng, (None, 1), F(1)),
            (Ng, (None, 3), F(s, 3)), (Ng, (None, 1), F(-1))]      # the Q = 0 singlets do not run
    if s == 2:
        ferm += [(Ng, (None, 1), F(1)), (Ng, (None, 1), F(-1))]    # E^c and the exotic's partner
    assert sum(m * d[1] * q**3 for m, d, q in ferm) == 0 and sum(m * d[1] * q for m, d, q in ferm) == 0
    X = (F(-1, 3), F(2, 3), F(-1, 3)) if s == 1 else (F(1, 3), F(1, 3), F(-2, 3))
    a, _ = coefficients([Group("X"), Group("SU3L", 3)], ferm, [(1, (None, 3), x) for x in X])
    assert (a[0], a[1]) == tuple(coefficients(*MODELS[variant](1, Ng)[:3])[0][:2])
    aX_inv = run_two_loop(3, mu0=mu0)[3]
    return a[0], a[1], mu0 * np.exp(2 * pi * aX_inv / float(a[0]))


def without_asymptotic_freedom():
    banner("E5  Is asymptotic freedom of colour needed?  The selection without it")
    print("   The SU(3)_L anomaly alone allows N_g = k N_c (N_c odd) and N_g = 2 k N_c (N_c even).")
    print("   Colour's one-loop coefficient is a_3 = -11 N_c/3 + 2 N_g; asymptotic freedom (a_3 < 0)")
    print("   is what cuts these to N_g = N_c. Here it is dropped, and every solution is run to")
    print("   M_Pl (two loops, no Yukawas, 4 TeV, the measured couplings as for every N_c):")
    for name, m in MODELS.items():
        print(f"   beta = {name}")
        for Nc, Ng in [(3, 3), (2, 4), (3, 6), (4, 8), (2, 8), (5, 10)]:
            assert all(v == 0 for v in anomalies(Nc, m, Ng).values())
            mp, a, b, _ = run_two_loop(Nc, model=m, Ng=Ng)
            m1 = run_two_loop(Nc, model=m, Ng=Ng, gmax=sqrt(4 * pi))[0]
            print(f"     N_c = {Nc}, N_g = {Ng:2d}: a = ({a[0]:5.2f}, {a[1]:5.2f}, {a[2]:5.2f})  blow-up "
                  f"{mp:.1e} GeV (g = 4 pi), {m1:.1e} (alpha = 1)  "
                  f"{'above' if mp > M_PLANCK else 'BELOW'} Planck")
    print("   All anomaly solutions with N_c <= 9, N_g <= 4 N_c that reach M_Pl for 3-3-1 scales of")
    print("   2-30 TeV, asymptotic freedom not imposed:")
    for crit, gm in [("g = 4 pi", 4 * pi), ("alpha = 1", sqrt(4 * pi))]:
        for name, sv in survivors(gm).items():
            print(f"     beta = {name:8s} {crit:10s} (N_c, N_g) = {sv}")
    mp, a, _, _ = run_two_loop(2, Ng=4)
    print(f"   -> beta = +1/sqrt3: running alone leaves only (3, 3). beta = -1/sqrt3: (2, 4) also")
    print(f"      reaches M_Pl. Its colour group is not asymptotically free (a_3 = {a[2]:+.2f}), but its")
    print("      pole lies far above M_Pl. Asymptotic freedom of colour is therefore an independent")
    print("      condition of the selection; it is needed only to remove (N_c, N_g) = (2, 4).")
    print("      Every other N_g > N_c is already excluded by the running (U(1)_X, or colour itself).")
    print("   The physical route to the same cut. A baryon is N_c quarks, so its spin is N_c/2 mod 1")
    print("   and its charge is (1 - N_c)/2 + k:")
    for Nc in (2, 3, 4, 5):
        fermion, q = baryon(Nc)
        print(f"     N_c = {Nc}: baryons are {'fermions' if fermion else 'bosons  '} with charges "
              + ", ".join(str(x) for x in q))
    odd = {name: [s for s in sv if s[0] % 2 == 1] for name, sv in survivors().items()}
    print("   Fermionic, integer-charged baryons need N_c odd. Among odd N_c >= 3 the survivors are")
    print(f"     {odd}")
    print("   with asymptotic freedom not imposed: it then follows (a_3 = -5 at N_c = N_g = 3).")
    print("   Beyond the scanned range more generations only lower the pole: d a_X / d N_g = "
          + ", ".join(f"{aX_per_generation(3, n)} (beta = {n})" for n in MODELS) + " at N_c = 3.")
    print("   N_c = 1 (no colour group at all; any N_g cancels the anomalies), one loop:")
    for name in MODELS:
        ok = [Ng for Ng in range(1, 13) if colourless(Ng, name)[2] > M_PLANCK]
        aX, aL, p = colourless(ok[-1], name)
        print(f"     beta = {name}: N_g = {ok[0]}..{ok[-1]} reach M_Pl (N_g = {ok[-1]}: a_X = {aX}, pole {p:.1e} GeV)")
    print("   -> a non-abelian colour group (N_c >= 2) is also a condition, in both variants.")


if __name__ == "__main__":
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    main()
    variant_plus()
    without_asymptotic_freedom()
