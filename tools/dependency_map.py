#!/usr/bin/env python3
"""The repository's dependency map: which script feeds which, and which physical quantities
each one uses.

Reads every module in src/ with Python's own parser (nothing is executed for the scan):
  - the imports between src/ modules and the names each module uses from another;
  - every numeric literal, matched against QUANTITIES, a catalogue of the measured inputs
    and of the values that one script derives and others copy.
The derived values are recomputed from the script that derives them (a few seconds), so
every hand-typed copy is checked against its source, not against another copy.

It reports:
  - topics and the imports within and between them;
  - quantities shared by more than one topic: the candidate links between the parts;
  - derived values retyped by hand instead of imported;
  - copies whose value differs from the source, each with its reason and, where it
    matters, its effect. A difference without a stated reason is DRIFT.

Usage:  python3 tools/dependency_map.py          (rewrites DEPENDENCIES.md)
Pinned by tests/test_dependency_map.py.
"""
import ast
import glob
import math
import os
import re
import sys
from collections import defaultdict

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SRC = os.path.join(ROOT, "src")
OUT = os.path.join(ROOT, "DEPENDENCIES.md")
sys.path.insert(0, SRC)

# ---------------------------------------------------------------------------- topics
TOPICS = {
    "3-3-1 selection": ["m331_why_three", "m331_three_generations", "m331_su3L_running", "m331_exact",
                        "m331_yukawa", "m331_threshold", "m331_closure", "m331_scalar", "m331_three_loop",
                        "m331_margin", "m331_zprime_recast", "m331_heavy_lepton", "m331_gravity_fixed_point", "m331_standalone",
                        "qcd_running", "rge_engine"],
    "Symmetry ladder": ["m331_breaking", "chiral_breaking", "casimir_diamonds", "graviton_exchange",
                        "macdowell_mansouri", "ladder_links", "ladder_standalone"],
    "Diamond experiment": ["stur_gravity_entanglement", "stur_gravity_full", "short_range_gravity"],
    "Classical and emergent gravity": ["stur_oppenheim", "stur_thermo_gravity", "stur_emergent", "stur_jacobson"],
    "Teleparallel gravity": ["stur_tegr", "stur_tegr_gr", "stur_tegr3d", "stur_tegr_corner", "stur_tegr_frame",
                             "stur_tegr_logs"],
    "Measurement, entropy, foundations": ["stur_derivation", "stur_born", "stur_measurement", "stur_unification",
                                          "stur_confinement", "stur_z2_higgs", "stur_lab_test"],
}
TOPIC_OF = {m: t for t, ms in TOPICS.items() for m in ms}
SHORT = {"3-3-1 selection": "331", "Symmetry ladder": "ladder", "Diamond experiment": "diamond",
         "Classical and emergent gravity": "classical", "Teleparallel gravity": "tegr",
         "Measurement, entropy, foundations": "foundations"}


# ---------------------------------------------------------------------- derived values
def _ew_at(mu):
    """sin^2 theta_W and 1/alpha at mu from the M_Z inputs, one-loop SM running, as
    src/m331_exact.run_two_loop starts the 3-3-1 couplings."""
    import m331_exact as E
    L0 = math.log(mu / E.MZ) / (2 * math.pi)
    aY = (1 - E.s2) * E.ainv - 41 / 6 * L0
    a2 = E.s2 * E.ainv + 19 / 6 * L0
    return a2 / (aY + a2), aY + a2


def _design_a():
    import graviton_exchange as GX
    import stur_gravity_full as GF
    return dict(GF.design_a(), dphi=GX.branch_phases()[0])


def _c_area():
    txt = open(os.path.join(ROOT, "results", "unification", "output.txt")).read()
    return float(re.search(r"extrapolated S = ([0-9.]+) \(R/a\)\^2", txt).group(1))


def _diamond_radius():
    return cached("A", _design_a)["R"]


def _mt_threshold_effect():
    import qcd_running as Q
    return Q.alpha_s_run(4e3, thresholds=(1.27, 4.18, 172.57)) / Q.alpha_s_run(4e3) - 1


_CACHE = {}


def cached(key, fn):
    if key not in _CACHE:
        _CACHE[key] = fn()
    return _CACHE[key]


