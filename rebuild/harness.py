#!/usr/bin/env python3
"""Gatekeeper for an AI rebuild of the symmetry ladder.

    python3 rebuild/harness.py rebuild/builds/<id> --mode builder     # what the builder may run
    python3 rebuild/harness.py rebuild/builds/<id> --mode verifier    # adds the oracle
    python3 rebuild/harness.py rebuild/builds/<a> --compare rebuild/builds/<b>   # two independent builds

Tiers, in order, stage by stage (a stage that fails tiers 1-4b blocks every later stage):
  1 contract     every export exists and is callable; PROVENANCE is complete and honest
  2 lint         standard library + inputs + earlier stages only; no file access, no exec;
                 no literal that looks like a measured or derived number
  3 blind        rebuild/blind/checks.py: identities, limits, two-route consistency, scaling
  4 sensitivity  mutate inputs.py values and require each output to move as physics says
                 (catches answers typed in or cached at import time)
  4b connections every link in contract.CONNECTIONS is a real call: the downstream rung
                 must use the upstream rung's function, not a private recomputation
  5 oracle       (verifier mode) differential comparison with src/ladder_standalone.py
  6 crossbuild   (with --compare) two independent builds must agree on a probe set

Writes a JSON report and prints a summary; exits 1 if anything fails.
"""
import argparse
import ast
import datetime
import importlib.util
import json
import os
import sys
from decimal import Decimal
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import contract  # noqa: E402
import inputs    # noqa: E402
from blind import checks as blind_checks  # noqa: E402

STDLIB_ALLOWED = {"math", "cmath", "fractions", "itertools", "functools", "random", "operator",
                  "typing", "dataclasses", "collections", "decimal", "numbers", "statistics"}
FORBIDDEN_CALLS = {"open", "exec", "eval", "compile", "__import__", "globals", "breakpoint", "input"}
FORBIDDEN_STRINGS = ("ladder_standalone", "src/", "src\\", "oracle", "_selftest")
KINDS = ("derived", "input", "quoted")
MAX_INT = 10000


# ------------------------------------------------------------------------------------------
# loading
# ------------------------------------------------------------------------------------------
def load_build(build_dir, stages):
    """Import a build's stage modules in order, fresh, with only rebuild/ and the build on the path."""
    build_dir = os.path.abspath(build_dir)
    unload(build_dir)
    if build_dir not in sys.path:
        sys.path.insert(0, build_dir)
    mods, errors = {}, {}
    for s in stages:
        path = os.path.join(build_dir, s["module"] + ".py")
        if not os.path.exists(path):
            errors[s["name"]] = f"missing file {s['module']}.py"
            break
        try:
            spec = importlib.util.spec_from_file_location(s["module"], path)
            mod = importlib.util.module_from_spec(spec)
            sys.modules[s["module"]] = mod
            spec.loader.exec_module(mod)
            mods[s["module"]] = mod
        except Exception as e:
            errors[s["name"]] = f"import failed: {type(e).__name__}: {e}"
            break
    sys.path.remove(build_dir)
    return mods, errors


def unload(build_dir):
    """Forget the stage modules and any helper module loaded from a build directory, so two
    builds with a same-named helper (or a re-run after an edit) never share cached code."""
    for s in contract.STAGES:
        sys.modules.pop(s["module"], None)
    builds_root = os.path.abspath(os.path.join(HERE, "builds"))
    for name, mod in list(sys.modules.items()):
        f = os.path.abspath(getattr(mod, "__file__", None) or os.devnull)
        if f.startswith(os.path.abspath(build_dir) + os.sep) or f.startswith(builds_root + os.sep) \
                or os.sep + "_selftest" + os.sep in f:
            sys.modules.pop(name, None)


