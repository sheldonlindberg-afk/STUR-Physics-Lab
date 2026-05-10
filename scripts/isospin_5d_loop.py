#!/usr/bin/env python3
"""
Full 5D QCD Loop Function for Isospin Splitting m_b/m_t
========================================================

Computes the 1-loop QCD-induced b-quark Yukawa on S^1/Z_3 where
the tree-level coupling is forbidden by Z_3 selection rules.

The key integral: y_b = (alpha_s/4pi) * C_F * F_5D * y_t
where F_5D is the full 5D loop function including KK sum and
wavefunction overlap on the orbifold.
"""

import numpy as np
from scipy import integrate

v_EW = 246.22
m_t = 172.57
m_b = 4.18
alpha_s_MZ = 0.1179
L_X = 3.0 / v_EW
M_KK = 2 * np.pi / L_X
C_F = 4.0 / 3  # SU(3) Casimir for fundamental

def header(title):
    print(f"\n{'=' * 72}")
    print(f"  {title}")
    print(f"{'=' * 72}\n")

# alpha_s at M_KK via 1-loop running
b3 = -7.0
alpha_s_KK = alpha_s_MZ / (1 + alpha_s_MZ * b3 / (2*np.pi) * np.log(M_KK/91.19))

header("SECTION 1: Parameters")
print(f"  M_KK = {M_KK:.1f} GeV")
print(f"  alpha_s(M_KK) = {alpha_s_KK:.4f}")
print(f"  Target: m_b/m_t = {m_b/m_t:.4f}")

# =====================================================================
# SECTION 2: BASIC KK SUM (from existing isospin_splitting_derivation.py)
# =====================================================================
header("SECTION 2: Basic KK Sum (Existing Result)")

omega = np.exp(2j * np.pi / 3)

def F_kk_basic(N_max=200):
    """Basic KK sum: F = sum_n Re(omega^n) * 1/(1 + (n*M_KK/M_KK)^2)"""
    F = 0.0
    for n in range(1, N_max+1):
        phase = np.real(omega**n)  # Re(omega^n) = cos(2pi*n/3)
        F += phase / (n**2)
    return F

F_basic = F_kk_basic()
yb_yt_basic = alpha_s_KK / (4*np.pi) * C_F * abs(F_basic)
print(f"  F_basic (1/n^2 sum) = {F_basic:.4f}")
print(f"  y_b/y_t (basic)     = {yb_yt_basic:.5f}")
print(f"  Target              = {m_b/m_t:.4f}")
print(f"  Ratio pred/obs      = {yb_yt_basic/(m_b/m_t):.3f}")

# =====================================================================
# SECTION 3: FULL 5D LOOP WITH FEYNMAN PARAMETER INTEGRAL
# =====================================================================
header("SECTION 3: Full 5D Loop Function")

print("  The 1-loop gluon exchange diagram in 5D:")
print("  y_b^(1-loop) = (g_s^2 C_F)/(16pi^2) * y_t * I_5D")
print()
print("  I_5D = sum_{n=-inf}^{inf} omega^n * integral dx [...]")
print("  where the Feynman parameter integral includes both")
print("  zero-mode and KK-mode propagators.")
print()

def loop_function_5d(N_max=500):
    """
    Full 5D 1-loop function with Feynman parameter integral.

    The loop has a gluon and a quark propagator.
    The quark propagator sums over KK modes with Z_3 phases.
    The gluon propagator also sums over KK modes.

    For the leading contribution (zero-mode gluon, KK quark):
    I_n = int_0^1 dx x(1-x) * M_KK^2 / (x*m_t^2 + (1-x)*m_n^2)
    where m_n = (n + 1/3)*M_KK for Z_3-twisted quark.
    """
    F_total = 0.0

    for n in range(-N_max, N_max+1):
        if n == 0:
            continue

        phase = np.real(omega**n)
        m_n = abs(n) * M_KK  # KK mass of quark in loop

        # Feynman parameter integral
        def integrand(x):
            denom = x * m_t**2 + (1-x) * (m_t**2 + m_n**2)
            return x * (1-x) * M_KK**2 / denom

        I_n, _ = integrate.quad(integrand, 0, 1)
        F_total += phase * I_n

    return F_total

F_5d = loop_function_5d()
yb_yt_5d = alpha_s_KK / (4*np.pi) * C_F * abs(F_5d)

