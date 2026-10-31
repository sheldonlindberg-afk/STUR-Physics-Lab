# STUR-ROLL: the hypothesis

Sheldon Lindberg, 2026-10-30. Source of truth: [`src/stur_final.py`](../src/stur_final.py).
Every number below appears in that script's output
([`results/stur_final_output.txt`](../results/stur_final_output.txt)).

## Claim

STUR-ROLL adds to Lambda-CDM a sector that predicts the CMB birefringence
angle from integers:

    |beta| = k alpha / 2,   k = 1 (minimal level)   ->   0.2091 deg

No continuous parameter is fitted. Gravity is TEGR, which is GR, so STUR-ROLL
agrees with the GR precision tests by construction. Its energy is
&lesssim; 1e-7 of the dark matter in the allowed window, so every other cosmological
observable is that of Lambda-CDM.

## Scoring rule (fixed before the numbers)

1. Pass/fail gates against published measurements at 2&sigma;.
2. On &beta;: AIC = &chi;&sup2; + 2 &times; (fitted parameters). Lower is better; a
   difference below 2 is not significant. This counts as a *global* comparison
   only because the sector leaves all other data unchanged (section C).

## The derived chain

1. **Zero-energy start.** Wheeler&ndash;DeWitt H&Psi; = 0: the universe nucleates
   whole. &theta;, the R-field holonomy &Phi;_R = &oint; J_a dx^a with J_a = B (a
   Z&#8322;-odd U(1) on the S&sup1;/Z&#8322; orbifold), starts at rest in a minimum.
2. **Chern&ndash;Simons coupling.** The 5D Chern&ndash;Simons term gives
   L = (k&alpha;/4&pi;) &theta; F F&#771;, with k an integer.
3. **Content and level.** A charge-1 bulk fermion (the Z&#8322; pair q_B = &plusmn;1
   is one Dirac field on the covering circle) and a neutral scalar charged
   under B. *(Round 2, R2.2: on S&sup1;/Z&#8322; this is a pair with masses (M, &minus;M) and no zero mode.
   Integer k needs the [SU(3)&times;SU(2)&times;U(1)]/Z&#8326; global structure with a colourless &psi;.)*
   The fermion's KK tower gives c_g = &frac12; sgn M (computed: 0.50000 at
   Mr = 2, 0.49998 at Mr = 10). The 5D parity anomaly makes the bare level
   half-integer, so k_eff is an integer. k = 1 is the minimal nonzero level.
4. **Trigger by cooling.** Wilson-line potential, exact one loop (5D Dirac:
   4 dof; scalar: 2). The scalar dominates above H_c = 15.1/L (nucleation) and
   above T_c = 9.8/L, so &theta; = 0 at nucleation. Below both, the fermions
   dominate: V = m&sup2;f&sup2;(1 + cos &theta;). &theta; = 0 becomes a hilltop and &theta;
   rolls to &pi;. (Check: the S&#8308; &times; S&sup1; result reproduces flat space at
   HL = 0.3 to 9.7e-4.)
5. **The angle.** &beta; = (k&alpha;/2&pi;) &times; &pi; = &alpha;/2, computed from the roll:

   | m [eV] | seed | lands / &pi; | &beta;_rec |
   |---|---|---|---|
   | 3e-31 | 1e-2 | 0.9927 | 0.2069&deg; |
   | 3e-31 | 1e-4 | 0.9843 | 0.2058&deg; |
   | 1e-30 | 1e-2 | 0.9962 | 0.2076&deg; |
   | 1e-30 | 1e-4 | 0.9951 | 0.2080&deg; |
   | 3e-30 | 1e-2 | 1.0016 | 0.2087&deg; |
   | 3e-30 | 1e-4 | 1.0023 | 0.2095&deg; |

   The seed is H_nuc / (2&pi;f). The original window was 1e-4 to 0.3. **Round 2 (R2.4):** &theta;
   random-walks during the de Sitter phase, so &beta; = (&alpha;/2)(1 &minus; |&theta;_i|/&pi;). With &ge; 60 e-folds,
   keeping &beta; within 3% of &alpha;/2 requires a seed &lesssim; 1.2e-2.

## Status

| | |
|---|---|
| **Derived** | steps 1&ndash;5; k integer; step = &pi;; sign of &beta; random per region |
| **Discrete choice** | k = 1 (minimal). k = 2: 0.4181&deg; (+2.5&sigma;); k = 3: 0.6272&deg; (+6.1&sigma;) |
| **Conditions** | the roll must start early enough (section B); f must lie in the window of section C |
| **Inputs that do not change &beta;** (for m &ge; 3e-31 eV) | fermion and scalar bulk masses, orbifold size L, warp, B coupling (sets f), H_nuc (window H_c &lt; H_nuc &lt; 2f) |
| **Assumed axiom** | the field B with J_a = B |
| **Excluded by the full code** | &theta; tunnelling through its own barrier (needs f ~ 1e-32 eV); models that need initial &theta; energy (STUR-B, M3a, U0, C0); the 2025 tanh(r/1 mm) gravity law |

## Audit

**A. Coupling normalisation.** See step 3. The k-ladder against data:

| k | &beta; | pulls (joint, ACT, WMAP+PR4) |
|---|---|---|
| 1 | 0.2091&deg; | &minus;1.2, &minus;0.1, &minus;1.4 &sigma; |
| 2 | 0.4181&deg; | +2.5, +2.7, +0.8 &sigma; |
| 3 | 0.6272&deg; | +6.1, +5.6, +3.1 &sigma; |

**B. Seed robustness.** Where &theta; lands, in units of &pi;:

| seed | m = 3e-31 | m = 1e-30 | m = 1e-29 |
|---|---|---|---|
| 1e-2 | 0.993 | 0.996 | 1.000 |
| 1e-10 | 1.008 | 0.992 | 1.000 |
| 1e-20 | 1.001 | 0.962 | 0.998 |
| 1e-40 | 1.249 | 1.083 | 0.996 |
| 1e-80 | 0.483 | 0.866 | 1.011 |

&beta; = k&alpha;/2 to within 4% needs a seed &gtrsim; 1e-20 (m = 1e-30) or &gtrsim; 1e-40
(m = 1e-29). Smaller seeds roll late and land between 0.5&pi; and 1.25&pi;.

**C. Cosmological consistency (k = 1).**

- Photon coupling g = &alpha;/(&pi;f) &lt; 8e-13/GeV (Chandra, NGC 1275) &rArr; f &gt; 2.9e9 GeV.
- Domain walls: regions roll to +&pi; or &minus;&pi;, separated by sine-Gordon walls of
  tension 8mf&sup2;. The CMB bound (1 MeV)&sup3; &rArr; f &lt; &radic;(1e18 eV&sup3; / 8m).
- &theta; energy: the hilltop energy 2m&sup2;f&sup2; is released at H ~ m/3, giving a
  dark-matter fraction ~ 6(f/M_Pl)&sup2;.

> **Round 2 correction.** The fractions below assume the energy is released at H ~ m/3. The hilltop start delays release to H &asymp; m/19.5, so each fraction is about 42&times; larger (&le; 2&times;10&#8315;&#8309; at m = 3e-31 eV). The conclusion is unchanged. See [`REFINEMENT_R2.md`](REFINEMENT_R2.md).

| m [eV] | allowed f [GeV] | DM fraction &le; |
|---|---|---|
| 3e-31 | 2.9e9 &ndash; 6.5e14 | 4e-7 |
| 1e-30 | 2.9e9 &ndash; 3.5e14 | 1e-7 |
| 1e-29 | 2.9e9 &ndash; 1.1e14 | 1e-8 |

CMB spectra, BAO, SNe, lensing and BBN are unchanged at &le; 1e-7. The CMB
rotation stays isotropic because &theta; = 0 at every emission point. The walls
only make late-time (reionization-era) birefringence patchy. *(Round 2: in an
opposite-sign domain the reionization-era rotation is &alpha; = 0.418&deg;, and the
sky rms is 0.02&ndash;0.20&deg;. No current bound is violated; see R2.4.)*

**D. Multipole pattern &beta;(&ell;).** See [`PREDICTIONS.md`](PREDICTIONS.md).

**E. New particles vs experiment.**

- **&psi;** (a charge-1 vectorlike fermion, mass M_f) must decay, because a
  stable charged relic is excluded by heavy-hydrogen searches. Brane mixing
  with a Standard-Model lepton is allowed only at y = 0 (R2.2), and its lifetime must be &lt; 1 s for BBN. It is then a
  vectorlike lepton, which the LHC excludes below about 1 TeV.
- **&theta;** is shift-symmetric and couples only to F F&#771;: there is no fifth
  force and no equivalence-principle violation at tree level.
- **&phi;** (the scalar) and the **B KK modes**: the Standard Model is B-neutral,
  so these are produced only through &psi; loops. Their Yukawa range is far
  below the 52 &micro;m Eot-Wash limit.
- **Round 2 (R2.3):** only U(1)_Y needs to be in the bulk. Its KK bosons at M&#8321; = 2&pi;/L are
  bounded by dilepton searches at M&#8321; &gt; 5.1&ndash;5.5 TeV, so **1/L &gtrsim; 0.8&ndash;1.0 TeV**. This supersedes
  the "10 GeV" lower end below.
- From m = 1e-30 eV: m&sup2;f&sup2; ~ e^(&minus;M_f L)/L&#8308;. The nucleation window requires
  1/L &lt; f/8. Allowed: 1/L from about 10 GeV (M_f &gt; 1 TeV) up to f/8. For
  1/L &gtrsim; 1 TeV, &psi; sits at &gtrsim; 1e5 GeV, beyond colliders, and the sector is
  then testable **only** through birefringence.

## Caveat

The &beta; measurements rely on calibrating the polarization angle against
Galactic foregrounds. The ACT+Planck authors describe the signal as a hint
whose systematics still need to be understood. A systematic origin would
remove the test entirely.
