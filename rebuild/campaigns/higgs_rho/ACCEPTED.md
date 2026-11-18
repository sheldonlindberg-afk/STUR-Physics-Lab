# Accepted: campaign `higgs_rho` (the Higgs-mass dependence of the rho parameter at one loop)

*Result: from the bosonic electroweak Lagrangian in R_xi gauge, the Higgs-containing one-loop diagrams give Delta rho(m_H) - Delta rho(M_W) with the poles m_H-independent and cancelling, xi dropping out exactly, and the large-m_H form -(3 alpha/16 pi c^2) ln(m_H^2/M_W^2) + C, C = 9.54e-4; two builds agree to the double over 10 GeV .. 1e33 M_W, and an auditor's two independent routes agree with both.*

(The history below is the log of how it got there, including the orchestrator's own mistakes.)

| Step | Result |
|---|---|
| Builders | build a (Opus) running; build b (Sonnet) returned |
| Class R (orchestrator's bug) | my custodial blind check divided by alpha s^2 although alpha = g^2 s^2/4 pi already scales as s^2 at fixed g, so it contradicted its own docstring; build b reported it instead of forcing the gate. Fixed: the check is now Delta rho / alpha finite as M_Z -> M_W (Delta rho ~ g'^2 ~ alpha/c^2). |
| Build b, builder gate (after the fix) | PASS, 7 of 7 blind checks |
| Build b, verifier with the hidden oracle | PASS: log_coefficient = -3 alpha/(16 pi c^2) to 2.2e-16 at three input sets; the same at xi = 1, 0.3, 4; the measured large-mH slope -6.001224e-4 against the target -6.001224e-4 |

## Audit (Opus) and the strengthened gate

Verdict: ACCEPT the result (both builds physically correct, confirmed by two independent routes of the auditor's, an exact-d Feynman-parameter
evaluation and a 4D Euclidean radial integral, which agree with each other and with both builds to the double, and by build a's own direct
integration); **one high finding against the gate**: it verified only the large-m_H logarithm, so six wrong modules (seagull dropped or doubled,
finite 1/d part of B00 dropped, the sign of the (1 - xi) propagator term flipped, the heavy-Higgs formula used at all m_H, B0/B00 replaced by their
heavy-mass forms) passed the full verifier. Also: the oracle's xi check was vacuous (it tested the analytic coefficient, which takes xi but does not use it);
the raw self-energies were unverifiable because SPEC did not pin the tensor reduction.

Adopted (the auditor's references, independent of the builds): rho_higgs_rel against the finite-function reference at seven masses (1e-9), xi and mu
independence at finite m_H (xi = 0.3, 4, 25), Landau gauge xi = 0, the large-m_H constant C = 9.539e-4 (analytic, 1e-5), raw self-energies in the pinned
convention (1e-9), and SPEC section 2 now pins the convention (conventional dimensional regularization with k^mu k^nu -> g k^2/d keeping the O(eps)
part of 1/d, MS-bar Delta = 1/eps - gamma + ln 4pi, sum of 1PI diagrams = i Pi g^{mu nu}, M^2(eff) = M^2 + Pi, xi >= 0). All nine of the auditor's
mutants and controls that are wrong are now killed.

| Build | Strengthened oracle |
|---|---|
| a | 7 of 7 (zero deviation from the references) |
| b | 6 of 7: fails only "Landau gauge xi = 0 is accepted" (returns nan), a class B finding sent back with the label only, together with documentation items |

Remaining findings sent to the builders (documentation, no result changes): vertex factors of i and the derivation of the sign of the H-phi bubble product
(build b fixed the sign by demanding xi independence), explicit exclusion of mixed W-Z / W-photon loops and the quartic H-phi-W-Z / H-phi-W-A vertices,
build b's garbled ghost paragraph, and that `log_coefficient` is a hand-typed analytic expression (it follows from the large-m_H expansion; a
numerical check was requested). Not enforceable by the gate: that a build derived its closed forms instead of reciting them (the audit read both
derivations; build b's is terse but contains no recited formula). Status: **not accepted until both builds pass the strengthened gate**.

## Final state

| Phase | Evidence |
|---|---|
| P0 rooms | level 2 of PROTOCOL.md; scratch in `tmp/`, every command begins with `cd <room>`; transcript audits clean (`builds/*/isolation_audit.txt`, re-run after every round, canary absent) |
| P1 builders | `builds/a` (Opus), `builds/b` (Sonnet); the builder gates pass (7 of 7 blind checks) |
| P2 verifier | both builds pass the strengthened oracle: log coefficient and its measured slope, the finite function at seven masses (1e-9) against the auditor's independent references, xi and mu independence at finite m_H, Landau gauge, the large-m_H constant, the exact large-mH form up to 1e20 MW, and the raw self-energies in the pinned convention (`builds/*/verifier_report.txt`, 26 passes each) |
| P3 cross-build | exact agreement (relative difference 0.0) on rho and Pi_WW at nine points from 10 GeV to 8e33 GeV, including xi = 0, 0.4, 1, 2, 3 and different mu |
| P4 audit | Opus auditor (`AUDIT.md`): physics confirmed by two independent routes; one high finding against the gate, fixed as above; nine mutants all killed |
| Class counts | R (orchestrator): 2 (the custodial check divided by alpha s^2; the first extreme-mass starting point too low); B: 2 (build b nan at xi = 0, its working precision at extreme m_H); C: 1 (SPEC pinned the tensor reduction); N: documentation items in both builds |

## What is and is not established

* **Established:** the Feynman rules, the complete Higgs-containing diagram set (the H seagull, the H-gauge bubble and the H-Goldstone bubble for W and Z; tadpoles cancel in
  Delta rho), the pole structure, the exact xi independence, the coefficient of ln m_H^2, and the finite function, by two builds and three independent evaluations.
* **Not established:** that a build derived and did not recite (the gate cannot enforce it; the audit read both derivations, build b's is terse); the
  full Higgs dependence of Delta r, which also needs the q^2-dependent self-energies (this campaign is Delta rho at q = 0); the exact agreement
  of the builds is algebraic (equivalent expressions evaluated at high precision), so it checks implementation and the shared SPEC conventions, not the physics, which
  the auditor's routes and the literature coefficient (-3 alpha/16 pi c^2, hidden oracle) check.
