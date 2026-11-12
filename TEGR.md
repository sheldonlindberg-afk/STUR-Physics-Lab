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
and is singular there. A frame that is regular at the tip winds around the time circle
at rate k = −κ, and then the flux at infinity diverges. In the family of flat frames
winding at rate k, only k = 0 is finite at infinity and only k = −κ is regular at the
tip (K5 below, which replaces an earlier check that used a connection that wasn't
flat). **TEGR gets A/4 with the same input as GR (a smooth horizon), not with less.**

This is a recomputation of a known result. Kuntz, Paci and Zanusso
([2410.04510](https://arxiv.org/abs/2410.04510)) obtain the black-hole thermodynamics from
the teleparallel Euclidean action. Beltrán Jiménez and Koivisto
([2412.13946](https://arxiv.org/abs/2412.13946)) do so without subtractions, for charged
black holes and with a cosmological constant.

**E3b. The charged black hole, and what the tip term is (CHECK).** For any static
metric f dτ² + dr²/f + r²dΩ², with the same tetrad and reference connection, the flux is

  e T^r / sin θ = r (4√f − 4f − r f′) / 2.

| | Result |
|---|---|
| Reissner–Nordström, flux at infinity | M: the Q² terms fall off, so I_grav = βM/2 with no subtraction, as for Schwarzschild |
| Maxwell action (the same in TEGR and GR; Gibbons–Hawking 1977, taken as input) | −βQΦ/2 |
| Entropy, S = β(M − QΦ) − I | π r₊² = **A/4** |
| Horizon tip, any f with f(r₊) = 0 | the flux is −r₊² f′(r₊)/2, so the tip term is β r₊² f′(r₊)/4 = π r₊² = **A/4 for every static horizon** |

For Schwarzschild the two ends happen to give the same value, 4πM², because there
βM/2 = A/4. The charged case separates them: **the flux at infinity gives the action and
the flux at the tip gives the entropy.** That is the known statement that the horizon
term of the Euclidean action carries the entropy (Bañados, Teitelboim and Zanelli 1994).
In TEGR it appears as the torsion flux at the tip of the non-rotating frame. Beltrán
Jiménez and Koivisto's horizon-only prescription is built on this term.

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

## Where the entropy sits: Noether charges and the frame (`src/stur_tegr_corner.py`)

TEGR's Lagrangian is GR's plus a total derivative, so the two theories have the same bulk
but their Noether charges differ by a corner term (Iyer and Wald 1994; for formulations of
gravity in general, Freidel, Geiller and Pranzetti,
[2006.12527](https://arxiv.org/abs/2006.12527)). This section computes both for static
metrics −f dt² + dr²/f + r²dΩ², with any f. Every flat connection is built as
ω = Λ⁻¹dΛ, and its curvature is checked to vanish. All of it is a check of known physics
except where marked open.

**K1. TEGR's Noether charge (CHECK).** For ξ = ∂_t, computed directly from
L = −eT/16π with no superpotential convention assumed:

  Q_TEGR(r) = r(√f − f) = N·E_BY,

the lapse N = √f times the Brown–York quasilocal energy E_BY = r(1 − √f). The TEGR
momentum Π₀^{tr} integrates to E_BY itself. Q_TEGR tends to M, the ADM mass, at infinity
(as Hammad et al., [1912.08811](https://arxiv.org/abs/1912.08811), find) and to **0 at the
horizon**. This matches Maluf's TEGR gravitational energy, which is E_BY.

**K2. GR's Iyer–Wald charge (CHECK).** Q_GR(r) = r²f′/4. That is Komar's M/2 at
infinity and κA/8π at the bifurcation surface, so the Wald entropy (2π/κ)Q_GR is A/4,
for Schwarzschild and Reissner–Nordström.

**K3. The difference is the corner term (CHECK).** Q_GR − Q_TEGR equals ι_ξα exactly,
where α^μ = e T^μ/8π is TEGR's boundary term and the corner term is the torsion flux of
E3b. The two routes (the Noether charge from L_TEGR, and GR's charge plus the corner term)
agree identically in f. At the bifurcation surface the corner term is all of κA/8π.
**With the static frame, TEGR's Noether charge carries none of the Wald entropy; the
corner term carries all of it.**

**K4. The frame regular at the bifurcation surface (CHECK).** Boost the frame along the
Killing flow, Λ = Λ_A B(κt). The connection is flat, and:
- the diffeomorphism charge is unchanged, r(√f − f); κ drops out;
- ξ is a symmetry only together with a compensating local boost λ = ι_ξω, and that
  adds a volume term κ r (1/√f − 1) per unit radius. This vanishes as the region shrinks
  to the horizon and grows linearly at infinity, where the frame keeps boosting.

Whether this Lorentz sector carries κ δS in the first law is answered by K6: it doesn't.

**K5. Euclidean: the frame winding around the time circle (CHECK).**
Λ = Λ_A R(kτ), with k = 0 the frame of E3:

| Winding rate | Tip term | Flux at infinity |
|---|---|---|
| any k | (A/4)(1 + k/κ) | diverges unless k = 0 |
| k = 0 (non-rotating, E3) | A/4 | M, finite: I = βM/2 |
| k = −κ (regular at the tip) | 0 | diverges |

The earlier version of this check added k dτ to the static reference connection. That
connection has four nonzero curvature components, so it isn't TEGR's. K5 replaces it, and
E3's conclusion survives.

**K6. The first law (CHECK).** The Hamiltonian variation on a sphere of radius r is
h(r) = ∮(δQ^{tr} + Θ^r). Here δ varies M and the charge q independently, for
Reissner–Nordström. TEGR's symplectic potential is computed from its own momentum,
Θ^r = Π_a^{rν} δe^a_ν. GR's Θ and Q come from the Iyer–Wald formulas, and Maxwell's
terms are added to both theories.

| | Result |
|---|---|
| Gravity, TEGR (static frame), TEGR (boosted frame), GR | h = δM − q δq/r in all three, identical at every r. The frame drops out |
| Gravity + Maxwell | h = δM at every r |
| At the horizon | gravity gives TδS = κδA/8π, Maxwell gives Φ δq (Φ = q/r₊): **δM = TδS + Φ δQ**, in both theories |
| The split, GR | δQ = δM/2 − q δq/r, Θ^r = δM/2: finite at the horizon |
| The split, TEGR | δQ = h(2 − 1/√f), Θ^r = h(1/√f − 1): each diverges at the horizon, and only the sum is finite |

Why the frame drops out: L_TEGR = L_GR + dα gives Θ_TEGR = Θ_GR + δα and
Q_TEGR = Q_GR + ι_ξα, so the difference in h is δ(ι_ξα) − ι_ξ(δα) = 0. TEGR's
symplectic current equals GR's, so the frame contributes no bulk term either. The
computation confirms this without assuming it, because Θ_TEGR and Q_TEGR are computed
from the TEGR Lagrangian directly.

A caveat. With ξ = ∂_t held fixed, the δM perturbation in static coordinates isn't smooth
at the bifurcation surface, because κ changes. So in neither theory does the charge alone
equal TδS there: GR's δQ(r₊) is δM/2 at q = 0, not δM. Only h(r₊) is invariant, and it is
TδS + Φ δq.

**What this shows.** The bulk theories are identical, but *where the entropy is booked*
depends on the flat connection, i.e. on the frame. For the static frame it sits entirely
in the corner term. For the frame regular at the Euclidean tip it leaves the tip, and the
frame pays at infinity instead. That the frame carries corner data in TEGR is the
edge-mode reading of Girelli, Qiu and Zwikel ([2412.14258](https://arxiv.org/abs/2412.14258))
at null infinity; K3–K5 are the corresponding classical facts at a horizon. The first
law (K6) is the same in both theories and doesn't see the frame, so classically the frame
changes the bookkeeping, not the thermodynamics. Whether quantizing that frame gives A/4
as entanglement entropy is the open question in
[QUANTUM_TEGR.md](QUANTUM_TEGR.md), section 6.

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
