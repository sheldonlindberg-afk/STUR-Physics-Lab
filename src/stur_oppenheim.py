#!/usr/bin/env python3
"""
Oppenheim's classical gravity: the decoherence-diffusion trade-off, and what one
levitated particle can decide.

LIT (retrieved, read in this work): Oppenheim, Sparaciari, Soda, Weller-Davies,
"Gravitationally induced decoherence vs space-time diffusion: testing the quantum nature
of gravity", arXiv:2203.01982 (Nat. Commun. 14, 7910 (2023)). Their eq. (29): a
classical field coupled to quantum matter by a completely positive Markovian map obeys
       [[2 D2, D1], [D1, D0]]  >= 0          (matrix-kernel positivity)
In the Newtonian limit (their eqs. 35-41) the potential is sourced by the mass density
plus a random mass J,  lap Phi = 4 pi G (m + J),  E[J J] = 2 D2 delta(t - t'),  and the
back-reaction D1 = -1/2 on each side (their eq. 38 sums the two Hermitian halves).

Conventions here (two-sided spectra; white in time; translation invariant):
  * decoherence:  d ln rho_LR / dt = -(1/2) Int Dm(x) D0(x - y) Dm(y)   (their eq. 43)
  * random mass:  <J(x,t) J(y,t')> = S_J(x - y) delta(t - t'),   S_J = 2 D2
  * trade-off per Fourier mode:  D0(q) S_J(q) >= g(q)^2 / 4
    where g(q) is the smearing of the mass density that sources Phi (g = 1: local,
    Oppenheim et al.'s assumption; g = exp(-q^2 R0^2 / 2): the repository's R0).

P1  CHECK. The trade-off constant, on a qubit coupled to one classical variable.
P2  FOLLOWS. Matter feels the noisy Phi through H_I = Int Phi m (their eq. 35). The
    total decoherence is then >= the Diosi-Penrose kernel at every q: the
    Tilloy-Diosi floor of src/stur_thermo_gravity.py Q1 is the minimised Oppenheim
    trade-off, so COLLECTIVE.md's argument covers Oppenheim's continuous class.
P3  CHECK (a worked example; not new, see NOVELTY.md). Without P2's back-action step, using only the trade-off: one
    particle, measured two ways, obeys a shape-free bound
          Gamma(dx) * S_a  >=  (M^2 / 4) I(dx)^2,
          I = Int d3q/(2pi)^3  (4 pi G / q^2) |F(q)|^2 |q_z| sqrt(1 - cos q_z dx)
    for every pair of kernels D0, S_J allowed by the trade-off (tight).
P5  CHECK (a worked example; not new, see NOVELTY.md). Kernel-free: Gamma * S_a >= (1/8)(F_LR/M)^2 for every CQ model, continuous or
    discrete, from the operator form of the trade-off. Largest at split = radius.
P4  FOLLOWS. Small splits: the same trade-off fixes a minimum centre-of-mass heating,
          d<p_z^2>/dt >= (4 pi / 3) hbar G M^2 Int rho_hat^2.
    For local coupling (g = 1), or smearing at the entanglement cutoff a, the nuclei set
    rho_hat and the floor is ~0.5 W/kg of internal heating: excluded by the Earth's heat
    flow (this corrects the point-nucleus 1e60 W/kg of stur_thermo_gravity.py Q3). Once
    R0 >= 0.54 Angstrom the centre-of-mass heating floor is ~1e-12 phonons/s: too small
    to see, so the deciding single-particle test is coherence at a large split (P2, P3).
"""
import numpy as np

G, hbar, c = 6.67430e-11, 1.054571817e-34, 2.99792458e8
u_amu = 1.66053906660e-27
lP = np.sqrt(hbar * G / c**3)
c_s = 0.3046

M_A, R_A, D_A, T_A = 1.5e-14, 1.007e-6, 721e-6, 3.24       # design A (GRAVITY_ENTANGLEMENT)
GAMMA_BUDGET = 0.12          # /s per diamond, total dephasing budget (GRAVITY_ENTANGLEMENT G3)
ASD_REQ = 3.1e-17            # m s^-2 /sqrt(Hz), one-sided: the vibration requirement (H5 envelope, derived gas rate)
R0_DONADI = 0.54e-10         # LIT: Donadi et al., Nature Phys. 17, 74 (2021)
L_ISL = 52e-6                # LIT recalled: Lee et al., PRL 124, 101101 (2020)
EARTH_W_PER_KG = 47e12 / 5.972e24   # LIT recalled: ~47 TW of internal heat flow

