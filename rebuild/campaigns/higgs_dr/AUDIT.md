# AUDIT: campaign higgs_dr (Higgs part of Sirlin's Δr with q²-dependent self-energies), builds a and b

Auditor (red team). In the repository I wrote only this file and `audit_proposed_checks.py`. Everything else ran on copies,
in the scratch directory `AUD = /tmp/claude-0/-home-user-STUR-Physics-Lab/6f003c51-fc14-5da0-833a-45f53d6397be/scratchpad/audit-higgs_dr`:
`copies/{a,b}` hold the builds, `mutants/` the mutants, and the scripts and their `*_out.txt` outputs sit next to them.
Builds: `.../scratchpad/verify-higgs_dr-a`, `.../scratchpad/verify-higgs_dr-b`.

## 0. Bottom line

* **The physics of the reference and of both builds is right.** I derived the Feynman rules myself (sympy) and
  re-derived Δr_H. I then evaluated the self-energies by three routes that share no code and no method with
  reference_dr.py: analytic Passarino–Veltman, a dispersion relation with Cutkosky imaginary parts, and a 4D Euclidean
  momentum integral. All three agree with the reference: to 1e-40, 1e-10 and ≤6e-12 (Δr_rel itself to ≤4e-13) respectively. The heavy-Higgs
  coefficient is 11α/(48πs²), and the constant reproduces the literature form (11/3)(α/16πs²)[ln(m_H²/M_W²) − 5/6]
  exactly at μ = M_W. **No class R error.**
* **Gate weakness: 3 of 15 wrong mutants pass the full verifier gate.** They are M08 (a switch to the heavy-Higgs
  asymptote above 6 TeV), M09 (self-energies that ignore the α, M_W, M_Z arguments in the couplings) and M10b (a wrong
  Goldstone q² term for q² < −5 M_W²). The five checks in `audit_proposed_checks.py` kill all three and pass both
  builds, with one exception, H_own_precision_extreme, which fails build b (next point).
* **Build b passes the gate only because the oracle raised its precision.** `reference_dr.py` sets the global
  `mp.mp.dps = 40` when it is imported. Build b depends on the global setting (`mp.mp.dps = 30`), so under the gate it
  silently ran at 40 digits. At its own 30 digits it misses the oracle's `extreme_mass_check`: 4.0e-4 at m_H = 1e14 M_W
  (tolerance 1e-8). With a patched oracle that uses only local precision, the gate **fails** build b
  (`gate_isolated_oracle_b.txt`) and still passes build a. This is finding C1 (campaign) plus B1 (build b, numerical).
* **Verdict:** build a may be accepted as derived. Build b's derivation is correct, but b should not be accepted as
  gated until it fixes its working precision (B1). Its physics content is accepted (§5).

## 1. Independent validation of the reference (task 1)

### 1.1 Feynman rules (`vertices.py` → `vertices_out.txt`)

I expanded |DΦ|² in sympy with commuting symbols (∂F as a symbol), using the SPEC conventions exactly. Every monomial
containing H and a vector:

| term | coefficient | rule (incoming momenta) |
|---|---|---|
| H W⁺W⁻ | g²v/2 = g M_W | i g M_W g^{μν} |
| H Z² | g²v/(4c²) | i (g/c) M_Z g^{μν} |
| H² W⁺W⁻ | g²/4 | i g²/2 g^{μν} |
| H² Z² | g²/(8c²) | i g²/(2c²) g^{μν} |
| W⁺(φ⁻∂H − H∂φ⁻) | i g/2 | i(g/2)(p_H − p_φ)^μ, with the conjugate −i(g/2)(p_H − p_φ)^μ for W⁻φ⁺H |
| Z(H∂χ − χ∂H) | g/(2c) | (g/2c)(p_χ − p_H)^μ |
| H φ^∓ W^± Z, H φ^∓ W^± A | g²(c²−1)/(2c), g² s/2 | cannot close a loop on two W's or two Z's at one loop |

The diagram set has three members per vector: the HH seagull, the H-V bubble and the H-Goldstone bubble (plus tadpoles).
It matches the accepted higgs_rho audit §1.2. In the H-Goldstone bubble, the vertex product times i·i from the scalar
propagators is +κ²(2k−q)^μ(2k−q)^ν, with κ = g/2 for the W and g/2c for the Z. The g^{μν} part is 4κ² B00. With these
rules I get 16π² Π_V/κ_V² = −M_V² B0 + B00 − A0(m_H)/4, with κ_W² = g² and κ_Z² = g²/c². The signs and the
convention M²_eff = M² + Π (1PI = iΠ g^{μν}) are the same as reference_dr.py.

