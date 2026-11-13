#!/usr/bin/env python3
"""Make, and bring back from, a clean room: a directory where a builder AI can work with
no way to read the answers.

    python3 rebuild/cleanroom.py export <dest> <build_id>    # make the clean room
    python3 rebuild/cleanroom.py import <dest> <build_id>    # copy the finished build back

The clean room holds exactly what a builder may see:
    SPEC.md  contract.py  inputs.py  harness.py  blind/  prompts/builder.md
    builds/<build_id>/            (the build so far, if any)
It does NOT hold src/, tests/, results/, the repository's .md pages, oracle.py or
_selftest/. The harness runs there in builder mode; verifier mode needs oracle.py and fails.

Run the builder with its working directory set to <dest>, ideally on a fresh checkout
or machine with only <dest> visible (rebuild/PROTOCOL.md, "Isolation levels").
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ALLOWED = ["SPEC.md", "contract.py", "inputs.py", "harness.py", "blind", os.path.join("prompts", "builder.md")]
FORBIDDEN_IN_ROOM = ["oracle.py", "_selftest", "src", "tests", "results"]


def export(dest, build_id):
    dest = os.path.abspath(dest)
    repo = os.path.abspath(os.path.join(HERE, ".."))
    if os.path.commonpath([dest, repo]) == repo:
        raise SystemExit("the clean room must be OUTSIDE the repository, or the builder can walk up into src/")
    os.makedirs(dest, exist_ok=True)
    for rel in ALLOWED:
        s, d = os.path.join(HERE, rel), os.path.join(dest, rel)
        os.makedirs(os.path.dirname(d), exist_ok=True)
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__"))
        else:
            shutil.copy2(s, d)
    src_build = os.path.join(HERE, "builds", build_id)
    dst_build = os.path.join(dest, "builds", build_id)
    if os.path.isdir(src_build):
        shutil.copytree(src_build, dst_build, dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__"))
    os.makedirs(dst_build, exist_ok=True)
    for bad in FORBIDDEN_IN_ROOM:
        assert not os.path.exists(os.path.join(dest, bad)), bad
    print(f"clean room ready: {dest}\n  build dir: {dst_build}\n"
          f"  builder runs: python3 harness.py builds/{build_id} --mode builder --stage <stage>")


def import_back(dest, build_id):
    s = os.path.join(os.path.abspath(dest), "builds", build_id)
    d = os.path.join(HERE, "builds", build_id)
    if not os.path.isdir(s):
        raise SystemExit(f"no build at {s}")
    shutil.copytree(s, d, dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__", "*.json"))
    print(f"imported {s} -> {d}")


if __name__ == "__main__":
    if len(sys.argv) != 4 or sys.argv[1] not in ("export", "import"):
        raise SystemExit(__doc__)
    (export if sys.argv[1] == "export" else import_back)(sys.argv[2], sys.argv[3])