# a 100-nm-diameter silica nanosphere, a femtogram particle as in cryogenic levitation
# (LIT: Tebbenjohanns et al., arXiv:2103.03853); trap frequency is an ASSUMPTION.
R_NANO, RHO_SIO2, OMEGA_NANO = 50e-9, 2200.0, 2 * np.pi * 50e3


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


def cutoff(N):
    return np.sqrt(N * c_s / np.pi) * lP


def sphere_ff(x):
    x = np.asarray(x, float)
    out = np.ones_like(x)
    s = x > 1e-3
    xs = x[s]
    out[s] = 3 * (np.sin(xs) - xs * np.cos(xs)) / xs**3
    out[~s] = 1 - x[~s] ** 2 / 10
    return out


def nuclear_radius(A):
    return 1.2e-15 * A ** (1 / 3)


# ---------------------------------------------------------------- P1: qubit check
def qubit_positivity(r, alpha=1.0, Dvar=1.0, t=1.0, nz=4001):
    """Qubit (X = sigma_z, eigenvalues +-1) drives a classical z: dz = alpha X dt + noise.
    D0 = r * alpha^2 / (4 Dvar). Returns min over z of rho00 rho11 - |rho01|^2,
    in units of rho00 rho11 at z = 0, for the CQ state from |+><+| with z = 0."""
    D0 = r * alpha**2 / (4 * Dvar)
    s2 = Dvar * t
    z = np.linspace(-8, 8, nz) * np.sqrt(s2)
    gauss = lambda mu: np.exp(-(z - mu) ** 2 / (2 * s2)) / np.sqrt(2 * np.pi * s2)
    r00, r11 = 0.5 * gauss(alpha * t), 0.5 * gauss(-alpha * t)
    r01 = 0.5 * np.exp(-0.5 * D0 * 4 * t) * gauss(0.0)       # (x0 - x1)^2 = 4
    det = r00 * r11 - r01**2
    return (det / (r00 * r11)).min()


def qubit_measurement_feedback(N=0.37, alpha=1.3, t=1.0, nz=4001):
    """Continuous measurement of X with record noise N, z = alpha * record.
    Returns (D0, Dvar, D0 * Dvar / (alpha^2/4), min det)."""
    s2 = N * t
    z = np.linspace(-10, 10, nz) * np.sqrt(alpha**2 * s2)
    like = lambda x: np.exp(-(z / alpha - x * t) ** 2 / (2 * s2)) / np.sqrt(2 * np.pi * s2) / alpha
    p0, p1 = like(1.0), like(-1.0)
    r00, r11, r01 = 0.5 * p0, 0.5 * p1, 0.5 * np.sqrt(p0 * p1)
    dz = z[1] - z[0]
    coh = 2 * np.trapezoid(r01, dx=dz)                  # |rho01| integrated over z
    D0 = -np.log(coh) / (0.5 * 4 * t)
    Dvar = alpha**2 * N
    return D0, Dvar, D0 * Dvar / (alpha**2 / 4), (r00 * r11 - r01**2).min()


# ------------------------------------------------- P2: back-action gives the DP floor
def total_decoherence_kernel(D0, q, g=1.0):
    """D0(q) + K^2 S_J / hbar^2 with S_J at the trade-off minimum g^2/(4 D0)."""
    K = 4 * np.pi * G / q**2
    return D0 + K**2 * g**2 / (4 * D0) / hbar**2


def min_total_over_D0(q, g=1.0):
    K = 4 * np.pi * G / q**2
    D0s = (K * g / (2 * hbar)) * np.logspace(-3, 3, 6001)
    vals = total_decoherence_kernel(D0s, q, g)
    i = np.argmin(vals)
    return vals[i] / (K * g / hbar), D0s[i] / (K * g / (2 * hbar))


# ------------------------------------------------- P3: shape-free one-particle bound
def h_abs(k):
    """Int_0^1 u |sin(k u)| du, exactly."""
    k = np.asarray(k, float)
    out = np.empty_like(k)
    small = k < 1e-6
    out[small] = k[small] / 3
    kk = k[~small]
    Mn = np.floor(kk / np.pi)
    out[~small] = (np.pi * Mn**2 + np.pi * Mn + (-1) ** Mn * (np.sin(kk) - kk * np.cos(kk))) / kk**2
    return out


