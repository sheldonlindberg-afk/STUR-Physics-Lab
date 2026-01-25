#!/usr/bin/env python3
"""
BOUNDARY CORRECTION FACTOR CALCULATION FOR STUR FRAMEWORK
==========================================================

This script computes the boundary correction factor f_boundary from first principles.

PROBLEM: The STUR framework claims a boundary correction factor of 0.65, but the
explicit calculation was not shown. This script performs that calculation.

PHYSICAL SETUP:
- Three fermion generations localized at phases phi_1=0, phi_2=2pi/3, phi_3=4pi/3
- Gaussian wavefunctions: psi_g(phi) = N * exp[-(phi - phi_g)^2 / (4*sigma^2)]
- Localization width: sigma = (2pi/3) / kappa with kappa = 2.5
- Domain: [0, 2pi) with periodic boundary conditions (Z_3 identification)

BOUNDARY CORRECTION ARISES FROM:
1. Truncation of Gaussian tails at domain boundaries [0, 2pi)
2. Z_3 periodicity affecting the integration measure
3. Interference from periodic images

Author: Theoretical Physics Calculation
Date: 2026-01-25
"""

import numpy as np
from scipy import integrate
from scipy.special import erf
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# PARAMETERS FROM STUR FRAMEWORK
# ============================================================================

kappa = 2.5  # Localization parameter
sigma = (2 * np.pi / 3) / kappa  # Localization width = 0.838 radians

# Generation phases (Z_3 fixed points)
phi_1 = 0.0
phi_2 = 2 * np.pi / 3
phi_3 = 4 * np.pi / 3

print("=" * 70)
print("BOUNDARY CORRECTION FACTOR CALCULATION")
print("=" * 70)
print(f"\nParameters:")
print(f"  kappa = {kappa}")
print(f"  sigma = 2*pi/(3*kappa) = {sigma:.6f} rad = {np.degrees(sigma):.3f} deg")
print(f"  Generation phases: phi_1={phi_1:.4f}, phi_2={phi_2:.4f}, phi_3={phi_3:.4f}")

# ============================================================================
# PART 1: DEFINE WAVEFUNCTIONS
# ============================================================================

print("\n" + "=" * 70)
print("PART 1: GAUSSIAN WAVEFUNCTIONS")
print("=" * 70)

def gaussian_unnormalized(phi, phi_g, sigma):
    """Unnormalized Gaussian wavefunction centered at phi_g"""
    return np.exp(-(phi - phi_g)**2 / (4 * sigma**2))

def gaussian_periodic(phi, phi_g, sigma, n_images=5):
    """
    Gaussian wavefunction with periodic images for proper Z_3 treatment.
    Includes images at phi_g + 2*pi*n for periodic boundary conditions.
    """
    result = 0.0
    for n in range(-n_images, n_images + 1):
        result += np.exp(-(phi - phi_g - 2*np.pi*n)**2 / (4 * sigma**2))
    return result

# ============================================================================
# PART 2: COMPUTE INFINITE-DOMAIN GAUSSIAN INTEGRAL
# ============================================================================

print("\n" + "=" * 70)
print("PART 2: INFINITE-DOMAIN GAUSSIAN OVERLAP")
print("=" * 70)

# For two Gaussians centered at phi_i and phi_j:
# Integral[-inf, +inf] of exp[-(phi-phi_i)^2/(4sigma^2)] * exp[-(phi-phi_j)^2/(4sigma^2)] dphi

# Using the formula: integral of exp(-ax^2 + bx) = sqrt(pi/a) * exp(b^2/(4a))
# After completing the square, we get:
# I_infinite = sqrt(2*pi) * sigma * exp[-Delta_phi^2 / (8*sigma^2)]

def infinite_domain_overlap(phi_i, phi_j, sigma):
    """
    Analytic result for overlap integral on infinite domain.

    I = integral_{-inf}^{+inf} psi_i*(phi) psi_j(phi) dphi

    For normalized Gaussians, this equals exp[-Delta^2 / (8*sigma^2)]
    where Delta = |phi_i - phi_j|
    """
    Delta = abs(phi_j - phi_i)
    return np.exp(-Delta**2 / (8 * sigma**2))

# Compute infinite-domain overlaps
Delta_12 = phi_2 - phi_1  # = 2*pi/3
Delta_23 = phi_3 - phi_2  # = 2*pi/3
Delta_13 = phi_3 - phi_1  # = 4*pi/3 (or -2*pi/3 with periodicity)

# With periodicity, Delta_13 should be min(4*pi/3, 2*pi - 4*pi/3) = 2*pi/3
Delta_13_periodic = min(Delta_13, 2*np.pi - Delta_13)

I_inf_12 = infinite_domain_overlap(phi_1, phi_2, sigma)
I_inf_11 = 1.0  # Same generation, fully overlapping

