# Quantum teleparallel gravity: literature map

*November 2026. Research notes, not peer reviewed.* This page records a literature search
on quantizing teleparallel gravity (TEGR). Its purpose is to find out what has been done,
what is open, and where a project built on this repository's TEGR code could add
something, before any such project starts. Like [NOVELTY.md](NOVELTY.md), it lists what
was searched and what was found. **Most entries were read at abstract level only**; the
papers marked "to read" need their full text checked before anything is built on them.

**Tools:**
- web search;
- INSPIRE-HEP through its API. Note for future searches: in INSPIRE's query syntax `a`
  means *author*. Abstract searches need `abstracts.value:`.

## 0. The constraint any quantum TEGR has to face

TEGR's action differs from Einstein–Hilbert by a total divergence, T = −R + B (checked
symbolically in [`src/stur_tegr.py`](src/stur_tegr.py), E1). So:

- **Classically**, TEGR and GR have the same field equations and the same predictions.
- **In perturbative quantum gravity** (gravitons on a background), a boundary term doesn't
  change the propagator or the vertices. TEGR and GR give the same graviton physics. In
  particular, **TEGR can't change the predicted two-diamond (BMV) entanglement phase**
  in [GRAVITY_ENTANGLEMENT.md](GRAVITY_ENTANGLEMENT.md).
- **Where the two can differ** are the places that are sensitive to boundaries:
  - the Euclidean action and black-hole entropy;
  - entanglement entropy and edge modes on an entangling surface;
  - the choice of variables used in a non-perturbative quantization (the tetrad and the
    flat spin connection instead of the metric);
  - local Lorentz frame dependence, which TEGR has in its action but not in its field
    equations.

A quantum TEGR result is only interesting if it lives in one of those places.

## 1. Canonical and non-perturbative quantization

