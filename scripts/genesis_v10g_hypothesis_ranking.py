#!/usr/bin/env python3
"""
================================================================================
GENESIS v10 -- Stage 10g: which birefringence hypothesis fits the math best?
================================================================================
Ranks every candidate on equal terms, using only results computed elsewhere in
the repo plus the one new calculation needed here (C0's viability).

Candidates
  H0      STUR as written. Either reading of the R-Yukawa gives beta ~ 0:
            reading A (fermions chirally R-charged): c_g = 8, c_s = 3, the phase
              is a QCD axion, pinned by QCD (m >> H) -> no slow rotation;
            reading B (theta only relocalises fermions, the exact flat direction
              found in genesis_v10f_theory_gaps.py): no chiral rotation -> c_g = 0.
  C0      Master Action's own U(1) dynamics: a freely rotating, massless phase
          with a conserved Noether charge Q (theta_dot = q/a^3). No new terms.
  STUR-B  pre-registered (Stage 10, 10b): log-time rotation.
  M3a     pre-registered (Stage 10c, 10c2): log-time oscillation.
Every beta != 0 candidate needs c_s = 0 (else it is a QCD axion, pinned) with
c_g != 0, i.e. chirally R-charged leptons but R-neutral quarks, which conflicts
with the repo's quark localisation (genesis_v10f_theory_gaps.py (b)), and needs
the pinned Higgs cos(3 theta) potential to be absent (genesis_v10f (a)).

New calculation: C0 with c_g = 3 (leptons only), normalised so the
visibility-weighted rotation equals beta_now:
  * upper bound on f: kinetic energy rho = f^2 q^2 / (2 a^6) at BBN, as Delta N_eff
  * lower bounds on f: anisotropic birefringence (massless during inflation,
    delta theta = H_I/2 pi f, ACT DR6 A_CB) and the photon coupling (NGC 1275).
  C0 is viable only if the window is non-empty.

Usage:  python genesis_v10g_hypothesis_ranking.py
================================================================================
"""
import camb
import numpy as np

HBAR_EV_S = 6.582119569e-16
GEV = 1e9
ALPHA = 1 / 137.035999
COSMO = dict(H0=67.36, ombh2=0.02237, omch2=0.1200, mnu=0.06, tau=0.0544, As=2.1e-9, ns=0.9649)

BETA_INPUTS = {   # deg; see GENESIS_V10_BIREFRINGENCE_PAPER_DRAFT.md sec. 1
    "ACT+Planck joint (arXiv:2608.06480)": (0.277, 0.057),
    "same, dust-mitigated (excludes 0 at 3.5 sigma)": (0.277, 0.277 / 3.5),
    "ACT DR6 alone (arXiv:2509.13654)": (0.215, 0.074),
}
# bounds used (as in genesis_v10d_field_constraints.py; caveats there)
A_CB_MAX = 0.15e-4          # rad^2, ACT DR6 95% (unit convention inferred, see v10d doc)
G_AGG_MAX = 6.3e-13         # GeV^-1, Chandra NGC 1275 (99.7%, B-field-model dependent)
H_INF = 1.47e13             # GeV, from r = 0.0035 (GENESIS R^2)
DNEFF_MAX = 0.3             # BBN-era Delta N_eff (rough; label as such)
T_BBN = 1e-3                # GeV
GSTAR_BBN = 10.75

gates = []


def gate(name, ok, detail):
    gates.append(bool(ok))
    print(f"  gate: {name:54s} {detail:34s} {'PASS' if ok else 'FAIL'}")


def header(s):
    print("\n" + "=" * 80 + "\n  " + s + "\n" + "=" * 80)


