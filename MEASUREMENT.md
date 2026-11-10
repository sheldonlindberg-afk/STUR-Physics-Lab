# Measurement, the double slit, and entanglement: three proposals, tested

Reproduce: `python3 src/stur_measurement.py` (about 3 s). The full output is in
`results/measurement/output.txt`, and `tests/test_measurement.py` pins the numbers.
Labels: KNOWN, FOLLOWS, LIT (literature value used as input), PROPOSAL.

## The proposals

| # | Proposal |
|---|---|
| M1 | The act of measuring is what creates the quantum particle we see. |
| M2 | Before it is seen, an electron is not a probability cloud but a real EM "cloud", produced by the strong force. |
| M3 | Entanglement isn't a separate thing: it is one particle stretched across spacetime. Act on one side and the other reacts instantly. |

The aim is a new equation for the double slit and quantum gravity. Before writing
one, each ingredient is tested the way options A–C were tested in [WALL.md](WALL.md).

## Verdict

| # | Result | Status |
|---|---|---|
| M1 | Measurement creates the **definite outcome** (which path, where the dot lands), not the electron. The electron's mass and charge are already there at the slits. | **Partly right, reworded.** The equation is KNOWN: V = \|⟨E₁\|E₂⟩\| |
| M2a | A real charge cloud repels itself. Hydrogen solved with that self-repulsion binds by 6.64 eV; measured: 13.60 eV. | **Excluded** (factor 2) |
| M2c | Restated as "one EM charge pulled into two places": the halves (e/2 each) repel in flight, a kick 0.4–0.7× the interferometer's own deflection; and a nearby surface would not wash out the fringes, but it does (Sonnentag & Hasselbach 2007). | **Excluded** |
| M2b | The cloud exists, at the right size and energy, in positronium (e⁺e⁻), which contains no quarks or gluons. | **Excluded** |
| M3 | "One stretched object with an instant reaction" gives S = 2√2, the same as quantum mechanics, and cannot send signals. Without the instant reaction it gives S = 2, which experiment rules out. | **Survives, but not new.** It is a picture of entanglement (collapse / Bohm-type nonlocality), not a replacement for it. |

## T1. A real EM cloud (M2, first half)

Schrödinger proposed this in 1926: the electron *is* a charge density e|ψ|². He
dropped it, and the reason can be computed. A real charge distribution has a
self-energy J = ½∫ρφ, so it pushes itself apart.

| Hydrogen 1s | Binding energy | ⟨r⟩ |
|---|---|---|
| Standard (no self-repulsion) | 13.605 eV | 1.50 a₀ |
| Real self-repelling cloud, solved self-consistently (FOLLOWS) | **6.64 eV** | 2.50 a₀ |
| Measured (LIT) | 13.598 eV | — |

The self-energy of the standard 1s cloud alone is 5/16 Ha = 8.50 eV. So whatever
surrounds the proton does not repel itself. It is not a cloud of charge; it is an
amplitude for where the one whole charge e will turn up. In the double slit, every
detection registers a whole e, never e/2 on each side.

## T2. Made by the strong force? (M2, second half)

- Electrons are leptons and carry no colour charge (KNOWN).
- The strong force's range is ħ/m_πc = 1.41 fm. The electron cloud is 52,918 fm.
  The Yukawa suppression at that distance is e^(−37,429) ≈ 10^(−16,255).
- Positronium is an electron bound to a positron, with nothing strongly interacting
  anywhere. The pure-EM Bohr formula gives its 1S–2S line to 6.8×10⁻⁵ (the size of
  the known QED corrections). With those corrections included, theory and
  measurement agree to about 10⁻⁹ (LIT: Fee et al. 1993).

## T3. The double slit with a which-path record (M1)

The equation that already explains the measurement effect (KNOWN; Wootters–Zurek
1979, Englert 1996):

```
P(y) = |ψ₁|² + |ψ₂|² + 2 Re[ψ₁ ψ₂* ⟨E₂|E₁⟩]        V = |⟨E₁|E₂⟩|,   D² + V² ≤ 1
```

|E₁⟩ and |E₂⟩ are the states the detector (or any environment) ends up in for
each path. The simulation reproduces D² + V² = 1 at every coupling. The fringes
fade **continuously** as the record gets clearer. Nobody has to look; it is enough
that a record exists anywhere.

