# The symmetry-breaking ladder: from 3-3-1 to the diamond experiment

*Worked examples, not peer reviewed. Every result below is computed by a script in `src/`
and pinned by a test. Labels: **CHECK** (computed here), **MODEL** (a stated model of the
physics), **REFORMULATION** (an equivalent rewriting), **LIT** (a measured input or a
quoted result).*

This page follows the forces down in energy, from the 3-3-1 scale to the two diamonds of
[GRAVITY_ENTANGLEMENT.md](GRAVITY_ENTANGLEMENT.md). At each rung it states what breaks,
how, what follows, and what is derived. The forces don't turn into one another: at each
threshold a symmetry breaks and the forces separate. Gravity is not part of the chain. It
sits beside it at every scale, with Newton's G as its own input. Its rung is written as a
broken gauge theory too, in an equivalent reformulation of GR. Rung 6, black holes, is not
a symmetry breaking and does not extend the chain: it is the strong-field end of gravity's
column, and the first place ħ, G, c and k_B appear in one formula.

## What is an input and what is derived

**Inputs, all measured:**
- the gauge couplings at one scale;
- the Fermi constant G_F, which gives v = (√2 G_F)^(−1/2) = 246.22 GeV;
- the light-quark masses, f_π, g_A and the nucleon mass;
- the quark condensate (lattice QCD, FLAG);
- the permittivity of diamond;
- G and the cosmological constant Λ;
- for rung 6: black-hole masses and distances measured without the EHT (stellar dynamics
  and stellar orbits), the EHT ring diameters, and GW250114's published masses, spins and
  ringdown fit;
- for the links: α(0), and the measured limits on q_p + q_e and q_n.

The 3-3-1 scale w is not known. It is bounded below by the LHC Z′ search.

**Not derived, by anyone:** why these inputs have their values, and how gravity unifies
with the other forces. Where a step uses a quoted result instead of a derivation, it is
marked.

## Rung 1: 3-3-1 → Standard Model → electromagnetism (`src/m331_breaking.py`)

**The mechanism.** Gauge group SU(3)_C × SU(3)_L × U(1)_X, with charge Q = T₃ + βT₈ + X,
β = ±1/√3.
- **Step 1, at w.** The triplet χ gets a vacuum value w/√2 and breaks SU(3)_L × U(1)_X to
  SU(2)_L × U(1)_Y.
- **Step 2, at v.** Two more triplets get v₁/√2 and v₂/√2, with v² = v₁² + v₂², and break
  SU(2)_L × U(1)_Y to U(1)_em.
- **Colour SU(3)_C is never broken.**

The gauge-boson mass matrix is computed from the generators and the vacuum values,
M²_AB = g_A g_B Σ_φ ⟨φ⟩†{t_A, t_B}⟨φ⟩, for both variants.

| | Result | Status |
|---|---|---|
| B0 | Each scalar triplet's neutral components follow from Q, and fix where each vacuum value can sit | CHECK |
| B1 | The 9×9 mass matrix has rank 8: 8 gauge bosons become massive, each eating a Goldstone boson | CHECK |
| B2 | The massless state is the gauge field of **Q = T₃ + βT₈ + X**: the photon, with 1/e² = (1 + β²)/g² + 1/g_X² | CHECK |
| B3 | After step 1 alone, 4 states stay massless: SU(2)_L and one U(1). That U(1) is **Y = βT₈ + X**, and **1/g_Y² = β²/g² + 1/g_X²**. This matching condition was typed into the 3-3-1 running code by hand; it now follows from the mass matrix | CHECK |
| B4 | M_W = gv/2; bileptons M² = g²(w² + v_i²)/4; at leading order in v/w, M_Z² = (g² + g_Y²)v²/4 and M_Z′² = (g² + β²g_X²)w²/3. So **M_Z′/M_V = √(4/3·(1 + β²t_X²))**, the formula `src/m331_threshold.py` used, now derived (zero residual) | CHECK |
| B5 | Z–Z′ mixing: ρ = M_W²/(M_Z² cos²θ_W) = 1 + (v/w)² × (a perfect square), so ρ ≥ 1 at tree level. Checked against exact diagonalization to 3×10⁻⁹ | CHECK |
| B6 | Every fermion's charge from Q, component by component, for N_c = 3, 5 and 7. Anti-triplets carry −T*. Every SU(2)_L doublet is (Q_u, Q_d) or (0, −1), with Q_u = (N_c + 1)/2N_c and Q_d = (1 − N_c)/2N_c | CHECK |
| B7 | v = 246.22 GeV from G_F. The tree-level M_Z = 91.51 GeV, against the measured 91.19: the +0.35% is the known radiative correction, not derived here | CHECK |

**After the Standard Model's loops (`src/m331_rho_bound.py`).** B7's +0.35% is known
Standard Model physics, not a test of 3-3-1. What the global fit leaves after the Standard
Model's loops is ρ₀ = 1.00039 ± 0.00019 (LIT: Erler, arXiv:1908.07346; a fit from before
the 2022–2024 W-mass measurements). That residual is where B5's mixing would show.

| | Result | Status |
|---|---|---|
| R1 | B5's coefficient is a perfect square: **ρ − 1 = (v/w)²(sin²a − sin²a₀)²**, tan a = v₂/v₁, with sin²a₀ = (3 − 2x)/2(3 + x) for β = +1/√3 and (3 + 4x)/2(3 + x) for β = −1/√3, x = g_X²/g². The two add to 1. So the mixing vanishes at one ratio of the vacuum values | CHECK |
| R2 | sin²a₀ = 0.350 and 0.650 (s² at M_Z); 0.333 and 0.667 at 4 TeV | CHECK |
| R3 | ρ₀ − 1 < 7.6×10⁻⁴ (95% CL) gives **w > 5.8 TeV at most**, and nothing at a = a₀. The LHC Z′ recast gives w > 11.9 TeV (β = +1/√3) and 10.3 TeV (β = −1/√3) for every a: ρ is weaker by a factor of about 2 | CHECK; LIT ρ₀ |
| R4 | The 2σ excess in ρ₀ would need w < 8.1 TeV. At the LHC bound, the mixing gives at most 47% (β = +1/√3) or 62% (β = −1/√3) of it, leaving 1.1σ or 0.8σ | CHECK |

