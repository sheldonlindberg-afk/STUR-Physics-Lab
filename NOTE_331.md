# Three colours and three generations from perturbativity in 3-3-1 models

*A standalone note. Sheldon Lindberg, STUR Physics Lab, November 2026. It can be read
without the rest of this repository.*

## Abstract

In SU(3)_C × SU(3)_L × U(1)_X ("3-3-1") gauge models, anomaly cancellation already ties
the number of fermion generations to the number of colours. This is known (Pisano and
Pleitez; Frampton). We keep the number of colours N_c general, with every charge and
anomaly coefficient computed as a function of N_c, and add one requirement: no gauge
coupling may become non-perturbative below the Planck scale. Then:

- The SU(3)_L anomaly plus asymptotic freedom of colour forces N_c to be odd and
  N_g = N_c. Witten's global anomaly is then automatically satisfied; it is implied, not
  needed.
- SU(3)_L running excludes N_c ≥ 7.
- U(1)_X running excludes N_c = 5.

**The only survivor is N_c = N_g = 3**, and anomaly cancellation then fixes the quark
charges to Q_u = ⅔ and Q_d = −⅓.

The result holds:
- with exact charges and the full scalar content;
- at two loops in the gauge couplings, including the two-loop Yukawa terms;
- with one-loop threshold matching at the 3-3-1 scale, across the heavy spectrum;
- for 3-3-1 breaking scales from 2 to 30 TeV;
- in both phenomenologically viable variants (β = ±1/√3).

Two-loop Yukawas can't rescue N_c = 5, even at constant strengths beyond perturbativity.

The selection takes the measured electroweak couplings at the TeV scale as input; it
doesn't predict them. How much it depends on them differs between the two variants:
- **β = −1/√3:** wide margins in the couplings, but N_c = 5 survives in a narrow band of
  weak mixing angle about three times below ours.
- **β = +1/√3:** N_c = 5 fails at every weak mixing angle, but N_c = 3 survives only for
  sin²θ_W(4 TeV) below 0.261–0.285, against the measured 0.250. Its worst-case pole, with
  thresholds, sits 1.6× above M_Pl, or 2.2× when the Z′ is above the LHC limits.

The result is conditional on the 3-3-1 framework, which collider searches for its Z′ and
bilepton gauge bosons decide, and on the perturbativity requirement.

## 1. Setup

The electric charge is Q = T₃ + βT₈ + X. The two variants without low-scale Landau poles
are β = ±1/√3. The minimal β = −√3 model is excluded by LHC Z′ limits, as computed in §6.

For colour group SU(N_c) we take N_g generations. Each generation has left-handed lepton
triplets and quark triplets or anti-triplets, with the third member an exotic quark. n of
the N_g quark generations sit in the anti-triplet.

**Charges for general N_c.** Cancelling the perturbative anomalies, with the Yukawa
couplings in place, gives

```
Q_u = (N_c + 1) / (2 N_c),        Q_d = (1 − N_c) / (2 N_c)
```

These reduce to ⅔ and −⅓ at N_c = 3. Every gauge anomaly vanishes identically in N_c,
both in the Standard Model and in the full 3-3-1 content: X³, grav²X, SU(3)_L²X,
SU(N_c)²X and SU(3)_L³. This was checked exactly for N_c = 3, 5 and 7. **Perturbative
anomalies therefore fix the charges given N_c, but not N_c itself.**

U(1)_X charges for β = −1/√3:
- quark triplet: X = Q_u − ⅓;
- quark anti-triplet: X = Q_d + ⅓;
- leptons: −⅓;
- scalars η, ρ, χ: −⅓, +⅔, −⅓, fixed by the Yukawas and independent of N_c.

For β = +1/√3: leptons −⅔, quark triplet Q_u − ⅔, anti-triplet Q_d + ⅔, scalars ⅓, ⅓, −⅔.

## 2. The chain