# ------------------------------------------------------------------------------------------
# tier 1: contract
# ------------------------------------------------------------------------------------------
def tier_contract(stage, mod):
    out = []
    for name in stage["exports"]:
        out.append((f"export {name}", callable(getattr(mod, name, None)), "missing or not callable"
                    if not callable(getattr(mod, name, None)) else ""))
    prov = getattr(mod, "PROVENANCE", None)
    if not isinstance(prov, dict):
        return out + [("PROVENANCE dict present", False, "module must define PROVENANCE = {export: (kind, note)}")]
    missing = [n for n in stage["exports"] if n not in prov]
    out.append(("PROVENANCE covers every export", not missing, f"missing {missing}" if missing else ""))
    for n, v in prov.items():
        ok = isinstance(v, tuple) and len(v) == 2 and v[0] in KINDS and isinstance(v[1], str) and v[1].strip()
        if not ok:
            out.append((f"PROVENANCE[{n}] well formed", False, f"{v!r}: need (kind in {KINDS}, non-empty note)"))
            continue
        if v[0] == "quoted" and n not in stage["quoted_allowed"]:
            out.append((f"PROVENANCE[{n}] quoted only where allowed", False,
                        f"{n} must be derived in this stage; quoted allowed only for {stage['quoted_allowed']}"))
    return out


# ------------------------------------------------------------------------------------------
# tier 2: lint
# ------------------------------------------------------------------------------------------
def _sig_digits(x):
    if x == 0:
        return 0
    d = Decimal(repr(float(x))).normalize()
    return len(d.as_tuple().digits)


def _input_values():
    vals = set()
    def add(v):
        if isinstance(v, (int, float)) and not isinstance(v, bool) and v != 0 and _sig_digits(v) >= 2:
            vals.add(float(v))
        elif isinstance(v, (tuple, list)):
            for x in v:
                add(x)
        elif isinstance(v, dict):
            for x in v.values():
                add(x)
    for k in dir(inputs):
        if k.isupper():
            add(getattr(inputs, k))
    return vals


def tier_lint(stage, path):
    earlier = {s["module"] for s in contract.STAGES[: contract.STAGE_NAMES.index(stage["name"])]}
    src = open(path, encoding="utf-8").read()
    try:
        tree = ast.parse(src)
    except SyntaxError as e:
        return [("parses", False, str(e))]
    inv = _input_values()
    bad_imp, bad_call, bad_str, bad_num = [], [], [], []
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            names = [a.name for a in node.names] if isinstance(node, ast.Import) else [node.module or ""]
            if isinstance(node, ast.ImportFrom) and node.level:
                bad_imp.append(f"relative import line {node.lineno}")
            for nm in names:
                top = nm.split(".")[0]
                if top in STDLIB_ALLOWED or top == "inputs" or top in earlier:
                    continue
                if top == "rebuild" and nm in ("rebuild", "rebuild.inputs"):
                    continue
                bad_imp.append(f"{nm} (line {node.lineno})")
            if isinstance(node, ast.ImportFrom) and (node.module or "").split(".")[0] in earlier:
                bad_imp.append(f"'from {node.module} import ...' at line {node.lineno}: use 'import {node.module}' and"
                               f" call {node.module}.<function>() so the connections tier can see the call")
            if isinstance(node, ast.ImportFrom) and (node.module or "").split(".")[-1] == "inputs":
                bad_imp.append(f"'from inputs import ...' at line {node.lineno}: use 'import inputs' and read"
                               " inputs.NAME inside functions, so the sensitivity tier can mutate them")
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in FORBIDDEN_CALLS:
            bad_call.append(f"{node.func.id}() line {node.lineno}")
        elif isinstance(node, ast.Constant):
            v = node.value
            if isinstance(v, str):
                if any(s in v for s in FORBIDDEN_STRINGS):
                    bad_str.append(f"line {node.lineno}: {v[:40]!r}")
            elif isinstance(v, bool):
                pass
            elif isinstance(v, int):
                if abs(v) > MAX_INT and str(abs(v)).rstrip("0") != "1":
                    bad_num.append(f"{v} (line {node.lineno}): integer above {MAX_INT}")
                elif abs(v) >= 100 and float(v) in inv:
                    bad_num.append(f"{v} (line {node.lineno}): equals a value in inputs.py")
            elif isinstance(v, float):
                if _sig_digits(v) >= 3:
                    bad_num.append(f"{v!r} (line {node.lineno}): {_sig_digits(v)} significant digits")
                elif any(abs(v - x) <= 1e-12 * abs(x) for x in inv):
                    bad_num.append(f"{v!r} (line {node.lineno}): equals a value in inputs.py")
    return [("imports: standard library, inputs, earlier stages only", not bad_imp, "; ".join(bad_imp)),
            ("no file access, exec or eval", not bad_call, "; ".join(bad_call)),
            ("no reference to the oracle or src/", not bad_str, "; ".join(bad_str)),
            ("no typed-in physical numbers (take them from inputs.py or compute them)", not bad_num,
             "; ".join(bad_num[:12]) + (f" ... ({len(bad_num)} total)" if len(bad_num) > 12 else ""))]


