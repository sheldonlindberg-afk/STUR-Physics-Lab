# SPEC: the electric and magnetic polarizabilities of the nucleon from the pion cloud, leading order in chiral perturbation theory

*Postulates and conventions only. Nothing here is the answer.*

Units: ħ = c = 1 inside the derivation; the exports return MeV⁻³ and a helper converts to fm³ with ħc = 197.3269804 MeV·fm.

## 1. The theory (postulates)

* Two-flavour chiral perturbation theory in the heavy-baryon formulation, leading non-trivial order (O(p³) for the polarizabilities): the pion field U = exp(i τ·π/f) of the SU(2)_L × SU(2)_R sigma-model Lagrangian
  (f²/4) Tr(D_μU D^μU† + χ U† + U χ†) with χ = m_π² (the pion mass m_π, decay constant f = f_π ≈ 92 MeV normalization), and the nucleon doublet N of mass m_N → ∞ with velocity v and spin operator S,
  L_N = N̄ (i v·D + g_A S·u) N with u_μ the axial pion–nucleon vertex (g_A the axial coupling) and the vector (Weinberg–Tomozawa) coupling in D_μ. The photon enters through the covariant derivatives with the electric-charge
  matrix Q = (1 + τ³)/2 on the nucleon doublet (proton charge e, neutron 0) and the pions carrying charges +e, 0, −e (π⁺, π⁰, π⁻); e² = 4πα. Derive every vertex from the Lagrangian, including the
  two-pion–photon and nucleon–pion–photon (Kroll–Ruderman) vertices.
* The Δ(1232) and all higher resonances are excluded (their effect is a counterterm at this order); there are no counterterms at this order (the one-loop result is finite and unambiguous).
* Inputs: g_A, f_π, m_π, α (all as numbers).

## 2. The quantities (definition)

The effective Hamiltonian of a static nucleon in slowly varying external fields is H_eff = −½ · 4π α_E E² − ½ · 4π β_M B² (Heaviside–Lorentz fields E, B with α = e²/4π; equivalently the induced electric dipole is d = 4π α_E E). α_E and β_M
are the electric and magnetic polarizabilities, read off from the O(ω²) terms of the Compton amplitude at general photon energy and scattering angle (forward scattering gives only α_E + β_M) after removing the nucleon-pole (Born) contributions; in the heavy-baryon limit m_N → ∞ and a radiation gauge ε·v = 0 the Born graphs vanish. Isospin symmetry holds (proton and neutron have the same α_E and β_M at this order).
α_E, β_M have the dimension (energy)⁻³ in natural units. Regularize in dimensional regularization; state whether any divergence appears and why not.

## 3. Exports (exact signatures in campaign.py)

`alpha_E(gA, fpi, mpi, alpha)` → α_E in MeV⁻³, `beta_M(gA, fpi, mpi, alpha)` → β_M in MeV⁻³, `to_fm3(x)` → x converted to fm³ (the cube of ħc = 197.3269804 MeV fm).

## 4. Conventions for numerics

Say which diagrams contribute to the electric and to the magnetic polarizability, the Born subtraction you use, the integrals (closed form in d dimensions), why the result is finite, and the independent route you used to check it (for example a different gauge for the photon, a different
way of separating the Born terms, or a second-order-perturbation-theory sum over πN intermediate states in the static limit).
