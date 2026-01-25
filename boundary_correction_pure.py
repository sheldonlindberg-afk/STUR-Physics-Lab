#!/usr/bin/env python3
"""
BOUNDARY CORRECTION FACTOR CALCULATION - Pure Python Version
=============================================================

Computes the boundary correction factor from first principles using only
standard library functions (math module).

PHYSICAL SETUP:
- Three fermion generations at phi_1=0, phi_2=2*pi/3, phi_3=4*pi/3
- Gaussian wavefunctions with width sigma = (2*pi/3)/kappa
- Domain: [0, 2*pi) with Z_3 identification
"""

import math

# ============================================================================
# ERROR FUNCTION IMPLEMENTATION (since scipy not available)
# ============================================================================

def erf(x):
    """
    Error function implementation using Horner's method
    Based on Abramowitz and Stegun formula 7.1.26
    Maximum error: 1.5e-7
    """
    # Save the sign of x
    sign = 1 if x >= 0 else -1
    x = abs(x)

    # A&S formula 7.1.26
    t = 1.0 / (1.0 + 0.3275911 * x)
    y = 1.0 - (((((1.061405429 * t - 1.453152027) * t) + 1.421413741) * t - 0.284496736) * t + 0.254829592) * t * math.exp(-x * x)

    return sign * y

def gaussian(phi, phi_center, sigma):
    """Unnormalized Gaussian centered at phi_center"""
    return math.exp(-(phi - phi_center)**2 / (4 * sigma**2))

# ============================================================================
# NUMERICAL INTEGRATION (Simpson's rule)
# ============================================================================

def integrate(func, a, b, n=10000):
    """
    Numerical integration using Simpson's rule
    n must be even
    """
    if n % 2 == 1:
        n += 1
    h = (b - a) / n
    result = func(a) + func(b)

    for i in range(1, n, 2):  # Odd indices
        result += 4 * func(a + i * h)
    for i in range(2, n, 2):  # Even indices
        result += 2 * func(a + i * h)

    return result * h / 3

# ============================================================================
# PARAMETERS
# ============================================================================

kappa = 2.5
sigma = (2 * math.pi / 3) / kappa  # = 0.838 radians

phi_1 = 0.0
phi_2 = 2 * math.pi / 3
phi_3 = 4 * math.pi / 3

Delta_12 = phi_2 - phi_1  # = 2*pi/3

print("=" * 70)
print("BOUNDARY CORRECTION FACTOR CALCULATION")
print("=" * 70)
print(f"\nParameters:")
print(f"  kappa = {kappa}")
print(f"  sigma = 2*pi/(3*kappa) = {sigma:.6f} rad")
print(f"  Generation phases: phi_1={phi_1:.4f}, phi_2={phi_2:.4f}, phi_3={phi_3:.4f}")
print(f"  Delta_12 = 2*pi/3 = {Delta_12:.6f} rad")

# ============================================================================
# STEP 1: WRITE THE WAVEFUNCTIONS EXPLICITLY
# ============================================================================

print("\n" + "=" * 70)
print("STEP 1: GAUSSIAN WAVEFUNCTIONS")
print("=" * 70)

print(f"""
For generation g at phase phi_g:

    psi_g(phi) = N_g * exp[-(phi - phi_g)^2 / (4*sigma^2)]

where N_g is the normalization factor ensuring:

    integral_0^(2*pi) |psi_g(phi)|^2 dphi = 1

Explicitly for each generation:

    psi_1(phi) = N_1 * exp[-phi^2 / (4*{sigma:.4f}^2)]
               = N_1 * exp[-phi^2 / {4*sigma**2:.4f}]

    psi_2(phi) = N_2 * exp[-(phi - 2*pi/3)^2 / {4*sigma**2:.4f}]

    psi_3(phi) = N_3 * exp[-(phi - 4*pi/3)^2 / {4*sigma**2:.4f}]
""")

# ============================================================================
# STEP 2: THE OVERLAP INTEGRAL
# ============================================================================

print("=" * 70)
print("STEP 2: THE YUKAWA OVERLAP INTEGRAL")
print("=" * 70)

