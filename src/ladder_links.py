#!/usr/bin/env python3
"""
Links between the rungs of the symmetry-breaking ladder (SYMMETRY_LADDER.md): places where one
rung's output is another rung's input, checked against a measurement.

L1  Neutral matter: rung 1 -> rung 4. The diamond experiment needs the Coulomb force between
    the diamonds to vanish far more precisely than any discharging can arrange. That rests on
    q_p + q_e = 0, which is an anomaly condition of rung 1.
  L1a For any beta, any N_c and any U(1)_X charges of the lepton triplet (X_L) and the quark
      triplet (X_t), with the anti-triplet's X_a = X_t + beta/sqrt3 (so u and d carry the
      same charge in both, as the W couplings and the quark mixing require) and the SU(3)_L^3
      count N_g(1 + N_c) = 2 n N_c:
          q_p + q_e   = [SU(3)_L]^2 U(1)_X anomaly / N_g        (identically)
          q_n + Q_nu  = q_p + q_e                               (identically: n -> p e nubar)
      so the anomaly makes the hydrogen atom neutral and q_n = -Q_nu; Q_nu = 0 is part of
      rung 1's charge assignment (L1b; in 3-3-1 the X^3 and grav^2 X anomalies with the
      Yukawas fix it, de S. Pires-Ravinez 1998, not re-derived here).
      A proton is the N_c-quark baryon with (N_c+1)/2 u and (N_c-1)/2 d. The same holds in
      the Standard Model with [SU(2)_L]^2 U(1)_Y: q_p + q_e = N_c Y_Q + Y_L. (CHECK,
      symbolic; KNOWN in substance: charge quantization from anomalies, Geng-Marshak,
      Babu-Mohapatra 1989; in 3-3-1, de S. Pires-Ravinez, PRD 58, 035008 (1998))
  L1b With rung 1's charges (src/m331_breaking.py B6): q_p = 1, q_n = 0, q_e = -1 exactly,
      for N_c = 3, 5, 7 and both variants. So neutral matter does not select N_c. (CHECK)
  L1c The size of the requirement. Coulomb and gravity are both 1/r and act along the same
      branch trajectories, so their entangling phases are in the exact ratio
      -k Q^2 / (G m^2). Coulomb below 10% of gravity needs a residual charge per nucleon
          delta < sqrt(0.1 G / k) u / e = 2.8e-19 e,
      for any diamond size (m and the nucleon count scale together). One stray electron gives
      1.6e10 x gravity (src/stur_gravity_full.py H6); discharging removes whole electrons but
      cannot remove a fractional charge per atom, which in design A totals < 1e-6 e. (CHECK)
  L1d Measured: |q_p + q_e| < 1e-21 e (Bressi et al., PRA 83, 052101 (2011)), the same limit
      for q_n; q_n = (-0.4 +- 1.1)e-21 e (Baumann et al., PRD 37, 3107 (1988)). The margin is
      about 280; rung 1 says the residual is exactly zero. (CHECK; LIT bounds)

L2  pi0 -> gamma gamma: rung 1 -> rung 2. The neutral pion of rung 2 decays through the chiral
    anomaly, with amplitude A = (alpha / pi f_pi) N_c (Q_u^2 - Q_d^2) (LIT: Adler; Bell-Jackiw
    1969, the anomaly coefficient quoted, not derived).
  L2a With rung 1's anomaly-fixed charges, N_c (Q_u^2 - Q_d^2) = 1 for every N_c. (CHECK)
  L2b The width from the amplitude M = A eps^{mu nu rho sigma} e1_mu e2_nu k1_rho k2_sigma: the
      polarization sum gives sum |M|^2 = A^2 m^4 / 2, and two-body phase space with identical
      photons gives Gamma = A^2 m^3 / (64 pi). (CHECK, symbolic)
  L2c With rung 2's f_pi = 92.07 MeV and alpha(0): Gamma = 7.79 eV, against the PrimEx-I+II
      average 7.802 +- 0.117 eV (Larin et al., Science 368, 506 (2020)). (CHECK; LIT)
  L2d What it does and does not test: the width checks that charges and colours come together
      as anomaly cancellation demands. With the charges held at 2/3 and -1/3 instead, the width
      would scale as (N_c/3)^2. With anomaly-fixed charges it cannot select N_c; the R-ratio
      can (src/m331_why_three.py W6). (FOLLOWS)
L3  The Planck mass: rung 4 -> rung 1. The 3-3-1 selection asks every coupling to stay
    perturbative up to M_Pl, and its scripts type M_Pl as a number. It is sqrt(hbar c / G):
    the same G that gives the diamonds' 2.19 rad phase (DEPENDENCIES.md found the shared input).
  L3a M_Pl from rung 4's G, hbar and c (src/stur_gravity_entanglement.py, the values
      src/graviton_exchange.py uses) equals the cutoff of src/m331_exact.py to 1e-6. (CHECK)
  L3b How much the selection leans on G. M_Pl scales as G^(-1/2), so with G -> x G the
      selection holds while (M_Pl / pole_3)^2 < x < (M_Pl / pole_5)^2. At the reference
      spectrum (M_V = 4 TeV, Yukawas and thresholds on, alpha = 1, three loops,
      src/m331_three_loop.py): beta = +1/sqrt3 holds for 0.12 < x < 6e14, beta = -1/sqrt3 for
      3e-21 < x < 1e8. G is measured to 2.2e-5 (CODATA 2018). The narrow side is
      beta = +1/sqrt3: with G 8.2x weaker, M_Pl would rise above N_c = 3's pole and exclude
      it. (CHECK)
  L3c At the mass floors with light heavy leptons (NOTE_331.md section 3e), N_c = 3 fails at
      the measured G (0.61 M_Pl); it would pass only if G were 2.7x stronger. The heavy-lepton
      condition is the statement there; this only restates it in terms of G. (CHECK)
  L3d What it assumes: G measured at laboratory and solar-system distances is used at
      10^19 GeV, i.e. gravity's strength does not run in between. In perturbative quantum
      gravity the corrections are of order (E/M_Pl)^2; many hidden light species would lower
      the effective cutoff, which this check does not cover. (FOLLOWS)
  L3e The window over the heavy spectrum. L3b uses one reference spectrum. Over the
      threshold scan of NOTE_331.md section 3a (r_J, r_S, M_V, light doublets: 72 points,
      src/m331_threshold.py GRID), beta = +1/sqrt3's N_c = 3 pole runs from 1.26 to 16 M_Pl,
      so the lower edge of the window runs from x = 0.004 to 0.63. At the scan's worst point
      (M_V = 2 TeV, r_J = 0.5, r_S = 1/3, two light doublets) the selection fails for G only
      1.6x weaker. The upper edge (N_c = 5) and beta = -1/sqrt3 stay many orders of magnitude
      away. So L3b's 8.2x is the reference spectrum's margin, not the model's. (CHECK)
  L3f Gravity's own term in the gauge running at M_Pl (src/m331_gravity_fixed_point.py). With
      the gravity contribution set to the strength that keeps the Standard Model's
      hypercharge finite (f* = 0.0098 at G* = 1, the benchmark of G2 there), the reference
      pole moves from 2.86 to 2.94 M_Pl and the worst-case pole from 1.26 to 1.27 M_Pl: 3%
      or less, against the factor of 13 that the spectrum spans. The threshold spectrum, not
      gravity's running, sets how close the edge comes. (CHECK, given that model)
Labels: CHECK, FOLLOWS, KNOWN, LIT, MODEL (L3f's gravity term).
"""
import functools
import math
import os
import sys
from itertools import product

