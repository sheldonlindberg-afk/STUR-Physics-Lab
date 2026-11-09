#!/usr/bin/env python3
"""
Make It Make Sense theory, part 6: what comes out when the horizon dissolves.

B1  What the collapse leaves (part 5's solver, run past the lifetime T).
    The trapped region vanishes, nothing is left inside r_s, and ALL the mass sits in one
    shell just outside r_s that drifts outward at a pace fixed in units of T:
    position converged to ~0.1% over three grid resolutions; speed ~ 0.019/M (c, Planck M).
    The shell is UNRESOLVED (the mass rises 0 -> M across ~2 cells).  CORRECTION (part 7):
    the "peak local fullness" printed below comes from one cell whose averaged phase sits
    near pi/2 -- an ARTIFACT, retracted.  What stands: the exact solution is a zero-thickness
    shell (unbounded local fullness), and part 7 shows its slow drift is an artifact of the
    winding rule; GR outside r_s moves such a shell at ~0.7 c.

B2  What it is made of.  A hole ending today has M_now (part 5) and must be primordial.
    It formed when the horizon mass was ~M: t_f = G M / c^3 (LIT, recalled: PBH mass is
    a fraction gamma ~ 0.2 of the horizon mass; gamma = 1 used, its effect is shown).
    FOLLOWS: the mean density inside r_s, 3 c^6 / (32 pi G^3 M^2), equals the density of
    the universe at t_f exactly (radiation era, rho = 3 / (32 pi G t^2)).  So the hole is
    early-universe plasma, all Standard-Model species (g* = 106.75, KNOWN).

B3  Photon energy.  Entropy is conserved in adiabatic collapse and bounce and only rises in
    shocks, so the emerging plasma, back at radius ~r_s, is at most as hot as at formation:
        k T_out <= k T_f,   (pi^2/30) g* (kT_f)^4 / (hbar c)^3 = rho(t_f) c^2.   (FOLLOWS)
    Baryon loading eta * m_p c^2 / (2.7 k T) is ~1e-13: a pure-radiation fireball, whose
    observed temperature stays ~T_0 (KNOWN, recalled: Goodman 1986; Paczynski 1986).
B4  The burst: energy M_now c^2, photons at ~2.7 k T_f (upper bound), all arriving within
    ~r_s / c: a simultaneous rain of multi-TeV photons.  Detection distance for a ground
    array (effective area 1e5 m^2, 10 photons; both are choices, not specifications).
"""
import numpy as np

import fp_collapse_shock as S

G, c, hbar, kB = 6.67430e-11, 2.99792458e8, 1.054571817e-34, 1.380649e-23
EV = 1.602176634e-19
MPC = 3.0857e22
M_P_KG = np.sqrt(hbar * c / G)
GSTAR = 106.75
ETA_B = 6.1e-10          # baryon-to-photon ratio (recalled, Planck)
M_PROTON_EV = 938.272e6


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


# ----------------------------------------------------------------- B1
def shell_after(M, dR=0.05, t_over_T=(1.5, 2.0), c0=24.1):
    """Front position (r_s), 10-90% mass interval (r_s), peak local fullness, m(<r_s)/M."""
    k, Rf, Rc, B = S.setup(M, 1.0, dR, 3.0, 1.5)
    T = c0 * M ** 2
    marks, out, t = list(t_over_T), [], 0.0
    while marks:
        B, dt = S.step(B, k, Rf, Rc, dR, 0.45)
        t += dt
        if t > marks[0] * T:
            marks.pop(0)
            b = np.clip(B / Rc ** 2, 0, np.pi)
            m = 4 * np.pi / 3 * Rc ** 3 * np.sin(b) ** 2
            rho = np.gradient(m, Rc) / (4 * np.pi * Rc ** 2)
            rs = 2 * M
            front = Rc[np.where(b > np.pi / 2)[0].max()] / rs
            lo, hi = Rc[np.searchsorted(m, 0.1 * M)] / rs, Rc[np.searchsorted(m, 0.9 * M)] / rs
            out.append(dict(t=t / T, front=front, lo=lo, hi=hi,
                            peak=float(np.max(rho[Rc > 0.8 * rs])),
                            inside=float(m[np.searchsorted(Rc, 0.95 * rs)] / M)))
    return out


