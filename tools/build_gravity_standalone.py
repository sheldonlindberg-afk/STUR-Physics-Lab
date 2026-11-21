#!/usr/bin/env python3
"""Write src/gravity_from_331.py: gravity from the 3-3-1 gauge theory, one standard-library file to paste anywhere.

    python3 tools/build_gravity_standalone.py            # write it
    python3 tools/build_gravity_standalone.py --check    # exit 1 if the committed file is stale

Assembled, not hand-written, with the same embedding as tools/build_chain_standalone.py:
  * rebuild/inputs.py, verbatim;
  * the blind build's stages toolkit, gauge331 and running (rebuild/builds/2026-11-b/);
  * the accepted build a of campaign induced_g, minus its numpy-only second-route helpers;
  * src/m331_gravigut_nogo.py, the no-go (its loader is called by the driver, which hands it the stages);
  * the driver, tools/gravity_driver.py.
Pinned by tests/test_gravity_standalone.py.
"""
import ast
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_chain_standalone as B  # noqa: E402

ROOT = B.ROOT
OUT = os.path.join(ROOT, "src", "gravity_from_331.py")
STAGES = ("toolkit", "gauge331", "running")


def render():
    driver = open(os.path.join(HERE, "gravity_driver.py"), encoding="utf-8").read()
    head, _, body = driver.partition("# --- driver body ---\n")
    doc = ast.get_docstring(ast.parse(head), clean=False)
    out = ["#!/usr/bin/env python3", '"""' + doc + '"""',
           "import math", "import sys", "import types as _types", "from fractions import Fraction", "", ""]
    out += [B.RULE, "# MEASURED INPUTS (rebuild/inputs.py, verbatim)", B.RULE]
    out += B._wrap("inputs", B._body_without_main(os.path.join(ROOT, "rebuild", "inputs.py"), set()))
    build = os.path.join(ROOT, "rebuild", "builds", B.BUILD_ID)
    for s in STAGES:
        out += ["", "", B.RULE, f"# STAGE {s}: blind build {B.BUILD_ID}, rebuild/builds/{B.BUILD_ID}/{s}.py", B.RULE]
        out += B._wrap(s, B._body_without_main(os.path.join(build, s + ".py"), set(STAGES) | {"inputs"}))
    for mod, rel_path, what in B.CAMPAIGN_STAGES:
        out += ["", "", B.RULE, f"# STAGE {mod}: {what}", f"# {rel_path}; helpers that need numpy (its second route) are left out", B.RULE]
        out += B._wrap(mod, B._body_without_main(os.path.join(ROOT, rel_path), set(), drop_nonstdlib=True))
    out += ["", "", B.RULE, "# THE NO-GO: src/m331_gravigut_nogo.py, verbatim (loaded by the driver, which hands it the stages)", B.RULE]
    out += B._wrap("nogo", B._body_without_main(os.path.join(ROOT, "src", "m331_gravigut_nogo.py"), set()))[:-1]
    out += ["", "", B.RULE, "# THE STORY (tools/gravity_driver.py, verbatim)", B.RULE, body.rstrip("\n"), ""]
    return "\n".join(out)


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    text = render()
    if "--check" in argv:
        ok = os.path.exists(OUT) and open(OUT, encoding="utf-8").read() == text
        print(f"{OUT}: " + ("up to date" if ok else "STALE: run python3 tools/build_gravity_standalone.py"))
        return 0 if ok else 1
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"wrote {OUT} ({len(text.splitlines())} lines, {len(text) // 1024} kB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