import sympy as sp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# measured inputs
G_NEWTON = 6.67430e-11              # CODATA 2018 (as in src/stur_gravity_entanglement.py)
K_COUL = 8.9875517923e9             # 1 / (4 pi eps0)
E_CH = 1.602176634e-19              # C
U_AMU = 1.66053906660e-27           # kg; carbon-12 has exactly 12 u for 12 nucleons
ALPHA_0 = 1 / 137.035999084         # fine-structure constant at q^2 = 0 (real photons)
EPS_PE_BOUND = 1e-21                # |q_p + q_e| / e, Bressi et al. 2011 (same limit for q_n)
Q_N_MEAS = (-0.4e-21, 1.1e-21)      # q_n / e, Baumann et al. 1988
GAMMA_PI0_MEAS = (7.802, math.hypot(0.052, 0.105))   # eV, PrimEx-I+II (Larin et al. 2020)
FRAC = 0.1                          # "below 10% of gravity", as for the Casimir gap


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


# ---------------------------------------------------------------------------------- L1
def baryon_charges(Qu, Qd, Nc):
    """N_c-quark proton and neutron: (N_c+1)/2 u + (N_c-1)/2 d, and the reverse."""
    up, dn = (Nc + 1) / sp.Integer(2), (Nc - 1) / sp.Integer(2)
    return sp.simplify(up * Qu + dn * Qd), sp.simplify(dn * Qu + up * Qd)


