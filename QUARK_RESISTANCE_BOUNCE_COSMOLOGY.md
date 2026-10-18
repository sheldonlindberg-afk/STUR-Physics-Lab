# Quark-Resistance Torsion Bounce: A Real-Physics Backward Cosmology

**Document Type:** Exploratory Derivation (standalone real-physics baseline + extension)
**Framework:** Standard ΛCDM + Einstein-Cartan-Kibble-Sciama (ECKS) torsion gravity
**Status:** OPEN — negative result. Every version of the torsion-bounce mechanism tried here
(thermal-sourced, preon-layer-patched, self-sourced with an assumed production efficiency,
and self-sourced with an actually *computed* production efficiency) lands trans-Planckian.
Not a closed STUR result; see §5 for the full verdict table.
**Scripts:** `scripts/lcdm_backward_baseline.py`, `scripts/quark_resistance_torsion_bounce.py`,
`scripts/quark_bogoliubov_bounce.py`

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
gravitational particle production, lattice electroweak-transition results) with every free
coefficient explicitly flagged as such — no numerology, no fabricated precision. Both halves
of the original claim are checked: does "resistance to tunneling creates quarks" supply a real
gravitational effect that can replace the Big Bang singularity with something more specific
(§1–§3, answer: not quite — real mechanism, wrong magnitude by ~100×), and does "binding
creates the weak force" survive as stated (§4, answer: no, misattributed, corrected)? The
remaining open items (what would still need to change for either half to actually close) are
listed in §7.

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

**On dark energy specifically — Ω_Λ is taken as measured throughout this document, not
derived or explained.** The question that opened this whole thread was framed as "start with
DM and DE and work backwards"; everything from here on is about DM's side of that (the early
universe, via the DM-sourced bounce in §2). A real, first-principles dark-energy *production*
mechanism is not attempted, and should not be expected from this document — the cosmological
constant problem (why vacuum energy is ~10¹²³ times smaller than the naive QFT estimate) is
one of the most famous open problems in physics, not something to casually resolve as a side
effect of a bounce calculation. For the record: this project has its own existing, separately
documented attempt at this (`COSMOLOGICAL_CONSTANT_COMPLETE_DERIVATION.md`, claimed status
"SOLVED" in `OPEN_PROBLEMS_ROADMAP.md` OP-5, Λ_residual = 3.15×10⁻⁴⁷ GeV⁴, a 10.8% deviation
from the observed 2.846×10⁻⁴⁷ GeV⁴, via a ∞₃ discrete-gauge Ward identity argument). That
derivation was **not re-audited as part of this document** — it uses an entirely different
mechanism (discrete gauge symmetry breaking, not torsion or tunneling) and has no established
connection to the bounce mechanism in §2. Citing it here only to be transparent about what
else exists in this project, not as a verification, and not as a connection — there isn't one.

---

## 2. Mechanism: Einstein-Cartan torsion repulsion, sourced by quarks

**The real physics.** In Einstein-Cartan-Kibble-Sciama (ECKS) gravity, torsion is
non-dynamical (algebraic, no kinetic term) and sourced locally by fermion spin density.
Substituting the algebraic torsion solution back into Einstein's equation produces an
effective extra term in the stress-energy tensor, quadratic in fermion number density n and
**repulsive**:

ρ_eff = ρ − α n², &nbsp; p_eff = p − α n²

(**correction**: an earlier version of this document wrote p_eff = p + α n² — opposite sign.
That was wrong, caught on a later audit pass; see the honesty note below for the verified
form. It never affected any computed number here, because the bounce-location code only ever
uses the ρ_eff/H² equation, not p_eff — confirmed by grep against the script.)

