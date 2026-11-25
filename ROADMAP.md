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
3. [ ] Deferred: proton-decay operator running above M_I in each chain. A general pair-exchange rule
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
4. [ ] Still deferred: proton-decay operator running above M_I (round 2, item 3), until its
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

## Later
- One running for every coupling (matrix Yukawas to M_GUT); GUT and superpartner thresholds;
  dark matter (axion misalignment, LSP); inflation (Higgs inflation vs lambda(M_P) < 0);
  electroweak precision (M_W).
