# DERIVATION — charged massless spin-1/2 emission from a charge-fluctuating Schwarzschild hole (build charged_half-a)

Units and postulates: SPEC.md (M = 1, r_h = 2, f = 1 − 2/r, T = 1/(8π), coupling g = α q n, ω̃ = ω − g/r).

## 1. Phase-factored amplitude equations (SPEC §1, §2)

Radial system (SPEC §1), with D ≡ d/dr*:

    (D − iω̃) R_− = W R_+ ,   (D + iω̃) R_+ = W R_− ,   W = k √f / r ,  k = j + 1/2 ∈ {1, 2, ...}.

**Flux.** D|R_−|² = 2W Re(R_−* R_+) = D|R_+|², so J = |R_−|² − |R_+|² is r*-independent (the iω̃ terms cancel in
|·|² for any real ω̃, so this holds for either sign of ω̃ and of g).

**Exact Coulomb phase.** Define Φ(r*) = ∫ ω̃ dr*. Since dr*/dr = 1/f and r f = r − 2,

    Φ = ω r* − g ∫ dr/(r f) = ω r* − g ln(r − 2)         (exact, up to an irrelevant constant).

Near the horizon ln(r − 2) = ln 2 + (r* − r)/2 → Φ = (ω − g/2) r* + const, which is SPEC's horizon phase; at large r
Φ = ω r* − g ln r + O(1/r): the logarithmic Coulomb phase is contained exactly in Φ, nothing is left to match.

Write R_+ = e^{−iΦ} u, R_− = e^{+iΦ} v. Then exactly

    D u = W e^{+2iΦ} v ,   D v = W e^{−2iΦ} u ,   J = |v|² − |u|².

**Independent variable.** I integrate in t = r* and carry y = ln(r − 2) as an extra state: Dy = f/(r − 2) = 1/r = 1/(2 + e^y).
Then r − 2 = e^y exactly (no cancellation near the horizon), f = e^y/(2 + e^y), Φ = ω t − g y.

**Horizon condition (SPEC §2).** R_+ = e^{−i(ω−g/2)r*}, R_− = 0 ⇒ u = 1 (constant phase dropped), v = 0 as r* → −∞.
Start at r0 = 2 + ε (ε = 1e-10) where W ≈ W(r0) e^{(r*−r*0)/4} (√f ∝ e^{r*/4} near r_h) and Φ ≈ ω_H r* + c, ω_H = ω − g/2.
The first-order solution there is

    u0 = 1 ,  v0 = ∫_{−∞}^{r*0} W e^{−2iΦ} dr* = W(r0) e^{−2iΦ(r0)} / (1/4 − 2iω_H),

with corrections O(W(r0)²) = O(k² ε/8) ~ 1e-11 k². Flux at the horizon: J = −1.

## 2. Asymptotic boundary condition: exact large-r series modes

At large r there are two exact solutions with pure asymptotics:

* in-mode:  R_+ = e^{−iΦ} A(x), R_− = e^{−iΦ} B(x), x = 1/r, A(0) = 1, B(0) = 0, which satisfy D A = W B, D B − 2iω̃ B = W A;
* out-mode: R_+ = e^{+iΦ} C(x), R_− = e^{+iΦ} E(x), E(0) = 1, C(0) = 0, which satisfy D E = W C, D C + 2iω̃ C = W E,
  i.e. the in-mode equations with (ω, g) → (−ω, −g).

With D = −f x² d/dx, f = 1 − 2x, W = k x s(x), s = √(1 − 2x) = Σ s_n x^n, A = Σ a_n x^n, B = Σ b_n x^n, matching powers gives
the recursion (a_0 = 1, b_0 = 0), for n = 1, 2, ...:

    b_n = [ −(n−1) b_{n−1} + 2(n−2) b_{n−2} + 2ig b_{n−1} − k Σ_{m=0}^{n−1} s_{n−1−m} a_m ] / (2iω)
    a_n = [ 2(n−1) a_{n−1} − k Σ_{m=0}^{n} s_{n−m} b_m ] / n

