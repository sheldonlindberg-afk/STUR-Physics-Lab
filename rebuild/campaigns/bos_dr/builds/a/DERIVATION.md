# DERIVATION: bosonic one-loop on-shell Delta r of muon decay (build bos_dr-a)

All conventions are those of SPEC section 1. Notation: `c = M_W/M_Z`, `s^2 = 1 - c^2`, `e = g s`,
`a = g^2/(16 pi^2) = alpha/(4 pi s^2)`, `L_m = ln(m^2/mu^2)`. Loop integrals are normalised as
`int_n f = (2 pi mu)^(4-d)/(i pi^2) int d^dq f`, so that `int d^4q/(2pi)^4 f = (i/16 pi^2) int_n f`. Dimensional
regularisation with `d = 4 - 2 eps`, anticommuting gamma5 (NDR), MS-bar (`1/eps - gamma + ln 4pi` dropped) --
the same scheme as the provided `bos_se` (it keeps the O(eps) part of d-dependent coefficients against the pole; so do I).

## 0. Postulates used

* SPEC 1: Lagrangian, `D = d - i g W^a T^a - i g' Y B`, `W^± = (W1 ∓ i W2)/√2`, `W3 = c Z + s A`, `B = -s Z + c A`,
  `g' = g s/c`, 't Hooft-Feynman gauge, massless leptons.
* SPEC 2: the transverse bosonic self-energies of `bos_se`, sign convention: inverse propagator `k^2 - M^2 + Sigma_T`,
  `+Sigma^AZ` off-diagonal; `Sigma_T = -Pi_T` (Pi = sum of 1PI diagrams / i).
* SPEC 3: on-shell inputs `M_W, M_Z` (poles), `s^2 = 1 - M_W^2/M_Z^2`, `alpha` from the Thomson limit, `G_F` from
  muon decay at zero momentum transfer with the Fermi-model QED correction removed.

## 1. Feynman rules (derived from the Lagrangian)

Fermion part `L = psibar i gamma.D psi  ⊃  psibar gamma^mu (g W^a T^a + g' Y B) psi`. Written with the
mass-basis fields, the vertex of a left-handed doublet with boson X is `i gamma^mu P_L G^X`, with the 2x2 doublet
matrices

    G^{W1} = g T1, G^{W2} = g T2, G^Z = (g/c)(T3 - s^2 Q) = (g/c)(c^2 T3 - s^2 Y), G^A = e Q,  Q = T3 + Y, Y = -1/2.

(`g T3 W3 + g' Y B = Z (g c T3 - g' s Y) + A g s (T3 + Y)`.) In the charged basis the W vertex is
`i (g/√2) gamma^mu P_L = i g/(2√2) gamma^mu (1 - gamma5)` (since `W1 T1 + W2 T2 = (W^+ T^+ + W^- T^-)/√2`).
Right-handed charged lepton: `G^Z_R = -(g/c) s^2 Q`, `G^A_R = e Q`, no W. Goldstone and Higgs couplings to the
leptons are proportional to the lepton mass and vanish; ghosts do not couple to fermions.

Triple gauge vertex: `-1/4 F^a F^a` with `F^a = dW^a - dW^a + g eps^{abc} W^b W^c` gives, for all momenta
incoming, `g eps^{abc} [g^{μν}(k1-k2)^ρ + g^{νρ}(k2-k3)^μ + g^{ρμ}(k3-k1)^ν]`; replacing `W3 -> c Z + s A`
multiplies the vertex by `κ_Z = c` or `κ_A = s` for each neutral leg. Propagators: vector `-i g^{μν}/(k^2-M^2)`
(photon with a mass `λ` to regulate the IR), fermion `i qslash/q^2`.

