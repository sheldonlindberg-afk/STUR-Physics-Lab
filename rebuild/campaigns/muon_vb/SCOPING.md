# Scoping: the vertex, box and bosonic corrections to the MS-bar relation (not launched)

This is the part of B7's +0.35% that L22 leaves open: Delta r-hat_W - Delta r_0 = 0.0029 and the bosonic 9% of
rho-hat - 1. It is not launched as a campaign yet, for a reason that would make any builder fail for the wrong cause:

**There is no unambiguous finite observable written down yet.** Vertex, box and wave-function pieces are
individually gauge- and scheme-dependent; they combine into a finite, gauge-independent quantity only together with
specific self-energy and counterterm pieces (the on-shell Delta r of Sirlin, or the MS-bar Delta r-hat_W of
Degrassi-Sirlin-Marciano). A SPEC.md that says "compute delta_VB" would leave the builder guessing which pieces to
include, and a hidden oracle (the textbook delta_VB = (alpha/4 pi s^2)[6 + (7 - 4 s^2)/(2 s^2) ln c^2]) could then
fail a correct calculation of a differently-defined quantity. That is the failure the protocol calls class C, and
it should be removed before spending two builds on it.

What a well-posed campaign needs, in order:
1. A SPEC.md that fixes the observable: the full one-loop correction to the muon-decay amplitude in the on-shell
   scheme with the W, Z, gamma, Higgs, Goldstone and ghost content, 't Hooft-Feynman gauge, massless external
   leptons, the list of diagrams, and which counterterms are included; the target is the on-shell Delta r (not a piece).
2. Oracle values that are sourced and checked against more than one published evaluation (the on-shell Delta r at
   several (m_t, m_H) from two independent programs or papers), with the tolerance set by their agreement.
3. Blind checks: UV pole cancellation, gauge-parameter independence (compute in a general R_xi gauge and check the
   sum does not move), the decoupling limits (m_t -> infinity gives the known m_t^2 term already derived in L18),
   and the ward identity of L18a for the self-energy pieces.
4. Staged exports (self-energies at q^2 = 0, then vertex, then box, then the sum) so each stage has its own gate.

Until (1) and (2) exist, running builders would test the SPEC, not the physics.

## Decision (orchestrator, on the user's instruction to decide what fits best)

The textbook delta_VB is not launched as a campaign: it is finite and gauge-independent only together with the on-shell counterterms and
a Fermi-theory subtraction, so a SPEC for it would test the SPEC. The first stage instead is the one piece of the bosonic remainder that
is gauge-independent and sharply defined: the Higgs-mass dependence of Delta rho (`rebuild/campaigns/higgs_rho`), which also replaces the
Higgs-log term that L18 quotes. Later stages (the full bosonic Delta rho in a fixed gauge with the pinch parts, then vertex and box) can
reuse its infrastructure once that campaign shows the method works.