(check: b_1 = −k/(2iω), a_1 = −k b_1 = −i k²/(2ω): the centrifugal phase correction). The series is asymptotic
(terms ~ n!/(2ωr)^n eventually); it is summed to its smallest term at x = 1/r_max with ω r_max ≥ 20 + k² (and r_max ≥ 40,
r_max ≥ 40|g|/ω), where the truncation error is far below 1e-10.

**Matching.** At r_max the integrated solution is A_in·(in-mode) + A_out·(out-mode):

    u = A_in A + A_out e^{2iΦ} C ,   v = A_in e^{−2iΦ} B + A_out E,

a 2×2 linear solve. Both modes have unit flux at x → 0 (|A|² = 1, |E|² = 1), so J = |A_out|² − |A_in|² = −1 and

    Γ_j(ω; g) = 1 − |A_out|²/|A_in|² = 1/|A_in|²        (SPEC §2).

The second equality is flux conservation; the code computes both and they agree to ~1e-12 (check). Γ ∈ [0, 1] is then
automatic for either sign of g (no fermionic superradiance: |A_out| < |A_in|).

ODE: Fortran DOP853 through `scipy.integrate.ode`, rtol 1e-11, atol 1e-16, real state (y, Re/Im u, Re/Im v), vectorised over
all (k, g) pairs at one ω (they share t and y). (`solve_ivp` was avoided: its error norm calls multithreaded BLAS, which
stalls under CPU contention.)

## 3. Thermal integrals (SPEC §3)

    N(g_gb, g_μ) = Σ_k 2k ∫_0^∞ (dω/2π) Γ_k(ω; g_gb) n_F ,  P = same with an extra ω,  n_F = 1/(e^{(ω − g_μ/2)/T} + 1).

ω quadrature: Gauss–Legendre on panels with breaks 0, 0.05, 0.15, 0.3, 0.5, 0.8, 1.2, 1.8, 2.6 (16 nodes per panel); beyond
ω = 2.6 the integrand is < e^{−(2.6 − 0.25)·8π} ~ 1e-26 relative. Partial waves k = 1 … 10 (j up to 19/2): the k-th wave
contributes ~ e^{−k/(3√3 T)} ~ e^{−4.8 k} relative, so k ≤ 10 is converged far beyond need (checked against k ≤ 5, 7).

**g dependence.** For the rates, ln Γ_k(ω_i; g) is tabulated at Chebyshev nodes g_m on [−G, G] (G = 0.25, 25 nodes; for |g| > G the
range is doubled and nodes 2n − 1, automatically) and interpolated with the barycentric formula; ln Γ is analytic in g.
The interpolation is checked against direct solves at random g: relative error ≤ 4e-11 (25 nodes) vs 5e-8 (17 nodes). `transmission` itself always solves directly (cached).

## 4. Charge process (SPEC §3)

Couplings for a particle of charge q emitted from charge n: g_gb = α q n_{r_gb}, g_μ = α q n_{r_μ},
n_before = n, n_mid = n − q/2, n_after = n − q.

    up(n)   = N(g_gb, g_μ)|_{q=−1}  (electron leaves, n → n+1),
    down(n) = N(g_gb, g_μ)|_{q=+1}  (positron leaves, n → n−1).

A one-dimensional birth–death chain with nearest-neighbour steps has a stationary distribution in detailed balance
(the stationary current between n and n+1 must vanish since the chain is a tree):

    π(n+1)/π(n) = up(n)/down(n+1),   π normalised, built outward from n = 0 until π < 1e-17·π(0), tails < 1e-14 dropped.

**Symmetry.** Under n → −n, q → −q the couplings α q n_r(q,n) are invariant for every rule (n_r(−q,−n) = −n_r(q,n)), so
down(−n) = up(n) and π(−n) = π(n). Physically, a hole with like-sign charge repels its own sign of particle via both the
chemical potential and the barrier, so the chain is restoring; π ≈ Gaussian with variance ~ T/(α·const).

