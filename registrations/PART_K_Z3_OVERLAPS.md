# Part K: can overlaps on the Z₃ circle give the quark masses and the CKM matrix?

*Written before any number below is computed, under the rules of
[archive/PREREGISTRATION.md](../archive/PREREGISTRATION.md). The derivation of every formula the
computation uses is part of the registration. Independent work, not peer reviewed.
Status: **draft, not yet registered** (nothing computed).*

## The question

STUR v7.0 obtained its CKM numbers from wave-function overlaps of three generations localized at
the three Z₃ fixed points of a circle (`scripts/ckm_full_diagonalization.py`, commit `2859610`).
Rerunning that code showed that its agreements come from constants typed into it (α_eff = 1.480
where its own calculation gives 1.431; A ≡ f_hol = 0.846; η̄ from four typed factors), and that it
never diagonalizes a Yukawa matrix. This registration keeps the geometry and drops everything typed
in. It asks one question:

**Is there any choice of the unknowns of the Z₃ overlap model that reproduces the four quark mass
ratios and the four CKM data at once?**

Every unknown is scanned over its whole range, never set. The model has 6 unknowns and the data are
8 numbers, so it makes **2 predictions**, and it is judged by a χ² test with 2 degrees of freedom, as
Part C judges texture zeros.

## The model (fixed here, not afterwards)

- **Geometry.** One extra dimension, a circle θ ∈ [0, 2π). The three generations k = 0, 1, 2 sit at
  the Z₃ points θ_k = 2πk/3. The gauge group is the Standard Model's. 3-3-1 is not used: its triplet
  and antitriplet families carry different U(1)_X charges (Part D), which would break the Z₃ that
  relates the generations.
- **Z₃ relates the generations.** For each species X ∈ {Q, u, d} (quark doublet, up singlet, down
  singlet), the three generations are rotated copies of one profile: Ψ_{X,k}(θ) = χ_X(θ − θ_k).
- **Localization.** χ_X is the normalized ground state of the operator v7.0 used,
  −(∂_θ − i q_X Φ/2π)² + a_X (1 − cos θ), on the circle with periodic boundary conditions.
  a_X > 0 sets the width of the profile.
- **Holonomy.** A constant hypercharge connection A_θ = Φ/2π, with holonomy ∮A = Φ, is the only
  source of CP violation. The charges are q_Q = 1/6, q_u = 2/3, q_d = −1/3 and q_H = 1/2. Every
  hypercharge is a multiple of 1/6, so Φ has period 12π.
- **Higgs.** φ_H(θ) = χ_H(θ − θ_H), the ground state of the same operator with a_H and q_H,
  centred at θ_H. In v7.0 the Higgs sat on the third fixed point. Here θ_H is an unknown, because
  K0b below shows that a fixed point is excluded.
- **Yukawas.** From L ⊃ −y_u Q̄ H̃ u − y_d Q̄ H d integrated over the circle, with H̃ = iσ₂H*:
  - Y^u_ij = y_u ∫₀^{2π} dθ  conj(Ψ_{Q,i}) · conj(φ_H) · Ψ_{u,j},
  - Y^d_ij = y_d ∫₀^{2π} dθ  conj(Ψ_{Q,i}) · φ_H · Ψ_{d,j}.

  The hypercharges in each integrand sum to zero (−1/6 − 1/2 + 2/3 = 0 and −1/6 + 1/2 − 1/3 = 0), so
  each integrand is gauge invariant and periodic. y_u and y_d are overall constants that cancel in
  every observable used here.

**Unknowns (6):** a_Q, a_u, a_d, a_H, θ_H and Φ. **Data (8):** m_u/m_c, m_c/m_t, m_d/m_s and m_s/m_b at
the evaluation scale, plus |V_us|, |V_cb|, |V_ub| and J. **Predictions: 8 − 6 = 2.**

## Derivation

**D1. Profiles in Fourier space.** Write χ(θ) = Σ_{n=−N}^{N} c_n e^{inθ} and s = qΦ/2π. Then
(∂_θ − is) e^{inθ} = i(n − s) e^{inθ}, so the kinetic term gives (n − s)² on the diagonal. The
potential a − (a/2)(e^{iθ} + e^{−iθ}) couples c_n to c_{n±1} with coefficient −a/2. The operator is
therefore the real symmetric tridiagonal matrix

  T_nn = (n − s)² + a,   T_{n,n±1} = −a/2.