**Step 1: N_c is odd. It follows from step 2; Witten is not needed.** In the Standard
Model, Witten's global SU(2) anomaly requires the N_c + 1 doublets per generation to be
even. In 3-3-1, though, SU(2)_L sits inside SU(3)_L, and π₄(SU(3)) = 0, so the UV group
imposes no global anomaly of its own. Step 2's equations already force N_c to be odd
(proof below), and the doublet count N_g(1 + N_c) = 2nN_c then comes out even
automatically. The spin–charge route, (−1)^F = exp(iπN_c(B − L)), gives the same
condition, now as a consequence rather than an input (`src/god_eq_331_closure.py`, C1;
all 29 solutions up to N_c = 60 checked).

**Step 2: N_g = N_c (3-3-1 anomaly plus asymptotic freedom).**
- SU(3)_L anomaly freedom requires equal numbers of triplets and anti-triplets:
  N_g(1 + N_c) = 2nN_c.
- For odd N_c, gcd(N_c, N_c + 1) = 1, so N_c divides N_g: N_g = kN_c.
- With three quark flavours per generation, asymptotic freedom of SU(N_c) needs
  11N_c/3 − 2N_g > 0, which means k < 11/6. So **k = 1**.
- For N_c = 3 this reproduces the standard assignment: two quark generations in the
  anti-triplet, one in the triplet.
- **Even N_c is excluded by the same two conditions.** If N_c is even, gcd(N_c + 1, 2N_c)
  = 1, so 2N_c must divide N_g. But 2N_c > 11N_c/6 violates asymptotic freedom. So
  N_c is odd and N_g = N_c, with no further input.

**Step 3: SU(3)_L excludes N_c ≥ 7.** With N_g = N_c there are N_c(1 + N_c) Weyl triplets.
The one-loop coefficient b_L = 11 − N_c(1 + N_c)/3 − (scalars) is computed from
1/α_L(4 TeV) = 31.5:

| N_c | b_L (3 scalar triplets) | Landau pole |
|---|---|---|
| 3 | +6.5 | none (asymptotically free) |
| 5 | +0.5 | none |
| 7 | −8.2 | 1.3×10¹⁴ GeV, below M_Pl |
| 9 | −19.5 | 10⁸ GeV |

Adding the minimal model's scalar sextet leaves the verdict unchanged.

**Step 4: U(1)_X excludes N_c = 5.** Two-loop gauge running from the 3-3-1 scale,
starting at 1/α_X(4 TeV) = 83.76. "Blow-up" means g = 4π.

| N_c = N_g | one-loop a_X | Blow-up, β = −1/√3 | Blow-up, β = +1/√3 |
|---|---|---|---|
| 3 | 26/3 = 8.67 (β = −1/√3); 14.00 (β = +1/√3) | **3.0×10²⁹ GeV** | **4.0×10¹⁹ GeV** |
| 5 | 19.33; 27.33 | 1.3×10¹⁵ GeV | 5.5×10¹¹ GeV |
| 7 | 34.44; 45.11 | 9.7×10⁹ GeV | 3.1×10⁸ GeV |

The Planck scale is 1.2×10¹⁹ GeV.
- For β = −1/√3, a pole exactly at M_Pl needs a_X = 14.76. The margins are +6.09 for
  N_c = 3 and −4.57 for N_c = 5.
- Both margins are set at one loop. Two-loop gauge terms move the blow-up scale by a
  factor of about 3.

**Two-loop Yukawa terms** (`src/god_eq_331_yukawa.py`, Y1–Y2).
- **The formula.** A Yukawa y φψ₁ψ₂ adds −g³y² n_terms [C₂(ψ₁) + C₂(ψ₂)] / d(G) / (16π²)²
  to each gauge β-function. It reproduces the Standard Model top-quark coefficients
  (17/10, 3/2, 2) exactly.
- **What was included:**
  - the top Yukawa, starting from its Standard Model value at 4 TeV, y_t = 0.83;
  - one Yukawa y_J for every exotic quark, and for every heavy lepton when β = +1/√3.
