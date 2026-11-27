# Roadmap: toward a complete unification attempt

The phases below are worked through in order. Each phase becomes one or more Parts of
`production_v2_2.py`, under the same rule as the rest: measured inputs in `INPUTS`, judging data
in `COMPARISONS`, published coefficients in `LITERATURE` with a self-check, unknowns scanned.
Numbers may be off while pieces are added; each entry says what is done and what is still open.

Status: [x] done, [~] in progress, [ ] not started.

## Done so far
- [x] Parts A-M: cosmology, quark flavour and textures, 3-3-1, flavour symmetries, closure,
      quantum gravity, alpha from unification, Yukawas, MSSM Higgs, SM criticality, joint test.
- [x] Part N: closed mass formulas (Koide), pole vs running masses.
- [x] Part O: strong CP angle (nEDM bound via chiral log; m_u = 0, axion, parity).
- [x] Part P: neutrino masses and mixing (cosmology, KATRIN, KamLAND-Zen; TBM, BM, GR, TM1, TM2).

## Phase 1: proton decay (Part Q) -- done
- [x] 1a. Dimension-six gauge-boson exchange, p -> e+ pi0, at Part I's M_GUT and alpha_GUT (MSSM)
      and at the SM's g1 = g2 point; short-distance factors from the RGE (exponents from the
      script's own b_i), long-distance factor from the script's QCD running; lattice matrix
      elements; against Super-K. Open: two-loop A_L (one loop used; 1.247 at two loops is quoted),
      GUT thresholds (M_X = M_GUT assumed). Result: MSSM 2.4e35 yr (10x the
      Super-K limit), SM g1 = g2 point 5e23 yr (excluded).
- [x] 1b. Dimension-five p -> nubar K+ in minimal SUSY SU(5), with M_S (Part I), tan(beta)
      (Part J), M_HC = M_GUT, GUT phases scanned (Hisano et al. 2013, eqs. 15-49). Result:
      3e28-7e29 yr vs 5.9e33: excluded. Open (debug): the higgsino part is a factor 2.2 shorter
      than their eq. 19 scaling; wino/higgsino thresholds below M_S; two-loop running; the
      CKM phases in the operator coefficients checked against their conventions; at tan(beta) =
      1.313 y_t(M_HC) = 3.55 is just past sqrt(4 pi), at the edge of perturbation theory.
- [ ] 1c. Feed proton decay into Part M as a condition (done in Phase 5).

## Phase 2: anomalies, charge quantization, family number (Part R) -- done
- [x] Hypercharges from anomaly cancellation (exact): SM unique with Yukawas; charge quantized;
      nu_R opens B - L, closed by a Majorana mass. Witten's anomaly. 3-3-1: N_f a multiple of 3,
      exactly 3 with asymptotic freedom.
- [ ] Later: the full 3-3-1 anomaly set with leptons and U(1)_X (Part D has the quarks only).

## Phase 3: baryon asymmetry and leptogenesis (Part S) -- done
- [x] eta_B from Omega_b h^2 and T_CMB. SM: sphaleron conversion 28/79 (exact), crossover for the
      measured m_h (31 sigma above the lattice endpoint), CP measure 4e-24: fails.
- [x] Leptogenesis: prefactor 0.96e-2 from the field content; Davidson-Ibarra needs M_1 > 3e8 GeV,
      inside Part P's window. Open: the washout efficiency kappa (bounded by 1 here) from the
      Boltzmann equations; flavour effects; the reheating temperature and, in the MSSM, gravitinos.

## Phase 4: SO(10) (Part T) -- done (first pass)
- [x] Group theory: B - L needs nu^c; sin^2 theta_W = 3/8, normalization 3/5 (exact).
- [x] Minimal 10_H Yukawa relations: excluded. t-b-tau (MSSM): needs a ~+28% m_b threshold.
- [x] Non-SUSY SO(10) via Pati-Salam (one loop): M_I = 5.5e11, M_GUT = 1.1e16 GeV, tau_p ~ 6e35 yr;
      M_I inside the leptogenesis window. Open: two-loop running with thresholds; the other chains
      (SU(3) x SU(2)_L x SU(2)_R x U(1)_{B-L}, with and without D-parity); operator running above M_I
      in the proton lifetime; Part L's lambda running only up to M_I (new vacuum-stability test).

