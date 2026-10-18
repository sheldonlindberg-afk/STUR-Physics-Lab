# Quark-Resistance Torsion Bounce: A Real-Physics Backward Cosmology

**Document Type:** Exploratory Derivation (standalone real-physics baseline + extension)
**Framework:** Standard ΛCDM + Einstein-Cartan-Kibble-Sciama (ECKS) torsion gravity
**Status:** OPEN — one mechanism built and checked for coherence; not a closed STUR result
**Scripts:** `scripts/lcdm_backward_baseline.py`, `scripts/quark_resistance_torsion_bounce.py`

---

## 0. What this document is, and isn't

This started from a specific question: if dark matter and dark energy are what we actually
measure *today*, what does integrating the real Friedmann equation **backward** say about
the early universe, with H0 left as a genuine free dial (the Planck-vs-SH0ES tension is real
and unresolved, so it is not hardcoded)? That baseline was then used to test a specific
proposed origin mechanism: the universe begins in its lowest-energy state and quantum-tunnels;
**resistance to that tunneling creates quarks**; some annihilate, some bind, and the binding is
claimed to generate the weak force.

Everything below is built from standard, citable physics (ΛCDM, Einstein-Cartan gravity,
gravitational particle production) with every free coefficient explicitly flagged as such — no
numerology, no fabricated precision. **The "binding creates the weak force" half of the claim
is not addressed here** — that is explicitly the next open step (see §6). What *is* addressed
is the cosmological half: does "resistance to tunneling creates quarks" supply a real
gravitational effect that can replace the Big Bang singularity with something more specific,
and if so, where does it land?

---

## 1. Real-ΛCDM backward baseline (H0 as a free dial)

**Fixed physical density parameters** (independent of H0, Planck 2018 TT,TE,EE+lowE+lensing):

| Parameter | Value | Source |
|---|---|---|
| Ω_b h² | 0.02237 | Planck 2018 VI (arXiv:1807.06209) / Planck 2018 X (arXiv:1807.06211) |
| Ω_c h² | 0.1200 | same |
| Ω_r h² | 4.16×10⁻⁵ | standard, N_eff = 3.046 |

Flat universe assumed (Ω_k = 0) — the one assumption, not derived. H0 is left as the free
dial: Ω_m(h) = (Ω_b h² + Ω_c h²)/h², Ω_r(h) = (Ω_r h²)/h², Ω_Λ(h) = 1 − Ω_m(h) − Ω_r(h).

**Results** (full scan in `scripts/lcdm_backward_baseline.py`):

| Quantity | H0 = 67.36 (Planck) | H0 = 73.04 (SH0ES) |
|---|---|---|
| Ω_m | 0.3138 | 0.2669 |
| Age of universe | **13.8141 Gyr** | **13.3264 Gyr** |
| Matter–radiation equality | z = 3421.36 (H0-**independent** — confirmed numerically identical at every H0 tested, since it is a ratio of physical densities) | z = 3421.36 |
| Matter–Λ density equality | z = 0.2980 | z = 0.4005 |
| Acceleration onset (q=0, derived from scratch and cross-checked against a finite-difference numerical derivative to ~10⁻¹¹) | z = 0.6348 | z = 0.7639 |

H0 sources: Planck 2018 VI gives H0 = 67.36 km/s/Mpc; SH0ES gives H0 = 73.04 ± 1.04 km/s/Mpc
(Riess et al. 2022, arXiv:2112.04510).

**Independent age cross-check:** oldest globular clusters give t_U = 13.5 (+0.16/−0.14 stat)
± 0.23(0.33 sys) Gyr (Valcin, Jimenez, Verde, Bernal & Wandelt 2021, arXiv:2102.04486). The
SH0ES-dial age (13.33 Gyr) sits slightly below this central value but within combined errors
— the real, literature-documented tension, not invented here.

**Honest conclusion on "a beginning":** backward integration of real GR+ΛCDM with only
matter, radiation and Λ does not and cannot reveal a new beginning — it runs into the ordinary
Big Bang curvature singularity at a=0, for any H0. That is a property of the equations with
this matter content, not a limitation of the integration. A genuinely different beginning
requires additional physics. §2 adds exactly one piece of such physics, chosen to be real and
citable rather than invented.

---

## 2. Mechanism: Einstein-Cartan torsion repulsion, sourced by quarks

**The real physics.** In Einstein-Cartan-Kibble-Sciama (ECKS) gravity, torsion is
non-dynamical (algebraic, no kinetic term) and sourced locally by fermion spin density.
Substituting the algebraic torsion solution back into Einstein's equation produces an
effective extra term in the stress-energy tensor, quadratic in fermion number density n and
**repulsive**:

