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
L10 The broken de Sitter gauge theory back to the lab: rung 5 -> rung 4.
  L10a The weak field of rung 5's solution. MacDowell-Mansouri's field equations give
      Schwarzschild-de Sitter, f = 1 - 2GM/(c^2 r) - r^2/l^2 with Lambda = 3/l^2
      (src/macdowell_mansouri.py M3-M5). Its Newtonian potential, Phi = -(c^2/2)(1 - f) =
      -GM/r - Lambda c^2 r^2 / 6, solves nabla^2 Phi = 4 pi G rho - Lambda c^2: Newton's law
      of rung 4 plus a uniform background. (CHECK, symbolic)
  L10b The background can't entangle. For two masses the Lambda term is a sum of one-body
      energies, -(Lambda c^2/6)(m_A |x_A|^2 + m_B |x_B|^2), so it cancels identically in the
      entangling combination phi_00 + phi_11 - phi_01 - phi_10; the 1/r term is what is left,
      with the same G. Rung 5's extra constant doesn't touch rung 4's 2.19 rad. (CHECK,
      symbolic)
  L10c What can: a mass-mass correction of relative order (r/l)^2 = Lambda r^2 / 3 from the
      de Sitter propagator. At design A's farthest branch distance it is 2e-59. Its
      coefficient is not computed here; the order is the statement. (FOLLOWS, order of
      magnitude)
  L10d The same G and Lambda: rung 5's coupling 3/(G Lambda) is formed from rung 4's G and
      the measured Lambda, and its l = sqrt(3/Lambda) = 1.65e26 m. (CHECK)
  L10e The coefficient of L10c, derived (linear in the source mass). A test mass m in rung 5's
      Schwarzschild-de Sitter field at areal distance r from M has static energy
      m c^2 sqrt(1 - 2GM/(c^2 r) - r^2/l^2); its part linear in M is
          U = -G M m / (r sqrt(1 - r^2/l^2)) = -(G M m / r)(1 + r^2/(2 l^2) + ...),
      so the relative correction is (r/l)^2 / 2 = Lambda r^2 / 6, depending only on r and so
      symmetric in the two masses. Integrated along design A's branches it shifts the
      entangling phase by -1.9e-60 of itself (-4.2e-60 rad; the sign is because the farther cross
      branches matter more). The frame is the static patch
      centred on one mass, and only terms linear in each mass are kept. (CHECK, symbolic and
      numeric; FOLLOWS for the frame)
L11 The cosmological horizon's entropy: rung 5 -> rung 6.
  L11a Rung 5's vacuum, f = 1 - r^2/l^2 with Lambda = 3/l^2, has a horizon at r_c = l. Rung 6's
      surface gravity kappa = |f'(r_h)|/2 gives kappa = 1/l, T_dS = hbar c / (2 pi k_B l) (the
      Gibbons-Hawking temperature), and the area law gives the horizon area A = 4 pi l^2 =
      12 pi / Lambda (not 4 pi / Lambda) and the entropy
          S_dS = A / (4 l_P^2) = 3 pi c^3 / (G hbar Lambda) = pi x [3 / (G Lambda)]
      in units k_B = 1: pi times rung 5's MacDowell-Mansouri coupling, and 3 times
      pi c^3 / (G hbar Lambda). (CHECK, symbolic)
  L11b The first law at every horizon of Schwarzschild-de Sitter, from the same f: with
      M(r_h) from f(r_h) = 0, dM = (f'(r_h) / 4 pi) dS, S = pi r_h^2 (G = c = hbar = 1). At the
      black-hole horizon f' > 0 and it is dM = T dS; at the cosmological horizon f' < 0 and
      it is dM = -T dS: the mass inside the cosmological horizon falls as that horizon grows.
      (CHECK, symbolic)
  L11c De Sitter space maximizes the entropy: S_bh + S_c < S_dS for every black hole the
      universe allows (9 M^2 Lambda < 1), approaching it as M -> 0. The three roots of
      r^3 - l^2 r + 2 M l^2 sum to zero, so r_b^2 + r_c^2 + (r_b + r_c)^2 = 2 l^2, exactly.
      (CHECK)
  L11d The measured Lambda (Planck 2018 with BAO, as rungs 5 and 6): l = 1.65e26 m, S_dS =
      3.3e122 k_B, T_dS = 2.2e-30 K. The cosmological-constant problem, in rung 6's
      terms: the entropy of the vacuum is the inverse of how small Lambda is in Planck units.
      Not tested: that S_dS counts microstates (the holographic reading); only that the area
      law of rung 6 and the Lambda of rung 5 give it. (CHECK; LIT Lambda; FOLLOWS for the
      reading)
L12 Neutrino mass from rung 1's breaking scale: rung 1 -> low-energy oscillation data.
  L12a Rung 1's lepton triplet, from its charges (src/m331_breaking.py B6): beta = -1/sqrt3 has
      (nu, e, N) with N electrically neutral; beta = +1/sqrt3 has (nu, e, E^-) with a charged
      heavy lepton. So only the first variant has a neutral state beside nu inside the
      multiplet; in the second a singlet nu_R must be added. (CHECK)
  L12b The type-I seesaw matrix [[0, m_D], [m_D, M]] with m_D = y_D v / sqrt2 (v from rung 1's
      G_F) and M = y_R w / sqrt2 (w the 3-3-1 vev, M_V = g w / 2): the eigenvalues multiply to
      -m_D^2 exactly, so m_light = m_D^2 / m_heavy exactly, = m_D^2/M to O(m_D^4/M^3); the
      inverse seesaw [[0, m_D, 0], [m_D, 0, Lambda], [0, Lambda, mu]] gives mu m_D^2/(m_D^2 +
      Lambda^2) to first order in mu. At fixed Yukawas m_light scales exactly as 1/w. (CHECK,
      symbolic and numeric)
  L12c What this does not do: the Yukawas are free. At w = 2 M_V / g with M_V = 4 TeV and y_R = 1,
      m_light = 0.05 eV (sqrt of the atmospheric splitting) needs y_D = 3.8e-6, 1.3 times the
      electron's Yukawa; y_D equal to the electron's gives 0.03 eV. That is a coincidence of
      order of magnitude, not a prediction: no relation fixes y_D. What rung 1 supplies is the
      scale w and the structure, so the suppression m_D / M ~ 8e-8 needs no Majorana
      scale below w. (CHECK for the arithmetic; MODEL for the Yukawas)
  L12d Against data (LIT: NuFIT 6.0, normal ordering, delta m^2_21 = 7.49e-5, delta m^2_31 =
      2.513e-3 eV^2; Planck 2018, sum m_nu < 0.12 eV): the minimal sum is 0.059 eV, inside the
      bound, so a sub-eV scale of the seesaw form is consistent with both. (CHECK; LIT)
L13 First post-Newtonian correction to the entangling phase: rung 4 -> rungs 5 and 6.
  L13a The two-body Einstein-Infeld-Hoffmann Lagrangian (LIT: EIH 1938; harmonic coordinates):
      L_int = G m1 m2 / r [1 + (v1^2 + v2^2) 3/(2c^2) - 7 v1.v2 / (2c^2) - (n.v1)(n.v2)/(2c^2)]
              - G^2 m1 m2 (m1 + m2) / (2 c^2 r^2).
      Its test-mass limit is checked here against the geodesic Lagrangian of rung 5/6's
      Schwarzschild metric in harmonic coordinates, expanded to 1/c^2: the 3/2 v^2 term and the
      G^2 term agree. The v1.v2 and (n.v1)(n.v2) terms are quoted. (CHECK for the test-mass
      limit; KNOWN for the rest)
  L13b Along design A's branch trajectories, the one-body terms (m v^4/8c^2 and the like) cancel
      in the entangling combination exactly, as in L10b. The rest, integrated: the entangling
      phase shifts by -1.4e-23 rad of 2.19, a relative -6.6e-24 (of order (v/c)^2 for v =
      dx/ramp = 0.46 mm/s); the G^2 term is another -1.8e-37 rad. No 1PN effect is near
      measurable. (CHECK; FOLLOWS
      for the reading: a coordinate-time phase in the lab frame)
L15 The cosmological constant against every rung's vacuum energy: rung 5 -> rungs 1, 2, 4.
  L15a An exact identity: with rho_L = Lambda c^4 / (8 pi G) and the Planck energy density
      rho_Pl = c^7 / (hbar G^2), S_dS = (3/8) rho_Pl / rho_L. The horizon's entropy is the ratio
      of the Planck vacuum energy density to the observed one. (CHECK, symbolic)
  L15b The measured rho_L^(1/4) = 2.25 meV, against: the chiral vacuum energy of rung 2,
      -f_pi^2 m_pi^2 (leading order of the chiral Lagrangian at U = 1), (111 MeV)^4; the Higgs
      potential's minimum of rung 1, -m_h^2 v^2 / 8, (104 GeV)^4; the 3-3-1 scale w^4 (an order
      of magnitude, coefficient unknown) with w from L12; and M_Pl^4 (link 3). Each is
      6e42, 5e54, 9e62 and 9e122 times rho_L (L15a gives the last as 8 S_dS / 3). Each
      phase transition changes the vacuum energy by about that much, and nothing in
      this repository cancels it: this quantifies the cosmological-constant problem, it
      does not solve it. (CHECK for the arithmetic; LIT for m_h; MODEL for the 3-3-1 w^4)
L16 The ringdown fit checked at zero spin: rung 6 -> its own data (H7, H8).
  L16a Leaver's continued fraction (Leaver 1985; gravitational perturbations of rung 6's
      Schwarzschild metric, 2M = 1) solved for the l = 2 quasinormal modes: M omega =
      0.373672 - 0.088962 i (n = 0) and 0.346711 - 0.273915 i (n = 1), the known values.
      (CHECK)
  L16b The Berti-Cardoso-Will fit that black_holes.py H7-H8 inverts, at chi = 0: M omega_R =
      f1 + f2 = 0.3683 (1.4% below the exact 0.37367) and Q = q1 + q2 = 2.119
      against the exact 2.100 (+0.9%). So the fit's error at the non-spinning end is about
      1%; the GW250114 inversion uses it at chi ~ 0.7, which L20 covers with Kerr's
      Teukolsky equation. (CHECK at chi = 0)
L17 The ABJ anomaly coefficient, derived: rung 1's anomalies -> L2's pi0 width.
  L17a Fujikawa's Jacobian with explicit Euclidean gamma matrices. D-slash^2 = D^2 - (e/2)
      sigma_{mu nu} F_{mu nu}; the regulated trace Tr gamma5 exp(-D-slash^2/M^2) keeps, as
      M -> infinity, only the term second order in sigma F, with int d^4k/(2 pi)^4 e^(-k^2) =
      1/(16 pi^2): A = (1/16 pi^2)(e^2/8) tr[gamma5 sigma_{mu nu} sigma_{rho sigma}] F F. The
      trace is computed for all 256 index sets: it is -4 eps_{mu nu rho sigma} exactly (the sign
      is the orientation chosen for gamma5; the magnitude is not conventional). So
      A = e^2 eps F F / (32 pi^2) and the divergence of the axial current, twice the Jacobian,
      is d_mu j5^mu = (e^2/16 pi^2) eps^{mu nu rho sigma} F_{mu nu} F_{rho sigma} in magnitude.
      (CHECK, symbolic; the dropped terms vanish as M -> infinity by power counting)
  L17b A second route that shares nothing with it. In parallel E and B, the lowest Landau
      level of each chirality is a 1+1 Weyl fermion with eB/2 pi states per area, whose
      momenta drift at eE: d n5/dt = 2 (eB/2 pi)(eE/2 pi) = e^2 E B / (2 pi^2). With
      eps F F = 8 F_12 F_34 (and |eps F F| = 8 E B in Minkowski) L17a gives the same
      number. (CHECK, symbolic)
  L17c Matching to L2. Weights: j5^3 = (u-bar g g5 u - d-bar g g5 d)/2 over N_c colours gives
      (N_c/2)(Q_u^2 - Q_d^2) times L17a. With <0|j5^3|pi0> = i f_pi p and eps F F = 4 eps
      d A d A (two photons: a factor 2), the amplitude is
          A = alpha N_c (Q_u^2 - Q_d^2) / (pi f_pi),
      the coefficient that L2 quoted; the width follows from L2b. (CHECK, symbolic)
  L17d What stays quoted: the PCAC step <0|j5|pi0> = i f_pi p, and that the anomaly is not
      renormalized beyond one loop (Adler-Bardeen). (LIT)
