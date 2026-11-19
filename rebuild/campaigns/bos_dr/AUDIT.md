# Red-team audit: bos_dr (bosonic one-loop on-shell Δr of muon decay; 't Hooft-Feynman gauge, massless leptons)

The auditor's scratch work is in `/tmp/claude-0/-home-user-STUR-Physics-Lab/6f003c51-fc14-5da0-833a-45f53d6397be/scratchpad/audit-bos_dr/`:
* `indep.py` is the independent symbolic derivation of δ_V, the Fermi subtraction and the Ward identity.
* `work/assemble.py` is my own assembly of Δr_bos, using the provided `bos_se` and my δ_V.
* `make_mutants.py` and `mutants/` hold the 23 mutants. Each mutant directory has its own `gate.log`, and the survivors also have a `checks.log`.
* `checks_build_{a,b}.log` are the runs of the proposed checks on the two builds.

I read and ran the code of both builds and the reference. The independent route in section 1 uses none of the builds' code and none of the reference's formulas. The reference is used only as the comparison target, and the provided stage-1 module `bos_se` only for the Σ's.

Classes: **B** = defect in a build. **R** = SPEC ambiguity (a correct build could resolve it differently). **C** = oracle/check gap. **N** = note or positive result.

## 1. Independent verification (task 1)

### (a) δ_V from the diagrams, exact d

**Machinery.** I wrote my own d-dimensional γ-string contractor ({γ^a, γ^b} = 2g^{ab}, g^a_a = d), using NDR (γ5 moved to the end of each massless chain). The O(ε)×pole terms are kept: c(d)·B0 → c(4)(Δ + fin) − 2c′(4).

**Fermi coefficients.** The box Fierz coefficients come from explicit 4×4 Dirac matrices: γ^αγ^σγ^ρP_L ⊗ γ_αγ_σγ_ρP_L = **16**·Γ and the reversed order = **4**·Γ. The boxes are UV finite, so using d = 4 there is legitimate.

**Feynman rules (my own, from SPEC §1).**
* The lepton vertex is iγ^μP_L G^X, with G^{W1,2} = gT^{1,2}, G^Z = (g/c)(T3 − s²Q) and G^A = eQ.
* The triple vertex is g ε^{abc}[g^{μν}(k1−k2)^ρ + …], with all momenta incoming. Replacing W3 = cZ + sA gives κ_Z = c and κ_A = s.

**Pieces, per W vertex, in units of 1/16π²:**

| Piece | Coefficient |
|---|---|
| abelian Z exchange | (d−2)²/d · B0(0;0,M_Z) · g_ν g_ℓ |
| non-abelian vertex | 4(d−1)/d · g² [c² B0(0;M_W,M_Z) + s² B0(0;M_W,λ)] |
| W exchange around the W vertex | cancels in the sum over a (no such charge flow) |
| photon exchange | absent: the neutrino is neutral |
| lepton self-energy | Σ_L = −(d−2)²/d · Σ_X G_X² B0(0;0,M_X), with ½Σ_L per external leg |

**Boxes.**
* I derived the internal-momentum signs s1s2 = (+, −, −, +) myself from the momentum routing, for V on (μ,e), (μ,ν_e), (ν_μ,e) and (ν_μ,ν_e).
* The tree amplitude is −i g²/(2M_W²) Γ.
* The result is δ_box = −(M_W²/16π²) Σ g1g2 s1s2 (C/4) J, with J = −ln(M_W²/M_V²)/(M_W² − M_V²). I checked the normalisation of J in the limit M_V → M_W against the Euclidean integral.

**Result.**

    δ_V = (g²/16π²)[4Δ + 6 + L_W(−6 + 7/(2s²)) + L_Z(2 − 7/(2s²))]

This is the claimed expression, confirmed: the symbolic difference is exactly 0.

Pole bookkeeping in units of g²Δ:

| Term | Pole |
|---|---|
| 2 × abelian | −1 + 1/(2c²) |
| 2 × non-abelian | +6 |
| LSZ | −1 − 1/(2c²) |
| boxes | 0 |
| **total** | **4** |

The total of 4 is 2C_A per vertex, consistent with Z_1F/Z_2.

**N1.** Independently, the Z-box combination is g_ℓ² − 8g_ℓg_ν + g_ν², and the photon box is +e² ln(M_W²/λ²). Both builds have these.

### (b) IR cancellation and the Fermi subtraction

**IR.** The coefficient of ln λ² in δ_V is exactly 0. The photon parts of the μ and e LSZ factors give +e² ln λ², and the W-γ box gives −e² ln λ². The W-γ vertex triangle B0(0;M_W,λ) is IR finite.

