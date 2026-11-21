# Red-team audit: nucleon_pol (α_E, β_M of the nucleon from the pion cloud, O(p³) heavy-baryon ChPT)

In the repository I wrote only this file and `audit_proposed_checks.py`. All scratch work is in
`S = /tmp/claude-0/-home-user-STUR-Physics-Lab/6f003c51-fc14-5da0-833a-45f53d6397be/scratchpad/audit-nucleon_pol`:
* `compton.py` / `compton.log`: the independent real-photon Compton route (§1);
* `make_mutants.py`, `mutants/<name>/` (each with `gate_stdout.txt`, `proposed_out.txt`), `gates.log`, `proposed.log` (§3);
* `checks_a.log`, `checks_b.log`: the proposed checks on both builds; `lint_proposal.log`: the proposed lint setting (C2).

The builds were gated from copies in `S/copies/{a,b}` (the gate writes `gate_report.json` into the build directory).
Nothing was written into `builds/` or `oracle.py`. A verifier gate run takes about 1 s.

Classes, as in the sibling audits: **B** = a defect in a build. **R** = a SPEC wording or ambiguity issue.
**C** = an oracle or check gap, or a caveat. **N** = a note or a positive result.

## 0. Verdict

* **Both builds are correct. I found no B finding.** The real-photon Compton amplitude, computed at general ω and angle
  without any static-field or zero-frequency argument, gives

  α_E = 5 α g_A² / (96 π f² m_π) = 5 e² g_A² / (384 π² f² m_π),  β_M = α g_A² / (192 π f² m_π) = α_E / 10,

  in the SPEC convention H_eff = −½·4π(α_E E² + β_M B²), Heaviside–Lorentz. At g_A = 1.27, f = 92.4 MeV, m_π = 139.57 MeV
  this is α_E = 12.58·10⁻⁴ fm³, β_M = 1.258·10⁻⁴ fm³.
* **Build b's two unchecked steps hold.** S1 (static-field energy shift = Born-subtracted O(ω²) Compton coefficient) and
  S2 (only zero Euclidean frequency survives) are both confirmed by §1. The Compton route reaches the same two numbers
  through different diagrams: there, the Kroll–Ruderman graphs carry most of α_E, whereas in the builds' static gauges they vanish.
* **The oracle reference is right** (it was recalled, not transcribed). The 12.6·10⁻⁴ fm³ is in the SPEC convention, which is
  numerically the Gaussian-unit polarizability (§1d).
* **The gate pins two pure numbers plus ħc** (§4). Every derivation-level mutant I made fails it (M01–M03, M05–M15).
  **7 of 21 genuinely wrong mutants pass** (M16–M22). They are wrong only outside the sampled parameter window, or they
  type in the answer (M19). The 4 proposed checks kill all 7, and both builds pass them. M04 is an equivalent mutant (N3).

## 1. Independent derivation: the real-photon Compton route (task 1; `S/compton.py`)

### (a) Method

* **Setting.** Static nucleon (m_N → ∞) at the origin. The SPEC Lagrangian gives:
  * H_πN = (g_A/2f) σ_i τ_a (D_i π)_a(0), which contains the πNN vertex and Kroll–Ruderman (KR);
  * the charged-pion operator K = −∂_t² + D² − m², with D = ∇ − ieA. Its expansion gives the γππ vertex e a·(2q+k)
    and the γγππ seagull −2e² a·a′.
* **Photons.** Two real photons: A = a e^{−ik·x} + a′ e^{+ik′·x}, with ω = ω′, |k| = |k′| = ω and scattering angle θ.
  The gauge is radiation gauge A⁰ = 0 (ε·v = 0).
* **What is computed.** The one-loop effective action of the source to O(g_A² e²):

  iS_eff = −2 (g_A/2f)² ∫d⁴p/(2π)⁴ F(p)/(−p⁰ + i0),  F = ⟨p+k−k′| D_i K⁻¹ D_i |p⟩,

  * the factor 2 counts π⁺ and π⁻ (§1c);
  * the heavy-nucleon propagator 1/(−p⁰ + i0) carries the full external energy dependence;
  * the formula's normalisation is checked at zero field against second-order perturbation theory, −Σ|V|²/E_π.