# ------------------------------------------------------------------------------------------
# tier 4: sensitivity (mutate inputs; outputs must respond)
# ------------------------------------------------------------------------------------------
class mutated:
    def __init__(self, **kw):
        self.kw, self.old = kw, {}

    def __enter__(self):
        for k, v in self.kw.items():
            self.old[k] = getattr(inputs, k)
            setattr(inputs, k, v)

    def __exit__(self, *a):
        for k, v in self.old.items():
            setattr(inputs, k, v)


def _rel(a, b):
    return abs(a - b) / max(abs(b), 1e-300)


def _sens(label, fn):
    try:
        ok, detail = fn()
    except Exception as e:
        ok, detail = False, f"raised {type(e).__name__}: {e}"
    return (label, bool(ok), detail)


def tier_sensitivity(name, m):
    out = []
    if name == "casimir":
        P = m["casimir"]
        def rad():
            a = P.diamond_radius(1e-14)
            with mutated(RHO_DIAMOND=8 * inputs.RHO_DIAMOND):
                b = P.diamond_radius(1e-14)
            return _rel(a / b, 2) < 1e-12, f"R ~ rho^(-1/3): {a:.4e} -> {b:.4e}"
        def gap_eps():
            a = P.casimir_safe_gap(1e-14, 250e-6, 2.5, 0.1)
            with mutated(EPS_DIAMOND=3.0):
                b = P.casimir_safe_gap(1e-14, 250e-6, 2.5, 0.1)
            return b < a, f"lower permittivity, smaller gap: {a:.4e} -> {b:.4e}"
        def cp_hbar():
            a = P.cp_energy(1e-6, 1e-6, 0.6, 0.6, 1e-4)
            with mutated(HBAR=2 * inputs.HBAR):
                b = P.cp_energy(1e-6, 1e-6, 0.6, 0.6, 1e-4)
            return _rel(b / a, 2) < 1e-12, "U ~ hbar"
        out += [_sens("diamond radius reads RHO_DIAMOND", rad), _sens("safe gap reads EPS_DIAMOND", gap_eps),
                _sens("Casimir-Polder energy ~ hbar", cp_hbar)]
    elif name == "graviton":
        Gr = m["graviton"]
        def hb():
            a = Gr.entangling_phase(1e-14, 5e-4, 0.1, 1.0, 2e-4)
            with mutated(HBAR=2 * inputs.HBAR):
                b = Gr.entangling_phase(1e-14, 5e-4, 0.1, 1.0, 2e-4)
            return _rel(a / b, 2) < 1e-12, "phase ~ 1/hbar"
        out.append(_sens("entangling phase ~ 1/hbar", hb))
    elif name == "desitter":
        D = m["desitter"]
        def ell_scaling():
            a, b = D.ell_from_lambda(1e-52), D.ell_from_lambda(4e-52)
            return _rel(a / b, 2) < 1e-12, f"ell(L)/ell(4L) = {a / b}"
        out.append(_sens("ell ~ Lambda^-1/2, not a constant", ell_scaling))
    elif name == "blackholes":
        B = m["blackholes"]
        def nar():
            a = B.nariai_mass_kg(1e-52)
            with mutated(G_NEWTON=2 * inputs.G_NEWTON):
                b = B.nariai_mass_kg(1e-52)
            return _rel(a / b, 2) < 1e-12, "M_Nariai ~ 1/G"
        def hk():
            a = B.hawking_K(1e3)
            with mutated(HBAR=2 * inputs.HBAR, K_B=4 * inputs.K_B):
                b = B.hawking_K(1e3)
            return _rel(b / a, 0.5) < 1e-12, "T_H ~ hbar / k_B"
        def sh():
            a = B.shadow_uas(1e6, 8000.0)
            with mutated(GM_SUN=3 * inputs.GM_SUN):
                b = B.shadow_uas(1e6, 8000.0)
            return _rel(b / a, 3) < 1e-12, "shadow ~ GM_sun"
        out += [_sens("Nariai mass reads G", nar), _sens("Hawking temperature reads hbar, k_B", hk),
                _sens("shadow reads GM_SUN", sh)]
    elif name == "links":
        Lk = m["links"]
        def neu():
            a = Lk.neutrality_per_nucleon(1e-14)
            with mutated(G_NEWTON=4 * inputs.G_NEWTON):
                b = Lk.neutrality_per_nucleon(1e-14)
            with mutated(GAP_FRACTION=4 * inputs.GAP_FRACTION):
                c = Lk.neutrality_per_nucleon(1e-14)
            return _rel(b / a, 2) < 1e-12 and _rel(c / a, 2) < 1e-12, "~ sqrt(fraction G)"
        def rs():
            a = Lk.schwarzschild_radius(1.0)
            with mutated(C_LIGHT=2 * inputs.C_LIGHT):
                b = Lk.schwarzschild_radius(1.0)
            return _rel(a / b, 4) < 1e-12, "r_s ~ 1/c^2"
        out += [_sens("neutrality reads G and the fraction", neu), _sens("Schwarzschild radius reads c", rs)]
    return out


