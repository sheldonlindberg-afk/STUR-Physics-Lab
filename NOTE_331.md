# Three colours and three generations from perturbativity in 3-3-1 models

*Sheldon Lindberg, November 2026. Preprint, not peer reviewed; comments from 3-3-1
experts are welcome. **PDF: [paper/note331.pdf](paper/note331.pdf)** (LaTeX source
[paper/note331.tex](paper/note331.tex)). This Markdown version carries the same content
with more detail on each check.*

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
- at two loops in the gauge couplings, including the two-loop Yukawa terms, and at three
  loops in the gauge and matter sector (§3d);
- with one-loop threshold matching at the 3-3-1 scale, across the heavy spectrum;
- for 3-3-1 breaking scales from 2 to 30 TeV;
- in both phenomenologically viable variants (β = ±1/√3).

Two-loop Yukawas can't rescue N_c = 5, even at constant strengths beyond perturbativity.

The selection takes the measured electroweak couplings at the TeV scale as input; it
doesn't predict them. How much it depends on them differs between the two variants:
- **β = −1/√3:** wide margins in the couplings, but N_c = 5 survives in a narrow band of
  weak mixing angle about three times below ours.
- **β = +1/√3:** N_c = 5 fails at every weak mixing angle, but N_c = 3 survives only for
  sin²θ_W(4 TeV) below 0.261–0.285, against the measured 0.250. On the threshold grid
  of §3a its worst case reaches M_Pl for any criterion α ≥ 0.64 (three loops, §3d), but
  that worst case sits on the grid's edge. Against physical mass floors (§3e), **N_c = 3
  reaches M_Pl at α = 1 only if the heavy charged leptons are heavier than about 0.56 TeV**
  (±0.11 TeV, with M_V at its LHC bound; 0.96 TeV at M_V = 10 TeV). Lighter heavy leptons,
  which the LHC still allows, push N_c = 3 below M_Pl as well. In this variant the
  selection is conditional on that mass. The LHC has not tested the condition yet; the
  HL-LHC reaches it about at the threshold (§3f). The two-loop figures at g = 4π (1.6×, or 2.2×
  with the LHC Z′ limit, §3a) are read where the perturbative series has broken down and
  are not robust (§3d).

The result is conditional on the 3-3-1 framework, which collider searches for its Z′ and
bilepton gauge bosons decide, and on the perturbativity requirement.

## 1. Setup

The electric charge is Q = T₃ + βT₈ + X. The two variants without low-scale Landau poles
are β = ±1/√3. The minimal β = −√3 model is excluded by atomic parity violation and sits at the LHC Z′
bound (§6).