This is the real mechanism behind Popławski's nonsingular big-bounce cosmology (*Phys. Rev. D*
85, 107502 (2012), arXiv:1111.4595), built on the original ECKS formalism (Hehl, von der
Heyde, Kerlick & Nester, *Rev. Mod. Phys.* 48, 393 (1976)). It directly operationalizes
"resistance to tunneling" as gravitational repulsion rather than an invented force, and it
specializes naturally to a TEGR/torsion-based framework.

**Honesty note on the coefficient — updated with a better-anchored estimate.** α must have
units of 1/mass² by dimensional analysis alone, and gravity's only natural mass scale is the
Planck mass, so α = C/M̄_Pl² for some dimensionless C. **The primary-source papers themselves
remain unreachable in this session** — not just arxiv.org, but every external host tried
(ar5iv, export.arxiv.org, inspirehep, semanticscholar, and even unrelated university/personal
pages like math.newhaven.edu) returns a proxy-level connection refusal, confirming this is a
session-wide network policy, not an arxiv-specific block. What changed on a later pass:
targeted search queries surfaced a **self-consistent, cross-checked** equation rather than a
bare assertion. Unger & Popławski (*Big Bounce and Closed Universe from Spin and Torsion*,
ApJ 870, 78 (2019), arXiv:1808.08327) give the general spin-fluid form ε_eff = ε − κs²/4,
p_eff = p − κs²/4 (s = spin density; same-sign correction to both, as corrected above), and
for an **unpolarized** fermion gas s² = (1/8)(ℏcn)². Substituting: κs²/4 =
κ(ℏc)²n²/32 = αn² with **α = κ(ℏc)²/32**, i.e. **C = 1/32 ≈ 0.03125** (using κ=8πG=1/M̄_Pl² in
natural units). This substitution is arithmetically verified here, not just quoted — it is
why this value is trusted more than the other secondary-source figure found earlier
(α=(9/16)κ, from arXiv:1111.4595, a different paper using "a different spin-averaging
convention" per the search's own description — the two are not necessarily in conflict, but
this session cannot read either primary derivation to confirm which applies). C is still
reported as a **range, not a single verified number** — C=1/32 is the best-anchored current
estimate, C=9/16 the alternative-convention figure, both explicitly scanned below alongside
the same honest treatment already given to the Chung-Kolb-Riotto O(1) coefficient in
`DARK_MATTER_RELIC_DENSITY.md` Part VIII. Because of the self-sourced mechanism's fourth-root
damping (§2.3), the 18× spread between these two values only shifts H_bounce by
18^(1/4) ≈ 2.1× — it does not change the qualitative conclusion either way.

**Specialization to quarks.** Popławski's mechanism is generic to any fermion species; it is
narrowed here to quarks specifically because that is the claim under test. Quark dof used:
g_Q = 2 flavors (u,d) × 3 colors × 2 (quark/antiquark) × 2 spin = 24 — the conservative
(minimal) version of the claim. Broadening to all 3 generations of SM fermions (quarks +
charged leptons + neutrinos, g=90 total, the standard fermionic dof behind g*=106.75) was
checked explicitly using the computed η from §2.4 (which is species-independent for an
exactly massless fermion, since the mode equation never references flavor or color — only the
overall dof count g enters): H_bounce ∝ g^(−1/2), so g=90 instead of g=24 only buys a factor
of √(90/24) ≈ 1.94. At C=9/16 that moves H_bounce from 101 to 52 M̄_Pl; at C=1/32, from 207 to
107 M̄_Pl. Still deeply trans-Planckian either way — broadening the source species is the same
weak lever that already failed for the preon-layer idea in §2.2, for the same structural
reason (a square/fourth-root dependence on dof, not linear).

