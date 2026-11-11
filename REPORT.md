# STUR and the search for a unifying equation: development record

*Research notes, not peer reviewed. This is the record of how the work developed,
failures included. For a plain-language introduction, see the guide (index.html).*

*Status as of November 2026. Every number below is computed by a script in `src/` and
pinned by `tests/` (121 tests, all passing). Detailed records are in the topic reports
linked from each section.*

## How the work was done

- **Hostile-referee rules.** Every claim is labelled with one of:
  - KNOWN: published and tested;
  - FOLLOWS: derived with no new assumption;
  - CONDITIONAL: derived, but only under assumptions that are stated next to it;
  - CHECK: reproduces a known exact result;
  - STUR: a new claim;
  - LIT: a literature input.
- **Inputs.** LIT inputs are marked *retrieved* when read in this work, and *recalled*
  when quoted from memory.
- **Numbers.** Every number is computed in code.
- **Negative results** are recorded as results.

## Bottom line

1. **STUR's original claims all failed their computed tests.** What survived of the
   original equation is established physics under new names.
2. **A unifying equation of known physics does exist.** The replica generating function
   puts horizon entropy, quark confinement, decoherence and local thermodynamics in one
   expression, and it has lattice support. It is a synthesis, not new physics.
3. **One conditional new result.** In 3-3-1 gauge models, requiring every coupling to
   stay perturbative up to the Planck scale selects exactly **3 colours = 3
   generations**, and through anomaly cancellation the **⅓ quark charges**.
4. **No continuous parameter was produced.** Masses, the Higgs mass, the gauge couplings
   and dark energy were not derived. Every mechanism tried either misses by 3–5%, only
   accommodates the data, or fails. There is a measurable trade-off: the structure that
   fixes the integers adds the free parameters that block the numbers.
5. **Gravity: conditional, and not distinctive.** In the later measurement–gravity
   work, gravity follows each branch (λ = 1) only if a statistical gravity is smeared at
   the entanglement cutoff and is Markovian. λ = 1 is also perturbative quantum
   gravity's prediction. The shape-free one-particle bound on Oppenheim's classical
   gravity, Γ·S_a ≥ (M²/4)I² (OPPENHEIM.md), is a worked example within an existing
   literature, not a new result (NOVELTY.md §3).

---

## 1. STUR's original equation: what failed

Details: POSTULATE_TEST.md, ASSUMPTIONS.md, OPEN_PROBLEMS.md, OPTION_A.md, WALL.md.

