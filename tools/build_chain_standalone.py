#!/usr/bin/env python3
"""Write two standard-library-only files that can be pasted into any Python runner:

    src/first_principles_standalone.py   the blind build's ten stages: the calculations alone
    src/chain_first_principles.py        the same stages wired into the force chain, with the fit

    python3 tools/build_chain_standalone.py            # write both
    python3 tools/build_chain_standalone.py --check    # exit 1 if a committed file is stale

Each file is assembled, not hand-written:
  * rebuild/inputs.py, verbatim: the measured inputs, the only numbers typed in;
  * the ten stage modules of an accepted blind build (rebuild/builds/<id>/), verbatim except that
    each is indented into a function (so its names stay private to it), its imports of inputs
    and of earlier stages are dropped (they are the enclosing file's names), and its
    `if __name__ == "__main__":` self-check is removed;
  * a driver, verbatim: tools/stages_driver.py (a report of each stage's results and provenance)
    or tools/chain_driver.py (the chain itself, which calls the stages in order).

tests/test_chain_first_principles.py checks that the committed files are what this tool writes
and that the embedded stages give the same numbers as the build they were copied from.
"""
import ast
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(ROOT, "rebuild"))
import contract  # noqa: E402

BUILD_ID = "2026-11-b"
# Accepted campaign builds embedded in the chain after the ten stages: (module, path, what it is).
# Their top-level helpers that import outside the standard library (a build's own second-route checks)
# are dropped, so the chain stays standard library only; the exports are embedded verbatim.
CAMPAIGN_STAGES = [("induced_g", os.path.join("rebuild", "campaigns", "induced_g", "builds", "a", "induced_g.py"),
                    "campaign induced_g, blind build a (oracle passed, audit pending: rebuild/campaigns/induced_g/)")]
STDLIB_OK = {"math", "cmath", "fractions", "itertools", "functools"}
OUTPUTS = {"chain": ("chain_first_principles.py", "chain_driver.py", "THE CHAIN"),
           "stages": ("first_principles_standalone.py", "stages_driver.py", "THE REPORT")}


def out_path(kind):
    return os.path.join(ROOT, "src", OUTPUTS[kind][0])
RULE = "# " + "=" * 98


def _body_without_main(path, drop_imports, drop_nonstdlib=False):
    """The module's source lines, minus the trailing __main__ block and the named top-level imports
    (and, with drop_nonstdlib, the top-level functions that import outside the standard library)."""
    src = open(path, encoding="utf-8").read()
    tree = ast.parse(src)
    lines = src.split("\n")
    cut = set()
    for node in tree.body:
        is_main = isinstance(node, ast.If) and isinstance(node.test, ast.Compare) and \
            getattr(node.test.left, "id", None) == "__name__"
        if is_main:
            if node is not tree.body[-1]:
                raise SystemExit(f"{path}: the __main__ block is not the last statement")
            cut.update(range(node.lineno - 1, len(lines)))
        elif isinstance(node, ast.Import) and all(a.name in drop_imports and a.asname is None for a in node.names):
            cut.update(range(node.lineno - 1, node.end_lineno))
        elif isinstance(node, ast.FunctionDef) and drop_nonstdlib and any(
            isinstance(n, (ast.Import, ast.ImportFrom)) and
            any((a.name if isinstance(n, ast.Import) else (n.module or "")).split(".")[0] not in STDLIB_OK
                for a in (n.names if isinstance(n, ast.Import) else [n])) for n in ast.walk(node)):
            cut.update(range(node.lineno - 1 - len(node.decorator_list), node.end_lineno))
        elif isinstance(node, ast.ImportFrom) and node.module in drop_imports:
            raise SystemExit(f"{path}: 'from {node.module} import' cannot be embedded")
        elif isinstance(node, ast.Global) or any(isinstance(n, ast.Global) for n in ast.walk(node)):
            raise SystemExit(f"{path}: a 'global' statement cannot be embedded")
    kept = [ln for i, ln in enumerate(lines) if i not in cut]
    while kept and not kept[-1].strip():
        kept.pop()
    return kept


def _wrap(name, lines):
    out = [f"def _load_{name}():"]
    out += [("    " + ln) if ln.strip() else "" for ln in lines]
    out += ["    return _types.SimpleNamespace(**locals())", "", "", f"{name} = _load_{name}()"]
    return out


def render(kind="chain", build_id=BUILD_ID):
    _, driver_name, title = OUTPUTS[kind]
    build = os.path.join(ROOT, "rebuild", "builds", build_id)
    stage_mods = [s["module"] for s in contract.STAGES]
    driver = open(os.path.join(ROOT, "tools", driver_name), encoding="utf-8").read()
    head, _, body = driver.partition("# --- driver body ---\n")
    if not body:
        raise SystemExit(f"tools/{driver_name}: marker '# --- driver body ---' not found")
    doc = ast.get_docstring(ast.parse(head), clean=False)
    out = ["#!/usr/bin/env python3", '"""' + doc.replace("<BUILD_ID>", build_id) + '"""',
           "import math", "import sys", "import types as _types", "from fractions import Fraction", "", ""]
    out += [RULE, "# MEASURED INPUTS (rebuild/inputs.py, verbatim). Change a number here and every stage below",
            "# recomputes from it: nothing downstream is typed in.", RULE]
    out += _wrap("inputs", _body_without_main(os.path.join(ROOT, "rebuild", "inputs.py"), set()))
    for s in contract.STAGES:
        out += ["", "", RULE, f"# STAGE {s['name']}: blind build {build_id}, rebuild/builds/{build_id}/{s['module']}.py",
                "# (its derivation notes: DERIVATION_" + s["name"] + ".md beside it)", RULE]
        out += _wrap(s["module"], _body_without_main(os.path.join(build, s["module"] + ".py"),
                                                     set(stage_mods) | {"inputs"}))
    if kind == "chain":
        for mod, rel_path, what in CAMPAIGN_STAGES:
            out += ["", "", RULE, f"# STAGE {mod}: {what}", f"# {rel_path}; helpers that need numpy (its second route) are left out", RULE]
            out += _wrap(mod, _body_without_main(os.path.join(ROOT, rel_path), set(), drop_nonstdlib=True))
    out += ["", "", RULE, f"# {title} (tools/{driver_name}, verbatim)", RULE, body.rstrip("\n"), ""]
    return "\n".join(out)


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    bad = 0
    for kind in OUTPUTS:
        text, out = render(kind), out_path(kind)
        if "--check" in argv:
            ok = os.path.exists(out) and open(out, encoding="utf-8").read() == text
            print(f"{out}: " + ("up to date" if ok else "STALE: run python3 tools/build_chain_standalone.py"))
            bad += not ok
            continue
        with open(out, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"wrote {out} ({len(text.splitlines())} lines, {len(text) // 1024} kB)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
