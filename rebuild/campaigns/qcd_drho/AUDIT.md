# Red-team audit: qcd_drho (O(α_s) QCD correction to Δρ of the (t, b) doublet, pole and MS-bar top mass)

In the repository I wrote only this file and `audit_proposed_checks.py`. All scratch work is in
`S = /tmp/claude-0/-home-user-STUR-Physics-Lab/6f003c51-fc14-5da0-833a-45f53d6397be/scratchpad/audit-qcd_drho`:
* `goldstone.py` / `goldstone.log`: the independent Goldstone-route derivation (§1);
* `masters.py` / `masters.log`: the numerical check of the two-loop vacuum masters at non-integer d (§1c);
* `mass_relation.py` / `mass_relation.log`: the on-shell self-energy and m_pole/m̄ (§1d);
* `make_mutants.py`, `run_gates.sh`, `gates.log`, `mutants/<name>/` (each with `gate_stdout.txt`, `gate_report.json`, `proposed_out.txt`), and `mutants_extra/M23_hardcoded_numbers/` (§3);
* `checks_a.log`, `checks_b.log`: the proposed checks run on both builds.

The builds were gated from copies in `S/copies/{a,b}`. Nothing was written into `builds/` or `oracle.py`. A verifier gate run takes about 10 s (build a rebuilds c from the traces on the first call).

Classes, as in the sibling audits: **B** = a defect in a build. **R** = a SPEC wording or ambiguity issue. **C** = an oracle or check gap, or a caveat. **N** = a note or a positive result.

## 0. Verdict

* **Both builds are correct. I found no B finding.** An independent route gives the same coefficients to 30 digits:

  c_pole = −C_F (1/2 + π²/6) = −C_F (3 + π²)/6,  c_MS = C_F (3/2 − π²/6 + (3/2) ln(μ²/m̄²)).

  This route is the gaugeless-limit Goldstone route: Yukawa vertices, the q² derivative of the Goldstone self-energies, my own d-dimensional traces, and a numerical ε → 0 limit. PSLQ on 25 digits gives 6c + 3 + π² = 0 and 6c − 9 + π² = 0. For C_F = 4/3 the values are −2.85991 and −0.19325.
* **The oracle reference is right.** It was recalled by the orchestrator, not read from a page, and §1 confirms it independently, including the +2C_F scheme shift and the (3/2)C_F ln(μ²/m̄²) running term.
* **The gate pins only four real numbers** (§4): the one-loop normalisation, c_pole/C_F, c_MS(μ = m̄)/C_F and the log coefficient. Inside the window it samples, it pins them well: every physics mutant I made (wrong diagram, counterterm, ζ₂, trace or log) fails.
* **The gate is blind to the arguments around those numbers.** 7 of my 22 mutants of build a pass the full verifier gate:
  * 3 come from delta_rho_qcd being probed only at (N_C, C_F) = (3, 4/3);
  * 1 comes from the pole coefficient being probed only at μ/m = 1;
  * 3 are wrong only outside the sampled C_F, μ/m and N_C ranges.

  The 5 proposed checks kill all 7, and both builds pass them.
* **A hard-coded answer passes the gate (C5).** Mutant M23 types −(1/2 + π²/6) and 3/2 − π²/6 directly. Lint misses it because `LINT_EXACT` is empty and `LINT_TARGETS` holds only the C_F = 4/3 values. The fix is proposed in C5.

## 1. Independent derivation: the Goldstone route (task 1; `S/goldstone.py`)

### (a) Method

**Reduction to Goldstone wave functions.** In the gaugeless limit, the heavy-quark loop generates the effective Lagrangian Z₊|∂φ⁺ − iM_W W⁺|² + (Z₀/2)(∂φ⁰ − M_Z Z)². So M²_W,eff/(c² M²_Z,eff) = Z₊/Z₀, and Δρ = A₊ − A₀. Here q² + Π(q²) = q²(1 + A) + Π(0) + … is the inverse Goldstone propagator, with iΠ the sum of 1PI amplitudes. This is Barbieri et al.'s Δρ = Z_φ0/Z_φ+ − 1, where Z is the field constant, = 1/(1 + A).

