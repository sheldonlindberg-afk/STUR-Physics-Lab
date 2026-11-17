#!/usr/bin/env python3
"""Generic gate for a rebuild campaign (see README.md). The builder runs it in its clean room:

    python3 gate.py builds/<id> --mode builder        # contract, lint, blind checks
and the orchestrator runs it with the hidden oracle:
    python3 gate.py <room>/builds/<id> --mode verifier --campaign <dir> --oracle <dir>/oracle.py

Exit status 0 only if every tier passes. The JSON report (gate_report.json in the build dir) is the evidence.
"""
import argparse, ast, importlib.util, json, math, os, signal, sys, time, traceback

ALWAYS_FORBIDDEN_NAMES = {"open", "exec", "eval", "compile", "__import__", "input"}
FORBIDDEN_MODULES = {"os", "sys", "subprocess", "socket", "urllib", "requests", "importlib", "shutil", "pathlib",
                     "builtins", "ctypes", "pickle", "http", "ftplib", "webbrowser"}
KINDS = ("derived", "input", "quoted")


class Timeout(Exception):
    pass


def _alarm(_s, _f):
    raise Timeout()


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run(label, fn, mod, seconds):
    t0 = time.time()
    signal.signal(signal.SIGALRM, _alarm)
    signal.alarm(seconds)
    try:
        out = fn(mod)
        ok, detail = (out if isinstance(out, tuple) else (bool(out), ""))
    except Timeout:
        ok, detail = False, f"timed out after {seconds} s"
    except Exception as e:                                           # a crash is a failure, with the reason
        ok, detail = False, f"{type(e).__name__}: {e}"
    finally:
        signal.alarm(0)
    return {"label": label, "ok": bool(ok), "detail": str(detail), "seconds": round(time.time() - t0, 2)}


def _fold(node):
    """Value of a constant expression built from numbers, math.pi / pi and + - * / **, else None."""
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)
    if isinstance(node, ast.Attribute) and node.attr == "pi":
        return math.pi
    if isinstance(node, ast.Name) and node.id == "pi":
        return math.pi
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.USub, ast.UAdd)):
        v = _fold(node.operand)
        return None if v is None else (-v if isinstance(node.op, ast.USub) else v)
    if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow)):
        a, b = _fold(node.left), _fold(node.right)
        if a is None or b is None:
            return None
        try:
            return {ast.Add: a + b, ast.Sub: a - b, ast.Mult: a * b, ast.Div: a / b if b else None, ast.Pow: a**b}[type(node.op)]
        except (OverflowError, ZeroDivisionError, ValueError):
            return None
    return None


