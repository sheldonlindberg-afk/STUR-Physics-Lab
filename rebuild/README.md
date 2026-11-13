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
| [cleanroom.py](cleanroom.py) | orchestrator | exports a directory the builder can work in without seeing answers |
| [prompts/](prompts) | each role | builder, verifier, auditor |
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
```

In Claude Code, `/rebuild-ladder` runs the protocol
([.claude/skills/rebuild-ladder/SKILL.md](../.claude/skills/rebuild-ladder/SKILL.md)).
