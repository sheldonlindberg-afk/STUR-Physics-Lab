#!/usr/bin/env python3
"""
Measurement, the double slit, and entanglement: three proposed mechanisms, tested.

Proposal (user, this session):
  M1. Measuring is what creates the particle we see.
  M2. Before it is seen, an electron is not a probability cloud but a real EM "cloud",
      and that cloud is produced by the strong force.
  M3. Entanglement is not a separate phenomenon: it is one particle stretched across
      spacetime. Act on one side and the other side reacts instantly.

Each is labelled, computed, and confronted with the strongest data available here.
Labels: KNOWN (textbook physics), FOLLOWS (derived here from KNOWN), LIT (literature
value used as input, not recomputed), PROPOSAL (the mechanism under test).

Atomic units (hbar = m_e = e = 4 pi eps0 = 1) are used in T1.
"""
import numpy as np
from scipy.linalg import eigh_tridiagonal

HARTREE_EV = 27.211386245988
RYDBERG_EV = HARTREE_EV / 2
HBARC_MEV_FM = 197.3269804
M_PI_MEV = 139.57039          # charged pion
M_E_MEV = 0.51099895
A0_FM = 52917.721090          # Bohr radius
H_IONIZATION_EV = 13.598434   # LIT: measured hydrogen ionization energy
PS_1S2S_MHZ = 1233607216.4    # LIT: Fee et al., PRL 70, 1397 (1993)
H_PLANCK_EV_S = 4.135667696e-15


def banner(s):
    print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)


# ---------------------------------------------------------------------------------------
# T1. M2 as stated: the electron is a real charge cloud of density e|psi|^2.
#     A real cloud repels itself (classical self-energy J = 1/2 int rho phi).
#     Solve hydrogen self-consistently WITH that self-repulsion and compare to data.
# ---------------------------------------------------------------------------------------
def hydrogen_scf(self_interaction=True, rmax=60.0, n=6000, iters=400, mix=0.3):
    """Radial 1s state of -1/2 u'' + (-1/r + lam*V_H[u]) u = eps u. Returns dict."""
    h = rmax / (n + 1)
    r = h * np.arange(1, n + 1)
    lam = 1.0 if self_interaction else 0.0
    VH = np.zeros(n)
    for _ in range(iters):
        d = 1.0 / h**2 - 1.0 / r + lam * VH
        e = -0.5 / h**2 * np.ones(n - 1)
        w, v = eigh_tridiagonal(d, e, select="i", select_range=(0, 0))
        u = v[:, 0] / np.sqrt(h)                     # int u^2 dr = 1
        q = np.cumsum(u**2) * h                      # charge inside r
        outer = (np.cumsum((u**2 / r)[::-1]) * h)[::-1]
        VH_new = q / r + outer - (u**2 / r) * h      # trapezoid-ish correction at r
        if lam == 0.0:
            break
        if np.max(np.abs(VH_new - VH)) < 1e-11:
            VH = VH_new
            break
        VH = (1 - mix) * VH + mix * VH_new
    eps = w[0]
    J = 0.5 * np.sum(u**2 * VH) * h * lam
    E = eps - J                                      # E = T + V_nuc + J
    rmean = np.sum(u**2 * r) * h
    return {"eps": eps, "J": J, "E": E, "rmean": rmean}


