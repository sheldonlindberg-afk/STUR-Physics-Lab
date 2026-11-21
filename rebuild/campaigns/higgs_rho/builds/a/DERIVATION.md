# DERIVATION: Higgs-mass dependence of rho at one loop (build higgs_rho-a)

All postulates from SPEC.md section 1 (Lagrangian, field definitions, R_xi gauge) and section 2 (observable).

## 1. Tree level (SPEC 1)

tau^a are the Pauli matrices. With W^± = (W^1 ∓ iW^2)/√2, W^3 = cZ + sA, B = −sZ + cA and g' = g s/c,

    g W^a tau^a/2 + g' B/2 = [[ eA + g(c²−s²)/(2c) Z ,  g W⁺/√2 ],
                              [ g W⁻/√2              , −g/(2c) Z ]]      (the A coupling of the lower entry cancels: g s − g' c = 0)

so with Φ = (φ⁺, (v+H+iφ⁰)/√2):

    (DΦ)_1 = ∂φ⁺ − i[eA + g(c²−s²)/(2c) Z] φ⁺ − i (g/2) W⁺ (v+H+iφ⁰)
    √2 (DΦ)_2 = ∂H + i∂φ⁰ − i g W⁻ φ⁺ + i (g/2c) Z (v+H) − (g/2c) Z φ⁰ .

Expanding |DΦ|² (done by hand and mechanically with sympy, tmp/vertices.py; both agree) gives the H-containing terms

    L ⊃ (g²/4)(v+H)² W⁺W⁻ + (g²/8c²)(v+H)² Z Z
      + (ig/2) [ W⁻^μ (H∂_μφ⁺ − φ⁺∂_μH) − W⁺^μ (H∂_μφ⁻ − φ⁻∂_μH) ]
      + (g/2c) Z^μ (H∂_μφ⁰ − φ⁰∂_μH)
      + mixing  M_W (i W⁻·∂φ⁺ − i W⁺·∂φ⁻) + M_Z Z·∂φ⁰ ,

hence M_W = g v/2, M_Z = g v/(2c) (so M_W = c M_Z), M_A = 0. The potential: ∂V/∂v = 0 gives μ² = λv², then
m_H² = 2λv² and the Goldstone mass terms vanish (they get ξ M_V² only from gauge fixing).

R_ξ gauge fixing (SPEC 1): F^± = ∂·W^± ∓ i ξ M_W φ^±, F_Z = ∂·Z − ξ M_Z φ⁰, L_gf = −(1/ξ)|F^+|² − (1/2ξ)F_Z² (with the
photon F_A = ∂·A). The cross terms ±(i M_W) ∂·W φ integrate by parts into exactly minus the mixing terms above, and
−ξ M_W² φ⁺φ⁻, −½ ξ M_Z² φ⁰² give the Goldstones mass² ξ M_V². The gauge propagator is

    D^{μν}_V(k) = −i/(k²−M²) [ g^{μν} − (1−ξ) k^μk^ν/(k²−ξM²) ] ,  Goldstone i/(k²−ξM²),  Higgs i/(k²−m_H²).

Feynman rules: vertex = i × (coefficient in L) × (symmetry factor), all momenta incoming, ∂_μ acting on a field with
incoming momentum p → −i p_μ. Every rule below carries its explicit factor of i (sympy coefficients from tmp/vertices.py:
W⁻ H ∂φ⁺: +ig/2, W⁻ φ⁺ ∂H: −ig/2, W⁺ H ∂φ⁻: −ig/2, W⁺ φ⁻ ∂H: +ig/2, Z H ∂φ⁰: g/2c, Z φ⁰ ∂H: −g/2c):

| vertex | W | Z |
|---|---|---|
| H V V | i · (g²v/2) g^{μν} = i g M_W g^{μν} | i · (g²v/4c²) · 2 g^{μν} = i (g/c) M_Z g^{μν} |
| H H V V | i · (g²/4) · 2 g^{μν} = i (g²/2) g^{μν} | i · (g²/8c²) · 2·2 g^{μν} = i (g²/2c²) g^{μν} |
| V φ H | W⁻_μ φ⁺ H: i · (ig/2)(−i p_φ⁺ + i p_H)_μ = **i (g/2)(p_φ⁺ − p_H)_μ** | Z_μ φ⁰ H: i · (g/2c)(−i p_φ⁰ + i p_H)_μ = **(g/2c)(p_φ⁰ − p_H)_μ** |
|  | W⁺_μ φ⁻ H: i · (−ig/2)(−i p_φ⁻ + i p_H)_μ = **−i (g/2)(p_φ⁻ − p_H)_μ** |  |

Sign of the product of the two V–φ–H vertices in each H–φ bubble (q = 0; H carries k from vertex A to vertex B, so at A
p_H = −k, p_φ = +k and at B p_H = +k, p_φ = −k):

* W bubble: the Goldstone line is a ⟨φ⁺φ⁻⟩ propagator, so one vertex is the W⁻φ⁺H rule and the other the W⁺φ⁻H rule.
  A: i(g/2)(k + k)^μ = i g k^μ;  B: −i(g/2)(−k − k)^ν = i g k^ν;  product (ig)(ig) k^μk^ν = **−g² k^μk^ν**.
* Z bubble: A: (g/2c)(2k)^μ = (g/c)k^μ;  B: (g/2c)(−2k)^ν = −(g/c)k^ν;  product **−(g/c)² k^μk^ν**.

Both are −κ² k^μk^ν with κ = g (W), g/c (Z): the factors of i in the W rules square to the same sign as the real Z rules.
(Relabelling which end is A, or which vertex sits on which external leg, gives the same product.)

Key structural fact: **every Z vertex is the W vertex with g → κ_Z = g/c and M_W → M_Z** (and the Goldstone mass
ξM_W² → ξM_Z²). So Π_WW = g² h(M_W), Π_ZZ = (g²/c²) h(M_Z) with one function h(M) (κ = g for W, g/c for Z).

## 2. Ghosts and tadpoles

Ghosts: ghost fields enter only bilinearly (c̄ … c). A one-loop 1PI two-point function of V containing a ghost is a closed
ghost loop with two V-ghost-ghost vertices: no H line. The only H–ghost coupling (H c̄ c ∝ ξ) can only enter through
an H tadpole, which is dropped. So no ghost diagram contains an H at one loop and ghosts are not needed.

Tadpoles: an H tadpole T attaches through the HVV vertex: Π^tad_WW = g M_W · (T/m_H²) ·(…) and Π^tad_ZZ = (g/c) M_Z ·(same).
Then Π^tad_WW/M_W² = g(…)/M_W and Π^tad_ZZ/M_Z² = g(…)/(c M_Z) = g(…)/M_W: equal, so they cancel in Δρ (physically a tadpole
is a shift δv, and δM_V²/M_V² = 2δv/v for both).

No mixed or photon loops with an H. Topology first: a one-loop two-point diagram has either one quartic vertex and one
propagator (seagull) or two cubic vertices and two propagators (bubble); quartic + cubic leaves an odd number of internal
legs, and two quartic vertices make two loops; two cubics joined by one line to a third are tadpoles (dropped). The complete
list of H-containing couplings to gauge fields from |DΦ|² (tmp/vertices.py prints every monomial) is

    H W⁺W⁻, H Z Z, H H W⁺W⁻, H H Z Z, W^∓ φ^± H (derivative), Z φ⁰ H (derivative),
    H φ^∓ W^± Z  (coefficient g²(c²−1)/(2c)),  H φ^∓ W^± A  (coefficient g² s/2).

There is no H Z A, H A A, H W Z or H W A vertex (the photon drops out of the lower component of the covariant derivative,
gs − g'c = 0, and H is neutral, so an H plus one W can only be accompanied by a charged W or φ). Hence:
* a bubble on W⁺W⁻ containing H has internal lines (H, W) or (H, φ); on ZZ, (H, Z) or (H, φ⁰). No W–Z, W–γ, Z–γ or γ–γ
  internal pair can appear together with an H;
* a seagull needs both external legs on one quartic vertex. H φ W Z and H φ W A each carry only one W and at most one Z,
  so they have no W⁺W⁻ pair and no Z Z pair, and their remaining legs (H, φ) cannot close on each other (there is no H–φ
  propagator). They cannot contribute to Π_WW or Π_ZZ at one loop (they only enter W–Z / W–γ mixing at this order, which
  is not part of Δρ). The only H seagulls are H H W⁺W⁻ and H H Z Z.

## 3. One-loop integrals (dim. reg., d = 4 − 2ε, MS-bar)

    (i/16π²) A0(m)          = μ^{2ε} ∫ d^dk/(2π)^d 1/(k²−m²)
    (i/16π²) B0(0;m1,m2)    = μ^{2ε} ∫ 1/((k²−m1²)(k²−m2²))
    (i/16π²) g^{μν} B00(0;m1,m2) = μ^{2ε} ∫ k^μk^ν/((k²−m1²)(k²−m2²))

With Δ = 1/ε − γ + ln4π, A0 = m²(Δ + 1 − ln m²/μ²). Partial fractions give B0 = (A0(m1) − A0(m2))/(m1²−m2²). For B00:
k^μk^ν → g^{μν} k²/d, k²/((k²−m1²)(k²−m2²)) reduces to (m1² A0(m1) − m2² A0(m2))/(m1²−m2²), and 1/d = ¼(1 + ε/2 + …) times the
pole ¼(m1⁴−m2⁴)/(m1²−m2²)/ε gives a finite extra term:

    B00(0;m1,m2) = ¼ [ (m1² A0(m1) − m2² A0(m2))/(m1²−m2²) + (m1² + m2²)/2 ] .

MS-bar: drop Δ. Equal-mass limits: B0(0;m,m) = −ln(m²/μ²); (m1²A0(m1)−m2²A0(m2))/(m1²−m2²) → m²(1 − 2 ln m²/μ²).

## 4. The three diagrams (SPEC 2), vertex coupling κ, gauge mass M, q = 0

Convention: the sum of 1PI diagrams is i Π g^{μν} (the tree mass term gives i M² g^{μν}), so M²(eff) = M² + Π.

(a) Seagull with an H loop (symmetry ½):  iΠ = ½ (iκ²/2) ∫ i/(k²−m_H²) = −i κ² A0(m_H)/(4·16π²),

    16π² Π_a = −κ² A0(m_H)/4 .

(b) H–Goldstone loop: vertex 1 (outgoing H k, φ −k) gives κ k^μ, vertex 2 gives −κ k^ν:
iΠ^{μν} = ∫ (−κ² k^μk^ν) i/(k²−m_H²) i/(k²−ξM²), so

    16π² Π_b = +κ² B00(0; m_H, √ξ M) .

(c) H–gauge loop: iΠ^{μν} = (iκM)² ∫ i/(k²−m_H²) (−i)[g^{μν} − (1−ξ)k^μk^ν/(k²−ξM²)]/(k²−M²). Using
(1−ξ)/((k²−M²)(k²−ξM²)) = [1/(k²−M²) − 1/(k²−ξM²)]/M²,

    16π² Π_c = −κ² [ M² B0(0;m_H,M) − B00(0;m_H,M) + B00(0;m_H,√ξM) ] .

Sum: the B00(m_H, √ξM) terms cancel between (b) and (c), so **the result is exactly ξ-independent**:

    16π² h(M) = −M² B0(0;m_H,M) + B00(0;m_H,M) − A0(m_H)/4 ,   Π_WW = g² h(M_W),  Π_ZZ = (g²/c²) h(M_Z).

Pole part: [−M² + ¼(m_H²+M²) − ¼m_H²] Δ = −¾ M² Δ: m_H-independent. In Δρ:

    Δρ = Π_WW/M_W² − Π_ZZ/M_Z² = (g²/M_W²) [ h(M_W) − h(M_Z) ]       (c²M_Z² = M_W²)

with g² = 4πα/s², s² = 1 − M_W²/M_Z². The pole of Δρ is −(3g²/64π²)(M_W²−M_Z²)Δ/M_W², independent of m_H, so in
Δρ(m_H) − Δρ(M_W) the poles cancel and with them the ln μ² dependence (μ appears only as ln(m²/μ²) multiplying the pole
coefficients). This is what `rho_higgs_rel` returns; it is linear in α at fixed masses. Custodial limit: h(M_W) − h(M_Z) is
O(M_Z² − M_W²), so Δρ = O(g² s²/c²) = O(g'²) → 0 as g' → 0 (see section 7 about the blind check).

## 5. Large-m_H coefficient B

With L_H = ln(m_H²/μ²), L = ln(M²/μ²) and m_H ≫ M:
A0(m_H) = m_H²(1 − L_H); B0 = 1 − L_H + O(M²/m_H² · L_H);
(m_H²A0(m_H) − M²A0(M))/(m_H²−M²) = (m_H² + M²)(1 − L_H) + O(M⁴/m_H² · L_H). Hence

    16π² h(M) = −M²(1−L_H) + ¼(m_H²+M²)(1−L_H) + ⅛(m_H²+M²) − ¼m_H²(1−L_H) + O(M⁴ L_H/m_H²)
              = ¾ M² L_H + (M-independent m_H² terms) + O(M²) constants + o(1).

Only the M-dependent part survives in h(M_W) − h(M_Z), so

    Δρ → (g²/(16π² M_W²)) · ¾ (M_W² − M_Z²) ln m_H² = −(3 g²/(64π²)) (s²/c²) ln m_H²,

    B = −3 g² s²/(64π² c²) = −3α/(16π c²)       (c² = M_W²/M_Z²).

How the export is obtained: `log_coefficient` evaluates B = g² · a · (M_W² − M_Z²)/(16π² M_W²) with g² = 4πα/s², where
a = lim_{m_H→∞} ∂/∂M² [∂(16π² h)/∂ ln m_H²] is the M²-dependent coefficient of ln m_H² in the expansion above. The hand
expansion gives a = 3/4; the sympy limit of the closed form h (run in `__main__`) gives exactly 3/4; and `__main__` also
evaluates the limit numerically from rho_higgs_rel itself: the ratio Δρ_rel(m_H)/ln(m_H²/M_W²) (which converges only
like 1/ln m_H, because of the constant term) and the secant slope between successive large m_H (which converges like
M²/m_H²), both compared with the export. Output: ratio/B = 0.828, 0.914, 0.957, 0.978, 0.989, 0.995 at
m_H = 10², 10⁴, …, 10⁶⁴ M_W (approaching 1 like 1/ln m_H); one Richardson step on (L, 2L), which for L₂ = 2L₁ is algebraically
the same as the secant slope, gives B to 1e-12 relative from 10¹⁶ M_W on (2e-8 at 10⁸ M_W). (The limit of the ratio and the coefficient of ln m_H² are the same number.)

The ξ cancellation of section 4 means B is ξ-independent; `log_coefficient` ignores xi on that ground.

## 6. Independent second routes

(i) **Direct 4-dimensional Euclidean integration with the explicit R_ξ propagators** (no PV reduction, no cancellation
of ξ assumed). Wick rotation k⁰ = i k_4, K = k_E²: (i/16π²)X = ∫d^dk/(2π)^d F(k²) becomes X = ∫_0^∞ dK K F(−K), with
k^μk^ν → g^{μν}k²/4. Per unit κ², 16π² Π(M) has integrand

    K { K/(4(K+m_H²)) − K/(4(K+m_H²)(K+ξM²))
        − M² [ 1/((K+m_H²)(K+M²)) − (1−ξ)(K/4)/((K+m_H²)(K+M²)(K+ξM²)) ] } .

The double difference [I(m_H,M_W) − I(m_H,M_Z)] − [I(M_W,M_W) − I(M_W,M_Z)] falls like 1/K² and is integrated
numerically (mpmath). The dim-reg/4D difference (the 1/d term in B00) is a polynomial a m_H² + b M² which cancels in
this double difference, so the result must equal rho_higgs_rel for any ξ.

(ii) **B from a sympy series** of the closed form at m_H → ∞, compared with the analytic −3α/(16πc²), and a numerical
slope of rho_higgs_rel at m_H ~ 10⁵–10⁶ M_W computed in high precision.

(iii) The Feynman rules were re-derived mechanically from the Lagrangian with sympy (tmp/vertices.py).

## 7. Numerics, accuracy, and the custodial blind check

All arithmetic is done in mpmath with 50 + 2 log10(max mass/min mass) + 1 significant digits (the m_H² terms cancel
between W and Z only in the difference, which costs ~2 log10(m_H/M_W) digits), then returned as float: exports are accurate
to double precision for any m_H. (Until the second revision the precision was a fixed 50 digits, which is exact to double
precision up to m_H ~ 10¹⁷ M_W but loses the result beyond ~10²⁵ M_W; the change leaves every export bit-identical for
m_H ≤ 10⁶ M_W, ξ ∈ {0, 1, 3}, μ ∈ {M_W, 3.7 M_W}, checked in tmp/cmp.py.)

Landau gauge (SPEC 2 now requires every ξ ≥ 0): the cancellation of B00(m_H, √ξ M) between diagrams (b) and (c) is an
algebraic identity that holds at ξ = 0 as well (B00(0; m_H, 0) is finite), and the Euclidean integrand of route (i) is
regular at ξ = 0; route (i) at ξ = 0 agrees with the closed form to all printed digits.

Conventions: SPEC 2 now pins the tensor reduction k^μk^ν → g^{μν}k²/d with the O(ε) part of 1/d kept, μ^{2ε} in the
measure, Δ = 1/ε − γ_E + ln4π dropped, and 1PI sum = iΠ g^{μν}. These are exactly the conventions used in sections 3–4. μ-independence holds to rounding; ξ-independence is exact algebraically and checked numerically by route (i).

Custodial check: the derived Δρ is ∝ g² s²/c² = g'² at fixed g (h(M_W) − h(M_Z) = O(M_Z² − M_W²)), i.e. Δρ/α tends to a
constant as s² → 0 at fixed g (numerically Δρ/s² → −0.00407 at m_H = 400 GeV for ε = 4e-3 … 5e-4). The version of
campaign.b_custodial I first read divided by α·s² (∝ s⁴ at fixed g), which would contradict its own docstring and this
result (the ratio would be ≈ 2, not 1); the file was replaced during the build (mtime 06:08:58) by one dividing by α,
which this honest result passes. Nothing in the build was changed in response.

Route (i) numerics: the O(K) pieces of the integrand cancel, so it is integrated in u = ln K at 90 digits up to
K_max = max(m_H², M_Z²)·e³⁰, with the f ~ C/K² tail added as f(K_max)K_max. It agrees with the closed form to all 12 printed
digits for ξ = 0, 0.4, 1, 3 and m_H = 50 … 1000 GeV. Route (ii): sympy gives lim d/dM² [d(16π²h)/d ln m_H²] = 3/4 exactly,
reproducing B; the numerical slope at 10⁵–10⁶ M_W agrees with B to 1e-9 relative.