# ----------------------------------------------------------------- B2-B4
def formation(M, gamma=1.0):
    t_f = G * M / (gamma * c ** 3)
    rho_univ = 3 / (32 * np.pi * G * t_f ** 2)
    rho_hole = 3 * c ** 6 / (32 * np.pi * G ** 3 * M ** 2)
    kT = (rho_univ * c ** 2 * (hbar * c) ** 3 * 30 / (np.pi ** 2 * GSTAR)) ** 0.25
    return t_f, rho_univ, rho_hole, kT


def burst(M, kT, f_gamma=0.5, area=1e5, n_det=10):
    E = M * c ** 2
    e_ph = 2.7 * kT
    N = f_gamma * E / e_ph
    d = np.sqrt(N * area / (4 * np.pi * n_det))
    return E, e_ph, N, d


def main():
    banner("B1  What the collapse leaves (dust, part 5's law)")
    print("   M = 3 m_P, three grid spacings:")
    res = {}
    for dR in (0.05, 0.025):
        r = shell_after(3.0, dR)
        res[dR] = r
        for x in r:
            print(f"   dR = {dR:<6} t = {x['t']:.1f} T: front {x['front']:.4f} r_s; 80% of mass"
                  f" in [{x['lo']:.4f}, {x['hi']:.4f}] r_s; m(<0.95 r_s) = {x['inside']:.3f} M")
    print("   (dR = 0.0125, run once in this project: front 1.1448 / 1.2594 r_s.)")
    r1, r2 = res[0.05], res[0.025]
    v = (r2[1]["front"] - r2[0]["front"]) * 2 * 3.0 / (0.5 * 24.1 * 9)
    print(f"   shell speed ~ {v:.4f} c at M = 3  ->  ~{v*3:.3f}/M c")
    print("   -> no horizon, nothing inside: a horizonless shell of pure matter, drifting out.")
    print("   -> CORRECTED in part 7: this slow drift is an artifact of the winding rule; GR")
    print("      outside r_s moves a thin shell at ~0.7 c.")

    banner("B2  What a hole ending today is made of")
    import fp_collapse_shock as C
    c0 = 24.1
    _, M_now = C.physical(c0)
    t_f, ru, rh, kT = formation(M_now)
    print(f"   M_now = {M_now:.3e} kg = {M_now/M_P_KG:.2e} m_P;  formed at t_f = GM/c^3 = "
          f"{t_f:.2e} s")
    print(f"   density of the universe then {ru:.4e} kg/m^3; mean density inside r_s "
          f"{rh:.4e}  (equal: FOLLOWS)")
    print(f"   -> early-universe plasma at k T_f = {kT/EV/1e12:.2f} TeV, all species (g* = "
          f"{GSTAR})")
    for g in (0.2, 0.5):
        print(f"      (gamma = {g}: k T_f = {formation(M_now, g)[3]/EV/1e12:.2f} TeV)")

    banner("B3-B4  The burst (upper bound on photon energy)")
    load = ETA_B * M_PROTON_EV / (2.7 * kT / EV)
    E, e_ph, N, d = burst(M_now, kT)
    rs = 2 * G * M_now / c ** 2
    print(f"   baryon loading eta m_p c^2 / (2.7 kT) = {load:.1e}: pure-radiation fireball")
    print(f"   energy {E:.2e} J; photons at <~ {e_ph/EV/1e12:.1f} TeV; ~{N:.1e} photons "
          "(half the energy, assumed)")
    print(f"   arrival spread ~ r_s / c = {rs/c:.1e} s: every photon lands at the same moment")
    print(f"   seen by a 1e5 m^2 ground array (10 photons) out to {d/MPC:.0f} Mpc, inside the")
    print("   ~100 Mpc range multi-TeV photons survive (recalled: absorption on starlight)")
    print("   SIGNATURE: many multi-TeV air showers at the same nanosecond across the array;")
    print("   TeV neutrinos at the same moment.")
    print("   Part 7: once outside r_s the shell leaves at ~0.7 c, so this prompt flash is the")
    print("   theory's burst; WHEN it happens (the lifetime) is open again.")
    return dict(res=res, M_now=M_now, kT=kT, ru=ru, rh=rh, load=load, d=d, e_ph=e_ph)


if __name__ == "__main__":
    main()
