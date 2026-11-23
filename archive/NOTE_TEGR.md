# The frame in teleparallel gravity is bookkeeping: corner charges, the first law and black-hole entropy

*Sheldon Lindberg, November 2026. Technical note, not peer reviewed. Every result is
computed by a script in `src/` and pinned by a test. Labels: **KNOWN** (published),
**CHECK** (computed here), **FOLLOWS** (a consequence), **LIT** (quoted from a source).*

## Abstract

Teleparallel gravity (TEGR) differs from general relativity by a boundary term, so the
two have the same field equations. They differ in one variable that GR doesn't have: the
frame, a local Lorentz frame that is pure gauge in the bulk and is encoded by a flat
connection. Edge-mode approaches to black-hole entropy need exactly such boundary data,
so it is natural to ask whether TEGR's frame contributes to the entropy. We find that it
doesn't:

- **Classically, the frame changes where the entropy is booked, not the first law.**
  - With the static frame, TEGR's Noether charge vanishes at the bifurcation surface and
    the whole Wald entropy sits in the corner term.
  - For frames winding around the Euclidean time circle, the tip term is (A/4)(1 + k/κ).
  - The first law, δM = TδS + ΦδQ, comes out identical to GR's for every frame.
- **The frame's corner phase space is a Lorentz coadjoint orbit through ⋆Σ_S/8πG,** the
  dual of the surface's area bivector, for any metric.
  - Its charges close exactly into so(3,1).
  - At linear order its normal boost is conjugate to area/8πG, the Carlip–Teitelboim
    pair.
