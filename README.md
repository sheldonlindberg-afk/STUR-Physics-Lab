<p align="center">
  <img src="assets/logo.svg" alt="" width="120"/>
</p>

<h1 align="center">STUR Physics Lab: one simulation</h1>

<p align="center">
  <strong><a href="production_v2_2.py">production_v2_2.py</a>: one script, Python standard library only, nothing tuned, nothing fitted.</strong><br>
  Every number it prints is calculated from measured inputs, and the measured results it is judged against never enter the calculation.<br>
  Independent work, not peer reviewed.
</p>

<p align="center">
  <a href="https://github.com/sheldonlindberg-afk/STUR-Physics-Lab/actions/workflows/tests.yml"><img src="https://github.com/sheldonlindberg-afk/STUR-Physics-Lab/actions/workflows/tests.yml/badge.svg" alt="Tests"></a>
  <a href="https://creativecommons.org/publicdomain/zero/1.0/"><img src="https://img.shields.io/badge/License-CC0_1.0-lightgrey.svg" alt="License: CC0-1.0"></a>
</p>

---

## Run it

```
python3 production_v2_2.py                     # full report, about 20 minutes (four cores)
python3 production_v2_2.py --json-out out.json # every number, as JSON
python3 production_v2_2.py --scales 2000 5000  # other evaluation scales (GeV, above m_t)
python3 production_v2_2.py --set M_t=173.5      # change a measured input; the whole model is recalculated
python3 production_v2_2.py --certify            # also prove every texture exclusion of Part C (~10 min more)
```

