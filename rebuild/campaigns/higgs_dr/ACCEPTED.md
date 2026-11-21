# Accepted: campaign `higgs_dr` (the Higgs dependence of Delta r from the q^2-dependent W and Z self-energies)

*Result: from the bosonic electroweak Lagrangian, the Higgs-containing one-loop W and Z self-energies at general q^2, Pi_V(q^2) = (kappa^2/16 pi^2)[-M^2 B0 + B00 - A0(m_H)/4], and the muon-decay relation give Delta r_H = [Pi_W(M_W^2) - Pi_W(0)]/M_W^2 + (c^2/s^2)[Pi_Z(M_Z^2)/M_Z^2 - Pi_W(M_W^2)/M_W^2]; its large-m_H form is (11/12)(alpha/4 pi s^2)[ln(m_H^2/mu^2) - 5/6], coefficient 11 alpha/(48 pi s^2) = 11/9 of the Delta rho screening term. Two builds agree exactly (relative difference 0.0) and an auditor's three independent routes agree with both.*

| Step | Result |
|---|---|
| Orchestrator reference | `reference_dr.py` (Feynman parameters, mpmath 40 digits): q^2 = 0 reproduces the accepted higgs_rho Delta rho to 2e-14; heavy-Higgs slope 11 alpha/(48 pi s^2) to 1e-8 |
| Builders | build a (Opus) and build b (Sonnet), blind, rooms outside the repository; builder gates 7 of 7 (9 after strengthening) |
| Isolation | transcript audits clean after all rounds (`builds/*/isolation_audit.txt`, four canary tokens absent) |
| First verifier | both passed the original oracle |
| Audit (Opus, `AUDIT.md`) | reference independently re-derived (Feynman rules in sympy; analytic Passarino-Veltman to 1e-37; dispersion relation with Cutkosky cuts to 1e-10; 4D Euclidean integral to 6e-12); no class R error; 15 wrong mutants, 3 survived the original gate |
| Strengthened gate | adopted `audit_proposed_checks.py`: Pi proportional to alpha and the coupling scaling (blind), Delta r_rel on a dense grid 1 GeV .. 2e7 GeV, raw self-energies at three (M_W, M_Z, alpha) with q^2 from -500 M_W^2 to near threshold (oracle), the extreme-mass check with the build at its own precision |
| Build b after the strengthening | failed the extreme-mass check at 1e14 M_W by 4e-4 (it relied on a global mpmath precision of 30 digits, which the orchestrator's reference module had been silently raising to 40); label-only round trip; fixed (local precision 90 digits, integration breakpoints to 1 - 1e-44); passes |
| Final verifier | both builds pass: 30 of 30 checks each (`builds/*/verifier_report.txt`) |

## Class counts

R (orchestrator): 1 (reference module set the global mpmath precision, which leaked into the gate and hid build b's reliance on it); B: 1 (build b, global precision; minor: W-phi-H vertex written without i, no threshold guard); C: 3 (the gate had no check away from the campaign inputs, between 5 TeV and 8e7 GeV, or at deep spacelike q^2); N: documentation items.

## What is and is not established

* **Established:** the Higgs-containing diagram set (seagull, H-gauge bubble, H-Goldstone bubble; tadpoles cancel in both brackets of Delta r), the q^2 dependence, the one-loop muon-decay relation of Delta r_H to the self-energies, the coefficient of ln m_H^2, the finite function.
* **Not established:** that a build derived and did not recite (the gate cannot enforce it; the audit read both derivations); gauge independence of Delta r_H (the gauge is fixed to Feynman; the earlier higgs_rho campaign showed xi independence of Delta rho only); the m_H-independent MS-bar constants of the raw self-energies are checked only against my reference and the auditor's routes of the same dim-reg definition; the gauge-boson loops of Delta rho, the vertex and box terms, the photon-Z mixing beyond the absence of Higgs diagrams, and two-loop terms.
* **Consequence for the ladder:** L18's Higgs term (3 G_F M_W^2/8 sqrt2 pi^2) ln(m_H^2/M_W^2) was the Delta rho screening part only; `src/ladder_links.py` L27 replaces it (M_W 80.501 GeV, Delta r_rest 0.0075).