| Work | What it does | Status |
|---|---|---|
| Okołów, *ADM-like Hamiltonian formulation of gravity in the teleparallel geometry*, [1111.5498](https://arxiv.org/abs/1111.5498) (GRG 2013) | 3+1 Hamiltonian TEGR without gauge fixing, as a starting point for canonical quantization | Formulation only |
| Okołów and Świeżewski, [1111.5490](https://arxiv.org/abs/1111.5490) | The same programme tested first on a simpler theory with TEGR's configuration space, because TEGR's own Hamiltonian is complicated | Toy model |
| Okołów, *Kinematic quantum states for TEGR*, [1304.6492](https://arxiv.org/abs/1304.6492); *Variables suitable for constructing quantum states for TEGR*, [1305.4526](https://arxiv.org/abs/1305.4526), [1308.2104](https://arxiv.org/abs/1308.2104) | Kinematic Hilbert space (states before the constraints are imposed), in the style of loop quantum gravity | Kinematics only; dynamics open |
| Maluf and collaborators, *Hamiltonian formulation of the teleparallel description of GR* (about 300 citations) | The standard Hamiltonian TEGR; constraints and gravitational energy | Classical |
| Kanatchikov, *Towards precanonical quantum teleparallel gravity*, [2302.10695](https://arxiv.org/abs/2302.10695); *The De Donder–Weyl Hamiltonian formulation of TEGR and its quantization*, [2308.10052](https://arxiv.org/abs/2308.10052) | Quantizes TEGR in the De Donder–Weyl (precanonical) framework; a covariant Schrödinger equation for TEGR | A different quantization scheme; not tested against known physics |
| Delcamp, Freidel and Girelli, *Dual loop quantizations of 3d gravity*, [1803.03246](https://arxiv.org/abs/1803.03246); Shoshany, *Dual 2+1D loop quantum gravity on the edge*, [1904.06386](https://arxiv.org/abs/1904.06386); Dupuis, Freidel, Girelli and Osumanu, [2006.10105](https://arxiv.org/abs/2006.10105); Geiller, Goeller and Merino, [2011.09873](https://arxiv.org/abs/2011.09873) | **In 2+1 dimensions**, teleparallel gravity is the loop quantization "dual" to the usual one (curvature constraint first). Edge modes and boundary symmetries appear | **The most developed quantum teleparallel work found.** 3D only |
| Landry, *Conceptual and geometric foundations for a teleparallel approach to quantum gravity*, [2606.09592](https://arxiv.org/abs/2606.09592) (2026) | Compares teleparallel variables with loop quantum gravity's Ashtekar–Barbero variables; says a complete teleparallel quantum theory is open | Review/programme. **To read** |

**Assessment:** there's no complete quantum TEGR in 4D. Canonical work stops at kinematics.
The full dynamics (the Hamiltonian constraint) is open, as it is in loop quantum gravity.
This is a hard, long-standing problem; it isn't a realistic first project.

## 2. Quantum fields on a teleparallel background

| Work | What it does | Status |
|---|---|---|
| *Quantum fields in teleparallel gravity: renormalization at one-loop*, [2110.04325](https://arxiv.org/abs/2110.04325) (EPJC 82, 186, 2022) | Gravity kept classical; matter loops on a teleparallel background. Divergences can't be absorbed by the TEGR action alone; a modification involving the spin connection absorbs them at one loop without ghosts | One loop only; full renormalizability open |
| *Covariant spin-parity decomposition of the torsion and path integrals*, [2304.08360](https://arxiv.org/abs/2304.08360) | Torsion decomposition set up for path integrals | **To read** |
| *Teleparallel renormalization of gravitational action*, [2609.31444](https://arxiv.org/abs/2609.31444) (2026) | — | Found by INSPIRE, 0 citations. **To read** |
| *Quantum field theory on the tangent bundle*, [2610.35778](https://arxiv.org/abs/2610.35778) (2026) | — | Found by INSPIRE, 0 citations. **To read** |

## 3. Euclidean action and black-hole entropy

| Work | What it does | Relation to this repo |
|---|---|---|
| Krššák, van den Hoogen, Pereira, Böhmer and others, the reference-tetrad prescription (*Teleparallel theories of gravity: illuminating a fully invariant approach*, [1810.12932](https://arxiv.org/abs/1810.12932), review) | The spin connection is chosen so that the reference tetrad (M = 0) has zero torsion; this makes the action finite | Used in `src/stur_tegr.py` E3, which recovers S = A/4 from the boundary flux at infinity |
| *Noether charge and black hole entropy in teleparallel gravity*, [1912.08811](https://arxiv.org/abs/1912.08811) | Wald-type entropy in TEGR | Known; **to read** |
| *Reference frames and black hole thermodynamics*, [2309.06293](https://arxiv.org/abs/2309.06293) | Schwarzschild entropy A/4 from a torsional boundary term, with the tetrad entering through that term | Same result as E3 |
| Kuntz, Paci and Zanusso, *Euclidean actions and static black hole entropy in teleparallel theories*, [2410.04510](https://arxiv.org/abs/2410.04510) (abstract read) | The on-shell bulk integrals are themselves boundary terms; with asymptotic subtractions they give the Bekenstein–Gibbons–Hawking results. For the **torsion** theory (TEGR), a direct bulk computation agrees. For the **nonmetricity** theory (STEGR) it doesn't: with a fiducial reference frame the partition function vanishes | **Agrees with E3.** The vanishing partition function is a STEGR problem, not a TEGR one |
| Beltrán Jiménez and Koivisto, *Euclidean teleparallel relativity and black hole partition functions*, [2412.13946](https://arxiv.org/abs/2412.13946) (abstract read) | A canonical teleparallel reformulation reproduces the black-hole partition function **without subtractions**, with or without charge or a cosmological constant. A quasilocal prescription uses only the horizon boundary term | Agrees with E3, and goes further (charged, Λ ≠ 0, horizon-only) |

**Assessment:** black-hole entropy and the partition function in TEGR are known and
agree with GR, for several prescriptions. E3 in `src/stur_tegr.py` is a recomputation of
this. [TEGR.md](TEGR.md) now cites 2410.04510 and 2412.13946 for it, and E3b extends the
check to Reissner–Nordström: the flux at infinity gives βM/2 and the flux at the horizon
tip gives A/4 for every static horizon. Nothing new is left here at the semiclassical
level.

## 4. Modified teleparallel theories (f(T)) and their degrees of freedom

Not quantum, but anyone quantizing teleparallel gravity meets this first:
- f(T) breaks local Lorentz invariance and gains extra modes: Li, Sotiriou and Barrow,
  *f(T) gravity and local Lorentz invariance*, [1010.1041](https://arxiv.org/abs/1010.1041).
- The count of extra modes was reported as three, then as one
  ([1903.06774](https://arxiv.org/abs/1903.06774)). The review
  [2106.13793](https://arxiv.org/abs/2106.13793) (707 citations) says the number is
  still being investigated.
- Around flat FLRW and maximally symmetric backgrounds, the extra modes have vanishing
  kinetic terms at quadratic order: a strong-coupling problem, whose status is still
  debated (reviewed in [2106.13793](https://arxiv.org/abs/2106.13793)).

TEGR itself (f(T) = T) is free of this: its extra term is a pure divergence, so it
keeps local Lorentz invariance in its field equations.

## 5. Entanglement entropy, edge modes and teleparallel gravity in 4D

**Queries (INSPIRE):**
- abstracts: teleparallel + "entanglement entropy": **0 hits**;
- abstracts: teleparallel + "edge modes": 1 hit, *At the corner of space and time*
  ([1912.02922](https://arxiv.org/abs/1912.02922)), a discretization of first-order GR
  with torsion tracked in holonomies, leading to spin networks with edge modes;
- abstracts: teleparallel + "entanglement": 1 hit, a CPT/Lorentz meeting proceedings;
- full text: teleparallel + "entanglement entropy" + "edge modes": 3 hits, all in 2+1D
  (section 1).

**Web search:** found the general edge-mode literature but no work linking it to 4D
teleparallel gravity:
- *Entanglement entropy of electromagnetic edge modes*, Donnelly and Wall,
  [1412.1895](https://arxiv.org/abs/1412.1895): edge modes explain a contact term in
  Maxwell entanglement entropy.
- *Entanglement entropy of gravitational edge modes*, [2201.06043](https://arxiv.org/abs/2201.06043):
  gravitons have d − 2 edge modes.
- *Entanglement entropy and the boundary action of edge modes*, [2310.14690](https://arxiv.org/abs/2310.14690).

**Assessment:** in 4D, nothing found on the entanglement entropy or edge modes of
teleparallel gravity. This is the gap that fits section 0: entanglement entropy across a
surface is exactly where a boundary term can matter. It also connects directly to this
repository's area-law page and Jacobson's argument ([DERIVATION.md](DERIVATION.md)). In
Donnelly and Wall's Maxwell case, edge modes produce a known contact term; the
teleparallel question would be whether TEGR's surface term
∂_μ(e T^μ) produces the same edge-mode contribution as GR's, or a different one.

**Caveats:**
- "Not found" in abstracts doesn't mean not done. Gravitational edge-mode papers often
  work in first-order (tetrad) variables without using the word "teleparallel". A
  full-text search under first-order terms (tetrad, coframe, Holst action) is needed.
- This is a research-level problem in quantum field theory. It needs an expert
  collaborator, or at least an expert reader.

## What this suggests

In order of size:

1. **Done: cite the literature for E3 and extend it (section 3).** TEGR.md cites
   2410.04510 and 2412.13946, and E3b (`src/stur_tegr.py`, pinned in `tests/test_tegr.py`)
   adds the Reissner–Nordström case and the horizon term. Recomputation, not new physics.
2. **Done in part: a worked example in 2+1D.** Notebook
   [05](notebooks/05_teleparallel_3d_quantum.ipynb) and `src/stur_tegr3d.py` reproduce the
   3D TEGR identity, the Ponzano–Regge asymptotics and the 2–3 move. They do not
   reproduce the dual (flat-first) construction itself; that is the natural next step
   for the notebook (its exercise 3).
3. **Research-level: 4D teleparallel edge modes and entanglement entropy (section 5).**
   The only gap found. It needs the first-order full-text search first, and then expert
   input.

Not recommended: a new version of quantum mechanics. Nothing in this search suggests
TEGR needs one; every quantum TEGR approach found uses standard quantum theory and asks
how to apply it to the tetrad.
