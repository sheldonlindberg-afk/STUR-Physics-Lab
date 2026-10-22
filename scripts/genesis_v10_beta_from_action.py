#!/usr/bin/env python3
"""
================================================================================
GENESIS v10 -- beta from the STUR action, with nothing fitted
================================================================================
Stage 10 FITS kappa to the measured beta = 0.277 deg. Here beta is an OUTPUT:

  beta = c_g * alpha_em * Delta phi / (2 pi)

  c_g        photon anomaly coefficient of the R-phase rotation, from STUR's own
             fermion coupling (ALPHA_PARAMETER_DERIVATION.md, sec. 1.2):
               L_Y = -y (psibar_L R_1 psi_R + psibar_L R_2 gamma^5 psi_R + h.c.)
                   = -y |R| psibar exp(i gamma^5 phi) psi
             Removing exp(i gamma^5 theta) from each mass by the chiral rotation
             psi -> exp(-i gamma^5 theta/2) psi generates, through the ABJ anomaly,
               theta * N_c Q^2 (alpha/4pi) F Ftilde      per Dirac fermion,
             so c_g = sum_f N_c Q_f^2 over every fermion with this Yukawa.
             The same rotation gives the colour term 2 T(R) theta (alpha_s/8pi) G Gtilde.
  Delta phi  phase accrued by the R-field zero mode between recombination and
             today. Two STUR options:
               (i)  chronomagnetic rotation at omega = 2 pi^2 per unit ln t
                    (stur_chronomagnetics_omega.html; the only log-time rate in STUR)
               (ii) Master Action as written: phi_dot = Q/(v^2 a^3), Q an initial
                    condition (see genesis_v10_sturb_action_audit.py, Part A)

Polarisation angles are defined mod 180 deg, and C_l^EB ~ sin(4 beta) is periodic
mod 90 deg, so the prediction is reduced accordingly and also checked against the
B-mode power it would generate, C_l^BB = sin^2(2 beta) C_l^EE.

Usage:  python genesis_v10_beta_from_action.py
================================================================================
"""
from fractions import Fraction

import camb
import numpy as np

ALPHA = 1 / 137.035999
OMEGA = 2 * np.pi ** 2
OMEGA_TRIANGLE = 2 * np.pi / np.log(3722 / 2705)
BETA_OBS, S_BETA_OBS = 0.277, 0.057          # deg, as used by the pre-registration
COSMO = dict(H0=67.36, ombh2=0.02237, omch2=0.1200, mnu=0.06, tau=0.0544, As=2.1e-9, ns=0.9649)

gates = []


def gate(name, ok, detail):
    gates.append(bool(ok))
    print(f"  gate: {name:54s} {detail:34s} {'PASS' if ok else 'FAIL'}")


def header(s):
    print("\n" + "=" * 80 + "\n  " + s + "\n" + "=" * 80)


# ------------------------------------------------------------------------------
# 1. anomaly coefficients from the STUR fermion content
# ------------------------------------------------------------------------------
# one SM generation, as Dirac fermions with the chiral R-Yukawa (neutrinos have Q = 0)
GEN = [("u", 3, Fraction(2, 3)), ("d", 3, Fraction(-1, 3)), ("e", 1, Fraction(-1)),
       ("nu", 1, Fraction(0))]


def anomaly(content, ngen=3):
    cg = sum(nc * q * q for _, nc, q in content) * ngen
    cs = sum(Fraction(1, 2) for _, nc, _ in content if nc == 3) * ngen   # T(fund) = 1/2
    return cg, cs


def part1():
    header("1. Photon anomaly coefficient c_g of the R-phase (chiral) rotation")
    cg, cs = anomaly(GEN)
    print("  per generation: u 3(2/3)^2 = 4/3, d 3(1/3)^2 = 1/3, e 1, nu 0  ->  8/3")
    print(f"  three generations:  c_g = {cg}   (= 8; the DFSZ-like value E = 8)")
    print(f"  colour coefficient: c_s = sum T(R) = {cs}  -> theta_QCD,eff = 2 c_s phi = {2 * cs} phi")
    gate("c_g = 8 for the full STUR (= SM) charged spectrum", cg == 8, f"c_g = {cg}")
    # cross-check the normalisation on a single Dirac lepton: L = theta (alpha/4pi) F Ftilde,
    # and the rotation formula beta = (g/2) Delta theta for L = (g/4) theta F Ftilde
    g_unit = ALPHA / np.pi
    gate("beta per unit c_g per radian = alpha/2pi", abs(g_unit / 2 - ALPHA / (2 * np.pi)) < 1e-15,
         f"{np.degrees(ALPHA / (2 * np.pi)):.5f} deg")
    variants = {
        "full spectrum (STUR Yukawa, 3 gen)": (Fraction(8), Fraction(3)),
        "leptons only (3 gen)": (Fraction(3), Fraction(0)),
        "one generation": (Fraction(8, 3), Fraction(1)),
        "one charged lepton": (Fraction(1), Fraction(0)),
    }
    return variants