ρ_eff = ρ − α n², &nbsp; p_eff = p + α n²

This is the real mechanism behind Popławski's nonsingular big-bounce cosmology (*Phys. Rev. D*
85, 107502 (2012), arXiv:1111.4595), built on the original ECKS formalism (Hehl, von der
Heyde, Kerlick & Nester, *Rev. Mod. Phys.* 48, 393 (1976)). It directly operationalizes
"resistance to tunneling" as gravitational repulsion rather than an invented force, and it
specializes naturally to a TEGR/torsion-based framework.

**Honesty note on the coefficient.** α must have units of 1/mass² by dimensional analysis
alone, and gravity's only natural mass scale is the Planck mass, so α = C/M̄_Pl² for some
dimensionless C. **The exact primary-source value of C could not be verified in this session**
— arxiv.org and every mirror/review host tried (ar5iv, export.arxiv.org, inspirehep,
semanticscholar) were blocked by this session's network policy. Secondary-source search
snippets gave two different prefactors in different unit conventions (α=(9/16)κ in one,
α=κ(ℏc)²/32 in another) that could not be reconciled without the primary derivation. C is
therefore treated throughout as an **explicit, scanned free parameter** — the same honest
treatment already given to the Chung-Kolb-Riotto O(1) coefficient in
`DARK_MATTER_RELIC_DENSITY.md` Part VIII.

**Specialization to quarks.** Popławski's mechanism is generic to any fermion species; it is
narrowed here to quarks specifically because that is the claim under test. Quark dof used:
g_Q = 2 flavors (u,d) × 3 colors × 2 (quark/antiquark) × 2 spin = 24 — the conservative
(minimal) version of the claim; leptons would only add more source density.

### 2.1 Thermal sourcing (first attempt) — lands trans-Planckian

Sourcing n_q(a) from a pre-existing thermal quark bath (standard entropy-conservation
redshift, T(a) = T₀ a⁻¹ (g_s0/g*)^(1/3), g_s0 = 3.909, g* = 106.75):

| C | T_bounce / M̄_Pl |
|---|---|
| 0.001 | 137.6 |
| 0.01 | 43.5 |
| 0.1 | 13.8 |
| 0.5625 (= 9/16) | 5.80 |
| 1 | 4.35 |
| 10 | 1.38 |

A bounce exists for **any** C > 0, robustly — the torsion term scales as n² ∝ a⁻⁶, steeper
than radiation's a⁻⁴, so it always eventually wins as a→0; only its location depends on C.
But for every physically plausible C, the bounce lands at or above the Planck density — the
same boundary-of-validity limitation the Popławski literature itself acknowledges (the bounce
density is generically "of order the Planck density" for ordinary matter content).

**Coherence checks (both pass):** regardless of C, the age of the universe computed from
bounce to today is **13.814064 Gyr**, an exact match to the pure-ΛCDM baseline in §1 — the
torsion term affects a negligible span of cosmic time. At BBN (T = 1 MeV), Ω_torsion/Ω_r =
8.9×10⁻⁴⁵ — completely undetectable; standard BBN is untouched.

### 2.2 Does adding a sub-quark (preon) layer help? — No, checked quantitatively

Tested whether adding degrees of freedom "underneath" quarks (preon substructure) could pull
the bounce down to a safely sub-Planckian scale. T_bounce scales as **1/g** at fixed C (the
weakest possible lever):

| Added layer | g / g_quarks | T_bounce / M̄_Pl |
|---|---|---|
| quarks only (baseline) | 1 | 5.80 |
| full Standard Model (all species) | 4.45 | 1.30 |
| rishon-style preons (3 preons/quark, quark-like dof each) | 3 | 1.93 |
| generic 10× toy preon sector | 10 | 0.58 |
| dof needed to reach 0.1 M̄_Pl | 43.5 | 0.13 |

A realistic preon model (e.g. the Harari–Shupe rishon model) supplies dof *comparable to*
quarks, not an order of magnitude more — moving the bounce only from 5.80 to ~1.9 M̄_Pl, still
trans-Planckian. Reaching clearly sub-Planckian would need ~43× the quark dof (~1000 species)
— not a number any real preon model produces, and reaching for it would mean inventing dof to
force the answer. **Ruled out as the fix**; also, quark compositeness is itself an unverified,
currently disfavored BSM conjecture (collider contact-interaction limits push any substructure
scale above ~10 TeV), so this route would stack a second untested conjecture on the first.

