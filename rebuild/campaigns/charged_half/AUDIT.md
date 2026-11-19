# AUDIT: campaign charged_half (charged massless spin-1/2 emission, fluctuating hole charge)

Red-team auditor. In the repository I wrote only this file and `audit_proposed_checks.py`. All scripts and outputs are in
`S = /tmp/claude-0/-home-user-STUR-Physics-Lab/6f003c51-fc14-5da0-833a-45f53d6397be/scratchpad/audit-charged_half`.
The builds were run from copies in `S/copies/{a,b}`, with bytecode writing off. Mutants of build a are in `S/mutants/<name>/`.
Each mutant directory holds its verifier-gate output (`gate_stdout.txt`, `gate_report.json`), and the survivors also hold
`proposed_out.txt`.

Classification used below:
* **B**: a blocking error in the result or a postulate.
* **R**: should be revised. The result stands, but a claim or a check is wrong or misleading.
* **C**: a caveat to state with the result.
* **N**: noted, harmless.

## 0. Summary verdict

* **The numbers are derived and reproducible.** For the model the SPEC postulates, the weight ratio of the principal rule is
  0.963447 and its energy ratio is 0.995946.
  * Build a, the reference and my own chain (generator null vector, my own coupling code) agree to 1e-7 or better.
  * My independent Γ solver agrees with build a to ≤ 3e-8 at 35 points.
* **Every postulate of SPEC §§1–2 is correct.** I re-derived it from the covariant Dirac equation (§1).
* **The thermal postulate of SPEC §3 is the standard Gibbons–Hawking one, and it is correct for a fixed background charge.**
* **What is not derived is the O(α) answer itself.** The weight ratio is decided by the "rule", which runs from 0.927 to 1.054.
  * The rule is a back-reaction choice that the test-field model cannot fix.
  * The thermodynamically consistent rule is **(after, mid)**: the grey-body factor uses the final hole and the chemical
    potential is the exact entropy difference. It gives a weight ratio of **1.0077**, f = 0.1481. That is *not* Carr's 0.142.
  * The principal rule (after, after) matches 0.142/0.147. So does (before, mid), at 0.9691, which contradicts the oracle
    docstring.
  * **No rule reproduces the literature energy ratio** 4.18/4.22 = 0.9905. All nine give 0.9975–1.0044.
  * **Conclusion on Carr's numbers.** This campaign shows that a Page-type model *can* give f ≈ 0.142 with one particular
    O(α) assignment. It does not show that 0.142 is the physically right number.
* **The gate is weak outside the window it probes.** 7 of my 20 mutants that are genuinely wrong pass it (§4).
  * The five proposed checks kill all of them, and they pass build a.

## 1. Postulates, verified from first principles

### (a) Radial system — `S/derive_dirac.py` (sympy), output in the run log. **Confirmed.**

1. **Setup.** I used the Schwarzschild metric (−+++), the static diagonal tetrad and Christoffel symbols, with
   ω_μ^a_b = e^a_ν(∂_μ e_b^ν + Γ^ν_{μλ} e_b^λ). The spinor connection is Ω_μ = +¼ ω_μab γ^aγ^b.
   * The sign is *fixed* by requiring γ^ν = γ^a e_a^ν to be covariantly constant. All 16 (μ, ν) were checked; −¼ fails.
2. **Coupling.** I used iγ^μ(∇_μ − iqA_μ)ψ with A = −Φ dt, Φ = Q/(4πr), so D_t = ∂_t + iqΦ.
   * With ψ = r⁻¹f^{−1/4}sin^{−1/2}θ e^{−iωt+imφ}χ, the spin connection cancels **exactly**.
   * The potential enters only as ω → ω̃ = ω − qΦ = ω − g/r.
   * qΦ = (qe)(ne)/(4πr) = αqn/r in Heaviside–Lorentz units with α = e²/4π. So **g = αqn and the sign of g are right**:
     like charges repel, g > 0.
3. **Separation.**
   * The massless equation splits into Weyl blocks. Multiplying one block by √f σ₁ gives
     ∂_{r*} − iω̃σ₁ + (√f/r)K, with K = σ₁(σ₂∂_θ + imσ₃/sinθ).
   * K anticommutes with σ₁ and is Hermitian on L²(dθ). Its spectrum is ±(j + ½) for j ≥ |m|: a numerical check at
     m = ½, 3/2, 5/2 gives 1, 2, 3, 4… The finite-difference spectrum is doubled; that doubling is an artefact.
   * Substituting KY = λY symbolically gives (D − iω̃)R_a = −λ(√f/r)R_b and (D + iω̃)R_b = −λ(√f/r)R_a.
   * With R_− = R_a and R_+ = −R_b this is exactly SPEC §1, with **W = (j + ½)√f/r**.
   * The product of the two couplings is +λ², because K is Hermitian. This makes the system hyperbolic, so the flux is
     |R_−|² − |R_+|² and not a sum.
