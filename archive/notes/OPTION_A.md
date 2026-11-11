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

---

# Update: confronted with stronger bounds. **Option A is excluded as a distinctive prediction.**

Reproduce: `python3 src/stur_option_a_bounds.py` (about 50 s). The output is in
`results/option_a/bounds_output.txt`.

## New physics input (FOLLOWS from the model)

The potential's variogram grows linearly with distance. So the **acceleration**
noise is correlated over long distances: H_ij(r) = κ(δ_ij/s − r_i r_j/s³), with
s = √(r² + ξ²). Two free-falling test masses therefore feel almost independent
noise along the line joining them.

## Bounds

The pulse spacing T and the LISA Pathfinder separation are scanned rather than
fixed, because this session's network blocked the sources (arxiv.org and
spiral.imperial.ac.uk would have to be allowed).

| Bound | Input | Status |
|---|---|---|
| Kovachy 2015 | 28% contrast observed (LIT), so Γ ≤ −ln 0.28 = 1.27; T scanned over 0.9–1.1 s | superseded |
| **LISA Pathfinder** | differential acceleration noise 1.74 fm s⁻²/√Hz (LIT, Armano et al. 2018); 46 mm cubes; separation scanned over 0.30–0.45 m | **binding for ξ ≲ 3 m: κ ≤ 2.8×10⁻³²** |
| **Ground-based GW detector** | 3995 m arms, strain ~10⁻²³/√Hz at 100 Hz. **ESTIMATE, not retrieved** | **binding for 10 m ≲ ξ ≤ R_E** |
| Earth's heat flow | 7.9×10⁻¹² W/kg | never binding |
| X-ray emission (Donadi et al. 2021) | — | not applicable for ξ ≫ atomic size: a neutral atom pushed uniformly emits no dipole radiation |

My earlier version required Γ ≤ 1 against Kovachy. That was slightly stricter
than the data justify; Γ ≤ 1.27 is the honest criterion.

## Best-case signal (Sr-87, illustrative geometries)

| ξ range | Largest Γ for 3 m × 4 s | Largest Γ for 10 m × 10 s |
|---|---|---|
| ≤ 3 m (LISA Pathfinder binding) | 7×10⁻¹⁰ | 1.3×10⁻⁸ |
| 10 m – 10 km (GW detector binding) | 7×10⁻⁹ | 2×10⁻⁷ |
| ≈ R_Earth (edge of the formula's validity) | 2.4×10⁻³ | 6.6×10⁻² |

The two unretrieved inputs don't matter: across LISA Pathfinder separations of
0.30–0.45 m and Kovachy T of 0.9–1.1 s, the best case stays at 2.37×10⁻³. The
ground-based-detector estimate does matter, quadratically. Multiplying its
acceleration sensitivity by 0.1, 1, 10 or 100 gives a best Γ of 2×10⁻⁵, 2×10⁻³,
0.24 or 24.

## Verdict

- **For ξ ≲ 10 km, option A is excluded as a MAGIS/AION target.** The best-case
  signal is Γ ≤ 10⁻⁸ or less, 8–13 orders of magnitude below what the Kovachy bound
  alone allowed. Free-falling test masses (LISA Pathfinder, GW detectors) measure
  the same acceleration noise far better than an atom interferometer's contrast.
- **The surviving corner, ξ ≈ Earth's radius, is not credible as a STUR
  prediction:**
  1. Its size rests on an *estimated* ground-based detector sensitivity, squared.
  2. At Earth-scale ξ the apparatus partly co-moves with the noise. By the
     equivalence principle only the tidal part is observable, so the formula
     overestimates there.
  3. Bounds relevant at that scale were not included: superconducting gravimeters,
     satellite gravimetry and lunar laser ranging.
  4. **The distinctive signature is gone.** For ξ ≫ Δx, Γ ∝ κ∫Δx²dt/ξ: quadratic
     in separation, not linear in enclosed area. That's ordinary stochastic
     gravity-gradient noise, with nothing specific to STUR.

**Option A fails in the form that made it distinctive.** "Spacetime records
which-path information with an area law" is excluded by 8–13 orders of magnitude
wherever the area law operates. To re-enable the next steps, allow arxiv.org in
the session's network settings; the published LIGO acceleration spectrum and the
geophysical bounds would then close or confirm the Earth-scale corner.