Higgs-sector couplings (used only for the high-precision M_H dependence, section 7): from `|Dφ|^2` with
`φ = (φ^+, (v + H + iχ)/√2)`, `v = 2 M_W/g`: `H W^+ W^-: i g M_W g^{μν}`, `H Z Z: i (g M_Z/c) g^{μν}`,
`H H W^+ W^-: i g^2/2 g^{μν}`, `H H Z Z: i g^2/(2c^2) g^{μν}`, `W^± φ^∓ H: (g/2)(p_H - p_φ)` (up to a phase),
`Z χ H: (g/(2c))(p_H - p_χ)` (from `(g/2c) Z (h dχ - χ dh)`).

## 2. Integrals at zero external momenta

With all external momenta zero (muon decay at zero momentum transfer, massless leptons) every vertex, box and
lepton self-energy derivative is a one-scale-per-propagator integral `int_n (q^2)^n / prod (q^2 - m_i^2)^{k_i}`.
`q^μ q^ν -> g^{μν} q^2/d`. Partial fractions in `x = q^2` reduce it to

    T_k(m) = int_n 1/(q^2 - m^2)^k :  T_1 = m^2 (1/eps + 1 - L_m),  T_2 = 1/eps - L_m,
    T_k = (-1)^k (k-3)!/(k-1)! m^(4-2k)  (k >= 3),     and  int_n (q^2)^j = int_n 1/(q^2)^j = 0  (scaleless).

`T_{k+1} = (1/k) dT_k/dm^2`. A massless pole `1/x^k` with `k >= 2` would be a genuine IR divergence: the code asserts
that none survives except through the photon mass `λ`. Then `c(d) T = c(4) T|_fin + c(4)/eps + (-2 c'(4)) Res`, the
last term being the O(eps) x pole piece (MS-bar). Needed values: `B0(0,0,M) = T_1(M)/M^2 = 1/eps + 1 - L_M`,
`B0(0,M,M) = 1/eps - L_M`, `B0(0,M1,M2) = 1/eps + 1 - (M1^2 L_1 - M2^2 L_2)/(M1^2 - M2^2)`.

## 3. Dirac algebra

d-dimensional contraction (`{γ^μ,γ^ν} = 2 g^{μν}`, `γ^ρ γ_ρ = d`), implemented as a small recursive engine and checked
at d = 4 against explicit 4x4 matrices:

* (V) `γ^ρ qslash γ^α qslash γ_ρ -> (q^2/d) γ^ρ γ^σ γ^α γ_σ γ_ρ = (d-2)^2/d q^2 γ^α`.
* (Σ) `γ^ρ (pslash + qslash) γ_ρ / (p+q)^2 = -(d-2) [pslash/q^2 - 2 qslash (p.q)/q^4] + O(p^2) -> -(d-2)^2/d pslash / q^2`.
* (NA) `γ^ρ qslash γ^σ [g_{αρ} q_σ - 2 g_{ρσ} q_α + g_{σα} q_ρ] -> (2 + 2(d-2)/d) q^2 γ_α`.
* Boxes are UV finite (`~ int d^4q q^2/q^8`), so d = 4 is used: with `q^μ q^ν -> q^2 g^{μν}/4`,
  `γ^α γ^σ γ^ρ P_L ⊗ γ_α γ_σ γ_ρ P_L = 16 γ^α P_L ⊗ γ_α P_L` (same order) and
  `γ^α γ^σ γ^ρ P_L ⊗ γ_ρ γ_σ γ_α P_L = 4 γ^α P_L ⊗ γ_α P_L` (reversed order); both computed numerically with explicit
  matrices in the code.

## 4. One-loop pieces (coefficients multiply `i γ^α P_L`)

Vertex corrections are written as doublet matrices `M^a` for the external real field `W^a` (a = 1,2), compared with the
tree coupling `g T^a`. The relative correction of the vertex `ν̄_μ μ W` is
`δ_1 = Σ_a M^a_{12} T^a_{21} / (g Σ_a T^a_{12} T^a_{21})`, of `ē ν_e W`: `δ_2 = Σ_a T^a_{12} M^a_{21} / (g Σ_a T^a_{12} T^a_{21})`.

