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
L6  The diamond's mass: rung 2 -> rung 4. The mass that sources design A's phase is almost
    entirely QCD binding energy, not Higgs-generated mass.
  L6a Carbon-12: 6 m_p + 6 m_n + 6 m_e - 12 u = 92.16 MeV, the binding of the nucleus (and,
      at the keV level, of the electrons), exact from CODATA 2018 because 12 u is the mass
      of the atom by definition. It is the residual strong force minus the protons' Coulomb
      repulsion. (CHECK; LIT)
  L6b Each nucleon, by the Feynman-Hellmann theorem (FLAG 2024 eq. fheq1): the light-quark
      masses contribute sigma_piN = m_ud <N|ubar u + dbar d|N> and the strange quark
      sigma_s; N_f = 2+1 lattice averages 42.2(2.4) and 44.9(6.4) MeV (FLAG 2024; the
      N_f = 2+1+1 averages, 60.9(6.5) and 41.0(8.8), are carried as the systematic spread).
      The rest of M_N is gluon field energy and quark motion. The electron's mass is all
      Higgs. Heavy-quark contributions to M_N (through the trace anomaly) are counted with
      QCD here. (CHECK; LIT)
  L6c Design A's diamond: 91% QCD field energy, 9.3% the Higgs-generated quark masses
      (4.5% u, d; 4.8% s), 0.03% electrons, -0.8% nuclear binding. (CHECK)
  L6d What rung 4 inherits: the phase goes as m^2, so with massless u and d quarks (first
      order in sigma_piN, strange quark kept) the same diamonds would give 1.99 rad instead
      of 2.19, and with every quark and the electron massless 1.80 rad. The entanglement
      survives a world without the Higgs mechanism's light-fermion masses; what the
      experiment weighs is QCD. (FOLLOWS, first order)
