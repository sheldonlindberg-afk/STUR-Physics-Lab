# Unification search, step 1: one equation across the surviving sectors

Reproduce: `python3 src/stur_unification.py` (about 30 s; needs numpy, scipy and
mpmath). The full output is in `results/unification/output.txt`, and
`tests/test_unification.py` pins the numbers.

Labels:
- **KNOWN:** published and tested;
- **FOLLOWS:** derived with no new assumption;
- **CHECK:** reproduces a known exact result.

## Starting point

The earlier tests (POSTULATE_TEST, ASSUMPTIONS, OPEN_PROBLEMS) left three
**exact** relations standing:
1. The energy given to a bath equals k_BT times the relative entropy
   D(record‖thermal) of the environment's record. Relative entropy measures how
   far a state is from a reference state.
2. Horizon entropy is set *linearly* by the 2π holonomy around the Euclidean
   horizon.
3. Visibility and abelian Wilson loops are expectation values of the same
   displacement operator.

The question was whether one equation contains all three.

## The candidate equation (all pieces KNOWN)

```
D(ρ‖σ) = Δ⟨K_σ⟩ − ΔS ≥ 0,     K_σ ≡ −ln σ                    (U1)
δS = δ⟨K_σ⟩  at first order   (first law of entanglement)    (U1′)
V  = ⟨(−1)^ΔN⟩                (visibility = parity of quanta exchanged)  (U2)
```

K_σ is the "modular Hamiltonian" of the reference state σ. **It is the only thing
that changes from sector to sector:**

| Sector | Reference state σ | Modular Hamiltonian K_σ | Status |
|---|---|---|---|
| Decoherence / thermodynamics | thermal bath | H/k_BT | (U1) gives E = k_BT·D exactly (ASSUMPTIONS §3) |
| Horizons and gravity | vacuum seen across a horizon | **2π × boost** (Bisognano–Wichmann theorem) | the 2π is the holonomy from OPEN_PROBLEMS P4 |
| Einstein's equations | the same, with S = A/4G on every local horizon | — | δS = δ⟨K⟩ gives the linearized Einstein equations. KNOWN (Jacobson 1995; Faulkner et al. 2014); not recomputed here |
| Wilson loops / interferometers | vacuum (free fields) | — | (U2), exact (§1) |
| **QCD confinement** | Yang–Mills vacuum around a flux tube | **unknown** | **the gap (§4)** |

## 1. Visibility = parity of quanta exchanged (FOLLOWS)

For linear coupling to bosons, and for **any** bath state that is diagonal in
the Fock (number) basis, not only thermal ones:

**V = ⟨(−1)^ΔN⟩**, where ΔN is the number of quanta exchanged, read off by
measuring the bath before and after.

Checked on six cases (thermal and random states): the largest difference is
**7.6×10⁻¹⁷**. The algebra behind it is D(α)†ΠD(α) = ΠD(2α), where D is the
displacement operator and Π is the photon-number parity.

For Gaussian noise this contains the earlier identity Γ = 2 Var(N_exch), so
visibility loss counts the quanta exchanged. An abelian Wilson loop is the same
object, ⟨0|D(α)|0⟩ (KNOWN). I haven't searched the literature for this exact
statement.

## 2. Horizon sector on a lattice (free-fermion chain)

**(a) The modular Hamiltonian is 2π × local boost** (Casini–Huerta–Myers /
Bisognano–Wichmann, KNOWN).
- **Prediction:** the slope is 2π/v_F = π, where v_F is the speed of the
  chain's excitations.
- **Result:** summing all lattice hoppings gives a slope of **3.14061, 3.14135
  and 3.14148** at the block centre for L = 20, 40, 60 (CHECK). Nearest-neighbour
  terms alone give 3.37; the hops of range 3, 5, … carry the rest.

**This is the same 2π as the Euclidean-horizon holonomy in P4.**

**(b) First law.** I rotated a filled wavepacket at the edge of the block into an
empty one, by an angle ε. Fitting both responses as aε + bε²:

