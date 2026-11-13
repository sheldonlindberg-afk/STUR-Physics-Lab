# Rebuild specification: postulates and conventions, without answers

*For the builder. This page states what to **assume** at each stage and the conventions that
make independent builds comparable. It deliberately gives no results: no eigenvalues, no phases, no exact integrals, no
masses. You derive them. The export signatures are in
[`contract.py`](contract.py), and the only source of numbers is [`inputs.py`](inputs.py).*

## 0. Layers

Every quantity you produce is exactly one of the following:
- **derived**: computed in your build from the postulates below.
- **input**: read from `inputs.py`.
- **quoted**: a published formula used without derivation. This is allowed only where the
  stage lists it, and you must name the source in `PROVENANCE`.

If you can't derive something and it isn't on the stage's quoted list, **stop and report it**.
Don't type the number in. The harness lint fails any literal with more than three
significant digits.

## Connections between stages

The rungs are one computation, not separate ones. Where `contract.CONNECTIONS` says a
downstream function uses an upstream one, it must **call** it, as
`import <stage>` … `<stage>.<function>(...)`, at call time. Never use
`from <stage> import`, and never use a private re-derivation. The harness spies on these
calls. The ones that carry physics:

- **Rung 2 → 4.** Gravity's static potential is the massless limit of rung 2's exchange
  transform: U(r) = −4πG m₁m₂ · `chiral.yukawa(r, 0)`.
- **Rung 3 → 4.** Design A's phase is evaluated at the gap that `casimir.casimir_safe_gap`
  returns for the baseline in `inputs.GAP_BASELINE_*`.
- **Rung 5 → 6.** The largest black hole comes from rung 5's de Sitter radius
  (`desitter.ell_from_lambda`). The surface gravity can also be read from rung 5's spin
  connection: κ = |ω⁰₁ₜ| at the horizon.
- **Rung 1 → links.** The proton, neutron, electron and neutrino charges, and the π⁰ width,
  use `gauge331.quark_charges` and `gauge331.triplet_charges`.
- **Rung 6 → link 3.** The temperature of a Planck-mass black hole uses
  `blackholes.hawking_K` at `links.planck_mass_GeV`'s mass.
- **The toolkit.** Every eigenvalue, Hessian, root, maximum and time integral listed there
  goes through `toolkit`.

## 1. toolkit

Standard library only. Implement and self-test: a Jacobi eigenvalue solver, a central-difference
Hessian, forward-mode dual numbers over `fractions.Fraction` (for `exact_derivative`),
bisection, golden-section search, the trapezoid rule and permutation parity. Every later
stage must use these, not ad hoc copies.

**Conventions.** The Hessian's step h is absolute and the same in every coordinate. A caller
whose coordinates are far from O(1) scales h itself.

## 2. gauge331: 3-3-1 → SM → electromagnetism

**Postulates.**
- Gauge group SU(3)_L × U(1)_X with couplings g and g_X. Generators t_a = λ_a/2 (standard
  Gell-Mann matrices, λ_8 = diag(1,1,−2)/√3), and X·𝟙 for U(1)_X.
- Charge Q = T₃ + βT₈ + X, β = −1/√3 (`"-1/sqrt3"`) or +1/√3 (`"+1/sqrt3"`). An
  antitriplet carries generators −t_a*. The X passed to `triplet_charges(X, variant, anti=True)`
  is the antitriplet's own U(1)_X charge (it is not conjugated; only the SU(3) part flips).
- **Scalars:** three triplets with X charges (−1/3, 2/3, −1/3) for β = −1/√3, and
  (1/3, 1/3, −2/3) for β = +1/√3. A vev may sit only in a component with Q = 0. The first
  triplet that is neutral in component 3 takes w; each other triplet takes its remaining
  neutral component, with v₁ then v₂ in order. Derive which components are neutral; don't
  assume it. "Remaining" means *other than component 3*: a triplet that is not the w triplet,
  but is neutral both in component 3 and in another component, takes the other one.
- **Fermions** for N_c colours: N_g = N_c generations. Of the quark families, n_A = (1+N_c)/2
  are antitriplets and N_g − n_A are triplets. Lepton triplets have X_L = −1/3 (β = −1/√3) or
  −2/3 (β = +1/√3). The quark-triplet X is fixed so that its first two components are
  (Q_u, Q_d), and the antitriplet X so that its first two are also (Q_u, Q_d) in some order.
- **Q_u and Q_d are not inputs.** Derive them from: Q_u − Q_d = 1 (they form an SU(2)
  doublet), the electron charge −1, and the cancellation of the [SU(3)_L]²U(1)_X anomaly.
  Equivalently, the N_c-quark proton ((N_c+1)/2 u, (N_c−1)/2 d) satisfies q_p + q_e = 0.