**Vertices.** They come from −y_t Q̄_L Φ̃ t_R + h.c., with Φ = (φ⁺, (v + h + iφ⁰)/√2) and m_b = 0:
* charged: i y P_L for φ⁺ t̄ b and i y P_R for φ⁻ b̄ t, with y = √2 m₀/v;
* neutral: −(m₀/v)γ5 for φ⁰ t̄ t.

**Renormalisation.** I used bare perturbation theory. The bare mass m₀ appears both in the propagators and in the Yukawa coupling y₀ = √2 m₀/v; Z_y = Z_m because QCD does not touch Φ, and v gets no QCD renormalisation at this order. The counterterm is m₀ = m − δm in A⁽¹⁾ ∝ (m₀²)^{1−ε}, kept exact in d.

**Diagrams.** At one loop there is one diagram per Goldstone. At O(α_s) there are four per Goldstone, all in a general covariant gauge ξ:
* gluon self-energy insertion on line 1;
* gluon self-energy insertion on line 2;
* vertex gluon exchange, Feynman part;
* vertex gluon exchange, (1 − ξ) part.

Line 1 (the top) carries k and l, and line 2 carries k − q and l − q, so the gluon momentum k − l does not depend on q.

**Computation chain.**
* **Trace.** I wrote my own d-dimensional trace: a pairing recursion with open Lorentz indices that are contracted afterwards. It shares no code with the builds.
* **q expansion.** The q-dependent propagators are Taylor-expanded to O(q²), with q^μq^ν → q² g^{μν}/d.
* **Wick rotation and partial fractions.** After the rotation, partial fractions in K = k_E² separate the massive and massless lines.
* **Masters.** Two two-loop vacuum masters remain, J_mm0(a, b; c) and J_m00(a; b, c), both in closed Γ-function form (§1c).
* **The ε → 0 limit is taken numerically, not by series expansion.** The renormalised combination is evaluated with exact mpmath Γ functions at 150 digits, at ε = 10⁻⁶, 10⁻¹² and 10⁻³⁰.

**Differences from the builds.**
* **Build a** used vector and axial current correlators, the relation Π_A(m₁, m₂) = Π_V(m₁, −m₂), and Π(m, 0) − Π(m, −m)/4.
* **Build b's second route** (its DERIVATION §8: Taylor-expanded scalar correlators through the vector Ward identity) is the closest to mine. Mine still differs:
  * the vertices are chiral Yukawa (P_L/P_R and γ5), not V/A currents;
  * there is no Ward identity and no (m₁ − m₂)² factor;
  * the flavour bookkeeping is different (φ⁺ against φ⁰).

### (b) Results (`goldstone.log`)

| Quantity | Auditor | Builds / oracle |
|---|---|---|
| one-loop A₊ − A₀ | 1.000000 × N_C m²/(16π² v²) = N_C G_F m²/(8√2 π²), positive | same |
| c_pole/C_F, ε = 10⁻⁶ / 10⁻¹² / 10⁻³⁰ | −2.144935155 / −2.144934067 / −2.14493406684822643647241516665 | −(1/2 + π²/6) = −2.14493406684822643647241516665 |
| c_MS(μ = m̄)/C_F | −0.144934066848226436472415166644 | 3/2 − π²/6 |
| PSLQ on [c, 1, π²] | pole [6, 3, 1]; MS [6, −9, 1] | (3 + π²)/6, (9 − π²)/6 |
| d(c_MS/C_F)/d ln(μ²/m̄²) at L = 1, −2, 5.5 | 1.5 (exact to 25 digits) | 3/2 |
| c_pole at L = 1, −2, 5.5 | unchanged to 25 digits (μ-independent) | μ-independent |
| ξ = 0, 1, 3, −7 | c_pole and c_MS identical to 25 digits | ξ-independent |
| Goldstone theorem, bare, ε = 0.1 and 0.37, ξ = 1 and 0.4 | Π₊(0) − Π₀(0) = 0 at one and two loops (≤ 10⁻¹⁵, with Π₀(0) ~ −2500) | (not in builds) |