**What this leaves out.** This is ρ alone, at tree level, not a full electroweak-precision
bound:
- **The Z-pole couplings.** The mixing also shifts the Z's couplings to fermions, at the
  same order (v/w)². That fit is below.
- **One-loop T from the bilepton gauge bosons:** about (g²/16π²)(M_W²/M_V²), a loop factor
  below the tree term. The exotic fermions are SU(2) singlets and contribute little.
- **One-loop T from the scalars:** not loop-suppressed in the same way. The second Higgs
  doublet's splittings come from the quartics, so its contribution goes as λ²/16π². With
  heavy scalars near the 0.1 TeV floor of NOTE_331.md §3e it isn't suppressed by v/w at
  all, and ρ then constrains the scalar spectrum, not w. Its sign is free, so it can lift
  R3's cancellation at a = a₀ or offset R4's tree term.
- **S and U** aren't used.

So R3 and R4 hold for the tree-level mixing with heavy, weakly coupled scalars.

**The Z-pole fit (`src/m331_zpole.py`).** Both effects of the mixing, ρ and the shifted Z
couplings, fitted to 14 LEP/SLD Z-pole observables at tree level, linear around the
Standard Model.
- Measurements and correlations: LEP/SLD, Phys. Rept. 427 (2006) 257 (LIT).
- SM predictions: Gfitter, Eur. Phys. J. C 78 (2018) 675 (LIT).
- The inputs, each with its table: [`results/m331/zpole/zpole_inputs.json`](results/m331/zpole/zpole_inputs.json).

| | Result | Status |
|---|---|---|
| Z1 | χ²_SM = 14.2 for 14 observables; A⁰,b_FB (−2.3σ) gives 4.6 of it | CHECK; LIT |
| Z2 | **Validation** against Erler, Langacker, Munir and Rojas, JHEP 08 (2009) 017, 95% CL sin θ_ZZ′: Z′_χ here [−0.0015, +0.0008], theirs [−0.0016, +0.0006]; Z′_ψ here [−0.0022, +0.0008], theirs [−0.0018, +0.0009]. Asymmetry reproduced, edges within 0.0004, widths within 12% (about 6% in w); their fit has more data | CHECK; LIT |
| Z3 | θ = (v/w)(sin²a₀ − sin²a) M_Z/M_Z′, against exact diagonalization of rung 1's mass matrix to < 0.5%. The same a₀ cancels θ and ρ − 1 together | CHECK |
| Z4 | **w > 7.5 TeV (β = +1/√3) and 7.6 TeV (β = −1/√3)** for every a and every choice of the odd quark generation (6.0 and 6.4 TeV without A⁰,b_FB). Stronger than ρ alone (5.8 TeV), below the LHC's 11.9 and 10.3 TeV by 1.6× and 1.4× in w. Near a = a₀ the Z pole gives almost nothing | CHECK; MODEL |
| Z4 | No significant preference for mixing: χ² improves by at most 1.0 (2.9 without A⁰,b_FB) for two extra parameters | CHECK |

Not included: loop contributions to T (above), correlated SM parametric errors (treated as
independent), M_W, low-energy parity violation and flavour-changing Z′ couplings.

## Rung 2: the strong force (`src/chiral_breaking.py`)

**What breaks.** Colour stays unbroken. What breaks is the approximate chiral symmetry of
the light quarks, SU(2)_L × SU(2)_R → SU(2)_V, through the quark condensate ⟨q̄q⟩. The
pions are its near-Goldstone bosons, and their exchange is the long-range nuclear force.
The derivation uses the linear sigma model (Gell-Mann and Lévy 1960), the minimal model
with this breaking pattern. It is a **MODEL** of QCD's low-energy structure, not QCD
itself. S6–S8 then compute the pion mass in chiral perturbation theory, QCD's own
low-energy effective theory, at O(p⁴), so that number no longer rests on the model.

| | Result | Status |
|---|---|---|
| S1 | With massless quarks: exactly **3 zero modes**, dim O(4) − dim O(3) = 6 − 3: the pions | MODEL; CHECK |
| S2 | With quark masses: m_π² = H/⟨σ⟩ and f_π = ⟨σ⟩, so **m_π² f_π² = (m_u + m_d)\|⟨q̄q⟩\|** (Gell-Mann–Oakes–Renner) | MODEL; CHECK |
| S3 | With measured m_u + m_d, f_π and the lattice condensate: m_π = **127.6 MeV**, against 135.0. This is leading order with the physical f_π standing in for the chiral-limit F; S7 corrects it | CHECK; LIT inputs |
| S4 | Exchanging a particle of mass m gives V(q) ∝ 1/(q² + m²), whose Fourier transform is **e^(−mr)/(4πr)** (derived symbolically). The range is 1/m_π = **1.414 fm**. The spin structure (σ₁·q)(σ₂·q) = (q²/3)[σ₁·σ₂ + S₁₂] gives the central and **tensor** nuclear forces | CHECK |
| S5 | Goldberger–Treiman: g_πNN = g_A M_N/f_π = **13.01**, against about 13.1 empirically (−0.7%, the known discrepancy; the empirical value is quoted approximately) | CHECK |
| S6 | Chiral perturbation theory (Weinberg, Physica A 96 (1979) 327; Gasser–Leutwyler, Ann. Phys. 158 (1984) 142). Its O(p²) Lagrangian (F²/4)Tr(∂U∂U†) + (F²M²/4)Tr(U + U†) is fixed by the symmetry. The one-loop mass comes from Wick-contracting its quartic terms (the tadpole): **M_π² = M²(1 + Δ/2F²)**. It's derived in two parametrizations of U, which split the loop differently between wave function and mass but agree on the physical mass. The tadpole in dimensional regularization is Δ = (M²/16π²)[ln(M²/μ²) − 1/ε̄ − 1], also derived. So M_π² = M²[1 − (M²/32π²F²) ℓ̄₃], the NLO term of FLAG 19's eq. (MF) | CHECK, symbolic |
| S7 | S3 at O(p⁴), with consistent leading order M² = 2m̂Σ/F² and N_f = 2+1 lattice inputs: m̂ = 3.364(41) MeV (FLAG 2024, arXiv:2411.04268), and Σ^(1/3) = 272(5) MeV, F_π/F = 1.062(7), ℓ̄₃ = 3.07(64) (the FLAG 19 averages, restated unchanged in FLAG 21, arXiv:2111.09849; FLAG 2024 omits the low-energy constants). The result is **m_π = 132.6 ± 3.8 MeV against 135.0** (−0.6σ), with the error mostly from the condensate. The O(p⁴) term is −2.3% of M². Most of S3's −5.5% came from using f_π for F, not from the loop | CHECK; LIT inputs |
| S8 | F_π/F = 1 + (M²/16π²F²) ℓ̄₄ (FLAG 19 eq. (MF)) = 1.061 with FLAG's ℓ̄₄ = 4.02(45), against FLAG's 1.062(7). This is a consistency check of the lattice inputs, not an independent test (same fits) | CHECK; LIT formula |