# ---------------------------------------------------------------------------- catalogue
# key: (label, value or callable, kind, origin, options)
#   kind:    "input" (measured, quoted) or "derived" (computed by a script in src/)
#   match:   relative window that identifies a literal as this quantity (default 2e-3)
#   same:    relative difference still counted as the same value, rounded (default 2e-4)
#   variants: {literal: reason}; an explained difference. Anything else is DRIFT.
#   skip:    (module, substring of the source line): literals that only look like it
#   note:    what the quantity connects
Q = {}


def q(key, label, value, kind, origin, **opt):
    Q[key] = dict(label=label, value=value, kind=kind, origin=origin, **opt)


hbar, c0, G0, eC = 1.054571817e-34, 299792458.0, 6.67430e-11, 1.602176634e-19
q("G", "Newton's G (m³ kg⁻¹ s⁻²)", G0, "input", "CODATA 2018",
  note="gravity's only input; it also fixes M_Pl, the 3-3-1 cutoff")
q("hbar", "ħ (J s)", hbar, "input", "SI exact", note="exact by definition, so copies cannot drift")
q("c", "c (m/s)", c0, "input", "SI exact", note="exact by definition, so copies cannot drift")
q("kB", "k_B (J/K)", 1.380649e-23, "input", "SI exact", note="exact by definition, so copies cannot drift")
q("e", "e (C)", eC, "input", "SI exact", note="exact by definition, so copies cannot drift")
q("kC", "1/4πε₀ (N m² C⁻²)", 8.9875517923e9, "input", "CODATA 2018")
q("u", "atomic mass unit (kg)", 1.66053906660e-27, "input", "CODATA 2018")
q("hbarc", "ħc (GeV fm)", 0.1973269804, "input", "CODATA 2018")
q("M_Pl", "Planck mass √(ħc/G) (GeV)", lambda: math.sqrt(hbar * c0 / G0) * c0**2 / eC / 1e9, "derived",
  "√(ħc/G) from G, ħ, c (this tool)", match=1e-3,
  checked_by="src/ladder_links.py L3 (SYMMETRY_LADDER.md, link 3)",
  note="the 3-3-1 selection's cutoff. It is typed as a number in the 3-3-1 scripts; it is "
       "√(ħc/G), the G the diamond experiment uses")
q("l_Pl", "Planck length √(ħG/c³) (m)", lambda: math.sqrt(hbar * G0 / c0**3), "derived",
  "√(ħG/c³) from G, ħ, c (this tool)")
q("Lambda", "cosmological constant Λ (m⁻²)", 1.1056e-52, "input", "Planck 2018")
q("ainv0", "1/α(0)", 137.035999084, "input", "CODATA 2018", match=1e-6)
q("ainvMZ", "1/α(M_Z), MS-bar", 127.951, "input", "PDG 2024",
  note="with sin²θ_W(M_Z) it fixes the U(1)_X start of every 3-3-1 run")
q("s2MZ", "sin²θ_W(M_Z), MS-bar", 0.23122, "input", "PDG 2024",
  variants={0.2312: "ATLAS's Z′_SSM convention, quoted as ATLAS uses it (m331_zprime_recast)"})
q("MZ", "M_Z (GeV)", 91.1876, "input", "PDG 2024", match=1e-4)
q("GZ", "Γ_Z (GeV)", 2.4952, "input", "PDG 2024")
q("GF", "G_F (GeV⁻²)", 1.1663788e-5, "input", "PDG 2024")
q("v", "electroweak vev (√2 G_F)^(−1/2) (GeV)", lambda: (math.sqrt(2) * 1.1663788e-5) ** -0.5, "derived",
  "src/m331_breaking.py B7", note="derived in rung 1 and retyped in the 3-3-1 Yukawa scripts")
q("as", "α_s(M_Z)", 0.1180, "input", "PDG 2024", match=1e-4)
q("mt", "top-quark mass (GeV)", 172.57, "input", "PDG 2024", match=1e-3,
  variants={172.69: "PDG 2022 value, used only as the α_s flavour threshold (qcd_running and its "
                    "copy in m331_standalone); α_s(4 TeV) moves by {mt_eff:+.1e} if it is changed to "
                    "172.57"})