## Phase 5: one scorecard (Part U) -- done (first pass)
- [x] Three complete hypotheses (SM to M_P, minimal SUSY SU(5), SO(10) via Pati-Salam) against
      unification, b-tau, Higgs mass, neutrino masses, proton decay, baryon asymmetry, strong CP.
      Result: only SO(10) via Pati-Salam fails nothing at one loop; lambda(M_I) = 0 gives
      m_h = 126.1 GeV (~1 sigma). Open: the justification for lambda(M_I) = 0; fold the new
      conditions into Part M's chi^2 machinery.

## Next round (proposed order)
1. [x] Two-loop running for every minimal chain (PS, PS+D, LR, LR+D; Part T5): b from the field
   content (checked on the SM); none predicts a coupling (unknowns = conditions). Two loops:
   PS M_I = 1.4e11, M_GUT = 8.0e15 GeV; both D-parity chains excluded by proton decay;
   lambda(M_I) = 0 gives 125.6 (PS), 123.3 (LR) GeV. Open: threshold corrections (tree matching).
2. [x] What lambda(M_I) is (Part T6): lambda_SM(M_I) = lambda_H - lambda_HS^2/lambda_S (tree threshold,
   Elias-Miro et al. 2012), unknown shift; lambda(M_I) = 0 is not required. Stability needs M_I < mu_0
   = 6.2e10 GeV (2.3e10-2.0e11 for M_t +- 1 sigma): LR, LR+D stabilizable; PS undecided (inside the
   band); PS+D metastable. Open: the Pati-Salam quartics' own running and positivity above M_I.
3. [x] (Done in item 4 of 'Next', below.) Deferred: proton-decay operator running above M_I in each chain. A general pair-exchange rule
   reproduces the SM's SU(3) exponent but not SU(2) (same- vs opposite-chirality pairs differ), so the
   one-loop anomalous-dimension formula for B-violating operators must be transcribed from a source
   (e.g. Abbott-Wise 1980; Alonso, Chang, Jenkins, Manohar, Shotwell 2014) and checked against Part Q's
   printed SM exponents first. The dimension-5 factor 2.2 against Hisano et al.'s eq. 19 is also open:
   eq. 19 is itself an approximation (hadronic and CKM factors dropped), so it may not be a bug.
4. [x] Leptogenesis efficiency (Part S): kappa_f from BDP eqs. 22, 59 (z_B solved exactly), m_* from g*
   and M_P; SM CP bound with 16 pi (BDP eq. 31). M_1 >= 6.5e8 GeV at kappa = 1; 1.5e10-1.3e11 GeV over
   m_sol <= m~_1 <= m_atm. PS covers it; LR (M_I = 2.8e9) needs weak washout. Open: scatterings,
   flavour effects, dynamical initial abundance.

## Round 3 (in order)
1. [x] Dark matter from the axion (Part V): misalignment from its ingredients (Di Luzio et al. eqs.
   148-169; eq. 170 reproduced to 1.3 %). All the DM post-inflation at f_a = 2.0e11 GeV; at PS's M_I
   65 % (strings add more), at LR's M_I under 1 % and no angle suffices. Open: string yield; lattice
   chi(T) instead of the instanton gas; feeding Omega_c back into Part A.
2. [x] Threshold corrections (Part T7): each matching condition shifted by up to +-1 in 1/alpha (assumed
   band), every corner at two loops. Only PS+D's exclusion is robust; LR+D's exclusion and the PS and
   LR verdicts can flip. Next: the actual heavy spectrum (scalar potential of 126 + 45/54/210).
