#!/usr/bin/env python3
"""
================================================================================
GENESIS v10 -- Stage 10d: field-normalisation constraints on STUR-B and STUR-M3a
================================================================================
Both birefringence hypotheses are written in terms of the dimensionless R-phase
theta. The physical field is a = f theta, and f controls everything else the
field does. This stage asks whether any f is allowed.

STUR does not fix f. The repo gives two incompatible R-field VEVs:
  v = 3/L_X with L_X = 0.8 um (ABSOLUTE_MASS_DERIVATION.md 582)  ->  ~0.74 eV
  v_R ~ M_GUT ~ 2e16 GeV            (COMPLETE_CORRECTIONS_AND_RESOLUTIONS.md 169)
so f is treated as free and both repo values are marked.

Hypotheses (rates per unit ln t; c_g photon anomaly coefficient):
  STUR-B (c_g = 8)    rotating, theta_dot = w_eff/t, w_eff = omega/399 (needed for 0.277 deg)
  STUR-B (c_g = 0.02) rotating at omega = 2 pi^2 (the coupling the fit requires)
  STUR-M3a            theta = A0 sin(omega ln t + delta), c_g = 3, leptons only,
                      A0 = 1.435-2.931 rad (Stage 10c registration)

Constraints, each as a function of f:
  (a) energy density   rho = f^2 W^2 / (2 t^2), W = w_eff (B) or A0 omega (M3a)
                       [M3a: kinetic + restoring potential, phase-independent].
                       Omega = (3/8) W^2 f^2/M^2 (matter era), (2/3) W^2 f^2/M^2 (radiation era)
                       vs early-dark-energy-type fractions: <~ 1% for z ~ 100-1000 and
                       <~ 2.6% in the radiation era (arXiv:2107.11065, 2 sigma).
  (b) photon coupling  g = c_g alpha/(pi f): CAST g < 0.66e-10 /GeV (95%, m < 0.02 eV,
                       arXiv:1705.02290); Chandra NGC 1275 / H1821+643 g < 6.3-8.0e-13 /GeV
                       (99.7%, m <~ 1e-12 eV; Reynolds et al. 2020). The field is ultralight
                       today (m ~ omega/t0 ~ 1e-32 eV), so both apply to the coupling.
  (c) lepton derivative coupling (M3a; also B with c_g = 8): the chiral rotation leaves
                       (d_mu theta)/2 psibar gamma^mu gamma^5 psi, a CPT-odd b_0 = theta_dot/2,
                       independent of f.
  (d) anisotropic birefringence: a field light during inflation has delta a = H_I/2pi, so
                       delta beta = g H_I/(4 pi) and L(L+1)C_L/2pi = (g H_I/4pi)^2 [rad^2].
                       ACT DR6 (arXiv:2608.27458): A_CB < 0.15e-4 rad^2 (95%), quoted there as
                       g < 4.9e-2/H_I (consistency checked below). SPT-3G B-modes:
                       A_CB < 1.2e-4 (0.53e-4 with a lensing prior; arXiv:2510.07928).
                       H_I from the GENESIS r = 0.0035. For M3a, the restoring term that
                       makes it oscillate (~ omega H) would make it heavy during inflation,
                       which removes these fluctuations; both cases are reported.
  (e) colour anomaly   c_s != 0 makes theta_QCD = 2 c_s theta roll by O(1) rad since
                       recombination, for any f (STUR-B with c_g = 8 has c_s = 3).

Usage:  python genesis_v10d_field_constraints.py
================================================================================
"""
import numpy as np

M_RED = 2.435e18                  # reduced Planck mass [GeV]
ALPHA = 1 / 137.035999
OMEGA = 2 * np.pi ** 2
AS, R_GENESIS = 2.1e-9, 0.0035
HBAR_GEV_S = 6.582119569e-25
T0_S = 13.797 * 3.15576e16
LN_T0_TSTAR = 10.5217
NEED = 4.163                      # c_g * Delta phi [rad] needed for beta = 0.277 deg

OMEGA_EDE_MATTER, OMEGA_EDE_RAD = 0.01, 0.026
G_CAST, G_NGC1275 = 0.66e-10, 8.0e-13
ACB_ACT, ACB_SPT = 0.15e-4, 1.2e-4
F_REPO = {"v = 3/L_X, L_X = 0.8 um": 0.74e-9, "v_R ~ M_GUT": 2e16}

gates = []


def gate(name, ok, detail):
    gates.append(bool(ok))
    print(f"  gate: {name:54s} {detail:34s} {'PASS' if ok else 'FAIL'}")


HYP = {
    "STUR-B (c_g = 8, w_eff = omega/399)": dict(cg=8, cs=3, W=[NEED / 8 / LN_T0_TSTAR], light_inflation=[True]),
    "STUR-B (c_g = 0.02, rate omega)": dict(cg=NEED / (OMEGA * LN_T0_TSTAR), cs=0, W=[OMEGA], light_inflation=[True]),
    "STUR-M3a (c_g = 3, leptons)": dict(cg=3, cs=0, W=[1.435 * OMEGA, 2.931 * OMEGA], light_inflation=[True, False]),
}