print(f"\nInfinite-domain results (analytic):")
print(f"  Delta_12 = 2*pi/3 = {Delta_12:.6f}")
print(f"  Delta_12 / sigma = {Delta_12/sigma:.6f}")
print(f"  Delta_12 / (2*sigma) = {Delta_12/(2*sigma):.6f}")
print(f"\n  I_infinite(1,1) = 1.0 (normalized)")
print(f"  I_infinite(1,2) = exp[-Delta^2/(8*sigma^2)]")
print(f"               = exp[-({Delta_12:.4f})^2/(8*{sigma:.4f}^2)]")
print(f"               = exp[-{Delta_12**2/(8*sigma**2):.6f}]")
print(f"               = {I_inf_12:.6f}")

# This gives us lambda_bare = exp[-kappa^2/8]
lambda_bare = np.exp(-kappa**2 / 8)
print(f"\n  Lambda_bare = exp[-kappa^2/8] = exp[-{kappa**2/8:.4f}] = {lambda_bare:.6f}")
print(f"  (Matches I_infinite(1,2)? {np.isclose(I_inf_12, lambda_bare)})")

# ============================================================================
# PART 3: COMPUTE FINITE-DOMAIN INTEGRALS (NUMERICAL)
# ============================================================================

print("\n" + "=" * 70)
print("PART 3: FINITE-DOMAIN INTEGRALS [0, 2*pi)")
print("=" * 70)

def normalized_wavefunction(phi, phi_g, sigma):
    """Properly normalized Gaussian on finite domain [0, 2*pi)"""
    # First compute the normalization factor
    norm_integrand = lambda x: np.exp(-(x - phi_g)**2 / (2 * sigma**2))
    norm_sq, _ = integrate.quad(norm_integrand, 0, 2*np.pi)
    N = 1.0 / np.sqrt(norm_sq)
    return N * np.exp(-(phi - phi_g)**2 / (4 * sigma**2))

def compute_normalization(phi_g, sigma):
    """Compute normalization factor for Gaussian on [0, 2*pi)"""
    integrand = lambda x: np.exp(-(x - phi_g)**2 / (2 * sigma**2))
    norm_sq, _ = integrate.quad(integrand, 0, 2*np.pi)
    return 1.0 / np.sqrt(norm_sq)

# Compute normalization factors for each generation
N_1 = compute_normalization(phi_1, sigma)
N_2 = compute_normalization(phi_2, sigma)
N_3 = compute_normalization(phi_3, sigma)

print(f"\nNormalization factors (finite domain [0, 2*pi)):")
print(f"  N_1 (phi=0) = {N_1:.6f}")
print(f"  N_2 (phi=2*pi/3) = {N_2:.6f}")
print(f"  N_3 (phi=4*pi/3) = {N_3:.6f}")

# For infinite domain, N_ideal = (1/(2*pi*sigma^2))^(1/4) = (2*sigma^2)^(-1/4) * pi^(-1/4)
# Actually for |psi|^2 normalization: N_ideal = 1/(2*pi*sigma^2)^(1/4) for psi
# and for |psi|^2, integrating gives N^2 * sqrt(2*pi) * sigma = 1
# So N_ideal = (1/(sqrt(2*pi)*sigma))^(1/2) = (2*pi)^(-1/4) * sigma^(-1/2)
N_ideal = (2*np.pi)**(-0.25) * sigma**(-0.5)
print(f"  N_ideal (infinite domain) = {N_ideal:.6f}")

# ============================================================================
# PART 4: OVERLAP INTEGRALS ON FINITE DOMAIN
# ============================================================================

print("\n" + "=" * 70)
print("PART 4: OVERLAP INTEGRALS Y_ij ON [0, 2*pi)")
print("=" * 70)

def overlap_integral_finite(phi_i, phi_j, sigma, use_periodic_images=False):
    """
    Compute overlap integral on finite domain [0, 2*pi)

    Y_ij = integral_0^{2*pi} psi_i*(phi) * H(phi) * psi_j(phi) dphi

    Assuming H(phi) = h_0 (constant), we get:
    Y_ij = h_0 * integral_0^{2*pi} psi_i*(phi) * psi_j(phi) dphi
    """
    if use_periodic_images:
        # Include periodic images for proper periodicity
        def integrand(phi):
            psi_i = 0.0
            psi_j = 0.0
            for n in range(-3, 4):
                psi_i += np.exp(-(phi - phi_i - 2*np.pi*n)**2 / (4 * sigma**2))
                psi_j += np.exp(-(phi - phi_j - 2*np.pi*n)**2 / (4 * sigma**2))
            return psi_i * psi_j
    else:
        # Simple truncation at boundaries
        def integrand(phi):
            psi_i = np.exp(-(phi - phi_i)**2 / (4 * sigma**2))
            psi_j = np.exp(-(phi - phi_j)**2 / (4 * sigma**2))
            return psi_i * psi_j

    result, error = integrate.quad(integrand, 0, 2*np.pi, limit=100)
    return result, error

