# Building the symmetry ladder from first principles

*How to write [`src/ladder_standalone.py`](src/ladder_standalone.py) from an empty file:
what to postulate, what to measure, what to derive, in what order, and how each step proves
itself before the next one uses it. Companion to [SYMMETRY_LADDER.md](SYMMETRY_LADDER.md),
which states the results; this page is the recipe. Independent work, not peer reviewed.*

---

## 0. What "first principles" can mean here

Nothing in physics comes from nothing. Every line of the script falls into one of four
layers. Building from first principles means keeping each layer as thin as possible and
never letting a lower layer smuggle in a number that a higher one could compute.

| Layer | What it is | Examples in the script | Can it be removed? |
|---|---|---|---|
| **Postulates** | Symmetry groups, field content, the form of the Lagrangian or action | SU(3)_C×SU(3)_L×U(1)_X with Q = T₃ + βT₈ + X; the O(4) sigma model; the Einstein–Hilbert action; quantum mechanics | No: this is the theory |
| **Measured inputs** | Numbers nature chose | G_F, α(M_Z), sin²θ_W, quark masses, f_π, ε(diamond), G, ħ, c, Λ, EHT rings, GW250114 fits | No: nobody derives these (stated in the script's last line) |
| **Quoted results** | Correct derivations that are not repeated in the file | the Casimir–Polder fluctuation formula; Hawking's T = κ/2π *as radiation*; the ABJ anomaly coefficient; lattice low-energy constants; the Berti–Cardoso–Will QNM fit; the 3-3-1 Landau poles | Yes, each one, with more work (§9) |
| **Derived** | Everything else: computed in the file and checked | the photon, the W/Z/Z′ masses, the pion count, GMOR, Yukawa, 23/4, Newton, 2.19 rad, F = R − e∧e/ℓ², κ, the first law, ISCO… | This is the point |

The script's check tags record which layer a result rests on: **[math]** = derived only,
**[data]** = derived and compared with a measured input, **[pinned]** = a number this
repository derives elsewhere, frozen so that changes get caught.

**The single rule that makes it first-principles:** *never type a result you could compute.*
Type the postulate (a generator matrix, a metric function f(r), a potential) and let the
code produce the consequence. Then check the consequence against an independent route: a
closed form, a second method, or a measurement.

---

## 1. Build order

The rungs are not independent. The dependency graph decides the order:

```
toolkit (§2)
  ├─ rung 1  gauge mass matrix ──────────────┐ charges Q_u, Q_d
  │                                          ├──► link 1 neutral matter ──► rung 4
  │                                          └──► link 2 π⁰→γγ ◄── rung 2 (f_π)
  ├─ rung 2  sigma model, Yukawa transform ──► rung 4 (Yukawa at m = 0 is Newton)
  ├─ rung 3  dielectric sphere, Green tensor ─► Casimir-safe gap ──► rung 4
  ├─ rung 4  linearized GR, graviton exchange, phase
  ├─ rung 5  tetrad, spin connection, so(4,1) ─► rung 6 (κ cross-check, Λ)
  └─ rung 6  horizons, κ, Euclidean period, Kerr thermodynamics, orbits, data
links: 1 (rung 1→4), 2 (1,2), 3 (4→1, M_Pl), 4–5 (6→4, 6→3)
```

So: toolkit → 1 → 2 → 3 → 4 → 5 → 6 → links. Each stage must pass its own checks before
anything downstream reads its output.

---

## 2. The toolkit: write and validate it first

Standard library only. Every tool gets a test on a case with a known answer *before* any
physics uses it.

| Tool | Why it is needed | Validate on |
|---|---|---|
| `fractions.Fraction` arithmetic | Charges, anomalies, 23/4, Kerr thermodynamics must hold *exactly*, not to 1e-12 | ⅓ + ⅙ = ½ |
| Matrix multiply, add, scale, commutator (lists of lists) | Generators, mass matrices, curvature | Pauli matrices: [σ₁, σ₂] = 2iσ₃ |
| **Jacobi eigenvalues** of a real symmetric matrix | Counting massless gauge bosons and Goldstones (zero eigenvalues) | diag(1,2,3) rotated by a random orthogonal matrix |
| **Finite-difference Hessian / Laplacian**, plus Richardson extrapolation | Masses from a potential; checking that a field solves its equation | V = x² + 3xy: Hessian [[2,3],[3,0]] |
| **Dual numbers** a + bε, ε² = 0, over Fractions | *Exact* derivatives of rational functions (the first law dM = T dS) | d/dx (x³) at x = 2 is 12 exactly |
| Newton, bisection, golden-section search | Vacua, horizons (f = 0), potential maxima (photon sphere) | √2 by bisection |
| Trapezoid and midpoint quadrature | The entangling phase and the proper distance ρ = ∫dr/√f | ∫₀^π sin = 2 |
| Levi-Civita symbol, permutation parity | Wedge products ε_abcd X^ab∧Y^cd and ε^μνρσ for π⁰→γγ | ε₀₁₂₃ = 1, any swap flips sign |

Tolerances follow from the method: exact tools give `==`; central differences have O(h²)
error, so with h = 1e-4 expect about 1e-8, and Richardson extrapolation gives O(h⁴).

---

## 3. Rung 1: 3-3-1 → Standard Model → electromagnetism

**Postulate.** Gauge group SU(3)_L × U(1)_X with couplings g and g_X, generators
t_a = λ_a/2 (the eight Gell-Mann matrices) plus X·𝟙. Charge Q = T₃ + βT₈ + X, β = ±1/√3.
Scalars: three triplets with X charges chosen so that each has a neutral component.

**Derive, in this order:**

1. **Where each vacuum value can sit.** Q on a triplet is diag(T₃ + βT₈) + X. With
   T₈ = diag(1,1,−2)/(2√3), βT₈ = ∓diag(1,1,−2)/6. A vev may only sit in a component with
   Q = 0, otherwise it breaks electromagnetism. Compute this with Fractions; don't choose it by hand.
2. **The mass matrix.** From the kinetic term |D_μφ|² with D = ∂ − i Σ g_A t_A W^A:
   M²_AB = g_A g_B Σ_φ ⟨φ⟩†{t_A, t_B}⟨φ⟩, a 9×9 real symmetric matrix.
3. **Why exactly one zero eigenvalue (the photon).** Define n_A = q_A/g_A, where
   Q = Σ q_A t_A, so n = (0,0,1/g,0,0,0,0,β/g,1/g_X). Then
   (M²n)_A = g_A Σ ⟨φ⟩†{t_A, Q}⟨φ⟩ = 0, because Q⟨φ⟩ = 0 for every vev (step 1). So n is
   the massless direction, and the photon couples with **1/e² = |n|² = (1+β²)/g² + 1/g_X²**.
   *Check:* Jacobi finds exactly one zero; M²n = 0 numerically.
4. **Two-step breaking.** Set v₁ = v₂ = 0 and keep w: four zero eigenvalues (SU(2)_L plus
   one U(1)). That U(1) is Y = βT₈ + X, the same argument applied to χ alone, and
   1/g_Y² = β²/g² + 1/g_X²: the matching condition, derived rather than assumed.
5. **Masses.** Read off M_W² = g²v²/4 and bileptons g²(w² + v_i²)/4 from the diagonal.
   Diagonalize the 3×3 neutral block (T₃, T₈, X) and expand in v²/w²:
   M_Z² → (g² + g_Y²)v²/4, M_Z′² → (g² + β²g_X²)w²/3. The ρ parameter is ≥ 1, and ρ − 1
   scales as (v/w)². *Check:* doubling w divides ρ − 1 by 4.
6. **Fermion charges for any N_c.** Anomaly cancellation sets the content.
   [SU(3)_L]³ needs equal numbers of triplets and antitriplets: N_g = N_c generations, with
   (1+N_c)/2 quark families in antitriplets. The remaining conditions fix
   Q_u = (N_c+1)/2N_c and Q_d = (1−N_c)/2N_c. Antitriplets carry −T*. Compute every
   component's Q with Fractions, for N_c = 3, 5, 7.
7. **Contact with data.** v = (√2 G_F)^(−1/2) = 246.22 GeV. At tree level
   M_Z = √(πα/(√2 G_F s²c²)) = 91.51 GeV, against 91.19 measured. The +0.35% is the
   loop correction (order α/π), which you don't derive here, so the tolerance is 0.5%.

---

## 4. Rung 2: the strong force

**Postulate.** The linear sigma model: four real fields φ = (σ, π⃗) with
V = (λ/4)(φ² − v²)² − Hσ. This is a *model* with QCD's chiral breaking pattern
O(4) ≅ SU(2)_L×SU(2)_R → O(3) ≅ SU(2)_V; tag its checks [model].

1. **Goldstone count.** H = 0: the finite-difference Hessian at (v,0,0,0) has
   eigenvalues {0,0,0, 2λv²}. Three pions = dim O(4) − dim O(3) = 6 − 3.
2. **GMOR.** H ≠ 0: Newton-solve λσ₀(σ₀² − v²) = H, then the Hessian gives m_π² = H/σ₀.
   With f_π = σ₀ and H f_π = (m_u+m_d)|⟨q̄q⟩|, this is **m_π²f_π² = (m_u+m_d)|⟨q̄q⟩|**.
   With measured inputs, 127.6 MeV against 135.0. This is leading order, so the tolerance is 8%.
3. **Beyond the model: ChPT at O(p⁴).** M² = 2m̂Σ/F², and
   M_π² = M²[1 − M² ℓ̄₃/(32π²F²)]. The one-loop tadpole is derived in
   `src/chiral_breaking.py` S6; ℓ̄₃, F_π/F and Σ are lattice inputs. Propagate their errors
   by finite differences (one input at a time, in quadrature): 132.6 ± 3.8 MeV.
4. **Why exchange gives e^(−mr)/(4πr).** Exchanging a mass-m boson gives V(q) ∝ 1/(q²+m²),
   whose Fourier transform is the Yukawa potential. Verify that it solves
   (∇² − m²)V = −δ³: check the Laplacian at three radii and the unit flux through a
   small sphere. Range: ħc/m_π = 1.414 fm. *Keep this function: at m = 0 it is Newton
   (rung 4).*
5. **Tensor force.** With Pauli matrices and a random q:
   (σ₁·q)(σ₂·q) = (q²/3)[σ₁·σ₂ + S₁₂], S₁₂ = 3(σ₁·q̂)(σ₂·q̂) − σ₁·σ₂. Check all 16
   entries of the 4×4 matrix.
6. **Goldberger–Treiman.** g_πNN = g_A M_N/f_π = 13.01 against 13.1. The tolerance of
   2% is (m_π/4πf_π)², the size of the next chiral order.

---

## 5. Rung 3: Casimir–Polder between the diamonds

**Postulate.** Maxwell's equations in a linear dielectric, and the fluctuation formula
U = −(ħ/2π)∫₀^∞dξ α₁(iξ)α₂(iξ) Tr[G(iξ)G(iξ)] (Casimir and Polder 1948; quoted, §9).

1. **Polarizability from Laplace.** Inside the sphere Φ = A r cosθ, outside
   Φ = −E₀ r cosθ + B cosθ/r² (R = E₀ = 1). Continuity of Φ gives A = −1 + B; continuity
   of ε∂_rΦ gives εA = −1 − 2B. So B = (ε−1)/(ε+2) and α/(4πε₀) = K R³. Solve this with
   Fractions.
2. **The Green tensor at imaginary frequency.** u = ξr/c:
   G_ij = e^(−u)/r³ [(1+u+u²)δ_ij − (3+3u+u²) r̂_i r̂_j]. Check (∇² − ξ²/c²)G = 0 off the
   source (Richardson-extrapolated Laplacian), and
   Tr G·G = 2e^(−2u)(3 + 6u + 5u² + 2u³ + u⁴)/r⁶.
3. **The exact number 23/4.** With constant α, ∫₀^∞ e^(−2u)uⁿ du = n!/2^(n+1), so
   ∫ e^(−2u)(3 + 6u + 5u² + 2u³ + u⁴) du = 3/2 + 3/2 + 5/4 + 3/4 + 3/4 = **23/4** in
   Fractions. Hence **U = −(23/4π) ħc α₁α₂ / r⁷**.
4. **The safe gap.** Casimir ∝ R⁶/r⁷ and gravity ∝ R⁶/r (both diamonds have mass ∝ R³),
   so their ratio doesn't depend on the mass. Scan the gap for the smallest value where
   the Casimir entangling phase is ≤ 10% of gravity's: **181.16 µm**.

---

## 6. Rung 4: gravity to the experiment

**Postulate.** Einstein's equations, linearized about flat space: g = η + h,
□h̄_μν = −16πG T_μν, with h̄ = h − ½η h.

1. **Newton and γ = 1.** A static point mass gives h̄₀₀ = 4GM/r (Poisson). Undoing the trace
   reversal gives h₀₀ = h_ii = 2GM/r, so Φ = −GM/r and the PPN parameter γ = h_ii/h₀₀ = 1.
   Do the trace reversal in Fractions.
2. **One-graviton exchange.** The amplitude is ∝ T₂^μν P_μνρσ T₁^ρσ with
   P = ½(η_μρη_νσ + η_μση_νρ − η_μνη_ρσ). Static masses: T₂·P·T₁ = m₁m₂/2, so
   U(q) = −4πGm₁m₂/q². Rung 2's transform at m = 0 gives U(r) = −Gm₁m₂/r.
3. **Light bends twice as much.** A photon, T = E(1,0,0,1), gives twice the contraction of a
   static mass of the same energy: 4GM/(c²b), not 2GM/(c²b).
4. **The entangling phase.** Each diamond is in a superposition of two positions; branch
   pair (i,j) accumulates φ_ij = (Gm²/ħ)∫dt / d_ij(t). The observable is
   **Δφ = φ_LL + φ_RR − φ_LR − φ_RL**. In the parallel geometry d_LL = d_RR = gap and
   d_LR = d_RL = √(gap² + (2y(t))²). y(t) rises smoothly over a ramp, holds, and returns.
   Integrate with the trapezoid rule. Design A's parameters (from the repository's design
   scan) and rung 3's gap give **2.1868 rad**.

