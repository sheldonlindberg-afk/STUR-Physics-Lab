# DERIVATION — greybody-a

Units G = c = ħ = k_B = M = 1, r_h = 2, f = 1 − 2/r, r* = r + 2 ln(r/2 − 1) (SPEC preamble).

## 0. Postulates used

* SPEC §1: master equation ψ'' + (ω² − V)ψ = 0 (prime = d/dr*), with
  bosons V = f [L/r² + κ/r³], L = j(j+1), κ = 2(1 − s²);
  fermions V = W² ± dW/dr*, W = k√f/r, k = j + 1/2.
* SPEC §2: ψ → e^{−iωr*} at the horizon; ψ → A_in e^{−iωr*} + A_out e^{+iωr*} at infinity; Γ = transmitted / incident flux.
* SPEC §3: T = 1/(8π); P_s = Σ_j (2j+1) ∫ dω/(2π) ω Γ_{s,j}(ω) / (e^{ω/T} ∓ 1).

Nothing else is assumed. No numerical value is quoted.

## 1. Flux and Γ

For real V the Wronskian W[ψ, ψ̄] = ψ ψ̄' − ψ̄ ψ' is r*-independent. At the horizon (ψ = e^{−iωr*}) it is
−2iω·(−1)… explicitly W = ψψ̄' − ψ̄ψ' = (e^{−iωr*})(iω e^{iωr*}) − (e^{iωr*})(−iω e^{−iωr*}) = 2iω.
At infinity, W = 2iω(|A_in|² − |A_out|²). Hence

    |A_in|² − |A_out|² = 1,      Γ = (transmitted flux)/(incident flux) = ω·1 / (ω|A_in|²) = 1/|A_in|² .

So Γ ∈ [0, 1] automatically and is obtained from |A_in| alone (no cancellation even when Γ ≪ 1).
The identity |A_in|² − |A_out|² = 1 is a free numerical check (route 2a).

## 2. Near-horizon boundary condition

With x = r − 2, f = x/(x+2), and dx/dr* = f. Inverting r*: r*/2 − 1 = x/2 + ln(x/2), so
x = 2 W₀(e^{r*/2 − 1}) (Lambert W). Near the horizon f ≈ e^{(r*−2)/2} → 0 exponentially.

Write ψ = e^{−iωr*} u. Then u'' − 2iω u' − V u = 0. Bosons: V ≈ V₁ f with V₁ = L/4 + κ/8 (value of V/f at r = 2), and
f' = f·f_r → f/2, so u = 1 + c f with c(1/4 − iω) = V₁, i.e. c = V₁/(1/4 − iω). For fermions V ≈ (W_r f) ~ ±(k/8)√f,
so the leading correction is O(√f). I start at r*_min = −80 (f ~ e^{−41}, √f ~ e^{−20.5} ≈ 1e−9) where the
correction is negligible, and impose ψ = e^{−iωr*}, ψ' = −iω e^{−iωr*} (plus the O(f) boson correction for safety).
x is carried as an ODE variable (dx/dr* = x/(x+2)) so r − 2 never underflows against 2.

## 3. Interior integration

