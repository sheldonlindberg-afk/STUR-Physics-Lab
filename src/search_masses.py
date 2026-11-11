#!/usr/bin/env python3
"""
Unifying-equation search, front 8: masses.  Start with the most precise unexplained mass
relation, Koide's formula (KNOWN, Koide 1982):

    Q = (m_e + m_mu + m_tau) / (sqrt m_e + sqrt m_mu + sqrt m_tau)^2 = 2/3

Equivalent Z3 form (KNOWN, Brannen 2006):
    sqrt m_k = M (1 + A cos(delta + 2 pi k / 3)),  k = 0, 1, 2,   Q = (1 + A^2/2)/3,
so Q = 2/3  <=>  A = sqrt 2.  The 2 pi/3 is a Z3 over GENERATIONS; front 7 tied N_g to N_c = 3.

Inputs (LIT): m_tau = 1776.93 +- 0.09 MeV (PDG live, retrieved);
m_e = 0.51099895000 MeV, m_mu = 105.6583755 MeV (CODATA 2018 / PDG, recalled; their
uncertainties are negligible here).  Quark masses (PDG, recalled; MS-bar, mixed scales -
illustrative only): u 2.16, d 4.70, s 93.5, c 1273, b 4183, t 172570 MeV.
"""
import numpy as np
from scipy.optimize import brentq

me, mmu = 0.51099895000, 105.6583755
mtau, dmtau = 1776.93, 0.09


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


def Q(m):
    m = np.asarray(m, float)
    return m.sum() / np.sqrt(m).sum() ** 2


def brannen(m):
    """Fit sqrt m_k = M (1 + A cos(delta + 2 pi k/3)) exactly (3 equations, 3 unknowns)."""
    r = np.sqrt(np.asarray(m, float))
    M = r.mean()
    c = (r / M - 1)                                           # = A cos(delta + 2 pi k/3)
    z = np.sum(c * np.exp(-1j * 2 * np.pi * np.arange(3) / 3)) * 2 / 3
    return M, abs(z), np.angle(z)