Its off-diagonal entries are negative, so by Perron–Frobenius (applied to cI − T) the ground state can
be chosen with every c_n > 0. That fixes its phase. The normalization is
∫₀^{2π} |χ|² dθ = 2π Σ c_n² = 1. For s ≠ 0 we have c_n ≠ c_{−n}, so χ is complex. For s = 0,
c_n = c_{−n}, so χ is real and even. A rotated copy is χ(θ − θ_c) = Σ c_n e^{−inθ_c} e^{inθ}. Rotation
commutes with a constant connection, so it is the correct copy at θ_c.

**D2. Overlap integrals.** Each Yukawa integrand is a product of three trigonometric polynomials of
degree ≤ N, so it has degree ≤ 3N. The trapezoid rule on M equally spaced points,
∫₀^{2π} f dθ = (2π/M) Σ_m f(2πm/M), is exact for degree < M. With M > 3N the integrals are exact up to
rounding.

**D3. Masses and mixing.** M_q = v Y^q/√2. Write H_q = Y^q Y^q† = U_q diag(y₁², y₂², y₃²) U_q†, with
the columns of U_q in ascending order. The mass ratios are the y_i ratios, and V = U_u† U_d. The
observables are |V_us| = |V₁₂|, |V_cb| = |V₂₃|, |V_ub| = |V₁₃| and J = Im(V_us V_cb V_ub* V_cs*), the
same definition as `ckm_observables` in Part B.

H_q is Hermitian. It is diagonalized through its real embedding [[Re H, −Im H], [Im H, Re H]], which
has every eigenvalue of H twice. The existing real Jacobi routine diagonalizes it. An eigenvector
(x; y) gives the eigenvector x + iy of H, and both vectors of a degenerate pair give the same complex
vector up to a phase, which no observable sees. This requires the eigenvalues of H to be distinct,
and the code checks that.

**D4. Field rephasings do not matter.** A phase change of any Ψ_{X,k}, or of φ_H, multiplies Y by
diagonal phase matrices. That changes neither the y_i nor |V_ij| nor J.

**D5. The scan covers both signs of J.** The reflection θ → −θ maps the set of fixed points to itself,
which is only a relabelling of the generations. It sends θ_H → −θ_H and Φ → −Φ, and it complex-
conjugates the Yukawas, which flips the sign of J. A Z₃ rotation brings −θ_H back into
[0, 2π/3). So θ_H ∈ [0, 2π/3) and Φ ∈ [0, 12π) cover both signs of J and every configuration up to
symmetry.

**D6. Theorem: no holonomy and a Higgs on a symmetry point give an excluded CKM matrix.** Let
Φ = 0 and θ_H ∈ (π/3)ℤ, that is, on a fixed point or halfway between two. Then the reflection
R: θ → 2θ_H − θ maps the set {θ_k} to itself. It fixes one generation and swaps the other two;
call that swap P. With Φ = 0 every profile is real and even about its own centre (D1). So
Ψ_{X,k}(Rθ) = Ψ_{X,P(k)}(θ) and φ_H(Rθ) = φ_H(θ). Changing variables θ → Rθ in the integral gives
Y_{P(i)P(j)} = Y_ij, so Y commutes with the permutation matrix P, and so do H_u and H_d. The P-odd
subspace is one-dimensional, spanned by (e_a − e_b)/√2 for the swapped pair. So that vector is an
eigenvector of both H_u and H_d. In the CKM matrix one up state and one down state are then the same
vector, and **some |V_ij| = 1 exactly**. All nine measured |V_ij| are below 1, with |V_tb| = 0.999 at the
closest, and the theorem's equality also forces two other entries of that row to 0. **So the v7.0
configuration, with the Higgs on the third fixed point and no flux, cannot give three-family mixing
when its Yukawa matrices are actually diagonalized.** The theorem needs only that each profile is even
about its centre, so it holds for any widths, Mathieu or Gaussian.

**D7. Leading-order estimate (the basis of the expectation in K1).** For large a the ground state is
close to a Gaussian, χ ∝ exp(−ω θ²/2) with ω = √(a/2). A triple Gaussian overlap gives
ln Y_kk = const − c d_k², where d_k is the distance from θ_k to θ_H and
c = ω_H(ω_Q + ω_q)/(2(ω_Q + ω_q + ω_H)). For θ_H ∈ [0, π/3] and D = 2π/3, the three distances are
θ_H, D − θ_H and D + θ_H. If each mass is close to its diagonal entry, then

  R ≡ ln(m₃/m₂) / ln(m₃/m₁) = (D − 2θ_H)/(D + 2θ_H),

independent of every width, and the same in both sectors. From the run masses at m_t(m_t)
(results/production_v2_2.txt, Part B): R_u = ln(1/r_ct) / ln(1/(r_uc r_ct)) ≈ 0.471, and
R_d = ln(1/r_sb) / ln(1/(r_ds r_sb)) ≈ 0.570. These need θ_H ≈ 0.180 D and θ_H ≈ 0.110 D
respectively: one θ_H cannot satisfy both. Off-diagonal entries, non-Gaussian tails and the holonomy
all correct this estimate. Broad profiles (small a) are where it fails most. So the estimate is a
reason to expect exclusion, not a proof.