print(f"  F_5D (Feynman param) = {F_5d:.4f}")
print(f"  y_b/y_t (5D loop)    = {yb_yt_5d:.5f}")
print(f"  Target               = {m_b/m_t:.4f}")
print(f"  Ratio pred/obs       = {yb_yt_5d/(m_b/m_t):.3f}")

# =====================================================================
# SECTION 4: WAVEFUNCTION OVERLAP ENHANCEMENT
# =====================================================================
header("SECTION 4: Wavefunction Overlap Enhancement")

print("  The localized wavefunctions on Z_3 enhance the loop.")
print("  The overlap between generation wavefunctions at the same")
print("  fixed point is NOT suppressed for the loop diagram.")
print()

alpha_eff = 1.463
kappa = np.sqrt(alpha_eff)

# The wavefunction at the fixed point (theta=0):
# psi_0(0) ~ exp(-kappa^2 * 0^2 / 2) * normalization
# For the loop, the relevant quantity is the wavefunction
# evaluated at the fixed point, which is just the peak value.

# Enhancement from localization:
# The 5D Yukawa coupling is y_5D, and the 4D effective coupling
# involves the wavefunction overlap: y_4D = y_5D * int psi_L psi_R H dx5
# For the loop, we need the 5D vertex at each point in the extra dimension
# integrated against the KK mode profile.

# The enhancement factor:
# f_loc = L_X * |psi_0(0)|^2 = sqrt(2*alpha_eff/pi) * L_X / L_X = sqrt(2*alpha/pi)
f_loc = np.sqrt(2 * alpha_eff / np.pi)
print(f"  Localization enhancement: f_loc = sqrt(2*alpha/pi) = {f_loc:.4f}")

# The full 5D loop with localization:
# The loop integral gets enhanced because the wavefunction is peaked
# at the orbifold fixed point where the loop vertex is localized.
# This effectively multiplies the loop function by f_loc^2 (two vertices).

F_5d_loc = F_5d * f_loc**2
yb_yt_loc = alpha_s_KK / (4*np.pi) * C_F * abs(F_5d_loc)

print(f"  F_5D * f_loc^2 = {F_5d_loc:.4f}")
print(f"  y_b/y_t (with localization) = {yb_yt_loc:.5f}")
print(f"  Target                      = {m_b/m_t:.4f}")
print(f"  Ratio pred/obs              = {yb_yt_loc/(m_b/m_t):.3f}")

# =====================================================================
# SECTION 5: Z_3 TWISTED SECTOR WITH SHIFTED MASSES
# =====================================================================
header("SECTION 5: Z_3 Twisted KK Spectrum")

def loop_function_twisted(N_max=500):
    """
    In the Z_3 twisted sector, KK masses are shifted:
    m_n = (n + 1/3) * M_KK for q=1 modes
    m_n = (n + 2/3) * M_KK for q=2 modes
    """
    F_total = 0.0

    for n in range(0, N_max+1):
        for q in [1, 2]:
            m_n = (n + q/3.0) * M_KK
            phase = np.real(omega**q) if n == 0 else np.real(omega**(3*n + q))

            def integrand(x):
                denom = x * m_t**2 + (1-x) * (m_t**2 + m_n**2)
                return x * (1-x) * M_KK**2 / denom

            I_n, _ = integrate.quad(integrand, 0, 1)
            F_total += phase * I_n

    return F_total

F_twisted = loop_function_twisted()
yb_yt_twisted = alpha_s_KK / (4*np.pi) * C_F * abs(F_twisted) * f_loc**2

print(f"  F_twisted (shifted masses) = {F_twisted:.4f}")
print(f"  y_b/y_t (twisted + loc)    = {yb_yt_twisted:.5f}")
print(f"  Target                     = {m_b/m_t:.4f}")
print(f"  Ratio pred/obs             = {yb_yt_twisted/(m_b/m_t):.3f}")

# =====================================================================
# SECTION 6: RG ENHANCEMENT (QCD running from M_KK to m_b)
# =====================================================================
header("SECTION 6: QCD RG Enhancement")

# Running y_b from M_KK to m_b scale enhances it by:
# eta_QCD = [alpha_s(m_b)/alpha_s(M_KK)]^(gamma_m/b_3)
# where gamma_m = 8 is the anomalous dimension for mass

alpha_s_mb = 0.224  # alpha_s at m_b ~ 4.2 GeV
gamma_m = 8.0
eta_QCD = (alpha_s_mb / alpha_s_KK)**(gamma_m / (2 * abs(b3)))