### 1.2 Δr_H (my own derivation)

Start from G_F/√2 = g₀²/(8(M_W0² + Π_W(0))), g₀² = e²/s₀², M_V0² = M_V² − Π_V(M_V²) and s₀² = 1 − M_W0²/M_Z0².
These give s₀² = s² + c²[Π_W(M_W²)/M_W² − Π_Z(M_Z²)/M_Z²] and

  Δr_H = [Π_W(M_W²) − Π_W(0)]/M_W² + (c²/s²)[Π_Z(M_Z²)/M_Z² − Π_W(M_W²)/M_W²].

This is the reference formula. With Σ = −Π it is also Denner's on-shell Δr, Fortsch. Phys. 41 (1993) eq. (4.20), keeping
only the Higgs terms. A tadpole shifts Π_W/M_W² and Π_Z/M_Z² by the same constant g t/M_W, so it cancels in both
brackets. The sign is right: Δr_H rises with m_H, so M_W falls.

### 1.3 Route A: analytic PV (`indep_routes.py` → `indep_routes_out.txt`, `routeA_wide_out.txt`)

* B0 uses the closed log form (Denner 4.23, with r + 1/r = (m₀²+m₁²−p²−i0)/(m₀m₁)), at 80 digits internally.
* B1 and B00 come from PV reduction, B00(0) is in closed form, and A0 is analytic. No Feynman-parameter quadrature.
* **Raw h(q²) against reference_dr.pi_v:** worst relative deviation 7.8e-40. The grid was M = M_W, M_Z;
  m_H = 10, 50, 80.38, 125.2, 400, 1500, 5000; q² = 0, 0.01, 0.5M_W², M_W², M_Z², 1.7M_Z², −0.2M_W², −3M_W², −50M_W²,
  0.98(m_H+M)², (m_H−M)²; μ = M_W, 2M_W, 0.7M_W, 17 GeV. Points above threshold were skipped. On the wider grid used by
  my proposed check (q² down to −500 M_W², M = 75 GeV) the deviation is 5e-40.
* **Δr_rel against the reference** at m_H = 10…1e4 GeV, μ = M_W and 3.7 M_W, plus the two other (M_W, M_Z, α)
  points: 1.3e-37.
* **Heavy Higgs:**
  * The slope over 1e6–1e7 M_W is B(1 − 1.1e-11), with B = 11α/(48πs²).
  * The constant is C = −2.400630511e-3. It is −2.4006305112e-3 at 1e7 M_W, against the oracle's C_INF =
    −2.4006305111738e-3.
  * At μ = M_W, Δr_H(m_H) − (11/12)(α/4πs²)[ln(m_H²/M_W²) − 5/6] = 1.7e-17 at m_H = 1e8 M_W. This is the literature
    heavy-Higgs form (Marciano–Sirlin; PDG EW review), constant term included.
  * The coefficient decomposes as (11/12)K = K[1/12 + (c²/s²)(5/6)(s²/c²)], K = α/(4πs²). The 1/12 comes from
    Π_W(M_W²) − Π_W(0) and the 5/6 from the mixing bracket at q² = M_V².

### 1.4 Route B: dispersion relation (non-polynomial q² dependence)

* Im parts come from Cutkosky, with the two-body tensor projected on shell:
  ⟨(2k−q)^μ(2k−q)^ν⟩ → A g^{μν}, A = (1/3)[P² − (P·q)²/q²] = −λ/(3s).
  This gives Im B0 = πλ^{1/2}/s and Im B00 = −πλ^{3/2}/(12 s²).
* h(q²) − h(0) − q² h′(0) = (q⁴/π)∫ Im h(s)/(s²(s−q²)) ds, with h(0) and h′(0) from route A.
* Agreement with the reference is 1.2e-10 (limited by the finite-difference h′(0)). The grid was m_H = 50…1500,
  q² = 0.5M_W², M_W², M_Z², −3M_W², −40M_W² and 0.9(m_H+M)², for W and Z.
* This confirms the Goldstone-loop q² dependence and its sign independently of the Feynman-parameter form.