L7  A black hole evaporating back through the forces: rung 6 -> rungs 3, 2, 1 and link 3.
    (Design A's diamond itself cannot be the hole: at 1.5e-14 kg it is 1e-6 of the Planck
    mass, below any semiclassical black hole.) An evaporating hole heats up as it shrinks,
    T_H = hbar c^3 / (8 pi G M k_B), and its emission grows with the species lighter than T_H.
  L7a Mass loss (LIT: Carr, Kohri, Sendouda and Yokoyama, Rept. Prog. Phys. 84, 116902
      (2021), arXiv:2002.12778, eqs. (11)-(13)): dM/dt = -5.34e25 f(M) / M^2 g^3/s, f a sum
      over emitted degrees of freedom with weights 0.267 (spin 0), 0.147 (neutral 1/2),
      0.142 (charged 1/2), 0.060 (1), 0.007 (2). T_H at 1e10 g is 1.058 TeV from the
      formula above, their 1.06 TeV. (CHECK)
  L7b Rung 1's particle content gives f. Below every mass: photons, neutrinos and gravitons,
      f = 1.016 (their "unity"). Every Standard Model species: f = 15.33, against their
      15.35, and only if the W and Z longitudinal modes, the Goldstones the Higgs mechanism
      gives them, count as scalars. The same count in the unbroken phase (12 gauge bosons,
      4 Higgs scalars) gives 15.33 identically. Above the 3-3-1 scale, from the 3-3-1 field
      content of src/m331_exact.py (17 gauge bosons, 18 real scalars, 66 or 69 Weyl
      fermions): f = 25.7 (beta = -1/sqrt3) or 26.5 (+1/sqrt3). (CHECK)
  L7c The thresholds a shrinking hole crosses (MODEL: a species switches on when T_H reaches
      a quarter of its mass, the mean emitted energy being about 4-6 T_H per Carr et al.;
      quarks and gluons replace pions at the QCD crossover, 156.5(1.5) MeV, LIT: HotQCD,
      PLB 795, 15 (2019); the electroweak crossover is 159.5(1.5) GeV, LIT: D'Onofrio and
      Rummukainen, PRD 93, 025003 (2016)): the diamond experiment's 0.15 K (8.2e23 kg);
      the CMB (2.72548 K, LIT: Fixsen, ApJ 707, 916 (2009)) at 4.5e22 kg, above which a hole
      absorbs more than it emits; electrons (rung 3's charges); pions (rung 2's Goldstones);
      the QCD crossover, where rung 2's condensate melts and quarks and gluons are emitted; the
      W, Z and Higgs, and the electroweak crossover (rung 1's breaking); the 3-3-1 scale
      (rung 1's start); and the Planck mass (link 3's cutoff), where the semiclassical
      description ends. Remaining lifetimes at each crossing are integrated with f(T). (CHECK,
      given the model)
  L7d Checks against Carr et al.: 407 s for 1e10 g at f = 15.35, here 406.7 s; the hole
      whose lifetime is the age of the universe (13.787 Gyr, LIT: Planck 2018 with BAO),
      their M* = 5.1e14 g at T_H = 21 MeV, here 5.11e14 g at 20.7 MeV with f(T) integrated.
      (CHECK)
L8  The pion from the weak and electromagnetic forces: rung 1 -> rung 2.
  L8a f_pi from rung 1's G_F. The pi+ -> mu+ nu rate, Gamma = G_F^2 f_pi^2 m_mu^2 m_pi
      (1 - m_mu^2/m_pi^2)^2 |V_ud|^2 / 8 pi (1 + delta_pi) (LIT: PDG 2024 review of leptonic
      decays of charged pseudoscalar mesons, eqs. 72.1, 72.3-72.4: delta_pi = 0.0176(21),
      Gamma = 3.8408(7)e7 /s from the 26.033 ns lifetime and 99.98770% branching fraction),
      with |V_ud| = 0.97367(32) (PDG 2024 CKM review, eq. 12.7), gives f_pi |V_ud| =
      127.13 MeV (theirs 127.13 +- 0.13) and f_pi = 130.57 MeV (theirs 130.56), against the
      lattice 130.2(1.2) MeV rung 2 takes as input: +0.3 sigma. (CHECK; LIT)
  L8b What rung 2 inherits: with that f_pi, Gamma(pi0 -> gamma gamma) = 7.742 eV (PrimEx
      7.802 +- 0.117, -0.5 sigma), and the O(p^4) pion mass of src/chiral_breaking.py S7 is
      132.3 MeV. (CHECK)
  L8c Rung 1's photon splits rung 2's pions. The DGMLY sum rule (Das, Guralnik, Mathur, Low
      and Young, PRL 18, 759 (1967); in the form of Shintani et al., PoS LATTICE2007, 134,
      arXiv:0710.0691, eq. 2.3), exact in the chiral limit:
          m_pi+^2 - m_pi0^2 = -(3 alpha / 4 pi f_pi^2) int dQ^2 Q^2 Pi_V-A(Q^2).
      Saturating Pi_V-A with the rho and a1 and imposing Weinberg's two sum rules (both
      consequences of chiral symmetry breaking), derived here symbolically:
          m_pi+^2 - m_pi0^2 = (3 alpha / 4 pi) m_rho^2 m_a1^2 / (m_a1^2 - m_rho^2) ln(m_a1^2/m_rho^2),
      independent of f_pi. With PDG 2024's m_rho = 775.26 and m_a1 = 1230(40) MeV: 1604 MeV^2
      (5.84 MeV), against the measured 1261.2 MeV^2 (4.59 MeV): +27%, the size of
      lowest-resonance saturation (the lattice evaluation of the same sum rule by Shintani et
      al. gives 1024(100) MeV^2). The sign and the scale come from rung 1's alpha and rung
      2's breaking; the 27% is the model. (CHECK; MODEL)
