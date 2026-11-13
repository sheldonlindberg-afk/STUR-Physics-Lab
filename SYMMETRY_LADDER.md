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
broken gauge theory too, in an equivalent reformulation of GR.

## What is an input and what is derived

**Inputs, all measured:**
- the gauge couplings at one scale;
- the Fermi constant G_F, which gives v = (√2 G_F)^(−1/2) = 246.22 GeV;
- the light-quark masses, f_π, g_A and the nucleon mass;
- the quark condensate (lattice QCD, FLAG);
- the permittivity of diamond;
- G and the cosmological constant Λ;
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
- **The Z-pole couplings** (the leading omission). The mixing also shifts the Z's couplings
  to fermions, at the same order (v/w)². A fit to the Z-pole observables could tighten the
  bound on w by an O(1) factor; whether it reaches the LHC's isn't computed.
- **One-loop T from the bilepton gauge bosons:** about (g²/16π²)(M_W²/M_V²), a loop factor
  below the tree term. The exotic fermions are SU(2) singlets and contribute little.
- **One-loop T from the scalars:** not loop-suppressed in the same way. The second Higgs
  doublet's splittings come from the quartics, so its contribution goes as λ²/16π². With
  heavy scalars near the 0.1 TeV floor of NOTE_331.md §3e it isn't suppressed by v/w at
  all, and ρ then constrains the scalar spectrum, not w. Its sign is free, so it can lift
  R3's cancellation at a = a₀ or offset R4's tree term.
- **S and U** aren't used.

So R3 and R4 hold for the tree-level mixing with heavy, weakly coupled scalars.

## Rung 2: the strong force (`src/chiral_breaking.py`)

**What breaks.** Colour stays unbroken. What breaks is the approximate chiral symmetry of
the light quarks, SU(2)_L × SU(2)_R → SU(2)_V, through the quark condensate ⟨q̄q⟩. The
pions are its near-Goldstone bosons, and their exchange is the long-range nuclear force.
The derivation uses the linear sigma model (Gell-Mann and Lévy 1960), the minimal model
with this breaking pattern. It is a **MODEL** of QCD's low-energy structure, not QCD
itself.

| | Result | Status |
|---|---|---|
| S1 | With massless quarks: exactly **3 zero modes**, dim O(4) − dim O(3) = 6 − 3: the pions | MODEL; CHECK |
| S2 | With quark masses: m_π² = H/⟨σ⟩ and f_π = ⟨σ⟩, so **m_π² f_π² = (m_u + m_d)\|⟨q̄q⟩\|** (Gell-Mann–Oakes–Renner) | MODEL; CHECK |
| S3 | With measured m_u + m_d, f_π and the lattice condensate: m_π = **127.6 MeV**, against 135.0. The −5.5% is the higher-order chiral terms, not derived here | CHECK; LIT inputs |
| S4 | Exchanging a particle of mass m gives V(q) ∝ 1/(q² + m²), whose Fourier transform is **e^(−mr)/(4πr)** (derived symbolically). The range is 1/m_π = **1.414 fm**. The spin structure (σ₁·q)(σ₂·q) = (q²/3)[σ₁·σ₂ + S₁₂] gives the central and **tensor** nuclear forces | CHECK |
| S5 | Goldberger–Treiman: g_πNN = g_A M_N/f_π = **13.01**, against about 13.1 empirically (−0.7%, the known discrepancy; the empirical value is quoted approximately) | CHECK |

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

## Links between the rungs (`src/ladder_links.py`)