### 1.5 Route C: 4D Euclidean momentum integral (`route_c.py` → `route_c_out.txt`)

* No Feynman parameters, no PV, no dimensional regularization. The g^{μν} part is the transverse part
  (2k−q)_⊥²/3 = (4/3)k² sin²θ. The Wick-rotation signs are A0 = −16π²∫1/D, B0 = 16π²∫1/(DD) and
  B00 = −(16π²/4)·(transverse coefficient).
* The regularization-dependent pieces are local polynomials a m_H² + b M² + c q². The UV-finite second difference
  G = h(q₁)−h(0) − (q₁/q₂)[h(q₂)−h(0)] removes them. Δr_rel removes them too: the a m_H² piece enters Π_W/M_W² and
  Π_Z/M_Z² identically, because κ_W²/M_W² = κ_Z²/M_Z².
* Timelike q² uses q_E = (0,0,0, i√q²) with routing α = 1/2, which has no poles below threshold for m_H > √q²/2. The UV
  tail beyond k = 100 × (largest scale) is a fitted pure power.
* **Spacelike G** at m_H = 50, 125.2, 400 and two (q₁, q₂) pairs: agreement 5e-13 to 9e-13.
* **Timelike G** (q₁ = M_V², q₂ = M_V²/2, complex q_E) for W and Z at m_H = 125.2 and 400: agreement 5e-13 to 6e-12.
* **The complete Δr_rel at the physical points** (Π_W(M_W²), Π_W(0), Π_Z(M_Z²), all in one 4D integrand) at
  m_H = 50, 125.2, 300 and 1000 GeV: agreement 7.8e-14 to 4.0e-13. For example, at m_H = 125.2 the 4D route gives
  1.47748694563899e-3 and the reference 1.47748694563918e-3.

### 1.6 Cross-check with higgs_rho, and what I could not verify

The reference also agrees with the accepted higgs_rho audit reference at q² = 0: Π_W(0) to 1.4e-40 and Δρ_rel to
2.3e-38 (`vs_higgs_rho.py`).

Not verified:
* No route gives the m_H-independent constants of Π (A0's "+1", B00's "+1", MS-bar) independently of dimensional
  regularization. Routes A and B use the same dim-reg definitions of A0, B0 and B00. Only the convention pinned in SPEC
  §2 fixes them, and that convention is what `raw_check` tests. Δr_rel does not depend on them, as §3 shows.
* Above threshold the reference returns an mpc and the oracle's `float()` would raise. Nothing tests there, and SPEC
  restricts Π to the real region.

## 2. The builds' derivations (task 2)

Both builds use exactly the Feynman-parameter functions of the reference, with x on the Higgs line (a) or on the V
line (b). Their outputs equal the reference to 0 ulp at every oracle point and on my wider grids
(`proposed_checks_out.txt`). I looked for errors that agree only at tested points or only in a limit, and found none in
either build:

| item | a | b |
|---|---|---|
| Feynman rules | complete table, matches §1.1 (vertex phases included) | HVV, seagulls right. W-φ-H rule written as (g/2)(p_H−p_φ) **without the i** (B2) |
| Goldstone-loop sign | derived from the vertex phases | not derived: fixed by requiring that the seagull and bubble quadratic divergences cancel (B2) |
| q² dependence | Δ(x) = (1−x)M² + x m_H² − x(1−x)q², the "+1" from the O(ε) of 1/d explained | same function. The "+1" comes from the d/2 identity ("4/d·d/2 = 2"), which is equivalent |
| μ / pole structure | dh/dlnμ² = −3M²/4 − q²/12, m_H-independent | same |
| tadpoles | common shift g t/M_W, cancels in both brackets | same (τ M_V²) |
| Δr_H | §3, identical to §1.2 | §3, identical |
| B and constant | 11/12 K and constant −5/6 (matches the literature, §1.3) | 11/12 K, no constant |
| threshold | guarded (ValueError at q² ≥ (m_H+M)²) | positivity of Δ shown only for q² ≤ M_V². Above threshold float() raises |
| precision | `mpmath.workdps(40)` locally | global `mp.mp.dps = 30`: too low for m_H ≳ 1e12 M_W (B1) |

Δr_H is "right only in some limit" for neither build. Both give 1.3e-37 against my route A at finite m_H and at three
(M_W, M_Z, α) points.

