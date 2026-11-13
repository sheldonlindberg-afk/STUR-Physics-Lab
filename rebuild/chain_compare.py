"""The force chain against an accepted rebuild: do the two agree where they overlap?

VERIFIER ONLY, like oracle.py: it runs src/force_chain.py and reads src/ modules, so it must never
be copied into a clean room (cleanroom.py copies only its explicit ALLOWED list).

src/force_chain.py hands values from stage to stage through a ledger. An accepted build of the
symmetry ladder (rebuild/builds/<id>/) computes many of the same values blind. Each overlap is
compared in one of two ways:

  * same arguments: the build's export is called with the chain's own arguments (the chain's
    alpha(0), f_pi, gap, Lambda, ...). Both sides then compute the same quantity, so they must agree
    to rounding; a difference is a physics or convention error on one side.
  * own route: the build's headline value, from its own inputs, against the chain's value. The two
    may differ, but only for a reason recorded in KNOWN below, and only inside the recorded band, so
    a change on either side shows up.

    python3 rebuild/chain_compare.py rebuild/builds/2026-11-b
"""
import contextlib
import importlib
import io
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "src")
sys.path.insert(0, HERE)

import contract  # noqa: E402
import harness   # noqa: E402

# own-route differences with a known cause: label -> (lowest, highest relative difference, reason)
KNOWN = {
    "alpha(0): chain's running vs the build's input": (
        0.0, 1e-9, "the chain runs 1/alpha-hat(M_Z) down to q = 0 (Delta alpha_had input); the build reads "
                   "inputs.ALPHA_0 (CODATA). They agree to the precision of the running's inputs"),
    "f_pi: chain's stage 3 vs the build's weak.fpi_from_pion_decay": (
        0.0, 1e-9, "the same route (G_F and Gamma(pi -> mu nu)); hbar in GeV s from HBAR/E_CH vs src's constant"),
    "pi0 width: chain vs the build's pi0_width_from_rungs": (
        0.0, 2e-9, "the same f_pi route; the chain's alpha(0) is its running, the build's is inputs.ALPHA_0"),
    "m_pi O(p^4): chain vs the build's chpt_mpi on its own inputs": (
        2.5e-3, 3.0e-3, "chiral's O(p^4) headline still takes the lattice inputs.F_PI = 130.2/sqrt2 MeV; the chain "
                        "uses its derived f_pi = 130.57 MeV, through F = f_pi/(F_pi/F)"),
    "+1/sqrt3 Landau pole, N_c = 3: the build's one loop vs the chain's three loops": (
        0.50, 0.56, "one loop, no thresholds or Yukawas (stage running) vs the chain's three loops with the "
                    "reference spectrum's thresholds and Yukawas (src/m331_three_loop.py)"),
    "+1/sqrt3 Landau pole, N_c = 5: the build's one loop vs the chain's three loops": (
        0.38, 0.44, "as for N_c = 3"),
    "neutrality: chain vs the build's neutrality_per_nucleon": (
        0.0, 1e-9, "the chain writes k e^2 = alpha(0) hbar c with its derived alpha(0); the build uses "
                   "inputs.K_COUL and E_CH"),
    "safe gap: chain vs the build's casimir_safe_gap": (
        2.9e-4, 3.0e-4, "the chain takes src's casimir_safe_gap, the first point of a 4000-point grid above "
                        "the root (FINDINGS N3); the build bisects to the root SPEC section 4 defines"),
    "design phase: chain vs the build's design_phase": (
        4.4e-4, 4.6e-4, "the gap row above, carried into the phase (FINDINGS N3)"),
}


def _rel(a, b):
    return abs(a - b) / max(abs(b), 1e-300)


