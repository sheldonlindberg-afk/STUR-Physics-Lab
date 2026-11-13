# Novelty search record

*November 2026.* This page records a targeted literature search for the two results
that might be new. It lists what was searched, what was found and what couldn't be
reached. Its purpose is to say honestly how new each result is before anything is
written up as a paper.

**Tools:**
- web search;
- arXiv's own full-text search (arxiv.org/search), and reading the full papers from
  arXiv;
- INSPIRE-HEP, the main particle-physics database: blocked at first, then allowed in
  the environment and queried through its API (section 3).

## 1. N_c = N_g = 3 from Planck-scale perturbativity in 3-3-1 (NOTE_331.md)

**Queries:**
- "3-3-1 / 331 model number of colors";
- "Landau pole" with "number of colors/colours";
- "number of colors number of families anomaly";
- "number of colors asymptotic freedom generations";
- "hypercharge Landau pole selects three colors";
- "why three colors".

**What exists (retrieved):**

| Work | What it does | Relation to our result |
|---|---|---|
| Frampton 1994, *The Third Family is Different*, [hep-ph/9409331](https://arxiv.org/abs/hep-ph/9409331) | "Taking … arbitrary numbers N_c of colors and N_l of light neutrinos we find this anomaly cancels only if N_c = N_l = 3" | Closest prior statement. It reaches N_c = 3 by **inputting** N_l = 3 (light neutrinos, from experiment). Our chain inputs neither N_g nor N_l: anomalies leave N_c = N_g ∈ {3, 5, 7, …}, and perturbativity selects 3. |
| Pisano 1996, [hep-ph/9609358](https://arxiv.org/abs/hep-ph/9609358); Doff & Pisano 2000, [hep-ph/0007306](https://arxiv.org/abs/hep-ph/0007306) | Anomaly cancellation matches the number of families to the number of colours | Known step 2. Pisano takes the Standard Model, with three colours, as the low-energy input. |
| Geng 2001, [hep-ph/0101329](https://arxiv.org/abs/hep-ph/0101329) | Charge quantization and representations with an arbitrary number of colours | Known part of our §1 (charges as functions of N_c). |
| Barela 2024, [2305.05066](https://arxiv.org/abs/2305.05066); Morisi, Perdonà, Ricciardi 2025, [2505.15785](https://arxiv.org/abs/2505.15785); [1711.09866](https://arxiv.org/abs/1711.09866); [2302.08578](https://arxiv.org/abs/2302.08578) | The minimal (β = √3) model's Landau pole, about 4–8.5 TeV, and ways to raise it | Running in 3-3-1 at N_c = 3 only. No variation of N_c. |
| Pleitez, slides *Aspects of 3-3-1 models* ([CERN Indico](https://indico.cern.ch/event/580860/contributions/2534292/attachments/1445567/2228491/331m_portoroz17_19april.pdf)) | Anomaly cancellation plus QCD asymptotic freedom restricts the ratio N_g/N_c | Known step 2. |

**Not found:** any use of gauge-coupling running, Landau poles or Planck-scale
perturbativity to fix N_c, in 3-3-1 or in the Standard Model with general N_c.

**Assessment (before INSPIRE; section 3 has the update):** the step looks new, but narrowly. The family–colour link and
general-N_c charges are well known, and N_c = 3 has been reached before by inputting
three neutrino species. What this work adds is removing that input and selecting N_c by
running instead. **The open check** was an INSPIRE search, which this environment couldn't
reach at first.

## 2. Bounds on classical–quantum gravity (OPPENHEIM.md)

**Queries:**
- "Oppenheim decoherence diffusion trade-off kernel-independent";
- "Cauchy–Schwarz bound acceleration noise decoherence product";
- "discrete classical-quantum gravity single particle test".

Full texts were read for 2203.01982, 2307.02557, 2402.17844, 2603.29230 and 2605.05375.

**What exists (retrieved):**

| Work | Content | Relation |
|---|---|---|
| Oppenheim, Sparaciari, Šoda, Weller-Davies, [2203.01982](https://arxiv.org/abs/2203.01982) (Nat. Commun. 2023), **appendix B.3–B.4** | A state-level ("observational") Cauchy–Schwarz trade-off with an arbitrary test function b(x), for any kernel (eqs. 76–84). Eq. 84 bounds the potential-weighted diffusion by \|⟨Φ⟩\|²/(16G²λ). | **P5's kernel-free inequality is theirs.** P5 only chooses the test functions (the force response, the branch difference) and works out the split dependence. Corrected in OPPENHEIM.md. |
| Layton, Oppenheim, Russo, Weller-Davies, [2307.02557](https://arxiv.org/abs/2307.02557) | The weak-field limit of CQ gravity | No product bound of the P3 type found |
| Grudka et al., [2402.17844](https://arxiv.org/abs/2402.17844) | Renormalisation of postquantum-classical gravity | — |
| Hirotani & Matsumura, [2603.29230](https://arxiv.org/abs/2603.29230) (2026) | Strain spectrum of geodesic deviation in CQ gravity; the original model is testable with gravitational-wave detectors | A complementary test: classical test masses, no superposition. Not P3 or P5. |
| [2605.05375](https://arxiv.org/abs/2605.05375) (2026) | Stochastic degrees of freedom; saturating kernels, a Schur-multiplier positivity condition | No single-particle product bound found |

**Assessment:**
- **P5:** not new as a principle. It is an application of Oppenheim et al.'s appendix B.4.
- **P3** (applying the trade-off mode by mode, for translation-invariant kernels): a
  sharpening of their framework. It wasn't found stated, but it is incremental.
- **The finite-nucleus heating correction:** not found stated. It is a correction inside
  this project.

None of these should be presented as a principal result.

## 3. INSPIRE-HEP search (after the host was allowed)

**3-3-1 and the number of colours:**
- **Every paper citing the founding papers.** All 992 papers citing Frampton 1992
  (recid 335407) or Pisano–Pleitez 1992 (recid 31937) were filtered:
  - by title for colour/colours: 3 hits;
  - by abstract for "number of colors/colours" or "color number": 4 hits;
  - by "Landau pole": 9 hits.
- **Every paper citing Frampton 1994:** 9 hits.
- **Every paper citing Doff & Pisano 2000:** 4 hits.
- **Abstract searches across all of INSPIRE** for "number of colors" with "Landau pole",
  "number of generations" or "perturbativity": 1, 0 and 0 hits, none relevant.
- **Full-text searches** for "number of colors/colours" + "Landau pole" + 3-3-1: 139 and
  65 hits, all QCD reviews and lectures matching generic terms. "Arbitrary number of
  colors" + "Landau pole": 11 hits, none relevant.

**The closest prior work found by INSPIRE:**

| Work | Content | Relation |
|---|---|---|
| Doff & Pisano 2000, *On the color simple group from chiral electroweak gauge groups*, [hep-ph/0011087](https://arxiv.org/abs/hep-ph/0011087) | Keeps n_c general in SU(n_c) × SU(m)_L × U(1)_N and derives N_generations = k·n_c, k = 1, 2, 3, … (their eq. 17), with an even-n_c branch | **Closest of all.** They don't impose asymptotic freedom to force k = 1, and they don't use running or Landau poles to choose n_c, so "why 3" stays open. Their even branch (N_g = 2n_c) matches our proof, which then excludes it by asymptotic freedom. |
| Diaz, Martinez, Ochoa 2005, [hep-ph/0411263](https://arxiv.org/abs/hep-ph/0411263) | Arbitrary β and generation numbers | N_c = 3 |
| Dias, Martinez, Pleitez 2005, [hep-ph/0407141](https://arxiv.org/abs/hep-ph/0407141); Martinez & Ochoa 2007 | Landau poles across 3-3-1 variants | N_c = 3 only |
| Melle 2026 (thesis), [2610.26893](https://arxiv.org/abs/2610.26893) | Anomalies plus QCD asymptotic freedom fix three generations; the TeV Landau pole | Three colours as input |

**Verdict on 3-3-1.**
- Varying N_c in 3-3-1 is known (Doff–Pisano 2000), and so is the family–colour link.
- Using asymptotic freedom to set k = 1 at general N_c, and then **running to the Planck
  scale to select N_c = 3 among {3, 5, 7, …}**, was not found anywhere. It remains the
  candidate new step, now with a precise predecessor to cite.

**Classical–quantum gravity:** all 103 papers citing Oppenheim et al. 2022 were filtered
for "Cauchy–Schwarz" (6), "acceleration noise" (5) and "levitated" + "trade-off" (4).

| Work | Content | Relation |
|---|---|---|
| Fabiano, Fujita, Matsumura, Carney 2026, *Minimal noise in non-quantized gravity*, [2603.26075](https://arxiv.org/abs/2603.26075) | Classifies **all** non-entangling Newtonian models (Galilean invariant, Newtonian on average). Each must inject a quantifiable minimal noise; tested on Oppenheim's models | **Supersedes P2–P5 as a program** |
| Angeli, Donadi, Di Bartolomeo, Gaona-Reyes 2025, [2501.13030](https://arxiv.org/abs/2501.13030) | A lower bound on the noise any classical gravity must induce; a torsion-pendulum protocol | Covers the heating and diffusion floor (P4) |
| Janse et al. 2024, [2403.08912](https://arxiv.org/abs/2403.08912) | Experimental force-noise bounds on spacetime diffusion | The acceleration side of P3 |
| Piccione 2026, [2602.19377](https://arxiv.org/abs/2602.19377) | Heating diverges without smearing; smearing profiles studied | Close to our finite-nucleus point |
| Kryhin & Sudhir 2023, [2309.09105](https://arxiv.org/abs/2309.09105) | Irreducible fluctuations of classical gravity, tested by cross-correlations of source masses | Complementary |

**Verdict on gravity:** P2–P5 and the heating floor are worked examples within an active,
systematic literature. None should be claimed as new.

## 4. Refresh, 12 November 2026 (3-3-1)

The 3-3-1 query families of sections 1 and 3 were rerun, with emphasis on 2025–2026.

**Queries:**
- INSPIRE abstracts: 3-3-1/331 with "number of colors/colours/generations/families"
  (5 hits); 3-3-1 with "Landau pole" since 2025 (0); "number of colors" with "Landau
  pole", perturbativity or asymptotic freedom since 2024 (1); "three generations/families"
  with "Landau pole" since 2024 (0); "number of colors" with "Planck scale" or "Landau
  pole" since 2025 (2, unrelated); "why three generations" since 2025 (1, unrelated).
- INSPIRE full text: 3-3-1 + number of colours + Landau pole, since 2025: 1 hit, a dark
  matter paper matching generic words.
- Every paper citing Doff–Pisano 2000 (hep-ph/0011087): 4, unchanged. Every paper citing
  Frampton 1994 (hep-ph/9409331): 9, unchanged. Papers citing Doff–Pisano,
  hep-ph/0007306: 29, the newest from 2024.
- arXiv's own abstract search ("3-3-1" with colors and Landau; "number of colors" with
  "Landau pole"; 331 with "number of colours"; "number of generations" with "Landau
  pole"): nothing relevant. The arXiv API host is blocked in this environment; the
  arxiv.org search page was used instead.
- Web search: nothing from 2026 on selecting the number of colours by running.

**Not in the earlier record (retrieved):**

| Work | Content | Relation |
|---|---|---|
| Corianò and Melle 2024, *The 331 model: addressing the fermion families problem within horizontal anomalies cancellation*, Entropy, [2404.05821](https://arxiv.org/abs/2404.05821) | Review: anomaly cancellation across generations makes the number of families three; the model's RGEs | Three colours as input. Same group as Melle 2026 (section 3) |
| Huitu, Koivunen, Kärkkäinen, Mondal 2024, *On the family discrimination in 331-model*, [2409.13013](https://arxiv.org/abs/2409.13013) | Which generation sits in the different representation; flavour constraints, β = −1/√3 | Phenomenology at N_c = 3 |
| Cacciapaglia, Sannino, Wagner 2026, *Completely asymptotically free chiral theories with scalars*, Phys. Rev. D, [2605.08294](https://arxiv.org/abs/2605.08294) | Requiring all couplings to be asymptotically free in generalized Georgi–Glashow and Bars–Yankielowicz theories selects specific numbers of colours and families | **A methodological cousin:** ultraviolet behaviour of the couplings selecting the number of colours. A different setting (chiral GUT-like theories, complete asymptotic freedom), not 3-3-1, and not Planck-scale perturbativity with measured couplings. To be cited |

**Verdict:** unchanged. No work found uses running to the Planck scale to select
N_c = 3 in 3-3-1. Cacciapaglia–Sannino–Wagner show that the general idea, ultraviolet
consistency selecting N_c, is in active use in another setting, and NOTE_331 should cite
it as such.

## What this changes

- **The 3-3-1 selection remains the candidate result.** The note now cites the retrieved
  prior work and states precisely what is added: the generation count is not taken from
  experiment.
- **The gravity side has no new result** (section 3). Its value is internal: the corrected
  design numbers, the derived gas rate, and worked examples.
