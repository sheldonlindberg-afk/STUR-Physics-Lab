# Accepted: campaign `nucleon_pol` (nucleon polarizabilities from the pion cloud, leading order heavy-baryon chiral perturbation theory)

*Result: two blind builds (Opus a, Sonnet b) derived, by static-field energy shifts of the charged-pion cloud, **alpha_E = 5 alpha gA^2 / (96 pi f_pi^2 m_pi)** and **beta_M = alpha_E / 10** in the SPEC convention H_eff = -1/2 4 pi (alpha_E E^2 + beta_M B^2)
(12.58e-4 and 1.258e-4 fm^3 at gA = 1.27, f_pi = 92.4 MeV, m_pi = 139.57 MeV; measured proton 11.2(4) and 2.5(4)). An auditor re-derived them through the Born-subtracted real-photon Compton amplitude at general energy and angle
(perpendicular polarization e^2 w^2 (10 + cos t)/(96 pi m_pi), in-plane e^2 w^2 (1 + 10 cos t)/(96 pi m_pi)), which checks the two steps build b had only argued (static-field shift = Born-subtracted O(w^2) coefficient; zero-frequency argument).*

| Phase | Evidence |
|---|---|
| P0 clean rooms | Level 2 of PROTOCOL.md section 3 |
| P1 builders | `builds/a`, `builds/b`; each passed `gate.py --mode builder` |
| P2 verifier | `gate.py --mode verifier` with the hidden oracle and the audit's four checks plus extended lint: `builds/*/verifier_report.txt` (all PASS) |
| P3 cross-build | identical to every printed digit; build a also checks the position-space gauges (2e-15) and the Baldin sum rule with the real-photon gamma p -> pi+ n tree cross section for alpha + beta (2e-14) |
| P4 audit | `AUDIT.md`: independent Compton-amplitude route, neutron = proton shown explicitly (pi0 has no photon vertex; Weinberg-Tomozawa terms vanish: A0 pieces zero in radiation gauge, the pi pi N N piece is C-odd), 21 wrong mutants of build a (14 killed by the first gate, all 21 by the adopted checks): no build bug |

## Class counts
B: 0. R: 2 SPEC wording gaps, fixed: "forward Compton amplitude" gives only alpha + beta (now general angle); the Born graphs vanish when e.v = 0 and m_N -> infinity (now stated). C: the oracle pinned only two pure numbers in narrow positive ranges (seven wrong mutants passed: negative gA, a clamped or drifting range, a typed-in closed form, abs() in the unit conversion); adopted checks added; lint now includes the denominators 96, 192, 384, 768.
Neutron = proton cannot be tested by the gate (no isospin argument in the exports). N: build b's prose on Born graphs is loose.

## What is and is not established
* **Established (within the SPEC):** the O(p^3) heavy-baryon coefficients, the convention (the SPEC's alpha_E equals the Gaussian-unit polarizability; the "natural Heaviside-Lorentz" value would be 4 pi times larger), the angle structure, the isospin statement.
* **Limits:** (i) both builders and the auditor are language models that knew the textbook result; the oracle reference was recalled; the independence evidence is the auditor's different gauge, real photons and diagram handling, not ignorance of the answer. (ii) shared with all derivations: the Lagrangian and vertex normalization, the heavy-baryon limit, no Delta and no counterterms, one pion mass.
  (iii) The leading-order beta_M is half the measured value: the missing part is the Delta(1232) paramagnetic term, excluded by the SPEC. alpha_E at LO is 12% above the measured value.

## Isolation evidence
`builds/{a,b}/isolation_audit.txt`: transcript audit, clean. Level 2, not level 3.
