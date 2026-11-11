# Gravity as torsion (TEGR): GR's equations and tests, recomputed

*Research notes, not peer reviewed. Labels mark what is established physics, what is computed here, and what holds only under stated assumptions.*

These notes write gravity in its teleparallel form (TEGR), which is known to be
equivalent to GR. As a check of that equivalence, GR's field equations, its
Schwarzschild solution and its classic tests are recomputed from TEGR below.

Reproduce:
- `python3 src/stur_tegr.py` (about 30 s, sympy). Output in `results/tegr/output.txt`;
  pinned by `tests/test_tegr.py`.
- `python3 src/stur_tegr_gr.py` (about 3 s). Output in `results/tegr/gr_output.txt`;
  pinned by `tests/test_tegr_gr.py`. Labels: KNOWN,
FOLLOWS, CHECK (computed here), LIT.

## What TEGR is (KNOWN)

TEGR is the teleparallel equivalent of general relativity (Einstein 1928;
Møller 1961; Hayashi–Shirafuji 1979; Aldrovandi–Pereira 2013).

- Gravity is a **gauge field of translations** on flat spacetime, not curvature. The
  field is the tetrad e^a_μ, and its potential is B^a_μ = e^a_μ − δ^a_μ.
- The field strength is **torsion**, T^a_μν = ∂_μe^a_ν − ∂_νe^a_μ + (flat spin-connection
  terms). Curvature is zero everywhere.
- The Lagrangian is quadratic in torsion, as electromagnetism's is in F_μν:
  L = −e·T/(16πG) − ρΦ.

Written this way, gravity looks like a force field similar to electromagnetism, with
nothing curved. It is the same physics as GR: every solution GR allows, TEGR allows too.

## Results

**E1. Same equations as GR (CHECK).** For a non-trivial tetrad, T = −R + B exactly,
where B = (2/e)∂_μ(e T^μ) is a total divergence. The residual T + R − B is 10⁻¹⁶⁵ at
random points. So the field equations are GR's, and every number in
[GRAVITY_ENTANGLEMENT.md](GRAVITY_ENTANGLEMENT.md) is unchanged.

**E2. Newton's law, coefficient included (CHECK).** For e⁰ = e^Φ dt and eⁱ = e^−Ψ dxⁱ:

```
(e T)₂ = 4 ∇Φ·∇Ψ − 2 (∇Ψ)²      (+ divergence)
δ/δΨ :  ∇²Ψ = ∇²Φ        →  Ψ = Φ
δ/δΦ :  ∇²Ψ = 4πGρ       →  Newton
```

With Ψ = Φ the Lagrangian becomes L = −(1/8πG)(∇Φ)² − ρΦ. That is the static
Lagrangian of electromagnetism with the sign of the field energy flipped, which is
why like charges attract.

**E3. Black-hole entropy (CHECK).** In vacuum R = 0, so the TEGR action is entirely a
boundary flux. I used Euclidean Schwarzschild with the diagonal tetrad, and with the
flat spin connection of the same tetrad at M = 0 (Krššák–Pereira 2015).

| Flux | Euclidean action |
|---|---|
| At infinity | **4πM²**, exactly GR's βM/2, with no Gibbons–Hawking term or subtraction |
| At the horizon tip | 4πM² |

With the horizon smooth, as GR assumes, S = βM − I_∞ = 4πM² = **A/4**.

The tip flux comes from a frame that doesn't rotate around the Euclidean horizon,
and is singular there. A frame that is regular at the tip needs a rotation k dτ, and
then the flux at infinity diverges (the integrand tends to −4kM; checked in the tests).
No single flat frame is regular at both ends. **TEGR gets A/4 with the same input as
GR (a smooth horizon), not with less.**

**E4. The gravitational phase is a TEGR holonomy, and the field carries part of it.**
A mass picks up phase −(mc/ħ)∫e⁰_μdx^μ, the holonomy of B⁰₀ = Φ/c². This is
measured in the COW experiment (1975) and in the gravitational Aharonov–Bohm effect
(Overstreet et al. 2022). For two masses:

| Term | Value |
|---|---|
| Matter coupling (−m₁Φ₂ − m₂Φ₁) | +2Gm²/r |
| The field's own action, −(1/8πG)∫(∇Φ)² cross term | −Gm²/r |
| Total Lagrangian = −U | +Gm²/r |

The field term isn't optional: without it the entangling phase would be doubled.
For it to depend on which branch each diamond is in, **the torsion field itself must
be in two places.** In TEGR language, λ = 1 means the torsion field is in two places,
exactly as the electron's EM field is (T5 in [MEASUREMENT.md](MEASUREMENT.md)).
λ = 0 means there is only one torsion field.

**E5. The translational potential as an abelian gauge field.** Take
A_μ = (mc/ħ)B⁰_μ, TEGR's translational potential.

- Its holonomy is a translation-gauge phase, abelian at linear order.
- It couples to every mass: the COW phase is 1.58×10⁸ rad in MAGIS-100.
- Being massless, its Wilson loops obey a perimeter law, as in electromagnetism.
- Its vacuum noise scales as (ℓ_P/L)², 2.6×10⁻⁷⁰ at 1 m.

