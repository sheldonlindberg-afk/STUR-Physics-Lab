# The Make It Make Sense theory (MIMS): version 0.8

*Named by its author. Earlier working name: fullness-phase theory, which is why the scripts
are `src/fp_*.py`. A new start, built from the user's postulates. The earlier STUR program and the
god-equation search (REPORT.md, GOD_EQUATION.md) are not inputs. Every number below is
computed in `src/fp_*.py` and pinned by `tests/test_fullness_phase.py`.*

**Labels:**
- **NEW:** this theory's own claim.
- **FOLLOWS:** derived from the postulates, with no new assumption.
- **KNOWN:** established physics.
- **LIT:** a published result, either *retrieved* (read in this work) or *recalled* (from
  memory).

## The postulates (the user's)

| | Postulate | User's words |
|---|---|---|
| P1 | Density has a ceiling ρ_max, at or beyond the Planck density. **Fullness** φ = ρ/ρ_max runs from 0 (empty) to 1 (full). | "Beyond Planck density, unable to measure without creating a black hole." |
| P2 | Gravity is teleparallel (gravity is the *torsion*, or twist, of spacetime), with a new law that respects the ceiling. | "New gravity law, look to TEGR." |
| P3 | Matter degrades with time itself. | "Time itself." |
| P4 | Measurement is phase locking: what is measured is the energy needed to lock a probe to the system. | "What is really being measured is how much energy it takes to phase lock a quantum system with an EM system." |
| P5 | The universe is the dance between 1 and 0: black holes are pure matter, voids head towards empty. | "Everything we experience is the dance between 1 and 0." |

## The equations

**(1) The gravity law.** In teleparallel gravity the expansion obeys
12H² f_T + f = 16πGρ, with T = −6H². Demanding that expansion stop at both empty and full,
H² = (8πG/3) ρ (1 − φ), fixes the law. With T_b = −4πGρ_max:

```
φ = sin²(u/2)          T = T_b sin²u = 4 T_b φ(1 − φ)
f = 2 T_b (u sin u + cos u − 1)          u ∈ [0, π]
```

- **FOLLOWS:** fullness is an **angle** u, which fits P4: fullness is a phase.
- **FOLLOWS:** torsion, which is the gravitational field here, is **zero at empty and at
  full, and greatest at half full**. Gravity is the dance itself: |T| ≤ 4πGρ_max.
- **FOLLOWS:** at low fullness the law becomes ordinary teleparallel gravity, which is
  equivalent to general relativity: f/T = 1 + φ/3 + …. The law is single-valued and smooth
  through half full when written in u; written in T alone it would have two branches.
- **LIT (recalled):** the same expansion law is the effective dynamics of loop quantum
  cosmology, where the same angle appears as a holonomy. An f(T) form of it is Amorós, de
  Haro & Odintsov (2013). The postulates force this structure; the reading of the angle as
  a phase and of torsion as φ(1 − φ) is this theory's.

**(2) Degradation.** With one constant, τ:

```
dρ_m/dt = −3Hρ_m − ρ_m/τ          dρ_r/dt = −4Hρ_r + ρ_m/τ
```

Rest mass becomes radiation, and total energy is conserved.

**(3) Measurement.** Viewing a feature of size δx means reading the locked phase to
δθ = kδx:
- **Locking (KNOWN, Adler):** dθ/dt = Δω − K sin θ.
- **Energy to view:** E = ħc/δx with quantum-correlated light (the Heisenberg limit), or
  ħcλ/(2πδx²) with classical light (the standard quantum limit).
- **Two conditions:** neither the probe nor the system being viewed may be inside its own
  horizon.

## What the equations give