* **Diagrams.** 9 terms, written out by hand:
  * KR–KR, 2 orderings;
  * KR + photon on the pion line, 4 graphs;
  * seagull, 1;
  * two γππ insertions, 2 orderings.

  Photons on the nucleon line couple only to v·A = A⁰ = 0, so the nucleon-pole (Born) graphs vanish identically. The Thomson
  term −Z²e²/m_N is O(1/m_N). Nothing has to be subtracted: in this gauge the whole one-loop amplitude is the structure part.
* **Computation chain.**
  * Feynman parameters combine the pion propagators.
  * The momentum shift p → p − P moves the heavy pole to p⁰ = P⁰ + i0.
  * The p⁰ integral is the residue at the N-fold pion pole p⁰ = +E in the lower half plane. The nucleon pole lies in the upper
    half plane at every ω, so it is never used.
  * The integrand is expanded to O(ω²). This is legitimate below threshold, ω < m_π.
  * Then n-dimensional angular averages, dimensionally regularised radial integrals at n = 3 − 2ε, the simplex integrals, and ε → 0.
* **Matching.** The SPEC's S_eff = ∫dt 2π(α_E E² + β_M B²) with E = −∂_t A gives
  4π[α_E ω² a·a′ + β_M (k×a)·(k′×a′)]. Two polarisation sets separate α from β by their angle dependence:
  * ⊥ (both ŷ): 4π(α_E + β_M cos θ) ω²;
  * ∥ (in the plane): 4π(α_E cos θ + β_M) ω².

### (b) Results (`compton.log`)

| Order | Result |
|---|---|
| ω⁰ | **0** for both polarisations. Each diagram is ∝ m_π; they cancel (KR–KR −1/4, KR–line +1/2, seagull +3/8, double −5/8, in units e²m/π). This is the low-energy theorem T(0) = −Z²e²/m_N → 0, so it is a gauge-invariance check. |
| ω¹ | **0**. Individual diagrams have 1/ε poles (heavy-baryon J₀-type, ∝ ω/ε). They cancel between crossed graphs. |
| ω², ⊥ | e²ω²(10 + cos θ)/(96π m_π) |
| ω², ∥ | e²ω²(1 + 10 cos θ)/(96π m_π) |
| Fit | The ⊥ amplitude alone gives α_E = 5αg²/(96πf²m), β_M = αg²/(192πf²m). The ∥ amplitude is then reproduced exactly (residual 0), so the angular structure is the polarizability form, with no extra structure. |

The ω² share of each diagram class (⊥, units e²ω²/(96π m)):
* KR–KR: +12;
* KR–line: −8;
* seagull: 10(1 − cos θ);
* double insertion: −4 + 11 cos θ.

The builds' static gauges (A(0) = 0, or a Coulomb field with a q·q′ read-off) see none of the KR terms: there α_E comes entirely
from the A⁰² seagull. Gauge invariance and the result are the same.

### (c) What this checks

* **S1, the static energy equals the Born-subtracted O(ω²) Compton coefficient: confirmed.**
  * In the Compton route the E² term arises from −∂_t A at ω ≠ 0 with transverse photons. In the builds it arises from a static A⁰.
  * The two coefficients agree exactly, and so do the β_M coefficients.
  * The Born subtraction is unambiguous here because the Born graphs are identically zero in radiation gauge at this order (R2).
* **S2, only zero Euclidean frequency survives: confirmed, and not needed.** I never use it. The nucleon pole is kept at finite
  external energy, and the contour is closed on the side without it.
  * Build b's argument is also correct on its own terms. In a static background the pion operator has no l⁰-odd piece at even
    order in the fields: in the electric case −2l⁰eA⁰ appears only squared at O(E²), and in the magnetic case there is no l⁰
    term at all. So P/l⁰ integrates to zero, and only the iπδ(l⁰) half survives.
  * Build a's form of the argument (the correlator is even in τ) is the same statement.
* **Isospin, neutron = proton: shown explicitly, without relying on the builds' wording.**
  * The spin-independent part needs ⟨N|τ_a τ_b|N⟩ G_ab = Σ_a G_aa + i ε_ab3 ⟨τ₃⟩ G_ab.
  * The redefinition π₂ → −π₂ together with e → −e leaves the Lagrangian invariant and flips G₁₂. So G₁₂ is odd in e, and its
    O(e²) part vanishes. Only δ_ab survives, independent of the nucleon state.
  * The surviving G₁₁ + G₂₂ = S₊ + S₋ (π⁺ and π⁻ loops) has S₊ = S₋ at O(e²). The weights are p → nπ⁺ (2) and n → pπ⁻ (2).
  * **π⁰:** [Q, τ₃] = 0, so π⁰ has no KR vertex and no γππ vertex. Its loop is field-independent, and the anomaly is not in the SPEC.
  * **Weinberg–Tomozawa:** v·Γ has photon pieces ∝ v·A = 0 in this gauge. Its ππNN piece closes a pion loop at one point,
    ∝ τ_c ε_cab π_a ∂₀π_b, which is the pion charge density. That is C-odd, so its O(A²) part vanishes (Furry).
