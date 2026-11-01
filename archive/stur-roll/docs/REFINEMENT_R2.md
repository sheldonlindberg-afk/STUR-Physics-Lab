# Refinement round 2: synthesis and verification

Date: 2026-10-31. Four items were worked in parallel and then each was
checked independently. The detailed reports are:

| Item | Report | Script | Runtime |
|---|---|---|---|
| R2.1 A prediction that distinguishes STUR-ROLL from LMTY [3] | [`R2_DISTINCT_PREDICTION.md`](R2_DISTINCT_PREDICTION.md) | `src/checks/r2_distinct_prediction.py` | ~2 min |
| R2.2 The level argument on S&sup1;/Z&#8322; | [`R2_ORBIFOLD_LEVEL.md`](R2_ORBIFOLD_LEVEL.md) | `src/checks/r2_orbifold_level.py` | ~2 s |
| R2.3 Collider bound on the KK hypercharge boson | [`R2_KK_PHOTON_BOUND.md`](R2_KK_PHOTON_BOUND.md) | `src/checks/r2_kk_photon_bound.py` | &lt; 1 s |
| R2.4 Seed statistics and anisotropic birefringence | [`R2_SEED_ANISOTROPY.md`](R2_SEED_ANISOTROPY.md) | `src/checks/r2_seed_anisotropy.py` | ~25 s |

## How the work was checked

- **Every script was re-run from scratch** after its author finished. All four
  exit cleanly and reproduce the numbers quoted in their reports.