S1–S5 remain the linear sigma model. Its σ is not QCD's broad f₀(500), and chiral
perturbation theory has no σ field. The pion mass is now a result of QCD's own effective
theory, carrying the lattice inputs' uncertainty rather than the model's caveat.

**Where the derivation stops.** Deriving the proton mass and nuclear binding needs lattice
QCD and nuclear many-body theory. They are not derived here.

## Rung 3: electromagnetism, the experiment's background (`src/casimir_diamonds.py`)

**Why it survives.** U(1)_em is never broken, so the photon stays massless and
electromagnetism is long-range. Between two neutral diamonds what's left is the
Casimir–Polder force.

| | Result | Status |
|---|---|---|
| P1 | The polarizability of a dielectric sphere, from Laplace's equation with the boundary conditions: **α/(4πε₀) = KR³, K = (ε − 1)/(ε + 2)** | CHECK |
| P2 | The dipole Green tensor at imaginary frequency satisfies the wave equation and is transverse off the source; **Tr G·G = 2e^(−2u)(3 + 6u + 5u² + 2u³ + u⁴)/r⁶** | CHECK |
| P3 | The Casimir–Polder fluctuation formula U = −(ħ/2π)∫dξ α₁α₂ Tr G·G (LIT: Casimir and Polder 1948, the one quantum step quoted, not derived). For constant α, the integral is exactly **23/4**, so **U = −(23/4π) ħc α₁α₂/r⁷** | CHECK; LIT formula |
| P4 | This is the formula the experiment code had quoted as known; it agrees to 12 digits. At 200 µm, Casimir/gravity = 2.3×10⁻². Casimir ∝ R⁶/r⁷ and gravity ∝ R⁶/r, so the safe gap doesn't depend on the mass: 181 µm | CHECK |
| P5 | At temperature T the frequency integral becomes the Matsubara sum. With constant α it is exact in closed form: **U_T = U₀ η(τ)**, τ = 2πk_BTr/ħc, with **η = 1 + (22/21735)τ⁶ + …** at small τ and η → 6τ/23 (U_T → −3k_BTα₁α₂/r⁶) at large τ. It agrees to machine precision with Boyer's far-zone result (PRA 11, 1650 (1975)) in the form of Passante and Spagnolo, PRA 76, 042112 (2007), eq. (11), including the τ⁶ term. The regimes are those of Goedecke and Wood, PRA 60, 2577 (1999). Constant α: only ξ up to ~10c/r = 1.7×10¹³ rad/s matter at the gap. Ideal diamond has zero Born effective charges (Lawler and Shirley, arXiv:cond-mat/0407541), and its one-phonon absorption at 1332 cm⁻¹ (2.5×10¹⁴ rad/s) is forbidden (Shiryaev et al., Meteorit. Planet. Sci. 57, 730 (2022)). So its lowest lattice absorption is 15× above the frequencies that matter | CHECK, exact; LIT |
| P6 | The safe gap at finite temperature. At the design's 0.15 K it moves by 1×10⁻¹¹, and at 4.2 K by 0.2%. It grows by 6% at 10 K and by 1.7× (to 0.31 mm) at 77 K. Thermal corrections don't tighten the gap at the design's temperature. With design A's own branch separation (721 µm, not the 250 µm H0 used) the gap would be 164 µm, so 181 µm is conservative | CHECK |
| P7 | Electric dipoles against H6's bound at design A, **p < 2.8×10⁻⁴ e·µm**. *Measured:* levitated silica microspheres carry permanent dipoles of typically ~100 e·µm, roughly mass-independent (Afek et al., PRA 104, 053512 (2021)). That is 3.6×10⁵× the bound, and still 3×10³× after the ×120 cancellation they demonstrate. *Model:* random patches of rms V and size l ≪ R give a dipole of **√(12π) ε₀ R l V** per axis (checked by Monte Carlo), so the bound needs **V l < 8.3×10⁻¹³ V m**. Patches measured on gold (V_rms 15–28 mV; scales 30–100 nm and 300–1000 nm; Garrett, Somers and Munday, J. Phys.: Condens. Matter 27, 214012 (2015)) exceed it 500–5000×. Diamond has not been measured. Afek et al. note that a conducting shield "would not necessarily eliminate such forces due to the dipole-shield interaction", so H6's remedy is not established for dipoles. **Dipole control at the 10⁻⁴ e·µm level is an open requirement of the design** | LIT; MODEL |

## Rung 4: gravity to the diamond experiment (`src/graviton_exchange.py`)

**Where gravity stands.** Gravity does not come out of rungs 1–3. Its low-energy quantum
description is GR as an effective field theory, which is what the diamond test probes.
TEGR gives the same results ([TEGR.md](TEGR.md), E1–E2).

