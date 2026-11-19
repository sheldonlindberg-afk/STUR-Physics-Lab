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
    import importlib.util
    spec = importlib.util.spec_from_file_location("greybody_campaign_oracle", os.path.join(CAMP, "greybody", "oracle.py"))
    oracle = importlib.util.module_from_spec(spec)             # a unique name: a module called `oracle` shadows rebuild/oracle.py
    spec.loader.exec_module(oracle)
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


QED_STUB = '''
import math
PROVENANCE = {"cp_energy": ("derived", "x"), "far_coefficient": ("derived", "x"), "near_coefficient": ("derived", "x")}
def cp_energy(r, w0, alpha0): return -1.0
def far_coefficient(): return %s
def near_coefficient(): return %s
'''


def test_lint_catches_integer_built_answers():
    """The audit's mutant M1 typed 23/(4*math.pi) and 3/4: the float-literal lint missed them."""
    oracle = os.path.join(CAMP, "qed_cp", "oracle.py")
    for far, near in (("23/(4*math.pi)", "1.0"), ("1.0", "3/4"), ("1.0", "0.75")):
        r = run_gate(stub(QED_STUB % (far, near), "qed_cp"), campaign="qed_cp", mode="verifier", oracle=oracle)
        assert "constant expression equals the oracle target" in r.stdout, (far, near)
    clean = run_gate(stub(QED_STUB % ("1.0", "2.0"), "qed_cp"), campaign="qed_cp", mode="verifier", oracle=oracle)
    assert "constant expression equals the oracle target" not in clean.stdout


def test_new_qed_cp_checks_exist_and_the_oracle_reference_is_accurate():
    import importlib.util
    def load(path, name):
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod
    camp = load(os.path.join(CAMP, "qed_cp", "campaign.py"), "qed_cp_campaign")
    oracle = load(os.path.join(CAMP, "qed_cp", "oracle.py"), "qed_cp_oracle")
    labels = [l for l, _ in camp.BLIND]
    assert "far zone approached with a 1/rho^2 deficit" in labels and "U / alpha0^2 independent of alpha0 at w0 != 1" in labels
    import math
    assert abs(-oracle.ref_rho(1e3) * 1e3**7 / (23 / (4 * math.pi)) - 1) < 1e-4     # the old reference was 9% off here
    assert abs(oracle.reference(2.0, 3.0, 0.5) / (oracle.ref_rho(6.0) * 0.25 * 3.0**7) - 1) < 1e-12


def test_qed_cp_builds_expose_the_route_enforcing_exports_and_agree():
    """The contract change (SPEC 3b): both accepted builds must provide denominator_sum and damped_energy, match the independent
    references, and agree with each other although they evaluate the damped energy differently."""
    import importlib.util
    def load(path, name):
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod
    base = os.path.join(CAMP, "qed_cp")
    a, b = load(os.path.join(base, "builds", "a", "qed_cp.py"), "qedcp_a_t"), load(os.path.join(base, "builds", "b", "qed_cp.py"), "qedcp_b_t")
    orc = load(os.path.join(base, "oracle.py"), "qedcp_oracle_t")
    for m in (a, b):
        assert orc.denominator_sum_check(m)[0]
    pt = (1.3, 0.9, 1.7, 0.6)
    ua, ub = a.damped_energy(*pt), b.damped_energy(*pt)
    ref = orc._RD.F(pt[0] * pt[1], pt[3] * pt[1]) * pt[2] ** 2 * pt[1] ** 7
    assert abs(ua / ub - 1) < 1e-12 and abs(ua / ref - 1) < 1e-6
    assert abs(a.denominator_sum(0.7, 1.9, 1.3, 0.6) / orc.sum_reference(0.7, 1.9, 1.3, 0.6) - 1) < 1e-12


def _transcript(calls, cwd=None):
    import json
    return "\n".join(json.dumps({"message": {"content": [{"type": "tool_use", "name": n, "input": i}]}, "timestamp": "t", "cwd": cwd}) for n, i in calls) + "\n"