**Checked for a connection to STUR's own established parameters — none found, and one
important distinction to avoid.** Searched this repository for any of the numbers used above
(C=1/32, 9/16; g_Q=24; η_computed≈9.5×10⁻⁶; H_bounce≈100–207 M̄_Pl) against STUR's own
established dimensionless constants (κ=2.430, σ=0.862, α_eff=1.480, λ_chrono=e^(1/π)≈1.376,
κ_q=2.417, κ_l=2.367, and others). No genuine match exists — the one numerical near-miss found
(α_GUT~1/24 at the GUT scale, in `ABSOLUTE_MASS_DERIVATION.md`) is a coupling constant at an
unrelated energy scale, not a degrees-of-freedom count, and treating it as a connection would
be exactly the kind of forced numerology this project has flagged and rejected elsewhere
(e.g. the chronomagnetics triangle, the δ_CP automorphism). Reported here as a clean null
result, not a near-miss. There is, however, a conceptual distinction worth making explicitly:
STUR's own first axiom is TEGR (gravity as torsion, not curvature) — superficially resonant
with this document's torsion-based mechanism, but **not the same thing**. TEGR is a
*reformulation* of ordinary GR (same predictions, same singularities, by construction — the
torsion there is a geometric re-encoding of curvature, not a new physical effect). The
Einstein-Cartan-Kibble-Sciama torsion used in this document is a genuine *extension* beyond
GR, sourced by fermion spin density, that changes physical predictions at high density (that
is the entire point of the bounce). STUR's TEGR axiom, taken on its own, would **not** by
itself produce this bounce mechanism — ECKS spin-torsion coupling is an additional ingredient
this document imports from outside STUR's stated axioms, not a consequence already contained
in them. Conflating the two kinds of "torsion" would be a mistake, not a discovery.

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

**Why this resolves the trans-Planckian problem.** At the bounce, the torsion term balances
the radiation term: C η² g_Q² H_rad⁶ / (3 H0² M̄_Pl⁴) = H_rad²/H0² (using Ω_r(a) =
H_rad(a)²/H0² at this order). The H0 and a-dependence cancel exactly, leaving a closed
equation for H_rad itself:

C η² g_Q² H_rad⁴ = 3 M̄_Pl⁴ &nbsp;⟹&nbsp; **H_bounce = M̄_Pl · (3 / (C η² g_Q²))^(1/4)**

A **fourth-root** dependence on the product of every uncertain number in the problem — still
far more damped than the direct, linear sensitivity in §2.1, though less dramatic than an
earlier draft of this derivation claimed (an eighth-root dependence was written down first and
is wrong: that exponent belongs to how the bounce *scale factor* a_bounce depends on these
parameters, not to H_bounce; re-deriving and then checking directly against the numerical scan
below — e.g. holding C fixed and comparing η=0.01 to η=1, a 10⁴× swing in η² should move
H_bounce by exactly (10⁴)^(1/4)=10×, and the table does: 8.495/0.850 = 9.994 — confirms 1/4,
not 1/8). Scanning C ∈ [0.01, 10] (3 orders of magnitude) and η ∈ [0.01, 1] (2 orders of
magnitude, so η² spans 4 orders):

| C | η = 0.01 | η = 0.1 | η = 1 |
|---|---|---|---|
| 0.01 | 8.50 | 2.69 | 0.85 |
| 0.03125 (= 1/32, best-anchored, see above) | 6.39 | **2.02** | 0.64 |
| 0.1 | 4.78 | 1.51 | 0.48 |
| 0.5625 (= 9/16, alternative convention) | 3.10 | 0.98 | 0.31 |
| 1 | 2.69 | 0.85 | 0.27 |
| 10 | 1.51 | 0.48 | 0.15 |

(table entries are H_bounce / M̄_Pl)