3. [x] Electroweak precision (Part W): M_W = 80.350 +/- 0.004 GeV (two-loop SM, Awramik et al.
   parametrization) against 80.360 (no CDF) and 80.369 (PDG average): within 1.4 sigma; reproduces the
   PDG fit (80.353). Open: sin^2 theta_eff, the full set of Z-pole observables.
4. [x] (Done in item 4 of 'Next'.) Still deferred: proton-decay operator running above M_I (round 2, item 3), until its
   anomalous-dimension formula is transcribed from a source and checked on the SM exponents.

## Round 4
1. [x] The heavy spectrum (Part T8, Pati-Salam): each heavy GUT multiplet of the 210, 126, 10 by group
   theory (decompositions checked against SO(10) indices). The SU(2)_L triplets (10,3,1), (15,3,1)
   dominate; proton decay flips if (10,3,1) is ~half of M_GUT; within a factor 10 tau_p spans 1e27-1e43
   yr. The verdicts are set by the scalar potential's couplings, which nothing measured fixes. Open: the
   same for LR (needs the 210 under 3221) and for the M_I thresholds; the potential itself.
2. [x] Part X: Omega_m from Omega_b + axion at PS's M_I + neutrinos; misalignment alone makes the
   universe 15.2 Gyr old (70 sigma): strings/defects must give ~35 % of the DM. Open: the string yield.
3. [x] Z pole (Part W): sin^2 theta_eff = 0.23164 (two-loop parametrization, Awramik et al. 2006) vs
   0.23151 +- 0.00016 (LEP+SLC). Open: Gamma_Z, R_l, the other pseudo-observables.
4. Proton running above M_I and the dimension-five factor 2.2.

## Round 5: the scalar potential
1. [x] The 210's potential (Part T9): all invariants (S2, cubic, Q1-Q4), vev on the PS singlet, masses
   of (15,1,1), (15,3,1), (15,1,3), (10,2,2) from curvatures; Goldstones massless (check). Couplings
   scanned in a perturbative box; ~80 % of viable potentials pass proton decay. Open: boundedness is
   tested on random directions only; the vacuum is local, not shown global; tree level only.
2. [x] The 126's couplings to <210> (Part T10): self-dual 5-form mass matrices; only the D-odd cubic
   splits (10,3,1) from (10bar,1,3); with (10bar,1,3) light, m^2(10,3,1) = 2 eta_2 v exactly. Joint scan
   with the 210: most viable potentials pass proton decay and natural leptogenesis.
2b. [x] The 10's couplings (Part T11): no H H phi cubic; one splitting quartic H_i H_j A_ij (A = 6 v^2 on
   SO(4), 0 on SO(6)); the cubic H S phi mixes the 10's and 126's (6,1,1). Light doublet assumed (the
   doublet-triplet tuning); the lighter colour triplet sits near M_GUT. Open: triplet-mediated proton
   decay (needs Yukawas at M_GUT); a complex 10 (two doublets); the one-loop potential.
3. [ ] The same for the LR chain (210 under SU(3) x SU(2)^2 x U(1)).
4. [x] The Yukawa sector (Part Y): PS excluded by an exact selection rule (light Higgs in one SU(4) irrep:
   M_e = M_d or -3 M_d); the LR chain's 10+126 sum rule reaches the charged leptons (8 unknowns).
5. [x] Type-II neutrinos from the sum rule (Part Y3): excluded at ~21 sigma; b and tau do not converge
   without SUSY ((m_b - m_tau)/m_b = -0.60 at M_GUT). [ ] Type I (and I + II) still to test.
7. [x] Closing the algorithm: Part X takes the scorecard's survivor; Part Z, the ledger of every free
   number with its computed status. The algorithm runs in one pass and closes; it calculates only
   discrete numbers.

