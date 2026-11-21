# AUDIT: campaign higgs_dr_xi (ξ dependence of the Higgs part of Sirlin's Δr in R_ξ gauge), builds a and b

Auditor (red team). In the repository I wrote only this file and `audit_proposed_checks.py`. Everything else ran on copies
in the scratch directory `AUD = /tmp/claude-0/-home-user-STUR-Physics-Lab/6f003c51-fc14-5da0-833a-45f53d6397be/scratchpad/audit-higgs_dr_xi`.
`copies/{a,b}` hold the builds, `mutants/` holds the mutants, and the scripts and their `*_out.txt` outputs sit next to them.
Builds: `.../scratchpad/verify-higgs_dr_xi-a` and `.../scratchpad/verify-higgs_dr_xi-b`.

## 0. Bottom line

* **The campaign's claim is TRUE. There is no class-C physics finding.** I checked it with my own Feynman rules, the
  unsplit R_ξ propagator and no partial fractions. The g^{μν} coefficient of the sum of the Higgs-containing 1PI diagrams
  (H–V bubble, H–Goldstone bubble, HH seagull, tadpoles excluded as SPEC §2 requires) does not depend on ξ, for every
  ξ ≥ 0 and every q² below the physical threshold. The cancellation already holds in the integrand, at each k:
  d/dξ of the transverse trace of (H–V + H–Goldstone) is **identically 0** (sympy). The cancellation is between diagrams.
  Each diagram on its own depends strongly on ξ: at m_H = 125.2 GeV and q² = M_W², the H–V g-part goes from 2851 to
  80990 (units g²/16π²) as ξ goes from 0 to 25. The H–Goldstone part moves the opposite way, and the sum stays fixed at
  5223.6901416868 in all 15 digits.
* **Numerical confirmation by two routes that share no code with the builds.**
  * Route 1: exact-d Feynman-parameter tensor integrals of the unsplit diagrams, with the −i0 prescription. Against
    reference_dr.pi_v, the error is ≤ 5e-25 over ξ = 0, 0.3, 1, 4, 25; q² = −3M_W², 0, M_W²/2, M_W², M_Z² and
    0.95(m_H+M)²; m_H = 10…1500 GeV; W and Z.
  * Route 2: a 4D Euclidean momentum integral (no Feynman parameters, no dim reg) of the UV-finite ξ-dependent part of
    **each diagram separately**. It agrees with route 1 to ≤ 1e-13.
  * Δr_rel from my own self-energies matches the reference to ≤ 6e-24 at every ξ.
  * The heavy-Higgs slope is ξ independent and equal to 11α/(48πs²).
* **Where the ξ dependence lives** (both builds claim this but compute neither piece). I computed both explicitly
  (`indep_xi_out.txt`): the q^μq^ν coefficient Π^L and the Higgs-containing W–φ mixing.
  * Π^L at m_H = 300 GeV and q² = M_W² is −0.117 at ξ = 0, −0.138 at ξ = 1 and −0.084 at ξ = 25.
  * The W–φ mixing coefficient is 262 at ξ = 0, 204 at ξ = 1 and −101 at ξ = 25.
  * Neither enters Δr. Both are proportional to q^μ, so they drop out of the transverse pole, and they vanish against the
    massless, conserved lepton currents (§3).
* **Gate:** 8 of 16 mutants (plus the control M00) survive the full verifier gate.
  * Two survivors are physically correct and must pass:
    * M01 ignores ξ entirely.
    * M03 uses a wrong Goldstone mass consistently in both ξ pieces, so the error cancels.
  * Six survivors are genuinely wrong: M07, M08, M09, M10, M14 and M15.
  * The three blind checks in `audit_proposed_checks.py` kill every wrong survivor. They pass both builds, M00, M01 and M03.
* **Verdict: accept build a and build b** (§6). Neither has a physics error. Build b slightly overstates its numerical
  evidence (B1). The gate cannot tell a ξ-ignoring build from a correct one, so the evidence for ξ independence is §2,
  not the gate (C1).

## 1. Feynman rules (`rules_and_integrands.py` → `rules_out.txt`)

I expanded |DΦ|² from SPEC §1 in sympy. Vector fields and scalar derivatives are commuting "μ-objects", and a product of
two of them is a contraction.

