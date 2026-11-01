# Unification search, step 2: where the confinement area sits

Reproduce: `python3 src/stur_confinement.py` (about 60 s). The full output is in
`results/confinement/output.txt`, and `tests/test_confinement.py` pins the
numbers on a small chain.

Labels:
- **KNOWN:** published and tested;
- **FOLLOWS:** derived with no new assumption;
- **CHECK:** reproduces a known exact result.

## The question

UNIFICATION.md found one equation, the first law δS = δ⟨K⟩, that covers
decoherence, thermodynamics and horizons. The QCD area law was missing.

**A correction first.** The Bisognano–Wichmann theorem holds for the vacuum of
*any* relativistic quantum field theory, QCD included. So for a half-space, the
modular Hamiltonian K is already 2π × boost.

The real question is therefore narrower: when a confining flux tube crosses the
entangling surface, does its tension σ enter the **entropy S**, or only the
**modular energy ⟨K⟩**?

## The answer, from the replica trick (FOLLOWS)

Rotate by 2πn around the entangling surface. This is the replica trick; 2π is
the horizon holonomy from P4, and n = 1 is the physical state. Then:
- **The horizon** contributes (1 − n)·A_H/4Għ (KNOWN; checked in P4).
- **A static quark at distance ℓ** traces a circle on each of the n sheets, so
  its string sweeps an area n·πℓ². The area law then contributes −n·σ·πℓ².

Together:

```
ln Z_n  =  (1 − n) · A_H / (4Għ)   −   n · σ · A_swept   + …,     A_swept = πℓ²

S       =  (1 − n ∂_n) ln Z_n |_{n=1}     =  A_H / 4Għ          (string drops out)
Δ⟨K⟩    =  2π ∫₀^ℓ x σ dx                 =  σ · A_swept        (Bisognano–Wichmann)
D(string‖vacuum) = Δ⟨K⟩ − ΔS              =  σ · A_swept − ΔS_puncture
```

**Both areas appear in one generating function, playing opposite roles:**
- the **horizon area** multiplies the holonomy *deficit* (1 − n), so it is an entropy;
- the **confinement area** multiplies the holonomy *n* itself, so it drops out of
  every entropy (S and all Rényi entropies; checked numerically, C2) and shows up
  only as modular energy.

This is the precise version of P4's "linked vs spanned". The horizon is the fixed
set of the rotation; the string's area is what the rotation sweeps.

Also, Δ⟨K⟩ = σπℓ² is the area-law part of −ln⟨W⟩ for a circular Wilson loop of
radius ℓ. **The QCD area law is the modular energy of the flux tube.**

The closest published work is Lewkowycz–Maldacena (2013), on entanglement
entropy with a Wilson line in conformal field theories. I haven't checked whether
this exact statement for confining strings is in the literature.

## The lattice test (lattice Schwinger model, exact diagonalization)

**Setup:** QED in 1+1D, which confines. Static charges ±q = ±½, chains of N = 12–20
sites. Region A is the left half of the chain. The string ends one site past the
cut, and its other end sits ℓ sites inside A.
- K is computed exactly as −ln ρ_A^vac, using an SVD. This resolves Schmidt modes
  up to K ≈ 69; the fraction of the string state's weight outside them is at most
  2×10⁻⁴, except 4×10⁻³ at N = 20, ℓ = 8.

**Confinement:** the string energy is linear in length, with σ = 0.2296 per site
(screened below the bare q² = 0.25).

N = 20, x = 1, m/g = 0.5 (x = 1/(ga)², where a is the lattice spacing):

| ℓ | ΔS | Δ⟨K⟩ (exact) | D = Δ⟨K⟩ − ΔS | Bisognano–Wichmann estimate | Δ⟨K⟩/estimate |
|---|---|---|---|---|---|
| 1 | +0.1127 | 0.1294 | 0.0167 | 0.1086 | 1.191 |
| 2 | +0.1242 | 0.1751 | 0.0508 | 0.1547 | 1.132 |
| 3 | +0.1311 | 0.3576 | 0.2265 | 0.3514 | 1.018 |
| 4 | +0.1320 | 0.4766 | 0.3446 | 0.4798 | 0.993 |
| 5 | +0.1327 | 0.8456 | 0.7128 | 0.8840 | 0.956 |
| 6 | +0.1328 | 1.0441 | 0.9113 | 1.1095 | 0.941 |
| 8 | +0.1330 | 1.6467 | 1.5137 | 2.0556 | 0.801 |