**Conventions.** The mass-matrix basis is (W¹…W⁸, B_X), and ⟨φ⟩_k = vev/√2. For
`mz_tree`, use the tree-level relation M_Z² = πα/(√2 G_F s²(1−s²)).

**What you must be able to explain** (the verifier will ask): why the photon direction is
massless for any vevs that respect Q; what stays massless when v₁ = v₂ = 0; how ρ − 1 scales
with v/w.

## 3. chiral: the strong force

**Postulates.**
- The linear sigma model, V = (λ/4)(φ·φ − v²)² − Hσ, with φ = (σ, π₁, π₂, π₃).
- GMOR: identify f_π = ⟨σ⟩ and H f_π = (m_u + m_d)|⟨q̄q⟩|.
- **Quoted (allowed):** the O(p⁴) chiral perturbation theory result
  M_π² = M²[1 − M² ℓ̄₃/(32π²F²)], with M² = 2m̂Σ/F², F = f_π/(F_π/F) and Σ = cond13³.
- Exchanging a boson of mass m gives a momentum-space potential ∝ 1/(q² + m²). Normalize it
  so that the Fourier transform has unit strength, i.e. (∇² − m²)V = −δ³.
- Pauli matrices for spin; S₁₂ = 3(σ₁·q̂)(σ₂·q̂) − σ₁·σ₂.
- Goldberger–Treiman: g_πNN = g_A M_N / f_π (state this as derived from PCAC, or tag it quoted).

## 4. casimir: the electromagnetic background

**Postulates.**
- Electrostatics of a dielectric sphere of permittivity ε in a uniform field (Laplace's
  equation, with continuity of Φ and of ε∂_rΦ).
- The dipole Green tensor at imaginary frequency, with u = kr:
  G_ij = e^(−u)/r³ [(1+u+u²)δ_ij − (3+3u+u²) x_i x_j / r²].
- **Quoted (allowed):** the Casimir–Polder fluctuation formula
  U = −(ħ/2π)∫₀^∞ dξ α₁α₂ Tr[G·G], with α in units of 4πε₀ and constant α (the static limit).
- **Safe gap.** Two diamonds of mass m are each in a superposition of two positions ±dx/2 along
  a line perpendicular to their separation (parallel geometry), for a time τ. The gap is
  the distance between the near branches. Branch distances: d_LL = d_RR = gap and
  d_LR = d_RL = √(gap² + dx²). The entangling phase of a potential U is
  (τ/ħ)[−U(d_LL) − U(d_RR) + U(d_LR) + U(d_RL)]. The safe gap is the smallest gap at which
  |Casimir phase| ≤ fraction × |gravity phase|. Find it as a root to relative precision
  1e−6 or better, not on a coarse grid.

## 5. graviton: gravity to the experiment

**Postulates.**
- Linearized GR: g = η + h, η = diag(−1,1,1,1), h̄ = h − ½ηh, □h̄_μν = −16πG T_μν.
- One-graviton exchange: the amplitude is ∝ T₂^μν P_μνρσ T₁^ρσ, with
  P = ½(η_μρη_νσ + η_μση_νρ − η_μνη_ρσ). Matter couples through ½h_μνT^μν; together with the
  field equation above, this fixes the normalization of the exchange.
- **Branch profile.** y(t) = (dx/2)·s(t), with s = up(t/ramp) for t < ramp, 1 during the
  hold, and up((T − t)/ramp) after ramp + hold, where T = hold + 2·ramp and
  up(x) = 2x² for x < ½, else 1 − 2(1−x)², where x is clamped to [0, 1] before up is applied.
- **Phase.** Parallel geometry as in §4, but with time-dependent separation 2y(t):
  Δφ = (Gm²/ħ)∫₀^T 2[1/gap − 1/√(gap² + (2y)²)] dt, by the trapezoid rule on n samples.
  Derive the 1/r potential from the exchange postulate (via `chiral.yukawa` at m = 0);
  don't assume Newton.
- **`design_phase`:** the phase for `inputs.DESIGN_A_*` at
  `casimir.casimir_safe_gap(GAP_BASELINE_MASS, GAP_BASELINE_DX, GAP_BASELINE_TAU, GAP_FRACTION)`.

## 6. desitter: gravity as a broken SO(4,1) gauge theory

**Postulates.**
- so(4,1) generators as in `contract.py`. The connection is
  A_μ = ½ω^{ab}_μ J_ab + (1/ℓ) e^a_μ J_a4, and F = dA + [A_μ, A_ν].
- The static metric −f dt² + dr²/f + r²dΩ², with diagonal tetrad
  (√f, 1/√f, r, r sinθ). Derive the Levi-Civita spin connection, and prove it by checking
  the torsion de + ω∧e = 0 numerically.