| term in L | coefficient | vertex (incoming momenta) |
|---|---|---|
| H W⁺W⁻ | g²v/2 = g M_W | i g M_W g^{μν} |
| H Z Z | v(g²+g'²)/4 | i (g/c) M_Z g^{μν} |
| H H W⁺W⁻, H H Z Z | g²/4, (g²+g'²)/8 | i g²/2, i g²/(2c²) |
| W⁺(φ⁻∂H) , W⁺(H∂φ⁻) | +ig/2, −ig/2 | i(g/2)(p_H − p_{φ⁻})^μ (conjugate for W⁻) |
| Z(χ∂H), Z(H∂χ) | −g/(2c), +g/(2c) | (g/2c)(p_χ − p_H)^μ up to the overall phase, product of two = +κ²(2k−q)(2k−q) |
| Z∂χ, W^±∂φ^∓ mixing | M_Z, ∓i g v/2 | cancelled by the 't Hooft gauge fixing −(1/2ξ)(∂V − ξ M_V φ)² (IBP), which also gives the Goldstone mass² ξM_V² |
| H A A, H A Z, A H ∂H | 0 | no Higgs coupling to the photon at this order |
| V(Φ): H φ⁺φ⁻, H χ² | 2λv, λv (λv² = m_H²/2) | −i m_H²/v |
| ghosts | δχ/δα_Z = −(g/2c)(v+H) | H c̄_Z c_Z coefficient ∝ ξ M_Z g/(2c): ghosts couple to H only in proportion to ξ |

The ratio (V–φ–H)/(V–V–H) = 1/(2M_V) is the same for W and Z (sympy: 1/(gv)). This ratio is what makes the
cancellation work in both sectors. These rules agree with both builds' DERIVATION tables, and with the
higgs_dr audit at ξ = 1.

**Ghosts.** Every ghost vertex is c̄ c X, so a ghost line runs around the whole loop. A one-loop V two-point function with
an H line has two internal lines (H plus one other), and there is no V–H–ghost vertex. Ghosts therefore never enter the
Higgs-containing Π_VV. The H c̄c vertex (∝ ξ) enters only the H tadpole and the H self-energy. Both builds state this
correctly.

## 2. Independent derivation and numerics for the ξ-dependent diagrams

### 2.1 Integrand-level identity (no partial fractions)

The two diagrams, with momentum routing k on the V or φ line and q−k on the H line:

* iΠ_a = −g_V²M_V² ∫ [g^{μν} − (1−ξ)k^μk^ν/(k²−ξM²)] / [(k²−M²)((q−k)²−m_H²)]  (full SPEC propagator)
* iΠ_b = +(g_V²/4) ∫ (2k−q)^μ(2k−q)^ν / [(k²−ξM²)((q−k)²−m_H²)]

I projected each onto T = g − qq/q² (trace = (d−1)·Π_g) and onto L = qq/q². The results:

* T·iΠ_a + T·iΠ_b minus its value at ξ = 1 is **exactly 0** as a rational function of (k², k·q, q²).
* d/dξ(T·iΠ_a) = −M²g_V² k_T²/((k²−ξM²)²D_H), which is nonzero. The Goldstone diagram contributes the same term with
  the opposite sign.
* d/dξ(L·iΠ_{a+b}) = M²g_V²(q² − 4k·q)/(4(k²−ξM²)²D_H), which is nonzero. The ξ dependence moves into Π^L.
* d/dξ of the q_μ-contracted W–φ mixing integrand is nonzero.

The cancellation is pointwise, so it holds for every ξ ≥ 0, including ξ = 0. It holds above unphysical thresholds and in
any regulator that keeps the routing. It does not depend on the partial-fraction split that both builds use.

### 2.2 Exact-d Feynman parameters, unsplit, complex logs (`indep_xi.py` → `indep_xi_out.txt`)

The triple denominator D_ξ D_M D_H is parametrised on the simplex. The t-integral is done analytically, because Δ₃ is
linear in t, and the x-integral is done numerically with break points at the zeros of Δ. Logs use ln(Δ − i0). The
master integrals are the d-dimensional ones, with the 1/d against 1/ε kept: the g-part of ∫ll/(l²−Δ)² carries a "+1",
the g-part of ∫ll/(l²−Δ)³ carries none, and ∫l²/(l²−Δ)³ carries −1/2.

* **Π_g against the Feynman-gauge reference:** ≤ 5e-25 at all 5 ξ, 6 q² (including 0.95 of the physical threshold),
  4 m_H, W and Z. The one large entry (0.24) is W at m_H = 10 GeV and q² = M_Z². That point is above the **physical**
  threshold (m_H+M_W)² = 8100 GeV². There my code takes Im with ln(Δ−i0) and the reference takes mpmath's principal
  branch, so the imaginary parts have opposite signs. The real parts agree, and Δr never uses this point.
* **Π^L and the W–φ mixing:** ξ dependent (numbers in §0).
* **Δr_rel from my own Π:** ≤ 6e-24 against reference_dr.dr_h_rel at ξ = 0, 0.3, 1, 4, 25 and m_H = 10, 125.2,
  1000 GeV.

### 2.3 4D Euclidean momentum integral (`euclid4d.py` → `euclid4d_out.txt`)

For each diagram separately I computed F(ξ,Q) = [Π(ξ,q²) − Π(1,q²)] − [Π(ξ,0) − Π(1,0)] at spacelike q (Q² = −q²).
F is UV finite, because the ξ-dependent divergence of each diagram does not depend on q². The g-part is the transverse
trace divided by 3, written as k²sin²θ. The θ integral uses Simpson's rule, and the k integral is mapped onto [0,1].

* Comparison with §2.2 per diagram: 144 points (M = M_W, M_Z; m_H = 50, 125.2, 400; Q = 40, 120, 300; ξ = 0, 0.3, 4, 25;
  a and b). Worst deviation 9.6e-14. Example: Z, m_H = 400, Q = 300, ξ = 25 gives F_a = +38.746072581 and
  F_b = −38.746072581.
* This confirms that each diagram is evaluated correctly in its own right, and that the two pieces cancel exactly.

### 2.4 Landau gauge and the unphysical threshold (point iii)

At ξ = 0 the Goldstone is massless. In the H–Goldstone bubble, and in the k^μk^ν/k² part of the H–V bubble, this opens an
**unphysical** threshold at q² = m_H². At q² = M_V² it is crossed whenever m_H < M_V. At general ξ it is crossed whenever
m_H + √ξ M_V < M_V.

Above that threshold each diagram's g-part is complex, but the imaginary parts cancel exactly:

| m_H, ξ | Im a | Im b |
|---|---|---|
| m_H = 10, ξ = 0 | +1614.14 | −1614.14 |
| m_H = 80, ξ = 0 | +0.00142 | −0.00142 |

The sum agrees with the reference to ≤ 4e-22. Π^L keeps an imaginary part there: Im = −0.75 at m_H = 10.

At m_H = M_V the threshold sits exactly at q² = M_V². The functions are finite there, with Im = 0.

So build b's statement is right: "above threshold (ξ = 0, m_H < M_V) the Goldstone loop has an imaginary part, the real
part is used, it cancels anyway". Taking ln|D| in both pieces is legitimate, because the real parts are the same
function evaluated twice.

I probed both builds (`probe_thresholds.py` → `probe_out.txt`):
* ξ = 0, 1e-12, 1e-6, 1e-3, 0.05, 0.3, 0.5, 2, 7, 100, 1e4, 1e6;
* m_H down to 1 MeV, plus m_H = (1−√ξ)M_V·(1, 1 ± 1e-9), for W and Z;
* 5 values of q².

σ(ξ) equals σ(1) exactly in both builds, and Δr equals the reference exactly. There were no NaNs and no exceptions.

### 2.5 Heavy Higgs (point iv)

From my own integrals at ξ = 0 and ξ = 4, the slope between 1e4 and 1e5 M_W is B(1 − 6.9e-8), where B = 11α/(48πs²).
The deviation is the expected O(M²/m_H² · ln) correction and is the same at both ξ. Build a's own run gives
B(1 − 1.1e-15) between 1e12 and 1e14 M_W, with constant −0.002400630511 = C_INF. Because Π_g is ξ independent, the
11α/(48πs²) and C_INF confirmed by the higgs_dr audit hold at every ξ.

## 3. Observable: pole definition, q^μq^ν, V–φ mixing, tadpoles (points i, ii)

* **Transverse pole.** Write the 1PI V–V function as Π_g g + Π^L qq = Π_g T + (Π_g + q²Π^L) L. The V–φ mixing is
  q^μ Π_{Vφ}, and T_{μν} q^ν = 0. So in the (V_μ, φ) two-point matrix the transverse block decouples exactly. Its
  inverse propagator is T(q² − M₀² − Π_g(q²)). The pole mass is therefore M² = M₀² + Π_g(M²), with no contribution from
  Π^L or Π_{Vφ}, for any ξ. **The concern that a ξ-dependent Higgs piece could enter the pole through V–φ mixing is
  unfounded.** The mixing exists and depends on ξ (§2.2), but it is purely longitudinal.
* **Muon decay.** In W exchange between massless lepton currents, q_μ J^μ = 0 removes every q^μ term (Π^L and the mixing
  insertions). The Goldstones have no coupling to massless leptons. There are no Higgs vertex or box diagrams. So
  G_F/√2 = g₀²/(8(M_W0² + Π_W(0))). From this and s₀² = 1 − M_W0²/M_Z0² I re-derived
  Δr_H = [Π_W(M_W²) − Π_W(0)]/M_W² + (c²/s²)[Π_Z(M_Z²)/M_Z² − Π_W(M_W²)/M_W²], the formula of both builds and of the
  reference.
* **Tadpoles.**
  * A tadpole T attaches to V through the HVV vertex and a zero-momentum H propagator. That gives
    Π_V^tad = (HVV coupling)·T/(−m_H²), up to a phase.
  * HVV/M_V² = g/M_W = 2/v for both W and Z (sympy), so Π^tad_W/M_W² = Π^tad_Z/M_Z². This common shift cancels in both
    brackets of Δr.
  * In R_ξ the tadpole depends on ξ. The Goldstone loops contribute ∝ (m_H²/v)A0(ξM²), and the ghost loops and the ξ part
    of the gauge loops contribute ∝ ξM²A0(ξM²)·(1/v).
  * After division by m_H², the tadpole shift is therefore both ξ dependent and m_H dependent. It still drops out of Δr.
    Both builds say this, and it is correct.
  * Note N2 follows: "Π_VV of the Higgs-containing diagrams is ξ independent" is true only for the SPEC set, which
    excludes tadpoles.

## 4. Mutants (`make_mutants.py`, `run_gate_all.sh` → `run_gate_all_out.txt`, `mutants/*/gate_out.txt`)

Every mutant is an exact text patch of build a. Every mutant dir has higgs_dr_xi.py, DERIVATION.md and MUTANT.txt. The
gate ran from rebuild/campaigns as
`python3 gate.py --mode verifier --campaign higgs_dr_xi --oracle higgs_dr_xi/oracle.py <dir>`.
The proposed checks ran via `python3 higgs_dr_xi/audit_proposed_checks.py <dir>` → `proposed_mutants_out.txt`.

| mutant | what it does | physically wrong? | verifier gate | killed by proposed checks |
|---|---|---|---|---|
| M00 control | nothing | no | PASS | passes all |
| M01 | ignores ξ entirely (Feynman gauge at every ξ) | **no** (outputs exact, since the claim is true) | PASS | passes all (correctly) |
| M02 | Goldstone mass² M² instead of ξM² in the H–φ loop only | yes | killed (6 oracle/blind) | — |
| M03 | Goldstone mass² ξ²M² consistently in both ξ pieces | intermediate wrong, **outputs exact** | PASS | passes all (undetectable from the exports) |
| M04 | H–Goldstone diagram dropped | yes | killed (7) | — |
| M05 | Z: H–χ–Z coupling g/2 instead of g/2c | yes | killed (8) | — |
| M06 | Landau gauge only: kk/k² piece of H–V dropped at ξ = 0 | yes | killed (6) | — |
| **M07** | ξ-dependent shift 0.01(1−ξ)M_V²g²/16π² common to Π_W/M_W², Π_Z/M_Z² (a tadpole-like term kept) | yes (σ wrong at ξ ≠ 1) | **SURVIVES** | B_sigma_xi_independent |
| **M08** | Π_Z gets 0.05(1−ξ)(q²−M_Z²)g²/c²/16π² (Δr sees Π_Z only at M_Z²) | yes | **SURVIVES** | B_sigma_xi_independent |
| **M09** | ξ > 30: Goldstone mass 0.1% off in the H–φ loop ("large-ξ expansion") | yes (Δr too) | **SURVIVES** | B_sigma_xi_independent, B_delta_r_xi_wide |
| **M10** | 0 < ξ < 0.2: Goldstone treated as massless in the H–φ loop only | yes (Δr 16% off at ξ = 0.1) | **SURVIVES** | B_sigma_xi_independent, B_delta_r_xi_wide |
| M11 | m_H > 2.5e7 GeV: heavy-Higgs asymptote with a constant off by 1e-4(1−ξ) | yes | killed (slope, constant, extreme) | — |
| M12 | control: mixing-bracket sign flipped in Δr | yes | killed (6) | — |
| M13 | ξ only in the W sector (Z Goldstone loop at ξ = 1) | yes | killed (6) | — |
| **M14** | 0 < ξ < 0.25: H–φ loop with ln D clipped above the unphysical threshold (Landau-region bug) | yes (Δr 48% off at m_H = 60, ξ = 0.01) | **SURVIVES** | B_sigma_xi_independent, B_delta_r_xi_wide |
| **M15** | ξ ≠ 1, q² < 0: Goldstone loop evaluated at \|q²\| | yes (σ only) | **SURVIVES** | B_sigma_xi_independent |
| M16 | control: seagull dropped (cancels in Δr) | yes (σ) | killed (raw only) | — |

**Result: 6 of 14 wrong mutants survive the shipped gate** (M07, M08, M09, M10, M14, M15). The proposed checks kill all six.
M01 and M03 pass, and they should, because their outputs are the exact physics.

Why they survive:
* **Raw σ at ξ ≠ 1 is never tested.** The oracle's raw check is at ξ = 1 only, and the blind checks test only μ and α
  scaling. This lets M07, M08 and M15 through.
* **The ξ grid has gaps.** It is {0, 0.3, 1, 4, 25} (plus 2, 3 and 5 in single checks). There is no 0 < ξ < 0.3 and no
  ξ > 25. This lets M09, M10 and M14 through. A light Higgs at small nonzero ξ, which is exactly the unphysical-threshold
  region, is untested.

**What M01 means for the gate.** M01 ignores ξ and passes. This is not a gate defect in the usual sense, because M01 is
correct. It does mean the gate **cannot distinguish a true ξ independence from a build that ignores ξ**. No export-level
check can, since a correct answer is ξ independent by definition. M03 is the same: an error that cancels is invisible.
The evidence for the campaign's answer YES is therefore the independent derivation (§2), not the gate. The proposed checks
also cannot tell M01 apart. They close the coverage gaps, but they assume the theorem of §2.

## 5. Proposed checks (`audit_proposed_checks.py`)

All three are blind (no reference value). Each is a function m → (bool, msg), listed in `CHECKS`.

| check | what | a | b | M00/M01/M03 | M07 | M08 | M09 | M10 | M14 | M15 |
|---|---|---|---|---|---|---|---|---|---|---|
| B_sigma_xi_independent | σ_W, σ_Z(ξ) = σ(1) to 1e-9. ξ ∈ {0, 1e-6, 1e-3, 0.01, 0.1, 0.2, 0.3, 2, 4, 25, 100, 1e3, 1e4}, q² ∈ [−50M_W², M_Z²] below threshold, m_H = 1…1500 GeV | PASS (0) | PASS (0) | PASS | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL |
| B_delta_r_xi_wide | Δr(ξ) = Δr(1) to 1e-9, ξ up to 1e4 and small nonzero ξ, m_H = 1 GeV…1e9 GeV | PASS | PASS | PASS | PASS | PASS | FAIL (3.7) | FAIL (0.16) | FAIL (0.48) | PASS |
| B_log_coefficient_xi_wide | B(ξ) = B(1) for ξ = 1e-3, 0.1, 100, 1e4 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |

Outputs: `AUD/proposed_builds_out.txt` and `AUD/proposed_mutants_out.txt`. The check B_sigma_xi_independent is justified
only by §2. Without §2 it would build the campaign's answer into the gate. I recommend adding it to the oracle tier with a
pointer to this audit, or to the blind tier once the campaign's answer is accepted.

## 6. Findings

| id | class | finding |
|---|---|---|
| R0 | R | **None.** reference_dr.py (Feynman gauge) equals my unsplit R_ξ computation at every ξ to ≤ 5e-25 (Π) and ≤ 6e-24 (Δr_rel). The oracle's argument (m_H enters only through Higgs propagators, and Δr is physical) is confirmed by explicit computation, including at the level of Π_g. |
| C0 | C | **The claim of ξ independence is not false in any respect checked.** Δr_H(m_H) − Δr_H(M_W), B = 11α/(48πs²), the constant, and even Π_g(q²) of the SPEC diagram set are ξ independent for all ξ ≥ 0. The transverse pole gets nothing from V–φ mixing (purely ∝ q^μ). |
| C1 | C (coverage) | The gate cannot separate "ξ independent" from "ignores ξ" (M01). The evidence must be an independent derivation, as in §2 here. State this in the campaign record. |
| C2 | C (coverage) | Raw σ at ξ ≠ 1 is untested. M07, M08 and M15 survive. Fix: B_sigma_xi_independent. |
| C3 | C (coverage) | The ξ grid has no 0 < ξ < 0.3 and no ξ > 25, and the light-Higgs unphysical-threshold region at small ξ is untested. M09, M10 and M14 survive. Fix: B_sigma_xi_independent and B_delta_r_xi_wide. |
| B1 | B (build b, low; evidence wording) | b says "the exports evaluate each diagram separately with its own ξ and the cancellation appears numerically", and lists "(iii) unitary-gauge sum vs the diagram-by-diagram ξ sum" as a check. After the partial-fraction split, the ξ pieces are the **same** B00x value added and subtracted (`_hv_terms`), so the cancellation holds by construction. Check (iii) is not independent of the split. The physics is right (§2), but b has no PF-free verification of its own. |
| B2 | B (build a, info) | a's code also cancels the ξ pieces by construction (`a2 = -bxi`, `b = +bxi`). Unlike b, a provides a genuine PF-free second route: the unsplit C00 by 2D quadrature. I ran it, and it agrees in all 13 printed digits at ξ = 0, 0.3, 1, 4, 25 and four q² (`AUD/build_a_main_out.txt`). No action needed. |
| N1 | N | Neither build computes Π^L or Π_{Vφ}. Both assert, correctly, that ξ "lives" there. I computed both, and both are ξ dependent (§0). |
| N2 | N | The statement "Π_VV of the Higgs-containing diagrams is ξ independent" holds only with tadpoles excluded (SPEC §2). The H tadpole contains an H propagator and is both ξ and m_H dependent. It shifts Π_W/M_W² and Π_Z/M_Z² equally, so Δr is unaffected. |
| N3 | N | SPEC §2 says "for q² below every threshold (q² < (m_H+M_V)²) Π_VV is real". That holds for the g^{μν} sum. Individual diagrams, and Π^L, have an unphysical threshold at (m_H + √ξM_V)², which lies below M_V² for small ξ and a light Higgs. |
| N4 | N | Both builds reproduce the reference bit for bit, and σ(ξ) = σ(1) exactly (0 ulp). Agreement with the oracle again says nothing about method independence. |

## 7. Verdict

* **Build a: ACCEPT.** The derivation is correct and complete. The ghost, pole, q^μq^ν, mixing and tadpole arguments are
  all right. There is a genuine PF-free second route, the gate passes, and the proposed checks pass.
* **Build b: ACCEPT.** The derivation and numbers are correct, the gate passes, and the proposed checks pass. Its claim of
  numerical evidence should be toned down (B1). The ξ independence in b rests on its algebra, which §2 confirms
  independently, and not on its numerics.
* **Campaign answer: YES.** The Higgs-dependent Δr_H(m_H) − Δr_H(M_W) is independent of ξ, and so is Π_g(q²) of the
  SPEC diagram set. This is established by §2, not by the gate.

## 8. What I could not verify

* My routes use the same dim-reg conventions as the reference for the m_H-independent constants. Δr_rel does not depend on
  them, and the higgs_dr audit covered them.
* Π^L and Π_{Vφ}: I computed them only by exact-d Feynman parameters, with no second route. Only "ξ dependent and nonzero"
  is claimed; the values are not validated to high precision. The W–φ diagram phases follow my rule derivation, and I did
  not check them against a Slavnov–Taylor identity.
* The tadpole's ξ dependence is argued from the vertex structure (H c̄c ∝ ξ, Hφφ ∝ m_H²). I did not evaluate it in closed
  form. Only its common-shift property matters, and that property is checked exactly.
* The 4D Euclidean route covers spacelike q² only. Timelike points rest on route 1 plus the pointwise identity.
* Above the physical threshold nothing is tested, and SPEC does not ask for it.
