"""
Extends lcdm_backward.py with an Einstein-Cartan (ECKS) spin-torsion repulsion
term, sourced by quark number density, to replace the a->0 singularity with a
bounce -- operationalizing "resistance to tunneling" as a real, citable
gravitational effect instead of an invented one.

MECHANISM (real, citable, not invented here):
  Einstein-Cartan-Kibble-Sciama gravity: torsion is non-dynamical (algebraic,
  no kinetic term), sourced locally by fermion spin density. Substituting the
  algebraic torsion solution back into the Einstein equation produces an
  EFFECTIVE extra term in the stress-energy tensor that is quadratic in the
  fermion number density n and REPULSIVE (negative effective energy density,
  positive effective pressure): rho_eff = rho - alpha*n^2, p_eff = p + alpha*n^2.
  This is the real mechanism behind Poplawski's nonsingular big-bounce
  cosmology (Phys. Rev. D 85, 107502 (2012), arXiv:1111.4595; see also Hehl,
  von der Heyde, Kerlick & Nester, Rev. Mod. Phys. 48, 393 (1976) for the
  original ECKS formalism).

HONESTY NOTE ON THE COEFFICIENT (read before trusting any bounce number
below): arxiv.org and all mirror/review hosts (ar5iv, export.arxiv.org,
inspirehep, semanticscholar) are blocked by this session's egress proxy, so
the exact PRIMARY-SOURCE numerical prefactor could not be verified directly
in this session. Secondary-source search snippets gave two DIFFERENT
prefactors in different unit conventions (alpha=(9/16)*kappa in one, alpha =
kappa*(hbar*c)^2/32 in another) that could not be reconciled without reading
the primary derivation. What IS certain by dimensional analysis alone (no
literature needed): alpha must have units of 1/mass^2, and gravity's only
natural mass scale is the Planck mass, so alpha = C / M_Pl_reduced^2 for
some dimensionless C that the literature puts at O(0.1-1) in the cases found.
C is therefore treated here as an EXPLICIT, SCANNED free parameter -- exactly
the same honest treatment given to the Chung-Kolb-Riotto O(1) coefficient in
DARK_MATTER_RELIC_DENSITY.md Part VIII -- not a fabricated precise number.

WHAT n IS, AND WHY IT'S SPECIALIZED TO QUARKS (a choice, flagged as such):
Poplawski's mechanism is generic to any fermion species; it is specialized
here to QUARKS specifically (not the full relativistic fermion bath) because
that is the user's specific claim under test ("a quark was created in every
possible space available ... resistance to tunneling"). This is a deliberate
narrowing, not a literature result -- if the real mechanism is sourced by ALL
relativistic fermions (leptons included), the effective g would be larger and
the bounce would occur at lower density. Using only quarks is the
conservative (minimal) version of the claim.

TIME AS THE FREE DIAL: there is no assumed absolute pre-bounce clock. Cosmic
time is defined to be t=0 AT the bounce; everything else (age today, equality
epochs) is measured as elapsed time since the bounce, recovering exactly the
H0-dial baseline from lcdm_backward.py at late times as a coherence check.
"""
import numpy as np
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq

# ---------------------------------------------------------------------------
# Fixed physical constants (standard, not fit)
# ---------------------------------------------------------------------------
ZETA3 = 1.2020569031595943
M_PL_REDUCED_GEV = 2.435e18          # reduced Planck mass
T0_KELVIN = 2.7255
K_BOLTZMANN_GEV_PER_K = 8.617333262e-14   # GeV/K  (8.617333262e-5 eV/K)
T0_GEV = T0_KELVIN * K_BOLTZMANN_GEV_PER_K

G_S0 = 3.909            # standard today's entropy dof (photons + decoupled neutrinos)
G_STAR_EARLY = 106.75   # standard full-SM relativistic dof, valid for T >> EW scale
G_Q = 2 * 3 * 2 * 2     # u,d flavors (2) x color (3) x {quark,antiquark} (2) x spin (2) = 24

KM_S_MPC_TO_GEV = None  # filled below numerically, not from a memorized constant

# Derive the km/s/Mpc -> GeV conversion from first principles (no recalled constant):
MPC_IN_KM = 3.0856775814913673e19   # 1 Mpc in km (IAU-standard definition, exact given AU & parsec defs)
HBAR_GEV_S = 6.582119569e-25        # GeV*s (CODATA, exact-ish)


