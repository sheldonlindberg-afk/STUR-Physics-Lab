> **Superseded.** This page records the choice offered after unification steps 4–5. The
> work went on to options A–C (all excluded or unobservable, [WALL.md](WALL.md)) and then to
> the current research notes ([README.md](README.md)). Kept for the record.

# Unification search, steps 4–5: equal weights, and the room for a prediction

Reproduce:
- `python3 src/stur_ising_confinement.py` (step 4)
- `python3 src/stur_predictions.py` (step 5)

Outputs are in `results/ising/` and `results/predictions/`. Labels: KNOWN, FOLLOWS,
LIT (a literature value used as input, not recomputed).

## Step 4: equal weights for quark and string. **Inconclusive.**

**Goal:** show that, in a theory with a relativistic continuum limit, the modular
Hamiltonian weights the string energy and the quark energy equally. This is
Bisognano–Wichmann with one slope.

**Model:** the Ising chain in transverse and longitudinal fields. Kinks are
confined (McCoy–Wu, KNOWN), the string energy is an operator, and at h = 0 there
is an exact lattice benchmark: the corner-transfer-matrix slope
ε = πK(k′)/K(k) (KNOWN).

**What went wrong.** The kink is itself a Z₂ charge. The string state flips the
magnetization right at the cut, which the vacuum almost never does. So:
- Δ⟨K⟩ is dominated by a large constant, already 15–30 at ℓ = 1.
- 0.2–30% of the weight lies beyond the Schmidt modes I can resolve (K > 69).
- ΔS grows near the chain's open edge instead of saturating.

The comparison ratio is therefore meaningless at N ≤ 18. Settling it needs DMRG
at large N with high-precision Schmidt spectra. Even a positive result would only
confirm Bisognano–Wichmann, which is already a theorem for relativistic quantum
field theories, so I've stopped here.

## Step 5: how much room is there for a STUR prediction?

**No new physics without new structure.** Every prediction of the unified
equation (the first law with sector-specific K) is standard physics. Three can be
tested in the lab, and none of them distinguishes STUR:
1. V = ⟨(−1)^ΔN⟩: a qubit coupled to a cavity, measuring the cavity's
   photon-number parity.
2. Entanglement Hamiltonian = distance-weighted local energy: already measured in
   quantum simulators (LIT: Kokail et al. 2021).
3. A confining string's entropy is independent of its length, while its modular
   energy grows as σ × area: testable in Rydberg-atom or trapped-ion simulators.

**STUR's picture with ordinary gravity.** Take "spacetime records which-path
information" literally, with standard gravity as the environment. A thermal
graviton bath gives a decoherence rate

Γ_rate = c₀ · (k_BT/ħ) · (ΔE/E_P)²

This form follows from the fluctuation–dissipation theorem plus dimensional
analysis, and matches Blencowe 2013; the O(1) factor c₀ is not fixed here.
- I took the arms' energy difference ΔE = 2.84×10⁻¹⁹ J (Sr clock transition),
  which is the most favourable case.
- I took t = 1 s and a visibility sensitivity of 10⁻³. **Both are parameters I
  chose, not instrument specifications.**

| Spacetime "bath" | T | Γ in 1 s | Enhancement over GR needed |
|---|---|---|---|
| Cosmic graviton background (LIT prediction, unobserved) | 0.905 K | 2.5×10⁻⁴⁵ | **4×10⁴¹** |
| Unruh temperature of a lab at g = 9.81 m/s² | 4.0×10⁻²⁰ K | 1.1×10⁻⁶⁴ | 9×10⁶⁰ |
| de Sitter horizon | 2.2×10⁻³⁰ K | 6×10⁻⁷⁵ | 1.6×10⁷¹ |
| A deliberately absurd 300 K graviton bath | 300 K | 8×10⁻⁴³ | 1.2×10³⁹ |

**Verdict:** to show up at MAGIS-100 or AION, STUR's "spacetime resistance"
would have to couple to matter at least **10³⁹–10⁴¹ times more strongly than
gravity**. That cannot come from rewriting known physics. It needs new structure,
and that is your decision.

## The choice: what new structure, if any

Each option, with the known constraint it must beat first:

| Option | Physical content | First constraint to beat |
|---|---|---|
| **A. Enhanced spacetime decoherence** | Spacetime records which-path information at a rate F × GR, with F ≥ 10⁴¹ | The Diósi–Penrose class of gravitational-collapse models. Its parameter-free version is already excluded by underground radiation searches (LIT: Donadi et al. 2021). |
| **B. A new field coupling to neutral atoms** | A light field, ideally confining at short range, that atoms feel | Equivalence-principle tests, η ≲ 10⁻¹⁵ (LIT: MICROSCOPE), and fifth-force searches |
| **C. Modify the horizon row** | Corrections to S = A/4G, or to Bisognano–Wichmann near horizons | Black-hole and gravitational-wave observations; nothing in the lab |
| **D. No new structure** | Write STUR up as the synthesis found here: one replica equation for horizons, confinement, decoherence and thermodynamics, with the lattice evidence | None. Honest, but not new physics. |

Whichever option you choose, I'll specify the new structure minimally, check it
against the first constraint in its row, and compute its MAGIS-100 or AION signal.
