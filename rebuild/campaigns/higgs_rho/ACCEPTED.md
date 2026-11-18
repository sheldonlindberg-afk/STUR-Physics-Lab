# Campaign `higgs_rho`: in progress (not accepted)

Status log; the acceptance sections are written when both builds, the cross-build comparison and the audit are done.

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