def H0_to_GeV(H0_kmsMpc):
    H0_per_s = H0_kmsMpc / MPC_IN_KM          # s^-1
    return H0_per_s * HBAR_GEV_S              # GeV


# ---------------------------------------------------------------------------
# Baseline (from lcdm_backward.py) -- physical density parameters, H0 as dial
# ---------------------------------------------------------------------------
OMEGA_B_H2 = 0.02237
OMEGA_C_H2 = 0.1200
OMEGA_M_H2 = OMEGA_B_H2 + OMEGA_C_H2
OMEGA_R_H2 = 4.16e-5


def omegas(H0_kmsMpc):
    h = H0_kmsMpc / 100.0
    Om = OMEGA_M_H2 / h**2
    Or = OMEGA_R_H2 / h**2
    OL = 1.0 - Om - Or
    return Om, Or, OL


def T_of_a(a):
    """Valid for a << a_EW (deep early universe, full SM dof)."""
    return T0_GEV / a * (G_S0 / G_STAR_EARLY) ** (1.0 / 3.0)


def n_q_of_a(a):
    """Total quark+antiquark number density (thermal, relativistic), GeV^3."""
    T = T_of_a(a)
    return (3 * ZETA3 / (4 * np.pi**2)) * G_Q * T**3


def rho_crit0_GeV4(H0_kmsMpc):
    H0_GeV = H0_to_GeV(H0_kmsMpc)
    return 3 * H0_GeV**2 * M_PL_REDUCED_GEV**2


def Omega_torsion(a, H0_kmsMpc, C):
    alpha = C / M_PL_REDUCED_GEV**2
    nq = n_q_of_a(a)
    return alpha * nq**2 / rho_crit0_GeV4(H0_kmsMpc)


def E2(a, H0_kmsMpc, C, Om, Or, OL):
    return Or * a**-4 + Om * a**-3 + OL - Omega_torsion(a, H0_kmsMpc, C)


def find_bounce(H0_kmsMpc, C, Om, Or, OL):
    """E^2(a) = 0 : since torsion ~ a^-6 beats radiation's a^-4 as a->0, a
    bounce exists for ANY C>0 (checked below: this is not fine-tuned, only ITS
    LOCATION depends on C). Root-find in x=ln(a) -- E2 spans ~10^170 in
    magnitude across the bracket, which defeats brentq in linear a. First
    coarse-scan a log-spaced grid to localize the sign change, then refine.
    """
    g = lambda x: E2(np.exp(x), H0_kmsMpc, C, Om, Or, OL)
    xs = np.linspace(0.0, -200.0, 4001)   # ln(a) from 0 (a=1) down to a~1e-87
    vals = [g(x) for x in xs]
    sign_change = None
    for i in range(len(xs) - 1):
        if np.sign(vals[i]) != np.sign(vals[i + 1]):
            sign_change = (xs[i + 1], xs[i])  # (more negative x, less negative x)
            break
    if sign_change is None:
        return None
    x_b = brentq(g, sign_change[0], sign_change[1], xtol=1e-12, rtol=1e-14)
    return np.exp(x_b)


def report_bounce(H0_kmsMpc, C, label=""):
    Om, Or, OL = omegas(H0_kmsMpc)
    a_b = find_bounce(H0_kmsMpc, C, Om, Or, OL)
    if a_b is None:
        print(f"  C={C:<8g}  NO BOUNCE FOUND in bracket (unexpected)")
        return None
    T_b = T_of_a(a_b)
    nq_b = n_q_of_a(a_b)
    rho_b_GeV4 = Or * a_b**-4 * rho_crit0_GeV4(H0_kmsMpc)  # dominant term at bounce
    rho_planck_GeV4 = M_PL_REDUCED_GEV**4
    # sub-horizon consistency: is bounce within the regime where T_of_a (fixed g*) is valid?
    print(f"  C={C:<8g}  a_bounce={a_b:.6e}   T_bounce={T_b:.4e} GeV = {T_b/M_PL_REDUCED_GEV:.4e} M_Pl"
          f"   rho_bounce/rho_Planck={rho_b_GeV4/rho_planck_GeV4:.4e}   n_q_bounce={nq_b:.4e} GeV^3")
    return dict(H0=H0_kmsMpc, C=C, a_b=a_b, T_b=T_b, nq_b=nq_b, rho_ratio=rho_b_GeV4 / rho_planck_GeV4)