**Fermi theory, zero momentum, photon mass λ:**
* **Charge-retention order** [ēγP_Lμ][ν̄γP_Lν]: vertex + LSZ = **0** identically (abelian Ward identity, any λ).
* **Charge-exchange order** with 4D numerators (the photon "box" without the W gives +e²B0(0;0,λ) with C/4 = 1, and the LSZ gives −e²B0): also **0**. The ordering is irrelevant as long as the Fermi theory is treated consistently in 4D, or Fierz-covariantly.
* **Charge-exchange order with mixed schemes** (4D exchange diagram but CDR LSZ): the result is UV divergent and has a scheme constant. Only this inconsistent treatment differs.

**N2.** The claim "the Fermi QED correction vanishes at zero momentum in charge-retention order" is right. The argument that the subtraction removes nothing from the p = 0 amplitude is also right: SM(p) − Fermi(p) is IR safe and dominated by loop momenta of order M_W, so it may be evaluated at p = 0, where Fermi(0) = 0.

**R2 (minor).** The SPEC does not name the Fierz ordering or the scheme for the Fermi-theory subtraction. The standard choice (charge retention, UV finite) is the one that gives Denner's δ_VB. Build a flagged this in its QUESTIONS 1. **Fix:** add "(in the charge-retention, i.e. Fierz-rearranged, form, in which its O(α) correction is UV finite)".

### (c) Ward identity and δe/e

**Right-handed electron.** Only γ and Z exchanges contribute (no W), and vertex + LSZ = 0. This gives

    e = e0[1 − Σ′_AA(0)/2 − (s/c) Σ_AZ(0)/M_Z²]

Build a's derivation is confirmed. Signs:
* The mixing propagator is (Γ⁻¹)_AZ → +Σ_AZ(0)/(M_Z² k²), from SPEC's +Σ_AZ in the inverse matrix.
* The charge part of G^Z_R is −(g/c)s²Q.

**Left-handed electron.** The extra pieces are:
* the non-abelian triangle with an external A and internal W1, W2: κ_A = s, ε^{3xy}
* the W part of the LSZ factor
* the abelian W exchange, which needs an internal ν and so gives 0

Universality with the right-handed coupling requires

    Σ_AZ(0) = (α/4π)(2M_W²/(sc)) ln(M_W²/μ²)

with no constant term. The provided `bos_se.sigma_AZ(0)` equals this to ≤ 3·10⁻¹³ absolute at 7 points × 3 values of μ. Neutrino neutrality also holds exactly: NA triangle + abelian W exchange + g_ν Σ_AZ = 0.

**N3.** Build b's assumption, that the T3 part of the γ-Z mixing cancels the non-universal photon-lepton vertex, is therefore correct. The check is also a CDR-scheme consistency test between the vertex constants and stage 1: the −½ O(ε) terms cancel in this combination in CDR, whereas in DRED a constant of 1 would survive.

### (d) The decomposition

**My derivation.** I worked from the bare-parameter amplitude:
* the W propagator at k = 0 is i/(M_W0² − Σ_W(0)), with M_W0² = M_W² + Σ_W(M_W²)
* M_Z0² = M_Z² + Σ_ZZ(M_Z²)
* g0² = e0²/s0², with s0² = s²[1 + (c²/s²)(Σ_ZZ/M_Z² − Σ_W/M_W²)]
* e0 comes from (c)

This gives

    Δr_bos = Σ′_AA(0) + 2(s/c)Σ_AZ(0)/M_Z² − (c²/s²)[Σ_ZZ(M_Z²)/M_Z² − Σ_W(M_W²)/M_W²] + [Σ_W(0) − Σ_W(M_W²)]/M_W² + δ_V(μ)

This is the stated decomposition, confirmed.

**Further checks of the decomposition:**
* Tadpoles cancel in it: Σ^tad_W/M_W² = Σ^tad_Z/M_Z².
* No W-field or lepton counterterm is needed beyond LSZ.
* The equivalence with Denner's grouping is δ_vb = δ_V(μ) + 2Σ_AZ(0;μ)/(sc M_Z²) = (α/4πs²)[6 + (7 − 4s²)/(2s²) ln c²], which is μ independent. The algebra closes exactly.

**Numerical check (`work/assemble.py`).** I combined my δ_V with the provided Σ's (Σ′_AA from a Richardson-extrapolated forward quotient):
* At the 5 oracle points plus M_W = 40 and M_W = 90 GeV, at μ = M_W, 13 and 700 GeV, the result agrees with the reference to ≤ 1·10⁻¹⁴ relative.
* At M_W = 90 the agreement is 5·10⁻¹³. That point is near the zero of Δr_bos, where doubles lose digits.

**N4.** Δr_bos and δ_vb are independently confirmed, and so is the oracle's reference.

