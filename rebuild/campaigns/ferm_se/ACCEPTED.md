# Accepted: campaign `ferm_se` (fermion-loop one-loop self-energies of gamma, Z, W)

*Result: two blind builds derived the fermionic transverse self-energies Sigma^AA, Sigma^AZ, Sigma^ZZ, Sigma^W (any fermion list, any weak isospin, MS-bar, 't Hooft-Feynman gauge) from the SPEC's
Lagrangian: couplings, d-dimensional traces, Feynman-parameter / Passarino-Veltman reduction. They agree with each other, with an auditor's independent derivation (sympy) and an independent
dispersion-relation numerics to ~1e-14 (75 points: thresholds, k^2 = 0, masses 1e-6..1e4 GeV, unusual charges, mu 1..1e4 GeV), and with the transcription of Denner's appendix B to ~1e-12.*

| Phase | Evidence |
|---|---|
| P0 clean rooms | Level 2 of PROTOCOL.md section 3 (same caveat as `greybody`) |
| P1 builders | `builds/a` (Opus), `builds/b` (Sonnet); each passed `gate.py --mode builder` |
| P2 verifier | the orchestrator ran `gate.py --mode verifier` with the hidden oracle, including the five audit checks: `builds/*/verifier_report.txt` (all PASS) |
| P3 cross-build | agree to ~1e-14 (audit table; Link 31: the fermionic Delta r of the two builds differs by 3e-17) |
| P4 audit | `AUDIT.md` (Opus; independent derivation, independent numerics, 24 mutants of build a, 17 killed by the first gate, all 24 by the adopted checks): no defect in either build |

## Class counts
B (builder bug): 0. R (oracle/SPEC weakness): 3 + 1, all addressed. (i) my reference used Denner's 3/(4 s2 c2) axial mass term, valid for |I3| = 1/2 only; the SPEC allows any I3, so the oracle's "odd" set failed build b;
the reference is now 3 I3^2/(s2 c2) (both builds and the audit's derivation agree: g_L - g_R = I3/(s c)). (ii) the SPEC did not name the gamma5 scheme (now NDR) and (iii) wrongly said Sigma_T is analytic at k^2 = 0
(massless loops: continuous, slope divergent; reworded). (iv) the oracle was over-strict at exact zeros (floor added). C: reference is a transcription of a published formula at k^2 = 0 evaluated at 1e-18 (harmless).
Blind tier is weak (3 of 24 mutants), the oracle carries the weight. N: prose slips in the DERIVATION.md files.

## What is and is not established
* **Established:** the couplings, the sign of Sigma^AZ under the SPEC's photon convention (opposite to Denner's; oracle flips), the axial mass term for general I3, no finite rational remainder in the NDR scheme,
  the W weight N_C |V|^2, thresholds as real parts, mu-linearity, the massless limits.
* **Not established:** the gamma5 scheme is a convention (the 't Hooft-Veltman scheme would add finite terms to Sigma_ZZ and Sigma_W; whether they cancel in Delta r was not checked). The oracle reference is not an independent derivation.
  The light-quark masses are model inputs: Link 31 replaces the hadronic block by the quoted Delta alpha_had.

## Isolation evidence
`builds/{a,b}/isolation_audit.txt`: transcript audit, clean. Level 2, not level 3.
