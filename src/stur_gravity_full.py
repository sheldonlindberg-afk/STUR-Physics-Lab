#!/usr/bin/env python3
"""
Gravity-induced entanglement, modelled to the end: everything stur_gravity_entanglement.py
left out, then a full design search.

  H1  Split and recombine stages (the branches are not held at fixed distances: they
      open, hold and close). Phases integrated along the trajectories.
  H2  Blackbody decoherence: scattering of thermal photons, and emission / absorption
      at the diamond's internal and the environment's temperature.
  H3  Acceleration noise: random phases shot to shot, independent per diamond or
      common to both (correlated or anti-correlated).
  H4  The split itself: a Stern-Gerlach force on ONE electron spin (an NV centre) has to
      open a 10^-14 kg diamond to dx. This ties mass, dx and ramp time together.
  H5  Full design search over mass, dx, hold time and ramp time, with gap set by Casimir,
      every dephasing source included, and the wall-clock time to a 3-sigma result.
  H6  EM forces that CAN fake entanglement: net charge and permanent dipoles.
  H7  What comes out: requirements against the state of the art, and the lambda reach.

Labels: KNOWN, FOLLOWS, LIT (literature input), ASSUMPTION (a stated input that the
result is then scanned over), PROPOSAL (lambda). Newtonian gravity and ordinary EM only.
"""
import numpy as np
from scipy.special import zeta

import stur_gravity_entanglement as g
from stur_gravity_entanglement import G, HBAR, C, KB, radius, EPS_DIAMOND

MU_B = 9.2740100783e-24
K_RE = (EPS_DIAMOND - 1) / (EPS_DIAMOND + 2)
B_GRAD = 1e6            # T/m   LIT: field gradient assumed by Bose et al. 2017
T_RESET = 5.0           # s     ASSUMPTION: reload / reset / readout overhead per run
YEAR = 3.156e7
MIN_RUNS = 9 * 30       # ASSUMPTION: at least 30 runs in each of the 9 local settings
LPF_ASD = 1.74e-15      # m s^-2 / sqrt(Hz)   LIT: LISA Pathfinder (Armano et al., PRL 120, 061101 (2018))
MAX_MASS_SUPERPOSED = 25000 * 1.66053907e-27   # LIT: Fein et al., Nat. Phys. 15, 1242 (2019)
NV_T2_BEST = 1.6        # s     LIT: NV ensemble T2 with dynamical decoupling at 77 K (Bar-Gill 2013: ~0.6 s);
                        #       1.6 s used as an optimistic round value, scanned below


# The design-search grids (H5) and design A. Design A is the best design of scenario A on these
# grids with the interpolated gas rate used before H5b; it is kept as the repository's reference
# geometry (with the derived rate the optimum moves to 6.8e-14 kg, 53 um, and design A needs
# 270 runs instead of 565). design_a() is the single source for every script that uses it;
# main() and tests/test_gravity_full.py check that the search still returns exactly this point.
MASSES = np.geomspace(1e-16, 1e-12, 25)
DXS = np.geomspace(10e-6, 3e-3, 25)
HOLDS = np.geomspace(0.05, 20, 25)
RAMPS = np.geomspace(0.05, 5, 17)
DESIGN_A_INDEX = (13, 18, 2, 12)                     # (mass, dx, hold, ramp) on the grids above


# scenario A of the H5 search: the Bose et al. targets, no acceleration noise, unlimited spin coherence
BASE_ENV = dict(P=1e-15, T_env=0.15, T_int=0.15, im_K=0.01, asd=0.0, T2=1e9, m_gas=g.M_N2)


def casimir_safe_gap():
    """H0: the gap where Casimir's entangling phase is 10% of gravity's (mass-independent)."""
    return g.casimir_vs_gravity_gap(g.BASE["m"], g.BASE["dx"], g.BASE["tau"], "parallel")


def design_a():
    """Design A (H5, scenario A, interpolated gas rate): mass, branch separation, hold and ramp
    times, total time, the Casimir-safe gap and the diamond's radius."""
    i, j, k, l = DESIGN_A_INDEX
    m, dx, hold, ramp = float(MASSES[i]), float(DXS[j]), float(HOLDS[k]), float(RAMPS[l])
    return dict(m=m, dx=dx, hold=hold, ramp=ramp, total=hold + 2 * ramp, gap=casimir_safe_gap(),
                R=float(radius(m)))


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


