#!/usr/bin/env python3
"""
God-equation search, front 5: why N_c = 3 colours?

N_c sets the thirds (front 4), the Z3 twist and the three quarks in a baryon.
Every route is checked for whether it is a THEORETICAL selection or an OBSERVATION.

W1 Witten's global SU(2) anomaly (KNOWN, Witten 1982): even number of doublets.
W2 Perturbative anomaly cancellation + Yukawas for general N_c (KNOWN; Baer & Wiese 2001):
   solve for hypercharges symbolically.
W3 Spin-charge relation of front 4 for general N_c: (-1)^F = exp(i pi N_c (B-L)).
W4 Asymptotic freedom with 6 flavours (KNOWN): b0 = 11 N_c/3 - 2 n_f/3 > 0.
W5 The minimal fold of front 4 for general N_c: does it select a value?
W6 Observables with anomaly-consistent, N_c-dependent charges:
   pi0 -> gamma gamma amplitude ~ N_c (Q_u^2 - Q_d^2);
   R = sigma(ee->hadrons)/sigma(ee->mu mu) below charm = N_c (Q_u^2 + 2 Q_d^2)(1 + 3 C_F alpha_s/4pi),
   vs KEDR (LIT): R = 2.225 +- 0.051 averaged over 1.84-3.05 GeV.
"""
import os
import sys
import sympy as sp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


def charges(Nc):
    """Solve anomaly + Yukawa conditions for one generation (left-handed Weyl fields):
    Q (Nc,2,YQ), u^c (Nc_bar,1,-Yu), d^c (Nc_bar,1,-Yd), L (1,2,YL), e^c (1,1,-Ye); Higgs YH."""
    YQ, Yu, Yd, YL, Ye, YH = sp.symbols("YQ Yu Yd YL Ye YH")
    eqs = [
        sp.Eq(2 * YQ - Yu - Yd, 0),                          # [SU(Nc)]^2 U(1)
        sp.Eq(Nc * YQ + YL, 0),                              # [SU(2)]^2 U(1)
        sp.Eq(Nc * (2 * YQ - Yu - Yd) + 2 * YL - Ye, 0),     # grav^2 U(1)
        sp.Eq(Yu, YQ + YH), sp.Eq(Yd, YQ - YH), sp.Eq(Ye, YL - YH),   # Yukawa couplings exist
        sp.Eq(YL, sp.Rational(-1, 2)),                       # normalisation: Q_e = -1, Q_nu = 0
    ]
    sol = sp.solve(eqs, [YQ, Yu, Yd, YL, Ye, YH], dict=True)[0]
    cubic = sp.simplify(Nc * (2 * sol[YQ]**3 - sol[Yu]**3 - sol[Yd]**3) + 2 * sol[YL]**3 - sol[Ye]**3)
    Qu, Qd = sol[Yu], sol[Yd]                                # T3 = 0 components
    return sp.nsimplify(Qu), sp.nsimplify(Qd), cubic


def main():
    Ns = [1, 2, 3, 4, 5, 7]
    banner("W1  Witten global anomaly: doublets per generation = N_c + 1 must be even")
    for Nc in Ns:
        print(f"   N_c = {Nc}:  doublets = {Nc+1}  -> {'allowed' if (Nc+1) % 2 == 0 else 'ANOMALOUS'}")
    print("   -> THEORY: N_c must be odd.")

    banner("W2  Anomaly cancellation for general N_c (charges come out N_c-dependent)")
    for Nc in Ns:
        Qu, Qd, cub = charges(Nc)
        print(f"   N_c = {Nc}:  Q_u = {str(Qu):6s} Q_d = {str(Qd):6s}  cubic anomaly residual = {cub}")
    Ncs = sp.symbols("N_c", positive=True)
    Qu, Qd, cub = charges(Ncs)
    print(f"   general:  Q_u = {sp.simplify(Qu)},  Q_d = {sp.simplify(Qd)},  cubic residual = {sp.simplify(cub)}")
    print("   -> every N_c cancels all perturbative anomalies: they fix the CHARGES given N_c, not N_c.")

    banner("W3  Spin-charge relation (front 4) for general N_c: (-1)^F = exp(i pi N_c (B-L))")
    for Nc in Ns:
        q = (-1) ** 1                                        # quark B-L = 1/N_c -> exp(i pi) = -1
        lep = (-1) ** Nc                                     # lepton B-L = -1
        print(f"   N_c = {Nc}:  quark {q:+d}, lepton {lep:+d}  -> {'consistent' if lep == -1 else 'FAILS'}")
    print("   -> same condition as W1 (N_c odd): the twist and Witten's anomaly agree.")

    banner("W4  Asymptotic freedom with n_f = 6")
    for Nc in Ns:
        b0 = sp.Rational(11 * Nc, 3) - sp.Rational(2 * 6, 3) if Nc > 1 else None
        print(f"   N_c = {Nc}:  b0 = {b0 if b0 is not None else 'no gauge group (no strong force)'}")
    print("   -> only a LOWER bound (N_c >= 2, i.e. a strong force exists at all). No upper bound.")

    banner("W5  Minimal combined fold (front 4) for general N_c")
    for Nc in Ns:
        k, m = Nc - 1, 1                                     # colour twist k, B-L flux 2 pi m
        nq, nl = (k + m) // Nc, -m
        print(f"   N_c = {Nc}:  k = {k}, m = 1  ->  quark J = {sp.Rational(nq, 2)}, lepton J = {sp.Rational(abs(nl), 2)}")
    print("   -> works for EVERY N_c: the fold does not select 3.")

    banner("W6  Observables with anomaly-consistent charges")
    from stur_open_problems import alpha_s_run
    a_s = alpha_s_run(2.45)                                  # mid-point of the KEDR range (3 light flavours produced)
    print(f"   alpha_s(2.45 GeV) = {a_s:.3f} (2-loop, our running from alpha_s(M_Z) = 0.118)")
    print("   N_c   pi0->gg ~ N_c(Qu^2-Qd^2)    R(u,d,s)     R vs KEDR 2.225 +- 0.051")
    for Nc in Ns:
        Qu, Qd, _ = charges(Nc)
        amp = Nc * (Qu**2 - Qd**2)
        CF = sp.Rational(Nc**2 - 1, 2 * Nc)
        R = float(Nc * (Qu**2 + 2 * Qd**2)) * (1 + 3 * float(CF) * a_s / (4 * 3.141592653589793))
        print(f"   {Nc:3d}   {str(sp.nsimplify(amp)):26s}  {R:8.3f}     {(R-2.225)/0.051:+7.1f} sigma")
    print("   -> pi0 -> gamma gamma cannot see N_c (KNOWN, Baer-Wiese). The R-ratio can: only N_c = 3 fits.")
    print("   (alpha_s would itself change with N_c; the N_c = 5 miss is 33 sigma, far beyond that.)")


if __name__ == "__main__":
    main()
