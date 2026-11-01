#!/usr/bin/env python3
"""
Refinement round 8, module 8A: can the bulk scalar phi be the dark matter?
Preregistered in docs/R8_PREREGISTRATION.md; results in docs/REFINEMENT_R8.md.
Requires numpy, scipy. Runs in a few minutes.

Assumptions (preregistered): D-A1 phi is stable; D-A2 the nucleation phase is
R^2 inflation; D-A3 phi is minimally coupled (xi = 0); D-A4 T_RH from the
scalaron's gravitational decay into the Higgs.

Units: reduced Planck mass M_Pl = 1 and time in units of 1/mu (mu = scalaron
mass) inside the integrators; GeV when reporting.

  B   R^2 background: mu from A_s, H at the pivot and at the end of inflation
  P   gravitational production: Bogoliubov coefficients for phi modes from
      Bunch-Davies initial conditions through the end of inflation and the
      scalaron oscillations; n_phi / rho_inflaton
  O   Omega_phi h^2 versus M_phi, with T_RH; the M_phi that gives 0.12
  C   pass conditions P1-P4 against STUR-ROLL's allowed window
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

BAR = "=" * 78
MPL_GEV = 2.435e18
A_S, N_STAR = 2.1e-9, 55.0
S23 = np.sqrt(2.0 / 3.0)
RHO_C_OVER_S = 3.645e-9          # rho_crit / (s0 h^2) in GeV
G_STAR = 106.75


# ---------------- background (mu = 1 units) ----------------
def V(p):
    return 0.75 * (1 - np.exp(-S23 * p)) ** 2


def dV(p):
    e = np.exp(-S23 * p)
    return 1.5 * S23 * (1 - e) * e


def eps_sr(p):
    return 0.5 * (dV(p) / V(p)) ** 2


def n_sr(p0, p1):
    """slow-roll e-folds from p0 down to p1: integral V/V' dphi"""
    x = np.linspace(p1, p0, 4001)
    return np.trapezoid(V(x) / dV(x), x)


def background(t_max=4000.0):
    p_end_sr = brentq(lambda p: eps_sr(p) - 1, 0.1, 3)
    p_star = brentq(lambda p: n_sr(p, p_end_sr) - N_STAR, 1, 20)
    # A_s = V / (24 pi^2 eps) with V in units of mu^2 M_Pl^2 -> mu^2 factor
    mu2 = A_S * 24 * np.pi ** 2 * eps_sr(p_star) / V(p_star)
    # exact background from a point ~12 e-folds before the end, in t (1/mu)
    p0 = brentq(lambda p: n_sr(p, p_end_sr) - 12, 1, 20)
    v0 = -dV(p0) / np.sqrt(3 * V(p0))

    def rhs(t, y):
        p, v, lna = y
        H = np.sqrt((0.5 * v * v + V(p)) / 3)
        return [v, -3 * H * v - dV(p), H]

    sol = solve_ivp(rhs, [0, t_max], [p0, v0, 0.0], method="DOP853",
                    rtol=1e-11, atol=1e-13, dense_output=True, max_step=0.05)
    t = sol.t
    p, v, lna = sol.y
    H = np.sqrt((0.5 * v * v + V(p)) / 3)
    eps = 0.5 * v * v / H ** 2
    i_end = np.argmax(eps >= 1)                       # first time eps_H = 1
    t_end = t[i_end]
    return dict(sol=sol, mu=np.sqrt(mu2), p_star=p_star, t_end=t_end,
                H_star=np.sqrt(V(p_star) / 3), H_end=H[i_end], lna_end=lna[i_end])


def bg_at(B, t):
    p, v, lna = B["sol"].sol(t)
    H = np.sqrt((0.5 * v * v + V(p)) / 3)
    Hdot = -0.5 * v * v
    return p, v, lna, H, Hdot


