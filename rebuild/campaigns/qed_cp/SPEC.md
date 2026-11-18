# SPEC: the Casimir–Polder interaction from fourth-order perturbation theory of the dipole–photon coupling

*Postulates and conventions only. Nothing here is the answer.*

Units: ħ = c = 1, Gaussian electrostatic units (so the polarizability α has dimension length³ and the fine-structure
constant is e² = α_fs). Energies are in units of inverse length.

## 1. Model (postulates)

Two identical neutral atoms A and B sit at fixed positions separated by a distance r. Each atom has a non-degenerate
ground state |0⟩ (energy 0) and a threefold-degenerate set of excited states |e_i⟩, i = x, y, z (energy ω₀), with
dipole matrix elements ⟨e_i| d_k |0⟩ = d δ_ik and ⟨0|d_k|0⟩ = ⟨e_i|d_k|e_j⟩ = 0. Its static polarizability is
α₀ = 2 d² / ω₀, and its dynamic polarizability α(ω) = α₀ ω₀² / (ω₀² − ω²) (check this from the model).

The free electromagnetic field is quantized in a large volume V with transverse plane-wave modes (k, λ), λ = 1, 2,
H_field = Σ k a†a. In the multipolar (dipole) formulation the atom–field interaction is

    H_int = − d_A · E⊥(x_A) − d_B · E⊥(x_B),

with the transverse electric field E⊥(x) = i Σ_{k,λ} √(2π k / V) [ ε_{kλ} a_{kλ} e^{ik·x} − ε*_{kλ} a†_{kλ} e^{−ik·x} ].
Terms independent of r (single-atom self-energies) are dropped. The longitudinal (Coulomb) interaction between the
dipoles is already contained in this formulation through the transverse displacement field; do not add it.

The unperturbed state is |0_A 0_B, no photons⟩. U(r) is the r-dependent part of its energy shift at **lowest
non-vanishing order**, which is fourth order in d (second order in α₀).

## 2. Route (required)

Use Rayleigh–Schrödinger perturbation theory over the intermediate states of the atoms and the photon modes (the route
of Casimir and Polder, 1948). Do **not** obtain U(r) from the Green-tensor/imaginary-frequency formula
−(1/2π)∫dξ α_A α_B Tr G·G or from any formula that already assumes it: the point of this campaign is an independent
derivation of that formula's content. You may reduce the photon sums to one-dimensional integrals analytically or
numerically, and you may use the standard integral over the directions of k and the sum over polarizations.

## 3. Exports (exact signatures in campaign.py)

* `cp_energy(r, w0, alpha0)` → U(r) for two identical atoms, at all separations (retardation included).
* `far_coefficient()` → C defined by U → −C α₀² / r⁷ for r ω₀ ≫ 1.
* `near_coefficient()` → D defined by U → −D ω₀ α₀² / r⁶ for r ω₀ ≪ 1.

## 3b. Intermediate exports (added after the audit: they make the required route checkable)

Two further exports expose quantities that exist only on the perturbation-theory route, so a build cannot satisfy them
with the imaginary-frequency formula:

* `denominator_sum(k, q, a, b)` where atom A has excitation energy a and atom B has b (the model of section 1 with a = b = ω₀
  is the case used for cp_energy) and k, q are the two exchanged photon energies: the sum, over the 24 orderings of the four
  vertex events (A with photon k, A with photon q, B with photon k, B with photon q), of 1/(E₁E₂E₃), divided by 2 for the
  exchange of the two photon labels (so 12 distinct time-ordered paths). Eₙ is the energy, above the ground state, of the
  intermediate state after the first n events of the ordering: each event toggles the excitation of its atom (ground ↔
  excited, energy a or b) and the occupation of its photon (absent ↔ present, energy k or q). Units: 1/energy³.
* `damped_energy(r, w0, alpha0, eps)`: the energy U of section 1 with every photon-momentum integrand multiplied by the
  damping factor e^{−eps (k+q)} (k, q the two exchanged photon energies, eps a length; the integrals then converge
  absolutely). It tends to cp_energy as eps → 0. Scaling: damped_energy(λr, w0/λ, λ³α₀, λ eps) = damped_energy(r, w0, α₀, eps)/λ.

## 4. Conventions for numerics

State the cut-offs (none should be needed: the physical energy shift is finite), how you perform the photon-momentum
integral and its principal values, and show that your U(r) is stable under refining the numerics.