## The computation (fixed here)

- **Evaluation scales.** m_t(m_t) and M_S, both produced by the existing script, as in Parts B and C.
- **Measured values.** The ratios r_uc, r_ct, r_ds and r_sb from `FlavourRunner.ratios_at`. Their
  uncertainties are propagated by ±1σ variations of `FLAVOUR_UNCERTAIN`, as in Part C's
  `input_sigma`. The CKM data come from `COMPARISONS` (V_us, V_cb, V_ub, J), with asymmetric errors as
  in `TextureSurvey.chi2`.
- **χ².** The sum of 8 terms. For each ratio: ((ln r_pred − ln r_meas) / (σ_r / r_meas))². For each CKM
  datum: ((pred − meas)/σ), with σ the upper or lower error on the side the prediction falls, combined
  in quadrature with the input-propagated error of the prediction at that point. Correlations are
  neglected, as in Part C. The p-value is chi2_pvalue(χ²_min, 2) = exp(−χ²_min/2), converted to
  Gaussian σ by `pvalue_to_sigma`.
- **Search coordinates.** log₁₀ a_X ∈ [−2, 4] for X = Q, u, d, H; t = θ_H/(2π/3) ∈ [0, 1); and
  f = Φ/12π ∈ [0, 1).
- **Start grid.** log₁₀ a_X ∈ {−2, −0.5, 1, 2.5, 4}, t ∈ {k/6 : k = 0..5} and f ∈ {k/8 : k = 0..7}:
  5⁴ × 6 × 8 = 30,000 points. The 10 lowest are refined by the compass search `_minimize`. The θ_H and
  Φ coordinates are periodic; the a coordinates are clamped to the range.
- **Boundary rule.** If the best point has some log₁₀ a_X on the edge of [−2, 4], that range is
  extended by 2 decades in that direction once, and the search is repeated. Both results are reported.
- **Numerical settings (NUMERICS).** N = 128 Fourier modes and M = 576 quadrature points
  (M > 3N, and divisible by 18 so that the grid values of θ_k and θ_H fall on quadrature points).
  The ground state comes from Sturm-sequence bisection plus inverse iteration on the tridiagonal T.
- **The point found is never reported as a determination** and is never used anywhere else, as in
  Part C.

## Pass conditions, fixed in advance

| Item | What is computed | Expected | What counts as the expectation failing |
|---|---|---|---|
| K0a | J at Φ = 0, at 20 fixed points drawn by the script's `_IntStream` (seed `closure_seed`) over the search box | \|J\| ≤ 10⁻¹² at every point (D1: real profiles) | any \|J\| > 10⁻¹² |
| K0b | max \|V_ij\| over all nine entries at Φ = 0, θ_H ∈ {0, π/3, 4π/3}, at the same 20 width sets | some \|V_ij\| = 1 within 10⁻⁹ at every point (D6) | any point with every \|V_ij\| < 1 − 10⁻⁹ |
| K1 | χ²_min with 2 dof, at m_t(m_t) and at M_S | **excluded**: above 3σ at both scales (D7) | χ²_min ≤ 11.83 (3σ or less) at either scale |
| K2 | the same search with N = 192 and M = 864, at the best point of K1 | χ²_min changes by < 10⁻⁶ relative | a larger change (numerics not converged; reported, not fixed) |
| K3 | 20 refined starts instead of 10, plus 200 extra random starts (`_IntStream`, seed `closure_seed`) refined the same way | no χ²_min lower than K1's by more than 1% | a lower minimum (K1's search was incomplete; the lower value replaces it, and both are reported) |
| K4 | at the best point: \|det Y\|² against y₁²y₂²y₃² from the diagonalization, and unitarity of V | relative difference < 10⁻⁶; \|VV† − 1\| < 10⁻¹² | either larger |

**What each outcome means.**
- *K1 excluded:* the Z₃ overlap geometry, with the profiles of v7.0 and no typed factors, cannot
  produce the quark masses and the CKM matrix together. The flavour sector of STUR then needs Z₃ to be
  broken further, which brings new unknowns.
- *K1 survives:* it is a genuine candidate with 2 predictions. Survival is constructive: the point
  found proves it. Exclusion holds only within the registered search, which K3 tests.
- *K0a or K0b failing* means the code is wrong, not the theorem. It would be fixed, then reported
  below the result under rule 5.

---

## Result

*(Not yet computed.)*