def I_joint(dx, R=R_A, R0=0.0, n=2_000_000):
    """I(dx) for a uniform sphere of radius R, source smeared by exp(-q^2 R0^2 / 2)."""
    qmax = 200 / R if R0 < R / 50 else min(200 / R, 12 / R0)
    q = np.linspace(qmax / n, qmax, n)
    f = q * sphere_ff(q * R) ** 2 * np.exp(-(q * R0) ** 2) * 2 * h_abs(q * dx / 2)
    val = np.trapezoid(f, q)
    if R0 < R / 50:                       # tail: <|F|^2> = 4.5/(qR)^4, h -> 1/pi
        val += (2 / np.pi) * 4.5 / R**4 / (2 * qmax**2)
    return np.sqrt(2) * G / np.pi * val


def I_split_limit(R):
    return 2 * np.sqrt(2) * G / (np.pi**2 * R**2) * 9 / 4


def r0_where_bound_meets_requirement():
    from scipy.optimize import brentq
    f = lambda lr: np.log(np.sqrt(2 * joint_bound(D_A, R0=np.exp(lr)) / GAMMA_BUDGET) / ASD_REQ)
    return np.exp(brentq(f, np.log(1e-6), np.log(1e-3)))


def joint_bound(dx, M=M_A, R=R_A, R0=0.0):
    return M**2 / 4 * I_joint(dx, R, R0) ** 2


def grid_gamma_Sa(D0_fn, SJ_fn, dx, M=M_A, R=R_A, nq=3000, nu=400):
    """Gamma and S_a on a (q, u = cos theta) grid for arbitrary kernels D0(q,u), S_J(q,u)."""
    q = np.logspace(np.log10(1e-3 / dx), np.log10(300 / R), nq)[:, None]
    uu = np.linspace(-1, 1, nu)[None, :]
    F2 = sphere_ff(q * R) ** 2
    K = 4 * np.pi * G / q**2
    qz = q * uu
    w1 = M**2 * F2 * (1 - np.cos(qz * dx))
    w2 = F2 * qz**2 * K**2
    meas = q**2 / (2 * np.pi) ** 3 * 2 * np.pi     # d3q = q^2 dq dphi du
    integ = lambda a: np.trapezoid(np.trapezoid(a * meas, uu[0], axis=1), q[:, 0])
    D0, SJ = D0_fn(q, uu), SJ_fn(q, uu)
    bound_grid = M**2 / 4 * integ(np.sqrt(F2**2 * K**2 * qz**2 * (1 - np.cos(qz * dx)))) ** 2
    return integ(D0 * w1), integ(SJ * w2), bound_grid, (w1, w2)


# ------------------------------------------------- P4: heating floors
def int_rho2_sphere(R, R0=0.0, n=400_000):
    """Int rho_hat^2 d3x for a uniform sphere (normalised), smeared by Gaussian R0."""
    if R0 == 0.0:
        return 3 / (4 * np.pi * R**3)
    qmax = min(60 / R, 12 / R0) if R0 < 10 * R else 12 / R0
    q = np.linspace(qmax / n, qmax, n)
    val = np.trapezoid(q**2 * sphere_ff(q * R) ** 2 * np.exp(-(q * R0) ** 2), q) / (2 * np.pi**2)
    if R0 < R / 50:
        val += 4.5 / R**4 / qmax / (2 * np.pi**2)
    return val


def int_rho2_body(M, R, nuclei, R0=0.0):
    """Coherent (whole sphere) + incoherent (nuclei) parts of Int rho_hat^2.
    nuclei: list of (A, fraction of mass). Nuclei are uniform spheres 1.2 A^(1/3) fm."""
    coh = int_rho2_sphere(R, R0)
    inc = 0.0
    for A, frac in nuclei:
        m_i = A * u_amu
        N_i = frac * M / m_i
        inc += N_i * (m_i / M) ** 2 * int_rho2_sphere(nuclear_radius(A), R0)
    return coh, inc


def cm_heating_floor(M, rho2):
    """Minimum d<p_z^2>/dt of the centre of mass, any continuous Markovian CQ gravity."""
    return 4 * np.pi / 3 * hbar * G * M**2 * rho2


def internal_heating_per_kg(nuclei, R0=0.0):
    """Every nucleus heated at its own floor: 3 axes, energy = p^2/2m, per kg."""
    tot = 0.0
    for A, frac in nuclei:
        m_i = A * u_amu
        tot += frac * 3 * cm_heating_floor(m_i, int_rho2_sphere(nuclear_radius(A), R0)) / (2 * m_i) / m_i
    return tot