# ------------------------------------------------------------------------------------------
# tier 5: connections (the rungs must actually use each other)
# ------------------------------------------------------------------------------------------
def tier_connections(name, mods):
    out = []
    for c in contract.CONNECTIONS:
        dstage, dfn, args = c["down"]
        if dstage != name:
            continue
        label = f"{c['id']}: {dstage}.{dfn} uses " + ", ".join(f"{u}.{f}" for u, f in c["up"])
        calls, saved = {}, []
        try:
            for ust, ufn in c["up"]:
                mod = mods[contract.stage(ust)["module"]]
                orig = getattr(mod, ufn)
                key = f"{ust}.{ufn}"
                calls[key] = 0
                def spy(*a, _orig=orig, _key=key, **k):
                    calls[_key] += 1
                    return _orig(*a, **k)
                saved.append((mod, ufn, orig))
                setattr(mod, ufn, spy)
            getattr(mods[contract.stage(dstage)["module"]], dfn)(*args)
            unused = [k for k, n in calls.items() if n == 0]
            out.append((label, not unused, f"never called: {unused} ({c['why']})" if unused else c["why"]))
        except Exception as e:
            out.append((label, False, f"raised {type(e).__name__}: {e}"))
        finally:
            for mod, ufn, orig in saved:
                setattr(mod, ufn, orig)
    return out