def t1_charge_cloud():
    banner("T1  M2 as a REAL charge cloud (Schrodinger's 1926 charge-density reading)")
    std = hydrogen_scf(self_interaction=False)
    cloud = hydrogen_scf(self_interaction=True)
    # closed form, exponential trial exp(-z r): E = z^2/2 - z + 5z/16 -> z = 11/16
    E_var = -121.0 / 512.0
    J_std = 5.0 / 16.0
    print("   KNOWN: a classical charge distribution has self-energy J = 1/2 int rho phi.")
    print(f"   Standard 1s (no self-repulsion): E = {std['E']*HARTREE_EV:9.4f} eV,"
          f" <r> = {std['rmean']:.4f} a0")
    print(f"   Self-energy of that 1s cloud:     J = 5/16 Ha = {J_std*HARTREE_EV:.4f} eV"
          "  (62% of the binding energy)")
    print(f"   FOLLOWS, self-consistent real cloud: E = {cloud['E']*HARTREE_EV:9.4f} eV,"
          f" <r> = {cloud['rmean']:.4f} a0")
    print(f"   (variational check, exponential trial: E = -121/512 Ha = {E_var*HARTREE_EV:.4f} eV)")
    print(f"   LIT measured ionization energy: {H_IONIZATION_EV:.6f} eV")
    print(f"   -> a real self-repelling cloud binds by {-cloud['E']*HARTREE_EV:.2f} eV, a factor"
          f" {H_IONIZATION_EV/(-cloud['E']*HARTREE_EV):.1f} too weak,")
    print(f"      and is {cloud['rmean']/std['rmean']:.1f}x too large. Every line of the"
          " hydrogen spectrum would move.")
    print("   -> Whatever surrounds the proton does NOT repel itself. It is not a real charge")
    print("      cloud; it is an amplitude for where the ONE whole charge e will be found.")
    print("   KNOWN corollary: in a double slit every detection registers a whole e, never e/2.")
    return std, cloud


# ---------------------------------------------------------------------------------------
# T2. M2's second half: the cloud is produced by the strong force.
# ---------------------------------------------------------------------------------------
def yukawa_exponent():
    rng = HBARC_MEV_FM / M_PI_MEV
    return rng, A0_FM / rng


def positronium_1s2s_mhz():
    # Bohr levels with reduced mass m_e/2: E_n = -Ry/2 / n^2  -> 1S-2S = (3/4)(Ry/2)
    dE = 0.75 * RYDBERG_EV / 2.0
    return dE / H_PLANCK_EV_S / 1e6


def t2_strong_force():
    banner("T2  M2: is the electron's cloud made by the strong force?")
    rng, x = yukawa_exponent()
    print("   KNOWN: electrons are leptons; they carry no colour charge, so gluons do not")
    print("   couple to them at tree level. Test the claim anyway, by range and by a clean atom.")
    print(f"   Strong-force range hbar/(m_pi c) = {rng:.4f} fm;  Bohr radius = {A0_FM:.1f} fm")
    print(f"   Yukawa suppression at the cloud's size: exp(-{x:.0f}) = 10^-{x/np.log(10):.0f}")
    f = positronium_1s2s_mhz()
    print("   Positronium (e+ e-) has an electron cloud and NO quarks or gluons anywhere.")
    print(f"   Bohr formula with reduced mass m_e/2, pure EM: 1S-2S = {f:,.1f} MHz")
    print(f"   LIT measured:                                  1S-2S = {PS_1S2S_MHZ:,.1f} MHz")
    print(f"   Relative difference {abs(f-PS_1S2S_MHZ)/PS_1S2S_MHZ:.1e}, which is the size of"
          " the known QED (alpha^2) corrections;")
    print("   with those included the agreement is at the 10^-9 level (LIT).")
    print("   -> The cloud exists, at the right size and energy, where there is no strong")
    print("      force at all. M2's strong-force origin is excluded.")
    return rng, x, f


# ---------------------------------------------------------------------------------------
# T3. M1: does measurement create the particle? The double slit with a which-path record.
# ---------------------------------------------------------------------------------------
def double_slit(theta, model="quantum", ny=4001):
    """Far-field pattern, slits at +-d/2, Gaussian envelope.

    quantum: detector starts in |0>, path 2 rotates it by theta, so <E1|E2> = cos(theta).
    cloud:   a real cloud with no phase: intensities add, no cross term.
    Returns (y, P, V_fringe, D) with D the which-path distinguishability."""
    y = np.linspace(-6, 6, ny)            # in units of the fringe period / (2 pi)
    env = np.exp(-y**2 / 18)
    psi1 = env * np.exp(+1j * y / 2)
    psi2 = env * np.exp(-1j * y / 2)
    overlap = np.cos(theta) if model == "quantum" else 0.0
    P = np.abs(psi1)**2 + np.abs(psi2)**2 + 2 * np.real(psi1 * np.conj(psi2) * overlap)
    core = np.abs(y) < np.pi + 1e-9           # one full fringe around centre
    Pn = P[core] / (2 * env[core]**2)
    V = (Pn.max() - Pn.min()) / (Pn.max() + Pn.min())
    D = abs(np.sin(theta)) if model == "quantum" else 1.0
    return y, P, V, D