For colour group SU(N_c) we take N_g generations, with N_c ≥ 2: for N_c = 1 there is
no colour gauge field, and the asymptotic-freedom condition of step 2 is vacuous. Each generation has left-handed lepton
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
condition, now as a consequence rather than an input (`src/m331_closure.py`, C1;
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

**Two-loop Yukawa terms** (`src/m331_yukawa.py`, Y1–Y2).
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

Source: `src/m331_threshold.py`, output `results/m331/331_threshold.txt`.

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
| β = +1/√3, M_V ≥ 3.76 TeV (Z′ ≥ 4.6 TeV, LHC recast, §6) | 2.17 M_Pl | — | only N_c = 3 |

- **The worst case for N_c = 3.** It is the lightest exotics (0.5 M_V), light scalars, a
  light second doublet and M_V = 2 TeV. That spectrum puts the Z′ at 2.45 TeV, already
  below the LHC limits.
- **The sin²θ_W margin.** For β = +1/√3 it moves from +0.016 (tree level) to **+0.010 to
  +0.035**, depending on the spectrum. Light exotics tighten it; heavy ones widen it.
- **The scheme is under control.** At two loops, moving μ from M_V/2 to 2M_V changes the
  pole by 1%.

**Verdict:** the selection survives one-loop threshold matching across the spectrum
scanned. In the narrow variant the worst allowed case sits a factor of 2 above M_Pl at
g = 4π; §3d shows that criterion is outside the convergent region and restates the margin
with controlled criteria (worst case 1.28 M_Pl at α = 1, three loops, on this grid). §3e
shows the grid's edge is not a bound and replaces it with mass floors.

## 3b. The cutoff and the criterion

Source: `src/m331_closure.py`, output `results/m331/331_closure.txt`.

The selection holds for any cutoff Λ with (best N_c = 5 pole) < Λ < (worst N_c = 3
pole), taken over the whole spectrum scanned in §3a:

| Criterion | Yukawas | β = −1/√3 window (GeV) | β = +1/√3 window (GeV) |
|---|---|---|---|
| g = 4π | on | 7.2×10¹⁵ – 2.4×10²⁹ | 3.8×10¹² – 2.0×10¹⁹ |
| g = 4π | off | 5.1×10¹⁵ – 2.1×10²⁹ | 2.6×10¹² – 1.9×10¹⁹ |
| α = 1 | on | 5.6×10¹⁵ – 1.5×10²⁹ | 3.2×10¹² – 1.5×10¹⁹ |
| α = 1 | off | 4.1×10¹⁵ – 1.2×10²⁹ | 2.2×10¹² – 1.4×10¹⁹ |

**Any cutoff from 7.2×10¹⁵ to 1.4×10¹⁹ GeV works in every row.** That range includes
the Planck mass, the reduced Planck mass (2.4×10¹⁸) and the usual grand-unification
scale (2×10¹⁶). Only the strict g = 1 criterion fails (§3). Of these rows, only α = 1
lies where the loop expansion still converges (§3d).

## 3d. Three-loop gauge running and the criterion

Source: `src/m331_three_loop.py`, output `results/m331/three_loop.txt`.

The three-loop gauge β-functions are taken from the general MS-bar result of Poole and
Thomsen (JHEP 09 (2019) 055, arXiv:1906.04625, eq. A.9). The gauge and matter terms are
included; three-loop Yukawa and quartic terms are not. The case without Yukawas, used as
the conservative bound in §3b, is complete at this order.

**Validation (exact rational arithmetic):**
- the same code's two-loop terms reproduce this note's two-loop coefficients exactly (SM
  and both variants, N_c = 3 and 5);
- its three-loop terms reproduce the Standard Model three-loop gauge β-functions of
  Mihaila, Salomon and Steinhauser (PRL 108 (2012) 151602), all gauge terms, n_G = 1–4.

**Convergence.** For U(1)_X in the β = +1/√3, N_c = 3 model (one-loop coefficient 14,
three-loop self coefficient −690), the three-loop term is:
- 3% of the two-loop term at g_X = 1, and 28% at g_X = 2;
- 71% at g_X = 3, and equal to it at g_X ≈ √(4π), i.e. α_X = 1;
- 25 times the **one-loop** term at g_X = 4π.

So the g = 4π criterion lies outside the region where the series converges. The two-loop
truncation blows up there; the three-loop truncation instead develops a spurious fixed
point, and never reaches 4π, even for N_c = 5. Numbers read off at g = 4π are not stable
under higher orders.

**Controlled criteria.** The scale where the largest coupling reaches g_crit, at two and
three loops (M_V = 4 TeV, Yukawas and thresholds on):

| | g_crit = 1.5 | 2 | 3 | √(4π) |
|---|---|---|---|---|
| β = +1/√3, N_c = 3 (M_Pl) | 0.388 → 0.391 | 1.12 → 1.14 | 2.33 → 2.43 | 2.73 → 2.89 |
| β = +1/√3, N_c = 5 (M_Pl) | 1.5×10⁻⁸, unchanged | 2.6×10⁻⁸ | 3.7 → 3.9×10⁻⁸ | 4.1 → 4.3×10⁻⁸ |
| β = −1/√3, N_c = 3 (M_Pl) | 7.7×10⁸ | 4.3×10⁹ | 1.4 → 1.5×10¹⁰ | 1.8 → 1.9×10¹⁰ |
| β = −1/√3, N_c = 5 (M_Pl) | 2.2×10⁻⁵ | 4.7×10⁻⁵ | 8.0 → 8.2×10⁻⁵ | 9.0 → 9.3×10⁻⁵ |

Three loops move these scales up by 0.5–6%.

**The narrow variant, worst case over the §3a scan** (β = +1/√3, N_c = 3; the worst point
is the same everywhere: lightest exotics, light scalars, a light second doublet, M_V = 2 TeV):

| g_crit (α) | two loops | three loops |
|---|---|---|
| 2.0 (0.32) | 0.50 M_Pl | 0.50 M_Pl |
| 2.5 (0.50) | 0.80 M_Pl | 0.82 M_Pl |
| 3.0 (0.72) | 1.03 M_Pl | 1.07 M_Pl |
| √(4π) (1.00) | 1.21 M_Pl | **1.28 M_Pl** |

The worst case stays perturbative to M_Pl for **g_crit ≥ 2.85 (α ≥ 0.64) at three loops**,
and 2.93 (α ≥ 0.68) at two. At α = 1, the largest sin²θ_W(M_V) for which N_c = 3 reaches
M_Pl at the reference spectrum moves from 0.2639 to 0.2647 (measured 0.250).

**Verdict.**
- Three loops slightly widen the margins; N_c = 5 stays excluded by 4–8 orders of
  magnitude, and β = −1/√3 keeps its wide margins.
- For β = +1/√3, the statement that is stable under higher orders is: **N_c = 3 stays
  perturbative to M_Pl, over the whole spectrum scanned, for any criterion α ≥ 0.64**.
  The two-loop g = 4π figures (1.64 M_Pl, 2.17 M_Pl) should not be relied on.
- At α ≈ 0.64 the three-loop term is already about 0.6–0.7 of the two-loop term, so the
  narrow variant's conclusion sits at the edge of perturbative control. That is a real
  limitation of this variant, not of the calculation.
- This statement holds on the §3a grid (r_J ≥ 0.5, heavy leptons tied to the exotic
  quarks). §3e shows it does not survive light heavy leptons.

## 3e. The narrow margin against mass floors

Source: `src/m331_margin.py`, output `results/m331/margin.txt`.

**The grid edge is not a bound.** The worst case of §3a–3d sits on the corner of the
threshold grid (r_J = 0.5, r_S = ⅓, M_V = 2 TeV). One step past it the pole keeps falling:
at M_V = 2 TeV it is 1.28 M_Pl at r_J = 0.5, 1.12 at 0.4 and **0.94 M_Pl at 0.3**
(α = 1, three loops). So the margin is set by how light the exotics may be, and has to be
stated against experimental floors, not against a grid.

**Split spectrum.** §3a ties the heavy charged leptons E to the exotic quarks J (one r_J).
Their direct limits differ by a factor of about four, so here m_J, m_E, the heavy scalars
m_S and M_V run independently, each Yukawa set by its own mass. The sensitivities at the
floors, d ln(pole)/d ln(mass), are +0.30 (m_J), +0.28 (m_E), +0.02 (m_S) and −0.16 (M_V
at fixed fermion masses: the light fermions then run longer below M_V). The scalars
barely matter; the exotic fermions do.

**Floors** (approximate): M_V ≥ 3.755 TeV (Z′ ≥ 4.6 TeV, §6); m_J ≥ 1.3 TeV, the low end
of the ATLAS 139 fb⁻¹ vector-like-quark pair limits (1.3–1.6 TeV, depending on decays);
m_E ≥ 0.1 TeV and m_S ≥ 0.1 TeV (LEP). E is an SU(2) singlet; LHC limits on singlet
vector-like leptons are about 0.3–0.4 TeV for e and μ partners and weaker for τ, and
depend on how E mixes, so they are not used.

**Result** (β = +1/√3, N_c = 3, α = 1):

| | pole |
|---|---|
| all masses at the floors, M_V = 3.755 TeV, three loops | **0.61 M_Pl** |
| worst over M_V = 3.755–30 TeV, three loops | 0.45 M_Pl (at 30 TeV) |
| same, three loops without Yukawas | 0.43 M_Pl |
| same, two loops | 0.42 M_Pl |

With light heavy leptons, N_c = 3 does not reach M_Pl in this variant. It would need
g_crit = 6.1 (α ≈ 3) at m_E = 0.1 TeV, or 4.5 (α ≈ 1.6) at 0.3 TeV: both outside the
convergent region (§3d). N_c = 5 stays excluded at the same floors (10⁻⁸ M_Pl).

**The condition that replaces the margin.** N_c = 3 reaches M_Pl at α = 1 iff

| M_V | m_E (m_J = 1.3 TeV) | m_J = m_E tied |
|---|---|---|
| 3.755 TeV | ≥ 0.56 TeV | ≥ 0.86 TeV |
| 10 TeV | ≥ 0.96 TeV | ≥ 1.12 TeV |
| 30 TeV | ≥ 1.74 TeV | ≥ 1.50 TeV |

**Error budget on the threshold m_E\* = 561 GeV** (M_V = 3.755 TeV, m_J = 1.3 TeV):
sin²θ_W(M_Z) 1.1%, 1/α(M_Z) 1.1%, α_s 0.3%, m_t 0.1%, matching scale M_V/2–2M_V 3.6%,
next order (the two- to three-loop shift) 19.8%. In quadrature, **m_E\* = 561 ± 113 GeV**.
Without Yukawas (complete at three loops) it is 668 GeV. The truncation dominates, as
expected at α = 1; the measured inputs are irrelevant at this level.

**Check.** At one loop, three Dirac leptons with Y = 1 running from 0.1 TeV to 3.755 TeV
lower 1/α_X(M_V) by 1.6 more than at m_E = 1.3 TeV. With b_X = 14 this moves the pole
down by a factor of e^{−0.72} ≈ 0.49, from 1.27 to about 0.62 M_Pl. The code gives 0.61.

**Verdict.** In the β = +1/√3 variant the selection of N_c = 3 is not a margin; it is a
condition on the spectrum. If this variant is perturbative to M_Pl with three colours,
its heavy charged leptons must lie above about 0.6 TeV (more if M_V is heavier), which is
inside the region the LHC has not yet excluded (§3f). In the β = −1/√3 variant there are
no heavy leptons and the margins stay wide.

## 3f. The heavy leptons against the LHC

Source: `src/m331_heavy_lepton.py`, output `results/m331/heavy_lepton.txt`. Data:
`tools/fetch_hepdata_vll.py`; luminosities `tools/vll_luminosities.py`; Pythia check
`tools/vll_pythia_crosscheck.py`.

**What E is at the LHC.** E is the third member of the lepton triplet (ν, e, E⁻), and E^c
is an SU(3)_L singlet. Both chiralities are SU(2)_L singlets with Y = Q = −1, so below M_V
E is a vector-like singlet lepton, the benchmark the LHC searches use. E^c and e^c carry
the same charges, so E mixes with the ordinary leptons through the allowed Yukawas and
decays promptly to Wν, Zℓ and hℓ. Which search applies depends on the flavour it mixes
with. There are three E, one per generation.

**Cross section.** q q̄ → γ*/Z/Z′ → E⁺E⁻ at LO with full interference, helicity amplitudes
for a massive final state, NNPDF3.1 luxQED.
- The partonic result reproduces QED, (4πα²/3ŝ) β(3 − β²)/2, to 10⁻¹².
- Against Pythia 8 (ffbar2gmZZprime, full γ*/Z/Z′, the same 3-3-1 couplings set by hand,
  the τ′ in its doublet mode) it agrees to 0.2–1.3% at five points, on and off the Z′
  peak. Pythia must be run with `Zprime:universality = off`: by default it copies the
  electron's Z′ couplings onto the τ′.
- The 3-3-1 Z′ (4.6 TeV) interferes constructively: +1% at 300 GeV, +2% at 400 GeV, +6%
  at 600 GeV, +16% at 800 GeV.
- ATLAS's singlet curve is 22% below our LO at 150 GeV and 19% above at 800 GeV; we don't
  reproduce its normalisation and use only the model ratio, as in the Z′ recast (§6).

**Run-2 limits on the 3-3-1 E** (each search assumes the singlet benchmark's branching
ratios):

| E mixes with | search | excluded (observed) | expected |
|---|---|---|---|
| e | ATLAS, 140 fb⁻¹ (arXiv:2411.07143) | 150–321 GeV | 150–302 GeV |
| μ | same | 150–404 GeV | 150–335 GeV |
| τ | CMS, 138 fb⁻¹ (arXiv:2202.08676) | 122–164 GeV (K = 1); 117–192 GeV (K = 1.2) | none; 126–162 GeV |

Check: for e and μ this reproduces ATLAS's own 320 and 400 GeV (the Z′ adds 1% there).
For τ, CMS quotes 125–150 GeV. Below 150 GeV (e, μ) or outside the window (τ), LEP's
~0.1 TeV applies, so a τ-mixed E is allowed down to about 100 GeV.

**The condition is on the geometric mean.** The threshold correction depends on
Σᵢ ln(m_Eᵢ/μ), so three non-degenerate E act like three degenerate ones at
(m_E1 m_E2 m_E3)^{1/3}: (320, 400, 100) GeV gives a pole of 0.7795 M_Pl, and 234 GeV for
all three gives 0.7794 M_Pl. With each E mixing with one flavour, the lightest set Run 2
allows is (321, 404, 100) GeV, a geometric mean of **235 GeV**. If all three mix with τ,
it is 100 GeV. The selection needs 561 ± 113 GeV (§3e). **The LHC has not tested the
condition.**

**HL-LHC** (3 ab⁻¹, 13 TeV cross sections; 14 TeV would help). Expected limits are scaled
by √(L₀/L) (background-limited) and by L₀/L (background-free), the two ends:

| | e | μ | τ | geometric mean |
|---|---|---|---|---|
| √L scaling | 735 GeV | 748 GeV | 455 GeV | 630 GeV |
| L scaling | > 800 GeV | > 800 GeV | 734 GeV | > 777 GeV |

(">" means beyond the last published mass point.) The τ-mixed E is the weakest link.

**The target moves too.** With no Z′ at the HL-LHC, the same recast and √L scaling put
the Z′ floor at 5.50 TeV (Run 2 expected: 4.80 TeV), so M_V ≥ 4.49 TeV and
m_E\* = **621 GeV** (733 GeV without Yukawas; ±20% truncation).

**Verdict.** The HL-LHC reaches the threshold but doesn't clear it. Its conservative
geometric-mean reach (630 GeV) sits at the central m_E\*, and covers the uncertainty
band only with the optimistic scaling, and only if each E mixes with a different flavour.
If the E mix mainly with τ, the HL-LHC cannot decide. Two things the recast does not
cover:
- extra decays E → ℓ + light neutral scalar when the scalars are below m_E, which would
  dilute the multilepton signal;
- non-diagonal flavour mixing.

Either changes the reach, not the RG condition. A future lepton or 100 TeV collider would
settle it.

## 3g. Above the Planck scale: asymptotically safe gravity

Source: `src/m331_gravity_fixed_point.py`, output `results/m331/331_gravity_fixed_point.txt`.

The selection stops at M_Pl. What happens above it? This section takes the
asymptotic-safety estimate as a **MODEL**: above the Planck scale, gravity adds the same
term −f_g g to every gauge β-function (Eichhorn and Versteegen, JHEP 01 (2018) 030;
Eichhorn, Held and Wetterich, PLB 782 (2018) 198). Here f_g = f*/(1 + G* M_Pl²/μ²): it
switches on as the dimensionless Newton coupling reaches its fixed point G*. Both f* and G*
depend on the regulator, and neither is computed here. The running below the transition
is the selection's own: three loops, Yukawas, thresholds, the α = 1 criterion.

- **Only g_X can be predicted (G1).** With b > 0, β = bg³/16π² − fg has a fixed point
  g*² = 16π²f/b. Its slope is +2f, so it is irrelevant: the coupling there is predicted.
  For N_c = 3, b_X = 14 or 26/3, while SU(3)_L (−13/2) and colour (−5) are asymptotically
  free. UV completion then asks g_X ≤ g_X* at the transition.
- **The f* that puts the measured couplings on the fixed-point trajectory (G2):**

  | G* | β = +1/√3 | β = −1/√3 | SM hypercharge, same profile |
  |---|---|---|---|
  | 0.5 | 0.246 | 0.0200 | 0.0097 |
  | 1 | 0.293 | 0.0203 | 0.0098 |
  | 2 | 0.359 | 0.0206 | 0.0099 |

  β = −1/√3 needs about **2×** the gravity contribution the Standard Model's hypercharge
  needs; β = +1/√3 needs about **30×**, because its g_X is already near its pole at M_Pl.
- **The selection is unchanged (G3).** The N_c = 5 and 7 poles sit at 3×10⁸–10¹⁵ GeV, where
  f_g is suppressed by (μ/M_Pl)² to below 10⁻⁷. Even the largest f* the criterion allows
  (b_X/4π) moves them by less than 10⁻⁶.
- **The heavy-lepton condition stands (G4).** With light heavy leptons, N_c = 3 fails at
  0.61 M_Pl, before the transition. Gravity rescues it only with g_X* at 80–98% of √(4π),
  the edge of the criterion (f* ≥ 0.72 at G* = 0.5, ≥ 1.07 at G* = 1), and not at all at
  G* = 2.

**What this gives (FOLLOWS).** One irrelevant coupling and one unknown f* give no
prediction from the gauge sector alone. It becomes a test once an FRG computation for 3-3-1
matter fixes f* and G*. A value near the Standard Model's benchmark would favour
β = −1/√3 and disfavour β = +1/√3. Not included: the gravity terms in the Yukawa and
quartic β-functions, which drive the Standard Model's Higgs-mass prediction from
asymptotic safety.

## 3c. The scalar sector itself, to the Planck scale

Source: `src/m331_scalar.py` and `src/rge_engine.py`, output
`results/m331/331_scalar.txt`.

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
   on them (`src/m331_yukawa.py`, Y3)?

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
   worst case is then 1.53 M_Pl (§3b). That figure is on the §3a grid; against mass floors the β = +1/√3
   case is conditional on the heavy-lepton mass (§3e). The Yukawas' own running is computed in §3c.
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
    hep-ph/0407141; Barela 2024, arXiv:2305.05066; Morisi, Perdonà, Ricciardi 2025,
    arXiv:2505.15785), and the β = 1/√3 model's high-energy U(1) pole, all at N_c = 3;
  - in a different setting, ultraviolet behaviour selecting the number of colours:
    requiring complete asymptotic freedom of chiral gauge theories with scalars selects
    specific numbers of colours and families (Cacciapaglia, Sannino, Wagner, Phys. Rev. D
    114, 075020 (2026), arXiv:2605.08294). The criterion here is different: Planck-scale
    perturbativity in 3-3-1, with the measured couplings as input.