## 3. Mutants (task 3)

`make_mutants.py` builds 16 modules from build a by exact text patches; `run_gate_all.sh` runs
`python3 gate.py --mode verifier --campaign higgs_dr --oracle higgs_dr/oracle.py <mutant>` from rebuild/campaigns/ on
each (gate.py lives there, i.e. `../gate.py` seen from higgs_dr/). Each mutant dir has higgs_dr.py (with PROVENANCE),
DERIVATION.md and MUTANT.txt. A mutant whose error changes the asymptotics gets a log_coefficient computed from its own
Δr, so a mismatch in B alone cannot kill it. Outputs are in `mutants/*/gate_out.txt` and `run_gate_all_out.txt`.

| mutant | what is wrong | verifier gate | killed by |
|---|---|---|---|
| M00 control | nothing | PASS (correct) | |
| M01 | Goldstone loop: sign of the q² term in Δ(x) flipped (B00 only) | killed | coeff, finite, other masses, raw, constant, extreme |
| M02 | B00 without its "+1" (A0 keeps it) | killed | **raw only** |
| M03 | Δr: s²/c² instead of c²/s² | killed | 5 oracle checks |
| M04 | Π_W(M_W²) → Π_W(0) in the mixing bracket | killed | 5 oracle checks |
| M05 | seagull doubled (−A0/2) | killed | **raw only** |
| M06 | MS instead of MS-bar (ln4π − γ_E kept) | killed | **raw only** |
| M07 | 4D tensor reduction k^μk^ν → g k²/4 (B00 "+1" → "+1/2") | killed | **raw only** |
| **M08** | Δr_rel switches to the exact heavy-Higgs asymptote above m_H = 6 TeV (2.4e-4 off at 7 TeV) | **SURVIVES** | — |
| **M09** | σ_W, σ_Z take g², c² from the module defaults, ignoring α, M_W, M_Z (67% off at 3α) | **SURVIVES** | — |
| M10a | Δ(x) uses \|q²\| for spacelike q² | killed | raw (q² = −3M_W²) |
| **M10b** | Goldstone q² sign flipped only for q² < −5M_W² | **SURVIVES** | — |
| M11 | sign of [Π_W(M_W²) − Π_W(0)]/M_W² flipped | killed | 5 oracle checks |
| M12 | χ given mass M_W in the Z's H-χ loop | killed | 6 checks |
| M13 | overall sign of the H-Goldstone loop flipped | killed | 6 checks |
| M14 | all finite "+1" constants dropped | killed | **raw only** |
| M15 | H-V loop with M_W² for the Z too | killed | 7 checks (including the blind sign check) |

**3 of 15 wrong mutants survive.** Some coverage notes:

* M02, M05, M06, M07 and M14 change only m_H-independent or common terms: the m_H²-proportional terms of Π_W/M_W² and
  Π_Z/M_Z², and constants. The observable cannot see them, and only `raw_check` kills them. That is correct physics,
  since Δr_rel is insensitive to them. But it means the raw check alone carries the SPEC §2 convention (the O(ε) of 1/d,
  the seagull normalisation, MS-bar). Any widening of the raw check (M09, M10b) is therefore essential, not cosmetic.
* M08: the oracle covers m_H = 10…5000 GeV and then 1e6…1e14 M_W, and the blind slope check sits at 1e5–1e6 M_W. Nothing
  tests between 5 TeV and 8e7 GeV, or below 10 GeV.
* M09: `raw_check` runs only at the campaign inputs, and the α-linearity blind check tests only Δr.
* M10b: `raw_check` has five q² points in [−3M_W², M_Z²]. Deep spacelike q² and q² between M_Z² and threshold are untested.

## 4. Proposed checks (`audit_proposed_checks.py`)

All are functions m → (bool, msg). The list is `CHECKS`; run with `python3 audit_proposed_checks.py <dir> ...`.
The output is in `AUD/proposed_checks_out.txt` and `AUD/proposed_checks_out_rawwide_v2.txt`.