def electron_wavelength_pm(kev):
    T = kev * 1e-3                         # MeV
    pc = np.sqrt(T * (T + 2 * M_E_MEV))    # MeV
    return 2 * np.pi * HBARC_MEV_FM / pc * 1e-3  # fm -> pm


def t3_double_slit():
    banner("T3  M1: the double slit with a which-path record (the measurement equation)")
    print("   KNOWN (Wootters-Zurek 1979, Englert 1996): with detector states |E1>, |E2>,")
    print("     P(y) = |psi1|^2 + |psi2|^2 + 2 Re[psi1 psi2* <E2|E1>],   V = |<E1|E2>|,")
    print("     D^2 + V^2 <= 1, with equality for pure detector states.")
    print("   theta/pi   D (which-path)   V (simulated)   D^2+V^2")
    rows = []
    for th in np.linspace(0, np.pi / 2, 6):
        _, _, V, D = double_slit(th)
        rows.append((th, D, V))
        print(f"   {th/np.pi:7.2f}   {D:12.4f}   {V:13.4f}   {D*D+V*V:9.6f}")
    _, _, Vc, _ = double_slit(0.0, model="cloud")
    print(f"   Real phaseless cloud, NO detector at all: V = {Vc:.4f}")
    lam = electron_wavelength_pm(50.0)
    print(f"   LIT: single electrons, one at a time, build up fringes (Tonomura 1989; Bach")
    print(f"   2013). At 50 keV the fringe spacing follows lambda = h/p = {lam:.3f} pm, which")
    print("   uses the electron's mass: what passes the slits already has m_e and e.")
    print("   -> A phaseless cloud gives V = 0 and is excluded. What M1 gets right: a definite")
    print("      PATH does not exist until a record of it exists. The fringes fade continuously")
    print("      with the overlap <E1|E2>, not with a person looking. Measurement creates the")
    print("      definite outcome (the dot), not the electron (its mass, charge and spin).")
    return rows, Vc


# ---------------------------------------------------------------------------------------
# T4. M3: entanglement as one stretched object with an instant reaction.
# ---------------------------------------------------------------------------------------
CHSH_ANGLES = (0.0, np.pi / 2, np.pi / 4, 3 * np.pi / 4)


def chsh(E):
    a, a2, b, b2 = CHSH_ANGLES
    return abs(E(a, b) - E(a, b2) + E(a2, b) + E(a2, b2))


def stretched_instant(a, b, n=400_000, rng=None):
    """PROPOSAL M3, made concrete: one object spans both sides. Alice's side is measured
    first and gets +-1 at random; the other end reacts instantly, becoming the opposite
    spin along a. Bob then measures along b with the ordinary single-spin rule."""
    rng = rng or np.random.default_rng(1)
    A = rng.choice([-1, 1], n)
    p_up = 0.5 * (1 - A * np.cos(a - b))       # Bob's end points along -A*a
    B = np.where(rng.random(n) < p_up, 1, -1)
    return A, B


def stretched_local(a, b, n=400_000, rng=None):
    """Same stretched object, but with no instant reaction: each end carries a shared
    direction lam fixed at creation, and answers sign(cos(setting - lam))."""
    rng = rng or np.random.default_rng(2)
    lam = rng.uniform(0, 2 * np.pi, n)
    A = np.sign(np.cos(a - lam))
    B = -np.sign(np.cos(b - lam))
    return A, B


