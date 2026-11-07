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

## Front 3: a quark as a folded, twisted area of spacetime

Script: `src/god_eq_quark_fold.py`; output: `results/god_equation/quark_fold.txt`.

**The fold equation.** Take a closed surface (the fold) threaded by flux Φ (the twist),
with a charge q bound to it. The field around them stores angular momentum

**J = qΦ/4π**  (Thomson 1904, KNOWN; Heaviside–Lorentz units with ħ = c = 1)

Single-valuedness requires qΦ = 2πn (Dirac 1931, KNOWN), so **J = n/2**. The STUR
claim is that a quark is the n = 1 fold.

**F1 CHECK.** Numerically, J = 0.079577471546 = 1/4π at separations of 0.5, 1 and 3,
agreeing to 12 digits. Spin ½ really does come from folding and twisting, and
the size of the fold doesn't matter.

**The quark checklist:**

| Property | Result |
|---|---|
| Spin ½ | **Yes**, from an odd Dirac twist (n = 1) |
| Charge ⅓ | **No.** A one-third twist (the Z₃ colour centre, the source of fractional charge via Q ≡ ⅔·triality mod 1, which I verified for u, d, ū, e, ν, g, W) gives J = 1/6 or 1/3, which is forbidden for an isolated object. The twist that makes ⅓ can't be the twist that makes spin ½. |
| Baryons | **No-go with electromagnetic flux.** Three spin-½ folds need odd n each, and three odd numbers can't sum to zero: none of the triples in [−7, 7] does. Every proton would be a magnetic monopole. |
| Colour | **No-go with colour-magnetic flux.** The minimal consistent fold gives "spin" 1, −½, −½ to the three colours, which breaks exact SU(3). Spin-from-isospin (Jackiw–Rebbi) needs an adjoint Higgs that QCD doesn't have. |
| Generations | **No.** Higher twists give J = 3/2, 5/2, …: higher spin, not heavier spin-½ copies. |
| Mass | **No.** An electromagnetic fold has E = 17.13ħc/r_c. An up quark (2.16 MeV) would need r_c = 1565 fm, which is 1,900 proton radii. Compositeness bounds (r_c ≲ ħc/20 TeV; an approximate literature value) force E ≳ 343 TeV, so the mass needs cancellation to 6×10⁻⁹. A pure-spacetime fold (spinorial geon, Friedman–Sorkin 1980) sits at the Planck scale: m_u/E_P = 1.8×10⁻²². |

**Verdict:**
- **What works:** the fold equation *does* turn a twist into intrinsic spin ½. That
  part of the picture is real physics; charge–monopole composites are fermions
  (KNOWN).
- **What fails:** a quark can't be such a fold. Fractional charge, baryon
  neutrality, colour symmetry, generations and mass each fail. The mismatch is
  structural: spin ½ needs a *full* twist (2π), while fractional charge needs a
  *one-third* twist (2π/3).
- **What a successful fold equation would have to do:** produce spin ½ and a Z₃
  phase from the *same* geometry. In known physics these come from different
  places (the Lorentz group and the centre of SU(3)).

## Front 4: one twist that does both (spin ½ and the thirds)

Script: `src/god_eq_spin_charge.py`; output: `results/god_equation/spin_charge.txt`.

**Question.** Is there one gauge twist g that acts as (−1)^F (−1 on every fermion, +1
on every boson)? A fold carrying g would then set statistics from charge.

**S1 CHECK.** The Standard Model's Z₆ element (ω, −1, e^{2πiY}) acts trivially on every
field, to 10⁻¹⁶.

**S2: no such twist in the Standard Model's gauge group.** The best mismatch is 2.0.
ν_R has nothing to flip its sign. Even without ν_R the mismatch is 1.62: e_R forces a
half-integer hypercharge angle, which then gives the Higgs a phase of ±i.

**S3: with gauged B−L there is one.** (−1)^{2J} = exp(3πi(B−L)) on every field. This is
the KNOWN spin–charge relation, the centre element −1 of Spin(10). A smaller twist also
works, B−L angle π *combined with the colour centre ω*: for quarks, ω·e^{iπ/3} = −1.
**One combined twist carries both the colour ⅓ and the fermion sign.**

**S4: the fold built from it.**
- A pure B−L fold needs flux 6π to be Dirac-consistent, because quark B−L = ⅓. It shifts
  the angular momentum of anything bound to it by J = 3(B−L)/2 mod 1, which is right for
  every case tested: quark ½, lepton ½, Higgs 0, meson 0, diquark 0, baryon ½,
  pentaquark ½.
- **S4b, the minimal combined fold:** colour-centre twist k = 2 plus B−L flux 2π. It gives
  quarks *and* leptons exactly J = ½, and the scalar S an integer. The colour twist is
  what makes the ⅓ B−L charge Dirac-consistent.
- **This object is known.** The minimal grand-unified monopole carries colour-magnetic
  flux that compensates fractional charges (LIT, recalled: Dokos–Tomaras 1980 for
  SU(5)).

**S5: the twist doesn't force the thirds.** S3 allows quark B−L = (2m + 1)/3, so ⅓, 1,
5/3, … are all consistent. The thirds come from **N_c = 3** through anomaly cancellation
(N_c·Y_Q + Y_L = 0, which gives Q_u = 2/3 and Q_d = −1/3 only for N_c = 3; computed for
N_c = 1–5).

**S6: the baryon no-go survives** if the quark *is* the fold. Three odd twist numbers
never cancel, and B−L flux is confined, so an uncancelled fold would drag an infinite
string.

**Verdict:**
- **What works:** "one twist that does both" exists, and its minimal form is a colour-
  centre twist plus B−L flux. It gives every quark and lepton spin ½ and every boson
  integer spin. **The precise version of the fold idea is the grand-unified monopole: the
  fold is the monopole, and the quark is what the fold acts on, not the fold itself.**
- **What doesn't:** colour SU(3) and its N_c = 3, which fixes the thirds, are inputs;
  generations and masses are untouched; and quark-as-fold fails on baryons.
- **What's left to explain:** *why N_c = 3*. That single number fixes the thirds, the
  Z₃ twist and the baryon's three quarks.