q("s2TeV", "sin²θ_W(4 TeV)", lambda: cached("ew", lambda: _ew_at(4e3))[0], "derived",
  "one-loop SM running from M_Z (m331_exact.run_two_loop)", match=2e-3)
q("ainvTeV", "1/α(4 TeV)", lambda: cached("ew", lambda: _ew_at(4e3))[1], "derived",
  "one-loop SM running from M_Z (m331_exact.run_two_loop)", match=1e-3, same=5e-4)
q("MZp_MV", "M_Z′/M_V = √(4/3 (1 + β² t_X²)) at 4 TeV", lambda: math.sqrt(
    4 / 3 * (1 + cached("ew", lambda: _ew_at(4e3))[0] / 3 / (1 - 4 / 3 * cached("ew", lambda: _ew_at(4e3))[0]))),
  "derived", "src/m331_breaking.py B4, evaluated at sin²θ_W(4 TeV)", match=2e-3, same=1e-3,
  note="derived from the mass matrix in rung 1 and typed as 1.225 where the 3-3-1 scans need "
       "M_V from the Z′ bound. Rung 1's own printout evaluates it at sin²θ_W(M_Z), giving 1.217")
q("fpi", "f_π, √2 convention (GeV)", 0.1302, "input", "PDG 2024", match=1e-4)
q("mpi0", "m_π⁰ (GeV)", 0.1349768, "input", "PDG 2024", match=1e-5)
q("mpic", "m_π± (GeV)", 0.13957039, "input", "PDG 2024", match=1e-5)
q("gA", "nucleon g_A", 1.2754, "input", "PDG 2024", match=1e-4)
q("MN", "average nucleon mass (GeV)", 0.9389187, "input", "PDG 2024", match=1e-4)
q("cond", "\\|⟨q̄q⟩\\|^(1/3) (GeV)", 0.272, "input", "FLAG 2024", match=1e-4,
  skip=[("m331_standalone", "alpha_s(2.45")])
q("mumd", "m_u, m_d (GeV)", 2.16e-3, "input", "PDG 2024", match=1e-4)
q("mc_mb", "m_c (GeV), MS-bar, α_s threshold", 1.27, "input", "PDG 2024", match=1e-6)
q("mb", "m_b (GeV), MS-bar, α_s threshold", 4.18, "input", "PDG 2024", match=1e-6)
q("g2MZ", "SU(2) coupling g at M_Z, √(4πα)/sinθ_W", lambda: math.sqrt(4 * math.pi / 127.951 / 0.23122), "derived",
  "from 1/α(M_Z) and sin²θ_W(M_Z) (this tool)", match=2e-3, same=1e-3)
q("gpiNN", "empirical g_πNN (approximate)", 13.1, "input", "LIT", match=1e-6)
q("KEDR", "R-ratio below charm, KEDR (1.84–3.05 GeV)", 2.225, "input", "Anashin et al. 2017", match=1e-6)
q("KEDRmu", "R-ratio comparison scale (GeV), KEDR range midpoint", 2.45, "input", "this repository's choice",
  match=1e-6)
q("Gpi0", "Γ(π⁰ → γγ), PrimEx-I+II (eV)", 7.802, "input", "Larin et al. 2020", match=1e-6)
q("Gpi0sys", "PrimEx-I+II systematic error (eV)", 0.105, "input", "Larin et al. 2020", match=1e-6)
q("epsD", "diamond permittivity", 5.7, "input", "LIT", match=1e-6, short=True,
  skip=[("m331_", ""), ("stur_tegr", ""), ("stur_born", "")])
q("rhoD", "diamond density (kg/m³)", 3510.0, "input", "LIT", match=1e-6)
q("mE", "Earth mass (kg)", 5.972e24, "input", "LIT", match=1e-3)
q("R0", "Diósi–Penrose smearing bound R₀ (m)", 0.54e-10, "input", "Donadi et al. 2021", match=1e-3, short=True)
q("LISL", "short-range gravity test length (m)", 52e-6, "input", "Lee et al. 2020", match=1e-3, short=True)
q("c_s", "area-law coefficient S/(R/a)² per scalar", lambda: _c_area(), "derived",
  "src/stur_unification.py U3 (results/unification/output.txt)", match=2e-3,
  note="computed once and retyped in the classical/emergent-gravity scripts")