- **Held constant to the blow-up.** Real Yukawas fall with energy, so this overstates
  their effect. That makes the N_c = 5 exclusion conservative.

| y_J | β = −1/√3: N_c = 3 / N_c = 5 | β = +1/√3: N_c = 3 / N_c = 5 |
|---|---|---|
| none (no Yukawas at all) | 3.0×10²⁹ / 1.3×10¹⁵ GeV | 4.0×10¹⁹ / 5.5×10¹¹ GeV |
| 0 (top only) | 3.4×10²⁹ / 1.3×10¹⁵ | 4.2×10¹⁹ / 5.6×10¹¹ |
| 1 | 4.7×10²⁹ / 1.6×10¹⁵ | 6.2×10¹⁹ / 6.8×10¹¹ |
| 2 | 1.2×10³⁰ / 2.8×10¹⁵ | 2.2×10²⁰ / 1.3×10¹² |

- Yukawas raise every pole by at most a factor of about 5.
- No constant y_J up to 6 lifts N_c = 5 to the Planck scale. (√(4π) = 3.5 is already the
  edge of perturbativity.)

## 3. Robustness

| Check | Result |
|---|---|
| Two-loop machinery, calibrated on the Standard Model | reproduces (41/10, −19/6, −7) and all nine two-loop coefficients exactly |
| 3-3-1 scale 2–30 TeV (β = −1/√3) | N_c = 3: (2.7–3.7)×10²⁹ GeV; N_c = 5: (0.8–4.5)×10¹⁵ GeV |
| 3-3-1 scale 2–30 TeV (β = +1/√3) | N_c = 3: (2.9–9.9)×10¹⁹ GeV; N_c = 5: (3.3–24)×10¹¹ GeV |
| Criterion α = 1 instead of g = 4π | β = −1/√3: 1.8×10²⁹ vs 1.0×10¹⁵; β = +1/√3: 2.9×10¹⁹ vs 4.7×10¹¹ |
| Criterion g = 1 (α = 0.08, very strict) | β = −1/√3: 5.3×10²⁵ vs 2.7×10¹³ (selects 3). β = +1/√3: 2.0×10¹⁷ vs 3.6×10¹⁰, so **N_c = 3 also fails**, with or without Yukawas |
| Two-loop Yukawas (top + all exotics at y_J = 1) | β = −1/√3: 4.7×10²⁹ vs 1.6×10¹⁵; β = +1/√3: 6.2×10¹⁹ vs 6.8×10¹¹ |
| β = +1/√3, N_c = 3 pole ÷ M_Pl (g = 4π) | 3.3 with no Yukawas; 5.1 with y_J = 1; 3.7–12.5 for 3-3-1 scales of 2–30 TeV |

**Verdict.**
- β = −1/√3: N_c = N_g = 3 is selected under every criterion. Its blow-up lies 6–10
  orders of magnitude above M_Pl, while N_c = 5 fails 4–6 orders below.
- β = +1/√3: 3 is selected under the standard criteria, but its pole sits only a factor of
  2–3 above M_Pl without Yukawas (3–5 with them). Yukawas can only widen this margin,
  because they only slow the growth of U(1)_X.

## 3a. One-loop threshold matching at the 3-3-1 scale

Source: `src/god_eq_331_threshold.py`, output `results/god_equation/331_threshold.txt`.

**Method.** The breaking SU(3)_L × U(1)_X → SU(2)_L × U(1)_Y is matched at one loop in
MS-bar (Weinberg 1980; Hall 1981):

```
1/α_low(μ) = 1/α_high(μ) − λ/(12π)
λ = Σ_V t²(1 − 21 ln M_V/μ) + 8 Σ_Dirac t² ln M_F/μ + Σ_real scalars t² ln M_S/μ
```

For U(1)_Y, the high-energy side is the combination 1/α_X + β²/α_L.