### (e) SPEC: the δ_vb definition

**R1.** "The on-shell W-ℓ-ν coupling counterterm *not* included" describes the unrenormalised sum δ_V. That sum is UV divergent (pole 4g²/16π²) and μ dependent in MS-bar, so it is not a number, and it contradicts the export signature, which takes no μ and depends on s² only.

Both builds resolved this the same way, by exporting Denner's δ_VB:
* build a: δ_V^{MS-bar}(μ = M_W)
* build b: δ_V + 2Σ_AZ(0)/(sc M_Z²)

The two coincide only because the Feynman-gauge bosonic Σ_AZ(0) ∝ B0(0;M_W,M_W) vanishes at μ = M_W. The oracle pins exactly this. A different but legitimate resolution, such as δ_V at μ = M_Z or "δ_V + all counterterms", would fail `vb_check` while Δr_bos is right (compare mutants M10 and M18).

**Fix:** "delta_vb := δ_V^{MS-bar}(μ) + 2Σ_AZ(0;μ)/(s c M_Z²) (SPEC photon sign), the μ-independent grouping in which Δr_bos = Σ′_AA(0) − 2(c/s)Σ_AZ(0)/M_Z² − … + delta_vb".

### What I could not verify

* The bosonic Σ's themselves are taken from stage 1 (audited there).
* The finite constants of the Z boxes, meaning the signs s1s2 and the 16/4 assignment, are checked only by my own derivation together with agreement with Denner's printed formula, which is also the textbook Sirlin/Hollik δ_VB. μ independence and IR cancellation do not test them.
* I did not do an R_ξ calculation, so gauge independence is unverified.

## 2. Findings

| # | Class | Finding |
|---|---|---|
| R1 | R | The δ_vb definition in SPEC §4 is literally a UV-divergent, μ-dependent quantity. The oracle pins Denner's grouping. Fix wording as in 1(e). |
| R2 | R (minor) | The Fierz ordering and scheme of the subtracted Fermi-theory QED correction are unstated. They are harmless if the theory is treated consistently (1b). |
| C1 | C | **Coverage gaps.** The oracle samples s² only in [0.13, 0.51] (5 points), α only in [1/132, 1/125] (the physical Thomson α = 1/137.036 is never tested), and M_H at 9 fixed points. Mutants M11, M11b, M12, M13 and M20 are genuinely wrong and pass the gate. |
| C2 | C | `total_check` is purely relative, but Δr_bos(M_H = 125) changes sign near M_W/M_Z ≈ 0.975. The current points avoid it, but any point added near there would be over-strict. The proposed `dr_far_s2` uses the floor α/4π. |
| C3 | N | **Equivalent mutant M04b.** Flipping the sign of the Σ_AZ(0) term while assembling at μ = M_W changes nothing, because Σ_AZ(0; M_W) = 0. Both builds assemble at μ = M_W, so the sign of their Σ_AZ coefficient is checked only by their μ-scan second routes. Build a is checked at μ = 10–2000 GeV, and build b at μ = 30 and 500 GeV. I confirmed the sign independently. No export-level check can do this. |
| C4 | N | The oracle docstring calls delta_VB "the textbook vertex + box + wave-function term". Strictly, it is δ_V plus the mixing piece 2Σ_AZ(0)/(sc M_Z²), and equal to δ_V only at μ = M_W (R1). |
| N1–N4 | N | See section 1: δ_V, the IR cancellation, the Fermi subtraction, the Ward identity, δe/e and the decomposition are all confirmed independently. |
| B | – | No build defects found. Both builds pass all six proposed checks. |

## 3. Mutants (task 2)

**Setup.** All mutants are build b plus an override block appended before `__main__`. Each directory has `bos_se.py`, `DERIVATION.md` and `QUESTIONS.md`. Each was run with `python3 gate.py --mode verifier --campaign bos_dr --oracle bos_dr/oracle.py <dir>` from `rebuild/campaigns`. Unmodified build b passes in about 3 minutes.

Oracle labels in the "Killed by" column:
* **tot**: the five-point Δr_bos check
* **vb**: the δ_vb check
* **MH**: the M_H scan
* **prec**: the build's own precision check