| | Result | Status |
|---|---|---|
| N1 | Linearized GR for a point mass: h̄₀₀ = 4GM/r, so h₀₀ = 2GM/r and h_ij = 2GM/r δ_ij. That gives **Φ = −GM/r** and **PPN γ = 1** | CHECK |
| N2 | One-graviton exchange: T₂·P·T₁ = m₁m₂/2 for static masses, so U(q) = −4πGm₁m₂/q², and with rung 2's Fourier transform at m = 0, **U(r) = −Gm₁m₂/r**: Newton's law | CHECK |
| N3 | The same contraction with a photon is **twice as large**: the factor 2 in light bending, 4GM/(c²b) | CHECK |
| N4 | Design A (1.468×10⁻¹⁴ kg, Δx = 720.8 µm, gap 181.2 µm, ramps 2 × 1.581 s, hold 0.082 s), with the N2 potential integrated along the branch trajectories: **Δφ = 2.1868 rad**, equal to the experiment code's 2.19 rad | CHECK |

**What a positive result would establish (FOLLOWS):** gravity's field can be in a
superposition. Under the experiment's assumptions (locality, local operations and classical
communication), a classical field cannot entangle the diamonds. This is what N2's graviton
field predicts.

**What it would not establish:** what gravity is at the Planck scale; any difference
between GR and TEGR; any link between gravity and 3-3-1.

## Rung 5: gravity as a broken gauge theory (`src/macdowell_mansouri.py`)

**The reformulation.** GR with a cosmological constant can be written as a gauge theory of
the de Sitter group SO(4,1), broken to the Lorentz group SO(3,1): MacDowell and Mansouri,
PRL 38 (1977) 739; Stelle and West, PRD 21 (1980) 1466. The connection is
A = ½ω^{ab}J_ab + (1/ℓ)e^a J_a4. This is a **REFORMULATION**: the same predictions as
GR + Λ, and no unification with the other forces.

| | Result | Status |
|---|---|---|
| M1 | so(4,1) = so(3,1) + 4 "translations", with [P_a, P_b] ∝ J_ab/ℓ². A de Sitter vector V = (0,0,0,0,ℓ) leaves the **6 Lorentz generators** unbroken and breaks **4**. In the gauge V = ℓ e₄, **DV^a = e^a**: the tetrad is the broken direction | CHECK |
| M2 | On any static spherical spacetime, with explicit 5×5 matrices: **F^{ab} = R^{ab} − e^a∧e^b/ℓ²** and **F^{a4} = T^a/ℓ = 0** (no torsion). R^{ab} is checked against the metric's Ricci scalar | CHECK |
| M3 | De Sitter space of radius ℓ has **F = 0** identically: the vacuum is the flat SO(4,1) connection, and Λ = 3/ℓ² | CHECK |
| M4 | The action N∫ε_abcd F^{ab}∧F^{cd} splits as the Euler density plus 2·(2s/ℓ²) eR plus 24(s²/ℓ⁴)e. The ratio of the last two terms gives **Λ = 3/ℓ²**, consistent with M3. 1/(16πG) fixes **N = −3/(64πGΛ)**. The Euler density is 4 sin θ · d/dr[f f′ − f′], a total derivative, so it doesn't change the field equations (KNOWN in general: the Chern–Gauss–Bonnet density) | CHECK |
| M5 | Schwarzschild–de Sitter satisfies G_μν + Λg_μν = 0 with Λ = 3/ℓ² | CHECK |
| M6 | The measured Λ gives ℓ = 1.65×10²⁶ m (17 billion light years). The dimensionless coupling 3/(GΛ) is about **10¹²²** in Planck units: the cosmological-constant problem, in this language | CHECK; LIT inputs |

## Rung 6: black holes, the strong-field end of gravity (`src/black_holes.py`)

**What this rung is, and isn't.** Nothing breaks at a black hole, so this rung is not a
step down the chain. It is gravity's column at its strong-field end, and it reuses rung 5's
static spherical tetrad, spin connection and Einstein tensor. It is also the first formula
on the ladder that needs ħ, G, c and k_B together: T_H = ħc³/(8πGMk_B).