print(f"""
The Yukawa coupling between generations i and j is:

    Y_ij = y_0 * integral_0^(2*pi) psi_i*(phi) * H(phi) * psi_j(phi) dphi

Assuming constant Higgs profile H(phi) = h_0:

    Y_ij = y_0 * h_0 * integral_0^(2*pi) psi_i*(phi) * psi_j(phi) dphi

For normalized wavefunctions, this gives us the overlap:

    <psi_i | psi_j> = integral_0^(2*pi) psi_i*(phi) * psi_j(phi) dphi
""")

# ============================================================================
# STEP 3: ANALYTIC RESULT FOR PRODUCT OF GAUSSIANS
# ============================================================================

print("=" * 70)
print("STEP 3: PRODUCT OF TWO GAUSSIANS")
print("=" * 70)

print(f"""
The product of two Gaussians is another Gaussian:

    psi_i(phi) * psi_j(phi) = N_i * N_j * exp[-(phi-phi_i)^2/(4*sigma^2)]
                                       * exp[-(phi-phi_j)^2/(4*sigma^2)]

Using the identity:
    (phi-phi_i)^2 + (phi-phi_j)^2 = 2*(phi - phi_mid)^2 + Delta^2/2

where phi_mid = (phi_i + phi_j)/2 and Delta = |phi_j - phi_i|

We get:
    psi_i * psi_j = N_i * N_j * exp[-Delta^2/(8*sigma^2)]
                             * exp[-2*(phi - phi_mid)^2/(4*sigma^2)]
                 = N_i * N_j * exp[-Delta^2/(8*sigma^2)]
                             * exp[-(phi - phi_mid)^2/(2*sigma_eff^2)]

where sigma_eff = sigma/sqrt(2)
""")

# For generations 1 and 2:
phi_mid = (phi_1 + phi_2) / 2  # = pi/3
sigma_eff = sigma / math.sqrt(2)
prefactor = math.exp(-Delta_12**2 / (8 * sigma**2))

print(f"\nFor generations 1 and 2:")
print(f"  phi_mid = (0 + 2*pi/3)/2 = pi/3 = {phi_mid:.6f}")
print(f"  Delta = 2*pi/3 = {Delta_12:.6f}")
print(f"  sigma_eff = sigma/sqrt(2) = {sigma_eff:.6f}")
print(f"  Prefactor = exp[-Delta^2/(8*sigma^2)]")
print(f"            = exp[-{Delta_12**2/(8*sigma**2):.6f}]")
print(f"            = {prefactor:.6f}")

# ============================================================================
# STEP 4: ANALYTIC INTEGRAL USING ERROR FUNCTIONS
# ============================================================================

print("\n" + "=" * 70)
print("STEP 4: ANALYTIC INTEGRATION VIA ERROR FUNCTIONS")
print("=" * 70)

print(f"""
The integral of a Gaussian over a finite domain [a, b]:

    I = integral_a^b exp[-(phi - phi_center)^2 / (2*sigma^2)] dphi
      = sqrt(pi/2) * sigma * [erf((b - phi_center)/(sqrt(2)*sigma))
                            - erf((a - phi_center)/(sqrt(2)*sigma))]

For infinite domain:
    I_inf = sqrt(2*pi) * sigma   (when erf -> 1 at both limits)
""")

def analytic_overlap(phi_i, phi_j, sigma, a=0, b=2*math.pi):
    """
    Compute the overlap integral analytically using error functions.

    Returns the unnormalized integral:
        I = integral_a^b psi_i(phi) * psi_j(phi) dphi

    where psi_g(phi) = exp[-(phi - phi_g)^2 / (4*sigma^2)] (unnormalized)
    """
    # Product Gaussian parameters
    phi_mid = (phi_i + phi_j) / 2
    delta = abs(phi_j - phi_i)
    sigma_eff = sigma / math.sqrt(2)
    prefactor = math.exp(-delta**2 / (8 * sigma**2))

    # Integral of product Gaussian
    sqrt2_sigma_eff = math.sqrt(2) * sigma_eff
    x_upper = (b - phi_mid) / sqrt2_sigma_eff
    x_lower = (a - phi_mid) / sqrt2_sigma_eff

    erf_factor = erf(x_upper) - erf(x_lower)
    integral = math.sqrt(math.pi) * sqrt2_sigma_eff * erf_factor

    return prefactor * integral, erf_factor, x_upper, x_lower