A real cloud with no phase gives V = 0 even with no detector. But single electrons
sent one at a time do build fringes (LIT: Tonomura 1989; Bach et al. 2013), with
spacing set by λ = h/p = 5.355 pm at 50 keV. That formula contains the electron's
mass, so what passes the slits already carries m_e and e.

**What M1 gets right:** a definite path does not exist until a record of it
exists. Stated that way, it is already the content of the equation above.

## T4. Entanglement as one stretched object (M3)

| Model | CHSH S |
|---|---|
| Quantum mechanics (singlet) | 2.8284 |
| One stretched object, instant reaction (Monte Carlo) | 2.822 ± 0.01 |
| One stretched object, set at creation, no instant reaction | 2.000 |
| Entanglement swapping: particles 1 and 4 never meet | 2.8284 |

- With an instant reaction, M3 reproduces quantum mechanics exactly. Bob's
  P(+1) = 0.5000 whatever Alice chooses, so no message can be sent.
- Without one, it is a local hidden-variable model and Bell's bound S ≤ 2 holds.
  Loophole-free tests see S > 2 (LIT: Hensen; Giustina; Shalm, all 2015).
- Any finite reaction speed would allow signalling (LIT: Bancal et al. 2012).
  Experiment puts it above 10⁴ c (LIT: Salart et al. 2008). So it must be instant.
- **Swapping** is the hard case for "one particle". Particles 1 and 4 come from
  separate sources and never interact. A measurement on 2 and 3 alone leaves 1 and
  4 maximally entangled. So the "one stretched object" would have to be assembled
  after the fact, by a measurement, out of pieces that never met.

So "entanglement isn't real" doesn't follow. The stretched-object picture is a
description of entanglement, and it gives the same predictions.

## T5. One EM charge pulled into two places, with ordinary EM only

This is M2 without the strong force: one charge, really split between the two paths.

**Self-repulsion in flight.** 50 keV electron, halves of e/2 starting 5 µm apart,
0.3 m of flight, typical biprism deflection of 5×10⁻⁵ rad per beam (an assumed
typical value, not fitted):

| Inertia of each half | Separation after flight | Repulsion kick / biprism kick |
|---|---|---|
| Half the electron's mass | 5.0 → 19.5 µm | 0.67 |
| Full electron mass (least kick) | 5.0 → 13.8 µm | 0.44 |

The halves push each other apart by an amount comparable to the interferometer's
own deflection. The kick depends on e² and on the path separation, so it would warp
the fringe spacing, and it acts on every electron, even when they are sent one at a
time. Standard theory has no such term.

**The field test, already done.** Where is the electron's field while it is in two
places?

- Split charge: a nearby surface feels e/2 + e/2, an ordinary classical field. The
  image charges only shift the phase, and the fringes stay sharp.
- Quantum: the image charge is different for the two paths, so the surface holds
  which-path information. The fringes fade, as V = |⟨E₁|E₂⟩|.

Sonnentag & Hasselbach (PRL 98, 200402, 2007) flew electrons past a semiconducting
plate and saw the fringes fade. The fading grew with path separation and with
closeness to the plate, as decoherence theory predicts (LIT).

**What survives:** the charge is in two places as an *amplitude*, which does not
repel itself, and its field is in two places as an amplitude too. That is the
standard picture, reached using EM alone.

## What this means for a new equation

None of the ingredients yields a measurable difference from standard quantum
mechanics. M2 conflicts with data; M1 and M3 restate known physics. The same wall
as [WALL.md](WALL.md) §3 applies: a new equation needs a free parameter that
changes some number.

**The Planck scale.** The Planck scale is taken here as the place where the current
equations (general relativity plus quantum field theory) stop giving finite,
trustworthy answers. It is not assumed to be a breakdown of reality. Nothing above
depends on Planck-scale physics.

**Where gravity enters without exotic physics.** Gravity-induced entanglement
(Bose et al. 2017; Marletto–Vedral 2017): put two masses each into a two-path
superposition and let only ordinary Newtonian gravity act between them. The
standard prediction is a path-dependent phase Δφ = G m² t / (ħ d), which entangles
the masses if gravity's field is in two places as an amplitude, just as T5 shows
for the electron's EM field. If gravity's field is instead a single classical
average (the gravitational version of the split charge), the masses never
entangle. This experiment is being developed, and it is the gravity version of T5.