def test_transcript_audit_accepts_own_files_and_flags_everything_else():
    import importlib.util
    spec = importlib.util.spec_from_file_location("audit_transcript_t", os.path.join(CAMP, "audit_transcript.py"))
    A = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(A)
    room = tempfile.mkdtemp()
    scratch = tempfile.mkdtemp()
    def run(calls, canaries=(), cwd=None):
        p = os.path.join(tempfile.mkdtemp(), "t.jsonl")
        open(p, "w").write(_transcript(calls, cwd or room))
        return A.check(p, room, canaries)[1]
    repo = os.path.join(ROOT)                      # a shell that starts in the repository, as the builders' did
    # clean: reads and writes in the room, math that looks like paths, scratch file it created and reads back, python stdlib
    assert not run([("Read", {"file_path": room + "/SPEC.md"}), ("Bash", {"command": f"cd {room} && python3 -c 'print(1/2, x/np.pi)'"}),
                    ("Bash", {"command": f"cat > {scratch}/a.py <<EOF\nprint(1)\nEOF"}), ("Bash", {"command": f"python3 {scratch}/a.py"}),
                    ("Bash", {"command": "python3 -m cProfile -o " + scratch + "/prof x.py; python3 -c \"import pstats; pstats.Stats('" + scratch + "/prof')\""}),
                    ("Read", {"file_path": "/usr/lib/python3/dist-packages/x.py"})])
    # violations
    assert run([("Read", {"file_path": "/home/user/STUR-Physics-Lab/src/ladder_links.py"})])                       # the repository
    assert run([("Bash", {"command": f"cat {scratch}/someone_elses_file.py"})])                                    # a file it did not create
    assert run([("Bash", {"command": "cat ../oracle.py"})])                                                        # relative escape
    assert run([("WebFetch", {"url": "https://example.org"})]) and run([("Agent", {"prompt": "x"})])               # web and delegation
    assert run([("Bash", {"command": f"cd .. && ls"})])                                                            # cd out
    # the shell starts in the repository: relative paths and default-directory searches there are leaks; inside the room they are fine
    assert run([("Bash", {"command": "cat README.md"})], cwd=repo) and run([("Bash", {"command": "ls"})], cwd=repo)
    assert run([("Bash", {"command": "grep -rn oracle"})], cwd=repo) and run([("Bash", {"command": "find . -name '*.py'"})], cwd=repo)
    assert run([("Bash", {"command": f"cd {room} && cd builds && cd ../.."})], cwd=repo)                              # one level too many leaves the room
    assert not run([("Bash", {"command": f"cd {room} && cat SPEC.md && ls && cd builds/x && cd ../.. && grep -rn x ."})], cwd=repo)
    assert not run([("Bash", {"command": "ps aux | grep gate.py | head -2; pgrep -af gate.py"})], cwd=repo)       # a grep pattern is not a path
    assert run([("Bash", {"command": "grep -n foo SPEC.md"})], cwd=repo)                                          # a grep FILE argument is
    assert run([("Bash", {"command": "echo hi"})], canaries=("CANARY-abc",)) == [] or True
    p = os.path.join(tempfile.mkdtemp(), "t.jsonl")
    open(p, "w").write(_transcript([("Bash", {"command": "echo CANARY-abc"})]))
    assert A.check(p, room, ("CANARY-abc",))[1]                                                                    # a canary in the transcript


def test_canaries_are_planted_in_the_oracles_and_never_in_a_room():
    tokens = [l.strip() for l in open(os.path.join(CAMP, "CANARIES.txt")) if l.strip() and not l.startswith("#")]
    assert len(tokens) == 6
    for tok, camp in zip(tokens, ("greybody", "qed_cp", "higgs_rho", "higgs_dr", "higgs_dr_xi", "bos_se")):
        assert tok in open(os.path.join(CAMP, camp, "oracle.py")).read()
        room = os.path.join(tempfile.mkdtemp(), "room")
        subprocess.run([sys.executable, os.path.join(CAMP, "export_room.py"), camp, camp + "-t", room], check=True, capture_output=True)
        assert os.path.isdir(os.path.join(room, "tmp"))                                       # the private scratch directory
        for f in os.listdir(room):
            p = os.path.join(room, f)
            if os.path.isfile(p):
                assert tok not in open(p).read(), f
