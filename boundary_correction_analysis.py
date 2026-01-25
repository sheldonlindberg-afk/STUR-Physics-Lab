#!/usr/bin/env python3
"""
COMPREHENSIVE BOUNDARY CORRECTION FACTOR ANALYSIS
==================================================

This script investigates multiple possible interpretations of the
"boundary correction factor" to understand where 0.65 might come from.

The basic calculation shows f_boundary > 1, which contradicts the
document's claim of 0.65. Let's explore alternative interpretations.
"""

import math

def erf(x):
    """Error function (Abramowitz & Stegun 7.1.26)"""
    sign = 1 if x >= 0 else -1
    x = abs(x)
    t = 1.0 / (1.0 + 0.3275911 * x)
    y = 1.0 - (((((1.061405429*t - 1.453152027)*t) + 1.421413741)*t - 0.284496736)*t + 0.254829592)*t * math.exp(-x*x)
    return sign * y

def integrate(func, a, b, n=10000):
    """Simpson's rule integration"""
    if n % 2 == 1: n += 1
    h = (b - a) / n
    result = func(a) + func(b)
    for i in range(1, n, 2):
        result += 4 * func(a + i * h)
    for i in range(2, n, 2):
        result += 2 * func(a + i * h)
    return result * h / 3

# Parameters
kappa = 2.5
sigma = (2 * math.pi / 3) / kappa
phi_1, phi_2, phi_3 = 0.0, 2*math.pi/3, 4*math.pi/3
Delta = 2 * math.pi / 3

print("=" * 75)
print("INVESTIGATING THE ORIGIN OF f_boundary = 0.65")
print("=" * 75)

# ============================================================================
# INTERPRETATION 1: Document's stated formula [erf(d/2sigma)]^2
# ============================================================================

print("\n" + "-" * 75)
print("INTERPRETATION 1: Document's formula f = [erf(d/(2*sigma))]^2")
print("-" * 75)

d = Delta
x = d / (2 * sigma)
f_doc = erf(x)**2

print(f"  d = 2*pi/3 = {d:.6f}")
print(f"  sigma = {sigma:.6f}")
print(f"  d/(2*sigma) = {x:.6f}")
print(f"  erf({x:.4f}) = {erf(x):.6f}")
print(f"  f = [erf({x:.4f})]^2 = {f_doc:.6f}")
print(f"\n  This gives f = {f_doc:.3f}, NOT 0.65")

# ============================================================================
# INTERPRETATION 2: Fraction of wavefunction in "wrong" sector
# ============================================================================

print("\n" + "-" * 75)
print("INTERPRETATION 2: Leakage into adjacent Z_3 sectors")
print("-" * 75)

# Each generation is in a sector of width 2*pi/3
# The wavefunction leaks into adjacent sectors
# For generation 1 at phi=0, the sector is [-pi/3, pi/3] (wrapping)

def fraction_in_sector(phi_center, sector_start, sector_end, sigma):
    """Fraction of Gaussian in a given sector"""
    sqrt2_sigma = math.sqrt(2) * sigma
    x_up = (sector_end - phi_center) / sqrt2_sigma
    x_lo = (sector_start - phi_center) / sqrt2_sigma
    return 0.5 * (erf(x_up) - erf(x_lo))

# Generation 1 at phi=0, its natural sector is [-pi/3, pi/3] = [5*pi/3, 2*pi] + [0, pi/3]
# Or we can use [0, 2*pi/3] as the "first sector"
sector_width = 2*math.pi/3

f_1_in_sector_1 = fraction_in_sector(phi_1, -math.pi/3, math.pi/3, sigma)
f_2_in_sector_2 = fraction_in_sector(phi_2, math.pi/3, math.pi, sigma)

print(f"  Fraction of psi_1 in sector [-pi/3, pi/3]: {f_1_in_sector_1:.4f}")
print(f"  Fraction of psi_2 in sector [pi/3, pi]: {f_2_in_sector_2:.4f}")

# The "reduction" could be due to leaked amplitude
leakage_1 = 1 - f_1_in_sector_1
leakage_2 = 1 - f_2_in_sector_2
print(f"  Leakage from sector 1: {leakage_1:.4f}")
print(f"  Leakage from sector 2: {leakage_2:.4f}")