**The heavy spectrum, counted from the model:**
- one complex SU(2) doublet of bilepton vectors (|Y| = ½), mass M_V;
- the Z′, which carries no Standard Model charge (M_Z′ = 1.225 M_V);
- N_c exotic quarks, plus N_c heavy leptons when β = +1/√3, all of mass r_J M_V. The same
  Yukawa, y_J = r_J g_L/√2, enters at two loops.
- nine heavy real scalars, after 4 form the light doublet and 5 are eaten: a second
  doublet, a charged singlet, and 3 neutral fields, all of mass r_S M_V. Optionally the
  second doublet is light, giving a two-Higgs-doublet model below M_V.

**Check.** At one loop the N_c = 3 pole must not depend on the matching scale μ once the
spectrum is fixed. Moving μ from M_V/3 to 3M_V changes ln(pole) by less than 10⁻⁹.
Without thresholds it changes the pole by a factor of 2.6. So every sign and
multiplicity in λ is right, and the heavy content is exactly 3-3-1 minus the Standard
Model.

N_c = 5 can't pass this check, and shouldn't. Below μ the running uses our three-colour
Standard Model, which isn't 3-3-1 at N_c = 5 minus its heavy fields. That is the
counterfactual boundary condition of §4 showing up directly. N_c = 5's pole moves by a
factor of 1.5 with μ, and the scan below takes its most favourable μ.

**Size.** With every heavy mass at μ, only the MS-bar vector constant survives
(λ_Y = λ_2 = 1), and 1/α_X moves by +0.018 out of 83.8. Spreading the masses
(r_J = 0.5–3, r_S = ⅓–3) moves 1/α_Y by −0.94 to +1.51 for β = +1/√3, and by −0.36 to
+0.58 for β = −1/√3. In effect, the heavy fields start running at their own masses.

**Result** (two-loop running, Yukawas included; the scan covers r_J, r_S, M_V = 2–10 TeV,
and the second doublet heavy or light):

| | N_c = 3, worst case | N_c = 5, best case | Verdict |
|---|---|---|---|
| β = −1/√3 | 2.4×10²⁹ GeV (2×10¹⁰ M_Pl) | 7.2×10¹⁵ GeV | only N_c = 3 |
| β = +1/√3 | 2.0×10¹⁹ GeV (**1.64 M_Pl**) | 3.8×10¹² GeV | only N_c = 3 |
| β = +1/√3, M_V ≥ 4 TeV (Z′ ≥ 4.9 TeV) | 2.23 M_Pl | — | only N_c = 3 |

- **The worst case for N_c = 3.** It is the lightest exotics (0.5 M_V), light scalars, a
  light second doublet and M_V = 2 TeV. That spectrum puts the Z′ at 2.45 TeV, already
  below the LHC limits.
- **The sin²θ_W margin.** For β = +1/√3 it moves from +0.016 (tree level) to **+0.010 to
  +0.035**, depending on the spectrum. Light exotics tighten it; heavy ones widen it.
- **The scheme is under control.** At two loops, moving μ from M_V/2 to 2M_V changes the
  pole by 1%.

**Verdict:** the selection survives one-loop threshold matching across the spectrum
scanned. In the narrow variant the worst allowed case sits a factor of 2 above M_Pl.

## 3b. The cutoff and the criterion

Source: `src/god_eq_331_closure.py`, output `results/god_equation/331_closure.txt`.

The selection holds for any cutoff Λ with (best N_c = 5 pole) < Λ < (worst N_c = 3
pole), taken over the whole front-7e spectrum:

| Criterion | Yukawas | β = −1/√3 window (GeV) | β = +1/√3 window (GeV) |
|---|---|---|---|
| g = 4π | on | 7.2×10¹⁵ – 2.4×10²⁹ | 3.8×10¹² – 2.0×10¹⁹ |
| g = 4π | off | 5.1×10¹⁵ – 2.1×10²⁹ | 2.6×10¹² – 1.9×10¹⁹ |
| α = 1 | on | 5.6×10¹⁵ – 1.5×10²⁹ | 3.2×10¹² – 1.5×10¹⁹ |
| α = 1 | off | 4.1×10¹⁵ – 1.2×10²⁹ | 2.2×10¹² – 1.4×10¹⁹ |