Averages: ⟨P⟩ = Σ_n π(n)[P_{e−}(n) + P_{e+}(n)]/2, ⟨N⟩ likewise; weight_ratio = ⟨P⟩/P(0,0),
energy_ratio = (⟨P⟩/⟨N⟩)/(P(0,0)/N(0,0)).

## 5. Independent second routes

1. **Γ, g = 0, different equation, variable and matching:** with g = 0 put ψ_1 = R_+ + R_−, ψ_2 = R_+ − R_−. Then
   Dψ_1 = Wψ_1 − iωψ_2, Dψ_2 = −Wψ_2 − iωψ_1 ⇒ D²ψ_1 + (ω² − V_+)ψ_1 = 0, V_+ = W² + DW (SPEC §1). Horizon:
   ψ_1 = e^{−iωr*}; at infinity ψ_1 = A_in e^{−iωr*} + A_out e^{iωr*} with |A_in|² − |A_out|² = 1 (Wronskian), so Γ = 1/|A_in|².
   Integrated in y = ln(r − 2) from r − 2 = 1e-20 (near the horizon V_+ ≈ W/4 = O(√f), so the start must be much
   closer than in §1), plain plane-wave projection at r = 2000/ω, no series. A real-potential scattering problem
   solved independently of §1–2. Agreement: 1e-10 (k = 1), 2e-7 (k = 2, 3; limited by the plane-wave projection).
2. **Γ, g ≠ 0:** direct integration of the unfactored R_± in r*, matched only to the leading Coulomb plane waves
   (u ≈ A_in, v ≈ A_out) at r_max = 4000/ω, compared with the series-matched result at much smaller r_max.
3. **Thermal integrals:** doubling GL nodes per panel, k_max 5 → 10, Chebyshev nodes 17 → 33, and direct Γ (no g table)
   vs the interpolated table at random g.
4. **Stationary distribution:** the null vector of the full generator matrix Q (Q_{n,n+1} = up(n), Q_{n,n−1} = down(n))
   by linear algebra, instead of the detailed-balance product.
5. **Main results, small-α expansion (principal rule).** With L = d ln N(g, g)/dg at 0, ln[π(n+1)/π(n)] =
   ln N(−α(n+1)) − ln N(αn) ≈ −Lα(2n+1), so π ∝ e^{−Lαn²} and ⟨n²⟩ ≈ 1/(2Lα). Expanding
   P_{e−}(n) + P_{e+}(n) = P(−α(n+1)) + P(α(n−1)) = 2P0 − 2αP_g + (α²/2)P_gg[(n+1)² + (n−1)²] + ...,
   ⟨P⟩/P0 = 1 + α[−P_g/P0 + P_gg/(4 L P0)] + O(α²), and likewise for N; P_g, P_gg, L by finite differences of rates().
   Result: L = 5.782, weight_ratio ≈ 1 − 5.094 α, energy_ratio ≈ 1 − 0.556 α. The full chain gives
   (wr − 1)/α = −5.009, −5.051, −5.073 at α, α/2, α/4 (extrapolating linearly → −5.094) and (er − 1)/α → −0.556:
   the two routes agree.

## 6. Results (α = 1/137.035999084)

Neutral, per helicity state: N(0,0) = 2.4284094e-4, P(0,0) = 4.0916527e-5. Principal rule (after, after):
weight_ratio = 0.96344670, energy_ratio = 0.99594617, ⟨n²⟩ = 11.81, π kept for |n| ≤ 26.
Convergence (each parameter ×2 or /2): k_max 10 → 5: 1.6e-11; GL nodes 16 → 32: 5e-13; Chebyshev nodes 25 → 49: 1e-15;
r_max ×2: Γ changes < 5e-12; ε_H 1e-10 → 1e-12 and rtol 1e-11 → 1e-12: Γ changes < 3e-10. Claimed tolerance on the
ratios: 1e-8.

Checked: g = 0 limit (continuity of rates at g = 1e-9), flux conservation (two expressions of Γ), Γ ∈ [0, 1],
low-frequency slope 2j + 1, Γ → 1 at high ω.

Nothing in this campaign had to be quoted.
