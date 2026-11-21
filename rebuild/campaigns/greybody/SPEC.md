# SPEC: grey-body factors and the Hawking emission power of a Schwarzschild black hole

*Postulates and conventions only. Nothing here is the answer.*

Units: G = c = ħ = k_B = 1 and M = 1 (so lengths are in units of GM/c², frequencies in c³/GM). The black
hole is non-rotating and uncharged, with horizon r_h = 2 and f(r) = 1 − 2/r.

## 1. Fields and master equations (postulates)

A massless free field of spin s ∈ {0, 1/2, 1, 2} propagating on the Schwarzschild background separates into
partial waves labelled by the total angular momentum j (j = 0, 1, 2, … for s = 0, 1, 2 with j ≥ s; j = 1/2, 3/2, …
for s = 1/2) and a radial function ψ(r*) obeying, with the tortoise coordinate r* = r + 2 ln(r/2 − 1) and
time dependence e^{−iωt},

    d²ψ/dr*² + (ω² − V(r)) ψ = 0 .

* Bosons (s = 0, 1, 2; the Regge–Wheeler form): V = f [ j(j+1)/r² + (1 − s²)(2/r³) ].
* Fermions (s = 1/2; the Chandrasekhar reduction of the massless Dirac equation): V = W² ± dW/dr*, with
  W = (j + 1/2) √f / r. The two signs (two chiral components) give the same transmission.

## 2. Absorption probability (postulate)

With the boundary condition of purely ingoing radiation at the horizon, ψ → e^{−iωr*} as r* → −∞, the solution at
large r* is ψ → A_in e^{−iωr*} + A_out e^{+iωr*}. The absorption probability (grey-body factor) of the partial wave
is the transmitted over the incident flux, Γ_{s,j}(ω).

## 3. Emission (postulates)

The Hawking temperature is T = 1/(8π). The black hole emits each partial wave (j, m) of each helicity state
("degree of freedom") with the grey-body factor and a Bose–Einstein (s = 0, 1, 2) or Fermi–Dirac (s = 1/2) occupation
1/(e^{ω/T} ∓ 1). The energy emitted per unit time per degree of freedom is

    P_s = Σ_j (2j + 1) ∫₀^∞ (dω / 2π) ω Γ_{s,j}(ω) / (e^{ω/T} ∓ 1) ,

and by dimensional analysis P_s is a pure number times 1/M² (so dM/dt = −P_s/M² per degree of freedom, M restored).

## 4. Exports (exact signatures in campaign.py)

* `transmission(s, j, w)` → Γ_{s,j}(ω), for ω in units of 1/M.
* `absorption_sum(s, w)` → Σ_j (2j + 1) Γ_{s,j}(ω), summed over all j ≥ s that matter at that ω.
* `power_per_dof(s)` → P_s, in units 1/M².

## 5. Conventions for numerics

Be explicit about the integration range in r*, how you impose the boundary conditions, how you obtain A_in at
finite r*, how many partial waves and how large an ω-range you include, and show convergence (changing each
by a factor of 2 should move the answer by less than the tolerance you claim). Note the Bose factor makes the
integrand finite at ω → 0 because Γ vanishes like a power of ω.