(a) boson X exchanged between the two legs of a vertex (fermion propagators carry q):
`i^3 (i)^2 (-i) = 1`, so `M_(a) = Σ_X G^X (vertex) G^X (d-2)^2/d B0(0,0,M_X)/(16π^2)`. X runs over A, Z, W1, W2
(the W-exchange terms cancel in the sum over a, as they must: no such charge flow exists).

(b) non-abelian triangle (external `W^a` or `A` at the triple vertex, internal X at the outgoing and Y at the incoming
fermion leg, momenta: Y carries q into the triple vertex, X carries q out of it, internal fermion momentum -q):
factor `i^3 (-1)(-i)^2 = -i`, triple vertex `λ_{aXY}[g_{αρ} q_σ - 2 g_{ρσ} q_α + g_{σα} q_ρ]`, so
`M_(b) = -i Σ_{X,Y} λ_{aXY} G^X G^Y (2 + 2(d-2)/d) B0(0,M_X,M_Y)/(16π^2)` with `λ_{aXY} = g ε^{a i(X) i(Y)} κ_X κ_Y`.
By hand: `Σ = i g^3 T^a [c^2 B0(0,M_W,M_Z) + s^2 B0(0,M_W,λ)]`, hence
`δ_NA = a (2 + 2(d-2)/d) [c^2 B0(0,M_W,M_Z) + s^2 B0(0,M_W,λ)]`, the same for both vertices.

(c) lepton self-energy: `-iΣ = Σ_X ∫ (iγ^ρ G^X)(i(p+q)slash/(p+q)^2)(iγ_ρ G^X)(-i/(q^2-M_X^2))`, so
`Σ = pslash P_L Σ_L`, `Σ_L^f = -Σ_X (G^X G^X)_{ff} (d-2)^2/d B0(0,0,M_X)/(16π^2)` (propagator `i/(pslash - Σ)`,
residue `1/(1 - Σ_L)`). LSZ: each of the four external legs gives `+Σ_L^f/2`. (W loop: `Σ_b (T^b T^b) = 1/2`.)
Ward identity check: (a) with X = neutral boson plus the X part of the LSZ factors of the two legs vanishes when
the two legs have the same coupling (abelian `Z_1 = Z_2`).

(d) boxes: one W and one neutral boson V ∈ {γ, Z} between the lines (a WW box would need a doubly charged state; the
doublet algebra gives zero). Loop momentum q in V, -q in W; fermion momenta: V on μ: -q, V on ν_μ: +q, V on e: -q,
V on ν_e: +q. Factor `i^4 (-i)^2 i^2 = +1`, tree `iM_0 = -i g^2/(2 M_W^2) T_0`, so

    δ_box = -(M_W^2/16π^2) Σ_V Σ_orderings (couplings) sgn C ∫_n 1/(q^2 (q^2 - M_V^2)(q^2 - M_W^2)),

with (V on μ, e): sgn +, C = 1 (reversed order); (μ, ν_e): -, 4; (ν_μ, e): -, 4; (ν_μ, ν_e): +, 1.
`∫_n 1/(x(x-M_V^2)(x-M_W^2)) = ln(M_W^2/M_V^2)/(M_V^2 - M_W^2)`; for the photon `-ln(M_W^2/λ^2)/M_W^2`.
Couplings: `g_ν = g/(2c)`, `g_ℓ = (g/c)(s^2 - 1/2)`: Z sum `g_ℓ^2 + g_ν^2 - 8 g_ℓ g_ν`; photon `e^2`.

(e) Fermi theory QED (the subtraction). The four-fermion operator is taken in its charge-retention (Fierzed, d = 4)
form `[ē γ^α P_L μ][ν̄_μ γ_α P_L ν_e]`, the form in which its QED correction is UV finite. At zero momentum with
photon mass λ: vertex `+e^2 (d-2)^2/d B0(0,0,λ)/16π^2`, LSZ of μ and e `2 × (-1/2) e^2 (d-2)^2/d B0(0,0,λ)/16π^2`.
Both contain `ln λ^2` (`∓(α/4π) ln λ^2`); the sum is exactly zero (Ward identity of the conserved vector current,
valid for a massive photon). So `δ_Fermi^virt = 0`; its real emission is identical to the SM one at this order
(radiation off the W is O(1/M_W^2)), so real and virtual IR divergences cancel separately in both theories and the
subtraction removes nothing from the zero-momentum amplitude.

