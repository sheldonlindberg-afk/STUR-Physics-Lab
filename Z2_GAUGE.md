# Unification search, step 3: a dynamical flux tube in 2+1D (Z₂ lattice gauge theory)

Reproduce:
- `python3 src/stur_z2_gauge.py` (static charges, about 2 min)
- `python3 src/stur_z2_higgs.py` (heavy dynamical charges, about 2 min)

Outputs are in `results/z2_gauge/`, and `tests/test_z2.py` checks a small
ladder. Labels: KNOWN (published and tested), FOLLOWS (derived with no new
assumption), CHECK (reproduces a known exact result).

## The question

CONFINEMENT.md found that in 1+1D, the modular Hamiltonian K sees only the
screening part of the string energy (1.4–8.5% of σ). The rest is a pure number
there, because 1+1D flux has no degrees of freedom of its own.

The replica equation

**ln Zₙ = (1 − n)·A_H/4G − n·σ·A_swept**

predicts that when the flux is dynamical, the **full** string energy enters ⟨K⟩,
while the entropy S stays independent of string length.

**Model:** Z₂ gauge theory, H = −Σ B_p − h Σ X_l (KNOWN; Wegner, Kogut). The
flux is a quantum operator here, and the model confines for h > 0.33.

## Result 1: static charges are a superselection sector (FOLLOWS)

**Setup:** a strip of 6×3 plaquettes, solved exactly through its Ising dual. The
reduced density matrix uses the extended Hilbert space, which includes the
boundary flux.
- The string confines: σ = 1.73 per link at h = 1 (strong-coupling value 2h = 2).
- **ΔS saturates** with string length. The increments are +0.067, +0.025, +0.010
  at h = 1, and +0.115, +0.039, +0.014 at h = 0.5.
- **But once the charge sits at an interior vertex of A** (ℓ ≥ 2), the
  string state has **zero overlap** with the vacuum's support. The Gauss law
  at that vertex is a superselection label of ρ_A, so D(string‖vacuum) = ∞, and
  ⟨K⟩ can't be compared at all.

This is a real feature of gauge theory with infinitely heavy charges, not a
numerical problem. My 1+1D test avoided it only because the charges were
encoded as a background field.

## Result 2: heavy dynamical charges, the decisive test

**Model:** the Z₂ gauge-Higgs model in unitary gauge,
H = −ΣB_p − hΣX_l − JΣZ_l − ΣG_v·A_v (KNOWN; Fradkin–Shenker).
- Matter costs 2G = 4 per charge.
- Two sites are pinned to hold a quark (G_v = −6; occupancy ⟨n⟩ = 0.999).
- The flux between them is dynamical, and string and vacuum now share one
  Hilbert space.

**Geometry:** a ladder of 6 plaquettes, 2¹⁹ states. K = −ln ρ_vac, resolved by
SVD up to K ≈ 69.

| h | σ per link | ΔS increments (ℓ = 1→2→3→4) | Δ⟨K⟩ at ℓ = 2, 3 | ratio to Σ d·ΔE at ℓ = 2, 3 | string share of Σ d·ΔE |
|---|---|---|---|---|---|
| 0.8 | 1.406 | +0.066, +0.035, +0.020 | 15.09, 33.39 | 2.46, 2.64 | 19%, 29% |
| 1.0 | 1.850 | +0.041, +0.019, +0.009 | 15.18, 34.34 | 2.36, 2.51 | 23%, 35% |
| 1.2 | 2.277 | +0.024, +0.009, +0.004 | 15.35, 35.32 | 2.28, 2.40 | 26%, 39% |

Here Σ d·ΔE is the change in energy, weighted by distance from the cut, using the
vacuum's own energy operators. The weight carried beyond the resolved modes is
≤ 2×10⁻³ at ℓ = 2–3. Two points are unreliable:
- **ℓ = 1:** the quark sits on the boundary vertex.
- **ℓ = 4:** up to 20% of the weight is unresolved, so Δ⟨K⟩ is only a lower bound.

**Separate weights.** Split Σ d·ΔE into a quark part and a string part, and solve
ℓ = 2, 3 for their weights in Δ⟨K⟩. This is exactly determined from two points,
so there is no error bar.

| h | quark weight c_q | string weight c_s |
|---|---|---|
| 0.8 | 2.13 | **3.89** |
| 1.0 | 2.07 | **3.33** |
| 1.2 | 2.03 | **2.96** |

For comparison, the weight on the bare string in 1+1D was 0.

**What this shows:**
1. **The entropy saturates** with string length in 2+1D too. String length
   doesn't enter S, as the replica equation predicts.
2. **The full string energy enters the modular energy,** with a weight at least as
   large as the quark's. K is roughly distance-weighted energy, as
   Bisognano–Wichmann predicts: the ratio stays at 2.3–2.6 while the string's share
   of the energy doubles. If K ignored the string, the ratio would have fallen by
   that share.
3. **The two weights aren't equal.** c_s/c_q = 1.83, 1.61, 1.46. Exact
   Bisognano–Wichmann would give 1, but it needs a Lorentz-invariant continuum, and
   this is a strongly coupled lattice ladder. The gap narrows as h grows, but I
   haven't shown it closes.

## Caveats (hostile-referee view)

- **Geometry:** the ladder is quasi-1D (one plaquette wide). The flux is
  dynamical, but this isn't a 2D bulk.
- **Statistics:** only two string lengths (ℓ = 2, 3) are clean, so there is no
  error bar on c_q and c_s.
- **Tomography failed:** fitting the vacuum K directly as Σβ·(local terms) is
  ill-posed here. Only about 20 modes have K < 40, fewer than the roughly 37 fit
  parameters.
- **Not the continuum:** none of this is a continuum limit. A larger or more
  continuum-like test needs tensor-network methods (DMRG), not exact
  diagonalization.

## Where the unifying equation stands

The confinement row of the replica equation now has qualitative lattice support
in both 1+1D and 2+1D:
- the confinement area stays out of the entropy;
- it enters the modular energy, fully once the flux is dynamical.

The 1+1D result is now explained: the string energy that K could not see there
is the part with no operator behind it.

Still open:
1. Equal weights (c_s = c_q) in a continuum-like limit.
2. Any prediction that differs from standard physics. Nothing so far.
