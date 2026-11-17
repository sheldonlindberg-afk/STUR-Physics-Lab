# DERIVATION — build qed_cp-a (Casimir–Polder by fourth-order perturbation theory)

Units ħ = c = 1, Gaussian (SPEC §0). Notation: ω₀ ≡ a, atom A at 0, atom B at **r** = r r̂.

## 0. Polarizability of the model (SPEC §1, "check this from the model")

α_ij(ω) = Σ_e [⟨0|d_i|e⟩⟨e|d_j|0⟩/(ω₀−ω) + ⟨0|d_j|e⟩⟨e|d_i|0⟩/(ω₀+ω)] = d²δ_ij · 2ω₀/(ω₀²−ω²).
So α(ω) = α₀ω₀²/(ω₀²−ω²) with α₀ = 2d²/ω₀, i.e. d⁴ = α₀²ω₀²/4. On the imaginary axis
α(iu) = α₀ω₀²/(ω₀²+u²) = 2d²ω₀/(ω₀²+u²).

## 1. Which fourth-order terms depend on r (SPEC §1)

RS perturbation theory, E₀ = 0 for |0_A 0_B; vac⟩:

E⁽⁴⁾ = Σ_{I,J,K≠0} V_{0K}V_{KJ}V_{JI}V_{I0} / [(−E_K)(−E_J)(−E_I)] − E⁽²⁾ Σ_I |V_{I0}|²/E_I²   (E⁽¹⁾ = E⁽³⁾ = 0).

H_int is linear in a single atom's dipole and in a single photon operator. Each atom must return to |0⟩, so each
atom carries an even number of vertices; each photon is created once and destroyed once. At fourth order the
options are: (i) all four vertices on one atom — r-independent; (ii) two on each atom with each photon starting and
ending on the same atom — a product of two single-atom self-energy processes, r-independent (and these are exactly
the terms cancelled by the −E⁽²⁾Σ… renormalisation term, which is itself r-independent because second order has no
r-dependent part: an A→B single photon exchange leaves both atoms excited, ≠ initial state); (iii) two vertices on
each atom, both photons exchanged between A and B. Only (iii) depends on r. No intermediate state of (iii) is the
initial state (after two vertices at least one photon or one excitation is present), so no exclusion problem.

**Counting.** Call p the photon attached to A's earlier vertex and q the one attached to A's later vertex. This labels
every path uniquely, and p, q are then summed independently over all modes. The four vertices
{A_p, A_q, B_p, B_q} with A_p before A_q have 4!/2 = 12 time orderings — the 12 Casimir–Polder diagrams.

## 2. Numerators

Vertex −d·E⊥(x): creation part +i√(2πk/V)(d·ε*)a† e^{−ik·x}, annihilation part −i√(2πk/V)(d·ε)a e^{ik·x}.
For a photon exchanged between A and B the product of its creation and annihilation factors is
(+i)(−i)(2πk/V) d^A_i d^B_j ε*_i ε_j e^{±ik·r}, irrespective of which atom emits it. Sum over λ:
Σ_λ ε_iε*_j = δ_ij − k̂_ik̂_j. Mode sum Σ_k → V(2π)⁻³∫d³k. Direction average (standard, SPEC §2):

τ_ij(kr) ≡ (1/4π)∫dΩ_k (δ_ij − k̂_ik̂_j) e^{ik·r} = P(kr) δ_ij + Q(kr) r̂_ir̂_j,
P(x) = sin x/x + cos x/x² − sin x/x³,  Q(x) = −sin x/x − 3cos x/x² + 3 sin x/x³  (real, even in r).

So each exchanged photon contributes (2πk)(4πk²)/(2π)³ dk τ = (k³/π) τ_ij dk.
Atom factors: Σ_e ⟨0|d_j|e⟩⟨e|d_i|0⟩ = d²δ_ij for each atom (indices i at the p-vertex, j at the q-vertex). The
product of four −1 signs from −d·E is +1. Contracting, every one of the 12 diagrams has numerator