**Any cutoff from 7.2×10¹⁵ to 1.4×10¹⁹ GeV works in every row.** That range includes
the Planck mass, the reduced Planck mass (2.4×10¹⁸) and the usual grand-unification
scale (2×10¹⁶). Only the strict g = 1 criterion fails (§3).

## 3c. The scalar sector itself, to the Planck scale

Source: `src/god_eq_331_scalar.py` and `src/rge_engine.py`, output
`results/god_equation/331_scalar.txt`.

**Why this matters.** The selection asks every coupling to stay perturbative to the
Planck scale, so 3-3-1 at N_c = 3 must pass the same test in its scalar sector. If its
quartics or Yukawas blew up, or its potential became unbounded below, it would exclude
itself.

**Method.**
- The general one-loop quartic and Yukawa RGEs (Machacek–Vaughn; Luo–Wang–Xiao) are
  implemented on the 18 real scalars. The engine reproduces the Standard Model's β_λ and
  β_yt exactly.
- The 9 quartics allowed by the model's discrete symmetry form a basis that is closed
  under the RGEs (residual 10⁻¹⁵), and the potential is gauge invariant (10⁻¹⁶).
- The top Yukawa and every exotic-quark and heavy-lepton Yukawa run separately; with
  separate couplings the Yukawa structures close too.
- The light-Higgs quartic is matched at 4 TeV to the SM value, λ_SM = 0.076, at tree
  level in the decoupling limit.
- Survival means: every |λ| < 4π, every Yukawa < √(4π), and the potential bounded below,
  checked numerically at 8 scales up to M_Pl.

**Results.**
- The SM alone is not stable to M_Pl: at one loop λ_SM crosses zero at 9×10⁷ GeV (it is
  metastable, as is known).
- **3-3-1 at N_c = 3 survives in both variants**, in a corner of parameter space:
  - 17 of 250 viable points (β = −1/√3) and 13 of 250 (β = +1/√3) survive under small
    priors;
  - none survive with O(1) quartics, which hit Landau poles near 30–40 TeV.
- **In the survivors the extra scalars cure the SM instability:** the top-doublet quartic
  stays positive at M_Pl.

**What consistency to M_Pl requires (conditional predictions for colliders):**

| | β = −1/√3 | β = +1/√3 |
|---|---|---|
| Exotic Yukawa at 4 TeV, gauge + Yukawas alone (exact at one loop) | < 0.80 | < 0.62 |
| → exotic-quark mass | **< 1.79 M_V** | **< 1.40 M_V** |
| Exotic Yukawa among full survivors | ≤ 0.57 | ≤ 0.53 |
| Share of the electroweak vev in the top's doublet | c² ≥ 0.68 | c² ≥ 0.69 |
| Quartics at 4 TeV | all ≲ 0.37 | all ≲ 0.35 |

With M_Z′ = 1.225 M_V, the exotic quarks must lie below about 1.1–1.5 M_Z′. If colliders
find them much heavier than the Z′, the selection's own perturbativity criterion fails.

**Limits.**
- The RGEs are one loop.
- The light-Higgs matching is tree level.
- The search is a random sampling, not a proof that the surviving region is the only one.

## 4. Conditions and caveats

1. **The framework.** Everything assumes 3-3-1 with β = ±1/√3. If colliders exclude it,
   the result goes with it.
2. **Perturbativity to the Planck scale** is a standard criterion, not a theorem. A pole
   below M_Pl signals new physics, not an inconsistency. Drop the requirement and the
   selection drops too.