def swap_chsh():
    """Entanglement swapping: pairs (1,2) and (3,4) are singlets; 1 and 4 never meet.
    Project (2,3) onto the singlet; return CHSH of (1,4) and the probability."""
    s = np.array([0, 1, -1, 0]) / np.sqrt(2)
    psi = np.kron(s, s).reshape(2, 2, 2, 2)                  # indices 1,2,3,4
    proj = np.einsum("bc,abcd->ad", s.reshape(2, 2), psi)    # <singlet_23|
    p = np.sum(np.abs(proj)**2)
    rho14 = np.outer(proj.ravel(), proj.ravel().conj()) / p
    Z = np.diag([1.0, -1.0]); X = np.array([[0, 1], [1, 0]], float)

    def op(t):
        return np.cos(t) * Z + np.sin(t) * X

    def E(a, b):
        return np.real(np.trace(rho14 @ np.kron(op(a), op(b))))
    return chsh(E), p


def t4_entanglement():
    banner("T4  M3: entanglement as one particle stretched across space, reacting instantly")
    cache = {}

    def corr(model):
        def E(a, b):
            A, B = model(a, b)
            cache[(model.__name__, a, b)] = (A, B)
            return np.mean(A * B)
        return E

    S_qm = chsh(lambda a, b: -np.cos(a - b))
    S_inst = chsh(corr(stretched_instant))
    S_loc = chsh(corr(stretched_local))
    print(f"   KNOWN quantum prediction (singlet):          S = {S_qm:.4f}  (2 sqrt2 = {2*np.sqrt(2):.4f})")
    print(f"   Stretched object, instant reaction (MC):     S = {S_inst:.4f}")
    print(f"   Stretched object, no instant reaction (MC):  S = {S_loc:.4f}  (Bell bound 2)")
    # no-signalling: Bob's marginal does not depend on Alice's setting
    a, a2, b, _ = CHSH_ANGLES
    mB1 = np.mean(cache[("stretched_instant", a, b)][1] == 1)
    mB2 = np.mean(cache[("stretched_instant", a2, b)][1] == 1)
    print(f"   Bob's P(+1) with Alice at a: {mB1:.4f};  at a': {mB2:.4f}  -> no message can be sent")
    Sw, p = swap_chsh()
    print(f"   Entanglement swapping: particles 1 and 4 never interact; after a Bell")
    print(f"   measurement on 2,3 (prob {p:.2f}), (1,4) give S = {Sw:.4f}")
    print("   LIT: loophole-free Bell tests (Hensen 2015; Giustina 2015; Shalm 2015) see S > 2;")
    print("   the reaction, if there is one, is faster than 10^4 c (Salart 2008), and any finite")
    print("   speed would allow signalling (Bancal 2012), so it must be truly instant.")
    print("   -> M3 SURVIVES, but only in its instant form, and it is not new: an instant")
    print("      reaction across a single extended object reproduces the quantum prediction")
    print("      exactly (it is collapse / Bohm-type nonlocality). It is not an alternative to")
    print("      entanglement; it is a picture of it. It makes no different prediction, and")
    print("      swapping shows the 'one object' can be assembled after the fact, by a")
    print("      measurement, from pieces that never met.")
    return S_qm, S_inst, S_loc, (mB1, mB2), Sw


def main():
    t1_charge_cloud()
    t2_strong_force()
    t3_double_slit()
    t4_entanglement()
    banner("VERDICT")
    print("   M1  partly right, reworded: measurement creates the definite outcome, not the")
    print("       particle. Equation: V = |<E1|E2>| (KNOWN). Fringes need no observer, only")
    print("       the absence of a record.")
    print("   M2  excluded twice: a real cloud repels itself (hydrogen binding off by x2), and the")
    print("       cloud exists in positronium where there is no strong force.")
    print("   M3  consistent with data only as instant nonlocality, which is already standard")
    print("       quantum mechanics in another picture. Its quantum-gravity version is the")
    print("       ER = EPR conjecture (Maldacena-Susskind 2013), also untested.")
    print("   The quantum-gravity test that touches all three: gravity-induced entanglement")
    print("   (Bose et al.; Marletto-Vedral 2017). If gravity can entangle two masses, the")
    print("   'stretched object' must be stretched by gravity itself.")


if __name__ == "__main__":
    main()