# Design A: every script imports it from stur_gravity_full.design_a(); single_source means a
# typed-in copy anywhere is a failure (tests/test_dependency_map.py). match is wide enough to
# catch the old rounded copies (1.5e-14 kg, 1.007 um, 721 um, 1.58 s, 3.24 s).
q("A_m", "design A: mass (kg)", lambda: cached("A", _design_a)["m"], "derived",
  "src/stur_gravity_full.py design_a()", match=0.03, same=1e-3, single_source=True, short=True)
q("A_R", "design A: diamond radius (m)", lambda: _diamond_radius(), "derived",
  "src/stur_gravity_full.py design_a()", match=0.02, same=1e-3, single_source=True)
q("A_dx", "design A: branch separation Δx (m)", lambda: cached("A", _design_a)["dx"], "derived",
  "src/stur_gravity_full.py design_a()", match=2e-3, same=5e-4, single_source=True)
q("A_gap", "Casimir-safe gap (m)", lambda: cached("A", _design_a)["gap"], "derived",
  "src/stur_gravity_full.py design_a() (Casimir < 10% of gravity)", match=2e-3, same=5e-4,
  single_source=True, skip=[("ladder_standalone", "abs(gap - 181.16e-6)")])
q("A_ramp", "design A: ramp time (s)", lambda: cached("A", _design_a)["ramp"], "derived",
  "src/stur_gravity_full.py design_a()", match=2e-3, same=1e-3, single_source=True)
q("A_total", "design A: total time (s)", lambda: cached("A", _design_a)["total"], "derived",
  "src/stur_gravity_full.py design_a()", match=3e-3, same=2e-3, single_source=True,
  skip=[("stur_z2_higgs", "cut = 3.25")])
q("A_dphi", "design A: entangling phase Δφ (rad)", lambda: cached("A", _design_a)["dphi"], "derived",
  "src/graviton_exchange.py N4", match=1e-3, same=1e-4)
q("pe", "\\|q_p + q_e\\| bound (e)", 1e-21, "input", "Bressi et al. 2011", match=1e-6, short=True,
  skip=[("ladder_links", "Q_N_MEAS[0] / 1e-21"), ("ladder_links", "Q_N_MEAS[1] / 1e-21")])

FMT = dict(mt_eff=lambda: _mt_threshold_effect())

# numbers that recur but are not physical quantities: numerical tolerances, grid bounds,
# step sizes, and the baseline design of stur_gravity_entanglement.BASE
NUMERIC = {1e-300, 1e-15, 1e-14, 1e-13, 1e-12, 1e-10, 1e-09, 1e-08, 1e-07, 1e-06, 1e-05, 1e-04, 1e-16,
           1e-17, 1e-20, 1e+45, 0.0001, 0.002, 0.003, 0.005, 0.0002, 0.00025, 1e-21,
           36525.0}                                                    # days per Julian century


# ---------------------------------------------------------------------------- scan
def scan():
    mods = {os.path.basename(f)[:-3]: f for f in sorted(glob.glob(os.path.join(SRC, "*.py")))}
    info = {}
    for m, f in mods.items():
        text = open(f, encoding="utf8").read()
        lines = text.splitlines()
        tree = ast.parse(text)
        doc = " ".join((ast.get_docstring(tree) or "").split())
        alias, imports = {}, set()
        for n in ast.walk(tree):
            if isinstance(n, ast.Import):
                for a in n.names:
                    if a.name in mods:
                        imports.add(a.name)
                        alias[a.asname or a.name] = a.name
            elif isinstance(n, ast.ImportFrom) and n.module in mods:
                imports.add(n.module)
        used = defaultdict(set)
        for n in ast.walk(tree):
            if isinstance(n, ast.Attribute) and isinstance(n.value, ast.Name) and n.value.id in alias:
                used[alias[n.value.id]].add(n.attr)
        lits = []
        for n in ast.walk(tree):
            if isinstance(n, ast.Constant) and isinstance(n.value, float):    # physical values are floats here;
                lits.append((n.value, n.lineno, lines[n.lineno - 1]))         # integers are counts and factors
        # negative literals appear as UnaryOp(-, Constant); keep them signed
        for n in ast.walk(tree):
            if isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.USub) and isinstance(n.operand, ast.Constant) \
                    and isinstance(n.operand.value, float):
                lits.append((-float(n.operand.value), n.lineno, lines[n.lineno - 1]))
        info[m] = dict(doc=doc, imports=imports, used=used, lits=lits)
    return info