# ============================================================================
# INTERPRETATION 3: Overlap restricted to overlap region
# ============================================================================

print("\n" + "-" * 75)
print("INTERPRETATION 3: Overlap in the 'interaction region'")
print("-" * 75)

# The overlap between psi_1 and psi_2 is significant only near phi = pi/3
# (the midpoint between phi_1=0 and phi_2=2*pi/3)
# If we restrict to a region of width ~2*sigma around this point...

phi_mid = (phi_1 + phi_2) / 2  # = pi/3
region_half_width = sigma  # 1-sigma region

def psi(phi, phi_g):
    return math.exp(-(phi - phi_g)**2 / (4 * sigma**2))

# Full domain overlap
overlap_full = integrate(lambda phi: psi(phi, phi_1) * psi(phi, phi_2), 0, 2*math.pi)

# Restricted to region around phi_mid
restricted_start = max(0, phi_mid - 2*sigma)
restricted_end = min(2*math.pi, phi_mid + 2*sigma)
overlap_restricted = integrate(lambda phi: psi(phi, phi_1) * psi(phi, phi_2),
                               restricted_start, restricted_end)

f_region = overlap_restricted / overlap_full
print(f"  Overlap region: [{restricted_start:.3f}, {restricted_end:.3f}]")
print(f"  Full overlap: {overlap_full:.6f}")
print(f"  Restricted overlap: {overlap_restricted:.6f}")
print(f"  Ratio: {f_region:.4f}")

# ============================================================================
# INTERPRETATION 4: Effect of Z_3 phase factor in Yukawa coupling
# ============================================================================

print("\n" + "-" * 75)
print("INTERPRETATION 4: Z_3 phase factor in Higgs coupling")
print("-" * 75)

# Perhaps the Higgs field has a Z_3 phase structure:
# H(phi) = h_0 * exp[i * floor(3*phi/(2*pi)) * 2*pi/3]
# This introduces phase factors that reduce the overlap

def phase_factor(phi):
    """Z_3 phase factor"""
    sector = int(3 * phi / (2 * math.pi)) % 3
    return math.cos(sector * 2 * math.pi / 3)  # Real part only

# Modified overlap with phase factor
overlap_with_phase = integrate(lambda phi: psi(phi, phi_1) * psi(phi, phi_2) * phase_factor(phi),
                               0, 2*math.pi)
f_phase = overlap_with_phase / overlap_full
print(f"  Overlap without phase: {overlap_full:.6f}")
print(f"  Overlap with Z_3 phase: {overlap_with_phase:.6f}")
print(f"  Ratio: {f_phase:.4f}")

# ============================================================================
# INTERPRETATION 5: Wavefunction mismatch at Z_3 boundaries
# ============================================================================

print("\n" + "-" * 75)
print("INTERPRETATION 5: Sharp damping at Z_3 phase boundaries")
print("-" * 75)

# Perhaps the wavefunctions are damped at the Z_3 boundaries
# (phi = 0, 2*pi/3, 4*pi/3) where the R-field phase changes

def damping_at_boundaries(phi, width=0.1):
    """Damping factor near Z_3 boundaries"""
    boundaries = [0, 2*math.pi/3, 4*math.pi/3, 2*math.pi]
    result = 1.0
    for b in boundaries:
        dist = min(abs(phi - b), 2*math.pi - abs(phi - b)) if phi != b else 0
        # Smooth step function
        if dist < width:
            result *= dist / width
    return result

overlap_with_damping = integrate(
    lambda phi: psi(phi, phi_1) * psi(phi, phi_2) * damping_at_boundaries(phi, width=0.2),
    0, 2*math.pi)
f_damping = overlap_with_damping / overlap_full
print(f"  Overlap without damping: {overlap_full:.6f}")
print(f"  Overlap with boundary damping: {overlap_with_damping:.6f}")
print(f"  Ratio: {f_damping:.4f}")

# ============================================================================
# INTERPRETATION 6: The ratio lambda_phys/lambda_bare with corrections
# ============================================================================