def neutrality_identity():
    """L1a in 3-3-1: returns (q_p + q_e - anomaly/N_g, q_n + Q_nu - (q_p + q_e)), both identically 0."""
    Nc, beta, XL, Xt, Ng, n = sp.symbols("N_c beta X_L X_t N_g n")
    b = beta / (2 * sp.sqrt(3))                          # beta T8 on the first two components
    Xa = Xt + beta / sp.sqrt(3)
    Qu, Qd = sp.Rational(1, 2) + b + Xt, -sp.Rational(1, 2) + b + Xt          # triplet (u, d, J)
    same = (sp.simplify(sp.Rational(1, 2) - b + Xa - Qu),                       # anti-triplet (d, -u, J'):
            sp.simplify(-sp.Rational(1, 2) - b + Xa - Qd))                      # Q = -T3 - beta T8 + X_a
    Qnu, Qe = sp.Rational(1, 2) + b + XL, -sp.Rational(1, 2) + b + XL
    anomaly = Ng * XL + Nc * ((Ng - n) * Xt + n * Xa)    # [SU(3)_L]^2 U(1)_X, all triplets index 1/2
    anomaly = sp.simplify(anomaly.subs(n, Ng * (1 + Nc) / (2 * Nc)))
    qp, qn = baryon_charges(Qu, Qd, Nc)
    d1 = sp.simplify(qp + Qe - anomaly / Ng)
    d2 = sp.simplify(qn + Qnu - (qp + Qe))
    return d1, d2, same


def neutrality_identity_sm():
    """L1a in the Standard Model: q_p + q_e = N_c Y_Q + Y_L, the [SU(2)_L]^2 U(1)_Y anomaly."""
    Nc, YQ, YL = sp.symbols("N_c Y_Q Y_L")
    Qu, Qd = YQ + sp.Rational(1, 2), YQ - sp.Rational(1, 2)
    Qnu, Qe = YL + sp.Rational(1, 2), YL - sp.Rational(1, 2)
    qp, qn = baryon_charges(Qu, Qd, Nc)
    return sp.simplify(qp + Qe - (Nc * YQ + YL)), sp.simplify(qn + Qnu - (qp + Qe))


def rung1_matter_charges():
    """L1b: q_p, q_n, q_e from rung 1's component charges (src/m331_breaking.py B6)."""
    import m331_breaking as B
    out = {}
    for variant in ("-1/sqrt3", "+1/sqrt3"):
        for Nc in (3, 5, 7):
            rows, ok, (Qu, Qd) = B.charges(variant, Nc)
            lep = [q for kind, _, q in rows if kind == "lepton triplet"][0]
            Qnu, Qe = (lep[0], lep[1]) if lep[0] == 0 else (lep[1], lep[0])
            qp, qn = baryon_charges(Qu, Qd, Nc)
            out[(variant, Nc)] = (qp, qn, Qe, Qnu, ok)
    return out


