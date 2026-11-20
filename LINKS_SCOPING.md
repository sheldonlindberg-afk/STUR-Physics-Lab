# Scoping the empty cells of the link table: rungs 2–3 and 3–5 (and the unnumbered 3–4)

*A scoping memo, not a result. Nothing here is pinned by a test or entered in
`src/ladder_links.py`. The numbers are first-pass values from short scratch scripts that import
the repository's own modules (`stur_gravity_entanglement`, `casimir_diamonds`) and standard
inputs. Labels follow [SYMMETRY_LADDER.md](SYMMETRY_LADDER.md): CHECK, MODEL, LIT, FOLLOWS.*

The table "Where links exist, by pair of rungs" in SYMMETRY_LADDER.md has two empty cells,
2–3 and 3–5, and shows 3–4 only as "(Casimir gap)". This memo asks, for each one, what a link
would physically be, whether it can be computed, whether it suits a blind-build campaign
(`rebuild/campaigns/README.md`), and whether the honest entry is "none". Every candidate also
gets the **novelty test**: does it predict something that is not already an input, or does it
only restate a known identity?

## The three rungs involved

- **Rung 2** (`src/chiral_breaking.py`): chiral SU(2)_L × SU(2)_R → SU(2)_V through ⟨q̄q⟩.
  Its outputs are the pion mass (GMOR, and O(p⁴) ChPT), the one-pion-exchange range
  1/m_π = 1.414 fm, Goldberger–Treiman g_πNN, and (through L6) the fact that the diamond's mass
  is 91% QCD field energy. Its inputs are m̂, Σ, F_π/F, ℓ̄₃, g_A, f_π and M_N.
- **Rung 3** (`src/casimir_diamonds.py`): U(1)_em is unbroken, so the photon is massless and
  long-range. The content is the Casimir–Polder (CP) energy between two neutral dielectric
  spheres: α/(4πε₀) = KR³ with K = (ε − 1)/(ε + 2) (P1), the imaginary-frequency Green tensor
  (P2), U = −(23/4π)ħc α₁α₂/r⁷ (P3; the dyadic step derived in L23), its Matsubara form
  U_T = U₀ η(τ), τ = 2πk_BTr/ħc (P5), and the safe gap (P4, P6). Its one material input is
  ε(diamond) = 5.7.
- **Rung 5** (`src/macdowell_mansouri.py`): GR + Λ as an SO(4,1) gauge theory broken to SO(3,1).
  Its single physical number is ℓ = √(3/Λ) = 1.647×10²⁶ m (M6). Its other outputs are F = 0
  for de Sitter (M3) and the coupling 3/(GΛ) ≈ 10¹²². Through L10, L11 and L15 it gives
  Λc²r²/6, S_dS and T_dS = ħc/(2πk_Bℓ).

## Summary

| Cell | Best candidate | Computable now? | Passes novelty test? | Campaign? | Recommended entry |
|---|---|---|---|---|---|
| 2–3 | The nucleon's electric polarizability from rung 2's pion cloud (LO ChPT), entered into rung 3's CP formula | LO value yes (closed form, LIT formula): **α_E = 12.8×10⁻⁴ fm³** against 11.2(4) measured | **Yes** for α_E (a measured quantity nowhere used as an input). No for the apparatus: the strong sector is **~10⁻¹⁷ to 10⁻¹⁵** of the diamonds' polarizability | Yes, well posed (HBChPT Compton at O(p³)), but every builder knows the textbook answer | Either a hadronic link (if the campaign is run), or "none in the apparatus" with the reason |
| 3–5 | (i) CP between two atoms in de Sitter; (ii) the photon's vacuum energy in de Sitter | (i) the thermal part only: τ = r/ℓ exactly, **η − 1 = 1.8×10⁻¹⁸³** at the gap; the curvature part, of order (r/ℓ)² = **1.2×10⁻⁶⁰**, is not computed. (ii) yes, with a quoted anomaly coefficient: **ρ_γ/ρ_Λ = (31/180)/S_dS = 5.3×10⁻¹²⁴** | (i) formally yes, but untestable by 60 orders; (ii) **no**: it is dimensional analysis plus one coefficient | (i) possible, but the SPEC is ambiguous at exactly the order of the effect; (ii) possible as a heat-kernel campaign, with low payoff | **"None, by the structure of the rungs"**, with the reason below. Optionally, (ii) as a footnote row of L15 |
| 3–4 | Already a link in substance (P4/P6: the CP entangling phase as a competing signal) | Yes, done | Yes: it sets the 181 µm gap | Not needed | Give it a link number instead of inventing a new one |