def chain_values():
    """Run the force chain once and collect its hand-offs and the arguments it used."""
    if SRC not in sys.path:
        sys.path.insert(0, SRC)
    fc = importlib.import_module("force_chain")
    gx = importlib.import_module("graviton_exchange")
    ll = importlib.import_module("ladder_links")
    cb = importlib.import_module("chiral_breaking")
    bh = importlib.import_module("black_holes")
    with contextlib.redirect_stdout(io.StringIO()):
        ledger, _ = fc.run()
        _, _, _, (m, dx, gap, hold, ramp) = gx.branch_phases()
    v = {name: value for name, value, _, _ in ledger}
    v["_design"] = (float(m), float(dx), float(hold), float(ramp), float(gap))
    v["_m_pi0"] = ll.M_PI0_GEV
    v["_lambda"] = ll.LAMBDA_SI
    v["_flag"] = (cb.M_UD_FLAG[0], cb.SIGMA_CUBE_ROOT, cb.FPI_OVER_F[0], cb.LBAR3[0])
    v["_sgra_kg"] = bh.SGRA_VLTI[0] * bh.GM_SUN / v["G"]
    t3, mg = importlib.import_module("m331_three_loop"), importlib.import_module("m331_margin")
    v["_poles"] = tuple(t3.pole(n, "+1/sqrt3", MV=4e3, gmax=mg.ALPHA1) for n in (3, 5))   # as force_chain stage 1
    return v


