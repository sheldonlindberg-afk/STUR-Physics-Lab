# Validation record

## Reproducible baseline

| | |
|---|---|
| Command | `python3 production_v2_2.py --json-out out.json` |
| Python | 3.13.18 (CI: 3.12), standard library only |
| Runtime | 5 min 30 s on one core (cloud container, 2026-11-24) |
| Before Part F certification (commit 4b10487) | output identical to `production_v2_2.txt` at that commit, 40/40 self-checks pass |
| After | 41/41 self-checks pass; only the Part F lines and the new check changed |

The self-checks test the calculation (exact identities, step-size and precision independence,
finite-difference checks of transcribed formulas). They do not test agreement with data and
do not establish any physical hypothesis.

## Evidence level of each headline result

| Result | Level | What it rests on |
|---|---|---|
| Part F: no zero pattern of general mass matrices predicts an equality | **Proved** | exact rank lower bound = symmetry upper bound for all 472 candidates; J ≡ 0 by symbolic expansion for the 2 rank-8 classes |
| Part F scope | not tested | rank 10 rules out equalities, not inequalities: a pattern may still be unable to reach the measured point |
| Part C: Hermitian texture survey, 1 survivor of 83 tested classes | **Numerical** | pattern enumeration is exhaustive and band exclusions are exact; joint χ² tests use a finite start grid + compass search, so a missed minimum could wrongly exclude a class |
| Part B: Fritzsch phase bands | **Numerical** | finite phase grid + local refinement |
| Part A: cosmology (age, Ω's) | **Derived, conditional** | flat ΛCDM is assumed, not derived |
| Part I: SUSY scale from α | **Parameter trade** | the measured α is used to infer M_S; not a parameter-free prediction |
| Part L: m_h from λ(M_P) = 0 (and β_λ = 0) | **Conditional prediction** | holds only if the criticality condition holds and nothing new appears below M_P; two-loop running, one-loop matching |
| Parts D, E: 3-3-1 charges, anomalies, Z_N scans | **Exact, model-building** | exhaustive within Z_N, N ≤ 6, abelian; does not show 3-3-1 describes nature |
| Part H: Planck-scale identities | **Exact identities** | dimensional relations, not explanations of the scales |

## Open items, in order

1. Part C: certify the joint-fit exclusions (interval arithmetic or branch-and-bound over the
   bounded parameter box), or report how close each excluded class comes to the 3σ line.
2. Part L: independent check of the beta functions and matching; sensitivity to loop order,
   to the matching scale and to correlated input uncertainties.
3. Parts D, E: scalar potential and symmetry breaking of the Z_6 model.
4. A dependency graph of which parts feed which (Part I → J → K; A and H independent).
