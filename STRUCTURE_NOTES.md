# Does compressing these formalisms into one ladder expose structure nobody had noticed?

*Scope and stance.* The ladder is evaluated here as a **compressed, unified bookkeeping of existing formalisms** (gauge theory and its radiative corrections, black-hole thermodynamics and emission, the
rung-to-rung links), **not** as a replacement for quantum mechanics, quantum field theory or general relativity. The question asked of each item is narrow: did putting it in one chain with shared inputs
and an audited derivation show a relation, a hidden assumption or a convention-dependence that the separate literatures do not state? Each item below is labelled **KNOWN** (in the literature as far as I
know), **LOCAL** (a fact about this repository's method, not about physics), or **CANDIDATE** (not recognised as stated in the sources I could check; novelty not established). This note was written from the
campaigns of the Links 24 to 33 session; it does not re-evaluate the earlier rungs.

## What the compression showed

| # | Observation | Where | Label |
|---|---|---|---|
| 1 | The Higgs coefficient of the M_W prediction, 11α/(48πs²), splits into the Veltman-screened Δρ piece 3α/(16πs²) and α/(24πs²): 11/9 of what a Δρ-only treatment carries. | L26, L27 | KNOWN (textbook; the ladder reproduces it by derivation) |
| 2 | In general R_ξ all the ξ dependence of the self-energy class sits in [Σ_W(0) − Σ_W(M_W²)]/M_W², cancelled by vertex, box and wave-function terms; δZ_e and Σ_W/M_W² − Σ_Z/M_Z² are separately ξ independent; each class diverges like ±(3/4)(α/4π) ln ξ as ξ → 0⁺. | L32 | KNOWN in spirit (pinch-technique and Nielsen-identity literature); I did not check that the specific ln ξ coefficient and class split are tabulated |
| 3 | The charged spin-½ emission weight of a Schwarzschild hole (Carr's 0.142 against 0.147) is an O(α) effect whose value depends on which hole charge (before, mid, after emission) the grey-body factor and the chemical potential use: nine rules span 0.93 to 1.05, only about 1.85α of the slope is the fluctuation itself, the thermodynamically consistent rule gives 1.008 (f = 0.148), and the literature energy ratio 0.9905 cannot be reached in the model. | L30 | CANDIDATE: I could not read Page 1977 (abstract only) and did not search the later literature for a rule-by-rule accounting. Effect size: 2 to 3% on the Standard-Model emission count (15.35 against 15.71), small for constraints |
| 4 | Denner's ZZ axial-mass coefficient 3/(4s²c²) is the |I₃| = ½ case of 3I₃²/(s²c²); the published form hides the assumption. | L31 | KNOWN as algebra, trivial for the Standard Model; it was caught by the audit protocol, not by the physics |
| 5 | The one-loop M_W relation closes with derived pieces only; the whole discrepancy to the measured value falls from 0.13 GeV (L18c) to 0.04 GeV after the leading QCD term, with the remainder unexplained. | L18 → L33 | KNOWN (this is the standard electroweak-fit story); the ladder's content is the audited derivation, not a new relation |
| 6 | One coupling α and one set of masses feed Δα, Δr, the Z-pole shifts and the charged-hole emission; the dependency map lists 53 quantities shared across scripts. | all | LOCAL: bookkeeping of shared inputs; it shows where a change propagates, it does not predict anything |

## What the compression did not show

* No relation between two rungs that is absent from the literature and that was **not** put in as an input. Every cross-link above is either a standard identity or a number carried between modules.
* No prediction that distinguishes the ladder from the Standard Model plus general relativity. Where the ladder's own rung-1 to rung-6 claims enter (the earlier Links), they were not re-examined in this session.
* The one place the compression produced something I would call a finding rather than a reproduction is item 3, and it is a statement about the **ambiguity** of an existing calculation, not a new result about nature.

## What the method itself showed (LOCAL, and the more reliable finding)

* **Derived versus recited cannot be enforced by the gate.** Builders and auditors are language models and recalled famous results (the QCD coefficient, Denner's structure) before deriving them. "Blind" means blind to the oracle and
  the repository, not to the literature. For results that are famous numbers the agreement of independent builds is weaker evidence than for results nobody had memorised; the auditor's structurally different route is what carries the weight.
* **The weak point is almost always the oracle or the specification, not the builds.** In this session the errors found were mine: a sign convention for the photon field (bos_se), a fixed-precision reference (bos_dr), the |I₃| = ½ assumption (ferm_se), a too-sharp continuity probe, a false "principal rule only" claim (charged_half). The builds were right each time; the protocol earns its cost by finding the orchestrator's mistakes.
* **A compressed chain is only as good as its weakest quoted input.** Hadronic Δα, α_s and the top mass remain quoted; the remaining 0.04 GeV in M_W is not attributed to any of them.

## How a real structural discovery would show up

A test that would count: a relation between two quantities computed in different rungs, derived without either being an input to the other, that holds numerically beyond the shared inputs and is not already a textbook identity. Candidate places to look,
none yet checked: the charged-hole fluctuation spectrum against the Standard Model's charge quantisation (the equilibrium ⟨n²⟩ = 1/(4πα) sets how many elementary charges a hole carries, a rung 6 to rung 1 link); and whether the convention
dependence in item 3 has a gauge-theoretic analogue in item 2 (both are "which intermediate state does the coupling see"). These are questions, not claims.