* **Pole cancellation.** The 1/ε², 1/ε and overall poles cancel: the value at ε = 10⁻⁶ differs from the limit by O(ε). The overall divergence cancels between A₊ and A₀, each of which diverges separately. The subdivergences cancel against the m₀ counterterm. Its O(ε) part (2 − 2ε) multiplies the 1/ε of A⁽¹⁾, so it matters, as in both builds.
* **The Goldstone-theorem identity is a non-trivial check.** It ties the normalisation of the neutral (γ5γ5) diagrams to the charged (P_L ⋯ P_R) diagrams, exactly in d and for any ξ. A wrong vertex/self-energy weight or a γ5 inconsistency in one sector would break it.

### (c) Master integrals (`S/masters.py`)

I integrated J_mm0 and J_m00 directly in d dimensions:
* radial k and l, with the relative angle done in closed form by a ₂F₁;
* that angular formula is itself checked against quadrature to 10⁻¹⁶;
* scipy double quadrature for the radial part.

**Coverage:** 32 points at d = 2.7, 3.3, 3.8 and 4.0, with non-integer indices (a, b, c), e.g. (2.5, 1.5, 0.8) and (2.2, 2, 0.6) for J_mm0 and (2; 1.2, 0.9) and (2.5; 0.7, 1.4) for J_m00.

**Result:** the worst relative deviation from the closed forms is 1.3·10⁻¹².

The integer and negative indices that the reduction uses follow by analytic continuation in the indices. Both sides are meromorphic and agree on an open set, so they agree everywhere. Both builds use the same closed forms, and they checked only 4 to 5 points at d = 4 (build a) or d = 3, 4 (build b).

### (d) Top-mass relation (`S/mass_relation.py`)

**Derivation.** I derived the on-shell self-energy with Feynman parameters (on shell, Δ = x²m²):

  Σ_OS/m = (α_s/4π) C_F Γ(ε) e^{γε}(μ²/m²)^ε [(2 − d)(1/(1 − 2ε) − 1/(2 − 2ε)) + d/(1 − 2ε)] = (α_s/4π) C_F [3/ε + 4 + 3L].

The builds used a different formula, the on-shell master O(a, b).

**Gauge independence of the pole mass, analytically.** On shell, the (1 − ξ) part of the numerator reduces to (D₁ − q²)/(2m q⁴), where q is the gluon momentum and D₁ = k² − m². After the shift k = p − q, both terms are massless and scaleless, so they vanish identically in dimensional regularisation.

**Results.**
* m_pole = m̄(μ)[1 + C_F (α_s/π)(1 + (3/4) ln(μ²/m̄²))], hence (m_pole/m̄)² − 1 = C_F a (2 + (3/2)L).
* This is exactly c_MS − c_pole (per C_F) that both builds and the oracle use.
* The MS-bar Z_m = 1 − 3C_F α_s/(4πε) gives d ln m̄²/d ln μ² = −(3/2)C_F a. This cancels the +(3/2)C_F L of c_MS, so the MS-bar Δρ is μ-independent at O(α_s).

### (e) The physics claims the task asked me to check

* **γ5 anticommutation is safe at this order.** This rests on an argument plus one numerical consistency check, not on a 't Hooft–Veltman computation.
  * The neutral trace has two γ5 on the single closed loop. They are eliminated with {γ5, γ^μ} = 0 and γ5² = 1, so no γ5 trace is ever evaluated. The known NDR inconsistency, Tr[γ5γ^aγ^bγ^cγ^d] ≠ 0 against cyclicity in d dimensions, enters only through odd-γ5 traces.
  * The charged trace Tr[P_L X P_R Y] (X odd, because b is massless) gives ½Tr[XY] + ½Tr[Xγ5Y]. The odd piece is ε^{μνρσ} contracted with at most three independent vectors (k, l, q), so it is 0 in any consistent scheme.
  * At O(α_s) there is no triangle or anomaly subgraph.
  * Supporting evidence: the exact two-loop Goldstone identity Π₊(0) = Π₀(0) mixes the γ5γ5 and chiral-projector sectors, and the builds' V/A-current route agrees with my Yukawa route.
  * Not done: an HV/BM computation with Larin's finite renormalisation of the pseudoscalar density.