def report_bounce_for_g(H0_kmsMpc, C, g_ratio, Om, Or, OL):
    """Same thermal-sourcing bounce as report_bounce, but with the quark dof
    g_Q rescaled by g_ratio -- used to test whether adding a sub-quark
    (preon) layer can rescue the trans-Planckian result. n_q ~ g, so this is
    equivalent to rescaling C by g_ratio^2."""
    a_b = find_bounce(H0_kmsMpc, C * g_ratio**2, Om, Or, OL)
    T_b = T_of_a(a_b)
    return a_b, T_b


# ---------------------------------------------------------------------------
# Self-sourced production: the tunneling event supplies its own density.
#
# The thermal picture above assumes a PRE-EXISTING equilibrium quark bath
# threaded in "from before" the bounce -- a strange assumption if the bounce
# is supposed to be the beginning. The alternative: the quark density is
# itself produced, non-adiabatically, by the transition's own rapid change
# in spacetime geometry -- exactly the gravitational-particle-production
# mechanism already validated in this project's dark-matter Bogoliubov
# calculation (DARK_MATTER_RELIC_DENSITY.md Part VIII.3), applied here to
# quarks instead of the dark R-field.
#
# Standard leading-order (test-field, fixed-background) treatment of
# gravitational particle production (Chung, Kolb & Riotto, Phys. Rev. D 59,
# 023501 (1998)): modes up to k~H are populated at O(eta) occupancy, giving
# a produced number density n ~ eta * g * H^3. Following that literature's
# own leading-order approach, H here is evaluated on the UNPERTURBED
# (pre-torsion) radiation-domination trajectory -- the production is
# computed as a test field on the background the universe WOULD have had,
# then checked for where it becomes large enough to backreact.
# ---------------------------------------------------------------------------

def H_rad_GeV(a, H0_kmsMpc, Or):
    """Unperturbed (pre-torsion) radiation-domination Hubble rate at a, GeV."""
    return H0_to_GeV(H0_kmsMpc) * np.sqrt(Or) * a ** -2


def n_q_selfsourced(a, H0_kmsMpc, Or, eta):
    return eta * G_Q * H_rad_GeV(a, H0_kmsMpc, Or) ** 3


def Omega_torsion_selfsourced(a, H0_kmsMpc, C, Or, eta):
    alpha = C / M_PL_REDUCED_GEV ** 2
    nq = n_q_selfsourced(a, H0_kmsMpc, Or, eta)
    return alpha * nq ** 2 / rho_crit0_GeV4(H0_kmsMpc)


def E2_selfsourced(a, H0_kmsMpc, C, eta, Om, Or, OL):
    return Or * a ** -4 + Om * a ** -3 + OL - Omega_torsion_selfsourced(a, H0_kmsMpc, C, Or, eta)


def find_bounce_selfsourced(H0_kmsMpc, C, eta, Om, Or, OL):
    g = lambda x: E2_selfsourced(np.exp(x), H0_kmsMpc, C, eta, Om, Or, OL)
    xs = np.linspace(0.0, -200.0, 4001)
    vals = [g(x) for x in xs]
    sign_change = None
    for i in range(len(xs) - 1):
        if np.sign(vals[i]) != np.sign(vals[i + 1]):
            sign_change = (xs[i + 1], xs[i])
            break
    if sign_change is None:
        return None
    x_b = brentq(g, sign_change[0], sign_change[1], xtol=1e-12, rtol=1e-14)
    return np.exp(x_b)


def report_bounce_selfsourced(H0_kmsMpc, C, eta, Om, Or, OL):
    a_b = find_bounce_selfsourced(H0_kmsMpc, C, eta, Om, Or, OL)
    if a_b is None:
        print(f"  C={C:<8g} eta={eta:<6g}  NO BOUNCE FOUND")
        return None
    Hb = H_rad_GeV(a_b, H0_kmsMpc, Or)
    print(f"  C={C:<8g} eta={eta:<6g}  a_bounce={a_b:.4e}   H_bounce/M_Pl={Hb/M_PL_REDUCED_GEV:.6f}")
    return dict(C=C, eta=eta, a_b=a_b, H_bounce_over_MPl=Hb / M_PL_REDUCED_GEV)


