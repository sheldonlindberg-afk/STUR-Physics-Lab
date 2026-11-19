# Accepted: campaign `higgs_dr_xi` (gauge-parameter independence of the Higgs part of Delta r)

*Result: in R_xi gauge (all xi >= 0, Landau gauge included) the g^{mu nu} coefficient Pi_VV(q^2) of the Higgs-containing W and Z self-energies is xi independent at every q^2 below threshold, so Delta r_H(m_H) - Delta r_H(M_W) is xi independent and equals the Feynman-gauge value of the higgs_dr campaign. The xi dependence of the diagrams lives only in the q^mu q^nu part and the V-Goldstone mixing, which do not enter muon decay with massless leptons.*

| Step | Result |
|---|---|
| Prediction (orchestrator, before the builds) | m_H enters only through Higgs lines and Delta r is physical, so the m_H dependence cannot depend on xi; the oracle used the Feynman-gauge reference of higgs_dr at every xi |
| Builders | build a (Opus), build b (Sonnet), blind; both answered "independent of xi" and derived why (a: split of the propagator, with an unsplit Feynman-parameter second route agreeing to 13 digits; b: partial fractions, the H-V xi term +B00(q^2; m_H, sqrt(xi) M)/M^2 cancelling the H-Goldstone -B00) |
| Isolation | transcript audits clean (`builds/*/isolation_audit.txt`, five canary tokens absent) |
| Audit (Opus, `AUDIT.md`) | independent derivation: Feynman rules in sympy; xi derivative of the transverse projection of (H-V + H-Goldstone) is zero pointwise in the loop momentum; Pi_g against the reference to 5e-25 at xi = 0, 0.3, 1, 4, 25; a 4D Euclidean route per diagram to 1e-13 at 144 points; each diagram alone depends strongly on xi (H-V part 2851 -> 80990 for xi 0 -> 25), the sum does not; the q^mu q^nu part and the mixing depend on xi and decouple; Landau-gauge unphysical thresholds cancel; no class C finding |
| Gate strengthening | 16 mutants, 8 survived; six were genuinely wrong (a xi-dependent common shift, an off-shell xi term in Pi_Z, an error only at xi > 30, a massless Goldstone for small xi, a threshold clip, a wrong spacelike sign at xi != 1); adopted as oracle checks: sigma xi independent on a wide xi grid (0 .. 1e4), delta_r on a wide xi grid, log_coefficient on a wide xi grid; all six now killed; the two survivors that are right (xi ignored entirely, a consistently wrong Goldstone mass that cancels) produce correct outputs |
| Final verifier | both builds pass (`builds/*/verifier_report.txt`) |

## What is and is not established

* **Established:** the Higgs-containing sector of Delta r is gauge-parameter independent in R_xi gauge, by two builds, an independent derivation and two numerical routes. The Link 27 result therefore does not depend on the Feynman-gauge choice.
* **Not established:** the gate cannot distinguish true xi independence from a build that ignores xi (class C finding of the audit: the independent derivation is the evidence, and the oracle's wide-xi checks are justified by it); Pi^L and the V-phi mixing were computed by one route (the auditor's) without a Slavnov-Taylor cross-check; the tadpoles' xi dependence is argued from the vertices (they cancel in Delta r); the 4D route covers spacelike q^2 only; the m_H-independent constants rest on the same dim-reg conventions as the reference. Build b's "unitary vs diagram sum" check is not independent of its own split (audit B1, minor). Gauge independence of the gauge-boson loops, vertex and box terms is a separate matter and was not tested.
* **Class counts:** R: 0; B: 1 minor (build b's self-check); C: 3 (the gate could not test raw sigma at xi != 1, nor xi between 0 and 0.3 or above 25, nor distinguish a build that ignores xi); N: tadpole note.