---

## 1. Rungs 2–3

### What a link would have to be

Rung 3's CP energy depends on exactly one property of matter: the polarizability α(iξ) at the
imaginary frequencies that matter at the gap, ξ ≲ 10c/r ≈ 1.7×10¹³ rad/s. A 2–3 link
therefore needs one of two things: either a rung 2 quantity entering α (or ε) of some object,
or rung 3's formula applied to a rung 2 object. Four candidates:

**2–3A. The nucleon's polarizability from rung 2's pion cloud, used in rung 3's CP formula.**
At O(p³) in heavy-baryon ChPT, the Compton amplitude's one-pion loop gives, at leading order
(Bernard, Kaiser and Meißner, PRL 67 (1991) 1515; LIT formula):

  α_E = 5α g_A² / (96π f_π² m_π),  β_M = α_E / 10,  the same for proton and neutron.

These are Gaussian units, the same convention as rung 3's α/(4πε₀). The inputs are rung 2's
own: g_A = 1.2754, f_π = 92.07 MeV and m_π± = 139.57 MeV, plus α(0).

- **First-pass number (CHECK of the closed form):** **α_E = 12.8×10⁻⁴ fm³, β_M = 1.28×10⁻⁴ fm³**.
  The PDG values for the proton are α_E = 11.2(4)×10⁻⁴ and β_M = 2.5(4)×10⁻⁴ fm³. α_E is 14%
  high, the known size of the LO overshoot. β_M is low because its large paramagnetic Δ(1232)
  part only enters at higher order. With m_π⁰ in place of m_π±, α_E is 13.2×10⁻⁴: the choice
  of pion mass alone moves it by 3%.
- **Where it enters rung 3.** For two neutral polarizable particles, P3 extended with magnetic
  polarizabilities is the Feinberg–Sucher potential (PRA 2, 2395 (1970); LIT):
  U = −(ħc/4πr⁷)[23(α₁α₂ + β₁β₂) − 7(α₁β₂ + α₂β₁)]. P3 is its electric part, and the
  −7 cross term would need L23's photon-exchange derivation redone with magnetic dipoles.
  For two neutrons with the LO values, the coefficient is 5.6×10⁻⁴ MeV fm⁸.
- **What it adds to the ladder's picture (FOLLOWS, order of magnitude):** between two neutrons,
  rung 3's CP tail overtakes rung 2's one-pion-exchange scale (f²/4π)m_π e^(−m_πr)/(m_πr) at
  r ≈ **48 fm**, at about 10⁻¹⁵ MeV. Gravity overtakes CP at r ≈ **2.8×10⁻¹⁰ m**. This puts
  a number on the "How the rungs fit together" row "below: … two long-range forces". One
  caveat is essential: the neutron's magnetic-dipole interaction (∝ 1/r³, spin dependent) is
  larger than CP at these distances, so the crossover applies to the spin-independent channel
  only.
- **What it means for the apparatus (CHECK, first pass):** per carbon atom, the diamond's
  Clausius–Mossotti polarizability is α_atom/(4πε₀) = 3KV_atom/4π = 8.3×10⁻³¹ m³. Twelve
  nucleons at LO give 1.5×10⁻⁴⁷ m³, which is **1.9×10⁻¹⁷** of it. The ¹²C nucleus's
  giant-dipole polarizability, from the TRK sum rule with a 23 MeV peak, is ≈ 0.3 fm³, or
  **4×10⁻¹⁶** of it. That is nuclear many-body physics, which rung 2 says it does not derive.
  Because CP ∝ α², the strong sector changes the diamonds' CP background by ≲ 10⁻¹⁵.

*Novelty test.* α_E is a genuine prediction. It comes from rung 2's inputs, is measured, and is
used as an input nowhere in the repository. The apparatus statement also predicts something:
the strong sector's share of the background is negligible. That conclusion is expected,
though, so it is a bound, not a test. **This candidate passes the test as hadron physics, not
as diamond-experiment physics.**

