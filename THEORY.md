# The Make It Make Sense theory (MIMS): version 0.4

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
- **The result:** a horizonless shell of pure matter. That's the user's "black holes are
  pure matter", taken literally.
- **But the shell breaks P1 (FOLLOWS).** It's unresolved: its local fullness is 6 to 94 and
  rises as the grid is refined. The part-1 law caps the *mean* fullness inside each radius,
  not the local density. **The law must also cap local fullness.** That acts like a
  pressure, and it decides how fast the shell actually comes out. OPEN, and now the top
  priority.

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

**The two ends:** with no pressure (dust), there's no burst and the shell drifts out over
many lifetimes. With prompt release, there's the nanosecond TeV flash above. The
local-fullness law decides between them.

## What is new, and what isn't

- **Coincides with known physics:** the expansion law (loop quantum cosmology), the
  bounce, a regular black hole with a core, the Adler and Salecker–Wigner relations. That's
  a consistency check: the postulates don't contradict what's measured.
- **This theory's own:**
  1. fullness as a phase angle, with gravity (torsion) as the dance φ(1 − φ);
  2. measurement as *mutual* phase locking, which puts the Planck wall in locking rather
     than in light;
  3. degradation by time itself, with the two-step return to 0;
  4. black holes as phase-advancing layers whose bounce escapes as a shock, with lifetime
     ≈ 24√χ M² (the structure matches loop-quantum dust collapse; the theory's own route
     to it is new).

## Open problems (next work)

1. **The local-fullness law (now the top priority).** Part 6 found that the law, as
   written, caps only the *mean* fullness inside each radius. After the shock forms, the
   local fullness exceeds 1, which breaks P1. The law has to cap local fullness too. It
   will act like a pressure, and it decides whether the remnant shell drifts out (no burst)
   or blows out (the TeV flash). It is also needed to confirm the part 5 lifetime, which was
   computed with the mean-fullness law.
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
python -m pytest tests/test_fullness_phase.py -q
```