| | dS | d⟨K⟩ | ratio |
|---|---|---|---|
| First-order slope | 0.39708 | 0.39745 | **0.99907** |

Their difference, the relative entropy D, is pure second order: D/ε² =
2.957–2.963 for ε from 0.2 down to 0.025, and it stays positive (CHECK). Since
D ≥ 0 is Casini's version of the Bekenstein bound, ΔS ≤ Δ⟨K⟩, this is the
correct, known version of STUR line 4.

**(c) Local Clausius law:**

dS = Σ_x dE(x)/T_loc(x),  with T_loc(x) = v_F / (2π β(x)).

Here T_loc is a local, Unruh-type temperature that varies across the region.
The Unruh-weighted local energy reproduces the exact d⟨K⟩ to a ratio of
**0.99969**.

**This is what STUR's E = TS was reaching for.** The correct law is local and
differential, and its temperature depends on position. It isn't one global T
multiplying a total entropy.

## 3. Area law and the running of σ for horizons (KNOWN; coefficient computed)

The entanglement entropy of a free scalar across a sphere (Srednicki's method)
gives S/(R/a)² = 0.3022 → 0.3036 for R/a = 10.5 → 26.5, where a is the lattice
cutoff. Extrapolated, **S = 0.3046 (R/a)² = 0.02424 A/a²** (LIT: Srednicki 0.30).

Getting A/4ℓ_P² this way needs either a cutoff a = 0.311 ℓ_P, or **10.3 scalar
fields** at a = ℓ_P. This dependence on the cutoff is the known renormalization
of Newton's constant (Susskind–Uglum 1994):

**1/(4G(μ)) = 1/(4G₀) + 0.0242 N_species μ²** for each scalar field.

**This is the known σ(μ) for the horizon sector.** It runs as μ² times the
number of fields, which agrees with the dimensional-analysis finding in P3. It
says nothing about QCD.

## 4. The gap: QCD confinement

Free and abelian fields fit (U2) and give a perimeter law. The confining area
law with σ_QCD is non-perturbative, and nobody knows K for a region pierced by
a flux tube.

**The target that would close the candidate equation:** show that the string
tension enters as boost-weighted energy, i.e. that dS_string = 2π Σ β(x)
dE_string(x) with E_string = σ_QCD × (length). Here β(x) is the local boost
weight from §2.
- If this holds, confinement and horizon entropy obey one equation with
  different K's.
- If it fails, the QCD sector really is separate.

**Computable toy (proposed next step):** a confining gauge theory small enough
for exact diagonalization:
- the 1+1D massive Schwinger model, whose static charges are confined with a
  known string tension; or
- 2+1D Z₂ lattice gauge theory.

## Where STUR's lines stand under this candidate

| STUR line | Replacement that is exact | Status |
|---|---|---|
| 1. Holonomy, V = exp(−½⟨Φ²⟩) | V = ⟨(−1)^ΔN⟩; Gaussian limit gives line 1 | kept, generalized |
| 2. S = −k_B ln V | ΔS = Δ⟨K⟩ − D | **replaced** |
| 3. E = ½k_BTΦ² | dS = Σ dE(x)/T_loc(x) | **replaced** (local, Unruh T) |
| 4. Φ² ≤ A/2ℓ_P² | ΔS ≤ Δ⟨K⟩ (Casini) | replaced by a known theorem |
| 5. Smarr check | — | dropped (circular) |
| 6. σ(μ) | horizon: 1/4G(μ) = 1/4G₀ + 0.0242 N μ²; QCD: open | half known, half open |

## Honest status

- **The equation above is not new.** Every line of (U1), and its gravitational
  consequence (Einstein's equations from δS = δ⟨K⟩), is published physics.
- **The parity identity (U2)** is the only piece derived here, and it is
  probably known in some form.
- **What a genuine STUR contribution would have to be:**
  1. closing the QCD gap in §4, so that the string tension appears inside the
     same first law; and
  2. a prediction from that which differs measurably from standard physics.
  
  Neither exists yet.