Across the whole scan, H_bounce/M̄_Pl spans only 0.15–8.5 — under two orders of magnitude
(1.75 decades), despite the combined input (C η²) swinging over 7 orders of magnitude —
consistent with the ¼-power law above: (10⁷)^(1/4) ≈ 56, matching the observed 8.5/0.15 ≈ 57.
For the best-anchored coefficient (C = 1/32, derived above from the cross-checked spin-density
substitution) with a conservative production efficiency (η = 0.1): **H_bounce = 2.02 M̄_Pl** —
still trans-Planckian by a factor of ~2, inside the η=1 column it drops to **0.64 M̄_Pl**,
sub-Planckian. The alternative-convention figure (C = 9/16) gives 0.98 M̄_Pl at η=0.1 and
0.31 M̄_Pl at η=1. Both candidate coefficients land in the same qualitative place: right
around the Planck scale, requiring η to not be too conservative (η ≳ 0.3–1, i.e. gravitational
particle production populating a sizeable fraction of the available modes) to end up
comfortably sub-Planckian rather than marginally above it. For η = 1 (maximal occupancy), the
bounce is comfortably sub-Planckian across the whole C range tested (0.15–0.85 M̄_Pl).

**Coherence checks (both pass, same as §2.1):** age(bounce → today) = **13.814064 Gyr**, an
exact match to the ΛCDM baseline, for C = 9/16, η = 0.1. Ω_torsion/Ω_r at BBN =
8.0×10⁻¹⁶⁹ — even more negligible than the thermal version (the self-sourced term falls off
even faster, n² ∝ a⁻¹²).

### 2.4 Computing η instead of assuming it — the mechanism does not survive

Everything in §2.3 above used η as a scanned free parameter (0.01–1), on the heuristic
assumption that gravitational particle production populates modes up to k~H at O(η)
occupancy. That heuristic can actually be checked: the dimensionless bounce shape implied by
§2.3's own ansatz is exact and closed-form (matter and Λ are negligible near the bounce, so
E²(a) = Ω_r a⁻⁴ − Ω_r a_bounce⁸ a⁻¹², with a_bounce defined by E²=0). In x≡a/a_bounce,
τ≡H_bounce·t, this gives a **universal, parameter-free bounce shape**:

h(x) ≡ H/H_bounce = √(x⁻⁴ − x⁻¹²), &nbsp; dx/dτ = √(x⁻² − x⁻¹⁰)

(cross-checked two independent ways — finite difference on the full E²(a), and the closed
form's own derivative — that dh/dτ at the bounce is exactly 4.0000, i.e. Ḣ(0) = 4 H_bounce²,
an exact identity of this mechanism, not a fitted number). Running the **same validated
Bogoliubov/adiabatic-vacuum mode equation** used for the dark-matter calculation
(`DARK_MATTER_RELIC_DENSITY.md` Part VIII.3) — not an assumed occupation, an actual mode
equation solved through this exact bounce background, for quarks (M/H_bounce ~ 10⁻²¹,
indistinguishable from exactly massless) — gives a genuinely computed number:

**η_computed ≈ 9.5 × 10⁻⁶**

five to six orders of magnitude below the η ≳ 0.3 that §2.3 needed for a sub-Planckian
result. This was checked for IR convergence (the momentum integrand k²n_k → 0 as k → 0,
confirmed down to k=0.002 H_bounce, so the result isn't an artifact of an unresolved
long-wavelength tail) and the representative-mode trace shows the expected plateau
(adiabaticity restored) well before the read-out point. Physically: only a narrow band of
modes near the bounce's own curvature scale (κ ~ 0.1–1 in H_bounce units) are produced with
order-unity occupancy; most of the naive "all modes up to k~H" phase space assumed by the η
heuristic simply isn't actually populated for a *smooth* (non-singular) transition — this is
the real, computed answer, not the optimistic guess.