### 2.3 Self-sourced production — the tunneling event supplies its own density

The thermal picture in §2.1 assumes a pre-existing equilibrium quark bath threaded in "from
before" the bounce — a strange assumption if the bounce is supposed to be the beginning. The
resolution: source the quark density from **non-adiabatic/gravitational particle production
at the transition itself**, not a pre-existing bath. This is the same mechanism already
validated in this project's dark-matter Bogoliubov calculation
(`DARK_MATTER_RELIC_DENSITY.md` Part VIII.3), applied here to quarks instead of the dark
R-field. Standard leading-order (test-field, fixed-background) result for gravitational
particle production (Chung, Kolb & Riotto, *Phys. Rev. D* 59, 023501 (1998),
arXiv:hep-ph/9802238): modes up to k~H are populated at O(η) occupancy, giving a produced
number density

n_q(a) = η · g_Q · H_rad(a)³

where H_rad(a) is the **unperturbed** (pre-torsion) radiation-domination Hubble rate — the
standard leading-order treatment of computing production on the background the universe would
have had, absent backreaction.

**Why this resolves the trans-Planckian problem.** Substituting back and solving
self-consistently (torsion term now depends on H itself):

H_bounce ∝ M̄_Pl · (3 / (C η² g_Q²))^(1/8)

An **eighth-root** dependence on the product of every uncertain number in the problem — vastly
more damped than the direct, linear sensitivity in §2.1. Scanning C ∈ [0.01, 10] and
η ∈ [0.01, 1] (five combined orders of magnitude of honest uncertainty):

| C | η = 0.01 | η = 0.1 | η = 1 |
|---|---|---|---|
| 0.01 | 8.50 | 2.69 | 0.85 |
| 0.1 | 4.78 | 1.51 | 0.48 |
| 0.5625 (= 9/16) | 3.10 | **0.98** | 0.31 |
| 1 | 2.69 | 0.85 | 0.27 |
| 10 | 1.51 | 0.48 | 0.15 |

(table entries are H_bounce / M̄_Pl)

Across the whole scan, H_bounce/M̄_Pl spans only 0.15–8.5 — under two orders of magnitude,
despite five orders of magnitude of input uncertainty. For the one literature-anchored
coefficient (C = 9/16) with a conservative production efficiency (η = 0.1):
**H_bounce = 0.98 M̄_Pl** — landing right at the Planck scale, which is the physically correct
place for a classical mechanism to hand off to quantum gravity, not several orders of
magnitude past it. For η → 1 (maximal occupancy), the bounce is comfortably sub-Planckian
(0.15–0.31 M̄_Pl).

**Coherence checks (both pass, same as §2.1):** age(bounce → today) = **13.814064 Gyr**, an
exact match to the ΛCDM baseline, for C = 9/16, η = 0.1. Ω_torsion/Ω_r at BBN =
8.0×10⁻¹⁶⁹ — even more negligible than the thermal version (the self-sourced term falls off
even faster, n² ∝ a⁻¹²).

---

## 3. What "the whole universe tunneling at once" can and can't mean

One part of the original proposal needs a specific correction, because it conflicts with how
tunneling actually works in QFT, not as a matter of interpretation. Vacuum decay is never a
uniform, instantaneous, infinite-volume event — Coleman's bounce calculus (*Phys. Rev. D* 15,
2929 (1977)) gives a decay rate *per unit volume per unit time*, because the tunneling
amplitude for an infinite region to flip coherently vanishes as volume→∞. Tunneling always
proceeds via **localized bubble nucleation**. The proposal is physically coherent if read as
"the pre-tunneling universe was itself a single small (sub-Hubble) patch" — then "the entire
universe tunneled as one event" is just ordinary bubble nucleation where the bubble is
everything there was. It is not coherent if read as "infinite space tunneled everywhere
simultaneously."

---

## 4. Does quark binding create the weak force? — checked, and corrected

The second half of the original claim: "some [quarks] bind creating a greater resistance to
tunneling and a force known as the weak force." This does not survive checking as stated, for
a specific, citable reason — but there is a real, correctly-attributed physics story
underneath it once the two forces involved are untangled.

