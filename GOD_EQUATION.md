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

## Front 5: why three colours?

Script: `src/god_eq_why_three.py`; output: `results/god_equation/why_three.txt`.

Each route is labelled **THEORY** (a theoretical selection) or **OBSERVATION**.

| Route | Result | Kind |
|---|---|---|
| W1: Witten's global SU(2) anomaly | each generation has N_c + 1 doublets, which must be an even number, so **N_c must be odd** | THEORY |
| W2: perturbative anomalies + Yukawas, solved symbolically | Q_u = (N_c + 1)/2N_c, Q_d = (1 − N_c)/2N_c; the cubic anomaly vanishes for *every* N_c. Anomalies fix the charges *given* N_c, not N_c. | THEORY (no selection) |
| W3: front 4's spin–charge relation, (−1)^F = exp(iπN_c(B−L)) | works only for odd N_c, the same condition as W1. **The twist and Witten's anomaly agree.** | THEORY |
| W4: asymptotic freedom with 6 flavours | b₀ > 0 for any N_c ≥ 2; only a lower bound (a strong force has to exist) | THEORY (lower bound) |
| W5: front 4's minimal fold | works for every N_c, with colour twist k = N_c − 1 | no selection |
| W6: π⁰ → γγ | N_c(Q_u² − Q_d²) = 1 for *every* N_c (KNOWN, Bär–Wiese) | blind to N_c |
| W6: R-ratio below charm, vs KEDR 2.225 ± 0.051 (LIT) | N_c = 1: −24σ · 2: −15σ · **3: −1.0σ** · 4: +16σ · 5: +33σ · 7: +73σ | **OBSERVATION picks 3** |

R uses N_c-dependent charges and α_s(2.45 GeV) = 0.272 from our two-loop running. α_s
would itself shift with N_c, but that can't absorb a 15–33σ miss.

**Verdict:**
- **Theory gives:** N_c odd (two independent routes, Witten's anomaly and the twist,
  which agree), plus N_c ≥ 2 if a strong force exists at all. So N_c ∈ {3, 5, 7, …}.
- **Observation picks 3** (the R-ratio). Three is the *smallest* value theory allows,
  but nothing derived here forces minimality.
- **This is a wall.** "Why 3 and not 5" has no theoretical answer in known physics or
  in anything built here. A god equation would have to supply a principle that selects
  the minimal odd value, or fix N_c some other way.

## Front 6: why three generations? (3-3-1 models)

Script: `src/god_eq_three_generations.py`; output: `results/god_equation/three_generations.txt`.

**Framework (KNOWN; Pisano–Pleitez, Frampton 1992).** The gauge group is
SU(3)_C × SU(3)_L × U(1)_X: the weak SU(2) is enlarged to SU(3)_L, so each
generation's left-handed fields come in triplets.

**G1 + G2 (computed).** The SU(3)_L anomaly requires as many triplets as
anti-triplets: N_g(1 + N_c) = 2nN_c, where n is the number of quark generations in the
anti-triplet. QCD stays asymptotically free only if the 3N_g quark flavours satisfy
11N_c/3 − 2N_g > 0. Together:

| N_c | Generation numbers the anomaly allows | Allowed by asymptotic freedom too |
|---|---|---|
| 3 | 3, 6, 9, … | **3** |
| 5 | 5, 10, … | **5** |
| 7 | 7, 14, … | **7** |

**The generation number is locked to the colour number: N_g = N_c.** For N_c = 3 the
counting reproduces the standard assignment: two quark generations in the anti-triplet,
one in the triplet.