# Compute overlaps WITHOUT periodic images (simple truncation)
print("\nCase A: Simple truncation (no periodic images)")
Y_11_trunc, err_11 = overlap_integral_finite(phi_1, phi_1, sigma, use_periodic_images=False)
Y_12_trunc, err_12 = overlap_integral_finite(phi_1, phi_2, sigma, use_periodic_images=False)
Y_22_trunc, err_22 = overlap_integral_finite(phi_2, phi_2, sigma, use_periodic_images=False)
Y_23_trunc, err_23 = overlap_integral_finite(phi_2, phi_3, sigma, use_periodic_images=False)

print(f"  Y_11 (unnormalized) = {Y_11_trunc:.6f}")
print(f"  Y_22 (unnormalized) = {Y_22_trunc:.6f}")
print(f"  Y_12 (unnormalized) = {Y_12_trunc:.6f}")
print(f"  Y_23 (unnormalized) = {Y_23_trunc:.6f}")

# Compute overlaps WITH periodic images
print("\nCase B: With periodic images (proper Z_3 periodicity)")
Y_11_per, err_11p = overlap_integral_finite(phi_1, phi_1, sigma, use_periodic_images=True)
Y_12_per, err_12p = overlap_integral_finite(phi_1, phi_2, sigma, use_periodic_images=True)
Y_22_per, err_22p = overlap_integral_finite(phi_2, phi_2, sigma, use_periodic_images=True)
Y_23_per, err_23p = overlap_integral_finite(phi_2, phi_3, sigma, use_periodic_images=True)

print(f"  Y_11 (unnormalized) = {Y_11_per:.6f}")
print(f"  Y_22 (unnormalized) = {Y_22_per:.6f}")
print(f"  Y_12 (unnormalized) = {Y_12_per:.6f}")
print(f"  Y_23 (unnormalized) = {Y_23_per:.6f}")

# ============================================================================
# PART 5: COMPUTE BOUNDARY CORRECTION FACTOR
# ============================================================================

print("\n" + "=" * 70)
print("PART 5: BOUNDARY CORRECTION FACTOR CALCULATION")
print("=" * 70)

# The infinite-domain result for Y_12 (unnormalized):
# I_inf = sqrt(2*pi) * sigma * exp[-Delta^2/(8*sigma^2)]
# where the factor sqrt(2*pi)*sigma comes from the Gaussian integral
I_inf_unnorm_11 = np.sqrt(2*np.pi) * sigma
I_inf_unnorm_12 = np.sqrt(2*np.pi) * sigma * np.exp(-Delta_12**2 / (8*sigma**2))

print(f"\nInfinite-domain overlaps (unnormalized):")
print(f"  I_inf(1,1) = sqrt(2*pi)*sigma = {I_inf_unnorm_11:.6f}")
print(f"  I_inf(1,2) = sqrt(2*pi)*sigma*exp[-Delta^2/(8*sigma^2)] = {I_inf_unnorm_12:.6f}")

# Now compute the boundary correction factor
print("\n" + "-" * 50)
print("METHOD 1: Simple ratio of finite/infinite integrals")
print("-" * 50)

f_boundary_11_trunc = Y_11_trunc / I_inf_unnorm_11
f_boundary_12_trunc = Y_12_trunc / I_inf_unnorm_12
f_boundary_11_per = Y_11_per / I_inf_unnorm_11
f_boundary_12_per = Y_12_per / I_inf_unnorm_12

print(f"\nSimple truncation:")
print(f"  f_boundary(1,1) = Y_11_finite / Y_11_infinite = {f_boundary_11_trunc:.6f}")
print(f"  f_boundary(1,2) = Y_12_finite / Y_12_infinite = {f_boundary_12_trunc:.6f}")

print(f"\nWith periodic images:")
print(f"  f_boundary(1,1) = Y_11_finite / Y_11_infinite = {f_boundary_11_per:.6f}")
print(f"  f_boundary(1,2) = Y_12_finite / Y_12_infinite = {f_boundary_12_per:.6f}")

# ============================================================================
# PART 6: NORMALIZED OVERLAP RATIO (THE ACTUAL LAMBDA CORRECTION)
# ============================================================================

print("\n" + "-" * 50)
print("METHOD 2: Ratio of normalized overlaps (lambda correction)")
print("-" * 50)

# The Yukawa hierarchy parameter lambda is defined as:
# lambda = Y_{12} / sqrt(Y_{11} * Y_{22})
# or simply the ratio of off-diagonal to diagonal Yukawa