DIAMOND = [(12, 1.0)]
SILICA = [(28, 28 / 60), (16, 32 / 60)]


# ------------------------------------------------- P5: kernel-free bound (any CQ model)
def sphere_force_closed(d, R=R_A, M=M_A):
    """Newtonian force between two uniform spheres (radius R, mass M) at centre distance d."""
    if d >= 2 * R:
        return G * M**2 / d**2
    x = d / R
    return G * M**2 / R**2 * x * (1 - 9 * x / 16 + x**3 / 32)


def sphere_force_fourier(d, R=R_A, M=M_A, n=2_000_000):
    """Same force from the Fourier integral, as a check."""
    qmax = 400 / R
    q = np.linspace(qmax / n, qmax, n)
    k = q * d
    g = np.where(k > 1e-4, (np.sin(k) - k * np.cos(k)) / np.maximum(k, 1e-300) ** 2, k / 3)
    return 2 * G * M**2 / np.pi * np.trapezoid(q * sphere_ff(q * R) ** 2 * g, q)


def general_bound(d, R=R_A, M=M_A):
    """Gamma * S_a >= (1/8) |<Delta m, w>|^2 = (1/8) (F_LR / M)^2, any kernel."""
    return (sphere_force_closed(d, R, M) / M) ** 2 / 8


def operator_check(n=40, trials=200, seed=3):
    """Finite-dimensional test of the operator inequality behind P5: for random S > 0,
    D0 >= S^-1/4 and vectors dm, w: (1/2 dm.D0.dm)(w.S.w) >= |dm.w|^2 / 8, with equality
    reachable (D0 = S^-1/4, w parallel to S^-1 dm)."""
    rng = np.random.default_rng(seed)
    worst = np.inf
    for _ in range(trials):
        A = rng.normal(size=(n, n)); S = A @ A.T + 0.1 * np.eye(n)
        B = rng.normal(size=(n, n)) * rng.uniform(0, 1)
        D0 = np.linalg.inv(S) / 4 + B @ B.T
        dm, w = rng.normal(size=n), rng.normal(size=n)
        lhs = 0.5 * dm @ D0 @ dm * (w @ S @ w)
        worst = min(worst, lhs / ((dm @ w) ** 2 / 8))
    A = rng.normal(size=(n, n)); S = A @ A.T + 0.1 * np.eye(n)
    dm = rng.normal(size=n); w = np.linalg.solve(S, dm)
    sat = 0.5 * dm @ (np.linalg.inv(S) / 4) @ dm * (w @ S @ w) / ((dm @ w) ** 2 / 8)
    return worst, sat


