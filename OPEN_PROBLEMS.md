# STUR open problems #2–#7 tested against known physics

Reproduce: `python3 src/stur_open_problems.py` (about 15 s). The full output is
in `results/open_problems/output.txt`, and `tests/test_open_problems.py` pins
the numbers. Every number below comes from that output.

Labels:
- **KNOWN:** published and tested;
- **FOLLOWS:** derived with no new assumption;
- **STUR:** a new claim or identification;
- **CHECK:** reproduces a known exact result;
- **LIT:** a literature value used as input, not recomputed here.

No new structure was added. Each problem was answered by testing the options
that already exist in the literature.

## Summary

| # | Problem | Result |
|---|---|---|
| 2 | Which connection A_μ is | **No known connection works.** None meets all five requirements. The two ends of the equation need different fields. |
| 3 | Derive σ(μ) | **Not derived.** The factor 1.9×10³⁸ is (E_P/√σ_QCD)², which is dimensional analysis. The nearest known running quantity misses σ_Planck by ×9.9 (QCD alone) or ×4.1 (QCD plus gravity). |
| 4 | Same kind of area? | **No**, in 4D general relativity plus QCD. The QCD area is *spanned* by the loop; the horizon area is *linked* by it. Gravity's relation is also linear in Φ, where STUR's is quadratic. The one exception is AdS/CFT, which needs Λ < 0. |
| 5 | Quark quantum numbers from folds | **Negative.** Folds give baryons (nucleon and Δ reproduced). A B = ⅓ fold has energy 0.18 E_P. Colour, flavour and generations don't appear. |
| 6 | ρ_c and R(ρ) in terms of Φ_R | **Written down, but only by renaming known results.** Φ_max² = 3ρ_P/(4ρ) and R = 3ρ_P/(8ρ). The trigger "emptiness causes tunnelling" runs opposite to the known tunnelling calculation. |
| 7 | Information paradox | **STUR reproduces the paradox rather than resolving it.** After the Page time, the postulate and the bound (line 4) contradict each other. |

## P2. Which connection is A_μ?

The equation as written needs a field with five properties:
- **R1:** its holonomy is a gauge connection;
- **R2:** its noise is Gaussian;
- **R3:** it gives an area law at the QCD scale;
- **R4:** it gives horizon entropy A/4ℓ_P²;
- **R5:** it couples to a neutral-atom interferometer, as any lab test needs.

**Computed checks:**

- **Electromagnetism in 4D gives a perimeter law, not an area law** (KNOWN). For
  square loops from L/a = 10 to 160, ⟨Φ²⟩/(4L) settles to 0.0071 while ⟨Φ²⟩/L²
  falls by 12×. A fit gives an area coefficient of −4×10⁻⁹, consistent with zero.
- **An area law needs a field with a finite correlation length** (KNOWN; this is
  the stochastic vacuum model). For a Gaussian field strength with correlation
  length ξ, ⟨Φ²⟩/(C₀πξ²L²) goes 0.0032 → 0.24 → 0.89 → 0.99 at L/ξ = 0.1, 1,
  10, 100. Massless fields such as the photon or graviton can't do this.
- **Loop quantum gravity's horizon entropy is fitted, not derived.** The Immirzi
  parameter γ is chosen to make S = A/4ℓ_P² come out:
  - 0.127384 (ABCK);
  - 0.237533 (Meissner);
  - 0.274067 (Ghosh–Mitra).
  
  All three are reproduced (LIT). So the ¼ is an input there.
- **Phases in a Rb-87 interferometer like MAGIS (T = 1 s):**
  - Ordinary gravity (the COW phase) gives 1.58×10⁸ rad.
  - The spin-connection holonomy from Earth's curvature (3.4×10⁻²³ m⁻²) gives a
    1.0×10⁻¹⁴ boost angle.
  - Vacuum graviton fluctuations at 1 m scale as (ℓ_P/L)² = 2.6×10⁻⁷⁰.
  - Electromagnetism and colour give 0: the atom is neutral and a colour singlet.

| Candidate | R1 | R2 | R3 | R4 | R5 |
|---|---|---|---|---|---|
| U(1) electromagnetism | ✓ | ✓ | ✗ (perimeter law) | ✗ | ✗ |
| SU(3) colour | ✓ | ≈ (lattice) | ✓ | ✗ | ✗ |
| Levi-Civita spin connection | ✓ | ✗ | ✗ | ✓ exactly, **but linear in Φ** (P4) | tiny |
| Ashtekar–Barbero SU(2) | ✓ | ✗ | ✗ | ✓ only by fitting γ | ✗ |
| TEGR translational potential B⁰_μ ([TEGR.md](TEGR.md)) | ✓ | ✓ (free field; tiny) | ✗ (perimeter law) | ✓ as in GR (smooth horizon) | ✓ (COW phase) |
| New field | must be confining at 1 fm *and* couple to neutral atoms | | | | |