# For properly normalized wavefunctions:
def compute_normalized_overlap(phi_i, phi_j, sigma, use_periodic=False):
    """Compute overlap with properly normalized wavefunctions on [0, 2*pi)"""

    if use_periodic:
        def psi(phi, phi_g):
            result = 0.0
            for n in range(-3, 4):
                result += np.exp(-(phi - phi_g - 2*np.pi*n)**2 / (4 * sigma**2))
            return result
    else:
        def psi(phi, phi_g):
            return np.exp(-(phi - phi_g)**2 / (4 * sigma**2))

    # Compute normalization factors
    norm_i_sq, _ = integrate.quad(lambda x: psi(x, phi_i)**2, 0, 2*np.pi)
    norm_j_sq, _ = integrate.quad(lambda x: psi(x, phi_j)**2, 0, 2*np.pi)
    N_i = 1.0 / np.sqrt(norm_i_sq)
    N_j = 1.0 / np.sqrt(norm_j_sq)

    # Compute overlap
    overlap, _ = integrate.quad(lambda x: psi(x, phi_i) * psi(x, phi_j), 0, 2*np.pi)

    return N_i * N_j * overlap

# Compute normalized overlaps
lambda_finite_trunc = compute_normalized_overlap(phi_1, phi_2, sigma, use_periodic=False)
lambda_finite_per = compute_normalized_overlap(phi_1, phi_2, sigma, use_periodic=True)

# The infinite-domain result (normalized Gaussians)
lambda_infinite = np.exp(-Delta_12**2 / (8 * sigma**2))

print(f"\nNormalized overlaps (lambda values):")
print(f"  lambda_infinite = {lambda_infinite:.6f}")
print(f"  lambda_finite (truncation) = {lambda_finite_trunc:.6f}")
print(f"  lambda_finite (periodic) = {lambda_finite_per:.6f}")

f_lambda_trunc = lambda_finite_trunc / lambda_infinite
f_lambda_per = lambda_finite_per / lambda_infinite

print(f"\nBoundary correction for lambda:")
print(f"  f_boundary (truncation) = lambda_finite/lambda_infinite = {f_lambda_trunc:.6f}")
print(f"  f_boundary (periodic) = lambda_finite/lambda_infinite = {f_lambda_per:.6f}")

# ============================================================================
# PART 7: ERROR FUNCTION ANALYSIS
# ============================================================================

print("\n" + "-" * 50)
print("METHOD 3: Analytic error function evaluation")
print("-" * 50)

# For a Gaussian centered at phi_g, the integral from 0 to 2*pi can be written
# in terms of error functions

def erf_integral(phi_g, sigma, a=0, b=2*np.pi):
    """
    Integral of exp[-(phi - phi_g)^2 / (4*sigma^2)] from a to b
    expressed in terms of error functions.

    = sqrt(pi) * sigma * sqrt(2) * [erf((b-phi_g)/(sqrt(2)*sigma)) - erf((a-phi_g)/(sqrt(2)*sigma))]
    """
    sqrt2_sigma = np.sqrt(2) * sigma
    return np.sqrt(np.pi) * sqrt2_sigma * (erf((b - phi_g) / sqrt2_sigma) - erf((a - phi_g) / sqrt2_sigma))

# For diagonal element Y_11 (phi_g = 0):
# Limits are [0, 2*pi], phi_g = 0
# erf((2*pi - 0)/(sqrt(2)*sigma)) - erf((0 - 0)/(sqrt(2)*sigma))
# = erf(2*pi/(sqrt(2)*sigma)) - erf(0)
# = erf(2*pi/(sqrt(2)*sigma))

sqrt2_sigma = np.sqrt(2) * sigma
x_upper = 2*np.pi / sqrt2_sigma
x_lower = 0 / sqrt2_sigma

print(f"\nFor generation 1 at phi=0:")
print(f"  sqrt(2)*sigma = {sqrt2_sigma:.6f}")
print(f"  Upper limit: 2*pi/(sqrt(2)*sigma) = {x_upper:.4f}")
print(f"  erf({x_upper:.4f}) = {erf(x_upper):.6f}")

# The fraction of the Gaussian within [0, 2*pi] compared to [-inf, +inf]
fraction_in_domain = 0.5 * (1 + erf(x_upper))  # since lower bound is at phi_g=0
print(f"  Fraction of |psi_1|^2 in [0, 2*pi): {fraction_in_domain:.6f}")

# For generation 2 at phi = 2*pi/3:
x_upper_2 = (2*np.pi - phi_2) / sqrt2_sigma
x_lower_2 = (0 - phi_2) / sqrt2_sigma
fraction_2 = 0.5 * (erf(x_upper_2) - erf(x_lower_2))
print(f"\nFor generation 2 at phi=2*pi/3:")
print(f"  Upper limit: (2*pi - 2*pi/3)/(sqrt(2)*sigma) = {x_upper_2:.4f}")
print(f"  Lower limit: (0 - 2*pi/3)/(sqrt(2)*sigma) = {x_lower_2:.4f}")
print(f"  Fraction of |psi_2|^2 in [0, 2*pi): {fraction_2:.6f}")

# ============================================================================
# PART 8: DETAILED OVERLAP INTEGRAL VIA ERROR FUNCTIONS
# ============================================================================