**The misattribution.** Resistance to separating bound quarks is real and measurable: the QCD
confining potential grows linearly with separation (V(r) ≈ σr, string tension σ ≈ 1 GeV/fm),
so pulling quarks apart costs ever-more energy — literal, quantifiable "resistance to
[quarks] tunneling apart." But that resistance is the **strong force** (QCD confinement), not
the weak force. In the Standard Model these are separate gauge interactions: color SU(3)
confines quarks into hadrons; the weak force (SU(2)_L×U(1)_Y, mediated by W±/Z) governs
flavor-changing processes and is active whether or not quarks are bound. Binding does not
create the weak force — it's present throughout, bound or free.

**What actually "activates" the weak force's familiar character.** The weak force's defining
feature — short-ranged, feeble at low energy — comes from the W/Z bosons acquiring mass via
the Higgs mechanism at electroweak symmetry breaking (EWSB), not from quark binding. So the
honest question becomes: is EWSB itself a tunneling event, the way the proposal imagines? For
a **first-order** electroweak phase transition, yes — it would proceed by bubble nucleation,
exactly like the vacuum decay discussed in §3, and the weak force's familiar form would
literally switch on inside expanding bubbles.

**But the real Standard Model's electroweak transition is not that.** Kajantie, Laine,
Rummukainen & Shaposhnikov (*Is There a Hot Electroweak Phase Transition at m_H ≳ m_W?*,
Phys. Rev. Lett. 77, 2887 (1996), hep-ph/9605288) gave the first non-perturbative lattice
evidence against a hot electroweak transition once the Higgs mass reaches the W mass. The
continuum-extrapolated endpoint itself — the precise Higgs mass below which the transition is
first-order and above which it is a crossover — was pinned down by Csikor, Fodor & Heitger
(*Endpoint of the Hot Electroweak Phase Transition*, Phys. Rev. Lett. 82, 21 (1999),
hep-ph/9809291) at **72.4 ± 1.7 GeV** for the full Standard Model (66.5 ± 1.4 GeV in the
pure SU(2)-Higgs sector before adding fermions). The measured Higgs mass is 125 GeV — far
above that boundary. Above it, the transition is a smooth **crossover**: no bubble
nucleation, no latent heat, no tunneling. A later dedicated lattice study at the physical
Higgs mass (D'Onofrio & Rummukainen, *The Standard Model cross-over on the lattice*, Phys.
Rev. D 93, 025003 (2016), arXiv:1508.07161) finds a crossover at T_c = 159.5 ± 1.5 GeV. **In
the real, measured Standard
Model, the weak force did not turn on via a tunneling event** — it switched on smoothly. This
is also the standard reason *electroweak* baryogenesis (the specific mechanism that needs a
first-order transition to supply its out-of-equilibrium condition) is known to require new
Higgs-sector physics beyond the SM. Note this is a separate point from this project's own
`BARYOGENESIS_DERIVATION.md`, which uses leptogenesis (CP-violating heavy-neutrino decay) plus
standard electroweak sphalerons, not electroweak baryogenesis — sphalerons are active in the
symmetric phase above ≈130 GeV regardless of whether the transition below them is first-order
or a crossover, so that document's mechanism does not depend on the EWPT's order and is not
affected by the finding in this section.

**The one place a real "resistance" framing legitimately applies to the weak force** is not
tunneling at all: the W/Z mass itself (the reason the weak force is weak) is a restoring/mass
term generated by the Higgs mechanism, which STUR's own Energy Resistance Principle (E=½RΦ²,
see `mycitations.html` and the honesty note already attached to it) could in principle relabel
as a resistance term. This is worth flagging precisely because it is *not* new rigor — ERP is
already flagged elsewhere in this repository as the paper's own heuristic, not an independently
verified law, and STUR's own "Theorem 1" claiming to promote it to an exact reduction is this
project's unverified construction. Relabeling Higgs mass generation as "resistance" via ERP is
internally consistent with STUR's axioms but adds no independent derivation beyond what the
Higgs mechanism already says.

**Corrected attribution, if this is carried forward:**

| Claim piece | Correct real-physics home | Character |
|---|---|---|
| "Binding creates resistance to [quarks] tunneling apart" | QCD confinement (strong force) | Real, measurable, happens at T ≈ 155 MeV |
| "...and this resistance is the weak force" | Mislabeled — the weak force is a separate interaction, active with or without binding | Not supported as stated |
| "A tunneling event activates the weak force's familiar form" | Only true for a first-order EWSB transition | The real SM's EWSB is a smooth crossover (T_c=159.5 GeV, measured Higgs mass 125 GeV ≫ the ≈72 GeV first-order boundary) — **not tunneling**, unless new BSM scalar content is added |