# ============================================================================
# STEP 5: COMPUTE ALL OVERLAPS
# ============================================================================

print("=" * 70)
print("STEP 5: EXPLICIT OVERLAP CALCULATIONS")
print("=" * 70)

print("\n--- Y_11: Same generation (phi_1 = 0) ---")
Y_11, erf_11, x_up_11, x_lo_11 = analytic_overlap(0, 0, sigma)
print(f"  phi_mid = 0, Delta = 0")
print(f"  sigma_eff = sigma (since Delta=0 gives product psi^2)")
print(f"  x_upper = 2*pi / (sqrt(2)*sigma) = {x_up_11:.4f}")
print(f"  x_lower = 0 / (sqrt(2)*sigma) = {x_lo_11:.4f}")
print(f"  erf({x_up_11:.4f}) = {erf(x_up_11):.6f}")
print(f"  erf({x_lo_11:.4f}) = {erf(x_lo_11):.6f}")
print(f"  erf_factor = {erf_11:.6f}")
print(f"  Y_11 (finite domain) = {Y_11:.6f}")

# Infinite domain for Y_11
Y_11_inf = math.sqrt(2*math.pi) * sigma  # prefactor=1, full erf range = 2
print(f"  Y_11 (infinite domain) = sqrt(2*pi)*sigma = {Y_11_inf:.6f}")
print(f"  Ratio f_11 = Y_11_finite / Y_11_infinite = {Y_11/Y_11_inf:.6f}")

print("\n--- Y_22: Same generation (phi_2 = 2*pi/3) ---")
Y_22, erf_22, x_up_22, x_lo_22 = analytic_overlap(phi_2, phi_2, sigma)
print(f"  phi_mid = 2*pi/3")
print(f"  x_upper = (2*pi - 2*pi/3) / (sqrt(2)*sigma) = {x_up_22:.4f}")
print(f"  x_lower = (0 - 2*pi/3) / (sqrt(2)*sigma) = {x_lo_22:.4f}")
print(f"  erf({x_up_22:.4f}) = {erf(x_up_22):.6f}")
print(f"  erf({x_lo_22:.4f}) = {erf(x_lo_22):.6f}")
print(f"  erf_factor = {erf_22:.6f}")
print(f"  Y_22 (finite domain) = {Y_22:.6f}")

Y_22_inf = math.sqrt(2*math.pi) * sigma
print(f"  Y_22 (infinite domain) = {Y_22_inf:.6f}")
print(f"  Ratio f_22 = Y_22_finite / Y_22_infinite = {Y_22/Y_22_inf:.6f}")

print("\n--- Y_33: Same generation (phi_3 = 4*pi/3) ---")
Y_33, erf_33, x_up_33, x_lo_33 = analytic_overlap(phi_3, phi_3, sigma)
print(f"  phi_mid = 4*pi/3")
print(f"  x_upper = (2*pi - 4*pi/3) / (sqrt(2)*sigma) = {x_up_33:.4f}")
print(f"  x_lower = (0 - 4*pi/3) / (sqrt(2)*sigma) = {x_lo_33:.4f}")
print(f"  erf({x_up_33:.4f}) = {erf(x_up_33):.6f}")
print(f"  erf({x_lo_33:.4f}) = {erf(x_lo_33):.6f}")
print(f"  erf_factor = {erf_33:.6f}")
print(f"  Y_33 (finite domain) = {Y_33:.6f}")

Y_33_inf = math.sqrt(2*math.pi) * sigma
print(f"  Y_33 (infinite domain) = {Y_33_inf:.6f}")
print(f"  Ratio f_33 = Y_33_finite / Y_33_infinite = {Y_33/Y_33_inf:.6f}")