print("\n" + "-" * 50)
print("METHOD 4: Product of Gaussians (exact analytic)")
print("-" * 50)

# The product of two Gaussians is another Gaussian:
# exp[-(phi-phi_1)^2/(4*sigma^2)] * exp[-(phi-phi_2)^2/(4*sigma^2)]
# = exp[-((phi-phi_1)^2 + (phi-phi_2)^2)/(4*sigma^2)]
# = exp[-2*(phi - (phi_1+phi_2)/2)^2/(4*sigma^2) - (phi_2-phi_1)^2/(8*sigma^2)]
# = exp[-(phi_2-phi_1)^2/(8*sigma^2)] * exp[-(phi - phi_mid)^2/(2*sigma^2)]

phi_mid = (phi_1 + phi_2) / 2  # = pi/3
prefactor = np.exp(-Delta_12**2 / (8*sigma**2))  # = lambda_bare
new_sigma = sigma / np.sqrt(2)  # Effective width of product Gaussian

print(f"\nProduct of psi_1 and psi_2:")
print(f"  phi_mid = (phi_1 + phi_2)/2 = {phi_mid:.6f}")
print(f"  Prefactor = exp[-Delta^2/(8*sigma^2)] = {prefactor:.6f}")
print(f"  Effective sigma = sigma/sqrt(2) = {new_sigma:.6f}")

# Now integrate this product Gaussian from 0 to 2*pi
# = prefactor * sqrt(2*pi) * new_sigma * [erf((2*pi - phi_mid)/(sqrt(2)*new_sigma)) - erf((0 - phi_mid)/(sqrt(2)*new_sigma))] / 2

sqrt2_new_sigma = np.sqrt(2) * new_sigma
x_upper_prod = (2*np.pi - phi_mid) / sqrt2_new_sigma
x_lower_prod = (0 - phi_mid) / sqrt2_new_sigma

erf_factor = 0.5 * (erf(x_upper_prod) - erf(x_lower_prod))
Y_12_analytic = np.sqrt(2*np.pi) * new_sigma * prefactor * 2 * erf_factor

print(f"\nAnalytic overlap integral Y_12:")
print(f"  x_upper = (2*pi - phi_mid)/(sqrt(2)*sigma_eff) = {x_upper_prod:.4f}")
print(f"  x_lower = (0 - phi_mid)/(sqrt(2)*sigma_eff) = {x_lower_prod:.4f}")
print(f"  erf({x_upper_prod:.4f}) = {erf(x_upper_prod):.6f}")
print(f"  erf({x_lower_prod:.4f}) = {erf(x_lower_prod):.6f}")
print(f"  erf_factor = [erf(x_upper) - erf(x_lower)]/2 = {erf_factor:.6f}")
print(f"  Y_12 (analytic) = {Y_12_analytic:.6f}")

# Compare with numerical
print(f"  Y_12 (numerical) = {Y_11_trunc:.6f}")

# Infinite-domain result
Y_12_infinite = np.sqrt(2*np.pi) * new_sigma * prefactor * 2 * 0.5  # erf(inf) - erf(-inf) = 2
# Actually: erf_factor_inf = 0.5 * (1 - (-1)) = 1
Y_12_infinite = np.sqrt(2*np.pi) * new_sigma * prefactor

print(f"  Y_12 (infinite) = sqrt(2*pi) * sigma_eff * prefactor = {Y_12_infinite:.6f}")

f_boundary_analytic = (erf(x_upper_prod) - erf(x_lower_prod)) / 2
print(f"\nBoundary factor from erf: {f_boundary_analytic:.6f}")

# ============================================================================
# PART 9: THE ACTUAL YUKAWA RATIO CORRECTION
# ============================================================================

print("\n" + "=" * 70)
print("PART 9: THE ACTUAL YUKAWA RATIO CORRECTION")
print("=" * 70)

# For the mass hierarchy, we need the ratio:
# lambda_phys = Y_{12} / sqrt(Y_{11} * Y_{22})
#
# The boundary correction is:
# f_boundary = lambda_phys / lambda_ideal

# Compute Y_11 analytically (same generation overlap)
# phi_1 = 0, so the product is centered at 0
x_upper_11 = (2*np.pi - 0) / sqrt2_sigma
x_lower_11 = (0 - 0) / sqrt2_sigma
erf_factor_11 = 0.5 * (erf(x_upper_11) - erf(x_lower_11))
Y_11_analytic = np.sqrt(2*np.pi) * sigma * 2 * erf_factor_11  # No prefactor for same-generation

# Wait, for Y_11 with same wavefunctions:
# |psi_1|^2 = exp[-(phi - phi_1)^2 / (2*sigma^2)]
# Integral from 0 to 2*pi of this
x_upper_11 = 2*np.pi / sqrt2_sigma
x_lower_11 = 0 / sqrt2_sigma
erf_factor_11 = 0.5 * (erf(x_upper_11) - erf(x_lower_11))
# But erf(0) = 0, so:
erf_factor_11 = 0.5 * erf(x_upper_11)