3. **The boundary condition: measured couplings are an input.** Every N_c is run from
   the couplings measured at 4 TeV: sin²θ_W = 0.2504, 1/α_em = 125.7 and α_s. In 3-3-1,
   1/α_X = (1 − 4s²/3)/α_em, so these fix the U(1)_X start. How far does the result lean
   on them (`src/god_eq_331_yukawa.py`, Y3)?

   | | β = −1/√3 | β = +1/√3 |
   |---|---|---|
   | N_c = 3 reaches M_Pl for | sin²θ_W < 0.449 (margin +0.20) | sin²θ_W < 0.266 (+0.016); 0.272 (+0.022) with y_J = 1 |
   | N_c = 5 reaches M_Pl for | only 0.066 < sin²θ_W < 0.074 (0.064–0.081 with Yukawas), 3.1–3.4× below ours | **no weak angle at all** |
   | At our weak angle, N_c = 5 needs α_em weaker by | 1.33× | 1.86× |

   Lowering sin²θ_W relieves U(1)_X but strengthens SU(3)_L, which is why N_c = 5 gets at
   most a narrow band.

   **The precise statement:** given the measured electroweak couplings, only N_c = 3 stays
   perturbative to the Planck scale. The selection doesn't predict those couplings. In the
   β = −1/√3 variant, a world whose TeV-scale weak angle were about three times smaller
   would also allow N_c = 5.

   The β = +1/√3 margin in sin²θ_W is 0.016 with tree-level matching, large next to the
   measurement error (about 10⁻⁴). One-loop threshold matching is computed in §3a and
   leaves it at +0.010 to +0.035.
4. **Yukawas: closed.** Two-loop Yukawa terms are included (§2). The selection also
   holds with **no Yukawas at all**, a lower bound for any Yukawa running: the β = +1/√3
   worst case is then 1.53 M_Pl (§3b). The Yukawas' own running is computed in §3c.
5. **Minimality isn't explained.** Steps 1–2 leave {3, 5, 7, …}. Here the
   perturbativity requirement does the selecting, not a principle of minimality.
6. **No numbers follow.** The structure that fixes these integers adds about 11 scalar
   parameters beyond the Standard Model's 2. It also blocks gauge unification: SU(3)_C and
   SU(3)_L never meet, and the gap grows from 18.6 to 27.3 in 1/α. Masses and couplings
   stay inputs.

## 5. What is known and what is new

- **Known** (retrieved in the novelty search, NOVELTY.md):
  - N_g a multiple of N_c from 3-3-1 anomaly cancellation (Pisano–Pleitez 1992;
    Frampton 1992; Pisano 1996, hep-ph/9609358; Doff–Pisano 2000, hep-ph/0007306);
  - with three light neutrinos as an input, N_c = 3 (Frampton 1994, hep-ph/9409331:
    "taking … arbitrary numbers N_c of colors and N_l of light neutrinos we find this
    anomaly cancels only if N_c = N_l = 3");
  - quark and lepton representations and charge quantization for an arbitrary number of
    colours (Geng 2001, hep-ph/0101329);
  - **the closest predecessor:** Doff & Pisano 2000, hep-ph/0011087. They keep n_c
    general and find N_generations = k·n_c for any k ≥ 1 (their eq. 17). They don't
    impose asymptotic freedom to force k = 1, and they don't use running to choose n_c;
  - generation counting for arbitrary β (Diaz, Martinez, Ochoa 2005, hep-ph/0411263);
  - N_c odd from Witten's anomaly (in the SM; in 3-3-1 it follows from step 2, §2);
  - the charges' N_c dependence from anomaly cancellation (e.g. Bär–Wiese 2001 on
    π⁰ → γγ);
  - the minimal model's low Landau pole (e.g. Dias, Martinez, Pleitez 2005,
    hep-ph/0407141; Barela 2023, arXiv:2305.05066; Morisi, Perdonà, Ricciardi 2025,
    arXiv:2505.15785), and the β = 1/√3 model's high-energy U(1) pole, all at N_c = 3.