* **Finiteness.** The O(ω²) coefficients are pole-free diagram by diagram (Γ functions at half-integer arguments). The only poles
  are at O(ω¹), and they cancel. The 1/m_π behaviour is non-analytic, so no O(p³) counterterm exists.

### (d) Conventions and numbers

* **SPEC convention.** H = −½·4π α_E E²_HL = −½ α_E E²_G, using E²_G = 4πE²_HL. So the SPEC's α_E is numerically the
  Gaussian-unit polarizability, and d = 4π α_E E_HL = α_E E_G.
* **Value.** In this convention 5αg²/(96πf²m)·(ħc)³ = 1.2582·10⁻³ fm³ at the physical inputs, which is the usual 12.6·10⁻⁴ fm³.
  It is compared with the measured 11.2 ± 0.4, which is quoted in the same convention.
* **Cross-checks.**
  * The Gaussian-convention Baldin sum rule α + β = (1/2π²)∫σ/ω² dω is the form build a's route C uses, and it reproduces
    (11/10)α_E. This ties the convention to a cross-section normalisation and not only to SPEC wording.
  * With the "natural HL" normalisation H = −½ α E²_HL one would get 4π × that = 1.58·10⁻² fm³ (mutant M07). M08 is the inverse error.
* **Proton value.** Both builds return the proton value. No export takes an isospin argument, so the gate cannot test
  neutron = proton (C3); §1c covers it analytically.

### (e) What is independent and what is shared

**Independent of the builds:**
* real photons at ω ≠ 0 and general angle, with α and β separated by the angle dependence;
* radiation gauge, in which the KR graphs contribute;
* the heavy-nucleon pole kept and handled by contour choice;
* Feynman parameters with a residue p⁰ integral;
* all of the code (`compton.py` shares nothing with either build);
* the explicit isospin and Furry arguments.

**Shared with the SPEC and the builds:**
* the SPEC Lagrangian and vertex normalisation (g_A/2f)σ·∇π τ with minimal coupling;
* the heavy-baryon static limit m_N → ∞;
* no Δ and no counterterms;
* the isospin limit (one m_π);
* the identification L_eff = 2π(α_E E² + β_M B²);
* the textbook n-dimensional angular-average and radial dim-reg formulas, which build a also uses;
* prior knowledge: like the builders, I knew the textbook result. Nothing is typed into `compton.py`; the numbers 10, 1 and 5/96 come out of the diagrams.

## 2. Build-specific notes

* **N1. Build a is the more complete build.** It has three routes: plane-wave static Coulomb/transverse fields; uniform-field
  gauges in position space; and the Baldin sum rule for α + β over the LO γp → π⁺n cross section. It also runs an
  explicit gauge-invariance check of the magnetic loop (the (q·q′)(a·a′) and (q·a′)(q′·a) coefficients equal and opposite).
  Its §7 says that the full real-photon, general-angle Compton loop was not done. §1 does it.
* **N2. Build b's two routes are two gauges of the same static functional** (symmetric and Landau). As build b states in its
  DERIVATION §7, they did not check S1 and S2. Its DERIVATION §2 calls the Born graphs "O(g_A⁴)". That is accurate only in a
  gauge where the tree γNN vertex vanishes (A⁰(0) = 0 or radiation gauge), so the wording is loose but the code is unaffected.
* **N3. The two orderings of build a's T4 are equal** in the static limit: each gives −11/(96πm) and 1/(96πm), by
  crossing/relabelling symmetry. So M04, which keeps one ordering twice, is an equivalent mutant, not a wrong one. Similarly,
  T2 (KR + line) contributes exactly zero in build a's gauge, so dropping it would also be equivalent.

## 3. Mutants of build a (task 2)

Each mutant is one or two exact text substitutions of `builds/a/nucleon_pol.py` (`S/make_mutants.py`). Each was run with
`python3 gate.py --mode verifier --campaign nucleon_pol --oracle nucleon_pol/oracle.py <dir>` from `campaigns/`, and then
with `audit_proposed_checks.py`.