# Actually we need to be more careful. Let me redo this properly.

# For psi_1(phi) = N_1 * exp[-(phi)^2/(4*sigma^2)]
# Y_11 = integral of |psi_1|^2 = N_1^2 * integral of exp[-(phi)^2/(2*sigma^2)]

# Infinite domain: integral = sqrt(2*pi) * sigma
# Finite domain [0, 2*pi]:

# Let's use numerical integration to be sure
print("\nDetailed calculation for Y_11, Y_22, Y_12:")

def full_overlap(phi_i, phi_j, sigma, domain=(0, 2*np.pi)):
    """Compute overlap integral with full analytic form where possible"""
    a, b = domain

    # Product of two Gaussians centered at phi_i, phi_j
    phi_mid = (phi_i + phi_j) / 2
    delta = abs(phi_j - phi_i)
    sigma_eff = sigma / np.sqrt(2)
    prefactor = np.exp(-delta**2 / (8 * sigma**2))

    # Integrate exp[-(phi - phi_mid)^2 / (2*sigma_eff^2)] from a to b
    sqrt2_sigma_eff = np.sqrt(2) * sigma_eff
    x_upper = (b - phi_mid) / sqrt2_sigma_eff
    x_lower = (a - phi_mid) / sqrt2_sigma_eff

    integral = np.sqrt(np.pi) * sqrt2_sigma_eff * (erf(x_upper) - erf(x_lower))

    return prefactor * integral, x_upper, x_lower

# Y_11 (phi_1 = 0)
Y_11_calc, x_up_11, x_lo_11 = full_overlap(0, 0, sigma)
print(f"\nY_11 (generation 1, phi=0):")
print(f"  phi_mid = 0, Delta = 0")
print(f"  x_upper = 2*pi/(sqrt(2)*sigma) = {x_up_11:.4f}")
print(f"  x_lower = 0 = {x_lo_11:.4f}")
print(f"  erf factor = erf({x_up_11:.3f}) - erf({x_lo_11:.3f}) = {erf(x_up_11) - erf(x_lo_11):.6f}")
print(f"  Y_11 = {Y_11_calc:.6f}")

# Y_22 (phi_2 = 2*pi/3)
Y_22_calc, x_up_22, x_lo_22 = full_overlap(phi_2, phi_2, sigma)
print(f"\nY_22 (generation 2, phi=2*pi/3):")
print(f"  phi_mid = 2*pi/3")
print(f"  x_upper = (2*pi - 2*pi/3)/(sqrt(2)*sigma) = {x_up_22:.4f}")
print(f"  x_lower = (0 - 2*pi/3)/(sqrt(2)*sigma) = {x_lo_22:.4f}")
print(f"  erf factor = erf({x_up_22:.3f}) - erf({x_lo_22:.3f}) = {erf(x_up_22) - erf(x_lo_22):.6f}")
print(f"  Y_22 = {Y_22_calc:.6f}")

# Y_12 (phi_1 = 0, phi_2 = 2*pi/3)
Y_12_calc, x_up_12, x_lo_12 = full_overlap(phi_1, phi_2, sigma)
print(f"\nY_12 (generations 1 and 2):")
print(f"  phi_mid = pi/3, Delta = 2*pi/3")
print(f"  prefactor = exp[-Delta^2/(8*sigma^2)] = {np.exp(-Delta_12**2/(8*sigma**2)):.6f}")
print(f"  x_upper = (2*pi - pi/3)/(sigma/sqrt(2)*sqrt(2)) = {x_up_12:.4f}")
print(f"  x_lower = (0 - pi/3)/... = {x_lo_12:.4f}")
print(f"  erf factor = erf({x_up_12:.3f}) - erf({x_lo_12:.3f}) = {erf(x_up_12) - erf(x_lo_12):.6f}")
print(f"  Y_12 = {Y_12_calc:.6f}")

# Infinite domain values
Y_11_inf = np.sqrt(2*np.pi) * sigma  # = sqrt(2*pi) * sigma * erf(inf) = sqrt(2*pi)*sigma
Y_22_inf = np.sqrt(2*np.pi) * sigma
Y_12_inf = np.sqrt(2*np.pi) * sigma * np.exp(-Delta_12**2/(8*sigma**2))

print(f"\nInfinite domain values:")
print(f"  Y_11_inf = sqrt(2*pi)*sigma = {Y_11_inf:.6f}")
print(f"  Y_22_inf = sqrt(2*pi)*sigma = {Y_22_inf:.6f}")
print(f"  Y_12_inf = sqrt(2*pi)*sigma * exp[-...] = {Y_12_inf:.6f}")

# Boundary correction factors for each
f_11 = Y_11_calc / Y_11_inf
f_22 = Y_22_calc / Y_22_inf
f_12 = Y_12_calc / Y_12_inf