With Gaussian noise in this potential, V = exp(−½⟨Φ²⟩) is the standard graviton-bath
decoherence, far too small to see. By contrast, the Levi-Civita spin connection reaches
an atom only as a 10⁻¹⁴ boost, so in TEGR the translational potential is the natural
place to put gravity's coupling to an interferometer phase.

**E6. Does gravity's own field record which path?** This is the gravitational version
of T5. I computed quadrupole radiation from one branch of the diamond, with a smooth
ramp and analytic derivatives:

| Design | Radiated energy | Gravitons emitted |
|---|---|---|
| 1.5×10⁻¹⁴ kg, 721 µm, ramps 1.58 s (design A) | 5.8×10⁻⁹³ J | 1.4×10⁻⁵⁹ |
| 10⁻¹⁴ kg, 250 µm, ramps 0.73 s | 1.8×10⁻⁹³ J | 1.9×10⁻⁶⁰ |

Essentially no graviton carries which-path information away. The only record is the static,
Coulomb-like torsion field bound to the source, and it is undone when the paths
recombine (KNOWN in outline: Belenchia et al. 2018).

For the electron, the decoherence in T5 needed a nearby *surface*. Gravity has no
conductors, because there is no negative mass, so it has no analogue of that surface
and can't be screened.

## GR from TEGR (`src/stur_tegr_gr.py`)

**F1. The black-hole solution, from TEGR's equations (CHECK).** For a static spherical
tetrad e⁰ = e^A dt, e¹ = e^B dr, e² = r dθ, e³ = r sinθ dφ, the reduced TEGR Lagrangian is

```
e T / sinθ = 2 e^(A−B) [ 2r A′(e^B − 1) − (e^B − 1)² ]
δ/δB :  2r A′ = e^(2B) − 1          (a constraint: B has no derivative)
δ/δA :  2r B′ = 1 − e^(2B)
⇒  e^(−2B) = 1 + C₁/r,   A = −B
```

The Newtonian limit (E2) fixes C₁ = −2GM/c². That gives e^(2A) = 1 − r_s/r and
e^(2B) = 1/(1 − r_s/r), which is the Schwarzschild metric g = eᵀηe. It is the only
static spherical solution, so Birkhoff's theorem falls out of TEGR's own equations.

**F2. The classic tests, from the F1 tetrad only.** These are numerical geodesic
integrals, not textbook formulas, and use no curvature anywhere.

| Test | TEGR | Observed (LIT) |
|---|---|---|
| Mercury's perihelion | **42.98″/century** | 42.98″ (GR part of the observed 43.1 ± 0.5) |
| Light bending at the solar limb | **1.7512″** | VLBI: γ = 0.99983 ± 0.00045 |
| PPN γ (Shapiro delay) | **exactly 1** | Cassini: γ − 1 = (2.1 ± 2.3)×10⁻⁵ |
| GPS clock, satellite vs ground | **+38.54 µs/day** (gravity alone +45.65) | design offset 38.6 |

Newton accounts for half of the light bending, through the e^(2A) part. The other half
is e^(2B), the Ψ = Φ result of E2, and Newton has no place for it.

**F3. The diamonds' interaction from TEGR's field energy.** I integrated the torsion
field energy (1/8πG)∫(∇Φ)² numerically over all space for two *finite* uniform
diamonds, not point masses. The field term is +Gm²/d to within 2×10⁻¹⁵ at 181 µm, and
to within 2×10⁻¹³ at d = 3R. So the total is −Gm²/d, and the shell theorem comes out
of the field itself.

**F4. The experiment's phases are TEGR's.** The four branch-pair phases recomputed
from F3 agree with those in [GRAVITY_ENTANGLEMENT.md](GRAVITY_ENTANGLEMENT.md) to
6×10⁻¹⁶ rad. The next TEGR order is Gm/(c²d) = 4×10⁻³⁸, and (v/c)² for the split is
2×10⁻²⁴. So the whole experimental design and noise budget stand, now as TEGR
results.

## What this means

- **TEGR reproduces GR.** GR's equations, Newton's law and the experiment's inputs are
  all recomputed from it (E1, E2, F1–F4), without using curvature. This checks a known
  equivalence; it is not a new result.
- **In TEGR, gravity is written as a gauge force field on flat spacetime,** with a
  structure similar to electromagnetism. The split-versus-amplitude question is therefore the *same*
  question for both fields:
  - EM already behaves as λ = 1.
  - TEGR's linear theory is an abelian gauge theory like EM, which makes λ = 1 the
    structural expectation. That is an expectation, not a proof; the experiment decides.
- **The torsion field's own action** is part of the entangling phase (E4). So the
  experiment tests whether the *torsion field* is in two places.
- **The translational potential as an abelian gauge field** (E5): it couples to every
  mass, and its vacuum noise is far too small to see.

Not used: f(T) and other modified teleparallel theories. They change predictions,
but they add new structure.