| Mutant | Error | Gate | Killed by (gate) | Killed by (proposed) |
|---|---|---|---|---|
| M01 | seagull loop momentum routing (k+Q)·k → k·k (factor 5 wrong) | FAIL | blind ratio and size, oracle α, fm³ | grid |
| M02 | paramagnetic double insertion T4 dropped | FAIL | blind (gauge-check crash), all oracle | grid, homogeneity |
| M03 | diamagnetic seagull T3 dropped from β | FAIL | as M02 | grid, homogeneity |
| *M04* | T4: one ordering counted twice (*equivalent*, N3) | *PASS* | – | – |
| M05 | isospin weight doubled (π⁺ and π⁻ counted as separate states) | FAIL | oracle α, β, fm³ | grid |
| M06 | π⁰ counted like a charged pion (weight 3/2) | FAIL | oracle α, β, fm³ | grid |
| M07 | Gaussian/HL: × 4π | FAIL | blind size, oracle | grid |
| M08 | Gaussian/HL: ÷ 4π | FAIL | oracle | grid |
| M09 | e² replaced by α | FAIL | oracle | grid |
| M10 | 1/m_π² × 139.57 (right only at the physical point) | FAIL | blind scaling, oracle α, β | grid, homogeneity |
| M11 | ħc = 197.327 | FAIL | blind to_fm3, oracle fm³ | to_fm3 |
| M12 | (ħc)² in to_fm3 | FAIL | blind, oracle fm³ | to_fm3 |
| M13 | f ↔ F = √2 f (130 MeV normalisation) | FAIL | oracle | grid |
| M14 | S = σ instead of σ/2 (× 4) | FAIL | oracle | grid |
| M15 | full-line instead of half-line τ integral (× ½) | FAIL | oracle | grid |
| **M16** | g_A·\|g_A\| (wrong for g_A < 0) | **PASS** | – | grid, homogeneity |
| **M17** | m_π clamped at ≥ 40 MeV (chiral limit wrong) | **PASS** | – | grid, homogeneity |
| **M18** | f > 200 MeV branch with a different power | **PASS** | – | grid, homogeneity |
| **M19** | closed form typed in, β = α/10 typed in (correct values, not derived) | **PASS** | – | lint heuristic (and C2) |
| **M20** | e² × (1 + α) for α ≥ 0.05 | **PASS** | – | grid, homogeneity |
| **M21** | to_fm3 uses \|x\| | **PASS** | – | to_fm3 |
| **M22** | β_M × 1.1 for m_π ≥ 600 MeV | **PASS** | – | grid, homogeneity |

**Totals:**
* 21 genuinely wrong mutants plus 1 equivalent one. The gate kills 14, and **7 survive** (M16–M22).
* **No survivor is a derivation error at the sampled points.** Each is a parameter region the oracle does not sample, or a
  typed-in answer.
* **The blind tier kills 7** (M01–M03, M07, M10, and M11 and M12 via to_fm3).
* **All 7 survivors fail `audit_proposed_checks.py`**, and every killed mutant fails it too.
* **Both builds pass all 4 proposed checks** (`checks_a.log`, `checks_b.log`; worst relative 6.7·10⁻¹⁶).

## 4. How few probes the gate has

**What the answer is.** Two pure numbers, 5/(96π) and 1/(192π), times α g_A²/(f² m_π), plus (ħc)³. The blind tier fixes the
functional form:
* single factor-2 scalings at one point;
* β/α constant at 3 points;
* positivity and size.

**What the oracle samples.** It pins both numbers at 10⁻¹² at 5 points: g_A ∈ [0.5, 2], f ∈ [60, 130] MeV,
m_π ∈ [50, 500] MeV, α ∈ [1/150, 1/100]. So any error that changes a coefficient is caught: factor 5, the 1/10, isospin,
4π, e² vs α, f normalisation, a dropped diagram class, the power of m_π, ħc. That is M01–M15.

**What the SPEC's exports allow** (all used in §5):
* **The full parameter space:** negative g_A; the chiral limit m_π → 0, where α_E ∝ 1/m_π is the physics claim; heavy pions;
  large f; α up to 1.
* **Exact reference-free structure:** evenness in g_A; homogeneity of degree −3 under (f, m_π) → λ(f, m_π); exact 1/m_π
  over many decades; exact linearity in α with α_E(α = 0) = 0; β/α everywhere.
