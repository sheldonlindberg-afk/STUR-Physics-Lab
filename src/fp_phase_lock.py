#!/usr/bin/env python3
"""
Fullness-phase theory, part 3: measurement is phase locking (postulate P4).

The user's statement: what is really measured is how much energy it takes to phase-lock a
quantum system to an EM system (the probe) so that we can view it.

  L1  Locking (KNOWN, Adler 1946): relative phase obeys  dtheta/dt = dw - K sin(theta).
      Locked (theta constant) iff |dw| <= K; otherwise it slips at sqrt(dw^2 - K^2).
  L2  Viewing a feature of size dx = reading the locked phase to dtheta = k dx.  With N
      probe quanta the phase is known to 1/sqrt(N) (classical light, SQL) or 1/N (quantum-
      correlated light, Heisenberg limit; KNOWN).  Energy to view:
          E_HL = hbar c / dx        (independent of the probe's colour)
          E_SQL = hbar c lambda / (2 pi dx^2)
  L3  The horizon wall: the probe energy sits in a region R >= max(lambda, dx); it must not
      be inside its own Schwarzschild radius 2GE/c^4.
  L4  Locking is MUTUAL: the coupling that pulls the probe onto the system pulls the system
      too (back-action).  During the lock time t >= R/c the system (mass m) spreads by
          dx^2 >= hbar t / (2 m)          (KNOWN, Salecker & Wigner 1958)
      and must not be a black hole: m <= c^2 R_s / 2G.  Causality: only the part of the
      system within c t can take part in the lock, R_s <= c t.
          => dx >= l_P                                                        (FOLLOWS)
      for ANY probe colour, photon number or quantum state.
  L5  Link to part 1: fullness of the lock region at the wall, compared with rho_max.
"""
import numpy as np

G, c, hbar = 6.67430e-11, 2.99792458e8, 1.054571817e-34
L_P = np.sqrt(hbar * G / c ** 3)
RHO_P = c ** 5 / (hbar * G ** 2)


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


# ----------------------------------------------------------------- L1
def adler_slip_rate(dw, K, t_end=4000.0, n=400001):
    """Mean d(theta)/dt of the Adler equation over the second half of the run (RK4)."""
    t = np.linspace(0, t_end, n)
    h = t[1] - t[0]
    th = 0.0
    f = lambda th: dw - K * np.sin(th)
    half = (n - 1) // 2
    for i in range(n - 1):
        if i == half:
            th_mid = th
        k1 = f(th); k2 = f(th + h * k1 / 2); k3 = f(th + h * k2 / 2); k4 = f(th + h * k3)
        th += h * (k1 + 2 * k2 + 2 * k3 + k4) / 6
    return (th - th_mid) / (t_end - t[half])


# ----------------------------------------------------------------- L2-L4
def energy_to_view(dx, lam, mode):
    return hbar * c / dx if mode == "HL" else hbar * c * lam / (2 * np.pi * dx ** 2)


def probe_wall(lam, mode):
    """Smallest dx with 2 G E / c^4 <= R, R = max(lam, dx)."""
    if lam is None:                      # imaging: lam = dx, one quantum
        return np.sqrt(2) * L_P
    if mode == "SQL":                    # 2G/c^4 * hbar c lam/(2 pi dx^2) <= lam
        return L_P / np.sqrt(np.pi)
    return 2 * L_P ** 2 / lam            # 2G/c^4 * hbar c/dx <= lam


def backaction_wall(t, R_s):
    """dx^2 >= hbar t / (2m),  m <= c^2 R_s / (2G)  ->  dx >= l_P sqrt(c t / R_s)."""
    return L_P * np.sqrt(c * t / R_s)


def main():
    banner("L1  CHECK: Adler locking")
    out = {}
    errs = []
    for dw, K in [(0.5, 1.0), (0.99, 1.0), (1.5, 1.0), (3.0, 1.0)]:
        num = adler_slip_rate(dw, K)
        th = 0.0 if abs(dw) <= K else np.sqrt(dw ** 2 - K ** 2)
        errs.append(abs(num - th))
        print(f"   dw/K = {dw/K:4.2f}: slip rate {num:.5f}  vs  {th:.5f}"
              f"  -> {'LOCKED' if th == 0 else 'slips'}")
    out["adler_err"] = max(errs)

    banner("L2-L3  Energy to view dx, and where the probe makes a horizon")
    for lam in (1e-6, 1e-15):
        print(f"   probe wavelength {lam:.0e} m:")
        for dx in (1e-18, 1e-25, 1e-33):
            print(f"      dx = {dx:.0e} m:  E_HL = {energy_to_view(dx, lam, 'HL'):.2e} J,"
                  f"  E_SQL = {energy_to_view(dx, lam, 'SQL'):.2e} J")
    print(f"\n   imaging (wavelength = dx):        dx_min = sqrt2 l_P = "
          f"{probe_wall(None, 'HL'):.2e} m")
    print(f"   classical light (SQL), R = lambda: dx_min = l_P/sqrt(pi) = "
          f"{probe_wall(1e-6, 'SQL'):.2e} m  (any colour)")
    for lam in (1e-6, 1.0):
        print(f"   quantum light (HL), lambda = {lam:.0e} m: dx_min = 2 l_P^2/lambda = "
              f"{probe_wall(lam, 'HL'):.1e} m  <- probe ALONE allows sub-Planck")

    banner("L4  Mutual locking: the system is pulled too")
    for lab, t, Rs in [("system = lock region (R_s = c t)", 1e-15, c * 1e-15),
                       ("1 s lock, 1 m system (small: spreads more)", 1.0, 1.0),
                       ("1 s lock, causal part of system (R_s = c t)", 1.0, c)]:
        print(f"   {lab:45s}: dx >= {backaction_wall(t, Rs):.2e} m")
    print("   Causality: in a lock of duration t only the part of the system within c t can")
    print("   respond together, so R_s <= c t and dx >= l_P = "
          f"{L_P:.3e} m, whatever the probe.")
    print("   FOLLOWS: the Planck wall is a property of LOCKING, not of light.  Quantum light")
    print("   beats the probe wall (L3) but not the back-action wall: the harder the probe")
    print("   pulls, the harder the system is pulled.")
    print("   (Ng & van Dam, KNOWN, get (l_P^2 L)^(1/3) by assuming the clock is no bigger")
    print("   than dx; the causal assumption here gives l_P exactly.)")

    banner("L5  The wall in fullness terms")
    dx = np.sqrt(2) * L_P
    rho = hbar * c / dx / c ** 2 / (4 / 3 * np.pi * dx ** 3)
    print(f"   Fullness of the lock region at the imaging wall: rho = {rho/RHO_P:.3f} rho_P")
    print("   With rho_max >= rho_P (user's choice C), the wall is reached at phi <= "
          f"{rho/RHO_P:.3f}:")
    print("   everything between the measurement wall and the ceiling (phi = 1) can never be")
    print("   viewed, because locking to it makes a horizon first.  This is P1 restated as a")
    print("   theorem about measurement.")
    out.update(phi_wall=rho / RHO_P)
    return out


if __name__ == "__main__":
    main()
