"""
Compute the actual gravitational particle production of (effectively massless)
quarks through the self-sourced torsion bounce, instead of assuming an O(eta)
occupation ansatz. Reuses the exact same Bogoliubov/adiabatic-vacuum formalism
already validated in the dark-matter calculation (DARK_MATTER_RELIC_DENSITY.md
Part VIII.3), applied here to the actual bounce background (not an idealized
sudden transition, not an unperturbed power law with no transition in it at all).

Background: near the bounce, matter and Lambda are utterly negligible (checked:
~45-169 orders of magnitude below radiation/torsion there), so
    E^2(a) = Omega_r a^-4 - Omega_r a_b^8 a^-12   (exact, given a_b defined by E^2(a_b)=0)
Nondimensionalizing x=a/a_b, tau=H_bounce*t:
    h(x) = H/H_bounce = sqrt(x^-4 - x^-12)
    dx/dtau = h*x = sqrt(x^-2 - x^-10)
    dh/dtau = -2 x^-4 + 6 x^-12   (exact; dh/dtau|_{x=1} = 4, i.e. Hdot(0) = 4 H_bounce^2,
                                   verified two independent ways: finite-difference on the
                                   full E^2(a) AND this closed form -- both give 4.0000)
Time-reversal symmetric bounce assumed: x(-tau)=x(tau), h(-tau)=-h(tau).
"""
import numpy as np
from scipy.integrate import solve_ivp, trapezoid
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import quark_resistance_torsion_bounce as tb

H0 = 67.36
Om, Or, OL = tb.omegas(H0)
C, ETA_ANSATZ = 1 / 32, 1.0   # the best-anchored C; eta=1 ansatz used to BUILD this background
a_b = tb.find_bounce_selfsourced(H0, C, ETA_ANSATZ, Om, Or, OL)
H_bounce_GeV = tb.H_rad_GeV(a_b, H0, Or)
H_bounce_over_MPl = H_bounce_GeV / tb.M_PL_REDUCED_GEV
print(f"a_bounce = {a_b:.6e}   H_bounce = {H_bounce_over_MPl:.6f} M_Pl  (background built assuming eta={ETA_ANSATZ})")

# --- dimensionless trajectory x(tau) for tau >= 0, mirrored for tau < 0 ---
def rhs_x(tau, x):
    xv = max(x[0], 1.0)
    val = xv ** -2 - xv ** -10
    return [np.sqrt(max(val, 0.0))]

TAU_MAX = 60.0
tau0 = 1e-6
x0 = 1 + 2 * tau0 ** 2
sol_x = solve_ivp(rhs_x, (tau0, TAU_MAX), [x0], method='RK45', rtol=1e-12, atol=1e-18,
                   dense_output=True, max_step=0.02)
assert sol_x.success

def x_of_tau(tau):
    t = abs(tau)
    if t < tau0:
        return 1 + 2 * t ** 2
    return float(sol_x.sol(min(t, TAU_MAX))[0])

def h_of_tau(tau):
    x = x_of_tau(tau)
    val = max(x ** -4 - x ** -12, 0.0)
    hh = np.sqrt(val)
    return hh if tau >= 0 else -hh

def hdot_of_tau(tau):
    x = x_of_tau(tau)
    return -2 * x ** -4 + 6 * x ** -12   # even in tau (same sign both branches, matches d(h)/dtau at tau=0+ and the mirrored slope at 0-)

# sanity check: Hdot(0)/H_bounce^2 should be exactly 4
print(f"sanity check: dh/dtau(0) = {hdot_of_tau(0.0):.6f}  (expect 4.0 exactly)")

M_OVER_HBOUNCE = 0.0   # quarks are ~5 MeV, H_bounce ~1e18 GeV -> ratio ~1e-21, treat as exactly massless

def omega2(tau, kappa):
    x = x_of_tau(tau)
    return (kappa / x) ** 2 + M_OVER_HBOUNCE ** 2

def Omega2(tau, kappa):
    return omega2(tau, kappa) - 2.25 * h_of_tau(tau) ** 2 - 1.5 * hdot_of_tau(tau)

def run_mode(kappa, tau_start, tau_end):
    def deriv(tau, y):
        f = y[0] + 1j * y[1]
        fd = y[2] + 1j * y[3]
        fdd = -3 * h_of_tau(tau) * fd - omega2(tau, kappa) * f
        return [fd.real, fd.imag, fdd.real, fdd.imag]
    x0_ = x_of_tau(tau_start)
    w0 = np.sqrt(omega2(tau_start, kappa))
    f0 = 1.0 / np.sqrt(2 * x0_ ** 3 * w0)   # using x as the (rescaled) scale factor; overall a_b^3 factors cancel in n_k ratios
    fd0 = -1j * w0 * f0 - 1.5 * h_of_tau(tau_start) * f0
    y0 = [f0.real, f0.imag, fd0.real, fd0.imag]
    return solve_ivp(deriv, (tau_start, tau_end), y0, method='RK45', rtol=1e-9, atol=1e-30, dense_output=True, max_step=0.05)