d⁴ (k³/π)(q³/π) Tr[τ(kr)τ(qr)] dk dq,

and differs only in its energy denominators. With the minus sign of (−E_I)(−E_J)(−E_K):

U(r) = −(d⁴/π²) ∫₀^∞dk ∫₀^∞dq k³q³ Tr[τ(kr)τ(qr)] Σ₁₂(k,q).     (1)

## 3. The 12 energy denominators

Intermediate energy = (sum of excitation energies of excited atoms) + (energies of photons present). Written out
for general a = ω_A, b = ω_B (done by enumeration in sympy; the code in `__main__` recomputes it), the sum is

Σ₁₂(k,q) = 4 N / [(a+b)(a+k)(a+q)(b+k)(b+q)(k+q)],
N = a²b+ab² + (a+b)²(k+q) + (a+b)(k²+q²) + 2(a+b)kq + kq(k+q),
already symmetric in k↔q. For a = b: Σ₁₂ = 2[2a³+4a²(k+q)+2a(k+q)²+kq(k+q)] / [a(a+k)²(a+q)²(k+q)].

**Key identity (posited, then proved by residues).** I found the form of (2) by trying an ansatz c₁·kq + c₂·u² in the numerator and fitting c₁, c₂ numerically during exploration (c₁ = 8/π, c₂ = 0); it was then proved:

Σ₁₂(k,q) = (8/π) ∫₀^∞ du  ab·kq / [(a²+u²)(b²+u²)(k²+u²)(q²+u²)].     (2)

Proof: the integrand is even in u, so ∫₀^∞ = ½∫_{−∞}^{∞}; close in the upper half plane, simple poles at
u = ia, ib, ik, iq; the sum of residues (2πi·½·Σ Res) is a rational function that reduces to Σ₁₂ (checked
symbolically with sympy residues in `__main__`, residual 0, and numerically by quad at 5 random (a,b,k,q) in
`__main__`). This identity is the step that turns real-photon-energy denominators into an imaginary-frequency
representation; it is not assumed, but it was guessed before it was proved.

## 4. Doing the photon integrals

Insert (2) in (1) and exchange orders (the k and q integrals then factorise):

U = −(8d⁴a²/π³) ∫₀^∞ du (a²+u²)⁻² Tr[M(u)²],  M_ij(u) = ∫₀^∞dk k⁴ τ_ij(kr)/(k²+u²).

Since (δ_ij−k̂_ik̂_j)e^{ik·r} = k⁻²(−∇²δ_ij+∂_i∂_j)e^{ik·r},
M_ij = (−∇²δ_ij+∂_i∂_j) (1/r)∫₀^∞dk k sin(kr)/(k²+u²) = (π/2)(−∇²δ_ij+∂_i∂_j) e^{−ur}/r   (r > 0).
The k-integral is meant as an Abel limit (factor e^{−εk}, ε→0⁺), which is also how the original double integral (1)
converges (its integrand grows ∝ k sin kr at large k); this is the only regularisation, no cut-off appears, and
the result is finite. The ∂_i∂_j(1/r) piece contained here is the transverse-delta (Coulomb-like) part of the
multipolar coupling (SPEC §1: not added separately).

With f = e^{−ur}/r, ∇²f = u²f, ∂_i∂_jf = r̂r̂ f'' + (δ−r̂r̂) f'/r:
M = (π/2)(e^{−ur}/r)[A δ + B r̂r̂], r²A = −(x²+x+1), r²B = x²+3x+3, x = ur.
Tr M² = (π²/4)(e^{−2x}/r²)(3A²+2AB+B²) = (π²/2) e^{−2x} p(x)/r⁶, p(x) = x⁴+2x³+5x²+6x+3.

Using 4d⁴a²/(a²+u²)² = α(iu)² (for a = b; for a ≠ b, α_A(iu)α_B(iu)):