def evaluate():
    vals = {}
    for k, d in Q.items():
        vals[k] = d["value"]() if callable(d["value"]) else d["value"]
    return vals


def sigdigits(v):
    return len(f"{abs(v):.12g}".split("e")[0].replace(".", "").lstrip("0").rstrip("0"))


def occurrences(info, vals):
    occ = defaultdict(list)
    seen = set()
    for m, d in info.items():
        for v, line, src in d["lits"]:
            if v == 0:
                continue
            for k, qd in Q.items():
                ref = vals[k]
                if ref is None or math.copysign(1, v) != math.copysign(1, ref):
                    continue
                if abs(v / ref - 1) > qd.get("match", 2e-3):
                    continue
                listed = any(abs(v / lit - 1) < 1e-12 for lit in qd.get("variants", {}))
                if sigdigits(v) < 3 and not listed and not qd.get("short"):   # 2.5, 0.25: grid points, not copies
                    continue
                if any(m.startswith(sm) and sub in src for sm, sub in qd.get("skip", [])):
                    continue
                key = (k, m, line, v)
                if key in seen:
                    continue
                seen.add(key)
                occ[k].append(dict(module=m, line=line, value=v))
    return occ


def status(k, v, ref):
    qd = Q[k]
    rel = abs(v / ref - 1)
    if rel < 1e-9:
        return "exact", ""
    if rel <= qd.get("same", 2e-4):
        return "rounded", ""
    for lit, why in qd.get("variants", {}).items():
        if abs(v / lit - 1) < 1e-12:
            return "variant", why.format(**{n: f() for n, f in FMT.items() if "{" + n in why})
    return "DRIFT", ""


def fmt(v):
    if v == 0:
        return "0"
    a = abs(v)
    if 1e-3 <= a < 1e5:
        return f"{v:.6g}"
    return f"{v:.6e}".replace("e-0", "e-").replace("e+0", "e+").replace("e+", "e")


def uncatalogued(info, occ):
    matched = {(o["module"], o["line"], o["value"]) for os_ in occ.values() for o in os_}
    rep = defaultdict(set)
    for m, d in info.items():
        for v, line, src in d["lits"]:
            if v in NUMERIC or (m, line, v) in matched:
                continue
            if sigdigits(v) < 3:
                continue
            rep[v].add(m)
    return {v: sorted(ms) for v, ms in rep.items() if len(ms) >= 2}


def build():
    info = scan()
    vals = evaluate()
    occ = occurrences(info, vals)
    missing = sorted(set(info) - set(TOPIC_OF))
    stale = sorted(set(TOPIC_OF) - set(info))
    rows = {}
    for k in Q:
        os_ = sorted(occ.get(k, []), key=lambda o: (o["module"], o["line"]))
        for o in os_:
            o["status"], o["why"] = status(k, o["value"], vals[k])
        rows[k] = os_
    return info, vals, rows, missing, stale