| check | tier | what | a | b | M00 | M08 | M09 | M10b |
|---|---|---|---|---|---|---|---|---|
| B_sigma_alpha_linear | blind | Π ∝ α at fixed masses, W and Z, three q² | PASS | PASS | PASS | PASS | **FAIL** (0.67) | PASS |
| B_sigma_coupling_scaling | blind | Π_W depends on M_Z only via 1/s², Π_Z on M_W only via 1/(s²c²) | PASS | PASS | PASS | PASS | **FAIL** (0.40) | PASS |
| O_dense_mH | oracle | Δr_rel vs reference at m_H = 1, 3, 7e3, 2e4, 1e5, 5e5, 3e6, 2e7 GeV, two μ, 1e-9 | PASS (0 ulp) | PASS | PASS | **FAIL** (2.4e-4) | PASS | PASS |
| O_raw_wide | oracle | raw Π_W, Π_Z at three (M_W, M_Z, α), q² = −500, −50, −7, 0.25 M_W², 1.6 M_Z², 0.95(m_H+M_W)², 1e-9; non-real = fail | PASS (4e-16) | PASS (2e-16) | PASS | PASS | **FAIL** (0.42) | **FAIL** (non-real) |
| H_own_precision_extreme | hygiene | extreme_mass_check with the module re-executed after resetting the global mpmath precision | PASS (1.8e-12) | **FAIL** (4.0e-4 at 1e14 M_W) | PASS | PASS | PASS | PASS |

The four physics checks kill every survivor and pass both builds. The hygiene check is meant to fail build b, because it
exposes B1/C1. The simpler fix is the oracle side: make `reference_dr.py` use `mp.workdps(40)` locally instead of
setting the global `mp.mp.dps`. With that patch (`AUD/oracle_isolated/`, a 6-line diff) the unchanged
`extreme_mass_check` fails b and passes a (`AUD/gate_isolated_oracle_{a,b}.txt`).

## 5. Findings

| id | class | finding |
|---|---|---|
| R0 | R | **None found.** The reference agrees with analytic PV (7.8e-40), with the dispersion relation (1.2e-10), with the 4D Euclidean momentum integral (≤6e-12; Δr_rel itself ≤4e-13) and with the higgs_rho reference at q² = 0. B = 11α/(48πs²) and C_INF are confirmed, and the literature "−5/6" constant holds exactly at μ = M_W. |
| C1 | C (oracle hygiene) | `reference_dr.py` sets the global `mp.mp.dps = 40` on import. This changes the working precision of the build under test and masks precision defects (it masked B1). Fix: local `mp.workdps`, or reset the precision before each oracle call. Proposed: H_own_precision_extreme. |
| C2 | C (coverage) | m_H gap 5 TeV … 8e7 GeV (and < 10 GeV). M08 survives. Fix: O_dense_mH. |
| C3 | C (coverage) | Raw self-energies are tested only at the campaign (M_W, M_Z, α). M09 survives. Fix: O_raw_wide, plus the blind B_sigma_alpha_linear and B_sigma_coupling_scaling. |
| C4 | C (coverage) | Raw q² grid has five points in [−3M_W², M_Z²]. M10b survives. Fix: O_raw_wide (deep spacelike, and between M_Z² and threshold). |
| B1 | B (build b, numerical) | Global 30-digit precision cannot resolve the m_H²/8 cancellation between Π_W/M_W² and Π_Z/M_Z² at m_H ≳ 1e12 M_W: 4e-8 at 1e12 M_W and 4e-4 at 1e14 M_W against a gate tolerance of 1e-8. It passed only through C1. The fix is ≥ 40 digits (as in a) or a local workdps, and b's DERIVATION should state the accuracy range. Also, b's breakpoints near x = 1 stop at 1e-18, below the M²/m_H² ~ 1e-28 scale at 1e14 M_W (harmless at 40 digits, but undocumented). |
| B2 | B (build b, low) | The H-φ⁺-W vertex is written without its factor i, and the loop's sign is fixed by a divergence-cancellation argument instead of the vertex phases. The result is correct, and the argument is legitimate as a consistency condition, but it is not a derivation of the sign from the Lagrangian as SPEC §1 asks. |
| B3 | B (build b, low) | Reality below threshold is shown only for q² ≤ M_V², not for q² < (m_H+M_V)². There is no threshold guard: the export raises a TypeError instead of a clear error. |
| N1 | N | Δr_rel is blind to the seagull normalisation, the "+1" constants and MS vs MS-bar (mutants M02/M05/M06/M07/M14). The SPEC §2 convention rests entirely on `raw_check`. That is fine by design, but the raw check must be wide (C3, C4). |
| N2 | N | Both builds reproduce the reference bit for bit (0 ulp), because all three use the same Feynman-parameter functions at ≥ 40 digits. Agreement with the oracle therefore says nothing about method independence; my routes A–C supply that. |
| N3 | N | Both builds' log_coefficient is a closed form typed from their own §4 expansion. This is legitimate (derived), and it is not caught by LINT_EXACT because it is built from the arguments. Their numerical slopes confirm it. |
| N4 | N | The task's gate command `python3 ../gate.py ... --campaign higgs_dr --oracle oracle.py` mixes two working directories. I ran the equivalent from rebuild/campaigns/: `python3 gate.py --mode verifier --campaign higgs_dr --oracle higgs_dr/oracle.py <dir>`. |