Stage 1, variable r*: state (x, ψ, ψ'), from r*_min to r*_a = r*(r = 3) = 3 + 2 ln(1/2). Check: the integrated x at r*_a
must equal 1 (consistency check on x(r*)).
Stage 2, variable r (no horizon singularity for r ≥ 3): dψ/dr = χ/f, dχ/dr = (V − ω²)ψ/f, χ = dψ/dr*, from r = 3 to R.
Both with DOP853 at rtol 1e−11 (complex state split into real/imag).

Fermion potential in closed form (sign +): dW/dr = k[f_r/(2√f r) − √f/r²] = (k√f/r²)[1/(f r) − 1], so
dW/dr* = f dW/dr = (k√f/r²)(3/r − 1), and

    V₊ = k² f/r² − k√f (1 − 3/r)/r² ,     V₋ = k² f/r² + k√f (1 − 3/r)/r² .

## 4. Asymptotic solutions at large r (exact series, used for matching at finite R)

Write ψ_ε = e^{iεωr*} u_ε(r), ε = ±1. Using d/dr* = f d/dr:
ψ'' = e^{iεωr*}[−ω² u + 2iεω f u_r + f (f u_r)_r], so the equation becomes

    (f u_r)_r + 2iεω u_r − (V/f) u = 0 ,    (f u_r)_r = f u_rr + (2/r²) u_r .

Expand V/f = Σ_{p≥2} v_p r^{−p} and u = Σ_{n≥0} a_n r^{−n}, a_0 = 1. Collecting r^{−n−2}:

    2iεω(n+1) a_{n+1} = n(n+1) a_n − 2(n² − 1) a_{n−1} − Σ_{p=2}^{n+2} v_p a_{n+2−p}.

(the −2(n−1)n a_{n−1} from −(2/r)u_rr and the −2(n−1)a_{n−1} from (2/r²)u_r combine to −2(n²−1)a_{n−1}.)

* Bosons: v_2 = L, v_3 = κ, others 0, giving a_{n+1} = {[n(n+1) − L] a_n − 2(n² − s²) a_{n−1}} / [2iεω(n+1)].
* Fermions: V/f = k²/r² ∓ k (1 − 3/r) r^{−2} f^{−1/2}, f^{−1/2} = Σ_m C(2m,m)4^{−m} (2/r)^m = Σ_m b_m r^{−m},
  b_m = C(2m,m)/2^m. So v_p = k² δ_{p2} ∓ k (b_{p−2} − 3 b_{p−3}) (upper sign for V₊). v_2 = k² ∓ k.

The series is asymptotic: for large n, |a_{n+1}/a_n| ≈ n/(2ωR) per power of 1/R, so the smallest term occurs near
n ≈ 2ωR with size ~ e^{−2ωR}; early terms need L/(2ωR) < 1. I pick R = max(60, (30 + L_eff)/ω), L_eff = L (bosons) or
k² (fermions), and sum until the term falls below 1e−17 relative or starts to grow. Then

    ψ(R)  = A_in ψ_−(R) + A_out ψ_+(R),   χ(R) = A_in χ_−(R) + A_out χ_+(R),
    χ_ε = e^{iεωr*}(iεω u_ε + f u_ε,r),

solved as a 2×2 linear system; Γ = 1/|A_in|².

## 5. Low-frequency and high-frequency limits (analytic checks, route 2b)

* ω → 0, s = 0, j = 0 (matched asymptotics). Near zone (ω ≪ 1/r): static solutions of (r² f ψ̃_r)_r = 0 for ψ = rψ̃:
  ψ̃ = const + C ln f; the horizon-regular ingoing solution ψ̃ ≈ e^{−iωr*} ≈ 1 − iω r* matches, at r* near the horizon,
  ln f term: −iω r* ≈ −iω·2 ln f + …, so C = −2iω and the far-zone (flat, r ≫ 2) solution is ψ̃ ≈ 1 + C·(−2/r) =
  1 + 4iω/r. Far zone: ψ̃ = α j₀(ωr) + β y₀(ωr) with j₀ → 1, y₀ → −1/(ωr): α = 1, β = −4iω². Then
  ψ = rψ̃ ≈ sin(ωr)/ω + O(ω) cos(ωr), whose e^{−iωr} coefficient is i/(2ω) + O(ω): |A_in| ≈ 1/(2ω).
  The transmitted amplitude of ψ = rψ̃ at the horizon is r_h = 2 (not 1), so
  Γ = |T|²/|A_in|² = r_h²·4ω² = 16ω². Equivalently σ_abs = πΓ/ω² = 16π = horizon area 4π r_h².
* General low-ω power laws: in the far zone the barrier L_eff/r² tunnels with Γ ∝ (ω)^{2ℓ_eff+2} where
  ℓ_eff(ℓ_eff+1) = v_2. Bosons: ℓ_eff = j ⇒ Γ ∝ ω^{2j+2}. Fermions (V₊): v_2 = k² − k = (j − 1/2)(j + 1/2) ⇒ ℓ_eff = j − 1/2 ⇒
  Γ ∝ ω^{2j+1}. (For V₋ the 1/r² coefficient is k(k+1) but the √f tail changes the near-zone; the exact equality of
  V₊ and V₋ transmission (supersymmetric partners, §6) settles the power. I use V₊ as the main route.)
* ω → ∞ geometric optics: Γ_j ≈ 1 for j + 1/2 < b_c ω and 0 otherwise, where b_c² = max over r of r²/f... capture
  impact parameter b_c = 1/max(√V/ω) at large j: V ≈ f j²/r², max of f/r² at r = 3 gives 1/27, so b_c = 3√3. Then
  Σ (2j+1)Γ_j ≈ (b_c ω)² = 27ω²: the classical capture cross section 27π (in M²).

## 6. Second routes used in code (__main__)

(a) Flux identity |A_in|² − |A_out|² = 1 at moderate ω.
(b) Fermions: Γ from V₊ and from V₋ must agree (they come from the first-order Dirac system
    (d/dr* − W)F = iωG, (d/dr* + W)G = iωF; F obeys V = W² + W', G obeys V = W² − W', and a pure-ingoing F at the horizon
    maps to a pure-ingoing G with |G| = |F| at both ends, so Γ₊ = Γ₋).
(c) Matching-radius convergence: R doubled ⇒ Γ unchanged; and r*_min halved/doubled.
(d) Power: main route Gauss–Legendre panels on ω ∈ [0, ω_max]; second route scipy.integrate.quad per partial wave.
    Convergence: ω_max doubled, node count doubled, j_max raised.
(e) Limits: Γ₀₀/ω² → 16, Σ(2j+1)Γ/ω² → 27.

## 7. Emission integral

P_s = Σ_j (2j+1) ∫₀^{ω_max} (dω/2π) ω Γ_{s,j}(ω)/(e^{8πω} ∓ 1). As ω → 0, Γ ∝ ω^{≥2} so the integrand → 0 (for bosons
ω Γ/(e^{8πω}−1) ~ ω^{2j+2}/(8π) ). ω_max = 2.5: the Boltzmann factor e^{−8π·2.5} ≈ e^{−63} makes the tail
negligible even with Γ·(2j+1) summed ~ 27ω². Partial waves j = s, s+1, … until the contribution of a wave is < 1e−10
of the running total (Γ_j at fixed ω falls exponentially once j ≫ 3√3 ω).

## 8. Not derived

Nothing numerical is quoted. The low-ω limit in §5 is derived only to leading order (sketch by matched asymptotics)
and is used as a check, not as an input.

## 9. Implementation notes and results of the second routes (output of `python3 greybody.py`, main_out.txt)

* Asymptotic series implemented with scaled coefficients b_n = a_n R^{−n} (no overflow), summed to n ≈ 2ωR or until
  three consecutive terms are < 1e−18 (single exact zeros occur, e.g. a_2 = 0 for s = 1, j = 1, so "stop when a term
  grows" is wrong; this was a bug in the first draft, caught by the flux identity).
* Flux identity |A_in|² − |A_out|² = 1 holds to ~1e−11 (moderate ω).
* Fermions: Γ(V₊) = Γ(V₋) to all printed digits (10) at ω = 0.05 … 1.
* R → 2R changes Γ by ≤ 1e−11; r*_min → 2 r*_min by ≤ 4e−10 (including Γ₂₂(0.01) ≈ 1.2e−12).
* Γ₀₀/ω² = 16.208, 16.541, 17.143 at ω = 0.002, 0.005, 0.01: linear in ω, extrapolating to ≈ 16.0 at ω → 0 (§5).
* Σ(2j+1)Γ/ω² at ω = 1, 2, 3 approaches 27 with the expected oscillating finite-ω corrections
  (s = 0: 26.18, 26.71, 27.17; s = 1/2: 27.83, 27.22, 26.83).
* Power: ω_max 2.5 → 5, Gauss–Legendre nodes 32 → 64 per panel, j cutoff 1e−10 → 1e−13, and the independent
  scipy.quad route all agree to ≤ 3e−11 relative. Claimed tolerance on P_s: 1e−8 relative.
  The quad route reuses the same Γ (it checks the ω-integration and j-sum); Γ itself is checked by the flux identity,
  the fermion partner potential, the R and r*_min convergence, and the two analytic limits.