def main():
    banner("P1  The trade-off constant, checked on a qubit (CHECK)")
    print("   D0 * Dvar / (alpha^2/4)    min_z [rho00 rho11 - |rho01|^2] / (rho00 rho11)")
    for r in (0.5, 0.9, 0.99, 1.0, 1.01, 2.0):
        print(f"   {r:6.2f}                     {qubit_positivity(r):+.6f}")
    D0, Dv, ratio, mdet = qubit_measurement_feedback()
    print(f"   Measurement + feedback (record noise 0.37, gain 1.3): D0 Dvar / (alpha^2/4) = {ratio:.6f},")
    print(f"   min det = {mdet:.1e}. It sits exactly on the bound: below it the CQ state is not positive.")
    print("   With Oppenheim et al.'s D1 = -1/2 and S_J = 2 D2, their eq. (29) is the same statement:")
    print("   D0(q) S_J(q) >= g(q)^2 / 4 for every Fourier mode of the mass density.")

    banner("P2  Matter feels the noisy potential: the total decoherence floor (FOLLOWS)")
    print("   q (1/m)    min over D0 of [D0 + K^2 S_J/hbar^2] / (4 pi G/hbar q^2)   D0 at min / (K/2hbar)")
    worst = 0.0
    for q in (1e2, 1e6, 1e10, 1e14):
        v, d = min_total_over_D0(q)
        worst = max(worst, abs(v - 1))
        print(f"   {q:8.0e}   {v:.6f}                                               {d:.4f}")
    print(f"   The floor is the Diosi-Penrose kernel (grid deviation {worst:.1e}): exactly the")
    print("   Tilloy-Diosi minimum of src/stur_thermo_gravity.py Q1. So every continuous, Markovian,")
    print("   translation-invariant CQ gravity in Oppenheim's class is covered by COLLECTIVE.md, and")
    print("   the design-A diamond's 3.24 s coherence tests it for any smearing R0 below 455 um.")

    banner("P3  One particle measured two ways: Gamma x S_a (worked example)")
    print(f"   Design-A diamond, M = {M_A:.1e} kg, R = {R_A*1e6:.3f} um, split {D_A*1e6:.0f} um.")
    print("   Uses only the trade-off: no assumption on how the noise acts back on the matter.")
    print("   R0 (m)       I (m/kg/s^2)   bound Gamma*S_a (m^2/s^4)   S_a if Gamma <= 0.12/s:")
    print("                                                         one-sided ASD (m s^-2/rtHz)  / requirement")
    rows = []
    for R0 in (0.0, R0_DONADI, 1e-7, 1e-6, 1e-5, L_ISL):
        I = I_joint(D_A, R0=R0)
        B = M_A**2 / 4 * I**2
        asd = np.sqrt(2 * B / GAMMA_BUDGET)
        rows.append((R0, I, B, asd))
        print(f"   {R0:9.2e}    {I:.4e}     {B:.4e}                 {asd:.3e}                 {asd/ASD_REQ:.1e}")
    I_inf = I_split_limit(R_A)
    print(f"   Check: for split >> R, I -> (2 sqrt2 G / pi^2 R^2) Int x f(x)^2 dx = {I_inf:.4e}")
    print(f"   (Int x f^2 dx = 9/4 for a uniform sphere); the full integral gives {rows[0][1]:.4e}.")
    R0x = r0_where_bound_meets_requirement()
    print("   Reading: if the diamond keeps coherence (Gamma within the 0.12 /s budget), a classical")
    print("   (CQ) gravity must shake it with at least the acceleration noise in the last columns.")
    print("   Design A already requires the noise to be lower than that, by the factor shown, for")
    print(f"   every R0 up to {R0x*1e6:.0f} um, which covers all R0 the inverse-square law allows ({L_ISL*1e6:.0f} um).")
    print("   So a coherent, quiet design-A diamond excludes every continuous Markovian CQ gravity,")
    print("   whatever the kernel shapes, without the back-action step of P2. A uniform sphere is")
    print("   used for F(q); the nuclei only add to I, so the bound is conservative.")

    banner("P4  Small splits: the minimum heating of matter (FOLLOWS)")
    print("   Every nucleus at its own floor (local coupling, g = 1; nuclei as uniform spheres):")
    for name, nuc in (("diamond", DIAMOND), ("silica", SILICA)):
        print(f"     {name:8s}: {internal_heating_per_kg(nuc):.2f} W/kg of internal heating")
    a1 = cutoff(1)
    print(f"   Smearing at the entanglement cutoff, R0 = a = {a1:.1e} m, changes nothing: the nuclei are")
    print(f"   already ~1e-15 m across (diamond {internal_heating_per_kg(DIAMOND, a1):.2f} W/kg). The point-nucleus formula")
    print("   hbar G / (4 sqrt(pi) R0^3) of src/stur_thermo_gravity.py Q3 holds only for R0 >> 1 fm;")
    print("   its 1e60 W/kg at R0 = a is an artefact of point nuclei. The real figure is ~0.5 W/kg.")
    print(f"   Earth's internal heat flow is {EARTH_W_PER_KG:.1e} W/kg (LIT recalled): local continuous CQ")
    print(f"   gravity is excluded by a factor {internal_heating_per_kg(SILICA)/EARTH_W_PER_KG:.0e}. It needs a smearing R0; the radiation bound")
    print(f"   already demands R0 >= 0.54 Angstrom (consistent with Oppenheim et al.'s own remark that")
    print("   continuous models with noise everywhere are ruled out).")
    M_n = RHO_SIO2 * 4 / 3 * np.pi * R_NANO**3
    print(f"\n   Centre-of-mass heating floor, in phonons/s (trap {OMEGA_NANO/2/np.pi/1e3:.0f} kHz, ASSUMPTION):")
    print(f"   R0 (m)       100-nm silica ({M_n:.2e} kg)    design-A diamond (at the same trap)")
    out = {}
    for R0 in (0.0, R0_DONADI, 1e-9, 1e-8):
        res = []
        for M, R, nuc in ((M_n, R_NANO, SILICA), (M_A, R_A, DIAMOND)):
            coh, inc = int_rho2_body(M, R, nuc, R0)
            rate = cm_heating_floor(M, coh + inc) / (2 * M * hbar * OMEGA_NANO)
            res.append(rate)
        out[R0] = res
        print(f"   {R0:9.2e}    {res[0]:.3e}                      {res[1]:.3e}")
    print(f"   Local coupling: ~{out[0.0][0]:.0f} phonons/s, the same for both bodies (the rate does not depend on mass).")
    print(f"   At R0 = 0.54 Angstrom: {out[R0_DONADI][0]:.1e} phonons/s, far below any measured heating.")
    print("   So heating rules out local CQ gravity but cannot reach the R0 the radiation bound allows;")
    print("   for those, the deciding test is coherence at a large split (P2 and P3). Collective")
    print("   gravity (this theory, and perturbative quantum gravity): Gamma = 0, S_a = 0, no heating.")
    banner("P5  Any classical-quantum gravity, any kernel, continuous or discrete (worked example)")
    worst, sat = operator_check()
    print("   The trade-off (their eq. 29) is an operator inequality, D0 >= S_J^-1 / 4, for every CQ model")
    print("   with Newtonian back-reaction on average, including jump models whose noise sits only where")
    print("   mass is. Cauchy-Schwarz in the S_J inner product then gives, with no kernel assumed:")
    print("        Gamma(split) * S_a  >=  (1/8) |<Delta m, w>|^2  =  (1/8) (F_LR / M)^2")
    print("   F_LR is the Newtonian pull of one branch's mass on the other's. Checks: random matrices,")
    print(f"   min ratio lhs/rhs = {worst:.3f} (>= 1); saturating case = {sat:.6f}.")
    x = np.array([0.25, 0.5, 1.0, 1.5, 2.0, 5.0])
    fc = [sphere_force_closed(xx * R_A) for xx in x]
    ff = [sphere_force_fourier(xx * R_A) for xx in x]
    print("   Uniform spheres, F_LR / (G M^2/R^2):  split/R = " + ", ".join(f"{a:g}" for a in x))
    print("     closed form: " + ", ".join(f"{f_/(G*M_A**2/R_A**2):.4f}" for f_ in fc))
    print("     Fourier    : " + ", ".join(f"{f_/(G*M_A**2/R_A**2):.4f}" for f_ in ff))
    out["P5_fit"] = max(abs(a / b - 1) for a, b in zip(fc, ff))
    print("   The pull is largest at split = R (0.46875 G M^2/R^2): the best test is a SMALL split.")
    print("   Design-A diamond, Gamma <= 0.12 /s:")
    print("     split         bound (m^2/s^4)   CQ acceleration noise needed (one-sided, m s^-2/rtHz)")
    for lab, d in (("R = 1.0 um", R_A), ("2R", 2 * R_A), ("721 um", D_A)):
        B = general_bound(d)
        asd = np.sqrt(2 * B / GAMMA_BUDGET)
        out[("P5", lab)] = (B, asd)
        print(f"     {lab:10s}    {B:.3e}         {asd:.2e}   ({asd/ASD_REQ:.1e} x design A's requirement)")
    rP3 = general_bound(R_A) / joint_bound(R_A)
    out["P5_vs_P3_at_R"] = rP3
    print(f"   At 721 um the kernel-free bound is {general_bound(D_A)/rows[0][2]:.0e} of the translation-invariant one (P3);")
    print(f"   at split = R it is {rP3:.2f} of P3 at the same split. So one diamond held coherent across about its radius,")
    print("   with its acceleration noise measured, tests every Markovian CQ gravity, discrete ones included.")
    print("   Diamond density, split = R, Gamma <= 0.1 /s:")
    print("     mass (kg)    R (um)    acceleration noise CQ gravity must produce (one-sided)")
    rho_d = M_A / (4 / 3 * np.pi * R_A**3)
    for Mx in (1e-17, 1e-15, 1e-14, 1e-12):
        Rx = (3 * Mx / (4 * np.pi * rho_d)) ** (1 / 3)
        asd = np.sqrt(2 * general_bound(Rx, Rx, Mx) / 0.1)
        out[("P5m", Mx)] = asd
        print(f"     {Mx:8.0e}    {Rx*1e6:6.3f}    {asd:.2e} m s^-2/rtHz")
    print("   For small splits (dx << R) the same bound becomes a heating floor of 2 pi G rho/(3 omega)")
    print(f"   phonons/s, {2*np.pi*G*rho_d/(3*OMEGA_NANO):.1e} at 50 kHz: unmeasurable. The test needs a split of order R.")
    return rows, out


if __name__ == "__main__":
    main()