# --------------------------------------------------------------------------- H1
def ramp_profile(t, tau_hold, t_ramp):
    """Fraction s(t) of the full separation: 0 -> 1 in t_ramp (accelerate then
    decelerate, so s = 2(t/t_r)^2 then 1 - 2(1 - t/t_r)^2), hold, then the mirror image."""
    def up(x):
        x = np.clip(x, 0, 1)
        return np.where(x < 0.5, 2 * x**2, 1 - 2 * (1 - x) ** 2)
    total = tau_hold + 2 * t_ramp
    s = np.where(t < t_ramp, up(t / max(t_ramp, 1e-30)), 1.0)
    s = np.where(t > t_ramp + tau_hold, up((total - t) / max(t_ramp, 1e-30)), s)
    return s


def trajectory_dphi(m, dx, gap, tau_hold, t_ramp, n=4001):
    """Entangling phase for the parallel geometry with symmetric splitting +-dx/2 (both
    diamonds), centres `gap` apart; nearest branches are `gap` apart throughout."""
    total = tau_hold + 2 * t_ramp
    t = np.linspace(0, total, n)
    s = ramp_profile(t, tau_hold, t_ramp)
    y = 0.5 * dx * s
    same = 1 / gap                                  # branches i == j stay `gap` apart
    cross = 1 / np.sqrt(gap**2 + (2 * y) ** 2)
    integrand = 2 * (same - cross)                  # phi00 + phi11 - phi01 - phi10
    return G * m**2 / HBAR * np.trapezoid(integrand, t)


def hold_dphi(m, dx, gap, tau):
    return 2 * G * m**2 * tau / HBAR * (1 / gap - 1 / np.sqrt(gap**2 + dx**2))


# --------------------------------------------------------------------------- H2
def lambda_bb_scatter(m, T_env):
    """LIT (Romero-Isart, PRA 84, 052121 (2011)), localization rate, dx << hbar c / k T:
    Lambda_sc = 8! 8 zeta(9) c R^6 / (9 pi) (k T / hbar c)^9 Re[K]^2."""
    R = radius(m)
    return 40320 * 8 * zeta(9) * C * R**6 / (9 * np.pi) * (KB * T_env / (HBAR * C)) ** 9 * K_RE**2


def lambda_bb_emit(m, T, im_K):
    """LIT (same): emission (T = internal) or absorption (T = environment):
    Lambda_e = 16 pi^5 c R^3 / 189 (k T / hbar c)^6 Im[K]."""
    R = radius(m)
    return 16 * np.pi**5 * C * R**3 / 189 * (KB * T / (HBAR * C)) ** 6 * im_K


def blackbody_rate(m, dx, T_env, T_int, im_K):
    """Dephasing rate between branches dx apart. Valid for dx < thermal wavelength; above it
    the rate saturates, approximated by capping dx at hbar c / k T for each process."""
    def cap(T):
        return min(dx, HBAR * C / (KB * T))
    return (lambda_bb_scatter(m, T_env) * cap(T_env) ** 2
            + lambda_bb_emit(m, T_int, im_K) * cap(T_int) ** 2
            + lambda_bb_emit(m, T_env, im_K) * cap(T_env) ** 2)


def max_internal_T(m, dx, budget_rate, T_env, im_K):
    lo, hi = T_env, 300.0
    if blackbody_rate(m, dx, T_env, lo, im_K) > budget_rate:
        return np.nan
    for _ in range(80):
        mid = np.sqrt(lo * hi)
        lo, hi = (mid, hi) if blackbody_rate(m, dx, T_env, mid, im_K) <= budget_rate else (lo, mid)
    return lo


# --------------------------------------------------------------------------- H3
def noisy_state(ph, gamma_tau=0.0, sigma_indep=0.0, sigma_common=0.0, anti=False):
    """Average over Gaussian random phases theta on branch '1' of each diamond.
    indep: separate theta per diamond. common: the same theta on both (anti: opposite sign)."""
    rho = g.state(ph, gamma_tau)
    idx = [(i, j) for i in range(2) for j in range(2)]
    for a, (i, j) in enumerate(idx):
        for b, (k, l) in enumerate(idx):
            dA, dB = i - k, j - l
            f = np.exp(-0.5 * sigma_indep**2 * (dA**2 + dB**2))
            d = dA - dB if anti else dA + dB
            f *= np.exp(-0.5 * sigma_common**2 * d**2)
            rho[a, b] *= f
    return rho