# ------------------------------------------------------------------------------------------
# tier 6: crossbuild probes
# ------------------------------------------------------------------------------------------
PROBES = [
    ("gauge331", "mass_matrix", ("+1/sqrt3", 0.61, 0.83, 5200.0, 120.0, 201.0)),
    ("gauge331", "neutral_masses", ("-1/sqrt3", 0.61, 0.83, 5200.0, 120.0, 201.0)),
    ("gauge331", "quark_charges", (5,)),
    ("chiral", "chpt_mpi", (inputs.M_UD_FLAG, inputs.COND_13, inputs.FPI_OVER_F, inputs.LBAR3, inputs.F_PI)),
    ("chiral", "sigma_model_vacuum", (1.7, 0.9, 0.03)),
    ("casimir", "cp_integral", ()),
    ("casimir", "casimir_safe_gap", (1e-14, 250e-6, 2.5, 0.1)),
    ("graviton", "entangling_phase", (inputs.DESIGN_A_MASS, inputs.DESIGN_A_DX, inputs.DESIGN_A_HOLD,
                                      inputs.DESIGN_A_RAMP, 2.0e-4)),
    ("desitter", "action_coefficients", (0.2, 5.0, [0.0, 1.9, 0.8, 0.3])),
    ("desitter", "ricci_scalar", (0.2, 5.0, [0.0, 1.9, 0.8, 0.3])),
    ("blackholes", "sds_horizons", (1.0, 7.0)),
    ("blackholes", "isco", ()),
    ("blackholes", "kerr_first_law", (Fraction(7, 2), Fraction(3, 5), 1, 1)),
    ("links", "pi0_width_eV", (inputs.ALPHA_0, inputs.F_PI, inputs.M_PI0, 3, Fraction(2, 3), Fraction(-1, 3))),
    ("graviton", "design_phase", ()),
    ("blackholes", "kappa_from_spin_connection", (1.0, 9.0)),
    ("links", "matter_charges", (5, "+1/sqrt3")),
    ("links", "planck_bh_kT_GeV", ()),
]


def _flat(x):
    if isinstance(x, (list, tuple)):
        return [y for e in x for y in _flat(e)]
    if isinstance(x, (set, frozenset)):
        return sorted(_flat(list(x)))
    return [x]


def probe_values(build_dir):
    mods, _ = load_build(build_dir, contract.STAGES)
    vals = {}
    for st, fn, args in PROBES:
        mod = mods.get(contract.stage(st)["module"])
        try:
            vals[f"{st}.{fn}"] = _flat(getattr(mod, fn)(*args))
        except Exception as e:
            vals[f"{st}.{fn}"] = f"error {type(e).__name__}: {e}"
    unload(build_dir)
    return vals


def tier_crossbuild(a_dir, b_dir, rtol=1e-8):
    A, B = probe_values(a_dir), probe_values(b_dir)
    out = []
    for k in A:
        x, y = A[k], B[k]
        if isinstance(x, str) or isinstance(y, str) or len(x) != len(y):
            out.append((k, False, f"{x!r} vs {y!r}"))
            continue
        worst = max((abs(float(p) - float(q)) / max(abs(float(q)), 1e-300) if q != 0 else abs(float(p))
                     for p, q in zip(x, y)), default=0.0)
        out.append((k, worst <= rtol, f"max rel diff {worst:.2e}"))
    return out


# ------------------------------------------------------------------------------------------
def run(build_dir, mode="builder", upto=None, compare=None, lint=True, modules=None):
    stages = contract.upto(upto) if upto else contract.STAGES
    report = {"build": os.path.abspath(build_dir), "mode": mode, "time": datetime.datetime.now().isoformat(),
              "stages": {}, "crossbuild": None}
    mods, errors = (modules, {}) if modules is not None else load_build(build_dir, stages)
    reference = None
    if mode == "verifier":
        try:
            import oracle
        except ImportError:
            raise SystemExit("verifier mode needs rebuild/oracle.py: run it in the repository, not in a clean room")
        reference = oracle.load_reference()
    blocked = None
    for s in stages:
        name, rec = s["name"], {}
        report["stages"][name] = rec
        if blocked:
            rec["status"] = f"blocked by {blocked}"
            continue
        if name in errors or s["module"] not in mods:
            rec["status"] = "fail"
            rec["load"] = errors.get(name, "not loaded")
            blocked = name
            continue
        mod = mods[s["module"]]
        rec["contract"] = tier_contract(s, mod)
        if lint:
            rec["lint"] = tier_lint(s, os.path.join(build_dir, s["module"] + ".py"))
        if all(ok for _, ok, _ in rec["contract"]):
            rec["blind"] = blind_checks.BY_STAGE[name](mods)
            rec["sensitivity"] = tier_sensitivity(name, mods)
            rec["connections"] = tier_connections(name, mods)
            if reference is not None:
                import oracle
                rec["oracle"] = oracle.BY_STAGE[name](mods, reference)
        gate = [r for t in ("contract", "lint", "blind", "sensitivity", "connections") for r in rec.get(t, [])]
        rec["status"] = "pass" if all(ok for _, ok, _ in gate) and all(ok for _, ok, _ in rec.get("oracle", [])) else "fail"
        if not all(ok for _, ok, _ in gate):
            blocked = name
    if compare:
        report["crossbuild"] = tier_crossbuild(build_dir, compare)
    if modules is None:
        unload(build_dir)
    report["ok"] = all(r.get("status") == "pass" for r in report["stages"].values()) and \
        all(ok for _, ok, _ in (report["crossbuild"] or []))
    return report


