#!/usr/bin/env python3
"""Export a clean room for one campaign and build id, OUTSIDE the repository:

    python3 export_room.py <campaign> <build_id> <room_dir>

The room holds gate.py, campaign.py (contract and blind checks), SPEC.md, BUILDER.md and an empty
builds/<build_id>/. It never holds oracle.py, the repository's src/, tests/ or any result.
"""
import os, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
campaign, build_id, room = sys.argv[1:4]
src = os.path.join(HERE, campaign)
assert os.path.isdir(src), campaign
room = os.path.abspath(room)
assert not room.startswith(os.path.abspath(os.path.join(HERE, "..", "..")) + os.sep), "room must be outside the repository"
os.makedirs(os.path.join(room, "builds", build_id), exist_ok=True)
os.makedirs(os.path.join(room, "tmp"), exist_ok=True)           # scratch files go here, not in the shared session scratchpad
for name, dest in (("gate.py", "gate.py"), (os.path.join(campaign, "campaign.py"), "campaign.py"),
                   (os.path.join(campaign, "SPEC.md"), "SPEC.md"), ("BUILDER.md", "BUILDER.md")):
    shutil.copy(os.path.join(HERE, name), os.path.join(room, dest))
open(os.path.join(room, "inputs.py"), "w").write('"""No measured inputs in this campaign: units and constants are in SPEC.md."""\n')
bad = [n for n in os.listdir(room) if n in ("oracle.py", "src", "tests", "results")]
assert not bad, bad
print("room ready:", room)
