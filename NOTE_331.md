# Three colours and three generations from perturbativity in 3-3-1 models

*A standalone note. Sheldon Lindberg, STUR Physics Lab, November 2026. It can be read
without the rest of this repository.*

## Abstract

In SU(3)_C × SU(3)_L × U(1)_X ("3-3-1") gauge models, anomaly cancellation already ties
the number of fermion generations to the number of colours. This is known (Pisano and
Pleitez; Frampton). We keep the number of colours N_c general, with every charge and
anomaly coefficient computed as a function of N_c, and add one requirement: no gauge
coupling may become non-perturbative below the Planck scale. Then:

- Witten's global SU(2) anomaly requires N_c to be odd.
- The SU(3)_L anomaly plus asymptotic freedom of colour gives N_g = N_c.
- SU(3)_L running excludes N_c ≥ 7.
- U(1)_X running excludes N_c = 5.

**The only survivor is N_c = N_g = 3**, and anomaly cancellation then fixes the quark
charges to Q_u = ⅔ and Q_d = −⅓.

The result holds:
- with exact charges and the full scalar content;
- at two loops in the gauge couplings;
- for 3-3-1 breaking scales from 2 to 30 TeV;
- in both phenomenologically viable variants (β = ±1/√3).

In the β = +1/√3 variant the margin is narrow.

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

**Step 1: N_c is odd (Witten).** Each generation contains N_c + 1 SU(2) doublets, so the
global anomaly requires N_c + 1 to be even. A second, independent route gives the same
condition: the spin–charge relation (−1)^F = exp(iπN_c(B − L)) is consistent for quarks
and leptons only when N_c is odd.

**Step 2: N_g = N_c (3-3-1 anomaly plus asymptotic freedom).**
- SU(3)_L anomaly freedom requires equal numbers of triplets and anti-triplets:
  N_g(1 + N_c) = 2nN_c.
- For odd N_c, gcd(N_c, N_c + 1) = 1, so N_c divides N_g: N_g = kN_c.
- With three quark flavours per generation, asymptotic freedom of SU(N_c) needs
  11N_c/3 − 2N_g > 0, which means k < 11/6. So **k = 1**.
- For N_c = 3 this reproduces the standard assignment: two quark generations in the
  anti-triplet, one in the triplet.

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
- Both margins are set at one loop. Two-loop terms move the blow-up scale by a factor
  of about 3.

## 3. Robustness

| Check | Result |
|---|---|
| Two-loop machinery, calibrated on the Standard Model | reproduces (41/10, −19/6, −7) and all nine two-loop coefficients exactly |
| 3-3-1 scale 2–30 TeV (β = −1/√3) | N_c = 3: (2.7–3.7)×10²⁹ GeV; N_c = 5: (0.8–4.5)×10¹⁵ GeV |
| 3-3-1 scale 2–30 TeV (β = +1/√3) | N_c = 3: (2.9–9.9)×10¹⁹ GeV; N_c = 5: (3.3–24)×10¹¹ GeV |
| Criterion α = 1 instead of g = 4π | β = −1/√3: 1.8×10²⁹ vs 1.0×10¹⁵; β = +1/√3: 2.9×10¹⁹ vs 4.7×10¹¹ |
| Criterion g = 1 (α = 0.08, very strict) | β = −1/√3: 5.3×10²⁵ vs 2.7×10¹³ (selects 3). β = +1/√3: 2.0×10¹⁷ vs 3.6×10¹⁰, so **N_c = 3 also fails** |

**Verdict.**
- β = −1/√3: N_c = N_g = 3 is selected under every criterion. Its blow-up lies 6–10
  orders of magnitude above M_Pl, while N_c = 5 fails 4–6 orders below.
- β = +1/√3: 3 is selected under the standard criteria, but its pole sits only a factor of
  2–3 above M_Pl.

## 4. Conditions and caveats

1. **The framework.** Everything assumes 3-3-1 with β = ±1/√3. If colliders exclude it,
   the result goes with it.
2. **Perturbativity to the Planck scale** is a standard criterion, not a theorem. A pole
   below M_Pl signals new physics, not an inconsistency. Drop the requirement and the
   selection drops too.
3. **A counterfactual boundary condition.** Every N_c is run from the *same* couplings at
   the 3-3-1 scale, the values measured in our N_c = 3 world. A world with N_c = 5 could
   have different low-energy couplings. The selection is a statement about our measured
   couplings, not about every possible world.
4. **Two-loop Yukawa terms are not included.** In the Standard Model they slow the growth
   of U(1). They can't plausibly flip the β = −1/√3 margins of 4.6 and 6.1 in a_X, but they
   could matter for the narrow β = +1/√3 case. That is the first calculation to add.
5. **Minimality isn't explained.** Step 1 alone leaves {3, 5, 7, …}. Here the
   perturbativity requirement does the selecting, not a principle of minimality.
6. **No numbers follow.** The structure that fixes these integers adds about 11 scalar
   parameters beyond the Standard Model's 2. It also blocks gauge unification: SU(3)_C and
   SU(3)_L never meet, and the gap grows from 18.6 to 27.3 in 1/α. Masses and couplings
   stay inputs.

## 5. What is known and what is new

- **Known:**
  - N_g a multiple of N_c from 3-3-1 anomaly cancellation (Pisano–Pleitez 1992;
    Frampton 1992);
  - N_c odd from Witten's anomaly;
  - the charges' N_c dependence from anomaly cancellation (e.g. Bär–Wiese 2001 on
    π⁰ → γγ);
  - the minimal model's low Landau pole, and the β = 1/√3 model's high-energy U(1) pole.
- **This note's step:** keeping N_c general throughout (charges, anomalies, scalars, two-
  loop running) and using Planck-scale perturbativity to fix N_c itself, and with it N_g
  and the ⅓ charges.
- **Novelty.** One literature search found no prior derivation of N_c by this route.
  That isn't proof there isn't one.

## 6. How it will be tested

- **The β = ±1/√3 models predict:**
  - a Z′ above about 3.6–4.2 TeV (LIT, recalled);
  - doubly or singly charged bilepton gauge bosons;
  - exotic quarks.

  LHC searches and future colliders will find or exclude them.
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
python -m pytest tests/test_god_eq.py -q
```

The full working record is fronts 5–7c and 11–12 of [GOD_EQUATION.md](GOD_EQUATION.md).

## References (recalled, not link-checked)

- F. Pisano, V. Pleitez, Phys. Rev. D 46, 410 (1992).
- P. H. Frampton, Phys. Rev. Lett. 69, 2889 (1992).
- E. Witten, "An SU(2) anomaly", Phys. Lett. B 117, 324 (1982).
- M. E. Machacek, M. T. Vaughn, Nucl. Phys. B 222, 83 (1983) (two-loop gauge β-functions).
- O. Bär, U.-J. Wiese, Nucl. Phys. B 609, 225 (2001).