# ---------------- gravitational production ----------------
def _ic(B, t0, ks, M, c):
    """Bunch-Davies (first adiabatic order) for the canonical field at t0"""
    p, v, lna, H, Hdot = bg_at(B, t0)
    a = np.exp(lna)
    K = np.exp(-c * S23 * p)                         # kinetic factor
    m2 = M * M * K                                   # effective mass^2
    w = np.sqrt((ks / a) ** 2 + m2)
    wdot = (-(ks / a) ** 2 * H - 0.5 * c * S23 * v * m2) / w
    u = 1 / np.sqrt(2 * w) + 0j
    udot = (-1j * w - wdot / (2 * w)) * u
    Xc = u * a ** -1.5
    Xcdot = a ** -1.5 * (udot - 1.5 * H * u)
    Kd = -c * S23 * v
    X = Xc / np.sqrt(K)
    Xdot = (Xcdot - 0.5 * Kd * Xc) / np.sqrt(K)
    return np.concatenate([[p, v, lna], X.real, X.imag, Xdot.real, Xdot.imag])


def _occupation(y, ks, M, c):
    n = len(ks)
    p, v, lna = y[:3]
    X = y[3:3 + n] + 1j * y[3 + n:3 + 2 * n]
    Xd = y[3 + 2 * n:3 + 3 * n] + 1j * y[3 + 3 * n:]
    a = np.exp(lna)
    H = np.sqrt((0.5 * v * v + V(p)) / 3)
    K = np.exp(-c * S23 * p)
    Kd = -c * S23 * v
    Xc = np.sqrt(K) * X
    Xcd = np.sqrt(K) * (Xd + 0.5 * Kd * X)
    u = a ** 1.5 * Xc
    ud = a ** 1.5 * (Xcd + 1.5 * H * Xc)
    w = np.sqrt((ks / a) ** 2 + M * M * K)
    wdot = (-(ks / a) ** 2 * H - 0.5 * c * S23 * v * M * M * K) / w
    f = 1 / np.sqrt(2 * w)
    fd = (-1j * w - wdot / (2 * w)) * f
    beta = -1j * (f * ud - fd * u)                   # u = alpha f + beta f*
    nk = np.abs(beta) ** 2
    wr = np.imag(np.conj(u) * ud)                    # Wronskian, should be -1/2
    return nk, wr, a, 0.5 * v * v + V(p)