- **Key results were re-derived independently:**
  - R2.2, &int;&#8320;^&pi; c_g d&theta; = &pi;/2 exactly: from the R1.1 closed form,
    &frac12; sinh a &middot; &int;&#8320;^&pi; d&theta;/(cosh a &minus; cos &theta;) = &frac12; sinh a &middot; &pi;/sinh a = &pi;/2.
  - R2.2 reproduces H_c = 15.06/L and T_c = 9.78/L, matching `stur_final.py`'s 15.1/L and 9.8/L.
  - R2.3, the contact-interaction formula: summing the KK tower gives
    2g_Y&sup2;Y_iY_j &sum;1/(nM&#8321;)&sup2; = (&pi;&sup2;/3)g_Y&sup2;Y_iY_j/M&#8321;&sup2;. Matching to
    4&pi;/&Lambda;&sup2; gives &Lambda;/M&#8321; = &radic;(12/(&pi;g_Y&sup2;|Y_iY_j|)), as reported.
  - R2.3, the convention: `g_mass(x = ML)` carries the factor e^(&minus;ML) of a single
    winding, so L is the circumference of the covering circle and M&#8321; = 2&pi;/L.
  - R2.1, the energy release: &rho;_&theta;/&rho;_tot = (2/3)(m/H)&sup2;(f/M_Pl)&sup2;. Release at
    H = m/19.5 instead of m/3 increases the fraction by (19.5/3)&sup2; &asymp; 42.
  - R2.1, the tomography: &Delta;&beta; = (r &minus; 1)&beta;_rec, with r = &beta;_reio/&beta;_rec from
    `HYPOTHESIS.md`, gives &minus;0.165&deg; at 3&times;10&#8315;&sup3;&sup1; eV and &minus;0.208&deg; at
    10&#8315;&sup3;&#8304; eV. Both match R2.1.
  - R2.4, the seed: &beta; = (&alpha;/2&pi;)(&pi; &minus; |&theta;_i|) with |&theta;_i| &asymp; s&#8320;&radic;N. For
    N = 60, a loss under 3% requires s&#8320; &lesssim; 0.012, as reported.
- **The one external number that contradicted round 1 was re-checked.** A
  separate search confirms the ACT DR6 anisotropic result: A_CB = 0.05 &plusmn; 0.06,
  A_CB &lt; 0.15 at 95% [21].
- **Cross-consistency between items.** R2.1's mass window
  (2&times;10&#8315;&sup3;&sup1; &ndash; 10&#8315;&sup2;&#8312; eV) assumes a seed of 10&#8315;&#8308;, which lies inside R2.4's
  narrowed seed window. R2.1's probability of a wall in our Hubble volume
  (0.1&ndash;0.2) and R2.4's reionization-patchiness model rest on the same
  random-walk seed statistics. R2.3's anomaly-freedom condition (no chiral
  zero mode of &psi;) is exactly what R2.2 established: the (M, &minus;M) pair has no
  zero mode. **No conflicts found.**

## Results

### R2.1 What separates STUR-ROLL from LMTY [3]?

- **Nothing does, across all of LMTY's parameter space.** STUR-ROLL is a
  special case of their scenario: c_&gamma; = 1 with a mass in a fixed window.
- **But STUR-ROLL is sharper, and that makes it falsifiable on its own.**
  - The derived amplitude &alpha;/2 holds (within 3%) only for
    **2&times;10&#8315;&sup3;&sup1; &lesssim; m &lesssim; 10&#8315;&sup2;&#8312; eV**. In this window &theta; rolls at z &asymp; 4&ndash;300.
  - Throughout the window, **&Delta;&beta; = &beta;_reio &minus; &beta;_rec &isin; [&minus;0.209&deg;, &minus;0.146&deg;]**,
    i.e. &minus;(0.70&ndash;1.00) &times; &alpha;/2. LiteBIRD's expected error,
    &sigma;(&Delta;&beta;) &asymp; 0.05&deg; [N1], makes this a 2.9&ndash;4.2&sigma; detection.
  - **If LiteBIRD finds |&beta;| &asymp; 0.2&deg; together with &Delta;&beta; &asymp; 0, STUR-ROLL is
    falsified.** That outcome also separates STUR-ROLL from an instrumental
    miscalibration (which gives &Delta;&beta; = 0) and from LMTY's late-roll
    (dark-energy) branch.
- **&theta; is not dark energy.** It holds at most 1% of &rho;_DE before it rolls,
  rolls at redshifts above DESI's range, and has &Omega;_&theta; &lesssim; 10&#8315;&#8309; today. LMTY
  tie their axion to DESI's evolving dark energy; STUR-ROLL predicts no such
  connection.
- **Not discriminators:** the seed spectrum, the potential shape,
  gravitational waves from the T_c transition (&Delta;V/&rho;_rad &le; 10&#8315;&#8310;&#8313;), and the KK
  photon, which is allowed but not predicted (see R2.3).

### R2.2 The level argument on the orbifold: **it survives, and becomes exact**

- **The fermion content.** A Z&#8322;-odd U(1)_B maps q_B &rarr; &minus;q_B, so &psi; must be a pair
  with (q_B, Q) = (&plusmn;1, 1). The orbifold forces their bulk masses to be (M, &minus;M).
  Together they form exactly one Dirac field on the covering circle, with a
  constant mass (not a kink) and **no zero mode**. This was checked with
  explicit Dirac matrices.
- **The Chern&ndash;Simons term is allowed.** B&and;F&and;F is Z&#8322;-even, so a constant level
  is allowed, and no fixed-point anomaly needs cancelling.
- **&theta; keeps period 2&pi;.** The large gauge transformations are Z&#8322;-odd and
  survive the projection. They equal (&minus;1)&#8319; at y = &pi;R, so **brane mixing of &psi;
  with an SM lepton is allowed only at y = 0**.
- **New exact result:** &Phi;(&pi;) &minus; &Phi;(0) = (&pi;/2) sgn M for every MR. Hence
  **&beta; = k_eff &middot; &alpha;/2 exactly**, with no e^(&minus;2&pi;MR) correction, and
  k_eff = &kappa; + &frac12; sgn M with &kappa; &isin; &Zopf; + &frac12;.
- **New caveat 1: global structure.** k_eff &isin; &Zopf; assumes the
  [SU(3)&times;SU(2)&times;U(1)]/Z&#8326; global structure with a colourless &psi; [N2.1, N2.2].
  Other global structures allow fractional levels.
- **New caveat 2: the roll distance.** &Delta;&theta; = &pi; requires the scalar and the
  fermion to carry the same B charge and boundary twist. A single
  C-projected scalar moves the trigger to H_c &asymp; 16.7/L and T_c &asymp; 10.8/L.

### R2.3 KK hypercharge bound: **R1.4 was too strong by a factor of 2&pi;**

- **Only U(1)_Y has to be in the bulk**, because &psi; is an SU(2)-singlet lepton
  with Y = &minus;1. The bound therefore applies to KK hypercharge bosons B_Y^(n),
  which couple to brane fermions with strength &radic;2 g_Y Y.
- **Dilepton searches.** ATLAS and CMS limits on a sequential-SM Z&prime; apply
  directly and conservatively: **M&#8321; &gt; 5.1&ndash;5.5 TeV** [N3.1&ndash;N3.3]. A rate rescaling
  (&sigma;&times;BR about 4&ndash;5 times larger) pushes this to about 6.0&ndash;6.3 TeV.
- **Contact interactions** from the whole tower give M&#8321; &gtrsim; 5.3 TeV
  (indicative only).
- **Convert to the length L.** In `stur_final.py` L is the circumference, so
  M&#8321; = 2&pi;/L and **1/L &gtrsim; 0.8&ndash;1.0 TeV**. Round 1 applied the 5 TeV figure
  directly to 1/L; that was wrong.
- **Section E after the fix.** The rows with 1/L = 1 TeV sit at the edge of the
  bound, and the lightest viable &psi; is about 1.4&times;10&#8309; GeV. A KK hypercharge
  boson near 6 TeV with 4&ndash;5 times the SSM dilepton rate is reachable at the
  HL-LHC, but only at that edge. It is the only collider-accessible corner of
  the model.

### R2.4 Seed, walls and anisotropy

- **Correction to round 1.** The ACT DR6 anisotropic bound is **A_CB &lt; 0.15**
  (A_CB = 0.05 &plusmn; 0.06), not 0.52 [21]. The 0.53 belongs to SPT with a lensing
  prior.
- **The seed window narrows.** In the de Sitter phase &theta;'s curvature is of
  order m&sup2; &laquo; H&sup2;, so &theta; random-walks instead of sitting at 0. This gives
  &beta; = (&alpha;/2)(1 &minus; |&theta;_i|/&pi;). With 60 or more e-folds, keeping &beta; within 3% of
  &alpha;/2 needs **s&#8320; &lesssim; 1.2&times;10&#8315;&sup2;**, i.e. H_nuc &lesssim; 0.08 f. The upper part of
  `stur_final.py`'s window (10&#8315;&#8308; to 0.3) is therefore excluded.
- **A conditional constraint.** *If* the nucleation phase is the archived
  GENESIS R&sup2; inflation (H &asymp; 1.5&times;10&sup1;&sup3; GeV), then f &gtrsim; 1.8&times;10&sup1;&#8308; GeV, which
  excludes m &gtrsim; 10&#8315;&sup2;&#8313; eV.
- **Recombination photons:** the rotation is isotropic. The anisotropy is at
  most A_CB &asymp; 10&#8315;&sup3;, so the claim is confirmed.
- **Reionization photons:** a scattering point inside an opposite-sign domain
  is rotated by **&alpha; = 0.418&deg;**, not &asymp; 0. The sky rms is 0.02&ndash;0.20&deg;, and the
  power is at most A_CB &asymp; 0.045 in the models considered. The absolute
  maximum is (&alpha;/2)&sup2;, i.e. A_CB = 0.13, concentrated at &ell; &lesssim; 10.
  - Current ACT, SPT and BICEP estimators do not probe these scales.
  - The relevant constraint is Planck's tomographic reionization analysis
    [N4.4]; its numerical value is still unverified †.
  - **Nothing in the mass window is excluded.**
  - The calibration-free bound |&beta;(2) &minus; &beta;(30)| &le; &alpha;/2 still holds, but its
    sign is no longer fixed.
- **Wall energy:** at the upper edge of section C, &delta;T/T &asymp; 3&times;10&#8315;&#8309; and
  &Omega;_wall &asymp; 4&times;10&#8315;&#8309;. This is marginal, and applies only if a wall lies
  inside our horizon.
- **Time-dependent &beta; today:** the period is 4&times;10&#8311;&ndash;4&times;10&#8312; yr and the
  amplitude at most 7&times;10&#8315;&sup3;&deg;, so the change over 5 yr is about 5&times;10&#8315;&sup1;&#8304;&deg;.
  This is unobservable and closes R1 open item 5.

## Corrections applied to the docs in this round

| Where | Was | Now |
|---|---|---|
| R1.4 / STATUS | 1/L &gtrsim; 5 TeV (placeholder) | 1/L &gtrsim; 0.8&ndash;1.0 TeV (the bound on M&#8321; = 2&pi;/L) |
| R1 open item 4, REFERENCES [21] | A_CB &lt; 0.52 | A_CB &lt; 0.15 (A_CB = 0.05 &plusmn; 0.06) |
| HYPOTHESIS section C | DM fraction &le; 4&times;10&#8315;&#8311; / 10&#8315;&#8311; / 10&#8315;&#8312; | about 42 times larger (&le; 2&times;10&#8315;&#8309; at m = 3&times;10&#8315;&sup3;&sup1; eV); still negligible |
| HYPOTHESIS / STATUS seed window | 10&#8315;&#8308; to 0.3 | s&#8320; &lesssim; 1.2&times;10&#8315;&sup2; (for &beta; within 3% of &alpha;/2) |
| HYPOTHESIS step 3 | "one Dirac field on the covering circle" | the (M, &minus;M) pair with no zero mode; requires the Z&#8326; global structure for k &isin; &Zopf; |
| HYPOTHESIS audit E | brane mixing allowed | allowed only at y = 0 |
| HYPOTHESIS section C, last line | walls make late-time birefringence patchy | the patchy reionization rotation can reach &alpha; = 0.418&deg; in opposite-sign domains |
| PREDICTIONS | no tomographic prediction | &Delta;&beta; &isin; [&minus;0.209&deg;, &minus;0.146&deg;]; Δβ = 0 with \|&beta;\| &asymp; 0.2&deg; falsifies |

`stur_final.py` is unchanged, as uploaded. Its outdated statements are listed
in [`STATUS.md`](STATUS.md).

## Open items for round 3

1. **Planck reionization-tomography bound** [N4.4]: get the number and apply
   it to the reionization patchiness of R2.4, which peaks at &ell; &lesssim; 10.
2. **The Z&#8326; caveat.** Decide whether STUR's gauge group is
   [SU(3)&times;SU(2)&times;U(1)]/Z&#8326;, which fixes k &isin; &Zopf;, and work out the
   fractional ladder otherwise.
3. **The nucleation phase.** Specify H_nuc and the number of e-folds. This fixes
   s&#8320; and decides the conditional m &gtrsim; 10&#8315;&sup2;&#8313; eV exclusion.
4. **Full-text verification** of the † references once arxiv.org is reachable.
5. **The companion scripts** (`class_check.py` and others) are still missing.