def c0_window(c_g=3.0, beta_deg=0.277):
    """f window [GeV] for C0 with photon coefficient c_g, normalised to beta_deg"""
    res = camb.get_results(camb.set_params(**COSMO))
    t0 = res.physical_time(0.0) * 3.15576e16                    # s
    # I(t) = int_t^t0 a^-3 dt  on a fine ln a grid
    lna = np.linspace(np.log(1e-4), 0.0, 40001)
    z = np.exp(-lna) - 1
    H = np.array([res.hubble_parameter(zz) for zz in z[::200]])   # km/s/Mpc
    H = np.interp(lna, lna[::200], H) * 1e3 / 3.0856776e22        # s^-1
    a = np.exp(lna)
    dt = 1 / H                                                    # dt/dlna
    integrand = a ** -3 * dt
    I_from = np.concatenate([[0.0], np.cumsum(0.5 * (integrand[1:] + integrand[:-1]) * np.diff(lna))])
    I_to_today = I_from[-1] - I_from                             # int_t^t0 a^-3 dt
    # visibility weighting at recombination
    eta = np.linspace(150, 600, 1801)
    vis = res.get_background_time_evolution(eta, ['visibility'])['visibility']
    zv = res.redshift_at_conformal_time(eta)
    Iv = np.interp(-np.log1p(zv), lna, I_to_today)
    I_eff = np.sum(vis * Iv) / np.sum(vis)
    K = c_g * ALPHA / (2 * np.pi)
    dtheta = np.radians(beta_deg) / K                            # rad, needed after emission
    q = dtheta / I_eff                                           # theta_dot = q / a^3 [s^-1]
    # spread of the rotation across the visibility window (l-dependence proxy)
    spread = np.sqrt(np.sum(vis * (Iv - I_eff) ** 2) / np.sum(vis)) / I_eff
    # BBN: a at T_BBN
    a_bbn = (2.348e-13 / T_BBN) * (3.91 / GSTAR_BBN) ** (1 / 3)
    thdot_bbn = q / a_bbn ** 3 * HBAR_EV_S / GEV                  # GeV
    rho_nu1 = (7 / 4) * (np.pi ** 2 / 30) * T_BBN ** 4             # one neutrino species, GeV^4
    f_max_bbn = np.sqrt(2 * DNEFF_MAX * rho_nu1) / thdot_bbn       # rho = f^2 thdot^2 / 2
    f_min_aniso = K * H_INF / (2 * np.pi * np.sqrt(A_CB_MAX))
    f_min_gag = c_g * ALPHA / (np.pi * G_AGG_MAX)
    return dict(dtheta=dtheta, I_eff=I_eff, spread=spread, f_max_bbn=f_max_bbn,
                f_min_aniso=f_min_aniso, f_min_gag=f_min_gag, t0=t0)