- **Quantum mechanically, the frame is bookkeeping too.**
  - Quantizing the orbit as a group gives a logarithm, not the area law.
  - That logarithm depends on the group chosen (1, 5 or 9 × ln a in Sen's ensemble) and
    not on the matter content. Sen's universal coefficient is 77/45 for pure gravity and
    does depend on it.
  - So the frame must be treated as gauge in the measure, and TEGR's black-hole entropy,
    area law and logarithm included, is GR's.

## 1. Setup

TEGR uses a tetrad e^a_μ and a flat spin connection ω, with torsion
T^a = de^a + ω^a_b e^b. The action is S = −(1/16πG)∫ e T, and the torsion scalar satisfies
T = −R + B with B = (2/e)∂_μ(e T^μ) a total divergence (CHECK: `src/stur_tegr.py`, E1).
So L_TEGR = L_GR + dα with α^μ = e T^μ/8πG.

Every flat connection used here is built as ω = Λ⁻¹dΛ, and its curvature is checked to
vanish. G = 1 unless stated.

## 2. Classical: charges, corner term and the first law (`src/stur_tegr_corner.py`)

Static metrics −f dt² + dr²/f + r²dΩ², for any f; ξ = ∂_t.

| | Result | Status |
|---|---|---|
| K1 | TEGR's Noether charge, from L_TEGR directly: **Q_TEGR(r) = r(√f − f)**, the lapse times the Brown–York energy. It is M at infinity and **0 at the horizon** | CHECK; matches Maluf's TEGR energy and the ADM mass (Hammad et al., [1912.08811](https://arxiv.org/abs/1912.08811)) |
| K2 | GR's Iyer–Wald charge: r²f′/4, which is κA/8π at the bifurcation surface, so the Wald entropy is A/4 | KNOWN; CHECK |
| K3 | Q_GR − Q_TEGR is exactly the corner term ι_ξα, and at the horizon it carries all of κA/8π | CHECK |
| K4 | The frame boosted along the Killing flow, regular at the bifurcation surface: the diffeomorphism charge is unchanged, and a compensating-boost volume term appears | CHECK |
| K5 | Euclidean frames winding at rate k: the tip term is **(A/4)(1 + k/κ)**. It is A/4 for the non-rotating frame and 0 for the frame regular at the tip (k = −κ), which then diverges at infinity | CHECK |
| K6 | The first law for Reissner–Nordström, varying M and q independently. h(r) = ∮(δQ + Θ^r) is the same in TEGR (static and boosted frames) and GR. With Maxwell, h = δM at every r, and **δM = TδS + ΦδQ** at the horizon. The split differs: GR's charge and flux are each finite at the horizon, TEGR's each diverge and only their sum is finite | CHECK |

**Why the frame drops out of K6** (FOLLOWS): Θ_TEGR = Θ_GR + δα and Q_TEGR = Q_GR + ι_ξα,
so the difference in h is δ(ι_ξα) − ι_ξ(δα) = 0. TEGR's symplectic current equals GR's.

**Caveat:** with ξ held fixed, a δM perturbation is not smooth at the bifurcation surface
in either theory. Only the total h(r₊) is invariant there.

## 3. The frame's corner phase space (`src/stur_tegr_frame.py`)

| | Result | Status |
|---|---|---|
| Q1 | Linearized: the frame (the antisymmetric part of the tetrad) is pure gauge in the bulk | KNOWN; CHECK |
| Q2 | The frame's part of the symplectic current is a unique covariant corner term | CHECK |
| Q3 | On an entangling plane: **the frame's normal boost is conjugate to area/8πG**. The mixed boosts and rotations pair with off-diagonal tetrad components. The rotation within the surface pairs with nothing | CHECK; the pairing is KNOWN in metric variables (Carlip–Teitelboim, [gr-qc/9312002](https://arxiv.org/abs/gr-qc/9312002)) and tetrad variables (Freidel–Perez, [1507.02573](https://arxiv.org/abs/1507.02573)) |
| Q4 | K5's Euclidean result gives the same coefficient, 1/8π | consistency |
| Q5 | Finite frames, flat metric: the corner form is exactly **(1/8π)[Λ⁻¹δ₁Λ, Λ⁻¹δ₂Λ]**, a Kirillov–Kostant form (60-digit check, error 10⁻³⁴) | CHECK |
| Q6 | The corner charges close exactly into **so(3,1) ≅ sl(2,ℂ)**. The stabilizer is {normal boost, rotation in the surface} | CHECK |
| Q8 | Any metric, off shell: the orbit passes through **⋆Σ_S/8πG**, with Casimirs N·N = −2σ (the radius is the area density) and N·⋆N = 0 (simple) | CHECK |

**What this matches** (KNOWN):
- the sl(2,ℂ) corner Lorentz charges of tetrad gravity (Freidel–Geiller–Pranzetti, Part II,
  [2007.03563](https://arxiv.org/abs/2007.03563));
- the simplicity condition B = ⋆(e∧e), imposed by hand in spin-foam models, which here
  comes out of the frame's corner form.

## 4. Quantum: the area law and the logarithm (`src/stur_tegr_frame.py` Q7, `src/stur_tegr_logs.py`)

**The area law.**
- Quantizing a coadjoint orbit through a boost gives principal-series representations,
  labelled by the area.
- Varrin ([2610.37750](https://arxiv.org/abs/2610.37750), eqs. 4.14 and 4.20) gives the
  group Plancherel density for SL(2,ℝ): k tanh(πk). It grows linearly and gives ln A.
  Only the causal semigroup SL⁺(2,ℝ) of normal-plane maps, with density k sinh(2πk),
  gives A/4. **For Lorentz boosts that causal condition holds automatically**, so it
  can't come from the frame.
- The area law needs normal-plane maps beyond boosts, which are diffeomorphism edge modes
  and are the same in TEGR and GR.

**The logarithm**, as the coefficient of ln a in Sen's ensemble (singlet states per unit
mass; [1205.0971](https://arxiv.org/abs/1205.0971), eqs. 1.2 and 1.5):

| | Coefficient |
|---|---|
| Sen, pure gravity (universal) | 77/45 = 1.711 |
| Sen, gravity + photon | 64/45 = 1.422 |
| SU(2) loop quantum gravity (Sen, section 4) | −2 |
| Frame as SO(1,1): the boost only (spherical reduction) | 1 |
| Frame as SL(2,ℝ) | 5 |
| Frame as SL(2,ℂ), simple series: its full orbit | 9 |
| Varrin's causal semigroup | 5 |

**FOLLOWS:**
- The frame's logarithm depends on the group chosen and not on the matter content. Sen's
  coefficient, an integrated trace anomaly plus zero modes, does depend on the matter
  content.
- Sen's coefficient is the same in TEGR and GR, because their one-loop bulk determinants
  coincide, provided the frame is treated as gauge in the path-integral measure.
- Counting the frame's states as physical would change it, against a result that matches
  microscopic counting in the extremal cases.

## 5. Conditions and caveats

- K1–K6 are for static, spherically symmetric black holes.
- Q5, Q6 and Q8 vary the frame with the metric held fixed. Joint variations of frame and
  metric are covered at linear order only (Q3).
- The SL(2,ℂ) Plancherel density, ∝ (n² + ρ²), is the Gelfand–Naimark result, quoted from
  memory.
- Mapping Varrin's spherically reduced counting onto Sen's ensemble is a heuristic
  comparison, not a derivation in that ensemble.
- A first-principles check would compute TEGR's Euclidean one-loop partition function with
  the frame's measure written out explicitly. That isn't done here.
- **Novelty.** The individual ingredients are known (sections 2–4). Small INSPIRE searches
  (recorded in [QUANTUM_TEGR.md](QUANTUM_TEGR.md), sections 6–8) found no statement of the
  TEGR versions: Q_TEGR vanishing at the bifurcation surface, the frame's orbit through
  ⋆Σ_S/8πG, or the log comparison. Not finding them doesn't mean they haven't been done.

## 6. What it means

TEGR is GR in different variables, and its extra variable, the frame, is where an
edge-mode account of black-hole entropy might have found something new. It does carry
real corner structure: an orbit of the Lorentz group sized by the area, with the area
conjugate to the boost. But that structure only moves terms between charges and fluxes
classically, and quantum mechanically it supplies neither the area law nor the universal
logarithm. In this sense the frame is bookkeeping, and TEGR's black-hole thermodynamics is
GR's.

## 7. Reproduce

```bash
python3 src/stur_tegr.py           # E1-E3b: identity, Newton, black-hole entropy
python3 src/stur_tegr_corner.py    # K1-K6, ~60 s
python3 src/stur_tegr_frame.py     # Q1-Q8, ~30 s
python3 src/stur_tegr_logs.py      # the log comparison, ~1 s
python -m pytest tests/test_tegr.py tests/test_tegr_corner.py tests/test_tegr_frame.py tests/test_tegr_logs.py -q
```

## References

- S. Carlip and C. Teitelboim, *The off-shell black hole*, Class. Quant. Grav. 12 (1995),
  [gr-qc/9312002](https://arxiv.org/abs/gr-qc/9312002).
- V. Iyer and R. M. Wald, Phys. Rev. D 50 (1994) 846, [gr-qc/9403028](https://arxiv.org/abs/gr-qc/9403028).
- L. Freidel and A. Perez, *Quantum gravity at the corner*, Universe 4 (2018),
  [1507.02573](https://arxiv.org/abs/1507.02573).
- L. Freidel, M. Geiller and D. Pranzetti, *Edge modes of gravity* I and II,
  [2006.12527](https://arxiv.org/abs/2006.12527), [2007.03563](https://arxiv.org/abs/2007.03563).
- F. Hammad, D. Dijamco, A. Torres-Rivas and D. Bérubé, *Noether charge and black hole
  entropy in teleparallel gravity*, [1912.08811](https://arxiv.org/abs/1912.08811).
- F. Girelli, J. Qiu and C. Zwikel, *Teleparallel gravity at null infinity*, Phys. Rev. D
  (2025), [2412.14258](https://arxiv.org/abs/2412.14258).
- I. Kuntz, G. Paci and O. Zanusso, [2410.04510](https://arxiv.org/abs/2410.04510);
  J. Beltrán Jiménez and T. S. Koivisto, [2412.13946](https://arxiv.org/abs/2412.13946).
- A. Sen, *Logarithmic corrections to Schwarzschild and other non-extremal black hole
  entropy in different dimensions*, JHEP 04 (2013) 156, [1205.0971](https://arxiv.org/abs/1205.0971).
- L. Varrin, *Black hole entropy from entangled quantum reference frames*,
  [2610.37750](https://arxiv.org/abs/2610.37750).
- J. R. David and J. Mukherjee, *Entanglement entropy of gravitational edge modes*,
  JHEP 08 (2022) 065, [2201.06043](https://arxiv.org/abs/2201.06043).