## 6. Verdict

* **Build a: accept as derived.** The rules, diagrams, Δr_H, B and constant are derived and correct. The numerics are
  self-contained (local workdps(40)). It passes the gate, the gate with an isolated oracle, and all my proposed checks.
* **Build b: physics accepted, build not acceptable as gated until B1 is fixed.** Its formulas are correct and agree with
  a to 0 ulp wherever b's own precision suffices. But it fails the campaign's own `extreme_mass_check` at its own
  precision, and its gate pass was an artefact of C1. After a one-line precision fix (local workdps ≥ 40) and a note on
  B2, b may be accepted as derived. If the campaign instead decides that m_H > 1e10 M_W is outside the physics, it must
  say so and relax extreme_mass_check. It should not rely on the oracle's side effect.
* **Campaign:** adopt the oracle precision fix (C1) and the four physics checks (C2–C4) before accepting future builds.
  The gate as shipped passes 3 wrong mutants out of 15.

## 7. Appendix: route-C output (`AUD/route_c_out.txt`)

```
G(q1=-3230, q2=-19383; M=MW, mH=50): 4D 2.48372424300245e+02  ref 2.48372424300122e+02  rel 5.0e-13
G(q1=-3230, q2=-19383; M=MW, mH=125.2): 4D 7.33018372015920e+01  ref 7.33018372015412e+01  rel 6.9e-13
G(q1=-3230, q2=-19383; M=MW, mH=400): 4D 7.41382897482933e+00  ref 7.41382897482435e+00  rel 6.7e-13
G(q1=-64609, q2=-6461; M=MW, mH=50): 4D -1.02417790855327e+04  ref -1.02417790855263e+04  rel 6.2e-13
G(q1=-64609, q2=-6461; M=MW, mH=125.2): 4D -3.89585577780139e+03  ref -3.89585577779773e+03  rel 9.4e-13
G(q1=-64609, q2=-6461; M=MW, mH=400): 4D -5.03594426513643e+02  ref -5.03594426513285e+02  rel 7.1e-13
G(timelike q1=M^2, q2=M^2/2; M=80.38, mH=125.2): 4D -4.00662215366995e+01  ref -4.00662215366792e+01  rel 5.1e-13
G(timelike q1=M^2, q2=M^2/2; M=80.38, mH=400): 4D -3.09496900348709e+00  ref -3.09496900346795e+00  rel 6.2e-12
G(timelike q1=M^2, q2=M^2/2; M=91.19, mH=125.2): 4D -6.72296074437062e+01  ref -6.72296074436725e+01  rel 5.0e-13
G(timelike q1=M^2, q2=M^2/2; M=91.19, mH=400): 4D -5.24956302198388e+00  ref -5.24956302195687e+00  rel 5.1e-12
Delta r_rel(mH=50): 4D -1.35436025840809e-03  ref -1.35436025840819e-03  rel 7.8e-14
Delta r_rel(mH=125.2): 4D 1.47748694563899e-03  ref 1.47748694563918e-03  rel 1.3e-13
Delta r_rel(mH=300): 4D 4.95127785463490e-03  ref 4.95127785463571e-03  rel 1.6e-13
Delta r_rel(mH=1000): 4D 1.06005042862148e-02  ref 1.06005042862190e-02  rel 4.0e-13
```

Scripts in AUD: `vertices.py`, `indep_routes.py`, `route_c.py`, `vs_higgs_rho.py`, `precision_b.py`, `make_mutants.py`,
`run_gate_all.sh`, `oracle_isolated/` (patched copy of the oracle side). Each has a matching `*_out.txt` or `gate_*.txt`.