def sigma_threshold(ph, kind, keep=0.1):
    """Phase-noise sigma (rad) at which the negativity falls to `keep` of its noiseless
    value. (Independent noise kills it outright near this point; common noise only
    makes it fade, so a fixed fraction is the fair comparison.)"""
    n0 = g.negativity(g.state(ph))
    lo, hi = 0.0, 10.0
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        kw = {"sigma_indep": mid} if kind == "indep" else {"sigma_common": mid, "anti": kind == "anti"}
        lo, hi = (mid, hi) if g.negativity(noisy_state(ph, **kw)) > keep * n0 else (lo, mid)
    return lo


def accel_phase_sigma(m, dx, tau, asd):
    """FOLLOWS: phase difference between branches = (m dx / hbar) int a dt. For white
    acceleration noise of one-sided ASD `asd`, Var(int a dt) = asd^2 tau / 2."""
    return m * dx / HBAR * asd * np.sqrt(tau / 2)


# --------------------------------------------------------------------------- H4
def max_split(m, t_ramp, grad=B_GRAD):
    """FOLLOWS: one NV spin gives force mu_B dB/dz; accelerate for t_r/2, decelerate t_r/2.
    Each branch moves a t_r^2 / 4, the opposite spin the other way: dx = a t_r^2 / 2."""
    return MU_B * grad / m * t_ramp**2 / 2


M_HE = 4.002602 * 1.66053907e-27


GAS_MODEL = "kinetic"


def gas_rate_interpolated(m, P, T, m_gas):
    """LIT (Romero-Isart, PRA 84, 052121 (2011), eq. 27): gamma = lambda_th^2 Lambda, a Gaussian
    interpolation of the long-wavelength coefficient into the saturated regime."""
    v = np.sqrt(3 * KB * T / m_gas)
    return 16 * np.pi * np.sqrt(2 * np.pi) / np.sqrt(3) * P * radius(m) ** 2 / (m_gas * v)


def hard_sphere_sigma(kR):
    """Exact quantum total cross-section of a hard sphere, in units of pi R^2 (partial waves)."""
    from scipy.special import spherical_jn, spherical_yn
    l = np.arange(0, int(kR + 40 * kR ** (1 / 3) + 50))
    d = np.arctan2(spherical_jn(l, kR), spherical_yn(l, kR))
    return 4 / kR**2 * np.sum((2 * l + 1) * np.sin(d) ** 2)


def gas_rate_kinetic(m, P, T, m_gas):
    """DERIVED. For a split much larger than the body and than the gas wavelength, every
    collision resolves the branches, so the decoherence rate is the collision rate:
        Gamma = n <v> sigma_tot,  n = P/kT,  <v> = sqrt(8kT/(pi m_gas)),  sigma_tot = 2 pi R^2
    (the quantum hard-sphere cross-section for kR >> 1, checked by hard_sphere_sigma)."""
    n = P / (KB * T)
    vbar = np.sqrt(8 * KB * T / (np.pi * m_gas))
    return n * vbar * 2 * np.pi * radius(m) ** 2


def gas_rate(m, P, T, m_gas, model=None):
    return (gas_rate_kinetic if (model or GAS_MODEL) == "kinetic" else gas_rate_interpolated)(m, P, T, m_gas)


def gt_limit(dphi):
    """Dephasing gamma*tau at which all entanglement is gone, for entangling phase dphi."""
    ph = np.array([[dphi / 2, 0.0], [0.0, dphi / 2]])
    lo, hi = 0.0, 3.0
    for _ in range(50):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if g.negativity(g.state(ph, mid)) > 1e-12 else (lo, mid)
    return lo


# --------------------------------------------------------------------------- H5
def runs_table(dphi_grid, gt_grid):
    """3-sigma run count N(dphi, gamma*tau) for the symmetric (parallel) state."""
    N = np.full((len(dphi_grid), len(gt_grid)), np.inf)
    for a, dp in enumerate(dphi_grid):
        ph = np.array([[dp / 2, 0.0], [0.0, dp / 2]])      # entangling phase dp, no local part
        for b, gt in enumerate(gt_grid):
            rho = g.state(ph, gt)
            if g.negativity(rho) > 1e-12:
                N[a, b] = max(MIN_RUNS, g.runs_for_witness(g.witness_for(rho), rho))
    return N


