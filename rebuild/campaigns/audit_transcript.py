#!/usr/bin/env python3
"""Evidence of isolation after the fact: scan a builder's transcript (JSONL of one subagent) for any tool call that reaches outside its clean room.

    python3 audit_transcript.py <transcript.jsonl> <room_dir> [--canary TOKEN ...] [--allow PREFIX ...]

A path outside the room is allowed only if this same transcript created it (a redirect, tee, -o, open(..., "w"), cp or the Write tool),
so the builder may use scratch files wherever it likes but may not READ anything it did not make.
Flags (exit status 1 if any):
  * a web, delegation or MCP tool used at all (the harness's own report-and-wait tools are allowed);
  * a Read/Write/Edit/Glob/Grep path, or an absolute path found in a Bash command, outside the room and the allowed system prefixes;
  * a relative path that escapes the room (`..`) or a `cd` to somewhere else;
  * any canary token, planted in the repository or the scratchpad outside the rooms, appearing anywhere in the transcript.
This turns "the builder was told not to look" into a checkable record: the transcript is the record of every call it made.
It cannot see what the process could have read through a library call that is not a tool call, which is why a fresh machine
(PROTOCOL.md section 3, level 3) remains the stronger isolation.
"""
import json, os, re, sys

DENIED_TOOLS = {"WebFetch", "WebSearch", "Agent", "Skill", "ReadMcpResourceTool", "ListMcpResourcesTool"}      # data from outside, or delegation
HARNESS_PLUMBING = ("SubagentHandback", "Monitor", "TaskStop", "TaskOutput", "ToolSearch", "SendMessage")     # report and wait; no data access
DEFAULT_ALLOW = ("/usr/", "/opt/", "/bin/", "/lib", "/etc/alternatives", "/dev/null", "/proc/self", "/sys/devices/system/cpu")
TOP = set(os.listdir("/"))                       # a token is a path only if its first component is a real top-level directory
PATH_RE = re.compile(r"(?<![\w.\-])(/(?:[\w.\-+@%~]+/?)+)")


def tool_calls(path):
    for line in open(path):
        try:
            d = json.loads(line)
        except Exception:
            continue
        m = d.get("message")
        c = m.get("content") if isinstance(m, dict) else None
        if isinstance(c, list):
            for x in c:
                if isinstance(x, dict) and x.get("type") == "tool_use":
                    yield x.get("name"), x.get("input", {}), d.get("timestamp"), d.get("cwd")


WRITE_PATTERNS = (r">>?\s*{p}", r"\btee\s+(?:-a\s+)?{p}", r"\s-o\s+{p}", r"open\(\s*['\"]{p}['\"]\s*,\s*['\"][wax]", r"\bcp\s+\S+\s+{p}", r"\bmkdir\s+(?:-p\s+)?{p}", r"cProfile\.run\([^\n]*?,\s*['\"]{p}['\"]", r"dump_stats\(\s*['\"]{p}['\"]")


def writes(cmd, p):
    """True if the command creates or writes the path p (redirect, tee, -o, open(..., 'w'), cp to, mkdir)."""
    return any(re.search(pat.format(p=re.escape(p)), cmd) for pat in WRITE_PATTERNS)


HEREDOC = re.compile(r"<<-?\s*['\"]?(\w+)['\"]?[^\n]*\n.*?\n\s*\1(?=\n|$)", re.S)
PATHLIKE = re.compile(r"^[\w.\-+/@%~]+$")