print("\n--- Y_12: Cross-generation (phi_1=0, phi_2=2*pi/3) ---")
Y_12, erf_12, x_up_12, x_lo_12 = analytic_overlap(phi_1, phi_2, sigma)
print(f"  phi_mid = pi/3 = {phi_mid:.6f}")
print(f"  Delta = 2*pi/3 = {Delta_12:.6f}")
print(f"  prefactor = exp[-Delta^2/(8*sigma^2)] = {prefactor:.6f}")
print(f"  sigma_eff = sigma/sqrt(2) = {sigma_eff:.6f}")
print(f"  x_upper = (2*pi - pi/3) / (sqrt(2)*sigma_eff) = {x_up_12:.4f}")
print(f"  x_lower = (0 - pi/3) / (sqrt(2)*sigma_eff) = {x_lo_12:.4f}")
print(f"  erf({x_up_12:.4f}) = {erf(x_up_12):.6f}")
print(f"  erf({x_lo_12:.4f}) = {erf(x_lo_12):.6f}")
print(f"  erf_factor = {erf_12:.6f}")
print(f"  Y_12 (finite domain) = {Y_12:.6f}")

Y_12_inf = math.sqrt(2*math.pi) * sigma_eff * prefactor * 2  # factor of 2 from erf range
# Actually: Y_12_inf = sqrt(pi) * sqrt(2) * sigma_eff * prefactor * 2 = sqrt(2*pi) * sigma_eff * prefactor
# No wait - let me recalculate properly
# For infinite domain: erf(+inf) - erf(-inf) = 1 - (-1) = 2
# So Y_12_inf = prefactor * sqrt(pi) * sqrt(2)*sigma_eff * 2 = prefactor * sqrt(2*pi) * sigma_eff * 2
# Hmm, that doesn't match the standard formula. Let me be more careful.

# The integral of exp[-(x-c)^2/(2*s^2)] from -inf to +inf is sqrt(2*pi)*s
# So for the product Gaussian with variance sigma_eff^2:
# Y_12_inf = prefactor * sqrt(2*pi) * sigma_eff
Y_12_inf = prefactor * math.sqrt(2*math.pi) * sigma_eff

print(f"  Y_12 (infinite domain) = prefactor * sqrt(2*pi) * sigma_eff")
print(f"                        = {prefactor:.6f} * sqrt(2*pi) * {sigma_eff:.6f}")
print(f"                        = {Y_12_inf:.6f}")
print(f"  Ratio f_12 = Y_12_finite / Y_12_infinite = {Y_12/Y_12_inf:.6f}")

# ============================================================================
# STEP 6: BOUNDARY CORRECTION FACTOR
# ============================================================================

print("\n" + "=" * 70)
print("STEP 6: BOUNDARY CORRECTION FACTOR")
print("=" * 70)

f_11 = Y_11 / Y_11_inf
f_22 = Y_22 / Y_22_inf
f_33 = Y_33 / Y_33_inf
f_12 = Y_12 / Y_12_inf

print(f"""
The Yukawa hierarchy parameter lambda is defined as:

    lambda = Y_12 / sqrt(Y_11 * Y_22)

The boundary correction factor is:

    f_boundary = lambda_finite / lambda_infinite
               = (Y_12_fin / sqrt(Y_11_fin * Y_22_fin))
               / (Y_12_inf / sqrt(Y_11_inf * Y_22_inf))
               = (Y_12_fin / Y_12_inf) / sqrt((Y_11_fin/Y_11_inf) * (Y_22_fin/Y_22_inf))
               = f_12 / sqrt(f_11 * f_22)

Substituting our calculated values:

    f_11 = {f_11:.6f}
    f_22 = {f_22:.6f}
    f_12 = {f_12:.6f}

    f_boundary = {f_12:.6f} / sqrt({f_11:.6f} * {f_22:.6f})
               = {f_12:.6f} / sqrt({f_11 * f_22:.6f})
               = {f_12:.6f} / {math.sqrt(f_11 * f_22):.6f}
               = {f_12 / math.sqrt(f_11 * f_22):.6f}
""")