def ramp_integral(dx, gap, n=2001):
    """I(dx) = int_0^1 [1/gap - 1/sqrt(gap^2 + (dx s(u))^2)] du over one ramp."""
    u = np.linspace(0, 1, n)
    su = ramp_profile(u, 0.0, 1.0)[: n]                   # opening profile on [0, 1]
    return np.trapezoid(1 / gap - 1 / np.sqrt(gap**2 + (dx * su) ** 2), u)


def dphi_fast(m, dx, gap, tau_hold, t_ramp):
    """Same as trajectory_dphi, in closed form per dx (checked against it in the tests)."""
    hold = tau_hold * (1 / gap - 1 / np.sqrt(gap**2 + dx**2))
    return 2 * G * m**2 / HBAR * (hold + 2 * t_ramp * ramp_integral(dx, gap))


def design_search(env, masses, dxs, holds, ramps, gap, table):
    dphi_grid, gt_grid, N = table
    M, DX, TH, TR = np.meshgrid(masses, dxs, holds, ramps, indexing="ij")
    I = np.array([ramp_integral(d, gap) for d in dxs])[None, :, None, None]
    total = TH + 2 * TR
    dp = 2 * G * M**2 / HBAR * (TH * (1 / gap - 1 / np.sqrt(gap**2 + DX**2)) + 2 * TR * I)
    gas = np.array([gas_rate(m, env["P"], env["T_env"], env.get("m_gas", g.M_N2)) for m in masses])
    bb = np.array([[blackbody_rate(m, d, env["T_env"], env["T_int"], env["im_K"]) for d in dxs]
                   for m in masses])
    acc = 0.5 * accel_phase_sigma(M, DX, total, env["asd"]) ** 2
    gt = (gas[:, None, None, None] + bb[:, :, None, None]) * total + acc
    ok = (MU_B * B_GRAD / M * TR**2 / 2 >= DX) & (total <= env["T2"])
    ok &= (dp < dphi_grid[-1]) & (gt < gt_grid[-1])
    ia = np.clip(np.searchsorted(dphi_grid, dp) - 1, 0, len(dphi_grid) - 1)  # round dphi DOWN
    ib = np.clip(np.searchsorted(gt_grid, gt), 0, len(gt_grid) - 1)           # round noise UP
    runs = np.where(ok, N[ia, ib], np.inf)
    wall = runs * (total + T_RESET)
    if not np.isfinite(wall).any():
        return None
    k = np.unravel_index(np.argmin(wall), wall.shape)
    m = M[k]
    return dict(m=m, dx=DX[k], hold=TH[k], ramp=TR[k], total=total[k], dphi=dp[k], gt=gt[k],
                gas=gas[k[0]] * total[k], bb=bb[k[0], k[1]] * total[k], acc=acc[k],
                runs=runs[k], wall=wall[k])


# --------------------------------------------------------------------------- H6
K_COUL = 8.9875517923e9
E_CH = 1.602176634e-19


def em_entangling_ratio(m, dx, gap, tau, q=0.0, p=0.0):
    """Entangling phase from Coulomb (charge q on each) or dipole-dipole (dipole p on each,
    both along the line joining them, worst case 2 k p^2 / r^3), relative to gravity's."""
    r = g.branch_distances(dx, gap, "parallel")
    U = K_COUL * q**2 / r + 2 * K_COUL * p**2 / r**3
    return abs(g.entangling_phase(U * tau / HBAR)) / abs(g.entangling_phase(g.phases(m, dx, gap, tau, "parallel")))


def max_dipole(m, dx, gap, tau, frac=0.1):
    lo, hi = 1e-40, 1e-20
    for _ in range(200):
        mid = np.sqrt(lo * hi)
        lo, hi = (mid, hi) if em_entangling_ratio(m, dx, gap, tau, p=mid) <= frac else (lo, mid)
    return lo


def envelope(key, base, search, lo, hi, increasing_is_harder=True, iters=14):
    """Bisect (in log) the value of env[key] at which a working design stops existing."""
    def works(v):
        return search({**base, key: v}) is not None
    if not works(lo if increasing_is_harder else hi):
        return np.nan
    a, b = np.log(lo), np.log(hi)
    for _ in range(iters):
        mid = 0.5 * (a + b)
        if works(np.exp(mid)) == increasing_is_harder:
            a = mid
        else:
            b = mid
    return np.exp(0.5 * (a + b))