- **This note's step:** keep N_c general throughout (charges, anomalies, scalars, two-loop
  running, thresholds, the scalar sector), and **don't** take the number of generations
  or neutrinos from experiment. Planck-scale perturbativity then fixes N_c itself, and
  with it N_g and the ⅓ charges. Frampton's 1994 statement reaches N_c = 3 only by
  inputting N_l = 3; Pisano takes the Standard Model, with three colours, as the input.
- **Novelty.** Web, arXiv and INSPIRE searches found no prior use of asymptotic freedom
  plus running to fix N_c, in 3-3-1 or in the Standard Model. The INSPIRE searches
  covered every paper citing the founding 3-3-1 papers, Frampton 1994 and Doff–Pisano
  2000 (NOVELTY.md), and were refreshed on 12 November 2026 (NOVELTY.md, section 4). That
  isn't proof of novelty.

## 6. How it will be tested

- **The β = ±1/√3 models predict:**
  - a Z′. Our recast of the ATLAS 13 TeV, 139 fb⁻¹ dilepton search (PLB 796 (2019) 68,
    arXiv:1903.06248; `src/m331_zprime_recast.py`) gives, at 95% CL:

    | | SM decays only | every exotic fermion open | every scalar open too |
    |---|---|---|---|
    | β = +1/√3 | M_Z′ > 5.0–5.2 TeV | M_Z′ > 4.6–4.9 TeV | M_Z′ > 4.6–4.8 TeV |
    | β = −1/√3 | M_Z′ > 4.7–5.0 TeV | M_Z′ > 4.0–4.4 TeV | M_Z′ > 4.0–4.2 TeV |

    The ranges cover which quark generation sits in the triplet, the sin²θ_W scheme and
    the PDF set. Method: ATLAS's own fiducial Z′_SSM prediction is rescaled by the ratio of
    Σ_q L_qq̄ (g_L² + g_R²) × BR(ℓℓ) between the models, so K-factors and acceptance cancel.
    Validation: the same procedure reproduces ATLAS's Z′_ψ and Z′_χ limits (4.53 and
    4.81 TeV against 4.5 and 4.8 TeV). Limits are the official HEPData tables
    (doi:10.17182/hepdata.88425.v1, `tools/fetch_hepdata_dilepton.py`); parton luminosities
    come from PDF4LHC21 and NNPDF3.1 NNLO (`tools/parton_luminosities.py`). An independent
    reproduction with Pythia 8's own Z′ process (`tools/pythia_crosscheck.py`) agrees to
    30–40 GeV. Earlier recasts used
    less data: 4 TeV for β = −1/√3 with 36.1 fb⁻¹ (Lindner, Platscher & Queiroz, Phys.
    Rept. 731, 1 (2018)), 2.64 TeV with exotic decays (de Jesus et al., PLB 809, 135689
    (2020)), and about 2.9 TeV for β = +1/√3 with 8 TeV data (Salazar et al., JHEP 07 (2015)
    096). Bilepton pairs are closed (M_Z′ = 1.225 M_V < 2 M_V). The 'every scalar open'
    column bounds Z′ → scalars, W_L W_L and Zh. Interference with Drell-Yan changes σB by
    −3% to +2% within ±10% of the peak (about 15 GeV), and Z-Z′ mixing by < 0.4%;
  - doubly or singly charged bilepton gauge bosons;
  - exotic quarks;
  - for β = +1/√3, three heavy charged leptons, vector-like SU(2) singlets. The selection
    needs their geometric-mean mass above 0.56 ± 0.11 TeV (0.62 TeV if the HL-LHC sees no
    Z′). Run 2 allows down to 0.24 TeV, and the HL-LHC reaches about 0.63–0.78 TeV (§3f).

  LHC searches and future colliders will find or exclude them.