def n_k_at(sol, tau, kappa):
    x = x_of_tau(tau)
    hh = h_of_tau(tau)
    Om_ = np.sqrt(max(Omega2(tau, kappa), 1e-30))
    f = sol.sol(tau)[0] + 1j * sol.sol(tau)[1]
    fd = sol.sol(tau)[2] + 1j * sol.sol(tau)[3]
    g = x ** 1.5 * f
    gd = x ** 1.5 * (1.5 * hh * f + fd)
    return (abs(gd) ** 2 / (2 * Om_) + Om_ * abs(g) ** 2 / 2) - 0.5

print("\n=== Representative mode (kappa=1, i.e. physical momentum = H_bounce AT the bounce) ===")
kappa_test = 1.0
tau_start = -30.0
sol = run_mode(kappa_test, tau_start, 40.0)
for tau in [-10, -1, 0, 1, 5, 10, 20, 30, 40]:
    nk = n_k_at(sol, tau, kappa_test)
    print(f"  tau={tau:6.1f}  x={x_of_tau(tau):10.4f}  n_k={nk.real if hasattr(nk,'real') else nk: .6e}")

print("\n=== Momentum scan (read at tau=40, well after re-adiabaticization) ===")
print("(kappa range extended down to 0.002 after confirming kappa^2*n_k -> 0 as kappa -> 0,")
print(" i.e. the integral is IR-convergent, not dominated by an unresolved low-kappa tail)")
kappas = np.geomspace(0.002, 50, 40)
nks = []
tau_read = 40.0
for kappa in kappas:
    tau_s = -max(20.0, 15.0 / max(kappa, 0.002))
    tau_s = max(tau_s, -60.0)
    try:
        solk = run_mode(kappa, tau_s, tau_read)
        nk = n_k_at(solk, tau_read, kappa)
        nkv = nk.real if hasattr(nk, 'real') else nk
        nks.append(max(nkv, 0.0))
    except Exception as e:
        nks.append(float('nan'))
        print(f"  kappa={kappa:9.4f}  FAILED: {e}")
        continue
    print(f"  kappa={kappa:9.4f}  tau_start={tau_s:7.2f}  n_k={nks[-1]: .6e}")

nks = np.array(nks)
good = np.isfinite(nks) & (nks >= 0)
integrand = kappas[good] ** 2 * nks[good]
n_comoving_dimensionless = trapezoid(integrand, kappas[good]) / (2 * np.pi ** 2)   # in units of (H_bounce)^3, comoving w.r.t. x
x_read = x_of_tau(tau_read)
n_phys_over_Hbounce3 = n_comoving_dimensionless / x_read ** 3

print(f"\nComoving number density integral (H_bounce^3, x_read^3 units): {n_comoving_dimensionless:.6e}")
print(f"x(tau_read) = {x_read:.4f}")
print(f"Physical number density at tau_read, in units of H_bounce^3: {n_phys_over_Hbounce3:.6e}")

eta_computed = n_phys_over_Hbounce3 / tb.G_Q
print(f"\neta_computed = n_phys/(g_Q * H_bounce^3) = {eta_computed:.6e}")
print(f"eta_ansatz used to build this background = {ETA_ANSATZ}")
print(f"ratio eta_computed/eta_ansatz = {eta_computed/ETA_ANSATZ:.6e}")

print("\n=== What this implies for H_bounce, self-consistently ===")
print("(the dimensionless bounce shape x(tau) -- and hence eta_computed -- is UNIVERSAL for")
print(" this self-sourced-via-unperturbed-H_rad mechanism: it does not depend on which C or")
print(" eta_ansatz was used to locate a_bounce in physical units, only on the a^-12 shape of")
print(" the torsion term. So eta_computed can be fed back into the H_bounce formula directly.)")
for C_label, C_val in [("1/32 (best-anchored)", 1 / 32), ("9/16 (alt. convention)", 9 / 16)]:
    Hb = (3 / (C_val * eta_computed ** 2 * tb.G_Q ** 2)) ** 0.25
    print(f"  C={C_label}: self-consistent H_bounce = {Hb:.2f} M_Pl")

print("\n=== Does broadening to all SM fermions (not just quarks) help? ===")
print("(eta_computed is species-independent for an exactly massless fermion -- the mode")
print(" equation never references flavor/color, only the overall dof count g -- so this is")
print(" just H_bounce ~ g^(-1/2) at fixed eta_computed, C)")
G_ALL_FERMIONS = 90   # standard 3-generation SM fermion dof (quarks 72 + charged leptons 12 + neutrinos 6)
for C_label, C_val in [("1/32", 1 / 32), ("9/16", 9 / 16)]:
    for g, glabel in [(tb.G_Q, "quarks only"), (G_ALL_FERMIONS, "all SM fermions")]:
        Hb = (3 / (C_val * eta_computed ** 2 * g ** 2)) ** 0.25
        print(f"  C={C_label:5s}  g={g:3d} ({glabel:16s})  H_bounce = {Hb:7.2f} M_Pl")
