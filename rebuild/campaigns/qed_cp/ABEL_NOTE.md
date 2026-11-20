# ABEL_NOTE: the Abel-damping step of Link 23 (L23b)

*Scope: the step that L23b and ACCEPTED.md list as "supported by three regularizers, not proved". It is the claim that the
damped double photon integral of the 12 time-ordered diagrams tends, as the damping is removed, to the value the campaign
uses (eq. (3) of `builds/a/DERIVATION.md`, the same number as rung 3's imaginary-frequency integral), whatever the damping
form. This note gives the exact statement, its hypotheses, a proof, the rate of convergence with its coefficients,
and the regulators for which the statement is **false**. Scripts: `/tmp/claude-0/-home-user-STUR-Physics-Lab/6f003c51-fc14-5da0-833a-45f53d6397be/scratchpad/abel/`
(`sym_checks.py`, `moments.py`, `product_regs.py`, `brute2d.py`, `cutoffs.py`, `power.py`, with `*.out` logs). The
scratchpad is not durable, so the numbers that matter are copied below.*

Units are ħ = c = 1 and a = ω₀. The numerics use a = α₀ = 1 and ρ = rω₀.

## 0. The object

From the 12 diagrams (DERIVATION a §1–3, b §1), with d⁴ = α₀²a²/4,

    U[Φ] = −(d⁴/π²) ∫₀^∞∫₀^∞ dk dq  G(k,q) Φ(k,q),   G = [h_A(k)h_A(q) + 2 h_B(k)h_B(q)] · Σ(k,q),          (1)

* h_X(k) = k³X(kr) is the direction-averaged one-photon factor. X = A is the longitudinal part and X = B the transverse
  part. Exactly (sympy, `sym_checks.py` S3), h_X(k) = Im[P_X(k) e^{ikr}]/r³ with P_A = 2(1 − ikr) and P_B = k²r² − 1 + ikr,
  and h_X(k) = (2/3)k³ + O(k⁵) at k → 0.
* Σ is the 24-ordering energy-denominator sum divided by 2 (SPEC 3b). For a = b it splits exactly (S1, residual 0) as
  Σ = 4(a+k)⁻²(a+q)⁻²[a²/(k+q) + 2a + (k+q) + kq/(2a)].
* Φ is the regulator. The campaign's choice is Abel damping, Φ = e^{−ε(k+q)}.

Without Φ, (1) is not a Lebesgue integral: G ~ (2/(a r²)) kq sin(kr) sin(qr) at large k and q (S1: λ²Σ(λk,λq) → 2/(akq)).

**The value the campaign uses** is

    U* = −(1/π r⁶) ∫₀^∞ du α(iu)² e^{−2ur} p(ur),   p(x) = x⁴+2x³+5x²+6x+3                                 (3)

(build a's eq. (3); `cp_energy` in both builds; at ρ = 1, U* = −0.651266426221).

**Note on "adiabatic switching".** The campaign's damping is in photon *energy*, e^{−εk} with ε a length. It is not
adiabatic switching in time. In position space it smears each dipole with the 3-D Poisson kernel ε/(π²(x²+ε²)²) (S7),
a smooth source with an ε/R⁴ tail. Switching H_int on as e^{−η|t|} does not regularise (1) at all: it changes only the
energy denominators, and the large-k oscillation remains. Section 4(d) covers switching combined with a UV regulator.

## 1. Statement

**Hypotheses.**

* **(H1) r > 0.** At r > 0 every term of G carries a phase e^{i(±k±q)r} with nonzero frequency in each variable. The
  terms with no phase, the r-independent self-energies, are excluded by the SPEC. They are the ones that diverge in a
  regulator-dependent way.
* **(H2) No zero-energy resonance: a > 0, ground-state atoms.** Then every intermediate energy is a positive combination
  of a, k and q. The only one that can vanish is k + q (at the corner k = q = 0, where h_X(k)h_X(q) ~ k³q³ kills it).
  Hence Σ is smooth on [0,∞)² \ {0}, with |Σ| ≤ C/(k+q) near 0. In addition, for k ≥ 1 or q ≥ 1 it satisfies the symbol
  bounds |∂_k^i ∂_q^j Σ| ≤ C (1+k)^{−1−i}(1+q)^{−1−j}. Proof: the bracket is a polynomial of order (1,1) plus
  a²/(k+q), and on k+q ≥ 1, (k+q)^{−1−i−j} ≤ C(1+k)^{−i}(1+q)^{−j}(1+k+q)^{−1}.
* **(H3) Single resonance**, a = b. This is used only to write Σ explicitly. Any finite set of levels with all aₙ > 0
  satisfies H2 term by term, and the proof is unchanged.
* **Regulator class 𝓡.** Φ_ε(k,q), ε ∈ (0,1], with three properties.
  * (R1) Uniform symbol bounds: |∂_k^i ∂_q^j Φ_ε(k,q)| ≤ C (1+k)^{−i}(1+q)^{−j} for 0 ≤ i, j ≤ 3, with C independent
    of ε.
  * (R2) Pointwise limits: Φ_ε → 1, and every derivative ∂^αΦ_ε → 0 for α ≠ 0.
  * (R3) Decay at each fixed ε: |∂^αΦ_ε(k,q)| ≤ C_ε (1+k)^{−3}(1+q)^{−3}. This makes (1) absolutely convergent and
    kills the boundary terms at infinity.

  For a scaled family Φ_ε = Φ(εk, εq), (R1) holds when sup (1+t₁)^i(1+t₂)^j |∂^{ij}Φ(t)| < ∞, because
  ε^i = k^{−i}(εk)^i. The class contains the following regulators:
  * Abel e^{−ε(k+q)};
  * Gaussians e^{−ε²(k²+q²)} and e^{−ε²(k+q)²};
  * form factors φ(εk)φ(εq) with φ = (1+t²)^{−4} (hydrogen-like) or any smooth φ that decays fast enough;
  * ψ(ε(k+q)) for smooth ψ that decays fast enough;
  * e^{−ε√(k²+q²)}.

  It excludes sharp cut-offs, Fejér (1 − k/Λ)₊ weights, and max(k,q)-type kinks.

**Theorem 1 (universality and identification).** Under H1–H3, for every Φ ∈ 𝓡, U[Φ_ε] → U* as ε → 0. More generally,
the limit holds jointly with any family of denominators Σ_η that satisfies H2's bounds uniformly in η and tends to Σ
pointwise. This includes adiabatic switching E_n → E_n − i n η.

**Theorem 2 (rate).** For a smooth scaled regulator Φ(εk, εq) that is symmetric in its two arguments,

    U[Φ_ε] = U* + ε(∂₁+∂₂)Φ(0)·m₁₀ + ε²[ ∂₁²Φ(0)·m₂₀ + ∂₁∂₂Φ(0)·m₁₁ ] + O(ε³)

Here m_ij is the regularised moment ∫∫ k^i q^j G. By Theorem 1 it is the same for every regulator in 𝓡, and with identity
(2) it reduces to closed form (§3). For a product φ(εk)φ(εq), this becomes

    U = U* + 2εφ′(0) m₁₀ + ε²[φ′(0)² m₁₁ + φ″(0) m₂₀] + O(ε³).

There are no log terms. The series is asymptotic: regulators with complex singularities, such as (1+t²)⁻⁴ with poles at
t = ±i, add terms of order e^{−r/ε}, which matter only once ε ≳ r/6.

## 2. Proof of Theorem 1

**Step A: the limit exists and does not depend on Φ.** Take a smooth partition χ(k) + (1−χ(k)), with χ = 1 on [0,1] and
χ = 0 on [2,∞), and the same in q. This splits (1) into four regions.

1. **χχ (both energies small).** The region is compact and |G| ≤ C k³q³/(k+q) is bounded. By (R1), |Φ_ε| ≤ C. By
   (R2) and dominated convergence, this part tends to its value at Φ = 1.
2. **χ(k)(1−χ(q)) (k small, q large).** Here k + q ≥ 1. Write h_B(q) = (P_B e^{iqr} − P̄_B e^{−iqr})/(2i r³), and
   likewise for A. For each sign of the phase, integrate by parts three times in q, using e^{±iqr} = (±ir)^{−1}∂_q e^{±iqr}.
   The boundary terms vanish: at q = 1 because of (1−χ), and at infinity by (R3).
   * The amplitude P(q)Σ(k,q) is a symbol of order 2 − 1 = 1 in q, uniformly for k ∈ [0,2] (H2).
   * So ∂_q³[(1−χ)PΣΦ_ε] is bounded by C(1+q)^{−2}, uniformly in ε (R1, Leibniz). This bound is integrable.
   * ∫₀²|h(k)|dk < ∞.
   * By dominated convergence and (R2), the limit is the same integral with Φ ≡ 1.
3. **(1−χ)χ.** The same with k and q exchanged.
4. **(1−χ)(1−χ) (both energies large).** Integrate by parts three times in each variable, for each of the four phases
   e^{i(σk+σ′q)r}. Leibniz and the bounds give |∂_k³∂_q³[amplitude·Φ_ε]| ≤ C(1+k)^{−2}(1+q)^{−2}, uniformly in ε. This
   bound is integrable, so dominated convergence applies again.

Every piece converges to an absolutely convergent expression that does not contain Φ. ∎(A)

The same argument with Σ_η in place of Σ gives the joint limit in (ε, η), since H2's bounds hold uniformly:
|E − i n η| ≥ E.

**Step B: the universal limit equals U*.** Use the Abel product regulator, which is in 𝓡, together with identity (2) of
build a:

    Σ = (8/π)∫₀^∞ du a²kq/[(a²+u²)²(k²+u²)(q²+u²)]

S1 re-verifies (2) by residues, with residual 0, for general a and b.

* **Fubini.** At ε > 0 the triple integrand is |h(k)h(q)|e^{−ε(k+q)} times a positive kernel whose u-integral is Σ.
  Tonelli then gives absolute convergence, so

      U_ε = −K∫₀^∞ du (a²+u²)^{−2}[I_A(u)² + 2I_B(u)²],   K = 8d⁴a²/π³,   I_X(u) = ∫ k⁴X(kr)e^{−εk}/(k²+u²) dk.

* **Pointwise limit and domination.** Write I_X as the near part plus the far part.
  * Near part: |∫χ…| ≤ C/(1+u²).
  * Far part: integrate by parts five times. The amplitude kP_X/(k²+u²) satisfies |∂ⁿ| ≤ C(1+k)^{3−n}/(k²+u²), so the
    far part is bounded by C∫₁^∞ k^{−2}dk/(k²+u²) ≤ C/(1+u²), uniformly in ε.
  * The same argument gives the pointwise limit I_X(u) → M_X(u), the Abel value.
* **The Abel values in closed form.** M_X(u) reduces to the polynomial Abel values j!(i/r)^{j+1} (S2) plus four basic
  integrals of e^{ikr}/(k²+u²) and k e^{ikr}/(k²+u²). These involve Ei and E₁ and are checked by `quadosc`. The Ei and
  E₁ parts cancel (S4), leaving
  * M_A = π(1+x)e^{−x}/r³;
  * M_B = −π(1+x+x²)e^{−x}/(2r³), with x = ur.

  These are build a's M. Moreover M_A² + 2M_B² = (π²/2)e^{−2x}p(x)/r⁶ (S4).
* **Conclusion.** Dominated convergence applies with the bound C²(1+u²)^{−2}(a²+u²)^{−2}, which is integrable. Hence
  U_ε → U*. ∎

**Proof of Theorem 2.** For a product regulator, Taylor-expand φ inside the far-part representation. The residual
φ(εk) − 1 − εkφ′(0) equals ε²k²ψ₂(εk), with ψ₂ bounded and symbol-type. Applying Step B's bound to the order-5 amplitude
k²F_u, with seven integrations by parts, gives

    I_X = M_X + εφ′(0)M_X^{(1)} + ε²[½φ″(0)M_X^{(2)} + o(1)]

with a remainder uniformly O(ε²/(1+u²)). Squaring and integrating over u gives the formula. The non-product case uses the
same Taylor-remainder argument in two dimensions; it is *sketched* and checked numerically, not written out.

## 3. Closed-form coefficients (`moments.py`, mpmath at 40 digits)

The one-photon moments are M_X^{(n)} = Abel∫k^{4+n}X/(k²+u²):

* M^{(1)} contains Ei and E₁ (S4);
* M^{(2)} = −u²M^{(0)} exactly.

The two-photon moments are m_ij = −K∫(a²+u²)^{−2} Σ_X c_X M_X^{(i)}M_X^{(j)}, with c_A = 1 and c_B = 2.

| ρ | U (u-rep) = U* (eq. 3) | Abel slope κ = (U_ε/U − 1)/(εω₀) | κ·ρ (coefficient of ε/r) | m₁₁/U | m₂₀/U |
|---|---|---|---|---|---|
| 0.01 | agree to 0 | −339.53 | −3.395 | 3.24e4 | −0.988 |
| 0.3 | agree to 0 | −11.323 | −3.397 | 35.90 | −0.736 |
| 1 | agree to 0 | **−3.34652** | −3.347 | 3.121 | −0.432 |
| 3 | agree to 0 | −1.03549 | −3.106 | 0.312 | −0.157 |
| 100 | 4e-33 | −0.026587 | −2.659 | 2.8e-4 | −2.8e-4 |

* The Abel slope at ρ = 1, −3.3465, is the value build b measured empirically (−3.346, ACCEPTED.md); here it is derived.
* The correction is O(ε/r) at every separation. Its coefficient runs from −3.40 (near zone) to about −2.66 (far zone).
* The audit's ε² ratio of 4 between the form factor and the Gaussian is φ″(0) = −8 against −2.

## 4. Numerical checks

### 4(a) Product regulators, exact at finite ε (`product_regs.py`)

Method: identity (2), then Gauss–Legendre in k and in θ (u = tan θ). It reproduces build a's `damped_energy` to 1e-15.
The table gives the residual after the two-term prediction of Theorem 2, (U_ε/U − 1) − c₁ε − c₂ε², at ρ = 1.

| φ | φ′(0), φ″(0) | ε = 0.04 | 0.02 | 0.01 | behaviour |
|---|---|---|---|---|---|
| Abel e^{−t} | −1, 1 | 2.8e-4 | 3.6e-5 | 4.6e-6 | residual ∝ ε³ (×4.5) |
| e^{−2t−t²} | −2, 2 | −7.0e-4 | −9.8e-5 | −1.3e-5 | ∝ ε³; slope twice Abel's |
| (1+t)e^{−t²} | **+1**, −2 | 1.8e-3 | 2.1e-4 | 2.6e-5 | ∝ ε³; approaches U* **from the strong side** |
| Gaussian e^{−t²} | 0, −2 | 4.9e-6 | 3.0e-7 | 1.9e-8 | ∝ ε⁴ |
| form factor (1+t²)⁻⁴ | 0, −8 | 8.7e-5 | 5.5e-6 | 3.4e-7 | ∝ ε⁴ (ε ≥ 0.08 is outside the asymptotic regime) |
| e^{−t}(1+t) | 0, −1 | −5.1e-4 | −6.4e-5 | −8.0e-6 | ∝ ε³; **not monotone** (U_ε/U − 1 changes sign) |

* ρ = 0.3 and ρ = 3 behave the same way (see `product_regs.out`).
* Every regulator tends to U*, with the slope and curvature that Theorem 2 predicts.
* The blind gate check `b_damped_properties` asserts "approaches cp_energy monotonically from the weak side". That
  property belongs to Abel (φ′(0) < 0, φ″(0) > 0). It is not a property of the limit.

### 4(b) Non-product regulators, brute-force 2-D quadrature without identity (2) (`brute2d.py`, ρ = 1)

| Φ | predicted | ε = 0.08 | 0.04 | 0.02 | residual after prediction |
|---|---|---|---|---|---|
| e^{−ε²(k²+q²)} (product, control) | +0.8633ε² | 5.605e-3 | 1.386e-3 | 3.456e-4 | 3.0e-7 at 0.02; matches 4(a) to all digits |
| e^{−ε²(k+q)²} | **−5.379ε²** = −2(m₂₀+m₁₁)ε² | −3.872e-2 | −8.848e-3 | −2.166e-3 | −1.5e-5 at 0.02 (∝ ε⁴) |
| e^{−ε(k+q)−ε²(k+q)²} | −3.3465ε − 2.690ε² | −0.2979 | −0.1397 | −0.0682 | −1.9e-4 (∝ ε³) |

* The grid is stable to 1e-16 when the cut is extended by 30%.
* The non-product Gaussian has a different ε² coefficient, with the opposite sign to the product one. It is predicted
  through m₁₁ and confirmed. So the limit is regulator-independent but the approach is not.

### 4(c) Analytic continuation in a power (`power.py`)

The regulator is (kq)^{−σ}, absolutely convergent for 2 < σ < 7/2, continued to σ = 0 with **no damping factor**.
* Per u, the k > c tail is expanded in 1/k and each term k^{n−σ}e^{ikr} is integrated exactly as c^{n−σ+1}E_{σ−n}(−irc),
  which is entire in σ.
* In the convergent region (σ = 2.5) this agrees with direct `quadosc` to 4e-12.
* At σ = 0 it equals the residue values M_X(u) to 1e-25 at u = 0.1, 1 and 4.
* The full power-continued energy at ρ = 1 is Z(0) = −0.6512664262212, against U* to **2.4e-13**. Z(±0.05) gives
  ∓7.5% and ±8.0%, so Z is smooth through σ = 0.
* An earlier run gave a garbage Z (about 1e75), from mpmath cancellation at u ~ 1e3. It was fixed by cutting the
  u-integral at u ≤ 20; the tail beyond is below 1e-9 relative at σ = 0.

Why the continuation equals the Abel limit: with k^{−σ} = Γ(σ)^{−1}∫λ^{σ−1}e^{−λk}dλ, Z(σ) is a Mellin transform of the
two-parameter Abel function U(λ, μ). That function is jointly continuous at 0 and has a mixed Lipschitz remainder
(product form in the u-representation). Since σΓ(σ) → 1, this gives Z(0) = U(0,0) = U*.

### 4(d) Adiabatic switching on top of a UV regulator (`brute2d.py`)

The denominators become E_n − i n η, with a product Gaussian at ε = 0.04 and ρ = 1.

| η | 0.2 | 0.1 | 0.05 | 0.025 | 0.0125 |
|---|---|---|---|---|---|
| Re U/U(η=0) − 1 | −9.7e-2 | −2.5e-2 | −6.4e-3 | −1.6e-3 | −4.0e-4 |
| Im U/\|U\| | −0.36 | −0.19 | −0.095 | −0.047 | −0.024 |

The real part converges as O(η²) and the imaginary part vanishes as O(η). Both are consistent with Theorem 1's joint
limit.

### 4(e) Where the statement is false: non-smooth regulators (`cutoffs.py`; sym_checks S5–S6)

* **Sharp cut-off, k, q < Λ.** There is no limit, and the energy *diverges*. To leading order
  U_Λ ≈ U* − (2K/r⁴)(π/4a³)Λ²cos²(Λr). Averaged over a period of Λ this is U* − Λ²/(2π²r⁴) (a = α₀ = 1).
  * Numerically at ρ = 1, the period average of U_Λ/U* − 1 is 216.8, 3195 and 50123 at Λ ≈ 50, 200, 800, against the
    predictions 219.3, 3208 and 50166.
  * The audit's "π − 2cos Λ" covered only a single longitudinal one-photon integral. The full two-photon transverse
    term grows like Λ².
* **"Sharp cut-off with averaging" in its naive form, the Cesàro mean over Λ of the square cut-off.** It also
  diverges, as −Λ²/(6π²r⁴): 258.7 against 259.3 predicted at Λ = 100, and 4171 against 4149 at Λ = 400. Averaging cannot
  help, because the divergent term is the *square* of an oscillation, and cos² has mean ½.
* **Fejér (Riesz order 1) product weights (1−k/Λ)₊(1−q/Λ)₊.** U_Λ oscillates without a limit, between −0.36 and +0.65
  relative at ρ = 1. Its Λ-average converges, but to the **wrong value**:

      U* + δU,   δU = −α₀²ω₀/(2π² r⁶)   (exact, S6),

  The transverse Fejér mean of ∫k sin(kr) is −sin(Λr)/r², whose square has mean 1/(2r⁴). Numerically the period
  averages are +0.0159, +0.0614, +0.0736 at Λ = 50, 200, 800 against +0.0778 (ρ = 1), and +0.1152 against +0.1165 at
  ρ = 3, approached as 1/Λ.
  * δU is 6.75% of the near-zone energy, 2/(3π²).
  * It goes as r⁻⁶, so it would **change the far-zone law** from r⁻⁷ to r⁻⁶.
* **Riesz order 2 product weights (1−k/Λ)₊²(1−q/Λ)₊².** These converge to U*, as 1/Λ: −1.2e-1, −3.3e-2, −8.3e-3 at
  Λ = 50, 200, 800. This matches the classical fact that ∫k^d e^{ikr} is (R, m)-summable exactly for m > d. Here the
  transverse amplitude has d = 1.

So the precise boundary of the statement is as follows.

* Smooth regulators (𝓡) all give U*, as do sufficiently high Riesz means.
* Regulators that are not smooth enough relative to the amplitude growth fail, separately in each photon energy:
  * sharp cut-offs, whether or not they are averaged over Λ, diverge;
  * Fejér means give a definite wrong value.
* The physical motivation for 𝓡 is that finite atoms have smooth form factors F(k²) with F(0) = 1. Such form factors are
  even in k, so the correction is O((size/r)²).

## 5. What is established and what is not

**Established (proof plus checks):**
* For two ground-state single-resonance atoms at r > 0 (H1–H3), every regulator in 𝓡 gives the same limit. This
  includes the builds' Abel damping, Gaussian (product and non-product), hydrogen-like form factor and power
  continuation. The limit is the campaign's U* (eq. (3) = rung 3's formula).
* The rate is O(ε/r), with the closed-form coefficient (∂₁+∂₂)Φ(0)·m₁₀. The Abel slope −3.3465 at ρ = 1 is derived.
  For even regulators the rate is O(ε²/r²).
* Smoothness is necessary: sharp and Fejér cut-offs are explicit counterexamples, and the Fejér mean gives a wrong value
  in closed form.

**Not established, or only sketched:**
* The rate theorem is proved for product regulators. For non-product regulators the Taylor-remainder step is sketched
  only (the numerics in 4(b) agree with it).
* The proof's regularity class (R1) with three derivatives is sufficient, not necessary. Riesz-2 lies outside it and
  still converges; this is observed, not proved here.
* The argument for power continuation is a Mellin argument whose uniform-in-u bounds are not written out. Numerically, Z was evaluated at
  σ = 0 and ±0.05 only, not along the whole continuation path from the convergent strip.
* **Outside the hypotheses:**
  * An excited atom (a < 0) puts on-shell poles at k = |a| inside the integration range. There the damping does not
    define the integral: a prescription for the denominators (±i0, principal value) is needed, and different
    prescriptions give different (complex or oscillating) results. Nothing here applies.
  * A zero-energy resonance (a → 0 at fixed d) makes U* diverge as 1/a.
  * The case r = 0 is not covered.
  * Multi-level atoms with infinitely many levels need uniform bounds summed over levels, which have not been checked.
* **Still physics input, not mathematics:**
  * that the dipole approximation with a smooth form factor in the point limit is the physical value;
  * the single-resonance model of L23b.
* The proof is written for this model and checked by sympy and numerics. It has not been reviewed independently.