def relative_violations(cmd, cwd, room, allow, created):
    """Follow `cd` through the command from the starting directory and resolve every space-free relative path-like token against it.
    Heredoc bodies are removed first (their text is data, not arguments; absolute paths in them are still caught by the caller)."""
    import shlex
    out = []
    body = HEREDOC.sub("", cmd)
    cwd = os.path.normpath(cwd)
    for stmt in re.split(r"&&|\|\||[;\n|()&]", body):
        stmt = stmt.strip()
        if not stmt:
            continue
        try:
            toks = shlex.split(stmt)
        except ValueError:
            toks = stmt.split()
        if not toks:
            continue
        if toks[0] == "cd":
            target = toks[1] if len(toks) > 1 else "/root"
            cwd = os.path.normpath(target if target.startswith("/") else os.path.join(cwd, target))
            if not inside(cwd, room) and not any(cwd.startswith(a) for a in allow):
                out.append(("cd leaves the room", f"cd {target} -> {cwd}"))
            continue
        cmdname = os.path.basename(toks[0])
        args = toks[1:]
        nonopt = [t for t in args if not t.startswith("-")]
        implicit_cwd = (cmdname in ("ls", "find", "tree", "du", "dir") and not [t for t in nonopt if not t.startswith("(")]) or \
                       (cmdname in ("grep", "egrep", "fgrep", "rg") and any(t in ("-r", "-R", "--recursive", "-rn", "-rl", "-ri", "-rI") or re.fullmatch(r"-[A-Za-z]*[rR][A-Za-z]*", t) for t in args) and len(nonopt) <= 1)
        if implicit_cwd and not inside(cwd, room) and not any(cwd.startswith(a) for a in allow):
            out.append(("default-directory search outside the room", f"{cmdname} with no path from {cwd}"))
        if cmdname in ("pgrep", "pkill"):
            args = []                                              # their only non-option argument is a process-name pattern
        elif cmdname in ("grep", "egrep", "fgrep", "rg") and nonopt:
            args = [t for t in args if t != nonopt[0] or t.startswith("-")]      # drop the pattern, keep the file arguments
        for t in args:
            if t.startswith(("-", "/", "$", "'", '"')) or "=" in t or not PATHLIKE.match(t):
                continue
            if not ("/" in t or t in (".", "..") or re.search(r"\.[A-Za-z0-9]{1,5}$", t)):
                continue
            if t not in (".", "..") and re.fullmatch(r"[\d./]+", t):      # arithmetic such as 1/2 or 3.5 (a bare . or .. is a directory)
                continue
            rp = os.path.normpath(os.path.join(cwd, t))
            if rp in created or inside(rp, room) or any(rp.startswith(a) for a in allow):
                continue
            out.append(("relative path resolves outside the room", f"{t} from {cwd} -> {rp}"))
    return out


def inside(p, root):
    p = os.path.normpath(p)
    return p == root or p.startswith(root + os.sep)


def check(path, room, canaries=(), allow=()):
    room = os.path.realpath(room)
    allow = tuple(DEFAULT_ALLOW) + tuple(allow)
    flags, counts, created = [], {}, set()
    for name, inp, ts, cwd0 in tool_calls(path):
        counts[name] = counts.get(name, 0) + 1
        if name in DENIED_TOOLS or (name or "").startswith("mcp__"):
            flags.append((ts, name, "tool not allowed in a clean room", json.dumps(inp)[:160]))
            continue
        if name in HARNESS_PLUMBING:
            continue
        paths = []
        for key in ("file_path", "path", "notebook_path"):
            if isinstance(inp.get(key), str):
                paths.append(inp[key])
        cmd = inp.get("command") if isinstance(inp.get("command"), str) else ""
        for p in PATH_RE.findall(cmd):
            p = p.rstrip("/")
            if p.split("/")[1] in TOP:
                paths.append(p)
        if name == "Write" and isinstance(inp.get("file_path"), str):
            created.add(os.path.normpath(inp["file_path"]))
        for p in paths:
            if p.startswith("/") and (os.path.normpath(p) in created or writes(cmd, p)):      # a file this builder created itself
                created.add(os.path.normpath(p))
                continue
            if not p.startswith("/"):
                if ".." in p.split("/"):
                    flags.append((ts, name, "relative path escapes the room", p[:160]))
                continue
            rp = os.path.normpath(p)
            if inside(rp, room) or any(rp.startswith(a) for a in allow) or rp == "/":
                continue
            if "/6f003c51-fc14-5da0-833a-45f53d6397be/tasks/" in rp and rp.endswith(".output"):      # the harness's own background-task output
                continue
            flags.append((ts, name, "path outside the room", p[:160]))
        if name == "Bash" and cmd:
            for kind, detail in relative_violations(cmd, cwd0 or room, room, allow, created):
                flags.append((ts, name, kind, detail))
        elif name in ("Glob", "Grep") and not isinstance(inp.get("path"), str):
            flags.append((ts, name, "search with no path runs in the starting directory", f"cwd={cwd0}"))
    text = open(path).read()
    for c in canaries:
        if c in text:
            flags.append((None, "transcript", "canary token present", c))
    return counts, flags


if __name__ == "__main__":
    args = sys.argv[1:]
    canaries, allow, pos = [], [], []
    i = 0
    while i < len(args):
        if args[i] == "--canary":
            canaries.append(args[i + 1]); i += 2
        elif args[i] == "--allow":
            allow.append(args[i + 1]); i += 2
        else:
            pos.append(args[i]); i += 1
    transcript, room = pos
    counts, flags = check(transcript, room, canaries, allow)
    print("tool calls:", counts)
    for f in flags:
        print("FLAG", f)
    print("ISOLATION RECORD CLEAN" if not flags else f"{len(flags)} FLAG(S)")
    sys.exit(1 if flags else 0)