## Next (if the attempt continues)
Every step also updates the website: tools/site_data.py regenerates assets/site-data.js, index.html shows
the new result, and the tests fail if a page value, the scorecard, the ledger or README's check count is stale.
1. [x] Type-I seesaw in the LR chain (Part Y4). Type I adds no unknown: M_D = M_u + (3 + c1)/c2 (M_d - M_e)
   is fixed by the sum rule; M_R ~ M_d - M_e, and its masses follow without a vev. Types I + II add one
   complex ratio. Levenberg-Marquardt (quark masses floated within errors, 13 data): type I best chi^2 ~ 160,
   types I + II ~ 18-32, no 3 sigma fit; every near-fit has M_R,3 ~ 1e2-1e3 M_I, above sqrt(4 pi) M_I.
   Neutrino entry stays open. Open: published fits (Joshipura-Patel 2011, Ohlsson-Pernow 2019) find type-I
   solutions with full running, so item 2 decides; leptogenesis from the fitted M_1 once a fit exists.
2. [x] Left-right Yukawa running between M_I and M_GUT (Part Y). The bidoublet theory's one-loop matrix RGE is
   derived, not quoted: the general Machacek-Vaughn formula over every component (checked on the SM's matrix RGE)
   fixes the reduced form exactly. Matrix SM running to M_I, symmetric matching (<Phi> = diag(k1, 0)), left-right
   running to M_GUT (the four couplings meet there: a check). (m_b - m_tau)/m_b at M_GUT: -0.60 -> -0.41.
   Fix: the fits had dropped one physical phase (the overall phase of M_d against M_u): 9 unknowns, 19 model
   parameters. Fits run in parallel (fork), with cross-seeding and kicks.
2b. [x] A reliable neutrino search. The type I + II mixture is now projective, M_nu ~ cos(theta) K^ + sin(theta)
   e^(i phi) D^: as a ratio w, both pure limits were endless flat valleys that trapped the local search. With
   uniform theta starts, mostly structured starts and small kicks, the shipped run finds 15 type I + II fits
   (best chi^2 1.4 for 13 data): delta 136-289 deg (not pinned; an earlier single point at 17 deg was not
   representative), M_R,3 = 177-360 M_I in every fit (perturbative bound 3.5 M_I), M_1 = 4e9-1e10 GeV. Type I
   alone: best chi^2 151; type II: ~19 sigma. Neutrino entry open, with the M_R tension stated. Open: the second
   bidoublet's vev and the Delta_R coupling in the running; whether thresholds (Part T7) can lift M_I enough.
3. [x] The LR chain's own scalar potential and its thresholds.
   [x] 3a. The heavy spectrum by group theory (Part T12): every heavy 3221 multiplet of the 210, 126 and 10 with its
       B - L charge (decompositions checked against the SO(10) indices); threshold responses; and the "lift" (Part Y):
       the smallest spread that brings M_I to where the type I + II fits put B - L breaking while keeping the proton,
       a linear program in the log-masses solved exactly. Answer: within a factor ~1.5 of M_GUT, M_I -> 1.4e11 GeV,
       tau_p at the Super-K limit (binding), vacuum no longer stabilizable.
   [x] 3b. The potential (Part T13): the 210 with both 3221 vevs and the 126 at that vev, multiplets found as
       highest-weight vectors (the 210's two (3,2,2) and two singlets as 2 x 2 blocks), stationarity solved for mu^2
       and eta, the (3,1,1) vector as its own threshold. Checks: decompositions, T9's and T10's PS limits, Goldstones.
       Result: ~1150 viable 210 + 126 potentials; proton passes ~97 %; M_I median ~1e9 GeV (down, not up); none
       lifts M_I to where the neutrino fits need it with the proton kept. Delta_R light drags its SU(2)_R partners
       light, lowering M_I. The 10 (T11's analogue): H_i H_j A_ij splits it; the cubic mixes its triplet with the
       126's (3,1,1) and, through the B - L vev, its doublet with the 126's (1,2,2): the light Higgs is a computed
       10-126 mixture (median ~1/4 126, as Part Y assumes); with it, still none lifts M_I. Open: two-loop
       thresholds; a complex 10 (the Yukawa fits use one).
4. [x] Proton running above M_I; triplet-mediated proton decay with the fitted Yukawas.
   The anomalous dimensions are derived, not transcribed: in Landau gauge only exchanges inside a Lorentz-scalar
   bilinear count, each 6 T_i.T_j (the mass operator's value; T_i.T_j = -(N+1)/2N for epsilon-contracted SU(N)
   fundamentals), and left-right exchanges cancel. This reproduces Ellis et al.'s SM c_i exactly (self-check); the
   earlier failure treated every pair alike. Each chain now runs the operators with its own group above M_I:
   A_S rises 5-16 %, tau_p falls 8-23 %; no verdict flips. Colour triplets (an estimate with the fitted first-
   generation Yukawas, T13's Higgs mixture and triplet mass, Clebsches <= 3): amplitude ~1e-10 of the gauge one,
   so triplets need only M_T >~ 1e11 GeV. Open: the exact triplet Clebsches; the dimension-five factor 2.2 (SUSY).

## After the "Next" round (in order)
5. [x] The left-right chain's neutrino tension (Part Y4 against T12-T13): settled, the chain fails.
   [x] 5a. The scales, sharpened (Part Y4). Perturbativity: M_R,3 <= 2 sqrt(4 pi) M_I/g_R ~ 12.6 M_I (M_WR = g_R v_R,
       M_N = 2 f v_R); the lift then needs x14, a spread of 1.33, and the potential gives it in 4 of 715. But SO(10)'s
       own Y126 (fixed by the charged fermions, ~1e-3) with M_R = Y126 v_R predicts v_R = 1e14-5e14 GeV, 2e4-1e5 times
       the chain's, beyond any threshold (x31): the left-right chain FAILS the neutrinos. No complete hypothesis
       survives; Parts X and Z follow the closest (LR). Open: whether a non-minimal Yukawa sector (a 120, a 16_H
       breaking B - L, non-renormalizable M_R) changes this; 5b and 5c below no longer decide it.
   [x] 5b. A complex 10. A real 10's bidoublet is self-conjugate, so |a| = |c|, i.e. |c2| = |1 - c1|: with that imposed
       the charged-lepton search reaches only chi^2 = 6e3 (m_mu = 0.022 GeV): the 10 must be complex. The fits fix the
       light Higgs's up/down ratios, |a/c| = (1 - c1)/c2 ~ 60 and |b/d| = (-3 - c1)/c2 ~ 30, so the 126 share f splits
       |b|^2 + |d|^2 = k^2 f and |d| = k sqrt(f/(1 + |b/d|^2)): giving all of f to d had overestimated d 30-fold. v_R
       now 4e12-2e13 GeV (800-4000 x the chain's); a perturbative Y126,3 alone keeps it >= 14 x (inside the x31 threshold band), so
       the verdict now rests on T13's 126 share (>= 4 %): 800 x, 25 x beyond thresholds. The chain still fails, with a
       margin 30 x smaller.
       [x] The complex 10's own potential (T13): a light complex bidoublet fixes the 10's doublet masses completely,
       D10 = X X^T/m_126 (three conditions, not two; a real 10 cannot leave two vectors light); two triplets mix with the
       126's (3,1,1), thresholds from the eigenstates; 4073 of 8648 draws viable. The fits' |a/c|, |b/d| pin the light
       Higgs's direction inside the bidoublet (two Apollonius circles), so each point predicts d: 52 points match, and
       every one puts v_R >= 3600 x its own chain's. The exclusion no longer rests on the f band.
   [x] 5c. Thresholds and the rest of the running. At two loops the matching now carries the heavy vectors' MS-bar
       constant, T_i/12 pi (Langacker-Polonsky eq. 12, C^1 = 1/21; T_i = C2(SO(10)) - C2(H_i), a check): no unknown,
       M_I +5 %, M_GUT +4 % in every chain. A second bidoublet vev up to |k2/k1| = m_b/m_t moves (m_b - m_tau)/m_b at
       M_GUT to -0.48..-0.35; the Delta_R coupling (RGE derived from the general formula: +3 Y f^dag f in Y3, Y4;
       6 f f^dag f + 2 Tr(f f^dag) f + A^T f + f A) only makes tau heavier, -1.58 at the largest perturbative f.
6. [x] One running for every coupling: matrix Yukawas to M_GUT with every threshold (SM, chains, MSSM). One engine
       (gauge + the full 3x3 Yukawa matrices, all generations and the CKM mixing) runs the SM from m_t(m_t), the MSSM
       above M_S (tan(beta) matching) and a chain's left-right stage above M_I; Part B's ratios, every mass at M_I and
       M_GUT and the left-right run all use it (the light-quark ratios, held fixed above m_t before, now run). MSSM
       matrix RGE = the general superpotential formula over every component (1e-16); Part J's third-generation
       running = the engine on that subspace (1e-16), and the light generations move it by 0.03 % (SM, at M_P) and
       0.04 % (MSSM y_b/y_tau at M_GUT), so Part J keeps its fast form. Effects downstream are small: the type I + II
       search now finds 19 fits (best chi^2 0.0, 17 unknowns for 13 data), delta 7-342 deg, M_R,3 = 167-720 M_I,
       v_R = 1e14-7e14 GeV from SO(10): the left-right chain still fails the neutrinos. The fit count and the delta
       range move with 1e-8 changes in the inputs (the search lands on different points of a degenerate set), so
       only the right-handed scale is a robust output.
7. [x] Leftovers. The full 3-3-1 set (Part R): with the lepton triplets and every conjugate singlet, SU(3)_C^3,
       SU(3)_L^3, SU(3)_C^2 X, SU(3)_L^2 X, X^3 and gravity^2 X vanish exactly for beta = +-1/sqrt3 (three fail without
       the leptons). The dimension-five factor: the full higgsino term has eq. 19's scaling exactly (one constant,
       1.77e35 years, at every tan(beta)); the factor 2.3 is 1.65 from the newer lattice alpha_p (-0.0144 vs -0.0112
       GeV^3) times 1.37 from eq. 19's one-digit constant and 2013 inputs: not a bug (a check).
8. [x] Dark matter and inflation (Part AA). Every one of the minimal theory's 28 multiplets is even under
       R = (-1)^(3(B-L)+2s), the Z2 the 126 leaves: no candidate besides the axion (0.7 %); one needs a scalar 16 or a
       fermionic 10/45/54 (mass a new unknown). Slow roll from each potential (N = 50-60): minimal phi^4 and phi^2
       excluded by r; the xi phi^2 R plateau (n_s 0.962-0.968, r 0.003-0.004) allowed; SM Higgs inflation excluded
       (lambda < 0 above mu_0 = 6e10 GeV: the CMB would need lambda ~ 1e21). A 210/126 direction with its own xi can
       inflate: allowed, not predicted.

## Adjacent sims (sims/, one piece changed at a time)
1. [x] so10_flavour: SO(10) in place of 3-3-1 (Parts D, E, R). Symmetric Yukawas (exact spinor algebra) remove the
       Part C survivor's prediction; minimal SO(10) x Z_N (N <= 6) gives 15 predictive classes, all excluded by fits
       (> 100 sigma); family number bounded 3-5. Open: the 81 classes with one more Higgs field; several light doublets.
2. [x] Part T14 (in so10_flavour): the two-step left-right chain SO(10) -> 3221 -> 3211 -> SM. M_R stays near 1e9 GeV
       for any M_BL, v_R <= M_R/g_R ~ 2e9 GeV: fails the neutrinos (38x short at the perturbative floor). Open: chains
       with SU(2)_R broken far higher, a 16_H for B - L, a 120 in the Yukawas.

## Later
- GUT and superpartner thresholds beyond tree level;
  dark matter (axion misalignment, LSP); inflation (Higgs inflation vs lambda(M_P) < 0);
  electroweak precision (M_W).
