# rebuild/: having an AI rebuild the ladder from first principles

A framework for having AI agents rebuild [`src/ladder_standalone.py`](../src/ladder_standalone.py)
**blind**, from postulates and measured inputs only. A harness, not the AI, decides
whether each step is right.

| File | For | What it is |
|---|---|---|
| [PROTOCOL.md](PROTOCOL.md) | orchestrator | roles, phases, gates, isolation levels |
| [SPEC.md](SPEC.md) | builder | postulates and conventions per stage, **with no answers** |
| [contract.py](contract.py) | builder, harness | every export's signature, units and allowed provenance |
| [inputs.py](inputs.py) | builder | the only source of numbers (PDG, CODATA, FLAG, Planck, EHT, LVK) |
| [blind/checks.py](blind/checks.py) | builder, harness | identities, limits, two-route and scaling checks; no reference values |
| [harness.py](harness.py) | everyone | the gatekeeper: contract → lint → blind → sensitivity → oracle → cross-build |
| [oracle.py](oracle.py) | verifier only | differential comparison with the reference, plus pinned numbers |
| [chain_compare.py](chain_compare.py) | verifier only | the force chain ([`src/force_chain.py`](../src/force_chain.py)) against an accepted build, wherever they overlap |
| [cleanroom.py](cleanroom.py) | orchestrator | exports a directory the builder can work in without seeing answers |
| [prompts/](prompts) | each role | builder, verifier, auditor |
| [HANDOFF.md](HANDOFF.md) | next orchestrator | status of build 2026-11-a and what to do before build b (contains answers: never copy it into a clean room) |
| `_selftest/` | CI only | the reference wrapped to the contract, to prove the harness passes correct builds |
| `builds/<id>/` | output | one AI build: stage modules, derivation notes, findings, ledger, audit |

```bash
# the harness itself is tested: it passes the reference and catches planted defects
python -m pytest tests/test_rebuild_harness.py -q

# a builder, inside its clean room
python3 harness.py builds/2026-11-a --mode builder --stage gauge331

# the verifier, in the repository
python3 rebuild/harness.py rebuild/builds/2026-11-a --mode verifier --ledger
python3 rebuild/harness.py rebuild/builds/2026-11-a --mode verifier --compare rebuild/builds/2026-11-b

# the force chain against the accepted builds (tests/test_chain_vs_rebuild.py runs it in CI)
python3 rebuild/chain_compare.py rebuild/builds/2026-11-a rebuild/builds/2026-11-b
```

**The force chain and the rebuild.** `chain_compare.py` compares the force chain's hand-offs with
an accepted build in two ways. With the chain's own arguments, the build must agree to rounding.
On its own inputs, the build must agree, or differ only for a recorded cause within a recorded
band. Both accepted builds agree on all 19 overlaps: 11 same-argument comparisons to ≤ 6e-16, and
8 own-route comparisons. Two causes explain every own-route difference:
- the chain derives f_π = 130.57 MeV from G_F and Γ(π→μν), while the rebuild reads 130.2 MeV.
  This moves the π⁰ width from 7.742 to 7.785 eV. It is still open, because SPEC must choose a route;
- the chain inherits src's grid-point safe gap, 181.16 µm (2.1868 rad), while the rebuild bisects
  to the root, 181.107 µm (2.1878 rad). See FINDINGS N3.

In Claude Code, `/rebuild-ladder` runs the protocol
([.claude/skills/rebuild-ladder/SKILL.md](../.claude/skills/rebuild-ladder/SKILL.md)).