print(f"\nIndividual boundary corrections:")
print(f"  f_11 = Y_11_finite / Y_11_infinite = {f_11:.6f}")
print(f"  f_22 = Y_22_finite / Y_22_infinite = {f_22:.6f}")
print(f"  f_12 = Y_12_finite / Y_12_infinite = {f_12:.6f}")

# The lambda ratio correction
# lambda_finite = Y_12_finite / sqrt(Y_11_finite * Y_22_finite)
# lambda_infinite = Y_12_infinite / sqrt(Y_11_infinite * Y_22_infinite)
# f_boundary = lambda_finite / lambda_infinite = (Y_12_f/Y_12_i) / sqrt((Y_11_f/Y_11_i)*(Y_22_f/Y_22_i))
#            = f_12 / sqrt(f_11 * f_22)

f_boundary_ratio = f_12 / np.sqrt(f_11 * f_22)

print(f"\n" + "=" * 70)
print("FINAL RESULT: BOUNDARY CORRECTION FACTOR")
print("=" * 70)
print(f"\n  f_boundary = f_12 / sqrt(f_11 * f_22)")
print(f"            = {f_12:.6f} / sqrt({f_11:.6f} * {f_22:.6f})")
print(f"            = {f_12:.6f} / {np.sqrt(f_11 * f_22):.6f}")
print(f"            = {f_boundary_ratio:.6f}")

# ============================================================================
# PART 10: SYSTEMATIC UNCERTAINTY ANALYSIS
# ============================================================================

print("\n" + "=" * 70)
print("PART 10: UNCERTAINTY ANALYSIS")
print("=" * 70)

# Vary kappa and compute the spread in f_boundary
kappa_range = np.linspace(2.0, 3.0, 11)
f_boundary_values = []

for k in kappa_range:
    s = (2 * np.pi / 3) / k
    d = phi_2 - phi_1

    Y_11, _, _ = full_overlap(0, 0, s)
    Y_22, _, _ = full_overlap(phi_2, phi_2, s)
    Y_12, _, _ = full_overlap(0, phi_2, s)

    Y_11_i = np.sqrt(2*np.pi) * s
    Y_22_i = np.sqrt(2*np.pi) * s
    Y_12_i = np.sqrt(2*np.pi) * s * np.exp(-d**2/(8*s**2))

    f_11 = Y_11 / Y_11_i
    f_22 = Y_22 / Y_22_i
    f_12 = Y_12 / Y_12_i

    fb = f_12 / np.sqrt(f_11 * f_22)
    f_boundary_values.append(fb)

print(f"\nVariation with kappa:")
for k, fb in zip(kappa_range, f_boundary_values):
    print(f"  kappa = {k:.1f}: f_boundary = {fb:.4f}")

mean_fb = np.mean(f_boundary_values)
std_fb = np.std(f_boundary_values)
print(f"\n  Mean: {mean_fb:.4f}")
print(f"  Std:  {std_fb:.4f}")

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

print(f"""
BOUNDARY CORRECTION FACTOR CALCULATION

Parameters:
  - Localization parameter: kappa = {kappa}
  - Gaussian width: sigma = 2*pi/(3*kappa) = {sigma:.4f} rad
  - Generation phases: phi_1=0, phi_2=2*pi/3, phi_3=4*pi/3
  - Domain: [0, 2*pi) with periodic boundary conditions

Results:

  1. Individual overlap truncation factors:
     f_11 = {f_11:.4f}  (diagonal, gen 1)
     f_22 = {f_22:.4f}  (diagonal, gen 2)
     f_12 = {f_12:.4f}  (off-diagonal, gen 1-2)

  2. Net boundary correction for Yukawa ratio:
     f_boundary = f_12 / sqrt(f_11 * f_22)
                = {f_boundary_ratio:.4f}

  3. Comparison with claimed value:
     Document claims: 0.65
     Calculated:      {f_boundary_ratio:.4f}
     Difference:      {abs(f_boundary_ratio - 0.65):.4f} ({100*abs(f_boundary_ratio - 0.65)/0.65:.1f}%)

  4. With kappa uncertainty (2.0 to 3.0):
     f_boundary = {mean_fb:.4f} +/- {std_fb:.4f}

CONCLUSION:
  The calculated boundary correction factor is {f_boundary_ratio:.3f}, which is
  SIGNIFICANTLY DIFFERENT from the claimed value of 0.65.

  The discrepancy is {abs(f_boundary_ratio - 0.65)/0.65*100:.0f}%, indicating that either:
  a) The document's value of 0.65 is incorrect
  b) Additional physics beyond simple Gaussian truncation is needed
  c) The definition of "boundary correction" differs from this calculation
""")

# ============================================================================
# PART 11: INVESTIGATE WHAT GIVES 0.65
# ============================================================================

