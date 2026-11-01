# Option A: spacetime records which-path information

Reproduce: `python3 src/stur_option_a.py`. The output is in
`results/option_a/output.txt`, and `tests/test_option_a.py` pins the numbers.

Labels:
- **KNOWN:** published and tested;
- **STUR POSTULATE:** a new claim;
- **FOLLOWS:** derived with no new assumption;
- **LIT:** a literature value used as input, not recomputed here.

## The model: minimal and built from STUR's own lines

**STUR POSTULATE (the only new structure).** The gravitational potential per unit
mass, Φ, carries Gaussian noise. That noise is white in time, and its spatial
variogram follows STUR's area law:

V(Δx) = 2κ(√(Δx² + ξ²) − ξ)

It grows linearly with separation, like a confining string, and is smoothed below
a scale ξ.

**FOLLOWS.** Visibility is then a Gaussian Wilson loop of the connection
A₀ = mΦ/ħ. That is STUR line 1 plus line 6, with A_μ fixed as the gravitational
potential:

**Γ = −ln(V/V₀) = (m/ħ)² · κ · A_st,  for Δx ≫ ξ**

A_st is the spacetime area enclosed by the two arms. Integrating over a real
separation profile reproduces the area law to within 4×10⁻⁶.

This answers open problem #2 *inside option A*, by postulate rather than by
derivation.

**FOLLOWS.** The same noise pushes on matter. The momentum spread grows at a rate
d⟨p²⟩/dt = m²κ/ξ along each axis, so all matter heats at 3κ/(2ξ) per kilogram.

## Constraints (computed; inputs LIT)

| Constraint | Input | Result |
|---|---|---|
| Interference was seen at 0.54 m separation (Kovachy et al., Nature 2015) | Rb-87; Δx = 0.54 m; T = 1.04 s; I required Γ ≤ 1, which is conservative | **κ ≤ 9.5×10⁻¹⁹ m³/s³** |
| Matter must not heat faster than Earth's internal heat flow | 47 TW over 5.97×10²⁴ kg = 7.9×10⁻¹² W/kg | at the largest allowed κ: **ξ > 0.18 µm** |

So a window is still open. The smoothing scale ξ is much larger than an atom, so
the noise acts coherently on each atom and Γ ∝ m² holds.

## Predicted signal at the largest allowed κ

The geometries below are **illustrative, not instrument specifications.**

| Geometry | Δx_max | T | A_st | Γ | Remaining contrast |
|---|---|---|---|---|---|
| Kovachy 2015 (sets the bound) | 0.54 m | 1.04 s | 0.56 m·s | 1.0 | 0.37 |
| MAGIS/AION-class, Sr-87 | 1 m | 2 s | 2 m·s | **3.6** | 0.028 |
| MAGIS/AION-class, Sr-87 | 3 m | 4 s | 12 m·s | **21** | 5×10⁻¹⁰ |
| km-scale, Sr-87 | 10 m | 10 s | 100 m·s | 178 | ≈ 0 |

**Reach.** Suppose an experiment measures contrast to a precision dV at an
enclosed area A. Then it bounds κ ≤ dV/((m/ħ)²A). For example, dV = 10⁻³ at
A = 12 m·s would push the bound down by a factor of **2×10⁴**, to 4.4×10⁻²³.

## Signatures that separate it from standard physics

1. **Γ is linear in the enclosed spacetime area.** Doubling Δx_max at fixed T
   doubles Γ. Gas collisions, blackbody scattering, CSL and Diósi–Penrose all
   *level off* once Δx exceeds their length scale.
2. **Γ ∝ m²** across atomic species at the same geometry. Taking Sr-87 as 1:
   Rb-87 1.000, Sr-88 1.023, Cs-133 2.337, **Yb-174 4.000**.
3. **Γ doesn't depend** on internal state, temperature or vacuum pressure, so
   standard backgrounds can be separated by varying those.
4. **A second, independent test:** all matter heats at 3κ/(2ξ) per kilogram.

## Hostile-referee caveats

- **κ is a free parameter, not a derived one.** I checked whether any natural
  scale lands in the window. None is derived:
  - c³ is excluded by 10⁴³;
  - c³·√(ℓ_P/R_H) is excluded by 10¹³;
  - c³·ℓ_P/R_H sits 10¹⁸ below today's bound, so it is untestable.
  
  Option A is therefore a *phenomenological* model, like every collapse model. It
  can be falsified only within its window, and the unification work doesn't fix
  κ. Linking κ to σ_QCD or 1/4G would need further structure.
- **ξ matters for the signal.** If ξ is larger than the arm separation, the area
  law turns into Γ ∝ κ∫Δx²dt/(2ξ), and the signal falls: at ξ = 10 m the 1 m case
  drops from 3.6 to 0.12. The heating bound used here (Earth's heat flow) is crude.
  Lab bounds were not computed and could force ξ upward:
  - LISA Pathfinder acceleration noise;
  - heating of cold atoms;
  - spontaneous X-ray emission, the Donadi et al. 2021 method.
  
  **Computing those is the next check.**
- **The Kovachy criterion is loose.** Γ ≤ 1 is weaker than the published
  contrast data allow; a proper fit would tighten κ.
- **Noise that is white in time picks out a preferred frame**, as collapse models
  do. That conflicts with Lorentz invariance, and it is a real theoretical cost.
- **Energy isn't conserved** (the heating), as in all collapse models.

## Status

Option A gives STUR its first prediction that differs from standard physics:
**visibility loss proportional to enclosed spacetime area × mass²**, with no
saturation. It is consistent with the two constraints checked here. MAGIS/AION-
class experiments could see it, or rule it out down to 4.4×10⁻²³ m³/s³, about
2×10⁴ below today's bound.

**Before treating this as a real candidate:**
1. Check it against the stronger lab heating bounds (LISA Pathfinder, cold atoms,
   X-ray emission).
2. Redo the Kovachy bound with the published contrast data.