IR cancellation in the SM amplitude: photon box `(α/4π) ln(M_W^2/λ^2)` + photon part of the four LSZ factors
`(α/4π)(1/2 + ln(λ^2/μ^2))` (μ and e) = `(α/4π)(1/2 + ln(M_W^2/μ^2))`: λ drops (checked symbolically in the code:
the coefficient of `ln λ^2` is zero; the W γ triangle `B0(0,M_W,λ)` is IR finite).

UV check of the vertex sum: per vertex the poles are `g_ν g_ℓ - (g_ν^2+g_ℓ^2)/2 - e^2/2 - g^2/2 + 3 g^2 = 2 g^2`,
i.e. `δ_VB` has the pole `4a/eps`; this is cancelled by the self-energy/counterterm part (section 6).

### Closed form at μ = M_W (by hand; `ℓ = ln c^2`)
Per vertex: `δ_a = g_ν g_ℓ (-1/2 + ℓ)`, `δ_NA = g^2 (5/2 + 3 c^2 ℓ/s^2)`, LSZ `-(1/2)[(g_ℓ^2+g_ν^2)(-1/2+ℓ) + e^2(-1/2 - ln λ^2/M_W^2) - g^2/2]`
(units 1/16π^2); box `-(g_ℓ^2+g_ν^2-8 g_ℓ g_ν) c^2 ℓ/s^2 + e^2 ln(M_W^2/λ^2)`. Summing (with `(g_ℓ - g_ν)^2 = g^2 c^2`,
`g_ℓ^2 + g_ν^2 - 8 g_ℓ g_ν = g^2 (s^4 - 5 s^2 + 5/2)/c^2`):

    δ_vb ≡ δ_VB(μ = M_W) = (α/(4π s^2)) [ 6 + (7 - 4 s^2)/(2 s^2) ln c^2 ].

This depends on the masses only through s^2. For general μ, `δ_VB(μ) = δ_vb - (2/(s c)) Σ^AZ_T(0; μ)/M_Z^2` (section 5).

## 5. Charge renormalisation (Thomson limit) and the Ward identity