def main():
    b = g.BASE
    gap = g.casimir_vs_gravity_gap(b["m"], b["dx"], b["tau"], "parallel")

    banner("H0  Casimir-safe gap does not depend on the mass (parallel geometry)")
    for m in (1e-16, 1e-15, 1e-14, 1e-13, 1e-12):
        print(f"   m = {m:.0e} kg: Casimir < 10% of gravity for gap > "
              f"{g.casimir_vs_gravity_gap(m, b['dx'], b['tau'], 'parallel')*1e6:.1f} um")
    print("   FOLLOWS: Casimir ~ R^6 / r^7 and gravity ~ m^2 / r ~ R^6 / r, so their ratio is")
    print("   mass-independent. Lighter diamonds cannot be brought closer to compensate.")
    print(f"   Gap used below: {gap*1e6:.1f} um.")

    banner("H1  Split and recombine stages (phases integrated along the trajectories)")
    print("   ramp t_r (s)   total time (s)   dphi with ramps   hold-only dphi   ratio")
    for tr in (0.0, 0.25, 0.5, 1.0):
        dpt = trajectory_dphi(b["m"], b["dx"], gap, b["tau"], tr)
        dph = hold_dphi(b["m"], b["dx"], gap, b["tau"])
        print(f"   {tr:12.2f}   {b['tau']+2*tr:14.2f}   {dpt:15.4f}   {dph:14.4f}   {dpt/dph:5.3f}")
    print("   FOLLOWS: the ramps ADD entangling phase (the branches are already partly open),")
    print("   but they also add time in which every noise source acts.")

    banner("H2  Blackbody decoherence (LIT formulas; Im K is an ASSUMPTION, scanned)")
    budget = 0.289 / (b["tau"] + 1.0) / 3      # one third of the total budget per mass, 0.5 s ramps
    lam_th = HBAR * C / (KB * 0.15)
    print(f"   Thermal wavelength at 0.15 K: {lam_th*1e3:.1f} mm (>> dx: the dx^2 regime holds)")
    print(f"   Rates at T_env = T_int = 0.15 K, dx = 250 um: scattering "
          f"{lambda_bb_scatter(b['m'], 0.15)*b['dx']**2:.1e} /s, emission (Im K = 0.01) "
          f"{lambda_bb_emit(b['m'], 0.15, 0.01)*b['dx']**2:.1e} /s")
    print(f"   Budget given to blackbody (1/3 of total): {budget:.3f} /s. Highest internal temperature:")
    for imk in (1e-3, 1e-2, 1e-1):
        print(f"     Im K = {imk:.0e}:  T_int < {max_internal_T(b['m'], b['dx'], budget, 0.15, imk):.2f} K")
    print("   FOLLOWS: scattering is negligible; emission from the diamond's own heat is what")
    print("   counts. The diamond must stay near 1 K inside, which rules out trapping it with")
    print("   absorbed laser light for the whole sequence (it must fly free or be held magnetically).")

    banner("H3  Acceleration noise: random phases shot to shot")
    ph = g.phases(**b, geometry="parallel")
    s_ind = sigma_threshold(ph, "indep")
    s_com = sigma_threshold(ph, "common")
    s_anti = sigma_threshold(ph, "anti")
    print(f"   Phase noise that cuts the entanglement to 10%: independent {s_ind:.3f} rad,"
          f" common {s_com:.3f} rad, anti-correlated {s_anti:.3f} rad")
    k = b["m"] * b["dx"] / HBAR
    print(f"   Phase per unit acceleration, (m dx / hbar) tau = {k*b['tau']:.2e} rad per m/s^2")
    asd_req = s_ind / (k * np.sqrt(b["tau"] / 2))
    print(f"   Required acceleration noise (independent, white): ASD < {asd_req:.1e} m s^-2 /sqrt(Hz)")
    print(f"   LIT LISA Pathfinder, best free-fall test mass ever: {LPF_ASD:.2e} m s^-2 /sqrt(Hz)")
    asd_com = s_com / (k * np.sqrt(b["tau"] / 2))
    print(f"   -> {LPF_ASD/asd_req:.0f} times quieter than LISA Pathfinder for independent noise;")
    print(f"      if the noise is common to both diamonds: ASD < {asd_com:.1e} ({LPF_ASD/asd_com:.0f}x).")
    print("      Common noise is tolerated somewhat better (it leaves the |01>-|10> coherence")
    print("      intact) but is still a random local phase on each diamond. The real cure is")
    print("      to measure and subtract it, or to let it cancel inside each interferometer.")

    banner("H4  The split itself: one electron spin has to open a whole diamond")
    print(f"   Field gradient {B_GRAD:.0e} T/m (LIT, Bose et al.): force mu_B dB/dz = {MU_B*B_GRAD:.2e} N")
    for m in (1e-15, 1e-14, 1e-13):
        print(f"   m = {m:.0e} kg: max dx in t_r = 0.5 s: {max_split(m, 0.5)*1e6:7.1f} um;"
              f" t_r needed for 250 um: {np.sqrt(2*250e-6*m/(MU_B*B_GRAD)):.2f} s")
    print("   FOLLOWS: m * dx is fixed by the ramp time. A heavier diamond splits less, and")
    print("   the whole sequence (ramps + hold) must fit inside the NV spin's coherence time.")

    banner("H5  Full design search (gap = Casimir-safe, every noise source on)")
    dphi_grid = np.linspace(0, np.pi, 241)
    gt_grid = np.linspace(0, 0.8, 161)
    table = (dphi_grid, gt_grid, runs_table(dphi_grid, gt_grid))
    masses, dxs, holds, ramps = MASSES, DXS, HOLDS, RAMPS

    def search(env):
        return design_search(env, masses, dxs, holds, ramps, gap, table)

    base_env = BASE_ENV
    scenarios = [
        ("A  Bose target (1e-15 Pa N2, 0.15 K), no acceleration noise, unlimited spin coherence", base_env),
        ("A' as A, but the leftover gas is helium (typical in a cryostat)", {**base_env, "m_gas": M_HE}),
        ("B  A + spin coherence limited to 1.6 s", {**base_env, "T2": NV_T2_BEST}),
        ("C  A + internal temperature 4 K", {**base_env, "T_int": 4.0}),
        ("D  A + vacuum 1e-14 Pa", {**base_env, "P": 1e-14}),
        ("E  A + LISA Pathfinder acceleration noise", {**base_env, "asd": LPF_ASD}),
    ]
    results = {}
    for name, env in scenarios:
        r = search(env)
        results[name.split()[0]] = r
        print(f"   {name}")
        if r is None:
            print("      NO design works: entanglement cannot be certified at any mass, dx or time.")
            continue
        print(f"      m = {r['m']:.1e} kg, dx = {r['dx']*1e6:.0f} um, hold {r['hold']:.2f} s,"
              f" ramps 2 x {r['ramp']:.2f} s, dphi = {r['dphi']:.3f} rad")
        print(f"      dephasing gamma*tau: gas {r['gas']:.3f}, blackbody {r['bb']:.1e},"
              f" acceleration {r['acc']:.1e}  (total {r['gt']:.3f}; limit at this dphi {gt_limit(r['dphi']):.3f})")
        print(f"      {r['runs']:.0f} runs -> {r['wall']/3600:.1f} h of running for 3 sigma")

    global GAS_MODEL
    banner("H5b  The gas-collision rate, derived (it decides design A)")
    print("   For a split much larger than the body and than the gas wavelength, each collision resolves")
    print("   the branches, so Gamma = n <v> sigma_tot. Exact quantum hard-sphere cross-section:")
    print("      kR       sigma_tot / (pi R^2)")
    for kR in (100, 1000, 3000):
        print(f"      {kR:5d}    {hard_sphere_sigma(kR):.4f}")
    A = design_a()
    for lab, mg in (("N2", g.M_N2), ("He", M_HE)):
        kR = np.sqrt(2 * mg * KB * 0.15) / HBAR * A["R"]
        print(f"   {lab} at 0.15 K on design A's {A['R'] * 1e6:.3f}-um diamond: kR = {kR:.0f},"
              " so sigma_tot = 2 pi R^2 (extinction paradox).")
    ratio = gas_rate_interpolated(A["m"], 1e-15, 0.15, g.M_N2) / gas_rate_kinetic(A["m"], 1e-15, 0.15, g.M_N2)
    print(f"   The interpolation used before (LIT: Romero-Isart 2011, eq. 27, gamma = lambda_th^2 Lambda) is")
    print(f"   {ratio:.2f}x the derived collision rate. It extends the long-wavelength coefficient into the")
    print("   saturated regime with a Gaussian, so it is an estimate. The derived rate is used above.")
    GAS_MODEL = "interpolated"
    old = {name.split()[0]: search(env) for name, env in scenarios}
    GAS_MODEL = "kinetic"
    print("   Scenario   interpolated gas rate          derived gas rate (above)")
    for name, _ in scenarios:
        k = name.split()[0]
        fmt = lambda r: "no design works" if r is None else f"{r['runs']:.0f} runs, {r['wall']/3600:.1f} h"
        print(f"   {k:8s}   {fmt(old[k]):28s}   {fmt(results[k])}")
    oA = old["A"]
    A = design_a()
    assert (oA["m"], oA["dx"], oA["hold"], oA["ramp"]) == (A["m"], A["dx"], A["hold"], A["ramp"])
    fixed = design_search(base_env, np.array([oA["m"]]), np.array([oA["dx"]]), np.array([oA["hold"]]),
                          np.array([oA["ramp"]]), gap, table)
    results["A_fixed"] = fixed
    print(f"   Design A ({A['m']:.3e} kg, {A['dx'] * 1e6:.0f} um, {A['total']:.2f} s), the reference geometry"
          " used across the repository:")
    print(f"      gas gamma*tau {oA['gas']:.3f} -> {fixed['gas']:.3f};  {oA['runs']:.0f} -> {fixed['runs']:.0f} runs"
          f" ({fixed['wall']/3600:.1f} h; {MIN_RUNS} runs, 30 per setting, is the protocol minimum)")

    print("   Requirement envelope: each varied alone. Column 1: everything else at target A")
    print("   (1e-15 Pa N2). Column 2: everything else ideal (1e-17 Pa), the best case.")
    print("   Requirement                              others at target     others ideal")
    rows = [
        ("Internal temperature: highest (K)", "T_int", 0.15, 50.0, True, "{:.2f}"),
        ("Spin coherence: shortest (s)", "T2", 0.1, 100.0, False, "{:.2f}"),
        ("Accel. noise: highest ASD (m/s^2/rtHz)", "asd", 1e-22, 1e-13, True, "{:.1e}"),
    ]
    env_req = {}
    for label, key, lo, hi, harder, fmt in rows:
        vals = [envelope(key, base_env, search, lo, hi, harder),
                envelope(key, {**base_env, "P": 1e-17}, search, lo, hi, harder)]
        env_req[key] = vals
        out = [("none" if not np.isfinite(v) else fmt.format(v)) for v in vals]
        print(f"   {label:40s}  {out[0]:>12s}     {out[1]:>12s}")
    vac = [envelope("P", base_env, search, 1e-18, 1e-12, True),
           envelope("P", {**base_env, "m_gas": M_HE}, search, 1e-18, 1e-12, True)]
    env_req["P"] = vac
    print(f"   Vacuum, highest pressure (Pa), others ideal:  N2 {vac[0]:.1e},  He {vac[1]:.1e}")

    banner("H6  EM forces that CAN fake entanglement (unlike noise, they are interactions)")
    rA0 = results["A"]
    rq1 = em_entangling_ratio(rA0["m"], rA0["dx"], gap, rA0["total"], q=E_CH)
    pmax = max_dipole(rA0["m"], rA0["dx"], gap, rA0["total"])
    print(f"   One electron charge on each diamond: Coulomb/gravity entangling phase = {rq1:.1e}")
    print("   -> both diamonds must carry EXACTLY zero net charge. LIT: levitated microspheres")
    print("      have been discharged to zero net charge (Moore, Rider & Gratta, PRL 113, 251801 (2014)).")
    print(f"   Permanent electric dipole, worst orientation: < {pmax:.1e} C m"
          f" = {pmax/(E_CH*1e-6):.1e} e*um for EM < 10% of gravity")
    print("   (Patch potentials and trapped charges in diamond typically give far larger dipoles;")
    print("    a conducting shield between the diamonds, LIT van de Kamp et al. PRA 102, 062807")
    print("    (2020), screens EM while leaving gravity untouched.)")
    print("   -> A positive result means gravity only after charge = 0, dipoles bounded or")
    print("      screened, and Casimir subtracted. Controls: run with the shield, with")
    print("      deliberately charged diamonds, and at several gaps (gravity 1/r, dipole 1/r^3).")

    banner("H7  What comes out")
    rA = results["A"]
    print("   Requirement                     Needed (computed above)     State of the art (LIT)")
    print(f"   Mass in a spatial superposition {rA['m']:.1e} kg                  "
          f"{MAX_MASS_SUPERPOSED:.0e} kg (Fein 2019): x{rA['m']/MAX_MASS_SUPERPOSED:.0e}")
    print(f"   Superposition size              {rA['dx']*1e6:.0f} um")
    print(f"   Vacuum                          < {env_req['P'][0]:.0e} Pa (N2), < {env_req['P'][1]:.0e} Pa (He)")
    print(f"   Spin coherence                  > {env_req['T2'][0]:.1f} s (best case {env_req['T2'][1]:.1f} s)    ~1 s (NV, cryogenic, decoupled)")
    print(f"   Internal temperature            < {env_req['T_int'][0]:.2f} K (best case {env_req['T_int'][1]:.1f} K)")
    print(f"   Acceleration noise              < {env_req['asd'][0]:.0e} m/s^2/rtHz (best case {env_req['asd'][1]:.0e})   "
          f"{LPF_ASD:.0e} (LISA Pathfinder): x{LPF_ASD/env_req['asd'][0]:.0f}")
    ph = np.array([[rA["dphi"] / 2, 0.0], [0.0, rA["dphi"] / 2]])
    W = g.witness_for(g.state(ph, rA["gt"]))
    lam_lo = np.nan
    for lam in np.linspace(0.001, 1, 1000):
        if g.runs_for_witness(W, g.state(lam * ph, rA["gt"])) <= 1e6:
            lam_lo = lam
            break
    print(f"   Zero net charge; dipole        < {pmax:.0e} C m, or a conducting shield")
    print(f"   lambda reach of the best design with 1e6 runs: lambda > {lam_lo:.2f} (dephasing floor, H5)")
    rq = search({**base_env, "P": 1e-17})
    ph = np.array([[rq["dphi"] / 2, 0.0], [0.0, rq["dphi"] / 2]])
    W = g.witness_for(g.state(ph, rq["gt"]))
    lam_q = np.nan
    for lam in np.linspace(0.001, 1, 1000):
        if g.runs_for_witness(W, g.state(lam * ph, rq["gt"])) <= 1e6:
            lam_q = lam
            break
    print(f"   ... and at 1e-17 Pa: best design {rq['runs']:.0f} runs ({rq['wall']/3600:.2f} h),"
          f" lambda reach {lam_q:.3f}")

    banner("VERDICT")
    print("   1. Nothing in the physics forbids the test. At the published targets (N2) the best")
    print(f"      design needs {rA['runs']:.0f} runs, {rA['wall']/3600:.1f} h, and settles lambda = 0 vs 1.")
    he, dv = results["A'"], results["D"]
    print("      Margin: " + ("on the edge: with helium as the leftover gas, or 10x worse vacuum, no design works."
                     if he is None and dv is None else
                     f"with helium as the leftover gas {'no design works' if he is None else f'{he[chr(114)+chr(117)+chr(110)+chr(115)]:.0f} runs'};"
                     f" at 10x worse vacuum {'none' if dv is None else f'{dv[chr(119)+chr(97)+chr(108)+chr(108)]/3600:.0f} h'}."))
    print("   2. The split field (lambda = 0) predicts exactly zero gravitational entanglement.")
    print("      Noise cannot create entanglement, it can only hide it. EM interactions CAN create")
    print("      it, so charge must be zero and dipoles screened before a positive witness")
    print("      means gravity (H6).")
    print(f"   3. What binds: mass in superposition (x{rA['m']/MAX_MASS_SUPERPOSED:.0e} beyond today), vacuum,")
    print(f"      acceleration noise (x{LPF_ASD/env_req['asd'][0]:.0f} below LISA Pathfinder), spin coherence")
    print(f"      (> {env_req['T2'][0]:.1f} s), internal temperature (< {env_req['T_int'][0]:.2f} K), all at once.")
    print("   4. The question 'is gravity's field split, or in two places?' is open, and what")
    print("      stands between it and an answer is engineering, not theory.")


if __name__ == "__main__":
    main()
