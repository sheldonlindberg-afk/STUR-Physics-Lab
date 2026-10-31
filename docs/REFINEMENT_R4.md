# Refinement round 4: torsion beyond TEGR ("spacetime resistance")

> **Superseded by round 5** ([`REFINEMENT_R5.md`](REFINEMENT_R5.md)). Deriving the 5D Lagrangian
> shows that the torsion twist &chi; assumed here does not exist on S&sup1;/Z&#8322;. The torsion
> component that could twist fermions, T_y, is odd under the orbifold reflection, so its
> holonomy vanishes. The conclusions "&beta; = &alpha;/2 without tuning via torsion" and "torsion
> twist = dark matter" are **withdrawn**. The dynamics below remain correct for any field
> of this type, and section A&rsquo;s no-go is extended to all orders in round 5.

Date: 2026-10-31. Script: [`src/checks/r4_torsion.py`](../src/checks/r4_torsion.py), about 75 s.
Status: **exploratory extension**. It is called STUR-ROLL-T below and is
not yet part of the core STUR-ROLL claim.

## Why torsion

Rounds 1&ndash;3 and the follow-up discussion established three things:

1. **The hilltop start is not derived.** &theta;'s potential is about 10&#8315;&#8312;&#8311; too weak to
   hold &theta; at 0 during nucleation, so a random start lands near the hilltop only
   about 3% of the time.
2. **A smooth birth fixes &theta; = 0 exactly, but at the wrong kind of point.** If the
   fifth dimension closes off smoothly at nucleation (the universe is born
   "untwisted"), the holonomy is fixed exactly. But the boundary conditions
   this imposes (bosons periodic, fermions antiperiodic) make that point a
   *minimum*, so &theta; never rolls.
3. **What is missing is a twist that acts on fermions only** and flips &psi; to
   effectively periodic after birth.

Torsion couples to spin, so fermions feel it while scalars and gauge fields do
not [T1]. TEGR torsion is equivalent to GR and Einstein&ndash;Cartan torsion does not
propagate, so the candidate is the **propagating pseudoscalar torsion mode of
quadratic Poincar&eacute; gauge theory**. It couples to the fermion axial current,
and it has already been proposed as a dark-matter candidate [T2]. Its holonomy
along the fifth dimension, &chi;, shifts &psi;'s twist (&psi; sees &theta; + &chi;) but not the
scalar's.

## A. The quantum vacuum resists every twist (generalised no-go)

Over 200 random field contents (spins, charges from &minus;2 to 2, masses 0&ndash;6/L,
torsion coupling to fermions only), the one-loop Wilson-line potential always
has its **global minimum at the birth point (&theta;, &chi;) = (0, 0)**.

So no quantum (loop) effect can start the twisting. It needs a **classical,
tree-level torsion potential whose maximum is at the birth point**. The
minimal periodic choice is

  V_T(&chi;) = &Lambda;&#8308;(1 + cos &chi;).

This is the mathematical form of "spacetime resistance": the untwisted state
is unstable classically, even though loop effects hold it in place. **It is a
new postulate, not a derivation.**

## B. With V_T, the dilemma is resolved: &beta; = &alpha;/2 with no tuning

Simulated with m_&theta; = 10&#8315;&sup3;&#8304; eV, m_&chi; = 10&#8315;&sup2;&#8311; eV and quantum seeds of 10&#8315;&#8308;:

- &chi; rolls from 0 to &pi; and its oscillation decays (amplitude 0.16 by H = m_&chi;/300).
- Meanwhile &theta; stays at its birth value (9.8&times;10&#8315;&#8309;), held by the &chi; = 0 minimum.
- After the flip, &psi; is effectively periodic, &theta; = 0 is a hilltop, and **&theta; lands at
  0.9956&pi;, giving &beta;_rec = 0.2081&deg;** (&alpha;/2 = 0.2091&deg;).
- Without the flip, &beta; = 0.

**The 3% initial-condition tuning is gone.** The smooth birth sets &theta; = 0
exactly, and the torsion flip turns that point into the hilltop. Requirement:
m_&chi; &raquo; m_&theta;, so &chi; flips before &theta; rolls. Because &chi;'s flip happens before
recombination, its own coupling to photons (through &psi;) is invisible.

## C. Dark energy and dark matter: what the math allows

**Dark energy is excluded.** A torsion twist light enough to be dark energy
(m_&chi; &lesssim; H&#8320;) has not flipped by z ~ 50, so &theta; never rolls. Within this mechanism
the twist **cannot** be the dark energy. Dark energy stays a cosmological
constant or a separate sector. Teleparallel f(T) models of acceleration [T3]
are a different mechanism that this round did not test.

**Dark matter is allowed.** After the flip, &chi; oscillates about &pi; and behaves as
matter. Taking all of dark matter to be &chi; requires m_&chi; &gt; 2&times;10&#8315;&sup2;&#8304; eV
(Lyman-&alpha; [T4]). The relic abundance for a hilltop start was computed by
integrating through the radiation era. The integrator reproduces the
standard misalignment benchmark (Omega h&sup2; = 0.066 for &chi;_i = 1, m = 10&#8315;&sup2;&sup2; eV,
f = 10&sup1;&#8311; GeV), which matches the literature's order of magnitude, O(0.1).

| m_&chi; [eV] | f_&chi; for Omega h&sup2; = 0.12 (seed 10&#8315;&#8308;) | (seed 10&#8315;&sup1;&sup2;) |
|---|---|---|
| 2&times;10&#8315;&sup2;&#8304; | 2.3&times;10&sup1;&#8309; GeV | 1.1&times;10&sup1;&#8309; GeV |
| 10&#8315;&sup1;&#8312; | 8.7&times;10&sup1;&#8308; GeV | 4.1&times;10&sup1;&#8308; GeV |
| 10&#8315;&sup1;&#8309; | 1.6&times;10&sup1;&#8308; GeV | 7.3&times;10&sup1;&sup3; GeV |

So the torsion twist can be **all of the dark matter with f_&chi; ~ 10&sup1;&#8308;&ndash;10&sup1;&#8310; GeV**,
which is sub-Planckian and near the GUT scale. One field would then supply
both the dark matter and the trigger for the birefringence.

## D. Two problems the dark-matter branch must solve

1. **Isocurvature.** If &chi; random-walks during inflation, the local roll time
   varies from place to place, and the dark-matter density varies with it:
   &delta;_iso ~ |d ln &rho;/d ln s|/&radic;N &asymp; 0.13/&radic;60 &asymp; 1.7&times;10&#8315;&sup2;. Planck allows
   &delta;_iso &lesssim; 9&times;10&#8315;&#8310; (&beta;_iso &lt; 0.038 [T5]). **This is excluded by 3&ndash;4 orders of
   magnitude**, unless &chi; is heavy during inflation (a Hubble-induced torsion
   mass, m_&chi;,eff &gt; H_inf), so that no super-horizon fluctuations of &chi; form.
2. **Domain walls.** Regions roll to +&pi; or &minus;&pi;. At the all-DM point the wall
   tension is 8m_&chi;f_&chi;&sup2; &asymp; (9.5 GeV)&sup3;, and a scaling network today would have
   &rho;_wall/&rho;_crit ~ 10&#8312;. **This is catastrophic**, unless every region of our
   universe rolls the same way. That needs a parity-odd tilt of V_T larger than
   the seed. Parity-violating torsion terms (Holst / Nieh&ndash;Yan [T6]) are the
   natural source.

With **both** inflationary pinning and a parity-odd tilt, &chi; rolls coherently
from a fixed offset. Then there is no isocurvature, no wall network, and the
abundance is deterministic. That is a consistent scenario, at the cost of two
further ingredients.

## Verdict on "torsion explains DM and DE"

| Claim | Status |
|---|---|
| Torsion supplies the fermion-only twist that fixes the hilltop start | **Yes** (B), given the postulated V_T with its maximum at the birth point |
| Torsion twist = dark matter | **Possible** (C), with m_&chi; &ge; 2&times;10&#8315;&sup2;&#8304; eV and f_&chi; ~ 10&sup1;&#8308;&ndash;10&sup1;&#8310; GeV, but **only if** the isocurvature and domain-wall problems are solved (D) |
| Torsion twist = dark energy | **No**, not within this mechanism (C) |
| Everything derived from first principles | **No**: V_T, the inflationary pinning and the parity-odd tilt are three new inputs |

## Next steps the math points to

1. **Derive V_T.** Find which quadratic Poincar&eacute; gauge theory Lagrangian [T2],
   reduced on S&sup1;/Z&#8322;, gives the pseudoscalar torsion holonomy a potential with
   a maximum at the untwisted point. If none does, STUR-ROLL-T fails.
2. **One term for both requirements.** A Holst / Nieh&ndash;Yan coupling to
   curvature could give both the Hubble-induced mass and the tilt. Check
   whether one term can do both.
3. **Observables of &chi; as dark matter.** Its photon coupling through &psi;
   (g ~ &alpha;/(2&pi;f_&chi;) &asymp; 10&#8315;&sup1;&#8313; GeV&#8315;&sup1;) and its spin coupling of gravitational
   strength are far below current reach. The fuzzy-DM regime near 2&times;10&#8315;&sup2;&#8304; eV
   (small-scale structure) is the testable edge.
4. **Dark energy.** It needs a separate explanation. The next candidate to test
   is the teleparallel f(T) background [T3].

## References (verified from search abstracts only; † = detail not checked)

- [T1] F. W. Hehl, P. von der Heyde, G. D. Kerlick, J. M. Nester, "General relativity with spin and torsion: foundations and prospects," *Rev. Mod. Phys.* **48**, 393 (1976).†
- [T2] &Aacute;. de la Cruz Dombriz, F. J. Maldonado Torralba, D. F. Mota, "Dark matter candidate from torsion," arXiv:2112.03957 (2021). The abstract states that the stable pseudoscalar mode of quadratic Poincar&eacute; gauge theory is a suitable dark-matter candidate, coupled to the fermion axial current.
- [T3] G. R. Bengochea, R. Ferraro, "Dark torsion as the cosmic speed-up," *Phys. Rev. D* **79**, 124019 (2009).†
- [T4] K. K. Rogers, H. V. Peiris, "Strong bound on canonical ultralight axion dark matter from the Lyman-alpha forest," *Phys. Rev. Lett.* **126**, 071302 (2021), arXiv:2007.12705. m &gt; 2&times;10&#8315;&sup2;&#8304; eV (95%).
- [T5] Planck Collaboration, "Planck 2018 results. X. Constraints on inflation," arXiv:1807.06211. &beta;_iso &lt; 0.038 (95%, axion-type uncorrelated CDM isocurvature).
- [T6] S. Holst, "Barbero's Hamiltonian derived from a generalized Hilbert-Palatini action," *Phys. Rev. D* **53**, 5966 (1996).†