---

## 7. Rung 5: gravity as a broken SO(4,1) gauge theory

**Postulate.** A connection valued in so(4,1),
A = ½ω^{ab}J_ab + (1/ℓ)e^a J_a4, with curvature F = dA + A∧A and action
N∫ε_abcd F^{ab}∧F^{cd} (MacDowell–Mansouri 1977). This is a *reformulation* of GR + Λ,
not new physics.

1. **The algebra and its breaking.** Write J_AB as explicit 5×5 matrices with η = (−,+,+,+,+).
   Check [J_a4, J_b4] ∝ J_ab. The generators that leave V = (0,0,0,0,ℓ) fixed are the
   6 Lorentz J_ab; the 4 J_a4 are broken, and DV^a = e^a: **the tetrad is the Goldstone
   direction.**
2. **A real spacetime.** Take the static metric −f dt² + dr²/f + r²dΩ². Its tetrad is
   diag(√f, 1/√f, r, r sinθ), and the spin connection has ω⁰₁ₜ = f′/2,
   ω²₁θ = √f, ω³₁φ = √f sinθ, ω³₂φ = cosθ. Prove it is the right one: the torsion
   de + ω∧e = 0, by finite differences.
3. **Curvature splits.** Compute F from A (finite-difference dA plus commutators) and R from
   ω alone. Check **F^{ab} = R^{ab} − e^a∧e^b/ℓ²** and **F^{a4} = T^a/ℓ = 0**.