*Campaign suitability.* The candidate is well posed for the rebuild/campaigns protocol:
- **SPEC (postulates only):** the LO πN Lagrangian (g_A, f_π, m_π, M_N → ∞), minimal coupling
  to the photon, and the definition of α_E and β_M as the ω² coefficients of the Compton
  amplitude once the Born (Powell) terms are removed.
- **Hidden oracle:** 5αg_A²/(96πf_π²m_π) and β/α = 1/10.
- **Blind checks:** α ∝ g_A²/(f_π² m_π) (which diverges in the chiral limit), proton equals
  neutron at this order, gauge invariance of the amplitude, and the Baldin sum rule
  α + β = (1/2π²)∫σ_γN/ω² dω evaluated with the LO threshold photoproduction cross-section
  (an independent route that an auditor can run).
- **Weakness, as in L33:** every capable builder knows the textbook result, so agreement shows
  correct execution with weaker independence than usual.
- **Optional second stage:** the −7 magnetic cross term of Feinberg–Sucher, by extending
  `qed_cp`'s 12 diagrams to magnetic-dipole vertices. That would be a genuine rung 3
  extension.

**2–3B. Rung 2's mass fraction entering the safe gap.** P4 says the safe gap does not depend on
the mass. It does depend on the **density**, though: the CP phase ∝ K²R⁶ and gravity's ∝ Gρ²R⁶,
so the gap goes roughly as ρ^(−1/3). L6 says ρ is 91% QCD. With L6d's counterfactuals
(phase 2.19 → 1.99 rad with massless u, d; → 1.80 rad with all quarks and the electron massless),
rescaling `RHO_DIAMOND` in `casimir_diamonds.safe_gap_T` gives a gap of 181.11 → **184.44 µm
(+1.8%)** and → 188.05 µm (+3.8%). A pure ρ^(−1/3) would give +1.6% and +3.3%. The entangling
combination is not a pure power, so the scaling is slightly steeper.
(181.11 µm is the root-found value. The 181.16 quoted elsewhere comes from a grid.)
*Novelty test:* this fails. It is L6 composed with P6, adds no physics, and the strong force
enters only through the gravitational side of the comparison, which makes it a 2–4 statement
routed through the 3–4 gap criterion. **It should not fill 2–3.** At most it is a remark under
L6.

**2–3C. QCD in ε(diamond) itself.** Diamond's ε is electronic. Its Born effective charges are
zero (P5), so there is no ionic part. The nuclear mass, which is mostly QCD, enters ε only
through:
- the electron–nucleus reduced mass, about m_e/M ≈ 5×10⁻⁵;
- the zero-point lattice motion, ∝ M^(−1/2), which renormalizes the band gap and the lattice
  constant (the measured ¹²C/¹³C isotope effects).

This is a real pathway, but computing it needs first-principles electron–phonon theory (DFT),
which is outside anything the repository does or could pose as a postulates-only SPEC of
reasonable size. **It is not computable here and not a campaign candidate.**

**2–3D. The strong force as a background at the gap.** Rung 2's force falls as e^(−m_πr). At
181 µm, m_πr = 1.3×10¹¹. *Novelty test:* this fails, because it only restates the known range
of the nuclear force. It is not a link.

**L8c is not a 2–3 link.** The π⁺–π⁰ mass splitting is an electromagnetic vacuum-fluctuation
energy of the kind rung 3 computes, but it uses rung 1's photon coupling and is already filed
as 1–2. Moving it to 2–3 would fill the cell by relabelling, not by computing anything.

### Verdict for 2–3

Only 2–3A is a physically meaningful link that passes the novelty test, and it is a hadronic
one: rung 2's pion cloud sets a polarizability, and rung 3's formula turns it into a
long-range force. For the diamond experiment, which is what rung 3 is about in this
repository, the link is empty by ~15 orders of magnitude. Two honest entries are possible:
- **If no campaign is run:** "none in the apparatus. Rung 3's CP depends only on α(iξ), which
  is electronic. The strong sector's share is ≲ 10⁻¹⁵ (nucleon pion cloud 2×10⁻¹⁷, nuclear
  giant dipole 4×10⁻¹⁶). QCD enters the experiment only through the mass (L6), on gravity's
  side."