def coulomb_vs_gravity():
    """L1c, L1d on design A (src/graviton_exchange.py N4)."""
    import graviton_exchange as GX
    dphi_grav, _, _, (m, dx, gap, hold, ramp) = GX.branch_phases()
    nucleons = m / U_AMU
    ratio = lambda Q: K_COUL * Q**2 / (G_NEWTON * m**2)          # |Coulomb / gravity| phase
    Qmax = math.sqrt(FRAC * G_NEWTON / K_COUL) * m               # C
    delta_max = Qmax / E_CH / nucleons                           # per nucleon, in e
    # carbon-12 atom: 6 (q_p + q_e) + 6 q_n; per nucleon (eps_pe + q_n) / 2
    delta_meas = (EPS_PE_BOUND + EPS_PE_BOUND) / 2
    return dict(m=m, dphi_grav=dphi_grav, nucleons=nucleons, one_electron=ratio(E_CH),
                Qmax_e=Qmax / E_CH, delta_max=delta_max, delta_meas=delta_meas,
                margin=delta_max / delta_meas, ratio_at_bound=ratio(delta_meas * E_CH * nucleons),
                residual_total_e=delta_meas * nucleons,
                size_independent=math.sqrt(FRAC * G_NEWTON / K_COUL) * U_AMU / E_CH)


# ---------------------------------------------------------------------------------- L2
def anomaly_factor():
    """L2a: N_c (Q_u^2 - Q_d^2) with the anomaly-fixed charges, from both rung-1 derivations."""
    import m331_why_three as W
    import m331_breaking as B
    out = {}
    for Nc in (1, 2, 3, 4, 5, 7):
        Qu, Qd, _ = W.charges(Nc)
        out[Nc] = sp.nsimplify(Nc * (Qu**2 - Qd**2))
    agree = all(B.charges(v, Nc)[2] == tuple(sp.nsimplify(x) for x in W.charges(Nc)[:2])
                for v in ("-1/sqrt3", "+1/sqrt3") for Nc in (3, 5, 7))
    Ncs = sp.symbols("N_c", positive=True)
    Qu, Qd, _ = W.charges(Ncs)
    general = sp.simplify(Ncs * (Qu**2 - Qd**2))
    return out, general, agree


def two_photon_width():
    """L2b: pseudoscalar at rest -> k1 = (m/2)(1,0,0,1), k2 = (m/2)(1,0,0,-1); physical
    (transverse) polarizations x, y for each photon; eps^{0123} = +1, metric (+,-,-,-)."""
    A, m = sp.symbols("A m", positive=True)
    k1 = [m / 2, 0, 0, m / 2]
    k2 = [m / 2, 0, 0, -m / 2]
    pols = [[0, 1, 0, 0], [0, 0, 1, 0]]
    low = lambda v: [v[0], -v[1], -v[2], -v[3]]
    total = 0
    for e1 in pols:
        for e2 in pols:
            a, b, c, d = low(e1), low(e2), low(k1), low(k2)
            M = A * sum(sp.LeviCivita(i, j, k, l) * a[i] * b[j] * c[k] * d[l]
                        for i in range(4) for j in range(4) for k in range(4) for l in range(4))
            total += sp.expand(M * sp.conjugate(M))
    msq = sp.simplify(total)
    p = m / 2                                             # photon momentum in the rest frame
    width = sp.simplify(sp.Rational(1, 2) * p / (8 * sp.pi * m**2) * msq)   # 1/2: identical photons
    return msq, width, A, m


def pi0_width():
    """L2c: Gamma(pi0 -> gamma gamma) from rung 1's charges and rung 2's f_pi."""
    import chiral_breaking as CB
    msq, width, A, m = two_photon_width()
    amp = ALPHA_0 / (math.pi * CB.F_PI) * 1                     # N_c (Q_u^2 - Q_d^2) = 1 (L2a)
    G = float(width.subs({A: amp, m: CB.M_PI0})) * 1e9          # GeV -> eV
    meas, err = GAMMA_PI0_MEAS
    fixed = {Nc: G * (Nc / 3) ** 2 for Nc in (3, 5, 7)}         # L2d: charges held at 2/3, -1/3
    return G, (G - meas) / err, CB.F_PI, fixed


