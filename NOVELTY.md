# Novelty search record

*November 2026.* This page records a targeted literature search for the two results
that might be new. It lists what was searched, what was found and what couldn't be
reached. Its purpose is to say honestly how new each result is before anything is
written up as a paper.

**Tools:**
- web search;
- arXiv's own full-text search (arxiv.org/search), and reading the full papers from
  arXiv;
- INSPIRE-HEP, the main particle-physics database, could not be queried: its host is
  blocked in this environment.

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
| Barela 2023, [2305.05066](https://arxiv.org/abs/2305.05066); Morisi, Perdonà, Ricciardi 2025, [2505.15785](https://arxiv.org/abs/2505.15785); [1711.09866](https://arxiv.org/abs/1711.09866); [2302.08578](https://arxiv.org/abs/2302.08578) | The minimal (β = √3) model's Landau pole, about 4–8.5 TeV, and ways to raise it | Running in 3-3-1 at N_c = 3 only. No variation of N_c. |
| Pleitez, slides *Aspects of 3-3-1 models* ([CERN Indico](https://indico.cern.ch/event/580860/contributions/2534292/attachments/1445567/2228491/331m_portoroz17_19april.pdf)) | Anomaly cancellation plus QCD asymptotic freedom restricts the ratio N_g/N_c | Known step 2. |

**Not found:** any use of gauge-coupling running, Landau poles or Planck-scale
perturbativity to fix N_c, in 3-3-1 or in the Standard Model with general N_c.

**Assessment:** the step looks new, but narrowly. The family–colour link and
general-N_c charges are well known, and N_c = 3 has been reached before by inputting
three neutrino species. What this work adds is removing that input and selecting N_c by
running instead. **The open check** is an INSPIRE search and an expert's reading, which
this environment can't provide.

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

## What this changes

- **The 3-3-1 selection remains the candidate result.** The note now cites the retrieved
  prior work and states precisely what is added: the generation count is not taken from
  experiment.
- **The gravity side has no principal new result.** Its value is the corrected design
  numbers, and P3 as a sharpening.
- **Next:** an INSPIRE search and one expert reader for NOTE_331, before any submission.