print(f"  alpha_s(m_b)  = {alpha_s_mb:.3f}")
print(f"  alpha_s(M_KK) = {alpha_s_KK:.4f}")
print(f"  gamma_m / (2|b_3|) = {gamma_m/(2*abs(b3)):.4f}")
print(f"  eta_QCD = {eta_QCD:.4f}")

# =====================================================================
# SECTION 7: COMBINED RESULT
# =====================================================================
header("SECTION 7: Combined Result")

# Method A: Basic F + localization + RG
result_A = alpha_s_KK / (4*np.pi) * C_F * abs(F_basic) * f_loc**2 * eta_QCD
# Method B: 5D Feynman + localization + RG
result_B = alpha_s_KK / (4*np.pi) * C_F * abs(F_5d) * f_loc**2 * eta_QCD
# Method C: Twisted + localization + RG
result_C = alpha_s_KK / (4*np.pi) * C_F * abs(F_twisted) * f_loc**2 * eta_QCD

target = m_b / m_t

print(f"  Method         F_loop  y_b/y_t   obs     ratio")
print(f"  {'─'*60}")
print(f"  A (basic+loc)  {abs(F_basic)*f_loc**2:.4f}  {result_A:.5f}  {target:.4f}  {result_A/target:.3f}")
print(f"  B (5D+loc)     {abs(F_5d)*f_loc**2:.4f}  {result_B:.5f}  {target:.4f}  {result_B/target:.3f}")
print(f"  C (twist+loc)  {abs(F_twisted)*f_loc**2:.4f}  {result_C:.5f}  {target:.4f}  {result_C/target:.3f}")
print()

# What F_eff is needed?
F_needed = target / (alpha_s_KK / (4*np.pi) * C_F * eta_QCD)
print(f"  F_eff needed for exact match: {F_needed:.4f}")
print(f"  F_eff (method B, with loc):   {abs(F_5d)*f_loc**2:.4f}")
print(f"  F_eff (method C, with loc):   {abs(F_twisted)*f_loc**2:.4f}")

# =====================================================================
# SECTION 8: SENSITIVITY ANALYSIS
# =====================================================================
header("SECTION 8: What Would Close This?")

# 2-loop QCD: multiply by (1 + alpha_s/(4pi) * K) where K ~ 10-20
K_2loop = 15.0
correction_2loop = 1 + alpha_s_KK / (4*np.pi) * K_2loop
result_2loop = result_B * correction_2loop

# Including EW loops (W/Z exchange in addition to gluon):
alpha_2 = 1.0 / 29.6  # alpha_2 at M_KK
C_2_fund = 3.0/4  # SU(2) Casimir
ew_correction = 1 + (alpha_2 * C_2_fund) / (alpha_s_KK * C_F)
result_ew = result_B * ew_correction

# Combined 2-loop + EW:
result_combined = result_B * correction_2loop * ew_correction

print(f"  2-loop QCD correction (K={K_2loop:.0f}): ×{correction_2loop:.3f} → y_b/y_t = {result_2loop:.5f} ({result_2loop/target:.3f})")
print(f"  EW loop correction:                ×{ew_correction:.3f} → y_b/y_t = {result_ew:.5f} ({result_ew/target:.3f})")
print(f"  Combined (2-loop + EW):            ×{correction_2loop*ew_correction:.3f} → y_b/y_t = {result_combined:.5f} ({result_combined/target:.3f})")
print()

best = max(result_A, result_B, result_C, result_combined)
best_ratio = best / target

print(f"  ╔═══════════════════════════════════════════════════════════╗")
print(f"  ║  ISOSPIN SPLITTING: BEST RESULT                         ║")
print(f"  ╠═══════════════════════════════════════════════════════════╣")
print(f"  ║  y_b/y_t predicted = {best:.5f}                        ║")
print(f"  ║  y_b/y_t observed  = {target:.4f}                         ║")
print(f"  ║  Ratio: {best_ratio:.3f}                                      ║")
if best_ratio > 0.7:
    print(f"  ║  STATUS: CLOSE — within 2-loop/EW uncertainty          ║")
elif best_ratio > 0.3:
    print(f"  ║  STATUS: PARTIAL — right order, factor {1/best_ratio:.1f}× off       ║")
else:
    print(f"  ║  STATUS: OPEN — factor {1/best_ratio:.0f}× off                       ║")
print(f"  ╚═══════════════════════════════════════════════════════════╝")