f_boundary = f_12 / math.sqrt(f_11 * f_22)

# ============================================================================
# STEP 7: NUMERICAL VERIFICATION
# ============================================================================

print("=" * 70)
print("STEP 7: NUMERICAL VERIFICATION (Simpson's Rule)")
print("=" * 70)

def psi_unnorm(phi, phi_g):
    return math.exp(-(phi - phi_g)**2 / (4 * sigma**2))

# Numerical integrals
Y_11_num = integrate(lambda phi: psi_unnorm(phi, 0) * psi_unnorm(phi, 0), 0, 2*math.pi)
Y_22_num = integrate(lambda phi: psi_unnorm(phi, phi_2) * psi_unnorm(phi, phi_2), 0, 2*math.pi)
Y_12_num = integrate(lambda phi: psi_unnorm(phi, 0) * psi_unnorm(phi, phi_2), 0, 2*math.pi)

print(f"\nNumerical results (10000-point Simpson's rule):")
print(f"  Y_11 = {Y_11_num:.6f}  (analytic: {Y_11:.6f})")
print(f"  Y_22 = {Y_22_num:.6f}  (analytic: {Y_22:.6f})")
print(f"  Y_12 = {Y_12_num:.6f}  (analytic: {Y_12:.6f})")

f_11_num = Y_11_num / Y_11_inf
f_22_num = Y_22_num / Y_22_inf
f_12_num = Y_12_num / Y_12_inf
f_boundary_num = f_12_num / math.sqrt(f_11_num * f_22_num)

print(f"\nNumerical boundary correction:")
print(f"  f_boundary = {f_boundary_num:.6f}")

# ============================================================================
# STEP 8: ALTERNATIVE CALCULATION - NORMALIZED WAVEFUNCTIONS
# ============================================================================

print("\n" + "=" * 70)
print("STEP 8: NORMALIZED WAVEFUNCTION OVERLAP")
print("=" * 70)

# Compute normalization factors
norm_1_sq = integrate(lambda phi: psi_unnorm(phi, 0)**2, 0, 2*math.pi)
norm_2_sq = integrate(lambda phi: psi_unnorm(phi, phi_2)**2, 0, 2*math.pi)
N_1 = 1.0 / math.sqrt(norm_1_sq)
N_2 = 1.0 / math.sqrt(norm_2_sq)

print(f"\nNormalization factors (for unit norm on [0, 2*pi)):")
print(f"  N_1 = 1/sqrt(integral |psi_1|^2) = {N_1:.6f}")
print(f"  N_2 = 1/sqrt(integral |psi_2|^2) = {N_2:.6f}")

# Normalized overlap
lambda_finite_norm = N_1 * N_2 * Y_12_num

# For infinite domain with normalized Gaussians:
# |psi_g|^2 integrates to 1, so N_inf = 1/sqrt(sqrt(2*pi)*sigma)
N_inf = (2*math.pi)**(-0.25) * sigma**(-0.5)
lambda_infinite_norm = math.exp(-Delta_12**2 / (8*sigma**2))

print(f"\nNormalized overlap (= lambda):")
print(f"  lambda_finite = N_1 * N_2 * integral(psi_1 * psi_2)")
print(f"                = {N_1:.6f} * {N_2:.6f} * {Y_12_num:.6f}")
print(f"                = {lambda_finite_norm:.6f}")
print(f"\n  lambda_infinite = exp[-Delta^2/(8*sigma^2)]")
print(f"                  = exp[-{kappa**2/8:.6f}]")
print(f"                  = {lambda_infinite_norm:.6f}")

f_boundary_norm = lambda_finite_norm / lambda_infinite_norm
print(f"\n  f_boundary = lambda_finite / lambda_infinite")
print(f"             = {lambda_finite_norm:.6f} / {lambda_infinite_norm:.6f}")
print(f"             = {f_boundary_norm:.6f}")

# ============================================================================
# STEP 9: INCLUDE PERIODIC IMAGES (Z_3 STRUCTURE)
# ============================================================================