* **N_C appears only as the overall factor.** Every O(α_s) diagram is a single quark loop with one gluon exchange, with colour factor Tr(T^aT^a) = C_F N_C. Diagrams in which a gluon joins two quark loops vanish (Tr T^a = 0), and gluon or ghost loops start at O(α_s²). So c is C_F times a pure number, and the auditor's code has no other colour factor.
* **A massless b gets no counterterm.** With m_b = 0 the b self-energy is ∝ p̸ (chiral symmetry), so δm_b ∝ m_b = 0. The Yukawa of b is zero as well. In bare perturbation theory no field counterterm is needed, so the b self-energy insertion is computed and contributes. It is not scaleless, because the same k flows through the massive top line.
* **Gauge independence.** The ξ-part of Σ_OS is scaleless, as shown in §1d. Numerically, c is ξ-independent to 25 digits at ξ = 0, 3, −7. The physical reason: Δρ is a ratio of low-energy amplitudes of colour-singlet operators (currents or Goldstone kinetic terms), and the pole mass and the MS-bar Z_m are gauge invariant.

### (f) What is independent and what is shared

**Independent of the builds:**
* the route: Goldstone kinetic terms with Yukawa/chiral vertices, not V/A currents and not the Ward-identity scalar route;
* all code: trace engine, q expansion, reduction, Σ_OS by Feynman parameters;
* the ε → 0 limit: numerical with exact Γ functions, instead of the builds' symbolic Laurent series;
* the numerical check of the masters at non-integer d.

**Shared with the builds and the orchestrator:**
* **The SPEC's definition of Δρ** (q² = 0, the gaugeless limit, M_Z²c² = M_W²).
* **The gaugeless-limit equivalence Δρ = A₊ − A₀.** This is the standard Barbieri et al. effective-Lagrangian argument. I did not derive the gauge-boson/Goldstone Ward identity at two loops. It is confirmed at one loop (§1b), and the agreement at O(α_s) with the builds' current route is the two-route check.
* **Conventions:** dimensional regularisation with NDR γ5, MS-bar with g₀² = 4πα_s μ^{2ε}(e^γ/4π)^ε, and the m₀^{2−2ε} counterterm scaling (elementary).
* **The closed forms of the masters**, which I re-verified numerically.
* **Prior knowledge.** Like the builders, I knew the textbook result (−2.86 for C_F = 4/3) beforehand. No target number is typed into `goldstone.py`: c is produced by the diagrams and identified afterwards by PSLQ.

## 2. Build-specific notes

* **N1. Both builds produce c from the diagrams.** Neither types the number in. Build a prints an interesting decomposition: Γ(1+ε)²[2/ε² + 5/ε + 17/2] + Γ(1+2ε)Γ(1−ε)Γ(1+ε)[−2/ε² − 5/ε − 21/2]. So the whole π² comes from the (m, 0, 0) signature of the charged correlator. I did not use this decomposition. My route reaches the same number with a different integrand.
* **N2. The γ5 justification is the same as mine.** Both builds rely on Π_A(m₁, m₂) = Π_V(m₁, −m₂) (the ψ → γ5ψ redefinition) and on the vanishing of the VA interference. This is the same even-count argument as §1e. It is not an independent check of NDR, and neither is mine.
* **N3. Build a's on-shell master is unchecked by build a; §1d checks it.** Build a's O(a, b) on-shell formula has no numerical check in build a (its DERIVATION §10 says so). My Feynman-parameter Σ_OS confirms its finite part 4 + 3L.

## 3. Mutants of build a (task 2)

Each mutant is one or two exact text substitutions of `builds/a/qcd_drho.py`, written by `S/make_mutants.py`. Each was run with `python3 gate.py --mode verifier --campaign qcd_drho --oracle qcd_drho/oracle.py <dir>` from `campaigns/`, and then with `audit_proposed_checks.py`.

