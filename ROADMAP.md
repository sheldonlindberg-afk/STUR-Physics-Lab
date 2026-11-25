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

## Phase 2: anomalies, charge quantization, family number (Part R)
- [~] Hypercharges from anomaly cancellation (exact); 3-3-1: anomaly freedom needs the number of
      families to equal the number of colours.

## Phase 3: baryon asymmetry and leptogenesis
- [ ] SM electroweak baryogenesis: CP violation (Part O's invariant) and the transition strength
      (Higgs mass) against eta_B.
- [ ] Leptogenesis: Davidson-Ibarra bound on the lightest right-handed neutrino against Part P's
      seesaw window.

## Phase 4: SO(10)
- [ ] Right-handed neutrino in the 16; seesaw scale tied to M_GUT; t-b-tau unification at large
      tan(beta); joint quark-lepton Yukawa relations.

## Phase 5: extend Part M
- [ ] Add neutrino masses, the strong CP solution, proton decay and eta_B as conditions; one table
      of which complete hypothesis survives everything.

## Later
- One running for every coupling (matrix Yukawas to M_GUT); GUT and superpartner thresholds;
  dark matter (axion misalignment, LSP); inflation (Higgs inflation vs lambda(M_P) < 0);
  electroweak precision (M_W).