print("\n" + "=" * 70)
print("STEP 9: WITH PERIODIC IMAGES (Z_3 PERIODICITY)")
print("=" * 70)

def psi_periodic(phi, phi_g, n_images=3):
    """Gaussian with periodic images"""
    result = 0.0
    for n in range(-n_images, n_images + 1):
        result += math.exp(-(phi - phi_g - 2*math.pi*n)**2 / (4 * sigma**2))
    return result

# Numerical integrals with periodic images
Y_11_per = integrate(lambda phi: psi_periodic(phi, 0) * psi_periodic(phi, 0), 0, 2*math.pi)
Y_22_per = integrate(lambda phi: psi_periodic(phi, phi_2) * psi_periodic(phi, phi_2), 0, 2*math.pi)
Y_12_per = integrate(lambda phi: psi_periodic(phi, 0) * psi_periodic(phi, phi_2), 0, 2*math.pi)

print(f"\nWith periodic images:")
print(f"  Y_11 = {Y_11_per:.6f}")
print(f"  Y_22 = {Y_22_per:.6f}")
print(f"  Y_12 = {Y_12_per:.6f}")

# The infinite domain result doesn't change (images are at infinity)
f_11_per = Y_11_per / Y_11_inf
f_22_per = Y_22_per / Y_22_inf
f_12_per = Y_12_per / Y_12_inf
f_boundary_per = f_12_per / math.sqrt(f_11_per * f_22_per)

print(f"\n  f_11 = {f_11_per:.6f}")
print(f"  f_22 = {f_22_per:.6f}")
print(f"  f_12 = {f_12_per:.6f}")
print(f"  f_boundary = {f_boundary_per:.6f}")

# ============================================================================
# STEP 10: KAPPA SENSITIVITY
# ============================================================================

print("\n" + "=" * 70)
print("STEP 10: SENSITIVITY TO LOCALIZATION PARAMETER KAPPA")
print("=" * 70)

print("\nkappa  |  sigma    |  f_11   |  f_22   |  f_12   | f_boundary")
print("-" * 70)

for k in [1.5, 2.0, 2.5, 3.0, 3.5, 4.0]:
    s = (2 * math.pi / 3) / k
    s_eff = s / math.sqrt(2)
    pref = math.exp(-Delta_12**2 / (8 * s**2))

    # Compute overlaps using analytic formula
    def overlap_k(phi_i, phi_j):
        phi_m = (phi_i + phi_j) / 2
        delta = abs(phi_j - phi_i)
        s_e = s / math.sqrt(2)
        pf = math.exp(-delta**2 / (8 * s**2))

        sqrt2_s_e = math.sqrt(2) * s_e
        x_up = (2*math.pi - phi_m) / sqrt2_s_e
        x_lo = (0 - phi_m) / sqrt2_s_e

        erf_f = erf(x_up) - erf(x_lo)
        return pf * math.sqrt(math.pi) * sqrt2_s_e * erf_f

    Y11 = overlap_k(0, 0)
    Y22 = overlap_k(phi_2, phi_2)
    Y12 = overlap_k(0, phi_2)

    Y11_i = math.sqrt(2*math.pi) * s
    Y22_i = math.sqrt(2*math.pi) * s
    Y12_i = pref * math.sqrt(2*math.pi) * s_eff

    f11 = Y11 / Y11_i
    f22 = Y22 / Y22_i
    f12 = Y12 / Y12_i
    fb = f12 / math.sqrt(f11 * f22)

    print(f" {k:.1f}   |  {s:.4f}  |  {f11:.4f}  |  {f22:.4f}  |  {f12:.4f}  |   {fb:.4f}")

# ============================================================================
# FINAL SUMMARY
# ============================================================================

print("\n" + "=" * 70)
print("FINAL SUMMARY")
print("=" * 70)