| Mutant | Error | Gate | Killed by (gate) | Killed by (proposed) |
|---|---|---|---|---|
| M01 | vertex diagram with the wrong sign | FAIL | coeff, total | wide, colour, scheme |
| M02 | self-energy insertion on line 2 dropped | FAIL | coeff, total | wide, colour, scheme |
| M03 | mass-counterterm sign flipped (both schemes) | FAIL | coeff, total | wide, colour, scheme |
| M04 | counterterm factor 2 instead of 2 − 2ε (dropped O(ε) × 1/ε term) | FAIL | coeff, total | wide, colour |
| M05 | counterterm factor 1 − ε (m instead of m² scaling) | FAIL | coeff, total | wide, colour, scheme |
| M06 | ζ₂ dropped from the Γ(1 + cε) expansion | FAIL | coeff, total | wide, colour |
| **M07** | delta_rho_qcd uses C_F = (N_C² − 1)/(2N_C), ignoring the C_F argument | **PASS** | – | colour, scheme |
| **M08** | delta_rho_qcd uses C_F = 4/3 | **PASS** | – | colour, scheme |
| M09 | MS-bar log coefficient halved (ln(μ/m) for ln(μ²/m²)) | FAIL | coeff, total | wide, colour, scheme |
| M10 | MS-bar log sign flipped | FAIL | coeff, total | wide, colour, scheme |
| M11 | scheme shift with the wrong sign (c_MS = c_pole − 2C_F + …) | FAIL | coeff, total | wide, colour, scheme |
| **M12** | pole coefficient carries the MS-bar log (μ dependence in the pole scheme) | **PASS** | – | wide, pole-μ |
| M13 | scheme argument ignored (always pole) | FAIL | coeff, total | wide, colour, scheme |
| M14 | d-dimensional trace factor γ^aγ_a = 4 instead of d | FAIL | one-loop, coeff, total | wide, colour, scheme |
| M15 | counterterm multiplies the d = 4 one-loop value (dropped O(ε) of Π⁽¹⁾) | FAIL | coeff, total | wide, colour, scheme |
| **M16** | μ/m clipped to [0.25, 25] in the MS-bar log | **PASS** | – | wide, scheme |
| M17 | delta_rho_qcd(MS-bar) evaluated at μ = m̄ when \|μ/m − 1\| < 0.6 (mass-scheme mix-up) | FAIL | total | scheme |
| M18 | delta_rho_qcd exponentiated, Δρ₀ e^{cα/π} | FAIL | total | colour, linear |
| **M19** | extra term 0.1(C_F − 3) for C_F > 3 | **PASS** | – | wide |
| M20 | e^{γε}μ^{2ε} dropped from the MS-bar two-loop term | FAIL | coeff, total | wide, colour |
| **M21** | one-loop with max(N_C, 2) (wrong only for N_C = 1) | **PASS** | – | colour |
| **M22** | delta_rho_qcd rescales C_F by 3/N_C for N_C > 3 | **PASS** | – | colour |
| *M23* | numbers hard-coded: −(1/2 + π²/6), 3/2 − π²/6, 3/2, lead = 1 (correct values, not derived) | *PASS* | – | – (lint, see C5) |

"wide", "pole-μ", "colour", "scheme" and "linear" are the five proposed checks (§5). All 22 mutants M01 to M22 fail at least one of them. Both builds pass all five (`checks_a.log`, `checks_b.log`).

## 4. How few probes the gate has

The exports are three functions, and the answer is four real numbers:
* the one-loop normalisation;
* c_pole/C_F;
* c_MS(μ = m̄)/C_F;
* the ln(μ²/m̄²) coefficient.

The blind tier enforces the functional form: c is linear in C_F, the scheme shift is C_F times a constant, and c_MS is linear in ln μ.

The oracle pins all four numbers at 10⁻⁹ inside its window:
* C_F ∈ {0.75, 1, 4/3, 2.5, 3};
* μ/m ∈ {0.3, 1, 2.5, 20}, with the pole only at μ/m = 1;
* N_C ∈ {2, 3, 5} for the one-loop value only;
* (N_C, C_F) = (3, 4/3) for the total.

So every derivation error (diagram, counterterm, ζ₂, d-dimensional factor, ε-order term) is caught (M01 to M06, M09 to M15, M20). What is not caught is how the arguments are used outside those points.

The SPEC exports no intermediate quantity: no Σ_OS or m_pole/m̄, no individual correlators, no ε-dependence. So the gate cannot test the derivation's internals, and a correct hard-coded number passes (M23). The probes that would tighten it, within the SPEC as written, are values across C_F, N_C, μ/m and α_s and the reference-free scheme consistency. Those are §5. Intermediate probes would need a SPEC change (R1).

## 5. Findings