Or copy the file (the [website](https://sheldonlindberg-afk.github.io/STUR-Physics-Lab/) has a
**Copy Python script** button; on GitHub use *Copy raw file*) and paste it into any Python 3.8+
runner, notebook or AI assistant's code tool. The expected output is
[results/production_v2_2.txt](results/production_v2_2.txt). It ends with 80 self-checks, which test
the calculation itself, not its agreement with data.

## The rule

**Nothing is tuned or fitted. Everything is calculated.**

| Kind of number | Where it lives | Example |
|---|---|---|
| Measured or defined input | `INPUTS`, each with uncertainty and source | quark masses (PDG 2024), H0 (Planck 2018), T_CMB |
| Measured result, used only to judge | `COMPARISONS` | CKM fit (PDG 2024), the age of the universe (Planck 2018) |
| Numerical-method setting | `NUMERICS`; the self-checks vary the key ones | RK4 steps, phase-grid size, Decimal digits |
| Published coefficient, too long to re-derive | `LITERATURE`, each with its source; self-checks reproduce the published results | three-loop SM and four-loop QCD β-functions, Higgs thresholds |
| Everything else | calculated | β-functions from Casimirs, the CKM matrix from an exact diagonalization |

[`tests/test_production.py`](tests/test_production.py) enforces the rule. It fails if any
non-integer number appears anywhere in the script outside those four tables, or if any
calculating function reads `COMPARISONS`.

Where the inputs cannot determine a quantity, the script does not pick a value. The two
phases of the quark mass matrices are the only such quantities, and each is scanned over its
whole range, [0, 2π). The prediction is the band that the scan sweeps out, and it is
compared with the measurement as a band.

## One model, one algorithm

The script runs as a chain of named stages, in order. A number is calculated once, in the
stage that produces it, and handed to every later stage that needs it: the superpartner scale
M_S and M_GUT from Part I, the Planck mass from Part H1, the quark-mass running from Part B.
Every read of a measured input and of another stage's result is recorded while the script
runs, so the dependency graph the report prints is the one the code followed, not a diagram
kept in step by hand. A test fails if any function reads `INPUTS` without going through the
recorder.

From that trace the report lists, for each stage, its evidence level (proved, exact,
numerical, conditional, parameter trade), the inputs it reads, the stages it takes results
from, and what it assumes. It also lists which stages each input reaches (change `M_t` and
seven stages are recalculated) and checks whether the stages' assumptions are compatible.
They are not: Parts I, J and K assume the MSSM above M_S, Part L the Standard Model up to
M_P, the SO(10) stages the Standard Model only up to each chain's M_I, and Parts D and E 3-3-1.
The script does not choose between them. Where one stage takes a result from a stage that
assumes a different field content (the place where the numbers could stop locking together),
the report lists the edge with its reason, for example the SO(10) chains take only Part L's
Standard-Model running below M_I, which every hypothesis shares; a test fails if any such edge
has no stated reason. Part M tests each against every combination of
the conditions the other parts impose (gauge unification, b-τ unification, the Higgs mass):

* **SM up to M_P** has no unknowns, so every condition is a prediction, and it misses each one:
  unification by 79σ, b-τ by 79σ, the Higgs mass from λ(M_P) = 0 by 3.3σ.
* **MSSM above M_S** has three unknowns (M_S, tan β, the stop mixing X_t). It meets any one or
  two of the conditions, but only because the unknowns absorb them: it never predicts anything.
  All three together exclude it at 24σ: unification fixes M_S, b-τ fixes tan β ≈ 1.33, and
  there the Higgs mass cannot exceed about 103 GeV.

Every verdict is given twice. The script calculates theory errors itself, never typing one in:
for every ingredient, the change from the last order it computes to the one below. The next
order is usually smaller than that step, so these give the weakest exclusions, and the truth
lies between the two columns. Two verdicts depend on them:

* **SM criticality**: 3.3σ with input errors, 2.95σ with theory errors, just inside the 3σ line.
  The theory error is 0.23 GeV (three-loop running against two), 0.001 GeV (SMDR's matching
  against the script's own) and 0.40 GeV (four-loop QCD against three). The last is the size
  of the four-loop term of the top pole/MS-bar conversion; the QCD series of the top pole mass
  falls by about a factor of three per order, so that step overstates the next one.
* **The MSSM with all three conditions**: 24σ, or 2.65σ once unification's one- to two-loop shift
  (12 in 1/α) is counted, because that frees M_S. Settling it needs three-loop gauge running
  with superpartner and GUT thresholds and the two-loop stop threshold.

With input errors only, no hypothesis and set of conditions both survives and predicts
anything; with theory errors, SM criticality would be the one that does. The audit findings,
open and resolved, are part of the output.

## What it calculates

**Part A: cosmology** (flat ΛCDM, the Friedmann equation, 50-digit Decimal arithmetic)

| Quantity | How | Result | Measured |
|---|---|---|---|
| Ω_γ | Stefan–Boltzmann law from T_CMB | 5.450 × 10⁻⁵ | |
| Ω_r | photons + N_eff = 3.044 neutrinos | 9.218 × 10⁻⁵ | |
| Ω_Λ | flatness: 1 − Ω_m − Ω_r | 0.6846 ± 0.0073 | 0.6847 ± 0.0073 |
| Age t₀ | Romberg quadrature of ∫ da / (a H) | 13.795 Gyr | 13.787 ± 0.020 Gyr |
| q₀, z_acc, z_eq | closed forms and root finding | −0.527, 0.631, 3420 | |
| Horizon entropies | π c⁵ / (G ħ H²) | 2.27 × 10¹²² k_B today, 3.31 × 10¹²² k_B de Sitter | |

**Part B: quark flavour** (the Fritzsch six-zero texture)

1. The six measured quark masses are run with the renormalization group. Below the top mass
   this is two-loop QCD and one-loop QED, with flavour thresholds at m_c, m_b and m_t. Above
   it there is one running for every coupling: the three Yukawa matrices (all generations and the
   CKM mixing) with the gauge couplings at one loop, evaluated at m_t(m_t) and at the superpartner
   scale M_S = 2.54 TeV that Part I derives. No scale is typed in. The top pole mass
   is converted to MS-bar at two loops. Every β-function and anomalous-dimension coefficient
   is computed from SU(N) Casimirs and the Standard Model field content, and checked against
   the textbook value.
2. The Fritzsch matrix [[0, A, 0], [A, 0, B], [0, B, C]] has its entries fixed exactly by its
   three eigenvalues. The script tries every sign assignment, finds that exactly one gives
   real entries, builds both quark sectors, and diagonalizes them exactly (Jacobi).
3. V = O_uᵀ · diag(1, e^{iσ}, e^{iτ}) · O_d for every (σ, τ). Each observable's band over the
   full phase torus is found and given the propagated input uncertainty.

Result at M_S = 2.54 TeV (m_t(m_t) agrees to within 3%):

| Observable | Band over all phases | Measured (PDG 2024) | Verdict |
|---|---|---|---|
| \|V_us\| | 0.1758 – 0.2614 | 0.22501 ± 0.00068 | inside |
| \|V_cb\| | 0.0741 – 0.1948 | 0.04183 ± 0.0007 | **outside by 32σ** |
| \|V_ub\| | 0.00266 – 0.00918 | 0.00373 ± 0.00009 | inside |
| \|V_ub/V_cb\| | 0.0359 – 0.0519 | 0.0892 ± 0.0026 | **outside by 14σ** |
| \|V_td/V_ts\| | 0.2274 – 0.2328 | 0.207 ± 0.003 | **outside by 5σ** |
| J | −3.55 – 3.55 × 10⁻⁴ | 3.12 × 10⁻⁵ | inside |

**Conclusion.** With nothing tuned, the quark masses in the six-zero texture reproduce the
Cabibbo angle, |V_ub| and the size of CP violation, but for no value of the phases do they
reproduce |V_cb|. The texture is excluded. This agrees with the literature, where the
six-zero Fritzsch texture is excluded by the heavy top quark.

**Part C: every texture-zero pattern that makes a prediction**

Part B tests one guess about the shape of the mass matrices. Part C tests all of them.
Each sector is a Hermitian matrix (always possible by right-handed rotations, which leave
the CKM matrix unchanged), and a symmetric off-diagonal pair counts as one zero.

* **Counting.** A sector with 3 zeros has its 3 entries fixed exactly by its 3 masses. A
  sector with 2 zeros keeps one free entry. Add the 2 phases between the sectors, plus a
  phase inside any sector whose three off-diagonals are all nonzero. The data are 4 numbers
  (|V_us|, |V_cb|, |V_ub|, J), so *predictions = 4 − unknowns*. Only pairs with five or six
  zeros predict anything.
* **Solving.** With no loop phase, the squared off-diagonal entries enter the trace, the
  sum of the 2×2 minors and the determinant linearly. Each sector is therefore solved
  exactly (linear algebra plus at most a cubic), with every sign assignment of the
  eigenvalues and every branch. One-parameter families are found on their exact intervals.
* **Testing, without fitting.** (1) The band test: for fixed rotations, each
  |V_ij| = |c₀ + c₁e^{iσ} + c₂e^{iτ}| sweeps exactly [max(0, 2 max|c| − Σ|c|), Σ|c|] over the
  phases. If a measurement lies outside that band at every value of the free entry, the
  pattern is excluded. (2) Otherwise, the joint test asks whether *any* point of the unknowns
  reproduces all four data at once. It converts the smallest χ² into a p-value with
  (predictions) degrees of freedom. The point found is never reported or used. It only
  decides survival, at the 3σ level.

Result: the 1,000 ordered pairs fall into 188 classes. 64 cannot give three real nonzero
masses, 41 keep a phase inside a sector and predict nothing, and **83 are tested. 82 are
excluded at every scale, and one survives:**

```
M_u = | 0 0 X |      M_d = | 0 X 0 |      chi^2 = 0.27 to 0.40 for 1 dof (0.5 to 0.6 sigma)
      | 0 X X |            | X 0 X |      at m_t(m_t) and at M_S
      | X X X |            | 0 X X |
```

The down sector is Fritzsch's. The up sector has five-zero structure, the kind of pattern
classified by Ramond, Roberts and Ross (1993). Every six-zero pattern is excluded,
Fritzsch's at 31σ or more.

**The exclusions are proved, not just searched** (`python3 production_v2_2.py --certify`, about
ten minutes on four cores; the report of that run is
[results/production_v2_2_certified.txt](results/production_v2_2_certified.txt)). The searches
above sample the parameter space; a certificate covers all of it (every point along every
family, both phases) with cells and proves for each that no point in it can fit. Along a
family the matrix entries are rational functions of the free entry with exact ranges, and the
eigenvalues never change, so eigenvector perturbation bounds turn the entry ranges into rigorous
bounds on every CKM element. **80 of the 82 exclusions are proved at m_t(m_t).** The two that are
not, 00X/0XX/XXX with 00X/0XX/XX0 and its mirror (excluded at 14σ and 17σ by the joint fit),
remain numerical: their certificates need finer cells than the budget allows. The survival
needs no certificate, since the search exhibits a point that fits.

**What the survivor predicts.** |V_us|, |V_cb| and |V_ub| fix its three unknowns at isolated
points; each then predicts |J| and |V_td/V_ts|, which the survey never used:

| at m_t(m_t) | \|J\| | \|V_td/V_ts\| |
|---|---|---|
| solution 1 | 2.90 ± 0.12 × 10⁻⁵ (−1.2σ) | 0.1966 ± 0.0030 (−2.4σ) |
| solution 2 | 3.23 ± 0.13 × 10⁻⁵ (+0.6σ) | 0.2751 ± 0.0034 (+14.5σ) |
| measured | 3.12 ± 0.13 × 10⁻⁵ | 0.207 ± 0.0032 |

Solution 2 is excluded by |V_td/V_ts|. Solution 1 is 2.2σ from both measurements together at
m_t(m_t) (1.4σ at M_S): the pattern survives, with a sharp prediction that a better measurement
of |V_td/V_ts| or J can test. (The PDG fit behind the measured moduli and J includes B-mixing
data, so the |V_td/V_ts| test is not fully independent of them.)

**Part D: what 3-3-1 says about the mass matrices**

The script derives the 3-3-1 charges from Q = T₃ + βT₈ + X, for β = −1/√3 and +1/√3, and
checks that the anomalies cancel. It then finds every gauge-invariant Yukawa operator.

* Every entry of both quark mass matrices is allowed. Rows 1 and 2 (the antitriplet
  families) get one vev and row 3 (the triplet family) gets another:
  M = diag(v_A, v_A, v_B) × (free Yukawas). **The gauge symmetry forces no texture zero, so
  3-3-1 by itself cannot rescue or select a pattern.** Zeros need an extra symmetry.
* The left-handed families split into gauge blocks {1, 2} and {3}. Only 2 of the 6 index
  permutations remain basis changes. The surviving class therefore becomes **3 distinct
  3-3-1 hypotheses**, which differ in which index is the triplet family. They give the same
  CKM matrix but different flavour-changing Z′ couplings, and that is what would tell them
  apart.

**Part E: can a flavour symmetry produce the survivor inside 3-3-1?**

The search covers abelian symmetries Z_N: each field gets a charge mod N, and a Yukawa
entry survives only if its charges sum to 0. Every abelian group is a product of such
factors, so scanning Z_N covers the abelian case. Everything is done for both β = ±1/√3.

* **E1, minimal scalars: no.** Each row of each mass matrix gets its mass from one scalar.
  The script computes that the down-minus-up scalar charge is the same for all three rows.
  So any abelian symmetry groups the rows in the same way in both sectors, and the CKM
  matrix then falls apart into blocks. An exhaustive scan of Z_2 to Z_6 confirms it: of
  50,364 realizable pattern pairs, **none** has a texture zero and three-family mixing.
* **E2, Hermiticity: impossible.** The survivor's one prediction relies on Hermitian
  matrices (M₁₂ = M₂₁* and so on). A symmetry would have to map the left-handed quarks
  (SU(3)_L triplets and antitriplets) onto the right-handed ones (singlets). No symmetry that
  commutes with SU(3)_L can do that.
* **E3, extra scalars: the zeros, but no prediction.** With extra copies of the two
  mass-giving scalars, **Z_6 with 6 scalar triplets** (4 more than minimal 3-3-1) gives
  exactly the survivor's zeros, in each of its three 3-3-1 placements. The charges are in
  the output, and the script re-derives the pattern from them. No Z_N with N ≤ 6 does it with
  fewer triplets. But the matrices are then general complex matrices: 11 magnitudes and 3
  phases, so 14 parameters for 10 observables and **−4 predictions**.

**Conclusion: no flavour symmetry inside 3-3-1 produces the survivor as a predictive
model.** Its prediction needs Hermitian mass matrices. That takes a symmetry exchanging left-
and right-handed quarks, so the gauge group must treat them alike: a left-right extension,
outside 3-3-1.

**Part F: does ANY texture of general mass matrices predict the CKM matrix?**

Inside 3-3-1 a symmetry can only put zeros into general (non-Hermitian) matrices. Part F
therefore checks every zero pattern of two general 3×3 matrices: 247² = 61,009 ordered pairs,
or 497 classes. The number of physical parameters of a pattern is the rank of the Jacobian of
10 weak-basis invariants of H = MM† (tr H, tr H², det H in each sector, and tr(H_u^a H_d^b)
for a, b = 1, 2), with respect to the entries. Every count is **proved**, not sampled:

* *Lower bound.* At integer points everything is an integer, and the elimination runs modulo
  a 61-bit prime. The rank found there can only be at or below the generic rank, and since 10
  is the largest possible rank, rank 10 at any point proves it.
* *Upper bound.* Unitary weak-basis transformations that keep every zero a zero (rephasings,
  and rotations of rows or columns with equal supports) leave all 10 invariants unchanged, so
  their tangent vectors are in the Jacobian's kernel. The rank is at most the number of real
  entries minus theirs. For all 472 candidates the two bounds meet.
* *CP.* J ∝ Im det[H_u, H_d]. A nonzero value at an integer point proves CP violation is
  possible; otherwise the polynomial is expanded symbolically, and an empty expansion proves
  J ≡ 0.

| Classes | Outcome |
|---|---|
| 19 | cannot mix all three families (structural: the CKM matrix splits into blocks) |
| 6 | no phase left after rephasing, so J = 0 |
| 470 | exactly 10 physical parameters for 10 observables: **no prediction** |
| 2 | rank 8 (bounds meet), but J ≡ 0 (symbolic expansion): excluded |
| **0** | **predict anything and allow CP violation** |

Scope: "no prediction" means no equality among the observables. A rank-10 pattern can still
be unable to reach the measured values (an inequality); Part F does not test that.

**Part G: other gauge frameworks.** 3-3-1 is not essential to the algorithm, so the script
asks the same question of the Standard Model and of left-right symmetric models.

* *Standard Model, any number of Higgs doublets:* an abelian symmetry makes zeros in general
  matrices, and Part F shows none of those predicts anything.
* *Left-right symmetric with parity:* the Yukawa matrices are Hermitian. But every bidoublet
  feeds both sectors through its two vevs, so the zeros sit in the same places in up and
  down ("parallel" textures). Part C tested all 3 parallel Hermitian classes that predict
  anything: all are excluded, at 31σ or more.

**Closure.** With abelian flavour symmetries and any number of scalars, in the Standard Model,
in left-right models and in 3-3-1, the quark sector closes with **10 measured inputs: 6 masses
and 4 CKM parameters**. Texture zeros calculate no CKM number. Calculating them needs
relations between nonzero entries (non-abelian flavour symmetries or grand unification),
which the script does not search.

**Part H: where quantum theory and gravity meet**

This part is a workshop in the spirit of a search for a theory of everything. It is built only
from established physics, and every apparent pattern carries its status. Everything follows
from G, ħ, c and k_B plus measured masses. The one exception is labelled: the one-loop
coefficient 41/(10π), quoted from Bjerrum-Bohr, Donoghue and Holstein 2003.

| | Result |
|---|---|
| H1 Planck units | l_P = 1.616×10⁻³⁵ m, E_P = 1.221×10¹⁹ GeV |
| H2 Quantum correction to Newton's law | Sun–Earth: 1.5×10⁻⁹² (the relativistic term is 3.0×10⁻⁸); for protons it overtakes the relativistic term below 0.22 Compton lengths; the effective theory ends at 1.14 l_P |
| H3 Black holes | the Sun: T_H = 6.2×10⁻⁸ K; the hole that evaporates in exactly the Part A age has 1.73×10¹¹ kg; de Sitter horizon: 2.2×10⁻³⁰ K, 3.3×10¹²² k_B |
| H4 Unruh effect | 4.0×10⁻²⁰ K at Earth's g |
| H5 Smallest mass gravity can ever entangle | (πħ²/(G c t₀))^(1/3) = 89 MeV/c² (0.095 m_p): maximal entanglement within the age of the universe at the closest allowed separation, the Compton wavelength. Zero if gravity is classical: the open test |
| H6 Why gravity is weak | the proton mass comes from Λ_QCD = 0.226 GeV, set by logarithmic running: ln(M_P/Λ) = 45.4 |
| H7 Large numbers | each one labelled as identity, known mechanism, measured input, or open |

The pattern that emerges is that two famous "coincidences" are exact identities:
α_G = (m_p/M_P)², and S_dS · ρ_Λ/ρ_Planck = 3/8. So the 10¹²² entropy and the 10⁻¹²³
vacuum energy are one fact. The weakness of gravity for a proton has a known cause,
logarithmic running. What remains open: α, the Yukawa couplings, ρ_Λ, and whether gravity
carries entanglement (H5), which is the measurement that would decide whether gravity is quantum.

A coincidence to watch: the smallest mass gravity can entangle within the age of the universe
(H5) is 0.64 m_π. It is the same combination of ħ, G, c and the Hubble time as Weinberg's 1972
large-number relation for the pion mass (0.43 m_π with H₀). The two agree in order of
magnitude, and no mechanism is known.

**Part I: can α be calculated from the other numbers?**

No accepted theory derives α. Grand unification is the one established framework that
relates it to other measured numbers. If the three gauge couplings meet at one scale,
1/α(M_Z) follows from α_s(M_Z) and sin²θ̂_W(M_Z) (PDG 2024: 0.23129 ± 0.00004) alone. The
script solves for that α. It runs the couplings at one and two loops, with coefficients computed
from the field content and checked against the textbook matrices.

| Content | 1/α(M_Z), 2-loop |
|---|---|
| Standard Model only | 81.8 (−36%: the SM couplings do not meet) |
| MSSM, superpartners at M_Z | 139.6 |
| MSSM, superpartners at 3 TeV | 127.4 |
| MSSM, superpartners at 10⁷ GeV | 98.7 |
| **measured** | **127.951 ± 0.009** |

So α is not calculated. Unification turns it into a function of one unknown, the superpartner
scale M_S. Read the other way, the measured α points to **M_S ≈ 2.5 TeV** (1.9–3.3 TeV from the
α_s and sin²θ_W errors), before the unknown threshold corrections. The closed formulas proposed
for 1/α (Eddington, Wyler, 4π³+π²+π) are all excluded by thousands of standard deviations or more.

**Part J: can the Yukawa couplings be calculated from the other numbers?**

No accepted theory gives them. Two established ideas relate them, and both are tested with
all scales taken from Part I:

* **Quark/lepton ratios from grand unification** (group theory). Minimal SU(5)'s
  m_s/m_d = m_μ/m_e (= 210.6) is off by 558σ. Georgi–Jarlskog's m_s/m_d = m_μ/(9m_e)
  (= 23.4) is off by 10σ from the measured 19.9 ± 0.3.
* **b–τ unification** (y_b = y_τ at unification). In the SM the ratio is 0.69 where g₁ = g₂
  and 0.58 at M_Planck. In the MSSM (M_S = 2.54 TeV, M_GUT = 1.15×10¹⁶ GeV from Part I, tan β
  scanned over its perturbative range) it is 0.77–0.86. It reaches 1 only at tan β = 1.33,
  where y_t(M_GUT) = 2.8, at the edge of perturbation theory.
* **The top quasi-fixed point.** In the SM, a large top coupling at M_Planck runs to
  m_t(m_t) = 217–220 GeV, against a measured 162.8. In the MSSM the measured top mass needs
  tan β = 1.31–1.38.

So no Yukawa coupling is calculated. In the MSSM, b–τ unification and the top fixed point
point to the same narrow region, tan β ≈ 1.3–1.4. That is one number, not a calculation of the
Yukawas. Part K tests it against the Higgs mass.

**Part K: the Higgs mass in the MSSM, from the scales of Parts I and J**

In the MSSM the Higgs self-coupling is not a free parameter: at M_S it is fixed by the gauge
couplings, tan β and the stop mixing X_t. The script matches λ(M_S) = (g² + g′²)/4 · cos²2β plus the
one-loop stop threshold (3y_t⁴/8π²)·X²(1 − X²/12), runs λ down to m_t in the SM, and takes
m_h = √λ · v. M_S (1.9–3.3 TeV) comes from Part I and tan β (1.31–1.38) from Part J. X_t is unknown,
so it is scanned. The threshold is largest at X_t² = 6 M_S², which gives an upper bound that holds
for every mixing.

| | Result |
|---|---|
| m_h, no stop mixing | 82–89 GeV |
| m_h, maximal mixing (upper bound) | **≤ 102.9 GeV** |
| measured | 125.20 ± 0.11 GeV |
| M_S that 125.2 GeV would need (tan β = 1.38, maximal mixing) | 1.3 × 10⁷ GeV, 8.6 e-folds above Part I |

The missing two-loop and pole-mass corrections are a few GeV in the literature, which leaves a
21 GeV gap. So the minimal MSSM with one superpartner scale cannot satisfy all four at once:
gauge unification at the measured α, b–τ unification, the top fixed point and the Higgs mass.
The route is excluded, with no free parameter adjusted.

**Part L: Standard Model criticality, the Higgs mass from one condition at the Planck scale**

If nothing new enters below the Planck scale, the Higgs self-coupling can be fixed there:
λ(M_P) = 0 (Froggatt–Nielsen 1996, Shaposhnikov–Wetterich 2010). Running it down with the
measured top mass and α_s predicts M_h, with no free parameter and no new particle.

* **Running:** one, two and three loops. The two-loop gauge b_ij come from the field content; the
  two-loop y_t and λ terms and all three-loop terms (plus the four-loop pure-QCD term of g₃) are
  quoted from Buttazzo et al. 2013, appendix B, read from the paper's LaTeX source. A self-check
  runs their own couplings at M_t to the Planck scale: three-loop running reproduces their printed
  Planck-scale values to 6 × 10⁻⁵, two-loop running misses by 8 × 10⁻⁴.
* **QCD** (shared with every part): α_s and the quark masses run at four loops (β₂, β₃, γ₂, γ₃ from
  RunDec), with three-loop decoupling at the c, b and t thresholds (Chetyrkin–Kniehl–Steinhauser),
  inverted exactly going up, and the top pole/MS-bar conversion at four loops (Melnikov–van
  Ritbergen; Marquard et al. 2015). Self-checks reproduce RunDec's α_s(M_b) = 0.2169467 and its
  α_s(1 GeV) at three and four loops, and Chetyrkin's numerical γ_m coefficient by coefficient.
* **Matching** to the pole masses M_h, M_t, M_W, M_Z and to G_F: one loop at μ = m_t(m_t) (their
  appendix A, Passarino–Veltman functions in closed form, checked against quadrature and against
  the one-loop RGE); two loops at μ = M_t (their interpolations of λ⁽²⁾ and of the electroweak
  parts of y_t⁽²⁾); three loops, its leading QCD part: λ⁽³⁾ at O(α_s² y_t⁴) (their footnote, from
  Martin 2013) and the pure-QCD y_t to four loops. With QCD at three loops, their inputs give
  their λ(M_t) and y_t(M_t) (0.12605 against 0.12604, 0.93689 against 0.93690).
* **Anchored to SMDR** (Martin–Robertson 2019), the most complete public matching: full two loops
  plus the leading three-loop terms, including the electroweak and mixed ones this script cannot
  transcribe. At SMDR's reference point the script's own couplings differ from SMDR's by
  −2.3 × 10⁻⁴ (λ) and −1.9 × 10⁻⁴ (y_t), inside Buttazzo et al.'s theory errors (a self-check);
  those differences are added at M_t, and the script's matching carries them to the measured
  inputs. The anchored M_h differs from the script's own by about a MeV.

| λ(M_P) = 0 (QCD at four loops unless noted) | M_h (GeV) |
|---|---|
| one-loop running, tree matching | 133.40 |
| two-loop running, one-loop matching | 127.58 |
| three-loop running, two-loop matching | 128.27 |
| three-loop running, two-loop matching, QCD at three loops (Buttazzo et al.'s order) | 128.67 |
| Buttazzo et al.'s own λ(M_Pl), solved at this script's M_t and α_s | 128.68 |
| three-loop running, three-loop matching (this script's own) | 128.34 |
| **three-loop running, matching anchored to SMDR** | **128.34 ± 0.95** (M_t, α_s, M_W errors) |
| measured | 125.20 ± 0.11 |

The last order of each ingredient moves the prediction by −0.23 GeV (three-loop running), +0.07
GeV (three-loop matching) and −0.40 GeV (four-loop QCD: running, decoupling and the top mass).
The gap is 3.1 GeV: 3.3σ on the input errors, 2.95σ once those last-order shifts are counted as
theory errors (Part M). The measured Higgs mass puts λ(M_P) at −0.0098, turning negative at
6 × 10¹⁰ GeV: the Standard Model sits just on the unstable side. Both Planck-scale conditions
together (λ = β_λ = 0, at two loops) give M_h = 130.7 GeV and M_t = 174.3 GeV. Not included: the
electroweak and mixed three-loop thresholds, and four-loop running beyond pure QCD.

All scales come from the algorithm. Parts B and C run at m_t(m_t) and at Part I's M_S. Part J
uses Part I's M_GUT and Part H's M_Planck. Part K uses Part I's M_S and Part J's tan β. The tan β range and the "large" top coupling come
from the perturbativity limit √(4π). The only numbers not produced by the algorithm are the
measured inputs, the numerical settings, the quoted coefficient 41/(10π), the quoted two-loop
y_t and λ coefficients and one-loop matching formulas of Part L, and the `LITERATURE` table
(three-loop running and matching, four-loop QCD), each checked by a self-check.

**Part N: can the quark and lepton masses be calculated? Closed mass formulas**

Part J tests what grand unification relates. What is left are closed formulas for the masses
themselves, tested the way Part I tests closed formulas for 1/α. The best known is Koide's (1982),
Q = (m₁ + m₂ + m₃)/(√m₁ + √m₂ + √m₃)² = 2/3, which no accepted theory derives. A relation among
masses needs a scale, so it is tested at the pole masses, at the running masses, and for the quarks:

| Masses | Q | Off 2/3 by |
|---|---|---|
| charged leptons, pole | 0.6666645 ± 0.0000051 | 0.4σ |
| charged leptons, MS-bar at M_Z (one-loop QED) | 0.66781 | 225σ |
| up quarks at m_t(m_t) | 0.888 | 289σ |
| down quarks at m_t(m_t) | 0.747 | 99σ |

Q = 2/3 at pole masses gives m_τ = 1776.97 MeV (measured 1776.93 ± 0.09). But running the
masses to M_Z, where they are couplings, moves Q by 225 times its error. A relation that holds only
for pole masses has no known mechanism: a coincidence to watch. No mass is calculated.

**Part O: the strong CP angle θ̄**

QCD allows a term θ G G̃ that violates P and CP; only θ̄ = θ − arg det(M_u M_d) is physical, and
the Standard Model gives it no value.

* **O1, the bound.** θ̄ makes a CP-odd pion–nucleon coupling, fixed at leading order by the strong
  part of m_n − m_p: ḡ₀ = δm_N m* θ̄/(m̄ ε) (de Vries, Mereghetti, Walker-Loud 2015). The pion loop
  (Crewther, Di Vecchia, Veneziano, Witten 1979) gives d_n = e g_πNN [ḡ₀/(2F_π)] ln(m_N/m_π)/(4π² m_N),
  with g_πNN = g_A m_N/F_π (Goldberger–Treiman). From the inputs: ḡ₀/(2F_π) = (15.5 ± 1.4)×10⁻³ θ̄
  (their published value: 15.5 ± 2.5) and d_n = (2.05 ± 0.18)×10⁻¹⁶ θ̄ e cm, between the QCD sum rules
  (2.4 ± 1.0) and lattice QCD (1.52 ± 0.71). With |d_n| < 1.8×10⁻²⁶ e cm: **|θ̄| < 8.8×10⁻¹¹**
  (2.2×10⁻¹⁰ with the weakest coefficient).
* **O2, the explanations.** A massless up quark is excluded: m_u is 31σ from zero. The axion makes
  θ̄ relax to zero but adds a scale f_a: m_a f_a = √z/(1+z) m_π F_π gives m_a = 5.77 ± 0.05 μeV ×
  (10¹² GeV/f_a) at leading order (NLO: 5.69 ± 0.05), so m_a = 0.5 neV at Part I's M_GUT. Parity:
  Hermitian mass matrices have real determinants, so arg det is 0 or π, and flipping a sector's sign
  (which V cannot see) always reaches θ̄ = 0 at tree level. The Part C survivor is checked. But
  Hermiticity needs left-right parity (Part E), whose textures Part G excludes.
* **O3, the SM's own CP violation.** It reaches θ̄ only through Im det[H_u, H_d] = 2J Π(y²
  differences), about 3×10⁻²⁴ at m_t(m_t), and first diverges at seven loops (Ellis–Gaillard).

θ̄ is bounded, not calculated: every explanation adds an unmeasured number or a symmetry whose
predictive textures are excluded.

**Part P: neutrino masses and mixing**

NuFIT 6.0 gives the mass-squared differences and the PMNS matrix. Not measured: the lightest mass
m₀, the ordering, two Majorana phases, and the origin of the masses. Each unknown is scanned.

| | Normal ordering | Inverted ordering |
|---|---|---|
| smallest Σm_ν (m₀ = 0) | 58.8 ± 0.2 meV | 98.9 ± 0.4 meV |
| vs Planck 2018 (< 120 meV) | allowed, m₀ < 30 meV | allowed, m₀ < 16 meV |
| vs DESI DR2 + CMB (< 64 meV) | allowed, m₀ < 4.1 meV | **excluded at 95%** |
| m_β at m₀ = 0 (KATRIN: < 450 meV) | 8.8 meV | 48.8 meV |
| m_ββ band at m₀ = 0 (Majorana phases scanned) | 1.5 – 3.7 meV, can vanish for m₀ = 2.3–6.5 meV | 18.2 – 48.2 meV, a floor |

The m_ββ band over the phases is exact, [max(0, 2 max c − Σc), Σc] with c_i = |U_ei|² m_i, the same
band as Part C's. KamLAND-Zen's 28–122 meV does not yet reach the inverted floor. Ω_ν h² follows
from T_CMB (Σm_ν = 94.1 eV for Ω_ν h² = 1): 0.4% of Ω_m at the normal minimum.

**Mixing patterns from discrete flavour symmetries**, tested like Part C's textures. The fixed
patterns (tribimaximal, bimaximal, two golden-ratio forms, hexagonal) predict θ₁₃ = 0 and are
excluded at 39σ. The corrected patterns TM1 and TM2 keep one column of the tribimaximal matrix and
add an angle and a phase; θ₁₃ and θ₂₃ fix those two unknowns exactly, so each predicts θ₁₂ and δ:

| | sin²θ₁₂ | δ (two solutions) | Verdict |
|---|---|---|---|
| TM1 (normal) | 0.3182 ± 0.0004 (+0.9σ) | 262° or 98° | survives |
| TM2 (normal) | 0.3409 ± 0.0002 (+2.9σ) | 286° or 74° | survives, just |
| measured | 0.308 ± 0.012 | 212 (+26 −41)° | |

TM1 reproduces the published sum rule for cos δ to 10⁻⁶ (a test). Quark–lepton complementarity,
θ₁₂ + θ_C = 45°, is off by 2.4σ.

**Where the masses come from.** In a seesaw, m = y²v²/(2M): with the heaviest mass of 50 meV,
M = 6×10¹⁴ GeV for y = 1 and at most 7.6×10¹⁵ GeV for a perturbative y, below Part I's M_GUT. Dirac
neutrinos need y_ν ≤ 3×10⁻¹³. This tests Part L: the SM up to M_P holds only if neutrinos are Dirac.

**Part Q: proton decay, the direct test of unification**

If the couplings unify (Part I), the SU(5) gauge bosons turn quarks into leptons, and the proton
decays through p → e⁺π⁰. The width (Ellis et al. 2020, minimal SU(5)) takes lattice matrix elements
(Aoki et al. 2017). The operators' running from M_X to M_Z uses exponents −2c_i/b_i built from the
script's own b_i, which a self-check compares with the printed ones. Their QCD running to 2 GeV uses
the script's α_s: A_L = 1.27 at one loop, against 1.247 at two loops (quoted).

| Hypothesis | M_X (GeV) | α_GUT | τ(p → e⁺π⁰) | vs Super-K (> 2.4×10³⁴ yr) |
|---|---|---|---|---|
| MSSM above M_S (Part I) | 1.15×10¹⁶ | 0.0389 | 2.4×10³⁵ yr | allowed, 10× the limit |
| SM, X bosons where g₁ = g₂ | 1.0×10¹³ | 0.0236 | 5×10²³ yr | excluded |

The supersymmetric lifetime agrees with Ellis et al.'s scaling formula to 10% and lies within reach
of Hyper-Kamiokande.

**Dimension five.** In minimal supersymmetric SU(5), the colour-triplet Higgsinos give p → ν̄K⁺
(Hisano, Kobayashi, Kuwahara, Nagata 2013, eqs. 15–49). Every input is taken from earlier stages:

* M_HC = M_GUT, and every superpartner at M_S (Part I); tan β from Part J.
* The Yukawas run in the SM up to M_S and in the MSSM up to M_HC.
* The operators run with the Yukawas above M_S, with the gauge couplings below M_S, and with QCD
  down to 2 GeV.
* The two unknown GUT phases are scanned.

The result is τ = 3×10²⁸ to 7×10²⁹ years over all phases, against Super-K's 5.9×10³³. **Minimal SUSY
SU(5) with one superpartner scale is excluded by proton decay**, as it is by the Higgs mass (Part K).
The limit would need M_HC ≈ 10¹⁸ GeV or superpartners near 200 TeV. The higgsino part reproduces Hisano et
al.'s scaling formula (eq. 19) exactly in form: τ/[sin⁴2β (0.1/Ā_R)² (M_S/100 TeV)² (M_HC/10¹⁶ GeV)²] comes out the
same constant, 1.77×10³⁵ years, at every tan β (to 10⁻¹⁵). The old factor 2.3 against their 4×10³⁵ is 1.65 from the
lattice matrix element (α_p = −0.0144 GeV³ here, Aoki et al. 2017; −0.0112 in their paper) times 1.37 from eq. 19's
one-digit constant and its 2013 quark masses. It was not a bug.

**Part R: what anomaly cancellation fixes (exact)**

A chiral gauge theory is consistent only if its gauge anomalies cancel. These are exact conditions
on the charges, and the one place where the Standard Model's quantum numbers are calculated:

* **Hypercharges.** One family with unknown hypercharges, under [SU(3)]²U(1), [SU(2)]²U(1),
  [gravity]²U(1) and U(1)³, solved exactly in rational arithmetic. Two solutions remain, which are
  the SM's assignment under the two namings of u^c and d^c. A third branch, with Y_Q = 0, also
  cancels, but it allows no Yukawa coupling. Requiring Yukawas gives the SM uniquely.
* **Charge quantization.** It follows: q_u = 2/3, q_d = −1/3, q_e = −1, so the proton plus the
  electron has charge 0, and so does the neutron.
* **Right-handed neutrino.** It reopens one direction: SM + ε(B − L) cancels for every ε. Hydrogen
  stays neutral, but the neutron gets charge ε. A Majorana mass, as in Part P's seesaw, forces ε = 0.
* **Witten's SU(2) anomaly.** There are 4 doublets per family, an even number, so it cancels.
* **3-3-1 (Part D).** [SU(3)_L]³ cancels only if N_f(N_c − 1) = 2N_c·k, so for N_c = 3 the number of
  families is a multiple of 3: 3, 6, 9, and so on. Asymptotic freedom of QCD then leaves **exactly
  three families**, the one free integer of the SM that a gauge theory calculates.
* **The full 3-3-1 set.** With the lepton triplets (ν, e, ℓ₃) (X fixed by Q(ν) = 0; ℓ₃ neutral for β = −1/√3, a
  heavy charged lepton for +1/√3) and the conjugate singlet of every charged component, all six anomalies vanish
  exactly for both embeddings: SU(3)_C³, SU(3)_L³, SU(3)_C²U(1)_X, SU(3)_L²U(1)_X, U(1)_X³ and gravity²U(1)_X.
  Without the leptons SU(3)_L³, SU(3)_L²X and X³ fail.

**Part S: the baryon asymmetry**

η_B = n_B/n_γ = (6.116 ± 0.041)×10⁻¹⁰, calculated from Planck's Ω_b h² and T_CMB. Making it needs
Sakharov's three conditions:

* **The Standard Model alone fails two of them.** Sphalerons violate B + L, changing each by
  N_f = 3, and chemical equilibrium gives B = 28/79 (B − L), solved exactly. But for the measured
  Higgs mass the transition is a crossover: the lattice endpoint is 72.4 ± 1.7 GeV, 31σ below
  125.2. And the CKM CP violation at T_c, J Π(m²_i − m²_j)/T_c¹², is 4×10⁻²⁴, 14 orders too small.
* **Leptogenesis works, at a price.** The seesaw of Part P gives η_B = c_sph (3/4)(g*_s,0/g*) ε₁κ.
  Every factor follows from the field content: c_sph = 28/79, g* = 108.5, g*_s,0 = 43/11, so the
  prefactor is 0.96×10⁻², Buchmüller–Di Bari–Plümacher's value, reproduced. The SM bound on the CP
  asymmetry, |ε₁| ≤ 3M₁(m₃ − m₁)/(16π⟨H⟩²) (their eq. 31; Davidson–Ibarra write the MSSM form, which
  is twice as large), needs M₁ ≥ 6.5×10⁸ GeV at full efficiency (they find 6.6×10⁸).
* **The efficiency is calculated.** κ_f = 2/(K z_B)(1 − e^{−K z_B/2}) with K = m̃₁/m_*, where
  m_* = 1.07 meV follows from g* and M_P, and z_B solves their freeze-out equation exactly (eqs. 22,
  59). Over the natural range m_sol ≤ m̃₁ ≤ m_atm, κ_f runs from 0.043 to 0.005, so **M₁ ≥ 1.5×10¹⁰
  to 1.3×10¹¹ GeV**. All of that is inside Part P's seesaw window. Each SO(10) chain allows M₁ up to
  2√(4π) M_I/g_R (its M_I is the W_R mass g_R v_R, and M_N = 2f v_R with a perturbative f), the same
  ceiling Parts T7 and Y4 use: for the left-right chain 12.6 M_I = 3.7×10¹⁰ GeV, which covers the
  natural range (Part Y4's fits put M₁ at 5×10⁹–1.7×10¹⁰ GeV). Part L's SM up to M_P, which needs
  Dirac neutrinos, has no such mechanism.

**Part T: SO(10)**

SO(10) puts a whole family, with a right-handed neutrino, into one 16.

* **Group theory (exact).** Gauging B − L is anomaly-free only with ν^c: without it, [gravity]²(B−L)
  and (B−L)³ are −1. Over a complete 16, sin²θ_W = Tr T₃²/Tr Q² = 3/8 at unification, and
  Tr T₃²/Tr Y² = 3/5, the hypercharge normalization the script uses throughout, now derived.
* **Minimal Yukawas** (one 10_H) make the three sectors' mass ratios equal and V = 1. At M_S,
  (m_s/m_b)/(m_c/m_t) is far from 1: excluded. With a 126_H each sector gets its own matrix,
  which has enough parameters to fit the data but predicts nothing (Part F).
* **t–b–τ unification** in the MSSM (Part I's scales) needs y_t = y_b at large tan β, where
  y_b/y_τ ≈ 0.78. That requires a supersymmetric threshold correction of about +28% to m_b,
  which depends on the unknown spectrum: a trade, not a test.
* **Non-supersymmetric SO(10) through Pati–Salam** SU(4)×SU(2)_L×SU(2)_R. The b_i come from the
  field content: (−23/3, −3, 11/3). The three measured couplings then fix the three unknowns
  exactly, through a linear system at one loop: **M_I = 5.5×10¹¹ GeV, M_GUT = 1.1×10¹⁶ GeV,
  1/α_GUT = 45.7.** With Part Q's formula the proton lives about 6×10³⁵ years, which passes
  Super-K. M_I, where B − L breaks and the right-handed neutrinos get their mass, falls inside the
  window leptogenesis needs (Part S). This one chain joins Parts I, P, Q and S without
  supersymmetry. It still predicts nothing, since three couplings fix three unknowns, and two-loop
  running and the thresholds decide whether it holds. In this picture Part L's SM runs only up to
  M_I.

**Part T5: every minimal SO(10) chain at two loops.** Each chain's one- and two-loop gauge
coefficients come from its field content, using the Machacek–Vaughn formula. The same code
reproduces the SM's textbook matrices exactly (a self-check). The SM runs at two loops below M_I.
At two loops the matching carries the heavy vector bosons' MS-bar constant, which has no unknown:
1/α_i(low) = 1/α_i(high) − T_i/12π with T_i the broken generators' Dynkin index (= C₂(SO(10)) − C₂(H_i) at M_GUT,
the W_R and leptoquarks at M_I; Langacker–Polonsky eq. 12, C¹ = 1/21; a self-check). It raises every chain's M_I by
about 5% and M_GUT by about 4%. The heavy masses' splittings are Parts T7, T12 and T13. Every chain has exactly as many
unknowns as conditions, so none predicts a coupling; the solution only locates the scales:

| Chain | b (one loop) | M_I, M_GUT (two loops, GeV) | τ(p → e⁺π⁰) | λ(M_I) = 0 gives m_h |
|---|---|---|---|---|
| Pati–Salam | (−23/3, −3, 11/3) | 1.5×10¹¹, 8.4×10¹⁵ | 1.4×10³⁵ yr | 125.6 GeV |
| Pati–Salam + D-parity | (−14/3, 11/3, 11/3) | 4.6×10¹³, 8.8×10¹⁴ | 1.8×10³¹ yr: **excluded** | 127.4 GeV |
| SU(3)×SU(2)²×U(1)_{B−L} | (−7, −3, −7/3, 11/2) | 2.9×10⁹, 1.6×10¹⁶ | 1.9×10³⁶ yr | 123.3 GeV |
| same + D-parity | (−7, −7/3, −7/3, 7) | 3.2×10¹⁰, 2.4×10¹⁵ | 1.0×10³³ yr: **excluded** | 124.8 GeV |

Above M_I the proton-decay operators run with the chain's own gauge group. Their anomalous dimensions are
derived, not transcribed: in Landau gauge the fermion wave functions are not renormalized, and for an operator
(ψψ)(χχ)† only gauge exchanges inside a Lorentz-scalar bilinear count, each 6 T_i·T_j (the value that gives a mass
its −6C₂; T_i·T_j = −(N+1)/2N for ε-contracted SU(N) fundamentals), while left–right exchanges cancel. This
reproduces Ellis et al.'s SM coefficients exactly for both operators (a self-check) and gives −15/2, −9/2, −9/2 g²
for Pati–Salam and −4, −9/2, −9/2, −1/2 g² for the left-right group. Running with the chain's own group shortens
each lifetime by 8–23 % against SM running throughout; no verdict changes.

Proton decay excludes both D-parity chains. Two loops move Pati–Salam's M_I down from 5.5×10¹¹
to 1.4×10¹¹ GeV, and its λ(M_I) = 0 Higgs mass from 126.1 to 125.6 GeV, against 125.20 measured.

**Part T6: what λ(M_I) really is.** The heavy scalar that breaks a chain at M_I shifts the SM
quartic at tree level (Elias-Miró, Espinosa, Giudice, Lee, Strumia 2012, eq. 5):
λ_SM(M_I) = λ_H − λ_HS²/λ_S. The shift is positive and unknown, so λ(M_I) = 0 is not a condition
of the theory. What is fixed is this: the vacuum can be stable only if the SM's λ stays positive up
to M_I, that is, if M_I lies below the scale μ₀ where λ turns negative. For the measured Higgs
mass μ₀ = 6.2×10¹⁰ GeV (2.3×10¹⁰ to 2.0×10¹¹ for M_t ± 1σ). Both left-right chains break below
μ₀, so the threshold can stabilize them. Pati–Salam's M_I = 1.4×10¹¹ lies inside the top-mass
band, so whether it is stable is decided by M_t. The "λ(M_I) = 0" Higgs masses only measure how
close each chain's M_I lies to μ₀: the 125.6 GeV of Pati–Salam is a coincidence of scales, not a
prediction. The scorecard has a vacuum-stability row.

**Part T7: are the chain verdicts robust against thresholds?** The masses of the heavy fields at M_I
and M_GUT are unknown, so each matching condition is shifted by up to ±1 in 1/α. That band is an
assumption: one heavy multiplet with b ≈ 2, a factor e from the matching scale, gives about 0.3.
Every corner is solved at two loops:

| Chain | M_I range (GeV) | τ_p range (yr) | Verdicts that can flip |
|---|---|---|---|
| Pati–Salam | 1.5×10¹⁰ – 1.3×10¹² | 5×10³² – 3×10³⁷ | proton decay, vacuum |
| Pati–Salam + D | 2.8×10¹³ – 6.7×10¹³ | 3×10²⁹ – 7×10³² | none: **robustly excluded** |
| Left-right | 9×10⁷ – 9×10¹⁰ | 4×10³³ – 7×10³⁸ | proton decay, vacuum, leptogenesis |
| Left-right + D | 5×10⁹ – 2×10¹¹ | 7×10³⁰ – 1×10³⁵ | all three, including its exclusion |

So only Pati–Salam with D-parity is excluded whatever the thresholds. The surviving chains'
verdicts depend on the heavy spectrum, which is what has to be calculated next.

**Part T8: the heavy spectrum, by group theory.** In the Pati–Salam chain a 210 breaks SO(10). The
heavy components of the 210, the 126 and the 10 sit at M_GUT, with masses set by the unknown scalar
potential. Each component shifts the couplings at M_GUT by (b^h/2π) ln(M_h/M_GUT), where b^h follows
from group theory; a self-check confirms that every decomposition adds up to its SO(10) index (1, 35,
56). Two components dominate, both SU(2)_L triplets: the 126's (10,3,1) and the 210's (15,3,1).
Proton decay flips if the (10,3,1) alone is about half as heavy as M_GUT. With all eight masses
anywhere within a factor 10 of M_GUT, M_I spans 10⁷–10¹⁶ GeV and τ_p spans 10²⁷–10⁴³ years.
**In non-supersymmetric SO(10), the heavy spectrum, not the running, decides every verdict.**
Calculating it needs the scalar potential's couplings, which nothing measured fixes.

**Part T9: the 210's own potential.** Four of those masses can be calculated. The 210 is the
antisymmetric tensor φ_ijkl; its potential is built from every invariant (a mass term, one cubic,
four quartics), with the vev on the Pati–Salam singlet. Each multiplet's mass is the curvature
along one representative direction. The construction is checked by the Goldstone theorem: the
eaten (6,2,2) comes out exactly massless for every coupling. The cubic coupling is what splits
(15,3,1) from (15,1,3). The couplings are scanned within a perturbative box (|λ| ≤ 1, |η/v| ≤ 1;
an assumption), and a point counts only if the vacuum is a local minimum and the potential is
bounded below along a fixed set of random directions. Over the viable potentials, with the 126's
and 10's components still at M_GUT:

* proton decay passes for about 77% (median τ_p ≈ 8×10³⁴ years);
* M_I has a median near 1.5×10¹¹ GeV, and natural leptogenesis works for nearly all of them;
* the vacuum can be stabilized for about 20%.

The verdicts are now fractions of a calculated parameter space instead of an assumed band.

**Part T10: the 126's masses from its couplings to the 210.** The 126 is the self-dual part of a
complex 5-form. Every invariant bilinear in it (the norm, one cubic, the quartics) becomes a mass
matrix, and the Pati–Salam multiplets are its eigenspaces. A self-check confirms self-duality and
that (10,3,1) and (10̄,1,3) do not mix. Only the cubic coupling, the one odd under D-parity, tells
(10,3,1) from (10̄,1,3). The chain needs (10̄,1,3) light, because its vev breaks Pati–Salam at M_I, and
that gives an exact result: **m²(10,3,1) = 2η₂v**. The dominant multiplet of T8 is set by one
coupling. With the 126's couplings scanned as well, most jointly viable potentials pass proton
decay, put M_I a little lower (median a few ×10¹⁰ GeV, often below the SM instability scale, so
the vacuum can be stabilized), and keep natural leptogenesis. The fractions depend on the scan's
priors, as the report states.

**Part T11: the 10's couplings.** No cubic H H φ exists, because 10×10 = 1 + 45 + 54 holds no 210.
The one quartic that splits the 10 is H_i H_j A_ij with A_ij = φ_iklm φ_jklm, and at the vacuum
A_ij is 6v² on the SO(4) indices and 0 on the SO(6) ones (a self-check). That coupling alone
splits the doublet (1,2,2) from the colour triplet (6,1,1). The cubic H_i Σ_ijklm φ_jklm mixes that
triplet with the 126's own (6,1,1). The light doublet fixes the 10's mass term; that is the
doublet–triplet splitting, a cancellation to (M_I/M_GUT)², assumed as in every SO(10) model. With
the 210's, the 126's and the 10's couplings all scanned, the lighter colour triplet sits near
M_GUT (median about 1.4 M_GUT). Most jointly viable potentials pass proton decay through the gauge
bosons, and most keep natural leptogenesis and a stabilizable vacuum. Not included: proton decay
through the colour triplets' own Yukawa couplings, which needs the Yukawa matrices at M_GUT.

**Part T12: the left-right chain's heavy spectrum.** SO(10) → SU(3) × SU(2)_L × SU(2)_R × U(1)_{B−L} without
D-parity needs the 210 on both of its 3221 singlets: the Pati–Salam singlet (odd under D) and the B − L direction
of its (15,1,1); the (3,2,2) and (3,1,1) are eaten. Every heavy multiplet of the 210, 126 and 10 is listed with
its B − L charge, and a self-check confirms that each decomposition adds up to the SO(10) index under all four
factors. Their threshold responses split cleanly: SU(2)_L-triplet coloured states (the 126's (6,3,1), the 210's
(8,3,1)) lower M_I when heavy, SU(2)_R ones raise it, by up to 1.5 in ln M_I per unit of ln(M_h/M_GUT).

**Part T13: the left-right chain's own potential.** The 210's vev now has both components,
φ = v (cos α e_PS + sin α e_BL). The multiplets are not typed in: in a complex basis every wedge monomial is a weight
vector of the rank-5 Cartan subalgebra, and each 3221 multiplet is found as the vectors its raising operators
annihilate. That separates the 210's two (3,2,2) and two singlets, which come out as 2 × 2 blocks of the Hessian.
Stationarity on the singlet plane fixes μ² and the cubic for scanned quartics and α. The heavy vectors split:
(3,2,2) defines M_GUT, and (3,1,1) is a threshold of its own. The 126's masses come from T10's invariants at the
new vev, with Δ_R light. Self-checks: the decompositions; at α = 0 every mass equals T9's and every 126
coefficient T10's (to 10⁻¹⁵); the eaten (3,2,2) and (3,1,1) are massless at any two-vev vacuum. The 10 follows
T11: H_iH_jA_ij splits it (A = 4 sin²α v² on SO(6), 6 cos²α v² on SO(4)), and the cubic H_iΣ_ijklmφ_jklm mixes its
colour triplet with the 126's (3,1,1) and, through the B − L vev, its doublet with the 126's bidoublet (strength
sin α). One doublet combination is kept light (the doublet–triplet tuning). So the light Higgs is a computed
10–126 mixture (median about a quarter 126), which is what Part Y's sum rule assumes, and the lighter colour triplet
sits near M_GUT. Over the viable 210 + 126 + 10 potentials, proton decay passes about 98% of the time and M_I tends
to fall (median ≈ 9 × 10⁸ GeV).

**Part V: dark matter from the axion**

Until now the dark-matter density was an input. The axion of Part O is produced by misalignment:
it sits frozen at an angle θ_i until 3H = m_a(T), then oscillates and redshifts like matter. The
script calculates this from its ingredients (Di Luzio, Giannotti, Nardi, Visinelli 2020, eqs.
148–169). It takes m_a f_a from Part O, M_P from Part H, g_S today = 43/11 from Part S and T₀ from
T_CMB; the dilute-instanton m_a(T) is quoted. The result reproduces the paper's own eq. 170 to 1.3%
(a self-check). After inflation, misalignment alone gives all of Ω_c h² = 0.1200 at
**f_a = 2.0×10¹¹ GeV, m_a = 28.5 μeV**. If the axion scale is each SO(10) chain's M_I (an
order-of-magnitude identification: f_a = v_PQ/N_DW, with PQ broken alongside B − L):

| Chain | f_a = M_I | m_a | Post-inflation misalignment | Pre-inflation |
|---|---|---|---|---|
| Pati–Salam | 1.5×10¹¹ GeV | 39 μeV | 69% of the dark matter | θ_i = 2.59 gives all |
| Left-right | 2.9×10⁹ GeV | 2.0 meV | 0.7% | impossible (θ_i > π) |

The same identification at the B − L scale SO(10)'s Y₁₂₆ needs for the neutrinos (Part Y4, ~10¹³ GeV)
would overclose post-inflation: until f_a comes from a PQ-charged potential, the dark-matter and
neutrino rows rest on different B − L scales (an open audit finding).

So at the Pati–Salam scale the axion makes about two thirds of the dark matter from misalignment
alone; strings and domain walls, whose yield is not agreed on, only add to it. Unification,
neutrino masses, the strong CP problem and dark matter would then share one scale. At the
left-right scale the axion cannot be the dark matter.

**Part W: the W mass, a test of the Standard Model itself**

Given G_F, α, M_Z, m_t and m_h, the SM fixes M_W through its quantum corrections. The script uses the
full two-loop result in its published parametrization (Awramik, Czakon, Freitas, Weiglein 2004,
accurate to 0.5 MeV) with the PDG's Δα_had⁽⁵⁾ = 0.02783. The Higgs mass is the one Part L
calculates; using the measured one instead moves M_W by +1.4 MeV.

| | M_W (GeV) | pull |
|---|---|---|
| this script (SM) | 80.350 ± 0.004 | |
| PDG 2024 global fit (SM) | 80.353 ± 0.006 | +0.5σ |
| measured, without CDF II | 80.360 ± 0.012 | +0.8σ |
| measured, PDG 2024 average | 80.369 ± 0.013 | +1.4σ |

The effective weak mixing angle of the Z couplings, from the same authors' two-loop parametrization
(2006), comes out at sin²θ_eff = 0.23164 ± 0.00003, against 0.23151 ± 0.00016 (LEP + SLC) and
0.23149 ± 0.00013 (hadron colliders).

The SM prediction agrees with the measurements and reproduces the PDG fit. Because it uses Part L's
Higgs mass, it is the M_W of the SM-to-M_P hypothesis (and the stage is tagged with it); with the measured
m_h it is the low-energy SM's, common to every hypothesis, since the SO(10) chains' heavy states decouple.
The PDG average is also an input of Part L's matching, so only the other two comparisons are independent.

**Part X: closing the loop, cosmology from the particle physics**

Part A takes Ω_m as an input. Here it is built from the rest: Ω_b (measured), the axion at the
M_I of each surviving chain (or, when none survives, of each closest one) by misalignment (Part V) and the
minimal neutrino masses (Part P). Flatness then gives Ω_Λ, and the Friedmann equation gives the age:

| Closest chain | axion share of Ω_c | Ω_m | age | vs Planck's 13.787 Gyr |
|---|---|---|---|---|
| left-right | 0.7% | 0.052 | 21.3 Gyr | **378σ** |
| Pati–Salam | 69% | 0.233 | 15.0 Gyr | **60σ** |
| left-right + D | 12% | 0.081 | 19.4 Gyr | **282σ** |

With all of Ω_c the same code returns Part A's 13.797 Gyr (a self-check). Closing the loop therefore needs
the rest of the dark matter (31% to 99%) from the axion's strings and domain walls, or from a second component.

**Part AA: dark matter beyond the axion, and inflation**

* **No other candidate.** A stable particle needs a symmetry. The 126's vev breaks B − L by two units and leaves
  exactly R = (−1)^{3(B−L)+2s}. All 28 multiplets of the minimal left-right theory (the 16's fermions; the 10's,
  126's and 210's scalars) are R-even, so every new particle can decay to SM ones, and only the axion (0.7% of
  Ω_c by misalignment at the chain's M_I) is a candidate. An R-odd neutral state needs one more multiplet: a scalar
  16 (an inert doublet or singlet) or a fermionic 10, 45, 54, … Its mass would be a new unknown: open.
* **Inflation**, slow roll computed from each potential (the e-fold integral and the ε = 1 endpoint, checked
  against the exact φ² and φ⁴ results), N = 50–60, against Planck's n_s = 0.9649 ± 0.0042 and BICEP/Keck's r < 0.036:

  | Potential | n_s | r | |
  |---|---|---|---|
  | plateau: Higgs, or any scalar with a large ξφ²R | 0.962 – 0.968 | 0.004 – 0.003 | allowed |
  | φ⁴, minimal (a GUT scalar) | 0.941 – 0.951 | 0.31 – 0.26 | excluded |
  | φ², minimal | 0.960 – 0.967 | 0.16 – 0.13 | excluded |

  Higgs inflation needs λ > 0 where its plateau sits, h ~ M_P/√ξ. Part L's λ turns negative at μ₀ = 6 × 10¹⁰ GeV,
  so ξ ≥ (M_P/μ₀)² = 1.5 × 10¹⁵, and the CMB amplitude (λ/ξ² = 4–5 × 10⁻¹⁰) would then need λ ≈ 10²¹. **SM Higgs
  inflation is excluded by the measured masses.** A 210 or 126 direction with its own ξ can inflate on the
  plateau, but ξ is a new unknown, so that is allowed, not predicted.

**Part Y: the SO(10) Yukawa sector, can it give the charged-fermion masses?**

With a 10 and a 126 the Yukawa matrices are symmetric and shared: M_u = a Y₁₀ + b Y₁₂₆,
M_d = c Y₁₀ + d Y₁₂₆ and M_e = c Y₁₀ − 3d Y₁₂₆.

* **Pati–Salam: excluded (exact selection rule).** Between M_I and M_GUT, SU(4) is unbroken and the
  210's vev is a Pati–Salam singlet, so nothing can mix the 10's (1,2,2), an SU(4) singlet, with the
  126's (15,2,2), an SU(4) 15. Part T11's contraction confirms that ⟨210⟩ reaches only the (6,1,1).
  The light Higgs therefore lies in one SU(4) irrep, which gives M_e = M_d (the 10) or M_e = −3M_d
  (the 126) for every generation at once. At M_I the measured ratios are m_e/m_d = 0.36,
  m_μ/m_s = 3.83 and m_τ/m_b = 1.34, which misses 1 by 88σ and 3 by 11σ or more. **The minimal
  Pati–Salam chain cannot give the charged-fermion masses**; it needs more Yukawa structure (a 120,
  or a vev that breaks SU(4) at M_GUT).
* **Left-right chain: reaches them.** There SU(4) breaks at M_GUT, so the doublets can mix, and
  eliminating Y₁₀ and Y₁₂₆ gives the sum rule M_e = c₁M_d + c₂M_u with complex c₁ and c₂. With M_u
  real and diagonal, M_d = ΨVXD_dXVᵀΨ; the up-quark phases Ψ are physical for symmetric Yukawas,
  and leaving them out had made the search fail. A seeded search with structured starts (a
  Georgi–Jarlskog-sized c₁ whose excess in the 33 entry c₂m_t cancels) finds a point that reaches
  all three lepton masses within 0.2%. With 8 unknowns and 3 masses that predicts nothing yet; the
  test is the neutrino sector (Y3, Y4 below). A found point
  proves reachability; some seeds of the search fail to find one, which says nothing against it.

The scorecard now has a fermion-mass row. It moves the surviving chain from Pati–Salam to the
left-right one.

**Closing the algorithm: the neutrino test (Part Y3), the survivor fed back (Part X), the ledger (Part Z)**

* **One running for every coupling.** Every running mass and mixing above m_t(m_t) comes from one engine:
  the gauge couplings with the full 3×3 Yukawa matrices (all generations, the CKM mixing) in the SM, in the
  MSSM above M_S (after y_SM = y_MSSM sin β or cos β) and in a chain's left-right stage above M_I. The MSSM
  matrix RGE is checked against the general superpotential formula written over every component (to 10⁻¹⁶).
  Part J's third-generation right-hand sides are the engine restricted to the third generation (a check, to
  10⁻¹⁶); the light generations and the mixing move its results by 0.03 % (y_t, y_b, y_τ at M_P) and 0.04 %
  (y_b/y_τ at M_GUT in the MSSM). The light-quark ratios now run too (they were held fixed above m_t).
* **Running to the left-right M_GUT.** Between M_I and M_GUT the chain is SU(3) × SU(2)_L × SU(2)_R ×
  U(1)_{B−L} with one bidoublet, −L = Q_L (Y₁Φ + Y₂Φ̃) Q_R + leptons. Its matrix RGE is derived, not quoted:
  the general one-loop formula (Machacek–Vaughn) is written out over every field component, checked on the
  SM's matrix RGE, and fixes the reduced form exactly (a self-check, to 10⁻¹⁶):
  16π² dY₂/dt = 2Y₂Y₂†Y₂ − Y₂Y₁†Y₁ − Y₁Y₁†Y₂ + T Y₂ + 2Tr(3Y₂Y₁† + Y₄Y₃†) Y₁ − gauge. Because u_R and d_R
  share an SU(2)_R doublet, y_t pushes y_b up (+4y_t² in d ln(y_b/y_τ)) where the SM pushes it down. The
  masses and the CKM matrix run in the SM to M_I, are matched symmetrically there (the second doublet's vev
  neglected), and run in the left-right theory to M_GUT, where the four couplings meet (a check).
  (m_b − m_τ)/m_b at M_GUT goes from −0.60 (SM running) to −0.41.
* **Y3: type-II neutrinos.** With type-II seesaw, M_ν ∝ M_d − M_e, so the same unknowns must also give the
  three PMNS angles and Δm²₂₁/Δm²₃₁ (the six quark masses float within their errors: 13 data). They don't:
  the best point misses by about 19σ (sin²θ₂₃ ≈ 0.18). Large atmospheric mixing from M_d − M_e needs b and τ
  to converge at M_GUT (Bajc–Senjanović–Vissani); even with left-right running they don't.
* **Y4: type I, and types I + II.** Type I adds no unknown. The same c₁, c₂ fix the Dirac matrix,
  M_D = M_u + (3 + c₁)/c₂ (M_d − M_e) (a self-check verifies the algebra), and M_R ∝ M_d − M_e, so
  M_ν ∝ M_D (M_d − M_e)⁻¹ M_D. Types I + II add one complex ratio. The right-handed masses follow without any
  vev: M_R,i = s_i(M_d − M_e) · s_max(M_ν matrix)/m₃. The fits also carry the overall phase of M_d against
  M_u, which the charged leptons cannot see but the neutrinos can (9 unknowns; with the 10 quark observables,
  the model's 19 parameters). For types I + II only the direction of M_ν matters, so it is written as
  M_ν ∝ cos θ K̂ + sin θ e^{iφ} D̂: both pure limits are ordinary points. (As a ratio w of the two terms they
  are endless flat valleys, w → 0 and w → ∞, which a local search runs into and never leaves; that, not the
  physics, is why earlier searches found no fit.) Levenberg–Marquardt runs from 1,000 seeded starts per type in
  parallel (three in four of the Georgi–Jarlskog-structured kind), with cross-seeding and small kicks of the
  32 best points:

  | Seesaw | Unknowns / data | Best χ² | Fits within 3σ | Heaviest M_R / M_I |
  |---|---|---|---|---|
  | type II | 15 / 13 | 440 | 0 (worst observable 19σ) | – |
  | type I | 15 / 13 | 150 | 0 | ≈ 10³ at the best point |
  | types I + II | 17 / 13 | 0.0 | 11 | 180 – 380 over the fits |

  **The mixed type I + II case fits.** With 17 unknowns for 13 data it reaches the data rather than predicting
  it, and the CP phase is not pinned: δ = 36°–353° over the fits (the measured 212° lies inside; the count of fits and this range move with
  tiny changes to the inputs, so they reflect the search more than the physics). What every
  fit shares is the right-handed scale: M_R,3 is 180 to 380 times the chain's M_I = 2.9 × 10⁹ GeV. The lightest
  right-handed neutrino comes out at M₁ = 5 × 10⁹ to 1.7 × 10¹⁰ GeV, above the full-efficiency leptogenesis bound.
* **The neutrino tension, settled.** Two relations decide it.
  - *The perturbative bound, sharpened.* The chain's M_I is the W_R mass, M_WR = g_R v_R for the triplet's vev,
    and a Majorana mass from f νν δ⁰ is M_N = 2 f v_R. With f ≤ √(4π) the heaviest right-handed neutrino is at
    most 2√(4π) M_I/g_R ≈ 12.6 M_I (not √(4π) M_I as earlier). The fits then need M_I ≈ 14 times higher. The heavy
    spectrum (Part T12) can do that with every multiplet within a factor 1.33 of M_GUT, the proton surviving at
    4.3 × 10³⁴ years; the chain's own potential (Part T13) does it in 4 of 715 viable cases.
  - *SO(10) fixes the coupling.* The Δ_R coupling is Y₁₂₆ itself (M_R = Y₁₂₆ v_R and M_d ⊃ d Y₁₂₆ in the same
    normalization), and the charged-fermion fit fixes Y₁₂₆ = (M_d − M_e)/4d, d the light Higgs's down-type 126
    component. The light Higgs's 126 share f (T13: 4–63%) splits into up- and down-type parts, |b|² + |d|² = κ²f,
    and every fit fixes their ratio: M_u = (a/c)A + (b/d)B with A = cY₁₀, B = dY₁₂₆ gives a/c = (1 − c₁)/c₂ and
    b/d = (−3 − c₁)/c₂, with |b/d| = 27–32 and |a/c| = 59–64 over the fits. So |d| = κ√(f/(1 + |b/d|²)) (roadmap 5b;
    giving all of f to d, as before, overestimated it 30-fold), and the fits predict v_R = 4 × 10¹² to 2 × 10¹³ GeV:
    800 to 4000 times the chain's own v_R = M_I/g_R = 5.2 × 10⁹ GeV. Whatever the potential gives for f, a
    perturbative Y₁₂₆,₃ ≤ 2√(4π) keeps v_R ≥ M_R,3/2√(4π) = 7 × 10¹⁰ GeV, 14 times the chain's. The unknown
    thresholds move M_I by at most 31 (Part T7), so that floor alone would not decide; the verdict rests on T13's
    126 share (f ≥ 4%), which puts v_R 800 times above, 25 times beyond any threshold. So within the minimal
    10 + 126 theory **the left-right chain fails the neutrinos**, with a margin 30 times smaller than before 5b.
  - *A real 10 is excluded.* Its bidoublet is self-conjugate, so its doublet's up- and down-type vevs are complex
    conjugates and |a| = |c|, i.e. |c₂| = |1 − c₁|. The same charged-lepton search with that imposed (7 unknowns)
    reaches only χ² = 6×10³ (m_μ = 0.022 GeV against 0.093): the 10 must be complex, as the fits assume.
  - *The complex 10's own potential decides it.* T13 now also scans the complex 10 (two real 10s, complex cubic
    couplings η_a, a symmetric splitting κ_ab), on its own random stream. The chain needs a light complex bidoublet,
    two real SO(4) vectors out of four (the two 10s' and the 126's two), so the Schur complement must vanish:
    D₁₀ = XXᵀ/m₁₂₆, which fixes the 10's doublet mass matrix completely (three conditions; a real 10 has only three
    vectors and can leave just one light). Its two triplets mix with the 126's (3,1,1); the thresholds come from the
    eigenstates: 4073 of 8648 draws are viable, all pass proton decay. Inside the light bidoublet the light Higgs is
    h = n₁ + z n₂ with z complex (picked at the v_R scale); each fit's |a/c| and |b/d| are two Apollonius circles in z,
    and at their intersections |d|, so v_R, is predicted (a self-check recovers a planted Higgs exactly). 52 points
    (1.3%) give the fits' Higgs, and at every one v_R is at least 3600 times that point's own v_R = M_I/g_R (median
    3 × 10⁴): far beyond any threshold, with no assumption about the 126 share.
  - *What is left of the running (5c).* A second bidoublet vev up to |k₂/k₁| = m_b/m_t (beyond it the bottom mass
    would be the top's, a tuning) moves (m_b − m_τ)/m_b at M_GUT only to −0.48 … −0.35. The Δ_R coupling f, run with
    the rest, only makes the τ heavier: its RGE, derived from the general formula over every component (a check,
    to 10⁻¹⁶), is 16π² df/dt = 6ff†f + 2Tr(ff†)f + Aᵀf + fA − gauge with A = Y₃†Y₃ + Y₄†Y₄, and it adds 3Yf†f to
    the leptons' Y₃, Y₄. At the largest f(M_I) that stays perturbative to M_GUT (f₃ = 0.85) the mismatch is −1.58.
    Nothing within reach makes b and τ meet.
* **Proton decay through the colour triplets.** They couple through the same Y₁₀ and Y₁₂₆ that give the masses.
  An estimate uses the best fit's first-generation entries (Y₁₀,₁₁ ≈ 8×10⁻⁴, Y₁₂₆,₁₁ ≈ 1×10⁻³, with the light Higgs
  a quarter 126 from Part T13, split by the fit's |a/c| and |b/d|), Clebsch factors up to 3, and the lighter triplet
  at T13's 1.3 M_GUT. The amplitude is about 4×10⁻⁵ of the gauge bosons': τ ~ 10⁴⁵ years. The triplets would matter
  only below ~4×10¹³ GeV.
* **No complete hypothesis survives.** The left-right chain fails the neutrinos, Pati–Salam the fermion masses
  and left-right with D-parity proton decay: each fails exactly one condition. Parts X and Z follow every one of
  these closest chains (fewest fails; the tie is carried, not broken by counting trades).
* **Part Z: the ledger.** Every free number of the Standard Model plus cosmology carries the status
  the stages computed for the closest hypotheses (shown for the left-right chain; the rows that differ for the
  others are printed after it). Nothing is credited from a framework that is not the hypothesis:

| Quantity | Count | Status |
|---|---|---|
| hypercharges, charge quantization | 5 per family | calculated (exact) |
| number of families | 1 | open (3-3-1 fixes it, but 3-3-1 is not on the scorecard) |
| weak mixing angle at unification | 1 | calculated (3/8) |
| gauge couplings | 3 | traded (for M_I, M_GUT, α_GUT) |
| Higgs mass | 1 | open (criticality 3.3σ off) |
| Higgs vev, quark masses, G | 1 + 6 + 1 | input |
| CKM | 4 | input (the predictive Hermitian texture comes from no framework tested) |
| charged-lepton masses | 3 | traded (sum rule, 8 unknowns); open for Pati–Salam |
| neutrino masses and mixing | 7–9 | open: no working mechanism (type II excluded; type I + II fits need v_R ~ 10¹³ GeV, ≥ 14× the chain's); traded for Pati–Salam (seesaw at M_I) |
| strong CP angle | 1 | bounded (< 9×10⁻¹¹) |
| dark matter, Λ | 1 + 1 | open (dark matter traded for Pati–Salam: 69% from misalignment, an angle for the rest) |
| baryon asymmetry | 1 | traded (leptogenesis, M₁ unknown, at most 2√(4π) M_I/g_R) |

Totals for the left-right chain: calculated 2, input 4, traded 3, bounded 1, open 5 (Pati–Salam: open 4,
traded 4).

**The algorithm closes.** It runs in one pass, every stage in dependency order, and every free number has a
status. What it calculates is discrete and exact: the charges and their quantization and sin²θ_W at
unification (the family number only in 3-3-1, which is not a complete hypothesis here). No continuous free
number of the Standard Model is calculated. And no complete hypothesis survives every condition: the closest
SO(10) chains each fail one, the left-right chain the neutrinos because SO(10) itself puts B − L breaking near
the unification scale, Pati–Salam the fermion masses by an exact selection rule.

**Part U: the scorecard, every complete hypothesis against every condition**

Part M weighs the high-energy hypotheses against unification, b–τ and the Higgs mass. Parts P–T add
neutrino masses, proton decay, the baryon asymmetry, the strong CP angle and the SO(10) chains.
Each entry below is the verdict the stage that computes it reached, labelled by fixed rules: *pass*
only for a test the hypothesis could have failed; *trade* when an unknown absorbs the condition (three
couplings fixing three unknown scales is a trade, as is a seesaw with a free Dirac Yukawa or a vacuum a
threshold of unknown size can stabilize); *open* when the hypothesis has no mechanism or does not impose
the condition (λ(M_I) = 0, Part T6).

| Condition | SM to M_P | minimal SUSY SU(5) | SO(10) via Pati–Salam | SO(10) via left-right | left-right + D |
|---|---|---|---|---|---|
| gauge unification | fail (79σ) | trade (M_S) | trade | trade | trade |
| b–τ unification | fail (79σ) | trade (tan β) | open | trade (sum rule) | trade |
| Higgs mass | fail (3.3σ) | fail (m_h ≤ 103 GeV) | open | open | open |
| neutrino masses | trade (Dirac) | trade | trade (seesaw at M_I) | **fail** (v_R ≥ 800× short) | open |
| proton decay | pass (no GUT) | **fail** (p → ν̄K⁺) | pass (1×10³⁵ yr) | pass (2×10³⁶ yr) | **fail** (1×10³³ yr) |
| baryon asymmetry | fail | trade | trade | trade (M₁ ≤ 12.6 M_I) | trade |
| strong CP | open | open | trade (axion) | trade | trade |
| vacuum stability | open | pass | open | trade | trade |
| dark matter | open | trade | trade (69% + angle) | open (0.7%) | open (12%) |
| fermion masses | trade | **fail** | **fail** (selection rule) | trade (8 unknowns) | trade |

Pati–Salam, left-right and left-right with D-parity each fail exactly one condition, and each passes at
most one real test (proton decay). Counts of trades and open entries do not rank them (every relabelling
reorders those counts), so all three are carried forward as the closest into Parts X and Z. Left-right with
D-parity's one failure, proton decay, is one the thresholds of Part T7 can flip. **No complete hypothesis
survives every condition.**

The λ(M_I) = 0 values (125.6 GeV for Pati–Salam) are still printed, but Part T6 shows the theory does not
impose that condition: they only say how near each chain's M_I lies to the SM instability scale.

## Adjacent sims: one piece changed at a time

Each file in [`sims/`](sims) is the whole production script with one piece swapped, under the same rules:
nothing tuned or fitted, every self-check passing, standard library only. Each can be copied or downloaded
like the main script (the website has the same **Copy Python script** button for each), and
`sims/<name>.diff` is its exact difference from `production_v2_2.py`. Its expected output is in
`results/sims/`; [`tests/test_sims.py`](tests/test_sims.py) applies the no-tuning tests to every sim, checks
that the diff is current, and (one CI job per sim) runs it in full against its expected output.

**[sims/so10_flavour.py](sims/so10_flavour.py): SO(10) in place of 3-3-1, plus a two-step left-right chain and
Pati–Salam with a light (15,2,2).**

* *Parts D, E, R asked of SO(10).* The 16 × 16 Yukawa bilinears come from the exact spinor algebra (the ten
  32 × 32 gamma matrices, elimination mod p): the 10 and 126 are symmetric, the 120 antisymmetric, and together
  they span every coupling. So SO(10)'s mass matrices are symmetric, never Hermitian, and the one surviving
  Hermitian texture of Part C loses its prediction (9 physical parameters as Hermitian matrices, 10 as symmetric
  ones; both proved). An abelian Z_N (N ≤ 6) on whole 16s with the minimal 10 + 126 makes every sector share one
  support; 15 classes make relations among the 13 charged-fermion observables (the exact Jacobian rank), and a
  fit of each to Part Y's masses and mixing at M_GUT misses by more than 100σ. With one more Higgs field there
  are 81 such classes, counted but not fitted. The family number is no longer calculated: SO(10) is anomaly-free
  for any number, and asymptotic freedom with the chain's scalars plus CP violation leave 3 to 5 (bounded).
* *Part T14, the two-step left-right chain* SO(10) → 3221 → 3211 → SM, with B − L breaking below SU(2)_R. The
  family in M_BL is solved at two loops; with M_BL = M_R it returns the one-step chain (a self-check). The W_R
  scale stays near 10⁹ GeV whatever M_BL is, and since M_WR ≥ g_R v_R the B − L vev stays below about 2 × 10⁹
  GeV, short of what SO(10)'s Y₁₂₆ needs (Part Y4) by 37 times at the weakest floor and thousands of times over
  the fits. **It fails the neutrinos too**: the scale problem belongs to every SO(10) → 3221 chain with this
  field content.
* *Part T15, Pati–Salam with the 126's (15,2,2) near M_I.* Part Y's selection rule (M_e = M_d or −3M_d) holds only
  if the whole (15,2,2) of the 126 sits at M_GUT. With it near M_I, the B − L vev that breaks SU(4) there mixes the 10's
  and the 126's doublets, and the 10 + 126 sum rule applies at M_I. The extra complex (15,2,2) changes the running
  (b = −7/3, 2, 26/3): at two loops M_I = 2.0 × 10¹⁰ GeV, M_GUT = 3.6 × 10¹⁶ GeV, τ_p = 2 × 10³⁷ years. The sum rule
  reaches the charged-lepton masses, and the type I + II search finds 54 neutrino fits (M_R,3 = 35–162 M_I, M₁ =
  5 × 10⁹–2 × 10¹⁰ GeV). **It fails no condition: the first complete hypothesis here that does.** It predicts nothing
  new, and two rows stay open. The neutrinos: with M_R = Y₁₂₆ v_R, a perturbative Y₁₂₆ needs v_R at least 2.3 times
  the chain's own M_I/g_R (against 3600 times for the left-right chain) when the (15,2,2) sits at M_I.
* *Part T15b, the (15,2,2) mass scanned.* With M_15 = r M_I from M_I to M_GUT (two-loop running with a step at
  M_15; at r = 1 it returns the T15 chain and above M_GUT minimal Pati–Salam, a self-check), raising r lifts M_I and
  so v_R, but weakens the doublet mixing: the light Higgs's 126 share is δ²/(δ² + M_15⁴) with δ = λv_R² from one
  quartic. Below r ≈ 30 v_R is under the fits' floor; at **r = 32** (M_I = 4.7 × 10¹⁰ GeV, v_R = 1.0 × 10¹¹ GeV) the
  mixing needs **λ = 0.88**, inside T9's assumed box |λ| ≤ 1; at r = 56 it needs 2.9. The window is one grid step
  wide (r = 32–100 with perturbativity alone, |λ| ≤ 4π), and the fits are T15's, not redone at each M_15. The
  neutrino row becomes a trade, and every row of the chain is read at that working point: proton 4 × 10³⁶ years,
  vacuum stabilizable (M_I < μ₀), leptogenesis open up to M₁ = 7 × 10¹¹ GeV, and the axion at 18% of the dark matter
  (the universe 18.6 Gyr old in Part X). **It fails nothing; the dark matter stays open.** Next: the Pati–Salam
  potential with a light (15,2,2) (the real mixing and thresholds instead of one quartic), the fits redone at the
  working point, f_a from a PQ charge, and a dark-matter candidate.

## What changed from production v1

The first version of `production_v2_2.py` (commit `2fa12f0`) gave χ² ≈ 3,600 for its Fritzsch
module and χ² ≈ 359,000 for its "resistance" module. Its outputs depended on hand-set numbers.
v2.2 replaces each one:

| v1 | Problem | v2.2 |
|---|---|---|
| `cp_phase_rad = 1.144` | the measured CKM phase, put in as input | removed; phases scanned over [0, 2π) |
| `theta_23_rad = 0` | a free phase set by hand | scanned |
| overlap model: `c1..c3, w1..w3, phi_12..phi_13`, `(abs(m) - 0.5)` and `2, 3 × eps` factors | arbitrary parameters, no derivation | removed |
| resistance model: `r1..r3`, `0.45 + 1.55 s^p`, widths `0.85/(1 + 0.45 r)`, phase coefficients `0.25, 0.18, 0.15, 0.22, 0.37, 0.05` | arbitrary parameters, no derivation | removed |
| cosmology–flavour feedback: `delta Omega_L = -(J/J0) ... × 1e-4`, entropy couplings `1e-6`, `1e-5`, `j_ref_scale = 3e-5` | invented couplings; `J0` was the measured J | removed: no calculated coupling exists, so there is no loop to close |
| `"status": "verified_within_1.3_sigma"` | hard-coded verdict string | removed; verdicts are computed |
| `Omega_r = 9.2e-5`, `Omega_Lambda = 0.685` | entered by hand | calculated from T_CMB, N_eff and flatness |
| `v_ew = 246.22` | entered by hand | (√2 G_F)^(−1/2) |
| FLRW ODE over `t_span = (0, 10)` from `a0 = 0.01` | arbitrary span; `a_final` meaningless | the age, by quadrature from a = 0 |
| two-loop mass anomalous dimension | off by a factor of 2 | corrected, and computed from Casimirs |
| up-type-only `3 y_t² / (32 π²)` term | not the Standard Model RGE | SM one-loop Yukawa RGE for the ratios |

## Repository layout

```
production_v2_2.py            the simulation
results/production_v2_2.txt   its expected output
tests/test_production.py      the no-tuning rule, the self-checks, the pinned numbers
sims/                         adjacent sims (one piece changed each) and their diffs
results/sims/                 their expected outputs
tests/test_sims.py            the same rules for every sim; full runs with STUR_SIM=<name>
tools/sim_diff.py             writes sims/<name>.diff
index.html                    website: the ladder, the results and their curves
assets/site-data.js           every number and curve the website shows (generated)
tools/site_data.py            writes assets/site-data.js from one run of the simulation
ROADMAP.md                    the phases still to build, and their status
archive/                      notes and the 3-3-1 paper from the earlier codebase (prose only)
```

The earlier modules, notebooks and tools are in the git history (last at commit `2fa12f0`).
The files in `archive/` refer to them by their old paths.

## Licence

CC0 1.0: public domain. Copy it freely.