**Verdict: no known connection meets R1–R5.** The QCD end needs a colour field
with a mass gap; the horizon end needs gravity. Asking one A_μ to do both is the
same problem as P3. Specifying a new field would be new structure, so I haven't
done it.

## P3. σ(μ)

- **CHECK:** σ_Planck/σ_QCD = 1.9248×10³⁸ = (E_P / (2 × 0.44 GeV))², to every
  digit printed.
- **The two endpoints are just dimensional analysis.** Divide each tension by the
  square of its own energy scale. Both come out O(1): 1 at the QCD end and 0.25 at
  the Planck end. The QCD value of 1 is circular, because μ was chosen as √σ. So
  the 38 orders of magnitude are (E_P/√σ_QCD)². A formula σ = c·μ² spans them
  automatically: its β(σ) = 2σ is just the engineering dimension (FOLLOWS).
- **The hierarchy itself is KNOWN physics** (dimensional transmutation).
  Two-loop Standard Model running from α_s(M_Z) = 0.1180 gives:
  - α_s(m_τ) = 0.313;
  - α_s(10¹⁰ GeV) = 0.0339;
  - **α_s(E_P) = 0.01886**.
- **Candidate flow: the Creutz ratio.** This is the static force between test
  charges at separation r = 1/μ, a known way to measure an effective string
  tension at scale μ:

  χ(μ) = C_F α_s(μ) μ² + σ_QCD, with C_F = 4/3.

  At μ = E_P:
  - **QCD alone** gives 0.0251 E_P², short of the required 0.25 E_P² by **×9.9**.
    It would need α_s(E_P) = 0.1875; the Standard Model gives 0.0189.
  - **The gravitational analogue** between quanta of energy μ at r = 1/μ (μ⁴/E_P²)
    gives 1 E_P². Adding it to QCD overshoots by **×4.10**.

**Verdict: σ(μ) is not derived, and nothing known lands on 1/(4ℓ_P²).** The real
content of the STUR hypothesis would be the dimensionless function σ/μ², which
goes from 1 to ¼, and there is no mechanism for that.

## P4. Are the QCD area and the horizon area the same kind?

- **CHECK:** In Euclidean Schwarzschild, the holonomy of the spin connection
  around the thermal circle at the horizon is exactly **2.0000000000 π** for every
  mass tested. This smoothness condition is what fixes T_H.
- **CHECK** (KNOWN; Susskind–Uglum, and Bañados–Teitelboim–Zanelli 1994). Let the
  holonomy be 2πn, as in the replica trick. Then
  ln Z_n ⊃ (1−n)·2π·A/(8πGħ), and the entropy that follows gives
  S/(A/4ℓ_P²) = **1.0000000000**.

**Two differences in structure** (FOLLOWS):
1. **Linear vs quadratic.** In gravity, ln Z is *linear* in the holonomy, with
   coefficient A/8πG, much like an Aharonov–Bohm phase. In QCD, ln W is
   *quadratic* in the phase fluctuation, with coefficient σ.
2. **Linked vs spanned.** The horizon area lies *across* the plane of the loop:
   the loop *links* the horizon, as an Aharonov–Bohm loop links a flux tube. The
   QCD area is the area the loop *spans*.

**Verdict: they are different kinds of area.**

The known exception is AdS/CFT. There, Wilson loops are string worldsheets
(tension 1/2πα′) and entropies are Ryu–Takayanagi surfaces (tension 1/4G). Both
are minimal surfaces in the bulk, and in a 4D bulk both are 2-surfaces. That is
the nearest known version of "one area law, two tensions". But it needs Λ < 0,
and our universe has Λ > 0.

This also bears on lines 4–5 of the STUR equation. The Smarr check there pairs
the horizon area with ½Φ², while Euclidean gravity pairs it with Φ.

## P5. Quark quantum numbers from folds

**CHECK.** The hedgehog profile was solved as a boundary-value problem with the
correct 1/r² tail. It gives:
- E/(12π²) = **1.231446** (LIT 1.2314);
- moment-of-inertia integral 50.979 (LIT, Adkins–Nappi–Witten (ANW) 50.9).

Fitting to the nucleon N(939) and the Δ(1232) gives e = **5.445** and
F_π = **129.3 MeV** (ANW: 5.45 and 129 MeV).

**What folds do give** (KNOWN):
- **Quantum numbers:** baryon number B = 1 and spin = isospin = ½ or 3/2.
- **Charges:** the formula Q = I₃ + B/2 gives charges **+1, 0** (nucleon) and
  **+2, +1, 0, −1** (Δ). All are integers.
- **Spin ½ is circular for this purpose.** It requires the Wess–Zumino–Witten
  term, which gives J = N_c·B/2 mod 1 (Witten 1983). So a fermionic fold needs
  **N_c = 3 colours as input**, and colours are exactly what quarks are supposed
  to explain.

