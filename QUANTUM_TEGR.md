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
  Done in section 6, which narrows this gap.
- This is a research-level problem in quantum field theory.

## 6. Full-text and first-order search (follow-up to section 5)

**Queries (INSPIRE):**
- abstracts: "edge modes" + (tetrad, coframe, first-order, Holst or Einstein–Cartan):
  21 hits, 5 on gravity;
- abstracts: torsion + "entanglement entropy": 7 hits, none on TEGR;
- full text: teleparallel + "entanglement entropy": 61 hits. Most are cosmology papers
  that mention both words; the relevant ones are listed below;
- full text: Weitzenböck + "entanglement entropy": 2 hits;
- every paper citing Freidel–Geiller–Pranzetti Part I that mentions teleparallel,
  Weitzenböck or entanglement entropy in its abstract: 15 hits;
- every paper citing Girelli–Qiu–Zwikel: 1 hit.

**Full texts read:** Freidel–Geiller–Pranzetti Parts I and II (searched for
"teleparallel" and "Weitzenböck"), and Girelli–Qiu–Zwikel.

**What exists:**

| Work | Content | Relation to the gap |
|---|---|---|
| Freidel, Geiller, Pranzetti, *Edge modes of gravity* I and II, [2006.12527](https://arxiv.org/abs/2006.12527), [2007.03563](https://arxiv.org/abs/2007.03563) | Formulations of gravity, metric and tetrad, share the bulk symplectic structure but differ at the corner, and so give inequivalent representations of the corner symmetry algebra. The tetrad formulation adds local Lorentz charges | **The framework the question belongs to.** Their texts don't mention teleparallel gravity or the Weitzenböck connection (INSPIRE's full-text hit on "teleparallel" for these papers is spurious) |
| Langenscheidt and Oriti, [2408.01809](https://arxiv.org/abs/2408.01809); Langenscheidt, [2505.16026](https://arxiv.org/abs/2505.16026) | Edge modes and corner charges of 4D tetrad gravity from tetrad-shift symmetries; a Poincaré-like corner algebra | Tetrad (Einstein–Cartan) variables, not teleparallel |
| Girelli, Qiu, Zwikel, *Teleparallel gravity at null infinity*, [2412.14258](https://arxiv.org/abs/2412.14258) (PRD 2025), full text read | In TEGR the BMS Goldstone modes, which the metric formulation must add by hand, sit in the flat (Weitzenböck) connection. They read them as edge modes. Their conclusion: teleparallel gravity "could offer a promising framework for encoding a degenerate vacuum beyond the case of null infinity" | **Closest prior work.** Teleparallel edge modes, but at null infinity, with no entanglement entropy |
| Girelli, Osumanu, Wieland, [2101.05347](https://arxiv.org/abs/2101.05347); Dupuis, Girelli, Hrytseniak, Wieland, [2603.12100](https://arxiv.org/abs/2603.12100) (PRD 2026) | Boundary terms as canonical transformations; a non-Abelian teleparallel formulation; corner terms and charges across formulations, teleparallel included | Corner structure of teleparallel-type formulations; no entropy |
| Koivisto, [2209.14959](https://arxiv.org/abs/2209.14959) | Covariant phase space with boundaries | *Symmetric* teleparallel (STEGR), not TEGR |
| Hammad et al., [1912.08811](https://arxiv.org/abs/1912.08811) | Wald entropy in TEGR from the Noether charge; it comes out as a volume integral | Black-hole entropy, not entanglement entropy |
| Geiller and Jai-akson, [1912.06025](https://arxiv.org/abs/1912.06025); Mukherjee, [2310.14690](https://arxiv.org/abs/2310.14690) | Edge-mode boundary actions and their contribution to entanglement entropy | General framework (Maxwell, metric gravity) |
| Ciambelli, Kowalski-Glikman, Varrin, [2507.16800](https://arxiv.org/abs/2507.16800); Varrin, [2610.37750](https://arxiv.org/abs/2610.37750) (2026) | Entanglement entropy of quantum corner states (2D, JT). Then: edge modes of Schwarzschild as **dynamical reference frames**; quantizing them gives the Bekenstein–Hawking entropy as entanglement entropy between the two exteriors, plus a logarithm | **The metric-variable version of the computation.** Not teleparallel |
| Solodukhin, *Newton constant, contact terms and entropy*, [1502.03758](https://arxiv.org/abs/1502.03758) | Contact terms of interaction mediators (vectors, gravitons) in entanglement entropy and the renormalized G | Background for Jacobson's identification (DERIVATION.md); mentions the Weitzenböck connection in passing |

**Assessment.** The gap is narrower than section 5 suggested, and sharper:
- Varrin (2026) gets A/4 as entanglement entropy from edge modes treated as quantum
  reference frames, in metric variables.
- Girelli, Qiu and Zwikel (2024) show that in TEGR the flat connection *is* such a
  reference-frame field, and that it carries edge-mode data, at null infinity.
- **Not found: anyone putting these together at a finite entangling surface or a
  bifurcate horizon.** In TEGR, does the flat connection supply the edge-mode frames
  that the metric formulation has to add, and does quantizing them give A/4 plus the
  same logarithm?

The question is well defined and current, and Girelli and collaborators point at it
themselves in their conclusion.

The classical part is within reach of this repository's code, and has been started:
[TEGR.md](TEGR.md), "Where the entropy sits" (`src/stur_tegr_corner.py`, K1–K5). With the
static frame, TEGR's Noether charge vanishes at the bifurcation surface and the corner
term carries all of the Wald entropy. With frames winding around the Euclidean time
circle, the tip term is (A/4)(1 + k/κ). So the frame decides where the entropy is booked.
Classically, the first law is now done too (K6). It is the same in TEGR and GR, the frame
drops out of it, and the frame only moves terms between the Noether charge and the
symplectic flux. So any role for the frame in the entropy has to come from quantizing it,
not from classical thermodynamics. The quantum part, quantizing the corner frames and computing the
entropy, is research-level.

## 7. Quantizing the frame: first step (`src/stur_tegr_frame.py`)

Classically the frame changes where the entropy is booked but not the first law
(TEGR.md K1–K6). So if the frame has a role in the entropy, it has to show up when it is
quantized. Before that, one needs the frame's classical phase space at an entangling
surface: what it is canonically conjugate to. That is computed here at linear order
around flat space, in the Weitzenböck gauge (ω = 0). The tetrad perturbation is split as
B = s + a: the symmetric part s is the metric perturbation (h = 2s), and the
antisymmetric part a is the linearized frame, a local Lorentz rotation.

| Step | Result | Status |
|---|---|---|
| Q1 | L(s + a) − L(s) has identically vanishing Euler–Lagrange derivatives (with a control that doesn't). The frame is pure gauge in the bulk | KNOWN; CHECK |
| Q2 | The frame's part of the symplectic current is divergence-free off shell, and equals ∂_νW^{μν} for a unique covariant corner 2-form W, bilinear in the two variations. W has no metric–metric part | CHECK |
| Q3 | On the plane t = const, x = 0: W^{tx} = (1/8π)[−δa₀₁∧δ(s₂₂ + s₃₃) + δa₀₂∧δB₁₂ + δa₀₃∧δB₁₃ − δa₁₂∧δB₀₂ − δa₁₃∧δB₀₃] | CHECK |
| Q4 | K5's nonlinear Euclidean result, re-expressed per unit area and per unit frame angle, has the same coefficient, 1/8π | consistency |

**Reading Q3.**
- a₀₁ = −η, where η is the rapidity of the frame's boost normal to the surface, and
  s₂₂ + s₃₃ = δ√σ is the linearized area density. So the corner form contains
  **(1/8πG)∫δη∧δ√σ: the frame's normal boost is canonically conjugate to area/8πG.**
  This is the pair Carlip and Teitelboim found in the metric Euclidean action, with the
  opening angle at the horizon in place of η ([gr-qc/9312002](https://arxiv.org/abs/gr-qc/9312002),
  CQG 12, 1699, 1995). It is also the pair Varrin quantizes to get the Bekenstein–Hawking
  entropy ([2610.37750](https://arxiv.org/abs/2610.37750)). In the metric formulation the
  angle has to be added as an extended-phase-space variable (Donnelly–Freidel). **In
  TEGR it is already there, as the frame.**
- The boosts and rotations that mix the normal with the tangent directions (a₀ᵢ, a₁ᵢ)
  pair with off-diagonal tetrad components.
- The rotation within the surface, a₂₃, pairs with nothing. It stays pure gauge even at
  the corner.

**Status.** The area–boost pairing is known in metric variables (Carlip–Teitelboim) and
in tetrad variables, where the area acts as a boost generator (Freidel and Perez,
[1507.02573](https://arxiv.org/abs/1507.02573); Freidel–Geiller–Pranzetti Part II). A
search of INSPIRE (teleparallel with Carlip–Teitelboim, with area and boost, and with
opening angle) found no statement of it for TEGR's frame. As before, not finding it
doesn't mean it hasn't been done.

**What this means for the quantum question.** At linear order, quantizing TEGR's frame
at an entangling surface means quantizing the pair (η, √σ/8πG) at each point of the
surface, plus the mixed modes. That is the structure from which Varrin obtains A/4 as
entanglement entropy. So the next step is concrete: check whether TEGR's corner algebra,
including the mixed modes, closes into the sl(2, ℝ) structure that Varrin's
construction uses, and whether the frame's boost is restricted the way his causal frames
are.

### The closure (Q5–Q7)

The linear frame–frame block of Q3, (1/8π)(δa₀₂∧δa₁₂ + δa₀₃∧δa₁₃), is the component along
the normal boost of the Lorentz commutator [ε₁, ε₂]. That is the shape of a
Kirillov–Kostant form, the canonical symplectic form on a coadjoint orbit. Q5–Q6 test
this beyond linear order.

| Step | Result | Status |
|---|---|---|
| Q5 | Flat metric, finite frame fields e = Λ(x), for SO(2,1) frames from three arbitrary functions and SO(3,1) frames from six: the exact symplectic current is ∂_νW^{μν} with **W^{μν} = (1/8π)[Λ⁻¹δ₁Λ, Λ⁻¹δ₂Λ]^{μν}**. Agreement 10⁻³⁴ (60-digit arithmetic, finite differences); the opposite sign fails at order 1 | CHECK |
| Q6 | The corner charges G_X = (1/8π)(Λ⁻¹XΛ)^{tx} generate the frame rotations (δG_X = Ω(δ_X, ·), to 10⁻³⁰). They **close exactly into the Lorentz algebra**, {G_X, G_Y} = G_[X,Y] (to 10⁻⁴², all 36 pairs). The stabilizer is {J₀₁, J₂₃}: the normal boost and the rotation within the surface, the two modes with no frame partner in Q3 | CHECK |
| Q7 | What the orbit quantizes to, and what entropy that gives | KNOWN representation theory |

**What closes, and into what.**
- In the pure-frame sector the corner phase space of TEGR's frame is a coadjoint orbit of
  the Lorentz group SO(3,1), through (1/8πG)·K_normal per unit area. Its charges form
  so(3,1) ≅ sl(2,ℂ). This matches the sl(2,ℂ) corner Lorentz charges that
  Freidel–Geiller–Pranzetti find in tetrad gravity (Part II).
- It contains sl(2,ℝ) ≅ so(2,1) subalgebras {K_normal, K_A, J_normal,A}, one for each
  tangent direction A.
- **This sl(2,ℝ) is not Varrin's.** His acts on the normal plane, i.e. normal-plane
  linear maps from the diffeomorphism edge modes, which include shears. The two share only
  the normal boost, the area pair of Q3.

**What it quantizes to (Q7).**
- A coadjoint orbit through a boost quantizes to principal-series representations, with
  the label fixed by the area.
- Varrin (eq. 4.14) gives the group Plancherel density for SL(2,ℝ): k tanh(πk), which
  grows linearly. Two powers of it give an edge entropy of order ln A, not A/4.
- Only the causal **semigroup** SL⁺(2,ℝ), with density k sinh(2πk) (his eq. 4.20), gives
  A/4. At A = 1000 (Planck units) that is 254.6 against A/4 = 250, the difference being
  his logarithmic terms; the group gives 6.0.
- His causal condition requires positive entries in null coordinates. **For Lorentz boosts
  it holds automatically**: a boost is diag(e^η, e^{−η}) there. So it imposes nothing on
  TEGR's frame.

**Conclusion of this step.** TEGR's frame supplies the boost–area pair, and its corner
charges close into the Lorentz algebra. On its own it does not supply the exponential
density of states that gives A/4. In Varrin's construction that comes from the
normal-plane maps beyond boosts, which are diffeomorphism edge modes and are the same in
TEGR and GR. So, at this level, quantizing the frame adds a logarithm, not the area law.

### Any metric (Q8)

Q8 repeats Q5 on an arbitrary curved background tetrad ē, with a finite frame on top,
E = Λ(x)·ē. The background is deliberately not a solution, because the identity holds off
shell. The frame part of the symplectic current is ∂_νW^{μν} with

  W^{μν} = (√−g/8π)[E⁻¹δ₁E, E⁻¹δ₂E]^μ_ρ g^{ρν}

(to 10⁻³⁴; control at order 0.1). On the surface t, x = const this is
W^{tx} = (1/16π) N_ab [θ₁, θ₂]^{ab}, and:
- **N = ⋆Σ_S** (to 10⁻⁶¹): N is the Hodge dual of the surface's area bivector,
  Σ^{ab} = e^a_y e^b_z − e^a_z e^b_y;
- **N·N = −2σ** (σ the determinant of the surface metric), so the orbit's radius is the
  area density;
- **N·⋆N = 0**: the bivector is simple.

So, for any metric, **the frame's corner phase space is the Lorentz coadjoint orbit through
⋆Σ_S/8πG**. This also settles the linear-order caveat about the orbit's radius. The
simplicity condition is the one imposed by hand in spin-foam models (B = ⋆(e∧e)); here
it comes out of the frame's corner form. In representation terms, simple orbits through a
boost correspond to the principal series of SL(2,ℂ) with one label fixed by the area and
the other zero.

**Caveats:**
- Q5, Q6 and Q8 vary the frame with the metric fixed. Joint variations of frame and
  metric are covered only at linear order (Q3).
- Q7 uses Varrin's construction and its normalization. Other quantizations of the orbit
  (other regularizations, or including discrete series) were not examined.
- Not examined either: the behaviour of W under linearized diffeomorphisms at the corner,
  and the full nonlinear corner form with a curved metric.

## 8. The logarithmic correction (`src/stur_tegr_logs.py`)

Quantized as a group, the frame adds a logarithm to the entropy (section 7, Q7). Is it
the physical one? Logarithmic corrections are universal. They come from the one-loop
determinants of the massless fields and from zero modes, so they don't depend on the
ultraviolet completion. Sen computes them for Schwarzschild in D = 4
([1205.0971](https://arxiv.org/abs/1205.0971), JHEP 04 (2013) 156).

**Benchmarks, quoted from the sources:**
- **Sen, eq. (1.2) and (1.5).** In the ensemble of rotation-singlet states per unit
  mass, ΔS = (C_local − 3) ln a, with
  C_local = (2n_S − 26n_V + 7n_F − (233/2)n_{3/2} + 424)/90. For pure gravity that is
  (77/45) ln a.
- **Sen, section 4.** SU(2) loop quantum gravity gives −2 ln a in the same ensemble.
- **Varrin, eqs. (4.20)–(4.24).** The edge term is 2⟨ln μ(k)⟩, with k ∝ A.
- **David and Mukherjee** ([2201.06043](https://arxiv.org/abs/2201.06043)). The graviton's
  edge sectors across a sphere in flat space give −16/3. This is a flat-space entanglement
  benchmark, not a black-hole ensemble.

**Computed here.** Varrin-type edge counting for each group the frame could be quantized
with, converted to Sen's ensemble. Converting from area-labelled to mass-labelled counting
adds +1·ln a: k = M², so the width in k at a fixed mass window is 2M δM. This is the same
conversion Sen uses for loop quantum gravity.

| Coefficient of ln a, Sen's singlet ensemble | Value |
|---|---|
| Sen, pure gravity (universal) | 77/45 = **1.711** |
| Sen, gravity + photon (the massless fields at black-hole scales) | 64/45 = **1.422** |
| SU(2) loop quantum gravity (Sen, section 4) | −2 |
| Edge counting, SO(1,1): the normal boost alone (spherical reduction) | 1 |
| Edge counting, SL(2,ℝ) ≅ so(2,1) (Q7) | 5 |
| Edge counting, SL(2,ℂ) ≅ so(3,1), simple principal series: the frame's full orbit (Q8) | 9 |
| Edge counting, Varrin's causal semigroup SL⁺(2,ℝ) | 5 |

The SL(2,ℂ) Plancherel density, ∝ (n² + ρ²) and so ∝ ρ² for the simple series, is the
Gelfand–Naimark result; the density |μ + iλ|² is checked against [2403.17180](https://arxiv.org/abs/2403.17180).

**What this shows.**
- The frame's logarithm depends on which group it is quantized with (1, 5 or 9). None of
  these equals the universal value.
- None of them depends on the matter content, which Sen's coefficient must, through the
  trace anomaly.
- So the frame's edge logarithm is construction-dependent and is not the physical log
  correction.
- Sen's coefficient comes from one-loop bulk determinants and zero modes, which are the
  same in TEGR and GR because they differ only by a boundary term. It stays the same in
  TEGR **provided the frame is treated as gauge in the path-integral measure**, i.e. its
  local Lorentz volume is divided out. Counting the frame's orbit states as physical would
  add to the universal coefficient, putting TEGR in conflict with a result that, in the
  extremal cases, matches microscopic string-theory counting (Sen's abstract).

**Conclusion.** Quantum mechanically, as classically (K6), the frame is bookkeeping. It
can't change the area law or the universal log, so TEGR's black-hole entropy is GR's.

**Caveats:**
- Varrin's construction is spherically reduced. Mapping it onto Sen's 4D singlet ensemble
  is a heuristic comparison, not a derivation in that ensemble.
- A first-principles test would compute TEGR's Euclidean one-loop partition function
  with the frame's measure written out explicitly.

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
3. **Research-level: 4D teleparallel edge modes and entanglement entropy (sections 5–6).**
   The search is done. The open question: does TEGR's flat connection supply the
   edge-mode reference frames at a bifurcate horizon, and does their quantization give
   A/4 (compare Varrin 2026, metric variables)? The classical part is done
   (TEGR.md K1–K6): the frame changes where the entropy is booked, but not the first law.
   The quantum part has started (section 7). The frame's normal boost is conjugate to
   area/8πG, and the frame's corner charges close exactly into the Lorentz algebra (a
   Kirillov–Kostant orbit). Quantized as a group, that gives ln A, not A/4: the area law
   needs the normal-plane edge modes, which are the same in TEGR and GR. Its logarithm is
   not the universal one either (section 8), so the frame must be gauge in the measure.
   TEGR's black-hole entropy is GR's.

Not recommended: a new version of quantum mechanics. Nothing in this search suggests
TEGR needs one; every quantum TEGR approach found uses standard quantum theory and asks
how to apply it to the tetrad.