* **to_fm3 on any real x.**

**What they do not allow.** The exports have no isospin argument, no intermediate quantity (Compton angle structure, α + β,
the n-dimensional closed form) and no frequency dependence. So the internals cannot be probed, and a correct typed-in answer
passes (M19).

## 5. Findings

* **C1. The parameter window is narrow and positive-only.** M16, M17, M18, M20 and M22 pass. **Fix:**
  * `audit_wide_grid`: 240 points, g_A = −1.27 to 3, f = 10 to 5000 MeV, m_π = 0.1 MeV to 10 GeV, α = 10⁻⁶ to 0.5,
    against the auditor's Compton-route coefficients, relative 10⁻¹⁰.
  * `audit_homogeneity`: reference-free evenness, homogeneity, 1/m_π from 10⁻³ to 10⁵ MeV, linearity in α, and the β/α ratio.
  * `audit_to_fm3_linear` covers M21.
* **C2. Lint cannot see a typed closed form.** `LINT_EXACT` folds only constant subtrees. In
  `5*alpha*gA**2/(96*math.pi*fpi**2*mpi)` no subtree equals 5/(96π), so M19 passes. **Fix (oracle edit, for the orchestrator;
  I did not make it):** add 96, 192, 384, 768 to `LINT_EXACT`, because `_fold` also checks bare constants. With that setting
  `gate.lint` flags M19 (line 119) and reports nothing for builds a and b (`lint_proposal.log`). The same rule is in
  `audit_no_closed_form_literals` as a heuristic. A determined builder can still evade it (for example with 3·32), so the
  transcript audit remains the real guard.
* **C3. neutron = proton is untestable through the exports.** §1c establishes it analytically: G₁₂ is odd in e, π⁰ decouples,
  and WT is Furry-odd. An optional export `alpha_E(..., nucleon='n')` would make it a gate check, but only a trivial one.
* **C4. The reference was recalled, not transcribed.** §1 confirms it independently. The confirmation shares the SPEC's
  Lagrangian, the heavy-baryon limit, the absence of Δ and counterterms, and the convention for α_E (§1e).
* **R1. "Read off from the O(ω²) terms of the forward Compton amplitude" (SPEC §2) determines only α_E + β_M.**
  Build b's QUESTIONS 1 raised this. **Fix:** "from the O(ω²) terms of the Compton amplitude at general angle, or equivalently
  the static energy shift". The equivalence is what §1 confirms.
* **R2. The Born subtraction should be stated concretely.** For m_N → ∞ with only L^(1) and gauge ε·v = 0, the nucleon-pole
  graphs and the Thomson term vanish, so the full one-loop amplitude is the structure amplitude. In other gauges the Born graphs
  are singular (1/(v·p) at zero energy), and both builds needed a separate argument (build a: the q·q′ read-off; build b:
  "drop nucleon-reducible graphs").
* **R3 (optional SPEC change). Intermediate exports.** Possible additions:
  * `compton_w2(pol, cos_theta)`, the ω² coefficient of the real-photon amplitude: (10 + cos θ) and (1 + 10 cos θ) in units of
    e²/(96π m_π) per 2(g_A/2f)²;
  * `alpha_plus_beta_baldin`;
  * the n-dimensional coefficient c(n) = −(n/2 + 1)Γ(2 − n/2)m^{n−4}/(6(4π)^{n/2}).

  These would test S1 and the angular separation directly, and would kill a typed-in answer. Diagram-by-diagram exports would
  be gauge dependent, so they should not be added.
* **N1.** The Compton route (§1) gives α_E = 5αg_A²/(96πf²m_π) and β_M = α_E/10 exactly. The amplitude vanishes at O(ω⁰)
  (low-energy theorem), and the O(ω) poles cancel.
* **N2.** S1 and S2 are confirmed, so build b's caveats are resolved.
* **N3.** M04 and the dropping of T2 are equivalent mutants of build a. In the static gauge build a's KR terms are zero, while in
  radiation gauge they give 12/96 − 8/96 of the ω² coefficient.

## 6. Not verified

* Isospin breaking (m_π± ≠ m_π0), which is outside the SPEC.
* The Δ and O(p⁴) counterterms, which the SPEC excludes.
* Spin-dependent polarizabilities.
* A fully covariant (finite m_N) calculation.
* A 't Hooft–Veltman-type treatment, which is not needed: there are no γ5 traces.
