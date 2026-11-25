"""Writes assets/site-data.js: the numbers and curves the website displays.

Every value comes from production_v2_2.py (one full run); nothing here is typed in.
    python3 tools/site_data.py
"""
import importlib.util
import json
import math
import os

ROOT = os.path.join(os.path.dirname(__file__), "..")
spec = importlib.util.spec_from_file_location("production_v2_2", os.path.join(ROOT, "production_v2_2.py"))
P = importlib.util.module_from_spec(spec)
spec.loader.exec_module(P)


def sampled(state, mu0, mu1, rhs, n):
    """Run state from mu0 to mu1, returning (log10 mu, state) at n+1 points (log-spaced)."""
    out, s = [(math.log10(mu0), list(state))], list(state)
    steps = int(P.num("rg_steps_per_efold"))
    l0, l1 = math.log(mu0), math.log(mu1)
    for i in range(1, n + 1):
        a, b = math.exp(l0 + (l1 - l0) * (i - 1) / n), math.exp(l0 + (l1 - l0) * i / n)
        s = P.integrate_ln_mu(s, a, b, rhs, [], steps)
        out.append((math.log10(b), list(s)))
    return out


def main():
    res = P.run()
    cr, hg, au, yk, qg = res["criticality"], res["higgs"], res["alpha_unification"], res["yukawa"], res["quantum_gravity"]
    mh_meas = float(P.COMPARISONS["m_h"]["value"][0])
    mp = cr["planck"]["M_P"]
    # Part L: lambda(mu) for the measured Higgs mass and for the critical one
    curves = {}
    for key, mh in (("measured", mh_meas), ("critical", cr["central"]["m_h"])):
        big_mt, v, st = P.anchored_state(None, mh, cr["smdr"])       # Part L's central order
        pts = sampled(st, big_mt, mp, P.sm_rge(3), 80)
        curves[key] = {"m_h": mh, "pts": [[round(x, 4), round(s[6], 6)] for x, s in pts]}
    prof = P.sm_lambda_profile(cr, mh_meas)
    # Part I: inverse gauge couplings, SM all the way and MSSM above M_S (one loop, for display)
    mt, st = P.couplings_at_mt(res["flavour"])
    m_s, m_gut = au["M_S_for_measured_alpha"]["M_S_GeV"], au["M_S_for_measured_alpha"]["M_GUT_GeV"]

    def inv_alpha(s):
        return [round(4 * math.pi / g ** 2, 4) for g in s[:3]]
    sm_line = [[round(x, 4)] + inv_alpha(s) for x, s in sampled(st, mt, mp, P.yukawa_rhs("SM"), 80)]
    s_ms = P.run_to(st, mt, m_s, "SM")
    tb = yk["btau_MSSM_unity"]["tan_beta"]
    sb, cb = tb / math.sqrt(1 + tb * tb), 1 / math.sqrt(1 + tb * tb)
    s0 = [s_ms[0], s_ms[1], s_ms[2], s_ms[3] / sb, s_ms[4] / cb, s_ms[5] / cb]
    mssm_line = [[round(x, 4)] + inv_alpha(s) for x, s in sampled(s0, m_s, m_gut, P.yukawa_rhs("MSSM"), 60)]
    # Part C: the surviving pattern and what it predicts at m_t(m_t)
    mu0 = res["scales"][0]
    surv = [r for r in res["survey"][mu0]["classes"] if r["status"] == "tested" and r["survives"]][0]
    tested = [r for r in res["survey"][mu0]["classes"] if r["status"] == "tested"]
    j_meas, j_sig, _ = P._comparison("J")
    q_meas, q_sig, _ = P._comparison("V_td/V_ts")
    best = min(surv["prediction"], key=lambda o: ((o["J"] - j_meas) / math.hypot(o["J_sigma"], j_sig)) ** 2
               + ((o["V_td/V_ts"] - q_meas) / math.hypot(o["V_td/V_ts_sigma"], q_sig)) ** 2)
    c2 = (((best["J"] - j_meas) / math.hypot(best["J_sigma"], j_sig)) ** 2
          + ((best["V_td/V_ts"] - q_meas) / math.hypot(best["V_td/V_ts_sigma"], q_sig)) ** 2)
    texture = {"tested": len(tested), "survivors": sum(r["survives"] for r in tested),
               "up": P.pattern_mask(surv["zeros_u"]), "down": P.pattern_mask(surv["zeros_d"]),
               "J": best["J"], "J_sigma": best["J_sigma"], "J_meas": j_meas,
               "Vtd_Vts": best["V_td/V_ts"], "Vtd_Vts_sigma": best["V_td/V_ts_sigma"], "Vtd_Vts_meas": q_meas,
               "both_sigma": P.pvalue_to_sigma(P.chi2_pvalue(c2, 2))}
    # Part M: which high-energy hypothesis survives
    jt = res["joint"]
    rows = {(r["hypothesis"], "+".join(r["conditions"])): r for r in jt["rows"]}
    joint = {"sm_U": abs(jt["SM_pulls"]["U"]), "sm_B": abs(jt["SM_pulls"]["B"]), "sm_H": jt["SM_pulls"]["H"],
             "sm_H_theory": jt["SM_pulls_theory"]["H"],
             "mssm_all": rows[("MSSM above M_S", "U+B+H")]["n_sigma"],
             "mssm_all_theory": rows[("MSSM above M_S", "U+B+H")]["with_theory"]["n_sigma"],
             "predictive_survivors": len(jt["predictive_survivors"])}
    # Parts N, O, P: masses, the strong CP angle, neutrinos
    mf, sc, nu = res["mass_formulas"], res["strong_cp"], res["neutrinos"]
    no, io = nu["orderings"]["NO"], nu["orderings"]["IO"]
    tm1 = [r for r in no["patterns"]["rows"] if r["pattern"].startswith("TM1")][0]
    best_tm1 = min(tm1["solutions"], key=lambda q: abs(q["delta_pull"]))
    beyond = {
        "koide_pole_sigma": mf["koide"][0]["n_sigma"], "koide_mz_sigma": mf["koide"][1]["n_sigma"],
        "koide_quark_sigma": min(r["n_sigma"] for r in mf["koide"][3:]),
        "theta_max": sc["bound"]["theta_max"], "theta_max_weakest": sc["bound"]["theta_max_weakest"],
        "mu_sigma": sc["massless_up"]["n_sigma"], "m_a_ueV": sc["axion"]["m_a_ueV_at_1e12"],
        "sum_no": no["sum_min"], "sum_io": io["sum_min"], "desi": P._comparison("sum_mnu_DESI")[0],
        "io_excluded": not io["vs_cosmology"]["sum_mnu_DESI"]["allowed"],
        "theta13_sigma": min(abs(r["pulls"]["s13sq"]) for r in no["patterns"]["rows"] if r["unknowns"] == 0),
        "tm1_s12": best_tm1["s12sq"], "tm1_s12_sigma": tm1["n_sigma"], "tm1_delta": best_tm1["delta_deg"],
        "seesaw_max": no["seesaw"]["M_max_perturbative"], "M_GUT": nu["M_GUT"],
    }
    data = {
        "beyond": beyond,
        "criticality": {
            "m_h_pred": cr["central"]["m_h"], "sigma": cr["sigma_total"], "m_h_meas": mh_meas,
            "m_h_tree": cr["tree_matching"]["m_h"],
            "m_h_lower_matching": cr["row"]["3L/three loops"]["m_h"],
            "one_loop_running": [r["m_h"] for r in cr["rows"] if r["loops"] == 1][0],
            "double_m_h": cr["double"]["m_h"], "double_M_t": cr["double"]["M_t"], "M_t_meas": P.inp("M_t"),
            "lambda_MP": prof["lambda_MP"], "mu_zero": prof["mu_zero"], "M_P": mp, "curves": curves},
        "unification": {"M_S": m_s, "M_GUT": m_gut, "alpha_GUT_inv": 1 / au["M_S_for_measured_alpha"]["alpha_GUT"],
                        "sm": sm_line, "mssm": mssm_line,
                        "sm_only_inv_alpha": [r for r in au["rows"] if not math.isfinite(r["M_S"])][0]["loop2"]["inv_alpha"],
                        "meas_inv_alpha": au["measured_inv_alpha_MZ"]},
        "higgs_mssm": {"bound": hg["mh_upper_bound"], "tan_beta": max(hg["tan_betas"]),
                       "M_S": hg["M_S"], "curve": [[round(x, 4), round(m, 3)] for x, m in hg["xt_curve"]]},
        "tan_beta": {"btau": tb, "fixed_point": [r["tan_beta"] for r in yk["fixed_point_MSSM"]["runs"]]},
        "cosmology": {"age": float(res["cosmology"]["age_Gyr"]), "Omega_Lambda": float(res["cosmology"]["Omega_Lambda"])},
        "planck": qg["planck"],
        "checks": [len(res["checks"]), sum(1 for c in res["checks"] if c[1])],
        "texture": texture,
        "joint": joint,
    }
    path = os.path.join(ROOT, "assets", "site-data.js")
    with open(path, "w", encoding="utf-8") as f:
        f.write("// Generated by tools/site_data.py from production_v2_2.py. Do not edit.\n")
        f.write("window.SITE_DATA = " + json.dumps(data, separators=(",", ":"), default=float) + ";\n")
    print("wrote", path)


if __name__ == "__main__":
    main()
