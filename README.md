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
python3 production_v2_2.py                     # full report, about 3 minutes
python3 production_v2_2.py --json-out out.json # every number, as JSON
python3 production_v2_2.py --scales 2000 5000  # other evaluation scales (GeV, above m_t)
```

Or copy the file (the [website](https://sheldonlindberg-afk.github.io/STUR-Physics-Lab/) has a
**Copy Python script** button; on GitHub use *Copy raw file*) and paste it into any Python 3.8+
runner, notebook or AI assistant's code tool. The expected output is
[results/production_v2_2.txt](results/production_v2_2.txt). It ends with 28 self-checks, which test
the calculation itself, not its agreement with data.

## The rule

**Nothing is tuned or fitted. Everything is calculated.**

| Kind of number | Where it lives | Example |
|---|---|---|
| Measured or defined input | `INPUTS`, each with uncertainty and source | quark masses (PDG 2024), H0 (Planck 2018), T_CMB |
| Measured result, used only to judge | `COMPARISONS` | CKM fit (PDG 2024), the age of the universe (Planck 2018) |
| Numerical-method setting | `NUMERICS`; the self-checks vary the key ones | RK4 steps, phase-grid size, Decimal digits |
| Everything else | calculated | β-functions from Casimirs, the CKM matrix from an exact diagonalization |

[`tests/test_production.py`](tests/test_production.py) enforces the rule. It fails if any
non-integer number appears anywhere in the script outside those three tables, or if any
calculating function reads `COMPARISONS`.

Where the inputs cannot determine a quantity, the script does not pick a value. The two
phases of the quark mass matrices are the only such quantities, and each is scanned over its
whole range, [0, 2π). The prediction is the band that the scan sweeps out, and it is
compared with the measurement as a band.

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
   it, the same-type mass ratios are run with one-loop Standard Model Yukawa and gauge terms,
   up to each of the four 3-3-1 benchmark scales (1.5, 3.5, 7 and 10 TeV). The top pole mass
   is converted to MS-bar at two loops. Every β-function and anomalous-dimension coefficient
   is computed from SU(N) Casimirs and the Standard Model field content, and checked against
   the textbook value.
2. The Fritzsch matrix [[0, A, 0], [A, 0, B], [0, B, C]] has its entries fixed exactly by its
   three eigenvalues. The script tries every sign assignment, finds that exactly one gives
   real entries, builds both quark sectors, and diagonalizes them exactly (Jacobi).
3. V = O_uᵀ · diag(1, e^{iσ}, e^{iτ}) · O_d for every (σ, τ). Each observable's band over the
   full phase torus is found and given the propagated input uncertainty.

Result at 3.5 TeV (the four scales agree to within 1%):

| Observable | Band over all phases | Measured (PDG 2024) | Verdict |
|---|---|---|---|
| \|V_us\| | 0.1758 – 0.2614 | 0.22501 ± 0.00068 | inside |
| \|V_cb\| | 0.0743 – 0.1949 | 0.04183 ± 0.0007 | **outside by 32σ** |
| \|V_ub\| | 0.00267 – 0.00919 | 0.00373 ± 0.00009 | inside |
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
M_u = | 0 0 X |      M_d = | 0 X 0 |      chi^2 = 0.29 to 0.37 for 1 dof (0.5 to 0.6 sigma)
      | 0 X X |            | X 0 X |      at 1.5, 3.5, 7 and 10 TeV
      | X X X |            | 0 X X |
```

The down sector is Fritzsch's. The up sector has five-zero structure, the kind of pattern
classified by Ramond, Roberts and Ross (1993). Every six-zero pattern is excluded,
Fritzsch's at 31σ or more.

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
for a, b = 1, 2), with respect to the entries. The rank is computed **exactly**: at integer
points everything is an integer, and the elimination runs modulo a 61-bit prime. Since 10 is
the largest possible rank, finding rank 10 at any point proves it.

| Classes | Outcome |
|---|---|
| 19 | cannot mix all three families |
| 6 | no phase left, so J = 0 |
| 470 | exactly 10 physical parameters for 10 observables: **no prediction** |
| 2 | rank 8, but J ≡ 0 (checked in exact Gaussian integers): excluded |
| **0** | **predict anything and allow CP violation** |

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
from G, ħ, c and k_B plus measured masses. The two exceptions are labelled: the one-loop
coefficient 41/(10π) (quoted from Bjerrum-Bohr, Donoghue and Holstein 2003), and the
design of the entanglement experiment.

| | Result |
|---|---|
| H1 Planck units | l_P = 1.616×10⁻³⁵ m, E_P = 1.221×10¹⁹ GeV |
| H2 Quantum correction to Newton's law | 3.4×10⁻⁷⁰ at 1 m; for protons it overtakes the relativistic term below 0.22 Compton lengths; the effective theory ends at 1.14 l_P |
| H3 Black holes | the Sun: T_H = 6.2×10⁻⁸ K; the hole that evaporates in exactly the Part A age has 1.73×10¹¹ kg; de Sitter horizon: 2.2×10⁻³⁰ K, 3.3×10¹²² k_B |
| H4 Unruh effect | 4.0×10⁻²⁰ K at Earth's g |
| H5 Gravity-mediated entanglement | 10⁻¹⁴ kg design: entangling phase 0.066 rad, concurrence 0.033. Zero if gravity is classical: the open test |
| H6 Why gravity is weak | the proton mass comes from Λ_QCD = 0.226 GeV, set by logarithmic running: ln(M_P/Λ) = 45.4 |
| H7 Large numbers | each one labelled as identity, known mechanism, measured input, or open |

The pattern that emerges is that two famous "coincidences" are exact identities:
α_G = (m_p/M_P)², and S_dS · ρ_Λ/ρ_Planck = 3/8. So the 10¹²² entropy and the 10⁻¹²³
vacuum energy are one fact. The weakness of gravity for a proton has a known cause,
logarithmic running. What remains open: α, the Yukawa couplings, ρ_Λ, and whether gravity
carries entanglement (H5), which is the measurement that would decide whether gravity is quantum.

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
production_v2_2.py            the simulation (the only script in this repository)
results/production_v2_2.txt   its expected output
tests/test_production.py      the no-tuning rule, the self-checks, the pinned numbers
index.html                    website: one page, one Copy button
archive/                      notes and the 3-3-1 paper from the earlier codebase (prose only)
```

The earlier modules, notebooks and tools are in the git history (last at commit `2fa12f0`).
The files in `archive/` refer to them by their old paths.

## Licence

CC0 1.0: public domain. Copy it freely.