* **C1. delta_rho_qcd is probed only at (N_C, C_F) = (3, 4/3).** This affects both the blind `b_total_consistent` and the oracle `total_check`. A total that re-derives C_F from N_C (M07), fixes it to 4/3 (M08) or mixes them (M22) passes, although the SPEC says to keep N_C and C_F general. **Fix:** `audit_total_general_colour`, 6 (N_C, C_F) pairs including (1, 0) and (8, 0.5), 2 schemes, 2 values of α_s. It compares against the auditor's values and against the module's own Δρ₀(1 + cα_s/π).
* **C2. The pole coefficient is probed only at μ/m = 1.** A pole-scheme result that keeps a ln μ (M12) passes, although μ-independence of c_pole is the main physics check of the pole scheme. **Fix:** `audit_pole_mu_independent`, reference-free, over μ/m = 10⁻⁶ to 10⁶, for qcd_coeff and delta_rho_qcd.
* **C3. The argument window is narrow.** It covers C_F ∈ [0.75, 3], μ/m ∈ [0.3, 20] and, for the one-loop value, N_C ∈ {2, 3, 5}, so M16, M19 and M21 pass. **Fix:** `audit_coeff_wide`, 45 points with C_F = 0.05 to 12, MS-bar μ/m = 10⁻⁴ to 10⁴ and pole μ/m = 10⁻³ to 10³, against the auditor's Goldstone-route numbers; N_C = 1 is in C1's check.
* **C4. Two physics constraints are not imposed directly. Fix:** two reference-free checks.
  * `audit_scheme_consistency`: Δρ_MS(m̄, μ) / Δρ_pole(m_pole) − 1 = O(α_s²) with m_pole = m̄[1 + C_F a (1 + (3/4)L)]. It is tested at α_s = 10⁻⁵ for 3 values of C_F × 5 values of μ/m. This ties the scheme shift to the independently derived mass relation (§1d), not to the oracle.
  * `audit_alpha_linear`: delta_rho_qcd is exactly linear in α_s.
* **C5. Lint cannot see a hard-coded answer.** The oracle's `LINT_TARGETS` = [2.8599, 2.859, 0.1932, 0.193] are the C_F = 4/3 values, and `LINT_EXACT` is empty. A module that types `-(0.5 + math.pi**2/6)` and `1.5 - math.pi**2/6` (M23) passes the whole gate, and only the transcript and isolation audit stands in the way. **Fix:**
  * add 2.1449 and 0.14493 to `LINT_TARGETS`;
  * add ±(1/2 + π²/6) and ±(3/2 − π²/6) to `LINT_EXACT`.

  I ran `gate.lint` with these settings: it flags M23 (line 368, the folded constant expressions), and reports nothing for builds a and b. This is an oracle edit for the orchestrator. I did not make it.
* **C6. The reference was recalled, not transcribed.** §1 is an independent confirmation of all four numbers, including the scheme shift +2C_F and the running term 3C_F ln(μ/m̄). The confirmation shares the SPEC's definition of Δρ and the gaugeless limit (§1f).
* **R1 (optional SPEC change). There are no intermediate exports.** The derivation's internals cannot be probed. An optional export `mass_ratio(CF, mu_over_m)` = (m_pole/m̄ − 1)/(α_s/π) = C_F(1 + (3/4)L) would let the gate check the counterterm finite part separately from c, and would kill a compensating error between Σ_OS and the two-loop finite part, which the current gate cannot distinguish. Splitting c_pole into rational and π² parts adds nothing: at 10⁻⁹, the real number already fixes both small rationals.
* **N1.** Goldstone route: c_pole = −C_F(1/2 + π²/6) and c_MS = C_F(3/2 − π²/6 + (3/2)ln(μ²/m̄²)), to 30 digits, ξ-independent, with the exact bare Goldstone identity Π₊(0) = Π₀(0) at two loops.
* **N2.** The masters J_mm0 and J_m00 agree with direct d-dimensional integration at 32 points, d = 2.7 to 4, to ≤ 1.3·10⁻¹².
* **N3.** m_pole = m̄[1 + C_F a(1 + (3/4)L)] by Feynman parameters, and the ξ-part of Σ_OS vanishes identically (scaleless).
* **N4.** N_C enters only Δρ₀, a massless b needs no counterterm, and γ5 anticommutation is safe by the even-count and three-vector argument (§1e), with the caveat that no HV computation was done.
