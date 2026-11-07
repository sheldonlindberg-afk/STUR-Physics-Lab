# The god-equation search: running log

## Ground rules (unchanged)

Hostile referee throughout. Every claim is labelled KNOWN, FOLLOWS, STUR/NEW, CHECK or
LIT; every number is computed in code; negative results are recorded plainly.

## What "god equation" can mean

- **Already exists:** the Standard Model plus general relativity, written as one
  path integral (the "Core Theory"). It describes every experiment on Earth. The
  replica/first-law equation from WALL.md is a corollary of it.
- **Missing:** an equation that also accounts for quantum gravity, the cosmological
  constant and dark energy, dark matter, and the values of the constants.
  Nobody has it.
  
The search therefore attacks one open gap at a time, looking for a candidate
equation that makes a prediction data can decide.

## Front 1: dark energy from holography (STUR's founding axiom)

Script: `src/god_eq_dark_energy.py`; output: `results/god_equation/dark_energy.txt`.

**Candidate (KNOWN, Li 2004):** ρ_de = 3c²M_P²/L², with L the future event horizon.
This is the holographic axiom applied to the whole universe, with one parameter c.

**Data (LIT, DESI DR2 + CMB + supernovae).** These are fits of the equation of state
in the form w(a) = w₀ + wₐ(1 − a):
- with DESY5 supernovae: w₀ = −0.752 ± 0.057, wₐ = −0.86;
- with Union3: w₀ = −0.667 ± 0.088, wₐ = −1.09.

The preference over a cosmological constant is 2.8–4.2σ, depending on the supernova
sample. σ(wₐ) and the w₀–wₐ correlation were not retrieved; I assume σ(wₐ) = 0.25.

**Result (FOLLOWS, exact).** dw/d ln a = −(1/3c)·√Ω(1 − Ω)(1 + 2√Ω/c) < 0 for every
c > 0. So holographic dark energy always has **wₐ > 0**:

| c | w₀ | wₐ |
|---|---|---|
| 0.5 | −1.47 | +1.15 |
| 1.0 | −0.90 | +0.38 |
| 2.0 | −0.62 | +0.13 |

DESI wants wₐ ≈ −0.9. The model tends to w → −1/3 in the past, while DESI's fit
implies w ≈ −1.6 to −1.8 then. The model crosses w = −1 in the opposite direction.
With the assumed σ(wₐ), that's a 4–8σ mismatch in wₐ.

**Verdict:**
- If DESI's evolving dark energy is real, the simplest holographic equation is
  **disfavoured**: it moves away from ΛCDM in the wrong direction.
- If the DESI signal turns out to be a supernova systematic, the model is merely
  unconstrained here, with c ≈ 1.2–1.5 matching w₀.
- Caveats: the comparison uses only the CPL projection and no full likelihood. I
  haven't checked the published fits of holographic dark energy to DESI.

**What this tells the search:** a holographic equation would have to produce w < −1
in the past and w > −1 today. Plain horizon holography gives the reverse.

## Front 2: running vacuum, the bridge from our own equation

Script: `src/god_eq_running_vacuum.py`; output: `results/god_equation/running_vacuum.txt`.

**R1: our equation's own bridge is dead (FOLLOWS).** The species running of the
horizon tension (U3), evaluated at the cosmic scale μ = H, changes G by
δG/G = 4cN(H₀/M_P)² = 1.3×10⁻¹²³ per scalar field. **Our unified equation predicts
nothing for dark energy.**

**R2: the running-vacuum family (KNOWN; Shapiro & Solà).** Vacuum energy slowly
exchanges with matter: ρ_vac(H) = ρ₀ + (3ν/8π)M_P²(H² − H₀²). In this model matter
isn't separately conserved. An analysis that assumes it is would infer an
effective w₀ and wₐ:
- **ν > 0 lands in DESI's quadrant** (w₀ > −1, wₐ < 0), and ν < 0 in the opposite
  one. That is the right direction, unlike front 1.
- The model never crosses w = −1 over 0.3 < a < 1.
- Matching DESI's w₀ = −0.75 needs **ν ≈ 0.13**, which then gives wₐ = −2.1. From
  ν ≈ 0.03 upward, the inferred dark-energy density turns negative in the past.

**R3: the early universe kills the size.** Matter then scales as a^(−3(1−ν)), so at
recombination the matter density is off by a factor a^(3ν). For ν = 0.13 that factor
is 0.06: a 16× deficit. Planck pins Ω_c h² to about 1% (LIT: 0.120 ± 0.001), which
requires |ν| ≲ 4.8×10⁻⁴. At that ν, w₀ = −0.9994 and wₐ = −0.006: **about 0.2% of
the DESI signal.**

The 1% criterion is crude. It ignores parameter degeneracies, and I haven't checked
the published running-vacuum fits. But the gap is a factor of 277.

**Verdict:** the running vacuum has the right *sign* for DESI but is about 300×
too weak once the CMB is respected. Our unified equation doesn't feed it at all.

## What two fronts have taught the search

DESI's hint needs dark energy that is phantom in the past (w < −1) and above −1
today, *without* changing the early universe. Neither a horizon-holographic density
(wrong direction) nor a vacuum–matter exchange (right direction, CMB-limited)
does this. Simple vacuum-energy equations can't produce it; it needs a dynamical
field or a late-time-only effect. The DESI signal itself may also shrink, since it
depends on the supernova calibration.
