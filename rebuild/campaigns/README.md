# Campaigns: systematic AI derivations of the repository's remaining open items

The ladder rebuild (`../PROTOCOL.md`) re-derives results that already exist. A **campaign** applies the same
discipline to a result that does *not* yet exist in the repository, so the first implementation is also blind,
independent and audited. Same failure modes, same defences:

| Failure | Defence here |
|---|---|
| Answer leakage | Clean room outside the repo (`export_room.py`); the oracle is never exported; the lint rejects literals within 1% of an oracle target |
| Hard-coding / special-casing | Blind property checks that are not the answer (limits, scalings, slopes, symmetries) |
| Plausible but wrong | The hidden oracle, with targets from the literature or from an independent route, run by the orchestrator |
| Self-grading | `gate.py`'s exit code and `gate_report.json` are the evidence, not an agent's report |
| Shared blind spots | Two builds on different models, compared; an independent route stated in each SPEC |
| Provenance inflation | `PROVENANCE` per export; `quoted` only where `campaign.QUOTED_ALLOWED` allows it; a `DERIVATION.md` that an auditor reads |

## Files

* `gate.py`: the generic gate (contract, lint, blind checks; with `--oracle`, the oracle). The builder runs it in
  `--mode builder`; the orchestrator runs `--mode verifier`.
* `export_room.py <campaign> <build_id> <room>`: the clean room (never inside the repository, never with `oracle.py`).
* `audit_transcript.py`, `CANARIES.txt`, `ISOLATION.md`: the isolation record (what is enforced, what is evidenced, what is not).
* `BUILDER.md`: the builder's instructions. `<campaign>/SPEC.md`: postulates, no answers. `<campaign>/campaign.py`:
  exports and blind checks (the builder may read it). `<campaign>/oracle.py`: hidden targets.

## Phases (each gate is a program's exit code)

P0 export two rooms; P1 two independent builders (different models), each must pass `--mode builder`, and each builder's transcript is audited for isolation (`audit_transcript.py`, `ISOLATION.md`);
P2 the orchestrator runs `--mode verifier --oracle` on each build; P3 cross-build: both builds on the same
arguments must agree; P4 an auditor session reads `DERIVATION.md` and the code, writes mutants, and every
surviving mutant becomes a new blind check; P5 accept: only then does a result enter `src/ladder_links.py`.

A campaign that fails honestly is a result: it says the SPEC is ambiguous or the problem harder than specified.
Class labels for oracle disagreements follow `../PROTOCOL.md` (B builder bug, R reference or oracle bug, C spec
change, N numerical).

## Campaigns

| Campaign | Replaces a quoted result | Targets (hidden) | Independent route |
|---|---|---|---|
| `greybody` | L7's weights 0.267, 0.147, 0.060, 0.007 and the 5.34e25 coefficient (Carr et al. 2021, after Page 1976) | power per degree of freedom for s = 0, 1/2, 1, 2 | solve the master equations; the oracle's own integration agreed to 1% |
| `qed_cp` | the Green-tensor formula's dyadic step (L21b) | 23/(4 pi) far zone, 3/4 near zone, the crossover | perturbation theory over photon modes vs the repository's imaginary-frequency integral |
| `muon_vb` | B7's remaining Delta r-hat_W - Delta r_0 and the bosonic 9% | see `muon_vb/SCOPING.md`: not launched | |