**What a fractional fold would cost** (FOLLOWS). A hedgehog with B = ⅓ needs a
central angle θ = 1.302663 rad.
- Putting B = ⅓ and I = ½ into the same formula would give charges +2/3 and −1/3,
  the up- and down-quark charges. But only because B = ⅓ was put in by hand.
- Such a field is singular at r = 0. Its core energy grows as 4π sin⁴θ/ε =
  10.86/ε, where ε is the core cutoff; ε·E is 6.16, 10.02, 10.74 and 10.85 as ε
  falls.
- With a Planck-length cutoff the core energy is **2.2×10¹⁸ GeV = 0.18 E_P**.
  Quark masses are 0.002–173 GeV.

**Verdict: folds give baryons, not quarks.** Colour, flavour and three
generations don't come out at all.

## P6. Bounce density and barrier in terms of Φ_R

**The bound on the Hubble sphere** (FOLLOWS, exact). Apply line 4 to the Hubble
sphere: **Φ_max²(ρ) = 3ρ_P/(4ρ)**. The direct calculation agrees to 7 digits at
ρ/ρ_P = 10⁻⁹, 10⁻⁶⁰ and 10⁻¹²⁰.

**The bounce density** (KNOWN within loop quantum cosmology, LQC):
ρ_c = √3/(32π²γ³) ρ_P = **0.4092 ρ_P**, using γ = 0.237533.
- In STUR variables: **ρ_c = 3ρ_P/(4Φ_c²)** with **Φ_c² = 1.8328**.
- So the bounce happens when the Hubble sphere holds Φ² ≈ 2. But Φ_c is set by
  γ, not by STUR.

**The barrier.** Tunnelling with "no parent vacuum" is KNOWN as Vilenkin's
creation from nothing (1982), with probability P ∝ exp(∓S_dS) and
S_dS = 3ρ_P/(8ρ). Here S_dS is the entropy of a de Sitter horizon.
- Identifying the barrier with half the ceiling (STUR identification) gives
  **R(ρ) = ½Φ_max²(ρ) = 3ρ_P/(8ρ)**.
- At the bounce R(ρ_c) = 0.9164, so the barrier is gone there (FOLLOWS).
- Today ρ_Λ/ρ_P = 1.13×10⁻¹²³ and R = **3.3×10¹²²**.

**What this contradicts:**
- **Emptiness doesn't trigger tunnelling.** R grows as ρ shrinks, so an emptier
  universe faces a *higher* Vilenkin barrier. With the opposite (Hartle–Hawking)
  sign, an empty de Sitter universe is the most probable outcome of creation, but
  that still isn't a trigger.
- **The bounce and the trigger can't be the same event.** The LQC bounce happens
  at high density, while the STUR trigger is at near-zero density. The two
  densities differ by **3.6×10¹²²**.

## P7. Information paradox

**CHECK.** With Page's ratio of radiation entropy to black-hole entropy lost,
1.4847 (LIT), the Page time is t_Page/t_evap = **0.5381**, matching the
literature value of 0.5381.

**Unitarity** (KNOWN) requires the fine-grained radiation entropy to follow the
Page curve: S = min(1.4847·(S₀ − S_BH), S_BH). The 2019 island calculations
reproduce this.

**What STUR does instead.** STUR's S_R = −ln V. For Gaussian baths this is
monotone and unbounded (POSTULATE_TEST.md), so it follows the *coarse-grained*
curve, which keeps rising. Line 4 caps it at S_BH(t), and that cap is violated at
every time after the Page time:

| t/t_evap | S_R / S₀ (rises) | Cap S_BH / S₀ (falls) |
|---|---|---|
| 0.60 | 0.679 | 0.543 |
| 0.80 | 0.977 | 0.342 |
| 0.95 | 1.283 | 0.136 |
| 0.999 | 1.470 | 0.010 |

These two lines of the STUR equation contradict each other once the hole is past
its Page time. The only escape is for Φ_R² to be a fine-grained entropy, and
ASSUMPTIONS.md shows it isn't one. Plot: `results/open_problems/page_curve.png`.

**The background picture also needs revising.** The final de Sitter horizon holds
**3.3×10¹²² k_B** of entropy. Coarse-grained entropy only grows (the second law),
while the fine-grained entropy of a closed universe evolving unitarily stays
constant (KNOWN). So "the universe ends with almost no information" is either
false (coarse-grained) or always true (fine-grained). Either way, it can't be a
trigger.

**Verdict: STUR as written reproduces Hawking's paradox, not its resolution.**

## What this means for the program

Taken together with POSTULATE_TEST.md and ASSUMPTIONS.md, every piece that
checks out is known physics under a new name:
- Gaussian Wilson loops;
- area laws from gapped fields;
- the Euclidean-horizon holonomy;
- skyrmions;
- the LQC bounce;
- Vilenkin tunnelling;
- the Page curve.

Every STUR-specific link has failed a computed test, and each failure lands on
one of three things:
1. the postulate S = −k_B ln V;
2. the use of a single A_μ and a single σ(μ) across scales;
3. the step from an empty universe to tunnelling.