if __name__ == "__main__":
    print("=== Unit-conversion self-check ===")
    print(f"  H0=100 km/s/Mpc -> {H0_to_GeV(100.0):.6e} GeV  "
          f"(cross-check: 1/H0 should be ~9.78 Gyr; GeV^-1 = 6.582e-25 s)")
    H0_100_GeV = H0_to_GeV(100.0)
    hubble_time_Gyr = (HBAR_GEV_S / H0_100_GeV) / (3.15576e16)  # s/Gyr = 3.15576e16
    print(f"  -> implied Hubble time for H0=100: {hubble_time_Gyr:.4f} Gyr (expect ~9.78 Gyr)")
    print(f"  T0 = {T0_GEV:.6e} GeV (expect ~2.35e-13 GeV for T=2.7255 K)")

    print("\n=== Bounce location vs the honestly-unknown coupling C (H0=67.36) ===")
    for C in [1e-3, 1e-2, 0.1, (9/16), 1.0, 10.0]:
        report_bounce(67.36, C, label=f"C={C}")

    print("\n=== Check: does the torsion term disturb standard BBN? (T~1 MeV, C=1) ===")
    H0 = 67.36
    Om, Or, OL = omegas(H0)
    a_bbn = T0_GEV * (G_S0 / G_STAR_EARLY) ** (1 / 3) / 1e-3  # a such that T_of_a(a) = 1 MeV
    Otor_bbn = Omega_torsion(a_bbn, H0, 1.0)
    Or_bbn = Or * a_bbn**-4
    print(f"  a(T=1 MeV) = {a_bbn:.4e}")
    print(f"  Omega_r(a_bbn) term = {Or_bbn:.4e}")
    print(f"  Omega_torsion(a_bbn, C=1) = {Otor_bbn:.4e}  (ratio to radiation: {Otor_bbn/Or_bbn:.4e})")

    print("\n=== Does a sub-quark (preon) layer rescue the trans-Planckian result? ===")
    print("  T_bounce scales as 1/g at fixed C -- test realistic dof multipliers:")
    for g_ratio, label in [
        (1.0, "quarks only (g=24), baseline"),
        (106.75 / G_Q, "full Standard Model (all relativistic species, g*=106.75)"),
        (3.0, "rishon-style preons: 3 preons/quark, quark-like dof each"),
        (10.0, "generic 10x toy preon sector"),
        (43.5, "dof needed to reach T_bounce ~ 0.1 M_Pl at C=9/16"),
    ]:
        a_b, T_b = report_bounce_for_g(H0, 9 / 16, g_ratio, Om, Or, OL)
        print(f"  g/g_quarks={g_ratio:7.2f}  T_bounce={T_b/M_PL_REDUCED_GEV:.4f} M_Pl   [{label}]")

    print("\n=== Self-sourced production: the tunneling event supplies its own density ===")
    print("  n_q(a) = eta * g_Q * H_rad(a)^3  (gravitational production, not a pre-existing bath)")
    print(f"  {'C':>8} {'eta':>6}   a_bounce      H_bounce/M_Pl")
    for C in [0.01, 0.1, 9 / 16, 1.0, 10.0]:
        for eta in [0.01, 0.1, 1.0]:
            report_bounce_selfsourced(H0, C, eta, Om, Or, OL)

    print("\n=== Self-sourced coherence checks (C=9/16, eta=0.1) ===")
    C, eta = 9 / 16, 0.1
    a_b = find_bounce_selfsourced(H0, C, eta, Om, Or, OL)

    def age_selfsourced(a_lo, a_hi, C, eta):
        H0_Gyr = H0 / 977.792
        def integrand(x):
            a = np.exp(x)
            E2v = E2_selfsourced(a, H0, C, eta, Om, Or, OL)
            if E2v <= 1e-300:
                return 0.0
            return 1.0 / (H0_Gyr * np.sqrt(E2v))
        val, err = quad(integrand, np.log(a_lo), np.log(a_hi), limit=500)
        return val

    t_bounce_today = age_selfsourced(a_b * 1.0000001, 1.0, C, eta)
    print(f"  age(bounce -> today) = {t_bounce_today:.6f} Gyr  (pure LambdaCDM baseline = 13.814064 Gyr)")

    a_bbn = T0_GEV * (G_S0 / G_STAR_EARLY) ** (1 / 3) / 1e-3
    Ot_bbn_ss = Omega_torsion_selfsourced(a_bbn, H0, C, Or, eta)
    Or_bbn = Or * a_bbn ** -4
    print(f"  Omega_torsion_selfsourced/Omega_r at BBN (T=1 MeV) = {Ot_bbn_ss/Or_bbn:.4e}")