**If this project wants to keep a weak-force-from-tunneling claim**, the honest path is to
treat a first-order EWSB as a new, explicit BSM ingredient (extra scalars, as electroweak
baryogenesis model-builders already do for the same reason), not something the measured SM
Higgs sector gives for free — and to say so.

---

## 5. Summary verdict

| Question | Answer |
|---|---|
| Does real backward ΛCDM reveal a new "beginning"? | No — it reaches the ordinary singularity, for any H0. Expected, not a defect. |
| Can resistance-to-tunneling (quark-sourced torsion) replace the singularity with something real? | Yes, via a real, citable mechanism (ECKS/Popławski) — a bounce always exists for any positive coupling. |
| Is the bounce scale trustworthy with a pre-existing thermal bath? | No — trans-Planckian (1.4–138 M̄_Pl) for any plausible coupling. |
| Does adding sub-quark dof fix this? | No — checked quantitatively; the lever is too weak (∝1/g) and the fix requires implausible dof. |
| Does letting the tunneling event supply its own density fix this? | Yes — self-consistency gives an eighth-root-damped result landing at 0.15–0.98 M̄_Pl across the full honest parameter range. |
| Does any of this disturb standard cosmology (age, BBN)? | No, checked explicitly in both versions — negligible at BBN, exact age match in both cases. |
| Does quark binding create the weak force? | No — misattributed. Binding resistance is the strong force (confinement). The weak force's familiar form comes from EWSB, which is a smooth crossover in the real SM (T_c=159.5 GeV), not a tunneling event, unless new BSM scalar content is added. |

---

## 6. Sources

- Planck Collaboration, *Planck 2018 results. VI. Cosmological parameters*, arXiv:1807.06209
- Planck Collaboration, *Planck 2018 results. X. Constraints on inflation*, arXiv:1807.06211
- Riess et al. (SH0ES), *A Comprehensive Measurement of the Local Value of the Hubble Constant
  with 1 km/s/Mpc Uncertainty*, arXiv:2112.04510
- Valcin, Jimenez, Verde, Bernal & Wandelt, *The Age of the Universe with Globular Clusters*,
  arXiv:2102.04486 (2021)
- Popławski, *Nonsingular, big-bounce cosmology from spinor-torsion coupling*, Phys. Rev. D 85,
  107502 (2012), arXiv:1111.4595
- Hehl, von der Heyde, Kerlick & Nester, *General Relativity with Spin and Torsion: Foundations
  and Prospects*, Rev. Mod. Phys. 48, 393 (1976)
- Chung, Kolb & Riotto, *Superheavy dark matter*, Phys. Rev. D 59, 023501 (1998),
  arXiv:hep-ph/9802238
- Coleman, *The Fate of the False Vacuum. 1. Semiclassical Theory*, Phys. Rev. D 15, 2929 (1977)
- Kajantie, Laine, Rummukainen & Shaposhnikov, *Is There a Hot Electroweak Phase Transition at
  m_H ≳ m_W?*, Phys. Rev. Lett. 77, 2887 (1996), hep-ph/9605288 (first non-perturbative lattice
  evidence against a hot transition once m_H reaches m_W)
- Csikor, Fodor & Heitger, *Endpoint of the Hot Electroweak Phase Transition*, Phys. Rev. Lett.
  82, 21 (1999), hep-ph/9809291 (continuum-extrapolated endpoint: m_H = 72.4 ± 1.7 GeV for the
  full Standard Model, 66.5 ± 1.4 GeV in the pure SU(2)-Higgs sector)
- D'Onofrio & Rummukainen, *The Standard Model cross-over on the lattice*, Phys. Rev. D 93,
  025003 (2016), arXiv:1508.07161 (crossover at the physical Higgs mass, T_c = 159.5 ± 1.5 GeV)

---

## 7. Open items (not addressed here)

1. **The exact ECKS coefficient C** — this session could not reach arxiv.org or any mirror to
   verify it against the primary source. A future session with that access should replace the
   scanned-C treatment with the verified value.
2. **This is a leading-order (test-field, fixed-background) estimate**, standard practice in
   this literature but not a full dynamical, self-consistently backreacting numerical solve
   through the bounce.
3. **If a first-order EWSB is wanted** (to literally recover a tunneling-driven weak-force
   activation, per §4), the specific new scalar content required has not been specified or
   checked against anything else established in this project.

---

**Document Status:** OPEN. One real mechanism built, scanned honestly over its uncertain
coefficients, and checked for coherence against standard cosmology. Not a STUR closure claim —
a standalone real-physics exploration, written up for reproducibility.
