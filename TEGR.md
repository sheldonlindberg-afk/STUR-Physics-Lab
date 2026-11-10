# Gravity in TEGR: the same predictions, a gauge-field reading, and STUR's connection

Reproduce: `python3 src/stur_tegr.py` (about 30 s, sympy). The full output is in
`results/tegr/output.txt`, and `tests/test_tegr.py` pins the results. Labels: KNOWN,
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

This is the "no exotic physics" form of gravity: a force field like electromagnetism,
with nothing curved and no wormholes.

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

**E5. STUR's open problem P2: which connection is A_μ?** Candidate:
A_μ = (mc/ħ)B⁰_μ, the translational potential.

| Requirement | Met? | Why |
|---|---|---|
| R1: holonomy of a gauge connection | **yes** | translation gauge group; abelian at linear order |
| R2: Gaussian noise | **yes** | free linear field; but noise ~ (ℓ_P/L)², 2.6×10⁻⁷⁰ at 1 m |
| R3: area law at the QCD scale | **no** | massless, so it gives a perimeter law, like EM |
| R4: horizon entropy A/4ℓ_P² | **yes** | E3, with a smooth horizon as in GR |
| R5: couples to a neutral atom | **yes** | every mass; COW phase 1.58×10⁸ rad in MAGIS |

It meets 4 of 5. It is the first candidate in P2 that meets R1, R4 and R5 at full
strength. The Levi-Civita spin connection reaches atoms only as a 10⁻¹⁴ boost.

With Gaussian noise in this A_μ, the visibility formula V = exp(−½⟨Φ_R²⟩) becomes exactly
the [OPTION_A.md](OPTION_A.md) model. Its area-law version is excluded, and its
standard graviton version is too small to see. **TEGR names STUR's connection on the
gravity side; the QCD end stays open.**

**E6. Does gravity's own field record which path?** This is the gravitational version
of T5. I computed quadrupole radiation from one branch of the diamond, with a smooth
ramp and analytic derivatives:

| Design | Radiated energy | Gravitons emitted |
|---|---|---|
| 1.5×10⁻¹⁴ kg, 721 µm, ramps 1.58 s (design A) | 5.8×10⁻⁹³ J | 1.4×10⁻⁵⁹ |
| 10⁻¹⁴ kg, 250 µm, ramps 0.73 s | 1.8×10⁻⁹³ J | 1.9×10⁻⁶⁰ |

No graviton carries which-path information away. The only record is the static,
Coulomb-like torsion field bound to the source, and it is undone when the paths
recombine (KNOWN in outline: Belenchia et al. 2018).

For the electron, the decoherence in T5 needed a nearby *surface*. Gravity has no
conductors, because there is no negative mass, so it has no analogue of that surface
and can't be screened.

## What TEGR changes

- **Predictions: nothing.** T = −R + B, so λ = 1 versus λ = 0, the phases, the noise
  budget and the experimental design are all as in GRAVITY_ENTANGLEMENT.md.
- **The reading changes.** Gravity becomes a gauge force field on flat spacetime with
  the same structure as electromagnetism. The split-versus-amplitude question
  becomes the *same* question for both fields:
  - EM already behaves as λ = 1.
  - TEGR's linear theory is an abelian gauge theory like EM, which makes λ = 1 the
    structural expectation for gravity. That is an expectation, not a proof; the
    experiment still decides.
- **The field's own action** is part of the entangling phase (E4).
- **STUR's A_μ has a name** on the gravity side (E5).

Not used: f(T) and other modified teleparallel theories. They do change predictions,
but they add new structure.