def lint(path, allowed, targets, exact=()):
    """Imports, forbidden calls, `from inputs import`, and (verifier only) literals that equal an oracle target."""
    src = open(path).read()
    problems = []
    for node in ast.walk(ast.parse(src)):
        if isinstance(node, ast.Import):
            for a in node.names:
                top = a.name.split(".")[0]
                if top in FORBIDDEN_MODULES or top not in allowed:
                    problems.append(f"line {node.lineno}: import {a.name} not allowed")
        elif isinstance(node, ast.ImportFrom):
            top = (node.module or "").split(".")[0]
            if top == "inputs":
                problems.append(f"line {node.lineno}: `from inputs import` (read inputs.NAME inside functions)")
            elif top in FORBIDDEN_MODULES or top not in allowed:
                problems.append(f"line {node.lineno}: from {node.module} import not allowed")
        elif isinstance(node, ast.Name) and node.id in ALWAYS_FORBIDDEN_NAMES:
            problems.append(f"line {node.lineno}: use of {node.id}")
        elif isinstance(node, ast.Constant) and isinstance(node.value, float) and targets:
            v = node.value
            sig = len(repr(v).replace("-", "").replace(".", "").replace("e", "").lstrip("0").rstrip("0"))
            for t in targets:
                if v and t and sig >= 3 and abs(v / t - 1) < 0.01:
                    problems.append(f"line {node.lineno}: literal {v} is within 1% of an oracle target")
    for node in ast.walk(ast.parse(src)):                                 # integer-built constant expressions that equal an oracle target
        if isinstance(node, (ast.BinOp, ast.Constant)) and exact:
            v = _fold(node)
            if v is not None:
                for t in exact:
                    if t and abs(v / t - 1) < 1e-9:
                        problems.append(f"line {node.lineno}: constant expression equals the oracle target {t:.6g}")
    return problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("build")
    ap.add_argument("--mode", choices=("builder", "verifier"), default="builder")
    ap.add_argument("--campaign", default=os.path.dirname(os.path.abspath(__file__)) if False else None)
    ap.add_argument("--oracle", default=None)
    ap.add_argument("--timeout", type=int, default=900)
    a = ap.parse_args()
    here = os.path.dirname(os.path.abspath(__file__))
    camp_dir = a.campaign or here
    camp = load(os.path.join(camp_dir, "campaign.py"), "campaign")
    build = os.path.abspath(a.build)
    sys.path[:0] = [build, camp_dir, here]
    report = {"campaign": camp.NAME, "mode": a.mode, "build": build, "tiers": {}}
    mod_path = os.path.join(build, camp.MODULE + ".py")
    ok_all = True

    # tier 1: contract
    contract = []
    mod = None
    try:
        mod = load(mod_path, camp.MODULE)
        for name in camp.EXPORTS:
            contract.append({"label": f"export {name}", "ok": callable(getattr(mod, name, None)), "detail": ""})
        prov = getattr(mod, "PROVENANCE", None)
        contract.append({"label": "PROVENANCE is a dict covering every export", "ok": isinstance(prov, dict) and set(camp.EXPORTS) <= set(prov), "detail": ""})
        if isinstance(prov, dict):
            for k, v in prov.items():
                good = isinstance(v, tuple) and len(v) == 2 and v[0] in KINDS and (v[0] != "quoted" or k in camp.QUOTED_ALLOWED)
                contract.append({"label": f"PROVENANCE[{k}] valid ({'quoted not allowed' if isinstance(v, tuple) and v[0] == 'quoted' and k not in camp.QUOTED_ALLOWED else 'kind and note'})", "ok": good, "detail": str(v)[:80]})
        contract.append({"label": "DERIVATION.md exists", "ok": os.path.exists(os.path.join(build, "DERIVATION.md")), "detail": ""})
    except Exception as e:
        contract.append({"label": "module imports", "ok": False, "detail": f"{type(e).__name__}: {e}"})
    report["tiers"]["contract"] = contract

    # tier 2: lint
    oracle = None
    targets, exact = [], []
    if a.mode == "verifier" and a.oracle:
        oracle = load(a.oracle, "oracle")
        targets = list(getattr(oracle, "LINT_TARGETS", []))
        exact = list(getattr(oracle, "LINT_EXACT", []))
    problems = lint(mod_path, set(camp.ALLOWED_IMPORTS) | {"inputs"}, targets, exact) if os.path.exists(mod_path) else ["module missing"]
    report["tiers"]["lint"] = [{"label": "lint", "ok": not problems, "detail": "; ".join(problems)}]

    # tier 3: blind checks
    blind = []
    if mod is not None:
        for label, fn in camp.BLIND:
            blind.append(run(label, fn, mod, a.timeout))
    report["tiers"]["blind"] = blind

    # tier 4: oracle (verifier only)
    if a.mode == "verifier":
        if oracle is None:
            raise SystemExit("verifier mode needs --oracle")
        report["tiers"]["oracle"] = [run(label, fn, mod, a.timeout) for label, fn in oracle.ORACLE] if mod is not None else []

    for tier, rows in report["tiers"].items():
        print(f"== {tier}")
        for r in rows:
            print(f"   [{'PASS' if r['ok'] else 'FAIL'}] {r['label']}" + (f"  ({r['detail']})" if r["detail"] and (not r["ok"] or tier == "oracle") else ""))
            ok_all &= r["ok"]
    report["ok"] = ok_all
    json.dump(report, open(os.path.join(build, "gate_report.json"), "w"), indent=1)
    print("GATE PASSED" if ok_all else "GATE FAILED")
    sys.exit(0 if ok_all else 1)


if __name__ == "__main__":
    main()