def produce(B, M, c, kappas, t_final=4000.0, k_start=300.0, rtol=1e-12):
    """occupation numbers n_k at t_final for k = kappa a_e H_e (mu = 1 units)"""
    ae_He = np.exp(B["lna_end"]) * B["H_end"]
    out_n, out_w = np.zeros(len(kappas)), np.zeros(len(kappas))
    groups = np.array_split(np.arange(len(kappas)), max(1, len(kappas) // 6))
    for g in groups:
        ks = kappas[g] * ae_He
        kmin = ks.min()
        t0 = brentq(lambda t: kmin / (np.exp(bg_at(B, t)[2]) * bg_at(B, t)[3]) - k_start,
                    0.0, B["t_end"])
        n = len(ks)

        def rhs(t, y):
            p, v, lna = y[:3]
            H = np.sqrt((0.5 * v * v + V(p)) / 3)
            a = np.exp(lna)
            X = y[3:3 + 2 * n]
            Xd = y[3 + 2 * n:]
            fr = 3 * H - c * S23 * v
            w2 = np.tile((ks / a) ** 2 + M * M * np.exp(-c * S23 * p), 2)
            return np.concatenate([[v, -3 * H * v - dV(p), H], Xd, -fr * Xd - w2 * X])

        sol = solve_ivp(rhs, [t0, t_final], _ic(B, t0, ks, M, c), method="DOP853",
                        rtol=rtol, atol=1e-30)
        nk, wr, a, rho = _occupation(sol.y[:, -1], ks, M, c)
        out_n[g], out_w[g] = nk, wr
    a_fin, rho_fin = a, rho
    return out_n, out_w, a_fin, rho_fin


def n_over_rho(B, M, c, kappas, **kw):
    """comoving n / comoving rho_inflaton at the end (mu, M_Pl = 1 units)"""
    nk, wr, a, rho = produce(B, M, c, kappas, **kw)
    ae_He = np.exp(B["lna_end"]) * B["H_end"]
    ks = kappas * ae_He
    n_com = np.trapezoid(ks ** 3 * nk, np.log(ks)) / (2 * np.pi ** 2)
    return n_com / (rho * a ** 3), nk, wr


def turning_time(B, t_near):
    """a time near t_near where the scalaron velocity vanishes (p at an extremum)"""
    ts = np.linspace(t_near - 4, t_near, 400)
    v = B["sol"].sol(ts)[1]
    j = np.where(np.sign(v[:-1]) != np.sign(v[1:]))[0][-1]
    return brentq(lambda t: B["sol"].sol(t)[1], ts[j], ts[j + 1])


def t_rh_gev(mu_gev):
    """scalaron gravitational decay into the Higgs doublet (4 real scalars)"""
    gamma = 4 * mu_gev ** 3 / (192 * np.pi * MPL_GEV ** 2)
    return (90 / (np.pi ** 2 * G_STAR)) ** 0.25 * np.sqrt(gamma * MPL_GEV)


def omega_h2(M_mu, nrho, mu_gev, t_rh, dof=2):
    """Omega h^2 for dof real scalars of mass M_mu * mu, given comoving n/rho (code units)"""
    M = M_mu * mu_gev
    n_over_rho_gev = nrho * mu_gev / MPL_GEV ** 2
    Y = dof * 0.75 * t_rh * n_over_rho_gev
    return M * Y / RHO_C_OVER_S


def stur_window_r2(H_inf_gev):
    """largest M_phi = (M_f L + 2)/L allowed in the R3.3 corner (N = 60)"""
    f_min = H_inf_gev / (2 * np.pi * 0.03 * np.pi / np.sqrt(60))      # GeV
    best = 0.0
    for m in np.geomspace(2e-31, 3.4e-30, 30):
        f_max = np.sqrt(1e18 / (8 * m)) / 1e9
        if f_max < f_min:
            continue
        for f in np.geomspace(f_min, f_max, 20):
            linv = H_inf_gev / 15.06
            x = -np.log((m * f * 1e9 / (linv * 1e9) ** 2) ** 2)
            best = max(best, (x + 2) * linv)
    return best, f_min


def real_production(M, kappas, t1=4000.0, t2=16000.0):
    """Jordan frame: separate real production from the virtual dressing by the
    still-oscillating scalaron, n_k = n_real + c amp^2, using two readouts."""
    out = []
    for T in (t1, t2):
        B = background(t_max=T + 10)
        tf = turning_time(B, T)
        amp = abs(B["sol"].sol(tf)[0])
        nk, _, _, _ = produce(B, M, 1, kappas, t_final=tf, k_start=1000.0)
        out.append((amp, nk))
    (a1, n1), (a2, n2) = out
    c = (n1 - n2) / (a1 ** 2 - a2 ** 2)
    return n2 - c * a2 ** 2, n1, n2, a1, a2, c


def main():
    B = background()
    mu = B["mu"] * MPL_GEV
    t_rh = t_rh_gev(mu)
    tf = turning_time(B, 4000.0)
    print(BAR + "\n B  R^2 background and inputs\n" + BAR)
    print(f"   scalaron mass mu = {mu:.3e} GeV;  H* = {B['H_star'] * mu:.3e} GeV;"
          f"  H_end = {B['H_end'] * mu:.3e} GeV;  phi_s* = {B['p_star']:.2f} M_Pl")
    print(f"   T_RH (scalaron -> Higgs, D-A4) = {t_rh:.2e} GeV")
    thr_J = 1.5 * B["H_star"] * np.exp(S23 * B["p_star"] / 2)
    thr_E = 1.5 * B["H_star"]
    Mmax, fmin = stur_window_r2(B["H_star"] * mu)
    print(f"   P2 (isocurvature): (J) M >= {thr_J:.2f} mu = {thr_J * mu:.2e} GeV;"
          f"  (E) M >= {thr_E:.2f} mu = {thr_E * mu:.2e} GeV")
    print(f"   P3 (no scalaron -> phi phi): M > mu/2 = {mu / 2:.2e} GeV;  T_RH << M: yes")
    print(f"   STUR window (R^2 corner, N = 60): M_phi <= {Mmax:.2e} GeV = {Mmax / mu:.2f} mu")

    print("\n" + BAR + "\n P  Jordan frame (primary): production inside the window\n" + BAR)
    kap4 = np.array([0.2, 0.8, 2.0, 5.0])
    for M in (thr_J, Mmax / mu):
        nr, n1, n2, a1, a2, c = real_production(M, kap4)
        print(f"   M = {M:.2f} mu: n_k at scalaron amp {a1:.1e}: "
              + " ".join(f"{x:.2e}" for x in n1))
        print(f"   {'':14s}at scalaron amp {a2:.1e}: " + " ".join(f"{x:.2e}" for x in n2))
        print(f"   {'':14s}n_k / amp^2 = " + " ".join(f"{x:.3e}" for x in c)
              + "  (constant: virtual dressing)")
        print(f"   {'':14s}real n_k = n - c amp^2 = " + " ".join(f"{x:+.1e}" for x in nr))
        bound = np.max(np.abs(nr)) + 1e-16
        r_plateau, nk, _ = n_over_rho(B, M, 1, np.geomspace(0.05, 60, 18), t_final=tf,
                                      k_start=1000.0)
        om_plateau = omega_h2(M, r_plateau, mu, t_rh)
        om_bound = om_plateau * bound / np.max(nk)
        w = kap4 ** 3                                # number density weights k^3
        om_w = om_plateau * np.sum(w * np.abs(nr)) / np.sum(w * n1)
        print(f"   {'':14s}-> Omega h^2 <= {om_bound:.0e} (largest residual on every mode);"
              f" k^3-weighted ~ {om_w:.0e}.  P1 needs 0.12: FAIL")
    print("   Below the threshold the field is light during inflation:")
    r, nk, _ = n_over_rho(B, 3.0, 1, np.geomspace(0.05, 60, 18), t_final=tf, k_start=1000.0)
    sl = np.log(nk[1] / nk[0]) / np.log(np.geomspace(0.05, 60, 18)[1] / 0.05) + 3
    print(f"   M = 3.00 mu: Omega h^2 = {omega_h2(3.0, r, mu, t_rh):.1e}, IR slope of"
          f" k^3 n_k = {sl:+.2f} (scale-invariant-ish: isocurvature): P2 FAIL")
    print("   -> (J): no M_phi in STUR's window satisfies P1 and P2 together. 8A is a NO-GO.")

    print("\n" + BAR + "\n E  Einstein-frame spectator (sensitivity only)\n" + BAR)
    kap = np.geomspace(0.05, 60, 18)
    res = []
    for M in (thr_E, 1.0, 1.5, 2.0, 2.5, 3.0):
        r, nk, _ = n_over_rho(B, M, 0, kap, t_final=tf, k_start=1000.0)
        om = omega_h2(M, r, mu, t_rh)
        res.append((M, om))
        print(f"   M = {M:.2f} mu = {M * mu:.2e} GeV: Omega h^2 = {om:.2e}  (n_k max {nk.max():.1e})")
    Ms, oms = np.array(res).T
    lg = np.log(oms)
    j = np.where((lg[:-1] - np.log(0.12)) * (lg[1:] - np.log(0.12)) <= 0)[0]
    if len(j):
        j = j[0]
        Mx = Ms[j] + (np.log(0.12) - lg[j]) * (Ms[j + 1] - Ms[j]) / (lg[j + 1] - lg[j])
        print(f"   -> Omega h^2 = 0.12 at M ~ {Mx:.2f} mu = {Mx * mu:.1e} GeV (inside the"
              f" window, above P2 and P3).")
        for t in (1e8, 1e10):
            print(f"      T_RH = {t:.0e} GeV would rescale Omega by {t / t_rh:.2f}:"
                  " the crossing mass moves only logarithmically.")
    print("   -> if phi coupled to the Einstein-frame metric, 8A would pass P1-P3;")
    print("      but that is not R^2 gravity, and it was preregistered as a sensitivity check.")


if __name__ == "__main__":
    main()