def main():
    header("1. Data: tension of H0 (beta = 0) with each beta input")
    tens = {}
    for k, (b, s) in BETA_INPUTS.items():
        tens[k] = b / s
        print(f"  {k:50s} {b:.3f} +/- {s:.3f} deg -> beta = 0 is {b / s:.1f} sigma off")
    print("  STUR-B, M3a and C0 each fit beta_now exactly by construction (one amplitude fitted).")

    header("2. C0: freely rotating massless R-phase (Master Action U(1) dynamics), c_g = 3")
    w = c0_window()
    print(f"  rotation needed after last scattering: Delta theta = {w['dtheta']:.3f} rad (natural, O(1))")
    print(f"  rotation spread across the visibility window: {100 * w['spread']:.0f}% (rotation is early-weighted)")
    print(f"  f upper bound (BBN Delta N_eff < {DNEFF_MAX}, kinetic energy ~ a^-6): f < {w['f_max_bbn']:.2e} GeV")
    print(f"  f lower bound, anisotropic birefringence (massless during inflation): f > {w['f_min_aniso']:.2e} GeV")
    print(f"  f lower bound, photon coupling (NGC 1275):                        f > {w['f_min_gag']:.2e} GeV")
    fmin = max(w['f_min_aniso'], w['f_min_gag'])
    viable = w['f_max_bbn'] > fmin
    print(f"  => window: {'[%.2e, %.2e] GeV' % (fmin, w['f_max_bbn']) if viable else 'EMPTY'}"
          f"  (gap factor {w['f_max_bbn'] / fmin:.1e})")
    gate("C0 has a viable f window", viable, f"f_max/f_min = {w['f_max_bbn'] / fmin:.1e}")
    # robustness: does any reasonable change rescue it?
    w8 = c0_window(c_g=8.0)
    print(f"  (c_g = 8 instead: f_max/f_min = {w8['f_max_bbn'] / max(w8['f_min_aniso'], w8['f_min_gag']):.1e};"
          " but c_g = 8 implies c_s = 3, a QCD axion)")
    gap_needed = fmin / w['f_max_bbn']
    print(f"  to open the window, H_I would have to be {gap_needed:.1e}x lower, i.e. r ~ {0.0035 / gap_needed ** 2:.1e}"
          " (not GENESIS), or the phase heavy during inflation (needs a potential C0 does not have)")

    header("3. Ranking (assumptions beyond the STUR Master Action, with evidence)")
    rows = [
        ("H0  STUR as written (beta ~ 0)", "none",
         "0 params", f"disfavoured {tens['same, dust-mitigated (excludes 0 at 3.5 sigma)']:.1f}-"
                     f"{tens['ACT+Planck joint (arXiv:2608.06480)']:.1f} sigma ({tens['ACT DR6 alone (arXiv:2509.13654)']:.1f} sigma ACT-only)",
         "consistent with STUR; inconsistent with the measured beta"),
        ("C0  free Noether-charge rotation", "c_s = 0 with leptons R-charged; no pinned Higgs cos 3 theta",
         "1 (Q)", "fits", "EXCLUDED: BBN vs anisotropic birefringence leave no f window" if not viable else "viable"),
        ("M3a log-time oscillation", "c_s = 0 (leptons only); no pinned Higgs cos 3 theta; H^2-scaled restoring force (xi T-type, U(1)-breaking)",
         "2 (A0, delta)", "fits", "viable for f = 2.1e12-6.9e15 GeV; natural O(1) amplitude"),
        ("STUR-B log-time rotation", "c_s = 0; no pinned Higgs cos 3 theta; xi T |R|^2 with unpinned |R| ~ t^-1/2; ~150x suppression with no mechanism (c_g = 3 forced by c_s = 0 needs omega_eff ~ omega/150; or a non-anomalous c_g ~ 0.02)",
         "1 (kappa)", "fits", "viable only with c_g ~ 0.02 (f = 1.4e10-2.0e16 GeV); c_g = 8 excluded"),
    ]
    for name, extra, npar, data, verdict in rows:
        print(f"\n  {name}\n    extra assumptions: {extra}\n    free parameters:   {npar}\n"
              f"    data:              {data}\n    verdict:           {verdict}")

    header("VERDICT")
    print(f"""  * The hypothesis that fits STUR's own math best is H0: no isotropic birefringence.
    It needs no assumption beyond the action, but the measured beta disfavours it at
    {tens['same, dust-mitigated (excludes 0 at 3.5 sigma)']:.1f}-{tens['ACT+Planck joint (arXiv:2608.06480)']:.1f} sigma ({tens['ACT DR6 alone (arXiv:2509.13654)']:.1f} sigma from ACT alone).
  * The minimal beta != 0 extension (C0, the action's own rotation) is
    {'excluded: BBN and anisotropic birefringence leave no window' if not viable else 'viable'}.
  * Of the pre-registered hypotheses, M3a needs strictly fewer unexplained elements than
    STUR-B (STUR-B needs the same c_s = 0 and potential assumptions, an H^2 coupling, and
    in addition a ~150x suppression with no mechanism) and uses only O(1) numbers.
    M3a is therefore the better-fitting beta != 0 hypothesis, conditional on c_s = 0.
  * Decisive next data: whether beta != 0 survives (it decides H0 vs everything else).""")
    print(f"\n  gates: {sum(gates)}/{len(gates)} passed (a FAIL here is a physics result)")


if __name__ == "__main__":
    main()