- **Consistency to M_Pl adds relations (§3c):**
  - exotic quarks lighter than 1.79 M_V (β = −1/√3) or 1.40 M_V (β = +1/√3);
  - M_Z′ = 1.225 M_V;
  - the top's doublet carrying at least about 70% of the electroweak vev squared.

  A discovery that breaks these relations would break the selection, without excluding
  3-3-1 itself.
- **The minimal model is excluded.** At one loop sin²θ_W reaches ¼ at 3.68 TeV, where
  g_X has its Landau pole, so its Z′ must lie below about 3.7 TeV.
  - The LHC bound is M_Z′ > 3.7 TeV (13 TeV, 36.1 fb⁻¹, exotic decays included;
    Nepomuceno & Meirose, PRD 101, 035017 (2020), arXiv:1911.12783), right at that ceiling.
  - Atomic parity violation in caesium requires M_Z′ ≳ 4.2–5.4 TeV (Long et al., NPB 943,
    114629 (2019), arXiv:1812.08669).
  - Higher-order effects would have to raise the pole by more than about 14% to evade the
    parity-violation bound.
- **An independent check of N_c = 3:** the R-ratio below charm. With N_c-dependent charges
  R(u,d,s) = N_c(Q_u² + 2Q_d²)(1 + 3C_Fα_s/4π) is 2.173 at N_c = 3 (`src/m331_why_three.py`,
  W6). KEDR's weighted average over 1.84–3.05 GeV is R = 2.225 ± 0.020 ± 0.047 (Anashin
  et al., PLB 770, 174 (2017), arXiv:1610.02827), so N_c = 3 agrees to −1.0σ, against
  −15σ at N_c = 2 and +33σ at N_c = 5.

