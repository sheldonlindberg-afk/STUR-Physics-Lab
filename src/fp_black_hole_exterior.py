#!/usr/bin/env python3
"""
Fullness-phase theory, part 4: where the core's bounce can get out.

Part 1 found a pure-matter core inside every astrophysical horizon, and that the gravity
law differs from GR only by ~phi/3, i.e. by 1e-77 or less outside the horizon if phi is
the local density.  But in teleparallel gravity the law acts on the TORSION scalar T, and T
outside a mass is not small near the horizon.

  X1  Exterior torsion.  For ds^2 = A dt^2 - B dr^2 - r^2 dOmega^2 with the spherical
      ("good", rotated) tetrad, the torsion scalar is (derived with sympy in this project,
      src/fp_torsion_derivation.py; LIT, recalled: same form as Bahamonde et al.)
          T = 2 (sqrt B - 1) [A (sqrt B - 1) - r A'] / (r^2 A B)
      Schwarzschild: T = (4/r^2) [1 - (r - M)/sqrt(r (r - 2M))]  ->  -2M^2/r^4 far away,
      and DIVERGES at the horizon r = 2M.
  X2  The cap.  The law (FP) only exists for |T| <= |T_b| = 4 pi G rho_max / c^2
      = 4 pi chi / l_P^2 (chi = rho_max / rho_P >= 1).  The static exterior therefore
      ends at a "cap surface" r_cap = r_s (1 + delta):
          sqrt(delta) = l_P^2 / (2 pi chi r_s^2)                               (FOLLOWS)
      proper distance above the horizon  s = l_P^2 / (pi chi r_s)  (sub-Planckian), and
      redshift factor there  1/sqrt(A) = 2 pi chi r_s^2 / l_P^2.
      By part 3 (the measurement wall at l_P) the cap is closer to the horizon than any
      measurement can resolve.
  X3  Observable consequences, by what the cap does:
      (a) reflects even partly -> gravitational-wave ECHOES after a merger, delay
          dt = 2 [r*(3M) - r*(r_cap)] / c,   r* = r + r_s ln(r/r_s - 1)    (FOLLOWS)
          It depends on chi and rho_max only through a logarithm: a sharp prediction.
      (b) lets the bounce straight out (milliseconds) -> accreting black holes would
          explode; they don't.  EXCLUDED.
      (c) releases the bounce at the cap's redshift (NEW assumption: the core's proper
          bounce time 2 r_s / 3c, seen through the cap's redshift):
          t_esc = (2 r_s / 3c) * 2 pi chi r_s^2 / l_P^2 = (32 pi chi / 3) G^2 M^3 / (hbar c^4)
          = Hawking time / (480 / chi).  Small primordial black holes would be releasing
          their whole mass in one burst TODAY.
"""
import numpy as np

G, c, hbar = 6.67430e-11, 2.99792458e8, 1.054571817e-34
M_SUN = 1.98892e30
L_P = np.sqrt(hbar * G / c ** 3)
M_P = np.sqrt(hbar * c / G)
YR = 3.15576e7
T_UNIV = 1.38e10 * YR
EV = 1.602176634e-19


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


# ----------------------------------------------------------------- X1
def torsion_general(r, A, B, dA):
    sB = np.sqrt(B)
    return 2 * (sB - 1) * (A * (sB - 1) - r * dA) / (r * r * A * B)


def torsion_schw(r, rs):
    M = rs / 2
    return 4 / r ** 2 * (1 - (r - M) / np.sqrt(r * (r - 2 * M)))


# ----------------------------------------------------------------- X2
def cap(rs, chi=1.0):
    sd = L_P ** 2 / (2 * np.pi * chi * rs ** 2)
    return dict(sqrt_delta=sd, ln_inv_delta=-2 * np.log(sd), proper=2 * rs * sd,
                redshift=1 / sd)


def cap_exact(rs_in_lP, chi=1.0):
    """CHECK, in Planck units with mpmath: solve |T(r)| = 4 pi chi exactly."""
    import mpmath as mp
    mp.mp.dps = 80
    rs = mp.mpf(rs_in_lP)
    Tb = 4 * mp.pi * chi
    T = lambda r: abs(4 / r ** 2 * (1 - (r - rs / 2) / mp.sqrt(r * (r - rs))))
    g = lambda ld: T(rs * (1 + mp.e ** (-ld))) - Tb          # ld = ln(1/delta)
    ld = mp.findroot(g, -2 * mp.log(1 / (2 * mp.pi * chi * rs ** 2)))
    return float(ld)


# ----------------------------------------------------------------- X3
def echo_delay(M, chi=1.0):
    """Non-spinning estimate: round trip between the photon sphere (3M) and the cap."""
    rs = 2 * G * M / c ** 2
    ld = cap(rs, chi)["ln_inv_delta"]
    return 2 * rs / c * (0.5 + np.log(0.5) + ld)


def t_escape(M, chi=1.0):
    return 32 * np.pi * chi / 3 * G ** 2 * M ** 3 / (hbar * c ** 4)


def t_hawking(M):
    return 5120 * np.pi * G ** 2 * M ** 3 / (hbar * c ** 4)


def mass_escaping_now(chi=1.0, t=T_UNIV):
    return (3 * hbar * c ** 4 * t / (32 * np.pi * chi * G ** 2)) ** (1 / 3)


