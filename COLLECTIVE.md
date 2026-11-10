# Why gravity's field follows each branch

Reproduce: `python3 src/stur_thermo_gravity.py` (about 6 s). The full output is in
`results/thermo_gravity/output.txt`, and `tests/test_thermo_gravity.py` pins it.

Gravity's strength comes from vacuum entanglement (D1–D3 in
[DERIVATION.md](DERIVATION.md)). Jacobson's step obtains Einstein's equation as an
*equation of state*. That leaves a question: is gravity's field an equation of state
in the literal sense, a classical average of the quantum level like temperature? Or
is it a collective field that, like sound in a crystal, follows each branch of a
superposition? This page answers it from the theory's own ingredients. The answer is
the second, and it fixes what the diamond experiments will see.

## 1. A statistical gravity must jitter, and the least jitter is fixed by G

A classical field that responds to quantum matter has to learn where the matter is.
Learning where matter is decoheres it, and a field built from that information
inherits its noise. The two effects trade against each other (Tilloy & Diósi 2016).

- Suppose the mass density m(x) is monitored with strength k(q) at wavenumber q.
- The record then has noise 1/4k. The potential built from it, Φ = −G∫m/r, carries
  noise S_Φ = G²K²/4k, with K = 4π/q².
- That noisy potential acts back on the matter and dephases it as well.

The total decoherence kernel is

```
k(q) + G²K² / (4ħ²k(q))   ≥   GK/ħ   =   4πG / (ħ q²)
```

The bound holds at every wavenumber. It is reached at one monitoring strength, and the
script confirms the minimum to 2×10⁻¹⁶ from q = 10² to 10¹⁴ m⁻¹. **The floor is the
Diósi–Penrose kernel.** Every Markovian statistical gravity decoheres matter at least
this fast. Such a model has only one freedom left, the length R₀ over which the mass
density that sources the field is smeared:

```
k_min(q) = (4πG / ħq²) · exp(−q²R₀²)
```

For the design-A diamond (1.5×10⁻¹⁴ kg, radius 1.007 µm, split 721 µm) with R₀ → 0,
the rate is (Gm²/ħ)(6/5R − 1/d) = **169.5 /s**.

## 2. The theory's own smearing length is the entanglement cutoff

An equation of state is defined above the scale at which its microscopic degrees of
freedom are counted. In D1–D3 that scale is the area-law cutoff a, the spacing at which
the vacuum's entanglement stops being counted. The measured G sets it:

| Number of quantum fields | a |
|---|---|
| 1 | 0.31 ℓ_P |
| 10 | 0.98 ℓ_P |
| 100 | 3.11 ℓ_P |
| 1000 | 9.85 ℓ_P |

The theory contains no other length. A statistical gravity built from it therefore has
R₀ = a.

## 3. That noise would heat every piece of matter

The same kernel kicks every nucleus. Summed over the nuclei in a kilogram of any
material, the heating is independent of composition:

```
P / mass = ħG / (4√π R₀³)
```

| R₀ | Heating |
|---|---|
| a, one field | **7.8×10⁶⁰ W/kg** |
| a, 1000 fields | 2.5×10⁵⁶ W/kg |
| 0.54 Å | 6.3×10⁻¹⁵ W/kg |

For scale, the Sun produces 1.9×10⁻⁴ W/kg. With R₀ = a, ordinary matter could not exist.
Searches for the X-rays such heating would produce require R₀ ≥ 0.54 Å (Donadi et al.
2021), which is 3.4×10²³ cutoff lengths.

**So gravity is not an equation of state in the statistical sense.** Its field follows
each branch of the matter that sources it (λ = 1). This is step D6 of the derivation,
and it now follows from D1–D3 instead of being added to them. Jacobson's equation of
state still holds, but for the collective field, as the equations of hydrodynamics
hold for sound.

## 4. What one diamond will show

A statistical gravity could survive only with an R₀ put in by hand, at least 10²³ times
the theory's own scale. Even then it is pinned down. The decoherence of the design-A
diamond over its 3.24 s sequence:

| R₀ | Rate | Coherence left after 3.24 s |
|---|---|---|
| 0.54 Å | 169.5 /s | 3×10⁻²³⁹ |
| 0.1 µm | 165.8 /s | 5×10⁻²³⁴ |
| 1 µm | 72.9 /s | 2×10⁻¹⁰³ |
| 10 µm | 7.83 /s | 1×10⁻¹¹ |
| 52 µm | 1.35 /s | 1.3% |
| 200 µm | 0.206 /s | 51% |
| 1 mm | 0.0033 /s | 99% |
| **collective gravity** | **0** | **100%** |

For R₀ ≫ R the numerical rates agree with the closed form for Gaussian-smeared points,
(Gm²/ħ)[1/(√π R₀) − erf(d/2R₀)/d], to 10⁻³.

- To keep 90% coherence, a statistical gravity needs **R₀ > 455 µm**.
- Smearing the source of gravity over R₀ softens Newton's law at separations comparable
  to R₀. The inverse-square law has been verified down to 52 µm (Lee et al. 2020).
- So a design-A diamond that stays coherent for 3.24 s leaves no Markovian statistical
  gravity standing. The two-diamond experiment then measures the entangling phase
  itself, Δφ = 2.19 rad ([GRAVITY_ENTANGLEMENT.md](GRAVITY_ENTANGLEMENT.md)).

## Scope

The argument covers classical fields coupled to quantum matter by Markovian (memoryless)
dynamics. This is the class in which consistent models of classical gravity have been
built, Diósi–Penrose and Tilloy–Diósi among them. The decoherence convention follows
the rest of this repository: the rate for a split much larger than the body is
(6/5)Gm²/ħR, and other conventions differ by a factor of 2, which leaves every
conclusion above unchanged.
