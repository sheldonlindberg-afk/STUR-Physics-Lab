# Consistency record

*November 2026.* This page replaces the consistency audit that an earlier commit removed.
It records three things:
- what was checked across the current documents;
- what was found and fixed;
- the tensions that remain, which are stated, not resolved.

`tests/test_consistency.py` enforces the mechanical part on every push:
- no superseded claim returns;
- numbers shared between documents match the scripts that compute them;
- document links resolve;
- the stated test count is the real one.

The archive is not checked.

## Fixed in this pass

| # | Where | Inconsistency | Fix |
|---|---|---|---|
| K1 | DERIVATION D6, the site, REPORT | D6 was labelled FOLLOWS ("no new assumption") while depending on R₀ = a and Markovian dynamics | New label **CONDITIONAL**, defined in REPORT and on the site; D6 carries it |
| K2 | DERIVATION D3 vs D6 | Jacobson's step is stated for ⟨T_μν⟩, the semiclassical form, while D6 has each branch source its own field. The two were never reconciled | Stated: D3 is applied inside each branch, with the same entanglement per area and that branch's own T_μν. Labelled an interpretation |
| K3 | GRAVITY_ENTANGLEMENT verdict | Called λ "a free parameter of known physics", while D6 claims λ = 1 | Reconciled. λ = 1 within the theory (CONDITIONAL), open experimentally, and not distinctive. Intermediate λ is marked a phenomenological scale, not a consistent dynamics |
| K4 | DERIVATION D8 | The entanglement reading of G was silent on gauge fields | Added: gauge-field contact terms (Kabat 1995, recalled) make the identification unsettled beyond scalars and fermions |
| K5 | Site D4 card | Residual 10⁻¹⁶⁸, against ≤ 10⁻¹⁶⁵ in the documents | Fixed |
| K6 | README, PREDICTIONS, GRAVITY_ENTANGLEMENT, WALL | Vibration gap "~140×"; 1.7×10⁻¹⁵ / 1.3×10⁻¹⁷ = 131 | ~130× everywhere (later ~57×, with the derived gas rate) |
| K7 | PREDICTIONS item 2 | "Any statistical gravity" where the argument covers only Markovian ones | "Any Markovian statistical gravity" |
| K8 | NOTE_331, REPORT §4 | Two-loop Yukawa terms were missing, and the boundary condition was unquantified | Front 7d computes both (below) |

The previous pass fixed:
- the point-nucleus heating, 10⁵⁶–10⁶⁰ → 0.5 W/kg ([OPPENHEIM.md](OPPENHEIM.md) P4);
- the unconditional D6 headline.

## The three weak spots of the 3-3-1 result, now computed

Source: `src/god_eq_331_yukawa.py`, [NOTE_331.md](NOTE_331.md), front 7d of
[GOD_EQUATION.md](GOD_EQUATION.md).

| Weak spot | Result |
|---|---|
| Two-loop Yukawa terms | The coefficient formula reproduces the SM top's (17/10, 3/2, 2) exactly. With every Yukawa held constant (overstating it), poles rise by at most about 5×. No constant y_J ≤ 6 rescues N_c = 5. **Closed.** |
| Boundary condition | It is the measured electroweak couplings at 4 TeV. β = +1/√3: N_c = 5 fails at every weak angle. β = −1/√3: N_c = 5 survives only for 0.066 < sin²θ_W < 0.074, about 3.4× below the measured 0.2504. At our angle, N_c = 5 would need α_em 1.33× (β = −1/√3) or 1.86× (β = +1/√3) weaker. **Quantified.** The selection takes the couplings as input and doesn't predict them. |
| The narrow β = +1/√3 margin | One-loop threshold matching (front 7e) passes a matching-scale-independence check to 10⁻⁹. Across the heavy spectrum, the N_c = 3 pole sits ≥ 1.64× above M_Pl (≥ 2.23× with the Z′ above LHC limits), and N_c = 5 stays ≤ 3.8×10¹² GeV. The sin²θ_W margin is +0.010 to +0.035. **Survives; still the tightest number.** |