# ------------------------------------------------------------------------------
# 2. phase accrued since recombination, smeared over the visibility function
# ------------------------------------------------------------------------------
def part2():
    header("2. Delta phi since recombination (no fitting)")
    res = camb.get_results(camb.set_params(**COSMO))
    t0 = res.physical_time(0.0)
    zs = res.get_derived_params()['zstar']
    tstar = res.physical_time(zs)
    eta = np.linspace(150, 600, 2001)
    vis = res.get_background_time_evolution(eta, ['visibility'])['visibility']
    z = res.redshift_at_conformal_time(eta)
    t = np.array([res.physical_time(zz) for zz in z])
    w = vis / np.sum(vis)
    lnt = np.log(t0 / t)
    print(f"  t0 = {t0:.4f} Gyr, t(z* = {zs:.1f}) = {tstar * 1e6:.1f} kyr, ln(t0/t*) = {np.log(t0 / tstar):.4f}")
    print(f"  visibility-weighted ln(t0/t): mean {np.sum(w * lnt):.4f}, rms spread {np.sqrt(np.sum(w * (lnt - np.sum(w * lnt)) ** 2)):.4f}")
    print(f"  (i)  chronomagnetic rotation, omega = 2 pi^2: Delta phi = {OMEGA * np.log(t0 / tstar):.2f} rad")
    print("  (ii) Master Action as written: Delta phi = (Q/v^2) int a^-3 dt, Q an initial condition -> no prediction")
    return lnt, w, t0, tstar


# ------------------------------------------------------------------------------
# 3. predicted beta and the observables it implies
# ------------------------------------------------------------------------------
def part3(variants, lnt, w, t0, tstar):
    header("3. Predicted beta (omega = 2 pi^2, no free parameter) vs observation")
    print(f"  observed: beta = {BETA_OBS} +/- {S_BETA_OBS} deg (EB, mod 90 deg); C_BB/C_EE at l ~ 100-1000"
          " is consistent with lensing (~1% or less)\n")
    print(f"  {'fermion content':36s} {'c_g':>5s} {'beta (raw)':>11s} {'mod 180':>8s} {'EB angle':>9s}"
          f" {'C_BB/C_EE':>9s} {'pol. frac':>9s} {'tension':>8s}")
    out = {}
    for name, (cg, cs) in variants.items():
        kap = float(cg) * ALPHA * OMEGA / (2 * np.pi)            # rad per unit ln t
        b = kap * lnt                                            # rotation of each emission time
        z2 = np.sum(w * np.exp(2j * b))                          # visibility-averaged e^{2 i beta}
        beta_eff = np.degrees(np.angle(z2) / 2)
        pol = abs(z2)                                            # depolarisation from the spread
        b180 = beta_eff % 180
        b90 = ((beta_eff + 45) % 90) - 45                        # what an EB estimator returns
        bb_ee = np.sin(2 * np.radians(b180)) ** 2
        tens = abs(b90 - BETA_OBS) / S_BETA_OBS
        raw = np.degrees(kap * np.log(t0 / tstar))
        out[name] = dict(c_g=float(cg), beta_raw=raw, beta_eb=b90, bb_ee=bb_ee, tension=tens,
                         theta_qcd_shift=2 * float(cs) * OMEGA * np.log(t0 / tstar))
        print(f"  {name:36s} {str(cg):>5s} {raw:10.2f}° {b180:7.2f}° {b90:8.2f}° {bb_ee:9.3f}"
              f" {pol:9.3f} {tens:7.0f}σ")
    need = 2 * np.pi * np.radians(BETA_OBS) / ALPHA
    print(f"\n  to obtain beta = {BETA_OBS} deg one needs c_g * Delta phi = {need:.3f} rad")
    for name, (cg, _) in variants.items():
        w_needed = need / float(cg) / np.log(t0 / tstar)
        print(f"    {name:36s} omega_eff = {w_needed:.4f} per unit ln t  (= omega / {OMEGA / w_needed:.0f})")
    full = out["full spectrum (STUR Yukawa, 3 gen)"]
    gate("full-spectrum prediction agrees with observed beta (< 3 sigma)", full['tension'] < 3,
         f"{full['beta_eb']:.2f}° vs {BETA_OBS}°")
    gate("implied C_BB/C_EE below 1% (BICEP/Keck, SPT)", full['bb_ee'] < 0.01, f"{full['bb_ee']:.3f}")
    print(f"\n  colour anomaly (full spectrum): theta_QCD shifts by 2 c_s Delta phi = {full['theta_qcd_shift']:.0f} rad"
          " since recombination;\n  the neutron EDM requires |theta| < 1e-10, and STUR itself predicts no axion.")
    gate("no rolling theta_QCD (c_s = 0 needed)", full['theta_qcd_shift'] == 0,
         f"Delta theta = {full['theta_qcd_shift']:.0f} rad")
    return out


def main():
    variants = part1()
    lnt, w, t0, tstar = part2()
    part3(variants, lnt, w, t0, tstar)
    header("VERDICT")
    print("""  With STUR's own ingredients and nothing fitted -- the chiral R-Yukawa of every charged
  fermion (c_g = 8) and the chronomagnetic log-time rate omega = 2 pi^2 -- the predicted
  birefringence is ~110 deg (EB-equivalent ~ 20 deg), with C_BB ~ 0.4 C_EE. Observation
  gives 0.277 +/- 0.057 deg and C_BB/C_EE < ~1%. The derived prediction is excluded by
  existing data by hundreds of sigma; the same rotation would also roll theta_QCD.
  Even the smallest STUR-compatible coupling (one charged lepton, c_g = 1) overshoots ~50x.
  The Master Action as written (option ii) leaves Delta phi to an initial condition, so it
  makes no beta prediction at all.  Matching 0.277 deg needs the phase to rotate ~400x
  slower than omega (c_g = 8), with no mechanism for that in the repo.""")
    print(f"\n  gates: {sum(gates)}/{len(gates)} passed (the FAILs are the result, not a code error)")


if __name__ == "__main__":
    main()