L18 The rho parameter from the top-bottom loop, and what it does to M_W: rung 1 -> data.
  L18a The W and Z self-energies at q^2 = 0 from the fermion loop, in dimensional regularization
      (d = 4 - 2 eps) with the tadpole A0 and the two-point function B0 done in closed form.
      Left-handed pieces give 2 (2/d - 1)[A0(m2) + m1^2 B0] and the left-right piece 2 m1 m2 B0;
      the vector current's Ward identity (Pi_VV(0) = 0 for equal masses) is checked first.
      Then Delta rho = Pi_ZZ(0)/M_Z^2 - Pi_WW(0)/M_W^2 for the (t, b) doublet (couplings
      T3 - Q s^2 from rung 1) has no 1/eps pole and no dependence on s^2, and equals
          N_c G_F / (8 sqrt2 pi^2) [m_t^2 + m_b^2 - 2 m_t^2 m_b^2 ln(m_t^2/m_b^2) / (m_t^2 - m_b^2)],
      which is 3 G_F m_t^2 / (8 sqrt2 pi^2) for m_b -> 0. (CHECK, symbolic)
  L18b With m_t = 172.57 GeV and m_b = 4.18 GeV (LIT: PDG 2024): Delta rho = 9.26e-3.
  L18c The radiative correction to M_W, from G_F, alpha(0), M_Z: M_W^2 (1 - M_W^2/M_Z^2) =
      pi alpha / (sqrt2 G_F) / (1 - Delta r) (Sirlin's definition), Delta r = Delta alpha - (c^2/s^2) Delta rho + Delta r_H
      + Delta r_rest. Tree level (Delta r = 0): 80.94 GeV.
      Adding Delta alpha = 0.05933 (the leptons of L9 through three loops plus the hadronic
      0.02783, LIT) lowers it to 79.96, the top loop (L18a) lifts it to 80.53, the Higgs term
      (LIT: 3 G_F M_W^2 ln(m_H^2/M_W^2) / (8 sqrt2 pi^2), quoted) takes it to 80.50 GeV, against
      the measured 80.37 (LIT: PDG 2024). The 0.13 GeV left is Delta r_rest = 0.007, everything
      beyond these leading terms; it is not computed here. (CHECK for the top loop; LIT for
      the rest)
  L18d What this does not do: B7's +0.35% (tree M_Z against the measured one) is in the MS-bar
      scheme, where s-hat^2(M_Z) absorbs part of Delta rho; that bookkeeping is not done here.
      This closes the leading piece of the on-shell correction, not B7's number. (FOLLOWS)
L19 Hawking radiation as radiation, derived: rung 6 -> its own temperature (H1, H2).
  H1 and H2 fix the temperature geometrically; the quoted step was that the field is then
  *emitted* with a Planck spectrum. Here: a massless field's outgoing modes at infinity,
  p_w = e^(-i w u)/sqrt(4 pi w), against the vacuum of the regular (Kruskal) coordinate U
  across the horizon, v_O = e^(-i O U)/sqrt(4 pi O). Near the horizon u = -(1/kappa)
  ln(-kappa U), kappa from rung 6 (H1).
  L19a The Klein-Gordon overlaps, with one integration by parts (checked numerically):
      alpha = (1/2 pi) sqrt(O/w) kappa^(i y) int_0^oo x^(i y) e^(-i O x) dx and beta the same with
      e^(+i O x), y = w/kappa. The integral is Gamma(1 + i y) s^(-1-i y) at s = +-i O, so
      |alpha|^2 = e^(pi y) |Gamma|^2 / (4 pi^2 w O) and |beta|^2 the same with e^(-pi y). With
      |Gamma(1 + i y)|^2 = pi y / sinh(pi y) (checked): |beta/alpha|^2 = e^(-2 pi w/kappa), and
      |alpha|^2 - |beta|^2 = 1/(2 pi kappa O), the unitarity (commutator) normalization. (CHECK)
  L19b The mean number of quanta in mode w is the ratio, n = |beta|^2/(|alpha|^2 - |beta|^2) =
      1/(e^(2 pi w/kappa) - 1): Planck's law at k_B T = hbar kappa/2 pi, now as an emission
      spectrum, for every O. (CHECK, symbolic)
  L19c The energy flux of one massless 1+1 field, (1/2 pi) int w n dw = pi (k_B T)^2/12 (hbar =
      1), is the Stefan-Boltzmann law in one dimension. For Schwarzschild it uses the T_H of
      H1. What this does not do: the 3+1 grey-body factors (greybody transmission) that turn
      this into L7's mass-loss rate are quoted there (LIT: Carr et al.). (CHECK, symbolic)
L20 The ringdown fit at the spin GW250114 uses: Leaver's method for Kerr, rung 6 -> H7, H8.
  L20a Teukolsky's radial equation for s = -2 with Leaver's three-term recurrence (units 2M = 1,
      a = chi/2) coupled to the spin-weighted spheroidal equation's recurrence through the
      separation constant A: two complex continued-fraction conditions for (omega, A), solved by
      Newton's method and continued in chi from L16's Schwarzschild mode. Compared with the 11
      tabulated values of Berti, Cardoso and Will (PRD 73, 064030, Table II, l = m = 2, n = 0,
      chi = 0 to 0.98; LIT, 4 digits): every real and imaginary part agrees to 6e-5. (CHECK; LIT)
  L20b The fit F = f1 + f2 (1 - chi)^f3, Q = q1 + q2 (1 - chi)^q3 against the exact modes over
      chi = 0 to 0.99: largest errors 1.85% (frequency) and 0.88% (Q), the 1.85% and 0.88% that
      Berti, Cardoso and Will state. (CHECK)
  L20c GW250114's ringdown-only 220 mode (247 Hz, damping 221 Hz, z = 0.09) inverted with the
      exact modes: M_f = 66.48 Msun, chi_f = 0.744 (the fit gave 66.73 and 0.746), final area
      4.04e5 km^2 (fit: 4.07e5). At the least favourable corner of the published ranges the final
      area is 3.36e5 km^2 (fit: 3.41e5) against the initial 2.52e5: the area law's check does
      not rest on the fit's error. (CHECK; LIT data)
L21 The retarded Casimir-Polder step, checked: rung 3's quoted ln det with propagating fields.
  L21a P3b of src/casimir_diamonds.py checked the fluctuation formula for instantaneous coupling.
      Retardation is the part that was left. An exactly solvable retarded system: two
      oscillators (frequency w0, coupling g) at sites 0 and r of a ring of M lattice sites
      carrying a massless-ish scalar field (-Delta + mu^2). Its normal modes are the
      eigenvalues of one real symmetric matrix, so the interaction energy U(r) =
      (1/2) sum_i w_i(r) - (same at the farthest separation) is computed by diagonalization.
      Integrating the field out (Schur complement) gives the same energy as
      (1/2 pi) int_0^oo dxi ln[1 - (g^2 G12(xi, r) alpha_d(xi))^2], alpha_d = 1/(xi^2 + w0^2 -
      g^2 G00(xi)), with G(xi) the field's Green function at imaginary frequency, which depends
      on xi through propagation: e^(-kappa r) decay with kappa = sqrt(xi^2 + mu^2). The two
      agree to 1e-10 (relative) at r = 4, 8, 12. Replacing G12(xi) by its static value
      G12(0) (instantaneous coupling) is off by a factor of 3 at r = 4. (CHECK)
  L21b What it covers: the step from a retarded kernel to the energy, in a model where the
      retarded field is solved exactly. The electromagnetic case has the same algebra with G a
      3 x 3 tensor (P2's Green tensor at imaginary frequency, already checked against the
      Helmholtz equation) and two transverse polarizations; the dyadic case itself is not
      diagonalized here. (FOLLOWS)
  L21c The order. At design A's gap, alpha G ~ K R^3 / r^3 = 1e-7, so the second-order term
      that P3 keeps is exact to 1e-14 (the next term of the logarithm is relatively (alpha G)^2).
      (CHECK)
L22 B7's +0.35% on M_Z, decomposed: rung 1's tree M_Z against the measurement, in the MS-bar scheme.
  L22a The MS-bar relations (LIT: PDG 2024 electroweak review, eq. 10.26): M_Z = A0 /
      [s-hat c-hat ((1 - Dr_W) rho-hat)^(1/2)], A0 = (pi alpha / sqrt2 G_F)^(1/2), with the
      published Dr_W = 0.06937 and rho-hat = 1.01016 (bosonic loops included). B7's tree
      formula M_Z = (pi alpha-hat / sqrt2 G_F)^(1/2) / (s-hat c-hat) is A0 / [s-hat c-hat (1 - Dr0)^(1/2)] with
      alpha-hat = alpha/(1 - Dr0), Dr0 = 1 - alpha/alpha-hat = 0.06645. So, exactly,
          M_Z^2 / M_Z(tree)^2 = (1 - Dr0) / [(1 - Dr_W) rho-hat],
      which gives 91.1879 GeV against the measured 91.1880, and a gap of -0.348% against B7's -0.348%.
      (CHECK for the algebra; LIT for the three published numbers)
  L22b The pieces, in M_Z^2: rho-hat contributes -1.006%, (1 - Dr0)/(1 - Dr_W) contributes +0.314%;
      together -0.695%, half of it the -0.348% in M_Z. The quadratic top-mass dependence sits in rho-hat
      alone (Dr_W has none, PDG). (CHECK)
  L22c What L18 derives of it: the one-loop top-bottom loop gives rho - 1 = 9.26e-3, 91% of rho-hat - 1 =
      1.016e-2. With it in place of rho-hat, M_Z = 91.229 GeV, 0.045% (0.04 GeV) above the measurement.
      Not derived here: the other 9% of rho-hat - 1 (bosonic loops, two-loop terms) and Dr_W - Dr0 =
      0.0029 (vertex and box corrections to muon decay and the rest of the MS-bar Dr_W). So B7's
      number is decomposed and its dominant part derived, not closed. (CHECK; LIT; FOLLOWS)
L23 The electromagnetic dyadic step of L21, derived independently: rung 3 from photon exchange.
  L23a Two blind builds (campaign qed_cp, rebuild/campaigns/qed_cp/ACCEPTED.md) derived the retarded
      Casimir-Polder energy of two single-resonance atoms from the 12 time-ordered fourth-order diagrams of
      the dipole-photon coupling, with the full photon polarization sum and angular average, and no use of the
      Green-tensor formula. The accepted builds agree with the imaginary-frequency integral of rung 3 (P3)
      to 1e-11 (1e-15 against the oracle's extended-precision reference) over r w0 = 1e-2 to 1e3, and derive the far coefficient 23/(4 pi) and the near coefficient 3/4.
      So the 3 x 3, two-polarization structure that L21b left as FOLLOWS is confirmed by an independent route.
      (CHECK; two builds, an audit, a hidden oracle)
  L23b What it does not do: the single-resonance atom model is the polarizability of P3b (constant-alpha
      follows in the far zone); the Abel-damping step for the photon integrals is supported, not proved; and
      the gate cannot enforce the independence of the route, which the audit checked by reading. (FOLLOWS)
L24 The emission weights of L7, derived: the grey-body campaign. Rung 6, quoted -> derived.
  L24a L7 took the energy emitted per degree of freedom of each spin (weights 0.267, 0.147, 0.060, 0.007 with
      dM/dt = -5.34e25 f/M^2 g^3/s) from Carr et al. 2021, after Page 1976 and MacGibbon-Webber. Two blind builds
      (rebuild/campaigns/greybody, ACCEPTED.md) derived them from the Regge-Wheeler and Chandrasekhar master equations
      on Schwarzschild: Gamma_{s,j}(omega) from the ingoing horizon solution matched to the large-r asymptotic series,
      then P_s = sum_j (2j+1) int dw/(2 pi) w Gamma/(e^{w/T} -+ 1) at T = 1/8 pi. In units 1/M^2: 7.43869e-5 (spin 0),
      4.09165e-5 (1/2), 1.68193e-5 (1), 1.91837e-6 (2); in Carr's normalization the weights are 0.2664, 0.1465,
      0.0602, 0.00687, against the quoted 0.267, 0.147, 0.060, 0.007 (differences 0.2%, 0.3%, 0.4%, 1.9%, all
      within the quoted digits). An auditor's independent solver (WKB projection at large R, no asymptotic series)
      reproduces P_s to 1e-9 and the low-frequency limits of Gamma are exact. (CHECK; two builds, audit, oracle)
  L24b What it does not reproduce: Carr's 0.142 for charged spin-1/2 against 0.147 for neutral. Massless grey-body
      factors give one spin-1/2 weight, 0.1465. L7's Standard Model count f = 15.332 uses the quoted 0.142 for charged
      fermions; with the derived 0.1465 for every fermion it would be 15.71, 2.5% above Carr's 15.35. Carr et al.
      (eqs. 12-13) quote the two weights with different mean emitted energies (4.22 and 4.18 T_BH) from MacGibbon 1991
      after Page 1976-77, so the charged value is a different (massive charged-lepton) calculation than the massless
      grey-body factors here; not derived here, and its source could not be retrieved. (FOLLOWS; located, not resolved)
L25 Hawking radiation from a collapsing shell: the map behind L19, derived. Rung 6, quoted -> derived.
  L25a L19 assumed the map u = -(1/kappa) ln(-kappa U) between the horizon-crossing coordinate and retarded time. For a thin null
      shell that collapses to a Schwarzschild hole of mass M (flat inside, Schwarzschild outside, the shell at advanced time v0)
      it follows exactly. An incoming ray at advanced time v < v0 passes through the centre (u_in = v), meets the shell at
      r_s = (v0 - v)/2, and leaves along u = v0 - 2 r*(r_s), r* = r + 2M ln(r/2M - 1). So
          u(v) = v - 4M ln((v_H - v)/4M),   v_H = v0 - 4M,
      derived symbolically here (residual 0). Near v_H, du/dv ~ 4M/(v_H - v): kappa = 1/4M, equal to |f'(r_h)|/2 of H1. Rays with
      v > v_H never reach infinity: the horizon. (CHECK, symbolic)
  L25b With this map the overlaps of L19 are exact: alpha and beta are the integrals int_0^oo x^(4iM w) e^(i(w -+ w')x) dx (x = v_H - v), so
          |beta_{w w'}|^2 / |alpha_{w w'}|^2 = ((w' - w)/(w' + w))^2 e^(-8 pi M w),
      the Planck factor of L19 times a correction that tends to 1 for in-frequencies w' >> w (the modes that fell in at late
      times), and that is ((w' - w)/(w' + w))^2 < 1 otherwise: a thin-shell hole is thermal only for those modes. The closed
      form of the overlap integrals is the one L19 verifies against direct integration; here it is evaluated at several
      (w, w'). (CHECK)
  L25c What it does not do: a thin shell is not a star (no matter dynamics, no back-reaction); the late-time stationarity of the
      flux, the 3+1 grey-body factors and the back-reaction on the mass are not derived here. (FOLLOWS)
L26 The Higgs term of L18, derived: the coefficient of ln m_H^2 in Delta rho. Rung 1, quoted -> derived (coefficient only).
  L26a L18 quoted the heavy-Higgs term Delta r_H = +(3 G_F M_W^2 / 8 sqrt2 pi^2) ln(m_H^2/M_W^2). Two blind builds (campaign higgs_rho,
      ACCEPTED.md) derived the m_H dependence of Delta rho = Pi_WW(0)/M_W^2 - Pi_ZZ(0)/M_Z^2 from the Higgs-containing one-loop diagrams of the
      bosonic electroweak Lagrangian in R_xi gauge (Feynman rules read off |D Phi|^2; the H-gauge bubble, the H-Goldstone bubble and the
      seagull, in dimensional regularization): the poles are m_H-independent and cancel, xi drops out exactly, and
          Delta rho = -(3 alpha / 16 pi c^2) ln(m_H^2/M_W^2) + C,   C = 9.54e-4 (relative to m_H = M_W),
      so, with Delta r_H = -(c^2/s^2) Delta rho and G_F M_W^2 = pi alpha / (sqrt2 s^2), the quoted coefficient 3 G_F M_W^2/(8 sqrt2 pi^2) =
      3 alpha/(16 pi s^2) is reproduced to the double. An independent auditor computed the finite function by two other routes
      (agreement to the double at m_H = 10 to 5000 GeV). (CHECK; two builds, audit, oracle)
  L26b What it does not give: the full Higgs dependence of Delta r at m_H = 125 GeV. The finite function Delta rho(m_H) - Delta rho(M_W) at 125.2
      GeV is -2.0e-4, 39% of the leading-log value -5.2e-4: the leading log overstates it. But Delta r's own m_H dependence also
      comes from the q^2-dependent self-energies (Pi_WW(M_W^2) - Pi_WW(0), photon-Z mixing), which are not computed here, so L18's term
      is not replaced; its coefficient is derived, its finite-m_H shape is not. (FOLLOWS)
L14 Bekenstein bound: rung 6 -> rung 4. S <= 2 pi k R E / (hbar c). A Schwarzschild black hole
  (R = 2GM/c^2, E = M c^2) saturates it exactly, = A / 4 l_P^2 (CHECK, symbolic). Design A's
  diamond (radius 1.0 um, 7.4e11 atoms): Bekenstein bound 2.6e23 k_B, holographic bound
  1.2e58 k_B; its entropy at 0.15 K is far below either, so neither constrains the experiment.
  (CHECK; the diamond's own entropy is not computed here)
Labels: CHECK, FOLLOWS, KNOWN, LIT, MODEL (L3f's gravity term; L7c's switch-on rule; L8c's resonance saturation).
"""
import functools
import math
import os
import sys
from itertools import product

import numpy as np
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


# ---------------------------------------------------------------------------------- L10
LAMBDA_SI = 1.1056e-52                    # m^-2, as in src/macdowell_mansouri.py and src/black_holes.py


def weak_field_of_sds():
    """L10a: Phi from Schwarzschild-de Sitter's f, and the Poisson equation it solves away
    from the source (nabla^2 Phi = -Lambda c^2 there; the point mass gives 4 pi G rho)."""
    import sympy as sp
    r, Gs, M, c, l = sp.symbols("r G M c l", positive=True)
    f = 1 - 2 * Gs * M / (c**2 * r) - r**2 / l**2
    Phi = sp.simplify(-(c**2 / 2) * (1 - f))
    Lam = 3 / l**2
    lap = sp.simplify(sp.diff(r**2 * sp.diff(Phi, r), r) / r**2)
    return sp.simplify(Phi - (-Gs * M / r - Lam * c**2 * r**2 / 6)), sp.simplify(lap + Lam * c**2)


def lambda_cancels_in_entangling_phase():
    """L10b: branch energies U_ij = -G m^2 / |x_Ai - x_Bj| - (Lambda c^2/6) m (|x_Ai|^2 + |x_Bj|^2);
    the entangling combination of the Lambda part is identically zero."""
    import sympy as sp
    m, Gs, c, Lam = sp.symbols("m G c Lambda", positive=True)
    xa = sp.symbols("xa0 xa1", real=True)
    xb = sp.symbols("xb0 xb1", real=True)
    ya = sp.symbols("ya0 ya1", real=True)
    yb = sp.symbols("yb0 yb1", real=True)
    bg = lambda i, j: -(Lam * c**2 / 6) * m * (xa[i] ** 2 + ya[i] ** 2 + xb[j] ** 2 + yb[j] ** 2)
    ent = bg(0, 0) + bg(1, 1) - bg(0, 1) - bg(1, 0)
    return sp.simplify(ent)


def lambda_correction_size():
    """L10c-d: (r/l)^2 at design A's farthest branch distance, and l."""
    import graviton_exchange as GX
    _, _, _, (m, dx, gap, hold, ramp) = GX.branch_phases()
    r_far = math.hypot(gap, dx)
    l = math.sqrt(3 / LAMBDA_SI)
    return (r_far / l) ** 2, l, r_far


# ---------------------------------------------------------------------------------- L11
HBAR_SI, C_SI, KB_SI = 1.054571817e-34, 299792458.0, 1.380649e-23


def de_sitter_entropy_symbolic():
    """L11a: horizon, surface gravity, area, entropy of f = 1 - r^2/l^2 (G = c = hbar = k_B = 1)."""
    import sympy as sp
    r, l = sp.symbols("r l", positive=True)
    f = 1 - r**2 / l**2
    Lam = 3 / l**2
    rc = [x for x in sp.solve(f, r) if x.is_positive][0]
    kappa = sp.Abs(sp.diff(f, r)).subs(r, rc) / 2
    A = 4 * sp.pi * rc**2
    S = A / 4
    return (sp.simplify(rc - l), sp.simplify(kappa - 1 / l), sp.simplify(A - 12 * sp.pi / Lam),
            sp.simplify(S - 3 * sp.pi / Lam), sp.simplify(S - sp.pi * 3 / Lam),
            sp.simplify(S / (sp.pi / Lam)))          # the last: 3, the factor over pi c^3/(G hbar Lambda)


def first_law_every_horizon():
    """L11b: dM/dr_h - (f'(r_h)/4 pi) dS/dr_h for SdS, with M from f(r_h) = 0."""
    import sympy as sp
    r, l, M = sp.symbols("r l M", positive=True)
    f = 1 - 2 * M / r - r**2 / l**2
    Mh = sp.solve(f, M)[0]
    fp = sp.diff(f, r).subs(M, Mh)
    return sp.simplify(sp.diff(Mh, r) - fp / (4 * sp.pi) * sp.diff(sp.pi * r**2, r))


def sds_entropy_bound(n=200):
    """L11c: max over M of (S_bh + S_c)/S_dS for 0 < 9 M^2 Lambda < 1, and the exact root identity."""
    import sympy as sp
    rb, rc = sp.symbols("r_b r_c", positive=True)
    # roots rb, rc, -(rb + rc) of r^3 - l^2 r + 2 M l^2: e2 = rb rc - (rb + rc)^2 = -l^2  ->  l^2 = rb^2 + rb rc + rc^2;  then the sum of squares is 2 l^2:
    ident = sp.simplify(rb**2 + rc**2 + (rb + rc) ** 2 - 2 * (rb**2 + rb * rc + rc**2))
    worst = 0.0
    for k in range(1, n):
        Mv = (k / n) / math.sqrt(27)               # l = 1: 9 M^2 Lambda = 27 M^2 < 1
        # stdlib bisection: f(r) = r^3 - r + 2 M has roots 0 < r_b < 1/sqrt3 < r_c < 1
        g = lambda x: x**3 - x + 2 * Mv
        a, b = 1e-12, 1 / math.sqrt(3)
        for _ in range(200):
            m = (a + b) / 2
            a, b = (m, b) if g(m) > 0 else (a, m)
        rbv = (a + b) / 2
        a, b = 1 / math.sqrt(3), 1.0
        for _ in range(200):
            m = (a + b) / 2
            a, b = (a, m) if g(m) > 0 else (m, b)
        rcv = (a + b) / 2
        worst = max(worst, rbv**2 + rcv**2)        # (S_bh + S_c) / S_dS with S = pi r^2, S_dS = pi l^2
    return ident, worst


def de_sitter_numbers():
    """L11d: l, S_dS, T_dS, and 3 pi c^3/(G hbar Lambda) against pi x 3/(G Lambda) in Planck units."""
    lP2 = G_NEWTON * HBAR_SI / C_SI**3
    l = math.sqrt(3 / LAMBDA_SI)
    A = 4 * math.pi * l**2
    S = A / (4 * lP2)
    T = HBAR_SI * C_SI / (2 * math.pi * KB_SI * l)
    mm = 3 / (lP2 * LAMBDA_SI)
    return l, A, S, T, S / (math.pi * mm), S / (math.pi * C_SI**3 / (G_NEWTON * HBAR_SI * LAMBDA_SI))


# ---------------------------------------------------------------------------------- L12
NUFIT_DM21, NUFIT_DM31 = 7.49e-5, 2.513e-3        # eV^2, NuFIT 6.0 (2024), normal ordering
SUM_NU_PLANCK = 0.12                              # eV, Planck 2018 (TT,TE,EE+lowE+lensing+BAO), 95%
M_E_EV = 0.51099895e6


def lepton_triplets():
    """L12a: the lepton triplet's charges for both variants, from rung 1's B6."""
    import m331_breaking as B
    out = {}
    for v in ("-1/sqrt3", "+1/sqrt3"):
        rows, ok, _ = B.charges(v, 3)
        out[v] = [str(x) for k, X, q in rows if k == "lepton triplet" for x in q]
    return out


def seesaw_symbolic():
    """L12b: det identity, leading terms, and the inverse seesaw's first order in mu."""
    import sympy as sp
    mD, M, mu, Lam, eps = sp.symbols("m_D M mu Lambda epsilon", positive=True)
    S = sp.Matrix([[0, mD], [mD, M]])
    ev = S.eigenvals()
    lam = sorted(ev, key=lambda e: float(e.subs({mD: 1, M: 7})))
    prod = sp.simplify(lam[0] * lam[1] + mD**2)                               # det = -m_D^2
    light = sp.simplify(-lam[0])
    ser = sp.series(light.subs(mD, eps * mD), eps, 0, 6).removeO()
    resid = sp.simplify(ser - (eps**2 * mD**2 / M - eps**4 * mD**4 / M**3))
    I = sp.Matrix([[0, mD, 0], [mD, 0, Lam], [0, Lam, mu]])
    p = sp.expand(I.charpoly(sp.Symbol("x")).as_expr())
    x = sp.Symbol("x")
    # smallest root to first order in mu: x = mu mD^2/(mD^2 + Lam^2) solves p = 0 up to O(mu^2)
    root = mu * mD**2 / (mD**2 + Lam**2)
    inv = sp.simplify(sp.series(p.subs(x, root), mu, 0, 2).removeO())
    return prod, resid, inv


def seesaw_numbers(MV=4e3, yR=1.0, target=math.sqrt(NUFIT_DM31)):
    """L12b-c: w from M_V = g w / 2, M = y_R w / sqrt2, the y_D that gives `target` eV, and
    the scaling of m_light with w at fixed Yukawas (log-log slope)."""
    import m331_breaking as B
    g = math.sqrt(4 * math.pi / B.ALPHA_MZ_INV / B.S2_MZ)
    w = 2 * MV / g
    v = (math.sqrt(2) * B.G_F) ** -0.5
    M = yR * w / math.sqrt(2) * 1e9                                  # eV
    vev = v * 1e9
    yD = math.sqrt(2 * target * M) / vev                              # m_D^2 / M = target, m_D = y_D v / sqrt2
    ye = math.sqrt(2) * M_E_EV / vev
    def light(wv, yd=yD):                                            # 2 m_D^2 / (M + sqrt(M^2 + 4 m_D^2)): no cancellation
        m_D, MM = yd * vev / math.sqrt(2), yR * wv * 1e9 / math.sqrt(2)
        return 2 * m_D**2 / (MM + math.sqrt(MM**2 + 4 * m_D**2))
    slope = math.log(light(10 * w) / light(w)) / math.log(10)
    m_with_ye = light(w, ye)
    return dict(g=g, w=w, M=M, yD=yD, ye=ye, ratio=yD / ye, light=light(w), slope=slope,
                m_with_ye=m_with_ye, suppress=(yD * vev / math.sqrt(2)) / M)


def neutrino_data():
    """L12d: minimal sum of masses for normal ordering from the splittings."""
    m1 = 0.0
    m2 = math.sqrt(NUFIT_DM21)
    m3 = math.sqrt(NUFIT_DM31)
    return m1 + m2 + m3, SUM_NU_PLANCK


# ---------------------------------------------------------------------------------- L13
def eih_test_mass_limit():
    """L13a: expand -m c^2 sqrt(-g_mu nu v^mu v^nu / c^2) in harmonic-coordinate Schwarzschild to
    1/c^2 and subtract the EIH test-mass limit (m2 -> M, v2 = 0). Zero means they agree."""
    import sympy as sp
    m, Mm, Gs, r, vv, t = sp.symbols("m M G r v t", positive=True)       # t = 1/c^2
    U = Gs * Mm / r
    L = -m / t * sp.sqrt(1 - 2 * t * U + 2 * t**2 * U**2 - (1 + 2 * t * U) * t * vv**2)
    ser = sp.series(L, t, 0, 2).removeO()
    eih = -m / t + m * vv**2 / 2 + m * U + t * (m * vv**4 / 8 + sp.Rational(3, 2) * m * U * vv**2
                                                   - Gs**2 * m * Mm**2 / (2 * r**2))       # m << M
    return sp.simplify(sp.expand(ser - eih))


def eih_phase_shift(n=4001):
    """L13b: entangling phase of design A, Newtonian and from the 1PN terms of the EIH Lagrangian,
    along the branch trajectories (A_i at (0, s_i y), B_j at (gap, s_j y))."""
    import graviton_exchange as GX
    import stur_gravity_full as GF
    _, _, _, (m, dx, gap, hold, ramp) = GX.branch_phases()
    total = hold + 2 * ramp
    t = np.linspace(0, total, n)
    y = 0.5 * dx * GF.ramp_profile(t, hold, ramp)
    vy = np.gradient(y, t)
    G_, hb, c2 = G_NEWTON, HBAR_SI, C_SI**2
    N = np.zeros((2, 2))
    P = np.zeros((2, 2))
    Q = np.zeros((2, 2))
    for i, si in enumerate((1, -1)):
        for j, sj in enumerate((1, -1)):
            d = np.stack([np.full_like(t, gap), sj * y - si * y])               # B - A
            r = np.sqrt((d**2).sum(0))
            nvec = d / r
            v1 = np.stack([np.zeros_like(t), si * vy])
            v2 = np.stack([np.zeros_like(t), sj * vy])
            newt = G_ * m**2 / r
            pn = newt / c2 * (1.5 * ((v1**2).sum(0) + (v2**2).sum(0)) - 3.5 * (v1 * v2).sum(0)
                              - 0.5 * (nvec * v1).sum(0) * (nvec * v2).sum(0))
            g2 = -G_**2 * m**3 / (c2 * r**2)
            N[i, j] = np.trapezoid(newt, t) / hb
            P[i, j] = np.trapezoid(pn, t) / hb
            Q[i, j] = np.trapezoid(g2, t) / hb
    ent = lambda a: a[0, 0] + a[1, 1] - a[0, 1] - a[1, 0]
    return ent(N), ent(P), ent(Q)


# ---------------------------------------------------------------------------------- L14
def bekenstein_saturation():
    """L14: 2 pi R E / (hbar c) for a Schwarzschild black hole minus A / (4 l_P^2), symbolic."""
    import sympy as sp
    Gs, hb, c, M = sp.symbols("G hbar c M", positive=True)
    R = 2 * Gs * M / c**2
    bek = 2 * sp.pi * R * M * c**2 / (hb * c)
    area = 4 * sp.pi * R**2 / (4 * Gs * hb / c**3)
    return sp.simplify(bek - area)


def diamond_bounds():
    """L14: design A's Bekenstein bound and holographic bound, against its atom count."""
    import graviton_exchange as GX
    import stur_gravity_entanglement as GE
    _, _, _, (m, dx, gap, hold, ramp) = GX.branch_phases()
    R = GE.radius(m)
    bek = 2 * math.pi * R * m * C_SI / HBAR_SI
    holo = 4 * math.pi * R**2 / (4 * G_NEWTON * HBAR_SI / C_SI**3)
    atoms = m / (12 * U_AMU)
    return R, bek, holo, atoms


# ---------------------------------------------------------------------------------- L10e, L15
M_H_GEV = 125.20                                   # PDG 2024


def de_sitter_pair_correction(n=4001):
    """L10e: linear-in-M part of the static energy of a test mass in SdS, its relative correction
    (r/l)^2/2, and the shift of design A's entangling phase."""
    import sympy as sp
    import graviton_exchange as GX
    import stur_gravity_full as GF
    r, l, Gs, M, m, c = sp.symbols("r l G M m c", positive=True)
    E = m * c**2 * sp.sqrt(1 - 2 * Gs * M / (c**2 * r) - r**2 / l**2)
    lin = sp.simplify(sp.diff(E, M).subs(M, 0))                       # coefficient of M
    newton = -Gs * m / r
    ratio = sp.simplify(lin / newton)
    resid = sp.simplify(sp.series(ratio, r, 0, 4).removeO() - 1 - r**2 / (2 * l**2))
    _, _, _, (mm, dx, gap, hold, ramp) = GX.branch_phases()
    t = np.linspace(0, hold + 2 * ramp, n)
    y = 0.5 * dx * GF.ramp_profile(t, hold, ramp)
    lval = math.sqrt(3 / LAMBDA_SI)
    base = lambda rr: G_NEWTON * mm**2 / HBAR_SI * np.trapezoid(1 / rr, t)
    corr = lambda rr: G_NEWTON * mm**2 / HBAR_SI * np.trapezoid(rr / (2 * lval**2), t)    # (1/r)(r^2/2l^2)
    rs, rc = np.full_like(t, gap), np.sqrt(gap**2 + (2 * y) ** 2)
    dn = 2 * base(rs) - 2 * base(rc)
    dc = 2 * corr(rs) - 2 * corr(rc)
    return resid, dn, dc


def de_sitter_entropy_identity():
    """L15a: S_dS - (3/8) rho_Pl / rho_L, symbolic."""
    import sympy as sp
    Gs, hb, c, Lam = sp.symbols("G hbar c Lambda", positive=True)
    rho_L = Lam * c**4 / (8 * sp.pi * Gs)
    rho_Pl = c**7 / (hb * Gs**2)
    S = 3 * sp.pi * c**3 / (Gs * hb * Lam)
    return sp.simplify(S - sp.Rational(3, 8) * rho_Pl / rho_L)


def vacuum_energy_scales():
    """L15b: rho_L^(1/4) and the ratios (E^4 / rho_L) of each rung's vacuum-energy scale, E in eV."""
    import m331_breaking as B
    eV = 1.602176634e-19
    rho = LAMBDA_SI * C_SI**4 / (8 * math.pi * G_NEWTON)             # J/m^3
    rho_ev4 = rho * (HBAR_SI * C_SI) ** 3 / eV**4                    # eV^4
    f_pi, m_pi = 92.07e6, 134.9768e6                                 # eV (rung 2's f_pi; PDG pi0)
    v = (math.sqrt(2) * B.G_F) ** -0.5 * 1e9
    w = seesaw_numbers()["w"] * 1e9
    mpl = math.sqrt(HBAR_SI * C_SI / G_NEWTON) * C_SI**2 / eV        # eV
    scales = {"chiral (rung 2): f_pi^2 m_pi^2": f_pi**2 * m_pi**2,
              "Higgs (rung 1): m_h^2 v^2 / 8": (M_H_GEV * 1e9) ** 2 * v**2 / 8,
              "3-3-1 (rung 1): w^4": w**4,
              "Planck (link 3): M_Pl^4": mpl**4}
    return rho_ev4 ** 0.25, {k: x / rho_ev4 for k, x in scales.items()}


# ---------------------------------------------------------------------------------- L16
def leaver_qnm(n=0, l=2, start=None):
    """L16a: M*omega of the gravitational l-mode, n-th overtone, from Leaver's continued fraction
    (2M = 1, s = 2); the n-th inversion for n > 0."""
    import mpmath as mp
    mp.mp.dps = 25
    eps = 3                                                          # s^2 - 1

    def cond(w, N=600):
        rho = -1j * w
        al = lambda k: k * k + (2 * rho + 2) * k + 2 * rho + 1
        be = lambda k: -(2 * k * k + (8 * rho + 2) * k + 8 * rho**2 + 4 * rho + l * (l + 1) - eps)
        ga = lambda k: k * k + 4 * rho * k + 4 * rho**2 - eps - 1
        R = 0
        for k in range(N - 1, n - 1, -1):
            R = al(k) * ga(k + 1) / (be(k + 1) - R)
        fwd = 0
        for k in range(1, n + 1):
            fwd = al(k - 1) * ga(k) / (be(k - 1) - fwd)
        return be(n) - fwd - R
    g = start or {0: 0.74 - 0.18j, 1: 0.69 - 0.55j}[n]
    w = mp.findroot(cond, g) / 2
    return complex(w)


def bcw_at_zero_spin():
    """L16b: the fit's M*omega_R and Q at chi = 0 against the exact n = 0 mode."""
    import black_holes as BH
    f1, f2, f3, q1, q2, q3 = BH.BCW_220
    w = leaver_qnm(0)
    return f1 + f2, w.real, q1 + q2, w.real / (-2 * w.imag)


# ---------------------------------------------------------------------------------- L17
def abj_fujikawa():
    """L17a: tr[gamma5 sigma_{mu nu} sigma_{rho sigma}] = lam eps_{mu nu rho sigma} for all
    indices (returns lam and whether it holds for every set), and the coefficient of
    eps F F in the Jacobian A = (1/16 pi^2)(e^2/8) lam, in units of e^2/(32 pi^2)."""
    import sympy as sp
    from sympy import I, Matrix, eye, zeros, LeviCivita
    s1 = Matrix([[0, 1], [1, 0]]); s2 = Matrix([[0, -I], [I, 0]]); s3 = Matrix([[1, 0], [0, -1]])
    def kron(a, b):
        return sp.kronecker_product(a, b)
    Z = sp.eye(2)
    gam = [kron(s2, s1), kron(s2, s2), kron(s2, s3), kron(s1, Z)]       # Euclidean: {g_m, g_n} = 2 delta
    ok = all(sp.simplify(gam[m] * gam[n] + gam[n] * gam[m] - 2 * (1 if m == n else 0) * sp.eye(4)) == sp.zeros(4, 4)
             for m in range(4) for n in range(4))
    g5 = gam[0] * gam[1] * gam[2] * gam[3]
    sig = lambda m, n: I / 2 * (gam[m] * gam[n] - gam[n] * gam[m])
    lam, holds = None, True
    for a in range(4):
        for b in range(4):
            for c in range(4):
                for d in range(4):
                    tr = sp.simplify((g5 * sig(a, b) * sig(c, d)).trace())
                    e = LeviCivita(a, b, c, d)
                    if e == 0:
                        holds &= tr == 0
                    else:
                        lam = tr / e if lam is None else lam
                        holds &= sp.simplify(tr - lam * e) == 0
    A = sp.Rational(1, 16) / sp.pi**2 * sp.Rational(1, 8) * lam           # in units of e^2 eps F F
    return ok, lam, holds, sp.simplify(abs(A) * 32 * sp.pi**2)             # last: 1 means e^2/(32 pi^2); the sign is gamma5's orientation


def abj_landau():
    """L17b: Jacobian route (divergence = 2 A, in units of eps F F with eps F F = 8 F12 F34) minus the
    Landau-level count 2 (eB/2pi)(eE/2pi), with F12 = B and F34 = E."""
    import sympy as sp
    e, B, E = sp.symbols("e B E", positive=True)
    from sympy import LeviCivita
    F = sp.zeros(4, 4)
    F[0, 1], F[1, 0], F[2, 3], F[3, 2] = B, -B, E, -E
    epsFF = sum(LeviCivita(a, b, c, d) * F[a, b] * F[c, d]
                for a in range(4) for b in range(4) for c in range(4) for d in range(4))
    div = 2 * e**2 / (32 * sp.pi**2) * epsFF
    landau = 2 * (e * B / (2 * sp.pi)) * (e * E / (2 * sp.pi))
    return sp.simplify(epsFF - 8 * B * E), sp.simplify(div - landau)


def abj_pion_amplitude():
    """L17c: amplitude from the anomaly, divided by alpha N_c (Q_u^2 - Q_d^2)/(pi f_pi); 1 if it matches."""
    import sympy as sp
    e, Nc, Qu, Qd, fpi, alpha = sp.symbols("e N_c Q_u Q_d f_pi alpha", positive=True)
    c = Nc * (Qu**2 - Qd**2) / 2 * e**2 / (16 * sp.pi**2)                  # d j5^3 = c eps F F
    amp = c / fpi * 8                                                      # eps F F = 4 eps dA dA, times 2 photon orderings
    target = alpha * Nc * (Qu**2 - Qd**2) / (sp.pi * fpi)
    return sp.simplify((amp / target).subs(e, sp.sqrt(4 * sp.pi * alpha)))


# ---------------------------------------------------------------------------------- L18
M_T_GEV, M_B_GEV = 172.57, 4.18                    # PDG 2024
MW_MEAS = 80.3692                                  # GeV, PDG 2024 average
DALPHA_HAD_5 = 0.02783                             # PDG 2024 (L9b)


def rho_parameter_loop():
    """L18a: Ward identity, pole- and s^2-independence, and the closed form of Delta rho."""
    import sympy as sp
    eps, s2 = sp.symbols("eps s2", positive=True)
    mt, mb = sp.symbols("m_t m_b", positive=True)
    D = 1 / eps
    A0 = lambda m: m**2 * (D + 1 - sp.log(m**2))
    B0 = lambda m1, m2: D + 1 - (m1**2 * sp.log(m1**2) - m2**2 * sp.log(m2**2)) / (m1**2 - m2**2)
    B0e = lambda m: D - sp.log(m**2)
    fac = -sp.Rational(1, 2) * (1 - eps) / (1 - eps / 2)                  # 2/d - 1
    LL = lambda m1, m2: 2 * fac * (A0(m2) + m1**2 * B0(m1, m2))
    LLe = lambda m: 2 * fac * (A0(m) + m**2 * B0e(m))
    LR = lambda m: 2 * m**2 * B0e(m)
    m = sp.Symbol("m", positive=True)
    ward = sp.simplify(sp.series(2 * LLe(m) + 2 * LR(m), eps, 0, 1).removeO())
    Z = lambda mm, Q, T3: (T3 - Q * s2) ** 2 * LLe(mm) + (Q * s2) ** 2 * LLe(mm) + 2 * (T3 - Q * s2) * (-Q * s2) * LR(mm)
    tot = 4 * (Z(mt, sp.Rational(2, 3), sp.Rational(1, 2)) + Z(mb, -sp.Rational(1, 3), -sp.Rational(1, 2))) - 2 * LL(mt, mb)
    ser = sp.simplify(sp.series(tot, eps, 0, 1).removeO())
    known = mt**2 + mb**2 - 2 * mt**2 * mb**2 / (mt**2 - mb**2) * sp.log(mt**2 / mb**2)
    return ward, ser.has(eps), ser.has(s2), sp.simplify(sp.expand_log(ser - known, force=True)), sp.limit(ser, mb, 0)


def rho_top_bottom(mt=M_T_GEV, mb=M_B_GEV):
    """L18b: Delta rho = N_c G_F F / (8 sqrt2 pi^2)."""
    GF = 1.1663788e-5
    F = mt**2 + mb**2 - 2 * mt**2 * mb**2 / (mt**2 - mb**2) * math.log(mt**2 / mb**2)
    return 3 * GF * F / (8 * math.sqrt(2) * math.pi**2)


def w_mass_steps(mH=125.20, mZ=91.1880):
    """L18c: M_W with Delta r built up term by term (fixed point in M_W), and the implied remainder."""
    GF = 1.1663788e-5
    A = math.pi * ALPHA_0 / (math.sqrt(2) * GF)
    drho = rho_top_bottom()
    dal = DALPHA_LEP_3LOOP + DALPHA_HAD_5

    def solve(use_dal, use_top, use_h, rest=0.0):
        MW = 80.4
        for _ in range(200):
            c2s2 = MW**2 / (mZ**2 - MW**2)
            dH = 3 * GF * MW**2 / (8 * math.sqrt(2) * math.pi**2) * math.log(mH**2 / MW**2) if use_h else 0.0
            dr = (dal if use_dal else 0.0) - (c2s2 * drho if use_top else 0.0) + dH + rest
            MW = math.sqrt(mZ**2 / 2 * (1 + math.sqrt(1 - 4 * A / (1 - dr) / mZ**2)))
        return MW, dr
    steps = [solve(False, False, False), solve(True, False, False), solve(True, True, False), solve(True, True, True)]
    lo, hi = -0.05, 0.05
    for _ in range(100):
        mid = (lo + hi) / 2
        if solve(True, True, True, mid)[0] > MW_MEAS:
            lo = mid
        else:
            hi = mid
    return drho, dal, steps, (lo + hi) / 2


# ---------------------------------------------------------------------------------- L19
def bogoliubov_checks(y=0.7, Om=1.3, s_re=0.6):
    """L19a: numerical check of the integral and of |Gamma(1+iy)|^2, then the moduli."""
    import mpmath as mp
    mp.mp.dps = 20
    # int_0^oo x^(iy) e^(-s x) dx = Gamma(1 + iy) s^(-1 - iy), checked at Re s > 0 (then continued to s = +-i Omega)
    s_ = mp.mpf(s_re) + 0.9j
    num = mp.quad(lambda x: x ** (1j * y) * mp.exp(-s_ * x), [0, 1, 10, mp.inf])
    clo = mp.gamma(1 + 1j * y) * s_ ** (-1 - 1j * y)
    gam2 = abs(mp.gamma(1 + 1j * y)) ** 2 - mp.pi * y / mp.sinh(mp.pi * y)
    # moduli of the continued integral at s = +- i Omega (principal branch)
    mod = lambda sgn: abs(mp.gamma(1 + 1j * y) * (sgn * 1j * Om) ** (-1 - 1j * y))
    ratio = (mod(-1) / mod(+1)) ** 2                        # |beta/alpha|^2 should be e^(-2 pi y)
    return abs(num - clo), abs(gam2), ratio, mp.e ** (-2 * mp.pi * y)


def bogoliubov_symbolic():
    """L19a-c: unitarity normalization, Planck's law and the 1+1 flux."""
    import sympy as sp
    y, w, O, k = sp.symbols("y omega Omega kappa", positive=True)
    g2 = sp.pi * y / sp.sinh(sp.pi * y)
    A2 = sp.exp(sp.pi * y) * g2 / (4 * sp.pi**2 * w * O)
    B2 = sp.exp(-sp.pi * y) * g2 / (4 * sp.pi**2 * w * O)
    unit = sp.simplify(sp.expand((A2 - B2).subs(y, w / k).rewrite(sp.exp) - 1 / (2 * sp.pi * k * O)))
    n = sp.simplify((B2 / (A2 - B2)).rewrite(sp.exp) - 1 / (sp.exp(2 * sp.pi * y) - 1))
    T = sp.Symbol("T", positive=True)
    t, nn = sp.symbols("t n", positive=True)                 # w/(e^(w/T) - 1) = T^2 t sum_n e^(-n t), w = T t
    zeta2 = sp.summation(sp.integrate(t * sp.exp(-nn * t), (t, 0, sp.oo)), (nn, 1, sp.oo))
    flux = sp.simplify(T**2 * zeta2 / (2 * sp.pi) - sp.pi * T**2 / 12)
    return unit, n, flux


# ---------------------------------------------------------------------------------- L20
KERR_BCW_TABLE = {0.0: (.3737, .0890), 0.1: (.3870, .0887), 0.2: (.4021, .0883), 0.3: (.4195, .0877),
                  0.4: (.4398, .0869), 0.5: (.4641, .0856), 0.6: (.4940, .0838), 0.7: (.5326, .0808),
                  0.8: (.5860, .0756), 0.9: (.6716, .0649), 0.98: (.8254, .0386)}   # BCW 2006, Table II, l = m = 2, n = 0


def kerr_conditions(w, A, chi, m=2, s=-2, N=300):
    """Leaver's two continued-fraction conditions (radial, angular) for the n = 0 mode (2M = 1)."""
    a = chi / 2
    b = math.sqrt(1 - 4 * a * a)
    k1, k2 = abs(m - s) / 2, abs(m + s) / 2
    q = w / 2 - m * a
    c0 = 1 - s - 1j * w - 2j * q / b
    c1 = -4 + 2j * w * (2 + b) + 4j * q / b
    c2 = s + 3 - 3j * w - 2j * q / b
    c3 = w * w * (4 + 2 * b - a * a) - 2 * a * m * w - s - 1 + (2 + b) * 1j * w - A + (4 * w + 2j) * q / b
    c4 = s + 1 - 2 * w * w - (2 * s + 3) * 1j * w - (4 * w + 2j) * q / b
    al = lambda k: k * k + (c0 + 1) * k + c0
    be = lambda k: -2 * k * k + (c1 + 2) * k + c3
    ga = lambda k: k * k + (c2 - 3) * k + c4 - c2 + 2
    R = 0
    for k in range(N - 1, -1, -1):
        R = al(k) * ga(k + 1) / (be(k + 1) - R)
    rad = be(0) - R
    aw = a * w
    alt = lambda k: -2 * (k + 1) * (k + 2 * k1 + 1)
    bet = lambda k: (k * (k - 1) + 2 * k * (k1 + k2 + 1 - 2 * aw)
                     - (2 * aw * (2 * k1 + s + 1) - (k1 + k2) * (k1 + k2 + 1)) - (aw * aw + s * (s + 1) + A))
    gat = lambda k: 2 * aw * (k + k1 + k2 + s)
    Rt = 0
    for k in range(N - 1, 0, -1):
        Rt = alt(k - 1) * gat(k) / (bet(k) - Rt)
    return rad, bet(0) - Rt


def kerr_solve(chi, guess):
    """Newton's method in (omega, A) with a finite-difference Jacobian."""
    x = list(guess)
    for _ in range(60):
        f = lambda v: kerr_conditions(v[0], v[1], chi)
        F0 = f(x)
        J = []
        for j in range(2):
            xp = list(x)
            xp[j] += 1e-7
            Fp = f(xp)
            J.append([(Fp[i] - F0[i]) / 1e-7 for i in range(2)])
        det = J[0][0] * J[1][1] - J[1][0] * J[0][1]
        d0 = (F0[0] * J[1][1] - F0[1] * J[1][0]) / det
        d1 = (F0[1] * J[0][0] - F0[0] * J[0][1]) / det
        x[0] -= d0
        x[1] -= d1
        if abs(d0) + abs(d1) < 1e-13:
            break
    return x


@functools.lru_cache(maxsize=None)
def kerr_grid():
    """Solutions on chi = 0, 0.025, ..., 0.975 by continuation from Schwarzschild (A = 4)."""
    x = kerr_solve(0.0, [2 * leaver_qnm(0), 4 + 0j])
    out = {0.0: tuple(x)}
    for i in range(1, 40):
        x = kerr_solve(i * 0.025, x)
        out[round(i * 0.025, 4)] = tuple(x)
    return out


def kerr_qnm(chi):
    """M omega (magnitude convention: real part > 0, imaginary part < 0) of the l = m = 2, n = 0 mode."""
    g = kerr_grid()
    k = min(g, key=lambda c: abs(c - chi))
    return kerr_solve(chi, list(g[k]))[0] / 2


def kerr_FQ(chi):
    w = kerr_qnm(chi)
    return w.real, w.real / (-2 * w.imag)


def kerr_table_check():
    """L20a: largest difference from BCW's Table II over its 11 tabulated spins."""
    worst = 0.0
    for chi, (re, im) in KERR_BCW_TABLE.items():
        w = kerr_qnm(chi)
        worst = max(worst, abs(w.real - re), abs(-w.imag - im))
    return worst


def kerr_fit_errors(n=100):
    """L20b: largest relative errors of BCW's F and Q fits against the exact modes, chi = 0 to 0.99."""
    import black_holes as BH
    f1, f2, f3, q1, q2, q3 = BH.BCW_220
    ef = eq = 0.0
    for i in range(n):
        c = i * 0.01
        F, Q = kerr_FQ(c)
        ef = max(ef, abs((f1 + f2 * (1 - c) ** f3) / F - 1))
        eq = max(eq, abs((q1 + q2 * (1 - c) ** q3) / Q - 1))
    return ef, eq


def invert_220_exact(freq, damp, z):
    """L20c: remnant mass and spin from the 220 frequency and damping rate with the exact Kerr modes."""
    import black_holes as BH
    Q = math.pi * freq / damp
    lo, hi = 0.0, 0.95
    for _ in range(50):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if kerr_FQ(mid)[1] < Q else (lo, mid)
    chi = (lo + hi) / 2
    m_det = kerr_FQ(chi)[0] / (2 * math.pi * freq * BH.GM_SUN / BH.C**3)
    return m_det / (1 + z), chi


def area_law_exact():
    """L20c: GW250114's final area with the exact modes, at the median and the least favourable corner."""
    import black_holes as BH
    mf, chif = invert_220_exact(BH.F220, BH.G220, BH.GW_Z)
    a_f = BH.kerr_area_km2(mf, chif)
    a_f_min = min(BH.kerr_area_km2(*invert_220_exact(f, g, z)) for f in (BH.F220 - BH.F220_ERR, BH.F220 + BH.F220_ERR)
                  for g in (BH.G220 - BH.G220_LO, BH.G220 + BH.G220_HI) for z in (BH.GW_Z - BH.GW_Z_ERR, BH.GW_Z + BH.GW_Z_ERR))
    return mf, chif, a_f, a_f_min


# ---------------------------------------------------------------------------------- L21
def lattice_green(M, mu, xi, d):
    """(-Delta + mu^2 + xi^2)^(-1) between sites d apart on a ring of M sites."""
    p = 2 * np.pi * np.arange(M) / M
    return float(np.mean(np.cos(p * d) / (xi**2 + mu**2 + 4 * np.sin(p / 2) ** 2)))


def retarded_pair_energy(M=200, mu=0.3, g=0.45, w0=1.0, rs=(4, 8, 12), r_far=100):
    """L21a: for each r, U(r) = E0(r) - E0(r_far) from the normal modes of the whole oscillators + field
    system, against (1/2 pi) int dxi ln det with the retarded and with the static Green function."""
    from scipy.integrate import quad
    K = np.zeros((M, M))
    for j in range(M):
        K[j, j] = 2 + mu**2
        K[j, (j + 1) % M] = K[(j + 1) % M, j] = -1

    def exact(r):
        V = np.zeros((M + 2, M + 2))
        V[:M, :M] = K
        V[M, M] = V[M + 1, M + 1] = w0**2
        V[M, 0] = V[0, M] = g
        V[M + 1, r] = V[r, M + 1] = g
        ev = np.linalg.eigvalsh(V)
        assert ev.min() > 0
        return 0.5 * np.sum(np.sqrt(ev))

    def formula(r, retarded):
        def f(xi):
            a = xi**2 + w0**2
            g12 = lattice_green(M, mu, xi if retarded else 0.0, r)
            return math.log(1 - (g * g * g12 / (a - g * g * lattice_green(M, mu, xi, 0))) ** 2)
        return quad(f, 0, np.inf, limit=400)[0] / (2 * np.pi)
    e0, f0, s0 = exact(r_far), formula(r_far, True), formula(r_far, False)
    return {r: (exact(r) - e0, formula(r, True) - f0, formula(r, False) - s0) for r in rs}


def casimir_polder_order():
    """L21c: alpha G at design A's gap, K R^3 / r^3, and the relative size of the next term of ln(1 - x)."""
    import casimir_diamonds as CD
    import graviton_exchange as GX
    import stur_gravity_entanglement as GE
    _, _, _, (m, dx, gap, hold, ramp) = GX.branch_phases()
    R = GE.radius(m)
    K = (GE.EPS_DIAMOND - 1) / (GE.EPS_DIAMOND + 2)
    x = K * R**3 / gap**3
    return x, x**2


# ---------------------------------------------------------------------------------- L22
DR_W_HAT, RHO_HAT = 0.06937, 1.01016              # PDG 2024 EW review: MS-bar Delta r_W and rho-hat (bosonic loops included)


def mz_bookkeeping():
    """L22: B7's tree M_Z against the measured one through the PDG MS-bar relations."""
    import m331_breaking as B
    GF = B.G_F
    al, alh = ALPHA_0, 1 / B.ALPHA_MZ_INV
    s2 = B.S2_MZ
    A0 = math.sqrt(math.pi * al / (math.sqrt(2) * GF))
    dr0 = 1 - al / alh
    tree = math.sqrt(math.pi * alh / (math.sqrt(2) * GF) / (s2 * (1 - s2)))
    pred = A0 / (math.sqrt(s2 * (1 - s2)) * math.sqrt((1 - DR_W_HAT) * RHO_HAT))
    ratio2 = (1 - dr0) / ((1 - DR_W_HAT) * RHO_HAT)
    parts = (1 / RHO_HAT - 1, (1 - dr0) / (1 - DR_W_HAT) - 1)
    drho = rho_top_bottom()
    pred_one_loop = A0 / (math.sqrt(s2 * (1 - s2)) * math.sqrt((1 - DR_W_HAT) * (1 + drho)))
    return dict(dr0=dr0, tree=tree, pred=pred, gap=pred / tree - 1, measured_gap=B.MZ_MEAS / tree - 1,
                ratio2=ratio2, parts=parts, drho=drho, frac=drho / (RHO_HAT - 1), pred_one_loop=pred_one_loop,
                mz=B.MZ_MEAS, dr_diff=DR_W_HAT - dr0)


# ---------------------------------------------------------------------------------- L23
def _load_build(name):
    import importlib.util
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "rebuild", "campaigns", "qed_cp", "builds", name, "qed_cp.py")
    spec = importlib.util.spec_from_file_location("qed_cp_build_" + name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def p3_reference(rho):
    """U in units alpha0^2 w0^7 at r w0 = rho from rung 3's route: -(1/2 pi) int dxi alpha(i xi)^2 Tr G.G, alpha0 = w0 = 1."""
    from scipy.integrate import quad
    f = lambda xi: (1 / (1 + xi**2)) ** 2 * 2 * math.exp(-2 * xi * rho) * (3 + 6 * xi * rho + 5 * (xi * rho) ** 2 + 2 * (xi * rho) ** 3 + (xi * rho) ** 4) / rho**6
    return -quad(f, 0, math.inf, limit=400)[0] / (2 * math.pi)


def qed_cp_accepted(rhos=(0.05, 0.5, 1.0, 3.0, 20.0)):
    """L23a: the accepted perturbation-theory build a against rung 3's route; build b at one point; the derived coefficients."""
    a, b = _load_build("a"), _load_build("b")
    worst = max(abs(a.cp_energy(r, 1.0, 1.0) / p3_reference(r) - 1) for r in rhos)
    cross = abs(b.cp_energy(1.0, 1.0, 1.0) / a.cp_energy(1.0, 1.0, 1.0) - 1)
    return worst, cross, a.far_coefficient(), a.near_coefficient()


# ---------------------------------------------------------------------------------- L24
GREY_P = {0: 7.43868693871e-5, 0.5: 4.09165271219e-5, 1: 1.68192739347e-5, 2: 1.91836996439e-6}   # accepted campaign, units 1/M^2


def grey_weights():
    """L24a: the derived P_s in Carr's normalization (5.34e25 g^3/s over hbar c^4/G^2), against the quoted weights."""
    unit = ALPHA_EVAP / (HBAR_SI * C_SI**4 / G_NEWTON**2 * 1e9)
    quoted = {0: W_S0, 0.5: W_HALF_N, 1: W_S1, 2: W_S2}
    return {s: (p / unit, quoted[s]) for s, p in GREY_P.items()}


def grey_f_standard_model():
    """L24b: the Standard Model count of L7 with the quoted charged-fermion weight, and with the derived one for all fermions."""
    w = grey_weights()
    f = lambda w0, wn, wc, w1, w2: 2 * 12 * w1 + 4 * w0 + 2 * 3 * wn + 2 * 42 * wc + 2 * w2
    return (f(w[0][1], w[0.5][1], W_HALF_C, w[1][1], w[2][1]),
            f(w[0][0], w[0.5][0], W_HALF_C, w[1][0], w[2][0]),
            f(w[0][0], w[0.5][0], w[0.5][0], w[1][0], w[2][0]))


def grey_gamma_against_reference(n=6):
    """L24a: the accepted build a's Gamma at n reference points against the auditor's independent solver."""
    import importlib.util, json
    here = os.path.dirname(os.path.abspath(__file__))
    spec = importlib.util.spec_from_file_location("greybody_build_a", os.path.join(here, "..", "rebuild", "campaigns", "greybody", "builds", "a", "greybody.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    ref = json.load(open(os.path.join(here, "..", "rebuild", "campaigns", "greybody", "reference.json")))["gamma"]
    step = max(1, len(ref) // n)
    return max(abs(mod.transmission(*k) / v - 1) for k, v in ref[::step])


# ---------------------------------------------------------------------------------- L25
def null_shell_map():
    """L25a: u(v) for a thin null shell collapsing to a Schwarzschild hole: derived symbolically from the ray through the centre."""
    import sympy as sp
    v, v0, M = sp.symbols("v v0 M", positive=True)
    rs = (v0 - v) / 2                                        # where the reflected ray meets the shell (flat inside: u_in = v)
    rstar = lambda r: r + 2 * M * sp.log(r / (2 * M) - 1)
    u = v0 - 2 * rstar(rs)                                    # outgoing ray u = v - 2 r* in the exterior, at v = v0
    vH = v0 - 4 * M
    claimed = v - 4 * M * sp.log((vH - v) / (4 * M))
    resid = sp.simplify(sp.expand_log(u - claimed, force=True))
    x = sp.Symbol("x", positive=True)
    dudx = sp.simplify(sp.diff(claimed.subs(v, vH - x), x))   # du/dv = -du/dx at fixed v0
    kappa_inv = sp.limit(-(sp.diff(claimed.subs(v, vH - x), x)) * x, x, 0)       # du/dv ~ (1/kappa)/x
    f = lambda r: 1 - 2 * M / r
    kappa_h1 = sp.simplify(sp.diff(f(sp.Symbol("r", positive=True)), sp.Symbol("r", positive=True)).subs(sp.Symbol("r", positive=True), 2 * M) / 2)
    return resid, sp.simplify(kappa_inv), kappa_h1


def shell_bogoliubov_ratio(w, wp, M=1.0):
    """L25b: |beta/alpha|^2 from the overlap integrals int_0^oo x^(i y) e^(i s x) dx = Gamma(1 + i y) (-i s)^(-1 - i y), y = 4 M w,
    s = w - w' (alpha) and w + w' (beta), and the closed form ((w' - w)/(w' + w))^2 e^(-8 pi M w)."""
    import mpmath as mp
    y = 4 * M * w
    # alpha: e^{-i w u} e^{+i w' v} -> integrand x^(i y) e^{i (w - w') x}; beta: e^{-i w u} e^{-i w' v} -> x^(i y) e^{i (w + w') x}
    ia = mp.gamma(1 + 1j * y) * mp.power(-1j * (w - wp), -1 - 1j * y)
    ib = mp.gamma(1 + 1j * y) * mp.power(-1j * (w + wp), -1 - 1j * y)
    return float(abs(ib) ** 2 / abs(ia) ** 2), float(((wp - w) / (wp + w)) ** 2 * mp.e ** (-8 * mp.pi * M * w))


# ---------------------------------------------------------------------------------- L26
def _load_higgs_build(name):
    import importlib.util
    here = os.path.dirname(os.path.abspath(__file__))
    spec = importlib.util.spec_from_file_location("higgs_rho_build_" + name, os.path.join(here, "..", "rebuild", "campaigns", "higgs_rho", "builds", name, "higgs_rho.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def higgs_term_derived(mh=125.20, MW_=80.3692, MZ_=91.1876):
    """L26: the accepted build's log coefficient against L18's quoted term, and the finite function against the leading log at mh."""
    a = _load_higgs_build("a")
    GF = 1.1663788e-5
    s2 = 1 - (MW_ / MZ_) ** 2
    alpha = math.sqrt(2) * GF * MW_**2 * s2 / math.pi                     # G_F M_W^2 = pi alpha / (sqrt2 s^2)
    B = a.log_coefficient(MW_, MZ_, alpha, 1.0)
    quoted = 3 * GF * MW_**2 / (8 * math.sqrt(2) * math.pi**2)             # L18's coefficient of ln(m_H^2/M_W^2) in Delta r_H
    derived = -(MW_**2 / MZ_**2) / s2 * B                                    # Delta r_H = -(c^2/s^2) Delta rho
    rho = a.rho_higgs_rel(mh, MW_, MZ_, alpha, 1.0, MW_)
    lead = B * math.log((mh / MW_) ** 2)
    return derived, quoted, rho, lead


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


def f_of_T(T, variant="+1/sqrt3", rule=4.0, mv=MV_FLOOR):
    """L7b-c: f at Hawking temperature T (GeV): species switch on at T >= m / rule; pions
    become quarks and gluons at T_QCD; above M_V / rule the unbroken 3-3-1 content."""
    if T >= mv / rule:
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


def lifetime_s(M_kg, variant="+1/sqrt3", n=4000, mv=MV_FLOOR):
    """Remaining lifetime from mass M: int_0^M M'^2 dM' / (alpha f(M')), in grams, with f
    taken at each step's Hawking temperature (log grid down to the Planck mass)."""
    import numpy as np
    from m331_exact import M_PLANCK
    m_pl_kg = math.sqrt(HBAR_SI * C_SI / G_NEWTON)
    Mg = M_kg * 1e3
    xs = np.geomspace(m_pl_kg * 1e3, Mg, n)
    fs = np.array([f_of_T(hawking_T_gev(x / 1e3), variant, mv=mv) for x in xs])
    integ = xs**2 / (ALPHA_EVAP * fs)
    tail = (m_pl_kg * 1e3) ** 3 / (3 * ALPHA_EVAP * fs[0])
    return float(np.trapezoid(integ, xs) + tail)


LABELS_LADDER = ("the diamond experiment's cryostat, 0.15 K", "CMB: absorbs more than it emits above this mass",
                 "electrons (rung 3's charges)", "muons", "pions (rung 2's Goldstone bosons)",
                 "QCD crossover: rung 2's condensate melts; quarks and gluons",
                 "W and Z, with the Higgs mechanism's Goldstones", "top quark",
                 "electroweak crossover (rung 1's breaking)", "3-3-1 content (rung 1's start)",
                 "Planck mass: link 3's cutoff, semiclassics ends")


def evaporation_thresholds(variant="+1/sqrt3", t_cryo=T_CRYO, mv=MV_FLOOR, m_pl_gev=None, labels=LABELS_LADDER):
    """L7c: (label, T_H in GeV, M in kg, remaining lifetime in s, f just above). The cryostat
    temperature (K), the 3-3-1 scale and the Planck mass (GeV) can be handed in."""
    kT = lambda T_K: KB_SI * T_K / GEV_J
    m_pl_kg = math.sqrt(HBAR_SI * C_SI / G_NEWTON) if m_pl_gev is None else m_pl_gev * GEV_J / C_SI**2
    Ts = [kT(t_cryo), kT(T_CMB), M_EL / 4, M_MU / 4, M_PIC_GEV / 4, T_QCD, M_W / 4, M_T / 4, T_EW,
          mv / 4, hawking_T_gev(m_pl_kg)]
    out = []
    for lab, T in zip(labels, Ts):
        M = mass_at_T(T)
        out.append((lab, T, M, lifetime_s(M, variant, mv=mv), f_of_T(T * 1.0001, variant, mv=mv)))
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

    banner("L10a-b  Rung 5's solution in the lab: Newton plus a background that can't entangle (CHECK)")
    d_phi, d_lap = weak_field_of_sds()
    print(f"   Phi = -(c^2/2)(1 - f) for Schwarzschild-de Sitter, minus (-GM/r - Lambda c^2 r^2/6): {d_phi}")
    print(f"   nabla^2 Phi + Lambda c^2 away from the mass: {d_lap}")
    print(f"   entangling combination of the Lambda term, any branch positions: {lambda_cancels_in_entangling_phase()}")

    banner("L10c-d  What is left of Lambda at the diamonds (FOLLOWS, order of magnitude)")
    rel, l, rf = lambda_correction_size()
    print(f"   l = sqrt(3/Lambda) = {l:.3e} m; farthest branch distance {rf * 1e6:.0f} um; (r/l)^2 = {rel:.1e}")

    banner("L10e  The de Sitter correction to the pair energy, with its coefficient (CHECK; FOLLOWS for the frame)")
    resid, dn, dc = de_sitter_pair_correction()
    print(f"   linear in M: U = -(G M m / r)/sqrt(1 - r^2/l^2); series minus (1 + r^2/(2 l^2)): {resid}")
    print(f"   design A: Newtonian {dn:.4f} rad, de Sitter shift {dc:+.2e} rad ({dc / dn:+.1e})")

    banner("L15  The cosmological constant against each rung's vacuum energy (CHECK; LIT; MODEL for w^4)")
    print(f"   S_dS - (3/8) rho_Pl / rho_L = {de_sitter_entropy_identity()}")
    r4, ratios = vacuum_energy_scales()
    print(f"   rho_L^(1/4) = {r4 * 1e3:.3f} meV")
    for k, x in ratios.items():
        print(f"   {k:34s} / rho_L = {x:.1e}")
    print("   nothing in the repository cancels these: the problem is quantified, not solved.")

    banner("L16  Quasinormal modes from Leaver's continued fraction, and the fit at zero spin (CHECK)")
    for n in (0, 1):
        w = leaver_qnm(n)
        print(f"   l = 2, n = {n}: M omega = {w.real:.6f} {w.imag:+.6f} i")
    fr, er, fq, eq = bcw_at_zero_spin()
    print(f"   Berti-Cardoso-Will at chi = 0: M omega_R {fr:.4f} vs exact {er:.4f} ({100 * (fr / er - 1):+.1f}%);"
          f"  Q {fq:.3f} vs {eq:.3f} ({100 * (fq / eq - 1):+.1f}%)")

    banner("L17  The ABJ anomaly coefficient, derived (CHECK, symbolic)")
    ok, lam, holds, coef = abj_fujikawa()
    print(f"   Euclidean gamma matrices satisfy the Clifford algebra: {ok};  tr[g5 sigma_mn sigma_rs] = {lam} eps_mnrs"
          f" for all 256 index sets: {holds}")
    print(f"   |Jacobian| = {coef} x e^2 eps F F / (32 pi^2): the divergence is e^2 eps F F / (16 pi^2) in magnitude")
    d1, d2 = abj_landau()
    print(f"   eps F F - 8 F12 F34 = {d1};  Fujikawa divergence minus the Landau-level count 2(eB/2pi)(eE/2pi) = {d2}")
    print(f"   pi0 -> gamma gamma amplitude from the anomaly over alpha N_c (Q_u^2 - Q_d^2)/(pi f_pi): {abj_pion_amplitude()}")

    banner("L18  The rho parameter from the top-bottom loop, and M_W (CHECK; LIT for the rest)")
    ward, pole, s2dep, diff, lim = rho_parameter_loop()
    print(f"   vector-current Ward identity 2 LL + 2 LR at equal masses: {ward};  1/eps pole left in Delta rho: {pole};"
          f"  s^2 dependence left: {s2dep}")
    print(f"   loop result minus N_c G_F/(8 sqrt2 pi^2) [m_t^2 + m_b^2 - 2 m_t^2 m_b^2 ln(m_t^2/m_b^2)/(m_t^2 - m_b^2)]: {diff};"
          f"  m_b -> 0: {lim}")
    drho, dal, steps, rest = w_mass_steps()
    print(f"   Delta rho = {drho:.3e} (m_t = {M_T_GEV}, m_b = {M_B_GEV} GeV);  Delta alpha = {dal:.5f}")
    for lab, (mw, dr) in zip(("tree", "+ Delta alpha", "+ top loop", "+ Higgs log"), steps):
        print(f"   {lab:14s} M_W = {mw:.3f} GeV  (Delta r = {dr:+.4f})")
    print(f"   measured {MW_MEAS} GeV; the remainder Delta r_rest that closes it: {rest:+.4f} (not computed here)")

    banner("L19  Hawking radiation as radiation: the Bogoliubov coefficients (CHECK)")
    de, dg, rat, ex = bogoliubov_checks()
    print(f"   int x^(iy) e^(-s x) dx against Gamma(1+iy) s^(-1-iy): difference {float(de):.1e};"
          f"  |Gamma(1+iy)|^2 - pi y/sinh(pi y): {float(dg):.1e}")
    print(f"   |beta/alpha|^2 from the continued integrals {float(rat):.10f}; e^(-2 pi w/kappa) = {float(ex):.10f}")
    unit, nplanck, flux = bogoliubov_symbolic()
    print(f"   |alpha|^2 - |beta|^2 - 1/(2 pi kappa Omega) = {unit};  |beta|^2/(|alpha|^2 - |beta|^2) - 1/(e^(2 pi w/kappa) - 1) = {nplanck}")
    print(f"   (1/2 pi) int w n dw - pi T^2/12 = {flux}  (one massless 1+1 field)")

    banner("L20  Kerr quasinormal modes: the ringdown fit at the spin GW250114 uses (CHECK; LIT)")
    print(f"   Leaver's coupled continued fractions against BCW Table II (11 spins, l = m = 2, n = 0): largest difference {kerr_table_check():.1e}")
    ef, eq = kerr_fit_errors()
    print(f"   the fit against the exact modes, chi = 0 to 0.99: largest errors {100 * ef:.2f}% (F), {100 * eq:.2f}% (Q);"
          " BCW state 1.85% and 0.88%")
    import black_holes as BH
    mf, chif, a_f, a_min = area_law_exact()
    fit_mf, fit_chi = BH.invert_220(BH.F220, BH.G220, BH.GW_Z)
    a_i, a_fit, a_i_max, a_fit_min, _ = BH.area_law()
    print(f"   GW250114 ringdown alone: exact M_f = {mf:.2f} Msun, chi_f = {chif:.3f} (fit {fit_mf:.2f}, {fit_chi:.3f});"
          f" final area {a_f:.4g} km^2 (fit {a_fit:.4g})")
    print(f"   least favourable corner: final {a_min:.4g} km^2 (fit {a_fit_min:.4g}) against initial {a_i_max:.4g}")

    banner("L21  The retarded Casimir-Polder step in an exactly solvable retarded system (CHECK; FOLLOWS for the dyadic case)")
    for r, (ex, fo, st) in retarded_pair_energy().items():
        print(f"   r = {r:2d}: U from the normal modes {ex:.12e};  ln det, retarded G(xi) {fo:.12e};  static G(0) {st:.6e}")
    x, x2 = casimir_polder_order()
    print(f"   design A's gap: alpha G ~ K R^3/r^3 = {x:.1e}; the term beyond P3's is relatively {x2:.0e}")

    banner("L22  B7's +0.35% on M_Z decomposed through the MS-bar relations (CHECK; LIT: PDG 2024)")
    mb_ = mz_bookkeeping()
    print(f"   Dr0 = 1 - alpha/alpha-hat = {mb_['dr0']:.5f};  B7's tree M_Z = {mb_['tree']:.3f} GeV;"
          f"  (1 - Dr0)/[(1 - Dr_W) rho-hat] -> M_Z = {mb_['pred']:.4f} GeV (measured {mb_['mz']})")
    print(f"   gap of the prediction from the tree {100 * mb_['gap']:+.3f}%, measured gap {100 * mb_['measured_gap']:+.3f}%")
    print(f"   in M_Z^2: rho-hat {100 * mb_['parts'][0]:+.3f}%, (1 - Dr0)/(1 - Dr_W) {100 * mb_['parts'][1]:+.3f}%,"
          f" together {100 * (mb_['ratio2'] - 1):+.3f}%")
    print(f"   L18's one-loop top-bottom rho - 1 = {mb_['drho']:.3e}, {100 * mb_['frac']:.0f}% of rho-hat - 1;"
          f" with it, M_Z = {mb_['pred_one_loop']:.3f} GeV ({100 * (mb_['pred_one_loop'] / mb_['mz'] - 1):+.3f}% from measured);"
          f" Dr_W - Dr0 = {mb_['dr_diff']:.4f} is not derived")

    banner("L23  The dyadic Casimir-Polder step from photon exchange: two blind builds (CHECK)")
    worst, cross, far, near = qed_cp_accepted()
    print(f"   12-diagram perturbation theory (accepted build a) against rung 3's Green-tensor integral, r w0 = 0.05 to 20: worst difference {worst:.1e}")
    print(f"   build b (a different reduction) against build a at r w0 = 1: {cross:.1e};  derived far coefficient {far:.6f} (23/(4 pi) = {23 / (4 * math.pi):.6f}),"
          f" near coefficient {near:.6f}")

    banner("L24  The emission weights of L7, derived by the grey-body campaign (CHECK; FOLLOWS for the charged weight)")
    gw = grey_weights()
    for s_, (d_, q_) in gw.items():
        print(f"   spin {s_}: P = {GREY_P[s_]:.5e}/M^2, weight {d_:.5f} (quoted {q_}, {100 * (d_ / q_ - 1):+.1f}%)")
    fq, fd, fall = grey_f_standard_model()
    print(f"   Standard Model f: quoted weights {fq:.3f}; derived weights, charged fermions at the quoted 0.142: {fd:.3f}; derived 0.1465 for every fermion: {fall:.3f} (Carr: 15.35)")
    print(f"   accepted build a's Gamma against the independent solver at 6 reference points: worst {grey_gamma_against_reference():.1e}")

    banner("L25  Hawking radiation from a collapsing shell: the map behind L19, derived (CHECK)")
    resid, kinv, kh1 = null_shell_map()
    print(f"   u(v) from the ray through the centre minus v - 4M ln((v_H - v)/4M): {resid};  1/kappa from du/dv ~ (1/kappa)/(v_H - v): {kinv};"
          f"  H1's |f'(r_h)|/2 = {kh1}")
    for w_, wp_ in ((0.05, 0.4), (0.05, 5.0), (0.1, 50.0), (0.1, 0.12)):
        num, closed = shell_bogoliubov_ratio(w_, wp_)
        print(f"   w = {w_}, w' = {wp_}: |beta/alpha|^2 from the overlap integrals {num:.9e}; ((w'-w)/(w'+w))^2 e^(-8 pi M w) = {closed:.9e}")

    banner("L26  The Higgs term of L18: its coefficient derived by two blind builds (CHECK; FOLLOWS for the finite shape)")
    derived, quoted, rho125, lead125 = higgs_term_derived()
    print(f"   -(c^2/s^2) x [log coefficient of Delta rho] = {derived:.9e};  L18's quoted 3 G_F M_W^2/(8 sqrt2 pi^2) = {quoted:.9e}  (ratio {derived / quoted:.12f})")
    print(f"   Delta rho(125.2) - Delta rho(M_W) = {rho125:.4e}; the leading log alone would give {lead125:.4e} ({rho125 / lead125:.2f} of it)")

    banner("L11a  The de Sitter horizon: rung 5's Lambda through rung 6's area law (CHECK, symbolic)")
    d_rc, d_k, d_A, d_S, d_S2, fac = de_sitter_entropy_symbolic()
    print(f"   r_c - l = {d_rc};  kappa - 1/l = {d_k};  A - 12 pi/Lambda = {d_A}  (A = 4 pi l^2; not 4 pi/Lambda)")
    print(f"   S - 3 pi/Lambda = {d_S}  (G = c = hbar = k_B = 1): S = pi x 3/(G Lambda), rung 5's coupling times pi")
    print(f"   S / (pi c^3/(G hbar Lambda)) = {fac}: the entropy is three times that form")

    banner("L11b-c  The first law at every horizon, and de Sitter as the entropy maximum (CHECK)")
    print(f"   dM/dr_h - (f'(r_h)/4 pi) dS/dr_h for SdS, any horizon: {first_law_every_horizon()}")
    ident, worst = sds_entropy_bound()
    print(f"   r_b^2 + r_c^2 + (r_b + r_c)^2 - 2 l^2 (Vieta, exact): {ident};"
          f"  max (S_bh + S_c)/S_dS over 0 < 9 M^2 Lambda < 1: {worst:.6f} < 1")

    banner("L11d  The vacuum's entropy at the measured Lambda (CHECK; LIT Lambda)")
    l, A, S, T, r1, r2 = de_sitter_numbers()
    print(f"   l = {l:.3e} m;  A = {A:.3e} m^2;  S_dS = {S:.3e} k_B;  T_dS = {T:.2e} K")
    print(f"   S_dS / (pi x 3/(G Lambda)) = {r1:.6f};  S_dS / (pi c^3/(G hbar Lambda)) = {r2:.6f}")

    banner("L12a-b  Neutrino mass: the lepton triplets and the seesaw algebra (CHECK)")
    for v, q in lepton_triplets().items():
        print(f"   beta = {v:8s} lepton triplet charges {q}")
    prod, resid, inv = seesaw_symbolic()
    print(f"   seesaw: lambda_1 lambda_2 + m_D^2 = {prod} (exact);  light - (m_D^2/M - m_D^4/M^3) = O(m_D^6): residual {resid}")
    print(f"   inverse seesaw: characteristic polynomial at mu m_D^2/(m_D^2 + Lambda^2), to first order in mu: {inv}")

    banner("L12c-d  The scale, the Yukawas it leaves free, and the data (CHECK; MODEL; LIT)")
    sn = seesaw_numbers()
    print(f"   M_V = 4 TeV: w = 2 M_V/g = {sn['w'] / 1e3:.2f} TeV (g = {sn['g']:.4f});  M = y_R w/sqrt2 = {sn['M'] / 1e12:.2f} TeV (y_R = 1)")
    print(f"   m_light = {sn['light']:.4f} eV needs y_D = {sn['yD']:.2e} = {sn['ratio']:.2f} x the electron's {sn['ye']:.2e};"
          f"  m_D/M = {sn['suppress']:.1e}")
    print(f"   y_D = y_e gives {sn['m_with_ye']:.4f} eV;  log-log slope of m_light against w at fixed Yukawas: {sn['slope']:.6f}")
    tot, bound = neutrino_data()
    print(f"   NuFIT 6.0 (normal ordering): minimal sum {tot:.4f} eV; Planck 2018: < {bound} eV. The Yukawas stay inputs.")

    banner("L13a-b  First post-Newtonian correction to the entangling phase (CHECK; KNOWN EIH terms)")
    print(f"   EIH test-mass limit minus the harmonic-coordinate geodesic Lagrangian, to 1/c^2: {eih_test_mass_limit()}")
    dn, dp, dq = eih_phase_shift()
    print(f"   design A: Newtonian {dn:.4f} rad;  v-dependent 1PN {dp:+.2e} rad ({dp / dn:+.1e});"
          f"  G^2 term {dq:+.2e} rad ({dq / dn:+.1e})")

    banner("L14  The Bekenstein bound (CHECK)")
    R, bek, holo, atoms = diamond_bounds()
    print(f"   2 pi R E/(hbar c) - A/(4 l_P^2) for Schwarzschild: {bekenstein_saturation()}")
    print(f"   design A's diamond: R = {R * 1e6:.2f} um, {atoms:.2e} atoms;  Bekenstein bound {bek:.2e} k_B,"
          f" holographic bound {holo:.2e} k_B")

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
