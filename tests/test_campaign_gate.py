"""Pins rebuild/campaigns: the gate must reject leaks and bad builds, and the exporter must never ship the oracle."""
import json, os, subprocess, sys, tempfile
ROOT = os.path.join(os.path.dirname(__file__), "..")
CAMP = os.path.join(ROOT, "rebuild", "campaigns")


def run_gate(build, campaign="greybody", mode="builder", oracle=None):
    cmd = [sys.executable, os.path.join(CAMP, "gate.py"), build, "--mode", mode, "--campaign", os.path.join(CAMP, campaign), "--timeout", "30"]
    if oracle:
        cmd += ["--oracle", oracle]
    return subprocess.run(cmd, capture_output=True, text=True, timeout=300)


def stub(code, name="greybody"):
    d = tempfile.mkdtemp()
    open(os.path.join(d, name + ".py"), "w").write(code)
    open(os.path.join(d, "DERIVATION.md"), "w").write("stub")
    return d


GOOD_SHAPE = '''
PROVENANCE = {"transmission": ("derived", "x"), "absorption_sum": ("derived", "x"), "power_per_dof": ("derived", "x")}
def transmission(s, j, w): return 0.5
def absorption_sum(s, w): return 1.0
def power_per_dof(s): return 1.0
'''


def test_a_wrong_build_fails_the_blind_tier():
    r = run_gate(stub(GOOD_SHAPE))
    assert r.returncode == 1 and "GATE FAILED" in r.stdout and "[FAIL] low-frequency scalar limit" in r.stdout


def test_lint_rejects_forbidden_imports_and_inputs_import():
    for bad in ("import os\n", "from inputs import X\n", "x = open('f')\n"):
        r = run_gate(stub(bad + GOOD_SHAPE))
        assert r.returncode == 1 and "[FAIL] lint" in r.stdout


def test_quoted_provenance_is_refused_outside_the_allowed_list():
    code = GOOD_SHAPE.replace('("derived", "x"), "absorption_sum"', '("quoted", "x"), "absorption_sum"', 1)
    r = run_gate(stub(code))
    assert r.returncode == 1 and "quoted not allowed" in r.stdout


def test_oracle_literal_lint_catches_a_typed_in_answer():
    sys.path.insert(0, os.path.join(CAMP, "greybody"))
    import importlib
    oracle = importlib.import_module("oracle")
    typed = GOOD_SHAPE.replace("return 1.0\n", "return %r\n" % (oracle.TARGET[1] * 1.004), 1) if False else GOOD_SHAPE + "\nP1 = %r\n" % (oracle.TARGET[1] * 1.004)
    r = run_gate(stub(typed), mode="verifier", oracle=os.path.join(CAMP, "greybody", "oracle.py"))
    assert "within 1% of an oracle target" in r.stdout


def test_exporter_never_ships_the_oracle_or_the_repository():
    for c in ("greybody", "qed_cp"):
        room = os.path.join(tempfile.mkdtemp(), "room")
        subprocess.run([sys.executable, os.path.join(CAMP, "export_room.py"), c, c + "-t", room], check=True, capture_output=True)
        names = set(os.listdir(room))
        assert {"gate.py", "campaign.py", "SPEC.md", "BUILDER.md", "inputs.py"} <= names
        assert not names & {"oracle.py", "src", "tests", "results"}
        for f in names:
            if f.endswith((".py", ".md")):
                text = open(os.path.join(room, f)).read()
                assert "23/(4" not in text and "0.267" not in text, f          # no oracle targets in anything shipped
    r = subprocess.run([sys.executable, os.path.join(CAMP, "export_room.py"), "greybody", "x", os.path.join(ROOT, "scratch-room")], capture_output=True, text=True)
    assert r.returncode != 0                                                        # a room inside the repository is refused