Feeding this back into the self-consistency formula from §2.3 (valid regardless of which C or
η was used to locate the bounce in the first place, since the dimensionless shape above does
not depend on them — only on the mechanism's a⁻¹² structure):

| C | self-consistent H_bounce (using η_computed) |
|---|---|
| 1/32 (best-anchored) | **207 M̄_Pl** |
| 9/16 (alternative convention) | **101 M̄_Pl** |

**This reverses the §2.3 conclusion.** Once the production efficiency is actually computed
rather than optimistically assumed, the self-sourced mechanism lands at ~100–200 M̄_Pl —
*worse* than the original thermal-bath estimate in §2.1 for the better-anchored coefficient.
The conceptual fix (let the tunneling event supply its own density, rather than assuming a
pre-existing bath) was the right question to ask, and the calculation needed to answer it was
worth doing properly — but the honest answer is that it does not rescue this mechanism. A
smooth, non-singular bounce in this specific construction (quarks, this specific a⁻¹² torsion
term) produces far too few quanta to generate enough self-sourced repulsion to turn around
before trans-Planckian densities, for either candidate value of C.

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

### 4.1 What a first-order EWSB would actually require (sketch, not a new model)

If this is carried forward, here is what real electroweak-baryogenesis model-building uses to
restore a first-order transition — a survey of the existing options, not a new derivation or
a specific proposal for this project to adopt:

- **A real gauge-singlet scalar added to the Higgs sector** (Profumo, Ramsey-Musolf &
  Shaughnessy, *Singlet Higgs Phenomenology and the Electroweak Phase Transition*,
  arXiv:0705.2425): the singlet mixes with the Higgs and can produce a tree-level barrier
  between the symmetric and broken phases, restoring a strong first-order transition for
  specific regions of its mass/coupling parameter space. One new scalar field, one new mass
  scale, one new coupling — the minimal addition.
- **A dimension-six EFT deformation of the Higgs potential**, i.e. a new operator (H†H)³
  suppressed by a cutoff scale Λ, without committing to what new states generate it (Grojean,
  Servant & Wells, hep-ph/0610003): viable for Λ in the range ~500–1000 GeV. This is the
  "agnostic" option — it doesn't say what the new physics is, only that something at the TeV
  scale must generate this operator.
- **A second Higgs doublet** (2HDM): can restore a first-order transition for part of its
  parameter space, generally requiring one new scalar mass at least ~300 GeV (per a
  dimension-six-operator treatment: Anisha, Biermann, Englert & Mühlleitner, *Two Higgs
  doublets, effective interactions and a strong first-order electroweak phase transition*,
  JHEP 08 (2022) 091, arXiv:2204.06966).

All three options share the same structure: **a new scalar (or an EFT stand-in for one) at or
near the TeV scale**, with no fixed, uniquely preferred choice among them in the literature.
Nothing established elsewhere in this project (κ, σ, chronomagnetics, the Z₃ triangle) points
to a specific new scalar at this scale — adopting any of these would be a genuinely new,
unmotivated conjecture for this project, not a consequence of anything already derived here.
This is recorded as the real menu of options, not a recommendation to pick one.

---

## 5. Summary verdict

| Question | Answer |
|---|---|
| Does real backward ΛCDM reveal a new "beginning"? | No — it reaches the ordinary singularity, for any H0. Expected, not a defect. |
| Can resistance-to-tunneling (quark-sourced torsion) replace the singularity with something real? | Yes, via a real, citable mechanism (ECKS/Popławski) — a bounce always exists for any positive coupling. |
| Is the bounce scale trustworthy with a pre-existing thermal bath? | No — trans-Planckian (1.4–138 M̄_Pl) for any plausible coupling. |
| Does adding sub-quark dof fix this? | No — checked quantitatively; the lever is too weak (∝1/g) and the fix requires implausible dof. |
| Does letting the tunneling event supply its own density fix this, *assuming* an O(η) production efficiency? | Looked like yes at first — fourth-root-damped self-consistency landed at 0.15–8.5 M̄_Pl across the scanned η ∈ [0.01,1]. |
| Does it still work once η is *actually computed* (§2.4), not assumed? | **No.** Running the real Bogoliubov mode equation through the exact bounce background gives η≈9.5×10⁻⁶ — far below what §2.3 needed. Self-consistent H_bounce comes out at 101–207 M̄_Pl, worse than the original thermal estimate. This reverses the §2.3 conclusion. |
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
- Unger & Popławski, *Big Bounce and Closed Universe from Spin and Torsion*, Astrophys. J. 870,
  78 (2019), arXiv:1808.08327 (source of the best-anchored coefficient, C = 1/32, used in §2)
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
- Profumo, Ramsey-Musolf & Shaughnessy, *Singlet Higgs Phenomenology and the Electroweak
  Phase Transition*, arXiv:0705.2425 (§4.1, BSM option: real singlet scalar)
- Grojean, Servant & Wells, hep-ph/0610003 (§4.1, BSM option: dimension-six (H†H)³ operator)
- Anisha, Biermann, Englert & Mühlleitner, *Two Higgs doublets, effective interactions and a
  strong first-order electroweak phase transition*, JHEP 08 (2022) 091, arXiv:2204.06966
  (§4.1, BSM option: two Higgs doublet model)

---

## 7. Open items (not addressed here)

1. **The exact ECKS coefficient C** — narrowed, not resolved. §2 now anchors C=1/32 to a
   cross-checked equation (Unger & Popławski 2019) rather than a bare assertion, with C=9/16
   as the alternative-convention figure, but this session still cannot reach any primary
   source directly (confirmed session-wide network policy, not arxiv-specific) to pick
   between them or rule out a third convention entirely. A future session with that access
   should replace this two-candidate treatment with the verified value.
2. **This is a leading-order (test-field, fixed-background) estimate, not a full dynamical,
   self-consistently backreacting solve — considered, and deliberately not pursued further.**
   Backreaction corrections matter when a leading-order result is marginal; §2.4's result
   (H_bounce off by a factor of ~100–200 from the Planck scale once η is actually computed)
   is not marginal. No plausible O(1)-ish backreaction correction closes a 2-order-of-magnitude
   gap, so building the full nonlinear solver was judged not to be worth the effort it would
   take relative to what it could change. This would need revisiting only if a future
   coefficient-C determination (item 1) or a different source mechanism entirely moved the
   leading-order estimate back into marginal territory.
3. **Post-bounce continuity (quarks → QCD confinement) — not modeled, and not high-value to
   model further given item 2.** Standard thermal-history physics (hadronization at the real
   QCD crossover, T≈155 MeV) is well-established and independent of whether this specific
   bounce mechanism is viable; modeling it in detail for a mechanism already shown not to
   reach a trustworthy density would mostly be modeling the standard model, not this proposal.
4. **If a first-order EWSB is wanted** (to literally recover a tunneling-driven weak-force
   activation, per §4) — see the sketch added below, §4.1.
5. **A real dark-energy production mechanism** — not attempted (§1), and not something this
   kind of document should be expected to resolve; it's the open cosmological constant
   problem. This project's own separate, pre-existing attempt
   (`COSMOLOGICAL_CONSTANT_COMPLETE_DERIVATION.md`, OP-5) was cited for transparency but
   **not re-audited** here, and has no established connection to this document's mechanism.

---

**Document Status:** OPEN, negative result on the cosmological half of the original claim. A
real mechanism (ECKS torsion repulsion) was built, scanned honestly over its uncertain
coefficients, and checked for coherence against standard cosmology (age, BBN both pass in
every version). Four variants were tried — thermal bath, preon-layer patch, self-sourced with
an assumed efficiency, self-sourced with a computed efficiency — and none lands at a
trustworthy sub-Planckian scale; the best current number is ~100 M̄_Pl. "Resistance to
tunneling creates quarks" remains a real, citable mechanism in the sense that it genuinely
produces *some* gravitational repulsion, but not enough, by 2+ orders of magnitude in H, to
credibly replace the Big Bang singularity with this specific construction. Not a STUR closure
claim — a standalone real-physics exploration, written up for reproducibility, including the
negative result.