print("\n" + "=" * 70)
print("PART 11: WHAT PARAMETERS WOULD GIVE f_boundary = 0.65?")
print("=" * 70)

def find_kappa_for_target(target_f, tolerance=0.001):
    """Find kappa that gives target boundary correction factor"""
    for k in np.linspace(0.5, 10.0, 1000):
        s = (2 * np.pi / 3) / k
        d = phi_2 - phi_1

        Y_11, _, _ = full_overlap(0, 0, s)
        Y_22, _, _ = full_overlap(phi_2, phi_2, s)
        Y_12, _, _ = full_overlap(0, phi_2, s)

        Y_11_i = np.sqrt(2*np.pi) * s
        Y_22_i = np.sqrt(2*np.pi) * s
        Y_12_i = np.sqrt(2*np.pi) * s * np.exp(-d**2/(8*s**2))

        if Y_11_i < 1e-10 or Y_22_i < 1e-10 or Y_12_i < 1e-10:
            continue

        f_11 = Y_11 / Y_11_i
        f_22 = Y_22 / Y_22_i
        f_12 = Y_12 / Y_12_i

        if f_11 * f_22 < 1e-10:
            continue

        fb = f_12 / np.sqrt(f_11 * f_22)

        if abs(fb - target_f) < tolerance:
            return k, s, fb
    return None, None, None

k_target, s_target, fb_actual = find_kappa_for_target(0.65)
if k_target:
    print(f"\nTo get f_boundary = 0.65 would require:")
    print(f"  kappa = {k_target:.2f}")
    print(f"  sigma = {s_target:.4f} rad")
    print(f"  (cf. kappa = 2.5 gives sigma = 0.838 rad)")
else:
    print(f"\nNo value of kappa in [0.5, 10.0] gives f_boundary = 0.65")
    print("The boundary correction from simple Gaussian truncation")
    print("cannot produce f_boundary = 0.65 for any reasonable kappa.")

# Try alternative model: sharp boundaries at Z_3 sectors
print("\n" + "-" * 50)
print("Alternative model: Z_3 sector restriction")
print("-" * 50)

# If we restrict integration to a single Z_3 sector [0, 2*pi/3):
# This represents the idea that wavefunctions are strictly confined

def sector_overlap(phi_i, phi_j, sigma, sector=(0, 2*np.pi/3)):
    """Overlap integral restricted to one Z_3 sector"""
    Y, _, _ = full_overlap(phi_i, phi_j, sigma, domain=sector)
    return Y

# For generations 1 and 2, their natural sector is centered on their position
# Gen 1 at phi=0 is in sector [-pi/3, pi/3] or [0, 2*pi/3) effectively [0, 2*pi/3)
# Gen 2 at phi=2*pi/3 is in sector [pi/3, pi]

# Let's compute with each generation in its own sector
sector_1 = (-np.pi/3, np.pi/3)  # Around phi=0, wrapping to [5*pi/3, 2*pi) + [0, pi/3)
sector_2 = (np.pi/3, np.pi)      # Around phi=2*pi/3

# Actually, better to use symmetric sectors around each generation center
# Gen 1: [-pi/3, pi/3] which is [5*pi/3, 2*pi) + [0, pi/3) = effectively needs periodic handling
# Let's use [0, 2*pi/3) for gen 1 (asymmetric but simple)

Y_11_sector, _, _ = full_overlap(0, 0, sigma, domain=(0, 2*np.pi/3))
Y_12_sector, _, _ = full_overlap(0, phi_2, sigma, domain=(0, 2*np.pi/3))

# This doesn't quite capture it either. Let me try the "interface reduction" model

print("\n" + "-" * 50)
print("Alternative model: Interface Gaussian damping")
print("-" * 50)

# Perhaps the 0.65 comes from including a damping factor at Z_3 boundaries
# where the R-field phase changes rapidly

def interface_damping_factor(phi, phi_g, sigma, interface_width=0.1):
    """
    Damping factor that reduces wavefunction amplitude near Z_3 boundaries
    Boundaries are at phi = 0, 2*pi/3, 4*pi/3
    """
    boundaries = [0, 2*np.pi/3, 4*np.pi/3, 2*np.pi]
    damping = 1.0
    for b in boundaries:
        dist = min(abs(phi - b), 2*np.pi - abs(phi - b))
        damping *= 1 - np.exp(-dist**2 / (2*interface_width**2)) * 0.5
    return damping

# This is getting too speculative. Let me just report the honest result.

print("""
The document's value of 0.65 cannot be reproduced from simple Gaussian
truncation at the [0, 2*pi) domain boundary.

Possible explanations for the discrepancy:
1. Additional "interface" effects at Z_3 phase boundaries
2. Holonomy phase factors not included in this calculation
3. The 0.65 may incorporate multiple effects together
4. The claimed value may simply be incorrect

Our calculation gives f_boundary = {:.3f} for kappa = 2.5.
""".format(f_boundary_ratio))