def main():
    banner("K1  Koide's relation for the charged leptons")
    q = Q([me, mmu, mtau])
    dq = (Q([me, mmu, mtau + dmtau]) - Q([me, mmu, mtau - dmtau])) / 2
    print(f"   Q = {q:.8f}   2/3 = {2/3:.8f}   Q - 2/3 = {q - 2/3:+.2e} +- {abs(dq):.1e}"
          f"  ({(q - 2/3)/abs(dq):+.2f} sigma)")
    mt_pred = brentq(lambda x: Q([me, mmu, x]) - 2 / 3, 1000, 3000)
    print(f"   Koide prediction m_tau = {mt_pred:.3f} MeV   measured {mtau} +- {dmtau}"
          f"  ->  {(mtau - mt_pred)/dmtau:+.2f} sigma")

    banner("K2  Z3 (Brannen) form: amplitude and phase")
    M, A, d = brannen([me, mmu, mtau])
    print(f"   M = {M:.5f} sqrt(MeV)   A = {A:.6f}  (sqrt 2 = {np.sqrt(2):.6f})   delta = {d:.6f} rad")
    dd = abs(brannen([me, mmu, mtau + dmtau])[2] - d)
    dr = d % (2 * np.pi / 3)                                   # relabelling generations shifts delta by 2pi/3
    print(f"   delta mod 2pi/3 = {dr:.7f} +- {dd:.1e}   2/9 = {2/9:.7f}   difference = {dr - 2/9:+.1e}"
          f"  ({(dr - 2/9)/dd:+.2f} sigma)")
    print("   (2/9 for delta is an empirical observation (Brannen); there is no derivation of it here.)")
    banner("K2b  Zero-parameter ratios from A = sqrt 2, delta = 2/9 (only the overall scale free)")
    k = np.arange(3)
    r = (1 + np.sqrt(2) * np.cos(2 / 9 + 2 * np.pi * k / 3)) ** 2
    r = np.sort(r)
    pe_mu, pt_mu = r[1] / r[0], r[2] / r[1]
    print(f"   m_mu/m_e  predicted {pe_mu:.6f}   measured {mmu/me:.6f}   rel. diff {pe_mu/(mmu/me) - 1:+.1e}")
    print(f"   m_tau/m_mu predicted {pt_mu:.6f}   measured {mtau/mmu:.6f} +- {dmtau/mmu:.6f}"
          f"   ({(pt_mu - mtau/mmu)/(dmtau/mmu):+.2f} sigma)")
    print("   (m_mu/m_e is measured to ~1e-8 relative; the m_e, m_mu inputs are recalled CODATA values.)")

    banner("K2c  Assume Koide exact (A = sqrt 2): what delta do m_e, m_mu alone require?")
    def ratio(dl):
        rr = np.sort((1 + np.sqrt(2) * np.cos(dl + 2 * np.pi * np.arange(3) / 3)) ** 2)
        return rr[1] / rr[0]
    target = mmu / me
    dK = brentq(lambda dl: ratio(dl) - target, 0.20, 0.24)
    rel = 2.2e-8                                              # m_mu/m_e relative uncertainty (CODATA, recalled)
    sens = (ratio(dK + 1e-7) - ratio(dK - 1e-7)) / 2e-7 / target
    sd = rel / abs(sens)
    print(f"   delta_K = {dK:.9f}   (precision {sd:.1e} from m_mu/m_e)   2/9 = {2/9:.9f}")
    print(f"   delta_K - 2/9 = {dK - 2/9:+.2e}  =  {(dK - 2/9)/sd:+.0f} sigma")
    mt = (1 + np.sqrt(2) * np.cos(dK + 2 * np.pi * np.arange(3) / 3)) ** 2
    mt = np.sort(mt); mt_pred = mt[2] / mt[0] * me
    print(f"   -> with Koide exact, m_tau = {mt_pred:.3f} MeV (measured {mtau} +- {dmtau}: "
          f"{(mtau - mt_pred)/dmtau:+.2f} sigma)")
    print("   VERDICT: Koide (A = sqrt 2) fits all data at 0.4 sigma; 'delta = 2/9' is only approximate -")
    print(f"   it misses by {abs(dK - 2/9):.1e}, {abs(dK - 2/9)/sd:.0f} standard deviations of the m_mu/m_e precision")
    print("   (that precision uses the recalled CODATA m_mu/m_e uncertainty, 2.2e-8 relative).")

    banner("K3  Same formula on quarks (illustrative: mixed schemes and scales)")
    for name, trip in [("u, c, t", [2.16, 1273, 172570]), ("d, s, b", [4.70, 93.5, 4183]),
                       ("s, c, b", [93.5, 1273, 4183])]:
        qq = Q(trip)
        print(f"   ({name}):  Q = {qq:.4f}   (2/3 = 0.6667)")
    print("   -> holds only for charged leptons (quark masses run with scale, so a scale-free")
    print("      quark version is not even well defined).")

    banner("K4  How surprising is the lepton result?  (hostile check)")
    rng = np.random.default_rng(0)
    lo, hi = np.log(mmu), np.log(1e4)
    x = np.exp(rng.uniform(lo, hi, 2_000_000))
    qs = (me + mmu + x) / (np.sqrt(me) + np.sqrt(mmu) + np.sqrt(x)) ** 2
    obs = abs(q - 2 / 3)
    p = np.mean(np.abs(qs - 2 / 3) <= max(obs, abs(dq)))
    print(f"   m_tau log-uniform in [m_mu, 10 GeV]: P(|Q - 2/3| <= {max(obs, abs(dq)):.1e}) = {p:.1e}")
    print("   Trials factor (how many 'nice' formulas and fractions people tried) is unknown;")
    for N in [100, 1000, 10000]:
        print(f"     with {N:5d} independent tries: chance of one such hit = {1 - (1 - p)**N:.1%}")
    print("   -> suggestive, not proof.")
    print("   Theory status: Koide is NOT derived from any accepted framework; masses run with")
    print("   scale, and Q = 2/3 holds for POLE masses only - a puzzle for any field-theory origin.")


if __name__ == "__main__":
    main()