**U(r) = −(1/π r⁶) ∫₀^∞ du α(iu)² e^{−2ur} p(ur).**     (3)

Dimensionless form used in the code, ρ = ω₀r, u = ω₀t:
U = −(α₀²ω₀/π r⁶) J(ρ),  J(ρ) = ∫₀^∞ dt e^{−2ρt} p(ρt)/(1+t²)²
  = (1/ρ)∫₀^∞ ds e^{−2s} p(s)/(1+s²/ρ²)²   (s = ρt; used for ρ ≥ 1).

Properties: U ∝ α₀² exactly; U(λr, ω₀/λ, λ³α₀) = U/λ exactly (ρ invariant); U < 0 (integrand positive);
d/dx[e^{−2x}p(x)] = −2x(x³+2x+1)e^{−2x} < 0, so J(ρ) = |U|r⁶π/(α₀²ω₀) strictly decreases with ρ.

## 5. Limits

Near (ρ→0): J → ∫₀^∞ 3 dt/(1+t²)² = 3π/4, so D = 3/4·(computed as (1/π)∫3/(1+t²)² in code, via sympy).
Far (ρ→∞): J → (1/ρ)∫₀^∞e^{−2s}p(s)ds = (1/ρ)Σ c_n n!/2^{n+1} = (1/ρ)(24/32+12/16+10/8+6/4+3/2) = 23/(4ρ),
so U → −(23/4π)α₀²/r⁷, C = 23/(4π) (computed in code from the coefficients of p, never typed).

## 6. Independent second routes (run in `__main__`)

(a) **London / electrostatic route for the near limit.** Second-order perturbation theory with the static
dipole–dipole operator V = [d_A·d_B − 3(d_A·r̂)(d_B·r̂)]/r³: U = −Σ_ij d⁴(δ_ij−3r̂_ir̂_j)²/(2ω₀r⁶) = −6d⁴/(2ω₀r⁶)
= −(3/4)ω₀α₀²/r⁶. Must agree with D from (3). Different physics input (no photons at all).
(b) **Direct numerical evaluation of the double photon integral (1)**, with Abel factor e^{−ε(k+q)}, evaluated on a
Gauss–Legendre grid for several ε and extrapolated polynomially to ε→0. This does not use identity (2) or the
contour step of §4. Compared with (3) at r ω₀ = 2 (slow but independent): direct −8.2793e−3 vs eq.(3) −8.2767e−3, 3e−4 relative, limited by the ε-extrapolation.
(c) Identity (2) checked symbolically by residues and numerically at random (a,b,k,q).
(d) Numerical stability of (3): the two variables (t vs s) agree to ~1e-14 at ρ = 1, and J(ρ) agrees with a
30-digit mpmath quadrature to 2e-16 relative (measured) for ρ from 1e-12 to 1e5 (both in `__main__`).

**Validity range of `cp_energy`.** Checked for 1e-12 ≤ rω₀ ≤ 1e5. An earlier version split the t-integral only at
t = 1, 10, 1/ρ, 20/ρ; for ρ ≤ 1e-7 `quad` under-sampled the single panel [10, 1/ρ] (the 3/t⁴ tail, ~1e-3 of J)
and U was low by 4.2e-4 relative. Decade breakpoints 10, 100, …, 1/ρ fix this; results for ρ ≥ 1e-6 are
changed by at most 2e-13 relative (at ρ = 1e-6, an improvement). Below ρ = 1e-12 it is untested, and floating-point r⁶ under/overflow eventually limits it.

## 7. Not derived / caveats

The direction average τ_ij and the polarisation sum are the standard results permitted by SPEC §2 (τ re-checked
numerically in `__main__`). The interchange of the u-integral with the conditionally convergent k, q integrals is
justified via the Abel regulator, not proved rigorously; route 6(b) checks it numerically.