# ---------------------------------------------------------------------------------- L3
def planck_mass():
    """L3a: sqrt(hbar c / G) in GeV from rung 4's constants, against the 3-3-1 cutoff."""
    import stur_gravity_entanglement as GE
    import m331_exact as E
    mpl = math.sqrt(GE.HBAR * GE.C / GE.G) * GE.C**2 / E_CH / 1e9
    return mpl, E.M_PLANCK, (GE.G, GE.HBAR, GE.C)


def g_window():
    """L3b-c: the factor x (G -> x G) over which the selection survives, from the poles in
    units of the measured M_Pl."""
    import m331_three_loop as T3
    import m331_margin as M
    mpl = planck_mass()[1]
    out = {}
    for v in ("+1/sqrt3", "-1/sqrt3"):
        p3 = T3.pole(3, v, MV=4e3, gmax=M.ALPHA1) / mpl
        p5 = T3.pole(5, v, MV=4e3, gmax=M.ALPHA1) / mpl
        out[v] = (p3, p5, 1 / p3**2, 1 / p5**2)
    floor = M.pole(**M.FLOORS, loops=3, gmax=M.ALPHA1) / mpl
    return out, floor, 1 / floor**2


@functools.lru_cache(maxsize=None)
def g_window_scan():
    """L3e: the N_c = 3 and N_c = 5 poles (units of M_Pl) over the threshold scan grid,
    as (min, max, spectrum at min, spectrum at max) per (variant, N_c), and the window edges
    that follow: x from 1 / max(p3)^2 to 1 / min(p3)^2 on the low side."""
    import m331_three_loop as T3
    import m331_threshold as T
    import m331_margin as M
    mpl = planck_mass()[1]
    grid = list(product(T.GRID["rJ"], T.GRID["rS"], T.GRID["MV"], T.GRID["n_light"]))
    out = {}
    for v in ("+1/sqrt3", "-1/sqrt3"):
        for Nc in (3, 5):
            vals = [(T3.pole(Nc, v, MV, rJ, rS, nl, gmax=M.ALPHA1) / mpl, (rJ, rS, MV, nl))
                    for rJ, rS, MV, nl in grid]
            lo, hi = min(vals), max(vals)
            out[v, Nc] = (lo[0], hi[0], lo[1], hi[1])
    return out, len(grid)


@functools.lru_cache(maxsize=None)
def gravity_shift():
    """L3f: beta = +1/sqrt3, N_c = 3 poles (units of M_Pl) with and without the
    asymptotic-safety gravity term at the Standard Model hypercharge's separatrix f*
    (G* = 1), at the reference spectrum and at the scan's worst point."""
    import m331_three_loop as T3
    import m331_margin as M
    import m331_gravity_fixed_point as GFP
    mpl = planck_mass()[1]
    f_sm = GFP.f_separatrix_sm(1.0)
    grav = GFP.f_profile(f_sm, 1.0)
    rows = {}
    for lab, spec in (("reference", dict(MV=4e3)), ("worst", T3.WORST)):
        p0 = T3.pole(3, "+1/sqrt3", gmax=M.ALPHA1, **spec) / mpl
        pg = T3.pole(3, "+1/sqrt3", gmax=M.ALPHA1, grav=grav, **spec) / mpl
        rows[lab] = (p0, pg)
    return f_sm, rows