**G3, with front 5.**
- **One number, not two.** N_c must be odd (Witten's anomaly and the spin–charge twist),
  and 3-3-1 sets N_g = N_c, so the two "threes" are a single number.
- **The data agree.** The measured N_g = 3 (LEP neutrino counting, LIT, recalled) and the
  R-ratio (N_c = 3) both say 3.
- **Still open:** why that number is 3 and not 5 or 7.

**G4: the minimal model vs data.**
- Running the Standard Model couplings at one loop, sin²θ_W reaches ¼ at
  **μ* = 3.68 TeV**. There the U(1)_X coupling diverges, so the minimal model's new gauge
  bosons must sit below about 3.7 TeV. The literature quotes a similar cap
  (m_Z′ ≲ 3.1 TeV, LIT).
- LHC dilepton searches exclude a minimal-model Z′ below 5 TeV (LIT).
- So **minimal 3-3-1 is excluded**, unless two-loop and threshold effects, which I didn't
  compute, raise μ* by 36%.
- The β = ±1/√3 variants have no such pole. The N_g = N_c result holds there too (same
  triplet counting), with Z′ > 3.6–4.2 TeV (LIT): **alive and testable**.

**Verdict:**
- **Real result:** both "threes" reduce to one number, linked *by theory*. That number
  must be odd (front 5), and the generations must equal the colours (3-3-1 + asymptotic
  freedom).
- **Excluded:** the minimal version that first gave this argument.
- **Surviving:** the β = ±1/√3 versions, which predict new heavy gauge bosons (a Z′ and
  bileptons) within the LHC's long-term reach.
- **The wall moves but doesn't fall:** why that one number is 3 is still decided by
  observation.

## Front 7: running couplings select N_c = N_g = 3 (conditional)

Script: `src/god_eq_su3L_running.py`; output: `results/god_equation/su3L_running.txt`.

**Assumption (labelled):** the theory stays perturbative, with no Landau pole, up to the
Planck scale. This is a standard criterion, not a theorem.

**L1–L3: SU(3)_L (one loop, computed).** With N_g = N_c there are N_c(1 + N_c) Weyl
triplets, and the running coefficient is b_L = 11 − N_c(1 + N_c)/3 − (scalar terms).
Starting from 1/α_L(4 TeV) = 31.5:

| N_c | b_L (3 scalar triplets) | Landau pole |
|---|---|---|
| 3 | +6.5 | none (asymptotically free) |
| 5 | +0.5 | none (asymptotically free) |
| 7 | −8.2 | 1.3×10¹⁴ GeV, below the Planck scale |
| 9 | −19.5 | 10⁸ GeV |

Adding the minimal model's sextet gives the same verdict: N_c = 5 then has a pole at
10²⁶¹ GeV, harmless. **So SU(3)_L cuts every N_c ≥ 7; theory leaves {3, 5}.**

**L4: hypercharge (ESTIMATE).** This is hypercharge-equivalent running with front 5's
N_c-dependent charges, one exotic quark per generation (β = −1/√3 pattern) and only the
Standard Model Higgs among scalars. The method reproduces the Standard Model's b_Y = −41/6
exactly.

| Content | b_Y | Landau pole |
|---|---|---|
| N_c = N_g = 3, with exotics | −9.50 | 4.7×10³⁰ GeV: **above** the Planck scale |
| N_c = N_g = 5, with exotics | −22.17 | 1.6×10¹⁵ GeV: **below** the Planck scale |
| N_c = N_g = 7 | −24 to −40 | 10¹⁰–10¹⁴ GeV: below |

**Robustness.** A pole exactly at the Planck scale corresponds to |b_Y| = 16.61:
- N_c = 3 would flip only if |b_Y| grew by 7.1;
- N_c = 5 would flip only if it shrank by 5.6.

The three scalar triplets add roughly 1–2 (not computed exactly). The true U(1)_X charges
would shift b by O(1). Neither is large enough to flip either verdict.

**Verdict, conditional on the framework (3-3-1, β = ±1/√3 type) and the assumption
(perturbative to the Planck scale):**
- Witten's anomaly (front 5) requires N_c odd.
- The SU(3)_L anomaly plus QCD asymptotic freedom (front 6) gives N_g = N_c.
- SU(3)_L perturbativity removes N_c ≥ 7.
- Hypercharge perturbativity removes N_c = 5.
- **That leaves exactly N_c = N_g = 3:** the colours, the generations, and through
  anomalies the ⅓ charges, all from one chain of consistency conditions.

**Status:**
- **Known vs new:** N_g = 3 from 3-3-1 is KNOWN (Frampton). Extending the chain to fix N_c
  as well, using N_c-dependent charges and Landau poles, is this project's step. I haven't
  checked whether it is in the literature.
- **Not computed:** the hypercharge step is an estimate; two-loop terms, the exact X
  charges and the full scalar content are open.
- **Assumption-dependent:** a Landau pole below the Planck scale only signals new physics,
  not inconsistency. Drop the assumption and the selection drops with it.
- **What decides the framework:** the β = ±1/√3 3-3-1 models predict a Z′ and bileptons,
  which the LHC (now) and future colliders can find or exclude.

## Front 7b: firming up "N_c = N_g = 3": exact charges, full scalars, two loops

Script: `src/god_eq_331_exact.py`; output: `results/god_equation/331_exact.txt`.

**Model.** The β = −1/√3 3-3-1 model, with N_g = N_c and quark charges from front 5. The
exact U(1)_X charges come from Q = T3 + βT8 + X:
- quark triplet: X = Q_u − ⅓;
- quark anti-triplet: X = Q_d + ⅓;
- leptons: −⅓;
- scalars η, ρ, χ: −⅓, +⅔, −⅓. These are fixed by the Yukawa couplings and don't depend
  on N_c.

**E1 CHECK (calibration).** The general two-loop gauge machinery reproduces the Standard
Model's one-loop coefficients (41/10, −19/6, −7) and **all nine two-loop entries exactly**.
The calibration caught two errors of mine: a GUT-normalisation bug, and the scalar
normalisation, which must count a complex scalar as two real degrees of freedom.

**E2 CHECK.** Every gauge anomaly (X³, grav²X, SU(3)_L²X, SU(N_c)²X, SU(3)_L³) vanishes
exactly for N_c = 3, 5 and 7, so the general-N_c model is consistent.

**E3: two-loop gauge running from the 3-3-1 scale.** Starting from 1/α_X(4 TeV) = 83.76;
"blow-up" means a coupling reaching g = 4π.

| N_c = N_g | one-loop a_X | Blow-up (2-loop) | vs Planck |
|---|---|---|---|
| 3 | 26/3 = 8.67 | 3.0×10²⁹ GeV | **above** |
| 5 | 19.33 | 1.3×10¹⁵ GeV | **below** |
| 7 | 34.44 | 9.7×10⁹ GeV | below |

- **Stable across the 3-3-1 scale.** For μ_331 = 2–30 TeV, N_c = 3 blows up at
  (2.7–3.7)×10²⁹ GeV and N_c = 5 at (0.8–4.5)×10¹⁵ GeV.
- **Margins.** A pole exactly at the Planck scale needs a_X = 14.76; the margins are
  +6.09 for N_c = 3 and −4.57 for N_c = 5. Charges and scalars are now exact.
- **Not included:** two-loop Yukawa terms. They enter only at two loops, and the verdict
  is already set at one loop.
- **Cross-check:** a_X = 26/3 for N_c = 3 matches the value I recall from the literature
  (not retrieved).

**Literature (one search).** The link between generations and colours via anomaly
cancellation is KNOWN (N_g divisible by N_c), as are the minimal model's ~4 TeV pole and
the β = 1/√3 model's high-energy U(1) pole. No source found derives N_c *itself* through
perturbativity. Not a novelty proof.

**Firmed-up verdict.** In the β = −1/√3 3-3-1 framework, requiring the theory to stay
perturbative up to the Planck scale, the chain

  Witten's anomaly (N_c odd) → SU(3)_L anomaly + QCD asymptotic freedom (N_g = N_c) → U(1)_X running

**selects N_c = N_g = 3 uniquely.**

Still conditional on:
1. the 3-3-1 framework, decided by collider searches for its Z′ and bileptons;
2. the perturbativity assumption;
3. this β value. The β = +1/√3 variant hasn't been checked.

## Front 7c: the other viable variant (β = +1/√3)

Same script, section E4. Exact charges for general N_c:
- lepton triplets (ν, e, E⁻) with X = −⅔, plus a heavy charged lepton E;
- quark triplet X = Q_u − ⅔, with a d-like exotic quark;
- quark anti-triplet X = Q_d + ⅔, with a u-like exotic quark;
- scalars X = ⅓, ⅓, −⅔, fixed by the Yukawa couplings.

**All anomalies vanish** for N_c = 3, 5 and 7.

**Two-loop blow-up scale (GeV) for three perturbativity criteria. The Planck scale is
1.2×10¹⁹ GeV.**

| Variant | Criterion | N_c = 3 | N_c = 5 |
|---|---|---|---|
| β = −1/√3 | g = 4π | 3.0×10²⁹ | 1.3×10¹⁵ |
| β = −1/√3 | α = 1 | 1.8×10²⁹ | 1.0×10¹⁵ |
| β = −1/√3 | g = 1 (α = 0.08) | 5.3×10²⁵ | 2.7×10¹³ |
| β = +1/√3 | g = 4π | **4.0×10¹⁹** | 5.5×10¹¹ |
| β = +1/√3 | α = 1 | **2.9×10¹⁹** | 4.7×10¹¹ |
| β = +1/√3 | g = 1 (α = 0.08) | 2.0×10¹⁷ | 3.6×10¹⁰ |

N_c = 7 fails in both variants (10⁸–10¹⁰ GeV).

**Verdict:**
- **β = −1/√3:** selects N_c = N_g = 3 under every criterion, by many orders of magnitude.
- **β = +1/√3:** selects 3 under the standard criteria (g = 4π, α = 1), but only narrowly:
  its pole sits a factor of 2–3 above the Planck scale. The g = 1 criterion is overly
  strict, since α = 0.08 is still perturbative.
  - The margin grows with the 3-3-1 scale: 2.9×10¹⁹ GeV at 2 TeV, 9.9×10¹⁹ at 30 TeV.
  - Two-loop Yukawa terms are not included. In the Standard Model they slow U(1) growth;
    I haven't checked whether they do so here.
- **So in both viable 3-3-1 variants, perturbativity to the Planck scale leaves exactly
  N_c = N_g = 3.** The result is robust in one variant and narrow in the other.