| # | Result | Status |
|---|---|---|
| G2 | A collapsing universe stops at φ = 1 exactly and re-expands, with no singularity. Checked for dust and radiation; the constraint holds to 5×10⁻⁸, and a_min matches the analytic value. | FOLLOWS |
| G3 | A collapsing star stops at a **pure-matter core** of radius (3M/4πρ_max)^⅓, reached a proper time 2r_s/3c after crossing the horizon. Sun: 4.5×10⁻²³ m after 6.6 μs. Sgr A*: 7.3×10⁻²¹ m. M87*: 8.4×10⁻²⁰ m. | FOLLOWS |
| G3′ | **The horizon stays.** Real black holes form their horizon while nearly empty (M87*: about 0.4 kg/m³), so no density ceiling can remove it. Only objects below 0.17 Planck masses (3.8 μg) have a full core bigger than their horizon. So: a hole on the outside, pure matter on the inside. After the bounce the core re-expands, which is a white-hole phase inside. | FOLLOWS |
| D1 | If degradation inside the Earth ends as heat: τ > 3.6×10²⁰ yr (Earth's heat flow, 47 TW, recalled). | FOLLOWS |
| D2 | If a proton's degradation has a visible channel: τ > 2.4×10³⁴ yr (Super-Kamiokande, recalled). Less than 6×10⁻²⁵ of all matter has degraded since the Big Bang. | LIT + FOLLOWS |
| D3 | Degradation erases free matter (at about 10³⁴ yr or later) long before black holes evaporate (about 10⁶⁷ yr). It **cannot empty a black hole**, because gravity counts radiation too. Going "back to 0" needs both steps: degradation turns matter into radiation, and expansion dilutes radiation away. | FOLLOWS |
| L3 | The probe alone: imaging hits a horizon at √2·l_P. Classical light hits it at l_P/√π for any colour. Quantum light alone could go to 2l_P²/λ, far below the Planck length. | FOLLOWS |
| L4 | **Locking is mutual,** so the system is pulled too. The system spreads by δx² ≥ ħt/2m (Salecker–Wigner, KNOWN). It must not be its own black hole, and by causality only its part within ct can join a lock lasting t. Together these give **δx ≥ l_P for any probe colour, photon number or quantum state.** | NEW (Ng & van Dam, KNOWN, get (l_P²L)^⅓ under a different assumption) |
| L5 | At the measurement wall, the lock region's fullness is 0.06 ρ_P. With ρ_max ≥ ρ_P, everything between the wall and φ = 1 can never be viewed. P1 becomes a statement about measurement. | FOLLOWS |

## Part 4: where the core's bounce gets out (v0.2)

Script: `src/fp_black_hole_exterior.py` (torsion derived in
`src/fp_torsion_derivation.py`); output: `results/fullness_phase/black_hole_exterior.txt`.

**X1, torsion outside a black hole.** For the spherical tetrad the torsion scalar is
T = 2(√B − 1)[A(√B − 1) − rA′]/(r²AB), derived with sympy. The same form appears in
Bahamonde et al. (LIT, recalled).
- **Schwarzschild:** T = (4/r²)[1 − (r − M)/√(r(r − 2M))].
- **Far away** it falls off as −2M²/r⁴.
- **At the horizon it diverges.**

The law's deviation from GR at the photon sphere is 10⁻⁸¹ (10 M☉) to 10⁻⁹⁹ (M87*), which
is invisible to the Event Horizon Telescope and to LIGO.

**X2, the cap (FOLLOWS).** The law only exists for |T| ≤ 4πχ/l_P², where χ = ρ_max/ρ_P.
So the static exterior ends at a *cap surface*:
- position: √δ = l_P²/(2πχ r_s²), with r_cap = r_s(1 + δ);
- height above the horizon: l_P²/(πχ r_s), a proper distance below the Planck length
  (10⁻⁴⁰ l_P for 10 M☉);
- redshift: 2πχ r_s²/l_P².

By part 3 no measurement can resolve the cap directly. Only what it *does* can be seen.

**X3, what the cap does decides the observables:**

| If the cap… | Observable | Status |
|---|---|---|
| (a) reflects at all | Gravitational-wave **echoes**, delayed by 2[r*(3M) − r*(r_cap)]/c. Values: **0.072 s** (10 M☉), **0.455 s** (62 M☉, GW150914), 8100 s (10⁶ M☉, LISA). ρ_max enters only through a logarithm: χ = 10³ adds 4%. That's about twice the delay of a Planck-length wall. | Sharp prediction. LIGO–Virgo searches have found no significant echoes (recalled), so this case needs low reflectivity. Spin isn't included yet. |
| (b) lets the bounce straight out | Re-emission within about 36 ms (10 M☉): accreting black holes would explode. | **Excluded** by persistent X-ray binaries and quasars. |
| (c) releases the bounce at its own redshift (NEW assumption; **superseded by part 5**) | t_esc = (32πχ/3)G²M³/(ħc⁴) = t_Hawking/480. Stellar and galactic black holes: 10⁶⁴ yr and longer. **Primordial black holes of 1.35×10¹² kg would be bursting today**, releasing 1.2×10²⁹ J at once at about 100 MeV (gamma rays). | Testable by gamma-ray burst searches such as Fermi-LAT. The rate isn't predicted, because the abundance of primordial black holes is unknown. |

Same cap, different assumption: if the cap runs on Planck time rather than the core's
bounce time, t ∝ M² instead. That's the Haggard–Rovelli scaling (LIT, recalled). Part 5
settles this by computing the collapse, with no assumption about the cap: the answer is
**M²**.

## Part 5: the time-dependent collapse, and how long a black hole lasts (v0.3)

Script: `src/fp_collapse_shock.py`; output: `results/fullness_phase/collapse_shock.txt`.

**The model.** A spherical dust star in free fall. Every layer obeys the theory's law with
its own mean fullness φ(R) = 3m(R)/(4πρ_max R³). With b = u/2 and φ = sin²b:

```
dR/dt = −kR sin b cos b          Db/Dt = (3k/2) sin²b          k = √(8πGρ_max/3)
```

- **FOLLOWS:** each layer carries a phase that only ever advances, and the layer bounces
  when the phase passes the half turn (φ = 1).
- **FOLLOWS, verified with sympy:** the same law in conservation form is
  ∂_t B + ∂_R[−(k/2)R³ sin²(B/R²)] = 0, with B = R²b. LIT (recalled): this has the same
  structure as effective loop-quantum dust collapse (Husain, Kelly, Santacruz &
  Wilson-Ewing, 2022).
- **The shock:** inner layers bounce first and run into outer layers that are still
  falling. Where they cross, a shock forms, and the conservation form fixes how it moves.

**Numerics.** Finite volume with the exact (Godunov) flux. Face values come from the
enclosed mass, so empty space outside the star is an exact equilibrium. Units: Planck
units. The horizon is where outgoing light can't move outward (v < −1).

**Results:**

| M (Planck masses) | 2 | 3 | 4 | 6 | 8 | 12 |
|---|---|---|---|---|---|---|
| Lifetime T (Planck times) | 91.7 | 215.4 | 384.0 | 866.6 | 1543.3 | 3478.7 |
| T/M² | 22.9 | 23.9 | 24.0 | 24.07 | 24.11 | 24.16 |

(The M = 12 run took 7 minutes, so it isn't part of the script's default output.)

> **Status after part 7:** this lifetime uses the *winding* rule for the shock. P1 forces
> the *angle* rule instead (part 7), so the M² lifetime below is the winding-rule answer,
> not yet the theory's. The numbers are kept as a record.

- **The lifetime is T ≈ 24.2·√χ·M²** (in Planck units). The ratio still creeps up slowly
  with M (24.00, 24.07, 24.11, 24.16), so the large-M value is about 24.2 ± 0.1. (8π/3)^{3/2} = 24.24 is
  numerically close, but it isn't derived.
- **Robustness:** halving the grid changes T by 0.6%; doubling the box changes nothing;
  starting the star at 1.2 r_s instead of 1.5 r_s changes T by 0.7%. Changing the ceiling
  χ by 4 or 1/4 gives T ratios of 2.00 and 0.49, so T ∝ √χ.
- **Mechanism:** the outer horizon stays at r_s, and the shock drives the inner edge of the
  trapped region outward until the two meet. Then the horizon is gone and the matter comes
  back out.

**What it means (χ = 1):**

| Black hole | MIMS lifetime | Hawking evaporation |
|---|---|---|
| 1 solar mass | 3.4×10²⁶ yr | 2×10⁶⁷ yr |
| Sgr A* | 6.4×10³⁹ yr | 2×10⁸⁷ yr |
| M87* | 1.5×10⁴⁶ yr | 6×10⁹⁶ yr |

- Black holes are **long-lived pure-matter bounces, not permanent holes**. Matter that
  falls in comes back out after a time proportional to M². Stellar black holes outlive the
  present universe by about 10¹⁶, so this conflicts with no observation.
- **Primordial black holes of 1.26×10²² kg (0.17 Moon masses) would be ending today.**
  Each would release 1.1×10³⁹ J from a region 19 μm across, so the natural wavelength is in
  the far infrared. The rate isn't predicted, because the primordial black-hole abundance
  is unknown.
- **This supersedes part 4's case (c)** (M³, primordial holes of 1.35×10¹² kg).

## Part 6: what comes out when the horizon dissolves (v0.4)

Script: `src/fp_burst.py`; output: `results/fullness_phase/burst.txt`.

**B1, what the collapse leaves (dust, part 5's law).** Running past the lifetime T:
- **Nothing is left inside r_s.** All the mass sits in one shell just outside r_s, which
  drifts outward at a pace fixed in units of T: it reaches 1.14 r_s at 1.5T and 1.26 r_s at
  2T.
- **The position is converged.** It agrees to 0.1% across three grids
  (Δr = 0.05, 0.025, 0.0125).
- **It moves very slowly:** about 0.019/M times c. That's 3×10⁻³² c for a real hole.
  *Part 7: this slow drift is an artifact of the winding rule. GR outside r_s moves such a
  shell at about 0.7c.*
- **The result:** a horizonless shell of pure matter. That's the user's "black holes are
  pure matter", taken literally.
- **The shell breaks P1.** The mass rises from 0 to M across about 2 cells, and in the
  exact solution across zero width, so the local density is unbounded. The part-1 law caps
  the *mean* fullness inside each radius, not the local density.
- **CORRECTION (part 7):** v0.4 reported the shell's local fullness as "6 to 94, rising
  with resolution". Those numbers were an artifact. In the one cell holding the shock, the
  stored phase is an average of b ≈ π and b ≈ 0, which sits near π/2 ("full"), and
  converting it to mass gave a spurious (4π/3)R³ρ_max. **Retracted.**

**B2, what a hole ending today is made of.**
- Its mass is M_now = 1.26×10²² kg, and it must be primordial.
- It formed when the horizon mass was about M, at t_f = GM/c³ = 3.1×10⁻¹⁴ s.
- **FOLLOWS:** the mean density inside r_s, 3c⁶/(32πG³M²), *equals* the density of the
  universe at t_f exactly.
- So the hole is early-universe plasma at kT_f = **2.7 TeV**, with all Standard Model
  species (g* = 106.75). LIT, recalled: holes form at a fraction γ ≈ 0.2 of the horizon
  mass; with γ = 0.2, kT_f = 1.2 TeV.

**B3, the photon energy (an upper bound, FOLLOWS).**
- Entropy is conserved through an adiabatic collapse and bounce, and only increases in
  shocks. So the emerging plasma, back at about r_s, is **no hotter than at formation**:
  kT_out ≤ kT_f.
- Baryon loading is 8×10⁻¹⁴, so this is a pure-radiation fireball. Such a fireball's
  observed temperature stays about T₀ (KNOWN, recalled: Goodman 1986; Paczyński 1986).

**B4, the burst if the plasma gets out promptly:**

| Quantity | Value |
|---|---|
| Energy | 1.1×10³⁹ J, at once |
| Photon energy | ≲ 7 TeV (2.7 kT_f) |
| Photons (half the energy, assumed) | ~5×10⁴⁴ |
| Arrival spread | ~r_s/c = 6×10⁻¹⁴ s |
| Reach (10⁵ m² ground array, 10 photons; both chosen, not specifications) | ~20 Mpc, inside the ~100 Mpc range of multi-TeV photons (recalled) |
| Signature | many multi-TeV air showers in the same nanosecond across the array, with TeV neutrinos at the same moment |

**Part 7 settles which end:** a thin shell outside r_s moves at about 0.7c (the GR
junction condition), so once the matter is outside r_s it leaves promptly. The TeV flash
above is the theory's burst. *When* it happens is open again.

## Part 7: the ceiling at every point (v0.5)

Script: `src/fp_local_fullness.py`; output: `results/fullness_phase/local_fullness.txt`.

**L1, correction.** See part 6: the reported local-fullness numbers were an artifact of a
cell-averaged phase, and are retracted. The zero-thickness shell is real.

**L2, a local law tried (NEW).** Weight each layer's active mass by its *own* fullness:
d²Rᵢ/dτ² = −(G/Rᵢ²) Σⱼ Δmⱼ(1 − 4φⱼ). This is exact for a uniform star.
- **It keeps P1:** the maximum local fullness is 0.996 (M = 2) and 0.993 (M = 3).
- **But it isn't consistent.** The model has no equation for the geometry outside the
  matter, so the star comes straight back out through its own horizon after about 3.6 M
  Planck times (about 10⁻⁵ s for a solar mass). That's part 4's excluded case (b).
- **Verdict:** not viable on its own.

**L3, the shell is a one-turn phase slip (FOLLOWS).** Across the shock, b jumps by about
π, which is one full turn of the dance (u = 2b). The inner layers have gone through
collapse, full and re-expansion; the outer layers haven't started. A conservation law's
shock speed is [F]/[B], so it depends on how that turn is counted. (KNOWN: weak solutions
need a rule to be unique.)

| Rule | Inside the shell, the phase passes through | Consequence |
|---|---|---|
| **Winding** (count the turn; used in parts 5–6) | **full** (b = π/2) | A smooth shell would need (4π/3)R³ρ_max of mass: 300 times the star's mass at M = 3, and 10⁶¹ times for a real primordial hole. So the shell must be infinitely thin, and **P1 fails**. |
| **Angle** (a full turn counts as no change) | **empty** (b = π) | A shell of finite thickness at φ ≤ 1 is possible: **P1 holds**. |

- **So P1 forces the angle rule,** and part 5's M² lifetime, computed with winding, is
  downgraded to OPEN.
- One attempt at an angle-rule solver re-wrapped the stored phase. That broke conservation
  (it injected hundreds of turns, even in empty space), so it was discarded and isn't used.

**L4, the check from GR (KNOWN + FOLLOWS).** Outside r_s the law equals GR to 10⁻⁷⁷, so a
thin shell of pure matter (rest mass μ = M, marginally bound) obeys the Israel junction
condition, M = μ√(1 + Ṙ²) − Gμ²/2R. That gives Ṙ² = M/R + M²/4R²:

| Shell radius | Speed |
|---|---|
| r_s | 0.75c |
| 1.14 r_s | 0.70c |
| 2 r_s | 0.52c |

- The winding solution's drift (0.0063c at M = 3) is **110 times too slow**, and 10³¹ times
  too slow for a real primordial hole. **The slow drift is an artifact of the winding
  rule.**
- **Once outside r_s, the matter leaves promptly.** The TeV flash (part 6) is the theory's
  burst.
- **Still open:** *when* the shell gets outside r_s, which is the lifetime. That needs a
  solver that conserves mass and counts the turn as an angle.

## Part 8: the mass-conserving, angle-rule collapse (v0.6)

Script: `src/fp_shell_crossing.py`; output: `results/fullness_phase/shell_crossing.txt`.

**The method.** Follow each mass layer individually and let layers pass through each
other, since dust doesn't collide.
- Mass is conserved exactly, and each layer's phase evolves continuously, so no jump
  between neighbours is counted.
- Each layer obeys the law with the mass inside it at that moment:
  d²Rᵢ/dτ² = −(Gmᵢ/Rᵢ²)(1 − 4φᵢ). That's exact GR for dust away from the ceiling, and its
  thin-shell limit is the Israel junction condition.

**E1, the lifetime is proportional to M:**

| Star | M = 2 | M = 4 | M = 8 | Solar mass |
|---|---|---|---|---|
| Uniform: T/M | 3.766 | 3.778 | 3.784 | 1.9×10⁻⁵ s |
| Concentrated (ρ ∝ 1 − x²): T/M | 3.03 | 3.21 | 3.20 | 1.6×10⁻⁵ s |

- **Converged:** going from 200 to 800 layers changes T by under 0.6%.
- **What it implies:** observed black holes last billions of years, so under this rule the
  bounce **can't re-emerge into our region of space**. It must open a new one beyond the
  hole: a white hole into a new expanding region. LIT (recalled): Popławski (2010)
  proposed bounces inside black holes opening new universes, using torsion, which is the
  same teleparallel/torsion family as this theory. This fits the author's cyclic picture:
  matter goes to full, bounces, and expands away towards 0.

**E2, P1 fails again (FOLLOWS).**
- In the uniform star the peak local fullness is exactly 1 at the bounce, so P1 is
  saturated but not broken.
- In the concentrated star, layers cross 457 to 2593 times, and the local fullness spikes
  to 3.6×10⁴ to 7.5×10⁴. These are caustics, and they're unbounded in the continuum.
- **Together with part 7, dust breaks P1 under either rule.** Winding gives a
  zero-thickness shell; the angle rule gives caustics.
- **So P1 requires pressure.** "Pure matter at 1" has to resist being compressed, and the
  theory needs an equation of state p(φ). OPEN, and now the top priority. Real primordial
  holes are radiation-era plasma (part 6, B2), which already has pressure p = ρc²/3.

## Part 9: collapse of matter that pushes back (v0.8, in progress)

Script: `src/fp_fluid_collapse.py`; output: `results/fullness_phase/fluid_collapse.txt`.

**CORRECTION.** The v0.7 solver for this part computed each zone's energy from its adiabat
and never checked energy conservation. Measured afterwards, it **created about 37% extra
energy** during the run (mass inside + escaped − M = +0.37 M). Its results are
**retracted**:
- 39% blown off;
- the horizon at 3.1 M;
- the shock at 8.7 M;
- "the stiffening holds the ceiling where plain radiation doesn't".

**The author's choice:** radiation that stiffens near full. In causal form:
- the sound speed² is 1/3 + (2/3)φ² up to full, and 1 beyond;
- that's ordinary radiation at low fullness, with sound reaching the speed of light exactly
  at full;
- pressure can't grow without limit, because past p = ρc² sound would travel faster than
  light.

**Gravity with pressure (FOLLOWS).** For a uniform region, the law and energy conservation
give exactly d²R/dτ² = −[(m + 4πR³P) − φ̄(4m + 8πR³P)]/R². With p = 0 that's part 8's law,
and with no ceiling it's GR.

**The solver (energy-conserving by construction).** It uses the Misner–Sharp equations for
a spherical fluid in GR (KNOWN):
- **the enclosed mass is evolved,** D_t m = −4πR²PU, and each zone's energy is its mass
  difference over its volume. Pressure is zero at the surface, so total mass-energy is
  conserved exactly;
- Γ² = 1 + U² − 2m(1 − φ̄)/R, and the lapse comes from the pressure gradient;
- artificial viscosity handles shocks, switching on only for compression faster than
  uniform contraction;
- time-stepping is fourth-order, with a kinematic limit so that no gap between layers
  closes by more than 10% per step;
- escaping outer zones are removed and counted, and a negligible outer zone is merged into
  its neighbour.

The start is a uniform ball at 1.5 r_s in free fall, which is arbitrary.

**Results:**

| Run | Horizon forms | Escaped | Peak fullness | Energy error | Stops at |
|---|---|---|---|---|---|
| Check, dust M = 2 | 1.13 M | 0 | 1.0000 | 9×10⁻¹⁶ | T = 7.589 (part 8: 7.53) |
| Stiffening, M = 2 | 3.82 M | 2.5% | 0.62 | 9×10⁻¹⁶ | 10.22 M |
| Stiffening, M = 4 | 3.76 M | 2.5% | 0.19 | 9×10⁻¹⁶ | 10.08 M |
| Radiation, M = 2 | 3.82 M | 2.5% | 0.62 | 9×10⁻¹⁶ | 10.22 M |
| Radiation, M = 4 | 3.76 M | 2.5% | 0.19 | 9×10⁻¹⁶ | 10.08 M |

- **F1:** energy is conserved to machine precision throughout every run.
- **F2:** the horizon forms at about 3.8 M, and only about 2.5% of the mass escapes before
  it does.
- **F3:** the stiffening and plain radiation agree so far. The peak fullness is at most
  0.62, where the stiffening hardly changes the pressure.
- **F4:** every run stops at about 10 M, when a zone is drained to almost no mass. That's a
  known odd–even instability of interface-averaged pressure work, not physics. The core is
  still collapsing, so the bounce, the lifetime and the burst aren't reached yet.

**OPEN, top priority:** a compatible energy discretisation, where each zone's energy is
changed by its own pressure and the total stays exact.

## What is new, and what isn't

- **Coincides with known physics:** the expansion law (loop quantum cosmology), the
  bounce, a regular black hole with a core, the Adler and Salecker–Wigner relations. That's
  a consistency check: the postulates don't contradict what's measured.
- **This theory's own:**
  1. fullness as a phase angle, with gravity (torsion) as the dance φ(1 − φ);
  2. measurement as *mutual* phase locking, which puts the Planck wall in locking rather
     than in light;
  3. degradation by time itself, with the two-step return to 0;
  4. black holes as phase-advancing layers whose bounce escapes as a one-turn phase slip.
     The ceiling P1 forces that slip to be counted as an angle (passing through empty), and
     GR then makes the released matter leave at about 0.7c. The lifetime is open again:
     the winding-rule value 24√χM² matches loop-quantum dust collapse, but P1 rules that
     rule out.

## Open problems (next work)

1. **Carry the fluid collapse through to the bounce (top priority).** The equation of state
   is chosen (part 9: radiation stiffening to the speed of light at full), and the solver
   now conserves energy exactly and has shock viscosity. It stops at about 10 M from a
   zone-draining instability. A compatible energy discretisation should fix that, and the
   full run decides:
   - whether the bounce re-emerges into our region or opens a new one;
   - the lifetime;
   - whether and when the TeV flash happens.
2. **Echoes and spin.** Does the shock or the cap reflect gravitational waves? The rotating
   version is needed to compare with real, spinning merger remnants.
3. **Fix τ.** Nothing yet sets the degradation time. If the theory predicts it,
   Hyper-Kamiokande (about 10³⁵ yr, recalled) can test it.
4. **The present universe.** Does the dance (torsion ∝ φ(1 − φ) on the scale of voids and
   clusters) do the job of dark energy or dark matter? At present-day fullness (about
   10⁻¹²³) the law is GR to 10⁻¹²³. So it can't, unless the fullness that matters on
   large scales is defined differently.
5. **The lock energy as an observable.** Can the mutual-locking bound be probed below the
   Planck scale with correlated interferometers (the Fermilab Holometer type)?
6. **Known problems of f(T) gravity:** local Lorentz invariance and extra modes have to be
   checked for this law.

## Reproduce

```
python src/fp_gravity.py       # results/fullness_phase/gravity.txt
python src/fp_degradation.py   # results/fullness_phase/degradation.txt
python src/fp_phase_lock.py    # results/fullness_phase/phase_lock.txt
python src/fp_black_hole_exterior.py  # results/fullness_phase/black_hole_exterior.txt
python src/fp_collapse_shock.py       # results/fullness_phase/collapse_shock.txt (about 4 min)
python src/fp_burst.py                # results/fullness_phase/burst.txt (about 30 s)
python src/fp_local_fullness.py       # results/fullness_phase/local_fullness.txt (about 10 s)
python src/fp_shell_crossing.py       # results/fullness_phase/shell_crossing.txt (about 2 s)
python src/fp_fluid_collapse.py       # results/fullness_phase/fluid_collapse.txt (about 10 s)
python -m pytest tests/test_fullness_phase.py -q
```