def main():
    banner("X1  Torsion outside a black hole")
    rs = 1.0
    r = np.array([1.001, 1.01, 1.5, 3.0, 10.0, 100.0])
    A = 1 - rs / r
    Tg = torsion_general(r, A, 1 / A, rs / r ** 2)
    Ts = torsion_schw(r, rs)
    print("   r/r_s     T r_s^2 (general)   (Schwarzschild form)   far-field -2M^2/r^4")
    for ri, a, b in zip(r, Tg, Ts):
        print(f"   {ri:7.3f}   {a:+.6e}       {b:+.6e}          {-2*0.25/ri**4:+.3e}")
    print("   -> |T| grows without bound as r -> r_s: the horizon is where the law matters.")
    print("   Law deviation f/T - 1 at the photon sphere (r = 1.5 r_s), rho_max = rho_P:")
    Tb_SI = -4 * np.pi / L_P ** 2
    dev = {}
    for lab, m in [("10 Msun", 10), ("Sgr A*", 4.3e6), ("M87*", 6.5e9)]:
        rsm = 2 * G * m * M_SUN / c ** 2
        T = torsion_schw(1.5 * rsm, rsm)
        dev[lab] = (T / Tb_SI) / 3          # f/T - 1 = x/3 + ..., x = T/T_b (too small for floats)
        print(f"      {lab:8s}: {dev[lab]:.1e}   (EHT and LIGO: unobservable)")

    banner("X2  The cap: the static exterior ends just above the horizon")
    print("   CHECK exact root vs formula ln(1/delta) = 4 ln(r_s/l_P) + 2 ln(2 pi chi):")
    chk = []
    for rsl in (1e3, 1e6):
        ex = cap_exact(rsl)
        fo = cap(rsl * L_P)["ln_inv_delta"]
        chk.append(abs(ex - fo))
        print(f"      r_s = {rsl:.0e} l_P:  exact {ex:.6f}   formula {fo:.6f}")
    print("   object      r_s (m)      proper height of cap   redshift at cap")
    rows = []
    for lab, m in [("10 Msun", 10), ("62 Msun (GW150914)", 62), ("Sgr A*", 4.3e6)]:
        rsm = 2 * G * m * M_SUN / c ** 2
        cp = cap(rsm)
        rows.append((lab, rsm, cp))
        print(f"   {lab:19s} {rsm:.3e}   {cp['proper']:.2e} m ({cp['proper']/L_P:.1e} l_P)"
              f"   {cp['redshift']:.2e}")
    print("   The cap sits a sub-Planck proper distance above the horizon: by part 3 no")
    print("   measurement can tell it from a horizon directly.  Only what it DOES can.")

    banner("X3a  If the cap reflects at all: echoes (sharp, almost parameter-free)")
    print("   final mass        echo delay (non-spinning)   chi = 1e3 instead of 1")
    echoes = {}
    for lab, m in [("10 Msun", 10), ("62 Msun (GW150914)", 62), ("1e6 Msun (LISA)", 1e6)]:
        d1, d2 = echo_delay(m * M_SUN), echo_delay(m * M_SUN, 1e3)
        echoes[lab] = d1
        print(f"   {lab:18s} {d1:10.4f} s                  {d2:10.4f} s")
    print("   LIT (recalled): Abedi, Dykaar & Afshordi 2016 claimed echoes in GW150914 at")
    print("   ~0.29 s (Planck-length wall, with spin); LIGO-Virgo searches since find no")
    print("   significant echoes.  Here the cap is at l_P^2/r_s, not l_P, so ln(1/delta) is")
    print("   doubled: the predicted delay is about TWICE the Planck-wall value.  Spin is not")
    print("   included (needs the rotating solution of the law: OPEN).")

    banner("X3b  If the cap lets the bounce straight out")
    rs10 = 2 * G * 10 * M_SUN / c ** 2
    print(f"   Outside time ~ (r_s/c) ln(1/delta) = {rs10/c*cap(rs10)['ln_inv_delta']*1e3:.1f}"
          " ms for 10 Msun: every accreting black hole")
    print("   would re-explode what it swallows.  X-ray binaries and quasars persist: EXCLUDED.")

    banner("X3c  If the cap releases the bounce at its redshift (NEW assumption)")
    print(f"   t_esc / t_Hawking = {t_escape(M_SUN)/t_hawking(M_SUN):.6f} = 1/480 (chi = 1)")
    for lab, m in [("1 Msun", 1), ("Sgr A*", 4.3e6)]:
        print(f"   {lab:7s}: t_esc = {t_escape(m*M_SUN)/YR:.1e} yr  (no conflict with any"
              " observation)")
    Mn = mass_escaping_now()
    rsn = 2 * G * Mn / c ** 2
    Eph = hbar * c / rsn / EV
    print(f"   Black holes releasing their bounce TODAY (if primordial): M = {Mn:.2e} kg")
    print(f"      (Hawking evaporation ending today, photons only: {mass_escaping_now(480):.2e} kg;"
          " ~5e11 kg with all species, recalled)")
    print(f"      burst energy M c^2 = {Mn*c**2:.1e} J, all at once, size r_s = {rsn:.1e} m,")
    print(f"      characteristic photon energy hbar c / r_s = {Eph/1e6:.0f} MeV (gamma rays).")
    print("   Hawking evaporation ends with a TeV flash of the last ~1e7 kg (recalled); the bounce")
    print(f"   instead releases ~{Mn:.0e} kg at ~100 MeV.  Distinct in energy and size.")
    print("   OPEN: the primordial black-hole abundance is unknown, so the burst RATE is")
    print("   not predicted; Fermi-LAT burst searches would bound it.")
    print("   ALTERNATIVE (same cap, Planck-time dynamics instead of the core's): t ~ M^2,")
    print("   the Haggard-Rovelli scaling (LIT, recalled).  The theory must decide.")
    return dict(chk=max(chk), echoes=echoes, Mn=Mn, Eph=Eph, dev=dev)


if __name__ == "__main__":
    main()