- **If 2–3A is run and accepted:** "L-nn (hadronic): α_E of the nucleon from rung 2's pion
  loop, and its CP tail." The entry should state that it does not touch the experiment.

## 2. Rungs 3–5

### What a link would have to be

Rung 5 has one scale, ℓ. Rung 3 has lab scales (r ~ 10⁻⁴ m, c/ξ) and computes only
**configuration-dependent energy differences** of a massless field. A 3–5 link can therefore
enter only in two ways. Either the de Sitter background modifies rung 3's propagator, which
gives powers of r/ℓ ≈ 10⁻³⁰, or the photon field contributes to rung 5's vacuum energy, which
gives absolute energies that rung 3 never computes.

**3–5A. Casimir–Polder in de Sitter (rung 5's vacuum as rung 3's background).** Rung 3's P2
Green tensor is the flat-space one. In rung 5's vacuum (f = 1 − r²/ℓ², the static patch), the
photon in the Bunch–Davies state has two effects:
- **(a) A thermal effect.** A static observer sees the Gibbons–Hawking temperature
  T_dS = ħc/(2πk_Bℓ) (L11). Inserted into P5's Matsubara variable it gives an **exact
  identity: τ = 2πk_BT_dS r/(ħc) = r/ℓ** (checked numerically against `casimir_diamonds.tau_of`
  to 10⁻¹²). Then η − 1 = (22/21735)(r/ℓ)⁶ = **1.8×10⁻¹⁸³** at the 181.2 µm gap and
  2.7×10⁻¹⁷⁹ at the farthest branch distance, 902 µm. (CHECK, first pass.)
- **(b) A curvature effect.** De Sitter is not thermal Minkowski. Maxwell's equations are
  conformally invariant and de Sitter is conformally flat, so the dS photon Green tensor is
  the flat one mapped conformally. The atoms' frequency scale breaks the conformal symmetry,
  and the remainder appears at relative order (r/ℓ)² = Λr²/3 = **1.2×10⁻⁶⁰** at the gap. That
  is the same order as L10c/L10e for gravity's propagator. The coefficient is **not computed
  here**.

*Novelty test.* (a) fails, because it is the Gibbons–Hawking temperature substituted into a
known function. (b) passes formally, since the function of r/ℓ is a prediction and not an
input. It is untestable by about 60 orders, and its value is conceptual: it would show that
rung 3's background in rung 5's vacuum is not a thermal bath. L10e has exactly this character
and was accepted, so there is precedent.