print("\n" + "-" * 75)
print("INTERPRETATION 6: lambda_phys / lambda_bare decomposition")
print("-" * 75)

# Document claims:
# lambda_phys = lambda_bare * (boundary) * (holonomy) * (RG)
#             = 0.458     * 0.65      * 0.85       * 0.87
#             = 0.220

# lambda_bare = exp[-kappa^2/8]
lambda_bare = math.exp(-kappa**2 / 8)
lambda_target = 0.225  # PDG value

print(f"  lambda_bare = exp[-kappa^2/8] = {lambda_bare:.4f}")
print(f"  lambda_target (PDG) = {lambda_target:.4f}")

# What total correction factor is needed?
total_correction_needed = lambda_target / lambda_bare
print(f"  Total correction needed: {total_correction_needed:.4f}")

# Document claims: 0.65 * 0.85 * 0.87 = 0.48
claimed_correction = 0.65 * 0.85 * 0.87
print(f"  Document's claimed correction: 0.65 * 0.85 * 0.87 = {claimed_correction:.4f}")
print(f"  lambda_phys (document): {lambda_bare * claimed_correction:.4f}")

# If we use our calculated f_boundary ~ 1.27...
our_f_boundary = 1.27
our_correction = our_f_boundary * 0.85 * 0.87
print(f"\n  With our f_boundary = 1.27:")
print(f"  Total correction: 1.27 * 0.85 * 0.87 = {our_correction:.4f}")
print(f"  lambda_phys: {lambda_bare * our_correction:.4f}")
print(f"  This is WAY OFF from target!")

# ============================================================================
# INTERPRETATION 7: Perhaps boundary reduces the BARE value differently
# ============================================================================

print("\n" + "-" * 75)
print("INTERPRETATION 7: Direct effect on wavefunction width")
print("-" * 75)

# Perhaps the 0.65 represents a reduction in the effective sigma due to boundaries
# Larger effective kappa -> smaller lambda_bare

# If f_boundary = 0.65 represents lambda_eff / lambda_bare, then:
# exp[-kappa_eff^2/8] / exp[-kappa^2/8] = 0.65
# -kappa_eff^2/8 + kappa^2/8 = ln(0.65)
# kappa_eff^2 - kappa^2 = -8 * ln(0.65)
# kappa_eff = sqrt(kappa^2 - 8*ln(0.65))

if kappa**2 - 8*math.log(0.65) > 0:
    kappa_eff = math.sqrt(kappa**2 - 8*math.log(0.65))
    print(f"  If f = 0.65 means lambda_eff = lambda_bare * 0.65:")
    print(f"  kappa_eff = sqrt(kappa^2 - 8*ln(0.65)) = {kappa_eff:.4f}")
    print(f"  (This would mean effective kappa increases from 2.5 to {kappa_eff:.2f})")
else:
    print(f"  No solution: kappa^2 - 8*ln(0.65) < 0")

# ============================================================================
# INTERPRETATION 8: Inverse interpretation - boundaries INCREASE suppression
# ============================================================================

print("\n" + "-" * 75)
print("INTERPRETATION 8: Boundaries increase the effective distance")
print("-" * 75)

# Perhaps the 0.65 represents the fact that with boundaries, the "effective"
# distance between generations is larger

# If exp[-Delta_eff^2/(8*sigma^2)] = 0.65 * exp[-Delta^2/(8*sigma^2)]
# Then -Delta_eff^2/(8*sigma^2) = ln(0.65) - Delta^2/(8*sigma^2)
# Delta_eff^2 = Delta^2 - 8*sigma^2*ln(0.65)
Delta_eff_sq = Delta**2 - 8*sigma**2*math.log(0.65)
if Delta_eff_sq > 0:
    Delta_eff = math.sqrt(Delta_eff_sq)
    print(f"  If boundaries make effective distance larger:")
    print(f"  Delta_eff = {Delta_eff:.4f} (vs Delta = {Delta:.4f})")
    print(f"  Ratio: {Delta_eff/Delta:.4f}")

# ============================================================================
# INTERPRETATION 9: Could 0.65 be 1/f_boundary where f > 1?
# ============================================================================