| | Result | Status |
|---|---|---|
| H1 | The surface gravity is defined by the Killing vector ξ = ∂_t: **κ² = −½ (∇_μξ_ν)(∇^μξ^ν)** on the horizon f(r_h) = 0. Computed from the metric's Christoffel symbols alone (symbolically for any f, numerically from f by finite differences on both Schwarzschild–de Sitter horizons), it gives **κ = \|f′(r_h)\|/2**; Schwarzschild: r_h = 2GM/c², κ = 1/4M. Rung 5's spin connection carries the same number, ω⁰₁ₜ = f′/2, but it is written into the tetrad code directly, so that is only a cross-check; rung 5's torsion-free check is what validates it. T_H = ħcκ/(2πk_B), with κ in 1/m | CHECK; the Hawking formula is LIT (Hawking 1975) |
| H2 | **The Euclidean check.** With t = −iτ, the proper distance ρ from the horizon satisfies d√f/dρ = f′/2 exactly, so near r_h the (τ, r) plane is dρ² + κ²ρ²dτ². It is smooth only if τ has period **2π/κ**; any other period leaves a cone. So the temperature is fixed by the geometry, not put in. Symbolic for any f; numerically on both Schwarzschild–de Sitter horizons, with ρ integrated from f alone and the period from H1's Killing κ (ratio 1 to 3×10⁻⁶). The ratio is linear in the period, so a period 10% off proves nothing; instead, the period of a different f, Schwarzschild's 8πM, leaves a cone at the SdS black-hole horizon (ratio 0.788) | CHECK |
| H3 | With S = A/4ℓ_P²: Schwarzschild **dM = T dS** and **M = 2TS** (Smarr). Kerr, written in its two horizon radii so every quantity is rational: **dM = T dS + Ω dJ** and **M = 2TS + 2ΩJ**, in exact fractions on 60 random horizons (the standalone script) and symbolically (here). Reissner–Nordström, with κ derived from its f: dM = T dS + Φ dQ, M = 2TS + ΦQ | CHECK; Kerr's T, Ω are LIT (Bardeen, Carter and Hawking 1973) |
| H4 | Schwarzschild–de Sitter has a black-hole and a cosmological horizon with **different temperatures**, so no single Euclidean period is smooth at both. They merge where f = f′ = 0: r = 3GM/c² and **9G²M²Λ = c⁴** (the Nariai limit), and both κ go to zero. Beyond it there is no static region. With rung 5's measured Λ: the largest black hole the universe allows has **M = c²/(3G√Λ) = 4.27×10⁵² kg = 2.1×10²² M☉**, horizon at 1/√Λ = 9.5×10²⁵ m | CHECK; LIT Λ |
| H5 | From the effective potentials: **photon sphere 3GM/c²**; critical impact parameter, the shadow's radius seen from far away, **√27 GM/c²**; circular orbits need L² ≥ 12(GM/c)², and at that minimum the stable and unstable orbits merge at the **ISCO, 6GM/c²**, with E² = 8/9. The standalone script finds these numerically, without the closed forms | CHECK |
| H6 | **Event Horizon Telescope.** The EHT measures a bright ring, not the shadow, and converts its diameter to θ_g = GM/(c²D) with α = d/θ_g calibrated on GRMHD images; the calibration's spread over spin, inclination and emission is in its error bar. So the ring-to-shadow offset is applied as a correction with the EHT's own uncertainty, and the comparison is θ_g, from masses and distances measured without the EHT. M87*, stellar dynamics (Gebhardt et al. 2011; M/D doesn't depend on the distance assumed): **θ_g = 3.64 μas against the EHT's 3.8 ± 0.4 μas, +0.4σ** (shadow 2√27 θ_g = 37.8 μas; ring 42 ± 3 μas, so α = 11.1 against the Schwarzschild shadow's 10.4; EHT 2019, ApJL 875, L1 and L6). Sgr A*, stellar orbits (GRAVITY 2022, Keck 2019): **5.03 μas against 4.8 (−0.7 +1.4) μas, −0.2σ** (shadow 52.2 μas; ring 51.8 ± 2.3 μas, α = 10.8; EHT 2022, ApJL 930, L12). Each pull uses the EHT's error on the side facing the prediction. M87*'s gas-dynamics mass would give θ_g = 1.93 μas, 4.7σ off, and is excluded | CHECK; LIT data |
| H7 | **GW250114 and Hawking's area law.** Kerr area 8π(GM/c²)²(1 + √(1−χ²)). Initial: the published component masses, 33.6 and 32.2 M☉, give **237,000 km²** (spins 0, which maximizes it, so the published spin bound χ ≤ 0.26 is not needed). Final: inverting the ringdown-only fit of the 220 mode (247 Hz, damping 221 Hz, z = 0.09) gives M_f = 66.7 M☉, χ_f = 0.75 and **407,000 km²**. The full-signal remnant (62.7 M☉, 0.68) is not used for the area, because that fit assumes GR and obeys the area law by construction. At the least favourable corners of the published 90% ranges, 252,000 km² initial against 341,000 km² final, the area still grows. That is a heuristic, not a bound: the area need not be monotonic in (f, γ), so its minimum over the ranges need not sit at a corner. The collaboration finds A_f > A_i at > 4σ at all analysis points (arXiv:2509.08054) | CHECK; LIT data |
| H8 | The full-signal remnant predicts the 220 mode with the Berti–Cardoso–Will fit: **249 Hz and damping 244 Hz**, against the ringdown's 247 ± 6 Hz and 221 (−32, +39) Hz. Inspiral-plus-merger and ringdown describe the same Kerr black hole | CHECK; LIT data |

**Not measured, and labelled so.** *Hawking radiation* is under stated assumptions: quantum
fields on a fixed classical background. For GW250114's remnant T_H = 1×10⁻⁹ K, far below the
2.7 K microwave background, so it absorbs more than it radiates; no black hole's radiation
has been seen. *Whether information is lost* in black-hole evaporation is open. Anything
that needs quantum gravity, including what happens at a Planck-mass black hole (link 5), is
outside what this page computes. H3's entropy is the Bekenstein–Hawking formula; what it
counts is not derived here (see [TEGR.md](TEGR.md) for the corner-charge attempt).

## Links between the rungs (`src/ladder_links.py`)

The rungs above are separate derivations. In five places one rung's output is another
rung's input, and the link can be checked against a measurement or against the other rung's
code.

### Link 1: neutral matter, from rung 1 to rung 4

**Why rung 4 needs it.** Coulomb and gravity both fall as 1/r and act along the same branch
trajectories. So their entangling phases are in the exact ratio −kQ²/(Gm²), where Q is each
diamond's net charge. For Coulomb to stay below 10% of gravity, a diamond may carry at most
2.5×10⁻⁶ e. One stray electron gives 1.6×10¹⁰ times gravity's phase (H6 in
[GRAVITY_ENTANGLEMENT.md](GRAVITY_ENTANGLEMENT.md)), so the diamonds must be discharged.
Discharging removes whole electrons, but it can't remove a fractional charge per atom. That
residual is set by q_p + q_e and q_n.

| | Result | Status |
|---|---|---|
| L1a | For any β, any N_c and any U(1)_X charges of the lepton and quark triplets: **q_p + q_e equals the [SU(3)_L]²U(1)_X anomaly coefficient divided by N_g**, identically. Here the proton is the N_c-quark baryon, with (N_c + 1)/2 u and (N_c − 1)/2 d quarks. The identity uses two facts: u and d carry the same charges in the triplet and the anti-triplet, and the SU(3)_L³ count gives N_g(1 + N_c) = 2nN_c. In the Standard Model the same holds with [SU(2)_L]²U(1)_Y: q_p + q_e = N_cY_Q + Y_L. Also q_n + Q_ν = q_p + q_e identically, which is charge conservation in n → p e ν̄ | CHECK (symbolic); KNOWN in substance: charge quantization from anomalies (Geng–Marshak; Babu–Mohapatra 1989); in 3-3-1, de S. Pires and Ravinez, PRD 58, 035008 (1998) |
| L1b | With rung 1's charges (B6): q_p = 1, q_n = 0, q_e = −1 and Q_ν = 0 exactly, in both variants, for N_c = 3, 5 and 7. **Neutral matter doesn't select N_c**, just as π⁰ → γγ doesn't (link 2) | CHECK |
| L1c | Design A's requirement: **a residual below 2.8×10⁻¹⁹ e per nucleon**, which is √(0.1 G/k) u/e. It doesn't depend on the diamond's size, because the mass and the nucleon count scale together, as the Casimir-safe gap doesn't depend on the mass | CHECK |
| L1d | Measured: \|q_p + q_e\| < 1×10⁻²¹ e, and the same limit for q_n (Bressi et al., PRA 83, 052101 (2011)). Separately, q_n = (−0.4 ± 1.1)×10⁻²¹ e (Baumann et al., PRD 37, 3107 (1988)). **The margin is 280×.** At the bound, the residual totals 9×10⁻⁹ e per design-A diamond, less than one electron, so no discharging could compensate it. Rung 1 makes the residual exactly zero | CHECK; LIT bounds |

**What this does and doesn't say.** The experiment needs electric charge quantized at the
atomic level. Measurement gives that to 10⁻²¹ e, and anomaly cancellation gives it exactly,
in the Standard Model and in 3-3-1 alike. The Q_ν = 0 part is rung 1's charge assignment.
In 3-3-1 it is fixed by the remaining anomalies together with the Yukawas (de S. Pires and
Ravinez), which this page doesn't re-derive. Nothing here favours 3-3-1 over the Standard
Model.

### Link 2: π⁰ → γγ, from rung 1 to rung 2

The neutral pion of rung 2 decays to two photons through the chiral anomaly. The amplitude
is A = (α/πf_π) N_c(Q_u² − Q_d²) (LIT: Adler; Bell and Jackiw 1969; the anomaly
coefficient is quoted, not derived).

| | Result | Status |
|---|---|---|
| L2a | With rung 1's anomaly-fixed charges, **N_c(Q_u² − Q_d²) = 1 for every N_c**. Both derivations of the charges agree: [`src/m331_why_three.py`](src/m331_why_three.py) W2 and rung 1's B6 | CHECK |
| L2b | From M = A ε^{μνρσ} ε₁_μ ε₂_ν k₁_ρ k₂_σ: the sum over photon polarizations is A²m⁴/2, and two-body phase space with identical photons gives **Γ = A²m³/64π** | CHECK (symbolic) |
| L2c | With f_π = 92.07 MeV (a measured input that rung 2 uses, not one it derives) and α(0): **Γ = 7.785 eV**, against the PrimEx-I+II average 7.802 ± 0.117 eV (Larin et al., Science 368, 506 (2020)), −0.1σ | CHECK; LIT |
| L2d | With the charges held at ⅔ and −⅓ instead, the width would scale as (N_c/3)²: 21.6 eV at N_c = 5. **With anomaly-fixed charges the width can't select N_c.** The R-ratio can ([`src/m331_why_three.py`](src/m331_why_three.py) W6) | FOLLOWS |

The width checks that charges and colours come together the way anomaly cancellation
demands. It links rung 1's charges to rung 2's pion, but it isn't an independent test of
N_c = 3. The agreement at the 0.1σ level is partly luck: the next-order chiral corrections
are a few percent.

### Link 3: the Planck mass, from rung 4 to rung 1

The 3-3-1 selection asks every gauge coupling to stay perturbative up to the Planck mass,
and its scripts type M_Pl = 1.22089×10¹⁹ GeV as a number. That number is √(ħc/G), with the
same G that gives rung 4's 2.19 rad phase. The two halves of the repository shared this
input without either importing it from the other; [DEPENDENCIES.md](DEPENDENCIES.md) found it.

| | Result | Status |
|---|---|---|
| L3a | √(ħc/G), from rung 4's G, ħ and c, **equals the 3-3-1 cutoff** to 1×10⁻⁷ | CHECK |
| L3b | M_Pl scales as G^(−1/2). If G were x times its measured value, the selection would hold for (M_Pl/pole₃)² < x < (M_Pl/pole₅)². At the reference spectrum (M_V = 4 TeV, Yukawas and thresholds on, α = 1, three loops; NOTE_331.md §3d) that is **0.12 < x < 6×10¹⁴ for β = +1/√3** and 3×10⁻²¹ < x < 1×10⁸ for β = −1/√3. G is measured to 2.2×10⁻⁵ (CODATA 2018). The narrow side: with G 8.2× weaker, M_Pl would rise above N_c = 3's pole and exclude it | CHECK |
| L3c | At the mass floors with light heavy leptons (NOTE_331.md §3e), N_c = 3's pole is 0.61 M_Pl, so it fails at the measured G; it would pass only if G were 2.7× stronger. This restates the heavy-lepton condition in terms of G; it adds nothing to it | CHECK |
| L3d | The check uses G, measured at laboratory and solar-system distances, at 10¹⁹ GeV. That assumes gravity's strength doesn't run in between. In perturbative quantum gravity the corrections are of order (E/M_Pl)². Many hidden light species would lower the effective cutoff, which this doesn't cover. Above M_Pl, an asymptotically safe gravity term leaves the selection unchanged ([NOTE_331.md](NOTE_331.md) §3g) | FOLLOWS |
| L3e | L3b uses one spectrum. Over the 72-point threshold scan of [NOTE_331.md](NOTE_331.md) §3a (r_J, r_S, M_V, light doublets), β = +1/√3's N_c = 3 pole runs from **1.26 to 16 M_Pl**, so the lower edge runs from x = 0.004 to **0.63**. At the scan's worst point (M_V = 2 TeV, r_J = 0.5, r_S = 1/3, two light doublets) the selection fails for G only **1.6× weaker**. The N_c = 5 edge and β = −1/√3 stay many orders of magnitude away. So 8.2× is the reference spectrum's margin, not the model's | CHECK |
| L3f | Gravity's own term in the gauge running (src/m331_gravity_fixed_point.py). At the strength that keeps the Standard Model's hypercharge finite (f* = 0.0098, G* = 1), the reference pole moves from 2.86 to 2.94 M_Pl and the worst-case pole from 1.26 to 1.27 M_Pl: 3% or less, against the factor of 13 the spectrum spans. The heavy spectrum, not gravity's running, sets how close the edge comes | CHECK, given the model |

So the selection's cutoff and the diamonds' signal rest on one measured number. On its
narrow side the selection tolerates G about 8× weaker at the reference spectrum, but only
1.6× weaker at the worst spectrum the scan allows. That is still far outside G's 2×10⁻⁵
measurement error, and the uncertainty in the edge comes from the heavy spectrum, not from G.

**Finding more links.** [DEPENDENCIES.md](DEPENDENCIES.md) maps which script feeds which and
where each physical constant is typed. It lists the quantities that more than one part of the
repository uses without importing them from one place; those are the candidates for the next
link.

### Link 4: the diamond as a black hole, from rung 6 to rung 4 (`src/black_holes.py`)

Design A's diamond, 1.468×10⁻¹⁴ kg, has a Schwarzschild radius 2Gm/c² = **2.18×10⁻⁴¹ m**:
1.35×10⁻⁶ of the Planck length, and 2×10⁻³⁵ of its own radius. That is how weak the gravity
in the experiment is, and why its 2.19 rad phase needs seconds of coherence. Status: CHECK
(pinned).

### Link 5: a Planck-mass black hole, from rung 6 to link 3 (`src/black_holes.py`)

A black hole of one Planck mass has k_BT_H = M_Pl c²/8π = **4.86×10¹⁷ GeV**, 1/(8π) of the
cutoff the 3-3-1 selection runs to, and a horizon of 2ℓ_P. So link 3's cutoff has a physical
picture: the scale where a black hole is as small as the Planck length and as hot as the
Planck energy over 8π. The Hawking formula is semiclassical, and at this size it is used
past where it is trusted, so the number is an order of magnitude, not a prediction.
Status: CHECK for the identity; the physics there needs quantum gravity.

### Link 6: the diamond's mass, from rung 2 to rung 4 (`src/ladder_links.py` L6)

The mass in rung 4's phase is the diamond's, and almost all of it is QCD.

| | Result | Status |
|---|---|---|
| L6a | Carbon-12 from its constituents: 6m_p + 6m_n + 6m_e − 12u = **92.162 MeV**, 7.680 MeV per nucleon (CODATA 2018; exact, since 12 u is the atom's mass by definition). This is the nuclear binding: the residual strong force, which rung 2's one-pion exchange describes at long range, minus the protons' Coulomb repulsion | CHECK; LIT |
| L6b | Each nucleon, by the Feynman–Hellmann theorem: the light-quark masses contribute σ_πN = 42.2(2.4) MeV and the strange quark σ_s = 44.9(6.4) MeV (FLAG 2024, N_f = 2+1; the N_f = 2+1+1 averages, 60.9(6.5) and 41.0(8.8) MeV, are carried as the spread). The rest is gluon field energy and quark motion | CHECK; LIT |
| L6c | Design A's diamond is **91% QCD field energy**, 4.5% u and d quark masses, 4.8% strange-quark mass, 0.03% electrons, −0.8% nuclear binding (N_f = 2+1+1: 90%, 6.5%, 4.4%) | CHECK |
| L6d | The phase goes as m². With massless u and d quarks (first order in σ_πN) the same diamonds give **1.99 rad** instead of 2.19; with every quark and the electron massless, 1.80 rad. The entanglement does not need the Higgs mechanism's light-fermion masses: what the experiment weighs is QCD | FOLLOWS, first order |

Heavy quarks enter the nucleon mass through the trace anomaly and are counted with QCD here.
The first-order counterfactual ignores how the binding and the strange-quark term would
themselves change.

### Link 7: a black hole evaporating back through the forces, from rung 6 to rungs 3, 2, 1 (`src/ladder_links.py` L7)

Design A's diamond can't be the black hole: at 1.5×10⁻¹⁴ kg it is a millionth of the Planck
mass, below any semiclassical hole. An evaporating hole is the way back down the ladder: it
heats as it shrinks, T_H = ħc³/(8πGMk_B), and emits every species lighter than T_H.

| | Result | Status |
|---|---|---|
| L7a | Mass loss dM/dt = −5.34×10²⁵ f(M)/M² g³/s, f a weighted count of emitted degrees of freedom: 0.267 (spin 0), 0.147 and 0.142 (neutral and charged spin ½), 0.060 (spin 1), 0.007 (spin 2) (Carr, Kohri, Sendouda and Yokoyama, Rept. Prog. Phys. 84, 116902 (2021)). T_H at 10¹⁰ g is 1.057 TeV, their 1.06 | CHECK; LIT |
| L7b | **Rung 1's particle content sets f.** Massless species only: f = 1.016. All Standard Model species: **f = 15.33**, against their 15.35, and only if the W and Z longitudinal modes, the Goldstones the Higgs mechanism gives them, count as scalars; unbroken counting gives 15.33 too. Above the 3-3-1 scale, from `src/m331_exact.py`'s field content (17 gauge bosons, 18 real scalars, 66 or 69 Weyl fermions): f = 25.7 (β = −1/√3) or 26.5 (β = +1/√3) | CHECK |
| L7c | The thresholds a shrinking hole crosses, coldest first (each species switches on at T_H = m/4; quarks and gluons replace pions at the QCD crossover, 156.5 MeV, HotQCD 2019): the diamond experiment's 0.15 K (8.2×10²³ kg); the CMB (2.72548 K, Fixsen 2009; 4.5×10²² kg); electrons (8×10¹³ kg); pions, rung 2's Goldstones (3×10¹¹ kg); **the QCD crossover, where rung 2's condensate melts** (6.8×10¹⁰ kg, 7 million years left); W and Z (5×10⁸ kg); **the electroweak crossover, 159.5 GeV (D'Onofrio and Rummukainen 2016), where rung 1's breaking undoes** (6.6×10⁷ kg, 33 hours left); the 3-3-1 content (1.1×10⁷ kg, 5.6 minutes left); and the Planck mass, link 3's cutoff, where semiclassics ends | CHECK, given the model |
| L7d | Checks: 10¹⁰ g lives 406.7 s at f = 15.35 (theirs 407 s); the hole that lives the age of the universe (13.787 Gyr, Planck 2018) is **5.11×10¹⁴ g at T_H = 20.7 MeV**, theirs 5.1×10¹⁴ g at 21 MeV | CHECK |

The switch-on rule is a model; real emission turns on smoothly over a factor of a few in T_H.
That the radiated species change at the crossovers doesn't mean the vacuum around the hole is
restored there; Hawking radiation is not a bath in equilibrium.

## How the rungs fit together

| Energy | What breaks | What is left below |
|---|---|---|
| w ≳ 4 TeV | SU(3)_L × U(1)_X → SU(2)_L × U(1)_Y (rung 1) | the Standard Model |
| v = 246 GeV | SU(2)_L × U(1)_Y → U(1)_em (rung 1) | the photon, massive W and Z |
| ~1 GeV | chiral SU(2)_L × SU(2)_R → SU(2)_V (rung 2); colour stays unbroken and confines | pions, nucleons, the nuclear force |
| below | nothing: U(1)_em stays unbroken (rung 3) | two long-range forces, electromagnetism and gravity |
| every scale | gravity, with G as its own input (rungs 4–5) | the signal in the diamond experiment |
| strong field | nothing breaks: gravity's column at horizons (rung 6) | black holes, tested by the EHT and LIGO |

The two chains meet in the apparatus. Gravity is the signal: the entangling phase,
2.19 rad. Electromagnetism, the last unbroken force of the gauge chain, is the background
the design must suppress: the Casimir–Polder force, which sets the 181 µm gap. Electric
charge is the other way it would enter, and rung 1's anomalies keep it out: they make
matter neutral (link 1). Within the gauge chain, rung 1's charges and rung 2's pion meet in
π⁰ → γγ (link 2). And gravity's G, beside the chain, sets the scale the chain's 3-3-1
selection is run to (link 3). At the far end of gravity's column, black holes use the same
geometry as rung 5: its Λ caps their size, its spin connection gives their temperature,
and a Planck-mass one sits at link 3's cutoff (link 5). The diamond is the opposite
extreme: its Schwarzschild radius is a millionth of the Planck length (link 4).

## Reproduce

**In one paste:** [`src/ladder_standalone.py`](src/ladder_standalone.py) reproduces all six
rungs and all five links with only the Python standard library (58 PASS/FAIL checks; expected output
[results/ladder/standalone.txt](results/ladder/standalone.txt)). Each check is tagged math
(41: identities verified by computation), data (9: against measurements, each printing its
tolerance and why) or pinned (8: this repository's own derived numbers); checks inside the
linear sigma model are also tagged model. It exits with status 1 if any check fails. The website has a
**Copy Python script** button for it.

```bash
python3 src/ladder_standalone.py   # everything below, one file, ~1 s
python3 src/m331_breaking.py       # rung 1, ~7 s
python3 src/m331_rho_bound.py      # rung 1 against the global fit's rho_0 and the LHC, ~7 s
python3 src/m331_zpole.py          # rung 1 against the LEP/SLD Z pole, validated on E6 Z', ~30 s
python3 src/chiral_breaking.py     # rung 2, ~1 s
python3 src/casimir_diamonds.py    # rung 3, ~15 s
python3 src/graviton_exchange.py   # rung 4, ~1 s
python3 src/macdowell_mansouri.py  # rung 5, ~3 s
python3 src/black_holes.py         # rung 6 and links 4-5, ~3 s
python3 src/ladder_links.py        # links 1-3: neutral matter, pi0 -> gamma gamma, M_Pl, ~2 s
python -m pytest tests/test_331_breaking.py tests/test_ladder.py tests/test_ladder_links.py tests/test_black_holes.py -q
```

## References

- F. Pisano and V. Pleitez, PRD 46 (1992) 410; P. H. Frampton, PRL 69 (1992) 2889 (3-3-1).
- M. Gell-Mann and M. Lévy, Nuovo Cim. 16 (1960) 705 (linear sigma model);
  M. Gell-Mann, R. J. Oakes and B. Renner, Phys. Rev. 175 (1968) 2195 (GMOR).
- H. B. G. Casimir and D. Polder, Phys. Rev. 73 (1948) 360.
- S. L. Adler, Phys. Rev. 177 (1969) 2426; J. S. Bell and R. Jackiw, Nuovo Cim. A 60 (1969) 47
  (the chiral anomaly).
- I. Larin et al. (PrimEx-II), Science 368 (2020) 506 (π⁰ → γγ).
- G. Bressi et al., PRA 83 (2011) 052101; J. Baumann et al., PRD 37 (1988) 3107 (neutrality
  of matter).
- C. Q. Geng and R. E. Marshak, PRD 39 (1989) 693; K. S. Babu and R. N. Mohapatra, PRL 63
  (1989) 938; C. A. de S. Pires and O. P. Ravinez, PRD 58 (1998) 035008 (charge
  quantization from anomalies).
- S. W. MacDowell and F. Mansouri, PRL 38 (1977) 739; K. S. Stelle and P. C. West, PRD 21
  (1980) 1466.
- S. W. Hawking, Commun. Math. Phys. 43 (1975) 199 (black-hole radiation); J. M. Bardeen,
  B. Carter and S. W. Hawking, Commun. Math. Phys. 31 (1973) 161 (the four laws);
  G. W. Gibbons and S. W. Hawking, PRD 15 (1977) 2738 (the de Sitter horizon's temperature)
  and 2752 (Euclidean periodicity); H. Nariai, Sci. Rep. Tohoku Univ. 35 (1951) 62.
- E. Berti, V. Cardoso and C. M. Will, PRD 73 (2006) 064030 (quasinormal-mode fits).
- Event Horizon Telescope Collaboration, ApJL 875 (2019) L1 (M87*); ApJL 930 (2022) L12
  (Sgr A*). K. Gebhardt et al., ApJ 729 (2011) 119; J. L. Walsh et al., ApJ 770 (2013) 86
  (M87* masses). GRAVITY Collaboration, A&A 657 (2022) L12; T. Do et al., Science 365 (2019)
  664 (Sgr A* mass and distance).
- LIGO, Virgo and KAGRA Collaborations, "GW250114: testing Hawking's area law and the Kerr
  nature of black holes", PRL 135 (2025) 111403, arXiv:2509.08054.
- Inputs: PDG 2024 (couplings, masses, G_F, f_π, g_A); FLAG 2024 (condensate);
  Planck 2018 (Λ); CODATA (G).
