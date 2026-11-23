# Note on L11d: is "S_dS counts microstates" a FOLLOWS?

Scope: SYMMETRY_LADDER.md L11a-d (lines 375-378, and the Link 11 text in src/ladder_links.py lines
198-220), with `de_sitter_entropy_symbolic`, `first_law_every_horizon`, `sds_entropy_bound`,
`de_sitter_numbers` (lines 785-843). No existing file was edited.

## 0. What the code actually checks

- `de_sitter_entropy_symbolic`: for f = 1 - r^2/l^2, horizon r_c = l, kappa = |f'|/2 = 1/l,
  A = 4 pi l^2 = 12 pi/Lambda, and S := A/4 = 3 pi/Lambda (G = c = hbar = k_B = 1). The entropy is
  *defined* in the code as A/4; the check is algebra (factor 3, not 4 pi/Lambda).
- `first_law_every_horizon`: with M(r_h) from f(r_h) = 0, dM/dr_h - (f'(r_h)/4 pi) d(pi r_h^2)/dr_h = 0.
  Again S = pi r_h^2 is put in by hand; the test shows that the *same* S = A/4 makes dM = (f'/4 pi) dS
  at both horizons. It does not derive the 1/4.
- `sds_entropy_bound`: the root identity r_b^2 + r_c^2 + (r_b + r_c)^2 = 2 l^2 and max (S_bh + S_c)/S_dS < 1.
  Pure classical geometry; "S_dS is the maximum" is an inequality between areas.
- `de_sitter_numbers`: l = sqrt(3/Lambda), S = A/(4 l_P^2) ~ 3.3e122, T ~ 2.2e-30 K. Arithmetic with
  Planck-2018 Lambda (a LIT input).

Nothing in the code refers to states, a Hilbert space, a trace, or a count. "Microstates" appears only
in the L11d prose. The existing prose already says "Not tested", so the issue is the label, not hidden
content.

## 1. What is derived here or standard (the area law)

| Claim | Route | Assumptions it uses |
|---|---|---|
| T_dS = hbar c/(2 pi k_B l) | Euclidean continuation: smoothness at r = l fixes the period of imaginary time at 2 pi/kappa; or the thermal response of a static-patch observer (Gibbons-Hawking 1977) | QFT on the fixed dS background; Bunch-Davies/Euclidean vacuum; static-patch observer; kappa from the Killing field (rung 6) |
| S = A/4G (hbar = c = k_B = 1) via the first law | Integrate dE = T dS with T from kappa, with E identified as the mass parameter | Semi-classical regime; a *choice* of energy: for de Sitter alone there is no asymptotic mass, so one uses SdS (L11b), where dM = -T dS at the cosmological horizon (note the sign: it is the energy inside, as seen from the patch, and the conventions are delicate); integration constant (S = 0 at r_h = 0) is an assumption; the first law is assumed to hold for the cosmological horizon as for a BH horizon |
| S = A/4G via the Euclidean action | Gibbons-Hawking: the Euclidean S^4 (for dS_4) has action I = -A/4G, so log Z = A/4G | The Euclidean path integral is dominated by the saddle; the S^4 is the correct contour for the dS vacuum (the usual "no-boundary"-type step); one-loop and higher corrections and the sign/phase of the conformal-factor problem are ignored; ensemble interpretation (Z = Tr e^{-beta H}) is assumed, which is itself a statement about states |
| S_dS is the maximum over SdS (L11c) | Classical area inequality | Cosmic censorship-free sub-extremal SdS only (9 M^2 Lambda < 1) |

What this establishes: a thermodynamic/semi-classical entropy A/4G, consistent between the first-law and
Euclidean routes *given* T and a definition of energy. It is a *coefficient* statement. Note the honest
limitation: the Euclidean route gives log Z, which is "an entropy" only if Z is a trace over some Hilbert
space; the first-law route gives S only up to an additive constant and depends on how the energy is
defined. Neither identifies *what is counted*.

## 2. What the "microstate counting" reading adds

The reading is: e^{S_dS} = dim H of the static patch (or of the whole de Sitter quantum gravity), i.e.
S_dS = ln N with N ~ e^{3.3e122}.

Established, solid and relevant:
- Bekenstein bound S <= 2 pi k R E/(hbar c) and the covariant/holographic bound S <= A/4 l_P^2 (Bousso
  covariant entropy bound; Bousso's "positive vacuum energy and the N-bound", hep-th/0010252, JHEP 11
  (2000) 038 is the dS version, which I could only confirm by citation, not read: see Sources). Within
  this repository: Link 14 checks the Schwarzschild case saturates Bekenstein.
  These are *bounds* on entropy of matter in a region; they are consistent with, and motivate, "S_dS is the
  maximum entropy of a static patch", but do not say empty dS *has* e^{S} states.

Conjectural (none is a theorem):
- Static-patch/finite-dimensional Hilbert space (Banks; Fischler-Banks): the quantum theory of
  (stable) de Sitter has finitely many states, dim H = e^{A/4G}. A 2005 paper "More Thoughts on the Quantum
  Theory of Stable de Sitter Space" (hep-th/0503066) summarizes this; Banks's later "De Sitter Musings"
  (arXiv:1205.3855) is also in the search results. I read only search-result snippets, not the full texts.
- dS/CFT (Strominger, hep-th/0106113, JHEP 10 (2001) 034): quantum gravity on dS_D is dual to a CFT on
  the future boundary sphere. Confirmed from the abstract/snippets: dS_3 central charge computed from the
  asymptotic symmetry group; dual CFT may be non-unitary with complex weights. Status: proposal, no
  complete example with a normalizable bulk dual; non-unitarity is a main objection.
- Static-patch holography (the "dS_{d+1} static patch" dual living on the horizon/stretched horizon, with
  TT-bar + Lambda_2 deformations, double-scaled SYK models): active 2025-2026 work, e.g. Ruan-Suzuki
  arXiv:2508.14478 (JHEP 01 (2026) 044, holographic entanglement entropy in static-patch holography,
  constrains the parameter space), arXiv:2502.03869 (a low-dimensional microscopic model with an observer,
  matching double-scaled SYK), arXiv:2511.16098 (unified TT-bar + Lambda_2 flow for dS/CFT and static patch
  holography), and Flow-geometry-microstates arXiv:2510.18901. I saw only titles/snippets; I did not verify
  claims in the full papers.

Main known objections (as found in search results and general knowledge):
- Goheer-Kleban-Susskind: exact dS symmetry (SO(d,1)) is incompatible with a finite-dimensional
  Hilbert space (unitary reps are infinite dimensional). So either dS is only approximate/metastable
  (Dyson-Kleban-Susskind "Disturbing implications of a cosmological constant", Poincare recurrences in a
  finite system), or the symmetry is anomalous or realized non-unitarily. Susskind's 2021 paper (arXiv:2106.03964)
  even entertains that eternal dS may be inconsistent. I read this from the search-result summary only.
- Dependence on the observer: the "entropy" is that of one static patch/observer; the global state is not
  a trace over the patch in any known UV-complete construction.
- Gibbons-Hawking entropy is a *semi-classical* quantity; a count requires a UV completion, and string
  theory has no controlled stable dS vacuum (a separate, ongoing debate that I did not research here).
- The count has no independent check: unlike Strominger-Vafa for extremal BHs, there is no microscopic
  computation that reproduces A/4G for dS from a known theory. Recent static-patch papers claim leading and
  log corrections for specific models (search snippet), which is model-level evidence, not a derivation
  of the real cosmological horizon.

## What would count as a test or derivation in this repository's style

The repo's labels are CHECK (symbolic/numeric identity), LIT (external input), FOLLOWS (consequence of
something derived), and the rungs are checked by code. A microstate reading can be handled in one of
three honest ways:
1. A *consistency CHECK*, not a derivation: show that a proposed state count reproduces S = 3 pi/Lambda,
   e.g. a double-scaled SYK or random-matrix toy whose density of states has S_0 = A/4G and whose
   disk partition function reproduces T_dS. This verifies a model, not nature.
2. A *derived structural result* the reading predicts and the area law alone does not: e.g. the
   log-correction coefficient of S_dS, or the Poincare recurrence time exp(S_dS) (Dyson-Kleban-Susskind)
   which is only defined if the count is finite. A code check of such a formula is possible but would still be
   a CHECK of a formula in a conjectural framework (label it MODEL).
3. Nothing observable at present: S = 3.3e122 gives T and l already; no experiment distinguishes
   "counts microstates" from "is a geometric area". So no empirical test exists.

## 3. Recommendation

The sentence in L11d mixes a CHECK-able number with an interpretive claim. "FOLLOWS" in this repo means
a consequence of derived content; the microstate reading does not follow from the area law and Lambda
(the entropy-as-count is an *additional* hypothesis, with a no-go theorem in tension). So:

**Do not keep it as FOLLOWS. Relabel the reading as MODEL / conjecture (open), keep the number as
CHECK + LIT.** Do not drop it entirely: the cosmological-constant remark (S_dS = inverse of Lambda in Planck
units) is true as arithmetic and is the repo's useful content; and the line at 577-578 already lists the
holographic reading as "still open". Wording changes:

L11d (replace the text from "Not tested" on; label cell changes `CHECK; LIT; FOLLOWS` to `CHECK; LIT; MODEL`):

> The measured Lambda (Planck 2018 with BAO, as rungs 5 and 6): l = 1.65e26 m, S_dS = A/4 l_P^2 =
> 3.3e122 k_B, T_dS = 2.2e-30 K. This is the Gibbons-Hawking entropy of the cosmological horizon, a
> semi-classical area-law number; it is not derived here that it counts microstates. The reading
> e^{S_dS} = dim H of the static patch is a conjecture (Banks-Fischler; dS/CFT; static-patch
> holography) that is not established, is in tension with exact de Sitter symmetry (Goheer-Kleban-Susskind),
> and is not tested here. (CHECK; LIT Lambda; MODEL for the microstate reading)

Table cell in line 378: `CHECK; LIT; MODEL`; sentence: "That S_dS counts microstates is a conjecture
(holographic proposals), not derived or tested here; only the area law of rung 6 and the Lambda of rung 5
are used." Line 577-578 ("Still open: the holographic reading of S_dS (L11d), which counts microstates
this repository cannot derive") may stay as is; it is already accurate.

Caveat on L11b prose: "dM = -T dS at the cosmological horizon" is correct as the sign of the identity
checked by code, but its physical reading ("the mass inside falls as that horizon grows") depends on the
choice of energy and the patch convention; consider saying "with S = A/4 at both horizons, the same
formula gives dM = (f'/4 pi) dS".

## Sources and access

Search results actually seen (titles/snippets only, no full-text reading):
- Strominger, The dS/CFT Correspondence: https://arxiv.org/pdf/hep-th/0106113
- Banks-Fischler line: https://ar5iv.labs.arxiv.org/html/hep-th/0503066 ; https://arxiv.org/pdf/1205.3855
- Susskind, De Sitter Holography: Fluctuations, Anomalous Symmetry, and Wormholes: https://arxiv.org/pdf/2106.03964
- Static-patch work: https://arxiv.org/html/2508.14478v2 ; https://arxiv.org/html/2502.03869v1 ;
  https://arxiv.org/abs/2511.16098v2 ; https://arxiv.org/pdf/2510.18901
Could not access: Gibbons-Hawking 1977 (Phys. Rev. D 15, 2738) and Bousso hep-th/0010252 (only
citations returned); Dyson-Kleban-Susskind (hep-th/0208013) and Goheer-Kleban-Susskind (hep-th/0212209) were
not retrieved directly: the GKS and recurrence statements rest on a search-result summary of Susskind's
paper and my background knowledge. The Euclidean-action and first-law assumption tables are standard
textbook material from memory, not re-verified against the papers. I did not survey the string-theory
dS-existence debate. These are status snapshots as of the search date, not a literature review.