*Campaign suitability for (b).* It can be posed, but the SPEC is ambiguous at the order of the
effect, which is where campaigns fail honestly (`rebuild/campaigns/README.md`: "the SPEC is
ambiguous"):
- Two atoms at fixed proper separation cannot both be geodesic. If atom A sits at the
  static-patch origin, atom B must be accelerated, with a ≈ c²r/ℓ². Freely falling (comoving)
  atoms drift apart.
- The choice of frame, the vacuum (Bunch–Davies against the static vacuum) and the observer's
  acceleration all change the answer at O(r²/ℓ²).
- A SPEC would have to fix all three. Like L10e, it would then be labelled "FOLLOWS (frame)".
- **Oracle:** an independent route, the conformal map of the flat Green tensor against a
  direct static-patch mode sum. Papers on atom–atom interactions in de Sitter (static against
  freely falling atoms, against thermal Minkowski) exist. **No specific reference has been
  located and read for this memo**, so a literature oracle is not yet available.
- **Blind checks:** the flat limit ℓ → ∞ must return 23/4π and 3/4, the thermal limit (a)
  must be reproduced as the leading T_dS part, and the result must be symmetric under
  A ↔ B where the frame allows.

**3–5B. The photon's vacuum energy in rung 5's vacuum.** L15 compares ρ_Λ with each rung's
vacuum energy, and rung 3 is missing from that list. The structural reason is that U(1)_em is
unbroken, so there is no condensate and no mass: in a covariant scheme (dimensional
regularization) the massless photon has no m⁴ zero-point term in flat space. In de Sitter its
renormalized stress tensor is fixed by the trace anomaly. The Euler coefficient for a Maxwell
field is 62 in units of a conformal scalar (LIT: Birrell and Davies, ch. 6; Duff). With H = c/ℓ,
this gives

  |ρ_γ| = 62ħc / (960π² ℓ⁴) = 2.8×10⁻¹³³ J/m³, against ρ_Λ = 5.3×10⁻¹⁰ J/m³:
  **ρ_γ/ρ_Λ = 5.3×10⁻¹²⁴ = (62/360)/S_dS exactly**, with S_dS = πℓ²/ℓ_P² = 3.3×10¹²² (L11).

(CHECK of the arithmetic. The coefficient is LIT. The sign is convention-laden and has not
been fixed here.)

*Novelty test:* this fails. Apart from the number 62, the ratio is forced by dimensional
analysis to be ∝ (ℓ_P/ℓ)² ∝ 1/S_dS. It restates L11/L15's identity. It is also
scheme-dependent in the way that matters: with a hard cutoff, the photon's zero-point energy is
the usual Λ_UV⁴ cosmological-constant problem, which L15 already quantifies with M_Pl⁴. The
only content it adds is that the photon's covariant, cutoff-free contribution is negligible.
*Campaign:* the 62 could be derived blind as the heat-kernel a₂ coefficient of Maxwell plus
Faddeev–Popov ghosts. That is well posed and has a literature oracle, but it is textbook
material, so independence would be weak. The known zero-mode subtleties of Maxwell on S⁴
between the local anomaly and the global ζ(0) would need care. The payoff for the ladder is
small.

**3–5C. Structural analogy.** Rung 3's photon is massless because U(1) is unbroken. Rung 5's
tetrad is the broken direction of SO(4,1) (M1). This parallel is real but yields no number,
and it is not a link.

**3–5D. "The Casimir effect shows vacuum energy gravitates, so it feeds Λ."** This is the most
common claimed 3–5 connection, and the repository's own rung 3 argues against it. P3b and L21
obtain CP from normal-mode *shifts* (energy differences between configurations). The same
result follows from fluctuating sources (L23's photon-exchange diagrams), and it vanishes as
α → 0 (Jaffe, PRD 72, 021301 (2005)). Rung 3 therefore measures nothing about the absolute
vacuum energy that sets Λ. Whether the CP *interaction* energy gravitates like E/c² is a 3–4
question, and at the gap it is ~10⁻³⁹ of the diamond's mass. **It is not a 3–5 link.**

### Verdict for 3–5

**Recommended entry: "none, by the structure of the rungs."** The reason to state is this.
Rung 3 computes configuration-dependent energies of a massless, conformal field at lab
distances. Rung 5 has a single absolute scale ℓ. The two meet only as powers of r/ℓ ≈ 10⁻³⁰
(3–5A), or through the absolute vacuum energy, which rung 3 neither measures nor fixes and
whose covariant photon part is (62/360)/S_dS of ρ_Λ (3–5B, dimensional analysis). The thermal
piece is an identity, τ = r/ℓ. The one candidate that is a prediction, 3–5A(b), is the
electromagnetic analogue of L10e. It can be computed only with a frame choice made at the
order of the effect, and it would need a campaign whose SPEC fixes that choice. If L15 is ever
revised, 3–5B can be added there as the photon's row ("U(1)_em unbroken: no condensation
energy; covariant anomaly term (31/180)/S_dS"), with the label that it restates dimensions.

## 3. Rungs 3–4: "(Casimir gap)"

This cell is not empty in substance. P4 and P6 already compute a rung 3 entangling phase along
rung 4's branch trajectories and require it to be ≤ 10% of gravity's. That criterion sets the
181 µm gap, and it is exactly a "one rung's output is another's input" link. It lacks only a
link number. The right fix is to name P4/P6 as that link, not to compute something new. The
other 3–4 candidates are all weaker:
- the density dependence of the gap (2–3B above);
- the gravitational weight of the CP interaction energy (~10⁻³⁹ of m);
- a graviton analogue of CP between polarizable masses.

None of them would change the design.

## What this memo does not do

- It does not add any link, test, or entry to `src/ladder_links.py`, and it does not edit
  SYMMETRY_LADDER.md.
- The literature values quoted (BKM's LO formula, PDG polarizabilities, Feinberg–Sucher's
  coefficients, the Maxwell anomaly coefficient 62, Jaffe 2005) come from the author's
  knowledge and were not re-read for this memo. A campaign SPEC or oracle built on them must
  re-check each one against its source.
- The first-pass numbers came from scratch scripts outside the repository. None is pinned.