def ledger(build_dir):
    """Markdown table of every export's provenance: what the build claims it derived,
    read or quoted. The auditor checks each claim against the code and DERIVATION notes."""
    mods, errors = load_build(build_dir, contract.STAGES)
    rows = ["| Stage | Export | Kind | Note |", "|---|---|---|---|"]
    counts = {k: 0 for k in KINDS}
    for s in contract.STAGES:
        mod = mods.get(s["module"])
        prov = getattr(mod, "PROVENANCE", {}) if mod else {}
        for n in s["exports"]:
            kind, note = prov.get(n, ("MISSING", errors.get(s["name"], "")))
            counts[kind] = counts.get(kind, 0) + 1
            rows.append(f"| {s['name']} | `{n}` | {kind} | {note} |")
    unload(build_dir)
    head = ", ".join(f"{v} {k}" for k, v in counts.items())
    return f"# Provenance ledger: {os.path.basename(os.path.abspath(build_dir))}\n\n{head}\n\n" + "\n".join(rows) + "\n"


def summarize(report):
    lines = [f"Build {report['build']}  (mode: {report['mode']})"]
    for name, rec in report["stages"].items():
        lines.append(f"\n[{rec.get('status', '?').upper():>4}] {name}")
        if "load" in rec:
            lines.append(f"       load: {rec['load']}")
        for tier in ("contract", "lint", "blind", "sensitivity", "connections", "oracle"):
            res = rec.get(tier)
            if not res:
                continue
            n_ok = sum(ok for _, ok, _ in res)
            lines.append(f"       {tier:<11} {n_ok}/{len(res)}")
            for label, ok, detail in res:
                if not ok:
                    lines.append(f"         FAIL {label}: {detail}")
    if report["crossbuild"] is not None:
        res = report["crossbuild"]
        lines.append(f"\ncrossbuild {sum(ok for _, ok, _ in res)}/{len(res)}")
        lines += [f"  FAIL {l}: {d}" for l, ok, d in res if not ok]
    lines.append("\nRESULT: " + ("ALL GATES PASS" if report["ok"] else "FAILURES (see above)"))
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("build_dir")
    ap.add_argument("--mode", choices=("builder", "verifier"), default="builder")
    ap.add_argument("--stage", choices=contract.STAGE_NAMES, help="run stages up to and including this one")
    ap.add_argument("--compare", help="a second, independent build directory")
    ap.add_argument("--report", help="JSON report path (default rebuild/reports/<build>-<mode>.json)")
    ap.add_argument("--ledger", action="store_true", help="also write <build>/LEDGER.md")
    args = ap.parse_args(argv)
    if args.ledger:
        with open(os.path.join(args.build_dir, "LEDGER.md"), "w") as fh:
            fh.write(ledger(args.build_dir))
    rep = run(args.build_dir, args.mode, args.stage, args.compare)
    path = args.report or os.path.join(HERE, "reports", f"{os.path.basename(os.path.abspath(args.build_dir))}-{args.mode}.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as fh:
        json.dump(rep, fh, indent=1, default=str)
    print(summarize(rep))
    print(f"\nreport: {path}")
    return 0 if rep["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