- **This note's step:** keep N_c general throughout (charges, anomalies, scalars, two-loop
  running, thresholds, the scalar sector), and **don't** take the number of generations
  or neutrinos from experiment. Planck-scale perturbativity then fixes N_c itself, and
  with it N_g and the ⅓ charges. Frampton's 1994 statement reaches N_c = 3 only by
  inputting N_l = 3; Pisano takes the Standard Model, with three colours, as the input.
- **Novelty.** Web, arXiv and INSPIRE searches found no prior use of asymptotic freedom
  plus running to fix N_c, in 3-3-1 or in the Standard Model. The INSPIRE searches
  covered every paper citing the founding 3-3-1 papers, Frampton 1994 and Doff–Pisano
  2000 (NOVELTY.md). That isn't proof of novelty; an expert in 3-3-1 phenomenology should
  still be asked.

## 6. How it will be tested

- **The β = ±1/√3 models predict:**
  - a Z′ above about 3.6–4.2 TeV (LIT, recalled);
  - doubly or singly charged bilepton gauge bosons;
  - exotic quarks.

  LHC searches and future colliders will find or exclude them.
- **Consistency to M_Pl adds relations (§3c):**
  - exotic quarks lighter than 1.79 M_V (β = −1/√3) or 1.40 M_V (β = +1/√3);
  - M_Z′ = 1.225 M_V;
  - the top's doublet carrying at least about 70% of the electroweak vev squared.

  A discovery that breaks these relations would break the selection, without excluding
  3-3-1 itself.
- **The minimal model is already excluded.** At one loop sin²θ_W reaches ¼ at 3.68 TeV,
  which forces its Z′ below about 3.7 TeV, while LHC dilepton searches exclude it below
  5 TeV.
- **An independent check of N_c = 3:** the R-ratio below charm. With N_c-dependent charges
  it gives −1.0σ at N_c = 3, against −15σ at N_c = 2 and +33σ at N_c = 5 (KEDR, recalled).

## 7. Reproduce

```bash
pip install -r requirements.txt pytest
python3 src/god_eq_why_three.py         # step 1, charges; results/god_equation/why_three.txt
python3 src/god_eq_three_generations.py # step 2, minimal model; three_generations.txt
python3 src/god_eq_su3L_running.py      # step 3; su3L_running.txt
python3 src/god_eq_331_exact.py         # step 4, robustness, both variants; 331_exact.txt
python3 src/god_eq_331_yukawa.py        # Yukawas, boundary condition, margins; 331_yukawa.txt
python3 src/god_eq_331_threshold.py     # one-loop threshold matching (~75 s); 331_threshold.txt
python3 src/god_eq_331_closure.py       # Witten redundant, no-Yukawa bound, cutoff window (~3 min)
python3 src/god_eq_331_scalar.py        # the scalar sector to M_Pl (~4 min); 331_scalar.txt
python -m pytest tests/test_god_eq.py tests/test_331_*.py -q
```

The full working record is fronts 5–7g and 11–12 of [GOD_EQUATION.md](GOD_EQUATION.md).

## References (recalled, not link-checked)

- F. Pisano, V. Pleitez, Phys. Rev. D 46, 410 (1992).
- P. H. Frampton, Phys. Rev. Lett. 69, 2889 (1992).
- E. Witten, "An SU(2) anomaly", Phys. Lett. B 117, 324 (1982).
- M. E. Machacek, M. T. Vaughn, Nucl. Phys. B 236, 221 (1984); B 249, 70 (1985) (Yukawa and
  quartic β-functions); M.-x. Luo, H.-w. Wang, Y. Xiao, Phys. Rev. D 67, 065019 (2003).
- M. E. Machacek, M. T. Vaughn, Nucl. Phys. B 222, 83 (1983) (two-loop gauge β-functions).
- O. Bär, U.-J. Wiese, Nucl. Phys. B 609, 225 (2001).
