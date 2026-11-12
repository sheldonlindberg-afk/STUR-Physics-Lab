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
- G and the cosmological constant Λ.

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
the design must suppress: the Casimir–Polder force, which sets the 181 µm gap.

## Reproduce

```bash
python3 src/m331_breaking.py       # rung 1, ~7 s
python3 src/chiral_breaking.py     # rung 2, ~1 s
python3 src/casimir_diamonds.py    # rung 3, ~2 s
python3 src/graviton_exchange.py   # rung 4, ~1 s
python3 src/macdowell_mansouri.py  # rung 5, ~3 s
python -m pytest tests/test_331_breaking.py tests/test_ladder.py -q
```

## References

- F. Pisano and V. Pleitez, PRD 46 (1992) 410; P. H. Frampton, PRL 69 (1992) 2889 (3-3-1).
- M. Gell-Mann and M. Lévy, Nuovo Cim. 16 (1960) 705 (linear sigma model);
  M. Gell-Mann, R. J. Oakes and B. Renner, Phys. Rev. 175 (1968) 2195 (GMOR).
- H. B. G. Casimir and D. Polder, Phys. Rev. 73 (1948) 360.
- S. W. MacDowell and F. Mansouri, PRL 38 (1977) 739; K. S. Stelle and P. C. West, PRD 21
  (1980) 1466.
- Inputs: PDG 2024 (couplings, masses, G_F, f_π, g_A); FLAG 2024 (condensate);
  Planck 2018 (Λ); CODATA (G).