L9  One electromagnetic coupling from rung 1 to rung 3: alpha-hat(M_Z) run down to alpha(0).
  L9a The leptons' vacuum polarization at one loop, from the Feynman-parameter integral
      Delta alpha = (2 alpha / pi) int_0^1 dx x(1-x) ln|1 - x(1-x) M_Z^2 / m_l^2|, done here
      numerically and in closed form for e, mu, tau: 314.191e-4, against 314.190e-4 at one
      loop (LIT: Steinhauser, PLB 429, 158 (1998), Table 1; through three loops 314.977e-4).
      (CHECK)
  L9b The hadrons' part can't be computed from the repository's data: the KEDR R-ratio
      (1.84-3.05 GeV, src/m331_why_three.py) gives 1.74e-3 of the dispersion integral
      Delta alpha_had = (alpha M_Z^2 / 3 pi) int ds R(s) / (s (M_Z^2 - s)), 6.3% of the
      total 0.02783(6) (LIT: PDG 2024 electroweak review, after eq. 10.12). (CHECK; LIT)
  L9c Closure: alpha(0) = alpha-hat(M_Z) (1 - Delta alpha-hat), with Delta alpha-hat =
      Delta alpha_lep + Delta alpha_had + 0.007122 (the MS-bar minus on-shell difference,
      PDG 2024 eq. 10.13). From rung 1's 1/alpha-hat(M_Z) = 127.930: 1/alpha(0) =
      137.035999, CODATA's 137.035999084. The coupling rung 1 breaks with and the one rung 3's
      charges and photons use (L2's pi0 width, L8c's pion splitting, L1's Coulomb law) are
      one coupling at two scales. (CHECK; LIT)
Labels: CHECK, FOLLOWS, KNOWN, LIT, MODEL (L3f's gravity term; L7c's switch-on rule; L8c's resonance saturation).
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
# CODATA 2018 mass-energies (MeV) and FLAG 2024 nucleon sigma terms (MeV, value, error)
M_P_MEV, M_N0_MEV, M_E_MEV, U_MEV = 938.27208816, 939.56542052, 0.51099895000, 931.49410242
SIGMA_PIN = {"2+1": (42.2, 2.4), "2+1+1": (60.9, 6.5)}
SIGMA_S = {"2+1": (44.9, 6.4), "2+1+1": (41.0, 8.8)}
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


# ---------------------------------------------------------------------------------- L8
GAMMA_PI_MUNU = 3.8408e7                  # /s, PDG 2024 leptonic-decays review (radiation inclusive)
DELTA_PI = (0.0176, 0.0021)               # PDG 2024, eq. 72.4
V_UD = (0.97367, 0.00032)                 # PDG 2024 CKM review, eq. 12.7
G_F_GEV = 1.1663788e-5                    # GeV^-2, PDG 2024
HBAR_GEV_S = 6.582119569e-25              # GeV s, CODATA 2018 (exact)
M_RHO, M_A1 = (0.77526, 0.00023), (1.230, 0.040)   # GeV, PDG 2024 Breit-Wigner masses
DM2_LATTICE = (1024.0, 100.0)             # MeV^2, Shintani et al. (JLQCD), PoS LATTICE2007 134


def fpi_from_weak():
    """L8a: f_pi (GeV, the 130 MeV convention) from Gamma(pi -> mu nu), G_F and |V_ud|;
    returns f_pi |V_ud|, f_pi and its error from delta_pi and V_ud in quadrature."""
    g0 = GAMMA_PI_MUNU * HBAR_GEV_S / (1 + DELTA_PI[0])
    mpi, mmu = M_PIC_GEV, M_MU
    fV = math.sqrt(8 * math.pi * g0 / (G_F_GEV**2 * mmu**2 * mpi * (1 - mmu**2 / mpi**2) ** 2))
    f = fV / V_UD[0]
    err = f * math.hypot(0.5 * DELTA_PI[1] / (1 + DELTA_PI[0]), V_UD[1] / V_UD[0])
    return fV, f, err


def rung2_with_weak_fpi():
    """L8b: the pi0 width and the O(p^4) pion mass with f_pi from L8a instead of the lattice."""
    import chiral_breaking as CB
    fV, f, _ = fpi_from_weak()
    F_new = f / math.sqrt(2)
    G, _, F_old, _ = pi0_width()
    G_new = G * (F_old / F_new) ** 2
    meas, err = GAMMA_PI0_MEAS
    old = CB.F_PI
    try:
        CB.F_PI = F_new
        m4 = CB.chpt_numbers()["mpi"]
    finally:
        CB.F_PI = old
    return G_new, (G_new - meas) / err, m4


def dgmly():
    """L8c: resonance-saturated DGMLY. Pi_V = F_V^2/(Q^2 + m_V^2), Pi_A = F_A^2/(Q^2 + m_A^2)
    + f^2/Q^2; Weinberg I: F_V^2 - F_A^2 = f^2, II: F_V^2 m_V^2 = F_A^2 m_A^2. Returns the
    closed form (symbolic), its f-independence, and the numbers in MeV^2 and MeV."""
    import sympy as sp
    Q2, mV, mA, f = sp.symbols("Q2 m_V m_A f", positive=True)
    FV2, FA2 = sp.symbols("F_V2 F_A2", positive=True)
    sol = sp.solve([sp.Eq(FV2 - FA2, f**2), sp.Eq(FV2 * mV**2, FA2 * mA**2)], [FV2, FA2], dict=True)[0]
    pi_va = (FV2 / (Q2 + mV**2) - FA2 / (Q2 + mA**2) - f**2 / Q2).subs(sol)
    alpha = sp.Symbol("alpha", positive=True)
    integral = sp.integrate(sp.simplify(Q2 * pi_va), (Q2, 0, sp.oo))
    dm2 = sp.simplify(-3 * alpha / (4 * sp.pi * f**2) * integral)
    target = 3 * alpha / (4 * sp.pi) * mV**2 * mA**2 / (mA**2 - mV**2) * sp.log(mA**2 / mV**2)
    resid = sp.simplify(sp.expand_log(dm2 - target, force=True))
    num = float(target.subs({alpha: ALPHA_0, mV: M_RHO[0], mA: M_A1[0]})) * 1e6
    lo = float(target.subs({alpha: ALPHA_0, mV: M_RHO[0], mA: M_A1[0] - M_A1[1]})) * 1e6
    hi = float(target.subs({alpha: ALPHA_0, mV: M_RHO[0], mA: M_A1[0] + M_A1[1]})) * 1e6
    meas = (M_PIC_GEV**2 - M_PI0_GEV**2) * 1e6
    dm = num / ((M_PIC_GEV + M_PI0_GEV) * 1e3)
    return resid, num, (lo, hi), meas, dm, (M_PIC_GEV - M_PI0_GEV) * 1e3


# ---------------------------------------------------------------------------------- L9
AINV_MZ_MSBAR = 127.930                   # PDG 2024, 1/alpha-hat^(5)(M_Z)
DALPHA_HAD = (0.02783, 0.00006)           # PDG 2024 electroweak review, on-shell, 5 flavours
DALPHA_CONV = 0.007122                    # PDG 2024 eq. 10.13: Delta alpha-hat - Delta alpha
DALPHA_LEP_3LOOP = 314.97686e-4           # Steinhauser, PLB 429, 158 (1998), Table 1
DALPHA_LEP_1LOOP_LIT = 314.19007e-4       # same table, one loop
R_KEDR = 2.225                            # Anashin et al., PLB 770, 174 (2017), 1.84-3.05 GeV


def dalpha_lep_one_loop():
    """L9a: one-loop leptonic Delta alpha(M_Z^2), from the Feynman-parameter integral
    (numerical) and from its closed form, summed over e, mu, tau."""
    from scipy.integrate import quad
    s = M_Z**2
    num = clo = 0.0
    for m in (M_EL, M_MU, M_TAU):
        f = lambda x: x * (1 - x) * math.log(abs(1 - x * (1 - x) * s / m**2))
        x0 = 0.5 * (1 - math.sqrt(1 - 4 * m**2 / s))                # the log's zero
        num += 2 * ALPHA_0 / math.pi * (quad(f, 0, x0, limit=200)[0] + quad(f, x0, 1 - x0, limit=200)[0]
                                        + quad(f, 1 - x0, 1, limit=200)[0])
        b = math.sqrt(1 - 4 * m**2 / s)
        clo += ALPHA_0 / (3 * math.pi) * (-8 / 3 + b * b + 0.5 * b * (3 - b * b) * math.log((1 + b) / (1 - b)))
    return num, clo


def dalpha_kedr_window():
    """L9b: the KEDR window's share of Delta alpha_had (constant R over 1.84-3.05 GeV)."""
    s, s1, s2 = M_Z**2, 1.84**2, 3.05**2
    w = ALPHA_0 / (3 * math.pi) * R_KEDR * (math.log(s2 / s1) - math.log((s - s2) / (s - s1)))
    return w, w / DALPHA_HAD[0]


def alpha0_from_mz():
    """L9c: 1/alpha(0) from rung 1's MS-bar 1/alpha-hat(M_Z)."""
    d = DALPHA_LEP_3LOOP + DALPHA_HAD[0] + DALPHA_CONV
    return AINV_MZ_MSBAR / (1 - d), d


# ---------------------------------------------------------------------------------- L6
def carbon12_binding():
    """L6a: B = 6 m_p + 6 m_n + 6 m_e - 12 u, in MeV, and per nucleon."""
    B = 6 * M_P_MEV + 6 * M_N0_MEV + 6 * M_E_MEV - 12 * U_MEV
    return B, B / 12


def mass_budget(flavours="2+1"):
    """L6b-c: fractions of a carbon-12 atom's mass (the diamond's, per atom): QCD field energy,
    light- and strange-quark masses (Feynman-Hellmann sigma terms), electrons, binding."""
    s_l, s_s = SIGMA_PIN[flavours][0], SIGMA_S[flavours][0]
    B, _ = carbon12_binding()
    total = 12 * U_MEV
    parts = {"QCD field energy": 6 * (M_P_MEV - s_l - s_s) + 6 * (M_N0_MEV - s_l - s_s),
             "u, d quark masses": 12 * s_l, "s quark mass": 12 * s_s,
             "electrons": 6 * M_E_MEV, "nuclear binding": -B}
    return {k: v / total for k, v in parts.items()}, sum(parts.values()) / total


def phase_without_masses():
    """L6d: design A's phase with the light quarks massless (first order: each nucleon loses
    sigma_piN), and with all quark masses and the electron's removed; phase ~ m^2."""
    c = coulomb_vs_gravity()
    phi = c["dphi_grav"]
    out = {}
    for fl in ("2+1", "2+1+1"):
        f, _ = mass_budget(fl)
        light = 1 - f["u, d quark masses"]
        none = 1 - f["u, d quark masses"] - f["s quark mass"] - f["electrons"]
        out[fl] = (phi * light**2, phi * none**2)
    return phi, out


# ---------------------------------------------------------------------------------- L7
HBAR_SI, C_SI, KB_SI = 1.054571817e-34, 2.99792458e8, 1.380649e-23
GEV_J = 1e9 * E_CH
ALPHA_EVAP = 5.34e25                      # g^3 / s (Carr et al. 2021, eq. 12)
W_S0, W_HALF_N, W_HALF_C, W_S1, W_S2 = 0.267, 0.147, 0.142, 0.060, 0.007
T_QCD, T_EW = 0.1565, 159.5               # GeV: HotQCD 2019; D'Onofrio and Rummukainen 2016
T_CMB, T_CRYO = 2.72548, 0.15             # K: Fixsen 2009; src/stur_gravity_full.py BASE_ENV
MV_FLOOR = 3755.1                         # GeV, the bilepton mass floor (src/m331_margin.py)
# PDG 2024 masses, GeV
M_EL, M_MU, M_TAU = 0.51099895e-3, 0.1056583755, 1.77693
M_PIC_GEV, M_PI0_GEV = 0.13957039, 0.1349768
M_C, M_B, M_T = 1.2730, 4.183, 172.57
M_W, M_Z, M_H = 80.3692, 91.1880, 125.20


def hawking_T_gev(M_kg):
    return HBAR_SI * C_SI**3 / (8 * math.pi * G_NEWTON * M_kg * KB_SI) * KB_SI / GEV_J


def mass_at_T(T_gev):
    """Black-hole mass (kg) with Hawking temperature T (GeV)."""
    return HBAR_SI * C_SI**3 / (8 * math.pi * G_NEWTON * KB_SI * (T_gev * GEV_J / KB_SI))


@functools.lru_cache(maxsize=None)
def f_331(variant):
    """L7b: f in the unbroken 3-3-1 phase from src/m331_exact.py's field content (N_c = 3)."""
    import m331_exact as E
    import m331_breaking as B
    gs, ferm, scal, _ = E.MODELS[variant](3)
    weyl = sum(m * d[1] * d[2] for m, d, q in ferm)
    rows, ok, _ = B.charges(variant, 3)
    lep = [q for kind, _, q in rows if kind == "lepton triplet"][0]
    neutral = 3 * sum(1 for q in lep if q == 0)                      # per generation, Weyl
    n_gauge = 8 + 8 + 1
    n_scal = sum(m * 2 * d[1] * d[2] for m, d, q in scal)           # complex triplets -> real
    f = (2 * n_gauge * W_S1 + n_scal * W_S0 + 2 * neutral * W_HALF_N + 2 * (weyl - neutral) * W_HALF_C
         + 2 * W_S2)
    return f, weyl, n_gauge, n_scal


def f_of_T(T, variant="+1/sqrt3", rule=4.0):
    """L7b-c: f at Hawking temperature T (GeV): species switch on at T >= m / rule; pions
    become quarks and gluons at T_QCD; above M_V / rule the unbroken 3-3-1 content."""
    if T >= MV_FLOOR / rule:
        return f_331(variant)[0]
    on = lambda m: T >= m / rule
    f = 2 * W_S1 + 6 * W_HALF_N + 2 * W_S2                          # photon, neutrinos, graviton
    f += sum(4 * W_HALF_C for m in (M_EL, M_MU, M_TAU) if on(m))
    if T < T_QCD:
        f += sum(W_S0 * n for m, n in ((M_PIC_GEV, 2), (M_PI0_GEV, 1)) if on(m))
    else:
        f += 3 * 12 * W_HALF_C + 16 * W_S1                          # u, d, s and gluons
        f += sum(12 * W_HALF_C for m in (M_C, M_B, M_T) if on(m))
    f += sum(n * (2 * W_S1 + W_S0) for m, n in ((M_W, 2), (M_Z, 1)) if on(m))
    f += W_S0 if on(M_H) else 0.0
    return f


def f_standard_model_unbroken():
    """L7b check: the same count with unbroken SU(3) x SU(2) x U(1): 12 gauge bosons, 4 real
    Higgs scalars, 45 Weyl fermions (6 of them neutrinos)."""
    return 2 * 12 * W_S1 + 4 * W_S0 + 2 * 3 * W_HALF_N + 2 * 42 * W_HALF_C + 2 * W_S2


AGE_S = 13.787e9 * 365.25 * 86400        # s, Planck 2018 (TT,TE,EE+lowE+lensing+BAO)


def m_star():
    """L7d: the mass (kg) whose remaining lifetime is the age of the universe."""
    from scipy.optimize import brentq
    lm = brentq(lambda x: math.log(lifetime_s(math.exp(x)) / AGE_S), math.log(1e10), math.log(1e13), xtol=1e-8)
    return math.exp(lm)


def lifetime_s(M_kg, variant="+1/sqrt3", n=4000):
    """Remaining lifetime from mass M: int_0^M M'^2 dM' / (alpha f(M')), in grams, with f
    taken at each step's Hawking temperature (log grid down to the Planck mass)."""
    import numpy as np
    from m331_exact import M_PLANCK
    m_pl_kg = math.sqrt(HBAR_SI * C_SI / G_NEWTON)
    Mg = M_kg * 1e3
    xs = np.geomspace(m_pl_kg * 1e3, Mg, n)
    fs = np.array([f_of_T(hawking_T_gev(x / 1e3), variant) for x in xs])
    integ = xs**2 / (ALPHA_EVAP * fs)
    tail = (m_pl_kg * 1e3) ** 3 / (3 * ALPHA_EVAP * fs[0])
    return float(np.trapezoid(integ, xs) + tail)


def evaporation_thresholds(variant="+1/sqrt3"):
    """L7c: (label, T_H in GeV, M in kg, remaining lifetime in s, f just above)."""
    kT = lambda T_K: KB_SI * T_K / GEV_J
    m_pl_kg = math.sqrt(HBAR_SI * C_SI / G_NEWTON)
    pts = [("the diamond experiment's cryostat, 0.15 K", kT(T_CRYO)),
           ("CMB: absorbs more than it emits above this mass", kT(T_CMB)),
           ("electrons (rung 3's charges)", M_EL / 4), ("muons", M_MU / 4),
           ("pions (rung 2's Goldstone bosons)", M_PIC_GEV / 4),
           ("QCD crossover: rung 2's condensate melts; quarks and gluons", T_QCD),
           ("W and Z, with the Higgs mechanism's Goldstones", M_W / 4),
           ("top quark", M_T / 4), ("electroweak crossover (rung 1's breaking)", T_EW),
           ("3-3-1 content (rung 1's start)", MV_FLOOR / 4),
           ("Planck mass: link 3's cutoff, semiclassics ends", hawking_T_gev(m_pl_kg))]
    out = []
    for lab, T in pts:
        M = mass_at_T(T)
        out.append((lab, T, M, lifetime_s(M, variant), f_of_T(T * 1.0001, variant)))
    return out


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

    banner("L6a  The diamond's mass: carbon-12 from its constituents (CHECK; CODATA 2018)")
    B, b = carbon12_binding()
    print(f"   6 m_p + 6 m_n + 6 m_e - 12 u = {B:.3f} MeV ({b:.3f} MeV per nucleon): the binding of the nucleus")
    print("   (residual strong force minus Coulomb), plus the electrons' keV-level atomic binding")

    banner("L6b-c  Where it comes from (Feynman-Hellmann; LIT: FLAG 2024 sigma terms)")
    for fl in ("2+1", "2+1+1"):
        f, tot = mass_budget(fl)
        print(f"   N_f = {fl:6s}: sigma_piN = {SIGMA_PIN[fl][0]} MeV, sigma_s = {SIGMA_S[fl][0]} MeV  (sum of parts = {tot:.9f})")
        print("      " + ";  ".join(f"{k} {100 * v:+.2f}%" for k, v in f.items()))
    print("   -> design A's diamond weighs what QCD's field energy weighs; the Higgs-generated masses")
    print("      are under a tenth of it")

    banner("L6d  What the gravity experiment inherits (FOLLOWS, first order in the sigma terms)")
    phi, out = phase_without_masses()
    print(f"   design A's phase {phi:.3f} rad goes as m^2 at fixed geometry and time")
    for fl, (pl, pn) in out.items():
        print(f"   N_f = {fl:6s}: massless u, d: {pl:.2f} rad;  massless quarks and electrons: {pn:.2f} rad")

    banner("L7a-b  An evaporating black hole: the emission counts rung 1's particles (CHECK; LIT)")
    print(f"   T_H at 1e10 g = {hawking_T_gev(1e7):.1f} GeV (Carr et al. eq. 11: 1.06 TeV)")
    print(f"   f below every mass (photons, neutrinos, gravitons): {f_of_T(1e-15):.3f}")
    print(f"   f, every Standard Model species (W, Z longitudinal modes as scalars): {f_of_T(500.0):.3f};"
          f" unbroken counting {f_standard_model_unbroken():.3f}; Carr et al. 15.35")
    for v in ("-1/sqrt3", "+1/sqrt3"):
        f, weyl, ng, ns = f_331(v)
        print(f"   f, unbroken 3-3-1 (beta = {v}): {f:.2f}  ({ng} gauge bosons, {ns} real scalars, {weyl} Weyl fermions)")

    banner("L7c  The thresholds a shrinking hole crosses (beta = +1/sqrt3; MODEL switch-on at m/4)")
    print("   threshold                                                      T_H (GeV)    M (kg)      left (s)    f above")
    for lab, T, M, tau, f in evaporation_thresholds():
        print(f"   {lab:62s} {T:9.3e}  {M:9.3e}  {tau:9.3e}  {f:6.2f}")
    print("   -> from the cryostat's temperature to the Planck mass, the hole's own temperature")
    print("      passes every scale the forces separate at, in reverse order.")

    banner("L7d  Checks against Carr et al. (CHECK)")
    print(f"   1e10 g at f = 15.35: lifetime {(1e10) ** 3 / (3 * ALPHA_EVAP * 15.35):.1f} s (theirs 407 s)")
    ms = m_star()
    print(f"   lifetime = 13.787 Gyr at M* = {ms * 1e3:.3e} g, T_H = {hawking_T_gev(ms) * 1e3:.1f} MeV"
          " (theirs 5.1e14 g, 21 MeV)")

    banner("L8a  f_pi from rung 1's G_F and the measured pi -> mu nu rate (CHECK; LIT: PDG 2024)")
    fV, f, ferr = fpi_from_weak()
    print(f"   f_pi |V_ud| = {fV * 1e3:.2f} MeV (PDG review: 127.13 +- 0.13);  |V_ud| = {V_UD[0]}:"
          f" f_pi = {f * 1e3:.2f} +- {ferr * 1e3:.2f} MeV")
    print(f"   rung 2's lattice input: 130.2 +- 1.2 MeV;  difference {(f * 1e3 - 130.2) / 1.2:+.1f} sigma")

    banner("L8b  What rung 2 inherits from it (CHECK)")
    Gn, pull, m4 = rung2_with_weak_fpi()
    print(f"   Gamma(pi0 -> gamma gamma) = {Gn:.3f} eV ({pull:+.1f} sigma against PrimEx);"
          f"  O(p^4) m_pi = {m4 * 1e3:.1f} MeV")

    banner("L8c  Rung 1's photon splits rung 2's pions: the DGMLY sum rule (CHECK; MODEL saturation)")
    resid, num, (lo, hi), meas, dm, dm_meas = dgmly()
    print(f"   rho + a1 saturation with Weinberg's sum rules: closed form residual {resid} (f_pi drops out)")
    print(f"   m_pi+^2 - m_pi0^2 = {num:.0f} MeV^2 ({lo:.0f}-{hi:.0f} over m_a1 +- 40 MeV), {dm:.2f} MeV;"
          f" measured {meas:.1f} MeV^2, {dm_meas:.2f} MeV")
    print(f"   lowest-resonance saturation is {100 * (num / meas - 1):+.0f}%; the lattice evaluation of the same"
          f" sum rule: {DM2_LATTICE[0]:.0f} +- {DM2_LATTICE[1]:.0f} MeV^2")

    banner("L9a  The leptons' running of alpha, from the vacuum-polarization integral (CHECK)")
    num, clo = dalpha_lep_one_loop()
    print(f"   one loop, e + mu + tau: integral {num * 1e4:.5f}e-4, closed form {clo * 1e4:.5f}e-4;"
          f" Steinhauser {DALPHA_LEP_1LOOP_LIT * 1e4:.5f}e-4 (three loops {DALPHA_LEP_3LOOP * 1e4:.5f}e-4)")

    banner("L9b  The hadrons' running: what the repository's own R-ratio data covers (CHECK; LIT)")
    w, frac = dalpha_kedr_window()
    print(f"   KEDR window (R = {R_KEDR}, 1.84-3.05 GeV): {w:.3e} of Delta alpha_had = {DALPHA_HAD[0]} (PDG), {100 * frac:.1f}%")

    banner("L9c  One coupling at two scales: alpha-hat(M_Z) -> alpha(0) (CHECK; LIT)")
    a0, d = alpha0_from_mz()
    print(f"   1/alpha-hat(M_Z) = {AINV_MZ_MSBAR} (rung 1), Delta alpha-hat = {d:.6f}:  1/alpha(0) = {a0:.6f};"
          f" CODATA {1 / ALPHA_0:.9f}")

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