Photon coupling to a lepton at zero photon momentum, external photon amputated on its pole:
`e_0 Q (1 - Σ'_AA(0)/2) + G^Z Σ^AZ_T(0)/M_Z^2 + [vertex + LSZ]`, where the mixing term comes from
`D_AZ = -Σ^AZ/(k^2 (k^2 - M_Z^2))`, and `Σ^AA_T(0) = 0`. For the right-handed electron the γ and Z loops cancel by the
abelian Ward identity and there is no W loop, so

    e = e_0 [1 - Σ'_AA(0)/2 - (s/c) Σ^AZ_T(0)/M_Z^2],   δe/e = Σ'_AA(0)/2 + (s/c) Σ^AZ_T(0)/M_Z^2.

Universality for the left-handed doublet (W triangle with external A, W loops of type (a), W part of LSZ) requires
`Σ^AZ_T(0)/M_Z^2 = s c a [(d-2)^2/d B0(0,0,M_W) - (2 + 2(d-2)/d) B0(0,M_W,M_W)] = 2 s c a L_W`, i.e.
`Σ^AZ_T(0) = (α/4π)(2 M_W^2/(s c)) ln(M_W^2/μ^2)` (pole `-4 s c a M_Z^2/eps`). This is a *prediction* of my vertex
algebra; the provided `bos_se.sigma_AZ(0)` agrees with it to 1e-15 at several μ (independent check of the triple-vertex
sign and of the conventions shared with stage 1; also the neutrino stays neutral). It vanishes at μ = M_W, and it is
how the leftover vertex divergence is written: `δ_VB(μ) + (2/(s c)) Σ^AZ(0)/M_Z^2` is μ independent.

## 6. Assembly (bare perturbation theory, no field renormalisation needed)

Amplitude `∝ (g_0^2/8) · 1/(M_W0^2 - Σ^W_T(0)) · (1 + δ_1 + δ_2 + δ_box + δ_LSZ - δ_Fermi)`. The W propagator at
`k = 0`: `-i g/(k^2 - M_W0^2 + Σ^W_T)`; its longitudinal part and the W-φ mixing drop because the massless charged
current is conserved (and φ does not couple). On-shell counterterms: `M_W0^2 = M_W^2 + Re Σ^W_T(M_W^2)`,
`M_Z0^2 = M_Z^2 + Re Σ^ZZ_T(M_Z^2)` (mixing enters the Z pole at second order), `s_0^2 = 1 - M_W0^2/M_Z0^2` so
`δs^2/s^2 = (c^2/s^2)(δM_Z^2/M_Z^2 - δM_W^2/M_W^2)`, `g_0^2 = e_0^2/s_0^2`. With `G_F/√2 = g^2/(8 M_W^2)(1+δ)` and
`e^2 = 4πα`: `M_W^2 s^2 = πα/(√2 G_F) (1 + δ)`, so `Δr = δ`:

    Δr_bos = Σ'_AA(0) + 2 (s/c) Σ^AZ(0)/M_Z^2                                [2 δe/e]
             - (c^2/s^2) [Σ^ZZ(M_Z^2)/M_Z^2 - Σ^W(M_W^2)/M_W^2]              [-δs^2/s^2]
             + [Σ^W(0) - Σ^W(M_W^2)]/M_W^2                                   [W propagator + δM_W^2]
             + δ_VB(μ)                                                       [vertices, boxes, LSZ, minus Fermi QED]
           = Σ'_AA(0) - 2 (c/s) Σ^AZ(0)/M_Z^2 - (c^2/s^2)[...] + [...] + δ_vb.

Which counterterms enter: δe (Thomson), δM_W^2, δM_Z^2 (through s^2 and through the bare W mass in the propagator);
the W-ℓ-ν coupling counterterm is just the bare-parameter combination `g_0 = e_0/s_0` (no field counterterms are
needed because LSZ factors are put on the external legs and the internal W is the full bare propagator). Tadpoles are
excluded consistently: they add `∝ M_V^2 × const` to `Σ^W, Σ^ZZ`, which cancels in each bracket above. All self-energies
are evaluated at the same μ (μ = M_W in the exports); μ independence of the sum is the UV check.

## 7. Numerics

* `Σ'_AA(0)`: central differences of `bos_se.sigma_AA` at `k^2 = ±h, ±2h` with `h = 10^-3 M_W^2`, Richardson
  extrapolated (error O(h^4), ~1e-12 relative; the bosonic Σ_AA is analytic below `4M_W^2`); `Σ^AA(0) = 0` checked.
* k^2 = 0 limits are taken by `bos_se` itself (k2 = 0 argument).
* Precision for large M_H. The exports of `bos_se` return doubles, and `Σ^W, Σ^ZZ` contain terms `~ 3.5e-4 M_H^2`
  that cancel in the brackets: at M_H = 1e14 GeV doubles lose everything. Only the Higgs-boson diagrams depend on M_H
  (γ and AZ have no H at one loop). I derived them (section 1 couplings):
  `Σ^W_H(k^2) = (g^2/16π^2)[M_W^2 B0(k^2,M_W,M_H) - B00(k^2;M_H,M_W) + A0(M_H)/4]`,
  `Σ^ZZ_H = (1/c^2) × same with M_W -> M_Z` (VH loop `+g_VVH^2 B0`, φH loop `-4κ^2 B00`, HH seagull `+g_HHVV A0/2`),
  `B00 = [A0(m2) + 2 m1^2 B0 + (k^2 + m1^2 - m2^2) B1]/(2(d-1))`, `B1 = [A0(m1) - A0(m2) - (k^2+m1^2-m2^2) B0]/(2k^2)`,
  `B00(0) = [A0(m2) + m1^2 B0(0)]/d` (MS-bar finite parts with the O(eps) pieces).
  Then `Δr_bos(M_H) = Δr_bos^{bos_se}(M_H^ref) + Δr_H(M_H) - Δr_H(M_H^ref)` with `M_H^ref = M_W` (keeps exact mass-scale
  covariance) and `Δr_H` the Higgs part of the brackets, evaluated with mpmath at a precision set locally
  (`mp.workdps(30 + 6 ceil(log10(max mass/min mass)))` inside the export: B00 holds terms `~ M_H^4/k^2` that cancel
  down to `ln M_H`). Check: the M_H dependence of my `Σ_H` equals that of `bos_se` to ~1e-14
  (k^2 = 0, M_W^2, M_Z^2), and the hybrid equals the pure-`bos_se` assembly at moderate M_H.
* `δ_VB` is assembled symbolically (sympy) from sections 2-4, λ → 0 taken after the `ln λ` coefficient is shown to
  vanish, and evaluated with the same μ.

## 8. Second routes / checks (printed by `python3 bos_dr.py`)

1. Hand closed form of δ_vb (section 4) vs the mechanically assembled sympy result (identical, symbolic difference 0).
2. UV: Δr_bos is μ independent (μ = M_W, 300 GeV, 10 GeV) with `bos_se` self-energies + my δ_VB(μ).
3. IR: coefficient of `ln λ^2` in δ_VB is 0; Fermi-theory virtual sum is 0 identically.
4. Ward identity: predicted `Σ^AZ(0)` vs `bos_se.sigma_AZ(0)`; neutrino photon coupling at q = 0 vanishes.
5. Dirac engine at d = 4 vs explicit matrices; box Fierz coefficients 16 and 4 from explicit matrices.
6. Higgs part vs `bos_se`; large-M_H slope `11α/(48π s^2)`.

## 9. Results of the checks (python3 bos_dr.py)

* Dirac engine: `cV = (d-2)^2/d`, `cS = -(d-2)^2/d`, `cNA = 4(d-1)/d` (= 2 + 2(d-2)/d); box K = 16 / 4 from matrices.
* Pieces (units 1/16π^2, μ arbitrary): each vertex pole `g^2(10c^2+1)/(4c^2)`, LSZ pole `-g^2(1 + 1/(2c^2))`, boxes
  finite; total pole `4 g^2`; `ln λ^2` coefficients: LSZ `+g^2 s^2`, box `-g^2 s^2`, total 0; Fermi vertex and Fermi LSZ
  `∓ g^2 s^2 ln λ^2`, Fermi total identically 0.
* `δ_VB(μ) = (g^2/16π^2)[6 + (7-4s^2)/(2s^2) ln c^2 - 4 ln(M_W^2/μ^2)]` (sympy, equal to the hand result).
* Ward: predicted `Σ^AZ(0)/M_Z^2 = 2 s c (g^2/16π^2) ln(M_W^2/μ^2)` equals `bos_se.sigma_AZ(0)` (1e-15 rel.); the
  left-right universality residue of the charged lepton is 0.
* μ independence: Δr_bos(M_H = 125) = 0.004297530731364 at μ = 10, 80.38, 300, 2000 GeV (all 15 digits).
* Hybrid (my Higgs diagrams) = pure bos_se assembly for M_H = 1 ... 1e4 GeV to ~1e-15; slope at large M_H =
  `11α/(48π s^2)` to 1e-10 at M_H ~ 1e8-1e13 M_W; B0 closed form vs quadrature 1e-43.
* With M_W = 80.38, M_Z = 91.19, α = 1/128: δ_vb = 0.0070927709, Δr_bos(M_H = 125) = 0.0042975307.

## Not derived / caveats
* The Fermi-theory QED subtraction assumes the standard charge-retention (Fierzed) form; with the charge-exchange form
  evaluated in NDR the (UV-divergent) Fermi correction would differ by a scheme-dependent constant. See QUESTIONS.md.
