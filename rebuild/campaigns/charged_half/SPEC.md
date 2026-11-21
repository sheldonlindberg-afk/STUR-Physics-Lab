# SPEC: emission of a charged massless spin-1/2 particle from a Schwarzschild hole whose charge fluctuates

*Postulates and conventions only. Nothing here is the answer.*

Units: G = c = ħ = k_B = 1, 4πε₀ → 1/(4π) (Heaviside–Lorentz: the potential energy of two charges q₁e, q₂e at distance r is q₁q₂ α/r, α = e²/4π the fine-structure constant), and the
mass of the hole M = 1 (lengths in GM/c², frequencies in c³/GM, power in 1/M²). The hole has the Schwarzschild horizon r_h = 2 and f(r) = 1 − 2/r; its temperature is
T = 1/(8π). The hole may carry a small electric charge Q = n e (n an integer); the Reissner–Nordström corrections to the geometry are O(α n²/M²) in Planck units and are
dropped, so the geometry is Schwarzschild, with the electrostatic potential of the charge Q at radius r the Coulomb potential: the potential energy of a particle of charge q e is
g/r with the dimensionless coupling **g = α q n** (so the horizon value is g/2).

## 1. The field and its radial equations (postulates)

A massless Dirac fermion of charge q e (a pair of chiral components; each helicity state is one "degree of freedom") is minimally coupled to the potential, which replaces ω by
ω̃(r) = ω − g/r for time dependence e^{−iωt}. For total angular momentum j = 1/2, 3/2, … the radial functions R_±(r*) (tortoise coordinate r* = r + 2 ln(r/2 − 1)) obey

    (d/dr* − i ω̃) R_− = W R_+ ,    (d/dr* + i ω̃) R_+ = W R_− ,    W = (j + 1/2) √f / r ,

which for g = 0 is the Chandrasekhar reduction of the massless Dirac equation on Schwarzschild (each of R_± then obeys d²ψ/dr*² + (ω² − V)ψ = 0 with V = W² ± dW/dr*).
The flux J = |R_−|² − |R_+|² is conserved.

## 2. Absorption probability (postulate)

The solution regular on the future horizon is R_+ = e^{−i(ω − g/2) r*}, R_− = 0 as r* → −∞ (for either sign of ω − g/2). At large r* the solution has an incident part (R_+ → A_in e^{−i φ(r*)}, φ the
phase ∫ω̃ dr*) and a reflected part (R_− → A_out e^{+iφ}); the absorption probability (grey-body factor) of the partial wave is Γ_j(ω; g) = 1 − |A_out|²/|A_in|² (the transmitted over the incident flux).

## 3. Emission and the charge process (postulates)

A mode of conserved energy ω > 0 leaves the hole with the Fermi–Dirac occupation at the Hawking temperature with the horizon potential as chemical potential,
n_F = 1/(e^{(ω − g_μ/2)/T} + 1), where g_μ/2 = q e Φ_H is the electrostatic energy of the particle at the horizon. The grey-body factor uses the coupling g_gb of the potential outside the horizon.
In a single emission the charge of the hole changes by −q (a particle of charge q e leaves), so which hole charge the emitted particle "sees" is ambiguous at order α: n before the emission, n − q after it, or the average n − q/2.
A **rule** (r_gb, r_μ) with each entry in {"before", "mid", "after"} chooses it separately for the grey-body coupling and for the chemical potential: for a particle of charge q emitted from a hole of charge n,

    g_gb = α q n_{r_gb}(q, n),   g_μ = α q n_{r_μ}(q, n),   n_before = n,  n_mid = n − q/2,  n_after = n − q.

The number rate and the power per helicity state at the pair of couplings (g_gb, g_μ) are

    N(g_gb, g_μ) = Σ_j (2j+1) ∫₀^∞ (dω/2π) Γ_j(ω; g_gb) n_F ,       P(g_gb, g_μ) = Σ_j (2j+1) ∫₀^∞ (dω/2π) ω Γ_j(ω; g_gb) n_F ,   n_F with g_μ,

and N(0, 0), P(0, 0) are the neutral values. A hole of charge n e emits only the electron and the positron (q = −1 and q = +1, the same number of helicity states each): emitting an electron raises n by one with the rate
up(n) = N(g_gb, g_μ) at q = −1, emitting a positron lowers it by one with the rate down(n) = N at q = +1. The charge relaxes much faster than the mass, so over the mass-loss time the hole is in the stationary distribution
π(n) of this birth–death process. The time-averaged power and number rate per helicity state per species are ⟨P⟩ = Σ_n π(n) [P_e⁻(n) + P_e⁺(n)]/2 and ⟨N⟩ likewise. The principal rule, the one of the literature
this campaign reproduces or tests, is ("after", "after"); the others are exported so that the dependence on the assignment can be shown.

## 4. Exports (exact signatures in campaign.py)

* `transmission(j, w, g)` → Γ_j(ω; g), ω in units 1/M, any real g.
* `rates(g_gb, g_mu)` → (N, P) of section 3, in units 1/M and 1/M².
* `charge_distribution(alpha, rule=("after", "after"))` → dict {n: π(n)}, n = −n_max … n_max with tails below 1e-14 dropped; Σπ = 1.
* `weight_ratio(alpha, rule=("after", "after"))` → ⟨P⟩ / P(0, 0): the time-averaged power per helicity state of the charge-fluctuating hole relative to the neutral massless fermion.
* `energy_ratio(alpha, rule=("after", "after"))` → (⟨P⟩/⟨N⟩) / (P(0, 0)/N(0, 0)): the mean energy per emitted quantum relative to the neutral one.

## 5. Conventions for numerics

State the radial variable and integration range, how the horizon and asymptotic boundary conditions are imposed (the large-r Coulomb phase is logarithmic), how many partial waves and what ω range and how the thermal integral is done, how the g dependence is
sampled, the chain's n range, and show convergence (changing each by a factor of 2 should move the answer by less than the tolerance you claim). Say what you checked: the g = 0 limit, flux conservation, Γ ∈ [0, 1].