print("\n" + "-" * 75)
print("INTERPRETATION 9: Is 0.65 actually 1/f_boundary?")
print("-" * 75)

# Our calculation gives f_boundary ~ 1.27
# 1/1.27 = 0.79, not 0.65
# But with periodic images, f_boundary ~ 1.55
# 1/1.55 = 0.65!

print(f"  Our f_boundary (normalized): 1.27")
print(f"  1/1.27 = {1/1.27:.4f}")
print(f"\n  Our f_boundary (periodic images): 1.55")
print(f"  1/1.55 = {1/1.55:.4f} <- CLOSE TO 0.65!")

print("\n  This suggests the document may have INVERTED the correction!")

# ============================================================================
# FINAL ANALYSIS
# ============================================================================

print("\n" + "=" * 75)
print("FINAL ANALYSIS")
print("=" * 75)

print("""
SUMMARY OF FINDINGS:

The explicit calculation from first principles shows that the boundary
correction factor depends on the interpretation:

1. Simple finite-domain truncation: f_boundary > 1
   - This is because generation 1 at phi=0 loses half its probability
     to phi<0, which gets renormalized, effectively BOOSTING its
     contribution to the overlap ratio.

2. With periodic images (proper Z_3 treatment): f_boundary ~ 1.55
   - The periodic structure actually INCREASES the overlap

3. The inverse, 1/f_boundary ~ 0.65, matches the document's value!

POSSIBLE EXPLANATION:
   The document may be using the INVERSE of the overlap enhancement
   as a "suppression factor" in a different context.

   Alternatively, if the Higgs profile H(phi) is localized rather than
   constant, this would suppress off-diagonal couplings.

HONEST CONCLUSION:
   The value 0.65 is NOT derivable from simple Gaussian overlap
   truncation at domain boundaries as described in the document.

   The calculation gives f_boundary ~ 1.27 to 1.55, meaning the
   finite domain ENHANCES rather than suppresses the overlap.

   The claimed value of 0.65 either:
   a) Represents a different physical effect entirely
   b) Is the inverse of the actual boundary factor
   c) Includes unstated assumptions about the Higgs profile
   d) May simply be incorrect
""")

# ============================================================================
# WHAT IF HIGGS IS LOCALIZED?
# ============================================================================

print("-" * 75)
print("ADDITIONAL TEST: Localized Higgs profile")
print("-" * 75)

# If H(phi) is localized at one generation (say phi=0), this would
# suppress Y_12 relative to Y_11

def H_localized(phi, phi_H, sigma_H):
    """Higgs localized at phi_H with width sigma_H"""
    return math.exp(-(phi - phi_H)**2 / (4 * sigma_H**2))

# Y_12 with localized Higgs at phi=0
Y_12_H_at_0 = integrate(
    lambda phi: psi(phi, phi_1) * H_localized(phi, 0, sigma) * psi(phi, phi_2),
    0, 2*math.pi)

Y_11_H_at_0 = integrate(
    lambda phi: psi(phi, phi_1) * H_localized(phi, 0, sigma) * psi(phi, phi_1),
    0, 2*math.pi)

Y_12_H_const = integrate(
    lambda phi: psi(phi, phi_1) * 1.0 * psi(phi, phi_2),
    0, 2*math.pi)

Y_11_H_const = integrate(
    lambda phi: psi(phi, phi_1) * 1.0 * psi(phi, phi_1),
    0, 2*math.pi)

lambda_H_loc = Y_12_H_at_0 / math.sqrt(Y_11_H_at_0 * Y_11_H_at_0)  # Using Y_11 twice since Y_22 undefined for H at phi_1
lambda_H_const = Y_12_H_const / Y_11_H_const  # Simplified ratio

print(f"  With Higgs at phi=0 (width sigma):")
print(f"  Y_12/Y_11 (H localized) = {Y_12_H_at_0/Y_11_H_at_0:.6f}")
print(f"  Y_12/Y_11 (H constant) = {Y_12_H_const/Y_11_H_const:.6f}")
print(f"  Suppression factor: {(Y_12_H_at_0/Y_11_H_at_0)/(Y_12_H_const/Y_11_H_const):.4f}")