**Three results**, which hold in all four parameter sets:
1. **ΔS saturates.** For ℓ ≥ 3 it varies by at most 0.007, while Δ⟨K⟩ grows 3–10×.
   The string adds a fixed "puncture" entropy where it crosses the cut: 0.133
   (x = 1), 0.085 (x = 4), 0.050 (m/g = 1). **This confirms the replica
   prediction that string length does not enter S.**
2. **Δ⟨K⟩ grows as ℓ²,** as the swept-area term predicts. The fitted ℓ²
   coefficient against the Bisognano–Wichmann value (π/v)·ε_dyn:

   | Run | Fitted | BW value | Difference |
   |---|---|---|---|
   | N = 16, x = 1 | 0.0266 | 0.0266 | exact |
   | x = 4 | 0.0086 | 0.0076 | 13% |
   | m/g = 1 | 0.0063 | 0.0053 | 19% |
   | N = 20 | 0.0194 | 0.0269 | 28% |

   The N = 20 fit includes ℓ = 7–8, where the region is too small and the leak is
   largest. Point by point, the ratio is 0.94–1.19 for ℓ ≤ 6 and x ≤ 4. **CHECK:**
   Bisognano–Wichmann holds on the lattice.
3. **A limit of 1+1D.** Here K sees only the *dynamical* part of the string
   energy: the screening by virtual pairs, ε_dyn = 0.017 per link (q² − σ =
   0.020). That is 7.5% of σ, and 1.4% for heavy fermions (m/g = 1). The bare q²
   per link is just a number with no operator behind it, because in 1+1D the
   electric flux has no degrees of freedom of its own.
   
   In 2+1D and 3+1D, the flux tube's energy is field energy and sits inside T₀₀.
   Bisognano–Wichmann then puts the **full σ** into Δ⟨K⟩. That FOLLOWS from the
   theorem but is not tested here. Testing it needs a gauge theory in 2+1D or
   more, such as Z₂ lattice gauge theory.

## Where the unification search stands

**The candidate unifying equation:** the replica generating function, with one
holonomy 2πn around the entangling surface.

```
ln Z_n = (1 − n)·A_H/4Għ − n·σ(μ)·A_swept + (thermal and record terms)
```

| Sector | How it enters | Evidence |
|---|---|---|
| Horizon entropy | (1 − n)·A/4G, so it is in S | P4, exact |
| Running σ for horizons | 1/4G(μ) = 1/4G₀ + 0.0242·N_species·μ² | U3 (Srednicki), KNOWN |
| Confinement | −n·σ·A_swept, so it is in ⟨K⟩, not S | replica (FOLLOWS); lattice C1 |
| Thermodynamics and decoherence | K = H/k_BT, with D = βQ − ΔS | ASSUMPTIONS §3, exact |
| Visibility and Wilson loops | V = ⟨(−1)^ΔN⟩ | U2, exact |
| Gravity | δS = δ⟨K⟩ on all local horizons, giving Einstein's equations | KNOWN (Jacobson; Faulkner et al.) |

**Compared with STUR's original line ½Φ_R² = σ(μ)A:**
- The holonomy enters *linearly* (as n), not as ½Φ².
- The two areas carry *different* factors, n and (1 − n), so they cannot share
  one σ(μ). σ_QCD is an energy per area that shows up in ⟨K⟩; 1/4G is an entropy
  per area that shows up in S.

That is why the 10³⁸ ratio found earlier was never a single running constant: it
compares an energy density to an entropy density.

**Honest status:**
- This equation unifies the sectors by putting them in **one generating
  function**.
- Every ingredient is known physics: the replica trick, Bisognano–Wichmann, the
  area law, and Gibbons–Hawking.
- The combined statement, and the lattice test, are new to this project. Nothing
  here yet predicts something that differs from standard physics.
- **The next decisive test** is the full σ appearing in Δ⟨K⟩ in 2+1D (Z₂ lattice
  gauge theory). If it doesn't, the confinement row fails.