4. **Flux.** dJ/dr* = 0 symbolically, for real W and ω̃ of either sign.
5. **g = 0 limit.** Z₁ = R_+ + R_− obeys Z'' + (ω² − W² − W')Z = 0 and Z₂ = R_+ − R_− obeys
   Z'' + (ω² − W² + W')Z = 0. **V = W² ± dW/dr* is confirmed.**
6. **Horizon condition.**
   * Near the horizon, W → 0 and the R_+ equation reads (∂_{r*} − ∂_t − iqΦ)R_+ = 0. So R_+ propagates along v = t + r*,
     inward, *whatever the sign of k_H = ω − g/2*. R_− propagates outward.
   * In my Frobenius expansion the two indicial exponents of R_− are (r−2)^{−2ik_H} (driven by R_+, R_− ∝ √f) and
     (r−2)^{+2ik_H}. The second is the outgoing wave from the past horizon.
   * The gauge with A_t(∞) = 0 is singular on the horizon. The transformation that removes it multiplies ψ by e^{iqΦ_H t},
     and the horizon frequency becomes k_H = ω − g/2.
   * So R_+ = e^{−i(ω−g/2)r*}, R_− = 0 is the "no flux from the white hole / regular in the future-horizon frame"
     condition for either sign of k_H. **SPEC §2 is correct.**
   * At the horizon J = −|R_+|² < 0 for every ω, so Γ = 1/|A_in|² ∈ (0, 1]. There is no fermionic superradiance, and that
     holds for 0 < ω < g/2 too.
   * *Not done symbolically:* the explicit boost to a Kruskal-regular tetrad, which multiplies the components by f^{∓1/4}.
     The argument above is the standard one, and the finite √f·f^{−1/2} combination is consistent with it.

### (b) Thermal postulate. **Confirmed for a fixed background charge.** C on the O(α) ambiguity.

* For a hole of fixed charge, Gibbons (1975) and Hawking give the expected number per mode as Γ/(e^{(ω−qΦ_H)/T} + 1), with
  qΦ_H = g/2 in the gauge A(∞) = 0. Sign check: like-sign charges (g > 0) are emitted more (μ > 0). This is the discharge
  direction.
* **In the band 0 < ω < g/2,** k_H < 0 and n_F > ½, with Γ ≥ 0 (above).
  * The formula is still right. These modes are the fermionic analogue of the superradiant band: Schwinger-like pair
    creation in the horizon field, which survives as T → 0 (n_F → 1).
* **Negative-ω modes of the q field are the antiparticle at energy |ω|.** By charge conjugation Γ_q(−ω) = Γ_{−q}(ω).
  * The occupation is 1 − n_F(−ω; μ) = 1/(e^{(|ω|+μ)/T} + 1), which is the antiparticle's formula with −μ.
  * Integrating ω > 0 for e⁻ and for e⁺ separately is therefore complete, with no double counting. For massless fields with
    A(∞) = 0 the split at ω = 0 is exact.

### (c) Horizon potential. **Confirmed.**

* r_h = 2, so qeΦ_H = αqn/2 = g/2 in units of 1/M.
* The Coulomb and the gravitational energies both scale as 1/r. Therefore g is independent of M.
* The Reissner–Nordström corrections are O(Q_G²/M²) = O(αn²/M²_Planck), negligible as the SPEC says.
* The entropy change at fixed M is ΔS = −2πQ_G² = −2παn², also independent of M. So the thermodynamic canonical weight is
  π_th(n) ∝ exp(−2παn²), as the task states. Check: Q²/(8πr_h)/T = αn²/4 · 8π = 2παn².

## 2. Independent Γ solver — `S/indep_solver.py`, `S/compare_gamma.py`, `S/compare_gamma.json`

**Method.** It shares nothing with reference_solver.py (amplitude variables in x = ln(r−2)) or with the builds' large-r series
of the full problem.
* It works with the unfactored R_±(r), integrated in ln r with DOP853 at rtol 1e-12.
* **Horizon:** a Frobenius series in s = √(r−2) for R_± = (r−2)^{−2ik_H}P_±(s), with 90 terms, summed at r = 2.25 (radius of
  convergence r = 4).
* **Large r:** matching to the *exact* flat-space massless Dirac–Coulomb solutions, which are Whittaker functions.
  * In-mode: R_+ = ρ^{−½}W_{½−iη, μ}(2iωρ). Out-mode: R_− = ρ^{−½}W_{½+iη, μ}(−2iωρ). Here ρ = r − 2, η = 2ω − g and
    μ² = k² − η² (complex when |η| > k).
  * In ρ the phase coefficient a = ω + η/ρ is exact. Only b = k/√(r(r−2)) ≈ k/ρ is approximated, with an O(k/ρ²) remainder.
  * The matching radius is R = max(1000, 4000/ω, 100k²/ω), and the error estimate is the change from R to 2R.
* The flux |A_in|² − |A_out|² = 1 holds to 1e-10. It is meaningless where Γ < 1e-12.

**Result at 35 points:**
* Coverage: g = −0.12…0.12 at 28 points, of which 10 have ω < g/2. j runs from ½ to 4.5. Seven more points go beyond the
  oracle's window: |g| = 0.3 and 0.6, and j = 5.5, 6.5, 9.5.
* **Build a vs mine: ≤ 2.8e-8 everywhere, typically 1e-9.** This includes Γ = 1.9e-13 and 5.2e-17 at ω < g/2.
* **Reference vs mine: ≤ 1e-7 except three low-ω points with ω < g/2.** Those are 1.1e-7 at (½, 0.012, 0.03), 2.6e-7 at
  Γ = 1.9e-13 and 4.2e-7 at Γ = 5.2e-17.
  * The 1.0e-7 "worst deviation" the oracle reports for build a at (½, 0.02, 0.05) is the reference's error, not a's
    (**N**: well inside the 2e-6 tolerance).
* On the greybody g = 0 references: 4e-9 – 7e-11 (mine).
* **Build b vs mine:** worst 6.9e-7, at (½, 0.25, 0) (S/copies/b/proposed_out.txt). This is consistent with the
  b correction that is in progress.

## 3. Charge process and rules — `S/chain_analysis.py`, output `S/chain_analysis.txt`

Derivatives come from build a's rates at g = 0. My own chain solves Qᵀπ = 0 by linear algebra, with |n| ≤ 60.

* **Derivatives at g = 0.**
  * d ln N/dg_gb = −6.304 and d ln N/dg_μ = +12.087; the latter is 4π⟨1 − n_F⟩.
  * Along the diagonal, L = d ln N(g, g)/dg = 5.782.
  * P_gb/P0 = −5.356, P_μ/P0 = 12.297, P_dd/P0 = 42.69.
* **The stationary distribution is not the thermodynamic one, and it should not be.**
  * The emission-only chain gives π ∝ exp(−Lαn²) to leading order, the same for every rule: the first-order shifts cancel
    in up(n)/down(n+1). Its ⟨n²⟩ is 1/(2Lα) = 11.85; the full chain gives 11.81–11.88.
  * The canonical expectation exp(−2παn²) gives ⟨n²⟩ = 10.905. At n = 10, π(n)/π(0) is 0.0145 against 0.0102.
  * An isolated hole radiating into vacuum is not in equilibrium with a bath, so nothing forces L = 2π. The near-equality
    (5.78 against 6.28) is a coincidence. With Boltzmann statistics d ln N/dg_gb = −6.373, not −2π (`S/boltzmann_L.py`).
  * **C:** the SPEC's π(n) is a kinetic, not a thermodynamic, distribution. It is ~8 % wider in ⟨n²⟩.
* **Which rule is thermodynamically consistent.** Put the hole in a bath at T, μ = 0, where emission and absorption must obey
  detailed balance.
  * Per mode, emission n → n′ = n − q is Γ n_F(1 − n_b) and absorption n′ → n is Γ′(1 − n_F′)n_b. Their ratio must be
    e^{S(n′) − S(n)}, with S(n′) − S(n) = −ω/T − 2πα(n′² − n²) = −(ω − μ*)/T. Here μ* = qeΦ_H is evaluated at the
    **midpoint** charge n − q/2, since 2πα(n′² − n²)·T = −αq(n − q/2)/2.
    * The step is exact here because S is quadratic in n, so ∫Φ dQ uses the midpoint.
  * This fixes **r_μ = mid**. With r_μ = before or after, the electron and positron channels between n and n+1 give
    different ratios: e^{−4παn} and e^{−4πα(n+1)}. Hence there is a steady charge-separated current in an equilibrium bath,
    which violates the second law.
  * Microscopic reversibility also requires the grey-body factor of the emission to be the absorption probability of the
    reverse process. The particle is absorbed by the *final* hole n′, so **r_gb = after**.
  * The thermodynamically consistent rule is therefore **(after, mid)**. Its weight ratio is **1.0077** and its energy ratio
    0.9967.
  * The principal rule (after, after) takes the chemical potential at the final charge. That misplaces μ by α/4 and
    suppresses each emission by ≈ e^{−2πα} ≈ 0.955.
* **All nine rules at α.** Build a and my chain agree to < 1e-9. "1st-order" is the expansion below.

| rule (gb, μ) | weight ratio | energy ratio | ⟨n²⟩ | 1st-order WR | (WR−1)/α at α, α/4 |
|---|---|---|---|---|---|
| before, before | 1.013553 | 1.004392 | 11.883 | 1.01347 | 1.86, 1.85 |
| before, mid | **0.969086** | 1.003595 | 11.852 | 0.96860 | −4.24, −4.29 |
| before, after | 0.926534 | 1.002823 | 11.823 | 0.92373 | −10.07, −10.35 |
| mid, before | 1.033553 | 1.000961 | 11.878 | 1.03301 | 4.60, 4.54 |
| mid, mid | 0.988218 | 1.000166 | 11.848 | 0.98814 | −1.62, −1.62 |
| mid, after | 0.944835 | 0.999395 | 11.818 | 0.94328 | −7.56, −7.72 |
| after, before | 1.053892 | 0.997509 | 11.873 | 1.05256 | 7.39, 7.25 |
| **after, mid** (consistent) | **1.007675** | 0.996715 | 11.842 | 1.00769 | 1.05, 1.05 |
| **after, after** (principal) | **0.963447** | 0.995946 | 11.813 | 0.96282 | −5.01, −5.07 |

* **Small-α expansion (mine, it agrees with a's DERIVATION §5.5 for the principal rule).**
  * Every coupling is g = αqn − αs (s = 0, ½, 1 for before, mid, after), so
    **WR ≈ 1 + α[P_dd/(4LP0) − s_gb P_gb/P0 − s_μ P_μ/P0] = 1 + α[1.846 + 5.356 s_gb − 12.297 s_μ]**.
  * The same expansion gives **ER ≈ 1 + α[0.602 − 0.948 s_gb − 0.210 s_μ]**.
  * The charge-fluctuation part (+1.85α) is rule-independent. Everything else is the O(α) self-interaction shift.
  * The rule spread is ±6 %, the same order as the effect itself. **C, strongly:** the sign of the effect is model-dependent.
* **Literature windows** (3-digit rounding): weight [0.9593, 0.9727], energy [0.9882, 0.9929].
  * The weight window contains **two** rules, (after, after) and (before, mid).
  * The energy window contains **none**. From the expansion, the most negative ER reachable with s ≤ 1 is
    1 − 0.556α = 0.9959. Reaching 0.9905 would need ER − 1 = −1.30α, which is impossible within this model family.
  * So the 4.18 T of the literature cannot come from this model, under any rule, with massless leptons.
  * Plausible sources I could **not** check (the APS page is not reachable from this session): electron rest-mass effects
    in Page's holes; a different definition of the mean energy; or a different treatment of the charge.
  * The neutral mean energy here is P0/N0 = 4.2346 T, which is not 4.22 either. That is suggestive of a different
    definition or a rounding of a different computation.
* **Page 1977 (abstract only, from a search result).** It says "the attraction between an emitted particle and its
  antiparticle … and the charge fluctuations make the average emission rate and power somewhat lower … a few percent".
  * This fits a final-charge (after) self-attraction. It does not tell which μ rule Page used.

## 4. Mutants of build a — verifier gate (`python3 gate.py --mode verifier --campaign charged_half --oracle charged_half/oracle.py <dir>`)

Twenty mutants were made by `S/make_mutants.py` (the exact old→new strings are there) and run by `S/run_mutants.sh`, four at a time.
"P" in the last column means the proposed checks of `audit_proposed_checks.py`.

| # | mutant (build a) | wrong? | gate | killed by | P |
|---|---|---|---|---|---|
| M01 | g → −g in the ODE phase 2(ωr* − g ln(r−2)) | yes | **killed** | oracle Γ, rates, ratios | – |
| M02 | chemical potential g/2 → g | yes | **killed** | oracle rates, ratios | – |
| M03 | n_after = n + 1 for both species (positron mapping wrong) | yes | **killed** | blind symmetry, oracle ratios | – |
| M04 | (2j+1) dropped | yes | **killed** | blind neutral size, oracle | – |
| M05 | occupation without g/2 (no μ) | yes | **killed** | blind "N increases with g_μ" (N is then flat). The run did not finish: the anti-restoring chain runs away and hit the per-check timeout | – |
| M06 | rates drop the band ω < g_gb/2 | yes | **killed** | oracle rates, ratios, π | – |
| M07 | Γ uses 1.05 g when \|g\| > 0.125 (beyond the oracle window) | yes | **survives** | – | killed (Γ wide 3e-2, rates self-consistency 8e-2) |
| M08 | Γ × 0.98 for j ≥ 4.5 (k ≥ 5) in transmission() | yes | **survives** | – | killed (Γ wide 2e-2) |
| M09 | chain built with the μ-rule coupling also for the grey-body (rates right) | yes, for mixed rules: ⟨n²⟩ off 5e-4 | **survives** | – | killed (mixed-rule detailed balance 4.5e-4) |
| M10 | rule tuple read as (r_μ, r_gb) | yes | **killed** | oracle (after, mid) | – |
| M11 | Boltzmann occupation | yes | **killed** | oracle rates, ratios | – |
| M12 | power weighted by ω − g_μ/2 | yes | **killed** | oracle rates, ratios | – |
| M13 | KMAX = 3 partial waves | numerically under-resolved: rates off 1.4e-5–1.8e-5, ratios unaffected | **survives** (inside the 3e-5 rates tolerance) | – | killed (rates self-consistency 1.8e-5 > 1e-6) |
| M14 | g → −g only in the out-mode asymptotic series | yes | **killed** | oracle Γ | – |
| M15 | "mid" for the grey-body coupling silently treated as "before" | yes | **killed** | oracle (mid, mid) | – |
| M16 | Γ = 1 for ω > 1.2 | yes (up to 1e-4 at j = 4.5) | **survives** | – | killed (Γ wide 9.2e-5) |
| M17 | the five unchecked mixed rules have their entries swapped | yes (ratios off up to 0.13) | **survives** | – | killed (nine rules, mixed balance, small-α structure) |
| M18 | rates() clip g_gb to ±0.25 | yes, for \|g_gb\| > 0.25 | **survives** | – | killed (rates self-consistency 0.31) |
| M19 | n_F halved for ω < g_μ/2 | yes | **killed** | oracle rates | – |
| M20 | Γ(ω < g/2) computed with g → 2ω | yes | **killed** | oracle Γ | – |

* **Tally.** 13 of 20 are killed by the gate. All 7 survivors are genuinely wrong, though M13 is wrong only numerically.
  * The survivors sit outside the oracle's probes: |g| > 0.12, j ≥ 4.5, ω > 0.8 at j ≤ 3.5, the five mixed rules
    (before, mid), (before, after), (mid, before), (mid, after) and (after, before), and mixed-rule distributions.
    They also exploit the gate never checking rates() against the build's own transmission().
  * None of them changes the principal result. The campaign's headline number is well protected; its other exports are not.
* **Proposed checks** (`audit_proposed_checks.py`; run with `python3 audit_proposed_checks.py <build dir>`, about 10 min
  cold). They **kill all 7 survivors**.
  * Build a passes, with margins: Γ 2.8e-8 against 1e-6; rates 8.4e-11 against 1e-6; nine rules 3.9e-8 against 3e-4;
    balance 1.8e-15; slope 0.05 against 0.15.
  * The current copy of build b passes, but its margins are thin: Γ 6.9e-7 and rates 2.0e-7, both against 1e-6.
  * `S/proposed_a.txt` is a's run, made before I tightened the rates tolerance from 2e-5 to 1e-6. a's value, 8.4e-11, passes
    either way.


## 5. Findings

* **R1 — the oracle docstring is wrong about uniqueness.** It says "the literature ratio is reproduced within its quoted
  digits by the principal rule only". (before, mid) gives 0.96909, which is also inside the window [0.9593, 0.9727].
* **R2 — the principal rule is not the thermodynamically consistent one (§3).**
  * The consistent rule is (after, mid): r_μ = mid follows from detailed balance, and r_gb = after from reversibility.
    It gives a weight ratio of **1.0077** (f ≈ 0.148), not 0.963.
  * So "f = 0.1416 reproduces Carr's 0.142" holds only under an O(α)-inconsistent μ assignment.
  * Either state this in the result, or promote (after, mid) as the physically preferred value with (after, after) as the
    literature-matching variant.
* **R3 — the literature energy ratio 0.9905 is not reproduced by any rule.**
  * The range over all rules is 0.9975–1.0044, and the first-order bound is ER ≥ 1 − 0.556α.
  * The neutral ⟨E⟩ = 4.2346 T is not 4.22 either.
  * The oracle and the campaign text should say that 4.18/4.22 is *not* reproduced and cannot be in this model.
* **R4 — the gate's coverage is narrow** (§4): 7 genuinely wrong mutants survive. Adopt `audit_proposed_checks.py`, or
  equivalent checks.
* **C1 — the size and sign of the effect are model-dependent.**
  * The fluctuation part is +1.85α. The rule-dependent self-interaction part, 5.36 s_gb − 12.30 s_μ (times α), dominates
    and spans 0.927–1.054.
  * Self-energy and image-charge corrections are of the same order and are not in the SPEC.
* **C2 — the stationary distribution is kinetic, not thermodynamic.** ⟨n²⟩ is 11.81, against 10.905 for exp(−2παn²);
  L = 5.78 against 2π.
* **C3 — the reference solver's accuracy is about 1e-7 at low ω below g/2, up to 4e-7 for Γ < 1e-12.**
  * This is enough for the 2e-6 oracle tolerance.
  * The reported "worst 1.0e-7" for build a at (½, 0.02, 0.05) is the reference's error.
* **C4 — reference_chain.py polynomial-extrapolates Γ(g) beyond its Chebyshev nodes (|g| ≤ 0.12).** Its chain uses up to
  |g| ≈ 0.23 (n ≤ 30).
  * Those states carry π < 1e-5, and the effect on ratios is < 1e-7 (build a, which tables to |g| = 0.25 and solves
    beyond, agrees to 4e-8).
  * Harmless, but not stated.
* **N1 — dead-code obfuscation in the orchestrator's scripts.**
  * reference_solver.py:35 has `... if False else ... * 0 + 1/(1 + |b|²)`, and chain.py:33 has `if False else`.
  * chain2.py cannot run rule "mid" for the grey-body (KeyError).
  * The returned value is right. Clean it up.
* **N2 — Build a.**
  * DERIVATION, PROVENANCE and the code agree. I found no hidden answers and no argument-dependent branches.
  * Its Γ is accurate to ~1e-8 even outside the oracle's window.
  * It clips Γ to [0, 1] (`_transmission_cached`), which blinds `b_range`. That has no numerical effect.
* **N3 — Build b (current copy).** It is inside every proposed tolerance, with Γ errors up to 6.9e-7. I did not audit b's
  pending correction.
* **No B findings.** I found no error in the postulates, the code of build a, or the reference that changes the stated
  result *for the model as specified*.

### Verdict

* **The result is derived.** For the SPEC model, weight ratio 0.96345 and energy ratio 0.99595 (principal rule) are derived
  numbers, reproduced by three independent codes. My Γ solver is the third independent Γ method.
* **The result is strongly model-dependent at the very order it is about.**
  * The test-field model leaves the O(α) charge assignment free, and that assignment moves the weight ratio by ±6 %.
  * The one assignment that thermodynamics selects, (after, mid), gives f ≈ 0.148 for charged leptons, essentially the
    neutral 0.147.
* **About Carr's 0.142.**
  * It is reproducible by a Page-type model with the "after" assignment for both Γ and μ. It is also reproducible by
    (before, mid).
  * Neither is singled out by first principles.
  * The companion number 4.18 T is not reproduced by any assignment.
  * I therefore regard 0.142 as **consistent with, but not derived by,** this campaign. Its residual against the neutral
    value lies within the O(α) systematic.


## 6. What I could not verify

* Page 1977 itself: the paper is not accessible here (link.aps.org is not allowed). So I could not check which rule, which
  occupation, or which lepton mass produced 0.142 and 4.18 T, or whether 0.142 is per helicity state.
* The Kruskal-frame regularity, done explicitly with the boosted tetrad (argued in §1a, not computed).
* Self-energy / image-charge corrections, which are O(α) and outside the SPEC. They may move the answer as much as the rule
  does.
* Build b after its correction. The proposed checks were run on the current copy (`S/copies/b/proposed_out.txt`).
