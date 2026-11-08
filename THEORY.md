# Fullness-phase theory (working name): version 0.1

*A new start, built from the user's postulates. The earlier STUR program and the
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

## What is new, and what isn't

- **Coincides with known physics:** the expansion law (loop quantum cosmology), the
  bounce, a regular black hole with a core, the Adler and Salecker–Wigner relations. That's
  a consistency check: the postulates don't contradict what's measured.
- **This theory's own:**
  1. fullness as a phase angle, with gravity (torsion) as the dance φ(1 − φ);
  2. measurement as *mutual* phase locking, which puts the Planck wall in locking rather
     than in light;
  3. degradation by time itself, with the two-step return to 0.

## Open problems (next work)

1. **The outside of a black hole.** The static, spherical solution of the gravity law
   decides what the outside sees: an ordinary horizon, a modified one, or a bounce visible
   from outside. This is the decisive test of "black holes are pure matter" against
   gravitational-wave and Event Horizon Telescope data.
2. **Fix τ.** Nothing yet sets the degradation time. If the theory predicts it,
   Hyper-Kamiokande (about 10³⁵ yr, recalled) can test it.
3. **The present universe.** Does the dance (torsion ∝ φ(1 − φ) on the scale of voids and
   clusters) do the job of dark energy or dark matter? At present-day fullness (about
   10⁻¹²³) the law is GR to 10⁻¹²³. So it can't, unless the fullness that matters on
   large scales is defined differently.
4. **The lock energy as an observable.** Can the mutual-locking bound be probed below the
   Planck scale with correlated interferometers (the Fermilab Holometer type)?
5. **Known problems of f(T) gravity:** local Lorentz invariance and extra modes have to be
   checked for this law.

## Reproduce

```
python src/fp_gravity.py       # results/fullness_phase/gravity.txt
python src/fp_degradation.py   # results/fullness_phase/degradation.txt
python src/fp_phase_lock.py    # results/fullness_phase/phase_lock.txt
python -m pytest tests/test_fullness_phase.py -q
```