| Mutant | Error | Gate | Killed by | Proposed check that kills it |
|---|---|---|---|---|
| M01 | box −8g_ℓg_ν → −6 | FAIL | tot, vb, MH, prec | – |
| M02 | W-γ box dropped | FAIL | tot, vb, MH, prec | – |
| M03 | Fierz 16↔4 swapped in the WZ boxes | FAIL | tot, vb, MH, prec | – |
| M04 | sign of the Σ_AZ(0) term flipped, assembled at μ = M_Z | FAIL | tot, MH, prec | – |
| M04b | the same at μ = M_W (**equivalent mutant**) | PASS | – | none possible (C3) |
| M05 | −(c²/s²)[…] → −(1/s²)[…] | FAIL | blind slope, tot, MH, prec | – |
| M06 | Σ′_AA(0) → Σ_AA(M_Z²)/M_Z² | FAIL | tot, MH, prec | – |
| M06b | Σ′_AA(0) by a one-sided step, h = 10⁻⁴ M_W² | FAIL | tot, MH, prec | – |
| M07 | constant 6 → 5.5 | FAIL | tot, vb, MH, prec | – |
| M08 | 7 → 6.5 in the ln c² coefficient | FAIL | tot, vb, MH, prec | – |
| M09 | δ_vb: ln c² → ln s² | FAIL | vb | `split_consistency` also |
| M10 | δ_vb = δ_V(μ = M_Z) (μ dependence left in) | FAIL | vb | `split_consistency` also |
| **M11** | Δr_bos × (1 + 10⁻⁴) only for 2·10³ < M_H < 4·10³ GeV | **PASS** | – | `dense_higgs_mass` |
| **M11b** | Δr_bos × (1 + 10⁻³) only for 2·10¹⁰ < M_H < 8·10¹² GeV | **PASS** | – | `dense_higgs_mass` |
| **M12** | δ_V constant 6 → 5 only for s² < 0.1 (both exports) | **PASS** | – | `vb_s2_sweep`, `dr_far_s2` |
| **M13** | both exports × (1 + 10⁻³) only for α < 1/133 (the Thomson α) | **PASS** | – | `alpha_linear_wide` (BLIND-OK), `thomson_alpha_reference`, `split_consistency` |
| M14 | O(ε)·pole (−½) dropped in the 3 NA vertices (DRED-like) | FAIL | tot, vb, MH, prec | – |
| M15 | neutrino wave function dropped | FAIL | tot, vb, MH, prec | – |
| M16 | W-γ box with ln(M_Z²/λ²) | FAIL | tot, vb, MH, prec | – |
| M17 | Σ_W(0) term dropped | FAIL | blind slope, tot, MH, prec | – |
| M18 | δ_vb regrouped with Σ_AZ at the wrong scale (Δr_bos right) | FAIL | vb | `split_consistency` also |
| M19 | control: Δr_bos × (1 + 3·10⁻⁹) | FAIL | tot | – |
| **M20** | Σ_W(0) × 1.01 only for M_W/M_Z > 0.95 | **PASS** | – | `dr_far_s2` |

**Results.**
* 6 of the 23 mutants survive the gate. Five of them (M11, M11b, M12, M13, M20) are genuinely wrong, and all five are killed by the checks in `audit_proposed_checks.py`. The sixth survivor, M04b, is equivalent to the correct build. The `checks.log` files show that M04b passes all six proposed checks, as it must.
* No mutant failed the blind tier except M05 and M17 (the large-M_H slope check).

**Proposed checks** (`rebuild/campaigns/bos_dr/audit_proposed_checks.py`; run with `python3 audit_proposed_checks.py <build dir>`):
* `alpha_linear_wide` (BLIND-OK)
* `split_consistency` (no reference; uses the provided bos_se and pins the R1 resolution)
* `thomson_alpha_reference`
* `vb_s2_sweep`
* `dr_far_s2`
* `dense_higgs_mass`

Both builds pass all six:

| Check | Build a | Build b |
|---|---|---|
| worst deviation | 1.1·10⁻¹³ | 5·10⁻¹⁴ |
| where | `dr_far_s2` at M_W = 89.5 GeV | – |

Running all six checks takes about 3 minutes per build.

## 4. Verdict

**Build a: PASS.**
* Its derivation is the most complete: an automated d-dimensional engine, and an explicit derivation of δe/e from the right-handed electron.
* Its Ward-identity prediction of Σ_AZ(0) is confirmed independently.
* Its QUESTIONS correctly flag R1 and R2.
* No defects.

**Build b: PASS.**
* Its diagram values are correct and match mine term by term.
* It took the Ward-identity step (T3 part of the mixing cancelling against the non-universal vertex) as given. That step is correct (section 1c), and the build labelled it honestly as "not derived".
* No defects.

Both builds' δ_vb is the oracle's grouping, which is a legitimate, and the most natural, resolution of the ambiguous SPEC §4. The physics target is confirmed by a route independent of both builds and of the reference transcription:
* Δr_bos
* δ_V = (g²/16π²)[4Δ + 6 + L_W(−6 + 7/(2s²)) + L_Z(2 − 7/(2s²))]
* δ_VB = (α/4πs²)[6 + (7 − 4s²)/(2s²) ln c²]