## Further closures (fronts 7f–7g)

| Assumption | Result |
|---|---|
| Witten's anomaly (step 1) | Redundant in 3-3-1: the SU(3)_L anomaly plus asymptotic freedom alone force N_c odd and N_g = N_c |
| The Yukawas' own running | Irrelevant to the verdict: the selection holds with no Yukawas at all (worst case 1.53 M_Pl) |
| "The Planck scale" | Any cutoff from 7.2×10¹⁵ to 1.4×10¹⁹ GeV works, under g = 4π or α = 1 |
| The scalar sector's own perturbativity | 3-3-1 at N_c = 3 survives to M_Pl, perturbative and bounded below, in a corner: exotic quarks < 1.79 M_V (β = −1/√3) or < 1.40 M_V (β = +1/√3), quartics ≲ 0.37, c² ≥ 0.68. The extra scalars cure the SM's instability there |

## Tensions that remain

1. **D6 rests on an identification.** R₀ = a is natural in the framework, but it isn't
   forced. Jacobson's local horizons are coarse-grained on patches much larger than a,
   which would favour a larger R₀. The one-diamond test (R₀ up to 455 µm) and the
   Oppenheim product bound (up to 100 µm) cover what the identification doesn't.
   Non-Markovian classical gravity is covered by neither.
2. **λ = 1 isn't distinctive.** It is perturbative quantum gravity's prediction too. No
   current prediction distinguishes this framework from standard physics. Its candidate
   new results are:
   - the identity −ln V = 2 Var(ΔN);
   - the 3-3-1 selection, the principal one.

   The Oppenheim-type bounds are worked examples within an existing systematic
   literature (NOVELTY.md).
3. **G isn't predicted.** c_s = 0.3046 depends on the regulator, only a²/N is fixed, and
   gauge fields are unsettled (K4).
4. **The Born rule's envariance route** assumes probabilities exist and depend only on the
   state (Schlosshauer–Fine). The additivity and no-signalling routes don't.
4b. **The 3-3-1 selection now hits three walls.** Computation can't move them:
   - *Conceptual:* it takes the measured TeV-scale couplings as input and can't predict
     them. Any statement about other N_c needs a choice of their couplings.
   - *Data:* the 3-3-1 framework (Z′ at 1.225 M_V, bileptons, exotic quarks below about
     1.1–1.5 M_Z′) must be found or excluded at colliders.
   - *Refinement:* two-loop quartic RGEs and one-loop Higgs matching would only reshape
     the surviving corner.
5. **The two threads are independent.** Nothing in the measurement–gravity equation
   selects 3-3-1, and nothing in the 3-3-1 chain uses the equation. They share a
   repository and a method, not a derivation. Presenting them as one theory would be
   inconsistent.
6. **Scope of the classical-gravity bounds.**
   - P3 covers continuous, translation-invariant models.
   - P5 ([OPPENHEIM.md](OPPENHEIM.md)) applies Oppenheim et al.'s own kernel-free trade-off
     (their appendix B.4). It covers every Markovian CQ
     model, discrete (jump) ones included, for splits of order the particle's radius:
     Γ·S_a ≥ (F_LR/M)²/8.
   - Discrete models are therefore testable, not excluded. Non-Markovian classical
     gravity remains uncovered: that is where the gravity thread's theory wall is.
7. **The gas-collision rate is now derived, no longer estimated.** It is the collision
   rate n⟨v⟩·2πR², with the hard-sphere cross-section checked by partial waves. The old
   interpolation was 4.19× too high. Design A now needs 270 runs (was 565), and helium
   as the leftover gas is no longer fatal. A 10× worse vacuum still is.

## Reproduce

```bash
python -m pytest tests/test_consistency.py -q     # the mechanical checks
python -m pytest tests -q                         # everything (121 tests)
```