| STUR claim | Computed result |
|---|---|
| S_R = −k_B ln V ("visibility loss is entropy") | Matches no standard entropy. Exact in only two limits: weak decoherence, and zero temperature (record fidelity). |
| E_R = ½k_BTΦ² (said to follow from Landauer) | Landauer applies to erasure, not dephasing. At fixed energy, standard decoherence gives Γ ∝ T⁺¹ where STUR gives T⁻¹. Agreement only at ħω = 2.40 k_BT, a coincidence that moves with the model. |
| The Smarr check (E_R = ½Mc²) | Circular: it reproduces an identity that was built in (the user's correction). |
| One A_μ and one σ(μ) from QCD to the Planck scale | No known connection meets all requirements. The 10³⁸ ratio is (E_P/√σ_QCD)², which is dimensional analysis. |
| Quarks as spacetime folds | Skyrme folds give baryons (nucleon and Δ reproduced: e = 5.445, F_π = 129.3 MeV). A B = ⅓ fold costs 0.18 E_P. |
| An empty universe triggers tunnelling | The Vilenkin barrier R = 3ρ_P/(8ρ) *grows* as ρ → 0. |
| Information paradox | STUR's entropy behaves like the coarse-grained curve and breaks STUR's own area bound after the Page time (0.5381 t_evap). |
| Option A: spacetime records which-path information | Excluded by 8–13 orders of magnitude (LISA Pathfinder and gravitational-wave detectors) wherever its area law operates. |
| Options B and C | B: a confining field felt by matter must have √σ < 1.4×10⁻³³ eV, which is an ordinary fifth force. C: a running horizon tension adds only a constant 4πcN to S. |

## 2. What stands: one equation for known physics

Details: UNIFICATION.md, CONFINEMENT.md, Z2_GAUGE.md.

```
ln Z_n = (1 − n) · A_H / 4Għ  −  n · σ · A_swept  + …        (rotate by holonomy 2πn)
δS = δ⟨K⟩,   D(ρ‖σ) = Δ⟨K⟩ − ΔS ≥ 0                          (first law of entanglement)
V = ⟨(−1)^ΔN⟩                                               (visibility = parity of quanta)
```

| Sector | Evidence |
|---|---|
| **Horizons:** the 2π holonomy multiplies (1 − n), so A/4G is an entropy | Euclidean Schwarzschild: holonomy = 2.0000000000π; replica entropy = A/4G exactly. |
| **Local thermodynamics:** K = 2π × boost (Bisognano–Wichmann) | Free-fermion lattice: slope 3.14148 against π; first-law slopes 0.39708 vs 0.39745; Clausius ratio 0.99969. |
| **Decoherence:** energy given to the bath = k_BT·D(record‖thermal); Γ_k = 2Var(Q_k)/(ħω_k)² | Exact identities, checked in Fock space to 10⁻⁶. |
| **Visibility = parity of exchanged quanta** | Exact to 7.6×10⁻¹⁷, for any number-diagonal bath. |
| **Confinement:** the string area multiplies n, so it is modular energy, not entropy | Schwinger model (1+1D): ΔS saturates while Δ⟨K⟩ grows as ℓ². Z₂ gauge-Higgs (2+1D): the full string energy enters K (weights c_s = 3.0–3.9 vs c_q ≈ 2.1). Static charges are superselection sectors (D = ∞). |
| **Running horizon tension** | 1/4G(μ) = 1/4G₀ + 0.0242 N μ² per scalar (Srednicki coefficient 0.3046). |

**Status:** every ingredient is published physics; the combined statement and the lattice
tests are this project's. Literature searches found nothing identical, which is not proof
of novelty. Open: whether quark and string get equal weights in a continuum-like limit.
This was inconclusive at exact-diagonalization scale and needs DMRG.

## 3. The unifying-equation search, front by front

Details: UNIFYING_SEARCH.md.

| # | Question | Result |
|---|---|---|
| 1 | Dark energy from holography | Li holographic dark energy has wₐ > 0 for every c. DESI DR2 prefers wₐ ≈ −0.9. Wrong direction. |
| 2 | Running vacuum | Our own bridge: δG/G = 10⁻¹²³. The running vacuum has the right sign but needs ν ≈ 0.13; the CMB allows ≲ 4.8×10⁻⁴, about 0.2% of the DESI signal. |
| 3 | A quark as a folded, twisted area | J = qΦ/4π verified to 10⁻¹²: a full twist gives spin ½. But a ⅓ twist gives J = 1/6; baryons would be monopoles; colour symmetry breaks; masses need 6×10⁻⁹ tuning. |
| 4 | One twist for spin ½ and the thirds | None in the Standard Model's group (mismatch 2.0). With gauged B−L, (−1)^F = exp(3πi(B−L)). The minimal combined fold gives quarks and leptons exactly J = ½, which is the grand-unified-monopole structure. |
| 5 | Why three colours | Witten's anomaly and the twist both require N_c odd. Anomalies fix the charges, not N_c: Q_u = (N_c + 1)/2N_c. π⁰ → γγ is blind to N_c. The R-ratio picks 3 (−1.0σ; 5 is +33σ). |
| 6 | Why three generations | 3-3-1 anomaly plus QCD asymptotic freedom gives N_g = N_c. The minimal β = −√3 model is excluded (its sin²θ_W = ¼ wall at 3.68 TeV vs Z′ > 5 TeV). |
| 7 | Running selects N_c = N_g = 3 | SU(3)_L perturbativity removes N_c ≥ 7; U(1) running removes N_c = 5. |
| 7b | Firmed up | Two-loop machinery reproduces *all* Standard Model coefficients. All anomalies vanish for general N_c. Blow-up: N_c = 3 at 3.0×10²⁹ GeV (above M_Pl), N_c = 5 at 1.3×10¹⁵, N_c = 7 at 9.7×10⁹. Margins +6.1 / −4.6. |
| 7c | The other variant (β = +1/√3) | N_c = 3 at 4.0×10¹⁹ GeV (narrowly above M_Pl), N_c = 5 at 5.5×10¹¹. Robust under every reasonable criterion. |
| 8 | Masses: Koide's formula | Q = 2/3 at −0.43σ (m_τ = 1776.93 ± 0.09). "δ = 2/9" is excluded at 447σ once Koide is assumed exact. Quarks show no relation. Nothing derived gives √2. |
| 9 | Why no numbers? | Planck-scale stability needs m_H ≥ 133 GeV at one loop (~129.5 at NNLO, recalled) vs 125.2. Consistency gives integers, not numbers. |
| 10 | Planck boundary conditions | λ(M_Pl) = 0 gives m_H ≈ 129.5 (calibrated) vs 125.2. Eichhorn–Held retrodict m_t = 178 / 182 GeV vs 172.6. Near misses of 3–5%. |
| 11 | Does 3-3-1 fix the Higgs? | 13 scalar parameters vs 2. A threshold δ = 0.021 is needed and is ordinary in size, so 3-3-1 accommodates rather than predicts. |
| 12 | Gauge unification in 3-3-1 | SU(3)_C and SU(3)_L never meet: the gap grows from 18.6 to 27.3. Meeting would need 14–18 extra triplets. |

## 4. The main positive result, with its conditions

**Chain:**
1. Witten's global anomaly requires N_c odd.
2. The 3-3-1 SU(3)_L anomaly plus QCD asymptotic freedom gives N_g = N_c.
3. Perturbativity of SU(3)_L up to the Planck scale removes N_c ≥ 7.
4. Perturbativity of U(1)_X up to the Planck scale removes N_c = 5.

That leaves **N_c = N_g = 3**, and anomaly cancellation then gives **Q_u = ⅔,
Q_d = −⅓**.

**Robustness checks passed:**
- exact charges and full scalar content for general N_c;
- two-loop running with calibrated machinery;
- 3-3-1 breaking scales from 2 to 30 TeV;
- three perturbativity criteria;
- both viable β variants.

**Conditional on:**
1. **The 3-3-1 framework.** The β = ±1/√3 models predict a Z′ above 3.6–4.2 TeV and
   bilepton gauge bosons, so collider searches decide it.
2. **The assumption** of no Landau pole below the Planck scale. It's standard, not a
   theorem; a pole there would signal new physics, not inconsistency.
3. **The measured electroweak couplings at the TeV scale**, which are an input, not a
   prediction (front 7d).
   - β = +1/√3: N_c = 5 fails for every weak mixing angle, while N_c = 3 needs
     sin²θ_W(4 TeV) < 0.266 (measured 0.250).
   - β = −1/√3: N_c = 3 is safe up to 0.449, but N_c = 5 would survive in a narrow band
     about three times below the measured angle.
   - Two-loop Yukawa terms are now included. They can't rescue N_c = 5, even held
     constant at 6.
   - One-loop threshold matching at the 3-3-1 scale is now included (front 7e). Across
     the heavy spectrum the β = +1/√3 worst case sits 1.64× above M_Pl, and the
     sin²θ_W margin is +0.010 to +0.035.
   - Witten's anomaly is redundant in 3-3-1 (front 7f).
   - The selection holds with no Yukawas, and for any cutoff from 7.2×10¹⁵ to
     1.4×10¹⁹ GeV.
   - The scalar sector itself survives to M_Pl in a corner that requires exotic quarks
     below 1.4–1.8 M_V (front 7g).
   - The thread has reached its walls (WALL.md).

**Standalone write-up:** [NOTE_331.md](NOTE_331.md). Its three weak spots (Yukawas, the
boundary condition, the narrow variant) are computed in front 7d and summarized in
[CONSISTENCY.md](CONSISTENCY.md).

**Novelty:** N_g = N_c from 3-3-1 is KNOWN (Frampton; Pisano–Pleitez). Extending the
chain to fix N_c itself, through N_c-dependent charges and Landau poles, is this
project's step. Searches found no prior derivation, which is not proof there isn't one.

## 5. Why the numbers don't come

- **Consistency produces integers.** Anomalies, topology and perturbativity fix discrete
  data (N_c, N_g, charges, spin, statistics).
- **Continuous parameters need dynamics plus a boundary condition or a symmetry,** and
  the unified equation contains neither.
- **The best known mechanisms land close but miss.** Asymptotic-safety boundary
  conditions at the Planck scale give m_H ≈ 129–132 GeV and m_t ≈ 178–182 GeV,
  against 125.2 and 172.6.
- **There's a trade-off.** The 3-3-1 structure that fixes "3" adds 11 scalar parameters
  (front 11) and blocks gauge unification (front 12), so it trades predictive power on
  the numbers for success on the integers.

## 6. Walls, and what would move each

| Wall | Kind | What would move it |
|---|---|---|
| Option A's corner at Earth-scale ξ (Γ ≈ 2×10⁻³) | data | the published LIGO acceleration spectrum (arXiv is now reachable from the new environment) |
| Equal quark and string weights in the continuum | compute | DMRG at large system size (would confirm a theorem) |
| Masses: Koide's √2 | new structure | a flavour symmetry with a Z₃ circulant mass matrix, compatible with running |
| Higgs and top from the Planck scale | new physics | better quantum-gravity computations of the gravity terms f_g and f_y |
| Dark energy crossing w = −1 | new structure | a dynamical field active only late; or the DESI signal fading |
| Unification | new structure | ad hoc extra matter, which would also force a redo of front 7 |
| Testing the "3 = 3" chain | experiment | a Z′ or bilepton discovery, or exclusion, at the LHC and future colliders |

## 7. Corrections made along the way

Errors caught by the checks and fixed, recorded for transparency:
1. **Skyrme moment of inertia** was 3% low (a hard cutoff); a boundary-value solve with
   the 1/r² tail fixed it.
2. **Lattice modular slope:** nearest-neighbour terms alone gave 3.37; the longer-range
   hoppings had to be included.
3. **First-law test:** the perturbation chosen first had zero first-order change.
4. **Modular Hamiltonian precision:** taking K from the reduced density matrix lost
   precision; an SVD fixed it.
5. **Static Z₂ charges** turned out to be superselection sectors, which required heavy
   dynamical charges instead.
6. **Two-loop machinery:** a normalization bug and the scalar factor, both caught by the
   Standard Model calibration.
7. **Koide phase:** the generation-relabelling branch, plus the joint test that excludes
   δ = 2/9.
8. **Eichhorn–Held relation:** applied at M_Pl instead of at the transplanckian fixed
   point; withdrawn after reading the paper.
9. **Smarr check:** circular (the user's correction).
10. **Statistical-gravity heating:** the point-nucleus formula gave 10⁵⁶–10⁶⁰ W/kg at the
    entanglement cutoff. Real nuclei are about 1 fm across, so the figure is 0.5 W/kg.
    That is still 6×10¹⁰ times the Earth's heat flow (OPPENHEIM.md P4).
11. **D6 overstated:** "gravity follows each branch" had been presented as derived
    outright. It is derived only under R₀ = a and Markovian dynamics, and λ = 1 is also
    perturbative quantum gravity's prediction (DERIVATION.md, COLLECTIVE.md).
12. **Gas-collision rate:** the interpolated formula was 4.19× too high; it is now derived
    (RECHECK.md). Design A needs 270 runs, not 565.
13. **Every failed claim rechecked** by independent code: 15 of 15 confirmed. Front 9's
    one-loop Higgs bound is 133.1–134.3 GeV, depending on the top-mass matching.

## 8. Housekeeping

- **Public files.** The home page is now the quantum-level-up theory; the original
  resistance-equation page is in `archive/resistance-equation/`. The PDF derivation
  record belongs to that original page.
- **Network.** A personal environment "STUR-Physics-Lab" was created during the work to
  allow `arxiv.org` and `ar5iv.labs.arxiv.org`. Its setup script installs the Python
  requirements; it's unproven until a fresh session starts on it.
- **Reproduce:**
  1. `pip install -r requirements.txt pytest matplotlib`
  2. `python -m pytest tests -q` (121 tests)
  3. run any `src/*.py` to regenerate its file in `results/`.