def compare(build_dir, chain=None):
    """[(label, kind, chain value, build value, rel diff, ok, note)] for one build."""
    c = chain or chain_values()
    mods, errors = harness.load_build(build_dir, contract.STAGES)
    if errors:
        raise RuntimeError(f"build does not load: {errors}")
    G8, Ch, Cs, Gr, D, B, R, W, Lk = (mods[k] for k in ("gauge331", "chiral", "casimir", "graviton", "desitter",
                                                          "blackholes", "running", "weak", "links"))
    import inputs as I
    rows = []

    def same(label, chain_v, build_v, rtol=1e-12, note=""):
        d = _rel(build_v, chain_v)
        rows.append((label, "same arguments", chain_v, build_v, d, d <= rtol, note or f"rtol {rtol:g}"))

    def exact(label, chain_v, build_v):
        rows.append((label, "same arguments", chain_v, build_v, 0.0 if chain_v == build_v else 1.0,
                     chain_v == build_v, "exact"))

    def own(label, chain_v, build_v):
        d = _rel(build_v, chain_v)
        lo, hi, why = KNOWN.get(label, (0.0, 1e-9, "no known cause: must agree"))
        rows.append((label, "own route", chain_v, build_v, d, lo <= d <= hi, f"band [{lo:g}, {hi:g}]: {why}"))

    # stage 1: charges, neutrality, Planck mass
    Qu, Qd = G8.quark_charges(3)
    exact("quark charges (N_c = 3)", (c["Q_u"], c["Q_d"]), (Qu, Qd))
    qp, qn, qe, qnu = Lk.matter_charges(3, "+1/sqrt3")
    exact("q_p + q_e (beta = +1/sqrt3)", c["q_p + q_e"], qp + qe)
    same("Planck mass from the chain's G", c["M_Pl"], Lk.planck_mass_GeV(c["G"], I.HBAR, I.C_LIGHT))
    # stage 2 and 3: the build reads these as inputs
    own("alpha(0): chain's running vs the build's input", c["alpha(0)"], I.ALPHA_0)
    own("f_pi: chain's stage 3 vs the build's weak.fpi_from_pion_decay", c["f_pi"], W.fpi_from_pion_decay())
    q3, q5 = c["_poles"]
    b3, b5 = R.landau_pole(3, "+1/sqrt3"), R.landau_pole(5, "+1/sqrt3")
    own("+1/sqrt3 Landau pole, N_c = 3: the build's one loop vs the chain's three loops", q3, b3)
    own("+1/sqrt3 Landau pole, N_c = 5: the build's one loop vs the chain's three loops", q5, b5)
    rows.append(("N_c = 3 selected against M_Pl: the build's one loop agrees with the chain's three loops",
                 "own route", float(q5 < c["M_Pl"] < q3), float(b5 < c["M_Pl"] < b3), 0.0,
                 (q5 < c["M_Pl"] < q3) and (b5 < c["M_Pl"] < b3), "pole_5 < M_Pl < pole_3 on both sides"))
    # stage 4: the strong force
    F = c["f_pi"] / math.sqrt(2)
    same("pi0 width with the chain's alpha(0), f_pi and charges", c["pi0 width"],
         Lk.pi0_width_eV(c["alpha(0)"], F, c["_m_pi0"], c["N_c"], c["Q_u"], c["Q_d"]))
    own("pi0 width: chain vs the build's pi0_width_from_rungs", c["pi0 width"], Lk.pi0_width_from_rungs())
    mq, cond, ratio, lbar = c["_flag"]
    same("O(p^4) pion mass with the chain's f_pi", c["m_pi O(p^4)"], Ch.chpt_mpi(mq, cond, ratio, lbar, F))
    own("m_pi O(p^4): chain vs the build's chpt_mpi on its own inputs", c["m_pi O(p^4)"],
        Ch.chpt_mpi(I.M_UD_FLAG, I.COND_13, I.FPI_OVER_F, I.LBAR3, I.F_PI))
    # stage 5: the lab's electromagnetism
    own("neutrality: chain vs the build's neutrality_per_nucleon", c["neutrality needed"],
        Lk.neutrality_per_nucleon(c["diamond mass"]))
    build_gap = Cs.casimir_safe_gap(I.GAP_BASELINE_MASS, I.GAP_BASELINE_DX, I.GAP_BASELINE_TAU, I.GAP_FRACTION)
    own("safe gap: chain vs the build's casimir_safe_gap", float(c["gap"]), build_gap)
    rows.append(("safe gap: the chain's grid point lies above the build's root, within one grid step",
                 "own route", float(c["gap"]), build_gap, _rel(build_gap, float(c["gap"])),
                 build_gap < float(c["gap"]) <= build_gap * (1e3 ** (1 / 3999)) * (1 + 1e-9),
                 "src's grid is 4000 log points over 1e-6..1e-3 m"))
    # stage 6: gravity in the lab
    m, dx, hold, ramp, gap = c["_design"]
    same("entangling phase at the chain's mass, dx, hold, ramp and gap", float(c["phase"]),
         Gr.entangling_phase(m, dx, hold, ramp, gap), rtol=1e-9, note="rtol 1e-9 (both trapezoid, n = 4001)")
    own("design phase: chain vs the build's design_phase", float(c["phase"]), Gr.design_phase())
    same("diamond mass: the chain's design A vs inputs.DESIGN_A_MASS", c["diamond mass"], I.DESIGN_A_MASS)
    # stage 7: gravity as a broken gauge theory
    same("de Sitter radius from the chain's Lambda", c["l"], D.ell_from_lambda(c["_lambda"]))
    f_sym, Ms, ls = c["f(r)"]
    import sympy as sp
    fnum = sp.lambdify((sp.Symbol("r", positive=True), Ms, ls), f_sym, "math")
    rb, rc = B.sds_horizons(1.0, 9.0)
    worst = max(abs(fnum(r, 1.0, 9.0)) for r in (rb, rc))
    rows.append(("the chain's f(r) vanishes at the build's SdS horizons (M = 1, l = 9)", "same arguments",
                 0.0, worst, worst, worst < 1e-12, "|f(r_b)|, |f(r_c)| < 1e-12"))
    # stage 8: black holes
    same("Sgr A* Hawking temperature (Lambda's 2e-32 shift is below rounding)", c["Sgr A* T_H"],
         B.hawking_K(c["_sgra_kg"]), rtol=1e-12)
    own("end temperature: chain vs the build's planck_bh_kT_GeV", c["end temperature"], Lk.planck_bh_kT_GeV())
    harness.unload(build_dir)
    return rows


def summarize(rows):
    lines = []
    for label, kind, cv, bv, d, ok, note in rows:
        lines.append(f"{'PASS' if ok else 'FAIL'}  [{kind}] {label}: rel diff {d:.2e}")
        if kind == "own route" and d > 1e-9:
            lines.append(f"        chain {cv!r}  build {bv!r}")
            lines.append(f"        {note}")
    n = sum(ok for *_, ok, _ in rows)
    lines.append(f"\n{n}/{len(rows)} overlaps agree" + ("" if n == len(rows) else " -- FAILURES"))
    return "\n".join(lines)


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    if not argv:
        print(__doc__)
        return 2
    chain = chain_values()
    bad = 0
    for b in argv:
        rows = compare(b, chain)
        print(f"== force chain vs {os.path.basename(os.path.normpath(b))}\n{summarize(rows)}\n")
        bad += sum(not ok for *_, ok, _ in rows)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