4. **Vacuum and field equations.** de Sitter, f = 1 − r²/ℓ², gives F ≡ 0, so Λ = 3/ℓ².
   The Ricci contraction of F vanishes for Schwarzschild–de Sitter and not for
   Schwarzschild: that is G_μν + Λg_μν = 0.
5. **The action.** Expand ε F∧F = Euler + (2s/ℓ²)·2eR + (1/ℓ⁴)·24e with the wedge routine
   (compute the 2 and the 24; don't type them), and read off Λ = 3/ℓ² and N = −3/(64πGΛ).
   With the measured Λ: ℓ = 1.65×10²⁶ m and a coupling of 10¹²², which is the
   cosmological-constant problem in this language.

---

## 8. Rung 6: black holes

**Postulate.** The same static metrics, plus the Kerr solution in horizon variables. The
only quantum input is "T = κ/2π", and it is *derived* geometrically in step 2. What is quoted
is that this T is the temperature of real radiation (Hawking 1975).

1. **Surface gravity from the Killing vector.** ξ = ∂_t, κ² = −½(∇_μξ_ν)(∇^μξ^ν) at the
   horizon. Build the Christoffels from finite differences of the metric (f only, never f′),
   evaluate just outside the horizon, and compare with |f′(r_h)|/2 and with rung 5's ω⁰₁ₜ.
   Find the horizons of Schwarzschild–de Sitter by bisection.
2. **Temperature from smoothness.** With t = −iτ the metric is f dτ² + dr²/f. Near r_h,
   ρ = ∫dr/√f gives f ≈ κ²ρ², so ds² ≈ dρ² + κ²ρ²dτ²: a plane only if τ ~ τ + 2π/κ, and
   otherwise a cone. Compute circumference/(2πρ) (substitute r = r_h + u² so the
   integrand is finite) and get 1 for β = 2π/κ. The discriminating test is not a slightly
   wrong period but *another geometry's* period: Schwarzschild's 8πM, used in SdS, leaves a
   cone.
3. **First law and Smarr, exactly.** Write Kerr in r₊ = p, r₋ = q: M = (p+q)/2, a² = pq,
   S = π(p² + a²), T = (p−q)/(4π(p²+a²)), Ω = a/(p²+a²), J = Ma. π cancels in T dS, and
   Ω dJ needs only a², so everything is rational. With Duals over Fractions, check
   **dM − T dS − Ω dJ = 0** and **M = 2TS + 2ΩJ** with `==` on random rational horizons.
4. **Nariai.** f = f′ = 0 at r = 3M exactly when 27M²/ℓ² = 1, i.e. 9G²M²Λ = c⁴. The two
   horizons and their κ merge, and beyond that there is no static region. With the
   measured Λ this gives the largest possible black hole, 4.27×10⁵² kg.
5. **Orbits without closed forms.** The photon sphere is the maximum of f/r² (golden
   section): 3M; the shadow radius is b_c = √27 M. For massive particles,
   V = (1 − 2/r)(1 + L²/r²). Bisect on L² for where the circular orbits (dV/dr = 0) first
   appear: L² = 12, r_ISCO = 6M, E² = 8/9.
6. **Data.** EHT: compare θ_g = GM/(c²D) (from stellar-dynamics masses) with the EHT's
   ring-calibrated θ_g, using the measured error on the side facing the prediction.
   GW250114: area 8π(GM/c²)²(1 + √(1−χ²)). The initial area comes from the component
   masses, with spin 0 to maximize it. The final area comes from *inverting* the ringdown's
   (f, γ) through the QNM fit. Don't use the full-signal remnant for this: that fit
   assumes GR.

---

## 9. Links: where the rungs meet

1. **Neutral matter (1 → 4).** For random rational β, X_L, X_t and N_c, check exactly that
   q_p + q_e = [SU(3)_L]²U(1)_X anomaly / N_g, using the N_c-quark proton
   ((N_c+1)/2 u, (N_c−1)/2 d). Then the experiment's requirement: Coulomb and gravity both
   go as 1/r on the same trajectories, so the ratio of their phases is kQ²/(Gm²).
   Q < √(0.1G/k)·m per diamond gives **2.8×10⁻¹⁹ e per nucleon**, independent of size.
2. **π⁰ → γγ (1, 2).** N_c(Q_u² − Q_d²) = 1 for every N_c (Fractions). Sum
   |A ε^{μνρσ}ε₁ε₂k₁k₂|² over polarizations (A²m⁴/2), then apply two-body phase space with
   identical photons: Γ = α²m_π³/(64π³f_π²) = 7.785 eV. The anomaly coefficient is
   quoted (Adler; Bell–Jackiw).
3. **Planck mass (4 → 1).** M_Pl = √(ħc/G) from rung 4's G equals the 3-3-1 cutoff.
   G → xG moves M_Pl by x^(−1/2), which gives the window of G in which N_c = 3 survives
   and N_c = 5 doesn't.
4. **Diamond as black hole (6 → 4).** 2Gm/c² = 2.2×10⁻⁴¹ m, a millionth of l_P.
5. **Planck-mass black hole (6 → 3).** k_B T_H = M_Pl c²/8π exactly, radius 2 l_P.

---

## 10. Pushing the boundary further: replacing quoted results

These are where the script stops deriving. Each could be brought inside, in rough order of
effort:

| Quoted now | How to derive it | Effort |
|---|---|---|
| 3-3-1 Landau poles (`POLES_331`) | One-loop running dα_i⁻¹/d ln μ = −b_i/2π. Get b_i from the field content (b = −11/3 C₂(G) + 2/3 Σ T(F) + 1/3 Σ T(S)) and find where α_X⁻¹ → 0. One loop gives the order of magnitude; the pinned values are three loops with thresholds (`src/m331_three_loop.py`) | small for one loop |
| Casimir–Polder formula | Second-order perturbation theory of two dipoles coupled to the quantized field, or the zero-point energy shift of the field modes; Wick-rotate ω → iξ | medium |
| Radiative correction to M_Z (+0.35%) | The one-loop oblique corrections Δr; needs m_t, m_H | medium–large |
| ChPT low-energy constants ℓ̄₃, Σ | Lattice QCD. Not feasible in a standard-library script; it stays an input | — |
| ABJ anomaly coefficient | The triangle diagram, or Fujikawa's path-integral Jacobian | medium |
| Hawking radiation as radiation | Bogoliubov coefficients of a field on the collapsing geometry, which give a Planckian spectrum at κ/2π | large |
| Berti–Cardoso–Will QNM fit | Leaver's continued fraction for the Teukolsky equation, solved for ω(χ) | medium |
| Design A's parameters | Re-run the design scan (`src/stur_gravity_entanglement.py`) | small |

---

## 11. Workflow that keeps it honest

1. **Write the check first,** with its tag and its tolerance justified in words (a
   tolerance without a reason is a fudge).
2. **Postulate in data, derive in code.** Generator matrices, f(r), V(φ) and the field
   content are typed. Masses, charges, κ, 23/4 and Λ = 3/ℓ² are computed.
3. **Two routes to every key number:** closed form vs numerics (κ = f′/2 vs the Killing
   invariant), exact vs float (23/4), or derivation vs measurement.
4. **Make each check falsifiable:** include a case that *must* fail (Schwarzschild without
   Λ fails the SdS field equation; the wrong Euclidean period leaves a cone).
5. **Pin, don't trust:** results from heavier code become `[pinned]`, with a test that
   compares them against that code (`tests/test_ladder_standalone.py`).
6. **Exit non-zero on failure,** so CI enforces all of the above.

Start the file with the toolkit and its self-tests, then add one rung at a time, running
the whole file after each. When the last link passes, you will have rebuilt
`ladder_standalone.py`, and you will know which of its numbers are derived, which are
measured, and which are still borrowed.