print(f"""
BOUNDARY CORRECTION FACTOR CALCULATION FROM FIRST PRINCIPLES

Parameters:
  Localization parameter kappa = {kappa}
  Gaussian width sigma = 2*pi/(3*kappa) = {sigma:.4f} rad = {math.degrees(sigma):.2f} deg
  Generation phases: phi_1 = 0, phi_2 = 2*pi/3, phi_3 = 4*pi/3
  Domain: [0, 2*pi) with Z_3 identification

Key Overlap Integrals:

  Infinite domain:
    Y_11_inf = Y_22_inf = sqrt(2*pi)*sigma = {Y_11_inf:.4f}
    Y_12_inf = exp[-kappa^2/8] * sqrt(2*pi)*sigma/sqrt(2) = {Y_12_inf:.4f}

  Finite domain [0, 2*pi):
    Y_11 = {Y_11:.4f}   (via erf)
    Y_22 = {Y_22:.4f}   (via erf)
    Y_12 = {Y_12:.4f}   (via erf)

Truncation Factors:
    f_11 = Y_11/Y_11_inf = {f_11:.4f}
    f_22 = Y_22/Y_22_inf = {f_22:.4f}
    f_12 = Y_12/Y_12_inf = {f_12:.4f}

RESULT:
    f_boundary = f_12 / sqrt(f_11 * f_22)
               = {f_boundary:.4f}

COMPARISON:
    Document claims:    0.65
    This calculation:   {f_boundary:.4f}
    Discrepancy:        {100*abs(f_boundary - 0.65)/0.65:.1f}%

CONCLUSION:
    The calculated boundary correction factor is {f_boundary:.3f}, which differs
    significantly from the claimed value of 0.65.

    The discrepancy of ~{100*abs(f_boundary - 0.65):.0f}% suggests that either:
    1. Additional physics effects are included in the 0.65 (beyond Gaussian truncation)
    2. The value 0.65 may incorporate holonomy phase factors
    3. The claimed value may require revision

    An honest assessment: The boundary correction factor from pure Gaussian
    truncation at finite domain boundaries is approximately {f_boundary:.2f},
    NOT 0.65.
""")

# ============================================================================
# WHAT WOULD GIVE 0.65?
# ============================================================================

print("=" * 70)
print("APPENDIX: INVESTIGATING f_boundary = 0.65")
print("=" * 70)

# Could a different kappa give 0.65?
print("\nSearching for kappa that gives f_boundary = 0.65...")
found = False
for k in [x/100 for x in range(50, 1000)]:
    s = (2 * math.pi / 3) / k
    s_eff = s / math.sqrt(2)
    pref = math.exp(-Delta_12**2 / (8 * s**2))

    def overlap_search(phi_i, phi_j):
        phi_m = (phi_i + phi_j) / 2
        delta = abs(phi_j - phi_i)
        s_e = s / math.sqrt(2)
        pf = math.exp(-delta**2 / (8 * s**2))
        sqrt2_s_e = math.sqrt(2) * s_e
        x_up = (2*math.pi - phi_m) / sqrt2_s_e
        x_lo = (0 - phi_m) / sqrt2_s_e
        erf_f = erf(x_up) - erf(x_lo)
        return pf * math.sqrt(math.pi) * sqrt2_s_e * erf_f

    Y11 = overlap_search(0, 0)
    Y22 = overlap_search(phi_2, phi_2)
    Y12 = overlap_search(0, phi_2)

    Y11_i = math.sqrt(2*math.pi) * s
    Y22_i = math.sqrt(2*math.pi) * s
    Y12_i = pref * math.sqrt(2*math.pi) * s_eff

    if Y11_i < 1e-10 or Y22_i < 1e-10 or Y12_i < 1e-10:
        continue

    f11 = Y11 / Y11_i
    f22 = Y22 / Y22_i
    f12 = Y12 / Y12_i

    if f11 * f22 < 1e-10:
        continue

    fb = f12 / math.sqrt(f11 * f22)

    if abs(fb - 0.65) < 0.01:
        print(f"  Found: kappa = {k:.2f} gives f_boundary = {fb:.4f}")
        found = True
        break

if not found:
    print("  No value of kappa in [0.5, 10.0] gives f_boundary = 0.65")
    print("  The value 0.65 cannot arise from simple Gaussian boundary truncation.")