def main():
    banner("L1a  Neutral matter is an anomaly condition (CHECK, symbolic; any beta, N_c, X)")
    d1, d2, same = neutrality_identity()
    print(f"   u, d charges agree between triplet and anti-triplet when X_a = X_t + beta/sqrt3: {same == (0, 0)}")
    print(f"   3-3-1:  (q_p + q_e) - [SU(3)_L]^2 U(1)_X / N_g = {d1};   (q_n + Q_nu) - (q_p + q_e) = {d2}")
    s1, s2 = neutrality_identity_sm()
    print(f"   SM:     (q_p + q_e) - [SU(2)_L]^2 U(1)_Y = (q_p + q_e) - (N_c Y_Q + Y_L) = {s1};"
          f"   (q_n + Q_nu) - (q_p + q_e) = {s2}")
    print("   -> the hydrogen atom is neutral exactly when the mixed SU(3)_L (or SU(2)_L) anomaly")
    print("      cancels, for any N_c; then q_n = -Q_nu (beta decay), and Q_nu = 0 in rung 1 (L1b).")

    banner("L1b  Rung 1's charges (src/m331_breaking.py B6): matter is exactly neutral")
    for (variant, Nc), (qp, qn, qe, qnu, ok) in rung1_matter_charges().items():
        print(f"   beta = {variant:8s} N_c = {Nc}:  q_p = {qp}, q_n = {qn}, q_e = {qe}, Q_nu = {qnu}"
              f"  -> q_p + q_e = {qp + qe}")
    print("   -> neutral matter holds for every N_c: like pi0 -> gamma gamma, it does not select 3.")

    banner("L1c-d  How neutral the diamonds must be (design A, src/graviton_exchange.py N4)")
    c = coulomb_vs_gravity()
    print(f"   design A: m = {c['m']:.4e} kg = {c['nucleons']:.3e} nucleons; gravity's phase {c['dphi_grav']:.4f} rad")
    print(f"   Coulomb and gravity are both 1/r on the same trajectories: phase ratio = -k Q^2 / (G m^2)")
    print(f"   one stray electron on each diamond: {c['one_electron']:.2e} x gravity"
          "  (src/stur_gravity_full.py H6: 1.6e10)")
    print(f"   Coulomb < {FRAC:.0%} of gravity: net charge < {c['Qmax_e']:.2e} e per diamond,")
    print(f"     i.e. < {c['delta_max']:.2e} e per nucleon = sqrt(0.1 G/k) u/e = {c['size_independent']:.2e} e"
          " for any diamond size")
    print(f"   LIT: |q_p + q_e| < 1e-21 e (Bressi et al. 2011), same for q_n;"
          f" q_n = ({Q_N_MEAS[0] / 1e-21:+.1f} +- {Q_N_MEAS[1] / 1e-21:.1f})e-21 e (Baumann et al. 1988)")
    print(f"   residual per nucleon at those bounds: <= {c['delta_meas']:.1e} e -> margin {c['margin']:.0f};"
          f" Coulomb/gravity <= {c['ratio_at_bound']:.1e}")
    print(f"   that residual totals <= {c['residual_total_e']:.1e} e per diamond: less than one electron,")
    print("   so discharging cannot reach it. The experiment needs charge quantized at the atomic level;")
    print("   measurement gives it to 1e-21, rung 1's anomaly cancellation gives it exactly.")

    banner("L2a  pi0 -> gamma gamma: the anomaly factor with rung 1's charges (CHECK)")
    out, general, agree = anomaly_factor()
    print("   " + ",  ".join(f"N_c = {k}: {v}" for k, v in out.items()) + f";  general N_c: {general}")
    print(f"   (src/m331_why_three.py W2 and src/m331_breaking.py B6 give the same Q_u, Q_d: {agree})")

    banner("L2b  The width from the anomaly amplitude (CHECK, symbolic)")
    msq, width, A, m = two_photon_width()
    print(f"   sum over polarizations |A eps(e1, e2, k1, k2)|^2 = {msq}")
    print(f"   Gamma = (1/2) |p| / (8 pi m^2) x sum |M|^2 = {width}")

    banner("L2c-d  Against PrimEx (rung 2's f_pi, alpha(0); LIT anomaly coefficient)")
    G, pull, fpi, fixed = pi0_width()
    meas, err = GAMMA_PI0_MEAS
    print(f"   A = alpha N_c (Q_u^2 - Q_d^2) / (pi f_pi), f_pi = {fpi * 1e3:.2f} MeV (src/chiral_breaking.py)")
    print(f"   Gamma(pi0 -> gamma gamma) = {G:.3f} eV;  PrimEx-I+II {meas:.3f} +- {err:.3f} eV  ({pull:+.1f} sigma)")
    print("   with the charges held at 2/3, -1/3 instead: " + ",  ".join(
        f"N_c = {k}: {v:.2f} eV" for k, v in fixed.items()))
    print("   -> the width tests that charges and colours come together as anomaly cancellation")
    print("      demands. It cannot select N_c; the R-ratio does (src/m331_why_three.py W6).")

    banner("L3a  The Planck mass: the 3-3-1 cutoff from rung 4's G (CHECK)")
    mpl, mpl331, (G, hb, c) = planck_mass()
    print(f"   rung 4 (src/stur_gravity_entanglement.py): G = {G:.5e}, hbar = {hb:.9e}, c = {c:.0f}")
    print(f"   sqrt(hbar c / G) = {mpl:.6e} GeV;  src/m331_exact.py M_PLANCK = {mpl331:.6e} GeV"
          f"  (ratio - 1 = {mpl / mpl331 - 1:+.1e})")

    banner("L3b-c  How far G could move before the selection changes (alpha = 1, three loops)")
    out, floor, x_floor = g_window()
    print("   G -> x G moves M_Pl by x^(-1/2); the selection holds for (M_Pl/pole_3)^2 < x < (M_Pl/pole_5)^2")
    for v, (p3, p5, lo, hi) in out.items():
        print(f"   beta = {v:8s} reference spectrum: N_c = 3 pole {p3:.3g} M_Pl, N_c = 5 pole {p5:.2g} M_Pl"
              f"  ->  {lo:.2g} < x < {hi:.2g}")
    print(f"   G is measured to 2.2e-5 (CODATA 2018). The narrow side: beta = +1/sqrt3 with G"
          f" {1 / out['+1/sqrt3'][2]:.1f}x weaker.")
    print(f"   at the mass floors with light heavy leptons (NOTE_331.md 3e): N_c = 3 pole {floor:.2f} M_Pl,"
          f" so it would need G {x_floor:.1f}x stronger")
    print("   -> the selection's cutoff and the diamonds' signal share one measured G. The selection")
    print("      assumes G does not run between the laboratory and 10^19 GeV.")

    banner("L3e  The same window over the threshold scan (NOTE_331.md 3a; alpha = 1, three loops)")
    scan, n = g_window_scan()
    print(f"   {n} spectra: r_J, r_S, M_V, light doublets (src/m331_threshold.py GRID)")
    for v in ("+1/sqrt3", "-1/sqrt3"):
        p3lo, p3hi, s3lo, _ = scan[v, 3]
        p5lo, p5hi, _, _ = scan[v, 5]
        print(f"   beta = {v:8s} N_c = 3 pole {p3lo:.3g} - {p3hi:.3g} M_Pl, N_c = 5 pole {p5lo:.2g} - {p5hi:.2g} M_Pl")
        print(f"      lower edge {1 / p3hi**2:.2g} - {1 / p3lo**2:.2g},  upper edge {1 / p5hi**2:.2g} - {1 / p5lo**2:.2g}")
    p3lo, _, (rJ, rS, MV, nl), _ = scan["+1/sqrt3", 3]
    print(f"   worst point (beta = +1/sqrt3): r_J = {rJ}, r_S = {rS:.3g}, M_V = {MV:.0f} GeV, {nl} light doublets:")
    print(f"      the selection fails for G {p3lo**2:.2f}x weaker (reference spectrum: {out['+1/sqrt3'][0]**2:.1f}x)")

    banner("L3f  Gravity's term in the gauge running (src/m331_gravity_fixed_point.py; MODEL)")
    f_sm, rows = gravity_shift()
    print(f"   f* = {f_sm:.4f}, G* = 1: the strength that keeps the SM hypercharge finite (G2 there)")
    for lab, (p0, pg) in rows.items():
        print(f"   beta = +1/sqrt3, N_c = 3, {lab:9s} spectrum: pole {p0:.3f} -> {pg:.3f} M_Pl  ({pg / p0 - 1:+.1%})")
    spread = scan["+1/sqrt3", 3][1] / scan["+1/sqrt3", 3][0]
    print(f"   -> a few percent, against the factor {spread:.0f} the threshold spectrum spans: the heavy")
    print("      spectrum, not gravity's running, sets how close N_c = 3's pole comes to M_Pl.")


if __name__ == "__main__":
    main()