The rungs above are separate derivations. In three places one rung's output is another
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
| L2c | With rung 2's f_π = 92.07 MeV and α(0): **Γ = 7.785 eV**, against the PrimEx-I+II average 7.802 ± 0.117 eV (Larin et al., Science 368, 506 (2020)), −0.1σ | CHECK; LIT |
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
| L3b | M_Pl scales as G^(−1/2). If G were x times its measured value, the selection would hold for (M_Pl/pole₃)² < x < (M_Pl/pole₅)². At the reference spectrum (M_V = 4 TeV, Yukawas and thresholds on, α = 1, three loops; NOTE_331.md §3d) that is **0.12 < x < 5×10¹⁴ for β = +1/√3** and 3×10⁻²¹ < x < 1×10⁸ for β = −1/√3. G is measured to 2.2×10⁻⁵ (CODATA 2018). The narrow side: with G 8.4× weaker, M_Pl would rise above N_c = 3's pole and exclude it | CHECK |
| L3c | At the mass floors with light heavy leptons (NOTE_331.md §3e), N_c = 3's pole is 0.61 M_Pl, so it fails at the measured G; it would pass only if G were 2.7× stronger. This restates the heavy-lepton condition in terms of G; it adds nothing to it | CHECK |
| L3d | The check uses G, measured at laboratory and solar-system distances, at 10¹⁹ GeV. That assumes gravity's strength doesn't run in between. In perturbative quantum gravity the corrections are of order (E/M_Pl)². Many hidden light species would lower the effective cutoff, which this doesn't cover. Above M_Pl, an asymptotically safe gravity term leaves the selection unchanged ([NOTE_331.md](NOTE_331.md) §3g) | FOLLOWS |

So the selection's cutoff and the diamonds' signal rest on one measured number. The
selection is insensitive to it, by about an order of magnitude in G on its narrow side.

**Finding more links.** [DEPENDENCIES.md](DEPENDENCIES.md) maps which script feeds which and
where each physical constant is typed. It lists the quantities that more than one part of the
repository uses without importing them from one place; those are the candidates for the next
link.

## How the rungs fit together

| Energy | What breaks | What is left below |
|---|---|---|
| w ≳ 4 TeV | SU(3)_L × U(1)_X → SU(2)_L × U(1)_Y (rung 1) | the Standard Model |
| v = 246 GeV | SU(2)_L × U(1)_Y → U(1)_em (rung 1) | the photon, massive W and Z |
| ~1 GeV | chiral SU(2)_L × SU(2)_R → SU(2)_V (rung 2); colour stays unbroken and confines | pions, nucleons, the nuclear force |
| below | nothing: U(1)_em stays unbroken (rung 3) | two long-range forces, electromagnetism and gravity |
| every scale | gravity, with G as its own input (rungs 4–5) | the signal in the diamond experiment |

The two chains meet in the apparatus. Gravity is the signal: the entangling phase,
2.19 rad. Electromagnetism, the last unbroken force of the gauge chain, is the background
the design must suppress: the Casimir–Polder force, which sets the 181 µm gap. Electric
charge is the other way it would enter, and rung 1's anomalies keep it out: they make
matter neutral (link 1). Within the gauge chain, rung 1's charges and rung 2's pion meet in
π⁰ → γγ (link 2). And gravity's G, beside the chain, sets the scale the chain's 3-3-1
selection is run to (link 3).

## Reproduce

**In one paste:** [`src/ladder_standalone.py`](src/ladder_standalone.py) reproduces all five
rungs and all three links with only the Python standard library (44 PASS/FAIL checks; expected output
[results/ladder/standalone.txt](results/ladder/standalone.txt)). Each check is tagged math
(34: identities verified by computation), data (5: against measurements, each printing its
tolerance and why) or pinned (5: this repository's own derived numbers); checks inside the
linear sigma model are also tagged model. It exits with status 1 if any check fails. The website has a
**Copy Python script** button for it.

```bash
python3 src/ladder_standalone.py   # everything below, one file, ~1 s
python3 src/m331_breaking.py       # rung 1, ~7 s
python3 src/m331_rho_bound.py      # rung 1 against the global fit's rho_0 and the LHC, ~7 s
python3 src/chiral_breaking.py     # rung 2, ~1 s
python3 src/casimir_diamonds.py    # rung 3, ~2 s
python3 src/graviton_exchange.py   # rung 4, ~1 s
python3 src/macdowell_mansouri.py  # rung 5, ~3 s
python3 src/ladder_links.py        # links 1-3: neutral matter, pi0 -> gamma gamma, M_Pl, ~2 s
python -m pytest tests/test_331_breaking.py tests/test_ladder.py tests/test_ladder_links.py -q
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
- Inputs: PDG 2024 (couplings, masses, G_F, f_π, g_A); FLAG 2024 (condensate);
  Planck 2018 (Λ); CODATA (G).