## 7. Reproduce

```bash
pip install -r requirements.txt pytest
python3 src/m331_why_three.py          # step 1, charges; results/m331/why_three.txt
python3 src/m331_three_generations.py  # step 2, minimal model; three_generations.txt
python3 src/m331_su3L_running.py       # step 3; su3L_running.txt
python3 src/m331_exact.py              # step 4, robustness, both variants; 331_exact.txt
python3 src/m331_yukawa.py             # Yukawas, boundary condition, margins; 331_yukawa.txt
python3 src/m331_threshold.py          # one-loop threshold matching (~75 s); 331_threshold.txt
python3 src/m331_closure.py            # Witten redundant, no-Yukawa bound, cutoff window (~3 min)
python3 src/m331_scalar.py             # the scalar sector to M_Pl (~4 min); 331_scalar.txt
python3 src/m331_zprime_recast.py      # the ATLAS 139 fb^-1 Z' recast (~1 s); zprime_recast.txt
python3 src/m331_margin.py             # the beta = +1/sqrt3 margin vs mass floors (~50 s); margin.txt
python3 src/m331_heavy_lepton.py       # heavy leptons vs LHC, HL-LHC (~5 s); heavy_lepton.txt
python3 src/m331_gravity_fixed_point.py  # gravity above M_Pl, asymptotic safety (~70 s); 331_gravity_fixed_point.txt
python -m pytest tests/test_331_*.py -q
```

## References

Full bibliography, with DOIs and arXiv numbers checked against INSPIRE, in
[paper/note331.pdf](paper/note331.pdf). The β = ±1/√3 Z′ limits (§6) are this note's
recast (paper Appendix A); the minimal-model limits are quoted from the cited papers.