def main():
    H_I = np.pi * M_RED * np.sqrt(R_GENESIS * AS / 2)
    print("\n=== Stage 10d: field-normalisation constraints ===")
    print(f"  H_I from r = {R_GENESIS}: {H_I:.3e} GeV")
    gate("H_I reproduces r = 2 H^2/(pi^2 M^2 A_s)", abs(2 * H_I ** 2 / (np.pi ** 2 * M_RED ** 2 * AS) - R_GENESIS) < 1e-12,
         f"r = {2 * H_I ** 2 / (np.pi ** 2 * M_RED ** 2 * AS):.4f}")
    gate("ACT A_CB < 0.15e-4 <=> g < 4.9e-2/H_I (units check)",
         abs((4.9e-2 / (4 * np.pi)) ** 2 / ACB_ACT - 1) < 0.02, f"(4.9e-2/4pi)^2 = {(4.9e-2 / (4 * np.pi)) ** 2:.3e}")

    report = {}
    for name, h in HYP.items():
        cg = h['cg']
        print(f"\n  --- {name}:  c_g = {cg:.4g}, c_s = {h['cs']}")
        # (a) energy density -> upper bound on f (strongest of matter / radiation era)
        f_up = []
        for W in h['W']:
            fm = M_RED * np.sqrt(OMEGA_EDE_MATTER / (3 / 8)) / W
            fr = M_RED * np.sqrt(OMEGA_EDE_RAD / (2 / 3)) / W
            f_up.append(min(fm, fr))
        # (b) photon coupling -> lower bounds
        f_cast = cg * ALPHA / (np.pi * G_CAST)
        f_ngc = cg * ALPHA / (np.pi * G_NGC1275)
        # (d) anisotropy (light during inflation) -> lower bound
        f_act = cg * ALPHA * H_I / (np.pi * 4 * np.pi * np.sqrt(ACB_ACT))
        f_spt = cg * ALPHA * H_I / (np.pi * 4 * np.pi * np.sqrt(ACB_SPT))
        # (c) lepton CPT-odd b_0 (f-independent)
        b0 = max(h['W']) / T0_S * HBAR_GEV_S / 2
        print(f"    (a) energy density:     f < {min(f_up):.2e} - {max(f_up):.2e} GeV")
        print(f"    (b) CAST:               f > {f_cast:.2e} GeV;  NGC 1275 (99.7%): f > {f_ngc:.2e} GeV")
        print(f"    (c) lepton b_0 = theta_dot/2 <= {b0:.1e} GeV today (f-independent)")
        print(f"    (d) anisotropic beta:   ACT DR6 f > {f_act:.2e} GeV; SPT-3G f > {f_spt:.2e} GeV"
              " (if light during inflation)")
        if h['cs']:
            dth = 2 * h['cs'] * NEED / cg
            print(f"    (e) colour anomaly:     theta_QCD rolls by {dth:.1f} rad since recombination -> EXCLUDED for every f")
        lo_light = max(f_ngc, f_act)
        lo_heavy = f_ngc
        up = min(f_up)
        cases = {}
        for light in h['light_inflation']:
            lo = lo_light if light else lo_heavy
            ok = (lo < up) and not h['cs']
            cases["light" if light else "heavy"] = (lo, up, ok)
            tag = "light during inflation" if light else "heavy during inflation"
            win = f"[{lo:.1e}, {up:.1e}] GeV" if ok else "NONE"
            print(f"    allowed f ({tag}): {win}")
        for lab, fv in F_REPO.items():
            om = (3 / 8) * max(h['W']) ** 2 * (fv / M_RED) ** 2
            g = cg * ALPHA / (np.pi * fv)
            print(f"    repo value {lab:24s} f = {fv:.2e} GeV: Omega = {om:.2e}, g = {g:.1e} /GeV")
        report[name] = cases
    print("\n  SUMMARY")
    for name, cases in report.items():
        for k, (lo, up, ok) in cases.items():
            print(f"    {name:38s} [{k:5s}] " + (f"f in [{lo:.1e}, {up:.1e}] GeV" if ok else "no allowed f"))
    m3 = report["STUR-M3a (c_g = 3, leptons)"]
    gate("STUR-M3a has an allowed f window (light case)", m3["light"][2], "window exists" if m3["light"][2] else "none")
    gate("colour anomaly excludes STUR-B c_g = 8 for every f", not report["STUR-B (c_g = 8, w_eff = omega/399)"]["light"][2],
         "excluded for every f")
    print(f"\n  gates: {sum(gates)}/{len(gates)} passed (a FAIL here is a physics result)")


if __name__ == "__main__":
    main()