- Schwarzschild–de Sitter: f = 1 − 2M/r − r²/ℓ². De Sitter: f = 1 − r²/ℓ².
- The MacDowell–Mansouri action N∫ε_abcd F^{ab}∧F^{cd}.

**Conventions.** The Lorentz symbol with lowered indices has ε₀₁₂₃ = +1 (the plain permutation
symbol, `toolkit.levi_civita`). The coordinate density has ε̃^{0123} = +1, i.e. a 4-form's
component is read on dt∧dr∧dθ∧dφ. `action_coefficients` uses both.
- **`ricci_scalar`** contracts the curvature 2-form R^{ab} = dω^{ab} + ω^a_c∧ω^{cb} that your
  `action_coefficients` uses, as E_a^μ E_b^ν R^{ab}_{μν} (indices raised with η). It is
  exported so the curvature itself can be checked: the coefficient cR alone can't detect a
  wrong R^{ab}.
- **`spin_connection`** returns the tetrad and ω^a_{bμ}, with a raised and b lowered by η
  (so ω^0_1 = ω^1_0 for the boost). It is exported because rung 6 uses it.

## 7. blackholes

**Postulates.**
- The static metrics above, the Killing vector ξ = ∂_t, and κ² = −½(∇_μξ_ν)(∇^μξ^ν).
  Compute the Christoffel symbols from the metric (f only, never f′).
- Euclidean time t = −iτ. Proper radial distance ρ = ∫dr/√f.
- Kerr in its horizon radii p = r₊ and q = r₋, with G = c = 1: M = (p+q)/2, a² = pq.
  **Quoted:** S = π(p² + a²), T = (p − q)/(4π(p² + a²)), Ω = a/(p² + a²), J = Ma
  (Bardeen–Carter–Hawking).
- Geodesics: photons have the effective potential f/r²; massive particles have
  V = f(1 + L²/r²). Find the photon sphere and the ISCO numerically, not from closed forms.
- **Quoted (allowed):** the Berti–Cardoso–Will fit, Mω = f₁ + f₂(1−χ)^f₃ and
  Q = q₁ + q₂(1−χ)^q₃ with damping rate ω/(2Q); and T_H = ħc³/(8πGMk_B) as a radiation
  temperature.
- Kerr area A = 8π(GM/c²)²(1 + √(1−χ²)). The shadow diameter is 2b_c GM/(c²D).

**Conventions.**
- The QNM damping rate ω/(2Q) is in s⁻¹ (the contract's "Hz" for it means s⁻¹); the frequency
  is ω/(2π) in Hz.
- In `kerr_first_law`, at q = 0 (Schwarzschild) along dq, dJ itself diverges; the residual
  uses the finite limit of Ω dJ there.
- In the self-check, a pull is (prediction − measured)/σ_measured, with σ taken on the side
  facing the prediction. For Sgr A*, the measured θ_g is the mean of the two θ_g = GM/(c²D)
  values (VLTI and Keck), not mean mass over mean distance.
- **`kappa_from_spin_connection`:** evaluate rung 5's ω⁰₁ₜ just on the static side of each
  SdS horizon (r_b(1 + 10⁻⁹), r_c(1 − 10⁻⁹)); κ = |ω⁰₁ₜ|. This is a second route to the
  Killing κ.

## 8. links

**Postulates.**
- **Anomaly identity.** For any rational b = β/(2√3), X_L, X_t and N_c:
  - lepton triplet: Q_ν = ½ + b + X_L, Q_e = −½ + b + X_L;
  - quark triplet: Q_u = ½ + b + X_t, Q_d = −½ + b + X_t;
  - antitriplet: X_a = X_t + 2b;
  - N_g = N_c, with n = (1+N_c)/2 antitriplet families;
  - anomaly = N_g X_L + N_c[(N_g − n)X_t + n X_a].
- **Neutrality.** Coulomb and gravity both go as 1/r on the same trajectories, so their
  phases are in the ratio kQ²/(Gm²). Divide by the nucleon count m/u.
- **Quoted (allowed):** the anomaly amplitude A = (α/πf_π)N_c(Q_u² − Q_d²) for π⁰ → γγ.
  Derive the polarization sum and the two-body phase space yourself.
- M_Pl = √(ħc/G). If G → xG, M_Pl → x^(−1/2)M_Pl.
- **`matter_charges`:** the N_c-quark proton is ((N_c+1)/2 u, (N_c−1)/2 d) and the neutron
  is the reverse. The electron and neutrino are the lepton triplet's components 2 and 1,
  with X_L as in §2.
- **`planck_bh_kT_GeV`:** m = M_Pl in kg, then k_B T_H in GeV.