# ---------------------------------------------------------------------------- report
def report(info, vals, rows, missing, stale):
    L = []
    w = L.append
    edges = sorted((a, b) for a, d in info.items() for b in d["imports"])
    cross = [(a, b) for a, b in edges if TOPIC_OF.get(a) != TOPIC_OF.get(b)]
    copies = {k: r for k, r in rows.items() if len({o["module"] for o in r}) >= 2}
    drift = [(k, o) for k, r in rows.items() for o in r if o["status"] == "DRIFT"]
    variants = [(k, o) for k, r in rows.items() for o in r if o["status"] == "variant"]
    shared = {k: sorted({TOPIC_OF.get(o["module"], "?") for o in r}) for k, r in rows.items()}
    shared = {k: t for k, t in shared.items() if len(t) >= 2}
    isolated = [m for m, d in info.items() if not d["imports"] and not any(m in e["imports"] for e in info.values())]

    w("# Dependency map")
    w("")
    w("*Generated by [`tools/dependency_map.py`](tools/dependency_map.py); do not edit by hand. "
      "Run `python3 tools/dependency_map.py` after changing a script; "
      "`tests/test_dependency_map.py` fails if this page is out of date or if a copied value "
      "drifts from its source without a stated reason.*")
    w("")
    w("This page records which script feeds which, and which physical quantities each one "
      "uses. A quantity that two parts of the repository share, but don't import from one "
      "place, is either a copy that can drift or a link between the parts that nothing checks yet.")
    w("")
    w("## Summary")
    w("")
    w(f"- **{len(info)} scripts** in `src/`, in {len(TOPICS)} topics; **{len(edges)} imports** between "
      f"them, {len(cross)} of them across topics. {len(isolated)} scripts import nothing from the others "
      "and nothing imports them.")
    w(f"- **{len(Q)} catalogued quantities** ({sum(d['kind'] == 'input' for d in Q.values())} measured inputs, "
      f"{sum(d['kind'] == 'derived' for d in Q.values())} derived in the repository), found as "
      f"{sum(len(r) for r in rows.values())} literals in the source.")
    w(f"- **{len(copies)} quantities are typed in more than one script**; "
      f"{len(shared)} of them are shared by more than one topic.")
    w(f"- **{len(variants)} copies differ from their source for a stated reason**; "
      f"**{len(drift)} differ without one (drift).**")
    if missing or stale:
        w(f"- Scripts without a topic: {', '.join(missing) or 'none'}; topics naming missing scripts: "
          f"{', '.join(stale) or 'none'}.")
    w("")

    w("## Imports")
    w("")
    w("Solid arrows are imports (`A --> B`: A uses B). Scripts with no arrows stand alone.")
    w("")
    w("```mermaid")
    w("flowchart LR")
    for t, ms in TOPICS.items():
        w(f'  subgraph {SHORT[t]}["{t}"]')
        for m in ms:
            if m in info:
                w(f"    {m}")
        w("  end")
    for a, b in edges:
        w(f"  {a} --> {b}")
    w("```")
    w("")
    w("### Across topics")
    w("")
    w("| From | To | Names used |")
    w("|---|---|---|")
    for a, b in cross:
        names = ", ".join(f"`{n}`" for n in sorted(info[a]["used"].get(b, []))) or "(module import only)"
        w(f"| `{a}` ({TOPIC_OF.get(a)}) | `{b}` ({TOPIC_OF.get(b)}) | {names} |")
    w("")
    w("### By topic")
    w("")
    for t, ms in TOPICS.items():
        w(f"**{t}**")
        w("")
        w("| Script | Imports | What it is |")
        w("|---|---|---|")
        for m in ms:
            if m not in info:
                continue
            d = info[m]
            imp = ", ".join(f"`{x}`" for x in sorted(d["imports"])) or "—"
            doc = d["doc"].split(". ")[0][:140].replace("|", "\\|")
            w(f"| [`{m}`](src/{m}.py) | {imp} | {doc} |")
        w("")

    w("## Quantities shared across topics: the candidate links")
    w("")
    w("Each row is one quantity typed into scripts of more than one topic. Where it is an "
      "input, the topics agree only because the same number was typed twice; where it is "
      "derived, one topic's output is another's input.")
    w("")
    w("| Quantity | Kind | Topics | Scripts | What it connects |")
    w("|---|---|---|---|---|")
    for k, ts in sorted(shared.items(), key=lambda x: (-len(x[1]), Q[x[0]]["label"])):
        ms = sorted({o["module"] for o in rows[k]})
        w(f"| {Q[k]['label']} | {Q[k]['kind']} | {', '.join(ts)} | {', '.join(f'`{m}`' for m in ms)} | "
          f"{Q[k].get('note', '')} |")
    w("")
    hidden = [k for k in Q if Q[k]["kind"] == "derived" and k in ("M_Pl", "l_Pl")]
    w("**Links through a formula.** Some quantities share inputs without sharing a number:")
    w("")
    for k in hidden:
        ms = sorted({o["module"] for o in rows[k]})
        topics = sorted({TOPIC_OF.get(m) for m in ms})
        w(f"- **{Q[k]['label']} = {fmt(vals[k])}**, typed as a number in "
          f"{', '.join(f'`{m}`' for m in ms) or 'no script'} ({', '.join(t for t in topics if t) or '—'}). "
          "It follows from G, ħ and c, which the gravity scripts type separately; "
          + (f"{Q[k]['checked_by']} checks that the two agree." if Q[k].get("checked_by")
             else "nothing checks that the two agree except this page."))
    w("")

    w("## Derived values typed by hand")
    w("")
    w("Values computed in one script and retyped in others instead of imported. Each copy is "
      "checked against the value recomputed from its source.")
    w("")
    w("| Quantity | Source | Value | Copies |")
    w("|---|---|---|---|")
    for k, r in rows.items():
        if Q[k]["kind"] != "derived" or not r:
            continue
        cp = "; ".join(f"`{o['module']}:{o['line']}` {fmt(o['value'])} ({o['status']})" for o in r)
        w(f"| {Q[k]['label']} | {Q[k]['origin']} | {fmt(vals[k])} | {cp} |")
    w("")

    single = [k for k in Q if Q[k].get("single_source")]
    w("## Values with one source")
    w("")
    w("These are imported from their source by every script that uses them; a typed-in copy "
      "fails `tests/test_dependency_map.py`.")
    w("")
    w("| Quantity | Value | Source | Typed-in copies |")
    w("|---|---|---|---|")
    for k in single:
        cp = "; ".join(f"`{o['module']}:{o['line']}`" for o in rows[k]) or "none"
        w(f"| {Q[k]['label']} | {fmt(vals[k])} | {Q[k]['origin']} | {cp} |")
    w("")

    w("## Copies that differ from the source")
    w("")
    if not variants and not drift:
        w("None.")
    else:
        w("| Quantity | Source value | Copy | Where | Status | Reason and effect |")
        w("|---|---|---|---|---|---|")
        groups = defaultdict(list)
        for k, o in variants + drift:
            groups[(k, o["value"], o["status"], o["why"])].append(f"`{o['module']}:{o['line']}`")
        for (k, v, st, why), where in groups.items():
            w(f"| {Q[k]['label']} | {fmt(vals[k])} | {fmt(v)} | {', '.join(where)} | "
              f"{st} | {why or 'none stated'} |")
    w("")
    w("*Rounded* copies (within the quantity's stated precision) are listed in the full table below, not here.")
    w("")

    w("## Every catalogued quantity")
    w("")
    w("| Quantity | Kind | Value | Origin | Typed in |")
    w("|---|---|---|---|---|")
    for k, r in rows.items():
        by = defaultdict(list)
        for o in r:
            by[o["module"]].append(o)
        where = ", ".join(f"`{m}`" + ("" if all(o["status"] == "exact" for o in os_) else
                                       " (" + ", ".join(sorted({o['status'] for o in os_})) + ")")
                          for m, os_ in sorted(by.items())) or "—"
        w(f"| {Q[k]['label']} | {Q[k]['kind']} | {fmt(vals[k])} | {Q[k]['origin']} | {where} |")
    w("")

    unc = uncatalogued(info, rows_to_occ(rows))
    w("## Repeated numbers not in the catalogue")
    w("")
    w("Literals with at least three significant digits that appear in two or more scripts and "
      "match no catalogued quantity. Most are grid points or example values; any that is a "
      "physical quantity belongs in the catalogue.")
    w("")
    if unc:
        w("| Value | Scripts |")
        w("|---|---|")
        for v, ms in sorted(unc.items(), key=lambda x: abs(x[0])):
            w(f"| {fmt(v)} | {', '.join(f'`{m}`' for m in ms)} |")
    else:
        w("None.")
    w("")
    return "\n".join(L)


def rows_to_occ(rows):
    return {k: r for k, r in rows.items()}


def main():
    info, vals, rows, missing, stale = build()
    text = report(info, vals, rows, missing, stale)
    with open(OUT, "w", encoding="utf8") as f:
        f.write(text)
    drift = [(k, o) for k, r in rows.items() for o in r if o["status"] == "DRIFT"]
    print(f"wrote {os.path.relpath(OUT, ROOT)}: {len(info)} scripts, {len(Q)} quantities, "
          f"{len(drift)} drifting copies")
    for k, o in drift:
        print(f"   DRIFT {k}: {o['module']}:{o['line']} = {o['value']} (source {vals[k]})")
    return text


if __name__ == "__main__":
    main()
